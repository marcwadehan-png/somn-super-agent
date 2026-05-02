# -*- coding: utf-8 -*-
"""
超级推理引擎测试
UnifiedReasoningEngine Test Suite

测试四大推理范式的整合：
1. GoT 图网络结构
2. LongCoT 长链推理
3. ToT 树状分支
4. ReAct 工具调用

作者: Somn AI
日期: 2026-04-28
"""

import sys
import json
import time
from typing import Dict, Any, List

# 添加项目路径
sys.path.insert(0, r'd:\AI\somn\smart_office_assistant\src')

from intelligence.reasoning._unified_reasoning_engine import (
    # 核心类
    UnifiedReasoningEngine,
    SuperGraph,
    
    # 配置
    UnifiedConfig,
    
    # 数据类
    UnifiedNode,
    UnifiedEdge,
    ReasoningMetadata,
    GraphStatistics,
    
    # 枚举
    NodeType,
    EdgeType,
    ReasoningMode,
    
    # 便捷函数
    create_super_engine,
    solve_with_super_engine,
)


def mock_llm(prompt: str) -> str:
    """模拟LLM调用"""
    if "生成" in prompt and "方向" in prompt:
        return """[方向1] 从数学角度分析，利用概率论和统计学原理...
[方向2] 从逻辑推理角度，考虑因果关系和充分必要条件...
[方向3] 从系统论角度，考虑各要素之间的相互作用..."""
    
    if "推理" in prompt or "分析" in prompt:
        return f"""首先，理解问题的本质：{prompt[:50]}...

经过深入分析，我发现关键在于：
1. 问题涉及多个要素的相互作用
2. 需要考虑边界条件和约束
3. 最终解应该是系统最优而非局部最优

因此，我得出结论：在综合考虑各种因素后，问题的解决方案应该从系统整体角度出发，平衡各方利益。"""
    
    return f"基于问题的深度分析，得出关键洞察：问题的核心在于系统性的思考和综合判断。"


class TestSuite:
    """测试套件"""
    
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
    
    def run_test(self, name: str, test_func):
        """运行测试"""
        print(f"\n{'='*60}")
        print(f"🧪 测试: {name}")
        print('='*60)
        
        try:
            result = test_func()
            if result.get('success', False):
                print(f"✅ 通过")
                self.passed += 1
                self.results.append({'name': name, 'status': 'PASS', 'result': result})
            else:
                print(f"❌ 失败: {result.get('error', 'Unknown')}")
                self.failed += 1
                self.results.append({'name': name, 'status': 'FAIL', 'result': result})
        except Exception as e:
            print(f"❌ 异常: {str(e)}")
            self.failed += 1
            self.results.append({'name': name, 'status': 'ERROR', 'error': str(e)})
    
    def summary(self):
        """测试总结"""
        print(f"\n{'='*60}")
        print(f"📊 测试总结")
        print('='*60)
        print(f"总计: {self.passed + self.failed}")
        print(f"通过: {self.passed} ✅")
        print(f"失败: {self.failed} ❌")
        print(f"成功率: {self.passed/(self.passed+self.failed)*100:.1f}%")


def test_super_graph_creation():
    """测试超级图创建"""
    print("\n测试超级图创建...")
    
    graph = SuperGraph("测试问题")
    assert graph.problem == "测试问题"
    assert len(graph.nodes) == 0
    
    # 创建根节点
    root = graph.create_root("问题：如何提高产品质量？")
    assert root is not None
    assert root.node_type == NodeType.ROOT
    assert root.node_id in graph.nodes
    
    print(f"  ✓ 根节点创建成功: {root.node_id[:8]}...")
    
    # 添加子节点
    child1 = graph.add_node(
        content="分析质量问题的关键因素",
        node_type=NodeType.LONG_COT_STEP,
        parent_ids=[root.node_id],
        depth=1,
        metadata=ReasoningMetadata(source_engine="long_cot")
    )
    
    assert child1.parent_ids == [root.node_id]
    assert len(graph.edges) == 1
    
    print(f"  ✓ 子节点添加成功: {child1.node_id[:8]}...")
    
    return {'success': True, 'graph': graph}


