# ClawEnvironment - 环境变量适配
# v1.0.0: 完整环境变量适配能力

from __future__ import annotations

import os
import logging
from typing import Dict, Optional, Any, List
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════
# 环境变量前缀
# ═══════════════════════════════════════════════════════════

PREFIX_CLAW = "CLAW_"
PREFIX_OPENCLAW = "OPENCLAW_"


# ═══════════════════════════════════════════════════════════
# 配置项定义
# ═══════════════════════════════════════════════════════════

@dataclass
class EnvConfigItem:
    """环境配置项"""
    key: str
    default: Any
    description: str
    required: bool = False
    type: str = "string"  # string/int/float/bool/path/list


# ═══════════════════════════════════════════════════════════
# 配置表
# ═══════════════════════════════════════════════════════════

CLAW_ENV_CONFIG: List[EnvConfigItem] = [
    # 基础配置
    EnvConfigItem("CLAW_NAME", "", "Claw名称", type="string"),
    EnvConfigItem("CLAW_MODE", "independent", "工作模式: independent/collaborative", type="string"),
    EnvConfigItem("CLAW_LEVEL", "normal", "Claw级别: basic/normal/advanced", type="string"),
    
    # 记忆配置
    EnvConfigItem("CLAW_MEMORY_ENABLED", "true", "启用记忆系统", type="bool"),
    EnvConfigItem("CLAW_MEMORY_PATH", "data/claws/{name}/memory", "记忆存储路径", type="path"),
    EnvConfigItem("CLAW_MEMORY_AUTO_SAVE", "true", "自动保存记忆", type="bool"),
    EnvConfigItem("CLAW_LEARNING_THRESHOLD", "10", "学习触发阈值", type="int"),
    
    # 协作配置
    EnvConfigItem("CLAW_COLLABORATORS", "", "协作者列表(逗号分隔)", type="string"),
    EnvConfigItem("CLAW_COLLABORATION_MAX", "2", "最大协作者数量", type="int"),
    EnvConfigItem("CLAW_COLLABORATION_TIMEOUT", "60", "协作超时(秒)", type="int"),
    
    # SOUL配置
    EnvConfigItem("CLAW_SOUL_STRICT", "false", "严格SOUL行为", type="bool"),
    EnvConfigItem("CLAW_BELIEF_PRIORITY", "medium", "信念优先级阈值", type="string"),
    
    # IDENTITY配置
    EnvConfigItem("CLAW_ROUTE_STRATEGY", "auto", "路由策略: auto/role/skill", type="string"),
    EnvConfigItem("CLAW_SKILL_THRESHOLD", "0.5", "技能匹配阈值", type="float"),
    
    # 性能配置
    EnvConfigItem("CLAW_TIMEOUT", "300", "处理超时(秒)", type="int"),
    EnvConfigItem("CLAW_MAX_RETRIES", "3", "最大重试次数", type="int"),
    EnvConfigItem("CLAW_CACHE_ENABLED", "true", "启用缓存", type="bool"),
    
    # 日志配置
    EnvConfigItem("CLAW_LOG_LEVEL", "INFO", "日志级别", type="string"),
    EnvConfigItem("CLAW_LOG_FILE", "", "日志文件路径", type="path"),
    
    # OpenClaw兼容
    EnvConfigItem("OPENCLAW_INSTALL_METHOD", "npm", "安装方法", type="string"),
    EnvConfigItem("OPENCLAW_TAG", "latest", "版本标签", type="string"),
    EnvConfigItem("OPENCLAW_NO_ONBOARD", "0", "跳过引导", type="bool"),
]


# ═══════════════════════════════════════════════════════════
# ClawEnvironment主类
# ═══════════════════════════════════════════════════════════

