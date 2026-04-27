#!/usr/bin/env python3
"""
PPT每日学习任务脚本
- 搜索最新设计趋势
- 提取知识并结构化
- 验证并编码到神经记忆
- 生成学习报告
"""

import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

KNOWLEDGE_BASE_PATH = PROJECT_ROOT / "data" / "learning" / "knowledge_base" / "ppt"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

from ppt.ppt_learning import PPTLearningEngine
from ppt.ppt_memory_integration import PPTMemoryIntegrator
import yaml
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def daily_ppt_learning():
    """执行每日PPT学习任务"""
    logger.info("=" * 60)
    logger.info("开始每日PPT设计趋势学习")
    logger.info("=" * 60)

    # 初始化引擎
    learning_engine = PPTLearningEngine(
        knowledge_base_path=str(KNOWLEDGE_BASE_PATH)
    )


    memory_integrator = PPTMemoryIntegrator()

    # 执行学习
    try:
        # 搜索并提取知识
        learning_results = learning_engine.comprehensive_learning()

        # 编码新知识到神经记忆
        new_knowledge_count = 0
        for category, details in learning_results['categories'].items():
            for knowledge in details['knowledge']:
                if knowledge.confidence > 0.7:  # 只编码高置信度知识
                    if knowledge.category == 'layout':
                        memory_integrator.encode_layout_knowledge(
                            layout_name=knowledge.content.get('name', 'unknown'),
                            layout_data=knowledge.content,
                            confidence=knowledge.confidence,
                            evidence=knowledge.evidence
                        )
                    elif knowledge.category == 'color':
                        memory_integrator.encode_color_knowledge(
                            scheme_name=knowledge.content.get('name', 'unknown'),
                            color_data=knowledge.content,
                            confidence=knowledge.confidence,
                            evidence=knowledge.evidence
                        )
                    elif knowledge.category == 'typography':
                        memory_integrator.encode_typography_knowledge(
                            font_name=knowledge.content.get('name', 'unknown'),
                            font_data=knowledge.content,
                            confidence=knowledge.confidence,
                            evidence=knowledge.evidence
                        )
                    new_knowledge_count += 1

        # 生成报告
        report = {
            "timestamp": datetime.now().isoformat(),
            "learning_results": learning_results,
            "new_knowledge_encoded": new_knowledge_count,
            "memory_statistics": memory_integrator.generate_learning_report(days=1)
        }

        # 保存报告
        outputs_dir = OUTPUTS_DIR
        outputs_dir.mkdir(exist_ok=True)


        # YAML报告
        yaml_report_path = outputs_dir / f"ppt_daily_learning_{datetime.now().strftime('%Y%m%d')}.yaml"
        with open(yaml_report_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(report, f, allow_unicode=True, default_flow_style=False)

        # Markdown报告
        markdown_report = generate_markdown_report(report)
        md_report_path = outputs_dir / f"ppt_daily_learning_{datetime.now().strftime('%Y%m%d')}.md"
        with open(md_report_path, 'w', encoding='utf-8') as f:
            f.write(markdown_report)

        logger.info(f"学习报告已保存:")
        logger.info(f"  - YAML: {yaml_report_path}")
        logger.info(f"  - Markdown: {md_report_path}")

        logger.info("=" * 60)
        logger.info("每日学习完成！")
        logger.info("=" * 60)

        return report

    except Exception as e:
        logger.error(f"学习过程中发生错误: {e}", exc_info=True)
        raise


def generate_markdown_report(report: dict) -> str:
    """生成Markdown格式的学习报告"""
    lines = [
        "# PPT设计趋势学习报告",
        f"",
        f"**生成时间**: {report['timestamp']}",
        f"",
        f"## 学习概览",
        f"",
        f"- **搜索类别数**: {len(report['learning_results']['categories'])}",
        f"- **总搜索次数**: {report['learning_results']['total_searches']}",
        f"- **提取知识数**: {report['learning_results']['total_knowledge']}",
        f"- **编码知识数**: {report['new_knowledge_encoded']}",
        f"",
        f"## 分类详情",
        f""
    ]

    for category, details in report['learning_results']['categories'].items():
        lines.extend([
            f"### {category.upper()}",
            f"",
            f"- 搜索次数: {details['searches']}",
            f"- 知识数量: {details['knowledge_count']}",
            f""
        ])

        if details['knowledge']:
            lines.append("**知识示例**:")
            lines.append("")
            for i, knowledge in enumerate(details['knowledge'][:5], 1):  # 最多显示5个
                lines.append(f"{i}. **{knowledge.type}**: {knowledge.content.get('name', 'N/A')}")
                lines.append(f"   - 置信度: {knowledge.confidence:.2f}")
                lines.append(f"   - 标签: {', '.join(knowledge.tags[:3])}")
            lines.append("")

    # 添加记忆统计
    if 'memory_statistics' in report:
        stats = report['memory_statistics']['statistics']
        lines.extend([
            f"## 记忆统计",
            f"",
            f"- **总记忆数**: {stats['total_memories']}",
            f"- **高置信度**: {stats['high_confidence']}",
            f"",
            f"### 分类统计",
            f""
        ])

        for category, count in stats['by_category'].items():
            lines.append(f"- **{category}**: {count}")
        lines.append("")

    lines.extend([
        f"## 建议",
        f"",
        f"1. 持续监控设计趋势，定期更新知识库",
        f"2. 重点关注高置信度的排版和配色方案",
        f"3. 收集用户反馈，验证知识有效性",
        f"4. 定期检查知识库的一致性和完整性",
        f"",
        f"---",
        f"",
        f"*由Somn PPT学习引擎自动生成*"
    ])

    return "\n".join(lines)


if __name__ == "__main__":
    try:
        report = daily_ppt_learning()
        print("\n✓ 每日学习任务执行成功！")
    except Exception as e:
        print(f"\n✗ 学习任务执行失败: {e}")
        sys.exit(1)
