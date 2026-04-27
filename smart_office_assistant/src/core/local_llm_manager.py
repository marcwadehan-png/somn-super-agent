# -*- coding: utf-8 -*-
"""
本地LLM管理器 - A大模型自动调度 v3.2
====================================
无任何第三方依赖，内置智能模板引擎

[v3.2 增强]
- 会话上下文管理
- 统一响应格式支持
- 智能降级策略
"""

import threading
import time
import logging
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

from .local_llm_engine import (
    LocalLLMEngine,
    GenerationResult,
    ServiceState,
    get_engine,
    DEFAULT_MODEL_NAME,
)

logger = logging.getLogger("LocalLLM.Manager")


# ============================================================
# 调度策略
# ============================================================

class DispatchStrategy(Enum):
    MANUAL = "manual"
    AUTO = "auto"


@dataclass
class DispatchRule:
    keywords: List[str]
    priority: int = 0


# ============================================================
# 本地LLM管理器
# ============================================================

class LocalLLMManager:
    """
    本地LLM管理器 v3.2
    
    特性：
    - 单例模式
    - 无外部依赖
    - 自动检测模式
    - 智能调度
    - [v3.2] 会话上下文管理
    - [v3.2] 统一响应格式
    """

    _instance: Optional['LocalLLMManager'] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, auto_start: bool = True):
        if hasattr(self, '_initialized') and self._initialized:
            return

        self._engine: Optional[LocalLLMEngine] = None
        self._auto_start = auto_start
        self._strategy = DispatchStrategy.AUTO
        self._enabled = True
        self._rules: List[DispatchRule] = []

        # [v3.2] 会话上下文管理
        self._conversation_history: Dict[str, List[Dict]] = defaultdict(list)
        self._max_history_per_session = 20
        self._session_lock = threading.Lock()
        self._last_cleanup = time.time()
        self._cleanup_interval = 300  # 5分钟清理一次过期会话

        self._register_default_rules()
        self._initialized = True

        logger.info("[LocalLLMManager] Manager v3.2 initialized")

        if auto_start:
            self._async_start()

    def _register_default_rules(self):
        self._rules = [
            DispatchRule(keywords=["什么是", "请问", "怎么", "如何"], priority=1),
            DispatchRule(keywords=["写", "生成", "创建", "翻译"], priority=2),
            DispatchRule(keywords=["代码", "函数", "class"], priority=3),
            DispatchRule(keywords=["分析", "研究", "比较"], priority=4),
        ]

    # ==================== 生命周期 ====================

    def start(self, timeout: float = 30.0) -> bool:
        """启动管理器"""
        if self._engine and self._engine.is_ready:
            return True

        logger.info("[LocalLLMManager] Starting engine...")
        self._engine = get_engine()
        success = self._engine.start(timeout=timeout)

        if success:
            logger.info(f"[LocalLLMManager] Ready! Mode: {self._engine.load_mode}")
        else:
            logger.warning(f"[LocalLLMManager] Failed: {self._engine._init_error}")

        return success

    def stop(self):
        if self._engine:
            self._engine.stop()
            self._engine = None

    def _async_start(self):
        thread = threading.Thread(target=self.start, daemon=True)
        thread.start()

    # ==================== 属性 ====================

    @property
    def engine(self) -> Optional[LocalLLMEngine]:
        return self._engine

    @property
    def is_ready(self) -> bool:
        return self._engine is not None and self._engine.is_ready

    @property
    def state(self) -> ServiceState:
        if self._engine:
            return self._engine.state
        return ServiceState.STOPPED

    # ==================== 调度 ====================

    def should_use_local(self, prompt: str, **kwargs) -> bool:
        """判断是否使用本地"""
        if not self._enabled:
            return False
        if not self.is_ready:
            return False

        # 默认总是使用本地（无外部依赖）
        return True
    
    # ==================== [v3.2] 会话上下文 ====================
    
    def _build_context_prompt(self, prompt: str, session_id: str) -> str:
        """
        构建带上下文的提示
        
        Args:
            prompt: 原始提示
            session_id: 会话ID
        
        Returns:
            带上下文的增强提示
        """
        with self._session_lock:
            history = self._conversation_history.get(session_id, [])
        
        if not history:
            return prompt
        
        # 构建上下文
        context_lines = []
        for h in history[-self._max_history_per_session:]:
            context_lines.append(f"用户: {h.get('user', '')}")
            context_lines.append(f"助手: {h.get('assistant', '')}")
        
        context_text = "\n".join(context_lines)
        return f"""[对话历史]
{context_text}

[当前提问]
用户: {prompt}
助手: """
    
    def _cleanup_expired_sessions(self, max_age_seconds: int = 3600):
        """清理过期会话"""
        current_time = time.time()
        if current_time - self._last_cleanup < self._cleanup_interval:
            return
        
        self._last_cleanup = current_time
        expired = []
        
        with self._session_lock:
            for session_id, history in self._conversation_history.items():
                if not history:
                    expired.append(session_id)
                    continue
                
                # 检查最后一条记录的时间
                last_time = history[-1].get('timestamp', 0)
                if current_time - last_time > max_age_seconds:
                    expired.append(session_id)
        
        for session_id in expired:
            with self._session_lock:
                self._conversation_history.pop(session_id, None)
        
        if expired:
            logger.info(f"[LocalLLMManager] 清理了 {len(expired)} 个过期会话")
    
    def chat(
        self, 
        message: str, 
        session_id: str = "default", 
        use_local: Optional[bool] = None,
        **kwargs
    ) -> str:
        """
        带会话上下文的聊天 [v3.2]
        
        Args:
            message: 用户消息
            session_id: 会话ID（用于维护上下文）
            use_local: 是否使用本地模型
            **kwargs: 传递给generate的参数
        
        Returns:
            助手回复文本
        """
        # 清理过期会话
        self._cleanup_expired_sessions()
        
        # 构建带上下文的提示
        context_prompt = self._build_context_prompt(message, session_id)
        
        # 调用生成
        if use_local is None:
            use_local = self.should_use_local(message, **kwargs)
        
        result = self.dispatch(context_prompt, use_local=use_local, **kwargs)
        
        # 记录对话历史
        with self._session_lock:
            self._conversation_history[session_id].append({
                "user": message,
                "assistant": result.text,
                "timestamp": time.time()
            })
            
            # 限制历史长度
            if len(self._conversation_history[session_id]) > self._max_history_per_session * 2:
                self._conversation_history[session_id] = \
                    self._conversation_history[session_id][-self._max_history_per_session:]
        
        return result.text
    
    def clear_session(self, session_id: str = "default"):
        """清除指定会话的历史"""
        with self._session_lock:
            self._conversation_history.pop(session_id, None)
        logger.info(f"[LocalLLMManager] 会话 {session_id} 已清除")
    
    def get_session_history(self, session_id: str = "default") -> List[Dict]:
        """获取会话历史"""
        with self._session_lock:
            return list(self._conversation_history.get(session_id, []))

    def dispatch(
        self,
        prompt: str,
        use_local: Optional[bool] = None,
        fallback: Optional[Callable] = None,
        **kwargs
    ) -> GenerationResult:
        """调度生成"""
        if use_local is None:
            use_local = self.should_use_local(prompt, **kwargs)

        if use_local and self.is_ready:
            try:
                return self._engine.generate(prompt, **kwargs)
            except Exception as e:
                logger.error(f"[LocalLLMManager] Generation error: {e}")
                if fallback:
                    return fallback(prompt, **kwargs)

        if fallback:
            return fallback(prompt, **kwargs)

        return GenerationResult(
            text="[LocalLLM] Not available",
            model=self._engine.model_name if self._engine else "unknown",
            tokens=0,
            latency_ms=0,
            finish_reason="error"
        )
    
    def dispatch_unified(
        self,
        prompt: str,
        use_local: Optional[bool] = None,
        session_id: str = "default",
        **kwargs
    ):
        """
        统一格式调度 [v3.2]
        
        返回统一格式响应，便于与DualModelService集成。
        
        Args:
            prompt: 提示词
            use_local: 是否使用本地
            session_id: 会话ID
            **kwargs: 其他参数
        
        Returns:
            UnifiedLLMResponse格式
        """
        from ._unified_response import UnifiedLLMResponse, ResponseConverter, ResponseSource
        
        # 如果有会话上下文，构建增强提示
        if session_id and session_id != "default":
            context_prompt = self._build_context_prompt(prompt, session_id)
        else:
            context_prompt = prompt
        
        # 调用生成
        result = self.dispatch(context_prompt, use_local=use_local, **kwargs)
        
        # 转换为统一格式
        unified = ResponseConverter.from_generation_result(result, ResponseSource.LOCAL_A)
        
        # 如果是使用模板引擎
        if self._engine and self._engine.load_mode == "smart_template":
            unified.source = ResponseSource.LOCAL_TEMPLATE
        
        return unified

    def chat(self, message: str, use_local: Optional[bool] = None, **kwargs) -> str:
        """快捷聊天"""
        result = self.dispatch(message, use_local=use_local, **kwargs)
        return result.text

    # ==================== 控制 ====================

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def set_strategy(self, strategy: DispatchStrategy):
        self._strategy = strategy

    # ==================== 状态 ====================

    def get_status(self) -> Dict[str, Any]:
        return {
            "enabled": self._enabled,
            "strategy": self._strategy.value,
            "state": self.state.value,
            "is_ready": self.is_ready,
            "engine": self._engine.model_info if self._engine else None,
            "stats": self._engine.get_stats() if self._engine else {},
        }

    def __repr__(self):
        return f"LocalLLMManager({self.state.value}, enabled={self._enabled})"


# ============================================================
# 全局
# ============================================================

_manager: Optional[LocalLLMManager] = None


def get_manager(auto_start: bool = True) -> LocalLLMManager:
    global _manager
    if _manager is None:
        _manager = LocalLLMManager(auto_start=auto_start)
    return _manager


def shutdown_manager():
    global _manager
    if _manager:
        _manager.stop()
        _manager = None


__all__ = [
    "LocalLLMManager",
    "DispatchStrategy",
    "DispatchRule",
    "get_manager",
    "shutdown_manager",
]
