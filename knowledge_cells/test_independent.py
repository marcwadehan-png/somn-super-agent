"""测试 v6.1.1 是否能独立解决问题"""
import sys
sys.path.insert(0, 'd:\\AI\\somn')
sys.path.insert(0, 'd:\\AI\\somn\\knowledge_cells')
sys.path.insert(0, 'd:\\AI\\somn\\smart_office_assistant\\src')

from knowledge_cells.core import get_engine

engine = get_engine()

tests = [
    ("简单信息查询", "什么是机器学习？", "information"),
    ("分析类问题", "分析一下新能源汽车市场的发展趋势", "analysis"),
    ("决策类问题", "选择 Python 还是 JavaScript 作为第一门编程语言？", "decision"),
]

print("=== v6.1.1 独立解决问题能力测试 ===\n")

all_ok = True
for name, problem, ptype in tests:
    print(f"【测试】{name}")
    print(f"  问题: {problem}")
    try:
        result = engine.dispatch(
            problem_desc=problem,
            problem_type=ptype
        )
        conf = result.output.get("confidence", 0.0)
        dispatched = result.dispatched_to
        print(f"  ✅ 置信度: {conf}")
        print(f"  调度至: {dispatched}")

        # 检查输出质量
        output = result.output.get("output", {})
        if isinstance(output, dict):
            answer = output.get("answer", output.get("conclusion", ""))
            if answer and len(str(answer)) > 20:
                print(f"  有实质回答: {str(answer)[:80]}...")
            else:
                print(f"  ⚠️ 回答内容较少或为空")
                all_ok = False
        print()
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        all_ok = False
        print()

print("=== 总体结论 ===")
if all_ok:
    print("✅ v6.1.1 能独立解决问题")
else:
    print("⚠️ v6.1.1 部分功能有问题，需要进一步检查")
