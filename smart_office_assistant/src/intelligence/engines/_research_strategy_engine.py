# -*- coding: utf-8 -*-
"""
研究发现驱动策略引擎 v2.0.0
Research-Driven Strategy Engine
====================================

核心理念：策略不是预设的，而是由研究发现动态生成的。
研究 → 发现 → 分类 → 策略生成 → 验证 → 入库 → 演化 → 迭代

与V1的关键区别：
- 四维分类框架（影响目标/作用对象/作用环节/作用机制）
- 7阶段策略生命周期状态机
- 策略关联网络（协同/冲突/前置/替代/组合）
- 研究发现到策略的自动映射与命名
- 策略验证闭环（生成→验证→入库/废弃）
- 策略版本管理与演化追踪

版本: v2.0.0
日期: 2026-04-23
"""

import json
import yaml
import logging
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field, asdict
from enum import Enum

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
# 枚举定义
# ═══════════════════════════════════════════════════════════════

class ImpactTarget(Enum):
    """影响目标 - 研究发现指向的业务目标"""
    GROWTH = "增长"          # 获客、规模
    CONVERSION = "转化"      # 成交、付费
    RETENTION = "留存"       # 复购、忠诚
    EFFICIENCY = "效率"      # 成本、速度
    INNOVATION = "创新"      # 产品、模式
    EXPERIENCE = "体验"      # 满意度、NPS


class TargetAudience(Enum):
    """作用对象 - 研究发现影响的人群"""
    NEW_USER = "新用户"
    EXISTING_USER = "存量用户"
    HIGH_VALUE = "高价值用户"
    CHURN_RISK = "流失风险用户"
    ALL_USERS = "全量用户"


class JourneyStage(Enum):
    """作用环节 - 用户旅程中的影响节点"""
    AWARENESS = "认知"       # 知道
    INTEREST = "兴趣"        # 想了解
    CONSIDERATION = "考虑"   # 对比
    PURCHASE = "购买"        # 决策
    USAGE = "使用"           # 体验
    ADVOCACY = "推荐"        # 传播


class Mechanism(Enum):
    """作用机制 - 研究发现产生效果的方式"""
    EMOTION_TRIGGER = "情绪触发"
    EMOTION_AMPLIFY = "情绪放大"
    EMOTION_CONVERT = "情绪转化"
    EMOTION_MAINTAIN = "情绪维系"
    EMOTION_REPAIR = "情绪修复"
    COGNITION_SHIFT = "认知转变"
    BEHAVIOR_NUDGE = "行为助推"


class StrategyLifecycleStage(Enum):
    """策略生命周期阶段"""
    DISCOVERY = "发现期"      # 研究产出
    GENERATION = "生成期"    # 策略文档生成
    VALIDATION = "验证期"    # A/B测试验证
    APPLICATION = "应用期"   # 规模应用
    MATURITY = "成熟期"      # 最佳实践
    DECLINE = "衰退期"      # 效果下降
    RETIRED = "退役"         # 归档保存


class StrategyRelationType(Enum):
    """策略间关系类型"""
    SYNERGY = "协同"         # 同时使用效果更好
    CONFLICT = "冲突"        # 互相抵消或冲突
    PREREQUISITE = "前置"    # A是B的前提
    SUBSTITUTE = "替代"      # A可以替代B
    COMBINATION = "组合"     # A+B形成新策略


class ValidationStatus(Enum):
    """验证状态"""
    PENDING = "待验证"
    IN_PROGRESS = "验证中"
    VALIDATED = "已验证"
    INVALIDATED = "已证伪"
    PARTIAL = "部分验证"


# ═══════════════════════════════════════════════════════════════
# 数据类定义
# ═══════════════════════════════════════════════════════════════

@dataclass
class FindingClassification:
    """研究发现四维分类"""
    impact_target: ImpactTarget
    target_audience: TargetAudience
    journey_stage: JourneyStage
    mechanism: Mechanism
    confidence: float = 0.0          # 置信度 0-1
    effect_size: float = 0.0         # 效应量 0-1
    replicability: float = 0.5       # 可复制性 0-1

    def to_dict(self) -> Dict:
        return {
            "impact_target": self.impact_target.value,
            "target_audience": self.target_audience.value,
            "journey_stage": self.journey_stage.value,
            "mechanism": self.mechanism.value,
            "confidence": round(self.confidence, 3),
            "effect_size": round(self.effect_size, 3),
            "replicability": round(self.replicability, 3),
        }


@dataclass
class ResearchFinding:
    """研究发现"""
    finding_id: str
    title: str
    description: str
    source: str                       # 来源（实验/调研/分析）
    evidence: List[str] = field(default_factory=list)
    classification: Optional[FindingClassification] = None
    scenarios: List[str] = field(default_factory=list)    # 归属应用场景
    value_types: List[str] = field(default_factory=list)  # 价值类型
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        d = {
            "finding_id": self.finding_id,
            "title": self.title,
            "description": self.description,
            "source": self.source,
            "evidence": self.evidence,
            "scenarios": self.scenarios,
            "value_types": self.value_types,
            "created_at": self.created_at,
        }
        if self.classification:
            d["classification"] = self.classification.to_dict()
        return d


@dataclass
class StrategyRelation:
    """策略间关系"""
    source_strategy_id: str
    target_strategy_id: str
    relation_type: StrategyRelationType
    strength: float = 0.5            # 关系强度 0-1
    description: str = ""

    def to_dict(self) -> Dict:
        return {
            "source": self.source_strategy_id,
            "target": self.target_strategy_id,
            "type": self.relation_type.value,
            "strength": round(self.strength, 3),
            "description": self.description,
        }


