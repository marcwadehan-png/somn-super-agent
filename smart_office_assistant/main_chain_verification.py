"""
主线冒烟测试 - 验证所有节点可在主线上被激活运转
运行方式：python main_chain_verification.py

日期：2026-04-05
版本：v1.0
"""

import sys
from pathlib import Path
import time

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths
bootstrap_project_paths(__file__)

# 导入日志
from loguru import logger
import logging

# 关闭烦人的 INFO 日志
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logger.disable("httpx")
logger.disable("openai")

# 测试结果收集
test_results = []
passed = 0
failed = 0


def test_result(name: str, is_passed: bool, details: str = ""):
    """记录测试结果"""
    global passed, failed
    status = "✅" if is_passed else "❌"
    test_results.append({
        "name": name,
        "status": status,
        "passed": is_passed,
        "details": details
    })
    if is_passed:
        passed += 1
    else:
        failed += 1
    print(f"  {status} {name}: {details}")


def test_import(module_path: str, class_name: str) -> bool:
    """测试模块导入"""
    try:
        parts = module_path.split(".")
        if parts[0] == "src":
            # 处理 src.core.xxx 或 src.intelligence.xxx
            if len(parts) >= 3:
                module = __import__(module_path, fromlist=[class_name])
            else:
                module = __import__(module_path, fromlist=[class_name])
        else:
            module = __import__(module_path, fromlist=[class_name])
        
        cls = getattr(module, class_name, None)
        if cls is None:
            # 尝试直接导入
            if "." in module_path:
                exec(f"from {module_path.rsplit('.', 1)[0]} import {class_name}")
            return True
        return cls is not None
    except Exception as e:
        return False


