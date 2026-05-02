"""
DivineReason V3.1.0 - 快速验证测试
测试：DIVINE 模式是否真正融合四大推理体系
"""
import sys
import time

# 添加路径
sys.path.insert(0, 'd:/AI/somn')
sys.path.insert(0, 'd:/AI/somn/smart_office_assistant/src')

print("=" * 80)
print("DivineReason V3.1.0 - 快速验证测试")
print("=" * 80)
print()

# 测试1: 导入
print("【测试1】导入 DivineReason...")
try:
    from knowledge_cells import DivineReason, ReasoningMode, NodeType, EdgeType
    print(f"✅ 导入成功")
    print(f"   VERSION = {DivineReason.VERSION}")
    print(f"   ENGINE_NAME = {DivineReason.ENGINE_NAME}")
except Exception as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)

print()

# 测试2: 实例化
print("【测试2】实例化 DivineReason...")
try:
    dr = DivineReason()
    print(f"✅ 实例化成功")
    print(f"   默认模式: {dr.config.default_mode}")
    print(f"   max_nodes: {dr.config.max_nodes}")
    print(f"   max_depth: {dr.config.max_depth}")
except Exception as e:
    print(f"❌ 实例化失败: {e}")
    sys.exit(1)

print()

# 测试3: DIVINE 模式 solve()
print("【测试3】DIVINE 模式 solve()...")
try:
    start_time = time.time()
    result = dr.solve("测试问题：如何提高团队效率？", mode=ReasoningMode.DIVINE)
    end_time = time.time()
    
    print(f"✅ solve() 调用成功")
    print(f"   耗时: {end_time - start_time:.2f} 秒")
    print(f"   success: {result.success}")
    print(f"   quality_score: {result.quality_score}")
    print(f"   mode: {result.mode}")
    print(f"   engine: {result.engine}")
    print(f"   solution 长度: {len(result.solution)} 字符")
    
    # 检查图结构
    if result.graph:
        graph = result.graph
        if hasattr(graph, 'nodes'):
            nodes = graph.nodes
            edges = graph.edges if hasattr(graph, 'edges') else {}
            print(f"   图节点数: {len(nodes)}")
            print(f"   图边数: {len(edges)}")
            
            # 统计节点类型
            type_counts = {}
            for n in nodes.values():
                t = n.node_type if hasattr(n, 'node_type') else 'unknown'
                type_counts[t] = type_counts.get(t, 0) + 1
            print(f"   节点类型统计:")
            for t, count in sorted(type_counts.items(), key=lambda x: -x[1]):
                print(f"      {t}: {count}")
        else:
            print(f"   图结构: 无 nodes 属性")
    else:
        print(f"   图结构: None")
    
    print(f"   solution 前200字符: {result.solution[:200]}...")
    
except Exception as e:
    print(f"❌ solve() 失败: {e}")
    import traceback
    traceback.print_exc()

print()

# 测试4: 检查 _expand_divine() 方法是否存在
print("【测试4】检查 _expand_divine() 方法...")
try:
    if hasattr(dr, '_expand_divine'):
        print(f"✅ _expand_divine() 方法存在")
        print(f"   方法: {dr._expand_divine}")
    else:
        print(f"❌ _expand_divine() 方法不存在")
except Exception as e:
    print(f"❌ 检查失败: {e}")

print()

# 测试5: 检查 solve() 中的 DIVINE 分支
print("【测试5】检查 solve() 中的 DIVINE 分支...")
try:
    import inspect
    source = inspect.getsource(dr.solve)
    if '_expand_divine' in source:
        print(f"✅ solve() 中调用了 _expand_divine()")
    else:
        print(f"❌ solve() 中没有调用 _expand_divine()")
        print(f"   可能还在调用 _expand_long_cot()")
except Exception as e:
    print(f"❌ 检查失败: {e}")

print()

# 测试6: 对比不同模式的输出
print("【测试6】对比不同推理模式的输出...")
modes = [
    ("LINEAR", ReasoningMode.LINEAR),
    ("DIVINE", ReasoningMode.DIVINE),
    ("SUPER", ReasoningMode.SUPER),
]

for mode_name, mode in modes:
    try:
        result = dr.solve("简单问题：1+1=?", mode=mode)
        print(f"   {mode_name}: quality_score={result.quality_score:.2f}, solution前50字='{result.solution[:50]}...'")
    except Exception as e:
        print(f"   {mode_name}: 失败 - {e}")

print()

print("=" * 80)
print("测试完成")
print("=" * 80)
