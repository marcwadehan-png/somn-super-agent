# -*- coding: utf-8 -*-
"""
__all__ = [
    'assess_risk',
    'detect_change',
    'get_yi_change_manager',
    'get_yijing_wisdom',
    'manage_transition',
]

易变风险管理器 v1.0.0
=======================

基于<易经>变易之道的风险管理智慧系统

核心思想:
- <易经>:穷则变,变则通,通则久
- 阴阳之道:一阴一阳之谓道
- 居安思危:安而不忘危,治而不忘乱
- 革故鼎新:日新又新,与时俱进

版本:v1.0.0
更新:2026-04-02
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

class YinYang(Enum):
    """阴阳状态"""
    YIN = "阴"    # 阴柔,内向,保守
    YANG = "阳"   # 阳刚,外向,进取
    BALANCED = "平衡"

class ChangePhase(Enum):
    """变化阶段"""
    ZHOU = "潜"    # 潜龙勿用
    XIAN = "见"    # 见龙在田
    TENG = "惕"    # 君子终日乾乾
    YUE = "跃"     # 或跃在渊
    HONG = "飞"     # 飞龙在天
    KAN = "亢"     # 亢龙有悔

@dataclass
class YiRiskAssessment:
    """易变风险评估"""
    yin_yang_state: YinYang
    change_phase: ChangePhase
    risk_level: float           # 风险等级(0-1)
    opportunity_level: float    # 机会等级(0-1)
    current_situation: str      # 当前形势
    recommended_strategy: str   # 推荐strategy
    warnings: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)
    quote: str = ""
    yijing_hexagram: str = ""

class YiChangeManager:
    """
    易变风险管理器

    风险管理框架:
    ┌─────────────────────────────────────────────┐
    │              易经智慧体系                    │
    ├─────────────────────────────────────────────┤
    │  乾卦 → 天行健,君子以自强不息              │
    │  坤卦 → 地势坤,君子以厚德载物              │
    │  泰卦 → 天地交泰,否极泰来                  │
    │  革卦 → 革故鼎新,与时俱进                  │
    │  震卦 → 君子以恐惧修省                      │
    │  巽卦 → 君子以申命行事                      │
    └─────────────────────────────────────────────┘

    核心方法:
    - assess_risk() - 评估风险状态
    - detect_change() - 洞察变化征兆
    - recommend_strategy() - 推荐应对strategy
    - manage_transition() - 管理转型期
    """

    def __init__(self):
        """init易变管理器"""
        self.name = "YiChangeManager"
        self.version = "v1.0.0"

        # 易经核心思想
        self.yijing_principles = {
            "变易": {
                "quote": "穷则变,变则通,通则久.",
                "meaning": "事物发展到极点就会变化,变化才能通达,通达才能持久",
                "application": "当困境时寻求变化,当顺境时警惕变故"
            },
            "阴阳": {
                "quote": "一阴一阳之谓道.",
                "meaning": "阴阳交替变化是宇宙的根本规律",
                "application": "阴阳平衡,阳极生阴,阴极生阳"
            },
            "居安思危": {
                "quote": "安而不忘危,治而不忘乱.",
                "meaning": "安全时不忘危险,太平时不忘动乱",
                "application": "保持警惕,防患于未然"
            },
            "革故鼎新": {
                "quote": "革,去之也;鼎,取新也.",
                "meaning": "革除旧的,建立新的",
                "application": "与时俱进,适时变革"
            },
            "乾健": {
                "quote": "天行健,君子以自强不息.",
                "meaning": "天道刚健,君子应效法天道,不断自我强进",
                "application": "积极进取,永不停止"
            },
            "坤顺": {
                "quote": "地势坤,君子以厚德载物.",
                "meaning": "地道柔顺,君子应效法大地,厚德包容",
                "application": "包容宽厚,承载万物"
            }
        }

        # 八卦象征
        self.bagua_meanings = {
            "乾": {"nature": "天", "quality": "刚健", "advice": "进取"},
            "坤": {"nature": "地", "quality": "柔顺", "advice": "包容"},
            "震": {"nature": "雷", "quality": "震动", "advice": "警觉"},
            "巽": {"nature": "风", "quality": "入", "advice": "顺应"},
            "坎": {"nature": "水", "quality": "陷", "advice": "谨慎"},
            "离": {"nature": "火", "quality": "丽", "advice": "明理"},
            "艮": {"nature": "山", "quality": "止", "advice": "知止"},
            "兑": {"nature": "泽", "quality": "悦", "advice": "和众"}
        }

        # 乾卦六龙阶段
        self.qiagua_stages = {
            ChangePhase.ZHOU: {
                "description": "潜龙勿用",
                "meaning": "力量尚弱,不宜妄动",
                "advice": "潜心修炼,积累实力"
            },
            ChangePhase.XIAN: {
                "description": "见龙在田",
                "meaning": "崭露头角,初现锋芒",
                "advice": "展示才能,积累人脉"
            },
            ChangePhase.TENG: {
                "description": "君子终日乾乾",
                "meaning": "勤勉精进,小心谨慎",
                "advice": "加倍努力,警惕风险"
            },
            ChangePhase.YUE: {
                "description": "或跃在渊",
                "meaning": "跃跃欲试,进退抉择",
                "advice": "审时度势,灵活应变"
            },
            ChangePhase.HONG: {
                "description": "飞龙在天",
                "meaning": "功成名就,如日中天",
                "advice": "乘势而上,大展宏图"
            },
            ChangePhase.KAN: {
                "description": "亢龙有悔",
                "meaning": "物极必反,盛极而衰",
                "advice": "知足知止,戒骄戒躁"
            }
        }

    def assess_risk(self, situation: Dict) -> YiRiskAssessment:
        """
        评估风险状态

        Args:
            situation: 情境数据,包含:
                - stability: 稳定性(0-1)
                - momentum: 发展势头(0-1)
                - risk_signals: 风险信号列表
                - opportunity_signals: 机会信号列表

        Returns:
            YiRiskAssessment: 易变风险评估
        """
        stability = situation.get("stability", 0.5)
        momentum = situation.get("momentum", 0.5)
        risk_signals = situation.get("risk_signals", [])
        opportunity_signals = situation.get("opportunity_signals", [])

        # judge阴阳状态
        if stability > 0.7 and momentum > 0.7:
            yin_yang = YinYang.YANG
        elif stability < 0.3 and momentum < 0.3:
            yin_yang = YinYang.YIN
        else:
            yin_yang = YinYang.BALANCED

        # judge发展阶段
        phase = self._determine_phase(stability, momentum)

        # 计算风险等级
        risk_level = self._calculate_risk_level(
            stability, momentum, risk_signals
        )

        # 计算机会等级
        opportunity_level = self._calculate_opportunity_level(
            stability, momentum, opportunity_signals
        )

        # generate形势描述
        current_situation = self._describe_situation(
            yin_yang, phase, risk_level, opportunity_level
        )

        # 推荐strategy
        recommended_strategy = self._recommend_strategy(
            yin_yang, phase, risk_level, opportunity_level
        )

        # 警告和机会
        warnings = self._generate_warnings(phase, risk_signals)
        opportunities = self._generate_opportunities(phase, opportunity_signals)

        return YiRiskAssessment(
            yin_yang_state=yin_yang,
            change_phase=phase,
            risk_level=risk_level,
            opportunity_level=opportunity_level,
            current_situation=current_situation,
            recommended_strategy=recommended_strategy,
            warnings=warnings,
            opportunities=opportunities,
            quote=self.qiagua_stages[phase]["description"],
            yijing_hexagram=self._get_corresponding_hexagram(phase)
        )

    def _determine_phase(self, stability: float, momentum: float) -> ChangePhase:
        """judge发展阶段"""
        combined = (stability + momentum) / 2

        if combined < 0.2:
            return ChangePhase.ZHOU
        elif combined < 0.35:
            return ChangePhase.XIAN
        elif combined < 0.5:
            return ChangePhase.TENG
        elif combined < 0.65:
            return ChangePhase.YUE
        elif combined < 0.85:
            return ChangePhase.HONG
        else:
            return ChangePhase.KAN

    def _calculate_risk_level(self, stability: float, momentum: float,
                              risk_signals: List[str]) -> float:
        """计算风险等级"""
        base_risk = 1.0 - stability

        # 势头过强也增加风险
        if momentum > 0.8:
            base_risk += (momentum - 0.8) * 0.3

        # 风险信号
        signal_risk = min(0.3, len(risk_signals) * 0.05)

        return min(1.0, base_risk + signal_risk)

    def _calculate_opportunity_level(self, stability: float, momentum: float,
                                      opportunity_signals: List[str]) -> float:
        """计算机会等级"""
        base_opportunity = momentum * 0.6 + (1 - stability) * 0.4

        # 机会信号
        signal_opportunity = min(0.3, len(opportunity_signals) * 0.05)

        return min(1.0, base_opportunity + signal_opportunity)

    def _describe_situation(self, yin_yang: YinYang, phase: ChangePhase,
                           risk_level: float,
                           opportunity_level: float) -> str:
        """描述当前形势"""
        phase_desc = self.qiagua_stages[phase]["meaning"]

        yin_yang_desc = {
            YinYang.YANG: "阳气上升,",
            YinYang.YIN: "阴气凝聚,",
            YinYang.BALANCED: "阴阳平衡,"
        }.get(yin_yang, "")

        if risk_level > 0.7:
            risk_desc = "风险较高,"
        elif risk_level > 0.4:
            risk_desc = "风险中等,"
        else:
            risk_desc = "风险可控,"

        if opportunity_level > 0.7:
            opp_desc = "机会丰富"
        elif opportunity_level > 0.4:
            opp_desc = "机会一般"
        else:
            opp_desc = "机会有限"

        return f"{yin_yang_desc}{phase_desc},{risk_desc}{opp_desc}."

    def _recommend_strategy(self, yin_yang: YinYang, phase: ChangePhase,
                           risk_level: float,
                           opportunity_level: float) -> str:
        """推荐应对strategy"""
        base_strategy = self.qiagua_stages[phase]["advice"]

        if risk_level > 0.7:
            return f"{base_strategy},同时警惕风险"

        if opportunity_level > 0.7 and risk_level < 0.5:
            return f"{base_strategy},宜抓住机遇"

        return base_strategy

    def _generate_warnings(self, phase: ChangePhase,
                          risk_signals: List[str]) -> List[str]:
        """generate警示"""
        warnings = []

        # 阶段警告
        if phase == ChangePhase.KAN:
            warnings.append("⚠️ 亢龙有悔:盛极必反,宜知足知止")

        if phase == ChangePhase.ZHOU:
            warnings.append("⚠️ 潜龙勿用:力量尚弱,不宜冒进")

        if phase == ChangePhase.TENG:
            warnings.append("⚠️ 终日乾乾:需保持警惕,不可松懈")

        # 风险信号警告
        risk_keywords = {
            "市场": "市场风险积聚",
            "竞争": "竞争压力加大",
            "资金": "资金链可能紧张",
            "政策": "政策风险上升",
            "技术": "技术更新换代"
        }

        for signal in risk_signals:
            for keyword, warning in risk_keywords.items():
                if keyword in signal:
                    warnings.append(f"⚠️ {warning}")
                    break

        return warnings if warnings else ["✅ 当前风险可控"]

    def _generate_opportunities(self, phase: ChangePhase,
                               opportunity_signals: List[str]) -> List[str]:
        """generate机会"""
        opportunities = []

        # 阶段机会
        if phase == ChangePhase.XIAN:
            opportunities.append("🌱 见龙在田:新机会初现,宜积极布局")

        if phase == ChangePhase.YUE:
            opportunities.append("🌟 或跃在渊:突破在即,宜果断action")

        if phase == ChangePhase.HONG:
            opportunities.append("☀️ 飞龙在天:如日中天,宜乘势而上")

        # 机会信号
        for signal in opportunity_signals:
            opportunities.append(f"✨ 把握{signal}")

        return opportunities

    def _get_corresponding_hexagram(self, phase: ChangePhase) -> str:
        """get对应的卦象"""
        hexagram_map = {
            ChangePhase.ZHOU: "乾卦初九",
            ChangePhase.XIAN: "乾卦九二",
            ChangePhase.TENG: "乾卦九三",
            ChangePhase.YUE: "乾卦九四",
            ChangePhase.HONG: "乾卦九五",
            ChangePhase.KAN: "乾卦上九"
        }
        return hexagram_map.get(phase, "乾卦")

    def detect_change(self, historical_data: List[Dict]) -> Dict[str, Any]:
        """
        洞察变化征兆

        Args:
            historical_data: 历史数据列表

        Returns:
            变化分析结果
        """
        if len(historical_data) < 2:
            return {
                "trend": "数据不足",
                "change_detected": False,
                "quote": "需积累更多数据以洞察变化"
            }

        # 分析趋势
        first = historical_data[0]
        last = historical_data[-1]

        # 计算变化
        stability_change = last.get("stability", 0.5) - first.get("stability", 0.5)
        momentum_change = last.get("momentum", 0.5) - first.get("momentum", 0.5)

        # judge趋势
        if stability_change > 0.2 and momentum_change > 0.2:
            trend = "向好"
            change_detected = True
            interpretation = "形势大好,宜乘势而上"
        elif stability_change < -0.2 and momentum_change < -0.2:
            trend = "向坏"
            change_detected = True
            interpretation = "形势严峻,需警惕应对"
        elif stability_change > 0.2:
            trend = "趋稳"
            change_detected = True
            interpretation = "稳定性增强,但需注意僵化"
        elif stability_change < -0.2:
            trend = "动荡"
            change_detected = True
            interpretation = "变化加剧,需灵活应对"
        elif momentum_change > 0.2:
            trend = "加速"
            change_detected = True
            interpretation = "势头增强,宜抓住机遇"
        elif momentum_change < -0.2:
            trend = "减速"
            change_detected = True
            interpretation = "势头减弱,需积蓄力量"
        else:
            trend = "平稳"
            change_detected = False
            interpretation = "暂无明显变化"

        return {
            "trend": trend,
            "change_detected": change_detected,
            "stability_change": stability_change,
            "momentum_change": momentum_change,
            "interpretation": interpretation,
            "quote": self.yijing_principles["变易"]["quote"]
        }

    def manage_transition(self, current_phase: ChangePhase,
                          target_phase: ChangePhase) -> Dict[str, Any]:
        """
        管理转型期

        Args:
            current_phase: 当前阶段
            target_phase: 目标阶段

        Returns:
            转型指导
        """
        transitions = {
            (ChangePhase.ZHOU, ChangePhase.XIAN): {
                "strategy": "韬光养晦,积极准备",
                "actions": ["积累实力", "展示才能", "建立人脉"],
                "warning": "不可急躁冒进"
            },
            (ChangePhase.XIAN, ChangePhase.TENG): {
                "strategy": "勤勉精进,保持警惕",
                "actions": ["加倍努力", "持续学习", "防范风险"],
                "warning": "不可骄傲自满"
            },
            (ChangePhase.TENG, ChangePhase.YUE): {
                "strategy": "审时度势,灵活抉择",
                "actions": ["评估形势", "准备突破", "设定目标"],
                "warning": "需权衡利弊得失"
            },
            (ChangePhase.YUE, ChangePhase.HONG): {
                "strategy": "果断action,乘势而上",
                "actions": ["抓住机遇", "大胆decision", "资源倾斜"],
                "warning": "保持适度谨慎"
            },
            (ChangePhase.HONG, ChangePhase.KAN): {
                "strategy": "知足知止,居安思危",
                "actions": ["控制规模", "防范风险", "准备转型"],
                "warning": "亢龙有悔,宜急流勇退"
            }
        }

        transition = transitions.get(
            (current_phase, target_phase),
            {
                "strategy": "顺势而为",
                "actions": ["观察形势", "做好准备"],
                "warning": "具体情况具体分析"
            }
        )

        return {
            "from_phase": current_phase.value,
            "to_phase": target_phase.value,
            "strategy": transition["strategy"],
            "actions": transition["actions"],
            "warning": transition["warning"],
            "quote": "穷则变,变则通,通则久"
        }

    def get_yijing_wisdom(self) -> Dict[str, str]:
        """get易经智慧"""
        return self.yijing_principles

# 全局实例
_yi_change_manager: Optional[YiChangeManager] = None

def get_yi_change_manager() -> YiChangeManager:
    """get易变管理器实例"""
    global _yi_change_manager
    if _yi_change_manager is None:
        _yi_change_manager = YiChangeManager()
    return _yi_change_manager
