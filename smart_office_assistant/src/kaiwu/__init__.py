"""
开物子系统 v1.0 - PPT 智能生成与风格学习

命名来源：《天工开物》（宋应星，明代工艺百科全书）
寓意：将工艺、设计、排版等知识系统化，如同开物般精细。

核心能力：
1. PPT 演示文稿生成（基于 python-pptx）
2. 设计风格智能学习（来自 learning/engine/ppt_style_learner.py）
3. 配色方案学习与评估
4. 排版模式学习与推荐
5. 基于反馈的持续优化

惰性加载：首次访问 KaiwuService 时才导入重型依赖。
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .kaiwu_service import KaiwuService
    from .kaiwu_service import PPTDesignKnowledge, PPTStyleProfile
    from .style_learner_wrapper import StyleLearnerWrapper

def __getattr__(name: str) -> Any:
    """惰性加载开物子系统模块"""

    # KaiwuService - 主服务类
    if name in ('KaiwuService',):
        from . import kaiwu_service as _m
        return getattr(_m, name)

    # 风格学习器包装器
    if name in ('StyleLearnerWrapper',):
        from . import style_learner_wrapper as _m
        return getattr(_m, name)

    # 数据类
    if name in ('PPTDesignKnowledge', 'PPTStyleProfile'):
        from .kaiwu_service import PPTDesignKnowledge, PPTStyleProfile
        return locals()[name]

    raise AttributeError(f"module 'kaiwu' has no attribute '{name}'")

__all__ = [
    'KaiwuService',
    'StyleLearnerWrapper',
    'PPTDesignKnowledge',
    'PPTStyleProfile',
]
