"""
Somn LLM统一配置管理器 v6.2.0
=============================
为所有板块提供统一的大模型调用能力

功能：
- 云端大模型优先配置
- 本地大模型备用
- 自动降级策略
- 统一的LLM服务接口

支持的云端模型：
- MiniMax M2.7 (默认，云端优先)
- DeepSeek Chat/Reasoner
- 腾讯混元
- 字节豆包
- 阿里通义千问
- OpenAI GPT-4/3.5
- Anthropic Claude

支持的本地模型：
- Gemma4 (B大模型，主脑)
- Llama 3.2 1B (A大模型，副脑)
- Ollama兼容模型

使用方式：
    from llm_unified_config import (
        get_llm_service,           # 获取统一LLM服务
        init_all_systems,          # 初始化所有系统
        CloudLLMPriority,          # 云端模型优先级
        LocalLLMPriority,           # 本地模型优先级
    )

版本: 6.2.0
日期: 2026-04-29
"""

import os
import sys
import time
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache

logger = logging.getLogger("Somn.LLM.Unified")

# ============================================================
# 路径设置
# ============================================================

def _get_project_root() -> Path:
    """获取项目根目录"""
    current = Path(__file__).resolve().parent
    # 向上查找 smart_office_assistant
    for parent in current.parents:
        if (parent / "smart_office_assistant").exists():
            return parent
    # 回退
    return current


PROJECT_ROOT = _get_project_root()
sys.path.insert(0, str(PROJECT_ROOT / "smart_office_assistant" / "src"))

# ============================================================
# 云端模型优先级枚举
# ============================================================

class CloudLLMPriority(Enum):
    """云端大模型优先级（按优先级从高到低）"""
    # 第一优先：MiniMax M2.7
    MINIMAX_M2_7 = "minimax-m2.7"
    MINIMAX = "minimax"

    # 第二优先：DeepSeek
    DEEPSEEK_REASONER = "deepseek-reasoner"
    DEEPSEEK_CHAT = "deepseek-chat"

    # 第三优先：腾讯混元
    HUNYUAN_TURBOS = "hunyuan-turbos"
    HUNYUAN = "hunyuan"

    # 第四优先：字节豆包
    DOUBAO_PRO = "doubao-pro"
    DOUBAO_LITE = "doubao-lite"
    DOUBAO = "doubao"

    # 第五优先：阿里通义千问
    QWEN_MAX = "qwen-max"
    QWEN_PLUS = "qwen-plus"
    QWEN = "qwen"

    # 第六优先：OpenAI
    GPT_4 = "gpt-4"
    GPT_35_TURBO = "gpt-3.5-turbo"
    OPENAI = "openai"

    # 第七优先：Anthropic
    CLAUDE_3_OPUS = "claude-3-opus"
    CLAUDE = "claude"


class LocalLLMPriority(Enum):
    """本地大模型优先级"""
    # 主脑：Gemma4多模态
    GEMMA4_LOCAL_B = "gemma4-local-b"

    # 副脑：Llama 3.2 1B
    LLAMA_3_2_1B = "llama-3.2-1b-a"

    # Ollama通用
    OLLAMA_DEFAULT = "local-default"


# ============================================================
# LLM配置数据类
# ============================================================

@dataclass
class LLMModelConfig:
    """LLM模型配置"""
    name: str                           # 模型标识名
    provider: str                       # 提供商
    model_name: str                    # API模型名
    api_base: str                       # API地址
    api_key: str                       # API密钥
    temperature: float = 0.7           # 温度参数
    max_tokens: int = 4000            # 最大token
    timeout: int = 60                  # 超时秒数
    capabilities: List[str] = field(default_factory=list)  # 能力列表
    is_cloud: bool = True              # 是否云端
    priority: int = 999               # 优先级（越小越优先）


# ============================================================
# 统一LLM服务
# ============================================================

