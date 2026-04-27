"""
__all__ = [
    'collect_module_data',
    'export_insights',
    'generate_insights',
    'get_cross_module_insight_generator',
    'get_high_impact_insights',
    'get_insight_statistics',
    'get_insights_by_module',
    'get_insights_by_type',
    'to_dict',
]

跨模块洞察生成模块

整合多个模块的数据生成系统性洞察
"""

from typing import Dict, List, Any, Optional, Callable, Set
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class InsightType(Enum):
    """洞察类型"""
    PATTERN = "pattern"           # 模式识别
    ANOMALY = "anomaly"           # 异常检测
    TREND = "trend"               # 趋势分析
    CORRELATION = "correlation"   # 关联分析
    PREDICTION = "prediction"     # 预测洞察
    OPTIMIZATION = "optimization" # 优化建议

class ModuleSource(Enum):
    """模块来源"""
    EVOLUTION = "evolution_engine"
    KNOWLEDGE = "knowledge_graph"
    GROWTH = "growth_strategies"
    AUTONOMY = "autonomous_agent"
    LEARNING = "learning_coord"
    MEMORY = "neural_memory"
    WISDOM = "wisdom_dispatcher"
    FEEDBACK = "feedback_loop"

@dataclass
class CrossModuleInsight:
    """跨模块洞察"""
    insight_id: str
    insight_type: InsightType
    title: str
    description: str
    source_modules: List[ModuleSource]
    confidence: float
    evidence: List[Dict]
    recommendations: List[Dict]
    impact_score: float
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "insight_id": self.insight_id,
            "insight_type": self.insight_type.value,
            "title": self.title,
            "description": self.description,
            "source_modules": [m.value for m in self.source_modules],
            "confidence": self.confidence,
            "evidence": self.evidence,
            "recommendations": self.recommendations,
            "impact_score": self.impact_score,
            "created_at": self.created_at.isoformat()
        }

@dataclass
class ModuleData:
    """模块数据"""
    module: ModuleSource
    data: Dict[str, Any]
    timestamp: datetime
    reliability: float

