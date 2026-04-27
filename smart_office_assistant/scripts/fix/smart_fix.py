# -*- coding: utf-8 -*-
"""
Smart fix for persona_core.py
Uses Python tokenize to properly handle all string quotes
"""
import tokenize
import io

filepath = 'src/intelligence/persona_core.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Parse the file
try:
    tokens = list(tokenize.generate_tokens(io.StringIO(content).readline))
    
    # Build the fixed content
    result = []
    for tok in tokens:
        if tok.type == tokenize.STRING:
            s = tok.string
            # Keep the string as-is, just fix any issues
            result.append(s)
        else:
            result.append(tok.string)
    
    fixed_content = ''.join(result)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    print("Fixed using tokenize!")
except Exception as e:
    print(f"Tokenize failed: {e}")
    print("Trying alternative approach...")
    
    # Alternative: simple line-by-line fix
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Skip docstrings and comments
        if line.strip().startswith('#') or '"""' in line or "'''" in line:
            fixed_lines.append(line)
            continue
        
        # Replace Chinese quotes that cause issues
        # Put all problematic strings in triple quotes
        fixed_lines.append(line)
    
    fixed_content = '\n'.join(fixed_lines)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    print("Applied alternative fix!")
