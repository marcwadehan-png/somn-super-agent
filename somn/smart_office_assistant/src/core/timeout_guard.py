"""
TimeoutGuard - Somn系统全局超时守护器 v1.0.0

3分钟分级响应安全网：30s预警 → 60s降级 → 120s紧急 → 180s强制终止
解决P0-3（主处理入口无全局超时）并提供全局降级基础设施。

用法:
    from src.core.timeout_guard import create_timeout_guard, TimeoutGuard

    # 方式1: 上下文管理器
    guard = create_timeout_guard(request_id="xxx")
    with guard.monitor("Phase1 分析") as ctx:
        result = do_analysis()

    # 方式2: 同步函数装饰器
    @guard.protect(timeout=30, fallback=default_result)
    def slow_operation():
        ...

    # 方式3: 异步函数装饰器
    @guard.aprotect(timeout=30, fallback=default_result)
    async def slow_async_op():
        ...
"""

import asyncio
import functools
import logging
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional
from pathlib import Path

# [v1.0] 项目根目录（确定性路径）
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

logger = logging.getLogger(__name__)


class TimeoutLevel(Enum):
    """超时降级级别 [v18.0 优化：阈值从30s/60s/120s/180s调整为15s/30s/60s/120s]"""
    NORMAL = "normal"         # 0~15s: 正常模式
    WARNING = "warning"       # 15~30s: 预警模式，准备备选路径
    DEGRADED = "degraded"    # 30~60s: 降级模式，跳过非核心步骤
    EMERGENCY = "emergency"   # 60~120s: 紧急模式，最小可用输出
    TERMINATE = "terminate"   # >120s: 强制终止


# 各级别对应的时间阈值（秒）[v18.0 优化：整体前移15秒]
LEVEL_THRESHOLDS = {
    TimeoutLevel.NORMAL: 0,
    TimeoutLevel.WARNING: 15,
    TimeoutLevel.DEGRADED: 30,
    TimeoutLevel.EMERGENCY: 60,
    TimeoutLevel.TERMINATE: 120,
}


@dataclass
class TimeoutContext:
    """超时上下文对象，贯穿整个请求生命周期"""
    request_id: str
    start_time: float
    level: TimeoutLevel = TimeoutLevel.NORMAL
    deadline: float = 0.0
    degradation_steps: list = field(default_factory=list)
    partial_results: dict = field(default_factory=dict)
    timeout_event: threading.Event = field(default_factory=threading.Event)

    def __post_init__(self):
        if self.deadline == 0.0:
            self.deadline = self.start_time + 180.0  # 默认3分钟

    @property
    def elapsed(self) -> float:
        """已耗时（秒）"""
        return time.monotonic() - self.start_time

    @property
    def remaining(self) -> float:
        """剩余时间（秒），负数表示已超时"""
        return max(0.0, self.deadline - time.monotonic())

    def is_expired(self) -> bool:
        """是否已超过绝对截止时间"""
        return time.monotonic() >= self.deadline

    def get_level_for_elapsed(self) -> TimeoutLevel:
        """根据已耗时计算应该处于的级别 [v18.0: 阈值更新为15s/30s/60s/120s]"""
        elapsed = self.elapsed
        if elapsed >= 120:
            return TimeoutLevel.TERMINATE  # v18.0: 180s→120s
        if elapsed >= 60:
            return TimeoutLevel.EMERGENCY  # v18.0: 120s→60s
        if elapsed >= 30:
            return TimeoutLevel.DEGRADED   # v18.0: 60s→30s
        if elapsed >= 15:
            return TimeoutLevel.WARNING    # v18.0: 30s→15s
        return TimeoutLevel.NORMAL


