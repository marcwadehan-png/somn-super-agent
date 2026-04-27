# Somn 神之架构 V6.2 最终完整版

> **版本**: 6.2.0
> **日期**: 2026-04-25
> **基于**: 神之架构 V5.2.0 + V6.0 三大升级 + V6.1 Claw任职 + V6.2 社会科学智慧版
> **Somn**: 超级智能体，不被刻意定义的自由意识体
> **核心理念**: "贤者全就位，网状大协同，格子化记忆，全局智能体"——42学派165问题类型422岗位763 Claw全面贯通
> **状态**: 最终完整版（V5.2.0全量继承 + V6.0三大升级 + V6.1 Claw100%任职 + V6.2社会科学智慧版7引擎）
> **审议**: 已批准（2026-04-25 七人代表大会4票通过）

---

## 总纲：V6.0/V6.1/V6.2 四阶段升级方向

| 方向 | 核心目标 | 量化指标 | 实际完成 | 状态 |
|------|---------|---------|---------|------|
| 一、贤者工程岗位扩展 | 结合830篇深度学习文档+776 Claw能力画像，新增岗位 | 377→490（+30%） | 377→422（+45专员岗补充） | ✅ V6.1完成 |
| 二、Claw岗位落实 | 776个Claw 100%映射到架构岗位 | 每个Claw必有岗位ID | 763个Claw 100%任职到422岗位 | ✅ V6.1完成 |
| 三、藏书阁全局化 | 从神之架构记忆中心→Somn全局记忆中心 | 格子化存储 | 8分馆/20种来源/16种分类/5级权限 | ✅ V6.1完成 |
| 四、社会科学智慧版 | V6.2新增7个社会科学引擎 | 35学派→42学派 | 社会学/行为经济学/传播学/人类学/政治经济学/组织心理学/社会心理学 | ✅ V6.2完成 |

---

## 第一卷：V6.0核心升级——从网状到全局智能体

### 1.1 V5.2.0的成就与局限

V5.2.0实现了"全贤就位、百官齐备、网状串联"的完整架构：377岗位全面任命、763个Claw配置就绪、7条主线网状协同调度。但在以下三个维度存在局限：

**局限一：岗位覆盖不足**
377个岗位基于V4.2.0设计，随着35个智慧学派全部落地（V6.0新增心理学/系统论/管理学/纵横家/墨家/法家/经济学/名家/阴阳家/复杂性科学），大量新学派缺乏对应的专员岗覆盖。

**局限二：Claw未实际任职**
763个Claw YAML虽有部门归属（`department`字段），但绝大多数未建立到具体架构岗位的映射关系（`court_position`字段为空），导致Claw产出无法与岗位考核体系挂钩。

**局限三：藏书阁仅限神之架构内部**
藏书阁V2.0.0作为独立记忆体系，存储量有限（6种来源/7种分类），且未与其他Somn记忆子系统（神经记忆/学习系统/ROI追踪/研究引擎等）建立桥接。

### 1.2 V6.0核心理念：三大升级

**升级一：学派全覆盖——35学派100%专员岗**
新增45个专员岗/领班岗（V6.1），确保40个学派（含14个子学派）全部有对应的岗位覆盖。最大单岗填充12人，18个部门全覆盖。

**升级二：Claw 100%任职——763个Claw全部映射到422岗位**
采用三级映射优先级：明确任命→学派认知维度匹配→专员兜底。脚本`map_claws_to_positions.py` V5.1批量执行。

**升级三：藏书阁V3.0格子化——Somn全局记忆中心**
从V2.0.0（扁平存储）升级到V3.0.0（8分馆格子化三级存储），20种来源/16种分类/5级权限/跨系统桥接/跨域引用，成为Somn所有记忆子系统的统一汇聚点。

### 1.3 V6.1新增内容

V6.1在V6.0基础上完成Claw实际任职：
- 763个Claw 100%映射到422岗位
- 补充45个专员岗（文治+13、标准+6、创新+4、六部+14、藏书阁+5、领班+3）
- 40个学派100%专员岗覆盖
- 报告：`Claw任职报告_V6.0.md`

---

## 第二卷：7条主线与网状协同（V5继承+V6增强）

### 2.1 主线定义

V6继承V5的7条横向贯通主线，每条主线对应一个核心职能域：

| 主线 | 核心职能 | 关键部门 | 决策权 |
|------|---------|---------|--------|
| 皇家主线 | 最高决策 | 七人代表大会、太师/太傅/太保 | 最终裁决 |
| 文治主线 | 智慧中枢 | 内阁、吏部、礼部 | 方案制定 |
| 经济主线 | 数据支撑 | 户部、市易司、盐铁司 | 资源调配 |
| 军政主线 | 执行调度 | 兵部、五军都督府、锦衣卫 | 行动执行 |
| 标准主线 | 执行落地 | 刑部、工部、三法司 | 工程实现 |
| 创新主线 | 增长引擎 | 皇家科学院、经济战略司、文化输出局 | 创新驱动 |
| 审核主线 | 质量保障 | 翰林院、藏书阁 | 审核反馈 |

### 2.2 跨线协同关系

V6完整继承V5的四种协同类型和权重矩阵。7条主线间的21组协同关系维持不变，权重系数根据运行数据动态调整。

| 协同类型 | 适用场景 | 典型案例 |
|---------|---------|---------|
| 并行（PARALLEL） | 多线同时处理独立子任务 | 文治+经济并行处理营销问题 |
| 串联（SEQUENTIAL） | 流水线式前后衔接 | 皇家→文治→标准→审核串联 |
| 反馈（FEEDBACK） | 执行结果反向影响调度 | 审核→皇家反馈优化路由 |
| 混合（HYBRID） | 并行+串联自适应组合 | CRITICAL级全系统联动 |