def test_node_types():
    """测试不同节点类型"""
    print("\n测试不同节点类型...")
    
    graph = SuperGraph("节点类型测试")
    root = graph.create_root("根节点")
    
    # LongCoT节点
    long_cot_node = graph.add_node(
        content="LongCoT推理步骤",
        node_type=NodeType.LONG_COT_STEP,
        parent_ids=[root.node_id],
        depth=1,
        is_checkpoint=True
    )
    assert long_cot_node.node_type == NodeType.LONG_COT_STEP
    assert long_cot_node.is_checkpoint == True
    print("  ✓ LongCoT节点创建成功")
    
    # ToT分支节点
    tot_node = graph.add_node(
        content="ToT分支选项",
        node_type=NodeType.TOT_BRANCH,
        parent_ids=[root.node_id],
        depth=1,
        feasibility_score=0.7,
        progress_score=0.6
    )
    assert tot_node.node_type == NodeType.TOT_BRANCH
    assert tot_node.feasibility_score == 0.7
    print("  ✓ ToT分支节点创建成功")
    
    # ReAct行动节点
    react_node = graph.add_node(
        content="ReAct工具调用",
        node_type=NodeType.REACT_ACTION,
        parent_ids=[root.node_id],
        depth=1,
        action={'tool': 'search', 'params': {'query': 'test'}}
    )
    assert react_node.node_type == NodeType.REACT_ACTION
    assert react_node.action is not None
    print("  ✓ ReAct行动节点创建成功")
    
    # 顿悟节点
    insight_node = graph.add_node(
        content="顿悟时刻：关键洞察",
        node_type=NodeType.INSIGHT,
        parent_ids=[root.node_id],
        depth=1,
        is_insight=True,
        insight_type="breakthrough",
        insight_impact=0.9
    )
    assert insight_node.is_insight == True
    assert insight_node.insight_type == "breakthrough"
    print("  ✓ 顿悟节点创建成功")
    
    return {'success': True, 'node_count': len(graph.nodes)}


def test_edge_types():
    """测试不同边类型"""
    print("\n测试不同边类型...")
    
    graph = SuperGraph("边类型测试")
    root = graph.create_root("根节点")
    
    # 逻辑流边
    node1 = graph.add_node(
        content="步骤1",
        node_type=NodeType.LONG_COT_STEP,
        parent_ids=[root.node_id],
        depth=1
    )
    edge1 = graph.add_edge(root.node_id, node1.node_id, EdgeType.LOGICAL_FLOW)
    assert edge1.edge_type == EdgeType.LOGICAL_FLOW
    print("  ✓ 逻辑流边创建成功")
    
    # 并行边
    node2 = graph.add_node(
        content="并行分支1",
        node_type=NodeType.TOT_BRANCH,
        parent_ids=[root.node_id],
        depth=1
    )
    edge2 = graph.add_edge(root.node_id, node2.node_id, EdgeType.PARALLEL)
    assert edge2.edge_type == EdgeType.PARALLEL
    print("  ✓ 并行边创建成功")
    
    # 反馈边
    node3 = graph.add_node(
        content="反馈检查",
        node_type=NodeType.CHECKPOINT,
        parent_ids=[node1.node_id],
        depth=2
    )
    edge3 = graph.add_edge(node3.node_id, node1.node_id, EdgeType.FEEDBACK)
    assert edge3.is_feedback_loop == True
    print("  ✓ 反馈边创建成功")
    
    # 回溯边
    edge4 = graph.add_edge(node3.node_id, root.node_id, EdgeType.BACKTRACK)
    assert edge4.is_backtrack == True
    print("  ✓ 回溯边创建成功")
    
    return {'success': True, 'edge_count': len(graph.edges)}


def test_unified_engine_linear():
    """测试线性模式(LongCoT风格)"""
    print("\n测试线性推理模式...")
    
    config = UnifiedConfig(
        default_mode=ReasoningMode.LINEAR,
        max_nodes=20,
        max_depth=5,
        checkpoint_interval=2
    )
    
    engine = create_super_engine(
        llm_callable=mock_llm,
        config=config
    )
    
    problem = "如何提高团队协作效率？"
    
    result = engine.solve(problem, mode=ReasoningMode.LINEAR)
    
    assert 'graph' in result
    assert 'solution' in result
    assert result['metadata']['mode'] == 'linear'
    
    graph = result['graph']
    print(f"  ✓ 推理图创建成功")
    print(f"  ✓ 节点数: {len(graph.nodes)}")
    print(f"  ✓ 边数: {len(graph.edges)}")
    print(f"  ✓ 顿悟时刻: {len(result['insights'])}")
    
    # 检查LongCoT特性
    checkpoints = graph.checkpoints
    print(f"  ✓ 检查点数量: {len(checkpoints)}")
    
    return {'success': True, 'result': result}


