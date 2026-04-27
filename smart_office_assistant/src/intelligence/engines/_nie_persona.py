"""
__all__ = [
    'build_deep_persona',
]

叙事智能引擎 - 人物画像构建器
拆分自 narrative_intelligence_engine.py
"""
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class PersonaDepthBuilder:
    """
    深度用户画像构建器
    
    基于路遥"人物是读者精神榜样"的塑造方法,
    将用户画像从数据维度提升到精神维度
    """
    
    # 路遥人物塑造的核心原则
    LU_YAO_PRINCIPLES = {
        "真实性": "人物必须扎根于真实的生活土壤",
        "矛盾性": "好人不完美,坏人不纯粹",
        "成长性": "人物在困境中成长和蜕变",
        "代表性": "人物代表一个群体/一代人",
        "精神力量": "在苦难中展现的人性光辉"
    }
    
    # 莫言人物塑造的核心原则
    MO_YAN_PRINCIPLES = {
        "复杂性": "人性不是非黑即白的",
        "欲望驱动": "所有行为都有深层的欲望动机",
        "历史塑造": "人物是历史的产物",
        "感官体验": "通过感官细节让人物立体",
        "荒诞真实": "在极端情境中展现真实人性"
    }
    
    def __init__(self):
        self.archetype_library = self._build_archetype_library()
    
    def _build_archetype_library(self) -> Dict[str, Dict]:
        """构建基于文学作品的人物原型库"""
        return {
            "奋斗者_路遥": {
                "source": "孙少平/高加林",
                "traits": ["坚韧", "自尊", "不甘平凡", "勤奋", "理想主义"],
                "needs": ["尊重", "成长机会", "自我实现", "公平"],
                "fears": ["被看不起", "失去尊严", "停滞不前"],
                "narrative_role": "在困境中奋斗的主角",
                "growth_drivers": ["外部机遇", "内在动力", "精神榜样"],
                "business_mapping": {
                    "产品偏好": "实用,有品质,性价比",
                    "品牌吸引": "有奋斗故事的,踏实做事的",
                    "decision因素": "口碑,信任度,长期价值"
                }
            },
            "守望者_路遥": {
                "source": "孙少安/德顺老汉",
                "traits": ["踏实", "责任感强", "传统", "重情义", "忍耐"],
                "needs": ["安全感", "家庭稳定", "社会认可"],
                "fears": ["变化失控", "家人受苦", "失去根基"],
                "narrative_role": "坚守土地的守护者",
                "growth_drivers": ["稳定性", "可靠性", "信任积累"],
                "business_mapping": {
                    "产品偏好": "熟悉品牌,稳定可靠",
                    "品牌吸引": "有历史,有口碑,有社会责任感",
                    "decision因素": "安全性,口碑,品牌历史"
                }
            },
            "梦想者_路遥": {
                "source": "田晓霞",
                "traits": ["理想主义", "勇敢", "有才华", "独立思考", "温暖"],
                "needs": ["自由", "创造", "改变世界", "精神共鸣"],
                "fears": ["被束缚", "平庸", "失去自我"],
                "narrative_role": "黑暗中的光",
                "growth_drivers": ["愿景", "创意", "情感连接"],
                "business_mapping": {
                    "产品偏好": "有创意,有设计感,有社会价值",
                    "品牌吸引": "有理想,有故事,有社会使命",
                    "decision因素": "价值观匹配,创新性,社会影响力"
                }
            },
            "幸存者_莫言": {
                "source": "上官鲁氏",
                "traits": ["顽强", "务实", "狡黠", "母性", "生命力极强"],
                "needs": ["生存", "保护家人", "掌控感"],
                "fears": ["饥饿", "无力感", "失去所爱"],
                "narrative_role": "在极端环境中存活的人",
                "growth_drivers": ["适应力", "韧性", "生存智慧"],
                "business_mapping": {
                    "产品偏好": "高性价比,实用,耐用",
                    "品牌吸引": "朴实,可靠,经历过风浪",
                    "decision因素": "实际效果,价格,口碑"
                }
            },
            "叛逆者_莫言": {
                "source": "余占鳌",
                "traits": ["大胆", "冲动", "有魅力", "反叛", "原始生命力"],
                "needs": ["自由", "刺激", "征服", "被崇拜"],
                "fears": ["被束缚", "平庸", "衰老"],
                "narrative_role": "打破规则的原始力量",
                "growth_drivers": ["创新", "冒险", "个人魅力"],
                "business_mapping": {
                    "产品偏好": "新潮,独特,有冲击力",
                    "品牌吸引": "有颠覆性,有个性,有态度",
                    "decision因素": "独特性,社交资本,刺激感"
                }
            },
            "观察者_莫言": {
                "source": "莫言本人/叙述者",
                "traits": ["敏感", "幽默", "洞察力强", "超然", "多面"],
                "needs": ["理解世界", "表达", "真相"],
                "fears": ["被欺骗", "肤浅", "失去独立思考"],
                "narrative_role": "看透一切的旁观者",
                "growth_drivers": ["知识", "洞察", "独立思考"],
                "business_mapping": {
                    "产品偏好": "有深度,有内容,有独特视角",
                    "品牌吸引": "真诚,有文化,不浮夸",
                    "decision因素": "内容质量,真实度,知识价值"
                }
            }
        }
    
    def build_deep_persona(self, basic_persona: Dict) -> Dict:
        """
        构建深度用户画像
        
        在基础画像数据之上,增加文学维度的人物分析
        
        Args:
            basic_persona: 基础用户画像( demographics, behaviors, preferences 等)
        
        Returns:
            深度用户画像(增加 archetype, spiritual_needs, narrative_role 等)
        """
        # 1. 匹配文学原型
        archetypes = self._match_archetypes(basic_persona)
        
        # 2. 提取精神需求
        spiritual_needs = self._extract_spiritual_needs(basic_persona, archetypes)
        
        # 3. 确定叙事角色
        narrative_role = self._determine_narrative_role(basic_persona, archetypes)
        
        # 4. analyze_emotion驱动力
        emotional_drivers = self._analyze_emotional_drivers(basic_persona)
        
        # 5. generate路遥式+莫言式双重洞察
        dual_insights = self._generate_dual_insights(basic_persona, archetypes)
        
        return {
            **basic_persona,
            "narrative_intelligence": {
                "primary_archetype": archetypes[0] if archetypes else "unknown",
                "all_archetypes": archetypes,
                "spiritual_needs": spiritual_needs,
                "narrative_role": narrative_role,
                "emotional_drivers": emotional_drivers,
                "dual_insights": dual_insights,
                "persona_depth_score": self._calculate_depth_score(basic_persona, archetypes)
            }
        }
    
    def _match_archetypes(self, persona: Dict) -> List[str]:
        """匹配文学原型"""
        scores = {}
        
        for arch_name, arch_data in self.archetype_library.items():
            score = 0.0
            traits = arch_data["traits"]
            
            # 基于标签/兴趣匹配
            interests = persona.get("interests", persona.get("tags", []))
            if isinstance(interests, str):
                interests = [interests]
            
            for interest in interests:
                for trait in traits:
                    if any(keyword in str(interest) for keyword in [trait, trait[:2]]):
                        score += 0.2
            
            # 基于行为匹配
            behaviors = persona.get("behaviors", {})
            if isinstance(behaviors, dict):
                if behaviors.get("active_level", "") in ["high", "very_high"] and "奋斗" in traits:
                    score += 0.3
                if behaviors.get("loyalty", "") in ["high", "very_high"] and "踏实" in traits:
                    score += 0.3
            
            scores[arch_name] = score
        
        # 排序返回
        sorted_archetypes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [name for name, score in sorted_archetypes if score > 0.1][:3]
    
    def _extract_spiritual_needs(self, persona: Dict, archetypes: List[str]) -> List[str]:
        """提取精神需求"""
        needs = set()
        for arch_name in archetypes[:2]:
            arch_data = self.archetype_library.get(arch_name, {})
            needs.update(arch_data.get("needs", []))
        return list(needs)
    
    def _determine_narrative_role(self, persona: Dict, archetypes: List[str]) -> str:
        """确定用户在品牌叙事中的角色"""
        if not archetypes:
            return "观众"
        
        primary = self.archetype_library.get(archetypes[0], {})
        return primary.get("narrative_role", "参与者")
    
    def _analyze_emotional_drivers(self, persona: Dict) -> List[str]:
        """analyze_emotion驱动力"""
        drivers = []
        
        # 从用户描述中提取情感关键词
        description = persona.get("description", "")
        pain_points = persona.get("pain_points", [])
        
        if isinstance(pain_points, list):
            for pp in pain_points:
                if any(w in str(pp) for w in ["难", "苦", "累", "忙", "压力"]):
                    drivers.append("路遥式奋斗驱动: 在困境中寻求突破")
                if any(w in str(pp) for w in ["迷茫", "不确定", "混乱", "矛盾"]):
                    drivers.append("莫言式真相驱动: 在混沌中寻找真相")
        
        if not drivers:
            drivers.append("基础驱动: 功能性需求满足")
        
        return drivers
    
    def _generate_dual_insights(self, persona: Dict, archetypes: List[str]) -> Dict:
        """generate路遥+莫言双重洞察"""
        insights = {
            "路遥之光": [],
            "莫言之深": []
        }
        
        for arch_name in archetypes[:2]:
            if "路遥" in arch_name:
                source = self.archetype_library[arch_name].get("source", "")
                mapping = self.archetype_library[arch_name].get("business_mapping", {})
                insights["路遥之光"].append(
                    f"该用户群体类似于{source}的读者群体--"
                    f"他们需要'精神榜样'式的品牌连接,而非单纯的功能推销."
                    f"产品偏好: {mapping.get('产品偏好', '注重品质')}"
                )
            elif "莫言" in arch_name:
                source = self.archetype_library[arch_name].get("source", "")
                mapping = self.archetype_library[arch_name].get("business_mapping", {})
                insights["莫言之深"].append(
                    f"该用户群体类似于{source}的读者群体--"
                    f"他们欣赏真实和深度,反感虚伪和肤浅."
                    f"品牌沟通需要展现'复杂性'和'真实感'."
                    f"decision因素: {mapping.get('decision因素', '真实度')}"
                )
        
        if not insights["路遥之光"]:
            insights["路遥之光"].append("建议用温情和希望的故事与该用户群体建立情感连接")
        if not insights["莫言之深"]:
            insights["莫言之深"].append("建议展现品牌真实的一面,用深度内容赢得该用户群体的尊重")
        
        return insights
    
    def _calculate_depth_score(self, persona: Dict, archetypes: List[str]) -> float:
        """计算画像深度分数"""
        score = 0.0
        info_fields = ["demographics", "behaviors", "preferences", "pain_points", "goals"]
        for f in info_fields:
            if persona.get(f):
                score += 0.15
        score += len(archetypes) * 0.1
        return min(1.0, score)

