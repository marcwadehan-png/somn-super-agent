"""
消费情绪与感性决策研究体系核心模块 [v1.0.0]
作为Somn项目核心能力、底层生产框架、自主学习升级中枢

核心职责:
1. 所有需求产出必须符合此研究框架
2. 系统围绕此框架在联网环境下自主学习自主迭代升级

架构: 5维度 × 6方向 = 30交叉研究点
融合: 神经科学 + AI情绪计算 + Somn智慧(神之架构V4.2.0)
"""

import json
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
import threading
import yaml

logger = logging.getLogger(__name__)


class ResearchDimension(Enum):
    """五大研究维度"""
    EMOTION_TRIGGER = "emotion_trigger"           # A: 情绪触发与波动机制
    EMOTION_TYPE = "emotion_type"                 # B: 情绪类型与消费行为关联
    EMOTION_VALUE = "emotion_value"               # C: 情绪价值感知维度
    SENTIENT_DECISION = "sentient_decision"       # D: 感性决策关键维度
    AI_EMOTION_COMPUTE = "ai_emotion_compute"     # E: AI时代情绪计算与智能决策


class ResearchDirection(Enum):
    """六大研究方向"""
    CONSUMER_EMOTION = "consumer_emotion"         # ①: 消费情绪
    SENTIENT_DECISION_MAKING = "sentient_decision_making"  # ②: 感性决策
    RESEARCH_METHOD = "research_method"           # ③: 研究方法
    PRACTICAL_APPLICATION = "practical_application"  # ④: 落地应用
    RISK_CONTROL = "risk_control"                 # ⑤: 风险管控
    NEUROSCIENCE = "neuroscience"                 # ⑥: 神经科学


@dataclass
class ResearchIntersection:
    """交叉研究点定义"""
    dimension: ResearchDimension
    direction: ResearchDirection
    code: str                                    # 如 "A1", "E6"
    title: str
    research_question: str
    key_frameworks: List[str] = field(default_factory=list)
    measurement_tools: List[str] = field(default_factory=list)
    application_strategies: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    neural_mechanisms: List[str] = field(default_factory=list)  # v2.0新增
    ai_applications: List[str] = field(default_factory=list)    # v2.0新增
    sss_wisdom_refs: List[str] = field(default_factory=list)    # Somn智慧引用
    version: str = "2.0"
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class EmotionResearchFramework:
    """情绪研究框架完整定义"""
    version: str = "2.0.0"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    intersections: Dict[str, ResearchIntersection] = field(default_factory=dict)
    
    # 核心公式与模型
    heart_price_formula: str = """
    心价比(t) = [情绪综合满足感(t) × 情境调节系数(t)] / [综合消费成本(t) × 认知负荷(t)]
    
    其中:
    情绪综合满足感(t) = α·情感满足(t) + β·社会认同(t) + γ·自我表达(t) + δ·神经愉悦度(t)
    综合消费成本(t) = 金钱成本(t) + 时间成本(t) + 认知成本(t) + 机会成本(t) + 神经努力成本(t)
    """
    
    # 应用场景体系
    application_domains: List[str] = field(default_factory=lambda: [
        "product_development",      # 产品研发
        "brand_marketing",          # 品牌营销
        "channel_operation",        # 渠道运营
        "user_operation",           # 用户运营
        "business_management",      # 企业经营
        "market_growth",            # 市场增长
        "neuro_design",             # 神经设计 (v2.0新增)
        "cross_culture",            # 跨文化 (v2.0新增)
    ])


class RequirementValidationResult:
    """需求校验结果"""
    def __init__(self):
        self.is_valid: bool = False
        self.matched_intersections: List[str] = []  # 匹配的交叉点代码
        self.coverage_score: float = 0.0            # 框架覆盖率 0-1
        self.gaps: List[str] = []                   # 缺失维度
        self.recommendations: List[str] = []        # 改进建议
        self.enhanced_requirement: str = ""         # 增强后的需求描述
        self.validation_timestamp: str = datetime.now().isoformat()


