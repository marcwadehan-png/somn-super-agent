"""
思维方法引擎 (Thinking Method Engine) - 兼容层

本文件已拆分为子包:
- src/intelligence/scheduler/thinking_method/

请使用以下方式导入:
    from src.intelligence.scheduler.thinking_method import ThinkingMethodEngine, analyze_thinking_method

原文件内容请参考 thinking_method/ 子包中的模块。
"""

# 重新导出所有公共接口
from src.intelligence.scheduler.thinking_method import (
    ThinkingMethod,
    ThinkingDepth,
    ThinkingAnalysis,
    ThinkingPath,
    MethodSuggestion,
    ThinkingMethodResult,
    ThinkingMethodEngine,
)

# 便捷函数和融合引擎
from src.intelligence.scheduler.thinking_method._tme_engine import (
    analyze_thinking_method,
    ThinkingMethodFusionEngine,
)

__all__ = [
    'ThinkingMethod',
    'ThinkingDepth',
    'ThinkingAnalysis',
    'ThinkingPath',
    'MethodSuggestion',
    'ThinkingMethodResult',
    'ThinkingMethodEngine',
    'ThinkingMethodFusionEngine',
    'analyze_thinking_method',
]
