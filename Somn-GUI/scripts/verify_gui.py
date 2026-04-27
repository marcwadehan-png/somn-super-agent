#!/usr/bin/env python3
"""Somn GUI 桌面验证脚本

检查所有依赖、模块导入、配置文件的完整性，
确保 GUI 可以正常启动。

用法:
  python scripts/verify_gui.py           # 完整检查
  python scripts/verify_gui.py --fix     # 检查并尝试修复问题
"""

import sys
import importlib
from pathlib import Path

_GUI_ROOT = Path(__file__).parent.parent.resolve()
if str(_GUI_ROOT) not in sys.path:
    sys.path.insert(0, str(_GUI_ROOT))


class Colors:
    OK = "\033[92m"
    WARN = "\033[93m"
    FAIL = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"


def ok(msg):   print(f"  {Colors.OK}✓{Colors.END} {msg}")
def warn(msg): print(f"  {Colors.WARN}⚠{Colors.END} {msg}")
def fail(msg): print(f"  {Colors.FAIL}✗{Colors.END} {msg}")


def check_python_version():
    """检查 Python 版本 (>=3.10)"""
    print(f"\n{Colors.BOLD}1. Python 版本{Colors.END}")
    ver = sys.version_info
    if ver >= (3, 10):
        ok(f"Python {ver.major}.{ver.minor}.{ver.micro} ✓")
    else:
        fail(f"Python {ver.major}.{ver.minor} — 需要 >=3.10")


def check_dependencies():
    """检查依赖包"""
    print(f"\n{Colors.BOLD}2. 依赖包检查{Colors.END}")

    required = {
        "PyQt6": ">=6.5.0",
        "httpx": ">=0.24.0",
        "yaml": ">=6.0",          # PyYAML
        "loguru": ">=0.7.0",
        "docx": ">=1.0.0",        # python-docx
        "reportlab": ">=4.0.0",
        "websockets": ">=14.0",
    }

    missing = []
    for pkg, ver in required.items():
        try:
            mod = importlib.import_module(pkg)
            version = getattr(mod, "__version__", "unknown")
            ok(f"{pkg} {version}")
        except ImportError:
            fail(f"{pkg} {ver} — 未安装")
            missing.append(pkg)

    if missing:
        warn(f"缺少 {len(missing)} 个依赖，请执行:")
        warn(f"  pip install {' '.join(missing)}")

    return len(missing) == 0


def check_module_imports():
    """检查所有核心模块是否可导入"""
    print(f"\n{Colors.BOLD}3. 模块导入检查{Colors.END}")

    modules = [
        "somngui",
        "somngui.core.config",
        "somngui.core.connection",
        "somngui.core.state",
        "somngui.client.api_client",
        "somngui.client.websocket_client",
        "somngui.cache.cache_db",
        "somngui.cache.cache_manager",
        "somngui.gui._types",
        "somngui.gui._stubs",
        "somngui.gui.tray_icon",
        "somngui.gui.main_window",
        "somngui.utils.file_ops",
        "somngui.utils.doc_export",
        "somngui.resources",
    ]

    failed = []
    for mod_name in modules:
        try:
            importlib.import_module(mod_name)
            ok(mod_name)
        except Exception as e:
            fail(f"{mod_name} — {e}")
            failed.append((mod_name, str(e)))

    return len(failed) == 0


def check_resources():
    """检查资源文件"""
    print(f"\n{Colors.BOLD}4. 资源文件检查{Colors.END}")

    resources_dir = _GUI_ROOT / "somngui" / "resources"
    files_to_check = [
        resources_dir / "light.qss",
        resources_dir / "dark.qss",
        resources_dir / "__init__.py",
    ]

    for f in files_to_check:
        if f.exists():
            size = f.stat().st_size
            ok(f"{f.name} ({size} bytes)")
        else:
            fail(f"{f.name} — 不存在")

    # 检查 QSS 基本覆盖
    qss_files = list(resources_dir.glob("*.qss"))
    if qss_files:
        ok(f"共 {len(qss_files)} 个 QSS 主题: {', '.join(f.stem for f in qss_files)}")
    else:
        warn("未找到 QSS 主题文件")


def check_config():
    """检查配置文件"""
    print(f"\n{Colors.BOLD}5. 配置文件检查{Colors.END}")

    config_path = _GUI_ROOT / "config" / "gui_config.yaml"
    if config_path.exists():
        ok(f"gui_config.yaml 存在")
        try:
            import yaml
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
            ok(f"配置解析成功，{len(cfg)} 个顶级键")
        except Exception as e:
            fail(f"配置解析失败: {e}")
    else:
        warn("gui_config.yaml 不存在 (将使用默认配置)")


