# Somn 智能助手 v6.2.0

> 增长解决方案专家智能体系统（超级智能体）

## 项目概述

Somn 是一个具备真实智能、自主性、可持续进化能力的增长解决方案专家智能体系统。支持多智能体协作、自规划、自进化、多层记忆与知识系统。

### 核心特性

- **神之架构 V6.2**: 422个岗位体系，763个贤者Claw，42个学派，165个问题类型
- **五层链路**: 深度学习文档 → 蒸馏文档 → 编码注册 → 克隆实现 → 子智能体
- **智能调度**: GlobalWisdomScheduler + WisdomDispatcher 双层调度
- **学习系统**: 三层学习架构，支持DAILY/THREE_TIER/ENHANCED等策略
- **推理引擎**: LongCoT + ToT + GoT + ReAct 四引擎协同
- **神经记忆**: v21.0 统一类型系统（7层MemoryTier + 4层UnifiedMemoryTier）
- **A/B双模型调度**: DualModelService 左右大脑架构
- **朝廷岗位体系**: V4.2.0，377岗 + 25爵位 + 七人代表大会

### 技术栈

- Python 3.11+
- PyTorch 2.x
- Transformers 5.x
- YAML 配置驱动

### 代码规模

| 指标 | 数量 |
|------|------|
| Python文件 | 1,091 个 |
| 代码行数 | 330,792 行 |
| 测试用例 | 543 个 |
| 核心子模块 | 30 个 |

## 快速开始

```bash
# 安装依赖
pip install -r requirements-dev.txt

# 运行测试
pytest tests/ -v

# 健康检查
python scripts/health_check.py

# 启动助手
python -m smart_office_assistant
```

## 项目结构

```
smart_office_assistant/       # 核心代码
├── src/
│   ├── core/                # 核心引擎 (82文件)
│   ├── intelligence/        # 智能系统 (468文件)
│   ├── neural_memory/       # 神经记忆 (64文件)
│   ├── neural_layout/       # 神经布局 (19文件)
│   ├── growth_engine/       # 增长引擎 (32文件)
│   ├── ppt/                 # PPT生成 (21文件)
│   ├── learning/            # 学习系统 (18文件)
│   ├── industry_engine/     # 行业引擎 (16文件)
│   ├── literature/          # 文学研究 (14文件)
│   ├── knowledge_graph/     # 知识图谱 (11文件)
│   └── tool_layer/          # 工具层
├── data/                    # 数据文件
├── claws/                   # Claw子智能体配置
├── tests/                   # 测试套件 (543用例)
├── scripts/                 # 工具脚本
├── file/                    # 系统文档
├── docs/                    # 蒸馏文档
└── config/                  # 配置文件
```

## 核心模块

| 模块 | 说明 |
|------|------|
| AgentCore | 智能体核心 |
| SomnCore | 核心引擎 |
| SuperWisdomCoordinator | 超级智慧协调器 |
| GlobalWisdomScheduler | 全局智慧调度器 |
| WisdomDispatcher | 智慧调度器 |
| DeepReasoningEngine | 深度推理引擎 |
| ClawArchitect | 贤者架构师 (1968行) |
| NeuralMemorySystem | 神经记忆系统 v21.0 |
| ROITracker | ROI追踪器 |
| LearningCoordinator | 学习协调器 |

## 测试

```bash
# 运行全部测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_somn_core.py -v

# 查看覆盖率
pytest tests/ --cov=smart_office_assistant
```

## 文档

### 核心架构文档

- [神之架构 V6.2](docs/神之架构_V6.2.md) ⭐⭐⭐⭐⭐ — 项目核心架构（422岗/763Claw/42学派/165问题类型）
- [主线架构文档](docs/主线架构文档.md) ⭐⭐⭐⭐⭐ — 串联/并形/交叉三种运行模式
- [贤者工程五层链路规范](docs/贤者工程五层链路规范化架构.md) — 深度学习→蒸馏→编码→克隆→Claw完整链路
- [Claw任职报告 V6.0](docs/Claw任职报告_V6.0.md) — 763个Claw 100%岗位映射
- [文档导航中心](docs/文档导航中心.md) — 项目文档总索引

