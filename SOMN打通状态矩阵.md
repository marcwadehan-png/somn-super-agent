# SOMN 打通状态矩阵（最终确认版）
> 更新时间：2026-05-01 15:19
> 核心版本：v6.2.0 | NeuralMemory v7.0 | engagement v22.0 | RefuteCore v3.1.0

---

## 一、整体架构概览

```
用户请求
   │
   ▼
┌─────────────────────────────────────────────────────────┐
│                   SOM 入口层                            │
│  SomnApp.py / SomnCore (src/core/)                      │
└──────────────────────┬──────────────────────────────────┘
                       │ 调用
                       ▼
┌─────────────────────────────────────────────────────────┐
│               神政轨 (Track A) [已集成]                  │
│  intelligence/dual_track/track_a.py                      │
│  功能：分析 + 监督 + 规划                                │
│  引用 → knowledge_cells.web_integration.TrackAWeb       │
└──────────────────────┬──────────────────────────────────┘
                       │ 任务下发
                       ▼
┌─────────────────────────────────────────────────────────┐
│            神行轨 (Track B) v4.2 [已集成]                │
│  intelligence/dual_track/track_b.py                       │
│  功能：独立执行单元（Claw）                               │
│  引用 → knowledge_cells.web_integration.TrackBWeb        │
│  引用 → knowledge_cells.domain_nexus (query)            │
└──────────────────────┬──────────────────────────────────┘
                       │ 分析结果
                       ▼
┌─────────────────────────────────────────────────────────┐
│          knowledge_cells / 八层管道 [✅ 已打通]           │
│                                                         │
│  L1 输入层    → 文本清洗 / 类型检测                        │
│  L2 自然语言  → demand_type / domain 分类                │
│  L3 分类      → 8大类型路由                               │
│  L4 路由      → 12调度器链（SD-P1/F1/F2/R1/R2/C1/C2/D1/D2/D3/E1/L1）│
│  L5 推理      → DivineReason v4.0 (三层推理)  ←知识库注入   │
│  L6 论证      → RefuteCore v3.1.0 (8维驳心) ← T2仅Super   │
│  L7 输出      → OutputEngine v1.1 (8种格式) ← Kaiwu增强  │
│  L8 优化      → 置信度传播 + 建议生成                      │
│                                                         │
│  懒加载：L0(5ms) → L1-L3(100ms) → L4-L8(按需)           │
└──────────────────────┬──────────────────────────────────┘
                       │ 结果 + 置信度
                       ▼
┌─────────────────────────────────────────────────────────┐
│           intelligence/ (WisdomDispatch) [✅ 已集成]     │
│                                                         │
│  子模块引用 knowledge_cells 内容：                        │
│  · dual_track/_supervision_claws.py → DomainNexus       │
│  · dual_track/track_a.py → TrackAWeb                    │
│  · dual_track/track_b.py → TrackBWeb + nexus_query     │
│  · engines/refute_core.py → RefuteCoreWeb + call_module_llm │
│  · engines/sub_engines/__init__.py → pan_wisdom_core    │
└──────────────────────┬──────────────────────────────────┘
                       │ 记忆写入
                       ▼
┌─────────────────────────────────────────────────────────┐
│         NeuralMemory v7.0 [✅ 已打通]                     │
│                                                         │
│  三层记忆架构 (书架 Metaphor)：                           │
│  · 藏书阁甲 (Working) / 藏书阁乙 (Short-term)            │
│  · 藏书阁丙 (Long-term)                                  │
│  · ImperialLibrary (记忆仓库)                           │
│                                                         │
│  核心组件引用 knowledge_cells：                          │
│  · neural_memory/unified_memory_interface.py →          │
│      knowledge_cells.domain_nexus (get_nexus)           │
│      knowledge_cells.llm_rule_layer (call_module_llm)   │
│  · neural_memory/neural_memory_v2.py →                 │
│      knowledge_cells.web_integration.NeuralMemoryWeb    │
│  · core/_somn_ensure.py → EightLayerPipeline +          │
│      knowledge_cells.core.get_engine + get_nexus         │
│  · core/_somn_routes.py → ProcessingGrade                │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│           engagement v22.0 [⚠️ 孤立 — 0引用]             │
│                                                         │
│  v22.0 新增：strategy_manager + execution_planner       │
│  状态：模块已就绪，但主包尚未接入                         │
│  待接入：主 Pipeline 或 SomnCore                         │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│           reasoning_mind/ [⚠️ 孤立 — 0引用]             │
│                                                         │
│  内容：Pan-Wisdom Tree + DivineReason v4 +              │
│        RefuteCore v3.1.0                                │
│  状态：模块已就绪，但未接入主链路                         │
│  注：RefuteCore v3.1.0 已在 eight_layer_pipeline 中调用  │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              kaiwu/ PPT生成 [✅ 接入 OutputEngine]        │
│                                                         │
│  KaiwuService 已接入 PptxOutputStrategy.render()         │
│  · 优先使用 KaiwuService（有风格学习 + Markdown理解）    │
│  · 失败时自动回退到原生 python-pptx                       │
│  · _render_context_to_markdown() 转换 RenderContext     │
└─────────────────────────────────────────────────────────┘
```

