"""
__all__ = [
    'config',
    'config_path',
    'get',
    'get_cross_config',
    'get_default_mode',
    'get_instance',
    'get_main_chain_config',
    'get_mode_decision_config',
    'get_monitor_config',
    'get_parallel_config',
    'is_enabled',
    'reload',
    'get_storage_config',
    'StorageConfig',
]

主线配置加载器
自动加载 config/main_chain_config.yaml 并提供配置访问接口

存储配置：
- config/storage_config.yaml 提供统一的存储架构配置
- 包括运行数据库、日志数据库、藏书阁备份配置
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import threading

logger = logging.getLogger(__name__)

class MainChainConfig:
    """主线配置单例"""

    _instance: Optional["MainChainConfig"] = None
    _lock = threading.Lock()

    def __init__(self):
        self._config: Dict[str, Any] = {}
        self._loaded = False
        self._config_path = None
        self._load_config()

    @classmethod
    def get_instance(cls) -> "MainChainConfig":
        """获取配置单例"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def _load_config(self):
        """加载配置文件"""
        if self._loaded:
            return

        # 查找配置文件（动态路径）
        try:
            from src.core.paths import PROJECT_ROOT
            _root = PROJECT_ROOT
        except ImportError:
            _root = Path(__file__).resolve().parent.parent.parent

        possible_paths = [
            _root / "config" / "main_chain_config.yaml",
            Path(__file__).resolve().parent.parent.parent / "config" / "main_chain_config.yaml",
        ]

        for path in possible_paths:
            if path.exists():
                self._config_path = path
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        self._config = yaml.safe_load(f) or {}
                    self._loaded = True
                    logger.info(f"[主线配置] 加载成功: {path}")
                    return
                except Exception as e:
                    logger.warning(f"[主线配置] 加载失败: {e}")

        # 使用默认配置
        self._config = self._get_default_config()
        self._loaded = True
        logger.info("[主线配置] 使用默认配置")

    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "main_chain_enabled": True,
            "default_mode": "auto",
            "log_level": "INFO",
            "parallel_router": {
                "max_concurrent": 5,
                "timeout": 30.0,
                "strategy": "best_k",
                "mode": "auto",
                "enable_fallback": True,
                "fallback_on_error": True,
            },
            "cross_weaver": {
                "max_iterations": 3,
                "max_hops": 3,
            },
            "main_chain_scheduler": {
                "mode": "auto",
                "history_size": 100,
                "enable_parallel": True,
                "enable_cross": True,
            },
            "main_chain_monitor": {
                "max_history": 100,
                "sampling_interval": 60,
            },
            "mode_decision": {
                "complexity": {
                    "parallel_threshold": 0.7,
                    "serial_threshold": 0.5,
                },
            },
        }

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值（支持点号分隔）"""
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def is_enabled(self) -> bool:
        """主线架构是否启用"""
        return self.get("main_chain_enabled", True)

    def get_default_mode(self) -> str:
        """获取默认运行模式"""
        return self.get("default_mode", "auto")

    def get_parallel_config(self) -> Dict[str, Any]:
        """获取并行路由器配置"""
        return self.get("parallel_router", {})

    def get_cross_config(self) -> Dict[str, Any]:
        """获取交叉织网器配置"""
        return self.get("cross_weaver", {})

    def get_monitor_config(self) -> Dict[str, Any]:
        """获取监控器配置"""
        return self.get("main_chain_monitor", {})

    def get_mode_decision_config(self) -> Dict[str, Any]:
        """获取模式决策配置"""
        return self.get("mode_decision", {})

    def reload(self):
        """重新加载配置"""
        self._loaded = False
        self._load_config()

    @property
    def config(self) -> Dict[str, Any]:
        """获取完整配置"""
        return self._config.copy()

    @property
    def config_path(self) -> Optional[Path]:
        """获取配置路径"""
        return self._config_path

# 全局配置实例
_config: Optional[MainChainConfig] = None

def get_main_chain_config() -> MainChainConfig:
    """获取主线配置单例"""
    global _config
    if _config is None:
        _config = MainChainConfig.get_instance()
    return _config


# ==================== 存储配置 ====================

class StorageConfig:
    """存储配置单例"""
    
    _instance: Optional["StorageConfig"] = None
    _lock = threading.Lock()
    
    def __init__(self):
        self._config: Dict[str, Any] = {}
        self._loaded = False
        self._config_path = None
        self._load_config()
    
    @classmethod
    def get_instance(cls) -> "StorageConfig":
        """获取配置单例"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    def _load_config(self):
        """加载存储配置文件"""
        if self._loaded:
            return
        
        try:
            from src.core.paths import PROJECT_ROOT
            _root = PROJECT_ROOT
        except ImportError:
            _root = Path(__file__).resolve().parent.parent.parent
        
        possible_paths = [
            _root / "config" / "storage_config.yaml",
            Path(__file__).resolve().parent.parent.parent / "config" / "storage_config.yaml",
        ]
        
        for path in possible_paths:
            if path.exists():
                self._config_path = path
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        self._config = yaml.safe_load(f) or {}
                    self._loaded = True
                    logger.info(f"[存储配置] 加载成功: {path}")
                    return
                except Exception as e:
                    logger.warning(f"[存储配置] 加载失败: {e}")
        
        # 使用默认配置
        self._config = self._get_default_config()
        self._loaded = True
        logger.info("[存储配置] 使用默认配置")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认存储配置"""
        try:
            from src.core.paths import PROJECT_ROOT
            _root = PROJECT_ROOT
        except ImportError:
            _root = Path(__file__).resolve().parent.parent.parent
        
        return {
            "paths": {
                "project_root": str(_root),
                "run_dir": "data/run",
                "log_dir": "data/logs",
                "core_dir": "data/core",
                "backup_dir": "data/backups",
                "imperial_library": "data/imperial_library",
            },
            "databases": {
                "run_db": {"enabled": True, "path": "data/run/run.db"},
                "log_db": {"enabled": True, "path": "data/logs/logs.db"},
            },
            "imperial_library_backup": {
                "enabled": True,
                "backup_tiers": {
                    "JIA": {"retention": None},
                    "YI": {"retention_days": 365},
                    "BING": {"retention_days": 30},
                    "DING": {"retention_days": 7},
                }
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值（支持点号分隔）"""
        keys = key.split(".")
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    @property
    def config(self) -> Dict[str, Any]:
        """获取完整配置"""
        return self._config.copy()
    
    @property
    def config_path(self) -> Optional[Path]:
        """获取配置路径"""
        return self._config_path
    
    def get_path(self, key: str) -> Path:
        """获取配置路径（自动拼接项目根目录）"""
        try:
            from src.core.paths import PROJECT_ROOT
            _root = PROJECT_ROOT
        except ImportError:
            _root = Path(__file__).resolve().parent.parent.parent
        
        relative_path = self.get(f"paths.{key}", "")
        if relative_path:
            return _root / relative_path
        return _root


def get_storage_config() -> StorageConfig:
    """获取存储配置单例"""
    return StorageConfig.get_instance()
