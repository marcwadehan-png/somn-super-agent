"""
__all__ = [
    'execute_learning_cycle',
    'generate_comprehensive_report',
    'get_summary',
    'run_enhanced_three_tier_learning',
    'run_enhanced_three_tier_learning_v2',
]

增强型三层学习模型 - Enhanced Three-Tier Learning with AI Optimization
整合浏览器自动化,动态strategy,智能参数调整

核心流程:
1. 场景recognize → 动态strategy选择 → generate执行参数
2. 浏览器自动化采集网络数据 + 本地数据加载
3. 数据权威性评估和过滤
4. 性能评估 → 参数调整优化
5. 交叉fusiongenerate高价值洞察
6. 反馈循环改进

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  兼容层说明（v1.0 统一重构后）
本文件保留原始实现以确保现有调用链 100% 兼容。
新代码请使用：
    from .unified_learning_orchestrator import UnifiedLearningOrchestrator
    from .learning_strategies import LearningStrategyType
    orchestrator = UnifiedLearningOrchestrator()
    report = orchestrator.execute_daily(strategy_types=[LearningStrategyType.ENHANCED])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import json
import yaml
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
import logging

from .browser_automation_learning import (
    BrowserNetworkLearner, DataSourceValidator, BrowserLearningSession, DataPoint
)
from .dynamic_strategy_engine import DynamicStrategyEngine, ScenarioContext, LearningStrategy
from .intelligent_parameter_system import ParameterAdjustmentSystem, PerformanceMetrics

logger = logging.getLogger(__name__)

@dataclass
class EnhancedLearningSession:
    """增强型学习会话"""
    session_id: str
    start_time: datetime
    
    # 场景和strategy
    scenario: Optional[ScenarioContext] = None
    strategy: Optional[LearningStrategy] = None
    execution_params: Optional[Dict] = None
    
    # 学习过程
    browser_session: Optional[BrowserLearningSession] = None
    local_data_loaded: int = 0
    
    # 性能和优化
    performance_metrics: Optional[PerformanceMetrics] = None
    parameter_adjustments: List[Dict] = field(default_factory=list)
    
    # 结果
    valid_findings: List[DataPoint] = field(default_factory=list)
    invalid_findings: List[DataPoint] = field(default_factory=list)
    cross_insights: List[Dict] = field(default_factory=list)
    
    status: str = "active"  # active/completed/failed
    errors: List[str] = field(default_factory=list)
    
    def get_summary(self) -> Dict:
        """get会话摘要"""
        return {
            "session_id": self.session_id,
            "scenario": self.scenario.scenario_type.value if self.scenario else None,
            "strategy": self.strategy.name if self.strategy else None,
            "total_findings": len(self.valid_findings) + len(self.invalid_findings),
            "valid_findings": len(self.valid_findings),
            "invalid_findings": len(self.invalid_findings),
            "cross_insights": len(self.cross_insights),
            "local_data_loaded": self.local_data_loaded,
            "performance_score": self.performance_metrics.overall_score if self.performance_metrics else 0,
            "adjustments_made": len(self.parameter_adjustments),
            "status": self.status,
            "duration": (datetime.now() - self.start_time).total_seconds(),
        }

class EnhancedThreeTierLearner:
    """增强型三层学习器"""
    
    def __init__(self, data_dir: str = "data"):
        """init学习器"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # init子系统
        self.strategy_engine = DynamicStrategyEngine()
        self.browser_learner = BrowserNetworkLearner()
        self.parameter_system = ParameterAdjustmentSystem()
        
        # 会话历史
        self.session_history: List[EnhancedLearningSession] = []
    
    async def execute_learning_cycle(self,
                                     research_topic: str,
                                     target_sources: List[Dict[str, Any]],
                                     local_data_context: Dict[str, Any],
                                     priority: str = "medium",
                                     urgency: str = "normal") -> EnhancedLearningSession:
        """
        执行完整的学习循环
        
        Args:
            research_topic: 研究主题
            target_sources: 网络数据源列表
            local_data_context: 本地数据上下文
                - data_count: 本地数据数量
                - growth_rate: 增长率
                - quality_trend: 质量趋势
            priority: 优先级
            urgency: 紧迫性
            
        Returns:
            增强型学习会话
        """
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        session = EnhancedLearningSession(
            session_id=session_id,
            start_time=datetime.now(),
        )
        
        try:
            logger.info(f"开始增强型学习循环: {session_id}")
            logger.info(f"主题: {research_topic}")
            
            # ============ 第1阶段: 场景recognize和strategy选择 ============
            logger.info("[阶段1]场景recognize和strategy选择...")
            
            local_count = local_data_context.get("data_count", 0)
            growth_rate = local_data_context.get("growth_rate", 0.0)
            network_avail = local_data_context.get("network_availability", 0.95)
            quality_trend = local_data_context.get("quality_trend", "stable")
            
            # recognize场景
            scenario = self.strategy_engine.identify_scenario(
                local_data_count=local_count,
                local_data_growth_rate=growth_rate,
                network_availability=network_avail,
                data_quality_trend=quality_trend,
                priority=priority,
                urgency=urgency,
                depth_requirement="deep" if urgency == "urgent" else "medium"
            )
            session.scenario = scenario
            logger.info(f"✓ 场景recognize: {scenario.scenario_type.value}")
            
            # 选择strategy
            strategy = self.strategy_engine.select_strategy(scenario)
            session.strategy = strategy
            logger.info(f"✓ strategy选择: {strategy.name}")
            
            # generate执行参数
            exec_params = self.strategy_engine.generate_execution_params(strategy)
            session.execution_params = exec_params
            logger.info(f"✓ 执行参数generate完成")
            
            # ============ 第2阶段: 网络学习 (必须) ============
            logger.info("[阶段2]网络学习 (必须执行)...")
            
            if strategy.network_learning_enabled:
                browser_session = await self.browser_learner.learn_from_sources(
                    research_topic=research_topic,
                    target_sources=target_sources,
                    research_goal="通过浏览器自动化get权威网络数据"
                )
                session.browser_session = browser_session
                logger.info(f"✓ 网络学习完成: {len(browser_session.data_collected)} 条数据")
                
                # 分类数据
                for point in browser_session.data_collected:
                    if point.metadata.has_data_source and point.quality_score >= 0.60:
                        session.valid_findings.append(point)
                    else:
                        session.invalid_findings.append(point)
            
            # ============ 第3阶段: 本地学习 (可选) ============
            logger.info("[阶段3]本地学习 (可选)...")
            
            if strategy.local_learning_enabled and local_count >= strategy.local_data_threshold:
                logger.info(f"✓ 本地数据充足,执行本地学习")
                # 这里可以集成本地数据加载逻辑
                session.local_data_loaded = min(local_count, 50)
            else:
                logger.info(f"⊘ 本地学习跳过 (enabled={strategy.local_learning_enabled}, "
                           f"data={local_count}, threshold={strategy.local_data_threshold})")
            
            # ============ 第4阶段: 性能评估 ============
            logger.info("[阶段4]性能评估...")
            
            learning_results = {
                "data_points": [asdict(p) if isinstance(p, DataPoint) else p 
                               for p in session.valid_findings],
                "patterns": [],  # 这里可以添加模式recognize
                "insights": session.cross_insights,
                "execution_time": (datetime.now() - session.start_time).total_seconds(),
                "errors": session.errors,
            }
            
            metrics = self.parameter_system.record_learning_result(
                learning_results,
                exec_params
            )
            session.performance_metrics = metrics
            logger.info(f"✓ 性能评估: {metrics.overall_score:.2f} ({metrics.satisfaction_level})")
            
            # ============ 第5阶段: 参数调整优化 ============
            logger.info("[阶段5]参数调整优化...")
            
            adjusted_params, adjustments = self.parameter_system.adjust_parameters(
                exec_params,
                metrics,
                aggressive=urgency == "urgent"
            )
            
            if adjustments:
                for adj in adjustments:
                    session.parameter_adjustments.append({
                        "parameter": adj.parameter_name,
                        "old": adj.old_value,
                        "new": adj.new_value,
                        "reason": adj.reason,
                    })
                logger.info(f"✓ 参数调整: {len(adjustments)} 处修改")
            else:
                logger.info(f"✓ 参数优化: 无需调整")
            
            # ============ 第6阶段: 交叉fusion ============
            logger.info("[阶段6]交叉fusion...")
            
            if (strategy.cross_learning_enabled and 
                len(session.valid_findings) > 0 and 
                session.local_data_loaded > 0):
                
                cross_insights = self._perform_cross_learning(
                    session.valid_findings,
                    session.local_data_loaded
                )
                session.cross_insights = cross_insights
                logger.info(f"✓ 交叉fusion: {len(cross_insights)} 条洞察")
            else:
                logger.info(f"⊘ 交叉fusion跳过 (enabled={strategy.cross_learning_enabled}, "
                           f"network={len(session.valid_findings)}, local={session.local_data_loaded})")
            
            session.status = "completed"
            
        except Exception as e:
            logger.error(f"学习循环出错: {str(e)}")
            session.status = "failed"
            session.errors.append("执行失败")
        
        finally:
            self.session_history.append(session)
            logger.info(f"学习循环完成: {session.status}")
        
        return session
    
    def _perform_cross_learning(self,
                               network_findings: List[DataPoint],
                               local_data_count: int) -> List[Dict]:
        """执行交叉fusion学习"""
        insights = []
        
        # 分析网络数据的权威性分布
        authority_dist = {}
        for finding in network_findings:
            auth = finding.metadata.authority.value
            authority_dist[auth] = authority_dist.get(auth, 0) + 1
        
        # generate洞察
        if authority_dist.get("权威", 0) >= len(network_findings) * 0.5:
            insights.append({
                "type": "authority_positive",
                "content": "网络数据以权威来源为主,数据可信度高",
                "confidence": 0.95,
            })
        
        avg_quality = sum(f.quality_score for f in network_findings) / len(network_findings) if network_findings else 0
        if avg_quality >= 0.75:
            insights.append({
                "type": "quality_positive",
                "content": f"网络数据质量优良 (平均{avg_quality:.2f})",
                "confidence": 0.90,
            })
        
        if local_data_count > len(network_findings):
            insights.append({
                "type": "data_fusion",
                "content": f"本地数据({local_data_count}) > 网络数据({len(network_findings)}), "
                         f"建议优先使用本地数据,网络数据作为验证",
                "confidence": 0.85,
            })
        
        return insights
    
    def generate_comprehensive_report(self) -> Dict:
        """generatesynthesize报告"""
        if not self.session_history:
            return {"message": "暂无学习会话"}
        
        latest_session = self.session_history[-1]
        
        return {
            "timestamp": datetime.now().isoformat(),
            "session_summary": latest_session.get_summary(),
            "scenario_analysis": {
                "type": latest_session.scenario.scenario_type.value if latest_session.scenario else None,
                "characteristics": [c.value for c in (latest_session.scenario.characteristics or [])],
            },
            "strategy_used": {
                "name": latest_session.strategy.name if latest_session.strategy else None,
                "local_weight": latest_session.strategy.local_priority_weight if latest_session.strategy else 0,
                "network_weight": latest_session.strategy.network_priority_weight if latest_session.strategy else 0,
            },
            "data_quality": {
                "valid_findings": len(latest_session.valid_findings),
                "invalid_findings": len(latest_session.invalid_findings),
                "average_quality": latest_session.performance_metrics.average_quality if latest_session.performance_metrics else 0,
                "authority_distribution": (
                    latest_session.performance_metrics.authority_distribution 
                    if latest_session.performance_metrics else {}
                ),
            },
            "performance": {
                "score": latest_session.performance_metrics.overall_score if latest_session.performance_metrics else 0,
                "satisfaction": latest_session.performance_metrics.satisfaction_level if latest_session.performance_metrics else "unknown",
                "efficiency": latest_session.performance_metrics.learning_effectiveness if latest_session.performance_metrics else 0,
            },
            "optimizations": {
                "adjustments_count": len(latest_session.parameter_adjustments),
                "adjustments": latest_session.parameter_adjustments,
            },
            "cross_insights": latest_session.cross_insights,
        }

