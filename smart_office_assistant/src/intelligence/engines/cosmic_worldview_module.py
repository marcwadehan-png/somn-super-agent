# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze_worldview',
    'create_cosmic_module',
    'expand_perspective',
    'get_cosmic_wisdom',
    'multi_scale_analysis',
    'think_probabilistically',
]

宇宙观认知模块 v1.0.0
Cosmic Worldview Module

基于<宇宙另一种真相><天才向左疯子向右>核心思想构建

核心思想:
- 宇宙观决定世界观,世界观决定人生观
- 量子思维:不确定性是本质
- 概率世界观:一切都以概率存在
- 跳出常规思维,看到更大的图景

作者:Somn AI
版本:v1.0.0
日期:2026-04-02
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict

class WorldviewType(Enum):
    """世界观类型"""
    NEWTONIAN = "牛顿世界观"  # 确定性,机械论
    PROBABILISTIC = "概率世界观"  # 概率论,统计学
    QUANTUM = "量子世界观"  # 不确定性,叠加态
    COMPLEXITY = "复杂性世界观"  # 涌现,非线性
    ECOSYSTEM = "生态系统观"  # 相互依存,演化

class ThinkingScale(Enum):
    """思维尺度"""
    MICRO = "微观"  # 细节,具体
    MESO = "中观"  # 系统,关联
    MACRO = "宏观"  # 大局,趋势
    META = "元观"  # 超越,反思

@dataclass
class CosmicInsight:
    """宇宙认知洞见"""
    topic: str
    conventional_view: str  # 常规视角
    expanded_view: str  # 扩展视角
    implications: List[str]
    practical_applications: List[str]

