#!/usr/bin/env python3
"""
PPT系统演示脚本
展示PPT智能生成与美化系统的核心功能
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths

PROJECT_ROOT = bootstrap_project_paths(__file__, change_cwd=True)
OUTPUT_DIR = PROJECT_ROOT / "outputs"

from src.ppt import PPTService, ContentFormat, ColorScheme, quick_generate

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def demo_basic_generation():
    """演示：基础PPT生成"""
    print("\n" + "="*60)
    print("演示1：基础PPT生成")
    print("="*60 + "\n")

    # 创建服务
    service = PPTService(theme="business", enable_learning=True)

    # 准备内容
    content = """
# Somn PPT智能生成系统

## 系统概述
- 全自动内容转PPT
- 智能美化引擎
- 全网自主学习
- 神经记忆整合

## 核心功能
- 内容生成
- 智能美化
- 知识学习
- 持续进化

## 技术架构
- 五层架构设计
- 神经记忆系统
- 智能学习引擎
- 自动化任务

## 总结
- 高效自动化
- 智能化决策
- 持续进化能力
"""

    # 生成PPT
    output_dir = OUTPUT_DIR
    output_dir.mkdir(exist_ok=True)


    ppt_path = output_dir / "demo_basic.pptx"
    result_path = service.generate_ppt(
        content=content,
        format=ContentFormat.MARKDOWN,
        output_path=str(ppt_path),
        beautify=True
    )

    print(f"✓ PPT生成成功: {result_path}")


def demo_theme_variations():
    """演示：不同主题风格"""
    print("\n" + "="*60)
    print("演示2：不同主题风格")
    print("="*60 + "\n")

    content = """
# 科技创新

## 发展趋势
- 人工智能
- 大数据
- 云计算

## 应用场景
- 智能家居
- 自动驾驶
- 医疗健康

## 未来展望
- 技术突破
- 产业融合
- 生态建设
"""

    themes = ["business", "tech", "education", "creative", "minimal"]
    output_dir = OUTPUT_DIR
    output_dir.mkdir(exist_ok=True)

    for theme in themes:

        service = PPTService(theme=theme, enable_learning=False)
        ppt_path = output_dir / f"demo_theme_{theme}.pptx"

        result_path = service.generate_ppt(
            content=content,
            format=ContentFormat.MARKDOWN,
            output_path=str(ppt_path),
            beautify=True
        )

        print(f"✓ {theme} 主题PPT: {result_path}")


def demo_content_formats():
    """演示：不同内容格式"""
    print("\n" + "="*60)
    print("演示3：不同内容格式")
    print("="*60 + "\n")

    # Markdown格式
    markdown_content = """
# 产品发布会

## 产品特性
- 功能强大
- 性能卓越
- 体验优秀

## 市场定位
- 高端市场
- 企业客户
- 行业领先

## 销售策略
- 渠道拓展
- 品牌推广
- 客户服务
"""

    # YAML格式
    yaml_content = """
title: "产品发布会"
sections:
  - title: "产品特性"
    content: "核心卖点"
    items:
      - title: "功能"
        content: "功能强大"
      - title: "性能"
        content: "性能卓越"
      - title: "体验"
        content: "体验优秀"
  - title: "市场定位"
    content: "目标市场"
    items:
      - title: "市场"
        content: "高端市场"
      - title: "客户"
        content: "企业客户"
  - title: "销售策略"
    content: "营销计划"
    items:
      - title: "渠道"
        content: "渠道拓展"
      - title: "品牌"
        content: "品牌推广"
