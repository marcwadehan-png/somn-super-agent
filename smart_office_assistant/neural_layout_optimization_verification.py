"""
神经网络布局优化串联验证脚本

验证四个维度的优化串联:
1. 主线集成器 ↔ UnifiedOrchestrator
2. 自主层 ↔ 反馈层深度整合
3. 学派层输出 → 执行层优化
4. 跨模块洞察生成
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_orchestrator_bridge():
    """测试编排器桥梁"""
    print("=" * 60)
    print("测试 1: 主线集成器 ↔ UnifiedOrchestrator 桥梁")
    print("=" * 60)
    
    try:
        from src.neural_layout import get_orchestrator_bridge, Signal, SignalType
        
        bridge = get_orchestrator_bridge()
        status = bridge.get_bridge_status()
        
        print(f"✅ 桥梁模块加载成功")
        print(f"   初始化状态: {status['initialized']}")
        print(f"   编排器连接: {status['orchestrator_connected']}")
        print(f"   信号处理器: {len(status['signal_handlers'])} 个")
        
        # 测试信号处理
        test_signal = Signal(
            source_id="neuron_agent_core",
            signal_type=SignalType.DATA,
            data={"test": "data", "query": "测试查询"}
        )
        
        result = bridge.process_signal(test_signal)
        print(f"✅ 信号处理测试通过")
        print(f"   处理结果: {result.data.get('handled_by', 'unknown')}")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_autonomy_feedback_fusion():
    """测试自主-反馈融合"""
    print("\n" + "=" * 60)
    print("测试 2: 自主层 ↔ 反馈层深度整合")
    print("=" * 60)
    
    try:
        from src.neural_layout import get_autonomy_feedback_fusion_engine
        
        engine = get_autonomy_feedback_fusion_engine()
        
        print(f"✅ 融合引擎模块加载成功")
        
        # 测试融合洞察生成
        decision = {"action": "test_action", "params": {"key": "value"}}
        feedback = {
            "outcome": "success",
            "signals": ["high_adoption"],
            "validated": True
        }
        
        # 模拟融合（通过内部方法）
        fusion = engine._fuse_decision_feedback(decision, feedback)
        
        print(f"✅ 决策-反馈融合测试通过")
        print(f"   融合洞察: {fusion.insight[:30]}...")
        print(f"   置信度: {fusion.confidence:.2f}")
        print(f"   已验证: {fusion.validated}")
        
        # 测试统计
        stats = engine.get_fusion_statistics()
        print(f"✅ 融合统计功能正常")
        print(f"   总记录数: {stats['total']}")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_school_execution_optimizer():
    """测试学派执行优化"""
    print("\n" + "=" * 60)
    print("测试 3: 学派层输出 → 执行层优化")
    print("=" * 60)
    
    try:
        from src.neural_layout import (
            get_school_execution_optimizer,
            SchoolOutput, SchoolType
        )
        
        optimizer = get_school_execution_optimizer()
        
        print(f"✅ 学派执行优化器加载成功")
        
        # 创建测试学派输出
        school_outputs = [
            SchoolOutput(
                school=SchoolType.CONFUCIAN,
                recommendation="注重伦理和长期规划",
                confidence=0.85,
                action_items=[{"action": "制定道德准则"}, {"action": "建立长期目标"}]
            ),
            SchoolOutput(
                school=SchoolType.SUNZI,
                recommendation="战略规划和竞争分析",
                confidence=0.78,
                action_items=[{"action": "分析竞争对手"}, {"action": "制定战术"}]
            ),
            SchoolOutput(
                school=SchoolType.YANGMING,
                recommendation="知行合一，实践导向",
                confidence=0.72,
                action_items=[{"action": "立即行动"}, {"action": "反思调整"}]
            )
        ]
        
        # 执行优化
        plan = optimizer.optimize(school_outputs, {"context": "test"})
        
        print(f"✅ 学派输出优化测试通过")
        print(f"   计划ID: {plan.plan_id}")
        print(f"   执行策略: {plan.execution_strategy.value}")
        print(f"   步骤数: {len(plan.steps)}")
        print(f"   预期成功率: {plan.estimated_success_rate:.1%}")
        print(f"   风险等级: {plan.risk_assessment.get('highest_level', 'low')}")
        
        # 测试统计
        stats = optimizer.get_optimization_stats()
        print(f"✅ 优化统计功能正常")
        print(f"   总计划数: {stats['total_plans']}")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cross_module_insight_generator():
    """测试跨模块洞察生成"""
    print("\n" + "=" * 60)
    print("测试 4: 跨模块洞察生成")
    print("=" * 60)
    
    try:
        from src.neural_layout import (
            get_cross_module_insight_generator,
            ModuleSource, InsightType
        )
        
        generator = get_cross_module_insight_generator()
        
        print(f"✅ 跨模块洞察生成器加载成功")
        
        # 模拟模块数据
        generator.collect_module_data(
            ModuleSource.EVOLUTION,
            {"metrics": {"performance": 0.85, "stability": 0.92}},
            reliability=0.9
        )
        
        generator.collect_module_data(
            ModuleSource.GROWTH,
            {"metrics": {"performance": 0.78, "experiments": 5}},
            reliability=0.85
        )
        
        generator.collect_module_data(
            ModuleSource.LEARNING,
            {"statistics": {"q_value_updates": 10, "feedback_count": 50}},
            reliability=0.8
        )
        
        generator.collect_module_data(
            ModuleSource.WISDOM,
            {"recommendations": [{"adopted": True}, {"adopted": False}]},
            reliability=0.75
        )
        
        print(f"✅ 模块数据收集测试通过")
        
        # 生成洞察
        insights = generator.generate_insights()
        
        print(f"✅ 洞察生成测试通过")
        print(f"   生成洞察数: {len(insights)}")
        
        for insight in insights:
            print(f"   - {insight.title[:40]}... (置信度: {insight.confidence:.2f})")
        
        # 测试统计
        stats = generator.get_insight_statistics()
        print(f"✅ 洞察统计功能正常")
        print(f"   总洞察数: {stats['total']}")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integration():
    """测试整体集成"""
    print("\n" + "=" * 60)
    print("测试 5: 整体集成验证")
    print("=" * 60)
    
    try:
        from src.neural_layout import (
            get_neural_integration,
            get_orchestrator_bridge,
            get_autonomy_feedback_fusion_engine,
            get_school_execution_optimizer,
            get_cross_module_insight_generator
        )
        
        # 验证所有组件可访问
        components = {
            "神经集成": get_neural_integration(),
            "编排器桥梁": get_orchestrator_bridge(),
            "自主反馈融合": get_autonomy_feedback_fusion_engine(),
            "学派执行优化": get_school_execution_optimizer(),
            "跨模块洞察": get_cross_module_insight_generator()
        }
        
        print(f"✅ 所有组件可正常访问")
        for name, component in components.items():
            print(f"   - {name}: {type(component).__name__}")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主验证函数"""
    print("\n" + "=" * 60)
    print("神经网络布局优化串联验证")
    print("=" * 60)
    print(f"验证时间: {__import__('datetime').datetime.now().isoformat()}")
    print()
    
    results = {
        "编排器桥梁": test_orchestrator_bridge(),
        "自主反馈融合": test_autonomy_feedback_fusion(),
        "学派执行优化": test_school_execution_optimizer(),
        "跨模块洞察": test_cross_module_insight_generator(),
        "整体集成": test_integration()
    }
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("验证结果汇总")
    print("=" * 60)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status}: {name}")
    
    print()
    print(f"总计: {passed}/{total} 通过 ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 所有优化串联验证通过！")
        return 0
    else:
        print(f"\n⚠️ 有 {total - passed} 项验证未通过")
        return 1


if __name__ == "__main__":
    exit(main())
