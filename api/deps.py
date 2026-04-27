"""
Somn API Server - 依赖注入
提供 SomnCore 实例等共享依赖
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class AppState:
    """API应用全局状态"""

    def __init__(self):
        self._somn_core = None
        self._agent_core = None
        self._project_root: Optional[Path] = None
        self._config: dict = {}
        self._start_time = None

    def initialize(self, project_root: Path, config: dict):
        """初始化应用状态"""
        self._project_root = project_root
        self._config = config
        self._start_time = time.time()
        logger.info(f"AppState 初始化完成, 项目根: {project_root}")

        # 启动系统资源监控
        try:
            import sys
            src_root = project_root / "smart_office_assistant" / "src"
            if str(src_root) not in sys.path:
                sys.path.insert(0, str(src_root))
            from system_monitor import start_system_monitoring
            start_system_monitoring(check_interval=60.0)
            logger.info("[系统监控] 已启动")
        except Exception as e:
            logger.warning(f"[系统监控] 启动失败: {e}")

    @property
    def project_root(self) -> Path:
        return self._project_root

    @property
    def config(self) -> dict:
        return self._config

    @property
    def start_time(self) -> float:
        return self._start_time

    def shutdown(self):
        """关闭应用状态（停止系统监控等）"""
        try:
            from system_monitor import stop_system_monitoring
            stop_system_monitoring()
            logger.info("[系统监控] 已停止")
        except Exception as e:
            logger.warning(f"[系统监控] 停止失败: {e}")

    def get_somn_core(self):
        """获取 SomnCore 实例 (延迟加载)"""
        if self._somn_core is None:
            self._somn_core = self._create_somn_core()
        return self._somn_core

    def _create_somn_core(self, timeout: float = 120.0):
        """延迟创建 SomnCore（修复版：添加超时保护）"""
        import sys
        from pathlib import Path
        
        # 确保 timeout_utils 在 sys.path 中
        src_root = self._project_root / "smart_office_assistant" / "src"
        if str(src_root) not in sys.path:
            sys.path.insert(0, str(src_root))
        
        from timeout_utils import run_with_timeout, TimeoutException
        
        start = time.time()
        logger.info(f"正在创建 SomnCore 实例（超时: {timeout}s）...")

        try:
            def _do_create():
                """内部创建函数"""
                import sys
                
                # 使用动态路径设置 sys.path（确保新线程也能访问）
                src_path = str(self._project_root / "smart_office_assistant" / "src")
                if src_path not in sys.path:
                    sys.path.insert(0, src_path)
                
                from src.core.somn_core import SomnCore
                return SomnCore()
            
            # 使用超时保护执行创建
            core = run_with_timeout(_do_create, timeout=timeout, DESCRIPTION="SomnCore创建")
            
            elapsed = time.time() - start
            logger.info(f"✅ SomnCore 创建完成（耗时 {elapsed:.2f}s）")
            return core
            
        except TimeoutException as e:
            elapsed = time.time() - start
            logger.error(f"❌ SomnCore 创建超时（耗时 {elapsed:.2f}s）: {e}")
            raise TimeoutError(f"SomnCore 创建超时（{timeout}秒），请检查系统配置")
        except Exception as e:
            elapsed = time.time() - start
            logger.error(f"❌ SomnCore 创建失败（耗时 {elapsed:.2f}s）: {e}")
            raise

    def get_agent_core(self):
        """获取 AgentCore 实例 (延迟加载)"""
        if self._agent_core is None:
            self._agent_core = self._create_agent_core()
        return self._agent_core

    def _create_agent_core(self):
        """延迟创建 AgentCore"""
        start = time.time()
        logger.info("正在创建 AgentCore 实例...")

        try:
            import sys
            pkg_root = self._project_root / "smart_office_assistant"
            src_root = pkg_root / "src"
            if str(pkg_root) not in sys.path:
                sys.path.insert(0, str(pkg_root))
            if str(src_root) not in sys.path:
                sys.path.insert(0, str(src_root))

            from src.core.memory_system import MemorySystem
            from src.core.knowledge_base import KnowledgeBase
            from src.core.agent_core import AgentCore

            # 使用项目根目录下的绝对路径，避免相对路径问题
            data_root = self._project_root / "smart_office_assistant" / "data"
            data_root.mkdir(parents=True, exist_ok=True)

            memory = MemorySystem(data_path=str(data_root / "memory"))
            kb = KnowledgeBase(data_path=str(data_root / "knowledge"))
            agent = AgentCore(memory, kb)
            elapsed = time.time() - start
            logger.info(f"AgentCore 创建完成 ({elapsed:.2f}s)")
            return agent
        except Exception as e:
            logger.error(f"AgentCore 创建失败: {e}")
            raise

    def get_safe_config(self) -> dict:
        """获取可安全暴露给前端的配置子集"""
        full_config = {}
        try:
            import yaml
            cfg_path = self._project_root / "smart_office_assistant" / "config.yaml"
            if cfg_path.exists():
                with open(cfg_path, "r", encoding="utf-8") as f:
                    full_config.update(yaml.safe_load(f) or {})

            local_cfg = self._project_root / "config" / "local_config.yaml"
            if local_cfg.exists():
                with open(local_cfg, "r", encoding="utf-8") as f:
                    local = yaml.safe_load(f) or {}
                    for key in ["ui", "features"]:
                        if key in local:
                            full_config[key] = local[key]
        except Exception as e:
            logger.warning(f"配置读取失败: {e}")

        # 安全过滤
        safe_keys = {"ui", "features", "learning"}
        filtered = {}
        for key in safe_keys:
            if key in full_config:
                filtered[key] = full_config[key]

        return filtered


# 全局单例
_app_state: Optional[AppState] = None


def get_app_state() -> AppState:
    """获取全局应用状态"""
    global _app_state
    if _app_state is None:
        _app_state = AppState()
    return _app_state


def init_app_state(project_root: Path, config: dict):
    """初始化全局应用状态"""
    global _app_state
    _app_state = AppState()
    _app_state.initialize(project_root, config)
    return _app_state
