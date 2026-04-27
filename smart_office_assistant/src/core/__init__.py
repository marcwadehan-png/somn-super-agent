"""Core modules for Smart Office Assistant"""

from typing import Any

# 核心组件 - 使用懒加载避免循环导入
def __getattr__(name: str) -> Any:
    if name == "AgentCore":
        from .agent_core import AgentCore
        return AgentCore
    if name == "SomnCore":
        from .somn_core import SomnCore
        return SomnCore
    # 本地LLM引擎
    if name == "LocalLLMEngine":
        from .local_llm_engine import LocalLLMEngine
        return LocalLLMEngine
    if name == "LocalLLMManager":
        from .local_llm_manager import LocalLLMManager
        return LocalLLMManager
    if name == "get_local_llm_manager":
        from .local_llm_manager import get_manager
        return get_manager
    if name == "local_llm_chat":
        from .local_llm_manager import chat
        return chat
    # B大模型 (Gemma4 safetensors)
    if name == "get_engine_b":
        from .local_llm_engine import get_engine_b
        return get_engine_b
    if name == "chat_b":
        from .local_llm_engine import chat_b
        return chat_b
    if name == "generate_b":
        from .local_llm_engine import generate_b
        return generate_b
    # 主线架构集成
    _main_chain_exports = {
        "get_main_chain_integration": "get_main_chain_integration",
        "get_parallel_router": "get_parallel_router",
        "get_cross_weaver": "get_cross_weaver",
        "get_main_chain_scheduler": "get_main_chain_scheduler",
        "get_main_chain_monitor": "get_main_chain_monitor",
        "MainChainIntegration": "MainChainIntegration",
        "MainChainScheduler": "MainChainScheduler",
        "MainChainMonitor": "MainChainMonitor",
    }
    if name in _main_chain_exports:
        from ..main_chain import (
            get_main_chain_integration,
            get_parallel_router,
            get_cross_weaver,
            get_main_chain_scheduler,
            get_main_chain_monitor,
            MainChainIntegration,
            MainChainScheduler,
            MainChainMonitor,
        )
    _import_map = {
        "get_main_chain_integration": get_main_chain_integration,
        "get_parallel_router": get_parallel_router,
        "get_cross_weaver": get_cross_weaver,
        "get_main_chain_scheduler": get_main_chain_scheduler,
        "get_main_chain_monitor": get_main_chain_monitor,
        "MainChainIntegration": MainChainIntegration,
        "MainChainScheduler": MainChainScheduler,
        "MainChainMonitor": MainChainMonitor,
    }
    return _import_map[name]
    raise AttributeError(f"module 'src.core' has no attribute {name}")

__all__ = [
    # 核心组件
    "AgentCore",
    "SomnCore",
    # 本地LLM (A大模型)
    "LocalLLMEngine",
    "LocalLLMManager",
    "get_local_llm_manager",
    "local_llm_chat",
    # B大模型 (Gemma4 safetensors)
    "get_engine_b",
    "chat_b",
    "generate_b",
    # 主线组件
    "get_main_chain_integration",
    "get_parallel_router",
    "get_cross_weaver",
    "get_main_chain_scheduler",
    "get_main_chain_monitor",
    "MainChainIntegration",
    "MainChainScheduler",
    "MainChainMonitor",
]
