"""
__all__ = [
    'build_local_fallback_context',
    'extract_similarity_terms',
    'query_memory_context',
]

记忆检索器 - 提供记忆上下文检索能力
"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class MemoryRetriever:
    """记忆检索器封装类"""

    def __init__(self, somn_core=None):
        """
        Args:
            somn_core: SomnCore实例引用
        """
        self._core = somn_core

    def query_memory_context(self, description: str) -> List[Dict[str, Any]]:
        """
        从神经记忆系统提取相关上下文

        Args:
            description: 任务描述

        Returns:
            记忆上下文列表
        """
        if not self._core or not hasattr(self._core, 'neural_system'):
            return []

        try:
            results = self._core.neural_system.retrieve(
                query=description,
                top_k=5
            )
            return results if results else []
        except Exception as e:
            logger.warning(f"记忆上下文查询失败: {e}")
            return []

    def build_local_fallback_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        构建本地上下文兜底条目

        当网络搜索熔断/超时/异常时使用

        Args:
            context: 原始上下文

        Returns:
            兜底上下文
        """
        fallback = {
            "source": "local_fallback",
            "search_results": [],
            "knowledge_context": [],
            "timestamp": self._get_timestamp(),
        }

        # 从已有上下文提取有用信息
        if context:
            if "matched_industries" in context:
                fallback["industries"] = context["matched_industries"]
            if "industry" in context:
                fallback["current_industry"] = context["industry"]

        return fallback

    def extract_similarity_terms(self, text: str) -> List[str]:
        """
        提取用于经验召回的关键词

        Args:
            text: 输入文本

        Returns:
            关键词列表
        """
        import re

        # 提取中英文词组
        terms = re.findall(r'[\u4e00-\u9fa5]{2,}', text)
        terms += re.findall(r'[a-zA-Z]{3,}', text)

        # 过滤停用词
        stopwords = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '那', 'the', 'and', 'for', 'are', 'with', 'this', 'that', 'from'}
        terms = [t for t in terms if t not in stopwords and len(t) >= 2]

        return list(set(terms))[:20]

    @staticmethod
    def _get_timestamp() -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
