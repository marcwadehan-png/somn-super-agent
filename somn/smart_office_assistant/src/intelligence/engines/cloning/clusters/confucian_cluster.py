# -*- coding: utf-8 -*-
"""
儒家集群 Cloning - Tier 2 学派集群
领军人物：孔子
成员：孟子、荀子、颜回、曾子、子思、董仲舒、朱熹（可扩展至50+人）

集群包含同领域多个贤者的Cloning，支持leader/consensus/debate/synthesis四种咨询方法。
"""

from typing import Dict, List, Optional, Any

from .._cloning_base import SageCloning, SchoolCluster
from .._cloning_types import (
    AnalysisResult, SageProfile, CloningTier,
)


class _MengZiCloning(SageCloning):
    """孟子Cloning - 性善论"""
    def __init__(self):
        super().__init__(SageProfile(
            name="孟子", name_en="Mencius", era="战国中期", years="前372-前289",
            school="儒家", tier=CloningTier.TIER2_CLUSTER,
            position="礼部侍郎", department="礼部",
            title="亚圣", biography="儒家学派重要继承人，提出性善论和仁政思想。",
            core_works=["《孟子》"],
            capability={"strategic_vision": 9, "execution": 8, "innovation": 8, "leadership": 9, "influence": 9, "cross_domain": 7},
        ))
        self._wisdom_laws = [
            "性善论 —— 人皆有恻隐羞恶辞让是非之心",
            "仁政 —— 以民为本，民为贵社稷次之君为轻",
            "浩然之气 —— 至大至刚的道德勇气",
            "义利之辨 —— 先义后利，不以利害义",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="孟子", school="儒家", problem=problem,
            perspective="从性善论和仁政出发",
            core_insight='人性本善，管理的关键是创造让人行善的环境。"仁政"的核心是以民为本。',
            recommendations=[
                "以恻隐之心为出发点，理解各方的需求和感受",
                "培养团队的'浩然之气'——正直和勇气",
                "坚持'义'的原则，不被短期利益诱惑",
                "'民为贵'——关注终端用户和基层员工的真实感受",
            ],
            wisdom_laws_applied=self._wisdom_laws[:3],
            confidence=0.88,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["仁","善","民","义"]) else 0))
        return DecisionResult(sage_name="孟子", problem=context.get("problem",""), chosen_option=chosen,
                             reasoning="以仁义为标准选择", confidence=0.85)

    def advise(self, context: Dict[str, Any]) -> str:
        return "孟子曰：'富贵不能淫，贫贱不能移，威武不能屈。' 保持内心的坚守，不为外物所动。"


class _XunZiCloning(SageCloning):
    """荀子Cloning - 性恶论/礼制"""
    def __init__(self):
        super().__init__(SageProfile(
            name="荀子", name_en="Xun Zi", era="战国末期", years="前313-前238",
            school="儒家", tier=CloningTier.TIER2_CLUSTER,
            position="吏部侍郎", department="吏部",
            title="后圣", biography="儒家集大成者，提出性恶论和礼制思想，弟子韩非、李斯为法家代表。",
            core_works=["《荀子》"],
            capability={"strategic_vision": 8, "execution": 9, "innovation": 8, "leadership": 8, "influence": 8, "cross_domain": 7},
        ))
        self._wisdom_laws = [
            "性恶论 —— 人性趋利，需以礼义教化",
            "制名指实 —— 概念清晰是有效沟通的基础",
            "学无止境 —— 学不可以已，终身学习",
            "天人相分 —— 尽人事而不必求天",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="荀子", school="儒家", problem=problem,
            perspective="从性恶论和礼制教化出发",
            core_insight="承认人性的趋利本质，通过制度（礼）来引导和约束，比依赖道德更可靠。",
            recommendations=[
                "设计合理的制度来引导行为，不要依赖人的自觉",
                "建立清晰的角色定义和职责划分（正名）",
                "持续学习——'学不可以已'",
                "区分可控和不可控——'天行有常，不为尧存，不为桀亡'",
            ],
            wisdom_laws_applied=self._wisdom_laws[:3],
            confidence=0.87,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["制度","规则","学习","务实"]) else 0))
        return DecisionResult(sage_name="荀子", problem=context.get("problem",""), chosen_option=chosen,
                             reasoning="以礼制教化为标准选择", confidence=0.85)

    def advise(self, context: Dict[str, Any]) -> str:
        return "荀子曰：'不积跬步，无以至千里；不积小流，无以成江海。' 积少成多，持之以恒。"


