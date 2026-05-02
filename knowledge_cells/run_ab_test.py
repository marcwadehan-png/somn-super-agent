#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quick A/B test runner"""
import sys, os
sys.path.insert(0, r'd:\AI\somn\knowledge_cells')
os.chdir(r'd:\AI\somn\knowledge_cells')

print('=== G1: 导入测试 ===')
from eight_layer_pipeline import EightLayerPipeline, PipelineResult
from domain_nexus import DomainNexus
from output_engine import OutputEngine
from divine_oversight import DivineTrackOversight
from reasoning_web_bridge import ReasoningWebBridge
from output_verifier import OutputVerifier
print('All imports OK')

print('\n=== 验证新模块 ===')
bridge = ReasoningWebBridge(session_id='test')
verifier = OutputVerifier()
print('New modules smoke test OK')

print('\n=== 运行 pytest ===')
import subprocess
result = subprocess.run(
    [r'C:\Users\18000\.workbuddy\binaries\python\versions\3.13.12\python.exe', '-m', 'pytest',
     'test_sage_ab.py', '--tb=short', '-q'],
    capture_output=True, text=True, cwd=r'd:\AI\somn\knowledge_cells'
)
# 只显示关键行
for line in result.stdout.split('\n'):
    if any(k in line for k in ['PASSED', 'FAILED', 'passed', 'failed', 'error', '=====']):
        print(line)
# 也显示错误
if result.stderr:
    for line in result.stderr.split('\n'):
        if 'FAILED' in line or 'ERROR' in line:
            print(line)
print('\nReturn code:', result.returncode)