class UnifiedLLMService:
    """
    统一LLM服务 v6.2.0

    特性：
    - 云端优先，自动降级
    - 统一的对话/分析接口
    - 自动检测可用模型
    - 支持会话上下文
    """

    _instance: Optional["UnifiedLLMService"] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return

        self._llm_service = None
        self._local_engine = None
        self._available_cloud_models: List[LLMModelConfig] = []
        self._available_local_models: List[LLMModelConfig] = []
        self._current_cloud_model: Optional[LLMModelConfig] = None
        self._current_local_model: Optional[LLMModelConfig] = None
        self._use_cloud_first = True  # 优先使用云端
        self._initialized = False
        self._init_error: Optional[str] = None

        # 执行初始化
        self._initialize()

    def _initialize(self):
        """初始化LLM服务"""
        start = time.time()
        logger.info("[UnifiedLLM] 开始初始化...")

        try:
            # 1. 加载云端模型配置
            self._load_cloud_models()

            # 2. 加载本地模型配置
            self._load_local_models()

            # 3. 初始化LLM服务
            self._init_llm_service()

            # 4. 初始化本地引擎
            self._init_local_engine()

            self._initialized = True
            elapsed = (time.time() - start) * 1000
            logger.info(f"[UnifiedLLM] 初始化完成（{elapsed:.1f}ms）")
            logger.info(f"[UnifiedLLM] 云端模型: {len(self._available_cloud_models)} 个可用")
            logger.info(f"[UnifiedLLM] 本地模型: {len(self._available_local_models)} 个可用")

        except Exception as e:
            self._init_error = str(e)
            logger.error(f"[UnifiedLLM] 初始化失败: {e}")

    def _load_cloud_models(self):
        """加载云端模型配置"""
        from smart_office_assistant.src.tool_layer.llm_service import LLMService

        # 创建临时LLM服务来获取配置
        temp_service = LLMService()

        # 从环境变量和配置中加载云端模型
        for model_name, config in temp_service.configs.items():
            # 跳过本地和mock类型的提供商
            if config.provider.value in ("local", "mock"):
                continue

            # 检查是否可用
            if not config.api_key or not config.api_base:
                continue

            # 确定优先级
            priority = 999
            for p in CloudLLMPriority:
                if p.value == model_name:
                    priority = p.value
                    break

            model_config = LLMModelConfig(
                name=model_name,
                provider=config.provider.value,
                model_name=config.model_name,
                api_base=config.api_base or "",
                api_key=config.api_key or "",
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                timeout=config.timeout,
                capabilities=[c.value for c in config.capabilities],
                is_cloud=True,
                priority=priority
            )

            self._available_cloud_models.append(model_config)

            # 设置当前云端模型（优先级最高的）
            if self._current_cloud_model is None or priority < self._current_cloud_model.priority:
                self._current_cloud_model = model_config

        # 按优先级排序
        self._available_cloud_models.sort(key=lambda x: x.priority)

    def _load_local_models(self):
        """加载本地模型配置"""
        # 检查Gemma4本地模型
        gemma4_path = PROJECT_ROOT / "models" / "gemma4-local-b"
        if gemma4_path.exists() and list(gemma4_path.glob("*.safetensors")):
            self._current_local_model = LLMModelConfig(
                name="gemma4-local-b",
                provider="local",
                model_name="gemma4-local-b",
                api_base="",
                api_key="",
                temperature=0.7,
                max_tokens=2000,
                timeout=120,
                capabilities=["chat", "analysis"],
                is_cloud=False,
                priority=1
            )
            self._available_local_models.append(self._current_local_model)

        # 检查Llama本地模型
        llama_path = PROJECT_ROOT / "models" / "llama-3.2-1b-instruct"
        if llama_path.exists() and list(llama_path.glob("*.gguf")):
            model_config = LLMModelConfig(
                name="llama-3.2-1b-a",
                provider="local",
                model_name="llama-3.2-1b-a",
                api_base="http://127.0.0.1:11434/v1",  # Ollama
                api_key="",
                temperature=0.7,
                max_tokens=2000,
                timeout=120,
                capabilities=["chat", "analysis"],
                is_cloud=False,
                priority=2
            )
            self._available_local_models.append(model_config)

    def _init_llm_service(self):
        """初始化LLM服务"""
        try:
            from smart_office_assistant.src.tool_layer.llm_service import get_llm_service
            self._llm_service = get_llm_service()
            logger.info("[UnifiedLLM] LLM服务初始化成功")
        except Exception as e:
            logger.warning(f"[UnifiedLLM] LLM服务初始化失败: {e}")

    def _init_local_engine(self):
        """初始化本地引擎"""
        try:
            from smart_office_assistant.src.core.local_llm_engine import get_engine_b, get_engine

            # 优先初始化Gemma4 B大模型
            try:
                self._local_engine = get_engine_b()
                logger.info("[UnifiedLLM] B大模型(Gemma4)引擎初始化成功")
            except Exception:
                # 回退到A大模型
                try:
                    self._local_engine = get_engine()
                    logger.info("[UnifiedLLM] A大模型(Llama)引擎初始化成功")
                except Exception as e:
                    logger.warning(f"[UnifiedLLM] 本地引擎初始化失败: {e}")

        except Exception as e:
            logger.warning(f"[UnifiedLLM] 本地引擎初始化失败: {e}")

    @property
    def is_ready(self) -> bool:
        """服务是否就绪"""
        return self._initialized and (
            self._llm_service is not None or self._local_engine is not None
        )

    @property
    def cloud_available(self) -> bool:
        """云端模型是否可用"""
        return self._llm_service is not None and self._current_cloud_model is not None

    @property
    def local_available(self) -> bool:
        """本地模型是否可用"""
        return self._local_engine is not None and self._local_engine.is_ready

    def get_default_model(self) -> str:
        """获取当前默认模型"""
        if self._use_cloud_first and self.cloud_available:
            return f"cloud:{self._current_cloud_model.name}"
        elif self.local_available:
            return f"local:{self._current_local_model.name}"
        return "mock"

    def chat(
        self,
        prompt: str,
        system_prompt: str = None,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None,
        conversation_id: str = None,
        **kwargs
    ) -> "LLMResponse":
        """
        统一对话接口

        Args:
            prompt: 用户提示
            system_prompt: 系统提示
            model: 指定模型（可选，默认使用云端优先）
            temperature: 温度参数
            max_tokens: 最大token
            conversation_id: 会话ID

        Returns:
            LLMResponse响应
        """
        # 确定使用哪个模型
        use_cloud = True

        if model:
            if model.startswith("cloud:"):
                use_cloud = True
                model = model[6:]
            elif model.startswith("local:"):
                use_cloud = False
                model = model[6:]
            elif self.cloud_available:
                # 未知格式，尝试云端
                model = self._current_cloud_model.name
            else:
                use_cloud = False

        # 优先云端
        if self._use_cloud_first and use_cloud and not model:
            if self.cloud_available:
                use_cloud = True
            elif self.local_available:
                use_cloud = False
        elif use_cloud and not self.cloud_available:
            # 云端不可用，降级到本地
            use_cloud = False

        # 执行调用
        if use_cloud and self.cloud_available:
            return self._chat_cloud(prompt, system_prompt, model, temperature, max_tokens, conversation_id)
        elif self.local_available:
            return self._chat_local(prompt, temperature, max_tokens, conversation_id)
        else:
            # 返回mock响应
            return self._mock_response(prompt)

    def _chat_cloud(
        self,
        prompt: str,
        system_prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
        conversation_id: str
    ):
        """云端对话"""
        try:
            model_name = model or self._current_cloud_model.name
            response = self._llm_service.chat(
                prompt=prompt,
                system_prompt=system_prompt,
                model=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                conversation_id=conversation_id
            )

            # 包装为统一响应
            return LLMResponse(
                content=response.content,
                model=response.model,
                provider=response.provider,
                usage=response.usage,
                finish_reason=response.finish_reason,
                latency_ms=response.latency_ms,
                source="cloud"
            )
        except Exception as e:
            logger.error(f"[UnifiedLLM] 云端对话失败: {e}")
            # 降级到本地
            if self.local_available:
                return self._chat_local(prompt, temperature, max_tokens, conversation_id)
            return self._mock_response(prompt)

    def _chat_local(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int,
        conversation_id: str
    ):
        """本地对话"""
        try:
            result = self._local_engine.generate(
                prompt,
                temperature=temperature or 0.7,
                max_new_tokens=max_tokens or 500
            )

            return LLMResponse(
                content=result.text,
                model=result.model,
                provider="local",
                usage={"prompt_tokens": 0, "completion_tokens": result.tokens},
                finish_reason=result.finish_reason,
                latency_ms=result.latency_ms,
                source="local"
            )
        except Exception as e:
            logger.error(f"[UnifiedLLM] 本地对话失败: {e}")
            return self._mock_response(prompt)

    def _mock_response(self, prompt: str) -> "LLMResponse":
        """Mock响应"""
        return LLMResponse(
            content=f"[UnifiedLLM] 所有模型不可用。请配置云端API密钥或启动本地模型服务。\n\n提示: {prompt[:100]}...",
            model="mock",
            provider="mock",
            usage={},
            finish_reason="error",
            latency_ms=0,
            source="mock"
        )

    def analyze(self, text: str, task: str, context: str = "", model: str = None) -> Dict[str, Any]:
        """分析接口"""
        if self._llm_service:
            return self._llm_service.analyze(text, task, context, model)
        return {"task": task, "analysis": "LLM服务不可用", "model": "none"}

    def generate_strategy(self, context: Dict[str, Any], model: str = None) -> Dict[str, Any]:
        """生成策略接口"""
        if self._llm_service:
            return self._llm_service.generate_strategy(context, model)
        return {"strategy_text": "LLM服务不可用", "context": context}

    def get_status(self) -> Dict[str, Any]:
        """获取服务状态"""
        return {
            "initialized": self._initialized,
            "init_error": self._init_error,
            "use_cloud_first": self._use_cloud_first,
            "cloud_available": self.cloud_available,
            "local_available": self.local_available,
            "default_model": self.get_default_model(),
            "cloud_models": [
                {"name": m.name, "provider": m.provider, "priority": m.priority}
                for m in self._available_cloud_models
            ],
            "local_models": [
                {"name": m.name, "priority": m.priority}
                for m in self._available_local_models
            ],
            "current_cloud": self._current_cloud_model.name if self._current_cloud_model else None,
            "current_local": self._current_local_model.name if self._current_local_model else None,
        }

    def set_cloud_priority(self, priority: CloudLLMPriority):
        """设置云端模型优先级"""
        for model in self._available_cloud_models:
            if model.name == priority.value:
                self._current_cloud_model = model
                logger.info(f"[UnifiedLLM] 云端模型切换为: {priority.value}")
                return True
        return False

    def set_local_priority(self, priority: LocalLLMPriority):
        """设置本地模型优先级"""
        for model in self._available_local_models:
            if model.name == priority.value:
                self._current_local_model = model
                logger.info(f"[UnifiedLLM] 本地模型切换为: {priority.value}")
                return True
        return False

    def enable_cloud_first(self, enabled: bool = True):
        """启用/禁用云端优先"""
        self._use_cloud_first = enabled
        logger.info(f"[UnifiedLLM] 云端优先: {enabled}")


