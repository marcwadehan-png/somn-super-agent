"""
__all__ = [
    'execute_learning_pipeline',
    'get_pipeline_status',
    'LearningPipeline',
]

学习流水线 - Learning Pipeline v2.0.0
整合所有学习组件，提供端到端的学习流程

流程:
输入 → 数据扫描 → 场景分析 → 策略选择 → 多策略执行
    ↓
反馈整合 → 知识更新 → 经验回放(LearningReplayBuffer) → 闭环强化

[v2.0 新增]
- 双向闭环：LearningReplayBuffer 从藏书阁提取经验回放到学习系统
- 知识库迁移：从 DomainNexus 抽取模式注入学习
- 定时触发回放：与 _library_review_scheduler 协同

组件:
1. 数据扫描 - UnifiedDataScanner
2. 场景分析 - AdaptiveStrategyEngine
3. 策略执行 - UnifiedLearningOrchestrator
4. 反馈整合 - FeedbackPipeline + ReinforcementBridge
5. 知识更新 - MemoryLifecycleManager
6. [v2.0] 经验回放 - LearningReplayBuffer（双向闭环核心）
"""

from __future__ import annotations

import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

from src.core.paths import LEARNING_DIR

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════════

class PipelineStage(Enum):
    """流水线阶段"""
    DATA_SCAN = "data_scan"
    SCENE_ANALYSIS = "scene_analysis"
    STRATEGY_SELECTION = "strategy_selection"
    STRATEGY_EXECUTION = "strategy_execution"
    FEEDBACK_INTEGRATION = "feedback_integration"
    KNOWLEDGE_UPDATE = "knowledge_update"
    REPORT_GENERATION = "report_generation"

@dataclass
class PipelineConfig:
    """流水线配置"""
    enable_adaptive: bool = True
    enable_feedback: bool = True
    enable_knowledge_update: bool = True
    max_strategies: int = 3
    parallel_execution: bool = True
    cache_scan_result: bool = True

@dataclass
class PipelineStageResult:
    """阶段结果"""
    stage: PipelineStage
    success: bool
    duration_seconds: float
    data: Any = None
    error: str = ""

@dataclass
class PipelineResult:
    """流水线执行结果"""
    # 必填字段
    pipeline_id: str
    start_time: str
    end_time: str
    duration_seconds: float
    config: Dict
    stages: Dict[str, PipelineStageResult]
    total_events: int
    total_updates: int
    strategies_executed: List[str]
    feedback_integrated: int
    knowledge_evolved: int
    # v2.0: 经验回放统计
    replay_extracted: int = 0
    replay_replayed: int = 0
    replay_buffer_size: int = 0
    # 可选字段
    success: bool = False
    summary: str = ""
    scene_type: str = ""
    health_score: float = 0.0
    recommendations: List[str] = field(default_factory=list)


