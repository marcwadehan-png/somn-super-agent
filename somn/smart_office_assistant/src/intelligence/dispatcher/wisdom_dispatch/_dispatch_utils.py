# -*- coding: utf-8 -*-
"""
wisdom_dispatch 共享工具函数

消除 _decision_congress / _imperial_library 等模块之间的重复工具代码。
v1.0.0 新增
"""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def find_project_root(start_file: str = __file__) -> Path:
    """定位项目根目录（与 path_bootstrap.py 同逻辑）"""
    current = Path(start_file).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "config" / "court_config.yaml").exists():
            return parent
        if (parent / "smart_office_assistant").is_dir():
            return parent
    # 回退：假设 src/intelligence/dispatcher/wisdom_dispatch 结构
    return current.parents[4]


def find_court_config(start_file: str = __file__) -> Optional[Path]:
    """定位 court_config.yaml"""
    current = Path(start_file).resolve()
    for parent in [current] + list(current.parents):
        candidate = parent / "config" / "court_config.yaml"
        if candidate.exists():
            return candidate
    return None


def load_yaml(path: Path) -> Dict[str, Any]:
    """安全加载 YAML 文件"""
    try:
        import yaml
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        logger.warning(f"YAML加载失败 [{path}]: {e}")
        return {}


def deep_merge(base: Dict, override: Dict) -> Dict:
    """深度合并字典，override 中的值覆盖 base"""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result
