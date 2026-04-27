"""
学习策略模块 - Learning Strategies Package

将 6 个碎片化学习文件的核心差异化能力提取为可插拔策略类。

策略清单：
    DAILY      → DailyLearningStrategy    （实例/验证/错误/关联 + RL闭环 + 迁移学习）
    THREE_TIER → ThreeTierLearningStrategy（三层：本地可选/网络必须/交叉融合）
    ENHANCED   → EnhancedLearningStrategy  （场景识别+动态策略+浏览器自动化+自适应调参）
    SOLUTION   → SolutionLearningStrategy  （growth_engine方案学习 + YAML报告 + 工作记忆）
    FEEDBACK   → FeedbackLoopStrategy      （轻量：RL闭环 + 迁移学习）

公共基础：
    LearningStrategyType  - 策略类型枚举
    BaseLearningStrategy  - 抽象基类（execute / should_execute / get_description）
    LearningResult        - 统一执行结果数据结构
    DataScanResult        - 统一数据扫描结果

数据扫描：
    UnifiedDataScanner    - 消除4处重复扫描逻辑的统一扫描器
"""

from .base_strategy import (
    LearningStrategyType,
    BaseLearningStrategy,
    LearningResult,
    DataScanResult,
)
from .data_scanner import UnifiedDataScanner
from .daily_strategy import DailyLearningStrategy
from .three_tier_strategy import ThreeTierLearningStrategy
from .enhanced_strategy import EnhancedLearningStrategy
from .solution_strategy import SolutionLearningStrategy
from .feedback_strategy import FeedbackLoopStrategy

__all__ = [
    # 类型 & 基类
    "LearningStrategyType",
    "BaseLearningStrategy",
    "LearningResult",
    "DataScanResult",
    # 扫描器
    "UnifiedDataScanner",
    # 策略实现
    "DailyLearningStrategy",
    "ThreeTierLearningStrategy",
    "EnhancedLearningStrategy",
    "SolutionLearningStrategy",
    "FeedbackLoopStrategy",
]

# 策略注册表（类型 → 实现类）
STRATEGY_REGISTRY = {
    LearningStrategyType.DAILY: DailyLearningStrategy,
    LearningStrategyType.THREE_TIER: ThreeTierLearningStrategy,
    LearningStrategyType.ENHANCED: EnhancedLearningStrategy,
    LearningStrategyType.SOLUTION: SolutionLearningStrategy,
    LearningStrategyType.FEEDBACK: FeedbackLoopStrategy,
}
