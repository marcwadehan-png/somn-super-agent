# Somn 开发者指南 v6.1

## 开发环境设置

### 1. 克隆与安装

```bash
git clone <repo>
cd somn
pip install -e .           # 开发模式
pip install -r requirements-dev.txt  # 开发工具
```

### 2. 代码格式化

```bash
# 自动格式化
black smart_office_assistant/
isort smart_office_assistant/

# 检查
flake8 smart_office_assistant/
pydocstyle smart_office_assistant/
```

### 3. 类型检查

```bash
mypy smart_office_assistant/
```

### 4. 运行测试

```bash
# 所有测试
pytest tests/ -v

# 特定模块
pytest tests/test_reasoning_engine.py -v

# 带覆盖率
pytest tests/ --cov=smart_office_assistant
```

## 代码规范

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 类 | CamelCase | `AgentCore`, `WisdomDispatcher` |
| 函数 | snake_case | `analyze_problem`, `get_wisdom` |
| 常量 | UPPER_SNAKE | `MAX_DEPTH`, `TIMEOUT_MS` |
| 私有 | 前缀 `_` | `_internal_method` |
| 保护 | 前缀 `_` | `_protected_attr` |

### Docstring格式

```python
def function_name(param: type) -> return_type:
    """
    简短描述。

    详细描述（如果需要）。

    Args:
        param: 参数描述

    Returns:
        返回值描述

    Raises:
        ExceptionType: 异常描述

    Example:
        >>> result = function_name(value)
    """
```

### 类型注解

所有公共函数必须包含类型注解：

```python
# 正确
def process(data: dict, timeout: int = 30) -> Result:
    ...

# 错误
def process(data, timeout=30):
    ...
```

## 项目结构

```
smart_office_assistant/
├── src/
│   ├── core/              # 核心组件
│   │   ├── agent_core.py
│   │   ├── somn_core.py
│   │   └── timeout_guard.py
│   ├── intelligence/      # 智能系统
│   │   ├── wisdom_dispatch/
│   │   └── reasoning/
│   ├── neural_memory/     # 记忆系统
│   ├── claw_subsystem/    # Claw系统
│   └── utils/             # 工具函数
├── tests/                 # 测试
├── config/               # 配置
└── data/                 # 数据
```

## 模块开发

### 创建新模块

1. 在适当目录创建文件
2. 添加 `__init__.py`
3. 编写docstring
4. 添加类型注解
5. 编写测试

```python
# smart_office_assistant/src/new_module.py

"""新模块文档。"""

from typing import Optional

class NewComponent:
    """
    新组件描述。

    Attributes:
        name: 组件名称
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def process(self, data: dict) -> dict:
        """
        处理数据。

        Args:
            data: 输入数据

        Returns:
            处理后的数据
        """
        return {"result": data}
```

### 添加新Claw

1. 在 `claws/` 创建YAML配置
2. 在注册表注册
3. 编写测试

```yaml
# claws/my_claw.yaml
name: my_claw
school: CONFUCIAN
expertise:
  - problem_solving
  - ethics
wisdom_code: CONFUCIUS_MY_001
```

### 添加新WisdomSchool

1. 创建引擎文件
2. 更新调度映射
3. 添加测试

## 测试规范

### 测试文件命名

```
tests/
├── test_module_name.py      # 模块测试
├── test_integration_*.py    # 集成测试
├── test_boundary_*.py       # 边界测试
└── conftest.py              # 共享fixture
```

### 测试结构

```python
import pytest
from smart_office_assistant import Something

class TestSomething:
    """Something类的测试。"""

    def setup_method(self):
        """每个测试前的设置。"""
        self.instance = Something()

    def test_basic(self):
        """基本功能测试。"""
        result = self.instance.process("input")
        assert result.output == "expected"

    def test_edge_case(self):
        """边界情况测试。"""
        with pytest.raises(ValueError):
            self.instance.process("")
```

### Mock使用

```python
from unittest.mock import Mock, patch

def test_with_mock():
    mock_model = Mock()
    mock_model.predict.return_value = "result"

    with patch('module.ModelClass', return_value=mock_model):
        result = function_under_test()
        assert result == "result"
```

## 提交规范

### Git提交信息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type**:
- `feat`: 新功能
- `fix`: 错误修复
- `docs`: 文档更新
- `test`: 测试更新
- `refactor`: 重构
- `perf`: 性能优化

**示例**:
```
feat(wisdom): 添加新的兵家引擎

添加用于军事战略分析的兵家WisdomSchool引擎。
支持阵型分析和战术评估。

Closes #123
```

### 提交前检查

```bash
# 代码格式
black --check smart_office_assistant/

# 导入排序
isort --check-only smart_office_assistant/

# Lint
flake8 smart_office_assistant/ --max-line-length=100

# 类型检查
mypy smart_office_assistant/

# 测试
pytest tests/ -v

# 安全扫描
bandit -r smart_office_assistant/
```

## 性能优化

### 常见优化点

1. **延迟加载**: 使用 `__getattr__` 避免启动时加载
2. **缓存**: 适当使用 `@lru_cache`
3. **批处理**: 批量操作减少开销
4. **流式处理**: 大数据用生成器

### 性能测试

```python
import time

def benchmark():
    start = time.time()
    result = expensive_operation()
    elapsed = time.time() - start
    print(f"Elapsed: {elapsed:.3f}s")
    return result
```

## 调试技巧

### 使用日志

```python
import logging

logger = logging.getLogger(__name__)

def debug_function(data):
    logger.debug(f"Input: {data}")
    result = process(data)
    logger.debug(f"Output: {result}")
    return result
```

### 断点调试

```python
# VS Code launch.json
{
    "name": "Python: Current File",
    "type": "python",
    "request": "launch",
    "program": "${file}",
    "cwd": "${workspaceFolder}"
}
```

### pytest调试

```bash
# 在失败时停下来
pytest tests/ -x

# 显示局部变量
pytest tests/ -l

# 停在第一个失败
pytest tests/ --pdb
```

## 文档贡献

### 更新文档

1. 编辑对应的 `.rst` 文件
2. 更新 `conf.py` 如需
3. 构建测试

```bash
cd docs
sphinx-build -b html source build
```

### 添加ADR

在 `docs/adr/` 创建新文件：

```markdown
# ADR-XXX: Title

## Status
Proposed

## Context
...

## Decision
...

## Consequences
...
```

## 获取帮助

- 查看 [架构文档](architecture.rst)
- 查看 [API文档](api/index.rst)
- 查看现有 [ADRs](adr/)
- 查看 [测试示例](tests/)

---

*最后更新: 2026-04-24*