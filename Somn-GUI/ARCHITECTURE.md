# Somn 前后端分离架构设计方案

> 版本: v1.0 | 日期: 2026-04-25
> 目标: 将 Somn 整体项目拆分为独立后端服务与前端交互两层，形成松耦合可独立部署的架构

---

## 一、架构总览

```
┌─────────────────────────────────────────────────────────────────────┐
│                        AI/Somn-GUI (前端)                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────────────┐ │
│  │ PyQt6  │ │  缓存层  │ │  状态层  │ │  API 客户端           │ │
│  │ 界面组件 │ │ SQLite   │ │ 内存管理 │ │  httpx/aiohttp        │ │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └───────────┬───────────┘ │
│       │            │           │                    │             │
│       └────────────┼───────────┼────────────────────┘             │
│                    │  本地缓存预加载 + 离线交互缓存                │
└────────────────────┼──────────────────────────────────────────────┘
                     │  HTTP/REST API (动态发现)
┌────────────────────┼──────────────────────────────────────────────┐
│                    ▼                                               │
│                     ★ FastAPI 网关层                               │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  /api/v1/*   RESTful API 接口                                │ │
│  │  /api/v1/ws  WebSocket 实时通信                              │ │
│  └──────────────────────┬───────────────────────────────────────┘ │
│                        AI/Somn (后端)                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────────┐ │
│  │ 智能体层 │ │ 引擎层   │ │ 知识层   │ │  存储层              │ │
│  │ SomnCore │ │ 45引擎   │ │ 知识图谱 │ │  SQLite/藏书阁       │ │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └──────────┬───────────┘ │
│       └─────────────┼────────────┼─────────────────┘             │
│                     │  本地大模型 (Gemma4/Llama)                 │
│                     │  [服务器本地配置，不暴露给前端]             │
└──────────────────────────────────────────────────────────────────┘
```

---

## 二、目录结构规划

### 2.1 后端: AI/Somn (根目录动态)

```
somn/                                  # 后端根目录 (路径动态)
├── smart_office_assistant/            # 核心项目包
│   ├── src/                           # ★ 全部核心源码 (37个子模块)
│   │   ├── core/                      # 核心层 (SomnCore, AgentCore, LLM引擎)
│   │   ├── intelligence/              # 智能体层 (45引擎, 智慧调度)
│   │   ├── main_chain/                # 主线架构 (并行路由, 交叉织网)
│   │   ├── neural_memory/             # 神经记忆系统
│   │   ├── knowledge_graph/           # 知识图谱
│   │   ├── growth_engine/             # 增长引擎
│   │   ├── tool_layer/                # 工具层 (LLM服务, 云模型)
│   │   ├── documents/                 # 文档引擎
│   │   ├── ...                        # 其余子模块不变
│   │   └── __init__.py
│   │
│   ├── config/                        # 配置文件
│   │   ├── court_config.yaml          # 神之架构配置
│   │   └── main_chain_config.yaml     # 主线架构配置
│   ├── config.yaml                    # 主配置
│   ├── .env                           # ★ 服务器本地配置 (LLM密钥等)
│   │
│   └── ...                            # 其余文件不变
│
├── config/                            # 服务器级配置 (仅后端生效)
│   ├── local_config.yaml              # 独立运行配置 v1.0
│   ├── storage_config.yaml            # 统一存储配置 v1.0
│   └── server_config.yaml             # ★ 新增: API服务配置
│
├── models/                            # ★ 本地大模型 (仅服务器)
│   ├── gemma4-local-b/                # B模型 (主脑)
│   └── llama-3.2-1b-instruct/         # A模型 (副脑)
│
├── data/                              # 运行时数据 (仅服务器)
│   ├── core/
│   ├── run/
│   ├── logs/
│   ├── imperial_library/
│   └── engine_cache/
│
├── api/                               # ★ 新增: API 服务层
│   ├── __init__.py
│   ├── server.py                      # FastAPI 应用入口
│   ├── routes/                        # API 路由定义
│   │   ├── __init__.py
│   │   ├── chat.py                    # 对话接口
│   │   ├── knowledge.py               # 知识库接口
│   │   ├── documents.py               # 文档生成接口
│   │   ├── analysis.py                # 分析/策略接口
│   │   ├── memory.py                  # 记忆系统接口
│   │   ├── learning.py                # 学习系统接口
│   │   ├── wisdom.py                  # 智慧引擎接口
│   │   ├── health.py                  # 健康检查/系统状态
│   │   └── config.py                  # 配置查询接口
│   ├── middleware/                     # 中间件
│   │   ├── __init__.py
│   │   ├── cors.py                    # CORS 配置
│   │   ├── auth.py                    # 认证中间件
│   │   └── rate_limit.py              # 限流中间件
│   ├── schemas/                       # 数据模型 (Pydantic)
│   │   ├── __init__.py
│   │   ├── chat.py                    # 对话请求/响应模型
│   │   ├── knowledge.py               # 知识库模型
│   │   └── common.py                  # 通用响应模型
│   └── deps.py                        # 依赖注入 (SomnCore实例等)
│
├── scripts/                           # 运维脚本
├── tests/                             # 测试套件
├── docs/                              # 文档
├── pyproject.toml
├── requirements.txt
└── start_server.py                    # ★ 新增: API服务启动入口
```

