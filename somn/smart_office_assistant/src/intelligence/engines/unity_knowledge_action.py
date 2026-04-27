# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze',
    'create_practice_case',
    'create_unity_evaluator',
    'diagnose_topic',
    'get_summary_report',
    'practice_guidance',
    'to_dict',
]

知行合一评估器 v1.0.0
Unity of Knowledge and Action Evaluator

基于王阳明<知行合一>核心思想构建

核心思想:
- 知是行的开始,行是知的完成
- 真知必能行,不行不是真知
- 知而不行,等于未知
- 事上磨练,在实践中验证认知

作者:Somn AI
版本:v1.0.0
日期:2026-04-02
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict

class KnowingLevel(Enum):
    """知之层次"""
    UNKNOWN = "未知"  # 完全不知
    THEORETICAL = "理论之知"  # 知道理论但未实践
    PARTIAL = "部分知行"  # 知与行都有欠缺
    INTEGRATED = "知行合一"  # 知与行unified
    SPONTANEOUS = "自然流露"  # 无需思考自然做到

class ActionQuality(Enum):
    """action质量"""
    DELAYED = "拖延执行"  # 知道但不action
    MECHANICAL = "机械执行"  # action但缺乏理解
    CONSCIOUS = "有意识执行"  # 理解后有意识action
    HABITUAL = "习惯性执行"  # 已形成习惯
    ENLIGHTENED = "顿悟执行"  # 身心合一

@dataclass
class KnowingActionAnalysis:
    """知行分析"""
    knowing_level: KnowingLevel
    action_quality: ActionQuality
    knowing_score: float  # 知的程度 0-100
    action_score: float  # 行的程度 0-100
    integration_score: float  # 知行合一程度 0-100
    
    gaps: List[str] = field(default_factory=list)  # 知行差距
    insights: List[str] = field(default_factory=list)  # 洞见
    
    def to_dict(self) -> Dict:
        return {
            "knowing_level": self.knowing_level.value,
            "action_quality": self.action_quality.value,
            "knowing_score": round(self.knowing_score, 1),
            "action_score": round(self.action_score, 1),
            "integration_score": round(self.integration_score, 1),
            "gaps": self.gaps,
            "insights": self.insights
        }

@dataclass
class PracticeCase:
    """实践案例"""
    title: str
    description: str
    knowing_score: float
    action_score: float
    obstacles: List[str] = field(default_factory=list)
    breakthroughs: List[str] = field(default_factory=list)

