# -*- coding: utf-8 -*-
"""
CodePilot - 自然语言可视化编程窗口
===================================
通过自然语言对话，对指定项目路径进行智能编程。

功能：
1. 配置大模型 API（OpenAI 兼容）
2. 选择项目文件夹，查看文件树
3. 自然语言输入编程指令
4. AI 分析项目结构，生成/修改代码
5. 代码预览与差异对比

依赖安装：
    pip install PyQt6 aiohttp requests loguru

用法：
    python codepilot.py
    或双击 "启动CodePilot.bat"
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import subprocess
import sys
import tempfile
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional

# 导入 LLM 配置管理器
try:
    from .llm_config import get_llm_config
except ImportError:
    from llm_config import get_llm_config

from PyQt6.QtCore import (
    Qt,
    QThread,
    QTimer,
    pyqtSignal,
    pyqtSlot,
    QSize,
    QMimeData,
)
from PyQt6.QtGui import QAction, QFont, QColor, QTextCursor
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSlider,
    QSpacerItem,
    QSplitter,
    QStackedWidget,
    QStatusBar,
    QTabWidget,
    QTextBrowser,
    QTextEdit,
    QToolBar,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
    QCompleter,
)
from loguru import logger

# ═══════════════════════════════════════════════════════════════════════════════
# 样式常量
# ═══════════════════════════════════════════════════════════════════════════════

_BRAND_PRIMARY = "#00d4aa"
_BRAND_PRIMARY_HOVER = "#00e4bb"
_BG_DARK = "#0d0d0d"
_BG_CARD = "#141414"
_BG_INPUT = "#1a1a1a"
_BORDER = "#2a2a2a"
_TEXT_PRIMARY = "#e5e5e5"
_TEXT_SECONDARY = "#888888"
_TEXT_MUTED = "#555555"
_ACCENT_ORANGE = "#ff9500"
_ACCENT_BLUE = "#0a84ff"
_ACCENT_RED = "#ff453a"
_ACCENT_GREEN = "#32d74b"
_SUCCESS = "#2ecc71"
_WARNING = "#f39c12"
_ERROR = "#e74c3c"

_MAIN_STYLE = f"""
QMainWindow {{
    background-color: {_BG_DARK};
    color: {_TEXT_PRIMARY};
    font-family: "Inter", "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
    font-size: 13px;
}}
QWidget {{
    background-color: transparent;
    color: {_TEXT_PRIMARY};
}}
QLabel {{
    color: {_TEXT_PRIMARY};
    background-color: transparent;
}}
QPushButton {{
    background-color: {_BG_INPUT};
    color: {_TEXT_PRIMARY};
    border: 1px solid {_BORDER};
    border-radius: 6px;
    padding: 8px 16px;
    min-height: 32px;
}}
QPushButton:hover {{
    background-color: #252525;
    border-color: #3a3a3a;
}}
QPushButton[primary="true"] {{
    background-color: {_BRAND_PRIMARY};
    border-color: {_BRAND_PRIMARY};
    color: #000000;
    font-weight: 600;
}}
QPushButton[primary="true"]:hover {{
    background-color: {_BRAND_PRIMARY_HOVER};
    border-color: {_BRAND_PRIMARY_HOVER};
}}
QPushButton[success="true"] {{
    background-color: {_SUCCESS};
    border-color: {_SUCCESS};
    color: #000000;
}}
QPushButton[danger="true"] {{
    background-color: {_ERROR};
    border-color: {_ERROR};
    color: #ffffff;
}}
QLineEdit, QTextEdit {{
    background-color: {_BG_INPUT};
    color: {_TEXT_PRIMARY};
    border: 1px solid {_BORDER};
    border-radius: 6px;
    padding: 8px 12px;
    selection-background-color: {_BRAND_PRIMARY};
}}
QLineEdit:focus, QTextEdit:focus {{
    border-color: {_BRAND_PRIMARY};
}}
QTreeWidget, QListWidget {{
    background-color: {_BG_CARD};
    color: {_TEXT_PRIMARY};
    border: 1px solid {_BORDER};
    border-radius: 6px;
    outline: none;
    padding: 4px;
}}
QTreeWidget::item:hover, QListWidget::item:hover {{
    background-color: #1f1f1f;
}}
QTreeWidget::item:selected, QListWidget::item:selected {{
    background-color: {_BRAND_PRIMARY}22;
    color: {_BRAND_PRIMARY};
}}
QTabWidget::pane {{
    border: 1px solid {_BORDER};
    border-radius: 6px;
    background-color: {_BG_CARD};
    padding: 8px;
}}
QTabBar::tab {{
    background-color: {_BG_INPUT};
    color: {_TEXT_SECONDARY};
    padding: 8px 16px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
}}
QTabBar::tab:selected {{
    background-color: {_BG_CARD};
    color: {_BRAND_PRIMARY};
    border-bottom: 2px solid {_BRAND_PRIMARY};
}}
QScrollBar:vertical {{
    background-color: transparent;
    width: 8px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background-color: {_BORDER};
    border-radius: 4px;
    min-height: 20px;
}}
QScrollBar::handle:vertical:hover {{
    background-color: #3a3a3a;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QStatusBar {{
    background-color: {_BG_CARD};
    color: {_TEXT_SECONDARY};
    border-top: 1px solid {_BORDER};
}}
QToolBar {{
    background-color: {_BG_CARD};
    border-bottom: 1px solid {_BORDER};
    spacing: 4px;
    padding: 4px;
}}
QMenu {{
    background-color: {_BG_CARD};
    color: {_TEXT_PRIMARY};
    border: 1px solid {_BORDER};
    border-radius: 6px;
    padding: 4px;
}}
QMenu::item:selected {{
    background-color: {_BRAND_PRIMARY}22;
    color: {_BRAND_PRIMARY};
}}
QComboBox {{
    background-color: {_BG_INPUT};
    color: {_TEXT_PRIMARY};
    border: 1px solid {_BORDER};
    border-radius: 4px;
    padding: 6px 10px;
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox QAbstractItemView {{
    background-color: {_BG_CARD};
    color: {_TEXT_PRIMARY};
    border: 1px solid {_BORDER};
    selection-background-color: {_BRAND_PRIMARY}44;
}}
QProgressBar {{
    background-color: {_BG_INPUT};
    border: 1px solid {_BORDER};
    border-radius: 4px;
    text-align: center;
    color: {_TEXT_PRIMARY};
}}
QProgressBar::chunk {{
    background-color: {_BRAND_PRIMARY};
    border-radius: 3px;
}}
"""

_CODE_STYLE = f"""
QTextEdit#codeView {{
    background-color: #0d0d0d;
    color: #d4d4d4;
    font-family: "JetBrains Mono", "Cascadia Code", "Fira Code", Consolas, monospace;
    font-size: 13px;
    line-height: 1.5;
    padding: 12px;
    border: 1px solid {_BORDER};
    border-radius: 6px;
}}
"""

_CARD_STYLE = f"""
QFrame.card {{
    background-color: {_BG_CARD};
    border: 1px solid {_BORDER};
    border-radius: 8px;
    padding: 12px;
}}
"""


# ═══════════════════════════════════════════════════════════════════════════════
# 后端 API 线程
# ═══════════════════════════════════════════════════════════════════════════════

class APIClient(QThread):
    """异步 API 调用线程"""
    response_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    thinking = pyqtSignal(str)
    progress = pyqtSignal(int, str)

    def __init__(self, api_url: str, api_key: str, model: str = "gpt-4"):
        super().__init__()
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    async def _call_api(self, messages: list, temperature: float = 0.7):
        """调用大模型 API"""
        import aiohttp

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": True,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=120),
            ) as resp:
                if resp.status != 200:
                    error_text = await resp.text()
                    raise Exception(f"API 错误 {resp.status}: {error_text}")

                full_content = ""
                async for line in resp.content:
                    line = line.decode("utf-8").strip()
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            obj = json.loads(data)
                            delta = obj["choices"][0]["delta"].get("content", "")
                            if delta:
                                full_content += delta
                                self.thinking.emit(delta)
                        except json.JSONDecodeError:
                            continue

                return full_content

    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            # 等待调用
            loop.run_until_complete(asyncio.sleep(0))
            loop.close()
        except Exception as e:
            self.error_occurred.emit(str(e))


# ═══════════════════════════════════════════════════════════════════════════════
# 代码生成器
# ═══════════════════════════════════════════════════════════════════════════════

class CodeGenerator:
    """代码生成核心引擎"""

    SYSTEM_PROMPT = """你是一个专业的 AI 编程助手。

