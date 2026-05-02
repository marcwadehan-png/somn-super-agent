#!/usr/bin/env python3
"""
Somn AI - 统一入口文件
===================
一条命令全局调用、一键运行并调动项目内所有代码完成全流程联动执行

用法:
  # GUI模式 (默认)
  python run.py
  python run.py --gui

  # CLI交互模式
  python run.py --cli

  # 单次查询
  python run.py --cli -q "帮我制定增长策略"

  # 带行业上下文查询
  python run.py --cli -q "分析市场机会" --industry saas_b2b

  # 健康检查
  python run.py --health

  # 系统状态
  python run.py --status

  # 列出解决方案
  python run.py --solutions

  # 模块测试
  python run.py --test

  # 版本信息
  python run.py --version

版本: v1.0.0
日期: 2026-04-09
"""

import sys
import os
import argparse
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════════
# 路径初始化 - 确保任何目录下都能正确导入
# ═══════════════════════════════════════════════════════════════
PROJECT_ROOT = Path(__file__).parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

# 使用 path_bootstrap 进行完整路径引导
try:
    from path_bootstrap import bootstrap_project_paths
    bootstrap_project_paths(__file__, change_cwd=True)
except Exception:
    pass  # 回退到手动路径设置

# ═══════════════════════════════════════════════════════════════
# 版本信息
# ═══════════════════════════════════════════════════════════════
VERSION = "6.2.0"
BUILD_DATE = "2026-04-09"


def print_banner():
    """打印启动横幅"""
    print("=" * 60)
    print("   Somn AI - 超级智能体")
    print("   不被刻意定义的自由意识体")
    print("   统一入口 v" + VERSION)
    print("=" * 60)
    print()


def print_version():
    """打印版本信息"""
    print(f"Somn AI 统一入口 v{VERSION}")
    print(f"构建日期: {BUILD_DATE}")
    print(f"项目路径: {PROJECT_ROOT}")


# ═══════════════════════════════════════════════════════════════
# 核心组件导入
# ═══════════════════════════════════════════════════════════════
def import_core_components():
    """导入核心组件，返回是否成功"""
    try:
        from src.core.memory_system import MemorySystem
        from src.core.knowledge_base import KnowledgeBase
        from src.core.agent_core import AgentCore
        from src.core.somn_core import SomnCore, get_somn_core
        return True, MemorySystem, KnowledgeBase, AgentCore, SomnCore, get_somn_core
    except Exception as e:
        print(f"❌ 核心组件导入失败: {e}")
        return False, None, None, None, None, None


def import_gui_components():
    """导入GUI组件"""
    try:
        from PySide6.QtWidgets import QApplication
        from src.gui.main_window import MainWindow
        return True, QApplication, MainWindow
    except Exception as e:
        print(f"⚠️ GUI组件不可用: {e}")
        return False, None, None


