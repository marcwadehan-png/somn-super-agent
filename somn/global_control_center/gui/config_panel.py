"""
配置管理面板
Configuration Management Panel
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class ConfigPanel(ttk.Frame):
    """配置管理面板"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.current_config = None
        self.has_changes = False
        self._create_widgets()
        self._load_default_config()
        
    def _create_widgets(self):
        """创建组件"""
        # 左侧配置文件列表
        left_frame = ttk.Frame(self)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        tk.Label(
            left_frame,
            text="配置文件",
            font=("Microsoft YaHei", 10, "bold")
        ).pack(anchor=tk.W)
        
        self.config_listbox = tk.Listbox(left_frame, width=20, height=15)
        self.config_listbox.pack(pady=5)
        self.config_listbox.insert(0, "系统配置")
        self.config_listbox.insert(1, "LLM配置")
        self.config_listbox.insert(2, "智慧引擎配置")
        self.config_listbox.insert(3, "Claw配置")
        self.config_listbox.insert(4, "调度器配置")
        self.config_listbox.insert(5, "日志配置")
        self.config_listbox.bind('<<ListboxSelect>>', self._on_config_select)
        
        ttk.Button(left_frame, text="导入配置", command=self._import_config).pack(pady=2, fill=tk.X)
        ttk.Button(left_frame, text="导出配置", command=self._export_config).pack(pady=2, fill=tk.X)
        
        # 右侧编辑器
        right_frame = ttk.LabelFrame(self, text="配置编辑器", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 工具栏
        toolbar = ttk.Frame(right_frame)
        toolbar.pack(fill=tk.X, pady=5)
        
        ttk.Button(toolbar, text="保存", command=self._save_config).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="重置", command=self._reset_config).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="应用", command=self._apply_config).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="撤销", command=self._undo_changes).pack(side=tk.LEFT, padx=2)
        
        # 状态标签
        self.status_label = tk.Label(
            toolbar,
            text="未修改",
            font=("Consolas", 9),
            fg="gray"
        )
        self.status_label.pack(side=tk.RIGHT)
        
        # 文本编辑器
        editor_frame = ttk.Frame(right_frame)
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_editor = tk.Text(
            editor_frame,
            font=("Consolas", 10),
            wrap=tk.NONE,
            undo=True
        )
        
        # 滚动条
        y_scrollbar = ttk.Scrollbar(editor_frame, orient=tk.VERTICAL, command=self.text_editor.yview)
        x_scrollbar = ttk.Scrollbar(editor_frame, orient=tk.HORIZONTAL, command=self.text_editor.xview)
        
        self.text_editor.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        self.text_editor.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        
        editor_frame.grid_rowconfigure(0, weight=1)
        editor_frame.grid_columnconfigure(0, weight=1)
        
        # 绑定修改事件
        self.text_editor.bind('<<Modified>>', self._on_text_change)
        
    def _load_default_config(self):
        """加载默认配置"""
        default_config = """# Somn 系统配置文件
# 版本: V1.0.0

# ==================== 系统配置 ====================
system:
  version: "2.0.0"
  mode: "standalone"
  log_level: "INFO"
  debug: false

# ==================== LLM配置 ====================
llm:
  default_model: "gemma4-local-b"
  api_host: "localhost"
  api_port: 8976
  timeout: 30
  max_retries: 3

# ==================== 性能配置 ====================
performance:
  lazy_loading: true
  max_parallel_tasks: 4
  cache_size: "100MB"
  thread_pool_size: 8

# ==================== 功能开关 ====================
features:
  gui: true
  web_search: true
  ml_engine: true
  knowledge_graph: true
  wisdom_fusion: true
"""
        self.text_editor.insert("1.0", default_config)
        self.current_config = default_config
        
    def _on_config_select(self, event):
        """配置文件选中事件"""
        selection = self.config_listbox.curselection()
        if selection:
            config_name = self.config_listbox.get(selection[0])
            print(f"选中配置: {config_name}")
            
    def _on_text_change(self, event):
        """文本修改事件"""
        if self.text_editor.edit_modified():
            self.has_changes = True
            self.status_label.config(text="已修改 *", fg="red")
            self.text_editor.edit_modified(False)
            
    def _save_config(self):
        """保存配置"""
        if self.has_changes:
            print("保存配置...")
            self.has_changes = False
            self.status_label.config(text="已保存", fg="green")
            
    def _reset_config(self):
        """重置配置"""
        if messagebox.askyesno("重置", "确定要重置为默认配置吗?"):
            self._load_default_config()
            self.has_changes = False
            self.status_label.config(text="已重置", fg="orange")
            
    def _apply_config(self):
        """应用配置"""
        if self.has_changes:
            if messagebox.askyesno("应用", "应用配置可能需要重启系统，确定吗?"):
                print("应用配置...")
                self.has_changes = False
                self.status_label.config(text="已应用", fg="blue")
                
    def _undo_changes(self):
        """撤销更改"""
        try:
            self.text_editor.edit_undo()
        except tk.TclError:
            pass

    def _import_config(self):
        """导入配置"""
        filepath = filedialog.askopenfilename(
            title="选择配置文件",
            filetypes=[("YAML文件", "*.yaml *.yml"), ("所有文件", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_editor.delete("1.0", tk.END)
                self.text_editor.insert("1.0", content)
                self.current_config = content
                messagebox.showinfo("导入", "配置导入成功")
            except Exception as e:
                messagebox.showerror("错误", f"导入失败: {e}")
                
    def _export_config(self):
        """导出配置"""
        filepath = filedialog.asksaveasfilename(
            title="保存配置文件",
            defaultextension=".yaml",
            filetypes=[("YAML文件", "*.yaml"), ("所有文件", "*.*")]
        )
        if filepath:
            try:
                content = self.text_editor.get("1.0", tk.END)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("导出", "配置导出成功")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {e}")


if __name__ == '__main__':
    root = tk.Tk()
    ConfigPanel(root).pack(fill=tk.BOTH, expand=True)
    root.mainloop()
