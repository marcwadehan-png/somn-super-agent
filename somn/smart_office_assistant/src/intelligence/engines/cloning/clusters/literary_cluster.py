# -*- coding: utf-8 -*-
"""文学集群 Cloning - Tier 2 学派集群"""

from typing import Dict, List, Optional, Any
from .._cloning_base import SageCloning, SchoolCluster
from .._cloning_types import AnalysisResult, DecisionResult, SageProfile, CloningTier


class _LiBaiCloning(SageCloning):
    """李白Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="李白", name_en="Li Bai", era="唐代", years="701-762",
            school="文学", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="礼部",
            title="诗仙", biography="唐代浪漫主义诗人，被称为'诗仙'。",
            core_works=["《李太白集》"],
            capability={"strategic_vision": 7, "execution": 5, "innovation": 10, "leadership": 5, "influence": 10, "cross_domain": 8},
        ))
        self._wisdom_laws = ["天生我材必有用——极致的自信和才华", "浪漫超越——突破现实的想象力", "自由精神——不受拘束的表达"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="李白", school="文学", problem=problem,
            perspective="从李白的诗仙智慧出发",
            core_insight="极致的自信和才华",
            recommendations=[["天生我材必有用——极致的自信和才华", "浪漫超越——突破现实的想象力", "自由精神——不受拘束的表达"][i].split("——")[1] if "——" in ["天生我材必有用——极致的自信和才华", "浪漫超越——突破现实的想象力", "自由精神——不受拘束的表达"][i] else ["天生我材必有用——极致的自信和才华", "浪漫超越——突破现实的想象力", "自由精神——不受拘束的表达"][i] for i in range(len(["天生我材必有用——极致的自信和才华", "浪漫超越——突破现实的想象力", "自由精神——不受拘束的表达"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["想象", "自由", "激情", "创意"]) else 0))
        return DecisionResult(sage_name="李白", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"李白的智慧：天生我材必有用——极致的自信和才华"


class _DuFuCloning(SageCloning):
    """杜甫Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="杜甫", name_en="Du Fu", era="唐代", years="712-770",
            school="文学", tier=CloningTier.TIER2_CLUSTER,
            position="礼部侍郎", department="礼部",
            title="诗圣", biography="唐代现实主义诗人，被称为'诗圣'。",
            core_works=["《杜工部集》"],
            capability={"strategic_vision": 8, "execution": 7, "innovation": 8, "leadership": 7, "influence": 10, "cross_domain": 8},
        ))
        self._wisdom_laws = ["忧国忧民——深沉的社会责任感", "现实主义——直面社会真相", "沉郁顿挫——深沉有力的表达"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="杜甫", school="文学", problem=problem,
            perspective="从杜甫的诗圣智慧出发",
            core_insight="深沉的社会责任感",
            recommendations=[["忧国忧民——深沉的社会责任感", "现实主义——直面社会真相", "沉郁顿挫——深沉有力的表达"][i].split("——")[1] if "——" in ["忧国忧民——深沉的社会责任感", "现实主义——直面社会真相", "沉郁顿挫——深沉有力的表达"][i] else ["忧国忧民——深沉的社会责任感", "现实主义——直面社会真相", "沉郁顿挫——深沉有力的表达"][i] for i in range(len(["忧国忧民——深沉的社会责任感", "现实主义——直面社会真相", "沉郁顿挫——深沉有力的表达"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["现实", "责任", "民生", "深度"]) else 0))
        return DecisionResult(sage_name="杜甫", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"杜甫的智慧：忧国忧民——深沉的社会责任感"


class _BaiJuyiCloning(SageCloning):
    """白居易Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="白居易", name_en="Bai Juyi", era="唐代", years="772-846",
            school="文学", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="礼部",
            title="诗魔", biography="唐代诗人，主张'文章合为时而著'。",
            core_works=["《白氏长庆集》"],
            capability={"strategic_vision": 8, "execution": 8, "innovation": 7, "leadership": 7, "influence": 9, "cross_domain": 7},
        ))
        self._wisdom_laws = ["通俗易懂——让所有人都能理解", "文章合为时而著——写作服务于现实", "兼济天下——知识分子的社会担当"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="白居易", school="文学", problem=problem,
            perspective="从白居易的诗魔智慧出发",
            core_insight="让所有人都能理解",
            recommendations=[["通俗易懂——让所有人都能理解", "文章合为时而著——写作服务于现实", "兼济天下——知识分子的社会担当"][i].split("——")[1] if "——" in ["通俗易懂——让所有人都能理解", "文章合为时而著——写作服务于现实", "兼济天下——知识分子的社会担当"][i] else ["通俗易懂——让所有人都能理解", "文章合为时而著——写作服务于现实", "兼济天下——知识分子的社会担当"][i] for i in range(len(["通俗易懂——让所有人都能理解", "文章合为时而著——写作服务于现实", "兼济天下——知识分子的社会担当"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["通俗", "现实", "传播", "社会"]) else 0))
        return DecisionResult(sage_name="白居易", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"白居易的智慧：通俗易懂——让所有人都能理解"


class _XinQijiCloning(SageCloning):
    """辛弃疾Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="辛弃疾", name_en="Xin Qiji", era="南宋", years="1140-1207",
            school="文学", tier=CloningTier.TIER2_CLUSTER,
            position="兵部主事", department="礼部",
            title="词中之龙", biography="南宋爱国词人，以豪放词风著称。",
            core_works=["《稼轩词》"],
            capability={"strategic_vision": 8, "execution": 8, "innovation": 9, "leadership": 8, "influence": 9, "cross_domain": 8},
        ))
        self._wisdom_laws = ["壮志难酬——理想与现实的永恒张力", "豪放创新——打破词的柔美传统", "文武兼备——词人中的将军"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="辛弃疾", school="文学", problem=problem,
            perspective="从辛弃疾的词中之龙智慧出发",
            core_insight="理想与现实的永恒张力",
            recommendations=[["壮志难酬——理想与现实的永恒张力", "豪放创新——打破词的柔美传统", "文武兼备——词人中的将军"][i].split("——")[1] if "——" in ["壮志难酬——理想与现实的永恒张力", "豪放创新——打破词的柔美传统", "文武兼备——词人中的将军"][i] else ["壮志难酬——理想与现实的永恒张力", "豪放创新——打破词的柔美传统", "文武兼备——词人中的将军"][i] for i in range(len(["壮志难酬——理想与现实的永恒张力", "豪放创新——打破词的柔美传统", "文武兼备——词人中的将军"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["豪放", "爱国", "创新", "跨界"]) else 0))
        return DecisionResult(sage_name="辛弃疾", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"辛弃疾的智慧：壮志难酬——理想与现实的永恒张力"


class _CaoXueqinCloning(SageCloning):
    """曹雪芹Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="曹雪芹", name_en="Cao Xueqin", era="清代", years="约1715-1763",
            school="文学", tier=CloningTier.TIER2_CLUSTER,
            position="礼部侍郎", department="礼部",
            title="红楼梦作者", biography="清代文学家，《红楼梦》作者。",
            core_works=["《红楼梦》"],
            capability={"strategic_vision": 9, "execution": 6, "innovation": 10, "leadership": 5, "influence": 10, "cross_domain": 9},
        ))
        self._wisdom_laws = ["人性洞察——对人性的深刻理解", "百科全书式写作——一个作品涵盖整个时代", "悲剧美学——在毁灭中展现美"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="曹雪芹", school="文学", problem=problem,
            perspective="从曹雪芹的红楼梦作者智慧出发",
            core_insight="对人性的深刻理解",
            recommendations=[["人性洞察——对人性的深刻理解", "百科全书式写作——一个作品涵盖整个时代", "悲剧美学——在毁灭中展现美"][i].split("——")[1] if "——" in ["人性洞察——对人性的深刻理解", "百科全书式写作——一个作品涵盖整个时代", "悲剧美学——在毁灭中展现美"][i] else ["人性洞察——对人性的深刻理解", "百科全书式写作——一个作品涵盖整个时代", "悲剧美学——在毁灭中展现美"][i] for i in range(len(["人性洞察——对人性的深刻理解", "百科全书式写作——一个作品涵盖整个时代", "悲剧美学——在毁灭中展现美"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["人性", "细节", "深度", "全貌"]) else 0))
        return DecisionResult(sage_name="曹雪芹", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"曹雪芹的智慧：人性洞察——对人性的深刻理解"


def build_cluster() -> SchoolCluster:
    """构建文学集群"""
    return SchoolCluster(
        name="文学集群",
        school="文学",
        department="礼部",
        leader_name="苏轼",
        members={
        "李白": _LiBaiCloning(),
        "杜甫": _DuFuCloning(),
        "白居易": _BaiJuyiCloning(),
        "辛弃疾": _XinQijiCloning(),
        "曹雪芹": _CaoXueqinCloning(),
        },
    )
__all__ = ['build_cluster']
