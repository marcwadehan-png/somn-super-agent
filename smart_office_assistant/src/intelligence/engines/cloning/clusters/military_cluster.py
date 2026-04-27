# -*- coding: utf-8 -*-
"""
兵家集群 Cloning - Tier 2 学派集群
领军人物：孙武
成员：孙膑、吴起、韩信、曹操（可扩展至80+人）
"""

from typing import Dict, List, Optional, Any

from .._cloning_base import SageCloning, SchoolCluster
from .._cloning_types import AnalysisResult, DecisionResult, SageProfile, CloningTier


class _SunBianCloning(SageCloning):
    """孙膑Cloning - 围魏救赵"""
    def __init__(self):
        super().__init__(SageProfile(
            name="孙膑", name_en="Sun Bin", era="战国中期", years="不详-前316",
            school="兵家", tier=CloningTier.TIER2_CLUSTER,
            position="兵部主事", department="兵部",
            title="兵圣后裔", biography="孙武后裔，战国时期军事家。以'围魏救赵'、'减灶诱敌'等策略闻名。著有《孙膑兵法》。",
            core_works=["《孙膑兵法》"],
            capability={"strategic_vision": 9, "execution": 10, "innovation": 9, "leadership": 7, "influence": 8, "cross_domain": 7},
        ))
        self._wisdom_laws = [
            "围魏救赵 —— 攻其必救，间接路线胜过直接对抗",
            "因势利导 —— 根据敌我形势灵活调整策略",
            "赏罚分明 —— 以赏罚激励士气",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="孙膑", school="兵家", problem=problem,
            perspective="从间接路线的战术智慧出发",
            core_insight="直接攻击往往代价最大。找到对手的'大梁'——它必须回防的核心利益，攻击那里。",
            recommendations=[
                "找到对手最在意的核心——那就是它的'大梁'",
                "不要正面硬碰——间接路线往往更有效",
                "利用对手的心理——'减灶'制造假象",
                "以弱示敌——让对手轻敌后再出击",
            ],
            wisdom_laws_applied=self._wisdom_laws,
            confidence=0.87,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["间接","迂回","智取","灵活"]) else 0))
        return DecisionResult(sage_name="孙膑", problem=context.get("problem",""), chosen_option=chosen, confidence=0.84)

    def advise(self, context: Dict[str, Any]) -> str:
        return "孙膑策略：不要和对手硬碰硬，找到它的致命弱点——它最在乎的东西。攻击那里，它不得不回防，你就掌握了主动。"


class _WuQiCloning(SageCloning):
    """吴起Cloning - 治军典范"""
    def __init__(self):
        super().__init__(SageProfile(
            name="吴起", name_en="Wu Qi", era="战国初期", years="前440-前381",
            school="兵家", tier=CloningTier.TIER2_CLUSTER,
            position="兵部主事", department="兵部",
            title="兵家亚圣", biography="战国初期军事家、政治家。著有《吴子》，提出'内修文德，外治武备'的治军理念。",
            core_works=["《吴子》"],
            capability={"strategic_vision": 8, "execution": 10, "innovation": 8, "leadership": 10, "influence": 8, "cross_domain": 7},
        ))
        self._wisdom_laws = [
            "内修文德外治武备 —— 文武并重，德才兼备",
            "用兵之法，教戒为先 —— 培训和纪律是战斗力的基础",
            "因敌变化而取胜 —— 灵活应变是制胜关键",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="吴起", school="兵家", problem=problem,
            perspective="从治军和团队建设的实战经验出发",
            core_insight="战斗力的根本在于人的素质和纪律。'教戒为先'——先训练，后上阵。",
            recommendations=[
                "先投资于人的培养——培训是最好的投资",
                "文武并重——既要硬实力也要软实力",
                "与士兵同甘共苦——领导者的以身作则是最强的激励",
                "根据对手调整策略——没有万能的方法",
            ],
            wisdom_laws_applied=self._wisdom_laws,
            confidence=0.86,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["训练","纪律","实干","以身作则"]) else 0))
        return DecisionResult(sage_name="吴起", problem=context.get("problem",""), chosen_option=chosen, confidence=0.84)

    def advise(self, context: Dict[str, Any]) -> str:
        return "吴起曰：'用兵之法，教戒为先。' 不管做什么事，先确保团队有足够的能力和纪律。"


class _HanXinCloning(SageCloning):
    """韩信Cloning - 兵仙"""
    def __init__(self):
        super().__init__(SageProfile(
            name="韩信", name_en="Han Xin", era="秦末汉初", years="前231-前196",
            school="兵家", tier=CloningTier.TIER2_CLUSTER,
            position="五军都督府都督", department="五军都督府",
            title="兵仙", biography="汉初军事家，被称为'兵仙'。以背水一战、十面埋伏、明修栈道暗渡陈仓等经典战例闻名。",
            core_works=["《韩信兵法》(已佚)"],
            capability={"strategic_vision": 10, "execution": 10, "innovation": 10, "leadership": 9, "influence": 9, "cross_domain": 7},
        ))
        self._wisdom_laws = [
            "背水一战 —— 置之死地而后生，极端环境激发极限潜力",
            "多多益善 —— 管理规模的核心是标准化和分权",
            "明修栈道暗渡陈仓 —— 声东击西，虚实结合",
            "国士无双 —— 真正的人才值得以最高的礼遇对待",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="韩信", school="兵家", problem=problem,
            perspective="从'兵仙'的极端战术思维出发",
            core_insight="在绝境中反而能激发最大的战斗力。当常规手段无效时，反其道而行往往能绝处逢生。",
            recommendations=[
                "如果常规方法行不通，考虑反向操作",
                "利用信息不对称——'明修栈道暗渡陈仓'",
                "给团队制造'背水'的紧迫感——但要有赢的方案",
                "'多多益善'——通过标准化和分权来管理大规模",
            ],
            wisdom_laws_applied=self._wisdom_laws,
            confidence=0.88,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["奇招","反常","冒险","大胆"]) else 0))
        return DecisionResult(sage_name="韩信", problem=context.get("problem",""), chosen_option=chosen, confidence=0.85)

    def advise(self, context: Dict[str, Any]) -> str:
        return "韩信说：'成也萧何，败也萧何。' 任何人的成功都依赖团队的支持。但也记住：背水一战时，你比自己想象的更强。"


def build_cluster() -> SchoolCluster:
    """构建兵家集群"""
    from ..tier1.sunwu import SunWuCloning

    cluster = SchoolCluster(
        name="兵家集群",
        school="兵家",
        department="兵部",
        leader_name="孙武",
        members={
            "孙武": SunWuCloning(),
            "孙膑": _SunBianCloning(),
            "吴起": _WuQiCloning(),
            "韩信": _HanXinCloning(),
        },
    )
    return cluster
__all__ = ['build_cluster']
