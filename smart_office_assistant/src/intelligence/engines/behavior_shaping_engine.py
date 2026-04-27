"""
__all__ = [
    'apply_minimalism',
    'assess_willpower',
    'create_energy_management_plan',
    'design_habit_system',
    'design_nudge_system',
    'implant_rich_habits',
    'quick_habit_design',
]

行为塑造引擎 v1.0
fusion自控力,极简主义,富有的习惯,超级记忆力等5篇自我管理类文档

核心能力:
1. 习惯系统设计 - 基于习惯回路(暗示→惯常行为→奖赏)
2. 自控力增强 - 基于自控力的生理/心理机制
3. 极简思维 - 剔除多余,聚焦本质
4. 富有习惯植入 - 富人思维模式的行为化
5. 精力管理 - 精力而非时间管理
6. 行为改变strategy - 基于行为经济学的助推设计

版本:v1.0.0
更新:2026-04-02
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, time

class HabitType(Enum):
    """习惯类型"""
    CORE = "核心习惯"           # 能引发连锁反应的习惯
    KEYSTONE = "基石习惯"       # 影响多个领域
    SUPPORTING = "支撑习惯"     # 支撑核心习惯
    ELIMINATION = "消除习惯"    # 需要消除的坏习惯

class ChangePhase(Enum):
    """改变阶段"""
    PRECONTEMPLATION = "前思考期"    # 未意识到需要改变
    CONTEMPLATION = "思考期"         # 意识到但未action
    PREPARATION = "准备期"           # 准备开始
    ACTION = "action期"               # 正在改变
    MAINTENANCE = "维持期"           # 维持新行为

@dataclass
class HabitLoop:
    """习惯回路"""
    cue: str           # 暗示/触发器
    routine: str       # 惯常行为
    reward: str        # 奖赏
    craving: str       # 渴望(驱动回路的内在动力)

@dataclass
class BehaviorProfile:
    """行为画像"""
    current_habits: List[str]
    change_readiness: ChangePhase
    willpower_level: float          # 自控力水平 (0-1)
    energy_pattern: str             # 精力模式
    clutter_areas: List[str]        # 需要简化的领域

class BehaviorShapingEngine:
    """
    行为塑造引擎
    
    fusion五大自我管理传统:
    - 自控力(凯利·麦格尼格尔):意志力的生理机制和训练方法
    - 极简主义(近藤麻理惠/乔布斯):减法思维,聚焦本质
    - 富有的习惯(托马斯·科里):富人思维的行为化
    - 大脑整理术:认知负荷管理和信息处理优化
    - 行为经济学(丹尼尔·卡尼曼/理查德·泰勒):助推和选择架构
    
    核心理念:不要对抗人性,而是设计让好行为更容易,坏行为更困难的环境
    """

    VERSION = "v1.0.0"
    
    def __init__(self):
        # === 富有的习惯核心清单 ===
        self.rich_habits = {
            "日常习惯": [
                {"habit": "每天早起", "impact": "掌控时间", "difficulty": "中"},
                {"habit": "每日阅读30分钟", "impact": "知识积累", "difficulty": "低"},
                {"habit": "每天运动30分钟", "impact": "精力充沛", "difficulty": "中"},
                {"habit": "维护人际关系", "impact": "社会资本", "difficulty": "低"},
                {"habit": "设定当日目标", "impact": "效率提升", "difficulty": "低"}
            ],
            "思维习惯": [
                {"habit": "积极思考", "impact": "心态优化", "difficulty": "高"},
                {"habit": "延迟满足", "impact": "长期收益", "difficulty": "高"},
                {"habit": "终身学习", "impact": "持续成长", "difficulty": "中"},
                {"habit": "感恩心态", "impact": "幸福感", "difficulty": "低"},
                {"habit": "风险管理意识", "impact": "避免重大损失", "difficulty": "中"}
            ],
            "财务习惯": [
                {"habit": "定期储蓄", "impact": "财富积累", "difficulty": "中"},
                {"habit": "控制支出", "impact": "财务健康", "difficulty": "中"},
                {"habit": "学习投资", "impact": "被动收入", "difficulty": "中"},
                {"habit": "记录财务", "impact": "财务意识", "difficulty": "低"},
                {"habit": "制定预算", "impact": "资金规划", "difficulty": "低"}
            ]
        }
        
        # === 自控力核心机制 ===
        self.willpower_mechanisms = {
            "生理基础": {
                "resource": "葡萄糖(前额叶皮层的燃料)",
                "depletion": "自控力是有限资源,持续使用会耗竭",
                "recovery": "睡眠,冥想,运动可以恢复自控力"
            },
            "心理机制": {
                "hot_cold_system": "热系统(冲动)vs 冷系统(理性)",
                "delay_discounting": "人们倾向于选择即时小奖赏而非延迟大奖赏",
                "ego_depletion": "自我损耗:前额叶皮层的疲劳效应"
            },
            "训练方法": {
                "meditation": "每天10分钟正念冥想,增强前额叶皮层",
                "exercise": "有氧运动提高自控力的生理基础",
                "sleep": "7-8小时睡眠是自控力的基础保障",
                "small_wins": "通过小成功积累自我效能感",
                "if_then_plans": "如果...就...计划,预设行为decision"
            }
        }
        
        # === 极简主义原则 ===
        self.minimalism_principles = {
            "二八法则": "20%的事物产生80%的价值,聚焦核心",
            "奥卡姆剃刀": "如无必要,勿增实体",
            "少即是多": "减少选择,提高decision质量",
            "一进一出": "每增加一件物品,就要淘汰一件",
            "问三个问题": ["需要吗?", "有用吗?", "快乐吗?"]
        }
        
        # === 行为改变阶段模型(跨理论模型)===
        self.stages_of_change = {
            ChangePhase.PRECONTEMPLATION: {
                "desc": "没有意识到需要改变",
                "strategy": "提高意识,揭示行为后果",
                "key_question": "我为什么需要改变?"
            },
            ChangePhase.CONTEMPLATION: {
                "desc": "知道需要改变但还在犹豫",
                "strategy": "权衡利弊,强化改变动机",
                "key_question": "改变的收益大于成本吗?"
            },
            ChangePhase.PREPARATION: {
                "desc": "准备开始改变",
                "strategy": "制定具体计划,设置触发条件",
                "key_question": "我具体要做什么?什么时候?"
            },
            ChangePhase.ACTION: {
                "desc": "正在执行改变",
                "strategy": "环境设计,社交支持,即时反馈",
                "key_question": "如何让好行为更容易?"
            },
            ChangePhase.MAINTENANCE: {
                "desc": "维持新行为,防止倒退",
                "strategy": "习惯化,身份认同转变,应急预案",
                "key_question": "如何防止旧习复发?"
            }
        }

    def design_habit_system(self, goals: List[str], current_profile: BehaviorProfile = None) -> Dict:
        """
        设计习惯系统
        
        Args:
            goals: 目标列表
            current_profile: 当前行为画像
            
        Returns:
            习惯系统设计方案
        """
        system = {
            "goals": goals,
            "phase": current_profile.change_readiness.value if current_profile else "action期",
            "keystone_habits": self._select_keystone_habits(goals),
            "daily_routine": self._design_daily_routine(goals),
            "habit_loops": self._design_habit_loops(goals),
            "environment_design": self._design_environment(goals),
            "tracking_system": self._design_tracking(goals),
            "change_strategy": self._generate_change_strategy(
                current_profile.change_readiness if current_profile else ChangePhase.ACTION
            )
        }
        
        return system

    def assess_willpower(self, context: str) -> Dict:
        """
        评估自控力状态
        
        Args:
            context: 当前情境描述
            
        Returns:
            自控力评估和建议
        """
        depleting_factors = self._identify_depleting_factors(context)
        recovery_actions = self._suggest_recovery_actions(depleting_factors)
        
        return {
            "context": context,
            "depleting_factors": depleting_factors,
            "current_assessment": "高消耗" if len(depleting_factors) >= 3 else "中等消耗" if len(depleting_factors) >= 1 else "状态良好",
            "recovery_actions": recovery_actions,
            "if_then_plan": self._generate_if_then_plan(context),
            "hot_cold_analysis": self._analyze_hot_cold_system(context)
        }

    def apply_minimalism(self, area: str, items: List[str]) -> Dict:
        """
        应用极简主义原则
        
        Args:
            area: 需要简化的领域
            items: 当前项目/任务/物品列表
            
        Returns:
            极简主义优化方案
        """
        # 用二八法则筛选
        essential = self._pareto_filter(items, 0.2)
        optional = [item for item in items if item not in essential]
        
        # 用三个问题过滤
        filtered = self._triple_question_filter(optional)
        
        return {
            "area": area,
            "original_count": len(items),
            "essential_items": essential,
            "optional_items": optional,
            "recommended_elimination": filtered,
            "optimized_count": len(essential) + len(optional) - len(filtered),
            "reduction_ratio": f"{len(filtered)/max(len(items),1)*100:.0f}%",
            "minimalism_principles_applied": self.minimalism_principles
        }

    def implant_rich_habits(self, current_habits: List[str], target_area: str = "all") -> Dict:
        """
        植入富人习惯
        
        Args:
            current_habits: 当前习惯列表
            target_area: 目标领域
            
        Returns:
            富有习惯植入方案
        """
        gaps = self._identify_habit_gaps(current_habits)
        recommendations = []
        
        if target_area == "all":
            areas = self.rich_habits
        else:
            areas = {target_area: self.rich_habits.get(target_area, [])}
        
        for area, habits in areas.items():
            area_gaps = [h["habit"] for h in habits if h["habit"] not in current_habits]
            if area_gaps:
                # 按难度排序,先推荐容易的
                easy_first = sorted(
                    [h for h in habits if h["habit"] in area_gaps],
                    key=lambda x: {"低": 0, "中": 1, "高": 2}.get(x["difficulty"], 1)
                )
                recommendations.append({
                    "area": area,
                    "missing_habits": area_gaps,
                    "recommended_start": easy_first[0] if easy_first else None,
                    "priority_order": easy_first[:3]
                })
        
        return {
            "current_habits": current_habits,
            "gaps_identified": gaps,
            "recommendations": recommendations,
            "daily_compound_effect": self._calculate_compound_effect(recommendations),
            "implementation_timeline": self._create_implementation_timeline(recommendations)
        }

    def design_nudge_system(self, target_behavior: str, barriers: List[str]) -> Dict:
        """
        设计助推系统(行为经济学应用)
        
        Args:
            target_behavior: 目标行为
            barriers: 行为障碍
            
        Returns:
            助推系统设计
        """
        return {
            "target_behavior": target_behavior,
            "barriers": barriers,
            "nudges": {
                "default_effect": self._design_default_nudge(target_behavior),
                "framing_effect": self._design_framing_nudge(target_behavior),
                "social_proof": self._design_social_proof_nudge(target_behavior),
                "commitment_device": self._design_commitment_nudge(target_behavior),
                "loss_aversion": self._design_loss_aversion_nudge(target_behavior),
                "choice_architecture": self._design_choice_architecture(target_behavior, barriers)
            },
            "implementation_priority": self._prioritize_nudges(barriers)
        }

    def create_energy_management_plan(self, energy_pattern: str = None) -> Dict:
        """
        创建精力管理计划
        
        Args:
            energy_pattern: 精力模式(早型/晚型/弹性型)
            
        Returns:
            精力管理计划
        """
        if not energy_pattern:
            energy_pattern = "弹性型"
        
        return {
            "energy_pattern": energy_pattern,
            "four_dimensions": {
                "体能精力": self._manage_physical_energy(energy_pattern),
                "情感精力": self._manage_emotional_energy(),
                "思维精力": self._manage_mental_energy(energy_pattern),
                "意志精力": self._manage_purpose_energy()
            },
            "daily_rhythm": self._design_energy_rhythm(energy_pattern),
            "recovery_protocol": self._design_recovery_protocol(),
            "energy_blockers": ["睡眠不足", "多任务切换", "负面情绪", "缺乏运动", "信息过载"]
        }

    # === 内部方法 ===
    
    def _select_keystone_habits(self, goals: List[str]) -> List[Dict]:
        """选择基石习惯"""
        keystone_map = {
            "健康": [{"habit": "每天运动30分钟", "spillover": ["精力提升", "情绪改善", "睡眠质量"]}],
            "效率": [{"habit": "早起+规划当日", "spillover": ["时间掌控", "目标聚焦", "减少拖延"]}],
            "学习": [{"habit": "每日阅读30分钟", "spillover": ["知识积累", "思维拓展", "写作提升"]}],
            "财富": [{"habit": "记录每日支出", "spillover": ["财务意识", "消费控制", "储蓄增加"]}],
            "社交": [{"habit": "每天主动联系一个人", "spillover": ["关系维护", "机会发现", "信息get"]}]
        }
        
        habits = []
        for goal in goals:
            for keyword, habit_info in keystone_map.items():
                if keyword in goal:
                    habits.extend(habit_info)
        return habits or [{"habit": "建立晨间仪式", "spillover": ["时间管理", "精力管理", "心理准备"]}]
    
    def _design_daily_routine(self, goals: List[str]) -> Dict:
        """设计每日常规"""
        return {
            "morning_ritual": {
                "time": "6:00-7:00",
                "activities": ["起床后立即喝一杯水", "10分钟冥想/思考", "30分钟运动", "健康早餐"],
                "purpose": "激活身体和精神,奠定一天基调"
            },
            "work_blocks": {
                "time": "9:00-12:00, 14:00-17:00",
                "strategy": "番茄工作法(25分钟专注+5分钟休息),处理最重要的3件事",
                "purpose": "在精力最高时段处理高价值任务"
            },
            "evening_routine": {
                "time": "20:00-22:00",
                "activities": ["回顾当日成果", "准备次日计划", "阅读30分钟", "22:00前睡觉"],
                "purpose": "巩固学习成果,确保充足睡眠"
            }
        }
    
    def _design_habit_loops(self, goals: List[str]) -> List[Dict]:
        """设计习惯回路"""
        loops = []
        loop_templates = {
            "运动": HabitLoop(cue="起床后/下班后", routine="运动30分钟", reward="内啡肽分泌+成就感", craving="活力充沛的感觉"),
            "阅读": HabitLoop(cue="固定时间+固定地点", routine="阅读30分钟", reward="知识get+心流体验", craving="求知欲"),
            "写作": HabitLoop(cue="完成一项重要工作后", routine="写15分钟总结", reward="思路清晰+输出成果", craving="表达的渴望"),
            "储蓄": HabitLoop(cue="发薪日", routine="自动转存20%", reward="账户增长的安全感", craving="财务安全感")
        }
        
        for goal in goals:
            for keyword, loop in loop_templates.items():
                if keyword in goal:
                    loops.append({
                        "goal": goal,
                        "cue": loop.cue,
                        "routine": loop.routine,
                        "reward": loop.reward,
                        "craving": loop.craving
                    })
        
        return loops or [{"note": "根据具体目标定制习惯回路:暗示→惯常行为→奖赏→渴望"}]
    
    def _design_environment(self, goals: List[str]) -> Dict:
        """设计行为环境"""
        return {
            "principle": "让好行为更容易,让坏行为更困难",
            "strategies": {
                "增加摩擦力(坏习惯)": ["把手机放到另一个房间", "取消不必要的订阅", "清理桌面零食"],
                "减少摩擦力(好习惯)": ["提前准备好运动衣物", "把书放在床头", "准备健康食材"],
                "视觉提示": ["使用习惯追踪应用", "在显眼处放置提醒", "创建视觉化进度墙"]
            }
        }
    
    def _design_tracking(self, goals: List[str]) -> Dict:
        """设计追踪系统"""
        return {
            "method": "不要断链(Don't break the chain)",
            "frequency": "每日标记完成状态",
            "review_cycle": "每周回顾+每月总结",
            "reward_milestones": ["连续7天 → 小奖励", "连续30天 → 中奖励", "连续100天 → 大奖励"]
        }
    
    def _generate_change_strategy(self, phase: ChangePhase) -> Dict:
        """generate改变strategy"""
        return self.stages_of_change.get(phase, {})
    
    def _identify_depleting_factors(self, context: str) -> List[str]:
        """recognize自控力消耗因素"""
        factors = []
        depleting_keywords = {
            "decision疲劳": ["选择", "决定", "权衡", "考虑"],
            "情绪消耗": ["压力", "冲突", "焦虑", "担忧"],
            "信息过载": ["大量", "很多", "同时处理"],
            "身体疲劳": ["累", "困", "疲惫", "没睡好"]
        }
        for factor, keywords in depleting_keywords.items():
            if any(kw in context for kw in keywords):
                factors.append(factor)
        return factors
    
    def _suggest_recovery_actions(self, factors: List[str]) -> List[str]:
        """建议恢复action"""
        actions = []
        if any(f in str(factors) for f in ["decision", "信息"]):
            actions.append("暂时减少选择,预设decision")
        if "情绪" in str(factors):
            actions.append("5分钟深呼吸或短暂散步")
        if "身体" in str(factors):
            actions.append("20分钟小睡或闭目休息")
        actions.extend(["喝一杯水", "做几个拉伸动作", "看远处放松眼睛"])
        return actions
    
    def _generate_if_then_plan(self, context: str) -> Dict:
        """generate如果...就...计划"""
        return {
            "principle": "预设行为decision,减少实时自控力消耗",
            "examples": [
                "如果我想吃零食 → 就先喝一杯水等10分钟",
                "如果我想刷手机 → 就把手机放到另一个房间",
                "如果我觉得拖延 → 就先做5分钟再说"
            ]
        }
    
    def _analyze_hot_cold_system(self, context: str) -> Dict:
        """分析热系统vs冷系统"""
        return {
            "hot_system": "负责冲动,欲望,即时满足(杏仁核驱动)",
            "cold_system": "负责理性,计划,延迟满足(前额叶皮层驱动)",
            "strategy": "当热系统被激活时,使用物理距离(如离开诱惑源)或时间延迟(等10分钟)来给冷系统反应时间"
        }
    
    def _pareto_filter(self, items: List[str], ratio: float = 0.2) -> List[str]:
        """二八法则筛选"""
        count = max(int(len(items) * ratio), 1)
        return items[:count]  # 简化处理,实际应基于价值评估
    
    def _triple_question_filter(self, items: List[str]) -> List[str]:
        """三个问题过滤"""
        return [item for item in items if hash(item) % 3 == 0]  # 简化处理
    
    def _identify_habit_gaps(self, current_habits: List[str]) -> List[str]:
        """recognize习惯缺口"""
        all_rich_habits = []
        for area_habits in self.rich_habits.values():
            for h in area_habits:
                all_rich_habits.append(h["habit"])
        
        return [h for h in all_rich_habits if h not in current_habits]
    
    def _calculate_compound_effect(self, recommendations: List[Dict]) -> str:
        """计算复合效应"""
        return "每天1%的进步 → 一年后进步37倍(1.01^365 ≈ 37.78)"
    
    def _create_implementation_timeline(self, recommendations: List[Dict]) -> Dict:
        """创建实施时间线"""
        return {
            "第1周": "选择1个最容易的习惯开始",
            "第2-4周": "巩固第一个习惯,开始第二个",
            "第2个月": "增加到3-4个新习惯",
            "第3个月": "形成稳定习惯系统"
        }
    
    def _design_default_nudge(self, behavior: str) -> Dict:
        """设计默认效应助推"""
        return {"principle": "将目标行为设为默认选项", "example": f"默认{behavior},需要主动选择退出"}
    
    def _design_framing_nudge(self, behavior: str) -> Dict:
        """设计框架效应助推"""
        return {"principle": "正向框架描述目标行为", "example": f"不说'减少浪费',而说'节省80%'"}
    
    def _design_social_proof_nudge(self, behavior: str) -> Dict:
        """设计社会证明助推"""
        return {"principle": "展示他人已经采取了目标行为", "example": f"90%的成功人士都有{behavior}的习惯"}
    
    def _design_commitment_nudge(self, behavior: str) -> Dict:
        """设计承诺装置助推"""
        return {"principle": "预先承诺,增加未来action的确定性", "example": f"公开承诺{behavior},引入社交监督"}
    
    def _design_loss_aversion_nudge(self, behavior: str) -> Dict:
        """设计损失厌恶助推"""
        return {"principle": "强调不action的损失而非action的收益", "example": f"不{behavior}每年损失X元/小时"}
    
    def _design_choice_architecture(self, behavior: str, barriers: List[str]) -> Dict:
        """设计选择架构"""
        return {"principle": "重新设计选择环境,使目标行为成为最容易的选择"}
    
    def _prioritize_nudges(self, barriers: List[str]) -> List[str]:
        """确定助推优先级"""
        return ["default_effect", "choice_architecture", "framing_effect", "commitment_device"]
    
    def _manage_physical_energy(self, pattern: str) -> Dict:
        """管理体能精力"""
        return {
            "sleep": "7-8小时,固定时间起床",
            "exercise": "每天30分钟有氧+2次力量训练",
            "nutrition": "规律饮食,减少高糖高油",
            "hydration": "每天2升水"
        }
    
    def _manage_emotional_energy(self) -> Dict:
        """管理情感精力"""
        return {
            "positive_connections": "每天与积极的人互动",
            "gratitude_practice": "睡前写3件感恩的事",
            "boundary_setting": "学会说'不',保护情感能量",
            "recreation": "定期做让自己开心的事"
        }
    
    def _manage_mental_energy(self, pattern: str) -> Dict:
        """管理思维精力"""
        return {
            "focus_blocks": "90分钟深度专注块,之后休息",
            "single_tasking": "一次只做一件事",
            "learning_time": "每天30分钟学习新知识",
            "reflection": "每天10分钟回顾和思考"
        }
    
    def _manage_purpose_energy(self) -> Dict:
        """管理意志精力"""
        return {
            "purpose_clarity": "明确人生的核心目标和价值观",
            "meaningful_work": "将日常任务与更大的意义连接",
            "values_alignment": "确保行为与价值观一致",
            "growth_mindset": "将挑战视为成长机会"
        }
    
    def _design_energy_rhythm(self, pattern: str) -> Dict:
        """设计精力节奏"""
        rhythms = {
            "早型": {"peak": "8:00-11:00", "trough": "14:00-16:00", "recovery": "22:00-6:00"},
            "晚型": {"peak": "15:00-20:00", "trough": "8:00-11:00", "recovery": "1:00-9:00"},
            "弹性型": {"peak": "9:00-12:00", "trough": "14:00-15:00", "recovery": "23:00-7:00"}
        }
        return rhythms.get(pattern, rhythms["弹性型"])
    
    def _design_recovery_protocol(self) -> Dict:
        """设计恢复协议"""
        return {
            "micro_recovery": "每90分钟休息5-10分钟",
            "daily_recovery": "确保7-8小时睡眠",
            "weekly_recovery": "一天完全休息日",
            "quarterly_recovery": "一次3-5天的深度休息"
        }

# 便捷函数
def quick_habit_design(goals: List[str]) -> Dict:
    """便捷函数:快速设计习惯系统"""
    engine = BehaviorShapingEngine()
    return engine.design_habit_system(goals)
