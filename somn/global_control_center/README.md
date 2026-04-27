# Somn 全局控制中心 (Global Control Center) v1.0.0

## 概述

Somn 全局控制中心是一个统一的前端启动系统，用于串联项目所有功能，实现对 Somn V6.2 项目的全局管理和操作。

## 功能特性

- **三模式启动**: CLI / GUI / Web
- **深度API集成**: 连接61个API端点
- **模块管理**: 32个顶层模块状态监控
- **引擎监控**: 45+智慧引擎实时状态
- **Claw管理**: 776个子代理控制
- **神经网络**: 57神经元/74突触/4集群
- **配置中心**: 配置编辑与热更新
- **健康检查**: 系统健康状态监控
- **日志系统**: 实时日志查看

## 快速启动

### 方式1: 主入口
```bash
cd /path/to/somn
python global_control_center/__init__.py --mode cli
python global_control_center/__init__.py --mode gui
python global_control_center/__init__.py --mode web --port 8970
```

### 方式2: 快速启动
```bash
python global_control_center/__main__.py cli
python global_control_center/__main__.py web -p 8080
```

## 启动模式

| 模式 | 命令 | 描述 |
|------|------|------|
| **CLI** | `--mode cli` | 命令行交互模式 |
| **GUI** | `--mode gui` | 图形界面 (Tkinter) |
| **Web** | `--mode web` | 浏览器访问 (Flask) |

## CLI命令

| 命令 | 描述 |
|------|------|
| `help` | 显示帮助 |
| `info` | 系统信息 |
| `status` | 运行状态 |
| `modules` | 模块列表 |
| `engines` | 引擎状态 |
| `claws` | Claw列表 |
| `scheduler` | 调度器状态 |
| `neural` | 神经网络状态 |
| `api` | API端点 |
| `config` | 配置管理 |
| `health` | 健康检查 |
| `logs` | 日志查看 |
| `start/stop` | 启停控制 |
| `clear` | 清除屏幕 |
| `exit` | 退出 |

## 系统架构

```
global_control_center/
├── __init__.py               # 主入口
├── __main__.py               # 快速启动
├── api_client.py             # API客户端 (61端点)
├── dashboard.py              # 仪表板
│
├── cli/                      # 命令行模式
│   ├── console.py             # CLI控制台
│   ├── commands.py            # 命令处理器
│   └── __init__.py
│
├── gui/                      # 图形界面
│   ├── main_window.py         # 主窗口
│   ├── dashboard.py           # 仪表板组件
│   ├── module_panel.py        # 模块面板
│   ├── engine_panel.py        # 引擎面板
│   ├── claw_panel.py          # Claw面板
│   ├── config_panel.py        # 配置面板
│   └── __init__.py
│
├── web/                      # Web模式
│   ├── app.py                 # Flask API v1
│   ├── app_v2.py              # Flask API v2 (增强)
│   ├── templates/             # HTML模板
│   │   ├── index.html         # 主页面
│   │   └── dashboard.html     # 仪表板
│   └── __init__.py
│
├── managers/                 # 管理器
│   ├── module_manager.py      # 模块管理
│   ├── engine_manager.py      # 引擎管理
│   ├── claw_manager.py       # Claw管理
│   ├── config_manager.py      # 配置管理
│   ├── somn_connector.py      # Somn连接器
│   └── __init__.py
│
├── schedulers/               # 调度监控
│   ├── wisdom_scheduler.py    # 智慧调度器
│   ├── claw_scheduler.py      # Claw调度器
│   └── __init__.py
│
└── utils/                    # 工具
    ├── color_printer.py       # 彩色输出
    ├── table_formatter.py     # 表格格式化
    └── __init__.py
```

## API端点集成

| 类别 | 数量 | 示例 |
|------|------|------|
| 基础端点 | 18 | /api/v1/health, /api/v1/chat |
| 管理端点 | 31 | /api/v1/admin/load-manager |
| 神经网络端点 | 12 | /api/v1/neural/status |

**总计**: 61个API端点

## 系统规模

| 组件 | 数量 |
|------|------|
| 顶层模块 | 32 |
| 智慧引擎 | 45+ |
| 智慧学派 | 35 |
| Claw子代理 | 776 |
| 问题类型 | 135 |
| 执行阶段 | A-G |
| 神经元 | 57 |
| 突触 | 74 |
| 集群 | 4 |

## 版本信息

- **控制中心版本**: v1.0.0
- **项目版本**: Somn V6.2
- **架构**: 神之架构最终完整版
- **日期**: 2026-04-26

## 作者

Somn Development Team
