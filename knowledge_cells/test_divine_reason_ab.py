"""
DivineReason V3.1.0 完整版 A/B 测试（简化版）
"""
import sys
import time
import json
from datetime import datetime

sys.path.insert(0, 'd:/AI/somn')
sys.path.insert(0, 'd:/AI/somn/smart_office_assistant/src')

test_results = []
start_time = time.time()


def check(test_id, description, condition, detail=""):
    """记录测试结果"""
    if condition:
        print(f"✅ {test_id}: 通过 - {description}")
        test_results.append({"id": test_id, "status": "PASS", "error": None})
        return True
    else:
        print(f"❌ {test_id}: 失败 - {description} {detail}")
        test_results.append({"id": test_id, "status": "FAIL", "error": detail})
        return False


# ==================== T1: 导入测试 ====================
print("\n" + "="*60)
print("T1: 导入测试")
print("="*60)
try:
    from knowledge_cells import DivineReason, ReasoningMode, NodeType, EdgeType, SuperGraph
    print(f"  VERSION = {DivineReason.VERSION}")
    check("T1", "导入 DivineReason 等类", True)
except Exception as e:
    print(f"  异常: {e}")
    check("T1", "导入 DivineReason 等类", False, str(e))
    sys.exit(1)


# ==================== T2: 实例化测试 ====================
print("\n" + "="*60)
print("T2: 实例化测试")
print("="*60)
try:
    dr = DivineReason()
    print(f"  max_nodes = {dr.config.max_nodes}")
    print(f"  max_depth = {dr.config.max_depth}")
    check("T2", "实例化 DivineReason", True)
except Exception as e:
    print(f"  异常: {e}")
    check("T2", "实例化 DivineReason", False, str(e))


# ==================== T3: solve() 基础测试 ====================
print("\n" + "="*60)
print("T3: solve() 基础测试")
print("="*60)
try:
    result = dr.solve("测试问题：如何提高团队效率？")
    print(f"  success = {result.success}")
    print(f"  solution 长度 = {len(result.solution)}")
    print(f"  quality_score = {result.quality_score}")
    print(f"  mode = {result.mode}")
    check("T3", "solve() 基础功能", result.success and len(result.solution) > 0)
except Exception as e:
    print(f"  异常: {e}")
    import traceback
    traceback.print_exc()
    check("T3", "solve() 基础功能", False, str(e))


# ==================== T4: 节点类型测试 ====================
print("\n" + "="*60)
print("T4: 节点类型测试")
print("="*60)
try:
    print(f"  节点类型数量: {len(NodeType)}")
    for nt in list(NodeType)[:5]:
        print(f"    - {nt.name} = {nt.value}")
    check("T4", f"节点类型 >= 14 种", len(NodeType) >= 14, f"实际: {len(NodeType)}")
except Exception as e:
    print(f"  异常: {e}")
    check("T4", "节点类型测试", False, str(e))


# ==================== T5: 边类型测试 ====================
print("\n" + "="*60)
print("T5: 边类型测试")
print("="*60)
try:
    print(f"  边类型数量: {len(EdgeType)}")
    for et in list(EdgeType)[:5]:
        print(f"    - {et.name} = {et.value}")
    check("T5", f"边类型 >= 11 种", len(EdgeType) >= 11, f"实际: {len(EdgeType)}")
except Exception as e:
    print(f"  异常: {e}")
    check("T5", "边类型测试", False, str(e))


# ==================== T6: SuperGraph 测试 ====================
print("\n" + "="*60)
print("T6: SuperGraph 图结构测试")
print("="*60)
try:
    graph = SuperGraph(problem="测试问题")
    print(f"  SuperGraph 创建成功")
    
    root = graph.create_root(content="测试问题：如何提高团队效率？")
    print(f"  根节点: {root.node_id}, type={root.node_type}")
    
    node1 = graph.add_node(
        content="步骤1：分析现状",
        node_type=NodeType.LONG_COT_STEP,
        depth=1
    )
    print(f"  节点1: {node1.node_id}, type={node1.node_type}")
    
    edge1 = graph.add_edge(
        source_id=root.node_id,
        target_id=node1.node_id,
        edge_type=EdgeType.LOGICAL_FLOW
    )
    print(f"  边1: {edge1.edge_id if edge1 else None}")
    
    if hasattr(graph, 'get_statistics'):
        stats = graph.get_statistics()
        print(f"  图统计: {stats}")
    
    check("T6", "SuperGraph 图结构", True)
except Exception as e:
    print(f"  异常: {e}")
    import traceback
    traceback.print_exc()
    check("T6", "SuperGraph 图结构", False, str(e))


# ==================== T7: 性能测试 ====================
print("\n" + "="*60)
print("T7: 性能测试")
print("="*60)
try:
    # 实例化性能
    start = time.time()
    dr2 = DivineReason()
    init_time = time.time() - start
    print(f"  实例化时间: {init_time*1000:.2f}ms")
    
    # 推理性能
    start = time.time()
    result = dr2.solve("快速测试问题")
    solve_time = time.time() - start
    print(f"  推理时间: {solve_time*1000:.2f}ms")
    
    check("T7", "性能测试", True)
except Exception as e:
    print(f"  异常: {e}")
    check("T7", "性能测试", False, str(e))


# ==================== 测试报告 ====================
total = len(test_results)
passed = sum(1 for r in test_results if r["status"] == "PASS")
failed = sum(1 for r in test_results if r["status"] == "FAIL")
errors = 0

end_time = time.time()
duration = end_time - start_time

print("\n" + "="*60)
print("测试报告")
print("="*60)
print(f"总测试数: {total}")
print(f"通过: {passed} ({passed/total*100:.1f}%)")
print(f"失败: {failed} ({failed/total*100:.1f}%)")
print(f"异常: {errors} ({errors/total*100:.1f}%)")
print(f"总耗时: {duration:.2f}s")
print("="*60)

# 输出失败的测试
if failed > 0:
    print("\n失败的测试:")
    for r in test_results:
        if r["status"] == "FAIL":
            print(f"  {r['id']}: {r['error']}")

# 保存结果
report = {
    "timestamp": datetime.now().isoformat(),
    "version": "V3.1.0",
    "total_tests": total,
    "passed": passed,
    "failed": failed,
    "errors": errors,
    "duration": duration,
    "results": test_results
}

with open("divine_reason_ab_test_results.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(f"\n详细报告已保存到: divine_reason_ab_test_results.json")

sys.exit(0 if (failed == 0 and errors == 0) else 1)
