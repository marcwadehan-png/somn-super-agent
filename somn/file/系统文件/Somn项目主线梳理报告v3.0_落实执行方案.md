# Somn项目主线梳理报告 v3.0 落实执行方案

> **日期**: 2026-04-24
> **制定依据**: `file/系统文件/Somn项目主线梳理报告.md` v3.0（4008行/63章节）
> **目的**: 将报告中的架构设计落实为可执行、可追踪的具体任务

---

## 一、现状盘点（报告 vs 实际）

| 模块 | 报告描述 | 实际状态 | 落实优先级 |
|------|---------|---------|----------|
| 王阳明xinxuefusion | 自主智能体可选集成 | `autonomous_agent.py`引用但模块不存在 | P0 |
| autonomous_core | 5大子系统+王阳明 | 子系统已实现，待集成SomnCore | P1 |
| dual_model_service v1.0 | 能力感知调度 | 在somn_core中已集成使用 | P2（验证） |
| collaboration_engine | 协作引擎+冲突解决 | 已实现，wisdom_dispatch有集成 | P2（补强） |
| timeout_guard | 五级降级守护 | 在somn_core/main_chain中已集成 | P2（验证） |
| data_collector | 多源数据采集 | 已实现，待与knowledge_graph打通 | P2 |
| growth_engine | AARRR漏斗+策略 | funnel_optimizer/demand_analyzer已实现 | P2（集成） |
| ImperialLibrary V3 | 藏书阁8分馆 | 已实现，稳定性待验证 | P3 |

---

## 二、P0级任务：修复王阳明fusion引擎

### 任务P0-1: 实现王阳明fusion引擎模块

**背景**: `src/autonomous_core/autonomous_agent.py` 第32行尝试导入：
```python
from ..intelligence.yangming_autonomous_fusion import 王阳明fusion引擎, xinxuedecision模式
```
该模块不存在，导致YANGMING_AVAILABLE=False。

**现有王阳明相关模块**（可复用）:
- `intelligence/engines/philosophy/yangming_zhixing_engine/` — 知行合一引擎
- `intelligence/reasoning/deep_reasoning_engine/_dre_xinmind.py` — 王阳明心学推理
- `intelligence/engines/unity_knowledge_action.py` — 知行合一评估器
- `intelligence/engines/super_wisdom_coordinator.py` — 王阳明xinxue系统注册
- `intelligence/engines/top_thinking_engine.py` — 王阳明思维法

**实施方案**:

```python
# src/intelligence/yangming_autonomous_fusion.py（新文件）
"""
王阳明xinxuefusion引擎 - Autonomous Agent融合模块
整合王阳明心学于自主智能体决策闭环
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

# 复用现有模块
try:
    from ..engines.philosophy.yangming_zhixing_engine import 王阳明知行合一引擎
    from .reasoning.deep_reasoning_engine._dre_xinmind import 王阳明心学推理
    from .engines.unity_knowledge_action import 知行合一评估器
    YANGMING_FUSION_AVAILABLE = True
except ImportError:
    YANGMING_FUSION_AVAILABLE = False

class xinxuedecision模式(Enum):
    """阳明心学决策模式"""
    ZHI_XING_HE_YI = "zhi_xing_he_yi"      # 知行合一
    ZHI_LIANG_ZHI = "zhi_liang_zhi"          # 致良知
    SHI_SHANG_MO_LIAN = "shi_shang_mo_lian"  # 事上磨练
    WU_WEI_ER_ZHI = "wu_wei_er_zhi"          # 无为而治

@dataclass
class 王阳明fusion引擎:
    """融合王阳明心学的自主决策引擎"""

    def __init__(self):
        if YANGMING_FUSION_AVAILABLE:
            self.zhixing = 王阳明知行合一引擎()
            self.xinmind = 王阳明心学推理()
            self.evaluator = 知行合一评估器()
        self.mode = xinxuedecision模式.ZHI_XING_HE_YI

    def think(self, problem: str, context: Dict) -> Dict[str, Any]:
        """
        阳明式思考：
        1. 知：理解问题本质（良知判断）
        2. 行：制定行动计划（事上磨练）
        3. 合一：知行互促，迭代优化
        """
        if not YANGMING_FUSION_AVAILABLE:
            return {"status": "fallback", "reason": "yangming_fusion_unavailable"}

        # 第一阶段：良知判断（问题本质）
        liangzhi = self.xinmind.analyze(problem)

        # 第二阶段：事上磨练（方案推演）
        plan = self.zhixing.generate_plan(problem, context)

        # 第三阶段：知行评估
        evaluation = self.evaluator.evaluate(plan, context)

        return {
            "liangzhi_insight": liangzhi,
            "action_plan": plan,
            "zhi_xing_score": evaluation.zhi_xing_score,
            "mode": self.mode.value,
        }

    def set_mode(self, mode: xinxuedecision模式):
        """设置决策模式"""
        self.mode = mode
```

**验收标准**:
- [ ] `autonomous_agent.py`导入YANGMING_AVAILABLE=True
- [ ] 引擎可处理goal_system产生的目标决策
- [ ] 与reflection_engine形成知行闭环

**文件**: `src/intelligence/yangming_autonomous_fusion.py`

---

## 三、P1级任务：AutonomousCore集成SomnCore

### 任务P1-1: AutonomousAgent注册到SomnCore主链

**现状**: `autonomous_core/autonomous_agent.py`独立运行，未接入SomnCore主入口。

**目标**: SomnCore启动时自动初始化AutonomousAgent，通过`_somn_main_chain.py`触发目标驱动。

**实施步骤**:

