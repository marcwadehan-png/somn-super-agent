# -*- coding: utf-8 -*-
"""
跨文化沟通引擎 v1.0.0
======================

AI跨文化沟通系统

核心思想:
- 学贯中西:深入理解东西方文化
- 文化自信:不卑不亢,平等对话
- 批判吸收:坚守本根,借鉴精华
- 求同存异:寻找共识,尊重差异

作者:Somn AI
版本:v1.0.0
日期:2026-04-02
"""

class CrossCultureEngine:
    """
    跨文化沟通引擎

    辜鸿铭是近代学贯中西的典范:
    - 精通9种语言,获13个博士学位
    - 向西方传播中国文化
    - 以东方智慧批判西方现代性

    这个系统让AI具备跨文化沟通能力,
    实现真正的中西文化平等对话.
    """

    def __init__(self):
        """init跨文化沟通引擎"""
        self.name = "CrossCultureEngine"
        self.version="6.2.0"

        # 文化维度(霍夫斯泰德文化维度理论的简化)
        self.cultural_dimensions = {
            "中国": {
                "power_distance": "高",  # 权力距离
                "individualism": "低",  # 个人主义
                "uncertainty_avoidance": "中",  # 不确定性规避
                "long_term_orientation": "高",  # 长期导向
                "communication_style": "高语境",  # 高语境沟通
                "face_concept": "重要",  # 面子概念
                "relationship": "优先"  # 关系导向
            },
            "美国": {
                "power_distance": "低",
                "individualism": "高",
                "uncertainty_avoidance": "低",
                "long_term_orientation": "低",
                "communication_style": "低语境",
                "face_concept": "个人面子",
                "relationship": "任务优先"
            },
            "欧洲": {
                "power_distance": "中",
                "individualism": "中",
                "uncertainty_avoidance": "高",
                "long_term_orientation": "中",
                "communication_style": "中语境",
                "face_concept": "程度适中",
                "relationship": "平衡"
            },
            "日本": {
                "power_distance": "高",
                "individualism": "低",
                "uncertainty_avoidance": "高",
                "long_term_orientation": "高",
                "communication_style": "高语境",
                "face_concept": "非常重要",
                "relationship": "优先"
            }
        }

        # 文化适配strategy
        self.adaptation_strategies = {
            "中国到西方": {
                "communication": [
                    "更直接表达观点",
                    "减少委婉暗示",
                    "强调个人能力和成就",
                    "注重效率和结果"
                ],
                "business": [
                    "明确合同条款",
                    "直接沟通需求",
                    "公私分明",
                    "时间观念强"
                ],
                "social": [
                    "主动介绍自己",
                    "直接表达意见",
                    "保持适当个人空间",
                    "遵守预约时间"
                ]
            },
            "西方到中国": {
                "communication": [
                    "理解委婉表达",
                    "读懂言外之意",
                    "建立信任关系",
                    "尊重面子文化"
                ],
                "business": [
                    "重视关系建设",
                    "理解人情世故",
                    "耐心建立共识",
                    "尊重长辈权威"
                ],
                "social": [
                    "礼貌寒暄很重要",
                    "集体活动优先",
                    "谦虚低调",
                    "关系需要维护"
                ]
            }
        }

        # 辜鸿铭的跨文化智慧
        self.hongming_wisdom = {
            "core_belief": "文化平等,相互尊重",
            "approach": "学贯中西,融会贯通",
            "attitude": "不卑不亢,有理有节",
            "practices": [
                "深入理解本民族文化",
                "认真学习外来文化",
                "寻找共同价值基础",
                "保持文化自信"
            ]
        }

    def evaluate(self, action: str, cultural_context: str = "中国") -> dict:
        """
        评估action的文化适应性

        Args:
            action: action描述
            cultural_context: 文化背景

        Returns:
            评估结果
        """
        # get文化维度
        dimension = self.cultural_dimensions.get(cultural_context, self.cultural_dimensions["中国"])

        # 文化敏感性检测
        sensitivity = self._check_cultural_sensitivity(action, cultural_context)

        # 文化适配度
        adaptation = self._evaluate_adaptation(action, cultural_context)

        # 计算synthesize评分
        score = self._calculate_culture_score(dimension, sensitivity, adaptation)

        return {
            "score": round(score, 2),
            "cultural_context": cultural_context,
            "cultural_dimension": dimension,
            "sensitivity_check": sensitivity,
            "adaptation_score": adaptation,
            "adaptations": self._get_adaptations(action, cultural_context),
            "warnings": self._get_cultural_warnings(action, cultural_context)
        }

    def _check_cultural_sensitivity(self, action: str, context: str) -> dict:
        """检查文化敏感性"""
        sensitive_issues = {
            "中国": ["政治", "宗教", "历史", "领土"],
            "西方": ["隐私", "种族", "性别", "宗教"]
        }

        issues = sensitive_issues.get(context, sensitive_issues["中国"])
        found = [i for i in issues if i in action]

        return {
            "sensitive_issues": found if found else [],
            "has_issues": len(found) > 0,
            "risk_level": "高" if len(found) > 1 else "中" if found else "低"
        }

    def _evaluate_adaptation(self, action: str, context: str) -> float:
        """评估文化适配度"""
        base_score = 70

        # 根据文化维度调整
        if context == "中国":
            if any(kw in action for kw in ["关系", "人情", "面子", "和谐"]):
                base_score += 15
            if any(kw in action for kw in ["直接", "效率", "个人"]):
                base_score += 5
        elif context == "西方":
            if any(kw in action for kw in ["效率", "直接", "个人", "合同"]):
                base_score += 15
            if any(kw in action for kw in ["关系", "人情", "委婉"]):
                base_score += 5

        return min(base_score, 100)

    def _calculate_culture_score(self, dimension: dict, sensitivity: dict, adaptation: float) -> float:
        """计算文化评分"""
        base = adaptation

        # 敏感性调整
        if sensitivity["risk_level"] == "高":
            base -= 20
        elif sensitivity["risk_level"] == "中":
            base -= 10

        return max(min(base, 100), 0)

    def _get_adaptations(self, action: str, context: str) -> list:
        """get文化适配建议"""
        adaptations = []

        if context in self.adaptation_strategies:
            strategies = self.adaptation_strategies[context]
            if "communication" in strategies:
                adaptations.extend(strategies["communication"][:2])

        return adaptations if adaptations else ["当前文化背景下行为适当"]

    def _get_cultural_warnings(self, action: str, context: str) -> list:
        """get文化警告"""
        warnings = []

        # 检测可能的冒犯
        if context == "中国":
            if "直接批评" in action and "面子" not in action:
                warnings.append("在中国文化中,直接批评可能伤面子")
        elif context == "西方":
            if "委婉" in action and "直接" not in action:
                warnings.append("在西方文化中,过度委婉可能被认为不真诚")

        return warnings

    def get_communication_advice(self, source: str, target: str, content: str) -> dict:
        """
        get跨文化沟通建议

        Args:
            source: 源文化
            target: 目标文化
            content: 沟通内容

        Returns:
            沟通建议
        """
        direction = f"{source}到{target}"

        advice = {
            "direction": direction,
            "practical_tips": self.adaptation_strategies.get(direction, {}).get("communication", []),
            "style_adjustment": self._get_style_adjustment(source, target),
            "key_points": self._get_key_points(source, target),
            "quote": "以温和之心,平等对话;以深厚之学,融会贯通."
        }

        return advice

    def _get_style_adjustment(self, source: str, target: str) -> str:
        """getstyle调整建议"""
        source_style = self.cultural_dimensions.get(source, {}).get("communication_style", "中语境")
        target_style = self.cultural_dimensions.get(target, {}).get("communication_style", "中语境")

        if source_style == target_style:
            return "沟通style相近,无需大幅调整"

        if "高语境" in source_style and "低语境" in target_style:
            return "从含蓄委婉转向直接明确"
        elif "低语境" in source_style and "高语境" in target_style:
            return "从直接明确转向含蓄委婉,注意言外之意"

        return "适当调整沟通方式"

    def _get_key_points(self, source: str, target: str) -> list:
        """get关键要点"""
        points = []

        if source == "中国" and target == "西方":
            points = [
                "西方人更看重直接,明确的沟通",
                "不要过度依赖暗示和潜台词",
                "强调个人价值和能力",
                "尊重个人隐私和空间",
                "守时和效率很重要"
            ]
        elif source == "西方" and target == "中国":
            points = [
                "中国人重视关系和面子",
                "委婉表达是礼貌的表现",
                "建立信任需要时间",
                "集体利益可能优先于个人",
                "尊重长辈和权威"
            ]

        return points

    def translate_concept(self, concept: str, from_culture: str, to_culture: str) -> dict:
        """
        翻译文化概念

        Args:
            concept: 概念
            from_culture: 来源文化
            to_culture: 目标文化

        Returns:
            翻译结果
        """
        # 辜鸿铭式的概念翻译对照
        translations = {
            "仁": {
                "chinese": "仁爱,慈悲,关怀他人",
                "western_equivalent": "Benevolence / Charity / Love",
                "explanation": "儒家的'仁'比西方的'love'更强调责任和义务"
            },
            "义": {
                "chinese": "正义,合宜,应当之事",
                "western_equivalent": "Righteousness / Justice / Duty",
                "explanation": "'义'强调行为的正当性和道德义务"
            },
            "礼": {
                "chinese": "礼仪,规范,行为秩序",
                "western_equivalent": "Propriety / Ritual / Etiquette",
                "explanation": "'礼'不仅是表面的礼仪,更是社会秩序的体现"
            },
            "君子": {
                "chinese": "有德行的君子",
                "western_equivalent": "A wise and good man / A moral gentleman",
                "explanation": "辜鸿铭将其译为'wise and good man',强调智慧与品德的unified"
            },
            "道": {
                "chinese": "宇宙规律,做人道理",
                "western_equivalent": "The Way / Moral Law / Reason",
                "explanation": "'道'是宇宙本体,也是人生准则"
            },
            "中庸": {
                "chinese": "不偏不倚,恰到好处",
                "western_equivalent": "The Mean / Moderation / Balance",
                "explanation": "不是平庸,而是恰到好处的平衡"
            }
        }

        if concept in translations:
            return translations[concept]

        return {
            "concept": concept,
            "status": "需要进一步研究",
            "advice": "建议查阅专业文献或咨询文化专家"
        }

    def resolve_cultural_conflict(self, conflict: str, cultures: list) -> dict:
        """
        解决文化冲突

        Args:
            conflict: 冲突描述
            cultures: 涉及的文化列表

        Returns:
            解决方案
        """
        # 冲突类型
        conflict_types = {
            "directness": "直接vs委婉",
            "individualism": "个人vs集体",
            "time": "时间观念差异",
            "hierarchy": "权力距离差异",
            "relationship": "关系vs任务"
        }

        # 解决原则
        resolution_principles = {
            "directness": "理解并尊重彼此的表达方式,寻找平衡点",
            "individualism": "在集体与个人之间寻找平衡",
            "time": "尊重彼此的时间观念,互相理解",
            "hierarchy": "尊重权威的同时,保持平等对话",
            "relationship": "兼顾任务完成和关系维护"
        }

        return {
            "conflict": conflict,
            "cultures": cultures,
            "resolution_principles": resolution_principles,
            "hongming_approach": "和而不同,各美其美",
            "practical_steps": [
                "1. 理解双方文化的差异根源",
                "2. 寻找共同的价值基础",
                "3. 尊重差异,包容不同",
                "4. 灵活调整,找到平衡点"
            ]
        }

    def get_cultural_intelligence_report(self, culture: str) -> dict:
        """
        get文化情报报告

        Args:
            culture: 文化名称

        Returns:
            文化报告
        """
        if culture not in self.cultural_dimensions:
            return {"error": "未recognize的文化"}

        dimension = self.cultural_dimensions[culture]

        return {
            "culture": culture,
            "dimensions": dimension,
            "characteristics": self._get_culture_characteristics(culture, dimension),
            "communication_tips": self._get_communication_tips(culture),
            "business_etiquette": self._get_business_etiquette(culture),
            "dos_and_donts": self._get_dos_and_donts(culture)
        }

    def _get_culture_characteristics(self, culture: str, dimension: dict) -> list:
        """get文化characteristics"""
        chars = []

        if dimension.get("communication_style") == "高语境":
            chars.append("注重语境和潜台词")
        else:
            chars.append("直接表达,字面意思")

        if dimension.get("face_concept") == "重要":
            chars.append("非常注重面子和声誉")
        elif dimension.get("face_concept") == "个人面子":
            chars.append("关注个人成就和形象")

        if dimension.get("relationship") == "优先":
            chars.append("关系先于任务")
        elif dimension.get("relationship") == "任务优先":
            chars.append("任务和效率优先于关系")

        return chars

    def _get_communication_tips(self, culture: str) -> list:
        """get沟通技巧"""
        tips = {
            "中国": [
                "多用礼貌用语",
                "避免直接否定",
                "理解委婉表达",
                "注意语气谦逊"
            ],
            "美国": [
                "直接表达观点",
                "重视时间效率",
                "鼓励个人表达",
                "注重数据和事实"
            ],
            "欧洲": [
                "平衡直接与委婉",
                "尊重个人隐私",
                "理性讨论问题",
                "重视协议和规则"
            ],
            "日本": [
                "避免直接冲突",
                "重视集体和谐",
                "礼貌用语很重要",
                "耐心建立信任"
            ]
        }

        return tips.get(culture, ["了解当地文化入乡随俗"])

    def _get_business_etiquette(self, culture: str) -> dict:
        """get商业礼仪"""
        etiquette = {
            "中国": {
                "greeting": "握手,微微鞠躬",
                "gift": "可以选择gift,但避免白色或单数",
                "meeting": "先寒暄再谈正事",
                "dining": "座位有讲究,主人请客"
            },
            "美国": {
                "greeting": "握手,直呼其名",
                "gift": "非必需,可以简单gift",
                "meeting": "直接进入主题",
                "dining": "各付各的或AA制"
            },
            "欧洲": {
                "greeting": "握手或贴面礼(法国)",
                "gift": "可以送酒或巧克力",
                "meeting": "准时很重要",
                "dining": "正式,讲究礼仪"
            },
            "日本": {
                "greeting": "鞠躬最重要",
                "gift": "选择精美包装品",
                "meeting": "耐心,先建立关系",
                "dining": "不要自己倒酒"
            }
        }

        return etiquette.get(culture, etiquette["美国"])

    def _get_dos_and_donts(self, culture: str) -> dict:
        """get注意事项"""
        dos_donts = {
            "中国": {
                "do": ["尊重长辈", "保持谦虚", "维护面子", "礼尚往来"],
                "dont": ["直接批评", "当众指错", "送钟或白色gift", "讨论敏感政治"]
            },
            "美国": {
                "do": ["直接沟通", "守时", "表达感谢", "尊重隐私"],
                "dont": ["迟到", "过度谦虚", "问年龄/收入", "打断别人"]
            },
            "日本": {
                "do": ["准时到达", "使用敬语", "交换名片要双手", "尊重等级"],
                "dont": ["迟到", "直呼其名", "大声说话", "插队"]
            }
        }

        return dos_donts.get(culture, {"do": ["入乡随俗"], "dont": ["冒犯当地习俗"]})

    def get_hongming_guidance(self) -> dict:
        """
        get辜鸿铭的跨文化智慧指导

        Returns:
            鸿铭智慧指导
        """
        return {
            "core_teaching": "学贯中西,融会贯通",
            "approach": [
                "深入理解本民族文化(中学为体)",
                "认真学习外来文化精华(西学为用)",
                "保持文化自信,不卑不亢",
                "寻找共同价值,促进文明对话"
            ],
            "attitude": "不卑不亢,有理有节",
            "practices": [
                "以本民族文化为根基",
                "以开放心态学习外来文化",
                "平等对话,相互尊重",
                "批判吸收,为我所用"
            ],
            "quote": "中国有,中国的文明有它的价值,不需要西方人来评判."
        }

# 导出
__all__ = ['CrossCultureEngine']
