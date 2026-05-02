# 神之架构双轨制系统 v2.0

## 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                    A轨：神政轨 (管理监管)                  │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐               │
│  │   DivineReason    │  │ Pan-Wisdom Tree  │               │
│  │   (神之推理V4.0)  │  │ (万法智慧树V1.0) │               │
│  │  节点→跳过调度    │  │ 枝丫→跳过调度    │               │
│  │    直接调用B轨    │  │    直接调用B轨    │               │
│  └────────┬─────────┘  └────────┬─────────┘               │
│           │    (特权调用)        │    (特权调用)            │
│  ┌────────▼──────────────────────▼────────┐               │
│  │         SageDispatch 调度系统           │               │
│  │  SD-F2 / SD-P1 / SD-R1 / SD-C2        │               │
│  └──────────────────┬─────────────────────┘               │
│                     ↓ A→B 单向调用                         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              B轨：神行轨 (执行)                            │
│                                                             │
│  ┌──────────────────────────────────────────────┐         │
│  │           ClawSystem (利爪系统)              │         │
│  │  ClawIndependentWorker × 763个              │         │
│  │  每个Claw独立思考/论证/答疑                  │         │
│  │  神行轨的Claws是干活的职场牛马              │         │
│  └──────────────────────────────────────────────┘         │
│                                                             │
│  ┌──────────────────────────────────────────────┐         │
│  │       职能部门 (可直接调用，跳过冗余环节)      │         │
│  │  兵部/户部/工部/吏部/礼部/刑部/厂卫/...     │         │
│  └──────────────────────────────────────────────┘         │
│                                                             │
│  知识访问: DomainNexus ✅  |  藏书阁 ❌                   │
│                     ↑ 结果回报A轨                          │
└─────────────────────────────────────────────────────────────┘

调用权限: DivineReason(节点) ✅ | Pan-Wisdom Tree(枝丫) ✅ | A神政轨 ✅ | 其他 ❌
```

## B轨核心差异定位

> **神行轨的Claws是干活的、是系统内的职场牛马。**

这是神行轨与架构中其他所有板块的**根本差异**：

| 维度 | A轨（神政轨） | B轨（神行轨） |
|------|-------------|-------------|
| **本质角色** | 思考者 / 决策者 | **干活者 / 执行者** |
| **核心使命** | 推理、分析、战略制定 | **干活、落地、产出结果** |
| **价值体现** | 想得对 | **干得完、干得好** |
| **比喻** | 军师 / 宰相 | **牛马 / 干将** |
| **能力重心** | DivineReason深度推理 | Claw独立执行 |

Claw虽然能独立思考、能论证、能答疑——但**能想不是目的，能干才是**。
思考力是为执行力服务的，不是自我欣赏的。

---

## 核心设计原则

| 原则 | 实现方式 |
|------|---------|
| **单向调用** | `TrackBridge.validate_call_direction()` 强制 A→B，禁止 B→A |
| **跳过多余环节** | `direct_department_call()` 直接调用B轨职能部门，无需层层下发 |
| **结果回报** | B轨通过callback机制回报A轨执行结果 |
| **独立工作** | 每个Claw拥有独立上下文、SOUL、IDENTITY、ReAct闭环 |
| **分层调度** | SD-F2/SD-P1负责任务分层，Pan-Wisdom Tree树干→枝干→枝丫 |

---

## 文件结构

```
src/intelligence/dual_track/
├── __init__.py          # 统一导出接口
├── track_a.py           # A轨: 神政轨 (管理监管)
├── track_b.py           # B轨: 神行轨 (执行)
├── bridge.py            # 双轨桥接器 + 统一入口
└── test_simple.py       # 简单测试脚本
```

---

## 核心类说明

### DivineGovernanceTrack (A轨 - 神政轨)

```python
class DivineGovernanceTrack:
    """
    管理监管类架构
    
    职责：
    1. 接收用户请求 → process_request()
    2. 问题分析与决策 → _analyze_and_decide()
    3. 制定执行策略 → _formulate_strategy()
    4. 派发任务给B轨 → _dispatch_to_track_b()
    5. 监控执行过程 → _wait_for_result()
    6. 验收执行结果 → _review_result()
    """
    
    # 使用DivineReason进行问题分析
    self.divine_reason = DivineReasonEngine()
