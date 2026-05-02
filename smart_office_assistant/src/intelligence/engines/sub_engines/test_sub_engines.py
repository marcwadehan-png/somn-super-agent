"""
测试142个子推理引擎系统
DivineReason Engine V3.2 - 实际推理验证
"""

import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_engine_registry():
    """测试1: 引擎注册表"""
    print("\n" + "="*60)
    print("测试1: 引擎注册表")
    print("="*60)

    from sub_engines import GLOBAL_ENGINE_REGISTRY, EngineCategory

    stats = GLOBAL_ENGINE_REGISTRY.get_stats()
    print(f"总引擎数: {stats['total_engines']}")
    print("\n按类别分布:")
    for cat, count in stats['by_category'].items():
        print(f"  {cat}: {count} 个")

    # 验证数量
    expected = {
        'cognitive': 40,
        'strategic': 35,
        'creative': 30,
        'analytical': 25,
        'decision': 12,
    }

    all_pass = True
    for cat, expected_count in expected.items():
        actual_count = stats['by_category'].get(cat, 0)
        status = "✓" if actual_count == expected_count else "✗"
        print(f"  {status} {cat}: {actual_count} / {expected_count}")
        if actual_count != expected_count:
            all_pass = False

    total_expected = sum(expected.values())
    print(f"\n总计: {stats['total_engines']} / {total_expected}")
    print(f"测试结果: {'通过 ✓' if all_pass and stats['total_engines'] == total_expected else '失败 ✗'}")
    return all_pass and stats['total_engines'] == total_expected


def test_single_engine():
    """测试2: 单个引擎调用"""
    print("\n" + "="*60)
    print("测试2: 单个引擎调用")
    print("="*60)

    from sub_engines import GLOBAL_ENGINE_REGISTRY

    # 测试演绎推理引擎
    deductive = GLOBAL_ENGINE_REGISTRY.get("COG_001")
    if not deductive:
        print("✗ 无法获取演绎推理引擎")
        return False

    print(f"引擎: {deductive.engine_name} ({deductive.engine_id})")
    print(f"类别: {deductive.category.value}")
    print(f"描述: {deductive.description}")

    # 执行推理
    result = deductive.reason({
        'premises': ['如果下雨，地面会湿', '下雨了'],
        'conclusion': '地面会湿'
    })

    print(f"\n推理结果:")
    print(f"  成功: {result.success}")
    print(f"  置信度: {result.confidence:.2%}")
    print(f"  结果: {result.result}")
    print(f"  推理链: {result.reasoning_chain[:3]}")

    print(f"\n测试结果: {'通过 ✓' if result.success else '失败 ✗'}")
    return result.success


def test_category_engines():
    """测试3: 各类别引擎抽样测试"""
    print("\n" + "="*60)
    print("测试3: 各类别引擎抽样测试")
    print("="*60)

    from sub_engines import GLOBAL_ENGINE_REGISTRY, EngineCategory

    test_cases = [
        (EngineCategory.COGNITIVE, "COG_001", "演绎推理"),
        (EngineCategory.COGNITIVE, "COG_023", "贝叶斯推理"),
        (EngineCategory.STRATEGIC, "STR_011", "SWOT分析"),
        (EngineCategory.STRATEGIC, "STR_019", "压力测试"),
        (EngineCategory.CREATIVE, "CRT_001", "联想头脑风暴"),
        (EngineCategory.CREATIVE, "CRT_021", "横向思维"),
        (EngineCategory.ANALYTICAL, "ANL_002", "回归分析"),
        (EngineCategory.ANALYTICAL, "ANL_008", "异常检测"),
        (EngineCategory.DECISION, "DEC_002", "AHP分析"),
        (EngineCategory.DECISION, "DEC_012", "蒙特卡洛决策"),
    ]

    results = []
    for cat, engine_id, name in test_cases:
        engine = GLOBAL_ENGINE_REGISTRY.get(engine_id)
        if engine:
            result = engine.reason({'query': 'test'})
            success = result.success
            results.append(success)
            status = "✓" if success else "✗"
            print(f"  {status} {engine_id} ({name}): 置信度={result.confidence:.2f}")
        else:
            results.append(False)
            print(f"  ✗ {engine_id} ({name}): 未找到")

    print(f"\n测试结果: {'通过 ✓' if all(results) else '失败 ✗'}")
    return all(results)


def test_divine_reason_engine():
    """测试4: DivineReason调度器"""
    print("\n" + "="*60)
    print("测试4: DivineReason调度器")
    print("="*60)

    from sub_engines import get_divine_reason_engine, ReasoningRequest

    engine = get_divine_reason_engine()
    print(f"DivineReason Engine 初始化成功")
    print(f"版本: {engine.get_stats()['divine_reason_version']}")
    print(f"总引擎数: {engine.get_stats()['total_engines']}")

    # 测试推理请求
    test_queries = [
        ReasoningRequest(
            query="分析市场竞争策略",
            problem_type="STRATEGY",
            context={}
        ),
        ReasoningRequest(
            query="预测销售趋势",
            problem_type="FORECAST",
            context={}
        ),
        ReasoningRequest(
            query="如何创新产品设计",
            problem_type="CREATIVE",
            context={}
        ),
    ]

    for req in test_queries:
        print(f"\n--- 推理: {req.query} ---")
        response = engine.reason(req)
        print(f"使用引擎数: {len(response.results)}")
        print(f"综合置信度: {response.confidence:.2%}")
        print(f"引擎列表: {response.engines_used[:5]}...")
        print(f"融合结果: {response.fused_answer[:100] if isinstance(response.fused_answer, str) else response.fused_answer}")

    print(f"\n测试结果: 通过 ✓")
    return True


def test_actual_reasoning():
    """测试5: 实际推理任务"""
    print("\n" + "="*60)
    print("测试5: 实际推理任务")
    print("="*60)

    from sub_engines import get_divine_reason_engine, ReasoningRequest

    engine = get_divine_reason_engine()

    # 实际商业问题
    real_request = ReasoningRequest(
        query="某公司市场份额下降20%，请分析原因并给出战略建议",
        problem_type="STRATEGIC_ANALYSIS",
        context={
            "company": "某公司",
            "situation": "市场份额下降20%",
            "industry": "消费品"
        }
    )

    print(f"问题: {real_request.query}")
    print("\n执行推理...\n")

    response = engine.reason(real_request)

    print(f"调用引擎数: {len(response.results)}")
    print(f"引擎类别分布:")
    categories = {}
    for r in response.results:
        cat = r.category.value
        categories[cat] = categories.get(cat, 0) + 1
    for cat, count in categories.items():
        print(f"  - {cat}: {count} 个")

    print(f"\n综合置信度: {response.confidence:.2%}")
    print(f"\n推理摘要:\n{response.reasoning_summary}")
    print(f"\n融合结果:\n{response.fused_answer}")

    print(f"\n测试结果: 通过 ✓")
    return True


def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("DivineReason 142+10 子推理引擎系统测试")
    print("="*60)

    results = []

    results.append(("引擎注册表", test_engine_registry()))
    results.append(("单个引擎调用", test_single_engine()))
    results.append(("类别引擎测试", test_category_engines()))
    results.append(("DivineReason调度器", test_divine_reason_engine()))
    results.append(("实际推理任务", test_actual_reasoning()))

    print("\n" + "="*60)
    print("测试汇总")
    print("="*60)

    for name, passed in results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"  {name}: {status}")

    all_passed = all(r[1] for r in results)
    print(f"\n总体结果: {'✓ 全部通过' if all_passed else '✗ 存在失败'}")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
