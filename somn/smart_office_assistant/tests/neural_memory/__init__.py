"""neural_memory 包专用 pytest 配置"""

import sys
from pathlib import Path
import pytest

# 确保项目根在 sys.path 中
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# 执行全局路径引导
from path_bootstrap import bootstrap_project_paths
bootstrap_project_paths(__file__, change_cwd=True)

import numpy as np


@pytest.fixture
def sample_encoding_context():
    """创建标准测试编码上下文"""
    from src.neural_memory.encoding_types import EncodingContext
    return EncodingContext(
        user_id="test_user",
        session_id="test_session",
        scenario="growth_consultation",
        task_type="advice",
        domain="business",
        emotion="neutral",
        priority=8,
        attention_focus=["私域", "增长"],
        abstraction_level=1,
    )


@pytest.fixture
def sample_learning_state():
    """创建标准测试学习状态"""
    from src.neural_memory.reinforcement_learning_v3 import LearningState
    return LearningState(
        state_id="state_001",
        state_vector=np.random.randn(128).tolist(),
        description="测试状态",
        context={"task": "memory_retrieval"},
    )


@pytest.fixture
def tmp_project(tmp_path):
    """创建临时项目目录结构（用于调度器测试）"""
    from src.core.paths import set_temp_base
    set_temp_base(tmp_path)
    yield tmp_path
    # 清理
    from src.core.paths import restore_base
    restore_base()
