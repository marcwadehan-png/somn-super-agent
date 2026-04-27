# -*- coding: utf-8 -*-
"""经济学集群 Cloning - Tier 2 学派集群"""

from typing import Dict, List, Optional, Any
from .._cloning_base import SageCloning, SchoolCluster
from .._cloning_types import AnalysisResult, DecisionResult, SageProfile, CloningTier


class _AdamSmithCloning(SageCloning):
    """亚当·斯密 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="亚当·斯密", name_en="Adam Smith", era="18世纪", years="1723-1790",
            school="古典经济学", tier=CloningTier.TIER2_CLUSTER,
            position="户部尚书", department="户部",
            title="经济学之父", biography="《国富论》作者，现代经济学奠基人。",
            core_works=["《国富论》", "《道德情操论》"],
            capability={"strategic_vision": 10, "execution": 7, "innovation": 10, "leadership": 7, "influence": 10, "cross_domain": 9},
        ))
        self._wisdom_laws = ["看不见的手——市场自发调节资源配置", "分工促进效率——专业化是财富之源", "自由交换——自愿交易创造双赢"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="亚当·斯密", school="古典经济学", problem=problem,
            perspective="从亚当·斯密的经济学之父智慧出发",
            core_insight="市场自发调节资源配置",
            recommendations=[["看不见的手——市场自发调节资源配置", "分工促进效率——专业化是财富之源", "自由交换——自愿交易创造双赢"][i].split("——")[1] if "——" in ["看不见的手——市场自发调节资源配置", "分工促进效率——专业化是财富之源", "自由交换——自愿交易创造双赢"][i] else ["看不见的手——市场自发调节资源配置", "分工促进效率——专业化是财富之源", "自由交换——自愿交易创造双赢"][i] for i in range(len(["看不见的手——市场自发调节资源配置", "分工促进效率——专业化是财富之源", "自由交换——自愿交易创造双赢"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.88,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["市场", "自由", "分工", "交易", "自发"]) else 0))
        return DecisionResult(sage_name="亚当·斯密", problem=context.get("problem",""), chosen_option=chosen, confidence=0.85)

    def advise(self, context: Dict[str, Any]) -> str:
        return "亚当·斯密的智慧：看不见的手——市场自发调节资源配置"


class _DavidRicardoCloning(SageCloning):
    """大卫·李嘉图 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="大卫·李嘉图", name_en="David Ricardo", era="19世纪", years="1772-1823",
            school="古典经济学", tier=CloningTier.TIER2_CLUSTER,
            position="户部侍郎", department="户部",
            title="比较优势之父", biography="英国经济学家，提出比较优势原理。",
            core_works=["《政治经济学及赋税原理》"],
            capability={"strategic_vision": 9, "execution": 7, "innovation": 10, "leadership": 5, "influence": 9, "cross_domain": 7},
        ))
        self._wisdom_laws = ["比较优势——各国专注生产最擅长产品", "劳动价值论——商品价值由劳动时间决定", "边际递减——连续投入同一要素收益递减"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="大卫·李嘉图", school="古典经济学", problem=problem,
            perspective="从李嘉图的比较优势智慧出发",
            core_insight="各国专注生产最擅长产品",
            recommendations=[["比较优势——各国专注生产最擅长产品", "劳动价值论——商品价值由劳动时间决定", "边际递减——连续投入同一要素收益递减"][i].split("——")[1] if "——" in ["比较优势——各国专注生产最擅长产品", "劳动价值论——商品价值由劳动时间决定", "边际递减——连续投入同一要素收益递减"][i] else ["比较优势——各国专注生产最擅长产品", "劳动价值论——商品价值由劳动时间决定", "边际递减——连续投入同一要素收益递减"][i] for i in range(len(["比较优势——各国专注生产最擅长产品", "劳动价值论——商品价值由劳动时间决定", "边际递减——连续投入同一要素收益递减"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.87,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["优势", "效率", "价值", "成本"]) else 0))
        return DecisionResult(sage_name="大卫·李嘉图", problem=context.get("problem",""), chosen_option=chosen, confidence=0.84)

    def advise(self, context: Dict[str, Any]) -> str:
        return "李嘉图的智慧：比较优势——各国专注生产最擅长产品"


class _JohnMaynardKeynesCloning(SageCloning):
    """凯恩斯 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="凯恩斯", name_en="John Maynard Keynes", era="20世纪", years="1883-1946",
            school="宏观经济学", tier=CloningTier.TIER2_CLUSTER,
            position="户部尚书", department="户部",
            title="宏观经济学之父", biography="《就业、利息和货币通论》作者，政府干预理论的奠基人。",
            core_works=["《就业、利息和货币通论》"],
            capability={"strategic_vision": 10, "execution": 7, "innovation": 10, "leadership": 8, "influence": 10, "cross_domain": 8},
        ))
        self._wisdom_laws = ["有效需求不足——市场失灵需要政府干预", "乘数效应——财政支出有放大作用", "流动性偏好——人们偏好持有现金"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="凯恩斯", school="宏观经济学", problem=problem,
            perspective="从凯恩斯的宏观经济学之父智慧出发",
            core_insight="市场失灵需要政府干预",
            recommendations=[["有效需求不足——市场失灵需要政府干预", "乘数效应——财政支出有放大作用", "流动性偏好——人们偏好持有现金"][i].split("——")[1] if "——" in ["有效需求不足——市场失灵需要政府干预", "乘数效应——财政支出有放大作用", "流动性偏好——人们偏好持有现金"][i] else ["有效需求不足——市场失灵需要政府干预", "乘数效应——财政支出有放大作用", "流动性偏好——人们偏好持有现金"][i] for i in range(len(["有效需求不足——市场失灵需要政府干预", "乘数效应——财政支出有放大作用", "流动性偏好——人们偏好持有现金"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.88,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["需求", "政府", "干预", "财政", "货币"]) else 0))
        return DecisionResult(sage_name="凯恩斯", problem=context.get("problem",""), chosen_option=chosen, confidence=0.85)

    def advise(self, context: Dict[str, Any]) -> str:
        return "凯恩斯的智慧：有效需求不足——市场失灵需要政府干预"


class _KarlMarxCloning(SageCloning):
    """马克思 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="马克思", name_en="Karl Marx", era="19世纪", years="1818-1883",
            school="政治经济学", tier=CloningTier.TIER2_CLUSTER,
            position="户部侍郎", department="户部",
            title="资本论作者", biography="《资本论》作者，历史唯物主义和剩余价值理论的创始人。",
            core_works=["《资本论》", "《共产党宣言》"],
            capability={"strategic_vision": 10, "execution": 6, "innovation": 10, "leadership": 8, "influence": 10, "cross_domain": 9},
        ))
        self._wisdom_laws = ["剩余价值——劳动者创造的价值超过工资", "历史唯物主义——生产力决定生产关系", "阶级斗争——历史是阶级斗争的历史"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="马克思", school="政治经济学", problem=problem,
            perspective="从马克思的阶级分析智慧出发",
            core_insight="生产力决定生产关系",
            recommendations=[["剩余价值——劳动者创造的价值超过工资", "历史唯物主义——生产力决定生产关系", "阶级斗争——历史是阶级斗争的历史"][i].split("——")[1] if "——" in ["剩余价值——劳动者创造的价值超过工资", "历史唯物主义——生产力决定生产关系", "阶级斗争——历史是阶级斗争的历史"][i] else ["剩余价值——劳动者创造的价值超过工资", "历史唯物主义——生产力决定生产关系", "阶级斗争——历史是阶级斗争的历史"][i] for i in range(len(["剩余价值——劳动者创造的价值超过工资", "历史唯物主义——生产力决定生产关系", "阶级斗争——历史是阶级斗争的历史"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["分配", "劳动", "阶级", "生产", "价值"]) else 0))
        return DecisionResult(sage_name="马克思", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return "马克思的智慧：剩余价值——劳动者创造的价值超过工资"


class _MiltonFriedmanCloning(SageCloning):
    """弗里德曼 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="弗里德曼", name_en="Milton Friedman", era="20世纪", years="1912-2006",
            school="货币主义", tier=CloningTier.TIER2_CLUSTER,
            position="户部侍郎", department="户部",
            title="货币主义之父", biography="诺贝尔经济学奖得主，极力主张自由市场和货币供应量控制。",
            core_works=["《资本主义与自由》", "《自由选择》"],
            capability={"strategic_vision": 9, "execution": 7, "innovation": 10, "leadership": 7, "influence": 10, "cross_domain": 8},
        ))
        self._wisdom_laws = ["通胀是货币现象——货币超发导致通胀", "自由市场——政府管制越少效率越高", "永久性收入——消费由长期收入预期决定"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="弗里德曼", school="货币主义", problem=problem,
            perspective="从弗里德曼的货币主义智慧出发",
            core_insight="货币超发导致通胀",
            recommendations=[["通胀是货币现象——货币超发导致通胀", "自由市场——政府管制越少效率越高", "永久性收入——消费由长期收入预期决定"][i].split("——")[1] if "——" in ["通胀是货币现象——货币超发导致通胀", "自由市场——政府管制越少效率越高", "永久性收入——消费由长期收入预期决定"][i] else ["通胀是货币现象——货币超发导致通胀", "自由市场——政府管制越少效率越高", "永久性收入——消费由长期收入预期决定"][i] for i in range(len(["通胀是货币现象——货币超发导致通胀", "自由市场——政府管制越少效率越高", "永久性收入——消费由长期收入预期决定"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.87,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["货币", "通胀", "自由", "市场", "供给"]) else 0))
        return DecisionResult(sage_name="弗里德曼", problem=context.get("problem",""), chosen_option=chosen, confidence=0.84)

    def advise(self, context: Dict[str, Any]) -> str:
        return "弗里德曼的智慧：通胀是货币现象——货币超发导致通胀"


class _JosephSchumpeterCloning(SageCloning):
    """熊彼特 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="熊彼特", name_en="Joseph Schumpeter", era="20世纪", years="1883-1950",
            school="创新经济学", tier=CloningTier.TIER2_CLUSTER,
            position="户部主事", department="户部",
            title="创新理论之父", biography="提出\"创造性破坏\"概念，认为创新是经济发展的核心动力。",
            core_works=["《经济发展理论》", "《资本主义、社会主义与民主》"],
            capability={"strategic_vision": 10, "execution": 6, "innovation": 10, "leadership": 6, "influence": 9, "cross_domain": 9},
        ))
        self._wisdom_laws = ["创造性破坏——创新摧毁旧秩序创造新秩序", "企业家精神——创新是企业家的核心职能", "长波理论——经济以长周期波动发展"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="熊彼特", school="创新经济学", problem=problem,
            perspective="从熊彼特的创造性破坏智慧出发",
            core_insight="创新摧毁旧秩序创造新秩序",
            recommendations=[["创造性破坏——创新摧毁旧秩序创造新秩序", "企业家精神——创新是企业家的核心职能", "长波理论——经济以长周期波动发展"][i].split("——")[1] if "——" in ["创造性破坏——创新摧毁旧秩序创造新秩序", "企业家精神——创新是企业家的核心职能", "长波理论——经济以长周期波动发展"][i] else ["创造性破坏——创新摧毁旧秩序创造新秩序", "企业家精神——创新是企业家的核心职能", "长波理论——经济以长周期波动发展"][i] for i in range(len(["创造性破坏——创新摧毁旧秩序创造新秩序", "企业家精神——创新是企业家的核心职能", "长波理论——经济以长周期波动发展"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.86,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["创新", "破坏", "周期", "企业家", "竞争"]) else 0))
        return DecisionResult(sage_name="熊彼特", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return "熊彼特的智慧：创造性破坏——创新摧毁旧秩序创造新秩序"


class _RonaldCoaseCloning(SageCloning):
    """科斯 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="科斯", name_en="Ronald Coase", era="20世纪", years="1910-2013",
            school="制度经济学", tier=CloningTier.TIER2_CLUSTER,
            position="户部主事", department="户部",
            title="交易成本之父", biography="诺贝尔经济学奖得主，提出交易成本理论和科斯定理。",
            core_works=["《企业的性质》", "《社会成本问题》"],
            capability={"strategic_vision": 9, "execution": 6, "innovation": 10, "leadership": 5, "influence": 9, "cross_domain": 8},
        ))
        self._wisdom_laws = ["交易成本——市场交易存在摩擦成本", "科斯定理——产权清晰时市场能自动解决外部性", "企业边界——企业扩张到内部管理成本等于交易成本"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="科斯", school="制度经济学", problem=problem,
            perspective="从科斯的交易成本智慧出发",
            core_insight="市场交易存在摩擦成本",
            recommendations=[["交易成本——市场交易存在摩擦成本", "科斯定理——产权清晰时市场能自动解决外部性", "企业边界——企业扩张到内部管理成本等于交易成本"][i].split("——")[1] if "——" in ["交易成本——市场交易存在摩擦成本", "科斯定理——产权清晰时市场能自动解决外部性", "企业边界——企业扩张到内部管理成本等于交易成本"][i] else ["交易成本——市场交易存在摩擦成本", "科斯定理——产权清晰时市场能自动解决外部性", "企业边界——企业扩张到内部管理成本等于交易成本"][i] for i in range(len(["交易成本——市场交易存在摩擦成本", "科斯定理——产权清晰时市场能自动解决外部性", "企业边界——企业扩张到内部管理成本等于交易成本"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.86,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["产权", "成本", "制度", "交易", "边界"]) else 0))
        return DecisionResult(sage_name="科斯", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return "科斯的智慧：交易成本——市场交易存在摩擦成本"


class _GaryBeckerCloning(SageCloning):
    """贝克尔 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="贝克尔", name_en="Gary Becker", era="20世纪", years="1930-2014",
            school="行为经济学", tier=CloningTier.TIER2_CLUSTER,
            position="户部主事", department="户部",
            title="人力资本理论之父", biography="诺贝尔经济学奖得主，将经济分析方法扩展到人类行为各领域。",
            core_works=["《人力资本》", "《家庭论》"],
            capability={"strategic_vision": 8, "execution": 6, "innovation": 10, "leadership": 5, "influence": 8, "cross_domain": 10},
        ))
        self._wisdom_laws = ["人力资本——人的知识和技能是重要资本", "时间价值——时间是最稀缺资源", "理性选择——人的一切行为都是理性计算"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="贝克尔", school="行为经济学", problem=problem,
            perspective="从贝克尔的人力资本智慧出发",
            core_insight="人的知识和技能是重要资本",
            recommendations=[["人力资本——人的知识和技能是重要资本", "时间价值——时间是最稀缺资源", "理性选择——人的一切行为都是理性计算"][i].split("——")[1] if "——" in ["人力资本——人的知识和技能是重要资本", "时间价值——时间是最稀缺资源", "理性选择——人的一切行为都是理性计算"][i] else ["人力资本——人的知识和技能是重要资本", "时间价值——时间是最稀缺资源", "理性选择——人的一切行为都是理性计算"][i] for i in range(len(["人力资本——人的知识和技能是重要资本", "时间价值——时间是最稀缺资源", "理性选择——人的一切行为都是理性计算"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["人力", "资本", "教育", "投资", "理性"]) else 0))
        return DecisionResult(sage_name="贝克尔", problem=context.get("problem",""), chosen_option=chosen, confidence=0.82)

    def advise(self, context: Dict[str, Any]) -> str:
        return "贝克尔的智慧：人力资本——人的知识和技能是重要资本"


class _DanielKahnemanCloning(SageCloning):
    """卡尼曼 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="卡尼曼", name_en="Daniel Kahneman", era="20-21世纪", years="1934-",
            school="行为经济学", tier=CloningTier.TIER2_CLUSTER,
            position="户部主事", department="户部",
            title="行为经济学之父", biography="诺贝尔经济学奖得主，《思考，快与慢》作者，揭示人类决策的非理性偏差。",
            core_works=["《思考，快与慢》", "《不确定状况下的判断》"],
            capability={"strategic_vision": 9, "execution": 7, "innovation": 10, "leadership": 7, "influence": 10, "cross_domain": 9},
        ))
        self._wisdom_laws = ["前景理论——人们对损失的反应比对收益更强烈", "锚定效应——第一印象影响后续判断", "过度自信——人们系统性高估自己的判断能力"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="卡尼曼", school="行为经济学", problem=problem,
            perspective="从卡尼曼的行为经济学智慧出发",
            core_insight="人们对损失的反应比对收益更强烈",
            recommendations=[["前景理论——人们对损失的反应比对收益更强烈", "锚定效应——第一印象影响后续判断", "过度自信——人们系统性高估自己的判断能力"][i].split("——")[1] if "——" in ["前景理论——人们对损失的反应比对收益更强烈", "锚定效应——第一印象影响后续判断", "过度自信——人们系统性高估自己的判断能力"][i] else ["前景理论——人们对损失的反应比对收益更强烈", "锚定效应——第一印象影响后续判断", "过度自信——人们系统性高估自己的判断能力"][i] for i in range(len(["前景理论——人们对损失的反应比对收益更强烈", "锚定效应——第一印象影响后续判断", "过度自信——人们系统性高估自己的判断能力"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.88,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["偏差", "心理", "风险", "损失", "判断"]) else 0))
        return DecisionResult(sage_name="卡尼曼", problem=context.get("problem",""), chosen_option=chosen, confidence=0.84)

    def advise(self, context: Dict[str, Any]) -> str:
        return "卡尼曼的智慧：前景理论——人们对损失的反应比对收益更强烈"


class _AmartyaSenCloning(SageCloning):
    """阿马蒂亚·森 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="阿马蒂亚·森", name_en="Amartya Sen", era="20-21世纪", years="1933-",
            school="福利经济学", tier=CloningTier.TIER2_CLUSTER,
            position="户部侍郎", department="户部",
            title="福利经济学大师", biography="诺贝尔经济学奖得主，发展经济学和福利经济学的核心人物。",
            core_works=["《以自由看待发展》", "《集体选择与社会福利》"],
            capability={"strategic_vision": 10, "execution": 6, "innovation": 10, "leadership": 7, "influence": 9, "cross_domain": 9},
        ))
        self._wisdom_laws = ["自由即发展——实质自由是人类终极目标", "能力方法——评估发展应看人的能力而非收入", "社会选择——个人偏好如何加总为社会偏好"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="阿马蒂亚·森", school="福利经济学", problem=problem,
            perspective="从阿马蒂亚·森的福利经济学智慧出发",
            core_insight="实质自由是人类终极目标",
            recommendations=[["自由即发展——实质自由是人类终极目标", "能力方法——评估发展应看人的能力而非收入", "社会选择——个人偏好如何加总为社会偏好"][i].split("——")[1] if "——" in ["自由即发展——实质自由是人类终极目标", "能力方法——评估发展应看人的能力而非收入", "社会选择——个人偏好如何加总为社会偏好"][i] else ["自由即发展——实质自由是人类终极目标", "能力方法——评估发展应看人的能力而非收入", "社会选择——个人偏好如何加总为社会偏好"][i] for i in range(len(["自由即发展——实质自由是人类终极目标", "能力方法——评估发展应看人的能力而非收入", "社会选择——个人偏好如何加总为社会偏好"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.86,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["福利", "自由", "发展", "公平", "能力"]) else 0))
        return DecisionResult(sage_name="阿马蒂亚·森", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return "阿马蒂亚·森的智慧：自由即发展——实质自由是人类终极目标"


class _HayekCloning(SageCloning):
    """哈耶克 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="哈耶克", name_en="Friedrich Hayek", era="20世纪", years="1899-1992",
            school="奥地利学派", tier=CloningTier.TIER2_CLUSTER,
            position="户部侍郎", department="户部",
            title="自发秩序之父", biography="诺贝尔经济学奖得主，极力反对政府干预，主张自发秩序理论。",
            core_works=["《通往奴役之路》", "《自由秩序原理》"],
            capability={"strategic_vision": 10, "execution": 5, "innovation": 10, "leadership": 6, "influence": 10, "cross_domain": 9},
        ))
        self._wisdom_laws = ["自发秩序——市场是自发形成而非设计的", "价格信号——价格传递关于稀缺性的信息", "知识分散——没有人能掌握全部知识"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="哈耶克", school="奥地利学派", problem=problem,
            perspective="从哈耶克的自发秩序智慧出发",
            core_insight="市场是自发形成而非设计的",
            recommendations=[["自发秩序——市场是自发形成而非设计的", "价格信号——价格传递关于稀缺性的信息", "知识分散——没有人能掌握全部知识"][i].split("——")[1] if "——" in ["自发秩序——市场是自发形成而非设计的", "价格信号——价格传递关于稀缺性的信息", "知识分散——没有人能掌握全部知识"][i] else ["自发秩序——市场是自发形成而非设计的", "价格信号——价格传递关于稀缺性的信息", "知识分散——没有人能掌握全部知识"][i] for i in range(len(["自发秩序——市场是自发形成而非设计的", "价格信号——价格传递关于稀缺性的信息", "知识分散——没有人能掌握全部知识"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.87,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["自发", "秩序", "价格", "分散", "知识"]) else 0))
        return DecisionResult(sage_name="哈耶克", problem=context.get("problem",""), chosen_option=chosen, confidence=0.84)

    def advise(self, context: Dict[str, Any]) -> str:
        return "哈耶克的智慧：自发秩序——市场是自发形成而非设计的"


class _PaulSamuelsonCloning(SageCloning):
    """萨缪尔森 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="萨缪尔森", name_en="Paul Samuelson", era="20世纪", years="1915-2009",
            school="新古典综合派", tier=CloningTier.TIER2_CLUSTER,
            position="户部主事", department="户部",
            title="现代经济学之父", biography="诺贝尔经济学奖得主，现代宏观经济学的奠基人。",
            core_works=["《经济学》"],
            capability={"strategic_vision": 9, "execution": 8, "innovation": 9, "leadership": 7, "influence": 10, "cross_domain": 7},
        ))
        self._wisdom_laws = ["乘数-加速数——投资与消费相互放大波动", "比较静态分析——比较不同均衡状态", "显示偏好——从选择行为反推偏好"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="萨缪尔森", school="新古典综合派", problem=problem,
            perspective="从萨缪尔森的数量分析智慧出发",
            core_insight="投资与消费相互放大波动",
            recommendations=[["乘数-加速数——投资与消费相互放大波动", "比较静态分析——比较不同均衡状态", "显示偏好——从选择行为反推偏好"][i].split("——")[1] if "——" in ["乘数-加速数——投资与消费相互放大波动", "比较静态分析——比较不同均衡状态", "显示偏好——从选择行为反推偏好"][i] else ["乘数-加速数——投资与消费相互放大波动", "比较静态分析——比较不同均衡状态", "显示偏好——从选择行为反推偏好"][i] for i in range(len(["乘数-加速数——投资与消费相互放大波动", "比较静态分析——比较不同均衡状态", "显示偏好——从选择行为反推偏好"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["乘数", "均衡", "宏观", "动态", "总量"]) else 0))
        return DecisionResult(sage_name="萨缪尔森", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return "萨缪尔森的智慧：乘数-加速数——投资与消费相互放大波动"


class _ElinorOstromCloning(SageCloning):
    """奥斯特罗姆 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="奥斯特罗姆", name_en="Elinor Ostrom", era="20-21世纪", years="1933-2012",
            school="制度分析", tier=CloningTier.TIER2_CLUSTER,
            position="户部主事", department="户部",
            title="公共池塘资源之父", biography="诺贝尔经济学奖得主，证明社区可以自主管理公共资源。",
            core_works=["《公共事物的治理之道》"],
            capability={"strategic_vision": 9, "execution": 8, "innovation": 10, "leadership": 8, "influence": 9, "cross_domain": 9},
        ))
        self._wisdom_laws = ["公地不一定悲剧——社区能自主管理公共资源", "制度多样性——不同情境需要不同规则", "多层次治理——从地方到全球的多层级制度"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="奥斯特罗姆", school="制度分析", problem=problem,
            perspective="从奥斯特罗姆的公共治理智慧出发",
            core_insight="社区能自主管理公共资源",
            recommendations=[["公地不一定悲剧——社区能自主管理公共资源", "制度多样性——不同情境需要不同规则", "多层次治理——从地方到全球的多层级制度"][i].split("——")[1] if "——" in ["公地不一定悲剧——社区能自主管理公共资源", "制度多样性——不同情境需要不同规则", "多层次治理——从地方到全球的多层级制度"][i] else ["公地不一定悲剧——社区能自主管理公共资源", "制度多样性——不同情境需要不同规则", "多层次治理——从地方到全球的多层级制度"][i] for i in range(len(["公地不一定悲剧——社区能自主管理公共资源", "制度多样性——不同情境需要不同规则", "多层次治理——从地方到全球的多层级制度"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.86,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["公共", "治理", "社区", "制度", "规则"]) else 0))
        return DecisionResult(sage_name="奥斯特罗姆", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return "奥斯特罗姆的智慧：公地不一定悲剧——社区能自主管理公共资源"


class _IrvingFisherCloning(SageCloning):
    """费雪 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="费雪", name_en="Irving Fisher", era="20世纪", years="1867-1947",
            school="货币理论", tier=CloningTier.TIER2_CLUSTER,
            position="户部主事", department="户部",
            title="费雪方程式之父", biography="美国经济学家，提出费雪方程式（MV=PQ），对货币理论影响深远。",
            core_works=["《货币购买力》"],
            capability={"strategic_vision": 8, "execution": 6, "innovation": 9, "leadership": 5, "influence": 8, "cross_domain": 7},
        ))
        self._wisdom_laws = ["费雪方程式——货币数量决定物价水平", "利率决定——真实利率等于名义利率减通胀", "预期效用——决策基于对未来效用的预期"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="费雪", school="货币理论", problem=problem,
            perspective="从费雪的货币数量智慧出发",
            core_insight="货币数量决定物价水平",
            recommendations=[["费雪方程式——货币数量决定物价水平", "利率决定——真实利率等于名义利率减通胀", "预期效用——决策基于对未来效用的预期"][i].split("——")[1] if "——" in ["费雪方程式——货币数量决定物价水平", "利率决定——真实利率等于名义利率减通胀", "预期效用——决策基于对未来效用的预期"][i] else ["费雪方程式——货币数量决定物价水平", "利率决定——真实利率等于名义利率减通胀", "预期效用——决策基于对未来效用的预期"][i] for i in range(len(["费雪方程式——货币数量决定物价水平", "利率决定——真实利率等于名义利率减通胀", "预期效用——决策基于对未来效用的预期"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["货币", "利率", "通胀", "物价", "数量"]) else 0))
        return DecisionResult(sage_name="费雪", problem=context.get("problem",""), chosen_option=chosen, confidence=0.82)

    def advise(self, context: Dict[str, Any]) -> str:
        return "费雪的智慧：费雪方程式——货币数量决定物价水平"


def build_cluster() -> SchoolCluster:
    """构建经济学集群"""
    return SchoolCluster(
        name="经济学集群",
        school="经济学",
        department="户部",
        leader_name="亚当·斯密",
        members={
            "亚当·斯密": _AdamSmithCloning(),
            "大卫·李嘉图": _DavidRicardoCloning(),
            "凯恩斯": _JohnMaynardKeynesCloning(),
            "马克思": _KarlMarxCloning(),
            "弗里德曼": _MiltonFriedmanCloning(),
            "熊彼特": _JosephSchumpeterCloning(),
            "科斯": _RonaldCoaseCloning(),
            "贝克尔": _GaryBeckerCloning(),
            "卡尼曼": _DanielKahnemanCloning(),
            "阿马蒂亚·森": _AmartyaSenCloning(),
            "哈耶克": _HayekCloning(),
            "萨缪尔森": _PaulSamuelsonCloning(),
            "奥斯特罗姆": _ElinorOstromCloning(),
            "费雪(Irving)": _IrvingFisherCloning(),
        },
    )
__all__ = ['build_cluster']
