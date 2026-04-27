# Somn自动化代码质量检查系统 v1.0

## 概述

本系统集成pylint、flake8、radon、bandit等工具，实现代码质量自动化检查与复杂度阈值控制。

## 已集成的工具

| 工具 | 用途 | 配置文件 |
|------|------|----------|
| pylint | Python代码分析/检查 | pyproject.toml [pylint.master] |
| flake8 | PEP8风格检查 | .flake8 / pyproject.toml |
| radon | 代码复杂度指标 | pyproject.toml [tool.radon] |
| bandit | 安全漏洞检查 | pyproject.toml [tool.bandit] |
| black | 代码格式化 | pyproject.toml [tool.black] |
| isort | import排序 | pyproject.toml [tool.isort] |
| mypy | 静态类型检查 | pyproject.toml [tool.mypy] |

## 复杂度阈值配置

### 函数级阈值
| 指标 | 阈值 | 说明 |
|------|------|------|
| 圈复杂度 (McCabe CC) | 15 | 核心阈值，超过必须重构 |
| 参数个数 | 8 | 超过使用字典封装 |
| 局部变量 | 20 | 超过拆分子函数 |
| 语句数 | 60 | 超过拆分为多个函数 |
| 分支数 | 15 | if/elif/else/while/for |

### 类级阈值
| 指标 | 阈值 |
|------|------|
| 属性数 | 12 |
| 公开方法 | 25 |
| 父类继承深度 | 7 |

### 行长度
| 指标 | 阈值 |
|------|------|
| 最大行长度 | 120字符 |

## 快速使用

### 方式1: Makefile (推荐)

```bash
cd smart_office_assistant

# 安装依赖
make install-deps

# 完整代码质量检查
make quality

# 单独运行各检查
make lint-pylint
make lint-flake8
make lint-complexity
make lint-security
```

### 方式2: Python脚本

```bash
cd {项目根}

# 安装依赖
pip install -r requirements-dev.txt

# 运行检查
python scripts/code_quality_check.py

# 指定目录和阈值
python scripts/code_quality_check.py --target src/core --threshold 10
```

### 方式3: 直接命令

```bash
# pylint
pylint src/ --max-complexity=15 --jobs=4

# flake8
flake8 src/ --max-line-length=120

# radon复杂度
radon cc -a -n 15 src/

# bandit安全
bandit -r src/
```

## 输出示例

```
============================================================
Somn 代码质量检查报告
============================================================
时间: 2026-04-23 16:00:00
目标: smart_office_assistant/src

配置:
  - 最大圈复杂度: 15
  - 最大行长度: 120
  - 最大参数数: 8

检查结果摘要:
  • Your code has been rated at 8.5/10
  • Flake8: 23 issues
  • 高复杂度函数: 12 个
```

## CI/CD集成建议

### GitLab CI (.gitlab-ci.yml)
```yaml
code-quality:
  stage: test
  script:
    - pip install -r requirements-dev.txt
    - python scripts/code_quality_check.py
  only:
    - merge_requests
    - main
```

### GitHub Actions (.github/workflows/quality.yml)
```yaml
name: Code Quality
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements-dev.txt
      - name: Run quality check
        run: python scripts/code_quality_check.py
```

### Pre-commit Hook (推荐)

创建 `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
        args: [--line-length=120]

  - repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/pylint
    rev: v3.0.3
    hooks:
      - id: pylint
        args: [--max-complexity=15]
```

## 复杂度超标处理流程

1. **发现阶段**: pylint/radon报告超标函数
2. **评估阶段**: 确认复杂度值，分析重构必要性
3. **重构阶段**:
   - CC 15-20: 局部重构
   - CC 21-30: 拆分为多个函数
   - CC 31+: 架构级重构
4. **验证阶段**: 重新运行检查确认通过

## 文件清单

```
.
├── requirements-dev.txt          # 开发依赖 (新增)
├── pyproject.toml                # pylint/flake8配置 (新增)
├── .flake8                        # flake8 IDE集成 (新增)
└── scripts/
    └── code_quality_check.py    # 自动化检查脚本 (新增)

smart_office_assistant/
├── Makefile                      # 已更新 (新增lint目标)
└── file/系统文件/
    └── Somn_代码复杂度阈值规范.md  # 复杂度规范文档 (新增)
```

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-04-23 | 初始版本，集成pylint/flake8/radon/bandit |

---
最后更新: 2026-04-23
