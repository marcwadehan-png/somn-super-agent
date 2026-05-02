# -*- coding: utf-8 -*-
"""
Tests for browser_learning.py
从 if __name__ == "__main__" 迁移的 pytest 测试用例。
"""

from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest


# ──────────────────────────────────────────────────────────────
# 模块导入与基本检查
# ──────────────────────────────────────────────────────────────

class TestBrowserLearningModule:
    """browser_learning 模块基础检查"""

    def test_module_imports(self):
        """模块能正常导入"""
        from src.neural_memory.browser_learning import BrowserNetworkLearner
        assert BrowserNetworkLearner is not None

    def test_run_browser_learning_callable(self):
        """顶层入口 run_browser_learning 可调用"""
        from src.neural_memory.browser_learning import run_browser_learning
        assert callable(run_browser_learning)

    def test_learner_accepts_findings_dir(self, tmp_path):
        """BrowserNetworkLearner 能接受 findings_dir 参数"""
        from src.neural_memory.browser_learning import BrowserNetworkLearner
        learner = BrowserNetworkLearner(findings_dir=str(tmp_path))
        assert learner is not None


# ──────────────────────────────────────────────────────────────
# BrowserNetworkLearner 基础
# ──────────────────────────────────────────────────────────────

class TestBrowserNetworkLearner:
    """测试 BrowserNetworkLearner 核心逻辑"""

    def test_learner_creation_default(self):
        """默认参数创建（findings_dir 为必需参数）"""
        from src.neural_memory.browser_learning import BrowserNetworkLearner
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            learner = BrowserNetworkLearner(findings_dir=tmp)
            assert learner is not None

    def test_learner_creation_with_browser_type(self, tmp_path):
        """指定 browser_type 创建"""
        from src.neural_memory.browser_learning import BrowserNetworkLearner
        for bt in ["chromium", "firefox", "webkit", "auto"]:
            learner = BrowserNetworkLearner(findings_dir=str(tmp_path), browser_type=bt)
            assert learner is not None