### 系统集成报告

- [全系统深度分析报告](docs/Somn_V6.2_全系统深度分析报告.md)
- [V6.0第三阶段集成报告](docs/V6.0第三阶段集成报告.md)
- [V6.0第二阶段集成报告](docs/V6.0第二阶段集成报告.md)
- [V6.0精优与验收报告](docs/V6.0精优与验收报告.md)
- [智慧引擎层深度分析报告](docs/智慧引擎层深度分析报告.md)

### Claw架构文档

- [Claw双阶段架构设计](docs/Claw双阶段架构设计_v4.md)
- [Phase4 OpenClaw架构设计](docs/Phase4_OpenClaw架构设计.md)
- [Phase_4 Claw子系统架构](docs/Phase_4_Claw子系统架构.md)
- [GlobalClawScheduler集成报告](docs/GlobalClawScheduler集成报告.md)

### 智慧融入报告

- [三教合一智慧融入报告](docs/三教合一智慧融入报告.md)
- [素书智慧融入报告](docs/素书智慧融入报告.md)
- [鸿铭智慧融入报告](docs/鸿铭智慧v1.0融入报告.md)
- [四大名著智慧融入报告](docs/四大名著智慧v1.0融入报告.md)
- [WCC智慧体系融入报告](docs/WCC智慧体系融入报告.md)

### 测试与质量

- [测试覆盖率分析报告](docs/Somn测试覆盖率分析报告.md)
- [测试覆盖率与质量追踪系统](docs/Somn_测试覆盖率与质量追踪系统.md)

### 蒸馏文档（600贤者）

- [第1卷 上古至秦汉](docs/蒸馏卷/史学/600贤者蒸馏_第1卷_上古至秦汉.md)
- [第2卷 魏晋南北朝隋唐](docs/蒸馏卷/史学/600贤者蒸馏_第2卷_魏晋南北朝隋唐.md)
- [第3卷 儒家集群](docs/蒸馏卷/儒家/600贤者蒸馏_第3卷_儒家集群.md)
- [第4卷 道家集群](docs/蒸馏卷/道家/600贤者蒸馏_第4卷_道家集群.md)
- [第5卷 佛家集群](docs/蒸馏卷/佛学/600贤者蒸馏_第5卷_佛家集群.md)
- [第6卷 法家集群](docs/蒸馏卷/法家/600贤者蒸馏_第6卷_法家集群.md)
- [第7卷 纵横医家](docs/蒸馏卷/纵横家/600贤者蒸馏_第7卷_纵横医家.md)
- [第8卷 文学集群](docs/蒸馏卷/文学/600贤者蒸馏_第8卷_文学集群.md)
- [第9卷 史学集群](docs/蒸馏卷/史学/600贤者蒸馏_第9卷_史学集群.md)
- [第10卷 科技集群](docs/蒸馏卷/科学/600贤者蒸馏_第10卷_科技集群.md)
- [第11卷 艺术巾帼](docs/蒸馏卷/其他/600贤者蒸馏_第11卷_艺术巾帼.md)
- [第12卷 当代补遗](docs/蒸馏卷/其他/600贤者蒸馏_第12卷_当代补遗.md)
- [第13卷 佛家补遗](docs/蒸馏卷/佛学/600贤者蒸馏_第13卷_佛家补遗.md)
- [第14卷 道家补遗](docs/蒸馏卷/道家/600贤者蒸馏_第14卷_道家补遗.md)
- [第15卷 兵家补遗](docs/蒸馏卷/兵家/600贤者蒸馏_第15卷_兵家补遗.md)
- [第16卷 科学家补遗](docs/蒸馏卷/科学/600贤者蒸馏_第16卷_科学家补遗.md)

## 许可证

GNU Affero General Public License v3 (AGPL-3.0)

详见根目录 [LICENSE](../LICENSE)

## 版本

当前版本: **6.2.0** (2026-04-25)
