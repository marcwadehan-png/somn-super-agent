# -*- coding: utf-8 -*-
with open('src/intelligence/literary_narrative_engine.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

line488 = lines[487]  # 0-indexed
print(f"Line 488: {repr(line488)}")
print(f"Decoded: {line488}")

# 查找所有包含 """ 的行
for i, line in enumerate(lines, 1):
    if '"""' in line:
        print(f"Line {i}: {repr(line[:100])}")