@dataclass
class StrategyVersion:
    """策略版本"""
    version: str
    date: str
    source_finding_ids: List[str]
    changes: str = ""
    validation_status: ValidationStatus = ValidationStatus.PENDING
    effect_data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "version": self.version,
            "date": self.date,
            "source_findings": self.source_finding_ids,
            "changes": self.changes,
            "validation_status": self.validation_status.value,
            "effect_data": self.effect_data,
        }


@dataclass
class Strategy:
    """策略"""
    strategy_id: str
    name: str
    description: str
    classification: FindingClassification
    lifecycle_stage: StrategyLifecycleStage = StrategyLifecycleStage.DISCOVERY

    # 内容
    content: str = ""
    application_guide: Dict[str, Any] = field(default_factory=dict)
    implementation_steps: List[str] = field(default_factory=list)

    # 验证
    validation_status: ValidationStatus = ValidationStatus.PENDING
    validation_plan: Dict[str, Any] = field(default_factory=dict)
    validation_results: List[Dict] = field(default_factory=list)

    # 版本
    current_version: str = "6.2.0"
    version_history: List[StrategyVersion] = field(default_factory=list)

    # 关联
    source_finding_ids: List[str] = field(default_factory=list)
    relations: List[StrategyRelation] = field(default_factory=list)
    related_scenarios: List[str] = field(default_factory=list)

    # 元数据
    priority: int = 5                # 1最高 10最低
    confidence: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return {
            "strategy_id": self.strategy_id,
            "name": self.name,
            "description": self.description,
            "classification": self.classification.to_dict(),
            "lifecycle_stage": self.lifecycle_stage.value,
            "content": self.content,
            "application_guide": self.application_guide,
            "implementation_steps": self.implementation_steps,
            "validation_status": self.validation_status.value,
            "validation_plan": self.validation_plan,
            "current_version": self.current_version,
            "source_finding_ids": self.source_finding_ids,
            "relations": [r.to_dict() for r in self.relations],
            "related_scenarios": self.related_scenarios,
            "priority": self.priority,
            "confidence": round(self.confidence, 3),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


# ═══════════════════════════════════════════════════════════════
# 命名规则与映射
# ═══════════════════════════════════════════════════════════════

# 策略自动命名规则：{作用机制}{影响目标}策略
_NAMING_TEMPLATE = "{mechanism}{target}策略"

# 影响目标 → 策略类型映射
_TARGET_STRATEGY_MAP = {
    ImpactTarget.GROWTH: "增长策略",
    ImpactTarget.CONVERSION: "转化策略",
    ImpactTarget.RETENTION: "留存策略",
    ImpactTarget.EFFICIENCY: "效率策略",
    ImpactTarget.INNOVATION: "创新策略",
    ImpactTarget.EXPERIENCE: "体验策略",
}

# 作用环节 → 应用阶段映射
_STAGE_APPLICATION_MAP = {
    JourneyStage.AWARENESS: "认知阶段干预",
    JourneyStage.INTEREST: "兴趣激发引导",
    JourneyStage.CONSIDERATION: "决策助推优化",
    JourneyStage.PURCHASE: "成交转化加速",
    JourneyStage.USAGE: "使用体验提升",
    JourneyStage.ADVOCACY: "口碑传播激发",
}


# ═══════════════════════════════════════════════════════════════
# 核心引擎
# ═══════════════════════════════════════════════════════════════

class ResearchStrategyEngine:
    """
    研究发现驱动策略引擎 v2.0

    核心闭环：
    研究发现录入 → 四维分类 → 自动策略生成 → 验证 → 入库 → 演化

    设计原则：
    1. 策略源于发现 - 没有研究发现，不生成策略
    2. 验证先于应用 - 新策略必须经过验证才能规模应用
    3. 持续监控迭代 - 策略效果持续监控，及时迭代
    4. 记录完整链路 - 从发现到策略到验证，完整记录
    5. 鼓励策略淘汰 - 无效策略及时退役，避免沉没成本
    """

    VERSION = "6.2.0"

    def __init__(self, data_dir: Optional[str] = None):
        """
        初始化引擎

        Args:
            data_dir: 数据持久化目录，为None时使用默认路径
        """
        if data_dir:
            self._data_dir = Path(data_dir)
        else:
            try:
                from src.core.paths import LEARNING_DIR
                self._data_dir = Path(LEARNING_DIR)
            except ImportError:
                self._data_dir = Path("data/learning")

        # 内存缓存
        self._findings: Dict[str, ResearchFinding] = {}
        self._strategies: Dict[str, Strategy] = {}
        self._relations: List[StrategyRelation] = []

        # 索引
        self._finding_index_by_target: Dict[ImpactTarget, List[str]] = {}
        self._strategy_index_by_lifecycle: Dict[StrategyLifecycleStage, List[str]] = {}
        self._strategy_index_by_scenario: Dict[str, List[str]] = {}

        # 加载持久化数据
        self._load_data()

    # ─────────────────────────────────────────────────
    # 研究发现录入
    # ─────────────────────────────────────────────────

    def record_finding(
        self,
        title: str,
        description: str,
        source: str,
        evidence: Optional[List[str]] = None,
        impact_target: Optional[str] = None,
        target_audience: Optional[str] = None,
        journey_stage: Optional[str] = None,
        mechanism: Optional[str] = None,
        confidence: float = 0.5,
        effect_size: float = 0.0,
        replicability: float = 0.5,
        scenarios: Optional[List[str]] = None,
        value_types: Optional[List[str]] = None,
    ) -> ResearchFinding:
        """
        记录研究发现

        如果未提供分类信息，将自动推断分类。

        Args:
            title: 发现标题
            description: 发现描述
            source: 来源（实验/调研/分析）
            evidence: 证据列表
            impact_target: 影响目标（增长/转化/留存/效率/创新/体验）
            target_audience: 作用对象（新用户/存量用户/...）
            journey_stage: 作用环节（认知/兴趣/.../推荐）
            mechanism: 作用机制（情绪触发/情绪放大/...）
            confidence: 置信度 0-1
            effect_size: 效应量 0-1
            replicability: 可复制性 0-1
            scenarios: 归属应用场景
            value_types: 价值类型

        Returns:
            ResearchFinding: 研究发现对象
        """
        finding_id = f"RF_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}"

        # 自动推断分类（如果未提供）
        classification = self._infer_classification(
            title=title,
            description=description,
            impact_target=impact_target,
            target_audience=target_audience,
            journey_stage=journey_stage,
            mechanism=mechanism,
            confidence=confidence,
            effect_size=effect_size,
            replicability=replicability,
        )

        finding = ResearchFinding(
            finding_id=finding_id,
            title=title,
            description=description,
            source=source,
            evidence=evidence or [],
            classification=classification,
            scenarios=scenarios or [],
            value_types=value_types or [],
        )

        self._findings[finding_id] = finding

        # 更新索引
        if classification:
            target = classification.impact_target
            if target not in self._finding_index_by_target:
                self._finding_index_by_target[target] = []
            self._finding_index_by_target[target].append(finding_id)

        self._persist_finding(finding)

        logger.info(f"研究发现已录入: {finding_id} - {title}")
        return finding

    def _infer_classification(
        self,
        title: str,
        description: str,
        impact_target: Optional[str],
        target_audience: Optional[str],
        journey_stage: Optional[str],
        mechanism: Optional[str],
        confidence: float,
        effect_size: float,
        replicability: float,
    ) -> FindingClassification:
        """自动推断研究发现分类"""
        content = f"{title} {description}".lower()

        # 映射影响目标
        target = self._map_enum(
            impact_target, ImpactTarget, content,
            {
                ImpactTarget.GROWTH: ["增长", "获客", "新用户", "扩张", "规模"],
                ImpactTarget.CONVERSION: ["转化", "成交", "付费", "购买", "客单"],
                ImpactTarget.RETENTION: ["留存", "复购", "忠诚", "粘性", "回流"],
                ImpactTarget.EFFICIENCY: ["效率", "成本", "速度", "自动化", "降本"],
                ImpactTarget.INNOVATION: ["创新", "新品", "差异化", "突破", "首创"],
                ImpactTarget.EXPERIENCE: ["体验", "满意", "NPS", "口碑", "好感"],
            },
            ImpactTarget.GROWTH,
        )

        # 映射作用对象
        audience = self._map_enum(
            target_audience, TargetAudience, content,
            {
                TargetAudience.NEW_USER: ["新用户", "潜客", "获客", "首购"],
                TargetAudience.EXISTING_USER: ["存量", "老用户", "复购", "活跃"],
                TargetAudience.HIGH_VALUE: ["高价值", "VIP", "大客", "核心用户"],
                TargetAudience.CHURN_RISK: ["流失", "沉默", "预警", "召回"],
                TargetAudience.ALL_USERS: ["全体", "全量", "所有用户"],
            },
            TargetAudience.EXISTING_USER,
        )

        # 映射作用环节
        stage = self._map_enum(
            journey_stage, JourneyStage, content,
            {
                JourneyStage.AWARENESS: ["认知", "知晓", "曝光", "覆盖"],
                JourneyStage.INTEREST: ["兴趣", "关注", "点击", "浏览"],
                JourneyStage.CONSIDERATION: ["考虑", "对比", "评估", "犹豫"],
                JourneyStage.PURCHASE: ["购买", "成交", "下单", "转化"],
                JourneyStage.USAGE: ["使用", "体验", "消费", "激活"],
                JourneyStage.ADVOCACY: ["推荐", "分享", "传播", "口碑"],
            },
            JourneyStage.PURCHASE,
        )

        # 映射作用机制
        mech = self._map_enum(
            mechanism, Mechanism, content,
            {
                Mechanism.EMOTION_TRIGGER: ["触发", "激发", "唤醒", "引起"],
                Mechanism.EMOTION_AMPLIFY: ["放大", "强化", "加深", "增强"],
                Mechanism.EMOTION_CONVERT: ["转化", "引导", "驱动", "推动"],
                Mechanism.EMOTION_MAINTAIN: ["维系", "维持", "保持", "延续"],
                Mechanism.EMOTION_REPAIR: ["修复", "挽回", "补救", "弥补"],
                Mechanism.COGNITION_SHIFT: ["认知", "观念", "意识", "理解"],
                Mechanism.BEHAVIOR_NUDGE: ["助推", "引导行为", "默认", "提示"],
            },
            Mechanism.EMOTION_TRIGGER,
        )

        return FindingClassification(
            impact_target=target,
            target_audience=audience,
            journey_stage=stage,
            mechanism=mech,
            confidence=confidence,
            effect_size=effect_size,
            replicability=replicability,
        )

    def _map_enum(
        self,
        value_str: Optional[str],
        enum_class: type,
        content: str,
        keyword_map: Dict[Any, List[str]],
        default: Any,
    ) -> Any:
        """通用枚举映射：优先使用显式值，否则从内容关键词推断"""
        # 显式值
        if value_str:
            for member in enum_class:
                if member.value == value_str or member.name == value_str.upper():
                    return member

        # 关键词推断
        for member, keywords in keyword_map.items():
            for kw in keywords:
                if kw in content:
                    return member

        return default

    # ─────────────────────────────────────────────────
    # 策略生成
    # ─────────────────────────────────────────────────

    def generate_strategy(
        self,
        finding_ids: List[str],
        custom_name: Optional[str] = None,
        custom_description: Optional[str] = None,
    ) -> Optional[Strategy]:
        """
        从研究发现生成策略

        策略命名规则：{作用机制}{影响目标}策略
        如：情绪触发转化策略、情绪维系留存策略

        Args:
            finding_ids: 研究发现ID列表
            custom_name: 自定义策略名（覆盖自动命名）
            custom_description: 自定义描述

        Returns:
            Strategy: 生成的策略，输入无效时返回None
        """
        # 收集有效发现
        findings = []
        for fid in finding_ids:
            if fid in self._findings:
                findings.append(self._findings[fid])

        if not findings:
            logger.warning("无有效研究发现，无法生成策略")
            return None

        # 聚合分类（取主导分类）
        classification = self._aggregate_classifications(findings)

        # 自动命名
        if custom_name:
            name = custom_name
        else:
            name = _NAMING_TEMPLATE.format(
                mechanism=classification.mechanism.value,
                target=classification.impact_target.value,
            )

        # 生成策略描述
        if custom_description:
            description = custom_description
        else:
            description = self._generate_strategy_description(findings, classification)

        # 生成策略内容
        content = self._generate_strategy_content(findings, classification)

        # 生成应用指南
        application_guide = self._generate_application_guide(classification)

        # 生成实施步骤
        steps = self._generate_implementation_steps(classification)

        # 计算优先级
        priority = self._calculate_priority(classification, findings)

        # 计算置信度
        confidence = self._calculate_strategy_confidence(findings, classification)

        strategy_id = f"STR_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}"

        # 创建初始版本记录
        initial_version = StrategyVersion(
            version="6.2.0",
            date=datetime.now().strftime('%Y-%m-%d'),
            source_finding_ids=[f.finding_id for f in findings],
            changes="初始版本",
            validation_status=ValidationStatus.PENDING,
        )

        strategy = Strategy(
            strategy_id=strategy_id,
            name=name,
            description=description,
            classification=classification,
            lifecycle_stage=StrategyLifecycleStage.GENERATION,
            content=content,
            application_guide=application_guide,
            implementation_steps=steps,
            validation_status=ValidationStatus.PENDING,
            current_version="6.2.0",
            version_history=[initial_version],
            source_finding_ids=[f.finding_id for f in findings],
            related_scenarios=list(set(
                s for f in findings for s in f.scenarios
            )),
            priority=priority,
            confidence=confidence,
        )

        self._strategies[strategy_id] = strategy

        # 更新索引
        lifecycle = strategy.lifecycle_stage
        if lifecycle not in self._strategy_index_by_lifecycle:
            self._strategy_index_by_lifecycle[lifecycle] = []
        self._strategy_index_by_lifecycle[lifecycle].append(strategy_id)

        for scenario in strategy.related_scenarios:
            if scenario not in self._strategy_index_by_scenario:
                self._strategy_index_by_scenario[scenario] = []
            self._strategy_index_by_scenario[scenario].append(strategy_id)

        # 自动检测策略关联
        self._detect_relations(strategy)

        self._persist_strategy(strategy)

        logger.info(f"策略已生成: {strategy_id} - {name}")
        return strategy

    def _aggregate_classifications(self, findings: List[ResearchFinding]) -> FindingClassification:
        """聚合多个发现的分类（取主导分类）"""
        # 统计各维度频率
        target_counts: Dict[ImpactTarget, int] = {}
        audience_counts: Dict[TargetAudience, int] = {}
        stage_counts: Dict[JourneyStage, int] = {}
        mechanism_counts: Dict[Mechanism, int] = {}

        total_confidence = 0.0
        total_effect = 0.0
        total_replicability = 0.0
        valid_count = 0

        for f in findings:
            if f.classification:
                c = f.classification
                target_counts[c.impact_target] = target_counts.get(c.impact_target, 0) + 1
                audience_counts[c.target_audience] = audience_counts.get(c.target_audience, 0) + 1
                stage_counts[c.journey_stage] = stage_counts.get(c.journey_stage, 0) + 1
                mechanism_counts[c.mechanism] = mechanism_counts.get(c.mechanism, 0) + 1
                total_confidence += c.confidence
                total_effect += c.effect_size
                total_replicability += c.replicability
                valid_count += 1

        if valid_count == 0:
            return FindingClassification(
                impact_target=ImpactTarget.GROWTH,
                target_audience=TargetAudience.EXISTING_USER,
                journey_stage=JourneyStage.PURCHASE,
                mechanism=Mechanism.EMOTION_TRIGGER,
            )

        # 取频率最高的维度值
        dominant_target = max(target_counts, key=target_counts.get) if target_counts else ImpactTarget.GROWTH
        dominant_audience = max(audience_counts, key=audience_counts.get) if audience_counts else TargetAudience.EXISTING_USER
        dominant_stage = max(stage_counts, key=stage_counts.get) if stage_counts else JourneyStage.PURCHASE
        dominant_mechanism = max(mechanism_counts, key=mechanism_counts.get) if mechanism_counts else Mechanism.EMOTION_TRIGGER

        return FindingClassification(
            impact_target=dominant_target,
            target_audience=dominant_audience,
            journey_stage=dominant_stage,
            mechanism=dominant_mechanism,
            confidence=total_confidence / valid_count,
            effect_size=total_effect / valid_count,
            replicability=total_replicability / valid_count,
        )

    def _generate_strategy_description(
        self, findings: List[ResearchFinding], classification: FindingClassification
    ) -> str:
        """生成策略描述"""
        parts = [
            f"基于{len(findings)}项研究发现，",
            f"通过{classification.mechanism.value}机制，",
            f"在用户{classification.journey_stage.value}环节，",
            f"对{classification.target_audience.value}施加影响，",
            f"实现{classification.impact_target.value}目标。",
        ]
        return "".join(parts)

    def _generate_strategy_content(
        self, findings: List[ResearchFinding], classification: FindingClassification
    ) -> str:
        """生成策略内容"""
        lines = [f"## 策略核心\n"]
        lines.append(f"**作用机制**: {classification.mechanism.value}")
        lines.append(f"**影响目标**: {classification.impact_target.value}")
        lines.append(f"**作用对象**: {classification.target_audience.value}")
        lines.append(f"**作用环节**: {classification.journey_stage.value}")
        lines.append(f"**策略类型**: {_TARGET_STRATEGY_MAP.get(classification.impact_target, '通用策略')}\n")

        lines.append("## 研究发现支撑\n")
        for f in findings:
            lines.append(f"- **{f.title}**: {f.description}")
            if f.classification:
                lines.append(f"  置信度: {f.classification.confidence:.1%}, 效应量: {f.classification.effect_size:.1%}")

        return "\n".join(lines)

    def _generate_application_guide(self, classification: FindingClassification) -> Dict:
        """生成应用指南"""
        return {
            "策略类型": _TARGET_STRATEGY_MAP.get(classification.impact_target, "通用策略"),
            "应用阶段": _STAGE_APPLICATION_MAP.get(classification.journey_stage, "综合应用"),
            "目标人群": classification.target_audience.value,
            "核心机制": classification.mechanism.value,
            "适用场景": self._infer_applicable_scenarios(classification),
        }

    def _infer_applicable_scenarios(self, classification: FindingClassification) -> List[str]:
        """根据分类推断适用场景"""
        scenario_map = {
            ImpactTarget.GROWTH: ["市场增长", "品牌营销"],
            ImpactTarget.CONVERSION: ["渠道运营", "零售增长"],
            ImpactTarget.RETENTION: ["用户运营", "整合营销"],
            ImpactTarget.EFFICIENCY: ["企业经营", "渠道运营"],
            ImpactTarget.INNOVATION: ["产品研发", "战略经营"],
            ImpactTarget.EXPERIENCE: ["产品研发", "用户运营"],
        }
        return scenario_map.get(classification.impact_target, ["通用"])

    def _generate_implementation_steps(self, classification: FindingClassification) -> List[str]:
        """生成实施步骤"""
        base_steps = [
            "第一阶段：准备期 - 收集补充数据，确认策略前提",
            "第二阶段：试点期 - 小范围A/B测试，验证效果假设",
            "第三阶段：推广期 - 基于验证结果决定是否规模应用",
            "第四阶段：优化期 - 持续监控效果，迭代优化策略",
        ]

        # 根据作用环节定制
        stage_specific = {
            JourneyStage.AWARENESS: "重点：在认知触点植入{mechanism}元素",
            JourneyStage.INTEREST: "重点：在兴趣激发环节强化{mechanism}效果",
            JourneyStage.CONSIDERATION: "重点：在决策对比阶段应用{mechanism}策略",
            JourneyStage.PURCHASE: "重点：在成交转化关键点实施{mechanism}干预",
            JourneyStage.USAGE: "重点：在使用体验中维持{mechanism}效应",
            JourneyStage.ADVOCACY: "重点：在推荐传播环节利用{mechanism}驱动",
        }

        specific = stage_specific.get(
            classification.journey_stage,
            "重点：在关键触点应用{mechanism}策略",
        ).format(mechanism=classification.mechanism.value)

        return base_steps + [specific]

    def _calculate_priority(
        self, classification: FindingClassification, findings: List[ResearchFinding]
    ) -> int:
        """计算策略优先级（1最高 10最低）"""
        score = 5.0  # 基础分

        # 高置信度 → 高优先级
        score -= classification.confidence * 2

        # 高效应量 → 高优先级
        score -= classification.effect_size * 2

        # 多发现支撑 → 高优先级
        score -= min(2.0, len(findings) * 0.5)

        # 高可复制性 → 高优先级
        score -= classification.replicability * 1.0

        return max(1, min(10, int(round(score))))

    def _calculate_strategy_confidence(
        self, findings: List[ResearchFinding], classification: FindingClassification
    ) -> float:
        """计算策略整体置信度"""
        if not findings:
            return 0.0

        # 发现平均置信度
        avg_conf = sum(
            f.classification.confidence for f in findings if f.classification
        ) / max(1, sum(1 for f in findings if f.classification))

        # 多发现验证加成
        multi_bonus = min(0.2, len(findings) * 0.05)

        # 高效应量加成
        effect_bonus = classification.effect_size * 0.1

        return min(1.0, avg_conf + multi_bonus + effect_bonus)

    # ─────────────────────────────────────────────────
    # 策略关联检测
    # ─────────────────────────────────────────────────

    def _detect_relations(self, strategy: Strategy) -> None:
        """自动检测策略间关联关系"""
        for other_id, other in self._strategies.items():
            if other_id == strategy.strategy_id:
                continue

            # 同目标 → 可能协同
            if (strategy.classification.impact_target == other.classification.impact_target
                    and strategy.classification.mechanism != other.classification.mechanism):
                self._add_relation(
                    strategy.strategy_id, other_id,
                    StrategyRelationType.SYNERGY, 0.6,
                    f"同目标({strategy.classification.impact_target.value})不同机制，可能协同增效",
                )

            # 同机制不同目标 → 可能组合
            if (strategy.classification.mechanism == other.classification.mechanism
                    and strategy.classification.impact_target != other.classification.impact_target):
                self._add_relation(
                    strategy.strategy_id, other_id,
                    StrategyRelationType.COMBINATION, 0.5,
                    f"同机制({strategy.classification.mechanism.value})不同目标，可能形成组合策略",
                )

            # 同环节同目标同机制 → 可能冲突或替代
            if (strategy.classification.impact_target == other.classification.impact_target
                    and strategy.classification.mechanism == other.classification.mechanism
                    and strategy.classification.journey_stage == other.classification.journey_stage):
                self._add_relation(
                    strategy.strategy_id, other_id,
                    StrategyRelationType.CONFLICT, 0.7,
                    f"同维度完全重叠，需评估是否冲突",
                )

    def _add_relation(
        self,
        source_id: str,
        target_id: str,
        rel_type: StrategyRelationType,
        strength: float,
        description: str,
    ) -> None:
        """添加策略关联"""
        relation = StrategyRelation(
            source_strategy_id=source_id,
            target_strategy_id=target_id,
            relation_type=rel_type,
            strength=strength,
            description=description,
        )

        self._relations.append(relation)

        # 双向添加到策略对象
        if source_id in self._strategies:
            self._strategies[source_id].relations.append(relation)
        if target_id in self._strategies:
            # 反向关系
            reverse_map = {
                StrategyRelationType.PREREQUISITE: StrategyRelationType.SYNERGY,
            }
            reverse_type = reverse_map.get(rel_type, rel_type)
            reverse = StrategyRelation(
                source_strategy_id=target_id,
                target_strategy_id=source_id,
                relation_type=reverse_type,
                strength=strength,
                description=description,
            )
            self._strategies[target_id].relations.append(reverse)

    # ─────────────────────────────────────────────────
    # 策略生命周期管理
    # ─────────────────────────────────────────────────

    def advance_lifecycle(
        self,
        strategy_id: str,
        validation_result: Optional[Dict] = None,
    ) -> Optional[StrategyLifecycleStage]:
        """
        推进策略生命周期

        生命周期流转：
        发现期 → 生成期 → 验证期 → 应用期 → 成熟期 → 衰退期 → 退役

        Args:
            strategy_id: 策略ID
            validation_result: 验证结果 {
                status: "validated" | "invalidated" | "partial",
                effect_data: {...},
                notes: str
            }

        Returns:
            新的生命周期阶段，策略不存在时返回None
        """
        if strategy_id not in self._strategies:
            return None

        strategy = self._strategies[strategy_id]

        # 处理验证结果
        if validation_result:
            status = validation_result.get("status", "")
            effect_data = validation_result.get("effect_data", {})

            strategy.validation_results.append({
                "date": datetime.now().isoformat(),
                "status": status,
                "effect_data": effect_data,
                "notes": validation_result.get("notes", ""),
            })

            if status == "validated":
                strategy.validation_status = ValidationStatus.VALIDATED
            elif status == "invalidated":
                strategy.validation_status = ValidationStatus.INVALIDATED
            elif status == "partial":
                strategy.validation_status = ValidationStatus.PARTIAL

        # 生命周期流转
        transitions = {
            StrategyLifecycleStage.DISCOVERY: StrategyLifecycleStage.GENERATION,
            StrategyLifecycleStage.GENERATION: StrategyLifecycleStage.VALIDATION,
            StrategyLifecycleStage.VALIDATION: (
                StrategyLifecycleStage.APPLICATION
                if strategy.validation_status == ValidationStatus.VALIDATED
                else StrategyLifecycleStage.DECLINE
            ),
            StrategyLifecycleStage.APPLICATION: StrategyLifecycleStage.MATURITY,
            StrategyLifecycleStage.MATURITY: StrategyLifecycleStage.DECLINE,
            StrategyLifecycleStage.DECLINE: StrategyLifecycleStage.RETIRED,
            StrategyLifecycleStage.RETIRED: StrategyLifecycleStage.RETIRED,  # 终态
        }

        current = strategy.lifecycle_stage
        next_stage = transitions.get(current, current)

        # 更新版本
        if next_stage != current:
            strategy.lifecycle_stage = next_stage
            strategy.updated_at = datetime.now().isoformat()

            # 更新索引
            if current in self._strategy_index_by_lifecycle:
                idx = self._strategy_index_by_lifecycle[current]
                if strategy_id in idx:
                    idx.remove(strategy_id)
            if next_stage not in self._strategy_index_by_lifecycle:
                self._strategy_index_by_lifecycle[next_stage] = []
            self._strategy_index_by_lifecycle[next_stage].append(strategy_id)

            logger.info(f"策略 {strategy_id} 生命周期: {current.value} → {next_stage.value}")
            self._persist_strategy(strategy)

        return next_stage

    def retire_strategy(self, strategy_id: str, reason: str = "") -> bool:
        """
        强制退役策略

        Args:
            strategy_id: 策略ID
            reason: 退役原因

        Returns:
            是否成功
        """
        if strategy_id not in self._strategies:
            return False

        strategy = self._strategies[strategy_id]
        strategy.lifecycle_stage = StrategyLifecycleStage.RETIRED
        strategy.validation_status = ValidationStatus.INVALIDATED
        strategy.updated_at = datetime.now().isoformat()

        # 添加版本记录
        strategy.version_history.append(StrategyVersion(
            version=f"{int(float(strategy.current_version)) + 1}.0",
            date=datetime.now().strftime('%Y-%m-%d'),
            source_finding_ids=[],
            changes=f"策略退役: {reason}",
            validation_status=ValidationStatus.INVALIDATED,
        ))

        self._persist_strategy(strategy)
        logger.info(f"策略已退役: {strategy_id} - {reason}")
        return True

    # ─────────────────────────────────────────────────
    # 查询与报告
    # ─────────────────────────────────────────────────

    def get_finding(self, finding_id: str) -> Optional[ResearchFinding]:
        """获取研究发现"""
        return self._findings.get(finding_id)

    def get_strategy(self, strategy_id: str) -> Optional[Strategy]:
        """获取策略"""
        return self._strategies.get(strategy_id)

    def list_findings(
        self,
        impact_target: Optional[str] = None,
        scenario: Optional[str] = None,
        limit: int = 50,
    ) -> List[ResearchFinding]:
        """列出研究发现"""
        results = list(self._findings.values())

        if impact_target:
            target_enum = None
            for m in ImpactTarget:
                if m.value == impact_target:
                    target_enum = m
                    break
            if target_enum and target_enum in self._finding_index_by_target:
                ids = set(self._finding_index_by_target[target_enum])
                results = [f for f in results if f.finding_id in ids]

        if scenario:
            results = [f for f in results if scenario in f.scenarios]

        return sorted(results, key=lambda f: f.created_at, reverse=True)[:limit]

    def list_strategies(
        self,
        lifecycle_stage: Optional[str] = None,
        scenario: Optional[str] = None,
        impact_target: Optional[str] = None,
        limit: int = 50,
    ) -> List[Strategy]:
        """列出策略"""
        results = list(self._strategies.values())

        if lifecycle_stage:
            stage_enum = None
            for m in StrategyLifecycleStage:
                if m.value == lifecycle_stage:
                    stage_enum = m
                    break
            if stage_enum:
                results = [s for s in results if s.lifecycle_stage == stage_enum]

        if scenario:
            results = [s for s in results if scenario in s.related_scenarios]

        if impact_target:
            target_enum = None
            for m in ImpactTarget:
                if m.value == impact_target:
                    target_enum = m
                    break
            if target_enum:
                results = [s for s in results if s.classification.impact_target == target_enum]

        return sorted(results, key=lambda s: s.priority)[:limit]

    def get_strategy_network(self, strategy_id: str) -> Dict:
        """获取策略关联网络"""
        if strategy_id not in self._strategies:
            return {"error": "策略不存在"}

        strategy = self._strategies[strategy_id]
        relations = []
        for r in strategy.relations:
            related = self._strategies.get(r.target_strategy_id)
            relations.append({
                "target_id": r.target_strategy_id,
                "target_name": related.name if related else "未知",
                "relation_type": r.relation_type.value,
                "strength": r.strength,
                "description": r.description,
            })

        return {
            "strategy_id": strategy_id,
            "strategy_name": strategy.name,
            "lifecycle": strategy.lifecycle_stage.value,
            "confidence": strategy.confidence,
            "relations": relations,
        }

    def generate_report(self) -> Dict:
        """生成引擎状态报告"""
        # 生命周期分布
        lifecycle_dist = {}
        for stage in StrategyLifecycleStage:
            count = len(self._strategy_index_by_lifecycle.get(stage, []))
            if count > 0:
                lifecycle_dist[stage.value] = count

        # 目标分布
        target_dist = {}
        for target, ids in self._finding_index_by_target.items():
            target_dist[target.value] = len(ids)

        # 验证状态分布
        validation_dist = {}
        for s in self._strategies.values():
            status = s.validation_status.value
            validation_dist[status] = validation_dist.get(status, 0) + 1

        return {
            "engine_version": self.VERSION,
            "timestamp": datetime.now().isoformat(),
            "total_findings": len(self._findings),
            "total_strategies": len(self._strategies),
            "total_relations": len(self._relations),
            "lifecycle_distribution": lifecycle_dist,
            "finding_target_distribution": target_dist,
            "validation_distribution": validation_dist,
        }

    # ─────────────────────────────────────────────────
    # 持久化
    # ─────────────────────────────────────────────────

    def _load_data(self) -> None:
        """加载持久化数据"""
        findings_dir = self._data_dir / "findings"
        strategies_dir = self._data_dir / "strategies"

        if findings_dir.exists():
            for fp in findings_dir.glob("RF_*.json"):
                try:
                    with open(fp, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    finding = self._dict_to_finding(data)
                    if finding:
                        self._findings[finding.finding_id] = finding
                except Exception as e:
                    logger.debug(f"加载研究发现失败: {fp} - {e}")

        if strategies_dir.exists():
            for fp in strategies_dir.glob("STR_*.json"):
                try:
                    with open(fp, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    strategy = self._dict_to_strategy(data)
                    if strategy:
                        self._strategies[strategy.strategy_id] = strategy
                except Exception as e:
                    logger.debug(f"加载策略失败: {fp} - {e}")

        # 重建索引
        self._rebuild_indexes()

    def _persist_finding(self, finding: ResearchFinding) -> None:
        """持久化研究发现"""
        findings_dir = self._data_dir / "findings"
        findings_dir.mkdir(parents=True, exist_ok=True)

        fp = findings_dir / f"{finding.finding_id}.json"
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(finding.to_dict(), f, ensure_ascii=False, indent=2)

    def _persist_strategy(self, strategy: Strategy) -> None:
        """持久化策略"""
        strategies_dir = self._data_dir / "strategies"
        strategies_dir.mkdir(parents=True, exist_ok=True)

        fp = strategies_dir / f"{strategy.strategy_id}.json"
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(strategy.to_dict(), f, ensure_ascii=False, indent=2)

    def _rebuild_indexes(self) -> None:
        """重建索引"""
        self._finding_index_by_target.clear()
        self._strategy_index_by_lifecycle.clear()
        self._strategy_index_by_scenario.clear()
        self._relations.clear()

        for f in self._findings.values():
            if f.classification:
                t = f.classification.impact_target
                if t not in self._finding_index_by_target:
                    self._finding_index_by_target[t] = []
                self._finding_index_by_target[t].append(f.finding_id)

        for s in self._strategies.values():
            lc = s.lifecycle_stage
            if lc not in self._strategy_index_by_lifecycle:
                self._strategy_index_by_lifecycle[lc] = []
            self._strategy_index_by_lifecycle[lc].append(s.strategy_id)

            for scenario in s.related_scenarios:
                if scenario not in self._strategy_index_by_scenario:
                    self._strategy_index_by_scenario[scenario] = []
                self._strategy_index_by_scenario[scenario].append(s.strategy_id)

            for r in s.relations:
                self._relations.append(r)

    # ─────────────────────────────────────────────────
    # 反序列化辅助
    # ─────────────────────────────────────────────────

    def _dict_to_finding(self, data: Dict) -> Optional[ResearchFinding]:
        """字典转ResearchFinding"""
        try:
            classification = None
            if "classification" in data and data["classification"]:
                c = data["classification"]
                classification = FindingClassification(
                    impact_target=ImpactTarget(c.get("impact_target", "增长")),
                    target_audience=TargetAudience(c.get("target_audience", "存量用户")),
                    journey_stage=JourneyStage(c.get("journey_stage", "购买")),
                    mechanism=Mechanism(c.get("mechanism", "情绪触发")),
                    confidence=c.get("confidence", 0.5),
                    effect_size=c.get("effect_size", 0.0),
                    replicability=c.get("replicability", 0.5),
                )
            return ResearchFinding(
                finding_id=data.get("finding_id", ""),
                title=data.get("title", ""),
                description=data.get("description", ""),
                source=data.get("source", ""),
                evidence=data.get("evidence", []),
                classification=classification,
                scenarios=data.get("scenarios", []),
                value_types=data.get("value_types", []),
                created_at=data.get("created_at", ""),
            )
        except Exception as e:
            logger.debug(f"反序列化研究发现失败: {e}")
            return None

    def _dict_to_strategy(self, data: Dict) -> Optional[Strategy]:
        """字典转Strategy"""
        try:
            c = data.get("classification", {})
            classification = FindingClassification(
                impact_target=ImpactTarget(c.get("impact_target", "增长")),
                target_audience=TargetAudience(c.get("target_audience", "存量用户")),
                journey_stage=JourneyStage(c.get("journey_stage", "购买")),
                mechanism=Mechanism(c.get("mechanism", "情绪触发")),
                confidence=c.get("confidence", 0.5),
                effect_size=c.get("effect_size", 0.0),
                replicability=c.get("replicability", 0.5),
            )

            lifecycle = StrategyLifecycleStage.GENERATION
            for m in StrategyLifecycleStage:
                if m.value == data.get("lifecycle_stage", ""):
                    lifecycle = m
                    break

            validation = ValidationStatus.PENDING
            for m in ValidationStatus:
                if m.value == data.get("validation_status", ""):
                    validation = m
                    break

            return Strategy(
                strategy_id=data.get("strategy_id", ""),
                name=data.get("name", ""),
                description=data.get("description", ""),
                classification=classification,
                lifecycle_stage=lifecycle,
                content=data.get("content", ""),
                application_guide=data.get("application_guide", {}),
                implementation_steps=data.get("implementation_steps", []),
                validation_status=validation,
                validation_plan=data.get("validation_plan", {}),
                current_version=data.get("current_version", "6.2.0"),
                source_finding_ids=data.get("source_finding_ids", []),
                related_scenarios=data.get("related_scenarios", []),
                priority=data.get("priority", 5),
                confidence=data.get("confidence", 0.0),
                created_at=data.get("created_at", ""),
                updated_at=data.get("updated_at", ""),
            )
        except Exception as e:
            logger.debug(f"反序列化策略失败: {e}")
            return None


# ═══════════════════════════════════════════════════════════════
# 便捷函数
# ═══════════════════════════════════════════════════════════════

def create_research_strategy_engine(data_dir: Optional[str] = None) -> ResearchStrategyEngine:
    """创建研究发现驱动策略引擎"""
    return ResearchStrategyEngine(data_dir)


__all__ = [
    'ResearchStrategyEngine',
    'ResearchFinding',
    'Strategy',
    'FindingClassification',
    'StrategyRelation',
    'StrategyVersion',
    'ImpactTarget',
    'TargetAudience',
    'JourneyStage',
    'Mechanism',
    'StrategyLifecycleStage',
    'StrategyRelationType',
    'ValidationStatus',
    'create_research_strategy_engine',
]