class _YanHuiCloning(SageCloning):
    """颜回Cloning - 修身典范"""
    def __init__(self):
        super().__init__(SageProfile(
            name="颜回", name_en="Yan Hui", era="春秋末期", years="前521-前481",
            school="儒家", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="礼部",
            title="复圣", biography="孔子最得意的弟子，以德行著称，被后世尊为'复圣'。",
            core_works=[],
            capability={"strategic_vision": 6, "execution": 7, "innovation": 6, "leadership": 7, "influence": 7, "cross_domain": 5},
        ))
        self._wisdom_laws = [
            "不迁怒不贰过 —— 同样的错误不犯第二次",
            "安贫乐道 —— 内心富足胜过外在富足",
            "好学 —— '有颜回者好学，不迁怒，不贰过'",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="颜回", school="儒家", problem=problem,
            perspective="从修身和好学出发",
            core_insight="面对任何问题，先反思自身：我有哪里做得不够好？同样的错误我是否在重复？",
            recommendations=[
                "不迁怒——问题出现时先从自身找原因",
                "不贰过——建立错误记录，确保不重复",
                "安贫乐道——在条件有限时也能保持状态",
                "持续学习——'一箪食一瓢饮，不改其乐'",
            ],
            wisdom_laws_applied=self._wisdom_laws,
            confidence=0.82,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (1.5 if any(w in o for w in ["修身","反思","学习"]) else 0))
        return DecisionResult(sage_name="颜回", problem=context.get("problem",""), chosen_option=chosen, confidence=0.80)

    def advise(self, context: Dict[str, Any]) -> str:
        return "颜回的精神：'一箪食，一瓢饮，在陋巷，人不堪其忧，回也不改其乐。' 内心的充实是最重要的。"


class _WangAnShiCloning(SageCloning):
    """王安石Cloning - 改革家"""
    def __init__(self):
        super().__init__(SageProfile(
            name="王安石", name_en="Wang Anshi", era="北宋", years="1021-1086",
            school="儒家", tier=CloningTier.TIER2_CLUSTER,
            position="户部侍郎", department="户部",
            title="临川先生", biography="北宋政治家、思想家、文学家，主导熙宁变法，提出'天变不足畏，祖宗不足法，人言不足恤'。",
            core_works=["《临川先生文集》"],
            capability={"strategic_vision": 10, "execution": 8, "innovation": 9, "leadership": 8, "influence": 9, "cross_domain": 7},
        ))
        self._wisdom_laws = [
            "三不足精神 —— 天变不足畏、祖宗不足法、人言不足恤",
            "经世致用 —— 理论必须服务于实际治理",
            "理财有道 —— 善理财者，不加赋而国用足",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="王安石", school="儒家", problem=problem,
            perspective="从改革家的经世致用精神出发",
            core_insight="改革需要'三不足'的勇气——不畏天命、不拘祖法、不顾人言。同时要务实——好的政策必须能在实践中落地。",
            recommendations=[
                "如果现有做法明显不合理，敢于打破常规",
                "任何改革必须有具体的实施方案，不能停留在口号",
                "预期管理——让利益相关者理解改革的必要性",
                "渐进推进——先试点再推广",
            ],
            wisdom_laws_applied=self._wisdom_laws,
            confidence=0.86,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["改革","务实","高效","创新"]) else 0))
        return DecisionResult(sage_name="王安石", problem=context.get("problem",""), chosen_option=chosen, confidence=0.84)

    def advise(self, context: Dict[str, Any]) -> str:
        return "王安石曰：'天变不足畏，祖宗不足法，人言不足恤。' 做正确的事，不要被传统和舆论束缚。"


def build_cluster() -> SchoolCluster:
    """构建儒家集群"""
    from ..tier1.confucius import ConfuciusCloning

    cluster = SchoolCluster(
        name="儒家集群",
        school="儒家",
        department="吏部/礼部",
        leader_name="孔子",
        members={
            "孔子": ConfuciusCloning(),
            "孟子": _MengZiCloning(),
            "荀子": _XunZiCloning(),
            "颜回": _YanHuiCloning(),
            "王安石": _WangAnShiCloning(),
        },
    )
    return cluster
__all__ = ['build_cluster']
