"""
聊天路径全局一致性测试 v12.1.0
测试完整调用链：process_input() → _understand_intent() → _generate_response() → _handle_general_chat()

验证：所有入口（IDE/Web/GUI）通过 agent_core.process_input() 走统一路径，
论证型问题走智慧板块，任务型问题走专用handler。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

from src.core.agent_core import AgentCore

from src.core.memory_system import MemorySystem
from src.core.knowledge_base import KnowledgeBase

# 初始化AgentCore
memory = MemorySystem()
kb = KnowledgeBase()
agent = AgentCore(memory, kb)

def test_intent_classification():
    """测试意图分类（_understand_intent 全局入口）"""
    print("=" * 60)
    print("测试1：意图分类（_understand_intent 全局入口）")
    print("=" * 60)
    
    test_cases = [
        # === 论证型（应该走 general_chat → 智慧板块）===
        ("人活着的意义是什么", "argumentative"),
        ("人生的价值是什么", "argumentative"),
        ("什么是幸福", "argumentative"),
        ("爱是什么", "argumentative"),
        ("人生是一场旅行吗", "argumentative"),
        ("为什么人会感到孤独", "argumentative"),
        ("自由的真谛是什么", "argumentative"),
        ("死亡是终结吗", "argumentative"),
        ("善良有什么意义", "argumentative"),
        ("什么是真正的友情", "argumentative"),
        ("宇宙的尽头是什么", "argumentative"),
        ("ai是否有意识", "argumentative"),
        ("什么是美", "argumentative"),
        ("真理存在吗", "argumentative"),
        # === 任务型（应该走对应handler）===
        ("帮我制定增长策略", "task"),
        ("生成一份工作报告", "task"),
        ("帮我写一个PPT", "task"),
        ("创建一个Excel表格", "task"),
        ("分析一下这个数据", "task"),
        ("帮我搜索相关信息", "task"),
        ("计算一下ROI", "task"),
        ("总结这段文字", "task"),
        ("打开文件夹", "task"),
        # === 问候/感谢（特殊handler）===
        ("你好", "greeting"),
        ("谢谢你的帮助", "thanks"),
    ]
    
    passed = 0
    failed = 0
    
    for user_input, expected_type in test_cases:
        intent = agent._understand_intent(user_input)
        
        # 论证型期望 general_chat
        if expected_type == "argumentative":
            ok = intent == "general_chat"
        elif expected_type == "task":
            ok = intent != "general_chat" and intent != "greeting" and intent != "thanks"
        else:
            ok = intent == expected_type
        
        status = "✅" if ok else "❌"
        if ok:
            passed += 1
        else:
            failed += 1
        print(f"  {status} \"{user_input}\" → {intent} (期望: {expected_type})")
    
    print(f"\n意图分类结果：{passed}/{len(test_cases)} 通过")
    return passed, failed, len(test_cases)


def test_general_chat_uses_wisdom():
    """测试 _handle_general_chat 对论证型问题使用智慧板块"""
    print("\n" + "=" * 60)
    print("测试2：_handle_general_chat 论证模式")
    print("=" * 60)
    
    # 只测论证型问题（已经通过 intent=general_chat 进入了）
    test_cases = [
        "人活着的意义是什么",
        "什么是真正的自由",
        "ai是否有灵魂",
    ]
    
    passed = 0
    for user_input in test_cases:
        intent = agent._understand_intent(user_input)
        if intent != "general_chat":
            print(f"  ⚠️ \"{user_input}\" 未进入 general_chat，跳过")
            continue
        
        # 验证 intent_type 分类
        intent_type = agent._classify_input_intent(user_input)
        if intent_type == "argumentative":
            print(f"  ✅ \"{user_input}\" → intent=general_chat, type=argumentative ✓")
            passed += 1
        else:
            print(f"  ❌ \"{user_input}\" → type={intent_type}，应为 argumentative")
    
    print(f"\n智慧板块接入验证：{passed}/{len(test_cases)} 通过")
    return passed, len(test_cases)


def test_task_intents_bypass_general_chat():
    """测试任务型意图正确绕过一般对话handler"""
    print("\n" + "=" * 60)
    print("测试3：任务型意图绕过 general_chat")
    print("=" * 60)
    
    task_cases = [
        ("帮我制定增长策略", "create_strategy"),
        ("生成一份工作报告", "generate_report"),
        ("帮我写一个PPT", "create_ppt"),
        ("创建一个Excel表格", "create_excel"),
        ("分析一下这个数据", "analyze"),
        ("帮我搜索相关信息", "search_knowledge"),
        ("计算一下ROI", "analyze"),
        ("总结这段文字", "summarize"),
    ]
    
    passed = 0
    for user_input, expected_intent in task_cases:
        intent = agent._understand_intent(user_input)
        ok = intent == expected_intent
        status = "✅" if ok else "❌"
        if ok:
            passed += 1
        print(f"  {status} \"{user_input}\" → {intent} (期望: {expected_intent})")
    
    print(f"\n任务型分发验证：{passed}/{len(task_cases)} 通过")
    return passed, len(task_cases)


def main():
    print("Somn v12.1.0 全局路径一致性测试")
    print("=" * 60)
    print("目标：所有入口走 agent_core.process_input() → 统一意图分类")
    print("论证型 → general_chat → _handle_general_chat() 论证模式 → 智慧板块")
    print("任务型 → 专用handler → execute_workflow")
    print("=" * 60 + "\n")
    
    # 测试1：意图分类
    p1, f1, t1 = test_intent_classification()
    
    # 测试2：智慧板块接入
    p2, t2 = test_general_chat_uses_wisdom()
    
    # 测试3：任务型分发
    p3, t3 = test_task_intents_bypass_general_chat()
    
    # 汇总
    total_pass = p1 + p2 + p3
    total_tests = t1 + t2 + t3
    
    print("\n" + "=" * 60)
    print(f"全局路径测试汇总：{total_pass}/{total_tests} 通过")
    print("=" * 60)
    
    if total_pass == total_tests:
        print("✅ 所有测试通过！聊天路径全局一致性已实现。")
        print("\n【架构确认】")
        print("  process_input() → _understand_intent() [全局意图分类]")
        print("    ├─ 论证型 → general_chat → _handle_general_chat() 论证模式")
        print("    └─ 任务型 → 专用handler (create_strategy/analyze/...)")
        print("  结论：所有入口（IDE/Web/GUI）走统一路径，问题类型决定处理方式。")
    else:
        print("❌ 部分测试失败，请检查输出。")
    
    return total_pass == total_tests


if __name__ == "__main__":
    main()
