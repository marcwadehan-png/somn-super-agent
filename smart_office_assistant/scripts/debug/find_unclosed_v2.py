# -*- coding: utf-8 -*-
with open('src/intelligence/literary_narrative_engine.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到不成对的 """
in_triple = False
triple_start = None
issues = []

for i, line in enumerate(lines, 1):
    # 跳过f-string中的"""
    clean_line = line
    if 'f"""' in line or "f'''" in line:
        # 跳过f-string开始
        pass
    
    count = line.count('"""')
    if count == 1:
        if not in_triple:
            in_triple = True
            triple_start = i
        else:
            issues.append(f"Line {i}: Unexpected closing \"\"\" (was open since {triple_start})")
            in_triple = False
            triple_start = None
    elif count == 2:
        # 两个""" - opens and closes
        if in_triple:
            issues.append(f"Line {i}: Extra opening \"\"\" (was open since {triple_start})")
            in_triple = False
            triple_start = None
        # 正常: 打开然后关闭在同一行
    elif count > 2:
        # 可能有特殊情况
        if count % 2 == 1:
            issues.append(f"Line {i}: Odd number ({count}) of \"\"\" - possible unclosed string")
        if in_triple:
            in_triple = False
            triple_start = None

if in_triple:
    print(f"UNCLOSED triple-quoted string starting at line {triple_start}")
else:
    print("All triple quotes appear matched")

print(f"\nIssues found: {len(issues)}")
for issue in issues[:20]:
    print(issue)
