# -*- coding: utf-8 -*-
"""心学集群 Cloning - Tier 2 学派集群"""

from typing import Dict, List, Optional, Any
from .._cloning_base import SageCloning, SchoolCluster
from .._cloning_types import AnalysisResult, DecisionResult, SageProfile, CloningTier


class _LuJiuyuanCloning(SageCloning):
    """陆九渊Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="陆九渊", name_en="Lu Jiuyuan", era="南宋", years="1139-1193",
            school="心学", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="礼部",
            title="象山先生", biography="南宋理学家，心学先驱，提出'心即理'。",
            core_works=["《象山全集》"],
            capability={"strategic_vision": 8, "execution": 7, "innovation": 9, "leadership": 7, "influence": 8, "cross_domain": 7},
        ))
        self._wisdom_laws = ["心即理——心外无物，心外无理", "辨志——先立志再治学", "易简功夫——大道至简"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="陆九渊", school="心学", problem=problem,
            perspective="从陆九渊的象山先生智慧出发",
            core_insight="心外无物，心外无理",
            recommendations=[["心即理——心外无物，心外无理", "辨志——先立志再治学", "易简功夫——大道至简"][i].split("——")[1] if "——" in ["心即理——心外无物，心外无理", "辨志——先立志再治学", "易简功夫——大道至简"][i] else ["心即理——心外无物，心外无理", "辨志——先立志再治学", "易简功夫——大道至简"][i] for i in range(len(["心即理——心外无物，心外无理", "辨志——先立志再治学", "易简功夫——大道至简"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["本心", "立志", "简洁", "直觉"]) else 0))
        return DecisionResult(sage_name="陆九渊", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"陆九渊的智慧：心即理——心外无物，心外无理"


class _LiZhiCloning(SageCloning):
    """李贽Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="李贽", name_en="Li Zhi", era="明代", years="1527-1602",
            school="心学", tier=CloningTier.TIER2_CLUSTER,
            position="吏部主事", department="礼部",
            title="卓吾先生", biography="明代思想家，以批判精神著称，主张个性解放。",
            core_works=["《焚书》《藏书》"],
            capability={"strategic_vision": 7, "execution": 6, "innovation": 10, "leadership": 6, "influence": 8, "cross_domain": 7},
        ))
        self._wisdom_laws = ["童心说——保持真实不被污染的心", "反传统——质疑权威和教条", "个性解放——尊重每个人的独特性"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="李贽", school="心学", problem=problem,
            perspective="从李贽的卓吾先生智慧出发",
            core_insight="保持真实不被污染的心",
            recommendations=[["童心说——保持真实不被污染的心", "反传统——质疑权威和教条", "个性解放——尊重每个人的独特性"][i].split("——")[1] if "——" in ["童心说——保持真实不被污染的心", "反传统——质疑权威和教条", "个性解放——尊重每个人的独特性"][i] else ["童心说——保持真实不被污染的心", "反传统——质疑权威和教条", "个性解放——尊重每个人的独特性"][i] for i in range(len(["童心说——保持真实不被污染的心", "反传统——质疑权威和教条", "个性解放——尊重每个人的独特性"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["真实", "反叛", "个性", "自由"]) else 0))
        return DecisionResult(sage_name="李贽", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"李贽的智慧：童心说——保持真实不被污染的心"


class _HuangZongxiCloning(SageCloning):
    """黄宗羲Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="黄宗羲", name_en="Huang Zongxi", era="明末清初", years="1610-1695",
            school="心学", tier=CloningTier.TIER2_CLUSTER,
            position="吏部侍郎", department="礼部",
            title="梨洲先生", biography="明末清初思想家，提出'天下为主君为客'。",
            core_works=["《明夷待访录》"],
            capability={"strategic_vision": 9, "execution": 6, "innovation": 9, "leadership": 7, "influence": 9, "cross_domain": 8},
        ))
        self._wisdom_laws = ["天下为主君为客——权力来源于人民", "学校议政——公共讨论是治理基础", "工商皆本——经济思想的超前突破"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="黄宗羲", school="心学", problem=problem,
            perspective="从黄宗羲的梨洲先生智慧出发",
            core_insight="权力来源于人民",
            recommendations=[["天下为主君为客——权力来源于人民", "学校议政——公共讨论是治理基础", "工商皆本——经济思想的超前突破"][i].split("——")[1] if "——" in ["天下为主君为客——权力来源于人民", "学校议政——公共讨论是治理基础", "工商皆本——经济思想的超前突破"][i] else ["天下为主君为客——权力来源于人民", "学校议政——公共讨论是治理基础", "工商皆本——经济思想的超前突破"][i] for i in range(len(["天下为主君为客——权力来源于人民", "学校议政——公共讨论是治理基础", "工商皆本——经济思想的超前突破"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["民主", "经济", "制度", "公共"]) else 0))
        return DecisionResult(sage_name="黄宗羲", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"黄宗羲的智慧：天下为主君为客——权力来源于人民"


def build_cluster() -> SchoolCluster:
    """构建心学集群"""
    from ..tier1.wangyangming import WangYangMingCloning

    return SchoolCluster(
        name="心学集群",
        school="心学",
        department="礼部",
        leader_name="王阳明",
        members={
            "王阳明": WangYangMingCloning(),
            "陆九渊": _LuJiuyuanCloning(),
            "李贽": _LiZhiCloning(),
            "黄宗羲": _HuangZongxiCloning(),
        },
    )
__all__ = ['build_cluster']
