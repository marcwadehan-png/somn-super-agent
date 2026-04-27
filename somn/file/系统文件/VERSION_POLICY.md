# VERSION_POLICY.md — Neural Memory System 版本策略

**制定时间**: 2026-04-06 01:00  
**适用范围**: `src/neural_memory/`  
**对照文档**: `file/系统文件/systems/HEALTH_ALERT_neural_memory_fragmentation.md`  
**依赖分析**: `file/系统文件/systems/V1_V3_COMPARISON_neural_memory.md`

---

## 1. 版本决策

### 1.1 决策结论

> 按照告警报告建议，确定 **V3 为唯一主线版本**。

但基于基线扫描的事实修正，实际的版本决策如下：

| 角色 | 文件 | 版本标识 | 决策 |
|---|---|---|---|
| **主线版本** | `neural_memory_system_v3.py` → 将重命名为 `neural_system.py` | V3 | ✅ 唯一主线 |
| **兼容层** | 当前 `neural_system.py`（V1）→ 降级为 `neural_system_v1.py` | V1 | ⚠️ 降级为兼容层 |
| **实验模块** | `memory_encoding_system_v3.py` | V1.0 | ✅ 纳入主线 |
| **实验模块** | `reinforcement_learning_v3.py` | V1.0 | ✅ 纳入主线 |
| **缺失模块** | `memory_richness_v3.py` | V3 | ❌ 需补建 |
| **缺失模块** | `memory_granularity_v3.py` | V3 | ❌ 需补建 |
| **缺失模块** | `memory_engine_v2.py` | V2 | ❌ 需补建或用 V1 MemoryEngine 替代 |

### 1.2 决策依据

1. 告警报告明确建议"选定一个版本作为唯一主线（建议 V3）"
2. V3 在架构设计上更先进（异步、组件化、强化学习、多模态编码）
3. V3 的编码系统和强化学习系统已完整可用
4. V3 的丰满度/颗粒度/兼容层子模块缺失 → 需补建，非放弃 V3 的理由

### 1.3 命名规划

```
迁移前:                              迁移后:
neural_system.py (V1 主线)      →    neural_system_v1.py (兼容层)
neural_memory_system_v3.py (V3)  →    neural_system.py (V2 主线，从 V3 演化)
memory_encoding_system_v3.py     →    memory_encoding_system.py (去掉 v3 后缀)
reinforcement_learning_v3.py     →    reinforcement_learning.py (去掉 v3 后缀)
memory_richness_v3.py (需补建)   →    memory_richness.py
memory_granularity_v3.py (需补建)→    memory_granularity.py
```

---

## 2. 迁移计划

### Phase 0: 补建缺失子模块（前置条件）

| 模块 | 优先级 | 状态 | 说明 |
|---|---|---|---|
| `memory_richness.py` | P0 | 待补建 | 从 `neural_memory_system_v3.py` 的接口契约推导实现 |
| `memory_granularity.py` | P0 | 待补建 | 同上 |
| V2 兼容层（`memory_engine.py` 适配） | P1 | 待实现 | 用现有 V1 `MemoryEngine` 作为 V3 兼容层的后端 |

### Phase 1: 版本切换（核心动作）

| 步骤 | 动作 | 风险 | 回滚方式 |
|---|---|---|---|
| 1.1 | 创建 `neural_system_v1.py`（从当前 `neural_system.py` 复制） | 低 | 删除 v1 文件，恢复原名 |
| 1.2 | 在 `neural_system_v1.py` 头部添加 `@deprecated` 注解 | 低 | — |
| 1.3 | 将当前 `neural_system.py` 重命名为 `neural_system_v1.py` | 低 | 从备份恢复 |
| 1.4 | 将 `neural_memory_system_v3.py` 复制为新的 `neural_system.py` | 中 | 从备份恢复 |
| 1.5 | 新 `neural_system.py` 内部修正 import 路径（去掉 v3 后缀引用） | 中 | 逐步验证 |
| 1.6 | 更新 `__init__.py`：导出 V3 类名 + V1 兼容别名 | 中 | 从备份恢复 |
| 1.7 | 更新 `somn.py` 中的 import（如有接口变化） | 高 | 从备份恢复 |
| 1.8 | 运行全链路冒烟测试 | — | — |

### Phase 2: 清理与规范化

| 步骤 | 动作 | 说明 |
|---|---|---|
| 2.1 | `memory_encoding_system_v3.py` → `memory_encoding_system.py` | 去掉 v3 后缀 |
| 2.2 | `reinforcement_learning_v3.py` → `reinforcement_learning.py` | 去掉 v3 后缀 |
| 2.3 | 补建 `memory_richness.py`（从接口契约实现） | 新文件 |
| 2.4 | 补建 `memory_granularity.py`（从接口契约实现） | 新文件 |
| 2.5 | 删除旧的 `neural_memory_system_v3.py` | 迁移完成后 |
| 2.6 | 更新所有外部引用（tests/、file/系统文件/、scripts/） | 全项目扫描 |

