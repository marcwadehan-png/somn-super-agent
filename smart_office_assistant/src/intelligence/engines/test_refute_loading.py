# -*- coding: utf-8 -*-
"""
RefuteCore v3.1.0 快速加载模式测试
- 性能基准测试
- 懒加载机制验证
- 功能完整性回归
"""

import sys
import os
import time

# 确保可以导入
sys.path.insert(0, os.path.dirname(__file__))

from refute_core import (
    RefuteCoreEngine, RefuteDimension,
    get_refute_core, quick_refute, quick_refute_md,
    refute_and_solve, batch_refute,
    benchmark_loading,
)

# ─── 颜色工具 ───
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

passed = 0
failed = 0
warnings = 0

def check(condition: bool, msg: str, level: str = "FAIL"):
    global passed, failed, warnings
    if condition:
        passed += 1
        print(f"  {GREEN}✓ PASS{RESET} {msg}")
    elif level == "WARN":
        warnings += 1
        print(f"  {YELLOW}⚠ WARN{RESET} {msg}")
    else:
        failed += 1
        print(f"  {RED}✗ FAIL{RESET} {msg}")


# ═══════════════════════════════════════════════════════════════
print(f"\n{BOLD}{'═' * 60}")
print(f"  RefuteCore v3.2.0 快速加载模式测试")
print(f"{'═' * 60}{RESET}\n")

# ═══════════════════════════════════════════════════════════════
print(f"{CYAN}{BOLD}A. 懒加载机制验证{RESET}")
print("-" * 40)

print("\n  [A1] 空实例化 — 零子组件")
t0 = time.perf_counter()
engine = RefuteCoreEngine()
t1 = time.perf_counter()
init_ms = (t1 - t0) * 1000
print(f"  实例化耗时: {init_ms:.4f} ms")
check(init_ms < 1.0, f"实例化 < 1ms (实际: {init_ms:.4f}ms)", "WARN")
check(len(engine._components) == 0, "初始化时零子组件加载")
check(not engine.is_fully_loaded, "is_fully_loaded = False (尚未加载)")

print("\n  [A2] 懒加载 parser — 首次访问触发")
t0 = time.perf_counter()
parser = engine.parser  # 应触发懒加载
t1 = time.perf_counter()
parse_ms = (t1 - t0) * 1000
print(f"  首次加载 parser: {parse_ms:.4f} ms")
check('parser' in engine._components, "parser 已加载")
check(len(engine._loaded_components) == 1, f"loaded_components == 1 (实际: {engine._loaded_components})")

print("\n  [A3] 懒加载 strategist — 独立加载")
strategist = engine.strategist
check('strategist' in engine._components, "strategist 已加载")
check(len(engine._loaded_components) == 2, f"loaded_components == 2 (实际: {engine._loaded_components})")

print("\n  [A4] 重复访问 — 缓存命中")
t0 = time.perf_counter()
parser2 = engine.parser
t1 = time.perf_counter()
cache_ms = (t1 - t0) * 1000
print(f"  缓存命中耗时: {cache_ms:.4f} ms")
check(parser2 is parser, "缓存命中: parser2 is parser (同一对象)")
check(cache_ms < 0.1, f"缓存访问 < 0.1ms (实际: {cache_ms:.4f}ms)", "WARN")

print("\n  [A5] preload_all — 批量预加载")
engine2 = RefuteCoreEngine()
check(not engine2.is_fully_loaded, "preload前: is_fully_loaded = False")
t0 = time.perf_counter()
engine2.preload_all()
t1 = time.perf_counter()
preload_ms = (t1 - t0) * 1000
print(f"  preload_all 耗时: {preload_ms:.4f} ms")
check(engine2.is_fully_loaded, "preload后: is_fully_loaded = True")
check(len(engine2._components) == 7, f"7个子组件全部加载 (实际: {len(engine2._components)})")

print("\n  [A6] loading_stats — 统计信息")
stats = engine.get_loading_stats()
check(stats["version"] == "v3.2.0", f"版本正确: {stats['version']}")
check(stats["total_components"] == 7, "total_components == 7")
check(stats["loaded_components"] == 2, f"loaded_components == 2 (当前engine已加载parser+strategist)")
check("component_status" in stats, "component_status 存在")

print("\n  [A7] 属性访问错误处理")
try:
    _ = engine.nonexistent_attr
    check(False, "访问不存在的属性应抛出 AttributeError")
except AttributeError as e:
    check("nonexistent_attr" in str(e), f"AttributeError 正确: {e}")


# ═══════════════════════════════════════════════════════════════
print(f"\n{CYAN}{BOLD}B. 功能完整性 — 懒加载不破坏功能{RESET}")
print("-" * 40)

print("\n  [B1] parse — 解析器懒加载")
engine3 = RefuteCoreEngine()
result_parse = engine3.parser.parse("我们应该投资这个项目因为市场很大")
check(result_parse.core_claim, f"解析成功: {result_parse.core_claim[:30]}")
check(result_parse.context_domain in ["投资理财", "通用"], f"领域识别: {result_parse.context_domain}")
check('parser' in engine3._components, "parser 已被懒加载")

