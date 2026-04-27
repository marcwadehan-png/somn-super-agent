# Somn-GUI 启动器说明

## 快速启动方式

### 1. 一体化启动器 (`start_somn.py`)
```bash
python start_somn.py
```
同时启动后端和GUI。

### 2. 全功能套件 (`start_full_suite.py`)
```bash
python start_full_suite.py
```
启动后端 + 全局控制中心 + 传统GUI。

### 3. 全局控制中心 (`start_control_center.py`)
```bash
python start_control_center.py
```
仅启动全局控制中心（需后端运行）。

### 4. 快捷启动器 (`quick_launcher.py`)
```bash
python quick_launcher.py
```
交互式菜单选择启动模式。

### 5. Windows批处理 (`启动器.bat`)
双击运行，选择启动模式。

## 全局控制中心功能

| 选项卡 | 功能 |
|--------|------|
| 仪表板 | 6个统计卡片：模块/引擎/Claw/神经网络/调度器/健康 |
| 模块管理 | 32个模块状态监控 |
| 引擎监控 | 45+智慧引擎实时状态 |
| Claw管理 | 776个子代理按学派统计 |
| 神经网络 | Phase 1-5 可视化进度 |
| 日志查看 | 实时日志过滤显示 |
| 配置管理 | YAML配置编辑 |

## 全局控制中心模块

```
global_control_center/
├── __init__.py          # 三模式启动入口
├── api_client.py        # 61个API端点集成
├── dashboard.py         # 仪表板
├── cli/                 # CLI模式
├── gui/                 # GUI模式 (嵌入)
├── web/                 # Web模式
├── managers/            # 管理系统
├── schedulers/          # 调度监控
└── utils/               # 工具
```

## 端口说明

| 端口 | 服务 |
|------|------|
| 8964 | Somn API后端 |
| 8970 | Web仪表板 |