@dataclass
class LLMResponse:
    """统一LLM响应格式"""
    content: str
    model: str
    provider: str
    usage: Dict[str, int] = field(default_factory=dict)
    finish_reason: str = "stop"
    latency_ms: int = 0
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))
    source: str = "unknown"  # cloud / local / mock


# ============================================================
# 全局实例和便捷函数
# ============================================================

_unified_llm_service: Optional[UnifiedLLMService] = None


def get_unified_llm_service() -> UnifiedLLMService:
    """获取统一LLM服务单例"""
    global _unified_llm_service
    if _unified_llm_service is None:
        _unified_llm_service = UnifiedLLMService()
    return _unified_llm_service


def get_llm_service():
    """获取LLM服务（兼容旧接口）"""
    return get_unified_llm_service()


def chat(prompt: str, **kwargs) -> LLMResponse:
    """快捷对话函数"""
    return get_unified_llm_service().chat(prompt, **kwargs)


def analyze(text: str, task: str, **kwargs) -> Dict[str, Any]:
    """快捷分析函数"""
    return get_unified_llm_service().analyze(text, task, **kwargs)


def get_llm_status() -> Dict[str, Any]:
    """获取LLM服务状态"""
    return get_unified_llm_service().get_status()


def init_all_systems(verbose: bool = True) -> Dict[str, Any]:
    """
    初始化所有Somn系统的大模型调用能力

    返回:
        各系统的初始化状态
    """
    results = {
        "unified_llm": False,
        "knowledge_cells": False,
        "neural_memory": False,
        "dual_track": False,
        "divine_reason": False,
        "domain_nexus": False,
        "pan_wisdom": False,
        "refute_core": False,
        "errors": []
    }

    if verbose:
        print("=" * 60)
        print("Somn LLM统一初始化 v6.2.0")
        print("=" * 60)

    # 1. 初始化统一LLM服务
    try:
        llm_service = get_unified_llm_service()
        results["unified_llm"] = llm_service.is_ready
        if verbose:
            status = llm_service.get_status()
            print(f"\n[1/8] 统一LLM服务: {'✓' if results['unified_llm'] else '✗'}")
            print(f"  - 云端可用: {status['cloud_available']}")
            print(f"  - 本地可用: {status['local_available']}")
            print(f"  - 默认模型: {status['default_model']}")
            if status['cloud_models']:
                print(f"  - 云端模型: {', '.join(m['name'] for m in status['cloud_models'][:3])}")
    except Exception as e:
        results["errors"].append(f"LLM服务: {e}")
        if verbose:
            print(f"\n[1/8] 统一LLM服务: ✗ ({e})")

    # 2. 初始化Knowledge Cells (SageDispatch)
    try:
        from knowledge_cells import dispatch, smart_dispatch, get_engine
        _ = get_engine()  # 触发懒加载
        results["knowledge_cells"] = True
        if verbose:
            print(f"[2/8] SageDispatch调度系统: ✓")
    except Exception as e:
        results["errors"].append(f"KnowledgeCells: {e}")
        if verbose:
            print(f"[2/8] SageDispatch调度系统: ✗ ({e})")

    # 3. 初始化Neural Memory
    try:
        from neural_memory import NeuralMemory, get_neural_memory
        _ = get_neural_memory()
        results["neural_memory"] = True
        if verbose:
            print(f"[3/8] NeuralMemory记忆系统: ✓")
    except Exception as e:
        results["errors"].append(f"NeuralMemory: {e}")
        if verbose:
            print(f"[3/8] NeuralMemory记忆系统: ✗ ({e})")

    # 4. 初始化Dual Track (神政轨/神行轨)
    try:
        from smart_office_assistant.src.intelligence.dual_track import DivineGovernanceTrack, get_loading_stats
        track_a = DivineGovernanceTrack()
        stats = get_loading_stats()
        results["dual_track"] = True
        if verbose:
            print(f"[4/8] 双轨系统(神政轨/神行轨): ✓")
            print(f"  - 版本: {stats.get('governance_version', 'N/A')}")
    except Exception as e:
        results["errors"].append(f"DualTrack: {e}")
        if verbose:
            print(f"[4/8] 双轨系统(神政轨/神行轨): ✗ ({e})")

    # 5. 初始化DivineReason (使用SuperReasoning封装)
    try:
        from knowledge_cells.dispatchers import SuperReasoning
        _ = SuperReasoning()
        results["divine_reason"] = True
        if verbose:
            print(f"[5/8] DivineReason推理系统: ✓ (via SuperReasoning)")
    except Exception as e:
        results["errors"].append(f"DivineReason: {e}")
        if verbose:
            print(f"[5/8] DivineReason推理系统: ✗ ({e})")

    # 6. 初始化DomainNexus
    try:
        from knowledge_cells import get_nexus
        _ = get_nexus()
        results["domain_nexus"] = True
        if verbose:
            print(f"[6/8] DomainNexus知识库: ✓")
    except Exception as e:
        results["errors"].append(f"DomainNexus: {e}")
        if verbose:
            print(f"[6/8] DomainNexus知识库: ✗ ({e})")

    # 7. 初始化Pan-Wisdom智慧树
    try:
        from knowledge_cells.pan_wisdom_lazy_loader import preload_pan_wisdom
        preload_pan_wisdom()
        results["pan_wisdom"] = True
        if verbose:
            print(f"[7/8] Pan-Wisdom智慧树: ✓")
    except Exception as e:
        results["errors"].append(f"Pan-Wisdom: {e}")
        if verbose:
            print(f"[7/8] Pan-Wisdom智慧树: ✗ ({e})")

    # 8. 初始化RefuteCore
    try:
        from knowledge_cells import DivineTrackOversight
        results["refute_core"] = True
        if verbose:
            print(f"[8/8] RefuteCore论证系统: ✓")
    except Exception as e:
        results["errors"].append(f"RefuteCore: {e}")
        if verbose:
            print(f"[8/8] RefuteCore论证系统: ✗ ({e})")

    if verbose:
        print("\n" + "=" * 60)
        success_count = sum(1 for v in results.values() if v is True)
        print(f"初始化完成: {success_count}/8 系统就绪")
        if results["errors"]:
            print(f"错误数: {len(results['errors'])}")
        print("=" * 60)

    return results


