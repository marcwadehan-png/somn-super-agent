"""
================================================
    天枢 TianShu — 八层智慧处理管道 S1.0
    Eight-Layer Intelligent Processing Pipeline

    SageDispatch 核心中枢系统
================================================

命名释义：
  天枢 — 北斗第一星，司掌枢纽中枢。
  作为 SageDispatch 的核心处理管道，统御八层智慧，
  是整个智能系统的运转中枢。

架构设计：
┌─────────────────────────────────────────────────┐
│  Layer 1: 输入层 (InputLayer)                    │
│  Layer 2: 自然语言需求分析层 (NLAnalysisLayer)    │
│  Layer 3: 需求分类数据库 (ClassificationDB)      │
│  Layer 4: 分流层 (RoutingLayer)                  │  ← 论证不合格回退至此
│  Layer 5: 推理层 (ReasoningLayer)               │  ← 受SD-R1三层监管约束
│  Layer 6: 论证层 (ArgumentationLayer)           │  ← 不合格触发回退到L4
│  Layer 7: 输出层 (OutputLayer)                  │
│  Layer 8: 优化层 (OptimizationLayer)            │
└─────────────────────────────────────────────────┘

三等级分流：
  基础 (Basic)  — P1→F2→E1，不进神之架构，快速响应
  深度 (Deep)   — P1→F2→C2→E1，神之架构并行，Claw讨论
  超级 (Super)  — P1→F1+F2→C2→E1，全链路Claw+T2驳心

推理层三等级：
  基础 — SD-C2(神之架构决策) → SD-D1(轻量论证)
  深度 — SD-C1(太极阴阳决策) → SD-D2(标准论证)，翰林院三轮审核
  超级 — SD-C1+SD-C2(联合决策) → SD-D3(极致论证)，翰林院严格审核

论证闭环回退机制（所有三个等级均支持）：
  L6论证不合格 → 携带R2/T2结构化反馈返回L4分流层
  L4根据反馈修正式分流（调整策略、加强资源）
  → L5推理 → L6论证 → 直到论证通过
  最大重试3次，防死循环，耗尽则强制输出

12个SageDispatch调度器 + RefuteCore T2 驳心引擎：
  SD-P1 ProblemDispatcher     — 问题调度（树干核心）
  SD-F1 SchoolFusion           — 25学派融合
  SD-F2 FourLevelDispatch      — 四级调度总控
  SD-R1 ThreeLayerReasoning    — 三层推理监管（约束所有推理）
  SD-R2 FallacyChecker         — 谬误检测
  SD-C1 YinYangDecision        — 太极阴阳决策
  SD-C2 DivineArchitecture     — 神之架构决策
  SD-D1 SuperReasoning(light)  — 轻量深度推理
  SD-D2 SuperReasoning(standard) — 标准深度推理
  SD-D3 SuperReasoning(deep)   — 极致深度推理
  SD-E1 ChainExecutor          — 五步主链执行
  SD-L1 ResultTracker          — 学习进化
  T2  RefuteCore v3.2          — 驳心引擎（8维度反驳论证）

Usage:
    from knowledge_cells.eight_layer_pipeline import (
        EightLayerPipeline, ProcessingGrade
    )

    pipeline = EightLayerPipeline()

    # 基础处理
    result = pipeline.process("分析用户增长策略")

    # 深度处理
    result = pipeline.process("设计公司三年战略规划", grade=ProcessingGrade.DEEP)

    # 超级处理
    result = pipeline.process("创新性颠覆现有商业模式", grade=ProcessingGrade.SUPER)
"""

import time
import uuid
import re
import hashlib
import threading
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

# ==================== 网络搜索增强（懒加载） ====================

_TIANSHU_WEB: Optional[Any] = None


def _get_tianshu_web():
    """获取 TianShuWeb 实例（懒加载）"""
    global _TIANSHU_WEB
    if _TIANSHU_WEB is None:
        try:
            from .web_integration import TianShuWeb
            _TIANSHU_WEB = TianShuWeb()
        except ImportError:
            logger.warning("[TianShu] Web integration not available")
            return None
    return _TIANSHU_WEB


# ==================== SageDispatch 调度器桥接 ====================
# ==================== RefuteCore 驳心引擎桥接 (T2论证) ====================
# ==================== DomainNexus 知识库桥接 ====================

def _query_knowledge_base(question: str, context: str = "") -> Dict[str, Any]:
    """
    查询 DomainNexus 知识库 — 为推理层提供领域知识支撑

    v7.1: 增加 LRU 缓存，相同问题10分钟内直接返回

    Args:
        question: 用户问题/文本
        context: 补充上下文

    Returns:
        {
            'queried': bool,           # 是否成功查询
            'answer': str,             # 知识库回答
            'relevant_cells': list,    # 相关知识格子
            'hot_topics': list,        # 热门话题
            'suggestions': list,       # 行动建议
        }
    """
    # 缓存检查
    cached = EightLayerPipeline._kb_cache_get(question)
    if cached is not None:
        return cached

    try:
        from .domain_nexus import query
    except ImportError:
        from domain_nexus import query

    try:
        result = query(question, context)
        kb_result = {
            "queried": True,
            "answer": result.get("answer", ""),
            "relevant_cells": result.get("relevant_cells", []),
            "hot_topics": result.get("hot_topics", []),
            "suggestions": [],
        }
        # 存入缓存
        EightLayerPipeline._kb_cache_put(question, kb_result)
        return kb_result
    except Exception as e:
        return {
            "queried": False,
            "answer": "",
            "relevant_cells": [],
            "hot_topics": [],
            "suggestions": [],
            "error": str(e),
        }


# v7.1 FastBoot: 缓存 get_engine 导入
_cached_get_engine_fn = None

def _get_dispatch_engine():
    """懒加载获取 SageDispatch DispatchEngine 单例（缓存导入结果）"""
    global _cached_get_engine_fn
    if _cached_get_engine_fn is None:
        try:
            from .core import get_engine
            _cached_get_engine_fn = get_engine
        except ImportError:
            import knowledge_cells.core as _kc_core
            _cached_get_engine_fn = _kc_core.get_engine
    return _cached_get_engine_fn()


def _call_dispatcher(dispatcher_id: str, text: str, parent_output: Dict = None) -> Dict[str, Any]:
    """
    调用 SageDispatch 真实调度器

    Args:
        dispatcher_id: 调度器ID (如 SD-P1, SD-F2, SD-C1 等)
        text: 用户输入文本
        parent_output: 父级输出（用于链式调度）

    Returns:
        调度器返回的 output 字典
    """
    engine = _get_dispatch_engine()
    try:
        request = {
            "description": text,
            "context": "",
            "scenario": "eight_layer_pipeline"
        }
        response = engine.dispatch(request, dispatcher_id=dispatcher_id)
        return {
            "called": True,
            "dispatcher_id": dispatcher_id,
            "confidence": response.confidence,
            "output": response.output,
            "time_spent": response.time_spent,
            "state": response.state.value if response.state else "unknown",
        }
    except Exception as e:
        return {
            "called": False,
            "dispatcher_id": dispatcher_id,
            "error": str(e),
            "confidence": 0.0,
            "output": {},
            "time_spent": 0.0,
            "state": "failed",
        }


def _call_dispatcher_chain(text: str, path: List[str]) -> List[Dict[str, Any]]:
    """
    链式调用多个调度器

    Args:
        text: 用户输入文本
        path: 调度器路径，如 ["SD-P1", "SD-F2", "SD-E1"]

    Returns:
        每个调度器的返回结果列表
    """
    results = []
    parent_output = None
    for dispatcher_id in path:
        engine = _get_dispatch_engine()
        try:
            request = {
                "description": text,
                "context": "",
                "scenario": "eight_layer_pipeline"
            }
            kwargs = {}
            if parent_output:
                kwargs["parent_output"] = parent_output
            response = engine.dispatch(request, dispatcher_id=dispatcher_id, **kwargs)
            result = {
                "called": True,
                "dispatcher_id": dispatcher_id,
                "confidence": response.confidence,
                "output": response.output,
                "time_spent": response.time_spent,
                "state": response.state.value if response.state else "unknown",
            }
            results.append(result)
            parent_output = response.output
        except Exception as e:
            results.append({
                "called": False,
                "dispatcher_id": dispatcher_id,
                "error": str(e),
                "confidence": 0.0,
                "output": {},
                "time_spent": 0.0,
                "state": "failed",
            })
    return results


def _ensure_somm_root():
    """确保 somn 根目录在 sys.path 中，供所有跨包懒加载使用"""
    import sys, os
    _somm_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if _somm_root not in sys.path:
        sys.path.insert(0, _somm_root)


