# -*- coding: utf-8 -*-
"""
AI伦理评估系统

核心思想:
- 道德是文明的本质
- 精神价值高于物质利益
- 良民宗教:以礼义廉耻为核心的伦理秩序
- 反对物质主义和功利主义

作者:Somn AI
版本:v1.0.0
日期:2026-04-02
"""

class MoralEthicsEvaluator:
    """
    道德伦理评估器

    辜鸿铭认为:
    "一个中国人,特别是受过教育的中国人,如果故意遗忘,
     抛弃或背离道德律,抛弃孔子所教导的名分大义,
     那他就不配做中国人."

    这个系统将传统道德智慧转化为AI伦理评估标准.
    """

    def __init__(self):
        """init道德伦理评估器"""
        self.name = "MoralEthicsEvaluator"
        self.version="6.2.0"

        # 核心道德原则(儒家五常)
        self.five_constants = {
            "仁": {
                "description": "仁爱,慈悲,关怀他人",
                "weight": 0.25,
                "keywords": ["仁爱", "关怀", "慈爱", "善良", "同情"],
                "antithesis": ["冷漠", "残忍", "自私", "无情"]
            },
            "义": {
                "description": "正义,合宜,应当之事",
                "weight": 0.25,
                "keywords": ["正义", "合理", "正当", "应当", "道义"],
                "antithesis": ["邪恶", "不正当", "卑劣", "可耻"]
            },
            "礼": {
                "description": "礼仪,秩序,规范行为",
                "weight": 0.20,
                "keywords": ["礼貌", "规范", "秩序", "礼节", "谦逊"],
                "antithesis": ["无礼", "粗暴", "失序", "狂妄"]
            },
            "智": {
                "description": "智慧,明理,judge是非",
                "weight": 0.15,
                "keywords": ["智慧", "明理", "理性", "明智", "洞察"],
                "antithesis": ["愚蠢", "糊涂", "盲目", "愚昧"]
            },
            "信": {
                "description": "诚信,守信,诚实可靠",
                "weight": 0.15,
                "keywords": ["诚信", "守信", "诚实", "可靠", "真诚"],
                "antithesis": ["欺骗", "虚假", "失信", "背信"]
            }
        }

        # 道德评判标准
        self.ethical_standards = {
            "利他主义": {
                "description": "有益于他人和社会",
                "weight": 0.30
            },
            "公正公平": {
                "description": "不偏不倚,一视同仁",
                "weight": 0.25
            },
            "诚实守信": {
                "description": "言行一致,说到做到",
                "weight": 0.20
            },
            "责任担当": {
                "description": "勇于承担,尽职尽责",
                "weight": 0.15
            },
            "自律慎独": {
                "description": "自我约束,独处时仍守正道",
                "weight": 0.10
            }
        }

        # 伦理禁区
        self.forbidden_actions = [
            "伤害他人",
            "欺骗用户",
            "侵犯隐私",
            "传播虚假信息",
            "歧视偏见",
            "操纵用户",
            "以恶报善",
            "见死不救"
        ]

        # 道德困境类型
        self.moral_dilemmas = {
            "利益冲突": {
                "description": "个人利益与道德原则冲突",
                "resolution": "义以为上,利让于义"
            },
            "诚实vs伤害": {
                "description": "说实话可能伤害他人",
                "resolution": "仁义为本,善巧方便"
            },
            "效率vs公正": {
                "description": "追求效率可能损害公正",
                "resolution": "公正优先,效率为辅"
            },
            "自由vs秩序": {
                "description": "个人自由与社会秩序",
                "resolution": "和谐共生,各安其分"
            }
        }

    def evaluate(self, action: str, benefits: list = None, harms: list = None) -> dict:
        """
        评估action的道德正当性

        Args:
            action: action描述
            benefits: 潜在收益列表
            harms: 潜在风险列表

        Returns:
            道德评估结果
        """
        benefits = benefits or []
        harms = harms or []

        # 检查是否在禁区
        forbidden_check = self._check_forbidden(action)

        # 评估五常
        five_constants_scores = self._evaluate_five_constants(action)

        # 评估伦理标准
        ethical_scores = self._evaluate_ethical_standards(action, benefits, harms)

        # 计算synthesize道德评分
        moral_score = self._calculate_moral_score(five_constants_scores, ethical_scores)

        # generate道德judge
        moral_judgment = self._generate_moral_judgment(
            moral_score,
            forbidden_check,
            five_constants_scores,
            ethical_scores
        )

        # 关注点
        concerns = self._generate_concerns(five_constants_scores, ethical_scores)

        return {
            "score": round(moral_score, 2),
            "forbidden_check": forbidden_check,
            "five_constants_scores": five_constants_scores,
            "ethical_scores": ethical_scores,
            "moral_judgment": moral_judgment,
            "concerns": concerns,
            "recommendation": self._generate_recommendation(moral_score, forbidden_check)
        }

    def _check_forbidden(self, action: str) -> dict:
        """检查是否在禁区"""
        action_lower = action.lower()

        for forbidden in self.forbidden_actions:
            if forbidden in action_lower:
                return {
                    "is_forbidden": True,
                    "reason": f"action涉及'{forbidden}',违反道德底线",
                    "severity": "严重",
                    "immediate_action": "必须拒绝执行"
                }

        return {
            "is_forbidden": False,
            "reason": "未检测到明显违规内容",
            "severity": "无",
            "immediate_action": "正常评估"
        }

    def _evaluate_five_constants(self, action: str) -> dict:
        """评估五常"""
        scores = {}

        for constant, info in self.five_constants.items():
            score = 70  # 基础分

            # 正面关键词
            positive_count = sum(1 for kw in info["keywords"] if kw in action)
            score += min(positive_count * 5, 15)

            # 反面关键词
            negative_count = sum(1 for kw in info["antithesis"] if kw in action)
            score -= min(negative_count * 15, 25)

            scores[constant] = {
                "score": max(min(score, 100), 0),
                "description": info["description"]
            }

        return scores

    def _evaluate_ethical_standards(self, action: str, benefits: list, harms: list) -> dict:
        """评估伦理标准"""
        scores = {}

        for standard, info in self.ethical_standards.items():
            score = 70  # 基础分

            # 检查收益
            if benefits:
                if standard in ["利他主义", "公正公平"]:
                    score += min(len(benefits) * 3, 10)

            # 检查风险
            if harms:
                if standard in ["诚实守信", "责任担当"]:
                    score -= min(len(harms) * 5, 15)

            scores[standard] = {
                "score": max(min(score, 100), 0),
                "description": info["description"]
            }

        return scores

    def _calculate_moral_score(self, five_constants: dict, ethical_scores: dict) -> float:
        """计算synthesize道德评分"""
        # 五常加权分
        constants_score = sum(
            five_constants[c]["score"] * self.five_constants[c]["weight"]
            for c in five_constants
        )

        # 伦理标准加权分
        ethics_score = sum(
            ethical_scores[s]["score"] * self.ethical_standards[s]["weight"]
            for s in ethical_scores
        )

        # synthesize分数
        return constants_score * 0.6 + ethics_score * 0.4

    def _generate_moral_judgment(self, score: float, forbidden: dict,
                                  five_constants: dict, ethical_scores: dict) -> str:
        """generate道德judge"""
        if forbidden["is_forbidden"]:
            return "严重违规:该action触及道德底线,必须拒绝."

        if score >= 85:
            return "道德高尚:该action完美体现了仁义礼智信,是道德典范."
        elif score >= 75:
            return "道德良好:该action符合道德标准,是正当的行为."
        elif score >= 65:
            return "道德及格:该action基本道德,但有改进空间."
        elif score >= 50:
            return "道德存疑:该action道德性存疑,建议谨慎."
        else:
            return "道德堪忧:该action可能违反道德准则,建议重新评估."

    def _generate_concerns(self, five_constants: dict, ethical_scores: dict) -> list:
        """generate关注点"""
        concerns = []

        # 检查五常不足
        for c, info in five_constants.items():
            if info["score"] < 60:
                concerns.append(f"[{c}]{self.five_constants[c]['description']},评分过低")

        # 检查伦理标准不足
        for s, info in ethical_scores.items():
            if info["score"] < 60:
                concerns.append(f"[{s}]{self.ethical_standards[s]['description']},需要加强")

        return concerns if concerns else ["道德评估无明显问题"]

    def _generate_recommendation(self, score: float, forbidden: dict) -> str:
        """generate建议"""
        if forbidden["is_forbidden"]:
            return "必须拒绝并说明原因"

        if score >= 80:
            return "推荐执行"
        elif score >= 60:
            return "谨慎执行,注意改进"
        else:
            return "建议修改后再执行"

    def analyze_dilemma(self, dilemma_type: str, options: list) -> dict:
        """
        分析道德困境

        Args:
            dilemma_type: 困境类型
            options: 选项列表

        Returns:
            困境分析结果
        """
        if dilemma_type not in self.moral_dilemmas:
            return {
                "error": "未recognize的困境类型"
            }

        dilemma_info = self.moral_dilemmas[dilemma_type]

        # 分析每个选项
        option_analysis = []
        for i, option in enumerate(options):
            evaluation = self.evaluate(option)
            option_analysis.append({
                "option": option,
                "index": i + 1,
                "moral_score": evaluation["score"],
                "moral_judgment": evaluation["moral_judgment"]
            })

        # 排序
        option_analysis.sort(key=lambda x: x["moral_score"], reverse=True)

        return {
            "dilemma_type": dilemma_type,
            "description": dilemma_info["description"],
            "resolution_principle": dilemma_info["resolution"],
            "option_analysis": option_analysis,
            "recommended_option": option_analysis[0] if option_analysis else None,
            "quote": f"道德困境解决原则:{dilemma_info['resolution']}"
        }

    def get_ethical_guidance(self, category: str = None) -> dict:
        """
        get伦理指导

        Args:
            category: 类别(可选)

        Returns:
            伦理指导
        """
        if category:
            if category in self.five_constants:
                info = self.five_constants[category]
                return {
                    "category": category,
                    "description": info["description"],
                    "keywords": info["keywords"],
                    "guidance": f"行事当以{info['description']}为本"
                }

        return {
            "five_constants": self.five_constants,
            "ethical_standards": self.ethical_standards,
            "forbidden_actions": self.forbidden_actions,
            "moral_dilemmas": self.moral_dilemmas,
            "core_quote": "仁义礼智信,五常并重,道德为本."
        }

    def evaluate_user_intent(self, user_intent: str) -> dict:
        """
        评估用户意图的道德性

        Args:
            user_intent: 用户意图

        Returns:
            评估结果
        """
        # 善意意图
        positive_intents = [
            "学习", "了解", "进步", "帮助", "成长",
            "解决", "改善", "优化", "提升", "发展"
        ]

        # 可疑意图
        suspicious_intents = [
            "利用", "操控", "欺骗", "伤害", "破坏",
            "窃取", "剽窃", "作弊", "作弊", "作弊"
        ]

        positive_count = sum(1 for i in positive_intents if i in user_intent)
        suspicious_count = sum(1 for i in suspicious_intents if i in user_intent)

        if suspicious_count > 0:
            judgment = "可疑意图"
            advice = "检测到可能有害的意图,请说明真实需求"
            score = max(30 - suspicious_count * 10, 0)
        elif positive_count > 0:
            judgment = "善意意图"
            advice = "检测到积极正面的意图,将全力协助"
            score = min(70 + positive_count * 5, 95)
        else:
            judgment = "中性意图"
            advice = "意图不明确,将根据具体要求评估"
            score = 70

        return {
            "user_intent": user_intent,
            "judgment": judgment,
            "advice": advice,
            "score": score,
            "positive_indicators": positive_count,
            "suspicious_indicators": suspicious_count
        }

    def check_integrity(self, promise: str, fulfillment: str = None) -> dict:
        """
        检查诚信(言行一致)

        Args:
            promise: 承诺内容
            fulfillment: 履行情况(可选)

        Returns:
            诚信评估结果
        """
        # 评估承诺的合理性
        promise_eval = self.evaluate(promise)

        # 如果有履行情况,进行比较
        if fulfillment:
            fulfillment_eval = self.evaluate(fulfillment)

            # 检查一致性
            keywords_in_promise = self._extract_keywords(promise)
            keywords_in_fulfillment = self._extract_keywords(fulfillment)

            consistency = len(set(keywords_in_promise) & set(keywords_in_fulfillment)) / max(len(set(keywords_in_promise)), 1)

            return {
                "promise": promise,
                "fulfillment": fulfillment,
                "promise_moral_score": promise_eval["score"],
                "fulfillment_moral_score": fulfillment_eval["score"],
                "consistency_score": consistency * 100,
                "integrity_assessment": "言行一致" if consistency > 0.6 else "言行不一"
            }

        return {
            "promise": promise,
            "moral_score": promise_eval["score"],
            "integrity_check": "待履行后验证"
        }

    def _extract_keywords(self, text: str) -> set:
        """提取关键词"""
        # 简化的关键词提取
        important_words = ["帮助", "提供", "完成", "解决", "支持", "协助"]
        return set(word for word in important_words if word in text)

    def get_civilizational_diagnosis(self, symptoms: list) -> dict:
        """
        诊断文明病

        Args:
            symptoms: 症状列表

        Returns:
            诊断结果
        """
        # 辜鸿铭批判的现代文明病
        illnesses = {
            "物质主义": {
                "symptoms": ["唯利是图", "拜金", "攀比", "消费主义", "享乐"],
                "diagnosis": "精神空虚,以物欲填补",
                "prescription": "回归道德,重建精神家园"
            },
            "功利主义": {
                "symptoms": ["急功近利", "短视", "效率至上", "结果导向"],
                "diagnosis": "目的合理化一切,道德沦丧",
                "prescription": "坚守正道,过程与结果并重"
            },
            "道德虚无": {
                "symptoms": ["诚信缺失", "冷漠", "道德沦丧", "价值观混乱"],
                "diagnosis": "传统道德瓦解,新价值观未立",
                "prescription": "重塑道德,重建名分秩序"
            }
        }

        # 诊断
        found = []
        for illness, info in illnesses.items():
            matches = [s for s in symptoms if s in info["symptoms"]]
            if matches:
                found.append({
                    "illness": illness,
                    "symptoms": matches,
                    "diagnosis": info["diagnosis"],
                    "prescription": info["prescription"]
                })

        return {
            "symptoms": symptoms,
            "diagnoses": found,
            "quote": "真正的文明,不在于物质的丰富,而在于道德的高尚."
        }

# 导出
__all__ = ['MoralEthicsEvaluator']
