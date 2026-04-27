# Somn (索姆) — 神之架构 · 万维智能
> **基于大语言模型** | 自主进化 · 多维推理 · 知识驱动

![Version](https://img.shields.io/badge/version-v6.2.0-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-green)
![License](https://img.shields.io/badge/license-AGPL%20v3-blue)
![Tests](https://img.shields.io/badge/tests-543%20passed-brightgreen)

---

## ✨ 一句话介绍

**Somn** 是一款基于大语言模型探索自主进化，采用多层级架构设计，集成 21 个智慧学派、142 个推理引擎、21 格知识系统、763+ 贤者子代理与神经记忆网络。支持本地部署与云端调用，前后端分离架构，可独立运行。

## ⚡ 开源邀请 · Join Us

Somn 是一个仍在建设中的理想项目，目前处于 **MVP (最小可行产品)** 阶段。

> *「一个人的梦想只是梦想，一群人的梦想就能成为现实。」*

### 🏗️ 我们需要你的帮助

Somn 的愿景是构建一个拥有无限可能的超级智能体，但一个人走得快，一群人走得远。无论你擅长什么领域，我们都热烈欢迎：

| 贡献方向 | 说明 | 适合人群 |
|----------|------|----------|
| 🧠 **核心开发** | 推理引擎、知识系统、神经记忆等核心模块 | Python/AI 开发 |
| 🎨 **界面设计** | PyQt GUI 优化、Web 前端美化 | UI/UX 设计 |
| 📚 **知识建设** | 600 贤者文档、蒸馏工程、智慧学派 | 领域专家/内容创作者 |
| 🧪 **测试维护** | 编写测试用例、修复 Bug、性能优化 | QA 工程师 |
| 📖 **文档翻译** | 英文文档、API 文档、用户手册 | 技术写作 |
| 💡 **创意提案** | 新功能设计、架构优化、场景拓展 | 产品/架构师思维 |

### 🤝 如何参与

```bash
# 1. Star + Fork
# 2. Clone 并探索代码
git clone https://github.com/marcwadehan-png/somn-agent.git

# 3. 查看 Issues 寻找感兴趣的议题
# https://github.com/marcwadehan-png/somn-agent/issues

# 4. 提交你的第一个 PR
git checkout -b feature/your-feature
git commit -m 'feat: 添加你的功能'
git push origin feature/your-feature
```

### 📋 开源协议

本项目采用 **AGPL v3** 开源，意味着：
- ✅ 你可以自由使用、修改、分发
- ⚠️ 如果你通过网络服务形式提供 Somn（含修改版），需要开源你的代码
- 💪 让我们一起构建一个更开放、更强大的智能系统

> ⚡ **特别声明**: Somn 属于个人理想项目，目前**尚未完善**，欢迎所有愿意一起探索的朋友加入！

---

## 🎯 核心亮点

| 特性 | 详情 |
|------|------|
| 🔮 **双脑模型架构** | B模型 Gemma4（主脑）+ A模型 Llama-3.2（副脑），本地推理（本地模型需下载，支持云端模型） |
| 🏫 **21 个智慧学派** | 儒/道/法/墨/兵家/佛家/心理学/经济学/复杂性科学等 |
| ⚡ **142 个推理引擎** | 覆盖 LongCoT / ToT / GoT / ReAct 四大推理体系 |
| 🧠 **21 格知识系统** | 动态网状知识库，跨领域关联 + 方法论检查 |
| 👑 **神之架构 V6.0** | 422 岗位 / 763 贤者 / 七人决策大会 / 锦衣卫体系 |
| 💾 **神经记忆 v21** | Hebbian 学习 + 强化学习 + 三层记忆架构 |
| 🖥️ **PyQt6 桌面端** | 前后端分离，动态服务发现，本地缓存层 |
| 🌐 **FastAPI 后端** | RESTful API + WebSocket 实时通信，61 个 API 端点 |
| 🎛️ **全局控制中心** | CLI / GUI / Web 三模式统一管理 |

---

## 📊 项目规模

```
总文件数:    ~4,575
Python源码:   1,091 文件 (330,792 行)
YAML配置:     853 个 (含 500+ Claw 贤者配置)
Markdown文档:  1,774 个
测试用例:     543 个 (100% 通过率)
核心子模块:    37 个一级模块
```

---

## 🏗️ 架构总览

```
┌──────────────────────────────────────────────────────────────────────┐
│                        Somn-GUI (前端)                            │
│   ┌──────────┐ ┌──────────┐ ┌──────────────┐ ┌─────────────────┐  │
│   │ PyQt6   │ │ 缓存层  │ │  状态层      │ │  HTTP/WebSocket│  │
│   │ 界面组件 │ │ SQLite  │ │ 内存管理     │ │  API 客户端      │  │
│   └────┬─────┘ └────┬────┘ └──────┬───────┘ └────────┬────────┘  │
│        └────────────┼────────────┘                    │             │
└────────────────────┼─────────────────────────────────────┘             │
                     │ HTTP/REST API (动态发现)                         │
┌────────────────────▼─────────────────────────────────────────────┐
│                   FastAPI Gateway (端口 8964)                       │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  /api/v1/*  RESTful + WebSocket                              │ │
│  └──────────────────────────┬──────────────────────────────────┘ │
│                             │                                       │
│  ┌──────────────────────────▼──────────────────────────────────┐ │
│  │                  SomnCore 引擎                               │ │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌─────────┐  │ │
│  │  │ Agent  │ │ Wisdom │ │ Neural │ │ Main   │ │ Memory  │  │ │
│  │  │ Core   │ │Engine  │ │ Memory │ │ Chain  │ │ Engine  │  │ │
│  │  └────────┘ └────────┘ └────────┘ └────────┘ └─────────┘  │ │
│  └──────────────────────────┬──────────────────────────────────┘ │
│                             │                                       │
│  ┌──────────────────────────▼──────────────────────────────────┐ │
│  │          本地 LLM: Gemma4 / Llama-3.2                          │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

### 架构分层说明

| 层级 | 组件 | 职责 |
|------|------|------|
| **展示层** | Somn-GUI (PyQt6) | 用户交互界面、本地缓存、状态管理 |
| **网关层** | FastAPI Gateway | 请求路由、中间件、限流保护 |
| **核心层** | SomnCore Engine | 智能推理、智慧调度、神经记忆 |
| **模型层** | 本地 LLM / 云端 API | 文本生成、推理计算 |

---

## 📁 项目结构

```
somn-git-repo/
├── README.md                        # 本文件
├── .gitignore                        # Git 忽略规则
│
├── somn/                            # ★ 后端核心项目
│   ├── LICENSE                      # AGPL v3 开源协议
│   ├── pyproject.toml                # 项目配置 v1.0 (pylint/flake8/black/mypy)
│   ├── requirements.txt              # 运行时依赖
│   ├── requirements-dev.txt           # 开发依赖
│   ├── pytest.ini                    # 测试框架配置
│   │
│   ├── api/                          # FastAPI 服务层
│   │   ├── server.py                # 应用入口 (v1.0)
│   │   ├── routes/                  # API 路由 (7个路由模块)
│   │   │   ├── chat.py               # 对话接口
│   │   │   ├── knowledge.py          # 知识库接口
│   │   │   ├── knowledge_cells.py    # 知识格子接口
│   │   │   ├── analysis.py           # 分析/策略接口
│   │   │   ├── admin.py              # 管理接口 (46KB)
│   │   │   └── health.py            # 健康检查
│   │   ├── middleware.py              # 中间件 (CORS/超时/限流)
│   │   ├── schemas.py                # Pydantic 数据模型
│   │   └── deps.py                   # 依赖注入
│   │
│   ├── config/                       # 配置文件
│   │   ├── local_config.yaml        # 独立运行配置 v1.0
│   │   ├── server_config.yaml       # API 服务配置 (端口 8964)
│   │   └── storage_config.yaml      # 统一存储配置
│   │
│   ├── smart_office_assistant/      # ★ 核心智能引擎
│   │   ├── src/                     # 核心源码 (37个子模块)
│   │   │   ├── core/                 # SomnCore / AgentCore
│   │   │   ├── intelligence/         # 智慧系统 (35学派, 142引擎)
│   │   │   │   └── claws/configs/    # 500+ 贤者 YAML 配置
│   │   │   ├── main_chain/           # 主线架构 (并行+交叉织网)
│   │   │   ├── neural_memory/        # 神经记忆 (v1.0)
│   │   │   ├── knowledge_graph/     # 知识图谱
│   │   │   ├── tool_layer/           # LLM 工具层
│   │   │   ├── documents/            # 文档引擎
│   │   │   └── ...                  # 其余 30+ 子模块
│   │   ├── config/court_config.yaml # 神之架构配置
│   │   └── start.bat / start.sh       # 启动脚本
│   │
│   ├── knowledge_cells/             # 21 格知识系统 v1.0
│   │   ├── __init__.py              # 统一接口
│   │   ├── cell_engine.py           # 格子引擎
│   │   ├── fusion_engine.py         # 知识融合器
│   │   ├── method_checker.py        # 方法论检查器
│   │   ├── reasoning_enhancer.py    # 推理增强器
│   │   ├── neural_integration.py    # 神经集成
│   │   ├── cli.py                   # 交互式 CLI
│   │   ├── INDEX.md                 # 格子索引
│   │   └── A1-C4.md                 # 21 个知识格子
│   │
│   ├── global_control_center/       # 全局控制中心 v1.0
│   │   ├── __init__.py              # 三模式入口 (CLI/GUI/Web)
│   │   ├── cli/                     # 命令行交互
│   │   ├── gui/                     # 图形界面
│   │   ├── web/                     # Web 浏览器 (Flask)
│   │   ├── managers/                # 模块/引擎/Claw/配置管理
│   │   └── schedulers/              # 调度监控
│   │
│   ├── models/                       # 本地大模型启动脚本
│   │   ├── 启动A大模型.bat          # Llama-3.2 (副脑)
│   │   ├── 启动B大模型.bat          # Gemma4 (主脑)
│   │   └── 启动A+B大模型.bat        # 双模型同时启动
│   │
│   ├── scripts/                      # 运维脚本
│   │   ├── health_check.py          # 健康检查
│   │   ├── code_quality_check.py    # 代码质量检查
│   │   └── init_config.py          # 配置初始化
│   │
│   ├── tests/                        # 测试套件 (21 个测试文件)
│   │   ├── conftest.py              # 共享 fixtures
│   │   ├── test_reasoning_engine.py # 推理引擎测试 (55KB)
│   │   ├── test_scheduler_system.py # 调度系统测试
│   │   └── ...                     # 共 543 用例, 100% 通过
│   │
│   ├── docs/                         # 文档
│   │   ├── adr/                     # 20 篇 ADR 架构决策记录
│   │   ├── source/                  # Sphinx 源码
│   │   └── 蒸蒸馏卷/               # 760 份蒸馏文档 (18分类)
│   │
│   ├── file/                         # 系统文档
│   │   ├── 学术文件/
│   │   ├── 智慧文件/               # 600+ 贤者深度学习文档
│   │   └── 系统文件/               # 架构/报告/规范
│   │
│   ├── SOUL.md                       # AI 灵魂内核
│   ├── IDENTITY.md                   # 身份定义
│   ├── METHODOLOGY.md                # 方法论纪律
│   ├── PROJECT_STATUS.md             # 项目状态概览
│   ├── CHANGELOG.md                  # 版本变更日志
│   ├── SECURITY.md                   # 安全策略
│   ├── CONTRIBUTING.md               # 贡献指南
│   ├── TESTING_RULES.md              # 全局测试规范
│   └── start_independent.bat         # Windows 独立启动脚本
│
├── Somn-GUI/                        # ★ 前端桌面程序
│   ├── README_LAUNCHERS.md           # 启动器说明
│   ├── ARCHITECTURE.md              # 前后端分离架构设计 (20KB)
│   ├── pyproject.toml                # 项目配置
│   ├── requirements.txt              # 前端依赖
│   ├── config/gui_config.yaml        # GUI 配置
│   │
│   └── somngui/                     # PyQt6 源码
│       ├── app.py                   # 应用入口
│       ├── core/                    # 连接/状态/插件管理
│       ├── client/                  # API 客户端 / WebSocket
│       ├── cache/                   # SQLite 缓存 / 预加载
│       ├── gui/                     # 主窗口 / 管理面板 / 控制中心
│       │   ├── admin_panel.py       # 管理面板 (212KB) ★最大组件
│       │   ├── main_window.py       # 主窗口
│       │   └── control_center_panel.py
│       └── resources/               # QSS 样式表 (6主题)
│
└── 开源打包分析报告.md              # 打包分析
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本 | 说明 |
|------|------|------|
| Python | 3.11+ | 推荐 3.13 获得最佳性能 |
| 操作系统 | Windows / Linux / macOS | 全平台支持 |
| 内存 | 16GB+ | 本地 LLM 需要较大内存 |
| 磁盘 | 10GB+ | 模型文件较大 |

### 前置准备

#### 1. 安装 Ollama (本地模型运行)

```bash
# Windows/macOS/Linux
# 访问 https://ollama.ai/download 下载安装

# 拉取模型
ollama pull gemma4:2b      # 主脑模型
ollama pull llama3.2:3b    # 副脑模型

# 验证安装
ollama list
```

#### 2. 克隆项目

```bash
git clone https://github.com/marcwadehan-png/somn-agent.git
cd somn-agent
```

### 安装步骤

#### 方式一：使用 pip 安装

```bash
# 1. 安装后端依赖
pip install -r somn/requirements.txt

# 2. 安装前端依赖
pip install -r Somn-GUI/requirements.txt
```

#### 方式二：使用 pyproject.toml (推荐)

```bash
# 后端
cd somn
pip install -e .

# 前端
cd ../Somn-GUI
pip install -e .
```

#### 方式三：使用虚拟环境 (隔离安装)

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# 安装依赖
pip install -r somn/requirements.txt
pip install -r Somn-GUI/requirements.txt
```

### 启动方式

#### 方式一：独立启动脚本（推荐新手）

双击运行或命令行执行：

```bash
somn\start_independent.bat
```

启动后显示菜单：

```
╔════════════════════════════════════════════════════╗
║           Somn 独立启动器 v6.2.0                    ║
╠════════════════════════════════════════════════════╣
║  1. GUI模式 (图形界面)                              ║
║  2. CLI交互模式 (命令行)                            ║
║  3. 健康检查                                        ║
║  4. 系统状态                                        ║
║  5. 列出解决方案                                    ║
║  6. 单次查询                                        ║
║  0. 退出                                            ║
╚════════════════════════════════════════════════════╝
请选择 [0-6]:
```

#### 方式二：手动分步启动

```bash
# Step 1: 启动后端 API 服务
python -m somn.api.server
# 服务地址: http://127.0.0.1:8964
# API文档:   http://127.0.0.1:8964/api/docs

# Step 2: 启动前端 GUI (新终端)
cd Somn-GUI
python -m somngui.app
```

#### 方式三：全局控制中心

```bash
# 命令行交互模式
python somn/global_control_center/__init__.py --mode cli

# 图形界面模式
python somn/global_control_center/__init__.py --mode gui

# Web 浏览器模式 (默认 8970 端口)
python somn/global_control_center/__init__.py --mode web
```

### 验证安装

```bash
# 1. 运行健康检查
python somn/scripts/health_check.py

# 预期输出:
# ✓ API 服务运行正常
# ✓ 本地模型连接正常
# ✓ 数据库连接正常
# ✓ 知识库索引正常

# 2. 运行测试套件
pytest somn/tests/ -v

# 3. 代码质量检查
python somn/scripts/code_quality_check.py
```

详细说明请参考 [Somn 全局主入口使用指南](somn/file/系统文件/快速启动指南.md)

---

## 💡 使用场景

### 场景一：智能问答助手

```python
import httpx

# 同步调用
response = httpx.post(
    "http://127.0.0.1:8964/api/v1/chat",
    json={"message": "如何提升用户留存率？"}
)
print(response.json()["answer"])
```

### 场景二：企业知识库问答

```python
# 查询知识库
response = httpx.get(
    "http://127.0.0.1:8964/api/v1/knowledge",
    params={"query": "营销策略"}
)
knowledge_results = response.json()

# 查询知识格子
response = httpx.get(
    "http://127.0.0.1:8964/api/v1/cells/search",
    params={"content": "用户增长"}
)
```

### 场景三：市场分析报告

```python
# 生成市场分析
response = httpx.post(
    "http://127.0.0.1:8964/api/v1/analysis/market",
    json={
        "industry": "电商",
        "region": "全国",
        "period": "2024"
    }
)
report = response.json()
```

### 场景四：策略咨询

```python
# 获取策略建议
response = httpx.post(
    "http://127.0.0.1:8964/api/v1/analysis/strategy",
    json={
        "situation": "新用户增长放缓",
        "constraints": ["预算有限", "时间紧迫"]
    }
)
```

### 场景五：实时对话 (WebSocket)

```python
import websockets
import asyncio

async def chat():
    uri = "ws://127.0.0.1:8964/api/v1/ws"
    async with websockets.connect(uri) as ws:
        # 发送消息
        await ws.send('{"message": "你好"}')
        
        # 接收响应
        while True:
            response = await ws.recv()
            print(response)

asyncio.run(chat())
```

---

## 📡 API 接口详解

### 基础接口

#### 健康检查
```
GET /api/v1/health
```
响应示例：
```json
{
    "status": "healthy",
    "version": "v6.2.0",
    "uptime": 3600,
    "services": {
        "api": "ok",
        "llm": "ok",
        "cache": "ok"
    }
}
```

#### 系统状态
```
GET /api/v1/system/status
```
响应示例：
```json
{
    "cpu_usage": 45.2,
    "memory_usage": 62.8,
    "gpu_usage": 78.5,
    "active_connections": 3
}
```

### 对话接口

#### 发送消息
```
POST /api/v1/chat
Content-Type: application/json

{
    "message": "string",           # 用户消息 (必填)
    "session_id": "string",        # 会话ID (可选)
    "model": "gemma4|llama3.2",    # 模型选择 (可选)
    "temperature": 0.7,           # 温度参数 (可选)
    "max_tokens": 2048             # 最大Token数 (可选)
}
```

响应：
```json
{
    "answer": "string",
    "session_id": "string",
    "tokens_used": 1500,
    "model": "gemma4",
    "reasoning_steps": ["step1", "step2"]
}
```

#### WebSocket 实时通信
```
WS /api/v1/ws
```
发送格式：`{"type": "chat", "message": "...", "session_id": "..."}`
接收格式：`{"type": "response", "content": "...", "done": true}`

### 知识库接口

#### 知识检索
```
GET /api/v1/knowledge
Query Parameters:
    - query: string      # 搜索关键词
    - limit: int         # 返回数量 (默认10)
    - offset: int        # 分页偏移 (默认0)
```

#### 知识上传
```
POST /api/v1/knowledge
Body: multipart/form-data
    - file: file         # 支持 .txt/.md/.pdf/.docx
    - category: string    # 分类标签
    - title: string     # 文档标题
```

### 知识格子接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/cells` | 获取所有格子列表 |
| GET | `/api/v1/cells/{cell_id}` | 获取指定格子内容 |
| GET | `/api/v1/cells/search` | 搜索格子 |
| GET | `/api/v1/cells/related` | 获取关联格子 |
| POST | `/api/v1/cells/fusion` | 融合查询 |
| POST | `/api/v1/cells/check` | 方法论检查 |

#### 融合查询示例
```bash
curl -X POST http://127.0.0.1:8964/api/v1/cells/fusion \
  -H "Content-Type: application/json" \
  -d '{"query": "如何提升用户增长", "top_k": 5}'
```

响应：
```json
{
    "answer": "基于知识融合的分析...",
    "related_cells": ["A1", "A2", "B1", "C2"],
    "framework_recommendations": ["AARRR模型", "RFM分析"],
    "cross_domain_insights": ["可参考直播运营的裂变策略"]
}
```

### 分析接口

#### 市场分析
```
POST /api/v1/analysis/market
Body: {
    "industry": "string",
    "region": "string",
    "period": "string",
    "metrics": ["growth", "market_share"]
}
```

#### 策略分析
```
POST /api/v1/analysis/strategy
Body: {
    "situation": "string",
    "constraints": ["string"],
    "objectives": ["string"]
}
```

### 管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/admin/stats` | 系统统计 |
| GET | `/api/v1/admin/modules` | 模块列表 |
| POST | `/api/v1/admin/modules/{id}/reload` | 重载模块 |
| GET | `/api/v1/admin/config` | 获取配置 |
| PUT | `/api/v1/admin/config` | 更新配置 |

> 完整 API 文档：启动后访问 `http://127.0.0.1:8964/api/docs` (Swagger UI)

---

## 🧠 知识格子系统详解

### 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    KnowledgeSystem                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ CellEngine │  │FusionEngine │  │  MethodChecker      │ │
│  │  (格子引擎) │  │ (知识融合)  │  │  (方法论检查)        │ │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬────────┘ │
│         │                │                     │           │
│  ┌──────▼────────────────▼─────────────────────▼────────┐ │
│  │              21 格动态知识库                          │ │
│  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐    │ │
│  │  │ A1  │ │ A2  │ │ A3  │ │ A4  │ │ ... │ │ C4  │    │ │
│  │  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘    │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 智慧核心 (8 格)

| ID | 名称 | 核心能力 | 适用场景 |
|----|------|----------|----------|
| A1 | 逻辑判断 | 三层推理 + 8种谬误检测 | 问题分析、方案评审 |
| A2 | 智慧模块 | 25学派融合 + 四级调度 | 复杂问题求解 |
| A3 | 论证审核 | 翰林院三轮审核 | 文案审核、报告把关 |
| A4 | 判断决策 | 七人投票 + 太极阴阳 | 重要决策、方案选择 |
| A5 | 五层架构 | Somn核心技术架构 | 系统设计、技术选型 |
| A6 | 核心执行链 | 五步主链 + 并行化 | 流程优化、执行监控 |
| A7 | 感知记忆 | 快速扫描 + 直觉反应 | 快速响应、模式识别 |
| A8 | 反思进化 | ROI追踪 + 强化学习 | 效果复盘、持续改进 |

### 知识域 (13 格)

| ID | 名称 | 专业领域 | 核心工具 |
|----|------|----------|----------|
| B1 | 用户增长 | AARRR / 裂变 / 私域 | 增长黑客、病毒营销 |
| B2 | 直播运营 | 三角定律 / FABE话术 | 直播脚本、话术设计 |
| B3 | 私域运营 | 企微 / 社群 / 沉淀 | 私域搭建、用户分层 |
| B4 | 活动运营 | 策划 / 执行 / 复盘 | 活动方案ROI分析 |
| B5 | 会员运营 | 体系设计 / 权益设计 | 会员生命周期管理 |
| B6 | 广告投放 | 投放策略 / 优化 | 投放漏斗、归因分析 |
| B7 | 地产营销 | 获客 / 转化 / 维系 | 案场管理、渠道运营 |
| B8 | 招商运营 | 招商策略 / 洽谈 | 商业定位、品牌组合 |
| B9 | 策略运营 | 规划 / 执行 / 复盘 | OKR管理、战略解码 |
| C1 | 电商运营 | 流量 / 转化 / 供应链 | GMV分析、品类管理 |
| C2 | 数据运营 | 指标 / 分析 / 数据驱动 | 数据看板、归因模型 |
| C3 | 内容营销 | 选题 / 创作 / 分发 | 内容矩阵、SEO优化 |
| C4 | 广告投放 | 平台 / 定向 / ROI | 投放策略、A/B测试 |

### 使用示例

#### Python API 调用

```python
from knowledge_cells import get_knowledge_system, KnowledgeFusion, MethodChecker

# 获取系统实例
system = get_knowledge_system()

# 查询知识
result = system.query("如何提升用户增长")
print(result["answer"])
print(result["related_cells"])  # 关联格子
print(result["frameworks"])      # 推荐框架

# 知识融合
fusion = KnowledgeFusion()
result = fusion.fuse("电商转化率低", top_k=5)
print(result.answer)
print(result.cross_domain_insights)

# 方法论检查
checker = MethodChecker()
score = checker.check(
    diagnosis="CAC=80元, LTV=200元, 复购率=30%",
    framework="RFM模型",
    data="月活100万, 转化率2%",
    logic="通过提升复购率增加LTV",
    analogy="参考电商行业平均水平"
)
print(f"综合评分: {score.total}/100")
```

#### 命令行调用

```bash
cd somn/knowledge_cells
python cli.py

# 交互式菜单:
# 1. 查询知识
# 2. 融合查询
# 3. 方法论检查
# 4. 查看格子列表
# 5. 查看格子内容
# 0. 退出
```

---

## 🏫 35个智慧学派详解

### 学派概览

Somn 整合了古今中外35个智慧学派，形成覆盖哲学、宗教、科学、军事、心理、管理等全领域的智慧体系。

### 核心学派 (9个)

| 学派 | 英文标识 | 代表人物 | 核心理念 | 激活模式 | 擅长问题类型 |
|------|----------|----------|----------|----------|--------------|
| **儒家** | CONFUCIAN | 孔子、孟子 | 仁义礼智信 | gradual | ETHICAL/GOVERNANCE/TALENT/CULTURE |
| **道家** | DAOIST | 老子、庄子 | 道法自然、无为而治 | resonant | STRATEGY/CRISIS/CHANGE/BALANCE/TIMING |
| **佛家** | BUDDHIST | 释迦牟尼、慧能 | 空、缘起、无常 | resonant | MINDSET/HARMONY/INTEREST/LONGTERM |
| **素书** | SUFU | 黄石公 | 道德仁义礼五德 | sharp | LEADERSHIP/RISK/FORTUNE/PERSONNEL |
| **兵法** | MILITARY | 孙子、吴子 | 知己知彼、出奇制胜 | sharp | COMPETITION/ATTACK/DEFENSE/NEGOTIATION |
| **王阳明心学** | YANGMING | 王阳明 | 知行合一、致良知 | resonant | MINDSET/GROWTH/ETHICAL/CLOSED_LOOP |
| **吕氏春秋** | LVSHI | 吕不韦 | 兼儒墨合仁义 | gradual | GOVERNANCE/CULTURE |
| **辜鸿铭** | HONGMING | 辜鸿铭 | 中西文化融合 | gradual | CULTURE/INTEREST |
| **术数时空** | METAPHYSICS | 邵雍、陈抟 | 象数之学、时空推演 | resonant | CHANGE/BALANCE/FORTUNE |

### 科学思维学派 (5个)

| 学派 | 英文标识 | 代表人物 | 核心理念 | 擅长问题类型 |
|------|----------|----------|----------|--------------|
| **科学思维** | SCIENCE | 牛顿、达尔文 | 假设验证、系统分析 | SCIENTIFIC_METHOD/SYSTEM_THINKING/EVIDENCE |
| **数学智慧** | MATH | 欧拉、高斯 | 逻辑严密、最优化 | PROBABILITY/GAME_THEORY/OPTIMIZATION |
| **自然科学** | NATURAL_SCIENCE | 爱因斯坦、费曼 | 探索自然规律 | SYSTEM_THINKING/EVIDENCE |
| **复杂性科学** | COMPLEXITY | 圣塔菲学派 | 涌现、自组织 | COMPLEX_SYSTEM/FEEDBACK_LOOP/EMERGENT_BEHAVIOR |
| **社会科学** | SOCIAL_SCIENCE | 韦伯、涂尔干 | 社会规律研究 | MARKET_ANALYSIS/SOCIAL_STRUCTURE |

### 心理学与管理学派 (8个)

| 学派 | 英文标识 | 代表人物 | 核心理念 | 擅长问题类型 |
|------|----------|----------|----------|--------------|
| **心理学** | PSYCHOLOGY | 弗洛伊德、荣格 | 潜意识、人格分析 | PERSONALITY_ANALYSIS/GROUP_DYNAMICS/TRAUMA_HEALING |
| **系统论** | SYSTEMS | 贝塔朗菲 | 整体性、反馈回路 | COMPLEX_SYSTEM/FEEDBACK_LOOP/SYSTEM_DESIGN |
| **管理学** | MANAGEMENT | 德鲁克、明茨伯格 | 目标管理、组织效能 | STRATEGIC_PLANNING/ORGANIZATIONAL_DESIGN |
| **行为塑造** | BEHAVIOR | 斯金纳、班杜拉 | 强化学习、行为改变 | BEHAVIOR_CHANGE/HABIT_FORMATION |
| **成长思维** | GROWTH | 卡罗尔·德韦克 | 持续迭代、突破极限 | GROWTH_MINDSET/CLOSED_LOOP |
| **杜威反省思维** | DEWEY | 约翰·杜威 | 反思实践、持续改进 | REFLECTIVE_PRACTICE/PROBLEM_SOLVING |
| **组织心理学** | ORGANIZATIONAL_PSYCHOLOGY | 沙因、爱德加·沙因 | 组织文化、团队动力 | ORGANIZATIONAL_CHANGE/TEAM_COHESION |
| **社会心理学** | SOCIAL_PSYCHOLOGY | 阿伦森、米尔格拉姆 | 态度改变、社会影响 | CONFORMITY_BEHAVIOR/AUTHORITY_OBEDIENCE |

### 哲学与宗教学派 (5个)

| 学派 | 英文标识 | 代表人物 | 核心理念 | 擅长问题类型 |
|------|----------|----------|----------|--------------|
| **墨家** | MOZI | 墨子 | 兼爱非攻、尚贤节用 | ENGINEERING_INNOVATION/COST_OPTIMIZATION |
| **法家** | FAJIA | 韩非、商鞅 | 法治术势、绩效管理 | INSTITUTIONAL_DESIGN/LAW_ENFORCEMENT |
| **纵横家** | ZONGHENG | 鬼谷子、苏秦 | 合纵连横、游说外交 | DIPLOMATIC_NEGOTIATION/ALLIANCE_BUILDING |
| **名家** | MINGJIA | 公孙龙、惠施 | 名实之辩、逻辑悖论 | LOGICAL_PARADOX/CLASSIFICATION_REFINEMENT |
| **阴阳家** | WUXING | 邹衍、伏羲 | 阴阳五行、天人感应 | WUXING_ANALYSIS/YINYANG_DIALECTICS |

### 历史与文化学派 (4个)

| 学派 | 英文标识 | 代表人物 | 核心理念 | 擅长问题类型 |
|------|----------|----------|----------|--------------|
| **文明演化** | CIVILIZATION | 汤因比 | 文明兴衰、挑战应战 | CIVILIZATION_ANALYSIS/HISTORICAL_LESSONS |
| **文明经战** | CIV_WAR_ECONOMY | 管仲、桑弘羊 | 轻重之术、盐铁专营 | WAR_ECONOMICS/RESOURCE_STRATEGY |
| **历史思想三维度** | HISTORICAL_THOUGHT | 司马迁、希罗多德 | 以史为鉴、叙事智慧 | HISTORICAL_ANALYSIS/NARRATIVE_WISDOM |
| **文化人类学** | CULTURAL_ANTHROPOLOGY | 马林诺夫斯基、格尔茨 | 文化模式、符号解读 | CULTURAL_PATTERN_RECOGNITION/CROSS_CULTURAL_ADAPTATION |

### 文学与创意学派 (4个)

| 学派 | 英文标识 | 代表人物 | 核心理念 | 擅长问题类型 |
|------|----------|----------|----------|--------------|
| **文学叙事** | LITERARY | 曹雪芹、托尔斯泰 | 叙事技巧、人物刻画 | NARRATIVE_STRUCTURE/CHARACTER_DEVELOPMENT |
| **神话智慧** | MYTHOLOGY | 约瑟夫·坎贝尔 | 英雄之旅、原型理论 | MYTH_INTERPRETATION/ARCHETYPE_ANALYSIS |
| **科幻思维** | SCI_FI | 刘慈欣、阿西莫夫 | 想象力、未来推演 | FUTURISM/TECHNOLOGY_PREDICTION/SCENARIO_PLANNING |
| **WCC智慧演化** | WCC | 复杂适应系统 | 群体智慧、协同进化 | COLLECTIVE_INTELLIGENCE/COEVOLUTION |

### 社会科学进阶学派 (7个 - V1.0新增)

| 学派 | 英文标识 | 代表人物 | 核心理念 | 擅长问题类型 |
|------|----------|----------|----------|--------------|
| **社会学** | SOCIOLOGY | 韦伯、涂尔干、马克思 | 社会结构、阶层流动 | SOCIAL_STRUCTURE/CLASS_MOBILITY/COLLECTIVE_ACTION |
| **行为经济学** | BEHAVIORAL_ECONOMICS | 西蒙、卡尼曼 | 有限理性、认知偏差 | COGNITIVE_BIAS/DECISION_MAKING/NUDGE_POLICY |
| **传播学** | COMMUNICATION | 拉斯韦尔、麦克卢汉 | 传播模型、舆论引导 | MEDIA_EFFECT/PUBLIC_OPINION/INFORMATION_CASCADE |
| **政治经济学** | POLITICAL_ECONOMICS | 凯恩斯、李嘉图 | 制度分析、政策博弈 | INSTITUTIONAL_ANALYSIS/MARKET_REGULATION |
| **中国消费文化** | CHINESE_CONSUMER | - | 消费心理、本土洞察 | CONSUMER_PSYCHOLOGY/MARKET_LOCALIZATION |
| **顶级思维法** | TOP_METHODS | 查理·芒格 | 多元思维模型 | MENTAL_MODELS/INVERSION/ANALOGICAL_REASONING |
| **人类学(扩展)** | ANTHROPOLOGY | 马林诺夫斯基 | 文化深描、跨文化理解 | SYMBOL_SYSTEM/RITUAL_CONTEXT/CULTURAL_ADAPTATION |

### 学派激活与协同机制

```
┌─────────────────────────────────────────────────────────────┐
│                  神经元智慧网络 (NeuronWisdomNetwork)        │
│                                                             │
│   激活模式:                                                  │
│   ├── sharp (锐利): 快速收敛，用于兵法、素书等                │
│   ├── gradual (渐进): 平稳激活，用于儒家、吕氏春秋等           │
│   ├── resonant (共振): 多学派联动，用于道家、佛家等           │
│   └── slow (缓慢): 深度积累，用于复杂性科学等                 │
│                                                             │
│   突触连接:                                                  │
│   ├── 促进性连接 (weight=0.6): 儒家↔素书↔纵横家              │
│   ├── 抑制性连接 (weight=-0.3): 道家↔兵法                     │
│   └── 全局弱连接 (weight=0.1): 所有学派间默认连接              │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚡ 142个推理引擎详解

### 引擎架构

Somn 的142个推理引擎分为四大推理体系，覆盖从基础逻辑到复杂推理的全场景。

### LongCoT 引擎 (长思维链)

| 引擎 | 文件 | 核心能力 | 特点 |
|------|------|----------|------|
| LongCoT | `_long_cot_engine.py` | 顿悟检测、自我纠错 | 超长推理链，支持200+步推理 |

### ToT 引擎 (思维树)

| 引擎 | 文件 | 核心能力 | 特点 |
|------|------|----------|------|
| ToT-BFS | `_tot_engine.py` | 广度优先搜索 | 横向探索多种可能 |
| ToT-DFS | `_tot_engine.py` | 深度优先搜索 | 纵向深入单一路径 |
| ToT-Greedy | `_tot_engine.py` | 贪心策略 | 快速收敛 |
| ToT-Beam | `_tot_engine.py` | 束搜索 | 多路径并行评估 |

### GoT 引擎 (思维图)

| 引擎 | 文件 | 核心能力 | 特点 |
|------|------|----------|------|
| GoT-Basic | `_got_engine.py` | 基础图推理 | 100节点图网络 |
| GoT-Collective | `_got_engine.py` | 聚合推理 | 群体思维融合 |
| GoT-Query | `_got_engine.py` | 查询推理 | 图查询优化 |
| GoT-Critic | `_got_engine.py` | 批评推理 | 自我质疑修正 |

### ReAct 引擎 (推理-行动闭环)

| 引擎 | 文件 | 核心能力 | 特点 |
|------|------|----------|------|
| ReAct-Basic | `_react_engine.py` | 基础闭环 | Thought→Action→Observation |
| ReAct-Parallel | `_react_engine.py` | 并行推理 | 多路径并行探索 |
| ReAct-Adaptive | `_react_engine.py` | 自适应 | 动态策略选择 |

### 21学派智慧引擎

| 学派 | 引擎文件 | 核心功能 | 权重 |
|------|----------|----------|------|
| 儒家 | `ru_wisdom_unified.py` | 伦理判断、君子修身 | 0.10 |
| 道家 | `dao_wisdom_core.py` | 无为而治、阴阳平衡 | 0.08 |
| 佛家 | `confucian_buddhist_dao_fusion_engine.py` | 空性智慧、慈悲喜舍 | 0.06 |
| 素书 | `sufu_wisdom_core.py` | 五德决策、福祸预测 | 0.05 |
| 兵法 | `military_strategy_engine.py` | 战略战术、攻防博弈 | 0.05 |
| 吕氏春秋 | `lvshi_wisdom_engine.py` | 兼收并蓄、治世之道 | 0.03 |
| 辜鸿铭 | `hongming_wisdom_core.py` | 中西会通、文明对话 | 0.03 |
| 术数时空 | `metaphysics_wisdom_unified.py` | 象数推演、时空预测 | 0.03 |
| 文明演化 | `civilization_wisdom_core.py` | 文明分析、历史规律 | 0.02 |
| 文明经战 | `civilization_war_economy_core.py` | 战时经济、资源战略 | 0.02 |
| 科幻思维 | `marvel_wisdom_unified.py` | 未来推演、场景规划 | 0.02 |
| 成长思维 | `thinking_growth_unified.py` | 持续迭代、突破极限 | 0.02 |
| 神话智慧 | `mythology_wisdom_engine.py` | 原型分析、英雄之旅 | 0.02 |
| 文学叙事 | `literary_narrative_engine.py` | 叙事结构、人物塑造 | 0.02 |
| 人类学 | `anthropology_wisdom_engine.py` | 文化模式、跨文化理解 | 0.01 |
| 行为塑造 | `behavior_shaping_engine.py` | 强化学习、行为改变 | 0.01 |
| 科学思维 | `science_thinking_engine.py` | 假设验证、系统分析 | 0.02 |
| 社会科学 | `social_science_engine.py` | 社会规律、市场分析 | 0.03 |
| 王阳明心学 | `yangming_xinxue_engine.py` | 知行合一、致良知 | 0.04 |
| 杜威反省 | `dewey_thinking_engine.py` | 反思实践、持续改进 | 0.03 |
| 顶级思维法 | `top_thinking_engine.py` | 多元模型、逆向思考 | 0.05 |
| 自然科学 | `natural_science_unified.py` | 自然规律探索 | 0.03 |
| 中国消费文化 | `chinese_consumer_culture_engine.py` | 本土消费洞察 | 0.03 |
| WCC智慧演化 | `wcc_evolutionary_core.py` | 群体智慧、协同进化 | 0.03 |
| 历史思想三维度 | `historical_thought_trinity_engine.py` | 历史智慧叙事 | 0.03 |
| 心理学 | `psychology_wisdom_engine.py` | 人格分析、潜意识探索 | 0.02 |
| 系统论 | `systems_thinking_engine.py` | 整体性、反馈回路 | 0.01 |
| 管理学 | `management_wisdom_engine.py` | 目标管理、组织效能 | 0.02 |
| 纵横家 | `zongheng_wisdom_engine.py` | 合纵连横、游说外交 | 0.02 |
| 墨家 | `mozi.py` | 兼爱非攻、工程创新 | 0.03 |
| 法家 | `hanfeizi.py` | 法治术势、制度设计 | 0.04 |
| 经济学 | `economics_wisdom_engine.py` | 资源配置、市场均衡 | 0.04 |
| 名家 | `mingjia_wisdom_engine.py` | 名实之辩、逻辑悖论 | 0.03 |
| 阴阳家 | `wuxing_wisdom_engine.py` | 阴阳五行、天人感应 | 0.04 |
| 社会学 | `sociology_wisdom.py` | 社会结构、阶层分析 | 0.04 |
| 行为经济学 | `behavioral_economics_wisdom.py` | 认知偏差、助推设计 | 0.04 |
| 传播学 | `communication_wisdom.py` | 传播模型、舆论引导 | 0.03 |
| 文化人类学 | `anthropology_wisdom.py` | 文化模式、符号解读 | 0.02 |
| 政治经济学 | `political_economics_wisdom.py` | 制度分析、政策博弈 | 0.04 |
| 组织心理学 | `organizational_psychology_wisdom.py` | 组织文化、团队凝聚 | 0.03 |
| 社会心理学 | `social_psychology_wisdom.py` | 态度改变、社会影响 | 0.03 |

### 引擎调度机制

```
用户问题
    ↓
ProblemTypeClassifier (问题分类)
    ↓
MeshRouting.evaluate_complexity() (复杂度评估)
    ├── SIMPLE → 单引擎快速响应
    ├── MODERATE → 2-3引擎协同
    ├── COMPLEX → 5-10引擎并行
    └── CRITICAL → 全引擎+七人大会
    ↓
WisdomDispatcher (学派分发)
    ↓
_engine_registry[WisdomSchool] → (module, class)
    ↓
动态导入 + 实例化 + 推理执行
    ↓
ClawRouter (贤者路由)
    ↓
ReActLoop (闭环推理)
    ↓
最终答案 + 置信度 + 推理轨迹
```

---

## 📚 21格知识系统详解

### 系统架构

21格知识系统是 Somn 的方法论知识库，采用格子化存储和网状关联设计。

```
┌─────────────────────────────────────────────────────────────┐
│                    Knowledge Cells System                    │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                     A系列: 智慧核心 (8格)               │ │
│  │  A1逻辑判断 → A2智慧模块 → A3论证审核 → A4判断决策     │ │
│  │       ↓              ↓              ↓              ↓    │ │
│  │  A5五层架构 → A6核心执行链 → A7感知记忆 → A8反思进化   │ │
│  └─────────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    B系列: 运营策略 (9格)                 │ │
│  │  B1用户增长 → B2直播运营 → B3私域运营 → B4活动策划     │ │
│  │       ↓              ↓              ↓              ↓    │ │
│  │  B5会员运营 → B6广告策划 → B7地产策划 → B8招商策划     │ │
│  │       ↓                                                       │ │
│  │  B9策略运营                                           │ │
│  └─────────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    C系列: 执行战术 (4格)                  │ │
│  │  C1电商运营 → C2数据运营 → C3内容营销 → C4广告投放     │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### A系列: 智慧核心 (8格)

| ID | 名称 | 文件 | 核心能力 | 关联格子 |
|----|------|------|----------|----------|
| A1 | 逻辑判断 | `A1_逻辑判断.md` | 三层推理 + 8种谬误检测 | A2, A3 |
| A2 | 智慧模块 | `A2_智慧模块.md` | 25学派融合 + 四级调度 | A1, A5 |
| A3 | 论证审核 | `A3_论证审核.md` | 翰林院三轮审核 | A1, A4 |
| A4 | 判断决策 | `A4_判断决策.md` | 七人投票 + 太极阴阳 | A3, B9 |
| A5 | 五层架构 | `A5_五层架构.md` | Somn核心技术架构 | A6, A7 |
| A6 | 核心执行链 | `A6_核心执行链.md` | 五步主链 + 并行化 | A8, B9 |
| A7 | 感知记忆 | `A7_感知记忆.md` | 快速扫描 + 直觉反应 | A8 |
| A8 | 反思进化 | `A8_反思进化.md` | ROI追踪 + 强化学习 | A7, B9 |

### B系列: 运营策略 (9格)

| ID | 名称 | 文件 | 专业领域 | 关联格子 |
|----|------|------|----------|----------|
| B1 | 用户增长 | `B1_互联网用户增长.md` | AARRR / 裂变 / 私域 | B2, B3, C3 |
| B2 | 直播运营 | `B2_直播运营.md` | 三角定律 / FABE话术 | B1, B5, C4 |
| B3 | 私域运营 | `B3_私域运营.md` | 企微 / 社群 / 沉淀 | B4, B5 |
| B4 | 活动策划 | `B4_活动策划.md` | 策划 / 执行 / 复盘 | B3, C1 |
| B5 | 会员运营 | `B5_会员运营.md` | 体系设计 / 权益设计 | B2, B3 |
| B6 | 广告策划 | `B6_广告策划.md` | 投放策略 / 优化 | B7, C4 |
| B7 | 地产策划 | `B7_地产策划.md` | 获客 / 转化 / 维系 | B6, B8 |
| B8 | 招商策划 | `B8_招商策划.md` | 招商策略 / 洽谈 | B7, B4 |
| B9 | 策略运营 | `B9_策略运营.md` | 规划 / 执行 / 复盘 | B1, C2, A4 |

### C系列: 执行战术 (4格)

| ID | 名称 | 文件 | 核心工具 | 关联格子 |
|----|------|------|----------|----------|
| C1 | 电商运营 | `C1_电商运营.md` | 流量 / 转化 / 供应链 | C2, C3 |
| C2 | 数据运营 | `C2_数据运营.md` | 指标 / 分析 / 数据驱动 | C1, B9 |
| C3 | 内容营销 | `C3_内容营销.md` | 选题 / 创作 / 分发 | C1, C4 |
| C4 | 广告投放 | `C4_广告投放.md` | 平台 / 定向 / ROI | C3, B2 |

### 格子关联图

```
A系列内部: A1↔A2↔A3↔A4, A5↔A6↔A7↔A8, A6↔A8
B系列内部: B1↔B2↔B3, B3↔B4↔B5, B5↔B2, B6↔B7↔B8, B8↔B4, B1↔B9
C系列内部: C1↔C2↔C3↔C4
跨系列关联: A4↔B9, A6↔B9, A8↔B9, B1↔B9, B2↔C4, B3↔C3
```

---

## 🧠 神经记忆系统 v21详解

### 系统架构

神经记忆系统是 Somn 的学习与记忆核心，采用三层记忆架构和Hebbian学习机制。

```
┌─────────────────────────────────────────────────────────────┐
│               Neural Memory System v21                       │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                    V3 主线版本                          │ │
│  │  ├── NeuralMemorySystemV3 (高性能向量索引版)           │ │
│  │  ├── MemoryEngine (记忆管理引擎)                       │ │
│  │  ├── KnowledgeEngine (知识库引擎)                      │ │
│  │  ├── ReasoningEngine (逻辑推理引擎)                    │ │
│  │  ├── LearningEngine (自主学习引擎)                     │ │
│  │  └── ValidationEngine (验证引擎)                       │ │
│  └───────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                    V5 超级记忆                          │ │
│  │  ├── SuperNeuralMemory (贤者记忆集成)                  │ │
│  │  ├── MemoryEntry (记忆条目)                            │ │
│  │  ├── MemoryQuery (记忆查询)                            │ │
│  │  └── recall() / get_super_memory()                    │ │
│  └───────────────────────────────────────────────────────┘ │
│                           ↓                                  │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                 v1.0 学习系统升级                      │ │
│  │  ├── AdaptiveStrategyEngine (自适应策略引擎)           │ │
│  │  ├── ReinforcementBridge (强化学习桥接器)              │ │
│  │  ├── MemoryLifecycleManager (记忆生命周期管理)         │ │
│  │  └── LearningPipeline (学习流水线)                     │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 三层记忆架构

| 层级 | 实现 | 容量 | 持久化 | 特点 |
|------|------|------|--------|------|
| **短期记忆** | 内存List[Dict] | 50条FIFO | 否 | 快速读写，当前会话有效 |
| **情景记忆** | 内存List[MemoryEpisode] | max_episodes上限 | JSON文件 | 重要事件持久化 |
| **归档记忆** | 磁盘JSON文件 | 无限 | 是(archive/) | 低重要性淘汰时归档 |

### 记忆类型系统

| 类型 | 说明 | 激活场景 |
|------|------|----------|
| WORKING | 工作记忆 | 当前任务处理 |
| EPISODIC | 情景记忆 | 重要事件记录 |
| SEMANTIC | 语义记忆 | 知识概念存储 |
| PROCEDURAL | 程序记忆 | 技能方法内化 |
| SENSORY | 感知记忆 | 原始输入缓存 |

### Hebbian学习机制

核心原则：**一起激活的神经元，连接会加强** (Cells that fire together, wire together)

```python
# Hebbian学习公式
Δw = η * a * b
# w: 突触权重
# η: 学习率
# a: 突触前激活
# b: 突触后激活
```

### 强化学习集成 (v1.0)

| 组件 | 功能 | 关键参数 |
|------|------|----------|
| RLExperience | 经验回放缓冲 | 128维状态向量 |
| PatternUpdate | 模式更新 | DQN配置 |
| ReinforcementBridge | 反馈↔RL集成 | 深度强化学习 |

### 记忆生命周期管理

| 阶段 | 机制 | 阈值 |
|------|------|------|
| 巩固 | 情景记忆写入 | consolidation_threshold=50 |
| 衰减 | 知识遗忘曲线 | 指数衰减模型 |
| 复习 | 间隔重复 | 艾宾浩斯曲线 |
| 归档 | 低重要性淘汰 | importance<0.3 |

---

## 👑 贤者Claw子系统详解

### 系统定位

贤者Claw是Somn的专家子代理系统，将763个历史智者转化为可独立运行的智能体实例。

```
┌─────────────────────────────────────────────────────────────┐
│                  Phase 4: Claw子智能体系统                    │
│                                                             │
│  Phase 0 (830篇) ──→ Phase 1 (760份) ──→ Phase 2 (779条)   │
│  深度学习文档       蒸馏文档          WisdomCode编码          │
│       │                   │                    │            │
│       └───────────────────┼────────────────────┘            │
│                           ↓                                  │
│              Phase 3: SageProxyFactory                     │
│              (751个克隆实例)                                │
│                           ↓                                  │
│              Phase 4: ClawArchitect×763                      │
│              (YAML配置驱动 + 四模块运行时)                   │
└─────────────────────────────────────────────────────────────┘
```

### 四模块架构

| 模块 | 功能 | 核心组件 |
|------|------|----------|
| **Perception** | 感知输入 | YAML元数据、触发词、上下文注入 |
| **Reasoning** | 推理闭环 | ReActLoop (Thought→Action→Observation) |
| **Execution** | 技能执行 | SkillsToolChain (10种标准技能) |
| **Feedback** | 反馈学习 | ClawMemoryAdapter (三层记忆) |

### 10种标准技能

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

### 推理风格

| 风格 | 值 | 行为特征 |
|------|-----|----------|
| DEEP_ANALYTICAL | deep_analytical | 偏好工具调用和深层推理，迭代次数多 |
| INTUITIVE_WISDOM | intuitive_wisdom | 快速收敛，直觉判断优先 |
| PRACTICAL_ACTION | practical_action | 行动导向，快速给出方案 |
| SYSTEMATIC_LOGIC | systematic_logic | 严谨逻辑推演 |
| NARRATIVE_POETIC | narrative_poetic | 叙事化表达，注重语境 |
| DIALECTICAL | dialectical | 多视角辩证综合 |

### 六维认知向量

| 维度 | 默认值 | 含义 |
|------|--------|------|
| cog_depth (思维深度) | 7.0 | 分析问题本质的能力 |
| decision_quality (决策质量) | 7.0 | 做出正确选择的能力 |
| value_judge (价值判断) | 7.0 | 道德和价值评估能力 |
| gov_decision (治理决策) | 7.0 | 组织管理决策能力 |
| strategy (战略思维) | 7.0 | 长远规划能力 |
| self_mgmt (自我管理) | 7.0 | 自我反思和修正能力 |

### 路由机制

```
用户输入
    │
    ├─ 1. 触发词精确匹配 (triggers字段，评分=匹配长度加权)
    │     └─ 匹配多个? → 取最高分为主Claw，次高2个为协作者
    │
    ├─ 2. 名称直接提及 (query中包含某Claw名字)
    │     └─ 置信度0.95 (高度确定)
    │
    ├─ 3. 学派关键词推断 (8大学派关键词表)
    │     └─ 在匹配学派中取cog_depth最高的Claw
    │     └─ 置信度0.7
    │
    └─ 4. 兜底 (默认Claw，通常为孔子)
          └─ 置信度0.2
```

---

## 📖 藏书阁V1.0详解

### 系统定位

藏书阁V1.0是Somn的全局记忆中心，从神之架构内部的独立记忆体系升级为Somn全局记忆中心。

### 八大分馆

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

### 记忆来源 (20种)

| 来源类型 | 说明 | 分类 |
|----------|------|------|
| DEPARTMENT_RESULT | 部门决策 | 原有6种 |
| TALENT_EVALUATION | 人才评估 | 原有6种 |
| HISTORICAL_DECISION | 历史决策 | 原有6种 |
| HANLIN_REVIEW | 翰林审核 | 原有6种 |
| CONGRESS_VOTE | 大会投票 | 原有6种 |
| SYSTEM_EVENT | 系统事件 | 原有6种 |
| CLAW_EXECUTION | Claw执行产出 | V1.0新增 |
| CLAW_MEMORY | Claw记忆 | V1.0新增 |
| SAGE_ENCODING | 智慧编码 | V1.0新增 |
| SAGE_DISTILLATION | 蒸馏产出 | V1.0新增 |
| NEURAL_MEMORY | 神经记忆 | V1.0新增 |
| SUPER_MEMORY | 超维记忆 | V1.0新增 |
| LEARNING_STRATEGY | 学习策略 | V1.0新增 |
| RESEARCH_FINDING | 研究发现 | V1.0新增 |
| EMOTION_RESEARCH | 情绪研究 | V1.0新增 |
| OPENCLAW_FETCH | OpenClaw获取 | V1.0新增 |
| ROI_TRACKING | ROI追踪 | V1.0新增 |
| USER_INTERACTION | 用户交互 | V1.0新增 |
| SYSTEM_PERFORMANCE | 系统性能 | V1.0新增 |
| BRIDGE_REPORT | 桥接报告 | V1.0新增 |

### 五级权限模型

| 权限等级 | 代码 | 能力 | 默认持有者 |
|---------|------|------|-----------|
| 只读 | READ_ONLY | 查询记忆 | 全系统默认 |
| 提交 | SUBMIT | 提交新记忆(不能修改) | 子系统自动汇报 |
| 写入 | WRITE | 写入/修改 | 格子管理员 |
| 删除 | DELETE | 删除记忆 | 大学士级 |
| 管理 | ADMIN | 配置/权限管理 | 大学士独享 |

### 持久化结构

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

### 跨系统桥接架构

```
┌──────────────────────────────────────────────────────────┐
│                   藏书阁 V1.0（全局记忆中心）                │
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
```

---

## 🧪 测试指南

### 测试结构

```
tests/
├── conftest.py                 # 共享 fixtures
├── test_reasoning_engine.py   # 推理引擎测试
├── test_scheduler_system.py   # 调度系统测试
├── test_knowledge_cells.py     # 知识格子测试
├── test_neural_memory.py       # 神经记忆测试
├── test_api_server.py         # API 服务测试
├── test_wisdom_schools.py      # 智慧学派测试
├── test_claw_agents.py         # Claw 代理测试
└── ...
```

### 运行测试

```bash
# 全量测试 (推荐)
pytest somn/tests/ -v

# 带覆盖率报告
pytest somn/tests/ --cov=smart_office_assistant.src --cov-report=html -v

# 快速冒烟测试 (排除慢速)
pytest somn/tests/ -m "not slow" -v

# 单个测试文件
pytest somn/tests/test_reasoning_engine.py -v

# 单个测试用例
pytest somn/tests/test_reasoning_engine.py::test_basic_reasoning -v

# 并行执行 (加速)
pytest somn/tests/ -n auto -v

# 失败时立即停止
pytest somn/tests/ -x -v
```

### 测试指标

| 指标 | 当前值 | 目标值 |
|------|--------|--------|
| 测试文件数 | 21个 | 持续增加 |
| 测试用例数 | 543个 | 800+ |
| 通过率 | **100%** | 保持100% |
| 失败数 | 0 | 0 |
| 跳过数 | 25 | - |
| 覆盖率 | 78% | 85%+ |

### 测试规范

详见 [TESTING_RULES.md](somn/TESTING_RULES.md)

---

## 🛠️ 技术栈详解

### 后端技术

| 组件 | 技术选型 | 用途 |
|------|----------|------|
| Web框架 | FastAPI + Uvicorn | 高性能异步API |
| 数据验证 | Pydantic v2 | 请求/响应模型定义 |
| 数据库 | SQLite (WAL模式) | 轻量级本地存储 |
| HTTP客户端 | httpx | 异步HTTP请求 |
| WebSocket | fastapi websockets | 实时通信 |
| 日志 | loguru | 结构化日志 |
| 配置 | PyYAML | 配置文件解析 |

### 前端技术

| 组件 | 技术选型 | 用途 |
|------|----------|------|
| GUI框架 | PyQt6 | 跨平台桌面应用 |
| 样式 | QSS | Qt样式表 |
| 缓存 | SQLite | 本地数据缓存 |
| HTTP | httpx | API通信 |
| WebSocket | websockets | 实时更新 |

### 模型技术

| 模型 | 角色 | 参数量 | 用途 |
|------|------|--------|------|
| Gemma4 | 主脑 | 2B | 复杂推理、主决策 |
| Llama-3.2 | 副脑 | 3B | 辅助推理、快速响应 |
| MiniMax M2.7 | 云端 | - | 超大规模任务 |
| OpenAI | 云端 | - | 备用模型 |

---

## 📦 开发依赖

### 核心运行时依赖

```bash
# 安装命令
pip install torch transformers safetensors numpy pandas pyyaml requests loguru pydantic pytest httpx uvicorn fastapi python-multipart
```

### 前端GUI依赖

```bash
pip install PyQt6 pyyaml loguru python-docx reportlab websockets
```

### 开发工具依赖

```bash
# 代码质量
pip install pylint flake8 black isort mypy

# 安全扫描
pip install bandit safety

# 测试
pip install pytest pytest-cov pytest-asyncio pytest-mock

# 预提交钩子
pip install pre-commit
```

完整依赖见 [requirements.txt](somn/requirements.txt) 和 [requirements-dev.txt](somn/requirements-dev.txt)

---

## ⚙️ 配置说明

### 配置文件结构

```
config/
├── local_config.yaml     # 本地运行配置
├── server_config.yaml    # API服务配置
└── storage_config.yaml  # 存储配置
```

### local_config.yaml 示例

```yaml
# 服务配置
server:
  host: "127.0.0.1"
  port: 8964
  workers: 4

# 模型配置
models:
  local:
    provider: "ollama"
    endpoint: "http://localhost:11434"
    main_model: "gemma4:2b"
    sub_model: "llama3.2:3b"
  cloud:
    enabled: true
    providers:
      - name: "minimax"
        api_key: "${MINIMAX_API_KEY}"
      - name: "openai"
        api_key: "${OPENAI_API_KEY}"

# 缓存配置
cache:
  enabled: true
  ttl: 3600
  max_size: "1GB"

# 日志配置
logging:
  level: "INFO"
  format: "{time} | {level} | {message}"
  rotation: "100 MB"
```

### 环境变量

```bash
# 模型API密钥
export MINIMAX_API_KEY="your-api-key"
export OPENAI_API_KEY="your-api-key"

# 可选: 自定义端口
export SOMN_PORT=8964

# 可选: 调试模式
export SOMN_DEBUG=true
```

---

## 🔒 安全策略

| 安全措施 | 说明 |
|----------|------|
| **数据隔离** | 所有数据仅存储本地，禁止云上传 |
| **凭证管理** | 使用环境变量存储API密钥，零硬编码 |
| **审计日志** | 所有敏感操作记录在案 |
| **权限最小化** | 模块间最小依赖原则 |
| **输入验证** | Pydantic严格模式，SQL注入防护 |
| **XSS防护** | 输出转义，防止XSS攻击 |
| **安全扫描** | bandit集成到CI/CD |

详见 [SECURITY.md](somn/SECURITY.md)

---

## ❓ 常见问题

### Q1: 启动时报错 "ModuleNotFoundError"

**问题**: 提示模块找不到

**解决方案**:
```bash
# 确保在项目根目录
cd somn-git-repo

# 重新安装依赖
pip install -e somn
pip install -e Somn-GUI
```

### Q2: 本地模型无法连接

**问题**: Ollama服务连接失败

**解决方案**:
```bash
# 1. 检查Ollama服务
ollama list

# 2. 如果没有运行，启动服务
ollama serve

# 3. 拉取模型
ollama pull gemma4:2b
ollama pull llama3.2:3b

# 4. 测试模型
ollama run gemma4:2b "你好"
```

### Q3: API服务启动失败

**问题**: 端口被占用

**解决方案**:
```bash
# 方法1: 更换端口
export SOMN_PORT=8965

# 方法2: 杀死占用进程
netstat -ano | findstr :8964
taskkill /PID <PID> /F
```

### Q4: 前端GUI闪退

**问题**: PyQt6初始化失败

**解决方案**:
```bash
# 重新安装PyQt6
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip
pip install PyQt6

# 检查Qt依赖
python -c "from PyQt6.QtCore import QT_VERSION_STR; print(QT_VERSION_STR)"
```

### Q5: 测试失败

**问题**: 部分测试用例失败

**解决方案**:
```bash
# 查看详细错误
pytest somn/tests/ -v --tb=long

# 检查测试环境
python somn/scripts/health_check.py

# 跳过网络相关测试
pytest somn/tests/ -m "not network" -v
```

### Q6: 如何查看日志

```bash
# 实时查看日志
tail -f somn/logs/somn.log

# 查看错误日志
grep -i error somn/logs/somn.log

# 按时间过滤
grep "2024-01-15" somn/logs/somn.log
```

---

## 📄 开源协议

本项目基于 **GNU AGPL v3 License** 开源。

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

### AGPL v3 License 核心条款

| 条款 | 说明 |
|------|------|
| **自由使用** | 可自由运行、复制、分发、学习和修改本软件 |
| **商业使用** | 允许商业使用，无需特殊授权 |
| **私有权** | 可私有权形式使用 |
| **简单要求** | 保留版权声明即可 |

### MIT vs AGPL 的主要区别

| 场景 | MIT | AGPL |
|------|-----|------|
| 本地运行 | ✅ 允许 | ✅ 允许 |
| 修改后分发 | ⚠️ 需保留版权声明 | ⚠️ 需开源 |
| 网络服务使用 | ✅ 无额外要求 | ⚠️ **必须开源** |

> 💡 **推荐**: 如果您计划将 Somn 作为网络服务/云服务对外提供，MIT 是更宽松的选择。

详见 [LICENSE](LICENSE)

---

## 🤝 贡献指南

欢迎贡献代码！请遵循以下流程：

### 贡献流程

```bash
# 1. Fork 本仓库

# 2. 克隆你的Fork
git clone https://github.com/marcwadehan-png/somn-agent.git
cd somn

# 3. 创建特性分支
git checkout -b feature/AmazingFeature

# 4. 进行开发
# ... 编写代码 ...

# 5. 确保测试通过
pytest somn/tests/ -v

# 6. 提交代码
git commit -m 'Add: 添加新功能'

# 7. 推送到你的Fork
git push origin feature/AmazingFeature

# 8. 创建 Pull Request
```

### 代码规范

- 遵循 PEP 8 编码规范
- 使用 Black 进行代码格式化
- 使用 isort 整理导入
- 使用 Pylint 检查代码质量
- 所有新功能必须附带测试

### Commit Message 规范

```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 重构
test: 测试相关
chore: 构建/工具
```

详见 [CONTRIBUTING.md](somn/CONTRIBUTING.md) 和 [TESTING_RULES.md](somn/TESTING_RULES.md)

---

## 📚 更多文档

| 文档 | 说明 |
|------|------|
| [CHANGELOG.md](CHANGELOG.md) | 版本变更历史 (Keep a Changelog 标准) |
| [PROJECT_STATUS.md](somn/PROJECT_STATUS.md) | 项目状态概览 |
| [ROADMAP.md](ROADMAP.md) | 发展路线图与愿景 |
| [ARCHITECTURE.md](Somn-GUI/ARCHITECTURE.md) | 前后端分离架构设计 |
| [knowledge_cells/README.md](somn/knowledge_cells/README.md) | 知识格子系统文档 |
| [global_control_center/README.md](somn/global_control_center/README.md) | 全局控制中心文档 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 贡献指南与开发流程 |
| [SECURITY.md](SECURITY.md) | 安全策略与漏洞报告 |
| `docs/adr/` | 20篇 ADR 架构决策记录 |
| `file/系统文件/神之架构_V6_COMPLETE.md` | V6 完整架构文档 |
| `file/系统文件/快速启动指南.md` | 详细启动指南 |

> 💬 需要帮助？查看 [.github/SUPPORT.md](.github/SUPPORT.md) 获取支持渠道。

---

## 🏆 致谢

Somn 项目融合了人类智慧的精华：

| 思想流派 | 代表人物/学派 | 核心贡献 |
|----------|---------------|----------|
| **儒家** | 孔子、孟子 | 仁政、民本、中庸之道 |
| **道家** | 老子、庄子 | 无为而治、道法自然 |
| **法家** | 商鞅、韩非 | 法治、术势、权谋 |
| **墨家** | 墨子 | 兼爱、非攻、尚贤 |
| **兵家** | 孙武、吴子 | 战略、奇正、形势 |
| **佛家** | 各宗派 | 般若、禅定、慈悲 |
| **西方哲学** | 柏拉图、亚里士多德、康德 | 形而上学、逻辑学 |
| **现代心理学** | 弗洛伊德、荣格、马斯洛 | 潜意识、需求层次 |
| **管理学** | 德鲁克、波特 | 战略管理、竞争优势 |
| **投资哲学** | 芒格、巴菲特 | 价值投资、多元思维 |
| **科学方法** | 牛顿、爱因斯坦、图灵 | 物理世界、计算理论 |

> *「站在巨人的肩膀上，我们看得更远。」*
>
> *「集百家之长，成一家之言。」*

---

## 📞 联系方式

- **邮箱**: marcwadehan@gmail.com
- **项目主页**: https://github.com/marcwadehan-png/somn-agent
- **问题反馈**: https://github.com/marcwadehan-png/somn-agent/issues
- **讨论交流**: https://github.com/marcwadehan-png/somn-agent/discussions

---

<div align="center">

**Somn** — 让智能更普惠

*Version v6.2.0 | Built with ❤️*

</div>
