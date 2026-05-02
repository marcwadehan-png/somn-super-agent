# -*- coding: utf-8 -*-
"""
NeuralMemory 快速加载性能测试
test_fast_load_benchmark.py

测试目标：
1. 模块导入时间（毫秒级）
2. NeuralMemory 实例化时间
3. 各组件懒加载触发时间
4. 预加载 vs 懒加载对比
5. 全量加载 vs 快速加载对比

Usage:
    python test_fast_load_benchmark.py
"""

import sys
import time
import gc
import os

# 确保正确的目录在 path 中
# __file__ = d:\AI\somn\smart_office_assistant\src\neural_memory\test_fast_load_benchmark.py
# src_dir      = d:\AI\somn\smart_office_assistant\src   ← import neural_memory
# package_dir  = d:\AI\somn\smart_office_assistant        ← from src.intelligence...
src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
package_dir = os.path.dirname(src_dir)
sys.path.insert(0, src_dir)
sys.path.insert(0, package_dir)


def format_time(seconds: float) -> str:
    """格式化时间输出"""
    if seconds < 0.001:
        return f"{seconds * 1_000_000:.2f}μs"
    elif seconds < 1.0:
        return f"{seconds * 1000:.2f}ms"
    else:
        return f"{seconds:.2f}s"


def test_module_import():
    """测试 1: 模块导入时间"""
    print("\n" + "=" * 60)
    print("测试 1: 模块导入时间 (Module Import)")
    print("=" * 60)
    
    # 清除缓存
    modules_to_remove = [m for m in sys.modules.keys() if 'neural_memory' in m or 'wisdom_dispatch' in m]
    for m in modules_to_remove:
        del sys.modules[m]
    gc.collect()
    
    # 测试导入时间
    times = []
    for i in range(5):
        modules_to_remove = [m for m in sys.modules.keys() if 'neural_memory' in m or 'wisdom_dispatch' in m]
        for m in modules_to_remove:
            del sys.modules[m]
        gc.collect()
        
        start = time.perf_counter()
        from neural_memory import NeuralMemory
        end = time.perf_counter()
        times.append(end - start)
        print(f"  第 {i+1} 次导入: {format_time(times[-1])}")
    
    avg = sum(times) / len(times)
    print(f"\n平均导入时间: {format_time(avg)}")
    print(f"最快: {format_time(min(times))}, 最慢: {format_time(max(times))}")
    return avg


def test_fast_load_instantiation():
    """测试 2: 快速加载模式实例化"""
    print("\n" + "=" * 60)
    print("测试 2: NeuralMemory 实例化 (快速加载模式, use_fast_load=True)")
    print("=" * 60)
    
    times = []
    for i in range(5):
        # 确保模块已导入
        from neural_memory import NeuralMemory
        
        start = time.perf_counter()
        nm = NeuralMemory(use_fast_load=True)
        end = time.perf_counter()
        times.append(end - start)
        print(f"  第 {i+1} 次实例化: {format_time(times[-1])}")
    
    avg = sum(times) / len(times)
    print(f"\n平均实例化时间: {format_time(avg)}")
    print(f"最快: {format_time(min(times))}, 最慢: {format_time(max(times))}")
    return avg


def test_lazy_loading_triggers():
    """测试 3: 各组件懒加载触发时间"""
    print("\n" + "=" * 60)
    print("测试 3: 组件懒加载触发时间")
    print("=" * 60)
    
    from neural_memory import NeuralMemory
    
    nm = NeuralMemory(use_fast_load=True)
    
    # 测试 library 懒加载
    start = time.perf_counter()
    _ = nm.library
    t1 = time.perf_counter() - start
    print(f"  library (首次访问): {format_time(t1)}")
    
    # 测试 encoder 懒加载
    start = time.perf_counter()
    _ = nm.encoder
    t2 = time.perf_counter() - start
    print(f"  encoder (首次访问): {format_time(t2)}")
    
    # 测试 replay_buffer 懒加载
    start = time.perf_counter()
    _ = nm.replay_buffer
    t3 = time.perf_counter() - start
    print(f"  replay_buffer (首次访问): {format_time(t3)}")
    
    # 再次访问 (应该命中缓存)
    start = time.perf_counter()
    _ = nm.library
    t4 = time.perf_counter() - start
    print(f"  library (缓存命中): {format_time(t4)}")
    
    start = time.perf_counter()
    _ = nm.encoder
    t5 = time.perf_counter() - start
    print(f"  encoder (缓存命中): {format_time(t5)}")
    
    return {"library_first": t1, "encoder_first": t2, "replay_first": t3,
            "library_cached": t4, "encoder_cached": t5}


def test_legacy_mode():
    """测试 4: 传统模式 (eager load) 对比"""
    print("\n" + "=" * 60)
    print("测试 4: 传统模式实例化 (use_fast_load=False)")
    print("=" * 60)
    
    from neural_memory import NeuralMemory
    
    times = []
    for i in range(3):
        start = time.perf_counter()
        nm = NeuralMemory(use_fast_load=False)
        end = time.perf_counter()
        times.append(end - start)
        print(f"  第 {i+1} 次实例化: {format_time(times[-1])}")
    
    avg = sum(times) / len(times)
    print(f"\n平均实例化时间: {format_time(avg)}")
    return avg