class EmotionResearchCore:
    """
    消费情绪研究体系核心 [v1.0.0]
    
    作为Somn项目的:
    1. 核心能力中枢 - 所有产出必须符合此框架
    2. 底层生产框架 - 指导需求分析、策略设计、执行评估
    3. 自主学习引擎 - 联网环境下持续迭代升级
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, base_path: Optional[Path] = None):
        if hasattr(self, '_initialized'):
            return
        
        self.base_path = base_path or Path(__file__).resolve().parents[4]
        self.framework_file = self.base_path / "file" / "系统文件" / "消费情绪与感性决策_交叉研究体系_v2.0.md"
        self.learning_data_dir = self.base_path / "data" / "emotion_research_learning"
        self.learning_data_dir.mkdir(parents=True, exist_ok=True)
        
        # 核心框架
        self.framework: EmotionResearchFramework = self._init_framework()
        
        # 校验规则引擎
        self.validation_rules: Dict[str, Any] = self._init_validation_rules()
        
        # 学习状态
        self.learning_state = {
            "last_learning_time": None,
            "learning_count": 0,
            "knowledge_updates": [],
            "auto_upgrade_enabled": True,
        }
        
        # 联网学习配置
        self.web_learning_config = {
            "sources": [
                "academic_journals",      # 学术期刊
                "industry_reports",       # 行业报告
                "news_trends",            # 新闻趋势
                "social_media",           # 社交媒体
                "competitor_analysis",    # 竞品分析
            ],
            "learning_frequency": "daily",    # 学习频率
            "update_threshold": 0.8,          # 更新阈值
        }
        
        self._initialized = True
        logger.info("✅ EmotionResearchCore 初始化完成 [v1.0.0]")
    
    def _init_framework(self) -> EmotionResearchFramework:
        """初始化30个交叉研究点框架 [v1.0 按维度拆分]"""
        framework = EmotionResearchFramework()
        
        # A系列: 情绪触发与波动机制 × 6方向
        self._init_dimension_A(framework)
        
        # B系列: 情绪类型与消费行为关联 × 6方向
        self._init_dimension_B(framework)
        
        # C系列: 情绪价值感知维度 × 6方向
        self._init_dimension_C(framework)
        
        # D系列: 感性决策关键维度 × 6方向
        self._init_dimension_D(framework)
        
        # E系列: AI时代情绪计算与智能决策 × 6方向 (v2.0新增)
        self._init_dimension_E(framework)
        
        return framework
    
    def _init_dimension_A(self, framework: EmotionResearchFramework) -> None:
        """[单一职责] A系列: 情绪触发与波动机制 × 6方向"""
        framework.intersections["A1"] = ResearchIntersection(
            dimension=ResearchDimension.EMOTION_TRIGGER,
            direction=ResearchDirection.CONSUMER_EMOTION,
            code="A1",
            title="情绪触发机制研究",
            research_question="生理-环境-心理-数字四重维度如何叠加触发消费情绪？",
            key_frameworks=["四重触发模型", "情绪唤醒理论", "数字情境触发"],
            measurement_tools=["GSR", "HRV", "fMRI", "情绪触发量表(ETS)"],
            application_strategies=["五感设计矩阵", "情绪曲线设计", "场景化陈列"],
            risk_factors=["过度触发", "负面放大", "伦理边界"],
            neural_mechanisms=["奖赏回路激活", "杏仁核快速响应", "前额叶调控", "多巴胺预测误差"],
            ai_applications=["实时情绪识别", "触发时机预测"],
            sss_wisdom_refs=["孔子:仁礼之道", "管仲:轻重之术"],
        )
        
        framework.intersections["A2"] = ResearchIntersection(
            dimension=ResearchDimension.EMOTION_TRIGGER,
            direction=ResearchDirection.SENTIENT_DECISION_MAKING,
            code="A2",
            title="情绪波动周期研究",
            research_question="不同时间维度的情绪波动如何影响决策模式？",
            key_frameworks=["波动周期模型", "决策模式切换理论"],
            measurement_tools=["时间戳记录", "决策路径追踪"],
            neural_mechanisms=["基底神经节快速响应", "边缘系统激活", "前额叶-边缘系统协调"],
        )
        
        framework.intersections["A3"] = ResearchIntersection(
            dimension=ResearchDimension.EMOTION_TRIGGER,
            direction=ResearchDirection.RESEARCH_METHOD,
            code="A3",
            title="情绪触发测量方法",
            research_question="如何科学测量情绪触发的时机与强度？",
            measurement_tools=["GSR", "HRV", "fMRI", "眼动追踪", "微表情识别", "LLM情感推理"],
        )
        
        framework.intersections["A4"] = ResearchIntersection(
            dimension=ResearchDimension.EMOTION_TRIGGER,
            direction=ResearchDirection.PRACTICAL_APPLICATION,
            code="A4",
            title="触发机制落地应用",
            research_question="如何在各业务场景设计情绪触发点？",
            application_strategies=["五感设计矩阵", "神经美学原则", "情绪曲线设计"],
        )
        
        framework.intersections["A5"] = ResearchIntersection(
            dimension=ResearchDimension.EMOTION_TRIGGER,
            direction=ResearchDirection.RISK_CONTROL,
            code="A5",
            title="触发机制风险管控",
            research_question="情绪触发设计中的潜在风险与规避？",
            risk_factors=["过度触发", "负面放大", "伦理边界", "算法偏见"],
        )
        
        framework.intersections["A6"] = ResearchIntersection(
            dimension=ResearchDimension.EMOTION_TRIGGER,
            direction=ResearchDirection.NEUROSCIENCE,
            code="A6",
            title="情绪触发神经机制",
            research_question="情绪触发的神经基础与神经营销应用",
            neural_mechanisms=["奖赏预测误差", "情绪记忆固化", "注意捕获", "社会认同神经基础"],
        )
    
    def _init_dimension_B(self, framework: EmotionResearchFramework) -> None:
        """[单一职责] B系列: 情绪类型与消费行为关联 × 6方向"""
        framework.intersections["B1"] = ResearchIntersection(
            dimension=ResearchDimension.EMOTION_TYPE,
            direction=ResearchDirection.CONSUMER_EMOTION,
            code="B1",
            title="情绪-行为映射研究",
            research_question="普拉切克情绪轮盘如何映射到具体消费行为？",
            key_frameworks=["四大象限消费行为矩阵", "情绪-神经递质-消费行为三元映射"],
            neural_mechanisms=["多巴胺释放峰值", "血清素稳定水平", "皮质醇-多巴胺平衡", "催产素需求激活"],
        )
        
        framework.intersections["B2"] = ResearchIntersection(
            dimension=ResearchDimension.EMOTION_TYPE,
            direction=ResearchDirection.SENTIENT_DECISION_MAKING,
            code="B2",
            title="情绪-决策关联研究",
            research_question="不同情绪类型如何影响决策路径？",
            neural_mechanisms=["边缘系统主导", "前额叶-边缘系统平衡", "杏仁核激活", "催产素系统激活"],
        )
        
        framework.intersections["B3"] = ResearchIntersection(
            dimension=ResearchDimension.EMOTION_TYPE,
            direction=ResearchDirection.RESEARCH_METHOD,
            code="B3",
            title="情绪类型测量方法",
            research_question="如何准确识别和测量消费者的情绪类型？",
            measurement_tools=["PANAS量表", "AI面部识别", "fMRI消费决策任务", "数字痕迹分析"],
        )
        
        framework.intersections["B4"] = ResearchIntersection(
            dimension=ResearchDimension.EMOTION_TYPE,
            direction=ResearchDirection.PRACTICAL_APPLICATION,
            code="B4",
            title="情绪类型应用策略",
            research_question="如何针对不同情绪类型设计产品和营销策略？",
            application_strategies=["神经设计原则", "多巴胺间歇强化", "催产素情感联结"],
        )
        
        framework.intersections["B5"] = ResearchIntersection(
            dimension=ResearchDimension.EMOTION_TYPE,
            direction=ResearchDirection.RISK_CONTROL,
            code="B5",
            title="情绪类型应用风险",
            research_question="情绪类型应用中的风险识别与规避？",
            risk_factors=["情绪误读", "情绪操纵", "神经伦理"],
        )
        
        framework.intersections["B6"] = ResearchIntersection(
            dimension=ResearchDimension.EMOTION_TYPE,
            direction=ResearchDirection.NEUROSCIENCE,
            code="B6",
            title="情绪类型神经基础",
            research_question="不同情绪类型的神经基础与神经营销应用",
            neural_mechanisms=["多巴胺系统", "血清素系统", "催产素系统", "皮质醇系统"],
        )
    
    def _init_dimension_C(self, framework: EmotionResearchFramework) -> None:
        """[单一职责] C系列: 情绪价值感知维度 × 6方向"""
        framework.intersections["C1"] = ResearchIntersection(
            dimension=ResearchDimension.EMOTION_VALUE,
            direction=ResearchDirection.CONSUMER_EMOTION,
            code="C1",
            title="心价比动态模型研究",
            research_question="消费者如何动态计算和感知心价比？",
            key_frameworks=["心价比动态模型", "情境调节系数", "神经愉悦度"],
            neural_mechanisms=["奖赏回路", "催产素系统", "默认模式网络(DMN)"],
        )
        
        framework.intersections["C2"] = ResearchIntersection(
            dimension=ResearchDimension.EMOTION_VALUE,
            direction=ResearchDirection.SENTIENT_DECISION_MAKING,
            code="C2",
            title="价值感知决策研究",
            research_question="情绪价值感知如何影响最终购买决策？",
            key_frameworks=["决策权重动态模型", "神经价值权重"],
        )
        
        framework.intersections["C3"] = ResearchIntersection(
            dimension=ResearchDimension.EMOTION_VALUE,
            direction=ResearchDirection.RESEARCH_METHOD,
            code="C3",
            title="心价比测量方法",
            research_question="如何科学测量消费者的心价比感知？",
            measurement_tools=["CSI量表", "fMRI愉悦度任务", "神经努力成本测量"],
        )
        
        framework.intersections["C4"] = ResearchIntersection(
            dimension=ResearchDimension.EMOTION_VALUE,
            direction=ResearchDirection.PRACTICAL_APPLICATION,
            code="C4",
            title="心价比提升策略",
            research_question="如何在各业务环节提升产品的心价比？",
            application_strategies=["多巴胺间歇强化", "前额叶负荷降低", "神经锚定"],
        )
        
        framework.intersections["C5"] = ResearchIntersection(
            dimension=ResearchDimension.EMOTION_VALUE,
            direction=ResearchDirection.RISK_CONTROL,
            code="C5",
            title="心价比风险管控",
            research_question="心价比承诺与交付不一致的风险？",
            risk_factors=["过度承诺", "神经疲劳", "多巴胺受体钝化"],
        )
        
        framework.intersections["C6"] = ResearchIntersection(
            dimension=ResearchDimension.EMOTION_VALUE,
            direction=ResearchDirection.NEUROSCIENCE,
            code="C6",
            title="心价比神经机制",
            research_question="心价比感知的神经基础与神经营销优化",
            neural_mechanisms=["眶额皮层价值编码", "前扣带回冲突监测", "时间折扣神经机制"],
        )
    
    def _init_dimension_D(self, framework: EmotionResearchFramework) -> None:
        """[单一职责] D系列: 感性决策关键维度 × 6方向"""
        framework.intersections["D1"] = ResearchIntersection(
            dimension=ResearchDimension.SENTIENT_DECISION,
            direction=ResearchDirection.CONSUMER_EMOTION,
            code="D1",
            title="决策触点研究",
            research_question="感性决策的关键触点如何影响情绪体验？",
            key_frameworks=["全链路情绪触点地图", "神经旅程地图"],
        )
        
        framework.intersections["D2"] = ResearchIntersection(
            dimension=ResearchDimension.SENTIENT_DECISION,
            direction=ResearchDirection.SENTIENT_DECISION_MAKING,
            code="D2",
            title="感性决策机制研究",
            research_question="感性决策的深层心理与神经机制是什么？",
            key_frameworks=["决策机制模型", "神经习惯回路"],
            neural_mechanisms=["基底神经节习惯回路", "认知捷径神经机制", "自我参照加工网络"],
        )
        
        framework.intersections["D3"] = ResearchIntersection(
            dimension=ResearchDimension.SENTIENT_DECISION,
            direction=ResearchDirection.RESEARCH_METHOD,
            code="D3",
            title="决策机制研究方法",
            research_question="如何研究消费者的感性决策机制？",
            measurement_tools=["神经旅程地图", "神经营销实验", "fNIRS移动测量"],
        )
        
        framework.intersections["D4"] = ResearchIntersection(
            dimension=ResearchDimension.SENTIENT_DECISION,
            direction=ResearchDirection.PRACTICAL_APPLICATION,
            code="D4",
            title="决策机制应用策略",
            research_question="如何在各业务环节优化感性决策？",
            application_strategies=["认知负荷神经降低", "情绪记忆神经固化", "习惯回路设计"],
        )
        
        framework.intersections["D5"] = ResearchIntersection(
            dimension=ResearchDimension.SENTIENT_DECISION,
            direction=ResearchDirection.RISK_CONTROL,
            code="D5",
            title="决策机制风险管控",
            research_question="感性决策引导中的伦理与合规风险？",
            risk_factors=["误导性scarcity", "情感操纵", "成瘾性设计", "神经操纵"],
        )
        
        framework.intersections["D6"] = ResearchIntersection(
            dimension=ResearchDimension.SENTIENT_DECISION,
            direction=ResearchDirection.NEUROSCIENCE,
            code="D6",
            title="决策机制神经科学",
            research_question="感性决策的神经机制与神经营销优化",
            neural_mechanisms=["双系统决策", "价值整合", "冲突监测", "习惯自动化"],
        )
    
    def _init_dimension_E(self, framework: EmotionResearchFramework) -> None:
        """[单一职责] E系列: AI时代情绪计算与智能决策 × 6方向"""
        framework.intersections["E1"] = ResearchIntersection(
            dimension=ResearchDimension.AI_EMOTION_COMPUTE,
            direction=ResearchDirection.CONSUMER_EMOTION,
            code="E1",
            title="AI情绪识别与预测",
            research_question="AI如何识别和预测消费者情绪状态？",
            key_frameworks=["多模态情绪融合", "LLM情绪推理"],
            ai_applications=["面部表情识别", "语音情感分析", "文本情感分析", "多模态融合"],
        )
        
        framework.intersections["E2"] = ResearchIntersection(
            dimension=ResearchDimension.AI_EMOTION_COMPUTE,
            direction=ResearchDirection.SENTIENT_DECISION_MAKING,
            code="E2",
            title="AI驱动的感性决策",
            research_question="AI如何影响和优化感性决策过程？",
            ai_applications=["个性化推荐", "情绪适配定价", "智能客服", "生成式AI内容"],
        )
        
        framework.intersections["E3"] = ResearchIntersection(
            dimension=ResearchDimension.AI_EMOTION_COMPUTE,
            direction=ResearchDirection.RESEARCH_METHOD,
            code="E3",
            title="AI情绪研究方法",
            research_question="如何利用AI技术提升情绪研究效率和精度？",
            ai_applications=["LLM情感分析", "生成式模拟", "预测模型", "因果推断"],
        )
        
        framework.intersections["E4"] = ResearchIntersection(
            dimension=ResearchDimension.AI_EMOTION_COMPUTE,
            direction=ResearchDirection.PRACTICAL_APPLICATION,
            code="E4",
            title="AI情绪应用落地",
            research_question="如何在业务场景中落地AI情绪计算？",
            ai_applications=["智能客服", "个性化推荐", "内容生成", "预测性干预"],
        )
        
        framework.intersections["E5"] = ResearchIntersection(
            dimension=ResearchDimension.AI_EMOTION_COMPUTE,
            direction=ResearchDirection.RISK_CONTROL,
            code="E5",
            title="AI情绪应用风险",
            research_question="AI情绪计算应用的伦理与合规风险？",
            risk_factors=["算法偏见", "隐私侵犯", "情绪操纵", "深度伪造"],
        )
        
        framework.intersections["E6"] = ResearchIntersection(
            dimension=ResearchDimension.AI_EMOTION_COMPUTE,
            direction=ResearchDirection.NEUROSCIENCE,
            code="E6",
            title="AI情绪神经科学",
            research_question="AI如何模拟和理解人类情绪神经机制？",
            neural_mechanisms=["神经启发AI", "脑机接口", "计算精神病学"],
            ai_applications=["脉冲神经网络", "神经信号解码", "情绪训练系统"],
        )
    
    def _init_validation_rules(self) -> Dict[str, Any]:
        """初始化需求校验规则引擎"""
        return {
            "required_dimensions": [d.value for d in ResearchDimension],
            "minimum_coverage": 0.6,  # 最低覆盖率60%
            "critical_intersections": ["A1", "B1", "C1", "D2", "E2"],  # 必须覆盖的关键交叉点
            "emotion_keywords": {
                "consumer_emotion": ["情绪", "情感", "感受", "体验", "满意", "愉悦", "焦虑", "信任"],
                "sentient_decision": ["决策", "选择", "购买", "偏好", "冲动", "理性", "感性"],
                "neuroscience": ["神经", "大脑", "认知", "心理", "生理", "潜意识"],
                "ai_emotion": ["AI", "智能", "算法", "预测", "识别", "个性化"],
            },
            "validation_weights": {
                "dimension_coverage": 0.3,
                "intersection_depth": 0.3,
                "methodology_rigor": 0.2,
                "application_clarity": 0.2,
            }
        }
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # 核心API: 需求校验与框架约束
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def validate_requirement(self, requirement: str, context: Optional[Dict] = None) -> RequirementValidationResult:
        """
        校验需求是否符合情绪研究框架
        
        所有进入系统的需求必须通过此校验
        """
        result = RequirementValidationResult()
        context = context or {}
        
        # 1. 关键词匹配分析
        matched_dimensions = set()
        matched_intersections = []
        
        for intersection in self.framework.intersections.values():
            score = self._calculate_intersection_match_score(requirement, intersection)
            if score > 0.3:  # 阈值
                matched_intersections.append((intersection.code, score))
                matched_dimensions.add(intersection.dimension)
        
        # 排序并提取
        matched_intersections.sort(key=lambda x: x[1], reverse=True)
        result.matched_intersections = [code for code, _ in matched_intersections[:10]]
        
        # 2. 覆盖率计算
        dimension_coverage = len(matched_dimensions) / len(ResearchDimension)
        result.coverage_score = dimension_coverage
        
        # 3. 关键交叉点检查
        critical_missing = set(self.validation_rules["critical_intersections"]) - set(result.matched_intersections)
        result.gaps = list(critical_missing)
        
        # 4. 生成增强需求描述
        result.enhanced_requirement = self._enhance_requirement(requirement, result.matched_intersections)
        
        # 5. 生成改进建议
        result.recommendations = self._generate_recommendations(requirement, result)
        
        # 6. 最终判定
        result.is_valid = (
            dimension_coverage >= self.validation_rules["minimum_coverage"] and
            len(critical_missing) <= 2  # 允许最多缺失2个关键交叉点
        )
        
        logger.info(f"需求校验完成: coverage={dimension_coverage:.2f}, valid={result.is_valid}")
        return result
    
    def _calculate_intersection_match_score(self, requirement: str, intersection: ResearchIntersection) -> float:
        """计算需求与交叉点的匹配分数"""
        score = 0.0
        req_lower = requirement.lower()
        
        # 标题匹配
        if intersection.title in requirement or any(kw in req_lower for kw in intersection.title.lower().split()):
            score += 0.3
        
        # 研究问题匹配
        if any(kw in req_lower for kw in intersection.research_question.lower().split()[:5]):
            score += 0.2
        
        # 框架匹配
        for framework in intersection.key_frameworks:
            if any(kw in req_lower for kw in framework.lower().split()):
                score += 0.1
        
        # 神经机制匹配 (v1.0)
        for mechanism in intersection.neural_mechanisms:
            if any(kw in req_lower for kw in mechanism.lower().split()):
                score += 0.1
        
        # AI应用匹配 (v1.0)
        for app in intersection.ai_applications:
            if any(kw in req_lower for kw in app.lower().split()):
                score += 0.1
        
        return min(score, 1.0)
    
    def _enhance_requirement(self, original: str, matched_intersections: List[str]) -> str:
        """基于框架增强需求描述"""
        enhancements = []
        
        for code in matched_intersections[:5]:
            intersection = self.framework.intersections.get(code)
            if intersection:
                enhancements.append(f"[{code}] {intersection.title}: {intersection.research_question}")
        
        enhanced = f"""原始需求: {original}