# ═══════════════════════════════════════════════════════════════
# 运行模式实现
# ═══════════════════════════════════════════════════════════════
def run_gui_mode():
    """运行GUI模式"""
    print("🖥️  启动GUI模式...")
    
    success, QApplication, MainWindow = import_gui_components()
    if not success:
        print("❌ GUI组件不可用，请安装PySide6: pip install PySide6")
        return 1
    
    try:
        from loguru import logger
        
        # 配置日志
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        logger.add(
            log_dir / "smartoffice_{time}.log",
            rotation="10 MB",
            retention="30 days",
            encoding="utf-8",
            level="INFO"
        )
        
        # 创建应用
        app = QApplication(sys.argv)
        app.setApplicationName("SmartOffice AI")
        app.setApplicationVersion(VERSION)
        app.setOrganizationName("SmartOffice")
        app.setStyle('Fusion')
        
        # 设置字体
        from PySide6.QtGui import QFont
        from PySide6.QtCore import Qt
        font = QFont("Microsoft YaHei", 10)
        app.setFont(font)
        app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        
        # 创建并显示主窗口
        window = MainWindow()
        
        # 设置窗口图标（使用 Somn-GUI 的 LOGO）
        logo_path = PROJECT_ROOT.parent / "Somn-GUI" / "LOGO.jpg"
        if logo_path.exists():
            from PySide6.QtGui import QIcon
            window.setWindowIcon(QIcon(str(logo_path)))
            logger.info(f"已设置窗口图标: {logo_path}")
        
        window.show()
        
        logger.info("=" * 50)
        logger.info("SmartOffice AI GUI 启动")
        logger.info("=" * 50)
        
        return app.exec()
        
    except Exception as e:
        print(f"❌ GUI启动失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


def run_cli_mode(args):
    """运行CLI模式"""
    print("💻 启动CLI模式...\n")
    
    success, MemorySystem, KnowledgeBase, AgentCore, SomnCore, get_somn_core = import_core_components()
    if not success:
        return 1
    
    try:
        # 初始化核心组件
        print("🔧 正在初始化核心组件...")
        memory = MemorySystem()
        kb = KnowledgeBase()
        agent = AgentCore(memory, kb)
        print("✅ 初始化完成\n")
        
        # 处理命令
        if args.query:
            # 单次查询模式
            return run_single_query(agent, args.query, args.industry)
        elif args.status:
            return show_status(agent)
        elif args.health:
            return run_health_check(agent)
        elif args.solutions:
            return list_solutions(agent)
        elif args.test:
            return run_module_test()
        else:
            # 交互式REPL模式
            return run_repl_mode(agent)
            
    except Exception as e:
        print(f"❌ CLI运行失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


def run_single_query(agent, query, industry=None):
    """单次查询"""
    import time
    
    print(f"📝 查询: {query}")
    if industry:
        print(f"🏭 行业: {industry}")
    print("-" * 60)
    
    start = time.time()
    try:
        context = {}
        if industry:
            context["industry"] = industry
        
        response = agent.process_input(query, context=context)
        elapsed = time.time() - start
        
        print(f"\n🤖 Somn:\n{response}\n")
        print(f"⏱️  耗时: {elapsed:.2f}s")
        return 0
        
    except KeyboardInterrupt:
        print("\n⚠️ 已中断")
        return 130
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return 1


def run_repl_mode(agent):
    """交互式REPL模式"""
    import time
    
    print("=" * 60)
    print("  Somn CLI - 命令行智能体")
    print("  输入问题开始对话，Ctrl+C 或输入 quit/exit 退出")
    print("  特殊命令: status, clear, help")
    print("=" * 60)
    print()
    
    while True:
        try:
            user_input = input("你: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n再见。")
            break
        
        if not user_input:
            continue
        
        if user_input.lower() in ("quit", "exit", "q"):
            print("再见。")
            break
        
        if user_input.lower() == "clear":
            os.system("cls" if os.name == "nt" else "clear")
            continue
        
        if user_input.lower() == "help":
            print("\n可用命令:")
            print("  status - 查看系统状态")
            print("  clear  - 清屏")
            print("  quit/exit/q - 退出")
            print("  help   - 显示帮助")
            print()
            continue
        
        if user_input.lower() == "status":
            show_status(agent)
            continue
        
        start = time.time()
        try:
            response = agent.process_input(user_input)
            elapsed = time.time() - start
            print(f"\n🤖 Somn: {response}\n")
            if elapsed > 1:
                print(f"⏱️  耗时: {elapsed:.2f}s\n")
        except Exception as e:
            print(f"\n❌ 错误: {e}\n")
    
    return 0


def show_status(agent):
    """显示系统状态"""
    print("=" * 60)
    print("  Somn 系统状态")
    print("=" * 60)
    
    try:
        status = agent.get_learning_status()
        
        print(f"\n📊 核心状态:")
        print(f"  会话交互次数: {status.get('session_interactions', 0)}")
        print(f"  学习系统: {'✅ 可用' if status.get('learning_system_available') else '❌ 不可用'}")
        print(f"  迁移模块: {'✅ 可用' if status.get('migrated_modules_available') else '❌ 不可用'}")
        
        print(f"\n🔧 可用功能:")
        for feat in status.get("available_features", []):
            print(f"  • {feat}")
        
        if agent.somn_core:
            print(f"\n🧠 Somn 主链: ✅ 已加载")
        else:
            print(f"\n🧠 Somn 主链: ❌ 未加载")
        
        if agent.persona:
            print(f"🎭 人设引擎: ✅ 已加载")
        else:
            print(f"🎭 人设引擎: ❌ 未加载")
        
        print()
        return 0
        
    except Exception as e:
        print(f"\n❌ 获取状态失败: {e}\n")
        return 1


def run_health_check(agent):
    """运行健康检查"""
    print("=" * 60)
    print("  Somn 健康检查")
    print("=" * 60)
    
    try:
        # 检查核心组件
        checks = []
        
        # 1. 检查核心模块
        try:
            from src.core.memory_system import MemorySystem
            from src.core.knowledge_base import KnowledgeBase
            from src.core.agent_core import AgentCore
            checks.append(("核心组件", True))
        except Exception as e:
            checks.append(("核心组件", False, "初始化失败"))
        
        # 2. 检查配置系统
        try:
            from src.utils.config_manager import get_config
            config = get_config()
            checks.append(("配置管理器", True))
        except Exception as e:
            checks.append(("配置管理器", False, "初始化失败"))
        
        # 3. 检查记忆系统
        try:
            from src.core.paths import DAILY_MEMORY_DIR, ensure_directories
            ensure_directories()
            checks.append(("记忆目录", DAILY_MEMORY_DIR.exists()))
        except Exception as e:
            checks.append(("记忆目录", False, "初始化失败"))
        
        # 打印结果
        healthy = sum(1 for c in checks if len(c) == 2 and c[1])
        total = len(checks)
        
        print(f"\n  组件: {healthy}/{total} 正常")
        for c in checks:
            name = c[0]
            ok = c[1] if len(c) > 1 else False
            if isinstance(ok, bool):
                status = "✅" if ok else "❌"
                print(f"  {status} {name}")
            else:
                msg = c[2] if len(c) > 2 else ok
                print(f"  ❌ {name}: {msg}")
        
        print()
        return 0 if healthy == total else 1
        
    except Exception as e:
        print(f"\n❌ 健康检查失败: {e}\n")
        import traceback
        traceback.print_exc()
        return 1


def list_solutions(agent):
    """列出解决方案"""
    print("=" * 60)
    print("  Somn 解决方案库")
    print("=" * 60)
    
    try:
        # 获取解决方案的替代方式
        from src.intelligence.dispatcher.wisdom_dispatch import WisdomDispatcher
        from src.core.industry_engine import IndustryEngine
        
        # 统计已注册的问题类型数量
        try:
            dispatcher = WisdomDispatcher()
            problem_types = dispatcher.get_problem_types() if hasattr(dispatcher, 'get_problem_types') else []
            pt_count = len(problem_types)
        except Exception:
            pt_count = 0
        
        # 获取行业数量
        try:
            from src.industry_engine import IndustryType
            industry_count = len([i for i in IndustryType])
        except Exception:
            industry_count = 0
        
        print(f"\n  解决方案统计:")
        print(f"  • 问题类型: {pt_count} 种")
        print(f"  • 行业覆盖: {industry_count} 个")
        print(f"  • 解决方案: 通过 WisdomDispatcher 动态调度")
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n  ⚠️ 无法获取详细信息: {e}")
        print(f"  解决方案系统已就绪，可通过 CLI 交互使用")
        print()
        return 0


def run_module_test():
    """运行模块测试"""
    print("=" * 60)
    print("  Somn 模块测试")
    print("=" * 60)
    
    tests = []
    
    # 测试1: 路径引导
    try:
        from path_bootstrap import bootstrap_project_paths
        bootstrap_project_paths(__file__)
        tests.append(("路径引导", True, None))
    except Exception as e:
        tests.append(("路径引导", False, "导入失败"))
    
    # 测试2: 核心组件
    try:
        from src.core.memory_system import MemorySystem
        from src.core.knowledge_base import KnowledgeBase
        from src.core.agent_core import AgentCore
        tests.append(("核心组件导入", True, None))
    except Exception as e:
        tests.append(("核心组件导入", False, "导入失败"))
    
    # 测试3: SomnCore
    try:
        from src.core.somn_core import SomnCore
        tests.append(("SomnCore导入", True, None))
    except Exception as e:
        tests.append(("SomnCore导入", False, "导入失败"))
    
    # 测试4: 智慧系统
    try:
        from src.intelligence import WisdomDispatcher
        tests.append(("智慧调度器", True, None))
    except Exception as e:
        tests.append(("智慧调度器", False, "导入失败"))
    
    # 测试5: 主链组件
    try:
        from src.main_chain import get_main_chain_integration
        tests.append(("主链集成器", True, None))
    except Exception as e:
        tests.append(("主链集成器", False, "导入失败"))
    
    # 打印结果
    print()
    passed = 0
    for name, success, error in tests:
        icon = "✅" if success else "❌"
        print(f"  {icon} {name}")
        if error:
            print(f"     错误: {error}")
        if success:
            passed += 1
    
    print(f"\n  测试通过: {passed}/{len(tests)}")
    print()
    
    return 0 if passed == len(tests) else 1


# ═══════════════════════════════════════════════════════════════
# 主函数
# ═══════════════════════════════════════════════════════════════
def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Somn AI - 超级智能体统一入口",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python run.py                           # 启动GUI (默认)
  python run.py --gui                     # 启动GUI
  python run.py --cli                     # 启动CLI交互模式
  python run.py --cli -q "增长策略"        # 单次查询
  python run.py --cli -q "分析" --industry ecommerce  # 带行业查询
  python run.py --health                  # 健康检查
  python run.py --status                  # 查看状态
  python run.py --solutions               # 列出解决方案
  python run.py --test                    # 模块测试
  python run.py --version                 # 版本信息
        """,
    )
    
    # 运行模式
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--gui", action="store_true", help="启动GUI模式 (默认)")
    mode_group.add_argument("--cli", action="store_true", help="启动CLI模式")
    
    # CLI参数
    parser.add_argument("-q", "--query", type=str, help="单次查询内容")
    parser.add_argument("--industry", type=str, default=None, help="指定行业上下文")
    
    # 功能命令
    parser.add_argument("--status", action="store_true", help="显示系统状态")
    parser.add_argument("--health", action="store_true", help="执行健康检查")
    parser.add_argument("--solutions", action="store_true", help="列出所有解决方案")
    parser.add_argument("--test", action="store_true", help="运行模块测试")
    parser.add_argument("--version", action="store_true", help="显示版本信息")
    
    args = parser.parse_args()
    
    # 版本信息
    if args.version:
        print_version()
        return 0
    
    # 打印横幅
    print_banner()
    
    # 确定运行模式
    if args.cli or args.query or args.status or args.health or args.solutions or args.test:
        # CLI模式
        return run_cli_mode(args)
    else:
        # GUI模式 (默认)
        return run_gui_mode()


if __name__ == "__main__":
    sys.exit(main())