# ============================================================
# 板块LLM调用快捷函数
# ============================================================

def call_with_llm(
    module_name: str,
    func: Callable,
    prompt: str,
    system_prompt: str = None,
    model: str = None,
    **kwargs
) -> Any:
    """
    为指定模块调用LLM

    Args:
        module_name: 模块名称（用于日志）
        func: 实际执行函数（如果LLM不可用则调用此函数）
        prompt: LLM提示
        system_prompt: 系统提示
        model: 指定模型

    Returns:
        函数执行结果
    """
    llm = get_unified_llm_service()

    if llm.is_ready:
        try:
            response = llm.chat(
                prompt=prompt,
                system_prompt=system_prompt,
                model=model
            )
            if response.source != "mock":
                logger.info(f"[{module_name}] LLM调用成功 ({response.source}, {response.latency_ms}ms)")
                return response.content
        except Exception as e:
            logger.warning(f"[{module_name}] LLM调用失败: {e}")

    # LLM不可用，执行回退函数
    logger.info(f"[{module_name}] 使用回退函数")
    return func(prompt, **kwargs)


def neural_memory_llm_call(prompt: str, context: str = None) -> str:
    """
    NeuralMemory模块的LLM调用

    用途：记忆编码、检索优化、语义理解
    """
    system_prompt = "你是一个专业的记忆系统助手，擅长理解和处理各类记忆信息。"

    if context:
        system_prompt += f"\n\n上下文信息:\n{context}"

    return call_with_llm("NeuralMemory", lambda p, **_: f"[记忆处理] {p[:50]}...", prompt, system_prompt)


