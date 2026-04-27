"""
三层学习模型演示脚本

展示：
1. 本地学习（可选）- 有数据则学习，无数据则跳过
2. 网络学习（必须）- 每日必须执行
3. 交叉融合（条件）- 当两层都有数据时触发
"""

import sys
from pathlib import Path

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

from src.neural_memory.three_tier_learning import (

    ThreeTierLearningExecutor,
    run_daily_three_tier_learning
)
import json


def print_header(title):
    """打印标题"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_task_result(task_name, task):
    """打印任务结果"""
    print(f"\n【{task_name}】")
    print(f"  任务ID: {task.task_id}")
    print(f"  状态: {task.status.value}")
    
    if hasattr(task, 'should_execute'):
        print(f"  执行: {'是' if task.should_execute else '否'}")
        print(f"  原因: {task.reason}")
        print(f"  数据条数: {task.data_count}")
    
    if hasattr(task, 'topics'):
        print(f"  研究主题: {len(task.topics)}个")
        print(f"  发现: {len(task.findings)}个")
    
    if hasattr(task, 'correlations'):
        print(f"  关联: {len(task.correlations)}个")
        print(f"  模式: {len(task.patterns)}个")
        print(f"  洞察: {len(task.insights)}个")
        
        if task.insights:
            print(f"  主要洞察:")
            for insight in task.insights:
                print(f"    • {insight}")


def demo_basic_usage():
    """演示基本使用"""
    print_header("演示1: 基本使用 - 执行日报告")
    
    report = run_daily_three_tier_learning()
    
    print(f"\n报告ID: {report.report_id}")
    print(f"执行日期: {report.execution_date}")
    
    # 打印各层任务结果
    if report.local_learning:
        print_task_result("本地学习层（可选）", report.local_learning)
    
    if report.network_learning:
        print_task_result("网络学习层（必须）", report.network_learning)
    
    if report.cross_learning:
        print_task_result("交叉融合层（条件）", report.cross_learning)
    
    # 打印执行流程
    print("\n【执行流程】")
    print(report.summary['execution_flow'])
    
    # 打印摘要
    print("\n【执行摘要】")
    for key, value in report.summary.items():
        if key != 'execution_flow':
            print(f"  {key}:")
            if isinstance(value, dict):
                for k, v in value.items():
                    print(f"    {k}: {v}")


def demo_scenarios():
    """演示不同场景"""
    print_header("演示2: 场景分析 - 三种执行模式")
    
    executor = ThreeTierLearningExecutor()
    
    # 场景1: 本地无数据，网络执行
    print("\n【场景1】本地无新数据 → 本地学习跳过 + 网络学习执行")
    print("  预期流程:")
    print("  ├─ 本地学习: ⊘ 跳过")
    print("  ├─ 网络学习: ✅ 执行（必须）")
    print("  └─ 交叉融合: ⊘ 未触发（缺少本地数据）")
    
    # 场景2: 两层都有数据
    print("\n【场景2】本地有数据 + 网络学习")
    print("  预期流程:")
    print("  ├─ 本地学习: ✅ 执行")
    print("  ├─ 网络学习: ✅ 执行（必须）")
    print("  └─ 交叉融合: ✅ 触发（两层都有数据）")
    print("             ├─ 发现关联")
    print("             ├─ 提取模式")
    print("             └─ 生成洞察")
    
    # 场景3: 完整执行
    print("\n【场景3】完整执行 - 当前实际执行")
    report = executor.execute_daily_learning()
    
    print(f"  本地学习执行: {report.local_learning.should_execute}")
    print(f"  网络学习执行: True (必须)")
    print(f"  交叉融合触发: {report.cross_learning.status.value == '已完成'}")
    
    if report.cross_learning.insights:
        print(f"  生成洞察: {len(report.cross_learning.insights)}个")


def demo_configuration():
    """演示配置调整"""
    print_header("演示3: 配置调整 - 自定义阈值")
    
    executor = ThreeTierLearningExecutor()
    
    print("\n默认配置:")
    print(f"  本地数据阈值: {executor.local_data_threshold} (≥此数则执行)")
    print(f"  网络学习: 必须执行")
    print(f"  交叉触发: 两层都≥1条数据")
    
    print("\n可调整参数:")
    print("  executor.local_data_threshold = 3  # 本地数据≥3条时执行")
    print("  executor.network_data_threshold = 1  # 网络必须执行")
    print("  executor.cross_trigger_threshold = 2  # 交叉融合的数据触发数")
    
    # 修改配置
    executor.local_data_threshold = 2
    print(f"\n修改后本地阈值: {executor.local_data_threshold}")


def demo_report_structure():
    """演示报告结构"""
    print_header("演示4: 报告结构 - 完整报告示例")
    
    report = run_daily_three_tier_learning()
    
    print("\n报告包含四个部分:")
    print("\n1️⃣ 本地学习结果:")
    print(f"   {json.dumps(report.summary['local_learning'], indent=2, ensure_ascii=False)}")
    
    print("\n2️⃣ 网络学习结果:")
    print(f"   {json.dumps(report.summary['network_learning'], indent=2, ensure_ascii=False)}")
    
    print("\n3️⃣ 交叉融合结果:")
    print(f"   {json.dumps(report.summary['cross_learning'], indent=2, ensure_ascii=False)}")
    
    print("\n4️⃣ 执行流程:")
    print(report.summary['execution_flow'])


def demo_comparison():
    """演示新旧对比"""
    print_header("演示5: 新旧学习模型对比")
    
    print("\n【旧模型】网络优先 + 本地补充:")
    print("  ├─ 优点: 数据覆盖广泛")
    print("  ├─ 缺点: 本地数据可能被忽视")
    print("  └─ 问题: 无法充分利用内部数据")
    
    print("\n【新模型】三层学习 - 本地可选 + 网络必须 + 交叉融合:")
    print("  ├─ 优点1: 本地优先（充分利用内部数据）")
    print("  ├─ 优点2: 网络必须（保证知识丰富性）")
    print("  ├─ 优点3: 交叉融合（生成高价值洞察）")
    print("  ├─ 优点4: 灵活自适应（可选执行，降低成本）")
    print("  └─ 优点5: 提升质量（两层数据交叉验证）")
    
    print("\n执行时间表:")
    print("  每日09:00自动执行三层学习流程")
    print("  ├─ 本地学习: 根据数据自动决策（有则执行，无则跳过）")
    print("  ├─ 网络学习: 必须执行（独立、不受本地影响）")
    print("  ├─ 交叉融合: 条件触发（两层都有数据时）")
    print("  └─ 报告输出: 统一汇总报告")


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  三层学习模型 (Three-Tier Learning) 演示程序".center(78) + "║")
    print("║" + "  本地可选 + 网络必须 + 交叉融合".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    
    try:
        # 演示1: 基本使用
        demo_basic_usage()
        
        # 演示2: 场景分析
        demo_scenarios()
        
        # 演示3: 配置调整
        demo_configuration()
        
        # 演示4: 报告结构
        demo_report_structure()
        
        # 演示5: 新旧对比
        demo_comparison()
        
        print_header("演示完成 ✅")
        
        print("\n使用建议:")
        print("  1. 集成到自动化任务 (automation-3)")
        print("  2. 配置定时执行 (每日09:00)")
        print("  3. 监控报告输出 (data/learning/reports/)")
        print("  4. 根据业务调整阈值参数")
        print("\n快速开始:")
        print("  from src.neural_memory.three_tier_learning import run_daily_three_tier_learning")
        print("  report = run_daily_three_tier_learning()")
        
    except Exception as e:
        print(f"\n❌ 演示过程中出错: {e}")
        import traceback
        traceback.print_exc()
