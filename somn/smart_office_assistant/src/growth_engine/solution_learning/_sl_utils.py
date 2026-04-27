"""工具函数模块"""

import re
import yaml
import warnings
from pathlib import Path
from typing import Dict, Any, Optional
from enum import Enum

__all__ = [
    'safe_yaml_dump',
    'safe_yaml_load',
]

def safe_yaml_load(file_path: Path) -> Optional[Dict[str, Any]]:
    """安全加载YAML文件,兼容新旧格式"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if '!!python/object' in content:
            try:
                data = yaml.load(content, Loader=yaml.UnsafeLoader)
                return _extract_python_object_data(data)
            except Exception:
                return _extract_basic_fields(content)
        else:
            return yaml.safe_load(content)
    except Exception as e:
        warnings.warn(f"加载YAML文件失败 {file_path}: {e}")
        return None

def _extract_python_object_data(obj: Any) -> Dict[str, Any]:
    """从Python对象中提取核心数据"""
    if obj is None:
        return {}
    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            extracted = _extract_python_object_data(v)
            if extracted is not None:
                result[k] = extracted
        return result
    if isinstance(obj, list):
        return [_extract_python_object_data(item) for item in obj]
    if isinstance(obj, Enum):
        return obj.value
    if hasattr(obj, '__dict__'):
        return _extract_python_object_data(obj.__dict__)
    return obj

def _extract_basic_fields(content: str) -> Dict[str, Any]:
    """从包含Python对象标记的旧格式YAML中提取基本字段"""
    result = {}
    simple_fields = ['session_id', 'provider_name', 'category', 'status',
                     'source_type', 'capabilities_count', 'started_at', 'completed_at']
    for field_name in simple_fields:
        pattern = rf'^{field_name}:\s*(.+?)$'
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            value = match.group(1).strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            result[field_name] = value
    return result

def safe_yaml_dump(data: Any, file_path: Path) -> bool:
    """安全保存YAML文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        return True
    except Exception as e:
        warnings.warn(f"保存YAML文件失败 {file_path}: {e}")
        return False

def _enum_to_str(obj):
    """递归将Enum值转为字符串,用于YAML序列化"""
    if isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, dict):
        return {k: _enum_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_enum_to_str(item) for item in obj]
    return obj
