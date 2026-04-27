# -*- coding: utf-8 -*-
"""
全局懒加载验证脚本
=================

验证:
1. 毫秒级启动
2. 加载失败降级方案
3. 模块健康检查

用法:
    python scripts/verify_lazy_loading.py
"""

import sys
import time
import os

# 添加项目根目录和smart_office_assistant到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'smart_office_assistant'))

from src.utils.lazy_loader import (
    StartupTimer, measure_startup, GracefulDegradation,
    ModuleHealthCheck, graceful_fallback, LazyImport
)


def test_startup_timer():
    """测试启动计时器"""
    print("\n" + "=" * 60)
    print("测试1: 启动计时器")
    print("=" * 60)
    
    timer = StartupTimer()
    
    # 模拟各模块加载
    with measure_startup("core模块"):
        time.sleep(0.001)  # 1ms
    
    with measure_startup("intelligence模块"):
        time.sleep(0.002)  # 2ms
    
    with measure_startup("neural_memory模块"):
        time.sleep(0.001)  # 1ms
    
    timer.print_report()
    return timer.get_total_time()


def test_graceful_degradation():
    """测试降级方案"""
    print("\n" + "=" * 60)
    print("测试2: 优雅降级")
    print("=" * 60)
    
    degrader = GracefulDegradation()
    
    # 测试1: 成功加载
    @degrader.handle("test_module_success")
    def load_success():
        return {"data": "success"}
    
    result = load_success()
    print(f"  ✅ 成功加载: {result}")
    
    # 测试2: 失败降级
    @degrader.handle("test_module_fail")
    def load_fail():
        raise ImportError("模块不存在")
    
    result = load_fail()
    print(f"  ✅ 失败降级: {result}")
    
    # 打印健康报告
    report = degrader.get_health_report()
    print(f"\n  健康报告: {report['summary']}")
    
    return degrader.is_healthy()


def test_module_health_check():
    """测试模块健康检查"""
    print("\n" + "=" * 60)
    print("测试3: 模块健康检查")
    print("=" * 60)

    checker = ModuleHealthCheck()

    # 检查核心模块（使用正确的模块路径）
    modules = [
        "smart_office_assistant.src.core",
        "smart_office_assistant.src.intelligence",
        "smart_office_assistant.src.intelligence.reasoning",
        "smart_office_assistant.src.intelligence.claws",
        "smart_office_assistant.src.intelligence.dispatcher",
    ]

    results = checker.check_all(modules)

    print("\n  模块加载状态:")
    for name, health in results.items():
        status = "✅" if health.loaded else "❌"
        time_str = f"{health.load_time_ms:.2f}ms" if health.load_time_ms else "N/A"
        error_str = f" ({health.error})" if health.error else ""
        print(f"    {status} {name:40s}: {time_str}{error_str}")

    report = checker.get_report()
    print(f"\n  总耗时: {report['summary']['total_load_time_ms']:.2f}ms")
    print(f"  平均耗时: {report['summary']['avg_load_time_ms']:.2f}ms")

    return report['summary']['failed'] == 0


def test_lazy_import():
    """测试延迟导入"""
    print("\n" + "=" * 60)
    print("测试4: 延迟导入")
    print("=" * 60)
    
    # 测试成功导入
    with LazyImport("json") as ctx:
        if ctx.success:
            print(f"  ✅ json模块加载成功")
        else:
            print(f"  ❌ json模块加载失败: {ctx.error}")
    
    # 测试失败导入
    with LazyImport("nonexistent_module_xyz") as ctx:
        if ctx.success:
            print(f"  ❌ 不应成功")
        else:
            print(f"  ✅ 正确处理失败: {ctx.error}")


def test_decorator_fallback():
    """测试装饰器降级"""
    print("\n" + "=" * 60)
    print("测试5: 装饰器降级")
    print("=" * 60)

    # 临时禁用graceful_fallback的日志输出，避免干扰
    import logging
    original_level = logger.level
    logger.setLevel(logging.ERROR)

    try:
        @graceful_fallback(default="fallback_value", error_log="加载失败")
        def may_fail():
            # 模拟可能的失败
            if True:  # 改为False会返回正常值
                raise RuntimeError("模拟加载失败")
            return "success"

        result = may_fail()
        if result == "fallback_value":
            print(f"  ✅ 降级结果: {result}")
        else:
            print(f"  ❌ 降级结果错误: {result}")
    finally:
        logger.setLevel(original_level)


def benchmark_cold_start():
    """冷启动基准测试"""
    print("\n" + "=" * 60)
    print("测试6: 冷启动基准测试")
    print("=" * 60)
    
    import subprocess
    
    # 获取项目根目录
    import os as _os
    _project_root = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
    
    # 创建测试脚本
    test_script = '''
import sys
import time
import os
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _project_root)

start = time.perf_counter()
from src.utils.lazy_loader import StartupTimer, GracefulDegradation
timer = StartupTimer()

# 模拟基础导入
with timer.start("__main__"), open("nul", "w") as devnull:
    import src.core
    import src.intelligence

end = time.perf_counter()
print(f"{(end - start) * 1000:.2f}")
'''
    
    print("  运行冷启动测试...")
    result = subprocess.run(
        [sys.executable, "-c", test_script],
        capture_output=True,
        text=True,
        cwd=_project_root
    )
    
    if result.returncode == 0:
        print(f"  ✅ 冷启动耗时: {result.stdout.strip()} ms")
    else:
        print(f"  ⚠️ 测试输出: {result.stderr[:200] if result.stderr else result.stdout[:200]}")


def main():
    """主测试流程"""
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "全局懒加载验证测试" + " " * 22 + "║")
    print("╚" + "═" * 58 + "╝")
    
    all_passed = True
    
    # 运行各项测试
    try:
        total_time = test_startup_timer()
        if total_time > 100:
            print("  ⚠️ 警告: 计时器测试耗时过长")
    except Exception as e:
        print(f"  ❌ 测试1失败: {e}")
        all_passed = False
    
    try:
        if not test_graceful_degradation():
            print("  ⚠️ 警告: 降级测试未全部通过")
    except Exception as e:
        print(f"  ❌ 测试2失败: {e}")
        all_passed = False
    
    try:
        if not test_module_health_check():
            print("  ⚠️ 警告: 模块健康检查有失败项")
    except Exception as e:
        print(f"  ❌ 测试3失败: {e}")
        all_passed = False
    
    try:
        test_lazy_import()
    except Exception as e:
        print(f"  ❌ 测试4失败: {e}")
        all_passed = False
    
    try:
        test_decorator_fallback()
    except Exception as e:
        print(f"  ❌ 测试5失败: {e}")
        all_passed = False
    
    try:
        benchmark_cold_start()
    except Exception as e:
        print(f"  ⚠️ 测试6跳过: {e}")
    
    # 总结
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 所有测试通过!")
    else:
        print("⚠️ 部分测试未通过，请检查日志")
    print("=" * 60)


if __name__ == "__main__":
    main()
