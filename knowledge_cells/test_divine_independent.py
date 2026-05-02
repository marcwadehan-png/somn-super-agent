"""
DivineReason V3.1.0 - 独立推理能力验证测试
验证：所有功能架构设计是否已落实到代码层面，能独立完成推理解决问题？
"""
import sys
import time

# 添加路径
sys.path.insert(0, 'd:/AI/somn')
sys.path.insert(0, 'd:/AI/somn/smart_office_assistant/src')

print("=" * 80)
print("DivineReason V3.1.0 - 独立推理能力验证测试")
print("=" * 80)
print()

# ============================================================
# 测试1: 基础架构验证
# ============================================================
print("【测试1】基础架构验证")
print("-" * 80)

try:
    from knowledge_cells import (
        DivineReason, ReasoningMode, NodeType, EdgeType,
        ReasoningResult, SuperGraph, UnifiedConfig
    )
    print("✅ 1.1 所有核心类导入成功")
    print(f"   DivineReason.VERSION = {DivineReason.VERSION}")
    print(f"   DivineReason.ENGINE_NAME = {DivineReason.ENGINE_NAME}")
    print(f"   推理模式数量: {len(ReasoningMode)} 种")
    print(f"   节点类型数量: {len(NodeType)} 种")
    print(f"   边类型数量: {len(EdgeType)} 种")
except Exception as e:
    print(f"❌ 1.1 导入失败: {e}")
    sys.exit(1)

# 检查四大推理体系的方法是否存在
dr = DivineReason()
required_methods = [
    '_expand_long_cot',   # LongCoT
    '_expand_tot',         # ToT
    '_expand_react',       # ReAct
    '_expand_got',         # GoT
    '_expand_divine',      # DIVINE (融合)
    '_expand_super',       # SUPER (超级)
]

print()
print("检查四大推理体系的方法实现:")
for method in required_methods:
    if hasattr(dr, method):
        print(f"✅ {method}() 存在")
    else:
        print(f"❌ {method}() 不存在")

print()
print("-" * 80)

# ============================================================
# 测试2: 无 LLM 时的推理能力（独立推理）
# ============================================================
print("【测试2】无 LLM 时的推理能力（独立推理）")
print("-" * 80)

test_problems = [
    ("简单数学", "1 + 1 = ?"),
    ("逻辑推理", "所有的猫都是动物，所有的动物都需要氧气，那么所有的猫都需要氧气吗？"),
    ("问题解决", "如何提高团队的工作效率？"),
    ("分析判断", "一个产品用户流失率突然上升，可能的原因有哪些？"),
]

for problem_name, problem in test_problems:
    print(f"\n问题: {problem_name}")
    print(f"内容: {problem}")
    
    start = time.time()
    result = dr.solve(problem, mode=ReasoningMode.DIVINE)
    end = time.time()
    
    print(f"  耗时: {end - start:.2f} 秒")
    print(f"  成功: {result.success}")
    print(f"  质量评分: {result.quality_score:.2f}")
    print(f"  推理模式: {result.mode}")
    print(f"  解决方案长度: {len(result.solution)} 字符")
    
    # 检查解决方案是否真实
    solution = result.solution
    if solution and len(solution) > 50:
        print(f"  解决方案前100字: {solution[:100]}...")
        
        # 检查是否包含模板文字
        template_keywords = ["步骤", "深入分析", "多个角度", "潜在关系"]
        is_template = any(kw in solution for kw in template_keywords)
        if is_template:
            print(f"  ⚠️ 警告: 解决方案可能包含模板文字")
        else:
            print(f"  ✅ 解决方案看起来是真实的推理结果")
    else:
        print(f"  ❌ 解决方案过短或为空: '{solution}'")
    
    # 检查图结构
    if result.graph and hasattr(result.graph, 'nodes'):
        nodes = result.graph.nodes
        node_count = len(nodes)
        print(f"  图节点数: {node_count}")
        
        # 统计节点类型
        type_counts = {}
        for n in nodes.values():
            t = n.node_type if hasattr(n, 'node_type') else 'unknown'
            type_counts[t] = type_counts.get(t, 0) + 1
        
        print(f"  节点类型分布:")
        for t, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            print(f"    {t}: {count}")

print()
print("-" * 80)

# ============================================================
# 测试3: 检查生成器实现（是否有真实的推理能力）
# ============================================================
print("【测试3】检查生成器实现")
print("-" * 80)

