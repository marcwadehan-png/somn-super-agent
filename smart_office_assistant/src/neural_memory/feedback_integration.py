"""
__all__ = [
    'collect_adoption_signal',
    'collect_explicit_rating',
    'collect_feedback',
    'collect_implicit_signal',
    'generate_loop_report',
    'get_feedback_system',
    'get_loop_report',
    'get_loop_status',
    'process_pending_feedbacks',
    'register_callback',
    'reset_metrics',
    'submit_rating',
]

反馈整合模块 - Feedback Integration Module

将v8.4.2的反馈管道,ROI追踪,强化学习整合到生产环境
实现从反馈采集到strategy优化的全自动化闭环

版本: v1.0
日期: 2026-04-03
"""

import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging
import threading
import queue

from .feedback_pipeline import (
    FeedbackPipeline, FeedbackType, FeedbackSignal, NormalizedFeedback
)
from .roi_tracker import ROITracker, TaskLifecycle
from .reinforcement_trigger import ReinforcementTrigger
from .transfer_learner import TransferLearner

logger = logging.getLogger(__name__)

class IntegrationStatus(Enum):
    """整合状态"""
    IDLE = "idle"
    COLLECTING = "collecting"
    PROCESSING = "processing"
    LEARNING = "learning"
    APPLYING = "applying"
    ERROR = "error"

@dataclass
class FeedbackLoopMetrics:
    """反馈闭环metrics"""
    total_feedbacks: int = 0
    processed_feedbacks: int = 0
    pending_feedbacks: int = 0
    
    roi_tasks_tracked: int = 0
    rl_updates: int = 0
    transfer_hypotheses: int = 0
    
    avg_processing_time: float = 0.0
    success_rate: float = 0.0
    
    last_update: str = field(default_factory=lambda: datetime.now().isoformat())

