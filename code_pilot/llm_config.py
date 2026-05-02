# -*- coding: utf-8 -*-
"""
CodePilot - LLM 配置管理器
复用 Somn 云端大模型配置
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Dict, Any


class LLMConfigManager:
    """LLM 配置管理器"""

    # 默认配置文件路径
    DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "data" / "llm_config.json"

    # 兼容路径（Somn-GUI）
    COMPAT_CONFIG_PATHS = [
        Path(__file__).parent.parent / "data" / "llm_config.json",
        Path.home() / ".codepilot" / "config.json",
    ]

    _instance: Optional["LLMConfigManager"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._config: Dict[str, Any] = {}
        self._config_path = self._find_config_path()
        self._load()
        self._initialized = True

    def _find_config_path(self) -> Path:
        """查找配置文件"""
        for path in self.COMPAT_CONFIG_PATHS:
            if path.exists():
                return path
        return self.DEFAULT_CONFIG_PATH

    def _load(self):
        """加载配置"""
        if self._config_path.exists():
            try:
                with open(self._config_path, "r", encoding="utf-8") as f:
                    self._config = json.load(f)
            except Exception:
                self._config = self._get_default_config()
        else:
            self._config = self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "api_url": "https://api.minimax.chat/v1",
            "api_key": "",
            "model": "MiniMax-Text-01",
            "temperature": 0.7,
            "enabled": True,
        }

    def save(self, config: Dict[str, Any] = None):
        """保存配置"""
        if config:
            self._config.update(config)

        self._config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._config_path, "w", encoding="utf-8") as f:
            json.dump(self._config, f, indent=2, ensure_ascii=False)

    @property
    def api_url(self) -> str:
        return self._config.get("api_url", "")

    @property
    def api_key(self) -> str:
        return self._config.get("api_key", "")

    @property
    def model(self) -> str:
        return self._config.get("model", "gpt-4o")

    @property
    def temperature(self) -> float:
        return self._config.get("temperature", 0.7)

    @property
    def enabled(self) -> bool:
        return self._config.get("enabled", True) and bool(self._config.get("api_key"))

    def get_config(self) -> Dict[str, Any]:
        """获取完整配置"""
        return self._config.copy()

    def is_configured(self) -> bool:
        """检查是否已配置"""
        return bool(self.api_url and self.api_key)


# 全局单例
_config_manager: Optional[LLMConfigManager] = None


def get_llm_config() -> LLMConfigManager:
    """获取 LLM 配置管理器单例"""
    global _config_manager
    if _config_manager is None:
        _config_manager = LLMConfigManager()
    return _config_manager