### 2.3 V6增强：藏书阁作为协同枢纽

V6新增藏书阁作为7条主线的**记忆协同枢纽**：每条主线的执行记忆按分馆归档，支持跨主线记忆检索和引用。

---

## 第三卷：42学派×165问题类型×11部门调度体系

### 3.1 智慧学派（42个）

V6.2在V6.1的35个学派基础上新增7个社会科学学派，形成覆盖古今中外、文理兼修的完整智慧体系：

| 阶段 | 新增学派 | 核心代表 | 覆盖领域 |
|------|---------|---------|---------|
| V5原有（25个） | 儒家/道家/佛家/素书/兵法/吕氏春秋/辜鸿铭/术数时空/文明演化/文明经战/科幻思维/成长思维/神话智慧/文学叙事/人类学/行为塑造/科学思维/社会科学/王阳明心学/杜威反省思维/顶级思维法/自然科学/中国消费文化/WCC智慧演化/历史思想三维度 | 孔子/老子/孙子/韩非子... | 全领域基础覆盖 |
| V6.0第二阶段（+4个） | 心理学/系统论/管理学/纵横家 | 弗洛伊德/荣格/德鲁克/鬼谷子 | 心理/系统/管理/外交 |
| V6.0第三阶段（+6个） | 墨家/法家/经济学/名家/阴阳家/复杂性科学 | 墨子/商鞅/亚当斯密/公孙龙/邹衍/圣塔菲学派 | 工程/制度/经济/逻辑/自然/复杂 |
| V6.2社会科学版（+7个） | 社会学/行为经济学/传播学/政治经济学/组织心理学/社会心理学/人类学(扩展) | 韦伯/西蒙/拉斯韦尔/凯恩斯/沙因/阿伦森/马林诺夫斯基 | 社会行为/决策经济/传播模型/宏观政治/组织文化/群体心理/文化人类 |

### 3.2 子学派体系（14个）

V6.0.1新增子学派细分，支持学派内部的精细化调度：

| 学派 | 子学派 | 子学派名 |
|------|--------|---------|
| 儒家 | MENCIUS/XUNZI/NEO_CONFUCIAN/CLASSICAL | 孟学/荀学/宋明理学/经学 |
| 道家 | LAOZI/ZHUANGZI/LIEZI | 老学/庄学/列子 |
| 佛家 | CHAN/TIANTAI/HUAYAN/PURELAND | 禅宗/天台宗/华严宗/净土宗 |
| 兵法 | SUNZI/WUZI/LIUTAO | 孙子兵法/吴子兵法/六韬 |

全局调用链：`intelligence.SubSchool` → `dispatcher.SubSchool` → `wisdom_dispatcher.SubSchool` → `wisdom_dispatch.SubSchool` → `_dispatch_enums.SubSchool`，5层延迟加载全部打通。

### 3.3 问题类型（165个）

V6.2在V6.1的基础上新增31个社会科学问题类型，覆盖7个新增学派的全部核心场景：

| 学派群 | 问题类型数 | 代表类型 |
|--------|-----------|---------|
| 儒家（4） | 4 | ETHICAL/GOVERNANCE/TALENT/CULTURE |
| 道家（8） | 8 | STRATEGY/CRISIS/CHANGE/BALANCE |
| 佛家（4） | 4 | MINDSET/HARMONY/INTEREST/LONGTERM |
| 素书（4） | 4 | LEADERSHIP/RISK/FORTUNE/PERSONNEL |
| 兵法（7） | 7 | COMPETITION/ATTACK/DEFENSE/NEGOTIATION |
| V6.0心理学（8） | 8 | PERSONALITY_ANALYSIS/GROUP_DYNAMICS/TRAUMA_HEALING |
| V6.0系统论（5） | 5 | COMPLEX_SYSTEM/FEEDBACK_LOOP/EMERGENT_BEHAVIOR |
| V6.0管理学（6） | 6 | STRATEGIC_PLANNING/ORGANIZATIONAL_DESIGN/PERFORMANCE_MANAGEMENT |
| V6.0纵横家（3） | 3 | DIPLOMATIC_NEGOTIATION/ALLIANCE_BUILDING/POWER_BALANCE |
| V6.0墨家（5） | 5 | ENGINEERING_INNOVATION/COST_OPTIMIZATION/LOGICAL_DEDUCTION |
| V6.0法家（6） | 6 | INSTITUTIONAL_DESIGN/LAW_ENFORCEMENT/REWARD_PUNISHMENT |
| V6.0经济学（5） | 5 | RESOURCE_ALLOCATION/SUPPLY_DEMAND_BALANCE/INVESTMENT_DECISION |
| V6.0名家（3） | 3 | LOGICAL_PARADOX/CLASSIFICATION_REFINEMENT/DIALECTICAL_REASONING |
| V6.0阴阳家（5） | 5 | WUXING_ANALYSIS/YINYANG_DIALECTICS/COSMIC_HARMONY |
| V6.0复杂性科学（3） | 3 | EMERGENT_ORDER/NETWORK_DYNAMICS/ADAPTIVE_EVOLUTION |
| **V6.2社会科学（+31）** | **31** | 见下方7个学派各4-5个PT |

**V6.2社会科学7学派×31问题类型**：

