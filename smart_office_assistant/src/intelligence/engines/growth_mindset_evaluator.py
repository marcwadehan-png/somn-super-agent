# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze_text',
    'assess_statement',
    'compare_mindsets',
    'create_growth_mindset_evaluator',
    'generate_growth_plan',
    'get_recommendations',
    'to_dict',
]

成长型思维评估系统 v1.0.0
Growth Mindset Evaluator

核心思想:
- 能力可通过努力培养(成长型思维)
- 固定型思维相信能力是天生的
- 成长型思维拥抱挑战,从错误中学习

作者:Somn AI
版本:v1.0.0
日期:2026-04-02
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import re

class MindsetType(Enum):
    """思维模式类型"""
    FIXED = "固定型思维"  # 相信能力是天生的,无法改变
    GROWTH = "成长型思维"  # 相信能力可以通过努力培养
    MIXED = "混合型思维"  # 不同领域有不同的思维模式

class ResponseCategory(Enum):
    """反应类型"""
    CHALLENGE_FACING = "挑战面对"  # 面对挑战的态度
    EFFORT_BELIEF = "努力信念"  # 对努力的观点
    MISTAKE_VIEW = "错误观念"  # 对错误的看法
    CRITICISM_RESPONSE = "批评回应"  # 对批评的反应
    SUCCESS_ATTRIBUTION = "成功归因"  # 成功的原因

@dataclass
class MindsetScore:
    """思维模式评分"""
    overall_score: float = 0.0  # 总体成长型思维分数 (0-100)
    challenge_score: float = 0.0  # 挑战面对分数
    effort_score: float = 0.0  # 努力信念分数
    mistake_score: float = 0.0  # 错误观念分数
    criticism_score: float = 0.0  # 批评回应分数
    success_score: float = 0.0  # 成功归因分数
    
    mindset_type: MindsetType = MindsetType.MIXED
    dominant_patterns: List[str] = field(default_factory=list)
    growth_areas: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "overall_score": round(self.overall_score, 2),
            "challenge_score": round(self.challenge_score, 2),
            "effort_score": round(self.effort_score, 2),
            "mistake_score": round(self.mistake_score, 2),
            "criticism_score": round(self.criticism_score, 2),
            "success_score": round(self.success_score, 2),
            "mindset_type": self.mindset_type.value,
            "dominant_patterns": self.dominant_patterns,
            "growth_areas": self.growth_areas
        }

@dataclass
class GrowthRecommendation:
    """成长建议"""
    category: str
    current_belief: str
    growth_belief: str
    action_suggestions: List[str]
    priority: int  # 1-5, 1为最高优先级

