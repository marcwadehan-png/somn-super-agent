# -*- coding: utf-8 -*-
"""保守修复persona_core.py - 只修复真正有问题的引号"""
import re

filepath = 'src/intelligence/persona_core.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# 策略：
# 1. 只修复 f'...' 和 f"..." 中的嵌套引号问题
# 2. 把所有 f-string 的引号统一改为三引号 f"""..."

# 处理f-string：统一使用三引号
def fix_fstring(match):
    prefix = match.group(1)  # f
    content_inner = match.group(2)  # 内容
    # 替换内部的中文引号为英文单引号
    content_inner = content_inner.replace('"', "'").replace('"', "'")
    return f'{prefix}"""{content_inner}"""'

# 修复所有f-string
content = re.sub(r"(f)\"([^\"]*)\"", fix_fstring, content)
content = re.sub(r"(f)'([^']*)'", fix_fstring, content)

# 只把f-string的引号改为三引号，不动其他字符串
# 这应该能解决所有问题

if content != original:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed!")
else:
    print("No changes needed")
