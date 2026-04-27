"""
智能学习系统演示
展示基于逻辑判断、择优决策、持续提炼的自主学习能力

演示内容:
1. 设计原则学习 - 评估、判断、择优
2. 配色方案学习 - 和谐度计算、质量评估
3. 排版模式学习 - 相关性评估、效果验证
4. 持续进化 - 反馈学习、知识优化
5. 冲突解决 - 在冲突中择优选择
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)


from src.learning.smart_learning_engine import (
    SmartLearningEngine,
    create_knowledge_item
)
from src.learning.ppt_style_learner import (
    PPTStyleLearner,
    create_principle,
    create_color_scheme,
    create_layout_pattern
)
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def print_section(title: str):
    """打印分节标题"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def demo_intelligent_decision_making():
    """
    演示1: 智能决策制定
    展示逻辑判断和择优决策能力
    """
    print_section("🧠 演示1: 智能决策制定")
    
    # 初始化学习引擎
    engine = SmartLearningEngine()
    
    # 场景: 学习新的设计原则
    print("📚 场景: 学习新的设计原则")
    print("-" * 40)
    
    # 创建多个来源的设计原则
    principle_1 = create_knowledge_item(
        source="OfficePLUS",
        content={
            "name": "对齐与秩序",
            "description": "所有元素应该对齐，保持视觉秩序",
            "category": "视觉"
        },
        quality=5,  # 高质量
        relevance=5,  # 高相关性
        confidence=0.9,
        evidence=["广泛应用于专业PPT", "被微软官方推荐"],
        tags=["alignment", "visual"]
    )
    
    principle_2 = create_knowledge_item(
        source="新手博客",
        content={
            "name": "自由排版",
            "description": "元素可以随意放置，追求自由创意",
            "category": "视觉"
        },
        quality=2,  # 低质量
        relevance=3,  # 中等相关性
        confidence=0.5,
        evidence=["个人观点", "缺乏验证"],
        tags=["free", "creative"]
    )
    
    principle_3 = create_knowledge_item(
        source="Beautiful.ai",
        content={
            "name": "智能间距",
            "description": "按黄金比例(1.618)自动计算元素间距",
            "category": "视觉"
        },
        quality=5,  # 高质量
        relevance=5,  # 高相关性
        confidence=0.95,
        evidence=["基于设计研究", "被AI系统采用", "用户反馈良好"],
        tags=["spacing", "golden_ratio"]
    )
    
    # 评估和学习
    for i, principle in enumerate([principle_1, principle_2, principle_3], 1):
        print(f"\n📖 知识项 {i}: {principle.source}")
        print(f"   - 名称: {principle.content['name']}")
        print(f"   - 质量: {principle.quality.value}级 ({principle.quality.name})")
        print(f"   - 相关性: {principle.relevance.value}级 ({principle.relevance.name})")
        print(f"   - 置信度: {principle.confidence:.2%}")
        
        decision = engine.make_decision(principle, "design_principles")
        print(f"   ✅ 决策: {decision.decision.value.upper()}")
        print(f"   📝 理由: {decision.reason}")
        print(f"   🎯 优先级: {decision.priority:.2f}")
    
    print("\n💡 智能决策总结:")
    print("   - ✓ 接受高质量、高相关性、高置信度的知识")
    print("   - ✗ 拒绝低质量、低相关性的知识")
    print("   - 🤔 对低置信度知识延迟决策")
    print("   - ⚖️ 综合质量、相关性、置信度做出判断")


def demo_conflict_resolution():
    """
    演示2: 冲突解决与择优
    展示在冲突知识中择优选择的能力
    """
    print_section("⚖️ 演示2: 冲突解决与择优")
    
    engine = SmartLearningEngine()
    
    print("🔥 场景: 检测到设计原则冲突")
    print("-" * 40)
    
    # 先学习一个原则
    principle_a = create_knowledge_item(
        source="平台A",
        content={
            "name": "最多使用2种字体",
            "description": "PPT中最多使用2种字体，保持一致性",
            "category": "视觉",
            "rule": "max_fonts=2"
        },
        quality=4,
        relevance=5,
        confidence=0.8,
        tags=["font", "consistency"]
    )
    
    decision_a = engine.make_decision(principle_a, "design_principles")
    engine.learn(principle_a, "design_principles")
    print(f"\n✅ 已学习: {principle_a.source} - {principle_a.content['name']}")
    
    # 学习冲突的原则
    principle_b = create_knowledge_item(
        source="平台B",
        content={
            "name": "最多使用3种字体",
            "description": "PPT中最多使用3种字体，增加变化性",
            "category": "视觉",
            "rule": "max_fonts=3"
        },
        quality=5,  # 更高质量
        relevance=5,
        confidence=0.9,  # 更高置信度
        tags=["font", "variety"]
    )
    
    print(f"\n⚠️  发现冲突: {principle_b.source} - {principle_b.content['name']}")
    print(f"   冲突规则: {principle_a.content['rule']} vs {principle_b.content['rule']}")
    
    decision_b = engine.make_decision(principle_b, "design_principles")
    
    print(f"\n🔍 择优决策:")
    print(f"   平台A: 质量={principle_a.quality.value}, 置信度={principle_a.confidence:.2%}")
    print(f"   平台B: 质量={principle_b.quality.value}, 置信度={principle_b.confidence:.2%}")
    print(f"   ✅ 最终选择: {decision_b.decision.value}")
    print(f"   📝 理由: {decision_b.reason}")


