# -*- coding: utf-8 -*-
"""创业集群 Cloning - Tier 2 学派集群"""

from typing import Dict, List, Optional, Any
from .._cloning_base import SageCloning, SchoolCluster
from .._cloning_types import AnalysisResult, DecisionResult, SageProfile, CloningTier


class _JeffBezosCloning(SageCloning):
    """贝索斯Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="贝索斯", name_en="Jeff Bezos", era="21世纪", years="1964-",
            school="创新创业", tier=CloningTier.TIER2_CLUSTER,
            position="工部侍郎", department="工部",
            title="长期主义实践者", biography="亚马逊创始人。",
            core_works=[],
            capability={"strategic_vision": 10, "execution": 9, "innovation": 9, "leadership": 9, "influence": 10, "cross_domain": 9},
        ))
        self._wisdom_laws = ["长期主义——一切都基于10年以上的判断", "客户至上——从客户需求倒推", "Day 1心态——永远保持创业状态"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="贝索斯", school="创新创业", problem=problem,
            perspective="从贝索斯的长期主义实践者智慧出发",
            core_insight="一切都基于10年以上的判断",
            recommendations=[["长期主义——一切都基于10年以上的判断", "客户至上——从客户需求倒推", "Day 1心态——永远保持创业状态"][i].split("——")[1] if "——" in ["长期主义——一切都基于10年以上的判断", "客户至上——从客户需求倒推", "Day 1心态——永远保持创业状态"][i] else ["长期主义——一切都基于10年以上的判断", "客户至上——从客户需求倒推", "Day 1心态——永远保持创业状态"][i] for i in range(len(["长期主义——一切都基于10年以上的判断", "客户至上——从客户需求倒推", "Day 1心态——永远保持创业状态"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["长期", "客户", "效率", "规模"]) else 0))
        return DecisionResult(sage_name="贝索斯", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"贝索斯的智慧：长期主义——一切都基于10年以上的判断"


class _RenZhengfeiCloning(SageCloning):
    """任正非Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="任正非", name_en="Ren Zhengfei", era="21世纪", years="1944-",
            school="创新创业", tier=CloningTier.TIER2_CLUSTER,
            position="工部尚书", department="工部",
            title="华为精神", biography="华为创始人，以狼性文化和自主研发著称。",
            core_works=[],
            capability={"strategic_vision": 10, "execution": 10, "innovation": 8, "leadership": 10, "influence": 10, "cross_domain": 7},
        ))
        self._wisdom_laws = ["活下去——企业第一要务是生存", "自主研发——核心技术不能受制于人", "灰度管理——在黑白之间找到平衡"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="任正非", school="创新创业", problem=problem,
            perspective="从任正非的华为精神智慧出发",
            core_insight="企业第一要务是生存",
            recommendations=[["活下去——企业第一要务是生存", "自主研发——核心技术不能受制于人", "灰度管理——在黑白之间找到平衡"][i].split("——")[1] if "——" in ["活下去——企业第一要务是生存", "自主研发——核心技术不能受制于人", "灰度管理——在黑白之间找到平衡"][i] else ["活下去——企业第一要务是生存", "自主研发——核心技术不能受制于人", "灰度管理——在黑白之间找到平衡"][i] for i in range(len(["活下去——企业第一要务是生存", "自主研发——核心技术不能受制于人", "灰度管理——在黑白之间找到平衡"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["生存", "研发", "管理", "危机"]) else 0))
        return DecisionResult(sage_name="任正非", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"任正非的智慧：活下去——企业第一要务是生存"


class _JackMaCloning(SageCloning):
    """马云Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="马云", name_en="Jack Ma", era="21世纪", years="1964-",
            school="创新创业", tier=CloningTier.TIER2_CLUSTER,
            position="户部侍郎", department="工部",
            title="电商先驱", biography="阿里巴巴创始人。",
            core_works=[],
            capability={"strategic_vision": 9, "execution": 8, "innovation": 9, "leadership": 9, "influence": 10, "cross_domain": 8},
        ))
        self._wisdom_laws = ["让天下没有难做的生意——平台思维", "赋能中小企业——生态而非帝国", "拥抱变化——唯一不变的是变化"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="马云", school="创新创业", problem=problem,
            perspective="从马云的电商先驱智慧出发",
            core_insight="平台思维",
            recommendations=[["让天下没有难做的生意——平台思维", "赋能中小企业——生态而非帝国", "拥抱变化——唯一不变的是变化"][i].split("——")[1] if "——" in ["让天下没有难做的生意——平台思维", "赋能中小企业——生态而非帝国", "拥抱变化——唯一不变的是变化"][i] else ["让天下没有难做的生意——平台思维", "赋能中小企业——生态而非帝国", "拥抱变化——唯一不变的是变化"][i] for i in range(len(["让天下没有难做的生意——平台思维", "赋能中小企业——生态而非帝国", "拥抱变化——唯一不变的是变化"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["平台", "生态", "变化", "赋能"]) else 0))
        return DecisionResult(sage_name="马云", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"马云的智慧：让天下没有难做的生意——平台思维"


class _ZhangYimingCloning(SageCloning):
    """张一鸣Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="张一鸣", name_en="Zhang Yiming", era="21世纪", years="1983-",
            school="创新创业", tier=CloningTier.TIER2_CLUSTER,
            position="工部主事", department="工部",
            title="算法驱动增长", biography="字节跳动创始人。",
            core_works=[],
            capability={"strategic_vision": 9, "execution": 9, "innovation": 10, "leadership": 8, "influence": 9, "cross_domain": 8},
        ))
        self._wisdom_laws = ["算法驱动——用技术解决信息分发", "Context not Control——提供背景而非控制", "延迟满足——短期不赚钱也要做正确的事"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="张一鸣", school="创新创业", problem=problem,
            perspective="从张一鸣的算法驱动增长智慧出发",
            core_insight="用技术解决信息分发",
            recommendations=[["算法驱动——用技术解决信息分发", "Context not Control——提供背景而非控制", "延迟满足——短期不赚钱也要做正确的事"][i].split("——")[1] if "——" in ["算法驱动——用技术解决信息分发", "Context not Control——提供背景而非控制", "延迟满足——短期不赚钱也要做正确的事"][i] else ["算法驱动——用技术解决信息分发", "Context not Control——提供背景而非控制", "延迟满足——短期不赚钱也要做正确的事"][i] for i in range(len(["算法驱动——用技术解决信息分发", "Context not Control——提供背景而非控制", "延迟满足——短期不赚钱也要做正确的事"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["算法", "效率", "数据", "创新"]) else 0))
        return DecisionResult(sage_name="张一鸣", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"张一鸣的智慧：算法驱动——用技术解决信息分发"


def build_cluster() -> SchoolCluster:
    """构建创业集群"""
    from ..tier1.musk import MuskCloning

    return SchoolCluster(
        name="创业集群",
        school="创新创业",
        department="工部",
        leader_name="马斯克",
        members={
            "马斯克": MuskCloning(),
            "贝索斯": _JeffBezosCloning(),
            "任正非": _RenZhengfeiCloning(),
            "马云": _JackMaCloning(),
            "张一鸣": _ZhangYimingCloning(),
        },
    )
__all__ = ['build_cluster']
