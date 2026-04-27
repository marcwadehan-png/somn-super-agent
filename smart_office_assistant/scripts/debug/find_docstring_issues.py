# -*- coding: utf-8 -*-
with open('src/intelligence/literary_narrative_engine.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到不成对的三引号
in_docstring = False
start_line = None
docstrings = []

for i, line in enumerate(lines):
    stripped = line.strip()
    
    # 跳过注释行中的三引号
    if stripped.startswith('#'):
        continue
    
    # 跳过包含 f"..." 的行 (这些是正常的)
    if stripped.startswith('f"'):
        continue
    
    count = stripped.count('"""')
    if count == 1:
        if not in_docstring:
            in_docstring = True
            start_line = i + 1
        else:
            # 意外的单个三引号
            docstrings.append(f"Line {i+1}: Unexpected single '\"\"\"' - {stripped[:60]}")
    elif count == 2:
        if in_docstring:
            docstrings.append(f"Line {i+1}: Docstring closed (was open since {start_line})")
            in_docstring = False
            start_line = None
        else:
            # 正常的函数/类文档字符串
            pass
    elif count >= 3:
        docstrings.append(f"Line {i+1}: Multiple '\"\"\"' - {stripped[:80]}")

if in_docstring:
    print(f"Unclosed docstring starting at line {start_line}")
else:
    print("All docstrings appear to be closed")

print(f"\nTotal docstring events: {len(docstrings)}")
for d in docstrings[:20]:
    print(d)