def demo_color_scheme_learning():
    """
    演示3: 配色方案智能学习
    展示和谐度计算和质量评估
    """
    print_section("🎨 演示3: 配色方案智能学习")
    
    engine = SmartLearningEngine()
    learner = PPTStyleLearner(engine)
    
    print("🎨 场景: 学习新的配色方案")
    print("-" * 40)
    
    # 创建多个配色方案
    schemes = [
        create_color_scheme(
            name="经典蓝灰",
            primary="#1F4E79",
            secondary="#5B9BD5",
            accent="#FFC000",
            background="#FFFFFF",
            text="#000000",
            source="OfficePLUS"
        ),
        create_color_scheme(
            name="马卡龙",
            primary="#FF6B9D",
            secondary="#C44DFF",
            accent="#FFD93D",
            background="#FFF5F5",
            text="#333333",
            source="SlidesCarnival"
        ),
        create_color_scheme(
            name="低对比度",
            primary="#EEEEEE",
            secondary="#F0F0F0",
            accent="#F5F5F5",
            background="#FAFAFA",
            text="#CCCCCC",
            source="未知来源"
        )
    ]
    
    for scheme in schemes:
        print(f"\n📦 配色方案: {scheme.name}")
        print(f"   来源: {scheme.source}")
        
        success = learner.learn_color_scheme(scheme)
        
        if success:
            print(f"   ✅ 学习成功")
            print(f"   📊 和谐度: {scheme.harmony_score:.2f}")
        else:
            print(f"   ❌ 学习失败 (质量不足)")


def demo_continuous_evolution():
    """
    演示4: 持续进化与反馈学习
    展示从反馈中学习和优化
    """
    print_section("🔄 演示4: 持续进化与反馈学习")
    
    engine = SmartLearningEngine()
    learner = PPTStyleLearner(engine)
    
    print("📈 场景: 基于反馈持续学习和优化")
    print("-" * 40)
    
    # 学习设计原则
    principle = create_principle(
        name="少即是多",
        description="PPT内容应该简洁，避免信息过载",
        source="优品PPT",
        category="内容",
        quality=5
    )
    
    print(f"\n📚 学习原则: {principle.name}")
    learner.learn_design_principle(principle)
    
    # 模拟多次应用和反馈
    print(f"\n🔄 模拟应用和反馈:")
    for i in range(1, 6):
        print(f"\n第 {i} 次应用:")
        
        # 假设前4次有效，第5次无效
        is_effective = i <= 4
        feedback = "用户反馈良好" if is_effective else "用户反馈复杂"
        
        learner.record_feedback(
            knowledge_type="principle",
            knowledge_name=principle.name,
            is_effective=is_effective,
            feedback=feedback
        )
        
        print(f"   效果: {'✅ 有效' if is_effective else '❌ 无效'}")
        print(f"   反馈: {feedback}")
        print(f"   成功率: {principle.success_rate:.2%}")
        print(f"   应用次数: {principle.application_count}")
    
    print(f"\n💡 持续进化总结:")
    print(f"   - ✓ 从成功案例中强化学习")
    print(f"   - ✓ 从失败案例中调整策略")
    print(f"   - ✓ 成功率动态更新: {principle.success_rate:.2%}")
    print(f"   - ✓ 支持持续优化和改进")


