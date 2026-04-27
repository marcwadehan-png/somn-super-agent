# -*- coding: utf-8 -*-
"""营销集群 Cloning - Tier 2 学派集群"""

from typing import Dict, List, Optional, Any
from .._cloning_base import SageCloning, SchoolCluster
from .._cloning_types import AnalysisResult, DecisionResult, SageProfile, CloningTier


class _DavidOgilvyCloning(SageCloning):
    """奥格威Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="奥格威", name_en="David Ogilvy", era="20世纪", years="1911-1999",
            school="营销学", tier=CloningTier.TIER2_CLUSTER,
            position="户部主事", department="户部",
            title="广告教父", biography="奥美广告创始人，被称为'广告教父'。",
            core_works=["《一个广告人的自白》"],
            capability={"strategic_vision": 8, "execution": 9, "innovation": 8, "leadership": 9, "influence": 10, "cross_domain": 7},
        ))
        self._wisdom_laws = ["广告的目标是销售——不是艺术", "深入研究产品——好创意来自深理解", "品牌形象——长期积累的品牌资产"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="奥格威", school="营销学", problem=problem,
            perspective="从奥格威的广告教父智慧出发",
            core_insight="不是艺术",
            recommendations=[["广告的目标是销售——不是艺术", "深入研究产品——好创意来自深理解", "品牌形象——长期积累的品牌资产"][i].split("——")[1] if "——" in ["广告的目标是销售——不是艺术", "深入研究产品——好创意来自深理解", "品牌形象——长期积累的品牌资产"][i] else ["广告的目标是销售——不是艺术", "深入研究产品——好创意来自深理解", "品牌形象——长期积累的品牌资产"][i] for i in range(len(["广告的目标是销售——不是艺术", "深入研究产品——好创意来自深理解", "品牌形象——长期积累的品牌资产"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["销售", "品牌", "研究", "创意"]) else 0))
        return DecisionResult(sage_name="奥格威", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"奥格威的智慧：广告的目标是销售——不是艺术"


class _JackTroutCloning(SageCloning):
    """特劳特Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="特劳特", name_en="Jack Trout", era="20世纪", years="1935-2017",
            school="营销学", tier=CloningTier.TIER2_CLUSTER,
            position="户部主事", department="户部",
            title="定位之父", biography="定位理论创始人。",
            core_works=["《定位》"],
            capability={"strategic_vision": 9, "execution": 7, "innovation": 9, "leadership": 7, "influence": 9, "cross_domain": 7},
        ))
        self._wisdom_laws = ["成为第一胜过做得更好——心智占领", "聚焦——不要试图满足所有人", "差异化——找到对手无法模仿的独特性"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="特劳特", school="营销学", problem=problem,
            perspective="从特劳特的定位之父智慧出发",
            core_insight="心智占领",
            recommendations=[["成为第一胜过做得更好——心智占领", "聚焦——不要试图满足所有人", "差异化——找到对手无法模仿的独特性"][i].split("——")[1] if "——" in ["成为第一胜过做得更好——心智占领", "聚焦——不要试图满足所有人", "差异化——找到对手无法模仿的独特性"][i] else ["成为第一胜过做得更好——心智占领", "聚焦——不要试图满足所有人", "差异化——找到对手无法模仿的独特性"][i] for i in range(len(["成为第一胜过做得更好——心智占领", "聚焦——不要试图满足所有人", "差异化——找到对手无法模仿的独特性"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["定位", "聚焦", "差异化", "心智"]) else 0))
        return DecisionResult(sage_name="特劳特", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"特劳特的智慧：成为第一胜过做得更好——心智占领"


class _AlRiesCloning(SageCloning):
    """里斯Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="里斯", name_en="Al Ries", era="20世纪", years="1926-",
            school="营销学", tier=CloningTier.TIER2_CLUSTER,
            position="户部主事", department="户部",
            title="定位之父", biography="定位理论联合创始人。",
            core_works=["《定位》《22条商规》"],
            capability={"strategic_vision": 8, "execution": 7, "innovation": 9, "leadership": 6, "influence": 8, "cross_domain": 7},
        ))
        self._wisdom_laws = ["品类创建——比品牌更重要的是品类", "对立定位——与领导者对着干", "营销是一场心智战"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="里斯", school="营销学", problem=problem,
            perspective="从里斯的定位之父智慧出发",
            core_insight="比品牌更重要的是品类",
            recommendations=[["品类创建——比品牌更重要的是品类", "对立定位——与领导者对着干", "营销是一场心智战"][i].split("——")[1] if "——" in ["品类创建——比品牌更重要的是品类", "对立定位——与领导者对着干", "营销是一场心智战"][i] else ["品类创建——比品牌更重要的是品类", "对立定位——与领导者对着干", "营销是一场心智战"][i] for i in range(len(["品类创建——比品牌更重要的是品类", "对立定位——与领导者对着干", "营销是一场心智战"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["品类", "对立", "心智", "规律"]) else 0))
        return DecisionResult(sage_name="里斯", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"里斯的智慧：品类创建——比品牌更重要的是品类"


class _DonSchultzCloning(SageCloning):
    """舒尔茨Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="舒尔茨", name_en="Don Schultz", era="20世纪", years="1940-",
            school="营销学", tier=CloningTier.TIER2_CLUSTER,
            position="户部主事", department="户部",
            title="整合营销之父", biography="整合营销传播理论创始人。",
            core_works=["《整合营销传播》"],
            capability={"strategic_vision": 8, "execution": 7, "innovation": 8, "leadership": 7, "influence": 8, "cross_domain": 8},
        ))
        self._wisdom_laws = ["整合传播——所有触点传递一致信息", "以顾客为中心——从卖方到买方的范式转变", "触点管理——每一个接触都是营销机会"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="舒尔茨", school="营销学", problem=problem,
            perspective="从舒尔茨的整合营销之父智慧出发",
            core_insight="所有触点传递一致信息",
            recommendations=[["整合传播——所有触点传递一致信息", "以顾客为中心——从卖方到买方的范式转变", "触点管理——每一个接触都是营销机会"][i].split("——")[1] if "——" in ["整合传播——所有触点传递一致信息", "以顾客为中心——从卖方到买方的范式转变", "触点管理——每一个接触都是营销机会"][i] else ["整合传播——所有触点传递一致信息", "以顾客为中心——从卖方到买方的范式转变", "触点管理——每一个接触都是营销机会"][i] for i in range(len(["整合传播——所有触点传递一致信息", "以顾客为中心——从卖方到买方的范式转变", "触点管理——每一个接触都是营销机会"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["整合", "顾客", "触点", "一致"]) else 0))
        return DecisionResult(sage_name="舒尔茨", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"舒尔茨的智慧：整合传播——所有触点传递一致信息"


class _TheodoreLevittCloning(SageCloning):
    """莱维特Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="莱维特", name_en="Theodore Levitt", era="20世纪", years="1925-2006",
            school="营销学", tier=CloningTier.TIER2_CLUSTER,
            position="户部主事", department="户部",
            title="营销短文大师", biography="哈佛商学院教授，'营销近视症'概念提出者。",
            core_works=[],
            capability={"strategic_vision": 9, "execution": 7, "innovation": 9, "leadership": 7, "influence": 8, "cross_domain": 7},
        ))
        self._wisdom_laws = ["营销近视症——行业定义不应局限于产品", "全球化——标准化的全球营销", "产品差异化——持续的差异化是竞争关键"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="莱维特", school="营销学", problem=problem,
            perspective="从莱维特的营销短文大师智慧出发",
            core_insight="行业定义不应局限于产品",
            recommendations=[["营销近视症——行业定义不应局限于产品", "全球化——标准化的全球营销", "产品差异化——持续的差异化是竞争关键"][i].split("——")[1] if "——" in ["营销近视症——行业定义不应局限于产品", "全球化——标准化的全球营销", "产品差异化——持续的差异化是竞争关键"][i] else ["营销近视症——行业定义不应局限于产品", "全球化——标准化的全球营销", "产品差异化——持续的差异化是竞争关键"][i] for i in range(len(["营销近视症——行业定义不应局限于产品", "全球化——标准化的全球营销", "产品差异化——持续的差异化是竞争关键"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["视野", "全球化", "差异化", "行业"]) else 0))
        return DecisionResult(sage_name="莱维特", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"莱维特的智慧：营销近视症——行业定义不应局限于产品"


def build_cluster() -> SchoolCluster:
    """构建营销集群"""
    from ..tier1.kotler import KotlerCloning

    return SchoolCluster(
        name="营销集群",
        school="营销学",
        department="户部",
        leader_name="科特勒",
        members={
            "科特勒": KotlerCloning(),
            "奥格威": _DavidOgilvyCloning(),
            "特劳特": _JackTroutCloning(),
            "里斯": _AlRiesCloning(),
            "舒尔茨": _DonSchultzCloning(),
            "莱维特": _TheodoreLevittCloning(),
        },
    )
__all__ = ['build_cluster']
