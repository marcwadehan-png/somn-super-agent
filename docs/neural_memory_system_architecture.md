# 神经记忆系统架构 v2.0

> **Neural Memory System Architecture**
> 最后更新：2026-04-28
> 版本：v2.0.0（架构迭代版）

---

## ⚡ V2.0 架构迭代摘要 (2026-04-28)

### 核心变更总览

| 变更ID | 名称 | 状态 | 涉及文件 |
|--------|------|------|----------|
| G-1 | **统一记忆分级体系** | ✅ | `memory_types.py`, `_imperial_library.py` |
| G-2 | **学习系统双向闭环** | ✅ | `learning_replay_buffer.py`(新), `learning_pipeline.py` |
| G-3 | **Claw贤者动态任职注册** | ✅ | `_library_staff_registry.py`(新), `_imperial_library.py` |
| G-4 | **知识库管理接口** | ✅ | `_library_knowledge_bridge.py` |
| G-5 | **语义向量编码器** | ✅ | `_semantic_encoder.py`(新) + `_imperial_library.py` + `_library_knowledge_bridge.py` |
| G-6 | **自动跨域关联** | ✅ | `_library_knowledge_bridge.py` |
| G-7 | **定时审查调度器** | ✅ | `_library_review_scheduler.py`(新) |
| G-8 | **统一存储格式V2** | ✅ | `unified_memory_interface.py` |

### 架构绑定关系（v2.0 核心设计）

```
┌──────────────────────────────────────────────────────────────────────┐
│                     神经记忆系统 v2.0 架构                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐                                                    │
│  │   输入层      │  学习系统 = 记忆仓库的出入库管理制度和体系            │
│  │   学习系统    │  [v2.0] 双向闭环：入库(已有) + 经验回放(新增)      │
│  └──────┬───────┘                                                    │
│         │                                                            │
│         ▼                                                            │
│  ┌──────────────┐                                                    │
│  │ 数据运营层    │  核心组件 = 记忆仓库（藏书阁）的管理工具             │
│  │  核心组件    │  UnifiedMemoryInterface v2.0                      │
│  └──────┬───────┘                                                    │
│         │                                                            │
│         ▼                                                            │
│  ┌──────────────┐    管理工具     ┌──────────────┐                  │
│  │ 数据管理层    │ ◄═══绑定════► │   记忆仓库     │                  │
│  │ 三层记忆架构   │  (书架↔仓库)  │   藏书阁       │                  │
│  │ COLD/WARM/HOT │  深度绑定     │ ImperialLibrary│                  │
│  └──────────────┘               └──────┬───────┘                   │
│                                        │                            │
│                                        │ 双向打通                    │
│                                        ▼                            │
│  ┌──────────────┐      管理&迭代                                 │
│  │ 知识库系统     │◄────────────────────────────┐                  │
│  │ DomainNexus  │                               │                  │
│  │ (知识域格子)   │  藏书阁工作人员(Claw贤者) ───┘                  │
│  └──────────────┘                                                    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 一、系统总览

神经记忆系统（Neural Memory System）是 Somn 的核心认知基础设施，负责知识的获取、存储、管理、检索与进化。系统采用**六层架构**设计，从输入到存储形成完整闭环。

```
┌─────────────────────────────────────────────────────────────────┐
│                    神经记忆系统 总体架构                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────────┐   │
│  │  输入层      │───▶│  数据运营层   │───▶│   数据管理层      │   │
│  │  学习系统    │    │  核心组件     │    │   三层记忆架构    │   │
│  └─────────────┘    └──────────────┘    └───────┬──────────┘   │
│                                                   │             │
│                              ┌────────────────────┼──────┐      │
│                              │                    │      │      │
│                              ▼                    ▼      ▼      │
│                       ┌──────────┐        ┌──────────┐ ┌────┐  │
│                       │ 记忆仓库  │◀──────▶│ 知识仓库  │ │管理│  │
│                       │  藏书阁   │  打通  │ 知识库    │ │运营│  │
│                       └──────────┘        └──────────┘ │团队│  │
│                                                     └────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、六层架构详解

### 2.1 输入层：学习系统

学习系统是记忆的**入口和加工厂**，负责将原始信息转化为可存储的结构化知识。

