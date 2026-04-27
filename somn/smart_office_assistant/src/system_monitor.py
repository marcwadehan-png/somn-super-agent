"""
系统资源监控模块 - 监控系统资源使用情况，防止资源耗尽导致卡死

功能：
1. 监控 CPU、内存、磁盘使用情况
2. 超过阈值时记录警告日志
3. 超过阈值时触发告警（集成 AlertManager）
4. 提供 API 端点查询资源使用情况和告警历史
"""

import time
import threading
import logging
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

# 导入告警管理器（可选，如果导入失败则不使用告警）
try:
    from src.utils.alert_manager import AlertManager, AlertLevel, get_alert_manager
    _HAS_ALERT_MANAGER = True
except ImportError:
    _HAS_ALERT_MANAGER = False
    AlertManager = None
    AlertLevel = None
    get_alert_manager = None


@dataclass
class ResourceThresholds:
    """资源阈值配置"""
    cpu_percent: float = 90.0          # CPU 使用率阈值（%）
    memory_percent: float = 90.0       # 内存使用率阈值（%）
    disk_percent: float = 90.0         # 磁盘使用率阈值（%）
    memory_available_mb: float = 500.0  # 可用内存阈值（MB）


@dataclass
class ResourceStatus:
    """资源状态"""
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    memory_available_mb: float = 0.0
    disk_percent: float = 0.0
    warning: bool = False
    warning_message: str = ""


