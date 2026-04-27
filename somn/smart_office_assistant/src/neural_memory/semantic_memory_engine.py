"""
__all__ = [
    'create_multi_user_engine',
    'create_single_user_engine',
    'learn_from_result',
    'process_with_user_context',
    'record_feedback_with_context',
]

语义记忆引擎 v1.0 - 兼容层
Semantic Memory Engine v1.0 - Compatibility Layer

原始模块拆分后，此文件保留所有公共符号的向后兼容导出。
新代码应直接导入拆分后的子模块:
  - semantic_types: KeywordMapping, UserSemanticProfile, SemanticContext, UserFeedback
  - multi_user_engine: MultiUserSemanticEngine
  - semantic_engine_utils: tokenize, extract_keywords, match_mappings, etc.
"""

from typing import Dict

from .semantic_types import (
    KeywordMapping,
    UserSemanticProfile,
    SemanticContext,
    UserFeedback,
)
from .multi_user_engine import MultiUserSemanticEngine

# ==================== 兼容层 ====================

class SemanticMemoryEngine(MultiUserSemanticEngine):
    """
    兼容层:保持原有API
    SemanticMemoryEngine 现在是 MultiUserSemanticEngine 的别名
    """
    pass

# ==================== Somn 集成接口 ====================

class SomnSemanticIntegration:
    """
    SomnCore 集成接口

    支持两种模式:
    1. 显式用户ID模式:在每次调用时传入 user_id
    2. 自动用户模式:需要外部提供当前用户ID(通过 session_context)
    """

    def __init__(self, engine: MultiUserSemanticEngine):
        self.engine = engine

    def process_with_user_context(self, text: str, context: Dict = None) -> SemanticContext:
        """
        根据上下文处理语义

        Args:
            text: 用户输入
            context: 上下文字典,可能包含:
                - user_id: 用户ID
                - session_context: 会话上下文
                - current_user: 当前用户

        Returns:
            语义理解结果
        """
        user_id = None

        if context:
            # 优先级:user_id > current_user
            user_id = context.get('user_id') or context.get('current_user')

        return self.engine.process_input(text, user_id=user_id)

    def learn_from_result(self, text: str, meaning: str, context: Dict = None):
        """从处理结果学习"""
        user_id = None
        if context:
            user_id = context.get('user_id') or context.get('current_user')

        self.engine.learn_from_input(text, meaning, user_id=user_id)

    def record_feedback_with_context(self,
                                      text: str,
                                      understanding: str,
                                      correction: str = "",
                                      is_correct: bool = True,
                                      context: Dict = None):
        """记录反馈"""
        user_id = None
        if context:
            user_id = context.get('user_id') or context.get('current_user')

        self.engine.record_feedback(
            user_input=text,
            system_understanding=understanding,
            user_correction=correction,
            is_correct=is_correct,
            user_id=user_id
        )

# ==================== 工厂函数 ====================

def create_multi_user_engine(base_path: str = None) -> MultiUserSemanticEngine:
    """创建多用户语义记忆引擎"""
    return MultiUserSemanticEngine(base_path=base_path)

def create_single_user_engine(base_path: str = None) -> SemanticMemoryEngine:
    """创建单用户语义记忆引擎(兼容旧代码)"""
    return SemanticMemoryEngine(base_path=base_path)

# 兼容:旧代码可能直接导入 Dict
from typing import Dict
