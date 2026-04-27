# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze_comprehensive',
    'analyze_growth_mindset',
    'analyze_learning_path',
    'analyze_self_growth',
    'assess_knowledge_action',
    'assess_learning',
    'create_closed_loop_task',
    'create_thinking_growth_unified',
    'declutter_space',
    'expand_cosmic_view',
    'get_system_capabilities',
    'growth_self_check',
    'quick_analyze',
]

成长思维智慧unified系统 v1.0.0
Thinking & Growth Wisdom Unified System

整合基于30本成长思维类书籍的核心智慧:
- 成长型思维:<终身成长>
- 逆向思维:<逆转思维><逆思维心理学>
- 闭环思维:<闭环思维>
- 自卑超越:<自卑与超越>
- 知行合一:王阳明xinxue
- 高效学习:<超级记忆力训练法><高效阅读>
- 宇宙观:<宇宙另一种真相>
- 极简专注:<极简主义><大脑整理术>
- 思维fusion:<底层逻辑><格局>

作者:Somn AI
版本:v1.0.0
日期:2026-04-02
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from .growth_mindset_evaluator import GrowthMindsetEvaluator, create_growth_mindset_evaluator
from ..reasoning.reverse_thinking_engine import ReverseThinkingEngine, ReverseMode, create_reverse_thinking_engine
from .closed_loop_system import ClosedLoopThinkingSystem, create_closed_loop_system
from .transcend_inferiority_engine import TranscendInferiorityEngine, create_transcend_engine
from .unity_knowledge_action import UnityKnowledgeActionEvaluator, create_unity_evaluator
from .efficient_learning_core import EfficientLearningCore, create_efficient_learning_core
from .cosmic_worldview_module import CosmicWorldviewModule, ThinkingScale, create_cosmic_module
from .minimalist_focus_system import MinimalistFocusSystem, DeclutterArea, create_minimalist_system
from .thinking_mode_fusion_engine import ThinkingModeFusionEngine, ThinkingMode, create_fusion_engine

@dataclass
class UnifiedAnalysis:
    """unified分析结果"""
    problem: str
    growth_mindset: Dict = field(default_factory=dict)
    reverse_analysis: Dict = field(default_factory=dict)
    closed_loop: Dict = field(default_factory=dict)
    thinking_fusion: Dict = field(default_factory=dict)
    final_recommendations: List[str] = field(default_factory=list)

