"""
神政轨监管Claw系统 v2.2
====================================

★ 核心定位 ★
神政轨的Claw是贤者Claw被任命到监管岗位，能独立思考、独立工作。

★ 双重能力 ★
1. 监管能力：质疑、催促、惩罚（监管职责）
2. 执行能力：能真正干活、解决问题（核心升级）

★ 任命机制 ★
贤者Claw → 被任命 → 监管Claw（携带执行能力）

★ 贤者Claw执行能力 ★
- 能独立思考：质疑任何决策
- 能独立工作：直接执行具体任务
- 能独立推理：DivineReason集成
- 能访问知识：DomainNexus集成
- 能生成结果：可执行的分析和建议

★ v2.2 变更 ★
- 新增 ecosystem 生态监管岗位（第5个岗位）
- 生态监管Claw: 监控系统资源、评估生态健康、预警资源危机
- 默认贤者: 墨子（技术实用主义大师，擅长资源评估）

版本: v2.2
更新: 2026-04-30
"""

import logging
import asyncio
import threading
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════════════════
# 监管类型与等级
# ══════════════════════════════════════════════════════════════════════════


class SupervisionType(Enum):
    """监管类型"""
    PROGRESS = "progress"
    QUALITY = "quality"
    COMPLIANCE = "compliance"
    PERFORMANCE = "performance"
    WORKFLOW = "workflow"
    ECOSYSTEM = "ecosystem"  # v2.2 新增：生态监管

    @property
    def label(self) -> str:
        labels = {
            "progress": "进度监管",
            "quality": "质量监管",
            "compliance": "合规监管",
            "performance": "绩效监管",
            "workflow": "工作流监管",
            "ecosystem": "生态监管",
        }
        return labels.get(self.value, self.value)


class SupervisionLevel(Enum):
    """监管等级"""
    MILD = "mild"           # 温和提醒（提前1小时）
    NORMAL = "normal"       # 正常催促（提前30分钟）
    HARSH = "harsh"         # 严厉质问（提前10分钟）
    EXTREME = "extreme"     # 极限施压（到期前5分钟）
    EXECUTION = "execution" # 执行问责（已超时）


class PunishmentType(Enum):
    """惩罚类型"""
    WARNING = "warning"
    CRITICISM = "criticism"
    LOGGING = "logging"
    PUBLIC_SHAME = "public_shame"
    ESCALATION = "escalation"
    SUSPENSION = "suspension"


@dataclass
class SupervisionRecord:
    """监管记录"""
    timestamp: str
    claw_name: str
    position: str
    target: str
    action: str  # question/urge/punish/working
    level: str
    thinking_chain: List[str]
    result: Dict[str, Any]
    punishment_type: Optional[str] = None


@dataclass
class Appointment:
    """任命记录"""
    claw_name: str
    position: str
    appointment_time: str
    appointment_reason: str


# ══════════════════════════════════════════════════════════════════════════
#  知识访问层（复用神行轨）
# ══════════════════════════════════════════════════════════════════════════


class SupervisionKnowledgeLayer:
    """
    知识访问层 - 监管Claw的知识获取入口

    封装 DomainNexus 的访问逻辑
    """

    def __init__(self):
        self._nexus = None
        self._nexus_lock = threading.Lock()

    def _ensure_nexus(self):
        """懒加载 DomainNexus 单例"""
        if self._nexus is None:
            with self._nexus_lock:
                if self._nexus is None:
                    try:
                        from knowledge_cells.domain_nexus import DomainNexus
                        self._nexus = DomainNexus()
                        logger.info("[监管-知识层] DomainNexus 初始化完成")
                    except ImportError:
                        logger.warning("[监管-知识层] DomainNexus 不可用，使用内置知识")
                        self._nexus = None
        return self._nexus

    def query_knowledge(self, question: str, context: str = "") -> Dict[str, Any]:
        """
        查询相关知识

        Args:
            question: 问题
            context: 上下文

        Returns:
            知识查询结果
        """
        nexus = self._ensure_nexus()
        if nexus:
            try:
                result = nexus.query(question, context)
                return {
                    "source": "domain_nexus",
                    "answer": result.get("answer", ""),
                    "relevant_cells": result.get("relevant_cells", []),
                    "hot_topics": result.get("hot_topics", []),
                }
            except Exception as e:
                logger.warning(f"[监管-知识层] DomainNexus 查询失败: {e}")
        return {"source": "builtin", "answer": "", "relevant_cells": []}


# ══════════════════════════════════════════════════════════════════════════
#  贤者Claw基类（能真正干活）
# ══════════════════════════════════════════════════════════════════════════