class GrowthMindsetEvaluator:
    """
    成长型思维评估器
    
    用于评估和引导成长型思维.
    
    主要功能:
    1. 评估固定型vs成长型思维倾向
    2. 分析思维模式的具体维度
    3. 提供成长型思维培养建议
    4. 追踪思维模式的改变
    """
    
    # 固定型思维关键词(负面)
    FIXED_KEYWORDS = {
        "天赋": -2, "天生": -2, "聪明": -1, "笨": -2, 
        "不会": -2, "做不到": -2, "没办法": -2, "就这样": -1,
        "我不行": -3, "我不够好": -3, "太难了": -2, "浪费时间": -1,
        "注定": -2, "只能": -2, "反正": -1, "没用": -2
    }
    
    # 成长型思维关键词(正面)
    GROWTH_KEYWORDS = {
        "可以": 2, "能够": 2, "努力": 3, "学习": 2, "进步": 2,
        "尝试": 2, "改进": 2, "提升": 2, "成长": 3, "挑战": 2,
        "坚持": 2, "方法": 1, "strategy": 1, "练习": 2, "积累": 2,
        "暂时": 1, "还不会": 1, "还没": 1, "会好的": 1
    }
    
    # 挑战面对维度的评估规则
    CHALLENGE_RESPONSES = {
        "fixed": [
            "太难了,我做不到",
            "这超出我的能力范围",
            "我害怕失败",
            "算了,不试了",
            "这不适合我"
        ],
        "growth": [
            "这是个学习的好机会",
            "我可以试试看",
            "虽然难,但我可以学",
            "让我想想有什么办法",
            "我可以慢慢来"
        ]
    }
    
    # 错误观念的评估规则
    MISTAKE_RESPONSES = {
        "fixed": [
            "我犯了错误,我很笨",
            "失败了就是失败者",
            "我不想承认错误",
            "错误说明我不行"
        ],
        "growth": [
            "错误是学习的机会",
            "我可以从中学到什么",
            "这次失败帮我排除一个方法",
            "错误是正常的"
        ]
    }
    
    # 批评回应的评估规则
    CRITICISM_RESPONSES = {
        "fixed": [
            "他为什么总是批评我",
            "他就是看我不顺眼",
            "我不想听这些",
            "这太伤人了"
        ],
        "growth": [
            "我能从中得到什么信息",
            "这个批评有没有道理",
            "我可以在哪些方面改进",
            "感谢你的反馈"
        ]
    }
    
    # 成功归因的评估规则
    SUCCESS_RESPONSES = {
        "fixed": [
            "因为我聪明",
            "我有天赋",
            "我运气好",
            "这说明我很厉害"
        ],
        "growth": [
            "因为我付出了努力",
            "我使用了正确的方法",
            "我坚持了下来",
            "我之前一直在练习"
        ]
    }
    
    def __init__(self):
        self.evaluation_history: List[MindsetScore] = []
        self.belief_patterns: Dict[str, int] = defaultdict(int)
    
    def analyze_text(self, text: str) -> MindsetScore:
        """
        分析文本中的思维模式
        
        Args:
            text: 待分析的文本
            
        Returns:
            MindsetScore: 思维模式评分
        """
        text_lower = text.lower()
        
        # 计算各维度分数
        challenge_score = self._evaluate_challenge(text)
        effort_score = self._evaluate_effort(text)
        mistake_score = self._evaluate_mistake(text)
        criticism_score = self._evaluate_criticism(text)
        success_score = self._evaluate_success(text)
        
        # 计算总体分数
        overall_score = (
            challenge_score * 0.2 +
            effort_score * 0.2 +
            mistake_score * 0.2 +
            criticism_score * 0.2 +
            success_score * 0.2
        )
        
        # 确定思维模式类型
        if overall_score >= 70:
            mindset_type = MindsetType.GROWTH
        elif overall_score <= 30:
            mindset_type = MindsetType.FIXED
        else:
            mindset_type = MindsetType.MIXED
        
        # recognize主导模式和需要成长的领域
        scores = {
            "挑战面对": challenge_score,
            "努力信念": effort_score,
            "错误观念": mistake_score,
            "批评回应": criticism_score,
            "成功归因": success_score
        }
        
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        dominant_patterns = [name for name, score in sorted_scores[:3] if score >= 60]
        growth_areas = [name for name, score in sorted_scores[-2:] if score <= 40]
        
        result = MindsetScore(
            overall_score=overall_score,
            challenge_score=challenge_score,
            effort_score=effort_score,
            mistake_score=mistake_score,
            criticism_score=criticism_score,
            success_score=success_score,
            mindset_type=mindset_type,
            dominant_patterns=dominant_patterns,
            growth_areas=growth_areas
        )
        
        self.evaluation_history.append(result)
        return result
    
    def _evaluate_challenge(self, text: str) -> float:
        """评估挑战面对维度"""
        text_lower = text.lower()
        score = 50  # 基础分
        
        # 固定型思维减分
        for keyword, weight in self.FIXED_KEYWORDS.items():
            if keyword in text_lower:
                score += weight
        
        # 成长型思维加分
        for keyword, weight in self.GROWTH_KEYWORDS.items():
            if keyword in text_lower:
                score += weight
        
        # 检查具体的挑战反应
        for response in self.CHALLENGE_RESPONSES["fixed"]:
            if response in text:
                score -= 15
        
        for response in self.CHALLENGE_RESPONSES["growth"]:
            if response in text:
                score += 15
        
        return max(0, min(100, score))
    
    def _evaluate_effort(self, text: str) -> float:
        """评估努力信念维度"""
        text_lower = text.lower()
        score = 50
        
        # 努力相关词汇
        effort_positive = ["努力", "付出", "坚持", "练习", "用心", "认真", "下功夫"]
        effort_negative = ["不努力", "偷懒", "不想动", "随便"]
        
        for word in effort_positive:
            if word in text_lower:
                score += 10
        
        for word in effort_negative:
            if word in text_lower:
                score -= 15
        
        # 检查是否认为努力有意义
        if "努力没用" in text_lower or "努力浪费时间" in text_lower:
            score -= 20
        
        if "一分耕耘一分收获" in text_lower or "努力会有回报" in text_lower:
            score += 20
        
        return max(0, min(100, score))
    
    def _evaluate_mistake(self, text: str) -> float:
        """评估错误观念维度"""
        text_lower = text.lower()
        score = 50
        
        # 检查具体的错误反应
        for response in self.MISTAKE_RESPONSES["fixed"]:
            if response in text:
                score -= 15
        
        for response in self.MISTAKE_RESPONSES["growth"]:
            if response in text:
                score += 15
        
        # 从错误中学习
        if "学到" in text_lower and "错误" in text_lower:
            score += 10
        
        if "失败是成功之母" in text_lower:
            score += 15
        
        return max(0, min(100, score))
    
    def _evaluate_criticism(self, text: str) -> float:
        """评估批评回应维度"""
        text_lower = text.lower()
        score = 50
        
        # 检查具体的批评反应
        for response in self.CRITICISM_RESPONSES["fixed"]:
            if response in text:
                score -= 15
        
        for response in self.CRITICISM_RESPONSES["growth"]:
            if response in text:
                score += 15
        
        # 防御性反应
        if "他凭什么说我" in text_lower or "他就是针对我" in text_lower:
            score -= 20
        
        # 开放性反应
        if "谢谢你的反馈" in text_lower or "我理解了" in text_lower:
            score += 15
        
        return max(0, min(100, score))
    
    def _evaluate_success(self, text: str) -> float:
        """评估成功归因维度"""
        text_lower = text.lower()
        score = 50
        
        # 检查具体的成功反应
        for response in self.SUCCESS_RESPONSES["fixed"]:
            if response in text:
                score -= 15
        
        for response in self.SUCCESS_RESPONSES["growth"]:
            if response in text:
                score += 15
        
        # 过程归因
        if any(word in text_lower for word in ["方法", "strategy", "坚持", "努力"]):
            score += 10
        
        # 能力归因
        if any(word in text_lower for word in ["天赋", "聪明", "运气"]):
            score -= 5
        
        return max(0, min(100, score))
    
    def get_recommendations(self, score: MindsetScore) -> List[GrowthRecommendation]:
        """
        根据评估结果get成长建议
        
        Args:
            score: 思维模式评分
            
        Returns:
            List[GrowthRecommendation]: 成长建议列表
        """
        recommendations = []
        
        # 挑战面对建议
        if score.challenge_score < 60:
            recommendations.append(GrowthRecommendation(
                category="挑战面对",
                current_belief="挑战太难了,我做不到",
                growth_belief="挑战是学习的机会,我可以一步步来",
                action_suggestions=[
                    "将大挑战分解成小步骤",
                    "每天尝试一件稍微超出舒适区的事",
                    "记录每次挑战后的收获",
                    "对自己说'我可以学'"
                ],
                priority=1
            ))
        
        # 努力信念建议
        if score.effort_score < 60:
            recommendations.append(GrowthRecommendation(
                category="努力信念",
                current_belief="努力不一定有结果,天赋更重要",
                growth_belief="努力是成功的关键,方法比天赋更重要",
                action_suggestions=[
                    "关注过程中的进步,而非结果",
                    "学习高效学习方法和strategy",
                    "建立'刻意练习'的习惯",
                    "奖励自己的努力,而非天赋"
                ],
                priority=2
            ))
        
        # 错误观念建议
        if score.mistake_score < 60:
            recommendations.append(GrowthRecommendation(
                category="错误观念",
                current_belief="犯错说明我不行,我应该避免错误",
                growth_belief="错误是最好的老师,每次错误都是学习机会",
                action_suggestions=[
                    "把错误记录下来,分析从中能学到什么",
                    "改变对错误的叙事:'我犯了一个错误'而非'我是一个错误'",
                    "庆祝从错误中学到东西的时刻",
                    "问自己:'这次错误教会了我什么?'"
                ],
                priority=1
            ))
        
        # 批评回应建议
        if score.criticism_score < 60:
            recommendations.append(GrowthRecommendation(
                category="批评回应",
                current_belief="批评让我难堪,我应该防御或回避",
                growth_belief="批评是成长的反馈,感谢别人花时间指出我的不足",
                action_suggestions=[
                    "先深呼吸,不要立即反应",
                    "问自己:'这个批评有没有道理?'",
                    "如果批评有道理,感谢对方并制定改进计划",
                    "如果批评没道理,礼貌地解释你的立场"
                ],
                priority=2
            ))
        
        # 成功归因建议
        if score.success_score < 60:
            recommendations.append(GrowthRecommendation(
                category="成功归因",
                current_belief="成功是因为我聪明/有天赋",
                growth_belief="成功是因为我付出了努力,使用了正确的方法",
                action_suggestions=[
                    "分析成功案例:是什么带来了成功?",
                    "把成功归因于具体的行为和strategy",
                    "问自己:'下次如何复制这个成功?'",
                    "与他人分享你努力的过程"
                ],
                priority=3
            ))
        
        return sorted(recommendations, key=lambda x: x.priority)
    
    def generate_growth_plan(self, score: MindsetScore) -> Dict[str, any]:
        """
        generate个性化成长计划
        
        Args:
            score: 思维模式评分
            
        Returns:
            Dict: 成长计划
        """
        recommendations = self.get_recommendations(score)
        
        plan = {
            "当前思维模式": score.mindset_type.value,
            "总体评分": f"{score.overall_score:.1f}/100",
            "优势领域": score.dominant_patterns,
            "成长领域": score.growth_areas,
            "优先action计划": [],
            "日常练习": [],
            "每周检视": []
        }
        
        # 添加优先action计划
        for rec in recommendations[:3]:
            plan["优先action计划"].append({
                "领域": rec.category,
                "目标信念": rec.growth_belief,
                "具体action": rec.action_suggestions[:2]
            })
        
        # 添加日常练习
        plan["每日练习"] = [
            "早晨:设定今天的成长目标(而非完美目标)",
            "中午:记录一次挑战经历和从中学习到什么",
            "晚上:反思今天的进步(无论多小)",
            "睡前:对自己说'今天我学到了____'"
        ]
        
        # 添加每周检视
        plan["每周检视"] = [
            "本周我接受了哪些新的挑战?",
            "我从哪些错误中学到了东西?",
            "我如何把成功归因于努力和方法?",
            "我的思维模式有哪些细微的改变?"
        ]
        
        return plan
    
    def compare_mindsets(self, score1: MindsetScore, score2: MindsetScore) -> Dict:
        """
        比较两次评估结果,追踪成长
        
        Args:
            score1: 之前的评估
            score2: 当前的评估
            
        Returns:
            Dict: 比较结果
        """
        changes = {
            "overall_change": round(score2.overall_score - score1.overall_score, 2),
            "challenge_change": round(score2.challenge_score - score1.challenge_score, 2),
            "effort_change": round(score2.effort_score - score1.effort_score, 2),
            "mistake_change": round(score2.mistake_score - score1.mistake_score, 2),
            "criticism_change": round(score2.criticism_score - score1.criticism_score, 2),
            "success_change": round(score2.success_score - score1.success_score, 2)
        }
        
        improvements = [k.replace("_change", "") for k, v in changes.items() if v > 0]
        regressions = [k.replace("_change", "") for k, v in changes.items() if v < 0]
        
        return {
            "changes": changes,
            "improvements": improvements,
            "regressions": regressions,
            "summary": self._generate_comparison_summary(changes)
        }
    
    def _generate_comparison_summary(self, changes: Dict) -> str:
        """generate比较总结"""
        total_change = sum(changes.values())
        
        if total_change > 10:
            return "思维模式显著进步!继续保持你的成长势头."
        elif total_change > 0:
            return "思维模式有所改善,继续努力培养成长型思维."
        elif total_change > -10:
            return "思维模式保持稳定,注意recognize可能的固定型思维陷阱."
        else:
            return "思维模式有所退化,建议重新审视近期遇到的挑战和困难."
    
    def assess_statement(self, statement: str) -> Dict[str, any]:
        """
        快速评估单个陈述的思维模式倾向
        
        Args:
            statement: 待评估的陈述
            
        Returns:
            Dict: 评估结果
        """
        score = self.analyze_text(statement)
        
        # 简化的解读
        if score.overall_score >= 70:
            interpretation = "这是一个成长型思维的陈述,表明相信能力可以通过努力培养."
        elif score.overall_score <= 30:
            interpretation = "这是一个固定型思维的陈述,可能需要调整为更成长导向的视角."
        else:
            interpretation = "这是一个混合思维的陈述,可以进一步培养成长型思维."
        
        return {
            "statement": statement,
            "score": score.overall_score,
            "interpretation": interpretation,
            "main_tendency": score.mindset_type.value,
            "quick_tip": self._get_quick_tip(score)
        }
    
    def _get_quick_tip(self, score: MindsetScore) -> str:
        """get快速提示"""
        lowest_dim = min([
            ("challenge_score", "挑战", score.challenge_score),
            ("effort_score", "努力", score.effort_score),
            ("mistake_score", "错误", score.mistake_score),
            ("criticism_score", "批评", score.criticism_score),
            ("success_score", "成功", score.success_score)
        ], key=lambda x: x[2])
        
        tips = {
            "挑战": "试着把'我做不到'换成'我暂时还不会'",
            "努力": "记住:努力本身就是成功的标志,而非弱点",
            "错误": "错误不是失败,而是学习机会",
            "批评": "把批评看作他人给你的免费反馈",
            "成功": "把成功归因于你的努力和方法"
        }
        
        return tips.get(lowest_dim[1], "继续保持自我反思")

def create_growth_mindset_evaluator() -> GrowthMindsetEvaluator:
    """工厂函数:创建成长型思维评估器"""
    return GrowthMindsetEvaluator()

# 使用示例
# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
