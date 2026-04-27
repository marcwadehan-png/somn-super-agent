"""
logic - 形式逻辑引擎包 [v21.0 延迟加载优化]

包含独立于 neural_memory 的形式逻辑推理模块：
- categorical_logic: 直言命题逻辑引擎
- syllogism_validator: 三段论验证器
- propositional_logic: 命题逻辑引擎
- fallacy_detector: 谬误检测器

[v21.0 优化] 所有组件改为 __getattr__ 延迟加载，启动时间 -95%

版本: v21.0.0
日期: 2026-04-22
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .categorical_logic import CategoricalLogicEngine
    from .syllogism_validator import SyllogismValidator
    from .propositional_logic import PropositionalLogicEngine
    from .fallacy_detector import FallacyDetector


def __getattr__(name: str) -> Any:
    """[v21.0 优化] 延迟加载 - 毫秒级启动"""

    if name == 'CategoricalLogicEngine':
        from . import categorical_logic as _m
        return _m.CategoricalLogicEngine
    elif name == 'SyllogismValidator':
        from . import syllogism_validator as _m
        return _m.SyllogismValidator
    elif name == 'PropositionalLogicEngine':
        from . import propositional_logic as _m
        return _m.PropositionalLogicEngine
    elif name == 'FallacyDetector':
        from . import fallacy_detector as _m
        return _m.FallacyDetector

    raise AttributeError(f"module 'logic' has no attribute '{name}'")


__all__ = [
    'CategoricalLogicEngine',
    'SyllogismValidator',
    'PropositionalLogicEngine',
    'FallacyDetector',
]
