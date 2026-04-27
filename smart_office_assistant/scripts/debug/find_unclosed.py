# -*- coding: utf-8 -*-
with open('src/intelligence/literary_narrative_engine.py', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

# 模拟Python tokenizer来找出不成对的三引号
in_string = False
string_start_line = None

for i, line in enumerate(lines, 1):
    j = 0
    while j < len(line):
        # 跳过转义字符
        if line[j] == '\\' and j + 1 < len(line):
            j += 2
            continue
        
        # 检查三引号
        if j + 2 < len(line) and line[j:j+3] == '"""':
            if not in_string:
                in_string = True
                string_start_line = i
            else:
                in_string = False
                string_start_line = None
            j += 3
            continue
        
        # 检查单引号和双引号字符串（简单版本）
        if line[j] in '"\'':
            quote = line[j]
            j += 1
            while j < len(line):
                if line[j] == '\\' and j + 1 < len(line):
                    j += 2
                    continue
                if line[j] == quote:
                    break
                j += 1
        else:
            j += 1
    
    if i > 950:  # 只检查前950行
        break

if in_string:
    print(f"Unclosed string starting at line {string_start_line}")
else:
    print("No unclosed string found")
