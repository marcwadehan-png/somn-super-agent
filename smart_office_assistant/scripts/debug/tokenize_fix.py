# -*- coding: utf-8 -*-
"""使用tokenize修复persona_core.py的引号问题"""
import tokenize
import io

filepath = 'src/intelligence/persona_core.py'

with open(filepath, 'rb') as f:
    content = f.read()

# 使用tokenize解析
tokens = list(tokenize.tokenize(io.BytesIO(content).readline))

result = []
i = 0
n = len(tokens)

while i < n:
    tok = tokens[i]
    
    if tok.type == tokenize.STRING:
        # 这是一个字符串字面量
        s = tok.string
        
        # 如果是f-string，替换内部的中文引号
        if s.startswith('f"') or s.startswith("f'"):
            # 替换内部的中文引号
            s = s.replace('"', "'").replace('"', "'")
            # 把边界改为三引号
            if s.startswith('f"') and s.endswith('"') and not s.startswith('f"""'):
                s = 'f"""' + s[2:-1] + '"""'
            elif s.startswith("f'") and s.endswith("'") and not s.startswith("f'''"):
                s = "f'''" + s[2:-1] + "'''"
        
        result.append((tok.type, tok.start, tok.end, s, tok.string))
    else:
        result.append(tok)
    
    i += 1

# 生成新的代码
output = io.StringIO()
tokenize_util = tokenize.TokenInfo

# 手动重建tokens
for tok in result:
    if isinstance(tok, tuple):
        if tok[0] == tokenize.ENCODING:
            continue
        output.write(tok[3])

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(output.getvalue())

print("Fixed using tokenize!")
