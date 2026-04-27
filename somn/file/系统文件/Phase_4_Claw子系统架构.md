# Phase 4 Claw子系统规范化架构文档

## 文档信息

| 项目 | 内容 |
|------|------|
| 名称 | Phase 4 Claw子智能体子系统 |
| 版本 | v1.0.0 |
| 日期 | 2026-04-22 |
| 状态 | ✅ 核心完成（代码100%，验证通过） |
| 规范依据 | 贤者工程五层链路规范化架构 v1.0.0 |

---

## 一、设计目标与定位

Phase 4 是贤者工程五层链路的最后一环，目标是将 Phase 0-3 积累的全部知识资产（742篇深度学习文档、759份蒸馏文档、766条SageCode编码、751个克隆实例）转化为**可独立运行的智能体实例**。每个贤者从一个静态的知识编码，升级为一个具备感知、推理、执行、反馈四模块能力的活体Claw。

核心原则：776个YAML配置驱动，零硬编码，全量可验证。

### 1.1 与前后Phase的关系

```
Phase 0 (深度学习文档) ──→ Phase 1 (蒸馏文档) ──→ Phase 2 (编码注册表)
       742篇                         759份                    766条
            │                              │                        │
            ▼                              ▼                        ▼
       原始知识                       结构化智慧              可执行接口
                                                                    │
                                                                    ▼
                           Phase 3 (Cloning克隆) ──→ Phase 4 (Claw子智能体)
                                751个实例                      776个Claw
                                   │                              │
                                   ▼                              ▼
                             SageProxyFactory           ClawArchitect×776
                          (P1+P2个性化驱动)        (YAML配置+四模块运行时)
```

Phase 3 产出的是**可调用的Python类实例**（SageProxy），Phase 4 将其封装为**具备完整生命周期的自治智能体**（ClawArchitect），并在此基础上叠加多智能体协作调度能力。

---

## 二、系统架构总览

### 2.1 模块结构

```
src/intelligence/claws/
├── __init__.py                # 包导出（75个符号）
├── claw.py                    # 统一入口（ClawSystem / ClawResponse / quick_ask）
├── _claw_architect.py         # 核心架构（~1317行）
│   ├── 数据类型定义             # ClawMetadata/CognitiveDimensions/ReActConfig等
│   ├── YAML配置加载器          # load_claw_config / _parse_raw_config（兼容v1+v2）
│   ├── ReAct闭环推理引擎       # ReActLoop（Thought→Action→Observation循环）
│   ├── Skills工具链系统        # SkillsToolChain（10种标准技能）
│   ├── NeuralMemory记忆适配器   # ClawMemoryAdapter（短期/长期/情景三层记忆）
│   ├── ClawArchitect主类       # 四模块架构编排
│   └── 工厂函数               # create_claw / create_claws_batch
├── _claws_coordinator.py      # 多Claw协调器（~720行）
│   ├── GatewayRouter          # 意图路由器（4级匹配策略）
│   ├── ClawsCoordinator       # 协调器主类（加载/路由/协作/统计）
│   └── ProcessResult          # 统一处理结果封装
├── _claw_bridge.py            # 主系统集成桥接（~320行）
│   ├── ClawSystemBridge       # SomnCore/WisdomDispatcher桥接器
│   ├── DispatchRequest/Response # 调度请求与响应数据结构
│   └── IntegrationConfig      # 集成级别配置（4级）
└── configs/                   # 776个YAML配置文件（v2格式）
    ├── 孔子.yaml
    ├── 老子.yaml
    ├── 王阳明.yaml
    └── ...（共776个）
```

### 2.2 架构层次图

