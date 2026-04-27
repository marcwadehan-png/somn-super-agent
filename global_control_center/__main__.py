"""
快速启动脚本
Quick Start Script
"""

import os
import sys

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


def main():
    """快速启动"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Somn 全局控制中心 - 快速启动')
    parser.add_argument('mode', choices=['cli', 'gui', 'web'], nargs='?', default='cli',
                       help='启动模式: cli, gui, web (默认: cli)')
    parser.add_argument('--port', '-p', type=int, default=8970,
                       help='Web模式端口 (默认: 8970)')
    parser.add_argument('--info', action='store_true',
                       help='显示系统信息')
    
    args = parser.parse_args()
    
    # 导入主模块
    from global_control_center import main as gcc_main
    
    if args.info:
        from global_control_center import print_system_info
        print_system_info()
        return
    
    # 设置模式
    os.environ['SOMN_MODE'] = args.mode
    if args.port:
        os.environ['SOMN_PORT'] = str(args.port)
    
    # 启动
    sys.argv = ['main_console.py', '--mode', args.mode]
    if args.port:
        sys.argv.extend(['--port', str(args.port)])
    
    gcc_main()


if __name__ == '__main__':
    main()