class SystemMonitor:
    """系统资源监控器"""

    def __init__(
        self,
        check_interval: float = 60.0,
        thresholds: Optional[ResourceThresholds] = None,
        enable_alerts: bool = True,
    ):
        """
        初始化系统监控器

        Args:
            check_interval: 检查间隔（秒），默认60秒
            thresholds: 资源阈值配置
            enable_alerts: 是否启用告警（默认启用）
        """
        self._check_interval = check_interval
        self._thresholds = thresholds or ResourceThresholds()
        self._status = ResourceStatus()
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.RLock()
        self._enable_alerts = enable_alerts and _HAS_ALERT_MANAGER

        # 告警管理器
        self._alert_manager: Optional[AlertManager] = None
        if self._enable_alerts:
            try:
                self._alert_manager = get_alert_manager()
                # 设置不同资源的冷却时间
                self._alert_manager.set_cooldown("system_monitor:cpu", 300.0)  # CPU告警冷却5分钟
                self._alert_manager.set_cooldown("system_monitor:memory", 300.0)  # 内存告警冷却5分钟
                self._alert_manager.set_cooldown("system_monitor:disk", 600.0)  # 磁盘告警冷却10分钟
                self._alert_manager.set_cooldown("system_monitor:memory_avail", 300.0)  # 可用内存告警冷却5分钟
                logger.info("[系统监控] 告警管理器已集成")
            except Exception as e:
                logger.warning(f"[系统监控] 告警管理器初始化失败: {e}")
                self._alert_manager = None
                self._enable_alerts = False

        # 尝试导入 psutil
        self._has_psutil = False
        try:
            import psutil
            self._psutil = psutil
            self._has_psutil = True
            logger.info("[系统监控] psutil 可用，启用系统资源监控")
        except ImportError:
            logger.warning("[系统监控] psutil 未安装，系统资源监控功能受限")
            self._psutil = None

    def start(self):
        """启动监控线程"""
        if self._running:
            logger.warning("[系统监控] 监控线程已在运行")
            return

        self._running = True
        self._thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True,
            name="system-monitor",
        )
        self._thread.start()
        logger.info(f"[系统监控] 监控线程已启动（间隔: {self._check_interval}s）")

    def stop(self):
        """停止监控线程"""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5.0)
            logger.info("[系统监控] 监控线程已停止")

    def _monitor_loop(self):
        """监控循环"""
        while self._running:
            try:
                self._check_resources()
            except Exception as e:
                logger.error(f"[系统监控] 检查资源时出错: {e}")

            # 等待下次检查
            time.sleep(self._check_interval)

    def _check_resources(self):
        """检查系统资源"""
        if not self._has_psutil:
            # 没有 psutil，尝试使用简化检查
            self._check_resources_simple()
            return

        try:
            import psutil

            # CPU 使用率
            cpu_percent = psutil.cpu_percent(interval=1.0)

            # 内存使用情况
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available_mb = memory.available / 1024 / 1024

            # 磁盘使用情况
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent

            # 更新状态
            with self._lock:
                self._status.cpu_percent = cpu_percent
                self._status.memory_percent = memory_percent
                self._status.memory_available_mb = memory_available_mb
                self._status.disk_percent = disk_percent

            # 检查阈值（区分 WARNING 和 CRITICAL）
            warnings = []
            criticals = []

            # CPU 检查
            if cpu_percent > self._thresholds.cpu_percent:
                msg = f"CPU 使用率过高: {cpu_percent:.1f}% > {self._thresholds.cpu_percent}%"
                # 超过 95% 为 CRITICAL
                if cpu_percent > 95.0:
                    criticals.append(msg)
                else:
                    warnings.append(msg)

            # 内存检查
            if memory_percent > self._thresholds.memory_percent:
                msg = f"内存使用率过高: {memory_percent:.1f}% > {self._thresholds.memory_percent}%"
                # 超过 95% 为 CRITICAL
                if memory_percent > 95.0:
                    criticals.append(msg)
                else:
                    warnings.append(msg)

            # 可用内存检查
            if memory_available_mb < self._thresholds.memory_available_mb:
                msg = f"可用内存不足: {memory_available_mb:.1f}MB < {self._thresholds.memory_available_mb}MB"
                # 低于 100MB 为 CRITICAL
                if memory_available_mb < 100.0:
                    criticals.append(msg)
                else:
                    warnings.append(msg)

            # 磁盘检查
            if disk_percent > self._thresholds.disk_percent:
                msg = f"磁盘使用率过高: {disk_percent:.1f}% > {self._thresholds.disk_percent}%"
                # 超过 98% 为 CRITICAL
                if disk_percent > 98.0:
                    criticals.append(msg)
                else:
                    warnings.append(msg)

            # 触发告警
            alert_triggered = False

            # 先处理 CRITICAL 告警
            for msg in criticals:
                alert_triggered = True
                if self._alert_manager:
                    try:
                        self._alert_manager.trigger_critical("system_monitor", msg)
                    except Exception as e:
                        logger.error(f"[系统监控] 触发 CRITICAL 告警失败: {e}")

            # 再处理 WARNING 告警
            for msg in warnings:
                alert_triggered = True
                if self._alert_manager:
                    try:
                        self._alert_manager.trigger_warning("system_monitor", msg)
                    except Exception as e:
                        logger.error(f"[系统监控] 触发 WARNING 告警失败: {e}")

            # 输出警告日志
            all_msgs = criticals + warnings
            if all_msgs:
                warning_msg = "; ".join(all_msgs)
                with self._lock:
                    self._status.warning = True
                    self._status.warning_message = warning_msg

                if criticals:
                    logger.critical(f"[系统监控] 🚨 资源严重告警: {warning_msg}")
                else:
                    logger.warning(f"[系统监控] ⚠️ 资源警告: {warning_msg}")
            else:
                with self._lock:
                    self._status.warning = False
                    self._status.warning_message = ""
                logger.debug(f"[系统监控] 资源正常: CPU={cpu_percent:.1f}%, MEM={memory_percent:.1f}%, DISK={disk_percent:.1f}%")

        except Exception as e:
            logger.error(f"[系统监控] 检查资源时出错: {e}")

    def _check_resources_simple(self):
        """简化资源检查（无 psutil）"""
        # 这里可以添加不使用 psutil 的资源检查方法
        # 例如：检查 /proc/meminfo (Linux) 或系统命令 (Windows)
        logger.debug("[系统监控] 使用简化资源检查（无 psutil）")

    def get_status(self) -> Dict[str, Any]:
        """获取当前资源状态"""
        with self._lock:
            return {
                "cpu_percent": self._status.cpu_percent,
                "memory_percent": self._status.memory_percent,
                "memory_available_mb": self._status.memory_available_mb,
                "disk_percent": self._status.disk_percent,
                "warning": self._status.warning,
                "warning_message": self._status.warning_message,
                "has_psutil": self._has_psutil,
            }

    def update_thresholds(
        self,
        cpu_percent: Optional[float] = None,
        memory_percent: Optional[float] = None,
        disk_percent: Optional[float] = None,
        memory_available_mb: Optional[float] = None,
    ):
        """更新资源阈值"""
        if cpu_percent is not None:
            self._thresholds.cpu_percent = cpu_percent
        if memory_percent is not None:
            self._thresholds.memory_percent = memory_percent
        if disk_percent is not None:
            self._thresholds.disk_percent = disk_percent
        if memory_available_mb is not None:
            self._thresholds.memory_available_mb = memory_available_mb

        logger.info(f"[系统监控] 阈值已更新: CPU={self._thresholds.cpu_percent}%, MEM={self._thresholds.memory_percent}%, DISK={self._thresholds.disk_percent}%, AVAIL={self._thresholds.memory_available_mb}MB")

    def get_alerts(
        self,
        limit: Optional[int] = None,
        level: Optional[str] = None,
        since: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        获取告警历史（从告警管理器）

        Args:
            limit: 返回的最大记录数
            level: 按级别过滤（"info"/"warning"/"critical"）
            since: 只返回该时间戳之后的告警

        Returns:
            List[Dict]: 告警记录列表
        """
        if not self._alert_manager:
            return []

        # 转换 level 字符串为 AlertLevel
        alert_level = None
        if level is not None:
            try:
                alert_level = AlertLevel(level)
            except ValueError:
                logger.warning(f"[系统监控] 无效的告警级别: {level}")
                return []

        alerts = self._alert_manager.get_history(
            limit=limit,
            level=alert_level,
            source="system_monitor",
            since=since,
        )

        # 转换为字典格式
        return [
            {
                "timestamp": a.timestamp,
                "time_str": a.time_str,
                "level": a.level_str,
                "source": a.source,
                "message": a.message,
                "details": a.details,
            }
            for a in alerts
        ]

    def get_alert_stats(self) -> Dict[str, Any]:
        """获取告警统计"""
        if not self._alert_manager:
            return {"enabled": False}
        stats = self._alert_manager.get_stats()
        stats["enabled"] = True
        return stats


# 全局监控器实例
_global_monitor: Optional[SystemMonitor] = None
_monitor_lock = threading.RLock()


def get_system_monitor(
    check_interval: float = 60.0,
    thresholds: Optional[ResourceThresholds] = None,
    enable_alerts: bool = True,
) -> SystemMonitor:
    """获取全局系统监控器实例"""
    global _global_monitor

    with _monitor_lock:
        if _global_monitor is None:
            _global_monitor = SystemMonitor(
                check_interval=check_interval,
                thresholds=thresholds,
                enable_alerts=enable_alerts,
            )
        return _global_monitor


def start_system_monitoring(
    check_interval: float = 60.0,
    thresholds: Optional[ResourceThresholds] = None,
    enable_alerts: bool = True,
):
    """启动系统监控"""
    monitor = get_system_monitor(check_interval, thresholds, enable_alerts)
    monitor.start()
    return monitor


def stop_system_monitoring():
    """停止系统监控"""
    global _global_monitor

    with _monitor_lock:
        if _global_monitor:
            _global_monitor.stop()
            _global_monitor = None


if __name__ == "__main__":
    # 测试
    import time

    # 启动监控
    monitor = start_system_monitoring(check_interval=10.0)

    # 查询状态
    for i in range(6):
        status = monitor.get_status()
        print(f"状态: {status}")
        time.sleep(10)

    # 停止监控
    stop_system_monitoring()
    print("监控已停止")
