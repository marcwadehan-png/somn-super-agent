#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 claw_appointment_results.json 提取唯一岗位列表
"""
import json

JSON_FILE = "d:/AI/somn/file/系统文件/claw_appointment_results.json"
OUTPUT_FILE = "d:/AI/somn/scripts/extracted_positions.json"

with open(JSON_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("总记录数: {}".format(len(data)))

# 提取唯一岗位
positions = {}
for r in data:
    pid = r.get('pos_id', '')
    if pid and pid not in positions:
        positions[pid] = {
            'name': r.get('position_name', ''),
            'department': r.get('department', ''),
            'pin': r.get('pin', ''),
            'nobility': r.get('nobility', ''),
            'domain': r.get('domain', ''),
            'si_name': r.get('si_name', ''),
        }

print("唯一岗位数: {}".format(len(positions)))

# 按部门分组
dept_stats = {}
for pid, info in positions.items():
    dept = info['department']
    dept_stats[dept] = dept_stats.get(dept, 0) + 1

print("\n各部门岗位数:")
for dept, cnt in sorted(dept_stats.items(), key=lambda x: -x[1]):
    print("  {}: {}".format(dept, cnt))

# 保存
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(positions, f, ensure_ascii=False, indent=2)

print("\n已保存到: {}".format(OUTPUT_FILE))

# 显示前30个岗位
print("\n前30个岗位:")
for i, (pid, info) in enumerate(sorted(positions.items())[:30]):
    print("  {}: {} ({})".format(pid, info['name'], info['department']))