class FeedbackIntegrationSystem:
    """
    反馈整合系统
    
    核心功能:
    1. unified反馈采集入口
    2. 自动路由到各子系统
    3. 触发学习引擎
    4. 应用学习到生产
    5. 监控闭环效果
    
    使用方式:
        fis = FeedbackIntegrationSystem()
        
        # 1. 采集反馈
        fis.collect_feedback(
            task_id="task_001",
            feedback_type=FeedbackType.RATING,
            value=5,
            context={"strategy": "私域运营"}
        )
        
        # 2. 自动处理(或定时触发)
        fis.process_pending_feedbacks()
        
        # 3. get闭环报告
        report = fis.generate_loop_report()
    """
    
    def __init__(self, base_path: str = None):
        from src.core.paths import LEARNING_DIR
        self.base_path = Path(base_path) if base_path else LEARNING_DIR / "feedback_integration"
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # init子系统
        self.feedback_pipeline = FeedbackPipeline(str(self.base_path))
        self.roi_tracker = ROITracker(str(self.base_path))
        self.rl_trigger = ReinforcementTrigger(str(self.base_path))
        self.transfer_learner = TransferLearner(str(self.base_path))
        
        # 状态管理
        self.status = IntegrationStatus.IDLE
        self.metrics = FeedbackLoopMetrics()
        self._load_metrics()
        
        # 处理队列
        self._processing_queue = queue.Queue()
        self._callbacks: List[Callable] = []
        
        # 配置
        self.config = self._load_config()
        
        logger.info("反馈整合系统init完成")
    
    def _load_config(self) -> Dict:
        """加载配置"""
        config_path = self.base_path / "config.yaml"
        default_config = {
            "auto_process": True,
            "batch_size": 10,
            "processing_interval": 300,  # 5分钟
            "confidence_threshold": 0.7,
            "min_feedback_for_rl": 5,
            "enable_transfer": True
        }
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return {**default_config, **yaml.safe_load(f)}
        
        return default_config
    
    def _load_metrics(self):
        """加载metrics"""
        metrics_path = self.base_path / "metrics.yaml"
        if metrics_path.exists():
            with open(metrics_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                self.metrics = FeedbackLoopMetrics(**data)
    
    def _save_metrics(self):
        """保存metrics"""
        self.metrics.last_update = datetime.now().isoformat()
        metrics_path = self.base_path / "metrics.yaml"
        with open(metrics_path, 'w', encoding='utf-8') as f:
            yaml.dump(asdict(self.metrics), f, allow_unicode=True)
    
    # ==================== 反馈采集接口 ====================
    
    def collect_feedback(
        self,
        task_id: str,
        feedback_type: FeedbackType,
        value: Any,
        context: Dict = None,
        user_id: str = "default",
        auto_process: bool = None
    ) -> str:
        """
        采集反馈
        
        Args:
            task_id: 任务ID
            feedback_type: 反馈类型
            value: 反馈值
            context: 上下文信息
            user_id: 用户ID
            auto_process: 是否自动处理
        
        Returns:
            feedback_id
        """
        context = context or {}
        
        # 构建原始反馈
        raw_feedback = {
            "type": feedback_type.value,
            "value": value,
            "context": context,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }
        
        # 提交到反馈管道
        feedback_id = self.feedback_pipeline.receive_feedback(
            task_id=task_id,
            raw_type=feedback_type.value,
            raw_value=value,
            context=context,
            user_id=user_id
        )
        
        # 更新metrics
        self.metrics.total_feedbacks += 1
        self.metrics.pending_feedbacks += 1
        self._save_metrics()
        
        logger.info(f"反馈已采集: {feedback_id} for task {task_id}")
        
        # 自动处理
        if auto_process or (auto_process is None and self.config["auto_process"]):
            self._schedule_processing()
        
        return feedback_id
    
    def collect_explicit_rating(
        self,
        task_id: str,
        rating: int,  # 1-5
        comment: str = "",
        context: Dict = None
    ) -> str:
        """
        采集显式评分
        
        快捷方法,用于采集用户评分反馈
        """
        context = context or {}
        context["comment"] = comment
        
        return self.collect_feedback(
            task_id=task_id,
            feedback_type=FeedbackType.RATING,
            value=rating,
            context=context
        )
    
    def collect_adoption_signal(
        self,
        task_id: str,
        adopted: bool,
        modifications: List[str] = None,
        context: Dict = None
    ) -> str:
        """
        采集采纳信号
        
        快捷方法,用于采集strategy采纳情况
        """
        context = context or {}
        context["modifications"] = modifications or []
        
        value = "adopted" if adopted else "rejected"
        
        return self.collect_feedback(
            task_id=task_id,
            feedback_type=FeedbackType.ADOPTION,
            value=value,
            context=context
        )
    
    def collect_implicit_signal(
        self,
        task_id: str,
        signal_type: str,  # "time_spent", "iteration", "silence"
        value: Any,
        context: Dict = None
    ) -> str:
        """
        采集隐式信号
        
        快捷方法,用于采集隐式行为信号
        """
        feedback_type_map = {
            "time_spent": FeedbackType.TIME_SPENT,
            "iteration": FeedbackType.ITERATION,
            "silence": FeedbackType.SILENCE
        }
        
        feedback_type = feedback_type_map.get(signal_type, FeedbackType.SILENCE)
        
        return self.collect_feedback(
            task_id=task_id,
            feedback_type=feedback_type,
            value=value,
            context=context
        )
    
    # ==================== 反馈处理 ====================
    
    def process_pending_feedbacks(self, batch_size: int = None) -> Dict:
        """
        处理待处理反馈
        
        核心处理流程:
        1. get待处理反馈
        2. 路由到ROI追踪器
        3. 触发强化学习
        4. generate迁移假设
        5. 归档反馈
        
        Returns:
            处理结果统计
        """
        batch_size = batch_size or self.config["batch_size"]
        
        self.status = IntegrationStatus.PROCESSING
        
        try:
            # 1. get可学习反馈
            learnable_feedbacks = self.feedback_pipeline.get_learnable_feedbacks(
                limit=batch_size
            )
            
            if not learnable_feedbacks:
                logger.info("没有待处理的反馈")
                self.status = IntegrationStatus.IDLE
                return {"processed": 0, "message": "No pending feedbacks"}
            
            results = {
                "processed": 0,
                "roi_updated": 0,
                "rl_triggered": 0,
                "transfer_generated": 0,
                "errors": []
            }
            
            for feedback in learnable_feedbacks:
                try:
                    self._process_single_feedback(feedback)
                    results["processed"] += 1
                except Exception as e:
                    logger.error(f"处理反馈失败 {feedback.feedback_id}: {e}")
                    results["errors"].append("执行失败")
            
            # 更新metrics
            self.metrics.processed_feedbacks += results["processed"]
            self.metrics.pending_feedbacks = max(
                0, 
                self.metrics.pending_feedbacks - results["processed"]
            )
            self._save_metrics()
            
            logger.info(f"处理完成: {results['processed']} 个反馈")
            
            self.status = IntegrationStatus.IDLE
            return results
            
        except Exception as e:
            logger.error(f"批处理失败: {e}")
            self.status = IntegrationStatus.ERROR
            return {"processed": 0, "error": "反馈批处理失败"}
    
    def _process_single_feedback(self, feedback: NormalizedFeedback):
        """处理单个反馈"""
        # 1. 更新ROI追踪
        self._update_roi_with_feedback(feedback)
        
        # 2. 触发强化学习
        if self._should_trigger_rl():
            self._trigger_reinforcement_learning(feedback)
        
        # 3. generate迁移假设
        if self.config["enable_transfer"]:
            self._generate_transfer_hypothesis(feedback)
        
        # 4. 归档
        self.feedback_pipeline.archive_feedback(feedback.feedback_id)
    
    def _update_roi_with_feedback(self, feedback: NormalizedFeedback):
        """使用反馈更新ROI"""
        # get或创建任务生命周期
        lifecycle = self.roi_tracker.get_lifecycle(feedback.task_id)
        
        if not lifecycle:
            # 创建新的生命周期
            lifecycle = TaskLifecycle(
                task_id=feedback.task_id,
                task_type=feedback.task_type,
                strategy=feedback.strategy
            )
            self.roi_tracker.register_task(lifecycle)
        
        # 记录反馈
        self.roi_tracker.record_feedback(
            task_id=feedback.task_id,
            feedback_type=feedback.raw_type,
            feedback_value=feedback.raw_value,
            timestamp=feedback.timestamp
        )
        
        self.metrics.roi_tasks_tracked += 1
    
    def _should_trigger_rl(self) -> bool:
        """judge是否触发强化学习"""
        pending_count = len(self.feedback_pipeline.get_pending_feedbacks())
        return pending_count >= self.config["min_feedback_for_rl"]
    
    def _trigger_reinforcement_learning(self, feedback: NormalizedFeedback):
        """触发强化学习"""
        # get该strategy的历史反馈
        strategy_feedbacks = self._get_strategy_feedbacks(feedback.strategy)
        
        if len(strategy_feedbacks) >= self.config["min_feedback_for_rl"]:
            # 批量更新Q值
            for fb in strategy_feedbacks:
                self.rl_trigger.update_q_value(
                    strategy=fb.strategy,
                    reward=fb.reward_value,
                    state_context=fb.task_type
                )
            
            self.metrics.rl_updates += 1
            logger.info(f"强化学习更新: {feedback.strategy}")
    
    def _generate_transfer_hypothesis(self, feedback: NormalizedFeedback):
        """generate迁移学习假设"""
        # 查找相似场景
        similar_contexts = self.transfer_learner.find_similar_contexts(
            feedback.task_type,
            top_k=3
        )
        
        for context, similarity in similar_contexts:
            if similarity >= self.config["confidence_threshold"]:
                # 注册迁移假设
                hypothesis = self.transfer_learner.register_transfer_hypothesis(
                    source_knowledge=feedback.strategy,
                    target_context=context,
                    similarity_score=similarity,
                    supporting_evidence=[feedback.feedback_id]
                )
                
                self.metrics.transfer_hypotheses += 1
                logger.info(f"迁移假设generate: {feedback.strategy} -> {context}")
    
    def _get_strategy_feedbacks(self, strategy: str) -> List[NormalizedFeedback]:
        """getstrategy相关的反馈"""
        all_pending = self.feedback_pipeline.get_pending_feedbacks()
        return [f for f in all_pending if f.strategy == strategy]
    
    def _schedule_processing(self):
        """调度处理"""
        # 简单实现:立即处理
        # 生产环境可以使用定时任务
        if self.config["auto_process"]:
            self.process_pending_feedbacks(batch_size=1)
    
    # ==================== 监控与报告 ====================
    
    def get_loop_status(self) -> Dict:
        """get闭环状态"""
        return {
            "status": self.status.value,
            "metrics": asdict(self.metrics),
            "pending_count": len(self.feedback_pipeline.get_pending_feedbacks()),
            "config": self.config
        }
    
    def generate_loop_report(self, days: int = 7) -> Dict:
        """
        generate闭环报告
        
        Args:
            days: 报告时间范围(天)
        
        Returns:
            闭环报告
        """
        since = datetime.now() - timedelta(days=days)
        
        # getROI报告
        roi_report = self.roi_tracker.generate_roi_report(
            since=since.isoformat()
        )
        
        # getQ表快照
        q_table = self.rl_trigger.get_q_table_snapshot()
        
        # get迁移假设
        hypotheses = self.transfer_learner.get_transfer_hypotheses(
            status="pending"
        )
        
        report = {
            "period": f"{days}天",
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_feedbacks": self.metrics.total_feedbacks,
                "processed_feedbacks": self.metrics.processed_feedbacks,
                "roi_tasks": self.metrics.roi_tasks_tracked,
                "rl_updates": self.metrics.rl_updates,
                "transfer_hypotheses": self.metrics.transfer_hypotheses
            },
            "roi_analysis": roi_report,
            "strategy_performance": q_table,
            "transfer_opportunities": hypotheses,
            "recommendations": self._generate_recommendations(roi_report, q_table)
        }
        
        # 保存报告
        report_path = self.base_path / f"loop_report_{datetime.now().strftime('%Y%m%d')}.yaml"
        with open(report_path, 'w', encoding='utf-8') as f:
            yaml.dump(report, f, allow_unicode=True)
        
        return report
    
    def _generate_recommendations(
        self, 
        roi_report: Dict, 
        q_table: Dict
    ) -> List[Dict]:
        """generate优化建议"""
        recommendations = []
        
        # 基于ROI分析
        if roi_report.get("average_roi", 0) < 1.0:
            recommendations.append({
                "type": "roi_warning",
                "priority": "high",
                "message": "整体ROI低于预期,需要优化strategy效果",
                "action": "审查低效strategy,增加A/B测试"
            })
        
        # 基于strategy表现
        low_performing = [
            s for s, data in q_table.items()
            if data.get("avg_q", 0) < 0.3
        ]
        if low_performing:
            recommendations.append({
                "type": "strategy_optimization",
                "priority": "medium",
                "message": f"发现{len(low_performing)}个低效strategy",
                "strategies": low_performing,
                "action": "考虑停用或重构这些strategy"
            })
        
        return recommendations
    
    def register_callback(self, callback: Callable):
        """注册回调函数"""
        self._callbacks.append(callback)
    
    def reset_metrics(self):
        """重置metrics"""
        self.metrics = FeedbackLoopMetrics()
        self._save_metrics()
        logger.info("metrics已重置")

