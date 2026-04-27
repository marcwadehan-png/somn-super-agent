# Somn代码复杂度阈值规范 v1.0

## 概述

本文档定义Somn项目中代码复杂度阈值，用于自动化代码质量检查。

## McCabe圈复杂度阈值

| 指标 | 阈值 | 说明 | 优先级 |
|------|------|------|--------|
| 函数/方法复杂度 | 15 | 超过15需重构 | P1 |
| 模块复杂度 | 30 | 模块内所有函数复杂度之和 | P2 |
| 类复杂度 | 20 | 类的加权复杂度 | P2 |

## 代码度量阈值

### 函数级
| 指标 | 阈值 | 说明 |
|------|------|------|
| 参数个数 (max-args) | 8 | 超过需使用字典/对象封装 |
| 局部变量 (max-locals) | 20 | 超过需拆分为子函数 |
| 返回点 (max-returns) | 6 | 超过需重构 |
| 语句数 (max-statements) | 60 | 超过需拆分 |
| 分支数 (max-branches) | 15 | if/elif/else/while/for分支 |

### 类级
| 指标 | 阈值 | 说明 |
|------|------|------|
| 属性数 (max-attributes) | 12 | 超过需拆分 |
| 公开方法 (max-public-methods) | 25 | 超过需拆分 |
| 父类继承 (max-parents) | 7 | 多继承深度 |

### 模块级
| 指标 | 阈值 | 说明 |
|------|------|------|
| import数量 | 30 | 超过需拆分模块 |
| 类数量 | 20 | 单文件类数量 |
| 函数数量 | 30 | 单文件函数数量 |
| 总代码行 | 500 | 超过需拆分 |

## 复杂度计算公式

### McCabe圈复杂度
```
CC = 1 + (决策点数)
决策点 = if + elif + else + for + while + except + with + assert + conditional expr
```

### 加权复杂度 (类)
```
CW = sum(方法CC) + 属性复杂度
```

### 模块复杂度
```
MC = sum(函数CC) + 耦合惩罚
耦合惩罚 = import数量 * 0.5
```

## 重构策略

| 复杂度范围 | 建议 |
|-----------|------|
| 1-10 | 简单，理想状态 |
| 11-15 | 可接受，需关注 |
| 16-20 | 需要重构 |
| 21-30 | 必须重构 |
| 31+ | 紧急重构 |

## 快速检查命令

```bash
# pylint 复杂度检查
pylint --max-complexity=15 smart_office_assistant/src

# radon 复杂度报告
radon cc -a -s smart_office_assistant/src

# 查找高复杂度函数
radon cc -a -n 15 smart_office_assistant/src

# 代码健康趋势
wily report smart_office_assistant/src
```

## CI/CD集成

在GitLab CI / GitHub Actions中使用:

```yaml
lint:
  script:
    - pip install -r requirements-dev.txt
    - pylint --max-complexity=15 src/
    - flake8 src/
    - radon cc -a -n 15 src/
```

---
最后更新: 2026-04-23
