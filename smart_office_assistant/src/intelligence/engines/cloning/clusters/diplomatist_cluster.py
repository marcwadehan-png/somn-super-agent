# -*- coding: utf-8 -*-
"""纵横家集群 Cloning - Tier 2 学派集群"""

from typing import Dict, List, Optional, Any
from .._cloning_base import SageCloning, SchoolCluster
from .._cloning_types import AnalysisResult, DecisionResult, SageProfile, CloningTier


class _SuQinCloning(SageCloning):
    """苏秦Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="苏秦", name_en="Su Qin", era="战国中期", years="前380-前284",
            school="纵横家", tier=CloningTier.TIER2_CLUSTER,
            position="兵部主事", department="厂卫",
            title="合纵家", biography="战国纵横家，以'合纵'策略联合六国抗秦。",
            core_works=["《苏子》"],
            capability={"strategic_vision": 9, "execution": 8, "innovation": 8, "leadership": 8, "influence": 9, "cross_domain": 7},
        ))
        self._wisdom_laws = ["合纵——联合弱者对抗强者", "口舌之劳——言语的力量超越刀剑", "时势造英雄——把握历史机遇"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="苏秦", school="纵横家", problem=problem,
            perspective="从苏秦的合纵家智慧出发",
            core_insight="联合弱者对抗强者",
            recommendations=[["合纵——联合弱者对抗强者", "口舌之劳——言语的力量超越刀剑", "时势造英雄——把握历史机遇"][i].split("——")[1] if "——" in ["合纵——联合弱者对抗强者", "口舌之劳——言语的力量超越刀剑", "时势造英雄——把握历史机遇"][i] else ["合纵——联合弱者对抗强者", "口舌之劳——言语的力量超越刀剑", "时势造英雄——把握历史机遇"][i] for i in range(len(["合纵——联合弱者对抗强者", "口舌之劳——言语的力量超越刀剑", "时势造英雄——把握历史机遇"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["联盟", "合作", "时机", "说服"]) else 0))
        return DecisionResult(sage_name="苏秦", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"苏秦的智慧：合纵——联合弱者对抗强者"


class _ZhangYiCloning(SageCloning):
    """张仪Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="张仪", name_en="Zhang Yi", era="战国中期", years="前378-前309",
            school="纵横家", tier=CloningTier.TIER2_CLUSTER,
            position="厂卫主事", department="厂卫",
            title="连横家", biography="战国纵横家，以'连横'策略分化六国。",
            core_works=[],
            capability={"strategic_vision": 9, "execution": 9, "innovation": 7, "leadership": 8, "influence": 8, "cross_domain": 7},
        ))
        self._wisdom_laws = ["连横——分化瓦解对手联盟", "利诱——以利益驱使对方决策", "因势利导——根据形势灵活变化"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="张仪", school="纵横家", problem=problem,
            perspective="从张仪的连横家智慧出发",
            core_insight="分化瓦解对手联盟",
            recommendations=[["连横——分化瓦解对手联盟", "利诱——以利益驱使对方决策", "因势利导——根据形势灵活变化"][i].split("——")[1] if "——" in ["连横——分化瓦解对手联盟", "利诱——以利益驱使对方决策", "因势利导——根据形势灵活变化"][i] else ["连横——分化瓦解对手联盟", "利诱——以利益驱使对方决策", "因势利导——根据形势灵活变化"][i] for i in range(len(["连横——分化瓦解对手联盟", "利诱——以利益驱使对方决策", "因势利导——根据形势灵活变化"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["分化", "利诱", "灵活", "策略"]) else 0))
        return DecisionResult(sage_name="张仪", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"张仪的智慧：连横——分化瓦解对手联盟"


class _ChenPingCloning(SageCloning):
    """陈平Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="陈平", name_en="Chen Ping", era="秦末汉初", years="前?-前178",
            school="纵横家", tier=CloningTier.TIER2_CLUSTER,
            position="内阁主事", department="厂卫",
            title="六出奇计", biography="汉初谋士，以'六出奇计'辅佐刘邦。",
            core_works=[],
            capability={"strategic_vision": 9, "execution": 8, "innovation": 9, "leadership": 7, "influence": 7, "cross_domain": 6},
        ))
        self._wisdom_laws = ["奇计——非常规手段解决关键问题", "反间——利用信息不对称分化敌人", "知人善任——看人极准"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="陈平", school="纵横家", problem=problem,
            perspective="从陈平的六出奇计智慧出发",
            core_insight="非常规手段解决关键问题",
            recommendations=[["奇计——非常规手段解决关键问题", "反间——利用信息不对称分化敌人", "知人善任——看人极准"][i].split("——")[1] if "——" in ["奇计——非常规手段解决关键问题", "反间——利用信息不对称分化敌人", "知人善任——看人极准"][i] else ["奇计——非常规手段解决关键问题", "反间——利用信息不对称分化敌人", "知人善任——看人极准"][i] for i in range(len(["奇计——非常规手段解决关键问题", "反间——利用信息不对称分化敌人", "知人善任——看人极准"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["奇计", "情报", "用人", "反间"]) else 0))
        return DecisionResult(sage_name="陈平", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"陈平的智慧：奇计——非常规手段解决关键问题"


class _FanJuCloning(SageCloning):
    """范雎Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="范雎", name_en="Fan Ju", era="战国", years="前338-前255",
            school="纵横家", tier=CloningTier.TIER2_CLUSTER,
            position="内阁首辅", department="厂卫",
            title="远交近攻", biography="战国魏人，入秦为相，提出'远交近攻'战略，辅佐秦昭王。",
            core_works=["《远交近攻策》"],
            capability={"strategic_vision": 9, "execution": 8, "innovation": 8, "leadership": 7, "influence": 8, "cross_domain": 7},
        ))
        self._wisdom_laws = ["远交近攻——距离远则联合，距离近则攻伐", "隐忍待机——在魏受辱时隐忍不发", "战略优先——先定长远战略再定战术"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="范雎", school="纵横家", problem=problem,
            perspective="从范雎的远交近攻智慧出发",
            core_insight="距离远则联合，距离近则攻伐",
            recommendations=[["远交近攻——距离远则联合，距离近则攻伐", "隐忍待机——在魏受辱时隐忍不发", "战略优先——先定长远战略再定战术"][i].split("——")[1] if "——" in ["远交近攻——距离远则联合，距离近则攻伐", "隐忍待机——在魏受辱时隐忍不发", "战略优先——先定长远战略再定战术"][i] else ["远交近攻——距离远则联合，距离近则攻伐", "隐忍待机——在魏受辱时隐忍不发", "战略优先——先定长远战略再定战术"][i] for i in range(len(["远交近攻——距离远则联合，距离近则攻伐", "隐忍待机——在魏受辱时隐忍不发", "战略优先——先定长远战略再定战术"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["战略", "远交", "隐忍", "优先"]) else 0))
        return DecisionResult(sage_name="范雎", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"范雎的智慧：远交近攻——距离远则联合，距离近则攻伐"


class _CaiZeCloning(SageCloning):
    """蔡泽Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="蔡泽", name_en="Cai Ze", era="战国", years="战国燕人",
            school="纵横家", tier=CloningTier.TIER2_CLUSTER,
            position="厂卫主事", department="厂卫",
            title="功成身退", biography="战国燕人，入秦为相，以历史教训劝范雎功成身退。",
            core_works=[],
            capability={"strategic_vision": 7, "execution": 7, "innovation": 7, "leadership": 7, "influence": 6, "cross_domain": 8},
        ))
        self._wisdom_laws = ["功成身退——成功之后及时隐退", "以史为鉴——用历史人物命运说服君主", "时机把握——知道何时该进何时该退"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="蔡泽", school="纵横家", problem=problem,
            perspective="从蔡泽的功成身退智慧出发",
            core_insight="成功之后及时隐退",
            recommendations=[["功成身退——成功之后及时隐退", "以史为鉴——用历史人物命运说服君主", "时机把握——知道何时该进何时该退"][i].split("——")[1] if "——" in ["功成身退——成功之后及时隐退", "以史为鉴——用历史人物命运说服君主", "时机把握——知道何时该进何时该退"][i] else ["功成身退——成功之后及时隐退", "以史为鉴——用历史人物命运说服君主", "时机把握——知道何时该进何时该退"][i] for i in range(len(["功成身退——成功之后及时隐退", "以史为鉴——用历史人物命运说服君主", "时机把握——知道何时该进何时该退"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.82,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["退", "时机", "历史", "身退"]) else 0))
        return DecisionResult(sage_name="蔡泽", problem=context.get("problem",""), chosen_option=chosen, confidence=0.81)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"蔡泽的智慧：功成身退——成功之后及时隐退"


class _GongsunYanCloning(SageCloning):
    """公孙衍Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="公孙衍", name_en="Gongsun Yan", era="战国", years="战国魏人",
            school="纵横家", tier=CloningTier.TIER2_CLUSTER,
            position="兵部主事", department="厂卫",
            title="五国相印", biography="战国魏人，著名纵横家，曾佩五国相印，合纵抗秦。",
            core_works=[],
            capability={"strategic_vision": 7, "execution": 7, "innovation": 6, "leadership": 7, "influence": 7, "cross_domain": 6},
        ))
        self._wisdom_laws = ["合纵抗秦——联合六国对抗强秦", "灵活立场——根据形势调整策略", "利益至上——立场灵活但利益必须坚守"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="公孙衍", school="纵横家", problem=problem,
            perspective="从公孙衍的合纵抗秦智慧出发",
            core_insight="联合六国对抗强秦",
            recommendations=[["合纵抗秦——联合六国对抗强秦", "灵活立场——根据形势调整策略", "利益至上——立场灵活但利益必须坚守"][i].split("——")[1] if "——" in ["合纵抗秦——联合六国对抗强秦", "灵活立场——根据形势调整策略", "利益至上——立场灵活但利益必须坚守"][i] else ["合纵抗秦——联合六国对抗强秦", "灵活立场——根据形势调整策略", "利益至上——立场灵活但利益必须坚守"][i] for i in range(len(["合纵抗秦——联合六国对抗强秦", "灵活立场——根据形势调整策略", "利益至上——立场灵活但利益必须坚守"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.82,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["联合", "灵活", "利益", "合纵"]) else 0))
        return DecisionResult(sage_name="公孙衍", problem=context.get("problem",""), chosen_option=chosen, confidence=0.81)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"公孙衍的智慧：合纵抗秦——联合六国对抗强秦"


class _GanMaoCloning(SageCloning):
    """甘茂Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="甘茂", name_en="Gan Mao", era="战国", years="战国楚人",
            school="纵横家", tier=CloningTier.TIER2_CLUSTER,
            position="兵部主事", department="兵部",
            title="文武双全", biography="战国楚人，在秦为将相，文武双全的纵横家。",
            core_works=[],
            capability={"strategic_vision": 7, "execution": 8, "innovation": 6, "leadership": 7, "influence": 6, "cross_domain": 6},
        ))
        self._wisdom_laws = ["以攻代守——主动进攻是最好的防守", "将相和合——军事与政治必须配合", "攻韩要地——集中优势资源突破关键方向"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="甘茂", school="纵横家", problem=problem,
            perspective="从甘茂的以攻代守智慧出发",
            core_insight="主动进攻是最好的防守",
            recommendations=[["以攻代守——主动进攻是最好的防守", "将相和合——军事与政治必须配合", "攻韩要地——集中优势资源突破关键方向"][i].split("——")[1] if "——" in ["以攻代守——主动进攻是最好的防守", "将相和合——军事与政治必须配合", "攻韩要地——集中优势资源突破关键方向"][i] else ["以攻代守——主动进攻是最好的防守", "将相和合——军事与政治必须配合", "攻韩要地——集中优势资源突破关键方向"][i] for i in range(len(["以攻代守——主动进攻是最好的防守", "将相和合——军事与政治必须配合", "攻韩要地——集中优势资源突破关键方向"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.82,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["进攻", "主动", "配合", "集中"]) else 0))
        return DecisionResult(sage_name="甘茂", problem=context.get("problem",""), chosen_option=chosen, confidence=0.81)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"甘茂的智慧：以攻代守——主动进攻是最好的防守"


class _LvBuweiCloning(SageCloning):
    """吕不韦Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="吕不韦", name_en="Lv Buwei", era="战国", years="前292-前235",
            school="纵横家", tier=CloningTier.TIER2_CLUSTER,
            position="内阁首辅", department="内阁",
            title="奇货可居", biography="战国末年卫人，最成功商人从政案例，将异人扶上王位，主持编纂《吕氏春秋》。",
            core_works=["《吕氏春秋》"],
            capability={"strategic_vision": 9, "execution": 8, "innovation": 8, "leadership": 8, "influence": 8, "cross_domain": 8},
        ))
        self._wisdom_laws = ["奇货可居——发现潜力股并长期投资", "长线投资——十几年战略投资而非短期回报", "兼收并蓄——杂家思想不拘一家博采众长"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="吕不韦", school="纵横家", problem=problem,
            perspective="从吕不韦的奇货可居智慧出发",
            core_insight="发现潜力股并长期投资",
            recommendations=[["奇货可居——发现潜力股并长期投资", "长线投资——十几年战略投资而非短期回报", "兼收并蓄——杂家思想不拘一家博采众长"][i].split("——")[1] if "——" in ["奇货可居——发现潜力股并长期投资", "长线投资——十几年战略投资而非短期回报", "兼收并蓄——杂家思想不拘一家博采众长"][i] else ["奇货可居——发现潜力股并长期投资", "长线投资——十几年战略投资而非短期回报", "兼收并蓄——杂家思想不拘一家博采众长"][i] for i in range(len(["奇货可居——发现潜力股并长期投资", "长线投资——十几年战略投资而非短期回报", "兼收并蓄——杂家思想不拘一家博采众长"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["投资", "潜力", "长期", "战略"]) else 0))
        return DecisionResult(sage_name="吕不韦", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"吕不韦的智慧：奇货可居——发现潜力股并长期投资"


class _LiSiCloning(SageCloning):
    """李斯Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="李斯", name_en="Li Si", era="战国-秦", years="前284-前208",
            school="纵横家", tier=CloningTier.TIER2_CLUSTER,
            position="内阁首辅", department="内阁",
            title="郡县制", biography="楚国上蔡人，秦朝丞相，助秦始皇统一六国，推行郡县制、统一文字度量衡。",
            core_works=["《谏逐客书》"],
            capability={"strategic_vision": 9, "execution": 9, "innovation": 9, "leadership": 8, "influence": 10, "cross_domain": 7},
        ))
        self._wisdom_laws = ["郡县制度——废除分封建立中央集权", "统一标准——文字度量衡车轨实现文化整合", "老鼠哲学——人生际遇取决于所处环境和位置"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="李斯", school="纵横家", problem=problem,
            perspective="从李斯的郡县制智慧出发",
            core_insight="废除分封建立中央集权",
            recommendations=[["郡县制度——废除分封建立中央集权", "统一标准——文字度量衡车轨实现文化整合", "老鼠哲学——人生际遇取决于所处环境和位置"][i].split("——")[1] if "——" in ["郡县制度——废除分封建立中央集权", "统一标准——文字度量衡车轨实现文化整合", "老鼠哲学——人生际遇取决于所处环境和位置"][i] else ["郡县制度——废除分封建立中央集权", "统一标准——文字度量衡车轨实现文化整合", "老鼠哲学——人生际遇取决于所处环境和位置"][i] for i in range(len(["郡县制度——废除分封建立中央集权", "统一标准——文字度量衡车轨实现文化整合", "老鼠哲学——人生际遇取决于所处环境和位置"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["统一", "集权", "制度", "标准"]) else 0))
        return DecisionResult(sage_name="李斯", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"李斯的智慧：郡县制度——废除分封建立中央集权"


class _KuaiTongCloning(SageCloning):
    """蒯通Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="蒯通", name_en="Kuai Tong", era="战国末-汉初", years="战国末至汉初",
            school="纵横家", tier=CloningTier.TIER2_CLUSTER,
            position="厂卫主事", department="厂卫",
            title="审时度势", biography="战国末期至汉初著名说客，曾劝韩信三分天下，典型纵横家。",
            core_works=[],
            capability={"strategic_vision": 8, "execution": 7, "innovation": 7, "leadership": 6, "influence": 6, "cross_domain": 7},
        ))
        self._wisdom_laws = ["审时度势——准确判断形势把握最佳时机", "时势造英雄——时机重要但创造时机更重要", "错过时机就错过一切——机会稍纵即逝"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="蒯通", school="纵横家", problem=problem,
            perspective="从蒯通的审时度势智慧出发",
            core_insight="准确判断形势把握最佳时机",
            recommendations=[["审时度势——准确判断形势把握最佳时机", "时势造英雄——时机重要但创造时机更重要", "错过时机就错过一切——机会稍纵即逝"][i].split("——")[1] if "——" in ["审时度势——准确判断形势把握最佳时机", "时势造英雄——时机重要但创造时机更重要", "错过时机就错过一切——机会稍纵即逝"][i] else ["审时度势——准确判断形势把握最佳时机", "时势造英雄——时机重要但创造时机更重要", "错过时机就错过一切——机会稍纵即逝"][i] for i in range(len(["审时度势——准确判断形势把握最佳时机", "时势造英雄——时机重要但创造时机更重要", "错过时机就错过一切——机会稍纵即逝"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.82,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["时机", "形势", "时机", "三分"]) else 0))
        return DecisionResult(sage_name="蒯通", problem=context.get("problem",""), chosen_option=chosen, confidence=0.81)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"蒯通的智慧：审时度势——准确判断形势把握最佳时机"


class _LiYijiCloning(SageCloning):
    """郦食其Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="郦食其", name_en="Li Yiji", era="秦末汉初", years="前269-前203",
            school="纵横家", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="厂卫",
            title="说降齐王", biography="秦汉之际著名说客，刘邦谋士，年过六旬凭三寸不烂之舌说降齐国七十余城。",
            core_works=[],
            capability={"strategic_vision": 7, "execution": 8, "innovation": 7, "leadership": 6, "influence": 7, "cross_domain": 6},
        ))
        self._wisdom_laws = ["以柔克刚——用温和方式达到强硬目的", "老骥伏枥——年龄不是限制意志才是关键", "说客之力——言辞有时比刀剑更有力量"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="郦食其", school="纵横家", problem=problem,
            perspective="从郦食其的以柔克刚智慧出发",
            core_insight="用温和方式达到强硬目的",
            recommendations=[["以柔克刚——用温和方式达到强硬目的", "老骥伏枥——年龄不是限制意志才是关键", "说客之力——言辞有时比刀剑更有力量"][i].split("——")[1] if "——" in ["以柔克刚——用温和方式达到强硬目的", "老骥伏枥——年龄不是限制意志才是关键", "说客之力——言辞有时比刀剑更有力量"][i] else ["以柔克刚——用温和方式达到强硬目的", "老骥伏枥——年龄不是限制意志才是关键", "说客之力——言辞有时比刀剑更有力量"][i] for i in range(len(["以柔克刚——用温和方式达到强硬目的", "老骥伏枥——年龄不是限制意志才是关键", "说客之力——言辞有时比刀剑更有力量"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.82,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["说服", "言辞", "柔和", "谈判"]) else 0))
        return DecisionResult(sage_name="郦食其", problem=context.get("problem",""), chosen_option=chosen, confidence=0.81)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"郦食其的智慧：以柔克刚——用温和方式达到强硬目的"


class _LuJiaCloning(SageCloning):
    """陆贾Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="陆贾", name_en="Lu Jia", era="西汉初", years="西汉初期",
            school="纵横家", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="礼部",
            title="逆取顺守", biography="西汉初期说客、思想家，成功说服赵佗归附汉朝，著《新语》十二篇。",
            core_works=["《新语》"],
            capability={"strategic_vision": 7, "execution": 8, "innovation": 7, "leadership": 6, "influence": 7, "cross_domain": 8},
        ))
        self._wisdom_laws = ["逆取顺守——打天下用武力，治天下用文德", "文武之道——刚柔并济才能长治久安", "以德治国——道德教化是统治的根基"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="陆贾", school="纵横家", problem=problem,
            perspective="从陆贾的逆取顺守智慧出发",
            core_insight="打天下用武力，治天下用文德",
            recommendations=[["逆取顺守——打天下用武力，治天下用文德", "文武之道——刚柔并济才能长治久安", "以德治国——道德教化是统治的根基"][i].split("——")[1] if "——" in ["逆取顺守——打天下用武力，治天下用文德", "文武之道——刚柔并济才能长治久安", "以德治国——道德教化是统治的根基"][i] else ["逆取顺守——打天下用武力，治天下用文德", "文武之道——刚柔并济才能长治久安", "以德治国——道德教化是统治的根基"][i] for i in range(len(["逆取顺守——打天下用武力，治天下用文德", "文武之道——刚柔并济才能长治久安", "以德治国——道德教化是统治的根基"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.82,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["文德", "文武", "道德", "教化"]) else 0))
        return DecisionResult(sage_name="陆贾", problem=context.get("problem",""), chosen_option=chosen, confidence=0.81)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"陆贾的智慧：逆取顺守——打天下用武力，治天下用文德"


class _ZhangQianCloning(SageCloning):
    """张骞Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="张骞", name_en="Zhang Qian", era="西汉", years="前164-前114",
            school="纵横家", tier=CloningTier.TIER2_CLUSTER,
            position="兵部主事", department="兵部",
            title="丝绸之路", biography="西汉著名外交家、探险家，出使西域十三年，开辟丝绸之路。",
            core_works=[],
            capability={"strategic_vision": 9, "execution": 8, "innovation": 8, "leadership": 8, "influence": 10, "cross_domain": 9},
        ))
        self._wisdom_laws = ["使命必达——无论多大困难完成使命是最终目标", "外交是和平的战争——外交官是国家利益守护者", "文化交流——文化影响比武力征服更深远"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="张骞", school="纵横家", problem=problem,
            perspective="从张骞的丝绸之路智慧出发",
            core_insight="无论多大困难完成使命是最终目标",
            recommendations=[["使命必达——无论多大困难完成使命是最终目标", "外交是和平的战争——外交官是国家利益守护者", "文化交流——文化影响比武力征服更深远"][i].split("——")[1] if "——" in ["使命必达——无论多大困难完成使命是最终目标", "外交是和平的战争——外交官是国家利益守护者", "文化交流——文化影响比武力征服更深远"][i] else ["使命必达——无论多大困难完成使命是最终目标", "外交是和平的战争——外交官是国家利益守护者", "文化交流——文化影响比武力征服更深远"][i] for i in range(len(["使命必达——无论多大困难完成使命是最终目标", "外交是和平的战争——外交官是国家利益守护者", "文化交流——文化影响比武力征服更深远"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["使命", "外交", "文化", "长期"]) else 0))
        return DecisionResult(sage_name="张骞", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"张骞的智慧：使命必达——无论多大困难完成使命是最终目标"


class _BanChaoCloning(SageCloning):
    """班超Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="班超", name_en="Ban Chao", era="东汉", years="32-102",
            school="纵横家", tier=CloningTier.TIER2_CLUSTER,
            position="兵部主事", department="兵部",
            title="定远侯", biography="东汉著名外交家、军事家，以三十六人平定西域，'不入虎穴焉得虎子'出自班超。",
            core_works=[],
            capability={"strategic_vision": 9, "execution": 9, "innovation": 8, "leadership": 8, "influence": 9, "cross_domain": 7},
        ))
        self._wisdom_laws = ["不入虎穴焉得虎子——不敢冒险就不可能获得大成功", "以夷制夷——利用矛盾维护自身利益", "先礼后兵——先和平后武力"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="班超", school="纵横家", problem=problem,
            perspective="从班超的不入虎穴智慧出发",
            core_insight="不敢冒险就不可能获得大成功",
            recommendations=[["不入虎穴焉得虎子——不敢冒险就不可能获得大成功", "以夷制夷——利用矛盾维护自身利益", "先礼后兵——先和平后武力"][i].split("——")[1] if "——" in ["不入虎穴焉得虎子——不敢冒险就不可能获得大成功", "以夷制夷——利用矛盾维护自身利益", "先礼后兵——先和平后武力"][i] else ["不入虎穴焉得虎子——不敢冒险就不可能获得大成功", "以夷制夷——利用矛盾维护自身利益", "先礼后兵——先和平后武力"][i] for i in range(len(["不入虎穴焉得虎子——不敢冒险就不可能获得大成功", "以夷制夷——利用矛盾维护自身利益", "先礼后兵——先和平后武力"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["冒险", "勇气", "果断", "虎穴"]) else 0))
        return DecisionResult(sage_name="班超", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"班超的智慧：不入虎穴焉得虎子——不敢冒险就不可能获得大成功"


class _SuWuCloning(SageCloning):
    """苏武Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="苏武", name_en="Su Wu", era="西汉", years="前140-前60",
            school="纵横家", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="礼部",
            title="持节牧羊", biography="西汉著名外交家，持节出使匈奴被扣十九年，始终保持忠诚，'富贵不能淫贫贱不能移威武不能屈'的代表。",
            core_works=[],
            capability={"strategic_vision": 6, "execution": 8, "innovation": 6, "leadership": 8, "influence": 9, "cross_domain": 6},
        ))
        self._wisdom_laws = ["气节至上——精神力量超越物质身体", "忠诚是最大力量——信念可以战胜任何困难", "苦难是人格试金石——逆境中看出真正品格"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="苏武", school="纵横家", problem=problem,
            perspective="从苏武的持节牧羊智慧出发",
            core_insight="精神力量超越物质身体",
            recommendations=[["气节至上——精神力量超越物质身体", "忠诚是最大力量——信念可以战胜任何困难", "苦难是人格试金石——逆境中看出真正品格"][i].split("——")[1] if "——" in ["气节至上——精神力量超越物质身体", "忠诚是最大力量——信念可以战胜任何困难", "苦难是人格试金石——逆境中看出真正品格"][i] else ["气节至上——精神力量超越物质身体", "忠诚是最大力量——信念可以战胜任何困难", "苦难是人格试金石——逆境中看出真正品格"][i] for i in range(len(["气节至上——精神力量超越物质身体", "忠诚是最大力量——信念可以战胜任何困难", "苦难是人格试金石——逆境中看出真正品格"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.82,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["忠诚", "气节", "信念", "坚守"]) else 0))
        return DecisionResult(sage_name="苏武", problem=context.get("problem",""), chosen_option=chosen, confidence=0.81)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"苏武的智慧：气节至上——精神力量超越物质身体"


def build_cluster() -> SchoolCluster:
    """构建纵横家集群"""
    from ..tier1.guiguzi import GuiGuZiCloning

    return SchoolCluster(
        name="纵横家集群",
        school="纵横家",
        department="厂卫",
        leader_name="鬼谷子",
        members={
            "鬼谷子": GuiGuZiCloning(),
            "苏秦": _SuQinCloning(),
            "张仪": _ZhangYiCloning(),
            "陈平": _ChenPingCloning(),
            "范雎": _FanJuCloning(),
            "蔡泽": _CaiZeCloning(),
            "公孙衍": _GongsunYanCloning(),
            "甘茂": _GanMaoCloning(),
            "吕不韦": _LvBuweiCloning(),
            "李斯": _LiSiCloning(),
            "蒯通": _KuaiTongCloning(),
            "郦食其": _LiYijiCloning(),
            "陆贾": _LuJiaCloning(),
            "张骞": _ZhangQianCloning(),
            "班超": _BanChaoCloning(),
            "苏武": _SuWuCloning(),
        },
    )
__all__ = ['build_cluster']
