# 知识格子系统 v1.1

> 迁移自legacy的动态格子系统，结合Somn项目进行优化升级

## 📁 目录结构

```
knowledge_cells/
├── __init__.py          # 统一接口
├── cell_engine.py       # 格子引擎
├── fusion_engine.py     # 知识融合器
├── method_checker.py    # 方法论检查器
├── cli.py               # 交互式CLI
├── test_system.py       # 测试脚本
├── INDEX.md             # 索引
├── A1-A8.md            # 智慧核心
└── B1-C4.md            # 知识域
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /path/to/somn
python -m pip install pytest
```

### 2. 运行测试

```bash
python knowledge_cells\test_system.py
```

### 3. 交互式CLI

```bash
python knowledge_cells\cli.py
```

## 📖 使用示例

### Python API

```python
from knowledge_cells import get_knowledge_system

# 获取系统
system = get_knowledge_system()

# 知识查询
result = system.query("如何提升用户增长")
print(result['answer'])
print(f"使用格子: {result['cells_used']}")
print(f"推荐框架: {result['frameworks']}")
print(f"质量分数: {result['quality_score']}")

# 方法论检查
check = system.check_methodology("你的分析内容...")
print(f"评分: {check['overall_score']}/100")
print(f"等级: {check['level']}")

# 获取格子详情
cell = system.get_cell_content("A1")
print(f"名称: {cell['name']}")
print(f"标签: {cell['tags']}")
print(f"关联: {cell['associations']}")

# 搜索
results = system.search_cells("裂变")
print(f"找到: {[r['name'] for r in results]}")

# 知识图谱
graph = system.get_knowledge_graph()
print(f"节点: {len(graph['nodes'])}, 边: {len(graph['links'])}")
```

### 快捷函数

```python
from knowledge_cells import query, check, get_status

# 一行查询
result = query("直播运营的关键指标有哪些?")

# 一行检查
result = check("CAC是80元，LTV是200元，比例2.5倍...")

# 一行状态
status = get_status()
```

### CLI命令

```
(知识) > ask 如何提升用户增长
(知识) > check 请分析当前的市场情况...
(知识) > search 直播
(知识) > cell B2
(知识) > related A1
(知识) > hot
(知识) > graph
(知识) > list
(知识) > status
```

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    KnowledgeSystem                       │
│                    统一接口层                            │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ CellEngine   │  │ FusionEngine │  │MethodChecker │  │
│  │ 格子引擎      │  │ 知识融合器    │  │ 方法论检查   │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                  │          │
│         ▼                 ▼                  ▼          │
│  ┌─────────────────────────────────────────────────┐   │
│  │              21个知识格子 (Markdown)              │   │
│  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐      │   │
│  │  │ A1  │ │ A2  │ │ A3  │ │ A4  │ │ A5  │ ...   │   │
│  │  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘      │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## 📊 21个知识格子

### 智慧核心 (8个)

| ID | 名称 | 核心能力 |
|----|------|----------|
| A1 | 逻辑判断 | 三层推理 + 8种谬误检测 |
| A2 | 智慧模块 | 25学派融合 |
| A3 | 论证审核 | 翰林院三轮审核 |
| A4 | 判断决策 | 七人投票 + 太极阴阳 |
| A5 | 五层架构 | Somn核心架构 |
| A6 | 核心执行链 | 五步主链 |
| A7 | 感知记忆 | 快速扫描 |
| A8 | 反思进化 | ROI追踪 |

### 知识域 (13个)

| ID | 名称 | 核心内容 |
|----|------|----------|
| B1 | 用户增长 | AARRR、裂变、私域 |
| B2 | 直播运营 | 三角定律、FABE |
| B3 | 私域运营 | 企微、社群 |
| B4 | 活动策划 | 四类活动 |
| B5 | 会员运营 | 等级、权益 |
| B6 | 广告策划 | 创意、投放 |
| B7 | 地产策划 | 定位、推广 |
| B8 | 招商策划 | 业态规划 |
| B9 | 策略运营 | 规划、执行 |
| C1 | 电商运营 | 流量、转化 |
| C2 | 数据运营 | 指标、分析 |
| C3 | 内容营销 | 选题、创作 |
| C4 | 广告投放 | 精准投放 |

## 🧠 核心功能

### 1. 知识融合
- 自动检索相关格子
- 整合多格子知识
- 推荐分析框架
- 提取举一反三

### 2. 方法论检查
五维度评估：
- 诊断 (20%)
- 框架 (20%)
- 数据 (20%)
- 逻辑 (20%)
- 类比 (20%)

### 3. 知识图谱
- 格子节点
- 关联边
- 激活统计

## 🔧 方法论纪律

来自legacy的实战经验：

1. **先诊断后开药** - 不清楚现状就给方案是职业病
2. **框架前置** - 结论必须在框架跑完之后
3. **数据优先** - "我不知道"比"我猜"更专业

## 🌐 API集成

知识格子系统已集成到Somn API，可通过HTTP访问：

```
# 获取所有格子
GET /api/v1/cells

# 系统状态
GET /api/v1/cells/status

# 搜索格子
GET /api/v1/cells/search?keyword=裂变

# 最热格子
GET /api/v1/cells/hot?top_n=5

# 知识图谱
GET /api/v1/cells/graph

# 获取指定格子
GET /api/v1/cells/{cell_id}

# 关联格子
GET /api/v1/cells/{cell_id}/related

# 知识查询
POST /api/v1/cells/query
Body: {"question": "如何提升用户增长"}

# 方法论检查
POST /api/v1/cells/check
Body: {"content": "你的分析内容..."}
```

## 📜 更新日志

### v1.3 (2026-04-26)
- 新增推理增强器 `reasoning_enhancer.py`
- 新增神经集成模块 `neural_integration.py`
- 与Somn核心推理引擎深度集成

### v1.2 (2026-04-26)
- 新增API路由 `/api/v1/cells/*`
- 新增pytest测试 `tests/test_knowledge_cells.py`
- 更新README文档

### v1.1 (2026-04-26)
- 新增CLI交互界面
- 新增test_system.py测试脚本
- 修复cell_engine.py解析bug
- 优化知识融合算法

### v1.0 (2026-04-26)
- 从legacy迁移21个知识格子
- 创建cell_engine、fusion_engine、method_checker
- 创建METHODOLOGY.md方法论纪律
