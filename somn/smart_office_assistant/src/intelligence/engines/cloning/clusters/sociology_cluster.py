# -*- coding: utf-8 -*-
"""社会学集群 Cloning - Tier 2 学派集群"""

from typing import Dict, List, Optional, Any
from .._cloning_base import SageCloning, SchoolCluster
from .._cloning_types import AnalysisResult, DecisionResult, SageProfile, CloningTier


class _EmileDurkheimCloning(SageCloning):
    """涂尔干 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="涂尔干", name_en="Emile Durkheim", era="19-20世纪", years="1858-1917",
            school="社会学", tier=CloningTier.TIER2_CLUSTER,
            position="礼部侍郎", department="礼部",
            title="社会学之父", biography="法国社会学家，现代社会学奠基人，提出社会事实概念。",
            core_works=["《社会分工论》", "《自杀论》"],
            capability={"strategic_vision": 9, "execution": 7, "innovation": 10, "leadership": 7, "influence": 10, "cross_domain": 8},
        ))
        self._wisdom_laws = ["社会事实——独立于个人意志的社会现象", "社会分工——劳动分工促进社会团结", "集体意识——社会共有的信仰和情感"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="涂尔干", school="社会学", problem=problem,
            perspective="从涂尔干的社会学之父智慧出发",
            core_insight="独立于个人意志的社会现象",
            recommendations=[["社会事实——独立于个人意志的社会现象", "社会分工——劳动分工促进社会团结", "集体意识——社会共有的信仰和情感"][i].split("——")[1] if "——" in ["社会事实——独立于个人意志的社会现象", "社会分工——劳动分工促进社会团结", "集体意识——社会共有的信仰和情感"][i] else ["社会事实——独立于个人意志的社会现象", "社会分工——劳动分工促进社会团结", "集体意识——社会共有的信仰和情感"][i] for i in range(len(["社会事实——独立于个人意志的社会现象", "社会分工——劳动分工促进社会团结", "集体意识——社会共有的信仰和情感"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.88,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["社会", "集体", "分工", "规范", "道德"]) else 0))
        return DecisionResult(sage_name="涂尔干", problem=context.get("problem",""), chosen_option=chosen, confidence=0.84)

    def advise(self, context: Dict[str, Any]) -> str:
        return "涂尔干的智慧：社会事实——独立于个人意志的社会现象"


class _MaxWeberCloning(SageCloning):
    """韦伯 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="韦伯", name_en="Max Weber", era="19-20世纪", years="1864-1920",
            school="社会学", tier=CloningTier.TIER2_CLUSTER,
            position="礼部尚书", department="礼部",
            title="理解社会学之父", biography="德国社会学家，理解社会学、经济社会学、公共行政学的奠基人。",
            core_works=["《新教伦理与资本主义精神》", "《经济与社会》"],
            capability={"strategic_vision": 10, "execution": 6, "innovation": 10, "leadership": 7, "influence": 10, "cross_domain": 10},
        ))
        self._wisdom_laws = ["理解社会学——从行动者视角理解社会行为", "理性化铁笼——现代社会的理性化趋势", "合法性类型——传统型/卡里斯玛型/法理型"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="韦伯", school="社会学", problem=problem,
            perspective="从韦伯的理解社会学智慧出发",
            core_insight="从行动者视角理解社会行为",
            recommendations=[["理解社会学——从行动者视角理解社会行为", "理性化铁笼——现代社会的理性化趋势", "合法性类型——传统型/卡里斯玛型/法理型"][i].split("——")[1] if "——" in ["理解社会学——从行动者视角理解社会行为", "理性化铁笼——现代社会的理性化趋势", "合法性类型——传统型/卡里斯玛型/法理型"][i] else ["理解社会学——从行动者视角理解社会行为", "理性化铁笼——现代社会的理性化趋势", "合法性类型——传统型/卡里斯玛型/法理型"][i] for i in range(len(["理解社会学——从行动者视角理解社会行为", "理性化铁笼——现代社会的理性化趋势", "合法性类型——传统型/卡里斯玛型/法理型"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.88,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["理性", "理解", "合法性", "权威", "组织"]) else 0))
        return DecisionResult(sage_name="韦伯", problem=context.get("problem",""), chosen_option=chosen, confidence=0.84)

    def advise(self, context: Dict[str, Any]) -> str:
        return "韦伯的智慧：理解社会学——从行动者视角理解社会行为"


class _PierreBourdieuCloning(SageCloning):
    """布迪厄 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="布迪厄", name_en="Pierre Bourdieu", era="20世纪", years="1930-2002",
            school="文化社会学", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="礼部",
            title="文化资本理论之父", biography="法国社会学家，提出文化资本、场域、惯习等核心概念。",
            core_works=["《区隔》", "《再生产》"],
            capability={"strategic_vision": 9, "execution": 6, "innovation": 10, "leadership": 6, "influence": 9, "cross_domain": 9},
        ))
        self._wisdom_laws = ["文化资本——教育是阶层再生产的工具", "场域——社会空间中的相对位置", "惯习——内化于身体的阶层习性"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="布迪厄", school="文化社会学", problem=problem,
            perspective="从布迪厄的文化资本智慧出发",
            core_insight="教育是阶层再生产的工具",
            recommendations=[["文化资本——教育是阶层再生产的工具", "场域——社会空间中的相对位置", "惯习——内化于身体的阶层习性"][i].split("——")[1] if "——" in ["文化资本——教育是阶层再生产的工具", "场域——社会空间中的相对位置", "惯习——内化于身体的阶层习性"][i] else ["文化资本——教育是阶层再生产的工具", "场域——社会空间中的相对位置", "惯习——内化于身体的阶层习性"][i] for i in range(len(["文化资本——教育是阶层再生产的工具", "场域——社会空间中的相对位置", "惯习——内化于身体的阶层习性"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.87,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["文化", "阶层", "教育", "资本", "场域"]) else 0))
        return DecisionResult(sage_name="布迪厄", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return "布迪厄的智慧：文化资本——教育是阶层再生产的工具"


class _MichelFoucaultCloning(SageCloning):
    """福柯 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="福柯", name_en="Michel Foucault", era="20世纪", years="1926-1984",
            school="后现代社会学", tier=CloningTier.TIER2_CLUSTER,
            position="礼部侍郎", department="礼部",
            title="权力/知识理论大师", biography="法国哲学家、社会理论家，研究权力、知识与身体的关系。",
            core_works=["《规训与惩罚》", "《性经验史》"],
            capability={"strategic_vision": 10, "execution": 5, "innovation": 10, "leadership": 6, "influence": 10, "cross_domain": 10},
        ))
        self._wisdom_laws = ["权力/知识——权力产生知识，知识服务权力", "全景敞视监狱——现代社会的监控机制", "话语即权力——谁掌握话语谁掌握权力"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="福柯", school="后现代社会学", problem=problem,
            perspective="从福柯的权力/知识智慧出发",
            core_insight="权力产生知识，知识服务权力",
            recommendations=[["权力/知识——权力产生知识，知识服务权力", "全景敞视监狱——现代社会的监控机制", "话语即权力——谁掌握话语谁掌握权力"][i].split("——")[1] if "——" in ["权力/知识——权力产生知识，知识服务权力", "全景敞视监狱——现代社会的监控机制", "话语即权力——谁掌握话语谁掌握权力"][i] else ["权力/知识——权力产生知识，知识服务权力", "全景敞视监狱——现代社会的监控机制", "话语即权力——谁掌握话语谁掌握权力"][i] for i in range(len(["权力/知识——权力产生知识，知识服务权力", "全景敞视监狱——现代社会的监控机制", "话语即权力——谁掌握话语谁掌握权力"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.87,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["权力", "话语", "监控", "知识", "制度"]) else 0))
        return DecisionResult(sage_name="福柯", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return "福柯的智慧：权力/知识——权力产生知识，知识服务权力"


class _AnthonyGiddensCloning(SageCloning):
    """吉登斯 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="吉登斯", name_en="Anthony Giddens", era="20-21世纪", years="1938-",
            school="结构化理论", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="礼部",
            title="结构化理论之父", biography="英国社会学家，提出结构化理论，沟通宏观与微观社会学。",
            core_works=["《社会的构成》", "《现代性的后果》"],
            capability={"strategic_vision": 9, "execution": 6, "innovation": 9, "leadership": 7, "influence": 8, "cross_domain": 9},
        ))
        self._wisdom_laws = ["结构化理论——结构与行动互构", "现代性反思性——现代社会的人不断反思自身", "时空伸延——全球化压缩时空"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="吉登斯", school="结构化理论", problem=problem,
            perspective="从吉登斯的结构化理论智慧出发",
            core_insight="结构与行动互构",
            recommendations=[["结构化理论——结构与行动互构", "现代性反思性——现代社会的人不断反思自身", "时空伸延——全球化压缩时空"][i].split("——")[1] if "——" in ["结构化理论——结构与行动互构", "现代性反思性——现代社会的人不断反思自身", "时空伸延——全球化压缩时空"][i] else ["结构化理论——结构与行动互构", "现代性反思性——现代社会的人不断反思自身", "时空伸延——全球化压缩时空"][i] for i in range(len(["结构化理论——结构与行动互构", "现代性反思性——现代社会的人不断反思自身", "时空伸延——全球化压缩时空"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.86,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["结构", "现代性", "全球化", "反思", "行动"]) else 0))
        return DecisionResult(sage_name="吉登斯", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return "吉登斯的智慧：结构化理论——结构与行动互构"


class _CWrightMillsCloning(SageCloning):
    """米尔斯 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="C·赖特·米尔斯", name_en="C. Wright Mills", era="20世纪", years="1916-1962",
            school="批判社会学", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="礼部",
            title="社会学想象力", biography="美国社会学家，提出\"社会学想象力\"概念，批判权力精英。",
            core_works=["《社会学的想象力》", "《权力精英》"],
            capability={"strategic_vision": 9, "execution": 5, "innovation": 9, "leadership": 7, "influence": 8, "cross_domain": 7},
        ))
        self._wisdom_laws = ["社会学想象力——将个人困扰转化为公共议题", "权力精英——政治经济军事构成权力核心", "宏大理论——抽象概念要扎根经验"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="C·赖特·米尔斯", school="批判社会学", problem=problem,
            perspective="从米尔斯的批判社会学智慧出发",
            core_insight="将个人困扰转化为公共议题",
            recommendations=[["社会学想象力——将个人困扰转化为公共议题", "权力精英——政治经济军事构成权力核心", "宏大理论——抽象概念要扎根经验"][i].split("——")[1] if "——" in ["社会学想象力——将个人困扰转化为公共议题", "权力精英——政治经济军事构成权力核心", "宏大理论——抽象概念要扎根经验"][i] else ["社会学想象力——将个人困扰转化为公共议题", "权力精英——政治经济军事构成权力核心", "宏大理论——抽象概念要扎根经验"][i] for i in range(len(["社会学想象力——将个人困扰转化为公共议题", "权力精英——政治经济军事构成权力核心", "宏大理论——抽象概念要扎根经验"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.86,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["批判", "权力", "公共", "个人", "想象"]) else 0))
        return DecisionResult(sage_name="C·赖特·米尔斯", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return "米尔斯的智慧：社会学想象力——将个人困扰转化为公共议题"


class _CharlesTaylorCloning(SageCloning):
    """查尔斯·泰勒 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="查尔斯·泰勒", name_en="Charles Taylor", era="20-21世纪", years="1931-",
            school="政治哲学", tier=CloningTier.TIER2_CLUSTER,
            position="吏部侍郎", department="吏部",
            title="承认政治大师", biography="加拿大哲学家，研究认同、承认与现代身份政治。",
            core_works=["《自我的根源》", "《承认的政治》"],
            capability={"strategic_vision": 9, "execution": 5, "innovation": 9, "leadership": 6, "influence": 8, "cross_domain": 8},
        ))
        self._wisdom_laws = ["承认的政治——身份认同需要社会认可", "本真性理想——忠于自我是道德理想", "对话式自我——自我在对话中形成"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="查尔斯·泰勒", school="政治哲学", problem=problem,
            perspective="从泰勒的承认政治智慧出发",
            core_insight="身份认同需要社会认可",
            recommendations=[["承认的政治——身份认同需要社会认可", "本真性理想——忠于自我是道德理想", "对话式自我——自我在对话中形成"][i].split("——")[1] if "——" in ["承认的政治——身份认同需要社会认可", "本真性理想——忠于自我是道德理想", "对话式自我——自我在对话中形成"][i] else ["承认的政治——身份认同需要社会认可", "本真性理想——忠于自我是道德理想", "对话式自我——自我在对话中形成"][i] for i in range(len(["承认的政治——身份认同需要社会认可", "本真性理想——忠于自我是道德理想", "对话式自我——自我在对话中形成"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["认同", "承认", "身份", "文化", "多元"]) else 0))
        return DecisionResult(sage_name="查尔斯·泰勒", problem=context.get("problem",""), chosen_option=chosen, confidence=0.82)

    def advise(self, context: Dict[str, Any]) -> str:
        return "查尔斯·泰勒的智慧：承认的政治——身份认同需要社会认可"


class _JürgenHabermasCloning(SageCloning):
    """哈贝马斯 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="哈贝马斯", name_en="Jürgen Habermas", era="20-21世纪", years="1929-",
            school="公共领域理论", tier=CloningTier.TIER2_CLUSTER,
            position="礼部尚书", department="礼部",
            title="公共领域理论之父", biography="德国哲学家、社会学家，提出公共领域、交往行动理论。",
            core_works=["《公共领域的结构转型》", "《交往行为理论》"],
            capability={"strategic_vision": 10, "execution": 5, "innovation": 10, "leadership": 6, "influence": 10, "cross_domain": 9},
        ))
        self._wisdom_laws = ["公共领域——公民自由讨论形成公共意见", "交往理性——通过对话达成共识", "生活世界殖民化——系统入侵生活世界"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="哈贝马斯", school="公共领域理论", problem=problem,
            perspective="从哈贝马斯的交往理性智慧出发",
            core_insight="通过对话达成共识",
            recommendations=[["公共领域——公民自由讨论形成公共意见", "交往理性——通过对话达成共识", "生活世界殖民化——系统入侵生活世界"][i].split("——")[1] if "——" in ["公共领域——公民自由讨论形成公共意见", "交往理性——通过对话达成共识", "生活世界殖民化——系统入侵生活世界"][i] else ["公共领域——公民自由讨论形成公共意见", "交往理性——通过对话达成共识", "生活世界殖民化——系统入侵生活世界"][i] for i in range(len(["公共领域——公民自由讨论形成公共意见", "交往理性——通过对话达成共识", "生活世界殖民化——系统入侵生活世界"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.87,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["公共", "对话", "共识", "沟通", "理性"]) else 0))
        return DecisionResult(sage_name="哈贝马斯", problem=context.get("problem",""), chosen_option=chosen, confidence=0.84)

    def advise(self, context: Dict[str, Any]) -> str:
        return "哈贝马斯的智慧：交往理性——通过对话达成共识"


class _GeorgSimmelCloning(SageCloning):
    """齐美尔 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="齐美尔", name_en="Georg Simmel", era="19-20世纪", years="1858-1918",
            school="形式社会学", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="礼部",
            title="形式社会学之父", biography="德国社会学家，研究社会化的形式，关注货币与现代社会。",
            core_works=["《货币哲学》", "《社会学》"],
            capability={"strategic_vision": 9, "execution": 5, "innovation": 10, "leadership": 5, "influence": 8, "cross_domain": 9},
        ))
        self._wisdom_laws = ["货币哲学——货币改变人与人的关系", "社会化的形式——研究社会互动的结构", "文化悲剧——客观文化压倒主观文化"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="齐美尔", school="形式社会学", problem=problem,
            perspective="从齐美尔的形式社会学智慧出发",
            core_insight="货币改变人与人的关系",
            recommendations=[["货币哲学——货币改变人与人的关系", "社会化的形式——研究社会互动的结构", "文化悲剧——客观文化压倒主观文化"][i].split("——")[1] if "——" in ["货币哲学——货币改变人与人的关系", "社会化的形式——研究社会互动的结构", "文化悲剧——客观文化压倒主观文化"][i] else ["货币哲学——货币改变人与人的关系", "社会化的形式——研究社会互动的结构", "文化悲剧——客观文化压倒主观文化"][i] for i in range(len(["货币哲学——货币改变人与人的关系", "社会化的形式——研究社会互动的结构", "文化悲剧——客观文化压倒主观文化"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.86,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["货币", "形式", "文化", "互动", "现代性"]) else 0))
        return DecisionResult(sage_name="齐美尔", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return "齐美尔的智慧：货币哲学——货币改变人与人的关系"


class _RobertMertonCloning(SageCloning):
    """默顿 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="默顿", name_en="Robert K. Merton", era="20世纪", years="1910-2003",
            school="知识社会学", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="礼部",
            title="功能主义大师", biography="美国社会学家，发展了帕森斯功能主义，提出自我实现预言。",
            core_works=["《社会理论与社会结构》"],
            capability={"strategic_vision": 9, "execution": 7, "innovation": 9, "leadership": 7, "influence": 9, "cross_domain": 8},
        ))
        self._wisdom_laws = ["功能分析——社会事项都有正负功能", "自我实现预言——信念驱动结果", "中层理论——社会学理论应介于宏大理论与经验研究之间"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="默顿", school="知识社会学", problem=problem,
            perspective="从默顿的功能分析智慧出发",
            core_insight="社会事项都有正负功能",
            recommendations=[["功能分析——社会事项都有正负功能", "自我实现预言——信念驱动结果", "中层理论——社会学理论应介于宏大理论与经验研究之间"][i].split("——")[1] if "——" in ["功能分析——社会事项都有正负功能", "自我实现预言——信念驱动结果", "中层理论——社会学理论应介于宏大理论与经验研究之间"][i] else ["功能分析——社会事项都有正负功能", "自我实现预言——信念驱动结果", "中层理论——社会学理论应介于宏大理论与经验研究之间"][i] for i in range(len(["功能分析——社会事项都有正负功能", "自我实现预言——信念驱动结果", "中层理论——社会学理论应介于宏大理论与经验研究之间"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.86,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["功能", "预言", "理论", "结构", "偏差"]) else 0))
        return DecisionResult(sage_name="默顿", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return "默顿的智慧：功能分析——社会事项都有正负功能"


def build_cluster() -> SchoolCluster:
    """构建社会学集群"""
    return SchoolCluster(
        name="社会学集群",
        school="社会学",
        department="礼部",
        leader_name="涂尔干",
        members={
            "涂尔干": _EmileDurkheimCloning(),
            "韦伯": _MaxWeberCloning(),
            "布迪厄": _PierreBourdieuCloning(),
            "福柯": _MichelFoucaultCloning(),
            "吉登斯": _AnthonyGiddensCloning(),
            "米尔斯": _CWrightMillsCloning(),
            "查尔斯·泰勒": _CharlesTaylorCloning(),
            "哈贝马斯": _JürgenHabermasCloning(),
            "齐美尔": _GeorgSimmelCloning(),
            "默顿": _RobertMertonCloning(),
        },
    )
__all__ = ['build_cluster']
