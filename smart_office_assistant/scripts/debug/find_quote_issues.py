# -*- coding: utf-8 -*-
"""扫描并修复中文引号嵌套问题"""
import os
import re

def scan_for_quote_issues():
    """扫描所有Python文件中的中文引号问题"""
    src_dir = 'src'
    files_with_issues = []
    
    for root, dirs, files in os.walk(src_dir):
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.trash']]
        for f in files:
            if f.endswith('.py'):
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                        # 查找所有字符串字面量
                        lines = content.split('\n')
                        for i, line in enumerate(lines, 1):
                            # 检查是否有中文引号在字符串中
                            if ('"' in line or '"' in line) and "'" not in line:
                                # 这行可能有问题
                                stripped = line.strip()
                                if stripped and not stripped.startswith('#'):
                                    # 检查是否是赋值语句
                                    if '=' in stripped and not stripped.startswith('='):
                                        files_with_issues.append((filepath, i, stripped[:100]))
                except:
                    pass
    return files_with_issues

def fix_chinese_quotes_in_file(filepath):
    """修复文件中的中文引号嵌套问题"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # 替换中文引号为单引号
        content = content.replace('"', "'")
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

if __name__ == '__main__':
    print("=== Scanning for Chinese quote issues ===")
    issues = scan_for_quote_issues()
    print(f"Found {len(issues)} potential issues")
    
    # 列出前20个
    for filepath, line, content in issues[:20]:
        print(f"{filepath}:{line}")
        print(f"  {content}")