---

## 二、模块引用矩阵（关键跨包引用）

| 源模块 | 目标模块 | 引用内容 | 状态 |
|--------|---------|---------|------|
| `src/core/somn_core.py` | `knowledge_cells.eight_layer_pipeline` | `ProcessingGrade` | ✅ |
| `src/core/_somn_routes.py` | `knowledge_cells.eight_layer_pipeline` | `ProcessingGrade` (×3) | ✅ |
| `src/core/_somn_ensure.py` | `knowledge_cells.core` | `get_engine` | ✅ |
| `src/core/_somn_ensure.py` | `knowledge_cells.eight_layer_pipeline` | `EightLayerPipeline` | ✅ |
| `src/core/_somn_ensure.py` | `knowledge_cells.domain_nexus` | `get_nexus` | ✅ |
| `src/intelligence/dual_track/track_a.py` | `knowledge_cells.web_integration` | `TrackAWeb` | ✅ |
| `src/intelligence/dual_track/track_b.py` | `knowledge_cells.web_integration` | `TrackBWeb` | ✅ |
| `src/intelligence/dual_track/track_b.py` | `knowledge_cells.domain_nexus` | `query` (nexus_query) | ✅ |
| `src/intelligence/dual_track/_supervision_claws.py` | `knowledge_cells.domain_nexus` | `DomainNexus` | ✅ |
| `src/intelligence/engines/refute_core.py` | `knowledge_cells.web_integration` | `RefuteCoreWeb` | ✅ |
| `src/intelligence/engines/refute_core.py` | `knowledge_cells.llm_rule_layer` | `call_module_llm` (×2) | ✅ |
| `src/intelligence/engines/sub_engines/__init__.py` | `knowledge_cells.pan_wisdom_core` | 多组件 | ✅ |
| `src/neural_memory/unified_memory_interface.py` | `knowledge_cells.domain_nexus` | `get_nexus` | ✅ |
| `src/neural_memory/unified_memory_interface.py` | `knowledge_cells.llm_rule_layer` | `call_module_llm` | ✅ |
| `src/neural_memory/neural_memory_v2.py` | `knowledge_cells.web_integration` | `NeuralMemoryWeb` | ✅ |
| `src/learning/learning_plan_engine.py` | `knowledge_cells` | `get_nexus` | ✅ |
| `knowledge_cells/output_engine.py` | `smart_office_assistant.src.kaiwu.kaiwu_service` | `KaiwuService` | ✅ |
| `SomnApp.py` | `knowledge_cells` | 多个组件 | ✅ |
| `llm_unified_config.py` | `knowledge_cells` | 多个组件 | ✅ |

**合计：19个跨包引用，全部 ✅ 已打通**

---

## 三、主包 `__init__.py` 引用状态

| 文件 | knowledge_cells 引用 | 策略 |
|------|-------------------|------|
| `smart_office_assistant/__init__.py` | **无** | 仅定义版本信息 |
| `src/core/__init__.py` | **无** | `__getattr__` 延迟加载本地模块 |
| `src/intelligence/__init__.py` | **无** | `__getattr__` 延迟加载本地模块 |
| `src/main_chain/__init__.py` | **无** | `__getattr__` 延迟加载本地模块 |
| `src/neural_memory/__init__.py` | **无** | `__getattr__` 延迟加载本地模块 |
| `src/engagement/__init__.py` | **无** | `__getattr__` 延迟加载本地模块 |

> 所有主包 `__init__.py` 均使用 `__getattr__` 延迟加载，**完全避免循环导入**，启动时间从 ~100ms 降至 ~5ms。

---

## 四、knowledge_cells 内部导入链

