"""
Somn API Server - 公共辅助函数
所有路由共享的工具函数
"""

from datetime import datetime
from typing import Any, Dict


def error_response(error: str, code: str = "ERROR") -> Dict[str, Any]:
    """构造标准错误响应"""
    return {
        "success": False,
        "error": error,
        "error_code": code,
        "timestamp": datetime.now().isoformat(),
    }


def success_response(message: str = "", data: Any = None) -> Dict[str, Any]:
    """构造标准成功响应"""
    return {
        "success": True,
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "data": data,
    }


def normalize_result(result) -> dict:
    """将各种类型的结果标准化为字典"""
    if result is None:
        return {}
    if isinstance(result, dict):
        return result
    if isinstance(result, str):
        return {"text": result}
    return {"raw": str(result)}
