# -*- coding: utf-8 -*-
"""彻底重建persona_core.py的正确引号"""
import re

filepath = 'src/intelligence/persona_core.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 策略：把所有错误的中文引号改回正确的Python引号
# 问题是：所有的 "xxx" 变成了 xxx"
# 需要把 xxx" 改为 "xxx"

# 匹配模式：在等号、冒号、逗号后面，没有引号开头的字符串
def fix_missing_quotes(line):
    # 如果行中有 xxx" 这样的模式，且前面是 = 或 : 或 , 或 ( 或 [ 或 {
    # 就需要修复
    result = line
    
    # 修复模式1: self.xxx = value" -> self.xxx = "value"
    # 匹配 = xxx" 或 : xxx" 等
    result = re.sub(r"""([=:,\[(\{]\s*)([^'"][^,;\)]*)\"""", r'\1"\2"', result)
    
    # 修复模式2: "xxx"y y" -> "xxx'yyy" (嵌套中文引号)
    
    return result

# 逐行处理
lines = content.split('\n')
fixed_lines = []

for line in lines:
    new_line = line
    
    # 跳过文档字符串和注释
    stripped = line.strip()
    if stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
        fixed_lines.append(line)
        continue
    
    # 检查是否在多行字符串中
    if '"""' in line or "'''" in line:
        fixed_lines.append(line)
        continue
    
    # 修复开头的引号问题
    # 例如:     "Somn 基础人设档案"" ->     """Somn 基础人设档案"""
    if re.match(r"^\s*[^\"']+\"", line):
        # 行开头有 xxx" 模式
        # 需要在前面加引号
        new_line = re.sub(r"""^(\s*)([^"']+)(\")$""", r'\1"""\2"""', line)
        if new_line != line:
            fixed_lines.append(new_line)
            continue
    
    # 修复 = xxx" 模式
    if '="' in line or "='" in line:
        # 需要在 = 后面加引号
        new_line = re.sub(r'(= )([^"\'].*?")', r'\1"\2', line)
        new_line = re.sub(r'(= )([^"\'].*?)$', r'\1"\2"', new_line)
    
    fixed_lines.append(new_line)

fixed_content = '\n'.join(fixed_lines)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("Rebuilt!")
