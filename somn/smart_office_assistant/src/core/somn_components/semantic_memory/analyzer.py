"""
__all__ = [
    'analyze',
    'extract_keywords',
    'get_report',
    'get_stats',
    'record_feedback',
    'summarize_understanding',
]

语义记忆分析器 - 提供语义分析和理解能力

从 SomnCore._run_semantic_analysis 提取
"""

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class SemanticAnalyzer:
    """语义分析器，负责理解用户输入的真实意图"""

    def __init__(self, semantic_memory=None):
        """
        Args:
            semantic_memory: 语义记忆引擎实例
        """
        self.semantic_memory = semantic_memory

    def analyze(self, description: str, context: Dict = None) -> Dict[str, Any]:
        """
        运行语义分析

        多用户支持:
        - 从 context 中获取 user_id 进行用户隔离
        - 每个用户有独立的语义记忆空间
        - 支持千人千面的个性化理解

        Args:
            description: 用户描述
            context: 上下文信息

        Returns:
            语义分析结果字典
        """
        if not self.semantic_memory:
            return {"enabled": False}

        try:
            # 1. 确定用户ID(多用户支持)
            user_id = None
            session_ctx = ""
            if context:
                user_id = context.get("user_id") or context.get("current_user")
                session_ctx = context.get("session_context", "") or ""

            # 2. 语义理解(传入用户ID)
            semantic_context = self.semantic_memory.process_input(
                description,
                user_id=user_id,
                session_context=session_ctx
            )

            # 3. 如需澄清,返回澄清信息(但不阻塞主链)
            clarification_needed = semantic_context.needs_clarification
            clarification_question = ""
            if clarification_needed and semantic_context.clarification_question:
                clarification_question = semantic_context.clarification_question

            # 4. 学习高频词mapping(多用户隔离)
            inferred = semantic_context.inferred_intent
            if inferred and inferred != 'unknown':
                self.semantic_memory.learn_from_input(
                    description,
                    inferred,
                    user_id=user_id
                )

            # 5. 构建结果(包含用户信息)
            result = {
                "enabled": True,
                "user_id": semantic_context.user_id,
                "raw_input": semantic_context.raw_input,
                "keywords": semantic_context.keywords_extracted or [],
                "inferred_intent": inferred or "unknown",
                "intent_confidence": semantic_context.intent_confidence or 0.0,
                "reasoning_chain": semantic_context.reasoning_chain or [],
                "clarification_needed": clarification_needed,
                "clarification_question": clarification_question,
                "matched_mappings": semantic_context.matched_mappings or [],
                "personalization_applied": semantic_context.personalization_applied,
                "understanding_summary": self._summarize_understanding(semantic_context)
            }

            logger.info(f"[语义分析] 用户:{semantic_context.user_id} | 意图:{inferred} | "
                       f"置信度:{semantic_context.intent_confidence:.2f} | "
                       f"个性化:{semantic_context.personalization_applied}")

            return result

        except Exception as e:
            logger.warning(f"语义分析执行失败: {e}")
            return {"enabled": False, "error": "语义分析执行失败"}

    def summarize_understanding(self, semantic_context) -> str:
        """
        生成语义理解摘要

        Args:
            semantic_context: 语义上下文对象

        Returns:
            摘要字符串
        """
        parts = []

        if semantic_context.inferred_intent != 'unknown':
            parts.append(f"用户想[{semantic_context.inferred_intent}]")

        if semantic_context.keywords_extracted:
            parts.append(f"关键词:{','.join(semantic_context.keywords_extracted[:5])}")

        if semantic_context.matched_mappings:
            parts.append(f"已匹配语义mapping:{len(semantic_context.matched_mappings)} 条")

        return ";".join(parts) if parts else "未recognize到明确意图"

    @staticmethod
    def extract_keywords(text: str) -> List[str]:
        """
        提取关键词

        Args:
            text: 输入文本

        Returns:
            关键词列表
        """
        growth_keywords = [
            "增长", "获客", "留存", "转化", "变现", "推荐",
            "用户", "流量", "渠道", "营销", "运营",
            "strategy", "方案", "优化", "提升", "降低",
            "DAU", "MAU", "GMV", "ROI", "LTV", "CAC",
            "电商", "SaaS", "内容", "社交", "金融", "智能体"
        ]
        return [kw for kw in growth_keywords if kw in text]

    def record_feedback(self,
                        user_input: str,
                        system_understanding: str,
                        user_correction: str = "",
                        is_correct: bool = True,
                        user_id: str = None):
        """
        记录语义理解反馈

        Args:
            user_input: 用户原始输入
            system_understanding: 系统理解的意思
            user_correction: 用户corrective(如有)
            is_correct: 系统理解是否正确
            user_id: 用户ID(多用户支持)
        """
        if not self.semantic_memory:
            return

        try:
            self.semantic_memory.record_feedback(
                user_input=user_input,
                system_understanding=system_understanding,
                user_correction=user_correction,
                is_correct=is_correct,
                user_id=user_id
            )

            if not is_correct and user_correction:
                logger.info(f"[语义反馈] 用户 {user_id or 'default'} corrective: '{user_input}' -> {user_correction}")

        except Exception as e:
            logger.warning(f"记录语义反馈失败: {e}")

    def get_stats(self, user_id: str = None) -> Dict[str, Any]:
        """获取语义记忆统计"""
        if not self.semantic_memory:
            return {"enabled": False}
        return self.semantic_memory.get_stats(user_id=user_id)

    def get_report(self, user_id: str = None) -> str:
        """获取语义记忆报告"""
        if not self.semantic_memory:
            return "语义记忆引擎未启用"
        return self.semantic_memory.generate_memory_report(user_id=user_id)
