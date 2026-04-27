"""
__all__ = [
    'generate_execution_params',
    'generate_report',
    'get_crisis_strategy',
    'get_exploration_strategy',
    'get_growth_strategy',
    'get_stable_strategy',
    'get_transition_strategy',
    'identify_scenario',
    'optimize_strategy_parameters',
    'select_strategy',
    'to_dict',
]

动态学习strategy引擎 - Dynamic Learning Strategy Engine
根据场景动态调整学习strategy,替代硬编码参数

核心设计:
1. 场景recognize - 自动recognize当前学习环境和需求
2. strategy库 - 预定义的最优strategy
3. 智能匹配 - 将场景mapping到最适合的strategy
4. 自适应优化 - 根据实际结果反馈优化strategy
5. 参数generate - 为strategygenerate具体的执行参数

场景类型:
- STABLE: 稳定期 (数据充足,变化不大)
- GROWTH: 增长期 (数据增加,需要深度学习)
- CRISIS: 危机期 (数据稀缺,需要采集)
- TRANSITION: 转变期 (数据characteristics变化,需要适应)
- EXPLORATION: 探索期 (新领域,需要广泛学习)
"""

import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ScenarioType(Enum):
    """学习场景类型"""
    STABLE = "稳定"         # 数据充足,变化稳定,优先本地
    GROWTH = "增长"         # 数据增加,快速变化,本地+网络结合
    CRISIS = "危机"         # 数据缺失,需要应急,网络优先
    TRANSITION = "转变"     # characteristics变化,需要适应,双向学习
    EXPLORATION = "探索"    # 新领域,需要广泛学习,网络为主

class DataCharacteristic(Enum):
    """数据characteristics"""
    SUFFICIENT = "充足"     # 数据量充足
    LIMITED = "有限"        # 数据量有限
    SCARCE = "稀缺"        # 数据稀缺
    EXPLOSIVE = "爆发"      # 数据爆发
    EMERGING = "新兴"       # 新兴领域

@dataclass
class ScenarioContext:
    """场景上下文"""
    scenario_type: ScenarioType
    identified_at: datetime
    characteristics: List[DataCharacteristic]
    
    # 量化metrics
    local_data_count: int                  # 本地数据数量
    local_data_growth_rate: float          # 本地数据增长率
    network_availability: float            # 网络可用性 0-1
    data_quality_trend: str                # 数据质量趋势 (improving/stable/declining)
    
    # 学习目标
    priority: str                          # 优先级 (high/medium/low)
    urgency: str                           # 紧迫性 (urgent/normal/relaxed)
    depth_requirement: str                 # 深度要求 (deep/medium/shallow)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "scenario_type": self.scenario_type.value,
            "identified_at": self.identified_at.isoformat(),
            "characteristics": [c.value for c in self.characteristics],
            "local_data_count": self.local_data_count,
            "local_data_growth_rate": self.local_data_growth_rate,
            "network_availability": self.network_availability,
            "data_quality_trend": self.data_quality_trend,
            "priority": self.priority,
            "urgency": self.urgency,
            "depth_requirement": self.depth_requirement,
        }

@dataclass
class LearningStrategy:
    """学习strategy"""
    name: str                              # strategy名称
    scenario: ScenarioType                 # 适用场景
    description: str                       # strategy描述
    
    # 参数配置
    local_learning_enabled: bool           # 是否启用本地学习
    network_learning_enabled: bool         # 是否启用网络学习
    cross_learning_enabled: bool           # 是否启用交叉学习
    
    local_data_threshold: int              # 本地数据阈值
    network_data_target: int               # 网络数据目标数量
    cross_trigger_threshold: int           # 交叉fusion触发阈值
    
    local_priority_weight: float           # 本地权重 0-1
    network_priority_weight: float         # 网络权重 0-1
    
    research_depth: str                    # 研究深度 (shallow/medium/deep)
    research_breadth: str                  # 研究广度 (narrow/medium/wide)
    
    data_quality_threshold: float          # 数据质量阈值 0-1
    authority_requirement: str             # 权威性要求 (strict/moderate/flexible)
    
    max_execution_time: int                # 最大执行时间 (秒)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "name": self.name,
            "scenario": self.scenario.value,
            "description": self.description,
            "local_learning_enabled": self.local_learning_enabled,
            "network_learning_enabled": self.network_learning_enabled,
            "cross_learning_enabled": self.cross_learning_enabled,
            "local_data_threshold": self.local_data_threshold,
            "network_data_target": self.network_data_target,
            "cross_trigger_threshold": self.cross_trigger_threshold,
            "local_priority_weight": self.local_priority_weight,
            "network_priority_weight": self.network_priority_weight,
            "research_depth": self.research_depth,
            "research_breadth": self.research_breadth,
            "data_quality_threshold": self.data_quality_threshold,
            "authority_requirement": self.authority_requirement,
            "max_execution_time": self.max_execution_time,
        }

