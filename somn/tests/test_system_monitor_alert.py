"""
系统监控和告警机制单元测试

测试内容：
1. AlertManager 基础功能
2. 告警频率限制
3. 告警历史记录
4. SystemMonitor 集成告警
"""

import unittest
import time
import threading
from unittest.mock import Mock, patch, MagicMock

# 导入被测模块
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'smart_office_assistant'))


class TestAlertLevel(unittest.TestCase):
    """测试告警级别枚举"""

    def test_alert_level_values(self):
        from src.utils.alert_manager import AlertLevel
        self.assertEqual(AlertLevel.INFO.value, "info")
        self.assertEqual(AlertLevel.WARNING.value, "warning")
        self.assertEqual(AlertLevel.CRITICAL.value, "critical")


class TestAlert(unittest.TestCase):
    """测试告警记录类"""

    def test_alert_creation(self):
        from src.utils.alert_manager import Alert, AlertLevel

        alert = Alert(
            timestamp=time.time(),
            level=AlertLevel.WARNING,
            source="test",
            message="测试告警",
            details={"key": "value"},
        )

        self.assertEqual(alert.level, AlertLevel.WARNING)
        self.assertEqual(alert.source, "test")
        self.assertEqual(alert.message, "测试告警")
        self.assertIsInstance(alert.time_str, str)
        self.assertIsInstance(str(alert), str)

    def test_alert_level_str(self):
        from src.utils.alert_manager import Alert, AlertLevel

        alert = Alert(
            timestamp=time.time(),
            level=AlertLevel.CRITICAL,
            source="test",
            message="严重告警",
        )

        self.assertEqual(alert.level_str, "critical")


