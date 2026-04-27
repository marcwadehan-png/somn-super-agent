# GlobalClawScheduler 集成报告

**版本**: v1.0.0  
**日期**: 2026-04-23  
**状态**: 完成 ✅  
**测试**: 40/40 PASS (1.04s)

---

## 一、需求概述

将Claw任职体系（763个贤者Claw→422岗位）写入代码全局，与系统全局代码打通，实现四大核心能力：

1. **全局调动** — 从SomnCore统一调度任意Claw，支持ProblemType/Department/School/Name四种路由策略
2. **分布式工作** — 任务队列+工作池+信号量并发控制，批量并发分发
3. **独立工作** — 单Claw ReAct闭环自主执行，完整生命周期管理
4. **协作工作** — 多Claw角色分工（PRIMARY/CONTRIBUTOR/ADVISOR/REVIEWER）+结果聚合

---

## 二、架构设计

### 2.1 核心模块

```
GlobalClawScheduler (_global_claw_scheduler.py, ~1350行)
│
├── ClawRouter          — 776个Claw路由索引（by PT/Department/Query/Name）
├── ClawsCoordinator    — Claw实例管理+懒加载（by School/Name）
├── ClawSystemBridge    — Somn主系统桥接（4级集成）
├── CollaborationProtocol — 跨部门多Claw协作协议（角色分工+结果聚合）
└── CourtPositionRegistry — 422岗位×763任职映射
```

### 2.2 数据结构

| 结构 | 用途 |
|------|------|
| `TaskTicket` | 任务票据：task_id, query, target_claw, mode, priority, collaborators, problem_type, department, wisdom_school, 结果字段 |
| `DispatchMode` | 调度模式枚举：SINGLE / COLLABORATIVE / DISTRIBUTED / AUTO |
| `TaskPriority` | 优先级枚举：CRITICAL(0) > HIGH(1) > NORMAL(2) > LOW(3) > BACKGROUND(4) |
| `ClawWorkMode` | 工作模式枚举：INDEPENDENT / PRIMARY / CONTRIBUTOR / ADVISOR / REVIEWER |
| `SchedulerStats` | 调度器统计：total_dispatched/completed/failed/collaborative/distributed/single, avg_response_time, claw_usage_counts |
| `WorkPoolStatus` | 工作池状态：total_claws, departments, schools, top_busy |

### 2.3 核心接口

#### 全局调度入口

```python
ticket = await scheduler.dispatch(TaskTicket.create("什么是仁？"))
# 自动路由 → 选择最优Claw → 选择最优执行模式（独立/协作）
```

#### 独立工作

```python
ticket = await scheduler.dispatch_single("孔子", "什么是仁？")
# ReAct闭环 → ClawArchitect.process() → 结果返回
```

#### 协作工作

```python
ticket = await scheduler.dispatch_collaborative(
    "如何治理国家", ["孔子", "管仲", "韩非子"],
    roles={"孔子": ClawWorkMode.PRIMARY, "管仲": ClawWorkMode.CONTRIBUTOR}
)
# CollaborationProtocol → 角色分工执行 → 结果聚合
```

#### 分布式工作

```python
tickets = await scheduler.dispatch_distributed([
    TaskTicket.create("什么是仁？"),
    TaskTicket.create("什么是道？"),
    TaskTicket.create("什么是法？"),
])
# 优先级排序 → semaphore并发控制 → 独立超时保护 → 批次超时保护
```

#### 全局调动路由

```python
# 按ProblemType路由
await scheduler.dispatch_to_problem_type("COMPETITION", "如何应对竞争")

# 按部门路由
await scheduler.dispatch_to_department("礼部", "什么是仁？")

# 按学派路由
await scheduler.dispatch_to_school("道家", "什么是无为")

# 直接指定Claw
await scheduler.dispatch_to_claw("韩非子", "什么是法？")
```

#### 快捷同步函数

```python
ticket = quick_dispatch("什么是仁？", claw_name="孔子")
# 非async环境下的同步包装器
```

### 2.4 自动路由策略（dispatch → _auto_dispatch）

```
Ticket输入
│
├── 有 problem_type? → ClawRouter.route_by_problem_type() → 部门内最优Claw
│   └── 有 collaborator_claws? → 升级协作模式
│
├── 有 department? → ClawRouter.route_by_department() → 部门内最优Claw
│
├── 有 wisdom_school? → ClawsCoordinator.find_by_school() → 学派首Claw
│
├── 默认 → ClawRouter.route_by_query() → 智能匹配最优Claw
│
└── 兜底 → Coordinator.gateway.route() → 孔子（终极兜底）
```

---

## 三、系统集成

### 3.1 修改文件清单

| 文件 | 变更类型 | 说明 |
|------|---------|------|
| `src/intelligence/claws/_global_claw_scheduler.py` | **新增** | 核心调度器模块（~1350行） |
| `src/core/somn_core.py` | 修改 | 添加global_claw_scheduler属性 + _ensure方法 + 系统状态 |
| `src/core/_somn_ensure.py` | 修改 | 添加ensure_global_claw_scheduler函数 |
| `src/intelligence/claws/__init__.py` | 修改 | 导出GlobalClawScheduler及相关类型 |
| `tests/test_global_claw_scheduler.py` | **新增** | 测试套件（40个用例） |

### 3.2 SomnCore集成点

```
SomnCore
│
├── __init__(): _global_claw_scheduler = None
│
├── _ensure_global_claw_scheduler():
│   └── 委托到 _somn_ensure.ensure_global_claw_scheduler(self)
│
├── global_claw_scheduler (属性):
│   ├── _ensure_global_claw_scheduler()  # 懒加载
│   └── return self._global_claw_scheduler
│
└── get_system_status():
    └── global_claw_scheduler_loaded: bool
        ├── pool_status: WorkPoolStatus
        └── stats: {total_dispatched, total_completed, total_failed}
```