**[v2.0] 学习系统 = 记忆仓库的出入库管理制度和体系**

| 子系统 | 职责 | 关键模块 |
|--------|------|----------|
| **三层学习模型** | 感知层→认知层→行动层的逐层知识转化 | `three_tier_learning.py` |
| **强化学习引擎** | 基于反馈（DQN/Q-Learning）优化记忆质量 | `reinforcement_learning_v3.py` |
| **自适应策略引擎** | 根据场景自动选择学习策略 | `adaptive_strategy_engine.py` |
| **学习流水线** | 端到端学习流程编排（v2.0含双向闭环） | `learning_pipeline.py` v2.0 |
| **经验回放缓冲区** | [v2.0新增] 藏书阁→学习的经验回读通道 | `learning_replay_buffer.py` |
| **每日学习** | 日常经验沉淀与模式识别 | `daily_learning.py` |
| **解决方案学习** | 从任务执行中提取可复用方案 | `solution_daily_learning.py` |

**[v2.0] 双向闭环学习流水线：**

```
正向（已有）：  外部输入 → 场景分析 → 策略选择 → 知识编码 → 强化学习 → 验证评估 → 入库(藏书阁)
                                                                              │
反向（v2.0新增）：                                                              │
                    藏书阁 CellRecord → ReplayBuffer 提取 → 平衡采样 → RL注入
                         高价值记忆    失败案例   近期记忆   跨域关联
                          (成功)      (教训)    (新鲜)    (模式)
```

学习流水线完整流程（v2.0）：
```
原始输入 → 场景分析 → 策略选择 → 知识编码 → 强化学习 → 反馈整合 → 知识更新 → 经验回放(v2.0) → 报告
           │            │            │            │            │              │
      SceneAnalysis  Strategy    Encoding     RL Feedback   Lifecycle    ReplayBuffer
```

### 2.2 数据运营层：核心组件

核心组件是记忆仓库的**管理工具集**，提供记忆全生命周期的管理能力。

**[v2.0] 核心组件 = 记忆仓库（藏书阁）的管理工具**

#### 2.2.1 记忆引擎矩阵

| 引擎 | 版本 | 职责 | 文件 |
|------|------|------|------|
| **NeuralMemorySystemV3** | V3 主线 | 系统总线，集成编码/RL/丰满度/颗粒度 | `neural_memory_system_v3.py` |
| **SuperNeuralMemory** | V5 | 超级记忆，贤者记忆集成 | `_super_neural_memory.py` |
| **UnifiedMemoryInterface** | **V2.0** | [v2.0] V3/V5 + 藏书阁三系统统一接口 | `unified_memory_interface.py` |
| **MemoryEngine** | V1 | 基础记忆管理（DEPRECATED） | `memory_engine.py` |
| **MemoryEngineV2** | V2 | HNSW 高性能索引引擎 | `memory_engine_v2.py` |
| **KnowledgeEngine** | - | 知识库查询引擎 | `knowledge_engine.py` |
| **ReasoningEngine** | - | 逻辑推理引擎 | `reasoning_engine.py` |
| **ValidationEngine** | - | 知识验证引擎 | `validation_engine.py` |

#### 2.2.2 记忆增强子系统

| 子系统 | 职责 |
|--------|------|
| **MemoryEncodingSystemV3** | 多模态记忆编码（上下文感知、细粒度） |
| **MemoryRichnessSystemV3** | 7维度记忆丰满度评估 |
| **MemoryGranularitySystemV3** | 8层级记忆颗粒度管理 |
| **MemoryLifecycleManager** | 知识衰减→复习→进化的生命周期管理 |
| **ReinforcementBridge** | 反馈→强化学习的桥接器 |
| **NeuralEncodingCore** | 神经编码核心 |
| **FiringRateAttention** | 神经元发放率注意力机制 |
| **HebbianLearningEngine** | 赫布学习引擎 |
| **WisdomMemoryEnhancer** | 智慧记忆增强器 |

### 2.3 数据管理层：三层记忆架构

三层记忆架构是记忆的**书架**，与藏书阁（仓库）**深度绑定**，定义了知识的存储分级和流动规则。