class LearningPipeline:
    """学习流水线 v2.0.0 - 整合所有学习组件的端到端流水线
    
    [v2.0 双向闭环]
    - 正向：数据扫描 → 策略执行 → 知识更新 → 藏书阁入库
    - 反向：藏书阁经验提取 → ReplayBuffer → 策略强化（新增）
    """
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else LEARNING_DIR
        self.reports_path = self.base_path / "pipeline_reports"
        self.reports_path.mkdir(parents=True, exist_ok=True)
        
        self.config = PipelineConfig()
        self._scanner = None
        self._strategy_engine = None
        self._orchestrator = None
        self._feedback_pipeline = None
        self._rl_bridge = None
        self._lifecycle_manager = None
        self._replay_buffer = None      # v2.0: 经验回放缓冲区
        self._scan_cache: Dict = {}
        
        logger.info("学习流水线 v2.0 初始化完成")
    
    @property
    def replay_buffer(self):
        """延迟加载经验回放缓冲区"""
        if self._replay_buffer is None:
            from .learning_replay_buffer import get_replay_buffer
            self._replay_buffer = get_replay_buffer()
        return self._replay_buffer
    
    @property
    def scanner(self):
        if self._scanner is None:
            from .learning_strategies.data_scanner import UnifiedDataScanner
            self._scanner = UnifiedDataScanner(str(self.base_path))
        return self._scanner
    
    @property
    def strategy_engine(self):
        if self._strategy_engine is None:
            from .adaptive_strategy_engine import AdaptiveStrategyEngine
            self._strategy_engine = AdaptiveStrategyEngine(str(self.base_path))
        return self._strategy_engine
    
    @property
    def orchestrator(self):
        if self._orchestrator is None:
            from .unified_learning_orchestrator import UnifiedLearningOrchestrator
            self._orchestrator = UnifiedLearningOrchestrator(str(self.base_path))
        return self._orchestrator
    
    @property
    def feedback_pipeline(self):
        if self._feedback_pipeline is None:
            from .feedback_pipeline import FeedbackPipeline
            self._feedback_pipeline = FeedbackPipeline(str(self.base_path))
        return self._feedback_pipeline
    
    @property
    def rl_bridge(self):
        if self._rl_bridge is None:
            from .reinforcement_bridge import ReinforcementBridge
            self._rl_bridge = ReinforcementBridge(str(self.base_path))
        return self._rl_bridge
    
    @property
    def lifecycle_manager(self):
        if self._lifecycle_manager is None:
            from .memory_lifecycle_manager import MemoryLifecycleManager
            self._lifecycle_manager = MemoryLifecycleManager(str(self.base_path))
        return self._lifecycle_manager
    
    def execute(self, context: Optional[Dict] = None,
                config: Optional[PipelineConfig] = None) -> PipelineResult:
        """执行完整学习流水线"""
        start_time = datetime.now()
        pipeline_id = f"PL_{start_time.strftime('%Y%m%d%H%M%S')}"
        
        if config:
            self.config = config
        
        context = context or {}
        stages = {}
        total_events = 0
        total_updates = 0
        strategies_executed = []
        feedback_integrated = 0
        knowledge_evolved = 0
        scene_type = "unknown"
        # v2.0: 经验回放统计（在 try 外初始化，确保 report 阶段可访问）
        replay_extracted = 0
        replay_replayed = 0
        
        logger.info(f"开始执行学习流水线: {pipeline_id}")
        
        # Stage 1: 数据扫描
        stage_start = datetime.now()
        try:
            scan_result = self.scanner.scan()
            duration = (datetime.now() - stage_start).total_seconds()
            stages["data_scan"] = PipelineStageResult(
                stage=PipelineStage.DATA_SCAN, success=True,
                duration_seconds=duration,
                data={"total": scan_result.total, "local": scan_result.local_count}
            )
            logger.info(f"[阶段1] 数据扫描完成: {scan_result.total}条数据")
        except Exception as e:
            stages["data_scan"] = PipelineStageResult(
                stage=PipelineStage.DATA_SCAN, success=False,
                duration_seconds=(datetime.now() - stage_start).total_seconds(),
                error="学习管道执行失败"
            )
            logger.error(f"[阶段1] 数据扫描失败: {e}")
            scan_result = None
        
        # Stage 2: 场景分析
        if self.config.enable_adaptive and scan_result:
            stage_start = datetime.now()
            try:
                scene = self.strategy_engine.analyze_scene(
                    scan_result,
                    context.get("feedback_stats"),
                    context.get("task_context")
                )
                scene_type = scene.scene_type.value
                stages["scene_analysis"] = PipelineStageResult(
                    stage=PipelineStage.SCENE_ANALYSIS, success=True,
                    duration_seconds=(datetime.now() - stage_start).total_seconds(),
                    data={"scene_type": scene_type, "confidence": scene.confidence}
                )
            except Exception as e:
                stages["scene_analysis"] = PipelineStageResult(
                    stage=PipelineStage.SCENE_ANALYSIS, success=False,
                    duration_seconds=(datetime.now() - stage_start).total_seconds(),
                    error="学习管道执行失败"
                )
        
        # Stage 3: 策略选择
        if self.config.enable_adaptive and scan_result:
            stage_start = datetime.now()
            try:
                strategies, _ = self.strategy_engine.select_strategies(scan_result)
                strategies_executed = strategies[:self.config.max_strategies]
                stages["strategy_selection"] = PipelineStageResult(
                    stage=PipelineStage.STRATEGY_SELECTION, success=True,
                    duration_seconds=(datetime.now() - stage_start).total_seconds(),
                    data={"strategies": strategies_executed}
                )
                logger.info(f"[阶段3] 策略选择完成: {strategies_executed}")
            except Exception as e:
                strategies_executed = ["DAILY"]
                stages["strategy_selection"] = PipelineStageResult(
                    stage=PipelineStage.STRATEGY_SELECTION, success=False,
                    duration_seconds=(datetime.now() - stage_start).total_seconds(),
                    error="学习管道执行失败"
                )
        
        # Stage 4: 策略执行
        if scan_result and strategies_executed:
            stage_start = datetime.now()
            try:
                from .learning_strategies import LearningStrategyType
                strategy_map = {
                    "DAILY": LearningStrategyType.DAILY,
                    "THREE_TIER": LearningStrategyType.THREE_TIER,
                    "ENHANCED": LearningStrategyType.ENHANCED,
                    "SOLUTION": LearningStrategyType.SOLUTION,
                    "FEEDBACK": LearningStrategyType.FEEDBACK
                }
                
                for stype in strategies_executed:
                    rl_stype = strategy_map.get(stype)
                    if rl_stype:
                        result = self.orchestrator.execute_strategy(
                            rl_stype, context=context, scan_result=scan_result
                        )
                        total_events += result.total_events
                        total_updates += result.total_knowledge_updates
                
                stages["strategy_execution"] = PipelineStageResult(
                    stage=PipelineStage.STRATEGY_EXECUTION, success=True,
                    duration_seconds=(datetime.now() - stage_start).total_seconds(),
                    data={"events": total_events, "updates": total_updates}
                )
                logger.info(f"[阶段4] 策略执行完成: {total_events}事件, {total_updates}更新")
            except Exception as e:
                stages["strategy_execution"] = PipelineStageResult(
                    stage=PipelineStage.STRATEGY_EXECUTION, success=False,
                    duration_seconds=(datetime.now() - stage_start).total_seconds(),
                    error="学习管道执行失败"
                )
        
        # Stage 5: 反馈整合
        if self.config.enable_feedback:
            stage_start = datetime.now()
            try:
                feedbacks = self.feedback_pipeline.get_learnable_feedbacks(limit=20)
                for fb in feedbacks:
                    self.rl_bridge.feedback_to_experience(fb, context)
                feedback_integrated = len(feedbacks)
                stages["feedback_integration"] = PipelineStageResult(
                    stage=PipelineStage.FEEDBACK_INTEGRATION, success=True,
                    duration_seconds=(datetime.now() - stage_start).total_seconds(),
                    data={"integrated": feedback_integrated}
                )
            except Exception as e:
                stages["feedback_integration"] = PipelineStageResult(
                    stage=PipelineStage.FEEDBACK_INTEGRATION, success=False,
                    duration_seconds=(datetime.now() - stage_start).total_seconds(),
                    error="学习管道执行失败"
                )
        
        # Stage 6: 知识更新
        if self.config.enable_knowledge_update:
            stage_start = datetime.now()
            try:
                self.lifecycle_manager.apply_decay()
                review_tasks = self.lifecycle_manager.trigger_review(max_tasks=5)
                health = self.lifecycle_manager.get_health_report()
                knowledge_evolved = len(review_tasks)
                stages["knowledge_update"] = PipelineStageResult(
                    stage=PipelineStage.KNOWLEDGE_UPDATE, success=True,
                    duration_seconds=(datetime.now() - stage_start).total_seconds(),
                    data={"evolved": knowledge_evolved, "health_score": health.health_score}
                )
            except Exception as e:
                stages["knowledge_update"] = PipelineStageResult(
                    stage=PipelineStage.KNOWLEDGE_UPDATE, success=False,
                    duration_seconds=(datetime.now() - stage_start).total_seconds(),
                    error="学习管道执行失败"
                )

        # Stage 6.5: [v2.0] 经验回放 — 双向闭环核心
        replay_extracted = 0
        replay_replayed = 0
        stage_start = datetime.now()
        try:
            rb = self.replay_buffer
            
            # 1) 从藏书阁提取经验
            replay_extracted = rb.extract_from_library()
            
            # 2) 从知识库(DomainNexus)提取模式
            kb_extracted = rb.extract_from_knowledge_base()
            replay_extracted += kb_extracted
            
            # 3) 获取回放批次并"学习"这些经验
            batch = rb.get_replay_batch(batch_size=12, balanced=True)
            if batch:
                replay_replayed = len(batch.entries)
                # 将回放条目转化为强化学习的经验样本
                for entry in batch.entries:
                    # 通过 RL Bridge 注入经验
                    experience = {
                        "source": entry.source.name,
                        "content": entry.content,
                        "lesson_type": entry.lesson_type,
                        "value_score": entry.value_score,
                        "importance_weight": entry.importance_weight,
                        "tags": entry.tags,
                    }
                    self.rl_bridge.feedback_to_experience(experience, context)
                # 标记已消费
                for entry in batch.entries:
                    rb.consume_entry(entry.entry_id, feedback="pipeline_replay")
            
            stages["experience_replay"] = PipelineStageResult(
                stage="experience_replay", success=True,
                duration_seconds=(datetime.now() - stage_start).total_seconds(),
                data={
                    "extracted": replay_extracted,
                    "replayed": replay_replayed,
                    "buffer_size": len(rb._buffer),
                },
            )
            logger.info(f"[阶段6.5] 经验回放完成: 提取{replay_extracted}条, 回放{replay_replayed}条")
        except Exception as e:
            stages["experience_replay"] = PipelineStageResult(
                stage="experience_replay", success=False,
                duration_seconds=(datetime.now() - stage_start).total_seconds(),
                error=str(e)[:100]
            )
        
        # Stage 7: 报告生成
        end_time = datetime.now()
        recommendations = []
        if scene_type != "unknown":
            recommendations.append(f"场景类型: {scene_type}")
        if total_events == 0:
            recommendations.append("无新增学习事件，考虑增加数据源")
        if feedback_integrated > 0:
            recommendations.append(f"已整合{feedback_integrated}条反馈用于RL学习")
        if replay_replayed > 0:
            recommendations.append(f"[v2.0] 经验回放: 提取{replay_extracted}条, 回放{replay_replayed}条")
        if replay_extracted == 0 and replay_replayed == 0:
            recommendations.append("[v2.0] 回放缓冲区为空，建议先入库记忆到藏书阁")
        
        success = all(s.success for s in stages.values())
        summary = f"执行{len(stages)}个阶段, {total_events}事件, {total_updates}更新"
        
        result = PipelineResult(
            pipeline_id=pipeline_id,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            duration_seconds=(end_time - start_time).total_seconds(),
            config={"adaptive": self.config.enable_adaptive,
                   "feedback": self.config.enable_feedback},
            stages={k: {"stage": v.stage.value, "success": v.success,
                       "duration": v.duration_seconds, "error": v.error}
                   for k, v in stages.items()},
            total_events=total_events,
            total_updates=total_updates,
            strategies_executed=strategies_executed,
            feedback_integrated=feedback_integrated,
            knowledge_evolved=knowledge_evolved,
            # v2.0: 经验回放统计
            replay_extracted=replay_extracted,
            replay_replayed=replay_replayed,
            success=success,
            summary=summary,
            recommendations=recommendations,
            scene_type=scene_type
        )
        
        self._save_report(result)
        logger.info(f"流水线执行完成: {summary}")
        
        return result
    
    def get_status(self) -> Dict:
        """获取流水线状态（含 v2.0 回放缓冲区状态）"""
        status = {
            "config": {
                "enable_adaptive": self.config.enable_adaptive,
                "enable_feedback": self.config.enable_feedback,
                "enable_knowledge_update": self.config.enable_knowledge_update
            },
            "components_initialized": {
                "scanner": self._scanner is not None,
                "strategy_engine": self._strategy_engine is not None,
                "orchestrator": self._orchestrator is not None,
                "replay_buffer": self._replay_buffer is not None,  # v2.0
            }
        }
        # v2.0: 加入回放缓冲区实时统计
        try:
            rb = self.replay_buffer
            status["replay_buffer_stats"] = rb.get_statistics()
        except Exception:
            pass
        return status
    
    def _save_report(self, result: PipelineResult):
        """保存执行报告（v2.0 含经验回放统计）"""
        try:
            report_file = self.reports_path / f"{result.pipeline_id}.json"
            data = {
                "pipeline_id": result.pipeline_id,
                "start_time": result.start_time,
                "end_time": result.end_time,
                "duration_seconds": result.duration_seconds,
                "stages": result.stages,
                "total_events": result.total_events,
                "strategies": result.strategies_executed,
                "feedback_integrated": result.feedback_integrated,
                # v2.0: 经验回放统计
                "replay_extracted": getattr(result, 'replay_extracted', 0),
                "replay_replayed": getattr(result, 'replay_replayed', 0),
                "replay_buffer_size": getattr(result, 'replay_buffer_size', 0),
                "success": result.success,
                "summary": result.summary,
                "recommendations": result.recommendations,
                "scene_type": result.scene_type
            }
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"保存报告失败: {e}")


_pipeline_instance = None

def get_learning_pipeline() -> LearningPipeline:
    """获取流水线实例"""
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = LearningPipeline()
    return _pipeline_instance

def execute_learning_pipeline(context: Optional[Dict] = None,
                              config: Optional[PipelineConfig] = None) -> PipelineResult:
    """便捷函数：执行学习流水线"""
    return get_learning_pipeline().execute(context, config)

def get_pipeline_status() -> Dict:
    """便捷函数：获取流水线状态"""
    return get_learning_pipeline().get_status()
