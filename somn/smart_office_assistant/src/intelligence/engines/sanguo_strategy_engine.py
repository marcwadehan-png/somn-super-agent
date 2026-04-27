# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze_battle_strategy',
    'analyze_position',
    'analyze_strategic_position',
    'assess_leadership',
    'assess_talent',
    'evaluate_leadership',
    'evaluate_talent',
    'get_sanguo_engine',
    'get_strategic_quote',
    'recommend_battle_strategy',
    'recommend_talent_strategy',
]

三国战略分析引擎 - Sanguo Strategy Engine v1.0.0
==================================================

将<三国演义>的战略智慧转化为现代商业decision工具

核心功能:
- 战略格局分析(魏蜀吴三足鼎立)
- 人才recognize与招揽(三顾茅庐)
- 竞争strategy分析(赤壁之战)
- 领导力评估模型

作者:Somn AI
日期:2026-04-02
"""

from typing import Dict, List, Any, Optional, Tuple
from enum import Enum

class SanguoStrategyEngine:
    """
    三国战略分析引擎
    
    基于<三国演义>的经典战略案例和人物分析,
    为现代商业decision提供战略智慧.
    """
    
    def __init__(self):
        """init三国战略引擎"""
        self.version = "v1.0.0"
        
        # 三大阵营战略模型
        self.kingdoms = {
            "魏": {
                "name": "魏国",
                "leader": "曹操",
                "strategy": "挟天子以令诸侯",
                "core_strength": "资源与实力",
                "weakness": "名不正言不顺",
                "business_model": "资源整合型",
                "characteristics": ["务实", "功利", "高效", "冷酷"]
            },
            "蜀": {
                "name": "蜀国",
                "leader": "刘备",
                "strategy": "联吴抗曹",
                "core_strength": "品牌与人心",
                "weakness": "资源匮乏",
                "business_model": "差异化型",
                "characteristics": ["仁德", "正义", "理想主义", "忠诚"]
            },
            "吴": {
                "name": "吴国",
                "leader": "孙权",
                "strategy": "鼎足江东",
                "core_strength": "地利与水军",
                "weakness": "进取心不足",
                "business_model": "稳健经营型",
                "characteristics": ["保守", "稳健", "务实", "守成"]
            }
        }
        
        # 经典战略案例库
        self.strategic_cases = {
            "隆中对": {
                "strategist": "诸葛亮",
                "context": "刘备三顾茅庐请教天下大势",
                "core_insight": "天下三分,联吴抗曹",
                "key_points": [
                    "荆州--四战之地,可图",
                    "益州--天府之国,可守",
                    "内修政理,外结孙权"
                ],
                "business_application": "差异化竞争 + 战略联盟"
            },
            "赤壁之战": {
                "strategist": "周瑜",
                "context": "曹操南下,意图一统天下",
                "core_insight": "以少胜多,火攻破敌",
                "key_points": [
                    "连环计--unified指挥",
                    "苦肉计--黄盖诈降",
                    "东南风--天时配合"
                ],
                "business_application": "弱者通过创新以小博大"
            },
            "三顾茅庐": {
                "strategist": "刘备",
                "context": "求贤若渴,三次拜访诸葛亮",
                "core_insight": "诚心求才,礼贤下士",
                "key_points": [
                    "不因多次拒绝而放弃",
                    "亲自登门拜访",
                    "给予充分信任和授权"
                ],
                "business_application": "顶尖人才需要诚意和耐心"
            },
            "官渡之战": {
                "strategist": "曹操",
                "context": "袁绍以十倍兵力进攻",
                "core_insight": "粮草决定胜负,关键一击",
                "key_points": [
                    "许攸献策",
                    "夜袭乌巢",
                    "烧毁袁绍粮草"
                ],
                "business_application": "抓住关键转折点"
            },
            "空城计": {
                "strategist": "诸葛亮",
                "context": "司马懿大军压境",
                "core_insight": "心理战术,以虚胜实",
                "key_points": [
                    "大开城门",
                    "焚香弹琴",
                    "示弱以惑敌"
                ],
                "business_application": "危机中的心理博弈"
            }
        }
        
        # 人才类型模型
        self.talent_types = {
            "创业领袖": {
                "representative": "刘备",
                "traits": ["有愿景", "会用人", "能凝聚人心", "坚韧不拔"],
                "weakness": ["执行力相对较弱", "过于理想主义"],
                "suitable_roles": ["CEO", "创始人", "愿景领袖"]
            },
            "战略大师": {
                "representative": "诸葛亮",
                "traits": ["洞察全局", "规划长远", "执行力强", "事必躬亲"],
                "weakness": ["难以授权", "过度操劳"],
                "suitable_roles": ["首席战略官", "COO", "军师"]
            },
            "执行悍将": {
                "representative": "关羽/张飞",
                "traits": ["战斗力强", "忠诚度高", "果敢勇猛"],
                "weakness": ["性格缺陷", "难以独当大局"],
                "suitable_roles": ["销售总监", "业务负责人", "业务骨干"]
            },
            "守成之主": {
                "representative": "孙权",
                "traits": ["知人善任", "稳定大局", "善于平衡"],
                "weakness": ["进取心不足", "缺乏开拓精神"],
                "suitable_roles": ["守成型CEO", "稳定期企业领导"]
            },
            "权谋之主": {
                "representative": "曹操",
                "traits": ["唯才是举", "务实高效", "知人善任"],
                "weakness": ["多疑冷酷", "树敌过多"],
                "suitable_roles": ["扩张期企业领导", "并购整合专家"]
            }
        }
        
        # 领导力评估维度
        self.leadership_dimensions = {
            "vision": {
                "name": "愿景能力",
                "description": "制定和传达愿景的能力",
                "weight": 0.25,
                "indicators": ["战略眼光", "目标清晰度", "感召力"]
            },
            "execution": {
                "name": "执行能力",
                "description": "推动目标实现的能力",
                "weight": 0.30,
                "indicators": ["决断力", "组织力", "控制力"]
            },
            "talent": {
                "name": "人才能力",
                "description": "发现和培养人才的能力",
                "weight": 0.25,
                "indicators": ["识人", "用人", "育人"]
            },
            "adaptation": {
                "name": "适应能力",
                "description": "应对变化和危机的能力",
                "weight": 0.20,
                "indicators": ["危机处理", "灵活应变", "学习成长"]
            }
        }
    
    def analyze_strategic_position(self, company_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析企业战略定位
        
        Args:
            company_info: 企业信息
            
        Returns:
            战略定位分析报告
        """
        resources = company_info.get("resources", "medium")
        brand = company_info.get("brand", "medium")
        innovation = company_info.get("innovation", "medium")
        culture = company_info.get("culture", "medium")
        
        # 根据企业characteristics匹配三国阵营
        if resources >= "high" and brand >= "medium":
            kingdom = "魏"
            recommendation = "资源整合型战略"
        elif brand >= "high" and resources <= "low":
            kingdom = "蜀"
            recommendation = "差异化竞争战略"
        else:
            kingdom = "吴"
            recommendation = "稳健经营型战略"
        
        # get建议的经典案例
        recommended_cases = []
        if kingdom == "魏":
            recommended_cases = ["官渡之战", "挟天子以令诸侯"]
        elif kingdom == "蜀":
            recommended_cases = ["隆中对", "赤壁之战"]
        else:
            recommended_cases = ["榻上策", "固守江东"]
        
        return {
            "recommended_kingdom": kingdom,
            "kingdom_info": self.kingdoms[kingdom],
            "recommendation": recommendation,
            "recommended_cases": recommended_cases,
            "strategy_principles": self._get_strategy_principles(kingdom),
            "risk_warnings": self._get_kingdom_risks(kingdom)
        }
    
    def _get_strategy_principles(self, kingdom: str) -> List[str]:
        """get战略原则"""
        principles_map = {
            "魏": [
                "资源整合,发挥规模优势",
                "唯才是举,吸引顶尖人才",
                "快速扩张,抢占市场份额"
            ],
            "蜀": [
                "差异化定位,聚焦细分市场",
                "品牌优先,建立用户忠诚",
                "战略联盟,借力发展"
            ],
            "吴": [
                "稳健经营,聚焦核心能力",
                "深耕本地,建立护城河",
                "伺机而动,等待时机"
            ]
        }
        return principles_map.get(kingdom, [])
    
    def _get_kingdom_risks(self, kingdom: str) -> List[str]:
        """get阵营风险"""
        risks_map = {
            "魏": [
                "树敌过多,陷入包围",
                "大企业病,效率降低",
                "名不正言不顺,人心不服"
            ],
            "蜀": [
                "资源有限,难以支撑长期竞争",
                "过度依赖核心人物",
                "差异化优势可能被模仿"
            ],
            "吴": [
                "进取心不足,错失发展机会",
                "人才断层,后继乏人",
                "过于保守,被时代淘汰"
            ]
        }
        return risks_map.get(kingdom, [])
    
    def analyze_battle_strategy(self, battle_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析竞争战役strategy
        
        Args:
            battle_info: 竞争信息
            
        Returns:
            战役strategy分析
        """
        our_strength = battle_info.get("our_strength", "medium")
        enemy_strength = battle_info.get("enemy_strength", "medium")
        our_advantages = battle_info.get("our_advantages", [])
        time_constraint = battle_info.get("time_constraint", "medium")
        
        # 根据实力对比选择strategy
        if our_strength >= enemy_strength:
            # 实力相当或更强
            if time_constraint == "urgent":
                strategy = "官渡之战模式"
                case = self.strategic_cases["官渡之战"]
            else:
                strategy = "稳扎稳打模式"
                case = self.strategic_cases["隆中对"]
        else:
            # 实力较弱
            if our_advantages:
                strategy = "赤壁之战模式"
                case = self.strategic_cases["赤壁之战"]
            else:
                strategy = "空城计模式"
                case = self.strategic_cases["空城计"]
        
        return {
            "recommended_strategy": strategy,
            "case_analysis": case,
            "action_plan": self._generate_battle_plan(strategy),
            "key_success_factors": self._get_battle_success_factors(strategy),
            "risk_warnings": self._get_battle_risks(strategy)
        }
    
    def _generate_battle_plan(self, strategy: str) -> List[str]:
        """generate战役计划"""
        plans_map = {
            "官渡之战模式": [
                "分析敌我双方核心资源",
                "找到关键突破点(如粮草)",
                "集中优势兵力一击",
                "速战速决"
            ],
            "赤壁之战模式": [
                "利用地形/环境优势",
                "设计连环计,unified协调",
                "诈降get信任",
                "关键时刻的火攻"
            ],
            "空城计模式": [
                "评估敌方心理",
                "展示出乎意料的布局",
                "以虚示强,心理博弈",
                "准备后援/撤退方案"
            ],
            "隆中对模式": [
                "制定长期战略规划",
                "建立战略联盟",
                "巩固核心根据地",
                "分阶段推进"
            ]
        }
        return plans_map.get(strategy, [])
    
    def _get_battle_success_factors(self, strategy: str) -> List[str]:
        """get战役成功要素"""
        factors_map = {
            "官渡之战模式": ["准确judge关键点", "保密措施到位", "果断执行"],
            "赤壁之战模式": ["团队协作", "创意战术", "天时配合"],
            "空城计模式": ["准确把握对手心理", "充分的准备", "镇定自若"],
            "隆中对模式": ["清晰的战略规划", "耐心执行", "灵活调整"]
        }
        return factors_map.get(strategy, [])
    
    def _get_battle_risks(self, strategy: str) -> List[str]:
        """get战役风险"""
        risks_map = {
            "官渡之战模式": ["judge失误,满盘皆输", "执行不力,丧失战机"],
            "赤壁之战模式": ["联盟破裂", "天气变化", "内部泄密"],
            "空城计模式": ["对手不按套路", "心理素质不过关"],
            "隆中对模式": ["时间太长,变数太多", "执行偏离战略"]
        }
        return risks_map.get(strategy, [])
    
    def evaluate_talent(self, talent_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        评估人才类型
        
        Args:
            talent_info: 人才信息
            
        Returns:
            人才评估报告
        """
        vision = talent_info.get("vision", 5)
        execution = talent_info.get("execution", 5)
        loyalty = talent_info.get("loyalty", 5)
        innovation = talent_info.get("innovation", 5)
        
        # 计算synthesize评分
        scores = {"vision": vision, "execution": execution, "loyalty": loyalty, "innovation": innovation}
        
        # 匹配人才类型
        if vision >= 8 and execution >= 7:
            talent_type = "创业领袖"
        elif vision >= 7 and innovation >= 8:
            talent_type = "战略大师"
        elif execution >= 8 and loyalty >= 7:
            talent_type = "执行悍将"
        elif execution >= 6 and vision >= 6 and loyalty >= 8:
            talent_type = "守成之主"
        else:
            talent_type = "权谋之主"
        
        talent_detail = self.talent_types[talent_type]
        
        return {
            "talent_type": talent_type,
            "representative": talent_detail["representative"],
            "traits": talent_detail["traits"],
            "weakness": talent_detail["weakness"],
            "suitable_roles": talent_detail["suitable_roles"],
            "scores": scores,
            "development_suggestions": self._generate_development_suggestions(talent_type, scores)
        }
    
    def _generate_development_suggestions(self, talent_type: str, scores: Dict[str, int]) -> List[str]:
        """generate发展建议"""
        suggestions = []
        
        for dimension, score in scores.items():
            if score < 6:
                dimension_names = {
                    "vision": "愿景能力",
                    "execution": "执行能力",
                    "loyalty": "忠诚度",
                    "innovation": "创新能力"
                }
                suggestions.append(f"加强{dimension_names[dimension]}的培养")
        
        if not suggestions:
            suggestions.append("继续保持优势,均衡发展")
        
        return suggestions
    
    def recommend_talent_strategy(self, company_stage: str) -> Dict[str, Any]:
        """
        推荐人才战略
        
        Args:
            company_stage: 企业阶段 (startup/growth/mature/decline)
            
        Returns:
            人才战略建议
        """
        strategies = {
            "startup": {
                "recommendation": "三顾茅庐模式",
                "focus": "招揽顶尖人才,给予充分信任",
                "case": self.strategic_cases["三顾茅庐"],
                "actions": [
                    "明确人才标准",
                    "主动出击,不惜成本",
                    "给予充分授权",
                    "建立信任关系"
                ]
            },
            "growth": {
                "recommendation": "唯才是举模式",
                "focus": "快速扩张人才队伍,唯才是举",
                "case": self.talent_types["权谋之主"],
                "actions": [
                    "建立人才梯队",
                    "设立竞争机制",
                    "快速提拔有能力者",
                    "保持团队活力"
                ]
            },
            "mature": {
                "recommendation": "知人善任模式",
                "focus": "稳定团队,知人善任",
                "case": self.talent_types["守成之主"],
                "actions": [
                    "优化人才结构",
                    "培养接班人",
                    "平衡老人与新人",
                    "保持组织稳定"
                ]
            },
            "decline": {
                "recommendation": "刘备模式",
                "focus": "重塑愿景,重新凝聚人心",
                "case": self.strategic_cases["隆中对"],
                "actions": [
                    "明确转型方向",
                    "寻找新增长点",
                    "稳定核心团队",
                    "大胆启用新人"
                ]
            }
        }
        
        return strategies.get(company_stage, strategies["growth"])
    
    def evaluate_leadership(self, leader_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        评估领导力
        
        Args:
            leader_info: 领导者信息
            
        Returns:
            领导力评估报告
        """
        # 提取评分
        scores = {
            "vision": leader_info.get("vision_score", 5),
            "execution": leader_info.get("execution_score", 5),
            "talent": leader_info.get("talent_score", 5),
            "adaptation": leader_info.get("adaptation_score", 5)
        }
        
        # 计算加权总分
        total_score = sum(
            scores[dim] * self.leadership_dimensions[dim]["weight"]
            for dim in scores
        )
        
        # 匹配历史人物
        if total_score >= 9:
            historical_match = "刘备 + 诸葛亮(理想型)"
            description = "具有远见卓识和强大执行力"
        elif total_score >= 7:
            historical_match = "曹操"
            description = "务实高效,知人善任"
        elif total_score >= 5:
            historical_match = "孙权"
            description = "稳健持重,善于守成"
        else:
            historical_match = "袁绍"
            description = "需要大幅提升领导力"
        
        # generate改进建议
        improvements = []
        for dim, score in scores.items():
            if score < 7:
                dim_info = self.leadership_dimensions[dim]
                improvements.append({
                    "dimension": dim_info["name"],
                    "current_score": score,
                    "target_score": 8,
                    "suggestions": self._get_dimension_suggestions(dim)
                })
        
        return {
            "total_score": round(total_score, 2),
            "historical_match": historical_match,
            "description": description,
            "dimension_scores": {
                self.leadership_dimensions[dim]["name"]: score
                for dim, score in scores.items()
            },
            "improvements_needed": improvements,
            "learning_references": self._get_learning_references(historical_match)
        }
    
    def _get_dimension_suggestions(self, dimension: str) -> List[str]:
        """get维度改进建议"""
        suggestions_map = {
            "vision": [
                "加强行业研究",
                "参加战略规划培训",
                "与行业专家交流"
            ],
            "execution": [
                "学习项目管理方法",
                "建立高效decision机制",
                "加强团队执行力"
            ],
            "talent": [
                "学习人才评估方法",
                "建立人才梯队",
                "加强沟通与激励"
            ],
            "adaptation": [
                "增强危机意识",
                "学习变革管理",
                "保持开放心态"
            ]
        }
        return suggestions_map.get(dimension, [])
    
    def _get_learning_references(self, historical_match: str) -> List[str]:
        """get学习参考"""
        references = {
            "刘备 + 诸葛亮(理想型)": [
                "刘备的仁德与凝聚人心",
                "诸葛亮的战略规划与执行"
            ],
            "曹操": [
                "曹操的务实与效率",
                "曹操的唯才是举"
            ],
            "孙权": [
                "孙权的知人善任",
                "孙权的稳健经营"
            ],
            "袁绍": [
                "袁绍失败教训",
                "如何避免优柔寡断"
            ]
        }
        return references.get(historical_match, [])
    
    def get_strategic_quote(self, theme: str) -> Dict[str, str]:
        """
        get战略语录
        
        Args:
            theme: 主题
            
        Returns:
            语录
        """
        quotes = {
            "战略": {
                "text": "天下大势,分久必合,合久必分.",
                "author": "罗贯中",
                "interpretation": "商业竞争也有周期性规律"
            },
            "领导": {
                "text": "勿以恶小而为之,勿以善小而不为.",
                "author": "刘备",
                "interpretation": "领导者的以身作则很重要"
            },
            "人才": {
                "text": "卧龙凤雏,得一可安天下.",
                "author": "司马徽",
                "interpretation": "顶尖人才是稀缺资源"
            },
            "decision": {
                "text": "谋事在人,成事在天.",
                "author": "诸葛亮",
                "interpretation": "尽力而为,顺势而为"
            },
            "竞争": {
                "text": "知己知彼,百战不殆.",
                "author": "孙子",
                "interpretation": "了解竞争对手是竞争的基础"
            }
        }
        
        return quotes.get(theme, quotes["战略"])

# ==================== 便捷函数 ====================

def get_sanguo_engine() -> SanguoStrategyEngine:
    """get三国战略引擎实例"""
    return SanguoStrategyEngine()

def analyze_position(company_info: Dict[str, Any]) -> Dict[str, Any]:
    """分析企业战略定位"""
    engine = SanguoStrategyEngine()
    return engine.analyze_strategic_position(company_info)

def recommend_battle_strategy(battle_info: Dict[str, Any]) -> Dict[str, Any]:
    """推荐竞争strategy"""
    engine = SanguoStrategyEngine()
    return engine.analyze_battle_strategy(battle_info)

def assess_talent(talent_info: Dict[str, Any]) -> Dict[str, Any]:
    """评估人才"""
    engine = SanguoStrategyEngine()
    return engine.evaluate_talent(talent_info)

def assess_leadership(leader_info: Dict[str, Any]) -> Dict[str, Any]:
    """评估领导力"""
    engine = SanguoStrategyEngine()
    return engine.evaluate_leadership(leader_info)

# ==================== 测试代码 ====================

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