```
┌─────────────────────────────────────────────────────────────┐
│                     SomnCore / WisdomDispatcher             │
│                          （主系统调度层）                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
              ┌────────▼────────┐
              │  _claw_bridge   │ ← IntegrationLevel: STANDALONE/DISPATCHER/SOMNCORE/FULL
              │  ClawSystemBridge│
              └────────┬────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                    claw.py 统一入口                           │
│         ClawSystem / ClawResponse / quick_ask               │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              _claws_coordinator.py 协调层                     │
│  ┌─────────────────────────────────────────┐                │
│  │           GatewayRouter                 │                │
│  │  触发词匹配 → 学派关键词 → 名称直接 → 兜底   │                │
│  └──────────────────┬──────────────────────┘                │
│                     │ 路由决策 RouteDecision                  │
│  ┌──────────────────▼──────────────────────┐                │
│  │         ClawsCoordinator                 │                │
│  │  批量加载 / 并发控制 / 协作调度 / 统计监控  │                │
│  └──────────────────┬──────────────────────┘                │
└──────────────────────┬──────────────────────────────────────┘
                       │ ProcessResult × N
        ┌──────────────┼──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Claw A     │ │  Claw B     │ │  Claw C     │ │  Claw D     │
│ (孔子)      │ │ (老子)      │ │ (王阳明)     │ │ (韩非子)    │
│  儒家       │ │  道家       │ │  儒家        │ │  法家       │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │               │
       ▼               ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────┐
│              _claw_architect.py — 单Claw四模块               │
│  ┌─────────┬─────────┬────────────┬─────────────────────┐  │
│  │Perception│Reasoning│ Execution  │     Feedback        │  │
│  │  感知    │  推理    │   执行      │      反馈           │  │
│  │ YAML元数据│ReActLoop│SkillsChain │ ClawMemoryAdapter   │  │
│  │ 触发词   │ SageLoop │ ToolCall   │ persist/search     │  │
│  └─────────┴─────────┴────────────┴─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 三、核心数据类型

### 3.1 ClawStatus — Claw状态枚举

| 状态 | 值 | 说明 |
|------|-----|------|
| IDLE | idle | 空闲待命 |
| ACTIVE | active | 活跃处理中 |
| REASONING | reasoning | ReAct推理中 |
| EXECUTING | executing | 技能执行中 |
| ERROR | error | 异常状态 |
| SUSPENDED | suspended | 已挂起 |

### 3.2 ReasoningStyle — 推理风格枚举

| 风格 | 值 | 适用学派 | 行为特征 |
|------|-----|----------|----------|
| DEEP_ANALYTICAL | deep_analytical | 儒、法 | 偏好工具调用和深层推理，迭代次数多 |
| INTUITIVE_WISDOM | intuitive_wisdom | 道、释 | 快速收敛，直觉判断优先 |
| PRACTICAL_ACTION | practical_action | 兵、墨 | 行动导向，快速给出方案 |
| SYSTEMATIC_LOGIC | systematic_logic | 名、阴阳 | 严谨逻辑推演 |
| NARRATIVE_POETIC | narrative_poetic | 文、史 | 叙事化表达，注重语境 |
| DIALECTICAL | dialectical | 杂家等 | 多视角辩证综合 |

### 3.3 CognitiveDimensions — 六维认知向量

| 维度 | 字段 | 类型 | 默认值 | 含义 |
|------|------|------|--------|------|
| 思维深度 | cog_depth | float | 7.0 | 分析问题本质的能力 |
| 决策质量 | decision_quality | float | 7.0 | 做出正确选择的能力 |
| 价值判断 | value_judge | float | 7.0 | 道德和价值评估能力 |
| 治理决策 | gov_decision | float | 7.0 | 组织管理决策能力 |
| 战略思维 | strategy | float | 7.0 | 长远规划能力 |
| 自我管理 | self_mgmt | float | 7.0 | 自我反思和修正能力 |

每个维度的取值范围 0.0-10.0，从YAML配置的 cognitive_dimensions 字段加载，来源于 Phase 1 蒸馏文档中的认知维度表或 Phase 2 编码注册表。

### 3.4 ClawMetadata — 完整元数据模型

这是从YAML配置文件解析后的完整数据结构，是整个Claw子系统的数据基石：

```python
@dataclass
class ClawMetadata:
    # 标识
    name: str                    # 贤者名称（如"孔子"）
    sage_id: str                 # 贤者唯一ID
    version: str = "1.0.0"       # 配置版本
    status: str = "idle"

    # 基本信息
    era: str = ""                # 时代（如"春秋战国"）
    school: str = ""             # 学派（如"儒家"）
    court_position: str = ""     # 朝廷岗位
    department: str = ""         # 所属部门
    wisdom_school: str = ""      # WisdomSchool枚举值

    # 四链路引用
    phase_0_doc: str = ""        # Phase 0 深度学习文档路径
    phase_1_doc: str = ""        # Phase 1 蒸馏文档路径
    phase_2_registry: str = ""   # Phase 2 编码注册表条目
    phase_3_factory: str = ""    # Phase 3 克隆工厂方法

    # 能力与智慧
    cognitive_dimensions: CognitiveDimensions  # 六维认知向量
    wisdom_laws: List[str]                   # 6条个性化智慧法则
    wisdom_functions: List[str]              # 智慧函数名列表
    triggers: List[str]                      # 触发词列表

    # ReAct闭环配置
    react_config: ReActConfig

    # 工具与技能
    tools: List[Dict[str, str]]              # 工具列表
    skills: List[Dict[str, Any]]             # 技能列表（含enabled标记）

    # 记忆配置
    memory_config: MemoryConfig

    # 人格配置
    personality: PersonalityProfile

    # 协作配置
    collaboration: CollaborationConfig