### 2.2 前端: AI/Somn-GUI (根目录动态)

```
Somn-GUI/                              # 前端根目录 (路径动态)
├── somngui/                           # ★ 前端主包
│   ├── __init__.py
│   │
│   ├── app.py                         # 应用入口 (PyQt6)
│   │
│   ├── core/                          # 核心框架
│   │   ├── __init__.py
│   │   ├── config.py                  # 前端配置管理
│   │   ├── connection.py              # ★ 后端连接管理 (动态路径发现)
│   │   └── state.py                   # 应用状态管理
│   │
│   ├── client/                        # ★ API 客户端层
│   │   ├── __init__.py
│   │   ├── base_client.py             # HTTP客户端基类
│   │   ├── chat_client.py             # 对话API客户端
│   │   ├── knowledge_client.py        # 知识库API客户端
│   │   ├── document_client.py         # 文档API客户端
│   │   ├── analysis_client.py         # 分析API客户端
│   │   └── system_client.py           # 系统/健康检查客户端
│   │
│   ├── cache/                         # ★ 本地缓存系统
│   │   ├── __init__.py
│   │   ├── cache_manager.py           # 缓存管理器 (统一入口)
│   │   ├── preloader.py               # 高频数据预加载器
│   │   ├── offline_cache.py           # 离线交互缓存
│   │   └── cache_db.py                # 本地缓存数据库 (SQLite)
│   │
│   ├── gui/                           # ★ UI界面层 (从Somn迁移)
│   │   ├── __init__.py
│   │   ├── main_window.py             # 主窗口
│   │   ├── main_window/
│   │   │   ├── _mw_chat.py            # 对话界面
│   │   │   ├── _mw_editor.py          # 文档编辑器
│   │   │   ├── _mw_kb.py              # 知识库界面
│   │   │   ├── _mw_kb_ops.py          # 知识库操作
│   │   │   ├── _mw_file_ops.py        # 文件操作
│   │   │   ├── _mw_export.py          # 文档导出
│   │   │   ├── _mw_scan.py            # 文件扫描
│   │   │   └── _mw_tools.py           # 报告/策略工具
│   │   ├── tray_icon.py               # 系统托盘
│   │   ├── styles/                    # 样式表
│   │   │   ├── light.qss
│   │   │   └── dark.qss
│   │   └── widgets/                   # 自定义组件
│   │       └── ...
│   │
│   └── utils/                         # 工具函数
│       ├── __init__.py
│       ├── logger.py                  # 日志工具
│       └── helpers.py                 # 辅助函数
│
├── cache_data/                        # ★ 本地缓存数据目录
│   ├── cache.db                       # 缓存SQLite数据库
│   ├── preloaded/                     # 预加载数据
│   │   ├── knowledge_index.json       # 知识库索引
│   │   ├── config_snapshot.json       # 配置快照
│   │   └── system_status.json         # 系统状态
│   └── offline/                       # 离线缓存
│       └── pending_requests.db        # 待同步请求队列
│
├── config/                            # 前端配置
│   ├── gui_config.yaml                # GUI界面配置
│   └── cache_config.yaml              # 缓存策略配置
│
├── requirements.txt                   # 前端依赖 (PyQt6, httpx等)
├── pyproject.toml
├── start_gui.py                       # ★ 前端启动入口
└── README.md
```

---

## 三、动态路径发现机制

### 3.1 核心原则

