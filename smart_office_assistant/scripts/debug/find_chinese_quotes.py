"""查找所有包含中文引号的Python文件"""
import os
import re

found = []
for root, dirs, files in os.walk('src'):
    if '__pycache__' in root or '.trash' in root:
        continue
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                # 查找中文引号
                if '"' in content or '"' in content or '"' in content or '"' in content:
                    found.append(path)
            except:
                pass

print(f"Found {len(found)} files with Chinese quotes:")
for p in found:
    print(f"  {p}")
