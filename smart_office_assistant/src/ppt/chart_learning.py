"""
__all__ = [
    'export_knowledge',
    'extract_knowledge_from_examples',
    'get_anti_patterns',
    'get_best_practices',
    'get_chart_recommendation',
    'learn_from_feedback',
    'search_knowledge',
]

图表学习引擎 - 持续学习图表最佳实践
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import yaml
import json
import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

class LearningCategory(Enum):
    """学习类别"""
    CHART_PATTERNS = "chart_patterns"
    BEST_PRACTICES = "best_practices"
    ANTI_PATTERNS = "anti_patterns"
    INDUSTRY_TRENDS = "industry_trends"
    USER_PREFERENCES = "user_preferences"

@dataclass
class ChartKnowledge:
    """图表知识"""
    category: LearningCategory
    title: str
    content: str
    source: str
    confidence: float
    tags: List[str]
    metadata: Dict[str, Any]

@dataclass
class SearchResult:
    """搜索结果"""
    knowledge: ChartKnowledge
    relevance_score: float
    matched_fields: List[str]

class ChartLearningEngine:
    """图表学习引擎"""

    def __init__(self, knowledge_base_path: str = None):
        """
        init学习引擎

        Args:
            knowledge_base_path: 知识库路径
        """
        self.knowledge_base_path = knowledge_base_path or \
            "data/learning/knowledge_base/ppt/chart_examples.yaml"
        self.knowledge_base = self._load_knowledge_base()
        self.learned_patterns = []

    def _load_knowledge_base(self) -> Dict:
        """加载知识库"""
        try:
            with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.warning(f"加载知识库失败: {e}")
            return {"chart_categories": {}}

    def extract_knowledge_from_examples(self) -> List[ChartKnowledge]:
        """
        从示例中提取知识

        Returns:
            图表知识列表
        """
        knowledge_list = []

        categories = self.knowledge_base.get("chart_categories", {})

        for category_name, examples in categories.items():
            for example in examples:
                # 提取最佳实践
                best_practices = example.get("best_practices", [])
                for practice in best_practices:
                    knowledge = ChartKnowledge(
                        category=LearningCategory.BEST_PRACTICES,
                        title=f"{example['name']} - 最佳实践",
                        content=practice,
                        source=self.knowledge_base_path,
                        confidence=0.9,
                        tags=[category_name, example['name'], "best_practice"],
                        metadata={
                            "chart_type": example.get("chart_type"),
                            "use_case": example.get("use_case")
                        }
                    )
                    knowledge_list.append(knowledge)

                # 提取反模式
                anti_patterns = example.get("anti_patterns", [])
                for pattern in anti_patterns:
                    knowledge = ChartKnowledge(
                        category=LearningCategory.ANTI_PATTERNS,
                        title=f"{example['name']} - 反模式",
                        content=pattern,
                        source=self.knowledge_base_path,
                        confidence=0.9,
                        tags=[category_name, example['name'], "anti_pattern"],
                        metadata={
                            "chart_type": example.get("chart_type"),
                            "use_case": example.get("use_case")
                        }
                    )
                    knowledge_list.append(knowledge)

        return knowledge_list

    def search_knowledge(
        self,
        query: str,
        category: Optional[LearningCategory] = None,
        limit: int = 10
    ) -> List[SearchResult]:
        """
        搜索知识

        Args:
            query: 查询字符串
            category: 学习类别(可选)
            limit: 返回结果限制

        Returns:
            搜索结果列表
        """
        knowledge_list = self.extract_knowledge_from_examples()

        # 简单的关键词匹配
        results = []
        query_lower = query.lower()

        for knowledge in knowledge_list:
            # 类别过滤
            if category and knowledge.category != category:
                continue

            # 计算相关性
            relevance_score = 0.0
            matched_fields = []

            # 标题匹配
            if query_lower in knowledge.title.lower():
                relevance_score += 0.5
                matched_fields.append("title")

            # 内容匹配
            if query_lower in knowledge.content.lower():
                relevance_score += 0.4
                matched_fields.append("content")

            # 标签匹配
            for tag in knowledge.tags:
                if query_lower in tag.lower():
                    relevance_score += 0.1
                    matched_fields.append("tag")

            # 置信度加权
            relevance_score *= knowledge.confidence

            if relevance_score > 0:
                results.append(SearchResult(
                    knowledge=knowledge,
                    relevance_score=relevance_score,
                    matched_fields=matched_fields
                ))

        # 按相关性排序
        results.sort(key=lambda x: x.relevance_score, reverse=True)

        return results[:limit]

    def get_best_practices(self, chart_type: str) -> List[str]:
        """
        get特定图表类型的最佳实践

        Args:
            chart_type: 图表类型

        Returns:
            最佳实践列表
        """
        categories = self.knowledge_base.get("chart_categories", {})

        for category_examples in categories.values():
            for example in category_examples:
                if example.get("chart_type") == chart_type:
                    return example.get("best_practices", [])

        return []

    def get_anti_patterns(self, chart_type: str) -> List[str]:
        """
        get特定图表类型的反模式

        Args:
            chart_type: 图表类型

        Returns:
            反模式列表
        """
        categories = self.knowledge_base.get("chart_categories", {})

        for category_examples in categories.values():
            for example in category_examples:
                if example.get("chart_type") == chart_type:
                    return example.get("anti_patterns", [])

        return []

    def get_chart_recommendation(
        self,
        data_structure: str,
        use_case: str
    ) -> Optional[Dict]:
        """
        根据数据结构和用途推荐图表

        Args:
            data_structure: 数据结构
            use_case: 使用场景

        Returns:
            图表推荐字典
        """
        categories = self.knowledge_base.get("chart_categories", {})

        for category_examples in categories.values():
            for example in category_examples:
                if (example.get("data_structure") == data_structure and
                    use_case in example.get("use_case", "")):
                    return example

        return None

    def learn_from_feedback(
        self,
        chart_type: str,
        feedback: str,
        positive: bool
    ):
        """
        从用户反馈中学习

        Args:
            chart_type: 图表类型
            feedback: 反馈内容
            positive: 是否正面反馈
        """
        # 这里可以实现更复杂的学习逻辑
        # 目前简单记录反馈
        logger.info(f"收到{'正面' if positive else '负面'}反馈: {chart_type} - {feedback}")

        # 可以将反馈编码到神经记忆系统
        # ...

    def export_knowledge(
        self,
        format: str = "yaml",
        output_path: Optional[str] = None
    ) -> str:
        """
        导出知识

        Args:
            format: 导出格式(yaml/json/markdown)
            output_path: 输出路径

        Returns:
            输出文件路径
        """
        knowledge_list = self.extract_knowledge_from_examples()

        if not output_path:
            output_path = f"outputs/chart_knowledge.{format}"

        # 确保目录存在
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        if format == "yaml":
            self._export_yaml(knowledge_list, output_path)
        elif format == "json":
            self._export_json(knowledge_list, output_path)
        elif format == "markdown":
            self._export_markdown(knowledge_list, output_path)
        else:
            raise ValueError(f"不支持的格式: {format}")

        logger.info(f"知识已导出到: {output_path}")
        return output_path

    def _export_yaml(self, knowledge_list: List[ChartKnowledge], output_path: str):
        """导出为YAML格式"""
        output_data = []
        for knowledge in knowledge_list:
            output_data.append({
                "category": knowledge.category.value,
                "title": knowledge.title,
                "content": knowledge.content,
                "source": knowledge.source,
                "confidence": knowledge.confidence,
                "tags": knowledge.tags,
                "metadata": knowledge.metadata
            })

        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(output_data, f, allow_unicode=True)

    def _export_json(self, knowledge_list: List[ChartKnowledge], output_path: str):
        """导出为JSON格式"""
        output_data = []
        for knowledge in knowledge_list:
            output_data.append({
                "category": knowledge.category.value,
                "title": knowledge.title,
                "content": knowledge.content,
                "source": knowledge.source,
                "confidence": knowledge.confidence,
                "tags": knowledge.tags,
                "metadata": knowledge.metadata
            })

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

    def _export_markdown(self, knowledge_list: List[ChartKnowledge], output_path: str):
        """导出为Markdown格式"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# 图表知识库\n\n")

            # 按类别分组
            by_category = {}
            for knowledge in knowledge_list:
                if knowledge.category not in by_category:
                    by_category[knowledge.category] = []
                by_category[knowledge.category].append(knowledge)

            # 输出每个类别
            for category, knowledge_items in by_category.items():
                f.write(f"## {category.value}\n\n")

                for knowledge in knowledge_items:
                    f.write(f"### {knowledge.title}\n\n")
                    f.write(f"{knowledge.content}\n\n")
                    f.write(f"**置信度**: {knowledge.confidence}\n\n")
                    f.write(f"**标签**: {', '.join(knowledge.tags)}\n\n")
                    f.write("---\n\n")
