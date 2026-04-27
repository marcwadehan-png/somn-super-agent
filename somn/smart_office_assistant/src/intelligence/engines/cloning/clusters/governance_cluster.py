# -*- coding: utf-8 -*-
"""治理/战略集群 Cloning - Tier 2 学派集群
包括：马基雅维利、汉娜·阿伦特、约翰·罗尔斯、麦克纳马拉、安德鲁·格鲁夫、克劳塞维茨
"""

from typing import Dict, List, Optional, Any
from .._cloning_base import SageCloning, SchoolCluster
from .._cloning_types import AnalysisResult, DecisionResult, SageProfile, CloningTier


class _MachiavelliCloning(SageCloning):
    """马基雅维利 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="马基雅维利", name_en="Niccolo Machiavelli", era="15-16世纪", years="1469-1527",
            school="政治现实主义", tier=CloningTier.TIER2_CLUSTER,
            position="吏部尚书", department="吏部",
            title="现代政治学之父", biography="意大利政治家、历史学家，《君主论》作者，政治现实主义奠基人。",
            core_works=["《君主论》", "《论李维》"],
            capability={"strategic_vision": 10, "execution": 8, "innovation": 10, "leadership": 9, "influence": 10, "cross_domain": 8},
        ))
        self._wisdom_laws = ["目的正当手段——政治中结果重于过程", "狐狸与狮子——领导者需兼具智慧与力量", "命运与德能——一半靠命运一半靠能力"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="马基雅维利", school="政治现实主义", problem=problem,
            perspective="从马基雅维利的政治现实主义智慧出发",
            core_insight="政治中结果重于过程",
            recommendations=[w.split("——")[1] if "——" in w else w for w in self._wisdom_laws],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.88,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["权力", "策略", "实力", "结果", "控制"]) else 0))
        return DecisionResult(sage_name="马基雅维利", problem=context.get("problem",""), chosen_option=chosen, confidence=0.85)

    def advise(self, context: Dict[str, Any]) -> str:
        return "马基雅维利的智慧：目的正当手段——政治中结果重于过程"


class _HannahArendtCloning(SageCloning):
    """汉娜·阿伦特 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="汉娜·阿伦特", name_en="Hannah Arendt", era="20世纪", years="1906-1975",
            school="政治哲学", tier=CloningTier.TIER2_CLUSTER,
            position="吏部侍郎", department="吏部",
            title="政治哲学大师", biography="德裔美籍政治哲学家，《极权主义的起源》《人的条件》作者。",
            core_works=["《极权主义的起源》", "《人的条件》", "《平庸的恶》"],
            capability={"strategic_vision": 10, "execution": 6, "innovation": 10, "leadership": 7, "influence": 10, "cross_domain": 9},
        ))
        self._wisdom_laws = ["公共领域——政治需要公开的交流空间", "思考的重要性——平庸之恶源于不思考", "权力来自行动——权力在人们共同行动时产生"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="汉娜·阿伦特", school="政治哲学", problem=problem,
            perspective="从阿伦特的政治哲学智慧出发",
            core_insight="政治需要公开的交流空间",
            recommendations=[w.split("——")[1] if "——" in w else w for w in self._wisdom_laws],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.87,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["公共", "透明", "行动", "沟通", "责任"]) else 0))
        return DecisionResult(sage_name="汉娜·阿伦特", problem=context.get("problem",""), chosen_option=chosen, confidence=0.84)

    def advise(self, context: Dict[str, Any]) -> str:
        return "汉娜·阿伦特的智慧：公共领域——政治需要公开的交流空间"