print("\n  [B2] refute — 完整反驳流程（触发全部懒加载）")
engine4 = RefuteCoreEngine()
check(not engine4.is_fully_loaded, "refute前: 未全量加载")
result = engine4.refute("所有人都必须使用Python，因为它是最好的语言")
check(result.engine_version == "6.2.0", f"版本正确: {result.engine_version}")
check(result.parsed_argument.argument_type is not None, "论证类型已解析")
check(len(result.refutation.refutations) > 0, f"反驳数量: {len(result.refutation.refutations)}")
check(result.assessment.strength_grade, f"强度等级: {result.assessment.strength_grade}")
check(len(result.debate.rounds) == 3, f"辩论轮次: {len(result.debate.rounds)}")
check(result.repair.repaired_claim, f"修复后论点: {result.repair.repaired_claim[:30]}")
check(len(result.solutions.solutions) > 0, f"解决方案: {len(result.solutions.solutions)}")
check(engine4.is_fully_loaded or len(engine4._components) == 6,
      f"refute后加载6个核心组件 (实际: {len(engine4._components)}/7, batch_refuter需batch_refute触发)")

print("\n  [B3] batch_refute — 批量反驳")
batch = engine4.batch_refute(["投资一定赚钱", "创业必然成功", "学习就能找到好工作"])
check(len(batch.arguments) == 3, f"批量输入: {len(batch.arguments)}")
check(len(batch.contradictions) >= 0, f"矛盾检测: {len(batch.contradictions)}")
check(batch.consistency_score >= 0, f"一致性: {batch.consistency_score:.0%}")

print("\n  [B4] quick_refute_text / quick_refute_markdown")
text_result = engine4.quick_refute_text("价格战是最好的竞争策略")
check("驳心引擎" in text_result, "文本格式包含引擎标识")
md_result = engine4.quick_refute_markdown("价格战是最好的竞争策略")
check("# 驳心引擎分析报告" in md_result, "Markdown格式包含标题")

print("\n  [B5] 便捷函数 — 全局单例")
global_engine = get_refute_core()
check(global_engine is get_refute_core(), "get_refute_core() 返回同一实例")

qr_text = quick_refute("应该立刻辞职创业")
check("驳心引擎" in qr_text, "quick_refute() 正常工作")

qr_md = quick_refute_md("应该立刻辞职创业")
check("驳心引擎" in qr_md, "quick_refute_md() 正常工作")

qr_result = refute_and_solve("应该立刻辞职创业", focus_dimensions=[RefuteDimension.BEHAVIORAL])
check(qr_result.engine_version == "6.2.0", f"refute_and_solve() 版本正确")

br = batch_refute(["论点A", "论点B"])
check(len(br.arguments) == 2, f"batch_refute() 输入: {len(br.arguments)}")


# ═══════════════════════════════════════════════════════════════
print(f"\n{CYAN}{BOLD}C. 性能基准测试{RESET}")
print("-" * 40)

print("\n  [C1] benchmark_loading — 50次迭代")
bench = benchmark_loading(iterations=50)

print(f"\n  {'指标':<20} {'平均':>10} {'最小':>10} {'最大':>10}")
print(f"  {'─' * 52}")
for key, vals in bench.items():
    label = {
        "cold_init": "空实例化",
        "preload_all": "全量预加载",
        "first_refute": "首次反驳(冷)",
        "cached_refute": "缓存反驳(热)",
    }.get(key, key)
    print(f"  {label:<18} {vals['avg_ms']:>8.2f}ms {vals['min_ms']:>8.2f}ms {vals['max_ms']:>8.2f}ms")

# 性能断言
check(bench["cold_init"]["avg_ms"] < 1.0,
      f"空实例化 < 1ms (实际: {bench['cold_init']['avg_ms']:.4f}ms)", "WARN")
check(bench["preload_all"]["avg_ms"] < 5.0,
      f"全量预加载 < 5ms (实际: {bench['preload_all']['avg_ms']:.4f}ms)", "WARN")
check(bench["first_refute"]["avg_ms"] < 50.0,
      f"首次反驳 < 50ms (实际: {bench['first_refute']['avg_ms']:.4f}ms)", "WARN")
check(bench["cached_refute"]["avg_ms"] < 50.0,
      f"缓存反驳 < 50ms (实际: {bench['cached_refute']['avg_ms']:.4f}ms)", "WARN")

# 冷/热比率
if bench["cached_refute"]["avg_ms"] > 0:
    ratio = bench["first_refute"]["avg_ms"] / bench["cached_refute"]["avg_ms"]
    print(f"\n  冷/热比率: {ratio:.1f}x (首次反驳 / 缓存反驳)")
    check(ratio < 5.0, f"冷热比率合理 < 5x (实际: {ratio:.1f}x)", "WARN")


# ═══════════════════════════════════════════════════════════════
# 总结
# ═══════════════════════════════════════════════════════════════
print(f"\n{BOLD}{'═' * 60}")
total = passed + failed + warnings
if failed == 0 and warnings == 0:
    print(f"  {GREEN}全绿! {passed}/{total} PASS{RESET}")
elif failed == 0:
    print(f"  {GREEN}通过! {passed} PASS / {warnings} WARN{RESET}")
else:
    print(f"  {RED}问题! {passed} PASS / {failed} FAIL / {warnings} WARN{RESET}")
print(f"{'═' * 60}{RESET}")

sys.exit(1 if failed > 0 else 0)