```

### DivineExecutionTrack (B轨 - 神行轨)

```python
class DivineExecutionTrack:
    """
    执行类架构
    
    ★ 核心差异定位 ★
    神行轨的Claws是干活的、是系统内的职场牛马。
    能想不是目的，能干才是。
    
    职责：
    1. 接收A轨派发的任务 → receive_task()
    2. 分配给合适的Claw/部门 → _execute_task()
    3. 直接调用职能部门处理器 (跳过多余环节)
    4. 将执行结果回报A轨
    
    关键特性：
    - 可被直接调用 (import ClawSystem and ask)
    - Claw独立思考和行动 — 但思考力服务于执行力
    - 单向通信: 只能接收A轨指令
    """
```

### TrackBridge (双轨桥接器)

```python
class TrackBridge:
    """
    双轨桥接器 - 连接A/B两轨
    
    核心方法：
    - create_system(): 创建并连接双轨系统
    - validate_call_direction(): 验证调用方向合法性
    - direct_department_call(): 直接部门调用(跳过多余环节)
    """
```

### DualTrackSystem (统一入口)

```python
class DualTrackSystem:
    """
    双轨架构对外统一入口
    
    使用方式：
    bridge = TrackBridge()
    system = bridge.create_system()
    result = system.process("如何提升竞争力？")
    
    # 或者直接调用（跳过多余环节）
    result = system.execute_direct("兵部", "分析竞争策略")
    """
```

---

## 调用流程图

### 完整请求流程

```
用户请求 "分析市场竞争"
        ↓
[A轨-神政轨]
        │
    ① process_request()
        │
    ② _analyze_and_decide()     ← DivineReason分析
        │
    ③ _formulate_strategy()      ← 确定主责部门(如兵部)
        │
    ④ _dispatch_to_track_b()     ↓ 派发任务给B轨
        │
[B轨-神行轨]  ← receive_task()
        │
    ⑤ _execute_task()            ← 直接调用兵部处理器
        │                        (跳过冗余环节！)
    ⑥ _handle_bingbu()           ← 兵部分析完成
        │
    ⑦ callback(task_id, result)  ↑ 回报A轨
        │
[A轨-神政轨]
        │
    ⑧ _review_result()           ← 验收结果
        │
    返回最终结果给用户 ✓
```

### Pan-Wisdom Tree集成

```
Pan-Wisdom Tree (万法智慧树)
    │
    ├── 树干 (SD-P1 任务分层)
    │     │
    │     ├── 枝干 (SD-D2 深度推理)
    │     │     │
    │     │     └── 枝丫 (具体执行)
    │     │           │
    │     │           ↓ import ClawSystem
    │     │           ↓ claw.ask("分析竞争策略")  ← 直接调用！
    │     │
    │     └── ...其他枝干...
    │
    └── ...
```

**关键代码** (`bridge.py`):
```python
def create_wisdom_tree_branch_executor(department: str):
    """创建Pan-Wisdom Tree枝干执行器"""
    def executor(task: str, **kwargs) -> Dict[str, Any]:
        # 这里就是"import ClawSystem 并 ask"的实现位置
        from ..claws._claw_engine import ClawIndependentWorker
        from ..claws._claw_architect import ClawArchitect
        
        architect = ClawArchitect()
        claw = architect.get_claw_by_department(department)
        
        result = await claw.process(query=task)
        return result
    
    return executor
