# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze',
    'create_reverse_thinking_engine',
    'multi_mode_analysis',
    'reverse_question',
    'to_dict',
]

逆向思维引擎 v1.0.0
Reverse Thinking Engine

核心思想:
- 换一个角度思考,往往能找到解决方案
- 阻力最小的路,往往不是最短的路
- 逆向思维是从结果倒推原因
- 换位思考,理解对方的立场

作者:Somn AI
版本:v1.0.0
日期:2026-04-02
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass, field
from collections import defaultdict
import re

class ReverseMode(Enum):
    """逆向思维模式"""
    RESULT_TO_CAUSE = "结果倒推"  # 从目标倒推action
    OPPOSITE_THINKING = "对立思考"  # 思考相反的可能性
    PERSPECTIVE_TAKING = "换位思考"  # 从对方角度思考
    ASSUMPTION_QUESTIONING = "假设质疑"  # 质疑现有假设
    CONSTRAINT_REFRAMING = "约束重构"  # 把限制转化为机会
    PREVENTION_ANALYSIS = "预防分析"  # 思考如何避免失败

@dataclass
class ReverseAnalysis:
    """逆向分析结果"""
    original_problem: str
    reverse_mode: ReverseMode
    reversed_perspective: str
    key_insights: List[str] = field(default_factory=list)
    alternative_solutions: List[str] = field(default_factory=list)
    action_recommendations: List[str] = field(default_factory=list)
    confidence: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "original_problem": self.original_problem,
            "reverse_mode": self.reverse_mode.value,
            "reversed_perspective": self.reversed_perspective,
            "key_insights": self.key_insights,
            "alternative_solutions": self.alternative_solutions,
            "action_recommendations": self.action_recommendations,
            "confidence": round(self.confidence, 2)
        }

@dataclass
class PerspectiveMapping:
    """视角mapping"""
    original_view: str  # 原始视角
    reverse_view: str  # 逆向视角
    common_biases: List[str] = field(default_factory=list)

