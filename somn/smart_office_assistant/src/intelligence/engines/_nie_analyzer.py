"""
__all__ = [
    'analyze_growth_narrative',
]

叙事智能引擎 - 增长叙事分析器
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

logger = logging.getLogger(__name__)

class GrowthNarrativeAnalyzer:
    """
    增长叙事分析器
    
    将文学叙事结构应用于商业增长分析:
    - 路遥的线性上升 → 增长轨迹规划
    - 莫言的循环轮回 → 周期性行业/复购分析
    - 人物弧光 → 用户生命周期分析
    - 冲突设计 → 痛点与需求recognize
    """
    
    def __init__(self):
        # 文学知识库:莫言+路遥的叙事模式
        self.narrative_patterns = self._load_narrative_patterns()
        # 情感词典
        self.emotion_lexicon = self._build_emotion_lexicon()
        # 叙事模板
        self.narrative_templates = self._build_narrative_templates()
    
    def _load_narrative_patterns(self) -> Dict:
        """加载文学叙事模式知识"""
        return {
            "路遥_线性上升": {
                "description": "从低谷到高峰的线性成长叙事",
                "key_features": ["苦难起点", "持续奋斗", "阶段性突破", "精神升华"],
                "emotional_curve": [0.2, 0.3, 0.4, 0.55, 0.7, 0.85, 0.95],
                "applicable_scenarios": ["创业故事", "品牌成长", "用户从新到忠诚"],
                "representative_work": "<平凡的世界>- 孙少平的成长弧线",
                "growth_mapping": {
                    "苦难起点": "业务冷启动/零用户",
                    "持续奋斗": "产品迭代/渠道拓展",
                    "阶段性突破": "关键里程碑达成",
                    "精神升华": "品牌价值观确立"
                }
            },
            "莫言_循环轮回": {
                "description": "循环往复的宿命叙事",
                "key_features": ["轮回结构", "荒诞转折", "暴力循环", "历史重演"],
                "emotional_curve": [0.5, 0.8, 0.3, 0.9, 0.2, 0.85, 0.4],
                "applicable_scenarios": ["行业周期分析", "复购循环", "用户流失回流"],
                "representative_work": "<生死疲劳>- 西门闹六道轮回",
                "growth_mapping": {
                    "轮回结构": "用户生命周期循环",
                    "荒诞转折": "市场突发事件",
                    "暴力循环": "价格战/竞争加剧",
                    "历史重演": "行业历史规律"
                }
            },
            "莫言_多声部": {
                "description": "多视角并行叙事",
                "key_features": ["多元视角", "声音交织", "真相碎片化", "读者参与"],
                "emotional_curve": [0.4, 0.7, 0.5, 0.8, 0.6, 0.9, 0.7],
                "applicable_scenarios": ["多用户画像分析", "多渠道增长", "品牌口碑管理"],
                "representative_work": "<酒国>- 双线叙事 / <檀香刑>- 多声部",
                "growth_mapping": {
                    "多元视角": "不同用户群体的视角",
                    "声音交织": "多渠道数据整合",
                    "真相碎片化": "用户反馈碎片化",
                    "读者参与": "UGC/社区互动"
                }
            },
            "路遥_温情现实主义": {
                "description": "温情而不回避苦难的现实主义",
                "key_features": ["真实困境", "人性温暖", "尊严坚守", "希望不灭"],
                "emotional_curve": [0.3, 0.4, 0.35, 0.5, 0.6, 0.75, 0.8],
                "applicable_scenarios": ["品牌危机公关", "用户信任重建", "社会责任营销"],
                "representative_work": "<人生>- 高加林的两难选择",
                "growth_mapping": {
                    "真实困境": "坦诚面对问题",
                    "人性温暖": "展现人文关怀",
                    "尊严坚守": "品牌价值观底线",
                    "希望不灭": "展望积极未来"
                }
            },
            "光暗交织": {
                "description": "路遥之光照耀+莫言之暗揭示的synthesize叙事",
                "key_features": ["光暗并存", "真实立体", "情感张力", "深层共鸣"],
                "emotional_curve": [0.4, 0.7, 0.3, 0.8, 0.5, 0.9, 0.6],
                "applicable_scenarios": ["品牌故事", "创始人叙事", "企业文化传播", "年度报告"],
                "representative_work": "路遥+莫言的synthesize智慧",
                "growth_mapping": {
                    "光暗并存": "成就与挑战并存",
                    "真实立体": "多维度的品牌形象",
                    "情感张力": "引发用户深层共鸣",
                    "深层共鸣": "建立品牌情感连接"
                }
            }
        }
    
    def _build_emotion_lexicon(self) -> Dict[str, List[str]]:
        """构建情感词典"""
        return {
            "hope": ["希望", "机遇", "增长", "突破", "未来", "进步", "发展", "升级"],
            "despair": ["困局", "瓶颈", "衰退", "危机", "失败", "淘汰", "缩水", "下滑"],
            "struggle": ["努力", "奋斗", "坚持", "突破", "挑战", "拼搏", "攻坚", "冲刺"],
            "warmth": ["温暖", "关怀", "帮助", "支持", "信任", "陪伴", "守护", "共情"],
            "cruelty": ["残酷", "暴力", "血腥", "毁灭", "碾压", "吞噬", "撕裂", "打击"],
            "rebellion": ["颠覆", "创新", "变革", "突破", "破局", "反击", "逆袭", "翻盘"],
            "elevation": ["升华", "超越", "卓越", "巅峰", "传奇", "伟大", "不朽", "永恒"],
            "irony": ["讽刺", "荒诞", "矛盾", "悖论", "反转", "意外", "嘲讽", "戏谑"]
        }
    
    def _build_narrative_templates(self) -> Dict[str, Dict]:
        """构建叙事模板"""
        return {
            "brand_origin_story": {
                "name": "品牌起源故事",
                "mode": NarrativeMode.LINEAR_ASCENT,
                "structure": [
                    NarrativeElementType.CONFLICT,    # 遇到问题
                    NarrativeElementType.SUFFERING,   # 深感痛苦
                    NarrativeElementType.TURNING_POINT,  # 转折出现
                    NarrativeElementType.ASCENT,      # 奋斗突破
                    NarrativeElementType.RESOLUTION   # 成功解决
                ],
                "template": "当[目标用户]面临[痛点]时,[品牌]因为[创始人初心]而诞生."
                           "起初[艰难起步],但[品牌]坚持[核心价值],"
                           "终于在[关键转折]后实现了[成就],"
                           "证明了[品牌理念]."
            },
            "growth_journey": {
                "name": "增长旅程叙事",
                "mode": NarrativeMode.DUAL_LIGHT_DARK,
                "structure": [
                    NarrativeElementType.PROTAGONIST,    # 用户/品牌
                    NarrativeElementType.CONFLICT,       # 面临挑战
                    NarrativeElementType.SUFFERING,      # 经历困难
                    NarrativeElementType.TURNING_POINT,  # 发现方法
                    NarrativeElementType.ASCENT,         # 获得增长
                    NarrativeElementType.CLIMAX,        # 达到高潮
                    NarrativeElementType.RESOLUTION      # 新的起点
                ],
                "template": "从[起始状态]到[当前成就],[主体]经历了[核心挑战]."
                           "在[低谷时刻],[转折因素]带来了改变,"
                           "通过[关键action]实现了[增长成果]."
                           "但这不是终点,而是[新愿景]的开始."
            },
            "user_hero_journey": {
                "name": "用户英雄旅程",
                "mode": NarrativeMode.LINEAR_ASCENT,
                "structure": [
                    NarrativeElementType.PROTAGONIST,
                    NarrativeElementType.CONFLICT,
                    NarrativeElementType.SUFFERING,
                    NarrativeElementType.TURNING_POINT,
                    NarrativeElementType.CLIMAX,
                    NarrativeElementType.RESOLUTION
                ],
                "description": "将用户放在英雄位置,品牌作为导师/伙伴",
                "template": "你(用户)在[场景]中面临[挑战],"
                           "感到[痛苦情绪].[品牌]提供了[解决方案],"
                           "帮助你[获得成长],最终[实现目标]."
            },
            "crisis_narrative": {
                "name": "危机叙事",
                "mode": NarrativeMode.REALIST_WARMTH,
                "structure": [
                    NarrativeElementType.THEME,
                    NarrativeElementType.CONFLICT,
                    NarrativeElementType.SUFFERING,
                    NarrativeElementType.TURNING_POINT,
                    NarrativeElementType.RESOLUTION
                ],
                "description": "路遥式温情现实主义应用于危机沟通",
                "template": "[品牌]始终坚守[核心价值].在[危机事件]中,"
                           "我们坦诚面对[问题],积极采取[action],"
                           "因为我们相信[信念]."
            }
        }
    
    def analyze_growth_narrative(self, business_context: Dict) -> NarrativeAnalysis:
        """
        分析业务增长的叙事结构
        
        将商业数据转化为叙事结构,recognize增长故事线
        """
        analysis_id = f"narrative_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # 1. 提取叙事元素
        elements = self._extract_narrative_elements(business_context)
        
        # 2. 选择叙事模式
        mode = self._select_narrative_mode(business_context, elements)
        
        # 3. 构建情感曲线
        emotional_curve = self._build_emotional_curve(business_context, mode)
        
        # 4. generate叙事结构
        structure = NarrativeStructure(
            mode=mode,
            elements=elements,
            title=self._generate_narrative_title(business_context),
            theme=self._extract_theme(business_context),
            arc_type=self._determine_arc_type(mode, emotional_curve),
            emotional_curve=emotional_curve
        )
        
        # 5. generate洞察
        insights = self._generate_narrative_insights(structure, business_context)
        
        # 6. generate建议
        recommendations = self._generate_narrative_recommendations(structure, business_context)
        
        # 7. 计算置信度
        confidence = self._calculate_confidence(structure, business_context)
        
        return NarrativeAnalysis(
            analysis_id=analysis_id,
            analysis_type="growth_narrative",
            narrative_structure=structure,
            insights=insights,
            recommendations=recommendations,
            confidence=confidence,
            metadata={"business_context": business_context}
        )
    
    def _extract_narrative_elements(self, context: Dict) -> List[NarrativeElement]:
        """从业务上下文中提取叙事元素"""
        elements = []
        elem_id = 0
        
        # 主角 = 品牌或核心用户
        brand_name = context.get("brand_name", "品牌")
        elements.append(NarrativeElement(
            id=f"elem_{elem_id}",
            element_type=NarrativeElementType.PROTAGONIST,
            content=f"{brand_name}是故事的主角",
            emotional_tone=EmotionalTone.HOPE,
            importance=1.0,
            metadata={"brand": brand_name}
        ))
        elem_id += 1
        
        # 冲突 = 核心挑战/痛点
        challenges = context.get("main_challenges", context.get("challenges", []))
        if challenges:
            challenge_text = "; ".join(challenges[:3])
            elements.append(NarrativeElement(
                id=f"elem_{elem_id}",
                element_type=NarrativeElementType.CONFLICT,
                content=f"面临的核心挑战: {challenge_text}",
                emotional_tone=EmotionalTone.STRUGGLE,
                importance=0.95,
                metadata={"challenges": challenges}
            ))
            elem_id += 1
        
        # 苦难 = 困境/低谷
        stage = context.get("stage", "growth")
        if stage in ["struggle", "early", "seed"]:
            elements.append(NarrativeElement(
                id=f"elem_{elem_id}",
                element_type=NarrativeElementType.SUFFERING,
                content=f"当前处于{stage}阶段,面临艰苦的早期探索",
                emotional_tone=EmotionalTone.DESPAIR,
                importance=0.85,
                metadata={"stage": stage}
            ))
            elem_id += 1
        
        # 转折点 = 关键机会
        opportunities = context.get("opportunities", [])
        if opportunities:
            elements.append(NarrativeElement(
                id=f"elem_{elem_id}",
                element_type=NarrativeElementType.TURNING_POINT,
                content=f"关键转折: {opportunities[0] if isinstance(opportunities, list) else opportunities}",
                emotional_tone=EmotionalTone.REBELLION,
                importance=0.9,
                metadata={"opportunities": opportunities}
            ))
            elem_id += 1
        
        # 奋斗/上升 = 增长目标
        goals = context.get("growth_goals", context.get("goals", []))
        if goals:
            elements.append(NarrativeElement(
                id=f"elem_{elem_id}",
                element_type=NarrativeElementType.ASCENT,
                content=f"增长目标: {'; '.join(goals[:3]) if isinstance(goals, list) else goals}",
                emotional_tone=EmotionalTone.ELEVATION,
                importance=0.9,
                metadata={"goals": goals}
            ))
            elem_id += 1
        
        # 主题 = 品牌价值观
        values = context.get("brand_values", context.get("values", []))
        if values:
            elements.append(NarrativeElement(
                id=f"elem_{elem_id}",
                element_type=NarrativeElementType.THEME,
                content=f"品牌价值观: {'; '.join(values[:3]) if isinstance(values, list) else values}",
                emotional_tone=EmotionalTone.ELEVATION,
                importance=0.8,
                metadata={"values": values}
            ))
            elem_id += 1
        
        return elements
    
    def _select_narrative_mode(self, context: Dict, elements: List[NarrativeElement]) -> NarrativeMode:
        """智能选择叙事模式"""
        stage = context.get("stage", "growth")
        industry = context.get("industry", "")
        
        # 早期/创业阶段 → 路遥式线性上升
        if stage in ["seed", "early", "struggle"]:
            return NarrativeMode.LINEAR_ASCENT
        
        # 成熟期/周期性行业 → 莫言式循环叙事
        if stage in ["mature", "decline"] or "cycle" in industry.lower():
            return NarrativeMode.CIRCULAR_DESTINY
        
        # 多渠道/多产品线 → 多声部
        channels = context.get("channels", [])
        products = context.get("products", [])
        if len(channels) > 2 or len(products) > 2:
            return NarrativeMode.MULTI_VOICE
        
        # 危机/负面情况 → 温情现实主义
        if context.get("crisis", False) or context.get("negative_situation", False):
            return NarrativeMode.REALIST_WARMTH
        
        # 默认 → 光暗交织
        return NarrativeMode.DUAL_LIGHT_DARK
    
    def _build_emotional_curve(self, context: Dict, mode: NarrativeMode) -> List[float]:
        """构建情感曲线"""
        pattern = self.narrative_patterns.get(mode.value.replace("_", "_"), None)
        
        if pattern:
            # 基于文学模式的情感曲线
            base_curve = pattern["emotional_curve"]
            # 根据业务上下文调整
            stage = context.get("stage", "growth")
            stage_adjust = {"seed": 0.7, "early": 0.8, "growth": 0.9, "mature": 1.0, "decline": 0.6}
            factor = stage_adjust.get(stage, 0.8)
            
            return [min(1.0, v * factor) for v in base_curve]
        
        # 默认情感曲线
        return [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    
    def _generate_narrative_title(self, context: Dict) -> str:
        """generate叙事标题"""
        brand = context.get("brand_name", "品牌")
        stage = context.get("stage", "growth")
        stage_names = {
            "seed": "启航", "early": "探索", "growth": "崛起",
            "mature": "卓越", "decline": "重生", "struggle": "突围"
        }
        stage_name = stage_names.get(stage, "成长")
        return f"{brand}的{stage_name}之路"
    
    def _extract_theme(self, context: Dict) -> str:
        """提取叙事主题"""
        challenges = context.get("main_challenges", [])
        goals = context.get("growth_goals", [])
        
        if challenges and goals:
            return f"在{'与'.join(str(c) for c in challenges[:2])}中追求{'与'.join(str(g) for g in goals[:2])}"
        elif challenges:
            return f"应对{'与'.join(str(c) for c in challenges[:2])}的挑战"
        else:
            return "持续增长与创新突破"
    
    def _determine_arc_type(self, mode: NarrativeMode, curve: List[float]) -> str:
        """确定叙事弧线类型"""
        if len(curve) < 2:
            return "rise"
        
        if mode == NarrativeMode.CIRCULAR_DESTINY:
            return "circular"
        
        first_half = sum(curve[:len(curve)//2]) / max(len(curve)//2, 1)
        second_half = sum(curve[len(curve)//2:]) / max(len(curve) - len(curve)//2, 1)
        
        if second_half > first_half * 1.1:
            return "rise"
        elif second_half < first_half * 0.9:
            return "fall"
        else:
            return "rise_fall"
    
    def _generate_narrative_insights(self, structure: NarrativeStructure, context: Dict) -> List[str]:
        """generate叙事洞察"""
        insights = []
        mode_name = structure.mode.value
        
        pattern = self.narrative_patterns.get(mode_name, {})
        
        if pattern:
            insights.append(f"叙事模式: {pattern.get('description', mode_name)}")
            insights.append(f"文学参照: {pattern.get('representative_work', '')}")
        
        # 路遥式洞察
        if structure.mode in [NarrativeMode.LINEAR_ASCENT, NarrativeMode.REALIST_WARMTH, NarrativeMode.DUAL_LIGHT_DARK]:
            insights.append("路遥叙事智慧: 苦难是起点而非终点,关键在于持续的奋斗和精神的升华")
            insights.append("增长revelations: 用户更愿意支持一个'从困境中奋斗出来'的品牌,而非天生完美的品牌")
        
        # 莫言式洞察
        if structure.mode in [NarrativeMode.CIRCULAR_DESTINY, NarrativeMode.MULTI_VOICE, NarrativeMode.GROTESQUE_TRUTH, NarrativeMode.DUAL_LIGHT_DARK]:
            insights.append("莫言叙事智慧: 真实比完美更有力量,揭示暗面比粉饰太平更能建立信任")
            insights.append("增长revelations: 多视角叙事能触及不同用户群体的真实需求,建立更深层的情感连接")
        
        # 情感曲线分析
        if structure.emotional_curve:
            peak_idx = structure.emotional_curve.index(max(structure.emotional_curve))
            valley_idx = structure.emotional_curve.index(min(structure.emotional_curve))
            insights.append(f"情感高点在第{peak_idx+1}阶段,建议在此处设计品牌高光时刻")
            if valley_idx != peak_idx:
                insights.append(f"情感低谷在第{valley_idx+1}阶段,此处是'路遥式'精神考验的关键叙事点")
        
        return insights
    
    def _generate_narrative_recommendations(self, structure: NarrativeStructure, context: Dict) -> List[str]:
        """generate叙事建议"""
        recommendations = []
        
        # 基于叙事模式的建议
        mode_rec = {
            NarrativeMode.LINEAR_ASCENT: [
                "构建'从零到一'的品牌起源故事",
                "展示团队在困难时期的坚持和奋斗",
                "设计清晰的阶段性里程碑叙事",
                "用'路遥式'精神榜样形象建立用户情感连接"
            ],
            NarrativeMode.CIRCULAR_DESTINY: [
                "分析用户生命周期中的循环模式",
                "设计复购和回流的'轮回'机制",
                "recognize行业周期规律,提前布局",
                "用'莫言式'深层洞察揭示用户行为的内在逻辑"
            ],
            NarrativeMode.MULTI_VOICE: [
                "收集并展示不同用户群体的真实声音",
                "构建多渠道叙事矩阵,覆盖多元视角",
                "鼓励UGC内容,让用户成为叙事参与者",
                "整合碎片化用户反馈,形成完整的故事图景"
            ],
            NarrativeMode.REALIST_WARMTH: [
                "坦诚面对问题,展现真实的人性温度",
                "在危机沟通中坚持路遥式的尊严坚守",
                "设计有温度的客服和服务体验",
                "用社会责任action展现品牌的'光'"
            ],
            NarrativeMode.DUAL_LIGHT_DARK: [
                "平衡展示成就与挑战,建立真实立体的品牌形象",
                "用光暗对比创造情感张力",
                "设计'从黑暗走向光明'的核心叙事线",
                "在企业文化中融入'路遥之光+莫言之深'的双重智慧"
            ]
        }
        
        recommendations.extend(mode_rec.get(structure.mode, []))
        return recommendations
    
    def _calculate_confidence(self, structure: NarrativeStructure, context: Dict) -> float:
        """计算分析置信度"""
        confidence = 0.5
        
        # 上下文越完整,置信度越高
        info_fields = ["brand_name", "stage", "main_challenges", "growth_goals", "industry"]
        filled = sum(1 for f in info_fields if f in context and context[f])
        confidence += filled * 0.08
        
        # 叙事元素越多,越可信
        confidence += min(0.2, len(structure.elements) * 0.03)
        
        return min(1.0, confidence)