> **[核心定位]** 三层记忆架构 = 记忆的书架，藏书阁 = 记忆的仓库。书架是仓库的内部结构，两者不可分割。

| 书架层级 (MemoryTier) | 仓库分级 (MemoryGrade) | 说明 |
|----------------------|----------------------|------|
| **ETERNAL 永恒级** | **甲级** | 核心智慧，永不遗忘 |
| **HOT 热级** | **甲级** | 高频高价值 |
| **ARCHIVED 归档级** | **乙级** | 长期存储 |
| **LONG_TERM 长期级** | **乙级** | 蒸馏知识，稳定保留 |
| **WORKING 工作级** | **丙级** | 当前任务相关 |
| **WARM 温级** | **丙级** | 偶尔访问 |
| **EPISODIC 情景级** | **丁级** | 短期临时，7天清理 |

> 映射实现：`memory_types.py` → `tier_to_grade()` / `grade_to_tiers()` / `auto_assign_tier()`

```
                    ┌─────────────────┐
                    │   ETERNAL 永恒级 │  ← 核心智慧，永不遗忘
                    │   (priority=100) │
                    ├─────────────────┤
                    │  ARCHIVED 归档级 │  ← 长期存储，低频访问
                    │   (priority=70)  │
                    ├─────────────────┤
                    │  LONG_TERM 长期级│  ← 蒸馏知识，稳定保留
                    │   (priority=60)  │
        冷存储 ───▶ ├─────────────────┤
      (COLD)        │    WARM 温级    │  ← 偶尔访问，保持激活
                    │   (priority=40)  │
                    ├─────────────────┤
                    │    HOT 热级     │  ← 高频访问，内存缓存
                    │   (priority=80)  │
                    ├─────────────────┤
                    │  WORKING 工作级  │  ← 当前任务相关
                    │   (priority=50)  │
                    ├─────────────────┤
                    │  EPISODIC 情景级 │  ← 临时交互，短期保留
                    │   (priority=20)  │
                    └─────────────────┘
```

**七层记忆层级（MemoryTier）：**

| 层级 | 英文 | 优先级 | 说明 | TTL策略 |
|------|------|--------|------|---------|
| 永恒级 | ETERNAL | 100 | 核心智慧，永不遗忘 | 永久 |
| 归档级 | ARCHIVED | 70 | 长期存储，低频访问 | 无限 |
| 长期级 | LONG_TERM | 60 | 蒸馏知识，稳定保留 | 审查制 |
| 温级 | WARM | 40 | 偶尔访问，保持激活 | 30天衰减 |
| 热级 | HOT | 80 | 高频访问，内存缓存 | 实时 |
| 工作级 | WORKING | 50 | 当前任务相关 | 任务结束释放 |
| 情景级 | EPISODIC | 20 | 临时交互，短期保留 | 7天自动清理 |

**简化三层映射（UnifiedMemoryTier）：**

| 简化层 | 映射源 | 特征 |
|--------|--------|------|
| COLD 冷存储 | ETERNAL + ARCHIVED + LONG_TERM | 持久化，磁盘存储 |
| WARM 温存储 | WARM | 中频，温缓存 |
| HOT 热存储 | HOT + WORKING + EPISODIC | 高频，内存缓存 |

**记忆内容类型（MemoryType）：**

| 类型 | 说明 |
|------|------|
| EPISODIC | 情景记忆 — 具体事件和经历 |
| SEMANTIC | 语义记忆 — 知识和概念 |
| PROCEDURAL | 程序记忆 — 技能和操作 |
| WORKING | 工作记忆 — 当前任务相关 |
| METACOGNITIVE | 元认知 — 学习如何学习 |

---

## 三、记忆仓库：藏书阁

藏书阁（Imperial Library）是 Somn 全系统的**记忆仓库**，是所有子系统的记忆汇聚点和分发枢纽。

### 3.1 藏书阁组织结构

