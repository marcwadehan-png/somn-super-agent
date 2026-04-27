# Contributing to Somn

感谢你对 Somn 项目的关注！本文档帮助你快速了解如何参与贡献。

## 🚀 Quick Start

```bash
# 1. Fork 并克隆仓库
git clone https://github.com/marcwadehan-png/somn-agent.git
cd somn

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate   # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. 运行测试
pytest somn/tests/ -v --tb=short

# 5. 开始编码！
```

## 📋 开发流程

### 1. 分支策略

| 分支类型 | 命名规范 | 用途 |
|----------|----------|------|
| `main` | — | 稳定发布分支 |
| `develop` | — | 开发集成分支 |
| `feature/*` | `feature/xxx` | 新功能开发 |
| `fix/*` | `fix/xxx` | Bug 修复 |
| `docs/*` | `docs/xxx` | 文档更新 |

> **注意**：所有 PR 都应提交到 `develop` 分支，由维护者合并到 `main`。

### 2. 提交规范 (Conventional Commits)

```
<type>(<scope>): <subject>

<body>
```

**常用 type**：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档变更
- `style`: 代码格式（不影响功能）
- `refactor`: 重构（非新功能、非修复）
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具链

**示例**：
```
feat(knowledge_cells): add cross-domain association inference

Add automatic link discovery between related knowledge cells based on
semantic similarity scoring (>0.8 threshold).

Closes #123
```

### 3. PR 流程

1. **Fork** 本仓库到你的 GitHub 账号
2. **Clone** 你的 fork：`git clone https://github.com/YOU/somn.git`
3. **创建特性分支**：`git checkout -b feature/my-feature develop`
4. **编写代码 + 测试**
5. **确保测试通过**：`pytest somn/tests/ -v`
6. **Commit & Push**
7. 在 GitHub 创建 **Pull Request** 到 `develop` 分支

### 4. PR 检查清单

在提交 PR 前，请确认：

- [ ] 代码遵循项目风格（`pylint` / `flake8` 通过）
- [ ] 新增功能包含对应的单元测试
- [ ] 所有现有测试通过（`pytest somn/tests/ -v`）
- [ ] Commit message 符合规范
- [ ] 没有引入新的安全漏洞（`bandit` 通过）
- [ ] 文档已更新（如有 API 变更）

## 🏗️ 项目结构概览

```
somn/
├── somn/
│   ├── api/                    # FastAPI 后端服务
│   │   ├── server.py           # 应用入口
│   │   └── routes/             # 路由模块
│   ├── smart_office_assistant/  # 核心引擎
│   │   ├── src/core/           # SomnCore 主引擎
│   │   ├── src/neural_memory/  # 神经记忆系统
│   │   ├── src/intelligence/   # 智慧调度器
│   │   └── src/tool_layer/     # LLM 工具层
│   ├── knowledge_cells/        # 知识格子系统
│   ├── global_control_center/  # 全局控制中心
│   ├── tests/                  # 测试套件
│   └── config/                 # 配置文件
├── Somn-GUI/                   # PyQt6 桌面前端
├── .github/workflows/          # CI/CD 配置
├── LICENSE                     # AGPL v3 许可证
├── README.md                   # 项目文档
└── requirements.txt            # Python 依赖
```

## 🧪 测试指南

### 运行全部测试
```bash
pytest somn/tests/ -v --tb=short
```

### 按分类运行
```bash
pytest somn/tests/ -k "core"       # 核心引擎测试
pytest somn/tests/ -k "memory"      # 记忆系统测试
pytest somn/tests/ -k "knowledge"   # 知识格子系统测试
pytest somn/tests/ -k "integration" # 集成测试
```

### 覆盖率报告
```bash
pytest somn/tests/ --cov=smart_office_assistant --cov-report=html
```

### 测试原则

Somn 遵循 **F.I.R.S.T** 原则：
- **F**ast — 测试要快
- **I**ndependent — 测试之间无依赖
- **R**epeatable — 结果可复现
- **S**elf-validating — 自动判断通过/失败
- **T**imely — 先写测试再写代码（TDD 推荐）

## 🔧 代码质量标准

| 工具 | 配置 | 最低要求 |
|------|------|----------|
| **pylint** | max-complexity=15, line-length=120 | 0 error |
| **flake8** | line-length=120, ignore E203/W503 | 0 violation |
| **mypy** | python>=3.11, 宽松模式 | 0 type error |
| **bandit** | 排除 tests/ | 0 high/critical |
| **pytest** | 543 test cases | 100% pass rate |

## 📌 开发注意事项

### 配置文件
- `somn/config/local_config.yaml` 是模板，**不含真实密钥**
- 敏感信息使用环境变量或 `.env` 文件
- `.env` 文件已被 `.gitignore` 忽略

### Python 版本
- 目标版本: **Python 3.11+**
- CI 使用 **Python 3.13**
- 请确保代码兼容 Python 3.11+

### 代码风格
- 缩进: **4 空格**
- 行长度: **120 字符**
- 引号: 字符串用 **双引号**，Docstring 用 **三双引号**
- 导入顺序: stdlib → third-party → local（使用 isort）

## 🐛 报告 Bug

请使用 [Bug Report Issue 模板](https://github.com/marcwadehan-png/somn-agent/issues/new?template=bug_report.yml) 提交，包含：
1. 复现步骤（必须）
2. 期望行为 vs 实际行为
3. Somn 版本 + Python 版本 + 操作系统
4. 相关日志/错误输出

## 💡 功能建议

请使用 [Feature Request 模板](https://github.com/marcwadehan-png/somn-agent/issues/new?template=feature_request.yml) 提交，说明：
1. 功能描述和使用场景
2. 为什么需要这个功能
3. 如果你有实现思路也可以分享

## 📜 License

贡献代码即表示你同意你的贡献将在 **AGPL v3 License** 下发布。