职责：
1. 分析用户自然语言需求
2. 理解目标项目的代码结构
3. 生成符合项目风格的代码
4. 提供完整的文件修改方案

输出格式（严格遵循）：
```
## 意图分析
[简短描述用户想要做什么]

## 修改文件
- **文件路径**: 要修改的文件
  - 操作: create/update/delete
  - 语言: python/js/typescript 等

## 代码内容
```[语言]
[完整代码内容]
```
"""

    def __init__(self, api_url: str, api_key: str, model: str):
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    async def generate(self, user_request: str, project_structure: str, 
                       selected_file: str = None, context: str = "") -> str:
        """生成代码"""
        import aiohttp

        user_content = f"""## 用户需求
{user_request}

## 项目结构
```
{project_structure}
```
"""

        if selected_file:
            user_content += f"\n## 当前选中文件\n```\n{selected_file}\n```\n"

        if context:
            user_content += f"\n## 上下文信息\n{context}\n"

        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ]

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "stream": True,
        }

        collected = []

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=120),
            ) as resp:
                if resp.status != 200:
                    error_text = await resp.text()
                    raise Exception(f"API 错误 {resp.status}: {error_text}")

                async for line in resp.content:
                    line_text = line.decode("utf-8").strip()
                    if line_text.startswith("data: "):
                        data = line_text[6:]
                        if data == "[DONE]":
                            break
                        try:
                            obj = json.loads(data)
                            delta = obj["choices"][0]["delta"].get("content", "")
                            if delta:
                                collected.append(delta)
                        except json.JSONDecodeError:
                            continue

        return "".join(collected)

    def parse_code_response(self, response: str) -> dict:
        """解析 AI 返回的内容，提取文件和代码"""
        result = {
            "intent": "",
            "files": [],
            "summary": response,
        }

        # 提取意图分析
        intent_match = re.search(r"## 意图分析\s*\n(.*?)(?=##|\Z)", response, re.DOTALL)
        if intent_match:
            result["intent"] = intent_match.group(1).strip()

        # 提取代码块
        code_blocks = re.findall(
            r"(?:```(\w+)\n)?```[^\n]*\n(.*?)```",
            response,
            re.DOTALL,
        )

        for lang, code in code_blocks:
            if code.strip():
                result["files"].append({
                    "language": lang or "text",
                    "code": code.strip(),
                })

        return result


