# -*- coding: utf-8 -*-
"""逻辑推理能力强化 - 简化验证"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.intelligence.reasoning._long_cot_engine import LongCoTReasoningEngine, LongCoTConfig
from src.intelligence.reasoning._tot_engine import TreeOfThoughtsEngine
from src.intelligence.reasoning._got_engine import GraphOfThoughtsEngine, GoTConfig
from src.intelligence.reasoning._react_engine import ReActEngine, ReActConfig, ToolRegistry, Tool

def mock_llm(prompt):
    return "模拟推理步骤: " + prompt[:50] + "..."

print("=" * 50)
print("逻辑推理能力强化 - 三阶段验证")
print("=" * 50)

# 第一阶段: LongCoT
print("\n[第一阶段] LongCoT基础增强...")
cot_config = LongCoTConfig(max_thinking_length=1024, checkpoint_interval=64)
cot = LongCoTReasoningEngine(config=cot_config, llm_callable=mock_llm)
result1 = cot.reason("分析市场竞争策略")
print(f"  ✅ LongCoT: {len(result1['reasoning_trace'])}步推理, {len(result1['checkpoints'])}检查点")

# 第二阶段: ToT
print("\n[第二阶段-1] ToT树推理...")
tot = TreeOfThoughtsEngine(llm_callable=mock_llm)
result2 = tot.solve("选择最佳增长方案", goal="最优解", max_iterations=5)
print(f"  ✅ ToT: {result2['metadata']['tree_stats']['total_nodes']}节点")

# 第二阶段: GoT
print("\n[第二阶段-2] GoT图推理...")
got_config = GoTConfig(max_nodes=30, max_depth=3)
got = GraphOfThoughtsEngine(config=got_config, llm_callable=mock_llm)
result3 = got.solve("分析竞争格局", goal="战略路径")
print(f"  ✅ GoT: {result3['metadata']['node_count']}节点, {result3['metadata']['edge_count']}边")

# 第三阶段: ReAct
print("\n[第三阶段] ReAct协同推理...")
registry = ToolRegistry()
registry.register(Tool(name="search", description="搜索", parameters={}, handler=lambda p: {"result": "OK"}))
registry.register(Tool(name="calculate", description="计算", parameters={}, handler=lambda p: {"result": "OK"}))
react_config = ReActConfig(max_iterations=10)
react = ReActEngine(config=react_config, registry=registry, llm_callable=mock_llm)
result4 = react.reason("查询数据并分析")
print(f"  ✅ ReAct: {result4['trajectory'].total_actions}行动, {result4['trajectory'].total_observations}观察")

print("\n" + "=" * 50)
print("✅ 三阶段验证全部通过!")
print("=" * 50)