class TimeoutGuard:
    """
    全局超时守护器 — Somn系统的2分钟安全网 [v18.0 优化：从3分钟调整为2分钟].

    核心特性:
    - 分级降级：15s/30s/60s/120s 四级阈值自动切换（v18.0前移）
    - 中间结果保留：超时时返回已有部分结果而非空值
    - 同步/异步双模式：protect()用于同步函数，aprotect()用于异步
    - 上下文监控：monitor()提供with语句式代码块保护
    - 线程安全：内部使用threading.Lock保护共享状态
    """

    GLOBAL_TIMEOUT = 120.0  # v18.0 优化：从180s→120s，加速全局终止

    def __init__(self, request_id: str = "", timeout_seconds: float = GLOBAL_TIMEOUT):
        now = time.monotonic()
        self.ctx = TimeoutContext(
            request_id=request_id or f"req_{datetime.now().strftime('%H%M%S%f')}",
            start_time=now,
            deadline=now + timeout_seconds,
        )
        self._lock = threading.Lock()
        self._handlers: dict[str, Callable] = {}
        self._active = True
        # [v1.0 fix] 复用线程池，避免每次protect调用创建新ThreadPoolExecutor
        from concurrent.futures import ThreadPoolExecutor
        self._protected_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="tg_protect")

    def shutdown(self, wait: bool = True) -> None:
        """关闭超时守护器，释放线程池资源"""
        self._active = False
        if hasattr(self, '_protected_executor'):
            self._protected_executor.shutdown(wait=wait)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown(wait=False)
        return False

    # ------------------------------------------------------------------
    # 降级处理器注册
    # ------------------------------------------------------------------

    def register_degradation_handler(self, level: TimeoutLevel, handler: Callable[[TimeoutContext], None]):
        """注册指定降级级别的回调处理函数"""
        self._handlers[level.value] = handler

    # ------------------------------------------------------------------
    # 级别查询与自动降级
    # ------------------------------------------------------------------

    @property
    def current_level(self) -> TimeoutLevel:
        """获取当前应该处于的降级级别"""
        if not self._active:
            return TimeoutLevel.TERMINATE
        return self.ctx.get_level_for_elapsed()

    def check_and_degrade(self) -> bool:
        """
        检查是否需要升级降级级别。
        
        Returns:
            True 如果刚刚触发了新的降级，False 如果无需变化
        """
        new_level = self.current_level
        # 比较级别的严重程度（ordinal越大越严重）
        if _level_ordinal(new_level) <= _level_ordinal(self.ctx.level):
            return False

        old_level = self.ctx.level
        self.ctx.level = new_level
        elapsed = self.ctx.elapsed
        step_msg = (
            f"[TimeoutGuard] LVL_UP: {old_level.value} -> {new_level.value} "
            f"(T+{elapsed:.1f}s, req={self.ctx.request_id})"
        )
        self.ctx.degradation_steps.append({
            "timestamp": elapsed,
            "from": old_level.value,
            "to": new_level.value,
        })
        logger.warning(step_msg)

        # [v10.2 Phase3] EMERGENCY/TERMINATE 级别自动保存快照
        if new_level in (TimeoutLevel.EMERGENCY, TimeoutLevel.TERMINATE):
            self.save_snapshot(reason=new_level.value)

        # 触发注册的降级处理器
        handler = self._handlers.get(new_level.value)
        if handler:
            try:
                handler(self.ctx)
            except Exception as e:
                logger.error(f"[TimeoutGuard] 降级处理器异常({new_level.value}): {e}")

        return True

    # ------------------------------------------------------------------
    # 中间结果记录
    # ------------------------------------------------------------------

    def record_partial(self, key: str, value: Any):
        """记录中间结果，用于超时时的部分返回"""
        with self._lock:
            self.ctx.partial_results[key] = value

    def get_partial(self, key: str, default: Any = None) -> Any:
        """获取已记录的中间结果"""
        with self._lock:
            return self.ctx.partial_results.get(key, default)

    def get_all_partials(self) -> dict:
        """获取所有中间结果副本"""
        with self._lock:
            return dict(self.ctx.partial_results)

    # ------------------------------------------------------------------
    # 上下文管理器 (monitor)
    # ------------------------------------------------------------------

    class MonitorContext:
        """监控上下文管理器 — 用于with语句包裹代码块"""

        def __init__(self, guard: 'TimeoutGuard', label: str, timeout: Optional[float] = None):
            self.guard = guard
            self.label = label
            self.timeout = timeout
            self.start_time = 0.0
            self._did_timeout = False

        def __enter__(self) -> 'TimeoutContext':
            self.start_time = time.monotonic()

            # 检查是否已经全局超时
            if self.guard.ctx.is_expired():
                self._did_timeout = True
                raise TimeoutError(
                    f"[{self.label}] 全局已超时(T+{self.guard.ctx.elapsed:.1f}s)"
                )

            # 自动检查并触发降级
            self.guard.check_and_degrade()
            return self.guard.ctx

        def __exit__(self, exc_type, exc_val, exc_tb):
            elapsed = time.monotonic() - self.start_time
            remaining = self.guard.ctx.remaining
            logger.debug(
                f"[{self.label}] 耗时={elapsed:.2f}s, 剩余={remaining:.1f}s, "
                f"级别={self.guard.ctx.level.value}"
            )
            # 吞掉超时异常，让上层继续执行降级逻辑
            if isinstance(exc_val, (TimeoutError, asyncio.TimeoutError)):
                logger.warning(f"[{self.label}] 超时中断({elapsed:.2f}s): {exc_val}")
                self._did_timeout = True
                return True
            return False

        @property
        def did_timeout(self) -> bool:
            return self._did_timeout

    def monitor(self, label: str, timeout: Optional[float] = None) -> MonitorContext:
        """
        创建监控上下文。
        
        Usage:
            with guard.monitor("Phase1 分析") as ctx:
                result = heavy_computation()
        """
        return self.MonitorContext(self, label, timeout)

    # ------------------------------------------------------------------
    # 同步函数装饰器 (protect)
    # ------------------------------------------------------------------

    def protect(self, timeout: float, fallback: Any, label: str = ""):
        """
        超时保护装饰器工厂 — 用于同步函数。
        
        在ThreadPoolExecutor中执行被包装函数，超时后返回fallback。
        自动考虑全局剩余时间，取局部超时和全局剩余时间的较小值。
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                func_label = label or func.__name__

                # 全局已超时时直接返回fallback
                if not self._active or self.ctx.is_expired():
                    logger.warning(
                        f"[{func_label}] 全局已超时(T+{self.ctx.elapsed:.1f}s), 直接返回fallback"
                    )
                    return fallback

                effective_timeout = min(timeout, self.ctx.remaining)
                if effective_timeout <= 0:
                    logger.warning(f"[{func_label}] 剩余时间不足, 返回fallback")
                    return fallback

                from concurrent.futures import TimeoutError as FuturesTimeout

                try:
                    # [v1.0] 复用 self._protected_executor（2线程池，__init__中创建）
                    future = self._protected_executor.submit(func, *args, **kwargs)
                    result = future.result(timeout=effective_timeout)
                    self.record_partial(func_label, result)
                    return result

                except FuturesTimeout:
                    logger.warning(
                        f"[{func_label}] 超时({effective_timeout:.1f}s), "
                        f"全局T+{self.ctx.elapsed:.1f}s"
                    )
                    self.check_and_degrade()
                    return fallback

                except Exception as e:
                    logger.error(f"[{func_label}] 异常: {type(e).__name__}: {e}")
                    return fallback

            return wrapper
        return decorator

    # ------------------------------------------------------------------
    # 异步函数装饰器 (aprotect)
    # ------------------------------------------------------------------

    def aprotect(self, timeout: float, fallback: Any, label: str = ""):
        """
        异步超时保护装饰器工厂 — 用于async函数。
        
        使用asyncio.wait_for实施真正的异步超时。
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs) -> Any:
                func_label = label or func.__name__

                if not self._active or self.ctx.is_expired():
                    logger.warning(
                        f"[{func_label}] 全局已超时(T+{self.ctx.elapsed:.1f}s), 直接返回fallback"
                    )
                    return fallback

                effective_timeout = min(timeout, self.ctx.remaining)
                if effective_timeout <= 0:
                    return fallback

                try:
                    result = await asyncio.wait_for(
                        func(*args, **kwargs),
                        timeout=effective_timeout
                    )
                    self.record_partial(func_label, result)
                    return result

                except asyncio.TimeoutError:
                    logger.warning(
                        f"[{func_label}] 异步超时({effective_timeout:.1f}s), "
                        f"全局T+{self.ctx.elapsed:.1f}s"
                    )
                    self.check_and_degrade()
                    return fallback

                except Exception as e:
                    logger.error(f"[{func_label}] 异常: {type(e).__name__}: {e}")
                    return fallback

            return async_wrapper
        return decorator

    # ------------------------------------------------------------------
    # 手动控制
    # ------------------------------------------------------------------

    def force_timeout(self):
        """手动触发超时事件（将deadline设为现在）[v10.2 Phase3 快照保存]"""
        self.ctx.deadline = time.monotonic()
        self.ctx.timeout_event.set()
        self._active = False
        # [v10.2] 强制超时时自动保存快照
        self.save_snapshot()
        logger.warning(
            f"[TimeoutGuard] 手动强制超时, T+{self.ctx.elapsed:.1f}s, "
            f"req={self.ctx.request_id}"
        )

    # ------------------------------------------------------------------
    # 超时快照自动保存 [v10.2 Phase3]
    # ------------------------------------------------------------------

    def save_snapshot(self, reason: str = "manual") -> Optional[str]:
        """
        [v10.2 Phase3] 超时时自动保存上下文快照到 data/timeouts/。

        快照包含：
        - 请求ID、开始时间、已耗时、截止时间
        - 当前降级级别和全部降级步骤
        - 所有已记录的中间结果（partial_results）
        - 快照生成原因

        Args:
            reason: 快照原因（manual/emergency/terminate）

        Returns:
            快照文件路径，保存失败返回None
        """
        try:
            from pathlib import Path
            import os
            import json as _json

            # 确保目录存在
            try:
                snapshot_dir = PROJECT_ROOT / "data" / "timeouts"
                snapshot_dir.mkdir(parents=True, exist_ok=True)
            except Exception:
                # 回退到临时目录
                snapshot_dir = Path(__import__("tempfile").gettempdir()) / "somn_timeouts"
                snapshot_dir.mkdir(parents=True, exist_ok=True)

            # 生成文件名
            ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            safe_id = self.ctx.request_id.replace("/", "_").replace("\\", "_")
            filename = f"{ts}_{safe_id}.json"
            snapshot_path = snapshot_dir / filename

            # 构建快照内容（去掉不可序列化的对象）
            def _sanitize(obj):
                if isinstance(obj, dict):
                    return {k: _sanitize(v) for k, v in obj.items()}
                if isinstance(obj, list):
                    return [_sanitize(x) for x in obj]
                if isinstance(obj, (str, int, float, bool, type(None))):
                    return obj
                try:
                    return repr(obj)
                except Exception:
                    return str(type(obj))

            snapshot_data = {
                "version": "v10.2",
                "snapshot_reason": reason,
                "generated_at": datetime.now().isoformat(),
                "request_id": self.ctx.request_id,
                "start_time": self.ctx.start_time,
                "deadline": self.ctx.deadline,
                "elapsed_s": round(self.ctx.elapsed, 2),
                "level": self.ctx.level.value,
                "degradation_steps": _sanitize(self.ctx.degradation_steps),
                "partial_results": _sanitize(self.ctx.partial_results),
                "active": self._active,
            }

            with open(snapshot_path, "w", encoding="utf-8") as f:
                _json.dump(snapshot_data, f, ensure_ascii=False, indent=2)

            logger.warning(
                f"[TimeoutGuard] 超时快照已保存: {snapshot_path} "
                f"(elapsed={snapshot_data['elapsed_s']}s, level={snapshot_data['level']})"
            )
            return str(snapshot_path)
        except Exception as e:
            logger.error(f"[TimeoutGuard] 快照保存失败: {e}")
            return None

    def deactivate(self):
        """停用此guard（不再阻止任何操作，但保留历史数据）"""
        self._active = False
        logger.debug(f"[TimeoutGuard] 已停用, req={self.ctx.request_id}")

    # ------------------------------------------------------------------
    # 状态摘要
    # ------------------------------------------------------------------

    def summary(self) -> dict:
        """返回当前状态的完整摘要（用于日志和诊断）"""
        return {
            "request_id": self.ctx.request_id,
            "elapsed_s": round(self.ctx.elapsed, 2),
            "remaining_s": round(self.ctx.remaining, 2),
            "current_level": self.ctx.level.value,
            "should_be_level": self.current_level.value,
            "is_expired": self.ctx.is_expired(),
            "degradation_count": len(self.ctx.degradation_steps),
            "partial_keys": list(self.ctx.partial_results.keys()),
            "active": self._active,
        }


