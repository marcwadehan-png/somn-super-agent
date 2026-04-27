# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze_crisis_response',
    'analyze_leader',
    'analyze_leader_type',
    'analyze_team_stage',
    'diagnose_team',
    'get_shuihu_engine',
    'get_team_diagnosis',
]

水浒团队协作引擎 - Shuihu Team Engine v1.0.0
=============================================

将<水浒传>的团队智慧转化为现代团队管理工具

核心功能:
- 团队组建与愿景塑造
- 危机管理与突破
- 义气与制度的平衡
- 团队悲剧的警示

作者:Somn AI
日期:2026-04-02
"""

from typing import Dict, List, Any, Optional
from enum import Enum

class ShuihuTeamEngine:
    """
    水浒团队协作引擎
    
    基于<水浒传>的经典团队案例和人物分析,
    为现代团队管理提供智慧借鉴.
    """
    
    def __init__(self):
        """init水浒团队引擎"""
        self.version = "v1.0.0"
        
        # 团队发展阶段模型
        self.team_stages = {
            "stage_1": {
                "name": "聚义期",
                "description": "团队组建,英雄聚义",
                "characteristics": [
                    "目标模糊,各怀心思",
                    "个人能力突出",
                    "缺乏unified愿景"
                ],
                "shuihu_example": "晁盖智取生辰纲后上梁山",
                "management_focus": "明确愿景,建立信任"
            },
            "stage_2": {
                "name": "排座次期",
                "description": "权力结构确立,角色分工",
                "characteristics": [
                    "权力结构明确",
                    "利益分配清晰",
                    "组织纪律形成"
                ],
                "shuihu_example": "梁山泊英雄排座次,108将归位",
                "management_focus": "合理分工,激励到位"
            },
            "stage_3": {
                "name": "忠义堂期",
                "description": "共同愿景形成,文化塑造",
                "characteristics": [
                    "共同价值观形成",
                    "团队凝聚力最强",
                    "战斗力巅峰"
                ],
                "shuihu_example": "宋江改'聚义厅'为'忠义堂'",
                "management_focus": "文化塑造,愿景强化"
            },
            "stage_4": {
                "name": "招安期",
                "description": "目标转变,团队分裂",
                "characteristics": [
                    "领导层目标偏离",
                    "核心成员反对",
                    "团队开始分化"
                ],
                "shuihu_example": "宋江力主招安,引发内部矛盾",
                "management_focus": "unified思想,弥合分歧"
            },
            "stage_5": {
                "name": "覆灭期",
                "description": "团队瓦解,悲剧结局",
                "characteristics": [
                    "核心成员离去",
                    "战斗力急剧下降",
                    "最终走向失败"
                ],
                "shuihu_example": "征方腊后,英雄凋零",
                "management_focus": "防止重蹈覆辙"
            }
        }
        
        # 关键人物分析
        self.key_characters = {
            "宋江": {
                "role": "领导者",
                "strengths": [
                    "仗义疏财,人缘极好",
                    "有领导魅力,能凝聚人心",
                    "善于协调各方关系"
                ],
                "weaknesses": [
                    "愚忠,缺乏战略眼光",
                    "decision失误,用人不当",
                    "过于追求正统认可"
                ],
                "tragic_flaw": "招安decision导致梁山悲剧",
                "lesson": "领导者的愿景决定团队命运"
            },
            "晁盖": {
                "role": "前任领袖",
                "strengths": [
                    "为人豪爽,真正的草莽英雄",
                    "重视义气,不慕荣利",
                    "领导style民主"
                ],
                "weaknesses": [
                    "早逝,未能建立接班机制",
                    "缺乏明确的政治主张"
                ],
                "lesson": "创业团队要解决接班人问题"
            },
            "吴用": {
                "role": "军师",
                "strengths": [
                    "足智多谋,战略眼光",
                    "善于分析形势",
                    "对团队忠诚"
                ],
                "weaknesses": [
                    "过度服从领导",
                    "缺乏独立立场"
                ],
                "lesson": "军师需要保持独立思考"
            },
            "林冲": {
                "role": "技术骨干",
                "strengths": [
                    "武艺高强,能力强",
                    "隐忍克制,有原则",
                    "忠贞不渝"
                ],
                "weaknesses": [
                    "过于忍让,缺乏主动出击",
                    "安分守己,不善于争取"
                ],
                "lesson": "技术骨干需要突破自我设限"
            },
            "鲁智深": {
                "role": "侠义之士",
                "strengths": [
                    "侠义心肠,路见不平",
                    "粗中有细,智慧非凡",
                    "真正的好汉"
                ],
                "weaknesses": [
                    "行事鲁莽",
                    "不拘小节"
                ],
                "lesson": "侠义精神需要智慧引导"
            },
            "武松": {
                "role": "战斗英雄",
                "strengths": [
                    "战斗力强,有勇有谋",
                    "快意恩仇",
                    "对朋友忠诚"
                ],
                "weaknesses": [
                    "过于刚烈,容易冲动",
                    "单打独斗倾向"
                ],
                "lesson": "战斗英雄需要学会团队协作"
            },
            "李逵": {
                "role": "狂热追随者",
                "strengths": [
                    "对领导绝对忠诚",
                    "战斗力强",
                    "直率可爱"
                ],
                "weaknesses": [
                    "盲目服从,缺乏judge",
                    "行事鲁莽,杀人无数",
                    "情绪化"
                ],
                "lesson": "盲目忠诚是危险的"
            }
        }
        
        # 团队悲剧案例
        self.tragic_cases = {
            "招安悲剧": {
                "case": "宋江接受招安",
                "root_cause": "领导者的价值观错误",
                "process": [
                    "宋江将'聚义厅'改为'忠义堂'",
                    "提出'替天行道'的妥协口号",
                    "部分好汉反对但被压制",
                    "最终接受招安"
                ],
                "consequence": "征辽,征方腊,英雄凋零",
                "lesson": "妥协换不来尊重,底线不可丢失"
            },
            "林冲之死": {
                "case": "林冲被迫上山的全过程",
                "root_cause": "高俅的迫害",
                "process": [
                    "林娘子被高衙内看中",
                    "林冲被陷害误入白虎堂",
                    "野猪林差点被害",
                    "风雪山神庙被逼反抗"
                ],
                "lesson": "再隐忍的人也有底线"
            },
            "李逵之死": {
                "case": "李逵被宋江毒酒赐死",
                "root_cause": "盲目的忠诚",
                "process": [
                    "李逵对宋江绝对服从",
                    "宋江怕李逵在自己死后造反",
                    "骗李逵喝下毒酒"
                ],
                "lesson": "没有独立人格的忠诚是悲剧"
            }
        }
        
        # 成功要素
        self.success_factors = {
            "聚义": {
                "description": "志同道合者相聚",
                "key_points": [
                    "共同的利益诉求",
                    "相近的价值观念",
                    "相互欣赏的能力"
                ]
            },
            "排位": {
                "description": "合理的权力结构",
                "key_points": [
                    "能力与位置匹配",
                    "激励机制到位",
                    "晋升通道清晰"
                ]
            },
            "忠义": {
                "description": "共同愿景与价值观",
                "key_points": [
                    "明确的使命",
                    "共享的价值观",
                    "强烈的归属感"
                ]
            }
        }
    
    def analyze_team_stage(self, team_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析团队当前阶段
        
        Args:
            team_info: 团队信息
            
        Returns:
            阶段分析报告
        """
        vision_clarity = team_info.get("vision_clarity", 5)
        structure_stability = team_info.get("structure_stability", 5)
        cohesion = team_info.get("cohesion", 5)
        goal_alignment = team_info.get("goal_alignment", 5)
        
        # 计算synthesize得分
        scores = {
            "vision_clarity": vision_clarity,
            "structure_stability": structure_stability,
            "cohesion": cohesion,
            "goal_alignment": goal_alignment
        }
        avg_score = sum(scores.values()) / len(scores)
        
        # 确定阶段
        if avg_score < 3:
            stage = "stage_1"  # 聚义期
        elif avg_score < 5:
            stage = "stage_2"  # 排座次期
        elif avg_score < 7:
            stage = "stage_3"  # 忠义堂期
        elif avg_score < 8:
            stage = "stage_4"  # 招安期
        else:
            stage = "stage_5"  # 覆灭期
        
        stage_info = self.team_stages[stage]
        
        # generate建议
        suggestions = self._generate_stage_suggestions(stage, scores)
        
        return {
            "current_stage": stage_info["name"],
            "stage_description": stage_info["description"],
            "shuihu_reference": stage_info["shuihu_example"],
            "management_focus": stage_info["management_focus"],
            "scores": scores,
            "suggestions": suggestions,
            "warnings": self._get_stage_warnings(stage)
        }
    
    def _generate_stage_suggestions(self, stage: str, scores: Dict[str, int]) -> List[str]:
        """generate阶段建议"""
        suggestions_map = {
            "stage_1": [
                "明确团队共同愿景",
                "建立基本信任机制",
                "recognize核心成员"
            ],
            "stage_2": [
                "完善权力结构",
                "明确角色分工",
                "建立激励机制"
            ],
            "stage_3": [
                "强化团队文化",
                "unified思想认识",
                "提升凝聚力"
            ],
            "stage_4": [
                "警惕目标漂移",
                "充分沟通愿景",
                "准备B方案"
            ],
            "stage_5": [
                "悬崖勒马",
                "重新审视战略",
                "可能需要重组"
            ]
        }
        
        suggestions = suggestions_map.get(stage, [])
        
        # 针对薄弱项的专项建议
        if scores.get("vision_clarity", 5) < 5:
            suggestions.append("立即明确团队愿景")
        if scores.get("cohesion", 5) < 5:
            suggestions.append("加强团队建设活动")
        
        return suggestions
    
    def _get_stage_warnings(self, stage: str) -> List[str]:
        """get阶段警示"""
        warnings_map = {
            "stage_1": [
                "警惕团队因目标不清而解散",
                "防止核心成员流失"
            ],
            "stage_2": [
                "警惕权力斗争",
                "防止利益分配不公"
            ],
            "stage_3": [
                "警惕领导者的decision失误",
                "防止外部诱惑动摇团队"
            ],
            "stage_4": [
                "警惕招安悲剧重演",
                "防止核心成员离去"
            ],
            "stage_5": [
                "立即止损",
                "重新审视团队方向"
            ]
        }
        return warnings_map.get(stage, [])
    
    def analyze_leader_type(self, leader_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析领导者类型
        
        Args:
            leader_info: 领导者信息
            
        Returns:
            领导者分析报告
        """
        loyalty_focus = leader_info.get("loyalty_focus", 5)
        mission_focus = leader_info.get("mission_focus", 5)
        people_focus = leader_info.get("people_focus", 5)
        results_focus = leader_info.get("results_focus", 5)
        
        # judge类型
        if loyalty_focus >= 8 and mission_focus < 5:
            leader_type = "宋江型"
            reference = self.key_characters["宋江"]
        elif mission_focus >= 8 and people_focus < 5:
            leader_type = "晁盖型"
            reference = self.key_characters["晁盖"]
        elif people_focus >= 8:
            leader_type = "仁义型"
            reference = {"strengths": ["得人心", "凝聚力强"], "weaknesses": ["原则性差"]}
        elif results_focus >= 8:
            leader_type = "铁腕型"
            reference = {"strengths": ["高效", "果断"], "weaknesses": ["冷酷"]}
        else:
            leader_type = "均衡型"
            reference = {"strengths": ["全面"], "weaknesses": ["特色不足"]}
        
        return {
            "leader_type": leader_type,
            "reference_character": reference,
            "strengths": reference["strengths"],
            "weaknesses": reference["weaknesses"],
            "risks": self._get_leader_risks(leader_type),
            "development_suggestions": self._get_leader_suggestions(leader_type)
        }
    
    def _get_leader_risks(self, leader_type: str) -> List[str]:
        """get领导者风险"""
        risks_map = {
            "宋江型": [
                "过度追求正统认可",
                "可能牺牲团队利益换取外部认可",
                "decision容易被外部势力左右"
            ],
            "晁盖型": [
                "缺乏政治敏感性",
                "难以应对复杂局面"
            ],
            "仁义型": [
                "原则性可能不够",
                "难以做出艰难decision"
            ],
            "铁腕型": [
                "可能失去人心",
                "团队氛围紧张"
            ]
        }
        return risks_map.get(leader_type, [])
    
    def _get_leader_suggestions(self, leader_type: str) -> List[str]:
        """get领导者建议"""
        suggestions_map = {
            "宋江型": [
                "坚守团队愿景,不轻易妥协",
                "建立独立的价值观体系",
                "学会说'不'"
            ],
            "晁盖型": [
                "加强政治素养",
                "培养战略眼光"
            ],
            "仁义型": [
                "在人情与原则间找到平衡",
                "学会处理棘手问题"
            ],
            "铁腕型": [
                "加强情商培养",
                "关注团队成员感受"
            ]
        }
        return suggestions_map.get(leader_type, [])
    
    def analyze_crisis_response(self, crisis_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析危机应对strategy
        
        Args:
            crisis_info: 危机信息
            
        Returns:
            危机应对分析
        """
        crisis_type = crisis_info.get("type", "pressure")
        team_strength = crisis_info.get("team_strength", "medium")
        
        # 林冲案例分析
        if crisis_type == "injustice":
            case = self.tragic_cases["林冲之死"]
            lessons = [
                "面对不公,需要有底线",
                "隐忍是有限度的",
                "要善于寻求帮助"
            ]
            recommendations = [
                "评估形势,明确底线",
                "寻找盟友,建立支持",
                "必要时果断反击"
            ]
        elif crisis_type == "pressure":
            case = self.tragic_cases["招安悲剧"]
            lessons = [
                "压力下的妥协可能导致灾难",
                "团队需要有共同信念"
            ]
            recommendations = [
                "明确团队底线",
                "保持战略定力",
                "做好最坏打算"
            ]
        else:
            case = {"description": "需要synthesize分析"}
            lessons = ["具体情况具体分析"]
            recommendations = ["保持冷静,寻求突破"]
        
        return {
            "crisis_type": crisis_type,
            "case_reference": case,
            "lessons": lessons,
            "recommendations": recommendations,
            "role_model": "鲁智深 - 侠义心肠,善于在危机中伸出援手"
        }
    
    def evaluate_team_义气(self, team_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        评估团队的义气水平
        
        Args:
            team_info: 团队信息
            
        Returns:
            义气评估报告
        """
        mutual_support = team_info.get("mutual_support", 5)
        loyalty = team_info.get("loyalty", 5)
        fairness = team_info.get("fairness", 5)
        independence = team_info.get("independence", 5)
        
        # 计算义气得分
        义气_score = (mutual_support + loyalty + fairness) / 3
        
        # 平衡性分析
        balance_score = 10 - abs(mutual_support - loyalty) - abs(loyalty - fairness)
        
        # 给出评价
        if 义气_score >= 8 and balance_score >= 7:
            evaluation = "健康的义气"
            description = "团队义气充足,且保持理性平衡"
        elif 义气_score >= 6:
            evaluation = "一般的义气"
            description = "有一定义气基础,但需要加强"
        else:
            evaluation = "缺乏义气"
            description = "团队凝聚力不足,需要改善"
        
        # 风险警示
        warnings = []
        if independence < 4:
            warnings.append("警惕李逵式盲从--团队成员缺乏独立思考")
        if fairness < 5:
            warnings.append("警惕宋江式偏心--利益分配不公导致不满")
        if loyalty > 9:
            warnings.append("警惕过度忠诚--可能导致团队失去judge力")
        
        return {
            "义气_score": round(义气_score, 2),
            "balance_score": round(balance_score, 2),
            "evaluation": evaluation,
            "description": description,
            "warnings": warnings,
            "suggestions": self._get_义气_suggestions(义气_score, balance_score)
        }
    
    def _get_义气_suggestions(self, 义气_score: float, balance_score: float) -> List[str]:
        """get义气改进建议"""
        suggestions = []
        
        if 义气_score < 6:
            suggestions.append("加强团队建设,提升凝聚力")
        if balance_score < 7:
            suggestions.append("平衡义气与原则,避免盲目忠诚")
        if 义气_score >= 8:
            suggestions.append("保持这种健康的义气文化")
        
        suggestions.append("建立团队公约,明确共同价值观")
        
        return suggestions
    
    def get_team_diagnosis(self, team_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        synthesize团队诊断
        
        Args:
            team_info: 团队信息
            
        Returns:
            synthesize诊断报告
        """
        stage_analysis = self.analyze_team_stage(team_info)
        义气_analysis = self.evaluate_team_义气(team_info)
        
        return {
            "stage_analysis": stage_analysis,
            "义气_analysis": 义气_analysis,
            "key_issues": self._identify_key_issues(team_info),
            "priority_actions": self._suggest_priority_actions(team_info),
            "shuihu_quote": self._get_shuihu_quote()
        }
    
    def _identify_key_issues(self, team_info: Dict[str, Any]) -> List[str]:
        """recognize关键问题"""
        issues = []
        
        if team_info.get("vision_clarity", 5) < 5:
            issues.append("团队愿景不清晰")
        if team_info.get("cohesion", 5) < 5:
            issues.append("团队凝聚力不足")
        if team_info.get("goal_alignment", 5) < 5:
            issues.append("目标不一致")
        
        return issues if issues else ["团队状态良好"]
    
    def _suggest_priority_actions(self, team_info: Dict[str, Any]) -> List[str]:
        """建议优先action"""
        actions = []
        
        lowest_score = min(
            team_info.get("vision_clarity", 5),
            team_info.get("structure_stability", 5),
            team_info.get("cohesion", 5),
            team_info.get("goal_alignment", 5)
        )
        
        if lowest_score == team_info.get("vision_clarity", 5):
            actions.append("立即召开愿景共识会议")
        elif lowest_score == team_info.get("cohesion", 5):
            actions.append("组织团队建设活动")
        elif lowest_score == team_info.get("goal_alignment", 5):
            actions.append("重新对齐团队目标")
        
        return actions if actions else ["继续保持,当前状态良好"]
    
    def _get_shuihu_quote(self) -> Dict[str, str]:
        """get水浒语录"""
        quotes = [
            {
                "text": "逼上梁山,官逼民反.",
                "context": "<水浒传>核心主题"
            },
            {
                "text": "他时若遂凌云志,敢笑黄巢不丈夫!",
                "context": "宋江题反诗"
            },
            {
                "text": "赤日炎炎似火烧,野田禾稻半枯焦.农夫心内如汤煮,公子王孙把扇摇.",
                "context": "底层人民的苦难"
            },
            {
                "text": "路见不平,拔刀相助.",
                "context": "侠义精神的体现"
            }
        ]
        import random
        return random.choice(quotes)

# ==================== 便捷函数 ====================

def get_shuihu_engine() -> ShuihuTeamEngine:
    """get水浒团队引擎"""
    return ShuihuTeamEngine()

def diagnose_team(team_info: Dict[str, Any]) -> Dict[str, Any]:
    """诊断团队状态"""
    engine = ShuihuTeamEngine()
    return engine.get_team_diagnosis(team_info)

def analyze_leader(leader_info: Dict[str, Any]) -> Dict[str, Any]:
    """分析领导者类型"""
    engine = ShuihuTeamEngine()
    return engine.analyze_leader_type(leader_info)

# ==================== 测试代码 ====================

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
