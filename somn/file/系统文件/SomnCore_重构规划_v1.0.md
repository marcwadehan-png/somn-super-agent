# SomnCore 重构规划文档 v1.0

## 目标
将 `somn_core.py` (5145行) 重构为多个独立模块，最终收敛 SomnCore 主类仅保留：
- 核心生命周期管理（init / 预热 / 懒加载入口）
- 6个对外核心接口（`run_agent_task` / `analyze_requirement` / `design_strategy` / `execute_workflow` / `evaluate_results` / `get_system_status`）
- 各子模块的委托调用入口（薄层）

## 提取原则
1. **工具函数 / 常量 / TF-IDF / 类型** → 最低风险，最先提取
2. **智慧层初始化** → 中等风险，依赖注入点收敛
3. **策略设计逻辑** → 独立函数，无外部状态依赖
4. **工作流执行逻辑** → 状态机与任务调度
5. **评估 / ROI / 反馈 / 学习** → 最多辅助方法集中
6. **收敛主类** → 最后清理导入引用

## 模块拆分方案

### Phase 1: 工具层（风险：极低）
| 提取内容 | 目标文件 | 说明 |
|---|---|---|
| `PurePythonTfidfIndex` + `_ensure_experience_index` | `_somn_tfidf.py` | TF-IDF 索引逻辑，无外部依赖 |
| `SomnContext` / `WorkflowTaskRecord` / `LongTermGoalRecord` | `_somn_types.py` | 数据类定义 |
| 所有 `@staticmethod` / 纯函数工具 + 搜索缓存 + LLM缓存 | `_somn_utils.py` | 辅助函数大杂烩 |
| 类级静态常量（熔断器 / 缓存配置 / 超时配置） | `_somn_constants.py` | 纯常量，可直接迁移 |

### Phase 2: 智慧层初始化与分析（风险：中等）
| 提取内容 | 目标文件 | 说明 |
|---|---|---|
| `_init_main_chain_integration` | `_somn_wisdom_init.py` | 主线集成器初始化 |
| `_init_learning_coordinator` | `_somn_wisdom_init.py` | 学习协调器初始化 |
| `_init_autonomous_agent` | `_somn_wisdom_init.py` | 自主智能体初始化 |
| `_init_cloud_learning_system` + 3个子模块 | `_somn_wisdom_init.py` | 云端学习体系初始化 |
| `_run_wisdom_analysis` | `_somn_wisdom_analysis.py` | 智慧分析主链 |
| `_run_unified_enhancement` | `_somn_wisdom_analysis.py` | 统一协调器增强 |

### Phase 3: 策略设计（风险：低）
| 提取内容 | 目标文件 | 说明 |
|---|---|---|
| `_build_strategy_learning_guidance` | `_somn_strategy_design.py` | RL/ROI 引导 |
| `_build_workflow_reference_base` | `_somn_strategy_design.py` | 工作流基准 |
| `_build_candidate_strategies` | `_somn_strategy_design.py` | 候选集构建 |
| `_rank_strategy_candidates` | `_somn_strategy_design.py` | 候选排序 |
| `_generate_structured_strategy` | `_somn_strategy_design.py` | 结构化策略生成 |

### Phase 4: 工作流执行（风险：中等）
| 提取内容 | 目标文件 | 说明 |
|---|---|---|
| `_parse_execution_tasks` | `_somn_workflow_execution.py` | 任务解析 |
| `_build_fallback_execution_tasks` | `_somn_workflow_execution.py` | fallback任务 |
| `_build_task_records` | `_somn_workflow_execution.py` | 任务记录构建 |
| `_evaluate_dependency_state` | `_somn_workflow_execution.py` | 依赖评估 |
| `_transition_task_state` | `_somn_workflow_execution.py` | 状态转移 |
| `_serialize_task_record` | `_somn_workflow_execution.py` | 记录序列化 |
| `_execute_task` | `_somn_workflow_execution.py` | 单任务执行 |
| `_execute_rollback` | `_somn_workflow_execution.py` | 回滚执行 |
| `_extract_strategy_combo` | `_somn_workflow_execution.py` | 策略组合提取 |
| `_resolve_reinforcement_action` | `_somn_workflow_execution.py` | 动作映射 |