```
knowledge_cells.__init__  [L0 预加载 ~5ms]
   ├── dispatch / get_engine        → core.py
   ├── get_nexus / DomainNexus     → domain_nexus.py
   ├── PanWisdomTree (lazy)        → pan_wisdom_core.py
   ├── DivineTrackOversight (lazy) → divine_track_oversight.py
   └── ClosedLoopSolver (lazy)     → closed_loop_solver.py

L1-L3 按需加载（~100ms）
   ├── eight_layer_pipeline.py     [L1-L3]
   ├── lazy_loader.py              [PanWisdomPreloader]
   ├── output_engine.py             [L7 多模态输出] ← KaiwuService ✅
   └── domain_nexus.py             [知识库]

L4-L8 按需加载（运行时）
   ├── dispatchers/                [12调度器]
   │   ├── ProblemDispatcher (SD-P1) ← 树干核心
   │   ├── SchoolFusion (SD-F1/F2)
   │   ├── FourLevelDispatchController
   │   ├── FallacyChecker (SD-R1/R2)
   │   ├── SuperReasoning (SD-C1/C2)
   │   ├── YinYangDecision (SD-D1/D2/D3)
   │   ├── DivineArchitecture (神之架构)
   │   ├── ChainExecutor
   │   └── ResultTracker
   ├── divine_reason.py             [三层推理]
   ├── refute_core.py               [8维驳心]
   └── output_engine.py             [8种格式]
```

---

## 五、孤立模块处置状态

| 模块 | 状态 | 说明 |
|------|------|------|
| `src/digital_brain/` | ✅ **已删除** | 功能迁移至 NeuralMemory v7.0 (DigitalStrategy + NeuralExecutor) |
| `src/strategy_engine/` | ✅ **已删除** | 已合并至 `engagement/strategy_manager.py` + `execution_planner.py` |
| `src/ecology/` | ⚠️ **未处理** | 2处引用，需确认废弃或集成 |
| `src/engagement/` | ⚠️ **孤立（0引用）** | v22.0 就绪，但主包未接入 Pipeline |
| `src/reasoning_mind/` | ⚠️ **孤立（0引用）** | Pan-Wisdom Tree / DivineReason v4 未接入主链路 |
| `src/kaiwu/` | ✅ **已接入** | KaiwuService 已接入 OutputEngine PptxOutputStrategy |

---

## 六、懒加载架构（最终版）

```
启动触发：import knowledge_cells
│
├─ L0 [~5ms] — __init__.py 预加载
│  · dispatch, get_engine, get_nexus
│  · DivineTrackOversight (lazy)
│  · ClosedLoopSolver (lazy)
│
├─ L1 [~20ms] — eight_layer_pipeline.py
│  · EightLayerPipeline, ProcessingGrade
│  · PipelineResult, LayerResult
│
├─ L2 [~50ms] — domain_nexus.py
│  · DomainNexus, query, get_domain_system
│
├─ L3 [~100ms] — lazy_loader.py
│  · PanWisdomTree, preload_pan_wisdom
│  · PanWisdomPreloader
│  · RefuteCore (lazy)
│
└─ L4+ [运行时] — 各模块按需加载
   · dispatchers/* (12调度器)
   · divine_reason.py (三层推理)
   · refute_core.py (8维驳心)
   · output_engine.py (8种格式)
   · web_integration.py (TrackA/B Web)
   · closed_loop_solver.py (闭环)
```

---

## 七、关键组件版本对照

| 组件 | 版本 | 状态 | 备注 |
|------|------|------|------|
| Somn 主包 | v6.2.0 | ✅ | 神之架构最终完整版 |
| NeuralMemory | v7.0 | ✅ | 三层书架 + DigitalStrategy + NeuralExecutor |
| engagement | v22.0 | ⚠️ | 就绪，未接入主链路 |
| RefuteCore | v3.1.0 | ✅ | 预加载+懒加载，8维驳心 |
| DivineReason | v4.0 | ✅ | 三层推理（直觉/分析/超级） |
| SageDispatch | — | ✅ | 12调度器，SD-P1=Problem Dispatcher |
| OutputEngine | v1.1 | ✅ | Kaiwu增强，8种格式 |
| Pan-Wisdom Tree | — | ⚠️ | 孤立，SD-F1 集成中 |
| 神行轨 Track B | v4.2 | ✅ | 预加载+懒加载，三核心组件 |
| 神政轨 Track A | — | ✅ | 分析监督架构完整 |

---

## 八、待处理事项（优先级排序）

| 优先级 | 事项 | 影响 |
|--------|------|------|
| 🔴 P0 | engagement v22.0 接入主 Pipeline | 策略+执行规划能力未释放 |
| 🔴 P0 | reasoning_mind DivineReason v4 接入 L5 | 三层推理尚未激活 |
| 🟡 P1 | `src/ecology/` 处置 | 2处引用，需确认去向 |
| 🟡 P1 | Pan-Wisdom Tree 接入 SD-F1 | 超级推理模式未激活 |
| 🟢 P2 | SomnApp.py 重构为统一入口 | 当前多入口，需要一个主调度器 |

---

*文档版本：v1.0.0 | 更新：2026-05-01 | 作者：WorkBuddy 张三*