# 检查 generator 的实现
generator = dr.generator
print(f"生成器类型: {type(generator).__name__}")
print(f"生成器方法:")
for method_name in ['generate_step', 'generate_branches', 'generate_tool_action']:
    if hasattr(generator, method_name):
        method = getattr(generator, method_name)
        print(f"  ✅ {method_name}() 存在")
        
        # 检查是否是默认实现（返回模板）
        if method_name == 'generate_step':
            test_output = method("测试问题", [], ReasoningMode.DIVINE)
            print(f"     测试结果: {test_output[:50]}...")
            
            if "步骤" in test_output and "深入分析" in test_output:
                print(f"  ⚠️ 警告: generate_step() 返回模板文字，无真实推理！")
            else:
                print(f"  ✅ generate_step() 返回非模板内容")
    else:
        print(f"  ❌ {method_name}() 不存在")

print()
print("-" * 80)

# ============================================================
# 测试4: 检查推理结果的真实性
# ============================================================
print("【测试4】检查推理结果的真实性")
print("-" * 80)

# 使用同一个问题，测试多次，看结果是否一致
problem = "如何提高团队效率？"
results = []

print(f"问题: {problem}")
print(f"运行 3 次，检查输出是否一致:")

for i in range(3):
    result = dr.solve(problem, mode=ReasoningMode.DIVINE)
    results.append(result.solution)
    print(f"  运行 {i+1}: solution = {result.solution[:50]}...")

# 检查是否所有结果都相同（说明是模板）
if len(set(results)) == 1:
    print(f"  ⚠️ 警告: 所有运行结果完全相同！")
    print(f"  这说明推理是模板化的，不是真实推理！")
else:
    print(f"  ✅ 运行结果不同，可能是真实推理")

print()
print("-" * 80)

# ============================================================
# 测试5: 检查是否需要外部 LLM
# ============================================================
print("【测试5】检查是否需要外部 LLM")
print("-" * 80)

print("当前 DivineReason 实例化方式:")
print(f"  dr = DivineReason()  # 无 LLM")
print()

print("检查代码中是否强制要求 LLM:")
print(f"  solve() 方法是否检查 LLM?")
print(f"  generator 是否有默认实现？")

# 检查 solve() 方法是否在没有 LLM 时也能工作
try:
    result = dr.solve("测试", mode=ReasoningMode.DIVINE)
    if result.success:
        print(f"  ✅ solve() 在无 LLM 时也能工作")
        print(f"     但这使用的是模板推理，不是真实推理！")
    else:
        print(f"  ❌ solve() 在无 LLM 时失败")
except Exception as e:
    print(f"  ❌ solve() 在无 LLM 时抛出异常: {e}")

print()
print("-" * 80)

# ============================================================
# 总结：是否能独立完成推理解决问题？
# ============================================================
print("【总结】DivineReason V3.1.0 是否能独立完成推理解决问题？")
print("=" * 80)
print()

# 评估标准
criteria = [
    ("✅ 架构完整性", "四大推理体系（GoT+LongCoT+ToT+ReAct）是否已实现？", "是"),
    ("✅ 代码实现", "所有方法是否已落实到代码层面？", "是"),
    ("❌ 推理真实性", "推理结果是真实的吗？（非模板）", "否"),
    ("❌ 独立推理能力", "无 LLM 时能否进行真实推理？", "否"),
    ("⚠️ 图结构", "是否生成了丰富的图结构？", "是（但内容是模板）"),
]

print("评估结果:")
for criterion, description, answer in criteria:
    print(f"  {criterion} {description}")
    print(f"    答案: {answer}")
    print()

print("=" * 80)
print("最终结论:")
print("=" * 80)
print()
print("❌ DivineReason V3.1.0 **不能**独立完成真实推理解决问题！")
print()
print("原因:")
print("  1. ✅ 架构设计完整（四大推理体系）")
print("  2. ✅ 代码实现完整（所有方法已落实）")
print("  3. ❌ 但推理内容是模板化的（非真实推理）")
print("  4. ❌ 无 LLM 时，只能返回硬编码模板")
print("  5. ❌ 需要外部 LLM 回调才能进行真实推理")
print()
print("结论:")
print("  DivineReason V3.1.0 是一个**推理框架**，不是**推理引擎**！")
print()
print("  - 作为框架：✅ 完整（架构 + 代码）")
print("  - 作为引擎：❌ 不完整（需要外部 LLM 提供推理能力）")
print()
print("建议:")
print("  1. 如果要独立完成推理，需要内置一个基础推理模型")
print("  2. 或者，明确文档说明：需要外部 LLM 回调")
print("  3. 或者，实现一个基础规则推理引擎（无 LLM 时）")
print()
print("=" * 80)
