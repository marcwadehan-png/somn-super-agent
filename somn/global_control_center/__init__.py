"""
Somn 全局控制中心 - 全局管理和操作控制台
Global Control Center for Somn Project

支持三种模式:
- CLI: 命令行交互模式
- GUI: 图形界面模式
- WEB: Web浏览器访问模式

Author: Somn Development Team
Version: 1.0.0
"""

import argparse
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from smart_office_assistant.src import Somn
from .api_client import SomnAPIClient, get_api_client
from .managers.somn_connector import SomnConnector, get_somn_connector


def run_cli_mode():
    """命令行交互模式"""
    from .cli.console import run_cli_console
    run_cli_console()


def run_gui_mode():
    """图形界面模式"""
    from .gui.main_window import run_gui_app
    run_gui_app()


def run_web_mode(port: int = 8970):
    """Web浏览器模式"""
    from .web.app import run_web_app
    run_web_app(port=port)


def main():
    """主入口点"""
    parser = argparse.ArgumentParser(
        description='Somn 全局控制中心 - 全局管理和操作控制台',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python main_console.py --mode cli          # 命令行模式
  python main_console.py --mode gui          # 图形界面模式
  python main_console.py --mode web          # Web模式(默认端口8970)
  python main_console.py --mode web --port 8080  # 自定义端口

环境变量:
  SOMN_MODE     设置默认启动模式
  SOMN_PORT     设置Web模式默认端口
        """
    )
    
    parser.add_argument(
        '--mode', '-m',
        choices=['cli', 'gui', 'web'],
        default=os.environ.get('SOMN_MODE', 'cli'),
        help='启动模式: cli(命令行), gui(图形界面), web(浏览器) (默认: cli)'
    )
    
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=int(os.environ.get('SOMN_PORT', '8970')),
        help='Web模式端口号 (默认: 8970)'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='Somn Global Control Center v1.0.0'
    )
    
    parser.add_argument(
        '--info',
        action='store_true',
        help='显示系统信息'
    )
    
    args = parser.parse_args()
    
    # 显示系统信息
    if args.info:
        print_system_info()
        if args.mode == 'cli':
            return
    
    # 根据模式启动
    print(f"[Somn 控制中心] 启动模式: {args.mode.upper()}")
    
    try:
        if args.mode == 'cli':
            run_cli_mode()
        elif args.mode == 'gui':
            run_gui_mode()
        elif args.mode == 'web':
            run_web_mode(port=args.port)
    except KeyboardInterrupt:
        print("\n[控制中心] 用户中断，正在退出...")
        sys.exit(0)
    except Exception as e:
        print(f"[错误] 启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def print_system_info():
    """显示系统信息"""
    info = """
╔══════════════════════════════════════════════════════════════╗
║                    SOMN 全局控制中心                          ║
║                  Global Control Center                        ║
╠══════════════════════════════════════════════════════════════╣
║  版本: V1.0.0                                                   ║
║  项目: Somn 智能助手 V1.0                                      ║
║  架构: 神之架构最终完整版                                        ║
╠══════════════════════════════════════════════════════════════╣
║  系统规模:                                                      ║
║    - 顶层模块: 32 个                                             ║
║    - 智慧引擎: 45+ 个                                            ║
║    - 智慧学派: 35 个                                             ║
║    - Claw子代理: 776 个                                          ║
║    - 问题类型: 135 种                                            ║
╠══════════════════════════════════════════════════════════════╣
║  启动模式:                                                      ║
║    --mode cli  命令行交互模式                                    ║
║    --mode gui  图形界面模式                                      ║
║    --mode web  Web浏览器模式                                     ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(info)


if __name__ == '__main__':
    main()
