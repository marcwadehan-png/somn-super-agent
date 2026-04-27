"""
图形界面模块
Graphical User Interface Module
"""

import os
import sys

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


def run_gui_app():
    """运行GUI应用"""
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox
    except ImportError:
        print("[错误] tkinter 未安装，请使用 CLI 模式")
        print("提示: python main_console.py --mode cli")
        return
        
    from .main_window import SomnControlCenterGUI
    from .dashboard import DashboardFrame
    from .module_panel import ModulePanel
    from .engine_panel import EnginePanel
    from .claw_panel import ClawPanel
    from .config_panel import ConfigPanel
    
    # 创建主窗口
    root = tk.Tk()
    root.title("Somn 全局控制中心 v1.0.0")
    root.geometry("1200x800")
    root.minsize(1000, 600)
    
    # 设置主题
    style = ttk.Style()
    style.theme_use('clam')
    
    # 创建应用
    app = SomnControlCenterGUI(root)
    
    # 运行应用
    root.mainloop()


if __name__ == '__main__':
    run_gui_app()
