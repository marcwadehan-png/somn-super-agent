# -*- coding: utf-8 -*-
"""
Shared fixtures for tests/neural_memory/
"""

import pytest
import tempfile
import os
from pathlib import Path


@pytest.fixture
def sample_encoding_context():
    """提供标准 EncodingContext 实例，供 encoding_types / encoding_subsystems 测试使用。"""
    from src.neural_memory.encoding_types import EncodingContext
    return EncodingContext(
        user_id="test_user",
        session_id="test_session",
        scenario="test_scenario",
        domain="growth_consulting",
    )


@pytest.fixture
def sample_learning_state(tmp_path):
    """提供标准学习状态 dict，供 reinforcement_learning 测试使用。"""
    return {
        "current_knowledge": ["概念A", "概念B"],
        "recent_findings": [
            {"title": "发现1", "confidence": 0.8},
            {"title": "发现2", "confidence": 0.6},
        ],
        "errors": [],
        "patterns_count": 3,
        "data_quality": 0.85,
    }


@pytest.fixture
def rl_system(tmp_path):
    """提供已初始化的 RL 系统，供 reinforcement_learning 测试使用。"""
    from src.neural_memory.reinforcement_learning_v3 import ReinforcementLearningSystemV3
    return ReinforcementLearningSystemV3(base_path=str(tmp_path))


@pytest.fixture
def tmp_project(tmp_path):
    """提供模拟项目目录结构（含 data/ 子目录），供 orchestrator 等测试使用。"""
    project = tmp_path / "project"
    project.mkdir()
    (project / "data").mkdir()
    (project / "data" / "findings").mkdir()
    (project / "data" / "learning").mkdir()
    (project / "data" / "memory").mkdir()
    (project / "data" / "knowledge").mkdir()
    return project
