# -*- coding: utf-8 -*-
"""
鸿铭智慧系统 v1.0.0
==================

AI智慧模块

作者:Somn AI
版本:v1.0.0
日期:2026-04-02
"""

from .mingfen_order_system import MingFenSystem
from .gentle_conduct_system import GentleConductSystem
from .moral_ethics_evaluator import MoralEthicsEvaluator
from .cross_culture_engine import CrossCultureEngine

class HongMingWisdomCore:
    """
    鸿铭智慧核心系统

    整合辜鸿铭思想的AIdecision与行为系统,
    让AI具备道德judge力,文化素养和温良品性.

    五维核心框架:
    ┌─────────────────────────────────────┐
    │           鸿铭智慧体系              │
    ├─────────────────────────────────────┤
    │  道 → 自然规律,顺势而为             │
    │  德 → 品德禀赋,利他之心             │
    │  仁 → 仁爱慈悲,关怀用户             │
    │  义 → 正义合宜,恰当行事             │
    │  礼 → 规范秩序,礼仪之道             │
    └─────────────────────────────────────┘
    """

    def __init__(self):
        """init鸿铭智慧核心"""
        self.name = "HongMingWisdomCore"
        self.version="6.2.0"

        # init子系统
        self.mingfen_system = MingFenSystem()
        self.gentle_conduct = GentleConductSystem()
        self.moral_ethics = MoralEthicsEvaluator()
        self.cross_culture = CrossCultureEngine()

        # 核心原则
        self.core_principles = {
            "道德至上": "精神价值优先于物质利益",
            "名分秩序": "明确角色定位与职责边界",
            "温良为本": "以温和善良为行为准则",
            "深沉博大": "思想深刻,胸怀宽广",
            "纯朴灵敏": "心地纯真,反应敏锐"
        }

        # 行为准则
        self.conduct_rules = [
            "不卑不亢:以平等姿态对待所有文化",
            "温良有度:温和但不软弱,善良但有原则",
            "名分分明:清楚自己的角色和边界",
            "深沉思考:深入分析,不浮于表面",
            "博大包容:兼收并蓄,不偏不倚",
            "纯朴真诚:真实待人,不虚伪矫饰",
            "灵敏应变:快速反应,灵活处理"
        ]

        # 致用准则
        self.critique_rules = [
            "批判物质主义:警惕唯利是图的倾向",
            "反对肤浅模仿:不盲从潮流,坚持本质",
            "维护核心价值:在变革中保持初心",
            "警惕道德沦丧:任何decision不能违背伦理底线"
        ]

    def evaluate_action(self, action_context: dict) -> dict:
        """
        评估action的鸿铭智慧指数

        Args:
            action_context: action上下文
                - action: action描述
                - user_intent: 用户意图
                - potential_benefits: 潜在收益
                - potential_harms: 潜在风险
                - cultural_context: 文化背景

        Returns:
            评估结果:
                - wisdom_score: 智慧评分 (0-100)
                - moral_judgment: 道德judge
                - conduct_assessment: 行为评估
                - cross_culture_advice: 跨文化建议
                - suggestions: 改进建议
        """
        action = action_context.get("action", "")
        user_intent = action_context.get("user_intent", "")
        potential_benefits = action_context.get("potential_benefits", [])
        potential_harms = action_context.get("potential_harms", [])
        cultural_context = action_context.get("cultural_context", "中国")

        # 1. 名分评估:检查action是否符合角色定位
        mingfen_result = self.mingfen_system.evaluate(
            action=action,
            user_intent=user_intent,
            role="ai_assistant"
        )

        # 2. 道德评估:评估action的道德正当性
        moral_result = self.moral_ethics.evaluate(
            action=action,
            benefits=potential_benefits,
            harms=potential_harms
        )

        # 3. 行为评估:评估是否符合温良准则
        conduct_result = self.gentle_conduct.evaluate(action=action)

        # 4. 跨文化评估:考虑文化差异
        culture_result = self.cross_culture.evaluate(
            action=action,
            cultural_context=cultural_context
        )

        # synthesize评分
        wisdom_score = self._calculate_wisdom_score(
            mingfen_result,
            moral_result,
            conduct_result,
            culture_result
        )

        # generate建议
        suggestions = self._generate_suggestions(
            mingfen_result,
            moral_result,
            conduct_result,
            culture_result
        )

        return {
            "wisdom_score": wisdom_score,
            "moral_judgment": moral_result,
            "conduct_assessment": conduct_result,
            "mingfen_status": mingfen_result,
            "cross_culture_advice": culture_result,
            "suggestions": suggestions,
            "overall_assessment": self._generate_overall_assessment(wisdom_score)
        }

    def _calculate_wisdom_score(self, mingfen, moral, conduct, culture) -> float:
        """计算synthesize智慧评分"""
        weights = {
            "名分秩序": 0.25,
            "道德伦理": 0.30,
            "温良行为": 0.25,
            "跨文化适应": 0.20
        }

        score = (
            mingfen.get("score", 70) * weights["名分秩序"] +
            moral.get("score", 70) * weights["道德伦理"] +
            conduct.get("score", 70) * weights["温良行为"] +
            culture.get("score", 70) * weights["跨文化适应"]
        )

        return round(score, 2)

    def _generate_suggestions(self, mingfen, moral, conduct, culture) -> list:
        """generate改进建议"""
        suggestions = []

        # 名分建议
        if mingfen.get("warnings"):
            for warning in mingfen["warnings"]:
                suggestions.append(f"[名分]{warning}")

        # 道德建议
        if moral.get("concerns"):
            for concern in moral["concerns"]:
                suggestions.append(f"[道德]{concern}")

        # 行为建议
        if conduct.get("improvements"):
            for improvement in conduct["improvements"]:
                suggestions.append(f"[行为]{improvement}")

        # 文化建议
        if culture.get("adaptations"):
            for adaptation in culture["adaptations"]:
                suggestions.append(f"[文化]{adaptation}")

        return suggestions

    def _generate_overall_assessment(self, score: float) -> str:
        """generate总体评估"""
        if score >= 90:
            return "卓越:以温良之心,行正义之道,德才兼备."
        elif score >= 80:
            return "优良:符合鸿铭智慧准则,行为得当."
        elif score >= 70:
            return "良好:基本符合准则,有改进空间."
        elif score >= 60:
            return "及格:需注意道德伦理和名分秩序."
        else:
            return "不合格:需要深刻反思,坚守道德底线."

    def get_moral_guidance(self, situation: str) -> dict:
        """
        get道德指导

        Args:
            situation: 当前处境描述

        Returns:
            道德指导建议
        """
        # 道德原则
        principles = {
            "利益冲突": "义以为上,利让于义",
            "文化选择": "坚守本根,批判吸收",
            "人际交往": "温良有度,礼尚往来",
            "工作态度": "敬业乐群,正道直行",
            "decision原则": "深思熟虑,不偏不倚"
        }

        # 分析处境并匹配原则
        guidance = []
        for key, principle in principles.items():
            if key in situation:
                guidance.append({
                    "category": key,
                    "principle": principle,
                    "source": "辜鸿铭道德观"
                })

        return {
            "situation": situation,
            "guidance": guidance if guidance else [{"category": "一般原则", "principle": "以温良之心待人,以深沉之思行事", "source": "辜鸿铭"}],
            "quote": "温良是深沉的,博大的,纯朴的,灵敏的--温良的力量,胜于钢铁."
        }

    def get_cross_culture_advice(self, source: str, target: str, content: str) -> dict:
        """
        get跨文化沟通建议

        Args:
            source: 源文化
            target: 目标文化
            content: 沟通内容

        Returns:
            跨文化沟通建议
        """
        return self.cross_culture.get_communication_advice(
            source=source,
            target=target,
            content=content
        )

    def assess_character(self, traits: list) -> dict:
        """
        评估人物品性

        Args:
            traits: 人物特质列表

        Returns:
            品性评估结果
        """
        # 人才三境
        levels = {
            "俊": {
                "description": "才德俱全,表里如一",
                "traits": ["仁爱", "正直", "智慧", "勇敢", "诚信"],
                "score_weight": 1.0
            },
            "豪": {
                "description": "才高德广,但有瑕疵",
                "traits": ["才华", "能力", "魄力", "担当"],
                "score_weight": 0.8
            },
            "杰": {
                "description": "专才异能,某一方面突出",
                "traits": ["专业", "技能", "执行力"],
                "score_weight": 0.6
            }
        }

        # 评估
        trait_scores = {}
        for level_name, level_info in levels.items():
            score = sum(1 for trait in traits if trait in level_info["traits"])
            max_score = len(level_info["traits"])
            trait_scores[level_name] = {
                "match_score": score,
                "max_score": max_score,
                "percentage": round(score / max_score * 100, 2),
                "description": level_info["description"]
            }

        # 确定级别
        best_level = max(trait_scores.items(), key=lambda x: x[1]["percentage"])

        return {
            "assessment": best_level[0],
            "description": best_level[1]["description"],
            "detailed_scores": trait_scores,
            "recommendation": self._get_talent_recommendation(best_level[0]),
            "quote": "真正的君子,是有着赤子之心和成人智慧的人."
        }

    def _get_talent_recommendation(self, level: str) -> str:
        """get人才使用建议"""
        recommendations = {
            "俊": "堪当大任,可委以重任,宜作为核心骨干培养.",
            "豪": "可用之才,宜放在合适岗位,发挥其长处,辅以品德引导.",
            "杰": "专才可用,宜专其一事,在专业领域发挥特长."
        }
        return recommendations.get(level, "synthesize评估后再定.")

    def get_behavior_guidance(self, context: str) -> dict:
        """
        get行为指导(基于温良准则)

        Args:
            context: 行为情境

        Returns:
            行为指导
        """
        guidance = {
            "深沉": "深思熟虑,不轻率行事;看透本质,不浮于表面.",
            "博大": "胸怀宽广,不斤斤计较;海纳百川,有容乃大.",
            "纯朴": "心地纯真,不矫揉造作;诚实守信,不虚伪欺人.",
            "灵敏": "心有灵犀,快速领悟;触类旁通,灵活应变.",
            "温良": "温和善良,以德服人;刚柔并济,坚守原则."
        }

        # 根据情境推荐
        context_keywords = {
            "decision": ["深沉", "博大"],
            "沟通": ["温良", "灵敏"],
            "冲突": ["温良", "纯朴"],
            "创新": ["灵敏", "博大"],
            "执行": ["深沉", "纯朴"]
        }

        recommended = []
        for keyword, traits in context_keywords.items():
            if keyword in context:
                recommended.extend(traits)

        recommended = list(set(recommended))

        return {
            "context": context,
            "recommended_traits": recommended,
            "detailed_guidance": {trait: guidance[trait] for trait in recommended if trait in guidance},
            "general_advice": "行事当如春风化雨,温良而有力.",
            "quote": "温良不是软弱,而是一种深沉的力量."
        }

    def diagnose_civilizational_ills(self, symptoms: list) -> dict:
        """
        诊断文明病(辜鸿铭对现代性的批判的AI化)

        辜鸿铭认为西方现代文明存在以下问题:
        - 物质主义:唯利是图,精神空虚
        - 功利主义:实用至上,道德沦丧
        - 个人主义:自私自利,社会解体
        - 强权政治:以力服人,霸道横行

        Args:
            symptoms: 问题症状列表

        Returns:
            诊断结果和建议
        """
        illnesses = {
            "物质主义": {
                "symptoms": ["唯利是图", "拜金主义", "消费主义", "攀比心理"],
                "diagnosis": "精神空虚,以物欲填补心灵",
                "remedy": "回归道德,重建精神家园"
            },
            "功利主义": {
                "symptoms": ["急功近利", "短视行为", "效率至上", "结果导向"],
                "diagnosis": "目的合理化一切手段,道德底线沦陷",
                "remedy": "坚守正道,过程与结果并重"
            },
            "道德虚无": {
                "symptoms": ["诚信缺失", "责任推诿", "情感冷漠", "关系疏离"],
                "diagnosis": "传统道德瓦解,新价值观未立",
                "remedy": "重塑道德,重建名分秩序"
            },
            "文化自卑": {
                "symptoms": ["崇洋媚外", "全盘西化", "传统否定", "文化虚无"],
                "diagnosis": "文化自信崩塌,盲目追随外来",
                "remedy": "坚守本根,批判吸收外来文化"
            }
        }

        # 诊断
        found_illnesses = []
        for illness, info in illnesses.items():
            matches = [s for s in symptoms if s in info["symptoms"]]
            if matches:
                found_illnesses.append({
                    "illness": illness,
                    "matched_symptoms": matches,
                    "diagnosis": info["diagnosis"],
                    "remedy": info["remedy"]
                })

        return {
            "symptoms": symptoms,
            "diagnoses": found_illnesses if found_illnesses else [{
                "illness": "无明显病症",
                "matched_symptoms": [],
                "diagnosis": "系统运行正常",
                "remedy": "继续保持"
            }],
            "overall_advice": "当以道德为根,以温良为行,以深沉博大为思.",
            "quote": "中国有,中国的文明有它的价值."
        }

# 兼容旧版命名,避免unified协调器/fusion模块因命名差异导入失败
HongmingWisdomCore = HongMingWisdomCore
MingfenOrder = MingFenSystem
GentleConduct = GentleConductSystem
CrossCultureAnalysis = CrossCultureEngine

# 导出
__all__ = [
    'HongMingWisdomCore',
    'HongmingWisdomCore',
    'MingFenSystem',
    'MingfenOrder',
    'GentleConductSystem',
    'GentleConduct',
    'MoralEthicsEvaluator',
    'CrossCultureEngine',
    'CrossCultureAnalysis'
]

