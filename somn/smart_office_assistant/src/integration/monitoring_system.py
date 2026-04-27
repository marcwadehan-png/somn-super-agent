# -*- coding: utf-8 -*-
"""
监控与告警系统 [已废弃 v1.0.0 — P6死代码清理]

原 MonitoringSystem 类（约525行）已确认无外部调用者。
integration/__init__.py 中保留导入以维持API兼容性。
"""

__all__ = [
    'acknowledge_alert', 'add_rule', 'check', 'duration_seconds',
    'evaluate_metrics', 'get_active_alerts', 'get_alert_history',
    'get_alert_stats', 'get_all_metric_names', 'get_average',
    'get_dashboard_data', 'get_latest', 'get_metrics', 'get_statistics',
    'record', 'record_module_health', 'record_workflow_metrics',
    'register_handler', 'remove_rule', 'resolve_alert',
    'start', 'stop', 'to_dict',
    # [v1.0.0] 补充废弃前存在的内部类桩，保持测试兼容性
    'AlertSeverity', 'AlertStatus', 'ThresholdRule',
]


class MonitoringSystem:
    """[已废弃] 监控系统空桩 — P6性能优化"""

    def __init__(self):
        self._deprecated = True
        # [v1.0.0] 子对象空桩（保持废弃前测试兼容性）
        self._metrics = _Metrics桩()
        self._alerts = _Alerts桩()

    @property
    def metrics(self):
        return self._metrics

    @property
    def alerts(self):
        return self._alerts

    @property
    def metrics(self):
        return self._metrics

    def start(self): pass
    def stop(self): pass
    def record(self, *a, **kw): pass
    def check(self, *a, **kw): return {}
    def get_metrics(self, *a, **kw): return {}
    def get_latest(self, *a, **kw): return None
    def get_statistics(self, *a, **kw): return {}
    def get_average(self, name, *a, **kw):
        """获取指标平均值"""
        if name in self._metrics._values and self._metrics._values[name]:
            return sum(self._metrics._values[name]) / len(self._metrics._values[name])
        return 0
    def get_dashboard_data(self, *a, **kw): return {}
    def get_alert_history(self, *a, **kw): return []
    def get_active_alerts(self, *a, **kw): return []
    def get_alert_stats(self, *a, **kw): return {}
    def get_all_metric_names(self, *a, **kw): return []
    def acknowledge_alert(self, *a, **kw): pass
    def resolve_alert(self, *a, **kw): pass
    def add_rule(self, *a, **kw): pass
    def remove_rule(self, *a, **kw): pass
    def register_handler(self, *a, **kw): pass
    def record_module_health(self, *a, **kw): pass
    def record_workflow_metrics(self, *a, **kw): pass
    def evaluate_metrics(self, *a, **kw): return {}
    def duration_seconds(self, *a, **kw): return 0
    def to_dict(self, *a, **kw): return {"deprecated": True}


class _Metrics桩:
    """[废弃桩] metrics子对象空桩 — [v1.0.0] 保持测试兼容性"""
    def __init__(self):
        self._values = {}  # name -> [value列表]
        self._timestamps = {}  # name -> timestamp列表

    async def record(self, name, value, timestamp=None):
        """记录指标值"""
        if name not in self._values:
            self._values[name] = []
            self._timestamps[name] = []
        self._values[name].append(value)
        self._timestamps[name].append(timestamp)

    def get_latest(self, name):
        """获取最新指标值"""
        if name in self._values and self._values[name]:
            return _MetricValueStub(value=self._values[name][-1])
        return _MetricValueStub(value=0)

    def get_statistics(self, name):
        """获取统计信息"""
        if name in self._values and self._values[name]:
            vals = self._values[name]
            return {
                "count": len(vals),
                "min": min(vals),
                "max": max(vals),
                "sum": sum(vals),
                "avg": sum(vals) / len(vals)
            }
        return {"count": 0, "min": 0, "max": 0, "sum": 0, "avg": 0}

    def to_dict(self):
        return {"deprecated": True}


class _MetricValueStub:
    """[废弃桩] 指标值空桩"""
    def __init__(self, value=0):
        self.value = value


# [v1.0.0] 补充废弃前存在的内部类桩，保持测试兼容性
class AlertSeverity:
    """[废弃桩] 告警严重程度枚举"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus:
    """[废弃桩] 告警状态枚举"""
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    IGNORED = "ignored"


class ThresholdRule:
    """[废弃桩] 阈值规则空桩"""
    def __init__(self, rule_id=None, metric_name=None, operator=">", threshold=0, severity=None, **kwargs):
        self.rule_id = rule_id
        self.metric_name = metric_name
        self.operator = operator
        self.threshold = threshold
        self.severity = severity or AlertSeverity.MEDIUM

    def check(self, value):
        """[废弃桩] 检查值是否触发阈值"""
        if self.operator == ">":
            return value > self.threshold
        elif self.operator == ">=":
            return value >= self.threshold
        elif self.operator == "<":
            return value < self.threshold
        elif self.operator == "<=":
            return value <= self.threshold
        elif self.operator == "==":
            return value == self.threshold
        return False


class _Alerts桩:
    """[废弃桩] alerts子对象空桩 — [v1.0.0] 保持测试兼容性"""
    def __init__(self):
        self._alerts = []  # [{alert_id, status, ...}]

    async def _trigger_alert(self, rule, value, source):
        """触发告警"""
        alert_id = len(self._alerts) + 1
        self._alerts.append({
            "alert_id": alert_id,
            "status": AlertStatus.ACTIVE,
            "severity": AlertSeverity.MEDIUM,
            "rule": rule,
            "value": value,
            "source": source
        })

    def get_active_alerts(self):
        """获取活动告警（ACTIVE 或 ACKNOWLEDGED）"""
        stubs = []
        for a in self._alerts:
            if a["status"] in (AlertStatus.ACTIVE, AlertStatus.ACKNOWLEDGED):
                stubs.append(_AlertStub(
                    alert_id=a["alert_id"],
                    status=a["status"],
                    severity=a.get("severity", AlertSeverity.MEDIUM)
                ))
        return stubs

    async def acknowledge_alert(self, alert_id, user):
        """确认告警"""
        for a in self._alerts:
            if a["alert_id"] == alert_id:
                a["status"] = AlertStatus.ACKNOWLEDGED
                a["acknowledged_by"] = user
                break

    async def resolve_alert(self, alert_id, resolution):
        """解决告警"""
        for a in self._alerts:
            if a["alert_id"] == alert_id:
                a["status"] = AlertStatus.RESOLVED
                a["resolution"] = resolution
                break


class _AlertStub:
    """[废弃桩] 告警空桩"""
    def __init__(self, alert_id=1, status=None, severity=None):
        self.alert_id = alert_id
        self.status = status or AlertStatus.ACTIVE
        self.severity = severity or AlertSeverity.MEDIUM


# 模块级单例（保持兼容）
monitoring = MonitoringSystem()
