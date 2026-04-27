# -*- coding: utf-8 -*-
"""
提取神之架构贤者-岗位映射
==========================

从_court_positions.py的assign_sage调用中提取映射关系

执行方式：
    python _extract_court_mapping.py
"""

import re
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[4]
court_file = PROJECT_ROOT / "smart_office_assistant" / "src" / "intelligence" / "engines" / "cloning" / "_court_positions.py"

logger.info("提取神之架构贤者-岗位映射...")

with open(court_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 查找所有 assign_sage 调用
# 格式: self.assign_sage("贤者名", "岗位ID")
pattern = r'self\.assign_sage\s*\(\s*"([^"]+)"\s*,\s*"([A-Z_]+)"\s*\)'

matches = re.findall(pattern, content)
logger.info(f"找到 {len(matches)} 个 assign_sage 调用")

# 构建映射
mapping = {}
for sage_name, pos_id in matches:
    mapping[sage_name] = pos_id

# 保存
output_file = PROJECT_ROOT / "_court_position_mapping.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2)

logger.info(f"保存到: {output_file}")
logger.info(f"共 {len(mapping)} 个映射")

# 显示前20个
logger.info("\n前20个映射:")
for i, (name, pos) in enumerate(list(mapping.items())[:20]):
    logger.info(f"  {name} -> {pos}")