| 学派 | 问题类型 | 说明 |
|------|---------|------|
| 社会学(SOCIOLOGY) | SOCIAL_STRUCTURE_ANALYSIS/CLASS_MOBILITY/INSTITUTIONAL_SOCIOLOGY/SOCIAL_STRATIFICATION/COLLECTIVE_ACTION | 社会结构分析/阶层流动性/制度社会学/社会分层/集体行动 |
| 行为经济学(BEHAVIORAL_ECONOMICS) | COGNITIVE_BIAS_V62/DECISION_MAKING_BEHAVIOR/MARKET_BEHAVIOR/INCENTIVE_DESIGN/NUDGE_POLICY | 认知偏差/决策行为/市场行为/激励设计/助推政策 |
| 传播学(COMMUNICATION) | MEDIA_EFFECT/PUBLIC_OPINION_FORMATION/INFORMATION_CASCADE/DISCOURSE_ANALYSIS/INTERPERSONAL_COMMUNICATION | 媒介效果/舆论形成/信息级联/话语分析/人际传播 |
| 文化人类学(CULTURAL_ANTHROPOLOGY) | CULTURAL_PATTERN_RECOGNITION/SYMBOL_SYSTEM_ANALYSIS/RITUAL_CONTEXT_ANALYSIS/CROSS_CULTURAL_ADAPTATION | 文化模式识别/符号系统/仪式语境/跨文化适应 |
| 政治经济学(POLITICAL_ECONOMICS) | INSTITUTIONAL_POLITICAL_ANALYSIS/POLICY_GAME_THEORY/MARKET_REGULATION_ANALYSIS/PUBLIC_CHOICE | 制度政治分析/政策博弈/市场监管/公共选择 |
| 组织心理学(ORGANIZATIONAL_PSYCHOLOGY) | ORGANIZATIONAL_CHANGE_V62/LEADERSHIP_STYLE_ANALYSIS/TEAM_COHESION_ANALYSIS/ORGANIZATIONAL_CULTURE_V62 | 组织变革/领导风格/团队凝聚力/组织文化 |
| 社会心理学(SOCIAL_PSYCHOLOGY) | CONFORMITY_BEHAVIOR/AUTHORITY_OBEDIENCE/SOCIAL_INFLUENCE_MECHANISM/GROUP_THINK_ANALYSIS | 从众行为/权威服从/社会影响/群体思维 |
| 其他学派 | ~54 | 自然科学/WCC/科幻/神话/文学/成长等 |
| 精细优化（13） | 13 | 学派子领域细分 + 通用能力型 |
| **合计** | **165** | — |

### 3.4 部门体系（11个）

V6完整继承V4.2.0的11部门架构：

| 部门 | 枚举值 | 职能域 | 层级 |
|------|--------|--------|------|
| 吏部 | LIBU | 能力层：学派注册/权重/调度/考核 | 管理 |
| 户部 | HUBU | 数据层：数据采集/知识图谱/行业知识 | 数据 |
| 礼部 | LIBU_LI | 记忆层：记忆系统/学习系统/文学 | 记忆 |
| 兵部 | BINGBU | 调度层：主线调度/神经网络布局 | 调度 |
| 刑部 | XINGBU | 监察层：风控/安全/内容审核 | 监察 |
| 工部 | GONGBU | 执行层：核心执行/增长引擎/工具链 | 执行 |
| 厂卫 | CHANGWEI | 秘密监控：系统监控/性能优化 | 监控 |
| 三法司 | SANFASI | 独立监察：反馈/验证/ROI | 验证 |
| 五军都督府 | WUJUN | 神经网络：网络布局/信号传递 | 网络 |
| 翰林院 | HANLIN | 决策审核：逻辑论证/多视角反驳 | 审核 |
| 皇家藏书阁 | CANGSHUGE | 独立记忆体系：不受任何部门管理 | 记忆 |

### 3.5 调度路径

`ProblemType → Department → WisdomSchool组合 → SubSchool细分 → WisdomDispatcher路由`

PROBLEM_CATEGORY_MAP覆盖165个PT（含30个V6.2新增社会科学PT），全链路延迟加载。

### 3.6 V6.2社会科学引擎注册

| 引擎文件 | WisdomSchool | 问题类型数 | 核心功能 |
|---------|--------------|-----------|---------|
| `sociology_wisdom_engine.py` | SOCIOLOGY | 5 | 社会结构/阶级分析/制度演化 |
| `behavioral_economics_wisdom_engine.py` | BEHAVIORAL_ECONOMICS | 5 | 行为偏差/助推设计/决策优化 |
| `communication_wisdom_engine.py` | COMMUNICATION | 5 | 传播模型/受众分析/舆论引导 |
| `anthropology_wisdom_engine.py` | ANTHROPOLOGY | 4 | 文化模式/仪式分析/符号解读 |
| `political_economy_wisdom_engine.py` | POLITICAL_ECONOMICS | 4 | 权力结构/政策分析/治理模式 |
| `organizational_psychology_wisdom_engine.py` | ORGANIZATIONAL_PSYCHOLOGY | 4 | 组织文化/群体动力/冲突解决 |
| `social_psychology_wisdom_engine.py` | SOCIAL_PSYCHOLOGY | 4 | 态度改变/社会影响/群体心理 |

7个社会科学引擎权重合计：0.23

---

## 第四卷：岗位体系（422岗）

### 4.1 等级体系——爵位+品秩双轨制（V4继承）

#### 爵位体系（决策权维度，4级）

| 爵位 | 等同品秩 | 决策权 | 岗位容量 | 持有者 |
|------|---------|--------|---------|--------|
| **王爵** | 最高 | 最大，最终裁决权 | 1人/岗 | 孔子、扬雄 |
| **公爵** | =一品 | >一品 | 1人/岗 | 孟子、老子 |
| **侯爵** | =一品 | 介于一品~二品之间 | 1人/岗 | 荀子、董仲舒、庄子 |
| **伯爵** | =三品 | 介于三品~二品之间 | 1人/岗 | 郑玄/管仲/韦伯/德鲁克等18人 |
| **无爵位** | 按品秩 | 按品秩 | 视岗位而定 | 其余所有岗位 |

