"""
图表自动生成系统演示脚本
展示智能图表推荐、自动生成、学习等功能
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

from ppt.chart_generator import ChartGenerator, ChartType, ChartLibrary, ChartConfig
from ppt.chart_learning import ChartLearningEngine

import json
import pandas as pd


def demo_chart_recommendation():
    """演示图表智能推荐"""
    print("\n" + "="*60)
    print("1. 图表智能推荐演示")
    print("="*60)

    # 创建图表生成器
    generator = ChartGenerator()

    # 示例数据1：时间序列
    time_series_data = {
        "月份": ["1月", "2月", "3月", "4月", "5月", "6月"],
        "销售额": [100, 120, 150, 180, 200, 220]
    }

    print("\n数据1：时间序列数据")
    print(f"数据：{time_series_data}")
    print("\n推荐图表类型：")

    recommendations = generator.get_recommendations(time_series_data)
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec.chart_type.value} - 置信度: {rec.confidence:.2f}")
        print(f"     原因: {rec.reason}")
        print(f"     推荐库: {rec.library.value}")

    # 示例数据2：比较数据
    comparison_data = {
        "产品": ["A", "B", "C", "D", "E"],
        "销量": [500, 300, 450, 200, 400]
    }

    print("\n数据2：比较数据")
    print(f"数据：{comparison_data}")
    print("\n推荐图表类型：")

    recommendations = generator.get_recommendations(comparison_data)
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec.chart_type.value} - 置信度: {rec.confidence:.2f}")
        print(f"     原因: {rec.reason}")

    # 示例数据3：分布数据
    distribution_data = {
        "年龄段": ["18-25", "26-35", "36-45", "46-55", "55+"],
        "人数": [120, 200, 150, 80, 50]
    }

    print("\n数据3：分布数据")
    print(f"数据：{distribution_data}")
    print("\n推荐图表类型：")

    recommendations = generator.get_recommendations(distribution_data)
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec.chart_type.value} - 置信度: {rec.confidence:.2f}")
        print(f"     原因: {rec.reason}")


def demo_chart_generation():
    """演示图表生成"""
    print("\n" + "="*60)
    print("2. 图表自动生成演示")
    print("="*60)

    # 创建图表生成器
    generator = ChartGenerator()

    # 生成时间序列折线图
    time_series_data = {
        "月份": ["1月", "2月", "3月", "4月", "5月", "6月"],
        "销售额": [100, 120, 150, 180, 200, 220]
    }

    print("\n生成时间序列折线图...")
    try:
        filepath, recommendation = generator.generate_chart(
            data=time_series_data,
            title="2024年上半年销售趋势"
        )
        print(f"✓ 图表已生成: {filepath}")
        print(f"  推荐类型: {recommendation.chart_type.value}")
        print(f"  推荐原因: {recommendation.reason}")
    except ImportError as e:
        print(f"✗ 生成失败: {e}")
        print("  提示：需要安装Plotly: pip install plotly kaleido")

    # 生成比较柱状图
    comparison_data = {
        "产品": ["产品A", "产品B", "产品C", "产品D", "产品E"],
        "销量": [500, 300, 450, 200, 400]
    }

    print("\n生成比较柱状图...")
    try:
        filepath, recommendation = generator.generate_chart(
            data=comparison_data,
            chart_type=ChartType.BAR,
            title="产品销量对比"
        )
        print(f"✓ 图表已生成: {filepath}")
    except ImportError as e:
        print(f"✗ 生成失败: {e}")

    # 生成饼图
    pie_data = {
        "类别": ["A", "B", "C", "D"],
        "数值": [30, 25, 20, 25]
    }

    print("\n生成饼图...")
    try:
        filepath, recommendation = generator.generate_chart(
            data=pie_data,
            chart_type=ChartType.PIE,
            title="占比分析"
        )
        print(f"✓ 图表已生成: {filepath}")
    except ImportError as e:
        print(f"✗ 生成失败: {e}")


def demo_chart_learning():
    """演示图表学习功能"""
    print("\n" + "="*60)
    print("3. 图表学习引擎演示")
    print("="*60)

    # 创建学习引擎
    learning_engine = ChartLearningEngine()

    # 搜索知识
    print("\n搜索'折线图'最佳实践...")
    results = learning_engine.search_knowledge("折线图", limit=5)

    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.knowledge.title}")
        print(f"   类别: {result.knowledge.category.value}")
        print(f"   内容: {result.knowledge.content}")
        print(f"   置信度: {result.knowledge.confidence:.2f}")
        print(f"   相关性: {result.relevance_score:.2f}")
        print(f"   匹配字段: {', '.join(result.matched_fields)}")

    # 获取特定图表类型的最佳实践
    print("\n\n获取'line'图表的最佳实践...")
    best_practices = learning_engine.get_best_practices("line")
    for i, practice in enumerate(best_practices, 1):
        print(f"{i}. {practice}")

    # 获取特定图表类型的反模式
    print("\n获取'line'图表的反模式...")
    anti_patterns = learning_engine.get_anti_patterns("line")
    for i, pattern in enumerate(anti_patterns, 1):
        print(f"{i}. {pattern}")

    # 导出知识
    print("\n\n导出知识库...")
    try:
        yaml_path = learning_engine.export_knowledge(format="yaml")
        print(f"✓ YAML格式已导出: {yaml_path}")

        json_path = learning_engine.export_knowledge(format="json")
        print(f"✓ JSON格式已导出: {json_path}")

        md_path = learning_engine.export_knowledge(format="markdown")
        print(f"✓ Markdown格式已导出: {md_path}")
    except Exception as e:
        print(f"✗ 导出失败: {e}")


def demo_advanced_features():
    """演示高级功能"""
    print("\n" + "="*60)
    print("4. 高级功能演示")
    print("="*60)

    # 多系列数据
    print("\n多系列时间序列数据推荐...")
    multi_series_data = {
        "月份": ["1月", "2月", "3月", "4月", "5月", "6月"],
        "产品A": [100, 120, 150, 180, 200, 220],
        "产品B": [80, 90, 110, 130, 150, 170],
        "产品C": [60, 70, 85, 100, 120, 140]
    }

    generator = ChartGenerator()
    recommendations = generator.get_recommendations(multi_series_data)

    print(f"\n数据：{list(multi_series_data.keys())}")
    print("\n推荐图表类型：")
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"  {i}. {rec.chart_type.value} - 置信度: {rec.confidence:.2f}")
        print(f"     原因: {rec.reason}")

    # 用户偏好指定图表类型
    print("\n\n用户偏好指定图表类型...")
    print("用户指定：使用柱状图展示")

    recommendations = generator.get_recommendations(
        multi_series_data,
        user_preference=ChartType.BAR
    )

    print("\n推荐结果（考虑用户偏好）：")
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"  {i}. {rec.chart_type.value} - 置信度: {rec.confidence:.2f}")
        print(f"     原因: {rec.reason}")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("PPT图表自动生成系统 - 完整演示")
    print("="*60)

    try:
        # 演示图表智能推荐
        demo_chart_recommendation()

        # 演示图表生成
        demo_chart_generation()

        # 演示图表学习
        demo_chart_learning()

        # 演示高级功能
        demo_advanced_features()

        print("\n" + "="*60)
        print("演示完成！")
        print("="*60)

        print("\n系统特性总结：")
        print("✓ 智能图表推荐 - 基于数据特征自动推荐最佳图表类型")
        print("✓ 多图表库支持 - Plotly（交互式）和Matplotlib（静态）")
        print("✓ 图表学习引擎 - 从案例库提取知识，支持搜索和学习")
        print("✓ 用户偏好支持 - 考虑用户指定的图表类型")
        print("✓ 多数据类型支持 - 时间序列、比较、分布、部分与整体等")
        print("✓ 最佳实践推荐 - 提供图表设计最佳实践和反模式")

    except Exception as e:
        print(f"\n演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
