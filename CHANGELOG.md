# Changelog

All notable changes to the Somn project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v1.0.0.html).

## [Unreleased]

### To Be Announced
- GitHub 开源发布 (v6.2.0)
- Docker 镜像构建
- 官方文档站点 (GitHub Pages)

---

## [6.2.0] - 2026-04-27

### Added (新增功能)
- **V6.2 神之架构升级**
  - 422 个岗位体系 (+45)
  - 763 个贤者 Claw
  - 42 个学派 (+7)
  - 165 个问题类型 (+30)
- **600贤者蒸馏工程文档**
  - 16卷完整蒸馏文档 (第1-16卷)
  - 涵盖史学/儒家/道家/佛学/法家/兵家/科学等
- **开源配置文件完善**
  - `.editorconfig` - 编辑器编码规范
  - `.gitattributes` - Git 属性配置
  - `.pre-commit-config.yaml` - 预提交钩子
  - `.markdownlint.json` - Markdown 规范
  - `.markdownlinkcheck.json` - 链接检查
- **知识格子系统增强** (`knowledge_cells/`)
  - `reasoning_enhancer.py` — 推理增强器
  - `neural_integration.py` — 神经集成模块
  - CLI 交互界面 (`cli.py`)
  - 完整测试脚本 (`test_system.py`)
- **文档结构重组**
  - 核心架构文档迁移至 `docs/` 目录
  - 蒸馏文档系统化整理
  - README.md 文档导航更新

### Changed (工程优化)
- **LICENSE 变更**: 最终确认为 AGPL v3 License
- **硬编码路径清零**: 扫描 1,091 个 .py 文件，修复 5 文件 7 处硬编码路径
- **导入链完整修复**: 包导入成功率 **99.0%** (103/104)
- **可选依赖优雅降级**: pptx / aiohttp / PySide6 缺失时空桩降级
- **autonomous_core ERROR 日志降级**: 启动阶段零 ERROR

### Testing (测试)
- 测试用例: **543 个** (100% 通过率, 25 跳过)

### Added (新增功能)
- **V1.0 Phase 3 社会科学系统集成**
  - 新增 7 个社会科学学派到 WisdomSchool 枚举（总计 **42 个**）
  - 新增 30 个 ProblemType（总计 **165 个**）
  - 7 个社会科学引擎注册到 ENGINE_TABLE
  - 50 个 Claw YAML 配置文件
- **代码量精确统计**
  - Python 文件: **1,091 个**
  - 代码行数: **330,792 行**
  - 测试用例: **543 个**（+180 新增）
- **知识格子系统增强** (`knowledge_cells/`)
  - `reasoning_engine.py` — 推理增强器
  - `neural_integration.py` — 神经集成模块

### Changed (工程优化)
- **硬编码路径清零**: 扫描 1,091 个 .py 文件，修复 5 文件 7 处硬编码路径
- **导入链完整修复**: 包导入成功率 **99.0%** (103/104)
- **可选依赖优雅降级**: pptx / aiohttp / PySide6 缺失时空桩降级，0 崩溃
- **autonomous_core ERROR 日志降级**: 启动阶段零 ERROR

### Fixed (Bug 修复)
- `src/__main__.py`: 导入路径错误 → try/except 双路径导入
- `neural_layout_phase1to5_integration.py`: 硬编码路径修正
- `simple_test.py`: 2 处动态路径修复
- `test_scheduler_system.py`: 学派数量断言 35→42
- `openclaw/__init__.py`: aiohttp 可选依赖检测 + 5 模块空桩

### Testing (测试)
- 测试用例: **543 个** (100% 通过率, 25 跳过)

---

## [6.1.1] - 2026-04-24

### Changed
- **测试修复**: 4 个失败测试全部修复（期望值/逻辑/兼容性/类型导入）
- **类型注解提升**: 75.7% → **78.4%** (+2.7%)
- **32 个 `__init__.py` 重构**: 延迟加载模式 (`__getattr__`)
- 测试用例: **521 个** (+158 新增, 100% 通过率)

---

## [6.1.0] - 2026-04-24

### Added
- **神之架构 V1.0**: 完整的贤者工程五层链路
  - Phase 0: 830 篇博士级深度学习文档
  - Phase 1: 760 份蒸馏文档
  - Phase 2: 779 条 WisdomCode 编码
  - Phase 3: 5 个核心克隆模块
  - Phase 4: 776 个 Claw YAML + 5 核心模块
- **GlobalClawScheduler**: 全局贤者调度系统（独立/协作双模式, 40 接口）
- **逻辑推理引擎体系 v3.0**: LongCoT / ToT / GoT(100节点) / ReAct
- **性能优化 v21**: 延迟加载架构 / I-O脏标记机制 / 反馈缓存500条上限

### Changed
- 岗位体系: 377岗 + 25爵位 + 七人代表大会
- WisdomSchool: **35 个**学派
- ProblemType: **135 个**问题类型
- 藏书阁 V1.0: 8分馆 / 20来源 / 16分类

---

## [6.0.0] - 2026-04-23

### Added
- **V6 神之架构升级**
- **七人代表大会**架构
- **贤者工程 Phase2 完成**

---

## [5.x] 及更早版本

详见 [somn/CHANGELOG.md](somn/CHANGELOG.md) 获取完整历史记录。

---

## 版本说明

| 类型 | 说明 |
|------|------|
| **Added** | 新功能、新特性 |
| **Changed** | 对现有功能的变更 |
| **Deprecated** | 即将移除的功能 |
| **Removed** | 已移除的功能 |
| **Fixed** | Bug 修复 |
| **Security** | 安全相关修复 |

## 链接

- [GitHub Releases](https://github.com/marcwadehan-png/somn-agent/releases)
- [Issue Tracker](https://github.com/marcwadehan-png/somn-agent/issues)
- [Project Status](somn/PROJECT_STATUS.md)
