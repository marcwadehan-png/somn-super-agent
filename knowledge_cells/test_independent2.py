"""测试 v6.1.1 是否能独立解决问题 - 修正版"""
import sys
sys.path.insert(0, r"d:\AI\somn")
sys.path.insert(0, r"d:\AI\somn\knowledge_cells")
sys.path.insert(0, r"d:\AI\somn\smart_office_assistant\src")

from knowledge_cells.core import dispatch, get_engine

engine = get_engine()

tests = [
    ("简单信息查询", "什么是机器学习？"),
    ("分析类问题", "分析一下新能源汽车市场的发展趋势"),
    ("决策类问题", "选择 Python 还是 JavaScript 作为第一门编程语言？"),
]

print("=== v6.1.1 独立解决问题能力测试 ===\n")

passed = 0
for name, problem in tests:
    print(f"【{name}】")
    print(f"  问题: {problem}")
    try:
        result = dispatch(problem=problem)
        conf = result.output.get("confidence", 0.0)
        dispatched = result.dispatched_to
        print(f"  ✅ 置信度: {conf}")
        print(f"  调度至: {dispatched}")

        # 检查输出质量
        output = result.output.get("output", {})
        if isinstance(output, dict):
            answer = output.get("answer", output.get("conclusion", ""))
            if answer and len(str(answer)) > 20:
                print(f"  回答: {str(answer)[:100]}...")
                passed += 1
            else:
                print(f"  ⚠️ 回答内容较少")
        print()
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        print()

print("=== 总体结论 ===")
if passed >= 2:
    print(f"✅ v6.1.1 能独立解决问题（{passed}/3 测试通过）")
else:
    print(f"⚠️ v6.1.1 解决问题能力有限（仅 {passed}/3 测试通过）")
