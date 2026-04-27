# GoT图推理引擎技术文档 v1.0

## 概述

GoT（Graph-of-Thoughts）图推理引擎是Somn智能系统的核心推理组件之一，提供了基于图网络的思维推理能力。

**版本**: V1.0.0
**日期**: 2026-04-24
**文件**: `src/intelligence/reasoning/_got_engine.py`

---

## 架构设计

### 核心组件

| 组件 | 类名 | 功能 |
|------|------|------|
| 图推理模式 | `GraphReasoningMode` | LINEAR/BRANCHING/CYCLIC/HYBRID 四种推理模式 |
| 思维节点 | `ThoughtGraphNode` | 表示推理过程中的思维单元 |
| 思维边 | `ThoughtEdge` | 表示节点间的关系（推导/支持/挑战/关联） |
| 思维图 | `ThoughtGraph` | 图结构管理，支持拓扑排序和路径搜索 |
| 图推理引擎 | `GraphOfThoughtsEngine` | 核心引擎，支持100节点图网络 |

### 节点数据结构

```
ThoughtGraphNode
├── node_id: str                    # 唯一标识
├── content: str                     # 推理内容
├── reasoning_type: str             # analysis/synthesis/evaluation/conclusion
├── parent_ids: List[str]            # 父节点列表（多父支持）
├── child_ids: List[str]             # 子节点列表
├── related_ids: List[str]           # 关联节点
├── relevance_score: float           # 相关性评分 0-1
├── coherence_score: float          # 连贯性评分 0-1
├── novelty_score: float            # 新颖性评分 0-1
├── combined_score: float           # 综合评分
├── depth: int                       # 图深度
├── status: str                     # pending/expanded/evaluated/final
└── metadata: Dict                  # 元数据
```

### 边数据结构

```
ThoughtEdge
├── edge_id: str                     # 唯一标识
├── source_id: str                   # 源节点
├── target_id: str                    # 目标节点
├── relation_type: str               # derives/supports/challenges/related
├── weight: float                    # 边权重
└── confidence: float                 # 置信度
```

---

## 推理模式

### 1. LINEAR（线性推理）
单链式推理，每个节点最多一个父节点和一个子节点。
适用于：简单因果推导、逐步论证。

### 2. BRANCHING（分支推理）
树状结构，支持多个子节点并行展开。
适用于：方案比较、多角度分析。

### 3. CYCLIC（循环推理）
支持循环边的图结构，用于迭代优化和反馈。
适用于：自我改进、反复推敲。

### 4. HYBRID（混合推理）
组合以上三种模式，适合复杂推理场景。

---

## 核心算法

### 1. 拓扑排序（Topological Sort）
```python
def topological_sort(self) -> List[str]:
    """返回节点的拓扑排序"""
```
使用Kahn算法，保证父节点在子节点之前处理。

### 2. 路径搜索（Path Finding）
```python
def get_path(self, node_id: str) -> List[ThoughtGraphNode]:
    """从根节点到指定节点的BFS最短路径"""

def get_all_paths(self, start_id: str, end_id: str) -> List[List[ThoughtGraphNode]]:
    """两节点间所有可能的路径"""
```
支持：最短路径、所有路径枚举。

### 3. 图注意力机制
`ThoughtGraphNode` 包含多维评分：
- relevance_score: 节点对目标的关联度
- coherence_score: 与上下文的连贯性
- novelty_score: 推理的创新程度
- combined_score: 综合评分（加权求和）

---

## GraphOfThoughtsEngine 核心方法

| 方法 | 功能 | 返回值 |
|------|------|--------|
| `reason()` | 执行图推理 | `GoTResult` |
| `expand_node()` | 扩展节点生成子节点 | `ThoughtGraphNode` |
| `evaluate_node()` | 评估节点质量 | `float` |
| `synthesize()` | 综合多个分支形成结论 | `str` |
| `export_trace()` | 导出推理轨迹 | `Optional[Dict]` |

### reason() 方法签名
```python
def reason(
    self,
    problem: str,
    context: Optional[Dict[str, Any]] = None,
    mode: GraphReasoningMode = GraphReasoningMode.HYBRID,
    max_nodes: int = 100,
    max_depth: int = 10
) -> GoTResult
```

### expand_node() 方法签名
```python
def expand_node(
    self,
    node: ThoughtGraphNode,
    num_children: int = 3,
    reasoning_type: str = "analysis"
) -> List[ThoughtGraphNode]
```

---

## 使用示例

### 基础使用
```python
from smart_office_assistant.src.intelligence.reasoning._got_engine import (
    GraphOfThoughtsEngine,
    GraphReasoningMode,
    ThoughtGraphNode,
)

# 创建引擎
engine = GraphOfThoughtsEngine(
    llm_callable=my_llm,  # LLM调用函数
    max_nodes=100,
    max_depth=10
)

# 执行推理
result = engine.reason(
    problem="分析人工智能对就业市场的影响",
    mode=GraphReasoningMode.BRANCHING
)

print(f"结论: {result.final_answer}")
print(f"节点数: {result.graph_stats['total_nodes']}")
```

### 自定义节点和边
```python
from smart_office_assistant.src.intelligence.reasoning._got_engine import (
    ThoughtGraph,
    ThoughtGraphNode,
    ThoughtEdge,
)

# 创建根节点
root = ThoughtGraphNode(
    node_id="root_1",
    content="初始问题分析",
    reasoning_type="analysis"
)

# 创建图
graph = ThoughtGraph(root)

# 添加节点
node2 = ThoughtGraphNode(
    node_id="node_2",
    content="第一层推理",
    reasoning_type="synthesis",
    depth=1
)
graph.add_node(node2)

# 添加边
edge = ThoughtEdge(
    edge_id="edge_1",
    source_id="root_1",
    target_id="node_2",
    relation_type="derives"
)
graph.add_edge(edge)

# 获取路径
path = graph.get_path("node_2")
print([n.content for n in path])
```

---

## 性能指标

| 指标 | 数值 |
|------|------|
| 最大节点数 | 100 |
| 最大深度 | 10 |
| 支持节点评分维度 | 4维（relevance/coherence/novelty/combined）|
| 边关系类型 | 4种（derives/supports/challenges/related）|

---

## 与其他引擎的集成

### 调度注册路径
```
UnifiedIntelligenceCoordinator
    └── got_reasoning → GraphOfThoughtsEngine
```

### 引擎选择逻辑
- 问题含"因果/关系/网络/图" → `got_reasoning`
- 问题含"分析/推理/论证" → `long_cot_reasoning`
- 问题含"方案/选择/比较" → `tot_reasoning`

---

## 测试覆盖

| 测试类 | 用例数 | 覆盖内容 |
|--------|--------|----------|
| `TestGoTTypes` | 4 | GraphReasoningMode枚举、ThoughtGraphNode、ThoughtEdge、GoTConfig |
| `TestThoughtGraph` | 7 | 图创建、节点操作、边操作、路径搜索、拓扑排序 |

**测试验证**: `tests/test_reasoning_engine.py` 中 103 个用例全部通过。

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| V1.0.0 | 2026-04-24 | 初始版本，支持图推理、注意力机制、路径搜索 |
