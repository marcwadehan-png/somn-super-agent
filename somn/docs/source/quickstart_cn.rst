# Somn 快速开始指南 v6.1

## 环境要求

- Python 3.10+
- Windows/Linux/macOS
- 4GB RAM (推荐8GB)
- 2GB磁盘空间

## 安装步骤

### 1. 克隆项目

```bash
git clone <repository-url>
cd somn
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. 配置

复制配置文件：

```bash
cp config/config.example.yaml config/config.yaml
```

编辑 `config/config.yaml`：

```yaml
model:
  provider: "local"
  model_path: "path/to/your/model"

memory:
  data_dir: "data/"
  max_size_gb: 10

wisdom:
  schools_path: "smart_office_assistant/claws/"
```

### 4. 验证安装

```bash
# 运行测试
pytest tests/ -v

# 验证导入
python -c "from smart_office_assistant import Somn; print('OK')"
```

## 基本使用

### 初始化Somn

```python
from smart_office_assistant import Somn

# 创建实例
somn = Somn()

# 初始化
await somn.initialize()
```

### 分析问题

```python
# 分析问题
result = await somn.analyze(
    "如何优化团队效率？"
)

print(result.solution)
print(f"置信度: {result.confidence}")
```

### 获取推荐

```python
# 获取基于智慧的推荐
recommendations = await somn.get_recommendations(
    context={"task": "项目规划"},
    max_results=5
)

for rec in recommendations:
    print(f"- {rec.text}")
```

### 推理引擎选择

```python
# 使用特定推理引擎
result = await somn.analyze(
    "复杂的多步骤问题",
    reasoning_engine="GoT"  # 可选: LongCoT, ToT, GoT, ReAct
)
```

### 批量处理

```python
# 批量处理任务
tasks = ["任务1", "任务2", "任务3"]
results = await somn.batch_process(tasks)

for task, result in zip(tasks, results):
    print(f"{task}: {result.status}")
```

## 常用配置示例

### 最小配置

```yaml
model:
  provider: "local"
  model_path: "./models/llama-3b"

memory:
  data_dir: "./data"
  max_size_gb: 5
```

### 双模型配置

```yaml
model:
  primary:
    name: "llama-3.2-1b"
    path: "./models/llama"
  secondary:
    name: "gemma4"
    path: "./models/gemma"
  fallback_enabled: true
```

## 项目结构

```
somn/
├── smart_office_assistant/  # 主包
│   └── src/
│       ├── core/           # 核心组件
│       ├── intelligence/    # 智能系统
│       ├── neural_memory/   # 记忆系统
│       ├── claw_subsystem/  # Claw子系统
│       └── ...
├── config/                  # 配置文件
├── data/                    # 数据目录
├── docs/                    # 文档
├── tests/                   # 测试用例
└── models/                  # 模型文件
```

## 调试技巧

### 查看日志

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 测试特定模块

```bash
pytest tests/test_reasoning_engine.py -v
```

### 检查配置

```python
from smart_office_assistant.config import load_config
config = load_config("config/config.yaml")
print(config)
```

## 下一步

- 阅读 [架构文档](docs/source/architecture.rst)
- 探索 [API参考](docs/source/api/index.rst)
- 查看 [开发者指南](docs/source/contributing.rst)

## 常见问题

### 导入错误

确保在项目根目录运行，或设置 PYTHONPATH：

```bash
export PYTHONPATH=.
python your_script.py
```

### 模型未找到

检查 config.yaml 中的 model_path 是否正确。

### 内存错误

增加 config.yaml 中的 max_size_gb 或清理旧数据。

---

*版本: 6.1.0 | 更新: 2026-04-24*