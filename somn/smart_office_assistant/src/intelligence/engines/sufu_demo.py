"""
__all__ = [
    'demo_cultivation',
    'demo_five_principles',
    'demo_fortune_assessment',
    'demo_general_decision',
    'demo_reasoning_integration',
    'demo_risk_warning',
    'demo_talent_assessment',
    'main',
    'print_header',
    'print_section',
]

素书智慧演示脚本
Sufu Wisdom Demo

展示<素书>智慧在Somn系统中的应用

运行方法:
    python src/intelligence/sufu_demo.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

from src.intelligence.engines.sufu_wisdom_core import (
    get_sufu_core,
    SufuPrinciple,
    SufuWisdomCore
)

def print_header(text: str):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_section(text: str):
    """打印分节标题"""
    print(f"\n## {text}")

def demo_five_principles():
    """演示五德原则"""
    print_header("<素书>五德原则")
    
    sufu = get_sufu_core()
    wisdom_summary = sufu.get_wisdom_summary()
    
    print("\n### 核心五德原则")
    for principle, desc in wisdom_summary["core_principles"].items():
        print(f"\n  [{principle}]")
        print(f"      {desc}")
    
    print("\n### 人才三境(正道章)")
    for level, qualities in wisdom_summary["talent_levels"].items():
        print(f"\n  [{level}]: {qualities}")
    
    print("\n### 警示要点(遵义章)")
    for warning in wisdom_summary["key_warnings"]:
        print(f"  ⚠️  {warning}")

def demo_talent_assessment():
    """演示人才评估"""
    print_header("正道章人才评估演示")
    
    sufu = get_sufu_core()
    
    # 模拟人才数据
    talent_situation = {
        "type": "talent",
        "person": {
            "德足以怀远": True,
            "信足以一异": True,
            "义足以得众": True,
            "才足以鉴古": True,
            "明足以照下": True,
        }
    }
    
    decision = sufu.make_decision(talent_situation)
    
    print(f"\n[评估结果]")
    print(f"  原则: {decision.principle.value}")
    print(f"  推理: {decision.reasoning}")
    print(f"  建议: {decision.action}")
    print(f"  来源: {decision.wisdom_source}")
    print(f"  平衡分数: {decision.balance_score:.2f}")
    print(f"  预期: {decision.expected_outcome}")

def demo_cultivation():
    """演示修身指导"""
    print_header("求人之志章修身指导演示")
    
    sufu = get_sufu_core()
    
    print("\n### 不同层级的修身方法")
    for level in [2, 5, 8]:
        print(f"\n[层级 {level}/10]")
        guide = sufu.get_cultivation_guide(level)
        for method in guide:
            print(f"  ✦ {method}")

def demo_risk_warning():
    """演示风险预警"""
    print_header("遵义章风险预警演示")
    
    sufu = get_sufu_core()
    
    # 测试场景
    scenarios = [
        {
            "type": "leadership",
            "content": "领导者在下属面前炫耀自己的成就"
        },
        {
            "type": "decision",
            "content": "固执己见,有错误也不承认"
        },
        {
            "type": "communication",
            "content": "口无遮拦,得罪了很多人"
        }
    ]
    
    print("\n### 风险检测结果")
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n[场景 {i}]: {scenario['content']}")
        warnings = sufu.warn_of_danger(scenario)
        for warning in warnings:
            print(f"  {warning}")

def demo_fortune_assessment():
    """演示福祸评估"""
    print_header("安礼章福祸评估演示")
    
    sufu = get_sufu_core()
    
    # 测试行为
    actions = [
        "主动帮助同事解决问题",
        "积极参与公益活动",
        "与团队成员发生争执",
        "经常加班完成工作",
        "虚心接受他人批评",
        "背后说人是非"
    ]
    
    print("\n### 行为列表")
    for action in actions:
        print(f"  - {action}")
    
    result = sufu.assess_fortune(actions)
    
    print(f"\n[评估结果]")
    print(f"  福祸分数: {result['fortune_score']:.2f}")
    print(f"  总体评价: {result['assessment']}")
    print(f"  理由:")
    for reason in result['reasons']:
        print(f"    - {reason}")
    print(f"\n  经典引用: {result['quote']}")

def demo_general_decision():
    """演示通用decision"""
    print_header("五德synthesize_decision演示")
    
    sufu = get_sufu_core()
    
    situation = {
        "type": "strategy",
        "description": "考虑进入新市场",
        "options": ["进入", "观望", "放弃"],
        "constraints": ["预算有限", "经验不足"]
    }
    
    decision = sufu.make_decision(situation)
    
    print(f"\n[decision情境]")
    print(f"  类型: {situation['type']}")
    print(f"  描述: {situation['description']}")
    
    print(f"\n[素书decision]")
    print(f"  主导原则: {decision.principle.value}")
    print(f"  推理过程: {decision.reasoning}")
    print(f"  action建议: {decision.action}")
    print(f"  智慧来源: {decision.wisdom_source}")
    print(f"  平衡分数: {decision.balance_score:.2f}")
    
    if decision.risk_warning:
        print(f"\n[风险警示]")
        for warning in decision.risk_warning:
            print(f"  ⚠️ {warning}")

def demo_reasoning_integration():
    """演示推理链fusion"""
    print_header("推理链素书fusion演示")
    
    sufu = get_sufu_core()
    
    # 模拟推理链
    reasoning_chain = [
        {
            "step": 1,
            "content": "首先分析市场需求和竞争格局"
        },
        {
            "step": 2,
            "content": "评估自身能力和资源储备"
        },
        {
            "step": 3,
            "content": "制定市场进入strategy"
        },
        {
            "step": 4,
            "content": "分配资源执行计划"
        }
    ]
    
    result = sufu.integrate_with_reasoning(reasoning_chain)
    
    print(f"\n[推理链素书fusion]")
    print(f"  总体平衡分数: {result['overall_balance']:.2f}")
    print(f"  总风险预警数: {result['total_warnings']}")
    
    print(f"\n[各步骤素书增强]")
    for step in result["enhanced_chain"]:
        wisdom = step["sufu_wisdom"]
        print(f"\n  步骤 {step['step']}: {step['content']}")
        print(f"    原则: {wisdom['principle']}")
        print(f"    分数: {wisdom['balance_score']:.2f}")
        if wisdom['warnings']:
            print(f"    预警: {', '.join(wisdom['warnings'])}")

def main():
    """主函数"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "<素书>智慧演示 - Somn v1.0.0" + " " * 10 + "║")
    print("║" + " " * 8 + "黄石公·道,德,仁,义,礼五位一体" + " " * 8 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # 演示各项功能
    demo_five_principles()
    demo_talent_assessment()
    demo_cultivation()
    demo_risk_warning()
    demo_fortune_assessment()
    demo_general_decision()
    demo_reasoning_integration()
    
    print_header("演示完成")
    print("\n  <素书>原文精髓:")
    print("  '夫道,德,仁,义,礼五者,一体也.'")
    print("  '欲为人之本,不可无一焉.'")
    print("\n  更多内容请参考: file/系统文件/素书智慧融入报告.md")
    print()

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
