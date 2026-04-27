"""
Somn GUI - 配置管理

v1.0.0: yaml 延迟导入 + __init__ 不再同步调用 load()，
减少启动时 yaml 库导入开销和文件 I/O 阻塞。
配置在首次 get() 时自动加载（延迟加载模式）。
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

_DEFAULT_CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "gui_config.yaml"


class GUIConfig:
    """前端配置管理器"""

    def __init__(self, config_path: str = None):
        self._config_path = Path(config_path) if config_path else _DEFAULT_CONFIG_PATH
        self._config: Dict[str, Any] = {}
        self._loaded = False
        # v1.0.0: 不再同步调用 self.load()，延迟到首次 get() 时加载

    def _ensure_loaded(self):
        """延迟加载 — 首次访问配置时才读取文件"""
        if self._loaded:
            return
        self._loaded = True
        self.load()

    def load(self):
        """加载配置文件"""
        import yaml  # v1.0.0: 延迟导入 yaml（~30-50ms）
        if self._config_path.exists():
            try:
                with open(self._config_path, "r", encoding="utf-8") as f:
                    self._config = yaml.safe_load(f) or {}
                logger.info(f"配置已加载: {self._config_path}")
            except Exception as e:
                logger.error(f"配置加载失败: {e}")
                self._config = {}
        else:
            logger.warning(f"配置文件不存在: {self._config_path}，使用默认配置")

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值 (支持嵌套key, 如 'ui.theme')"""
        self._ensure_loaded()  # v1.0.0: 延迟加载
        parts = key.split(".")
        obj = self._config
        for p in parts:
            if isinstance(obj, dict) and p in obj:
                obj = obj[p]
            else:
                return default
        return obj

    def set(self, key: str, value: Any):
        """设置配置值"""
        self._ensure_loaded()
        parts = key.split(".")
        obj = self._config
        for p in parts[:-1]:
            if p not in obj or not isinstance(obj[p], dict):
                obj[p] = {}
            obj = obj[p]
        obj[parts[-1]] = value

    def save(self):
        """保存配置到文件"""
        import yaml  # v1.0.0: 延迟导入 yaml
        self._ensure_loaded()
        self._config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._config_path, "w", encoding="utf-8") as f:
            yaml.dump(self._config, f, allow_unicode=True, default_flow_style=False)
        logger.info(f"配置已保存: {self._config_path}")

    @property
    def raw(self) -> dict:
        self._ensure_loaded()
        return self._config