1. **在 `src/core/somn_core.py` 中添加初始化**:
```python
# SomnCore.__init__ 中添加
from src.autonomous_core.autonomous_agent import AutonomousAgent

self.autonomous_agent = None
if config.get('enable_autonomous', False):
    self.autonomous_agent = AutonomousAgent()
    logger.info("AutonomousAgent 已集成")
```

2. **在 `_somn_main_chain.py` 中添加目标触发**:
```python
# 用户输入后，检查是否有自主目标需要执行
if self.autonomous_agent:
    pending_goals = self.autonomous_agent.goal_system.get_ready_goals()
    if pending_goals:
        self._execute_autonomous_goals(pending_goals)
```

3. **AutonomousAgent与SomnCore的双向通信**:
```python
# SomnCore.think() 中
# 用户请求 → WisdomDispatcher → Claw执行
# ↓
# 结果 → AutonomousAgent.reflection.add_execution()
# ↓
# 反思 → 更新goal_progress → 生成新目标

# AutonomousAgent goal完成 → SomnCore执行
# ↓
# 结果 → reflection_engine观察 → 评估
```

**验收标准**:
- [ ] `somn_core.py`启动日志显示"AutonomousAgent 已集成"
- [ ] 用户对话触发自主目标执行（需有goal存在时）
- [ ] 目标完成后反思记录写入

### 任务P1-2: 王阳明fusion与GoalSystem联动

**目标**: GoalSystem创建目标时，自动使用xinxuefusion进行"知行合一"式目标分解。

```python
# 在GoalSystem.decompose_goal()中
def decompose_goal(self, goal_id: str) -> List[Goal]:
    # 使用王阳明xinxue进行目标分解
    if yangming_fusion := get_yangming_fusion():
        return yangming_fusion.decompose_with_liangzhi(goal)
    else:
        return self._default_decompose(goal)
```

---

## 四、P2级任务：补强验证类任务

### 任务P2-1: dual_model_service能力感知调度验证

**现状**: v2.0已集成，需验证以下场景:
- [ ] 图片输入 → 自动切换Gemma4（VISION能力）
- [ ] 代码分析 → 自动切换Gemma4（CODE能力）
- [ ] 超时切换 → 记录到failover_history
- [ ] 能力矩阵 `get_capability_matrix()` 输出正确

**验证脚本**: `scripts/verify_dual_model_v2.py`

### 任务P2-2: collaboration_engine与WisdomDispatcher打通

**现状**: `wisdom_dispatch/_dispatch_collaboration.py`已引用collaboration_engine，但协作模式未完整测试。

**目标**:
- [ ] 验证wisdom school协作调度（多学派并行思考）
- [ ] 冲突检测：两个学派给出矛盾建议时的处理
- [ ] 版本历史记录与回溯

### 任务P2-3: timeout_guard五级降级集成验证

**现状**: `somn_core.py`和`_somn_main_chain.py`已使用TimeoutGuard。

**验证**:
- [ ] 超时15s → WARNING级别日志
- [ ] 超时30s → DEGRADED，跳过非核心步骤
- [ ] 超时60s → EMERGENCY，最小可用输出
- [ ] 超时120s → TERMINATE，返回超时错误

### 任务P2-4: data_collector与knowledge_graph打通

**目标**:
- [ ] `data_collector.collect()` → 自动索引到KnowledgeGraph
- [ ] 外部数据源变化 → KnowledgeGraph自动更新
- [ ] 采集任务定时调度（cron表达式）

### 任务P2-5: growth_engine各模块集成验证

**目标**:
- [ ] `demand_analyzer.py` → `growth_strategy.py` → `funnel_optimizer.py` 全链路
- [ ] AARRR漏斗数据流入 → 增长策略生成
- [ ] 策略执行 → ROI追踪

---

## 五、P3级任务：稳定性与优化

| 任务ID | 内容 | 状态 |
|--------|------|------|
| P3-1 | ImperialLibrary V1.0稳定性压测（8分馆并发读写） | 待做 |
| P3-2 | 763个Claw全量任职率复验 | 待做 |
| P3-3 | ROI系统 v1.0双重计算bug复验 | 待做 |
| P3-4 | 藏书阁get_stats()性能基准测试 | 待做 |
| P3-5 | LearningSystem脏标记flush机制验证 | 待做 |

---

## 六、任务汇总

| 优先级 | 任务数 | 主要内容 | 预计工时 |
|--------|--------|---------|---------|
| **P0** | 1个 | 王阳明fusion引擎实现 | 2小时 |
| **P1** | 2个 | AutonomousCore→SomnCore集成 | 3小时 |
| **P2** | 5个 | 各模块补强验证 | 4小时 |
| **P3** | 5个 | 稳定性与优化 | 3小时 |
| **合计** | **13个** | | **12小时** |

---

## 七、落实进度追踪表

| 任务ID | 内容 | 状态 | 完成日期 | 备注 |
|--------|------|------|---------|------|
| P0-1 | 王阳明fusion引擎 | 待开始 | - | 阻断P1 |
| P1-1 | AutonomousAgent→SomnCore | 待开始 | - | |
| P1-2 | 阳明fusion与GoalSystem联动 | 待开始 | - | |
| P2-1 | dual_model验证 | 待开始 | - | |
| P2-2 | collaboration打通 | 待开始 | - | |
| P2-3 | timeout_guard验证 | 待开始 | - | |
| P2-4 | data_collector→KG打通 | 待开始 | - | |
| P2-5 | growth_engine集成验证 | 待开始 | - | |
| P3-1 | ImperialLibrary压测 | 待做 | - | |
| P3-2 | 763 Claw复验 | 待做 | - | |
| P3-3 | ROI bug复验 | 待做 | - | |
| P3-4 | get_stats基准测试 | 待做 | - | |
| P3-5 | flush机制验证 | 待做 | - | |

---

*本方案由Somn项目主线梳理报告 v3.0 落实程序自动生成*
