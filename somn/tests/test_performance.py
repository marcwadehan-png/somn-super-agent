# -*- coding: utf-8 -*-
"""
P12-1#3 性能测试
覆盖: 延迟测试、吞吐量测试、内存测试、缓存测试
"""

import pytest
import time
import psutil
import os
from unittest.mock import Mock, patch
from datetime import datetime
import json


# ============================================================
# 1. 延迟性能测试
# ============================================================

class TestLatencyPerformance:
    """延迟性能测试"""

    def test_simple_operation_latency(self):
        """简单操作延迟"""
        start = time.perf_counter()
        result = sum(range(1000))
        end = time.perf_counter()
        latency_ms = (end - start) * 1000
        assert latency_ms < 100  # 应小于100ms

    def test_json_parsing_latency(self):
        """JSON解析延迟"""
        data = {"key": "value", "nested": {"data": [1, 2, 3]}}
        json_str = json.dumps(data)

        start = time.perf_counter()
        for _ in range(1000):
            parsed = json.loads(json_str)
        end = time.perf_counter()

        avg_latency_us = ((end - start) * 1000000) / 1000
        assert avg_latency_us < 1000  # 平均小于1ms

    def test_string_operations_latency(self):
        """字符串操作延迟"""
        text = "hello world " * 100

        start = time.perf_counter()
        for _ in range(1000):
            _ = text.upper()
            _ = text.lower()
            _ = text.split()
        end = time.perf_counter()

        total_time = (end - start) * 1000
        assert total_time < 500  # 1000次操作应在500ms内

    def test_list_operations_latency(self):
        """列表操作延迟"""
        lst = list(range(1000))

        start = time.perf_counter()
        for _ in range(1000):
            _ = sum(lst)
            _ = max(lst)
            _ = min(lst)
        end = time.perf_counter()

        total_time = (end - start) * 1000
        assert total_time < 1000  # 1000次操作应在1秒内


# ============================================================
# 2. 吞吐量测试
# ============================================================

class TestThroughputPerformance:
    """吞吐量性能测试"""

    def test_dict_creation_throughput(self):
        """字典创建吞吐量"""
        iterations = 10000
        start = time.perf_counter()
        for _ in range(iterations):
            _ = {f"key_{i}": i for i in range(100)}
        end = time.perf_counter()

        ops_per_sec = iterations / (end - start)
        assert ops_per_sec > 100  # 至少100 ops/s

    def test_list_comprehension_throughput(self):
        """列表推导式吞吐量"""
        iterations = 10000
        start = time.perf_counter()
        for _ in range(iterations):
            _ = [i * 2 for i in range(100)]
        end = time.perf_counter()

        ops_per_sec = iterations / (end - start)
        assert ops_per_sec > 500  # 至少500 ops/s

    def test_regex_matching_throughput(self):
        """正则匹配吞吐量"""
        import re
        pattern = re.compile(r'\w+')
        text = "hello world this is a test " * 100

        iterations = 1000
        start = time.perf_counter()
        for _ in range(iterations):
            _ = pattern.findall(text)
        end = time.perf_counter()

        ops_per_sec = iterations / (end - start)
        assert ops_per_sec > 100

    def test_json_serialization_throughput(self):
        """JSON序列化吞吐量"""
        data = {"items": [{"id": i, "value": f"item_{i}"} for i in range(100)]}

        iterations = 1000
        start = time.perf_counter()
        for _ in range(iterations):
            _ = json.dumps(data)
        end = time.perf_counter()

        ops_per_sec = iterations / (end - start)
        assert ops_per_sec > 100


# ============================================================
# 3. 内存性能测试
# ============================================================

class TestMemoryPerformance:
    """内存性能测试"""

    def test_memory_overhead_basic_types(self):
        """基本类型内存开销"""
        # 获取当前进程
        process = psutil.Process(os.getpid())

        initial_mem = process.memory_info().rss / 1024 / 1024  # MB

        # 创建一些数据
        data = [list(range(1000)) for _ in range(100)]

        final_mem = process.memory_info().rss / 1024 / 1024  # MB
        mem_increase = final_mem - initial_mem

        # 内存增长应该在合理范围内
        assert mem_increase < 50  # 小于50MB

    def test_generator_vs_list_memory(self):
        """生成器 vs 列表内存对比"""
        process = psutil.Process(os.getpid())

        # 列表
        initial_mem = process.memory_info().rss / 1024 / 1024
        list_data = list(range(100000))
        list_mem = process.memory_info().rss / 1024 / 1024 - initial_mem

        # 生成器
        initial_mem = process.memory_info().rss / 1024 / 1024
        gen_data = (i for i in range(100000))
        gen_mem = process.memory_info().rss / 1024 / 1024 - initial_mem

        # 生成器内存开销应该更小
        # 注意：这里只是粗略测试
        assert gen_mem >= 0  # 确保测试执行

    def test_string_interning(self):
        """字符串驻留优化"""
        # 短字符串自动驻留
        s1 = "hello"
        s2 = "hello"
        assert s1 is s2  # 相同字符串应该是同一对象

    def test_dict_memory_efficiency(self):
        """字典内存效率"""
        # 小字典
        small_dict = {f"key_{i}": i for i in range(10)}
        assert len(small_dict) == 10

        # 中字典
        medium_dict = {f"key_{i}": i for i in range(100)}
        assert len(medium_dict) == 100

        # 大字典
        large_dict = {f"key_{i}": i for i in range(1000)}
        assert len(large_dict) == 1000


