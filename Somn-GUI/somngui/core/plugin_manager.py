# -*- coding: utf-8 -*-
"""Somn GUI - 插件系统

提供轻量级插件加载与扩展框架：
- 从 plugins/ 目录自动发现并加载插件
- 支持 Qt 菜单扩展、工具栏按钮、侧边面板
- 插件通过 manifest.json 声明元数据
- 热加载/热卸载（开发模式）

插件目录结构:
  plugins/
    my_plugin/
      manifest.json    # 插件元数据
      plugin.py        # 插件入口
"""

from __future__ import annotations

import importlib
import importlib.util
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from loguru import logger


# ---------------------------------------------------------------------------
# 插件元数据
# ---------------------------------------------------------------------------

@dataclass
class PluginManifest:
    """插件清单"""
    id: str                          # 唯一标识 (如 "somn.plugin.todo")
    name: str                        # 显示名称
    version: str = "1.0.0"
    description: str = ""
    author: str = ""
    min_app_version: str = "1.0.0"   # 要求的最低应用版本
    entry: str = "plugin.py"         # 入口文件
    enabled: bool = True

    # 扩展点
    menu_items: List[dict] = field(default_factory=list)    # [{label, action, shortcut}]
    sidebar_panels: List[dict] = field(default_factory=list) # [{title, widget_class}]
    toolbar_buttons: List[dict] = field(default_factory=list) # [{icon, tooltip, action}]
    settings_fields: List[dict] = field(default_factory=list) # [{key, label, type, default}]

    @classmethod
    def from_dict(cls, data: dict) -> PluginManifest:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class PluginInstance:
    """已加载的插件实例"""
    manifest: PluginManifest
    module: Any = None
    path: Path = field(default_factory=Path)
    loaded: bool = False
    error: str = ""


# ---------------------------------------------------------------------------
# 插件钩子接口
# ---------------------------------------------------------------------------

class PluginHooks:
    """插件可实现的钩子方法（基类，插件继承此类）

    class MyPlugin(PluginHooks):
        def on_load(self, app_context):
            ...

        def on_unload(self):
            ...
    """

    def on_load(self, app_context: dict):
        """插件加载时调用

        app_context 包含:
          - main_window: QMainWindow 实例
          - state: AppState 实例
          - config: GUIConfig 实例
        """
        pass

    def on_unload(self):
        """插件卸载时调用"""
        pass

    def on_chat_message(self, role: str, content: str) -> Optional[str]:
        """聊天消息钩子，返回值将追加到消息中（或 None）"""
        return None

    def get_settings(self) -> dict:
        """返回插件设置"""
        return {}

    def on_settings_changed(self, settings: dict):
        """设置变更回调"""
        pass


# ---------------------------------------------------------------------------
# 插件管理器
# ---------------------------------------------------------------------------

