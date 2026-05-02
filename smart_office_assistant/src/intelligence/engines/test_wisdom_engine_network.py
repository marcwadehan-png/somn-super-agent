# -*- coding: utf-8 -*-
"""
WisdomEngine 166引擎网络测试套件
================================

测试 Somn 系统的 166 个智慧引擎节点是否正确集成到 DivineReason。

版本: V2.0.0
创建: 2026-04-28
"""

import sys
import os

# 添加 src 目录到路径
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, src_path)

from intelligence.engines._wisdom_engine_nodes import (
    EngineType,
    WisdomEngineNode,
    WisdomEngineRegistry,
    WisdomEngineNetwork,
    get_wisdom_engine_network,
)


def test_registry_creation():
    """测试注册表创建"""
    print("\n" + "="*60)
    print("测试1: 智慧引擎注册表创建")
    print("="*60)
    
    registry = WisdomEngineRegistry()
    stats = registry.get_network_stats()
    
    print(f"\n✅ 注册表创建成功!")
    print(f"   总节点数: {stats['total_nodes']}")
    print(f"   学派引擎: {stats['school_nodes']} 个")
    print(f"   问题引擎: {stats['problem_type_nodes']} 个")
    print(f"   高优先级学派: {stats['schools_by_priority']['high']} 个")
    print(f"   互补链接: {stats['total_complementary_links']} 对")
    print(f"   相关链接: {stats['total_related_links']} 对")
    
    assert stats['school_nodes'] == 42, f"期望42个学派引擎，实际{stats['school_nodes']}"
    print("\n✅ 断言通过: 42个智慧学派引擎")
    
    return True


def test_school_nodes():
    """测试学派引擎节点"""
    print("\n" + "="*60)
    print("测试2: 学派引擎节点验证")
    print("="*60)
    
    registry = WisdomEngineRegistry()
    
    # 核心学派
    core_schools = ["CONFUCIAN", "DAOIST", "BUDDHIST", "MILITARY", "FAJIA", "ECONOMICS"]
    
    print("\n核心学派节点:")
    for school in core_schools:
        node = registry.get_school_node(school)
        if node:
            print(f"  ✅ {node.name}: {node.description[:40]}...")
            print(f"     关键词: {', '.join(node.keywords[:3])}")
            print(f"     优先级: {node.load_priority}")
    
    return True


def test_problem_nodes():
    """测试问题类型引擎节点"""
    print("\n" + "="*60)
    print("测试3: 问题类型引擎节点验证")
    print("="*60)
    
    registry = WisdomEngineRegistry()
    stats = registry.get_network_stats()
    
    print(f"\n问题类型引擎: {stats['problem_type_nodes']} 个")
    
    # 示例问题类型
    sample_problems = ["STRATEGY", "CRISIS", "COMPETITION", "GROWTH_MINDSET"]
    
    print("\n示例问题类型节点:")
    for problem in sample_problems:
        node = registry.get_problem_node(problem)
        if node:
            print(f"  ✅ {node.node_id}:")
            print(f"     关键词: {', '.join(node.keywords[:3])}")
            print(f"     所属学派: {node.school}")
    
    return True


def test_node_search():
    """测试节点搜索"""
    print("\n" + "="*60)
    print("测试4: 引擎节点搜索")
    print("="*60)
    
    registry = WisdomEngineRegistry()
    
    test_queries = [
        "战略规划",
        "危机处理",
        "团队管理",
        "市场竞争",
    ]
    
    for query in test_queries:
        results = registry.search_nodes(query, top_k=3)
        print(f"\n查询: '{query}'")
        for node, score in results:
            print(f"  📍 {node.name} (相关度: {score:.2f})")
    
    return True


def test_engine_network_solve():
    """测试引擎网络求解"""
    print("\n" + "="*60)
    print("测试5: 引擎网络求解")
    print("="*60)
    
    network = get_wisdom_engine_network()
    
    test_queries = [
        "如何制定企业战略规划?",
        "遇到危机如何处理?",
        "团队如何提升凝聚力?",
    ]
    
    for query in test_queries:
        print(f"\n🔍 问题: {query}")
        result = network.solve(query)
        
        if result["success"]:
            print(f"   ✅ 使用 {result['engines_used']} 个引擎")
            print(f"   📊 网络节点总数: {result['total_nodes']}")
            
            # 显示引擎路径
            for engine in result["engine_path"][:3]:
                print(f"   🚀 {engine['engine_name']} (相关度: {engine['relevance_score']:.2f})")
            
            # 显示洞察
            if result["insights"]:
                print(f"   💡 {result['insights'][0][:60]}...")
        else:
            print(f"   ❌ {result.get('error', '未知错误')}")
    
    return True


def test_engine_tree():
    """测试引擎树结构"""
    print("\n" + "="*60)
    print("测试6: 引擎树结构")
    print("="*60)
    
    registry = WisdomEngineRegistry()
    tree = registry.get_engine_tree()
    
    print(f"\n🌳 {tree['name']}")
    print(f"   总计: {tree['total_count']} 个引擎节点\n")
    
    for category in tree["children"]:
        print(f"📂 {category['name']} ({len(category['children'])} 学派)")
        for school in category["children"][:2]:
            print(f"   ├── {school['name']} ({school['count']} 引擎)")
        if len(category["children"]) > 2:
            print(f"   └── ... 等 {len(category['children'])-2} 更多")


def test_singleton():
    """测试单例模式"""
    print("\n" + "="*60)
    print("测试7: 单例模式验证")
    print("="*60)
    
    network1 = get_wisdom_engine_network()
    network2 = get_wisdom_engine_network()
    
    print(f"\n单例验证:")
    print(f"   network1 id: {id(network1)}")
    print(f"   network2 id: {id(network2)}")
    print(f"   相同实例: {network1 is network2}")
    
    assert network1 is network2, "单例模式失败!"
    print("\n✅ 单例模式验证通过")


def main():
    """主测试函数"""
    print("\n" + "🎯"*30)
    print("WisdomEngine 166引擎网络测试套件")
    print("="*60)
    print(f"测试 Somn 系统的 166 个智慧引擎 (42学派 + 问题类型)")
    print("🎯"*30)
    
    tests = [
        ("注册表创建", test_registry_creation),
        ("学派节点", test_school_nodes),
        ("问题节点", test_problem_nodes),
        ("节点搜索", test_node_search),
        ("引擎求解", test_engine_network_solve),
        ("引擎树", test_engine_tree),
        ("单例模式", test_singleton),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"\n❌ 测试失败: {name}")
            print(f"   错误: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"📊 测试结果: {passed} 通过, {failed} 失败")
    print("="*60)
    
    if failed == 0:
        print("\n🎉 所有测试通过! WisdomEngine 166引擎网络已就绪!")
    else:
        print(f"\n⚠️  {failed} 个测试失败，请检查错误信息。")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
