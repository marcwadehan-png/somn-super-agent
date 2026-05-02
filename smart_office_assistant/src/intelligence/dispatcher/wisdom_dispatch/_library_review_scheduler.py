# -*- coding: utf-8 -*-
"""
藏书阁定时审查调度器 v1.0
_library_review_scheduler.py

按 TTL 定期触发记忆审查任务，实现记忆生命周期的自动化：
- 丁级：7天自动清理
- 丙级：30天审查
- 乙级：365天审查
- 甲级：永不删除，仅标记

版本: v1.0.0
创建: 2026-04-28
"""

from __future__ import annotations

import logging
import time
import threading
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class ReviewAction(Enum):
    """审查动作"""
    CLEAN = auto()         # 清理/删除
    REVIEW = auto()        # 标记审查
    PROMOTE = auto()       # 提升等级
    DEMOTE = auto()        # 降低等级
    KEEP = auto()          # 保持不变


@dataclass
class ReviewTask:
    """单条审查任务"""
    cell_id: str
    current_grade: str     # 当前分级名称
    age_days: float
    action: ReviewAction
    reason: str
    priority: int          # 越小越优先


@dataclass
class ReviewResult:
    """一轮审查的结果"""
    executed_at: str
    total_scanned: int = 0
    actions_taken: Dict[str, int] = field(default_factory=dict)
    tasks: List[ReviewTask] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class LibraryReviewScheduler:
    """
    藏书阁定时审查调度器
    
    功能:
    - 按甲/乙/丙/丁各级 TTL 触发审查
    - 支持后台线程周期运行
    - 支持手动触发单次审查
    - 审查结果回调通知
    """
    
    # 各级的 TTL 配置（天）
    GRADE_TTL_DAYS: Dict[str, Dict[str, Any]] = {
        "甲级": {"ttl": None, "action": "keep", "description": "永恒记忆，永不删除"},
        "乙级": {"ttl": 365, "action": "review", "description": "长期记忆，年审"},
        "丙级": {"ttl": 30, "action": "review", "description": "短期记忆，月审"},
        "丁级": {"ttl": 7, "action": "clean", "description": "待定记忆，7天自动清理"},
    }
    
    def __init__(
        self,
        library=None,
        callback: Optional[Callable[[ReviewResult], None]] = None,
    ):
        """
        Args:
            library: 藏书阁实例（延迟初始化）
            callback: 审查完成后的回调函数
        """
        self._library = library
        self._callback = callback
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._last_run_time: float = 0.0
        self._run_count = int(0)
        
        # 审查统计
        self._stats = {
            "total_runs": 0,
            "total_reviews": 0,
            "total_cleaned": 0,
            "total_promoted": 0,
            "total_demoted": 0,
        }
    
    def _get_library(self):
        """获取藏书阁实例"""
        if self._library is None:
            from ._imperial_library import ImperialLibrary
            self._library = ImperialLibrary()
        return self._library

    def bind_library(self, library) -> None:
        """[v2.0] 绑定藏书阁实例（由 ImperialLibrary.__init__ 自动调用）"""
        self._library = library
    
    # ──────────────────────────────────────────────────────
    #  核心审查逻辑
    # ──────────────────────────────────────────────────────
    
    def run_review(self, operator: str = "scheduler") -> ReviewResult:
        """
        执行一轮完整审查。
        
        遍历所有 CellRecord，根据分级和年龄决定处理方式。
        
        Returns:
            ReviewResult 包含所有审查结果
        """
        lib = self._get_library()
        now = time.time()
        
        result = ReviewResult(
            executed_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        
        for cell_id, record in lib._cells.items():
            result.total_scanned += 1
            
            age_days = (now - record.created_at) / 86400 if record.created_at else 0
            grade_name = record.grade.value if hasattr(record.grade, 'value') else str(record.grade)
            
            task = self._evaluate_cell(cell_id, record, age_days)
            
            if task:
                result.tasks.append(task)
                
                # 执行动作
                try:
                    self._execute_action(lib, record, task, operator)
                    action_name = task.action.name.lower()
                    result.actions_taken[action_name] = result.actions_taken.get(action_name, 0) + 1
                    
                    # 更新统计
                    if task.action == ReviewAction.CLEAN:
                        self._stats["total_cleaned"] += 1
                    elif task.action == ReviewAction.PROMOTE:
                        self._stats["total_promoted"] += 1
                    elif task.action == ReviewAction.DEMOTE:
                        self._stats["total_demoted"] += 1
                    elif task.action in (ReviewAction.REVIEW, ReviewAction.KEEP):
                        self._stats["total_reviews"] += 1
                        
                except Exception as e:
                    result.errors.append(f"{cell_id}: {e}")
                    logger.error(f"审查执行失败 [{cell_id}]: {e}")
        
        # 更新状态
        self._last_run_time = now
        self._run_count += 1
        self._stats["total_runs"] = self._run_count
        
        logger.info(
            f"[ReviewScheduler] 第{self._run_count}轮审查完成: "
            f"扫描={result.total_scanned}, 动作={result.actions_taken}"
        )
        
        # 回调
        if self._callback:
            try:
                self._callback(result)
            except Exception as e:
                logger.error(f"审查回调异常: {e}")
        
        return result
    
    def _evaluate_cell(
        self, cell_id: str, record: Any, age_days: float
    ) -> Optional[ReviewTask]:
        """
        评估单个格子的审查需求。
        
        返回 None 表示不需要操作。
        """
        grade_name = record.grade.value if hasattr(record.grade, 'value') else str(record.grade)
        ttl_config = self.GRADE_TTL_DAYS.get(grade_name)
        
        if not ttl_config:
            return None
        
        ttl = ttl_config.get("ttl")
        action_type = ttl_config.get("action", "keep")
        
        # 甲级：永不操作
        if ttl is None:
            return None
        
        # 年龄未到 TTL
        if age_days < ttl:
            return None
        
        # 决定动作和优先级
        if action_type == "clean":
            return ReviewTask(
                cell_id=cell_id,
                current_grade=grade_name,
                age_days=age_days,
                action=ReviewAction.CLEAN,
                reason=f"{grade_name}记忆超过{ttl}天({age_days:.1f}天)，执行清理",
                priority=10,  # 清理最高优先级
            )
        
        elif action_type == "review":
            # 根据访问频率决定升降级
            access_freq = record.access_count / max(age_days, 1)
            
            if access_freq > 0.5 and record.value_score >= 0.7:
                # 高频高价值 → 考虑升级
                action = ReviewAction.PROMOTE
                reason = f"高频({record.access_count}次)高价值({record.value_score:.2f})→建议升级"
                priority = 3
            elif access_freq < 0.05 and record.value_score < 0.3:
                # 低频低价值 → 降级
                action = ReviewAction.DEMOTE
                reason = f"低频低价值({record.value_score:.2f})→建议降级"
                priority = 2
            else:
                action = ReviewAction.REVIEW
                reason = f"定期审查: {age_days:.0f}天, 访问{record.access_count}次"
                priority = 5
            
            return ReviewTask(
                cell_id=cell_id,
                current_grade=grade_name,
                age_days=age_days,
                action=action,
                reason=reason,
                priority=priority,
            )
        
        return None
    
    def _execute_action(
        self, library: Any, record: Any, task: ReviewTask, operator: str
    ) -> None:
        """执行审查动作"""
        if task.action == ReviewAction.CLEAN:
            library.delete_cell(record.id, operator=operator)
            
        elif task.action == ReviewAction.REVIEW:
            record.last_reviewed = time.time()
            record.review_count += 1
            library._dirty = True
            
        elif task.action == ReviewAction.PROMOTE:
            # 提升分级
            from ._imperial_library import MemoryGrade
            grade_order = [MemoryGrade.DING, MemoryGrade.BING, MemoryGrade.YI, MemoryGrade.JIA]
            try:
                current_idx = grade_order.index(record.grade)
                if current_idx < len(grade_order) - 1:
                    record.grade = grade_order[current_idx + 1]
                    record.last_reviewed = time.time()
                    record.review_count += 1
                    library._dirty = True
            except ValueError:
                pass
                
        elif task.action == ReviewAction.DEMOTE:
            # 降低分级
            from ._imperial_library import MemoryGrade
            grade_order = [MemoryGrade.DING, MemoryGrade.BING, MemoryGrade.YI, MemoryGrade.JIA]
            try:
                current_idx = grade_order.index(record.grade)
                if current_idx > 0:
                    record.grade = grade_order[current_idx - 1]
                    record.last_reviewed = time.time()
                    record.review_count += 1
                    library._dirty = True
            except ValueError:
                pass
    
    # ──────────────────────────────────────────────────────
    #  周期运行
    # ──────────────────────────────────────────────────────
    
    def start_background(self, interval_hours: float = 24.0) -> None:
        """
        启动后台周期性审查。
        
        Args:
            interval_hours: 审查间隔（小时），默认每天一次
        """
        if self._running:
            logger.warning("[ReviewScheduler] 已在运行中")
            return
        
        self._running = True
        interval_seconds = interval_hours * 3600
        
        def _loop():
            while self._running:
                try:
                    self.run_review()
                except Exception as e:
                    logger.error(f"[ReviewScheduler] 后台审查异常: {e}")

                # 分段休眠（每小时检查一次是否需要停止）
                remaining = interval_seconds
                while remaining > 0:
                    if not self._running:
                        break
                    chunk = min(3600, remaining)
                    time.sleep(chunk)
                    remaining -= chunk
        
        self._thread = threading.Thread(target=_loop, daemon=True, name="LibraryReviewScheduler")
        self._thread.start()
        logger.info(f"[ReviewScheduler] 后台审查已启动，间隔={interval_hours}小时")
    
    def stop_background(self) -> None:
        """停止后台周期审查"""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=10)
        logger.info("[ReviewScheduler] 后台审查已停止")
    
    @property
    def is_running(self) -> bool:
        return self._running
    
    # ──────────────────────────────────────────────────────
    #  查询 & 统计
    # ──────────────────────────────────────────────────────
    
    def get_stats(self) -> Dict[str, Any]:
        """获取调度器统计信息"""
        return {
            **self._stats,
            "is_running": self._running,
            "last_run_time": datetime.fromtimestamp(self._last_run_time).isoformat() if self._last_run_time else None,
            "run_count": self._run_count,
            "grade_ttl_config": {
                k: {"ttl_days": v["ttl"], "action": v["action"]}
                for k, v in self.GRADE_TTL_DAYS.items()
            },
        }
    
    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """
        获取即将到期需要处理的任务预览（不执行）。
        
        用于 Dashboard 展示。
        """
        lib = self._get_library()
        now = time.time()
        pending = []
        
        for cell_id, record in lib._cells.items():
            age_days = (now - record.created_at) / 86400
            grade_name = record.grade.value if hasattr(record.grade, 'value') else str(record.grade)
            config = self.GRADE_TTL_DAYS.get(grade_name, {})
            ttl = config.get("ttl")
            
            if ttl is not None:
                remaining = ttl - age_days
                if remaining <= 7 and remaining > 0:  # 未来7天内到期
                    pending.append({
                        "cell_id": cell_id[:20],
                        "title": getattr(record, 'title', ''),
                        "grade": grade_name,
                        "age_days": round(age_days, 1),
                        "remaining_days": round(remaining, 1),
                        "pending_action": config.get("action", "?"),
                    })
        
        pending.sort(key=lambda x: x["remaining_days"])
        return pending[:20]


# ══════════════════════════════════════════════════════════════
#  便捷入口
# ══════════════════════════════════════════════════════════════

_scheduler_instance: Optional[LibraryReviewScheduler] = None


def get_review_scheduler() -> LibraryReviewScheduler:
    """获取全局审查调度器单例"""
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = LibraryReviewScheduler()
    return _scheduler_instance


def run_once(operator: str = "manual") -> ReviewResult:
    """便捷：手动触发一轮审查"""
    scheduler = get_review_scheduler()
    return scheduler.run_review(operator=operator)