```

### 3.5 其他关键数据结构

| 数据结构 | 用途 | 关键字段 |
|----------|------|----------|
| ReActConfig | ReAct闭环参数 | max_iterations(10), timeout_seconds(300), quality_threshold(0.7), reasoning_style |
| MemoryConfig | 记忆系统参数 | memory_type(episodic), path, max_episodes(1000), consolidation_threshold(50) |
| PersonalityProfile | 人格参数 | response_style, formality_level(1-10), creativity_level(1-10), caution_level(1-10) |
| CollaborationConfig | 协作参数 | can_lead, can_support, preferred_role(leader/analyst/supporter/reviewer) |
| ReActStep | ReAct单步结果 | step_num, thought, action, observation, confidence, timestamp |
| ReActResult | ReAct最终结果 | query, claw_name, steps[], final_answer, success, reason, elapsed |
| MemoryEpisode | 记忆片段 | episode_id, content, timestamp, metadata, importance(0-1) |
| RouteDecision | 路由决策 | primary(主Claw), collaborators[], strategy, confidence, reason |
| ProcessResult | 处理结果 | query, routed_to, collaborators_used[], success, react_result, error, elapsed |
| DispatchRequest | 调度请求(Bridge) | query, problem_type, department, wisdom_schools[], context, priority |
| DispatchResponse | 调度响应(Bridge) | success, answer, claw_name, collaborators[], confidence, react_trace[] |

---

## 四、四模块架构详解

### 4.1 Perception（感知）— 输入接收与上下文注入

感知层不是独立类，而是 ClawArchitect.process() 方法的第一阶段：

**流程：**
1. 接收用户输入 query
2. 写入短期记忆（role="user", content=query）
3. 从记忆适配器获取上下文窗口（最近10条情景记忆 + 最近5条短期记忆）
4. 注入额外上下文：personality人格参数 + wisdom_laws智慧法则
5. 组装完整的 ctx 字典传递给推理层

**关键代码位置：** ClawArchitect.process() 第1157-1164行

### 4.2 Reasoning（推理）— ReAct闭环引擎

ReActLoop 是整个Claw的推理核心，实现经典的 Thought → Action → Observation 循环：

#### 4.2.1 循环控制

```
初始化 → _should_continue()?
  │         │
  │ YES     │ NO（达到max_iterations或quality_threshold）
  ▼         ▼
_think()  _synthesize()
  │         │
  ▼         ▼
_act()   返回ReActResult
  │
  ▼
_observe()
  │
  ▼