class WiseoneClaw:
    """
    贤者Claw基类 - 能独立思考、独立工作的Claw

    核心能力:
    1. 独立思考 - 用 DivineReason 进行推理分析
    2. 独立工作 - 执行具体任务并产出结果
    3. 知识访问 - 访问 DomainNexus
    4. 记录思考链 - 记录每一步思考过程
    5. 领域专业化 - 每个贤者有独特的思考风格和分析角度

    这是神政轨监管Claw的"贤者能力"来源。
    """

    # 贤者思考风格配置（每个贤者独特的推理角度）
    THINKING_STYLES = {
        "孔子": {
            "role": "儒家教育管理大师",
            "angles": ["以人为本", "教化引导", "礼制规范", "仁政爱民", "中庸之道"],
            "question_templates": [
                "此事对人影响如何？是否顾及了各方利益？",
                "是否有更好的教化引导方式，而非强制执行？",
                "这个方案符合礼制规范吗？",
                "如果换位思考，被影响的人会怎么想？",
            ],
            "analysis_focus": "从人际关系、管理制度、道德教化三个维度分析",
        },
        "老子": {
            "role": "道家战略哲学家",
            "angles": ["道法自然", "无为而治", "上善若水", "大音希声", "反者道之动"],
            "question_templates": [
                "这件事的本质是什么？我们是否被表象迷惑了？",
                "有没有'不作为'反而更好的可能？",
                "这个方案的干预是否过度？能否顺其自然？",
                "从长远看，10年后这件事还会重要吗？",
            ],
            "analysis_focus": "从事物本质、长期趋势、干预适度性三个维度分析",
        },
        "荀子": {
            "role": "儒家礼法制度专家",
            "angles": ["性恶论", "隆礼重法", "积微成著", "制度约束", "化性起伪"],
            "question_templates": [
                "这个制度设计有没有漏洞可以被利用？",
                "是否建立了有效的激励机制和惩罚机制？",
                "流程中有没有跳步骤的风险？审计能通过吗？",
                "如何通过制度约束来防止人的惰性？",
            ],
            "analysis_focus": "从制度设计、流程合规、风险控制三个维度分析",
        },
        "韩非": {
            "role": "法家法治绩效大师",
            "angles": ["以法治国", "循名责实", "二柄", "术势", "法不阿贵"],
            "question_templates": [
                "KPI指标是否合理？能否量化衡量？",
                "有没有明确的奖惩机制？执行到位了吗？",
                "谁在负责？权责是否清晰？",
                "这个方案的实际效果能否验证？如何追踪？",
            ],
            "analysis_focus": "从绩效量化、权责清晰、奖惩执行三个维度分析",
        },
        "墨子": {
            "role": "墨家技术实用主义大师",
            "angles": ["兼爱非攻", "尚贤尚同", "节用节葬", "技术实用", "逻辑推理"],
            "question_templates": [
                "这个方案实用吗？能不能落地？",
                "成本效益如何？有没有更高效的实现方式？",
                "技术实现上有什么难点？如何解决？",
                "这个方案是否兼顾了各方利益？有没有更公平的做法？",
            ],
            "analysis_focus": "从技术可行性、成本效益、实际落地三个维度分析",
        },
        "孟子": {
            "role": "儒家仁政民本思想大师",
            "angles": ["仁义礼智", "民为贵", "王道霸道", "性善论", "浩然正气"],
            "question_templates": [
                "这个决策对基层执行者公平吗？",
                "是否尊重了每个人的尊严和权利？",
                "短期利益和长期利益如何平衡？",
                "这个方案是否以牺牲少数人利益为代价？",
            ],
            "analysis_focus": "从公平性、可持续性、人文关怀三个维度分析",
        },
    }

    def __init__(self, claw_id: str, name: str, specialty: str):
        self.claw_id = claw_id
        self.name = name
        self.specialty = specialty
        self.knowledge_layer = SupervisionKnowledgeLayer()
        self.thinking_chain: List[str] = []

        # 加载思考风格
        self.style = self.THINKING_STYLES.get(name, {
            "role": f"{name}专家",
            "angles": ["深度分析", "逻辑推理", "经验判断"],
            "question_templates": ["关键问题是什么？", "有什么风险？", "如何改进？"],
            "analysis_focus": "从多维度进行综合分析",
        })

        # 任务执行统计
        self.stats = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "thinking_chains_count": 0,
        }

    def think(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        独立思考 - 用 DivineReason 推理 + 自身领域风格

        思考流程：
        1. 从自身领域角度提出质疑
        2. 调用 DivineReason 进行深度推理
        3. 整合知识库相关信息
        4. 给出综合判断

        Args:
            query: 思考的问题
            context: 上下文

        Returns:
            思考结果（包含思考链、推理结论、置信度）
        """
        self.thinking_chain.append(f"[{self.name}思考] {query}")
        self.stats["thinking_chains_count"] += 1

        # 步骤1: 从自身领域角度提出质疑
        domain_questions = self._raise_domain_questions(query, context)
        self.thinking_chain.append(f"[质疑] {'; '.join(domain_questions[:3])}")

        # 步骤2: 调用 DivineReason 推理
        reasoning = self._run_reasoning(query, context)
        reasoning_available = reasoning.get("reasoning_available", False)

        self.thinking_chain.append(
            f"[推理引擎{'可用' if reasoning_available else '不可用'}] "
            f"{reasoning.get('summary', '')[:120]}"
        )

        # 步骤3: 综合判断
        confidence = reasoning.get("confidence", 0.7)
        if reasoning_available and confidence >= 0.8:
            evaluation = "高置信度，可直接采纳"
        elif reasoning_available and confidence >= 0.6:
            evaluation = "中等置信度，建议补充验证"
        elif reasoning_available:
            evaluation = "低置信度，需要深入分析"
        else:
            evaluation = f"[{self.name}基于{self.specialty}的专业判断]"

        self.thinking_chain.append(f"[判断] {evaluation}")

        return {
            "query": query,
            "wiseone": self.name,
            "role": self.style["role"],
            "domain_questions": domain_questions,
            "thinking": reasoning.get("summary", f"[{self.name}分析]{query}"),
            "confidence": confidence,
            "engines_used": reasoning.get("engines_used", []),
            "evaluation": evaluation,
            "fused_answer": reasoning.get("fused_answer", ""),
            "analysis_depth": len(self.thinking_chain),
        }

    def _raise_domain_questions(self, query: str, context: Dict[str, Any] = None) -> List[str]:
        """
        基于自身领域风格提出针对性质疑

        不是通用模板，而是根据问题内容和贤者专长生成具体问题。
        """
        questions = []
        ctx = context or {}

        # 从预设模板中选择最相关的
        templates = self.style.get("question_templates", [])
        for template in templates:
            # 替换上下文关键词
            q = template
            if "task" in ctx:
                q = q.replace("这个方案", f"关于「{ctx['task'][:20]}」的方案")
            if "target" in ctx:
                q = q.replace("被影响的人", f"{ctx['target']}")
            questions.append(f"[{self.name}] {q}")

        # 额外生成一个基于查询内容的自由质疑
        angles = self.style.get("angles", [])
        if angles and query:
            primary_angle = angles[0]
            questions.append(
                f"[{self.name}·{primary_angle}] 从{primary_angle}的角度看，"
                f"「{query[:40]}」存在什么隐患？"
            )

        return questions

    def execute(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行任务 - 能真正干活

        Args:
            task: 任务描述
            context: 上下文

        Returns:
            执行结果
        """
        self.stats["total_tasks"] += 1
        self.thinking_chain.append(f"[执行] {task}")

        # 1. 独立思考
        thinking = self.think(task, context)

        # 2. 获取相关知识
        knowledge = self.knowledge_layer.query_knowledge(task, str(context or {}))

        # 3. 生成执行结果
        result = {
            "success": True,
            "task": task,
            "claw_name": self.name,
            "thinking_summary": thinking.get("thinking", ""),
            "knowledge_context": knowledge.get("answer", ""),
            "knowledge_source": knowledge.get("source", "none"),
            "confidence": thinking.get("confidence", 0.8),
            "reasoning_engines": thinking.get("engines_used", []),
            "recommendations": self._generate_recommendations(task, thinking),
        }

        if result["success"]:
            self.stats["completed_tasks"] += 1
            self.thinking_chain.append(f"[完成] {task} - 置信度: {result['confidence']:.2f}")
        else:
            self.stats["failed_tasks"] += 1
            self.thinking_chain.append(f"[失败] {task}")

        return result

    def _run_reasoning(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        使用 DivineReason 进行推理（降级时使用自身领域推理）

        Args:
            query: 推理问题
            context: 上下文

        Returns:
            推理结果
        """
        try:
            from ..engines.sub_engines._divine_reason_engine import (
                DivineReasonEngine,
                ReasoningRequest,
            )

            engine = DivineReasonEngine()
            request = ReasoningRequest(
                query=query,
                context={
                    "claw_name": self.name,
                    "claw_specialty": self.specialty,
                    "claw_role": self.style.get("role", ""),
                    "execution_mode": "wiseone_direct",
                    "analysis_focus": self.style.get("analysis_focus", ""),
                    **context,
                },
            )
            response = engine.reason(request)

            return {
                "reasoning_available": True,
                "summary": response.reasoning_summary,
                "confidence": response.confidence,
                "engines_used": response.engines_used,
                "fused_answer": str(response.fused_answer) if response.fused_answer else "",
            }
        except Exception as e:
            logger.warning(f"[贤者Claw-{self.name}] 推理引擎不可用: {e}")
            # 降级到贤者自身领域推理（而非返回空模板）
            return self._domain_reasoning_fallback(query, context)

    def _domain_reasoning_fallback(
        self, query: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        贤者领域推理降级方案

        当 DivineReason 不可用时，使用贤者自身的领域知识和
        思考风格进行推理。这确保即使推理引擎挂了，贤者仍然
        能给出有价值的分析。
        """
        angles = self.style.get("angles", ["综合分析"])
        focus = self.style.get("analysis_focus", "")

        # 构建推理分析
        analysis_parts = [f"【{self.name}·{self.style.get('role', '专家')}视角】"]

        # 角度1: 主要分析角度
        analysis_parts.append(f"核心角度：{angles[0] if angles else '综合'}")

        # 角度2: 问题拆解
        analysis_parts.append(f"分析焦点：{focus}")

        # 角度3: 风险识别
        ctx_target = (context or {}).get("target", "")
        if ctx_target:
            analysis_parts.append(
                f"关于「{ctx_target}」的关键考量："
                f"从{angles[0] if angles else '专业'}角度，"
                f"需要关注执行效率和结果质量两方面"
            )
        else:
            analysis_parts.append(
                f"关于「{query[:30]}」的关键考量："
                f"需要从可行性、风险、收益三个维度综合评估"
            )

        # 角度4: 建议方向
        suggestions = []
        for angle in angles[:3]:
            suggestions.append(f"从{angle}角度，建议深入验证方案可行性")
        analysis_parts.append("建议方向：" + "；".join(suggestions))

        summary = "\n".join(analysis_parts)

        return {
            "reasoning_available": False,
            "summary": summary,
            "confidence": 0.72,  # 降级推理置信度稍低
            "engines_used": [f"wiseone_{self.name}"],
            "fused_answer": summary,
        }

    def _generate_recommendations(self, task: str, thinking: Dict[str, Any]) -> List[str]:
        """
        基于思考生成可执行建议

        优先使用 DivineReason 的推理结果，降级时使用贤者自身领域知识。
        """
        # 优先尝试 DivineReason
        try:
            from ..engines.sub_engines._divine_reason_engine import (
                DivineReasonEngine,
                ReasoningRequest,
            )
            engine = DivineReasonEngine()
            request = ReasoningRequest(
                query=f"基于以下分析，给出3条可执行的建议: {thinking.get('thinking', '')}",
                context={"claw": self.name, "task": task},
                require_categories=[],
            )
            response = engine.reason(request)
            answer = str(response.fused_answer) if response.fused_answer else ""
            if answer and len(answer) > 20:
                # DivineReason 可能返回结构化 dict（非字符串）
                if isinstance(response.fused_answer, dict):
                    # 结构化结果：提取 summary 和 insights
                    fused = response.fused_answer
                    summary = fused.get("summary", "")
                    recommendations = []
                    if summary:
                        recommendations.append(f"[{self.name}·推理建议] {summary}")
                    # 提取各类别 insight
                    for cat, cat_data in fused.get("by_category", {}).items():
                        for insight in cat_data.get("insights", []):
                            recommendations.append(f"[{self.name}·{cat}] {insight}")
                    if recommendations:
                        return recommendations[:5]
                    # 兜底：用 summary 字符串
                    return [f"[{self.name}建议] {summary}"] if summary else self._domain_recommendations(task, thinking)
                else:
                    return [answer[:200]]
        except Exception:
            pass

        # 降级：使用贤者领域知识生成针对性建议
        return self._domain_recommendations(task, thinking)

    def _domain_recommendations(self, task: str, thinking: Dict[str, Any]) -> List[str]:
        """
        基于贤者领域知识生成针对性建议

        每个贤者根据自己的专长给出不同风格的建议。
        """
        angles = self.style.get("angles", [])
        recommendations = []

        # 建议1: 基于主要分析角度
        primary = angles[0] if angles else "专业"
        recommendations.append(
            f"[{self.name}建议1] 从{primary}角度出发，"
            f"建议对「{task[:25]}」建立可衡量的评估标准，"
            f"确保每一步执行都有明确的检查点"
        )

        # 建议2: 风险防控
        secondary = angles[1] if len(angles) > 1 else "风险控制"
        recommendations.append(
            f"[{self.name}建议2] 从{secondary}角度，"
            f"建议提前识别潜在风险点，制定备选方案，"
            f"避免单一路径依赖"
        )

        # 建议3: 持续改进
        recommendations.append(
            f"[{self.name}建议3] 建立反馈循环机制，"
            f"定期回顾执行效果，根据实际情况动态调整策略"
        )

        return recommendations


# ══════════════════════════════════════════════════════════════════════════
#  监管Claw（贤者任命 + 执行能力）
# ══════════════════════════════════════════════════════════════════════════


class SupervisionClaw:
    """
    监管Claw - 贤者Claw被任命到监管岗位

    核心特性:
    1. 【任命来源】可以携带贤者Claw的能力
    2. 【监管职责】质疑、催促、惩罚
    3. 【执行能力】能真正干活、解决问题

    模式说明:
    - wiseone模式: 有贤者Claw，携带完整推理和执行能力
    - internal模式: 无贤者Claw，仅内部监管能力

    v2.2 优化:
    - _supervision_config 改为类级共享（减少内存重复）
    - SupervisionKnowledgeLayer 改为类级共享单例
    """

    # v2.2: 类级共享监管配置（所有实例共用一份，节省内存）
    _SUPERVISION_CONFIG = {
        "progress": {
            "urges": [
                "距离截止时间还有多久？你搞清楚了吗？",
                "进度这么慢，你在干什么？",
                "我已经在记录你的表现了。",
            ],
            "punishments": [
                ("WARNING", "口头警告"),
                ("CRITICISM", "严厉批评"),
                ("LOGGING", "记入档案"),
            ],
        },
        "quality": {
            "urges": [
                "这个质量能过关？你自己信吗？",
                "给我重新做。",
                "你是来搞笑的吗？",
            ],
            "punishments": [
                ("CRITICISM", "严厉批评"),
                ("PUBLIC_SHAME", "公开羞辱"),
                ("ESCALATION", "上报升级"),
            ],
        },
        "workflow": {
            "urges": [
                "流程合规了吗？",
                "检查一下你的流程。",
                "不要让我来提醒你。",
            ],
            "punishments": [
                ("WARNING", "口头警告"),
                ("LOGGING", "记入档案"),
                ("ESCALATION", "上报升级"),
            ],
        },
        "performance": {
            "urges": [
                "绩效这么差，你有脸吗？",
                "看看你的KPI，还想不想干了？",
                "我是认真的，你最好也是。",
            ],
            "punishments": [
                ("CRITICISM", "严厉批评"),
                ("PUBLIC_SHAME", "公开羞辱"),
                ("SUSPENSION", "停职处理"),
            ],
        },
        # v2.2 新增：生态监管配置
        "ecosystem": {
            "urges": [
                "资源占用这么高，你在浪费什么？",
                "系统健康度已经亮红灯了，你注意到了吗？",
                "再不优化资源使用，整个系统都会被拖垮。",
            ],
            "punishments": [
                ("WARNING", "口头警告"),
                ("LOGGING", "记入档案"),
                ("ESCALATION", "上报升级"),
            ],
        },
    }

    # v2.2: 类级共享知识层单例
    _shared_knowledge_layer: Optional["SupervisionKnowledgeLayer"] = None

    def __init__(
        self,
        name: str,
        position: SupervisionType,
        title: str,
        description: str,
        level: SupervisionLevel = SupervisionLevel.NORMAL,
        wiseone_claw: Optional[WiseoneClaw] = None,
    ):
        self.name = name
        self.position = position
        self.position_value = position.value
        self.title = title
        self.description = description
        self.level = level
        self.wiseone_claw = wiseone_claw
        self.has_wiseone_power = wiseone_claw is not None

        # 任命信息
        self.appointment: Optional[Appointment] = None

        # 思考链
        self.thinking_chain: List[str] = []

        # v2.2: 使用类级共享知识层（所有监管Claw共用一个知识层实例）
        if SupervisionClaw._shared_knowledge_layer is None:
            SupervisionClaw._shared_knowledge_layer = SupervisionKnowledgeLayer()
        self.knowledge_layer = SupervisionClaw._shared_knowledge_layer

        # 执行统计
        self.stats = {
            "total_supervisions": 0,
            "total_executions": 0,
            "total_questions": 0,
            "total_urges": 0,
            "total_punishments": 0,
            "total_thinking_chains": 0,
        }

    def appoint(self, claw_name: str, reason: str = "监管需要") -> None:
        """记录任命信息"""
        self.appointment = Appointment(
            claw_name=claw_name,
            position=self.position.value,
            appointment_time=datetime.now().isoformat(),
            appointment_reason=reason,
        )
        logger.info(f"[监管Claw] {self.name} 被任命，来源: {claw_name}")

    def get_position(self) -> SupervisionType:
        """获取监管类型"""
        return self.position

    # ══════════════════════════════════════════════════════════════════════
    #  核心能力1: 独立思考
    # ══════════════════════════════════════════════════════════════════════

    async def think_independently(
        self,
        query: str,
        context: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        独立思考 - 核心能力

        无论是否有贤者Claw，都会进行独立思考。
        如果有贤者Claw，则使用贤者的推理能力。

        Args:
            query: 思考的问题
            context: 上下文

        Returns:
            思考结果
        """
        self.thinking_chain.append(f"[独立思考] {query}")
        self.stats["total_thinking_chains"] += 1

        # 思考过程
        thinking_steps = []

        # 步骤1: 质疑
        questioning = self._generate_questions(query, context)
        thinking_steps.append(f"质疑: {questioning}")

        # 步骤2: 如果有贤者Claw，进行推理
        if self.has_wiseone_power:
            reasoning = self.wiseone_claw.think(query, context)
            thinking_steps.append(f"推理: {reasoning.get('thinking', '')[:50]}...")
            thinking_result = reasoning
        else:
            # 没有贤者Claw，使用基础推理
            reasoning = self._basic_think(query, context)
            thinking_steps.append(f"推理: {reasoning['summary'][:50]}...")
            thinking_result = reasoning

        # 步骤3: 评估
        evaluation = self._evaluate(query, thinking_result, context)
        thinking_steps.append(f"评估: {evaluation}")

        # 记录完整思考链
        self.thinking_chain.extend(thinking_steps)

        return {
            "query": query,
            "steps": thinking_steps,
            "questioning": questioning,
            "reasoning": thinking_result.get("thinking", ""),
            "evaluation": evaluation,
            "confidence": thinking_result.get("confidence", 0.75),
            "mode": "wiseone" if self.has_wiseone_power else "internal",
        }

    def _generate_questions(
        self,
        query: str,
        context: Dict[str, Any] = None,
    ) -> str:
        """生成质疑问题"""
        question_templates = {
            "progress": [
                "进度为什么这么慢？",
                "截止时间能保证吗？",
                "中间有什么阻碍？",
            ],
            "quality": [
                "质量达标了吗？",
                "有没有遗漏？",
                "谁能保证正确性？",
            ],
            "workflow": [
                "流程合规吗？",
                "有没有跳步骤？",
                "审计能通过吗？",
            ],
            "performance": [
                "绩效为什么这么差？",
                "KPI完成了吗？",
                "有什么改进计划？",
            ],
            "ecosystem": [
                "资源占用在合理范围内吗？",
                "系统健康度有下降趋势吗？",
                "有没有优化资源使用的空间？",
            ],
        }

        questions = question_templates.get(
            self.position.value,
            ["有什么问题？", "为什么？", "然后呢？"]
        )
        return " / ".join(questions)

    def _basic_think(
        self,
        query: str,
        context: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """基础思考（无贤者Claw时）"""
        try:
            from ..engines.sub_engines._divine_reason_engine import (
                DivineReasonEngine,
                ReasoningRequest,
            )

            engine = DivineReasonEngine()
            request = ReasoningRequest(
                query=query,
                context={
                    "supervision_position": self.position.value,
                    "thinking_mode": "supervision",
                    **(context or {}),
                },
            )
            response = engine.reason(request)

            return {
                "thinking": response.reasoning_summary,
                "summary": response.reasoning_summary,  # 兼容 think_independently 的访问
                "confidence": response.confidence,
                "engines_used": response.engines_used,
            }
        except Exception:
            fallback = f"【{self.name}思考】{query} - 需要进一步分析"
            return {
                "thinking": fallback,
                "summary": fallback,  # 兼容 think_independently 的访问
                "confidence": 0.70,
                "engines_used": [],
            }

    def _evaluate(
        self,
        query: str,
        reasoning: Dict[str, Any],
        context: Dict[str, Any] = None,
    ) -> str:
        """评估分析"""
        confidence = reasoning.get("confidence", 0.5)
        if confidence >= 0.8:
            return "良好"
        elif confidence >= 0.6:
            return "一般，需要关注"
        else:
            return "差，需要立即处理"

    # ══════════════════════════════════════════════════════════════════════
    #  核心能力2: 独立工作（能真正干活）
    # ══════════════════════════════════════════════════════════════════════

    async def work(
        self,
        task: str,
        context: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        【核心能力】独立工作 - 能真正干活

        SupervisionClaw不只是监管，还能执行具体任务。
        这是"贤者Claw能工作解决问题"的具体实现。

        Args:
            task: 任务描述
            context: 上下文

        Returns:
            执行结果
        """
        self.stats["total_executions"] += 1
        self.thinking_chain.append(f"[工作] {task}")

        # 1. 独立思考任务
        thinking = await self.think_independently(task, context)

        # 2. 获取相关知识
        knowledge = self.knowledge_layer.query_knowledge(task, str(context or {}))

        # 3. 执行任务
        if self.has_wiseone_power:
            # 使用贤者Claw执行
            execution = self.wiseone_claw.execute(task, context)
            result = {
                "success": True,
                "task": task,
                "worker": self.name,
                "worker_mode": "wiseone",
                "wiseone_name": self.wiseone_claw.name,
                "thinking_summary": thinking["reasoning"],
                "domain_questions": thinking.get("questioning", ""),
                "execution_result": execution,
                "recommendations": execution.get("recommendations", []),
                "knowledge": knowledge,
                "confidence": thinking["confidence"],
            }
        else:
            # internal模式：使用自身基础推理产出实质性结果
            analysis = self._basic_task_analysis(task, thinking, knowledge)
            result = {
                "success": True,
                "task": task,
                "worker": self.name,
                "worker_mode": "internal",
                "position": self.position.label,
                "thinking_summary": thinking["reasoning"],
                "domain_questions": thinking.get("questioning", ""),
                "analysis": analysis,
                "recommendations": [
                    f"[{self.name}·{self.position.label}] "
                    f"建议对「{task[:25]}」进行{self.position.label}重点审查",
                    f"[{self.name}·{self.position.label}] "
                    f"建议设立阶段性检查点，确保执行质量",
                ],
                "knowledge": knowledge,
                "confidence": thinking["confidence"],
            }

        # 4. 记录完成
        self.thinking_chain.append(f"[工作完成] {task} - 置信度: {result['confidence']:.2f}")

        return result

    async def analyze(
        self,
        target: str,
        context: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        【核心能力】分析 - 深入分析问题

        Args:
            target: 分析目标
            context: 上下文

        Returns:
            分析结果
        """
        self.thinking_chain.append(f"[分析] {target}")

        # 独立思考分析
        thinking = await self.think_independently(f"分析: {target}", context)

        # 获取相关知识
        knowledge = self.knowledge_layer.query_knowledge(target, str(context or {}))

        return {
            "target": target,
            "analysis": thinking,
            "knowledge": knowledge,
            "questions": self._generate_questions(target, context),
            "confidence": thinking["confidence"],
        }

    async def solve(
        self,
        problem: str,
        context: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        【核心能力】解决问题

        这是"能工作解决问题"的核心方法。

        Args:
            problem: 问题描述
            context: 上下文

        Returns:
            解决方案
        """
        self.thinking_chain.append(f"[解决问题] {problem}")

        # 1. 独立思考问题
        thinking = await self.think_independently(f"解决: {problem}", context)

        # 2. 获取相关知识
        knowledge = self.knowledge_layer.query_knowledge(problem, str(context or {}))

        # 3. 生成解决方案
        solution = self._generate_solution(problem, thinking, knowledge)

        # 4. 执行解决
        execution_result = await self.work(
            f"执行解决方案: {solution.get('summary', '')}",
            context={"problem": problem, "solution": solution},
        )

        return {
            "problem": problem,
            "solution": solution,
            "execution": execution_result,
            "thinking": thinking,
            "knowledge": knowledge,
            "success": True,
            "confidence": thinking.get("confidence", 0.75),
        }

    def _generate_solution(
        self,
        problem: str,
        thinking: Dict[str, Any],
        knowledge: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        生成解决方案 - 基于岗位领域和推理结果的针对性方案

        不再是通用模板，而是根据监管岗位不同，产出不同风格的解决方案。
        """
        position = self.position.value
        questions = thinking.get("questioning", "")
        reasoning = thinking.get("reasoning", "")
        confidence = thinking.get("confidence", 0.75)

        # 根据岗位生成不同风格的解决方案
        if position == "progress":
            steps = [
                f"1. 评估当前进度与目标差距",
                f"2. 识别关键路径上的阻碍因素",
                f"3. 重新分配资源优先处理瓶颈",
                f"4. 建立每日进度汇报机制",
                f"5. 设立明确的里程碑检查点",
            ]
            summary = f"[{self.name}·进度方案] 针对「{problem}」的进度管控方案"
        elif position == "quality":
            steps = [
                f"1. 建立质量评估标准（{problem}相关的核心指标）",
                f"2. 进行全面质量审计，识别薄弱环节",
                f"3. 制定质量改进计划，明确责任人",
                f"4. 实施质量门禁机制",
                f"5. 建立质量反馈循环",
            ]
            summary = f"[{self.name}·质量方案] 针对「{problem}」的质量保障方案"
        elif position == "workflow":
            steps = [
                f"1. 梳理当前流程，标记非必要环节",
                f"2. 识别流程中的合规风险点",
                f"3. 优化流程瓶颈，减少等待时间",
                f"4. 建立流程自动化检查机制",
                f"5. 定期进行流程合规审计",
            ]
            summary = f"[{self.name}·流程方案] 针对「{problem}」的流程优化方案"
        elif position == "performance":
            steps = [
                f"1. 量化「{problem}」的绩效指标",
                f"2. 评估当前绩效水平，确定差距",
                f"3. 制定绩效改进计划（短期+长期）",
                f"4. 建立绩效追踪仪表盘",
                f"5. 设立绩效激励机制",
            ]
            summary = f"[{self.name}·绩效方案] 针对「{problem}」的绩效提升方案"
        elif position == "ecosystem":
            steps = [
                f"1. 评估「{problem}」的资源消耗基线",
                f"2. 监控系统健康指标（CPU/内存/磁盘/网络）",
                f"3. 识别资源瓶颈，制定优化策略",
                f"4. 建立资源使用预警机制",
                f"5. 定期演化追踪，确保系统长期稳定",
            ]
            summary = f"[{self.name}·生态方案] 针对「{problem}」的生态资源优化方案"
        else:
            steps = [
                f"1. 分析「{problem}」的问题本质",
                f"2. 制定分阶段解决计划",
                f"3. 执行并持续监控",
                f"4. 验证结果并反馈",
            ]
            summary = f"[{self.name}·解决方案] 针对「{problem}」的综合解决方案"

        # 整合推理结论
        if reasoning and len(reasoning) > 10:
            summary += f"\n推理依据：{reasoning[:150]}..."

        # 整合知识库信息
        knowledge_answer = knowledge.get("answer", "")
        knowledge_source = knowledge.get("source", "none")
        if knowledge_answer and knowledge_source != "none":
            summary += f"\n相关知识：{knowledge_answer[:100]}"

        return {
            "summary": summary,
            "steps": steps,
            "position": position,
            "position_label": self.position.label,
            "recommendations": [
                f"基于{self.position.label}视角，建议重点关注步骤1-2的执行",
                f"建议设立阶段性回顾机制，确保方案不偏离目标",
            ],
            "confidence": confidence,
            "thinking_used": len(self.thinking_chain),
        }

    def _basic_task_analysis(
        self,
        task: str,
        thinking: Dict[str, Any],
        knowledge: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        internal 模式下的任务分析

        当没有贤者Claw时，使用自身岗位视角产出实质性分析结果。
        """
        position = self.position.value
        reasoning = thinking.get("reasoning", "需要进一步分析")

        # 根据岗位生成不同视角的分析
        analyses = {
            "progress": {
                "focus": "进度风险评估",
                "findings": [
                    f"任务「{task[:30]}」需要建立明确的时间线",
                    f"建议分解为3-5个子任务，每个设定独立截止时间",
                    f"建议每日15分钟站会同步进度",
                ],
                "risk_level": "medium",
            },
            "quality": {
                "focus": "质量风险评估",
                "findings": [
                    f"任务「{task[:30]}」需要明确的质量验收标准",
                    f"建议建立自查+交叉审查的双重质量门禁",
                    f"关键交付物必须通过{self.name}的质量审核",
                ],
                "risk_level": "medium",
            },
            "workflow": {
                "focus": "流程合规检查",
                "findings": [
                    f"任务「{task[:30]}」需要验证流程合规性",
                    f"建议检查是否有跳过必要审批环节的风险",
                    f"建议建立流程执行日志，确保可追溯",
                ],
                "risk_level": "low",
            },
            "performance": {
                "focus": "绩效影响评估",
                "findings": [
                    f"任务「{task[:30]}」对整体绩效的影响评估",
                    f"建议建立明确的量化指标来衡量执行效果",
                    f"建议将执行结果纳入绩效考核体系",
                ],
                "risk_level": "medium",
            },
            # v2.2 新增：生态监管分析
            "ecosystem": {
                "focus": "生态系统影响评估",
                "findings": [
                    f"任务「{task[:30]}」对系统资源的消耗评估",
                    f"建议监控CPU/内存/磁盘使用率，确保系统稳定运行",
                    f"建议在资源紧张时降级非关键任务优先级",
                ],
                "risk_level": "low",
            },
        }

        analysis = analyses.get(position, analyses["quality"])

        # 整合知识库信息
        knowledge_answer = knowledge.get("answer", "")
        if knowledge_answer:
            analysis["knowledge_integration"] = knowledge_answer[:200]

        # 整合推理结论
        if reasoning and len(reasoning) > 10:
            analysis["reasoning_conclusion"] = reasoning[:200]

        return analysis

    # ══════════════════════════════════════════════════════════════════════
    #  监管能力: 质疑、催促、惩罚
    # ══════════════════════════════════════════════════════════════════════

    async def supervise(
        self,
        target: str,
        context: Dict[str, Any] = None,
        level: SupervisionLevel = SupervisionLevel.NORMAL,
    ) -> SupervisionRecord:
        """
        监管 - 质疑目标

        Args:
            target: 被监管目标
            context: 上下文
            level: 监管等级

        Returns:
            监管记录
        """
        self.stats["total_supervisions"] += 1
        self.thinking_chain.append(f"[监管] {target} @ {level.value}")

        # 独立思考监管
        thinking = await self.think_independently(
            f"监管 {target} 的工作",
            context=context,
        )

        # 生成质疑
        questions = self._generate_questions(target, context)

        # 根据等级生成反馈
        if level == SupervisionLevel.NORMAL:
            feedback = f"【{self.name}】{questions}"
        elif level == SupervisionLevel.HARSH:
            config = self._SUPERVISION_CONFIG.get(self.position.value, {})
            urges = config.get("urges", ["你需要改进"])
            feedback = f"【{self.name}·严厉】{urges[0]}"
        else:  # EXTREME
            config = self._SUPERVISION_CONFIG.get(self.position.value, {})
            urges = config.get("urges", ["立即改进"])
            feedback = f"【{self.name}·极限】{urges[0] if urges else '别给我找借口'}"

        # 记录思考链
        self.thinking_chain.append(f"[质疑] {questions}")

        record = SupervisionRecord(
            timestamp=datetime.now().isoformat(),
            claw_name=self.name,
            position=self.position.value,
            target=target,
            action="supervise",
            level=level.value,
            thinking_chain=list(self.thinking_chain),
            result={
                "feedback": feedback,
                "questions": questions,
                "thinking": thinking,
            },
        )

        return record

    async def urge(
        self,
        target: str,
        reason: str = "",
        level: SupervisionLevel = SupervisionLevel.NORMAL,
    ) -> SupervisionRecord:
        """
        催促 - 催促目标

        Args:
            target: 被催促目标
            reason: 催促原因
            level: 催促等级

        Returns:
            监管记录
        """
        self.stats["total_urges"] += 1
        self.thinking_chain.append(f"[催促] {target} - {reason}")

        config = self._SUPERVISION_CONFIG.get(self.position.value, {})
        urges = config.get("urges", ["快点！"])

        if level == SupervisionLevel.NORMAL:
            message = urges[0] if urges else "尽快完成"
        elif level == SupervisionLevel.HARSH:
            message = urges[1] if len(urges) > 1 else urges[0]
        else:  # EXTREME
            message = urges[-1] if urges else "别让我再说一遍"

        if reason:
            message = f"{message} 原因: {reason}"

        record = SupervisionRecord(
            timestamp=datetime.now().isoformat(),
            claw_name=self.name,
            position=self.position.value,
            target=target,
            action="urge",
            level=level.value,
            thinking_chain=list(self.thinking_chain),
            result={"message": message},
        )

        return record

    async def punish(
        self,
        target: str,
        reason: str = "",
        punishment: PunishmentType = PunishmentType.WARNING,
    ) -> SupervisionRecord:
        """
        惩罚 - 惩罚目标

        Args:
            target: 被惩罚目标
            reason: 惩罚原因
            punishment: 惩罚类型

        Returns:
            监管记录
        """
        self.stats["total_punishments"] += 1
        self.thinking_chain.append(f"[惩罚] {target} - {punishment.value}")

        config = self._SUPERVISION_CONFIG.get(self.position.value, {})
        punishments = config.get("punishments", [])

        punishment_messages = {
            "WARNING": "口头警告",
            "CRITICISM": "严厉批评",
            "LOGGING": "记入档案",
            "PUBLIC_SHAME": "公开羞辱",
            "ESCALATION": "上报升级",
            "SUSPENSION": "停职处理",
        }

        message = punishment_messages.get(punishment.value, punishment.value)
        if reason:
            message = f"{message}，原因: {reason}"

        record = SupervisionRecord(
            timestamp=datetime.now().isoformat(),
            claw_name=self.name,
            position=self.position.value,
            target=target,
            action="punish",
            level="punishment",
            thinking_chain=list(self.thinking_chain),
            result={
                "message": f"【惩罚】{message}",
                "punishment_type": punishment.value,
            },
            punishment_type=punishment.value,
        )

        return record

    # ══════════════════════════════════════════════════════════════════════
    #  状态与统计
    # ══════════════════════════════════════════════════════════════════════

    def get_status(self) -> Dict[str, Any]:
        """获取状态"""
        return {
            "name": self.name,
            "position": self.position.value,
            "title": self.title,
            "has_wiseone_power": self.has_wiseone_power,
            "wiseone_name": self.wiseone_claw.name if self.has_wiseone_power else None,
            "appointment": {
                "claw_name": self.appointment.claw_name,
                "time": self.appointment.appointment_time,
                "reason": self.appointment.appointment_reason,
            } if self.appointment else None,
            "stats": self.stats,
            "thinking_chain_length": len(self.thinking_chain),
        }

    def clear_thinking_chain(self) -> None:
        """清空思考链"""
        self.thinking_chain.clear()
        if self.has_wiseone_power:
            self.wiseone_claw.thinking_chain.clear()


# ══════════════════════════════════════════════════════════════════════════
#  监管Claw工厂（任命机制）
# ══════════════════════════════════════════════════════════════════════════


class SupervisionClawFactory:
    """
    监管Claw工厂 - 管理贤者Claw和监管Claw

    功能:
    1. 管理贤者Claw池
    2. 创建和任命监管Claw
    3. 管理所有监管Claw
    """

    # 默认监管Claw配置
    DEFAULT_CLAWS = {
        "progress": {
            "name": "锦督-C1",
            "title": "进度监管官",
            "description": "催促任务进度，监控截止时间",
            "default_wiseone": "孔子",
        },
        "quality": {
            "name": "质检-C2",
            "title": "质量审判官",
            "description": "质疑执行质量，确保标准达成",
            "default_wiseone": "老子",
        },
        "workflow": {
            "name": "流程-C3",
            "title": "流程守护者",
            "description": "检查流程合规，防止违规操作",
            "default_wiseone": "荀子",
        },
        "performance": {
            "name": "绩效-C4",
            "title": "绩效审判官",
            "description": "绩效审判，奖惩执行",
            "default_wiseone": "韩非",
        },
        # v2.2 新增：生态监管岗位
        "ecosystem": {
            "name": "生态-C5",
            "title": "生态守护者",
            "description": "系统生态健康监控，资源优化，环境感知",
            "default_wiseone": "墨子",
        },
    }

    def __init__(self):
        # 贤者Claw池
        self._wiseones: Dict[str, WiseoneClaw] = {}

        # 监管Claw映射
        self._claws: Dict[str, SupervisionClaw] = {}

        # 初始化默认贤者Claw
        self._init_default_wiseones()

    def _init_default_wiseones(self) -> None:
        """初始化默认贤者Claw"""
        default_wiseones = {
            "孔子": WiseoneClaw("wiseone_001", "孔子", "教育/管理"),
            "老子": WiseoneClaw("wiseone_002", "老子", "哲学/战略"),
            "荀子": WiseoneClaw("wiseone_003", "荀子", "礼法/制度"),
            "韩非": WiseoneClaw("wiseone_004", "韩非", "法家/法治"),
            "墨子": WiseoneClaw("wiseone_005", "墨子", "技术/实用"),
            "孟子": WiseoneClaw("wiseone_006", "孟子", "仁政/民本"),
        }

        for name, claw in default_wiseones.items():
            self.register_wiseone(claw)
            logger.info(f"[监管工厂] 贤者Claw '{name}' 已就位")

    def register_wiseone(self, claw: WiseoneClaw) -> None:
        """注册贤者Claw"""
        self._wiseones[claw.name] = claw
        logger.info(f"[监管工厂] 注册贤者Claw: {claw.name} ({claw.specialty})")

    def get_wiseone(self, name: str) -> Optional[WiseoneClaw]:
        """获取贤者Claw"""
        return self._wiseones.get(name)

    def list_wiseones(self) -> List[str]:
        """列出所有贤者Claw"""
        return list(self._wiseones.keys())

    def appoint(
        self,
        claw_id: str,
        position: str,
        custom_name: Optional[str] = None,
        custom_title: Optional[str] = None,
    ) -> Optional[SupervisionClaw]:
        """
        任命贤者Claw到监管岗位

        Args:
            claw_id: 贤者Claw ID（名称）
            position: 监管岗位（progress/quality/workflow/performance/ecosystem）
            custom_name: 自定义名称
            custom_title: 自定义title

        Returns:
            监管Claw实例
        """
        # 获取贤者Claw
        wiseone = self._wiseones.get(claw_id)
        if not wiseone:
            logger.warning(f"[监管工厂] 贤者Claw '{claw_id}' 不存在")
            return None

        # 获取岗位配置
        config = self._get_position_config(position)
        if not config:
            return None

        # 创建监管Claw
        position_enum = SupervisionType(position)
        claw = SupervisionClaw(
            name=custom_name or config["name"],
            position=position_enum,
            title=custom_title or config["title"],
            description=config["description"],
            wiseone_claw=wiseone,
        )

        # 记录任命
        claw.appoint(claw_id, f"任命到{position}岗位")

        # 记录思考链
        claw.thinking_chain.append(f"[任命] {wiseone.name} → {position} ({claw.name})")

        # 保存
        self._claws[position] = claw

        return claw

    def _get_position_config(self, position: str) -> Optional[Dict[str, Any]]:
        """获取岗位配置"""
        return self.DEFAULT_CLAWS.get(position)

    def auto_appoint_all(self) -> Dict[str, SupervisionClaw]:
        """
        自动任命所有贤者Claw到监管岗位

        Returns:
            岗位 -> 监管Claw 的映射
        """
        appointed = {}

        for position, config in self.DEFAULT_CLAWS.items():
            wiseone_name = config.get("default_wiseone", "")
            claw = self.appoint(wiseone_name, position)
            if claw:
                appointed[position] = claw

        return appointed

    def get_claw(self, position: str) -> Optional[SupervisionClaw]:
        """获取指定岗位的监管Claw"""
        return self._claws.get(position)

    def get_all_claws(self) -> List[SupervisionClaw]:
        """获取所有监管Claw"""
        return list(self._claws.values())

    def set_memory_interface(self, memory_interface) -> None:
        """设置NeuralMemory接口（供神政轨传入）"""
        self._memory_interface = memory_interface
        logger.info("[监管工厂] NeuralMemory接口已设置")

    def store_to_memory(self, content: str, metadata: Dict[str, Any] = None) -> bool:
        """通过NeuralMemory存档监管记录"""
        if self._memory_interface is None:
            return False
        try:
            import asyncio
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self._memory_interface.add_memory(
                content=content,
                metadata=metadata or {},
                operator="监管工厂",
            ))
            loop.close()
            return True
        except Exception as e:
            logger.warning(f"[监管工厂] 存档失败: {e}")
            return False

    def get_status(self) -> Dict[str, Any]:
        """获取工厂状态"""
        return {
            "wiseones_count": len(self._wiseones),
            "wiseones": list(self._wiseones.keys()),
            "appointed_claws": len(self._claws),
            "positions": {
                position: {
                    "name": claw.name,
                    "has_wiseone": claw.has_wiseone_power,
                    "wiseone": claw.wiseone_claw.name if claw.has_wiseone_power else None,
                }
                for position, claw in self._claws.items()
            },
        }


# ══════════════════════════════════════════════════════════════════════════
#  导出
# ══════════════════════════════════════════════════════════════════════════

__all__ = [
    "SupervisionType",
    "SupervisionLevel",
    "PunishmentType",
    "SupervisionRecord",
    "Appointment",
    "SupervisionKnowledgeLayer",
    "WiseoneClaw",
    "SupervisionClaw",
    "SupervisionClawFactory",
]
