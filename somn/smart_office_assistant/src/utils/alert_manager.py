"""
告警管理器模块 - 统一管理系统告警，防止告警风暴

功能：
1. 告警级别管理（INFO/WARNING/CRITICAL）
2. 告警频率限制（防止告警风暴）
3. 告警历史记录（保留最近N条）
4. 告警回调机制（支持GUI通知、日志、Webhook等）
5. 线程安全
"""

import time
import threading
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
from collections import deque
import logging

logger = logging.getLogger(__name__)


class AlertLevel(Enum):
    """告警级别"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class Alert:
    """告警记录"""
    timestamp: float  # 时间戳
    level: AlertLevel  # 告警级别
    source: str  # 源模块（如 "system_monitor", "circuit_breaker"）
    message: str  # 告警消息
    details: Dict[str, Any] = field(default_factory=dict)  # 详细信息

    def __str__(self) -> str:
        level_emoji = {
            AlertLevel.INFO: "ℹ️",
            AlertLevel.WARNING: "⚠️",
            AlertLevel.CRITICAL: "🚨",
        }
        emoji = level_emoji.get(self.level, "ℹ️")
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp))
        return f"{emoji} [{time_str}] [{self.source}] {self.message}"

    @property
    def level_str(self) -> str:
        return self.level.value

    @property
    def time_str(self) -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp))


class AlertManager:
    """
    告警管理器

    功能：
    1. 接收并过滤告警（频率限制）
    2. 记录告警历史
    3. 触发告警回调（通知GUI、日志等）
    """

    def __init__(
        self,
        max_history: int = 100,
        default_cooldown: float = 60.0,
    ):
        """
        初始化告警管理器

        Args:
            max_history: 最大告警历史记录数
            default_cooldown: 默认告警冷却时间（秒），相同告警在冷却时间内只会触发一次
        """
        self._max_history = max_history
        self._default_cooldown = default_cooldown
        self._lock = threading.RLock()

        # 告警历史（双端队列，自动淘汰旧记录）
        self._history: deque[Alert] = deque(maxlen=max_history)

        # 告警冷却时间记录（key: (source, message), value: 上次告警时间戳）
        self._cooldown: Dict[str, float] = {}

        # 自定义冷却时间（per-source 或 per-source+message）
        self._custom_cooldowns: Dict[str, float] = {}

        # 告警回调列表
        self._callbacks: List[Callable[[Alert], None]] = []

        # 告警统计
        self._stats = {
            "total_alerts": 0,
            "filtered_alerts": 0,  # 被频率限制过滤的告警数
            "by_level": {
                AlertLevel.INFO: 0,
                AlertLevel.WARNING: 0,
                AlertLevel.CRITICAL: 0,
            },
        }

        logger.info(
            f"[告警管理器] 初始化完成 "
            f"(max_history={max_history}, default_cooldown={default_cooldown}s)"
        )

    def set_cooldown(self, source: str, cooldown: float, message: Optional[str] = None):
        """
        设置特定源或特定告警的冷却时间

        Args:
            source: 源模块名
            cooldown: 冷却时间（秒）
            message: 告警消息（可选，如果提供则只对该消息生效）
        """
        key = f"{source}:{message}" if message else source
        self._custom_cooldowns[key] = cooldown
        logger.debug(f"[告警管理器] 设置冷却时间: {key} = {cooldown}s")

    def register_callback(self, callback: Callable[[Alert], None]):
        """
        注册告警回调

        回调函数会在告警触发时被调用（如果在冷却时间内则不会触发）

        Args:
            callback: 回调函数，接受 Alert 参数
        """
        with self._lock:
            self._callbacks.append(callback)
            logger.debug(f"[告警管理器] 注册回调: {callback.__name__ if hasattr(callback, '__name__') else callback}")

    def unregister_callback(self, callback: Callable[[Alert], None]):
        """取消注册告警回调"""
        with self._lock:
            if callback in self._callbacks:
                self._callbacks.remove(callback)
                logger.debug(f"[告警管理器] 取消注册回调")

    def trigger(
        self,
        level: AlertLevel,
        source: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        force: bool = False,
    ) -> bool:
        """
        触发告警

        Args:
            level: 告警级别
            source: 源模块
            message: 告警消息
            details: 详细信息（可选）
            force: 是否强制触发（忽略冷却时间）

        Returns:
            bool: 是否成功触发（如果因冷却被过滤则返回 False）
        """
        now = time.time()
        cooldown_key = f"{source}:{message}"

        with self._lock:
            # 检查冷却时间
            if not force:
                last_time = self._cooldown.get(cooldown_key)
                if last_time is not None:
                    # 获取该告警的冷却时间
                    cooldown = self._custom_cooldowns.get(
                        f"{source}:{message}",
                        self._custom_cooldowns.get(source, self._default_cooldown),
                    )
                    if now - last_time < cooldown:
                        # 还在冷却时间内，过滤该告警
                        self._stats["filtered_alerts"] += 1
                        logger.debug(
                            f"[告警管理器] 告警被过滤（冷却中）: [{source}] {message}"
                        )
                        return False

            # 创建告警记录
            alert = Alert(
                timestamp=now,
                level=level,
                source=source,
                message=message,
                details=details or {},
            )

            # 更新冷却时间
            self._cooldown[cooldown_key] = now

            # 记录历史
            self._history.append(alert)

            # 更新统计
            self._stats["total_alerts"] += 1
            self._stats["by_level"][level] += 1

            # 触发回调
            for callback in self._callbacks:
                try:
                    callback(alert)
                except Exception as e:
                    logger.error(f"[告警管理器] 回调执行失败: {e}")

            # 记录日志
            log_msg = f"[告警管理器] {alert}"
            if level == AlertLevel.CRITICAL:
                logger.critical(log_msg)
            elif level == AlertLevel.WARNING:
                logger.warning(log_msg)
            else:
                logger.info(log_msg)

            return True

    def trigger_info(self, source: str, message: str, details: Optional[Dict] = None, force: bool = False) -> bool:
        """触发 INFO 级别告警"""
        return self.trigger(AlertLevel.INFO, source, message, details, force)

    def trigger_warning(self, source: str, message: str, details: Optional[Dict] = None, force: bool = False) -> bool:
        """触发 WARNING 级别告警"""
        return self.trigger(AlertLevel.WARNING, source, message, details, force)

    def trigger_critical(self, source: str, message: str, details: Optional[Dict] = None, force: bool = False) -> bool:
        """触发 CRITICAL 级别告警"""
        return self.trigger(AlertLevel.CRITICAL, source, message, details, force)

    def get_history(
        self,
        limit: Optional[int] = None,
        level: Optional[AlertLevel] = None,
        source: Optional[str] = None,
        since: Optional[float] = None,
    ) -> List[Alert]:
        """
        获取告警历史

        Args:
            limit: 返回的最大记录数
            level: 按级别过滤
            source: 按源模块过滤
            since: 只返回该时间戳之后的告警

        Returns:
            List[Alert]: 告警记录列表（按时间倒序）
        """
        with self._lock:
            history = list(self._history)

        # 过滤
        if level is not None:
            history = [a for a in history if a.level == level]
        if source is not None:
            history = [a for a in history if a.source == source]
        if since is not None:
            history = [a for a in history if a.timestamp >= since]

        # 按时间倒序（最新的在前）
        history.reverse()

        # 限制返回数量
        if limit is not None:
            history = history[:limit]

        return history

    def get_stats(self) -> Dict[str, Any]:
        """获取告警统计"""
        with self._lock:
            return {
                "total_alerts": self._stats["total_alerts"],
                "filtered_alerts": self._stats["filtered_alerts"],
                "by_level": {
                    k.value: v for k, v in self._stats["by_level"].items()
                },
                "history_count": len(self._history),
                "callbacks_count": len(self._callbacks),
            }

    def clear_history(self, level: Optional[AlertLevel] = None) -> int:
        """
        清空告警历史

        Args:
            level: 按级别清除（None表示全部清除）

        Returns:
            int: 清除的告警数量
        """
        with self._lock:
            if level is None:
                count = len(self._history)
                # 统计各级别数量以便后续更新
                level_counts = {}
                for a in self._history:
                    level_counts[a.level] = level_counts.get(a.level, 0) + 1
                self._history.clear()
                self._cooldown.clear()
                # 更新统计
                self._stats["total_alerts"] = 0
                for lvl, cnt in level_counts.items():
                    self._stats["by_level"][lvl] = 0
                logger.info("[告警管理器] 告警历史已全部清空")
            else:
                # 只清除指定级别的告警
                original_count = len(self._history)
                cleared_count = 0
                # 分离保留和清除的告警
                remaining = []
                for a in self._history:
                    if a.level == level:
                        cleared_count += 1
                    else:
                        remaining.append(a)
                self._history = remaining
                # 清除该级别的冷却记录
                keys_to_remove = [k for k in self._cooldown.keys()
                                if k.endswith(f":{level.value}") or k.startswith(level.value)]
                for k in keys_to_remove:
                    self._cooldown.pop(k, None)
                # 更新统计
                self._stats["total_alerts"] -= cleared_count
                self._stats["by_level"][level] = 0
                count = cleared_count
                logger.info(f"[告警管理器] 告警历史已清除 {count} 条 {level.value} 级别")
            return count

    def cleanup(self):
        """清理资源"""
        with self._lock:
            self._callbacks.clear()
            self._cooldown.clear()
            logger.info("[告警管理器] 已清理")


# ---------------------------------------------------------------------------
# 全局告警管理器
# ---------------------------------------------------------------------------

_global_alert_manager: Optional[AlertManager] = None
_alert_manager_lock = threading.RLock()


def get_alert_manager(
    max_history: int = 100,
    default_cooldown: float = 60.0,
) -> AlertManager:
    """获取全局告警管理器实例"""
    global _global_alert_manager

    with _alert_manager_lock:
        if _global_alert_manager is None:
            _global_alert_manager = AlertManager(
                max_history=max_history,
                default_cooldown=default_cooldown,
            )
        return _global_alert_manager


def trigger_alert(
    level: AlertLevel,
    source: str,
    message: str,
    details: Optional[Dict[str, Any]] = None,
    force: bool = False,
) -> bool:
    """快捷函数：触发告警"""
    return get_alert_manager().trigger(level, source, message, details, force)


def trigger_info(source: str, message: str, details: Optional[Dict] = None, force: bool = False) -> bool:
    """快捷函数：触发 INFO 告警"""
    return get_alert_manager().trigger_info(source, message, details, force)


def trigger_warning(source: str, message: str, details: Optional[Dict] = None, force: bool = False) -> bool:
    """快捷函数：触发 WARNING 告警"""
    return get_alert_manager().trigger_warning(source, message, details, force)


def trigger_critical(source: str, message: str, details: Optional[Dict] = None, force: bool = False) -> bool:
    """快捷函数：触发 CRITICAL 告警"""
    return get_alert_manager().trigger_critical(source, message, details, force)


if __name__ == "__main__":
    # 测试
    import time

    # 创建告警管理器
    am = AlertManager(max_history=10, default_cooldown=5.0)

    # 注册回调
    def print_callback(alert: Alert):
        print(f"  [回调] {alert}")

    am.register_callback(print_callback)

    # 测试告警触发
    print("=== 测试告警触发 ===")
    am.trigger_warning("test", "测试告警 1")
    am.trigger_warning("test", "测试告警 1")  # 应该被过滤（冷却中）
    am.trigger_warning("test", "测试告警 2")  # 不同消息，应该触发

    # 等待冷却时间过期
    print("\n等待冷却时间过期...")
    time.sleep(6)

    am.trigger_warning("test", "测试告警 1")  # 冷却已过期，应该触发

    # 查看历史
    print("\n=== 告警历史 ===")
    for alert in am.get_history():
        print(f"  {alert}")

    # 查看统计
    print(f"\n=== 统计 ===")
    print(f"  {am.get_stats()}")