记录ReActStep → 回到_should_continue()
```

**终止条件（任一满足即停止）：**
- 迭代次数 >= max_iterations（默认10步）
- 最后一步置信度 >= quality_threshold（默认0.7）
- 超时（timeout_seconds，默认300秒）

#### 4.2.2 Thought阶段 (_think)

生成思考内容，融合四个维度：
- **智慧法则约束**：取前3条wisdom_laws作为主要思维约束
- **认知维度权重**：cog_depth 和 value_judge 影响思考深度
- **历史步骤上下文**：上一步的动作和观察结果
- **推理风格**：reasoning_style 决定思考偏向

#### 4.2.3 Action阶段 (_act)

支持4种动作类型：

| 动作 | 触发条件 | 说明 |
|------|----------|------|
| conclude | 达到最后一步或置信度足够 | 终止循环，生成最终答案 |
| tool_call | 深度分析型前期 + 有已注册工具 | 调用工具获取外部信息 |
| deep_think | 默认动作 | 继续深层推理，结合智慧法则 |
| consult | 后期阶段 + 有已注册协作Claw | 发起跨Claw咨询获取多元视角 |

**推理风格对动作选择的影响：**
- `deep_analytical`：前2步偏好tool_call，第5步后尝试consult
- `intuitive_wisdom`：第3步后即可conclude（快速收敛）
- 默认策略：第4步后有协作Claw时尝试consult

#### 4.2.4 Observation阶段 (_observe)

根据不同动作执行对应操作并返回 (observation_string, confidence)：

- **conclude**: 返回结论摘要，置信度0.85
- **tool_call**: 执行已注册的工具函数，成功0.6/失败0.2/未找到0.5
- **deep_think**: 返回结合智慧法则的推理文本，置信度0.55
- **consult**: 委托给 _observe_consult 方法处理

#### 4.2.5 跨Claw协作机制 (_observe_consult)

这是 Phase 4 的关键创新点 —— Claw之间可以相互咨询：

**流程：**
1. 确定咨询目标（自动选择或指定）
2. 优先选择不同学派的协作Claw（确保视角多样性）
3. 构建咨询上下文（标注角色为"consultant"，记录原始Claw名称）
4. 调用协作Claw的 process() 方法
5. 记录咨询历史（目标、查询摘要、学派、成功状态、时间戳）
6. 返回协作Claw的回答摘要（截断至300字符）

**协作伙伴管理：**
- register_collaborator(name, claw): 注册协作Claw
- get_collaborators(): 获取已注册列表
- _consult_history: 保存历史咨询记录

### 4.3 Execution（执行）— SkillsToolChain工具链

管理每个Claw可用的技能集合：

#### 4.3.1 标准技能清单（10种）

| 技能名 | 分类 | 描述 | 适用学派 |
|--------|------|------|----------|
| analysis | core | 深度分析 | 全部 |
| writing | core | 文本生成 | 全部 |
| reasoning | core | 逻辑推理 | 全部 |
| memory_recall | core | 记忆召回 | 全部 |
| knowledge_retrieval | extended | 知识检索 | 全部 |
| ethical_judgment | school_specialized | 伦理判断 | 儒家等 |
| tactical_planning | school_specialized | 战术规划 | 兵家等 |
| strategic_consulting | school_specialized | 战略咨询 | 法家等 |
| classics_interpretation | school_specialized | 典籍解读 | 经学派 |
| metaphysical_reasoning | school_specialized | 形而上学推理 | 道、释等 |

#### 4.3.2 技能生命周期

1. **加载阶段**：从YAML的 skills 列表解析，按 enabled 字段过滤
2. **注册阶段**：通过 register_handler(skill_name, handler) 注册自定义处理函数
3. **执行阶段**：
   - 有自定义handler → 调用handler
   - 无自定义handler → 使用_default_skill_impl兜底（返回格式化的学派视角响应）

### 4.4 Feedback（反馈）— ClawMemoryAdapter记忆层

为每个Claw提供独立的三层记忆空间：

#### 4.4.1 记忆层级

| 层级 | 实现方式 | 容量 | 持久化 |
|------|----------|------|--------|
| 短期记忆 | 内存List[Dict] | 最多50条（FIFO淘汰） | 否 |
| 情景记忆 | 内存List[MemoryEpisode] | max_episodes上限 | JSON文件 |
| 归档记忆 | 磁盘JSON文件 | 无限 | 是（archive/目录） |

#### 4.4.2 存储路径规范

```
data/claws/{sage_id}/memory/
├── episodes.json        # 活跃情景记忆（持久化目标）
└── archive/
    └── archive_{timestamp}.json  # 归档记忆（低重要性淘汰时写入）
```

#### 4.4.3 关键操作

| 操作 | 方法 | 说明 |
|------|------|------|
| 写入短期 | add_short_term(role, content) | 记录对话交互 |
| 写入情景 | add_episode(content, importance) | 记录重要事件 |
| 获取上下文 | get_context_window(max_episodes=10) | 格式化为推理注入文本 |
| 搜索记忆 | search(query, top_k=5) | 关键词匹配（TODO: 向量检索） |
| 巩固记忆 | _consolidate() | 超过阈值时低重要性归档 |
| 持久化 | persist() | episodes.json写入磁盘 |
| 统计信息 | get_stats() | 各层级计数和路径 |

#### 4.4.4 自动记忆流程（在process()中触发）

推理成功后自动执行：
1. 将助手回复写入短期记忆（role="assistant"）
2. 创建情景记忆片段（Q+A格式，importance=最后一步置信度）
3. 调用 persist() 写入磁盘

---

## 五、多Claw协调机制

### 5.1 GatewayRouter — 意图路由器

实现4级递降式匹配策略：

```
用户输入
  │
  ├─ 1. 触发词精确匹配（triggers字段，评分=匹配长度加权）
  │     └─ 匹配多个？→ 取最高分为主Claw，次高2个为协作者
  │
  ├─ 2. 名称直接提及（query中包含某Claw名字）
  │     └─ 置信度0.95（高度确定）
  │
  ├─ 3. 学派关键词推断（8大学派关键词表）
  │     └─ 在匹配学派中取cog_depth最高的Claw
  │     └─ 置信度0.7
  │
  └─ 4. 兜底（默认Claw，通常为孔子）
        └─ 置信度0.2