def demo_knowledge_optimization():
    """
    演示5: 知识库优化
    展示基于效果反馈的知识库优化
    """
    print_section("🧹 演示5: 知识库优化")
    
    engine = SmartLearningEngine()
    learner = PPTStyleLearner(engine)
    
    print("🗂️  场景: 基于效果反馈优化知识库")
    print("-" * 40)
    
    # 学习多个原则（设置不同的成功率）
    principles = [
        create_principle("原则A", "描述A", "平台A", "视觉", 5),
        create_principle("原则B", "描述B", "平台B", "内容", 4),
        create_principle("原则C", "描述C", "平台C", "动画", 3),
    ]
    
    for principle in principles:
        learner.learn_design_principle(principle)
        print(f"\n✅ 学习: {principle.name}")
    
    # 模拟应用和反馈
    print(f"\n🔄 模拟应用和反馈:")
    
    # 原则A: 高成功率
    for i in range(10):
        learner.record_feedback("principle", "原则A", is_effective=(i < 9))
    
    # 原则B: 中等成功率
    for i in range(8):
        learner.record_feedback("principle", "原则B", is_effective=(i < 6))
    
    # 原则C: 低成功率
    for i in range(6):
        learner.record_feedback("principle", "原则C", is_effective=(i < 2))
    
    print(f"\n📊 优化前统计:")
    for principle in learner.design_principles:
        print(f"   - {principle.name}: "
              f"应用{principle.application_count}次, "
              f"成功率{principle.success_rate:.2%}")
    
    # 优化知识库
    print(f"\n🧹 执行优化...")
    learner.optimize_knowledge_base()
    
    print(f"\n✅ 优化后统计:")
    for principle in learner.design_principles:
        print(f"   - {principle.name}: "
              f"应用{principle.application_count}次, "
              f"成功率{principle.success_rate:.2%}")
    
    print(f"\n💡 优化总结:")
    print(f"   - ✓ 移除低效知识（成功率<30%且应用次数>=5）")
    print(f"   - ✓ 保留高效知识")
    print(f"   - ✓ 提升知识库质量")


def demo_learning_summary():
    """
    演示6: 学习总结和导出
    """
    print_section("📊 演示6: 学习总结和导出")
    
    engine = SmartLearningEngine()
    learner = PPTStyleLearner(engine)
    
    # 学习一些知识
    principles = [
        create_principle("对齐原则", "元素对齐保持秩序", "OfficePLUS", "视觉", 5),
        create_principle("对比原则", "增强对比突出重点", "Canva", "视觉", 4),
    ]
    
    for principle in principles:
        learner.learn_design_principle(principle)
    
    schemes = [
        create_color_scheme("蓝灰", "#1F4E79", "#5B9BD5", "#FFC000",
                           "#FFFFFF", "#000000", "OfficePLUS")
    ]
    
    for scheme in schemes:
        learner.learn_color_scheme(scheme)
    
    # 获取学习总结
    summary = learner.get_learning_summary()
    
    print("📊 学习总结:")
    print("-" * 40)
    print(f"\n学习统计:")
    print(f"  - 设计原则: {summary['knowledge_counts']['design_principles']}")
    print(f"  - 配色方案: {summary['knowledge_counts']['color_schemes']}")
    print(f"  - 排版模式: {summary['knowledge_counts']['layout_patterns']}")
    print(f"\n决策统计:")
    stats = summary['learning_stats']
    print(f"  - 总决策数: {stats.get('total_decisions_made', 0)}")
    print(f"  - 平均成功率: {stats.get('avg_success_rate', 0):.2%}")
    
    # 导出知识库
    export_path = os.path.join(project_root, "data", "learning", "knowledge_base_export.json")
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    learner.export_knowledge_base(export_path)
    
    print(f"\n✅ 知识库已导出至: {export_path}")


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("  智能学习系统演示")
    print("  基于逻辑判断、择优决策、持续提炼的自主学习")
    print("=" * 80)
    
    try:
        # 演示1: 智能决策制定
        demo_intelligent_decision_making()
        
        # 演示2: 冲突解决与择优
        demo_conflict_resolution()
        
        # 演示3: 配色方案智能学习
        demo_color_scheme_learning()
        
        # 演示4: 持续进化与反馈学习
        demo_continuous_evolution()
        
        # 演示5: 知识库优化
        demo_knowledge_optimization()
        
        # 演示6: 学习总结和导出
        demo_learning_summary()
        
        print("\n" + "=" * 80)
        print("  ✅ 所有演示完成")
        print("=" * 80)
        
        print("\n🎯 核心特性总结:")
        print("  1. 智能评估 - 自动评估知识的相关性、质量、置信度")
        print("  2. 逻辑判断 - 基于多因素做出学习决策")
        print("  3. 择优决策 - 在多个方案中选择最优")
        print("  4. 持续进化 - 从反馈中学习和优化")
        print("  5. 冲突解决 - 在冲突知识中择优选择")
        print("  6. 知识优化 - 基于效果反馈优化知识库")
        
    except Exception as e:
        logger.error(f"演示失败: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
