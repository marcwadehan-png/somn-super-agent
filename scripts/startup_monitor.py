# -*- coding: utf-8 -*-
"""
启动性能监控脚本
================

监控Somn项目的启动性能和模块加载时间。

用法:
    python scripts/startup_monitor.py
"""

import sys
import time
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.lazy_loader import StartupTimer, ModuleHealthCheck


def measure_import_time():
    """测量各模块的导入时间"""
    print("\n" + "=" * 70)
    print("📊 Somn启动性能监控")
    print("=" * 70)
    
    timer = StartupTimer()
    results = []
    
    # 定义要测试的模块
    modules = [
        ("src.utils", "工具模块"),
        ("src.core", "核心模块"),
        ("src.intelligence", "智能层"),
        ("src.neural_memory", "神经记忆"),
        ("src.main_chain", "主线架构"),
        ("src.learning", "学习系统"),
        ("src.tool_layer", "工具链层"),
        ("src.growth_engine", "增长引擎"),
        ("src.security", "安全模块"),
        ("src.risk_control", "风险控制"),
    ]
    
    for module_path, module_name in modules:
        timer.start(module_path)
        try:
            __import__(module_path)
            duration_ms = timer.end(module_path, success=True)
            status = "✅"
        except Exception as e:
            duration_ms = timer.end(module_path, success=False, error=str(e))
            status = "❌"
        
        results.append({
            "name": module_name,
            "path": module_path,
            "duration_ms": duration_ms or 0,
            "status": status
        })
    
    # 打印结果
    print("\n模块加载时间:")
    print("-" * 70)
    
    total = 0
    for r in sorted(results, key=lambda x: x["duration_ms"], reverse=True):
        print(f"  {r['status']} {r['name']:20s}: {r['duration_ms']:8.2f} ms")
        total += r["duration_ms"]
    
    print("-" * 70)
    print(f"  总计: {total:8.2f} ms")
    print(f"  目标: < 50 ms")
    
    if total < 50:
        print(f"  状态: ✅ 达标!")
    elif total < 100:
        print(f"  状态: ⚠️ 可接受")
    else:
        print(f"  状态: ❌ 需要优化")
    
    return total


def measure_first_import():
    """测量首次导入时间（冷启动）"""
    print("\n" + "=" * 70)
    print("❄️ 冷启动测试")
    print("=" * 70)
    
    # 测试基础模块
    test_modules = [
        "src.utils.lazy_loader",
        "src.core._common_exceptions",
        "src.intelligence",
    ]
    
    for module in test_modules:
        start = time.perf_counter()
        try:
            __import__(module)
            duration_ms = (time.perf_counter() - start) * 1000
            print(f"  ✅ {module:40s}: {duration_ms:8.2f} ms")
        except Exception as e:
            print(f"  ❌ {module:40s}: {str(e)[:30]}")


def health_check():
    """健康检查"""
    print("\n" + "=" * 70)
    print("🏥 模块健康检查")
    print("=" * 70)
    
    checker = ModuleHealthCheck()
    
    # 检查核心模块
    modules = [
        "src.core",
        "src.intelligence",
        "src.neural_memory",
        "src.main_chain",
        "src.tool_layer",
    ]
    
    results = checker.check_all(modules)
    report = checker.get_report()
    
    healthy_count = sum(1 for h in results.values() if h.loaded)
    
    print(f"\n  核心模块: {healthy_count}/{len(modules)} 健康")
    
    if healthy_count == len(modules):
        print("  状态: ✅ 所有核心模块正常")
    else:
        print("  状态: ⚠️ 部分模块异常")
        for name, health in results.items():
            if not health.loaded:
                print(f"    - {name}: {health.error}")


def main():
    """主函数"""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "Somn启动性能监控" + " " * 27 + "║")
    print("╚" + "═" * 68 + "╝")
    
    # 冷启动测试
    measure_first_import()
    
    # 性能测量
    measure_import_time()
    
    # 健康检查
    health_check()
    
    print("\n" + "=" * 70)
    print("监控完成!")
    print("=" * 70)


if __name__ == "__main__":
    main()