```

**学派关键词映射表：**

| 学派 | 关键词 |
|------|--------|
| 儒家 | 仁、礼、德、君子、孔子、孟子、论语、仁义 |
| 道家 | 道、无为、自然、逍遥、老子、庄子、道德经 |
| 法家 | 法、术、势、法治、韩非、商鞅 |
| 兵家 | 兵、战、谋略、孙子、孙武、兵法、战争 |
| 墨家 | 兼爱、非攻、墨子、尚贤 |
| 佛学 | 佛、禅、菩提、涅槃、禅宗 |
| 阴阳 | 阴阳、五行、八卦、易经 |

### 5.2 ClawsCoordinator — 协调器主类

#### 5.2.1 初始化流程

```
initialize(names?, lazy_load?)
  │
  ├─ names为None → list_all_configs() 扫描configs/目录全部yaml
  ├─ 逐个load_claw_config() → 解析为ClawMetadata
  ├─ 非懒加载模式 → create_claw() 创建完整ClawArchitect实例
  ├─ 设置并发信号量（默认max_concurrent=5）
  └─ 如果有"孔子" → 设为默认兜底Claw
```

#### 5.2.2 处理流程（process方法）

```
用户请求
  │
  ├─ 触发 on_process_start 回调
  │
  ├─ 【路由阶段】
  │   ├─ 手动指定target_claw? → 跳过Gateway直接路由
  │   └─ 否则 → gateway.route(query, strategy)
  │
  ├─ 【目标检查】
  │   ├─ primary在self.claws? → 直接使用
  │   └─ 否则 → 懒加载create_claw()
  │
  ├─ 【协作注册】
  │   └─ 将decision.collaborators[:2]注册到primary_claw.react_loop
  │
  ├─ 【主Claw执行】
  │   └─ primary_claw.process(query, context)
  │
  ├─ 【协作阶段】（可选）
  │   └─ 对collaborators[:2]以"补充视角"模式调用process()
  │       └─ 结果追加到react_result.final_answer
  │
  ├─ 【统计更新】
  │   └─ successful_routes++, avg_response_time, claw_usage_counts
  │
  └─ 触发 on_process_complete 回调
```

#### 5.2.3 批量处理

`process_batch()` 支持并发批量查询，使用 asyncio.Semaphore 控制并发上限。

### 5.3 路由策略枚举

| 策略 | 值 | 说明 |
|------|-----|------|
| TRIGGER_MATCH | trigger_match | 触发词匹配（默认） |
| SINGLE_BEST | single_best | 单最佳匹配 |
| MULTI_COLLABORATIVE | multi_collaborative | 多Claw协作 |
| ROUND_ROBIN | round_robin | 轮询 |
| MANUAL | manual | 手动指定 |
| SCHOOL_BASED | school_based | 基于学派路由 |

---

## 六、主系统集成桥接（_claw_bridge.py）

### 6.1 集成级别

| 级别 | 值 | 功能范围 |
|------|-----|----------|
| STANDBONE | standalone | 独立运行，不接入主系统（默认） |
| DISPATCHER | dispatcher | 接入WisdomDispatcher调度链路 |
| SOMNCORE | somncore | 接入SomnCore生命周期管理 |
| FULL | full | 全集成（上述全部 + OpenClaw知识注入 + 记忆同步） |

### 6.2 ClawSystemBridge 核心接口

| 方法 | 功能 |
|------|------|
| initialize() | 初始化桥接器 + 加载全部Claw + 初始化OpenClaw |
| dispatch(request) | 处理调度请求（WisdomDispatcher/SomnCore入口） |
| dispatch_batch(requests) | 批量调度（并发） |
| inject_knowledge(query, claws) | 通过OpenClaw抓取外部知识注入Claw记忆 |
| submit_feedback(feedback_data) | 提交用户反馈学习 |
| get_bridge_status() | 获取完整状态（含调度统计） |

### 6.3 调度请求/响应模型

DispatchRequest 从主系统接收 ProblemType/Department/WisdomSchool 信息，通过学派匹配路由到对应Claw。DispatchResponse 返回完整答案及 ReAct 推理轨迹（react_trace），供上层系统做质量评估和日志审计。

### 6.4 OpenClaw知识注入流程

```
inject_knowledge("人工智能最新进展", ["孔子", "老子"])
  │
  ├─ OpenClawCore.fetch_knowledge("人工智能最新进展")
  │   └─ 返回 List[Knowledge]
  │
  ├─ 对每个目标Claw:
  │   └─ OpenClawCore.inject_to_claw(claw.memory, items)
  │       └─ 将知识项写入Claw的记忆系统
  │
  └─ OpenClawCore.update_knowledge(items)
      └─ 更新全局知识库
