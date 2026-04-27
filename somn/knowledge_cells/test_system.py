#!/usr/bin/env python3
"""
知识格子系统测试
================
测试knowledge_cells模块的完整功能
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from knowledge_cells import get_knowledge_system, query, check, get_status


def test_engine():
    """测试引擎加载"""
    print("\n" + "="*50)
    print("测试1: 知识格子引擎加载")
    print("="*50)
    
    system = get_knowledge_system()
    status = system.get_status()
    
    print(f"✓ 总格子数: {status['total_cells']}")
    print(f"✓ 最热格子: {[c['name'] for c in status['hot_cells'][:3]]}")
    
    return status['total_cells'] > 0


def test_cell_retrieval():
    """测试格子检索"""
    print("\n" + "="*50)
    print("测试2: 格子检索")
    print("="*50)
    
    system = get_knowledge_system()
    
    # 获取A1格子
    cell = system.get_cell_content("A1")
    if cell:
        print(f"✓ A1格子: {cell['name']}")
        print(f"  标签: {cell['tags']}")
        print(f"  激活次数: {cell['activation_count']}")
    else:
        print("✗ A1格子加载失败")
    
    # 获取关联格子
    related = system.get_related_cells("A1")
    print(f"✓ A1关联格子: {[r['name'] for r in related[:3]]}")
    
    return cell is not None


def test_search():
    """测试搜索"""
    print("\n" + "="*50)
    print("测试3: 关键词搜索")
    print("="*50)
    
    system = get_knowledge_system()
    
    # 搜索"裂变"
    results = system.search_cells("裂变")
    print(f"搜索'裂变': {[r['name'] for r in results]}")
    
    # 搜索"直播"
    results = system.search_cells("直播")
    print(f"搜索'直播': {[r['name'] for r in results]}")
    
    return True


def test_query():
    """测试知识查询"""
    print("\n" + "="*50)
    print("测试4: 知识查询")
    print("="*50)
    
    result = query("如何提升用户增长")
    
    print(f"✓ 质量分数: {result['quality_score']}")
    print(f"✓ 使用格子: {result['cells_used']}")
    print(f"✓ 推荐框架: {result['frameworks']}")
    print(f"✓ 举一反三: {result['analogies'][:1] if result['analogies'] else '无'}")
    
    return result['cells_used'] and len(result['cells_used']) > 0


def test_methodology_check():
    """测试方法论检查"""
    print("\n" + "="*50)
    print("测试5: 方法论检查")
    print("="*50)
    
    # 好的回答
    good_answer = """
    【问题诊断】
    当前用户增长主要面临获客成本高、留存率低的问题。

    【数据支撑】
    - CAC(获客成本)为80元，高于行业平均60元
    - 次日留存率35%，低于目标50%

    【框架建议】
    采用AARRR模型进行分析优化

    【举一反三】
    用户增长就像经营线下门店，需要同时关注进店率(获客)和复购率(留存)
    """
    
    check_result = check(good_answer)
    
    print(f"✓ 整体分数: {check_result['overall_score']}")
    print(f"✓ 评估等级: {check_result['level']}")
    print(f"✓ 各维度: 诊断={check_result['dimensions']['diagnosis']['score']}, "
          f"框架={check_result['dimensions']['framework']['score']}, "
          f"数据={check_result['dimensions']['data']['score']}, "
          f"逻辑={check_result['dimensions']['logic']['score']}, "
          f"类比={check_result['dimensions']['analogy']['score']}")
    
    return True


def test_knowledge_graph():
    """测试知识图谱"""
    print("\n" + "="*50)
    print("测试6: 知识图谱")
    print("="*50)
    
    system = get_knowledge_system()
    graph = system.get_knowledge_graph()
    
    print(f"✓ 节点数: {len(graph['nodes'])}")
    print(f"✓ 边数: {len(graph['links'])}")
    
    # 统计分类
    core_nodes = [n for n in graph['nodes'] if n['category'] == 'core']
    domain_nodes = [n for n in graph['nodes'] if n['category'] == 'domain']
    print(f"✓ 核心格子: {len(core_nodes)}")
    print(f"✓ 知识域: {len(domain_nodes)}")
    
    return len(graph['nodes']) > 0


def run_all_tests():
    """运行所有测试"""
    print("\n" + "█"*60)
    print("  知识格子系统 v1.1 - 完整测试")
    print("█"*60)
    
    results = []
    
    results.append(("引擎加载", test_engine()))
    results.append(("格子检索", test_cell_retrieval()))
    results.append(("关键词搜索", test_search()))
    results.append(("知识查询", test_query()))
    results.append(("方法论检查", test_methodology_check()))
    results.append(("知识图谱", test_knowledge_graph()))
    
    print("\n" + "="*50)
    print("测试结果汇总")
    print("="*50)
    
    passed = 0
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{len(results)} 测试通过")
    
    return passed == len(results)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