"""

    # JSON格式
    json_content = """{
  "title": "产品发布会",
  "sections": [
    {
      "title": "产品特性",
      "content": "核心卖点",
      "items": [
        {"title": "功能", "content": "功能强大"},
        {"title": "性能", "content": "性能卓越"}
      ]
    },
    {
      "title": "市场定位",
      "content": "目标市场",
      "items": [
        {"title": "市场", "content": "高端市场"}
      ]
    }
  ]
}"""

    service = PPTService(theme="business", enable_learning=False)
    output_dir = OUTPUT_DIR
    output_dir.mkdir(exist_ok=True)


    # 生成不同格式的PPT
    formats = [
        ("markdown", ContentFormat.MARKDOWN, markdown_content),
        ("yaml", ContentFormat.YAML, yaml_content),
        ("json", ContentFormat.JSON, json_content)
    ]

    for name, format_type, content in formats:
        ppt_path = output_dir / f"demo_format_{name}.pptx"
        result_path = service.generate_ppt(
            content=content,
            format=format_type,
            output_path=str(ppt_path),
            beautify=True
        )
        print(f"✓ {name} 格式PPT: {result_path}")


def demo_knowledge_retrieval():
    """演示：知识检索"""
    print("\n" + "="*60)
    print("演示4：知识检索")
    print("="*60 + "\n")

    service = PPTService(theme="business", enable_learning=True)

    # 检索排版建议
    print("1. 检索排版建议（文本密集型）：")
    layout_suggestions = service.get_layout_suggestions("text_heavy")
    print(f"   找到 {len(layout_suggestions)} 个排版建议")
    for suggestion in layout_suggestions[:3]:
        print(f"   - {suggestion.get('name', 'N/A')}: {suggestion.get('description', 'N/A')}")

    # 检索配色方案
    print("\n2. 检索配色方案：")
    color_schemes = service.get_color_schemes()
    print(f"   找到 {len(color_schemes)} 个配色方案")
    for scheme in color_schemes[:3]:
        print(f"   - {scheme.get('name', 'N/A')}: 主色={scheme.get('primary', 'N/A')}")

    # 检索字体搭配
    print("\n3. 检索字体搭配：")
    font_pairs = service.get_font_pairs()
    print(f"   找到 {len(font_pairs)} 个字体搭配")
    for font in font_pairs[:3]:
        print(f"   - {font.get('name', 'N/A')}: {font.get('title_font', 'N/A')} + {font.get('body_font', 'N/A')}")


def demo_quick_functions():
    """演示：快捷函数"""
    print("\n" + "="*60)
    print("演示5：快捷函数")
    print("="*60 + "\n")

    content = """
# 快速生成示例

## 要点
- 快速上手
- 简单易用
- 高效便捷

## 优势
- 一行代码
- 自动美化
- 专业输出
"""

    # 使用快捷函数生成
    ppt_path = quick_generate(content, theme="business")
    print(f"✓ 快速生成PPT: {ppt_path}")


def demo_learning_report():
    """演示：学习报告"""
    print("\n" + "="*60)
    print("演示6：学习报告")
    print("="*60 + "\n")

    service = PPTService(theme="business", enable_learning=True)

    # 获取学习报告
    report = service.get_learning_report(days=7)

    print(f"总记忆数: {report['statistics']['total_memories']}")
    print(f"高置信度: {report['statistics']['high_confidence']}")

    print("\n分类统计:")
    for category, count in report['statistics']['by_category'].items():
        print(f"  - {category}: {count}")


def main():
    """运行所有演示"""
    print("\n" + "="*60)
    print("PPT智能生成与美化系统 - 功能演示")
    print("="*60)

    try:
        # 演示1：基础生成
        demo_basic_generation()

        # 演示2：主题变化
        demo_theme_variations()

        # 演示3：不同格式
        demo_content_formats()

        # 演示4：知识检索
        demo_knowledge_retrieval()

        # 演示5：快捷函数
        demo_quick_functions()

        # 演示6：学习报告
        demo_learning_report()

        print("\n" + "="*60)
        print("所有演示完成！")
        print("="*60)
        print(f"\n生成的PPT文件位于: {OUTPUT_DIR}")

        print("请打开PowerPoint查看生成的PPT文件。\n")

    except Exception as e:
        logger.error(f"演示过程中发生错误: {e}", exc_info=True)
        print(f"\n✗ 演示失败: {e}")


if __name__ == "__main__":
    main()