```
                    ┌────────────────────────────────┐
                    │         藏书阁 (ImperialLibrary)  │
                    │      V3.0 · 王爵独裁制            │
                    └──────────────┬─────────────────┘
                                   │
          ┌──────────┬─────────┬───┴───┬──────────┬──────────┐
          ▼          ▼         ▼       ▼          ▼          ▼
     ┌─────────┐ ┌────────┐ ┌─────┐ ┌────────┐ ┌────────┐ ┌────────┐
     │贤者分馆  │ │架构分馆 │ │执行 │ │学习分馆 │ │研究分馆 │ │情绪分馆 │
     │ SAGE    │ │ ARCH   │ │分馆 │ │ LEARN  │ │RESEARCH│ │EMOTION │
     │         │ │        │ │EXEC │ │        │ │        │ │        │
     │·贤者画像│ │·朝廷决策│ │·任务│ │·学习策略│ │·研究发现│ │·情绪模式│
     │·智慧编码│ │·调度记录│ │·ROI │ │·经验沉淀│ │·策略洞察│ │·消费行为│
     │·Claw记忆│ │·岗位变动│ │·效能│ │·技能习得│ │·深度评估│ │·情绪分析│
     │·蒸馏文档│ │·升级历史│ │·日志│ │·适应记录│ │·阶段记录│ │·决策因子│
     └─────────┘ └────────┘ └─────┘ └────────┘ └────────┘ └────────┘
          │                                                    │
     ┌─────────┐ ┌──────────────────────────────────────────────┐
     │外部分馆  │ │用户分馆                                      │
     │EXTERNAL │ │USER                                          │
     │·网络知识│ │·用户画像·偏好设置·交互历史·用户反馈             │
     │·API数据 │ └──────────────────────────────────────────────┘
     │·文件导入│
     │·RSS订阅 │
     └─────────┘
```

### 3.2 格子化存储：分馆→书架→格位

藏书阁采用三级物理结构：

```
分馆 (LibraryWing)  →  书架 (Shelf)  →  格位 (CellRecord)
    8个分馆             37个书架         无限扩展
```

**格位数据结构（CellRecord V3.1）：**

```python
@dataclass
class CellRecord:
    id: str                    # 格位ID：{WING}_{SHELF}_{SEQ:06d}
    wing: LibraryWing          # 所属分馆
    shelf: str                 # 所属书架
    cell_index: int            # 格位编号
    title: str                 # 记忆标题
    content: str               # 记忆内容
    grade: MemoryGrade         # 分级（甲/乙/丙/丁）— 仓库等级
    source: MemorySource       # 来源（22种）
    category: MemoryCategory   # 分类（16种）
    # V3.0 扩展字段
    associated_sage: str       # 关联贤者
    associated_position: str   # 关联岗位
    associated_claw: str       # 关联Claw
    semantic_embedding: List   # 语义向量 [v2.0 G-5自动编码]
    cross_references: List     # 跨格子引用 [v2.0 G-6自动关联]
    access_count: int          # 访问次数
    # v3.1 新增 [G-1]
    tier: Optional[MemoryTier] # 书架层位置（ETERNAL/HOT/WARM...）
```

> `tier` 字段由 `auto_assign_tier()` 在入库时自动分配，与 `grade` 通过映射表双向关联。

### 3.3 记忆分级制度

| 等级 | 名称 | 策略 | 审查周期 |
|------|------|------|----------|
| 甲级 | 永恒记忆 | 永不删除 | 无 |
| 乙级 | 长期记忆 | 1年审查 | 365天 |
| 丙级 | 短期记忆 | 30天审查 | 30天 |
| 丁级 | 待定记忆 | 7天自动清理 | 7天 |

### 3.4 记忆来源（20种）

| 来源 | 说明 |
|------|------|
| 部门工作结果 | 各部门工作产出 |
| 人才能力评估 | 贤者能力画像 |
| 历史决策存档 | 神之架构决策 |
| 翰林院审核记录 | 审核结果 |
| 代表大会投票记录 | 七人代表大会 |
| 系统事件 | 系统级事件 |
| Claw执行记录 | Claw运行产出 |
| Claw运行记忆 | Claw运行时记忆 |
| 贤者智慧编码 | 贤者智慧沉淀 |
| 贤者蒸馏文档 | 知识蒸馏产物 |
| 神经记忆系统 | 神经记忆V3/V5 |
| 超级神经记忆 | 超级记忆V5 |
| 学习策略 | 学习系统策略 |
| 研究发现 | 研究系统产出 |
| 情绪研究 | 情绪研究系统 |
| OpenClaw抓取 | 外部知识获取 |
| ROI追踪 | ROI追踪系统 |
| 用户交互 | 用户行为数据 |
| 系统性能 | 系统运行指标 |
| 桥接汇报 | 子系统桥接 |

