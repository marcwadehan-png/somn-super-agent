# -*- coding: utf-8 -*-
"""
神之架构V4 - 自动任命与部署数据生成脚本
运行此脚本将：
1. 初始化CourtPositionRegistry
2. 执行auto_assign_all_sages()为862位贤者自动分配岗位
3. 输出完整的V4部署数据到JSON文件
"""

import sys
import os
import json

# 确保项目根在sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def main():
    print("=" * 70)
    print("神之架构V4 - 贤者自动任命与部署数据生成")
    print("=" * 70)

    # 1. 导入并初始化
    print("\n[1/5] 初始化岗位注册中心...")
    from src.intelligence.engines.cloning._court_positions import (
        CourtPositionRegistry, get_court_registry,
        NobilityRank, PinRank, SageType, SystemType, PositionType,
        _NOBILITY_NAMES, _PIN_NAMES, _SAGE_TYPE_NAMES, _SAGE_TYPE_SYMBOLS,
    )

    registry = get_court_registry()
    print(f"  岗位注册中心初始化完成")

    # 2. 获取初始统计
    stats = registry.get_stats()
    print(f"\n[2/5] 岗位体系概览:")
    print(f"  总岗位数: {stats['total_positions']}")
    print(f"  固定容量: {stats['total_fixed_capacity']}")
    print(f"  专员岗位: {stats['specialist_positions']}")
    print(f"  爵位岗位: {stats['noble_positions']}")
    print(f"  部门数: {stats['departments']}")

    # 3. 自动分配
    print(f"\n[3/5] 开始自动分配862位贤者...")
    assign_result = registry.auto_assign_all_sages()
    print(f"  总贤者: {assign_result['total']}")
    print(f"  成功分配: {assign_result['assigned']}")
    print(f"  分配失败: {assign_result['failed']}")
    if assign_result['failed_sages']:
        print(f"  失败列表(前20): {assign_result['failed_sages'][:20]}")

    # 4. 生成完整部署数据
    print(f"\n[4/5] 生成V4完整部署数据...")

    deployment = {
        "version": "V4.0.0",
        "generated_at": "",
        "summary": {
            "total_positions": stats['total_positions'],
            "total_sages": assign_result['total'],
            "assigned_sages": assign_result['assigned'],
            "failed_sages": assign_result['failed'],
            "coverage_pct": round(assign_result['assigned'] / max(assign_result['total'], 1) * 100, 1),
        },
        "by_department": {},
        "by_nobility": {},
        "all_positions": [],
        "failed_sages": assign_result['failed_sages'],
    }

    from datetime import datetime
    deployment["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 按部门组织
    all_departments = registry.get_all_departments()
    for dept_name in all_departments:
        dept_positions = registry.get_positions_by_department(dept_name)
        dept_data = {
            "department": dept_name,
            "total_positions": len(dept_positions),
            "positions": []
        }

        for pos in dept_positions:
            pos_sages = pos.assigned_sages if pos.assigned_sages else []
            pos_entry = {
                "id": pos.id,
                "name": pos.name,
                "department": pos.department,
                "system_type": pos.system_type.value,
                "nobility": _NOBILITY_NAMES.get(pos.nobility, "无"),
                "pin": _PIN_NAMES.get(pos.pin, str(pos.pin.value)),
                "is_zheng": pos.is_zheng,
                "position_type": pos.position_type.value,
                "capacity": pos.capacity,
                "assigned_count": len(pos_sages),
                "assigned_sages": pos_sages[:50],  # 限制输出
                "domain": pos.domain,
                "si_name": pos.si_name,
                "track": pos.track,
                "dispatch_path": pos.dispatch_path,
                "suitable_schools": pos.suitable_schools,
                "description": pos.description,
                "sage_type": _SAGE_TYPE_NAMES.get(pos.sage_type, "") if pos.sage_type else "",
                "sage_type_symbol": _SAGE_TYPE_SYMBOLS.get(pos.sage_type, "") if pos.sage_type else "",
                "authority_value": pos.authority_value,
            }
            dept_data["positions"].append(pos_entry)
            deployment["all_positions"].append(pos_entry)

        # 按品秩排序
        dept_data["positions"].sort(key=lambda x: x["authority_value"])
        deployment["by_department"][dept_name] = dept_data

    # 爵位概况
    noble_overview = registry.get_nobility_overview()
    deployment["by_nobility"] = noble_overview

    # 实战派统计
    practitioner_stats = registry.get_practitioner_stats()
    deployment["practitioner_stats"] = practitioner_stats

    # 实战派达标检查
    quota_check = registry.check_practitioner_quota()
    deployment["practitioner_quota_check"] = quota_check

    # 5. 保存JSON
    output_path = os.path.join(project_root, "docs", "v4_deployment_data.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(deployment, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n[5/5] 部署数据已保存: {output_path}")

    # 额外：按部门统计分配情况
    print(f"\n{'=' * 70}")
    print(f"V4 任命部署统计摘要")
    print(f"{'=' * 70}")
    print(f"覆盖率: {deployment['summary']['coverage_pct']}%")
    print(f"\n按部门分配:")
    if assign_result.get('by_department'):
        for dept, count in sorted(assign_result['by_department'].items(), key=lambda x: -x[1]):
            print(f"  {dept}: {count} 人")

    print(f"\n按爵位分配:")
    if assign_result.get('by_nobility'):
        for n, count in assign_result['by_nobility'].items():
            print(f"  {n}: {count} 人")

    print(f"\n按品秩分配:")
    if assign_result.get('by_pin'):
        for pin, count in sorted(assign_result['by_pin'].items()):
            print(f"  {pin}: {count} 人")

    print(f"\n实战派达标检查:")
    for sys_name, check in quota_check.items():
        if check['status'] == 'skip':
            print(f"  {sys_name}: 跳过（无要求）")
        else:
            status = "达标" if check['status'] == 'pass' else "未达标"
            print(f"  {sys_name}: 实战派={check['practitioner']}, 复合型={check['dual_type']}, "
                  f"有效={check['effective']}, 要求>={check['quota']} [{status}]")

    return deployment


if __name__ == "__main__":
    main()
