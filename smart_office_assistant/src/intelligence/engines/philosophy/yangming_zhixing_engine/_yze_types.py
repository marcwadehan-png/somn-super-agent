# -*- coding: utf-8 -*-
"""王阳明知行合一引擎 - 类型定义模块"""
from enum import Enum
from dataclasses import dataclass, field
from typing import List

class KnowingLevel(Enum):
    """知的层次 - 从浅到深"""
    UNKNOWN = "未知"           # 完全不了解
    HEARSAY = "道听途说"       # 听过但不了解
    UNDERSTANDING = "理解"     # 理论上理解
    PRACTICED = "实践过"       # 有实践经验
    INTEGRATED = "融会贯通"    # 知行开始unified
    NATURAL = "自然流露"       # 无需思考自然做到

class ActionStage(Enum):
    """action阶段"""
    NOT_STARTED = "未开始"     # 完全没action
    DELAYED = "拖延中"         # 知道但不动
    STARTED = "已启动"          # 开始action
    PERSISTING = "坚持中"      # 持续执行
    HABITUAL = "习惯化"        # 成为习惯
    MASTERED = "精通"           # 身心合一

class ZhixingBarrier(Enum):
    """执行障碍类型"""
    COGNITIVE = "认知障碍"      # 知之不深
    MOTIVATION = "动机障碍"    # 知与行之间缺乏动力
    CAPABILITY = "能力障碍"    # 知道但不知道怎么做到
    ENVIRONMENT = "环境障碍"    # 外部条件限制
    DESIRE = "私欲障碍"        # 私欲遮蔽良知

@dataclass
class KnowingAnalysis:
    """知之分析"""
    level: KnowingLevel
    score: float  # 0-100
    elements: List[str] = field(default_factory=list)
    barriers: List[str] = field(default_factory=list)
    depth_path: List[str] = field(default_factory=list)
    evidence: str = ""
    quote: str = "知之真切笃实处即是行"

@dataclass
class ActionAnalysis:
    """行之分析"""
    stage: ActionStage
    score: float  # 0-100
    quality: str = ""
    obstacles: List[str] = field(default_factory=list)
    improvement: List[str] = field(default_factory=list)
    evidence: str = ""
    quote: str = "行是知的功夫"

@dataclass
class ZhixingLoop:
    """知行闭环"""
    knowing: KnowingAnalysis
    action: ActionAnalysis
    integration_score: float  # 0-100
    is_true_knowledge: bool
    is_zhi_action: bool
    gap_type: str = ""
    gap_reason: str = ""
    closure_path: List[str] = field(default_factory=list)
    immediate_action: str = ""
    quote: str = ""

@dataclass
class TrueKnowledgeValidator:
    """真知验证器"""
    is_true_knowledge: bool
    validation_criteria: List[dict] = field(default_factory=list)
    evidence_for: List[str] = field(default_factory=list)
    evidence_against: List[str] = field(default_factory=list)
    confidence: float = 0.0
    recommendation: str = ""

@dataclass
class ActionStarterConfig:
    """action启动配置"""
    task: str
    mini_action: str
    barrier_analysis: List[dict] = field(default_factory=list)
    motivation_boost: List[str] = field(default_factory=list)
    friction_reducers: List[str] = field(default_factory=list)
    start_trigger: str = ""
    quote: str = "知是行的开始"

@dataclass
class IterationDeepener:
    """迭代深化器"""
    cycle: int
    current_knowing: KnowingLevel
    current_action: ActionStage
    new_insight: str = ""
    improved_practice: str = ""
    next_action: str = ""
    wisdom_gain: str = ""
    quote: str = "行即是知"

# Python 3.13兼容别名：Unicode标识符在跨模块相对导入时可能被NFKC规范化
# 添加ASCII别名以确保兼容性
Zhixing闭环 = ZhixingLoop  # 保留中文别名（已修复Python 3.13 Unicode规范化）
