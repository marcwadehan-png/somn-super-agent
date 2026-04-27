# -*- coding: utf-8 -*-
"""精确修复persona_core.py中的引号问题"""
import re

filepath = 'src/intelligence/persona_core.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# 简单策略：
# 1. 把所有包含中文单引号 '...' 的字符串改为双引号 "..."
# 2. 使用三引号来处理复杂情况

# 找到所有使用单引号包裹的字符串，如果内部有中文单引号，改为双引号
def fix_string(match):
    quote = match.group(1)  # 引号类型
    content_inner = match.group(2)  # 内容
    trailing = match.group(3)  # 结尾
    
    if quote == "'" and "'" in content_inner:
        # 有嵌套的单引号，改为双引号
        return '"' + content_inner + '"' + trailing
    return match.group(0)

# 只处理字典值中的字符串（包含中文引号的）
# 匹配 'key': 'value' 或 "key": 'value' 模式
content = re.sub(r"(\s*[=:]\s*)'([^']*?)'(\s*[,\n\]])", fix_string, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed!")
