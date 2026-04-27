"""
增强型学习系统 - 完整演示脚本
展示四大核心功能的集成运行

功能展示：
1. 浏览器自动化网络学习 - 真实网络访问 + 数据权威性评估
2. 动态学习策略引擎 - 场景识别 + 智能策略匹配
3. 智能参数调整系统 - 性能评估 + 自适应优化
4. 增强型三层学习模型 - 完整集成 + 交叉融合
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

from src.neural_memory.browser_automation_learning import (

    BrowserNetworkLearner, DataSourceValidator, DataSourceType, SourceAuthority
)
from src.neural_memory.dynamic_strategy_engine import (
    DynamicStrategyEngine, ScenarioType
)
from src.neural_memory.intelligent_parameter_system import (
    ParameterAdjustmentSystem, PerformanceEvaluator
)


def print_section(title: str):
    """打印分隔线"""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def demo_browser_automation():
    """演示1: 浏览器自动化网络学习"""
    print_section("演示1: 浏览器自动化网络学习")
    
    print("\n【功能说明】")
    print("  ✓ 真实浏览器访问网络")
    print("  ✓ 自动数据提取和清洗")
    print("  ✓ 数据权威性评估 (权威/可信/一般/未验证/不可信)")
    print("  ✓ 数据来源验证")
    print("  ✓ 拒绝编造数据")
    print("  ✓ 缓存管理")
    
    print("\n【数据来源权威性评估】")
    test_sources = [
        ("国家统计局", DataSourceType.OFFICIAL),
        ("清华大学数据库", DataSourceType.ACADEMIC),
        ("艾媒咨询", DataSourceType.PROFESSIONAL),
        ("36氪", DataSourceType.NEWS),
        ("朋友圈分享", DataSourceType.SOCIAL),
        ("某不知名网站", DataSourceType.BLOG),
    ]
    
    for source_name, source_type in test_sources:
        authority, confidence = DataSourceValidator.validate_source(
            source_name, source_type, has_citation=True
        )
        
        # 创建质量指示器
        if confidence >= 0.90:
            indicator = "🟢"  # 绿色 - 优秀
        elif confidence >= 0.75:
            indicator = "🟡"  # 黄色 - 良好
        elif confidence >= 0.50:
            indicator = "🟠"  # 橙色 - 一般
        else:
            indicator = "🔴"  # 红色 - 差
        
        print(f"  {indicator} {source_name:20} → {authority.value:8} (置信度: {confidence:.0%})")
    
    print("\n【学习器初始化】")
    learner = BrowserNetworkLearner(use_playwright=True)
    print(f"  ✓ 学习器初始化完成")
    print(f"  ✓ 缓存目录: {learner.cache_dir}")
    print(f"  ✓ 已加载会话数: {len(learner.session_history)}")
    
    return learner


def demo_dynamic_strategy():
    """演示2: 动态学习策略引擎"""
    print_section("演示2: 动态学习策略引擎")
    
    print("\n【功能说明】")
    print("  ✓ 场景自动识别 (5种场景)")
    print("  ✓ 策略智能匹配")
    print("  ✓ 参数自动生成")
    print("  ✓ 根据洞察优化策略")
    
    print("\n【场景类型】")
    scenarios = [
        ("STABLE", "稳定期", "数据充足，变化不大"),
        ("GROWTH", "增长期", "数据增加，快速变化"),
        ("CRISIS", "危机期", "数据缺失，紧急需求"),
        ("TRANSITION", "转变期", "特征变化，需要适应"),
        ("EXPLORATION", "探索期", "新领域，广泛学习"),
    ]
    
    for code, name, desc in scenarios:
        print(f"  • {name:8} - {desc}")
    
    engine = DynamicStrategyEngine()
    
    print("\n【真实场景识别示例】")
    
    # 场景1: 稳定期
    print("\n  场景1: 稳定期 (数据充足)")
    context1 = engine.identify_scenario(
        local_data_count=15,
        local_data_growth_rate=0.05,
        network_availability=0.95,
        data_quality_trend="stable",
        urgency="normal",
        depth_requirement="deep"
    )
    strategy1 = engine.select_strategy(context1)
    
    print(f"    识别场景: {context1.scenario_type.value}")
    print(f"    选择策略: {strategy1.name}")
    print(f"    本地数据阈值: {strategy1.local_data_threshold}")
    print(f"    网络数据目标: {strategy1.network_data_target}")
    print(f"    权重分配: 本地{strategy1.local_priority_weight:.0%} / 网络{strategy1.network_priority_weight:.0%}")
    
    # 场景2: 危机期
    print("\n  场景2: 危机期 (数据缺失)")
    context2 = engine.identify_scenario(
        local_data_count=0,
        local_data_growth_rate=0.0,
        network_availability=0.90,
        data_quality_trend="unknown",
        urgency="urgent",
        depth_requirement="shallow"
    )
    strategy2 = engine.select_strategy(context2)
    
    print(f"    识别场景: {context2.scenario_type.value}")
    print(f"    选择策略: {strategy2.name}")
    print(f"    本地学习: {'✓ 启用' if strategy2.local_learning_enabled else '✗ 禁用'}")
    print(f"    网络学习: {'✓ 启用' if strategy2.network_learning_enabled else '✗ 禁用'}")
    print(f"    执行时间: {strategy2.max_execution_time}秒 (快速应对)")
    
    # 场景3: 增长期
    print("\n  场景3: 增长期 (数据快速增加)")
    context3 = engine.identify_scenario(
        local_data_count=25,
        local_data_growth_rate=0.40,
        network_availability=0.95,
        data_quality_trend="improving",
        urgency="normal",
        depth_requirement="medium"
    )
    strategy3 = engine.select_strategy(context3)
    
    print(f"    识别场景: {context3.scenario_type.value}")
    print(f"    选择策略: {strategy3.name}")
    print(f"    研究深度: {strategy3.research_depth}")
    print(f"    研究广度: {strategy3.research_breadth}")
    
    # 参数优化
    print("\n【参数优化示例】")
    insights = {
        "average_data_quality": 0.88,
        "local_coverage_rate": 0.85,
        "network_value_rate": 0.72,
        "new_patterns_found": 5,
        "execution_time": 250
    }
    
    print("  原始参数:")
    print(f"    本地阈值: {strategy1.local_data_threshold}")
    print(f"    网络目标: {strategy1.network_data_target}")
    print(f"    本地权重: {strategy1.local_priority_weight:.1%}")
    
    optimized = engine.optimize_strategy_parameters(strategy1, insights)
    
    print("  优化后参数:")
    print(f"    本地阈值: {optimized.local_data_threshold} (调整为: {optimized.local_data_threshold})")
    print(f"    网络目标: {optimized.network_data_target} (调整为: {optimized.network_data_target})")
    print(f"    本地权重: {optimized.local_priority_weight:.1%} (调整为: {optimized.local_priority_weight:.1%})")
    
    return engine


def demo_parameter_adjustment():
    """演示3: 智能参数调整系统"""
    print_section("演示3: 智能参数调整系统")
    
    print("\n【功能说明】")
    print("  ✓ 性能自动评估 (8个维度)")
    print("  ✓ 智能参数调整")
    print("  ✓ 调整约束管理")
    print("  ✓ 调整历史记录")
    print("  ✓ 反馈循环优化")
    
    system = ParameterAdjustmentSystem()
    
    print("\n【初始参数配置】")
    initial_params = {
        "local_data_threshold": 5,
        "network_data_target": 10,
        "max_execution_time": 300,
        "data_quality_threshold": 0.7,
        "research_breadth": "medium",
    }
    
    for k, v in initial_params.items():
        print(f"  {k:30}: {v}")
    
    print("\n【执行1: 高质量学习结果】")
    results1 = {
        "data_points": [
            {"quality": 0.9, "has_source": True, "authority": "权威"},
            {"quality": 0.85, "has_source": True, "authority": "可信"},
            {"quality": 0.88, "has_source": True, "authority": "权威"},
        ] * 5,  # 15条高质量数据
        "patterns": [{"type": "trend"}] * 4,
        "insights": [{"value": "insight"}] * 3,
        "execution_time": 250,
        "errors": [],
    }
    
    metrics1 = system.record_learning_result(results1, initial_params)
    print(f"  性能评估:")
    print(f"    有效数据: {metrics1.data_points_collected} ({metrics1.valid_data_ratio:.0%})")
    print(f"    平均质量: {metrics1.average_quality:.2f}")
    print(f"    发现模式: {metrics1.patterns_discovered} 个")
    print(f"    学习效率: {metrics1.learning_effectiveness:.2f}")
    print(f"    综合评分: {metrics1.overall_score:.2f} ({metrics1.satisfaction_level})")
    
    # 自动调整
    adjusted1, adjustments1 = system.adjust_parameters(initial_params, metrics1)
    if adjustments1:
        print(f"  自动调整:")
        for adj in adjustments1:
            print(f"    {adj.parameter_name}: {adj.old_value} → {adj.new_value} ({adj.reason})")
    else:
        print(f"  无需调整")
    
    print("\n【执行2: 低效率学习结果】")
    results2 = {
        "data_points": [
            {"quality": 0.5, "has_source": False, "authority": "未验证"},
            {"quality": 0.3, "has_source": False, "authority": "未验证"},
        ],
        "patterns": [],
        "insights": [],
        "execution_time": 800,
        "errors": ["timeout", "network_error"],
    }
    
    metrics2 = system.record_learning_result(results2, adjusted1)
    print(f"  性能评估:")
    print(f"    有效数据: {metrics2.data_points_collected} ({metrics2.valid_data_ratio:.0%})")
    print(f"    平均质量: {metrics2.average_quality:.2f}")
    print(f"    综合评分: {metrics2.overall_score:.2f} ({metrics2.satisfaction_level})")
    
    # 激进调整
    adjusted2, adjustments2 = system.adjust_parameters(adjusted1, metrics2, aggressive=True)
    if adjustments2:
        print(f"  激进调整:")
        for adj in adjustments2:
            print(f"    {adj.parameter_name}: {adj.old_value} → {adj.new_value} ({adj.direction.value})")
    
    # 调整总结
    print("\n【调整总结】")
    summary = system.get_adjustment_summary()
    print(f"  总调整次数: {summary['total_adjustments']}")
    if summary.get('most_adjusted_parameter'):
        print(f"  最常调整: {summary['most_adjusted_parameter']} ({summary['adjustment_frequency']}次)")
    
    return system


def demo_integration():
    """演示4: 完整系统集成"""
    print_section("演示4: 完整系统集成")
    
    print("\n【整体架构】")
    print("""
    输入层 (场景信息)
         ↓
    ┌─────────────────────────────────┐
    │ 1. 场景识别 (DynamicStrategy)  │ ← 自动识别当前学习场景
    └─────────────────┬───────────────┘
                      ↓
    ┌─────────────────────────────────┐
    │ 2. 策略选择 (StrategyLibrary)   │ ← 匹配最优学习策略
    └─────────────────┬───────────────┘
                      ↓
    ┌─────────────────────────────────┐
    │ 3. 执行参数生成                  │ ← 生成具体执行参数
    └─────────────────┬───────────────┘
                      ↓
    ┌─────────────────────────────────┐
    │ 4. 浏览器学习 (Browser + Auth)  │ ← 真实网络访问 + 权威性评估
    └─────────────────┬───────────────┘
                      ↓
    ┌─────────────────────────────────┐
    │ 5. 本地学习 (Local Data)        │ ← 本地数据处理
    └─────────────────┬───────────────┘
                      ↓
    ┌─────────────────────────────────┐
    │ 6. 交叉融合 (Cross Learning)    │ ← 两层融合生成洞察
    └─────────────────┬───────────────┘
                      ↓
    ┌─────────────────────────────────┐
    │ 7. 性能评估 (Evaluator)         │ ← 8维度性能评分
    └─────────────────┬───────────────┘
                      ↓
    ┌─────────────────────────────────┐
    │ 8. 参数优化 (ParamAdjustment)   │ ← 自动调整参数
    └─────────────────┬───────────────┘
                      ↓
    输出层 (优化的系统)
    """)
    
    print("\n【系统特性】")
    features = [
        ("真实网络访问", "Playwright浏览器自动化，访问真实网站"),
        ("权威性评估", "5级权威性分类，拒绝编造数据"),
        ("动态策略", "5种场景预定义策略，智能匹配"),
        ("智能参数", "基于性能反馈自动调整参数"),
        ("反馈循环", "持续改进，自适应优化"),
        ("完整融合", "本地+网络交叉学习，生成高价值洞察"),
    ]
    
    for i, (name, desc) in enumerate(features, 1):
        print(f"  {i}. {name:12} - {desc}")


def main():
    """主函数"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + "  智能办公助手 - 增强型学习系统完整演示".center(68) + "║")
    print("║" + "  Enhanced Three-Tier Learning with AI Optimization".center(68) + "║")
    print("╚" + "=" * 68 + "╝")
    
    # 演示1: 浏览器自动化
    browser_learner = demo_browser_automation()
    
    # 演示2: 动态策略
    strategy_engine = demo_dynamic_strategy()
    
    # 演示3: 参数调整
    param_system = demo_parameter_adjustment()
    
    # 演示4: 集成
    demo_integration()
    
    # 总结
    print_section("总结")
    
    print("\n【核心成就】")
    print("  ✅ 浏览器自动化网络学习模块")
    print("     - 真实网络访问 (Playwright)")
    print("     - 数据权威性评估系统")
    print("     - 5级权威性分类")
    print("     - 数据来源验证")
    print("     - 缓存管理")
    
    print("\n  ✅ 动态学习策略引擎")
    print("     - 5种场景识别")
    print("     - 预定义策略库")
    print("     - 智能策略匹配")
    print("     - 参数自动生成")
    print("     - 洞察驱动优化")
    
    print("\n  ✅ 智能参数调整系统")
    print("     - 8维度性能评估")
    print("     - 10+ 条调整规则")
    print("     - 自适应参数优化")
    print("     - 约束管理")
    print("     - 调整历史记录")
    
    print("\n  ✅ 增强型三层学习模型")
    print("     - 完整系统集成")
    print("     - 场景识别 → 策略选择 → 参数生成")
    print("     - 浏览器学习 → 本地学习 → 交叉融合")
    print("     - 性能评估 → 参数优化 → 反馈循环")
    print("     - 生产级实现")
    
    print("\n【下一步建议】")
    print("  1. 集成到 automation-3 自动化任务")
    print("  2. 配置每日09:00自动执行")
    print("  3. 监控报告输出目录")
    print("  4. 持续优化调整规则")
    print("  5. 扩展网络数据源")
    
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
