#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从Claw任职报告_V6.0.md提取所有岗位，
对比架构文档的422目标，找出缺失的岗位
"""
import re

# 读取任职报告
with open('d:/AI/somn/file/系统文件/Claw任职报告_V6.0.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取第四节"管理层岗位填充详情"表格
# 格式: | PID | 岗位名称 | 部门 | 品秩 | 爵位 | 填充Claw |
pattern = r'\| (\w+)\s*\| ([^|]+)\| ([^|]+)\| ([^|]+)\| ([^|]*)\| ([^|]*) \|'
matches = re.findall(pattern, content)

print("从任职报告提取的岗位数: {}".format(len(matches)))
print("\n前10个岗位:")
for i, m in enumerate(matches[:10]):
    print("  {}: {} - {}".format(m[0], m[1].strip(), m[2].strip()))

# 保存到JSON
import json
positions = {}
for m in matches:
    pid = m[0].strip()
    positions[pid] = {
        'name': m[1].strip(),
        'department': m[2].strip(),
        'pin': m[3].strip(),
        'nobility': m[4].strip(),
    }

with open('d:/AI/somn/scripts/positions_from_report.json', 'w', encoding='utf-8') as f:
    json.dump(positions, f, ensure_ascii=False, indent=2)

print("\n已保存到: d:/AI/somn/scripts/positions_from_report.json")
print("唯一岗位ID数: {}".format(len(positions)))

# 对比我们之前提取的365个唯一岗位
with open('d:/AI/somn/scripts/extracted_positions.json', 'r', encoding='utf-8') as f:
    extracted = json.load(f)

print("\n提取的岗位数: {}".format(len(extracted)))
print("报告中提取的岗位数: {}".format(len(positions)))

# 找出在报告中但不在提取中的岗位
report_pids = set(positions.keys())
extracted_pids = set(extracted.keys())
missing = report_pids - extracted_pids
extra = extracted_pids - report_pids

print("\n只在报告中出现的岗位数: {}".format(len(missing)))
if missing:
    print("示例:")
    for pid in list(missing)[:10]:
        print("  {}: {}".format(pid, positions[pid]['name']))

print("\n只在提取中出现的岗位数: {}".format(len(extra)))
if extra:
    print("示例:")
    for pid in list(extra)[:10]:
        print("  {}: {}".format(pid, extracted[pid]['name']))
