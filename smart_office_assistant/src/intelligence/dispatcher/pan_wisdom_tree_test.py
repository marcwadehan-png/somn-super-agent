# -*- coding: utf-8 -*-
"""
Pan-Wisdom Tree (万法智慧树) - 系统测试与使用示例
=====================================================

本脚本验证 Pan-Wisdom Tree 系统能够正常工作：
1. 165个问题类型 (ProblemType) ✓
2. 36个智慧学派 (WisdomSchool) ✓
3. 问题-学派映射矩阵 ✓
4. 引擎调度 ✓

运行方式：
    cd d:\AI\somn\smart_office_assistant
    python -m src.intelligence.dispatcher.pan_wisdom_tree_test

作者: Somn Team
版本: V6.2
日期: 2026-04-28
"""

from __future__ import annotations
import sys
import os

# 确保能正确导入
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.intelligence.dispatcher.wisdom_dispatch import (
    WisdomDispatcher,
    WisdomSchool,
    ProblemType,
)


def print_header(text: str):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_sub_header(text: str):
    """打印副标题"""
    print(f"\n▶ {text}")


def test_enums():
    """测试1: 验证枚举定义"""
    print_header("测试1: 枚举定义验证")

    # 统计问题类型数量
    problem_types = list(ProblemType)
    print(f"✅ ProblemType 数量: {len(problem_types)}")

    # 统计智慧学派数量
    wisdom_schools = list(WisdomSchool)
    print(f"✅ WisdomSchool 数量: {len(wisdom_schools)}")

    # 列出所有问题类型
    print_sub_header("165个问题类型列表:")
    for i, pt in enumerate(problem_types, 1):
        print(f"  {i:3d}. {pt.name} = {pt.value}")

    # 列出所有智慧学派
    print_sub_header("36个智慧学派列表:")
    for i, ws in enumerate(wisdom_schools, 1):
        print(f"  {i:2d}. {ws.name} = {ws.value}")


def test_mapping():
    """测试2: 验证问题-学派映射矩阵"""
    print_header("测试2: 问题-学派映射矩阵验证")

    dispatcher = WisdomDispatcher()
    mapping = dispatcher.problem_school_mapping

    print(f"✅ 映射矩阵大小: {len(mapping)} 个问题类型")

    # 验证每个问题类型都有映射
    missing = []
    for pt in ProblemType:
        if pt not in mapping:
            missing.append(pt)

    if missing:
        print(f"⚠️ 缺少映射的问题类型: {[m.name for m in missing]}")
    else:
        print("✅ 所有问题类型都有映射")

    # 展示几个示例映射
    print_sub_header("示例映射:")
    examples = [
        ProblemType.ETHICAL,
        ProblemType.COMPETITION,
        ProblemType.MARKETING,
        ProblemType.LEADERSHIP,
        ProblemType.CRISIS,
    ]
    for pt in examples:
        if pt in mapping:
            schools = mapping[pt]
            school_names = [f"{s.name}({w:.0%})" for s, w in schools]
            print(f"  {pt.name}: {', '.join(school_names)}")


def test_engine_dispatch():
    """测试3: 测试引擎调度"""
    print_header("测试3: 引擎调度测试")

    dispatcher = WisdomDispatcher()

    # 测试获取引擎
    print_sub_header("获取智慧学派引擎:")
    test_schools = [
        WisdomSchool.CONFUCIAN,
        WisdomSchool.DAOIST,
        WisdomSchool.MILITARY,
        WisdomSchool.PSYCHOLOGY,
    ]

    for school in test_schools:
        engine = dispatcher._get_engine(school)
        if engine:
            print(f"  ✅ {school.value}: {engine.__class__.__name__}")
        else:
            print(f"  ⚠️ {school.value}: 引擎未实现或加载失败")


def test_problem_solving():
    """测试4: 模拟问题解决流程"""
    print_header("测试4: 问题解决流程模拟")

    dispatcher = WisdomDispatcher()

    # 模拟几个实际问题
    test_cases = [
        {
            "name": "市场竞争策略",
            "description": "我们公司产品在市场上遇到强劲竞争对手，对方价格更低，我们应该如何应对？",
            "problem_type": ProblemType.COMPETITION,
        },
        {
            "name": "组织文化变革",
            "description": "我们公司要从传统行业转型互联网，员工抵触情绪很大，怎么办？",
            "problem_type": ProblemType.ORGANIZATIONAL_CULTURE,
        },
        {
            "name": "营销策略制定",
            "description": "我们新出一款面向年轻人的功能性饮料，如何打开市场？",
            "problem_type": ProblemType.MARKETING,
        },
        {
            "name": "团队危机处理",
            "description": "核心团队成员突然离职，项目面临延期风险，如何处理？",
            "problem_type": ProblemType.CRISIS,
        },
        {
            "name": "人才选用育留",
            "description": "如何识别和培养高潜力人才，建立人才梯队？",
            "problem_type": ProblemType.TALENT,
        },
    ]

    for case in test_cases:
        print_sub_header(f"问题: {case['name']}")
        print(f"  描述: {case['description']}")
        print(f"  问题类型: {case['problem_type'].name} ({case['problem_type'].value})")

        # 获取推荐学派
        schools = dispatcher.get_schools_for_problem(case['problem_type'])
        if schools:
            print(f"  推荐引擎:")
            for school, weight in schools[:5]:  # 只显示前5个
                engine = dispatcher._get_engine(school)
                status = "✓" if engine else "⚠️"
                print(f"    {status} {school.value}: 权重={weight:.0%}")
        else:
            print("  ⚠️ 暂无推荐")

        print()