class StrategyLibrary:
    """strategy库 - 预定义的最优strategy"""
    
    @staticmethod
    def get_stable_strategy() -> LearningStrategy:
        """稳定期strategy - 数据充足,变化不大"""
        return LearningStrategy(
            name="稳定期strategy (Stable Strategy)",
            scenario=ScenarioType.STABLE,
            description="数据充足,优先本地深度学习,网络作为补充",
            
            local_learning_enabled=True,
            network_learning_enabled=True,
            cross_learning_enabled=True,
            
            local_data_threshold=5,        # 只需5条触发
            network_data_target=3,         # 网络作为补充
            cross_trigger_threshold=3,     # 容易触发交叉
            
            local_priority_weight=0.7,     # 本地70%
            network_priority_weight=0.3,   # 网络30%
            
            research_depth="deep",         # 深度学习
            research_breadth="medium",     # 中等广度
            
            data_quality_threshold=0.75,   # 质量要求75%+
            authority_requirement="moderate",  # 中等权威性
            
            max_execution_time=300,        # 5分钟
        )
    
    @staticmethod
    def get_growth_strategy() -> LearningStrategy:
        """增长期strategy - 数据增加,快速变化"""
        return LearningStrategy(
            name="增长期strategy (Growth Strategy)",
            scenario=ScenarioType.GROWTH,
            description="数据增加,均衡本地网络学习,关注趋势和模式",
            
            local_learning_enabled=True,
            network_learning_enabled=True,
            cross_learning_enabled=True,
            
            local_data_threshold=10,       # 需要更多本地数据
            network_data_target=8,         # 网络数据增加
            cross_trigger_threshold=5,     # 更容易触发交叉
            
            local_priority_weight=0.5,     # 本地50%
            network_priority_weight=0.5,   # 网络50%
            
            research_depth="medium",       # 中等深度
            research_breadth="wide",       # 宽广度
            
            data_quality_threshold=0.70,   # 质量要求70%+
            authority_requirement="moderate",
            
            max_execution_time=600,        # 10分钟
        )
    
    @staticmethod
    def get_crisis_strategy() -> LearningStrategy:
        """危机期strategy - 数据缺失,需要应急"""
        return LearningStrategy(
            name="危机期strategy (Crisis Strategy)",
            scenario=ScenarioType.CRISIS,
            description="数据缺失,优先网络采集,快速应对",
            
            local_learning_enabled=False,   # 禁用本地 (无数据)
            network_learning_enabled=True,
            cross_learning_enabled=False,   # 禁用交叉 (无本地)
            
            local_data_threshold=1,         # 任何数据都用
            network_data_target=20,         # 大量网络数据
            cross_trigger_threshold=10,
            
            local_priority_weight=0.0,      # 本地0%
            network_priority_weight=1.0,    # 网络100%
            
            research_depth="shallow",       # 浅度学习 (快速)
            research_breadth="wide",        # 宽广度 (全面)
            
            data_quality_threshold=0.50,    # 质量要求50%+ (宽松)
            authority_requirement="flexible",
            
            max_execution_time=180,         # 3分钟 (快速)
        )
    
    @staticmethod
    def get_transition_strategy() -> LearningStrategy:
        """转变期strategy - characteristics变化,需要适应"""
        return LearningStrategy(
            name="转变期strategy (Transition Strategy)",
            scenario=ScenarioType.TRANSITION,
            description="characteristics变化,双向学习,快速适应新环境",
            
            local_learning_enabled=True,
            network_learning_enabled=True,
            cross_learning_enabled=True,
            
            local_data_threshold=3,        # 低阈值
            network_data_target=12,        # 更多网络数据
            cross_trigger_threshold=2,     # 容易触发交叉
            
            local_priority_weight=0.4,     # 本地40%
            network_priority_weight=0.6,   # 网络60%
            
            research_depth="medium",
            research_breadth="wide",       # 宽广度 (适应新环境)
            
            data_quality_threshold=0.65,   # 质量要求65%+
            authority_requirement="moderate",
            
            max_execution_time=900,        # 15分钟 (充分探索)
        )
    
    @staticmethod
    def get_exploration_strategy() -> LearningStrategy:
        """探索期strategy - 新领域,需要广泛学习"""
        return LearningStrategy(
            name="探索期strategy (Exploration Strategy)",
            scenario=ScenarioType.EXPLORATION,
            description="新领域,以网络广泛学习为主,建立知识基础",
            
            local_learning_enabled=False,   # 新领域无本地数据
            network_learning_enabled=True,
            cross_learning_enabled=False,
            
            local_data_threshold=1,
            network_data_target=25,        # 大量网络学习
            cross_trigger_threshold=15,
            
            local_priority_weight=0.0,
            network_priority_weight=1.0,   # 100% 网络
            
            research_depth="medium",       # 中等深度 (构建框架)
            research_breadth="wide",       # 宽广度 (多维探索)
            
            data_quality_threshold=0.60,   # 质量要求60%+
            authority_requirement="moderate",
            
            max_execution_time=1200,       # 20分钟 (深入探索)
        )