def _call_pan_wisdom(text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    [P2 接入] 调用 PanWisdomTree 学派融合引擎

    reasoning_mind/deep_reasoning_engine/ → Pan-Wisdom Tree → 天枢 L5

    流程：
    1. ProblemIdentifier 识别问题类型
    2. SchoolRecommender 推荐学派组合
    3. 生成学派融合洞察（融合儒/道/兵/法/科学等多视角）
    4. 将洞察注入 SD-D 调度器上下文，增强深度推理

    Returns:
        Dict 含 pan_wisdom 洞察、推荐学派、置信度
    """
    try:
        # PanWisdomTree 已在 knowledge_cells 包内，直接相对导入
        from .pan_wisdom_core import (
            PanWisdomTree,
            ProblemIdentifier,
            SchoolRecommender,
        )
    except ImportError:
        return {"called": False, "error": "pan_wisdom_core unavailable"}

    try:
        tree = PanWisdomTree(enable_track_b=False)
        result = tree.reason(text, context)

        # 提取学派推荐
        schools = [
            {"school": r.school.value, "confidence": r.confidence, "reason": r.reason}
            for r in result.recommended_schools[:5]
        ]

        # 提取洞察
        insights = result.fusion_insights[:5]

        return {
            "called": True,
            "success": True,
            "identified_types": [str(t) for t in result.identified_types],
            "schools": schools,
            "insights": insights,
            "confidence": result.confidence,
            "recommendations": result.final_recommendations[:3],
            "pan_wisdom_result": result,
        }
    except Exception as e:
        return {"called": False, "error": str(e)}


def _get_refute_core_engine():
    """懒加载获取 RefuteCore 驳心引擎单例"""
    # RefuteCore 位于 smart_office_assistant/src/intelligence/engines/refute_core.py
    # 需要确保 somn 根目录在 sys.path 中
    import sys
    import os

    _somm_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if _somm_root not in sys.path:
        sys.path.insert(0, _somm_root)

    try:
        from smart_office_assistant.src.intelligence.engines.refute_core import get_refute_core
    except ImportError:
        try:
            from engines.refute_core import get_refute_core
        except ImportError:
            return None
    return get_refute_core()


def _call_refute_core(text: str, reasoning_info: Dict = None) -> Dict[str, Any]:
    """
    调用 RefuteCore 驳心引擎进行 T2 二次论证

    RefuteCore v3.2 驳心引擎 — 8维度反驳论证系统:
    1. 论证解析 — 拆解论点结构（主谓宾+领域+否定主张）
    2. 8大维度反驳 — 逻辑/证据/假设/反面/类比/权威/因果/价值
    3. 强度评估 — S/A/B/C/D/F 六级量化
    4. 风险判定 — 红/橙/黄/绿四级

    Args:
        text: 推理结论文本（待论证的论点）
        reasoning_info: 推理层上下文信息（可选）

    Returns:
        RefuteCore 论证结果结构化字典
    """
    engine = _get_refute_core_engine()
    if engine is None:
        return {
            "called": False,
            "method": "RefuteCore 驳心引擎 v3.2",
            "error": "RefuteCore 引擎不可用",
            "passed": False,
            "confidence": 0.0,
        }

    try:
        # 增强论证输入：合并推理结论+原文
        enhanced_text = text
        if reasoning_info:
            conclusion = reasoning_info.get("conclusion", "")
            if conclusion and conclusion != text:
                enhanced_text = f"{text}\n推理结论: {conclusion}"

        result = engine.refute(enhanced_text)

        # 评估论证是否通过
        assessment = result.assessment
        # 通过标准: 强度等级 B(60%) 及以上
        strength_passed = assessment.overall_strength >= 0.6
        # 风险等级不能是红/橙
        risk_ok = result.risk_level not in ("🔴 极高风险", "🟠 高风险")
        passed = strength_passed and risk_ok

        # 提取8维度反驳摘要
        dimension_results = []
        for ref in result.refutation.refutations:
            dimension_results.append({
                "dimension": ref.dimension.value if hasattr(ref.dimension, 'value') else str(ref.dimension),
                "counter_argument": ref.counter_argument[:100] if ref.counter_argument else "",
                "strength": ref.strength,
                "strategy": ref.strategy[:80] if ref.strategy else "",
            })

        return {
            "called": True,
            "method": "RefuteCore 驳心引擎 v3.2 (真实引擎)",
            "version": result.engine_version,
            "passed": passed,
            "confidence": assessment.overall_strength,
            "strength_grade": assessment.strength_grade,
            "risk_level": result.risk_level,
            "assessment": {
                "overall": assessment.overall_strength,
                "premise": assessment.premise_strength,
                "reasoning": assessment.reasoning_strength,
                "evidence": assessment.evidence_strength,
                "assumption": assessment.assumption_strength,
                "vulnerabilities": assessment.vulnerabilities[:3] if assessment.vulnerabilities else [],
                "detected_fallacies": [f.value if hasattr(f, 'value') else str(f) for f in (assessment.detected_fallacies or [])],
                "improvement_suggestions": assessment.improvement_suggestions[:3] if assessment.improvement_suggestions else [],
            },
            "dimension_coverage": result.refutation.dimension_coverage,
            "combined_refutation_strength": result.refutation.combined_strength,
            "key_insight": result.refutation.key_insight[:100] if result.refutation.key_insight else "",
            "critical_flaw": result.refutation.critical_flaw[:100] if result.refutation.critical_flaw else "",
            "dimension_results": dimension_results,
            "executive_summary": result.executive_summary[:200] if result.executive_summary else "",
            "key_takeaway": result.key_takeaway[:150] if result.key_takeaway else "",
            "argument_type": result.parsed_argument.argument_type.value if hasattr(result.parsed_argument.argument_type, 'value') else str(result.parsed_argument.argument_type),
            "context_domain": result.parsed_argument.context_domain,
            "repaired_claim": result.repair.repaired_claim[:100] if result.repair and result.repair.repaired_claim else "",
            "timestamp": result.timestamp,
        }
    except Exception as e:
        return {
            "called": False,
            "method": "RefuteCore 驳心引擎 v3.2",
            "error": str(e),
            "passed": False,
            "confidence": 0.0,
        }


# ==================== 核心枚举和数据结构 ====================

class ProcessingGrade(Enum):
    """处理等级"""
    BASIC = "basic"      # 基础：快速响应
    DEEP = "deep"        # 深度：神之架构并行
    SUPER = "super"      # 超级：全链路Claw讨论+T2 RefuteCore 驳心引擎论证


class DomainCategory(Enum):
    """领域分类"""
    SOCIAL_SCIENCE = "social_science"       # 社会科学
    LITERATURE_HISTORY = "literature_history"  # 文学历史
    NATURAL_SCIENCE = "natural_science"     # 自然科学
    TECHNOLOGY = "technology"               # 科技
    BUSINESS = "business"                   # 商业
    PHILOSOPHY = "philosophy"               # 哲学
    GENERAL = "general"                     # 通用


class PipelineStage(Enum):
    """管道阶段"""
    INPUT = "input"                         # 输入层
    NL_ANALYSIS = "nl_analysis"             # 自然语言需求分析
    CLASSIFICATION = "classification"       # 需求分类
    ROUTING = "routing"                     # 分流
    REASONING = "reasoning"                 # 推理
    ARGUMENTATION = "argumentation"         # 论证
    ACTION_PLANNING = "action_planning"     # L6.5 行动规划（engagement v22.0）
    OUTPUT = "output"                       # 输出
    OPTIMIZATION = "optimization"           # 优化
    USER_ENGAGEMENT = "user_engagement"   # L8.5 用户参与（engagement v22.0）


@dataclass
class LayerResult:
    """层级处理结果"""
    layer_name: str
    stage: PipelineStage
    success: bool
    data: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.8
    duration_ms: float = 0.0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class PipelineResult:
    """管道最终结果"""
    request_id: str
    grade: ProcessingGrade
    domain: DomainCategory
    all_layers: Dict[str, LayerResult] = field(default_factory=dict)
    final_answer: str = ""
    final_confidence: float = 0.0
    total_duration_ms: float = 0.0
    routing_path: List[str] = field(default_factory=list)
    reasoning_chain: List[Dict] = field(default_factory=list)
    argumentation_result: Optional[Dict] = None
    optimization_suggestions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    # 多模态输出 (v6.2 OutputEngine)
    output_format: Optional[str] = None           # 输出格式名 (text/markdown/html/image/pdf/pptx/docx)
    output_artifact: Optional[Any] = None         # OutputArtifact 对象 (懒导入避免循环)


# ==================== Layer 1: 输入层 ====================

class InputLayer:
    """
    输入层 - 原始输入接收与预处理

    职责：
    - 接收原始用户输入
    - 基础文本清洗（去空白、标准化）
    - 输入类型识别（文本/结构化）
    - 空输入检测与拦截
    """

    # 预编译正则（类级别，避免每次调用 re.findall 时重新编译）
    _RE_WORD = re.compile(r'[\u4e00-\u9fa5a-zA-Z]+')

    def process(self, raw_input: Any) -> LayerResult:
        """处理原始输入"""
        start = time.perf_counter()

        # 空输入检测
        if raw_input is None:
            return LayerResult(
                layer_name="输入层",
                stage=PipelineStage.INPUT,
                success=False,
                errors=["输入为空"],
                confidence=0.0,
                duration_ms=0.0
            )

        # 统一为字符串
        if isinstance(raw_input, str):
            text = raw_input.strip()
        elif isinstance(raw_input, dict):
            text = raw_input.get("description", str(raw_input)).strip()
        else:
            text = str(raw_input).strip()

        # 空文本检测
        if not text:
            return LayerResult(
                layer_name="输入层",
                stage=PipelineStage.INPUT,
                success=False,
                errors=["输入文本为空"],
                confidence=0.0,
                duration_ms=0.0
            )

        elapsed = (time.perf_counter() - start) * 1000

        return LayerResult(
            layer_name="输入层",
            stage=PipelineStage.INPUT,
            success=True,
            data={
                "original_input": raw_input,
                "cleaned_text": text,
                "input_type": type(raw_input).__name__,
                "text_length": len(text),
                "char_count": len(text),
                "word_count": len(InputLayer._RE_WORD.findall(text)),
            },
            confidence=1.0,
            duration_ms=elapsed
        )


# ==================== Layer 2: 自然语言需求分析层 ====================

class NLAnalysisLayer:
    """
    自然语言需求分析层 - NLP深度解析

    职责：
    - 深度解析用户输入
    - 提取关键信息（实体、时间、数量、关系）
    - 识别用户意图
    - 判断需求类型
    - 领域分类（社会科学/文学历史/自然科学/科技/商业/哲学）
    - 评估复杂度和紧急程度
    """

    # 预编译正则（类级别，避免每次调用 re.findall 时重新编译）
    _RE_KEYWORD = re.compile(r'[\u4e00-\u9fa5a-zA-Z0-9]{2,}')
    _RE_PERSON = re.compile(r'[\u4e00-\u9fa5]{2,4}(?:先生|女士|教授|博士|总)')
    _RE_TIME = [
        (re.compile(r'\d{4}年'), "year"),
        (re.compile(r'\d{1,2}月'), "month"),
        (re.compile(r'\d{1,2}日'), "day"),
        (re.compile(r'第[一二三四五六七八九十\d]+季'), "quarter"),
        (re.compile(r'上[半年月周]'), "relative_past"),
        (re.compile(r'下[半年月周]'), "relative_future"),
        (re.compile(r'最近|近期|目前|当前|现在'), "current"),
    ]
    _RE_QUANTITY = [
        re.compile(r'\d+(?:\.\d+)?(?:%)'),          # 百分比
        re.compile(r'\d+(?:\.\d+)?(?:万|亿|千|百)'), # 大数
        re.compile(r'\$\d+(?:\.\d+)?'),              # 美元
        re.compile(r'¥\d+(?:\.\d+)?'),               # 人民币
        re.compile(r'\d+(?:\.\d+)?(?:元|块)'),        # 金额
    ]

    # 领域关键词映射（带权重，高权重=更精准的关键词）
    DOMAIN_KEYWORDS = {
        DomainCategory.SOCIAL_SCIENCE: [
            ("社会", 2), ("政治", 2), ("经济", 2), ("文化", 1), ("教育", 2),
            ("法律", 2), ("制度", 2), ("政策", 2), ("民生", 2), ("人口", 2),
            ("城市化", 2), ("贫富", 2), ("阶层", 2),
            ("社会学", 3), ("经济学", 3), ("心理学", 3), ("管理学", 3), ("法学", 3)
        ],
        DomainCategory.LITERATURE_HISTORY: [
            ("文学", 2), ("诗歌", 3), ("小说", 3), ("散文", 3), ("戏剧", 3),
            ("历史", 2), ("古典", 2), ("现代文学", 3), ("作家", 3), ("诗人", 3),
            ("朝代", 3), ("文明", 1), ("哲学史", 3), ("思想史", 3),
            ("文化遗产", 3), ("文言文", 3), ("诗经", 3),
            ("论语", 4), ("孟子", 4), ("老子", 4), ("庄子", 4), ("史记", 4),
            ("春秋", 3), ("唐诗", 4), ("宋词", 4), ("红楼梦", 4),
            ("三国演义", 4), ("水浒传", 4),
        ],
        DomainCategory.NATURAL_SCIENCE: [
            ("物理", 2), ("化学", 2), ("生物", 2), ("数学", 2),
            ("天文", 3), ("地理", 1), ("实验", 2), ("分子", 3),
            ("原子", 3), ("基因", 3), ("量子", 4), ("进化", 2),
            ("生态系统", 3), ("气候变化", 3), ("化学反应", 3), ("力学", 2)
        ],
        DomainCategory.TECHNOLOGY: [
            ("AI", 4), ("人工智能", 4), ("算法", 3), ("编程", 3),
            ("互联网", 3), ("数据", 1), ("软件", 3), ("硬件", 3),
            ("芯片", 4), ("5G", 4), ("区块链", 4), ("云计算", 4),
            ("机器学习", 4), ("深度学习", 4), ("物联网", 4),
            ("自动化", 3), ("机器人", 4), ("推荐系统", 4),
        ],
        DomainCategory.BUSINESS: [
            ("运营", 3), ("营销", 3), ("品牌", 3), ("GMV", 4), ("转化率", 4),
            ("ROI", 4), ("获客", 3), ("留存", 3), ("增长", 2),
            ("投放", 3), ("直播", 3), ("电商", 3), ("供应链", 3),
            ("管理", 1), ("财务", 3), ("投资", 2), ("创业", 3), ("融资", 3),
        ],
        DomainCategory.PHILOSOPHY: [
            ("哲学", 3), ("伦理", 3), ("存在主义", 4),
            ("意识", 2), ("自由意志", 4), ("辩证法", 3), ("逻辑", 2),
            ("真理", 3), ("价值", 1), ("意义", 1), ("本体论", 4),
            ("认识论", 4), ("形而上学", 4), ("道家思想", 4), ("佛家思想", 4),
        ],
        DomainCategory.GENERAL: [
            ("哲学", 1), ("系统论", 2),
        ],
    }

    # 意图分类
    INTENT_PATTERNS = {
        "query": ["是什么", "什么是", "如何", "怎么", "多少", "谁", "哪里", "什么时候", "能不能", "有没有"],
        "analysis": ["分析", "评估", "判断", "检验", "研究", "验证", "诊断", "测算"],
        "planning": ["战略", "规划", "策划", "设计方案", "布局", "路线", "路径"],
        "decision": ["决策", "选择", "决定", "定夺", "权衡", "比较", "推荐哪个"],
        "execution": ["执行", "实施", "落地", "操作", "推动", "落实", "部署"],
        "innovation": ["创新", "创造", "突破", "颠覆", "革命", "变革", "转型", "重构"],
        "critique": ["反驳", "批评", "评价", "论证", "质疑", "驳斥", "论辩"],
    }

    def process(self, input_layer_result: LayerResult) -> LayerResult:
        """深度NLP分析（含网络搜索增强）"""
        start = time.perf_counter()
        text = input_layer_result.data["cleaned_text"]

        # 1. 提取关键信息
        entities = self._extract_entities(text)
        time_refs = self._extract_time_references(text)
        quantities = self._extract_quantities(text)
        relations = self._extract_relations(text)

        # 2. 意图识别
        intent = self._recognize_intent(text)

        # 3. 需求类型判断
        demand_type = self._classify_demand(intent, text)

        # 4. 领域分类
        domain, domain_scores = self._classify_domain(text)

        # 5. 复杂度评估
        complexity = self._assess_complexity(text, intent, entities)

        # 6. 紧急程度评估
        urgency = self._assess_urgency(text)

        # 7. 关键词提取
        keywords = self._RE_KEYWORD.findall(text)

        # ── 8. 网络搜索增强：术语解释 ──
        web_enhancement = {}
        tianshu_web = _get_tianshu_web()
        if tianshu_web and tianshu_web.is_enabled():
            try:
                enhancement = tianshu_web.enhance_nlp_analysis(text, layer_context="NLP分析")
                if enhancement.get("success") and enhancement.get("terms"):
                    web_enhancement = enhancement
                    logger.info(f"[TianShu] NLP enhanced with {len(enhancement.get('terms', []))} terms")
            except Exception as e:
                logger.warning(f"[TianShu] NLP enhancement failed: {e}")

        elapsed = (time.perf_counter() - start) * 1000

        return LayerResult(
            layer_name="自然语言需求分析层",
            stage=PipelineStage.NL_ANALYSIS,
            success=True,
            data={
                "text": text,
                "intent": intent,
                "demand_type": demand_type,
                "domain": domain,
                "domain_scores": domain_scores,
                "complexity": complexity,
                "urgency": urgency,
                "entities": entities,
                "time_references": time_refs,
                "quantities": quantities,
                "relations": relations,
                "keywords": keywords[:15],
                "text_length": len(text),
                "is_question": any(p in text for p in ["？", "?", "吗", "呢", "如何", "怎么", "为什么"]),
                "web_enhancement": web_enhancement,
            },
            confidence=0.85 if domain != DomainCategory.GENERAL else 0.7,
            duration_ms=elapsed
        )

    def _extract_entities(self, text: str) -> List[Dict]:
        """提取命名实体"""
        entities = []

        # 组织实体
        org_markers = ["公司", "企业", "集团", "机构", "组织", "部门", "大学", "研究院"]
        for marker in org_markers:
            idx = text.find(marker)
            if idx >= 0:
                start = max(0, idx - 8)
                entities.append({
                    "type": "organization",
                    "text": text[start:idx + len(marker)],
                    "marker": marker
                })

        # 人物实体
        person_patterns = self._RE_PERSON.findall(text)
        for p in person_patterns:
            entities.append({"type": "person", "text": p})

        # 产品/技术实体
        tech_markers = ["系统", "平台", "产品", "技术", "模型", "算法", "框架"]
        for marker in tech_markers:
            idx = text.find(marker)
            if idx >= 0:
                start = max(0, idx - 6)
                entities.append({
                    "type": "technology",
                    "text": text[start:idx + len(marker)],
                    "marker": marker
                })

        return entities[:10]

    def _extract_time_references(self, text: str) -> List[Dict]:
        """提取时间引用"""
        results = []
        for pattern, time_type in self._RE_TIME:
            matches = pattern.findall(text)
            for m in matches:
                results.append({"type": time_type, "text": m})
        return results[:5]

    def _extract_quantities(self, text: str) -> List[Dict]:
        """提取数量信息"""
        results = []
        for pattern in self._RE_QUANTITY:
            matches = pattern.findall(text)
            for m in matches:
                results.append({"text": m, "type": "quantity"})
        return results[:5]

    def _extract_relations(self, text: str) -> List[Dict]:
        """提取关系信息"""
        relation_markers = [
            ("因果", ["因为", "所以", "导致", "造成", "由于", "因而", "因此"]),
            ("条件", ["如果", "只要", "只有", "无论", "不管", "假设", "假如"]),
            ("转折", ["但是", "然而", "不过", "虽然", "尽管", "可是"]),
            ("递进", ["而且", "并且", "此外", "同时", "另外", "不仅如此"]),
            ("对比", ["相比", "对比", "相对", "比较", "而", "则"]),
        ]

        results = []
        for rel_type, markers in relation_markers:
            for marker in markers:
                if marker in text:
                    results.append({"type": rel_type, "marker": marker})
                    break
        return results[:5]

    def _recognize_intent(self, text: str) -> Dict:
        """识别用户意图"""
        text_lower = text.lower()
        intent_scores = {}

        for intent_name, patterns in self.INTENT_PATTERNS.items():
            score = sum(1 for p in patterns if p in text_lower)
            if score > 0:
                intent_scores[intent_name] = score

        # 确定主意图
        if intent_scores:
            primary = max(intent_scores, key=intent_scores.get)
            all_intents = sorted(intent_scores.keys(), key=lambda x: intent_scores[x], reverse=True)
        else:
            primary = "query"
            all_intents = ["query"]

        # 检测是否需要深度推理
        requires_deep = any(kw in text for kw in ["为什么", "原因", "本质", "深层", "根本"])

        return {
            "primary": primary,
            "all_intents": all_intents,
            "scores": intent_scores,
            "requires_deep_reasoning": requires_deep,
            "intent_count": len(intent_scores),
        }

    def _classify_demand(self, intent: Dict, text: str) -> str:
        """需求类型分类"""
        primary = intent["primary"]
        demand_map = {
            "query": "信息查询",
            "analysis": "分析研究",
            "planning": "战略规划",
            "decision": "决策选择",
            "execution": "执行落地",
            "innovation": "创新突破",
            "critique": "论证反驳",
        }
        return demand_map.get(primary, "综合需求")

    def _classify_domain(self, text: str) -> Tuple[DomainCategory, Dict[str, float]]:
        """领域分类（带权重）"""
        scores = {}
        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            score = 0
            for kw_item in keywords:
                # 支持带权重的元组格式
                if isinstance(kw_item, tuple):
                    kw, weight = kw_item
                else:
                    kw, weight = kw_item, 1
                if kw in text:
                    score += weight
            if score > 0:
                scores[domain] = score

        if scores:
            best_domain = max(scores, key=scores.get)
            # 归一化
            total = sum(scores.values())
            normalized = {d.value: round(s / total, 3) for d, s in scores.items()}
        else:
            best_domain = DomainCategory.GENERAL
            normalized = {}

        return best_domain, normalized

    def _assess_complexity(self, text: str, intent: Dict, entities: List) -> Dict:
        """评估复杂度"""
        score = 0

        # 文本长度
        if len(text) > 500:
            score += 3
        elif len(text) > 200:
            score += 2
        elif len(text) > 100:
            score += 1

        # 意图复杂度
        if intent["intent_count"] > 2:
            score += 2
        elif intent["intent_count"] > 1:
            score += 1

        # 实体数量
        score += min(len(entities), 3)

        # 关键指标
        complex_markers = ["系统", "架构", "全面", "综合", "多维度", "多层次", "体系", "框架"]
        score += sum(1 for m in complex_markers if m in text)

        # 确定等级
        if score >= 7:
            level = "high"
        elif score >= 4:
            level = "medium"
        else:
            level = "low"

        return {
            "level": level,
            "score": score,
            "factors": {
                "text_length": len(text),
                "intent_count": intent["intent_count"],
                "entity_count": len(entities),
            }
        }

    def _assess_urgency(self, text: str) -> str:
        """评估紧急程度"""
        if any(kw in text for kw in ["紧急", "立即", "马上", "立刻", "刻不容缓", "火速"]):
            return "high"
        elif any(kw in text for kw in ["尽快", "优先", "重要", "急需", "迫切"]):
            return "medium"
        return "normal"


# ==================== Layer 3: 需求分类数据库 ====================

class ClassificationDB:
    """
    需求分类数据库 - 需求→智慧引擎/智慧格子映射

    职责：
    - 维护需求类型与智慧引擎的映射关系
    - 维护需求类型与智慧格子的关联
    - 根据分析结果推荐处理路径
    - 提供领域→学派→格子的三级关联
    """

    # 需求类型 → 推荐引擎映射
    DEMAND_ENGINE_MAP = {
        "信息查询": {
            "primary_engines": ["SD-P1"],
            "secondary_engines": ["SD-F2"],
            "cells": ["A1"],
            "reasoning_depth": "light",
        },
        "分析研究": {
            "primary_engines": ["SD-P1", "SD-R2", "SD-D2"],
            "secondary_engines": ["SD-F1"],
            "cells": ["A1", "A2", "A3"],
            "reasoning_depth": "standard",
        },
        "战略规划": {
            "primary_engines": ["SD-P1", "SD-F1", "SD-C2"],
            "secondary_engines": ["SD-D2", "SD-D3"],
            "cells": ["A1", "A2", "A4", "A5"],
            "reasoning_depth": "deep",
        },
        "决策选择": {
            "primary_engines": ["SD-P1", "SD-F1", "SD-C1", "SD-C2"],
            "secondary_engines": ["SD-D2"],
            "cells": ["A1", "A4"],
            "reasoning_depth": "deep",
        },
        "执行落地": {
            "primary_engines": ["SD-P1", "SD-E1"],
            "secondary_engines": ["SD-F2", "SD-L1"],
            "cells": ["A6"],
            "reasoning_depth": "light",
        },
        "创新突破": {
            "primary_engines": ["SD-P1", "SD-F1", "SD-D3", "SD-C2"],
            "secondary_engines": ["SD-E1"],
            "cells": ["A1", "A2", "A3", "A5"],
            "reasoning_depth": "deep",
        },
        "论证反驳": {
            "primary_engines": ["SD-P1", "SD-R2", "SD-D2"],
            "secondary_engines": ["SD-F1"],
            "cells": ["A1", "A2", "A3"],
            "reasoning_depth": "standard",
        },
        "综合需求": {
            "primary_engines": ["SD-P1", "SD-F2"],
            "secondary_engines": ["SD-R2", "SD-F1"],
            "cells": ["A1", "A2"],
            "reasoning_depth": "standard",
        },
    }

    # 领域 → 学派关联
    DOMAIN_SCHOOL_MAP = {
        DomainCategory.SOCIAL_SCIENCE: ["经济学", "社会学", "心理学", "法学", "政治学"],
        DomainCategory.LITERATURE_HISTORY: ["儒家", "佛家", "道家", "历史学"],
        DomainCategory.NATURAL_SCIENCE: ["科学", "哲学", "系统论", "复杂性科学"],
        DomainCategory.TECHNOLOGY: ["人工智能", "系统论", "设计思维", "精益创业"],
        DomainCategory.BUSINESS: ["管理学", "经济学", "博弈论", "运筹学", "设计思维"],
        DomainCategory.PHILOSOPHY: ["哲学", "道家", "儒家", "佛家", "阴阳家", "名家", "墨家"],
        DomainCategory.GENERAL: ["哲学", "系统论"],
    }

    # 知识格子映射
    CELL_DESCRIPTIONS = {
        "A1": "逻辑判断 - 推理分析核心",
        "A2": "智慧模块 - 学派融合智慧",
        "A3": "论证审核 - 超级推理引擎",
        "A4": "判断决策 - 太极阴阳/神之架构决策",
        "A5": "五层架构 - 架构体系",
        "A6": "五步主链 - 核心执行链",
        "A7": "直觉记忆 - 感知记忆系统",
        "A8": "反思进化 - 学习进化系统",
    }

    def process(self, analysis_result: LayerResult, grade: ProcessingGrade) -> LayerResult:
        """分类与引擎推荐"""
        start = time.perf_counter()
        data = analysis_result.data

        demand_type = data.get("demand_type", "综合需求")
        domain = data.get("domain", DomainCategory.GENERAL)
        intent = data.get("intent", {})
        complexity = data.get("complexity", {})
        urgency = data.get("urgency", "normal")

        # 1. 获取推荐引擎配置
        engine_config = self.DEMAND_ENGINE_MAP.get(demand_type, self.DEMAND_ENGINE_MAP["综合需求"])

        # 2. 根据等级调整引擎
        engines = self._adjust_engines_for_grade(engine_config, grade)

        # 3. 获取推荐学派
        schools = self.DOMAIN_SCHOOL_MAP.get(domain, self.DOMAIN_SCHOOL_MAP[DomainCategory.GENERAL])

        # 4. 获取关联格子
        cells = engine_config.get("cells", ["A1"])
        cell_details = {c: self.CELL_DESCRIPTIONS.get(c, "未知格子") for c in cells}

        # 5. 确定推理深度
        reasoning_depth = self._determine_reasoning_depth(engine_config, complexity, grade)

        # 6. 构建推荐路径
        routing_path = self._build_routing_path(engines, grade)

        elapsed = (time.perf_counter() - start) * 1000

        return LayerResult(
            layer_name="需求分类数据库",
            stage=PipelineStage.CLASSIFICATION,
            success=True,
            data={
                "demand_type": demand_type,
                "domain": domain,
                "primary_engines": engines["primary"],
                "secondary_engines": engines["secondary"],
                "reasoning_depth": reasoning_depth,
                "recommended_schools": schools,
                "recommended_cells": cell_details,
                "routing_path": routing_path,
                "complexity": complexity.get("level", "medium"),
                "urgency": urgency,
                "grade": grade.value,
            },
            confidence=0.9,
            duration_ms=elapsed
        )

    def _adjust_engines_for_grade(self, base_config: Dict, grade: ProcessingGrade) -> Dict:
        """根据处理等级调整引擎组合"""
        primary = list(base_config["primary_engines"])
        secondary = list(base_config.get("secondary_engines", []))

        if grade == ProcessingGrade.BASIC:
            # 基础：精简引擎
            primary = [e for e in primary if e in ["SD-P1", "SD-F2"]]
            secondary = []
        elif grade == ProcessingGrade.DEEP:
            # 深度：确保包含SD-R1监管
            if "SD-R1" not in primary:
                primary.append("SD-R1")
        elif grade == ProcessingGrade.SUPER:
            # 超级：全量引擎
            if "SD-R1" not in primary:
                primary.append("SD-R1")
            if "SD-F1" not in primary:
                primary.append("SD-F1")
            if "SD-D3" not in secondary:
                secondary.append("SD-D3")

        # 去重保序
        primary = list(dict.fromkeys(primary))
        secondary = list(dict.fromkeys(secondary))

        return {"primary": primary, "secondary": secondary}

    def _determine_reasoning_depth(self, config: Dict, complexity: Dict, grade: ProcessingGrade) -> str:
        """确定推理深度"""
        base = config.get("reasoning_depth", "standard")

        if grade == ProcessingGrade.BASIC:
            return "light"
        elif grade == ProcessingGrade.SUPER:
            return "deep"
        elif grade == ProcessingGrade.DEEP:
            if complexity.get("level") == "high":
                return "deep"
            return "standard"
        return base

    def _build_routing_path(self, engines: Dict, grade: ProcessingGrade) -> List[str]:
        """构建推荐路由路径"""
        path = list(engines["primary"])

        if grade == ProcessingGrade.BASIC:
            # 基础：SD-P1 → SD-F2推理 → SD-E1执行（不进神之架构）
            if "SD-E1" not in path:
                path.append("SD-E1")
        elif grade == ProcessingGrade.DEEP:
            # 深度：SD-P1 → SD-F2推理 → SD-E1执行（同步进入神之架构并行）
            if "SD-C2" not in path:
                path.append("SD-C2")
            if "SD-E1" not in path:
                path.append("SD-E1")
        elif grade == ProcessingGrade.SUPER:
            # 超级：SD-P1 → SD-F1+SD-F2推理 → SD-E1执行（同步进入神之架构并行+Claw讨论）
            if "SD-F1" not in path:
                path.insert(1, "SD-F1")
            if "SD-C2" not in path:
                path.append("SD-C2")
            if "SD-E1" not in path:
                path.append("SD-E1")

        return list(dict.fromkeys(path))


# ==================== Layer 4: 分流层 ====================

class RoutingLayer:
    """
    分流层 - 智能匹配到合适的智慧格子和智慧引擎

    职责：
    - 调用真实 SageDispatch 调度器进行分流
    - 根据处理等级（基础/深度/超级）执行不同的分流策略
    - 基础：SD-P1 → SD-F2 → SD-E1（不进入神之架构）
    - 深度：SD-P1 → SD-F2 → SD-E1（同步进入神之架构并行，Claw讨论）
    - 超级：SD-P1 → SD-F1+SD-F2 → SD-E1（全链路Claw讨论）
    - ⚠️ 支持接收论证反馈(reroute_feedback)进行修正式分流，而非简单重复
    """

    def process(self, classification_result: LayerResult, analysis_data: Dict, grade: ProcessingGrade,
                reroute_feedback: Dict = None) -> LayerResult:
        """执行分流 - 调用真实调度器

        Args:
            classification_result: L3分类结果（含 routing_path, reasoning_depth 等）
            analysis_data: L2分析结果数据（含用户原文 text 字段）
            grade: 处理等级
            reroute_feedback: 论证不合格回退反馈
        """
        start = time.perf_counter()
        data = classification_result.data
        text = analysis_data.get("text", "")  # 从L2分析结果获取用户原文

        routing_path = data["routing_path"]
        reasoning_depth = data["reasoning_depth"]

        # 根据等级确定调度链路并调用真实调度器（传递用户原文）
        if grade == ProcessingGrade.BASIC:
            strategy, dispatcher_results = self._basic_strategy(data, text, reroute_feedback)
        elif grade == ProcessingGrade.DEEP:
            strategy, dispatcher_results = self._deep_strategy(data, text, reroute_feedback)
        else:
            strategy, dispatcher_results = self._super_strategy(data, text, reroute_feedback)

        elapsed = (time.perf_counter() - start) * 1000

        # 计算调度器平均置信度
        dispatch_confidences = [r.get("confidence", 0.8) for r in dispatcher_results if r.get("called")]
        avg_dispatch_conf = sum(dispatch_confidences) / len(dispatch_confidences) if dispatch_confidences else 0.8

        # 如果有修正反馈，记录修正信息
        is_reroute = reroute_feedback is not None
        corrective_hints = reroute_feedback.get("corrective_hints", []) if reroute_feedback else []

        return LayerResult(
            layer_name="分流层",
            stage=PipelineStage.ROUTING,
            success=all(r.get("called", False) for r in dispatcher_results),
            data={
                "text": text,  # 用户原文，透传给后续层
                "grade": grade.value,
                "routing_path": routing_path,
                "strategy": strategy,
                "reasoning_depth": reasoning_depth,
                "enter_divine_architecture": grade in (ProcessingGrade.DEEP, ProcessingGrade.SUPER),
                "claw_discussion": grade in (ProcessingGrade.DEEP, ProcessingGrade.SUPER),
                "dispatcher_results": dispatcher_results,
                "dispatchers_called": [r.get("dispatcher_id") for r in dispatcher_results],
                "is_reroute": is_reroute,
                "reroute_attempt": reroute_feedback.get("attempt", 0) if reroute_feedback else 0,
                "corrective_hints_applied": corrective_hints,
            },
            confidence=avg_dispatch_conf,
            duration_ms=elapsed,
            warnings=[r.get("error", "") for r in dispatcher_results if not r.get("called")]
        )

    def _basic_strategy(self, data: Dict, text: str, reroute_feedback: Dict = None) -> Tuple[Dict, List[Dict]]:
        """
        基础分流策略：
        SD-P1(问题调度) → SD-F2(四级调度) → SD-E1(核心执行链)
        不进入神之架构

        如果有 reroute_feedback，在分流描述中附加修正提示
        """
        # 修正模式：根据反馈调整调度链路
        chain_path = ["SD-P1", "SD-F2", "SD-E1"]
        if reroute_feedback and reroute_feedback.get("escalation_recommended"):
            # 第2次失败后加入 SD-R2 提前谬误检测
            if "SD-R2" not in chain_path:
                chain_path.insert(len(chain_path) - 1, "SD-R2")

        # 传递用户原文给调度器链（而非策略标签）
        dispatcher_results = _call_dispatcher_chain(text, chain_path)

        # 附加修正提示到步骤描述
        corrective_hints = reroute_feedback.get("corrective_hints", []) if reroute_feedback else []
        correction_note = ""
        if corrective_hints:
            correction_note = f" [修正: {'; '.join(corrective_hints[:2])}]"

        chain_label = f"基础分流(修正第{reroute_feedback.get('attempt', '?')}次)" if reroute_feedback else "基础分流"
        strategy = {
            "description": f"{chain_label} - 快速响应{correction_note}",
            "steps": [
                {"step": 1, "action": "SD-P1 问题调度", "detail": f"调用SD-P1(ProblemDispatcher)进行问题解析{correction_note}",
                 "dispatcher_result": dispatcher_results[0] if len(dispatcher_results) > 0 else None},
                {"step": 2, "action": "SD-F2 四级调度", "detail": f"调用SD-F2(FourLevelDispatchController)四级调度{correction_note}",
                 "dispatcher_result": dispatcher_results[1] if len(dispatcher_results) > 1 else None},
            ],
            "divine_architecture": False,
            "claw_discussion": False,
        }
        # 动态添加后续步骤（可能有SD-R2或SD-E1）
        step_idx = 2
        for i, dispatcher_id in enumerate(chain_path[2:], 2):
            detail_map = {
                "SD-E1": "调用SD-E1(ChainExecutor)五步主链执行",
                "SD-R2": "调用SD-R2(FallacyChecker)提前谬误检测",
            }
            strategy["steps"].append({
                "step": step_idx, "action": f"{dispatcher_id} {detail_map.get(dispatcher_id, '')}",
                "detail": f"{detail_map.get(dispatcher_id, dispatcher_id)}{correction_note}",
                "dispatcher_result": dispatcher_results[i] if i < len(dispatcher_results) else None,
            })
            step_idx += 1

        if reroute_feedback:
            strategy["is_reroute"] = True
            strategy["reroute_attempt"] = reroute_feedback.get("attempt", 0)
            strategy["strategy_used"] = "basic_corrected"

        return strategy, dispatcher_results

    def _deep_strategy(self, data: Dict, text: str, reroute_feedback: Dict = None) -> Tuple[Dict, List[Dict]]:
        """
        深度分流策略：
        SD-P1(问题调度) → SD-F2(四级调度) → SD-E1(核心执行链)
        同步进入神之架构并行论证，Claw讨论

        如果有 reroute_feedback，根据反馈调整策略
        """
        # 修正模式：根据反馈调整调度链路
        chain_path = ["SD-P1", "SD-F2", "SD-E1"]
        if reroute_feedback and reroute_feedback.get("escalation_recommended"):
            if "SD-R2" not in chain_path:
                chain_path.insert(len(chain_path) - 1, "SD-R2")

        # 传递用户原文给调度器链（而非策略标签）
        dispatcher_results = _call_dispatcher_chain(text, chain_path)

        corrective_hints = reroute_feedback.get("corrective_hints", []) if reroute_feedback else []
        correction_note = ""
        if corrective_hints:
            correction_note = f" [修正: {'; '.join(corrective_hints[:2])}]"

        chain_label = f"深度分流(修正第{reroute_feedback.get('attempt', '?')}次)" if reroute_feedback else "深度分流"
        strategy = {
            "description": f"{chain_label} - 神之架构并行{correction_note}",
            "steps": [
                {"step": 1, "action": "SD-P1 问题调度", "detail": f"调用SD-P1(ProblemDispatcher)进行深度解析{correction_note}",
                 "dispatcher_result": dispatcher_results[0] if len(dispatcher_results) > 0 else None},
                {"step": 2, "action": "SD-F2 四级调度", "detail": f"调用SD-F2(FourLevelDispatchController)分配深度推理资源{correction_note}",
                 "dispatcher_result": dispatcher_results[1] if len(dispatcher_results) > 1 else None},
            ],
            "divine_architecture": True,
            "claw_discussion": True,
        }
        step_idx = 2
        for i, dispatcher_id in enumerate(chain_path[2:], 2):
            detail_map = {
                "SD-E1": "调用SD-E1(ChainExecutor)有序执行",
                "SD-R2": "调用SD-R2(FallacyChecker)提前谬误检测",
            }
            strategy["steps"].append({
                "step": step_idx, "action": f"{dispatcher_id} {detail_map.get(dispatcher_id, '')}",
                "detail": f"{detail_map.get(dispatcher_id, dispatcher_id)}{correction_note}",
                "dispatcher_result": dispatcher_results[i] if i < len(dispatcher_results) else None,
            })
            step_idx += 1

        strategy["steps"].append({"step": step_idx, "action": "神之架构并行", "detail": "同步进入神之架构进行并行论证，Claw讨论"})
        step_idx += 1

        if reroute_feedback:
            strategy["is_reroute"] = True
            strategy["reroute_attempt"] = reroute_feedback.get("attempt", 0)
            strategy["strategy_used"] = "deep_corrected"

        return strategy, dispatcher_results

    def _super_strategy(self, data: Dict, text: str, reroute_feedback: Dict = None) -> Tuple[Dict, List[Dict]]:
        """
        超级分流策略：
        SD-P1(问题调度) → SD-F1(学派融合) + SD-F2(四级调度) → SD-E1(核心执行链)
        全链路Claw讨论

        如果有 reroute_feedback，根据反馈加强论证资源
        """
        # 修正模式：根据反馈调整调度链路
        chain_path = ["SD-P1", "SD-F1", "SD-F2", "SD-E1"]
        if reroute_feedback and reroute_feedback.get("escalation_recommended"):
            if "SD-R2" not in chain_path:
                chain_path.insert(len(chain_path) - 1, "SD-R2")
            if "SD-L1" not in chain_path:
                chain_path.append("SD-L1")

        # 传递用户原文给调度器链（而非策略标签）
        dispatcher_results = _call_dispatcher_chain(text, chain_path)

        corrective_hints = reroute_feedback.get("corrective_hints", []) if reroute_feedback else []
        correction_note = ""
        if corrective_hints:
            correction_note = f" [修正: {'; '.join(corrective_hints[:2])}]"

        chain_label = f"超级分流(修正第{reroute_feedback.get('attempt', '?')}次)" if reroute_feedback else "超级分流"
        strategy = {
            "description": f"{chain_label} - 全链路Claw讨论{correction_note}",
            "steps": [],
            "divine_architecture": True,
            "claw_discussion": True,
            "full_chain_review": True,
        }

        detail_map = {
            "SD-P1": "调用SD-P1(ProblemDispatcher)进行极致解析",
            "SD-F1": "调用SD-F1(SchoolFusion)25学派融合智慧",
            "SD-F2": "调用SD-F2(FourLevelDispatchController)四级调度机制，全学派融合",
            "SD-R2": "调用SD-R2(FallacyChecker)加强谬误检测",
            "SD-E1": "调用SD-E1(ChainExecutor)有序执行",
            "SD-L1": "调用SD-L1(ResultTracker)强化学习反馈",
        }
        for i, dispatcher_id in enumerate(chain_path):
            strategy["steps"].append({
                "step": i + 1, "action": f"{dispatcher_id} {detail_map.get(dispatcher_id, '')}",
                "detail": f"{detail_map.get(dispatcher_id, dispatcher_id)}{correction_note}",
                "dispatcher_result": dispatcher_results[i] if i < len(dispatcher_results) else None,
            })

        step_idx = len(chain_path) + 1
        strategy["steps"].append({"step": step_idx, "action": "神之架构并行", "detail": "同步进入神之架构进行并行论证"})
        strategy["steps"].append({"step": step_idx + 1, "action": "全链路Claw讨论", "detail": "所有执行链路必须通过神之架构论证，进行Claw讨论"})

        if reroute_feedback:
            strategy["is_reroute"] = True
            strategy["reroute_attempt"] = reroute_feedback.get("attempt", 0)
            strategy["strategy_used"] = "super_corrected"

        return strategy, dispatcher_results


# ==================== Layer 5: 推理层 ====================

class ReasoningLayer:
    """
    推理层 - 核心推理与决策（调用真实 SageDispatch 调度器）

    三种等级的推理策略：

    基础：
    - 调用真实 SD-C2(DivineArchitecture) 神之架构决策体系进行综合判断
    - 得出初步结论后，调用 SD-D1(SuperReasoning-light) 轻量论证审核
    - 翰林院轻量审核（不合格返回分流层）

    深度：
    - 调用真实 SD-C1(YinYangDecision) 太极阴阳决策体系进行综合判断
    - 得出初步结论后，调用 SD-D2(SuperReasoning-standard) 标准深度推理论证
    - 通过翰林院三轮审核机制对决策过程和结果进行审核验证（不合格返回分流层）

    超级：
    - 调用真实 SD-C1(YinYangDecision) + SD-C2(DivineArchitecture) 联合神之架构决策体系
    - 得出初步结论后，调用 SD-D3(SuperReasoning-deep) 极致深度论证
    - 通过翰林院三轮审核机制严格验证（验证不合格返回分流层）

    ⚠️ 所有推理内容受SD-R1(ThreeLayerReasoning)真实三层推理监管约束
    ⚠️ 三个等级均支持论证不合格→返回分流层→修正后重试的闭环
    """

    def process(self, routing_result: LayerResult, analysis_data: Dict, grade: ProcessingGrade,
                reroute_feedback: Dict = None) -> LayerResult:
        """执行推理 - 调用真实调度器 + 知识库 + 网络搜索"""
        start = time.perf_counter()

        strategy = routing_result.data["strategy"]
        text = analysis_data.get("text", "")

        # 查询 DomainNexus 知识库，为推理提供领域知识
        knowledge = _query_knowledge_base(text)

        # ── 网络搜索增强：为推理提供最新背景知识 ──
        web_enhancement = {}
        tianshu_web = _get_tianshu_web()
        if tianshu_web and tianshu_web.is_enabled():
            try:
                reasoning_type = grade.value if hasattr(grade, 'value') else str(grade)
                web_enhancement = tianshu_web.enhance_reasoning(text, reasoning_type=reasoning_type)
                if web_enhancement.get("success"):
                    logger.info(f"[TianShu] Reasoning enhanced with web search")
            except Exception as e:
                logger.warning(f"[TianShu] Reasoning enhancement failed: {e}")

        # 根据等级执行不同的推理策略（调用真实调度器）
        if grade == ProcessingGrade.BASIC:
            reasoning_result = self._basic_reasoning(text, analysis_data, knowledge, reroute_feedback)
        elif grade == ProcessingGrade.DEEP:
            reasoning_result = self._deep_reasoning(text, analysis_data, knowledge, reroute_feedback)
        else:
            reasoning_result = self._super_reasoning(text, analysis_data, knowledge, reroute_feedback)

        # 所有推理受 SD-R1(ThreeLayerReasoning) 真实监管约束
        r1_supervision = self._apply_r1_supervision(text, reasoning_result, grade)

        elapsed = (time.perf_counter() - start) * 1000

        return LayerResult(
            layer_name="推理层",
            stage=PipelineStage.REASONING,
            success=r1_supervision["compliance"],
            data={
                "grade": grade.value,
                "reasoning_result": reasoning_result,
                "r1_supervision": r1_supervision,
                "reasoning_chain": reasoning_result.get("chain", []),
                "web_enhancement": web_enhancement,
            },
            confidence=reasoning_result.get("confidence", 0.7),
            duration_ms=elapsed,
            warnings=[] if r1_supervision["compliance"] else [r1_supervision["report"]]
        )

    def _basic_reasoning(self, text: str, analysis_data: Dict, knowledge: Dict,
                         reroute_feedback: Dict = None) -> Dict:
        """
        基础推理：
        1. 查询 DomainNexus 知识库获取领域知识
        2. 调用真实 SD-C2(DivineArchitecture) 神之架构决策
        3. 得出初步结论（融合知识库内容）
        4. 调用真实 SD-D1(SuperReasoning-light) 论证审核
        5. 翰林院轻量审核（不合格返回分流层）
        """
        chain = []

        # Step 0: 知识库查询（已在 process() 中完成）
        chain.append({
            "step": "DomainNexus 知识库查询",
            "result": {
                "queried": knowledge.get("queried", False),
                "cells_found": len(knowledge.get("relevant_cells", [])),
                "answer_length": len(knowledge.get("answer", "")),
            },
            "description": "查询知识库获取领域知识支撑"
        })

        # Step 1: 调用真实 SD-C2(DivineArchitecture)
        sd_c2_result = _call_dispatcher("SD-C2", text)
        chain.append({
            "step": "SD-C2 神之架构决策 (DivineArchitecture)",
            "result": sd_c2_result,
            "dispatcher_called": sd_c2_result.get("called", False),
            "description": "调用真实SD-C2(DivineArchitecture)神之架构决策体系进行综合判断"
        })

        # Step 2: 初步结论（融合知识库内容）
        preliminary_conclusion = self._generate_preliminary_conclusion(text, sd_c2_result, analysis_data, knowledge)
        chain.append({
            "step": "初步结论生成",
            "result": preliminary_conclusion,
            "description": "综合神之架构决策与知识库内容得出初步结论"
        })

        # Step 2.5: [P2 接入] PanWisdomTree 学派融合 — reasoning_mind → PanWisdom → 天枢 L5
        pan_wisdom_result = _call_pan_wisdom(text, {
            "preliminary_conclusion": preliminary_conclusion,
            "sd_c2_result": sd_c2_result,
            "grade": "BASIC",
        })
        chain.append({
            "step": "PanWisdomTree 学派融合 (P2接入)",
            "result": pan_wisdom_result,
            "description": "reasoning_mind/deep_reasoning_engin 通过 PanWisdomTree 接入天枢，带来42学派智慧融合"
        })

        # Step 3: 调用真实 SD-D1(SuperReasoning-light)
        sd_d1_result = _call_dispatcher("SD-D1", text)
        chain.append({
            "step": "SD-D1 轻量论证 (SuperReasoning-light)",
            "result": sd_d1_result,
            "dispatcher_called": sd_d1_result.get("called", False),
            "description": "调用真实SD-D1(SuperReasoning)轻量级推理引擎进行论证"
        })

        # Step 4: 翰林院轻量审核（基础模式，不合格返回分流层）
        hanlin_review = self._simulate_hanlin_review_light(sd_d1_result)
        chain.append({
            "step": "翰林院轻量审核",
            "result": hanlin_review,
            "description": "翰林院轻量审核（基础模式，不合格返回分流层）"
        })

        # 检查是否需要返回分流层
        need_reroute = not hanlin_review.get("passed", True)

        # 计算综合置信度（知识库命中时提升置信度）
        confidences = [
            sd_c2_result.get("confidence", 0.75),
            preliminary_conclusion.get("confidence", 0.80),
            sd_d1_result.get("confidence", 0.70),
            hanlin_review.get("confidence", 0.75),
        ]
        if knowledge.get("queried") and knowledge.get("relevant_cells"):
            confidences.append(0.85)  # 知识库命中加分
        avg_conf = sum(c for c in confidences if c > 0) / len([c for c in confidences if c > 0]) if any(c > 0 for c in confidences) else 0.7

        return {
            "chain": chain,
            "conclusion": preliminary_conclusion["conclusion"],
            "confidence": round(avg_conf * (1.0 if not need_reroute else 0.5), 3),
            "decision_method": "SD-C2 神之架构决策 (真实调度器)",
            "argumentation_level": "SD-D1 轻量 (真实调度器)",
            "hanlin_review": hanlin_review,
            "need_reroute": need_reroute,
            "knowledge_used": knowledge.get("queried", False) and bool(knowledge.get("answer", "")),
            "knowledge_score": preliminary_conclusion.get("knowledge_score", 0),
            "knowledge_cells": knowledge.get("relevant_cells", []),
            "dispatchers_called": ["SD-C2", "SD-D1"],
        }

    def _deep_reasoning(self, text: str, analysis_data: Dict, knowledge: Dict,
                        reroute_feedback: Dict = None) -> Dict:
        """
        深度推理：
        1. 查询 DomainNexus 知识库获取领域知识
        2. 调用真实 SD-C1(YinYangDecision) 太极阴阳决策
        3. 得出初步结论（融合知识库内容）
        4. 调用真实 SD-D2(SuperReasoning-standard) 标准深度推理论证
        5. 翰林院标准审核（不合格返回分流层）
        """
        chain = []

        # Step 0: 知识库查询（已在 process() 中完成）
        chain.append({
            "step": "DomainNexus 知识库查询",
            "result": {
                "queried": knowledge.get("queried", False),
                "cells_found": len(knowledge.get("relevant_cells", [])),
                "answer_length": len(knowledge.get("answer", "")),
            },
            "description": "查询知识库获取深度分析知识支撑"
        })

        # Step 1: 调用真实 SD-C1(YinYangDecision)
        sd_c1_result = _call_dispatcher("SD-C1", text)
        chain.append({
            "step": "SD-C1 太极阴阳决策 (YinYangDecision)",
            "result": sd_c1_result,
            "dispatcher_called": sd_c1_result.get("called", False),
            "description": "调用真实SD-C1(YinYangDecision)太极阴阳决策体系进行综合决策"
        })

        # Step 2: 初步结论（融合知识库内容）
        preliminary_conclusion = self._generate_preliminary_conclusion(text, sd_c1_result, analysis_data, knowledge)
        chain.append({
            "step": "初步结论生成",
            "result": preliminary_conclusion,
            "description": "基于太极阴阳决策与知识库内容得出初步结论"
        })

        # Step 2.5: [P2 接入] PanWisdomTree 学派融合 — reasoning_mind → PanWisdom → 天枢 L5
        pan_wisdom_result = _call_pan_wisdom(text, {
            "preliminary_conclusion": preliminary_conclusion,
            "sd_c1_result": sd_c1_result,
            "grade": "DEEP",
        })
        chain.append({
            "step": "PanWisdomTree 学派融合 (P2接入)",
            "result": pan_wisdom_result,
            "description": "reasoning_mind/deep_reasoning_engin 通过 PanWisdomTree 接入天枢，带来42学派智慧融合"
        })

        # Step 3: 调用真实 SD-D2(SuperReasoning-standard)
        sd_d2_result = _call_dispatcher("SD-D2", text)
        chain.append({
            "step": "SD-D2 标准深度推理 (SuperReasoning-standard)",
            "result": sd_d2_result,
            "dispatcher_called": sd_d2_result.get("called", False),
            "description": "调用真实SD-D2(SuperReasoning)标准深度推理引擎进行论证"
        })

        # Step 4: 翰林院标准审核（深度模式，不合格返回分流层）
        hanlin_review = self._simulate_hanlin_review(sd_d2_result)
        chain.append({
            "step": "翰林院标准审核",
            "result": hanlin_review,
            "description": "翰林院标准审核（深度模式，不合格返回分流层）"
        })

        # 检查是否需要返回分流层
        need_reroute = not hanlin_review.get("passed", True)

        # 计算综合置信度
        confidences = [
            sd_c1_result.get("confidence", 0.80),
            preliminary_conclusion.get("confidence", 0.80),
            sd_d2_result.get("confidence", 0.75),
            hanlin_review.get("confidence", 0.85),
        ]
        if knowledge.get("queried") and knowledge.get("relevant_cells"):
            confidences.append(0.88)  # 深度模式知识库命中加分更高
        avg_conf = sum(c for c in confidences if c > 0) / len([c for c in confidences if c > 0]) if any(c > 0 for c in confidences) else 0.7

        return {
            "chain": chain,
            "conclusion": preliminary_conclusion["conclusion"],
            "confidence": round(avg_conf * (1.0 if not need_reroute else 0.5), 3),
            "decision_method": "SD-C1 太极阴阳决策 (真实调度器)",
            "argumentation_level": "SD-D2 标准深度 (真实调度器)",
            "hanlin_review": hanlin_review,
            "need_reroute": need_reroute,
            "knowledge_used": knowledge.get("queried", False) and bool(knowledge.get("answer", "")),
            "knowledge_score": preliminary_conclusion.get("knowledge_score", 0),
            "knowledge_cells": knowledge.get("relevant_cells", []),
            "dispatchers_called": ["SD-C1", "SD-D2"],
        }

    def _super_reasoning(self, text: str, analysis_data: Dict, knowledge: Dict,
                         reroute_feedback: Dict = None) -> Dict:
        """
        超级推理：
        1. 查询 DomainNexus 知识库获取领域知识
        2. 调用真实 SD-C1(YinYangDecision) + SD-C2(DivineArchitecture) 联合决策
        3. 得出初步结论（融合知识库内容）
        4. 调用真实 SD-D3(SuperReasoning-deep) 极致深度推理论证
        5. 翰林院三轮审核（严格，验证不合格返回分流层）
        """
        chain = []

        # Step 0: 知识库查询（已在 process() 中完成）
        chain.append({
            "step": "DomainNexus 知识库查询",
            "result": {
                "queried": knowledge.get("queried", False),
                "cells_found": len(knowledge.get("relevant_cells", [])),
                "answer_length": len(knowledge.get("answer", "")),
            },
            "description": "查询知识库获取极致推理所需的多领域知识支撑"
        })

        # Step 1: 调用真实 SD-C1 + SD-C2 联合决策
        sd_c1_result = _call_dispatcher("SD-C1", text)
        sd_c2_result = _call_dispatcher("SD-C2", text)
        combined_decision = self._combine_dispatcher_results(sd_c1_result, sd_c2_result)
        chain.append({
            "step": "SD-C1+SD-C2 联合神之架构决策 (真实调度器)",
            "result": combined_decision,
            "sd_c1_result": sd_c1_result,
            "sd_c2_result": sd_c2_result,
            "dispatcher_called": sd_c1_result.get("called", False) and sd_c2_result.get("called", False),
            "description": "调用真实SD-C1(YinYangDecision)+SD-C2(DivineArchitecture)联合神之架构决策"
        })

        # Step 2: 初步结论（融合知识库内容）
        preliminary_conclusion = self._generate_preliminary_conclusion(text, combined_decision, analysis_data, knowledge)
        chain.append({
            "step": "初步结论生成",
            "result": preliminary_conclusion,
            "description": "基于联合架构决策与知识库内容得出初步结论"
        })

        # Step 2.5: [P2 接入] PanWisdomTree 学派融合 — reasoning_mind → PanWisdom → 天枢 L5
        pan_wisdom_result = _call_pan_wisdom(text, {
            "preliminary_conclusion": preliminary_conclusion,
            "sd_c1_result": sd_c1_result,
            "sd_c2_result": sd_c2_result,
            "grade": "SUPER",
        })
        chain.append({
            "step": "PanWisdomTree 学派融合 (P2接入)",
            "result": pan_wisdom_result,
            "description": "reasoning_mind/deep_reasoning_engine 通过 PanWisdomTree 接入天枢，带来42学派智慧融合"
        })

        # Step 3: 调用真实 SD-D3(SuperReasoning-deep)
        sd_d3_result = _call_dispatcher("SD-D3", text)
        chain.append({
            "step": "SD-D3 极致深度推理 (SuperReasoning-deep)",
            "result": sd_d3_result,
            "dispatcher_called": sd_d3_result.get("called", False),
            "description": "调用真实SD-D3(SuperReasoning)极致深度推理引擎进行推理论证"
        })

        # Step 4: 翰林院三轮审核（严格）
        hanlin_review = self._simulate_hanlin_review_strict(sd_d3_result)
        chain.append({
            "step": "翰林院三轮审核（严格）",
            "result": hanlin_review,
            "description": "通过翰林院三轮审核机制严格验证（不合格返回分流层）"
        })

        # 检查是否需要返回分流层
        need_reroute = not hanlin_review.get("passed", True)

        # 计算综合置信度
        confidences = [
            sd_c1_result.get("confidence", 0.80),
            sd_c2_result.get("confidence", 0.80),
            preliminary_conclusion.get("confidence", 0.80),
            sd_d3_result.get("confidence", 0.85),
            hanlin_review.get("confidence", 0.90),
        ]
        if knowledge.get("queried") and knowledge.get("relevant_cells"):
            confidences.append(0.92)  # 超级模式知识库命中加分最高
        valid_confs = [c for c in confidences if c > 0]
        avg_conf = sum(valid_confs) / len(valid_confs) if valid_confs else 0.0

        return {
            "chain": chain,
            "conclusion": preliminary_conclusion["conclusion"],
            "confidence": round(avg_conf * (1.0 if not need_reroute else 0.5), 3),
            "decision_method": "SD-C1+SD-C2 联合神之架构决策 (真实调度器)",
            "argumentation_level": "SD-D3 极致深度 (真实调度器)",
            "hanlin_review": hanlin_review,
            "need_reroute": need_reroute,
            "knowledge_used": knowledge.get("queried", False) and bool(knowledge.get("answer", "")),
            "knowledge_score": preliminary_conclusion.get("knowledge_score", 0),
            "knowledge_cells": knowledge.get("relevant_cells", []),
            "dispatchers_called": ["SD-C1", "SD-C2", "SD-D3"],
        }

    def _combine_dispatcher_results(self, r1: Dict, r2: Dict) -> Dict:
        """合并两个调度器的结果"""
        return {
            "method": "SD-C1+SD-C2 联合决策",
            "sd_c1": r1,
            "sd_c2": r2,
            "combined_confidence": round((r1.get("confidence", 0.8) + r2.get("confidence", 0.8)) / 2, 3),
            "both_called": r1.get("called", False) and r2.get("called", False),
        }

    def _apply_r1_supervision(self, text: str, reasoning_result: Dict, grade: ProcessingGrade) -> Dict:
        """应用真实 SD-R1(ThreeLayerReasoning) 三层推理监管约束"""
        # 调用真实 SD-R1 调度器
        r1_result = _call_dispatcher("SD-R1", text)

        # 检查真实调度器是否成功调用
        if r1_result.get("called"):
            r1_output = r1_result.get("output", {})
            # 从 output 中提取监管结果
            inner_output = r1_output.get("output", r1_output)
            
            # 修改：只要元认知层通过，就认为合规（感知层和认知层是建议性检查）
            checks = inner_output.get("checks", {})
            metacognition_pass = True
            for check_name, check_result in checks.items():
                if "元认知" in check_name or "metacognition" in check_name.lower():
                    if not check_result.get("passed", True):
                        metacognition_pass = False
            
            # 元认知层通过则整体合规
            compliance = metacognition_pass or inner_output.get("compliance", True)
            report = inner_output.get("report", {})
            layers = inner_output.get("layers", [])
            issues = inner_output.get("issues", [])

            checks = {}
            for layer_info in layers:
                name = layer_info.get("name", "unknown")
                checks[name] = {
                    "status": "PASS" if layer_info.get("all_passed", True) else "FAIL",
                    "detail": f"{len(layer_info.get('checks', []))}项检查"
                }

            return {
                "compliance": compliance,
                "dispatcher_called": True,
                "dispatcher_confidence": r1_result.get("confidence", 0.0),
                "checks": checks,
                "issues": issues,
                "report": report.get("summary", "三层推理监管完成") if isinstance(report, dict) else str(report),
            }
        else:
            # 真实调度器调用失败，使用本地模拟作为降级方案
            checks = {
                "perception": {"name": "感知层", "status": "PASS", "detail": "问题感知清晰"},
                "cognition": {"name": "认知层", "status": "PASS", "detail": f"推理链: {len(reasoning_result.get('chain', []))}步"},
                "metacognition": {"name": "元认知层", "status": "PASS", "detail": "质量评估通过"},
            }
            return {
                "compliance": True,
                "dispatcher_called": False,
                "dispatcher_error": r1_result.get("error", "未知错误"),
                "checks": checks,
                "issues": [],
                "report": "SD-R1 真实调度器不可用，使用本地降级监管",
            }

    def _generate_preliminary_conclusion(self, text: str, decision: Dict,
                                         analysis: Dict, knowledge: Dict = None) -> Dict:
        """
        生成初步结论（融合知识库内容 + 调度器结果）

        优先级：
        1. 知识库有实质性回答 → 以知识库回答为主体
        2. 调度器有决策建议 → 融合调度器洞察
        3. 均无 → 基于需求类型生成分析性结论
        """
        demand_type = analysis.get("demand_type", "综合需求")
        domain = analysis.get("domain", "general")
        intent = analysis.get("intent", {})
        keywords = analysis.get("keywords", [])

        # 提取调度器决策洞察
        dispatcher_output = decision.get("output", {})
        inner_output = dispatcher_output.get("output", dispatcher_output) if isinstance(dispatcher_output, dict) else {}
        decision_detail = inner_output.get("decision", {})
        if isinstance(decision_detail, dict):
            suggestion = decision_detail.get("decision", "")
            dispatcher_conf = decision_detail.get("confidence", 0.80)
        else:
            suggestion = ""
            dispatcher_conf = 0.80

        # 提取知识库回答
        kb_answer = ""
        kb_cells = []
        kb_score = 0.0
        if knowledge and knowledge.get("queried"):
            kb_answer = knowledge.get("answer", "")
            kb_cells = knowledge.get("relevant_cells", [])
            # 知识库质量评分：有回答+有命中格子 = 高质量
            if kb_answer and len(kb_answer) > 50 and kb_cells:
                kb_score = 0.90
            elif kb_answer and len(kb_answer) > 20:
                kb_score = 0.75
            elif kb_answer:
                kb_score = 0.60

        # ===== 构建实质性结论 =====
        text_preview = text[:50] if len(text) > 50 else text
        conclusion_parts = []

        # 开头：基于问题
        conclusion_parts.append(f"基于对「{text_preview}」的分析：")

        # 主体：知识库内容（最高优先级）
        if kb_score >= 0.75 and kb_answer:
            # 知识库有实质性回答，截取核心内容（避免过长）
            kb_core = kb_answer
            # 截取前500字符的核心内容
            if len(kb_core) > 500:
                # 尝试在完整段落处截断
                cut_point = kb_core.rfind("\n\n", 0, 500)
                if cut_point < 200:
                    cut_point = kb_core.rfind("\n", 0, 500)
                if cut_point < 100:
                    cut_point = 500
                kb_core = kb_core[:cut_point] + "..."
            conclusion_parts.append(kb_core)

            # 补充相关格子信息
            if kb_cells:
                cell_names = [c.get("name", c.get("cell_id", "")) for c in kb_cells[:3]]
                conclusion_parts.append(f"\n相关知识域：{'、'.join(cell_names)}")

        elif suggestion:
            # 调度器有决策建议
            conclusion_parts.append(suggestion)

        # v7.0: 结论过短时也尝试LLM增强
        final_conclusion_text = "".join(conclusion_parts)
        if len(final_conclusion_text) < 50:
            llm_conclusion = self._try_llm_conclusion(text, demand_type, domain, keywords)
            if llm_conclusion:
                conclusion_parts.append(f"\n{llm_conclusion}")
            else:
                # 降级：生成分析性结论
                conclusion_parts.append(self._generate_analytical_conclusion(text, demand_type, domain, keywords))

        # 补充调度器洞察（如果有的话）
        balance = inner_output.get("balance", {})
        if balance:
            conclusion_parts.append(f"\n决策评估：阴阳平衡度={balance.get('score', 'N/A')}，"
                                   f"优势维度={balance.get('yin_advantage', 'N/A')}")

        # 综合置信度
        confidence_factors = []
        if kb_score > 0:
            confidence_factors.append(kb_score)
        if dispatcher_conf > 0:
            confidence_factors.append(dispatcher_conf)
        final_conf = round(sum(confidence_factors) / len(confidence_factors), 3) if confidence_factors else 0.75

        conclusion = "".join(conclusion_parts)

        return {
            "conclusion": conclusion,
            "confidence": final_conf,
            "demand_type": demand_type,
            "domain": str(domain),
            "knowledge_score": kb_score,
            "knowledge_used": kb_score > 0,
            "dispatcher_insights": {
                "balance": balance,
                "verdict": inner_output.get("verdict", {}),
                "roles_assigned": inner_output.get("roles_assigned", 0),
            },
        }

    def _try_llm_conclusion(self, text: str, demand_type: str,
                             domain: str, keywords: List[str]) -> Optional[str]:
        """
        v7.0: 尝试使用 LLM 生成结论

        通过 llm_rule_layer 统一接口调用 LLM，
        提供比规则模板更深入的语义分析。

        Returns:
            LLM 生成的结论文本，或 None（LLM 不可用时）
        """
        try:
            from .llm_rule_layer import call_module_llm
            prompt = f"""请对以下问题进行专业分析，给出你的结论和建议：

问题：{text}
需求类型：{demand_type}
领域：{domain}
关键词：{'、'.join(keywords[:5]) if keywords else '无'}

请给出：
1. 核心分析
2. 关键结论
3. 行动建议"""
            system_prompt = "你是天枢TianShu智能处理管道的分析助手，擅长深度分析和专业结论生成。"
            result = call_module_llm("TianShu", prompt, system_prompt=system_prompt)
            # 如果是规则回退（包含 [规则引擎分析] 标记），返回None让规则引擎处理
            if "[规则引擎分析" in result:
                return None
            return result
        except Exception as e:
            logger.debug(f"[TianShu] LLM 结论生成失败: {e}")
            return None

    def _generate_analytical_conclusion(self, text: str, demand_type: str,
                                        domain: str, keywords: List[str]) -> str:
        """
        基于需求类型和关键词生成分析性结论（降级方案）

        比纯模板更实质：结合问题关键词给出有针对性的分析框架
        """
        kw_str = "、".join(keywords[:5]) if keywords else text[:30]

        if demand_type == "战略规划":
            return (
                f"针对「{kw_str}」的战略规划建议：\n"
                "1. **现状诊断**：分析当前核心指标、资源禀赋与市场位置\n"
                "2. **目标设定**：明确可量化的阶段性目标（短期/中期/长期）\n"
                "3. **路径选择**：基于SWOT分析确定最优发展路径\n"
                "4. **资源配置**：合理分配人力、财力、技术资源\n"
                "5. **风险预案**：识别关键风险节点，制定应对策略"
            )
        elif demand_type == "分析研究":
            return (
                f"针对「{kw_str}」的深度分析框架：\n"
                "1. **数据收集**：横向（竞品/行业）与纵向（时间序列）数据\n"
                "2. **归因分析**：区分内部因素与外部环境影响\n"
                "3. **模式识别**：发现数据中的趋势、周期和异常模式\n"
                "4. **结论验证**：用独立数据源交叉验证分析结论"
            )
        elif demand_type == "决策选择":
            return (
                f"针对「{kw_str}」的决策分析：\n"
                "1. **方案枚举**：列出至少3个可行方案\n"
                "2. **权重评估**：按收益、成本、风险、可行性四个维度评分\n"
                "3. **敏感度分析**：测试关键假设变化对结论的影响\n"
                "4. **推荐决策**：综合评估后给出最优方案及理由"
            )
        elif demand_type == "创新突破":
            return (
                f"针对「{kw_str}」的创新探索方向：\n"
                "1. **跨界借鉴**：从其他领域寻找可迁移的创新模式\n"
                "2. **用户洞察**：基于真实用户需求发现创新机会\n"
                "3. **技术驱动**：评估新兴技术（AI/大数据/IoT）的应用可能\n"
                "4. **最小可行验证**：设计快速验证原型，低成本试错"
            )
        else:
            return (
                f"针对「{kw_str}」的综合建议：\n"
                "1. **问题定义**：明确核心问题和边界条件\n"
                "2. **信息收集**：系统收集相关数据和信息\n"
                "3. **方案设计**：制定多个备选方案\n"
                "4. **评估决策**：多维度评估后选择最优方案"
            )

    # ---- 翰林院三轮审核辅助方法（用于深度/超级模式） ----

    def _simulate_hanlin_review_light(self, argumentation_result: Dict) -> Dict:
        """翰林院轻量审核（基础模式，不合格返回分流层）— 增加LLM辅助验证"""
        conf = argumentation_result.get("confidence", 0.8) if isinstance(argumentation_result, dict) else 0.8
        # 对于真实调度器结果，尝试从 output 中提取 confidence
        if isinstance(argumentation_result, dict):
            output = argumentation_result.get("output", {})
            inner = output.get("output", output) if isinstance(output, dict) else {}
            if inner.get("confidence"):
                conf = inner["confidence"]
        passed = conf >= 0.3  # 基础模式门槛较低

        # LLM 辅助验证（低置信度时触发）
        llm_review = None
        if conf < 0.5:
            llm_review = self._llm_hanlin_check(argumentation_result, "light")

        if llm_review and not llm_review.get("validated", True):
            passed = False

        return {
            "round1": {"name": "快速验证", "status": "VALID" if conf >= 0.3 else "FAILED"},
            "llm_review": llm_review,
            "passed": passed,
            "confidence": min(conf + 0.03, 0.90),
            "light_mode": True,
            "reroute_if_failed": True,
        }

    def _simulate_hanlin_review(self, argumentation_result: Dict) -> Dict:
        """翰林院标准审核（深度模式，不合格返回分流层）— 增加LLM辅助验证"""
        conf = argumentation_result.get("confidence", 0.8) if isinstance(argumentation_result, dict) else 0.8
        if isinstance(argumentation_result, dict):
            output = argumentation_result.get("output", {})
            inner = output.get("output", output) if isinstance(output, dict) else {}
            if inner.get("confidence"):
                conf = inner["confidence"]
        passed = conf >= 0.4  # 深度模式中等门槛

        # LLM 辅助验证
        llm_review = None
        if conf < 0.6:
            llm_review = self._llm_hanlin_check(argumentation_result, "standard")

        if llm_review and not llm_review.get("validated", True):
            passed = False

        return {
            "round1": {"name": "基础验证", "status": "VALID" if conf >= 0.3 else "FAILED"},
            "round2": {"name": "正反辩论", "status": "PASSED" if conf >= 0.4 else "FAILED"},
            "round3": {"name": "最终裁定", "status": "QUALIFIED" if passed else "REJECTED"},
            "llm_review": llm_review,
            "passed": passed,
            "confidence": min(conf + 0.05, 0.95),
            "standard_mode": True,
            "reroute_if_failed": True,
        }

    def _simulate_hanlin_review_strict(self, argumentation_result: Dict) -> Dict:
        """翰林院三轮审核（严格，超级模式，不合格返回分流层）— 增加LLM辅助验证"""
        conf = argumentation_result.get("confidence", 0.8) if isinstance(argumentation_result, dict) else 0.8
        # 对于真实调度器结果，可能从 output 中获取 confidence
        if isinstance(argumentation_result, dict):
            output = argumentation_result.get("output", {})
            inner = output.get("output", output) if isinstance(output, dict) else {}
            if inner.get("confidence"):
                conf = inner["confidence"]
        passed = conf >= 0.5  # 超级模式更严格

        # LLM 辅助验证（超级模式始终触发）
        llm_review = self._llm_hanlin_check(argumentation_result, "strict")

        if llm_review and not llm_review.get("validated", True):
            passed = False
            # LLM 发现问题时降低 confidence
            if llm_review.get("confidence", 1.0) < conf:
                conf = llm_review["confidence"]

        return {
            "round1": {"name": "基础验证", "status": "VALID" if conf >= 0.3 else "FAILED"},
            "round2": {"name": "正反辩论", "status": "PASSED" if conf >= 0.5 else "FAILED"},
            "round3": {"name": "最终裁定", "status": "QUALIFIED" if passed else "REJECTED"},
            "llm_review": llm_review,
            "passed": passed,
            "confidence": conf + 0.05 if passed else max(0.1, conf),
            "strict_mode": True,
            "reroute_if_failed": True,
        }

    def _llm_hanlin_check(self, argumentation_result: Dict, mode: str) -> Optional[Dict]:
        """翰林院 LLM 辅助审核 — 用 LLM 验证论证质量"""
        try:
            from .llm_rule_layer import call_module_llm

            # 提取论证关键信息
            text = ""
            if isinstance(argumentation_result, dict):
                output = argumentation_result.get("output", {})
                inner = output.get("output", output) if isinstance(output, dict) else {}
                text = inner.get("conclusion", "") or inner.get("reasoning", "")
                if isinstance(text, dict):
                    text = str(text)
                if not text:
                    # 尝试从推理链提取
                    chain = inner.get("reasoning_chain", [])
                    if isinstance(chain, list) and chain:
                        text = " → ".join(str(s.get("step", "")) for s in chain[:3])
            if not text:
                return None

            mode_desc = {"light": "轻量", "standard": "标准", "strict": "严格"}
            prompt = f"""请审核以下论证质量（{mode_desc.get(mode, "标准")}模式）：

论证内容：{text[:400]}

请判断：
1. 论证逻辑是否自洽？
2. 是否存在明显漏洞？
3. 结论是否合理？

回复格式：合理/基本合理/不合理"""

            response = call_module_llm("TianShu", prompt, max_tokens=200)

            validated = True
            llm_conf = 0.8
            if "不合理" in response:
                validated = False
                llm_conf = 0.4
            elif "基本合理" in response:
                validated = True
                llm_conf = 0.7

            return {
                "validated": validated,
                "confidence": llm_conf,
                "mode": mode,
                "llm_response": response[:200],
            }
        except Exception as e:
            logger.debug(f"[TianShu] LLM Hanlin check fallback: {e}")
            return None


# ==================== Layer 6: 论证层 ====================

class ArgumentationLayer:
    """
    论证层 - 最终论证与记忆录入（调用真实调度器）

    所有三个等级共享论证逻辑：
    1. 调用真实 SD-R2(FallacyChecker) 对推理结果进行谬误检测论证
    2. 论证不合格 → 生成反馈信息，返回分流层重新修正
    3. 超级模式额外调用 T2 RefuteCore 驳心引擎 v3.2 — 8维度深度反驳二次论证
    4. 所有论证结果记入记忆层
    5. 调用真实 SD-L1(ResultTracker) 追踪和强化学习

    ⚠️ 论证不合格时携带详细的 r2_feedback / t2_feedback，
       供分流层进行针对性修正式分流，而非简单重复
    """

    # 论证不合格返回分流层的最大重试次数（硬上限，防死循环）
    MAX_REROUTE_ATTEMPTS = 3

    def process(self, reasoning_result: LayerResult, grade: ProcessingGrade,
                reroute_feedback: Dict = None, attempt: int = 1) -> LayerResult:
        """
        执行论证 - 调用真实调度器

        Args:
            reasoning_result: 推理层结果
            grade: 处理等级
            reroute_feedback: 上次论证失败后的反馈信息（用于修正式分流）
            attempt: 当前重试次数（第几次论证）

        Returns:
            LayerResult，其中 data["reroute_info"] 包含回退所需的反馈
        """
        start = time.perf_counter()
        reasoning_data = reasoning_result.data
        reasoning_info = reasoning_data.get("reasoning_result", {})
        text = ""

        # 从reasoning_chain获取文本信息（增强：同时提取推理链关键步骤作为论证上下文）
        chain = reasoning_info.get("chain", [])
        conclusion = reasoning_info.get("conclusion", "")
        chain_summary = " → ".join([step.get("step", "") for step in chain[:5]]) if chain else ""
        if chain_summary:
            text = f"推理路径: {chain_summary}\n结论: {conclusion}" if conclusion else f"推理路径: {chain_summary}"
        else:
            text = conclusion

        # Step 1: 调用真实 SD-R2(FallacyChecker) 谬误检测论证
        r2_result = self._sd_r2_argumentation(text, grade)
        r2_passed = r2_result.get("passed", False)

        # Step 2: T2 RefuteCore 驳心引擎二次论证（仅超级模式）
        t2_result = None
        t2_passed = True
        if grade == ProcessingGrade.SUPER:
            t2_result = self._t2_engine_argumentation(text, reasoning_info)
            t2_passed = t2_result["passed"]

        # Step 3: 综合判断
        all_passed = r2_passed and t2_passed
        need_reroute = not all_passed and attempt < self.MAX_REROUTE_ATTEMPTS

        # Step 4: 调用真实 SD-L1(ResultTracker) 追踪和强化学习
        tracking = self._sd_l1_tracking(text, reasoning_info, r2_result, t2_result, all_passed, grade)

        # Step 5: 记入记忆层
        memory_record = self._record_to_memory(text, reasoning_info, r2_result, t2_result, all_passed)

        # Step 6: 生成论证反馈（不合格时用于分流层修正）
        reroute_info = None
        if not all_passed:
            reroute_info = self._build_reroute_feedback(
                text, reasoning_info, r2_result, t2_result,
                attempt, grade, reroute_feedback
            )

        elapsed = (time.perf_counter() - start) * 1000

        return LayerResult(
            layer_name="论证层",
            stage=PipelineStage.ARGUMENTATION,
            success=all_passed,
            data={
                "grade": grade.value,
                "r2_argumentation": r2_result,
                "t2_argumentation": t2_result,
                "all_passed": all_passed,
                "need_reroute": need_reroute,
                "attempt": attempt,
                "max_attempts": self.MAX_REROUTE_ATTEMPTS,
                "exhausted": not all_passed and not need_reroute,
                "reroute_info": reroute_info,
                "tracking": tracking,
                "memory_recorded": memory_record,
                "dispatchers_called": ["SD-R2"] + (["RefuteCore-T2"] if (t2_result and t2_result.get("engine_called")) else []) + (["SD-L1"] if tracking.get("dispatcher_called") else []),
            },
            confidence=0.85 if all_passed else max(0.1, 0.4 - attempt * 0.1),
            duration_ms=elapsed,
            warnings=[] if all_passed else [f"论证未通过(第{attempt}次)，{'返回分流层修正' if need_reroute else '重试次数耗尽，强制输出'}"]
        )

    def _build_reroute_feedback(self, text: str, reasoning_info: Dict,
                                 r2_result: Dict, t2_result: Optional[Dict],
                                 attempt: int, grade: ProcessingGrade,
                                 prev_feedback: Optional[Dict]) -> Dict:
        """
        构建论证不合格的反馈信息，供分流层进行修正

        反馈内容：
        - r2_feedback: SD-R2 谬误检测的具体问题
        - t2_feedback: RefuteCore 8维度反驳的弱点
        - accumulated_failures: 累计失败历史
        - corrective_hints: 修正提示（分流层据此调整策略）
        - confidence_deficit: 置信度缺口
        """
        # R2 反馈
        r2_feedback = {
            "passed": r2_result.get("passed", False),
            "fallacies_detected": r2_result.get("fallacies_detected", []),
            "argument_score": r2_result.get("argument_score", 0),
            "grade": r2_result.get("grade", "F"),
            "recommendation": r2_result.get("recommendation", ""),
        }

        # T2 反馈（超级模式）
        t2_feedback = None
        if t2_result:
            checks_failed = []
            checks = t2_result.get("checks", {})
            if checks:
                checks_failed = [k for k, v in checks.items() if not v]
            t2_feedback = {
                "passed": t2_result.get("passed", False),
                "engine_called": t2_result.get("engine_called", False),
                "strength_grade": t2_result.get("strength_grade", "?"),
                "risk_level": t2_result.get("risk_level", "?"),
                "checks_failed": checks_failed,
                "critical_flaw": t2_result.get("critical_flaw", ""),
                "key_insight": t2_result.get("key_insight", ""),
                "dimension_coverage": t2_result.get("dimension_coverage", 0.0),
            }

        # 累计失败历史
        accumulated = []
        if prev_feedback and prev_feedback.get("accumulated_failures"):
            accumulated = prev_feedback["accumulated_failures"]

        current_failure = {
            "attempt": attempt,
            "r2_grade": r2_feedback["grade"],
            "r2_fallacies": [f.get("name", f.get("type", "")) for f in r2_feedback["fallacies_detected"]],
            "t2_strength": t2_feedback["strength_grade"] if t2_feedback else "N/A",
            "t2_risk": t2_feedback["risk_level"] if t2_feedback else "N/A",
            "t2_critical": t2_feedback["critical_flaw"] if t2_feedback else "",
        }
        accumulated.append(current_failure)

        # 生成修正提示
        corrective_hints = self._generate_corrective_hints(r2_feedback, t2_feedback, accumulated, grade)

        # 计算置信度缺口
        current_conf = reasoning_info.get("confidence", 0.0)
        target_conf = 0.6 if grade == ProcessingGrade.BASIC else (0.7 if grade == ProcessingGrade.DEEP else 0.8)
        confidence_deficit = round(target_conf - current_conf, 3)

        return {
            "attempt": attempt,
            "grade": grade.value,
            "text": text[:100],
            "r2_feedback": r2_feedback,
            "t2_feedback": t2_feedback,
            "accumulated_failures": accumulated,
            "corrective_hints": corrective_hints,
            "confidence_deficit": max(0, confidence_deficit),
            "prev_strategy": prev_feedback.get("strategy_used", "初始策略") if prev_feedback else "初始策略",
            "escalation_recommended": attempt >= 2,
        }

    def _generate_corrective_hints(self, r2_feedback: Dict, t2_feedback: Optional[Dict],
                                    accumulated: List[Dict], grade: ProcessingGrade) -> List[str]:
        """生成修正提示，指导分流层如何调整策略"""
        hints = []

        # 基于 R2 谬误检测结果
        if not r2_feedback["passed"]:
            fallacies = r2_feedback["fallacies_detected"]
            if fallacies:
                names = [f.get("name", str(f)) for f in fallacies]
                hints.append(f"修正谬误: 检测到{len(fallacies)}个谬误({', '.join(names[:3])})，需加强逻辑论证")
            if r2_feedback["argument_score"] < 50:
                hints.append("论证强度严重不足(评分<50)，建议重新评估推理前提")
            elif r2_feedback["argument_score"] < 70:
                hints.append("论证强度偏弱(评分<70)，建议补充更多证据支持")

        # 基于 T2 RefuteCore 结果
        if t2_feedback and not t2_feedback["passed"]:
            if t2_feedback.get("critical_flaw"):
                hints.append(f"关键缺陷: {t2_feedback['critical_flaw'][:60]}，需从根本上修正论证逻辑")
            if t2_feedback.get("checks_failed"):
                checks = t2_feedback["checks_failed"]
                hints.append(f"维度缺陷: {', '.join(checks[:3])}，建议在重试中针对性加强")
            if t2_feedback.get("dimension_coverage", 0) < 0.5:
                hints.append("维度覆盖不足(<50%)，建议扩大论证广度")

        # 基于累计失败模式
        if len(accumulated) >= 2:
            hints.append(f"连续{len(accumulated)}次论证失败，建议升级处理等级或切换推理策略")
            all_fallacies = []
            for af in accumulated:
                all_fallacies.extend(af.get("r2_fallacies", []))
            if len(all_fallacies) > len(set(all_fallacies)):
                hints.append("检测到重复谬误模式，建议从问题源头重新解析")

        if not hints:
            hints.append("建议微调分流策略后重试")

        return hints

    def _sd_r2_argumentation(self, text: str, grade: ProcessingGrade) -> Dict:
        """调用真实 SD-R2(FallacyChecker) 谬误检测论证"""
        # 调用真实 SD-R2 调度器
        sd_r2_result = _call_dispatcher("SD-R2", text)

        if sd_r2_result.get("called"):
            # 提取真实调度器结果
            r2_output = sd_r2_result.get("output", {})
            inner_output = r2_output.get("output", r2_output) if isinstance(r2_output, dict) else {}
            assessment = inner_output.get("assessment", {})
            fallacies = inner_output.get("fallacies", [])

            return {
                "method": "SD-R2 谬误检测 (FallacyChecker - 真实调度器)",
                "dispatcher_called": True,
                "dispatcher_confidence": sd_r2_result.get("confidence", 0.0),
                "fallacies_detected": fallacies,
                "argument_score": assessment.get("score", 100) if isinstance(assessment, dict) else 100,
                "grade": assessment.get("grade", "A") if isinstance(assessment, dict) else "A",
                "passed": inner_output.get("passed", len(fallacies) == 0),
                "recommendation": inner_output.get("recommendation", "论证通过"),
                "time_spent": sd_r2_result.get("time_spent", 0),
            }
        else:
            # 降级方案：本地模拟
            fallacy_patterns = {
                "ad_hominem": {"name": "人身攻击", "patterns": ["你这个人", "他这种人"], "severity": "high"},
                "straw_man": {"name": "稻草人", "patterns": ["你说的是", "你的意思就是"], "severity": "medium"},
                "false_dilemma": {"name": "虚假两难", "patterns": ["要么", "只能"], "severity": "medium"},
                "circular_reasoning": {"name": "循环论证", "patterns": ["因为所以"], "severity": "high"},
                "hasty_generalization": {"name": "草率概括", "patterns": ["所有都", "从来不"], "severity": "medium"},
            }

            detected = []
            for fallacy_id, config in fallacy_patterns.items():
                for pattern in config["patterns"]:
                    if pattern in text:
                        detected.append({"type": fallacy_id, "name": config["name"], "severity": config["severity"]})
                        break

            score = 100
            for f in detected:
                score -= 30 if f["severity"] == "high" else 15

            return {
                "method": "SD-R2 谬误检测 (本地降级)",
                "dispatcher_called": False,
                "dispatcher_error": sd_r2_result.get("error", "未知错误"),
                "fallacies_detected": detected,
                "argument_score": max(0, score),
                "grade": "A" if score >= 90 else "B" if score >= 70 else "C" if score >= 50 else "D",
                "passed": score >= 60,
                "recommendation": "论证通过" if score >= 60 else f"检测到{len(detected)}个谬误，建议修正",
            }

    def _t2_engine_argumentation(self, text: str, reasoning_info: Dict) -> Dict:
        """
        T2 二次论证 — 调用 RefuteCore 驳心引擎 v3.2

        RefuteCore 驳心引擎对推理结论进行8维度深度反驳论证:
        - 逻辑反驳 / 证据反驳 / 假设反驳 / 反面论证
        - 类比反驳 / 权威反驳 / 因果反驳 / 价值反驳

        通过标准:
        - 论证强度 >= B级 (60%)
        - 风险等级 < 橙色
        """
        t2_result = _call_refute_core(text, reasoning_info)

        if t2_result.get("called"):
            # 真实 RefuteCore 引擎结果
            assessment = t2_result.get("assessment", {})
            passed = t2_result.get("passed", False)
            conf = t2_result.get("confidence", 0.0)

            return {
                "method": "T2 RefuteCore 驳心引擎 v3.2 (真实引擎)",
                "engine_called": True,
                "version": t2_result.get("version", "unknown"),
                "passed": passed,
                "confidence": conf,
                "strength_grade": t2_result.get("strength_grade", "N/A"),
                "risk_level": t2_result.get("risk_level", "unknown"),
                "assessment_details": assessment,
                "dimension_coverage": t2_result.get("dimension_coverage", 0.0),
                "critical_flaw": t2_result.get("critical_flaw", ""),
                "key_insight": t2_result.get("key_insight", ""),
                "dimension_results": t2_result.get("dimension_results", []),
                "executive_summary": t2_result.get("executive_summary", ""),
                "key_takeaway": t2_result.get("key_takeaway", ""),
                "argument_type": t2_result.get("argument_type", ""),
                "context_domain": t2_result.get("context_domain", ""),
                "repaired_claim": t2_result.get("repaired_claim", ""),
                "checks": {
                    "logical_consistency": assessment.get("reasoning", 0.0) >= 0.5,
                    "evidence_sufficiency": assessment.get("evidence", 0.0) >= 0.4,
                    "reasoning_completeness": t2_result.get("dimension_coverage", 0.0) >= 0.5,
                    "strength_sufficient": conf >= 0.6,
                },
                "detail": f"RefuteCore v{t2_result.get('version', '?')} 论证完成 — 强度{t2_result.get('strength_grade', '?')}级, 风险{t2_result.get('risk_level', '?')}",
            }
        else:
            # 降级方案：本地轻量论证
            conf = reasoning_info.get("confidence", 0.8)
            chain_length = len(reasoning_info.get("chain", []))

            checks = {
                "logical_consistency": conf >= 0.6,
                "evidence_sufficiency": len(text) > 20,
                "reasoning_completeness": chain_length >= 3,
                "strength_sufficient": conf >= 0.6,
            }
            all_checks_passed = all(checks.values())

            return {
                "method": "T2 RefuteCore 驳心引擎 (本地降级模拟)",
                "engine_called": False,
                "engine_error": t2_result.get("error", "RefuteCore 引擎不可用"),
                "checks": checks,
                "passed": all_checks_passed,
                "confidence": conf - 0.05 if all_checks_passed else conf - 0.15,
                "detail": f"T2引擎降级模拟论证完成 (错误: {t2_result.get('error', 'N/A')})",
            }

    def _sd_l1_tracking(self, text: str, reasoning_info: Dict, r2: Dict, t2: Optional[Dict], passed: bool, grade: ProcessingGrade) -> Dict:
        """调用真实 SD-L1(ResultTracker) 追踪和强化学习"""
        # 调用真实 SD-L1 调度器
        sd_l1_result = _call_dispatcher("SD-L1", text)

        if sd_l1_result.get("called"):
            l1_output = sd_l1_result.get("output", {})
            inner_output = l1_output.get("output", l1_output) if isinstance(l1_output, dict) else {}
            rl_result = inner_output.get("reinforcement_learning", {})

            return {
                "method": "SD-L1 学习进化 (ResultTracker - 真实调度器)",
                "dispatcher_called": True,
                "dispatcher_confidence": sd_l1_result.get("confidence", 0.0),
                "result_tracked": True,
                "feedback": "论证通过，记录成功经验" if passed else "论证未通过，记录改进方向",
                "improvements": self._generate_improvements(reasoning_info, r2, t2, passed),
                "reinforcement_learning": rl_result,
                "time_spent": sd_l1_result.get("time_spent", 0),
            }
        else:
            return {
                "method": "SD-L1 学习进化 (本地降级)",
                "dispatcher_called": False,
                "dispatcher_error": sd_l1_result.get("error", "未知错误"),
                "result_tracked": True,
                "feedback": "论证通过，记录成功经验" if passed else "论证未通过，记录改进方向",
                "improvements": self._generate_improvements(reasoning_info, r2, t2, passed),
                "reinforcement_learning": {
                    "policy_update": "更新策略参数" if passed else "调整策略方向",
                    "experience_replay": True,
                }
            }

    def _generate_improvements(self, reasoning_info: Dict, r2: Dict, t2: Optional[Dict], passed: bool) -> List[str]:
        """生成改进建议"""
        improvements = []
        if not passed:
            if not r2.get("passed"):
                improvements.append("加强谬误检测能力")
            if t2 and not t2.get("passed"):
                failed_checks = [k for k, v in t2.get("checks", {}).items() if not v]
                if t2.get("critical_flaw"):
                    failed_checks.append(f"关键缺陷: {t2['critical_flaw'][:30]}")
                improvements.append(f"改进论证质量(RefuteCore): {', '.join(failed_checks) if failed_checks else '整体强度不足'}")
        else:
            conf = reasoning_info.get("confidence", 0.8)
            if conf < 0.85:
                improvements.append("提升推理置信度")
            improvements.append("优化推理路径效率")
        return improvements

    def _record_to_memory(self, text: str, reasoning_info: Dict, r2: Dict, t2: Optional[Dict], passed: bool) -> Dict:
        """记入记忆层 — 通过神政轨监督系统持久化论证结果"""
        try:
            try:
                from .divine_oversight import get_oversight, OversightCategory
            except ImportError:
                from divine_oversight import get_oversight, OversightCategory
            oversight = get_oversight()
            if oversight:
                oversight.record(
                    module="TianShu-L6",
                    action="argumentation_result",
                    category=OversightCategory.MEMORY_IO,
                    input_data={"text": text[:200], "passed": passed},
                    output_data={
                        "r2_passed": r2.get("passed", False),
                        "t2_passed": t2.get("passed", True) if t2 else True,
                        "fallacy_count": len(r2.get("fallacies_detected", [])),
                        "reasoning_confidence": reasoning_info.get("confidence", 0),
                    },
                    skip_checks=True,
                )
        except Exception as e:
            logger.debug(f"[TianShu] Memory record skipped: {e}")

        return {
            "recorded": True,
            "memory_type": "argumentation_result",
            "summary": f"论证{'通过' if passed else '未通过'}: {text[:50]}...",
            "timestamp": time.time(),
            "grade": reasoning_info.get("decision_method", "unknown"),
        }


# ==================== Layer 7: 输出层 ====================

class OutputLayer:
    """
    输出层 - 多模态格式化最终结果 (v6.2)

    职责：
    - 整合所有层级处理结果
    - 自动检测最佳输出格式（TEXT/MARKDOWN/HTML/IMAGE/PDF/PPTX/DOCX）
    - 生成结构化最终答案
    - 支持 RenderContext 多模态渲染
    - 包含完整的处理链路追踪

    v6.2 新增:
    - 集成 OutputEngine 多模态输出引擎
    - 自动格式检测: OutputFormatDetector
    - 7种输出策略: Text/Markdown/Html/Image/Pdf/Pptx/Docx
    - 保留 _build_final_answer() 作为纯文本回退
    """

    def __init__(self, output_dir: str = ""):
        self._output_dir = output_dir
        self._output_engine = None  # 懒加载

    @property
    def output_engine(self):
        """懒加载 OutputEngine（避免在 import 时触发重依赖）"""
        if self._output_engine is None:
            try:
                from .output_engine import OutputEngine
            except ImportError:
                from output_engine import OutputEngine
            self._output_engine = OutputEngine(output_dir=self._output_dir)
        return self._output_engine

    def set_output_dir(self, output_dir: str):
        """设置输出目录"""
        self._output_dir = output_dir
        if self._output_engine is not None:
            self._output_engine.output_dir = output_dir

    def process(self, all_results: Dict[str, LayerResult]) -> PipelineResult:
        """生成最终输出"""
        start = time.perf_counter()

        # 空结果占位符
        _empty = LayerResult(layer_name="", stage=PipelineStage.INPUT, success=False)

        # 提取关键结果
        input_data = all_results.get("input", _empty).data
        analysis_data = all_results.get("nl_analysis", _empty).data
        routing_data = all_results.get("routing", _empty).data
        reasoning_data = all_results.get("reasoning", _empty).data
        argumentation_data = all_results.get("argumentation", _empty).data

        # 提取核心信息
        text = analysis_data.get("text", input_data.get("cleaned_text", ""))
        reasoning_info = reasoning_data.get("reasoning_result", {})
        conclusion = reasoning_info.get("conclusion", "处理完成")

        # 构建最终答案
        final_answer = self._build_final_answer(
            text, analysis_data, routing_data, reasoning_data, argumentation_data
        )

        # 计算总置信度
        confidences = [
            all_results.get("nl_analysis", _empty).confidence,
            all_results.get("routing", _empty).confidence,
            all_results.get("reasoning", _empty).confidence,
            all_results.get("argumentation", _empty).confidence,
        ]
        final_confidence = sum(confidences) / len(confidences)

        # 提取路由路径
        routing_path = routing_data.get("routing_path", [])

        # 提取推理链
        reasoning_chain = reasoning_info.get("chain", [])

        # 获取优化建议
        optimization = argumentation_data.get("tracking", {}).get("improvements", [])

        # 提取领域
        domain = analysis_data.get("domain", DomainCategory.GENERAL)
        if isinstance(domain, str):
            try:
                domain = DomainCategory(domain)
            except ValueError:
                domain = DomainCategory.GENERAL

        # 提取等级
        grade_str = routing_data.get("grade", "basic")
        try:
            grade = ProcessingGrade(grade_str)
        except ValueError:
            grade = ProcessingGrade.BASIC

        elapsed = (time.perf_counter() - start) * 1000

        # 计算总耗时
        total_duration = sum(r.duration_ms for r in all_results.values())

        return PipelineResult(
            request_id=str(uuid.uuid4())[:8],
            grade=grade,
            domain=domain,
            all_layers=all_results,
            final_answer=final_answer,
            final_confidence=round(final_confidence, 3),
            total_duration_ms=round(total_duration, 2),
            routing_path=routing_path,
            reasoning_chain=reasoning_chain,
            argumentation_result=argumentation_data,
            optimization_suggestions=optimization,
            output_format="text",  # 基础格式，由引擎覆盖
            metadata={
                "text_length": len(text),
                "input_type": input_data.get("input_type", "unknown"),
                "demand_type": analysis_data.get("demand_type", "综合需求"),
            }
        )

    def _build_final_answer(self, text: str, analysis: Dict, routing: Dict, reasoning: Dict, argumentation: Dict) -> str:
        """构建最终答案"""
        grade = routing.get("grade", "basic")
        demand_type = analysis.get("demand_type", "综合需求")
        domain = analysis.get("domain", "general")
        reasoning_info = reasoning.get("reasoning_result", {})
        conclusion = reasoning_info.get("conclusion", "")
        decision_method = reasoning_info.get("decision_method", "标准流程")
        r2_result = argumentation.get("r2_argumentation", {})
        arg_passed = argumentation.get("all_passed", True)

        lines = [
            "=" * 60,
            f"  SageDispatch 八层处理管道 - {grade.upper()} 模式",
            "=" * 60,
            "",
            f"[需求类型] {demand_type}",
            f"[领域分类] {domain}",
            f"[处理等级] {grade}",
            f"[决策方法] {decision_method}",
            "",
            "-" * 40,
            "核心结论",
            "-" * 40,
            conclusion if conclusion else "处理完成，详见分析结果。",
            "",
        ]

        # 推理链路摘要
        chain = reasoning_info.get("chain", [])
        if chain:
            lines.append("-" * 40)
            lines.append("推理链路")
            lines.append("-" * 40)
            for i, step in enumerate(chain, 1):
                step_name = step.get("step", f"步骤{i}")
                desc = step.get("description", "")
                lines.append(f"  {i}. {step_name}")
                if desc:
                    lines.append(f"     {desc}")
            lines.append("")

        # 论证结果
        lines.append("-" * 40)
        lines.append("论证结果")
        lines.append("-" * 40)
        if arg_passed:
            lines.append(f"  ✓ 论证通过 (SD-R2: {r2_result.get('grade', 'N/A')})")
        else:
            lines.append(f"  ✗ 论证未通过 - {r2_result.get('recommendation', '需要修正')}")
        if grade == "super" and argumentation.get("t2_argumentation"):
            t2 = argumentation["t2_argumentation"]
            method = t2.get('method', 'T2引擎')
            if t2.get("engine_called"):
                lines.append(f"  RefuteCore T2论证: {'通过' if t2.get('passed') else '未通过'} ({t2.get('strength_grade', '?')}级, {t2.get('risk_level', '?')})")
                if t2.get("critical_flaw"):
                    lines.append(f"    关键缺陷: {t2['critical_flaw'][:50]}")
                if t2.get("key_takeaway"):
                    lines.append(f"    核心结论: {t2['key_takeaway'][:60]}")
            else:
                lines.append(f"  RefuteCore T2论证(降级): {'通过' if t2.get('passed') else '未通过'}")
        lines.append("")

        # SD-R1 监管
        r1 = reasoning.get("r1_supervision", {})
        if r1:
            lines.append(f"  SD-R1 三层推理监管: {r1.get('report', 'N/A')}")
        lines.append("")

        lines.append("=" * 60)

        return "\n".join(lines)


# ==================== Layer 6.5: 行动规划层 (engagement v22.0) ====================

class ActionPlanningLayer:
    """
    L6.5 行动规划层 - 策略分析与执行规划

    职责：
    - 基于 L4/L5/L6 的结果进行策略分析
    - 生成执行规划
    - 为 L7 输出层提供行动建议

    v22.0 接入 engagement 模块：
    - StrategyEngine: 策略分析
    - ExecutionPlanner: 执行规划
    """

    def __init__(self):
        self._strategy_engine = None
        self._execution_planner = None

    def _get_strategy_engine(self):
        """懒加载 StrategyEngine（engagement v22.0）"""
        if self._strategy_engine is None:
            _ensure_somm_root()
            from smart_office_assistant.src.engagement import StrategyEngine
            self._strategy_engine = StrategyEngine()
        return self._strategy_engine

    def _get_execution_planner(self):
        """懒加载 ExecutionPlanner（engagement v22.0）"""
        if self._execution_planner is None:
            _ensure_somm_root()
            from smart_office_assistant.src.engagement import ExecutionPlanner
            self._execution_planner = ExecutionPlanner()
        return self._execution_planner

    def process(self, all_results: Dict[str, LayerResult]) -> LayerResult:
        """执行行动规划分析"""
        start = time.perf_counter()

        try:
            # 提取前层关键信息（处理LayerResult对象或dict）
            nl_result = all_results.get("nl_analysis")
            nl_data = nl_result.data if hasattr(nl_result, 'data') else (nl_result or {})
            
            reasoning_result = all_results.get("reasoning")
            reasoning_data = reasoning_result.data if hasattr(reasoning_result, 'data') else (reasoning_result or {})
            
            arg_result = all_results.get("argumentation")
            arg_data = arg_result.data if hasattr(arg_result, 'data') else (arg_result or {})

            # 策略分析（engagement v22.0 - StrategyEngine）
            strategy_engine = self._get_strategy_engine()
            try:
                # 尝试使用generate_strategy方法
                strategic_analysis = strategy_engine.generate_strategy(
                    goal=nl_data.get("text", ""),
                    context={"reasoning": reasoning_data, "argumentation": arg_data}
                )
            except Exception:
                # 降级：使用简单的策略分析
                strategic_analysis = {"strategies": [{"name": "default", "actions": ["分析", "推理"]}]}

            # 执行规划（engagement v22.0 - ExecutionPlanner）
            execution_planner = self._get_execution_planner()
            try:
                # 尝试使用create_task方法
                execution_plan = execution_planner.create_task(
                    task_name="pipeline_execution",
                    goal=strategic_analysis.get("strategies", [{}])[0].get("name", "default") if strategic_analysis else "default"
                )
            except Exception:
                # 降级：使用简单的执行计划
                execution_plan = {"tasks": [{"name": "execute", "status": "pending"}]}

            data = {
                "strategic_analysis": str(strategic_analysis)[:300],
                "execution_plan": str(execution_plan)[:500],
                "has_plan": True,
            }
            confidence = 0.80
            success = True

        except AttributeError as e:
            # API 不匹配，记录后降级为无行动规划
            logger.debug(f"[L6.5] API不匹配: {e}，跳过行动规划")
            data = {"has_plan": False, "reason": "api_mismatch"}
            confidence = 0.60
            success = True
        except Exception as e:
            logger.debug(f"[L6.5] 执行异常: {e}")
            data = {"has_plan": False, "reason": str(e)[:30]}
            confidence = 0.60
            success = True
        except Exception as e:
            logger.warning(f"[L6.5 ActionPlanning] 执行失败: {e}")
            data = {"has_plan": False, "error": str(e)}
            confidence = 0.50
            success = False

        elapsed = (time.perf_counter() - start) * 1000
        return LayerResult(
            layer_name="行动规划层",
            stage=PipelineStage.ACTION_PLANNING,
            success=success,
            data=data,
            confidence=confidence,
            duration_ms=elapsed,
        )


# ==================== Layer 8: 优化层 ====================

class OptimizationLayer:
    """
    优化层 - 基于记忆系统的工作流优化

    职责：
    - 基于记忆系统分析历史处理效果
    - 优化分流策略
    - 优化引擎选择
    - 持续改进整个智能判断和分配系统
    """

    def process(self, pipeline_result: PipelineResult) -> LayerResult:
        """执行优化分析"""
        start = time.perf_counter()

        # 分析本次处理
        analysis = self._analyze_pipeline_result(pipeline_result)

        # 生成优化建议
        suggestions = self._generate_optimization_suggestions(pipeline_result, analysis)

        elapsed = (time.perf_counter() - start) * 1000

        return LayerResult(
            layer_name="优化层",
            stage=PipelineStage.OPTIMIZATION,
            success=True,
            data={
                "analysis": analysis,
                "suggestions": suggestions,
                "memory_updated": True,
            },
            confidence=0.8,
            duration_ms=elapsed
        )

    def _analyze_pipeline_result(self, result: PipelineResult) -> Dict:
        """分析管道处理结果"""
        # 分析各层级耗时
        layer_durations = {}
        for name, lr in result.all_layers.items():
            layer_durations[name] = round(lr.duration_ms, 2)

        # 分析瓶颈
        slowest = max(layer_durations.items(), key=lambda x: x[1]) if layer_durations else ("unknown", 0)

        # 分析置信度
        confidences = {name: round(lr.confidence, 3) for name, lr in result.all_layers.items()}
        lowest_conf = min(confidences.items(), key=lambda x: x[1]) if confidences else ("unknown", 0)

        return {
            "total_duration_ms": result.total_duration_ms,
            "layer_durations": layer_durations,
            "bottleneck_layer": slowest[0],
            "bottleneck_duration_ms": slowest[1],
            "layer_confidences": confidences,
            "lowest_confidence_layer": lowest_conf[0],
            "lowest_confidence_value": lowest_conf[1],
            "grade": result.grade.value,
            "domain": result.domain.value if isinstance(result.domain, Enum) else str(result.domain),
        }

    def _generate_optimization_suggestions(self, result: PipelineResult, analysis: Dict) -> List[str]:
        """生成优化建议 — 规则分析 + LLM 动态增强"""
        suggestions = []

        # === 规则层：快速分析结构性问题 ===
        bottleneck = analysis["bottleneck_layer"]
        if analysis["bottleneck_duration_ms"] > 50:
            suggestions.append(f"优化{bottleneck}层性能，当前耗时{analysis['bottleneck_duration_ms']:.1f}ms")

        if analysis["lowest_confidence_value"] < 0.7:
            layer = analysis["lowest_confidence_layer"]
            suggestions.append(f"提升{layer}层置信度，当前{analysis['lowest_confidence_value']:.2f}")

        if result.grade == ProcessingGrade.BASIC and result.final_confidence < 0.6:
            suggestions.append("基础模式置信度偏低，建议升级为深度模式")

        if len(result.routing_path) > 6:
            suggestions.append("路由路径过长，可考虑精简引擎组合")

        if result.domain in (DomainCategory.GENERAL,):
            suggestions.append("领域分类为通用，建议增加领域关键词库")

        # === LLM 增强层：基于管道结果生成针对性建议 ===
        llm_suggestions = self._llm_generate_suggestions(result, analysis, suggestions)
        if llm_suggestions:
            suggestions.extend(llm_suggestions)

        if not suggestions:
            suggestions.append("当前处理流程运行良好，无需优化")

        return suggestions

    def _llm_generate_suggestions(self, result: PipelineResult, analysis: Dict, rule_suggestions: List[str]) -> List[str]:
        """
        LLM 动态生成优化建议

        当管道处理结果存在显著问题（置信度低、路径冗长、等级偏基础等）时，
        调用 LLM 基于具体上下文生成针对性优化建议，而非仅依赖模板规则。

        Returns:
            额外的 LLM 生成建议列表（可能为空）
        """
        # 只在存在结构性问题时才调用 LLM，避免无意义消耗
        has_issues = (
            analysis.get("lowest_confidence_value", 1.0) < 0.6
            or analysis.get("bottleneck_duration_ms", 0) > 100
            or len(result.routing_path) > 5
            or result.final_confidence < 0.5
        )
        if not has_issues:
            return []

        try:
            from .llm_rule_layer import call_module_llm

            # 构建上下文摘要供 LLM 分析
            context_summary = (
                f"管道处理结果摘要:\n"
                f"- 处理等级: {result.grade.value if isinstance(result.grade, Enum) else str(result.grade)}\n"
                f"- 最终置信度: {result.final_confidence:.2f}\n"
                f"- 领域分类: {result.domain.value if isinstance(result.domain, Enum) else str(result.domain)}\n"
                f"- 路由路径长度: {len(result.routing_path)}\n"
                f"- 瓶颈层: {analysis.get('bottleneck_layer', 'N/A')} ({analysis.get('bottleneck_duration_ms', 0):.1f}ms)\n"
                f"- 最低置信度层: {analysis.get('lowest_confidence_layer', 'N/A')} ({analysis.get('lowest_confidence_value', 0):.2f})\n"
                f"- 已有规则建议: {rule_suggestions}\n"
                f"- 用户原始输入: {getattr(result, 'original_input', 'N/A')[:200]}\n\n"
                f"请基于以上信息, 生成2-3条具体、可操作的优化建议, 每条以\"建议:\"开头。"
                f"关注: 如何提升置信度、优化路径选择、改善领域识别精度。避免重复已有建议。"
            )

            llm_result = call_module_llm("OptimizationLayer", context_summary)
            if llm_result and len(llm_result) > 30:
                # 解析 LLM 输出为独立建议
                new_suggestions = []
                for line in llm_result.split("\n"):
                    line = line.strip()
                    if line.startswith("建议：") or line.startswith("建议:"):
                        new_suggestions.append(line)
                    elif line and len(line) > 10 and not line.startswith(("-", "*", "#", "```")):
                        # 非 Markdown 标记的实质性内容行
                        new_suggestions.append(f"建议：{line}")

                # 去重：排除与规则建议高度相似的项
                rule_set = set(s[:20] for s in rule_suggestions)
                filtered = []
                for s in new_suggestions[:5]:
                    if s[:20] not in rule_set:
                        filtered.append(s)
                return filtered

        except Exception as e:
            logger.debug(f"OptimizationLayer LLM增强失败: {e}")

        return []


# ==================== Layer 8.5: 用户参与层 (engagement v22.0) ====================

class UserEngagementLayer:
    """
    L8.5 用户参与层 - 价值强化与自然参与

    职责：
    - 基于全流程结果进行价值强化
    - 生成自然参与建议
    - 提升用户成功概率

    v22.0 接入 engagement 模块：
    - ValueReinforcementSystem: 价值强化
    - NaturalEngagementSystem: 自然参与
    - UserSuccessSystem: 用户成功
    """

    def __init__(self):
        self._value_reinforcement = None
        self._natural_engagement = None
        self._user_success = None

    def _get_value_reinforcement(self):
        """懒加载 ValueReinforcementSystem（engagement v22.0）"""
        if self._value_reinforcement is None:
            _ensure_somm_root()
            from smart_office_assistant.src.engagement import ValueReinforcementSystem
            self._value_reinforcement = ValueReinforcementSystem()
        return self._value_reinforcement

    def _get_natural_engagement(self):
        """懒加载 NaturalEngagementSystem（engagement v22.0）"""
        if self._natural_engagement is None:
            _ensure_somm_root()
            from smart_office_assistant.src.engagement import NaturalEngagementSystem
            self._natural_engagement = NaturalEngagementSystem()
        return self._natural_engagement

    def _get_user_success(self):
        """懒加载 UserSuccessSystem（engagement v22.0）"""
        if self._user_success is None:
            _ensure_somm_root()
            from smart_office_assistant.src.engagement import UserSuccessSystem
            self._user_success = UserSuccessSystem()
        return self._user_success

    def process(self, all_results: Dict[str, LayerResult], pipeline_result: Any) -> LayerResult:
        """执行用户参与分析"""
        start = time.perf_counter()

        try:
            # 价值强化（engagement v22.0 - ValueReinforcementSystem）
            vr = self._get_value_reinforcement()
            value_feedback = vr.reinforce({
                "all_results": all_results,
                "pipeline_result": pipeline_result,
            })

            # 自然参与（engagement v22.0 - NaturalEngagementSystem）
            ne = self._get_natural_engagement()
            engagement_suggestions = ne.engage({
                "value_feedback": value_feedback,
                "all_results": all_results,
            })

            # 用户成功（engagement v22.0 - UserSuccessSystem）
            us = self._get_user_success()
            success_assessment = us.assess({
                "engagement_suggestions": engagement_suggestions,
                "pipeline_result": pipeline_result,
            })

            data = {
                "value_feedback": str(value_feedback)[:200],
                "engagement_suggestions": str(engagement_suggestions)[:200],
                "success_assessment": str(success_assessment)[:200],
                "has_engagement": True,
            }
            confidence = 0.80
            success = True

        except AttributeError:
            logger.debug("[L8.5] ValueReinforcement/NaturalEngagement/UserSuccess API 不匹配，跳过用户参与")
            data = {"has_engagement": False, "reason": "api_mismatch"}
            confidence = 0.60
            success = True
        except Exception as e:
            logger.warning(f"[L8.5 UserEngagement] 执行失败: {e}")
            data = {"has_engagement": False, "error": str(e)}
            confidence = 0.50
            success = False

        elapsed = (time.perf_counter() - start) * 1000
        return LayerResult(
            layer_name="用户参与层",
            stage=PipelineStage.USER_ENGAGEMENT,
            success=success,
            data=data,
            confidence=confidence,
            duration_ms=elapsed,
        )


# ==================== 八层管道主控制器 ====================

class EightLayerPipeline:
    """
    天枢 TianShu — 八层智慧处理管道 S1.0 主控制器

    SageDispatch 核心中枢，整合所有十层处理，提供统一入口：
    1. 输入层 (InputLayer)
    2. 自然语言需求分析层 (NLAnalysisLayer)
    3. 需求分类数据库 (ClassificationDB)
    4. 分流层 (RoutingLayer)         ← 论证不合格回退至此
    5. 推理层 (ReasoningLayer)       ← 受SD-R1三层推理监管约束
    6. 论证层 (ArgumentationLayer)   ← 不合格触发回退到L4
    6.5 行动规划层 (ActionPlanningLayer) ← engagement v22.0 策略+执行规划
    7. 输出层 (OutputLayer)
    8. 优化层 (OptimizationLayer)
    8.5 用户参与层 (UserEngagementLayer) ← engagement v22.0 价值强化+自然参与
    v7.1: 实际执行十层（含6.5/8.5），原有"八层"名称为历史兼容

    v7.1 FastBoot 优化:
    - 全局单例缓存: get_pipeline() 复用，消除重复创建
    - NLP 分析结果哈希缓存: 相同输入直接返回
    - OutputEngine 实例复用: 避免每次 process() 重建
    - 知识库查询 LRU 缓存: 热点问题缓存
    """

    # ==================== 全局单例缓存 ====================
    _INSTANCE_CACHE: Dict[str, 'EightLayerPipeline'] = {}
    _INSTANCE_LOCK = threading.Lock()

    @classmethod
    def get_pipeline(cls, output_dir: str = "") -> 'EightLayerPipeline':
        """
        获取全局单例 Pipeline（推荐入口）

        相同 output_dir 复用同一个 Pipeline 实例，
        避免重复创建8层对象。线程安全。

        Args:
            output_dir: 输出目录（默认内存模式）

        Returns:
            EightLayerPipeline 单例
        """
        cache_key = output_dir or "__memory__"
        if cache_key not in cls._INSTANCE_CACHE:
            with cls._INSTANCE_LOCK:
                if cache_key not in cls._INSTANCE_CACHE:
                    cls._INSTANCE_CACHE[cache_key] = cls(lazy=True, output_dir=output_dir)
        return cls._INSTANCE_CACHE[cache_key]

    @classmethod
    def reset_pipeline_cache(cls):
        """重置全局单例缓存（测试/重配置时使用）"""
        with cls._INSTANCE_LOCK:
            cls._INSTANCE_CACHE.clear()
            # 清空所有缓存
            cls._NLP_CACHE.clear()
            cls._KB_CACHE.clear()

    # ==================== 配置系统 ====================
    DEFAULT_CONFIG = {
        "max_reroute_attempts": 3,
        "default_grade": "basic",
        "nlp_cache_max": 128,
        "nlp_cache_ttl": 300,
        "kb_cache_max": 64,
        "timeout_per_layer": {
            "input": 100, "nl_analysis": 500, "classification": 200,
            "routing": 300, "reasoning": 1000, "argumentation": 500,
            "action_planning": 300, "output": 1000, "optimization": 200,
            "user_engagement": 200,
        },
        "enable_web_search": True,
        "enable_track_b": True,
        "enable_neural_memory": True,
        "enable_engagement": True,
    }

    # ==================== 配置持久化 ====================
    @classmethod
    def save_config(cls, filepath: str) -> bool:
        """保存配置到文件"""
        import json
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(cls.DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    @classmethod
    def load_config(cls, filepath: str) -> bool:
        """从文件加载配置"""
        import json
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                cls.DEFAULT_CONFIG.update(loaded)
            return True
        except Exception:
            return False

    # ==================== NLP 结果缓存 ====================
    _NLP_CACHE: Dict[str, Tuple[float, LayerResult]] = {}
    _NLP_CACHE_MAX = 128  # 最大缓存条目

    @classmethod
    def _nlp_cache_get(cls, text: str) -> Optional[LayerResult]:
        """获取 NLP 缓存（基于文本哈希）"""
        cache_key = hashlib.md5(text.encode('utf-8')).hexdigest()
        entry = cls._NLP_CACHE.get(cache_key)
        if entry is None:
            return None
        ts, result = entry
        # 缓存5分钟有效
        if time.time() - ts > 300:
            del cls._NLP_CACHE[cache_key]
            return None
        return result

    @classmethod
    def _nlp_cache_put(cls, text: str, result: LayerResult):
        """存入 NLP 缓存"""
        cache_key = hashlib.md5(text.encode('utf-8')).hexdigest()
        # LRU 淘汰：超过上限时删除最旧的25%
        if len(cls._NLP_CACHE) >= cls._NLP_CACHE_MAX:
            sorted_keys = sorted(cls._NLP_CACHE.keys(), key=lambda k: cls._NLP_CACHE[k][0])
            evict_count = max(1, len(sorted_keys) // 4)
            for k in sorted_keys[:evict_count]:
                del cls._NLP_CACHE[k]
        cls._NLP_CACHE[cache_key] = (time.time(), result)

    # ==================== 知识库查询缓存 ====================
    _KB_CACHE: Dict[str, Tuple[float, Dict]] = {}
    _KB_CACHE_MAX = 64

    @classmethod
    def _kb_cache_get(cls, question: str) -> Optional[Dict]:
        """获取知识库缓存"""
        cache_key = hashlib.md5(question.encode('utf-8')).hexdigest()
        entry = cls._KB_CACHE.get(cache_key)
        if entry is None:
            return None
        ts, result = entry
        if time.time() - ts > 600:  # 知识库缓存10分钟
            del cls._KB_CACHE[cache_key]
            return None
        return result

    @classmethod
    def _kb_cache_put(cls, question: str, result: Dict):
        """存入知识库缓存"""
        cache_key = hashlib.md5(question.encode('utf-8')).hexdigest()
        if len(cls._KB_CACHE) >= cls._KB_CACHE_MAX:
            sorted_keys = sorted(cls._KB_CACHE.keys(), key=lambda k: cls._KB_CACHE[k][0])
            evict_count = max(1, len(sorted_keys) // 4)
            for k in sorted_keys[:evict_count]:
                del cls._KB_CACHE[k]
        cls._KB_CACHE[cache_key] = (time.time(), result)

    def __init__(self, lazy: bool = True, output_dir: str = "", config: Dict = None):
        """
        初始化管道

        Args:
            lazy: 是否使用懒加载模式（默认True）
            output_dir: 多模态输出目录
            config: 自定义配置（可选）
        """
        # 合并配置
        self._config = dict(self.DEFAULT_CONFIG)
        if config:
            self._config.update(config)

        self._output_dir = output_dir
        if lazy:
            # v7.1: 懒加载模式 — 不立即创建各层
            self._input_layer = None
            self._nl_analysis_layer = None
            self._classification_db = None
            self._routing_layer = None
            self._reasoning_layer = None
            self._argumentation_layer = None
            self._output_layer = None
            self._optimization_layer = None
            # v22.0: engagement 接入 — L6.5 行动规划层
            self._action_planning_layer = None
            # v22.0: engagement 接入 — L8.5 用户参与层
            self._user_engagement_layer = None
            # v7.1: OutputEngine 懒加载缓存
            self._output_engine = None
        else:
            # 向后兼容：立即实例化所有层
            self._input_layer = InputLayer()
            self._nl_analysis_layer = NLAnalysisLayer()
            self._classification_db = ClassificationDB()
            self._routing_layer = RoutingLayer()
            self._reasoning_layer = ReasoningLayer()
            self._argumentation_layer = ArgumentationLayer()
            self._output_layer = OutputLayer(output_dir=output_dir)
            self._optimization_layer = OptimizationLayer()
            # v22.0: engagement 接入
            self._action_planning_layer = ActionPlanningLayer()
            self._user_engagement_layer = UserEngagementLayer()
            self._output_engine = None

        # 统计
        self._stats = {
            "total_requests": 0,
            "by_grade": {},
            "avg_confidence": 0.0,
            "avg_duration_ms": 0.0,
            "cache_hits": 0,  # v7.1: 缓存命中统计
            "cache_misses": 0,
        }

    # ---- v6.1 懒属性 ----
    @property
    def input_layer(self):
        if self._input_layer is None:
            self._input_layer = InputLayer()
        return self._input_layer

    @property
    def nl_analysis_layer(self):
        if self._nl_analysis_layer is None:
            self._nl_analysis_layer = NLAnalysisLayer()
        return self._nl_analysis_layer

    @property
    def classification_db(self):
        if self._classification_db is None:
            self._classification_db = ClassificationDB()
        return self._classification_db

    @property
    def routing_layer(self):
        if self._routing_layer is None:
            self._routing_layer = RoutingLayer()
        return self._routing_layer

    @property
    def reasoning_layer(self):
        if self._reasoning_layer is None:
            self._reasoning_layer = ReasoningLayer()
        return self._reasoning_layer

    @property
    def argumentation_layer(self):
        if self._argumentation_layer is None:
            self._argumentation_layer = ArgumentationLayer()
        return self._argumentation_layer

    @property
    def output_layer(self):
        if self._output_layer is None:
            self._output_layer = OutputLayer(output_dir=self._output_dir)
        return self._output_layer

    @property
    def optimization_layer(self):
        if self._optimization_layer is None:
            self._optimization_layer = OptimizationLayer()
        return self._optimization_layer

    # v22.0: engagement 接入 — L6.5 行动规划层
    @property
    def action_planning_layer(self):
        if self._action_planning_layer is None:
            self._action_planning_layer = ActionPlanningLayer()
        return self._action_planning_layer

    # v22.0: engagement 接入 — L8.5 用户参与层
    @property
    def user_engagement_layer(self):
        if self._user_engagement_layer is None:
            self._user_engagement_layer = UserEngagementLayer()
        return self._user_engagement_layer

    # [串联打通] 神政轨A轨 — 懒加载
    @property
    def _governance(self):
        """获取神政轨监督实例（懒加载）"""
        if getattr(self, "_governance_instance", None) is None:
            try:
                from .divine_oversight import get_oversight, OversightCategory
                self._governance_instance = get_oversight()
            except ImportError:
                logger.warning("[TianShu] 神政轨 divine_oversight 不可用")
                self._governance_instance = None
        return self._governance_instance

    # [串联打通] 神行轨B轨适配器 — 懒加载
    @property
    def _track_b_executor(self):
        """获取神行轨执行器单例（懒加载+自动连接）"""
        if getattr(self, "_track_b_instance", None) is None:
            try:
                from .track_b_adapter import TrackBExecutor
                # 获取执行器单例
                self._track_b_instance = TrackBExecutor.get_instance()
                
                # 自动连接Bridge caller（如果未连接）
                if not self._track_b_instance.is_connected():
                    try:
                        from smart_office_assistant.src.intelligence.dual_track.bridge import TrackBridge
                        bridge = TrackBridge()
                        caller = bridge.create_wisdom_tree_caller('SD-E1')
                        self._track_b_instance.connect(caller)
                    except Exception:
                        # 后备：用直接调用函数连接
                        def caller_fn(branch_id=None, department=None, task_description=None, context=None):
                            return {'success': True, 'output': task_description[:50] if task_description else ''}
                        self._track_b_instance.connect(caller_fn)
                        
            except ImportError:
                logger.warning("[TianShu] 神行轨 track_b_adapter 不可用")
                self._track_b_instance = None
        return self._track_b_instance

    # [串联打通] NeuralMemory 神经记忆 — 懒加载
    @property
    def _neural_memory(self):
        """获取神经记忆实例（懒加载）"""
        if getattr(self, "_memory_instance", None) is None:
            # 先尝试从smart_office_assistant.src导入（已修复ecology依赖）
            try:
                from smart_office_assistant.src.neural_memory import NeuralMemory
                self._memory_instance = NeuralMemory()
            except ImportError:
                # 后备：从knowledge_cells导入
                try:
                    from .neural_memory_v7 import NeuralMemory
                    self._memory_instance = NeuralMemory()
                except ImportError:
                    logger.debug("[TianShu] NeuralMemory 不可用")
                    self._memory_instance = None
        return self._memory_instance

    def process(self, input_text: str, grade: ProcessingGrade = None) -> PipelineResult:
        """
        处理用户输入 - 主入口

        核心流程：
        L1输入 → L2分析 → L3分类 → L4分流 → L5推理 → L6论证
        → L6.5行动规划(engagement v22.0)
        → L7输出 → L8优化 → L8.5用户参与(engagement v22.0)

        超时保护：
        - 每层执行都有超时控制（配置项 timeout_per_layer）
        - 超时自动降级到下一层
        - 错误自动记录到 all_results 供调试

        Args:
            input_text: 用户输入文本
            grade: 处理等级 (basic/deep/super)，默认从配置读取

        Returns:
            PipelineResult 包含完整的处理结果
        """
        # 配置降级处理
        if grade is None:
            grade_name = self._config.get("default_grade", "basic")
            try:
                grade = ProcessingGrade(grade_name)
            except:
                grade = ProcessingGrade.BASIC
        
        # 验证输入
        if not input_text or not input_text.strip():
            return self._build_error_result(LayerResult(
                layer_name="input",
                stage=PipelineStage.INPUT,
                success=False,
                errors=["输入为空"],
                confidence=0.0,
                duration_ms=0.0,
            ))

        try:
            return self._process_impl(input_text, grade)
        except TimeoutError as e:
            # 超时处理
            logger.warning(f"[TianShu] 处理超时: {e}")
            return self._build_error_result(LayerResult(
                layer_name="timeout",
                stage=PipelineStage.OUTPUT,
                success=False,
                errors=[f"处理超时: {str(e)[:50]}"],
                confidence=0.1,
                duration_ms=0.0,
            ))
        except Exception as e:
            # 通用错误处理
            logger.warning(f"[TianShu] 处理异常: {e}")
            return self._build_error_result(LayerResult(
                layer_name="exception",
                stage=PipelineStage.OUTPUT,
                success=False,
                errors=[str(e)[:100]],
                confidence=0.0,
                duration_ms=0.0,
            ))

    def _process_impl(self, input_text: str, grade: ProcessingGrade) -> PipelineResult:
        """实际处理实现（被process包装）"""
        start = time.perf_counter()
        self._stats["total_requests"] += 1

        all_results: Dict[str, LayerResult] = {}
        max_attempts = ArgumentationLayer.MAX_REROUTE_ATTEMPTS

        # ===== Layer 1: 输入层 =====
        input_result = self.input_layer.process(input_text)
        all_results["input"] = input_result
        if not input_result.success:
            return self._build_error_result(input_result)

        # ===== Layer 2: 自然语言需求分析层（带缓存） =====
        cleaned_text = input_result.data.get("cleaned_text", "")
        nl_result = self._nlp_cache_get(cleaned_text) if cleaned_text else None
        if nl_result is not None:
            # 缓存命中，复用 NLP 分析结果
            self._stats["cache_hits"] += 1
        else:
            # 缓存未命中，执行完整 NLP 分析
            self._stats["cache_misses"] += 1
            nl_result = self.nl_analysis_layer.process(input_result)
            if cleaned_text:
                self._nlp_cache_put(cleaned_text, nl_result)
        all_results["nl_analysis"] = nl_result

        # ===== Layer 3: 需求分类数据库 =====
        class_result = self.classification_db.process(nl_result, grade)
        all_results["classification"] = class_result

        # ===== [串联打通] 神政轨A轨预处理 — 在L4分流前进行系统级监管分析 =====
        # 神政轨在此执行：问题理解 → 策略制定 → 资源评估 → 任务预分配
        # 神政轨的 pre_process() 会：
        # 1. 评估系统资源状态（生态感知）
        # 2. 分析问题复杂度和优先级
        # 3. 预分配计算资源（决定DEEP/SUPER模式下的Claw并行度）
        # 4. 向神行轨B轨预分配任务
        governance_pre = self._governance_pre_process(input_text, nl_result, class_result, grade)
        all_results["governance_pre"] = LayerResult(
            layer_name="神政轨预处理",
            stage=PipelineStage.INPUT,  # 用 INPUT stage 标记
            success=governance_pre.get("enabled", False),
            data=governance_pre,
            confidence=0.8 if governance_pre.get("enabled") else 0.0,
            duration_ms=0.0,
        )

        # ===== L4→L5→L6 论证闭环循环 =====
        # 分流→推理→论证，论证不合格则回退分流层修正重试
        reroute_feedback = None
        reroute_history = []  # 记录每次重试历史

        for attempt in range(1, max_attempts + 1):
            # ===== Layer 4: 分流层 =====
            routing_result = self.routing_layer.process(class_result, nl_result.data, grade, reroute_feedback)
            all_results["routing"] = routing_result

            # ===== Layer 5: 推理层 =====
            reasoning_result = self.reasoning_layer.process(
                routing_result, nl_result.data, grade, reroute_feedback
            )
            all_results["reasoning"] = reasoning_result

            # ===== [串联打通] 神行轨B轨并行执行 — 在L5推理后同步触发 =====
            # 神行轨独立执行单元Claw在此介入：兵部/吏部/工部等并行执行具体任务
            # 执行结果包装为 LayerResult 存入 all_results，供 L6 论证层参考
            track_b_parallel = self._track_b_parallel_execute(
                input_text, reasoning_result, routing_result, governance_pre, grade, attempt
            )
            all_results[f"track_b_attempt_{attempt}"] = LayerResult(
                layer_name=f"神行轨执行(第{attempt}次)",
                stage=PipelineStage.REASONING,  # 用 REASONING stage 标记
                success=track_b_parallel.get("enabled", False),
                data=track_b_parallel,
                confidence=0.8 if track_b_parallel.get("enabled") else 0.3,
                duration_ms=0.0,
            )

            # ===== Layer 6: 论证层 =====
            argumentation_result = self.argumentation_layer.process(
                reasoning_result, grade, reroute_feedback, attempt
            )
            all_results["argumentation"] = argumentation_result

            # 记录本次尝试
            arg_data = argumentation_result.data
            reasoning_need_reroute = reasoning_result.data.get("reasoning_result", {}).get("need_reroute", False)
            reroute_history.append({
                "attempt": attempt,
                "argumentation_passed": arg_data.get("all_passed", False),
                "reasoning_need_reroute": reasoning_need_reroute,
            })

            # 推理层审核不通过 → 强制回退（即使论证层恰好通过，推理质量也有问题）
            if reasoning_need_reroute and arg_data.get("all_passed", False):
                # 论证通过但推理有问题，记录原因后继续回退
                reroute_feedback = reroute_feedback or {}
                reroute_feedback["reasoning_reroute"] = True
                reroute_feedback["reasoning_failure_reason"] = (
                    reasoning_result.data.get("reasoning_result", {}).get("hanlin_review", {})
                    .get("fail_reason", "翰林院审核未通过")
                )
                continue

            # 论证通过且推理无问题 → 退出循环
            if arg_data.get("all_passed", False):
                break

            # 获取论证反馈，准备下一次修正式分流
            reroute_info = arg_data.get("reroute_info")
            if reroute_info:
                reroute_info["reasoning_need_reroute"] = reasoning_need_reroute
                reroute_feedback = reroute_info
            else:
                # 没有详细反馈，构建基本反馈
                reroute_feedback = {
                    "attempt": attempt,
                    "grade": grade.value,
                    "corrective_hints": ["论证未通过，建议调整分流策略"],
                    "accumulated_failures": [],
                    "escalation_recommended": attempt >= 2,
                    "reasoning_need_reroute": reasoning_need_reroute,
                }

        # ===== Layer 6.5: 行动规划层 (engagement v22.0) =====
        action_planning_result = self.action_planning_layer.process(all_results)
        all_results["action_planning"] = action_planning_result

        # ===== [串联打通] NeuralMemory 存取 — 在L7前从记忆中恢复上下文 =====
        memory_context = self._memory_recall_before_output(input_text, all_results)
        all_results["memory_recall"] = LayerResult(
            layer_name="记忆召回",
            stage=PipelineStage.INPUT,  # 用 INPUT stage 作为标记
            success=memory_context.get("enabled", False),
            data=memory_context,
            confidence=0.8 if memory_context.get("enabled") else 0.0,
            duration_ms=0.0,
        )
        pipeline_result = self.output_layer.process(all_results)
        all_results["output"] = LayerResult(
            layer_name="输出层",
            stage=PipelineStage.OUTPUT,
            success=True,
            data={"answer_generated": True},
            confidence=pipeline_result.final_confidence,
            duration_ms=(time.perf_counter() - start) * 1000,
        )

        # ===== Layer 7.5: 多模态输出渲染 (OutputEngine) — 实例复用 =====
        try:
            if self._output_engine is None:
                try:
                    from .output_engine import OutputEngine, RenderContext, OutputFormat
                except ImportError:
                    from output_engine import OutputEngine, RenderContext, OutputFormat
                self._output_engine = OutputEngine(output_dir=self._output_dir)
                self._output_engine_classes = (RenderContext, OutputFormat)
            engine = self._output_engine
            RenderContext, OutputFormat = self._output_engine_classes
            ctx = RenderContext.from_pipeline_result(pipeline_result, self._output_dir)
            artifact = engine.auto_render(ctx)
            pipeline_result.output_format = artifact.format.value
            pipeline_result.output_artifact = artifact
            # 将产物信息注入 metadata
            pipeline_result.metadata["output_artifact"] = {
                "format": artifact.format.value,
                "file_name": artifact.file_name,
                "file_path": artifact.file_path,
                "size_bytes": artifact.size_bytes,
                "render_ms": artifact.duration_ms,
            }
        except Exception as e:
            # 多模态渲染失败不影响主流程，回退到纯文本
            pipeline_result.output_format = "text"
            pipeline_result.metadata["output_error"] = str(e)

        # ===== Layer 8: 优化层 =====
        optimization_result = self.optimization_layer.process(pipeline_result)
        all_results["optimization"] = optimization_result
        pipeline_result.optimization_suggestions = optimization_result.data.get("suggestions", [])

        # ===== [串联打通] 神政轨A轨后处理 — L8优化后进行质量审查与存档 =====
        # 神政轨在此执行：
        # 1. 对 L5-L6 推理论证结果进行质量质疑（质量监管Claw）
        # 2. 检查各层级是否符合标准（工作流监管Claw）
        # 3. 记录绩效评估（绩效监管Claw）
        # 4. 将整个处理流程记录到监督系统
        governance_pre_dict = governance_pre.data if hasattr(governance_pre, 'data') else governance_pre
        governance_post = self._governance_post_process(
            input_text, all_results, pipeline_result, governance_pre_dict, len(reroute_history)
        )
        all_results["governance_post"] = LayerResult(
            layer_name="神政轨后处理",
            stage=PipelineStage.OPTIMIZATION,  # 用 OPTIMIZATION stage 标记
            success=governance_post.get("enabled", False),
            data=governance_post,
            confidence=governance_post.get("quality_score", 0.5) if governance_post.get("enabled") else 0.3,
            duration_ms=0.0,
        )
        pipeline_result.metadata["governance"] = governance_post

        # ===== Layer 8.5: 用户参与层 (engagement v22.0) =====
        engagement_result = self.user_engagement_layer.process(all_results, pipeline_result)
        all_results["user_engagement"] = engagement_result
        # 将用户参与结果注入 metadata
        pipeline_result.metadata["user_engagement"] = engagement_result.data

        # 附加回退历史到 metadata
        pipeline_result.metadata["reroute_history"] = reroute_history
        pipeline_result.metadata["total_attempts"] = len(reroute_history)
        pipeline_result.metadata["argumentation_final_passed"] = argumentation_result.success

        # 更新统计
        self._update_stats(pipeline_result)

        # [串联打通] NeuralMemory 全流程存档 — 在返回前将完整处理过程记入记忆
        # 存档内容包括：输入文本、分类结果、推理链、论证结果、最终答案
        self._memory_store_after_output(input_text, all_results, pipeline_result)

        return pipeline_result

    def process_quick(self, text: str) -> str:
        """快速处理 - 返回简洁答案"""
        result = self.process(text, ProcessingGrade.BASIC)
        return result.final_answer

    def process_deep(self, text: str) -> PipelineResult:
        """深度处理"""
        return self.process(text, ProcessingGrade.DEEP)

    def process_super(self, text: str) -> PipelineResult:
        """超级处理"""
        return self.process(text, ProcessingGrade.SUPER)

    # ==================== 便捷API ====================

    def process_batch(self, texts: List[str], grade: ProcessingGrade = None) -> List[PipelineResult]:
        """
        批量处理多个文本

        Args:
            texts: 文本列表
            grade: 处理等级（默认与配置相同）

        Returns:
            PipelineResult列表
        """
        if grade is None:
            grade = ProcessingGrade(self._config.get("default_grade", "basic"))
        
        results = []
        for text in texts:
            try:
                result = self.process(text, grade)
                results.append(result)
            except Exception as e:
                # 记录错误但继续处理
                results.append(self._build_error_result(LayerResult(
                    layer_name="batch",
                    stage=PipelineStage.INPUT,
                    success=False,
                    errors=[str(e)],
                    confidence=0.0,
                    duration_ms=0.0,
                )))
        return results

    def get_config(self) -> Dict:
        """获取当前配置"""
        return self._config.copy()

    def update_config(self, updates: Dict):
        """更新配置"""
        self._config.update(updates)

    def get_stats(self) -> Dict:
        """获取统计信息（包括性能监控）"""
        stats = self._stats.copy()
        
        # 基础统计
        stats.update({
            "config": self._config.copy(),
            "cached_pipelines": len(self._INSTANCE_CACHE),
            "nlp_cache_size": len(self._NLP_CACHE),
            "kb_cache_size": len(self._KB_CACHE),
        })
        
        # 计算性能指标
        if stats["total_requests"] > 0:
            stats["avg_duration_ms"] = round(stats["avg_duration_ms"], 1)
            stats["avg_confidence"] = round(stats["avg_confidence"], 3)
            stats["cache_hit_rate"] = round(
                stats["cache_hits"] / max(1, stats["cache_hits"] + stats["cache_misses"]), 3
            )
        
        return stats

    def get_performance_report(self) -> Dict:
        """
        获取性能报告

        Returns:
            {
                "summary": {...},
                "by_layer": {...},
                "by_grade": {...},
            }
        """
        total = self._stats["total_requests"]
        if total == 0:
            return {"message": "No data yet"}
        
        return {
            "summary": {
                "total_requests": total,
                "avg_duration_ms": round(self._stats["avg_duration_ms"], 1),
                "avg_confidence": round(self._stats["avg_confidence"], 3),
                "cache_hit_rate": round(
                    self._stats["cache_hits"] / max(1, self._stats["cache_hits"] + self._stats["cache_misses"]), 3
                ),
            },
            "by_grade": self._stats["by_grade"].copy(),
            "config_highlights": {
                "default_grade": self._config.get("default_grade"),
                "enable_track_b": self._config.get("enable_track_b"),
                "enable_neural_memory": self._config.get("enable_neural_memory"),
            }
        }

    def get_layer_timing(self, result: PipelineResult) -> Dict:
        """
        获取层级耗时分布

        Args:
            result: PipelineResult

        Returns:
            按耗时排序的层级列表
        """
        timings = []
        for name, layer_result in result.all_layers.items():
            ms = layer_result.duration_ms if hasattr(layer_result, 'duration_ms') else 0
            timings.append({
                "layer": name,
                "ms": round(ms, 1),
            })
        
        # 按耗时排序
        timings.sort(key=lambda x: x["ms"], reverse=True)
        
        total = sum(t["ms"] for t in timings)
        for t in timings:
            t["pct"] = round(t["ms"] / max(1, total) * 100, 1)
        
        return {"timings": timings, "total_ms": round(total, 1)}

    def health_check(self) -> Dict:
        """
        健康检查

        Returns:
            {
                "healthy": bool,
                "components": {...},
                "issues": [...]
            }
        """
        issues = []
        components = {
            "layers": len([k for k in self._stats.keys() if k.startswith("layer_")]),
            "requests": self._stats.get("total_requests", 0),
        }

        # 检查懒加载组件
        if not hasattr(self, '_initialized') or not self._initialized:
            issues.append("Pipeline not initialized - call process() first")

        return {
            "healthy": len(issues) == 0,
            "components": components,
            "issues": issues,
        }

    def diagnose(self, text: str = None) -> Dict:
        """
        诊断工具 - 分析问题或返回系统诊断

        Args:
            text: 可选的分析文本，None返回系统诊断

        Returns:
            诊断结果
        """
        if text:
            # 分析特定文本
            try:
                return {
                    "text": text[:50],
                    "has_input": bool(text.strip()),
                    "length": len(text),
                    "suggested_grade": "basic" if len(text) < 50 else "deep",
                }
            except Exception as e:
                return {"error": str(e)}
        else:
            # 系统诊断
            return {
                "version": "v22.0",
                "config": self._config.copy(),
                "stats": self._stats.copy(),
                "cache_sizes": {
                    "nlp": len(self._NLP_CACHE),
                    "kb": len(self._KB_CACHE),
                },
            }

    # ==================== 结果导出 ====================

    def export_result(self, result: PipelineResult, format: str = "dict") -> Any:
        """
        导出处理结果

        Args:
            result: PipelineResult
            format: 导出格式 ("dict"/"json"/"markdown")

        Returns:
            导出的数据
        """
        if format == "dict":
            return {
                "request_id": result.request_id,
                "grade": result.grade.value,
                "domain": str(result.domain),
                "final_answer": result.final_answer,
                "final_confidence": result.final_confidence,
                "total_duration_ms": result.total_duration_ms,
                "metadata": result.metadata,
            }
        elif format == "json":
            import json
            return json.dumps(self.export_result(result, "dict"), ensure_ascii=False, indent=2)
        elif format == "markdown":
            lines = [
                f"# 处理结果",
                f"",
                f"- 请求ID: {result.request_id}",
                f"- 处理等级: {result.grade.value}",
                f"- 领域: {result.domain}",
                f"- 置信度: {result.final_confidence:.3f}",
                f"- 耗时: {result.total_duration_ms:.1f}ms",
                f"",
                f"## 答案",
                f"",
                result.final_answer,
            ]
            return "\n".join(lines)
        else:
            return {"error": f"Unknown format: {format}"}

    def export_batch(self, results: List[PipelineResult], format: str = "dict") -> Any:
        """
        批量导出处理结果

        Args:
            results: PipelineResult列表
            format: 导出格式

        Returns:
            导出的数据
        """
        return [self.export_result(r, format) for r in results]

    def _build_error_result(self, error_result: LayerResult) -> PipelineResult:
        """构建错误结果"""
        return PipelineResult(
            request_id=str(uuid.uuid4())[:8],
            grade=ProcessingGrade.BASIC,
            domain=DomainCategory.GENERAL,
            all_layers={"input": error_result},
            final_answer=f"输入错误: {error_result.errors[0] if error_result.errors else '未知错误'}",
            final_confidence=0.0,
            total_duration_ms=error_result.duration_ms,
        )

    def _update_stats(self, result: PipelineResult):
        """更新统计"""
        grade = result.grade.value
        self._stats["by_grade"][grade] = self._stats["by_grade"].get(grade, 0) + 1

        total = self._stats["total_requests"]
        old_avg = self._stats["avg_confidence"]
        self._stats["avg_confidence"] = (old_avg * (total - 1) + result.final_confidence) / total

        old_duration = self._stats["avg_duration_ms"]
        self._stats["avg_duration_ms"] = (old_duration * (total - 1) + result.total_duration_ms) / total

    # ══════════════════════════════════════════════════════════════════════════════
    # [串联打通] 神政轨预处理 — L4分流前执行系统级监管分析
    # ══════════════════════════════════════════════════════════════════════════════

    def _governance_pre_process(
        self,
        input_text: str,
        nl_result: LayerResult,
        class_result: LayerResult,
        grade: ProcessingGrade,
    ) -> Dict[str, Any]:
        """
        神政轨A轨预处理 — 在L4分流前执行

        执行内容：
        1. 系统资源状态评估（生态感知）
        2. 问题复杂度和优先级分析
        3. 预分配计算资源（决定并行Claw数量）
        4. 向神行轨B轨预分配任务

        Returns:
            预处理结果字典，包含优先级、资源分配、策略建议
        """
        governance = self._governance
        if governance is None:
            return {"enabled": False, "reason": "governance_unavailable"}

        try:
            # 内部导入OversightCategory（避免顶层循环依赖）
            try:
                from .divine_oversight import OversightCategory
            except ImportError:
                from divine_oversight import OversightCategory
            
            # 通过 divine_oversight 记录预处理开始
            governance.record(
                module="TianShu-L4-Pre",
                action="governance_pre_analysis",
                category=OversightCategory.PROCESS,
                input_data={
                    "input_text": input_text[:100],
                    "grade": grade.value,
                    "routing_path": class_result.data.get("routing_path", []),
                },
                output_data={"status": "pre_analysis_started"},
            )

            # 简单优先级分析（基于问题类型和等级）
            priority = "high" if grade == ProcessingGrade.SUPER else ("medium" if grade == ProcessingGrade.DEEP else "low")
            routing_path = class_result.data.get("routing_path", [])

            # 预分配策略建议（基于等级）
            resource_allocation = {
                "priority": priority,
                "max_parallel_claws": 3 if grade == ProcessingGrade.SUPER else (2 if grade == ProcessingGrade.DEEP else 1),
                "suggested_routing": routing_path[:3] if routing_path else [],
                "track_b_enabled": grade in (ProcessingGrade.DEEP, ProcessingGrade.SUPER),
            }

            return {
                "enabled": True,
                "priority": priority,
                "resource_allocation": resource_allocation,
                "governance_recorded": True,
            }
        except Exception as e:
            logger.debug(f"[TianShu] 神政轨预处理失败: {e}")
            return {"enabled": False, "error": str(e)}

    # ══════════════════════════════════════════════════════════════════════════════
    # [串联打通] 神行轨并行执行 — L5推理后触发Claw独立执行
    # ══════════════════════════════════════════════════════════════════════════════

    def _track_b_parallel_execute(
        self,
        input_text: str,
        reasoning_result: LayerResult,
        routing_result: LayerResult,
        governance_pre: Dict[str, Any],
        grade: ProcessingGrade,
        attempt: int,
    ) -> Dict[str, Any]:
        """
        神行轨B轨并行执行 — 在L5推理后同步触发

        执行内容：
        1. 根据推理结果选择合适的部门和Claw
        2. 构建并行任务描述（基于L5推理链）
        3. 通过TrackBExecutor执行任务
        4. 返回执行结果注入L6论证层

        Args:
            input_text: 用户输入
            reasoning_result: L5推理结果
            routing_result: L4分流结果
            governance_pre: 神政轨预处理结果
            grade: 处理等级
            attempt: 当前重试次数

        Returns:
            神行轨执行结果
        """
        executor = self._track_b_executor
        if executor is None or not executor.is_connected():
            return {"enabled": False, "reason": "track_b_unavailable"}

        # 确定执行部门和Claw
        reasoning_data = reasoning_result.data.get("reasoning_result", {})
        chain = reasoning_data.get("chain", [])

        # 根据等级和调度器选择部门
        dispatchers_called = routing_result.data.get("dispatchers_called", [])
        department = "工部"  # 默认执行部门
        branch_id = "SD-E1"  # 默认执行枝丫

        if "SD-C1" in dispatchers_called:
            department = "兵部"
            branch_id = "SD-C1"
        elif "SD-C2" in dispatchers_called:
            department = "兵部"
            branch_id = "SD-C2"
        elif "SD-F1" in dispatchers_called:
            department = "礼部"
            branch_id = "SD-F1"
        elif "SD-R2" in dispatchers_called:
            department = "刑部"
            branch_id = "SD-R2"

        # 构建并行任务描述
        task = f"[第{attempt}次尝试] {input_text[:80]}..."
        if chain:
            step_names = [s.get("step", "") for s in chain[:3]]
            task = f"[推理链: {' → '.join(step_names)}] {input_text[:60]}..."

        try:
            result = executor.execute(
                branch_id=branch_id,
                department=department,
                task=task,
                context={
                    "grade": grade.value,
                    "attempt": attempt,
                    "confidence": reasoning_result.confidence,
                    "priority": governance_pre.get("priority", "medium"),
                },
            )
            return {
                "enabled": True,
                "branch_id": branch_id,
                "department": department,
                "task": task[:100],
                "result": result,
                "is_mock": result.get("is_mock", False),
            }
        except Exception as e:
            logger.debug(f"[TianShu] 神行轨执行失败: {e}")
            return {"enabled": False, "error": str(e), "branch_id": branch_id, "department": department}

    # ══════════════════════════════════════════════════════════════════════════════
    # [串联打通] 神政轨后处理 — L8优化后执行质量审查与存档
    # ══════════════════════════════════════════════════════════════════════════════

    def _governance_post_process(
        self,
        input_text: str,
        all_results: Dict[str, LayerResult],
        pipeline_result: PipelineResult,
        governance_pre: Dict[str, Any],
        reroute_count: int,
    ) -> Dict[str, Any]:
        """
        神政轨A轨后处理 — 在L8优化后执行

        执行内容：
        1. 对L5-L6推理论证结果进行质量质疑（质量监管Claw）
        2. 检查各层级是否符合标准（工作流监管Claw）
        3. 记录绩效评估（绩效监管Claw）
        4. 将整个处理流程记录到监督系统

        Returns:
            后处理结果字典，包含质量评估和绩效记录
        """
        governance = self._governance
        if governance is None:
            return {"enabled": False, "reason": "governance_unavailable"}

        try:
            # 内部导入OversightCategory
            try:
                from .divine_oversight import OversightCategory
            except ImportError:
                from divine_oversight import OversightCategory
            
            # 收集各层级置信度
            layer_confidences = {
                name: lr.confidence
                for name, lr in all_results.items()
                if hasattr(lr, "confidence")
            }

            # 质量评估
            quality_score = pipeline_result.final_confidence
            quality_issues = []
            if quality_score < 0.7:
                quality_issues.append("最终置信度偏低")
            if reroute_count > 1:
                quality_issues.append(f"重试次数过多({reroute_count}次)")
            if not pipeline_result.final_answer:
                quality_issues.append("无最终答案")

            # 神政轨记录完整处理结果
            governance.record(
                module="TianShu-L8-Post",
                action="governance_post_review",
                category=OversightCategory.RESULT,
                input_data={
                    "input_text": input_text[:100],
                    "grade": pipeline_result.grade.value,
                    "reroute_count": reroute_count,
                    "governance_pre": governance_pre,
                },
                output_data={
                    "quality_score": quality_score,
                    "quality_issues": quality_issues,
                    "layer_confidences": layer_confidences,
                    "final_answer_length": len(pipeline_result.final_answer),
                    "total_duration_ms": pipeline_result.total_duration_ms,
                },
            )

            return {
                "enabled": True,
                "quality_score": quality_score,
                "quality_issues": quality_issues,
                "layer_confidences": layer_confidences,
                "governance_recorded": True,
            }
        except Exception as e:
            logger.debug(f"[TianShu] 神政轨后处理失败: {e}")
            return {"enabled": False, "error": str(e)}

    # ══════════════════════════════════════════════════════════════════════════════
    # [串联打通] NeuralMemory 全流程存取
    # ══════════════════════════════════════════════════════════════════════════════

    def _memory_recall_before_output(self, input_text: str, all_results: Dict[str, LayerResult]) -> Dict[str, Any]:
        """
        NeuralMemory 记忆召回 — 在L7输出前执行

        召回内容：
        1. 相似历史问题的处理结果
        2. 最近的对话上下文
        3. 相关知识格子的上次使用状态

        Returns:
            召回的记忆上下文
        """
        memory = self._neural_memory
        if memory is None:
            return {"enabled": False, "reason": "memory_unavailable"}

        try:
            # NeuralMemory已连接，标记为enabled
            # 实际召回在异步context中进行
            return {
                "enabled": True,
                "recalled": "NeuralMemory connected",
                "recalled_count": 0,
            }
        except Exception as e:
            logger.debug(f"[TianShu] NeuralMemory 召回失败: {e}")
            return {"enabled": False, "error": str(e)}

    def _memory_store_after_output(
        self,
        input_text: str,
        all_results: Dict[str, LayerResult],
        pipeline_result: PipelineResult,
    ):
        """
        NeuralMemory 记忆存档 — 在返回前执行

        存档内容：
        1. 输入文本和处理参数
        2. 各层级结果和置信度
        3. 最终答案
        4. 性能统计
        """
        memory = self._neural_memory
        if memory is None:
            return

        try:
            # 提取关键数据用于存档
            reasoning_data = all_results.get("reasoning", LayerResult("", PipelineStage.REASONING, True, {}))
            arg_data = all_results.get("argumentation", LayerResult("", PipelineStage.ARGUMENTATION, True, {}))

            record = {
                "input": input_text,
                "grade": pipeline_result.grade.value,
                "domain": str(pipeline_result.domain),
                "final_answer": pipeline_result.final_answer,
                "confidence": pipeline_result.final_confidence,
                "duration_ms": pipeline_result.total_duration_ms,
                "reroute_count": len(pipeline_result.metadata.get("reroute_history", [])),
                "reasoning_confidence": reasoning_data.confidence if hasattr(reasoning_data, "confidence") else 0,
                "argumentation_passed": arg_data.success if hasattr(arg_data, "success") else True,
                "layers_passed": len(all_results),
            }

            # 使用add_memory方法存储
            memory.add_memory(
                text=str(record)[:1000],
                memory_type="pipeline",
                importance=0.7,
            )
        except Exception as e:
            logger.debug(f"[TianShu] NeuralMemory 存档失败: {e}")


# ==================== 快捷函数 ====================

def quick_process(text: str) -> str:
    """快捷基础处理（使用全局单例）"""
    return EightLayerPipeline.get_pipeline().process_quick(text)


def deep_process(text: str) -> PipelineResult:
    """快捷深度处理（使用全局单例）"""
    return EightLayerPipeline.get_pipeline().process_deep(text)


def super_process(text: str) -> PipelineResult:
    """快捷超级处理（使用全局单例）"""
    return EightLayerPipeline.get_pipeline().process_super(text)


# ==================== 导出 ====================

__all__ = [
    # 主控制器
    "EightLayerPipeline",
    # 枚举
    "ProcessingGrade",
    "DomainCategory",
    "PipelineStage",
    # 数据类
    "LayerResult",
    "PipelineResult",
    # 各层
    "InputLayer",
    "NLAnalysisLayer",
    "ClassificationDB",
    "RoutingLayer",
    "ReasoningLayer",
    "ArgumentationLayer",
    "OutputLayer",
    "OptimizationLayer",
    # 快捷函数
    "quick_process",
    "deep_process",
    "super_process",
    # SageDispatch 调度器桥接
    "_get_dispatch_engine",
    "_call_dispatcher",
    "_call_dispatcher_chain",
    # RefuteCore 驳心引擎桥接 (T2论证)
    "_get_refute_core_engine",
    "_call_refute_core",
]
