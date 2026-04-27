"""
Somn 项目测试套件 — 共享 fixtures 和路径初始化

所有测试自动获得:
- sys.path 三层路径 (src / smart_office_assistant / 项目根)
- tmp_path 临时目录
- 抑制日志噪音
"""
import sys
import os
import logging
import warnings
from pathlib import Path

# ============================================================
# 项目根定位 + 路径初始化（所有测试共享）
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "smart_office_assistant" / "src"
PKG_DIR = PROJECT_ROOT / "smart_office_assistant"

# 三层路径（与 path_bootstrap.py 保持一致）
_str_root = str(PROJECT_ROOT)
_str_src = str(SRC_DIR)
_str_pkg = str(PKG_DIR)

for _p in (_str_src, _str_pkg, _str_root):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# 抑制测试期间的非关键日志
logging.disable(logging.CRITICAL)


# ============================================================
# pytest fixtures
# ============================================================

def pytest_configure(config):
    """pytest 启动时注册自定义标记"""
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: integration tests")
    config.addinivalue_line("markers", "core: core module tests")
    config.addinivalue_line("markers", "dispatcher: dispatcher tests")
    config.addinivalue_line("markers", "memory: memory system tests")
    config.addinivalue_line("markers", "claw: claw subsystem tests")
    config.addinivalue_line("markers", "learning: learning system tests")
    config.addinivalue_line("markers", "scheduler: scheduler system tests")
    config.addinivalue_line("markers", "tier3: tier3 neural scheduler tests")
    config.addinivalue_line("markers", "optimizer: scheduler optimizer tests")


import pytest

@pytest.fixture(scope="session")
def project_root() -> Path:
    """项目根目录"""
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def src_dir() -> Path:
    """源码目录"""
    return SRC_DIR


@pytest.fixture
def clean_tmp(tmp_path) -> Path:
    """干净的临时目录（每个测试独立）"""
    return tmp_path


@pytest.fixture
def suppress_logs():
    """上下文管理器：抑制日志输出"""
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)