class UnityKnowledgeActionEvaluator:
    """
    知行合一评估器
    
    基于王阳明xinxue构建,评估知与行的unified程度,
    帮助用户实现知行合一的境界.
    
    主要功能:
    1. 评估知的深度
    2. 评估行的质量
    3. 诊断知行差距
    4. 提供事上磨练指导
    """
    
    # 知之深度关键词
    KNOWING_KEYWORDS = {
        # 浅知
        "听说过": 20, "知道一点": 30, "大概知道": 40,
        # 深知
        "理解": 60, "深刻理解": 75, "真正懂得": 85,
        # 真知
        "彻底明白": 90, "刻骨铭心": 95, "融入血液": 100
    }
    
    # 行之质量关键词
    ACTION_KEYWORDS = {
        # 拖延
        "还没做": 20, "等会": 30, "以后": 40, "算了": 30,
        # action
        "开始做": 60, "在做": 70, "坚持做": 80, "养成习惯": 90,
        # 顿悟
        "自然做": 95, "不刻意": 98, "无条件": 100
    }
    
    # 知行对照表
    KNOWING_ACTION_PAIRS = {
        "知道健康重要": ["坚持运动", "健康饮食", "规律作息"],
        "知道学习重要": ["每天读书", "主动学习", "学以致用"],
        "知道时间宝贵": ["时间管理", "优先级排序", "避免拖延"],
        "知道沟通重要": ["倾听他人", "表达清晰", "及时反馈"],
        "知道目标重要": ["设定目标", "分解任务", "定期检视"]
    }
    
    def __init__(self):
        self.analysis_history: List[KnowingActionAnalysis] = []
        self.practice_cases: List[PracticeCase] = []
    
    def analyze(self, knowing_text: str = "", action_text: str = "",
                integrated_text: str = "") -> KnowingActionAnalysis:
        """
        分析知行状态
        
        Args:
            knowing_text: 关于"知"的描述
            action_text: 关于"行"的描述
            integrated_text: 整合性描述
            
        Returns:
            KnowingActionAnalysis: 知行分析结果
        """
        # 评估知的程度
        knowing_score = self._score_knowing(knowing_text or integrated_text)
        
        # 评估行的程度
        action_score = self._score_action(action_text or integrated_text)
        
        # 计算知行合一程度
        integration_score = self._calculate_integration(knowing_score, action_score)
        
        # 确定层次
        knowing_level = self._determine_knowing_level(knowing_score)
        action_quality = self._determine_action_quality(action_score)
        
        # recognize知行差距
        gaps = self._identify_gaps(knowing_score, action_score, 
                                   knowing_text, action_text)
        
        # generate洞见
        insights = self._generate_insights(knowing_score, action_score, integration_score)
        
        result = KnowingActionAnalysis(
            knowing_level=knowing_level,
            action_quality=action_quality,
            knowing_score=knowing_score,
            action_score=action_score,
            integration_score=integration_score,
            gaps=gaps,
            insights=insights
        )
        
        self.analysis_history.append(result)
        return result
    
    def _score_knowing(self, text: str) -> float:
        """评估知的程度"""
        if not text:
            return 50.0
        
        text_lower = text.lower()
        score = 50.0
        
        # 关键词评分
        for keyword, points in self.KNOWING_KEYWORDS.items():
            if keyword in text_lower:
                score = max(score, points)
        
        # 深度metrics
        depth_indicators = ["深刻", "透彻", "真正", "彻底", "本质", "核心"]
        for indicator in depth_indicators:
            if indicator in text:
                score += 10
        
        # 表面metrics
        surface_indicators = ["大概", "似乎", "好像", "可能", "也许"]
        for indicator in surface_indicators:
            if indicator in text:
                score -= 10
        
        return max(0, min(100, score))
    
    def _score_action(self, text: str) -> float:
        """评估行的程度"""
        if not text:
            return 50.0
        
        text_lower = text.lower()
        score = 50.0
        
        # 关键词评分
        for keyword, points in self.ACTION_KEYWORDS.items():
            if keyword in text_lower:
                score = max(score, points)
        
        # actionmetrics
        action_indicators = ["做", "action", "执行", "实践", "坚持", "完成"]
        count = sum(1 for ind in action_indicators if ind in text)
        score += count * 5
        
        # 拖延metrics
        delay_indicators = ["等", "以后", "再说", "算了", "不"]
        count = sum(1 for ind in delay_indicators if ind in text_lower)
        score -= count * 8
        
        return max(0, min(100, score))
    
    def _calculate_integration(self, knowing: float, action: float) -> float:
        """计算知行合一程度"""
        if knowing == 0 or action == 0:
            return 0.0
        
        # 知行差距
        gap = abs(knowing - action)
        
        # 知行合一 = 平均分数 - 差距惩罚
        avg = (knowing + action) / 2
        penalty = gap * 0.5
        
        integration = avg - penalty
        
        return max(0, min(100, integration))
    
    def _determine_knowing_level(self, score: float) -> KnowingLevel:
        """确定知之层次"""
        if score < 30:
            return KnowingLevel.UNKNOWN
        elif score < 60:
            return KnowingLevel.THEORETICAL
        elif score < 80:
            return KnowingLevel.PARTIAL
        elif score < 95:
            return KnowingLevel.INTEGRATED
        else:
            return KnowingLevel.SPONTANEOUS
    
    def _determine_action_quality(self, score: float) -> ActionQuality:
        """确定action质量"""
        if score < 30:
            return ActionQuality.DELAYED
        elif score < 50:
            return ActionQuality.MECHANICAL
        elif score < 70:
            return ActionQuality.CONSCIOUS
        elif score < 90:
            return ActionQuality.HABITUAL
        else:
            return ActionQuality.ENLIGHTENED
    
    def _identify_gaps(self, knowing: float, action: float,
                       knowing_text: str, action_text: str) -> List[str]:
        """recognize知行差距"""
        gaps = []
        
        if knowing > action + 20:
            gaps.append("知多行少:知道很多但做得很少,需要更多实践")
            gaps.append("可能原因:缺乏action计划,意志力不足,害怕失败")
        elif action > knowing + 20:
            gaps.append("行多知少:埋头action但缺乏反思,需要深化认知")
            gaps.append("可能原因:盲目action,缺乏学习,不善于总结")
        elif knowing < 50 and action < 50:
            gaps.append("知行皆浅:需要在实践中深化认知")
        
        # 具体差距分析
        if knowing_text and action_text:
            for known, actions in self.KNOWING_ACTION_PAIRS.items():
                if known in knowing_text:
                    gap_found = False
                    for action in actions:
                        if action not in action_text:
                            gap_found = True
                    if gap_found:
                        gaps.append(f"知道'{known}',但未完全践行相应action")
        
        return gaps if gaps else ["知行基本unified"]
    
    def _generate_insights(self, knowing: float, action: float, 
                          integration: float) -> List[str]:
        """generate洞见"""
        insights = []
        
        # 整体评估
        if integration >= 80:
            insights.append("你正在接近知行合一的境界")
        elif integration >= 60:
            insights.append("你的知行有一定unified,但还有提升空间")
        else:
            insights.append("知行差距较大,需要在知或行上加强")
        
        # 具体建议
        if knowing > action:
            insights.append("关键在于action:不要等完美,现在就开始")
            insights.append("王阳明:'知是行的开始,行是知的结果'")
        elif action > knowing:
            insights.append("关键在于深化认知:边做边想,多问为什么")
            insights.append("王阳明:'真知即所以为行,不行不足以谓之知'")
        else:
            insights.append("知行平衡发展,继续保持")
        
        # 王阳明思想
        insights.append("'事上磨练':在具体事情上修炼心性")
        
        return insights
    
    def diagnose_topic(self, topic: str, knowing: str, action: str) -> Dict:
        """
        诊断具体话题的知行状态
        
        Args:
            topic: 话题(如:健康,学习,人际关系)
            knowing: 对该话题的认知
            action: 对该话题的实践
            
        Returns:
            Dict: 诊断结果
        """
        knowing_score = self._score_knowing(knowing)
        action_score = self._score_action(action)
        integration = self._calculate_integration(knowing_score, action_score)
        
        # 查找标准对照
        standard_actions = []
        for known, actions in self.KNOWING_ACTION_PAIRS.items():
            if known in knowing:
                standard_actions = actions
                break
        
        # generate诊断
        diagnosis = {
            "topic": topic,
            "knowing_score": round(knowing_score, 1),
            "action_score": round(action_score, 1),
            "integration_score": round(integration, 1),
            "diagnosis": self._get_diagnosis_text(integration),
            "standard_actions": standard_actions,
            "action_plan": self._generate_action_plan(topic, knowing_score, action_score),
            "yangming_quote": self._get_yangming_quote(topic)
        }
        
        return diagnosis
    
    def _get_diagnosis_text(self, integration: float) -> str:
        """get诊断文字"""
        if integration >= 90:
            return "知行高度unified,是该领域的典范"
        elif integration >= 70:
            return "知行基本unified,继续保持并深化"
        elif integration >= 50:
            return "知行有一定差距,需要更多实践"
        elif integration >= 30:
            return "知行差距较大,需要重新审视认知和action"
        else:
            return "知行严重脱节,需要从基础开始"
    
    def _generate_action_plan(self, topic: str, knowing: float, 
                              action: float) -> List[str]:
        """generateaction计划"""
        plan = []
        
        if knowing > action:
            # 知多行少
            plan.append(f"设定具体的action目标,不要只停留在想")
            plan.append(f"从小事开始,立刻action")
            plan.append(f"找人监督或结伴action")
        else:
            # 行多知少
            plan.append(f"action后进行复盘反思")
            plan.append(f"学习该领域的系统性知识")
            plan.append(f"理解action背后的原理")
        
        # 通用建议
        plan.append("王阳明:事上磨练,在实践中验证认知")
        
        return plan
    
    def _get_yangming_quote(self, topic: str) -> str:
        """get相关阳明语录"""
        quotes_by_topic = {
            "健康": "养生不过寡欲,然亦不是丸泥块囊也.",
            "学习": "知是行的主意,行是知的功夫;知是行之始,行是知之成.",
            "人际关系": "亲民者,兼爱众人也.",
            "事业": "致知者,诚意之本也.",
            "人生": "此心光明,亦复何言."
        }
        
        for key, quote in quotes_by_topic.items():
            if key in topic:
                return quote
        
        return "知行合一:知之真切笃实处即是行,行之明觉精察处即是知."
    
    def practice_guidance(self, analysis: KnowingActionAnalysis) -> Dict:
        """
        提供事上磨练的指导
        
        Args:
            analysis: 知行分析结果
            
        Returns:
            Dict: 实践指导
        """
        guidance = {
            "principles": [],  # 核心原则
            "methods": [],  # 方法
            "exercises": []  # 练习
        }
        
        # 根据分析结果generate指导
        if analysis.knowing_score < 60:
            guidance["principles"].append("先学后行:深入学习理论,理解本质")
            guidance["methods"].append("阅读经典著作,向有经验的人学习")
            guidance["exercises"].append("每天学习一个概念,并用自己的话解释")
        
        if analysis.action_score < 60:
            guidance["principles"].append("先行后知:在action中深化认知")
            guidance["methods"].append("设定最小action单元,立即执行")
            guidance["exercises"].append("每天完成一个小action,不要等到准备好")
        
        if analysis.integration_score < 60:
            guidance["principles"].append("知行合一:在事上磨练")
            guidance["methods"].append("每做一件事,都问自己:'我真的懂了吗?'")
            guidance["exercises"].append("记录知行日记,对照反思")
        
        # 王阳明核心思想
        guidance["principles"].append("王阳明四句教:无善无恶心之体,有善有恶意之动")
        guidance["principles"].append("知善知恶是良知,为善去恶是格物")
        
        return guidance
    
    def create_practice_case(self, title: str, description: str,
                            knowing: str, action: str) -> PracticeCase:
        """
        创建实践案例
        
        Args:
            title: 案例标题
            description: 案例描述
            knowing: 认知
            action: action
            
        Returns:
            PracticeCase: 实践案例
        """
        case = PracticeCase(
            title=title,
            description=description,
            knowing_score=self._score_knowing(knowing),
            action_score=self._score_action(action)
        )
        
        self.practice_cases.append(case)
        return case
    
    def get_summary_report(self) -> str:
        """get总结报告"""
        if not self.analysis_history:
            return "暂无分析记录"
        
        # 计算平均分
        avg_knowing = sum(a.knowing_score for a in self.analysis_history) / len(self.analysis_history)
        avg_action = sum(a.action_score for a in self.analysis_history) / len(self.analysis_history)
        avg_integration = sum(a.integration_score for a in self.analysis_history) / len(self.analysis_history)
        
        # generate报告
        report = f"""
{'='*50}
知行合一评估报告
{'='*50}

总体评分
--------
知的程度:{avg_knowing:.1f}/100
行的程度:{avg_action:.1f}/100
知行合一:{avg_integration:.1f}/100

核心发现
--------
"""
        
        if avg_knowing > avg_action:
            report += "你知多行少,需要更多action和实践\n"
        elif avg_action > avg_knowing:
            report += "你行多知少,需要深化认知和反思\n"
        else:
            report += "你知行较为平衡,继续保持\n"
        
        report += f"""
分析记录
--------
共分析 {len(self.analysis_history)} 个主题
        
实践案例
--------
共记录 {len(self.practice_cases)} 个实践案例

{'='*50}
王阳明曰:知行合一,止于至善.
{'='*50}
"""
        
        return report

def create_unity_evaluator() -> UnityKnowledgeActionEvaluator:
    """工厂函数"""
    return UnityKnowledgeActionEvaluator()
