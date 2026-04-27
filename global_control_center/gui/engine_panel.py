"""
引擎监控面板
Engine Monitoring Panel
"""

import tkinter as tk
from tkinter import ttk


class EnginePanel(ttk.Frame):
    """引擎监控面板"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()
        self._load_engines()
        
    def _create_widgets(self):
        """创建组件"""
        # 工具栏
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="刷新", command=self._load_engines).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="全部检查", command=self._check_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="刷新配置", command=self._reload_config).pack(side=tk.LEFT, padx=2)
        
        # 引擎列表
        list_frame = ttk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("id", "name", "school", "status", "requests", "avg_time")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        col_names = ["引擎ID", "引擎名称", "所属学派", "状态", "请求数", "平均耗时"]
        for col, name in zip(columns, col_names):
            self.tree.heading(col, text=name)
            
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def _load_engines(self):
        """加载引擎列表"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        engines = [
            ("SUFU", "俗谛智慧核", "综合", "● 运行中", "1,247", "12ms"),
            ("DAOIST", "道家智慧", "道家", "● 运行中", "892", "8ms"),
            ("CONFUCIAN", "儒家智慧", "儒家", "● 运行中", "756", "10ms"),
            ("BUDDHIST", "佛家智慧", "佛家", "● 运行中", "623", "9ms"),
            ("MILITARY", "兵家智慧", "兵家", "● 运行中", "534", "7ms"),
            ("ECONOMICS", "经济学智慧", "经济学", "● 运行中", "445", "11ms"),
            ("PSYCHOLOGY", "心理学智慧", "心理学", "● 运行中", "398", "8ms"),
            ("SOCIOLOGY", "社会学智慧", "社会学", "● 运行中", "312", "13ms"),
            ("LAW", "法学智慧", "法学", "● 运行中", "267", "9ms"),
            ("ANTHROPOLOGY", "人类学智慧", "人类学", "● 运行中", "198", "14ms"),
            ("COMMUNICATION", "传播学智慧", "传播学", "● 运行中", "156", "10ms"),
            ("POLITICAL", "政治经济学智慧", "政治经济学", "● 运行中", "134", "15ms"),
        ]
        
        for e in engines:
            self.tree.insert("", tk.END, values=e)
            
    def _check_all(self):
        """检查所有引擎"""
        print("检查所有引擎健康状态...")
        
    def _reload_config(self):
        """重新加载配置"""
        print("重新加载引擎配置...")


if __name__ == '__main__':
    root = tk.Tk()
    EnginePanel(root).pack(fill=tk.BOTH, expand=True)
    root.mainloop()