> **无论路径如何调整，Somn-GUI 都能调用 Somn 后端**

### 3.2 后端服务注册

后端启动时，自动将自身地址写入一个 **约定位置的注册文件**：

```
注册文件位置: {系统TEMP目录}/somn_server_registry.json
Windows: %TEMP%/somn_server_registry.json
Linux/Mac: /tmp/somn_server_registry.json
```

```json
{
  "version": "1.0",
  "server_url": "http://127.0.0.1:8964",
  "api_prefix": "/api/v1",
  "ws_url": "ws://127.0.0.1:8964/api/v1/ws",
  "somn_root": "./somn",
  "pid": 12345,
  "started_at": "2026-04-25T20:00:00",
  "instance_id": "uuid-xxxx"
}
```

### 3.3 前端发现流程

```
Somn-GUI 启动
    │
    ├─ 1. 读取本地 gui_config.yaml → 获取 server_url (手动配置)
    │     如果配置了且可连通 → 直接使用
    │
    ├─ 2. 读取 {TEMP}/somn_server_registry.json (自动发现)
    │     如果存在且进程存活 → 使用注册地址
    │
    ├─ 3. 扫描本地网络 (可选)
    │     尝试 127.0.0.1:8964, 192.168.x.x:8964
    │
    └─ 4. 显示连接配置对话框让用户手动输入
```

### 3.4 后端连接管理器 (前端)

```python
# somngui/core/connection.py

class BackendConnection:
    """后端连接管理器 - 动态路径发现"""

    DEFAULT_PORT = 8964
    REGISTRY_FILE = Path(tempfile.gettempdir()) / "somn_server_registry.json"

    def discover_backend(self) -> str:
        """多策略发现后端地址"""
        # 策略1: 配置文件
        # 策略2: 注册文件
        # 策略3: 默认地址探测
        # 策略4: 用户手动输入

    def check_health(self, url: str) -> bool:
        """检查后端是否可达"""
        # GET {url}/api/v1/health

    def get_api_base(self) -> str:
        """获取API基础URL"""
```

---

## 四、API 接口设计

### 4.1 接口概览

| 模块 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 健康 | GET | /api/v1/health | 后端健康检查 |
| 状态 | GET | /api/v1/status | 系统状态/版本 |
| 配置 | GET | /api/v1/config | 获取前端可见配置 |
| 对话 | POST | /api/v1/chat | 发送对话消息 |
| 对话 | GET | /api/v1/chat/stream | SSE 流式对话 |
| 对话 | WS | /api/v1/ws | WebSocket 实时通信 |
| 知识库 | GET | /api/v1/knowledge | 获取知识库列表 |
| 知识库 | POST | /api/v1/knowledge/search | 搜索知识 |
| 知识库 | POST | /api/v1/knowledge/add | 添加知识 |
| 文档 | POST | /api/v1/documents/generate | 生成文档 |
| 文档 | GET | /api/v1/documents/{id} | 获取文档 |
| 文档 | GET | /api/v1/documents/export | 导出文档 |
| 分析 | POST | /api/v1/analysis/strategy | 策略分析 |
| 分析 | POST | /api/v1/analysis/market | 市场分析 |
| 记忆 | GET | /api/v1/memory | 获取记忆列表 |
| 学习 | GET | /api/v1/learning/status | 学习状态 |
| 学习 | POST | /api/v1/learning/trigger | 触发学习 |
| 智慧 | POST | /api/v1/wisdom/query | 智慧引擎查询 |
| 智慧 | GET | /api/v1/wisdom/schools | 获取学派列表 |

### 4.2 认证机制

- **本地模式**: API Key 认证 (写在配置文件中)
- **远程模式**: Token 认证 + HTTPS 加密
- 首次连接时交换密钥，后续请求携带 token

---

## 五、前端本地缓存系统

### 5.1 缓存架构

```
┌─────────────────────────────────────────────────┐
│                  缓存管理器                       │
│  ┌─────────────┐  ┌──────────────┐              │
│  │ 预加载器     │  │ 离线缓存     │              │
│  │ Preloader   │  │ OfflineCache │              │
│  └──────┬──────┘  └──────┬───────┘              │
│         │                │                      │
│  ┌──────▼────────────────▼───────┐              │
│  │       本地缓存数据库           │              │
│  │       SQLite (cache.db)       │              │
│  │  ┌──────────┬─────────────┐   │              │
│  │  │ kv_cache │ obj_cache   │   │              │
│  │  │ (热点KV) │ (序列化对象) │   │              │
│  │  └──────────┴─────────────┘   │              │
│  └───────────────────────────────┘              │
└─────────────────────────────────────────────────┘
```

