"""
图表自动生成系统增强演示 - 完整功能展示
展示图表生成、推荐、嵌入PPT、样式自适应等完整流程
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)


from ppt.chart_generator import (
    ChartGenerator, ChartType, ChartLibrary,
    DataAnalyzer, ChartRecommender
)
from ppt.chart_style_adapter import ChartStyleAdapter
from ppt.chart_embedder import ChartEmbedder
from ppt.ppt_service import PPTService

import pandas as pd
import numpy as np
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def demo_data_analysis():
    """演示数据分析"""
    print("\n" + "="*60)
    print("1. 数据分析演示")
    print("="*60)

    analyzer = DataAnalyzer()

    # 时间序列数据
    print("\n【时间序列数据】")
    time_series_data = {
        "日期": pd.date_range("2024-01-01", periods=12, freq="M"),
        "销售额": [100, 120, 150, 180, 200, 220, 240, 260, 280, 300, 320, 340]
    }
    feature = analyzer.analyze_data(time_series_data)
    print(f"  - 时间序列: {feature.has_time_series}")
    print(f"  - 数值型: {feature.is_numerical}")
    print(f"  - 数据量: {feature.data_volume}")
    print(f"  - 观测数: {feature.observation_count}")

    # 比较数据
    print("\n【比较数据】")
    comparison_data = {
        "产品": ["产品A", "产品B", "产品C", "产品D"],
        "Q1": [100, 120, 90, 110],
        "Q2": [110, 130, 95, 120],
        "Q3": [115, 140, 100, 125]
    }
    feature = analyzer.analyze_data(comparison_data)
    print(f"  - 比较关系: {feature.is_comparison}")
    print(f"  - 数值列数: {len(feature.numeric_columns)}")

    # 部分与整体数据
    print("\n【部分与整体数据】")
    part_whole_data = {
        "类别": ["销售", "市场", "研发", "运营"],
        "预算": [300, 200, 150, 100]
    }
    feature = analyzer.analyze_data(part_whole_data)
    print(f"  - 部分与整体: {feature.is_part_to_whole}")
    print(f"  - 分类列数: {len(feature.categorical_columns)}")


def demo_chart_recommendation():
    """演示图表推荐"""
    print("\n" + "="*60)
    print("2. 图表推荐演示")
    print("="*60)

    recommender = ChartRecommender()

    # 时间序列数据推荐
    print("\n【时间序列数据推荐】")
    time_data = {
        "日期": pd.date_range("2024-01-01", periods=6, freq="M"),
        "销售额": [100, 120, 150, 180, 200, 220]
    }
    recommendations = recommender.recommend(time_data)

    print(f"  推荐 {len(recommendations)} 种图表类型:")
    for i, rec in enumerate(recommendations[:5], 1):
        print(f"    {i}. {rec.chart_type.value} (置信度: {rec.confidence:.2f})")
        print(f"       原因: {rec.reason}")

    # 比较数据推荐
    print("\n【比较数据推荐】")
    comp_data = {
        "产品": ["A", "B", "C", "D"],
        "Q1": [100, 120, 90, 110],
        "Q2": [110, 130, 95, 120]
    }
    recommendations = recommender.recommend(comp_data)

    print(f"  推荐 {len(recommendations)} 种图表类型:")
    for i, rec in enumerate(recommendations[:5], 1):
        print(f"    {i}. {rec.chart_type.value} (置信度: {rec.confidence:.2f})")


def demo_style_adaptation():
    """演示样式自适应"""
    print("\n" + "="*60)
    print("3. 样式自适应演示")
    print("="*60)

    adapter = ChartStyleAdapter()

    themes = ["business", "tech", "education", "creative", "minimal"]
    for theme in themes:
        print(f"\n【{theme.upper()} 主题】")
        style = adapter.adapt_style("bar", 10, theme=theme)
        print(f"  - 字体: {style.font_family}")
        print(f"  - 字号: {style.font_size}")
        print(f"  - 颜色数量: {len(style.color_palette)}")
        print(f"  - 显示网格: {style.show_grid}")
        print(f"  - 显示图例: {style.show_legend}")


def demo_chart_generation():
    """演示图表生成"""
    print("\n" + "="*60)
    print("4. 图表生成演示")
    print("="*60)

    generator = ChartGenerator()

    # 生成时间序列图表
    print("\n【生成时间序列折线图】")
    time_data = {
        "日期": pd.date_range("2024-01-01", periods=12, freq="M"),
        "销售额": [100, 120, 150, 180, 200, 220, 240, 260, 280, 300, 320, 340]
    }

    try:
        filepath, recommendation = generator.generate_chart(
            data=time_data,
            title="2024年销售趋势"
        )
        print(f"  ✓ 图表已生成: {filepath}")
        print(f"  ✓ 推荐类型: {recommendation.chart_type.value}")
        print(f"  ✓ 置信度: {recommendation.confidence:.2f}")
    except Exception as e:
        print(f"  ✗ 图表生成失败: {e}")

    # 生成饼图
    print("\n【生成预算分配饼图】")
    pie_data = {
        "部门": ["销售", "市场", "研发", "运营"],
        "预算": [300, 200, 150, 100]
    }

    try:
        filepath, recommendation = generator.generate_chart(
            data=pie_data,
            chart_type=ChartType.PIE,
            title="2024年预算分配"
        )
        print(f"  ✓ 图表已生成: {filepath}")
        print(f"  ✓ 推荐类型: {recommendation.chart_type.value}")
    except Exception as e:
        print(f"  ✗ 图表生成失败: {e}")

    # 生成堆叠柱状图
    print("\n【生成分季度堆叠柱状图】")
    stack_data = {
        "产品": ["产品A", "产品B", "产品C"],
        "Q1": [100, 120, 90],
        "Q2": [110, 130, 95],
        "Q3": [115, 140, 100]
    }

    try:
        filepath, recommendation = generator.generate_chart(
            data=stack_data,
            chart_type=ChartType.STACKED_BAR,
            title="分季度销售对比"
        )
        print(f"  ✓ 图表已生成: {filepath}")
        print(f"  ✓ 推荐类型: {recommendation.chart_type.value}")
    except Exception as e:
        print(f"  ✗ 图表生成失败: {e}")


def demo_ppt_service():
    """演示PPT服务集成"""
    print("\n" + "="*60)
    print("5. PPT服务集成演示")
    print("="*60)

    service = PPTService(theme="business", enable_charts=True)

    # 生成图表并获取推荐
    print("\n【生成图表】")
    data = {
        "月份": ["1月", "2月", "3月", "4月", "5月", "6月"],
        "销售额": [100, 120, 150, 180, 200, 220]
    }

    try:
        filepath, recommendation = service.generate_chart(
            data=data,
            title="上半年销售趋势"
        )
        print(f"  ✓ 图表已生成: {filepath}")
    except Exception as e:
        print(f"  ✗ 图表生成失败: {e}")
        return

    # 获取推荐列表
    print("\n【获取图表推荐列表】")
    try:
        recommendations = service.get_chart_recommendations(data)
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"  {i}. {rec['chart_type']} (置信度: {rec['confidence']:.2f})")
            print(f"     {rec['reason']}")
    except Exception as e:
        print(f"  ✗ 获取推荐失败: {e}")

    # 查询最佳实践
    print("\n【查询图表最佳实践】")
    try:
        best_practices = service.get_chart_best_practices("line")
        print(f"  折线图最佳实践 ({len(best_practices)} 条):")
        for i, practice in enumerate(best_practices[:3], 1):
            print(f"    {i}. {practice}")
    except Exception as e:
        print(f"  ✗ 查询最佳实践失败: {e}")

    # 搜索图表知识
    print("\n【搜索图表知识】")
    try:
        results = service.search_chart_knowledge("折线图", limit=2)
        print(f"  找到 {len(results)} 条相关知识:")
        for i, result in enumerate(results, 1):
            print(f"    {i}. {result['title']}")
            print(f"       相关性: {result['relevance_score']:.2f}")
    except Exception as e:
        print(f"  ✗ 搜索知识失败: {e}")


def demo_complete_workflow():
    """演示完整工作流程"""
    print("\n" + "="*60)
    print("6. 完整工作流程演示")
    print("="*60)

    print("\n【创建PPT服务】")
    service = PPTService(theme="business", enable_charts=True)

    print("\n【生成多个图表】")
    chart_paths = []

    # 图表1: 销售趋势
    data1 = {
        "月份": ["1月", "2月", "3月", "4月", "5月", "6月"],
        "销售额": [100, 120, 150, 180, 200, 220]
    }
    try:
        path1, _ = service.generate_chart(data1, title="销售趋势")
        chart_paths.append(path1)
        print(f"  ✓ 图表1已生成")
    except:
        print(f"  ✗ 图表1生成失败")

    # 图表2: 预算分配
    data2 = {
        "部门": ["销售", "市场", "研发", "运营"],
        "预算": [300, 200, 150, 100]
    }
    try:
        path2, _ = service.generate_chart(data2, chart_type=ChartType.PIE, title="预算分配")
        chart_paths.append(path2)
        print(f"  ✓ 图表2已生成")
    except:
        print(f"  ✗ 图表2生成失败")

    # 图表3: 产品对比
    data3 = {
        "产品": ["A", "B", "C", "D"],
        "Q1": [100, 120, 90, 110],
        "Q2": [110, 130, 95, 120]
    }
    try:
        path3, _ = service.generate_chart(data3, chart_type=ChartType.GROUPED_BAR, title="产品对比")
        chart_paths.append(path3)
        print(f"  ✓ 图表3已生成")
    except:
        print(f"  ✗ 图表3生成失败")

    # 创建仪表板
    if len(chart_paths) >= 2:
        print(f"\n【创建图表仪表板】")
        try:
            dashboard_path = service.create_chart_dashboard(
                chart_paths=chart_paths,
                output_path="outputs/chart_dashboard.pptx",
                layout="grid",
                titles=["销售趋势", "预算分配", "产品对比"]
            )
            print(f"  ✓ 仪表板已创建: {dashboard_path}")
        except Exception as e:
            print(f"  ✗ 仪表板创建失败: {e}")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("图表自动生成系统 - 完整功能演示")
    print("版本: v1.0 (优化版)")
    print("="*60)

    try:
        # 1. 数据分析演示
        demo_data_analysis()

        # 2. 图表推荐演示
        demo_chart_recommendation()

        # 3. 样式自适应演示
        demo_style_adaptation()

        # 4. 图表生成演示
        demo_chart_generation()

        # 5. PPT服务集成演示
        demo_ppt_service()

        # 6. 完整工作流程演示
        demo_complete_workflow()

        print("\n" + "="*60)
        print("✓ 所有演示完成！")
        print("="*60)

    except Exception as e:
        logger.error(f"演示过程中发生错误: {e}", exc_info=True)
        print(f"\n✗ 演示失败: {e}")


if __name__ == "__main__":
    main()
