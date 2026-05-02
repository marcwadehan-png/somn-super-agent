# -*- coding: utf-8 -*-
"""
Somn LLM 统一规则层 S1.0
==========================
所有子系统的 LLM 调用统一入口。

设计原则:
1. 云端优先 → 本地降级 → 规则回退
2. 所有子系统通过本文件获取 LLM 能力
3. 回退函数提供真实本地分析能力（非占位符）
4. 统一日志、统一错误处理、统一调用统计

v7.1 增强:
- 规则回退引擎增加 system_prompt 角色化响应 + 领域识别
- 网络搜索增加相关性过滤 + 引用标注
- call_module_llm 确保 fallback_func 返回类型一致

支持的子系统:
- NeuralMemory: 记忆编码/语义检索
- RefuteCore: 论证分析/反驳检测
- Pan-Wisdom: 学派融合/智慧整合
- DivineReason: 三层推理(深度推理/假设探索/元认知审视)
- TianShu: 管道分析/NLP/分类
- 双轨系统: 神政轨监管/神行轨执行
- DomainNexus: 知识查询/关联分析
- SageDispatch: 问题调度/决策分析
- OutputEngine: 内容生成/格式化输出

Usage:
    from knowledge_cells.llm_rule_layer import (
        llm_chat,           # 统一对话
        llm_analyze,        # 统一分析
        get_llm_status,     # LLM状态
        call_module_llm,    # 模块级调用（带回退）
    )

版本: 7.1.0
日期: 2026-04-29
"""

from __future__ import annotations

import time
import logging
import re
import hashlib
import threading
from typing import Any, Callable, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from functools import lru_cache
from enum import Enum

logger = logging.getLogger("Somn.LLM.RuleLayer")

# ═══════════════════════════════════════════════════════════════
#  数据结构
# ═══════════════════════════════════════════════════════════════

class LLMSource(Enum):
    """LLM 来源"""
    CLOUD = "cloud"       # 云端大模型
    LOCAL = "local"       # 本地大模型
    FALLBACK = "fallback"  # 规则回退


@dataclass
class LLMResponse:
    """统一 LLM 响应"""
    content: str
    source: LLMSource = LLMSource.FALLBACK
    model: str = ""
    provider: str = ""
    latency_ms: int = 0
    token_usage: Dict[str, int] = field(default_factory=dict)
    success: bool = True
    error: str = ""


@dataclass
class LLMCallStats:
    """LLM 调用统计"""
    total_calls: int = 0
    cloud_calls: int = 0
    local_calls: int = 0
    fallback_calls: int = 0
    total_latency_ms: int = 0
    errors: int = 0

    @property
    def avg_latency_ms(self) -> float:
        return self.total_latency_ms / max(self.total_calls, 1)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_calls": self.total_calls,
            "cloud_calls": self.cloud_calls,
            "local_calls": self.local_calls,
            "fallback_calls": self.fallback_calls,
            "avg_latency_ms": round(self.avg_latency_ms, 1),
            "errors": self.errors,
            "cloud_ratio": round(self.cloud_calls / max(self.total_calls, 1), 2),
        }


# 全局统计
_stats = LLMCallStats()

# ═══════════════════════════════════════════════════════════════
#  LLM 服务层 — 懒加载
# ═══════════════════════════════════════════════════════════════

_llm_service: Optional[Any] = None
_local_engine: Optional[Any] = None
_llm_initialized = False


def _init_llm_service():
    """懒加载初始化 LLM 服务"""
    global _llm_service, _local_engine, _llm_initialized
    if _llm_initialized:
        return
    _llm_initialized = True

    # 尝试导入统一 LLM 服务
    try:
        import sys
        from pathlib import Path
        project_root = Path(__file__).resolve().parents[1]
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        from llm_unified_config import get_unified_llm_service
        svc = get_unified_llm_service()
        if svc.is_ready:
            _llm_service = svc
            logger.info("[LLM-RuleLayer] 云端/本地LLM服务加载成功")
            return
    except Exception as e:
        logger.debug(f"[LLM-RuleLayer] 统一LLM服务不可用: {e}")

    # 尝试直接导入 tool_layer LLMService
    try:
        from smart_office_assistant.src.tool_layer.llm_service import get_llm_service
        _llm_service = get_llm_service()
        logger.info("[LLM-RuleLayer] LLMService 直接加载成功")
    except Exception as e:
        logger.debug(f"[LLM-RuleLayer] LLMService 不可用: {e}")

    # 尝试本地引擎
    try:
        from smart_office_assistant.src.core.local_llm_engine import get_engine_b
        _local_engine = get_engine_b()
        logger.info("[LLM-RuleLayer] 本地B大模型加载成功")
    except Exception:
        try:
            from smart_office_assistant.src.core.local_llm_engine import get_engine
            _local_engine = get_engine()
            logger.info("[LLM-RuleLayer] 本地A大模型加载成功")
        except Exception as e:
            logger.debug(f"[LLM-RuleLayer] 本地引擎不可用: {e}")

    if _llm_service is None and _local_engine is None:
        logger.info("[LLM-RuleLayer] 所有LLM不可用，使用规则回退引擎")


