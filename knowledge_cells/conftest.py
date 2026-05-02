"""
conftest.py — 阻止 pytest 收集 test_sage_ab.py 中的自定义测试函数

test_sage_ab.py 使用自定义 Tester 框架，测试函数 return (ok, msg) tuple，
不符合 pytest 规范，会触发 PytestReturnNotNoneWarning。

本文件让 pytest 跳过对这些函数的收集，只保留 Tester 框架的执行路径。
"""


def pytest_collection_modifyitems(config, items):
    """
    在收集阶段过滤掉 test_sage_ab.py 中的 test_xxx 函数。
    Tester 框架会通过 t.test() 统一执行它们并生成报告。
    """
    filtered = []
    for item in items:
        # item.location: (file_path, line, test_name)
        loc_file = item.location[0] if item.location else ""
        if "test_sage_ab.py" in loc_file:
            # 跳过 test_sage_ab.py 收集的 test_ 函数
            continue
        filtered.append(item)
    items[:] = filtered
