"""
__all__ = [
    'create_arc',
    'create_growth_tracker',
    'get_arc_visualization',
    'get_transformation_report',
    'record_interaction',
]

用户成长弧线追踪系统 (User Growth Arc Tracker)
==========================================

基于漫威宇宙叙事模式的成长追踪系统

功能:
1. 漫威式角色弧线可视化
2. 成长阶段recognize与追踪
3. 里程碑成就系统
4. 身份标记积累
5. 导师/盟友关系追踪
6. 转化程度评估

版本:v1.0.0
日期:2026-04-02
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

class GrowthPhase(Enum):
    """成长阶段"""
    DORMANT = ("休眠", 0)
    AWAKENING = ("觉醒", 1)
    CHALLENGING = ("挑战", 2)
    BREAKTHROUGH = ("突破", 3)
    INTEGRATING = ("整合", 4)
    MASTERY = ("精通", 5)

class MilestoneType(Enum):
    """里程碑类型"""
    TRIAL_COMPLETED = "试炼完成"
    WISDOM_GAINED = "智慧获得"
    RELATIONSHIP_BUILT = "关系建立"
    SHADOW_CONFRONTED = "阴影面对"
    IDENTITY_MARKED = "身份标记"
    TRANSFORMATION = "蜕变"

@dataclass
class Milestone:
    """里程碑"""
    milestone_id: str
    milestone_type: MilestoneType
    title: str
    description: str
    achieved_at: str
    growth_impact: float  # 对成长的影响值 0-1
    wisdom_gained: List[str]
    character_development: str

@dataclass
class Relationship:
    """关系"""
    entity_id: str
    entity_name: str
    relationship_type: str  # mentor, ally, opponent, guide
    interactions: int
    trust_level: float  # 0-1
    key_moments: List[str]

@dataclass
class IdentityMarker:
    """身份标记"""
    marker_id: str
    label: str
    acquired_at: str
    description: str
    significance: float  # 0-1

@dataclass
class ShadowWork:
    """阴影工作记录"""
    shadow_id: str
    shadow_name: str
    confronted_at: Optional[str]
    integration_status: str  # confronted, integrating, integrated
    lesson_learned: str

@dataclass
class GrowthArc:
    """成长弧线"""
    arc_id: str
    user_id: str
    started_at: str
    current_phase: GrowthPhase
    transformation_level: float  # 0-1

    # 轨迹
    phase_history: List[Dict[str, Any]]
    milestones: List[Milestone]
    identity_markers: List[IdentityMarker]

    # 关系
    mentors: List[Relationship]
    allies: List[Relationship]

    # 挑战
    shadows_confronted: List[ShadowWork]
    lessons_learned: List[str]

    # 能力
    capabilities: Dict[str, float]  # 能力名称 -> 熟练度 0-1
    wisdom_accumulated: List[str]

    # 元数据
    total_interactions: int
    breakthrough_count: int
    setback_count: int

class UserGrowthTracker:
    """
    用户成长弧线追踪系统

    基于漫威宇宙的角色成长模式,提供个人成长追踪
    """

    # 成长模板
    GROWTH_TEMPLATES = {
        "iron_man_arc": {
            "name": "救赎者弧线",
            "description": "从自我中心的破坏者到愿意为更大善牺牲的守护者",
            "milestones": [
                {"type": MilestoneType.TRIAL_COMPLETED, "title": "第一滴血", "description": "第一次意识到自己造成的后果"},
                {"type": MilestoneType.SHADOW_CONFRONTED, "title": "直面贪婪", "description": "面对自己为了利润不顾后果的本质"},
                {"type": MilestoneType.RELATIONSHIP_BUILT, "title": "第一个盟友", "description": "找到一个真正信任的人"},
                {"type": MilestoneType.WISDOM_GAINED, "title": "承担责任", "description": "理解能力与责任的必然联系"},
                {"type": MilestoneType.TRANSFORMATION, "title": "最后的选择", "description": "愿意为更大善牺牲一切"}
            ]
        },
        "captain_america_arc": {
            "name": "信念守护者弧线",
            "description": "从一个想要贡献的年轻人到一个坚守信念的守护者",
            "milestones": [
                {"type": MilestoneType.TRIAL_COMPLETED, "title": "注射血清", "description": "外在力量获得,但考验才刚刚开始"},
                {"type": MilestoneType.SHADOW_CONFRONTED, "title": "冰封苏醒", "description": "失去整个时代,直面孤独"},
                {"type": MilestoneType.RELATIONSHIP_BUILT, "title": "新的战斗", "description": "找到新的战斗理由和战友"},
                {"type": MilestoneType.IDENTITY_MARKED, "title": "选择而非命运", "description": "理解信念是选择而非命运"},
                {"type": MilestoneType.TRANSFORMATION, "title": "那支舞", "description": "完成未竟的心愿,完整人生"}
            ]
        },
        "spider_man_arc": {
            "name": "邻家英雄弧线",
            "description": "从一个追逐认可的少年到一个为责任放手的成熟英雄",
            "milestones": [
                {"type": MilestoneType.TRIAL_COMPLETED, "title": "第一套制服", "description": "获得能力,开始英雄之旅"},
                {"type": MilestoneType.WISDOM_GAINED, "title": "本叔叔的教诲", "description": "学习能力与责任的真正含义"},
                {"type": MilestoneType.SHADOW_CONFRONTED, "title": "失去导师", "description": "面对失去的痛苦,继承遗志"},
                {"type": MilestoneType.IDENTITY_MARKED, "title": "我就是蜘蛛侠", "description": "不再寻求认可,自我定义身份"},
                {"type": MilestoneType.TRANSFORMATION, "title": "放手的智慧", "description": "理解有时候最好的帮助是让他人自己成长"}
            ]
        },
        "thor_arc": {
            "name": "失落之王弧线",
            "description": "从傲慢的王子到放下王位,守护更广大世界的成熟神",
            "milestones": [
                {"type": MilestoneType.TRIAL_COMPLETED, "title": "被放逐", "description": "失去神力和身份,从零开始"},
                {"type": MilestoneType.SHADOW_CONFRONTED, "title": "失去一切", "description": "面对最深的失去--阿斯加德"},
                {"type": MilestoneType.WISDOM_GAINED, "title": "真正的力量", "description": "理解力量来自内心而非武器"},
                {"type": MilestoneType.RELATIONSHIP_BUILT, "title": "与弟弟和解", "description": "接受洛基是家人,即使他是敌人"},
                {"type": MilestoneType.TRANSFORMATION, "title": "新的使命", "description": "成为银河系守护者,重新定义身份"}
            ]
        },
        "bucky_arc": {
            "name": "重建自我弧线",
            "description": "从被操控的武器到重新掌握自己命运的人",
            "milestones": [
                {"type": MilestoneType.SHADOW_CONFRONTED, "title": "记忆恢复", "description": "面对被操控期间造成的伤害"},
                {"type": MilestoneType.WISDOM_GAINED, "title": "不是我的错", "description": "理解洗脑状态下的行为不是自由选择"},
                {"type": MilestoneType.RELATIONSHIP_BUILT, "title": "找到盟友", "description": "找到那些接受真实自我的人"},
                {"type": MilestoneType.IDENTITY_MARKED, "title": "我是巴基", "description": "拒绝'冬兵'标签,宣布身份"},
                {"type": MilestoneType.TRANSFORMATION, "title": "成为猎鹰", "description": "接过盾牌,守护美国队长的遗志"}
            ]
        }
    }

    def __init__(self):
        self.user_arcs: Dict[str, GrowthArc] = {}

    def create_arc(self, user_id: str, arc_type: str = "iron_man_arc") -> GrowthArc:
        """
        创建成长弧线

        Args:
            user_id: 用户ID
            arc_type: 弧线模板类型

        Returns:
            GrowthArc: 新的成长弧线
        """
        if arc_type not in self.GROWTH_TEMPLATES:
            arc_type = "iron_man_arc"

        template = self.GROWTH_TEMPLATES[arc_type]

        arc = GrowthArc(
            arc_id=f"arc_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            user_id=user_id,
            started_at=datetime.now().isoformat(),
            current_phase=GrowthPhase.DORMANT,
            transformation_level=0.0,
            phase_history=[],
            milestones=[],
            identity_markers=[],
            mentors=[],
            allies=[],
            shadows_confronted=[],
            lessons_learned=[],
            capabilities={},
            wisdom_accumulated=[],
            total_interactions=0,
            breakthrough_count=0,
            setback_count=0
        )

        self.user_arcs[user_id] = arc

        return arc

    def record_interaction(self, user_id: str, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        记录一次交互,更新成长弧线

        Args:
            user_id: 用户ID
            interaction_data: 交互数据,包含类型,内容,影响等

        Returns:
            Dict: 更新后的状态和成长洞见
        """
        if user_id not in self.user_arcs:
            self.create_arc(user_id)

        arc = self.user_arcs[user_id]
        arc.total_interactions += 1

        result = {"phase": arc.current_phase.value[0], "growth": 0.0, "insights": []}

        # 根据交互类型更新弧线
        interaction_type = interaction_data.get("type", "exploration")

        if interaction_type == "milestone":
            milestone = self._add_milestone(arc, interaction_data)
            result["insights"].append(f"🏆 里程碑达成:{milestone.title}")
            result["growth"] += milestone.growth_impact

        elif interaction_type == "lesson":
            arc.lessons_learned.append(interaction_data.get("content", ""))
            result["growth"] += 0.02
            result["insights"].append("💡 新的领悟")

        elif interaction_type == "breakthrough":
            arc.breakthrough_count += 1
            arc.transformation_level = min(1.0, arc.transformation_level + 0.1)
            arc.current_phase = self._calculate_phase(arc)
            result["growth"] = 0.1
            result["insights"].append("⚡ 突破性成长!")
            result["phase_change"] = arc.current_phase.value[0]

        elif interaction_type == "setback":
            arc.setback_count += 1
            result["insights"].append("🌙 暂时的挫折...但挫折也是成长的一部分")
            result["growth"] = -0.02

        elif interaction_type == "relationship":
            self._add_relationship(arc, interaction_data)
            result["growth"] += 0.03
            result["insights"].append(f"🤝 {interaction_data.get('entity_name', '某人')}成为你旅程中的重要存在")

        elif interaction_type == "wisdom":
            arc.wisdom_accumulated.append(interaction_data.get("content", ""))
            result["growth"] += 0.02
            result["insights"].append("📚 智慧积累")

        elif interaction_type == "capability":
            capability = interaction_data.get("capability", "未知")
            improvement = interaction_data.get("improvement", 0.05)
            arc.capabilities[capability] = min(1.0, arc.capabilities.get(capability, 0) + improvement)
            result["growth"] += improvement
            result["insights"].append(f"⚡ {capability}能力提升")

        elif interaction_type == "shadow":
            self._add_shadow_work(arc, interaction_data)
            result["growth"] += 0.05
            result["insights"].append("🌑 你直面了内心的阴影")

        # 更新整体转化水平
        arc.transformation_level = min(1.0, arc.transformation_level + result["growth"])

        # 记录相位历史
        arc.phase_history.append({
            "phase": arc.current_phase.value[0],
            "transformation_level": arc.transformation_level,
            "interaction_type": interaction_type,
            "timestamp": datetime.now().isoformat()
        })

        return result

    def _add_milestone(self, arc: GrowthArc, data: Dict[str, Any]) -> Milestone:
        """添加里程碑"""
        milestone = Milestone(
            milestone_id=f"ms_{len(arc.milestones)}",
            milestone_type=data.get("type", MilestoneType.TRIAL_COMPLETED),
            title=data.get("title", "未命名里程碑"),
            description=data.get("description", ""),
            achieved_at=datetime.now().isoformat(),
            growth_impact=data.get("growth_impact", 0.1),
            wisdom_gained=data.get("wisdom_gained", []),
            character_development=data.get("character_development", "")
        )
        arc.milestones.append(milestone)
        return milestone

    def _add_relationship(self, arc: GrowthArc, data: Dict[str, Any]) -> Relationship:
        """添加关系"""
        rel_type = data.get("relationship_type", "ally")

        relationship = Relationship(
            entity_id=data.get("entity_id", f"entity_{len(arc.allies) + len(arc.mentors)}"),
            entity_name=data.get("entity_name", "神秘盟友"),
            relationship_type=rel_type,
            interactions=1,
            trust_level=data.get("trust_level", 0.5),
            key_moments=[data.get("key_moment", "第一次相遇")]
        )

        if rel_type == "mentor":
            arc.mentors.append(relationship)
        else:
            arc.allies.append(relationship)

        return relationship

    def _add_shadow_work(self, arc: GrowthArc, data: Dict[str, Any]) -> ShadowWork:
        """添加阴影工作记录"""
        shadow = ShadowWork(
            shadow_id=f"shadow_{len(arc.shadows_confronted)}",
            shadow_name=data.get("shadow_name", "未知的阴影"),
            confronted_at=datetime.now().isoformat(),
            integration_status="confronted",
            lesson_learned=data.get("lesson", "")
        )
        arc.shadows_confronted.append(shadow)
        return shadow

    def _calculate_phase(self, arc: GrowthArc) -> GrowthPhase:
        """根据转化水平计算相位"""
        level = arc.transformation_level

        if level < 0.1:
            return GrowthPhase.DORMANT
        elif level < 0.3:
            return GrowthPhase.AWAKENING
        elif level < 0.5:
            return GrowthPhase.CHALLENGING
        elif level < 0.7:
            return GrowthPhase.BREAKTHROUGH
        elif level < 0.9:
            return GrowthPhase.INTEGRATING
        else:
            return GrowthPhase.MASTERY

    def get_arc_visualization(self, user_id: str) -> Dict[str, Any]:
        """
        get成长弧线可视化数据

        漫威式角色卡片展示
        """
        if user_id not in self.user_arcs:
            return {"status": "no_arc", "message": "还没有开始成长旅程"}

        arc = self.user_arcs[user_id]

        # 计算能力条
        capability_bars = {}
        for capability, level in arc.capabilities.items():
            bar_length = int(level * 10)
            capability_bars[capability] = {
                "level": level,
                "bar": "█" * bar_length + "░" * (10 - bar_length)
            }

        # get当前阶段信息
        phase_info = {
            GrowthPhase.DORMANT: {"title": "🌱 休眠状态", "description": "潜能正在积蓄,等待觉醒", "progress": "0-10%"},
            GrowthPhase.AWAKENING: {"title": "⚡ 觉醒中", "description": "开始意识到需要改变", "progress": "10-30%"},
            GrowthPhase.CHALLENGING: {"title": "🔥 挑战模式", "description": "正在经历考验和试炼", "progress": "30-50%"},
            GrowthPhase.BREAKTHROUGH: {"title": "💥 突破时刻", "description": "重大突破即将到来", "progress": "50-70%"},
            GrowthPhase.INTEGRATING: {"title": "🌈 整合阶段", "description": "将新获得的智慧整合进自我", "progress": "70-90%"},
            GrowthPhase.MASTERY: {"title": "✨ 精通境界", "description": "达到新的高度,准备新的旅程", "progress": "90-100%"}
        }

        current_phase_info = phase_info.get(arc.current_phase, phase_info[GrowthPhase.DORMANT])

        # generate英雄称号
        hero_title = self._generate_hero_title(arc)

        visualization = {
            "hero_card": {
                "user_id": user_id,
                "hero_title": hero_title,
                "transformation_level": f"{int(arc.transformation_level * 100)}%",
                "current_phase": current_phase_info["title"],
                "phase_description": current_phase_info["description"],
                "progress_visual": self._generate_progress_bar(arc.transformation_level)
            },
            "journey_stats": {
                "total_interactions": arc.total_interactions,
                "breakthroughs": arc.breakthrough_count,
                "setbacks": arc.setback_count,
                "milestones_achieved": len(arc.milestones),
                "relationships_formed": len(arc.mentors) + len(arc.allies),
                "shadows_confronted": len(arc.shadows_confronted)
            },
            "capabilities": capability_bars,
            "recent_milestones": [
                {
                    "title": m.title,
                    "type": m.milestone_type.value,
                    "achieved_at": m.achieved_at[:10]
                } for m in arc.milestones[-3:]
            ],
            "relationships": {
                "mentors": [r.entity_name for r in arc.mentors],
                "allies": [r.entity_name for r in arc.allies]
            },
            "wisdom_accumulated": arc.wisdom_accumulated[-5:] if arc.wisdom_accumulated else [],
            "next_recommendation": self._generate_next_recommendation(arc),
            "narrative_summary": self._generate_narrative_summary(arc)
        }

        return visualization

    def _generate_hero_title(self, arc: GrowthArc) -> str:
        """generate英雄称号"""
        milestones_count = len(arc.milestones)
        transformation = arc.transformation_level

        if transformation >= 0.9:
            if milestones_count >= 4:
                return "✨ 觉醒大师"
            else:
                return "🌟 成熟英雄"
        elif transformation >= 0.7:
            return "⚡ 成长战士"
        elif transformation >= 0.5:
            return "🔥 入门修行者"
        elif transformation >= 0.3:
            return "🌙 觉醒探索者"
        else:
            return "🌱 初始冒险者"

    def _generate_progress_bar(self, level: float) -> str:
        """generate进度条"""
        bar_length = 20
        filled = int(level * bar_length)
        return "█" * filled + "░" * (bar_length - filled)

    def _generate_next_recommendation(self, arc: GrowthArc) -> Dict[str, str]:
        """generate下一步推荐"""
        recommendations = {
            GrowthPhase.DORMANT: {
                "action": "开始你的旅程",
                "suggestion": "是什么一直困扰着你?是什么促使你想要改变?"
            },
            GrowthPhase.AWAKENING: {
                "action": "明确你的目标",
                "suggestion": "写下你想要实现的具体目标."
            },
            GrowthPhase.CHALLENGING: {
                "action": "坚持面对",
                "suggestion": "不要放弃.每一次试炼都是成长的机会."
            },
            GrowthPhase.BREAKTHROUGH: {
                "action": "整合洞见",
                "suggestion": "你刚刚获得的洞见是什么?写下来."
            },
            GrowthPhase.INTEGRATING: {
                "action": "应用实践",
                "suggestion": "在真实生活中应用你学到的东西."
            },
            GrowthPhase.MASTERY: {
                "action": "分享智慧",
                "suggestion": "你愿意帮助其他正在旅程中的人吗?"
            }
        }

        return recommendations.get(arc.current_phase, recommendations[GrowthPhase.DORMANT])

    def _generate_narrative_summary(self, arc: GrowthArc) -> str:
        """generate叙事性总结"""
        milestone_titles = [m.title for m in arc.milestones[-3:]]

        summary = f"""
📖 **你的英雄故事**

在过去的{arc.total_interactions}次交互中,你已经走过了从{arc.phase_history[0]['phase'] if arc.phase_history else '起点'}到{arc.current_phase.value[0]}的旅程.

你已经完成了{len(arc.milestones)}个里程碑,
经历了{arc.breakthrough_count}次突破,
面对了{len(arc.shadows_confronted)}次内心的阴影.

{', '.join(milestone_titles) if milestone_titles else '你的旅程才刚刚开始.'}

你已经获得了{len(arc.wisdom_accumulated)}条智慧,
与{len(arc.mentors) + len(arc.allies)}位重要的同行者建立了联系.

**当前转化程度:{int(arc.transformation_level * 100)}%**

{'你已经接近精通境界,准备好开始新的旅程了吗?' if arc.transformation_level >= 0.7 else '继续前进,英雄.你的旅程还在继续.'}
"""
        return summary

    def get_transformation_report(self, user_id: str) -> Dict[str, Any]:
        """get转化报告"""
        if user_id not in self.user_arcs:
            return {"status": "no_arc"}

        arc = self.user_arcs[user_id]

        return {
            "user_id": user_id,
            "started_at": arc.started_at,
            "current_phase": arc.current_phase.value[0],
            "transformation_level": arc.transformation_level,
            "milestones": [
                {
                    "title": m.title,
                    "description": m.description,
                    "wisdom": m.wisdom_gained,
                    "impact": m.growth_impact
                } for m in arc.milestones
            ],
            "capability_growth": arc.capabilities,
            "wisdom_journey": arc.wisdom_accumulated,
            "relationship_network": {
                "mentors": [{"name": r.entity_name, "trust": r.trust_level} for r in arc.mentors],
                "allies": [{"name": r.entity_name, "trust": r.trust_level} for r in arc.allies]
            },
            "shadow_journey": [
                {
                    "name": s.shadow_name,
                    "status": s.integration_status,
                    "lesson": s.lesson_learned
                } for s in arc.shadows_confronted
            ],
            "lessons_learned": arc.lessons_learned,
            "next_steps": self._generate_next_recommendation(arc)
        }

def create_growth_tracker() -> UserGrowthTracker:
    """创建成长追踪system_instance"""
    return UserGrowthTracker()
