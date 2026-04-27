# -*- coding: utf-8 -*-
"""
Somn主线调用链路验证脚本
======================

验证核心模块的调用链路是否完整可用。
"""

import sys
sys.path.insert(0, '.')

print("=" * 60)
print("Somn主线调用链路验证")
print("=" * 60)

# 1. 验证somn主入口
print("\n[1] somn.py 主入口")
try:
    from smart_office_assistant.src.somn import Somn
    somn = Somn()
    print("  ✅ Somn() 初始化成功 (v19.0延迟加载)")
    print(f"  ✅ 版本: {somn.__doc__.split(chr(10))[2] if somn.__doc__ else 'N/A'}")
except Exception as e:
    print(f"  ❌ Somn初始化失败: {e}")

# 2. 验证WisdomDispatcher
print("\n[2] WisdomDispatcher 调度器")
try:
    from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch import WisdomDispatcher
    wd = WisdomDispatcher()
    print(f"  ✅ WisdomDispatcher 初始化成功")
    print(f"  ✅ ProblemType映射: {len(wd.problem_school_mapping)} 个")
    
    # 测试推荐功能
    from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums import ProblemType
    recs = wd.recommend_schools(ProblemType.GROWTH_PLAN)
    print(f"  ✅ recommend_schools(GROWTH_PLAN): {len(recs)} 个学派")
except Exception as e:
    print(f"  ❌ WisdomDispatcher失败: {e}")

# 3. 验证GlobalClawScheduler
print("\n[3] GlobalClawScheduler 全局Claw调度")
try:
    from smart_office_assistant.src.intelligence.claws._global_claw_scheduler import GlobalClawScheduler
    gcs = GlobalClawScheduler()
    print(f"  ✅ GlobalClawScheduler 初始化成功")
    print(f"  ✅ Claw总数: {len(gcs.claws)}")
    print(f"  ✅ 岗位总数: {len(gcs.position_registry)}")
except Exception as e:
    print(f"  ❌ GlobalClawScheduler失败: {e}")

# 4. 验证藏书阁V3.0
print("\n[4] ImperialLibrary 藏书阁V3.0")
try:
    from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch import get_imperial_library
    lib = get_imperial_library()
    print(f"  ✅ ImperialLibrary 初始化成功")
    stats = lib.get_stats()
    print(f"  ✅ 统计: {stats}")
except Exception as e:
    print(f"  ❌ ImperialLibrary失败: {e}")

# 5. 验证wisdom_encoding_registry
print("\n[5] WisdomEncodingRegistry 智慧编码")
try:
    from smart_office_assistant.src.intelligence.wisdom_encoding.wisdom_encoding_registry import WisdomEncodingRegistry
    reg = WisdomEncodingRegistry(lazy=True)
    data = reg.export_data()
    print(f"  ✅ WisdomEncodingRegistry 初始化成功")
    print(f"  ✅ 编码数量: {data.get('total_sages', 0)}")
except Exception as e:
    print(f"  ❌ WisdomEncodingRegistry失败: {e}")

# 6. 验证_solutions模块
print("\n[6] _solutions.py 解决方案模块")
try:
    from smart_office_assistant.src.somn_legacy._solutions import (
        get_solution_recommendations,
        assess_solution_v2,
        get_solution_details,
        list_all_solutions
    )
    print("  ✅ 解决方案函数全部可导入:")
    print("     - get_solution_recommendations")
    print("     - assess_solution_v2")
    print("     - get_solution_details")
    print("     - list_all_solutions")
except Exception as e:
    print(f"  ❌ _solutions模块失败: {e}")

# 7. 验证_analysis模块
print("\n[7] _analysis.py 分析模块")
try:
    from smart_office_assistant.src.somn_legacy._analysis import (
        analyze,
        generate_growth_plan,
        analyze_demand,
        analyze_funnel,
        map_user_journey,
        diagnose_business,
        narrative_analysis
    )
    print("  ✅ 分析函数全部可导入:")
    print("     - analyze")
    print("     - generate_growth_plan")
    print("     - analyze_demand")
    print("     - analyze_funnel")
    print("     - map_user_journey")
    print("     - diagnose_business")
    print("     - narrative_analysis")
except Exception as e:
    print(f"  ❌ _analysis模块失败: {e}")

# 总结
print("\n" + "=" * 60)
print("验证完成")
print("=" * 60)