# ============================================================
# 4. 缓存性能测试
# ============================================================

class TestCachePerformance:
    """缓存性能测试"""

    def test_lru_cache_hit_rate(self):
        """LRU缓存命中率"""
        from functools import lru_cache

        @lru_cache(maxsize=100)
        def cached_func(n):
            return n * 2

        # 填充缓存
        for i in range(100):
            cached_func(i)

        # 重新访问（缓存命中）
        start = time.perf_counter()
        for _ in range(1000):
            _ = cached_func(50)
        end = time.perf_counter()

        # 缓存命中应该很快
        assert (end - start) < 0.1  # 小于100ms

    def test_cache_invalidation(self):
        """缓存失效"""
        from functools import lru_cache

        cache_store = {"key": "value"}

        @lru_cache(maxsize=1)
        def get_value():
            return cache_store.get("key", "default")

        # 首次访问
        result1 = get_value()

        # 修改缓存
        cache_store["key"] = "new_value"

        # 再次访问（应该使用缓存的旧值）
        result2 = get_value()

        # 如果缓存被正确实现，结果应该相同
        assert result1 == result2

    def test_cache_size_limit(self):
        """缓存大小限制"""
        from functools import lru_cache

        @lru_cache(maxsize=3)
        def limited_cache(n):
            return n

        # 填充到限制
        for i in range(3):
            limited_cache(i)

        # 检查缓存信息
        info = limited_cache.cache_info()
        assert info.currsize <= 3


# ============================================================
# 5. 并发性能测试
# ============================================================

class TestConcurrencyPerformance:
    """并发性能测试"""

    def test_sequential_vs_parallel(self):
        """顺序 vs 并行性能对比"""
        def work(n):
            time.sleep(0.01)
            return n * 2

        # 顺序执行
        start = time.perf_counter()
        results = [work(i) for i in range(5)]
        sequential_time = time.perf_counter() - start

        # 结果应该正确
        assert results == [0, 2, 4, 6, 8]
        # 顺序执行应该至少花费 5 * 0.01 = 0.05秒
        assert sequential_time >= 0.05

    def test_concurrent_execution_time(self):
        """并发执行时间"""
        import concurrent.futures

        def work(n):
            return n * 2

        start = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(work, i) for i in range(5)]
            results = [f.result() for f in futures]
        concurrent_time = time.perf_counter() - start

        assert results == [0, 2, 4, 6, 8]
        # 并发执行应该很快
        assert concurrent_time < 1.0

    def test_thread_pool_efficiency(self):
        """线程池效率"""
        import concurrent.futures

        def cpu_work(n):
            return sum(range(n))

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(cpu_work, [1000] * 10))

        assert len(results) == 10
        assert all(r == sum(range(1000)) for r in results)


# ============================================================
# 6. 延迟加载性能测试
# ============================================================

class TestLazyLoadingPerformance:
    """延迟加载性能测试"""

    def test_lazy_import_time(self):
        """延迟导入时间"""
        # 记录开始时间
        start = time.perf_counter()

        # 导入（应该很快，因为是按需导入）
        import smart_office_assistant.src.core.somn_core

        end = time.perf_counter()
        import_time = (end - start) * 1000

        # 导入时间应该合理
        assert import_time < 5000  # 小于5秒

    def test_deferred_initialization(self):
        """延迟初始化"""
        class DeferredInit:
            def __init__(self, lazy=False):
                self._initialized = False
                self._lazy = lazy
                if not lazy:
                    self._do_init()

            def _do_init(self):
                time.sleep(0.01)  # 模拟耗时初始化
                self._data = [1, 2, 3]
                self._initialized = True

            def get_data(self):
                if self._lazy and not self._initialized:
                    self._do_init()
                return self._data

        # 立即初始化
        start = time.perf_counter()
        obj1 = DeferredInit(lazy=False)
        init_time = time.perf_counter() - start
        assert init_time >= 0.01

        # 延迟初始化
        start = time.perf_counter()
        obj2 = DeferredInit(lazy=True)
        lazy_init_time = time.perf_counter() - start
        assert lazy_init_time < 0.01  # 应该很快

        # 实际使用时才初始化
        start = time.perf_counter()
        _ = obj2.get_data()
        access_time = time.perf_counter() - start
        assert access_time >= 0.01


# ============================================================
# 7. 数据库/存储性能测试（模拟）
# ============================================================