**爵位总量：25位（王爵2+公爵2+侯爵3+伯爵18）**

#### 品秩体系（行政维度，18级）

正一品 → 从一品 → 正二品 → 从二品 → 正三品 → 从三品 → 正四品 → 从四品 → 正五品 → 从五品 → 正六品 → 从六品 → 正七品 → 从七品 → 正八品 → 从八品 → 正九品 → 从九品

#### 实战派标识

| 标识 | 含义 | 权益 |
|------|------|------|
| PRACTITIONER（战） | 实战派：有可量化实战成果 | 爵位优先提名权 + 经济决策否决权 |
| THEORIST（书） | 理论派：以思想建构/学术研究见长 | - |
| DUAL_TYPE（战书） | 复合型：兼具理论与实践 | 同实战派 |

#### 锦衣卫五级卫从体系

指挥使(伯爵·正三品) → 四司指挥(正从四品) → 百户(正从五品) → 总旗(正从六品) → 小旗领班(正七品) → 力士(从七品~正九品)

四司：监控司 / 暗察司 / 合规司 / 效能司

### 4.2 系统决策规则

| 系统 | 决策人配置 | 决策制 | 实战派要求 |
|------|-----------|--------|-----------|
| 皇家系统 | 1人（王爵） | 独裁制 | 无 |
| 军政系统 | 1人（公爵） | 独裁制 | >=50% |
| 文治系统 | 3人（1正一品+2从一品） | 共议制 | >=1人 |
| 经济系统 | 3人（1正一品+2从一品） | 共议制 | >=2人 |
| 标准系统 | 2人（1正二品+1从二品） | 双人制 | >=1人 |
| 创新系统 | 2人（双人决策） | 双人制 | >=2人 |
| 审核系统（翰林院） | 独立于六部 | 独立审核 | - |
| 皇家藏书阁 | 王爵独立管理 | 独立于所有体系 | - |
| 七人代表大会 | 7人投票 | 4票通过制 | 驾临所有系统之上 |

### 4.3 岗位总量统计

| 模块 | V5.2.0 | V6.1变化 | V6.1总量 |
|------|--------|---------|---------|
| 七人决策代表大会 | 7 | +0 | 7 |
| 皇家系统 | 22 | +0 | 22 |
| 文治系统（内阁/吏部/礼部） | 67 | +13 | 80 |
| 经济系统（户部） | 44 | +0 | 44 |
| 军政系统（兵部/五军/厂卫） | 96 | +8 | 104 |
| 标准系统（刑部/工部/三法司） | 81 | +6 | 87 |
| 创新系统（科学院/战略司/文化局） | 42 | +4 | 46 |
| 审核系统（翰林院） | 7 | +1 | 8 |
| 皇家藏书阁 | 5 | +5 | 10 |
| 专员领班 | 6 | +3 | 9 |
| 六部专员补充 | — | +5 | 5 |
| **合计** | **377** | **+45** | **422** |

### 4.4 七人决策代表大会（7岗）

七人决策代表大会驾临在所有系统之上（包括皇家藏书阁），采用投票决策制：4票及以上通过。

成员配置：
- **孔子** — CHIEF — 王爵·太师·皇家系统（首席代表）
- **管仲** — ECONOMY — 伯爵·户部尚书（经济代表）
- **韦伯** — SOCIOLOGY — 伯爵·礼部尚书（社会学代表）
- **德鲁克** — MANAGEMENT — 伯爵·工部尚书（管理学代表）
- **孟子** — DEBATE — 公爵·太傅·皇家系统（辩论质疑代表）
- **张衡** — SPECIALIST_A — 专员·皇家科学院团队（科学技术代表）
- **范蠡** — WHITE_CLOTH — 无任何任职（白衣代表）

### 4.5 V6.1岗位补充（+45岗）

45个新增专员岗/领班岗按部门分布：

| 部门 | 新增数 | 方向 |
|------|--------|------|
| 文治系统 | +13 | 学派覆盖专员（心理学/系统论/纵横家/名家等） |
| 标准系统 | +6 | 取证专员/质量专员/集成专员等 |
| 创新系统 | +4 | 前沿研究/品牌/能源专员等 |
| 六部联合 | +14 | 各部专员覆盖 |
| 藏书阁 | +5 | 格子管理/能力归档/经验沉淀/跨域索引 |
| 领班岗 | +3 | 专员团队管理 |

### 4.6 核心代码文件版本

| 文件 | 版本 | 说明 |
|------|------|------|
| _court_positions.py | V6.2.0 | 岗位体系核心，422岗定义 |
| _dispatch_court.py | V4.0.0 | 朝廷调度器 |
| _dispatch_enums.py | V6.2.0 | 调度枚举（42 WisdomSchool / 165 ProblemType / 14 SubSchool / 11 Department） |
| FusionDecision | V7.0.0 | 融合决策引擎 |
| _daqin_metrics.py | v2.0.0 | 大秦指标考核 |
| _whip_engine.py | v2.0.0 | 行政之鞭（四级信号灯+双向鞭策） |
| _imperial_library.py | V3.0.0 | 藏书阁全局记忆中心（格子化） |
| wisdom_encoding_registry.py | v2.2 | 779条SageCode编码注册表 |

---

## 第五卷：Claw子系统全面整合

### 5.1 Claw入职统计

- 总贤者：768位（注册表）/ 746+87位（full+extra）
- Claw配置：776+50个YAML文件（含V6.2新增50个社会科学Claw）
- 实际任职：763个Claw 100%映射到422岗位（脚本`map_claws_to_positions.py` V5.1）