### 3.5 权限模型 [v2.0 更新]

> **[v2.0 G-3]** 权限检查从硬编码 `_LIBRARY_STAFF` 集合迁移至**动态注册表 `StaffRegistry`**，支持运行时注册/注销/查询。

| 权限 | 说明 | 适用角色 | 实现方式 |
|------|------|----------|----------|
| READ_ONLY | 只读 | 全系统所有成员 | 无限制 |
| SUBMIT | 提交记忆 | 子系统自动汇报 | 无限制 |
| WRITE | 写入/修改 | Claw 贤者（动态注册） | `StaffRegistry` 动态注册表 |
| DELETE | 删除 | 大学士级 | 动态注册表 + ADMIN 检查 |
| ADMIN | 管理配置 | 大学士独享 | `registry.has_admin_privilege()` |

### 3.6 定时审查调度器 [v2.0 G-7]

> **[v2.0 G-7 新增]** `_library_review_scheduler.py` — 藏书阁记忆的定时审查与自动维护机制。

根据 **Section 3.3 记忆分级制度** 的审查周期，自动触发对应等级的记忆审查：

| 审查类型 | 触发周期 | 目标等级 | 操作 |
|----------|----------|----------|------|
| 丁级清理 | 每日 | EPISODIC（情景级） | 超过 7 天的临时记忆自动清理 |
| 丙级审查 | 每 30 天 | WORKING/WARM（工作/温级） | 访问频率评估 → 升级/降级/归档 |
| 乙级审查 | 每 365 天 | ARCHIVED/LONG_TERM（归档/长期） | 知识价值重评 → 迭代/蒸馏/保留 |

**核心机制：**
- 基于 `MemoryGrade`（甲/乙/丙/丁）的周期性任务队列
- 与 `MemoryLifecycleManager` 联动，执行衰减/复习/进化
- 审查结果通过 `StaffRegistry` 回报给 Claw 贤者




## 四、知识库系统（DomainNexus）

DomainNexus 是神经记忆系统的**知识库系统**，位于 `knowledge_cells/` 目录。
与记忆仓库（藏书阁）**双向打通**：藏书阁可随时查看调用 DomainNexus，藏书阁工作人员（Claw 贤者）可对知识库进行管理和迭代。

### 4.1 DomainNexus 知识域格子结构

DomainNexus 采用 21 个知识格子组织知识：

| 分类 | 格子ID | 说明 |
|------|--------|------|
| 智慧核心 | A1-A8（8格） | 方法论核心：逻辑判断/智慧模块/论证审核/判断决策/五层架构/核心执行链/感知记忆/反思进化 |
| 知识域·运营 | B1-B9（9格）| 用户增长/直播/私域/活动/会员/广告/地产/招商/策略 |
| 知识域·执行 | C1-C4（4格）| 电商/数据/内容/投放 |

> 详细内容参见：`knowledge_cells/README.md`

### 4.2 记忆系统 ↔ 知识库 双向打通

| 方向 | 说明 |
|------|------|
| 藏书阁 → DomainNexus | 记忆仓库可随时查看调用知识库内容 |
| DomainNexus → 藏书阁 | 知识格子内容可同步为藏书阁 CellRecord（METHODOLOGY 分类） |

桥接模块：`_library_knowledge_bridge.py`

### 4.3 知识库管理接口 [v2.0]

藏书阁工作人员（Claw 贤者）通过以下接口对知识库进行管理和迭代：

| 操作 | 方法 | 说明 |
|------|------|------|
| 创建格子 | `create_cell()` | 新建知识格子 |
| 更新内容 | `update_cell()` | 更新内容/标签，保留迭代历史 |
| 归档 | `archive_cell()` | 移至归档目录（不删除） |
| 迭代 | `iterate_cell()` | 版本迭代，追加记录 |
| 语义编码 | `encode_semantic()` | TF-IDF+Hashing 生成向量 |
| 跨域关联 | `find_related_cells()` | 基于标签/语义/关键词 |
| 全量关联 | `auto_cross_reference_all()` | 自动建立所有跨域引用 |