def sage_dispatch_llm_call(prompt: str, dispatcher_type: str = "SD-F2") -> str:
    """
    SageDispatch模块的LLM调用

    用途：问题分析、调度决策、结果生成
    """
    system_prompt = f"""你是一个专业的智能调度助手，负责分析问题并选择最优的解决路径。

当前调度器: {dispatcher_type}

请分析用户输入的问题，选择合适的处理方式。"""

    return call_with_llm("SageDispatch", lambda p, **_: f"[调度处理] {p[:50]}...", prompt, system_prompt)


def divine_reason_llm_call(prompt: str, mode: str = "standard") -> str:
    """
    DivineReason模块的LLM调用

    用途：深度推理、假设探索、元认知审视
    """
    system_prompt = f"""你是一个专业的深度推理引擎，擅长进行多层次的逻辑推理和分析。

推理模式: {mode}

支持以下推理深度:
- Light: 表层推理，模式匹配
- Standard: 深度推理，假设探索
- Deep: 极致推理，元认知审视"""

    return call_with_llm("DivineReason", lambda p, **_: f"[推理处理] {p[:50]}...", prompt, system_prompt)


def super_reasoning_llm_call(prompt: str, depth: str = "standard") -> str:
    """
    SuperReasoning模块的LLM调用 (DivineReason的封装)

    用途：三层深度推理 (Light/Standard/Deep)
    """
    system_prompt = f"""你是一个SuperReasoning超级推理引擎。

推理深度: {depth}

三层推理架构:
- Light: 表层推理，模式匹配，快速响应
- Standard: 深度推理，假设探索，多角度分析
- Deep: 极致推理，元认知审视，批判性思考"""

    return call_with_llm("SuperReasoning", lambda p, **_: f"[超级推理] {p[:50]}...", prompt, system_prompt)


