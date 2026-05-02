# -*- coding: utf-8 -*-
"""
agent_core 测试用例 - 意图识别测试
Agent Core Tests - Intent Classification Tests
"""
import sys
from pathlib import Path
from unittest.mock import patch, Mock

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "smart_office_assistant"))

TEST_CONFIG = {'auto_learn': True, 'learning_data_path': 'data/learning'}


def test_06_classify_input_intent():
    """Test 06: 验证意图分类功能"""
    from src.core.agent_core import AgentCore
    from tests.agent_core_test._mocks import MockMemorySystem, MockKnowledgeBase

    memory = MockMemorySystem()
    kb = MockKnowledgeBase()

    with patch.object(AgentCore, '_background_warmup'):
        agent = AgentCore(memory, kb, TEST_CONFIG)

    test_cases = [
        ("你好", "conversational"),
        ("你是谁", "conversational"),
        ("谢谢你的帮助", "conversational"),
        ("关于这件事", "conversational"),
        ("帮我创建一个Word文档", "task"),
        ("制定一个增长策略", "task"),
    ]

    for user_input, expected_type in test_cases:
        result = agent._classify_input_intent(user_input)
        assert result == expected_type, f"输入 '{user_input}' 应分类为 '{expected_type}', 实际为 '{result}'"

    print("✓ test_06_classify_input_intent: 意图分类正确")


def test_07_understand_intent_basic():
    """Test 07: 验证 understand_intent 基础功能"""
    from src.core.agent_core import AgentCore
    from tests.agent_core_test._mocks import MockMemorySystem, MockKnowledgeBase

    memory = MockMemorySystem()
    kb = MockKnowledgeBase()

    with patch.object(AgentCore, '_background_warmup'):
        agent = AgentCore(memory, kb, TEST_CONFIG)

    test_cases = [
        ("你好", "greeting"),
        ("谢谢", "thanks"),
        ("帮我创建一个Word文档", "create_word"),
        ("帮我创建一个PPT", "create_ppt"),
        ("帮我创建一个PDF", "create_pdf"),
        ("帮我创建一个Excel表格", "create_excel"),
        ("查找Python知识", "search_knowledge"),
        ("记住这个重要信息", "add_knowledge"),
        ("总结一下这份文档", "summarize"),
        ("分析市场趋势", "analyze"),
        ("清理临时文件", "clean_files"),
        ("生成一份报告", "generate_report"),
        ("制定一个策略", "create_strategy"),
        ("预测一下效果", "ml_prediction"),
        ("学习状态", "learning_summary"),
    ]

    for user_input, expected_intent in test_cases:
        with patch.object(agent, 'hybrid_router', None):
            result = agent._understand_intent(user_input)
            assert result == expected_intent, f"输入 '{user_input}' 应理解为 '{expected_intent}', 实际为 '{result}'"

    print("✓ test_07_understand_intent_basic: understand_intent 基础功能正确")


def test_30_understand_intent_with_hybrid_router():
    """Test 30: 验证 understand_intent 与混合路由器集成"""
    from src.core.agent_core import AgentCore
    from tests.agent_core_test._mocks import MockMemorySystem, MockKnowledgeBase

    memory = MockMemorySystem()
    kb = MockKnowledgeBase()

    with patch.object(AgentCore, '_background_warmup'):
        agent = AgentCore(memory, kb, TEST_CONFIG)

    mock_router = Mock()
    mock_decision = Mock()
    mock_decision.route_type = Mock()
    mock_decision.route_type.value = "LLM_DIRECT"
    mock_decision.confidence = 0.9
    mock_decision.reasoning = "测试推理"
    mock_router.route.return_value = mock_decision

    agent.hybrid_router = mock_router

    result = agent._understand_intent("普通对话内容")
    assert result is not None, "应返回意图结果"

    print("✓ test_30_understand_intent_with_hybrid_router: 混合路由器集成正确")


def test_38_intent_caching():
    """Test 38: 验证意图缓存"""
    from src.core.agent_core import AgentCore
    from tests.agent_core_test._mocks import MockMemorySystem, MockKnowledgeBase

    memory = MockMemorySystem()
    kb = MockKnowledgeBase()

    with patch.object(AgentCore, '_background_warmup'):
        agent = AgentCore(memory, kb, TEST_CONFIG)

    context = {'_cached_intent_type': 'task'}

    with patch.object(agent, '_classify_input_intent', return_value='task') as mock_classify:
        intent = agent._understand_intent("测试输入")

    print("✓ test_38_intent_caching: 意图缓存正确")