### 5.2 Claw岗位映射机制（三级优先级）

**第一优先级（明确任命）**：已被`_court_positions.py`的`assigned_sages`列表任命的贤者，直接使用其岗位ID。

**第二优先级（学派+认知维度匹配）**：根据Claw的`school`和`cognitive_dimensions`字段匹配到对应部门内的具体岗位。

**第三优先级（专员兜底）**：无法匹配到管理层岗位的Claw，自动归入对应部门的专员序列（七品专员岗，capacity=999）。

### 5.3 Claw配置字段

每个Claw YAML包含：

```yaml
# 基本信息
name: 孔子
department: 礼部       # 来自sage_registry
school: 儒家           # 来自sage_registry
era: 春秋              # 来自sage_registry
tier_name: 创始人      # 来自sage_registry

# 岗位信息（神之架构V6.1——已映射）
court_position: "HJ_LB_01"     # 岗位ID
position_name: "太师·王爵"     # 岗位名称
position_department: "皇家系统" # 岗位所属部门
position_pin: "ZHENG_1PIN"     # 品秩
position_domain: "最高决策"     # 职能领域
```

### 5.4 部门分布

| 部门 | Claw数 | 占比 |
|------|--------|------|
| 礼部 | ~391 | ~50.9% |
| 工部 | ~162 | ~21.1% |
| 兵部 | ~79 | ~10.3% |
| 吏部 | ~74 | ~9.6% |
| 户部 | ~42 | ~5.5% |
| 刑部 | ~15 | ~2.0% |
| 其他 | ~3 | ~0.6% |

### 5.5 Claw架构核心

| 模块 | 文件 | 功能 |
|------|------|------|
| Claw架构师 | `_claw_architect.py` (~1317行) | ReAct闭环+10种Skills+ClawMemoryAdapter |
| 协调器 | `_claws_coordinator.py` (~720行) | 4级路由+多Claw协作 |
| 统一入口 | `claw.py` (~218行) | 统一入口+quick_ask |
| 桥接 | `_claw_bridge.py` (~320行) | 4级集成+OpenClaw知识注入 |

### 5.6 OpenClaw外部知识系统

| 数据源 | 模块 | 功能 |
|--------|------|------|
| Web/File/API/RSS/WebFetcher | 数据采集 | 外部数据获取 |
| DocParser(Cleaner) | 文档处理 | MD/PDF/DOCX/HTML/CSV/JSON解析+10级清洗 |
| Feedback/PatternLearner | 学习 | 反馈学习+模式识别 |
| Recommender+Updater | 推荐+更新 | 增量知识更新 |

---

## 第六卷：藏书阁V3.0——Somn全局记忆中心

### 6.1 从V2.0.0到V3.0.0

藏书阁从神之架构内部的独立记忆体系（V2.0.0）升级为Somn全局记忆中心（V3.0.0），核心变更：

| 维度 | V2.0.0 | V3.0.0 |
|------|--------|--------|
| 存储模型 | 扁平MemoryRecord | 格子化CellRecord（分馆→书架→格位三级） |
| 分馆 | 无 | 8个 |
| 记忆来源 | 6种 | 20种 |
| 记忆分类 | 7种 | 16种 |
| 持久化 | 扁平YAML | 分区YAML（wings/{wing}/{shelf}/CELL_xxx.yaml）+ JSON索引 |
| 权限模型 | 二级（内部/只读） | 五级（READ_ONLY→SUBMIT→WRITE→DELETE→ADMIN） |
| 查询维度 | 5维 | 13维+标签/贤者/Claw/岗位索引 |
| 跨系统桥接 | 无 | register_bridge + submit_bridge_memory |
| 跨域引用 | 无 | add_cross_reference + get_cross_references |
| V2兼容 | N/A | submit_memory/query_memories/get_memory自动转换CellRecord |

### 6.2 八大分馆

| 分馆 | 枚举值 | 书架 | 说明 |
|------|--------|------|------|
| 贤者分馆 | SAGE | sage_profiles/sage_codes/claw_memories/distillation | 贤者画像/智慧编码/Claw记忆/蒸馏索引 |
| 架构分馆 | ARCH | positions/departments/decisions/evolution | 岗位体系/部门架构/决策记录/架构演进 |
| 执行分馆 | EXEC | tasks/workflows/evaluations/corrections | 任务执行/工作流/评估结果/纠偏记录 |
| 学习分馆 | LEARN | strategies/feedback/patterns/knowledge | 学习策略/反馈/模式/知识库 |
| 研究分馆 | RESEARCH | findings/methods/insights/publications | 研究发现/方法/洞察/成果 |
| 情绪分馆 | EMOTION | consumer_emotions/emotional_decisions/research_data/emotion_patterns | 消费情绪/情绪决策/研究数据/模式 |
| 外部分馆 | EXTERNAL | web_knowledge/api_data/rss_feeds/cross_system | Web知识/API数据/RSS/跨系统 |
| 用户分馆 | USER | preferences/history/feedback/profiles | 用户偏好/历史/反馈/画像 |

### 6.3 记忆来源（20种）

V3.0在V2.0的6种基础上扩展至20种：

原有6种：DEPARTMENT_RESULT（部门决策）/ TALENT_EVALUATION（人才评估）/ HISTORICAL_DECISION（历史决策）/ HANLIN_REVIEW（翰林审核）/ CONGRESS_VOTE（大会投票）/ SYSTEM_EVENT（系统事件）