框架增强分析:
{chr(10).join(f"- {e}" for e in enhancements)}

建议研究方向:
基于情绪研究体系v2.0，建议从以下维度深入:
{chr(10).join(f"- 维度{self.framework.intersections[c].dimension.value}: {self.framework.intersections[c].title}" for c in matched_intersections[:3] if c in self.framework.intersections)}
"""
        return enhanced
    
    def _generate_recommendations(self, requirement: str, result: RequirementValidationResult) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        if result.coverage_score < 0.6:
            recommendations.append(f"框架覆盖率仅{result.coverage_score:.0%}，建议补充以下维度:")
            all_dims = set(d.value for d in ResearchDimension)
            covered_dims = set(self.framework.intersections[c].dimension.value for c in result.matched_intersections if c in self.framework.intersections)
            missing_dims = all_dims - covered_dims
            for dim in missing_dims:
                recommendations.append(f"  - 考虑纳入{dim}维度的研究视角")
        
        if result.gaps:
            recommendations.append(f"缺失关键交叉点: {', '.join(result.gaps)}，建议补充研究")
        
        # 检查是否涉及AI
        if "AI" in requirement or "智能" in requirement:
            if not any(c.startswith("E") for c in result.matched_intersections):
                recommendations.append("需求涉及AI但缺少E系列(AI情绪计算)交叉点，建议补充AI情绪识别/预测研究")
        
        # 检查是否涉及神经科学
        if "神经" in requirement or "大脑" in requirement:
            if not any(c.endswith("6") for c in result.matched_intersections):
                recommendations.append("需求涉及神经科学但缺少⑥列研究，建议补充神经机制分析")
        
        return recommendations
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # 核心API: 策略生成与框架指导
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def generate_strategy_framework(self, requirement: str, validation_result: Optional[RequirementValidationResult] = None) -> Dict[str, Any]:
        """
        基于研究框架生成策略设计框架
        
        所有策略设计必须基于此框架产出
        """
        validation = validation_result or self.validate_requirement(requirement)
        
        strategy_framework = {
            "requirement": requirement,
            "validation": {
                "is_valid": validation.is_valid,
                "coverage_score": validation.coverage_score,
                "matched_intersections": validation.matched_intersections,
            },
            "research_dimensions": {},
            "application_domains": {},
            "methodology_stack": [],
            "risk_control_points": [],
            "neuroscience_insights": [],  # v1.0
            "ai_applications": [],        # v1.0
            "sss_wisdom_refs": [],        # Somn智慧
        }
        
        # 按维度组织交叉点
        for code in validation.matched_intersections:
            intersection = self.framework.intersections.get(code)
            if intersection:
                dim_key = intersection.dimension.value
                if dim_key not in strategy_framework["research_dimensions"]:
                    strategy_framework["research_dimensions"][dim_key] = []
                
                strategy_framework["research_dimensions"][dim_key].append({
                    "code": code,
                    "title": intersection.title,
                    "research_question": intersection.research_question,
                    "key_frameworks": intersection.key_frameworks,
                    "application_strategies": intersection.application_strategies,
                    "neural_mechanisms": intersection.neural_mechanisms,
                    "ai_applications": intersection.ai_applications,
                })
                
                # 收集方法论
                strategy_framework["methodology_stack"].extend(intersection.measurement_tools)
                
                # 收集风险点
                strategy_framework["risk_control_points"].extend(intersection.risk_factors)
                
                # 收集神经科学洞察
                strategy_framework["neuroscience_insights"].extend(intersection.neural_mechanisms)
                
                # 收集AI应用
                strategy_framework["ai_applications"].extend(intersection.ai_applications)
                
                # 收集Somn智慧
                strategy_framework["sss_wisdom_refs"].extend(intersection.sss_wisdom_refs)
        
        # 去重
        strategy_framework["methodology_stack"] = list(set(strategy_framework["methodology_stack"]))
        strategy_framework["risk_control_points"] = list(set(strategy_framework["risk_control_points"]))
        strategy_framework["neuroscience_insights"] = list(set(strategy_framework["neuroscience_insights"]))
        strategy_framework["ai_applications"] = list(set(strategy_framework["ai_applications"]))
        strategy_framework["sss_wisdom_refs"] = list(set(strategy_framework["sss_wisdom_refs"]))
        
        return strategy_framework
    
    def get_heart_price_formula(self, context: Optional[Dict] = None) -> Dict[str, Any]:
        """获取心价比计算公式及应用指导"""
        return {
            "formula": self.framework.heart_price_formula,
            "variables": {
                "emotional_satisfaction": {
                    "description": "情绪综合满足感",
                    "components": ["情感满足", "社会认同", "自我表达", "神经愉悦度"],
                    "weights": {"alpha": 0.3, "beta": 0.25, "gamma": 0.2, "delta": 0.25},
                },
                "contextual_modulator": {
                    "description": "情境调节系数",
                    "factors": ["时间压力", "社交情境", "生理状态", "数字环境"],
                },
                "total_cost": {
                    "description": "综合消费成本",
                    "components": ["金钱成本", "时间成本", "认知成本", "机会成本", "神经努力成本"],
                },
                "cognitive_load": {
                    "description": "认知负荷",
                    "factors": ["信息复杂度", "决策选项数", "情绪唤醒度"],
                },
            },
            "interpretation": {
                ">2.0": "极高心价比，冲动购买",
                "1.5-2.0": "高心价比，强购买意愿",
                "1.0-1.5": "中心价比，需推动",
                "<1.0": "低心价比，需优化",
            },
        }
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # 核心API: 自主学习与迭代升级
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def learn_from_execution(self, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        从执行结果中学习，更新研究框架
        
        每次任务执行后调用，实现持续学习
        """
        learning_record = {
            "timestamp": datetime.now().isoformat(),
            "execution_id": execution_data.get("execution_id"),
            "requirement": execution_data.get("requirement"),
            "intersections_used": execution_data.get("intersections_used", []),
            "effectiveness_score": execution_data.get("effectiveness_score", 0.0),
            "new_insights": execution_data.get("new_insights", []),
            "gaps_identified": execution_data.get("gaps_identified", []),
        }
        
        # 保存学习记录
        self._save_learning_record(learning_record)
        
        # 更新学习状态
        self.learning_state["learning_count"] += 1
        self.learning_state["last_learning_time"] = datetime.now().isoformat()
        self.learning_state["knowledge_updates"].append(learning_record)
        
        # 触发框架更新检查
        update_suggestions = self._check_framework_updates(learning_record)
        
        logger.info(f"学习记录已保存: execution_id={execution_data.get('execution_id')}")
        
        return {
            "learning_record_id": self._hash_learning_record(learning_record),
            "framework_version": self.framework.version,
            "update_suggestions": update_suggestions,
        }
    
    def _save_learning_record(self, record: Dict[str, Any]):
        """保存学习记录到本地存储"""
        record_id = self._hash_learning_record(record)
        record_file = self.learning_data_dir / f"learning_{record_id}.json"
        
        with open(record_file, 'w', encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
    
    def _hash_learning_record(self, record: Dict[str, Any]) -> str:
        """生成学习记录哈希ID"""
        content = f"{record['timestamp']}_{record.get('execution_id', '')}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _check_framework_updates(self, learning_record: Dict[str, Any]) -> List[str]:
        """检查是否需要更新框架"""
        suggestions = []
        
        # 检查效果分数
        if learning_record.get("effectiveness_score", 0) < 0.6:
            suggestions.append("效果分数较低，建议优化对应交叉点的应用策略")
        
        # 检查新洞察
        new_insights = learning_record.get("new_insights", [])
        if len(new_insights) > 3:
            suggestions.append(f"发现{len(new_insights)}个新洞察，建议考虑纳入框架更新")
        
        # 检查缺失
        gaps = learning_record.get("gaps_identified", [])
        if gaps:
            suggestions.append(f"识别到缺失维度: {', '.join(gaps)}")
        
        return suggestions
    
    def auto_learn_from_web(self, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        从联网搜索结果中自主学习
        
        在联网环境下自动调用，实现知识更新
        """
        if not self.learning_state["auto_upgrade_enabled"]:
            return {"status": "disabled", "message": "自动学习已禁用"}
        
        learned_items = []
        
        for result in search_results:
            # 分析搜索结果与框架的关联
            relevance = self._analyze_web_content_relevance(result)
            
            if relevance["score"] > 0.7:
                learned_item = {
                    "source": result.get("source"),
                    "title": result.get("title"),
                    "relevance_score": relevance["score"],
                    "related_intersections": relevance["related_intersections"],
                    "key_findings": relevance["key_findings"],
                    "suggested_framework_updates": relevance["suggestions"],
                }
                learned_items.append(learned_item)
        
        # 保存学习结果
        learning_batch = {
            "timestamp": datetime.now().isoformat(),
            "source_type": "web_search",
            "items_learned": len(learned_items),
            "learned_items": learned_items,
        }
        
        batch_file = self.learning_data_dir / f"web_learning_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(learning_batch, f, ensure_ascii=False, indent=2)
        
        logger.info(f"联网学习完成: 从{len(search_results)}条结果中学习{len(learned_items)}条")
        
        return {
            "status": "success",
            "items_learned": len(learned_items),
            "learning_batch_file": str(batch_file),
            "suggested_updates": [item["suggested_framework_updates"] for item in learned_items[:5]],
        }
    
    def _analyze_web_content_relevance(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """分析网页内容与框架的相关性"""
        text = f"{content.get('title', '')} {content.get('snippet', '')}"
        text_lower = text.lower()
        
        score = 0.0
        related_intersections = []
        key_findings = []
        suggestions = []
        
        # 检查与各个交叉点的相关性
        for code, intersection in self.framework.intersections.items():
            match_score = 0.0
            
            # 标题关键词匹配
            for kw in intersection.title.lower().split():
                if kw in text_lower:
                    match_score += 0.1
            
            # 神经机制匹配
            for mechanism in intersection.neural_mechanisms:
                if any(m.lower() in text_lower for m in mechanism.lower().split()):
                    match_score += 0.15
                    key_findings.append(f"神经机制: {mechanism}")
            
            # AI应用匹配
            for app in intersection.ai_applications:
                if any(a.lower() in text_lower for a in app.lower().split()):
                    match_score += 0.15
                    key_findings.append(f"AI应用: {app}")
            
            if match_score > 0.3:
                score = max(score, match_score)
                related_intersections.append(code)
        
        # 生成更新建议
        if score > 0.7:
            suggestions.append(f"高相关性内容，建议更新交叉点{related_intersections[:3]}")
        
        return {
            "score": min(score, 1.0),
            "related_intersections": related_intersections[:5],
            "key_findings": list(set(key_findings))[:10],
            "suggestions": suggestions,
        }
    
    def propose_framework_upgrade(self) -> Dict[str, Any]:
        """
        基于学习历史提出框架升级建议
        
        定期调用，实现框架自主迭代
        """
        # 加载所有学习记录
        learning_records = self._load_all_learning_records()
        
        # 分析趋势
        intersection_effectiveness = {}
        for record in learning_records:
            for intersection in record.get("intersections_used", []):
                if intersection not in intersection_effectiveness:
                    intersection_effectiveness[intersection] = []
                intersection_effectiveness[intersection].append(record.get("effectiveness_score", 0))
        
        # 计算平均效果
        avg_effectiveness = {
            k: sum(v) / len(v) if v else 0
            for k, v in intersection_effectiveness.items()
        }
        
        # 识别需要优化的交叉点
        weak_intersections = [
            k for k, v in avg_effectiveness.items()
            if v < 0.6 and k in self.framework.intersections
        ]
        
        # 识别高效果交叉点
        strong_intersections = [
            k for k, v in avg_effectiveness.items()
            if v > 0.8 and k in self.framework.intersections
        ]
        
        # 生成升级建议
        upgrade_proposal = {
            "proposal_id": f"upgrade_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "current_version": self.framework.version,
            "proposed_version": f"{float(self.framework.version) + 0.1:.1f}",
            "analysis_summary": {
                "total_learning_records": len(learning_records),
                "intersections_analyzed": len(intersection_effectiveness),
                "weak_intersections": weak_intersections,
                "strong_intersections": strong_intersections,
            },
            "suggested_updates": [],
        }
        
        # 为弱交叉点生成更新建议
        for code in weak_intersections:
            intersection = self.framework.intersections.get(code)
            if intersection:
                upgrade_proposal["suggested_updates"].append({
                    "intersection_code": code,
                    "title": intersection.title,
                    "issue": "效果分数持续低于阈值",
                    "suggestions": [
                        "补充更多应用案例",
                        "优化测量工具",
                        "增加神经科学解释",
                        "补充AI应用方法",
                    ],
                })
        
        return upgrade_proposal
    
    def _load_all_learning_records(self) -> List[Dict[str, Any]]:
        """加载所有学习记录"""
        records = []
        
        for record_file in self.learning_data_dir.glob("learning_*.json"):
            try:
                with open(record_file, 'r', encoding='utf-8') as f:
                    records.append(json.load(f))
            except Exception as e:
                logger.warning(f"加载学习记录失败 {record_file}: {e}")
        
        return records
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # 工具方法
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def get_intersection_detail(self, code: str) -> Optional[Dict[str, Any]]:
        """获取交叉点详细信息"""
        intersection = self.framework.intersections.get(code)
        if intersection:
            return asdict(intersection)
        return None
    
    def list_all_intersections(self) -> List[Dict[str, Any]]:
        """列出所有交叉点"""
        return [asdict(i) for i in self.framework.intersections.values()]
    
    def get_framework_summary(self) -> Dict[str, Any]:
        """获取框架摘要"""
        return {
            "version": self.framework.version,
            "total_intersections": len(self.framework.intersections),
            "dimensions": [d.value for d in ResearchDimension],
            "directions": [d.value for d in ResearchDirection],
            "application_domains": self.framework.application_domains,
            "learning_stats": {
                "total_learning_records": len(self._load_all_learning_records()),
                "auto_upgrade_enabled": self.learning_state["auto_upgrade_enabled"],
                "last_learning_time": self.learning_state["last_learning_time"],
            },
        }
    
    def export_framework(self, format: str = "json") -> str:
        """导出框架到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == "json":
            export_file = self.learning_data_dir / f"framework_export_{timestamp}.json"
            export_data = {
                "framework": asdict(self.framework),
                "validation_rules": self.validation_rules,
                "learning_state": self.learning_state,
                "export_timestamp": datetime.now().isoformat(),
            }
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        elif format == "yaml":
            export_file = self.learning_data_dir / f"framework_export_{timestamp}.yaml"
            export_data = {
                "framework": asdict(self.framework),
                "validation_rules": self.validation_rules,
                "learning_state": self.learning_state,
                "export_timestamp": datetime.now().isoformat(),
            }
            with open(export_file, 'w', encoding='utf-8') as f:
                yaml.dump(export_data, f, allow_unicode=True, sort_keys=False)
        
        return str(export_file)


# ═══════════════════════════════════════════════════════════════════════════════
# 全局单例实例
# ═══════════════════════════════════════════════════════════════════════════════

_emotion_research_core: Optional[EmotionResearchCore] = None

def get_emotion_research_core(base_path: Optional[Path] = None) -> EmotionResearchCore:
    """获取EmotionResearchCore单例实例"""
    global _emotion_research_core
    
    if _emotion_research_core is None:
        _emotion_research_core = EmotionResearchCore(base_path)
    
    return _emotion_research_core


# 便捷函数
def validate_requirement(requirement: str, context: Optional[Dict] = None) -> RequirementValidationResult:
    """便捷函数: 校验需求"""
    core = get_emotion_research_core()
    return core.validate_requirement(requirement, context)

def generate_strategy_framework(requirement: str) -> Dict[str, Any]:
    """便捷函数: 生成策略框架"""
    core = get_emotion_research_core()
    validation = core.validate_requirement(requirement)
    return core.generate_strategy_framework(requirement, validation)

def get_heart_price_formula() -> Dict[str, Any]:
    """便捷函数: 获取心价比公式"""
    core = get_emotion_research_core()
    return core.get_heart_price_formula()

def learn_from_execution(execution_data: Dict[str, Any]) -> Dict[str, Any]:
    """便捷函数: 学习执行结果"""
    core = get_emotion_research_core()
    return core.learn_from_execution(execution_data)

def auto_learn_from_web(search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """便捷函数: 联网自主学习"""
    core = get_emotion_research_core()
    return core.auto_learn_from_web(search_results)
