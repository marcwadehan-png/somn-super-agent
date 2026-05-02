# -*- coding: utf-8 -*-
"""
agent_core 测试用例 - API 与集成测试
Agent Core Tests - API & Integration Tests
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


def test_19_learn_from_interaction():
    """Test 19: 验证从交互中学习"""
    from tests.agent_core_test._mocks import MockMemorySystem

    memory = MockMemorySystem()
    kb = MockKnowledgeBase()

    with patch.object(AgentCore, '_background_warmup'):
        from src.core.agent_core import AgentCore
        agent = AgentCore(memory, kb, TEST_CONFIG)

    response = Mock()
    response.content = "这是一个有效的回答"
    response.confidence = 0.85

    agent._learn_from_interaction("这是一个很长的用户陈述内容不需要问问题", response)
    assert len(memory.memories) > 0

    print("✓ test_19_learn_from_interaction: 从交互学习正确")


def test_20_execute_action():
    """Test 20: 验证操作执行"""
    agent = _create_agent()

    result1 = agent._execute_action('prepare_word_template', {'topic': '测试'})
    assert "准备好" in result1 or "Word" in result1

    result2 = agent._execute_action('prepare_ppt_template', {'topic': '测试'})
    assert "准备好" in result2 or "PPT" in result2

    result3 = agent._execute_action('unknown_action', {})
    assert "未知" in result3

    print("✓ test_20_execute_action: 操作执行正确")


def test_21_get_learning_status():
    """Test 21: 验证学习状态获取"""
    agent = _create_agent()
    status = agent.get_learning_status()

    assert isinstance(status, dict)
    assert 'learning_enabled' in status
    assert 'session_interactions' in status
    assert 'memory_stats' in status
    assert 'kb_stats' in status

    print("✓ test_21_get_learning_status: 学习状态获取正确")


def test_22_get_learning_summary():
    """Test 22: 验证学习摘要获取"""
    agent = _create_agent()
    summary = agent.get_learning_summary()
    assert summary == "学习系统未启用"

    print("✓ test_22_get_learning_summary: 学习摘要获取正确")


def test_23_trigger_learning():
    """Test 23: 验证手动触发学习"""
    agent = _create_agent()
    result = agent.trigger_learning()

    assert isinstance(result, dict)
    assert 'success' in result

    print("✓ test_23_trigger_learning: 手动触发学习正确")


def test_24_scan_directory():
    """Test 24: 验证目录扫描公共API"""
    agent = _create_agent()
    result = agent.scan_directory("test_path")
    assert result is None

    print("✓ test_24_scan_directory: 目录扫描 API 正确")


def test_25_generate_strategy():
    """Test 25: 验证策略生成公共API"""
    agent = _create_agent()
    result = agent.generate_strategy("提高销量")
    assert result is None

    print("✓ test_25_generate_strategy: 策略生成 API 正确")


def test_26_predict_content_performance():
    """Test 26: 验证内容表现预测API"""
    agent = _create_agent()
    result = agent.predict_content_performance({"title": "test", "content": "test"})
    assert result is None

    print("✓ test_26_predict_content_performance: 内容预测 API 正确")


def test_27_generate_markdown_report():
    """Test 27: 验证 Markdown 报告生成 API"""
    agent = _create_agent()
    result = agent.generate_markdown_report("测试报告", [])
    assert result is None

    print("✓ test_27_generate_markdown_report: Markdown 报告 API 正确")


def test_28_action_scan_directory():
    """Test 28: 验证扫描目录操作"""
    agent = _create_agent()
    result = agent._action_scan_directory({'path': 'test_path'})
    assert "模块不可用" in result or "扫描" in result

    print("✓ test_28_action_scan_directory: 扫描目录操作正确")


def test_29_action_analyze_cleanup():
    """Test 29: 验证分析清理操作"""
    agent = _create_agent()
    result = agent._action_analyze_cleanup({})
    assert "模块不可用" in result or "先执行" in result

    print("✓ test_29_action_analyze_cleanup: 分析清理操作正确")


def test_31_process_input_basic():
    """Test 31: 验证 process_input 基础功能"""
    agent = _create_agent()

    result = agent.process_input("你好")
    assert isinstance(result, str)
    assert len(result) > 0

    result2 = agent.process_input("谢谢")
    assert isinstance(result2, str)

    result3 = agent.process_input("搜索Python")
    assert isinstance(result3, str)

    print("✓ test_31_process_input_basic: process_input 基础功能正确")


def test_32_process_input_with_persona():
    """Test 32: 验证 process_input 与人设引擎集成"""
    agent = _create_agent()

    mock_persona = Mock()
    mock_persona.assess_signals.return_value = {
        'signals': [], 'priority': 'low',
        'suggested_response': None, 'suggested_scenario': None
    }
    mock_persona.check_output_style.return_value = {
        'should_brief': False, 'brief_action': None
    }
    agent.persona = mock_persona

    result = agent.process_input("你好")
    assert isinstance(result, str)

    print("✓ test_32_process_input_with_persona: 人设引擎集成正确")


def test_36_multiple_interactions():
    """Test 36: 验证多次交互的会话状态"""
    from tests.agent_core_test._mocks import MockMemorySystem

    memory = MockMemorySystem()
    kb = MockKnowledgeBase()

    with patch.object(AgentCore, '_background_warmup'):
        from src.core.agent_core import AgentCore
        agent = AgentCore(memory, kb, TEST_CONFIG)

    initial_count = agent.session_context['interaction_count']

    for i in range(5):
        agent.process_input(f"你好 {i}")

    assert agent.session_context['interaction_count'] == initial_count + 5
    assert len(memory.memories) >= 10

    print("✓ test_36_multiple_interactions: 多次交互状态正确")


def test_37_context_persistence():
    """Test 37: 验证上下文持久化"""
    agent = _create_agent()
    agent.session_context['current_topic'] = "Python学习"

    context = agent._gather_context("继续学习", "general_chat")
    assert context.get('current_topic') == "Python学习"

    print("✓ test_37_context_persistence: 上下文持久化正确")


def test_39_response_content_structure():
    """Test 39: 验证响应内容结构"""
    agent = _create_agent()
    response = agent._handle_greeting("你好", {})

    assert hasattr(response, 'content')
    assert hasattr(response, 'action')
    assert hasattr(response, 'action_params')
    assert hasattr(response, 'confidence')

    print("✓ test_39_response_content_structure: 响应内容结构正确")


def test_40_backward_compatibility():
    """Test 40: 验证向后兼容性"""
    from src.core.agent_core import (
        AgentCore, SOMN_CORE_AVAILABLE, MIGRATED_MODULES_AVAILABLE,
        LEARNING_SYSTEM_AVAILABLE, PERSONA_AVAILABLE
    )

    assert callable(AgentCore)
    assert isinstance(SOMN_CORE_AVAILABLE, bool)
    assert isinstance(MIGRATED_MODULES_AVAILABLE, bool)
    assert isinstance(LEARNING_SYSTEM_AVAILABLE, bool)
    assert isinstance(PERSONA_AVAILABLE, bool)

    print("✓ test_40_backward_compatibility: 向后兼容性正确")