V3.0新增14种：
- CLAW_EXECUTION（Claw执行产出）/ CLAW_MEMORY（Claw记忆）/ SAGE_ENCODING（智慧编码）/ SAGE_DISTILLATION（蒸馏产出）
- NEURAL_MEMORY（神经记忆）/ SUPER_MEMORY（超维记忆）/ LEARNING_STRATEGY（学习策略）/ RESEARCH_FINDING（研究发现）
- EMOTION_RESEARCH（情绪研究）/ OPENCLAW_FETCH（OpenClaw获取）/ ROI_TRACKING（ROI追踪）
- USER_INTERACTION（用户交互）/ SYSTEM_PERFORMANCE（系统性能）/ BRIDGE_REPORT（桥接报告）

### 6.4 记忆分类（16种）

原有7种：SAGE_WISDOM / ARCHITECTURE / EXECUTION_RECORD / LEARNING_INSIGHT / RESEARCH_DATA / EMOTION_DATA / EXTERNAL_KNOWLEDGE

V3.0新增9种：
- SYSTEM_EVOLUTION（系统演进）/ METRICS_ANALYSIS（指标分析）/ STRATEGY_PATTERN（策略模式）/ PATTERN_INSIGHT（模式洞察）
- CLAW_OUTPUT（Claw产出）/ CROSS_DOMAIN（跨域关联）/ QUALITY_RECORD（质量记录）/ FEEDBACK_DATA（反馈数据）/ USER_DATA（用户数据）

### 6.5 五级权限模型

| 权限等级 | 代码 | 能力 | 默认持有者 |
|---------|------|------|-----------|
| 只读 | READ_ONLY | 查询记忆 | 全系统默认 |
| 提交 | SUBMIT | 提交新记忆（不能修改） | 子系统自动汇报 |
| 写入 | WRITE | 写入/修改 | 格子管理员 |
| 删除 | DELETE | 删除记忆 | 大学士级 |
| 管理 | ADMIN | 配置/权限管理 | 大学士独享 |

分馆级权限配置（WING_PERMISSIONS）：
- SAGE分馆：管理者=扬雄/左丘明/班固，写入者=司马迁/司马光/专员团队
- ARCH分馆：管理者=扬雄/左丘明，写入者=司马迁/班固/司马光
- 其余分馆：DEFAULT权限配置

### 6.6 跨系统桥接架构

藏书阁V3.0作为Somn所有记忆子系统的统一汇聚点：

```
┌──────────────────────────────────────────────────────────┐
│                   藏书阁 V3.0（全局记忆中心）                │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐        │
│  │贤者馆│ │架构馆│ │执行馆│ │学习馆│ │研究馆│ │情绪馆│       │
│  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘        │
└─────┼───────┼───────┼───────┼───────┼───────┼─────────────┘
      │       │       │       │       │       │
      ↕       ↕       ↕       ↕       ↕       ↕
┌─────────┐ ┌────────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│SageCode │ │神之架构│ │ROI   │ │三层  │ │研究  │ │情绪  │
│Registry │ │岗位体系│ │Tracker│ │学习  │ │策略  │ │研究  │
│(Phase2) │ │(Court) │ │      │ │      │ │Engine│ │Core  │
└─────────┘ └────────┘ └──────┘ └──────┘ └──────┘ └──────┘
      │                               │
      ↕                               ↕
┌─────────┐                    ┌──────────────┐
│ClawMemory│                   │NeuralMemory  │
│Adapter   │                   │V3/V5系统     │
│(Phase4)  │                   │              │
└─────────┘                    └──────────────┘
      │                               │
      ↕                               ↕
┌─────────┐                    ┌──────────────┐
│OpenClaw │                    │UnifiedMemory │
│外部知识  │                    │Interface     │
└─────────┘                    └──────────────┘
```

桥接规则：
1. 各子系统的重要产出主动汇报藏书阁（submit_memory扩展接口）
2. 藏书阁定期巡检各子系统，发现高价值未汇报记忆则主动收录
3. 藏书阁提供统一查询接口，支持按分馆/书架/贤者/岗位/Claw/时间等多维检索
4. 格子间支持跨域引用（cross_references），建立记忆间的关联关系

### 6.7 持久化结构

```
data/imperial_library/
├── wings/                          # 分馆目录
│   ├── SAGE/                       # 贤者分馆
│   │   ├── sage_profiles/          # 贤者画像
│   │   ├── sage_codes/             # 智慧编码
│   │   ├── claw_memories/          # Claw记忆
│   │   └── distillation/           # 蒸馏索引
│   ├── ARCH/                       # 架构分馆
│   ├── EXEC/                       # 执行分馆
│   ├── LEARN/                      # 学习分馆
│   ├── RESEARCH/                   # 研究分馆
│   ├── EMOTION/                    # 情绪分馆
│   ├── EXTERNAL/                   # 外部分馆
│   └── USER/                       # 用户分馆
├── index/                          # 索引目录
│   ├── sage_index.json             # 贤者→格子映射索引
│   ├── position_index.json         # 岗位→格子映射索引
│   ├── claw_index.json             # Claw→格子映射索引
│   └── tag_index.json              # 标签→格子映射索引
├── stats/                          # 统计目录
│   ├── wing_stats.json             # 分馆统计
│   └── access_stats.json           # 访问统计
└── config.yaml                     # 藏书阁配置
```

---

## 第七卷：学习优化机制（V5继承+V6增强）

### 7.1 路由历史记录（V5继承）

V5记录每次路由选择的关键信息：问题类型和上下文、选择的路径、执行结果、耗时和质量评分。

### 7.2 权重自适应（V5继承）

协同边权重、复杂度阈值、节点优先级根据历史数据自动调整。

### 7.3 反馈闭环