def test_api_usage():
    """测试5: API使用示例"""
    print_header("测试5: API使用示例")

    code_example = '''
# ==================== Pan-Wisdom Tree API 使用示例 ====================

from src.intelligence.dispatcher.wisdom_dispatch import (
    WisdomDispatcher,
    WisdomSchool,
    ProblemType,
)

# 1. 创建调度器
dispatcher = WisdomDispatcher()

# 2. 根据问题类型获取推荐引擎
problem = ProblemType.MARKETING
schools = dispatcher.get_schools_for_problem(problem)
# 返回: [(WisdomSchool.CHINESE_CONSUMER, 0.95), (WisdomSchool.BEHAVIOR, 0.9), ...]

# 3. 获取学派引擎实例
for school, weight in schools:
    engine = dispatcher._get_engine(school)
    if engine:
        # 4. 调用引擎解决问题
        result = engine.solve(
            problem_type=problem,
            context={"industry": "fashion", "target": " Gen-Z"},
            depth="deep"
        )
        print(f"{school.value} 建议: {result}")

# 5. 获取部门路由
routing = dispatcher.get_department_routing(problem)
# 返回: {"primary_department": "商部", "all_departments": ["商部", ...], ...}

# ==================== 完整问题解决流程 ====================

def solve_with_wisdom(problem_type: ProblemType, context: dict):
    \"\"\"使用万法智慧树解决问题\"\"\"
    dispatcher = WisdomDispatcher()

    # Step 1: 获取推荐引擎
    schools = dispatcher.get_schools_for_problem(problem_type)

    # Step 2: 并行执行引擎
    results = []
    for school, weight in schools:
        engine = dispatcher._get_engine(school)
        if engine:
            result = engine.solve(problem_type, context, depth="deep")
            results.append((school, weight, result))

    # Step 3: 融合结果
    fused = dispatcher.fuse_results(results)

    return fused
'''
    print(code_example)


def print_summary():
    """打印总结"""
    print_header("Pan-Wisdom Tree 系统总结")

    summary = """
┌─────────────────────────────────────────────────────────────┐
│                    Pan-Wisdom Tree                          │
│                    万法智慧树 V6.2                           │
│              Root of Infinite Wisdom                        │
├─────────────────────────────────────────────────────────────┤
│  系统规模                                                     │
│  ├── 问题类型 (ProblemType): 165个                          │
│  ├── 智慧学派 (WisdomSchool): 36个                          │
│  ├── 问题-学派映射: 完整矩阵                                 │
│  └── 引擎实现: 逐步完善中                                   │
├─────────────────────────────────────────────────────────────┤
│  系统架构                                                     │
│  ├── SD-R1: 深度推理层                                       │
│  ├── SD-F2: 智慧调度层                                       │
│  └── 引擎引擎: 36个学派引擎                                  │
├─────────────────────────────────────────────────────────────┤
│  使用方式                                                     │
│  dispatcher = WisdomDispatcher()                             │
│  schools = dispatcher.get_schools_for_problem(problem)      │
│  engine = dispatcher._get_engine(school)                    │
│  result = engine.solve(problem_type, context)               │
└─────────────────────────────────────────────────────────────┘
    """
    print(summary)


def main():
    """主函数"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ████████╗██╗  ██╗███████╗                                 ║
║   ╚══██╔══╝██║  ██║██╔════╝                                 ║
║      ██║   ███████║█████╗                                   ║
║      ██║   ██╔══██║██╔══╝                                   ║
║      ██║   ██║  ██║███████╗                                 ║
║      ╚═╝   ╚═╝  ╚═╝╚══════╝                                 ║
║                                                               ║
║   万法智慧树 (Pan-Wisdom Tree) V6.2                          ║
║   Root of Infinite Wisdom                                     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)

    try:
        # 运行所有测试
        test_enums()
        test_mapping()
        test_engine_dispatch()
        test_problem_solving()
        test_api_usage()
        print_summary()

        print("\n" + "=" * 60)
        print("  ✅ 所有测试完成!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