class TestAlertManager(unittest.TestCase):
    """测试告警管理器"""

    def setUp(self):
        from src.utils.alert_manager import AlertManager, AlertLevel
        self.AlertLevel = AlertLevel
        self.manager = AlertManager(max_history=10, default_cooldown=1.0)

    def tearDown(self):
        self.manager.cleanup()

    def test_trigger_and_history(self):
        """测试触发告警和历史记录"""
        # 触发告警
        result = self.manager.trigger_warning("test", "测试告警")
        self.assertTrue(result)

        # 检查历史
        history = self.manager.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].message, "测试告警")
        self.assertEqual(history[0].level, self.AlertLevel.WARNING)

    def test_cooldown_filtering(self):
        """测试告警频率限制"""
        # 第一次触发
        result1 = self.manager.trigger_warning("test", "重复告警")
        self.assertTrue(result1)

        # 立即再次触发（应该在冷却中）
        result2 = self.manager.trigger_warning("test", "重复告警")
        self.assertFalse(result2)

        # 检查统计
        stats = self.manager.get_stats()
        self.assertEqual(stats["filtered_alerts"], 1)

    def test_cooldown_expiry(self):
        """测试冷却时间过期"""
        # 设置短冷却时间
        self.manager.set_cooldown("test", 0.5)

        # 第一次触发
        result1 = self.manager.trigger_warning("test", "冷却测试")
        self.assertTrue(result1)

        # 立即再次触发（应该在冷却中）
        result2 = self.manager.trigger_warning("test", "冷却测试")
        self.assertFalse(result2)

        # 等待冷却时间过期
        time.sleep(0.6)

        # 再次触发（应该成功）
        result3 = self.manager.trigger_warning("test", "冷却测试")
        self.assertTrue(result3)

    def test_force_trigger(self):
        """测试强制触发（忽略冷却）"""
        # 第一次触发
        self.manager.trigger_warning("test", "强制告警")

        # 立即再次触发（忽略冷却）
        result = self.manager.trigger_warning("test", "强制告警", force=True)
        self.assertTrue(result)

        # 应该有2条历史记录
        history = self.manager.get_history()
        self.assertEqual(len(history), 2)

    def test_different_messages_no_cooldown(self):
        """测试不同消息不受冷却影响"""
        # 触发不同消息
        result1 = self.manager.trigger_warning("test", "告警1")
        result2 = self.manager.trigger_warning("test", "告警2")

        self.assertTrue(result1)
        self.assertTrue(result2)

        # 应该有2条历史记录
        history = self.manager.get_history()
        self.assertEqual(len(history), 2)

    def test_callback(self):
        """测试告警回调"""
        callback_mock = Mock()
        self.manager.register_callback(callback_mock)

        # 触发告警
        self.manager.trigger_warning("test", "回调测试")

        # 检查回调是否被调用
        callback_mock.assert_called_once()
        alert_arg = callback_mock.call_args[0][0]
        self.assertIsInstance(alert_arg, self.manager._history[0].__class__)

    def test_callback_error_handling(self):
        """测试回调错误处理（一个回调失败不应影响其他回调）"""
        callback_ok = Mock()
        callback_fail = Mock(side_effect=Exception("回调失败"))
        callback_ok2 = Mock()

        self.manager.register_callback(callback_ok)
        self.manager.register_callback(callback_fail)
        self.manager.register_callback(callback_ok2)

        # 触发告警（应该触发所有回调，即使有一个失败）
        self.manager.trigger_warning("test", "回调错误处理测试")

        # 检查回调是否被调用
        callback_ok.assert_called_once()
        callback_fail.assert_called_once()
        callback_ok2.assert_called_once()

    def test_get_history_filter_by_level(self):
        """测试按级别过滤历史"""
        self.manager.trigger_info("test", "信息告警")
        self.manager.trigger_warning("test", "警告告警")
        self.manager.trigger_critical("test", "严重告警")

        # 过滤 WARNING 级别
        warnings = self.manager.get_history(level=self.AlertLevel.WARNING)
        self.assertEqual(len(warnings), 1)
        self.assertEqual(warnings[0].level, self.AlertLevel.WARNING)

    def test_get_history_filter_by_source(self):
        """测试按源模块过滤历史"""
        self.manager.trigger_warning("source1", "告警1")
        self.manager.trigger_warning("source2", "告警2")

        # 过滤 source1
        alerts = self.manager.get_history(source="source1")
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].source, "source1")

    def test_get_history_filter_by_since(self):
        """测试按时间过滤历史"""
        # 触发告警
        self.manager.trigger_warning("test", "时间过滤测试")
        time.sleep(0.1)
        since = time.time()

        # 再触发一个告警
        self.manager.trigger_warning("test", "时间过滤测试2")

        # 只获取 since 之后的告警
        alerts = self.manager.get_history(since=since)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].message, "时间过滤测试2")

    def test_get_history_limit(self):
        """测试限制返回数量"""
        for i in range(5):
            self.manager.trigger_warning("test", f"告警{i}")

        # 限制返回3条
        alerts = self.manager.get_history(limit=3)
        self.assertEqual(len(alerts), 3)

    def test_get_stats(self):
        """测试获取统计信息"""
        self.manager.trigger_info("test", "信息")
        self.manager.trigger_warning("test", "警告")
        self.manager.trigger_critical("test", "严重")

        stats = self.manager.get_stats()
        self.assertEqual(stats["total_alerts"], 3)
        self.assertEqual(stats["by_level"]["info"], 1)
        self.assertEqual(stats["by_level"]["warning"], 1)
        self.assertEqual(stats["by_level"]["critical"], 1)

    def test_clear_history(self):
        """测试清空历史"""
        self.manager.trigger_warning("test", "测试告警")
        self.assertEqual(len(self.manager.get_history()), 1)

        self.manager.clear_history()
        self.assertEqual(len(self.manager.get_history()), 0)

    def test_max_history_truncate(self):
        """测试历史记录自动淘汰"""
        from src.utils.alert_manager import AlertManager
        manager = AlertManager(max_history=3, default_cooldown=0)
        try:
            for i in range(5):
                manager.trigger_warning("test", f"告警{i}")

            # 应该只保留最近3条
            history = manager.get_history()
            self.assertEqual(len(history), 3)
            # 最新的应该在前面
            self.assertIn("告警4", history[0].message)
        finally:
            manager.cleanup()


