#!/usr/bin/env python3
"""查找 reinforcement_learning_v3.py 中 learn 方法的位置"""
with open(r"d:\AI\somn\smart_office_assistant\src\neural_memory\reinforcement_learning_v3.py", encoding="utf-8") as f:
    lines = f.readlines()

print("=== 包含 'def ' 的行 ===")
for i, line in enumerate(lines, 1):
    if "def " in line and not line.strip().startswith("#"):
        print(f"  Line {i}: {line.rstrip()}")

print("\n=== 包含 'learn' 的行 ===")
for i, line in enumerate(lines, 1):
    if "learn" in line.lower() and "all" not in line and "Learning" not in line:
        print(f"  Line {i}: {line.rstrip()}")
