# -*- coding: utf-8 -*-
"""
agent_core 测试用例 - 基础测试
Agent Core Tests - Basic Tests
"""
import sys
from pathlib import Path
from unittest.mock import patch, Mock

# 项目路径引导
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "smart_office_assistant"))

TEST_CONFIG = {
    'auto_learn': True,
    'learning_data_path': 'data/learning',
}


def test_01_import():
    """Test 01: 验证模块可以正确导入"""
    from src.core.agent_core import (
        AgentCore, AgentResponse,
        SOMN_CORE_AVAILABLE, MIGRATED_MODULES_AVAILABLE,
        LEARNING_SYSTEM_AVAILABLE, PERSONA_AVAILABLE
    )
    assert AgentCore is not None, "AgentCore 类应可导入"
    assert AgentResponse is not None, "AgentResponse 应可导入"
    print("✓ test_01_import: 模块导入成功")


def test_02_agent_response_creation():
    """Test 02: 验证 AgentResponse 数据类"""
    from src.core.agent_core import AgentResponse

    resp1 = AgentResponse(content="测试内容")
    assert resp1.content == "测试内容"
    assert resp1.action is None
    assert resp1.action_params is None
    assert resp1.confidence == 1.0

    resp2 = AgentResponse(
        content="完整响应",
        action="test_action",
        action_params={'key': 'value'},
        confidence=0.95
    )
    assert resp2.action == "test_action"
    assert resp2.action_params == {'key': 'value'}
    assert resp2.confidence == 0.95

    print("✓ test_02_agent_response_creation: AgentResponse 创建正确")


def test_03_agent_core_initialization():
    """Test 03: 验证 AgentCore 可以正确初始化"""
    from src.core.agent_core import AgentCore
    from tests.agent_core_test._mocks import MockMemorySystem, MockKnowledgeBase

    memory = MockMemorySystem()
    kb = MockKnowledgeBase()

    with patch.object(AgentCore, '_background_warmup'):
        agent = AgentCore(memory, kb, TEST_CONFIG)

    assert agent.memory is not None
    assert agent.kb is not None
    assert agent.config == TEST_CONFIG
    assert agent.session_context is not None
    assert 'interaction_count' in agent.session_context

    print("✓ test_03_agent_core_initialization: AgentCore 初始化正确")


def test_04_session_context():
    """Test 04: 验证会话上下文"""
    from src.core.agent_core import AgentCore
    from tests.agent_core_test._mocks import MockMemorySystem, MockKnowledgeBase

    memory = MockMemorySystem()
    kb = MockKnowledgeBase()

    with patch.object(AgentCore, '_background_warmup'):
        agent = AgentCore(memory, kb, TEST_CONFIG)

    assert agent.session_context['interaction_count'] == 0
    assert agent.session_context['current_topic'] is None
    assert 'start_time' in agent.session_context

    agent.session_context['interaction_count'] += 1
    assert agent.session_context['interaction_count'] == 1

    print("✓ test_04_session_context: 会话上下文正确")


def test_05_extract_topic():
    """Test 05: 验证主题提取功能"""
    from src.core.agent_core import AgentCore
    from tests.agent_core_test._mocks import MockMemorySystem, MockKnowledgeBase

    memory = MockMemorySystem()
    kb = MockKnowledgeBase()

    with patch.object(AgentCore, '_background_warmup'):
        agent = AgentCore(memory, kb, TEST_CONFIG)

    test_cases = [
        ("关于项目X的需求", "项目X的需求"),
        ("主题是销售策略", "销售策略"),
        ("帮我写一个营销计划", None),
        ("你好", None),
        ("分析市场趋势报告", "分析市场趋势"),
    ]

    for user_input, expected in test_cases:
        result = agent._extract_topic(user_input)
        assert result == expected, f"输入 '{user_input}' 应提取为 '{expected}', 实际为 '{result}'"

    print("✓ test_05_extract_topic: 主题提取正确")