# ═══════════════════════════════════════════════════════════════════════════════
# LLM 配置对话框
# ═══════════════════════════════════════════════════════════════════════════════

class LLMConfigDialog(QDialog):
    """LLM API 配置对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("配置大模型")
        self.setMinimumSize(500, 400)
        self._init_ui()
        self._load_config()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # API 基础地址
        layout.addWidget(QLabel("API 地址"))
        # 预设快捷选择
        preset_layout = QHBoxLayout()
        self.api_preset_combo = QComboBox()
        self.api_preset_combo.addItems([
            "自定义 URL",
            "OpenAI (https://api.openai.com/v1)",
            "阿里通义百炼 (https://dashscope.aliyuncs.com/compatible-mode/v1)",
            "百度文心 (https://qianfan.baidubce.com/v2)",
            "智谱 GLM (https://open.bigmodel.cn/api/paas/v4)",
            "DeepSeek (https://api.deepseek.com/v1)",
            "MiniMax (https://api.minimax.chat/v1)",
            "讯飞星火 (https://spark-api.xf-yun.com/v3.5)",
            "Kimi (https://api.moonshot.cn/v1)",
            "豆包火山引擎 (https://ark.cn-beijing.volces.com/api/v3)",
            "阶跃星辰 (https://api.stepfun.com/v1)",
            "零一万物 (https://api.lingyiwanwu.com/v1)",
            "商汤 (https://api.sensetime.com/v1)",
            "腾讯混元 (https://hunyuan.cloud.tencent.com/v3)",
        ])
        self.api_preset_combo.currentIndexChanged.connect(self._on_api_preset_changed)
        preset_layout.addWidget(self.api_preset_combo)
        use_btn = QPushButton("应用")
        use_btn.clicked.connect(lambda: self._on_api_preset_changed(self.api_preset_combo.currentIndex()))
        preset_layout.addWidget(use_btn)
        layout.addLayout(preset_layout)

        self.api_url_input = QLineEdit()
        self.api_url_input.setPlaceholderText("选择上方预设或输入自定义地址...")
        layout.addWidget(self.api_url_input)

        # API Key
        layout.addWidget(QLabel("API Key"))
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setPlaceholderText("sk-...")
        layout.addWidget(self.api_key_input)

        # 模型选择
        layout.addWidget(QLabel("模型"))
        self.model_combo = QComboBox()
        # 按厂商分组（基于 2025-2026 实际 API 模型名）
        self.model_combo.addItems([
            # === 国际大厂 ===
            # OpenAI
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "gpt-4",
            "chatgpt-4o-latest",
            # Anthropic
            "claude-3-5-sonnet-latest",
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-latest",
            "claude-3-opus-latest",
            # === 国内主流 ===
            # 阿里通义千问
            "qwen-plus",
            "qwen-plus-2025-01-25",
            "qwen-turbo",
            "qwen-turbo-2025-01-25",
            "qwen-max",
            "qwen-max-2025-01-25",
            "qwen-long",
            "qwen-coder-turbo",
            "qwen-coder-turbo-2025-01-25",
            "qwen2.5-72b-instruct",
            # 百度文心一言
            "ernie-bot",
            "ernie-bot-4",
            "ernie-bot-8k",
            "ernie-bot- Turbo",
            "ernie-speed-128k",
            "ernie-speed-32k",
            "ernie-lite-8k",
            "ernie-lite-4k",
            # 智谱 GLM
            "glm-4",
            "glm-4-plus",
            "glm-4-0520",
            "glm-4-air",
            "glm-4-airx",
            "glm-4-long",
            "glm-4-flashx",
            "glm-4-flash",
            "glm-4.7",
            "glm-4.7-flash",
            "glm-3-turbo",
            # 科大讯飞星火
            "spark-4.0",
            "spark-4.0-ultra",
            "spark-3.5",
            "spark-3.5-pro",
            "spark-3.5-ultra",
            "spark-x2-flash",
            # MiniMax（最新）
            "MiniMax-Text-01",
            "MiniMax-VL-01",
            "abab6.5s",
            "abab6.5g",
            "abab5.5s",
            # DeepSeek
            "deepseek-chat",
            "deepseek-chat-v2",
            "deepseek-chat-v3",
            "deepseek-coder",
            "deepseek-coder-v2",
            "deepseek-math",
            "deepseek-reasoner",
            # 字节豆包
            "doubao-pro-32k",
            "doubao-pro-128k",
            "doubao-lite-32k",
            "doubao-lite-4k",
            "doubao-auto",
            # 月之暗面 Kimi
            "kimi-k2.6",
            "kimi-k2.5",
            "moonshot-v1-8k",
            "moonshot-v1-32k",
            "moonshot-v1-128k",
            # 阶跃星辰
            "step-1v",
            "step-1",
            "step-2",
            # 零一万物
            "yi-large",
            "yi-medium",
            "yi-spark",
            # 商汤日日新
            "SenseChat",
            "SenseChat-5",
            # 腾讯混元
            "hunyuan",
            "hunyuan-pro",
            "hunyuan-standard",
        ])
        layout.addWidget(self.model_combo)

        # 温度滑块
        layout.addWidget(QLabel("创造性 (Temperature)"))
        temp_layout = QHBoxLayout()
        self.temp_slider = QSlider(Qt.Orientation.Horizontal)
        self.temp_slider.setRange(0, 100)
        self.temp_slider.setValue(70)
        self.temp_label = QLabel("0.70")
        self.temp_slider.valueChanged.connect(
            lambda v: self.temp_label.setText(f"{v/100:.2f}")
        )
        temp_layout.addWidget(self.temp_slider)
        temp_layout.addWidget(self.temp_label)
        layout.addLayout(temp_layout)

        layout.addStretch()

        # 按钮
        btn_layout = QHBoxLayout()
        test_btn = QPushButton("测试连接")
        test_btn.clicked.connect(self._test_connection)
        save_btn = QPushButton("保存")
        save_btn.setProperty("primary", True)
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(test_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def _on_api_preset_changed(self, index: int):
        """处理 API 预设选择"""
        if index == 0:
            return  # 自定义，不做处理
        preset_text = self.api_preset_combo.currentText()
        # 提取括号中的 URL
        import re
        match = re.search(r"\((.+)\)", preset_text)
        if match:
            url = match.group(1)
            self.api_url_input.setText(url)

    def _load_config(self):
        """加载已保存的配置 - 优先使用 Somn 配置"""
        # 优先使用 Somn 统一配置
        llm_cfg = get_llm_config()
        if llm_cfg.is_configured():
            config = llm_cfg.get_config()
            self.api_url_input.setText(config.get("api_url", ""))
            self.api_key_input.setText(config.get("api_key", ""))
            model = config.get("model", "")
            idx = self.model_combo.findText(model)
            if idx >= 0:
                self.model_combo.setCurrentIndex(idx)
            self.temp_slider.setValue(int(config.get("temperature", 0.7) * 100))
            return

        # 回退到本地配置文件
        config_path = Path.home() / ".codepilot" / "config.json"
        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = json.load(f)
                self.api_url_input.setText(config.get("api_url", ""))
                self.api_key_input.setText(config.get("api_key", ""))
                model = config.get("model", "gpt-4o")
                idx = self.model_combo.findText(model)
                if idx >= 0:
                    self.model_combo.setCurrentIndex(idx)
                self.temp_slider.setValue(int(config.get("temperature", 0.7) * 100))
            except Exception:
                pass

    def _test_connection(self):
        """测试 API 连接"""
        api_url = self.api_url_input.text().strip()
        api_key = self.api_key_input.text().strip()
        model = self.model_combo.currentText()

        if not api_url or not api_key:
            QMessageBox.warning(self, "提示", "请填写完整的 API 信息")
            return

        self._test_worker = _TestConnectionWorker(api_url, api_key, model)
        self._test_worker.result.connect(self._on_test_result)
        self._test_worker.error.connect(self._on_test_error)
        self._test_worker.start()

    @pyqtSlot(bool, str)
    def _on_test_result(self, success: bool, message: str):
        if success:
            QMessageBox.information(self, "成功", f"连接测试通过！\n{message}")
        else:
            QMessageBox.warning(self, "失败", f"连接失败：\n{message}")

    @pyqtSlot(str)
    def _on_test_error(self, error: str):
        QMessageBox.critical(self, "错误", f"连接异常：\n{error}")

    def get_config(self) -> dict:
        """获取配置"""
        return {
            "api_url": self.api_url_input.text().strip(),
            "api_key": self.api_key_input.text().strip(),
            "model": self.model_combo.currentText(),
            "temperature": self.temp_slider.value() / 100,
        }

    def save_config(self):
        """保存配置"""
        config = self.get_config()
        config_path = Path.home() / ".codepilot" / "config.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)


class _TestConnectionWorker(QThread):
    """测试连接后台线程"""
    result = pyqtSignal(bool, str)
    error = pyqtSignal(str)

    def __init__(self, api_url: str, api_key: str, model: str):
        super().__init__()
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    def run(self):
        import aiohttp
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": "Hi"}],
                "max_tokens": 5,
            }
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(asyncio.sleep(0))
            loop.close()

            # 同步方式测试
            import requests
            resp = requests.post(
                f"{self.api_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30,
            )
            if resp.status_code == 200:
                self.result.emit(True, f"模型 {self.model} 响应正常")
            else:
                self.result.emit(False, f"状态码: {resp.status_code}")
        except Exception as e:
            self.error.emit(str(e))


# ═══════════════════════════════════════════════════════════════════════════════
# 文件树组件
# ═══════════════════════════════════════════════════════════════════════════════

class FileTreeWidget(QWidget):
    """项目文件树组件"""

    file_selected = pyqtSignal(str)  # 选中文件路径

    # 文件类型图标映射
    FILE_ICONS = {
        ".py": "🐍",
        ".js": "📜",
        ".ts": "📘",
        ".tsx": "📘",
        ".jsx": "📦",
        ".json": "📋",
        ".md": "📝",
        ".txt": "📄",
        ".yaml": "⚙️",
        ".yml": "⚙️",
        ".toml": "⚙️",
        ".xml": "📄",
        ".html": "🌐",
        ".css": "🎨",
        ".scss": "🎨",
        ".png": "🖼️",
        ".jpg": "🖼️",
        ".jpeg": "🖼️",
        ".gif": "🖼️",
        ".svg": "🖼️",
        ".vue": "💚",
        ".go": "🐹",
        ".rs": "🦀",
        ".java": "☕",
        ".c": "⚡",
        ".cpp": "⚡",
        ".h": "⚡",
        ".hpp": "⚡",
        ".sh": "🐚",
        ".bat": "📦",
        ".ps1": "💠",
        ".sql": "🗃️",
        ".env": "🔐",
        ".gitignore": "🙈",
        "folder": "📁",
        "default": "📄",
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project_path: Optional[Path] = None
        self._init_ui()
        self._apply_styles()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 工具栏
        toolbar = QHBoxLayout()
        self.path_label = QLabel("未选择项目")
        self.path_label.setStyleSheet(f"color: {_TEXT_SECONDARY}; font-size: 12px;")
        toolbar.addWidget(self.path_label)
        toolbar.addStretch()

        open_btn = QPushButton("📂 打开")
        open_btn.setFixedHeight(28)
        open_btn.clicked.connect(self._open_folder)
        toolbar.addWidget(open_btn)

        refresh_btn = QPushButton("🔄")
        refresh_btn.setFixedSize(28, 28)
        refresh_btn.clicked.connect(self._refresh_tree)
        toolbar.addWidget(refresh_btn)

        layout.addLayout(toolbar)

        # 文件树
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setColumnCount(1)
        self.tree.itemClicked.connect(self._on_item_clicked)
        self.tree.itemDoubleClicked.connect(self._on_item_double_clicked)
        layout.addWidget(self.tree)

    def _apply_styles(self):
        self.setStyleSheet(_MAIN_STYLE)

    def _get_icon(self, name: str, is_folder: bool = False) -> str:
        if is_folder:
            return self.FILE_ICONS["folder"]
        ext = Path(name).suffix.lower()
        return self.FILE_ICONS.get(ext, self.FILE_ICONS["default"])

    def _open_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "选择项目文件夹", str(Path.home()),
        )
        if folder:
            self.set_project_path(Path(folder))

    def set_project_path(self, path: Path):
        """设置项目路径"""
        self.project_path = path
        self.path_label.setText(str(path))
        self._refresh_tree()

    def _refresh_tree(self):
        """刷新文件树"""
        self.tree.clear()
        if not self.project_path or not self.project_path.exists():
            return

        root = self._build_tree(self.project_path)
        self.tree.addTopLevelItem(root)
        root.setExpanded(True)

        # 展开第一层
        for i in range(root.childCount()):
            root.child(i).setExpanded(True)

    def _build_tree(self, path: Path, max_depth: int = 4) -> QTreeWidgetItem:
        """递归构建树"""
        is_dir = path.is_dir()
        name = path.name

        item = QTreeWidgetItem([f"{self._get_icon(name, is_dir)} {name}"])
        item.setData(0, Qt.ItemDataRole.UserRole, str(path))

        if is_dir and path.parts != ():
            # 排除某些目录
            exclude = {".git", "__pycache__", "node_modules", ".venv", "venv",
                       ".idea", ".vscode", "dist", "build", ".cache"}
            if name not in exclude and path.stat().st_size < 10_000_000:
                children = []
                try:
                    for child in sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
                        if child.name not in exclude:
                            child_item = self._build_tree(child, max_depth - 1)
                            if child_item:
                                children.append(child_item)
                except PermissionError:
                    pass

                # 限制子项数量
                for i, child in enumerate(children[:100]):
                    item.addChild(child)

                # 如果还有更多
                if len(children) > 100:
                    more_item = QTreeWidgetItem([f"... 还有 {len(children) - 100} 个文件"])
                    more_item.setFlags(more_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                    item.addChild(more_item)

        return item

    def _on_item_clicked(self, item, column):
        path = item.data(0, Qt.ItemDataRole.UserRole)
        if path:
            self.file_selected.emit(path)

    def _on_item_double_clicked(self, item, column):
        path = item.data(0, Qt.ItemDataRole.UserRole)
        if path and Path(path).is_file():
            # 读取文件内容并发送信号
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                self.file_selected.emit(path)
            except Exception:
                pass

    def get_structure_str(self) -> str:
        """获取项目结构字符串"""
        if not self.project_path:
            return ""

        lines = []
        for p in sorted(self.project_path.rglob("*")):
            if any(ex in p.parts for ex in [".git", "__pycache__", "node_modules", ".venv"]):
                continue
            rel = p.relative_to(self.project_path)
            indent = "  " * (len(rel.parts) - 1)
            icon = self._get_icon(p.name, p.is_dir())
            lines.append(f"{indent}{icon} {rel.name if p.is_file() else rel.name + '/'}")

        return "\n".join(lines[:500])  # 限制大小


# ═══════════════════════════════════════════════════════════════════════════════
# 代码预览组件
# ═══════════════════════════════════════════════════════════════════════════════

class CodePreviewWidget(QWidget):
    """代码预览组件"""

    apply_requested = pyqtSignal(str, str)  # file_path, content

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_file = None
        self._init_ui()
        self._apply_styles()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 工具栏
        toolbar = QHBoxLayout()
        self.file_label = QLabel("代码预览")
        self.file_label.setStyleSheet(f"color: {_TEXT_SECONDARY}; font-size: 12px;")
        toolbar.addWidget(self.file_label)
        toolbar.addStretch()

        self.apply_btn = QPushButton("✓ 应用到文件")
        self.apply_btn.setProperty("primary", True)
        self.apply_btn.clicked.connect(self._apply_changes)
        self.apply_btn.setEnabled(False)
        toolbar.addWidget(self.apply_btn)

        copy_btn = QPushButton("📋 复制")
        copy_btn.clicked.connect(self._copy_code)
        toolbar.addWidget(copy_btn)

        layout.addLayout(toolbar)

        # 代码编辑器
        self.code_edit = QTextEdit()
        self.code_edit.setObjectName("codeView")
        self.code_edit.setReadOnly(False)
        self.code_edit.setFont(QFont("Cascadia Code", 12))
        layout.addWidget(self.code_edit)

        # 差异视图区域
        self.diff_area = QTextBrowser()
        self.diff_area.setVisible(False)
        layout.addWidget(self.diff_area)

    def _apply_styles(self):
        self.setStyleSheet(_MAIN_STYLE + _CODE_STYLE)

    def set_content(self, content: str, file_path: str = None, language: str = "python"):
        """设置代码内容"""
        self.current_file = file_path
        self.code_edit.setPlainText(content)

        # 高亮语法
        self._highlight_code(content, language)

        if file_path:
            self.file_label.setText(f"📄 {file_path}")
            self.apply_btn.setEnabled(True)
        else:
            self.file_label.setText("新建文件")
            self.apply_btn.setEnabled(False)

    def _highlight_code(self, code: str, language: str):
        """简单语法高亮"""
        # 使用 QTextCharFormat 进行基本高亮
        cursor = self.code_edit.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)

        # 基础样式
        fmt = self.code_edit.currentCharFormat()
        fmt.setFontFamily("Cascadia Code")
        fmt.setFontPointSize(12)
        self.code_edit.setCurrentCharFormat(fmt)

    def _apply_changes(self):
        """应用修改到文件"""
        if not self.current_file:
            return

        content = self.code_edit.toPlainText()

        # 选择保存路径
        if self.current_file == "NEW_FILE":
            save_path, _ = QFileDialog.getSaveFileName(
                self, "保存文件", str(Path.home()),
            )
            if not save_path:
                return
        else:
            save_path = self.current_file

        try:
            # 备份
            bak_path = save_path + ".bak"
            if Path(save_path).exists():
                Path(save_path).rename(bak_path)

            with open(save_path, "w", encoding="utf-8") as f:
                f.write(content)

            QMessageBox.information(
                self, "成功",
                f"文件已保存\n{save_path}\n\n备份: {bak_path}"
            )
            self.apply_btn.setEnabled(False)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败:\n{str(e)}")

    def _copy_code(self):
        """复制代码"""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.code_edit.toPlainText())
        QMessageBox.information(self, "提示", "代码已复制到剪贴板")


# ═══════════════════════════════════════════════════════════════════════════════
# AI 对话线程
# ═══════════════════════════════════════════════════════════════════════════════

class AIWorker(QThread):
    """AI 代码生成工作线程"""
    chunk_ready = pyqtSignal(str)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    progress = pyqtSignal(int, str)

    def __init__(self, generator: CodeGenerator, request: str,
                 project_structure: str, selected_file: str = None,
                 file_content: str = ""):
        super().__init__()
        self.generator = generator
        self.request = request
        self.project_structure = project_structure
        self.selected_file = selected_file
        self.file_content = file_content

    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            context = ""
            if self.file_content:
                context = f"\n\n## 当前文件内容\n```\n{self.file_content[:3000]}\n```\n"

            result = loop.run_until_complete(
                self.generator.generate(
                    self.request,
                    self.project_structure,
                    self.selected_file,
                    context,
                )
            )
            loop.close()
            self.finished.emit(result)
        except Exception as e:
            try:
                loop.close()
            except Exception:
                pass
            self.error.emit(str(e))


# ═══════════════════════════════════════════════════════════════════════════════
# 主窗口
# ═══════════════════════════════════════════════════════════════════════════════

class CodePilotWindow(QMainWindow):
    """CodePilot 主窗口"""

    def __init__(self):
        super().__init__()
        self.config = self._load_config()
        self.generator = None
        self.ai_worker = None
        self.pending_code_blocks = []
        self.current_code = ""

        self._init_ui()
        self._apply_styles()
        self._setup_connections()

    def _init_ui(self):
        self.setWindowTitle("CodePilot - 自然语言编程助手")
        self.setMinimumSize(1400, 900)

        # 中央部件
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        # 左侧：文件树 + 配置
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        # 文件浏览器
        self.file_tree = FileTreeWidget()
        self.file_tree.setMinimumWidth(280)
        self.file_tree.setMaximumWidth(400)
        left_layout.addWidget(self.file_tree, 1)

        # LLM 配置按钮
        config_btn = QPushButton("⚙️ 大模型配置")
        config_btn.clicked.connect(self._show_llm_config)
        left_layout.addWidget(config_btn)

        main_layout.addWidget(left_panel, 0)

        # 中间：对话区
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)

        # 输入区
        input_frame = QFrame()
        input_frame.setObjectName("inputFrame")
        input_layout = QVBoxLayout(input_frame)

        prompt_label = QLabel("💬 输入你的编程指令")
        prompt_label.setStyleSheet("font-weight: 600; color: #e5e5e5;")
        input_layout.addWidget(prompt_label)

        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText(
            "例如：在 src/utils 目录下创建一个日志工具模块...\n"
            "或者：在现有的 user.py 中添加一个用户验证函数..."
        )
        self.prompt_input.setMaximumHeight(120)
        self.prompt_input.setMinimumHeight(80)
        input_layout.addWidget(self.prompt_input)

        # 操作按钮
        btn_layout = QHBoxLayout()
        self.send_btn = QPushButton("🚀 发送请求")
        self.send_btn.setProperty("primary", True)
        self.send_btn.clicked.connect(self._send_request)
        btn_layout.addWidget(self.send_btn)

        stop_btn = QPushButton("⏹ 停止")
        stop_btn.clicked.connect(self._stop_generation)
        btn_layout.addWidget(stop_btn)

        btn_layout.addStretch()

        clear_btn = QPushButton("🗑 清空")
        clear_btn.clicked.connect(self._clear_chat)
        btn_layout.addWidget(clear_btn)

        input_layout.addLayout(btn_layout)

        center_layout.addWidget(input_frame, 0)

        # AI 输出区
        self.output_browser = QTextBrowser()
        self.output_browser.setFont(QFont("Cascadia Code", 12))
        self.output_browser.setOpenExternalLinks(True)
        center_layout.addWidget(self.output_browser, 1)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        center_layout.addWidget(self.progress_bar)

        main_layout.addWidget(center_panel, 1)

        # 右侧：代码预览
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        self.code_preview = CodePreviewWidget()
        right_layout.addWidget(self.code_preview, 1)

        main_layout.addWidget(right_panel, 0)

        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self._update_status()

    def _apply_styles(self):
        self.setStyleSheet(_MAIN_STYLE)

    def _setup_connections(self):
        """设置信号连接"""
        self.file_tree.file_selected.connect(self._on_file_selected)
        self.output_browser.copyAvailable.connect(self._on_copy_available)

    def _load_config(self) -> dict:
        """加载配置 - 复用 Somn 云端大模型配置"""
        llm_cfg = get_llm_config()
        if llm_cfg.is_configured():
            return llm_cfg.get_config()
        # 回退到本地配置文件
        config_path = Path.home() / ".codepilot" / "config.json"
        if config_path.exists():
            try:
                with open(config_path) as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "api_url": "https://api.minimax.chat/v1",
            "api_key": "",
            "model": "MiniMax-Text-01",
            "temperature": 0.7,
        }

    def _show_llm_config(self):
        """显示 LLM 配置对话框"""
        dialog = LLMConfigDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            config = dialog.get_config()
            dialog.save_config()
            self.config = config
            # 同时保存到 Somn 配置
            llm_cfg = get_llm_config()
            llm_cfg.save(config)
            self._update_status()
            QMessageBox.information(self, "成功", "配置已保存！")

    def _update_status(self):
        """更新状态栏"""
        if self.config.get("api_url") and self.config.get("api_key"):
            self.status_bar.showMessage(
                f"✅ 已配置: {self.config['model']} | {self.config['api_url']}"
            )
        else:
            self.status_bar.showMessage("⚠️ 请先配置大模型 API")

    def _on_file_selected(self, path: str):
        """文件选中"""
        if Path(path).is_file():
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                self.code_preview.set_content(content[:5000], path)
            except Exception as e:
                logger.error(f"读取文件失败: {e}")

    def _on_copy_available(self, available: bool):
        pass

    def _send_request(self):
        """发送请求"""
        if not self.config.get("api_url") or not self.config.get("api_key"):
            QMessageBox.warning(self, "提示", "请先配置大模型 API")
            self._show_llm_config()
            return

        request = self.prompt_input.toPlainText().strip()
        if not request:
            QMessageBox.warning(self, "提示", "请输入编程指令")
            return

        # 获取项目结构
        project_structure = self.file_tree.get_structure_str()
        if not project_structure:
            project_structure = "未选择项目，使用空项目模板"

        # 初始化生成器
        self.generator = CodeGenerator(
            self.config["api_url"],
            self.config["api_key"],
            self.config["model"],
        )

        # 获取选中文件内容
        selected_file = None
        file_content = ""
        if self.code_preview.current_file:
            selected_file = self.code_preview.current_file
            file_content = self.code_preview.code_edit.toPlainText()

        # 更新 UI
        self.send_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.output_browser.append(
            f"<div style='color: {_BRAND_PRIMARY};'>"
            f"<b>👤 用户:</b> {request}</div><hr>"
        )

        # 启动工作线程
        self.ai_worker = AIWorker(
            self.generator,
            request,
            project_structure,
            selected_file,
            file_content,
        )
        self.ai_worker.chunk_ready.connect(self._on_chunk)
        self.ai_worker.finished.connect(self._on_finished)
        self.ai_worker.error.connect(self._on_error)
        self.ai_worker.start()

        self.current_code = ""

    def _on_chunk(self, chunk: str):
        """处理流式输出"""
        self.current_code += chunk
        # 简单显示
        self.output_browser.insertPlainText(chunk)

    def _on_finished(self, result: str):
        """处理完成"""
        self.send_btn.setEnabled(True)
        self.progress_bar.setVisible(False)

        # 解析并提取代码
        parsed = self.generator.parse_code_response(result)

        if parsed["files"]:
            # 显示第一个代码块
            code = parsed["files"][0]["code"]
            lang = parsed["files"][0]["language"]
            self.code_preview.set_content(code, "NEW_FILE", lang)
        else:
            self.output_browser.append(
                f"<div style='color: {_ACCENT_ORANGE};'>"
                f"<b>⚠️ 未检测到代码块，请在下方编辑器中查看完整回复</b></div>"
            )

        self.status_bar.showMessage("✅ 生成完成")

    def _on_error(self, error: str):
        """处理错误"""
        self.send_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.output_browser.append(
            f"<div style='color: {_ERROR};'>"
            f"<b>❌ 错误:</b> {error}</div>"
        )
        self.status_bar.showMessage(f"❌ 错误: {error[:50]}")

    def _stop_generation(self):
        """停止生成"""
        if self.ai_worker and self.ai_worker.isRunning():
            self.ai_worker.terminate()
            self.ai_worker.wait()
        self.send_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage("⏹ 已停止")

    def _clear_chat(self):
        """清空对话"""
        self.output_browser.clear()
        self.code_preview.set_content("")
        self.prompt_input.clear()


# ═══════════════════════════════════════════════════════════════════════════════
# 程序入口
# ═══════════════════════════════════════════════════════════════════════════════

def _install_dependencies():
    """确保依赖已安装"""
    deps = ["PyQt6", "aiohttp", "requests", "loguru"]
    for dep in deps:
        try:
            __import__(dep.lower().replace("-", "_"))
        except ImportError:
            import subprocess
            subprocess.run([sys.executable, "-m", "pip", "install", dep, "-q"])


def main():
    """主入口"""
    _install_dependencies()

    app = QApplication(sys.argv)
    app.setApplicationName("CodePilot")
    app.setOrganizationName("CodePilot")

    # 尝试加载深色主题
    try:
        from qdarktheme import setup_theme
        app.setStyle("Fusion")
        setup_theme("dark")
    except ImportError:
        pass

    window = CodePilotWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
