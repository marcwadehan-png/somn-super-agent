# -*- coding: utf-8 -*-
"""医家集群 Cloning - Tier 2 学派集群"""

from typing import Dict, List, Optional, Any
from .._cloning_base import SageCloning, SchoolCluster
from .._cloning_types import AnalysisResult, DecisionResult, SageProfile, CloningTier


class _HuaTuoCloning(SageCloning):
    """华佗Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="华佗", name_en="Hua Tuo", era="东汉", years="约145-208",
            school="医家", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="户部",
            title="神医", biography="东汉末年医学家，外科鼻祖，发明麻沸散。",
            core_works=[],
            capability={"strategic_vision": 7, "execution": 9, "innovation": 10, "leadership": 6, "influence": 9, "cross_domain": 6},
        ))
        self._wisdom_laws = ["对症下药——因人制宜的治疗方案", "预防为主——治未病的理念", "五禽戏——运动是健康之本"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="华佗", school="医家", problem=problem,
            perspective="从华佗的神医智慧出发",
            core_insight="因人制宜的治疗方案",
            recommendations=[["对症下药——因人制宜的治疗方案", "预防为主——治未病的理念", "五禽戏——运动是健康之本"][i].split("——")[1] if "——" in ["对症下药——因人制宜的治疗方案", "预防为主——治未病的理念", "五禽戏——运动是健康之本"][i] else ["对症下药——因人制宜的治疗方案", "预防为主——治未病的理念", "五禽戏——运动是健康之本"][i] for i in range(len(["对症下药——因人制宜的治疗方案", "预防为主——治未病的理念", "五禽戏——运动是健康之本"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["创新", "预防", "对症", "运动"]) else 0))
        return DecisionResult(sage_name="华佗", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"华佗的智慧：对症下药——因人制宜的治疗方案"


class _SunSimiaoCloning(SageCloning):
    """孙思邈Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="孙思邈", name_en="Sun Simiao", era="唐代", years="541-682",
            school="医家", tier=CloningTier.TIER2_CLUSTER,
            position="户部主事", department="户部",
            title="药王", biography="唐代医学家，著有《千金要方》。",
            core_works=["《千金要方》《千金翼方》"],
            capability={"strategic_vision": 7, "execution": 8, "innovation": 7, "leadership": 7, "influence": 9, "cross_domain": 7},
        ))
        self._wisdom_laws = ["大医精诚——医者的职业道德", "养生有道——预防重于治疗", "综合治疗——身心并治"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="孙思邈", school="医家", problem=problem,
            perspective="从孙思邈的药王智慧出发",
            core_insight="医者的职业道德",
            recommendations=[["大医精诚——医者的职业道德", "养生有道——预防重于治疗", "综合治疗——身心并治"][i].split("——")[1] if "——" in ["大医精诚——医者的职业道德", "养生有道——预防重于治疗", "综合治疗——身心并治"][i] else ["大医精诚——医者的职业道德", "养生有道——预防重于治疗", "综合治疗——身心并治"][i] for i in range(len(["大医精诚——医者的职业道德", "养生有道——预防重于治疗", "综合治疗——身心并治"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["道德", "养生", "综合", "细节"]) else 0))
        return DecisionResult(sage_name="孙思邈", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"孙思邈的智慧：大医精诚——医者的职业道德"


class _LiShizhenCloning(SageCloning):
    """李时珍Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="李时珍", name_en="Li Shizhen", era="明代", years="1518-1593",
            school="医家", tier=CloningTier.TIER2_CLUSTER,
            position="户部主事", department="户部",
            title="药圣", biography="明代医学家，著有《本草纲目》。",
            core_works=["《本草纲目》"],
            capability={"strategic_vision": 7, "execution": 10, "innovation": 8, "leadership": 6, "influence": 10, "cross_domain": 7},
        ))
        self._wisdom_laws = ["实证精神——亲身验证每一种药物", "系统分类——建立完整的知识体系", "持之以恒——27年编成一部书"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="李时珍", school="医家", problem=problem,
            perspective="从李时珍的药圣智慧出发",
            core_insight="亲身验证每一种药物",
            recommendations=[["实证精神——亲身验证每一种药物", "系统分类——建立完整的知识体系", "持之以恒——27年编成一部书"][i].split("——")[1] if "——" in ["实证精神——亲身验证每一种药物", "系统分类——建立完整的知识体系", "持之以恒——27年编成一部书"][i] else ["实证精神——亲身验证每一种药物", "系统分类——建立完整的知识体系", "持之以恒——27年编成一部书"][i] for i in range(len(["实证精神——亲身验证每一种药物", "系统分类——建立完整的知识体系", "持之以恒——27年编成一部书"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["实证", "系统", "坚持", "分类"]) else 0))
        return DecisionResult(sage_name="李时珍", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"李时珍的智慧：实证精神——亲身验证每一种药物"


class _GeHongCloning(SageCloning):
    """葛洪Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="葛洪", name_en="Ge Hong", era="东晋", years="284-364",
            school="医家", tier=CloningTier.TIER2_CLUSTER,
            position="工部主事", department="户部",
            title="抱朴子", biography="东晋道教学者、炼丹家、医学家。",
            core_works=["《抱朴子》《肘后备急方》"],
            capability={"strategic_vision": 7, "execution": 8, "innovation": 9, "leadership": 5, "influence": 7, "cross_domain": 8},
        ))
        self._wisdom_laws = ["急症急救——快速应对突发状况", "实验精神——炼丹即古代化学实验", "简便验廉——用最简单的方法解决最大问题"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="葛洪", school="医家", problem=problem,
            perspective="从葛洪的抱朴子智慧出发",
            core_insight="快速应对突发状况",
            recommendations=[["急症急救——快速应对突发状况", "实验精神——炼丹即古代化学实验", "简便验廉——用最简单的方法解决最大问题"][i].split("——")[1] if "——" in ["急症急救——快速应对突发状况", "实验精神——炼丹即古代化学实验", "简便验廉——用最简单的方法解决最大问题"][i] else ["急症急救——快速应对突发状况", "实验精神——炼丹即古代化学实验", "简便验廉——用最简单的方法解决最大问题"][i] for i in range(len(["急症急救——快速应对突发状况", "实验精神——炼丹即古代化学实验", "简便验廉——用最简单的方法解决最大问题"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["急救", "实验", "简便", "实用"]) else 0))
        return DecisionResult(sage_name="葛洪", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"葛洪的智慧：急症急救——快速应对突发状况"


class _TaoHongjingCloning(SageCloning):
    """陶弘景Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="陶弘景", name_en="Tao Hongjing", era="南朝", years="456-536",
            school="医家", tier=CloningTier.TIER2_CLUSTER,
            position="户部主事", department="户部",
            title="山中宰相", biography="南朝道教思想家、医学家。",
            core_works=["《本草经集注》《养性延命录》"],
            capability={"strategic_vision": 7, "execution": 7, "innovation": 7, "leadership": 6, "influence": 7, "cross_domain": 7},
        ))
        self._wisdom_laws = ["系统整理——建立知识的分类体系", "养生之道——身心合一的健康观", "隐士智慧——在退隐中观察和思考"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="陶弘景", school="医家", problem=problem,
            perspective="从陶弘景的山中宰相智慧出发",
            core_insight="建立知识的分类体系",
            recommendations=[["系统整理——建立知识的分类体系", "养生之道——身心合一的健康观", "隐士智慧——在退隐中观察和思考"][i].split("——")[1] if "——" in ["系统整理——建立知识的分类体系", "养生之道——身心合一的健康观", "隐士智慧——在退隐中观察和思考"][i] else ["系统整理——建立知识的分类体系", "养生之道——身心合一的健康观", "隐士智慧——在退隐中观察和思考"][i] for i in range(len(["系统整理——建立知识的分类体系", "养生之道——身心合一的健康观", "隐士智慧——在退隐中观察和思考"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["系统", "养生", "分类", "整合"]) else 0))
        return DecisionResult(sage_name="陶弘景", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"陶弘景的智慧：系统整理——建立知识的分类体系"


def build_cluster() -> SchoolCluster:
    """构建医家集群"""
    return SchoolCluster(
        name="医家集群",
        school="医家",
        department="户部",
        leader_name="张仲景",
        members={
        "华佗": _HuaTuoCloning(),
        "孙思邈": _SunSimiaoCloning(),
        "李时珍": _LiShizhenCloning(),
        "葛洪": _GeHongCloning(),
        "陶弘景": _TaoHongjingCloning(),
        },
    )
__all__ = ['build_cluster']