---

## 3. 弃用规则

### 3.1 V1 降级注解规范

对降级为兼容层的文件，在模块 docstring 和类 docstring 中添加弃用标注：

```python
"""
[DEPRECATED] 神经记忆系统 V1 — 兼容层
Deprecated since: 2026-04-06
Replacement: neural_system.py (V3 主线)
Removal target: 2026-07-06

此文件为向后兼容保留，新代码请使用 neural_system.py (V3)。
"""
```

### 3.2 `@deprecated` 装饰器

对 V1 特有的公开方法，添加运行时弃用警告：

```python
import warnings

def deprecated(replacement: str, removal_date: str):
    """弃用装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} 已弃用，请使用 {replacement}。"
                f"计划移除日期: {removal_date}",
                DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### 3.3 弃用文件清单

| 文件 | 弃用时间 | 替代 | 计划移除 |
|---|---|---|---|
| `neural_system_v1.py`（原 `neural_system.py`） | 2026-04-06 | `neural_system.py` (V3) | 2026-07-06 |
| `test_memory_engine_v2.py` | 2026-04-06 | 待补建的 V2 兼容层测试 | 2026-07-06 |

---

## 4. 兼容周期

| 阶段 | 时间范围 | 状态 | 说明 |
|---|---|---|---|
| **Phase 0 — 补建** | 2026-04-06 ~ 2026-04-10 | 🔴 进行中 | 补建 3 个缺失子模块 |
| **Phase 1 — 切换** | 2026-04-10 ~ 2026-04-15 | ⏳ 待开始 | 版本切换 + 接口迁移 |
| **Phase 2 — 清理** | 2026-04-15 ~ 2026-04-20 | ⏳ 待开始 | 后缀清理 + 引用更新 |
| **兼容期** | 2026-04-06 ~ 2026-07-06 | — | V1 兼容层保留，发出 DeprecationWarning |
| **硬移除** | 2026-07-06 之后 | ⏳ 未来 | 删除 `neural_system_v1.py`、清理所有 V1 import |

---

## 5. 接口兼容保证

### 5.1 `__init__.py` 兼容别名

切换后 `__init__.py` 将同时导出 V3 主线接口和 V1 兼容别名：

```python
# V3 主线接口
from .neural_system import NeuralMemorySystemV3 as NeuralMemorySystem
from .neural_system import NeuralMemorySystemV3 as create_neural_system  # 不完全兼容，需要适配

# V1 兼容别名（Deprecated）
from .neural_system_v1 import NeuralMemorySystem as NeuralMemorySystemV1  # @deprecated
from .neural_system_v1 import create_neural_system as create_neural_system_v1  # @deprecated
```

### 5.2 `somn.py` 接口适配

```python
# somn.py 当前:
from src.neural_memory import NeuralMemorySystem

# 切换后（自动兼容，无需改动 somn.py）:
# __init__.py 将 NeuralMemorySystem 指向 V3 实现
# V3 的接口如果与 V1 不兼容，需要在 V3 中添加 V1 方法适配层
```

### 5.3 V1 独有功能迁移

V1 有 7 个独有方法在 V3 中不存在。迁移方案：

| V1 方法 | 迁移策略 | 优先级 |
|---|---|---|
| `record_research_finding()` | 在 V3 中实现为 `add_research_memory()` | P0 |
| `discover_value_and_generate_dimensions()` | 在 V3 中实现 | P1 |
| `generate_core_strategy()` | 在 V3 中实现 | P1 |
| `evolve_system()` | 在 V3 中实现 | P2 |
| `query_with_evidence()` | 在 V3 中实现为 `retrieve_with_evidence()` | P0 |
| `_suggest_validation()` | 合并入 V3 | P2 |
| `_assess_system_health()` | 合并入 V3 的 `get_stats()` | P1 |

---

## 6. 回滚策略

每个 Phase 执行前必须创建增量备份：

```
Phase 0 备份: _backup_neural_memory_phase0_YYYYMMDD.zip
Phase 1 备份: _backup_neural_memory_phase1_YYYYMMDD.zip
Phase 2 备份: _backup_neural_memory_phase2_YYYYMMDD.zip
```

全局回滚：使用 S0 阶段的 `_backup_neural_memory_cleanup_20260406.zip`。

---

*本策略文档基于 2026-04-06 代码快照和 V1/V3 功能对比分析制定。执行前需确认 Phase 0 补建完成。*
