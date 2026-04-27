# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze_emotional_intelligence',
    'analyze_family_stage',
    'analyze_human_relations',
    'analyze_personality',
    'analyze_relationship',
    'diagnose_enterprise',
    'diagnose_enterprise_risks',
    'get_honglou_engine',
    'get_insight_diagnosis',
]

红楼人情洞察引擎 - Honglou Insight Engine v1.0.0
===============================================

将<红楼梦>的人情世故智慧转化为现代人际关系洞察工具

核心功能:
- 家族企业兴衰分析
- 人际关系洞察
- 情感智慧分析
- 组织政治智慧

作者:Somn AI
日期:2026-04-02
"""

from typing import Dict, List, Any, Optional

class HonglouInsightEngine:
    """
    红楼人情洞察引擎
    
    基于<红楼梦>的经典人物和情节,
    为人际关系和情感洞察提供智慧.
    """
    
    def __init__(self):
        """init红楼洞察引擎"""
        self.version = "v1.0.0"
        
        # 家族兴衰周期模型
        self.family_cycle = {
            "prosperity": {
                "name": "鼎盛期",
                "signs": [
                    "烈火烹油,鲜花着锦",
                    "经济繁荣,人丁兴旺",
                    "社会地位高,权势滔天"
                ],
                "honglou_example": "元春省亲--贾府鼎盛的标志",
                "management_focus": "繁华时的危机意识"
            },
            "transition": {
                "name": "转折期",
                "signs": [
                    "内部争斗开始",
                    "资源浪费加剧",
                    "方向迷失"
                ],
                "honglou_example": "抄检大观园--矛盾开始爆发",
                "management_focus": "recognize早期预警信号"
            },
            "decline": {
                "name": "衰落期",
                "signs": [
                    "核心人物去世",
                    "领导力真空",
                    "人心涣散"
                ],
                "honglou_example": "贾母去世,凤姐病逝",
                "management_focus": "核心人才风险管理"
            },
            "collapse": {
                "name": "败落期",
                "signs": [
                    "外部打击",
                    "树倒猢狲散",
                    "一无所有"
                ],
                "honglou_example": "贾府被抄--大厦倾覆",
                "management_focus": "危机应对与重建"
            }
        }
        
        # 核心人物性格分析
        self.characters = {
            "贾宝玉": {
                "role": "叛逆者",
                "strengths": [
                    "善良真诚",
                    "审美情趣高",
                    "重情重义"
                ],
                "weaknesses": [
                    "不愿走仕途经济",
                    "过于天真",
                    "逃避现实"
                ],
                "lesson": "理想主义需要与现实妥协"
            },
            "林黛玉": {
                "role": "才情者",
                "strengths": [
                    "才情绝世",
                    "情感细腻",
                    "真实不做作"
                ],
                "weaknesses": [
                    "多愁多病",
                    "清高孤傲",
                    "不善交际"
                ],
                "lesson": "才情与生存需要平衡"
            },
            "薛宝钗": {
                "role": "现实者",
                "strengths": [
                    "温柔敦厚",
                    "城府深沉",
                    "善于处理关系"
                ],
                "weaknesses": [
                    "过于功利",
                    "缺乏真情",
                    "压抑自我"
                ],
                "lesson": "现实成功不等于幸福"
            },
            "王熙凤": {
                "role": "管理者",
                "strengths": [
                    "精明能干",
                    "雷厉风行",
                    "管理能力强"
                ],
                "weaknesses": [
                    "心狠手辣",
                    "过度揽权",
                    "过于算计"
                ],
                "lesson": "能力与道德需要平衡"
            },
            "刘姥姥": {
                "role": "智者",
                "strengths": [
                    "朴实善良",
                    "知恩图报",
                    "智慧通达"
                ],
                "weaknesses": [
                    "出身卑微",
                    "缺乏教育"
                ],
                "lesson": "善良和智慧比地位更重要"
            },
            "探春": {
                "role": "改革者",
                "strengths": [
                    "精明能干",
                    "有见识",
                    "敢于改革"
                ],
                "weaknesses": [
                    "庶出身份",
                    "难以施展抱负"
                ],
                "lesson": "改革需要一把手支持"
            }
        }
        
        # 人际关系模式
        self.relationship_patterns = {
            "木石前盟": {
                "type": "理想型关系",
                "description": "宝黛爱情--真挚但脆弱",
                "characteristics": [
                    "两情相悦",
                    "不为世俗所容",
                    "最终悲剧"
                ],
                "lesson": "理想与现实难以调和"
            },
            "金玉良缘": {
                "type": "现实型关系",
                "description": "宝玉宝钗婚姻--稳定但缺乏爱情",
                "characteristics": [
                    "门当户对",
                    "条件匹配",
                    "情感淡漠"
                ],
                "lesson": "现实婚姻不等于幸福"
            },
            "王熙凤与贾琏": {
                "type": "利益型关系",
                "description": "共富贵易,同患难难",
                "characteristics": [
                    "表面和谐",
                    "内里矛盾",
                    "危机时各自打算"
                ],
                "lesson": "利益关系经不起考验"
            },
            "刘姥姥与贾府": {
                "type": "施恩型关系",
                "description": "善有善报--刘姥姥救巧姐",
                "characteristics": [
                    "知恩图报",
                    "危难时伸援手",
                    "跨越阶层的友谊"
                ],
                "lesson": "善良最终会有回报"
            }
        }
        
        # 家族企业警示
        self.enterprise_warnings = [
            {
                "issue": "经济管理混乱",
                "manifestation": "贾府入不敷出",
                "lesson": "加强财务管理"
            },
            {
                "issue": "接班人问题",
                "manifestation": "宝玉不愿走仕途",
                "lesson": "培养合格的接班人"
            },
            {
                "issue": "人才断层",
                "manifestation": "贾敬出家,贾珍荒淫",
                "lesson": "建立人才梯队"
            },
            {
                "issue": "内斗消耗",
                "manifestation": "王夫人与邢夫人争权",
                "lesson": "避免内部斗争"
            },
            {
                "issue": "过度依赖外部资源",
                "manifestation": "元春的庇护不可持续",
                "lesson": "建立独立能力"
            },
            {
                "issue": "创新不足",
                "manifestation": "守着祖业不思进取",
                "lesson": "持续创新"
            }
        ]
        
        # 人生哲理
        self.life_philosophy = {
            "繁华与虚无": {
                "quote": "赤条条来去无牵挂",
                "interpretation": "一切皆空,珍惜当下"
            },
            "真与假": {
                "quote": "假作真时真亦假,无为有处有还无",
                "interpretation": "世事如梦,看清本质"
            },
            "情与理": {
                "quote": "情之所钟,正在我辈",
                "interpretation": "真情是可贵的"
            },
            "得与失": {
                "quote": "机关算尽太聪明,反误了卿卿性命",
                "interpretation": "不要过于算计"
            },
            "生与死": {
                "quote": "纵有千年铁门槛,终须一个土馒头",
                "interpretation": "生死无常,坦然面对"
            }
        }
    
    def analyze_family_stage(self, family_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析家族/企业所处阶段
        
        Args:
            family_info: 家族/企业信息
            
        Returns:
            阶段分析报告
        """
        economy = family_info.get("economy", "medium")  # 经济状况
        harmony = family_info.get("harmony", "medium")  # 内部和谐
        leadership = family_info.get("leadership", "medium")  # 领导力
        innovation = family_info.get("innovation", "medium")  # 创新能力
        
        # 计算synthesize得分
        score_map = {"high": 8, "medium": 5, "low": 2}
        scores = {
            "economy": score_map.get(economy, 5),
            "harmony": score_map.get(harmony, 5),
            "leadership": score_map.get(leadership, 5),
            "innovation": score_map.get(innovation, 5)
        }
        avg_score = sum(scores.values()) / len(scores)
        
        # 确定阶段
        if avg_score >= 7:
            stage = "prosperity"
        elif avg_score >= 5:
            stage = "transition"
        elif avg_score >= 3:
            stage = "decline"
        else:
            stage = "collapse"
        
        stage_info = self.family_cycle[stage]
        
        return {
            "current_stage": stage_info["name"],
            "signs": stage_info["signs"],
            "honglou_reference": stage_info["honglou_example"],
            "management_focus": stage_info["management_focus"],
            "scores": scores,
            "warnings": self._get_stage_warnings(stage),
            "suggestions": self._generate_stage_suggestions(stage, scores)
        }
    
    def _get_stage_warnings(self, stage: str) -> List[str]:
        """get阶段警示"""
        warnings_map = {
            "prosperity": [
                "警惕过度消费",
                "防止内部矛盾积累",
                "注意培养接班人"
            ],
            "transition": [
                "及时处理内部矛盾",
                "控制成本",
                "unified发展方向"
            ],
            "decline": [
                "稳定核心团队",
                "寻找新的增长点",
                "防止人才流失"
            ],
            "collapse": [
                "果断止损",
                "保护核心资产",
                "准备东山再起"
            ]
        }
        return warnings_map.get(stage, [])
    
    def _generate_stage_suggestions(self, stage: str, scores: Dict[str, int]) -> List[str]:
        """generate阶段建议"""
        suggestions = []
        
        if scores.get("economy", 5) < 6:
            suggestions.append("加强财务管理,开源节流")
        if scores.get("harmony", 5) < 6:
            suggestions.append("化解内部矛盾,unified思想")
        if scores.get("leadership", 5) < 6:
            suggestions.append("培养领导力,建立梯队")
        if scores.get("innovation", 5) < 6:
            suggestions.append("鼓励创新,寻找新方向")
        
        if not suggestions:
            suggestions.append("保持当前状态,做好风险管理")
        
        return suggestions
    
    def analyze_personality(self, person_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析人物性格
        
        Args:
            person_info: 人物信息
            
        Returns:
            性格分析报告
        """
        emotional = person_info.get("emotional", 5)
        practical = person_info.get("practical", 5)
        social = person_info.get("social", 5)
        independent = person_info.get("independent", 5)
        
        # 计算性格characteristics
        score_map = {
            "emotional": emotional,
            "practical": practical,
            "social": social,
            "independent": independent
        }
        
        # 匹配人物类型
        if emotional >= 8 and practical < 5:
            char_type = "贾宝玉/林黛玉"
            reference = self.characters["林黛玉"]
        elif practical >= 8 and emotional < 5:
            char_type = "薛宝钗"
            reference = self.characters["薛宝钗"]
        elif social >= 8 and practical >= 7:
            char_type = "王熙凤"
            reference = self.characters["王熙凤"]
        elif emotional >= 6 and social >= 6:
            char_type = "刘姥姥"
            reference = self.characters["刘姥姥"]
        else:
            char_type = "探春"
            reference = self.characters["探春"]
        
        return {
            "personality_type": char_type,
            "reference_character": reference,
            "strengths": reference["strengths"],
            "weaknesses": reference["weaknesses"],
            "life_lesson": reference["lesson"],
            "relationship_advice": self._get_relationship_advice(char_type),
            "score_breakdown": score_map
        }
    
    def _get_relationship_advice(self, char_type: str) -> List[str]:
        """get关系建议"""
        advice_map = {
            "贾宝玉/林黛玉": [
                "学会与现实妥协",
                "不要太理想主义",
                "培养实际能力"
            ],
            "薛宝钗": [
                "不要压抑真实情感",
                "学会真诚待人",
                "不要太算计"
            ],
            "王熙凤": [
                "注意道德底线",
                "不要过度揽权",
                "学会分享功劳"
            ],
            "刘姥姥": [
                "保持善良本色",
                "学会适应不同场合",
                "知恩图报"
            ],
            "探春": [
                "寻找施展才华的舞台",
                "不要被出身限制",
                "大胆表达想法"
            ]
        }
        return advice_map.get(char_type, [])
    
    def analyze_relationship(self, relationship_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析人际关系
        
        Args:
            relationship_info: 关系信息
            
        Returns:
            关系分析报告
        """
        relationship_type = relationship_info.get("type", "ideal")
        authenticity = relationship_info.get("authenticity", 5)
        stability = relationship_info.get("stability", 5)
        
        # 匹配关系模式
        if authenticity >= 7 and stability < 6:
            pattern = "木石前盟"
        elif stability >= 7 and authenticity < 6:
            pattern = "金玉良缘"
        elif relationship_info.get("based_on_interest", False):
            pattern = "王熙凤与贾琏"
        else:
            pattern = "刘姥姥与贾府"
        
        pattern_info = self.relationship_patterns[pattern]
        
        return {
            "relationship_pattern": pattern,
            "pattern_type": pattern_info["type"],
            "description": pattern_info["description"],
            "characteristics": pattern_info["characteristics"],
            "lesson": pattern_info["lesson"],
            "health_score": self._calculate_relationship_health(authenticity, stability),
            "improvement_suggestions": self._get_relationship_improvements(authenticity, stability)
        }
    
    def _calculate_relationship_health(self, authenticity: int, stability: int) -> Dict[str, Any]:
        """计算关系健康度"""
        health_score = (authenticity + stability) / 2
        
        if health_score >= 8:
            status = "健康"
        elif health_score >= 6:
            status = "一般"
        else:
            status = "需要改善"
        
        return {
            "score": round(health_score, 2),
            "status": status
        }
    
    def _get_relationship_improvements(self, authenticity: int, stability: int) -> List[str]:
        """get关系改进建议"""
        suggestions = []
        
        if authenticity < 6:
            suggestions.append("增加真诚交流")
            suggestions.append("减少伪装和算计")
        if stability < 6:
            suggestions.append("建立共同目标")
            suggestions.append("加强信任建设")
        if not suggestions:
            suggestions.append("继续保持这种健康的关系")
        
        return suggestions
    
    def analyze_emotional_intelligence(self, eq_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析情商水平
        
        Args:
            eq_info: 情商信息
            
        Returns:
            情商分析报告
        """
        self_awareness = eq_info.get("self_awareness", 5)
        self_regulation = eq_info.get("self_regulation", 5)
        empathy = eq_info.get("empathy", 5)
        social_skills = eq_info.get("social_skills", 5)
        
        eq_score = (self_awareness + self_regulation + empathy + social_skills) / 4
        
        # 匹配红楼人物
        if eq_score >= 8:
            reference = "薛宝钗 - 情商极高,善于处理关系"
        elif eq_score >= 6:
            reference = "王熙凤 - 社交能力强,但有时过犹不及"
        elif eq_score >= 4:
            reference = "林黛玉 - 情感丰富,但不善交际"
        else:
            reference = "迎春 - 过于软弱,需要提升"
        
        return {
            "eq_score": round(eq_score, 2),
            "reference": reference,
            "dimensions": {
                "self_awareness": self_awareness,
                "self_regulation": self_regulation,
                "empathy": empathy,
                "social_skills": social_skills
            },
            "strengths": self._identify_eq_strengths(self_awareness, self_regulation, empathy, social_skills),
            "areas_for_improvement": self._identify_eq_improvements(self_awareness, self_regulation, empathy, social_skills),
            "honglou_advice": self._get_eq_advice(eq_score)
        }
    
    def _identify_eq_strengths(self, sa: int, sr: int, em: int, ss: int) -> List[str]:
        """recognize情商优势"""
        strengths = []
        if sa >= 7:
            strengths.append("自我认知清晰")
        if sr >= 7:
            strengths.append("情绪控制良好")
        if em >= 7:
            strengths.append("同理心强")
        if ss >= 7:
            strengths.append("社交技巧熟练")
        return strengths if strengths else ["各方面均衡发展"]
    
    def _identify_eq_improvements(self, sa: int, sr: int, em: int, ss: int) -> List[str]:
        """recognize情商改进点"""
        improvements = []
        if sa < 6:
            improvements.append("加强自我反思,提高自我认知")
        if sr < 6:
            improvements.append("学习情绪管理技巧")
        if em < 6:
            improvements.append("多倾听他人,培养同理心")
        if ss < 6:
            improvements.append("学习社交技巧,多与人交流")
        return improvements if improvements else ["继续保持"]
    
    def _get_eq_advice(self, score: float) -> Dict[str, str]:
        """get红楼梦式情商建议"""
        if score >= 8:
            return {
                "model": "薛宝钗",
                "advice": "你的情商很高,但要记得真诚比技巧更重要"
            }
        elif score >= 6:
            return {
                "model": "王熙凤",
                "advice": "社交能力强,但注意不要过于算计"
            }
        elif score >= 4:
            return {
                "model": "林黛玉",
                "advice": "情感丰富是优势,但也要学会与不同人相处"
            }
        else:
            return {
                "model": "刘姥姥",
                "advice": "善良是根本,在此基础上学习社交技巧"
            }
    
    def diagnose_enterprise_risks(self, enterprise_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        诊断企业风险
        
        Args:
            enterprise_info: 企业信息
            
        Returns:
            风险诊断报告
        """
        # recognize风险
        risks = []
        warnings = enterprise_info.get("warnings", [])
        
        for warning in self.enterprise_warnings:
            if warning["issue"] in warnings or not warnings:
                risks.append({
                    "issue": warning["issue"],
                    "manifestation": warning["manifestation"],
                    "lesson": warning["lesson"],
                    "severity": "high"
                })
        
        return {
            "enterprise_risks": risks,
            "honglou_case_study": self._get_case_study(),
            "prevention_strategies": self._get_prevention_strategies(risks),
            "crisis_management": self._get_crisis_management()
        }
    
    def _get_case_study(self) -> Dict[str, str]:
        """get案例研究"""
        return {
            "title": "王熙凤管理宁国府",
            "strengths": "精明能干,雷厉风行,责任到人",
            "weaknesses": "心狠手辣,过度揽权",
            "lesson": "能力与道德需要平衡"
        }
    
    def _get_prevention_strategies(self, risks: List[Dict]) -> List[str]:
        """get预防strategy"""
        strategies = []
        for risk in risks:
            strategies.append(f"预防{risk['issue']}:{risk['lesson']}")
        return strategies if strategies else ["加强全面风险管理"]
    
    def _get_crisis_management(self) -> Dict[str, Any]:
        """get危机管理建议"""
        return {
            "crisis_warning_signs": [
                "内部争斗加剧",
                "核心人才流失",
                "财务状况恶化",
                "创新能力下降"
            ],
            "response_strategy": [
                "冷静分析形势",
                "果断采取action",
                "保护核心资产",
                "准备东山再起"
            ],
            "honglou_inspiration": "刘姥姥的智慧--无论处于什么地位,都要保持善良和智慧"
        }
    
    def get_insight_diagnosis(self, info: Dict[str, Any]) -> Dict[str, Any]:
        """
        synthesize洞察诊断
        
        Args:
            info: synthesize信息
            
        Returns:
            synthesize诊断报告
        """
        info_type = info.get("type", "family")
        
        if info_type == "family":
            diagnosis = self.analyze_family_stage(info)
        elif info_type == "personality":
            diagnosis = self.analyze_personality(info)
        elif info_type == "relationship":
            diagnosis = self.analyze_relationship(info)
        elif info_type == "eq":
            diagnosis = self.analyze_emotional_intelligence(info)
        else:
            diagnosis = self.diagnose_enterprise_risks(info)
        
        return {
            "diagnosis": diagnosis,
            "life_quote": self._get_honglou_quote(),
            "action_plan": self._generate_action_plan(diagnosis, info_type)
        }
    
    def _generate_action_plan(self, diagnosis: Dict, info_type: str) -> List[str]:
        """generateaction计划"""
        if info_type == "family":
            return diagnosis.get("suggestions", [])[:3]
        elif info_type == "personality":
            return diagnosis.get("relationship_advice", [])[:3]
        elif info_type == "relationship":
            return diagnosis.get("improvement_suggestions", [])[:3]
        elif info_type == "eq":
            return diagnosis.get("areas_for_improvement", [])[:3]
        else:
            return diagnosis.get("prevention_strategies", [])[:3]
    
    def _get_honglou_quote(self) -> Dict[str, str]:
        """get红楼梦语录"""
        quotes = [
            {"text": "满纸荒唐言,一把辛酸泪.都云作者痴,谁解其中味?", "context": "创作的艰辛"},
            {"text": "假作真时真亦假,无为有处有还无.", "context": "真假难辨"},
            {"text": "机关算尽太聪明,反误了卿卿性命.", "context": "不要过于算计"},
            {"text": "世人都晓神仙好,惟有功名忘不了!", "context": "名利的虚妄"},
            {"text": "千里搭长棚,没有不散的宴席.", "context": "聚散离合"}
        ]
        import random
        return random.choice(quotes)

def get_honglou_engine() -> HonglouInsightEngine:
    """get红楼洞察引擎"""
    return HonglouInsightEngine()

def analyze_human_relations(info: Dict[str, Any]) -> Dict[str, Any]:
    """分析人际关系"""
    engine = HonglouInsightEngine()
    return engine.analyze_relationship(info)

def diagnose_enterprise(info: Dict[str, Any]) -> Dict[str, Any]:
    """诊断企业风险"""
    engine = HonglouInsightEngine()
    return engine.diagnose_enterprise_risks(info)

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
