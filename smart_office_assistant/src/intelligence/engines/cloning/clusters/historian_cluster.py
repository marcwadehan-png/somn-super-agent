# -*- coding: utf-8 -*-
"""史学集群 Cloning - Tier 2 学派集群"""

from typing import Dict, List, Optional, Any
from .._cloning_base import SageCloning, SchoolCluster
from .._cloning_types import AnalysisResult, DecisionResult, SageProfile, CloningTier


class _BanGuCloning(SageCloning):
    """班固Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="班固", name_en="Ban Gu", era="东汉", years="32-92",
            school="史学", tier=CloningTier.TIER2_CLUSTER,
            position="五军都督府主事", department="五军都督府",
            title="汉书作者", biography="东汉史学家，中国第一部纪传体断代史《汉书》作者。",
            core_works=["《汉书》"],
            capability={"strategic_vision": 7, "execution": 9, "innovation": 8, "leadership": 6, "influence": 9, "cross_domain": 7},
        ))
        self._wisdom_laws = ["断代为史——专注于一个时代深入研究", "体例创新——开创纪传体断代史", "文史兼通——文学与史学并重"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="班固", school="史学", problem=problem,
            perspective="从班固的汉书作者智慧出发",
            core_insight="专注于一个时代深入研究",
            recommendations=[["断代为史——专注于一个时代深入研究", "体例创新——开创纪传体断代史", "文史兼通——文学与史学并重"][i].split("——")[1] if "——" in ["断代为史——专注于一个时代深入研究", "体例创新——开创纪传体断代史", "文史兼通——文学与史学并重"][i] else ["断代为史——专注于一个时代深入研究", "体例创新——开创纪传体断代史", "文史兼通——文学与史学并重"][i] for i in range(len(["断代为史——专注于一个时代深入研究", "体例创新——开创纪传体断代史", "文史兼通——文学与史学并重"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["专注", "系统", "断代", "整理"]) else 0))
        return DecisionResult(sage_name="班固", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"班固的智慧：断代为史——专注于一个时代深入研究"


class _SimaGuangCloning(SageCloning):
    """司马光Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="司马光", name_en="Sima Guang", era="北宋", years="1019-1086",
            school="史学", tier=CloningTier.TIER2_CLUSTER,
            position="内阁学士", department="五军都督府",
            title="资治通鉴作者", biography="北宋政治家、史学家，编撰《资治通鉴》。",
            core_works=["《资治通鉴》"],
            capability={"strategic_vision": 9, "execution": 8, "innovation": 7, "leadership": 8, "influence": 10, "cross_domain": 8},
        ))
        self._wisdom_laws = ["以史为鉴——从历史中提取决策智慧", "编年叙事——以时间为线索还原真相", "鉴于往事有资于治道——历史服务于现实"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="司马光", school="史学", problem=problem,
            perspective="从司马光的资治通鉴作者智慧出发",
            core_insight="从历史中提取决策智慧",
            recommendations=[["以史为鉴——从历史中提取决策智慧", "编年叙事——以时间为线索还原真相", "鉴于往事有资于治道——历史服务于现实"][i].split("——")[1] if "——" in ["以史为鉴——从历史中提取决策智慧", "编年叙事——以时间为线索还原真相", "鉴于往事有资于治道——历史服务于现实"][i] else ["以史为鉴——从历史中提取决策智慧", "编年叙事——以时间为线索还原真相", "鉴于往事有资于治道——历史服务于现实"][i] for i in range(len(["以史为鉴——从历史中提取决策智慧", "编年叙事——以时间为线索还原真相", "鉴于往事有资于治道——历史服务于现实"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["历史", "借鉴", "决策", "治理"]) else 0))
        return DecisionResult(sage_name="司马光", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"司马光的智慧：以史为鉴——从历史中提取决策智慧"


class _LiuZhijiCloning(SageCloning):
    """刘知几Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="刘知几", name_en="Liu Zhiji", era="唐代", years="661-721",
            school="史学", tier=CloningTier.TIER2_CLUSTER,
            position="五军都督府主事", department="五军都督府",
            title="史通作者", biography="唐代史学理论家，著有中国第一部史学理论著作《史通》。",
            core_works=["《史通》"],
            capability={"strategic_vision": 7, "execution": 7, "innovation": 9, "leadership": 6, "influence": 7, "cross_domain": 7},
        ))
        self._wisdom_laws = ["史学方法论——建立评判历史的标准", "直笔实录——不受政治干预如实记录", "识才——好的史学家需要才学识三长"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="刘知几", school="史学", problem=problem,
            perspective="从刘知几的史通作者智慧出发",
            core_insight="建立评判历史的标准",
            recommendations=[["史学方法论——建立评判历史的标准", "直笔实录——不受政治干预如实记录", "识才——好的史学家需要才学识三长"][i].split("——")[1] if "——" in ["史学方法论——建立评判历史的标准", "直笔实录——不受政治干预如实记录", "识才——好的史学家需要才学识三长"][i] else ["史学方法论——建立评判历史的标准", "直笔实录——不受政治干预如实记录", "识才——好的史学家需要才学识三长"][i] for i in range(len(["史学方法论——建立评判历史的标准", "直笔实录——不受政治干预如实记录", "识才——好的史学家需要才学识三长"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["方法论", "客观", "批判", "标准"]) else 0))
        return DecisionResult(sage_name="刘知几", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"刘知几的智慧：史学方法论——建立评判历史的标准"


class _DuYouCloning(SageCloning):
    """杜佑Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="杜佑", name_en="Du You", era="唐代", years="735-812",
            school="史学", tier=CloningTier.TIER2_CLUSTER,
            position="户部侍郎", department="五军都督府",
            title="通典作者", biography="唐代政治家、史学家，著有中国第一部制度史《通典》。",
            core_works=["《通典》"],
            capability={"strategic_vision": 8, "execution": 8, "innovation": 8, "leadership": 7, "influence": 7, "cross_domain": 7},
        ))
        self._wisdom_laws = ["制度史观——从制度变迁理解历史", "经世致用——史学服务于现实治理", "分类考述——系统化研究各类制度"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="杜佑", school="史学", problem=problem,
            perspective="从杜佑的通典作者智慧出发",
            core_insight="从制度变迁理解历史",
            recommendations=[["制度史观——从制度变迁理解历史", "经世致用——史学服务于现实治理", "分类考述——系统化研究各类制度"][i].split("——")[1] if "——" in ["制度史观——从制度变迁理解历史", "经世致用——史学服务于现实治理", "分类考述——系统化研究各类制度"][i] else ["制度史观——从制度变迁理解历史", "经世致用——史学服务于现实治理", "分类考述——系统化研究各类制度"][i] for i in range(len(["制度史观——从制度变迁理解历史", "经世致用——史学服务于现实治理", "分类考述——系统化研究各类制度"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["制度", "实用", "分类", "经济"]) else 0))
        return DecisionResult(sage_name="杜佑", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"杜佑的智慧：制度史观——从制度变迁理解历史"


def build_cluster() -> SchoolCluster:
    """构建史学集群"""
    return SchoolCluster(
        name="史学集群",
        school="史学",
        department="五军都督府",
        leader_name="司马迁",
        members={
        "班固": _BanGuCloning(),
        "司马光": _SimaGuangCloning(),
        "刘知几": _LiuZhijiCloning(),
        "杜佑": _DuYouCloning(),
        },
    )
__all__ = ['build_cluster']
