# -*- coding: utf-8 -*-
"""示例插件 — 演示插件系统基本用法

当用户发送包含 "hello" 的消息时，追加一句问候。
"""

from somngui.core.plugin_manager import PluginHooks


class ExamplePlugin(PluginHooks):
    """示例插件"""

    def __init__(self):
        self._greeted = False

    def on_load(self, app_context):
        print(f"[ExamplePlugin] 已加载! main_window={type(app_context.get('main_window'))}")
        self._greeted = True

    def on_unload(self):
        print("[ExamplePlugin] 已卸载")

    def on_chat_message(self, role: str, content: str):
        """当用户消息包含 hello 时，追加一句"""
        if role == "user" and "hello" in content.lower():
            return " 👋 (ExamplePlugin: Hello from the plugin system!)"
        return None
