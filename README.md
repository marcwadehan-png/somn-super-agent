<div align="center">

# Somn (索姆) — 超级智能体

**自主进化的 LLM 智能体 · 多层级推理引擎 · 深度知识系统**

[![Version](https://img.shields.io/badge/version-v7.1-blue)]()
[![License](https://img.shields.io/badge/license-AGPL%20v3-blue)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-green)]()
[![Tests](https://img.shields.io/badge/tests-25%2F25%20passed-brightgreen)]()

</div>

---

## 项目简介

**Somn** 是一个基于大语言模型的自主进化智能体系统，融合了 862 位东西方贤者的智慧体系，构建了多层级推理引擎、深度知识系统与神经记忆架构。

> "Somn" — 拉丁语 "睡眠"，寓意 AI 在深度思考中自我进化。

---

## 核心架构

```
┌──────────────────────────────────────────────────────────┐
│                     Somn 超级智能体                        │
├──────────┬──────────┬───────────┬───────────┬────────────┤
│ 驳心引擎  │ DivineReason │ SageDispatch │ 神行轨    │ 神之架构  │
│ RefuteCore│  三层推理    │  调度系统     │ Track-B   │ 四层七线  │
│ 8维论证   │ Light/Std/Deep│ 12调度器     │ B轨v4.2  │ 377岗位  │
├──────────┴──────────┴───────────┴───────────┴────────────┤
│                  NeuralMemory v7 · 神经记忆                 │
│          感知记忆 → 工作记忆 → 短期 → 长期 → 永恒           │
├──────────────────────────────────────────────────────────┤
│              21 格知识系统 · 42 智慧学派 · 166+ 推理引擎     │
├──────────────────────────────────────────────────────────┤
│              UnifiedLLMConfigManager v6.2 云端优先          │
├──────────────────────────────────────────────────────────┤
│         FastAPI 后端 · RESTful API · SQLite 持久化          │
└──────────────────────────────────────────────────────────┘
```

---

## 核心特性

| 模块 | 说明 | 版本 |
|------|------|------|
| **驳心引擎 RefuteCore** | 8维结构化论证：情绪/人性/驳斥/社交/逆向/暗森林/行为 | v3.1 |
| **DivineReason** | 三层推理模型：表层模式匹配 → 深度假设探索 → 元认知审视 | v4.0 |
| **SageDispatch** | 12调度器 + 懒加载优化，监管调度/深度推理/架构决策 | v4.2 |
| **神行轨 Track-B** | 独立执行单元，Claw 自主工作，0.02ms 瞬间实例化 | v4.2 |
| **NeuralMemory** | 五层记忆架构（感知/工作/短期/长期/永恒），Hebbian 学习 | v7.0 |
| **知识格子系统** | 21 格动态知识网，跨领域关联，热度统计，知识图谱 | v1.1 |
| **神之架构** | 四层架构（感知→认知→决策→执行），七条主线，377 个岗位角色 | V4.2 |
| **UnifiedLLM** | 统一管理 9 模块 LLM 配置，云端优先，网络状态感知 | v6.2 |

### 推理体系

- **LongCoT** — 长链思维推理
- **ToT** — 思维树推理
- **GoT** — 思维图推理
- **ReAct** — 推理+行动交替

### 42 智慧学派

儒家 · 道家 · 佛家 · 法家 · 兵家 · 墨家 · 名家 · 阴阳家 · 纵横家 · 杂家 · 农家 · 医家 · 科学 · 经济学 · 心理学 · 社会学 · 复杂性科学 · 系统论 · 控制论 · 信息论 · 博弈论 · 逻辑学 · 统计学 · 计算机科学 · 认知科学 · 神经科学 · 语言学 · 符号学 · 传播学 · 营销学 · 管理学 · 人类学 · 历史学 · 政治学 · 法学 · 教育学 · 伦理学 · 美学 · 数学 · 哲学 · 生态学

---

## 项目规模

| 指标 | 数量 |
|------|------|
| Python 源文件 | 1,010+ |
| YAML 配置 | 880+（862 贤者定义） |
| Markdown 文档 | 1,879（含 800+ 深度学习文档） |
| 知识格子 | 21 格（A1-C4） |
| 推理引擎 | 166+ |
| 智慧学派 | 42 |
| 贤者体系 | 862 位 |
| E2E 测试 | 25/25 通过 |

---

## 快速开始

### 环境要求

- Python 3.11+
- pip

### 安装

```bash
# 克隆仓库
git clone https://github.com/marcwadehan-png/somn-super-agent.git
cd somn-super-agent

# 安装依赖
pip install -r requirements.txt

# （可选）安装开发依赖
pip install -r requirements-dev.txt

# （可选）安装 GUI 依赖
pip install -e ".[gui]"
```

### 启动后端服务

```bash
cd somn-super-agent
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### 运行测试

```bash
cd somn-super-agent
pytest tests/ -v
```

---

## 项目结构

```
somn-super-agent/
├── smart_office_assistant/     # 核心引擎（939 Python 文件）
│   ├── src/                    #   源代码
│   │   ├── core/               #     核心模块（AgentCore, SomnCore）
│   │   ├── intelligence/       #     智能调度（WisdomDispatcher）
│   │   ├── main_chain/         #     主链集成
│   │   ├── reasoning/          #     推理引擎
│   │   ├── neural_memory/      #     神经记忆系统
│   │   ├── wisdom/             #     智慧学派引擎
│   │   ├── dual_track/         #     神行轨（Track-B）
│   │   └── divine/             #     DivineReason 推理
│   ├── config/                 #   配置文件
│   └── tests/                  #   测试套件
├── api/                        # FastAPI 后端服务（14 端点文件）
├── knowledge_cells/            # 21 格知识系统（57 Python 文件）
│   ├── A1-A8.md               #   智慧核心格子
│   ├── B1-B9.md               #   应用域格子
│   ├── C1-C4.md               #   扩展域格子
│   ├── cell_engine.py         #   格子引擎
│   └── fusion_engine.py       #   知识融合器
├── tests/                      # 全局测试（20 文件）
├── docs/                       # 文档（800+ 深度学习文档）
├── file/                       # 历史报告（836 份）
├── pyproject.toml              # 项目配置
├── requirements.txt            # 生产依赖
├── requirements-dev.txt        # 开发依赖
├── Dockerfile                  # Docker 构建
└── docker-compose.yml          # Docker Compose
```

---

## 技术栈

- **后端**: Python 3.11+, FastAPI, Uvicorn, SQLite
- **AI**: Transformers, PyTorch, Hugging Face
- **知识**: NetworkX (知识图谱), PyYAML
- **文档**: python-docx, python-pptx, ReportLab, openpyxl
- **网络**: httpx, aiohttp, websockets
- **日志**: Loguru
- **工具**: PyQt6 (GUI), Schedule (定时任务)

---

## 协议

[AGPL-3.0](LICENSE) — GNU Affero General Public License v3.0

---

## 贡献

欢迎提交 Issue 和 Pull Request。详见 [CONTRIBUTING.md](CONTRIBUTING.md)

### 如何贡献

1. **Fork** 本仓库
2. 创建特性分支：`git checkout -b feature/your-idea`
3. 提交代码：`git commit -m 'Add: your feature'`
4. 推送分支：`git push origin feature/your-idea`
5. 提交 **Pull Request**

---

## 招募贡献者

**Somn** 是开源协作项目，欢迎各类开发者加入！

| 领域 | 描述 | 难度 |
|------|------|------|
| **推理引擎优化** | 提升 LongCoT/ToT/GoT/ReAct 推理效率 | ⭐⭐⭐ |
| **知识系统扩展** | 丰富 42 智慧学派与知识格子内容 | ⭐⭐ |
| **后端架构** | FastAPI 服务扩展与性能优化 | ⭐⭐⭐ |
| **测试覆盖** | 编写单元测试与集成测试 | ⭐ |
| **文档翻译** | 中英文文档互译 | ⭐ |

---

## 联系

- 📧 邮箱：marcwadehan@gmail.com
- 🐛 问题反馈：[GitHub Issues](https://github.com/marcwadehan-png/somn-super-agent/issues)

<div align="center">

**无论大小，每一份贡献都值得感谢！**

</div>
