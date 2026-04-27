"""
__all__ = [
    'batch_encode_from_yaml',
    'discover_patterns',
    'encode_color_knowledge',
    'encode_design_rule',
    'encode_layout_knowledge',
    'encode_template_knowledge',
    'encode_typography_knowledge',
    'export_knowledge_base',
    'generate_learning_report',
    'learn_from_validation',
    'main',
    'retrieve_color_schemes',
    'retrieve_font_pairs',
    'retrieve_layout_patterns',
    'retrieve_ppt_knowledge',
]

PPT神经记忆整合 - 将PPT知识整合进神经记忆系统
"""

from src.core.paths import LEARNING_DIR
import sys
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import yaml
import json
from datetime import datetime

# 导入神经记忆系统
from src.neural_memory.memory_engine import MemoryEngine
from src.neural_memory.knowledge_engine import KnowledgeEngine
from src.neural_memory.learning_engine import LearningEngine

import logging

logger = logging.getLogger(__name__)

class PPTMemoryIntegrator:
    """PPT知识神经记忆整合器"""

    def __init__(self, memory_path: str = None):
        self.memory_engine = MemoryEngine(memory_base_path=memory_path)
        self.knowledge_engine = KnowledgeEngine(memory_base_path=memory_path)
        self.learning_engine = LearningEngine(memory_base_path=memory_path)

        # PPT知识类别
        self.ppt_categories = {
            "layout": "排版知识",
            "color": "配色知识",
            "typography": "字体知识",
            "design_rules": "设计规则",
            "templates": "模板知识",
            "visual_elements": "视觉元素"
        }

    def encode_layout_knowledge(self, layout_name: str, layout_data: Dict[str, Any],
                                confidence: float = 0.8, evidence: List[str] = None) -> str:
        """
        编码排版知识到神经记忆
        """
        memory_id = self.memory_engine.encode_memory(
            content={
                "type": "layout_pattern",
                "name": layout_name,
                "data": layout_data,
                "timestamp": datetime.now().isoformat()
            },
            memory_type="pattern",
            category="ppt_layout",
            confidence=confidence,
            evidence=evidence or [],
            tags=["ppt", "layout", layout_name]
        )

        # 同时添加到知识库
        self.knowledge_engine.add_concept(
            concept_name=f"layout_{layout_name}",
            category="layout",
            definition=layout_data.get("description", ""),
            attributes=layout_data,
            examples=[],
            confidence=confidence
        )

        logger.info(f"排版知识已编码: {layout_name} (ID: {memory_id})")
        return memory_id

    def encode_color_knowledge(self, scheme_name: str, color_data: Dict[str, Any],
                              confidence: float = 0.8, evidence: List[str] = None) -> str:
        """
        编码配色知识到神经记忆
        """
        memory_id = self.memory_engine.encode_memory(
            content={
                "type": "color_scheme",
                "name": scheme_name,
                "data": color_data,
                "timestamp": datetime.now().isoformat()
            },
            memory_type="concept",
            category="ppt_color",
            confidence=confidence,
            evidence=evidence or [],
            tags=["ppt", "color", scheme_name]
        )

        # 添加到知识库
        self.knowledge_engine.add_concept(
            concept_name=f"color_{scheme_name}",
            category="color",
            definition=f"{scheme_name}配色方案",
            attributes=color_data,
            examples=[],
            confidence=confidence
        )

        # 建立颜色关系
        if "primary" in color_data:
            self.knowledge_engine.add_relation(
                relation_type="primary_color",
                source=scheme_name,
                target=color_data["primary"],
                attributes={"role": "主色"}
            )

        if "secondary" in color_data:
            self.knowledge_engine.add_relation(
                relation_type="secondary_color",
                source=scheme_name,
                target=color_data["secondary"],
                attributes={"role": "辅助色"}
            )

        if "accent" in color_data:
            self.knowledge_engine.add_relation(
                relation_type="accent_color",
                source=scheme_name,
                target=color_data["accent"],
                attributes={"role": "强调色"}
            )

        logger.info(f"配色知识已编码: {scheme_name} (ID: {memory_id})")
        return memory_id

    def encode_typography_knowledge(self, font_name: str, font_data: Dict[str, Any],
                                    confidence: float = 0.7, evidence: List[str] = None) -> str:
        """
        编码字体知识到神经记忆
        """
        memory_id = self.memory_engine.encode_memory(
            content={
                "type": "font_pair",
                "name": font_name,
                "data": font_data,
                "timestamp": datetime.now().isoformat()
            },
            memory_type="pattern",
            category="ppt_typography",
            confidence=confidence,
            evidence=evidence or [],
            tags=["ppt", "font", font_name]
        )

        # 添加到知识库
        self.knowledge_engine.add_concept(
            concept_name=f"font_{font_name}",
            category="typography",
            definition=f"{font_name}字体搭配",
            attributes=font_data,
            examples=[],
            confidence=confidence
        )

        logger.info(f"字体知识已编码: {font_name} (ID: {memory_id})")
        return memory_id

    def encode_design_rule(self, rule_name: str, rule_data: Dict[str, Any],
                          confidence: float = 0.9, evidence: List[str] = None) -> str:
        """
        编码设计规则到神经记忆
        """
        memory_id = self.memory_engine.encode_memory(
            content={
                "type": "design_rule",
                "name": rule_name,
                "data": rule_data,
                "timestamp": datetime.now().isoformat()
            },
            memory_type="rule",
            category="ppt_design",
            confidence=confidence,
            evidence=evidence or [],
            tags=["ppt", "design", rule_name]
        )

        # 添加到规则库
        self.knowledge_engine.add_rule(
            rule_name=f"rule_{rule_name}",
            rule_type="design_principle",
            conditions=rule_data.get("conditions", []),
            consequences=rule_data.get("consequences", []),
            confidence=confidence,
            examples=rule_data.get("examples", [])
        )

        logger.info(f"设计规则已编码: {rule_name} (ID: {memory_id})")
        return memory_id

    def encode_template_knowledge(self, template_name: str, template_data: Dict[str, Any],
                                 confidence: float = 0.8, evidence: List[str] = None) -> str:
        """
        编码模板知识到神经记忆
        """
        memory_id = self.memory_engine.encode_memory(
            content={
                "type": "template",
                "name": template_name,
                "data": template_data,
                "timestamp": datetime.now().isoformat()
            },
            memory_type="concept",
            category="ppt_template",
            confidence=confidence,
            evidence=evidence or [],
            tags=["ppt", "template", template_name]
        )

        logger.info(f"模板知识已编码: {template_name} (ID: {memory_id})")
        return memory_id

    def batch_encode_from_yaml(self, yaml_path: str, knowledge_type: str) -> List[str]:
        """
        从YAML文件批量编码知识
        """
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        memory_ids = []

        if knowledge_type == "layout":
            for layout_name, layout_data in data.items():
                memory_id = self.encode_layout_knowledge(layout_name, layout_data)
                memory_ids.append(memory_id)

        elif knowledge_type == "color":
            for scheme_name, color_data in data.items():
                memory_id = self.encode_color_knowledge(scheme_name, color_data)
                memory_ids.append(memory_id)

        elif knowledge_type == "typography":
            for font_name, font_data in data.items():
                memory_id = self.encode_typography_knowledge(font_name, font_data)
                memory_ids.append(memory_id)

        elif knowledge_type == "design_rules":
            for rule_name, rule_data in data.items():
                memory_id = self.encode_design_rule(rule_name, rule_data)
                memory_ids.append(memory_id)

        logger.info(f"批量编码完成: {len(memory_ids)}条知识")
        return memory_ids

    def retrieve_ppt_knowledge(self, query: str, category: Optional[str] = None,
                               retrieval_type: str = "semantic", limit: int = 10) -> List[Dict[str, Any]]:
        """
        检索PPT知识
        """
        results = self.memory_engine.retrieve(
            query=query,
            retrieval_type=retrieval_type,
            category=category,
            limit=limit
        )

        # 过滤PPT相关记忆
        ppt_results = [
            result for result in results
            if any(tag.startswith("ppt") for tag in result.get("tags", []))
        ]

        return ppt_results

    def retrieve_layout_patterns(self, content_type: str) -> List[Dict[str, Any]]:
        """
        检索排版模式
        """
        query = f"layout pattern for {content_type}"
        return self.retrieve_ppt_knowledge(query, category="ppt_layout")

    def retrieve_color_schemes(self, theme: str = None) -> List[Dict[str, Any]]:
        """
        检索配色方案
        """
        query = f"color scheme {theme}" if theme else "color scheme"
        return self.retrieve_ppt_knowledge(query, category="ppt_color")

    def retrieve_font_pairs(self, style: str = None) -> List[Dict[str, Any]]:
        """
        检索字体搭配
        """
        query = f"font pair {style}" if style else "font pair"
        return self.retrieve_ppt_knowledge(query, category="ppt_typography")

    def learn_from_validation(self, validation_result: Dict[str, Any]):
        """
        从验证结果中学习
        """
        if validation_result.get("success"):
            # 成功的案例:强化相关知识
            related_memories = validation_result.get("related_memories", [])
            for memory_id in related_memories:
                self.learning_engine.reinforce_memory(memory_id, factor=1.1)
                logger.info(f"强化记忆: {memory_id}")
        else:
            # 失败的案例:降低置信度
            related_memories = validation_result.get("related_memories", [])
            for memory_id in related_memories:
                self.learning_engine.degrade_memory(memory_id, factor=0.9)
                logger.info(f"降低置信度: {memory_id}")

    def discover_patterns(self, threshold: int = 5) -> List[Dict[str, Any]]:
        """
        发现新模式(通过实例学习)
        """
        # get相关记忆
        memories = self.memory_engine.retrieve(
            query="ppt design",
            retrieval_type="semantic",
            limit=100
        )

        # 分析共现模式
        patterns = []
        # TODO: 实现模式发现逻辑 [延期: 需要先建立模式库]
        # 当前实现依赖于手工规则，未来可引入ML聚类或规则挖掘
        logger.info("模式发现逻辑已标记延期，等待模式库建设")

        return patterns

    def generate_learning_report(self, days: int = 7) -> Dict[str, Any]:
        """
        generate学习报告
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "period_days": days,
            "statistics": {
                "total_memories": 0,
                "by_category": {},
                "high_confidence": 0,
                "recent_additions": 0
            },
            "trends": {},
            "recommendations": []
        }

        # 统计记忆数量
        for category in self.ppt_categories.keys():
            results = self.retrieve_ppt_knowledge(f"{category}", category=f"ppt_{category}", limit=1000)
            report["statistics"]["by_category"][category] = len(results)
            report["statistics"]["total_memories"] += len(results)

            # 统计高置信度记忆
            high_conf = [r for r in results if r.get("confidence", 0) > 0.8]
            report["statistics"]["high_confidence"] += len(high_conf)

        return report

    def export_knowledge_base(self, output_path: str):
        """
        导出知识库
        """
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "categories": {}
        }

        for category, description in self.ppt_categories.items():
            results = self.retrieve_ppt_knowledge(f"{category}", category=f"ppt_{category}", limit=1000)
            export_data["categories"][category] = {
                "description": description,
                "count": len(results),
                "knowledge": results
            }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

        logger.info(f"知识库已导出: {output_path}")

def main():
    """主函数 - 示例"""
    integrator = PPTMemoryIntegrator()

    # 编码示例知识
    layout_data = {
        "description": "左右分栏布局",
        "conditions": "bullet_points >= 6",
        "optimization": "equal_width"
    }
    integrator.encode_layout_knowledge("two_column", layout_data)

    color_data = {
        "primary": "#2C3E50",
        "secondary": "#3498DB",
        "accent": "#E74C3C",
        "background": "#FFFFFF",
        "text": "#2C3E50"
    }
    integrator.encode_color_knowledge("business", color_data)

    # 检索知识
    layouts = integrator.retrieve_layout_patterns("text_heavy")
    print(f"找到 {len(layouts)} 个排版模式")

    # generate学习报告
    report = integrator.generate_learning_report()
    print(f"总记忆数: {report['statistics']['total_memories']}")

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