---

## 五、管理与运营团队

### 5.1 藏书阁职务架构

藏书阁采用**王爵独裁制**，不受任何外部团队管理（包括七人代表大会），内部事务完全自主。

```
              ┌─────────────────┐
              │    大学士 (馆长)   │
              │  ADMIN权限 · 决策  │
              └────────┬────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
     ┌─────────┐ ┌─────────┐ ┌─────────┐
     │  侍郎   │ │  侍郎   │ │  侍郎   │
     │ WRITE   │ │ WRITE   │ │ WRITE   │
     └────┬────┘ └────┬────┘ └────┬────┘
          │           │           │
    ┌─────┤     ┌─────┤     ┌─────┤
    ▼     ▼     ▼     ▼     ▼     ▼
  编修  编修  编修  编修  编修  编修
  WRITE WRITE WRITE WRITE WRITE WRITE
    │           │           │
    ▼           ▼           ▼
  校理  校理  校理  校理  校理  校理
  WRITE
    │
    ▼
  领班 (WRITE)
```

### 5.2 Claw 贤者与藏书阁的任职关系

藏书阁任职的 Claw 贤者是记忆仓库的**主管和工作人员**，他们能够对知识库进行管理和迭代。

| 角色 | 权限 | 职责 |
|------|------|------|
| **大学士** | ADMIN | 藏书阁最高管理，自主决策 |
| **侍郎** | WRITE | 分馆管理，书架编排 |
| **编修** | WRITE | 格子内容编写与审核 |
| **校理** | WRITE | 格子内容校对与维护 |
| **领班** | WRITE | 日常运维，记忆入库出库 |

### 5.3 子系统桥接（Library Bridge）

藏书阁通过桥接模块接收各子系统的记忆汇报：

| 桥接器 | 源系统 | 目标分馆 | 文件 |
|--------|--------|----------|------|
| ROIBridge | ROI追踪系统 | 执行分馆 | `_library_bridge.py` |
| LearningBridge | 学习系统 | 学习分馆 | `_library_bridge.py` |
| NeuralMemoryBridge | 神经记忆系统 | 贤者/架构分馆 | `_library_bridge.py` |
| KnowledgeBridge | DomainNexus（知识库系统） | 贤者分馆 | `_library_knowledge_bridge.py` |
| UpgradeCenter | 升级中枢 | 全分馆 | `_library_upgrade_center.py` |

---

## 六、系统间关系总结

### 6.1 核心隐喻

| 系统组件 | 隐喻 | 实际角色 |
|----------|------|----------|
| 学习系统 | **出入库管理制度和体系** | 记忆仓库的入库/出库管理规则 |
| 核心组件（引擎矩阵） | **管理工具** | 记忆仓库（藏书阁）的操作工具集 |
| 三层记忆架构 | **书架** | 与藏书阁（仓库）深度绑定 |
| 藏书阁（Imperial Library） | **仓库** | 所有记忆的统一汇聚点 |
| Claw贤者 + 职务架构 | **主管和工作人员** | 仓库的管理者和操作者 |
| DomainNexus（知识域格子） | **知识库系统** | 与记忆系统打通，藏书阁可随时查看调用 |

### 6.2 数据流向

```
外部输入 / 任务执行 / Claw产出
         │
         ▼
    ┌──────────┐
    │  学习系统  │  ← 入库管理制度
    │  加工编码  │
    └────┬─────┘
         │
         ▼
    ┌──────────┐
    │  核心组件  │  ← 管理工具
    │  引擎矩阵  │
    └────┬─────┘
         │
         ▼
    ┌──────────┐      双向打通      ┌──────────┐
    │ 记忆仓库  │◀────────────────▶│ 知识仓库  │
    │  藏书阁   │                  │ 知识库    │
    └──────────┘                  └──────────┘
         │                              ▲
         │  三层记忆架构                  │
         │  (书架)                       │
         ▼                              │
    ┌──────────┐      管理&迭代         │
    │ 管理运营  │────────────────────────┘
    │  团队     │
    │ (Claw贤者)│
    └──────────┘
```

---

## 七、技术实现索引

