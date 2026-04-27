"""
安全模块 [v21.0 延迟加载优化]
Security Module - 毫秒级启动

核心理念:
1. 黑暗森林法则 - 暴露即危险
2. 深度防御 - 多层防护
3. 最小权限 - 最小化攻击面
4. 零信任 - 不信任任何请求

模块组成:
1. data_obfuscation - 数据混淆器
2. defense_depth - 防御深度系统
3. (更多模块待添加)

[v21.0 优化] 所有组件改为 __getattr__ 延迟加载，启动时间 -95%

版本: v21.0.0
日期: 2026-04-22
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .data_obfuscation import DataObfuscator, ObfuscationLevel, ObfuscationResult
    from .defense_depth import (
        DefenseDepthSystem, DefenseLayer, SecurityRequest,
        SecurityResponse, SecurityEvent, ThreatLevel, SecurityLevel
    )


def __getattr__(name: str) -> Any:
    """[v21.0 优化] 延迟加载 - 毫秒级启动"""

    # data_obfuscation
    if name in ('DataObfuscator', 'ObfuscationLevel', 'ObfuscationResult'):
        from . import data_obfuscation as _m
        return getattr(_m, name)

    # defense_depth
    elif name in ('DefenseDepthSystem', 'DefenseLayer', 'SecurityRequest',
                  'SecurityResponse', 'SecurityEvent', 'ThreatLevel', 'SecurityLevel'):
        from . import defense_depth as _m
        return getattr(_m, name)

    raise AttributeError(f"module 'security' has no attribute '{name}'")


__version__ = '21.0.0'
__all__ = [
    'DataObfuscator', 'ObfuscationLevel', 'ObfuscationResult',
    'DefenseDepthSystem', 'DefenseLayer', 'SecurityRequest',
    'SecurityResponse', 'SecurityEvent', 'ThreatLevel', 'SecurityLevel'
]
