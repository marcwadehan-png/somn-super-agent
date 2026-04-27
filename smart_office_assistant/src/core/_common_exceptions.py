# -*- coding: utf-8 -*-
"""
Somn 统一异常体系 v1.0 [v22.0]

设计原则:
1. 轻量级 — 只定义核心异常层次, 不强制替换现有代码
2. 语义化 — 每个异常对应一类可操作的错误场景
3. 可追溯 — 所有异常支持 error_code + context 字段

使用方式:
    from src.core._common_exceptions import (
        SomnError, ConfigError, TimeoutExceededError,
        InitializationError, DataValidationError, ExternalServiceError
    )

    raise InitializationError(component="WisdomDispatcher", reason="学派引擎未注册")
"""

__all__ = [
    'SomnError',
    'SomnErrorCategory',
    'ConfigError',
    'InitializationError',
    'TimeoutExceededError',
    'DataValidationError',
    'ExternalServiceError',
    'StateError',
]


class SomnErrorCategory:
    """错误分类枚举"""
    CONFIG = "CONFIG"
    INITIALIZATION = "INIT"
    TIMEOUT = "TIMEOUT"
    VALIDATION = "VALIDATION"
    EXTERNAL = "EXTERNAL"
    INTERNAL = "INTERNAL"
    STATE = "STATE"


class SomnError(Exception):
    """Somn系统基础异常类
    
    所有Somn自定义异常的根类。提供统一的error_code、category、context字段。
    
    Attributes:
        message: 人类可读的错误描述
        error_code: 机器可读的错误码 (如 "INIT-001", "TIMEOUT-003")
        category: 错误分类 (SomnErrorCategory常量)
        context: 额外上下文信息字典
        component: 出错的组件名
    """
    
    _code_counter = {}  # 用于自动生成error_code
    
    def __init__(
        self,
        message: str,
        error_code: str = "",
        category: str = SomnErrorCategory.INTERNAL,
        component: str = "",
        context: dict | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self._auto_code()
        self.category = category
        self.component = component
        self.context = context or {}
    
    @classmethod
    def _auto_code(cls) -> str:
        """基于类名自动生成error_code"""
        name = cls.__name__
        if name == "SomnError":
            return "ERR-000"
        # 提取前缀: ConfigError -> CONFIG, InitError -> INIT
        prefix = name.replace("Error", "").upper()[:8]
        count = SomnError._code_counter.get(prefix, 0) + 1
        SomnError._code_counter[prefix] = count
        return f"{prefix}-{count:03d}"
    
    def __str__(self) -> str:
        parts = [f"[{self.error_code}]"]
        if self.component:
            parts.append(f"@{self.component}")
        parts.append(self.message)
        return " ".join(parts)
    
    def to_dict(self) -> dict:
        """转换为可序列化的字典(用于日志/跨进程传递)"""
        return {
            "error": self.__class__.__name__,
            "error_code": self.error_code,
            "category": self.category,
            "component": self.component,
            "message": self.message,
            "context": self.context,
        }


class ConfigError(SomnError):
    """配置错误 — 配置缺失、格式错误、值域非法等"""
    def __init__(self, message: str, config_key: str = "", **kwargs):
        super().__init__(
            message=message,
            category=SomnErrorCategory.CONFIG,
            **kwargs
        )
        self.config_key = config_key
        if config_key:
            self.context["config_key"] = config_key


class InitializationError(SomnError):
    """初始化错误 — 组件加载失败、依赖缺失、循环依赖等"""
    def __init__(self, message: str, component: str = "", **kwargs):
        kwargs.setdefault("category", SomnErrorCategory.INITIALIZATION)
        kwargs.setdefault("component", component)
        super().__init__(message=message, **kwargs)


class TimeoutExceededError(SomnError):
    """超时错误 — 操作超时、全局超时触发、降级等"""
    def __init__(self, message: str, timeout_seconds: float = 0.0, operation: str = "", **kwargs):
        super().__init__(
            message=message,
            category=SomnErrorCategory.TIMEOUT,
            **kwargs
        )
        self.timeout_seconds = timeout_seconds
        self.operation = operation
        if timeout_seconds:
            self.context["timeout_seconds"] = timeout_seconds
        if operation:
            self.context["operation"] = operation


class DataValidationError(SomnError):
    """数据验证错误 — 数据格式非法、值域越界、必填缺失等"""
    def __init__(self, message: str, field: str = "", value=None, **kwargs):
        super().__init__(
            message=message,
            category=SomnErrorCategory.VALIDATION,
            **kwargs
        )
        self.field = field
        if field:
            self.context["field"] = field
        if value is not None:
            self.context["value_repr"] = repr(value)[:200]


class ExternalServiceError(SomnError):
    """外部服务错误 — API调用失败、网络异常、第三方服务不可用等"""
    def __init__(self, message: str, service: str = "", status_code: int = 0, **kwargs):
        super().__init__(
            message=message,
            category=SomnErrorCategory.EXTERNAL,
            **kwargs
        )
        self.service = service
        self.status_code = status_code
        if service:
            self.context["service"] = service
        if status_code:
            self.context["status_code"] = status_code


class StateError(SomnError):
    """状态错误 — 对象处于不允许操作的状态、并发冲突等"""
    def __init__(self, message: str, expected_state: str = "", actual_state: str = "", **kwargs):
        super().__init__(
            message=message,
            category=SomnErrorCategory.STATE,
            **kwargs
        )
        if expected_state:
            self.context["expected_state"] = expected_state
        if actual_state:
            self.context["actual_state"] = actual_state