# 便利函数
async def run_enhanced_three_tier_learning(
    research_topic: str,
    target_sources: List[Dict],
    local_data_context: Dict,
    priority: str = "medium",
    urgency: str = "normal"
) -> EnhancedLearningSession:
    """运行增强型三层学习"""
    learner = EnhancedThreeTierLearner()
    return await learner.execute_learning_cycle(
        research_topic,
        target_sources,
        local_data_context,
        priority,
        urgency
    )

async def run_enhanced_three_tier_learning_v2(
    research_topic: str = "消费情绪与决策",
    target_sources: list = None,
    local_data_context: dict = None,
    priority: str = "normal",
    urgency: str = "normal"
):
    """
    新路由入口（推荐）：通过 UnifiedLearningOrchestrator 执行增强学习。
    保留 run_enhanced_three_tier_learning() 原有接口不变。
    """
    try:
        from .unified_learning_orchestrator import UnifiedLearningOrchestrator
        from .learning_strategies import LearningStrategyType
        orchestrator = UnifiedLearningOrchestrator()
        report = orchestrator.execute_daily(strategy_types=[LearningStrategyType.ENHANCED])
        return report
    except Exception as e:
        logger.warning(f"v2路由失败，回退到原始执行器: {e}")
        return await run_enhanced_three_tier_learning(
            research_topic, target_sources, local_data_context, priority, urgency
        )

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
