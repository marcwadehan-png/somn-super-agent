#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
演示脚本：学习系统 v2.0 - 统一架构 + 本地优先策略
Demonstration Script: Unified Learning System

运行方式:
  cd smart_office_assistant
  python scripts/demo/demo_new_learning_system.py
"""

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

from src.neural_memory.unified_learning_orchestrator import (
    UnifiedLearningOrchestrator,
    SchedulerConfig,
    SchedulerStrategyMode,
    LearningStrategyType,
)
from src.neural_memory.learning_scheduler import LearningScheduler, LearningStrategy


def demo_unified_orchestrator():
    """演示1: 统一调度器 - 数据源扫描和规划"""
    print("\n" + "="*70)
    print("演示1: UnifiedLearningOrchestrator - 数据源扫描和规划")
    print("="*70)

    orchestrator = UnifiedLearningOrchestrator()

    # 扫描数据源
    print("\n[步骤1] 扫描可用数据源...")
    sources = orchestrator.scan_data_sources()

    print("\n数据源统计:")
    if isinstance(sources, dict):
        for key, val in sources.items():
            print(f"  {key}: {val}")

    # 规划学习
    print("\n[步骤2] 规划学习数据选择...")
    plan = orchestrator.plan_learning_data_selection()

    print(f"\n学习规划结果:")
    print(f"  策略: {plan.get('strategy', 'N/A')}")
    print(f"  本地数据: {len(plan.get('local_data', []))} 条")
    print(f"  网络数据: {len(plan.get('network_data', []))} 条")
    print(f"  总计: {plan.get('total_data', 0)} 条")

    breakdown = plan.get('data_source_breakdown', {})
    if breakdown:
        print(f"  数据源分布: {breakdown}")

    if plan.get('recommendations'):
        print(f"\n学习建议:")
        for i, rec in enumerate(plan['recommendations'], 1):
            print(f"  {i}. {rec}")


def demo_strategy_switching():
    """演示2: 切换调度策略"""
    print("\n" + "="*70)
    print("演示2: 调度策略切换")
    print("="*70)

    orchestrator = UnifiedLearningOrchestrator()

    modes = [
        SchedulerStrategyMode.LOCAL_ONLY,
        SchedulerStrategyMode.LOCAL_FIRST,
        SchedulerStrategyMode.LOCAL_NETWORK_HYBRID,
        SchedulerStrategyMode.NETWORK_ONLY
    ]

    for mode in modes:
        print(f"\n[切换策略] {mode.value}")
        config = SchedulerConfig(strategy_mode=mode)
        orchestrator.set_config(config)

        plan = orchestrator.plan_learning_data_selection()
        print(f"  本地数据: {len(plan.get('local_data', []))} 条")
        print(f"  网络数据: {len(plan.get('network_data', []))} 条")

        if plan.get('recommendations'):
            print(f"  建议: {plan['recommendations'][0]}")

    # 恢复默认
    default_config = SchedulerConfig()
    orchestrator.set_config(default_config)
    print(f"\n已恢复默认策略: LOCAL_FIRST")


def demo_parameter_adjustment():
    """演示3: 参数调整"""
    print("\n" + "="*70)
    print("演示3: 调度参数调整")
    print("="*70)

    print("\n[调整1] 本地数据阈值")
    print("  场景A: 降低到3（更依赖本地）")
    config_a = SchedulerConfig(local_threshold=3)
    orch = UnifiedLearningOrchestrator()
    orch.set_config(config_a)
    status_a = orch.get_status()
    print(f"    阈值: {status_a['config']['local_threshold']}")

    print("\n  场景B: 提高到8（更易触发网络）")
    config_b = SchedulerConfig(local_threshold=8)
    orch.set_config(config_b)
    status_b = orch.get_status()
    print(f"    阈值: {status_b['config']['local_threshold']}")

    print("\n[调整2] 网络补充比例")
    print("  场景C: 降低到0.1（轻量补充）")
    config_c = SchedulerConfig(network_supplement_ratio=0.1)
    orch.set_config(config_c)
    print(f"    比例: {0.1:.1%}")

    print("\n  场景D: 提高到0.5（充分补充）")
    config_d = SchedulerConfig(network_supplement_ratio=0.5)
    orch.set_config(config_d)
    print(f"    比例: {0.5:.1%}")

    # 恢复默认
    orch.set_config(SchedulerConfig())
    print("\n已恢复默认参数")


def demo_daily_learning():
    """演示4: 执行每日学习"""
    print("\n" + "="*70)
    print("演示4: 执行每日学习流程")
    print("="*70)

    orchestrator = UnifiedLearningOrchestrator()

    print("\n即将执行每日学习...")
    print("步骤: 扫描数据 → 执行策略 → 生成报告")

    try:
        report = orchestrator.execute_daily()

        print(f"\n学习执行完成")
        print(f"  报告ID: {report.report_id}")
        print(f"  学习事件: {report.total_learning_events}")
        print(f"  知识更新: {report.total_knowledge_updates}")
        print(f"  总耗时: {report.total_duration_seconds:.2f}s")
        print(f"  总结: {report.summary}")

        if report.recommendations:
            print(f"\n建议:")
            for r in report.recommendations:
                print(f"  - {r}")

    except Exception as e:
        print(f"\n学习执行异常: {e}")


def demo_plan_and_execute():
    """演示5: 完整学习周期（计划 → 执行）"""
    print("\n" + "="*70)
    print("演示5: 完整学习周期 (plan_and_execute)")
    print("="*70)

    orchestrator = UnifiedLearningOrchestrator()

    try:
        result = orchestrator.plan_and_execute()

        print(f"\n执行完成")
        print(f"  成功: {result.get('success', False)}")

        if result.get('report'):
            report = result['report']
            if isinstance(report, dict):
                print(f"  学习事件: {report.get('total_learning_events', 0)}")
                print(f"  知识更新: {report.get('total_knowledge_updates', 0)}")
            else:
                print(f"  学习事件: {report.total_learning_events}")
                print(f"  知识更新: {report.total_knowledge_updates}")

    except Exception as e:
        print(f"\n执行异常: {e}")


def demo_legacy_compatibility():
    """演示6: 旧接口兼容性（LearningScheduler）"""
    print("\n" + "="*70)
    print("演示6: 旧接口兼容性 - LearningScheduler")
    print("="*70)

    scheduler = LearningScheduler()

    print("\n[兼容层] 旧接口仍可正常使用:")
    sources = scheduler.scan_data_sources()
    print(f"  数据源数量: {len(sources)}")

    plan = scheduler.plan_learning_data_selection()
    print(f"  策略: {plan.get('strategy', 'N/A')}")
    print(f"  总数据: {plan.get('total_data', 0)} 条")

    if plan.get('recommendations'):
        print(f"  建议: {plan['recommendations'][0]}")

    print("\n  说明: LearningScheduler 内部路由到 UnifiedLearningOrchestrator")
    print("  新代码建议直接使用 UnifiedLearningOrchestrator")


def print_welcome():
    """打印欢迎信息"""
    print("\n" + "="*70)
    print("学习系统 v2.0 演示 - 统一架构 + 本地优先策略")
    print("="*70)
    print("""
    本演示展示 v2.0 统一学习系统的完整功能:

    架构:
    - UnifiedLearningOrchestrator: 统一调度入口
    - 5种策略: Daily / ThreeTier / Enhanced / Solution / Feedback
    - UnifiedDataScanner: 消除重复的数据扫描
    - 兼容层: LearningScheduler / IntegratedLearningExecutor 仍可用

    核心策略 (SchedulerStrategyMode):
    - LOCAL_ONLY:           仅本地
    - LOCAL_FIRST:          本地优先 (默认)
    - LOCAL_NETWORK_HYBRID: 混合学习
    - NETWORK_ONLY:         仅网络

    演示内容:
    1. 统一调度器 - 数据源扫描和规划
    2. 调度策略切换
    3. 参数调整
    4. 每日学习执行
    5. 完整学习周期
    6. 旧接口兼容性
    """)


def main():
    """主演示流程"""
    print_welcome()

    print("\n" + "-"*70)
    print("开始演示...")
    print("-"*70)

    demo_unified_orchestrator()
    demo_strategy_switching()
    demo_parameter_adjustment()
    demo_daily_learning()
    demo_plan_and_execute()
    demo_legacy_compatibility()

    # 总结
    print("\n" + "="*70)
    print("所有演示完成")
    print("="*70)
    print("""
    总结:

    v2.0 统一架构提供了:
    - 单一调度入口: UnifiedLearningOrchestrator
    - 5种可插拔学习策略
    - 4种调度策略模式 (本地优先/混合/纯网络)
    - 7个可配置参数
    - 完整的兼容层 (旧代码无需修改)

    后续步骤:
    1. 查看策略文档: data/learning/LEARNING_STRATEGY.md
    2. 修改配置:     data/learning/learning_schedule.yaml
    3. 运行快速入口: python -c "from src.neural_memory.unified_learning_orchestrator import run_unified_learning; run_unified_learning()"
    """)


if __name__ == '__main__':
    main()
