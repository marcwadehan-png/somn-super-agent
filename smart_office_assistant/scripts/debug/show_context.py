# -*- coding: utf-8 -*-
with open('src/intelligence/literary_narrative_engine.py', 'rb') as f:
    content = f.read()

# 找到字节位置 42521
pos = 42521

# 显示上下文
start = max(0, pos - 100)
end = min(len(content), pos + 100)
print(f"Content around position {pos}:")
print(repr(content[start:end]))
print()

# 找行号
line_num = content[:pos].count(b'\n') + 1
print(f"This is approximately line {line_num}")

# 显示前后几行
lines = content.split(b'\n')
print(f"\nLines around {line_num}:")
for i in range(max(0, line_num-3), min(len(lines), line_num+2)):
    print(f"Line {i+1}: {repr(lines[i][:100])}")
