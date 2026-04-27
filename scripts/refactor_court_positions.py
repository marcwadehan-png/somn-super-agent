#!/usr/bin/env python3
"""
自动化重构 _court_positions.py
将各 _build_*_positions() 函数提取到独立模块
"""
import re
import sys
from pathlib import Path

BASE_DIR = Path("d:/AI/somn/smart_office_assistant/src/intelligence/engines/cloning")

def extract_function(code: str, func_name: str) -> str:
    """从代码中提取指定函数的完整定义"""
    # 找到函数定义行
    pattern = rf'def {func_name}\s*\([^)]*\)\s*->\s*List\[Position\]:'
    match = re.search(pattern, code)
    if not match:
        return ""
    
    start = match.start()
    
    # 找到函数结束位置（下一个 def 或类定义，或文件结束）
    # 向后搜索，找到相同缩进的 def 或 class
    lines = code[start:].split('\n')
    result_lines = []
    base_indent = None
    
    for line in lines:
        if base_indent is None:
            result_lines.append(line)
            # 获取函数定义后的第一行缩进
            continue
        
        # 检查是否是新的顶层定义（def 或 class）
        stripped = line.lstrip()
        if stripped and not line.startswith('    ') and (stripped.startswith('def ') or stripped.startswith('class ')):
            break
        result_lines.append(line)
    
    return '\n'.join(result_lines)


def refactor():
    """执行重构"""
    original_file = BASE_DIR / "_court_positions.py"
    
    if not original_file.exists():
        print(f"错误：找不到文件 {original_file}")
        return
    
    code = original_file.read_text(encoding='utf-8')
    
    # 要提取的函数列表
    functions = [
        ("_build_royal_positions", "positions_royal.py"),
        ("_build_wenzhi_positions", "positions_wenzhi.py"),
        ("_build_economy_positions", "positions_economy.py"),
        ("_build_military_positions", "positions_military.py"),
        ("_build_standard_positions", "positions_standard.py"),
        ("_build_chuangxin_positions", "positions_chuangxin.py"),
        ("_build_review_positions", "positions_review.py"),
        ("_build_library_positions", "positions_library.py"),
        ("_build_congress_positions", "positions_congress.py"),
        ("_build_specialist_leaders", "positions_specialist.py"),
        ("_build_supplement_positions", "positions_supplement.py"),
    ]
    
    created_files = []
    
    for func_name, module_name in functions:
        func_code = extract_function(code, func_name)
        if not func_code:
            print(f"警告：未找到函数 {func_name}")
            continue
        
        # 添加文件头
        module_code = f'''# -*- coding: utf-8 -*-
"""
朝廷岗位体系 - {func_name.replace('_build_', '').replace('_positions', '')} 系统岗位
从 _court_positions.py 提取，V4.2.0
"""
from typing import List
from .court_enums import (
    NobilityRank, PinRank, PositionType, SystemType, SageType,
)
from .court_models import Position
from .court_helpers import _p, _zheng_cong_pair, _specialist_batch

{func_code}

__all__ = ['{func_name}']
'''
        
        module_file = BASE_DIR / module_name
        module_file.write_text(module_code, encoding='utf-8')
        created_files.append(module_name)
        print(f"已创建：{module_name}")
    
    print(f"\n共创建 {len(created_files)} 个模块")
    print("\n下一步：更新 _court_positions.py 主文件，导入这些模块")


if __name__ == "__main__":
    refactor()