def domain_nexus_llm_call(prompt: str, query_type: str = "knowledge") -> str:
    """
    DomainNexus模块的LLM调用

    用途：知识检索、关联查询、知识图谱构建
    """
    system_prompt = f"""你是一个专业的知识库助手，擅长从多个知识域中检索和整合信息。

查询类型: {query_type}

请分析查询意图，从知识库中检索相关信息。"""

    return call_with_llm("DomainNexus", lambda p, **_: f"[知识查询] {p[:50]}...", prompt, system_prompt)


def pan_wisdom_llm_call(prompt: str, school: str = None) -> str:
    """
    PanWisdom模块的LLM调用

    用途：学派融合、智慧整合、跨学派分析
    """
    system_prompt = f"""你是一个融合了42个学派智慧的智能助手。

当前学派: {school or "自动选择"}

可用的学派包括:
- 儒家、道家、墨家、法家、名家
- 西方哲学各流派
- 现代科学各学科

请结合相关学派的智慧来分析问题。"""

    return call_with_llm("PanWisdom", lambda p, **_: f"[智慧融合] {p[:50]}...", prompt, system_prompt)


def refute_core_llm_call(prompt: str, dimension: str = "logic") -> str:
    """
    RefuteCore模块的LLM调用

    用途：论证分析、反驳检测、逻辑验证
    """
    system_prompt = f"""你是一个专业的论证分析助手，擅长从多个维度检验论证的有效性。

检验维度: {dimension}

8个检验维度:
1. 逻辑维度 - 检验推理的有效性
2. 证据维度 - 评估证据的可靠性
3. 假设维度 - 识别潜在的假设
4. 反面维度 - 考虑反面观点
5. 类比维度 - 检验类比的有效性
6. 权威维度 - 评估权威的适当性
7. 因果维度 - 分析因果关系的强度
8. 价值维度 - 评估价值判断的合理性"""

    return call_with_llm("RefuteCore", lambda p, **_: f"[论证检验] {p[:50]}...", prompt, system_prompt)


