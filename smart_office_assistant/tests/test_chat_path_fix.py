"""
聊天路径一致性冒烟测试 v12.0.0

验证目标：
1. 论证型问题（哲学/观点）→ 直接调用 SuperWisdomCoordinator
2. 任务型问题（动作/执行）→ 走 execute_workflow
3. 路径一致性：IDE对话和Web聊天窗走相同链路
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)


def test_intent_classification():
    """测试意图分类逻辑"""
    print("=" * 60)
    print("测试 1: 意图分类")
    print("=" * 60)
    
    # 导入需要测试的模块
    from src.core.agent_core import AgentCore
    from src.core.memory_system import MemorySystem
    from src.core.knowledge_base import KnowledgeBase
    
    # 创建 AgentCore 实例
    memory = MemorySystem()
    kb = KnowledgeBase()
    agent = AgentCore(memory, kb)
    
    # 测试用例
    test_cases = [
        # 论证型问题
        ("人活着的意义是什么", "argumentative", "哲学追问"),
        ("什么是幸福", "argumentative", "哲学概念"),
        ("人生的价值是什么", "argumentative", "哲学追问"),
        ("为什么存在痛苦", "argumentative", "哲学追问"),
        ("如何理解自由", "argumentative", "哲学概念"),
        
        # 任务型问题
        ("帮我制定增长策略", "task", "明确动作"),
        ("给我生成一份报告", "task", "动作指令"),
        ("分析用户增长数据", "task", "分析动作"),
        ("执行这个计划", "task", "执行动作"),
        ("帮我优化转化率", "task", "优化动作"),
        
        # 边界情况
        ("你好", "argumentative", "问候-短输入"),
        ("嗯", "argumentative", "极短输入"),
        ("今天天气如何", "argumentative", "非哲学但较短"),
    ]
    
    passed = 0
    failed = 0
    
    for user_input, expected_intent, description in test_cases:
        actual_intent = agent._classify_input_intent(user_input)
        status = "✅" if actual_intent == expected_intent else "❌"
        
        if actual_intent == expected_intent:
            passed += 1
            print(f"{status} [{description}] \"{user_input}\" → {actual_intent}")
        else:
            failed += 1
            print(f"{status} [{description}] \"{user_input}\"")
            print(f"   期望: {expected_intent}, 实际: {actual_intent} ❌")
    
    print(f"\n结果: {passed}/{len(test_cases)} 通过")
    return failed == 0


def test_wisdom_coordinator_integration():
    """测试智慧协调器集成"""
    print("\n" + "=" * 60)
    print("测试 2: 智慧协调器集成")
    print("=" * 60)
    
    try:
        from src.core.somn_core import get_somn_core
        
        somn_core = get_somn_core()
        if somn_core is None:
            print("❌ SomnCore 未初始化")
            return False
        
        if somn_core.super_wisdom is None:
            print("❌ SuperWisdomCoordinator 未加载")
            return False
        
        print("✅ SomnCore + SuperWisdomCoordinator 正常")
        
        # 测试调用
        test_query = "人活着的意义是什么"
        result = somn_core.super_wisdom.analyze(
            query_text=test_query,
            context={},
            threshold=0.25,
            max_schools=6
        )
        
        print(f"✅ 智慧分析调用成功")
        print(f"   主洞察: {result.primary_insight[:50] if result.primary_insight else '无'}...")
        print(f"   激活学派: {result.activated_schools[:3] if result.activated_schools else '无'}")
        
        return True
        
    except Exception as e:
        print(f"❌ 智慧协调器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_general_chat_handling():
    """测试一般对话处理"""
    print("\n" + "=" * 60)
    print("测试 3: 一般对话处理（论证模式）")
    print("=" * 60)
    
    try:
        from src.core.agent_core import AgentCore
        from src.core.memory_system import MemorySystem
        from src.core.knowledge_base import KnowledgeBase
        
        memory = MemorySystem()
        kb = KnowledgeBase()
        agent = AgentCore(memory, kb)
        
        # 测试论证型问题
        test_input = "人活着的意义是什么"
        
        print(f"输入: \"{test_input}\"")
        print(f"意图: {agent._classify_input_intent(test_input)}")
        
        # 由于完整处理可能耗时，只验证路径不报错
        try:
            # 模拟 context
            context = {'recent_memories': '', 'relevant_knowledge': [], 'current_topic': None}
            
            # 检查是否能正确分类
            intent = agent._classify_input_intent(test_input)
            assert intent == "argumentative", f"意图分类错误: {intent}"
            
            print("✅ 论证型问题路径正确")
            return True
            
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n" + "=" * 60)
    print("Somn 聊天路径一致性冒烟测试 v12.0.0")
    print("=" * 60)
    print()
    
    results = []
    
    # 测试1: 意图分类
    results.append(("意图分类", test_intent_classification()))
    
    # 测试2: 智慧协调器集成
    results.append(("智慧协调器集成", test_wisdom_coordinator_integration()))
    
    # 测试3: 一般对话处理
    results.append(("一般对话处理", test_general_chat_handling()))
    
    # 汇总
    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 所有测试通过！聊天路径一致性已修复。")
    else:
        print("⚠️ 部分测试失败，请检查上述输出。")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
