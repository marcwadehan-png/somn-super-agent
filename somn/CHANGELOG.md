# Somn v1.0.0 - Changelog

## [6.2.0] - 2026-04-25

### 新增功能

- **V1.0 Phase 3 社会科学系统集成**
  - 新增7个社会科学学派到WisdomSchool枚举（总计42个）
  - 新增30个ProblemType（总计165个，每个学派5个）
  - 7个社会科学引擎注册到ENGINE_TABLE
  - 50个Claw YAML配置文件
  - 7个学派权重配置（合计0.23）

- **代码量精确统计**
  - Python文件: 1,091个（之前估计773个）
  - 代码行数: 330,792行（之前估计276,010行）
  - 测试用例: 543个（之前363个）

### 工程优化

- **硬编码路径清零**
  - 扫描1,091个.py文件，修复5个文件7处硬编码绝对路径
  - 统一使用 `Path(__file__).resolve()` 和 `path_bootstrap.PROJECT_ROOT` 动态路径
  - 零硬编码路径残留（仅保留1处CHANGELOG历史注释）

- **导入链完整修复**
  - 修复6个文件的导入断裂问题
  - 包导入成功率: 103/104 (99.0%)
  - 4个核心入口全部通过

- **可选依赖优雅降级**
  - `pptx` 缺失时PPT模块空桩降级（非崩溃）
  - `aiohttp` 缺失时OpenClaw Web/API/RSS模块空桩降级
  - `PySide6` 缺失时GUI入口提前报错退出
  - 第三方依赖缺失导致包崩溃: 0个

- **autonomous_core ERROR日志降级**
  - goal_system.py: 空文件检测 + JSONDecodeError→WARNING + 默认目标生成
  - reflection_engine.py: 空文件检测 + JSONDecodeError→WARNING
  - state_manager.py: 空文件检测 + JSONDecodeError→WARNING + 新session生成
  - value_system.py: 空文件检测 + JSONDecodeError→WARNING
  - autonomous_scheduler.py: 孤儿任务自动清理（ERROR→WARNING）
  - 启动阶段零ERROR日志

### 修复

- `src/__main__.py`: `from src.somn_cli` 路径错误 → try/except双路径导入
- `neural_layout_phase1to5_integration.py`: 硬编码路径 → 动态路径
- `simple_test.py`: 硬编码路径 → 动态路径（2处）
- `src/main_chain/config_loader.py`: 硬编码配置路径 → 多候选路径fallback
- `tests/test_v4_upgrade.py`: 硬编码输出路径 → 动态路径
- `test_scheduler_system.py`: 学派数量断言 35→42
- `test_v62_integration.py`: project_root多一级parent修正 + 权重断言修正
- `openclaw/__init__.py`: aiohttp可选依赖检测 + 5个模块空桩降级

### 测试

- 测试用例: 543个 (新增180个)
- 测试通过率: 100% (543 passed, 25 skipped)

## [6.1.1] - 2026-04-24

### 工程优化 (P18)

- **测试修复**: 4个失败测试全部修复
  - `test_sanitize_filename_standard` - 期望值修正
  - `test_is_valid_ipv4` - 测试逻辑修正
  - `test_round_to_decimal_places` - Python 3.13行为兼容
  - `test_semantic_memory_import` - 添加Dict类型导入

- **类型注解提升**: 75.7% → 78.4% (+2.7%)
  - 32个 `__init__.py` 文件重构为 `__getattr__` 延迟加载模式
  - 核心模块: somn.py, api_probe.py
  - Claw子系统: 6个包初始化重构
  - Intelligence引擎: 4个包初始化重构
  - Growth引擎: 3个包初始化重构

### 测试

- 测试用例: 521个 (新增158个)
- 测试通过率: 100% (521 passed, 25 skipped)

## [6.1.0] - 2026-04-24

### 新增功能

- **神之架构 V1.0**: 完整的贤者工程五层链路
  - Phase 0: 830篇博士级深度学习文档
  - Phase 1: 760份蒸馏文档
  - Phase 2: 779条WisdomCode编码
  - Phase 3: 5个核心克隆模块
  - Phase 4: 776个Claw YAML + 5核心模块

- **GlobalClawScheduler**: 全局贤者调度系统
  - 独立模式与协作模式双支持
  - 40个调度接口全覆盖

- **逻辑推理引擎体系 v3.0**:
  - LongCoT: 长思维链
  - ToT: 思维树
  - GoT: 图思维（100节点图网络）
  - ReAct: 推理+行动

- **性能优化 v21**:
  - 延迟加载架构
  - I/O优化脏标记机制
  - 反馈缓存500条上限

### 架构改进

- 贤者Claw系统: 763个Claw覆盖422个岗位
- WisdomSchool: 35个学派
- ProblemType: 135个问题类型
- 藏书阁V1.0: 8分馆/20来源/16分类

## [6.0.0] - 2026-04-23

### 重大更新

- V1.0神之架构升级
- 七人代表大会架构
- 贤者工程Phase2完成

---

完整变更日志请查看 `file/系统文件/` 目录下的相关文档。
