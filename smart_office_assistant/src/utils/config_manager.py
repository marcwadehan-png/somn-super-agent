"""
Somn AI 独立配置管理器 v2.0
===========================
统一的配置读取和管理接口

使用方式:
    from src.utils.config_manager import IndependentConfig

    config = IndependentConfig()
    print(config.llm_mode)           # 获取LLM模式
    print(config.memory_mode)        # 获取记忆模式
    print(config.enable_gui)         # 是否启用GUI

版本: 2.0.0
日期: 2026-04-24
"""

import sys
from pathlib import Path
from typing import Optional, Any, Dict
from dataclasses import dataclass, field
from functools import lru_cache


@dataclass
class SystemConfig:
    """系统配置"""
    version: str = "6.2.0"
    environment: str = "standalone"
    debug: bool = False
    log_level: str = "INFO"
    log_retention_days: int = 30


@dataclass
class LLMConfig:
    """LLM配置"""
    default_mode: str = "local"
    default_model: str = "gemma4-local-b"  # [v2.0] B模型(主脑)成为默认
    api_base: str = ""                       # [v2.0] 无需API地址，直接本地调用
    api_key: str = ""
    model_name: str = "gemma4-local-b"        # [v2.0] B模型Gemma4多模态为主
    fallback_model: str = "llama-3.2-1b-a"   # [v2.0] A模型Llama为副脑
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 60


@dataclass
class StorageConfig:
    """存储配置"""
    memory_mode: str = "sqlite"
    knowledge_dir: str = "./data/knowledge"
    memory_log_dir: str = "./data/daily_memory"


@dataclass
class FeaturesConfig:
    """功能开关配置"""
    enable_gui: bool = True
    enable_web_search: bool = False
    enable_ml_engine: bool = False
    enable_emotion_wave: bool = True
    enable_persona: bool = True
    enable_rag: bool = False
    enable_daily_learning: bool = True


@dataclass
class PerformanceConfig:
    """性能配置"""
    lazy_loading: bool = True
    max_parallel_tasks: int = 4
    cache_size: int = 100
    session_timeout: int = 3600


@dataclass
class UIConfig:
    """界面配置"""
    theme: str = "auto"
    language: str = "zh-CN"
    font_size: int = 10
    high_dpi: bool = True