class ClawEnvironment:
    """
    Claw环境变量适配器
    
    功能：
    - 加载CLAW_/OPENCLAW_前缀的环境变量
    - 类型转换
    - 默认值处理
    - 配置验证
    """
    
    def __init__(self, claw_name: Optional[str] = None):
        self.claw_name = claw_name or os.getenv("CLAW_NAME", "default")
        self._configs: Dict[str, EnvConfigItem] = {c.key: c for c in CLAW_ENV_CONFIG}
        self._values: Dict[str, Any] = {}
        self._load()
        
        logger.info(f"[ClawEnvironment] 初始化: {self.claw_name}")
    
    def _load(self) -> None:
        """加载环境变量"""
        # 加载所有相关环境变量
        for key, value in os.environ.items():
            if key.startswith(PREFIX_CLAW) or key.startswith(PREFIX_OPENCLAW):
                # 去除前缀，保留原键
                clean_key = key[len(PREFIX_CLAW):] if key.startswith(PREFIX_CLAW) else key[len(PREFIX_OPENCLAW):]
                self._values[clean_key] = value
        
        # 处理路径模板
        if "CLAW_MEMORY_PATH" in self._values:
            path = self._values["CLAW_MEMORY_PATH"]
            if "{name}" in path:
                self._values["CLAW_MEMORY_PATH"] = path.replace("{name}", self.claw_name)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键（不含前缀）
            default: 默认值
            
        Returns:
            Any: 配置值（已类型转换）
        """
        # 尝试多个可能的前缀
        candidates = [
            f"{PREFIX_CLAW}{key}",
            f"{PREFIX_OPENCLAW}{key}",
            key
        ]
        
        raw_value = None
        for candidate in candidates:
            if candidate in os.environ:
                raw_value = os.environ[candidate]
                break
        
        if raw_value is None:
            return default
        
        # 类型转换
        config = self._configs.get(key)
        if config:
            return self._convert(raw_value, config.type)
        
        # 尝试自动检测类型
        return self._auto_convert(raw_value)
    
    def _convert(self, value: str, target_type: str) -> Any:
        """类型转换"""
        if target_type == "string":
            return value
        elif target_type == "int":
            return int(value)
        elif target_type == "float":
            return float(value)
        elif target_type == "bool":
            return value.lower() in ("true", "1", "yes", "on")
        elif target_type == "path":
            return Path(value)
        elif target_type == "list":
            return [v.strip() for v in value.split(",") if v.strip()]
        return value
    
    def _auto_convert(self, value: str) -> Any:
        """自动类型转换"""
        # 布尔
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        # 整数
        try:
            return int(value)
        except ValueError:
            pass
        # 浮点数
        try:
            return float(value)
        except ValueError:
            pass
        # 列表
        if "," in value:
            return [v.strip() for v in value.split(",")]
        # 路径
        if "/" in value or "\\" in value or value.endswith((".md", ".yaml", ".json")):
            return Path(value)
        return value
    
    # ── 便捷访问方法 ──
    
    def get_name(self) -> str:
        """获取Claw名称"""
        return self.get("CLAW_NAME", self.claw_name)
    
    def get_mode(self) -> str:
        """获取工作模式"""
        return self.get("CLAW_MODE", "independent")
    
    def is_memory_enabled(self) -> bool:
        """记忆是否启用"""
        return self.get("CLAW_MEMORY_ENABLED", True)
    
    def get_memory_path(self) -> Path:
        """获取记忆路径"""
        return self.get("CLAW_MEMORY_PATH", Path(f"data/claws/{self.claw_name}/memory"))
    
    def get_collaborators(self) -> List[str]:
        """获取协作者列表"""
        return self.get("CLAW_COLLABORATORS", [])
    
    def get_timeout(self) -> int:
        """获取超时时间"""
        return self.get("CLAW_TIMEOUT", 300)
    
    def get_log_level(self) -> str:
        """获取日志级别"""
        return self.get("CLAW_LOG_LEVEL", "INFO")
    
    def get_soul_strict(self) -> bool:
        """SOUL是否严格"""
        return self.get("CLAW_SOUL_STRICT", False)
    
    # ── 配置验证 ──
    
    def validate(self) -> Dict[str, Any]:
        """
        验证配置
        
        Returns:
            Dict: 验证结果 {"valid": bool, "errors": List[str], "warnings": List[str]}
        """
        errors = []
        warnings = []
        
        for key, config in self._configs.items():
            if config.required:
                value = self.get(key)
                if value is None:
                    errors.append(f"必需配置 '{key}' 未设置")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    # ── 配置导出 ──
    
    def to_dict(self) -> Dict[str, Any]:
        """导出所有配置"""
        return {
            "claw_name": self.claw_name,
            "configs": {k: self.get(k) for k in self._configs.keys()}
        }
    
    def to_env_file(self, path: Path) -> None:
        """
        导出为.env文件
        
        Args:
            path: .env文件路径
        """
        lines = [f"# ClawEnvironment 配置"]
        lines.append(f"# 生成时间: {__import__('datetime').datetime.now().isoformat()}")
        lines.append("")
        lines.append(f"# === Claw配置 ===")
        lines.append(f"CLAW_NAME={self.claw_name}")
        
        for key in sorted(self._configs.keys()):
            value = self.get(key)
            if value is not None:
                lines.append(f"{key}={value}")
        
        content = "\n".join(lines)
        path.write_text(content, encoding="utf-8")
        logger.info(f"[ClawEnvironment] 导出配置到: {path}")


# ═══════════════════════════════════════════════════════════
# 导出
# ═══════════════════════════════════════════════════════════

__all__ = [
    "PREFIX_CLAW",
    "PREFIX_OPENCLAW",
    "EnvConfigItem",
    "CLAW_ENV_CONFIG",
    "ClawEnvironment",
]