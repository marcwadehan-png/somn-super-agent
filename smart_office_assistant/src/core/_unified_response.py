# -*- coding: utf-8 -*-
"""
统一LLM响应格式 v1.0
====================

解决三层响应格式不一致问题：
- GenerationResult (LocalLLMEngine)
- LLMResponse (LLMService)
- DualModelResponse (DualModelService)

提供统一的接口和转换方法。
"""

from __future__ import annotations

import time
import logging
from typing import Dict, Optional, Any, List, Union
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger("UnifiedLLM")


# ═══════════════════════════════════════════════════════════════════════
# 来源枚举
# ═══════════════════════════════════════════════════════════════════════

class ResponseSource(Enum):
    """响应来源"""
    LOCAL_A = "local-a"       # A大模型 (Llama 3.2 1B)
    LOCAL_B = "local-b"       # B大模型 (Gemma4)
    LOCAL_TEMPLATE = "local-template"  # 智能模板引擎
    CLOUD_OPENAI = "cloud-openai"
    CLOUD_DEEPSEEK = "cloud-deepseek"
    CLOUD_DOUBAO = "cloud-doubao"
    CLOUD_HUNYUAN = "cloud-hunyuan"
    CLOUD_QWEN = "cloud-qwen"
    CLOUD_OTHER = "cloud-other"
    UNKNOWN = "unknown"


class FinishReason(Enum):
    """结束原因"""
    STOP = "stop"
    LENGTH = "length"
    ERROR = "error"
    TIMEOUT = "timeout"
    SAFETY = "safety"
    FILTER = "filter"


# ═══════════════════════════════════════════════════════════════════════
# 统一响应数据类
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class UnifiedLLMResponse:
    """
    统一LLM响应格式
    
    兼容所有来源的响应，并提供统一的访问接口。
    
    属性:
        content: 生成的文本内容
        model: 模型名称
        source: 响应来源 (ResponseSource枚举)
        tokens: 生成的token数量
        latency_ms: 延迟（毫秒）
        finish_reason: 结束原因
        error: 错误信息（如果有）
        metadata: 额外元数据
    """
    
    content: str
    model: str = "unknown"
    source: Union[str, ResponseSource] = ResponseSource.UNKNOWN
    tokens: int = 0
    latency_ms: float = 0.0
    finish_reason: Union[str, FinishReason] = FinishReason.STOP
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """后处理：标准化枚举值"""
        # 标准化source
        if isinstance(self.source, str):
            self.source = ResponseSource(self.source)
        
        # 标准化finish_reason
        if isinstance(self.finish_reason, str):
            try:
                self.finish_reason = FinishReason(self.finish_reason)
            except ValueError:
                self.finish_reason = FinishReason.STOP
    
    @property
    def is_success(self) -> bool:
        """是否成功"""
        return self.error is None and self.finish_reason == FinishReason.STOP
    
    @property
    def is_error(self) -> bool:
        """是否有错误"""
        return self.error is not None or self.finish_reason == FinishReason.ERROR
    
    @property
    def is_local(self) -> bool:
        """是否来自本地模型"""
        return self.source in (
            ResponseSource.LOCAL_A,
            ResponseSource.LOCAL_B,
            ResponseSource.LOCAL_TEMPLATE
        )
    
    @property
    def is_cloud(self) -> bool:
        """是否来自云端模型"""
        return not self.is_local and self.source != ResponseSource.UNKNOWN
    
    @property
    def duration_seconds(self) -> float:
        """延迟（秒）"""
        return self.latency_ms / 1000.0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "content": self.content,
            "model": self.model,
            "source": self.source.value if isinstance(self.source, ResponseSource) else self.source,
            "tokens": self.tokens,
            "latency_ms": self.latency_ms,
            "finish_reason": self.finish_reason.value if isinstance(self.finish_reason, FinishReason) else self.finish_reason,
            "error": self.error,
            "metadata": self.metadata,
        }
    
    def summary(self) -> str:
        """简要摘要"""
        src = self.source.value if isinstance(self.source, ResponseSource) else self.source
        return f"[{src}] {self.model} | {self.latency_ms:.0f}ms | {len(self.content)}chars"


# ═══════════════════════════════════════════════════════════════════════
# 响应转换器
# ═══════════════════════════════════════════════════════════════════════

