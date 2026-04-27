# -*- coding: utf-8 -*-
"""
鬼谷子 Cloning - Tier 1 核心独立Cloning

鬼谷子（约前400-前320），纵横家鼻祖。
核心思想：捭阖之道、揣摩之术、飞钳之术、反应之术。
"""

from typing import Dict, List, Optional, Any

from .._cloning_base import SageCloning
from .._cloning_types import (
    AnalysisResult, DecisionResult, SageProfile, CloningTier,
)


class GuiGuZiCloning(SageCloning):
    """鬼谷子Cloning - 厂卫指挥使"""

    def __init__(self):
        profile = SageProfile(
            name="鬼谷子",
            name_en="Gui Gu Zi",
            era="战国中期",
            years="约前400-前320",
            school="纵横家",
            tier=CloningTier.TIER1_CORE,
            position="厂卫指挥使",
            department="厂卫",
            title="纵横家鼻祖·隐士大师",
            biography="战国时期隐居鬼谷的神秘人物，苏秦、张仪、孙膑、庞涓皆出其门下。精通捭阖、揣摩、飞钳、反应等游说与谋略之术，是中国古代最全面的战略思想家之一。",
            core_works=["《鬼谷子》"],
            capability={
                "strategic_vision": 10, "execution": 8, "innovation": 10,
                "leadership": 8, "influence": 9, "cross_domain": 10,
            },
        )
        super().__init__(profile)
        self._wisdom_laws = [
            "捭阖之道 —— 开合有度，言语是打开和关闭人心的钥匙",
            "揣摩之术 —— 洞察对方真实意图，揣其情而摩其意",
            "飞钳之术 —— 先赞扬后控制，以赞美引出真话",
            "与世沉浮 —— 因人因时因地制宜，没有万能的方法",
            "见微知著 —— 从细微处推断全局，从已知推未知",
        ]
        self._methodologies = [
            "捭阖分析法 —— 从开放和闭合两个维度分析局势",
            "揣情摩意法 —— 通过非语言信息推断真实意图",
            "反应法 —— 以反求复，用对方的反应来验证推测",
            "量权法 —— 衡量各方实力对比，找到最优策略",
        ]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        context = context or {}

        if any(w in problem for w in ["谈判", "沟通", "说服", "博弈"]):
            perspective = "从'捭阖揣摩'的沟通博弈术出发"
            insight = ("谈判的本质是心理博弈。'捭'是让对方敞开心扉，'阖'是让对方收敛防线。"
                      "关键不是你说什么，而是让对方说出什么。")
            recs = [
                "先倾听后发言——'阖'以探虚实",
                "找到对方的真实需求——'揣情'",
                "用对方能接受的方式表达——'摩意'",
                "准备多套话术——开口前已经预判了所有走向",
            ]
        elif any(w in problem for w in ["情报", "分析", "调查", "竞争"]):
            perspective = "从'见微知著'的情报分析出发"
            insight = ("信息的不对称是博弈的核心。收集信息、分析信息、利用信息——"
                      "这是纵横家的基本功。")
            recs = [
                "从公开信息推断隐秘信息——'反应'之法",
                "交叉验证多个信息源",
                "分析对手的'言外之意'和'弦外之音'",
                "建立情报网络——'与世沉浮'需要信息支撑",
            ]
        else:
            perspective = "从纵横家的全局谋略出发"
            insight = ("任何问题都可以转化为'人'的问题。"
                      "理解人、影响人、联合人、分化敌人——这就是纵横之术。")
            recs = [
                "捭阖——先判断是该'开'(主动)还是'阖'(被动)",
                "揣摩——推断各方真实意图",
                "飞钳——先用肯定获取信任，再用引导施加影响",
                "量权——计算各方实力和利益，找到最优路径",
            ]

        return AnalysisResult(
            sage_name="鬼谷子",
            school="纵横家",
            problem=problem,
            perspective=perspective,
            core_insight=insight,
            wisdom_laws_applied=self._wisdom_laws[:3],
            recommendations=recs,
            warnings=["纵横之术可用不可恃，需以道德为底线"],
            confidence=0.89,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        scored_options = []
        for opt in options:
            score = 7.0
            reasons = []
            if any(w in opt for w in ["灵活", "应变", "策略", "计谋"]):
                score += 2.0
                reasons.append("纵横之道在于应变无穷")
            if any(w in opt for w in ["联盟", "合作", "联合"]):
                score += 1.5
                reasons.append("合纵连横，联合则强")
            if any(w in opt for w in ["分化", "离间", "瓦解"]):
                score += 1.0
                reasons.append("分化对手是纵横家常用手段")
            if any(w in opt for w in ["正面对抗", "硬碰硬", "直接"]):
                score -= 1.5
                reasons.append("直来直去非纵横之道")
            scored_options.append((opt, score, "; ".join(reasons)))

        scored_options.sort(key=lambda x: x[1], reverse=True)
        chosen = scored_options[0]
        return DecisionResult(
            sage_name="鬼谷子",
            problem=context.get("problem", ""),
            chosen_option=chosen[0],
            reasoning=f"纵横家评估：{chosen[2]}",
            alternatives_considered=[o[0] for o in scored_options[1:]],
            wisdom_laws_applied=["捭阖之道", "揣摩之术", "与世沉浮"],
            confidence=chosen[1] / 10.0,
        )

    def advise(self, context: Dict[str, Any]) -> str:
        return (
            "鬼谷子曰：'与贵者言，依于势；与贫者言，依于利；"
            "与勇者言，依于敢；与愚者言，依于锐。' "
            "沟通必须因人而异。先了解对方是什么样的人，"
            "然后用对方最在意的方式去沟通。"
            "记住：'口者，心之门户也。' 控制了言辞，就控制了人心。"
        )
__all__ = ['GuiGuZiCloning']
