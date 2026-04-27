# 贡献指南 | Contributing Guide

感谢您对 Somn 项目的关注！本指南将帮助您了解如何为项目做出贡献。

## 行为准则 | Code of Conduct

请阅读 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) 了解我们的社区准则。

## 快速开始 | Getting Started

### 1. Fork 项目

点击 GitHub 页面右上角的 "Fork" 按钮。

### 2. 克隆您的 Fork

```bash
git clone https://github.com/YOUR_USERNAME/somn-agent.git
cd somn-agent
```

### 3. 创建开发分支

```bash
git checkout -b feature/your-feature-name
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 开发依赖
```

## 开发规范 | Development Standards

### 代码风格

项目使用以下工具维护代码质量：

- **pylint** — Python 代码检查
- **flake8** — 代码风格检查
- **black** — 代码格式化
- **isort** — import 排序

运行检查：

```bash
flake8 . --max-line-length=120
pylint smart_office_assistant/ api/
black --check .
isort --check .
```

### 提交规范 | Commit Convention

使用语义化提交信息：

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型 (type)：

- `feat` — 新功能
- `fix` — Bug 修复
- `docs` — 文档更新
- `style` — 代码格式（不影响功能）
- `refactor` — 重构
- `test` — 测试
- `chore` — 构建/工具

### Pull Request 流程 | PR Process

在提交 PR 前，请确认：

- [ ] 代码遵循项目风格（`pylint` / `flake8` 通过）
- [ ] 新增功能包含对应的单元测试
- [ ] 所有现有测试通过（`pytest tests/ -v`）
- [ ] Commit message 符合规范
- [ ] 没有引入新的安全漏洞（`bandit` 通过）
- [ ] 文档已更新（如有 API 变更）

## 项目结构概览

```
├── smart_office_assistant/    # 核心引擎
│   ├── src/core/             # SomnCore 主引擎
│   ├── src/neural_memory/     # 神经记忆系统
│   ├── src/intelligence/      # 智慧调度器
│   └── src/tool_layer/        # LLM 工具层
├── api/                       # FastAPI 后端服务
├── knowledge_cells/           # 知识格子系统
├── scripts/                   # 工具脚本
├── tests/                     # 测试套件
├── Somn-GUI/                  # PyQt6 图形界面
├── docs/                      # 项目文档 (ADR)
└── .github/                   # GitHub Actions
```

## 测试指南

### 运行全部测试

```bash
pytest tests/ -v --tb=short
```

### 按分类运行

```bash
pytest tests/ -k "core"       # 核心引擎测试
pytest tests/ -k "memory"      # 记忆系统测试
pytest tests/ -k "knowledge"   # 知识格子系统测试
pytest tests/ -k "integration" # 集成测试
```

### 覆盖率报告

```bash
pytest tests/ --cov=smart_office_assistant --cov-report=html
```

## 文档 | Documentation

项目文档位于 `docs/` 目录，使用 Sphinx 构建。

```bash
cd docs
make html
```

## 许可证 | License

通过提交代码，您同意您的贡献将按照 [AGPL v3](LICENSE) 许可证发布。

## 联系我们 | Contact

- 邮箱：marcwadehan@gmail.com
- GitHub Issues：https://github.com/marcwadehan-png/somn-agent/issues

---

感谢您的贡献！
