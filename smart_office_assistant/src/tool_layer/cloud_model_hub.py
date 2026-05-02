"""CloudModelHub - Unified Cloud LLM Hub.

__all__ = [
    'consult_multiple',
    'consult_teacher',
    'get_teacher_report',
    'list_teachers',
    'register_teacher',
    'score_teacher',
]

Manages cloud LLM API endpoints with unified interface.
"""

import logging
import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from urllib import request, error

logger = logging.getLogger(__name__)

# 导入熔断器（可选，如果导入失败则不使用熔断器）
try:
    from src.utils.retry_utils import get_circuit_breaker
    _HAS_CIRCUIT_BREAKER = True
except ImportError:
    _HAS_CIRCUIT_BREAKER = False


class TeacherSpecialty(Enum):
    REASONING = "reasoning"
    CODE = "code"
    CREATIVE = "creative"
    MULTIMODAL = "multimodal"
    FAST = "fast"
    GENERAL = "general"
    RAG = "rag"
    ACADEMIC = "academic"

@dataclass
class TeacherConfig:
    teacher_id: str
    name: str
    provider: str
    model_name: str
    api_base: str
    api_key: Optional[str] = None
    specialties: List[TeacherSpecialty] = field(default_factory=list)
    context_window: int = 32768
    max_output_tokens: int = 4096
    cost_per_1k: float = 0.0
    free_tier: bool = True
    rate_limit_rpm: int = 60
    timeout: int = 90
    enabled: bool = True

@dataclass
class TeacherResponse:
    teacher_id: str
    teacher_name: str
    content: str
    latency_ms: int
    usage: Dict[str, int] = field(default_factory=dict)
    finish_reason: str = "stop"
    quality_score: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class ConsultationRequest:
    task: str
    question: str
    context: str = ""
    preferred_teachers: List[str] = field(default_factory=list)
    required_specialties: List[TeacherSpecialty] = field(default_factory=list)
    max_teachers: int = 3
    timeout_per_teacher: int = 60