class DynamicStrategyEngine:
    """动态学习strategy引擎"""
    
    def __init__(self):
        """initstrategy引擎"""
        self.strategy_library = StrategyLibrary()
        self.scenario_history: List[ScenarioContext] = []
        self.strategy_history: List[Tuple[ScenarioContext, LearningStrategy]] = []
        self.strategy_performance: Dict[str, Dict] = {}
        
    def identify_scenario(self,
                         local_data_count: int,
                         local_data_growth_rate: float,
                         network_availability: float,
                         data_quality_trend: str,
                         priority: str = "medium",
                         urgency: str = "normal",
                         depth_requirement: str = "medium") -> ScenarioContext:
        """
        recognize当前学习场景
        
        Args:
            local_data_count: 本地数据数量
            local_data_growth_rate: 本地数据增长率
            network_availability: 网络可用性 (0-1)
            data_quality_trend: 数据质量趋势
            priority: 优先级
            urgency: 紧迫性
            depth_requirement: 深度要求
            
        Returns:
            场景上下文
        """
        characteristics = []
        
        # recognize数据characteristics
        if local_data_count == 0:
            characteristics.append(DataCharacteristic.SCARCE)
        elif local_data_count < 5:
            characteristics.append(DataCharacteristic.LIMITED)
        else:
            characteristics.append(DataCharacteristic.SUFFICIENT)
        
        if local_data_growth_rate > 0.5:  # 增长率>50%
            characteristics.append(DataCharacteristic.EXPLOSIVE)
        elif local_data_growth_rate > 0.1:  # 增长率>10%
            characteristics.append(DataCharacteristic.EMERGING)
        
        # recognize场景类型
        scenario_type = self._map_to_scenario(
            local_data_count,
            local_data_growth_rate,
            network_availability,
            urgency,
            depth_requirement
        )
        
        context = ScenarioContext(
            scenario_type=scenario_type,
            identified_at=datetime.now(),
            characteristics=characteristics,
            local_data_count=local_data_count,
            local_data_growth_rate=local_data_growth_rate,
            network_availability=network_availability,
            data_quality_trend=data_quality_trend,
            priority=priority,
            urgency=urgency,
            depth_requirement=depth_requirement,
        )
        
        self.scenario_history.append(context)
        logger.info(f"场景recognize完成: {scenario_type.value}")
        
        return context
    
    def _map_to_scenario(self,
                        local_data_count: int,
                        growth_rate: float,
                        network_avail: float,
                        urgency: str,
                        depth: str) -> ScenarioType:
        """将metricsmapping到场景类型"""
        
        # 危机judge (数据缺失 + 紧急)
        if local_data_count == 0 and urgency == "urgent":
            return ScenarioType.CRISIS
        
        # 探索judge (无本地数据 + 非紧急)
        if local_data_count == 0 and urgency != "urgent":
            return ScenarioType.EXPLORATION
        
        # 增长judge (快速增长)
        if growth_rate > 0.3:
            return ScenarioType.GROWTH
        
        # 转变judge (缓慢增长 + 深度要求)
        if 0.1 <= growth_rate <= 0.3 and depth in ["deep", "medium"]:
            return ScenarioType.TRANSITION
        
        # 默认稳定
        return ScenarioType.STABLE
    
    def select_strategy(self, scenario: ScenarioContext) -> LearningStrategy:
        """
        根据场景选择最优strategy
        
        Args:
            scenario: 场景上下文
            
        Returns:
            学习strategy
        """
        strategy_map = {
            ScenarioType.STABLE: self.strategy_library.get_stable_strategy,
            ScenarioType.GROWTH: self.strategy_library.get_growth_strategy,
            ScenarioType.CRISIS: self.strategy_library.get_crisis_strategy,
            ScenarioType.TRANSITION: self.strategy_library.get_transition_strategy,
            ScenarioType.EXPLORATION: self.strategy_library.get_exploration_strategy,
        }
        
        strategy_getter = strategy_map.get(scenario.scenario_type)
        if strategy_getter:
            strategy = strategy_getter()
        else:
            strategy = self.strategy_library.get_stable_strategy()
        
        # 记录strategy选择
        self.strategy_history.append((scenario, strategy))
        logger.info(f"strategy选择: {strategy.name}")
        
        return strategy
    
    def optimize_strategy_parameters(self,
                                    strategy: LearningStrategy,
                                    learning_insights: Dict[str, Any]) -> LearningStrategy:
        """
        根据学习洞察优化strategy参数
        
        Args:
            strategy: 原始strategy
            learning_insights: 学习洞察,包含:
                - average_data_quality: 平均数据质量
                - local_coverage_rate: 本地覆盖率
                - network_value_rate: 网络价值率
                - new_patterns_found: 发现新模式数
                - execution_time: 执行时间
                
        Returns:
            优化后的strategy
        """
        optimized = strategy
        
        avg_quality = learning_insights.get("average_data_quality", 0.7)
        local_coverage = learning_insights.get("local_coverage_rate", 0.5)
        network_value = learning_insights.get("network_value_rate", 0.5)
        new_patterns = learning_insights.get("new_patterns_found", 0)
        exec_time = learning_insights.get("execution_time", 0)
        
        # 优化阈值 (正向调整)
        # 如果本地数据质量高,可以提高阈值
        if avg_quality > 0.85:
            optimized.local_data_threshold = max(3, optimized.local_data_threshold - 2)
        
        # 如果网络数据价值高,增加网络目标
        if network_value > 0.75:
            optimized.network_data_target = int(optimized.network_data_target * 1.2)
        
        # 如果发现多个新模式,增加深度
        if new_patterns > 3:
            if optimized.research_depth == "shallow":
                optimized.research_depth = "medium"
            elif optimized.research_depth == "medium":
                optimized.research_depth = "deep"
        
        # 如果执行时间过长,降低广度
        if exec_time > optimized.max_execution_time * 0.9:
            if optimized.research_breadth == "wide":
                optimized.research_breadth = "medium"
        
        # 调整权重
        if local_coverage > 0.8:
            optimized.local_priority_weight = min(0.9, optimized.local_priority_weight + 0.1)
        
        if network_value > 0.8:
            optimized.network_priority_weight = min(0.9, optimized.network_priority_weight + 0.1)
        
        # 规范化权重
        total = optimized.local_priority_weight + optimized.network_priority_weight
        optimized.local_priority_weight /= total
        optimized.network_priority_weight /= total
        
        logger.info(f"strategy参数已优化: {strategy.name}")
        return optimized
    
    def generate_execution_params(self, strategy: LearningStrategy) -> Dict[str, Any]:
        """
        generate具体的执行参数
        
        Args:
            strategy: 学习strategy
            
        Returns:
            执行参数字典
        """
        return {
            "local_learning": strategy.local_learning_enabled,
            "network_learning": strategy.network_learning_enabled,
            "cross_learning": strategy.cross_learning_enabled,
            "local_data_threshold": strategy.local_data_threshold,
            "network_data_target": strategy.network_data_target,
            "cross_trigger_threshold": strategy.cross_trigger_threshold,
            "local_priority": strategy.local_priority_weight,
            "network_priority": strategy.network_priority_weight,
            "research_depth": strategy.research_depth,
            "research_breadth": strategy.research_breadth,
            "min_data_quality": strategy.data_quality_threshold,
            "authority_requirement": strategy.authority_requirement,
            "max_time_seconds": strategy.max_execution_time,
        }
    
    def generate_report(self) -> Dict:
        """generatestrategy引擎报告"""
        return {
            "timestamp": datetime.now().isoformat(),
            "scenarios_identified": len(self.scenario_history),
            "strategies_used": len(self.strategy_history),
            "latest_scenario": self.scenario_history[-1].to_dict() if self.scenario_history else None,
            "latest_strategy": self.strategy_history[-1][1].to_dict() if self.strategy_history else None,
            "scenario_distribution": self._get_scenario_distribution(),
        }
    
    def _get_scenario_distribution(self) -> Dict[str, int]:
        """get场景分布"""
        dist = {}
        for context in self.scenario_history:
            scenario_name = context.scenario_type.value
            dist[scenario_name] = dist.get(scenario_name, 0) + 1
        return dist

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