```

---

## 七、统一入口（claw.py）

### 7.1 ClawSystem — 门面类

提供最简API供外部使用：

```python
# 完整生命周期
system = ClawSystem()           # 创建（可指定claw_names部分加载）
await system.start()            # 初始化（加载所有Claw配置）
result = await system.ask("什么是仁？")  # 提问
print(result.answer)            # 获取答案
await system.shutdown()         # 关闭（持久化所有记忆）

# 便捷功能
system.list_available()         # 列出所有可用Claw名称
system.list_loaded()            # 列出已加载Claw详情
system.find_claw("仁")          # 根据触发词查找匹配Claw
system.get_stats()              # 系统统计信息
```

### 7.2 ClawResponse — 响应包装器

提供属性化访问：

| 属性 | 类型 | 说明 |
|------|------|------|
| success | bool | 是否成功 |
| answer | str | 最终答案文本 |
| routed_to | str | 路由到的Claw名称 |
| collaborators | List[str] | 参与协作的Claw |
| confidence | float | 路由置信度 |
| elapsed | float | 耗时（秒） |
| error | str | 错误信息（如有） |
| steps_count | int | ReAct推理步数 |
| steps | list | 完整推理轨迹 |

### 7.3 quick_ask — 一次性函数

自动管理完整生命周期，适合简单场景：

```python
response = await quick_ask("什么是道？", target="老子")
print(response.answer)
```

---

## 八、YAML配置规范

### 8.1 配置文件格式（v2）

每个Claw对应一个YAML文件，存放在 `src/intelligence/claws/configs/{name}.yaml`：

```yaml
name: 孔子
sage_id: confucius
version: "2.0"
status: active
era: 春秋末期
school: 儒家
court_position: 至圣先师·王爵
department: 教化司
wisdom_school: CONFUCIANISM

phase_documents:
  phase_0: file/智慧文件/孔子（Confucius）深度学习.md
  phase_1: docs/蒸馏卷/儒家/孔子智慧蒸馏.md
  phase_2: wisdom_encoding_registry.py → SAGE_CONFUCIUS
  phase_3: _sage_proxy_factory.py → create_cloning_class("孔子", ...)

cognitive_dimensions:
  cog_depth: 9.8
  decision_quality: 9.5
  value_judge: 9.9
  gov_decision: 9.2
  strategy: 9.0
  self_mgmt: 9.6

wisdom_laws:
  - "仁者爱人，己所不欲勿施于人——一切行为的终极出发点是仁爱之心"
  - "克己复礼为仁——通过自我约束回归礼制秩序来实现人格完善"
  - "因材施教，有教无类——教育应尊重个体差异且面向所有人开放"
  - "德治为主，刑辅为从——治理应以道德感化为核心，法律仅作补充"
  - "学而不思则罔，思而不学则殆——学习与思考必须紧密结合互为印证"
  - "君子和而不同，小人同而不和——真正和谐允许多样性存在"

wisdom_functions:
  - advise_on_ethics
  - analyze_social_order
  - assess_moral_character
  - decide_by_virtue
  - teach_by_example
  - cultivate_moral_character

triggers:
  - 孔子
  - 仁
  - 礼
  - 君子
  - 儒家
  - 论语
  - 仁义
  - 己所不欲

