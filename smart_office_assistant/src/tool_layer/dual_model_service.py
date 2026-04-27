# -*- coding: utf-8 -*-
"""
双模型平行调度服务 - A/B左右大脑 v2.0
=========================================
全局模式下A、B两个模型属于平行调用关系：
- 当其中一个响应速度不够时自动切换另一个
- 在全局任何需求指令下，大模型都会被自动激活
- A/B模型作为系统的左右大脑来完成任务

设计原则：
- 优先使用A模型（主脑），B模型为辅（副脑）
- A模型超时/熔断/错误时，自动切换B模型
- B模型同样支持独立工作
- 全局任何调用都自动激活双模型服务
- 透明代理：对外接口与 LLMService 完全兼容

集成方式：
- SomnCore.dual_model_service 属性（懒加载）
- 替代直接使用 llm_service 的场景
- 兼容所有现有 LLMService.chat() / analyze() / generate_strategy() 调用

[v1.1.0 增强]
- 直接集成LocalLLMEngine的A/B模型
- 本地模型优先策略
- 透明级联切换

[v2.0 能力感知调度]
- CapabilityAnalyzer: 自动分析输入内容的能力需求
- dispatch_by_capability: 根据任务需求动态选择最佳模型
- 模型能力评分机制：输入图片→优先视觉模型，输入代码→优先代码模型
"""

import json
import logging
import os
import threading
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# 枚举与数据类
# ═══════════════════════════════════════════════════════════════

class BrainRole(Enum):
    """大脑角色"""
    LEFT = "left"     # B模型 - 左脑（主脑，Gemma4多模态，优先调用）
    RIGHT = "right"   # A模型 - 右脑（副脑，Llama 3.2 1B)


class TaskCapability(Enum):
    """任务所需能力"""
    VISION = "vision"       # 视觉理解（图片输入）
    CODE = "code"          # 代码生成/分析
    ANALYSIS = "analysis"  # 分析推理
    CHAT = "chat"          # 对话生成
    CREATIVE = "creative"   # 创意写作
    REASONING = "reasoning"  # 复杂推理


class FailoverReason(Enum):
    """切换原因"""
    NONE = "none"
    TIMEOUT = "timeout"           # 响应超时
    CIRCUIT_OPEN = "circuit_open" # 熔断器开启
    ERROR = "error"               # 调用错误
    LATENCY_HIGH = "latency_high" # 延迟过高
    NOT_AVAILABLE = "not_available"  # 服务不可用


@dataclass
class BrainStatus:
    """单个大脑的状态"""
    role: BrainRole
    model_name: str
    provider: str
    is_available: bool = False
    avg_latency_ms: float = 0.0
    success_count: int = 0
    fail_count: int = 0
    last_used: Optional[str] = None
    circuit_state: str = "closed"


@dataclass
class DualModelResponse:
    """双模型响应（包装LLMResponse，增加调度信息）"""
    content: str
    model: str
    provider: str
    usage: Dict[str, int] = field(default_factory=dict)
    finish_reason: str = "stop"
    latency_ms: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    # 双模型专属信息
    brain_used: str = ""           # "left" / "right"
    failover: bool = False         # 是否发生了切换
    failover_reason: str = ""      # 切换原因
    primary_latency_ms: int = 0    # 主模型耗时（如果切换了）
    fallback_latency_ms: int = 0   # 备用模型耗时


@dataclass
class DualModelConfig:
    """双模型配置"""
    # B模型（左脑/主脑）- Gemma4多模态
    primary_model: str = "gemma4-local-b"        # 优先使用的模型名
    primary_timeout_ms: int = 30_000              # 主模型超时（毫秒）
    primary_max_latency_ms: int = 15_000         # 主模型最大可接受延迟

    # A模型（右脑/副脑）- Llama 3.2 1B
    fallback_model: str = "llama-3.2-1b-a"      # 自动切换的目标模型
    fallback_timeout_ms: int = 60_000            # 备用模型超时

    # 调度策略
    auto_failover: bool = True                 # 是否自动切换
    failover_on_latency: bool = True           # 延迟过高时切换
    failover_on_error: bool = True             # 错误时切换
    failover_on_circuit_open: bool = True      # 熔断时切换
    latency_threshold_ms: int = 15_000         # 延迟切换阈值
    track_performance: bool = True             # 是否追踪性能

    # 冷却
    primary_cooldown_seconds: float = 60.0     # 切换后主脑冷却时间


# ═══════════════════════════════════════════════════════════════
# 性能追踪器
# ═══════════════════════════════════════════════════════════════

class PerformanceTracker:
    """
    性能追踪器 - 实时监控A/B模型表现

    追踪指标：
    - 平均延迟
    - 成功率
    - 熔断状态
    - 最近N次调用历史
    """

    def __init__(self, window_size: int = 20):
        self._window_size = window_size
        self._lock = threading.Lock()
        # 每个模型的历史记录
        self._history: Dict[str, List[Dict]] = {}
        # 累计统计
        self._stats: Dict[str, Dict[str, int]] = {}

    def record(self, model_name: str, latency_ms: float, success: bool):
        """记录一次调用结果"""
        with self._lock:
            if model_name not in self._history:
                self._history[model_name] = []
                self._stats[model_name] = {"success": 0, "fail": 0, "total": 0}

            entry = {
                "latency_ms": latency_ms,
                "success": success,
                "timestamp": time.time(),
            }
            self._history[model_name].append(entry)
            # 滑动窗口
            if len(self._history[model_name]) > self._window_size:
                self._history[model_name] = self._history[model_name][-self._window_size:]

            self._stats[model_name]["total"] += 1
            if success:
                self._stats[model_name]["success"] += 1
            else:
                self._stats[model_name]["fail"] += 1

    def get_avg_latency(self, model_name: str) -> float:
        """获取平均延迟（毫秒）"""
        with self._lock:
            history = self._history.get(model_name, [])
            if not history:
                return 0.0
            return sum(h["latency_ms"] for h in history) / len(history)

    def get_success_rate(self, model_name: str) -> float:
        """获取成功率"""
        with self._lock:
            stats = self._stats.get(model_name, {})
            total = stats.get("total", 0)
            if total == 0:
                return 1.0
            return stats.get("success", 0) / total

    def is_model_healthy(self, model_name: str) -> bool:
        """判断模型是否健康（成功率 > 50% 且 平均延迟 < 阈值）"""
        success_rate = self.get_success_rate(model_name)
        avg_latency = self.get_avg_latency(model_name)
        return success_rate > 0.5 and avg_latency < 30_000

    def get_stats(self) -> Dict[str, Any]:
        """获取所有模型统计"""
        with self._lock:
            result = {}
            for name, stats in self._stats.items():
                result[name] = {
                    **stats,
                    "avg_latency_ms": self.get_avg_latency(name),
                    "success_rate": self.get_success_rate(name),
                    "healthy": self.is_model_healthy(name),
                }
            return result


