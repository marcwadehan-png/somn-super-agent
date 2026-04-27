# -*- coding: utf-8 -*-
"""最简单直接的修复 - 把所有f-string改为三引号"""
import re

filepath = 'src/intelligence/persona_core.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# 策略：
# 1. 把所有 f"..." 改为 f"""..."""
# 2. 把所有 f'...' 改为 f'''...'''
# 3. 把所有包含中文引号的字符串边界统一处理

def fix_fstring_double(match):
    """修复 f"..." 中的嵌套引号"""
    inner = match.group(1)
    # 替换内部的中文引号为单引号
    inner = inner.replace('"', "'").replace('"', "'")
    return f'f"""{inner}"""'

def fix_fstring_single(match):
    """修复 f'...' 中的嵌套引号"""
    inner = match.group(1)
    # 替换内部的中文引号为单引号
    inner = inner.replace('"', "'").replace('"', "'")
    return f"f'''{inner}'''"

# 修复f-string
content = re.sub(r'f"([^"]*)"', fix_fstring_double, content)
content = re.sub(r"f'([^']*)'", fix_fstring_single, content)

# 把所有普通字符串中的中文引号替换为单引号
# 这应该处理所有剩余问题
content = content.replace('"', "'").replace('"', "'")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
