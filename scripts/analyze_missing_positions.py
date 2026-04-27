#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析缺失的岗位：对比实际提取的365个岗位和架构文档中的422个目标
"""
import json

# 从claw_appointment_results.json提取唯一岗位
with open('d:/AI/somn/file/系统文件/claw_appointment_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 提取唯一岗位
positions = {}
for r in data:
    pid = r.get('pos_id', '')
    if pid and pid not in positions:
        positions[pid] = {
            'name': r.get('position_name', ''),
            'department': r.get('department', ''),
        }

print("实际提取的唯一岗位数: {}".format(len(positions)))

# 按部门分组（合并统计）
dept_map = {
    '七人代表大会': ['七人代表大会'],
    '皇家': ['皇家', '皇家藏书阁'],
    '文治系统': ['内阁', '吏部', '礼部'],
    '经济系统': ['户部'],
    '军政系统': ['兵部', '五军都督府', '厂卫'],
    '标准系统': ['刑部', '工部', '三法司'],
    '创新系统': ['内阁'],  # 科学院/战略司/文化局属于内阁
    '审核系统': ['翰林院'],
}

# 实际统计
actual_stats = {}
for pid, info in positions.items():
    dept = info['department']
    actual_stats[dept] = actual_stats.get(dept, 0) + 1

# 合并统计
merged_stats = {}
for category, dept_list in dept_map.items():
    total = 0
    for dept in dept_list:
        total += actual_stats.get(dept, 0)
    merged_stats[category] = total

print("\n实际各部门岗位数（合并后）:")
for category, cnt in sorted(merged_stats.items(), key=lambda x: -x[1]):
    print("  {}: {}".format(category, cnt))

# 目标数量（从架构文档）
target_stats = {
    '七人代表大会': 7,
    '皇家系统': 22,
    '文治系统': 80,
    '经济系统': 44,
    '军政系统': 104,
    '标准系统': 87,
    '创新系统': 46,
    '审核系统': 8,
    '皇家藏书阁': 10,
    '专员领班': 9,
    '六部专员补充': 5,
}

print("\n对比目标数量:")
total_actual = 0
total_target = 0
for category in target_stats:
    actual = merged_stats.get(category, 0)
    target = target_stats.get(category, 0)
    diff = target - actual
    total_actual += actual
    total_target += target
    if diff != 0:
        print("  {}: 实际={}, 目标={}, 差异={}".format(category, actual, target, diff))
    else:
        print("  {}: {}/{} (OK)".format(category, actual, target))

print("\n总计: 实际={}, 目标={}, 缺失={}".format(total_actual, total_target, total_target - total_actual))

# 保存实际岗位列表
with open('d:/AI/somn/scripts/actual_positions.json', 'w', encoding='utf-8') as f:
    json.dump(positions, f, ensure_ascii=False, indent=2)
print("\n实际岗位列表已保存到: d:/AI/somn/scripts/actual_positions.json")