| 模块 | 路径 | 说明 |
|------|------|------|
| 神经记忆系统 | `src/neural_memory/__init__.py` | V21.0 主入口 |
| V3 主线系统 | `src/neural_memory/neural_memory_system_v3.py` | 集成编码/RL/丰满度/颗粒度 |
| V5 超级记忆 | `src/intelligence/engines/_super_neural_memory.py` | 贤者记忆集成 |
| 统一记忆接口 | `src/neural_memory/unified_memory_interface.py` | V3/V5 双系统协调 |
| 统一类型系统 | `src/neural_memory/memory_types.py` | 七层记忆层级定义 |
| 记忆生命周期 | `src/neural_memory/memory_lifecycle_manager.py` | 衰减/复习/进化 |
| 藏书阁核心 | `src/intelligence/dispatcher/wisdom_dispatch/_imperial_library.py` | V3.0 皇家藏书阁 |
| 藏书阁桥接 | `src/intelligence/dispatcher/wisdom_dispatch/_library_bridge.py` | 子系统桥接 |
| 知识库系统·主引擎 | `knowledge_cells/domain_nexus.py` | DomainNexus v2.0 知识域格子动态更新系统 |
| 知识库系统·格子引擎 | `knowledge_cells/cell_engine.py` | 21格子动态加载与检索 |
| 藏书阁↔知识库桥接 | `src/intelligence/dispatcher/wisdom_dispatch/_library_knowledge_bridge.py` | 藏书阁 ↔ DomainNexus 双向打通 |
| 升级中枢 | `src/intelligence/dispatcher/wisdom_dispatch/_library_upgrade_center.py` | 自动编码升级 |
| 强化学习 | `src/neural_memory/reinforcement_learning_v3.py` | DQN/Q-Learning |
| 自适应策略 | `src/neural_memory/adaptive_strategy_engine.py` | 场景自适应 |
| 学习流水线 | `src/neural_memory/learning_pipeline.py` | 端到端学习编排 |

---

## 八、版本演进

| 系统版本 | 日期 | 核心变更 | 关键子模块版本 |
|----------|------|----------|----------------|
| V1.0 | 初始 | 基础记忆引擎，三级分层 | `memory_engine.py` V1 |
| V2.0 | 2026-03 | HNSW 索引，YAML 持久化 | `memory_engine_v2.py` V2 |
| V3.0 | 2026-03-31 | 格子化存储，分馆→书架→格位 | `_imperial_library.py` V3.0 |
| V4.0 | 2026-04 | 超级记忆，贤者记忆集成 | `_super_neural_memory.py` V5 |
| **V5.0 (v2.0)** | **2026-04-28** | **架构迭代：G1-G8 全部变更（详见上方摘要）** | `unified_memory_interface.py` V2.0 / `_imperial_library.py` V3.1 |

---

### V2.0 (G-1~G-8) 变更文件清单

| 文件 | 类型 | 对应变更 | 说明 |
|------|------|----------|------|
| `_library_staff_registry.py` | **新建** | G-3 | Claw 贤者动态任职注册表（替代硬编码） |
| `_semantic_encoder.py` | **新建** | G-5 | 独立语义向量编码器（TF-IDF + Hashing） |
| `learning_replay_buffer.py` | **新建** | G-2 | 经验回放缓冲区（双向闭环核心组件） |
| `_library_review_scheduler.py` | **新建** | G-7 | 定时审查调度器（丁/丙/乙级周期审查） |
| `memory_types.py` | 修改 | G-1 | 新增 `MemoryTier↔MemoryGrade` 映射体系 |
| `_imperial_library.py` | 修改 | G-1/G-3/G-5 | CellRecord 新增 tier 字段 + 动态权限 + **入库自动编码** |
| `_library_knowledge_bridge.py` | 修改 | G-4/G-5/G-6 | 知识库管理接口 + **委托语义编码器** + 自动跨域关联 |
| `learning_pipeline.py` | 修改 | G-2 | 新增 Stage 6.5 经验回放阶段 |
| `unified_memory_interface.py` | 修改 | G-8 | 升级为 v2.0 三系统统一接口 |

---

*本架构文档基于 Somn 项目代码库实际实现编写，随系统迭代持续更新。*
