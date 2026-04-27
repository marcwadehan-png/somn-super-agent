#!/usr/bin/env python3
"""
处理项目中的 TODO/FIXME 注释
可以选择：删除、转换为 NOTE、或生成任务清单
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path("d:/AI/somn")
PROTECTED_DIRS = {
    "data/memory_v2", "data/q_values", "data/learning",
    "data/solution_learning", "data/memory", "data/feedback_production",
    "data/feedback_loop", "data/reasoning", "data/ml"
}

def is_protected(path_str):
    rel = os.path.relpath(path_str, "d:/AI/somn").replace("\\", "/")
    return any(rel.startswith(p) for p in PROTECTED_DIRS)

def find_todo_files():
    """查找包含 TODO/FIXME 的 Python 文件"""
    results = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        rel_root = os.path.relpath(root, PROJECT_ROOT).replace("\\", "/")
        if any(rel_root.startswith(p) for p in PROTECTED_DIRS):
            dirs[:] = []
            continue
        for file in files:
            if file.endswith(".py"):
                fp = os.path.join(root, file)
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                    todos = []
                    for i, line in enumerate(lines, 1):
                        if re.search(r"\b(TODO|FIXME|HACK|XXX)\b", line, re.IGNORECASE):
                            todos.append((i, line.rstrip()))
                    if todos:
                        results.append({"file": fp, "todos": todos})
                except:
                    pass
    return results

def main():
    print("=" * 60)
    print("TODO/FIXME 注释处理工具")
    print("=" * 60)
    
    results = find_todo_files()
    print(f"\n找到 {len(results)} 个文件包含 TODO/FIXME：\n")
    
    for item in results:
        rel_path = os.path.relpath(item["file"], PROJECT_ROOT)
        print(f"  {rel_path} ({len(item['todos'])} 条)")
        for line_no, content in item["todos"][:3]:  # 只显示前3条
            print(f"    L{line_no}: {content[:80]}")
        if len(item["todos"]) > 3:
            print(f"    ... 还有 {len(item['todos']) - 3} 条")
        print()
    
    # 生成任务清单
    report_path = PROJECT_ROOT / "file/系统文件/TODO任务清单.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# TODO/FIXME 任务清单\n\n")
        f.write(f"生成时间: {os.path.basename(__file__)}\n\n")
        for item in results:
            rel_path = os.path.relpath(item["file"], PROJECT_ROOT)
            f.write(f"## {rel_path}\n\n")
            for line_no, content in item["todos"]:
                f.write(f"- **L{line_no}**: `{content.strip()}`\n")
            f.write("\n")
    
    print(f"任务清单已保存至: {report_path}")
    print(f"\n建议：逐项审查这些 TODO/FIXME，决定是删除、实现还是保留。")

if __name__ == "__main__":
    main()
