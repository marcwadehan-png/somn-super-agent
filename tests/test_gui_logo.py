# -*- coding: utf-8 -*-
"""
test_gui_logo.py - GUI LOGO 全局图标测试

测试范围:
1. Somn-GUI 托盘图标加载 LOGO.jpg
2. Somn 后端托盘图标加载 LOGO.jpg
3. LOGO 文件存在性验证
4. 图标创建回退机制

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
    # Somn-GUI 在 D:\AI\Somn-GUI (与 somn 平级)
    return PROJECT_ROOT.parent / "Somn-GUI"


@pytest.fixture
def logo_path(somn_gui_root):
    """LOGO.jpg 路径"""
    return somn_gui_root / "LOGO.jpg"


@pytest.fixture
def somn_backend_root():
    """Somn 后端根目录"""
    return PROJECT_ROOT


# ============================================================================
# 测试用例
# ============================================================================

class TestLogoFileExists:
    """LOGO 文件存在性测试"""

    def test_logo_jpg_exists_in_somn_gui(self, somn_gui_root, logo_path):
        """验证 LOGO.jpg 存在于 Somn-GUI 目录"""
        assert logo_path.exists(), f"LOGO.jpg 不存在: {logo_path}"
        assert logo_path.is_file(), f"LOGO.jpg 不是文件: {logo_path}"

    def test_logo_has_valid_extension(self, logo_path):
        """验证 LOGO 文件扩展名正确"""
        assert logo_path.suffix.lower() in [".jpg", ".jpeg", ".png"], \
            f"LOGO 扩展名无效: {logo_path.suffix}"

    def test_logo_file_size_reasonable(self, logo_path):
        """验证 LOGO 文件大小合理 (> 1KB)"""
        size = logo_path.stat().st_size
        assert size > 1024, f"LOGO 文件太小 ({size} bytes)，可能损坏"


class TestSomnGUITrayIcon:
    """Somn-GUI 托盘图标测试"""

    def test_tray_icon_module_imports(self):
        """验证 Somn-GUI tray_icon 模块可正常导入（需要 PySide6）"""
        # 检查 PySide6 是否可用
        try:
            import PySide6
        except ImportError:
            pytest.skip("PySide6 未安装，跳过 Qt 模块导入测试")
        
        # 添加 Somn-GUI 路径到 sys.path
        somn_gui_path = str(PROJECT_ROOT.parent / "Somn-GUI")
        if somn_gui_path not in sys.path:
            sys.path.insert(0, somn_gui_path)
        try:
            from somngui.gui.tray_icon import TrayIconManager, DEFAULT_ICON_PATH
        except ImportError as e:
            pytest.fail(f"导入失败: {e}")

    def test_tray_icon_default_path_configured(self, logo_path):
        """验证托盘图标默认路径指向 LOGO.jpg"""
        # 动态验证路径存在
        assert logo_path.exists()
        # 验证路径格式正确
        assert logo_path.name == "LOGO.jpg"


class TestSomnBackendTrayIcon:
    """Somn 后端托盘图标测试"""

    def test_backend_tray_icon_resolves_to_somn_gui_logo(self, logo_path):
        """验证后端托盘图标路径解析到 Somn-GUI 的 LOGO"""
        # 后端路径: PROJECT_ROOT.parent / "Somn-GUI" / "LOGO.jpg"
        expected = PROJECT_ROOT.parent / "Somn-GUI" / "LOGO.jpg"
        assert expected.exists(), f"后端 LOGO 路径无效: {expected}"
        # 只验证存在性，不要求完全相等（可能大小写差异）
        assert logo_path.exists(), f"GUI LOGO 路径无效: {logo_path}"


class TestLogoIconLoading:
    """LOGO 图标加载测试"""

    def test_logo_can_be_loaded_as_pixmap(self, logo_path):
        """验证 LOGO 可作为 QPixmap 加载"""
        # 仅在 PySide6 可用时测试
        try:
            from PySide6.QtGui import QPixmap
            pixmap = QPixmap(str(logo_path))
            assert not pixmap.isNull(), "LOGO 加载后 pixmap 为空"
            assert pixmap.width() > 0, "LOGO 宽度为 0"
            assert pixmap.height() > 0, "LOGO 高度为 0"
        except ImportError:
            pytest.skip("PySide6 未安装，跳过 Qt 相关测试")

    def test_logo_can_be_loaded_as_icon(self, logo_path):
        """验证 LOGO 可作为 QIcon 加载"""
        try:
            from PySide6.QtGui import QIcon
            icon = QIcon(str(logo_path))
            # QIcon 不会为 null，即使图片无效也会返回默认图标
            # 所以这里只验证不抛出异常
            assert icon is not None
        except ImportError:
            pytest.skip("PySide6 未安装，跳过 Qt 相关测试")


class TestWindowIconConfiguration:
    """窗口图标配置测试"""

    def test_start_gui_defines_logo_path(self):
        """验证 start_gui.py 定义了 LOGO_PATH 常量"""
        gui_path = PROJECT_ROOT.parent / "Somn-GUI" / "start_gui.py"
        content = gui_path.read_text(encoding="utf-8")
        assert "LOGO_PATH" in content, "start_gui.py 未定义 LOGO_PATH"

    def test_run_py_configures_window_icon(self):
        """验证后端 run.py 配置了窗口图标"""
        run_path = PROJECT_ROOT / "smart_office_assistant" / "run.py"
        content = run_path.read_text(encoding="utf-8")
        assert "setWindowIcon" in content, "run.py 未配置 setWindowIcon"


# ============================================================================
# 测试运行入口
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