class CosmicWorldviewModule:
    """
    宇宙观认知模块
    
    基于<宇宙另一种真相>构建,帮助用户拓展思维尺度,
    建立更宏大的宇宙观认知框架.
    
    主要功能:
    1. 世界观类型分析
    2. 思维尺度训练
    3. 概率思维培养
    4. 复杂系统思维
    """
    
    # 世界观characteristics
    WORLDVIEW_FEATURES = {
        WorldviewType.NEWTONIAN: {
            "核心假设": "世界是确定的,可预测的",
            "思维特点": "线性因果,还原论,机械论",
            "优势": "简单直接,易于理解",
            "局限": "忽视不确定性和复杂性"
        },
        WorldviewType.PROBABILISTIC: {
            "核心假设": "一切以概率存在",
            "思维特点": "统计思维,期望值,风险评估",
            "优势": "考虑不确定性",
            "局限": "难以精确预测个体"
        },
        WorldviewType.QUANTUM: {
            "核心假设": "观察者影响被观察者",
            "思维特点": "可能性思维,叠加态思维",
            "优势": "超越二元对立",
            "局限": "容易陷入不可知论"
        },
        WorldviewType.COMPLEXITY: {
            "核心假设": "整体大于部分之和",
            "思维特点": "系统思维,涌现思维",
            "优势": "理解复杂系统",
            "局限": "难以精确控制"
        },
        WorldviewType.ECOSYSTEM: {
            "核心假设": "万物相互依存",
            "思维特点": "生态思维,演化思维",
            "优势": "长期视野,共赢思维",
            "局限": "action见效慢"
        }
    }
    
    # 思维尺度视角
    SCALE_PERSPECTIVES = {
        ThinkingScale.MICRO: {
            "关注": "细节,具体,局部",
            "优势": "精确,专业,执行",
            "局限": "可能只见树木不见森林",
            "适用": "技术问题,执行细节"
        },
        ThinkingScale.MESO: {
            "关注": "系统,关联,过程",
            "优势": "全面,平衡",
            "局限": "可能缺乏深度",
            "适用": "战略规划,项目管理"
        },
        ThinkingScale.MACRO: {
            "关注": "大局,趋势,长期",
            "优势": "战略高度,前瞻性",
            "局限": "可能脱离实际",
            "适用": "顶层设计,长期规划"
        },
        ThinkingScale.META: {
            "关注": "本质,假设,反思",
            "优势": "深刻,创新",
            "局限": "可能过于抽象",
            "适用": "根本问题,范式转变"
        }
    }
    
    def __init__(self):
        self.insights_cache: List[CosmicInsight] = []
    
    def analyze_worldview(self, text: str = "") -> Dict:
        """
        分析世界观类型
        
        Args:
            text: 关于思维方式的描述
            
        Returns:
            Dict: 世界观分析
        """
        # 基于文本关键词judge
        text_lower = text.lower()
        
        scores = defaultdict(float)
        
        # 牛顿世界观metrics
        if any(kw in text_lower for kw in ["确定", "必然", "一定", "肯定"]):
            scores[WorldviewType.NEWTONIAN] += 30
        
        # 概率世界观metrics
        if any(kw in text_lower for kw in ["可能", "概率", "风险", "不确定", "也许"]):
            scores[WorldviewType.PROBABILISTIC] += 30
        
        # 量子世界观metrics
        if any(kw in text_lower for kw in ["叠加", "观察", "量子", "波函数"]):
            scores[WorldviewType.QUANTUM] += 30
        
        # 复杂性世界观metrics
        if any(kw in text_lower for kw in ["系统", "涌现", "整体", "复杂", "网络"]):
            scores[WorldviewType.COMPLEXITY] += 30
        
        # 生态系统观metrics
        if any(kw in text_lower for kw in ["生态", "演化", "依存", "共赢", "长期"]):
            scores[WorldviewType.ECOSYSTEM] += 30
        
        # 确定主导世界观
        if scores:
            dominant = max(scores.items(), key=lambda x: x[1])
            dominant_type = dominant[0]
        else:
            dominant_type = WorldviewType.NEWTONIAN  # 默认
        
        features = self.WORLDVIEW_FEATURES.get(dominant_type, {})
        
        return {
            "dominant_worldview": dominant_type.value,
            "features": features,
            "scale_scores": dict(scores),
            "advice": self._get_worldview_advice(dominant_type)
        }
    
    def _get_worldview_advice(self, worldview: WorldviewType) -> str:
        """get世界观建议"""
        advices = {
            WorldviewType.NEWTONIAN: "尝试接受不确定性,培养概率思维",
            WorldviewType.PROBABILISTIC: "保持对风险的敏感,同时敢于action",
            WorldviewType.QUANTUM: "在可能性中寻找确定,创造你观察到的现实",
            WorldviewType.COMPLEXITY: "关注系统涌现效应,不要只关注线性因果",
            WorldviewType.ECOSYSTEM: "考虑长期和整体,追求共赢而非零和"
        }
        return advices.get(worldview, "持续扩展你的世界观")
    
    def multi_scale_analysis(self, problem: str) -> Dict:
        """
        多尺度分析问题
        
        Args:
            problem: 待分析的问题
            
        Returns:
            Dict: 多尺度分析结果
        """
        analysis = {
            "problem": problem,
            "scales": {}
        }
        
        for scale in ThinkingScale:
            perspective = self.SCALE_PERSPECTIVES[scale]
            
            analysis["scales"][scale.value] = {
                "perspective": perspective["关注"],
                "viewpoint": self._get_scale_viewpoint(problem, scale),
                "advantages": perspective["优势"],
                "applications": self._get_scale_applications(problem, scale)
            }
        
        # generatesynthesize视角
        analysis["synthesis"] = self._synthesize_scales(problem, analysis["scales"])
        
        return analysis
    
    def _get_scale_viewpoint(self, problem: str, scale: ThinkingScale) -> str:
        """get尺度视角"""
        if scale == ThinkingScale.MICRO:
            return f"从微观细节看'{problem}':具体是什么?如何执行?"
        elif scale == ThinkingScale.MESO:
            return f"从系统关联看'{problem}':涉及哪些环节?相互关系如何?"
        elif scale == ThinkingScale.MACRO:
            return f"从宏观大局看'{problem}':趋势如何?长期影响?"
        else:  # META
            return f"从元视角反思'{problem}':为什么会有这个问题?框架本身有问题吗?"
    
    def _get_scale_applications(self, problem: str, scale: ThinkingScale) -> List[str]:
        """get尺度应用"""
        if scale == ThinkingScale.MICRO:
            return ["制定详细的执行计划", "recognize具体的障碍点", "量化关键metrics"]
        elif scale == ThinkingScale.MESO:
            return ["画系统流程图", "recognize关键节点", "设计反馈机制"]
        elif scale == ThinkingScale.MACRO:
            return ["分析趋势数据", "考虑长期后果", "制定战略方向"]
        else:  # META
            return ["质疑基本假设", "寻找替代框架", "重新定义问题"]
    
    def _synthesize_scales(self, problem: str, scales: Dict) -> Dict:
        """synthesize多尺度视角"""
        return {
            "recommended_approach": "先用宏观确定方向,再用微观落地执行",
            "action_sequence": [
                "1. 从宏观角度看为什么这个问题重要",
                "2. 从元视角质疑问题的前提是否正确",
                "3. 从中观角度recognize系统中的关键杠杆点",
                "4. 从微观角度制定具体action计划"
            ],
            "key_insight": f"'{problem}'在不同尺度下有不同含义,解决方案也应多尺度协调"
        }
    
    def expand_perspective(self, statement: str) -> CosmicInsight:
        """
        扩展视角
        
        Args:
            statement: 原始陈述
            
        Returns:
            CosmicInsight: 宇宙认知洞见
        """
        # 基于陈述recognize主题
        topic = self._extract_topic(statement)
        
        # generate常规视角
        conventional = self._get_conventional_view(topic)
        
        # generate扩展视角
        expanded = self._get_expanded_view(topic)
        
        # recognize含义
        implications = self._get_implications(topic)
        
        # 实际应用
        applications = self._get_applications(topic)
        
        insight = CosmicInsight(
            topic=topic,
            conventional_view=conventional,
            expanded_view=expanded,
            implications=implications,
            practical_applications=applications
        )
        
        self.insights_cache.append(insight)
        return insight
    
    def _extract_topic(self, text: str) -> str:
        """提取主题"""
        topics = ["成功", "失败", "时间", "人生", "努力", "选择", "幸福", "痛苦",
                 "知识", "智慧", "竞争", "合作", "风险", "机会", "成长"]
        
        for topic in topics:
            if topic in text:
                return topic
        
        return "事物"
    
    def _get_conventional_view(self, topic: str) -> str:
        """get常规视角"""
        views = {
            "成功": "成功是达到预定的目标和结果",
            "失败": "失败是不好的,应该避免",
            "时间": "时间是线性的,一去不复返",
            "人生": "人生是有限的,要及时行乐",
            "努力": "努力就会有回报",
            "选择": "选择有好坏之分",
            "幸福": "幸福是获得想要的东西",
            "痛苦": "痛苦是不好的,应该消除",
            "知识": "知识是可以确定的",
            "智慧": "智慧是知道正确答案",
            "竞争": "竞争是你死我活的零和游戏",
            "合作": "合作是牺牲自己的利益",
            "风险": "风险应该最小化",
            "机会": "机会是稀缺的",
            "成长": "成长是线性的,渐进的"
        }
        return views.get(topic, f"{topic}是确定的,可控的")
    
    def _get_expanded_view(self, topic: str) -> str:
        """get扩展视角"""
        views = {
            "成功": "成功是持续成长和创造价值的过程,失败也是成功的一部分",
            "失败": "失败是学习的机会和信息反馈,没有失败就没有成长",
            "时间": "时间可能是主观的,高峰体验中时间会变慢",
            "人生": "人生是意识的体验,意义是创造的而非发现的",
            "努力": "刻意练习比努力更重要,方向比努力更重要",
            "选择": "每个选择都创造新的可能性,没有绝对的好坏",
            "幸福": "幸福是全身心投入生活的能力,而非结果的副产品",
            "痛苦": "痛苦是成长的信号,逃避痛苦也逃避了成长",
            "知识": "所有知识都有前提假设,质疑是进步的起点",
            "智慧": "智慧是知道边界在哪里,承认无知是智慧的开始",
            "竞争": "竞争可以激发创新,也可以导致内耗",
            "合作": "合作可以创造增量价值,是更高维度的竞争",
            "风险": "风险与机会并存,追求零风险意味着零机会",
            "机会": "机会是可以创造的,限制思维限制了机会",
            "成长": "成长可能是突变的,在积累临界点后爆发"
        }
        return views.get(topic, f"换个角度看{topic}会有新的发现")
    
    def _get_implications(self, topic: str) -> List[str]:
        """get含义"""
        return [
            "世界是复杂的,单一视角往往不完整",
            "不确定性是本质,确定性是例外",
            "思维尺度影响认知结论",
            "接受不确定性才能更好地action"
        ]
    
    def _get_applications(self, topic: str) -> List[str]:
        """get实际应用"""
        return [
            "做重大decision时,从多个尺度思考",
            "面对不确定性时,用概率思维评估",
            "遇到困难时,尝试转换视角",
            "保持谦逊,承认认知的局限性"
        ]
    
    def think_probabilistically(self, statement: str) -> Dict:
        """
        概率思维训练
        
        Args:
            statement: 需要用概率思维审视的陈述
            
        Returns:
            Dict: 概率思维分析
        """
        return {
            "original_statement": statement,
            "probability_version": self._to_probability(statement),
            "confidence_assessment": self._assess_confidence(statement),
            "alternative_scenarios": self._generate_scenarios(statement),
            "decision_advice": self._probabilistic_advice(statement)
        }
    
    def _to_probability(self, statement: str) -> str:
        """转换为概率表述"""
        replacements = {
            "一定": "很可能(70%)",
            "肯定": "大概率(80%)",
            "绝对": "极高概率(90%)",
            "不可能": "极低概率(5%)",
            "肯定不会": "小概率(10%)"
        }
        
        result = statement
        for old, new in replacements.items():
            if old in statement:
                result = result.replace(old, new)
        
        return result if result != statement else statement + "(概率待评估)"
    
    def _assess_confidence(self, statement: str) -> str:
        """评估置信度"""
        if any(kw in statement for kw in ["一定", "绝对", "肯定", "总是"]):
            return "低置信度 - 这些词暗示过度确定性"
        elif any(kw in statement for kw in ["可能", "也许", "大概", "通常"]):
            return "中等置信度 - 已考虑不确定性"
        else:
            return "建议明确置信水平"
    
    def _generate_scenarios(self, statement: str) -> List[str]:
        """generate替代场景"""
        return [
            "乐观场景:假设有利条件全部具备",
            "悲观场景:假设不利因素全部出现",
            "基准场景:最可能的情况",
            "黑天鹅场景:假设完全出乎意料的情况"
        ]
    
    def _probabilistic_advice(self, statement: str) -> str:
        """概率思维建议"""
        return "在不确定的世界中,追求好的概率比追求确定性更现实"
    
    def get_cosmic_wisdom(self) -> List[str]:
        """get宇宙智慧语录"""
        wisdoms = [
            "宇宙中有1400亿个星系,每个星系有数千亿颗恒星--我们如此渺小,却能思考宇宙.",
            "你所看到的颜色只是电磁波谱的极小部分,我们活在一个充满看不见的世界里.",
            "量子力学告诉我们,观察者影响被观察者--我们参与创造现实.",
            "熵增定律告诉我们,宇宙正在从有序走向无序,但生命却在创造有序.",
            "进化告诉我们,最适应的不一定是最强的,而是最灵活的.",
            "复杂系统告诉我们,整体大于部分之和,涌现不可预测.",
            "贝叶斯定理告诉我们,认知应该随新证据更新.",
            "熵的视角看,成功是创造局部有序,失败是接受全局无序."
        ]
        return wisdoms

def create_cosmic_module() -> CosmicWorldviewModule:
    """工厂函数"""
    return CosmicWorldviewModule()