# ═══════════════════════════════════════════════════════════════
# 双模型调度服务
# ═══════════════════════════════════════════════════════════════

class DualModelService:
    """
    双模型平行调度服务 - A/B左右大脑

    核心机制：
    1. 优先调用A模型（左脑/主脑）
    2. A模型在以下情况自动切换B模型（右脑/副脑）：
       - 响应超时
       - 熔断器开启
       - 调用错误
       - 延迟过高
    3. B模型同样具备完整LLM能力
    4. 对外接口与 LLMService 完全兼容

    用法：
        # 通过 SomnCore 自动获取
        response = somn_core.dual_model_service.chat("你好")

        # 替代原来的 llm_service 调用
        response = dual_model.chat(prompt, model=None, system_prompt="...")
    """

    def __init__(
        self,
        llm_service,  # LLMService 实例
        config: Optional[DualModelConfig] = None,
    ):
        self._llm = llm_service
        self._config = config or DualModelConfig()
        self._perf = PerformanceTracker() if self._config.track_performance else None
        self._lock = threading.Lock()

        # 主脑冷却（切换后暂时不尝试主脑）
        self._primary_cooldown_until: float = 0.0
        
        # [v1.1.0] 本地引擎直接引用
        self._local_engine_a = None
        self._local_engine_b = None
        self._local_engines_initialized = False

        # 从环境变量覆盖配置
        self._load_env_config()
        
        # [v1.1.0] 初始化本地引擎
        self._init_local_engines()
    
    def _init_local_engines(self):
        """[v2.0] 初始化本地引擎直接引用
        
        注意：
        - _local_engine_a = A模型（Llama 3.2 1B，副脑）
        - _local_engine_b = B模型（Gemma4多模态，主脑）
        """
        if self._local_engines_initialized:
            return
        
        try:
            from src.core.local_llm_engine import get_engine, get_engine_b
            # A引擎（Llama，副脑）
            self._local_engine_a = get_engine()
            # B引擎（Gemma4，主脑）
            self._local_engine_b = get_engine_b()
            self._local_engines_initialized = True
            logger.info("[DualModel] 本地引擎A/B引用已建立，B=主脑/A=副脑")
        except ImportError:
            logger.warning("[DualModel] 本地引擎模块未找到，将使用LLMService代理")
        except Exception as e:
            logger.warning(f"[DualModel] 本地引擎初始化失败: {e}")

        logger.info(
            f"[DualModel] 初始化完成: "
            f"左脑(B主脑)={self._config.primary_model}, "
            f"右脑(A副脑)={self._config.fallback_model}"
        )

        # [v2.0] 初始化能力模型评分
        self._init_capability_scores()

    # ══════════════════════════════════════════════════════════
    # [v2.0] 能力感知调度系统
    # ══════════════════════════════════════════════════════════

    def _init_capability_scores(self):
        """[v2.0] 初始化模型能力评分表

        评分标准：0=无此能力, 1=基础, 2=良好, 3=优秀
        """
        # 模型能力评分（相对于其他模型的比例）
        # 格式: {model_id: {TaskCapability: score}}
        self._capability_scores = {
            # B模型 - Gemma4 多模态 (主脑)
            "gemma4-local-b": {
                TaskCapability.VISION: 3,      # 多模态，视觉能力优秀
                TaskCapability.CODE: 2,         # 代码能力良好
                TaskCapability.ANALYSIS: 3,    # 分析能力强
                TaskCapability.CHAT: 2,         # 对话能力良好
                TaskCapability.CREATIVE: 2,     # 创意能力良好
                TaskCapability.REASONING: 3,    # 推理能力强
            },
            # A模型 - Llama 3.2 1B (副脑)
            "llama3-local-a": {
                TaskCapability.VISION: 0,       # 不支持视觉
                TaskCapability.CODE: 2,         # 代码能力良好
                TaskCapability.ANALYSIS: 2,     # 分析能力中等
                TaskCapability.CHAT: 3,          # 对话能力强
                TaskCapability.CREATIVE: 2,     # 创意能力良好
                TaskCapability.REASONING: 1,    # 推理能力基础
            },
            # 云端模型 - 可通过add_cloud_model动态注册
        }

    def _analyze_input_capabilities(
        self,
        prompt: str = None,
        messages: List[Dict] = None,
        **kwargs
    ) -> Dict[TaskCapability, int]:
        """
        [v2.0] 分析输入内容，识别所需能力及强度

        Args:
            prompt: 字符串提示词
            messages: 消息列表 [{"role": "user", "content": "...", "image_urls": [...]}]

        Returns:
            能力需求字典 {TaskCapability: 强度(1-3)}
        """
        required = {}

        # 合并所有文本内容用于分析
        texts = []
        has_images = False

        if prompt:
            texts.append(prompt)

        if messages:
            for msg in messages:
                content = msg.get("content", "")
                if isinstance(content, str):
                    texts.append(content)
                elif isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict):
                            if item.get("type") == "text":
                                texts.append(item.get("text", ""))
                            elif item.get("type") == "image_url":
                                has_images = True
                        elif isinstance(item, str):
                            texts.append(item)
                            # 检测是否为图片URL
                            if item.startswith("http") and any(
                                item.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]
                            ):
                                has_images = True

                # 检查image_urls字段
                if msg.get("image_urls"):
                    has_images = True

        combined_text = " ".join(texts).lower()

        # 1. 视觉能力检测（图片输入）
        if has_images or any(k in combined_text for k in [
            "图片", "图像", "看图", "描述这张图", "what's in this image",
            "describe the image", "image", "照片", "截图"
        ]):
            required[TaskCapability.VISION] = 3

        # 2. 代码能力检测
        code_keywords = [
            "代码", "写代码", "python", "javascript", "java", "rust", "go",
            "编程", "function", "def ", "class ", "import ", "算法",
            "code", "programming", "implement", "bug", "debug"
        ]
        if any(k in combined_text for k in code_keywords):
            required[TaskCapability.CODE] = 2

        # 检测代码块
        if "```" in combined_text:
            required[TaskCapability.CODE] = max(required.get(TaskCapability.CODE, 0), 2)

        # 3. 分析能力检测
        analysis_keywords = [
            "分析", "对比", "评估", "研究", "调查", "报告",
            "analyze", "compare", "evaluate", "research", "study",
            "数据", "统计", "趋势", "洞察"
        ]
        if any(k in combined_text for k in analysis_keywords):
            required[TaskCapability.ANALYSIS] = 2

        # 4. 创意能力检测
        creative_keywords = [
            "创作", "写诗", "写小说", "故事", "创意", "想象",
            "creative", "story", "write a", "imagine", "poem"
        ]
        if any(k in combined_text for k in creative_keywords):
            required[TaskCapability.CREATIVE] = 2

        # 5. 推理能力检测
        reasoning_keywords = [
            "推理", "逻辑", "思考", "证明", "为什么", "原因",
            "reasoning", "logic", "think", "prove", "why", "because"
        ]
        if any(k in combined_text for k in reasoning_keywords):
            required[TaskCapability.REASONING] = 2

        # 6. 默认对话能力
        if not required:
            required[TaskCapability.CHAT] = 1

        return required

    def _select_best_model_for_capabilities(
        self,
        required_capabilities: Dict[TaskCapability, int]
    ) -> BrainRole:
        """
        [v2.0] 根据能力需求选择最佳模型

        Args:
            required_capabilities: 所需能力字典

        Returns:
            最佳匹配的BrainRole
        """
        # 候选模型
        candidates = [
            (BrainRole.LEFT, "gemma4-local-b"),   # B模型 - Gemma4多模态
            (BrainRole.RIGHT, "llama3-local-a"),  # A模型 - Llama
        ]

        # 获取云端注册模型
        if hasattr(self, '_llm') and hasattr(self._llm, 'configs'):
            for name, config in self._llm.configs.items():
                # 跳过预设模型
                if name.startswith('preset_'):
                    continue
                # 云端模型使用默认中等能力
                if config.provider.value not in ("local", "mock"):
                    self._capability_scores[name] = {
                        TaskCapability.VISION: 1 if "vision" in str(config.capabilities) else 0,
                        TaskCapability.CODE: 2,
                        TaskCapability.ANALYSIS: 2,
                        TaskCapability.CHAT: 2,
                        TaskCapability.CREATIVE: 2,
                        TaskCapability.REASONING: 2,
                    }
                    candidates.append((None, name))  # None表示通过LLMService调度

        # 计算每个模型的综合得分
        best_role = BrainRole.LEFT  # 默认B模型
        best_score = -1

        for role, model_id in candidates:
            model_scores = self._capability_scores.get(model_id, {})
            if not model_scores:
                continue

            total_score = 0
            has_mandatory = False  # 是否有必须使用主脑的能力

            for cap, need_level in required_capabilities.items():
                model_level = model_scores.get(cap, 0)
                # 满足需求则加分，不满足则扣分
                if model_level >= need_level:
                    total_score += model_level * 10  # 满足需求，加分
                elif model_level > 0:
                    total_score += model_level * 5   # 部分满足，半分
                # model_level == 0 不扣分（备用方案）

                # VISION能力必须使用主脑(B脑/Gemma4)
                if cap == TaskCapability.VISION and need_level > 0:
                    has_mandatory = True

            if total_score > best_score:
                best_score = total_score
                best_role = role if role else BrainRole.LEFT
            elif total_score == best_score and total_score > 0 and best_score > 0:
                # 得分相同时，优先使用副脑节省主脑资源
                # 除非该任务必须使用主脑（如视觉任务）
                if not has_mandatory and role == BrainRole.RIGHT:
                    best_role = BrainRole.RIGHT  # 优先副脑

        logger.info(
            f"[CapabilityDispatcher] 能力需求: {required_capabilities}, "
            f"选择: {best_role.value}, 得分: {best_score}"
        )
        return best_role

    def _has_multimodal_content(
        self,
        prompt: str = None,
        messages: List[Dict] = None,
    ) -> bool:
        """[v2.1] 检测是否包含多模态内容（图片等）

        Returns:
            True 如果检测到图片或其他多模态内容
        """
        # 检测prompt中的图片URL
        if prompt:
            prompt_lower = prompt.lower()
            if any(prompt_lower.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]):
                return True
            if "image" in prompt_lower and ("http" in prompt_lower or "data:" in prompt_lower):
                return True

        # 检测messages中的图片
        if messages:
            for msg in messages:
                content = msg.get("content", "")
                if isinstance(content, str) and content:
                    content_lower = content.lower()
                    if any(content_lower.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]):
                        return True
                    if "image" in content_lower and ("http" in content_lower or "data:" in content_lower):
                        return True
                elif isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict):
                            if item.get("type") == "image_url":
                                return True
                if msg.get("image_urls"):
                    return True

        return False

    def _messages_to_prompt(
        self,
        messages: List[Dict],
        system_prompt: str = None,
    ) -> str:
        """[v2.1] 将messages列表转换为纯文本prompt

        用于本地引擎不支持多模态时的降级处理。
        """
        parts = []

        if system_prompt:
            parts.append(f"[系统提示] {system_prompt}")

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if isinstance(content, str):
                parts.append(f"[{role}] {content}")
            elif isinstance(content, list):
                # 处理多模态content
                text_parts = []
                for item in content:
                    if isinstance(item, dict):
                        if item.get("type") == "text":
                            text_parts.append(item.get("text", ""))
                        elif item.get("type") == "image_url":
                            text_parts.append("[图片]")
                    elif isinstance(item, str):
                        text_parts.append(item)
                if text_parts:
                    parts.append(f"[{role}] {' '.join(text_parts)}")

        return "\n".join(parts)

    def _has_cloud_service(self) -> bool:
        """[v2.2] 检测是否有可用的云端服务

        Returns:
            True 如果配置了云端模型
        """
        # 检查LLMService中是否有云端模型
        if hasattr(self, '_llm') and hasattr(self._llm, 'configs'):
            for name, config in self._llm.configs.items():
                # 跳过预设模型和本地模型
                if name.startswith('preset_'):
                    continue
                provider = getattr(config, 'provider', None)
                if provider:
                    provider_val = provider.value if hasattr(provider, 'value') else str(provider)
                    if provider_val not in ("local", "mock", ""):
                        return True
        return False

    def _dispatch_local_with_multimodal_fallback(
        self,
        prompt: str,
        brain_role: BrainRole,
        system_prompt: str = None,
        temperature: float = None,
        max_tokens: int = None,
    ) -> DualModelResponse:
        """[v2.2] 本地引擎调度，支持多模态降级

        当本地引擎不支持多模态时，使用智能模板引擎降级处理。
        """
        try:
            return self._dispatch_local(
                prompt=prompt,
                brain_role=brain_role,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except (RuntimeError, AttributeError) as e:
            # 本地引擎不支持，尝试使用LLMService的降级模式
            logger.warning(f"[CapabilityDispatcher] 本地引擎失败: {e}，尝试降级")
            try:
                raw_resp = self._llm.chat(
                    prompt,
                    model=None,  # 让LLMService选择默认模型
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                return DualModelResponse(
                    content=raw_resp.content,
                    model=raw_resp.model,
                    provider=raw_resp.provider,
                    usage=raw_resp.usage,
                    finish_reason=raw_resp.finish_reason,
                    latency_ms=0,
                    timestamp=raw_resp.timestamp,
                    brain_used="fallback",
                    failover=True,
                    failover_reason="local_engine_unsupported",
                )
            except Exception as llm_error:
                # 最终降级：返回友好的错误信息
                logger.error(f"[CapabilityDispatcher] 所有引擎都失败: {llm_error}")
                return DualModelResponse(
                    content=f"[提示] 当前系统未配置云端服务，无法处理多模态内容（图片输入）。请配置支持视觉的云端模型（如GPT-4V、Claude等）来处理图片相关任务。",
                    model="none",
                    provider="local",
                    usage={"prompt_tokens": 0, "completion_tokens": 0},
                    finish_reason="error",
                    latency_ms=0,
                    brain_used="none",
                    failover=True,
                    failover_reason="no_multimodal_support",
                )

    def dispatch_by_capability(
        self,
        prompt: str = None,
        messages: List[Dict] = None,
        system_prompt: str = None,
        temperature: float = None,
        max_tokens: int = None,
        **kwargs
    ) -> DualModelResponse:
        """
        [v2.2] 能力感知调度 - 根据任务需求自动选择最佳模型

        调度策略：
        - 有云端服务 + 多模态 → 云端服务
        - 无云端服务 + 多模态 → 本地引擎降级处理（图片转为文本提示）
        - 纯文本输入 → 本地引擎

        用法示例：
            # 图片输入 → 自动选择视觉能力强的模型
            response = dual.dispatch_by_capability(
                messages=[{"role": "user", "content": "描述这张图片", "image_urls": ["xxx.jpg"]}]
            )

            # 代码分析 → 自动选择代码能力强的模型
            response = dual.dispatch_by_capability(
                prompt="分析这段Python代码"
            )

        Args:
            prompt: 提示词（字符串形式）
            messages: 消息列表（支持图片等多模态内容）
            system_prompt: 系统提示
            temperature: 温度
            max_tokens: 最大token数

        Returns:
            DualModelResponse格式的响应
        """
        # 1. 分析输入所需能力
        required_caps = self._analyze_input_capabilities(prompt=prompt, messages=messages, **kwargs)

        # 2. 选择最佳模型
        best_role = self._select_best_model_for_capabilities(required_caps)

        # 3. 检查是否包含多模态内容
        has_multimodal = self._has_multimodal_content(prompt=prompt, messages=messages)

        if has_multimodal:
            # 有多模态内容
            if self._has_cloud_service():
                # 有云端服务 → 降级到云端
                logger.info(f"[CapabilityDispatcher] 检测到多模态内容，有云端服务，降级到云端")
                combined_prompt = prompt or ""
                if messages:
                    combined_prompt = combined_prompt or self._messages_to_prompt(messages, system_prompt)
                return self._dispatch_dual(
                    combined_prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    conversation_id=kwargs.get("conversation_id"),
                )
            else:
                # 无云端服务 → 使用本地引擎降级处理
                logger.info(f"[CapabilityDispatcher] 检测到多模态内容，无云端服务，使用本地引擎")
                combined_prompt = self._messages_to_prompt(messages, system_prompt) if messages else (prompt or "")
                return self._dispatch_local_with_multimodal_fallback(
                    prompt=combined_prompt,
                    brain_role=best_role,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

        # 4. 执行调度（纯文本输入，使用本地引擎）
        # LEFT = B脑(主脑,Gemma4), RIGHT = A脑(副脑,Llama)
        return self._dispatch_local(
            prompt=prompt or "",
            brain_role=best_role,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def get_capability_matrix(self) -> Dict[str, Dict[str, Any]]:
        """
        [v2.0] 获取当前所有模型的能力矩阵

        Returns:
            模型能力矩阵
        """
        matrix = {}
        for model_id, scores in self._capability_scores.items():
            matrix[model_id] = {
                cap.value: level for cap, level in scores.items()
            }
        return matrix

    def _load_env_config(self):
        """从环境变量加载配置"""
        # A模型（左脑）
        env_primary = os.getenv("SOMN_DUAL_PRIMARY_MODEL", "").strip()
        if env_primary:
            self._config.primary_model = env_primary

        env_primary_timeout = os.getenv("SOMN_DUAL_PRIMARY_TIMEOUT_MS", "").strip()
        if env_primary_timeout:
            self._config.primary_timeout_ms = int(env_primary_timeout)

        # B模型（右脑）
        env_fallback = os.getenv("SOMN_DUAL_FALLBACK_MODEL", "").strip()
        if env_fallback:
            self._config.fallback_model = env_fallback

        env_fallback_timeout = os.getenv("SOMN_DUAL_FALLBACK_TIMEOUT_MS", "").strip()
        if env_fallback_timeout:
            self._config.fallback_timeout_ms = int(env_fallback_timeout)

        # 是否自动切换
        env_auto = os.getenv("SOMN_DUAL_AUTO_FAILOVER", "").strip().lower()
        if env_auto in ("0", "false", "no"):
            self._config.auto_failover = False
        elif env_auto in ("1", "true", "yes"):
            self._config.auto_failover = True

    # ══════════════════════════════════════════════════════════
    # 公开接口 - 与 LLMService 完全兼容
    # ══════════════════════════════════════════════════════════

    def chat(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: str = None,
        temperature: float = None,
        max_tokens: int = None,
        conversation_id: str = None,
        prefer_local: bool = True,
        messages: List[Dict] = None,
        use_capability_dispatch: bool = None,
    ) -> DualModelResponse:
        """
        对话接口 - 与 LLMService.chat() 完全兼容 [v2.0]

        如果指定了 model，则直接使用该模型（不触发双模型切换）。
        如果 model=None 且 prefer_local=True，则优先使用本地A/B引擎。
        如果 model=None 且 prefer_local=False，则使用云端模型调度。
        如果 use_capability_dispatch=True，则根据输入内容自动选择最佳模型。

        Args:
            prefer_local: [v1.1.0] 是否优先使用本地引擎（默认True）
            messages: [v2.0] 消息列表，支持图片等多模态内容
            use_capability_dispatch: [v2.0] 是否启用能力感知调度（默认False）
                - True: 自动分析输入内容，选择能力最强的模型
                - False: 使用传统调度策略（主脑优先）
        """
        # 指定了模型 → 直连模式，不触发切换
        if model is not None:
            return self._call_single(
                prompt, model, system_prompt, temperature, max_tokens,
                conversation_id, brain_role=BrainRole.LEFT
            )

        # [v2.0] 能力感知调度（自动检测多模态内容）
        if use_capability_dispatch or (use_capability_dispatch is None and messages):
            return self.dispatch_by_capability(
                prompt=prompt,
                messages=messages,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )

        # [v1.1.0] 优先使用本地引擎
        if prefer_local:
            return self._dispatch_dual_with_local_fallback(
                prompt, system_prompt, temperature, max_tokens, conversation_id
            )

        # 降级到云端模型调度
        return self._dispatch_dual(
            prompt, system_prompt, temperature, max_tokens, conversation_id
        )

    def analyze(
        self,
        text: str,
        task: str,
        context: str = "",
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """分析文本 - 与 LLMService.analyze() 兼容"""
        task_prompts = {
            "sentiment": f"分析以下文本的情感倾向(正面/负面/中性),并给出置信度:\n\n{text}",
            "summary": f"总结以下文本的核心要点(3-5条):\n\n{text}",
            "keywords": f"提取以下文本的关键词(5-10个):\n\n{text}",
            "classification": f"将以下文本分类,给出类别和置信度:\n\n{text}",
            "growth_insight": f"基于以下数据提供增长洞察和建议:\n\n{text}\n\n上下文:{context}",
        }

        prompt = task_prompts.get(task, f"分析以下内容:\n\n{text}")
        system_prompt = "你是一个专业的增长strategy分析师,擅长从数据中提取洞察并提供可执行建议."

        response = self.chat(
            prompt, model=model, system_prompt=system_prompt
        )

        return {
            "task": task,
            "analysis": response.content,
            "model": response.model,
            "provider": response.provider,
            "timestamp": response.timestamp,
            "brain_used": response.brain_used,
            "failover": response.failover,
        }

    def generate_strategy(
        self,
        context: Dict[str, Any],
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """生成增长策略 - 与 LLMService.generate_strategy() 兼容"""
        prompt = f"""基于以下背景信息,generate具体的增长strategy方案:

行业: {context.get('industry', '未知')}
阶段: {context.get('stage', '未知')}
目标: {context.get('objective', '未知')}
当前数据: {json.dumps(context.get('metrics', {}), ensure_ascii=False)}
约束条件: {json.dumps(context.get('constraints', []), ensure_ascii=False)}
补充上下文: {json.dumps(context.get('context', {}), ensure_ascii=False)}

请提供:
1. strategy概述(1-2句话)
2. 核心strategy(3-5条,每条包含:strategy名称,具体做法,预期效果)
3. 执行步骤(时间线)
4. 关键metrics
5. 风险提示
"""

        system_prompt = "你是一个资深的增长strategy专家,擅长制定数据驱动,可落地的增长方案."
        response = self.chat(
            prompt,
            model=model,
            system_prompt=system_prompt,
            max_tokens=3000,
            temperature=0.3,
        )

        return {
            "strategy_text": response.content,
            "context": context,
            "model": response.model,
            "provider": response.provider,
            "generated_at": response.timestamp,
            "brain_used": response.brain_used,
            "failover": response.failover,
        }

    # ══════════════════════════════════════════════════════════
    # 核心：双模型调度逻辑
    # ══════════════════════════════════════════════════════════

    def _dispatch_dual(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = None,
        max_tokens: int = None,
        conversation_id: str = None,
    ) -> DualModelResponse:
        """
        双模型调度核心

        流程：
        1. 检查A模型（左脑）是否可用
        2. 可用 → 调用A模型，设置超时
        3. A模型失败/超时 → 自动切换B模型（右脑）
        4. 记录性能数据
        """
        primary_model = self._config.primary_model
        fallback_model = self._config.fallback_model

        # ── 检查主脑是否在冷却期 ──
        if self._is_primary_cooling_down():
            logger.info(f"[DualModel] 左脑冷却中，直接使用右脑(B={fallback_model})")
            return self._call_single(
                prompt, fallback_model, system_prompt, temperature, max_tokens,
                conversation_id, brain_role=BrainRole.RIGHT,
                failover=True, failover_reason=FailoverReason.LATENCY_HIGH.value,
            )

        # ── 检查主脑熔断状态 ──
        if self._config.failover_on_circuit_open:
            from src.utils.retry_utils import get_circuit_breaker
            primary_cb = get_circuit_breaker(
                f"dual-primary-{primary_model}",
                failure_threshold=3,
                recovery_timeout=30.0,
            )
            if not primary_cb.is_available():
                logger.info(f"[DualModel] 左脑熔断中，切换右脑(B={fallback_model})")
                return self._call_single(
                    prompt, fallback_model, system_prompt, temperature, max_tokens,
                    conversation_id, brain_role=BrainRole.RIGHT,
                    failover=True, failover_reason=FailoverReason.CIRCUIT_OPEN.value,
                )

        # ── 检查性能追踪 ──
        if self._perf and self._config.failover_on_latency:
            if not self._perf.is_model_healthy(primary_model):
                avg_lat = self._perf.get_avg_latency(primary_model)
                logger.info(
                    f"[DualModel] 左脑不健康(avg={avg_lat:.0f}ms)，切换右脑(B={fallback_model})"
                )
                return self._call_single(
                    prompt, fallback_model, system_prompt, temperature, max_tokens,
                    conversation_id, brain_role=BrainRole.RIGHT,
                    failover=True, failover_reason=FailoverReason.LATENCY_HIGH.value,
                )

        # ── 尝试调用A模型（左脑） ──
        primary_start = time.time()
        try:
            # 使用线程+超时控制
            result_holder = [None]
            error_holder = [None]

            def _call_primary():
                try:
                    from src.tool_layer.llm_service import LLMResponse
                    raw_resp = self._llm.chat(
                        prompt,
                        model=primary_model,
                        system_prompt=system_prompt,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        conversation_id=conversation_id,
                    )
                    result_holder[0] = raw_resp
                except Exception as e:
                    error_holder[0] = e

            t = threading.Thread(target=_call_primary, daemon=True)
            t.start()
            timeout_sec = self._config.primary_timeout_ms / 1000.0
            t.join(timeout=timeout_sec)

            primary_latency_ms = int((time.time() - primary_start) * 1000)

            if t.is_alive():
                # A模型超时
                logger.warning(
                    f"[DualModel] 左脑超时({timeout_sec:.1f}s)，切换右脑(B={fallback_model})"
                )
                self._record_perf(primary_model, primary_latency_ms, success=False)
                self._enter_primary_cooldown()

                if self._config.auto_failover:
                    return self._call_single(
                        prompt, fallback_model, system_prompt, temperature, max_tokens,
                        conversation_id, brain_role=BrainRole.RIGHT,
                        failover=True, failover_reason=FailoverReason.TIMEOUT.value,
                        primary_latency_ms=primary_latency_ms,
                    )

            if error_holder[0] is not None:
                # A模型错误
                logger.warning(
                    f"[DualModel] 左脑错误: {error_holder[0]}，切换右脑(B={fallback_model})"
                )
                self._record_perf(primary_model, primary_latency_ms, success=False)

                if self._config.auto_failover and self._config.failover_on_error:
                    self._enter_primary_cooldown()
                    return self._call_single(
                        prompt, fallback_model, system_prompt, temperature, max_tokens,
                        conversation_id, brain_role=BrainRole.RIGHT,
                        failover=True, failover_reason=FailoverReason.ERROR.value,
                        primary_latency_ms=primary_latency_ms,
                    )

            raw_resp = result_holder[0]
            if raw_resp is not None:
                # A模型成功
                self._record_perf(primary_model, primary_latency_ms, success=True)

                # 检查响应是否为错误响应
                if hasattr(raw_resp, 'finish_reason') and raw_resp.finish_reason == "error":
                    logger.warning(
                        f"[DualModel] 左脑返回错误响应，切换右脑(B={fallback_model})"
                    )
                    if self._config.auto_failover and self._config.failover_on_error:
                        return self._call_single(
                            prompt, fallback_model, system_prompt, temperature, max_tokens,
                            conversation_id, brain_role=BrainRole.RIGHT,
                            failover=True, failover_reason=FailoverReason.ERROR.value,
                            primary_latency_ms=primary_latency_ms,
                        )

                return DualModelResponse(
                    content=raw_resp.content,
                    model=raw_resp.model,
                    provider=raw_resp.provider,
                    usage=raw_resp.usage,
                    finish_reason=raw_resp.finish_reason,
                    latency_ms=primary_latency_ms,
                    timestamp=raw_resp.timestamp,
                    brain_used=BrainRole.LEFT.value,
                    failover=False,
                    failover_reason="",
                    primary_latency_ms=primary_latency_ms,
                    fallback_latency_ms=0,
                )

        except Exception as e:
            primary_latency_ms = int((time.time() - primary_start) * 1000)
            logger.error(f"[DualModel] 左脑异常: {e}")
            self._record_perf(primary_model, primary_latency_ms, success=False)

            if self._config.auto_failover and self._config.failover_on_error:
                self._enter_primary_cooldown()
                return self._call_single(
                    prompt, fallback_model, system_prompt, temperature, max_tokens,
                    conversation_id, brain_role=BrainRole.RIGHT,
                    failover=True, failover_reason=FailoverReason.ERROR.value,
                    primary_latency_ms=primary_latency_ms,
                )

        # 兜底：直接使用B模型
        return self._call_single(
            prompt, fallback_model, system_prompt, temperature, max_tokens,
            conversation_id, brain_role=BrainRole.RIGHT,
            failover=True, failover_reason=FailoverReason.NOT_AVAILABLE.value,
        )

    def _call_single(
        self,
        prompt: str,
        model: str,
        system_prompt: str = None,
        temperature: float = None,
        max_tokens: int = None,
        conversation_id: str = None,
        brain_role: BrainRole = BrainRole.LEFT,
        failover: bool = False,
        failover_reason: str = "",
        primary_latency_ms: int = 0,
    ) -> DualModelResponse:
        """调用单个模型"""
        start = time.time()
        try:
            raw_resp = self._llm.chat(
                prompt,
                model=model,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                conversation_id=conversation_id,
            )
            latency_ms = int((time.time() - start) * 1000)
            self._record_perf(model, latency_ms, success=True)

            return DualModelResponse(
                content=raw_resp.content,
                model=raw_resp.model,
                provider=raw_resp.provider,
                usage=raw_resp.usage,
                finish_reason=raw_resp.finish_reason,
                latency_ms=latency_ms,
                timestamp=raw_resp.timestamp,
                brain_used=brain_role.value,
                failover=failover,
                failover_reason=failover_reason,
                primary_latency_ms=primary_latency_ms if failover else 0,
                fallback_latency_ms=latency_ms if failover else 0,
            )

        except Exception as e:
            latency_ms = int((time.time() - start) * 1000)
            self._record_perf(model, latency_ms, success=False)
            logger.error(f"[DualModel] {brain_role.value}脑({model})调用失败: {e}")

            return DualModelResponse(
                content=f"[DualModel] {brain_role.value}脑调用失败",
                model=model,
                provider="unknown",
                usage={"prompt_tokens": 0, "completion_tokens": 0},
                finish_reason="error",
                latency_ms=latency_ms,
                brain_used=brain_role.value,
                failover=failover,
                failover_reason=failover_reason or FailoverReason.ERROR.value,
                primary_latency_ms=primary_latency_ms,
                fallback_latency_ms=latency_ms,
            )
    
    # ══════════════════════════════════════════════════════════
    # [v1.1.0] 本地引擎直接调度
    # ══════════════════════════════════════════════════════════
    
    def _dispatch_local(
        self,
        prompt: str,
        brain_role: BrainRole = BrainRole.LEFT,
        system_prompt: str = None,
        temperature: float = None,
        max_tokens: int = None,
        **kwargs
    ) -> DualModelResponse:
        """
        [v1.1.0] 直接调度到本地引擎（A/B模型）
        
        优先使用本地引擎进行推理，减少网络开销。
        如果本地引擎不可用，自动降级到LLMService。
        
        Args:
            prompt: 提示词
            brain_role: 使用哪个大脑 (LEFT=A模型, RIGHT=B模型)
            system_prompt: 系统提示
            temperature: 温度
            max_tokens: 最大token数
            **kwargs: 其他参数
        
        Returns:
            DualModelResponse格式的响应
        """
        start = time.time()
        
        # [v2.0] 选择引擎 - LEFT=B脑(主脑), RIGHT=A脑(副脑)
        engine = self._local_engine_b if brain_role == BrainRole.LEFT else self._local_engine_a
        if engine is None:
            raise RuntimeError(f"{brain_role.value}脑引擎未初始化")
        
        # 构建完整提示（含系统提示）
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{full_prompt}"
        
        # 检查引擎状态
        if not engine.is_ready:
            logger.warning(f"[DualModel] {brain_role.value}脑未就绪，尝试启动...")
            if not engine.start(timeout=30.0):
                raise RuntimeError(f"{brain_role.value}脑启动失败")
        
        try:
            # 调用本地引擎
            result = engine.generate(
                full_prompt,
                temperature=temperature or 0.7,
                max_new_tokens=max_tokens or 512,
                request_timeout=kwargs.get("request_timeout", 120.0)
            )
            
            latency_ms = int((time.time() - start) * 1000)
            self._record_perf(engine.model_name, latency_ms, success=True)
            
            return DualModelResponse(
                content=result.text,
                model=engine.model_name,
                provider="local",
                usage={"prompt_tokens": 0, "completion_tokens": result.tokens},
                finish_reason=result.finish_reason,
                latency_ms=latency_ms,
                brain_used=brain_role.value,
                failover=False,
                failover_reason=""
            )
            
        except Exception as e:
            latency_ms = int((time.time() - start) * 1000)
            self._record_perf(engine.model_name, latency_ms, success=False)
            logger.error(f"[DualModel] {brain_role.value}脑调用失败: {e}")
            
            raise RuntimeError(f"{brain_role.value}脑调用失败: {e}")
    
    def _dispatch_dual_with_local_fallback(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = None,
        max_tokens: int = None,
        conversation_id: str = None,
    ) -> DualModelResponse:
        """
        [v1.1.0] 双模型调度（优先本地引擎）
        
        优先尝试本地A/B引擎，失败时降级到云端模型。
        """
        # 确保本地引擎已初始化
        if not self._local_engines_initialized:
            self._init_local_engines()
        
        # [v2.0] 优先尝试本地B模型（主脑，Gemma4多模态）
        if self._local_engine_b and self._local_engine_b.is_ready:
            try:
                return self._dispatch_local(
                    prompt, BrainRole.LEFT, system_prompt, temperature, max_tokens
                )
            except Exception as e:
                logger.warning(f"[DualModel] 本地B脑(主脑)失败，尝试A脑: {e}")
        
        # 尝试本地A模型（副脑，Llama 3.2 1B）
        if self._local_engine_a and self._local_engine_a.is_ready:
            try:
                return self._dispatch_local(
                    prompt, BrainRole.RIGHT, system_prompt, temperature, max_tokens
                )
            except Exception as e2:
                logger.warning(f"[DualModel] 本地A脑(副脑)也失败: {e2}")
        
        # 降级到LLMService
        logger.info("[DualModel] 本地引擎不可用，降级到LLMService")
        return self._dispatch_dual(
            prompt, system_prompt, temperature, max_tokens, conversation_id
        )

    # ══════════════════════════════════════════════════════════
    # 辅助方法
    # ══════════════════════════════════════════════════════════

    def _record_perf(self, model_name: str, latency_ms: float, success: bool):
        """记录性能数据"""
        if self._perf:
            self._perf.record(model_name, latency_ms, success)

    def _is_primary_cooling_down(self) -> bool:
        """主脑是否在冷却期"""
        return time.time() < self._primary_cooldown_until

    def _enter_primary_cooldown(self):
        """进入主脑冷却"""
        self._primary_cooldown_until = time.time() + self._config.primary_cooldown_seconds
        logger.info(
            f"[DualModel] 左脑进入冷却({self._config.primary_cooldown_seconds}s)"
        )

    # ══════════════════════════════════════════════════════════
    # 兼容 LLMService 的代理方法
    # ══════════════════════════════════════════════════════════

    def get_default_model(self) -> str:
        """获取默认模型（主脑）"""
        return self._config.primary_model

    def get_model_info(self, model: str = None) -> Dict[str, Any]:
        """获取模型信息"""
        return self._llm.get_model_info(model)

    def list_available_models(self) -> Dict[str, Any]:
        """列出所有可用模型"""
        return self._llm.list_available_models()

    def register_model(self, name: str, config):
        """注册模型"""
        self._llm.register_model(name, config)

    def add_cloud_model(self, name: str, provider: str, model_name: str,
                        api_base: str, api_key: str = None,
                        temperature: float = 0.7, max_tokens: int = 2000):
        """动态添加云端模型"""
        self._llm.add_cloud_model(name, provider, model_name, api_base, api_key,
                                  temperature, max_tokens)

    def configure_from_env(self):
        """从环境变量配置"""
        self._llm.configure_from_env()

    def test_connection(self, model: str = None) -> Dict[str, Any]:
        """测试模型连接"""
        return self._llm.test_connection(model)

    # ══════════════════════════════════════════════════════════
    # 双模型专属接口
    # ══════════════════════════════════════════════════════════

    def get_brain_status(self) -> Dict[str, Any]:
        """获取双大脑状态"""
        from src.utils.retry_utils import get_circuit_breaker
        primary = self._config.primary_model
        fallback = self._config.fallback_model

        primary_cb = get_circuit_breaker(
            f"dual-primary-{primary}", failure_threshold=3, recovery_timeout=30.0
        )
        fallback_cb = get_circuit_breaker(
            f"dual-fallback-{fallback}", failure_threshold=5, recovery_timeout=30.0
        )

        left = BrainStatus(
            role=BrainRole.LEFT,
            model_name=primary,
            provider=self._get_provider(primary),
            is_available=not self._is_primary_cooling_down() and primary_cb.is_available(),
            avg_latency_ms=self._perf.get_avg_latency(primary) if self._perf else 0,
            success_count=self._perf._stats.get(primary, {}).get("success", 0) if self._perf else 0,
            fail_count=self._perf._stats.get(primary, {}).get("fail", 0) if self._perf else 0,
            circuit_state=primary_cb.state.value,
        )

        right = BrainStatus(
            role=BrainRole.RIGHT,
            model_name=fallback,
            provider=self._get_provider(fallback),
            is_available=fallback_cb.is_available(),
            avg_latency_ms=self._perf.get_avg_latency(fallback) if self._perf else 0,
            success_count=self._perf._stats.get(fallback, {}).get("success", 0) if self._perf else 0,
            fail_count=self._perf._stats.get(fallback, {}).get("fail", 0) if self._perf else 0,
            circuit_state=fallback_cb.state.value,
        )

        return {
            "left_brain": {
                "role": left.role.value,
                "model": left.model_name,
                "provider": left.provider,
                "available": left.is_available,
                "avg_latency_ms": left.avg_latency_ms,
                "success_count": left.success_count,
                "fail_count": left.fail_count,
                "circuit_state": left.circuit_state,
                "cooling_down": self._is_primary_cooling_down(),
            },
            "right_brain": {
                "role": right.role.value,
                "model": right.model_name,
                "provider": right.provider,
                "available": right.is_available,
                "avg_latency_ms": right.avg_latency_ms,
                "success_count": right.success_count,
                "fail_count": right.fail_count,
                "circuit_state": right.circuit_state,
            },
            # [v1.1.0] 本地引擎状态
            "local_engines": {
                "initialized": self._local_engines_initialized,
                "engine_a_ready": self._local_engine_a.is_ready if self._local_engine_a else False,
                "engine_b_ready": self._local_engine_b.is_ready if self._local_engine_b else False,
                "engine_a_mode": self._local_engine_a.load_mode if self._local_engine_a else None,
                "engine_b_mode": self._local_engine_b.load_mode if self._local_engine_b else None,
            },
            "config": {
                "primary_model": primary,
                "fallback_model": fallback,
                "auto_failover": self._config.auto_failover,
                "primary_timeout_ms": self._config.primary_timeout_ms,
                "fallback_timeout_ms": self._config.fallback_timeout_ms,
                "latency_threshold_ms": self._config.latency_threshold_ms,
            },
            "performance": self._perf.get_stats() if self._perf else {},
        }

    def set_primary_model(self, model_name: str):
        """手动设置主脑模型"""
        with self._lock:
            self._config.primary_model = model_name
            logger.info(f"[DualModel] 左脑切换为: {model_name}")

    def set_fallback_model(self, model_name: str):
        """手动设置副脑模型"""
        with self._lock:
            self._config.fallback_model = model_name
            logger.info(f"[DualModel] 右脑切换为: {model_name}")

    def force_use_brain(self, role: BrainRole) -> 'DualModelService':
        """
        强制使用指定大脑（上下文管理器模式）

        用法：
            with dual_model.force_use_brain(BrainRole.RIGHT):
                response = dual_model.chat("hello")  # 强制使用右脑
        """
        return _ForceBrainContext(self, role)

    def _get_provider(self, model_name: str) -> str:
        """获取模型的provider"""
        config = self._llm.configs.get(model_name)
        if config:
            return config.provider.value
        return "unknown"


class _ForceBrainContext:
    """强制使用指定大脑的上下文管理器"""

    def __init__(self, dual_service: DualModelService, role: BrainRole):
        self._service = dual_service
        self._role = role
        self._saved_primary = None
        self._saved_fallback = None

    def __enter__(self):
        self._saved_primary = self._service._config.primary_model
        self._saved_fallback = self._service._config.fallback_model
        if self._role == BrainRole.RIGHT:
            # 交换主/副脑
            self._service._config.primary_model = self._saved_fallback
            self._service._config.fallback_model = self._saved_primary
        return self._service

    def __exit__(self, *args):
        self._service._config.primary_model = self._saved_primary
        self._service._config.fallback_model = self._saved_fallback


# ═══════════════════════════════════════════════════════════════
# 全局单例
# ═══════════════════════════════════════════════════════════════

_dual_service: Optional[DualModelService] = None
_dual_lock = threading.Lock()


def get_dual_model_service(llm_service=None, config: Optional[DualModelConfig] = None) -> DualModelService:
    """获取全局双模型服务实例"""
    global _dual_service
    with _dual_lock:
        if _dual_service is None:
            if llm_service is None:
                from src.tool_layer.llm_service import LLMService
                llm_service = LLMService()
            _dual_service = DualModelService(llm_service, config)
        return _dual_service


def reset_dual_model_service():
    """重置全局双模型服务"""
    global _dual_service
    with _dual_lock:
        _dual_service = None


__all__ = [
    "DualModelService",
    "DualModelConfig",
    "DualModelResponse",
    "BrainRole",
    "FailoverReason",
    "BrainStatus",
    "PerformanceTracker",
    "get_dual_model_service",
    "reset_dual_model_service",
]