def test_preload():
    """测试 5: 预加载功能"""
    print("\n" + "=" * 60)
    print("测试 5: 预加载 (preload) 功能")
    print("=" * 60)
    
    from neural_memory import NeuralMemory
    
    nm = NeuralMemory(use_fast_load=True)
    
    # 测试 preload() 方法
    start = time.perf_counter()
    nm.preload()
    end = time.perf_counter()
    print(f"  preload() 执行时间: {format_time(end - start)}")
    
    # 检查加载状态
    status = nm.get_load_status()
    print(f"\n加载状态:")
    for comp, state in status.items():
        print(f"  {comp}: {state}")


def test_load_status():
    """测试 6: 加载状态追踪"""
    print("\n" + "=" * 60)
    print("测试 6: 加载状态追踪 (LoadTracker)")
    print("=" * 60)
    
    from neural_memory import quick_load_summary, NeuralMemory
    
    # 触发一些组件加载
    nm = NeuralMemory(use_fast_load=True)
    _ = nm.library
    _ = nm.encoder
    
    # 获取加载摘要
    summary = quick_load_summary()
    print(f"  总组件数: {summary.get('total_components', 'N/A')}")
    print(f"  已加载: {summary.get('loaded_components', 'N/A')}")
    print(f"  待加载: {summary.get('pending_components', 'N/A')}")
    print(f"  总加载时间: {summary.get('total_load_time_ms', 'N/A')}ms")


def test_fast_loader():
    """测试 7: NeuralMemoryFastLoader 独立使用"""
    print("\n" + "=" * 60)
    print("测试 7: NeuralMemoryFastLoader 独立使用")
    print("=" * 60)
    
    from neural_memory import (
        get_fast_loader, FastLoadConfig, LoadStrategy,
        NeuralMemoryFastLoader
    )
    
    # 测试单例
    loader1 = get_fast_loader()
    loader2 = get_fast_loader()
    print(f"  单例测试: {'✓ 通过' if loader1 is loader2 else '✗ 失败'}")
    
    # 测试自定义配置
    config = FastLoadConfig(
        library_strategy=LoadStrategy.LAZY,
        encoder_strategy=LoadStrategy.EAGER,
        preload_lightweight=False,
    )
    custom_loader = NeuralMemoryFastLoader(config)
    print(f"  自定义配置: ✓")
    
    # 获取 stats
    stats = custom_loader.get_stats()
    print(f"  配置策略: library={stats['config']['library_strategy']}, "
          f"encoder={stats['config']['encoder_strategy']}")


def test_concurrent_access():
    """测试 8: 并发访问安全性"""
    print("\n" + "=" * 60)
    print("测试 8: 并发访问安全性")
    print("=" * 60)
    
    import threading
    from neural_memory import NeuralMemory
    
    nm = NeuralMemory(use_fast_load=True)
    results = []
    errors = []
    
    def access_library(thread_id: int):
        try:
            for _ in range(10):
                _ = nm.library
                time.sleep(0.001)
            results.append(thread_id)
        except Exception as e:
            errors.append((thread_id, str(e)))
    
    threads = [threading.Thread(target=access_library, args=(i,)) for i in range(5)]
    start = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - start
    
    print(f"  5 线程并发访问 library 10 次")
    print(f"  成功: {len(results)} 线程, 错误: {len(errors)}")
    print(f"  总耗时: {format_time(elapsed)}")
    if errors:
        print(f"  错误详情: {errors}")
    else:
        print(f"  ✓ 并发安全测试通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 70)
    print("  NeuralMemory 快速加载性能测试 v1.0")
    print("=" * 70)
    print(f"  Python: {sys.version.split()[0]}")
    print(f"  运行环境: Windows (推测)")
    
    results = {}
    
    try:
        results["import"] = test_module_import()
        results["fast_instantiate"] = test_fast_load_instantiation()
        results["lazy_triggers"] = test_lazy_loading_triggers()
        results["legacy"] = test_legacy_mode()
        test_preload()
        test_load_status()
        test_fast_loader()
        test_concurrent_access()
    except Exception as e:
        print(f"\n\n!!! 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 汇总
    print("\n" + "=" * 70)
    print("  测试结果汇总")
    print("=" * 70)
    
    print(f"\n{'测试项':<35} {'平均时间':<15} {'评级'}")
    print("-" * 70)
    
    import_ms = results.get("import", 0) * 1000
    fast_ms = results.get("fast_instantiate", 0) * 1000
    lazy_lib = results.get("lazy_triggers", {}).get("library_first", 0) * 1000
    legacy_ms = results.get("legacy", 0) * 1000
    
    def rate(ms):
        if ms < 1.0:
            return "★★★★★"
        elif ms < 5.0:
            return "★★★★☆"
        elif ms < 20.0:
            return "★★★☆☆"
        elif ms < 100.0:
            return "★★☆☆☆"
        else:
            return "★☆☆☆☆"
    
    # 注意：import_ms/fast_ms/lazy_lib/legacy_ms 已经是毫秒值
    # format_time 接受秒，所以需要除以 1000
    print(f"{'模块导入':<35} {format_time(import_ms/1000):<15} {rate(import_ms)}")
    print(f"{'快速加载实例化':<35} {format_time(fast_ms/1000):<15} {rate(fast_ms)}")
    print(f"{'懒加载 library (首次)':<35} {format_time(lazy_lib/1000):<15} {rate(lazy_lib)}")
    print(f"{'传统模式实例化 (对比)':<35} {format_time(legacy_ms/1000):<15} {rate(legacy_ms)}")
    
    speedup = legacy_ms / fast_ms if fast_ms > 0 else 0
    print(f"\n{'快速加载 vs 传统模式 加速比:':<35} {speedup:.1f}x")
    
    print("\n" + "=" * 70)
    print("  测试完成")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
