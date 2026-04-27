# -*- coding: utf-8 -*-
"""理学集群 Cloning - Tier 2 学派集群"""

from typing import Dict, List, Optional, Any
from .._cloning_base import SageCloning, SchoolCluster
from .._cloning_types import AnalysisResult, DecisionResult, SageProfile, CloningTier


class _ChengHaoCloning(SageCloning):
    """程颢Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="程颢", name_en="Cheng Hao", era="北宋", years="1032-1085",
            school="理学", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="礼部",
            title="明道先生", biography="北宋理学家，'洛学'创始人之一。",
            core_works=[],
            capability={"strategic_vision": 7, "execution": 6, "innovation": 8, "leadership": 6, "influence": 8, "cross_domain": 7},
        ))
        self._wisdom_laws = ["仁者浑然与物同体——万物一体的世界观", "识仁——通过修养体认仁的境界", "定性——不被外物所动的定力"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="程颢", school="理学", problem=problem,
            perspective="从程颢的明道先生智慧出发",
            core_insight="万物一体的世界观",
            recommendations=[["仁者浑然与物同体——万物一体的世界观", "识仁——通过修养体认仁的境界", "定性——不被外物所动的定力"][i].split("——")[1] if "——" in ["仁者浑然与物同体——万物一体的世界观", "识仁——通过修养体认仁的境界", "定性——不被外物所动的定力"][i] else ["仁者浑然与物同体——万物一体的世界观", "识仁——通过修养体认仁的境界", "定性——不被外物所动的定力"][i] for i in range(len(["仁者浑然与物同体——万物一体的世界观", "识仁——通过修养体认仁的境界", "定性——不被外物所动的定力"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["仁", "整体", "修养", "定性"]) else 0))
        return DecisionResult(sage_name="程颢", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"程颢的智慧：仁者浑然与物同体——万物一体的世界观"


class _ChengYiCloning(SageCloning):
    """程颐Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="程颐", name_en="Cheng Yi", era="北宋", years="1033-1107",
            school="理学", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="礼部",
            title="伊川先生", biography="北宋理学家，'洛学'创始人之一，主张'性即理'。",
            core_works=[],
            capability={"strategic_vision": 7, "execution": 6, "innovation": 7, "leadership": 6, "influence": 8, "cross_domain": 6},
        ))
        self._wisdom_laws = ["性即理——人性中蕴含天理", "涵养须用敬——以敬畏之心修养", "格物致知——通过研究事物获取知识"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="程颐", school="理学", problem=problem,
            perspective="从程颐的伊川先生智慧出发",
            core_insight="人性中蕴含天理",
            recommendations=[["性即理——人性中蕴含天理", "涵养须用敬——以敬畏之心修养", "格物致知——通过研究事物获取知识"][i].split("——")[1] if "——" in ["性即理——人性中蕴含天理", "涵养须用敬——以敬畏之心修养", "格物致知——通过研究事物获取知识"][i] else ["性即理——人性中蕴含天理", "涵养须用敬——以敬畏之心修养", "格物致知——通过研究事物获取知识"][i] for i in range(len(["性即理——人性中蕴含天理", "涵养须用敬——以敬畏之心修养", "格物致知——通过研究事物获取知识"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["敬", "理", "格物", "致知"]) else 0))
        return DecisionResult(sage_name="程颐", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"程颐的智慧：性即理——人性中蕴含天理"


class _ZhangZaiCloning(SageCloning):
    """张载Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="张载", name_en="Zhang Zai", era="北宋", years="1020-1077",
            school="理学", tier=CloningTier.TIER2_CLUSTER,
            position="礼部侍郎", department="礼部",
            title="横渠先生", biography="北宋理学家，提出'为天地立心'。",
            core_works=["《正蒙》"],
            capability={"strategic_vision": 8, "execution": 6, "innovation": 8, "leadership": 7, "influence": 9, "cross_domain": 7},
        ))
        self._wisdom_laws = ["为天地立心——知识分子的终极使命", "为生民立命——改善民生的责任感", "横渠四句——天地生民往圣万世"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="张载", school="理学", problem=problem,
            perspective="从张载的横渠先生智慧出发",
            core_insight="知识分子的终极使命",
            recommendations=[["为天地立心——知识分子的终极使命", "为生民立命——改善民生的责任感", "横渠四句——天地生民往圣万世"][i].split("——")[1] if "——" in ["为天地立心——知识分子的终极使命", "为生民立命——改善民生的责任感", "横渠四句——天地生民往圣万世"][i] else ["为天地立心——知识分子的终极使命", "为生民立命——改善民生的责任感", "横渠四句——天地生民往圣万世"][i] for i in range(len(["为天地立心——知识分子的终极使命", "为生民立命——改善民生的责任感", "横渠四句——天地生民往圣万世"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["使命", "民生", "责任", "担当"]) else 0))
        return DecisionResult(sage_name="张载", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"张载的智慧：为天地立心——知识分子的终极使命"


class _ShaoYongCloning(SageCloning):
    """邵雍Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="邵雍", name_en="Shao Yong", era="北宋", years="1011-1077",
            school="理学", tier=CloningTier.TIER2_CLUSTER,
            position="五军都督府主事", department="礼部",
            title="康节先生", biography="北宋理学家、数学家，先天象数体系创立者。",
            core_works=["《皇极经世》"],
            capability={"strategic_vision": 9, "execution": 5, "innovation": 10, "leadership": 5, "influence": 7, "cross_domain": 9},
        ))
        self._wisdom_laws = ["先天象数——以数学模型描述宇宙", "观物——从整体上观察和理解事物", "元会运世——宏观周期理论"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="邵雍", school="理学", problem=problem,
            perspective="从邵雍的康节先生智慧出发",
            core_insight="以数学模型描述宇宙",
            recommendations=[["先天象数——以数学模型描述宇宙", "观物——从整体上观察和理解事物", "元会运世——宏观周期理论"][i].split("——")[1] if "——" in ["先天象数——以数学模型描述宇宙", "观物——从整体上观察和理解事物", "元会运世——宏观周期理论"][i] else ["先天象数——以数学模型描述宇宙", "观物——从整体上观察和理解事物", "元会运世——宏观周期理论"][i] for i in range(len(["先天象数——以数学模型描述宇宙", "观物——从整体上观察和理解事物", "元会运世——宏观周期理论"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["系统", "周期", "数学", "宏观"]) else 0))
        return DecisionResult(sage_name="邵雍", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"邵雍的智慧：先天象数——以数学模型描述宇宙"


def build_cluster() -> SchoolCluster:
    """构建理学集群"""
    from ..tier1.zhuxi import ZhuXiCloning

    return SchoolCluster(
        name="理学集群",
        school="理学",
        department="礼部",
        leader_name="朱熹",
        members={
            "朱熹": ZhuXiCloning(),
            "程颢": _ChengHaoCloning(),
            "程颐": _ChengYiCloning(),
            "张载": _ZhangZaiCloning(),
            "邵雍": _ShaoYongCloning(),
        },
    )
__all__ = ['build_cluster']
