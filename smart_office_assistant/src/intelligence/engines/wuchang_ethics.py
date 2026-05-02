# -*- coding: utf-8 -*-
"""
__all__ = [
    'ethical_judgment',
    'evaluate_action',
    'evaluate_person',
    'get_wuchang_evaluator',
    'get_wuchang_wisdom',
    'recommend_balance',
]

五常伦理评估器 v1.0.0
======================

基于儒学"仁义礼智信"五常的道德评估系统

核心思想:
- 仁:仁者爱人,恻隐之心
- 义:义者宜也,羞恶之心
- 礼:礼者理也,辞让之心
- 智:智者知也,是非之心
- 信:信者诚也,笃实不欺

版本:v1.0.0
更新:2026-04-02
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

class FiveChang(Enum):
    """五常枚举"""
    REN = "仁"     # 仁者爱人
    YI = "义"      # 义者宜也
    LI = "礼"      # 礼者理也
    ZHI = "智"     # 智者知也
    XIN = "信"     # 信者诚也

@dataclass
class WuchangAssessment:
    """五常评估结果"""
    ren_score: float           # 仁
    yi_score: float            # 义
    li_score: float            # 礼
    zhi_score: float           # 智
    xin_score: float           # 信
    total_score: float         # 总分
    primary_strength: str      # 主要优点
    primary_weakness: str      # 主要不足
    overall_judgment: str      # 总体judge
    recommendations: List[str] = field(default_factory=list)
    quote: str = ""             # 五常引述

class WuchangEthicsEvaluator:
    """
    五常伦理评估器

    评估框架:
    ┌─────────────────────────────────────────────┐
    │              五常伦理体系                    │
    ├─────────────────────────────────────────────┤
    │  仁 → 恻隐之心,仁者爱人                    │
    │  义 → 羞恶之心,义者宜也                    │
    │  礼 → 辞让之心,礼者理也                   │
    │  智 → 是非之心,智者知也                   │
    │  信 → 笃实之心,信者诚也                   │
    └─────────────────────────────────────────────┘

    核心方法:
    - evaluate_action() - 评估行为五常
    - evaluate_person() - 评估人物五常
    - ethical_judgment() - 道德judge
    - recommend_balance() - 平衡建议
    """

    def __init__(self):
        """init五常评估器"""
        self.name = "WuchangEthicsEvaluator"
        self.version="6.2.0"

        # 五常核心定义
        self.wuchang_definitions = {
            "仁": {
                "meaning": "仁者爱人,包括爱自己,爱他人,爱万物",
                "keywords": ["爱", "关怀", "慈悲", "同情", "助人", "宽恕", "恻隐"],
                "antonyms": ["残忍", "冷酷", "自私", "冷漠"],
                "quote": "仁者爱人,有礼者敬人.爱人者,人恒爱之.",
                "source": "<孟子>"
            },
            "义": {
                "meaning": "义者宜也,做应当做的事",
                "keywords": ["正当", "合宜", "正义", "公正", "道义", "合适", "应当"],
                "antonyms": ["邪恶", "不义", "徇私", "枉法"],
                "quote": "义,人之路也.舍生而取义.",
                "source": "<孟子>"
            },
            "礼": {
                "meaning": "礼者理也,社会规范与秩序",
                "keywords": ["礼貌", "规矩", "秩序", "规范", "礼节", "谦让", "恭敬"],
                "antonyms": ["无礼", "傲慢", "粗鲁", "失礼"],
                "quote": "非礼勿视,非礼勿听,非礼勿言,非礼勿动.",
                "source": "<论语>"
            },
            "智": {
                "meaning": "智者知也,明辨是非真假",
                "keywords": ["明智", "聪明", "智慧", "理性", "judge", "知识", "学识"],
                "antonyms": ["愚昧", "无知", "糊涂", "盲目"],
                "quote": "知之为知之,不知为不知,是知也.",
                "source": "<论语>"
            },
            "信": {
                "meaning": "信者诚也,说话真实,行为笃实",
                "keywords": ["诚信", "诚实", "可靠", "守信", "承诺", "真实", "信用"],
                "antonyms": ["欺诈", "虚伪", "失信", "欺骗"],
                "quote": "言必信,行必果.民无信不立.",
                "source": "<论语>"
            }
        }

        # 评估权重
        self.weights = {
            "仁": 0.25,
            "义": 0.25,
            "礼": 0.2,
            "智": 0.15,
            "信": 0.15
        }

    def evaluate_action(self, action: str, context: Optional[Dict] = None) -> WuchangAssessment:
        """
        评估行为的五常表现

        Args:
            action: 行为描述
            context: 上下文(可选)

        Returns:
            WuchangAssessment: 五常评估结果
        """
        action_lower = action.lower()

        # 评估每一种常
        scores = {}
        for chang in FiveChang:
            scores[chang.value] = self._evaluate_single(
                chang.value, action_lower, context
            )

        # 计算总分
        total = sum(scores[k] * self.weights[k] for k in scores)

        # 找出优势和劣势
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        primary_strength = sorted_scores[0][0]
        primary_weakness = sorted_scores[-1][0]

        # generate总体judge
        judgment = self._generate_judgment(scores, total)

        # generate建议
        recommendations = self._generate_recommendations(scores)

        return WuchangAssessment(
            ren_score=scores["仁"],
            yi_score=scores["义"],
            li_score=scores["礼"],
            zhi_score=scores["智"],
            xin_score=scores["信"],
            total_score=total,
            primary_strength=primary_strength,
            primary_weakness=primary_weakness,
            overall_judgment=judgment,
            recommendations=recommendations,
            quote=self.wuchang_definitions[primary_strength]["quote"]
        )

    def _evaluate_single(self, chang: str, action: str,
                         context: Optional[Dict]) -> float:
        """评估单一五常"""
        definition = self.wuchang_definitions[chang]
        base_score = 0.5

        # 检查正向关键词
        for kw in definition["keywords"]:
            if kw in action:
                base_score += 0.1

        # 检查反向关键词
        for kw in definition["antonyms"]:
            if kw in action:
                base_score -= 0.2

        # 上下文调整
        if context:
            if context.get("is_intentional"):
                base_score += 0.05
            if context.get("has_consequence"):
                base_score += 0.05 * context.get("consequence_magnitude", 0.5)

        return max(0.0, min(1.0, base_score))

    def _generate_judgment(self, scores: Dict[str, float],
                           total: float) -> str:
        """generate总体judge"""
        if total >= 0.85:
            return "上德:五常兼备,道德完人"
        elif total >= 0.75:
            return "中德:道德优良,有待完善"
        elif total >= 0.6:
            return "下德:基本合格,需加强修养"
        elif total >= 0.45:
            return "小德:有所偏废,需要改正"
        else:
            return "无德:背离五常,需深刻反省"

    def _generate_recommendations(self, scores: Dict[str, float]) -> List[str]:
        """generate五常建议"""
        recommendations = []

        for chang, score in scores.items():
            if score < 0.6:
                definition = self.wuchang_definitions[chang]
                recommendations.append(
                    f"加强{chang}:{definition['meaning']},"
                    f"可从{','.join(definition['keywords'][:2])}做起"
                )

        if not recommendations:
            recommendations.append("继续保持五常修行,精益求精")

        return recommendations

    def evaluate_person(self, traits: List[str],
                        behaviors: List[str]) -> WuchangAssessment:
        """
        评估人物的五常水平

        Args:
            traits: 特质列表
            behaviors: 行为列表

        Returns:
            WuchangAssessment: 五常评估结果
        """
        all_text = " ".join(traits + behaviors)

        scores = {}
        for chang in FiveChang:
            definition = self.wuchang_definitions[chang.value]
            score = 0.5

            # 特质加分
            for trait in traits:
                if any(kw in trait for kw in definition["keywords"]):
                    score += 0.1
                if any(kw in trait for kw in definition["antonyms"]):
                    score -= 0.15

            # 行为加分
            for behavior in behaviors:
                if any(kw in behavior for kw in definition["keywords"]):
                    score += 0.1
                if any(kw in behavior for kw in definition["antonyms"]):
                    score -= 0.15

            scores[chang.value] = max(0.0, min(1.0, score))

        # 计算总分
        total = sum(scores[k] * self.weights[k] for k in scores)

        # 找出优势和劣势
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return WuchangAssessment(
            ren_score=scores["仁"],
            yi_score=scores["义"],
            li_score=scores["礼"],
            zhi_score=scores["智"],
            xin_score=scores["信"],
            total_score=total,
            primary_strength=sorted_scores[0][0],
            primary_weakness=sorted_scores[-1][0],
            overall_judgment=self._generate_judgment(scores, total),
            recommendations=self._generate_recommendations(scores),
            quote=f"君子五常:仁义礼智信,各有所长."
        )

    def ethical_judgment(self, action: str, stakeholder: str,
                         principle: str = "功利主义") -> Dict[str, Any]:
        """
        道德judge

        Args:
            action: 行为
            stakeholder: 相关方
            principle: judge原则(功利主义/义务论/美德伦理)

        Returns:
            道德judge结果
        """
        assessment = self.evaluate_action(action)

        # 功利主义judge
        if principle == "功利主义":
            if assessment.total_score >= 0.6:
                result = "道德上可接受"
                reason = "该行为能带来正面的道德后果"
            else:
                result = "道德上不可取"
                reason = "该行为可能导致负面后果"

        # 义务论judge
        elif principle == "义务论":
            if assessment.yi_score >= 0.7 and assessment.xin_score >= 0.7:
                result = "义务上正当"
                reason = "该行为符合义与信的要求"
            else:
                result = "义务上有问题"
                reason = "该行为可能违背义务论原则"

        # 美德伦理judge
        else:  # 美德伦理
            if assessment.total_score >= 0.7:
                result = "符合美德"
                reason = "该行为体现了良好的道德品质"
            else:
                result = "有违美德"
                reason = "该行为未能体现应有的美德"

        return {
            "action": action,
            "stakeholder": stakeholder,
            "principle": principle,
            "assessment": assessment,
            "judgment": result,
            "reason": reason,
            "quote": "君子喻于义,小人喻于利."
        }

    def recommend_balance(self, current_scores: Dict[str, float]) -> Dict[str, Any]:
        """
        五常平衡建议

        Args:
            current_scores: 当前五常分数

        Returns:
            平衡建议
        """
        total = sum(current_scores.values())
        avg = total / 5

        unbalanced = []
        balanced = []

        for chang, score in current_scores.items():
            if abs(score - avg) > 0.2:
                unbalanced.append(chang)
            else:
                balanced.append(chang)

        recommendations = []

        # 调整建议
        if "仁" in unbalanced:
            recommendations.append(
                "仁:己所不欲,勿施于人;恻隐之心,人皆有之"
            )

        if "义" in unbalanced:
            recommendations.append(
                "义:见利思义,舍生取义;当义不义,非勇也"
            )

        if "礼" in unbalanced:
            recommendations.append(
                "礼:非礼勿动,恭而有礼;礼尚往来,以和为贵"
            )

        if "智" in unbalanced:
            recommendations.append(
                "智:知人者智,自知者明;多闻阙疑,慎言其余"
            )

        if "信" in unbalanced:
            recommendations.append(
                "信:言必信,行必果;人无信不立,国无信不强"
            )

        return {
            "current_scores": current_scores,
            "average": avg,
            "unbalanced": unbalanced,
            "balanced": balanced,
            "recommendations": recommendations,
            "quote": "五常并重,缺一不可."
        }

    def get_wuchang_wisdom(self) -> Dict[str, Dict[str, str]]:
        """get五常智慧"""
        return self.wuchang_definitions

# 全局实例
_wuchang_evaluator: Optional[WuchangEthicsEvaluator] = None

def get_wuchang_evaluator() -> WuchangEthicsEvaluator:
    """get五常评估器实例"""
    global _wuchang_evaluator
    if _wuchang_evaluator is None:
        _wuchang_evaluator = WuchangEthicsEvaluator()
    return _wuchang_evaluator
