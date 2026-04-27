# -*- coding: utf-8 -*-
import tokenize
import io

with open('src/intelligence/literary_narrative_engine.py', 'rb') as f:
    content = f.read()

# 手动查找三引号
pos = 0
in_triple = False
triple_start = None
issues = []

while pos < len(content):
    if content[pos:pos+3] == b'"""':
        if not in_triple:
            in_triple = True
            triple_start = pos
        else:
            in_triple = False
            triple_start = None
        pos += 3
    else:
        pos += 1

if in_triple:
    print(f"Unclosed triple quote starting at byte position {triple_start}")
    # 找到对应的行号
    lines = content[:triple_start].count(b'\n') + 1
    print(f"Which is approximately line {lines}")
