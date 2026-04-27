"""
Somn - 汇千古之智，向未知而生
一个能持续学习,成长的超级智能体
Somn v1.0.0 - 神之架构最终完整版
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# 根治 from src.xxx import ... 错误导入（全局修复）
# 让 `import src` / `from src.xxx import ...` 指向当前模块 (smart_office_assistant.src)
# ═══════════════════════════════════════════════════════════════════════════════
import sys
# 让 `import src` / `from src.xxx import ...` 指向当前模块 (smart_office_assistant.src)
sys.modules['src'] = sys.modules[__name__]
# ═══════════════════════════════════════════════════════════════════════════════

__version__ = "1.0.0"
__author__ = "Somn Team"
__description__ = "Smart Office Assistant - 超级智能体系统"


def __getattr__(name: str):
    """延迟导入公开符号"""
    if name == "Somn":
        from .somn import Somn
        return Somn
    if name == "main":
        from .som import main
        return main
    if name == "setup_logging":
        from .som import setup_logging
        return setup_logging
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
