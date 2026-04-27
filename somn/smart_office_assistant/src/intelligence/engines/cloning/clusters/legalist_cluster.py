# -*- coding: utf-8 -*-
"""法家集群 Cloning - Tier 2 学派集群"""

from typing import Dict, List, Optional, Any
from .._cloning_base import SageCloning, SchoolCluster
from .._cloning_types import AnalysisResult, DecisionResult, SageProfile, CloningTier


class _ShangYangCloning(SageCloning):
    """商鞅Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="商鞅", name_en="Shang Yang", era="战国中期", years="前390-前338",
            school="法家", tier=CloningTier.TIER2_CLUSTER,
            position="刑部主事", department="刑部",
            title="变法先驱", biography="战国政治家，在秦国推行变法使秦国强大。",
            core_works=["《商君书》"],
            capability={"strategic_vision": 9, "execution": 10, "innovation": 9, "leadership": 8, "influence": 9, "cross_domain": 6},
        ))
        self._wisdom_laws = ["法不阿贵——法律面前人人平等", "奖励耕战——以制度引导行为", "徙木立信——公信力是执行力的基础"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="商鞅", school="法家", problem=problem,
            perspective="从商鞅的变法先驱智慧出发",
            core_insight="法律面前人人平等",
            recommendations=[["法不阿贵——法律面前人人平等", "奖励耕战——以制度引导行为", "徙木立信——公信力是执行力的基础"][i].split("——")[1] if "——" in ["法不阿贵——法律面前人人平等", "奖励耕战——以制度引导行为", "徙木立信——公信力是执行力的基础"][i] else ["法不阿贵——法律面前人人平等", "奖励耕战——以制度引导行为", "徙木立信——公信力是执行力的基础"][i] for i in range(len(["法不阿贵——法律面前人人平等", "奖励耕战——以制度引导行为", "徙木立信——公信力是执行力的基础"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["制度", "法治", "务实", "改革"]) else 0))
        return DecisionResult(sage_name="商鞅", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"商鞅的智慧：法不阿贵——法律面前人人平等"


class _GuanZhongCloning(SageCloning):
    """管仲Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="管仲", name_en="Guan Zhong", era="春秋", years="前723-前645",
            school="法家", tier=CloningTier.TIER2_CLUSTER,
            position="户部侍郎", department="刑部",
            title="华夏第一相", biography="春秋齐国政治家，辅佐齐桓公成为春秋首霸。",
            core_works=["《管子》"],
            capability={"strategic_vision": 10, "execution": 9, "innovation": 9, "leadership": 9, "influence": 10, "cross_domain": 8},
        ))
        self._wisdom_laws = ["仓廪实而知礼节——物质基础决定上层建筑", "四维不张国乃灭亡——礼义廉耻是根基", "与俗同好恶——政策顺应民心"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="管仲", school="法家", problem=problem,
            perspective="从管仲的华夏第一相智慧出发",
            core_insight="物质基础决定上层建筑",
            recommendations=[["仓廪实而知礼节——物质基础决定上层建筑", "四维不张国乃灭亡——礼义廉耻是根基", "与俗同好恶——政策顺应民心"][i].split("——")[1] if "——" in ["仓廪实而知礼节——物质基础决定上层建筑", "四维不张国乃灭亡——礼义廉耻是根基", "与俗同好恶——政策顺应民心"][i] else ["仓廪实而知礼节——物质基础决定上层建筑", "四维不张国乃灭亡——礼义廉耻是根基", "与俗同好恶——政策顺应民心"][i] for i in range(len(["仓廪实而知礼节——物质基础决定上层建筑", "四维不张国乃灭亡——礼义廉耻是根基", "与俗同好恶——政策顺应民心"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["经济", "民生", "全局", "统筹"]) else 0))
        return DecisionResult(sage_name="管仲", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"管仲的智慧：仓廪实而知礼节——物质基础决定上层建筑"


class _LiSiCloning(SageCloning):
    """李斯Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="李斯", name_en="Li Si", era="秦代", years="前284-前208",
            school="法家", tier=CloningTier.TIER2_CLUSTER,
            position="吏部主事", department="刑部",
            title="统一功臣", biography="秦朝丞相，推动书同文车同轨等统一政策。",
            core_works=[],
            capability={"strategic_vision": 8, "execution": 9, "innovation": 8, "leadership": 7, "influence": 9, "cross_domain": 7},
        ))
        self._wisdom_laws = ["统一标准——减少内耗的最佳方式", "以史为鉴——从历史中学习治理", "各尽其能——人尽其才物尽其用"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="李斯", school="法家", problem=problem,
            perspective="从李斯的统一功臣智慧出发",
            core_insight="减少内耗的最佳方式",
            recommendations=[["统一标准——减少内耗的最佳方式", "以史为鉴——从历史中学习治理", "各尽其能——人尽其才物尽其用"][i].split("——")[1] if "——" in ["统一标准——减少内耗的最佳方式", "以史为鉴——从历史中学习治理", "各尽其能——人尽其才物尽其用"][i] else ["统一标准——减少内耗的最佳方式", "以史为鉴——从历史中学习治理", "各尽其能——人尽其才物尽其用"][i] for i in range(len(["统一标准——减少内耗的最佳方式", "以史为鉴——从历史中学习治理", "各尽其能——人尽其才物尽其用"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["统一", "标准", "规范", "整合"]) else 0))
        return DecisionResult(sage_name="李斯", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"李斯的智慧：统一标准——减少内耗的最佳方式"


class _ShenBuhaiCloning(SageCloning):
    """申不害Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="申不害", name_en="Shen Buhai", era="战国中期", years="前385-前337",
            school="法家", tier=CloningTier.TIER2_CLUSTER,
            position="厂卫主事", department="刑部",
            title="术治先驱", biography="战国法家思想家，以'术'（权术）著称。",
            core_works=[],
            capability={"strategic_vision": 7, "execution": 8, "innovation": 8, "leadership": 7, "influence": 7, "cross_domain": 6},
        ))
        self._wisdom_laws = ["术治——用制度和信息控制权力", "循名责实——名实相符方为正道", "因任授官——能力匹配职位"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="申不害", school="法家", problem=problem,
            perspective="从申不害的术治先驱智慧出发",
            core_insight="用制度和信息控制权力",
            recommendations=[["术治——用制度和信息控制权力", "循名责实——名实相符方为正道", "因任授官——能力匹配职位"][i].split("——")[1] if "——" in ["术治——用制度和信息控制权力", "循名责实——名实相符方为正道", "因任授官——能力匹配职位"][i] else ["术治——用制度和信息控制权力", "循名责实——名实相符方为正道", "因任授官——能力匹配职位"][i] for i in range(len(["术治——用制度和信息控制权力", "循名责实——名实相符方为正道", "因任授官——能力匹配职位"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["权术", "监控", "考核", "名实"]) else 0))
        return DecisionResult(sage_name="申不害", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"申不害的智慧：术治——用制度和信息控制权力"


def build_cluster() -> SchoolCluster:
    """构建法家集群"""
    from ..tier1.hanfeizi import HanFeiZiCloning

    return SchoolCluster(
        name="法家集群",
        school="法家",
        department="刑部",
        leader_name="韩非子",
        members={
            "韩非子": HanFeiZiCloning(),
            "商鞅": _ShangYangCloning(),
            "管仲": _GuanZhongCloning(),
            "李斯": _LiSiCloning(),
            "申不害": _ShenBuhaiCloning(),
        },
    )
__all__ = ['build_cluster']
