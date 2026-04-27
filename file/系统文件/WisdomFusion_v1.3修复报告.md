# WisdomFusion v1.3/v1.4 修复报告

## 修复概述

| 项目 | v1.3 | v1.4 |
|------|------|------|
| 日期 | 2026-04-24 19:32 | 2026-04-24 19:45 |
| 问题 | `__all__` 列表声明错误 | 循环导入问题 |
| 修复文件 | `wisdom_fusion/__init__.py` | `wisdom_fusion/__init__.py` |

## v1.3 修复：__all__ 列表声明错误

### 原始代码

```python
__all__ = [
    'fuse_wisdom',
    'get_fusion_insights',
    'get_wisdom_fusion_core',
]
```

### 问题

`fuse_wisdom` 和 `get_fusion_insights` 是 `WisdomFusionCore` 类的方法，而不是模块级函数。

## v1.4 修复：循环导入问题

### 问题链

```
wisdom_fusion_core.py → wisdom_fusion/__init__.py
     ↑                              ↓
     └──── _fusion_core_init ← (过早导入)
                              ↓
                    reasoning/deep_reasoning_engine
                              ↓
                           loguru → ctypes (循环)
```

### 修复方案

将 `_fusion_core_init` 和 `_fusion_core_execute` 的导入从模块级移到 `WisdomFusionCore.__init__` 方法内部（延迟导入）。

### 修复后代码

```python
class WisdomFusionCore:
    def __init__(self, config=None):
        # 延迟导入避免循环依赖
        from . import _fusion_core_init as _init_mod
        from . import _fusion_core_execute as _exec_mod

        self._config = config
        self.config = None
        self.wisdom_modules = {}
        self.conflict_resolver = None
        self.fusion_history = []
        self.performance_log = []
        self.fusion_cache = {}
        _init_mod.fusion_core_init(self)
```

## 验证

```bash
pytest tests/ -q
# 353 passed, 10 skipped
```
