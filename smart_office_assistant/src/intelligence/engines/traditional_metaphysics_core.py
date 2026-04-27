# -*- coding: utf-8 -*-
"""
中国传统术数核心模块 v1.0.0
Traditional Metaphysics Core

整合:阴阳,五行,天干,地支,生肖,八字

设计原则:
1. 把传统术数抽象为"时空结构分析"而非神秘化结论
2. 输出结构化解释,平衡judge,风险提示与action建议
3. 适合被unified协调器,智慧调度器和上层业务模块复用

版本:v1.0.0
更新:2026-04-02
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Tuple

class WuXing(Enum):
    """五行基础属性"""

    WOOD = ("木", "生发条达", "东方", "春", "青")
    FIRE = ("火", "炎上光明", "南方", "夏", "赤")
    EARTH = ("土", "承载转化", "中央", "四季末", "黄")
    METAL = ("金", "收敛肃杀", "西方", "秋", "白")
    WATER = ("水", "润下藏养", "北方", "冬", "黑")

    def __init__(self, label: str, nature: str, direction: str, season: str, color: str):
        self.label = label
        self.nature = nature
        self.direction = direction
        self.season = season
        self.color = color

    @classmethod
    def from_label(cls, label: str) -> "WuXing":
        for item in cls:
            if item.label == label:
                return item
        raise ValueError(f"未知五行:{label}")

class HeavenlyStem(Enum):
    """十天干"""

    JIA = ("甲", "阳", WuXing.WOOD, "乔木", "开创,生长")
    YI = ("乙", "阴", WuXing.WOOD, "花草", "柔韧,渗透")
    BING = ("丙", "阳", WuXing.FIRE, "太阳", "外放,照耀")
    DING = ("丁", "阴", WuXing.FIRE, "灯烛", "精细,持续")
    WU = ("戊", "阳", WuXing.EARTH, "城墙", "稳固,统摄")
    JI = ("己", "阴", WuXing.EARTH, "田园", "包容,滋养")
    GENG = ("庚", "阳", WuXing.METAL, "刀斧", "决断,改革")
    XIN = ("辛", "阴", WuXing.METAL, "珠玉", "审美,规则")
    REN = ("壬", "阳", WuXing.WATER, "江海", "流动,扩展")
    GUI = ("癸", "阴", WuXing.WATER, "雨露", "润泽,潜藏")

    def __init__(self, label: str, yin_yang: str, element: WuXing, image: str, trait: str):
        self.label = label
        self.yin_yang = yin_yang
        self.element = element
        self.image = image
        self.trait = trait

    @classmethod
    def from_label(cls, label: str) -> "HeavenlyStem":
        for item in cls:
            if item.label == label:
                return item
        raise ValueError(f"未知天干:{label}")

class EarthlyBranch(Enum):
    """十二地支"""

    ZI = ("子", "阳", WuXing.WATER, "鼠", "冬", "23-01", "机敏,启始")
    CHOU = ("丑", "阴", WuXing.EARTH, "牛", "冬末", "01-03", "蓄势,沉稳")
    YIN = ("寅", "阳", WuXing.WOOD, "虎", "初春", "03-05", "开拓,action")
    MAO = ("卯", "阴", WuXing.WOOD, "兔", "仲春", "05-07", "生长,协调")
    CHEN = ("辰", "阳", WuXing.EARTH, "龙", "春末", "07-09", "转化,枢纽")
    SI = ("巳", "阴", WuXing.FIRE, "蛇", "初夏", "09-11", "筹谋,变化")
    WU = ("午", "阳", WuXing.FIRE, "马", "仲夏", "11-13", "外放,执行")
    WEI = ("未", "阴", WuXing.EARTH, "羊", "夏末", "13-15", "调和,收束")
    SHEN = ("申", "阳", WuXing.METAL, "猴", "初秋", "15-17", "应变,效率")
    YOU = ("酉", "阴", WuXing.METAL, "鸡", "仲秋", "17-19", "精修,秩序")
    XU = ("戌", "阳", WuXing.EARTH, "狗", "秋末", "19-21", "守成,边界")
    HAI = ("亥", "阴", WuXing.WATER, "猪", "初冬", "21-23", "涵养,储备")

    def __init__(
        self,
        label: str,
        yin_yang: str,
        element: WuXing,
        zodiac: str,
        season: str,
        clock: str,
        trait: str,
    ):
        self.label = label
        self.yin_yang = yin_yang
        self.element = element
        self.zodiac = zodiac
        self.season = season
        self.clock = clock
        self.trait = trait

    @classmethod
    def from_label(cls, label: str) -> "EarthlyBranch":
        for item in cls:
            if item.label == label:
                return item
        raise ValueError(f"未知地支:{label}")

@dataclass
class GanzhiPillar:
    """干支柱"""

    pillar_name: str
    stem: str
    branch: str
    stem_element: str
    branch_element: str
    yin_yang: str
    zodiac: str
    season: str
    branch_trait: str

@dataclass
class BaziInsight:
    """八字结构洞察"""

    day_master: str
    day_master_element: str
    strength_state: str
    dominant_elements: List[str]
    lacking_elements: List[str]
    useful_elements: List[str]
    controlling_elements: List[str]
    branch_relations: List[str]
    key_suggestions: List[str]

class TraditionalMetaphysicsCore:
    """中国传统术数核心引擎"""

    def __init__(self):
        self.generation_cycle = {
            "木": "火",
            "火": "土",
            "土": "金",
            "金": "水",
            "水": "木",
        }
        self.control_cycle = {
            "木": "土",
            "土": "水",
            "水": "火",
            "火": "金",
            "金": "木",
        }
        self.generated_by = {value: key for key, value in self.generation_cycle.items()}
        self.controlled_by = {value: key for key, value in self.control_cycle.items()}

        self.branch_clashes = {
            frozenset(("子", "午")): "子午冲:节奏过急,易走极端",
            frozenset(("丑", "未")): "丑未冲:内部协调成本上升",
            frozenset(("寅", "申")): "寅申冲:战略与执行拉扯",
            frozenset(("卯", "酉")): "卯酉冲:关系与规则冲突",
            frozenset(("辰", "戌")): "辰戌冲:旧结构与新结构碰撞",
            frozenset(("巳", "亥")): "巳亥冲:明面推进与底层资源错位",
        }
        self.branch_harmony = {
            frozenset(("子", "丑")): "子丑合:资源沉淀能力增强",
            frozenset(("寅", "亥")): "寅亥合:愿景与学习形成助力",
            frozenset(("卯", "戌")): "卯戌合:文化与执行开始成形",
            frozenset(("辰", "酉")): "辰酉合:规则,制度与细节趋于收敛",
            frozenset(("巳", "申")): "巳申合:strategy与效率相互支持",
            frozenset(("午", "未")): "午未合:外部表达与内部承接较顺",
        }

        self.element_keywords = {
            "木": ["增长", "生长", "开拓", "创新", "教育", "组织扩张", "产品迭代"],
            "火": ["品牌", "传播", "曝光", "热度", "表达", "影响力", "内容"],
            "土": ["管理", "交付", "承接", "组织稳定", "中台", "流程", "信任"],
            "金": ["规则", "标准", "财务", "法务", "风控", "决断", "考核"],
            "水": ["信息", "流量", "研究", "数据", "连接", "供应链", "储备"],
        }

    def infer_elements_from_text(self, text: str) -> Dict[str, float]:
        """根据文本粗略提取五行倾向"""
        scores = {item.label: 0.0 for item in WuXing}
        for element, keywords in self.element_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    scores[element] += 1.0

        if sum(scores.values()) == 0:
            # 默认给出一个中性起点,避免全零
            return {"木": 1.0, "火": 1.0, "土": 1.0, "金": 1.0, "水": 1.0}
        return scores

    def normalize_element_weights(self, element_weights: Any) -> Dict[str, float]:
        """标准化五行输入"""
        normalized = {item.label: 0.0 for item in WuXing}

        if isinstance(element_weights, dict):
            for key, value in element_weights.items():
                if key in normalized:
                    normalized[key] += float(value)
                else:
                    inferred = self.infer_elements_from_text(str(key))
                    for element, score in inferred.items():
                        normalized[element] += score * float(value)
        elif isinstance(element_weights, Sequence) and not isinstance(element_weights, (str, bytes)):
            for token in element_weights:
                inferred = self.infer_elements_from_text(str(token))
                for element, score in inferred.items():
                    normalized[element] += score
        else:
            return self.infer_elements_from_text(str(element_weights))

        if sum(normalized.values()) == 0:
            return {"木": 1.0, "火": 1.0, "土": 1.0, "金": 1.0, "水": 1.0}
        return normalized

    def analyze_wuxing_balance(self, element_weights: Any) -> Dict[str, Any]:
        """五行平衡分析"""
        scores = self.normalize_element_weights(element_weights)
        total = sum(scores.values()) or 1.0
        ratios = {key: round(value / total, 3) for key, value in scores.items()}
        ranked = sorted(ratios.items(), key=lambda item: item[1], reverse=True)

        strongest = ranked[0][0]
        weakest = ranked[-1][0]
        spread = round(ranked[0][1] - ranked[-1][1], 3)

        if spread <= 0.08:
            state = "五行相对均衡"
        elif ranked[0][1] >= 0.32:
            state = f"{strongest}偏旺"
        else:
            state = f"{ranked[0][0]},{ranked[1][0]}偏强"

        recommendations = []
        if ratios[weakest] < 0.12:
            source = self.generated_by[weakest]
            recommendations.append(f"当前{weakest}偏弱,宜优先补足{source}→{weakest}的生扶链路.")
        if ratios[strongest] > 0.30:
            drain = self.generation_cycle[strongest]
            control = self.controlled_by[strongest]
            recommendations.append(f"当前{strongest}偏旺,宜用{drain}泄秀或用{control}制衡,避免单一力量过盛.")
        recommendations.append(f"核心节奏建议:以{strongest}为主动力,以{weakest}为补短板方向.")

        return {
            "scores": {key: round(value, 2) for key, value in scores.items()},
            "ratios": ratios,
            "state": state,
            "strongest": strongest,
            "weakest": weakest,
            "dominant_pair": [ranked[0][0], ranked[1][0]],
            "spread": spread,
            "recommendations": recommendations,
        }

    def build_pillar(self, pillar_name: str, ganzhi: str) -> GanzhiPillar:
        """构建单柱信息"""
        if not isinstance(ganzhi, str) or len(ganzhi) < 2:
            raise ValueError(f"无效干支:{ganzhi}")

        stem = HeavenlyStem.from_label(ganzhi[0])
        branch = EarthlyBranch.from_label(ganzhi[1])
        return GanzhiPillar(
            pillar_name=pillar_name,
            stem=stem.label,
            branch=branch.label,
            stem_element=stem.element.label,
            branch_element=branch.element.label,
            yin_yang=stem.yin_yang,
            zodiac=branch.zodiac,
            season=branch.season,
            branch_trait=branch.trait,
        )

    def analyze_ganzhi_structure(self, pillars: Dict[str, str]) -> Dict[str, Any]:
        """天干地支结构分析"""
        pillar_objects: Dict[str, GanzhiPillar] = {
            name: self.build_pillar(name, ganzhi)
            for name, ganzhi in pillars.items()
            if ganzhi
        }

        element_weights: Dict[str, float] = {item.label: 0.0 for item in WuXing}
        branch_labels: List[str] = []
        for pillar in pillar_objects.values():
            element_weights[pillar.stem_element] += 1.0
            element_weights[pillar.branch_element] += 1.2
            branch_labels.append(pillar.branch)

        relations: List[str] = []
        for i in range(len(branch_labels)):
            for j in range(i + 1, len(branch_labels)):
                pair = frozenset((branch_labels[i], branch_labels[j]))
                if pair in self.branch_clashes:
                    relations.append(self.branch_clashes[pair])
                if pair in self.branch_harmony:
                    relations.append(self.branch_harmony[pair])

        month_branch = pillar_objects.get("month")
        timing_advice = (
            f"月令落在{month_branch.branch}位,对应{month_branch.season}之气,适合围绕{month_branch.branch_element}行资源配置."
            if month_branch
            else "缺少月令信息,时机judge只能做保守解释."
        )

        return {
            "pillars": {name: asdict(pillar) for name, pillar in pillar_objects.items()},
            "element_balance": self.analyze_wuxing_balance(element_weights),
            "branch_relations": relations or ["地支之间未见明显冲合,结构相对平稳."],
            "timing_advice": timing_advice,
        }

    def interpret_bazi(self, pillars: Dict[str, str]) -> Dict[str, Any]:
        """八字结构解释器"""
        structure = self.analyze_ganzhi_structure(pillars)
        day_pillar = structure["pillars"].get("day")
        if not day_pillar:
            raise ValueError("八字解释至少需要提供日柱")

        day_master = day_pillar["stem"]
        day_master_element = day_pillar["stem_element"]
        balance = structure["element_balance"]
        ratios = balance["ratios"]

        month_pillar = structure["pillars"].get("month")
        month_support = 0.0
        if month_pillar:
            month_element = month_pillar["branch_element"]
            if month_element == day_master_element:
                month_support = 0.25
            elif self.generated_by[day_master_element] == month_element:
                month_support = 0.18
            elif self.controlled_by[day_master_element] == month_element:
                month_support = -0.18

        base_score = ratios.get(day_master_element, 0.2) + month_support
        if base_score >= 0.42:
            strength_state = "日主偏强"
            useful_elements = [self.generation_cycle[day_master_element], self.controlled_by[day_master_element]]
        elif base_score <= 0.20:
            strength_state = "日主偏弱"
            useful_elements = [day_master_element, self.generated_by[day_master_element]]
        else:
            strength_state = "日主中和"
            useful_elements = [self.generation_cycle[day_master_element], self.generated_by[day_master_element]]

        ranked = sorted(balance["ratios"].items(), key=lambda item: item[1], reverse=True)
        dominant_elements = [item[0] for item in ranked[:2]]
        lacking_elements = [item[0] for item in ranked if item[1] <= 0.12]
        controlling_elements = [self.controlled_by[day_master_element], self.control_cycle[day_master_element]]

        suggestions = [
            f"先看日主:{day_master}{day_master_element},当前judge为'{strength_state}'.",
            f"用神倾向可优先参考:{','.join(useful_elements)}.",
            f"当前结构主轴在:{','.join(dominant_elements)}.",
        ]
        if lacking_elements:
            suggestions.append(f"短板主要在:{','.join(lacking_elements)},宜通过环境,角色分工或节奏安排补齐.")
        suggestions.extend(structure["branch_relations"][:2])

        insight = BaziInsight(
            day_master=day_master,
            day_master_element=day_master_element,
            strength_state=strength_state,
            dominant_elements=dominant_elements,
            lacking_elements=lacking_elements,
            useful_elements=useful_elements,
            controlling_elements=controlling_elements,
            branch_relations=structure["branch_relations"],
            key_suggestions=suggestions,
        )

        return {
            "pillars": structure["pillars"],
            "element_balance": balance,
            "timing_advice": structure["timing_advice"],
            "insight": asdict(insight),
        }

    def analyze_zodiac_pattern(self, zodiacs: Sequence[str]) -> Dict[str, Any]:
        """生肖关系分析"""
        zodiac_to_branch = {branch.zodiac: branch for branch in EarthlyBranch}
        branches = [zodiac_to_branch[z] for z in zodiacs if z in zodiac_to_branch]
        if not branches:
            return {
                "zodiacs": list(zodiacs),
                "relations": ["未recognize到有效生肖,无法建立生肖关系分析."],
                "recommendation": "请传入标准生肖名称,例如:龙,蛇,马.",
            }

        relations: List[str] = []
        for i in range(len(branches)):
            for j in range(i + 1, len(branches)):
                pair = frozenset((branches[i].label, branches[j].label))
                if pair in self.branch_harmony:
                    relations.append(self.branch_harmony[pair])
                if pair in self.branch_clashes:
                    relations.append(self.branch_clashes[pair])

        traits = [f"{branch.zodiac}:{branch.trait}" for branch in branches]
        recommendation = "生肖组合整体平稳,可按角色互补设计协作."
        if any("冲" in relation for relation in relations):
            recommendation = "生肖关系存在明显冲位,协作时要先定边界,再定节奏."
        elif any("合" in relation for relation in relations):
            recommendation = "生肖关系有合势,适合做分工互补与长期搭配."

        return {
            "zodiacs": [branch.zodiac for branch in branches],
            "traits": traits,
            "relations": relations or ["未见明显冲合,关系偏中性."],
            "recommendation": recommendation,
        }

    def generate_metaphysics_brief(self, problem: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """generate术数简报"""
        context = context or {}
        element_input = context.get("element_weights") or context.get("factors") or problem
        wuxing = self.analyze_wuxing_balance(element_input)

        brief = {
            "problem": problem,
            "wuxing": wuxing,
            "recommendation": f"围绕{wuxing['strongest']}展开主攻,同时优先补足{wuxing['weakest']}短板.",
            "action": f"把{wuxing['strongest']}作为当前发力轴,把{wuxing['weakest']}作为风险补位轴.",
        }

        pillars = context.get("pillars") or context.get("bazi")
        if isinstance(pillars, dict):
            brief["bazi"] = self.interpret_bazi(pillars)

        zodiacs = context.get("zodiacs")
        if isinstance(zodiacs, Sequence) and not isinstance(zodiacs, (str, bytes)):
            brief["zodiac"] = self.analyze_zodiac_pattern(zodiacs)

        return brief

_default_core: Optional[TraditionalMetaphysicsCore] = None

def get_traditional_metaphysics_core() -> TraditionalMetaphysicsCore:
    """get单例核心"""
    global _default_core
    if _default_core is None:
        _default_core = TraditionalMetaphysicsCore()
    return _default_core

__all__ = [
    "WuXing",
    "HeavenlyStem",
    "EarthlyBranch",
    "GanzhiPillar",
    "BaziInsight",
    "TraditionalMetaphysicsCore",
    "get_traditional_metaphysics_core",
]
