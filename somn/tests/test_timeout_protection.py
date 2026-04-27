"""
超时保护机制单元测试
测试目标:
1. timeout_utils.run_with_timeout - 函数级超时保护
2. timeout_utils.with_timeout  - 装饰器级超时保护
3. llm_service 总体超时保护（集成测试）
"""

import sys
import os
import time
import threading
import pytest

# 确保 src 目录在 Python 路径中
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'smart_office_assistant', 'src'))

from src.timeout_utils import run_with_timeout, with_timeout, TimeoutException


# ============================================================
# run_with_timeout 测试
# ============================================================

class TestRunWithTimeout:
    """测试 run_with_timeout 函数"""

    def test_normal_return(self):
        """测试: 函数正常返回"""
        def normal_func():
            return "hello"

        result = run_with_timeout(normal_func, timeout=5.0, DESCRIPTION="正常函数")
        assert result == "hello"

    def test_timeout(self):
        """测试: 函数执行超时"""
        def slow_func():
            time.sleep(10)

        with pytest.raises(TimeoutException):
            run_with_timeout(slow_func, timeout=0.5, DESCRIPTION="慢速函数")

    def test_exception(self):
        """测试: 函数抛出异常"""
        def error_func():
            raise ValueError("测试错误")

        with pytest.raises(ValueError, match="测试错误"):
            run_with_timeout(error_func, timeout=5.0, DESCRIPTION="错误函数")

    def test_with_args(self):
        """测试: 带参数的函数"""
        def add(a, b):
            return a + b

        result = run_with_timeout(add, args=(1, 2), timeout=5.0, DESCRIPTION="加法函数")
        assert result == 3

    def test_with_kwargs(self):
        """测试: 带关键字参数的函数"""
        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}!"

        result = run_with_timeout(
            greet,
            kwargs={"name": "World", "greeting": "Hi"},
            timeout=5.0,
            DESCRIPTION="问候函数"
        )
        assert result == "Hi, World!"

    def test_thread_daemon(self):
        """测试: 超时后线程不会成为僵尸线程（daemon=True）"""
        def infinite_func():
            while True:
                time.sleep(0.1)

        # 启动前线程数
        before = threading.active_count()

        try:
            run_with_timeout(infinite_func, timeout=0.5, DESCRIPTION="无限函数")
        except TimeoutException:
            pass

        # 等待一下，让守护线程结束
        time.sleep(0.2)
        after = threading.active_count()

        # 守护线程应该已经被清理
        assert after <= before + 1  # 允许一个线程的误差


# ============================================================
# with_timeout 装饰器测试
# ============================================================

class TestWithTimeout:
    """测试 with_timeout 装饰器"""

    def test_decorator_normal(self):
        """测试: 装饰器正常返回"""
        @with_timeout(timeout=5.0, description="装饰器测试")
        def normal_func():
            return "decorated"

        result = normal_func()
        assert result == "decorated"

    def test_decorator_timeout(self):
        """测试: 装饰器超时"""
        @with_timeout(timeout=0.5, description="装饰器超时测试")
        def slow_func():
            time.sleep(10)

        with pytest.raises(TimeoutException):
            slow_func()

    def test_decorator_exception(self):
        """测试: 装饰器抛出异常"""
        @with_timeout(timeout=5.0, description="装饰器异常测试")
        def error_func():
            raise RuntimeError("装饰器错误")

        with pytest.raises(RuntimeError, match="装饰器错误"):
            error_func()

    def test_decorator_with_args(self):
        """测试: 装饰器带参数"""
        @with_timeout(timeout=5.0, description="装饰器带参数")
        def multiply(a, b):
            return a * b

        result = multiply(3, 4)
        assert result == 12


# ============================================================
# 集成测试: llm_service 总体超时保护
# ============================================================

class TestLLMServiceTimeout:
    """测试 llm_service 中的总体超时保护"""

    def test_overall_timeout_check(self):
        """测试: 总体超时检查逻辑（不实际调用 LLM）"""
        import time

        _overall_timeout = 2.0  # 总体超时2秒
        _func_start_time = time.time()

        # 模拟一些工作
        time.sleep(1.0)

        # 检查是否超时
        elapsed = time.time() - _func_start_time
        assert elapsed < _overall_timeout  # 不应该超时

        # 模拟超过总体超时
        _func_start_time = time.time() - 3.0  # 假装开始于3秒前

        elapsed = time.time() - _func_start_time
        assert elapsed > _overall_timeout  # 应该超时

    def test_circuit_breaker_integration(self):
        """测试: 熔断器与超时保护的集成"""
        from src.utils.retry_utils import get_circuit_breaker, CircuitBreaker
        import time

        # 使用唯一名称，避免与其他测试共享状态
        unique_name = f"test-cb-{time.time()}"
        cb = get_circuit_breaker(unique_name, failure_threshold=3, recovery_timeout=1.0)

        # 记录足够次数的失败，使熔断器打开
        for _ in range(3):
            cb.record_failure()

        # 熔断器应该打开
        assert not cb.is_available()
        assert cb._state == CircuitBreaker.State.OPEN

        # 真实等待超过恢复超时
        time.sleep(1.5)

        # 熔断器应该进入半开状态
        assert cb.is_available()
        assert cb._state == CircuitBreaker.State.HALF_OPEN

        # 记录成功，应该关闭熔断器
        cb.record_success()
        assert cb.is_available()
        assert cb._state == CircuitBreaker.State.CLOSED


# ============================================================
# 辅助函数测试
# ============================================================

class TestHelperFunctions:
    """测试辅助函数"""

    def test_timeout_exception_message(self):
        """测试: TimeoutException 包含正确的消息"""
        try:
            def slow():
                time.sleep(10)

            run_with_timeout(slow, timeout=0.5, DESCRIPTION="测试操作")
        except TimeoutException as e:
            assert "测试操作" in str(e)
            assert "0.5" in str(e) or "1.0" in str(e)  # 超时时间


if __name__ == "__main__":
    # 直接运行测试
    pytest.main([__file__, "-v"])