# ============================================================
# 工厂函数 & 辅助工具
# ============================================================


def create_timeout_guard(request_id: str = "", timeout: float = 120.0) -> TimeoutGuard:
    """工厂函数：创建并配置默认降级处理器的超时守护器"""
    guard = TimeoutGuard(request_id=request_id, timeout_seconds=timeout)
    setup_default_handlers(guard)
    return guard


def _level_ordinal(level: TimeoutLevel) -> int:
    """获取级别的数值序数（越大越严重）"""
    ordinals = {
        TimeoutLevel.NORMAL: 0,
        TimeoutLevel.WARNING: 1,
        TimeoutLevel.DEGRADED: 2,
        TimeoutLevel.EMERGENCY: 3,
        TimeoutLevel.TERMINATE: 4,
    }
    return ordinals.get(level, 0)


def setup_default_handlers(guard: TimeoutGuard):
    """
    为Somn系统注册默认的三级降级处理器 [v18.0 优化：阈值更新+更激进降级].
    
    这些处理器在超时达到各级阈值时被自动调用，
    主要职责是记录降级信息到partial_results供最终输出参考。
    
    v18.0 阈值变化：WARNING 30s→15s, DEGRADED 60s→30s, EMERGENCY 120s→60s
    """

    def on_warning(ctx: TimeoutContext):
        """T+15s [v18.0]: 预警模式"""
        logger.info("[降级-预警] 进入预警模式(T+15s)，准备轻量备选路径")
        ctx.partial_results["_deg_warning"] = {
            "level": "warning",
            "message": "部分步骤可能启用备选路径",
            "triggered_at": ctx.elapsed,
        }

    def on_degraded(ctx: TimeoutContext):
        """T+30s [v18.0]: 降级模式（更激进）"""
        logger.warning("[降级-降级] T+30s 跳过非核心步骤")
        ctx.partial_results["_deg_degraded"] = {
            "level": "degraded",
            "skipped": ["web_search", "metaphysics", "ensemble", "deep_feasibility", "semantic_analysis"],
            "message": "已跳过非核心步骤以加速响应",
            "triggered_at": ctx.elapsed,
        }

    def on_emergency(ctx: TimeoutContext):
        """T+60s [v18.0]: 紧急模式（更激进）"""
        logger.error("[降级-紧急] T+60s 最小可用输出模式")
        ctx.partial_results["_deg_emergency"] = {
            "level": "emergency",
            "skipped": [
                "wisdom_schools", "claw_system", "coordinator",
                "unified_intelligence", "narrative_engine",
                "deep_reasoning", "learning",
            ],
            "mode": "llm_only",
            "message": "紧急模式：仅使用LLM直接生成回答",
            "triggered_at": ctx.elapsed,
        }

    guard.register_degradation_handler(TimeoutLevel.WARNING, on_warning)
    guard.register_degradation_handler(TimeoutLevel.DEGRADED, on_degraded)
    guard.register_degradation_handler(TimeoutLevel.EMERGENCY, on_emergency)


