"""
__all__ = [
    'assess_fortune',
    'get_cultivation_guide',
    'get_sufu_core',
    'get_wisdom_summary',
    'integrate_with_reasoning',
    'make_decision',
    'warn_of_danger',
]

素书智慧核心模块 v1.0
Sufu Wisdom Core Module

<素书>智慧融入Somn智能体系统
黄石公·道,德,仁,义,礼五位一体

核心思想:
- 道者,人之所蹈,使万物不知其所由
- 德者,人之所得,使万物各得其所欲
- 仁者,人之所亲,有慈惠恻隐之心
- 义者,人之所宜,赏善罚恶
- 礼者,人之所履,成人伦之序

版本: v1.0
更新: 2026-04-02
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json

class SufuPrinciple(Enum):
    """素书五德原则"""
    DAO = "道"           # 规律,自然,无为
    DE = "德"            # 品德,禀赋,所得
    REN = "仁"           # 仁爱,慈悲,同情
    YI = "义"            # 正义,合宜,奖惩
    LI = "礼"            # 规范,秩序,礼仪

@dataclass
class SufuDecision:
    """素书decision结构"""
    principle: SufuPrinciple      # 核心原则
    reasoning: str                 # 推理过程
    action: str                     # action建议
    wisdom_source: str              # 智慧来源(素书原文)
    balance_score: float            # 五德平衡分数(0-1)
    risk_warning: List[str]         # 风险警示(遵义章)
    expected_outcome: str            # 预期结果

@dataclass
class SufuPersona:
    """素书人格特质"""
    # 正道章人才标准
    is_jun: bool = False    # 俊 - 领袖之才(德,信,义,才,明)
    is_hao: bool = False    # 豪 - 将帅之才(行,智,信,廉)
    is_jie: bool = False    # 杰 - 干练之才(忠,义,勇,廉)
    
    # 求人之志章特质
    cultivation_level: int = 5      # 修养层级(1-10)
    wisdom_accumulation: float = 0.0  # 智慧积累
    moral_integrity: float = 1.0    # 道德操守(0-1)
    
    # 本德宗道章
    contentedness: float = 0.8     # 知足程度(0-1)
    perseverance: float = 0.8       # 忍辱能力(0-1)
    sincerity: float = 0.9         # 至诚程度(0-1)
    
    # 遵义章警示
    warning_prone: bool = False     # 易犯遵义章错误
    caution_score: float = 0.7     # 谨慎程度(0-1)

class SufuWisdomCore:
    """
    素书智慧核心引擎
    
    将<素书>六章智慧融入智能decision:
    1. 原始章 - 五位一体核心原则
    2. 正道章 - 人才recognize与分类
    3. 求人之志章 - 修身养性法则
    4. 本德宗道章 - 根本智慧
    5. 遵义章 - 避祸警示
    6. 安礼章 - 福祸规律
    """
    
    def __init__(self):
        """init素书智慧核心"""
        self.principles = {
            SufuPrinciple.DAO: self._apply_dao,
            SufuPrinciple.DE: self._apply_de,
            SufuPrinciple.REN: self._apply_ren,
            SufuPrinciple.YI: self._apply_yi,
            SufuPrinciple.LI: self._apply_li,
        }
        
        # 修身二十法(求人之志章)
        self.cultivation_methods = [
            "绝嗜禁欲,所以除累",
            "抑非损恶,所以让过",
            "贬酒阙色,所以无污",
            "避嫌远疑,所以不误",
            "博学切问,所以广知",
            "高行微言,所以修身",
            "恭俭谦约,所以自守",
            "深计远虑,所以不穷",
            "亲仁友直,所以扶颠",
            "近恕笃行,所以接人",
            "任材使能,所以济物",
            "殚恶斥谗,所以止乱",
            "推古验今,所以不惑",
            "先揆后度,所以应卒",
            "设变致权,所以解结",
            "括囊顺会,所以无咎",
            "横戈介骑,所以卫志",
            "伐罪集功,所以待时",
            "释怪逐远,所以迁稚",
            "任贤使能,所以竟尚",
        ]
        
        # 致败行为警示(遵义章)
        self.failure_warnings = [
            "以明示下者暗",
            "有过不知者蔽",
            "迷而不返者惑",
            "以言取怨者祸",
            "令与心乖者废",
            "赏罚不平则乱",
            "任数不知权变是以危",
            "阴计外泄者败",
            "厚敛薄施者凋",
            "上下相嫉必败",
        ]
        
        # 福祸八因(安礼章)
        self.fortune_misfortune = {
            "怨在不舍小过": "福",
            "患在不预定谋": "祸",
            "福在积善": "福",
            "祸在积恶": "祸",
            "饥在贱农": "祸",
            "寒在堕织": "祸",
            "安在得人": "福",
            "危在失事": "祸",
        }
        
        # decision历史
        self.decision_history: List[SufuDecision] = []
        
    # ==================== 核心decision方法 ====================
    
    def _apply_dao(self, context: Dict) -> Dict:
        """
        应用'道'的原则
        道者,人之所蹈,使万物不知其所由
        """
        return {
            "principle": "道",
            "meaning": "遵循自然规律,无为而无不为",
            "action": "顺应事物本性,不强加人为意志",
            "quote": "道者,人之所蹈,使万物不知其所由"
        }
    
    def _apply_de(self, context: Dict) -> Dict:
        """
        应用'德'的原则
        德者,人之所得,使万物各得其所欲
        """
        return {
            "principle": "德",
            "meaning": "有所得,心想事成",
            "action": "以德服人,以德感人",
            "quote": "德者,人之所得,使万物各得其所欲"
        }
    
    def _apply_ren(self, context: Dict) -> Dict:
        """
        应用'仁'的原则
        仁者,人之所亲,有慈惠恻隐之心
        """
        return {
            "principle": "仁",
            "meaning": "仁者爱人,慈悲为怀",
            "action": "推己及人,助人自助",
            "quote": "仁者,人之所亲,有慈惠恻隐之心,以遂其generate"
        }
    
    def _apply_yi(self, context: Dict) -> Dict:
        """
        应用'义'的原则
        义者,人之所宜,赏善罚恶
        """
        return {
            "principle": "义",
            "meaning": "是非分明,合宜得当",
            "action": "奖惩分明,公正无私",
            "quote": "义者,人之所宜,赏善罚恶,以立功立事"
        }
    
    def _apply_li(self, context: Dict) -> Dict:
        """
        应用'礼'的原则
        礼者,人之所履,成人伦之序
        """
        return {
            "principle": "礼",
            "meaning": "规范秩序,各安其位",
            "action": "遵规守纪,维护秩序",
            "quote": "礼者,人之所履,夙兴夜寐,以成人伦之序"
        }
    
    def make_decision(self, situation: Dict) -> SufuDecision:
        """
        素书智慧decision
        
        Args:
            situation: decision情境,包含:
                - type: decision类型
                - options: 可选方案
                - constraints: 约束条件
                - stakeholders: 利益相关方
        
        Returns:
            SufuDecision: 素书decision结果
        """
        decision_type = situation.get("type", "general")
        options = situation.get("options", [])
        
        # 1. 分析五德平衡
        principle_scores = self._evaluate_principles(situation)
        
        # 2. 检查遵义章警示
        warnings = self._check_failure_warnings(situation)
        
        # 3. 应用正道章标准
        if decision_type == "talent":
            return self._talent_decision(situation, principle_scores)
        
        # 4. 应用修身法则
        if decision_type == "self_cultivation":
            return self._cultivation_decision(situation, principle_scores)
        
        # 5. 通用decision
        return self._general_decision(situation, principle_scores, warnings)
    
    def _evaluate_principles(self, situation: Dict) -> Dict[SufuPrinciple, float]:
        """评估五德在当前情境中的适用性"""
        scores = {}
        for principle in SufuPrinciple:
            scores[principle] = self._score_principle(principle, situation)
        return scores
    
    def _score_principle(self, principle: SufuPrinciple, situation: Dict) -> float:
        """对单一原则评分"""
        # 简化的评分逻辑
        situation_type = situation.get("type", "general")
        
        principle_weights = {
            SufuPrinciple.DAO: {"strategy": 0.9, "general": 0.7, "talent": 0.5},
            SufuPrinciple.DE: {"strategy": 0.6, "general": 0.8, "talent": 0.9},
            SufuPrinciple.REN: {"strategy": 0.5, "general": 0.9, "talent": 0.7},
            SufuPrinciple.YI: {"strategy": 0.8, "general": 0.7, "talent": 0.6},
            SufuPrinciple.LI: {"strategy": 0.6, "general": 0.8, "talent": 0.5},
        }
        
        return principle_weights.get(principle, {}).get(situation_type, 0.7)
    
    def _check_failure_warnings(self, situation: Dict) -> List[str]:
        """检查遵义章警示"""
        relevant_warnings = []
        situation_text = json.dumps(situation, ensure_ascii=False)
        
        # 检查是否触发警示
        warning_triggers = {
            "以明示下者暗": ["炫耀", "显摆", "高调"],
            "有过不知者蔽": ["固执", "不认错", "自大"],
            "以言取怨者祸": ["得罪", "口无遮拦", "失言"],
            "令与心乖者废": ["违背民意", "强推", "不顺应"],
            "赏罚不平则乱": ["偏心", "不公", "徇私"],
        }
        
        for warning, triggers in warning_triggers.items():
            for trigger in triggers:
                if trigger in situation_text:
                    relevant_warnings.append(warning)
                    break
        
        return relevant_warnings
    
    def _talent_decision(self, situation: Dict, 
                        principle_scores: Dict[SufuPrinciple, float]) -> SufuDecision:
        """人才decision(正道章)"""
        person = situation.get("person", {})
        
        # 正道章人才标准
        is_jun = (
            person.get("德足以怀远", False) and
            person.get("信足以一异", False) and
            person.get("义足以得众", False) and
            person.get("才足以鉴古", False) and
            person.get("明足以照下", False)
        )
        
        is_hao = (
            person.get("行足以为仪表", False) and
            person.get("智足以决嫌疑", False) and
            person.get("信可以使守约", False) and
            person.get("廉可以使分财", False)
        )
        
        is_jie = (
            person.get("守职而不废", False) and
            person.get("处义而不回", False) and
            person.get("见嫌而不苟免", False) and
            person.get("见利而不苟得", False)
        )
        
        if is_jun:
            talent_level = "俊"
            wisdom = "德足以怀远,信足以一异,义足以得众,才足以鉴古,明足以照下"
        elif is_hao:
            talent_level = "豪"
            wisdom = "行足以为仪表,智足以决嫌疑,信可以使守约,廉可以使分财"
        elif is_jie:
            talent_level = "杰"
            wisdom = "守职而不废,处义而不回,见嫌而不苟免,见利而不苟得"
        else:
            talent_level = "待培养"
            wisdom = "需加强德,才,能,忠等方面修养"
        
        balance_score = sum(principle_scores.values()) / len(principle_scores)
        
        return SufuDecision(
            principle=SufuPrinciple.DE,
            reasoning=f"basis正道章标准,评定为'{talent_level}'",
            action=f"建议{talent_level}级人才担任",
            wisdom_source=f"正道章:{wisdom}",
            balance_score=balance_score,
            risk_warning=[],
            expected_outcome=f"人尽其才,各得其所"
        )
    
    def _cultivation_decision(self, situation: Dict,
                             principle_scores: Dict[SufuPrinciple, float]) -> SufuDecision:
        """修身decision(求人之志章)"""
        current_cultivation = situation.get("cultivation_level", 5)
        
        # 选择最适合当前层级的修身方法
        if current_cultivation < 3:
            method = self.cultivation_methods[0]  # 绝嗜禁欲
        elif current_cultivation < 6:
            method = self.cultivation_methods[4]  # 博学切问
        elif current_cultivation < 9:
            method = self.cultivation_methods[7]  # 深计远虑
        else:
            method = self.cultivation_methods[11]  # 殚恶斥谗
        
        balance_score = sum(principle_scores.values()) / len(principle_scores)
        
        return SufuDecision(
            principle=SufuPrinciple.REN,
            reasoning=f"当前修养层级{current_cultivation},宜修{method.split(',')[0]}",
            action=method,
            wisdom_source=f"求人之志章:{method}",
            balance_score=balance_score,
            risk_warning=[],
            expected_outcome="修身齐家治国平天下"
        )
    
    def _general_decision(self, situation: Dict,
                         principle_scores: Dict[SufuPrinciple, float],
                         warnings: List[str]) -> SufuDecision:
        """通用decision"""
        # 确定主导原则
        dominant_principle = max(principle_scores, key=principle_scores.get)
        principle_info = self.principles[dominant_principle](situation)
        
        balance_score = sum(principle_scores.values()) / len(principle_scores)
        
        return SufuDecision(
            principle=dominant_principle,
            reasoning=f"basis{principle_info['meaning']},synthesize评估后decision",
            action=principle_info["action"],
            wisdom_source=f"原始章:{principle_info['quote']}",
            balance_score=balance_score,
            risk_warning=warnings,
            expected_outcome="诸事顺遂"
        )
    
    # ==================== 修身指导 ====================
    
    def get_cultivation_guide(self, current_level: int = 5) -> List[str]:
        """
        get修身指导
        
        基于求人之志章的二十种修身方法
        """
        if current_level < 3:
            return [
                "绝嗜禁欲,所以除累",
                "抑非损恶,所以让过",
                "贬酒阙色,所以无污",
            ]
        elif current_level < 6:
            return [
                "博学切问,所以广知",
                "高行微言,所以修身",
                "恭俭谦约,所以自守",
            ]
        elif current_level < 9:
            return [
                "深计远虑,所以不穷",
                "亲仁友直,所以扶颠",
                "近恕笃行,所以接人",
            ]
        else:
            return [
                "任材使能,所以济物",
                "殚恶斥谗,所以止乱",
                "推古验今,所以不惑",
            ]
    
    def assess_fortune(self, actions: List[str]) -> Dict[str, Any]:
        """
        评估行为吉凶(安礼章)
        
        福祸八因:
        - 福在积善,祸在积恶
        - 怨在不舍小过,患在不预定谋
        - 饥在贱农,寒在堕织
        - 安在得人,危在失事
        """
        fortune_score = 0.0
        reasons = []
        
        for action in actions:
            if any(kw in action for kw in ["善", "积德", "助人"]):
                fortune_score += 0.2
                reasons.append("积善得福")
            if any(kw in action for kw in ["恶", "害", "损"]):
                fortune_score -= 0.2
                reasons.append("积恶致祸")
            if any(kw in action for kw in ["宽恕", "谅解", "容忍"]):
                fortune_score += 0.1
                reasons.append("舍小过则无怨")
            if any(kw in action for kw in ["计划", "预谋", "谋略"]):
                fortune_score += 0.1
                reasons.append("预谋则无患")
            if any(kw in action for kw in ["用人", "得人", "聚才"]):
                fortune_score += 0.1
                reasons.append("得人则安")
        
        return {
            "fortune_score": max(0, min(1, fortune_score)),
            "assessment": "大吉" if fortune_score >= 0.5 else "吉" if fortune_score >= 0.2 else "凶",
            "reasons": reasons,
            "quote": "福在积善,祸在积恶"
        }
    
    # ==================== 风险预警 ====================
    
    def warn_of_danger(self, situation: Dict) -> List[str]:
        """
        危险预警(遵义章)
        
        列举46种致败行为
        """
        warnings = []
        situation_text = json.dumps(situation, ensure_ascii=False)
        
        # 简化的警示检测
        danger_patterns = [
            ("示下不明", ["炫耀", "显摆"]),
            ("有过不知", ["不认错", "固执"]),
            ("以言取怨", ["得罪", "口无遮拦"]),
            ("赏罚不平", ["偏心", "不公"]),
            ("上下相嫉", ["内斗", "争权"]),
        ]
        
        for warning, patterns in danger_patterns:
            for pattern in patterns:
                if pattern in situation_text:
                    warnings.append(f"⚠️ {warning}:{','.join(patterns)}")
                    break
        
        return warnings if warnings else ["✅ 未检测到明显风险"]
    
    # ==================== 系统整合 ====================
    
    def integrate_with_reasoning(self, reasoning_chain: List[Dict]) -> Dict[str, Any]:
        """
        将素书智慧融入推理链
        
        对每个推理步骤应用五德检验
        """
        enhanced_chain = []
        
        for step in reasoning_chain:
            # 应用五德检验
            situation = {
                "type": "reasoning_step",
                "content": step.get("content", "")
            }
            
            decision = self.make_decision(situation)
            
            enhanced_step = {
                **step,
                "sufu_wisdom": {
                    "principle": decision.principle.value,
                    "balance_score": decision.balance_score,
                    "warnings": decision.risk_warning,
                    "quote": decision.wisdom_source
                }
            }
            
            enhanced_chain.append(enhanced_step)
        
        return {
            "original_chain": reasoning_chain,
            "enhanced_chain": enhanced_chain,
            "overall_balance": sum(
                s["sufu_wisdom"]["balance_score"] 
                for s in enhanced_chain
            ) / len(enhanced_chain) if enhanced_chain else 0,
            "total_warnings": sum(
                len(s["sufu_wisdom"]["warnings"])
                for s in enhanced_chain
            )
        }
    
    def get_wisdom_summary(self) -> Dict[str, Any]:
        """get素书智慧概要"""
        return {
            "core_principles": {
                "道": "人之所蹈,使万物不知其所由",
                "德": "人之所得,使万物各得其所欲",
                "仁": "人之所亲,有慈惠恻隐之心",
                "义": "人之所宜,赏善罚恶",
                "礼": "人之所履,成人伦之序"
            },
            "talent_levels": {
                "俊": "德,信,义,才,明",
                "豪": "行,智,信,廉",
                "杰": "忠,义,勇,廉"
            },
            "key_warnings": self.failure_warnings[:5],
            "fortune_rules": self.fortune_misfortune,
            "cultivation_methods_count": len(self.cultivation_methods)
        }

# 全局实例
_sufu_core: Optional[SufuWisdomCore] = None

def get_sufu_core() -> SufuWisdomCore:
    """get素书智慧核心实例"""
    global _sufu_core
    if _sufu_core is None:
        _sufu_core = SufuWisdomCore()
    return _sufu_core