# ═══════════════════════════════════════════════════════════════
#  核心调用接口
# ═══════════════════════════════════════════════════════════════

def llm_chat(
    prompt: str,
    system_prompt: str = "",
    model: str = None,
    temperature: float = None,
    max_tokens: int = None,
    timeout: int = 30,
) -> LLMResponse:
    """
    统一 LLM 对话接口 — 云端优先 → 本地降级 → 规则回退

    Args:
        prompt: 用户提示
        system_prompt: 系统提示
        model: 指定模型
        temperature: 温度
        max_tokens: 最大token
        timeout: 超时秒数

    Returns:
        LLMResponse
    """
    _init_llm_service()
    _stats.total_calls += 1
    start = time.perf_counter()

    # 尝试云端
    if _llm_service is not None:
        try:
            if hasattr(_llm_service, 'chat'):
                resp = _llm_service.chat(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                latency = int((time.perf_counter() - start) * 1000)
                source = LLMSource.CLOUD if getattr(resp, 'source', '') != 'local' else LLMSource.LOCAL
                if source == LLMSource.CLOUD:
                    _stats.cloud_calls += 1
                else:
                    _stats.local_calls += 1
                _stats.total_latency_ms += latency

                return LLMResponse(
                    content=getattr(resp, 'content', str(resp)),
                    source=source,
                    model=getattr(resp, 'model', ''),
                    provider=getattr(resp, 'provider', ''),
                    latency_ms=getattr(resp, 'latency_ms', latency),
                    token_usage=getattr(resp, 'usage', {}),
                )
        except Exception as e:
            logger.warning(f"[LLM-RuleLayer] 云端调用失败: {e}")
            _stats.errors += 1

    # 尝试本地
    if _local_engine is not None:
        try:
            result = _local_engine.generate(
                prompt,
                temperature=temperature or 0.7,
                max_new_tokens=max_tokens or 500
            )
            latency = int((time.perf_counter() - start) * 1000)
            _stats.local_calls += 1
            _stats.total_latency_ms += latency

            return LLMResponse(
                content=result.text,
                source=LLMSource.LOCAL,
                model=getattr(result, 'model', 'local'),
                provider="local",
                latency_ms=getattr(result, 'latency_ms', latency),
                token_usage={"completion_tokens": getattr(result, 'tokens', 0)},
            )
        except Exception as e:
            logger.warning(f"[LLM-RuleLayer] 本地调用失败: {e}")
            _stats.errors += 1

    # 规则回退
    _stats.fallback_calls += 1
    latency = int((time.perf_counter() - start) * 1000)
    _stats.total_latency_ms += latency

    return LLMResponse(
        content=fallback_process(prompt, system_prompt),
        source=LLMSource.FALLBACK,
        latency_ms=latency,
    )


def llm_analyze(text: str, task: str, context: str = "", model: str = None) -> LLMResponse:
    """
    统一 LLM 分析接口

    Args:
        text: 待分析文本
        task: 任务类型（如"分类", "情感分析", "论证检验"）
        context: 上下文
        model: 指定模型

    Returns:
        LLMResponse
    """
    system_prompt = f"""你是一个专业的{task}引擎。请分析以下内容。
任务: {task}
:{f'上下文: {context}' if context else ''}"""
    prompt = f"请对以下内容进行{task}：\n\n{text}"

    return llm_chat(prompt=prompt, system_prompt=system_prompt, model=model)


def get_llm_status() -> Dict[str, Any]:
    """获取 LLM 服务状态"""
    _init_llm_service()
    return {
        "cloud_available": _llm_service is not None,
        "local_available": _local_engine is not None,
        "stats": _stats.to_dict(),
    }


def get_call_stats() -> Dict[str, Any]:
    """获取调用统计"""
    return _stats.to_dict()


# ═══════════════════════════════════════════════════════════════
#  模块级调用 — 带智能回退
# ═══════════════════════════════════════════════════════════════

# 模块 System Prompt 注册表
_MODULE_PROMPTS: Dict[str, str] = {
    "NeuralMemory": "你是NeuralMemory三层神经记忆系统的AI助手，擅长记忆编码、语义分析和记忆关联。你需要帮助理解和组织各类记忆信息，提取关键概念并建立关联。",
    "RefuteCore": "你是RefuteCore论证分析引擎，擅长从8个维度检验论证的有效性：逻辑、证据、假设、反面、类比、权威、因果、价值。你需要严谨地分析论证结构，识别谬误，给出强度评估。",
    "PanWisdom": "你融合了42个学派的智慧，包括儒家、道家、墨家、法家、名家、兵家等中国哲学学派，以及西方哲学、现代科学各学科。请结合相关学派的智慧来分析问题。",
    "DivineReason": "你是DivineReason深度推理引擎，支持三层推理深度：Light(表层模式匹配)、Standard(深度假设探索)、Deep(极致元认知审视)。请根据指定深度进行推理分析。",
    "TianShu": "你是天枢TianShu八层智慧处理管道的分析引擎，负责自然语言理解、需求分类、分流决策和结果优化。",
    "TrackA": "你是神政轨(TrackA)监管助手，负责监管调度过程、验证决策合规性、记录执行轨迹、保障系统稳定性。",
    "TrackB": "你是神行轨(TrackB)执行助手，负责执行具体任务、调用Claw贤者完成工作、管理任务状态、协调部门协作。",
    "DomainNexus": "你是DomainNexus知识库助手，擅长从多个知识域中检索和整合信息，分析查询意图，建立跨领域知识关联。",
    "SageDispatch": "你是SageDispatch智能调度助手，负责分析问题并选择最优处理路径，将问题分配给最合适的调度器处理。",
    "OutputEngine": "你是内容生成引擎，擅长将分析结果转化为清晰、结构化的输出内容，支持多种格式。",
}

# ==================== v7.1 LLM 调用缓存 ====================
# 相同 module_name+prompt 组合2分钟内直接返回（减少重复LLM调用）
_LLM_CALL_CACHE: Dict[str, Tuple[float, str]] = {}
_LLM_CACHE_MAX = 32
_LLM_CACHE_TTL = 120  # 2分钟
_LLM_CACHE_LOCK = threading.Lock()


def _llm_cache_get(module_name: str, prompt: str) -> Optional[str]:
    """获取LLM调用缓存"""
    cache_key = hashlib.md5(f"{module_name}:{prompt}".encode('utf-8')).hexdigest()
    with _LLM_CACHE_LOCK:
        entry = _LLM_CALL_CACHE.get(cache_key)
        if entry is None:
            return None
        ts, result = entry
        if time.time() - ts > _LLM_CACHE_TTL:
            del _LLM_CALL_CACHE[cache_key]
            return None
        return result


def _llm_cache_put(module_name: str, prompt: str, result: str):
    """存入LLM调用缓存"""
    cache_key = hashlib.md5(f"{module_name}:{prompt}".encode('utf-8')).hexdigest()
    with _LLM_CACHE_LOCK:
        if len(_LLM_CALL_CACHE) >= _LLM_CACHE_MAX:
            # 淘汰最旧的25%
            sorted_keys = sorted(_LLM_CALL_CACHE.keys(), key=lambda k: _LLM_CALL_CACHE[k][0])
            for k in sorted_keys[:max(1, len(sorted_keys) // 4)]:
                del _LLM_CALL_CACHE[k]
        _LLM_CALL_CACHE[cache_key] = (time.time(), result)


def call_module_llm(
    module_name: str,
    prompt: str,
    system_prompt: str = None,
    fallback_func: Optional[Callable] = None,
    **kwargs,
) -> str:
    """
    模块级 LLM 调用 — 带智能回退

    Args:
        module_name: 模块名称（用于选择system prompt和日志）
        prompt: 用户提示
        system_prompt: 自定义系统提示（覆盖默认）
        fallback_func: 自定义回退函数（覆盖默认）

    Returns:
        处理结果字符串（始终返回 str）
    """
    # v7.1: LLM调用缓存检查
    cached = _llm_cache_get(module_name, prompt)
    if cached is not None:
        return cached
    
    # 获取模块专属 system prompt
    sp = system_prompt or _MODULE_PROMPTS.get(module_name, "你是Somn智能系统的助手。")

    # 调用 LLM
    response = llm_chat(prompt=prompt, system_prompt=sp, **kwargs)

    # 如果 LLM 不可用，使用回退
    if response.source == LLMSource.FALLBACK:
        if fallback_func is not None:
            try:
                result = fallback_func(prompt, **kwargs)
                # 确保返回值始终转为 str
                final = str(result) if result is not None else ""
                _llm_cache_put(module_name, prompt, final)
                return final
            except Exception as e:
                logger.error(f"[{module_name}] 回退函数也失败: {e}")
                _llm_cache_put(module_name, prompt, response.content)
                return response.content
        _llm_cache_put(module_name, prompt, response.content)
        return response.content

    _llm_cache_put(module_name, prompt, response.content)
    return response.content


# ═══════════════════════════════════════════════════════════════
#  规则回退引擎 — 真实本地分析能力 v7.1
# ═══════════════════════════════════════════════════════════════

# 预编译正则
_RE_KEYWORDS = re.compile(r'[\u4e00-\u9fa5]{2,4}')
_RE_SENTENCE = re.compile(r'[。！？\n]+')
_RE_NUMBER = re.compile(r'\d+\.?\d*')

# 领域识别关键词
_DOMAIN_PATTERNS = {
    "business": {
        "keywords": ["商业", "营销", "销售", "利润", "市场", "客户", "品牌", "运营", "战略", "投资", "融资", "股权", "估值", "商业模式", "增长", "转化", "用户增长", "GMV", "收入", "成本", "预算", "定价"],
        "weight": 1.0,
    },
    "technology": {
        "keywords": ["代码", "编程", "开发", "系统", "架构", "算法", "数据", "数据库", "API", "服务器", "性能", "安全", "测试", "部署", "DevOps", "云", "AI", "机器学习", "模型", "接口", "协议"],
        "weight": 1.0,
    },
    "academic": {
        "keywords": ["研究", "理论", "论文", "学术", "科学", "实验", "假设", "验证",
                       "方法论", "文献", "综述", "结论", "样本", "显著性", "相关性", "因果", "变量"],
        "weight": 1.0,
        # 学术独有关键词（不与 technology 重叠），匹配时额外加分
        "unique_keywords": ["论文", "学术", "文献", "综述", "方法论", "显著性", "样本"],
        "unique_weight": 0.5,
    },
    "philosophy": {
        "keywords": ["哲学", "智慧", "思想", "道德", "伦理", "存在", "认识", "价值", "意义", "人生", "世界", "知识", "真理", "信仰", "理性", "感性", "灵魂", "意识", "自我"],
        "weight": 1.0,
    },
    "daily": {
        "keywords": ["生活", "健康", "饮食", "运动", "休息", "心情", "情感", "家庭", "朋友", "旅游", "购物", "娱乐", "学习", "工作", "通勤", "日程", "习惯", "爱好"],
        "weight": 0.8,
    },
}


def _extract_domain(text: str) -> str:
    """
    识别问题所属领域

    Returns:
        领域标签: "business" | "technology" | "academic" | "philosophy" | "daily" | "general"
    """
    text_lower = text.lower()
    scores: Dict[str, float] = {}

    for domain, config in _DOMAIN_PATTERNS.items():
        score = 0.0
        for kw in config["keywords"]:
            if kw in text_lower:
                score += config["weight"]
        # v7.2: 独有关键词加分，解决领域交叉问题
        unique_keywords = config.get("unique_keywords", [])
        unique_weight = config.get("unique_weight", 0.5)
        for uk in unique_keywords:
            if uk in text_lower:
                score += unique_weight
        if score > 0:
            scores[domain] = score

    if not scores:
        return "general"

    # 返回得分最高的领域
    return max(scores, key=scores.get)  # type: ignore


def _extract_module_role(system_prompt: str) -> Tuple[str, str]:
    """
    从 system_prompt 提取模块角色信息

    Returns:
        (role_name, role_description)
        例如: ("神行轨执行助手", "负责执行具体任务...")
    """
    if not system_prompt:
        return ("通用助手", "提供综合性帮助")

    # 尝试提取"你是XXX"模式
    match = re.search(r'你是([^\n，,。]+?)(?:[，,。]|$)', system_prompt)
    if match:
        role_name = match.group(1).strip()
        # 提取第一句话作为描述
        desc_match = re.search(r'[，,。]([^。]+)', system_prompt)
        role_desc = desc_match.group(1).strip() if desc_match else ""
        return (role_name, role_desc)

    # 尝试提取模块名（如 NeuralMemory, RefuteCore）
    for module in _MODULE_PROMPTS.keys():
        if module in system_prompt or module in (system_prompt or ""):
            default = _MODULE_PROMPTS.get(module, "")
            match2 = re.search(r'你是([^\n，,。]+)', default)
            if match2:
                return (match2.group(1), f"模块{module}的助手")
            return (module, "")

    return ("Somn助手", "提供综合性帮助")


def _build_role_prefix(system_prompt: str, domain: str) -> str:
    """
    根据 system_prompt 和领域构建角色化前缀

    Returns:
        角色化前缀文本
    """
    role_name, role_desc = _extract_module_role(system_prompt)

    # 领域对应的中文标签
    domain_labels = {
        "business": "商业分析",
        "technology": "技术分析",
        "academic": "学术研究",
        "philosophy": "哲学思考",
        "daily": "生活建议",
        "general": "综合分析",
    }
    domain_label = domain_labels.get(domain, "综合分析")

    # 根据角色生成前缀
    if role_name == "Somn助手":
        return f"作为 Somn 智能助手，我对这个问题进行{domain_label}：\n\n"
    else:
        return f"作为 {role_name}，我从{domain_label}角度提供分析：\n\n"


def fallback_process(prompt: str, system_prompt: str = "") -> str:
    """
    规则回退引擎 v7.1 — 提供基础分析能力

    当所有 LLM 不可用时，使用规则引擎提供有意义的分析。
    能力包括：
    1. 关键词提取
    2. 问题分类
    3. 领域识别（商业/技术/学术/哲学/日常）
    4. 基于 system_prompt 的角色化响应
    5. 基于模板的响应生成
    """
    # 提取关键词
    keywords = _RE_KEYWORDS.findall(prompt)
    stopwords = {'如何', '怎么', '什么', '为什么', '这个', '那个', '可以', '需要', '进行', '通过', '以及', '关于', '对于', '请问', '帮忙', '一下'}
    keywords = [k for k in keywords if k not in stopwords]
    keywords = keywords[:8]

    # 提取数字
    numbers = _RE_NUMBER.findall(prompt)

    # 问题分类
    question_type = _classify_question(prompt)

    # 领域识别
    domain = _extract_domain(prompt)

    # 构建角色化前缀
    role_prefix = _build_role_prefix(system_prompt, domain)

    # 基于分类 + 领域 + system_prompt 生成响应
    if question_type == "how":
        response = _generate_how_response(keywords, prompt, system_prompt, domain)
    elif question_type == "why":
        response = _generate_why_response(keywords, prompt, system_prompt, domain)
    elif question_type == "what":
        response = _generate_what_response(keywords, prompt, system_prompt, domain)
    elif question_type == "compare":
        response = _generate_compare_response(keywords, prompt, system_prompt, domain)
    elif question_type == "analyze":
        response = _generate_analyze_response(keywords, prompt, system_prompt, domain)
    else:
        response = _generate_general_response(keywords, prompt, system_prompt, domain)

    # 添加角色前缀
    response = role_prefix + response

    # 添加LLM不可用提示
    footer = "\n\n---\n⚠️ [规则引擎分析 — LLM服务暂不可用，如需更深入分析请等待LLM服务恢复]"
    return response + footer


def _classify_question(text: str) -> str:
    """问题分类"""
    if any(k in text for k in ['如何', '怎么', '怎样', '方法', '步骤', '怎么做']):
        return "how"
    if any(k in text for k in ['为什么', '原因', '导致', '因素', '动机']):
        return "why"
    if any(k in text for k in ['是什么', '什么是', '定义', '概念', '解释']):
        return "what"
    if any(k in text for k in ['对比', '比较', '区别', '差异', 'vs', '优劣']):
        return "compare"
    if any(k in text for k in ['分析', '评估', '判断', '诊断', '检验']):
        return "analyze"
    return "general"


def _generate_how_response(keywords: List[str], prompt: str, system_prompt: str = "", domain: str = "general") -> str:
    """如何类响应 — 角色化 + 领域定制"""
    if not keywords:
        return "请提供更具体的问题描述，以便给出有针对性的建议。"

    topic = keywords[0] if keywords else "该问题"

    # 领域定制化步骤
    domain_steps = {
        "business": [
            ("市场调研", f"了解{topic}相关的市场需求和竞争格局"),
            ("商业模式设计", "设计可盈利的运营模式"),
            ("执行计划", "制定具体的实施路线图和时间节点"),
        ],
        "technology": [
            ("技术选型", f"评估{topic}相关的技术栈和工具"),
            ("架构设计", "设计可扩展的技术架构"),
            ("开发计划", "制定开发里程碑和迭代计划"),
        ],
        "academic": [
            ("文献梳理", f"调研{topic}相关的学术前沿和现有研究"),
            ("研究设计", "制定研究方法和实验方案"),
            ("验证计划", "设计验证假设的具体步骤"),
        ],
        "philosophy": [
            ("概念澄清", f"深入理解{topic}的本质和内涵"),
            ("多视角分析", "从不同哲学流派审视问题"),
            ("实践指引", "将哲学思考转化为行动指南"),
        ],
        "daily": [
            ("现状评估", f"了解当前{topic}的实际状况"),
            ("目标设定", "设定切实可行的小目标"),
            ("行动方案", "制定简单易行的日常实践计划"),
        ],
        "general": [
            ("现状诊断", f"明确当前{topic}的基线状态"),
            ("目标设定", "设定可量化的目标"),
            ("方案设计", "设计至少3种备选方案"),
        ],
    }

    steps = domain_steps.get(domain, domain_steps["general"])

    # system_prompt 角色定制
    role_name, _ = _extract_module_role(system_prompt)

    steps_md = "\n".join([
        f"**步骤{i+1}：{s[0]}**\n- {s[1]}"
        for i, s in enumerate(steps)
    ])

    tip = {
        "business": "💡 建议：从市场需求出发，先做最小可行产品验证。",
        "technology": "💡 建议：优先保证系统稳定性，再考虑性能优化。",
        "academic": "💡 建议：从文献综述开始，确保站在巨人肩膀上。",
        "philosophy": "💡 建议：深入思考本质，避免流于表面。",
        "daily": "💡 建议：从微小的改变开始，循序渐进。",
        "general": "💡 建议：先做最小可行验证，再逐步扩大。",
    }.get(domain, "")

    return f"""关于「{topic}」的实施建议：

{steps_md}

**步骤四：快速验证**
- 选择投入产出比最高的方案优先执行
- 小规模测试，收集反馈

**步骤五：迭代优化**
- 根据测试结果调整方案
- 扩大实施范围

{tip}"""


def _generate_why_response(keywords: List[str], prompt: str, system_prompt: str = "", domain: str = "general") -> str:
    """为什么类响应 — 角色化 + 领域定制"""
    if not keywords:
        return "请提供更具体的问题背景，以便进行原因分析。"

    topic = keywords[0]

    # 领域定制化原因分析
    domain_causes = {
        "business": [
            ("市场因素", "需求变化、竞争加剧、市场饱和"),
            ("运营因素", "流程效率、成本控制、团队执行"),
            ("战略因素", "定位偏差、创新不足、资本运作"),
        ],
        "technology": [
            ("技术债", "代码质量、架构腐化、技术选型失误"),
            ("工程实践", "测试不足、部署流程、监控缺失"),
            ("人员因素", "技能不足、沟通不畅、知识断层"),
        ],
        "academic": [
            ("理论局限", "前提假设过强、适用范围有限"),
            ("研究方法", "样本偏差、测量误差、设计缺陷"),
            ("外部因素", "资源限制、时间压力、发表偏见"),
        ],
        "philosophy": [
            ("认识论根源", "思维定式、认知偏差、价值观差异"),
            ("实践困境", "知行不一、环境制约、利益冲突"),
            ("本体论问题", "概念模糊、定义不清、边界不明"),
        ],
        "daily": [
            ("习惯因素", "固有习惯、舒适区依赖、意志力消耗"),
            ("环境因素", "时间压力、资源限制、外部干扰"),
            ("心理因素", "动机不足、恐惧焦虑、完美主义"),
        ],
        "general": [
            ("内部因素", "资源配置、流程瓶颈、团队能力"),
            ("外部因素", "市场环境、竞争对手、政策变化"),
            ("系统性因素", "结构问题、历史累积、反馈失灵"),
        ],
    }

    causes = domain_causes.get(domain, domain_causes["general"])
    causes_md = "\n\n".join([
        f"{i+1}. **{s[0]}**\n   - {s[1]}"
        for i, s in enumerate(causes)
    ])

    return f"""关于「{topic}」的原因分析：

**可能原因（多维度分析）：**

{causes_md}

**建议下一步：**
- 收集数据验证以上假设
- 从最可能的原因入手排查
- 关注相关指标：{', '.join(keywords[:4])}"""


def _generate_what_response(keywords: List[str], prompt: str, system_prompt: str = "", domain: str = "general") -> str:
    """是什么类响应 — 角色化 + 领域定制"""
    if not keywords:
        return "请提供更具体的查询内容。"

    topic = keywords[0]

    # 领域定制化定义
    domain_defs = {
        "business": f"「{topic}」是商业领域中的核心概念，涉及市场、客户、价值创造等要素。",
        "technology": f"「{topic}」是技术领域中的重要概念，涉及系统、数据、算法等要素。",
        "academic": f"「{topic}」是学术研究中的核心概念，具有明确的定义域和方法论。",
        "philosophy": f"「{topic}」是哲学思考中的重要命题，涉及存在、认识、价值等维度。",
        "daily": f"「{topic}」是日常生活中的重要议题，与个人习惯和幸福感密切相关。",
        "general": f"「{topic}」是一个值得深入探讨的概念。",
    }

    definition = domain_defs.get(domain, domain_defs["general"])
    related = ', '.join(keywords[1:4]) if len(keywords) > 1 else '相关领域'

    return f"""**{topic}** 的核心概念：

{definition}

**核心要点：**
- 定义：{topic}指代的是该领域中的核心机制或方法论
- 作用：帮助解决实际问题，提升效率和质量
- 关联：与{related}密切相关

💡 更详细的分析需要接入LLM服务。"""


def _generate_compare_response(keywords: List[str], prompt: str, system_prompt: str = "", domain: str = "general") -> str:
    """对比类响应 — 角色化 + 领域定制"""
    if len(keywords) < 2:
        return "请提供需要对比的至少两个对象。"

    a, b = keywords[0], keywords[1]

    # 领域定制化对比维度
    domain_dims = {
        "business": [("商业模式", "盈利方式", "抗风险能力"), ("市场规模", "增长潜力", "市场份额"), ("团队能力", "执行效率", "创新能力")],
        "technology": [("性能", "速度/吞吐", "延迟/并发"), ("稳定性", "可用性", "容错性"), ("维护性", "可扩展性", "开发效率")],
        "academic": [("理论深度", "解释力", "预测力"), ("研究方法", "严谨性", "可重复性"), ("创新性", "突破性", "影响力")],
        "philosophy": [("思想深度", "逻辑严密", "自洽性"), ("实践价值", "指导意义", "现实关怀"), ("创新性", "独特视角", "启发性")],
        "daily": [("便利性", "易获取", "操作复杂度"), ("成本", "金钱", "时间精力"), ("效果", "即时反馈", "长期收益")],
        "general": [("适用场景", "特定场景适配度", "灵活性"), ("优势", "核心竞争力", "独特价值"), ("劣势", "局限范围", "潜在风险")],
    }

    dims = domain_dims.get(domain, domain_dims["general"])

    header = "| 维度 | " + a + " | " + b + " |"
    separator = "|------|" + "-" * (len(a) + 1) + "|" + "-" * (len(b) + 1) + "|"
    rows = []
    for dim_name, a_val, b_val in dims:
        rows.append(f"| {dim_name} | {a_val} | {b_val} |")

    table = "\n".join([header, separator] + rows)

    return f"""**对比分析：{a} vs {b}**

| 维度 | {a} | {b} |
|------|-----|-----|
""" + "\n".join([f"| {d[0]} | {d[1]} | {d[2]} |" for d in dims]) + f"""

💡 完整的对比分析需要接入LLM服务获取更深入的分析。"""


def _generate_analyze_response(keywords: List[str], prompt: str, system_prompt: str = "", domain: str = "general") -> str:
    """分析类响应 — 角色化 + 领域定制"""
    if not keywords:
        return "请提供需要分析的具体内容。"

    topic = ", ".join(keywords[:3])

    # 领域定制化分析框架
    domain_frameworks = {
        "business": ("市场分析", ["宏观环境(PEST)", "行业竞争(波特五力)", "自身资源能力"], ["SWOT分析", "商业画布", "价值链分析"]),
        "technology": ("技术分析", ["功能需求", "非功能需求", "约束条件"], ["架构评审", "代码审查", "性能测试"]),
        "academic": ("学术分析", ["文献综述", "理论框架", "研究方法"], ["假设检验", "数据分析", "结论验证"]),
        "philosophy": ("哲学分析", ["概念澄清", "前提反思", "论证重构"], ["多视角审视", "思想实验", "实践检验"]),
        "daily": ("生活分析", ["现状评估", "目标设定", "障碍识别"], ["微习惯养成", "环境设计", "正向激励"]),
        "general": ("综合分析", ["现状概览", "多维度因素", "关联分析"], ["假设验证", "方案设计", "行动计划"]),
    }

    framework = domain_frameworks.get(domain, domain_frameworks["general"])

    return f"""**分析报告：{topic}**

**1. {framework[0]}**
- 涉及领域：{', '.join(keywords[:5])}
- 分析框架：{' / '.join(framework[1])}

**2. 分析步骤**
1. {' → '.join(framework[1])}
2. {' → '.join(framework[2])}

**3. 建议行动**
1. 收集相关数据和案例
2. 进行结构化分析
3. 制定可执行的行动方案

💡 接入LLM服务后可获得更深入的分析结果。"""


def _generate_general_response(keywords: List[str], prompt: str, system_prompt: str = "", domain: str = "general") -> str:
    """通用响应 — 角色化 + 领域定制"""
    if not keywords:
        return "请提供更具体的输入，以便给出有针对性的回答。"

    topic = ", ".join(keywords[:5])

    suggestions = {
        "business": ["**明确商业目标** — 确定核心KPI", f"**市场调研** — 了解{keywords[0]}相关的市场机会", "**竞品分析** — 对比不同路径的优劣", "**快速验证** — 小规模测试MVP"],
        "technology": ["**需求澄清** — 明确功能边界", f"**技术调研** — 了解{keywords[0]}相关的技术方案", "**架构设计** — 评估扩展性和风险", "**迭代开发** — 敏捷交付核心功能"],
        "academic": ["**文献检索** — 了解研究现状", f"**概念界定** — 明确{keywords[0]}的定义", "**方法选择** — 选取合适的研究方法", "**数据分析** — 验证假设或理论"],
        "philosophy": ["**概念澄清** — 厘清核心内涵", f"**多视角思考** — 从{keywords[0]}的不同维度审视", "**论证评估** — 检验逻辑自洽性", "**实践联系** — 思考现实意义"],
        "daily": ["**现状记录** — 了解当前状态", f"**目标分解** — 设定{keywords[0]}相关的小目标", "**习惯设计** — 建立简单易行的行动", "**持续追踪** — 记录并调整"],
        "general": ["**明确核心需求** — 确定最重要的目标", f"**收集信息** — 了解{keywords[0]}相关的背景", "**分析方案** — 对比不同路径的优劣", "**执行验证** — 快速测试并迭代"],
    }

    steps = suggestions.get(domain, suggestions["general"])

    return f"""关于「{topic}」的分析：

这是一个涉及多个维度的综合性问题。建议：

1. {steps[0]}
2. {steps[1]}
3. {steps[2]}
4. {steps[3]}

💡 接入LLM服务可获得更精准的分析。"""


# ═══════════════════════════════════════════════════════════════
#  网络搜索增强 — LLM + 网络协同 v7.1
# ═══════════════════════════════════════════════════════════════

# 搜索结果相关性过滤阈值
_MIN_RELEVANCE_SCORE = 0.1


def _calculate_relevance(query: str, result: Dict[str, Any]) -> float:
    """
    计算搜索结果与查询的相关性得分

    Returns:
        0.0 ~ 1.0 的相关性得分
    """
    query_lower = query.lower()
    # 提取查询关键词
    query_keywords = _RE_KEYWORDS.findall(query)
    query_keywords = [k.lower() for k in query_keywords if len(k) >= 2]

    if not query_keywords:
        return 0.0  # 无关键词时无法判断相关性

    score = 0.0
    title = (result.get("title") or "").lower()
    snippet = (result.get("snippet") or "").lower()
    url = (result.get("url") or "").lower()

    combined = title + " " + snippet + " " + url

    for kw in query_keywords:
        if kw in combined:
            # 标题中命中权重更高
            if kw in title:
                score += 0.4
            elif kw in snippet:
                score += 0.2
            elif kw in url:
                score += 0.1

    # 归一化（最多5个关键词）
    score = min(score / min(len(query_keywords), 5), 1.0)
    return score


def _filter_relevant_results(query: str, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    过滤搜索结果，只保留相关性 > 阈值的条目

    Returns:
        过滤后的结果列表
    """
    filtered = []
    for r in results:
        score = _calculate_relevance(query, r)
        r["_relevance_score"] = round(score, 2)
        if score >= _MIN_RELEVANCE_SCORE:
            filtered.append(r)

    # 按相关性排序
    filtered.sort(key=lambda x: x["_relevance_score"], reverse=True)
    return filtered


def _format_citation(index: int, result: Dict[str, Any], relevance: float) -> str:
    """
    格式化单个搜索结果的引用标注

    Returns:
        引用格式: [1] 标题 (相关度: 0.85)
    """
    title = result.get("title", "未知来源")
    # 截断过长的标题
    if len(title) > 30:
        title = title[:27] + "..."
    return f"[{index}] {title} (相关度: {relevance:.0%})"


def llm_with_web_search(
    query: str,
    module_name: str = "TianShu",
    system_prompt: str = None,
    max_search_results: int = 3,
) -> Dict[str, Any]:
    """
    LLM + 网络搜索协同分析 v7.1

    流程:
    1. 判断是否需要网络搜索
    2. 执行网络搜索
    3. 相关性过滤（v7.1 新增）
    4. 将过滤后的搜索结果注入 LLM prompt（含引用标注 v7.1）
    5. LLM 生成增强回答

    Returns:
        {
            "answer": str,
            "web_results": list,          # 过滤后的结果
            "all_results": list,         # 原始全部结果（v7.1 新增）
            "llm_source": str,            # cloud / local / fallback
            "used_web": bool,
            "filter_stats": dict,         # 过滤统计（v7.1 新增）
        }
    """
    # 判断是否需要搜索
    web_results = []
    all_results = []
    used_web = False
    filter_stats = {"total": 0, "filtered": 0, "threshold": _MIN_RELEVANCE_SCORE}

    try:
        from .web_integration import should_trigger_web_search, search_with_fallback

        should_search, trigger = should_trigger_web_search(query)
        if should_search:
            search_resp = search_with_fallback(query, max_results=max_search_results)
            if search_resp.get("success") and search_resp.get("results"):
                all_results = search_resp["results"]
                filter_stats["total"] = len(all_results)

                # v7.1: 相关性过滤
                web_results = _filter_relevant_results(query, all_results)
                filter_stats["filtered"] = len(web_results)

                used_web = len(web_results) > 0
    except Exception as e:
        logger.debug(f"[LLM-RuleLayer] 网络搜索检查失败: {e}")

    # 构建 prompt
    enhanced_prompt = query
    citations = []

    if used_web and web_results:
        # v7.1: 添加引用标注
        web_context_lines = []
        for i, r in enumerate(web_results, 1):
            relevance = r.get("_relevance_score", 0.5)
            citation = _format_citation(i, r, relevance)
            citations.append(citation)

            # 拼接 snippet
            snippet = r.get("snippet", "")
            title = r.get("title", "")
            url = r.get("url", "")

            web_context_lines.append(
                f"{citation}\n标题: {title}\n摘要: {snippet}\n来源: {url}\n"
            )

        web_context = "\n---\n".join(web_context_lines)

        # v7.1: 引用标注格式改进
        citation_list = " | ".join(citations)

        enhanced_prompt = f"""请综合以下搜索结果回答问题。搜索结果已按相关性排序：

{citation_list}

---
详细信息：
{web_context}

---
用户问题：{query}

请基于以上信息给出回答，并在回答中适当引用来源。"""

    # 调用 LLM
    answer = call_module_llm(module_name, enhanced_prompt, system_prompt)

    # v7.2: 改进 llm_source 判断逻辑 — 基于实际调用结果而非静态状态
    llm_source = "fallback"
    # 检查 answer 是否包含规则回退的特征文本
    if "⚠️ [规则引擎分析" not in answer:
        # answer 不包含回退标记 → LLM 成功调用了
        _init_llm_service()
        if _llm_service is not None:
            llm_source = "cloud"
        elif _local_engine is not None:
            llm_source = "local"
        else:
            llm_source = "fallback"  # 无规则回退标记但 LLM 也不可用 → 可能是自定义 fallback

    return {
        "answer": answer,
        "web_results": web_results,        # 过滤后相关结果
        "all_results": all_results,        # 原始全部结果
        "llm_source": llm_source,
        "used_web": used_web,
        "filter_stats": filter_stats,      # 过滤统计
    }


# ═══════════════════════════════════════════════════════════════
#  导出
# ═══════════════════════════════════════════════════════════════

__all__ = [
    # 核心接口
    "llm_chat",
    "llm_analyze",
    "llm_with_web_search",
    "call_module_llm",
    "get_llm_status",
    "get_call_stats",

    # 数据类型
    "LLMResponse",
    "LLMSource",
    "LLMCallStats",

    # 配置
    "_MODULE_PROMPTS",
]