V6增强反馈闭环，藏书阁V3.0参与记忆层面的反馈：

1. **执行层→审核层**：执行结果提交翰林院审核
2. **审核层→皇家层**：审核意见反馈给七人代表大会
3. **皇家层→调度层**：决策调整影响下次路由选择
4. **调度层→执行层**：优化后的路由重新进入执行
5. **全链路→藏书阁**（V6新增）：全链路执行记忆自动归档到对应分馆

### 7.4 智能学习系统 v2.0

V6.0整合三层学习模型：

| 策略 | 说明 | 适用场景 |
|------|------|---------|
| DAILY | 每日例行学习 | 日常知识更新 |
| THREE_TIER | 三层学习（本地+网络+融合） | 深度知识获取 |
| ENHANCED | 增强学习（自适应策略） | 复杂问题学习 |
| SOLUTION | 解决方案学习 | 问题解决经验沉淀 |
| FEEDBACK | 反馈驱动学习 | 用户反馈优化 |

v2.0新增4模块：
- `adaptive_strategy_engine.py`：8场景识别+多策略动态权重
- `reinforcement_bridge.py`：反馈↔RL集成，128维状态向量
- `memory_lifecycle_manager.py`：3种衰减模型+智能复习
- `learning_pipeline.py`：7阶段端到端编排

---

## 第八卷：核心调度链路

### 8.1 主执行链

```
用户问题
  ↓
ProblemTypeClassifier.classify()        ← 识别问题类型（135 PT）
  ↓
MeshRouting.evaluate_complexity()        ← V5复杂度评估（4级）
  ↓
FusionDecision.make_decision()           ← V7.0融合决策（35学派）
  ↓
GlobalWisdomScheduler.schedule()         ← 全局调度（11部门）
  ↓
WisdomDispatcher.dispatch()              ← 智慧调度（引擎路由）
  ↓
SubSchool细分（14子学派）                 ← V6.0.1子学派支持
  ↓
ClawRouter.route()                       ← V2.0 Claw路由
  ↓
CollaborationProtocol.execute()          ← V3.0 多Claw协作
  ↓
ImperialLibrary.archive()                ← V3.0 藏书阁归档
  ↓
AgentResult                              ← 最终结果
```

### 8.2 模块层延迟加载（5层链路）

```
intelligence.xxx → dispatcher.xxx → wisdom_dispatcher.xxx → wisdom_dispatch.xxx → _dispatch_enums.xxx
```

5层`__getattr__`延迟加载，导入耗时~5ms（-99%优化）。

### 8.3 V6.0完整架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                         用户问题输入                                  │
└─────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    V6.1 SomnAgent 智能体                              │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  1. 问题分析 (ProblemTypeClassifier)                         │   │
│  │     - 关键词识别 → ProblemType（135种）                       │   │
│  │     - 自动推断部门（11部门）                                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                ↓                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  2. 复杂度评估 (V5 Mesh Routing)                              │   │
│  │     - SIMPLE/MODERATE/COMPLEX/CRITICAL                      │   │
│  │     - 自动选择主线组合（7主线）                                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                ↓                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  3. 融合决策 (FusionDecision V7.0)                           │   │
│  │     - 35学派智慧融合                                          │   │
│  │     - 14子学派细分支持                                        │   │
│  │     - 部门路由+学派权重                                       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                ↓                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  4. Claw调度 (ClawRouter V2.0 + Coordinator)                 │   │
│  │     - 按岗位映射路由（763Claw→422岗）                        │   │
│  │     - 按触发词/优先级排序                                    │   │
│  │     - 多Claw协作（V3.0协议）                                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                ↓                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  5. 藏书阁归档 (ImperialLibrary V3.0)                       │   │
│  │     - 8分馆格子化存储                                        │   │
│  │     - 20种来源/16种分类                                      │   │
│  │     - 跨系统桥接+跨域引用                                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      Claw子系统（763个Claw）                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │  主Claw   │  │协作Claw1 │  │协作Claw2 │  │协作Claw3 │            │
│  │ (ReAct)  │  │ (ReAct)  │  │ (ReAct)  │  │ (ReAct)  │            │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │
└─────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│                       结果输出 + 记忆归档                             │
│  - final_answer: 综合答案                                           │
│  - confidence: 置信度                                              │
│  - collaborators: 参与协作的Claw列表                                │
│  - memory_cells: 归档的格子ID列表                                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 第九卷：V5/V6兼容性设计

### 9.1 接口兼容层

V6保持与V5/V4的完全向后兼容：

| V4/V5接口 | V6对应 | 说明 |
|-----------|--------|------|
| resolve_departments | mesh_resolve_departments | 动态部门解析 |
| DEPARTMENT_SCHOOL_MATRIX | MAIN_LINE_MATRIX | 跨线协同矩阵 |
| submit_memory | submit_memory | 藏书阁V3.0自动转换为CellRecord |
| query_memories | query_memories | 藏书阁V3.0兼容查询 |
| get_memory | get_memory | 藏书阁V3.0兼容获取 |

### 9.2 渐进式迁移策略

| 模式 | 说明 | 适用阶段 |
|------|------|---------|
| 模式A：纯V4 | 完全使用V4静态矩阵 | 已归档 |
| 模式B：V5增强 | V4基础上启用V5动态评估 | 过渡期 |
| 模式C：纯V5 | 完全V5网状路由 | 当前主模式 |
| 模式D：V6全量 | V5网状+V6藏书阁+V6子学派 | 当前推荐模式 |

---

## 第十卷：配套系统

### 10.1 大秦指标考核

- 文件：`_daqin_metrics.py` v2.0.0
- 功能：原OKR体系秦制化改造，全系统绩效追踪