def test_unified_engine_branching():
    """测试分支模式(ToT风格)"""
    print("\n测试分支推理模式...")
    
    config = UnifiedConfig(
        default_mode=ReasoningMode.BRANCHING,
        max_nodes=30,
        max_branching=4
    )
    
    engine = create_super_engine(
        llm_callable=mock_llm,
        config=config
    )
    
    problem = "制定营销策略的三个方案"
    
    result = engine.solve(problem, mode=ReasoningMode.BRANCHING)
    
    graph = result['graph']
    
    # 检查ToT特性
    tot_nodes = [n for n in graph.nodes.values() if n.node_type == NodeType.TOT_BRANCH]
    print(f"  ✓ ToT分支节点数: {len(tot_nodes)}")
    
    # 检查多父节点
    multi_parent = [n for n in graph.nodes.values() if len(n.parent_ids) > 1]
    print(f"  ✓ 多分支汇聚节点数: {len(multi_parent)}")
    
    return {'success': True, 'result': result}


def test_unified_engine_reactive():
    """测试反应模式(ReAct风格)"""
    print("\n测试反应推理模式...")
    
    config = UnifiedConfig(
        default_mode=ReasoningMode.REACTIVE,
        max_nodes=15,
        enable_react=True
    )
    
    # 模拟工具
    class MockTool:
        name = "search"
        description = "搜索工具"
        
        def execute(self, query):
            return {"results": [f"关于'{query}'的搜索结果"]}
    
    class MockCalculator:
        name = "calculate"
        description = "计算工具"
        
        def execute(self, expression):
            return {"result": 42}
    
    engine = create_super_engine(
        llm_callable=mock_llm,
        config=config,
        tools=[MockTool(), MockCalculator()]
    )
    
    problem = "搜索2024年AI发展趋势并计算增长率"
    
    result = engine.solve(problem, mode=ReasoningMode.REACTIVE)
    
    graph = result['graph']
    
    # 检查ReAct特性
    action_nodes = [n for n in graph.nodes.values() if n.node_type == NodeType.REACT_ACTION]
    observation_nodes = [n for n in graph.nodes.values() if n.node_type == NodeType.OBSERVATION]
    
    print(f"  ✓ 行动节点数: {len(action_nodes)}")
    print(f"  ✓ 观察节点数: {len(observation_nodes)}")
    
    return {'success': True, 'result': result}


def test_unified_engine_super():
    """测试超级模式(全部引擎)"""
    print("\n测试超级推理模式...")
    
    config = UnifiedConfig(
        default_mode=ReasoningMode.SUPER,
        max_nodes=50,
        max_depth=8,
        enable_long_cot=True,
        enable_tot=True,
        enable_react=True,
        enable_got=True,
        checkpoint_interval=3
    )
    
    engine = create_super_engine(
        llm_callable=mock_llm,
        config=config
    )
    
    problem = "设计一个创新的产品解决方案，需要考虑技术可行性、用户需求和商业价值"
    
    start_time = time.time()
    result = engine.solve(problem, mode=ReasoningMode.SUPER)
    elapsed = time.time() - start_time
    
    graph = result['graph']
    stats = result['statistics']
    
    print(f"\n📊 超级模式推理结果:")
    print(f"  总节点数: {stats['total_nodes']}")
    print(f"  总边数: {stats['total_edges']}")
    print(f"  最大深度: {stats['max_depth']}")
    print(f"  平均评分: {stats['avg_score']:.3f}")
    
    print(f"\n📈 节点类型分布:")
    for node_type, count in stats['node_type_counts'].items():
        print(f"    {node_type}: {count}")
    
    print(f"\n🔗 边类型分布:")
    for edge_type, count in stats['edge_type_counts'].items():
        print(f"    {edge_type}: {count}")
    
    print(f"\n💡 顿悟时刻: {len(result['insights'])}")
    for i, insight in enumerate(result['insights'][:3]):
        print(f"    {i+1}. [{insight['type']}] {insight['content'][:50]}...")
    
    print(f"\n⏱️ 推理耗时: {elapsed:.2f}秒")
    
    return {'success': True, 'result': result}


