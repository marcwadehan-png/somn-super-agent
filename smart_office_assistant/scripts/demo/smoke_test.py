# -*- coding: utf-8 -*-
"""Somn 系统冒烟测试脚本"""

import sys
sys.path.insert(0, '.')

print('=== Somn 系统冒烟测试 ===')
print()

# 测试核心模块
modules = [
    'src.intelligence.persona_core',
    'src.intelligence.unified_intelligence_coordinator',
    'src.intelligence.wisdom_dispatcher',
    'src.intelligence.wisdom_fusion_core',
    'src.intelligence.neural_voice_core',
    'src.core.somn_core',
    'src.neural_memory.semantic_memory_engine',
]

passed = 0
for mod in modules:
    try:
        __import__(mod)
        print(f'  OK  {mod}')
        passed += 1
    except Exception as e:
        print(f'  ERR {mod}: {str(e)[:80]}')

print()
print(f'模块导入: {passed}/{len(modules)} 通过')
print()

# 测试SomnCore实例化
print('=== SomnCore 实例化测试 ===')
try:
    from src.core.somn_core import SomnCore
    core = SomnCore()
    print('  OK  SomnCore 实例化成功')
    persona_status = "已加载" if hasattr(core, "persona") and core.persona else "未加载"
    wisdom_status = "已加载" if hasattr(core, "wisdom") else "未加载"
    coord_status = "已加载" if hasattr(core, "unified_coordinator") else "未加载"
    print(f'      persona: {persona_status}')
    print(f'      wisdom: {wisdom_status}')
    print(f'      unified_coordinator: {coord_status}')
except Exception as e:
    print(f'  ERR SomnCore: {e}')
    import traceback
    traceback.print_exc()

print()
print('=== 测试完成 ===')