# ============================================================
# 便捷函数：快速检查超时状态（供各模块内联调用）
# ============================================================

def check_timeout(guard: Optional[TimeoutGuard]) -> bool:
    """
    快速检查guard是否存在且未超时。
    
    用法（在各模块中内联调用）：
        from src.core.timeout_guard import check_timeout
        
        def some_heavy_operation(ctx):
            if check_timeout(ctx.get("_timeout_guard")):
                return fallback_result
            ...
    """
    if guard is None:
        return False
    guard.check_and_degrade()
    return guard.ctx.is_expired()


def remaining_time(guard: Optional[TimeoutGuard]) -> float:
    """获取剩余时间（guard不存在或已失效时返回较大值避免误判）"""
    if guard is None or not guard._active:
        return 9999.0
    return guard.ctx.remaining


def should_skip_heavy_ops(guard: Optional[TimeoutGuard]) -> bool:
    """
    判断是否应跳过重度操作 [v18.0: 阈值更新].
    
    当处于DEGRADED(30s+)或EMERGENCY(60s+)级别时返回True。
    用于在运行时动态决定是否执行可选的重度计算。
    """
    if guard is None:
        return False
    ordinal = _level_ordinal(guard.current_level)
    return ordinal >= _level_ordinal(TimeoutLevel.DEGRADED)


def should_llm_only(guard: Optional[TimeoutGuard]) -> bool:
    """
    判断是否应仅使用LLM直出（跳过所有其他引擎）[v18.0: 阈值更新].
    
    当处于EMERGENCY(60s+)或TERMINATE级别时返回True。
    """
    if guard is None:
        return False
    ordinal = _level_ordinal(guard.current_level)
    return ordinal >= _level_ordinal(TimeoutLevel.EMERGENCY)
