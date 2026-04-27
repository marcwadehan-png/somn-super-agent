# -*- coding: utf-8 -*-
"""从v4_deployment_data.json生成完整的V4部署文档Markdown"""

import json
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(PROJECT_ROOT, "docs", "v4_deployment_data.json")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "docs", "神之架构_V4.md")


def gen_doc():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    lines = []
    L = lines.append

    # ═══════ 标题与总览 ═══════
    L("# 神之架构 V4.0.0 - 完整任命部署文档")
    L("")
    L(f"> 生成时间：{data['generated_at']}")
    L(f"> 版本：{data['version']}")
    L("")
    L("---")
    L("")

    # 总览
    s = data['summary']
    L("## 一、总览")
    L("")
    L(f"| 指标 | 数值 |")
    L(f"|------|------|")
    L(f"| 总岗位数 | {s['total_positions']} |")
    L(f"| 总贤者数 | {s['total_sages']} |")
    L(f"| 成功任命 | {s['assigned_sages']} |")
    L(f"| 任命失败 | {s['failed_sages']} |")
    L(f"| 覆盖率 | {s['coverage_pct']}% |")
    L("")

    # 按部门统计
    L("## 二、按部门分布")
    L("")
    L("| 部门 | 人数 |")
    L("|------|------|")

    # 从by_department中获取实际分配人数
    # 但我们需要按分配排序
    dept_counts = {}
    for dept_key, dept_data in data['by_department'].items():
        total_assigned = sum(p['assigned_count'] for p in dept_data['positions'])
        dept_counts[dept_key] = total_assigned

    for dept, count in sorted(dept_counts.items(), key=lambda x: -x[1]):
        L(f"| {dept} | {count} |")
    L("")

    # 按爵位分布
    L("## 三、爵位任命概况")
    L("")
    L("| 爵位 | 岗位名 | 部门 | 品秩 | 类型 | 任命贤者 |")
    L("|------|--------|------|------|------|----------|")
    for item in data['by_nobility']:
        sages_str = ", ".join(item['sages'][:5]) if item['sages'] else "待任命"
        L(f"| {item['nobility']} | {item['position_name']} | {item['department']} | "
          f"{item['pin']} | {item['sage_type_symbol']} {item['sage_type']} | {sages_str} |")
    L("")

    # 实战派统计
    ps = data['practitioner_stats']
    L("## 四、贤者类型分布")
    L("")
    L("| 类型 | 岗位数 |")
    L("|------|--------|")
    L(f"| ⚔ 实战派 | {ps['practitioner_count']} |")
    L(f"| 📚 理论派 | {ps['theorist_count']} |")
    L(f"| ⚔📚 复合型 | {ps['dual_type_count']} |")
    L("")

    # 实战派达标
    L("## 五、各系统实战派达标检查")
    L("")
    L("| 系统 | 实战派 | 复合型 | 有效数 | 要求 | 状态 |")
    L("|------|--------|--------|--------|------|------|")
    for sys_name, check in data['practitioner_quota_check'].items():
        if check['status'] == 'skip':
            L(f"| {sys_name} | - | - | - | 无要求 | 跳过 |")
        else:
            st = "达标" if check['status'] == 'pass' else "未达标"
            L(f"| {sys_name} | {check['practitioner']} | {check['dual_type']} | "
              f"{check['effective']} | >={check['quota']} | {st} |")
    L("")

    # ═══════ 六、各部门完整岗位×人员安排 ═══════
    L("---")
    L("")
    L("## 六、各部门完整岗位与人员安排")
    L("")

    # 部门顺序
    dept_order = ["皇家", "文治系统", "经济系统", "军政系统", "标准系统", "创新系统", "审核系统", "皇家藏书阁"]

    for dept_name in dept_order:
        if dept_name not in data['by_department']:
            continue
        dept_data = data['by_department'][dept_name]
        positions = dept_data['positions']

        # 部门标题
        dept_title_map = {
            "皇家": "一、皇家系统",
            "文治系统": "二、文治系统（内阁/吏部/礼部）",
            "经济系统": "三、经济系统（户部）",
            "军政系统": "四、军政系统（兵部/五军都督府/厂卫）",
            "标准系统": "五、标准系统（刑部/工部/三法司）",
            "创新系统": "六、创新系统（皇家科学院/经济战略司/文化输出局）",
            "审核系统": "七、审核系统（翰林院）",
            "皇家藏书阁": "八、皇家藏书阁",
        }
        L(f"### {dept_title_map.get(dept_name, dept_name)}")
        L("")
        L(f"> 部门岗位总数：{dept_data['total_positions']}")
        L("")

        for pos in positions:
            # 岗位标题
            nobility_str = f"**{pos['nobility']}** " if pos['nobility'] != "无" else ""
            type_symbol = pos.get('sage_type_symbol', '')
            type_name = pos.get('sage_type', '')

            L(f"#### {pos['name']}")
            L("")
            L(f"- **岗位ID**: `{pos['id']}`")
            L(f"- **品秩**: {pos['pin']}（{'正品' if pos['is_zheng'] else '从品'}）")
            L(f"- **爵位**: {nobility_str.strip()}")
            L(f"- **系统**: {pos['system_type']}")
            L(f"- **类型**: {pos['position_type']}")
            L(f"- **容量**: {pos['capacity']}（已任命 {pos['assigned_count']}）")
            L(f"- **职能**: {pos['domain']}")
            if pos.get('si_name'):
                L(f"- **所属**: {pos['si_name']}")
            L(f"- **轨道**: {pos['track']}")
            if pos.get('dispatch_path'):
                L(f"- **调度路径**: {pos['dispatch_path']}")
            L(f"- **适合学派**: {', '.join(pos['suitable_schools'][:10])}")
            if type_name:
                L(f"- **贤者类型**: {type_symbol} {type_name}")
            if pos.get('description'):
                L(f"- **职责描述**: {pos['description']}")
            L("")
            # 任命人员
            if pos['assigned_sages']:
                L(f"**任命人员**（{len(pos['assigned_sages'])}人）:")
                L("")
                for i, sage in enumerate(pos['assigned_sages'], 1):
                    L(f"  {i}. {sage}")
            else:
                L("**任命人员**: 暂无")
            L("")

    # 七、品秩分布
    L("---")
    L("")
    L("## 七、品秩分布")
    L("")

    # 统计
    pin_counts = {}
    for pos in data['all_positions']:
        pin = pos['pin']
        if pin not in pin_counts:
            pin_counts[pin] = {"positions": 0, "assigned": 0}
        pin_counts[pin]["positions"] += 1
        pin_counts[pin]["assigned"] += pos['assigned_count']

    # 按品级排序
    pin_order = ["正一品", "从一品", "正二品", "从二品", "正三品", "从三品",
                 "正四品", "从四品", "正五品", "从五品", "正六品", "从六品",
                 "正七品", "从七品", "正八品", "从八品", "正九品", "从九品"]
    L("| 品秩 | 岗位数 | 任命人数 |")
    L("|------|--------|----------|")
    for pin in pin_order:
        if pin in pin_counts:
            c = pin_counts[pin]
            L(f"| {pin} | {c['positions']} | {c['assigned']} |")
    L("")

    # 八、失败列表
    if data.get('failed_sages'):
        L("## 八、未分配贤者")
        L("")
        for name in data['failed_sages']:
            L(f"- {name}")
        L("")

    L("---")
    L("")
    L("*神之架构V4.0.0 - 全贤就位，百官齐备 - 由Somn系统自动生成*")

    # 写入文件
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"V4部署文档已生成: {OUTPUT_PATH}")
    print(f"总行数: {len(lines)}")
    return OUTPUT_PATH


if __name__ == "__main__":
    gen_doc()