class ThinkingGrowthUnifiedSystem:
    """
    成长思维智慧unified系统
    
    整合9大思维成长子系统,提供unified的分析入口.
    
    子系统:
    1. 成长型思维评估器 - 评估成长vs固定思维
    2. 逆向思维引擎 - 多角度逆向分析
    3. 闭环思维系统 - 确保知行闭环
    4. 自卑超越引擎 - 阿德勒心理学应用
    5. 知行合一评估器 - 王阳明xinxue应用
    6. 高效学习核心 - 科学学习方法
    7. 宇宙观认知模块 - 宏大视角思维
    8. 极简专注系统 - 简化与专注
    9. 思维模式fusion引擎 - 多模式整合
    """
    
    def __init__(self):
        # init_all子系统
        self.growth_evaluator = create_growth_mindset_evaluator()
        self.reverse_engine = create_reverse_thinking_engine()
        self.closed_loop = create_closed_loop_system()
        self.transcend_engine = create_transcend_engine()
        self.unity_evaluator = create_unity_evaluator()
        self.learning_core = create_efficient_learning_core()
        self.cosmic_module = create_cosmic_module()
        self.minimalist = create_minimalist_system()
        self.fusion_engine = create_fusion_engine()
    
    def analyze_comprehensive(self, problem: str, context: str = "") -> UnifiedAnalysis:
        """
        synthesize分析问题
        
        Args:
            problem: 待分析的问题
            context: 背景上下文
            
        Returns:
            UnifiedAnalysis: unified分析结果
        """
        result = UnifiedAnalysis(problem=problem)
        
        # 1. 成长型思维分析
        growth_result = self.growth_evaluator.analyze_text(context or problem)
        result.growth_mindset = growth_result.to_dict()
        
        # 2. 逆向思维分析
        reverse_result = self.reverse_engine.multi_mode_analysis(problem)
        result.reverse_analysis = reverse_result
        
        # 3. 思维fusion分析
        profile = self.fusion_engine.analyze_problem(problem)
        fusion_result = self.fusion_engine.fuse_decision(profile)
        result.thinking_fusion = fusion_result
        
        # 4. generatesynthesize建议
        result.final_recommendations = self._synthesize_recommendations(result)
        
        return result
    
    def _synthesize_recommendations(self, result: UnifiedAnalysis) -> List[str]:
        """synthesize各系统建议"""
        recommendations = []
        
        # 成长型思维建议
        if result.growth_mindset.get("overall_score", 50) < 60:
            recommendations.append("培养成长型思维:把挑战视为学习机会,把错误当作老师")
        
        # 逆向思维建议
        if "best_approach" in result.reverse_analysis:
            recommendations.append(result.reverse_analysis["best_approach"])
        
        # 思维fusion建议
        if result.thinking_fusion.get("key_insight"):
            recommendations.append(result.thinking_fusion["key_insight"])
        
        # 去重并限制
        unique_recs = list(dict.fromkeys(recommendations))
        return unique_recs[:5]
    
    def analyze_learning_path(self, topic: str, current_level: str = "初学者") -> Dict:
        """
        分析学习路径
        
        Args:
            topic: 学习主题
            current_level: 当前水平
            
        Returns:
            Dict: 学习路径分析
        """
        # 学习style评估
        style = self.learning_core.assess_learning_style()
        
        # 推荐记忆技巧
        techniques = self.learning_core.recommend_techniques(topic)
        
        # 创建学习计划
        plan = self.learning_core.create_study_plan(topic, current_level)
        
        # 专注力训练
        focus = self.learning_core.get_focus_training()
        
        return {
            "topic": topic,
            "learning_style": style.to_dict(),
            "recommended_techniques": [
                {"name": t.technique.value, "description": t.description}
                for t in techniques[:3]
            ],
            "study_plan": plan,
            "focus_training": focus
        }
    
    def analyze_growth_mindset(self, text: str) -> Dict:
        """
        分析成长型思维
        
        Args:
            text: 待分析文本
            
        Returns:
            Dict: 成长型思维分析
        """
        score = self.growth_evaluator.analyze_text(text)
        recommendations = self.growth_evaluator.get_recommendations(score)
        
        return {
            "score": score.to_dict(),
            "recommendations": [
                {"category": r.category, "advice": r.growth_belief, "actions": r.action_suggestions}
                for r in recommendations
            ],
            "growth_plan": self.growth_evaluator.generate_growth_plan(score)
        }
    
    def create_closed_loop_task(self, task_name: str, 
                                description: str = "") -> Dict:
        """
        创建闭环任务
        
        Args:
            task_name: 任务名称
            description: 任务描述
            
        Returns:
            Dict: 任务状态
        """
        loop = self.closed_loop.create_loop(task_name, description, template="task")
        return self.closed_loop.get_loop_status(loop.loop_id)
    
    def assess_knowledge_action(self, knowing: str = "", action: str = "") -> Dict:
        """
        评估知行状态
        
        Args:
            knowing: 关于"知"的描述
            action: 关于"行"的描述
            
        Returns:
            Dict: 知行分析
        """
        analysis = self.unity_evaluator.analyze("", action, knowing + action)
        guidance = self.unity_evaluator.practice_guidance(analysis)
        
        return {
            "analysis": analysis.to_dict(),
            "guidance": guidance,
            "yangming_quotes": [
                "知是行的开始,行是知的完成",
                "知行合一,致良知"
            ]
        }
    
    def declutter_space(self, area: str, items: List[str]) -> Dict:
        """
        整理空间
        
        Args:
            area: 整理领域(物理/数字/精神/时间/人际)
            items: 待整理项目
            
        Returns:
            Dict: 整理结果
        """
        area_map = {
            "物理": DeclutterArea.PHYSICAL,
            "数字": DeclutterArea.DIGITAL,
            "精神": DeclutterArea.MENTAL,
            "时间": DeclutterArea.SCHEDULE,
            "人际": DeclutterArea.RELATIONSHIPS
        }
        
        declutter_area = area_map.get(area, DeclutterArea.PHYSICAL)
        result = self.minimalist.declutter_area(declutter_area, items)
        
        return {
            "area": result.area.value,
            "removed": result.items_removed,
            "retained": result.items_retained,
            "space_freed": result.space_freed,
            "emotional_relief": result.emotional_relief,
            "minimalism_tips": self.minimalist.get_minimalism_quotes()[:3]
        }
    
    def expand_cosmic_view(self, statement: str) -> Dict:
        """
        拓展宇宙观视角
        
        Args:
            statement: 原始陈述
            
        Returns:
            Dict: 宇宙认知分析
        """
        # 多尺度分析
        multi_scale = self.cosmic_module.multi_scale_analysis(statement)
        
        # 概率思维训练
        probabilistic = self.cosmic_module.think_probabilistically(statement)
        
        # 扩展视角
        insight = self.cosmic_module.expand_perspective(statement)
        
        return {
            "original": statement,
            "multi_scale_view": multi_scale,
            "probabilistic_thinking": probabilistic,
            "expanded_view": {
                "topic": insight.topic,
                "conventional": insight.conventional_view,
                "expanded": insight.expanded_view,
                "implications": insight.implications,
                "applications": insight.practical_applications
            },
            "cosmic_wisdom": self.cosmic_module.get_cosmic_wisdom()[:2]
        }
    
    def analyze_self_growth(self, reflection: str) -> Dict:
        """
        自我成长分析
        
        Args:
            reflection: 自我反思文本
            
        Returns:
            Dict: 成长分析
        """
        # 自卑超越分析
        transcend = self.transcend_engine.comprehensive_analysis(reflection)
        
        # 成长型思维分析
        growth = self.analyze_growth_mindset(reflection)
        
        return {
            "transcend_analysis": transcend,
            "growth_mindset": growth,
            "integrated_insights": [
                f"自卑感可能来源:{transcend['inferiority_analysis'][0]['type'] if transcend['inferiority_analysis'] else '待探索'}",
                f"应对style:{transcend['coping_style']['dominant_style']}",
                f"成长思维评分:{growth['score']['overall_score']}/100"
            ],
            "action_recommendations": self._generate_growth_actions(transcend, growth)
        }
    
    def _generate_growth_actions(self, transcend: Dict, growth: Dict) -> List[str]:
        """generate成长action建议"""
        actions = []
        
        # 基于自卑分析
        if transcend.get("inferiority_analysis"):
            for analysis in transcend["inferiority_analysis"][:2]:
                actions.append(f"探索{analysis['type']}相关的自卑感来源")
        
        # 基于成长思维
        recommendations = growth.get("recommendations", [])
        if recommendations:
            actions.append(f"优先改进:{recommendations[0]['category']}")
        
        return actions[:5]
    
    def get_system_capabilities(self) -> Dict:
        """get系统能力总览"""
        return {
            "system_name": "成长思维智慧unified系统 v1.0.0",
            "core_capabilities": {
                "growth_mindset": {
                    "name": "成长型思维评估器",
                    "description": "评估固定型vs成长型思维倾向",
                    "key_method": "GrowthMindsetEvaluator"
                },
                "reverse_thinking": {
                    "name": "逆向思维引擎",
                    "description": "6种逆向思考模式",
                    "key_method": "ReverseThinkingEngine"
                },
                "closed_loop": {
                    "name": "闭环思维系统",
                    "description": "确保知行闭环,PDCA循环",
                    "key_method": "ClosedLoopThinkingSystem"
                },
                "transcend": {
                    "name": "自卑超越引擎",
                    "description": "基于阿德勒心理学的超越路径",
                    "key_method": "TranscendInferiorityEngine"
                },
                "unity_knowledge_action": {
                    "name": "知行合一评估器",
                    "description": "王阳明xinxue的知行观",
                    "key_method": "UnityKnowledgeActionEvaluator"
                },
                "efficient_learning": {
                    "name": "高效学习核心",
                    "description": "学习style+记忆技巧+阅读方法",
                    "key_method": "EfficientLearningCore"
                },
                "cosmic_view": {
                    "name": "宇宙观认知模块",
                    "description": "宏大视角思维训练",
                    "key_method": "CosmicWorldviewModule"
                },
                "minimalist_focus": {
                    "name": "极简专注系统",
                    "description": "简化与专注力训练",
                    "key_method": "MinimalistFocusSystem"
                },
                "thinking_fusion": {
                    "name": "思维模式fusion引擎",
                    "description": "9+种思维模式整合",
                    "key_method": "ThinkingModeFusionEngine"
                }
            },
            "integration_apis": {
                "analyze_comprehensive": "synthesize分析入口",
                "analyze_learning_path": "学习路径分析",
                "analyze_growth_mindset": "成长思维分析",
                "assess_knowledge_action": "知行评估",
                "expand_cosmic_view": "宇宙观拓展",
                "analyze_self_growth": "自我成长分析"
            }
        }

def create_thinking_growth_unified() -> ThinkingGrowthUnifiedSystem:
    """工厂函数:创建unified系统"""
    return ThinkingGrowthUnifiedSystem()

# 便捷函数
def quick_analyze(problem: str) -> Dict:
    """快速分析问题"""
    system = create_thinking_growth_unified()
    result = system.analyze_comprehensive(problem)
    return result.final_recommendations

def assess_learning(topic: str) -> Dict:
    """快速学习评估"""
    system = create_thinking_growth_unified()
    return system.analyze_learning_path(topic)

def growth_self_check(text: str) -> Dict:
    """快速自我成长检查"""
    system = create_thinking_growth_unified()
    return system.analyze_growth_mindset(text)

# 向后兼容别名
ThinkingGrowthUnified = ThinkingGrowthUnifiedSystem  # 兼容 global_wisdom_scheduler.py 导入
