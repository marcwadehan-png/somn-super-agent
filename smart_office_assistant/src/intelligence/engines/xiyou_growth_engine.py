# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze_commitment_level',
    'analyze_growth',
    'analyze_growth_path',
    'analyze_team_roles',
    'analyze_trial_type',
    'get_growth_diagnosis',
    'get_xiyou_engine',
    'recommend_team_training',
]

西游成长修炼引擎 - Xiyou Growth Engine v1.0.0
=============================================

将<西游记>的成长智慧转化为个人和组织修炼工具

核心功能:
- 取经团队角色分析
- 八十一难成长阶段
- 信念与坚持的修炼
- 团队协作的智慧

作者:Somn AI
日期:2026-04-02
"""

from typing import Dict, List, Any, Optional

class XiyouGrowthEngine:
    """
    西游成长修炼引擎
    
    基于<西游记>的取经故事,
    为个人成长和团队修炼提供智慧指引.
    """
    
    def __init__(self):
        """init西游成长引擎"""
        self.version = "v1.0.0"
        
        # 取经团队角色分析
        self.pilgrim_team = {
            "唐僧": {
                "role": "愿景领袖",
                "type": "VisionaryLeader",
                "strengths": [
                    "目标坚定,意志顽强",
                    "慈悲为怀,以德服人",
                    "不忘初心,方得始终"
                ],
                "weaknesses": [
                    "人妖不分,是非不明",
                    "缺乏战斗力",
                    "过于迂腐"
                ],
                "symbolism": "信念与使命",
                "growth_lesson": "领导者需要愿景感召,不需要事必躬亲"
            },
            "孙悟空": {
                "role": "核心执行",
                "type": "CoreExecutor",
                "strengths": [
                    "神通广大,能力超强",
                    "机智勇敢,敢于战斗",
                    "忠诚护主,最终修成正果"
                ],
                "weaknesses": [
                    "桀骜不驯,好名好胜",
                    "难以管束",
                    "性格急躁"
                ],
                "symbolism": "能力与成长",
                "growth_lesson": "天才需要舞台,也需要约束"
            },
            "猪八戒": {
                "role": "氛围调节",
                "type": "TeamRegulator",
                "strengths": [
                    "乐观开朗,调节气氛",
                    "人缘极好,善于交际",
                    "懂得生活,不那么严肃"
                ],
                "weaknesses": [
                    "好吃懒做",
                    "贪财好色",
                    "意志薄弱,容易动摇"
                ],
                "symbolism": "人性欲望",
                "growth_lesson": "团队需要调节者,但要控制负面影响"
            },
            "沙僧": {
                "role": "稳定执行",
                "type": "StableBackbone",
                "strengths": [
                    "忠厚老实,任劳任怨",
                    "稳定可靠,默默奉献",
                    "执行力强,不抱怨"
                ],
                "weaknesses": [
                    "缺乏主见",
                    "能力平庸",
                    "少言寡语"
                ],
                "symbolism": "踏实与坚持",
                "growth_lesson": "默默奉献的人往往被忽视,但不可或缺"
            }
        }
        
        # 成长阶段模型
        self.growth_stages = {
            "stage_1": {
                "name": "大闹天宫",
                "description": "个人英雄主义阶段",
                "characteristics": [
                    "自视甚高,以为我天下第一",
                    "挑战权威,不服管教",
                    "追求自由,藐视规则"
                ],
                "xiyou_example": "孙悟空自封齐天大圣,大闹天宫",
                "lesson": "个人能力再强,也需要组织和纪律"
            },
            "stage_2": {
                "name": "五行山下",
                "description": "挫折与反思阶段",
                "characteristics": [
                    "遭遇重大挫折",
                    "被压五百年",
                    "从狂妄到收敛"
                ],
                "xiyou_example": "孙悟空被如来压在五行山下",
                "lesson": "挫折是最好的老师"
            },
            "stage_3": {
                "name": "取经之路",
                "description": "团队协作阶段",
                "characteristics": [
                    "加入唐僧团队",
                    "戴上紧箍咒",
                    "学习协作与服从"
                ],
                "xiyou_example": "孙悟空保护唐僧西天取经",
                "lesson": "真正的成长在于学会与他人协作"
            },
            "stage_4": {
                "name": "功德圆满",
                "description": "自我实现阶段",
                "characteristics": [
                    "取经成功",
                    "成为斗战胜佛",
                    "实现自我价值"
                ],
                "xiyou_example": "孙悟空被封为斗战胜佛",
                "lesson": "在帮助他人中成就自己"
            }
        }
        
        # 八十一难分类
        self.trials = {
            "external": {
                "name": "外敌挑战",
                "examples": ["白骨精", "牛魔王", "红孩儿", "金角银角"],
                "characteristics": [
                    "有明确的敌人",
                    "需要战斗能力",
                    "考验勇气"
                ],
                "lesson": "外部竞争是最直接的挑战"
            },
            "internal": {
                "name": "心魔考验",
                "examples": ["六耳猕猴", "蜘蛛精"],
                "characteristics": [
                    "内心挣扎",
                    "自我对抗",
                    "真假难辨"
                ],
                "lesson": "最大的敌人往往是自己"
            },
            "temptation": {
                "name": "诱惑测试",
                "examples": ["女儿国", "嫦娥玉兔", "老鼠精"],
                "characteristics": [
                    "美好事物的诱惑",
                    "情色的考验",
                    "权力的考验"
                ],
                "lesson": "抵制诱惑比战胜敌人更难"
            },
            "dilemma": {
                "name": "困境考验",
                "examples": ["火焰山", "流沙河", "通天河"],
                "characteristics": [
                    "客观障碍",
                    "资源限制",
                    "需要智慧和耐心"
                ],
                "lesson": "环境困难需要特殊解决方案"
            },
            "relationship": {
                "name": "关系考验",
                "examples": ["三打白骨精被唐僧误解"],
                "characteristics": [
                    "团队内部矛盾",
                    "信任危机",
                    "沟通障碍"
                ],
                "lesson": "内耗往往比外敌更消耗精力"
            }
        }
        
        # 成功要素
        self.success_factors = {
            "信念": {
                "description": "取经必成的决心",
                "manifestation": "唐僧从未动摇西天取经的信念",
                "application": "设定清晰的目标,坚持不懈"
            },
            "团队": {
                "description": "互补的团队配置",
                "manifestation": "各有特长,互补共赢",
                "application": "建立互补型团队"
            },
            "支持": {
                "description": "外部资源与帮助",
                "manifestation": "观音菩萨和天界的帮助",
                "application": "善用外部资源和导师"
            },
            "克服心魔": {
                "description": "战胜自我",
                "manifestation": "六耳猕猴就是孙悟空自己的心魔",
                "application": "认识并克服内心的弱点"
            },
            "坚持": {
                "description": "不放弃",
                "manifestation": "九九八十一难,从不放弃",
                "application": "面对困难不放弃"
            }
        }
    
    def analyze_team_roles(self, team_info: Dict[str, Any]) -> Dict[str, Any]:
        """分析团队角色配置"""
        members = team_info.get("members", [])
        
        default_analysis = {
            "visionary": "唐僧型 - 有愿景,能坚持",
            "executor": "孙悟空型 - 能力强,有主见",
            "regulator": "猪八戒型 - 人缘好,调节气氛",
            "backbone": "沙僧型 - 踏实,默默奉献"
        }
        
        return {
            "team_structure": "取经团队模式",
            "recommended_roles": default_analysis,
            "role_balance": self._analyze_role_balance(members),
            "suggestions": self._generate_role_suggestions(members)
        }
    
    def _analyze_role_balance(self, members: List[Dict]) -> Dict[str, Any]:
        """分析角色平衡"""
        if not members:
            return {
                "balance_score": 7,
                "status": "基本平衡",
                "missing_roles": []
            }
        
        roles = [m.get("role", "") for m in members]
        missing = []
        
        role_types = ["visionary", "executor", "regulator", "backbone"]
        for rt in role_types:
            if rt not in roles:
                missing.append(self.pilgrim_team.get(
                    "唐僧" if rt == "visionary" else 
                    "孙悟空" if rt == "executor" else
                    "猪八戒" if rt == "regulator" else "沙僧",
                    {}
                ).get("role", ""))
        
        return {
            "balance_score": 8 if len(missing) == 0 else 5,
            "status": "平衡" if len(missing) == 0 else "需要补充",
            "missing_roles": missing
        }
    
    def _generate_role_suggestions(self, members: List[Dict]) -> List[str]:
        """generate角色建议"""
        if not members:
            return [
                "明确团队愿景(唐僧型)",
                "培养核心执行者(孙悟空型)",
                "设置氛围调节者(猪八戒型)",
                "确保稳定执行者(沙僧型)"
            ]
        
        return ["团队配置基本合理,保持优化"]
    
    def analyze_growth_path(self, current_level: str) -> Dict[str, Any]:
        """分析成长路径"""
        level_map = {
            "beginner": "stage_1",
            "intermediate": "stage_3",
            "advanced": "stage_4"
        }
        
        current_stage = level_map.get(current_level, "stage_3")
        stage_info = self.growth_stages[current_stage]
        
        return {
            "current_stage": stage_info["name"],
            "description": stage_info["description"],
            "characteristics": stage_info["characteristics"],
            "xiyou_example": stage_info["xiyou_example"],
            "lesson": stage_info["lesson"],
            "next_stage": self._get_next_stage(current_stage),
            "growth_principles": self._get_growth_principles()
        }
    
    def _get_next_stage(self, current_stage: str) -> Dict[str, str]:
        """get下一阶段"""
        next_map = {
            "stage_1": "stage_2",
            "stage_2": "stage_3",
            "stage_3": "stage_4",
            "stage_4": "圆满"
        }
        
        next_stage_key = next_map.get(current_stage, "stage_4")
        if next_stage_key != "圆满":
            return self.growth_stages[next_stage_key]
        return {"name": "功德圆满", "description": "达到目标,实现价值"}
    
    def _get_growth_principles(self) -> List[str]:
        """get成长原则"""
        return [
            "信念第一--坚定目标不动摇",
            "团队协作--独行快,众行远",
            "克服心魔--最大的敌人是自己",
            "坚持修炼--九九八十一难,缺一不可",
            "善用支持--导师和资源的重要性"
        ]
    
    def analyze_trial_type(self, trial_info: Dict[str, Any]) -> Dict[str, Any]:
        """分析困难类型"""
        trial_category = trial_info.get("category", "external")
        trial_intensity = trial_info.get("intensity", 5)
        
        trial_type = self.trials.get(trial_category, self.trials["external"])
        
        return {
            "trial_type": trial_type["name"],
            "characteristics": trial_type["characteristics"],
            "examples": trial_type["examples"][:2],
            "lesson": trial_type["lesson"],
            "intensity_assessment": self._assess_trial_intensity(trial_intensity),
            "coping_strategies": self._generate_coping_strategies(trial_category)
        }
    
    def _assess_trial_intensity(self, intensity: int) -> str:
        """评估困难强度"""
        if intensity <= 3:
            return "轻微 - 容易克服"
        elif intensity <= 6:
            return "中等 - 需要努力"
        elif intensity <= 8:
            return "困难 - 需要团队协作"
        else:
            return "极难 - 需要外部帮助"
    
    def _generate_coping_strategies(self, trial_category: str) -> List[str]:
        """generate应对strategy"""
        strategies_map = {
            "external": ["提升战斗能力", "寻求外部帮助", "智取而非硬拼"],
            "internal": ["认清自我", "坚定信念", "寻求导师指导"],
            "temptation": ["保持清醒", "坚守底线", "寻求同伴支持"],
            "dilemma": ["耐心寻找方法", "善用资源", "等待时机"],
            "relationship": ["加强沟通", "增进理解", "信任队友"]
        }
        return strategies_map.get(trial_category, strategies_map["external"])
    
    def analyze_commitment_level(self, commitment_info: Dict[str, Any]) -> Dict[str, Any]:
        """分析信念坚定程度"""
        goal_clarity = commitment_info.get("goal_clarity", 5)
        persistence = commitment_info.get("persistence", 5)
        resistance = commitment_info.get("resistance", 5)
        
        commitment_score = (goal_clarity + persistence + resistance) / 3
        
        if commitment_score >= 8:
            level = "坚定"
            description = "信念坚定,不为外物所动"
            model = "唐僧 - 取经路上从未动摇"
        elif commitment_score >= 6:
            level = "一般"
            description = "有一定信念,但可能动摇"
            model = "猪八戒 - 时常有退缩之心"
        else:
            level = "薄弱"
            description = "信念不够坚定,容易放弃"
            model = "需要加强修炼"
        
        return {
            "commitment_level": level,
            "commitment_score": round(commitment_score, 2),
            "description": description,
            "role_model": model,
            "improvement_suggestions": self._get_commitment_suggestions(commitment_score)
        }
    
    def _get_commitment_suggestions(self, score: float) -> List[str]:
        """get信念提升建议"""
        if score >= 8:
            return ["继续保持", "帮助其他队友"]
        
        suggestions = []
        if score < 6:
            suggestions.append("明确目标,坚定信念")
        if score < 8:
            suggestions.append("寻找志同道合的伙伴")
        suggestions.append("设置里程碑,庆祝小成功")
        suggestions.append("想象成功后的景象")
        
        return suggestions
    
    def get_growth_diagnosis(self, person_info: Dict[str, Any]) -> Dict[str, Any]:
        """synthesize成长诊断"""
        current_level = person_info.get("experience_level", "intermediate")
        trial_category = person_info.get("current_trial", "external")
        commitment = person_info.get("commitment_level", 5)
        
        growth_path = self.analyze_growth_path(current_level)
        trial_analysis = self.analyze_trial_type({"category": trial_category, "intensity": 5})
        commitment_analysis = self.analyze_commitment_level({"commitment_level": commitment})
        
        return {
            "growth_stage": growth_path["current_stage"],
            "current_trial": trial_analysis["trial_type"],
            "commitment_level": commitment_analysis["commitment_level"],
            "next_step": self._suggest_next_step(person_info),
            "growth_quote": self._get_xiyou_quote()
        }
    
    def _suggest_next_step(self, person_info: Dict[str, Any]) -> List[str]:
        """建议下一步"""
        level = person_info.get("experience_level", "intermediate")
        
        steps_map = {
            "beginner": [
                "先经历挫折,认识自己的局限",
                "寻找导师,获得指导",
                "加入团队,学习协作"
            ],
            "intermediate": [
                "在团队中承担责任",
                "克服更多困难",
                "帮助他人成长"
            ],
            "advanced": [
                "分享经验",
                "成为他人的导师",
                "追求更高的目标"
            ]
        }
        
        return steps_map.get(level, steps_map["intermediate"])
    
    def _get_xiyou_quote(self) -> Dict[str, str]:
        """get西游语录"""
        quotes = [
            {"text": "敢问路在何方?路在脚下.", "context": "信念与action"},
            {"text": "山高自有客行路,水深自有渡船人.", "context": "困难与出路"},
            {"text": "人心生一念,天地悉皆知.善恶若无报,乾坤必有私.", "context": "因果与报应"},
            {"text": "求经路漫漫,意志要坚定.", "context": "坚持的重要性"}
        ]
        import random
        return random.choice(quotes)
    
    def recommend_team_training(self, team_info: Dict[str, Any]) -> Dict[str, Any]:
        """推荐团队修炼方案"""
        return {
            "training_theme": "取经团队修炼",
            "training_phases": [
                {"phase": "第一阶段:觉醒", "duration": "1个月", "content": [
                    "认识自我,发现局限",
                    "明确目标,坚定信念",
                    "理解团队的重要性"
                ]},
                {"phase": "第二阶段:修炼", "duration": "3个月", "content": [
                    "承担角色责任",
                    "克服内心障碍",
                    "学会团队协作"
                ]},
                {"phase": "第三阶段:突破", "duration": "2个月", "content": [
                    "面对重大挑战",
                    "寻求外部支持",
                    "实现自我突破"
                ]},
                {"phase": "第四阶段:圆满", "duration": "持续", "content": [
                    "分享成功经验",
                    "帮助他人成长",
                    "追求更高价值"
                ]}
            ],
            "key_principles": [
                "唐僧的信念--不达目标不罢休",
                "孙悟空的能力--不断提升自己",
                "猪八戒的调节--保持团队活力",
                "沙僧的坚持--默默付出"
            ]
        }

def get_xiyou_engine() -> XiyouGrowthEngine:
    """get西游成长引擎"""
    return XiyouGrowthEngine()

def analyze_growth(info: Dict[str, Any]) -> Dict[str, Any]:
    """分析成长状态"""
    engine = XiyouGrowthEngine()
    return engine.get_growth_diagnosis(info)

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