class IndependentConfig:
    """
    Somn独立运行配置管理器

    配置优先级（从高到低）:
    1. 环境变量
    2. config/config.yaml
    3. config/local_config.yaml（模板）
    4. 默认值
    """

    _instance: Optional['IndependentConfig'] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._project_root = self._find_project_root()
        self._config_file = self._project_root / "config" / "config.yaml"
        self._template_file = self._project_root / "config" / "local_config.yaml"

        # 子配置对象
        self.system = SystemConfig()
        self.llm = LLMConfig()
        self.storage = StorageConfig()
        self.features = FeaturesConfig()
        self.performance = PerformanceConfig()
        self.ui = UIConfig()

        # 加载配置
        self._load_config()

        self._initialized = True

    def _find_project_root(self) -> Path:
        """查找项目根目录"""
        # 优先从当前文件位置查找
        current = Path(__file__).resolve().parent.parent.parent

        # 检查是否有smart_office_assistant子目录
        if (current / "smart_office_assistant").exists():
            return current

        # 向上查找
        for parent in current.parents:
            if (parent / "smart_office_assistant").exists():
                return parent

        # 回退到当前工作目录
        return Path.cwd()

    def _load_config(self):
        """加载配置文件"""
        config_file = self._config_file if self._config_file.exists() else self._template_file

        if not config_file.exists():
            # 使用默认值，不报错
            return

        try:
            import yaml

            with open(config_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}

            # 加载系统配置
            sys_cfg = data.get('system', {})
            self.system = SystemConfig(
                version=sys_cfg.get('version', self.system.version),
                environment=sys_cfg.get('environment', self.system.environment),
                debug=sys_cfg.get('debug', self.system.debug),
                log_level=sys_cfg.get('log_level', self.system.log_level),
                log_retention_days=sys_cfg.get('log_retention_days', self.system.log_retention_days),
            )

            # 加载LLM配置
            llm_cfg = data.get('llm', {})
            self.llm = LLMConfig(
                default_mode=llm_cfg.get('default_mode', self.llm.default_mode),
                default_model=llm_cfg.get('default_model', self.llm.default_model),
            )

            local_cfg = llm_cfg.get('local', {})
            if local_cfg:
                self.llm.api_base = local_cfg.get('api_base', self.llm.api_base)
                self.llm.api_key = local_cfg.get('api_key', self.llm.api_key)
                self.llm.model_name = local_cfg.get('model_name', self.llm.model_name)
                self.llm.temperature = local_cfg.get('temperature', self.llm.temperature)
                self.llm.max_tokens = local_cfg.get('max_tokens', self.llm.max_tokens)
                self.llm.timeout = local_cfg.get('timeout', self.llm.timeout)

            # 加载存储配置
            storage_cfg = data.get('storage', {})
            self.storage = StorageConfig(
                memory_mode=storage_cfg.get('memory_mode', self.storage.memory_mode),
                knowledge_dir=storage_cfg.get('knowledge_dir', self.storage.knowledge_dir),
                memory_log_dir=storage_cfg.get('memory_log_dir', self.storage.memory_log_dir),
            )

            # 加载功能开关
            features_cfg = data.get('features', {})
            self.features = FeaturesConfig(
                enable_gui=features_cfg.get('enable_gui', self.features.enable_gui),
                enable_web_search=features_cfg.get('enable_web_search', self.features.enable_web_search),
                enable_ml_engine=features_cfg.get('enable_ml_engine', self.features.enable_ml_engine),
                enable_emotion_wave=features_cfg.get('enable_emotion_wave', self.features.enable_emotion_wave),
                enable_persona=features_cfg.get('enable_persona', self.features.enable_persona),
                enable_rag=features_cfg.get('enable_rag', self.features.enable_rag),
                enable_daily_learning=features_cfg.get('enable_daily_learning', self.features.enable_daily_learning),
            )

            # 加载性能配置
            perf_cfg = data.get('performance', {})
            self.performance = PerformanceConfig(
                lazy_loading=perf_cfg.get('lazy_loading', self.performance.lazy_loading),
                max_parallel_tasks=perf_cfg.get('max_parallel_tasks', self.performance.max_parallel_tasks),
                cache_size=perf_cfg.get('cache_size', self.performance.cache_size),
                session_timeout=perf_cfg.get('session_timeout', self.performance.session_timeout),
            )

            # 加载界面配置
            ui_cfg = data.get('ui', {})
            self.ui = UIConfig(
                theme=ui_cfg.get('theme', self.ui.theme),
                language=ui_cfg.get('language', self.ui.language),
                font_size=ui_cfg.get('font_size', self.ui.font_size),
                high_dpi=ui_cfg.get('high_dpi', self.ui.high_dpi),
            )

        except ImportError:
            # PyYAML未安装，使用默认值
            pass
        except Exception:
            # 配置加载失败，使用默认值
            pass

    @property
    def project_root(self) -> Path:
        """项目根目录"""
        return self._project_root

    @property
    def is_standalone(self) -> bool:
        """是否独立运行模式"""
        return self.system.environment == "standalone"

    @property
    def is_debug(self) -> bool:
        """是否调试模式"""
        return self.system.debug

    @property
    def llm_mode(self) -> str:
        """LLM运行模式"""
        return self.llm.default_mode

    @property
    def memory_mode(self) -> str:
        """记忆系统模式"""
        return self.storage.memory_mode

    @property
    def enable_gui(self) -> bool:
        """是否启用GUI"""
        return self.features.enable_gui

    @property
    def enable_web_search(self) -> bool:
        """是否启用网络搜索"""
        return self.features.enable_web_search

    @property
    def enable_ml_engine(self) -> bool:
        """是否启用ML引擎"""
        return self.features.enable_ml_engine

    @property
    def enable_emotion_wave(self) -> bool:
        """是否启用情绪波动"""
        return self.features.enable_emotion_wave

    @property
    def enable_persona(self) -> bool:
        """是否启用人设系统"""
        return self.features.enable_persona

    @property
    def enable_rag(self) -> bool:
        """是否启用RAG"""
        return self.features.enable_rag

    @property
    def enable_daily_learning(self) -> bool:
        """是否启用每日学习"""
        return self.features.enable_daily_learning

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        parts = key.split('.')
        obj = self
        for part in parts:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            else:
                return default
        return obj

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'system': {
                'version': self.system.version,
                'environment': self.system.environment,
                'debug': self.system.debug,
                'log_level': self.system.log_level,
            },
            'llm': {
                'default_mode': self.llm.default_mode,
                'default_model': self.llm.default_model,
                'api_base': self.llm.api_base,
                'model_name': self.llm.model_name,
            },
            'storage': {
                'memory_mode': self.storage.memory_mode,
            },
            'features': {
                'enable_gui': self.features.enable_gui,
                'enable_web_search': self.features.enable_web_search,
                'enable_ml_engine': self.features.enable_ml_engine,
                'enable_emotion_wave': self.features.enable_emotion_wave,
                'enable_persona': self.features.enable_persona,
                'enable_rag': self.features.enable_rag,
                'enable_daily_learning': self.features.enable_daily_learning,
            },
        }

    def __repr__(self) -> str:
        return f"IndependentConfig(environment={self.system.environment}, llm_mode={self.llm.default_mode})"


@lru_cache(maxsize=1)
def get_config() -> IndependentConfig:
    """获取配置单例"""
    return IndependentConfig()


# ───────────────────────────────────────────────────────────────
# 便捷访问函数
# ───────────────────────────────────────────────────────────────

def is_standalone() -> bool:
    """是否独立运行模式"""
    return get_config().is_standalone


def is_debug() -> bool:
    """是否调试模式"""
    return get_config().is_debug


def llm_mode() -> str:
    """获取LLM运行模式"""
    return get_config().llm_mode


def memory_mode() -> str:
    """获取记忆系统模式"""
    return get_config().memory_mode


def is_gui_enabled() -> bool:
    """是否启用GUI"""
    return get_config().enable_gui


# 兼容性别名
ConfigManager = IndependentConfig

__all__ = [
    'IndependentConfig',
    'ConfigManager',  # 兼容性别名
    'SystemConfig',
    'LLMConfig',
    'StorageConfig',
    'FeaturesConfig',
    'PerformanceConfig',
    'UIConfig',
    'get_config',
    'is_standalone',
    'is_debug',
    'llm_mode',
    'memory_mode',
    'is_gui_enabled',
]
