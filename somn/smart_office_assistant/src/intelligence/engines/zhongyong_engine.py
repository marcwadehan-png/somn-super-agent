# -*- coding: utf-8 -*-
"""
__all__ = [
    'assess_situation_zhongyong',
    'evaluate_action_extremes',
    'evaluate_balance',
    'find_central_path',
    'get_zhongyong_engine',
    'get_zhongyong_wisdom',
]

中庸decision引擎 v1.0.0
=====================

基于<中庸>的中和之道decision系统

核心思想:
- <中庸>:喜怒哀乐之未发,谓之中;发而皆中节,谓之和
- 极高明而道中庸
- 执其两端,用其中于民
- 过犹不及,恰到好处

版本:v1.0.0
更新:2026-04-02
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math

class BalanceState(Enum):
    """平衡状态"""
    TOO_LEFT = "偏左"      # 过于保守
    SLIGHTLY_LEFT = "微左"  # 略微保守
    BALANCED = "中正"      # 恰到好处
    SLIGHTLY_RIGHT = "微右" # 略微激进
    TOO_RIGHT = "偏右"     # 过于激进

class ExtremeType(Enum):
    """极端类型"""
    OVER = "过"     # 过分
    UNDER = "不及"   # 不足
    NONE = "中"     # 中正

@dataclass
class ZhongYongDecision:
    """中庸decision结果"""
    balance_score: float           # 平衡分数(0-1)
    balance_state: BalanceState    # 平衡状态
    extreme_risk: ExtremeType      # 极端风险
    recommendation: str            # 调整建议
    quote: str                      # 中庸引述
    reasoning: str                  # 推理过程

class ZhongYongEngine:
    """
    中庸decision引擎

    核心原理:
    ┌─────────────────────────────────────────────┐
    │            中庸之道                            │
    ├─────────────────────────────────────────────┤
    │   偏左 ←──────── 中正 ────────→ 偏右         │
    │   (保守)    (恰到好处)    (激进)             │
    │   不足 ←──────── 中庸 ────────→ 过分         │
    │        叩其两端而用中                         │
    └─────────────────────────────────────────────┘

    核心方法:
    - evaluate_balance() - 评估decision平衡性
    - find_central_path() - 找到中正之路
    - detect_extremes() - 检测极端倾向
    - recommend_adjustment() - 调整建议
    """

    def __init__(self):
        """init中庸引擎"""
        self.name = "ZhongYongEngine"
        self.version = "v1.0.0"

        # 中庸核心语录
        self.zhongyong_quotes = {
            "中和": "喜怒哀乐之未发,谓之中;发而皆中节,谓之和.",
            "天命": "天命之谓性,率性之谓道,修道之谓教.",
            "至诚": "唯天下至诚,为能尽其性.",
            "高明": "极高明而道中庸.",
            "两端": "执其两端,用其中于民.",
            "明诚": "自明诚,谓之教.自诚明,谓之性.",
            "素位": "君子素其位而行,不愿乎其外.",
            "弗措": "人一能之,己百之;人十能之,己千之."
        }

        # 极端警示
        self.extreme_warnings = {
            "过分的仁": "妇人之仁,缺乏原则",
            "过分的义": "匹夫之勇,不顾大局",
            "过分的礼": "繁文缛节,本末倒置",
            "过分的智": "聪明反被聪明误",
            "过分的信": "匹夫匹妇,不顾轻重",
            "不及的仁": "冷漠无情,自私自利",
            "不及的义": "见利忘义,徇私枉法",
            "不及的礼": "粗鲁无礼,傲慢无状",
            "不及的智": "愚昧无知,是非不分",
            "不及的信": "言而无信,自食其言"
        }

    def evaluate_balance(self, options: List[Dict],
                        criteria: Optional[Dict[str, float]] = None) -> ZhongYongDecision:
        """
        评估选项的平衡性

        Args:
            options: 选项列表,每个选项包含:
                - name: 选项名称
                - risk_level: 风险等级(0-1)
                - return_level: 收益等级(0-1)
                - urgency: 紧迫程度(0-1)
                - resource_cost: 资源消耗(0-1)
            criteria: 评判标准权重

        Returns:
            ZhongYongDecision: 中庸decision结果
        """
        if not options:
            return ZhongYongDecision(
                balance_score=0.0,
                balance_state=BalanceState.BALANCED,
                extreme_risk=ExtremeType.NONE,
                recommendation="无选项可供评估",
                quote="",
                reasoning="缺少decision选项"
            )

        # 默认权重
        if criteria is None:
            criteria = {
                "risk_level": 0.3,
                "return_level": 0.3,
                "urgency": 0.2,
                "resource_cost": 0.2
            }

        # 计算每个选项的平衡分
        balance_scores = []
        for option in options:
            # 理想状态:风险适中,收益较高,不太紧迫,资源适中
            ideal_risk = 0.5
            ideal_return = 0.8
            ideal_urgency = 0.5
            ideal_cost = 0.4

            # 计算偏离程度
            risk_dev = abs(option.get("risk_level", 0.5) - ideal_risk)
            return_dev = abs(option.get("return_level", 0.5) - ideal_return)
            urgency_dev = abs(option.get("urgency", 0.5) - ideal_urgency)
            cost_dev = abs(option.get("resource_cost", 0.5) - ideal_cost)

            # synthesize平衡分(越低越好)
            total_dev = (
                risk_dev * criteria["risk_level"] +
                return_dev * criteria["return_level"] +
                urgency_dev * criteria["urgency"] +
                cost_dev * criteria["resource_cost"]
            )

            balance = 1.0 - total_dev
            balance_scores.append(balance)

        # 取最佳选项
        best_score = max(balance_scores)
        best_index = balance_scores.index(best_score)
        best_option = options[best_index]

        # judge平衡状态
        if best_score >= 0.8:
            state = BalanceState.BALANCED
        elif best_score >= 0.6:
            risk = best_option.get("risk_level", 0.5)
            state = BalanceState.SLIGHTLY_LEFT if risk < 0.5 else BalanceState.SLIGHTLY_RIGHT
        else:
            risk = best_option.get("risk_level", 0.5)
            state = BalanceState.TOO_LEFT if risk < 0.3 else BalanceState.TOO_RIGHT

        # 检测极端风险
        extreme = self._detect_extremes(best_option)

        # generate建议
        recommendation = self._recommend_adjustment(best_option, state)

        return ZhongYongDecision(
            balance_score=best_score,
            balance_state=state,
            extreme_risk=extreme,
            recommendation=recommendation,
            quote=self.zhongyong_quotes["两端"],
            reasoning=f"评估{best_option.get('name', '选项')}的风险{option.get('risk_level', 0.5):.1f},"
                     f"收益{best_option.get('return_level', 0.5):.1f},"
                     f"紧迫{best_option.get('urgency', 0.5):.1f},"
                     f"成本{best_option.get('resource_cost', 0.5):.1f}"
        )

    def _detect_extremes(self, option: Dict) -> ExtremeType:
        """检测极端风险"""
        risk = option.get("risk_level", 0.5)
        return_level = option.get("return_level", 0.5)

        # 过犹不及
        if risk > 0.8 or risk < 0.2:
            return ExtremeType.OVER
        if return_level > 0.9 or return_level < 0.2:
            return ExtremeType.OVER

        if 0.3 <= risk <= 0.7 and 0.4 <= return_level <= 0.8:
            return ExtremeType.NONE

        return ExtremeType.UNDER

    def _recommend_adjustment(self, option: Dict, state: BalanceState) -> str:
        """generate调整建议"""
        risk = option.get("risk_level", 0.5)
        cost = option.get("resource_cost", 0.5)

        if state == BalanceState.BALANCED:
            return "此选项恰到好处,可稳步执行"

        suggestions = []

        if state in [BalanceState.TOO_LEFT, BalanceState.SLIGHTLY_LEFT]:
            if risk < 0.4:
                suggestions.append("适当提高风险承受度,适度进取")
            if cost < 0.3:
                suggestions.append("增加必要投入,确保执行质量")

        if state in [BalanceState.TOO_RIGHT, BalanceState.SLIGHTLY_RIGHT]:
            if risk > 0.6:
                suggestions.append("适当降低风险,稳健为上")
            if cost > 0.6:
                suggestions.append("控制资源消耗,避免过度投入")

        if not suggestions:
            suggestions.append("微调至更平衡的状态")

        return ";".join(suggestions) + "."

    def find_central_path(self, start: Dict, end: Dict,
                          steps: int = 5) -> List[Dict]:
        """
        在两个极端之间找到中正之路

        Args:
            start: 起点(偏保守)
            end: 终点(偏激进)
            steps: 中间步数

        Returns:
            路径点列表
        """
        path = []

        for i in range(steps + 2):
            ratio = i / (steps + 1)
            point = {}

            for key in start.keys():
                if key in end:
                    # 线性插值
                    point[key] = start[key] * (1 - ratio) + end[key] * ratio

            # 添加中庸评注
            if ratio == 0:
                point["comment"] = "起点"
            elif ratio == 1:
                point["comment"] = "终点"
            else:
                point["comment"] = self._get_middle_comment(ratio)

            path.append(point)

        return path

    def _get_middle_comment(self, ratio: float) -> str:
        """根据位置给出评注"""
        if 0.4 <= ratio <= 0.6:
            return "中正之道"
        elif ratio < 0.3:
            return "偏起点"
        elif ratio > 0.7:
            return "偏终点"
        else:
            return "渐入佳境"

    def evaluate_action_extremes(self, action: str,
                                 context: Dict) -> Dict[str, Any]:
        """
        评估行为是否极端

        Args:
            action: 行为描述
            context: 上下文信息

        Returns:
            极端评估结果
        """
        action_lower = action.lower()
        result = {
            "action": action,
            "is_extreme": False,
            "extreme_type": None,
            "warning": "",
            "recommendation": "",
            "quote": ""
        }

        # 检测极端关键词
        extreme_keywords = {
            "过分": ["极端", "过度", "太过", "过分"],
            "不及": ["不够", "不足", "欠缺", "缺乏"]
        }

        for ext_type, keywords in extreme_keywords.items():
            if any(kw in action_lower for kw in keywords):
                result["is_extreme"] = True
                result["extreme_type"] = ext_type
                result["quote"] = self.zhongyong_quotes["两端"]
                break

        # generate警示和建议
        if result["is_extreme"]:
            if result["extreme_type"] == "过分":
                result["warning"] = "行为过于极端,有违中庸之道"
                result["recommendation"] = "执其两端,用其中于民"
            else:
                result["warning"] = "行为有所不足,未达中正"
                result["recommendation"] = "适度提升,恰到好处"

        return result

    def assess_situation_zhongyong(self, situation: Dict) -> Dict[str, Any]:
        """
        评估情境的中庸状态

        Args:
            situation: 情境描述

        Returns:
            中庸评估
        """
        # 简化的中庸评估
        score = 0.5
        factors = []

        situation_text = str(situation)

        # 正向因子
        if any(kw in situation_text for kw in ["平衡", "和谐", "适中", "中"]):
            score += 0.1
            factors.append("存在平衡因素")

        if any(kw in situation_text for kw in ["稳健", "保守", "谨慎"]):
            score -= 0.05  # 略偏左

        if any(kw in situation_text for kw in ["激进", "冒险", "积极"]):
            score += 0.05  # 略偏右

        # 极端因子
        if any(kw in situation_text for kw in ["极端", "过分", "过度"]):
            score = 0.3 if score > 0.5 else 0.7
            factors.append("存在极端倾向")

        # judge状态
        if score >= 0.6:
            state = "偏右" if score > 0.7 else "中正偏右"
        elif score <= 0.4:
            state = "偏左" if score < 0.3 else "中正偏左"
        else:
            state = "中正"

        return {
            "score": score,
            "state": state,
            "factors": factors,
            "quote": self.zhongyong_quotes["高明"],
            "advice": f"当前状态{state},宜{self._get_state_advice(state)}"
        }

    def _get_state_advice(self, state: str) -> str:
        """根据状态给出建议"""
        advice_map = {
            "偏左": "适度进取,不可过于保守",
            "中正偏左": "保持稳健,略加进取",
            "中正": "恰到好处,持中而行",
            "中正偏右": "保持积极,注意风险",
            "偏右": "稳健为上,不可过于激进"
        }
        return advice_map.get(state, "持中而行")

    def get_zhongyong_wisdom(self) -> Dict[str, str]:
        """get中庸智慧语录"""
        return self.zhongyong_quotes

# 全局实例
_zhongyong_engine: Optional[ZhongYongEngine] = None

def get_zhongyong_engine() -> ZhongYongEngine:
    """get中庸引擎实例"""
    global _zhongyong_engine
    if _zhongyong_engine is None:
        _zhongyong_engine = ZhongYongEngine()
    return _zhongyong_engine
