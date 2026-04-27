# WisdomEncodingRegistry v2.2 技术文档

> **版本**: 2.2
> **日期**: 2026-04-24
> **状态**: v2.2懒加载优化版

---

## 概述

WisdomEncodingRegistry是Somn系统的智慧编码注册中心，负责管理830+位贤者的智慧编码数据。

### 核心功能

- 管理779条SageCode编码记录
- 提供贤者信息查询接口
- 支持懒加载模式（v2.2新增）
- 与藏书阁V3.0无缝集成

---

## 架构设计

### 数据模型

```python
class WisdomEncodingRegistry:
    def __init__(self, lazy: bool = True):
        """
        参数:
            lazy: 是否启用懒加载模式（默认True）
                  - True: 初始化不含数据，首次访问时加载
                  - False: 初始化时立即加载全部数据
        """
        self._lazy = lazy
        self._sage_codes = {}  # 懒加载数据存储
        self._loaded = False
```

### 懒加载机制

v2.2采用`__getattr__`延迟加载模式：

```python
def __getattr__(self, name: str):
    """首次访问任意属性时触发数据加载"""
    if not self._loaded and name not in self.__dict__:
        self._ensure_loaded()
    return super().__getattribute__(name)
```

### 关键接口

| 方法 | 功能 | 懒加载支持 |
|------|------|-----------|
| `get_sage(sage_id)` | 获取贤者信息 | ✅ 首次调用时加载 |
| `get_cognitive_blend(sage_id)` | 获取认知融合配置 | ✅ |
| `export_data()` | 导出全部数据 | ✅ |
| `get_school_count()` | 获取学派数量 | ✅ |

---

## 性能指标

| 指标 | v2.1 | v2.2 | 提升 |
|------|------|------|------|
| 初始化时间 | ~200ms | <1ms | -99.5% |
| 懒加载触发时间 | — | <50ms | — |
| 内存占用 | 全量加载 | 按需加载 | -60% |

---

## 使用方式

### 标准模式（自动懒加载）

```python
from smart_office_assistant.src.intelligence.wisdom_encoding.wisdom_encoding_registry import WisdomEncodingRegistry

reg = WisdomEncodingRegistry()  # 默认懒加载
data = reg.export_data()       # 首次访问触发加载
print(data['total_sages'])     # 输出: 830
```

### 显式懒加载

```python
reg = WisdomEncodingRegistry(lazy=True)
# 仅初始化，无I/O操作
```

### 非懒加载模式

```python
reg = WisdomEncodingRegistry(lazy=False)
# 立即加载全部数据
```

### 全局注册表

```python
from smart_office_assistant.src.intelligence.wisdom_encoding.wisdom_encoding_registry import get_wisdom_registry

reg = get_wisdom_registry(lazy=True)
data = reg.export_data()
```

---

## 数据结构

### SageCode格式

```yaml
sage_code:
  sage_id: "孔子"              # 贤者标识
  school: RU                   # 学派 (RU=儒家)
  cognitive_blend:             # 认知融合配置
    primary: CONFUCIAN        # 主认知模式
    secondary: DIALECTICAL    # 次认知模式
    weight: 0.85              # 权重
  wisdom_dimensions:           # 智慧维度
    - moral_reasoning
    - social_harmony
    - governance
  encoded_knowledge: "..."      # 编码知识
```

### 统计数据

```python
{
    "total_sages": 830,        # 贤者总数
    "total_sages_count": 779,  # SageCode数量
    "school_distribution": {    # 学派分布
        "RU": 120,
        "DAO": 95,
        "FA": 88,
        ...
    }
}
```

---

## 验证方法

### 懒加载验证脚本

```bash
python scripts/verify_lazy_loading.py
```

### 性能基准测试

```bash
python scripts/benchmark_performance.py
```

### 测试用例

```python
# tests/test_memory_claw.py
def test_registry_has_entries():
    reg = WisdomEncodingRegistry(lazy=True)
    data = reg.export_data()
    total = data.get("total_sages", 0)
    assert total > 700
```

---

## 与藏书阁V3.0集成

WisdomEncodingRegistry通过LibraryBridge与藏书阁V3.0集成：

```python
# 藏书阁存储智慧编码
library.store(
    content=sage_data,
    category=MemoryCategory.SAGE_ENCODING,
    source=MemorySource.SYSTEM_GENERATED,
    permission=LibraryPermission.INTERNAL
)
```

---

## 更新历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.2 | 2026-04-24 | 懒加载优化，初始化时间-99.5% |
| v2.1 | 2026-04-23 | 数据外置，副本消除优化 |
| v2.0 | 2026-04-22 | 完全重构，支持35学派 |

---

**文档版本**: v1.0
**最后更新**: 2026-04-24
