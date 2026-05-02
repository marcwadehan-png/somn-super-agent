"""
测试 Somn 启动器 LOGO 配置
遵循 TESTING_RULES.md - 无测试不合入
"""

import sys
import pytest
import subprocess
from pathlib import Path

# 动态解析项目路径（不再硬编码）
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_GUI_DIR = _PROJECT_ROOT.parent / "Somn-GUI"


class TestLauncherLogo:
    """启动器 LOGO 配置测试"""

    @pytest.fixture
    def logo_path(self):
        """LOGO 文件路径"""
        return _GUI_DIR / "LOGO.jpg"

    @pytest.fixture
    def shortcuts(self):
        """快捷方式路径列表"""
        return [
            _PROJECT_ROOT.parent / "Somn-GUI.lnk",
            Path.home() / "Desktop" / "Somn GUI.lnk",
        ]

    def test_logo_exists(self, logo_path):
        """LOGO 文件必须存在"""
        assert logo_path.exists(), f"LOGO 文件不存在: {logo_path}"

    def test_shortcuts_exist(self, shortcuts):
        """快捷方式必须存在"""
        for shortcut_path in shortcuts:
            if shortcut_path.exists():
                assert shortcut_path.exists(), f"快捷方式不存在: {shortcut_path}"

    def test_launcher_logo_configuration(self):
        """启动器 LOGO 配置验证（通过外部脚本）"""
        logo_str = str(_GUI_DIR / "LOGO.jpg")
        lnk_str = str(_PROJECT_ROOT.parent / "Somn-GUI.lnk")
        desktop_str = str(Path.home() / "Desktop" / "Somn GUI.lnk")

        # 使用当前 Python 解释器，避免硬编码路径
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                f"""
import pythoncom
from win32com.client import Dispatch

logo_path = r"{logo_str}"
shortcuts = [
    (r"{lnk_str}", "AI文件夹"),
    (r"{desktop_str}", "桌面"),
]

pythoncom.CoInitialize()
try:
    wsh = Dispatch("WScript.Shell")
    all_passed = True
    for path, name in shortcuts:
        try:
            sh = wsh.CreateShortcut(path)
            icon_str = sh.IconLocation
            icon_path = icon_str.split(",")[0] if icon_str else ""
            desc = sh.Description

            if icon_path.lower().replace("/", "\\\\") == logo_path.lower():
                pass
            else:
                print(f"FAIL: {{name}} 图标错误")
                all_passed = False

            if desc == "Somn 汇千古之智，向未知而生":
                pass
            else:
                print(f"FAIL: {{name}} 描述错误")
                all_passed = False
        except Exception as e:
            print(f"FAIL: {{name}} 读取失败: {{e}}")
            all_passed = False

    if all_passed:
        print("ALL_PASSED")
finally:
    pythoncom.CoUninitialize()
""",
            ],
            capture_output=True,
            text=True,
            cwd=str(_PROJECT_ROOT),
        )

        output = result.stdout + result.stderr
        assert "ALL_PASSED" in output, f"测试失败:\n{output}"
        assert "FAIL" not in output, f"部分测试失败:\n{output}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
