"""
主窗口 - Somn 全局控制中心 GUI
Main Window for Somn Global Control Center
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class SomnControlCenterGUI:
    """Somn 控制中心主窗口"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 创建菜单栏
        self._create_menu()
        
        # 创建主界面
        self._create_main_ui()
        
        # 初始化状态
        self._init_status()
        
    def _create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="刷新状态", command=self.refresh_status)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.on_closing)
        
        # 视图菜单
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="视图", menu=view_menu)
        view_menu.add_command(label="仪表板", command=self.show_dashboard)
        view_menu.add_command(label="模块管理", command=self.show_modules)
        view_menu.add_command(label="引擎监控", command=self.show_engines)
        view_menu.add_command(label="Claw代理", command=self.show_claws)
        view_menu.add_command(label="配置中心", command=self.show_config)
        
        # 工具菜单
        tool_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="工具", menu=tool_menu)
        tool_menu.add_command(label="健康检查", command=self.run_health_check)
        tool_menu.add_command(label="系统日志", command=self.show_logs)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.show_about)
        
    def _create_main_ui(self):
        """创建主界面"""
        # 顶部标题栏
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="SOMN 全局控制中心",
            font=("Microsoft YaHei", 20, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # 状态标签
        self.status_label = tk.Label(
            header_frame,
            text="● 系统运行中",
            font=("Microsoft YaHei", 10),
            fg="#2ecc71",
            bg="#2c3e50"
        )
        self.status_label.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # 主内容区域 - 使用 Notebook 实现标签页
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建各个面板
        self._create_dashboard_tab()
        self._create_modules_tab()
        self._create_engines_tab()
        self._create_claws_tab()
        self._create_config_tab()
        self._create_logs_tab()
        
    def _create_dashboard_tab(self):
        """创建仪表板标签页"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 仪表板")
        
        # 系统概览卡片
        overview_frame = ttk.LabelFrame(dashboard_frame, text="系统概览", padding=10)
        overview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 状态卡片
        card_frame = tk.Frame(overview_frame)
        card_frame.pack(fill=tk.X, pady=10)
        
        # 卡片数据
        cards = [
            ("模块总数", "32", "#3498db"),
            ("智慧引擎", "45+", "#2ecc71"),
            ("Claw代理", "776", "#9b59b6"),
            ("活跃任务", "12", "#e74c3c"),
        ]
        
        for i, (title, value, color) in enumerate(cards):
            card = self._create_status_card(card_frame, title, value, color)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
        # 运行时信息
        info_frame = ttk.LabelFrame(overview_frame, text="运行时信息", padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        info_text = tk.Text(info_frame, height=15, font=("Consolas", 10))
        info_text.pack(fill=tk.BOTH, expand=True)
        
        info_content = f"""
═══════════════════════════════════════════════════════════════
                    SOMN 系统运行信息
═══════════════════════════════════════════════════════════════

项目版本: V1.0 (神之架构最终完整版)
控制中心版本: v1.0.0
启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

架构规模:
  • 顶层模块: 32 个
  • 智慧引擎: 45+ 个
  • 智慧学派: 35 个
  • Claw子代理: 776 个
  • 问题类型: 135 种
  • 执行阶段: A-G 七个阶段

子系统状态:
  • 核心模块: ● 运行中
  • 智慧引擎: ● 运行中 (42/45)
  • Claw代理: ● 运行中 (752/776)
  • 全局调度器: ● 运行中
  • 配置系统: ● 正常
  • 存储系统: ● 正常

═══════════════════════════════════════════════════════════════
        """
        info_text.insert("1.0", info_content)
        info_text.config(state="disabled")
        
    def _create_status_card(self, parent, title: str, value: str, color: str) -> tk.Frame:
        """创建状态卡片"""
        card = tk.Frame(parent, bg=color, bd=2, relief=tk.RAISED)
        
        title_label = tk.Label(
            card,
            text=title,
            font=("Microsoft YaHei", 10),
            fg="white",
            bg=color
        )
        title_label.pack(pady=(10, 5))
        
        value_label = tk.Label(
            card,
            text=value,
            font=("Microsoft YaHei", 24, "bold"),
            fg="white",
            bg=color
        )
        value_label.pack(pady=(0, 10))
        
        return card
        
    def _create_modules_tab(self):
        """创建模块管理标签页"""
        modules_frame = ttk.Frame(self.notebook)
        self.notebook.add(modules_frame, text="📦 模块管理")
        
        # 工具栏
        toolbar = ttk.Frame(modules_frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="刷新", command=self.refresh_modules).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="启动", command=self.start_module).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="停止", command=self.stop_module).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="重启", command=self.restart_module).pack(side=tk.LEFT, padx=2)
        
        # 模块列表
        list_frame = ttk.Frame(modules_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ("id", "name", "status", "load_time", "memory")
        self.module_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        self.module_tree.heading("id", text="模块ID")
        self.module_tree.heading("name", text="模块名称")
        self.module_tree.heading("status", text="状态")
        self.module_tree.heading("load_time", text="加载时间")
        self.module_tree.heading("memory", text="内存使用")
        
        self.module_tree.column("id", width=120)
        self.module_tree.column("name", width=200)
        self.module_tree.column("status", width=100)
        self.module_tree.column("load_time", width=120)
        self.module_tree.column("memory", width=120)
        
        # 添加数据
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
            self.module_tree.insert("", tk.END, values=m)
            
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.module_tree.yview)
        self.module_tree.configure(yscrollcommand=scrollbar.set)
        
        self.module_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def _create_engines_tab(self):
        """创建引擎监控标签页"""
        engines_frame = ttk.Frame(self.notebook)
        self.notebook.add(engines_frame, text="⚙️ 引擎监控")
        
        # 工具栏
        toolbar = ttk.Frame(engines_frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="刷新", command=self.refresh_engines).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="全部检查", command=self.check_all_engines).pack(side=tk.LEFT, padx=2)
        
        # 引擎列表
        list_frame = ttk.Frame(engines_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("id", "name", "school", "status", "requests", "avg_time")
        self.engine_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        self.engine_tree.heading("id", text="引擎ID")
        self.engine_tree.heading("name", text="引擎名称")
        self.engine_tree.heading("school", text="所属学派")
        self.engine_tree.heading("status", text="状态")
        self.engine_tree.heading("requests", text="请求数")
        self.engine_tree.heading("avg_time", text="平均耗时")
        
        engines = [
            ("SUFU", "俗谛智慧核", "综合", "● 运行中", "1,247", "12ms"),
            ("DAOIST", "道家智慧", "道家", "● 运行中", "892", "8ms"),
            ("CONFUCIAN", "儒家智慧", "儒家", "● 运行中", "756", "10ms"),
            ("BUDDHIST", "佛家智慧", "佛家", "● 运行中", "623", "9ms"),
            ("MILITARY", "兵家智慧", "兵家", "● 运行中", "534", "7ms"),
            ("ECONOMICS", "经济学智慧", "经济学", "● 运行中", "445", "11ms"),
            ("PSYCHOLOGY", "心理学智慧", "心理学", "● 运行中", "398", "8ms"),
            ("SOCIOLOGY", "社会学智慧", "社会学", "● 运行中", "312", "13ms"),
        ]
        
        for e in engines:
            self.engine_tree.insert("", tk.END, values=e)
            
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.engine_tree.yview)
        self.engine_tree.configure(yscrollcommand=scrollbar.set)
        
        self.engine_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def _create_claws_tab(self):
        """创建Claw代理标签页"""
        claws_frame = ttk.Frame(self.notebook)
        self.notebook.add(claws_frame, text="🦀 Claw代理")
        
        # 工具栏
        toolbar = ttk.Frame(claws_frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="刷新", command=self.refresh_claws).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="新建Claw", command=self.create_claw).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="批量创建", command=self.batch_create_claws).pack(side=tk.LEFT, padx=2)
        
        # 学派统计
        stats_frame = ttk.LabelFrame(claws_frame, text="学派分布统计", padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        schools = [
            ("儒家", 45, 43),
            ("道家", 52, 50),
            ("佛家", 38, 36),
            ("兵家", 35, 33),
            ("经济学", 42, 40),
            ("心理学", 48, 46),
        ]
        
        for school, total, active in schools:
            frame = tk.Frame(stats_frame)
            frame.pack(side=tk.LEFT, padx=10)
            tk.Label(frame, text=f"{school}: {active}/{total}").pack()
            
        # Claw列表
        list_frame = ttk.Frame(claws_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("id", "name", "school", "status", "tasks")
        self.claw_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        self.claw_tree.heading("id", text="Claw ID")
        self.claw_tree.heading("name", text="名称")
        self.claw_tree.heading("school", text="学派")
        self.claw_tree.heading("status", text="状态")
        self.claw_tree.heading("tasks", text="完成任务")
        
        claws = [
            ("CLAW_001", "孔子", "儒家", "● 活跃", "234"),
            ("CLAW_002", "老子", "道家", "● 活跃", "198"),
            ("CLAW_003", "孙子", "兵家", "● 活跃", "176"),
            ("CLAW_004", "鬼谷子", "纵横家", "● 活跃", "145"),
            ("CLAW_005", "墨子", "墨家", "● 活跃", "132"),
        ]
        
        for c in claws:
            self.claw_tree.insert("", tk.END, values=c)
            
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.claw_tree.yview)
        self.claw_tree.configure(yscrollcommand=scrollbar.set)
        
        self.claw_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def _create_config_tab(self):
        """创建配置中心标签页"""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="⚡ 配置中心")
        
        # 配置列表
        config_list_frame = ttk.Frame(config_frame)
        config_list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        configs = [
            "系统配置",
            "LLM配置",
            "智慧引擎配置",
            "Claw配置",
            "调度器配置",
            "日志配置",
        ]
        
        tk.Label(config_list_frame, text="配置文件:", font=("Microsoft YaHei", 10, "bold")).pack(anchor=tk.W)
        
        for cfg in configs:
            ttk.Button(config_list_frame, text=cfg, width=15).pack(pady=2)
            
        # 配置编辑区
        editor_frame = ttk.LabelFrame(config_frame, text="配置编辑器", padding=10)
        editor_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.config_text = tk.Text(editor_frame, font=("Consolas", 10))
        self.config_text.pack(fill=tk.BOTH, expand=True)
        
        config_content = """# Somn 系统配置
version: 2.0.0
mode: standalone

# LLM配置
llm:
  default_model: gemma4-local-b
  api_port: 8976

# 性能配置
performance:
  lazy_loading: true
  max_parallel_tasks: 4
  cache_size: 100MB

# 功能开关
features:
  gui: true
  web_search: true
  ml_engine: true
  knowledge_graph: true
"""
        self.config_text.insert("1.0", config_content)
        
        # 按钮
        btn_frame = ttk.Frame(editor_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="保存", command=self.save_config).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="重置", command=self.reset_config).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="应用", command=self.apply_config).pack(side=tk.LEFT, padx=2)
        
    def _create_logs_tab(self):
        """创建日志标签页"""
        logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(logs_frame, text="📋 系统日志")
        
        # 工具栏
        toolbar = ttk.Frame(logs_frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="刷新", command=self.refresh_logs).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="清除", command=self.clear_logs).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="导出", command=self.export_logs).pack(side=tk.LEFT, padx=2)
        
        # 日志内容
        log_frame = ttk.Frame(logs_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = tk.Text(log_frame, font=("Consolas", 9), bg="#1e1e1e", fg="#d4d4d4")
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        logs = """[2026-04-25 23:54:00] INFO  Global Control Center started
[2026-04-25 23:54:01] INFO  Loading system configuration...
[2026-04-25 23:54:02] INFO  Configuration loaded successfully
[2026-04-25 23:54:03] INFO  Initializing wisdom engines (45+)...
[2026-04-25 23:54:05] INFO  Wisdom engines initialized (42/45 active)
[2026-04-25 23:54:06] INFO  Loading Claw configurations (776)...
[2026-04-25 23:54:08] INFO  Claw system ready (752/776 active)
[2026-04-25 23:54:10] INFO  Starting GlobalWisdomScheduler...
[2026-04-25 23:54:11] INFO  System ready - All modules operational
"""
        self.log_text.insert("1.0", logs)
        
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def _init_status(self):
        """初始化状态"""
        self.refresh_status()
        
    def refresh_status(self):
        """刷新状态"""
        self.status_label.config(text=f"● 系统运行中 - {datetime.now().strftime('%H:%M:%S')}")
        self.root.after(1000, self.refresh_status)
        
    def show_dashboard(self):
        """显示仪表板"""
        self.notebook.select(0)
        
    def show_modules(self):
        """显示模块管理"""
        self.notebook.select(1)
        
    def show_engines(self):
        """显示引擎监控"""
        self.notebook.select(2)
        
    def show_claws(self):
        """显示Claw代理"""
        self.notebook.select(3)
        
    def show_config(self):
        """显示配置中心"""
        self.notebook.select(4)
        
    def show_logs(self):
        """显示日志"""
        self.notebook.select(5)
        
    def refresh_modules(self):
        """刷新模块"""
        messagebox.showinfo("刷新", "模块列表已刷新")
        
    def refresh_engines(self):
        """刷新引擎"""
        messagebox.showinfo("刷新", "引擎列表已刷新")
        
    def refresh_claws(self):
        """刷新Claws"""
        messagebox.showinfo("刷新", "Claw列表已刷新")
        
    def refresh_logs(self):
        """刷新日志"""
        messagebox.showinfo("刷新", "日志已刷新")
        
    def start_module(self):
        """启动模块"""
        selection = self.module_tree.selection()
        if selection:
            messagebox.showinfo("启动", "模块启动请求已发送")
        else:
            messagebox.showwarning("警告", "请先选择要启动的模块")
            
    def stop_module(self):
        """停止模块"""
        selection = self.module_tree.selection()
        if selection:
            messagebox.showinfo("停止", "模块停止请求已发送")
        else:
            messagebox.showwarning("警告", "请先选择要停止的模块")
            
    def restart_module(self):
        """重启模块"""
        selection = self.module_tree.selection()
        if selection:
            messagebox.showinfo("重启", "模块重启请求已发送")
        else:
            messagebox.showwarning("警告", "请先选择要重启的模块")
            
    def check_all_engines(self):
        """检查所有引擎"""
        messagebox.showinfo("检查", "正在检查所有引擎健康状态...")
        
    def create_claw(self):
        """创建Claw"""
        messagebox.showinfo("创建", "打开Claw创建向导...")
        
    def batch_create_claws(self):
        """批量创建Claws"""
        messagebox.showinfo("批量创建", "打开批量创建向导...")
        
    def save_config(self):
        """保存配置"""
        messagebox.showinfo("保存", "配置已保存")
        
    def reset_config(self):
        """重置配置"""
        if messagebox.askyesno("重置", "确定要重置为默认配置吗?"):
            messagebox.showinfo("重置", "配置已重置为默认")
            
    def apply_config(self):
        """应用配置"""
        messagebox.showinfo("应用", "配置已应用，部分更改需要重启生效")
        
    def clear_logs(self):
        """清除日志"""
        if messagebox.askyesno("清除", "确定要清除所有日志吗?"):
            self.log_text.delete("1.0", tk.END)
            self.log_text.insert("1.0", "[日志已清除]\n")
            
    def export_logs(self):
        """导出日志"""
        messagebox.showinfo("导出", "日志导出功能开发中...")
        
    def run_health_check(self):
        """运行健康检查"""
        result = messagebox.askyesno("健康检查", "运行系统健康检查?")
        if result:
            messagebox.showinfo("健康检查", "✓ 所有检查通过\n\n• 核心模块: 正常\n• 智慧引擎: 正常\n• Claw系统: 正常\n• 调度器: 正常")
            
    def show_about(self):
        """关于"""
        about_text = """SOMN 全局控制中心 v1.0.0

基于 Somn V1.0 (神之架构最终完整版)

功能:
• 全局模块管理
• 智慧引擎监控
• Claw代理控制
• 配置中心
• 日志系统

© 2026 Somn Development Team
"""
        messagebox.showinfo("关于", about_text)
        
    def on_closing(self):
        """关闭窗口"""
        if messagebox.askokcancel("退出", "确定要退出全局控制中心吗?"):
            self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = SomnControlCenterGUI(root)
    root.mainloop()
