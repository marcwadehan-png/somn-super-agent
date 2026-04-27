"""
__all__ = [
    'analyze_civilization',
    'assess_continuity',
    'compare_civilizations',
    'evaluate_formation_mechanism',
    'get_civilization_wisdom_core',
    'get_wisdom_summary',
    'integrate_with_reasoning',
    'process',
]

文明智慧核心模块 v1.0
Civilization Wisdom Core

将<人类文明与中国文明深度学习文档>中的核心研究结论工程化接入 Somn.

核心能力:
1. 文明判准分析:把 Childe 文明判准与现代修正转成结构化评估框架
2. 中国文明recognize:把多元汇流,礼制结构,家国同构,文字记忆等characteristics转成可调用规则
3. 连续性评估:把文明为何能延续的问题转成机制评分
4. 形成机制分析:把良渚,陶寺,石峁,二里头,殷墟的演化链转成阶段模型

版本: v1.0
更新: 2026-04-02
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

class CivilizationCriterion(Enum):
    """文明判准"""
    SURPLUS = "生产剩余"
    SPECIALIZATION = "社会分工"
    CITY = "都邑中心"
    STATE = "公共权力"
    WRITING = "文字记忆"
    RITUAL = "礼制秩序"
    INFRASTRUCTURE = "大型工程"
    MEMORY = "历史意识"

class ChineseCivilizationTrait(Enum):
    """中国文明核心characteristics"""
    PLURAL_INTEGRATION = "多元汇流"
    CONTINUITY = "文明连续"
    RITUAL_ORDER = "礼制结构"
    FAMILY_STATE = "家国同构"
    AGRARIAN_BASE = "农耕底盘"
    BUREAUCRATIC_GOVERNANCE = "治理官僚化"
    WRITTEN_MEMORY = "文字记忆"
    ETHICAL_POLITICS = "伦理政治化"
    CULTURAL_ABSORPTION = "文化吸纳"
    PRACTICAL_REASON = "经世致用"

class FormationPhase(Enum):
    """中国文明形成链条"""
    LIANGZHU = "良渚"
    TAOSI = "陶寺"
    SHIMAO = "石峁"
    ERLITOU = "二里头"
    YINXU = "殷墟"

class ContinuityMechanism(Enum):
    """文明连续性机制"""
    WRITING_MEMORY = "文字与经典记忆"
    RITUAL_REPRODUCTION = "礼制再生产"
    AGRARIAN_FISCAL_BASE = "农耕与赋税底盘"
    POLITICAL_INTEGRATION = "政治整合能力"
    HISTORICAL_CONSCIOUSNESS = "历史意识与正统叙事"

@dataclass
class CivilizationAssessment:
    """文明评估结果"""
    subject: str
    dominant_criterion: CivilizationCriterion
    matched_traits: List[ChineseCivilizationTrait]
    formation_phase: FormationPhase
    continuity_score: float
    key_mechanisms: List[ContinuityMechanism]
    diagnosis: str
    recommendations: List[str]
    warnings: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

class CivilizationWisdomCore:
    """文明智慧核心引擎"""

    def __init__(self):
        self.criteria_library: Dict[CivilizationCriterion, Dict[str, str]] = {
            CivilizationCriterion.SURPLUS: {
                "meaning": "是否形成稳定剩余,并能支持专业化与组织化.",
                "signal": "农业,财政,仓储,物流,再分配"
            },
            CivilizationCriterion.SPECIALIZATION: {
                "meaning": "是否出现持续的角色分化与知识分工.",
                "signal": "官僚,工匠,军队,祭司,商人"
            },
            CivilizationCriterion.CITY: {
                "meaning": "是否形成都邑中心与区域组织核心.",
                "signal": "城址,宫殿,中心聚落,交通节点"
            },
            CivilizationCriterion.STATE: {
                "meaning": "是否形成超越血缘的公共权力与治理能力.",
                "signal": "制度,征税,命令,法度,行政"
            },
            CivilizationCriterion.WRITING: {
                "meaning": "是否形成跨代累积的符号记录系统.",
                "signal": "文字,档案,经典,契约,记录"
            },
            CivilizationCriterion.RITUAL: {
                "meaning": "是否形成稳定秩序,等级结构与公共象征.",
                "signal": "礼制,祭祀,规范,等级,身份"
            },
            CivilizationCriterion.INFRASTRUCTURE: {
                "meaning": "是否具备组织大型工程与调配资源的能力.",
                "signal": "水利,城墙,道路,粮仓,工程"
            },
            CivilizationCriterion.MEMORY: {
                "meaning": "是否建立对自身历史的连续叙述能力.",
                "signal": "谱系,正统,史书,祖先,文明自觉"
            },
        }

        self.chinese_trait_library: Dict[ChineseCivilizationTrait, Dict[str, str]] = {
            ChineseCivilizationTrait.PLURAL_INTEGRATION: {
                "summary": "中国文明不是单线起源,而是多区域并起,逐步整合.",
                "keywords": "多元,汇流,整合,区域,文明圈"
            },
            ChineseCivilizationTrait.CONTINUITY: {
                "summary": "文明长期延续,政权更替但文化记忆不断线.",
                "keywords": "延续,连续,传承,不断裂"
            },
            ChineseCivilizationTrait.RITUAL_ORDER: {
                "summary": "礼制既是价值体系,也是组织技术.",
                "keywords": "礼制,秩序,规范,祭祀"
            },
            ChineseCivilizationTrait.FAMILY_STATE: {
                "summary": "家族伦理与国家治理长期互相嵌套.",
                "keywords": "家国,宗族,亲属,伦理政治"
            },
            ChineseCivilizationTrait.AGRARIAN_BASE: {
                "summary": "农业剩余构成税赋,军政与人口治理的底盘.",
                "keywords": "农耕,田地,粮食,赋税"
            },
            ChineseCivilizationTrait.BUREAUCRATIC_GOVERNANCE: {
                "summary": "治理能力依赖稳定官僚系统与文书技术.",
                "keywords": "官僚,行政,郡县,文书"
            },
            ChineseCivilizationTrait.WRITTEN_MEMORY: {
                "summary": "文字与经典体系构成文明跨代复制的硬骨架.",
                "keywords": "文字,经典,甲骨,文献,记忆"
            },
            ChineseCivilizationTrait.ETHICAL_POLITICS: {
                "summary": "政治合法性与伦理正当性长期绑定.",
                "keywords": "德治,仁政,正统,道德"
            },
            ChineseCivilizationTrait.CULTURAL_ABSORPTION: {
                "summary": "善于吸纳边缘与外来要素并重写为自身秩序.",
                "keywords": "吸纳,同化,fusion,转化"
            },
            ChineseCivilizationTrait.PRACTICAL_REASON: {
                "summary": "偏重经世致用,而不是纯抽象建构.",
                "keywords": "经世,实用,治理,事功"
            },
        }

        self.formation_chain: Dict[FormationPhase, Dict[str, Any]] = {
            FormationPhase.LIANGZHU: {
                "role": "区域文明高峰,提供水利,礼制和等级结构样本",
                "keywords": ["良渚", "水利", "玉器", "礼制"]
            },
            FormationPhase.TAOSI: {
                "role": "早期都邑,历法与政治中心化的重要证据",
                "keywords": ["陶寺", "都邑", "历法", "中心聚落"]
            },
            FormationPhase.SHIMAO: {
                "role": "北方强力中心与资源整合样本",
                "keywords": ["石峁", "城墙", "边地", "军事化"]
            },
            FormationPhase.ERLITOU: {
                "role": "王朝早期国家形态与中原整合能力的关键节点",
                "keywords": ["二里头", "王权", "青铜", "国家形成"]
            },
            FormationPhase.YINXU: {
                "role": "文字,祭祀,战争与国家机器成熟化",
                "keywords": ["殷墟", "甲骨文", "祭祀", "王朝"]
            },
        }

        self.continuity_mechanisms: Dict[ContinuityMechanism, str] = {
            ContinuityMechanism.WRITING_MEMORY: "用文字,经典,档案把经验跨代保存.",
            ContinuityMechanism.RITUAL_REPRODUCTION: "用礼制把秩序固化为可反复执行的社会脚本.",
            ContinuityMechanism.AGRARIAN_FISCAL_BASE: "用农耕剩余与税赋支撑长期治理.",
            ContinuityMechanism.POLITICAL_INTEGRATION: "通过整合地方,边疆与新人口维持大一统能力.",
            ContinuityMechanism.HISTORICAL_CONSCIOUSNESS: "通过历史叙事维持合法性,身份与方向感.",
        }

        self.analysis_history: List[CivilizationAssessment] = []

    def analyze_civilization(self, subject: str, context: Optional[Dict[str, Any]] = None) -> CivilizationAssessment:
        """分析一个对象的文明结构characteristics"""
        context = context or {}
        text_parts = [subject]
        for value in context.values():
            if isinstance(value, (str, int, float)):
                text_parts.append(str(value))
        text = " ".join(text_parts)

        dominant_criterion = self._detect_dominant_criterion(text)
        matched_traits = self._detect_chinese_traits(text)
        formation_phase = self._detect_formation_phase(text)
        continuity = self.assess_continuity({
            "writing": context.get("writing") or ("文字" in text or "甲骨" in text or "经典" in text),
            "ritual": context.get("ritual") or ("礼" in text or "祭祀" in text or "秩序" in text),
            "agriculture": context.get("agriculture") or ("农业" in text or "农耕" in text or "粮食" in text),
            "integration": context.get("integration") or ("整合" in text or "unified" in text),
            "history": context.get("history") or ("历史" in text or "传统" in text or "祖先" in text),
        })

        diagnosis = self._build_diagnosis(subject, dominant_criterion, matched_traits, formation_phase, continuity)
        recommendations = self._build_recommendations(dominant_criterion, matched_traits, continuity["score"])
        warnings = self._build_warnings(matched_traits, continuity["score"])

        assessment = CivilizationAssessment(
            subject=subject,
            dominant_criterion=dominant_criterion,
            matched_traits=matched_traits,
            formation_phase=formation_phase,
            continuity_score=continuity["score"],
            key_mechanisms=continuity["mechanisms"],
            diagnosis=diagnosis,
            recommendations=recommendations,
            warnings=warnings,
        )
        self.analysis_history.append(assessment)
        return assessment

    def compare_civilizations(self, primary: str, secondary: str, focus: str = "") -> Dict[str, Any]:
        """比较两个文明对象"""
        primary_assessment = self.analyze_civilization(primary, {"focus": focus})
        secondary_assessment = self.analyze_civilization(secondary, {"focus": focus})

        shared = sorted({trait.value for trait in primary_assessment.matched_traits} & {
            trait.value for trait in secondary_assessment.matched_traits
        })
        unique_primary = sorted({trait.value for trait in primary_assessment.matched_traits} - set(shared))
        unique_secondary = sorted({trait.value for trait in secondary_assessment.matched_traits} - set(shared))

        return {
            "primary": primary,
            "secondary": secondary,
            "focus": focus or "synthesize比较",
            "shared_traits": shared,
            "primary_unique_traits": unique_primary,
            "secondary_unique_traits": unique_secondary,
            "continuity_gap": round(primary_assessment.continuity_score - secondary_assessment.continuity_score, 3),
            "summary": (
                f"{primary}与{secondary}都具备文明组织化characteristics,但在连续性,礼制复制与历史记忆上"
                f"呈现不同强弱."
            )
        }

    def assess_continuity(self, factors: Dict[str, Any]) -> Dict[str, Any]:
        """评估文明连续性"""
        weights = {
            ContinuityMechanism.WRITING_MEMORY: 0.24,
            ContinuityMechanism.RITUAL_REPRODUCTION: 0.20,
            ContinuityMechanism.AGRARIAN_FISCAL_BASE: 0.18,
            ContinuityMechanism.POLITICAL_INTEGRATION: 0.22,
            ContinuityMechanism.HISTORICAL_CONSCIOUSNESS: 0.16,
        }

        active_mechanisms: List[ContinuityMechanism] = []
        score = 0.0

        mapping = {
            ContinuityMechanism.WRITING_MEMORY: bool(factors.get("writing")),
            ContinuityMechanism.RITUAL_REPRODUCTION: bool(factors.get("ritual")),
            ContinuityMechanism.AGRARIAN_FISCAL_BASE: bool(factors.get("agriculture")),
            ContinuityMechanism.POLITICAL_INTEGRATION: bool(factors.get("integration")),
            ContinuityMechanism.HISTORICAL_CONSCIOUSNESS: bool(factors.get("history")),
        }

        for mechanism, active in mapping.items():
            if active:
                active_mechanisms.append(mechanism)
                score += weights[mechanism]

        return {
            "score": round(min(score, 1.0), 3),
            "mechanisms": active_mechanisms,
            "explanations": [self.continuity_mechanisms[m] for m in active_mechanisms],
        }

    def evaluate_formation_mechanism(self, region_context: Dict[str, Any]) -> Dict[str, Any]:
        """评估文明形成机制"""
        region = region_context.get("region", "未知区域")
        text = " ".join(str(v) for v in region_context.values())
        phase = self._detect_formation_phase(text)
        criterion = self._detect_dominant_criterion(text)

        return {
            "region": region,
            "formation_phase": phase.value,
            "dominant_criterion": criterion.value,
            "interpretation": self.formation_chain[phase]["role"],
            "recommendation": (
                "先judge剩余,权力,礼制,文字是否开始耦合,再judge是否形成真正文明跃迁."
            ),
        }

    def integrate_with_reasoning(self, reasoning_chain: List[Dict[str, Any]]) -> Dict[str, Any]:
        """将文明分析接入已有推理链"""
        chain_text = " ".join(str(step) for step in reasoning_chain)
        assessment = self.analyze_civilization(chain_text)

        return {
            "civilization_diagnosis": assessment.diagnosis,
            "dominant_criterion": assessment.dominant_criterion.value,
            "matched_traits": [trait.value for trait in assessment.matched_traits],
            "continuity_score": assessment.continuity_score,
            "recommended_actions": assessment.recommendations,
        }

    def get_wisdom_summary(self) -> Dict[str, Any]:
        """get文明智慧摘要"""
        return {
            "name": "文明智慧核心",
            "version": "v1.0",
            "criteria_count": len(self.criteria_library),
            "traits_count": len(self.chinese_trait_library),
            "formation_phases": [phase.value for phase in FormationPhase],
            "continuity_mechanisms": [m.value for m in ContinuityMechanism],
            "history_size": len(self.analysis_history),
            "core_proposition": "文明不是静态标签,而是剩余,秩序,记忆与整合能力长期耦合的结果.",
        }

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """unified接口,供协调器/fusion器调用"""
        problem = payload.get("problem", "")
        context = payload.get("context", {})
        assessment = self.analyze_civilization(problem, context)
        return {
            "summary": assessment.diagnosis,
            "dominant_criterion": assessment.dominant_criterion.value,
            "continuity_score": assessment.continuity_score,
            "matched_traits": [trait.value for trait in assessment.matched_traits],
            "recommendations": assessment.recommendations,
            "warnings": assessment.warnings,
        }

    def _detect_dominant_criterion(self, text: str) -> CivilizationCriterion:
        scores = {
            CivilizationCriterion.SURPLUS: ["农业", "剩余", "税", "粮食", "仓储", "财政"],
            CivilizationCriterion.SPECIALIZATION: ["分工", "工匠", "官僚", "军队", "祭司", "专业"],
            CivilizationCriterion.CITY: ["都邑", "城市", "宫殿", "中心", "聚落"],
            CivilizationCriterion.STATE: ["国家", "政权", "治理", "官僚", "命令", "法度"],
            CivilizationCriterion.WRITING: ["文字", "甲骨", "经典", "记载", "文献"],
            CivilizationCriterion.RITUAL: ["礼", "礼制", "祭祀", "等级", "秩序"],
            CivilizationCriterion.INFRASTRUCTURE: ["工程", "水利", "城墙", "道路", "交通"],
            CivilizationCriterion.MEMORY: ["历史", "祖先", "传统", "记忆", "谱系", "正统"],
        }

        max_score = -1
        selected = CivilizationCriterion.STATE
        for criterion, keywords in scores.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > max_score:
                max_score = score
                selected = criterion
        return selected

    def _detect_chinese_traits(self, text: str) -> List[ChineseCivilizationTrait]:
        matched: List[ChineseCivilizationTrait] = []
        for trait, info in self.chinese_trait_library.items():
            keywords = [kw.strip() for kw in info["keywords"].split(",")]
            if any(kw and kw in text for kw in keywords):
                matched.append(trait)

        if not matched:
            return [
                ChineseCivilizationTrait.PLURAL_INTEGRATION,
                ChineseCivilizationTrait.CONTINUITY,
                ChineseCivilizationTrait.WRITTEN_MEMORY,
            ]
        return matched

    def _detect_formation_phase(self, text: str) -> FormationPhase:
        for phase, info in self.formation_chain.items():
            if any(keyword in text for keyword in info["keywords"]):
                return phase
        return FormationPhase.ERLITOU

    def _build_diagnosis(
        self,
        subject: str,
        criterion: CivilizationCriterion,
        traits: List[ChineseCivilizationTrait],
        phase: FormationPhase,
        continuity: Dict[str, Any],
    ) -> str:
        trait_text = ",".join(trait.value for trait in traits[:4])
        return (
            f"{subject}当前最突出的文明判准是'{criterion.value}',"
            f"更接近中国文明形成链中的'{phase.value}'阶段逻辑,"
            f"核心表现为{trait_text}.连续性评分为{continuity['score']:.2f},"
            "说明它不是单点现象,而是组织,记忆与秩序正在耦合."
        )

    def _build_recommendations(
        self,
        criterion: CivilizationCriterion,
        traits: List[ChineseCivilizationTrait],
        continuity_score: float,
    ) -> List[str]:
        recommendations = [
            f"围绕'{criterion.value}'补齐配套制度,避免只有表层形态没有底层支撑.",
            "把礼制,文字,组织与资源调度放到同一框架里看,不要单点优化.",
        ]

        if ChineseCivilizationTrait.WRITTEN_MEMORY not in traits:
            recommendations.append("补强档案,知识沉淀与文字化机制,否则经验无法跨代复制.")
        if ChineseCivilizationTrait.RITUAL_ORDER not in traits:
            recommendations.append("补强规范与仪式化执action作,把价值观转成可重复秩序.")
        if continuity_score < 0.5:
            recommendations.append("优先修复连续性:先做记忆,整合和底盘建设,再追求外部扩张.")

        return recommendations

    def _build_warnings(self, traits: List[ChineseCivilizationTrait], continuity_score: float) -> List[str]:
        warnings: List[str] = []
        if continuity_score < 0.4:
            warnings.append("连续性偏弱,容易出现'一代工程,二代失传'.")
        if ChineseCivilizationTrait.AGRARIAN_BASE not in traits:
            warnings.append("若缺乏稳定资源底盘,文明结构可能停留在叙事层而非组织层.")
        if ChineseCivilizationTrait.CULTURAL_ABSORPTION not in traits:
            warnings.append("吸纳与整合能力不足时,外部冲击会放大内部断裂.")
        return warnings

_civilization_wisdom_core: Optional[CivilizationWisdomCore] = None

def get_civilization_wisdom_core() -> CivilizationWisdomCore:
    """get文明智慧核心单例"""
    global _civilization_wisdom_core
    if _civilization_wisdom_core is None:
        _civilization_wisdom_core = CivilizationWisdomCore()
    return _civilization_wisdom_core
