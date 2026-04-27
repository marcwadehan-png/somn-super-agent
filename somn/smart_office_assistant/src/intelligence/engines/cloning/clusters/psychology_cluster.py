# -*- coding: utf-8 -*-
"""心理学集群 Cloning - Tier 2 学派集群"""

from typing import Dict, List, Optional, Any
from .._cloning_base import SageCloning, SchoolCluster
from .._cloning_types import AnalysisResult, DecisionResult, SageProfile, CloningTier


class _SigmundFreudCloning(SageCloning):
    """弗洛伊德 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="弗洛伊德", name_en="Sigmund Freud", era="19-20世纪", years="1856-1939",
            school="精神分析", tier=CloningTier.TIER2_CLUSTER,
            position="礼部侍郎", department="礼部",
            title="精神分析之父", biography="精神分析学派创始人，提出潜意识、梦的解析、性心理发展阶段。",
            core_works=["《梦的解析》", "《精神分析引论》"],
            capability={"strategic_vision": 9, "execution": 6, "innovation": 10, "leadership": 7, "influence": 10, "cross_domain": 8},
        ))
        self._wisdom_laws = ["潜意识——人的行为受无意识驱动", "人格结构——本我自我超我三层次", "性驱力——性是人生最强大的动力"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="弗洛伊德", school="精神分析", problem=problem,
            perspective="从弗洛伊德的精神分析智慧出发",
            core_insight="人的行为受无意识驱动",
            recommendations=[["潜意识——人的行为受无意识驱动", "人格结构——本我自我超我三层次", "性驱力——性是人生最强大的动力"][i].split("——")[1] if "——" in ["潜意识——人的行为受无意识驱动", "人格结构——本我自我超我三层次", "性驱力——性是人生最强大的动力"][i] else ["潜意识——人的行为受无意识驱动", "人格结构——本我自我超我三层次", "性驱力——性是人生最强大的动力"][i] for i in range(len(["潜意识——人的行为受无意识驱动", "人格结构——本我自我超我三层次", "性驱力——性是人生最强大的动力"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.87,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["潜意", "本能", "欲望", "压抑", "梦"]) else 0))
        return DecisionResult(sage_name="弗洛伊德", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return "弗洛伊德的智慧：潜意识——人的行为受无意识驱动"


class _CarlJungCloning(SageCloning):
    """荣格 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="荣格", name_en="Carl Jung", era="19-20世纪", years="1875-1961",
            school="分析心理学", tier=CloningTier.TIER2_CLUSTER,
            position="礼部侍郎", department="礼部",
            title="集体无意识之父", biography="瑞士心理学家，分析心理学创始人，提出集体无意识、原型和人格类型。",
            core_works=["《原型与集体无意识》", "《心理类型》"],
            capability={"strategic_vision": 10, "execution": 6, "innovation": 10, "leadership": 6, "influence": 10, "cross_domain": 10},
        ))
        self._wisdom_laws = ["集体无意识——人类共享的心理原型", "原型理论——英雄、母亲、阴影等普遍模式", "人格类型——内向外向思维情感直觉"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="荣格", school="分析心理学", problem=problem,
            perspective="从荣格的集体无意识智慧出发",
            core_insight="人类共享的心理原型",
            recommendations=[["集体无意识——人类共享的心理原型", "原型理论——英雄、母亲、阴影等普遍模式", "人格类型——内向外向思维情感直觉"][i].split("——")[1] if "——" in ["集体无意识——人类共享的心理原型", "原型理论——英雄、母亲、阴影等普遍模式", "人格类型——内向外向思维情感直觉"][i] else ["集体无意识——人类共享的心理原型", "原型理论——英雄、母亲、阴影等普遍模式", "人格类型——内向外向思维情感直觉"][i] for i in range(len(["集体无意识——人类共享的心理原型", "原型理论——英雄、母亲、阴影等普遍模式", "人格类型——内向外向思维情感直觉"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.88,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["原型", "集体", "人格", "阴影", "自性"]) else 0))
        return DecisionResult(sage_name="荣格", problem=context.get("problem",""), chosen_option=chosen, confidence=0.84)

    def advise(self, context: Dict[str, Any]) -> str:
        return "荣格的智慧：集体无意识——人类共享的心理原型"


class _AbrahamMaslowCloning(SageCloning):
    """马斯洛 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="马斯洛", name_en="Abraham Maslow", era="20世纪", years="1908-1970",
            school="人本心理学", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="礼部",
            title="需求层次之父", biography="美国心理学家，人本心理学创始人，提出需求层次理论和自我实现。",
            core_works=["《动机与人格》"],
            capability={"strategic_vision": 9, "execution": 7, "innovation": 10, "leadership": 7, "influence": 10, "cross_domain": 8},
        ))
        self._wisdom_laws = ["需求层次——生理安全社交尊重自我实现", "自我实现——成为你自己", "高峰体验——全神贯注的忘我状态"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="马斯洛", school="人本心理学", problem=problem,
            perspective="从马斯洛的需求层次智慧出发",
            core_insight="生理安全社交尊重自我实现",
            recommendations=[["需求层次——生理安全社交尊重自我实现", "自我实现——成为你自己", "高峰体验——全神贯注的忘我状态"][i].split("——")[1] if "——" in ["需求层次——生理安全社交尊重自我实现", "自我实现——成为你自己", "高峰体验——全神贯注的忘我状态"][i] else ["需求层次——生理安全社交尊重自我实现", "自我实现——成为你自己", "高峰体验——全神贯注的忘我状态"][i] for i in range(len(["需求层次——生理安全社交尊重自我实现", "自我实现——成为你自己", "高峰体验——全神贯注的忘我状态"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.88,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["需求", "动机", "自我实现", "成长", "尊重"]) else 0))
        return DecisionResult(sage_name="马斯洛", problem=context.get("problem",""), chosen_option=chosen, confidence=0.84)

    def advise(self, context: Dict[str, Any]) -> str:
        return "马斯洛的智慧：需求层次——生理安全社交尊重自我实现"


class _BFSkinnerCloning(SageCloning):
    """斯金纳 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="斯金纳", name_en="B.F. Skinner", era="20世纪", years="1904-1990",
            school="行为主义", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="礼部",
            title="行为强化之父", biography="美国心理学家，行为主义代表人物，提出操作性条件反射。",
            core_works=["《科学与人类行为》", "《Walden Two》"],
            capability={"strategic_vision": 8, "execution": 8, "innovation": 9, "leadership": 6, "influence": 9, "cross_domain": 7},
        ))
        self._wisdom_laws = ["操作性条件反射——行为由结果塑造", "强化理论——正负强化塑造行为", "行为工程——设计环境可以塑造任何人"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="斯金纳", school="行为主义", problem=problem,
            perspective="从斯金纳的行为主义智慧出发",
            core_insight="行为由结果塑造",
            recommendations=[["操作性条件反射——行为由结果塑造", "强化理论——正负强化塑造行为", "行为工程——设计环境可以塑造任何人"][i].split("——")[1] if "——" in ["操作性条件反射——行为由结果塑造", "强化理论——正负强化塑造行为", "行为工程——设计环境可以塑造任何人"][i] else ["操作性条件反射——行为由结果塑造", "强化理论——正负强化塑造行为", "行为工程——设计环境可以塑造任何人"][i] for i in range(len(["操作性条件反射——行为由结果塑造", "强化理论——正负强化塑造行为", "行为工程——设计环境可以塑造任何人"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.86,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["强化", "行为", "环境", "习惯", "激励"]) else 0))
        return DecisionResult(sage_name="斯金纳", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return "斯金纳的智慧：操作性条件反射——行为由结果塑造"


class _JeanPiagetCloning(SageCloning):
    """皮亚杰 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="皮亚杰", name_en="Jean Piaget", era="20世纪", years="1896-1980",
            school="认知发展心理学", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="礼部",
            title="认知发展之父", biography="瑞士心理学家，提出儿童认知发展的四个阶段理论。",
            core_works=["《儿童智力的起源》", "《儿童的心理起源》"],
            capability={"strategic_vision": 9, "execution": 7, "innovation": 10, "leadership": 6, "influence": 9, "cross_domain": 8},
        ))
        self._wisdom_laws = ["认知发展阶段——感知运动前运算具体运算形式运算", "图式——组织化认知结构", "建构主义——知识是主动建构而非被动接受"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="皮亚杰", school="认知发展心理学", problem=problem,
            perspective="从皮亚杰的认知发展智慧出发",
            core_insight="感知运动前运算具体运算形式运算",
            recommendations=[["认知发展阶段——感知运动前运算具体运算形式运算", "图式——组织化认知结构", "建构主义——知识是主动建构而非被动接受"][i].split("——")[1] if "——" in ["认知发展阶段——感知运动前运算具体运算形式运算", "图式——组织化认知结构", "建构主义——知识是主动建构而非被动接受"][i] else ["认知发展阶段——感知运动前运算具体运算形式运算", "图式——组织化认知结构", "建构主义——知识是主动建构而非被动接受"][i] for i in range(len(["认知发展阶段——感知运动前运算具体运算形式运算", "图式——组织化认知结构", "建构主义——知识是主动建构而非被动接受"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.86,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["认知", "发展", "图式", "建构", "阶段"]) else 0))
        return DecisionResult(sage_name="皮亚杰", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return "皮亚杰的智慧：认知发展阶段——感知运动前运算具体运算形式运算"


class _AlbertBanduraCloning(SageCloning):
    """班杜拉 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="班杜拉", name_en="Albert Bandura", era="20-21世纪", years="1925-2021",
            school="社会学习理论", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="礼部",
            title="社会学习理论之父", biography="加拿大心理学家，提出社会学习理论、自我效能感概念。",
            core_works=["《思想和行动的社会基础》"],
            capability={"strategic_vision": 9, "execution": 8, "innovation": 10, "leadership": 7, "influence": 9, "cross_domain": 8},
        ))
        self._wisdom_laws = ["观察学习——人通过观察他人学习", "自我效能感——相信自己能做到", "交互决定论——个人环境行为三者互相关联"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="班杜拉", school="社会学习理论", problem=problem,
            perspective="从班杜拉的社会学习智慧出发",
            core_insight="人通过观察他人学习",
            recommendations=[["观察学习——人通过观察他人学习", "自我效能感——相信自己能做到", "交互决定论——个人环境行为三者互相关联"][i].split("——")[1] if "——" in ["观察学习——人通过观察他人学习", "自我效能感——相信自己能做到", "交互决定论——个人环境行为三者互相关联"][i] else ["观察学习——人通过观察他人学习", "自我效能感——相信自己能做到", "交互决定论——个人环境行为三者互相关联"][i] for i in range(len(["观察学习——人通过观察他人学习", "自我效能感——相信自己能做到", "交互决定论——个人环境行为三者互相关联"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.87,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["观察", "模仿", "效能", "学习", "信心"]) else 0))
        return DecisionResult(sage_name="班杜拉", problem=context.get("problem",""), chosen_option=chosen, confidence=0.84)

    def advise(self, context: Dict[str, Any]) -> str:
        return "班杜拉的智慧：观察学习——人通过观察他人学习"


class _RobertCialdiniCloning(SageCloning):
    """西奥迪尼 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="西奥迪尼", name_en="Robert Cialdini", era="20-21世纪", years="1945-",
            school="社会心理学", tier=CloningTier.TIER2_CLUSTER,
            position="户部主事", department="户部",
            title="影响力六要素之父", biography="美国心理学家，提出影响力的六大原则。",
            core_works=["《影响力》"],
            capability={"strategic_vision": 8, "execution": 9, "innovation": 8, "leadership": 7, "influence": 10, "cross_domain": 8},
        ))
        self._wisdom_laws = ["互惠——受人恩惠必须回报", "社会认同——人跟随多数人的行为", "承诺一致——人倾向履行公开承诺"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="西奥迪尼", school="社会心理学", problem=problem,
            perspective="从西奥迪尼的影响力智慧出发",
            core_insight="受人恩惠必须回报",
            recommendations=[["互惠——受人恩惠必须回报", "社会认同——人跟随多数人的行为", "承诺一致——人倾向履行公开承诺"][i].split("——")[1] if "——" in ["互惠——受人恩惠必须回报", "社会认同——人跟随多数人的行为", "承诺一致——人倾向履行公开承诺"][i] else ["互惠——受人恩惠必须回报", "社会认同——人跟随多数人的行为", "承诺一致——人倾向履行公开承诺"][i] for i in range(len(["互惠——受人恩惠必须回报", "社会认同——人跟随多数人的行为", "承诺一致——人倾向履行公开承诺"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.88,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["影响", "说服", "互惠", "认同", "承诺"]) else 0))
        return DecisionResult(sage_name="西奥迪尼", problem=context.get("problem",""), chosen_option=chosen, confidence=0.84)

    def advise(self, context: Dict[str, Any]) -> str:
        return "西奥迪尼的智慧：互惠——受人恩惠必须回报"


class _LevVygotskyCloning(SageCloning):
    """维果茨基 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="维果茨基", name_en="Lev Vygotsky", era="20世纪", years="1896-1934",
            school="社会文化理论", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="礼部",
            title="最近发展区之父", biography="俄国心理学家，提出社会文化理论、最近发展区概念。",
            core_works=["《思维与语言》"],
            capability={"strategic_vision": 10, "execution": 6, "innovation": 10, "leadership": 6, "influence": 9, "cross_domain": 9},
        ))
        self._wisdom_laws = ["最近发展区——学习发生在现有与潜在水平之间", "支架式教学——在能力边缘给予支持", "内化——社会互动逐渐转为内部思维"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="维果茨基", school="社会文化理论", problem=problem,
            perspective="从维果茨基的社会文化智慧出发",
            core_insight="学习发生在现有与潜在水平之间",
            recommendations=[["最近发展区——学习发生在现有与潜在水平之间", "支架式教学——在能力边缘给予支持", "内化——社会互动逐渐转为内部思维"][i].split("——")[1] if "——" in ["最近发展区——学习发生在现有与潜在水平之间", "支架式教学——在能力边缘给予支持", "内化——社会互动逐渐转为内部思维"][i] else ["最近发展区——学习发生在现有与潜在水平之间", "支架式教学——在能力边缘给予支持", "内化——社会互动逐渐转为内部思维"][i] for i in range(len(["最近发展区——学习发生在现有与潜在水平之间", "支架式教学——在能力边缘给予支持", "内化——社会互动逐渐转为内部思维"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.86,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["学习", "支架", "发展", "文化", "互动"]) else 0))
        return DecisionResult(sage_name="维果茨基", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return "维果茨基的智慧：最近发展区——学习发生在现有与潜在水平之间"


class _MartinSeligmanCloning(SageCloning):
    """塞利格曼 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="塞利格曼", name_en="Martin Seligman", era="20-21世纪", years="1942-",
            school="积极心理学", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="礼部",
            title="积极心理学之父", biography="美国心理学家，积极心理学创始人，提出习得性无助与乐观学习。",
            core_works=["《活出乐观的自己》", "《真实的幸福》"],
            capability={"strategic_vision": 9, "execution": 8, "innovation": 10, "leadership": 8, "influence": 9, "cross_domain": 8},
        ))
        self._wisdom_laws = ["习得性无助——反复失败导致放弃", "解释风格——对事件的解读方式影响情绪", "PERMA模型——积极情绪投入关系意义成就"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="塞利格曼", school="积极心理学", problem=problem,
            perspective="从塞利格曼的积极心理学智慧出发",
            core_insight="反复失败导致放弃",
            recommendations=[["习得性无助——反复失败导致放弃", "解释风格——对事件的解读方式影响情绪", "PERMA模型——积极情绪投入关系意义成就"][i].split("——")[1] if "——" in ["习得性无助——反复失败导致放弃", "解释风格——对事件的解读方式影响情绪", "PERMA模型——积极情绪投入关系意义成就"][i] else ["习得性无助——反复失败导致放弃", "解释风格——对事件的解读方式影响情绪", "PERMA模型——积极情绪投入关系意义成就"][i] for i in range(len(["习得性无助——反复失败导致放弃", "解释风格——对事件的解读方式影响情绪", "PERMA模型——积极情绪投入关系意义成就"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.87,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["乐观", "积极", "幸福", "无助", "成长"]) else 0))
        return DecisionResult(sage_name="塞利格曼", problem=context.get("problem",""), chosen_option=chosen, confidence=0.84)

    def advise(self, context: Dict[str, Any]) -> str:
        return "塞利格曼的智慧：习得性无助——反复失败导致放弃"


def build_cluster() -> SchoolCluster:
    """构建心理学集群"""
    return SchoolCluster(
        name="心理学集群",
        school="心理学",
        department="礼部",
        leader_name="弗洛伊德",
        members={
            "弗洛伊德": _SigmundFreudCloning(),
            "荣格": _CarlJungCloning(),
            "马斯洛": _AbrahamMaslowCloning(),
            "斯金纳": _BFSkinnerCloning(),
            "皮亚杰": _JeanPiagetCloning(),
            "班杜拉": _AlbertBanduraCloning(),
            "西奥迪尼": _RobertCialdiniCloning(),
            "维果茨基": _LevVygotskyCloning(),
            "塞利格曼": _MartinSeligmanCloning(),
        },
    )
__all__ = ['build_cluster']