class ReverseThinkingEngine:
    """
    逆向思维引擎
    
    提供多种逆向思考方法.
    
    主要功能:
    1. 结果倒推:从目标倒推需要采取的action
    2. 对立思考:思考相反的可能性
    3. 换位思考:从对方角度理解问题
    4. 假设质疑:质疑现有的默认假设
    5. 约束重构:把限制转化为机会
    6. 预防分析:思考如何避免失败
    """
    
    # 常见认知偏差及其逆向修正
    COGNITIVE_BIASES = {
        "确认偏误": "故意寻找反对自己观点的证据",
        "损失厌恶": "思考如果不action会失去什么机会",
        "现状偏见": "想象没有现状时的选择自由",
        "后见之明": "假设回到过去,理性分析当时的选择",
        "可得性启发": "反向思考:哪些重要信息是我没看到的?",
        "锚定效应": "摆脱第一个数字,寻找新的参考点",
        "过度自信": "假设自己的judge有一半可能是错的",
        "群体思维": "想象团队里有个唱反调的人会说什么"
    }
    
    # 常见问题的逆向问法
    REVERSE_QUESTIONS = {
        "如何成功": ["如何确保失败?", "失败的最大原因是什么?"],
        "如何赚钱": ["如何确保亏钱?", "什么习惯让人破产?"],
        "如何幸福": ["什么让人不幸福?", "痛苦的根源是什么?"],
        "如何健康": ["什么让人不健康?", "损害健康的习惯有哪些?"],
        "如何成长": ["什么阻碍成长?", "什么让人停滞不前?"],
        "如何人际和谐": ["什么破坏人际关系?", "什么让关系恶化?"]
    }
    
    # 对立转换词
    OPPOSITE_PAIRS = {
        "快": "慢", "慢": "快",
        "多": "少", "少": "多",
        "大": "小", "小": "大",
        "主动": "被动", "被动": "主动",
        "进攻": "防守", "防守": "进攻",
        "竞争": "合作", "合作": "竞争",
        "集中": "分散", "分散": "集中",
        "坚持": "放弃", "放弃": "坚持",
        "理性": "感性", "感性": "理性",
        "短期": "长期", "长期": "短期",
        "结果": "过程", "过程": "结果",
        "个人": "集体", "集体": "个人",
        "内部": "外部", "外部": "内部",
        "进攻": "防守", "防守": "进攻"
    }
    
    def __init__(self):
        self.analysis_history: List[ReverseAnalysis] = []
        self.perspective_stack: List[str] = []
    
    def analyze(self, problem: str, mode: ReverseMode = ReverseMode.RESULT_TO_CAUSE) -> ReverseAnalysis:
        """逆向分析问题"""
        if mode == ReverseMode.RESULT_TO_CAUSE:
            result = self._reverse_from_result(problem)
        elif mode == ReverseMode.OPPOSITE_THINKING:
            result = self._opposite_thinking(problem)
        elif mode == ReverseMode.PERSPECTIVE_TAKING:
            result = self._perspective_taking(problem)
        elif mode == ReverseMode.ASSUMPTION_QUESTIONING:
            result = self._assumption_questioning(problem)
        elif mode == ReverseMode.CONSTRAINT_REFRAMING:
            result = self._constraint_reframing(problem)
        elif mode == ReverseMode.PREVENTION_ANALYSIS:
            result = self._prevention_analysis(problem)
        else:
            result = self._reverse_from_result(problem)
        
        self.analysis_history.append(result)
        return result
    
    def _reverse_from_result(self, problem: str) -> ReverseAnalysis:
        """结果倒推"""
        goal = problem
        for pattern in ["想要", "要", "希望", "目标是", "达到"]:
            if pattern in problem:
                goal = problem.split(pattern)[-1].strip()
                break
        
        return ReverseAnalysis(
            original_problem=problem,
            reverse_mode=ReverseMode.RESULT_TO_CAUSE,
            reversed_perspective=f"从'{goal}'这个目标倒推,我们需要...",
            key_insights=[
                "从目标倒推需要采取的具体action",
                "recognize关键的里程碑和节点",
                "思考哪些是必要条件,哪些是充分条件",
                "考虑时间线和资源需求"
            ],
            alternative_solutions=[
                "直接路径:从当前状态到目标状态",
                "间接路径:通过中间目标绕行",
                "颠覆路径:重新定义目标",
                "协作路径:借助外部力量"
            ],
            action_recommendations=[
                f"第一步:明确'{goal}'的定义和标准",
                "第二步:recognize从现在到目标的障碍",
                "第三步:找到跨越障碍的方法",
                "第四步:制定具体的action计划",
                "第五步:建立反馈和调整机制"
            ],
            confidence=0.85
        )
    
    def _opposite_thinking(self, problem: str) -> ReverseAnalysis:
        """对立思考"""
        keywords = self._extract_keywords(problem)
        transformed = problem
        for kw in keywords:
            for orig, opp in self.OPPOSITE_PAIRS.items():
                if orig in problem:
                    transformed = transformed.replace(orig, f"[{orig}/{opp}]")
        
        opposite_views = [problem.replace(kw, self.OPPOSITE_PAIRS.get(kw, kw)) 
                        for kw in keywords if kw in self.OPPOSITE_PAIRS]
        
        return ReverseAnalysis(
            original_problem=problem,
            reverse_mode=ReverseMode.OPPOSITE_THINKING,
            reversed_perspective=transformed,
            key_insights=[
                "对立思考打破惯性思维",
                "最显而易见的答案往往不是最优解",
                "转换视角可能带来突破性洞见",
                "对立面往往包含被忽视的信息"
            ],
            alternative_solutions=opposite_views or ["思考相反的可能性"],
            action_recommendations=[
                "列出当前方案的所有关键要素",
                "对每个要素,思考其对立面",
                "评估对立方案是否可行",
                "寻找整合对立面的可能性"
            ],
            confidence=0.78
        )
    
    def _perspective_taking(self, problem: str) -> ReverseAnalysis:
        """换位思考"""
        parties = self._identify_parties(problem)
        perspectives = [f"从{party}的角度看:{party}最关心的是什么?" for party in parties]
        
        return ReverseAnalysis(
            original_problem=problem,
            reverse_mode=ReverseMode.PERSPECTIVE_TAKING,
            reversed_perspective="从各利益相关方的角度看...",
            key_insights=[
                "理解对方的需求和顾虑是解决问题的前提",
                "寻找各方的共同利益点",
                "思考对方做出妥协的可能性",
                "考虑如何让对方从合作中获益"
            ],
            alternative_solutions=perspectives,
            action_recommendations=[
                f"recognize所有涉及的各方:{', '.join(parties)}",
                "列出每方最关心的问题",
                "寻找各方的共同目标",
                "设计让各方都受益的方案"
            ],
            confidence=0.82
        )
    
    def _assumption_questioning(self, problem: str) -> ReverseAnalysis:
        """假设质疑"""
        assumptions = self._identify_assumptions(problem)
        
        return ReverseAnalysis(
            original_problem=problem,
            reverse_mode=ReverseMode.ASSUMPTION_QUESTIONING,
            reversed_perspective="质疑隐藏在问题背后的假设...",
            key_insights=[
                "大多数问题都建立在隐藏的假设之上",
                "质疑假设是突破思维定式的关键",
                "最危险的假设是我们认为理所当然的",
                "打破一个关键假设可能完全改变问题"
            ],
            alternative_solutions=[f"如果假设'{a}'不成立呢?" for a in assumptions],
            action_recommendations=[
                f"recognize问题中的隐含假设:{', '.join(assumptions)}",
                "对每个假设问:'这是真的吗?'",
                "思考如果假设不成立会怎样",
                "用新的假设重新构建问题"
            ],
            confidence=0.80
        )
    
    def _constraint_reframing(self, problem: str) -> ReverseAnalysis:
        """约束重构"""
        constraints = self._identify_constraints(problem)
        
        return ReverseAnalysis(
            original_problem=problem,
            reverse_mode=ReverseMode.CONSTRAINT_REFRAMING,
            reversed_perspective="把限制转化为机会...",
            key_insights=[
                "限制往往激发创新",
                "约束条件下的解决方案更有针对性",
                "换个角度看,限制就是资源",
                "完全的自由反而可能导致无法decision"
            ],
            alternative_solutions=[f"由于'{c}',反而可以..." for c in constraints],
            action_recommendations=[
                f"列出所有的约束条件:{', '.join(constraints)}",
                "对每个约束,问:'这个约束能带来什么机会?'",
                "探索如何利用约束",
                "设计在约束下最优的方案"
            ],
            confidence=0.76
        )
    
    def _prevention_analysis(self, problem: str) -> ReverseAnalysis:
        """预防分析"""
        goal = self._extract_goal(problem)
        
        return ReverseAnalysis(
            original_problem=problem,
            reverse_mode=ReverseMode.PREVENTION_ANALYSIS,
            reversed_perspective=f"要避免无法达成'{goal}',我们需要...",
            key_insights=[
                "知道什么会导致失败,就知道如何避免",
                "预防胜于治疗",
                "最常见的失败原因往往是最容易忽视的",
                "建立预警机制比事后补救更有效"
            ],
            alternative_solutions=[
                "要确保失败,最确定的方法是什么?",
                "什么因素最可能导致无法达成目标?",
                "有哪些潜在的陷阱需要避免?"
            ],
            action_recommendations=[
                "recognize可能导致失败的因素",
                "评估每个因素发生的可能性",
                "制定预防措施",
                "建立预警metrics"
            ],
            confidence=0.88
        )
    
    def _extract_keywords(self, text: str) -> List[str]:
        return [kw for kw in self.OPPOSITE_PAIRS.keys() if kw in text]
    
    def _identify_parties(self, problem: str) -> List[str]:
        common = ["客户", "用户", "员工", "领导", "同事", "合作伙伴", "供应商", "股东"]
        return [p for p in common if p in problem] or ["相关方A", "相关方B"]
    
    def _identify_assumptions(self, problem: str) -> List[str]:
        patterns = ["我", "他们", "现在", "一直", "应该", "必须"]
        return [f"'{p}'相关的隐含假设" for p in patterns if p in problem] or [
            "假设当前的方法是正确的", "假设目标是不变的",
            "假设资源是有限的", "假设时间是不够的"
        ]
    
    def _identify_constraints(self, problem: str) -> List[str]:
        keywords = ["不能", "没有", "不够", "缺乏", "限制", "必须", "只能"]
        found = [f"包含'{k}'的限制" for k in keywords if k in problem]
        return found or ["资源限制", "能力限制", "环境限制", "心理限制"]
    
    def _extract_goal(self, problem: str) -> str:
        for pattern in ["要", "想", "希望", "目标", "达到"]:
            if pattern in problem:
                parts = problem.split(pattern)
                if len(parts) > 1:
                    return parts[-1].strip().rstrip('..,,,')
        return problem
    
    def multi_mode_analysis(self, problem: str) -> Dict:
        """多模式synthesize分析"""
        results = {}
        for mode in ReverseMode:
            results[mode.value] = self.analyze(problem, mode).to_dict()
        
        all_solutions = []
        all_recommendations = []
        for r in self.analysis_history[-6:]:
            all_solutions.extend(r.alternative_solutions[:2])
            all_recommendations.extend(r.action_recommendations[:2])
        
        return {
            "problem": problem,
            "mode_results": results,
            "integrated_solutions": list(set(all_solutions))[:5],
            "integrated_recommendations": list(set(all_recommendations))[:5],
            "best_approach": self._suggest_best_approach(problem)
        }
    
    def _suggest_best_approach(self, problem: str) -> str:
        if "冲突" in problem or "矛盾" in problem:
            return "建议使用'换位思考'模式"
        elif "失败" in problem or "避免" in problem:
            return "建议使用'预防分析'模式"
        elif "假设" in problem or "认为" in problem:
            return "建议使用'假设质疑'模式"
        elif "限制" in problem or "不能" in problem:
            return "建议使用'约束重构'模式"
        return "建议使用'结果倒推'模式"
    
    def reverse_question(self, question: str) -> Dict:
        """逆向问题generate"""
        for key, reverses in self.REVERSE_QUESTIONS.items():
            if key in question:
                return {
                    "original": question,
                    "reverse_questions": reverses,
                    "explanation": f"将'{key}'的思考方向逆转"
                }
        
        return {
            "original": question,
            "reverse_questions": [
                "如果完全相反,会是什么?",
                "什么情况会导致相反的结果?",
                "谁会希望相反的结果?"
            ],
            "explanation": "通过逆向提问探索问题另一面"
        }

def create_reverse_thinking_engine() -> ReverseThinkingEngine:
    """工厂函数"""
    return ReverseThinkingEngine()