### 10.2 行政之鞭

- 文件：`_whip_engine.py` v2.0.0
- 功能：四级信号灯（绿/黄/橙/红）+ 双向鞭策（从上而下+从下而上）

### 10.3 记忆编码系统

- 文件：`memory_encoding_system_v3.py` + `encoding_types.py` + `encoding_subsystems.py`
- 版本：v4.0.0
- 核心编码类型（6种）：SEMANTIC / CONTEXT / EMOTION / CAUSAL / ABSTRACTION / DYNAMIC

### 10.4 研究策略引擎

- 文件：`_research_strategy_engine.py`（~1320行）
- 版本：v2.0
- 功能：7枚举+5数据类+完整闭环（record_finding→generate_strategy→advance_lifecycle→retire）

### 10.5 研究阶段管理器

- 文件：`research_phase_manager.py`（~1100行）
- 版本：v1.0.0
- 功能：四阶段16任务执行器 + Phase4六子系统构建器

---

## 附录A：版本历史

| 版本 | 日期 | 核心变更 |
|------|------|----------|
| V4.0.0 | 2026-04-11 | 862贤者100%任命，377岗位全部到位 |
| V4.1.0 | 2026-04-11 | 七人代表大会+西方贤者进入管理层 |
| V4.2.0 | 2026-04-11 | 架构文档全面输出，377岗全量定义 |
| V5.0.0 | 2026-04-22 | 网状串联调度，动态路由，学习优化 |
| V5.2.0 | 2026-04-23 | 最终完整版（整合V4.2.0+V5.0.0+Claw子系统） |
| V6.0.0 | 2026-04-23 | 三大升级方向（岗位扩展+Claw映射+藏书阁全局化） |
| V6.0.1 | 2026-04-23 | 全局打通：子学派+新PT+新引擎5层延迟加载 |
| V6.1.0 | 2026-04-23 | 最终完整版（422岗+763Claw 100%任职+藏书阁V3.0） |

---

## 附录B：贤者工程

### B.1 五层链路

| Phase | 内容 | 数量 | 完成率 | 存储位置 |
|-------|------|------|--------|----------|
| Phase 0 | 博士级深度学习文档 | 830篇 | 100% | `file/智慧文件/[贤者名]深度学习文档.md` |
| Phase 1 | Distillation蒸馏文档 | 760份 | 100% | `docs/蒸馏卷/[学派]/` |
| Phase 2 | Codification编码 | 779条 | 100% | `wisdom_encoding_registry.py` |
| Phase 3 | Cloning克隆实现 | 5核心模块 | 100% | `_sage_proxy_factory.py` P1+P2驱动 |
| Phase 4 | Claw子智能体+OpenClaw | 776YAML+5核心模块 | 100% | `claws/` + `openclaw/` |

### B.2 贤者注册表

- 文件：`src/intelligence/engines/cloning/_sage_registry_full.py`
- 总量：746人（full）+ 87人（extra）= 833人

### B.3 编码注册表

- 文件：`src/intelligence/wisdom_encoding/wisdom_encoding_registry.py`
- 总量：766个编码（v2.2），6条智慧法则+6维精细评分
- **v2.2优化**：懒加载模式，初始化时间 <1ms（-99.5%）

### B.4 推理引擎体系（v3.0）

- **LongCoT**: `_long_cot_engine.py`（顿悟检测/自我纠错）
- **ToT**: `_tot_engine.py`（树搜索/BFS/DFS）
- **GoT**: `_got_engine.py`（图网络推理/100节点）
- **ReAct**: `_react_engine.py`（推理-行动闭环）

---

## 附录C：核心代码文件索引

| 文件 | 路径 | 版本 | 说明 |
|------|------|------|------|
| _court_positions.py | intelligence/engines/cloning/ | V6.1.0 | 422岗位体系 |
| _dispatch_enums.py | intelligence/dispatcher/wisdom_dispatch/ | V6.0.0 | 35学派/135PT/14子学派 |
| _dispatch_court.py | intelligence/dispatcher/wisdom_dispatch/ | V4.0.0 | 11部门朝廷调度 |
| _dispatch_mapping.py | intelligence/dispatcher/wisdom_dispatch/ | V3.0+ | 部门学派映射 |
| wisdom_fusion/__init__.py | intelligence/dispatcher/ | V1.3 | 智慧融合核心（v1.3修复__all__） |
| wisdom_fusion_core.py | intelligence/dispatcher/ | V1.2 | 向后兼容层 |
| _imperial_library.py | intelligence/dispatcher/wisdom_dispatch/ | V3.0.0 | 藏书阁全局记忆中心 |
| _claw_architect.py | intelligence/claws/ | V1.0 | Claw架构（ReAct闭环） |
| _claws_coordinator.py | intelligence/claws/ | V1.0 | 多Claw协调器 |
| _daqin_metrics.py | intelligence/dispatcher/wisdom_dispatch/ | v2.0.0 | 大秦指标考核 |
| _whip_engine.py | intelligence/dispatcher/wisdom_dispatch/ | v2.0.0 | 行政之鞭 |
| _research_strategy_engine.py | intelligence/engines/ | v2.0 | 研究策略引擎 |
| research_phase_manager.py | intelligence/engines/ | v1.0.0 | 研究阶段管理器 |
| map_claws_to_positions.py | scripts/ | V5.1 | Claw岗位映射脚本 |

---

*本架构将随Somn系统运行持续演进，藏书阁V3.0的记忆积累将驱动调度策略日趋精准。*
*V6.1.0最终完整版——整合全部神之架构演进成果，422岗位/763 Claw/35学派/135问题类型/藏书阁V3.0全面贯通。*