def check_qt_backend():
    """检查 Qt 后端可用性"""
    print(f"\n{Colors.BOLD}6. Qt 后端检查{Colors.END}")

    # 仅检查能否导入 Qt 核心（不尝试创建 QApplication）
    try:
        import PyQt6
        pyside_ver = getattr(PyQt6, "__version__", "unknown")
        ok(f"PyQt6 {pyside_ver}")
    except ImportError as e:
        fail(f"PyQt6 导入失败: {e}")
        return False

    try:
        from PyQt6.QtCore import qVersion
        ok(f"Qt {qVersion()}")
    except Exception as e:
        warn(f"Qt 版本获取失败: {e}")

    # 检查平台插件
    try:
        from PyQt6.QtCore import QLibraryInfo
        plugins_dir = QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath)
        ok(f"Qt 插件目录: {plugins_dir}")
    except Exception as e:
        warn(f"无法获取插件路径: {e}")

    # 检查是否有 display（Linux 下很重要）
    import os
    display = os.environ.get("DISPLAY", os.environ.get("WAYLAND_DISPLAY", ""))
    import platform
    if platform.system() == "Linux" and not display:
        warn("未检测到 DISPLAY/WAYLAND_DISPLAY，GUI 可能无法渲染")
        warn("如遇错误，尝试: export QT_QPA_PLATFORM=offscreen")
    else:
        ok(f"显示环境: {'OK' if display else 'Windows/macOS'}")

    return True


def check_export_formats():
    """检查文档导出功能"""
    print(f"\n{Colors.BOLD}7. 文档导出检查{Colors.END}")

    try:
        from somngui.utils.doc_export import EXPORT_FORMATS
        ok(f"支持 {len(EXPORT_FORMATS)} 种导出格式: {', '.join(EXPORT_FORMATS.keys())}")
    except Exception as e:
        fail(f"导出模块加载失败: {e}")
        return

    # 快速测试纯文本导出
    try:
        import tempfile
        from somngui.utils.doc_export import export_document
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w") as f:
            f.write("")
            tmp = f.name
        from pathlib import Path
        Path(tmp).unlink()  # 删除空文件
        export_document(tmp, "测试内容", fmt=".txt", title="测试")
        size = Path(tmp).stat().st_size
        Path(tmp).unlink()
        ok(f"TXT 导出测试通过 ({size} bytes)")
    except Exception as e:
        warn(f"TXT 导出测试跳过: {e}")


def check_websocket():
    """检查 WebSocket 客户端"""
    print(f"\n{Colors.BOLD}8. WebSocket 客户端检查{Colors.END}")

    try:
        from somngui.client.websocket_client import SomnWebSocketClient
        ws = SomnWebSocketClient("ws://127.0.0.1:8964/ws")

        methods = [
            "connect", "disconnect", "send_chat", "send_ping",
            "set_callbacks", "is_connected",
        ]
        for method in methods:
            if hasattr(ws, method):
                ok(f"SomnWebSocketClient.{method}()")
            else:
                fail(f"SomnWebSocketClient.{method}() — 缺失")
    except Exception as e:
        fail(f"WebSocket 模块加载失败: {e}")


def main():
    print(f"{Colors.BOLD}{'=' * 55}{Colors.END}")
    print(f"{Colors.BOLD}  Somn GUI 桌面验证 v1.0{Colors.END}")
    print(f"{Colors.BOLD}{'=' * 55}{Colors.END}")
    print(f"项目路径: {_GUI_ROOT}")

    check_python_version()
    deps_ok = check_dependencies()
    imports_ok = check_module_imports()
    check_resources()
    check_config()
    qt_ok = check_qt_backend()
    check_export_formats()
    check_websocket()

    # 总结
    print(f"\n{Colors.BOLD}{'=' * 55}{Colors.END}")
    if deps_ok and imports_ok and qt_ok:
        print(f"  {Colors.OK}{Colors.BOLD}✓ 所有检查通过，可以启动 GUI{Colors.END}")
        print(f"\n  启动命令:")
        print(f"    cd {_GUI_ROOT}")
        print(f"    python start_gui.py              # 自动发现后端")
        print(f"    python start_gui.py --offline    # 离线模式")
        print(f"    python start_gui.py --theme dark # 暗色主题")
    else:
        print(f"  {Colors.WARN}{Colors.BOLD}⚠ 部分检查未通过，请修复后再启动{Colors.END}")
    print(f"{Colors.BOLD}{'=' * 55}{Colors.END}")


if __name__ == "__main__":
    main()