class CrossModuleInsightGenerator:
    """
    跨模块洞察生成器
    
    整合多个模块的数据生成系统性洞察：
    1. 数据收集与标准化
    2. 模式识别与关联分析
    3. 洞察生成与验证
    4. 推荐生成与优先级排序
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = Path(storage_path) if storage_path else Path("data/cross_module_insights")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self._insights: List[CrossModuleInsight] = []
        self._module_data_buffer: Dict[ModuleSource, List[ModuleData]] = {}
        self._pattern_detectors: Dict[str, Callable] = {}
        
        self._initialize_detectors()
    
    def _initialize_detectors(self):
        """初始化模式检测器"""
        self._pattern_detectors = {
            "performance_correlation": self._detect_performance_correlation,
            "learning_efficiency": self._detect_learning_efficiency,
            "strategy_effectiveness": self._detect_strategy_effectiveness,
            "autonomy_feedback_loop": self._detect_autonomy_feedback_loop,
            "knowledge_growth_synergy": self._detect_knowledge_growth_synergy,
        }
    
    def collect_module_data(self, module: ModuleSource, data: Dict[str, Any],
                           reliability: float = 0.8):
        """收集模块数据"""
        module_data = ModuleData(
            module=module,
            data=data,
            timestamp=datetime.now(),
            reliability=reliability
        )
        
        if module not in self._module_data_buffer:
            self._module_data_buffer[module] = []
        
        self._module_data_buffer[module].append(module_data)
        
        # 限制缓冲区大小
        if len(self._module_data_buffer[module]) > 100:
            self._module_data_buffer[module] = self._module_data_buffer[module][-100:]
    
    def generate_insights(self, target_modules: Optional[List[ModuleSource]] = None) -> List[CrossModuleInsight]:
        """
        生成跨模块洞察
        
        Args:
            target_modules: 目标模块列表，None表示所有模块
            
        Returns:
            生成的洞察列表
        """
        new_insights = []
        
        # 确定要分析的模块
        modules = target_modules or list(self._module_data_buffer.keys())
        
        # 运行所有模式检测器
        for detector_name, detector in self._pattern_detectors.items():
            try:
                insight = detector(modules)
                if insight:
                    new_insights.append(insight)
                    self._insights.append(insight)
            except Exception as e:
                logger.warning(f"检测器 {detector_name} 执行失败: {e}")
        
        return new_insights
    
    def _detect_performance_correlation(self, modules: List[ModuleSource]) -> Optional[CrossModuleInsight]:
        """检测性能关联"""
        # 检查是否有进化引擎和增长策略的数据
        evolution_data = self._get_latest_data(ModuleSource.EVOLUTION)
        growth_data = self._get_latest_data(ModuleSource.GROWTH)
        
        if not evolution_data or not growth_data:
            return None
        
        # 分析性能指标关联
        evolution_metrics = evolution_data.data.get("metrics", {})
        growth_metrics = growth_data.data.get("metrics", {})
        
        # 简单的关联检测
        correlation_score = self._calculate_correlation(evolution_metrics, growth_metrics)
        
        if correlation_score > 0.6:
            return CrossModuleInsight(
                insight_id=f"insight_perf_corr_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                insight_type=InsightType.CORRELATION,
                title="进化引擎与增长策略性能正相关",
                description=f"检测到进化优化与增长策略效果存在强关联（相关系数: {correlation_score:.2f}）",
                source_modules=[ModuleSource.EVOLUTION, ModuleSource.GROWTH],
                confidence=correlation_score,
                evidence=[
                    {"source": "evolution", "metrics": evolution_metrics},
                    {"source": "growth", "metrics": growth_metrics}
                ],
                recommendations=[
                    {"type": "optimization", "action": "同步优化进化引擎和增长策略参数"},
                    {"type": "monitoring", "action": "建立联合性能监控面板"}
                ],
                impact_score=0.8
            )
        
        return None
    
    def _detect_learning_efficiency(self, modules: List[ModuleSource]) -> Optional[CrossModuleInsight]:
        """检测学习效率"""
        learning_data = self._get_latest_data(ModuleSource.LEARNING)
        memory_data = self._get_latest_data(ModuleSource.MEMORY)
        
        if not learning_data:
            return None
        
        learning_stats = learning_data.data.get("statistics", {})
        q_updates = learning_stats.get("q_value_updates", 0)
        feedback_count = learning_stats.get("feedback_count", 0)
        
        # 检测学习效率
        if feedback_count > 0:
            efficiency = q_updates / feedback_count
            
            if efficiency < 0.3:
                return CrossModuleInsight(
                    insight_id=f"insight_learning_eff_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    insight_type=InsightType.OPTIMIZATION,
                    title="学习效率偏低，建议优化反馈处理",
                    description=f"学习效率指标为 {efficiency:.2f}，低于预期阈值（0.3），建议检查反馈采集机制",
                    source_modules=[ModuleSource.LEARNING, ModuleSource.FEEDBACK],
                    confidence=0.75,
                    evidence=[
                        {"q_updates": q_updates, "feedback_count": feedback_count, "efficiency": efficiency}
                    ],
                    recommendations=[
                        {"type": "optimization", "action": "优化反馈采集点的触发频率"},
                        {"type": "configuration", "action": "调整学习率和探索参数"}
                    ],
                    impact_score=0.7
                )
        
        return None
    
    def _detect_strategy_effectiveness(self, modules: List[ModuleSource]) -> Optional[CrossModuleInsight]:
        """检测策略有效性"""
        wisdom_data = self._get_latest_data(ModuleSource.WISDOM)
        feedback_data = self._get_latest_data(ModuleSource.FEEDBACK)
        
        if not wisdom_data or not feedback_data:
            return None
        
        # 分析策略推荐与实际效果的匹配度
        recommendations = wisdom_data.data.get("recommendations", [])
        feedback_results = feedback_data.data.get("results", [])
        
        # 计算策略有效性
        if recommendations and feedback_results:
            match_count = sum(1 for r in recommendations if r.get("adopted", False))
            effectiveness = match_count / len(recommendations) if recommendations else 0
            
            if effectiveness < 0.5:
                return CrossModuleInsight(
                    insight_id=f"insight_strategy_eff_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    insight_type=InsightType.OPTIMIZATION,
                    title="智慧学派推荐采纳率偏低",
                    description=f"策略推荐采纳率为 {effectiveness:.1%}，建议优化推荐算法或增强解释性",
                    source_modules=[ModuleSource.WISDOM, ModuleSource.FEEDBACK],
                    confidence=0.8,
                    evidence=[
                        {"recommendations": len(recommendations), "adopted": match_count, "effectiveness": effectiveness}
                    ],
                    recommendations=[
                        {"type": "algorithm", "action": "优化学派选择和融合算法"},
                        {"type": "ux", "action": "增强策略推荐理由的展示"}
                    ],
                    impact_score=0.85
                )
        
        return None
    
    def _detect_autonomy_feedback_loop(self, modules: List[ModuleSource]) -> Optional[CrossModuleInsight]:
        """检测自主-反馈循环"""
        autonomy_data = self._get_latest_data(ModuleSource.AUTONOMY)
        feedback_data = self._get_latest_data(ModuleSource.FEEDBACK)
        
        if not autonomy_data or not feedback_data:
            return None
        
        # 检测自主决策与反馈的闭环
        decisions = autonomy_data.data.get("decisions", [])
        feedbacks = feedback_data.data.get("feedbacks", [])
        
        # 检查闭环完整性
        if decisions and feedbacks:
            decision_ids = set(d.get("id") for d in decisions)
            feedback_refs = set(f.get("decision_ref") for f in feedbacks)
            
            covered = len(decision_ids & feedback_refs)
            coverage = covered / len(decision_ids) if decision_ids else 0
            
            if coverage < 0.7:
                return CrossModuleInsight(
                    insight_id=f"insight_autonomy_loop_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    insight_type=InsightType.PATTERN,
                    title="自主-反馈闭环覆盖率不足",
                    description=f"仅有 {coverage:.1%} 的自主决策有对应反馈，建议加强反馈采集",
                    source_modules=[ModuleSource.AUTONOMY, ModuleSource.FEEDBACK],
                    confidence=0.85,
                    evidence=[
                        {"decisions": len(decision_ids), "with_feedback": covered, "coverage": coverage}
                    ],
                    recommendations=[
                        {"type": "integration", "action": "强化自主层与反馈层的自动联动"},
                        {"type": "automation", "action": "设置默认反馈采集点"}
                    ],
                    impact_score=0.9
                )
        
        return None
    
    def _detect_knowledge_growth_synergy(self, modules: List[ModuleSource]) -> Optional[CrossModuleInsight]:
        """检测知识与增长协同"""
        knowledge_data = self._get_latest_data(ModuleSource.KNOWLEDGE)
        growth_data = self._get_latest_data(ModuleSource.GROWTH)
        
        if not knowledge_data or not growth_data:
            return None
        
        # 检测知识图谱更新与增长策略的协同
        knowledge_updates = knowledge_data.data.get("updates", [])
        growth_experiments = growth_data.data.get("experiments", [])
        
        if knowledge_updates and growth_experiments:
            # 检查知识更新是否驱动了增长实验
            knowledge_driven = sum(1 for e in growth_experiments if e.get("knowledge_based", False))
            synergy_rate = knowledge_driven / len(growth_experiments) if growth_experiments else 0
            
            if synergy_rate > 0.6:
                return CrossModuleInsight(
                    insight_id=f"insight_kg_synergy_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    insight_type=InsightType.PATTERN,
                    title="知识-增长协同效应显著",
                    description=f"{synergy_rate:.1%} 的增长实验基于知识图谱洞察，协同效应良好",
                    source_modules=[ModuleSource.KNOWLEDGE, ModuleSource.GROWTH],
                    confidence=0.8,
                    evidence=[
                        {"knowledge_updates": len(knowledge_updates), 
                         "growth_experiments": len(growth_experiments),
                         "knowledge_driven": knowledge_driven}
                    ],
                    recommendations=[
                        {"type": "enhancement", "action": "进一步强化知识图谱到增长策略的自动流转"},
                        {"type": "automation", "action": "建立知识更新自动触发增长实验的机制"}
                    ],
                    impact_score=0.75
                )
        
        return None
    
    def _get_latest_data(self, module: ModuleSource) -> Optional[ModuleData]:
        """获取模块最新数据"""
        if module not in self._module_data_buffer:
            return None
        
        data_list = self._module_data_buffer[module]
        if not data_list:
            return None
        
        return max(data_list, key=lambda x: x.timestamp)
    
    def _calculate_correlation(self, metrics1: Dict, metrics2: Dict) -> float:
        """计算指标关联度（简化版）"""
        # 提取数值指标
        values1 = [v for v in metrics1.values() if isinstance(v, (int, float))]
        values2 = [v for v in metrics2.values() if isinstance(v, (int, float))]
        
        if not values1 or not values2:
            return 0.0
        
        # 简化的相关性计算
        avg1 = sum(values1) / len(values1) if values1 else 0
        avg2 = sum(values2) / len(values2) if values2 else 0
        
        # 返回基于平均值差异的相似度
        diff = abs(avg1 - avg2) / max(avg1, avg2, 1)
        return max(0, 1 - diff)
    
    def get_insights_by_type(self, insight_type: InsightType, 
                            limit: int = 10) -> List[CrossModuleInsight]:
        """按类型获取洞察"""
        filtered = [i for i in self._insights if i.insight_type == insight_type]
        return sorted(filtered, key=lambda x: x.created_at, reverse=True)[:limit]
    
    def get_insights_by_module(self, module: ModuleSource,
                              limit: int = 10) -> List[CrossModuleInsight]:
        """按模块获取洞察"""
        filtered = [i for i in self._insights if module in i.source_modules]
        return sorted(filtered, key=lambda x: x.created_at, reverse=True)[:limit]
    
    def get_high_impact_insights(self, threshold: float = 0.8) -> List[CrossModuleInsight]:
        """获取高影响洞察"""
        return [i for i in self._insights if i.impact_score >= threshold]
    
    def export_insights(self, filepath: Optional[str] = None) -> str:
        """导出洞察到文件"""
        if filepath is None:
            filepath = self.storage_path / f"insights_{datetime.now().strftime('%Y%m%d')}.json"
        
        data = {
            "export_time": datetime.now().isoformat(),
            "total_insights": len(self._insights),
            "insights": [i.to_dict() for i in self._insights]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return str(filepath)
    
    def get_insight_statistics(self) -> Dict:
        """获取洞察统计"""
        if not self._insights:
            return {"total": 0}
        
        type_counts = {}
        module_counts = {}
        
        for insight in self._insights:
            # 类型统计
            t = insight.insight_type.value
            type_counts[t] = type_counts.get(t, 0) + 1
            
            # 模块统计
            for m in insight.source_modules:
                module_counts[m.value] = module_counts.get(m.value, 0) + 1
        
        return {
            "total": len(self._insights),
            "by_type": type_counts,
            "by_module": module_counts,
            "avg_confidence": sum(i.confidence for i in self._insights) / len(self._insights),
            "avg_impact": sum(i.impact_score for i in self._insights) / len(self._insights),
            "high_impact_count": len(self.get_high_impact_insights())
        }

# 全局生成器实例
_insight_generator: Optional[CrossModuleInsightGenerator] = None

def get_cross_module_insight_generator() -> CrossModuleInsightGenerator:
    """获取跨模块洞察生成器"""
    global _insight_generator
    if _insight_generator is None:
        _insight_generator = CrossModuleInsightGenerator()
    return _insight_generator
