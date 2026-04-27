"""
__all__ = [
    'execute',
    'get_description',
    'local_count',
    'network_count',
    'should_execute',
    'strategy_type',
    'total',
    'total_events',
    'total_knowledge_updates',
]

基础策略接口与公共数据结构
Base strategy interface and common data structures for all learning strategies.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

class LearningStrategyType(Enum):
    """学习策略类型"""
    DAILY = "daily"                      # 每日学习（原 daily_learning.py）
    THREE_TIER = "three_tier"            # 三层融合（原 three_tier_learning.py）
    ENHANCED = "enhanced"                # 增强学习（原 enhanced_three_tier_learning.py）
    SOLUTION = "solution"                # 解决方案学习（原 solution_daily_learning.py）
    FEEDBACK = "feedback"                # 闭环学习（RL + Transfer）

class LearningPhase(Enum):
    """学习阶段"""
    DATA_SCAN = "数据扫描"
    INSTANCE_LEARNING = "实例学习"
    VALIDATION_LEARNING = "验证学习"
    ERROR_LEARNING = "错误学习"
    ASSOCIATION_LEARNING = "关联学习"
    FEEDBACK_INTEGRATION = "反馈整合"
    TRANSFER_LEARNING = "迁移学习"
    CROSS_FUSION = "交叉融合"
    REPORT_GENERATION = "报告生成"

@dataclass
class DataScanResult:
    """数据扫描结果（统一数据结构，消除 4 处重复）"""
    findings: List[Dict] = field(default_factory=list)
    validations: List[Dict] = field(default_factory=list)
    errors: List[Dict] = field(default_factory=list)
    learning_events: List[Dict] = field(default_factory=list)
    network_research: List[Dict] = field(default_factory=list)

    @property
    def total(self) -> int:
        return (len(self.findings) + len(self.validations) + len(self.errors)
                + len(self.learning_events) + len(self.network_research))

    @property
    def local_count(self) -> int:
        return len(self.findings) + len(self.validations) + len(self.learning_events)

    @property
    def network_count(self) -> int:
        return len(self.network_research)

@dataclass
class LearningResult:
    """学习执行结果"""
    success: bool = True
    strategy_type: str = ""
    execution_time: str = field(default_factory=lambda: datetime.now().strftime('%H:%M:%S'))
    duration_seconds: float = 0.0
    phases_completed: List[str] = field(default_factory=list)
    learning_events: List[Dict] = field(default_factory=list)
    new_patterns: List[Dict] = field(default_factory=list)
    confidence_updates: List[Dict] = field(default_factory=list)
    new_associations: List[Dict] = field(default_factory=list)
    rl_updates: List[Dict] = field(default_factory=list)
    transfer_hypotheses: List[Dict] = field(default_factory=list)
    registered_knowledge: List[Dict] = field(default_factory=list)
    cross_insights: List[Dict] = field(default_factory=list)
    error_messages: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    summary: str = ""
    extra: Dict = field(default_factory=dict)

    @property
    def total_events(self) -> int:
        return len(self.learning_events)

    @property
    def total_knowledge_updates(self) -> int:
        return (len(self.new_patterns) + len(self.confidence_updates)
                + len(self.new_associations))

class BaseLearningStrategy(ABC):
    """学习策略抽象基类"""

    def __init__(self, base_path: str = None):
        self.base_path = base_path

    @property
    @abstractmethod
    def strategy_type(self) -> LearningStrategyType:
        """策略类型标识"""
        ...

    @abstractmethod
    def execute(self, scan_result: DataScanResult, context: Dict[str, Any]) -> LearningResult:
        """
        执行学习策略

        Args:
            scan_result: 数据扫描结果
            context: 执行上下文（包含 neural_system, learning_engine 等）

        Returns:
            LearningResult: 学习结果
        """
        ...

    @abstractmethod
    def get_description(self) -> str:
        """策略描述"""
        ...

    def should_execute(self, scan_result: DataScanResult) -> bool:
        """判断是否应执行此策略（默认总有数据就执行）"""
        return scan_result.total > 0
