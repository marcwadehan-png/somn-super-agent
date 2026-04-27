# -*- coding: utf-8 -*-
"""
agent_core 测试用例 - Handler 测试
Agent Core Tests - Handler Tests
"""
import sys
from pathlib import Path
from unittest.mock import patch, Mock

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "smart_office_assistant"))

TEST_CONFIG = {'auto_learn': True, 'learning_data_path': 'data/learning'}


def _create_agent():
    """创建测试用 Agent 实例"""
    from src.core.agent_core import AgentCore
    from tests.agent_core_test._mocks import MockMemorySystem, MockKnowledgeBase

    memory = MockMemorySystem()
    kb = MockKnowledgeBase()
    with patch.object(AgentCore, '_background_warmup'):
        agent = AgentCore(memory, kb, TEST_CONFIG)
    return agent


def test_08_gather_context():
    """Test 08: 验证上下文收集"""
    from tests.agent_core_test._mocks import MockMemorySystem, MockKnowledgeBase

    memory = MockMemorySystem()
    kb = MockKnowledgeBase()
    memory.add_memory("用户问了关于Python的问题", memory_type="short_term")
    memory.add_memory("用户想要学习AI", memory_type="short_term")
    kb.add_knowledge("Python基础", "Python是一种编程语言", "技术")
    kb.add_knowledge("AI概述", "人工智能让机器具有智能", "技术")

    agent = _create_agent()
    context = agent._gather_context("搜索Python知识", "search_knowledge")

    assert 'recent_memories' in context
    assert 'relevant_knowledge' in context
    assert 'session_info' in context
    assert isinstance(context['relevant_knowledge'], list)

    print("✓ test_08_gather_context: 上下文收集正确")


def test_09_handle_create_word():
    """Test 09: 验证创建 Word 文档处理"""
    agent = _create_agent()
    response = agent._handle_create_word("帮我创建一个关于项目X的Word文档", {})

    assert response is not None
    assert hasattr(response, 'content')
    assert response.content is not None
    assert "Word" in response.content
    assert response.action == "prepare_word_template"

    print("✓ test_09_handle_create_word: Word 文档处理正确")


def test_10_handle_create_ppt():
    """Test 10: 验证创建 PPT 处理"""
    agent = _create_agent()
    response = agent._handle_create_ppt("帮我创建一个营销PPT", {})

    assert response.content is not None
    assert "PPT" in response.content
    assert response.action == "prepare_ppt_template"

    print("✓ test_10_handle_create_ppt: PPT 处理正确")


def test_11_handle_search_knowledge():
    """Test 11: 验证知识搜索处理"""
    from tests.agent_core_test._mocks import MockKnowledgeBase

    kb = MockKnowledgeBase()
    kb.add_knowledge("Python教程", "Python是一种高级编程语言", "技术")
    kb.add_knowledge("Java教程", "Java是一种面向对象语言", "技术")

    agent = _create_agent()
    agent.kb = kb

    response = agent._handle_search_knowledge("搜索Python", {})

    assert response.content is not None
    assert "Python" in response.content

    print("✓ test_11_handle_search_knowledge: 知识搜索正确")


def test_12_handle_add_knowledge():
    """Test 12: 验证添加知识处理"""
    agent = _create_agent()
    response = agent._handle_add_knowledge("记住这个重要信息", {})

    assert response.content is not None
    assert "知识库" in response.content

    print("✓ test_12_handle_add_knowledge: 添加知识处理正确")


def test_13_handle_summarize():
    """Test 13: 验证总结处理"""
    agent = _create_agent()
    response = agent._handle_summarize("总结一下这份文档", {})

    assert response.content is not None
    assert "总结" in response.content
    assert response.action == "prepare_summarize"

    print("✓ test_13_handle_summarize: 总结处理正确")


def test_14_handle_analyze():
    """Test 14: 验证分析处理"""
    agent = _create_agent()
    response = agent._handle_analyze("分析市场趋势", {})

    assert response.content is not None
    assert "不可用" in response.content or "检查" in response.content

    print("✓ test_14_handle_analyze: 分析处理正确")


def test_15_handle_greeting():
    """Test 15: 验证问候处理"""
    agent = _create_agent()
    response = agent._handle_greeting("你好", {})

    assert response.content is not None
    assert len(response.content) > 0

    print("✓ test_15_handle_greeting: 问候处理正确")


def test_16_handle_thanks():
    """Test 16: 验证感谢处理"""
    agent = _create_agent()
    response = agent._handle_thanks("谢谢你的帮助", {})

    assert response.content is not None
    assert len(response.content) > 0

    print("✓ test_16_handle_thanks: 感谢处理正确")


def test_17_handle_general_chat():
    """Test 17: 验证一般对话处理"""
    agent = _create_agent()

    response = agent._handle_general_chat("你好", {})
    assert response.content is not None

    response2 = agent._handle_general_chat("分析市场竞争格局", {})
    assert response2.content is not None

    print("✓ test_17_handle_general_chat: 一般对话处理正确")


def test_18_handle_conversational():
    """Test 18: 验证对话型输入处理"""
    agent = _create_agent()

    response = agent._handle_conversational("介绍一下你自己", {})
    assert response.content is not None
    assert "Somn" in response.content

    response2 = agent._handle_conversational("今天天气不错", {})
    assert response2.content is not None

    print("✓ test_18_handle_conversational: 对话型输入处理正确")


def test_33_handle_learning_summary():
    """Test 33: 验证学习摘要处理"""
    agent = _create_agent()
    response = agent._handle_learning_summary("学习状态", {})

    assert response.content is not None
    assert "不可用" in response.content or "摘要" in response.content

    print("✓ test_33_handle_learning_summary: 学习摘要处理正确")


def test_34_handle_trigger_learning():
    """Test 34: 验证触发学习处理"""
    agent = _create_agent()
    response = agent._handle_trigger_learning("开始学习", {})

    assert response.content is not None
    assert "不可用" in response.content or "触发" in response.content

    print("✓ test_34_handle_trigger_learning: 触发学习处理正确")


def test_35_handle_search_learning():
    """Test 35: 验证搜索学习内容处理"""
    agent = _create_agent()
    response = agent._handle_search_learning("搜索学过的Python", {})

    assert response.content is not None

    print("✓ test_35_handle_search_learning: 搜索学习处理正确")