class PluginManager:
    """插件管理器"""

    def __init__(self, plugins_dir: str | Path = "plugins"):
        self._plugins_dir = Path(plugins_dir)
        self._plugins: Dict[str, PluginInstance] = {}
        self._hooks: Dict[str, PluginHooks] = {}  # 插件 ID → 钩子实例

        # 回调列表
        self._on_plugin_loaded: List[Callable] = []
        self._on_plugin_unloaded: List[Callable] = []

    # ── 发现与加载 ──

    def discover(self) -> List[PluginManifest]:
        """扫描插件目录，发现所有插件（不加载）"""
        manifests = []
        if not self._plugins_dir.exists():
            logger.debug(f"插件目录不存在: {self._plugins_dir}")
            return manifests

        for plugin_dir in self._plugins_dir.iterdir():
            if not plugin_dir.is_dir():
                continue
            manifest_path = plugin_dir / "manifest.json"
            if not manifest_path.exists():
                continue
            try:
                data = json.loads(manifest_path.read_text(encoding="utf-8"))
                manifest = PluginManifest.from_dict(data)
                manifests.append(manifest)
            except Exception as e:
                logger.warning(f"插件清单解析失败 {manifest_path}: {e}")

        return manifests

    def load_all(self, app_context: dict | None = None):
        """加载所有已发现的插件"""
        manifests = self.discover()
        loaded = 0
        for manifest in manifests:
            if manifest.enabled:
                try:
                    self.load_plugin(manifest.id, app_context)
                    loaded += 1
                except Exception as e:
                    logger.error(f"插件 {manifest.id} 加载失败: {e}")
        logger.info(f"插件加载完成: {loaded}/{len(manifests)}")
        return loaded

    def load_plugin(self, plugin_id: str, app_context: dict | None = None) -> bool:
        """加载单个插件"""
        if plugin_id in self._plugins and self._plugins[plugin_id].loaded:
            logger.debug(f"插件已加载: {plugin_id}")
            return True

        # 查找插件目录
        plugin_dir = self._plugins_dir / plugin_id
        if not plugin_dir.exists():
            # 尝试按目录名查找
            for d in self._plugins_dir.iterdir():
                if d.is_dir():
                    mf = d / "manifest.json"
                    if mf.exists():
                        try:
                            data = json.loads(mf.read_text(encoding="utf-8"))
                            if data.get("id") == plugin_id:
                                plugin_dir = d
                                break
                        except Exception:
                            continue

        if not plugin_dir.exists():
            raise FileNotFoundError(f"插件目录不存在: {plugin_id}")

        # 解析清单
        manifest_path = plugin_dir / "manifest.json"
        manifest = PluginManifest.from_dict(
            json.loads(manifest_path.read_text(encoding="utf-8"))
        )

        # 动态加载模块
        entry_path = plugin_dir / manifest.entry
        if not entry_path.exists():
            raise FileNotFoundError(f"插件入口文件不存在: {entry_path}")

        spec = importlib.util.spec_from_file_location(
            f"somn_plugin_{manifest.id}", str(entry_path)
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        # 查找钩子实例
        hooks = None
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, PluginHooks) and attr is not PluginHooks:
                hooks = attr()
                break

        if hooks and app_context:
            try:
                hooks.on_load(app_context)
            except Exception as e:
                logger.warning(f"插件 {plugin_id} on_load 钩子失败: {e}")

        # 注册
        instance = PluginInstance(
            manifest=manifest,
            module=module,
            path=plugin_dir,
            loaded=True,
        )
        self._plugins[manifest.id] = instance
        if hooks:
            self._hooks[manifest.id] = hooks

        logger.info(f"插件已加载: {manifest.name} v{manifest.version}")
        for cb in self._on_plugin_loaded:
            try:
                cb(instance)
            except Exception as e:
                logger.warning(f"插件加载回调失败: {e}")

        return True

    def unload_plugin(self, plugin_id: str) -> bool:
        """卸载插件"""
        instance = self._plugins.get(plugin_id)
        if not instance:
            return False

        # 调用卸载钩子
        hooks = self._hooks.pop(plugin_id, None)
        if hooks:
            try:
                hooks.on_unload()
            except Exception as e:
                logger.warning(f"插件 {plugin_id} on_unload 钩子失败: {e}")

        instance.loaded = False

        # 清理模块
        if instance.module:
            mod_name = f"somn_plugin_{plugin_id}"
            sys.modules.pop(mod_name, None)

        for cb in self._on_plugin_unloaded:
            try:
                cb(instance)
            except Exception as e:
                logger.warning(f"插件卸载回调失败: {e}")

        logger.info(f"插件已卸载: {plugin_id}")
        return True

    # ── 钩子调用 ──

    def notify_chat_message(self, role: str, content: str) -> List[str]:
        """通知所有插件有新聊天消息"""
        extras = []
        for pid, hooks in self._hooks.items():
            try:
                result = hooks.on_chat_message(role, content)
                if result:
                    extras.append(result)
            except Exception as e:
                logger.warning(f"插件 {pid} 聊天钩子失败: {e}")
        return extras

    # ── 查询 ──

    @property
    def loaded_plugins(self) -> List[PluginInstance]:
        return [p for p in self._plugins.values() if p.loaded]

    @property
    def all_plugins(self) -> Dict[str, PluginInstance]:
        return dict(self._plugins)

    def get_plugin(self, plugin_id: str) -> Optional[PluginInstance]:
        return self._plugins.get(plugin_id)

    def is_loaded(self, plugin_id: str) -> bool:
        p = self._plugins.get(plugin_id)
        return p.loaded if p else False

    # ── 回调注册 ──

    def on_plugin_loaded(self, callback: Callable):
        self._on_plugin_loaded.append(callback)

    def on_plugin_unloaded(self, callback: Callable):
        self._on_plugin_unloaded.append(callback)

    # ── 清理 ──

    def unload_all(self):
        """卸载所有插件"""
        for plugin_id in list(self._plugins.keys()):
            self.unload_plugin(plugin_id)
        logger.info("所有插件已卸载")
