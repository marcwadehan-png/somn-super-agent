# -*- coding: utf-8 -*-
"""
风水环境认知模块 v1.0.0
Feng Shui Environment Engine

核心目标:
1. 用工程化方式表达风水中的环境结构judge
2. 将"藏风聚气,明堂,靠山,气口,动线,九宫"转成可解释metrics
3. 为办公,商业,居住等场景提供环境优化建议

版本:v1.0.0
更新:2026-04-02
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional

@dataclass
class FengShuiAssessment:
    """风水环境评估结果"""

    overall_score: float
    grade: str
    strengths: List[str]
    warnings: List[str]
    recommendations: List[str]
    nine_palace_focus: Dict[str, str]
    key_pattern: str

class FengShuiEnvironmentEngine:
    """风水环境引擎"""

    def __init__(self):
        self.orientation_elements = {
            "东": "木",
            "东南": "木",
            "南": "火",
            "西南": "土",
            "东北": "土",
            "西": "金",
            "西北": "金",
            "北": "水",
            "中央": "土",
        }
        self.nine_palace_meanings = {
            "坎一宫": "流动,信息,机会入口",
            "坤二宫": "承载,团队稳定,后勤",
            "震三宫": "启动,创新,项目推进",
            "巽四宫": "渗透,传播,合作网络",
            "中五宫": "统筹,中台,系统中枢",
            "乾六宫": "领导,decision,目标牵引",
            "兑七宫": "表达,销售,谈判",
            "艮八宫": "学习,沉淀,知识资产",
            "离九宫": "品牌,可见度,影响力",
        }

    def _to_score(self, value: Any, positive_words: List[str], negative_words: List[str], default: float = 0.5) -> float:
        if isinstance(value, bool):
            return 1.0 if value else 0.25
        if isinstance(value, (int, float)):
            return max(0.0, min(1.0, float(value)))
        if value is None:
            return default

        text = str(value)
        if any(word in text for word in positive_words):
            return 0.85
        if any(word in text for word in negative_words):
            return 0.25
        return default

    def analyze_layout(self, layout: Dict[str, Any]) -> Dict[str, Any]:
        """环境布局分析"""
        orientation = str(layout.get("orientation", "未知"))
        entrance = layout.get("entrance", "一般")
        backing = layout.get("backing", False)
        openness = layout.get("openness", "一般")
        lighting = layout.get("lighting", "一般")
        ventilation = layout.get("ventilation", "一般")
        clutter = layout.get("clutter", "一般")
        movement = layout.get("movement", "一般")
        water_feature = layout.get("water_feature", False)
        plants = layout.get("plants", False)

        scores = {
            "靠山": self._to_score(backing, ["稳", "有靠", "厚实"], ["空", "无靠", "背门"]),
            "明堂": self._to_score(openness, ["开阔", "明堂", "宽敞"], ["逼仄", "压迫", "狭窄"]),
            "采光": self._to_score(lighting, ["明亮", "通透", "自然光"], ["昏暗", "压抑", "阴沉"]),
            "通风": self._to_score(ventilation, ["通风", "流通", "清爽"], ["闷", "浊", "不流通"]),
            "整洁": 1.0 - self._to_score(clutter, ["杂乱", "堆积", "拥堵"], ["整洁", "清爽", "有序"], default=0.5),
            "动线": self._to_score(movement, ["顺畅", "回旋", "平稳"], ["冲撞", "穿堂", "直冲"]),
            "气口": self._to_score(entrance, ["明亮", "有缓冲", "整洁"], ["直冲", "狭窄", "杂乱"]),
            "生机": max(
                self._to_score(water_feature, ["活水", "循环", "清澈"], ["死水", "污浊", "干涸"], default=0.45),
                self._to_score(plants, ["绿植", "生机", "旺盛"], ["枯萎", "衰败"], default=0.45),
            ),
        }

        overall = round(sum(scores.values()) / len(scores), 3)
        if overall >= 0.82:
            grade = "上吉"
        elif overall >= 0.68:
            grade = "中吉"
        elif overall >= 0.52:
            grade = "平"
        else:
            grade = "待调整"

        strengths = [name for name, score in scores.items() if score >= 0.75]
        warnings = [name for name, score in scores.items() if score <= 0.4]

        recommendations: List[str] = []
        if "靠山" in warnings:
            recommendations.append("主位背后宜有实体支撑,减少背门,背窗或背过道带来的不稳感.")
        if "明堂" in warnings:
            recommendations.append("入口与主工作区前方要留出缓冲带,避免一进门即压迫或杂物堆积.")
        if "动线" in warnings or "气口" in warnings:
            recommendations.append("优化入口动线,避免穿堂直冲;宜让人流,信息流,decision流有回旋与停留.")
        if "采光" in warnings or "通风" in warnings:
            recommendations.append("优先改善采光和空气流动,环境气场先天不足时,效率与情绪都会被拖累.")
        if "整洁" in warnings:
            recommendations.append("减少堆积,特别是入口,走道,工位背后和会议区的长期杂物.")
        if "生机" in warnings:
            recommendations.append("可增加健康绿植或循环活水imagery,但重在清洁维护,不宜做成装饰性负担.")
        if not recommendations:
            recommendations.append("环境整体结构顺畅,下一步重点是按业务目标微调功能分区与主位朝向.")

        orientation_element = self._match_orientation_element(orientation)
        nine_palace_focus = self._build_nine_palace_focus(orientation_element)

        key_pattern = f"朝向偏{orientation},主气落在{orientation_element},当前环境以{nine_palace_focus[self._focus_palace(orientation_element)]}为主要发力方向."

        assessment = FengShuiAssessment(
            overall_score=overall,
            grade=grade,
            strengths=strengths or ["整体没有明显结构性硬伤"],
            warnings=warnings or ["暂无显著风水硬伤"],
            recommendations=recommendations,
            nine_palace_focus=nine_palace_focus,
            key_pattern=key_pattern,
        )
        return asdict(assessment)

    def analyze_business_space(self, business_type: str, layout: Dict[str, Any]) -> Dict[str, Any]:
        """面向商业场景的风水分析"""
        base = self.analyze_layout(layout)

        business_focus = {
            "零售": "离九宫与兑七宫优先,重展示,转化与客流停留.",
            "办公室": "乾六宫与中五宫优先,重decision效率与协作秩序.",
            "咨询": "艮八宫与巽四宫优先,重知识沉淀与关系网络.",
            "工厂": "坤二宫与震三宫优先,重承载,执行与生产动线.",
            "餐饮": "离九宫与坎一宫优先,重可见度,流量与体验节奏.",
        }

        base["business_type"] = business_type
        base["business_focus"] = business_focus.get(
            business_type,
            "先看入口与主位,再看展示/协作/交付三大区是否形成完整回路.",
        )
        return base

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """unified处理接口"""
        layout = input_data.get("environment") or input_data.get("layout") or input_data
        business_type = input_data.get("business_type")
        if business_type:
            return self.analyze_business_space(business_type, layout)
        return self.analyze_layout(layout)

    def _match_orientation_element(self, orientation: str) -> str:
        for key, element in self.orientation_elements.items():
            if key in orientation:
                return element
        return "土"

    def _focus_palace(self, element: str) -> str:
        mapping = {
            "木": "震三宫",
            "火": "离九宫",
            "土": "中五宫",
            "金": "乾六宫",
            "水": "坎一宫",
        }
        return mapping.get(element, "中五宫")

    def _build_nine_palace_focus(self, orientation_element: str) -> Dict[str, str]:
        focus_palace = self._focus_palace(orientation_element)
        return {
            palace: (
                f"重点激活:{meaning}" if palace == focus_palace else f"辅助观察:{meaning}"
            )
            for palace, meaning in self.nine_palace_meanings.items()
        }

_default_engine: Optional[FengShuiEnvironmentEngine] = None

def get_fengshui_environment_engine() -> FengShuiEnvironmentEngine:
    """get风水环境引擎单例"""
    global _default_engine
    if _default_engine is None:
        _default_engine = FengShuiEnvironmentEngine()
    return _default_engine

__all__ = [
    "FengShuiAssessment",
    "FengShuiEnvironmentEngine",
    "get_fengshui_environment_engine",
]