class _JohnRawlsCloning(SageCloning):
    """约翰·罗尔斯 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="约翰·罗尔斯", name_en="John Rawls", era="20世纪", years="1921-2002",
            school="政治哲学", tier=CloningTier.TIER2_CLUSTER,
            position="吏部侍郎", department="吏部",
            title="正义理论之父", biography="美国政治哲学家，《正义论》作者，提出无知之幕思想实验。",
            core_works=["《正义论》", "《政治自由主义》"],
            capability={"strategic_vision": 9, "execution": 6, "innovation": 10, "leadership": 6, "influence": 10, "cross_domain": 8},
        ))
        self._wisdom_laws = ["无知之幕——在不知自己地位时选择最公正制度", "差异原则——不平等只有利于最弱势群体才合理", "原初状态——正义需要脱离个人利益的中立立场"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="约翰·罗尔斯", school="政治哲学", problem=problem,
            perspective="从罗尔斯的正义理论智慧出发",
            core_insight="在不知自己地位时选择最公正制度",
            recommendations=[w.split("——")[1] if "——" in w else w for w in self._wisdom_laws],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.87,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["公平", "公正", "平等", "弱势", "制度"]) else 0))
        return DecisionResult(sage_name="约翰·罗尔斯", problem=context.get("problem",""), chosen_option=chosen, confidence=0.84)

    def advise(self, context: Dict[str, Any]) -> str:
        return "约翰·罗尔斯的智慧：无知之幕——在不知自己地位时选择最公正制度"


class _RobertMcNamaraCloning(SageCloning):
    """麦克纳马拉 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="麦克纳马拉", name_en="Robert McNamara", era="20世纪", years="1916-2009",
            school="管理科学", tier=CloningTier.TIER2_CLUSTER,
            position="兵部尚书", department="兵部",
            title="系统分析之父", biography="福特汽车CEO、美国国防部长，将系统分析和量化方法引入政府管理。",
            core_works=["《回顾》", "《战争的迷雾》"],
            capability={"strategic_vision": 9, "execution": 10, "innovation": 9, "leadership": 9, "influence": 9, "cross_domain": 8},
        ))
        self._wisdom_laws = ["量化管理——用数据和指标驱动决策", "系统分析——在复杂问题中寻找最优方案", "责任承担——领导者必须为决策后果负责"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="麦克纳马拉", school="管理科学", problem=problem,
            perspective="从麦克纳马拉的系统分析智慧出发",
            core_insight="用数据和指标驱动决策",
            recommendations=[w.split("——")[1] if "——" in w else w for w in self._wisdom_laws],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.86,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["数据", "量化", "系统", "指标", "分析"]) else 0))
        return DecisionResult(sage_name="麦克纳马拉", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return "麦克纳马拉的智慧：量化管理——用数据和指标驱动决策"


class _AndrewGroveCloning(SageCloning):
    """安迪·格鲁夫 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="安迪·格鲁夫", name_en="Andrew Grove", era="20世纪", years="1936-2016",
            school="科技管理", tier=CloningTier.TIER2_CLUSTER,
            position="工部侍郎", department="工部",
            title="英特尔教父", biography="英特尔CEO，管理学名著《只有偏执狂才能生存》作者，推动英特尔成为全球最大芯片公司。",
            core_works=["《只有偏执狂才能生存》", "《高产出管理》"],
            capability={"strategic_vision": 10, "execution": 10, "innovation": 10, "leadership": 10, "influence": 9, "cross_domain": 8},
        ))
        self._wisdom_laws = ["战略转折点——识别行业的根本性变化时机", "偏执狂生存——只有时刻保持危机意识才能存活", "OKR管理——目标与关键结果的量化执行体系"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="安迪·格鲁夫", school="科技管理", problem=problem,
            perspective="从安迪·格鲁夫的英特尔教父智慧出发",
            core_insight="识别行业的根本性变化时机",
            recommendations=[w.split("——")[1] if "——" in w else w for w in self._wisdom_laws],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.89,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["危机", "转折", "执行", "目标", "大秦指标"]) else 0))
        return DecisionResult(sage_name="安迪·格鲁夫", problem=context.get("problem",""), chosen_option=chosen, confidence=0.86)

    def advise(self, context: Dict[str, Any]) -> str:
        return "安迪·格鲁夫的智慧：战略转折点——识别行业的根本性变化时机"


class _ClausewitzCloning(SageCloning):
    """克劳塞维茨 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="克劳塞维茨", name_en="Carl von Clausewitz", era="18-19世纪", years="1780-1831",
            school="战略学", tier=CloningTier.TIER2_CLUSTER,
            position="兵部侍郎", department="兵部",
            title="现代战略学之父", biography="普鲁士军事理论家，《战争论》作者，提出战争是政治的延续。",
            core_works=["《战争论》"],
            capability={"strategic_vision": 10, "execution": 8, "innovation": 10, "leadership": 9, "influence": 10, "cross_domain": 9},
        ))
        self._wisdom_laws = ["战争是政治的延续——战争从来不脱离政治目的", "战争迷雾——战场上信息永远是不完整的", "摩擦力——理论计划在实战中总会遇到阻碍"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="克劳塞维茨", school="战略学", problem=problem,
            perspective="从克劳塞维茨的战略学智慧出发",
            core_insight="战争从来不脱离政治目的",
            recommendations=[w.split("——")[1] if "——" in w else w for w in self._wisdom_laws],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.88,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["战略", "目的", "政治", "不确定", "摩擦"]) else 0))
        return DecisionResult(sage_name="克劳塞维茨", problem=context.get("problem",""), chosen_option=chosen, confidence=0.85)

    def advise(self, context: Dict[str, Any]) -> str:
        return "克劳塞维茨的智慧：战争是政治的延续——战争从来不脱离政治目的"


def build_cluster() -> SchoolCluster:
    """构建治理/战略集群"""
    return SchoolCluster(
        name="治理战略集群",
        school="治理与战略",
        department="吏部",
        leader_name="马基雅维利",
        members={
            "马基雅维利": _MachiavelliCloning(),
            "汉娜·阿伦特": _HannahArendtCloning(),
            "约翰·罗尔斯": _JohnRawlsCloning(),
            "麦克纳马拉": _RobertMcNamaraCloning(),
            "安迪·格鲁夫": _AndrewGroveCloning(),
            "克劳塞维茨": _ClausewitzCloning(),
        },
    )

__all__ = ['build_cluster']
