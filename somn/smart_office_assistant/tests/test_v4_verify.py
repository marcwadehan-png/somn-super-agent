# -*- coding: utf-8 -*-
"""神之架构V4.0.0 升级验证脚本"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_enums():
    """测试枚举定义"""
    from src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums import WisdomSchool, ProblemType
    ws_count = len(WisdomSchool)
    pt_count = len(ProblemType)
    print(f"[ENUMS] WisdomSchool: {ws_count}, ProblemType: {pt_count}")
    return ws_count, pt_count

def test_positions():
    """测试岗位体系"""
    from src.intelligence.engines.cloning._court_positions import CourtPositionRegistry
    reg = CourtPositionRegistry()
    stats = reg.get_stats()
    print(f"[POSITIONS] total: {stats['total_positions']}, departments: {stats['departments']}")
    print(f"[NOBILITY] {stats['by_nobility']}")
    return stats

def test_auto_assign():
    """测试自动任命"""
    from src.intelligence.engines.cloning._court_positions import CourtPositionRegistry
    from src.intelligence.engines.cloning._sage_registry_full import ALL_SAGES, get_registry_stats
    
    reg = CourtPositionRegistry()
    
    # 获取贤者列表
    sage_names = [s for s in ALL_SAGES if hasattr(s, 'name')] if ALL_SAGES else []
    print(f"[SAGES] Total in ALL_SAGES: {len(ALL_SAGES)}")
    
    try:
        reg_stats = get_registry_stats()
        print(f"[SAGES] Registry stats: {reg_stats}")
    except:
        pass
    
    # 执行自动任命
    result = reg.auto_assign_all_sages()
    
    assigned = result.get('assigned', 0)
    failed_list = result.get('failed', [])
    total = result.get('total', 0)
    
    if isinstance(failed_list, int):
        failed_count = failed_list
        failed_list = []
    else:
        failed_count = len(failed_list)
    
    print(f"[ASSIGN] Attempted: {total}, Assigned: {assigned}, Failed: {failed_count}")
    if failed_list:
        print(f"[ASSIGN] Failed sages (first 20): {failed_list[:20]}")
    
    # 获取任命后统计
    stats = reg.get_stats()
    coverage = stats.get('coverage_pct', 0)
    print(f"[ASSIGN] Coverage: {coverage}%")
    print(f"[ASSIGN] Total assigned: {stats.get('total_assigned_sages', 'N/A')}")
    
    return result, stats

def test_departments():
    """测试部门调度"""
    from src.intelligence.dispatcher.wisdom_dispatch._dispatch_court import Department, DEPARTMENT_SCHOOL_MATRIX
    dept_count = len(Department)
    matrix_count = len(DEPARTMENT_SCHOOL_MATRIX)
    print(f"[DEPARTMENTS] Count: {dept_count}, Matrix entries: {matrix_count}")
    return dept_count, matrix_count

def test_fusion_decision():
    """测试FusionDecision"""
    from src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums import FusionDecision
    print(f"[FUSION] FusionDecision v1.0.0 fields: {[f for f in FusionDecision.__dataclass_fields__.keys()]}")
    return True

def test_modules_load():
    """测试模块加载"""
    modules = [
        ('_court_positions', 'src.intelligence.engines.cloning._court_positions'),
        ('_dispatch_court', 'src.intelligence.dispatcher.wisdom_dispatch._dispatch_court'),
        ('_dispatch_enums', 'src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums'),
        ('_dispatch_mapping', 'src.intelligence.dispatcher.wisdom_dispatch._dispatch_mapping'),
        ('_hanlin_review', 'src.intelligence.dispatcher.wisdom_dispatch._hanlin_review'),
        ('_imperial_library', 'src.intelligence.dispatcher.wisdom_dispatch._imperial_library'),
        ('_decision_congress', 'src.intelligence.dispatcher.wisdom_dispatch._decision_congress'),
        ('_daqin_metrics', 'src.intelligence.dispatcher.wisdom_dispatch._daqin_metrics'),
        ('_whip_engine', 'src.intelligence.dispatcher.wisdom_dispatch._whip_engine'),
    ]
    results = []
    for name, path in modules:
        try:
            __import__(path, fromlist=[''])
            results.append(f"  [PASS] {name}")
        except Exception as e:
            results.append(f"  [FAIL] {name}: {str(e)[:100]}")
    print("[MODULES]")
    for r in results:
        print(r)
    return results

def main():
    print("=" * 60)
    print("  神之架构V4.0.0 升级验证报告")
    print("=" * 60)
    
    # 1. 模块加载
    print("\n--- 模块加载测试 ---")
    module_results = test_modules_load()
    pass_count = sum(1 for r in module_results if '[PASS]' in r)
    fail_count = sum(1 for r in module_results if '[FAIL]' in r)
    print(f"  结果: {pass_count}/{pass_count+fail_count} PASS")
    
    # 2. 枚举验证
    print("\n--- 枚举验证 ---")
    ws_count, pt_count = test_enums()
    
    # 3. 岗位验证
    print("\n--- 岗位体系验证 ---")
    pos_stats = test_positions()
    
    # 4. 部门验证
    print("\n--- 部门调度验证 ---")
    dept_count, matrix_count = test_departments()
    
    # 5. FusionDecision验证
    print("\n--- FusionDecision验证 ---")
    test_fusion_decision()
    
    # 6. 自动任命
    print("\n--- 自动任命验证 ---")
    assign_result, assign_stats = test_auto_assign()
    
    # 汇总
    print("\n" + "=" * 60)
    print("  验证汇总")
    print("=" * 60)
    checks = [
        ("模块加载", f"{pass_count}/{pass_count+fail_count}", pass_count == pass_count+fail_count),
        ("WisdomSchool", str(ws_count), ws_count == 25),
        ("ProblemType", str(pt_count), pt_count >= 75),
        ("岗位总数", str(pos_stats['total_positions']), pos_stats['total_positions'] == 364),
        ("爵位总数", str(pos_stats['noble_positions']), pos_stats['noble_positions'] == 25),
        ("部门数量", str(dept_count), dept_count == 11),
        ("路由矩阵", str(matrix_count), matrix_count >= 75),
        ("贤者任命", f"{assign_stats.get('coverage_pct', 0)}%", assign_stats.get('coverage_pct', 0) > 90),
    ]
    
    all_pass = True
    for name, value, ok in checks:
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_pass = False
        print(f"  [{status}] {name}: {value}")
    
    print(f"\n  总体结果: {'ALL PASS' if all_pass else 'HAS FAILURES'}")
    print("=" * 60)

if __name__ == "__main__":
    main()