### Phase 5: 评估 / ROI / 反馈 / 学习（风险：中等）
| 提取内容 | 目标文件 | 说明 |
|---|---|---|
| `_get_feedback_pipeline` | `_somn_feedback.py` | 反馈管道 getter |
| `_get_reinforcement_trigger` | `_somn_feedback.py` | 强化触发器 getter |
| `_get_roi_tracker` | `_somn_feedback.py` | ROI 追踪器 getter |
| `_build_fallback_evaluation` | `_somn_evaluation.py` | 兜底评估 |
| `_build_roi_signal_snapshot` | `_somn_evaluation.py` | ROI 信号快照 |
| `_estimate_task_quality_score` | `_somn_evaluation.py` | 任务质量估算 |
| `_score_to_rating_value` | `_somn_evaluation.py` | 分值→评分转换 |
| `_task_outcome_anchor` | `_somn_evaluation.py` | 任务状态锚点 |
| `_normalize_roi_ratio` / `_roi_trend_bias` | `_somn_evaluation.py` | ROI 辅助 |
| `_track_roi_task_start` / `_track_roi_task_completion` | `_somn_evaluation.py` | ROI 追踪 |
| `_track_roi_workflow_completion` | `_somn_evaluation.py` | 工作流ROI聚合 |
| `_clamp_unit_score` | `_somn_evaluation.py` | 分值钳制 |
| `_build_workflow_feedback_entries` | `_somn_feedback.py` | 反馈条目构建 |
| `_build_evaluation_feedback_entries` | `_somn_feedback.py` | 评估反馈条目 |
| `_apply_reinforcement_inputs` | `_somn_feedback.py` | 强化学习写入 |
| `_submit_feedback_entries` | `_somn_feedback.py` | 反馈提交 |
| `_record_learning_feedback` | `_somn_feedback.py` | 学习反馈记录 |
| `_record_evaluation_learning_feedback` | `_somn_feedback.py` | 评估反馈记录 |
| `_record_workflow_feedback` | `_somn_feedback.py` | 工作流反馈记录 |
| `_record_validation_learning` | `_somn_feedback.py` | 验证学习记录 |
| `_serialize_feedback_item` | `_somn_feedback.py` | 反馈序列化 |
| `_serialize_reinforcement_updates` | `_somn_feedback.py` | 强化更新序列化 |

### Phase 6: 主类收敛
最终 `somn_core.py` 保留：
- `__init__`（Tier0 零阻塞初始化）
- `_background_warmup`
- 所有 `_ensure_*` 方法（懒加载入口，仅调用 `engine_self` 属性的薄层）
- `run_agent_task`（主链入口，含4条路由分支）
- `_run_orchestrator_route` / `_run_local_llm_route` / `_run_wisdom_route`
- `analyze_requirement`（并行分析主链）
- `design_strategy`（策略设计主链）
- `execute_workflow`（工作流执行主链）
- `evaluate_results`（评估主链）
- `get_system_status` / `run_daily_learning`
- `record_user_feedback`（对外反馈接口）
- 所有 `self.` 属性访问的委托调用
- `get_somn_core` 单例函数

## 验证计划
1. 每个 Phase 完成后运行 `python -m pytest tests/test_deep_reasoning_engine.py -v`（回归验证）
2. 检查 `from src.core.somn_core import SomnCore` 导入正常
3. 检查所有 `from ._somn_* import` 导入正常
4. 最终运行冒烟测试验证主链可执行

## 风险控制
- **Phase 1 最先做**：常量/工具类提取零业务风险
- **Phase 2-3 最后做主类修改**：先确认子模块可独立导入
- **每次替换后立即测试**：不堆积多步修改
- **保留旧文件备份**：直到全部验证通过再清理
