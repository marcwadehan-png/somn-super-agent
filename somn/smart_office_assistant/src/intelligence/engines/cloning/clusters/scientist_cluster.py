# -*- coding: utf-8 -*-
"""科技集群 Cloning - Tier 2 学派集群"""

from typing import Dict, List, Optional, Any
from .._cloning_base import SageCloning, SchoolCluster
from .._cloning_types import AnalysisResult, DecisionResult, SageProfile, CloningTier


class _ZuChongzhiCloning(SageCloning):
    """祖冲之Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="祖冲之", name_en="Zu Chongzhi", era="南北朝", years="429-500",
            school="科技", tier=CloningTier.TIER2_CLUSTER,
            position="工部主事", department="工部",
            title="数学泰斗", biography="南北朝数学家、天文学家，将圆周率精确到小数点后7位。",
            core_works=["《大明历》"],
            capability={"strategic_vision": 7, "execution": 9, "innovation": 10, "leadership": 5, "influence": 9, "cross_domain": 8},
        ))
        self._wisdom_laws = ["极致精确——追求计算的极限精度", "打破权威——质疑前人的结论", "数学建模——用数学描述自然规律"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="祖冲之", school="科技", problem=problem,
            perspective="从祖冲之的数学泰斗智慧出发",
            core_insight="追求计算的极限精度",
            recommendations=[["极致精确——追求计算的极限精度", "打破权威——质疑前人的结论", "数学建模——用数学描述自然规律"][i].split("——")[1] if "——" in ["极致精确——追求计算的极限精度", "打破权威——质疑前人的结论", "数学建模——用数学描述自然规律"][i] else ["极致精确——追求计算的极限精度", "打破权威——质疑前人的结论", "数学建模——用数学描述自然规律"][i] for i in range(len(["极致精确——追求计算的极限精度", "打破权威——质疑前人的结论", "数学建模——用数学描述自然规律"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["精确", "数学", "质疑", "建模"]) else 0))
        return DecisionResult(sage_name="祖冲之", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"祖冲之的智慧：极致精确——追求计算的极限精度"


class _ShenKuoCloning(SageCloning):
    """沈括Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="沈括", name_en="Shen Kuo", era="北宋", years="1031-1095",
            school="科技", tier=CloningTier.TIER2_CLUSTER,
            position="工部侍郎", department="工部",
            title="中国科学全才", biography="北宋科学家、政治家，《梦溪笔谈》作者。",
            core_works=["《梦溪笔谈》"],
            capability={"strategic_vision": 9, "execution": 8, "innovation": 10, "leadership": 7, "influence": 9, "cross_domain": 10},
        ))
        self._wisdom_laws = ["跨学科整合——天文地理物理化学无所不包", "实验验证——以实践检验理论", "系统记录——详尽记录观察和数据"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="沈括", school="科技", problem=problem,
            perspective="从沈括的中国科学全才智慧出发",
            core_insight="天文地理物理化学无所不包",
            recommendations=[["跨学科整合——天文地理物理化学无所不包", "实验验证——以实践检验理论", "系统记录——详尽记录观察和数据"][i].split("——")[1] if "——" in ["跨学科整合——天文地理物理化学无所不包", "实验验证——以实践检验理论", "系统记录——详尽记录观察和数据"][i] else ["跨学科整合——天文地理物理化学无所不包", "实验验证——以实践检验理论", "系统记录——详尽记录观察和数据"][i] for i in range(len(["跨学科整合——天文地理物理化学无所不包", "实验验证——以实践检验理论", "系统记录——详尽记录观察和数据"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["跨学科", "实验", "记录", "系统"]) else 0))
        return DecisionResult(sage_name="沈括", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"沈括的智慧：跨学科整合——天文地理物理化学无所不包"


class _GuoShoujingCloning(SageCloning):
    """郭守敬Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="郭守敬", name_en="Guo Shoujing", era="元代", years="1231-1316",
            school="科技", tier=CloningTier.TIER2_CLUSTER,
            position="工部主事", department="工部",
            title="天文大师", biography="元代天文学家、数学家、水利学家。",
            core_works=["《授时历》"],
            capability={"strategic_vision": 8, "execution": 10, "innovation": 9, "leadership": 7, "influence": 8, "cross_domain": 8},
        ))
        self._wisdom_laws = ["实测精神——亲自动手测量和验证", "精密仪器——发明制造天文仪器", "水利工程——理论与实践结合"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="郭守敬", school="科技", problem=problem,
            perspective="从郭守敬的天文大师智慧出发",
            core_insight="亲自动手测量和验证",
            recommendations=[["实测精神——亲自动手测量和验证", "精密仪器——发明制造天文仪器", "水利工程——理论与实践结合"][i].split("——")[1] if "——" in ["实测精神——亲自动手测量和验证", "精密仪器——发明制造天文仪器", "水利工程——理论与实践结合"][i] else ["实测精神——亲自动手测量和验证", "精密仪器——发明制造天文仪器", "水利工程——理论与实践结合"][i] for i in range(len(["实测精神——亲自动手测量和验证", "精密仪器——发明制造天文仪器", "水利工程——理论与实践结合"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["实测", "仪器", "水利", "精密"]) else 0))
        return DecisionResult(sage_name="郭守敬", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"郭守敬的智慧：实测精神——亲自动手测量和验证"


class _SongYingxingCloning(SageCloning):
    """宋应星Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="宋应星", name_en="Song Yingxing", era="明代", years="1587-1666",
            school="科技", tier=CloningTier.TIER2_CLUSTER,
            position="工部主事", department="工部",
            title="中国狄德罗", biography="明代科学家，《天工开物》作者。",
            core_works=["《天工开物》"],
            capability={"strategic_vision": 7, "execution": 8, "innovation": 8, "leadership": 5, "influence": 8, "cross_domain": 8},
        ))
        self._wisdom_laws = ["工艺百科——系统记录工农业生产技术", "实用主义——技术服务于生产", "工匠精神——尊重劳动和技术"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="宋应星", school="科技", problem=problem,
            perspective="从宋应星的中国狄德罗智慧出发",
            core_insight="系统记录工农业生产技术",
            recommendations=[["工艺百科——系统记录工农业生产技术", "实用主义——技术服务于生产", "工匠精神——尊重劳动和技术"][i].split("——")[1] if "——" in ["工艺百科——系统记录工农业生产技术", "实用主义——技术服务于生产", "工匠精神——尊重劳动和技术"][i] else ["工艺百科——系统记录工农业生产技术", "实用主义——技术服务于生产", "工匠精神——尊重劳动和技术"][i] for i in range(len(["工艺百科——系统记录工农业生产技术", "实用主义——技术服务于生产", "工匠精神——尊重劳动和技术"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["工艺", "实用", "技术", "生产"]) else 0))
        return DecisionResult(sage_name="宋应星", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"宋应星的智慧：工艺百科——系统记录工农业生产技术"


class _XuGuangqiCloning(SageCloning):
    """徐光启Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="徐光启", name_en="Xu Guangqi", era="明代", years="1562-1633",
            school="科技", tier=CloningTier.TIER2_CLUSTER,
            position="工部侍郎", department="工部",
            title="中西交流先驱", biography="明代科学家，翻译《几何原本》，引进西方科学。",
            core_works=["《农政全书》"],
            capability={"strategic_vision": 9, "execution": 8, "innovation": 9, "leadership": 8, "influence": 9, "cross_domain": 10},
        ))
        self._wisdom_laws = ["中西融合——引进消化西方先进知识", "实用科学——科学服务于农业和国防", "数学思维——用数学方法解决实际问题"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="徐光启", school="科技", problem=problem,
            perspective="从徐光启的中西交流先驱智慧出发",
            core_insight="引进消化西方先进知识",
            recommendations=[["中西融合——引进消化西方先进知识", "实用科学——科学服务于农业和国防", "数学思维——用数学方法解决实际问题"][i].split("——")[1] if "——" in ["中西融合——引进消化西方先进知识", "实用科学——科学服务于农业和国防", "数学思维——用数学方法解决实际问题"][i] else ["中西融合——引进消化西方先进知识", "实用科学——科学服务于农业和国防", "数学思维——用数学方法解决实际问题"][i] for i in range(len(["中西融合——引进消化西方先进知识", "实用科学——科学服务于农业和国防", "数学思维——用数学方法解决实际问题"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["中西融合", "数学", "农业", "引进"]) else 0))
        return DecisionResult(sage_name="徐光启", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"徐光启的智慧：中西融合——引进消化西方先进知识"


def build_cluster() -> SchoolCluster:
    """构建科技集群"""
    return SchoolCluster(
        name="科技集群",
        school="科技",
        department="工部",
        leader_name="张衡",
        members={
        "祖冲之": _ZuChongzhiCloning(),
        "沈括": _ShenKuoCloning(),
        "郭守敬": _GuoShoujingCloning(),
        "宋应星": _SongYingxingCloning(),
        "徐光启": _XuGuangqiCloning(),
        },
    )
__all__ = ['build_cluster']
