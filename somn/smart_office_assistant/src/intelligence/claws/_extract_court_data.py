# -*- coding: utf-8 -*-
"""
神之架构岗位数据提取脚本
=========================

从_court_positions.py中提取岗位定义和贤者任命信息

执行方式：
    python _extract_court_data.py
"""

import re
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[4]
court_file = PROJECT_ROOT / "smart_office_assistant" / "src" / "intelligence" / "engines" / "cloning" / "_court_positions.py"

logger.info("提取神之架构岗位数据...")

with open(court_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 提取岗位定义
# 格式: id="XXX", name="岗位名", department="部门"
pos_pattern = r'id\s*=\s*"([^"]+)"\s*,\s*name\s*=\s*"([^"]+)"\s*,\s*department\s*=\s*"([^"]+)"'
pos_matches = re.findall(pos_pattern, content)

positions = {}
for pos_id, name, dept in pos_matches:
    positions[pos_id] = {"name": name, "department": dept}

logger.info(f"找到 {len(positions)} 个岗位定义")

# 2. 提取贤者任命 - 从_builtin_assignments
# 格式: "孔子": "HJ_WJ_01"
builtin_pattern = r'"([^"]+)"\s*:\s*"([A-Z_]+\d+)"'
matches = re.findall(builtin_pattern, content)

# 过滤出有效的岗位任命
assignments = {}
for name, pos_id in matches:
    if pos_id in positions:
        assignments[name] = pos_id

logger.info(f"找到 {len(assignments)} 个贤者任命")

# 3. 保存
output_data = {
    "positions": positions,
    "assignments": assignments,
}

output_file = PROJECT_ROOT / "_court_data.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

logger.info(f"保存到: {output_file}")

# 显示前10个任命
logger.info("\n前10个贤者任命:")
for i, (name, pos) in enumerate(list(assignments.items())[:10]):
    pos_name = positions.get(pos, {}).get("name", "")
    pos_dept = positions.get(pos, {}).get("department", "")
    logger.info(f"  {name} -> {pos} ({pos_name}, {pos_dept})")