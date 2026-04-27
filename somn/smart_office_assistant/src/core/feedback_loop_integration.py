# -*- coding: utf-8 -*-
"""
__all__ = [
    'collect_adoption_signal',
    'collect_workflow_feedback',
    'generate_daily_report',
    'get_integrator',
    'get_loop_report',
    'match_transfer_learning',
    'register_callback',
    'submit_user_rating',
    'track_roi',
    'trigger_reinforcement_learning',
]

反馈闭环集成模块 v1.0
Feedback Loop Integration
=========================

将v8.4.2技术债务闭环整合到SomnCore主流程:
- 反馈采集点嵌入
- ROI追踪自动触发
- 强化学习实时更新
- 迁移学习场景匹配

集成点:
1. 工作流执行完成 → 自动采集执行反馈
2. strategy交付 → 用户评分/采纳信号
3. 日常交互 → 隐式反馈收集
4. 定时任务 → 闭环报告generate

版本: v1.0
日期: 2026-04-03
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class CoreFeedbackType(Enum):
    """核心反馈类型（区别于其他模块的FeedbackType）"""
    EXPLICIT_RATING = "explicit_rating"  # 显式评分
    ADOPTION_SIGNAL = "adoption_signal"  # 采纳信号
    EXECUTION_RESULT = "execution_result"  # 执行结果
    IMPLICIT_ENGAGEMENT = "implicit_engagement"  # 隐式参与

@dataclass
class FeedbackCollectionPoint:
    """反馈采集点配置"""
    name: str
    timing: str  # 采集时机
    methods: List[str]  # 采集方法
    signals: List[str]  # 信号类型
    auto_trigger: bool = True  # 是否自动触发

# 预定义反馈采集点
FEEDBACK_COLLECTION_POINTS = {
    "solution_delivery": FeedbackCollectionPoint(
        name="方案交付",
        timing="strategy方案交付后",
        methods=["星级评分", "采纳按钮", "修改追踪"],
        signals=["adoption", "rating", "iteration"],
        auto_trigger=True
    ),
    "strategy_execution": FeedbackCollectionPoint(
        name="strategy执行",
        timing="strategy执行过程中",
        methods=["进度反馈", "效果上报", "问题标记"],
        signals=["progress", "outcome", "issue"],
        auto_trigger=True
    ),
    "workflow_completion": FeedbackCollectionPoint(
        name="工作流完成",
        timing="工作流执行完成后",
        methods=["执行结果", "成功率统计"],
        signals=["execution_result", "success_ratio"],
        auto_trigger=True
    ),
    "daily_interaction": FeedbackCollectionPoint(
        name="日常交互",
        timing="日常对话交互中",
        methods=["隐式信号", "停留时长", "操作路径"],
        signals=["engagement", "time_spent", "navigation"],
        auto_trigger=False  # 需要显式触发
    ),
}

class FeedbackLoopIntegrator:
    """
    反馈闭环集成器

    负责将反馈管道,ROI追踪,强化学习,迁移学习
    整合到SomnCore的主流程中.
    """

    def __init__(self, base_path: Optional[str] = None):
        self.base_path = Path(base_path) if base_path else Path(__file__).parent.parent.parent
        self.data_dir = self.base_path / "data" / "feedback_loop"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # 延迟init(避免循环导入)
        self._feedback_pipeline = None
        self._roi_tracker = None
        self._reinforcement_trigger = None
        self._transfer_learner = None

        # 回调注册
        self._callbacks: Dict[str, List[Callable]] = {
            "on_feedback_collected": [],
            "on_roi_updated": [],
            "on_rl_triggered": [],
            "on_transfer_matched": [],
        }

        # [v10.1 P1-8] 异步写入队列：所有JSON写操作走队列+daemon线程
        # 收益：主线程不被JSON I/O阻塞；daemon线程确保程序退出时不漏写
        from concurrent.futures import ThreadPoolExecutor
        self._write_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="fb_write")
        self._write_queue: List[Tuple[Path, Dict]] = []
        self._write_lock = __import__('threading').Lock()

        # [P6] 反馈数据内存索引缓存：避免 get_loop_report() 每次glob+逐文件load
        self._feedback_cache: Dict[str, Dict] = {}   # task_id → data
        self._cache_lock = __import__('threading').Lock()
        self._CACHE_MAX_ENTRIES = 500  # [P6] 缓存上限，防止长期运行内存无限增长

        self._initialized = False
        
    def _ensure_initialized(self):
        """确保组件已init"""
        if self._initialized:
            return
        
        try:
            from ..neural_memory.feedback_pipeline import FeedbackPipeline
            self._feedback_pipeline = FeedbackPipeline(str(self.data_dir))
        except Exception as e:
            logger.warning(f"FeedbackPipeline init失败: {e}")
        
        try:
            from ..neural_memory.roi_tracker import ROITracker
            self._roi_tracker = ROITracker(str(self.data_dir))
        except Exception as e:
            logger.warning(f"ROITracker init失败: {e}")
        
        try:
            from ..neural_memory.reinforcement_trigger import ReinforcementTrigger
            self._reinforcement_trigger = ReinforcementTrigger(str(self.data_dir))
        except Exception as e:
            logger.warning(f"ReinforcementTrigger init失败: {e}")
        
        try:
            from ..neural_memory.transfer_learner import TransferLearner
            self._transfer_learner = TransferLearner(str(self.data_dir))
        except Exception as e:
            logger.warning(f"TransferLearner init失败: {e}")
        
        self._initialized = True

    # [v10.1 P1-8] 异步写入队列：所有JSON写操作走队列+daemon线程
    def _async_write(self, file_path: Path, data: Dict) -> None:
        """
        将数据异步写入文件（daemon线程，不阻塞主线程）。

        写入使用紧凑JSON格式（indent=None），相比 indent=2 可减少约40%文件大小。
        写入失败时记录warning，不向上抛异常以保证主流程不中断。
        """
        def _do_write():
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)  # 无indent，紧凑格式
                # [P6] 写入成功后更新内存索引缓存（带上限淘汰）
                task_id = data.get('task_id', file_path.stem)
                with self._cache_lock:
                    if len(self._feedback_cache) >= self._CACHE_MAX_ENTRIES:
                        # 淘汰最旧的一半条目（简单的批量LRU近似）
                        keys_to_evict = list(self._feedback_cache.keys())[:len(self._feedback_cache) // 2]
                        for k in keys_to_evict:
                            del self._feedback_cache[k]
                    self._feedback_cache[task_id] = data
            except Exception as e:
                logger.warning(f"[反馈写入] {file_path.name} 写入失败: {e}")

        self._write_executor.submit(_do_write)

    # ============================================================
    # 回调注册
    # ============================================================
    
    def register_callback(self, event: str, callback: Callable):
        """注册回调函数"""
        if event in self._callbacks:
            self._callbacks[event].append(callback)
    
    def _trigger_callbacks(self, event: str, data: Any):
        """触发回调"""
        for callback in self._callbacks.get(event, []):
            try:
                callback(data)
            except Exception as e:
                logger.warning(f"回调执行失败: {e}")
    
    # ============================================================
    # 核心集成方法
    # ============================================================
    
    def collect_workflow_feedback(
        self,
        task_id: str,
        strategy_plan: Dict[str, Any],
        execution_summary: Dict[str, Any],
        task_records: List[Any],
        state_history: List[Dict],
        rollback_results: List[Dict]
    ) -> Dict[str, Any]:
        """
        采集工作流执行反馈
        
        集成点: execute_workflow() 执行完成后自动调用
        """
        self._ensure_initialized()
        
        feedback_data = {
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "collection_point": "workflow_completion",
            "execution_summary": execution_summary,
            "task_details": [
                {
                    "task_name": record.task_name if hasattr(record, 'task_name') else record.get('task_name'),
                    "status": record.status if hasattr(record, 'status') else record.get('status'),
                    "attempts": record.attempts if hasattr(record, 'attempts') else record.get('attempts', 1),
                }
                for record in task_records
            ],
            "state_transitions": len(state_history),
            "rollback_count": len(rollback_results),
        }
        
        # 计算成功率作为隐式评分
        success_ratio = execution_summary.get("success_ratio", 0.0)
        implicit_rating = int(success_ratio * 5)  # 0-5星
        
        feedback_data["implicit_rating"] = implicit_rating
        feedback_data["success_ratio"] = success_ratio
        
        # 保存反馈
        feedback_file = self.data_dir / f"workflow_feedback_{task_id}.json"
        self._async_write(feedback_file, feedback_data)
        
        # 触发回调
        self._trigger_callbacks("on_feedback_collected", feedback_data)
        
        logger.info(f"工作流反馈已采集: {task_id}, 隐式评分: {implicit_rating}")
        return feedback_data
    
    def submit_user_rating(
        self,
        task_id: str,
        rating: int,  # 1-5星
        comment: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        提交用户显式评分
        
        集成点: 用户界面评分提交
        """
        self._ensure_initialized()
        
        if self._feedback_pipeline:
            return self._feedback_pipeline.submit_rating(
                task_id=task_id,
                rating=rating,
                comment=comment,
                user_id=user_id
            )
        else:
            # 降级处理:直接保存
            rating_data = {
                "task_id": task_id,
                "rating": rating,
                "comment": comment,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
            }
            rating_file = self.data_dir / f"rating_{task_id}.json"
            self._async_write(rating_file, rating_data)
            return {"status": "saved", "data": rating_data}
    
    def collect_adoption_signal(
        self,
        task_id: str,
        adopted: bool,
        modifications: Optional[List[str]] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        采集采纳信号
        
        集成点: 用户采纳/拒绝strategy方案
        """
        self._ensure_initialized()
        
        if self._feedback_pipeline:
            return self._feedback_pipeline.collect_adoption_signal(
                task_id=task_id,
                adopted=adopted,
                modifications=modifications,
                user_id=user_id
            )
        else:
            adoption_data = {
                "task_id": task_id,
                "adopted": adopted,
                "modifications": modifications or [],
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
            }
            adoption_file = self.data_dir / f"adoption_{task_id}.json"
            self._async_write(adoption_file, adoption_data)
            return {"status": "saved", "data": adoption_data}
    
    def track_roi(
        self,
        task_id: str,
        expected_outcome: Dict[str, Any],
        actual_outcome: Optional[Dict[str, Any]] = None,
        cost_investment: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        追踪ROI
        
        集成点: 任务ROI效果追踪
        """
        self._ensure_initialized()
        
        if self._roi_tracker:
            return self._roi_tracker.track_task(
                task_id=task_id,
                expected_outcome=expected_outcome,
                actual_outcome=actual_outcome,
                cost_investment=cost_investment
            )
        else:
            roi_data = {
                "task_id": task_id,
                "expected_outcome": expected_outcome,
                "actual_outcome": actual_outcome,
                "cost_investment": cost_investment,
                "timestamp": datetime.now().isoformat(),
            }
            roi_file = self.data_dir / f"roi_{task_id}.json"
            self._async_write(roi_file, roi_data)
            return {"status": "saved", "data": roi_data}
    
    def trigger_reinforcement_learning(
        self,
        action: str,
        reward: float,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        触发强化学习
        
        集成点: 根据执行结果更新strategyQ值
        """
        self._ensure_initialized()
        
        result = {"action": action, "reward": reward, "updated": False}
        
        if self._reinforcement_trigger:
            try:
                update_result = self._reinforcement_trigger.update_q_value(
                    action=action,
                    reward=reward,
                    context=context
                )
                result["updated"] = True
                result["q_value"] = update_result.get("q_value")
                self._trigger_callbacks("on_rl_triggered", result)
            except Exception as e:
                logger.warning(f"强化学习更新失败: {e}")
        
        return result
    
    def match_transfer_learning(
        self,
        source_knowledge: str,
        target_scenario: str,
        similarity_threshold: float = 0.7
    ) -> Dict[str, Any]:
        """
        匹配迁移学习
        
        集成点: 知识跨场景迁移
        """
        self._ensure_initialized()
        
        if self._transfer_learner:
            result = self._transfer_learner.match_scenario(
                source_knowledge=source_knowledge,
                target_scenario=target_scenario,
                similarity_threshold=similarity_threshold
            )
            self._trigger_callbacks("on_transfer_matched", result)
            return result
        else:
            return {
                "source": source_knowledge,
                "target": target_scenario,
                "matched": False,
                "reason": "TransferLearner not available"
            }
    
    # ============================================================
    # 闭环报告
    # ============================================================
    
    def get_loop_report(self, days: int = 7) -> Dict[str, Any]:
        """
        get反馈闭环报告
        
        集成点: 定时任务generate报告
        """
        self._ensure_initialized()
        
        report = {
            "period_days": days,
            "generated_at": datetime.now().isoformat(),
            "feedback_summary": {},
            "roi_summary": {},
            "rl_summary": {},
            "transfer_summary": {},
        }
        
        # 收集反馈数据 — [P6] 优先走内存缓存，避免 O(n) 磁盘扫描
        ratings = []
        adoptions = []

        with self._cache_lock:
            if self._feedback_cache:
                # 缓存命中：直接从内存读取
                for data in self._feedback_cache.values():
                    if "implicit_rating" in data:
                        ratings.append(data["implicit_rating"])
            else:
                # 缓存为空时 fallback 到磁盘扫描
                for f in self.data_dir.glob("workflow_feedback_*.json"):
                    try:
                        with open(f, 'r', encoding='utf-8') as file:
                            data = json.load(file)
                            if "implicit_rating" in data:
                                ratings.append(data["implicit_rating"])
                            # 回填缓存
                            task_id = data.get('task_id', f.stem)
                            self._feedback_cache[task_id] = data
                    except Exception as e:
                        logger.debug(f"跳过损坏的反馈文件 {f.name}: {e}")
        
        if ratings:
            report["feedback_summary"] = {
                "total_feedback": len(ratings),
                "average_rating": sum(ratings) / len(ratings),
                "rating_distribution": {
                    f"{i}_star": ratings.count(i) for i in range(1, 6)
                }
            }
        
        return report
    
    def generate_daily_report(self) -> Dict[str, Any]:
        """generate每日闭环报告"""
        return self.get_loop_report(days=1)

# ============================================================
# 便捷函数(供SomnCore调用)
# ============================================================

_integrator_instance: Optional[FeedbackLoopIntegrator] = None

def get_integrator(base_path: Optional[str] = None) -> FeedbackLoopIntegrator:
    """get集成器实例(单例模式)"""
    global _integrator_instance
    if _integrator_instance is None:
        _integrator_instance = FeedbackLoopIntegrator(base_path)
    return _integrator_instance

def collect_workflow_feedback(
    task_id: str,
    strategy_plan: Dict[str, Any],
    execution_summary: Dict[str, Any],
    task_records: List[Any],
    state_history: List[Dict],
    rollback_results: List[Dict],
    base_path: Optional[str] = None
) -> Dict[str, Any]:
    """便捷函数:采集工作流反馈"""
    return get_integrator(base_path).collect_workflow_feedback(
        task_id, strategy_plan, execution_summary, task_records, state_history, rollback_results
    )

def submit_user_rating(
    task_id: str,
    rating: int,
    comment: Optional[str] = None,
    user_id: Optional[str] = None,
    base_path: Optional[str] = None
) -> Dict[str, Any]:
    """便捷函数:提交用户评分"""
    return get_integrator(base_path).submit_user_rating(task_id, rating, comment, user_id)

def trigger_reinforcement_learning(
    action: str,
    reward: float,
    context: Optional[Dict[str, Any]] = None,
    base_path: Optional[str] = None
) -> Dict[str, Any]:
    """便捷函数:触发强化学习"""
    return get_integrator(base_path).trigger_reinforcement_learning(action, reward, context)

# ============================================================
# 测试
# ============================================================

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
