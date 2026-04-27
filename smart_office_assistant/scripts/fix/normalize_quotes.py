# -*- coding: utf-8 -*-
"""把所有Python单引号字符串改为双引号"""
import re

filepath = 'src/intelligence/persona_core.py'

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed_lines = []
for line in lines:
    new_line = line
    
    # 跳过注释
    if line.strip().startswith('#'):
        fixed_lines.append(new_line)
        continue
    
    # 跳过包含三引号的行
    if "'''" in line or '"""' in line:
        fixed_lines.append(new_line)
        continue
    
    # 跳过f-string行（已经处理过了）
    if "f'" in line or 'f"' in line:
        fixed_lines.append(new_line)
        continue
    
    # 把 = '...' 改为 = "..."
    # 匹配单引号字符串
    def replace_single_quotes(m):
        before = m.group(1)  # = 或 : 或 ,
        content = m.group(2)  # 字符串内容
        after = m.group(3)    # 结尾
        # 如果内容中有中文单引号，改用双引号
        if "'" in content:
            return before + '"' + content + '"' + after
        return before + "'" + content + "'" + after
    
    # 替换赋值语句中的单引号字符串
    new_line = re.sub(r"(\s*[=:]\s*)'([^']*)'(\s*[,\n])", replace_single_quotes, new_line)
    
    fixed_lines.append(new_line)

content = ''.join(fixed_lines)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Normalized quotes!")
