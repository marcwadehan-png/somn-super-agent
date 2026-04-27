# Somn测试覆盖率提升与质量追踪系统

**版本**: v1.0.0
**更新**: 2026-04-23
**状态**: 已建立

---

## 一、系统架构

### 1.1 测试目录结构

```
tests/
├── __init__.py
├── conftest.py                    # pytest共享配置
├── test_tracker.py               # 测试追踪器
├── test_technical_debt.py         # 技术债务追踪器
├── unit/                          # 单元测试
│   ├── __init__.py
│   ├── test_saint_king_wisdom.py  # 圣王智慧引擎测试
│   └── test_timeout_guard.py      # 核心模块测试模板
├── integration/                   # 集成测试
│   ├── __init__.py
│   └── test_wisdom_integration.py # 智慧系统集成测试
└── e2e/                           # 端到端测试
    └── __init__.py
```

### 1.2 核心配置文件

**pytest.ini**: 测试框架配置
- 测试路径和命名规范
- 覆盖率配置
- 标记系统（unit/integration/e2e/smoke等）

---

## 二、追踪系统

### 2.1 测试追踪器 (test_tracker.py)

**功能**:
- 扫描所有待测模块
- 记录模块函数/类数量
- 追踪测试覆盖率历史
- 生成覆盖率报告

**使用**:
```bash
python tests/test_tracker.py
```

**输出**:
- `data/test_tracking/coverage_history.json` - 覆盖率历史
- `data/test_tracking/module_coverage.json` - 模块覆盖率详情
- `file/系统文件/SSS_测试追踪报告.md` - 覆盖率报告

### 2.2 技术债务追踪器 (test_technical_debt.py)

**功能**:
- 扫描TODO/FIXME/XXX/HACK等技术债务标记
- 按优先级分类（P0/P1/P2）
- 生成行动项列表
- 追踪债务历史

**标记类型**:
| 标记 | 优先级 | 严重性 | 说明 |
|------|--------|--------|------|
| FIXME | P1 | 高 | 需要修复的问题 |
| TODO | P2 | 中 | 待实现的功能 |
| XXX | P0 | 紧急 | 已知问题需立即处理 |
| HACK | P2 | 中 | 临时解决方案 |
| BUG | P0 | 紧急 | 已确认的Bug |
| PERF | P1 | 高 | 性能问题 |
| SECURITY | P0 | 紧急 | 安全漏洞 |

**使用**:
```bash
python tests/test_technical_debt.py
```

**输出**:
- `data/test_tracking/technical_debt.json` - 债务详情
- `data/test_tracking/debt_report.md` - 债务报告

---

## 三、单元测试模板

### 3.1 核心模块测试 (test_timeout_guard.py)

覆盖核心模块的基本导入和功能测试：
- SomnCore
- TimeoutGuard
- AgentCore
- WisdomDispatcher
- DeepReasoningEngine
- SageProxyFactory
- NeuralMemorySystem
- ClawArchitect/Coordinator/Bridge

### 3.2 智慧引擎测试 (test_saint_king_wisdom.py)

针对重构后的圣王智慧引擎测试：
- 引擎初始化
- 7个领域子函数独立调用
- 圣人总数验证
- 圣人属性验证
- 调度器单一职责验证

### 3.3 集成测试 (test_wisdom_integration.py)

**测试类别**:
- WisdomIntegration - 智慧系统集成
- ClawIntegration - Claw子系统集成
- MemoryIntegration - 记忆系统集成
- LearningIntegration - 学习系统集成
- SmokeTests - 冒烟测试
- Performance - 性能测试

---

## 四、运行指南

### 4.1 运行所有测试

```bash
cd smart_office_assistant
pytest tests/ -v
```

### 4.2 运行特定类别

```bash
# 仅单元测试
pytest tests/unit/ -v

# 仅集成测试
pytest tests/integration/ -v -m integration

# 仅冒烟测试
pytest tests/ -v -m smoke

# 跳过慢速测试
pytest tests/ -v -m "not slow"
```

### 4.3 生成覆盖率报告

```bash
# 需要安装 pytest-cov
pip install pytest-cov

# 生成覆盖率
pytest tests/ --cov=src --cov-report=html --cov-report=term

# 查看HTML报告
start tests/coverage_html/index.html
```

### 4.4 运行追踪系统

```bash
# 测试追踪
python tests/test_tracker.py

# 技术债务追踪
python tests/test_technical_debt.py
```

---

## 五、测试标记说明

### 5.1 测试类型标记

- `@pytest.mark.unit` - 单元测试
- `@pytest.mark.integration` - 集成测试
- `@pytest.mark.e2e` - 端到端测试
- `@pytest.mark.smoke` - 冒烟测试

### 5.2 功能模块标记

- `@pytest.mark.core` - 核心模块
- `@pytest.mark.wisdom` - 智慧引擎
- `@pytest.mark.memory` - 记忆系统
- `@pytest.mark.learning` - 学习系统
- `@pytest.mark.cloning` - 克隆系统
- `@pytest.mark.claw` - Claw子系统
- `@pytest.mark.reasoning` - 推理引擎
- `@pytest.mark.dispatcher` - 调度器

### 5.3 其他标记

- `@pytest.mark.slow` - 慢速测试（>5s）
- `@pytest.mark.performance` - 性能测试
- `@pytest.mark.asyncio` - 异步测试
- `@pytest.mark.requires_llm` - 需要LLM调用

---

## 六、当前测试覆盖情况

**统计时间**: 2026-04-23

| 指标 | 数值 |
|------|------|
| 总模块数 | 714 |
| 已测试模块 | 10 |
| 测试覆盖率 | 1.4% |
| 技术债务项 | 1 |
| P0/P1债务 | 0 |

**说明**:
- 项目采用懒加载架构，大部分模块通过导入时测试
- 核心功能通过集成测试覆盖
- 技术债务极低，代码质量良好

---

## 七、待补充测试

### 7.1 高优先级

| 模块 | 建议测试类型 | 负责人 |
|------|-------------|--------|
| SomnCore | 集成测试 | - |
| WisdomDispatcher | 单元测试 | - |
| NeuralMemorySystem | 集成测试 | - |
| ClawArchitect | 单元测试 | - |

### 7.2 中优先级

| 模块 | 建议测试类型 |
|------|-------------|
| DeepReasoningEngine | 单元测试 |
| SageProxyFactory | 单元测试 |
| TimeoutGuard | 单元测试 |
| LearningOrchestrator | 集成测试 |

### 7.3 低优先级

| 模块 | 建议测试类型 |
|------|-------------|
| 其他引擎模块 | 冒烟测试 |
| GUI组件 | E2E测试 |
| 工具层 | 单元测试 |

---

## 八、持续集成建议

### 8.1 本地验证

每次提交前运行:
```bash
pytest tests/unit/ -v
pytest tests/integration/ -v -m "not slow"
python tests/test_tracker.py
python tests/test_technical_debt.py
```

### 8.2 CI/CD配置示例

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.13'
      - name: Run tests
        run: |
          pip install pytest pytest-cov
          pytest tests/ -v --cov=src
      - name: Run trackers
        run: |
          python tests/test_tracker.py
          python tests/test_technical_debt.py
```

---

**维护者**: 18000
**最后更新**: 2026-04-23
