"""
__all__ = [
    'generate_story_strategy',
]

叙事智能引擎 - 故事驱动增长顾问
拆分自 narrative_intelligence_engine.py
"""
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

from ._nie_types import (
    NarrativeMode, NarrativeElementType, EmotionalTone,
    NarrativeElement, NarrativeStructure, NarrativeAnalysis,
)
from ._nie_analyzer import GrowthNarrativeAnalyzer
from ._nie_persona import PersonaDepthBuilder

logger = logging.getLogger(__name__)

class StoryDrivenGrowthAdvisor:
    """
    故事驱动增长顾问
    
    将文学叙事理论转化为可执行的增长strategy
    """
    
    def __init__(self):
        self.narrative_analyzer = GrowthNarrativeAnalyzer()
        self.persona_builder = PersonaDepthBuilder()
    
    def generate_story_strategy(self, business_context: Dict) -> Dict:
        """
        generate故事驱动增长strategy
        
        整合叙事分析 + 深度画像 → 可执行的增长strategy
        """
        # 1. 叙事分析
        narrative_analysis = self.narrative_analyzer.analyze_growth_narrative(business_context)
        
        # 2. 用户画像深化
        personas = business_context.get("personas", [])
        deep_personas = []
        for p in personas:
            deep_personas.append(self.persona_builder.build_deep_persona(p))
        
        # 3. generate故事框架
        story_framework = self._build_story_framework(narrative_analysis, deep_personas)
        
        # 4. generate增长strategy
        growth_strategies = self._generate_story_strategies(narrative_analysis, deep_personas)
        
        # 5. generate内容日历
        content_calendar = self._generate_content_calendar(narrative_analysis)
        
        return {
            "strategy_id": f"story_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "narrative_analysis": narrative_analysis.to_dict(),
            "deep_personas": deep_personas,
            "story_framework": story_framework,
            "growth_strategies": growth_strategies,
            "content_calendar": content_calendar,
            "narrative_metrics": self._define_narrative_metrics()
        }
    
    def _build_story_framework(self, analysis: NarrativeAnalysis, personas: List[Dict]) -> Dict:
        """构建故事框架"""
        structure = analysis.narrative_structure
        
        return {
            "core_narrative": self._generate_core_narrative(structure),
            "brand_archetype": self._identify_brand_archetype(structure),
            "narrative_voice": self._define_narrative_voice(structure),
            "key_story_beats": self._design_story_beats(structure),
            "emotional_design": {
                "target_emotions": self._identify_target_emotions(structure),
                "emotional_curve_plan": structure.emotional_curve,
                "peak_moments": self._design_peak_moments(structure)
            }
        }
    
    def _generate_core_narrative(self, structure: NarrativeStructure) -> str:
        """generate核心叙事"""
        mode = structure.mode
        title = structure.title
        theme = structure.theme
        
        templates = {
            NarrativeMode.LINEAR_ASCENT: 
                f"'{title}'--{theme}.这是一段从困境到突破的奋斗故事,"
                f"每一步都凝聚着坚持与信念.",
            NarrativeMode.CIRCULAR_DESTINY:
                f"'{title}'--{theme}.在循环中寻找突破,在轮回中发现新的可能.",
            NarrativeMode.MULTI_VOICE:
                f"'{title}'--{theme}.从不同视角讲述同一个故事,每个声音都值得被听见.",
            NarrativeMode.REALIST_WARMTH:
                f"'{title}'--{theme}.在真实中寻找温暖,在困境中坚守希望.",
            NarrativeMode.DUAL_LIGHT_DARK:
                f"'{title}'--{theme}.光与暗的交织,成就与挑战并存,真实而有力.",
            NarrativeMode.GROTESQUE_TRUTH:
                f"'{title}'--{theme}.打破表象,揭示真实."
        }
        return templates.get(mode, f"'{title}'--{theme}")
    
    def _identify_brand_archetype(self, structure: NarrativeStructure) -> str:
        """recognize品牌原型"""
        mode_archetypes = {
            NarrativeMode.LINEAR_ASCENT: "英雄/勇士",
            NarrativeMode.CIRCULAR_DESTINY: "智者/探索者",
            NarrativeMode.MULTI_VOICE: "创作者/讲故事的人",
            NarrativeMode.REALIST_WARMTH: "守护者/照料者",
            NarrativeMode.DUAL_LIGHT_DARK: "魔术师/变革者",
            NarrativeMode.GROTESQUE_TRUTH: "叛逆者/颠覆者"
        }
        return mode_archetypes.get(structure.mode, "创造者")
    
    def _define_narrative_voice(self, structure: NarrativeStructure) -> Dict:
        """定义叙事声音"""
        mode = structure.mode
        
        voice_profiles = {
            NarrativeMode.LINEAR_ASCENT: {
                "tone": "坚定,温暖,有力量",
                "reference": "路遥<平凡的世界>的叙事style",
                "key_words": ["奋斗", "坚持", "突破", "成长", "希望"],
                "avoid": ["炫耀", "浮夸", "空洞", "煽情"]
            },
            NarrativeMode.CIRCULAR_DESTINY: {
                "tone": "深沉,哲学,有洞察",
                "reference": "莫言<生死疲劳>的轮回叙事",
                "key_words": ["洞察", "规律", "本质", "真相", "循环"],
                "avoid": ["浅薄", "武断", "片面"]
            },
            NarrativeMode.MULTI_VOICE: {
                "tone": "多元,包容,有层次",
                "reference": "莫言<檀香刑>的多声部叙事",
                "key_words": ["多元", "真实", "声音", "故事", "互动"],
                "avoid": ["单一视角", "权威说教"]
            },
            NarrativeMode.REALIST_WARMTH: {
                "tone": "真诚,温暖,有人文关怀",
                "reference": "路遥<人生>的温情现实主义",
                "key_words": ["真实", "温暖", "关怀", "陪伴", "尊严"],
                "avoid": ["虚伪", "冷漠", "套路化"]
            },
            NarrativeMode.DUAL_LIGHT_DARK: {
                "tone": "真实,立体,有张力",
                "reference": "路遥之光+莫言之深的synthesize叙事",
                "key_words": ["真实", "力量", "深度", "共鸣", "成长"],
                "avoid": ["虚假", "片面", "肤浅"]
            }
        }
        return voice_profiles.get(mode, {"tone": "专业,真诚", "reference": "synthesize叙事style"})
    
    def _design_story_beats(self, structure: NarrativeStructure) -> List[Dict]:
        """设计故事节拍点"""
        mode = structure.mode
        
        beat_templates = {
            NarrativeMode.LINEAR_ASCENT: [
                {"beat": "平凡起点", "description": "展示品牌/用户最初的普通状态", "emotion": "共鸣"},
                {"beat": "困境降临", "description": "面临真实挑战和困难", "emotion": "紧张"},
                {"beat": "暗夜坚持", "description": "在看不到希望时依然坚持", "emotion": "感动"},
                {"beat": "转折出现", "description": "一个关键事件带来改变", "emotion": "振奋"},
                {"beat": "突破成功", "description": "实现阶段性目标", "emotion": "喜悦"},
                {"beat": "精神升华", "description": "超越物质成就的精神成长", "emotion": "升华"}
            ],
            NarrativeMode.CIRCULAR_DESTINY: [
                {"beat": "当前循环", "description": "描述当前所处的行业/用户循环", "emotion": "认知"},
                {"beat": "历史规律", "description": "揭示类似循环的历史规律", "emotion": "洞察"},
                {"beat": "荒诞揭示", "description": "展示循环中不合理的地方", "emotion": "反思"},
                {"beat": "打破循环", "description": "提出打破循环的新方案", "emotion": "振奋"},
                {"beat": "新叙事建立", "description": "建立新的叙事框架", "emotion": "希望"}
            ]
        }
        
        return beat_templates.get(mode, [
            {"beat": "引入", "description": "品牌/用户的故事开始", "emotion": "好奇"},
            {"beat": "发展", "description": "面临挑战和选择", "emotion": "紧张"},
            {"beat": "高潮", "description": "关键转折点", "emotion": "振奋"},
            {"beat": "解决", "description": "找到答案", "emotion": "满足"}
        ])
    
    def _identify_target_emotions(self, structure: NarrativeStructure) -> List[str]:
        """recognize目标情感"""
        mode = structure.mode
        target_map = {
            NarrativeMode.LINEAR_ASCENT: ["共鸣", "感动", "振奋", "信任", "希望"],
            NarrativeMode.CIRCULAR_DESTINY: ["好奇", "洞察", "反思", "觉醒"],
            NarrativeMode.MULTI_VOICE: ["好奇", "认同", "参与", "归属感"],
            NarrativeMode.REALIST_WARMTH: ["信任", "温暖", "安全感", "尊重"],
            NarrativeMode.DUAL_LIGHT_DARK: ["共鸣", "信任", "尊重", "忠诚"]
        }
        return target_map.get(mode, ["共鸣", "信任"])
    
    def _design_peak_moments(self, structure: NarrativeStructure) -> List[Dict]:
        """设计情感峰值时刻"""
        moments = []
        curve = structure.emotional_curve
        
        if curve:
            max_val = max(curve)
            min_val = min(curve)
            
            # 情感高点 → 品牌高光时刻
            peak_indices = [i for i, v in enumerate(curve) if v >= max_val * 0.9]
            for idx in peak_indices:
                moments.append({
                    "type": "peak",
                    "position": f"第{idx+1}阶段",
                    "purpose": "品牌高光时刻,展示核心成就",
                    "narrative_technique": "路遥式精神升华"
                })
            
            # 情感低点 → 精神考验时刻
            valley_indices = [i for i, v in enumerate(curve) if v <= min_val * 1.1]
            for idx in valley_indices:
                moments.append({
                    "type": "valley",
                    "position": f"第{idx+1}阶段",
                    "purpose": "展示真实困境,建立共情",
                    "narrative_technique": "莫言式真实揭示"
                })
        
        return moments
    
    def _generate_story_strategies(self, analysis: NarrativeAnalysis, personas: List[Dict]) -> List[Dict]:
        """generate故事驱动增长strategy"""
        strategies = []
        mode = analysis.narrative_structure.mode
        
        # 通用strategy
        strategies.append({
            "name": "品牌叙事体系构建",
            "description": f"基于{mode.value}叙事模式,构建完整的品牌叙事体系",
            "priority": "high",
            "expected_impact": "品牌认知度+30%, 用户情感连接+50%",
            "actions": [
                "梳理品牌历史中的关键故事节点",
                "确定品牌叙事的核心人物和冲突",
                "设计品牌故事的内容矩阵",
                "建立品牌叙事的视觉语言系统"
            ]
        })
        
        # 基于画本的strategy
        if personas:
            primary_persona = personas[0] if personas else {}
            narrative = primary_persona.get("narrative_intelligence", {})
            narrative_role = narrative.get("narrative_role", "参与者")
            
            strategies.append({
                "name": f"用户叙事角色激活",
                "description": f"将用户定位为'{narrative_role}',让用户成为品牌故事的主角",
                "priority": "high",
                "expected_impact": "用户参与度+40%, UGC内容+60%",
                "actions": [
                    f"设计用户'{narrative_role}'角色的内容模板",
                    "建立用户故事收集和展示机制",
                    "创建用户成长旅程的可视化工具",
                    "设计用户成就系统(路遥式阶段性成长)"
                ]
            })
        
        # 叙事化营销strategy
        strategies.append({
            "name": "叙事化内容营销",
            "description": "将产品功能转化为用户故事,用叙事替代硬广",
            "priority": "medium",
            "expected_impact": "内容转化率+25%, 分享率+35%",
            "actions": [
                "每个产品功能对应一个用户故事场景",
                "设计'路遥式'系列内容--用户奋斗故事",
                "设计'莫言式'系列内容--深度行业洞察",
                "建立内容情感标签系统,追踪情感传播效果"
            ]
        })
        
        return strategies
    
    def _generate_content_calendar(self, analysis: NarrativeAnalysis) -> List[Dict]:
        """generate叙事内容日历"""
        calendar = []
        beats = self._design_story_beats(analysis.narrative_structure)
        
        for i, beat in enumerate(beats):
            calendar.append({
                "week": i + 1,
                "theme": beat["beat"],
                "content_type": "品牌故事",
                "target_emotion": beat["emotion"],
                "content_suggestion": beat["description"],
                "channels": ["公众号", "小红书", "抖音"],
                "kpi": f"情感共鸣度目标: {beat['emotion']}"
            })
        
        return calendar
    
    def _define_narrative_metrics(self) -> Dict:
        """定义叙事效果衡量metrics"""
        return {
            "narrative_resonance_score": {
                "description": "叙事共鸣度 - 内容引发的情感共鸣程度",
                "calculation": "(互动率 × 情感正向比 × 分享率) / 展现量",
                "target": "> 0.15"
            },
            "story_consistency_score": {
                "description": "故事一致性 - 各渠道叙事的一致程度",
                "calculation": "各渠道核心叙事元素覆盖率",
                "target": "> 0.8"
            },
            "user_hero_completion_rate": {
                "description": "用户英雄旅程完成率 - 用户参与完整叙事的比例",
                "calculation": "完成预设故事触点的用户数 / 总触达用户数",
                "target": "> 0.3"
            },
            "emotional_depth_index": {
                "description": "情感深度指数 - 用户评论/反馈的情感深度",
                "calculation": "深度情感表达(>50字)的评论占比",
                "target": "> 0.2"
            }
        }

# ============================================================
# 叙事智能引擎主类
# ============================================================