class ResponseConverter:
    """
    响应格式转换器
    
    提供各格式之间的相互转换。
    """
    
    @staticmethod
    def from_generation_result(result, source: ResponseSource = ResponseSource.LOCAL_A) -> UnifiedLLMResponse:
        """
        从GenerationResult转换 (LocalLLMEngine)
        
        Args:
            result: GenerationResult对象
            source: 来源标识
        """
        if result is None:
            return UnifiedLLMResponse(
                content="",
                error="None result",
                finish_reason=FinishReason.ERROR
            )
        
        return UnifiedLLMResponse(
            content=result.text,
            model=getattr(result, 'model', 'unknown'),
            source=source,
            tokens=getattr(result, 'tokens', 0),
            latency_ms=getattr(result, 'latency_ms', 0.0),
            finish_reason=getattr(result, 'finish_reason', 'stop'),
            error=getattr(result, 'error', None),
            metadata={"original_type": "GenerationResult"}
        )
    
    @staticmethod
    def from_llm_response(result, source: ResponseSource = None) -> UnifiedLLMResponse:
        """
        从LLMResponse转换 (LLMService)
        
        Args:
            result: LLMResponse对象
            source: 来源标识（自动识别）
        """
        if result is None:
            return UnifiedLLMResponse(
                content="",
                error="None result",
                finish_reason=FinishReason.ERROR
            )
        
        # 自动识别来源
        if source is None:
            source = ResponseConverter._identify_source(getattr(result, 'provider', 'unknown'))
        
        return UnifiedLLMResponse(
            content=getattr(result, 'content', ''),
            model=getattr(result, 'model', 'unknown'),
            source=source,
            tokens=sum(getattr(result, 'usage', {}).values()) if hasattr(result, 'usage') else 0,
            latency_ms=getattr(result, 'latency_ms', 0.0),
            finish_reason=getattr(result, 'finish_reason', 'stop'),
            error=None if getattr(result, 'finish_reason') != 'error' else getattr(result, 'content', 'Unknown error')[:200],
            metadata={
                "original_type": "LLMResponse",
                "usage": getattr(result, 'usage', {}),
                "timestamp": getattr(result, 'timestamp', None)
            }
        )
    
    @staticmethod
    def from_dual_model_response(result) -> UnifiedLLMResponse:
        """
        从DualModelResponse转换 (DualModelService)
        
        Args:
            result: DualModelResponse对象
        """
        if result is None:
            return UnifiedLLMResponse(
                content="",
                error="None result",
                finish_reason=FinishReason.ERROR
            )
        
        # 根据brain_used确定来源
        brain_used = getattr(result, 'brain_used', 'left')
        if brain_used == 'left':
            source = ResponseSource.LOCAL_A
        elif brain_used == 'right':
            source = ResponseSource.LOCAL_B
        else:
            source = ResponseSource.UNKNOWN
        
        # 如果有failover，添加标记
        metadata = {
            "original_type": "DualModelResponse",
            "failover": getattr(result, 'failover', False),
            "failover_reason": getattr(result, 'failover_reason', ''),
            "primary_latency_ms": getattr(result, 'primary_latency_ms', 0),
            "fallback_latency_ms": getattr(result, 'fallback_latency_ms', 0),
        }
        
        return UnifiedLLMResponse(
            content=getattr(result, 'content', ''),
            model=getattr(result, 'model', 'unknown'),
            source=source,
            tokens=sum(getattr(result, 'usage', {}).values()) if hasattr(result, 'usage') else 0,
            latency_ms=getattr(result, 'latency_ms', 0.0),
            finish_reason=getattr(result, 'finish_reason', 'stop'),
            error=None if getattr(result, 'finish_reason') != 'error' else getattr(result, 'content', 'Unknown error')[:200],
            metadata=metadata
        )
    
    @staticmethod
    def to_llm_response(unified: UnifiedLLMResponse):
        """
        转换为LLMResponse格式
        
        用于兼容需要LLMResponse的调用点。
        """
        try:
            from src.tool_layer.llm_service import LLMResponse
            return LLMResponse(
                content=unified.content,
                model=unified.model,
                provider=unified.source.value if isinstance(unified.source, ResponseSource) else unified.source,
                usage={"prompt_tokens": 0, "completion_tokens": unified.tokens},
                finish_reason=unified.finish_reason.value if isinstance(unified.finish_reason, FinishReason) else unified.finish_reason,
                latency_ms=int(unified.latency_ms)
            )
        except ImportError:
            logger.warning("[ResponseConverter] LLMResponse未找到，返回字典")
            return unified.to_dict()
    
    @staticmethod
    def to_dual_model_response(unified: UnifiedLLMResponse):
        """
        转换为DualModelResponse格式
        
        用于兼容需要DualModelResponse的调用点。
        """
        try:
            from src.tool_layer.dual_model_service import DualModelResponse
            
            brain = "left" if unified.source == ResponseSource.LOCAL_A else "right"
            
            return DualModelResponse(
                content=unified.content,
                model=unified.model,
                provider=unified.source.value if isinstance(unified.source, ResponseSource) else unified.source,
                usage={"prompt_tokens": 0, "completion_tokens": unified.tokens},
                finish_reason=unified.finish_reason.value if isinstance(unified.finish_reason, FinishReason) else unified.finish_reason,
                latency_ms=int(unified.latency_ms),
                brain_used=brain,
                failover=False,
                failover_reason=""
            )
        except ImportError:
            logger.warning("[ResponseConverter] DualModelResponse未找到，返回字典")
            return unified.to_dict()
    
    @staticmethod
    def _identify_source(provider: str) -> ResponseSource:
        """根据provider识别来源"""
        provider_lower = provider.lower()
        
        if provider_lower == "local":
            return ResponseSource.LOCAL_A
        elif provider_lower == "deepseek":
            return ResponseSource.CLOUD_DEEPSEEK
        elif provider_lower in ("doubit", "doubao", "volcengine"):
            return ResponseSource.CLOUD_DOUBAO
        elif provider_lower in ("hunyuan", "tencent"):
            return ResponseSource.CLOUD_HUNYUAN
        elif provider_lower in ("alibaba", "qwen", "dashscope"):
            return ResponseSource.CLOUD_QWEN
        elif provider_lower == "openai":
            return ResponseSource.CLOUD_OPENAI
        else:
            return ResponseSource.CLOUD_OTHER


