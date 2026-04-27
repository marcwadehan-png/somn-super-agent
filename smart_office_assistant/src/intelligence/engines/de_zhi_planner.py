# -*- coding: utf-8 -*-
"""
__all__ = [
    'assess_governance',
    'evaluate_ruler',
    'get_de_zhi_planner',
    'get_strategy_plan',
    'plan_strategy',
    'select_talent',
]

德治战略规划器 v1.0.0
=======================

战略规划系统

核心思想:
- <尚书>:皇天无亲,唯德是辅
- 德治:任贤使能,以德服人
- 民本:民之所欲,天必从之
- 明德:黾勉求之,迪上哲

版本:v1.0.0
更新:2026-04-02
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

class GovernanceLevel(Enum):
    """治理层级"""
    德治 = "德治"        # 以德治国
    法治 = "法治"        # 以法治国
    礼治 = "礼治"        # 以礼治国
    人治 = "人治"        # 以人治国

class StrategyType(Enum):
    """战略类型"""
    任贤 = "任贤"        # 任用贤能
    明德 = "明德"        # 彰显德性
    惠民 = "惠民"        # 惠及百姓
    修身 = "修身"        # 修身正己

@dataclass
class DeZhiStrategy:
    """德治战略"""
    strategy_type: StrategyType
    title: str           # 战略标题
    description: str      # 战略描述
    core_principle: str   # 核心原则
    key_actions: List[str] = field(default_factory=list)
    expected_outcome: str = ""
    warning: str = ""
    quote: str = ""

class DeZhiPlanner:
    """
    德治战略规划器

    战略框架:
    ┌─────────────────────────────────────────────┐
    │              德治战略体系                    │
    ├─────────────────────────────────────────────┤
    │  任贤使能 → 德才兼备,人尽其才              │
    │  明德慎罚 → 彰显德性,教育为主              │
    │  惠民安民 → 以民为本,天下为公              │
    │  修身正己 → 正人先正己,率先垂范            │
    └─────────────────────────────────────────────┘

    核心方法:
    - plan_strategy() - 规划德治战略
    - evaluate_ruler() - 评估治理者德性
    - select_talent() - 选拔德才兼备之人
    - assess_governance() - 评估治理效果
    """

    def __init__(self):
        """init德治规划器"""
        self.name = "DeZhiPlanner"
        self.version = "v1.0.0"

        # 尚书德治核心思想
        self.de_zhi_principles = {
            "德治本质": {
                "quote": "皇天无亲,唯德是辅.",
                "meaning": "上天公正无私,只辅助有德之人",
                "application": "领导者应以德服人,而非以力服人"
            },
            "任贤": {
                "quote": "任官惟贤材,左右惟其人.",
                "meaning": "任命官员只选贤能,身边人也要选贤才",
                "application": "广开才路,任人唯贤"
            },
            "明德": {
                "quote": "黾勉求之,迪上哲,维民其康.",
                "meaning": "勤勉追求德治之道,引导人民走向安康",
                "application": "以德教化,率先垂范"
            },
            "慎刑": {
                "quote": "罪疑惟轻,功疑惟重.",
                "meaning": "罪行有疑则从轻论处,功劳有疑则从重奖赏",
                "application": "德主刑辅,慎用刑罚"
            },
            "民本": {
                "quote": "民之所欲,天必从之.",
                "meaning": "百姓的愿望,上天必定顺从",
                "application": "以民为本,顺应民意"
            }
        }

        # 德治战略模板
        self.strategy_templates = {
            "任贤": {
                "核心": "任贤使能",
                "方法": [
                    "建立贤才recognize机制",
                    "德才兼备,以德为先",
                    "任人唯贤,不拘一格",
                    "容才之量,用人之长"
                ],
                "quote": "外举不弃仇,内举不失亲."
            },
            "明德": {
                "核心": "明德慎罚",
                "方法": [
                    "以德教化为先",
                    "身教重于言教",
                    "表彰道德典范",
                    "慎用刑罚惩罚"
                ],
                "quote": "道之以德,齐之以礼,有耻且格."
            },
            "惠民": {
                "核心": "以民为本",
                "方法": [
                    "了解民众疾苦",
                    "倾听民众呼声",
                    "解决民生问题",
                    "共享发展成果"
                ],
                "quote": "民为邦本,本固邦宁."
            },
            "修身": {
                "核心": "正人正己",
                "方法": [
                    "先正己后正人",
                    "率先垂范",
                    "修身齐家治国",
                    "内圣外王之道"
                ],
                "quote": "其身正,不令而行;其身不正,虽令不从."
            }
        }

        # 德治评估维度
        self.evaluation_dimensions = {
            "德性": {
                "weight": 0.3,
                "indicators": ["仁爱", "公正", "诚信", "勤勉"]
            },
            "才能": {
                "weight": 0.25,
                "indicators": ["学识", "能力", "经验", "魄力"]
            },
            "治理": {
                "weight": 0.25,
                "indicators": ["decision", "执行", "协调", "创新"]
            },
            "民心": {
                "weight": 0.2,
                "indicators": ["信任", "满意", "支持", "拥护"]
            }
        }

    def plan_strategy(self, situation: Dict,
                     goal: str) -> DeZhiStrategy:
        """
        规划德治战略

        Args:
            situation: 当前形势
            goal: 战略目标

        Returns:
            DeZhiStrategy: 德治战略
        """
        situation_text = str(situation)
        goal_text = str(goal)

        # 分析形势,确定战略类型
        if any(kw in goal_text for kw in ["人才", "团队", "干部"]):
            strategy_type = StrategyType.任贤
        elif any(kw in situation_text for kw in ["道德", "文化", "风气"]):
            strategy_type = StrategyType.明德
        elif any(kw in situation_text for kw in ["民生", "员工", "客户"]):
            strategy_type = StrategyType.惠民
        else:
            strategy_type = StrategyType.修身

        template = self.strategy_templates[strategy_type.value]

        return DeZhiStrategy(
            strategy_type=strategy_type,
            title=f"{template['核心']}战略",
            description=f"basis{template['核心']}制定战略规划",
            core_principle=template["核心"],
            key_actions=template["方法"],
            expected_outcome=f"实现{goal}",
            warning="德治需持之以恒,不可急功近利",
            quote=template["quote"]
        )

    def evaluate_ruler(self, ruler_data: Dict) -> Dict[str, Any]:
        """
        评估治理者的德性

        Args:
            ruler_data: 治理者数据

        Returns:
            德性评估结果
        """
        scores = {}

        for dimension, info in self.evaluation_dimensions.items():
            dimension_score = 0.0
            for indicator in info["indicators"]:
                if ruler_data.get(indicator, False):
                    dimension_score += 1.0 / len(info["indicators"])

            scores[dimension] = {
                "score": dimension_score,
                "weight": info["weight"],
                "weighted_score": dimension_score * info["weight"]
            }

        total_score = sum(s["weighted_score"] for s in scores.values())

        # 判定等级
        if total_score >= 0.85:
            level = "圣主"
            description = "德才兼备,圣人之治"
        elif total_score >= 0.75:
            level = "明主"
            description = "德高望重,明智之治"
        elif total_score >= 0.6:
            level = "庸主"
            description = "德才中等,尚需努力"
        else:
            level = "昏主"
            description = "德薄才寡,宜先修身"

        return {
            "scores": scores,
            "total_score": total_score,
            "level": level,
            "description": description,
            "suggestions": self._generate_ruler_suggestions(scores),
            "quote": self.de_zhi_principles["德治本质"]["quote"]
        }

    def _generate_ruler_suggestions(self, scores: Dict) -> List[str]:
        """generate治理者建议"""
        suggestions = []

        for dimension, score_info in scores.items():
            if score_info["score"] < 0.6:
                suggestions.append(
                    f"加强{dimension}:当前分数{score_info['score']:.2f},"
                    f"建议重点提升{','.join(self.evaluation_dimensions[dimension]['indicators'][:2])}"
                )

        if not suggestions:
            suggestions.append("继续保持德治修行,精益求精")

        return suggestions

    def select_talent(self, candidates: List[Dict],
                     criteria: Optional[Dict] = None) -> List[Dict]:
        """
        选拔德才兼备的人才

        Args:
            candidates: 候选人列表
            criteria: 选拔标准

        Returns:
            排序后的人才列表
        """
        if criteria is None:
            criteria = {
                "德": 0.6,  # 德才比例 6:4
                "才": 0.4
            }

        rated_candidates = []

        for candidate in candidates:
            # 德性评估
            de_score = self._assess_de(candidate)

            # 才能评估
            cai_score = self._assess_cai(candidate)

            # synthesize评分
            total_score = (
                de_score * criteria["德"] +
                cai_score * criteria["才"]
            )

            rated_candidates.append({
                **candidate,
                "de_score": de_score,
                "cai_score": cai_score,
                "total_score": total_score,
                "ranking": None,
                "recommendation": self._get_talent_recommendation(de_score, cai_score)
            })

        # 排序
        rated_candidates.sort(key=lambda x: x["total_score"], reverse=True)

        # 添加排名
        for i, candidate in enumerate(rated_candidates):
            candidate["ranking"] = i + 1

        return rated_candidates

    def _assess_de(self, candidate: Dict) -> float:
        """评估德性"""
        de_traits = ["仁爱", "诚信", "公正", "勤勉", "谦逊"]
        score = 0.5

        for trait in de_traits:
            if candidate.get(trait, False):
                score += 0.1

        return min(1.0, score)

    def _assess_cai(self, candidate: Dict) -> float:
        """评估才能"""
        cai_traits = ["学识", "能力", "经验", "魄力", "创新"]
        score = 0.5

        for trait in cai_traits:
            if candidate.get(trait, False):
                score += 0.1

        return min(1.0, score)

    def _get_talent_recommendation(self, de_score: float,
                                   cai_score: float) -> str:
        """get人才使用建议"""
        if de_score >= 0.8 and cai_score >= 0.8:
            return "堪当大任,可委以重任"
        elif de_score >= 0.8 and cai_score >= 0.5:
            return "德才兼备,宜重点培养"
        elif de_score >= 0.6 and cai_score >= 0.8:
            return "才能出众,需加强品德引导"
        elif de_score >= 0.5 and cai_score >= 0.5:
            return "基本合格,可放在合适岗位"
        else:
            return "尚需修炼,不宜重用"

    def assess_governance(self, governance_data: Dict) -> Dict[str, Any]:
        """
        评估治理效果

        Args:
            governance_data: 治理数据

        Returns:
            治理评估结果
        """
        # 计算各维度得分
        moral_score = governance_data.get("道德风气", 0.5)
        talent_score = governance_data.get("人才状况", 0.5)
        people_score = governance_data.get("民心所向", 0.5)
        order_score = governance_data.get("社会秩序", 0.5)

        # synthesize评分
        total_score = (moral_score * 0.3 + talent_score * 0.2 +
                       people_score * 0.3 + order_score * 0.2)

        # 判定治理等级
        if total_score >= 0.85:
            level = "上治"
            advice = "德治成效显著,宜守成持正"
        elif total_score >= 0.7:
            level = "中治"
            advice = "治理基本良好,尚有提升空间"
        elif total_score >= 0.5:
            level = "下治"
            advice = "治理存在问题,需要改进"
        else:
            level = "乱世"
            advice = "治理失效,需要深刻变革"

        return {
            "scores": {
                "道德风气": moral_score,
                "人才状况": talent_score,
                "民心所向": people_score,
                "社会秩序": order_score
            },
            "total_score": total_score,
            "level": level,
            "advice": advice,
            "quote": "为政以德,譬如北辰,居其所而众星共之."
        }

    def get_strategy_plan(self, context: Dict) -> Dict[str, Any]:
        """
        get完整战略规划

        Args:
            context: 战略上下文

        Returns:
            完整战略规划
        """
        situation = context.get("situation", "")
        goal = context.get("goal", "")
        resources = context.get("resources", {})
        constraints = context.get("constraints", {})

        # generate四大战略
        strategies = {
            "任贤战略": self._generate_strategy(StrategyType.任贤, situation, goal),
            "明德战略": self._generate_strategy(StrategyType.明德, situation, goal),
            "惠民战略": self._generate_strategy(StrategyType.惠民, situation, goal),
            "修身战略": self._generate_strategy(StrategyType.修身, situation, goal)
        }

        # 选择最佳战略
        recommended = self.plan_strategy(situation, goal)

        return {
            "context": context,
            "all_strategies": strategies,
            "recommended": recommended,
            "quote": "皇天无亲,唯德是辅",
            "advice": self._generate_strategic_advice(recommended)
        }

    def _generate_strategy(self, strategy_type: StrategyType,
                          situation: str, goal: str) -> Dict[str, Any]:
        """generate特定战略"""
        template = self.strategy_templates[strategy_type.value]

        return {
            "type": strategy_type.value,
            "title": template["核心"],
            "actions": template["方法"],
            "quote": template["quote"]
        }

    def _generate_strategic_advice(self, strategy: DeZhiStrategy) -> str:
        """generate战略建议"""
        advice_map = {
            StrategyType.任贤: "任贤使能,广开才路,以德为先",
            StrategyType.明德: "以德服人,身教重于言教",
            StrategyType.惠民: "以民为本,顺应民意,共享成果",
            StrategyType.修身: "正人先正己,修身为本"
        }

        return advice_map.get(strategy.strategy_type, "")

# 全局实例
_de_zhi_planner: Optional[DeZhiPlanner] = None

def get_de_zhi_planner() -> DeZhiPlanner:
    """get德治规划器实例"""
    global _de_zhi_planner
    if _de_zhi_planner is None:
        _de_zhi_planner = DeZhiPlanner()
    return _de_zhi_planner