def dual_track_llm_call(prompt: str, track: str = "A") -> str:
    """
    双轨系统的LLM调用

    Args:
        prompt: 输入提示
        track: 轨道类型 ("A"=神政轨, "B"=神行轨)
    """
    if track == "A":
        system_prompt = """你是一个神政轨( DivineGovernanceTrack)的管理监管助手。

神政轨职责：
- 监管调度过程
- 验证决策合规性
- 记录执行轨迹
- 保障系统稳定性"""
    else:
        system_prompt = """你是一个神行轨(DivineExecutionTrack)的执行助手。

神行轨职责：
- 执行具体任务
- 调用Claw贤者完成工作
- 管理任务状态
- 协调部门协作"""

    return call_with_llm(f"DualTrack-{track}", lambda p, **_: f"[{track}轨执行] {p[:50]}...", prompt, system_prompt)


# ============================================================
# 导出
# ============================================================

__all__ = [
    # 核心类
    "UnifiedLLMService",
    "LLMModelConfig",
    "LLMResponse",

    # 优先级枚举
    "CloudLLMPriority",
    "LocalLLMPriority",

    # 便捷函数
    "get_unified_llm_service",
    "get_llm_service",
    "chat",
    "analyze",
    "get_llm_status",
    "init_all_systems",

    # 板块LLM调用
    "call_with_llm",
    "neural_memory_llm_call",
    "sage_dispatch_llm_call",
    "divine_reason_llm_call",
    "super_reasoning_llm_call",
    "domain_nexus_llm_call",
    "pan_wisdom_llm_call",
    "refute_core_llm_call",
    "dual_track_llm_call",
]