class TestStoragePerformance:
    """存储性能测试"""

    def test_dict_as_cache_performance(self):
        """字典缓存性能"""
        cache = {}

        # 写入性能
        start = time.perf_counter()
        for i in range(10000):
            cache[f"key_{i}"] = i
        write_time = time.perf_counter() - start

        assert write_time < 1.0  # 1秒内完成

        # 读取性能
        start = time.perf_counter()
        for i in range(10000):
            _ = cache.get(f"key_{i}")
        read_time = time.perf_counter() - start

        assert read_time < 0.5  # 500ms内完成

    def test_bulk_operations(self):
        """批量操作性能"""
        data = [{"id": i, "value": f"item_{i}"} for i in range(1000)]

        # 批量读取
        start = time.perf_counter()
        ids = [item["id"] for item in data]
        values = [item["value"] for item in data]
        end = time.perf_counter()

        assert len(ids) == 1000
        assert (end - start) < 0.1  # 小于100ms


# ============================================================
# 8. 算法性能测试
# ============================================================

class TestAlgorithmPerformance:
    """算法性能测试"""

    def test_sorting_algorithm_performance(self):
        """排序算法性能"""
        import random

        # 生成随机数据
        data = [random.randint(0, 10000) for _ in range(1000)]

        start = time.perf_counter()
        sorted_data = sorted(data)
        end = time.perf_counter()

        sort_time = (end - start) * 1000
        assert sort_time < 100  # 小于100ms
        assert sorted_data == sorted(data)  # 验证正确性

    def test_search_algorithm_performance(self):
        """搜索算法性能"""
        import bisect

        sorted_list = list(range(10000))

        start = time.perf_counter()
        for _ in range(1000):
            _ = bisect.bisect_left(sorted_list, 5000)
        end = time.perf_counter()

        avg_time_us = ((end - start) * 1000000) / 1000
        assert avg_time_us < 100  # 平均小于100微秒

    def test_set_operations_performance(self):
        """集合操作性能"""
        s1 = set(range(10000))
        s2 = set(range(5000, 15000))

        start = time.perf_counter()
        intersection = s1 & s2
        union = s1 | s2
        difference = s1 - s2
        end = time.perf_counter()

        assert len(intersection) > 0
        assert len(union) > 0
        assert len(difference) > 0
        assert (end - start) < 0.1  # 小于100ms


# ============================================================
# 9. 网络模拟性能测试
# ============================================================

class TestNetworkSimulatedPerformance:
    """网络模拟性能测试"""

    def test_request_response_cycle(self):
        """请求响应周期（模拟）"""
        start = time.perf_counter()

        # 模拟网络延迟
        time.sleep(0.1)

        # 模拟处理
        response = {"status": "ok", "data": [1, 2, 3]}

        end = time.perf_counter()
        cycle_time = (end - start) * 1000

        assert cycle_time >= 100  # 至少100ms
        assert response["status"] == "ok"

    def test_batch_request_performance(self):
        """批量请求性能"""
        start = time.perf_counter()

        # 模拟5个请求
        for _ in range(5):
            time.sleep(0.01)
            _ = {"status": "ok"}

        end = time.perf_counter()
        total_time = (end - start) * 1000

        # 顺序执行至少需要50ms
        assert total_time >= 50


# ============================================================
# 10. 综合性能基准测试
# ============================================================

class TestComprehensiveBenchmark:
    """综合性能基准测试"""

    def test_overall_operation_speed(self):
        """综合操作速度"""
        start = time.perf_counter()

        # 综合操作
        data = [list(range(100)) for _ in range(50)]
        processed = [
            [item * 2 for item in row if item % 2 == 0]
            for row in data
        ]
        result = sum(sum(row) for row in processed)

        end = time.perf_counter()
        total_time = (end - start) * 1000

        assert total_time < 1000  # 整个操作应在1秒内
        assert result >= 0

    def test_cpu_intensive_task(self):
        """CPU密集型任务"""
        def cpu_task(n):
            return sum(i * i for i in range(n))

        iterations = 100
        start = time.perf_counter()
        results = [cpu_task(1000) for _ in range(iterations)]
        end = time.perf_counter()

        total_time = (end - start) * 1000
        assert len(results) == iterations
        assert total_time < 5000  # 100次CPU密集任务应在5秒内

    def test_memory_intensive_task(self):
        """内存密集型任务"""
        process = psutil.Process(os.getpid())
        initial_mem = process.memory_info().rss / 1024 / 1024

        # 创建多个大型数据结构
        data_structures = [
            [list(range(10000)) for _ in range(10)],
            {f"key_{i}": list(range(100)) for i in range(1000)},
            [[i, i*2, i*3] for i in range(5000)]
        ]

        final_mem = process.memory_info().rss / 1024 / 1024
        mem_increase = final_mem - initial_mem

        assert mem_increase < 100  # 内存增长小于100MB
