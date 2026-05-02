# -*- coding: utf-8 -*-
"""
__all__ = [
    'daily_practice',
    'judge_with_liangzhi',
    'liangzhi_test',
    'quick_decide',
    'quick_judge',
    'quick_test',
    'remove_private_desires',
    'value_decision',
]

王阳明良知decision系统 - Yangming Liangzhi (Conscience-Informed) Decision System
v8.1.0 版本

深化王阳明xinxue"致良知"的decision层面,构建:
1. 良知judge引擎 - 内在的是非之心
2. 良知检验框架 - 做决定前的四问
3. 去私欲系统 - 消除私欲对良知的遮蔽
4. 价值decisionfusion - 良知与现代decisionfusion
5. 日常修身指导 - 良知持续光明

[良知四心]
1. 是非之心 - 知道什么是对,什么是错
2. 羞恶之心 - 对错误的羞耻和厌恶
3. 恻隐之心 - 对他人苦难的同情
4. 恭敬之心 - 对他人和规则的尊重

[致良知方法]
1. 内省 - 每天反思自己的行为
2. 事上练 - 在具体事情上检验良知
3. 去私欲 - 去除遮蔽良知的人欲
4. 不动心 - 在困境中保持良知

版本历史:
- v8.1.0 (2026-04-03): 深化良知decision系统,构建价值judge引擎
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

class LiangzhiHeart(Enum):
    """良知四心"""
    RIGHT_WRONG = "是非之心"      # 知道对错
    SHAME_DISLIKE = "羞恶之心"   # 对错的羞耻厌恶
    COMPASSION = "恻隐之心"      # 对苦难的同情
    RESPECT = "恭敬之心"         # 对规则尊重

class PrivateDesire(Enum):
    """私欲类型"""
    MATERIAL = "物欲"             # 对物质的过度追求
    FAME = "名欲"                 # 对名利的追求
    PLEASURE = "逸欲"             # 对享乐的追求
    CONTROL = "权欲"              # 对控制的追求
    APPROVAL = "认可欲"           # 对他人认可的过度追求
    AVOIDANCE = "逃避欲"          # 逃避责任的欲望

@dataclass
class ConscienceJudgment:
    """良知judge"""
    heart_type: LiangzhiHeart
    judgment: str
    reasoning: str
    confidence: float
    is_liangzhi_clear: bool
    evidence_for: List[str] = field(default_factory=list)
    evidence_against: List[str] = field(default_factory=list)
    quote: str = ""

@dataclass
class LiangzhiTest:
    """良知检验"""
    situation: str
    four_questions: List[Dict] = field(default_factory=list)
    conscience_answer: str = ""
    selfish_obstruction: List[str] = field(default_factory=list)
    recommended_action: str = ""
    heart_check_result: str = ""
    quote: str = ""

@dataclass
class DesiresAnalysis:
    """私欲分析"""
    dominant_desire: Optional[PrivateDesire]
    desire_strength: float
    obstructions: List[Dict] = field(default_factory=list)
    removal_methods: List[str] = field(default_factory=list)
    progress_indicator: str = ""
    quote: str = ""

@dataclass
class ValueDecision:
    """价值decision"""
    situation: str
    options: List[str]
    conscience_rankings: List[Dict] = field(default_factory=list)
    best_option: str = ""
    reasoning: str = ""
    long_term_view: str = ""
    quote: str = ""

@dataclass
class DailyPractice:
    """日常修身"""
    morning_practice: Dict = field(default_factory=dict)
    midday_practice: Dict = field(default_factory=dict)
    evening_practice: Dict = field(default_factory=dict)
    weekly_review: List[str] = field(default_factory=list)
    monthly_breakthrough: str = ""
    quote: str = ""

class LiangzhiDecisionSystem:
    """
    王阳明良知decision系统
    
    核心功能:
    1. 良知judge - 内在是非之心
    2. 良知检验 - decision前四问
    3. 去私欲 - 消除私欲遮蔽
    4. 价值decision - 良知与现代decisionfusion
    5. 日常修身 - 良知持续光明
    """
    
    LIANGZHI_QUOTES = {
        "良知本质": [
            "良知是,人人本有,不待学而后能.",
            "良知之外,更无知;致知之外,更无学.",
            "人胸中各有个圣人,只因自信不及,都自埋倒了."
        ],
        "致良知": [
            "致吾心之良知于事事物物,则事事物物皆得其理.",
            "致良知是学问大头脑,是圣人教人第一义."
        ],
        "去私欲": [
            "去人欲,存天理.",
            "克己须要扫除廊清,一毫不存方是."
        ],
        "事上练": [
            "人须在事上磨,方立得住."
        ]
    }
    
    LIANGZHI_HEARTS = {
        LiangzhiHeart.RIGHT_WRONG: {
            "description": "知道什么是对,什么是错",
            "核心问题": "这件事是对还是错?",
            "问法": "如果是圣人(你最敬佩的人),会如何judge?"
        },
        LiangzhiHeart.SHAME_DISLIKE: {
            "description": "对错误的羞耻和厌恶",
            "核心问题": "我做这件事会感到羞耻吗?",
            "问法": "如果公开这件事,我会感到羞耻吗?"
        },
        LiangzhiHeart.COMPASSION: {
            "description": "对他人苦难的同情",
            "核心问题": "这个决定会伤害他人吗?",
            "问法": "如果我是受影响的人,我会怎么想?"
        },
        LiangzhiHeart.RESPECT: {
            "description": "对他人和规则的尊重",
            "核心问题": "这个决定尊重规则和他人吗?",
            "问法": "这个决定符合道德规范吗?"
        }
    }
    
    PRIVATE_DESIRES = {
        PrivateDesire.MATERIAL: {
            "description": "对物质的过度追求",
            "manifestation": "金钱,房产,物品的过度追求",
            "removal": [
                "1. 知足:知道什么是足够的",
                "2. 简化:减少对物质的依赖",
                "3. 分享:学会给予而非只知get",
                "4. 内在富足:发现内心本有的富足"
            ]
        },
        PrivateDesire.FAME: {
            "description": "对名利的追求",
            "manifestation": "名声,地位,荣誉的过度追求",
            "removal": [
                "1. 看淡名声:名声是外在的,不可控",
                "2. 内在价值:建立不依赖外在评价的自我价值",
                "3. 专注本质:关注做事本身,而非名声",
                "4. 淡泊名利:追求卓越而非追求名声"
            ]
        },
        PrivateDesire.PLEASURE: {
            "description": "对享乐的追求",
            "manifestation": "安逸,舒适,娱乐的过度追求",
            "removal": [
                "1. 延迟满足:学会等待和忍耐",
                "2. 承担痛苦:成长需要走出舒适区",
                "3. 意义导向:追求有意义的快乐",
                "4. 平衡生活:享受但不沉迷"
            ]
        },
        PrivateDesire.APPROVAL: {
            "description": "对他人认可的过度追求",
            "manifestation": "渴望被喜欢,被认可,被赞扬",
            "removal": [
                "1. 内在认可:寻求自我认可而非外在认可",
                "2. 接受批评:批评是成长的机会",
                "3. 独立judge:有自己的价值观,不随波逐流",
                "4. 被讨厌的勇气:不必让所有人喜欢"
            ]
        },
        PrivateDesire.AVOIDANCE: {
            "description": "逃避责任的欲望",
            "manifestation": "逃避困难,逃避责任,逃避现实",
            "removal": [
                "1. 直面恐惧:恐惧是成长的契机",
                "2. 承担责任:成熟意味着承担责任",
                "3. 立即action:不要等到准备好",
                "4. 事上磨练:在事上锻炼勇气"
            ]
        }
    }
    
    def __init__(self):
        self.name = "王阳明良知decision系统"
        self.version="6.2.0"
        logger.info(f"{self.name} {self.version} init完成")
    
    def judge_with_liangzhi(self, situation: str) -> ConscienceJudgment:
        """良知judge"""
        heart_type = self._identify_heart_type(situation)
        heart_def = self.LIANGZHI_HEARTS[heart_type]
        is_liangzhi_clear = self._is_liangzhi_clear(situation)
        evidence_for, evidence_against = self._extract_evidence(situation)
        
        if is_liangzhi_clear:
            judgment = "这件事符合良知,是对的选择"
            reasoning = "你的良知告诉你:{}".format(heart_def["核心问题"])
            confidence = 0.85
        else:
            judgment = "良知不够清明,需要进一步检验"
            reasoning = "可能存在私欲遮蔽,建议进行良知检验"
            confidence = 0.5
        
        return ConscienceJudgment(
            heart_type=heart_type,
            judgment=judgment,
            reasoning=reasoning,
            confidence=confidence,
            is_liangzhi_clear=is_liangzhi_clear,
            evidence_for=evidence_for,
            evidence_against=evidence_against,
            quote=heart_def["问法"]
        )
    
    def liangzhi_test(self, situation: str) -> LiangzhiTest:
        """良知检验 - decision前四问"""
        four_questions = [
            {
                "number": 1,
                "question": "这件事是对还是错?(是非之心)",
                "guidance": "想象一个你最敬佩的人(圣人)会如何judge",
                "reflection": "我内心深处真的认为这是对的吗?"
            },
            {
                "number": 2,
                "question": "如果公开做这件事,我会感到羞耻吗?(羞恶之心)",
                "guidance": "想象这件事被公之于众",
                "reflection": "我能坦然面对吗?"
            },
            {
                "number": 3,
                "question": "这个决定会伤害他人吗?(恻隐之心)",
                "guidance": "站在受影响的人的角度思考",
                "reflection": "如果是我的家人,朋友,我会怎么想?"
            },
            {
                "number": 4,
                "question": "十年后回看,这个决定是对的吗?(长远之心)",
                "guidance": "拉长时间维度来审视",
                "reflection": "我现在做的决定,十年后还会认为是对的吗?"
            }
        ]
        
        selfish_obstructions = self._analyze_selfish_obstructions(situation)
        
        if selfish_obstructions:
            recommended_action = "需要先去除私欲遮蔽,再做judge"
        else:
            recommended_action = "良知清明,可以按照良知judgeaction"
        
        return LiangzhiTest(
            situation=situation,
            four_questions=four_questions,
            conscience_answer="让心静下来,听听内在的声音",
            selfish_obstruction=selfish_obstructions,
            recommended_action=recommended_action,
            heart_check_result="想象做这件事后,你的内心是感到安宁还是不安?",
            quote=self.LIANGZHI_QUOTES["致良知"][0]
        )
    
    def remove_private_desires(self, situation: str) -> DesiresAnalysis:
        """去私欲分析"""
        dominant_desire = self._identify_desire_type(situation)
        desire_def = self.PRIVATE_DESIRES.get(dominant_desire, 
                                              self.PRIVATE_DESIRES[PrivateDesire.APPROVAL])
        desire_strength = self._assess_desire_strength(situation, dominant_desire)
        
        obstructions = [{
            "desire_type": dominant_desire.value,
            "description": desire_def["description"],
            "manifestation": desire_def["manifestation"]
        }]
        
        removal_methods = desire_def["removal"]
        
        progress_indicators = {
            PrivateDesire.MATERIAL: "从追求物质转向追求内在富足",
            PrivateDesire.FAME: "从追求名声转向追求卓越",
            PrivateDesire.PLEASURE: "从追求享乐转向追求意义",
            PrivateDesire.APPROVAL: "从追求认可转向自我认可",
            PrivateDesire.AVOIDANCE: "从逃避转向直面"
        }
        
        return DesiresAnalysis(
            dominant_desire=dominant_desire,
            desire_strength=desire_strength,
            obstructions=obstructions,
            removal_methods=removal_methods,
            progress_indicator=progress_indicators.get(dominant_desire, "持续修身"),
            quote=self.LIANGZHI_QUOTES["去私欲"][0]
        )
    
    def value_decision(self, situation: str, options: List[str]) -> ValueDecision:
        """价值decision"""
        conscience_rankings = []
        for option in options:
            judgment = self.judge_with_liangzhi(f"{situation} - {option}")
            conscience_rankings.append({
                "option": option,
                "liangzhi_score": judgment.confidence * 100,
                "heart_type": judgment.heart_type.value,
                "is_clear": judgment.is_liangzhi_clear
            })
        
        conscience_rankings.sort(key=lambda x: x["liangzhi_score"], reverse=True)
        
        best_option = conscience_rankings[0]["option"] if conscience_rankings else options[0]
        reasoning = "良知judge'{}'为最佳选择".format(best_option)
        
        return ValueDecision(
            situation=situation,
            options=options,
            conscience_rankings=conscience_rankings,
            best_option=best_option,
            reasoning=reasoning,
            long_term_view="想象这个选择10年后,你会不会后悔?",
            quote=self.LIANGZHI_QUOTES["致良知"][0]
        )
    
    def daily_practice(self) -> DailyPractice:
        """日常修身计划"""
        return DailyPractice(
            morning_practice={
                "activity": "静坐养心",
                "duration": "15-30分钟",
                "method": "盘腿而坐,脊背挺直,闭目专注呼吸,让心静下来",
                "goal": "息心静气,让良知显现"
            },
            midday_practice={
                "activity": "事上磨练",
                "duration": "随时",
                "method": "将每件事当作修炼的机会,观察自己的起心动念",
                "goal": "在action中致良知"
            },
            evening_practice={
                "activity": "反思日记",
                "duration": "10-15分钟",
                "method": "记录今天的起心动念,哪些是良知,哪些是私欲",
                "goal": "发现问题,持续改进"
            },
            weekly_review=[
                "本周我的良知是否越来越清明?",
                "哪些事情我做对了?哪些做错了?",
                "本周我被什么私欲遮蔽了?",
                "下周我要在哪些事情上继续磨练?"
            ],
            monthly_breakthrough="选择一个方面的私欲,进行集中突破",
            quote=self.LIANGZHI_QUOTES["事上练"][0]
        )
    
    def _identify_heart_type(self, situation: str) -> LiangzhiHeart:
        """recognize良知类型"""
        text = situation.lower()
        if any(w in text for w in ["对错", "是非", "应该", "道德"]):
            return LiangzhiHeart.RIGHT_WRONG
        elif any(w in text for w in ["羞耻", "羞愧", "丢脸"]):
            return LiangzhiHeart.SHAME_DISLIKE
        elif any(w in text for w in ["伤害", "影响", "他人", "同情"]):
            return LiangzhiHeart.COMPASSION
        elif any(w in text for w in ["尊重", "规则", "义务", "责任"]):
            return LiangzhiHeart.RESPECT
        return LiangzhiHeart.RIGHT_WRONG
    
    def _is_liangzhi_clear(self, situation: str) -> bool:
        """judge良知是否清明"""
        text = situation.lower()
        clear_indicators = ["应该", "对", "正确", "心安", "坦荡"]
        unclear_indicators = ["纠结", "犹豫", "不安", "愧疚"]
        clear_count = sum(1 for w in clear_indicators if w in text)
        unclear_count = sum(1 for w in unclear_indicators if w in text)
        return clear_count > unclear_count
    
    def _extract_evidence(self, situation: str) -> Tuple[List[str], List[str]]:
        """提取证据"""
        evidence_for, evidence_against = [], []
        text = situation.lower()
        if "应该" in text or "对" in text:
            evidence_for.append("情境中包含正向judge")
        if "心安" in text:
            evidence_for.append("当事人感到心安")
        if "纠结" in text or "犹豫" in text:
            evidence_against.append("存在内心纠结")
        if "不安" in text:
            evidence_against.append("存在不安感")
        return evidence_for, evidence_against
    
    def _analyze_selfish_obstructions(self, situation: str) -> List[str]:
        """分析私欲阻碍"""
        obstructions = []
        text = situation.lower()
        keywords = {
            PrivateDesire.MATERIAL: ["钱", "金钱", "利益", "好处"],
            PrivateDesire.FAME: ["名声", "面子", "荣誉", "地位"],
            PrivateDesire.PLEASURE: ["享乐", "舒服", "安逸", "享受"],
            PrivateDesire.APPROVAL: ["认可", "喜欢", "赞扬", "好评"]
        }
        for desire, words in keywords.items():
            if any(w in text for w in words):
                obstructions.append(f"可能存在{desire.value}")
        return obstructions
    
    def _identify_desire_type(self, situation: str) -> PrivateDesire:
        """recognize私欲类型"""
        text = situation.lower()
        mapping = {
            "钱": PrivateDesire.MATERIAL, "名声": PrivateDesire.FAME,
            "面子": PrivateDesire.FAME, "舒服": PrivateDesire.PLEASURE,
            "认可": PrivateDesire.APPROVAL, "逃避": PrivateDesire.AVOIDANCE
        }
        for keyword, desire in mapping.items():
            if keyword in text:
                return desire
        return PrivateDesire.APPROVAL
    
    def _assess_desire_strength(self, situation: str, desire: PrivateDesire) -> float:
        """评估私欲强度"""
        text = situation.lower()
        boosters = ["很多", "大量", "极度", "非常", "极度"]
        base = 0.5
        for b in boosters:
            if b in text:
                base += 0.1
        return min(1.0, base)

    # ---- fusion 兼容方法（v8.2.0）----
    def get_liangzhi_judgment(self, situation: str, options: List) -> Dict:
        """
        融合 judge_with_liangzhi + value_decision，返回与 fusion 期望一致的格式。
        Args:
            situation: 情境描述
            options: 选项列表 (List[Dict] 或 List[str])
        Returns:
            适配 fusion 期望的字典结构
        """
        # 基础良知判断
        judgment = self.judge_with_liangzhi(situation)
        # 价值决策
        opt_strs = []
        for o in options:
            if isinstance(o, dict):
                opt_strs.append(o.get("name", o.get("title", str(o))))
            else:
                opt_strs.append(str(o))
        vdecision = self.value_decision(situation, opt_strs) if opt_strs else None
        # 构建 fusion 期望的格式
        final_judge = {}
        if vdecision and vdecision.best_option:
            final_judge = {
                "结论": vdecision.best_option,
                "basis": vdecision.reasoning,
                "经典basis": {"原文": vdecision.quote}
            }
        return {
            "最终judge": final_judge,
            "置信度": 0.85,
            "heart_type": judgment.heart_type.value if judgment.heart_type else "unknown",
            "conscience_rankings": getattr(vdecision, "conscience_rankings", []) if vdecision else []
        }

    def get_heart_cultivation_guide(self) -> Dict:
        """
        每日修身指导，包装 daily_practice。
        Returns:
            适配 fusion 期望的字典结构
        """
        practice = self.daily_practice()
        return {
            "morning_practice": practice.morning_practice,
            "midday_practice": practice.midday_practice,
            "evening_practice": practice.evening_practice,
            "weekly_review": practice.weekly_review,
            "quote": practice.quote
        }

def quick_judge(situation: str) -> Dict[str, Any]:
    """快速良知judge"""
    system = LiangzhiDecisionSystem()
    result = system.judge_with_liangzhi(situation)
    return {
        "judge": result.judgment,
        "理由": result.reasoning,
        "良知清明": "是" if result.is_liangzhi_clear else "否",
        "检验问题": result.quote
    }

def quick_test(situation: str) -> Dict[str, Any]:
    """快速良知检验"""
    system = LiangzhiDecisionSystem()
    result = system.liangzhi_test(situation)
    return {
        "情境": result.situation,
        "四问": [f"{q['number']}. {q['question']}" for q in result.four_questions],
        "私欲阻碍": result.selfish_obstruction,
        "建议": result.recommended_action
    }

def quick_decide(situation: str, options: List[str]) -> Dict[str, Any]:
    """快速价值decision"""
    system = LiangzhiDecisionSystem()
    result = system.value_decision(situation, options)
    return {
        "最佳选项": result.best_option,
        "理由": result.reasoning,
        "排序": [(r["option"], f"{r['liangzhi_score']:.0f}分") for r in result.conscience_rankings]
    }

# 中文别名（兼容 fusion 模块导入）
良知系统 = LiangzhiDecisionSystem
良知领域 = LiangzhiHeart

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
