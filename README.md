<div align="center">

# Somn (索姆) — AI 认知操作系统

**不只是 Agent，是一个能思考、能论证、能进化的认知体系**

[![Version](https://img.shields.io/badge/version-v7.1-blue)]()
[![License](https://img.shields.io/badge/license-AGPL%20v3-blue)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-green)]()
[![Tests](https://img.shields.io/badge/E2E-25%2F25%20passed-brightgreen)]()

</div>

---

## 一句话介绍

Somn 融合了 862 位东西方贤者的智慧体系（儒/道/佛/法/兵/墨/心理学/经济学/博弈论等 42 学派），构建了一套**多维度结构化论证 → 深度推理 → 知识融合 → 记忆进化 → 自主执行**的完整认知管线，让 AI 不只是"回答问题"，而是真正"思考问题"。

---

## 与市面 Agent 框架的核心差异
| 维度 | 主流 Agent 框架 (AutoGPT/LangGraph/CrewAI) | Somn 差异化实现 | 涉及核心模块 |
|------|--------------------------------------------|-------------------------------|----------------|
| **推理方式** | 单链 ReAct：思考→行动→观察→循环 | **天枢八层管道**：L1→L2→L3→L4→L5→L6→L7→L8，论证不合格回退重做（最多3轮） | EightLayerPipeline, SageDispatch |
| **"思考"深度** | Prompt 驱动，依赖 LLM 自身能力 | **DivineReason 三层推理**：SD-D1表层模式匹配→SD-D2深度假设探索→SD-D3元认知自我审视 | SD-D1/SD-D2/SD-D3, DivineReason |
| **论证能力** | 无专门论证模块 | **RefuteCore 驳心引擎**：8维论证（感性/人性/驳斥/社交/逆向/暗森林/行为），自动找漏洞并修复 | RefuteCore v3.2, SD-R2谬误检测 |
| **知识体系** | RAG + Vector DB | **21格动态知识网 + PanWisdomTree**：DomainNexus知识域自动丰富，发现缺口后智能迭代 | DomainNexus, PanWisdomTree, 42学派引擎 |
| **记忆机制** | 短期对话窗口 + 外部存储 | **NeuralMemory v7 五层神经记忆**：感知→工作→短期(7天TTL)→长期→永恒 + Hebbian学习 | NeuralMemory v7, MemoryEncoder |
| **执行架构** | 单 Agent 或简单编排 | **双轨制**：A轨(神政轨)推理决策，B轨(神行轨)执行，763个独立Claw各司其职 | TrackA, TrackB, 763 Claw |
| **智慧多样性** | 单一推理路径 | **166+子推理引擎 + 42学派并行推理 + 融合决策**，儒/道/法/兵/墨/经济等42个角度分析 | PanWisdomTree, 165 ProblemType |
| **监管机制** | 无 | **SD-R1三层推理监管**：感知层→认知层→元认知层，元认知不通过=整体不合规 | SD-R1 ThreeLayerReasoning |
| **调度系统** | 硬编码路由 | **SageDispatch 12调度器**：SD-P1问题调度/SD-F1+SD-F2四级总控/SD-C1阴阳决策/SD-C2神之架构/SD-E1执行/SD-L1结果追踪 | SageDispatch, DispatcherCore |

### 用一个例子说明差异（附详细子系统调用链）

**用户问**："公司要不要做直播？"

| 框架 | 回答方式 | 调用的核心子系统 |
|------|---------|----------------|
| **主流 Agent** | 搜索直播行业数据 → 整理 pros/cons → 给建议 | WebSearch → 单次LLM调用 |
| **Somn** | ① L2意图识别 → L3匹配B2直播格子 → L4分流(SD-P1→SD-F2→SD-R1) → L5推理(DomainNexus→SD-C1阴阳→PanWisdomTree→SD-D2) → L6论证(SD-R2谬误检测→RefuteCore 8���) → L7输出结构化建议 | 14个真实子系统按序调用 |

### Somn 的差异化核心价值

**1. 不是"回答问题"，是"思考问题"**
- 主流Agent：你问直播，它搜直播数据，给你建议
- Somn：你问直播，它分析你的竞争态势(兵家) + 合规风险(法家) + 品牌调性(儒家) + 成本效率(墨家) + 市场逻辑(经济学) → 42学派融合推理 → 论证回退验证 → 给你有论证支撑的决策

**2. 不是"单链推理"，是"八层管道 + 回退机制"**
- 主流Agent：一次推理链，错了就是错了
- Somn：L6论证不合格 → 携带结构化反馈返回L4修正式重分流 → 最多3轮，确保输出质量

**3. 不是"单一视角"，是"42学派并行 + 融合决策"**
- 主流Agent：单一LLM视角
- Somn：兵家看竞争、法家看合规、墨家看效率、儒家看调性、阴阳家看平衡... → 融合42学派智慧 → 输出多维决策建议

**4. 不是"简单记忆"，是"五层神经记忆"**
- 主流Agent：对话窗口 + 外部存储
- Somn：感知记忆(即时) → 工作记忆(当前上下文) → 短期记忆(7天TTL自动衰减) → 长期记忆(持久化) → 永恒记忆(核心知识)，Hebbian学习强化高频记忆
---

## 核心架构详解（天枢 TianShu 八层管道三级调用链全展开）

### 全局入口：SomnCore 主链路（双阶段处理）

用户请求进入系统后，由 `SomnCore.run_agent_task()` 主链路统一处理，分为**分析阶段**和**路由阶段**：

```
用户请求
  │
  ├─ 分析阶段（analyze_requirement）
  │   ├─ 快车道检测 → 简单问候/致谢等，直接返回，跳过完整链路
  │   ├─ 超时守护初始化 → TimeoutGuard（120s全局 / 240s任务级）
  │   ├─ 语义理解层 → SemanticMemoryEngine 意图推理
  │   ├─ Phase1 三路并行 ─┬─ LLM解析 (_module_parse_requirement → LLMService)
  │   │                   ├─ 网络搜索 (WebSearchEngine，3s超时)
  │   │                   └─ 记忆查询 (NeuralMemory → _query_memory_context)
  │   ├─ 人设场景识别 → SomnPersona.generate_voice_output()
  │   └─ Phase2 四路fan-out ─┬─ 智慧分析 → SuperWisdomCoordinator.analyze()
  │                          ├─ 形而上学 → _maybe_run_metaphysics_analysis()
  │                          ├─ 可行性评估 → _module_assess_feasibility()
  │                          └─ 路由决策 → _module_assess_task_routing()
  │
  └─ 路由阶段（9条路由，根据 Phase2 决策结果选择一条执行）
      ├─ 路由A：SomnOrchestrator 编排（FAST/HOME/FEAST三种模式）
      ├─ 路由B：本地LLM直答（A/B双模型左右大脑调度，含降级）
      ├─ 路由C：智慧板块直答（SuperWisdomCoordinator 多学派融合）
      ├─ 路由D：完整工作流（策略设计→执行→评估→反思，FEAST模式）
      ├─ 路由E：SageDispatch 贤者调度（12调度器智能分配）
      ├─ 路由F：DivineReason 统一推理（GoT+LongCoT+ToT+ReAct 4合1）
      ├─ 路由G：天枢八层管道 ⭐ 核心路由，下文展开
      ├─ 路由PPT：SlideForge 幻灯片生成（KaiwuService）
      └─ 路由NL：NeuralLayout 神经网络布局全链路
```

其中**路由G（天枢八层管道）**是系统最核心的深度处理通道，下文逐层展开其三级调用链。

---

### 八层智慧管道（天枢 TianShu）— 三级调用链全展开

天枢管道是 Somn 的"大脑皮层"。一个用户问题进入管道后，每一层都会调用真实的子系统模块协同工作。以下按**「层 → 调用板块 → 板块内部实现」**三级展开。

> 三种处理等级：**BASIC**（快速响应）→ **DEEP**（深度分析）→ **SUPER**（全链路极致推理），等级越高，调用越多子系统。

---

#### L1 输入层 — InputLayer

| 级别 | 说明 |
|------|------|
| **做什么** | 接收原始输入，执行基础文本清洗和标准化 |
| **调用板块** | 无外部依赖，纯本地处理 |
| **内部实现** | ① 空输入检测与拦截 ② 统一为字符串（支持str/dict/Any） ③ 正则预编译词数统计 ④ 输出 `LayerResult(data={cleaned_text, input_type, text_length, word_count})` |

---

#### L2 自然语言需求分析层 — NLAnalysisLayer

| 级别 | 说明 |
|------|------|
| **做什么** | 深度NLP解析用户输入，提取关键信息、识别意图、分类领域 |
| **调用板块** | ① TianShuWebSearch（网络搜索增强） ② LLM规则层（call_module_llm） |
| **内部实现** | |

L2 内部8步处理链：

```
步骤1: 实体提取 → 预编译正则（人名/组织/地点）
步骤2: 时间引用提取 → 7组正则（年/月/日/季度/相对时间）
步骤3: 数量提取 → 5组正则（百分比/大数/金额）
步骤4: 关系提取 → 主语-谓语-宾语三元组
步骤5: 意图识别 → 8类模式匹配（query/analysis/planning/decision/execution/innovation/critique/general）
步骤6: 需求类型判断 → 基于意图分类（战略规划/分析研究/决策评估/执行落地/创新突破/综合需求）
步骤7: 领域分类 → 6大领域+权重关键词（社会科学/文学历史/自然科学/科技/商业/哲学）
步骤8: 网络搜索增强 → TianShuWebSearch.enhance_analysis() 术语解释 + 最新背景知识
```

输出：`{text, entities, time_refs, quantities, relations, intent, demand_type, domain, domain_scores, complexity, urgency, keywords, web_enhancement}`

---

#### L3 分类与引擎推荐层 — ClassificationLayer

| 级别 | 说明 |
|------|------|
| **做什么** | 根据L2分析结果，匹配问题类型 → 推荐SageDispatch调度器组合 → 确定推理深度 |
| **调用板块** | ① 165种ProblemType分类表 ② 21格知识系统（格子路由映射） ③ SageDispatch调度器注册表 |
| **内部实现** | |

L3 内部分类逻辑：

```
输入: L2分析结果 + ProcessingGrade(BASIC/DEEP/SUPER)

步骤1: ProblemType匹配 → 165种问题类型（战略规划/竞品分析/用户增长...）
步骤2: 知识格子路由 → 匹配21格（A1逻辑判断/A2智慧模块...B2直播/C1电商...）
步骤3: 学派推荐 → 42学派引擎权重排序
步骤4: 调度器组合推荐（根据等级调整）:
  ├─ BASIC: SD-P1(问题调度) → SD-F2(四级总控) → SD-E1(执行)
  ├─ DEEP:  + SD-R1(推理监管) + SD-C2(神之架构)
  └─ SUPER: + SD-F1(深度总控) + SD-C1(阴阳决策)
步骤5: 推理深度确定 → light / standard / deep
步骤6: 路由路径构建 → 如 ["SD-P1", "SD-F2", "SD-R1", "SD-C2", "SD-E1"]
```

输出：`{problem_type, knowledge_cells, school_recommendations, primary_engines, secondary_engines, routing_path, reasoning_depth}`

---

#### L4 分流层 — RoutingLayer ⭐ 核心枢纽

| 级别 | 说明 |
|------|------|
| **做什么** | 根据L3推荐的路由路径，**调用真实的SageDispatch调度器链**，将问题分发到正确的推理/决策模块 |
| **调用板块** | ① SageDispatch.DispatchEngine（调度器引擎） ② SD-P1问题分类器 ③ SD-F1/F2四级总控 ④ SD-R1/R2推理监管 ⑤ SD-C1/C2神之架构 ⑥ SD-D1/D2/D3 DivineReason ⑦ SD-E1执行引擎 ⑧ SD-L1结果追踪 |
| **内部实现** | |

L4 三种分流策略（每种都调用真实调度器）：

```
BASIC分流:
  SD-P1(问题分类) → SD-F2(四级总控) → SD-E1(执行)
  产出: 基础分析结论 + 轻量审核

DEEP分流:
  SD-P1(问题分类) → SD-F2(四级总控) → SD-R1(推理监管) → SD-C2(神之架构) → SD-E1(执行)
  + 同步进入神之架构并行处理
  + Claw小组讨论（763贤者中选派）
  产出: 深度分析结论 + 翰林院标准审核

SUPER分流:
  SD-P1(问题分类) → SD-F1(深度总控) + SD-F2(四级总控) → SD-R1+SD-R2(双重监管)
  → SD-C1(太极阴阳决策) + SD-C2(神之架构) → SD-E1(执行)
  + 全量Claw讨论 + 神之架构T2层
  产出: 极致推理结论 + 翰林院三轮严格审核
```

**论证回退机制**：当L6论证层判定不合格时，L4会接收结构化反馈（含谬误详情、维度缺陷、修正提示），进行**修正式重新分流**，而非简单重复。最多重试3次。

---

#### L5 推理层 — ReasoningLayer ⭐ 核心推理

| 级别 | 说明 |
|------|------|
| **做什么** | 调用真实调度器进行**决策推理** + **推理论证** + **监管约束**，并融合知识库和学派智慧 |
| **调用板块** | ① DomainNexus知识库（_query_knowledge_base） ② PanWisdomTree万法智慧树（42学派融合） ③ SD-C1太极阴阳决策 ④ SD-C2神之架构决策 ⑤ SD-D1/D2/D3 DivineReason三层推理 ⑥ SD-R1三层推理监管（感知/认知/元认知） ⑦ 翰林院审核机制 ⑧ TianShuWebSearch推理增强 |
| **内部实现** | |

L5 三种推理策略（每种调用链不同）：

**BASIC推理链（5步）:**
```
Step 1: DomainNexus 知识库查询 → 获取领域知识支撑
Step 2: SD-C2 神之架构决策 (DivineArchitecture) → 综合判断
Step 3: PanWisdomTree 学派融合 → 42学派智慧注入
Step 4: SD-D1 轻量论证 (SuperReasoning-light) → 快速推理验证
Step 5: 翰林院轻量审核 → 不合格返回L4
```

**DEEP推理链（5步）:**
```
Step 1: DomainNexus 知识库查询
Step 2: SD-C1 太极阴阳决策 (YinYangDecision) → 阴阳平衡分析
Step 3: PanWisdomTree 学派融合 → 42学派深度注入
Step 4: SD-D2 标准深度推理 (SuperReasoning-standard) → 假设探索+多角度分析
Step 5: 翰林院标准审核 → 不合格返回L4
```

**SUPER推理链（5步）:**
```
Step 1: DomainNexus 知识库查询
Step 2: SD-C1 + SD-C2 联合神之架构决策 → 太极阴阳+神之架构双重决策
Step 3: PanWisdomTree 学派融合 → 全量42学派极致注入
Step 4: SD-D3 极致深度推理 (SuperReasoning-deep) → 含元认知自我审视
Step 5: 翰林院三轮严格审核 → 不合格返回L4
```

**SD-R1 三层推理监管**（所有等级共享）：
```
SD-R1(ThreeLayerReasoning) 对推理结果施加三层监管约束:
  ├─ 感知层: 问题感知、模式识别、意图理解 → 检查是否遗漏关键信息
  ├─ 认知层: 前提提取、逻辑推理、结论生成 → 检查推理链完整性
  └─ 元认知层: 推理审视、谬误检测、质量评估 → ⚠️ 此层不通过 = 整体不合规
```

---

#### L6 论证层 — ArgumentationLayer ⭐ 自我纠错

| 级别 | 说明 |
|------|------|
| **做什么** | 对L5的推理结论进行**谬误检测**和**反驳论证**，确保输出经得起推敲 |
| **调用板块** | ① SD-R2谬误检测器（FallacyChecker） ② RefuteCore T2 驳心引擎（仅SUPER模式） ③ SD-L1结果追踪器（ResultTracker） ④ NeuralMemory记忆系统 |
| **内部实现** | |

L6 论证处理链：

```
输入: L5推理结论 + 推理链

Step 1: SD-R2 谬误检测论证
  └─ FallacyChecker 检测逻辑谬误:
     ├─ 人身攻击 (ad_hominem)
     ├─ 稻草人谬误 (straw_man)
     ├─ 虚假两难 (false_dilemma)
     ├─ 循环论证 (circular_reasoning)
     └─ 草率概括 (hasty_generalization)
  └─ 输出: 论证评分(A-F) + 谬误清单 + 通过/不通过

Step 2: RefuteCore T2 驳心引擎二次论证（仅SUPER模式）
  └─ 8维度深度反驳:
     ├─ 感性维度 → 捕捉情感诉求
     ├─ 人性维度 → 评估人性可行性
     ├─ 驳斥维度 → 攻击逻辑漏洞
     ├─ 社交维度 → 传播可行性
     ├─ 逆向维度 → 反向验证
     ├─ 暗森林维度 → 博弈风险评估
     ├─ 行为学维度 → 执行偏差分析
     └─ 情绪维度 → 决策质量影响
  └─ 输出: 论证强度(S/A/B/C/?) + 风险等级 + 维度覆盖率 + 关键缺陷

Step 3: 综合判断 → R2通过 AND T2通过 = 全部通过
  └─ 不通过 → 生成结构化反馈(r2_feedback + t2_feedback + corrective_hints)
  └─ 携带反馈返回 L4 分流层修正重试（最多3轮，防死循环）

Step 4: SD-L1 结果追踪 → 记录论证结果，强化学习

Step 5: NeuralMemory 记忆记录 → 论证结果记入五层记忆系统
```

**关键创新**：论证不合格时的反馈不是简单的"fail"，而是包含：
- R2检测到的具体谬误类型和位置
- T2的维度覆盖率和关键缺陷
- 修正提示（"建议加强逻辑论证"/"建议补充更多证据"）
- 累计失败历史（连续失败会触发升级策略）

---

#### L7 输出层 — OutputLayer

| 级别 | 说明 |
|------|------|
| **做什么** | 整合所有层级结果，生成结构化最终答案 |
| **调用板块** | ① OutputEngine多模态输出引擎 ② OutputFormatDetector格式检测 ③ 7种输出策略(Text/Markdown/Html/Image/Pdf/Pptx/Docx) |
| **内部实现** | |

```
输入: L1-L6 全部 LayerResult

步骤1: 提取核心信息 → 原文/分析/路由/推理/论证数据
步骤2: 构建最终答案 → _build_final_answer() 整合各层结论
步骤3: 格式检测 → OutputFormatDetector 自动检测最佳输出格式
步骤4: 多模态渲染 → OutputEngine 选择对应策略渲染
步骤5: 置信度汇总 → 加权平均各层置信度
步骤6: 链路追踪 → 输出完整处理路径和耗时
```

---

#### L8 优化层 — OptimizationLayer

| 级别 | 说明 |
|------|------|
| **做什么** | 基于本次处理结果，分析瓶颈、生成优化建议，持续改进管道效率 |
| **调用板块** | ① 规则分析引擎（快速检测结构性问题） ② LLM动态增强（基于管道结果生成针对性建议） ③ NeuralMemory（优化建议记入记忆） |
| **内部实现** | |

```
输入: PipelineResult (L7输出)

步骤1: 规则分析
  ├─ 瓶颈检测 → 各层耗时分析，标记最慢层
  ├─ 置信度分析 → 标记最低置信度层
  ├─ 路径分析 → 路由路径是否过长(>6步)
  └─ 领域分析 → 领域分类是否过于泛化

步骤2: LLM动态增强 → 基于管道结果生成针对性优化建议

步骤3: 输出优化建议列表
  例: "优化推理层性能，当前耗时85.3ms"
      "基础模式置信度偏低，建议升级为深度模式"
      "路由路径过长(7步)，可考虑精简引擎组合"

步骤4: 写入记忆 → 优化建议记入NeuralMemory，影响后续分流决策
```

---

### 天枢管道完整数据流总览

以**DEEP等级**处理「公司要不要做直播」为例：

```
用户输入: "公司要不要做直播"
         │
[L1] InputLayer ──── 文本清洗 → "公司要不要做直播" (21字)
         │
[L2] NLAnalysisLayer ──── 意图=decision, 类型=决策评估, 领域=商业, 关键词=[公司,直播]
         │                    复杂度=medium, 紧急度=normal
         │                    + 网络搜索增强: 直播行业最新数据
         │
[L3] ClassificationLayer ──── ProblemType=商业决策, 知识格子=B2(直播)+B8(招商)
         │                        推荐学派: 儒家/法家/兵家/墨家/经济学
         │                        路由路径: [SD-P1→SD-F2→SD-R1→SD-C2→SD-E1]
         │
[L4] RoutingLayer(DEEP) ──── SD-P1确认分类 → SD-F2四级总控 → SD-R1就绪 → SD-C2神之架构
         │                        + Claw小组讨论(严助/司马迁/鬼谷子...)
         │
[L5] ReasoningLayer(DEEP) ──── ① DomainNexus查询B2直播格子 → 获得直播运营知识
         │                           ② SD-C1太极阴阳决策 → 直播优势(增长)vs劣势(成本)阴阳分析
         │                           ③ PanWisdomTree融合 → 42学派多维注入
         │                           ④ SD-D2标准深度推理 → 假设探索+多角度分析
         │                           ⑤ SD-R1三层监管 → 感知✓ 认知✓ 元认知✓
         │                           ⑥ 翰林院标准审核 → 通过
         │
[L6] ArgumentationLayer ──── ① SD-R2谬误检测 → 论证评分A, 0谬误
         │                       ② SD-L1结果追踪 → 记录
         │                       ③ NeuralMemory → 记忆存档
         │                       → 全部通过，无需回退
         │
[L7] OutputLayer ──── 格式=Markdown, 结构化答案生成
         │                  置信度=0.82, 总耗时=1.2s
         │
[L8] OptimizationLayer ──── 建议: "推理层耗时较高，可考虑增加DomainNexus缓存命中率"
                              写入记忆，影响下次分流
```

---

### 双轨制：思考与执行分离

```
┌─────────────────────────────────────────────────────┐
│  A轨：神政轨（思考者）                                │
│  DivineReason + SageDispatch + 翰林院审核            │
│  负责：推理、分析、决策、监管                          │
│         ↓ 单向调用                                   │
├─────────────────────────────────────────────────────┤
│  B轨：神行轨（执行者）                                │
│  763个独立 Claw（严助/亚当·斯密/丁肇中/韩非...）     │
│  负责：执行、产出、落地                               │
│  每个Claw拥有独立上下文、SOUL、IDENTITY、ReAct闭环    │
│         ↑ 结果回报                                   │
└─────────────────────────────────────────────────────┘
```

**核心约束**：B轨不能调用A轨（铁律），只能接收指令和回报结果。Claw虽然能独立思考和论证，但"能想不是目的，能干才是"——思考力服务于执行力。

### RefuteCore 驳心引擎（8维论证）

这不是一个简单的"检查逻辑错误"模块，而是一个完整的论证-反驳-修复闭环：

| 维度 | 作用 |
|------|------|
| **感性** | 捕捉论点中的情感诉求和情绪倾向 |
| **人性** | 从人性弱点出发评估论点的可行性 |
| **驳斥** | 直接攻击论点的逻辑漏洞 |
| **社交** | 评估论点在社交传播中的可行性 |
| **逆向** | 反过来想——如果这个论点成立，应该观察到什么？ |
| **暗森林** | 从博弈论角度评估论点暴露的风险 |
| **行为学** | 从行为经济学角度分析实际执行偏差 |
| **情绪** | 综合情绪状态影响决策质量评估 |

处理流程：`输入 → 论证解析 → 主张提取 → 矛盾检测(5层) → 反驳生成 → 辩论进化(3轮递进) → 论证修复 → 输出`

### DivineReason 三层推理

| 层级 | 名称 | 深度 | 适用场景 |
|------|------|------|---------|
| **Layer 1** | 表层推理 | 模式匹配、快速响应 | 简单问答、信息查询 |
| **Layer 2** | 深度推理 | 假设探索、多角度分析 | 复杂决策、策略分析 |
| **Layer 3** | 元认知审视 | 自我审视、谬误检测 | 关键决策、高风险场景 |

每层向下兼容。Layer 3 会在 Layer 2 推理完成后，对推理过程本身进行审视——检查是否存在认知偏差、逻辑谬误、信息遗漏。

### NeuralMemory v7 五层神经记忆

```
感知记忆 ──→ 工作记忆 ──→ 短期记忆 ──→ 长期记忆 ──→ 永恒记忆
(即时感知)   (当前上下文)  (7天TTL)    (持久化)    (核心知识)
```

- **Hebbian 学习**：高频访问的记忆自动强化，低频的逐渐衰减
- **资源感知**：根据内存/存储/Token预算动态优化分配
- **预测预加载**：基于访问频率模式预测并预加载即将需要的记忆
- **藏书阁同步**：核心知识定期同步到藏书阁，防止遗忘

### 21格动态知识系统（DomainNexus）

知识格子**不是预设的**，是动态生长的：

- **智慧核心 8格**（A1-A8）：逻辑判断/智慧模块/论证审核/判断决策/五层架构/核心执行链/感知记忆/反思进化
- **应用域 13格**（B1-C4）：用户增长/直播/私域/活动/会员/广告/地产/招商/策略/电商/数据/内容/投放

每格根据实际使用自动追踪、发现知识缺口、智能合并/拆分建议。**绝对禁止删除任何知识点**——归档≠删除。

---

## 技术栈

| 层 | 技术 |
|----|------|
| **核心引擎** | Python 3.11+, 纯Python实现（无重度ML依赖） |
| **推理调度** | 166+ 子引擎，12个SageDispatch调度器 |
| **知识系统** | NetworkX知识图谱, TF-IDF+Hashing语义编码 |
| **API层** | FastAPI + Uvicorn |
| **数据层** | SQLite (本地持久化), JSON/YAML (配置与知识) |
| **文档生成** | python-docx, python-pptx, ReportLab, openpyxl |
| **可选ML** | PyTorch, Transformers, HuggingFace (用于嵌入编码增强) |

---

## 项目规模

| 指标 | 数量 |
|------|------|
| Python 源文件 | 1,010+ |
| YAML 配置（贤者定义） | 880+ |
| 深度学习/哲学文档 | 800+ |
| 知识格子 | 21（智慧核心8 + 应用域13） |
| 子推理引擎 | 166+ |
| 智慧学派 | 42 |
| 问题类型 | 165 |
| 贤者 Claw | 763（11部门） |
| E2E 测试 | 25/25 通过 |
| 调度器 | 12（SageDispatch）+ RefuteCore T2 |

---

## 快速开始

```bash
# 克隆
git clone https://github.com/marcwadehan-png/somn-super-agent.git
cd somn-super-agent

# 安装核心依赖
pip install -r requirements.txt

# 启动后端
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# 运行测试
pytest tests/ -v
```

---

## 项目结构

```
somn-super-agent/
├── smart_office_assistant/src/     # 核心引擎
│   ├── core/                       #   SomnCore 主控
│   ├── intelligence/               #   智能系统
│   │   ├── engines/                #     推理引擎 (RefuteCore, DivineReason, 子引擎)
│   │   ├── dispatcher/wisdom_dispatch/  # SageDispatch 12调度器 + 藏书阁
│   │   ├── claws/                  #     Claw系统 (763贤者)
│   │   ├── dual_track/             #     双轨制 (A轨神政轨 + B轨神行轨)
│   │   └── three_core/             #     三核心整合
│   ├── neural_memory/              #   神经记忆 v7 (五层架构)
│   ├── learning/                   #   学习系统 (计划引擎/重放缓冲区)
│   └── wisdom/                     #   42学派智慧引擎
├── knowledge_cells/                # 21格知识系统
│   ├── domain_nexus.py             #   知识域动态管理
│   ├── pan_wisdom_core.py          #   万法智慧树 (42学派)
│   ├── eight_layer_pipeline.py     #   八层智慧管道 (天枢)
│   ├── divine_oversight.py         #   神政监督
│   ├── A1-C4.md                    #   21格知识内容
│   └── ecology_ml_bridge.py        #   生态学ML桥接
├── api/                            # FastAPI 后端
├── docs/                           # 800+ 深度文档
├── tests/                          # 测试套件
└── pyproject.toml                  # 项目配置
```

---

## 创新点总结

1. **八层智慧管道 + 论证回退机制**：业界首创的"论证不合格→回退重推理"闭环，确保输出质量
2. **驳心引擎 8维论证**：不只是逻辑检查，而是从感性、人性、博弈论、行为学等多维度结构化论证
3. **DivineReason 三层递进推理 + 元认知审视**：Layer 3 的"对推理过程的推理"能力
4. **双轨制（思考/执行分离）**：A轨推理决策，B轨763个独立Claw执行，单向通信铁律
5. **42学派融合推理**：一个问题同时从儒家、道家、法家、兵家、博弈论、行为经济学等42个角度分析并融合
6. **五层神经记忆 + Hebbian学习**：模拟人类记忆机制，会遗忘、会强化、会预测预加载
7. **21格动态知识系统**：知识格子不是预设的，根据使用自动生长、发现缺口、智能迭代
8. **0.02ms 瞬间实例化 + 懒加载**：神行轨763个Claw定义，0.02ms启动，按需加载

---

## 现阶段的不足与正在完善的内容

### 已知不足（按优先级排序）

| 问题 | 说明 | 优先级 | 临时方案/替代 |
|------|------|------|-------------|
| **LLM调用依赖** | 核心推理引擎（DivineReason/RefuteCore）需要外部LLM API支持，离线模式能力受限 | P1 | 计划集成 Ollama 本地模型 |
| **硬编码模板** | DivineReason 部分增强引擎仍使用硬编码模板，场景覆盖有限 | P1 | 已识别，待重构为动态生成 |
| **API兼容性** | 部分API接口命名不一致（如 divine_reason. vs DivineReasonEngine），降级运行 | P2 | 统一命名规范中 |
| **测试覆盖** | 核心模块 25/25 E2E 通过，但边缘路径（回退3轮/Supr模式）覆盖不足 | P2 | 持续补充中 |
| **GUI-S1界面** | 桌面可视化入口开发中，当前为命令行模式 | P2 | 命令行模式可用 |
| **文档站点** | 尚未建立完整的在线文档站 | P3 | GitHub Wiki 临时替代 |
| **Docker/CI/CD** | Dockerfile已就位但构建未自动化，Actions部分workflow禁用 | P3 | 手动构建，逐步启用 |
| **性能监控** | 缺乏实时管道耗时监控面板 | P3 | 日志手动分析 |
| **多语言支持** | 中文/英文为主，其他语言覆盖有限 | P3 | 计划扩展 |

### 正在推进的完善项

| 完善项 | 目标 | 当前状态 | 预计版本 |
|--------|------|--------|--------|
| **联网搜索能力** | 所有核心子系统添加自动联网检索 + 离线降级 | 部分集成TianShuWebSearch | v7.2 |
| **FastBoot深度优化** | 第二轮加载优化（NeuralMemory/DivineReason/DomainNexus） | 第一轮完成(0.02ms)，第二轮进行中 | v7.2 |
| **本地模型适配** | 支持 Ollama 本地模型（qwen/llama3）离线运行 | 规划验证中 | v7.3 |
| **GUI-S1版本** | PyQt6 + FastAPI 桌面可视化入口 | 开发中 | v7.2 |
| **v7.2规划** | LLM统一管理 + 网络状态感知 + 云端配置UI | 开发中 | v7.2 |
| **S-prefix版本** | 统一版本前缀应用于所有子系统 | 推进中 | v7.2 |

---

## 协议

[AGPL-3.0](LICENSE) — GNU Affero General Public License v3.0

---

## 贡献

欢迎提交 Issue 和 Pull Request。详见 [CONTRIBUTING.md](CONTRIBUTING.md)

```bash
git checkout -b feature/your-idea
git commit -m 'Add: your feature'
git push origin feature/your-idea
# 提交 Pull Request
```

### 招募方向

| 领域 | 难度 |
|------|------|
| 推理引擎优化（提升 LongCoT/ToT/GoT/ReAct 效率） | ⭐⭐⭐ |
| 知识系统扩展（丰富42学派与知识格子内容） | ⭐⭐ |
| 驳心引擎增强（新增论证维度或优化现有8维） | ⭐⭐⭐ |
| 后端架构（FastAPI 服务扩展与性能优化） | ⭐⭐⭐ |
| 本地模型适配（让核心推理支持离线运行） | ⭐⭐⭐ |
| 测试覆盖 | ⭐ |
| 文档翻译 | ⭐ |

---

## 联系

- 📧 邮箱：marcwadehan@gmail.com
- 🐛 [GitHub Issues](https://github.com/marcwadehan-png/somn-super-agent/issues)
