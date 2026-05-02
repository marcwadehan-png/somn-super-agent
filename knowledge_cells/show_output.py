"""查看 v6.1.1 实际输出内容"""
import sys, json
sys.path.insert(0, r"d:\AI\somn")
sys.path.insert(0, r"d:\AI\somn\knowledge_cells")
sys.path.insert(0, r"d:\AI\somn\smart_office_assistant\src")

from knowledge_cells.core import dispatch

problems = [
    "什么是机器学习？",
    "分析一下新能源汽车市场的发展趋势",
]

for p in problems:
    print(f"【问题】{p}")
    try:
        result = dispatch(problem=p)
        output = result.output
        print("输出类型:", type(output))
        print("输出内容:")
        print(json.dumps(output, ensure_ascii=False, indent=2)[:1000])
        print()
        print("---")
        print()
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        print()
