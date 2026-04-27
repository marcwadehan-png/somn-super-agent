# -*- coding: utf-8 -*-
"""系统性修复persona_core.py的所有引号问题"""
import re

filepath = 'src/intelligence/persona_core.py'

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed_lines = []
in_multiline_string = False

for i, line in enumerate(lines):
    new_line = line
    
    # 跳过文档字符串和注释
    stripped = line.strip()
    if stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
        fixed_lines.append(line)
        continue
    
    # 检查是否在多行字符串中
    if '"""' in line or "'''" in line:
        # 切换多行字符串状态
        if in_multiline_string:
            in_multiline_string = False
        else:
            in_multiline_string = True
        fixed_lines.append(line)
        continue
    
    if in_multiline_string:
        fixed_lines.append(line)
        continue
    
    # 修复单引号字符串中的中文引号问题
    # 策略：把包含中文单引号的单引号字符串改为双引号
    
    # 匹配赋值语句中的字符串
    # 例如: self.x = 'value' 或 'key': 'value'
    
    # 修复模式1: = '...' 
    # 如果 '...' 内部包含 '，改为双引号
    def fix_single_quoted(m):
        prefix = m.group(1)  # = 或 : 
        content = m.group(2)  # 字符串内容
        suffix = m.group(3)  # , 或 ) 或 [ 或 ]
        
        if "'" in content:  # 内部有中文单引号
            # 改用双引号
            return prefix + '"' + content + '"' + suffix
        return m.group(0)
    
    # 匹配 = '...' 或 : '...' 或 , '...' 或 [ '...' 或 ( '...' 或 { '...
    new_line = re.sub(r"([=:,\(\[\{]\s*)'([^']*)'(\s*[,\)\]\}])", fix_single_quoted, new_line)
    
    fixed_lines.append(new_line)

fixed_content = ''.join(fixed_lines)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("Systematic fix applied!")