class TestSystemMonitorIntegration(unittest.TestCase):
    """测试 SystemMonitor 集成告警"""

    def setUp(self):
        from src.system_monitor import SystemMonitor, ResourceThresholds
        from src.utils.alert_manager import AlertManager, AlertLevel

        # 保存 AlertManager 类引用，供测试方法使用
        self.AlertManager = AlertManager
        self.AlertLevel = AlertLevel

        # 创建告警管理器
        self.alert_manager = AlertManager(max_history=100, default_cooldown=0)

        # 创建系统监控器
        self.monitor = SystemMonitor(
            check_interval=1.0,
            thresholds=ResourceThresholds(
                cpu_percent=50.0,  # 设置低阈值方便测试
                memory_percent=50.0,
                disk_percent=50.0,
                memory_available_mb=10000.0,
            ),
            enable_alerts=False,  # 先禁用，后面手动设置
        )
        self.monitor._alert_manager = self.alert_manager

    def tearDown(self):
        self.monitor.stop()
        self.alert_manager.cleanup()

    @patch('psutil.cpu_percent', return_value=80.0)
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    def test_check_resources_with_alert(self, mock_disk, mock_memory, mock_cpu):
        """测试资源检查触发告警"""
        # 设置 mock
        mock_memory.return_value = MagicMock(
            percent=85.0,
            available=50 * 1024 * 1024,  # 50MB
        )
        mock_disk.return_value = MagicMock(percent=60.0)

        # 检查资源
        self.monitor._check_resources()

        # 应该有告警触发
        stats = self.alert_manager.get_stats()
        self.assertGreater(stats["total_alerts"], 0)

    @patch('psutil.cpu_percent', return_value=30.0)
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    def test_check_resources_no_alert(self, mock_disk, mock_memory, mock_cpu):
        """测试资源正常时不触发告警"""
        # 重新创建告警管理器，确保状态干净
        self.alert_manager = self.AlertManager(max_history=100, default_cooldown=0)
        self.monitor._alert_manager = self.alert_manager

        # 设置 mock（资源正常）
        # 注意：可用内存需要超过阈值（10000MB），否则会触发告警
        mock_memory.return_value = MagicMock(
            percent=40.0,
            available=20000 * 1024 * 1024,  # 20GB 可用内存（超过阈值10GB）
        )
        mock_disk.return_value = MagicMock(percent=30.0)

        # 检查资源
        self.monitor._check_resources()

        # 应该没有告警（检查告警历史，而不是统计）
        alerts = self.monitor.get_alerts()
        if alerts:
            msgs = ", ".join([a['message'] for a in alerts])
            self.fail(f"期望无告警，但收到: {msgs}")

    def test_get_alerts(self):
        """测试获取告警历史"""
        # 手动添加告警到告警管理器
        self.alert_manager.trigger_warning("system_monitor", "测试告警")

        # 获取告警
        alerts = self.monitor.get_alerts()
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["source"], "system_monitor")

    def test_get_alert_stats(self):
        """测试获取告警统计"""
        stats = self.monitor.get_alert_stats()
        self.assertIsInstance(stats, dict)
        self.assertIn("enabled", stats)


class TestGlobalFunctions(unittest.TestCase):
    """测试全局函数"""

    def test_get_alert_manager_singleton(self):
        from src.utils.alert_manager import get_alert_manager, _global_alert_manager

        # 清理全局实例
        import src.utils.alert_manager as am_module
        am_module._global_alert_manager = None

        # 获取实例
        manager1 = get_alert_manager()
        manager2 = get_alert_manager()

        # 应该是同一个实例
        self.assertIs(manager1, manager2)


if __name__ == "__main__":
    unittest.main()
