#!/usr/bin/env python3
"""查找 graph_engine.py 中所有 self.graph 和 self._nx_graph 的使用位置"""
import re

with open(r"d:\AI\somn\smart_office_assistant\src\knowledge_graph\graph_engine.py", encoding="utf-8") as f:
    lines = f.readlines()

print("=== self.graph 使用位置 ===")
for i, line in enumerate(lines, 1):
    if "self.graph" in line and "self.graph_loaded" not in line and "#" not in line.split("self.graph")[0]:
        print(f"  Line {i}: {line.rstrip()}")

print("\n=== self._nx_graph 使用位置 ===")
for i, line in enumerate(lines, 1):
    if "self._nx_graph" in line:
        print(f"  Line {i}: {line.rstrip()}")

print("\n=== 方法定义（判断哪些方法需要加 _ensure_graph）===")
for i, line in enumerate(lines, 1):
    if "def " in line and not line.strip().startswith("#"):
        print(f"  Line {i}: {line.rstrip()}")
