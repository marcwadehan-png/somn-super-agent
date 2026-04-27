"""
__all__ = [
    'analyze_nexus',
    'assess_fiscal_military_state',
    'compare_war_economy_systems',
    'evaluate_state_capacity',
    'get_civilization_war_economy_core',
    'get_wisdom_summary',
    'integrate_with_reasoning',
    'process',
]

文明-经济-战争核心模块 v1.0
Civilization War Economy Core

将<文明,经济与战争关系深度学习文档>中的核心研究结论工程化接入 Somn.

核心能力:
1. 主链分析:生产剩余 -> 税收提取 -> 战争动员 -> 政治整合 -> 制度沉淀
2. 国家能力评估:财政,后勤,组织,技术,合法性五维评分
3. 财政-军事国家诊断:recognize扩张能力与治理负担的平衡点
4. 中国案例mapping:战国富国强兵,盐铁,屯田,漕运,工业后勤

版本: v1.0
更新: 2026-04-02
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

class NexusPhase(Enum):
    """文明-经济-战争主链阶段"""
    SURPLUS = "生产剩余"
    TAXATION = "税收提取"
    MOBILIZATION = "战争动员"
    INTEGRATION = "政治整合"
    SEDIMENTATION = "制度沉淀"

class StateFormationTheory(Enum):
    """国家形成理论"""
    TILLY = "Tilly: 战争塑造国家"
    CARNEIRO = "Carneiro: 压力与战争"
    FISCAL_MILITARY = "财政-军事国家"
    LOGISTICS = "工业后勤与总体战"
    CHINESE_STATECRAFT = "中国式富国强兵与治理沉淀"

class MobilizationType(Enum):
    """动员类型"""
    GRAIN = "粮食动员"
    TAX = "财政动员"
    LABOR = "人力动员"
    TECHNOLOGY = "技术动员"
    IDEOLOGY = "合法性动员"

@dataclass
class WarEconomyAssessment:
    """文明-经济-战争分析结果"""
    problem: str
    dominant_phase: NexusPhase
    matched_theories: List[StateFormationTheory]
    mobilization_types: List[MobilizationType]
    state_capacity_score: float
    fiscal_military_score: float
    diagnosis: str
    recommendations: List[str]
    warnings: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

class CivilizationWarEconomyCore:
    """文明-经济-战争核心引擎"""

    def __init__(self):
        self.phase_explanations: Dict[NexusPhase, str] = {
            NexusPhase.SURPLUS: "没有持续剩余,国家能力与战争能力都没有底盘.",
            NexusPhase.TAXATION: "不能稳定提取资源,就无法把经济力量转成组织力量.",
            NexusPhase.MOBILIZATION: "战争是动员效率与组织密度的压力测试.",
            NexusPhase.INTEGRATION: "真正强的国家,不只会打,还能把不同地区与群体整合起来.",
            NexusPhase.SEDIMENTATION: "文明高度取决于战时动员能否沉淀为长期制度.",
        }

        self.theory_library: Dict[StateFormationTheory, Dict[str, Any]] = {
            StateFormationTheory.TILLY: {
                "summary": "战争逼迫统治者建设税收,行政与军事系统.",
                "keywords": ["战争", "国家", "政权", "行政", "军队"]
            },
            StateFormationTheory.CARNEIRO: {
                "summary": "资源与空间压力上升时,冲突推动更高层级整合.",
                "keywords": ["压力", "资源", "边界", "冲突", "扩张"]
            },
            StateFormationTheory.FISCAL_MILITARY: {
                "summary": "财政能力决定军事能力,军事压力反过来重塑财政制度.",
                "keywords": ["财政", "税收", "军费", "债务", "常备军"]
            },
            StateFormationTheory.LOGISTICS: {
                "summary": "工业与后勤系统让战争从战场竞争变成体系竞争.",
                "keywords": ["工业", "后勤", "运输", "补给", "总体战"]
            },
            StateFormationTheory.CHINESE_STATECRAFT: {
                "summary": "战国富国强兵,盐铁,屯田,漕运都体现经济基础如何沉淀为国家能力.",
                "keywords": ["富国强兵", "盐铁", "屯田", "漕运", "整合"]
            },
        }

        self.case_library: Dict[str, Dict[str, str]] = {
            "战国": {
                "lesson": "竞争压力迫使各国改革财政,军制,官僚体系.",
                "phase": NexusPhase.MOBILIZATION.value
            },
            "盐铁": {
                "lesson": "关键资源国有化,是财政提取与军政保障的一体化动作.",
                "phase": NexusPhase.TAXATION.value
            },
            "屯田": {
                "lesson": "把农业生产和军队供给绑定,降低长期作战成本.",
                "phase": NexusPhase.SURPLUS.value
            },
            "漕运": {
                "lesson": "后勤不是附属环节,而是帝国整合与统治半径的硬约束.",
                "phase": NexusPhase.INTEGRATION.value
            },
            "工业后勤": {
                "lesson": "现代国家竞争不只拼勇武,更拼工业,运输,标准化与组织效率.",
                "phase": NexusPhase.SEDIMENTATION.value
            },
        }

        self.history: List[WarEconomyAssessment] = []

    def analyze_nexus(self, problem: str, context: Optional[Dict[str, Any]] = None) -> WarEconomyAssessment:
        """分析文明-经济-战争关系"""
        context = context or {}
        text = " ".join([problem] + [str(v) for v in context.values() if isinstance(v, (str, int, float))])

        dominant_phase = self._detect_phase(text)
        matched_theories = self._detect_theories(text)
        mobilization_types = self._detect_mobilization_types(text)
        state_capacity = self.evaluate_state_capacity(context)
        fiscal_military = self.assess_fiscal_military_state(context)

        diagnosis = self._build_diagnosis(problem, dominant_phase, matched_theories, state_capacity, fiscal_military)
        recommendations = self._build_recommendations(dominant_phase, state_capacity["score"], fiscal_military["score"])
        warnings = self._build_warnings(dominant_phase, state_capacity["score"], fiscal_military["score"])

        assessment = WarEconomyAssessment(
            problem=problem,
            dominant_phase=dominant_phase,
            matched_theories=matched_theories,
            mobilization_types=mobilization_types,
            state_capacity_score=state_capacity["score"],
            fiscal_military_score=fiscal_military["score"],
            diagnosis=diagnosis,
            recommendations=recommendations,
            warnings=warnings,
        )
        self.history.append(assessment)
        return assessment

    def evaluate_state_capacity(self, factors: Dict[str, Any]) -> Dict[str, Any]:
        """评估国家能力"""
        dims = {
            "fiscal": 0.24,
            "logistics": 0.22,
            "organization": 0.22,
            "technology": 0.16,
            "legitimacy": 0.16,
        }

        normalized = {
            "fiscal": self._to_score(factors.get("fiscal", factors.get("tax", 0.5))),
            "logistics": self._to_score(factors.get("logistics", factors.get("supply", 0.5))),
            "organization": self._to_score(factors.get("organization", factors.get("bureaucracy", 0.5))),
            "technology": self._to_score(factors.get("technology", factors.get("industry", 0.5))),
            "legitimacy": self._to_score(factors.get("legitimacy", factors.get("integration", 0.5))),
        }

        score = sum(normalized[name] * weight for name, weight in dims.items())
        weakest = sorted(normalized.items(), key=lambda x: x[1])[0][0]

        return {
            "score": round(min(score, 1.0), 3),
            "dimensions": normalized,
            "weakest_link": weakest,
            "summary": f"国家能力短板当前集中在 {weakest} 维度.",
        }

    def assess_fiscal_military_state(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """评估财政-军事国家成熟度"""
        fiscal = self._to_score(context.get("fiscal", context.get("tax", 0.5)))
        military = self._to_score(context.get("military", context.get("mobilization", 0.5)))
        coordination = self._to_score(context.get("coordination", context.get("organization", 0.5)))
        score = fiscal * 0.4 + military * 0.35 + coordination * 0.25

        return {
            "score": round(min(score, 1.0), 3),
            "interpretation": (
                "财政,军事,行政三者越紧密,越可能把短期冲突转化为长期国家能力."
            ),
            "balance": round(abs(fiscal - military), 3),
        }

    def compare_war_economy_systems(self, system_a: str, system_b: str, focus: str = "") -> Dict[str, Any]:
        """比较两个战争经济系统"""
        assessment_a = self.analyze_nexus(system_a, {"focus": focus})
        assessment_b = self.analyze_nexus(system_b, {"focus": focus})

        return {
            "system_a": system_a,
            "system_b": system_b,
            "focus": focus or "synthesize比较",
            "capacity_gap": round(assessment_a.state_capacity_score - assessment_b.state_capacity_score, 3),
            "fiscal_military_gap": round(assessment_a.fiscal_military_score - assessment_b.fiscal_military_score, 3),
            "summary": (
                f"{system_a}与{system_b}的核心差异,不在口号,而在财政提取,后勤支撑和制度沉淀能力."
            ),
        }

    def integrate_with_reasoning(self, reasoning_chain: List[Dict[str, Any]]) -> Dict[str, Any]:
        """将文明-经济-战争分析融入推理链"""
        text = " ".join(str(step) for step in reasoning_chain)
        assessment = self.analyze_nexus(text)
        return {
            "dominant_phase": assessment.dominant_phase.value,
            "state_capacity_score": assessment.state_capacity_score,
            "fiscal_military_score": assessment.fiscal_military_score,
            "recommendations": assessment.recommendations,
            "warnings": assessment.warnings,
        }

    def get_wisdom_summary(self) -> Dict[str, Any]:
        """get核心摘要"""
        return {
            "name": "文明-经济-战争核心",
            "version": "v1.0",
            "phases": [phase.value for phase in NexusPhase],
            "theories": [theory.value for theory in StateFormationTheory],
            "case_count": len(self.case_library),
            "history_size": len(self.history),
            "core_proposition": "真正强的文明,不只会动员资源打仗,还能把战时能力沉淀为长期治理能力.",
        }

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """unified接口,供协调器/fusion器调用"""
        problem = payload.get("problem", "")
        context = payload.get("context", {})
        assessment = self.analyze_nexus(problem, context)
        return {
            "summary": assessment.diagnosis,
            "dominant_phase": assessment.dominant_phase.value,
            "state_capacity_score": assessment.state_capacity_score,
            "fiscal_military_score": assessment.fiscal_military_score,
            "matched_theories": [theory.value for theory in assessment.matched_theories],
            "mobilization_types": [item.value for item in assessment.mobilization_types],
            "recommendations": assessment.recommendations,
            "warnings": assessment.warnings,
        }

    def _detect_phase(self, text: str) -> NexusPhase:
        mapping = {
            NexusPhase.SURPLUS: ["粮食", "农业", "剩余", "供给", "屯田"],
            NexusPhase.TAXATION: ["税", "财政", "盐铁", "征收", "国库"],
            NexusPhase.MOBILIZATION: ["战争", "军队", "动员", "征兵", "富国强兵"],
            NexusPhase.INTEGRATION: ["整合", "unified", "治理", "漕运", "秩序"],
            NexusPhase.SEDIMENTATION: ["制度", "沉淀", "官僚", "工业", "长期"],
        }

        best_phase = NexusPhase.MOBILIZATION
        best_score = -1
        for phase, keywords in mapping.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > best_score:
                best_score = score
                best_phase = phase
        return best_phase

    def _detect_theories(self, text: str) -> List[StateFormationTheory]:
        matched: List[StateFormationTheory] = []
        for theory, info in self.theory_library.items():
            if any(keyword in text for keyword in info["keywords"]):
                matched.append(theory)
        if not matched:
            return [
                StateFormationTheory.TILLY,
                StateFormationTheory.FISCAL_MILITARY,
                StateFormationTheory.CHINESE_STATECRAFT,
            ]
        return matched

    def _detect_mobilization_types(self, text: str) -> List[MobilizationType]:
        mapping = {
            MobilizationType.GRAIN: ["粮", "农业", "屯田", "供给"],
            MobilizationType.TAX: ["税", "财政", "盐铁", "预算"],
            MobilizationType.LABOR: ["人力", "征兵", "劳役", "组织"],
            MobilizationType.TECHNOLOGY: ["工业", "技术", "装备", "标准化"],
            MobilizationType.IDEOLOGY: ["合法性", "认同", "动员叙事", "整合"],
        }
        matched = [kind for kind, keywords in mapping.items() if any(kw in text for kw in keywords)]
        return matched or [MobilizationType.TAX, MobilizationType.LABOR]

    def _build_diagnosis(
        self,
        problem: str,
        phase: NexusPhase,
        theories: List[StateFormationTheory],
        state_capacity: Dict[str, Any],
        fiscal_military: Dict[str, Any],
    ) -> str:
        theory_text = ",".join(theory.value for theory in theories[:3])
        return (
            f"针对'{problem}',当前最关键的链路阶段是'{phase.value}'."
            f"从{theory_text}看,问题本质不是单一军事动作,而是经济提取,组织动员与制度沉淀是否打通."
            f"国家能力评分 {state_capacity['score']:.2f},财政-军事成熟度 {fiscal_military['score']:.2f}."
        )

    def _build_recommendations(self, phase: NexusPhase, state_capacity: float, fiscal_military: float) -> List[str]:
        recommendations = [
            f"围绕'{phase.value}'补链,而不是只在结果端加码.",
            "同时评估资源提取,后勤保障,合法性与组织密度,避免把单点强项误判为系统强项.",
        ]

        if state_capacity < 0.55:
            recommendations.append("先补国家能力短板,尤其是财政,后勤与组织执行,不宜直接追求大规模扩张.")
        if fiscal_military < 0.55:
            recommendations.append("把财政系统与军事/执行系统打通,否则动员成本会持续失控.")
        if phase == NexusPhase.SEDIMENTATION:
            recommendations.append("把战时机制转成平时制度,形成可复制,可训练,可审计的组织资产.")
        return recommendations

    def _build_warnings(self, phase: NexusPhase, state_capacity: float, fiscal_military: float) -> List[str]:
        warnings: List[str] = []
        if phase == NexusPhase.MOBILIZATION and state_capacity < 0.5:
            warnings.append("动员冲在前面,制度跟不上,会导致高耗散与反噬.")
        if fiscal_military < 0.45:
            warnings.append("财政与军事脱节,容易出现短期胜利,长期透支.")
        if state_capacity < 0.45:
            warnings.append("国家能力偏弱,外部竞争压力可能迅速放大内部断裂.")
        return warnings

    def _to_score(self, value: Any) -> float:
        if isinstance(value, bool):
            return 1.0 if value else 0.0
        if isinstance(value, (int, float)):
            if value > 1:
                return max(0.0, min(float(value) / 100.0, 1.0))
            return max(0.0, min(float(value), 1.0))
        return 0.5

_civilization_war_economy_core: Optional[CivilizationWarEconomyCore] = None

def get_civilization_war_economy_core() -> CivilizationWarEconomyCore:
    """get文明-经济-战争核心单例"""
    global _civilization_war_economy_core
    if _civilization_war_economy_core is None:
        _civilization_war_economy_core = CivilizationWarEconomyCore()
    return _civilization_war_economy_core
