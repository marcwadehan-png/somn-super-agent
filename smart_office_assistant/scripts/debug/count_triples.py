# -*- coding: utf-8 -*-
with open('src/intelligence/literary_narrative_engine.py', 'rb') as f:
    content = f.read()

# 找到所有三引号的位置
pos = 0
triple_positions = []
while pos < len(content):
    if content[pos:pos+3] == b'"""':
        triple_positions.append(pos)
        pos += 3
    else:
        pos += 1

print(f"Total triple quotes found: {len(triple_positions)}")
print(f"Positions: {triple_positions}")

# 找出行号
lines = content.split(b'\n')
for i, pos in enumerate(triple_positions):
    line_num = content[:pos].count(b'\n') + 1
    col = pos - content.rfind(b'\n', 0, pos)
    print(f"Position {pos}: line {line_num}, column {col}")