react_loop:
  max_iterations: 10
  timeout_seconds: 300
  quality_threshold: 0.7
  reasoning_style: deep_analytical

tools:
  - name: knowledge_retrieval
    category: core
  - name: general_reasoning
    category: core
  - name: memory_recall
    category: core

skills:
  - name: analysis
    enabled: true
  - name: writing
    enabled: true
  - name: reasoning
    enabled: true
  - name: ethical_judgment
    enabled: true
  - name: classics_interpretation
    enabled: true
  - name: strategic_consulting
    enabled: false

memory:
  type: episodic
  path: ""
  max_episodes: 1000
  consolidation_threshold: 50

personality:
  response_style: balanced_informative
  formality_level: 8
  creativity_level: 5
  caution_level: 7

collaboration:
  can_lead: true
  can_support: true
  preferred_role: leader
```

### 8.2 v1/v2兼容性

_parse_raw_config() 同时支持两种YAML格式：
- v1格式：扁平结构，字段名为 system_tools, personalized_rules 等（_gen_claw.py 生成）
- v2格式：分段注释结构，字段名为 tools, wisdom_laws 等（_gen_claw_v2.py 生成）

加载器通过 `raw.get("新字段", raw.get("旧字段", 默认值))` 的回退模式实现兼容。

---

## 九、回调与扩展机制

### 9.1 ClawArchitect 钩子

| 钩子 | 注册方法 | 触发时机 | 用途 |
|------|----------|----------|------|
| 推理前 | on_before_reasoning(fn) | ReAct执行前 | 上下文注入、权限检查 |
| 执行后 | on_after_execution(fn) | ReAct完成后 | 日志记录、结果后处理 |
| 错误 | on_error(fn) | 异常发生时 | 错误告警、降级策略 |

所有钩子支持同步和异步函数，返回 self 以支持链式调用：

```python
claw.on_before_reasoning(my_hook).on_after_execution(my_logger)
```

### 9.2 ClawsCoordinator 钩子

| 钩子 | 注册方法 | 触发时机 |
|------|----------|----------|
| 处理开始 | on_process_start(fn) | process()入口处 |
| 处理完成 | on_process_complete(fn) | process()返回前 |

---

## 十、验证与测试

### 10.1 端到端测试覆盖（21个用例，100%通过）

| 测试域 | 用例数 | 覆盖内容 |
|--------|--------|----------|
| YAML配置加载 | 3 | 孔子/王阳明/白玉蟾三种典型配置解析 |
| ClawArchitect创建 | 2 | 四模块初始化 + 默认参数验证 |
| ReAct闭环推理 | 3 | 10步迭代/质量阈值终止/超时处理 |
| Skills工具链 | 2 | 技能检查 + 默认执行 |
| 记忆系统 | 3 | 写入/搜索/持久化到磁盘 |
| Gateway路由 | 3 | 触发词匹配/学派关键词/兜底策略 |
| ClawsCoordinator | 3 | 批量加载/端到端问答/统计报告 |
| ClawSystem入口 | 2 | 快速问答/list_available |
| 触发词匹配 | 2 | 正向匹配/反向排除 |
| 统计与健康 | 1 | 健康报告/错误检测 |

### 10.2 全量验证（776个Claw，100%通过）

扫描 configs/ 目录下全部776个YAML文件，逐个执行：
1. YAML解析（PyYAML safe_load）
2. ClawMetadata 构建
3. ClawArchitect 实例化
4. 四模块非空校验
5. 触发词非空校验
6. 智慧法则>=1条校验

结果：776/776 全部通过（修复20个数据损坏YAML后）。

### 10.3 已修复的Bug清单

| Bug | 文件 | 问题 | 修复 |
|-----|------|------|------|
| 语法错误 | _claws_coordinator.py:228 | Optional[str): 括号不匹配 | → Optional[str]: |
| 变量冲突 | _claw_architect.py:search | scored.append((scored, ep)) 变量名与列表同名 | → (score, ep) |
| YAML格式 | 776个文件 | cognitive_dimensions:{ 多余花括号 | 正则清理开{和独立}行 |
| 数据损坏 | 20个文件 | \\\"\"\" / \"\" / POL\_ 等残缺 | 行级正则清理 |
| 未定义变量 | openclaw/_feedback.py:49 | self._user_sage_negative 不存在 | → self._user_patterns |
| 缺括号 | openclaw/_updater.py:110 | return list(set(old + new) 缺闭合 | → list(set(old + new)) |

---

## 十一、统计数据汇总

### 11.1 代码规模

| 文件 | 行数 | 功能 |
|------|------|------|
| _claw_architect.py | ~1317行 | 核心：类型定义 + YAML加载 + ReAct + Skills + Memory + 主类 + 工厂 |
| _claws_coordinator.py | ~720行 | Gateway路由 + Coordinator协调 + 统计 |
| claw.py | ~218行 | 统一入口 + 响应包装 + quick_ask |
| _claw_bridge.py | ~320行 | 主系统集成 + OpenClaw对接 |
| __init__.py | ~76行 | 包导出（75个符号） |
| **合计** | **~2651行** | **不含YAML和测试** |

### 11.2 配置规模

| 指标 | 数值 |
|------|------|
| YAML配置文件总数 | 776个 |
| 覆盖贤者数量 | 776人（含11虚拟人物） |
| 覆盖学派数量 | 25个WisdomSchool |
| 平均触发词数 | ~8个/Claw |
| 平均智慧法则数 | 6条/Claw（100%达标） |
| 平均认知维度 | 6维全量/Claw（100%达标） |

### 11.3 验证结果

| 验证项 | 结果 |
|--------|------|
| E2E测试 | 21/21 通过 (100%) |
| 全量Claw验证 | 776/776 通过 (100%) |
| Python语法检查 | 0 错误 (856文件扫描) |

---

## 十二、后续演进方向

### 12.1 短期优化（v1.0.0规划）

1. **记忆搜索升级**：从关键词匹配升级为向量语义检索（集成NeuralMemorySystem）
2. **动态负载均衡**：基于Claw历史响应时间和成功率调整路由权重
3. **技能热插拔**：运行时动态注册/注销技能处理器
4. **ReAct并行分支**：支持多条推理路径并行探索后合并

### 12.2 中期规划（Phase 4.5 - OpenClaw深化）

1. **数据源连接器**：实现_web_source / _file_source / _api_source / _rss_source
2. **知识抓取器**：实现_web_fetcher / _doc_parser / _cleaner
3. **增量更新引擎**：实现_diff_engine / _merger / _version_ctrl
4. **主动学习**：实现_pattern_learner / _recommender

### 12.3 长期愿景

1. **Claw自治进化**：基于反馈闭环自主优化自身配置参数
2. **跨Claw知识共享**：建立Claw间知识图谱，实现经验传承
3. **多模态Claw**：扩展SkillsToolChain支持图像/音频/代码等多模态输入输出

---

## 附录A：完整导出符号列表（__init__.py, 75个）

**统一入口（3）：** ClawSystem, ClawResponse, quick_ask

**核心架构（4）：** ClawArchitect, ReActLoop, SkillsToolChain, ClawMemoryAdapter

**类型定义（14）：** ClawMetadata, ClawStatus, CognitiveDimensions, ReActConfig, MemoryConfig, PersonalityProfile, CollaborationConfig, ReActStep, ReActResult, MemoryEpisode, ReasoningStyle

**协调器（6）：** ClawsCoordinator, GatewayRouter, RouteStrategy, RouteDecision, CoordinatorStats, ProcessResult

**工厂函数（4）：** load_claw_config, list_all_configs, create_claw, create_claws_batch

**其他（内部桥接等未在此包导出）：** ClawSystemBridge, DispatchRequest, DispatchResponse, IntegrationConfig, IntegrationLevel

---

## 附录B：关键文件路径索引

| 文件 | 项目路径 |
|------|----------|
| Claw核心 | smart_office_assistant/src/intelligence/claws/_claw_architect.py |
| 协调器 | smart_office_assistant/src/intelligence/claws/_claws_coordinator.py |
| 统一入口 | smart_office_assistant/src/intelligence/claws/claw.py |
| 包导出 | smart_office_assistant/src/intelligence/claws/__init__.py |
| 系统桥接 | smart_office_assistant/src/intelligence/claws/_claw_bridge.py |
| YAML配置目录 | smart_office_assistant/src/intelligence/claws/configs/ |
| E2E验证脚本 | _verify_claws_e2e.py |
| 全量验证脚本 | _verify_all_776_claws.py |
| 架构设计（旧版） | docs/项目进度/Phase4_OpenClaw架构设计.md |
| 本文档 | docs/Phase_4_Claw子系统架构.md |
