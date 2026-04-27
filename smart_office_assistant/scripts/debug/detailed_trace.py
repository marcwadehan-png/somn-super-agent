# -*- coding: utf-8 -*-
import ast

with open('src/intelligence/literary_narrative_engine.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 使用AST来查找问题
try:
    ast.parse(content)
    print("AST parse successful")
except SyntaxError as e:
    print(f"SyntaxError at line {e.lineno}: {e.msg}")
    print(f"Text: {e.text}")
    if e.lineno:
        lines = content.split('\n')
        start = max(0, e.lineno - 5)
        end = min(len(lines), e.lineno + 3)
        print("\nContext:")
        for i in range(start, end):
            marker = ">>>" if i + 1 == e.lineno else "   "
            print(f"{marker} Line {i+1}: {lines[i][:80]}")
