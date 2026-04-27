# -*- coding: utf-8 -*-
"""彻底修复persona_core.py - 把所有单引号字符串改为双引号"""
import re

filepath = 'src/intelligence/persona_core.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# 策略：
# 1. 把所有使用单引号的字符串改为使用双引号
# 2. 这要求内部不能有双引号
# 3. 如果内部有双引号，保持单引号

# 查找并替换所有单引号字符串
# 这是一个简单的字符串替换

# 使用一个更智能的方法：
# 找到所有使用单引号的赋值语句中的字符串，把它们改为双引号

# 匹配模式：'key': 'value' 或 'key': 'value', 或 'key': 'value'
# 需要把内部的单引号改为双引号（如果包含中文引号）

def replace_single_quoted_strings(text):
    """把所有包含中文单引号的单引号字符串改为双引号"""
    result = []
    i = 0
    n = len(text)
    
    while i < n:
        c = text[i]
        
        # 检查是否是单引号开始
        if c == "'" and (i == 0 or text[i-1] in '=:'):
            # 找字符串结束
            j = i + 1
            while j < n:
                if text[j] == '\\':
                    j += 2
                    continue
                if text[j] == "'":
                    break
                j += 1
            
            if j < n and text[j] == "'":
                substr = text[i:j+1]
                # 如果内部有中文单引号，改为双引号
                if "'" in substr:
                    result.append('"' + text[i+1:j] + '"')
                else:
                    result.append(substr)
                i = j + 1
                continue
        
        result.append(c)
        i += 1
    
    return ''.join(result)

# 简单版本：把所有中文单引号替换为双引号字符
# 然后把Python单引号改为双引号
result = []
i = 0
n = len(content)
in_string = False
string_char = None
string_start = -1

while i < n:
    c = content[i]
    
    # 检查是否在字符串中
    if not in_string:
        if c == "'" or c == '"':
            in_string = True
            string_char = c
            string_start = i
        else:
            result.append(c)
    else:
        if c == '\\':
            result.append(c)
            i += 1
            if i < n:
                result.append(content[i])
        elif c == string_char:
            # 字符串结束
            in_string = False
            result.append(c)
        else:
            result.append(c)
    
    i += 1

new_content = ''.join(result)

# 现在把中文单引号替换为中文双引号
new_content = new_content.replace("'", '"')

# 然后把外部引号统一处理
# 需要把 "xxx" 改为 "xxx"（保持不变）
# 但要确保没有引号不匹配的问题

# 简单处理：把所有外部单引号改为双引号
# 使用正则来匹配字符串

def replace_outer_quotes(text):
    """把外部单引号改为双引号"""
    result = []
    i = 0
    n = len(text)
    
    while i < n:
        c = text[i]
        
        # 检查是否是字符串开始（但不是转义）
        if c == "'" and (i == 0 or text[i-1] not in ('\\',)):
            # 检查上下文 - 如果后面有中文引号，改为双引号
            j = i + 1
            has_chinese_quote = False
            while j < n and text[j] != "'":
                if text[j] == '"':
                    has_chinese_quote = True
                    break
                j += 1
            
            if has_chinese_quote:
                # 把这个单引号改为双引号
                result.append('"')
                # 把内部的中文双引号改回单引号
                k = i + 1
                while k < n and text[k] != "'":
                    if text[k] == '"':
                        result.append("'")
                    else:
                        result.append(text[k])
                    k += 1
                result.append('"')
                i = k + 1
                continue
            else:
                result.append(c)
        else:
            result.append(c)
        
        i += 1
    
    return ''.join(result)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Done!")