### 5.2 预加载策略

| 数据类型 | 预加载时机 | TTL | 说明 |
|----------|-----------|-----|------|
| 系统状态 | 启动时 | 5min | 版本、引擎状态 |
| 知识库索引 | 启动时 | 30min | 知识条目列表/分类 |
| 配置快照 | 启动时/变更时 | ∞ | UI配置、功能开关 |
| 近期对话 | 启动时 | 1h | 最近N条对话记录 |
| 学派列表 | 首次访问 | 24h | 35个智慧学派信息 |
| 行业模板 | 首次访问 | 24h | 行业知识模板 |

### 5.3 离线交互缓存

```python
# 离线模式工作流程:
# 1. 检测到后端不可达 → 自动切换离线模式
# 2. 用户操作记录到本地队列 (pending_requests.db)
# 3. 恢复连接后自动重放待处理请求
# 4. 只读操作从本地缓存返回数据
# 5. 写操作提示"将在恢复连接后同步"
```

---

## 六、服务器本地配置隔离

### 6.1 配置分层

| 配置文件 | 归属 | 说明 |
|----------|------|------|
| `.env` | 后端 | LLM API密钥、本地模型路径 |
| `config/local_config.yaml` | 后端 | LLM模型配置、存储配置 |
| `config/storage_config.yaml` | 后端 | 数据库路径、备份策略 |
| `models/` | 后端 | 本地大模型权重文件 |
| `config/server_config.yaml` | 后端 | API端口、认证配置 |
| `somn_gui/config/gui_config.yaml` | 前端 | 界面主题、字体、布局 |
| `somn_gui/config/cache_config.yaml` | 前端 | 缓存策略、预加载配置 |

### 6.2 后端 API 暴露策略

后端通过 `/api/v1/config` 接口向前端暴露 **经过过滤的安全配置子集**：

```python
# 后端暴露给前端的配置 (不包含密钥/路径等敏感信息)
SAFE_CONFIG_KEYS = [
    "ui.theme", "ui.language", "ui.font_size",
    "features.enable_web_search", "features.enable_ml_engine",
    "features.enable_emotion_wave", "features.enable_persona",
    "features.enable_rag", "features.enable_daily_learning",
    "neural_memory.enabled",
]
```

---

## 七、技术选型

| 层级 | 技术 | 说明 |
|------|------|------|
| 后端API | FastAPI + Uvicorn | 高性能异步API框架 |
| 异步通信 | WebSocket | 实时对话/状态推送 |
| 前端UI | PyQt6 | 跨平台桌面GUI |
| HTTP客户端 | httpx | 异步HTTP客户端 |
| 本地缓存 | SQLite + aiosqlite | 轻量级本地数据库 |
| 数据验证 | Pydantic v2 | 请求/响应模型 |
| 服务发现 | 文件注册 + 端口探测 | 零依赖服务发现 |
| 日志 | loguru | 结构化日志 |

---

## 八、迁移计划

### Phase 1: 后端 API 层 (当前阶段)
1. 在 Somn 中创建 `api/` 目录
2. 实现 FastAPI 服务入口 + 核心路由
3. 实现服务注册机制
4. 验证后端可独立启动

### Phase 2: 前端骨架
5. 创建 Somn-GUI 项目结构
6. 迁移 GUI 界面代码
7. 实现 API 客户端层
8. 实现后端动态发现

### Phase 3: 缓存系统
9. 实现本地缓存数据库
10. 实现预加载策略
11. 实现离线交互缓存

### Phase 4: 集成测试
12. 端到端前后端联调
13. 性能基准测试
14. 离线模式测试

---

## 九、启动方式

### 后端启动
```bash
cd {Somn根目录}
python start_server.py              # 启动API服务 (默认端口 8964)
python start_server.py --port 9000  # 自定义端口
python start_server.py --host 0.0.0.0  # 允许远程连接
```

### 前端启动
```bash
cd {Somn-GUI根目录}
python start_gui.py                 # 自动发现后端并启动
python start_gui.py --server http://192.168.1.100:8964  # 指定后端地址
python start_gui.py --offline       # 离线模式
```
