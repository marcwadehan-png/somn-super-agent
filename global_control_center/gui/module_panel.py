"""
模块管理面板
Module Management Panel
"""

import tkinter as tk
from tkinter import ttk


class ModulePanel(ttk.Frame):
    """模块管理面板"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.modules = []
        self._create_widgets()
        self._load_modules()
        
    def _create_widgets(self):
        """创建组件"""
        # 工具栏
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="刷新", command=self._load_modules).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="启动", command=self._start_module).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="停止", command=self._stop_module).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="重启", command=self._restart_module).pack(side=tk.LEFT, padx=2)
        
        # 模块列表
        list_frame = ttk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("id", "name", "status", "load_time", "memory")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def _load_modules(self):
        """加载模块列表"""
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 添加模块数据
        modules = [
            ("core", "核心模块", "● 运行中", "0.12s", "128MB"),
            ("intelligence", "智慧层", "● 运行中", "0.25s", "256MB"),
            ("capability", "能力层", "● 运行中", "0.18s", "192MB"),
            ("application", "应用层", "● 运行中", "0.15s", "144MB"),
            ("data", "数据层", "● 运行中", "0.08s", "96MB"),
            ("network", "网络模块", "● 运行中", "0.05s", "64MB"),
            ("storage", "存储模块", "● 运行中", "0.10s", "112MB"),
            ("scheduler", "调度模块", "● 运行中", "0.09s", "88MB"),
        ]
        
        for m in modules:
            self.tree.insert("", tk.END, values=m)
            
    def _start_module(self):
        """启动选中模块"""
        selection = self.tree.selection()
        if selection:
            print("启动模块:", self.tree.item(selection[0])['values'][0])
            
    def _stop_module(self):
        """停止选中模块"""
        selection = self.tree.selection()
        if selection:
            print("停止模块:", self.tree.item(selection[0])['values'][0])
            
    def _restart_module(self):
        """重启选中模块"""
        selection = self.tree.selection()
        if selection:
            print("重启模块:", self.tree.item(selection[0])['values'][0])


if __name__ == '__main__':
    root = tk.Tk()
    ModulePanel(root).pack(fill=tk.BOTH, expand=True)
    root.mainloop()
