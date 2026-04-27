# -*- coding: utf-8 -*-
"""
test_somn_description.py - Somn 描述更新测试

验证所有核心文件中的 Somn 描述已更新为新 slogan。

@pytest.mark.unit
"""
import sys
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

import pytest


# ============================================================================
# 测试标记
# ============================================================================
pytestmark = pytest.mark.unit


# ============================================================================
# 测试夹具 (Fixtures)
# ============================================================================

@pytest.fixture
def somn_gui_root():
    """Somn-GUI 根目录"""
    return PROJECT_ROOT.parent / "Somn-GUI"


@pytest.fixture
def somn_backend_root():
    """Somn 后端根目录"""
    return PROJECT_ROOT


@pytest.fixture
def new_slogan():
    """新的 slogan"""
    return "汇千古之智，向未知而生"


@pytest.fixture
def old_description():
    """旧的描述关键词（应该不再出现）"""
    return "智能办公助手"


# ============================================================================
# 测试用例
# ============================================================================

class TestSomnGUIDescription:
    """Somn-GUI 描述更新测试"""

    def test_main_window_title_updated(self, somn_gui_root, new_slogan):
        """验证主窗口标题已更新"""
        main_window_path = somn_gui_root / "somngui" / "gui" / "main_window.py"
        content = main_window_path.read_text(encoding="utf-8")
        assert new_slogan in content, \
            f"主窗口标题未包含新 slogan: {new_slogan}"
        assert "Somn - 智能办公助手" not in content, \
            "主窗口仍包含旧描述 '智能办公助手'"

    def test_welcome_message_updated(self, somn_gui_root, new_slogan):
        """验证欢迎消息已更新"""
        templates_path = somn_gui_root / "somngui" / "gui" / "_ui_templates.py"
        content = templates_path.read_text(encoding="utf-8")
        assert new_slogan in content, \
            f"欢迎消息未包含新 slogan: {new_slogan}"


class TestSomnBackendDescription:
    """Somn 后端描述更新测试"""

    def test_main_window_title_updated(self, somn_backend_root, new_slogan):
        """验证后端主窗口标题已更新"""
        main_window_path = somn_backend_root / "smart_office_assistant" / "src" / "gui" / "main_window.py"
        content = main_window_path.read_text(encoding="utf-8")
        assert new_slogan in content, \
            f"后端主窗口未包含新 slogan: {new_slogan}"
        assert "智能办公助手" not in content, \
            "后端主窗口仍包含旧描述"

    def test_welcome_message_updated(self, somn_backend_root, new_slogan):
        """验证后端欢迎消息已更新"""
        stubs_path = somn_backend_root / "smart_office_assistant" / "src" / "gui" / "_mw_stubs.py"
        content = stubs_path.read_text(encoding="utf-8")
        assert new_slogan in content, \
            f"后端欢迎消息未包含新 slogan: {new_slogan}"

    def test_about_dialog_updated(self, somn_backend_root, new_slogan):
        """验证关于对话框已更新"""
        main_window_path = somn_backend_root / "smart_office_assistant" / "src" / "gui" / "main_window.py"
        content = main_window_path.read_text(encoding="utf-8")
        assert "关于 Somn" in content, \
            "关于对话框未更新为 '关于 Somn'"

    def test_src_init_updated(self, somn_backend_root, new_slogan):
        """验证 src/__init__.py 已更新"""
        init_path = somn_backend_root / "smart_office_assistant" / "src" / "__init__.py"
        content = init_path.read_text(encoding="utf-8")
        assert new_slogan in content, \
            f"src/__init__.py 未包含新 slogan: {new_slogan}"


class TestSomnConfigFiles:
    """Somn 配置文件更新测试"""

    def test_config_yaml_updated(self, somn_backend_root, new_slogan):
        """验证 config.yaml 已更新"""
        config_path = somn_backend_root / "smart_office_assistant" / "config.yaml"
        content = config_path.read_text(encoding="utf-8")
        assert new_slogan in content, \
            f"config.yaml 未包含新 slogan: {new_slogan}"

    def test_start_bat_updated(self, somn_backend_root, new_slogan):
        """验证 start.bat 已更新"""
        start_bat_path = somn_backend_root / "smart_office_assistant" / "start.bat"
        content = start_bat_path.read_text(encoding="utf-8")
        assert new_slogan in content, \
            f"start.bat 未包含新 slogan: {new_slogan}"
        assert "智能办公助手" not in content, \
            "start.bat 仍包含旧描述"

    def test_start_somn_bat_updated(self, somn_backend_root, new_slogan):
        """验证 start_somn.bat 已更新"""
        start_somn_path = somn_backend_root / "smart_office_assistant" / "start_somn.bat"
        content = start_somn_path.read_text(encoding="utf-8")
        assert new_slogan in content, \
            f"start_somn.bat 未包含新 slogan: {new_slogan}"

    def test_setup_py_updated(self, somn_backend_root, new_slogan):
        """验证 setup.py 已更新"""
        setup_path = somn_backend_root / "smart_office_assistant" / "setup.py"
        content = setup_path.read_text(encoding="utf-8")
        assert new_slogan in content, \
            f"setup.py 未包含新 slogan: {new_slogan}"

    def test_main_py_updated(self, somn_backend_root, new_slogan):
        """验证 main.py 已更新"""
        main_path = somn_backend_root / "smart_office_assistant" / "main.py"
        content = main_path.read_text(encoding="utf-8")
        assert new_slogan in content, \
            f"main.py 未包含新 slogan: {new_slogan}"


# ============================================================================
# 测试运行入口
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