# ═══════════════════════════════════════════════════════════════════════
# 便捷函数
# ═══════════════════════════════════════════════════════════════════════

def convert_response(result, target_type: str = "unified") -> UnifiedLLMResponse:
    """
    通用响应转换函数
    
    Args:
        result: 任意格式的响应对象
        target_type: 目标类型 ("unified" / "llm" / "dual")
    
    Returns:
        转换后的响应对象
    """
    # 首先统一为UnifiedLLMResponse
    if isinstance(result, UnifiedLLMResponse):
        unified = result
    elif hasattr(result, 'text') and hasattr(result, 'model'):
        # GenerationResult
        unified = ResponseConverter.from_generation_result(result)
    elif hasattr(result, 'content') and hasattr(result, 'provider'):
        # DualModelResponse
        unified = ResponseConverter.from_dual_model_response(result)
    elif hasattr(result, 'content'):
        # LLMResponse
        unified = ResponseConverter.from_llm_response(result)
    elif isinstance(result, dict):
        # 字典格式
        unified = UnifiedLLMResponse(
            content=result.get("content", ""),
            model=result.get("model", "unknown"),
            source=ResponseSource(result.get("source", "unknown")),
            error=result.get("error")
        )
    else:
        # 未知格式
        unified = UnifiedLLMResponse(
            content=str(result) if result else "",
            error="Unknown response format"
        )
    
    # 转换为目标格式
    if target_type == "unified":
        return unified
    elif target_type == "llm":
        return ResponseConverter.to_llm_response(unified)
    elif target_type == "dual":
        return ResponseConverter.to_dual_model_response(unified)
    else:
        return unified


def error_response(message: str, model: str = "unknown", source: ResponseSource = ResponseSource.UNKNOWN) -> UnifiedLLMResponse:
    """创建错误响应"""
    return UnifiedLLMResponse(
        content="",
        model=model,
        source=source,
        finish_reason=FinishReason.ERROR,
        error=message,
        latency_ms=0.0
    )


def timeout_response(model: str = "unknown", timeout_ms: float = 0.0) -> UnifiedLLMResponse:
    """创建超时响应"""
    return UnifiedLLMResponse(
        content="",
        model=model,
        source=ResponseSource.LOCAL_A,
        finish_reason=FinishReason.TIMEOUT,
        error=f"Request timeout after {timeout_ms:.0f}ms",
        latency_ms=timeout_ms
    )


# ═══════════════════════════════════════════════════════════════════════
# 导出
# ═══════════════════════════════════════════════════════════════════════

__all__ = [
    # 枚举
    "ResponseSource",
    "FinishReason",
    
    # 数据类
    "UnifiedLLMResponse",
    
    # 转换器
    "ResponseConverter",
    "convert_response",
    
    # 便捷函数
    "error_response",
    "timeout_response",
]