```

---

## 安全约束与调用权限

### 核心铁律

| 约束 | 实现 | 说明 |
|------|------|------|
| **B不能调A** | `validate_call_direction("B", "A")` 返回False | 铁律，不可绕过 |
| **只能A调B** | `direct_department_call(caller="A", ...)` | 只有A可以发起直接调用 |
| **必须回报** | `callback(task_id, result)` | B轨执行完必须通知A轨 |

### 神行轨调用权限（特权机制）

**神行轨的调用是 DivineReason 和 Pan-Wisdom Tree 的特权。**

| 调用方 | 调用权限 | 约束 |
|--------|---------|------|
| **DivineReason** | ✅ 有权调用 | 仅允许各**节点**跳过调度器调用神行轨 |
| **Pan-Wisdom Tree** | ✅ 有权调用 | 仅允许各**枝丫（末端）**跳过调度器调用神行轨 |
| **A神政轨** | ✅ 有权调用 | 通过 TrackBridge 派发任务 |
| **其他维度/板块** | ❌ 禁止 | 无法直接调用神行轨 |

### Claw 独立性

每个贤者 Claw 都是**独立个体**：

| 特性 | 说明 |
|------|------|
| **独立思考** | Claw 能自主推理、论证、答疑 |
| **独立工作** | 无需外部指令即可完成分配的任务 |
| **职场定位** | 神行轨的 Claws 是干活的、是系统内的职场牛马 |
| **直接调用** | 可根据需求跳过多余环节，直接调用目标团队或 Claw |

### 知识访问权限

| 知识源 | 神行轨权限 | 说明 |
|--------|-----------|------|
| **DomainNexus** | ✅ 可访问 | 直接获取相关知识 |
| **藏书阁（皇家藏书阁）** | ❌ 禁止访问 | 独立记忆体系，执行层不可触达 |

---

## 测试结果

```
============================================================
双轨架构简单测试
============================================================
  ✓ 导入模块: PASS
  ✓ 创建双轨系统: PASS
  ✓ A轨调用B轨: PASS
  ✓ 直接部门调用: PASS
  ✓ B轨不能调用A轨: PASS

总计: 5/5 通过 ✅
```

---

## 与现有系统的关系

| 现有组件 | 在双轨中的角色 |
|---------|--------------|
| **DivineReason V4.0** | A轨的核心推理引擎 |
| **Pan-Wisdom Tree V1.0** | A轨的学派推理系统 |
| **SageDispatch (12个调度器)** | A轨的任务调度层 |
| **ClawSystem (763个Claw)** | B轨的执行单元 |
| **11部门路由系统** | B轨的直接调用目标 |

---

## 版本历史

- **v2.0** (2026-04-28): 全面重构，落地可运行
  - B轨各部门执行器接入真实 DivineReason 推理引擎（不再返回假数据）
  - B轨接入 DomainNexus 知识系统（KnowledgeAccessLayer）
  - 完善调用权限校验：CallerType 枚举 + validate_caller() 方法
  - 新增 DivineReason / Pan-Wisdom Tree 特权调用入口
  - 修复 ClawArchitect/ClawIndependentWorker 接口调用错误
  - 修复 track_a.py ReasoningResponse 字段映射（使用 ProblemAnalyzer 独立获取）
  - 新增 test_dual_track_v2.py 14项集成测试（14/14 通过）
  - 藏书阁访问拒绝机制实现
  - 向后兼容接口保留（create_wisdom_tree_branch_executor）
- **v1.1** (2026-04-28): 调用权限体系完善
  - 明确神行轨调用权限：DivineReason(节点) / Pan-Wisdom Tree(枝丫) / A神政轨
  - 新增知识访问权限：DomainNexus ✅ / 藏书阁 ❌
  - Claw独立性定义：每个Claw是独立个体，可思考/论证/答疑
  - 其他维度和板块禁止直接调用神行轨
- **v1.0** (2026-04-28): 初始实现
  - A轨(神政轨) + B轨(神行轨)
  - TrackBridge桥接器
  - 直接部门调用机制
  - 5/5测试通过
