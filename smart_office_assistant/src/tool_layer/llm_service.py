"""
__all__ = [
    'add_cloud_model',
    'analyze',
    'chat',
    'configure_from_env',
    'delete_cloud_model',
    'generate_strategy',
    'get_default_model',
    'get_llm_service',
    'get_model_info',
    'list_available_models',
    'list_cloud_providers',
    'register_model',
    'test_connection',
    'update_cloud_model',
    'validate_cloud_model',
]

LLM服务 - 大语言模型unified接口
默认优先走本地模型(OpenAI 兼容接口),严格避免项目内容外传到云端.
"""

import json
import os
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from urllib import request, error

from src.core.paths import DATA_DIR
from src.utils.retry_utils import get_circuit_breaker, RetryConfig, http_retry_with_status
import threading

class ModelProvider(Enum):
    """模型提供商"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    BAIDU = "baidu"
    ALIBABA = "alibaba"
    TENCENT = "tencent"
    DOUBIT = "doubit"       # 豆包/火山方舟 (字节跳动)
    DEEPSEEK = "deepseek"   # DeepSeek
    HUNYUAN = "hunyuan"     # 腾讯混元/元宝
    LOCAL = "local"
    MOCK = "mock"

class ModelCapability(Enum):
    """模型能力"""
    CHAT = "chat"
    COMPLETION = "completion"
    ANALYSIS = "analysis"
    CODE = "code"
    VISION = "vision"

@dataclass
class LLMConfig:
    """LLM配置"""
    provider: ModelProvider
    model_name: str
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 60
    capabilities: List[ModelCapability] = field(default_factory=list)
    cost_per_1k_tokens: float = 0.0

@dataclass
class Message:
    """消息"""
    role: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LLMResponse:
    """LLM响应"""
    content: str
    model: str
    provider: str
    usage: Dict[str, int] = field(default_factory=dict)
    finish_reason: str = "stop"
    latency_ms: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

class LLMService:
    """LLM服务"""

    PRESET_MODELS = {
        # OpenAI 系列
        "gpt-4": LLMConfig(
            provider=ModelProvider.OPENAI,
            model_name="gpt-4",
            capabilities=[ModelCapability.CHAT, ModelCapability.ANALYSIS, ModelCapability.CODE],
            cost_per_1k_tokens=0.03
        ),
        "gpt-3.5-turbo": LLMConfig(
            provider=ModelProvider.OPENAI,
            model_name="gpt-3.5-turbo",
            capabilities=[ModelCapability.CHAT, ModelCapability.COMPLETION],
            cost_per_1k_tokens=0.002
        ),
        # Anthropic 系列
        "claude-3-opus": LLMConfig(
            provider=ModelProvider.ANTHROPIC,
            model_name="claude-3-opus-20240229",
            capabilities=[ModelCapability.CHAT, ModelCapability.ANALYSIS, ModelCapability.VISION],
            cost_per_1k_tokens=0.015
        ),
        # 百度文心一言
        "ernie-bot": LLMConfig(
            provider=ModelProvider.BAIDU,
            model_name="ernie-bot-4",
            capabilities=[ModelCapability.CHAT, ModelCapability.ANALYSIS],
            cost_per_1k_tokens=0.012
        ),
        # 阿里通义千问 (新版 OpenAI 兼容格式)
        "qwen-max": LLMConfig(
            provider=ModelProvider.ALIBABA,
            model_name="qwen-max",
            api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
            capabilities=[ModelCapability.CHAT, ModelCapability.ANALYSIS, ModelCapability.CODE],
            cost_per_1k_tokens=0.01
        ),
        # ===== 国产大模型通用端口 (核心新增) =====
        # 豆包 (字节跳动/火山方舟)
        "doubao-pro": LLMConfig(
            provider=ModelProvider.DOUBIT,
            model_name="doubao-pro-32k",
            api_base="https://ark.cn-beijing.volces.com/v1",
            capabilities=[ModelCapability.CHAT, ModelCapability.ANALYSIS],
            cost_per_1k_tokens=0.008
        ),
        "doubao-lite": LLMConfig(
            provider=ModelProvider.DOUBIT,
            model_name="doubao-lite-32k",
            api_base="https://ark.cn-beijing.volces.com/v1",
            capabilities=[ModelCapability.CHAT, ModelCapability.ANALYSIS],
            cost_per_1k_tokens=0.001
        ),
        # DeepSeek (深度求索) - 完全兼容 OpenAI 格式
        "deepseek-chat": LLMConfig(
            provider=ModelProvider.DEEPSEEK,
            model_name="deepseek-chat",
            api_base="https://api.deepseek.com/v1",
            capabilities=[ModelCapability.CHAT, ModelCapability.ANALYSIS, ModelCapability.CODE],
            cost_per_1k_tokens=0.001
        ),
        "deepseek-reasoner": LLMConfig(
            provider=ModelProvider.DEEPSEEK,
            model_name="deepseek-reasoner",
            api_base="https://api.deepseek.com/v1",
            capabilities=[ModelCapability.CHAT, ModelCapability.ANALYSIS],
            cost_per_1k_tokens=0.002
        ),
        # 腾讯混元/元宝 - OpenAI 兼容格式
        "hunyuan-turbos": LLMConfig(
            provider=ModelProvider.HUNYUAN,
            model_name="hunyuan-turbos-latest",
            api_base="https://api.hunyuan.cloud.tencent.com/v1",
            capabilities=[ModelCapability.CHAT, ModelCapability.ANALYSIS, ModelCapability.CODE],
            cost_per_1k_tokens=0.006
        ),
        "hunyuan-vision": LLMConfig(
            provider=ModelProvider.HUNYUAN,
            model_name="hunyuan-vision",
            api_base="https://api.hunyuan.cloud.tencent.com/v1",
            capabilities=[ModelCapability.CHAT, ModelCapability.ANALYSIS, ModelCapability.VISION],
            cost_per_1k_tokens=0.009
        ),
        # ===== 本地模型 =====
        # A大模型 - Llama 3.2 1B (GGUF格式,本地部署)
        "llama-3.2-1b-a": LLMConfig(
            provider=ModelProvider.LOCAL,
            model_name="llama-3.2-1b-a",
            api_base="http://127.0.0.1:11434/v1",
            capabilities=[ModelCapability.CHAT, ModelCapability.ANALYSIS],
            cost_per_1k_tokens=0.0
        ),
        "local-default": LLMConfig(
            provider=ModelProvider.LOCAL,
            model_name="qwen2.5:7b-instruct",
            api_base="http://127.0.0.1:11434/v1",
            capabilities=[ModelCapability.CHAT, ModelCapability.ANALYSIS, ModelCapability.CODE],
            cost_per_1k_tokens=0.0
        ),
        # Mock 兜底
        "mock": LLMConfig(
            provider=ModelProvider.MOCK,
            model_name="mock-model",
            capabilities=[ModelCapability.CHAT, ModelCapability.ANALYSIS],
            cost_per_1k_tokens=0.0
        )
    }

    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else DATA_DIR / "llm"
        self.base_path.mkdir(parents=True, exist_ok=True)

        self.configs: Dict[str, LLMConfig] = {}
        self.conversation_history: Dict[str, List[Message]] = {}

        # 加载预设模型
        for name, config in self.PRESET_MODELS.items():
            self.configs[name] = LLMConfig(**config.__dict__)

        # 从环境变量加载 API Keys
        self._load_api_keys()

        # 刷新本地模型配置
        self._refresh_local_config()

        # 从环境变量批量配置云端模型 (国产大模型支持)
        self.configure_from_env()

    def _load_api_keys(self):
        """从环境变量加载API密钥"""
        # OpenAI 兼容格式的环境变量mapping
        env_mapping = {
            ModelProvider.OPENAI: "OPENAI_API_KEY",
            ModelProvider.ANTHROPIC: "ANTHROPIC_API_KEY",
            ModelProvider.BAIDU: "BAIDU_API_KEY",
            ModelProvider.ALIBABA: "DASHSCOPE_API_KEY",
            ModelProvider.TENCENT: "TENCENT_API_KEY",
            # 国产大模型 API Key 环境变量
            ModelProvider.DOUBIT: "VOLCENGINE_API_KEY",       # 火山方舟/豆包
            ModelProvider.DEEPSEEK: "DEEPSEEK_API_KEY",       # DeepSeek
            ModelProvider.HUNYUAN: "HUNYUAN_API_KEY",         # 腾讯混元/元宝
        }

        for provider, env_var in env_mapping.items():
            api_key = os.getenv(env_var)
            if not api_key:
                continue

            for config in self.configs.values():
                if config.provider == provider:
                    config.api_key = api_key

    def _refresh_local_config(self):
        """刷新本地模型配置"""
        local_model = os.getenv("SOMN_LOCAL_LLM_MODEL", "qwen2.5:7b-instruct")
        local_base = os.getenv("SOMN_LOCAL_LLM_BASE_URL", "http://127.0.0.1:11434/v1")
        local_api_key = os.getenv("SOMN_LOCAL_LLM_API_KEY", "")

        self.configs["local-default"] = LLMConfig(
            provider=ModelProvider.LOCAL,
            model_name=local_model,
            api_base=local_base,
            api_key=local_api_key or None,
            temperature=0.3,
            max_tokens=4000,
            # [v9.0 修复] 默认120s→60s，避免单次LLM调用阻塞过久
            # 可通过环境变量SOMN_LOCAL_LLM_TIMEOUT覆盖
            timeout=int(os.getenv("SOMN_LOCAL_LLM_TIMEOUT", "60")),
            capabilities=[ModelCapability.CHAT, ModelCapability.ANALYSIS, ModelCapability.CODE],
            cost_per_1k_tokens=0.0
        )

    def get_default_model(self) -> str:
        """get默认模型,优先本地模型"""
        preferred = os.getenv("SOMN_DEFAULT_MODEL", "").strip()
        if preferred and preferred in self.configs:
            return preferred

        local_config = self.configs.get("local-default")
        if local_config and local_config.api_base:
            return "local-default"
        return "mock"

    def register_model(self, name: str, config: LLMConfig):
        """注册模型配置"""
        self.configs[name] = config

    def chat(self, prompt: str, model: Optional[str] = None,
             system_prompt: str = None,
             temperature: float = None,
             max_tokens: int = None,
             conversation_id: str = None) -> LLMResponse:
        """对话"""
        selected_model = model or self.get_default_model()
        config = self.configs.get(selected_model, self.configs["mock"])

        messages: List[Message] = []
        if system_prompt:
            messages.append(Message("system", system_prompt))

        if conversation_id and conversation_id in self.conversation_history:
            messages.extend(self.conversation_history[conversation_id][-6:])

        messages.append(Message("user", prompt))

        if config.provider == ModelProvider.MOCK:
            response = self._mock_chat(messages, config)
        else:
            response = self._call_api(messages, config, temperature, max_tokens)

        if conversation_id:
            if conversation_id not in self.conversation_history:
                self.conversation_history[conversation_id] = []
            self.conversation_history[conversation_id].append(Message("user", prompt))
            self.conversation_history[conversation_id].append(Message("assistant", response.content))

        return response

    def analyze(self, text: str, task: str, context: str = "",
                model: Optional[str] = None) -> Dict[str, Any]:
        """分析文本"""
        task_prompts = {
            "sentiment": f"分析以下文本的情感倾向(正面/负面/中性),并给出置信度:\n\n{text}",
            "summary": f"总结以下文本的核心要点(3-5条):\n\n{text}",
            "keywords": f"提取以下文本的关键词(5-10个):\n\n{text}",
            "classification": f"将以下文本分类,给出类别和置信度:\n\n{text}",
            "growth_insight": f"基于以下数据提供增长洞察和建议:\n\n{text}\n\n上下文:{context}"
        }

        prompt = task_prompts.get(task, f"分析以下内容:\n\n{text}")
        system_prompt = "你是一个专业的增长strategy分析师,擅长从数据中提取洞察并提供可执行建议."
        response = self.chat(prompt, model=model, system_prompt=system_prompt)

        return {
            "task": task,
            "analysis": response.content,
            "model": response.model,
            "provider": response.provider,
            "timestamp": response.timestamp
        }

    def generate_strategy(self, context: Dict[str, Any],
                          model: Optional[str] = None) -> Dict[str, Any]:
        """generate增长strategy"""
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
            temperature=0.3
        )

        return {
            "strategy_text": response.content,
            "context": context,
            "model": response.model,
            "provider": response.provider,
            "generated_at": response.timestamp
        }

    def _mock_chat(self, messages: List[Message], config: LLMConfig) -> LLMResponse:
        """模拟对话(本地模型不可用时兜底)"""
        user_message = messages[-1].content if messages else ""

        if "增长" in user_message or "strategy" in user_message:
            content = """基于当前情况,我建议以下增长strategy:

**核心strategy:**
1. **产品优化驱动** - 通过A/B测试优化核心转化漏斗,预期提升转化率15-20%
2. **内容营销矩阵** - 建立SEO+社交媒体+KOL的内容组合拳,降低获客成本30%
3. **用户裂变机制** - 设计邀请奖励体系,目标病毒系数达到0.5

**执行步骤:**
- 第1-2周:完成产品优化和测试
- 第3-4周:启动内容营销
- 第5-8周:上线裂变功能并迭代

**关键metrics:**
- 月活跃用户增长 20%
- 获客成本降低 25%
- 用户留存率提升 10%"""
        elif "分析" in user_message:
            content = """**数据分析结果:**

1. **用户行为趋势**:近30日活跃用户呈上升趋势(+15%),但次日留存略有下降(-3%)
2. **渠道表现**:自然搜索流量质量最高(转化率4.2%),付费广告流量需优化(转化率1.8%)
3. **关键发现**:用户在注册后第3天流失率最高,建议加强新用户引导

**建议action:**
- 优化注册流程,减少步骤
- 增加新用户 onboarding 邮件序列
- 对高价值用户群体进行再营销"""
        else:
            content = (
                f"收到您的消息:{user_message[:80]}...\n\n"
                "当前未检测到可用本地模型,因此使用了本地 mock 响应.\n"
                "请配置 SOMN_LOCAL_LLM_BASE_URL 和 SOMN_LOCAL_LLM_MODEL 以启用真实本地推理."
            )

        return LLMResponse(
            content=content,
            model=config.model_name,
            provider=config.provider.value,
            usage={"prompt_tokens": len(user_message), "completion_tokens": len(content)},
            latency_ms=10
        )

    def _call_api(self, messages: List[Message], config: LLMConfig,
                  temperature: float = None, max_tokens: int = None) -> LLMResponse:
        """
        调用实际 API,支持所有 OpenAI 兼容格式的云端模型.

        支持的模型类型:
        - LOCAL: 本地 OpenAI 兼容接口 (如 Ollama)
        - OPENAI: OpenAI API
        - DOUBIT: 豆包/火山方舟
        - DEEPSEEK: DeepSeek
        - HUNYUAN: 腾讯混元/元宝
        - ALIBABA: 通义千问 (新版)
        - BAIDU: 文心一言 (非标准格式,需特殊处理)
        - ANTHROPIC: Claude (非标准格式,需特殊处理)
        """
        # 本地模型使用专门的调用方法
        if config.provider == ModelProvider.LOCAL:
            return self._call_local_api(messages, config, temperature, max_tokens)

        # 百度文心一言 - 非标准格式
        if config.provider == ModelProvider.BAIDU:
            return self._call_baidu_api(messages, config, temperature, max_tokens)

        # Anthropic Claude - 非标准格式
        if config.provider == ModelProvider.ANTHROPIC:
            return self._call_anthropic_api(messages, config, temperature, max_tokens)

        # 所有 OpenAI 兼容格式的云端模型 (豆包/DeepSeek/混元/千问等)
        return self._call_openai_compatible_api(messages, config, temperature, max_tokens)

    def _call_local_api(self, messages: List[Message], config: LLMConfig,
                        temperature: float = None, max_tokens: int = None) -> LLMResponse:
        """调用本地 OpenAI 兼容接口。 [v10.1 重试优化] 本方法内部自带重试。"""
        endpoint = self._normalize_chat_endpoint(config.api_base)
        payload = {
            "model": config.model_name,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature if temperature is not None else config.temperature,
            "max_tokens": max_tokens if max_tokens is not None else config.max_tokens,
            "stream": False
        }

        headers = {"Content-Type": "application/json"}
        if config.api_key:
            headers["Authorization"] = f"Bearer {config.api_key}"

        started = time.time()
        _overall_timeout = 60.0  # 总体超时60秒
        _func_start_time = time.time()
        cb = get_circuit_breaker(f"llm-local-{config.model_name}", failure_threshold=3, recovery_timeout=60.0)

        # [v10.1] 指数退避重试：最多3次，针对429限流/5xx错误/网络超时
        _MAX_RETRIES = 3
        for _attempt in range(1, _MAX_RETRIES + 1):
            # 检查总体超时 [v10.2 防卡死]
            if time.time() - _func_start_time > _overall_timeout:
                logger.error(f"[LLM-本地] 总体超时（{_overall_timeout}s），放弃重试")
                return LLMResponse(
                    content=f"本地模型调用超时（超过{_overall_timeout}秒）",
                    model=config.model_name,
                    provider=config.provider.value,
                    usage={"prompt_tokens": 0, "completion_tokens": 0},
                    latency_ms=int((time.time() - _func_start_time) * 1000),
                    finish_reason="timeout"
                )
            try:
                req = request.Request(
                    endpoint,
                    data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                    headers=headers,
                    method="POST"
                )
                with request.urlopen(req, timeout=config.timeout) as resp:
                    raw = resp.read().decode("utf-8")
                data = json.loads(raw)
                cb.record_success()
                break
            except error.HTTPError as exc:
                cb.record_failure()
                # 429限流和5xx错误值得重试
                if exc.code in (429, 500, 502, 503, 504) and _attempt < _MAX_RETRIES:
                    _delay = min(2.0 * (2 ** (_attempt - 1)), 10.0)
                    logger.warning(
                        f"[LLM-本地] HTTP {exc.code}，{_delay:.1f}s后重试({_attempt}/{_MAX_RETRIES})"
                    )
                    threading.Event().wait(_delay)
                    started = time.time()
                    continue
                detail = exc.read().decode("utf-8", errors="ignore") if hasattr(exc, "read") else str(exc)
                return LLMResponse(
                    content=f"本地模型调用失败(HTTP {exc.code}): {detail[:500]}",
                    model=config.model_name,
                    provider=config.provider.value,
                    usage={"prompt_tokens": 0, "completion_tokens": 0},
                    latency_ms=int((time.time() - started) * 1000),
                    finish_reason="error"
                )
            except Exception as exc:
                cb.record_failure()
                if _attempt < _MAX_RETRIES:
                    _delay = min(2.0 * (2 ** (_attempt - 1)), 10.0)
                    logger.warning(
                        f"[LLM-本地] {type(exc).__name__}，{_delay:.1f}s后重试({_attempt}/{_MAX_RETRIES})"
                    )
                    threading.Event().wait(_delay)
                    started = time.time()
                    continue
                # 重试次数用尽
                return LLMResponse(
                    content=(
                        "本地模型调用失败.请确认本地模型服务已启动,"
                        f"当前地址:{endpoint};错误:{str(exc)}"
                    ),
                    model=config.model_name,
                    provider=config.provider.value,
                    usage={"prompt_tokens": 0, "completion_tokens": 0},
                    latency_ms=int((time.time() - started) * 1000),
                    finish_reason="error"
                )

        content = self._extract_content_from_response(data)
        usage = data.get("usage", {}) if isinstance(data, dict) else {}
        finish_reason = "stop"
        if isinstance(data, dict):
            choices = data.get("choices", [])
            if choices:
                finish_reason = choices[0].get("finish_reason", "stop")

        return LLMResponse(
            content=content,
            model=config.model_name,
            provider=config.provider.value,
            usage={
                "prompt_tokens": int(usage.get("prompt_tokens", 0)),
                "completion_tokens": int(usage.get("completion_tokens", 0)),
                "total_tokens": int(usage.get("total_tokens", 0))
            },
            finish_reason=finish_reason,
            latency_ms=int((time.time() - started) * 1000)
        )

    def _call_openai_compatible_api(self, messages: List[Message], config: LLMConfig,
                                     temperature: float = None, max_tokens: int = None) -> LLMResponse:
        """
        调用 OpenAI 兼容格式的云端 API.

        支持的模型:
        - 豆包 (Doubao/火山方舟): https://ark.cn-beijing.volces.com/v1
        - DeepSeek: https://api.deepseek.com/v1
        - 腾讯混元/元宝: https://api.hunyuan.cloud.tencent.com/v1
        - 通义千问 (新版): https://dashscope.aliyuncs.com/compatible-mode/v1
        """
        if not config.api_base:
            return LLMResponse(
                content=f"未配置 API 端点,请设置 {config.provider.value.upper()}_BASE_URL 环境变量",
                model=config.model_name,
                provider=config.provider.value,
                usage={"prompt_tokens": 0, "completion_tokens": 0},
                latency_ms=0,
                finish_reason="config_error"
            )

        if not config.api_key:
            return LLMResponse(
                content=(
                    f"未配置 API Key,请设置以下环境变量之一:\n"
                    f"  - VOLCENGINE_API_KEY (豆包/火山方舟)\n"
                    f"  - DEEPSEEK_API_KEY (DeepSeek)\n"
                    f"  - HUNYUAN_API_KEY (腾讯混元/元宝)\n"
                    f"  - DASHSCOPE_API_KEY (通义千问)\n"
                    f"  - OPENAI_API_KEY (OpenAI)"
                ),
                model=config.model_name,
                provider=config.provider.value,
                usage={"prompt_tokens": 0, "completion_tokens": 0},
                latency_ms=0,
                finish_reason="auth_error"
            )

        endpoint = self._normalize_chat_endpoint(config.api_base)
        payload = {
            "model": config.model_name,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature if temperature is not None else config.temperature,
            "max_tokens": max_tokens if max_tokens is not None else config.max_tokens,
            "stream": False
        }

        # DeepSeek 特殊参数:思考模式
        if config.provider == ModelProvider.DEEPSEEK:
            payload["thinking"] = {"type": "enabled"}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.api_key}"
        }

        # 腾讯混元特殊 Header
        if config.provider == ModelProvider.HUNYUAN:
            headers["X-App-Id"] = "somn-agent"

        started = time.time()
        _overall_timeout = 60.0  # 总体超时60秒
        _func_start_time = time.time()
        cb = get_circuit_breaker(f"llm-{config.provider.value}-{config.model_name}", failure_threshold=5, recovery_timeout=30.0)

        # [v10.1] 指数退避重试：最多3次，针对429限流/5xx错误/网络超时
        _MAX_RETRIES = 3
        for _attempt in range(1, _MAX_RETRIES + 1):
            # 检查总体超时 [v10.2 防卡死]
            if time.time() - _func_start_time > _overall_timeout:
                logger.error(f"[LLM-{config.provider.value}] 总体超时（{_overall_timeout}s），放弃重试")
                return LLMResponse(
                    content=f"API 调用超时（超过{_overall_timeout}秒）",
                    model=config.model_name,
                    provider=config.provider.value,
                    usage={"prompt_tokens": 0, "completion_tokens": 0},
                    latency_ms=int((time.time() - _func_start_time) * 1000),
                    finish_reason="timeout"
                )
            try:
                req = request.Request(
                    endpoint,
                    data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                    headers=headers,
                    method="POST"
                )
                with request.urlopen(req, timeout=config.timeout) as resp:
                    raw = resp.read().decode("utf-8")
                data = json.loads(raw)
                cb.record_success()
                break
            except error.HTTPError as exc:
                cb.record_failure()
                # 429限流和5xx错误值得重试
                if exc.code in (429, 500, 502, 503, 504) and _attempt < _MAX_RETRIES:
                    _delay = min(2.0 * (2 ** (_attempt - 1)), 10.0)
                    logger.warning(
                        f"[LLM-{config.provider.value}] HTTP {exc.code}，"
                        f"{_delay:.1f}s后重试({_attempt}/{_MAX_RETRIES})"
                    )
                    threading.Event().wait(_delay)
                    started = time.time()
                    continue
                detail = exc.read().decode("utf-8", errors="ignore") if hasattr(exc, "read") else str(exc)
                return LLMResponse(
                    content=f"API 调用失败(HTTP {exc.code}): {detail[:500]}",
                    model=config.model_name,
                    provider=config.provider.value,
                    usage={"prompt_tokens": 0, "completion_tokens": 0},
                    latency_ms=int((time.time() - started) * 1000),
                    finish_reason="error"
                )
            except Exception as exc:
                cb.record_failure()
                if _attempt < _MAX_RETRIES:
                    _delay = min(2.0 * (2 ** (_attempt - 1)), 10.0)
                    logger.warning(
                        f"[LLM-{config.provider.value}] {type(exc).__name__}，"
                        f"{_delay:.1f}s后重试({_attempt}/{_MAX_RETRIES})"
                    )
                    threading.Event().wait(_delay)
                    started = time.time()
                    continue
                return LLMResponse(
                    content=f"API 调用失败: {str(exc)}",
                    model=config.model_name,
                    provider=config.provider.value,
                    usage={"prompt_tokens": 0, "completion_tokens": 0},
                    latency_ms=int((time.time() - started) * 1000),
                    finish_reason="error"
                )

        content = self._extract_content_from_response(data)
        usage = data.get("usage", {}) if isinstance(data, dict) else {}
        finish_reason = "stop"
        if isinstance(data, dict):
            choices = data.get("choices", [])
            if choices:
                finish_reason = choices[0].get("finish_reason", "stop")

        return LLMResponse(
            content=content,
            model=config.model_name,
            provider=config.provider.value,
            usage={
                "prompt_tokens": int(usage.get("prompt_tokens", 0)),
                "completion_tokens": int(usage.get("completion_tokens", 0)),
                "total_tokens": int(usage.get("total_tokens", 0))
            },
            finish_reason=finish_reason,
            latency_ms=int((time.time() - started) * 1000)
        )

    def _call_baidu_api(self, messages: List[Message], config: LLMConfig,
                        temperature: float = None, max_tokens: int = None) -> LLMResponse:
        """调用百度文心一言 API (非标准格式)."""
        if not config.api_key:
            return LLMResponse(
                content="未配置 BAIDU_API_KEY 环境变量",
                model=config.model_name,
                provider=config.provider.value,
                usage={"prompt_tokens": 0, "completion_tokens": 0},
                latency_ms=0,
                finish_reason="auth_error"
            )

        endpoint = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-4.0-8k-latest"
        access_token = config.api_key  # 百度需要先get access_token,这里简化处理

        payload = {
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature if temperature is not None else config.temperature,
            "max_output_tokens": max_tokens if max_tokens is not None else config.max_tokens,
        }

        headers = {"Content-Type": "application/json"}
        url = f"{endpoint}?access_token={access_token}"

        started = time.time()
        try:
            req = request.Request(
                url,
                data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                headers=headers,
                method="POST"
            )
            with request.urlopen(req, timeout=config.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception as exc:
            return LLMResponse(
                content=f"百度 API 调用失败: {str(exc)}",
                model=config.model_name,
                provider=config.provider.value,
                usage={"prompt_tokens": 0, "completion_tokens": 0},
                latency_ms=int((time.time() - started) * 1000),
                finish_reason="error"
            )

        if "error_code" in data:
            return LLMResponse(
                content=f"百度 API 错误: {data.get('error_msg', data.get('error_code'))}",
                model=config.model_name,
                provider=config.provider.value,
                usage={"prompt_tokens": 0, "completion_tokens": 0},
                latency_ms=int((time.time() - started) * 1000),
                finish_reason="error"
            )

        return LLMResponse(
            content=data.get("result", ""),
            model=config.model_name,
            provider=config.provider.value,
            usage={
                "prompt_tokens": data.get("usage", {}).get("prompt_tokens", 0),
                "completion_tokens": data.get("usage", {}).get("completion_tokens", 0),
                "total_tokens": data.get("usage", {}).get("total_tokens", 0)
            },
            latency_ms=int((time.time() - started) * 1000)
        )

    def _call_anthropic_api(self, messages: List[Message], config: LLMConfig,
                            temperature: float = None, max_tokens: int = None) -> LLMResponse:
        """调用 Anthropic Claude API (非标准格式)."""
        if not config.api_key:
            return LLMResponse(
                content="未配置 ANTHROPIC_API_KEY 环境变量",
                model=config.model_name,
                provider=config.provider.value,
                usage={"prompt_tokens": 0, "completion_tokens": 0},
                latency_ms=0,
                finish_reason="auth_error"
            )

        endpoint = "https://api.anthropic.com/v1/messages"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": config.api_key,
            "anthropic-version": "2023-06-01",
            "anthropic-dangerous-direct-browser-access": "true"
        }

        # 转换消息格式
        system_msg = ""
        filtered_messages = []
        for msg in messages:
            if msg.role == "system":
                system_msg = msg.content
            else:
                filtered_messages.append({"role": msg.role, "content": msg.content})

        payload = {
            "model": config.model_name,
            "messages": filtered_messages,
            "max_tokens": max_tokens if max_tokens is not None else config.max_tokens,
            "temperature": temperature if temperature is not None else config.temperature,
        }
        if system_msg:
            payload["system"] = system_msg

        started = time.time()
        try:
            req = request.Request(
                endpoint,
                data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                headers=headers,
                method="POST"
            )
            with request.urlopen(req, timeout=config.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception as exc:
            return LLMResponse(
                content=f"Anthropic API 调用失败: {str(exc)}",
                model=config.model_name,
                provider=config.provider.value,
                usage={"prompt_tokens": 0, "completion_tokens": 0},
                latency_ms=int((time.time() - started) * 1000),
                finish_reason="error"
            )

        if "error" in data:
            return LLMResponse(
                content=f"Anthropic API 错误: {data['error'].get('message', str(data['error']))}",
                model=config.model_name,
                provider=config.provider.value,
                usage={"prompt_tokens": 0, "completion_tokens": 0},
                latency_ms=int((time.time() - started) * 1000),
                finish_reason="error"
            )

        return LLMResponse(
            content=data.get("content", [{}])[0].get("text", ""),
            model=config.model_name,
            provider=config.provider.value,
            usage={
                "prompt_tokens": data.get("usage", {}).get("input_tokens", 0),
                "completion_tokens": data.get("usage", {}).get("output_tokens", 0),
                "total_tokens": data.get("usage", {}).get("input_tokens", 0) + data.get("usage", {}).get("output_tokens", 0)
            },
            latency_ms=int((time.time() - started) * 1000)
        )

    def _normalize_chat_endpoint(self, api_base: Optional[str]) -> str:
        """标准化 chat completions 端点."""
        base = (api_base or "http://127.0.0.1:11434/v1").rstrip("/")
        if base.endswith("/chat/completions"):
            return base
        if base.endswith("/v1"):
            return f"{base}/chat/completions"
        return f"{base}/v1/chat/completions"

    def _extract_content_from_response(self, data: Dict[str, Any]) -> str:
        """从 OpenAI 兼容响应中提取文本."""
        if not isinstance(data, dict):
            return str(data)

        choices = data.get("choices", [])
        if not choices:
            return json.dumps(data, ensure_ascii=False)

        message = choices[0].get("message", {})
        content = message.get("content", "")
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        parts.append(item.get("text", ""))
                else:
                    parts.append(str(item))
            return "\n".join(part for part in parts if part)
        return content or json.dumps(choices[0], ensure_ascii=False)

    def get_model_info(self, model: str = None) -> Dict[str, Any]:
        """get模型信息"""
        if model:
            config = self.configs.get(model)
            if not config:
                return {}
            return {
                "name": model,
                "provider": config.provider.value,
                "model_name": config.model_name,
                "api_base": config.api_base,
                "capabilities": [c.value for c in config.capabilities],
                "cost_per_1k_tokens": config.cost_per_1k_tokens
            }

        return {
            name: {
                "provider": config.provider.value,
                "model_name": config.model_name,
                "api_base": config.api_base,
                "capabilities": [c.value for c in config.capabilities],
                "cost_per_1k_tokens": config.cost_per_1k_tokens
            }
            for name, config in self.configs.items()
        }

    def add_cloud_model(self, name: str, provider: str, model_name: str,
                        api_base: str, api_key: str = None,
                        temperature: float = 0.7, max_tokens: int = 2000):
        """
        动态添加云端模型配置.

        Args:
            name: 模型别名 (如 "my-doubao")
            provider: 提供商 (doubit/deepseek/hunyuan/qwen/openai)
            model_name: API 中的模型名
            api_base: API Base URL
            api_key: API Key (可选,会从环境变量加载)
            temperature: 默认温度
            max_tokens: 默认最大 token 数
        """
        provider_map = {
            "doubit": ModelProvider.DOUBIT,
            "deepseek": ModelProvider.DEEPSEEK,
            "hunyuan": ModelProvider.HUNYUAN,
            "qwen": ModelProvider.ALIBABA,
            "openai": ModelProvider.OPENAI,
            "baidu": ModelProvider.BAIDU,
            "anthropic": ModelProvider.ANTHROPIC,
        }

        provider_enum = provider_map.get(provider.lower())
        if not provider_enum:
            raise ValueError(f"未知提供商: {provider},支持: {list(provider_map.keys())}")

        self.configs[name] = LLMConfig(
            provider=provider_enum,
            model_name=model_name,
            api_base=api_base,
            api_key=api_key or os.getenv(f"{provider.upper()}_API_KEY"),
            temperature=temperature,
            max_tokens=max_tokens,
            capabilities=[ModelCapability.CHAT, ModelCapability.ANALYSIS]
        )

    def configure_from_env(self):
        """从环境变量批量配置模型 API."""
        # 豆包/火山方舟
        if os.getenv("VOLCENGINE_API_KEY"):
            volc_base = os.getenv("DOUBAO_BASE_URL", "https://ark.cn-beijing.volces.com/v1")
            volc_model = os.getenv("DOUBAO_MODEL", "doubao-pro-32k")
            self.configs["doubao"] = LLMConfig(
                provider=ModelProvider.DOUBIT,
                model_name=volc_model,
                api_base=volc_base,
                api_key=os.getenv("VOLCENGINE_API_KEY"),
                temperature=0.7,
                max_tokens=4000,
                capabilities=[ModelCapability.CHAT, ModelCapability.ANALYSIS]
            )

        # DeepSeek
        if os.getenv("DEEPSEEK_API_KEY"):
            deepseek_base = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
            deepseek_model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
            self.configs["deepseek"] = LLMConfig(
                provider=ModelProvider.DEEPSEEK,
                model_name=deepseek_model,
                api_base=deepseek_base,
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                temperature=0.3,
                max_tokens=4000,
                capabilities=[ModelCapability.CHAT, ModelCapability.ANALYSIS, ModelCapability.CODE]
            )

        # 腾讯混元/元宝
        if os.getenv("HUNYUAN_API_KEY"):
            hunyuan_base = os.getenv("HUNYUAN_BASE_URL", "https://api.hunyuan.cloud.tencent.com/v1")
            hunyuan_model = os.getenv("HUNYUAN_MODEL", "hunyuan-turbos-latest")
            self.configs["hunyuan"] = LLMConfig(
                provider=ModelProvider.HUNYUAN,
                model_name=hunyuan_model,
                api_base=hunyuan_base,
                api_key=os.getenv("HUNYUAN_API_KEY"),
                temperature=0.5,
                max_tokens=4000,
                capabilities=[ModelCapability.CHAT, ModelCapability.ANALYSIS]
            )

        # 通义千问 (从环境变量覆盖预设)
        if os.getenv("DASHSCOPE_API_KEY"):
            qwen_base = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
            qwen_model = os.getenv("QWEN_MODEL", "qwen-max")
            self.configs["qwen"] = LLMConfig(
                provider=ModelProvider.ALIBABA,
                model_name=qwen_model,
                api_base=qwen_base,
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                temperature=0.7,
                max_tokens=4000,
                capabilities=[ModelCapability.CHAT, ModelCapability.ANALYSIS, ModelCapability.CODE]
            )

        # OpenAI
        if os.getenv("OPENAI_API_KEY"):
            openai_base = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
            openai_model = os.getenv("OPENAI_MODEL", "gpt-4")
            self.configs["openai"] = LLMConfig(
                provider=ModelProvider.OPENAI,
                model_name=openai_model,
                api_base=openai_base,
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0.7,
                max_tokens=2000,
                capabilities=[ModelCapability.CHAT, ModelCapability.ANALYSIS, ModelCapability.CODE]
            )

        # MiniMax M2.7 (OpenAI兼容格式)
        if os.getenv("MINIMAX_API_KEY"):
            minimax_base = os.getenv("MINIMAX_BASE_URL", "https://api.minimax.chat/v1")
            minimax_model = os.getenv("MINIMAX_MODEL", "minimax-m2.7")
            self.configs["minimax"] = LLMConfig(
                provider=ModelProvider.OPENAI,  # MiniMax使用OpenAI兼容格式
                model_name=minimax_model,
                api_base=minimax_base,
                api_key=os.getenv("MINIMAX_API_KEY"),
                temperature=0.7,
                max_tokens=4000,
                capabilities=[ModelCapability.CHAT, ModelCapability.ANALYSIS, ModelCapability.CODE]
            )

    def list_available_models(self) -> Dict[str, Any]:
        """列出所有可用的模型及其状态."""
        result = {}
        for name, config in self.configs.items():
            has_key = bool(config.api_key)
            has_endpoint = bool(config.api_base)
            available = has_key and has_endpoint and config.provider != ModelProvider.MOCK

            result[name] = {
                "provider": config.provider.value,
                "model_name": config.model_name,
                "api_key_configured": has_key,
                "api_base_configured": has_endpoint,
                "available": available,
                "status": "ready" if available else ("missing_key" if not has_key else ("missing_endpoint" if not has_endpoint else "mock"))
            }
        return result

    def test_connection(self, model: str = None) -> Dict[str, Any]:
        """
        测试模型连接.

        Args:
            model: 模型名 (默认使用配置的默认模型)

        Returns:
            测试结果字典
        """
        selected = model or self.get_default_model()
        config = self.configs.get(selected)

        if not config:
            return {"success": False, "error": f"未知模型: {selected}"}

        if not config.api_key:
            return {"success": False, "error": "未配置 API Key", "model": selected}

        if not config.api_base:
            return {"success": False, "error": "未配置 API Base URL", "model": selected}

        # 发送简单测试消息
        response = self.chat(
            "请回复 'OK' 确认连接正常.",
            model=selected,
            max_tokens=50,
            temperature=0
        )

        return {
            "success": response.finish_reason != "error",
            "model": selected,
            "provider": config.provider.value,
            "latency_ms": response.latency_ms,
            "response_preview": response.content[:200] if response.content else None,
            "error": response.content if response.finish_reason == "error" else None
        }

    # ══════════════════════════════════════════════════════════
    # 云端模型配置 API v2.0
    # 支持通过API自定义配置所有云端大模型
    # ══════════════════════════════════════════════════════════

    def add_cloud_model(
        self,
        name: str,
        model_name: str,
        api_base: str,
        api_key: str = None,
        provider: str = "custom",
        temperature: float = 0.7,
        max_tokens: int = 4000,
        timeout: int = 60,
        capabilities: List[str] = None,
        context_window: int = 128000,
        cost_per_1k: float = 0.0,
        save: bool = True
    ) -> Dict[str, Any]:
        """
        [v2.0] 添加自定义云端模型配置.

        Args:
            name: 模型别名 (如 "my-deepseek", "custom-gpt4")
            model_name: API中的模型名 (如 "deepseek-chat", "gpt-4")
            api_base: API地址 (如 "https://api.deepseek.com/v1")
            api_key: API密钥
            provider: 提供商标识 (custom/openai/anthropic/deepseek/qwen/doubao等)
            temperature: 默认温度
            max_tokens: 最大输出token
            timeout: 超时秒数
            capabilities: 能力列表 ["chat", "analysis", "code", "vision"]
            context_window: 上下文窗口大小
            cost_per_1k: 每1K token成本
            save: 是否持久化到配置文件

        Returns:
            配置结果
        """
        # 映射提供商
        provider_map = {
            "openai": ModelProvider.OPENAI,
            "anthropic": ModelProvider.ANTHROPIC,
            "deepseek": ModelProvider.DEEPSEEK,
            "qwen": ModelProvider.ALIBABA,
            "doubao": ModelProvider.DOUBIT,
            "hunyuan": ModelProvider.HUNYUAN,
            "baidu": ModelProvider.BAIDU,
            "custom": ModelProvider.OPENAI,  # 自定义模型使用OpenAI兼容格式
        }
        mapped_provider = provider_map.get(provider.lower(), ModelProvider.OPENAI)

        # 映射能力
        cap_map = {
            "chat": ModelCapability.CHAT,
            "analysis": ModelCapability.ANALYSIS,
            "code": ModelCapability.CODE,
            "vision": ModelCapability.VISION,
            "completion": ModelCapability.COMPLETION,
        }
        caps = [cap_map.get(c.lower(), ModelCapability.CHAT) for c in (capabilities or ["chat"])]

        # 创建配置
        config = LLMConfig(
            provider=mapped_provider,
            model_name=model_name,
            api_key=api_key,
            api_base=api_base,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
            capabilities=caps,
            cost_per_1k_tokens=cost_per_1k
        )

        # 注册模型
        self.configs[name] = config

        # 持久化
        if save:
            self._save_cloud_model_config(name, config)

        return {
            "success": True,
            "name": name,
            "model": model_name,
            "provider": provider,
            "api_base": api_base,
            "message": f"模型 '{name}' 配置成功"
        }

    def update_cloud_model(
        self,
        name: str,
        api_key: str = None,
        api_base: str = None,
        temperature: float = None,
        max_tokens: int = None,
        enabled: bool = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        [v2.0] 更新已存在的云端模型配置.

        Args:
            name: 模型名
            api_key: 新API密钥
            api_base: 新API地址
            temperature: 新温度
            max_tokens: 新最大token
            enabled: 是否启用

        Returns:
            更新结果
        """
        if name not in self.configs:
            return {"success": False, "error": f"模型 '{name}' 不存在"}

        config = self.configs[name]

        if api_key is not None:
            config.api_key = api_key
        if api_base is not None:
            config.api_base = api_base
        if temperature is not None:
            config.temperature = temperature
        if max_tokens is not None:
            config.max_tokens = max_tokens

        # 持久化
        self._save_cloud_model_config(name, config)

        return {
            "success": True,
            "name": name,
            "message": f"模型 '{name}' 配置已更新"
        }

    def delete_cloud_model(self, name: str) -> Dict[str, Any]:
        """
        [v2.0] 删除自定义云端模型配置.

        Args:
            name: 模型名

        Returns:
            删除结果
        """
        if name not in self.configs:
            return {"success": False, "error": f"模型 '{name}' 不存在"}

        # 不允许删除预设模型
        preset_names = list(self.PRESET_MODELS.keys())
        if name in preset_names:
            return {"success": False, "error": f"无法删除预设模型 '{name}'"}

        del self.configs[name]

        # 删除持久化配置
        self._delete_cloud_model_config(name)

        return {"success": True, "name": name, "message": f"模型 '{name}' 已删除"}

    def get_model_info(self, name: str = None) -> Dict[str, Any]:
        """
        [v2.0] 获取模型详细信息.

        Args:
            name: 模型名 (默认返回默认模型信息)

        Returns:
            模型配置详情
        """
        if name:
            config = self.configs.get(name)
            if not config:
                return {"success": False, "error": f"模型 '{name}' 不存在"}
        else:
            name = self.get_default_model()
            config = self.configs.get(name)

        if not config:
            return {"success": False, "error": "未找到模型配置"}

        return {
            "success": True,
            "name": name,
            "model_name": config.model_name,
            "provider": config.provider.value,
            "api_base": config.api_base,
            "api_key_configured": bool(config.api_key),
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
            "timeout": config.timeout,
            "capabilities": [c.value for c in config.capabilities],
            "cost_per_1k": config.cost_per_1k_tokens,
        }

    def list_cloud_providers(self) -> List[Dict[str, Any]]:
        """
        [v2.0] 列出所有支持的云端提供商.

        Returns:
            提供商列表
        """
        return [
            {"id": "openai", "name": "OpenAI", "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]},
            {"id": "anthropic", "name": "Anthropic Claude", "models": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"]},
            {"id": "deepseek", "name": "DeepSeek", "models": ["deepseek-chat", "deepseek-reasoner"]},
            {"id": "qwen", "name": "阿里通义千问", "models": ["qwen-max", "qwen-plus", "qwen-turbo"]},
            {"id": "doubao", "name": "字节豆包", "models": ["doubao-pro-32k", "doubao-lite-32k"]},
            {"id": "hunyuan", "name": "腾讯混元", "models": ["hunyuan-turbos", "hunyuan-vision"]},
            {"id": "baidu", "name": "百度文心一言", "models": ["ernie-bot-4", "ernie-bot-3.5"]},
            {"id": "custom", "name": "自定义 (OpenAI兼容)", "models": ["any-openai-compatible"]},
            {"id": "groq", "name": "Groq", "models": ["llama-3.3-70b-versatile", "mixtral-8x7b"]},
            {"id": "mistral", "name": "Mistral", "models": ["mistral-small", "mistral-large"]},
            {"id": "cohere", "name": "Cohere", "models": ["command-r-plus", "command-r"]},
            {"id": "together", "name": "Together AI", "models": ["meta-llama/Llama-3-70b-chat"]},
            {"id": "zhipu", "name": "智谱GLM", "models": ["glm-4-flash", "glm-4"]},
        ]

    def save_models_to_config(self, filepath: str = None) -> Dict[str, Any]:
        """
        [v2.0] 持久化所有自定义模型配置到文件.

        Args:
            filepath: 保存路径 (默认: data/llm/cloud_models.json)

        Returns:
            保存结果
        """
        if filepath is None:
            filepath = str(self.base_path / "cloud_models.json")

        # 收集自定义模型（排除预设模型）
        preset_names = set(self.PRESET_MODELS.keys())
        custom_models = {}

        for name, config in self.configs.items():
            if name in preset_names:
                continue
            custom_models[name] = {
                "model_name": config.model_name,
                "api_base": config.api_base,
                "api_key": config.api_key or "",
                "provider": config.provider.value,
                "temperature": config.temperature,
                "max_tokens": config.max_tokens,
                "timeout": config.timeout,
                "capabilities": [c.value for c in config.capabilities],
                "cost_per_1k": config.cost_per_1k_tokens,
            }

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(custom_models, f, ensure_ascii=False, indent=2)

            return {
                "success": True,
                "filepath": filepath,
                "count": len(custom_models),
                "message": f"已保存 {len(custom_models)} 个自定义模型"
            }
        except Exception as e:
            return {"success": False, "error": "操作失败"}

    def load_models_from_config(self, filepath: str = None) -> Dict[str, Any]:
        """
        [v2.0] 从配置文件加载自定义模型配置.

        Args:
            filepath: 配置文件路径

        Returns:
            加载结果
        """
        if filepath is None:
            filepath = str(self.base_path / "cloud_models.json")

        if not os.path.exists(filepath):
            return {"success": True, "count": 0, "message": "配置文件不存在，跳过加载"}

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                custom_models = json.load(f)

            loaded = 0
            for name, data in custom_models.items():
                provider_map = {
                    "openai": ModelProvider.OPENAI,
                    "anthropic": ModelProvider.ANTHROPIC,
                    "deepseek": ModelProvider.DEEPSEEK,
                    "alibaba": ModelProvider.ALIBABA,
                    "doubit": ModelProvider.DOUBIT,
                    "hunyuan": ModelProvider.HUNYUAN,
                    "baidu": ModelProvider.BAIDU,
                }

                cap_map = {
                    "chat": ModelCapability.CHAT,
                    "analysis": ModelCapability.ANALYSIS,
                    "code": ModelCapability.CODE,
                    "vision": ModelCapability.VISION,
                }

                caps = [cap_map.get(c, ModelCapability.CHAT) for c in data.get("capabilities", ["chat"])]

                config = LLMConfig(
                    provider=provider_map.get(data.get("provider", "openai"), ModelProvider.OPENAI),
                    model_name=data.get("model_name", name),
                    api_base=data.get("api_base", ""),
                    api_key=data.get("api_key") or None,
                    temperature=data.get("temperature", 0.7),
                    max_tokens=data.get("max_tokens", 4000),
                    timeout=data.get("timeout", 60),
                    capabilities=caps,
                    cost_per_1k_tokens=data.get("cost_per_1k", 0.0),
                )

                self.configs[name] = config
                loaded += 1

            return {
                "success": True,
                "count": loaded,
                "message": f"已加载 {loaded} 个自定义模型"
            }
        except Exception as e:
            return {"success": False, "error": "操作失败"}

    def _save_cloud_model_config(self, name: str, config: LLMConfig):
        """保存单个模型配置到文件"""
        config_file = self.base_path / "cloud_models.json"

        # 读取现有配置
        existing = {}
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
            except Exception as e:
                logger.debug(f"读取 LLM 配置文件失败，使用空配置: {e}")
                existing = {}

        # 更新配置
        existing[name] = {
            "model_name": config.model_name,
            "api_base": config.api_base or "",
            "api_key": config.api_key or "",
            "provider": config.provider.value,
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
            "timeout": config.timeout,
            "capabilities": [c.value for c in config.capabilities],
            "cost_per_1k": config.cost_per_1k_tokens,
        }

        # 写入
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)

    def _delete_cloud_model_config(self, name: str):
        """删除模型配置"""
        config_file = self.base_path / "cloud_models.json"

        if not config_file.exists():
            return

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                existing = json.load(f)

            if name in existing:
                del existing[name]

                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(existing, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"删除 LLM 配置 '{name}' 失败: {e}")

    def validate_cloud_model(
        self,
        api_base: str,
        model_name: str,
        api_key: str = None
    ) -> Dict[str, Any]:
        """
        [v2.0] 验证云端模型配置是否可用.

        Args:
            api_base: API地址
            model_name: 模型名
            api_key: API密钥

        Returns:
            验证结果
        """
        endpoint = self._normalize_chat_endpoint(api_base)
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": "Hi"}],
            "max_tokens": 5,
        }

        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            req = request.Request(
                endpoint,
                data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                headers=headers,
                method="POST"
            )

            started = time.time()
            with request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            return {
                "success": True,
                "latency_ms": int((time.time() - started) * 1000),
                "response": data.get("choices", [{}])[0].get("message", {}).get("content", ""),
                "model": model_name,
                "provider": api_base.split("//")[1].split("/")[0] if "//" in api_base else "unknown"
            }

        except error.HTTPError as e:
            return {"success": False, "error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"success": False, "error": "操作失败"}


# ══════════════════════════════════════════════════════════
# 模块级便捷函数
# ══════════════════════════════════════════════════════════

# 全局LLM服务实例
_llm_service_instance: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """获取全局LLM服务实例"""
    global _llm_service_instance
    if _llm_service_instance is None:
        _llm_service_instance = LLMService()
    return _llm_service_instance


def add_cloud_model(**kwargs) -> Dict[str, Any]:
    """模块级便捷函数：添加云端模型"""
    return get_llm_service().add_cloud_model(**kwargs)


def list_available_models() -> Dict[str, Any]:
    """模块级便捷函数：列出可用模型"""
    return get_llm_service().list_available_models()


def test_connection(model: str = None) -> Dict[str, Any]:
    """模块级便捷函数：测试连接"""
    return get_llm_service().test_connection(model)


def get_model_info(name: str = None) -> Dict[str, Any]:
    """模块级便捷函数：获取模型信息"""
    return get_llm_service().get_model_info(name)
