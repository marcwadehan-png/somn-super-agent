# -*- coding: utf-8 -*-
"""
道家集群 Cloning - Tier 2 学派集群
领军人物：老子
成员：庄子、列子、列子（可扩展至35+人）
"""

from typing import Dict, List, Optional, Any

from .._cloning_base import SageCloning, SchoolCluster
from .._cloning_types import AnalysisResult, DecisionResult, SageProfile, CloningTier


class _ZhuangZiCloning(SageCloning):
    """庄子Cloning - 逍遥游"""
    def __init__(self):
        super().__init__(SageProfile(
            name="庄子", name_en="Zhuang Zi", era="战国中期", years="约前369-前286",
            school="道家", tier=CloningTier.TIER2_CLUSTER,
            position="吏部主事", department="吏部",
            title="南华真人", biography="道家学派代表人物，以《庄子》（又称《南华真经》）闻名。提出逍遥游、齐物论、庖丁解牛等深刻思想。",
            core_works=["《庄子》"],
            capability={"strategic_vision": 9, "execution": 5, "innovation": 10, "leadership": 6, "influence": 9, "cross_domain": 9},
        ))
        self._wisdom_laws = [
            "逍遥游 —— 精神自由是最高境界，不被外物所累",
            "齐物论 —— 万物齐一，大小、是非、生死都是相对的",
            "庖丁解牛 —— 技艺到极致则游刃有余",
            "无用之用 —— 看似无用的东西往往有最大的价值",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="庄子", school="道家", problem=problem,
            perspective="从逍遥游和齐物论的视角出发",
            core_insight="很多时候困扰我们的是我们的执着。放下执念，用更宏大的视角看问题——'天地与我并生，万物与我为一'。",
            recommendations=[
                "跳出框架——你以为的'问题'可能根本不是问题",
                "享受过程——'庖丁解牛'式的沉浸感",
                "不被有用/无用束缚——无用之用方为大用",
                "保持心灵的自由——逍遥不是逃避，而是超越",
            ],
            wisdom_laws_applied=self._wisdom_laws[:3],
            confidence=0.87,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["自由","超越","自然","放松"]) else 0))
        return DecisionResult(sage_name="庄子", problem=context.get("problem",""), chosen_option=chosen, confidence=0.85)

    def advise(self, context: Dict[str, Any]) -> str:
        return "庄子曰：'井蛙不可以语于海者，拘于虚也；夏虫不可以语于冰者，笃于时也。' 拓宽你的视野，跳出认知的局限。"


class _LieZiCloning(SageCloning):
    """列子Cloning - 冲虚真人"""
    def __init__(self):
        super().__init__(SageProfile(
            name="列子", name_en="Lie Zi", era="战国早期", years="约前450-前375",
            school="道家", tier=CloningTier.TIER2_CLUSTER,
            position="五军都督府主事", department="五军都督府",
            title="冲虚真人", biography="道家学派重要人物，以御风而行、愚公移山等寓言闻名，强调道法自然、生死齐一。",
            core_works=["《列子》"],
            capability={"strategic_vision": 8, "execution": 5, "innovation": 8, "leadership": 5, "influence": 7, "cross_domain": 8},
        ))
        self._wisdom_laws = [
            "御风而行 —— 借力而行，顺势而为",
            "生死齐一 —— 对待生死变化要有达观态度",
            "愚公移山 —— 坚持的力量可以移山填海",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="列子", school="道家", problem=problem,
            perspective="从御风而行的借力智慧出发",
            core_insight="与其用蛮力解决问题，不如找到可以借力的'风'——趋势、资源、盟友。",
            recommendations=[
                "寻找可以借力的外部趋势",
                "用愚公移山的精神面对看似不可能的任务",
                "保持达观——变化是永恒的，接受它",
                "以柔克刚——顺势而非对抗",
            ],
            wisdom_laws_applied=self._wisdom_laws,
            confidence=0.83,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (1.5 if any(w in o for w in ["借力","坚持","趋势"]) else 0))
        return DecisionResult(sage_name="列子", problem=context.get("problem",""), chosen_option=chosen, confidence=0.80)

    def advise(self, context: Dict[str, Any]) -> str:
        return "列子教我们：'天地无全功，万物无全用，人无全能。' 接受不完美，善用可用之资源。"


def build_cluster() -> SchoolCluster:
    """构建道家集群"""
    from ..tier1.laotzu import LaoTzuCloning

    cluster = SchoolCluster(
        name="道家集群",
        school="道家",
        department="吏部",
        leader_name="老子",
        members={
            "老子": LaoTzuCloning(),
            "庄子": _ZhuangZiCloning(),
            "列子": _LieZiCloning(),
        },
    )
    return cluster
__all__ = ['build_cluster']
