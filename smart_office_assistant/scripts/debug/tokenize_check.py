# -*- coding: utf-8 -*-
import tokenize
import io

with open('src/intelligence/literary_narrative_engine.py', 'rb') as f:
    content = f.read()

try:
    tokens = list(tokenize.tokenize(io.BytesIO(content).readline))
    print(f"Tokenization successful, {len(tokens)} tokens")
except tokenize.TokenError as e:
    print(f"TokenError: {e}")
except SyntaxError as e:
    print(f"SyntaxError: {e}")
