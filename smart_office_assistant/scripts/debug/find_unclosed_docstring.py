# -*- coding: utf-8 -*-
with open('src/intelligence/literary_narrative_engine.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到所有三引号的位置
in_docstring = False
docstring_start = None
for i, line in enumerate(lines):
    if '"""' in line:
        if not in_docstring:
            in_docstring = True
            docstring_start = i + 1
        else:
            in_docstring = False
            docstring_start = None
    elif in_docstring and i - docstring_start > 200:  # 超过200行未闭合
        print(f'Possible unclosed docstring starting at line {docstring_start}')
        break

# 简单检查:每个 """ 应该是成对的
content = ''.join(lines)
# 计算简单的三引号数量
count = content.count('"""')
print(f'Total """ count: {count}')
if count % 2 != 0:
    print('Odd number of triple quotes - check for unclosed docstrings')
