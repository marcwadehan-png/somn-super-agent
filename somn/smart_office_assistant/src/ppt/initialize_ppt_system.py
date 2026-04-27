"""
__all__ = [
    'export_knowledge_base',
    'initialize_ppt_system',
]

PPT系统init脚本 - init知识库,编码知识到神经记忆
"""

import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

from ppt_memory_integration import PPTMemoryIntegrator
import yaml
import logging
from src.core.paths import LEARNING_DIR, PROJECT_ROOT

logger = logging.getLogger(__name__)

def initialize_ppt_system():
    """
    initPPT系统
    1. 加载知识库文件
    2. 编码知识到神经记忆系统
    3. 验证系统状态
    """
    logger.info("开始initPPT系统...")

    # 创建记忆整合器
    integrator = PPTMemoryIntegrator()

    # 知识库路径
    knowledge_base_path = str(LEARNING_DIR / "knowledge_base/ppt")

    # 1. 编码排版知识
    logger.info("正在编码排版知识...")
    layouts_path = f"{knowledge_base_path}/layouts.yaml"
    if os.path.exists(layouts_path):
        with open(layouts_path, 'r', encoding='utf-8') as f:
            layouts_data = yaml.safe_load(f)

        # 编码布局模式
        for layout_name, layout_patterns in layouts_data.get("layout_patterns", {}).items():
            for pattern in layout_patterns:
                integrator.encode_layout_knowledge(
                    layout_name=pattern.get("name", layout_name),
                    layout_data=pattern,
                    confidence=0.85
                )

        # 编码设计规则
        rule_categories = ["alignment_rules", "spacing_rules", "hierarchy_rules", "whitespace_rules"]
        for category in rule_categories:
            for rule in layouts_data.get(category, []):
                integrator.encode_design_rule(
                    rule_name=rule.get("rule", category),
                    rule_data=rule,
                    confidence=0.9
                )

        logger.info("排版知识编码完成")
    else:
        logger.warning(f"排版知识库文件不存在: {layouts_path}")

    # 2. 编码配色知识
    logger.info("正在编码配色知识...")
    colors_path = f"{knowledge_base_path}/color_schemes.yaml"
    if os.path.exists(colors_path):
        with open(colors_path, 'r', encoding='utf-8') as f:
            colors_data = yaml.safe_load(f)

        # 编码配色方案
        for scheme_name, scheme_data in colors_data.get("color_schemes", {}).items():
            integrator.encode_color_knowledge(
                scheme_name=scheme_name,
                color_data=scheme_data,
                confidence=0.9
            )

        logger.info("配色知识编码完成")
    else:
        logger.warning(f"配色知识库文件不存在: {colors_path}")

    # 3. 编码字体知识
    logger.info("正在编码字体知识...")
    fonts_path = f"{knowledge_base_path}/fonts.yaml"
    if os.path.exists(fonts_path):
        with open(fonts_path, 'r', encoding='utf-8') as f:
            fonts_data = yaml.safe_load(f)

        # 编码字体搭配
        for font_name, font_data in fonts_data.get("font_pairs", {}).items():
            integrator.encode_typography_knowledge(
                font_name=font_name,
                font_data=font_data,
                confidence=0.8
            )

        # 编码字体规则
        rule_categories = ["font_pairing_rules", "line_spacing_rules", "font_weight_guidelines"]
        for category in rule_categories:
            for rule in fonts_data.get(category, []):
                integrator.encode_design_rule(
                    rule_name=rule.get("rule", category),
                    rule_data=rule,
                    confidence=0.85
                )

        logger.info("字体知识编码完成")
    else:
        logger.warning(f"字体知识库文件不存在: {fonts_path}")

    # 4. 验证系统状态
    logger.info("验证系统状态...")
    report = integrator.generate_learning_report(days=0)

    logger.info(f"""
    init完成!
    ----------------------------------------
    总记忆数: {report['statistics']['total_memories']}
    排版知识: {report['statistics']['by_category'].get('layout', 0)}
    配色知识: {report['statistics']['by_category'].get('color', 0)}
    字体知识: {report['statistics']['by_category'].get('typography', 0)}
    设计规则: {report['statistics']['by_category'].get('design', 0)}
    高置信度: {report['statistics']['high_confidence']}
    ----------------------------------------
    """)

    return report

def export_knowledge_base(output_path: str = None):
    """
    导出知识库
    """
    if output_path is None:
        output_path = str(PROJECT_ROOT / "outputs/ppt_knowledge_base.json")

    integrator = PPTMemoryIntegrator()
    integrator.export_knowledge_base(output_path)

    logger.info(f"知识库已导出到: {output_path}")

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")

    # 导出知识库
    export_knowledge_base()