def test_graph_traversal():
    """测试图遍历功能"""
    print("\n测试图遍历功能...")
    
    graph = SuperGraph("遍历测试")
    root = graph.create_root("根节点")
    
    # 构建复杂图结构
    node1 = graph.add_node("节点1", NodeType.LONG_COT_STEP, [root.node_id], 1)
    node2 = graph.add_node("节点2", NodeType.LONG_COT_STEP, [root.node_id], 1)
    node3 = graph.add_node("节点3", NodeType.TOT_BRANCH, [node1.node_id], 2)
    node4 = graph.add_node("节点4", NodeType.SYNTHESIS, [node1.node_id, node2.node_id], 2)
    node5 = graph.add_node("节点5", NodeType.FINAL, [node4.node_id], 3)
    
    # 测试路径查找
    path = graph.get_path(node5.node_id)
    assert len(path) > 0
    assert path[0].node_type == NodeType.ROOT
    assert path[-1].node_id == node5.node_id
    print(f"  ✓ 路径查找成功: {' -> '.join([n.content for n in path])}")
    
    # 测试拓扑排序
    topo = graph.topological_sort()
    assert len(topo) == len(graph.nodes)
    print(f"  ✓ 拓扑排序成功: {len(topo)}个节点")
    
    # 测试统计
    stats = graph.get_statistics()
    print(f"  ✓ 统计获取成功")
    print(f"    节点数: {stats.total_nodes}")
    print(f"    边数: {stats.total_edges}")
    print(f"    最大深度: {stats.max_depth}")
    
    return {'success': True, 'stats': stats.to_dict()}


def test_evaluator():
    """测试评估器"""
    print("\n测试评估器...")
    
    from intelligence.reasoning._unified_reasoning_engine import UnifiedEvaluator
    
    config = UnifiedConfig()
    evaluator = UnifiedEvaluator(config)
    
    # 创建测试节点
    node = UnifiedNode(
        node_id="test",
        content="因为A，所以B。因此C。这是一个关键的分析步骤。",
        node_type=NodeType.LONG_COT_STEP,
        depth=1
    )
    
    # 评估节点
    scores = evaluator.evaluate_node(node, {'problem': '测试问题'})
    
    print(f"  评估结果:")
    print(f"    相关性: {scores['relevance']:.3f}")
    print(f"    连贯性: {scores['coherence']:.3f}")
    print(f"    新颖性: {scores['novelty']:.3f}")
    print(f"    可行性: {scores['feasibility']:.3f}")
    print(f"    进展性: {scores['progress']:.3f}")
    print(f"    综合评分: {node.combined_score:.3f}")
    
    # 顿悟检测
    insight_node = UnifiedNode(
        node_id="insight",
        content="突然意识到，关键在于整合各方资源。",
        node_type=NodeType.INSIGHT
    )
    
    insight_result = evaluator.detect_insight(insight_node.content)
    if insight_result:
        print(f"  ✓ 顿悟检测成功: {insight_result[0]}, 影响度: {insight_result[1]:.2f}")
    
    return {'success': True, 'scores': scores}


def test_serializable():
    """测试序列化"""
    print("\n测试序列化...")
    
    graph = SuperGraph("序列化测试")
    root = graph.create_root("测试根节点")
    
    # 添加多个节点
    for i in range(5):
        graph.add_node(
            content=f"测试节点{i+1}",
            node_type=NodeType.LONG_COT_STEP,
            parent_ids=[root.node_id],
            depth=1
        )
    
    # 序列化为字典
    graph_dict = graph.to_dict()
    
    assert 'nodes' in graph_dict
    assert 'edges' in graph_dict
    assert 'statistics' in graph_dict
    
    # 转换为JSON
    json_str = json.dumps(graph_dict, indent=2, ensure_ascii=False)
    assert len(json_str) > 0
    
    print(f"  ✓ 序列化成功")
    print(f"  ✓ JSON长度: {len(json_str)} 字符")
    print(f"  ✓ 节点数: {len(graph_dict['nodes'])}")
    print(f"  ✓ 边数: {len(graph_dict['edges'])}")
    
    return {'success': True, 'json_length': len(json_str)}


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*70)
    print("🚀 超级推理引擎测试套件")
    print("="*70)
    
    suite = TestSuite()
    
    # 核心测试
    suite.run_test("超级图创建", test_super_graph_creation)
    suite.run_test("节点类型", test_node_types)
    suite.run_test("边类型", test_edge_types)
    suite.run_test("评估器", test_evaluator)
    suite.run_test("图遍历", test_graph_traversal)
    suite.run_test("序列化", test_serializable)
    
    # 推理模式测试
    suite.run_test("线性推理模式 (LongCoT)", test_unified_engine_linear)
    suite.run_test("分支推理模式 (ToT)", test_unified_engine_branching)
    suite.run_test("反应推理模式 (ReAct)", test_unified_engine_reactive)
    suite.run_test("超级推理模式 (All)", test_unified_engine_super)
    
    # 总结
    suite.summary()
    
    return suite


if __name__ == "__main__":
    results = run_all_tests()
    
    # 输出详细结果
    print("\n" + "="*70)
    print("📝 详细测试结果")
    print("="*70)
    
    for i, result in enumerate(results.results):
        status_icon = "✅" if result['status'] == 'PASS' else "❌"
        print(f"{i+1}. {status_icon} {result['name']}: {result['status']}")