class CloudModelHub:
    """Unified hub for all free cloud LLM teachers."""

    PRESET_TEACHERS: Dict[str, TeacherConfig] = {
        "deepseek-chat": TeacherConfig(
            teacher_id="deepseek-chat", name="DeepSeek", provider="deepseek",
            model_name="deepseek-chat", api_base="https://api.deepseek.com/v1",
            specialties=[TeacherSpecialty.REASONING, TeacherSpecialty.CODE],
            context_window=64000, cost_per_1k=0.001, free_tier=True, rate_limit_rpm=60),
        "deepseek-reasoner": TeacherConfig(
            teacher_id="deepseek-reasoner", name="DeepSeek-Reasoner", provider="deepseek",
            model_name="deepseek-reasoner", api_base="https://api.deepseek.com/v1",
            specialties=[TeacherSpecialty.REASONING],
            context_window=64000, cost_per_1k=0.002, free_tier=True, rate_limit_rpm=60),
        "groq-llama-70b": TeacherConfig(
            teacher_id="groq-llama-70b", name="Groq-Llama", provider="groq",
            model_name="llama-3.3-70b-versatile", api_base="https://api.groq.com/openai/v1",
            specialties=[TeacherSpecialty.FAST, TeacherSpecialty.GENERAL],
            context_window=8192, cost_per_1k=0.0, free_tier=True, rate_limit_rpm=30),
        "groq-mixtral": TeacherConfig(
            teacher_id="groq-mixtral", name="Groq-Mixtral", provider="groq",
            model_name="mixtral-8x7b-32768", api_base="https://api.groq.com/openai/v1",
            specialties=[TeacherSpecialty.FAST, TeacherSpecialty.CODE],
            context_window=32768, cost_per_1k=0.0, free_tier=True, rate_limit_rpm=30),
        "gemini-2.0-flash": TeacherConfig(
            teacher_id="gemini-2.0-flash", name="Gemini", provider="google",
            model_name="gemini-2.0-flash", api_base="https://generativelanguage.googleapis/v1beta/models",
            specialties=[TeacherSpecialty.MULTIMODAL, TeacherSpecialty.FAST, TeacherSpecialty.GENERAL],
            context_window=1000000, cost_per_1k=0.0, free_tier=True, rate_limit_rpm=15),
        "mistral-small": TeacherConfig(
            teacher_id="mistral-small", name="Mistral", provider="mistral",
            model_name="mistral-small-latest", api_base="https://api.mistral.ai/v1",
            specialties=[TeacherSpecialty.GENERAL, TeacherSpecialty.CREATIVE],
            context_window=32000, cost_per_1k=0.002, free_tier=True, rate_limit_rpm=60),
        "mistral-large": TeacherConfig(
            teacher_id="mistral-large", name="Mistral-Large", provider="mistral",
            model_name="mistral-large-latest", api_base="https://api.mistral.ai/v1",
            specialties=[TeacherSpecialty.REASONING, TeacherSpecialty.ACADEMIC],
            context_window=128000, cost_per_1k=0.008, free_tier=False, rate_limit_rpm=60),
        "cohere-command-r": TeacherConfig(
            teacher_id="cohere-command-r", name="Cohere", provider="cohere",
            model_name="command-r-plus-08-2024", api_base="https://api.cohere.ai/v1",
            specialties=[TeacherSpecialty.RAG, TeacherSpecialty.REASONING],
            context_window=128000, cost_per_1k=0.003, free_tier=True, rate_limit_rpm=20),
        "together-llama": TeacherConfig(
            teacher_id="together-llama", name="Together", provider="together",
            model_name="meta-llama/Llama-3-70b-chat-hf", api_base="https://api.together.ai/v1",
            specialties=[TeacherSpecialty.GENERAL, TeacherSpecialty.CODE],
            context_window=8192, cost_per_1k=0.00088, free_tier=True, rate_limit_rpm=60),
        "hf-llama": TeacherConfig(
            teacher_id="hf-llama", name="HuggingFace", provider="huggingface",
            model_name="meta-llama/Llama-3-70b-Instruct", api_base="https://api-inference.huggingface.co/v1",
            specialties=[TeacherSpecialty.GENERAL],
            context_window=8192, cost_per_1k=0.0, free_tier=True, rate_limit_rpm=30),
        "openrouter-aggregate": TeacherConfig(
            teacher_id="openrouter-aggregate", name="OpenRouter", provider="openrouter",
            model_name="openai/gpt-4o-mini", api_base="https://openrouter.ai/api/v1",
            specialties=[TeacherSpecialty.GENERAL],
            context_window=128000, cost_per_1k=0.0, free_tier=True, rate_limit_rpm=60),
        "zhipu-free": TeacherConfig(
            teacher_id="zhipu-free", name="Zhipu", provider="zhipu",
            model_name="glm-4-flash", api_base="https://open.bigmodel.cn/api/paas/v4",
            specialties=[TeacherSpecialty.GENERAL, TeacherSpecialty.CODE],
            context_window=128000, cost_per_1k=0.0, free_tier=True, rate_limit_rpm=60),
    }

    def __init__(self, base_path: str = None):
        self.base_path = os.path.join(base_path or ".", "data", "cloud_hub")
        os.makedirs(self.base_path, exist_ok=True)
        self.teachers: Dict[str, TeacherConfig] = {}
        for tid, config in self.PRESET_TEACHERS.items():
            self.teachers[tid] = TeacherConfig(**config.__dict__)
        self.teacher_stats: Dict[str, Dict] = self._load_stats()
        self.rate_limit_tracker: Dict[str, List[float]] = {}
        self._load_api_keys()

    def _load_stats(self) -> Dict:
        f = os.path.join(self.base_path, "teacher_stats.json")
        if os.path.exists(f):
            try:
                with open(f, encoding="utf-8") as fp:
                    return json.load(fp)
            except Exception as e:
                logger.debug(f"加载教师统计失败: {e}")
        return {"total_calls": 0, "total_success": 0, "total_errors": 0,
                "avg_latency_ms": 0, "total_tokens": 0, "quality_scores": [], "last_used": None}

    def _load_api_keys(self):
        """从环境变量加载各 provider 的 API keys."""
        env_map = {
            "DEEPSEEK_API_KEY": ["deepseek-chat", "deepseek-reasoner"],
            "GROQ_API_KEY": ["groq-llama-70b", "groq-mixtral"],
            "GOOGLE_API_KEY": "gemini-2.0-flash",
            "MISTRAL_API_KEY": ["mistral-small", "mistral-large"],
            "COHERE_API_KEY": "cohere-command-r",
            "TOGETHER_API_KEY": "together-llama",
            "HF_API_KEY": "hf-llama",
            "OPENROUTER_API_KEY": "openrouter-aggregate",
            "ZHIPU_API_KEY": "zhipu-free",
        }
        for env_var, teacher_ids in env_map.items():
            key = os.getenv(env_var)
            if not key:
                continue
            if isinstance(teacher_ids, str):
                teacher_ids = [teacher_ids]
            for tid in teacher_ids:
                if tid in self.teachers:
                    self.teachers[tid].api_key = key

    def _save_stats(self):
        f = os.path.join(self.base_path, "teacher_stats.json")
        try:
            with open(f, "w", encoding="utf-8") as fp:
                json.dump(self.teacher_stats, fp, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.debug(f"保存教师统计失败: {e}")

    def _check_rate_limit(self, teacher_id: str) -> bool:
        now = time.time()
        if teacher_id not in self.rate_limit_tracker:
            self.rate_limit_tracker[teacher_id] = []
        self.rate_limit_tracker[teacher_id] = [t for t in self.rate_limit_tracker[teacher_id] if now - t < 60]
        teacher = self.teachers.get(teacher_id)
        if not teacher:
            return False
        if len(self.rate_limit_tracker[teacher_id]) >= teacher.rate_limit_rpm:
            return True
        self.rate_limit_tracker[teacher_id].append(now)
        return False

    def consult_teacher(self, teacher_id: str, prompt: str,
                        system_prompt: str = "", temperature: float = 0.3,
                        max_tokens: int = 2000, context: str = "") -> TeacherResponse:
        teacher = self.teachers.get(teacher_id)
        if not teacher:
            return TeacherResponse(teacher_id=teacher_id, teacher_name=teacher_id,
                                   content=f"Unknown teacher: {teacher_id}", latency_ms=0, quality_score=0.0)
        if not teacher.api_key:
            return TeacherResponse(teacher_id=teacher_id, teacher_name=teacher.name,
                                   content=f"[{teacher.name}] API key not configured", latency_ms=0, quality_score=0.0)
        if self._check_rate_limit(teacher_id):
            return TeacherResponse(teacher_id=teacher_id, teacher_name=teacher.name,
                                   content=f"[{teacher.name}] Rate limited", latency_ms=0, quality_score=0.0,
                                   finish_reason="rate_limited")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if context:
            messages.append({"role": "system", "content": "Context: " + context})
        messages.append({"role": "user", "content": prompt})

        response = self._call_api(teacher, messages, temperature, max_tokens)
        self._update_stats(teacher_id, response)
        return response

    def consult_multiple(self, request: ConsultationRequest) -> List[TeacherResponse]:
        candidates = self._select_best_teachers(request)
        if not candidates:
            return [TeacherResponse(teacher_id="none", teacher_name="No teacher",
                                   content="No available teachers found", latency_ms=0, quality_score=0.0)]
        return [self.consult_teacher(tid, request.question, context=request.context) for tid in candidates]

    def _select_best_teachers(self, request: ConsultationRequest) -> List[str]:
        candidates = []
        if request.preferred_teachers:
            for tid in request.preferred_teachers:
                if tid in self.teachers and self.teachers[tid].enabled and not self._check_rate_limit(tid):
                    candidates.append(tid)
        if not candidates and request.required_specialties:
            for tid, teacher in self.teachers.items():
                if teacher.enabled and not self._check_rate_limit(tid):
                    if any(s in teacher.specialties for s in request.required_specialties):
                        candidates.append(tid)
        if not candidates:
            for tid, teacher in self.teachers.items():
                if teacher.enabled and not self._check_rate_limit(tid):
                    if tid not in candidates:
                        candidates.append(tid)

        def score_teacher(tid):
            stats = self.teacher_stats.get(tid, {})
            sr = stats.get("total_success", 0) / max(stats.get("total_calls", 1), 1)
            lat = stats.get("avg_latency_ms", 999999)
            return sr * 0.6 + max(0, 1 - lat / 10000) * 0.4

        candidates.sort(key=score_teacher, reverse=True)
        return candidates[:request.max_teachers]

    def _call_api(self, teacher: TeacherConfig, messages: List[Dict],
                  temperature: float, max_tokens: int) -> TeacherResponse:
        """调用API [v4.0 新增：熔断器保护]"""
        # 熔断器检查
        cb = None
        if _HAS_CIRCUIT_BREAKER:
            try:
                cb = get_circuit_breaker(f"cloud-model-hub-{teacher.teacher_id}")
                if not cb.is_available():
                    logger.warning(f"[熔断器] {teacher.name} 熔断中，跳过调用")
                    return TeacherResponse(
                        teacher_id=teacher.teacher_id,
                        teacher_name=teacher.name,
                        content=f"[{teacher.name}] 服务熔断中，请稍后重试",
                        latency_ms=0,
                        quality_score=0.0,
                        finish_reason="circuit_breaker_open"
                    )
            except Exception as e:
                logger.debug(f"[熔断器] 获取熔断器失败: {e}")
                cb = None
        
        endpoint = self._build_endpoint(teacher)
        payload = {"model": teacher.model_name, "messages": messages,
                   "temperature": temperature, "max_tokens": min(max_tokens, teacher.max_output_tokens),
                   "stream": False}
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {teacher.api_key}"}

        if teacher.provider == "google":
            payload.pop("model")
            endpoint = f"{endpoint}/{teacher.model_name}:generateContent"
            headers = {"Content-Type": "application/json", "x-goog-api-key": teacher.api_key}

        started = time.time()
        try:
            req = request.Request(endpoint,
                                  data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                                  headers=headers, method="POST")
            with request.urlopen(req, timeout=teacher.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            
            # 成功：记录成功
            if cb:
                try:
                    cb.record_success()
                except Exception:
                    pass
            
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore") if hasattr(exc, "read") else str(exc)
            
            # 失败：记录失败
            if cb:
                try:
                    cb.record_failure()
                except Exception:
                    pass
            
            return TeacherResponse(teacher_id=teacher.teacher_id, teacher_name=teacher.name,
                                   content=f"[{teacher.name}] HTTP {exc.code}: {detail[:300]}",
                                   latency_ms=int((time.time() - started) * 1000),
                                   quality_score=0.0, finish_reason="error")
        except Exception as exc:
            # 失败：记录失败
            if cb:
                try:
                    cb.record_failure()
                except Exception:
                    pass
            
            return TeacherResponse(teacher_id=teacher.teacher_id, teacher_name=teacher.name,
                                   content=f"[{teacher.name}] Error: {str(exc)}",
                                   latency_ms=int((time.time() - started) * 1000),
                                   quality_score=0.0, finish_reason="error")

        content = self._extract_content(teacher.provider, data)
        usage = self._extract_usage(teacher.provider, data)
        return TeacherResponse(teacher_id=teacher.teacher_id, teacher_name=teacher.name,
                               content=content, latency_ms=int((time.time() - started) * 1000),
                               usage=usage, quality_score=0.5, finish_reason="stop")

    def _build_endpoint(self, teacher: TeacherConfig) -> str:
        base = teacher.api_base.rstrip("/")
        if teacher.provider == "google":
            return base
        if base.endswith("/v1"):
            return f"{base}/chat/completions"
        return f"{base}/v1/chat/completions"

    def _extract_content(self, provider: str, data: Any) -> str:
        if not isinstance(data, dict):
            return str(data)
        if provider == "google":
            for c in data.get("candidates", []):
                parts = c.get("content", {}).get("parts", [])
                return "".join(p.get("text", "") for p in parts)
            return json.dumps(data, ensure_ascii=False)
        if provider == "cohere":
            return data.get("text", "")
        if provider == "huggingface":
            if isinstance(data, list):
                return data[0].get("generated_text", "")
            return data.get("generated_text", "")
        choices = data.get("choices", [])
        if choices:
            return choices[0].get("message", {}).get("content", "")
        return json.dumps(data, ensure_ascii=False)

    def _extract_usage(self, provider: str, data: Any) -> Dict:
        if not isinstance(data, dict):
            return {}
        if provider == "google":
            u = data.get("usageMetadata", {})
            return {"prompt_tokens": u.get("promptTokenCount", 0),
                    "completion_tokens": u.get("candidatesTokenCount", 0),
                    "total_tokens": u.get("totalTokenCount", 0)}
        u = data.get("usage", {})
        return {"prompt_tokens": u.get("prompt_tokens", 0),
                "completion_tokens": u.get("completion_tokens", 0),
                "total_tokens": u.get("total_tokens", 0)}

    def _update_stats(self, teacher_id: str, response: TeacherResponse):
        stats = self.teacher_stats.get(teacher_id, {})
        if not stats:
            return
        stats["total_calls"] = stats.get("total_calls", 0) + 1
        if response.finish_reason != "error":
            stats["total_success"] = stats.get("total_success", 0) + 1
        else:
            stats["total_errors"] = stats.get("total_errors", 0) + 1
        old_lat = stats.get("avg_latency_ms", 0)
        old_calls = stats.get("total_calls", 1)
        stats["avg_latency_ms"] = (old_lat * (old_calls - 1) + response.latency_ms) / old_calls
        usage = response.usage or {}
        stats["total_tokens"] = stats.get("total_tokens", 0) + usage.get("total_tokens", 0)
        if response.quality_score > 0:
            scores = stats.get("quality_scores", [])
            scores.append(response.quality_score)
            if len(scores) > 100:
                scores = scores[-100:]
            stats["quality_scores"] = scores
        stats["last_used"] = datetime.now().isoformat()
        self.teacher_stats[teacher_id] = stats
        if stats["total_calls"] % 10 == 0:
            self._save_stats()

    def register_teacher(self, config: TeacherConfig):
        self.teachers[config.teacher_id] = config
        if config.teacher_id not in self.teacher_stats:
            self.teacher_stats[config.teacher_id] = {
                "total_calls": 0, "total_success": 0, "total_errors": 0,
                "avg_latency_ms": 0, "total_tokens": 0, "quality_scores": [], "last_used": None}

    def list_teachers(self, specialty=None, free_only=False, available_only=False) -> List[Dict]:
        result = []
        for tid, teacher in self.teachers.items():
            if available_only and not teacher.enabled:
                continue
            if free_only and not teacher.free_tier:
                continue
            if specialty and specialty not in teacher.specialties:
                continue
            stats = self.teacher_stats.get(tid, {})
            result.append({
                "teacher_id": tid, "name": teacher.name, "provider": teacher.provider,
                "model_name": teacher.model_name,
                "specialties": [s.value for s in teacher.specialties],
                "free_tier": teacher.free_tier, "enabled": teacher.enabled,
                "has_api_key": bool(teacher.api_key),
                "total_calls": stats.get("total_calls", 0),
                "avg_latency_ms": round(stats.get("avg_latency_ms", 0), 0),
            })
        return result

    def get_teacher_report(self) -> Dict:
        report = {}
        for tid, stats in self.teacher_stats.items():
            teacher = self.teachers.get(tid)
            if not teacher:
                continue
            sr = stats.get("total_success", 0) / max(stats.get("total_calls", 1), 1)
            qs = stats.get("quality_scores", [])
            qavg = sum(qs) / max(len(qs), 1)
            report[tid] = {
                "name": teacher.name,
                "specialties": [s.value for s in teacher.specialties],
                "free_tier": teacher.free_tier, "enabled": teacher.enabled,
                "total_calls": stats.get("total_calls", 0),
                "success_rate": round(sr * 100, 1),
                "avg_latency_ms": round(stats.get("avg_latency_ms", 0), 0),
                "quality_score": round(qavg, 2),
                "rate_limited": self._check_rate_limit(tid),
            }
        return report
