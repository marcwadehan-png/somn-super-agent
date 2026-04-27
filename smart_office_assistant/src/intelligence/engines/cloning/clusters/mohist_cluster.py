# -*- coding: utf-8 -*-
"""墨家集群 Cloning - Tier 2 学派集群"""

from typing import Dict, List, Optional, Any
from .._cloning_base import SageCloning, SchoolCluster
from .._cloning_types import AnalysisResult, DecisionResult, SageProfile, CloningTier


class _QinGuliCloning(SageCloning):
    """禽滑厘Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="禽滑厘", name_en="Qin Guli", era="战国", years="前470-前390",
            school="墨家", tier=CloningTier.TIER2_CLUSTER,
            position="工部主事", department="工部",
            title="墨家巨子", biography="墨子最重要的弟子，墨家第二任巨子。",
            core_works=[],
            capability={"strategic_vision": 6, "execution": 9, "innovation": 6, "leadership": 8, "influence": 6, "cross_domain": 5},
        ))
        self._wisdom_laws = ["兼爱非攻——和平主义先驱", "身体力行——实践墨子理念", "组织纪律——墨者集团以纪律严明著称"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="禽滑厘", school="墨家", problem=problem,
            perspective="从禽滑厘的墨家巨子智慧出发",
            core_insight="和平主义先驱",
            recommendations=[["兼爱非攻——和平主义先驱", "身体力行——实践墨子理念", "组织纪律——墨者集团以纪律严明著称"][i].split("——")[1] if "——" in ["兼爱非攻——和平主义先驱", "身体力行——实践墨子理念", "组织纪律——墨者集团以纪律严明著称"][i] else ["兼爱非攻——和平主义先驱", "身体力行——实践墨子理念", "组织纪律——墨者集团以纪律严明著称"][i] for i in range(len(["兼爱非攻——和平主义先驱", "身体力行——实践墨子理念", "组织纪律——墨者集团以纪律严明著称"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["实践", "纪律", "和平", "执行"]) else 0))
        return DecisionResult(sage_name="禽滑厘", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"禽滑厘的智慧：兼爱非攻——和平主义先驱"


class _MengShengCloning(SageCloning):
    """孟胜Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="孟胜", name_en="Meng Sheng", era="战国中期", years="战国中期",
            school="墨家", tier=CloningTier.TIER2_CLUSTER,
            position="工部主事", department="工部",
            title="墨家巨子", biography="墨家重要传人，巨子制度代表，为信义与一百八十余弟子集体殉死。",
            core_works=[],
            capability={"strategic_vision": 6, "execution": 9, "innovation": 6, "leadership": 9, "influence": 7, "cross_domain": 5},
        ))
        self._wisdom_laws = ["信念比生命更重要——信仰的力量超越生死", "契约精神——守信用是墨家核心价值观", "团体利益高于个人——集体主义精神"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="孟胜", school="墨家", problem=problem,
            perspective="从孟胜的信念殉道智慧出发",
            core_insight="信仰的力量超越生死",
            recommendations=[["信念比生命更重要——信仰的力量超越生死", "契约精神——守信用是墨家核心价值观", "团体利益高于个人——集体主义精神"][i].split("——")[1] if "——" in ["信念比生命更重要——信仰的力量超越生死", "契约精神——守信用是墨家核心价值观", "团体利益高于个人——集体主义精神"][i] else ["信念比生命更重要——信仰的力量超越生死", "契约精神——守信用是墨家核心价值观", "团体利益高于个人——集体主义精神"][i] for i in range(len(["信念比生命更重要——信仰的力量超越生死", "契约精神——守信用是墨家核心价值观", "团体利益高于个人——集体主义精神"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.82,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["信念", "信义", "集体", "原则"]) else 0))
        return DecisionResult(sage_name="孟胜", problem=context.get("problem",""), chosen_option=chosen, confidence=0.81)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"孟胜的智慧：信念比生命更重要——信仰的力量超越生死"


class _TianXiangziCloning(SageCloning):
    """田襄子Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="田襄子", name_en="Tian Xiangzi", era="战国中期", years="战国中期",
            school="墨家", tier=CloningTier.TIER2_CLUSTER,
            position="工部主事", department="工部",
            title="墨家巨子", biography="墨家重要传人，继孟胜之后担任墨家巨子，继续发展传播墨学。",
            core_works=[],
            capability={"strategic_vision": 6, "execution": 7, "innovation": 5, "leadership": 7, "influence": 6, "cross_domain": 5},
        ))
        self._wisdom_laws = ["传承需要载体——组织是理念传承的保障", "接力棒式发展——每代人都为共同事业贡献力量", "组织建设——维护和发展墨家组织体系"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="田襄子", school="墨家", problem=problem,
            perspective="从田襄子的墨学传承智慧出发",
            core_insight="组织是理念传承的保障",
            recommendations=[["传承需要载体——组织是理念传承的保障", "接力棒式发展——每代人都为共同事业贡献力量", "组织建设——维护和发展墨家组织体系"][i].split("——")[1] if "——" in ["传承需要载体——组织是理念传承的保障", "接力棒式发展——每代人都为共同事业贡献力量", "组织建设——维护和发展墨家组织体系"][i] else ["传承需要载体——组织是理念传承的保障", "接力棒式发展——每代人都为共同事业贡献力量", "组织建设——维护和发展墨家组织体系"][i] for i in range(len(["传承需要载体——组织是理念传承的保障", "接力棒式发展——每代人都为共同事业贡献力量", "组织建设——维护和发展墨家组织体系"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.80,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["传承", "组织", "接力", "延续"]) else 0))
        return DecisionResult(sage_name="田襄子", problem=context.get("problem",""), chosen_option=chosen, confidence=0.79)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"田襄子的智慧：传承需要载体——组织是理念传承的保障"


class _FuDunCloning(SageCloning):
    """腹䵍Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="腹䵍", name_en="Fu Dun", era="战国末期", years="战国末期",
            school="墨家", tier=CloningTier.TIER2_CLUSTER,
            position="工部主事", department="工部",
            title="秦国墨家巨子", biography="秦国墨家巨子，其子杀人，秦王欲赦，腹䵍坚持墨家原则处死亲子。",
            core_works=[],
            capability={"strategic_vision": 6, "execution": 8, "innovation": 6, "leadership": 8, "influence": 7, "cross_domain": 5},
        ))
        self._wisdom_laws = ["法律面前人人平等——王公贵族不能例外", "以身作则——领导者必须以身作则", "大义灭亲——公与私必须分明"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="腹䵍", school="墨家", problem=problem,
            perspective="从腹䵍的大义灭亲智慧出发",
            core_insight="法律面前人人平等",
            recommendations=[["法律面前人人平等——王公贵族不能例外", "以身作则——领导者必须以身作则", "大义灭亲——公与私必须分明"][i].split("——")[1] if "——" in ["法律面前人人平等——王公贵族不能例外", "以身作则——领导者必须以身作则", "大义灭亲——公与私必须分明"][i] else ["法律面前人人平等——王公贵族不能例外", "以身作则——领导者必须以身作则", "大义灭亲——公与私必须分明"][i] for i in range(len(["法律面前人人平等——王公贵族不能例外", "以身作则——领导者必须以身作则", "大义灭亲——公与私必须分明"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.82,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["法律", "原则", "公正", "平等"]) else 0))
        return DecisionResult(sage_name="腹䵍", problem=context.get("problem",""), chosen_option=chosen, confidence=0.81)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"腹䵍的智慧：法律面前人人平等——王公贵族不能例外"


class _WangZhongCloning(SageCloning):
    """汪中Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="汪中", name_en="Wang Zhong", era="清代", years="1745-1794",
            school="墨家", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="礼部",
            title="墨学复兴先驱", biography="清代学者，墨学复兴先驱，整理出版《墨子》校本，使墨学得以重新流传。",
            core_works=["《墨子校本》"],
            capability={"strategic_vision": 6, "execution": 7, "innovation": 7, "leadership": 5, "influence": 8, "cross_domain": 6},
        ))
        self._wisdom_laws = ["重新发现被遗忘的智慧——让墨学重见天日", "考证是学术基础——严谨考证还历史真相", "被忽视不等于没价值——沉寂千年终被发现"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="汪中", school="墨家", problem=problem,
            perspective="从汪中的墨学复兴智慧出发",
            core_insight="让墨学重见天日",
            recommendations=[["重新发现被遗忘的智慧——让墨学重见天日", "考证是学术基础——严谨考证还历史真相", "被忽视不等于没价值——沉寂千年终被发现"][i].split("——")[1] if "——" in ["重新发现被遗忘的智慧——让墨学重见天日", "考证是学术基础——严谨考证还历史真相", "被忽视不等于没价值——沉寂千年终被发现"][i] else ["重新发现被遗忘的智慧——让墨学重见天日", "考证是学术基础——严谨考证还历史真相", "被忽视不等于没价值——沉寂千年终被发现"][i] for i in range(len(["重新发现被遗忘的智慧——让墨学重见天日", "考证是学术基础——严谨考证还历史真相", "被忽视不等于没价值——沉寂千年终被发现"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.82,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["考证", "复兴", "整理", "发现"]) else 0))
        return DecisionResult(sage_name="汪中", problem=context.get("problem",""), chosen_option=chosen, confidence=0.81)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"汪中的智慧：重新发现被遗忘的智慧——让墨学重见天日"


class _SunYirangCloning(SageCloning):
    """孙诒让Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="孙诒让", name_en="Sun Yirang", era="清末", years="1848-1908",
            school="墨家", tier=CloningTier.TIER2_CLUSTER,
            position="礼部主事", department="礼部",
            title="墨学集大成", biography="清末著名学者，著《墨子闲诂》，墨学研究的集大成之作，被梁启超誉为'现代墨学复兴的开端'。",
            core_works=["《墨子闲诂》"],
            capability={"strategic_vision": 7, "execution": 7, "innovation": 8, "leadership": 6, "influence": 9, "cross_domain": 7},
        ))
        self._wisdom_laws = ["集大成需要站在巨人肩上——吸收历代研究成果", "校勘是经典传承的基础——没有校勘就没有准确文本", "学术研究服务社会——经世致用是治学更高境界"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="孙诒让", school="墨家", problem=problem,
            perspective="从孙诒让的墨学集大成智慧出发",
            core_insight="站在巨人肩上集历代之大成",
            recommendations=[["集大成需要站在巨人肩上——吸收历代研究成果", "校勘是经典传承的基础——没有校勘就没有准确文本", "学术研究服务社会——经世致用是治学更高境界"][i].split("——")[1] if "——" in ["集大成需要站在巨人肩上——吸收历代研究成果", "校勘是经典传承的基础——没有校勘就没有准确文本", "学术研究服务社会——经世致用是治学更高境界"][i] else ["集大成需要站在巨人肩上——吸收历代研究成果", "校勘是经典传承的基础——没有校勘就没有准确文本", "学术研究服务社会——经世致用是治学更高境界"][i] for i in range(len(["集大成需要站在巨人肩上——吸收历代研究成果", "校勘是经典传承的基础——没有校勘就没有准确文本", "学术研究服务社会——经世致用是治学更高境界"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["集大成", "传承", "校勘", "经世致用"]) else 0))
        return DecisionResult(sage_name="孙诒让", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"孙诒让的智慧：集大成需要站在巨人肩上——吸收历代研究成果"


def build_cluster() -> SchoolCluster:
    """构建墨家集群"""
    from ..tier1.mozi import MoZiCloning

    return SchoolCluster(
        name="墨家集群",
        school="墨家",
        department="工部",
        leader_name="墨子",
        members={
            "墨子": MoZiCloning(),
            "禽滑厘": _QinGuliCloning(),
            "孟胜": _MengShengCloning(),
            "田襄子": _TianXiangziCloning(),
            "腹䵍": _FuDunCloning(),
            "汪中": _WangZhongCloning(),
            "孙诒让": _SunYirangCloning(),
        },
    )
__all__ = ['build_cluster']