### 3.3 _somn_ensure集成

```python
def ensure_global_claw_scheduler(self):
    """三级初始化策略"""
    if self._global_claw_scheduler_initialized:
        return  # 已初始化
    if self._global_claw_scheduler is not None:
        return  # 异步初始化进行中或已完成
    _init_global_claw_scheduler(self)  # 同步初始化（仅创建实例）
```

### 3.4 包导出链路

```
src/intelligence/claws/__init__.py
    └── GlobalClawScheduler, TaskTicket, DispatchMode, ClawWorkMode,
        get_global_claw_scheduler, quick_dispatch
```

---

## 四、分布式工作实现细节

### 4.1 并发控制

```python
async def dispatch_distributed(tickets, max_concurrent=None, timeout_per_item=None):
    sem = asyncio.Semaphore(actual_max_concurrent)  # 信号量控制
    
    async def _process_one(ticket):
        async with sem:  # 并发限流
            return await asyncio.wait_for(self.dispatch(ticket), timeout)
    
    tasks = [asyncio.create_task(_process_one(t)) for t in sorted_tickets]
    done, pending = await asyncio.wait(tasks, timeout=BATCH_TIMEOUT)
```

### 4.2 结果收集

通过 `task_ticket_map: Dict[asyncio.Task, str]` 建立异步Task与Ticket的映射，从`done`集合正确收集结果并保持原始顺序返回。

### 4.3 保护机制

| 层级 | 机制 | 默认值 |
|------|------|--------|
| 单Claw | SINGLE_TIMEOUT | 120s |
| 协作 | COLLABORATIVE_TIMEOUT | 300s |
| 分布式单项 | CLAW_PER_ITEM_TIMEOUT | 90s |
| 分布式批次 | DISTRIBUTED_BATCH_TIMEOUT | 600s |
| 并发数 | MAX_CONCURRENT_LIMIT | 20 |

---

## 五、Bug修复历史

| # | 问题 | 严重性 | 修复方案 |
|---|------|--------|---------|
| 1 | 测试中`side_effect=asyncio.sleep(10)`返回coroutine对象，被wait_for直接消费导致不超时 | P1 | 改用真实async函数 |
| 2 | `dispatch_distributed._process_one`获取sem → `dispatch` → `dispatch_single`再次获取同一个semaphore，死锁 | P0 | 从dispatch_single和dispatch_collaborative_from_ticket移除semaphore，并发控制统一由调用方管理 |
| 3 | `_auto_dispatch`检测到有collaborators即升级协作模式，但`_collaboration_protocol`可能为None | P1 | 添加`and self._collaboration_protocol`条件检查 |
| 4 | `dispatch`入口调用`dispatch_collaborative_from_ticket`，但total_collaborative计数在`dispatch_collaborative`中递增，从ticket入口调用时计数遗漏 | P2 | 在`dispatch_collaborative_from_ticket`开头添加`self._stats.total_collaborative += 1` |
| 5 | `asyncio.wait`返回的`done`集合是`Set[asyncio.Task]`，原代码错误访问`t.task_id`（Task无此属性） | P0 | 建立`task_ticket_map`映射表，通过task→ticket_id正确关联结果 |

---

## 六、测试验证

### 6.1 测试覆盖

| 测试类 | 用例数 | 覆盖能力 |
|--------|--------|---------|
| TestDataStructures | 7 | 数据结构定义正确性 |
| TestSchedulerInitialization | 4 | 初始化+单例+参数限制 |
| TestIndependentWork | 4 | 单Claw执行+超时+Bridge回退 |
| TestCollaborativeWork | 3 | 协作调度+角色分配+参数校验 |
| TestDistributedWork | 4 | 批量分发+失败处理+优先级排序 |
| TestGlobalRouting | 5 | 四种路由策略+自动路由 |
| TestMonitoring | 6 | 统计+工作池+Claw列表+活跃任务+最近结果+协作发现 |
| TestLifecycle | 2 | 关闭+回调注册 |
| TestDispatchEntry | 2 | AUTO模式+COLLABORATIVE模式 |
| TestModuleImports | 2 | 模块导入+包导出 |
| TestQuickDispatch | 1 | 快捷同步调度 |
| **合计** | **40** | |

### 6.2 运行结果

```
40 passed in 1.04s
0 lint errors
```

---

## 七、后续优化方向

1. **持久化队列**：分布式工作目前是内存队列，可扩展为Redis持久化队列
2. **负载均衡**：基于Claw使用频率和历史响应时间进行智能负载均衡
3. **断路器模式**：对频繁失败的Claw自动熔断，避免资源浪费
4. **结果缓存**：相似查询的缓存机制，减少重复计算
5. **实时监控面板**：WebSocket推送调度器状态到前端
6. **Claw预热策略**：基于历史使用模式预测性加载高频Claw

---

## 八、文件索引

| 文件 | 路径 |
|------|------|
| 核心模块 | `smart_office_assistant/src/intelligence/claws/_global_claw_scheduler.py` |
| 测试套件 | `smart_office_assistant/tests/test_global_claw_scheduler.py` |
| SomnCore集成 | `smart_office_assistant/src/core/somn_core.py` |
| 初始化函数 | `smart_office_assistant/src/core/_somn_ensure.py` |
| 包导出 | `smart_office_assistant/src/intelligence/claws/__init__.py` |
| 本报告 | `file/系统文件/GlobalClawScheduler集成报告.md` |