# 便捷函数
_feedback_system = None

def get_feedback_system() -> FeedbackIntegrationSystem:
    """get反馈system_instance(单例)"""
    global _feedback_system
    if _feedback_system is None:
        _feedback_system = FeedbackIntegrationSystem()
    return _feedback_system

def collect_feedback(
    task_id: str,
    feedback_type: str,
    value: Any,
    context: Dict = None
) -> str:
    """便捷函数:采集反馈"""
    system = get_feedback_system()
    
    type_map = {
        "rating": FeedbackType.RATING,
        "adoption": FeedbackType.ADOPTION,
        "thumbs": FeedbackType.THUMBS,
        "comment": FeedbackType.COMMENT
    }
    
    fb_type = type_map.get(feedback_type, FeedbackType.COMMENT)
    
    return system.collect_feedback(
        task_id=task_id,
        feedback_type=fb_type,
        value=value,
        context=context
    )

def submit_rating(task_id: str, rating: int, comment: str = "") -> str:
    """便捷函数:提交评分"""
    system = get_feedback_system()
    return system.collect_explicit_rating(task_id, rating, comment)

def get_loop_report(days: int = 7) -> Dict:
    """便捷函数:get闭环报告"""
    system = get_feedback_system()
    return system.generate_loop_report(days)
