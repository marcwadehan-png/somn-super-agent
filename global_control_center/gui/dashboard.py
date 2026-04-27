"""
仪表板模块 - 系统状态可视化
Dashboard Module
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime


class DashboardFrame(ttk.Frame):
    """仪表板框架"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()
        
    def _create_widgets(self):
        """创建组件"""
        # 标题
        title = tk.Label(
            self,
            text="系统仪表板",
            font=("Microsoft YaHei", 18, "bold")
        )
        title.pack(pady=10)
        
        # 状态卡片区域
        self._create_status_cards()
        
    def _create_status_cards(self):
        """创建状态卡片"""
        cards_frame = tk.Frame(self)
        cards_frame.pack(fill=tk.X, padx=20, pady=10)
        
        cards_data = [
            ("总模块数", "32", "blue"),
            ("智慧引擎", "45+", "green"),
            ("Claw代理", "776", "purple"),
            ("活跃任务", "12", "red"),
        ]
        
        for title, value, color in cards_data:
            self._create_card(cards_frame, title, value, color)
            
    def _create_card(self, parent, title: str, value: str, color: str):
        """创建单个卡片"""
        card = tk.Frame(parent, bg=color, bd=2, relief=tk.RAISED)
        card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, ipady=10)
        
        tk.Label(
            card,
            text=title,
            font=("Microsoft YaHei", 10),
            fg="white",
            bg=color
        ).pack(pady=(10, 5))
        
        tk.Label(
            card,
            text=value,
            font=("Microsoft YaHei", 24, "bold"),
            fg="white",
            bg=color
        ).pack(pady=(0, 10))


if __name__ == '__main__':
    root = tk.Tk()
    DashboardFrame(root).pack(fill=tk.BOTH, expand=True)
    root.mainloop()
