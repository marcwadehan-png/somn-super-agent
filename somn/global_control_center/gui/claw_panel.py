"""
Claw代理管理面板
Claw Agent Management Panel
"""

import tkinter as tk
from tkinter import ttk


class ClawPanel(ttk.Frame):
    """Claw代理管理面板"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()
        self._load_claws()
        
    def _create_widgets(self):
        """创建组件"""
        # 工具栏
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="刷新", command=self._load_claws).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="新建", command=self._create_claw).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="批量创建", command=self._batch_create).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="删除", command=self._delete_claw).pack(side=tk.LEFT, padx=2)
        
        # 学派统计
        stats_frame = ttk.LabelFrame(self, text="学派分布统计", padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.school_labels = {}
        schools = [
            ("CONFUCIAN", "儒家", 45, 43),
            ("DAOIST", "道家", 52, 50),
            ("BUDDHIST", "佛家", 38, 36),
            ("MILITARY", "兵家", 35, 33),
            ("ECONOMICS", "经济学", 42, 40),
            ("PSYCHOLOGY", "心理学", 48, 46),
            ("SOCIOLOGY", "社会学", 30, 28),
            ("LAW", "法学", 28, 26),
        ]
        
        for school_id, name, total, active in schools:
            frame = tk.Frame(stats_frame, bg="#f0f0f0")
            frame.pack(side=tk.LEFT, padx=10, fill=tk.Y)
            
            tk.Label(
                frame,
                text=name,
                font=("Microsoft YaHei", 9, "bold"),
                bg="#f0f0f0"
            ).pack()
            
            label = tk.Label(
                frame,
                text=f"{active}/{total}",
                font=("Consolas", 10),
                fg="green",
                bg="#f0f0f0"
            )
            label.pack()
            self.school_labels[school_id] = label
            
        # Claw列表
        list_frame = ttk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("id", "name", "school", "status", "tasks", "created")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        col_names = ["Claw ID", "名称", "学派", "状态", "完成任务", "创建时间"]
        for col, name in zip(columns, col_names):
            self.tree.heading(col, text=name)
            
        self.tree.column("id", width=100)
        self.tree.column("name", width=120)
        self.tree.column("school", width=80)
        self.tree.column("status", width=80)
        self.tree.column("tasks", width=80)
        self.tree.column("created", width=120)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def _load_claws(self):
        """加载Claw列表"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        claws = [
            ("CLAW_001", "孔子", "儒家", "● 活跃", "234", "2026-01-15"),
            ("CLAW_002", "老子", "道家", "● 活跃", "198", "2026-01-15"),
            ("CLAW_003", "孙子", "兵家", "● 活跃", "176", "2026-01-16"),
            ("CLAW_004", "鬼谷子", "纵横家", "● 活跃", "145", "2026-01-17"),
            ("CLAW_005", "墨子", "墨家", "● 活跃", "132", "2026-01-18"),
            ("CLAW_006", "孟子", "儒家", "● 活跃", "128", "2026-01-19"),
            ("CLAW_007", "庄子", "道家", "● 活跃", "119", "2026-01-20"),
            ("CLAW_008", "荀子", "儒家", "● 活跃", "98", "2026-01-21"),
        ]
        
        for c in claws:
            self.tree.insert("", tk.END, values=c)
            
    def _create_claw(self):
        """创建Claw"""
        print("打开Claw创建对话框...")
        
    def _batch_create(self):
        """批量创建"""
        print("打开批量创建对话框...")
        
    def _delete_claw(self):
        """删除Claw"""
        selection = self.tree.selection()
        if selection:
            print("删除Claw:", self.tree.item(selection[0])['values'][0])


if __name__ == '__main__':
    root = tk.Tk()
    ClawPanel(root).pack(fill=tk.BOTH, expand=True)
    root.mainloop()