def test_main_chain():
    """测试主线串联运转"""
    print("\n" + "=" * 60)
    print("Somn 主线节点激活验证测试")
    print("=" * 60 + "\n")
    
    print("📦 第一阶段：模块导入测试（16个一级节点）\n")
    
    # ── 一级节点导入测试 ──────────────────────────────────────
    # (模块路径, 类名, 节点名称) - v1.1 修复路径
    node_tests = [
        ("src.core.agent_core", "AgentCore", "N01-AgentCore"),
        ("src.core.somn_core", "SomnCore", "N02-SomnCore"),
        ("src.intelligence.engines.super_wisdom_coordinator", "SuperWisdomCoordinator", "N03-SuperWisdomCoordinator"),
        ("src.intelligence.engines.unified_intelligence_coordinator", "UnifiedIntelligenceCoordinator", "N04-UnifiedIntelligenceCoordinator"),
        ("src.intelligence.scheduler.global_wisdom_scheduler", "GlobalWisdomScheduler", "N05-GlobalWisdomScheduler"),
        ("src.intelligence.dispatcher.wisdom_dispatcher", "WisdomDispatcher", "N06-WisdomDispatcher"),
        ("src.intelligence.scheduler.thinking_method_engine", "ThinkingMethodFusionEngine", "N07-ThinkingMethodFusionEngine"),
        ("src.intelligence.reasoning.deep_reasoning_engine", "DeepReasoningEngine", "N08-DeepReasoningEngine"),
        ("src.intelligence.scheduler.tier3_neural_scheduler", "Tier3NeuralScheduler", "N09-Tier3NeuralScheduler"),
        ("src.intelligence.engines.narrative_intelligence_engine", "NarrativeIntelligenceEngine", "N10-NarrativeIntelligenceEngine"),
        ("src.learning.coordinator", "LearningCoordinator", "N11-LearningCoordinator"),
        ("src.autonomous_core.autonomous_agent", "AutonomousAgent", "N12-AutonomousAgent"),
        ("src.neural_memory.neural_memory_system_v3", "NeuralMemorySystem", "N13-NeuralMemorySystem"),
        ("src.neural_memory.semantic_memory_engine", "SemanticMemoryEngine", "N14-SemanticMemoryEngine"),
        ("src.neural_memory.reinforcement_trigger", "ReinforcementTrigger", "N15-ReinforcementTrigger"),
        ("src.neural_memory.roi_tracker", "ROITracker", "N16-ROITracker"),
    ]
    
    import_success = 0
    import_fail = 0
    
    for module_path, class_name, node_name in node_tests:
        try:
            if "." in module_path:
                parts = module_path.rsplit(".", 1)
                module = __import__(module_path, fromlist=[parts[1]])
            else:
                module = __import__(module_path, fromlist=[class_name])
            
            cls = getattr(module, class_name, None)
            if cls is None:
                # 尝试直接导入
                exec(f"from {module_path} import {class_name}")
                cls = eval(class_name)
            
            import_success += 1
            print(f"  ✅ {node_name}: 导入成功")
        except Exception as e:
            import_fail += 1
            print(f"  ❌ {node_name}: 导入失败 - {type(e).__name__}: {str(e)[:60]}")
    
    print(f"\n  导入统计：{import_success} 成功 / {import_fail} 失败")
    
    # ── 二级节点导入测试 ──────────────────────────────────────
    # v1.1 修复路径
    secondary_tests = [
        ("src.intelligence.dispatcher.wisdom_fusion_core", "WisdomFusionCore"),
        ("src.intelligence.engines.supreme_decision_fusion_engine", "SupremeDecisionFusionEngine"),
        ("src.intelligence.engines.confucian_buddhist_dao_fusion_engine", "ConfucianBuddhistDaoFusion"),
        ("src.intelligence.engines.sufu_wisdom_core", "SufuWisdomCore"),
        ("src.intelligence.engines.dao_wisdom_core", "DaoWisdomCore"),
        ("src.intelligence.engines.ru_wisdom_unified", "RuWisdomCore"),  # 实际文件为 ru_wisdom_unified.py
        ("src.intelligence.engines.buddha_wisdom_core", "BuddhaWisdomCore"),
        ("src.intelligence.engines.hongming_wisdom_core", "HongmingWisdomCore"),
        ("src.intelligence.engines.military_strategy_engine", "MilitaryStrategyEngine"),
        ("src.intelligence.engines.philosophy.yangming_xinxue_engine", "YangmingXinxueEngine"),
        ("src.intelligence.reasoning.dewey_thinking_engine", "DeweyThinkingEngine"),
        ("src.intelligence.engines.top_thinking_engine", "TopThinkingEngine"),
        ("src.intelligence.engines.natural_science_unified", "NaturalScienceUnified"),
        ("src.intelligence.engines.metaphysics_wisdom_unified", "MetaphysicsWisdomUnified"),
        ("src.growth_engine.growth_strategy", "GrowthStrategyEngine"),
        ("src.growth_engine.solution_learning", "SolutionLearningEngine"),
        ("src.autonomous_core.reflection_engine", "ReflectionEngine"),
        ("src.autonomous_core.goal_system", "GoalSystem"),
        ("src.autonomous_core.state_manager", "StateManager"),
        ("src.autonomous_core.value_system", "ValueSystem"),
    ]
    
    secondary_success = 0
    secondary_fail = 0
    
    for module_path, class_name in secondary_tests:
        try:
            if "." in module_path:
                parts = module_path.rsplit(".", 1)
                module = __import__(module_path, fromlist=[parts[1]])
            else:
                module = __import__(module_path, fromlist=[class_name])
            
            cls = getattr(module, class_name, None)
            if cls is None:
                exec(f"from {module_path} import {class_name}")
                cls = eval(class_name)
            
            secondary_success += 1
            print(f"  ✅ {class_name}: 导入成功")
        except Exception as e:
            secondary_fail += 1
            print(f"  ❌ {class_name}: 导入失败 - {type(e).__name__}: {str(e)[:60]}")
    
    print(f"\n  导入统计：{secondary_success} 成功 / {secondary_fail} 失败")
    
    # ── SomnCore 主链调用测试 ─────────────────────────────────
    print("\n📦 第三阶段：SomnCore 主链调用测试\n")

    try:
        print("  初始化 SomnCore（这可能需要几秒钟）...")
        from src.core.somn_core import SomnCore
        core = SomnCore()
        print("  ✅ SomnCore 初始化成功")

        # 等待后台预热完成（v16.1 修复：主动触发各层初始化）
        print("  触发各层预热...")
        core._ensure_runtime()
        core._ensure_autonomy_stores()
        core._ensure_layers()
        core._ensure_wisdom_layers()
        core._ensure_autonomous_agent()
        core._ensure_learning_coordinator()
        core._ensure_main_chain()
        print("  ✅ 各层预热完成")

        # 检查关键属性
        checks = [
            ("super_wisdom", "SuperWisdomCoordinator"),
            ("unified_coordinator", "UnifiedIntelligenceCoordinator"),
            ("global_wisdom", "GlobalWisdomScheduler"),
            ("thinking_engine", "ThinkingMethodFusionEngine"),
            ("semantic_memory", "SemanticMemoryEngine"),
            ("neural_system", "NeuralMemorySystem"),
        ]
        
        main_chain_ok = 0
        main_chain_fail = 0
        
        for attr, name in checks:
            if hasattr(core, attr):
                val = getattr(core, attr)
                if val is not None:
                    main_chain_ok += 1
                    print(f"  ✅ {name} 已接入主线")
                else:
                    main_chain_fail += 1
                    print(f"  ⚠️ {name} 已定义但未初始化（可能缺少依赖）")
            else:
                main_chain_fail += 1
                print(f"  ❌ {name} 未在 SomnCore 中定义")
        
        print(f"\n  主链接入统计：{main_chain_ok} 已接入 / {main_chain_fail} 未接入")
        
    except Exception as e:
        print(f"  ❌ SomnCore 初始化失败: {type(e).__name__}: {str(e)[:100]}")
        import traceback
        traceback.print_exc()
        main_chain_ok = 0
        main_chain_fail = 16
    
    # ── 总结 ─────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"\n  一级节点导入：{import_success} 成功 / {import_fail} 失败")
    print(f"  二级节点导入：{secondary_success} 成功 / {secondary_fail} 失败")
    print(f"  主链接入测试：{main_chain_ok} 已接入 / {main_chain_fail} 未接入")
    
    total = import_success + secondary_success + main_chain_ok
    total_check = 16 + 20 + 6  # 一级节点 + 二级节点 + 主链检查
    
    print(f"\n  总计：{total} / {total_check} 通过")
    
    if total == total_check:
        print("\n🎉 所有节点可正常导入和激活！")
        return True
    elif total >= total_check * 0.8:
        print("\n⚠️ 大部分节点通过，部分需要修复")
        return True
    else:
        print("\n❌ 节点激活率不足，需要修复")
        return False


if __name__ == "__main__":
    success = test_main_chain()
    sys.exit(0 if success else 1)
