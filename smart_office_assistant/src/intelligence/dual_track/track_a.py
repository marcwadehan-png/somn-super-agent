"""
A轨：神政轨 (Divine Governance Track)
====================================

★ 核心定位 ★
神政轨是监管体系，对整个项目全局进行监管。

核心职责:
1. 系统级全局监管 - 生态引擎驱动（健康监控/资源分配/环境感知/演化追踪）
2. 任务级监管 - 对所有工作流进行监管
3. 进度催促 - 锦督促引擎监管节点
4. 惩罚问责 - 行政之鞭引擎执行惩罚
5. 存档归档 - NeuralMemory存档核心知识

★ 监管Claw体系 ★
神政轨Claw是贤者Claw被任命到监管岗位:
- 生态监管Claw - 系统全局生态健康监管（v3.0新增）
- 进度监管Claw - 催促任务进度
- 质量监管Claw - 质疑执行质量
- 工作流监管Claw - 检查流程合规
- 绩效监管Claw - PPU大师，绩效审判

★ 生态引擎集成 ★
v3.0 接入生态引擎5大组件，实现系统级全局监管:
- EcosystemManager: 系统健康度监控（CPU/内存/磁盘/网络）
- ResourceOptimizer: 资源智能分配（优先级抢占式）
- EnvironmentalAdapter: 环境实时感知（psutil采集）
- EvolutionEngine: 多代演化追踪与改进建议
- EcosystemIntelligence: 一键串联监控Facade

★ 与神行轨的关系 ★
- 神政轨 → 监管方：喷子、质疑者、鞭策者、生态守护者
- 神行轨 → 执行方：干活的人、牛马
- 神政轨对神行轨的Claw进行监管和鞭策

★ 网络搜索增强 ★
v2.6.0 新增网络搜索能力，支持：
- 执行案例搜索
- 监管政策搜索
- 行业基准数据搜索

版本: v3.2.0
更新: 2026-04-30（v3.2.0 系统压力门控+生态驱动决策+资源生命周期闭环）
"""

import logging
import asyncio
import threading
import time as _time
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════════════════════
# 网络搜索增强（懒加载）
# ══════════════════════════════════════════════════════════════════════════════

_TRACK_A_WEB: Optional[Any] = None


def _get_track_a_web():
    """获取 TrackAWeb 实例（懒加载）"""
    global _TRACK_A_WEB
    if _TRACK_A_WEB is None:
        try:
            # 路径：knowledge_cells/web_integration.py
            import sys
            from pathlib import Path
            kc_path = Path(__file__).resolve().parents[2] / "knowledge_cells"
            if kc_path.exists():
                sys.path.insert(0, str(kc_path.parent))
                from knowledge_cells.web_integration import TrackAWeb
                _TRACK_A_WEB = TrackAWeb()
        except ImportError:
            logger.warning("[TrackA] Web integration not available")
            return None
    return _TRACK_A_WEB


# ══════════════════════════════════════════════════════════════════════════════
# 懒加载导入生态引擎（v3.0新增）
# ══════════════════════════════════════════════════════════════════════════════

_ECOSYSTEM_INTELLIGENCE: Optional[Any] = None
_ECOSYSTEM_INIT_LOCK = threading.Lock()


def _get_ecosystem_intelligence() -> Optional[Any]:
    """获取 EcosystemIntelligence 单例（懒加载+双重检查锁）

    Note: src/ecology/ 目录已移除，生态能力已整合至
    knowledge_cells/ecology_ml_bridge.py + neural_memory_v7.py
    """
    # 生态模块已迁移至 neural_memory_v7，始终返回 None
    return None


# ══════════════════════════════════════════════════════════════════════════════
# 懒加载导入监管系统
# ══════════════════════════════════════════════════════════════════════════════

def _get_supervision_claws():
    """懒加载监管Claw系统"""
    from ._supervision_claws import (
        SupervisionClawFactory,
        SupervisionLevel,
        SupervisionType,
        SupervisionClaw,
    )
    return {
        'factory': SupervisionClawFactory,
        'SupervisionLevel': SupervisionLevel,
        'SupervisionType': SupervisionType,
        'SupervisionClaw': SupervisionClaw,
    }


def _get_supervision_engines():
    """懒加载监管引擎"""
    from ._supervision_engines import (
        get_jindu_engine,
        get_whiplash_engine,
        JinDuCuJinEngine,
        AdministrativeWhipEngine,
    )
    return {
        'jindu': get_jindu_engine,
        'whiplash': get_whiplash_engine,
        'JinDuCuJinEngine': JinDuCuJinEngine,
        'AdministrativeWhipEngine': AdministrativeWhipEngine,
    }


# ══════════════════════════════════════════════════════════════════════════════
# 数据结构
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class TaskAssignment:
    """任务派发记录"""
    task_id: str
    task_type: str
    department: str
    assigned_claw: str
    assigned_time: str
    deadline: Optional[str] = None
    status: str = "pending"  # pending/running/completed/failed
    result: Optional[Dict[str, Any]] = None


@dataclass
class SupervisionReport:
    """监管报告"""
    id: str
    timestamp: str
    target_claw: str
    target_task: str
    supervision_type: str
    level: str
    message: str
    archived: bool = False


# ══════════════════════════════════════════════════════════════════════════════
# 神政轨主类
# ══════════════════════════════════════════════════════════════════════════════

class DivineGovernanceTrack:
    """
    神政轨 - 管理监管架构
    
    核心职责:
    1. 接收用户请求 + 全局监管
    2. 分析问题类型 + 质疑质量
    3. 制定执行策略 + 绩效评估
    4. 派发任务给B轨 + 进度催促
    5. 监控执行过程 + 流程合规
    6. 验收执行结果 + 存档归档
    
    核心差异定位:
    - 神政轨Claw = 监管者，喷子+质疑者+鞭策者
    - 对神行轨Claw进行全环节监管
    - NeuralMemory存档核心知识点
    
    知识访问权限:
    - 神政轨可以访问 NeuralMemory 全局调用
    - 神政轨可以访问 DomainNexus
    - 神政轨可以访问藏书阁
    """
    
    def __init__(self):
        # 推理引擎
        self.divine_reason = None  # 懒加载
        
        # 任务管理
        self.assignments: Dict[str, TaskAssignment] = {}
        self.task_counter = 0
        
        # B轨引用 (由Bridge设置)
        self._track_b = None
        
        # 监管系统 (懒加载)
        self._supervision_factory = None
        self._jindu_engine = None
        self._whiplash_engine = None
        
        # NeuralMemory接口
        self._memory_interface = None
        
        # 监管报告历史
        self.supervision_reports: List[SupervisionReport] = []

        # ── 网络搜索增强 (懒加载) ──
        self._track_a_web: Optional[Any] = None

        # ── 生态引擎系统 (v3.0新增, v3.1升级) ──
        self._ecosystem = None  # EcosystemIntelligence 单例
        self._ecosystem_last_monitor: Optional[Dict[str, Any]] = None
        self._ecosystem_monitor_count: int = 0

        # ── v3.1: 后台守护进程 + 回调管理 ──
        self._daemon_alerts: List[Dict[str, Any]] = []  # Daemon 推送的告警
        self._daemon_actions: List[Dict[str, Any]] = []  # Daemon 触发的策略
        self._on_resource_alert: Optional[Callable] = None  # 外部告警回调

        logger.info("[A轨] 神政轨 v3.2.0 初始化完成 (生产级资源管理+后台监控+自动演化+压力门控)")

    @property
    def track_a_web(self):
        """懒加载 TrackAWeb"""
        if self._track_a_web is None:
            self._track_a_web = _get_track_a_web()
        return self._track_a_web

    def _init_divine_reason(self):
        """懒加载推理引擎"""
        if self.divine_reason is None:
            from ..engines.sub_engines._divine_reason_engine import DivineReasonEngine
            self.divine_reason = DivineReasonEngine()
            logger.info("[A轨] DivineReasonEngine 加载完成")
    
    def _init_supervision_system(self):
        """初始化监管系统"""
        if self._supervision_factory is None:
            supervision_claws = _get_supervision_claws()
            self._supervision_factory = supervision_claws['factory']()
            
            # 加载监管引擎（共享Factory）
            supervision_engines = _get_supervision_engines()
            self._jindu_engine = supervision_engines['jindu'](factory=self._supervision_factory)
            self._whiplash_engine = supervision_engines['whiplash'](factory=self._supervision_factory)
            
            # 设置NeuralMemory接口
            if self._memory_interface:
                self._supervision_factory.set_memory_interface(self._memory_interface)
            
            logger.info("[A轨] 监管系统初始化完成（共享Factory v2.5.0）")

    def _init_ecosystem(self):
        """初始化生态引擎系统（v3.0新增, v3.1升级: 真实资源+Daemon集成）"""
        if self._ecosystem is None:
            self._ecosystem = _get_ecosystem_intelligence()
            if self._ecosystem:
                # v3.1: 注册超限回调 — 资源超限时自动通知A轨
                self._ecosystem.resource_optimizer.set_limit_callback(self._on_resource_limit)
                self._ecosystem.resource_optimizer.set_reclaim_callback(self._on_resource_reclaim)
                # 注册 Daemon 告警回调
                self._setup_daemon_callbacks()
                logger.info("[A轨] 生态引擎已连接（生产级资源管理+系统级监管就绪）")
            else:
                logger.warning("[A轨] 生态引擎不可用，系统级监管功能受限")

    def _setup_daemon_callbacks(self):
        """设置 Daemon 事件回调 (v3.1新增)"""
        if self._ecosystem and self._ecosystem.daemon_running:
            daemon = self._ecosystem._daemon
            daemon.on_alert(self._handle_daemon_alert)
            daemon.on_action(self._handle_daemon_action)

    def _handle_daemon_alert(self, event: Any) -> None:
        """Daemon 告警回调 — 将告警注入A轨监管报告"""
        alert_data = {
            "source": getattr(event, 'source', 'unknown'),
            "severity": getattr(event, 'severity', 'warning'),
            "detail": getattr(event, 'detail', ''),
            "timestamp": getattr(event, 'timestamp', 0),
        }
        self._daemon_alerts.append(alert_data)

        # 转换为监管报告
        report = SupervisionReport(
            id=f"DAEMON_{len(self._daemon_alerts)}_{alert_data['source']}",
            timestamp=datetime.now().isoformat(),
            target_claw="SYSTEM",
            target_task="daemon_monitor",
            supervision_type="ecosystem",
            level="critical" if alert_data['severity'] == "critical" else "warning",
            message=f"[后台监控] {alert_data['detail']}",
        )
        self.supervision_reports.append(report)
        logger.info(f"[A轨] Daemon告警已接收: {alert_data['detail'][:80]}")

    def _handle_daemon_action(self, event: Any) -> None:
        """Daemon 策略执行回调 — 记录自动策略执行"""
        action_data = {
            "detail": getattr(event, 'detail', ''),
            "data": getattr(event, 'data', {}),
            "timestamp": getattr(event, 'timestamp', 0),
        }
        self._daemon_actions.append(action_data)
        logger.info(f"[A轨] Daemon策略已执行: {action_data['detail'][:80]}")

    def _on_resource_limit(self, resource_type: Any, allocation: Any, event_type: str) -> None:
        """资源超限回调 (v3.1新增)"""
        rt_name = resource_type.value if hasattr(resource_type, 'value') else str(resource_type)
        report = SupervisionReport(
            id=f"RESOURCE_{event_type}_{rt_name}",
            timestamp=datetime.now().isoformat(),
            target_claw="RESOURCE_MANAGER",
            target_task="resource_limit",
            supervision_type="ecosystem",
            level="critical" if "hard" in event_type else "warning",
            message=f"[资源{event_type}] {rt_name} 利用率={allocation.utilization:.1f}%, "
                    f"稀缺度={allocation.scarcity:.0%}",
        )
        self.supervision_reports.append(report)
        logger.warning(
            f"[A轨] 资源{event_type}: {rt_name} "
            f"利用率={allocation.utilization:.1f}%, 稀缺度={allocation.scarcity:.0%}"
        )

    def _on_resource_reclaim(self, event: Any) -> None:
        """资源回收回调 (v3.1新增)"""
        report = SupervisionReport(
            id=f"RECLAIM_{event.task_id}_{event.resource_type.value}",
            timestamp=datetime.now().isoformat(),
            target_claw=event.task_id,
            target_task="resource_reclaim",
            supervision_type="ecosystem",
            level="warning",
            message=f"[资源回收] {event.task_id} 被回收 {event.amount_reclaimed:.0f} "
                    f"{event.resource_type.value} — {event.reason}",
        )
        self.supervision_reports.append(report)

    def set_memory_interface(self, memory_interface):
        """
        设置NeuralMemory接口
        
        神政轨可全局调用NeuralMemory进行存档
        """
        self._memory_interface = memory_interface
        if self._supervision_factory:
            self._supervision_factory.set_memory_interface(memory_interface)
        logger.info("[A轨] NeuralMemory接口已连接")
    
    def set_track_b(self, track_b) -> None:
        """设置B轨引用"""
        self._track_b = track_b
        logger.info("[A轨] 已连接B轨(神行轨)")

    # ══════════════════════════════════════════════════════════════════════════
    # 贤者Claw任命机制（核心功能）
    # ══════════════════════════════════════════════════════════════════════════

    def register_wiseone(
        self,
        claw_id: str,
        worker: "ClawIndependentWorker",
    ) -> bool:
        """
        【核心功能】注册贤者Claw到神政轨池

        贤者Claw可以被任命到监管岗位。

        Args:
            claw_id: 贤者Claw ID
            worker: Claw工作器实例

        Returns:
            是否注册成功
        """
        if self._supervision_factory is None:
            self._init_supervision_system()

        try:
            self._supervision_factory.register_wiseone(worker)
            logger.info(f"[A轨] 贤者Claw '{claw_id}' 已注册到神政轨池")
            return True
        except Exception as e:
            logger.error(f"[A轨] 贤者Claw注册失败: {e}")
            return False

    def appoint(
        self,
        claw_id: str,
        position: str,
        custom_name: Optional[str] = None,
        custom_title: Optional[str] = None,
    ) -> Optional["SupervisionClaw"]:
        """
        【核心功能】任命贤者Claw到监管岗位

        流程:
        1. 从池中获取贤者Claw
        2. 创建监管Claw（携带贤者能力）
        3. 记录任命
        4. 返回监管Claw

        Args:
            claw_id: 贤者Claw ID
            position: 监管岗位（progress/quality/workflow/performance）
            custom_name: 自定义名称
            custom_title: 自定义title

        Returns:
            监管Claw实例（任命失败返回None）
        """
        if self._supervision_factory is None:
            self._init_supervision_system()

        claw = self._supervision_factory.appoint(
            claw_id=claw_id,
            position=position,
            custom_name=custom_name,
            custom_title=custom_title,
        )

        if claw:
            logger.info(
                f"[A轨] 任命完成: {claw_id} → {position} "
                f"({claw.name}) | 模式: {'贤者' if claw.has_wiseone_power else '独立'}"
            )

        return claw

    def auto_appoint_all(self) -> Dict[str, "SupervisionClaw"]:
        """
        【核心功能】自动任命所有贤者Claw到监管岗位

        使用默认配置批量任命

        Returns:
            岗位 -> 监管Claw 的映射
        """
        if self._supervision_factory is None:
            self._init_supervision_system()

        claws = self._supervision_factory.auto_appoint_all()

        for pos, claw in claws.items():
            logger.info(
                f"[A轨] 自动任命: {claw.name} → {pos} "
                f"| 模式: {'贤者' if claw.has_wiseone_power else '独立'}"
            )

        return claws

    def get_supervision_claw(self, position: str) -> Optional["SupervisionClaw"]:
        """获取指定岗位的监管Claw"""
        if self._supervision_factory is None:
            return None
        return self._supervision_factory.get_claw(position)

    def get_all_supervision_claws(self) -> List["SupervisionClaw"]:
        """获取所有监管Claw"""
        if self._supervision_factory is None:
            return []
        return self._supervision_factory.get_all_claws()

    def list_wiseones(self) -> List[str]:
        """列出所有注册的贤者Claw"""
        if self._supervision_factory is None:
            return []
        return self._supervision_factory.list_wiseones()

    async def supervise_with_thinking(
        self,
        position: str,
        target: str,
        context: Dict[str, Any],
        level: str = "normal",
    ) -> Optional["SupervisionRecord"]:
        """
        【核心功能】带独立思考的监管

        让监管Claw先独立思考，再执行监管。

        Args:
            position: 监管岗位
            target: 被监管目标
            context: 上下文
            level: 监管等级

        Returns:
            监管记录
        """
        claw = self.get_supervision_claw(position)
        if not claw:
            logger.warning(f"[A轨] 岗位 {position} 无监管Claw")
            return None

        # 独立思考
        task_desc = context.get("task", "unknown")
        thinking_result = await claw.think_independently(
            f"监管 {target} 的 {task_desc}",
            context=context,
        )
        logger.info(f"[A轨] {claw.name} 独立思考: {thinking_result.get('thinking', '')[:100]}...")

        # 执行监管
        from ._supervision_claws import SupervisionLevel
        level_enum = getattr(SupervisionLevel, level.upper(), SupervisionLevel.NORMAL)

        record = await claw.supervise(
            target=target,
            context=context,
            level=level_enum,
        )

        return record

    # ══════════════════════════════════════════════════════════════════════════
    # 核心能力: 贤者Claw独立工作（能真正干活）
    # ══════════════════════════════════════════════════════════════════════════

    async def work(
        self,
        position: str,
        task: str,
        context: Dict[str, Any] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        【核心能力】让监管Claw独立工作

        SupervisionClaw不只是监管，还能执行具体任务。
        这是"贤者Claw能工作解决问题"的具体实现。

        Args:
            position: 监管岗位（progress/quality/workflow/performance）
            task: 任务描述
            context: 上下文

        Returns:
            执行结果
        """
        claw = self.get_supervision_claw(position)
        if not claw:
            logger.warning(f"[A轨] 岗位 {position} 无监管Claw")
            return None

        logger.info(f"[A轨] {claw.name} 执行任务: {task[:50]}...")

        # 调用监管Claw的工作能力
        result = await claw.work(task, context)

        logger.info(
            f"[A轨] {claw.name} 工作完成 - "
            f"模式: {result.get('worker_mode', 'unknown')} - "
            f"置信度: {result.get('confidence', 0):.2f}"
        )

        return result

    async def solve(
        self,
        position: str,
        problem: str,
        context: Dict[str, Any] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        【核心能力】让监管Claw解决问题

        监管Claw能独立分析问题并给出解决方案。

        Args:
            position: 监管岗位
            problem: 问题描述
            context: 上下文

        Returns:
            解决方案
        """
        claw = self.get_supervision_claw(position)
        if not claw:
            logger.warning(f"[A轨] 岗位 {position} 无监管Claw")
            return None

        logger.info(f"[A轨] {claw.name} 解决问题: {problem[:50]}...")

        # 调用监管Claw的解决问题能力
        result = await claw.solve(problem, context)

        logger.info(
            f"[A轨] {claw.name} 问题解决 - "
            f"成功: {result.get('success', False)}"
        )

        return result

    async def analyze(
        self,
        position: str,
        target: str,
        context: Dict[str, Any] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        【核心能力】让监管Claw分析问题

        Args:
            position: 监管岗位
            target: 分析目标
            context: 上下文

        Returns:
            分析结果
        """
        claw = self.get_supervision_claw(position)
        if not claw:
            logger.warning(f"[A轨] 岗位 {position} 无监管Claw")
            return None

        result = await claw.analyze(target, context)

        return result

    async def delegate_to_track_b(
        self,
        task: str,
        context: Dict[str, Any] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        【核心能力】委派任务到神行轨

        神政轨可以委派任务给神行轨执行。

        Args:
            task: 任务描述
            context: 上下文

        Returns:
            执行结果
        """
        if not self._track_b:
            logger.warning("[A轨] 神行轨未连接，无法委派任务")
            return None

        logger.info(f"[A轨] 委派任务到B轨: {task[:50]}...")

        # 委派到神行轨
        result = await self._track_b.delegate_task(
            task=task,
            caller_type="a_governance",
            context=context,
        )

        return result

    # ══════════════════════════════════════════════════════════════════════════
    # 核心处理流程
    # ══════════════════════════════════════════════════════════════════════════
    
    def process_request(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        处理用户请求 (A轨主入口)
        
        v3.0 升级：新增生态感知环节，在任务分析前先评估系统环境状态
        
        Args:
            query: 用户查询
            context: 上下文
            
        Returns:
            处理结果
        """
        start_time = datetime.now()
        logger.info(f"[A轨] 接收请求: {query[:50]}...")
        
        # 初始化懒加载组件
        self._init_divine_reason()
        self._init_supervision_system()
        self._init_ecosystem()
        
        # ── v3.0: 系统生态感知（在任务分析前评估系统状态） ──
        ecosystem_context = self._quick_ecosystem_check()

        # ── v3.2: 系统压力门控 — 危急时拒绝低优先级任务 ──
        gate_check = self._system_pressure_gate(query, ecosystem_context)
        if gate_check["blocked"]:
            elapsed = (datetime.now() - start_time).total_seconds()
            return {
                "success": False,
                "blocked": True,
                "reason": gate_check["reason"],
                "pressure": gate_check.get("pressure"),
                "track": "A",
                "version": "v3.2.0",
                "elapsed_seconds": elapsed,
            }

        # 1. 问题分析与决策
        analysis = self._analyze_and_decide(query, context)
        
        # 将生态上下文注入分析结果
        analysis["ecosystem_snapshot"] = ecosystem_context

        # ── v3.2: 生态快照驱动决策 — 根据系统健康度调整优先级和策略 ──
        self._ecosystem_driven_adjustment(analysis, ecosystem_context)
        
        # 2. 对分析结果进行质量质疑
        self._supervise_analysis(analysis)
        
        # ── v3.0: 生态监管Claw参与质量质疑 ──
        self._ecosystem_supervise(analysis, ecosystem_context)
        
        # 3. 制定执行策略
        strategy = self._formulate_strategy(analysis)
        
        # 4. 派发任务给B轨 + 注册截止节点
        if self._track_b is None:
            raise RuntimeError("B轨未连接，无法派发任务")

        # ── v3.2: 派发前真实资源分配 ──
        task_priority = 7 if strategy.get("priority") == "high" else 5
        resource_allocated = self._allocate_task_resources(
            f"pending_{self.task_counter + 1}", task_priority
        )
        strategy["resource_allocated"] = resource_allocated

        # 如果资源不足, 降低优先级或拒绝
        if not resource_allocated.get("success") and resource_allocated.get("suggestion") == "reject":
            elapsed = (datetime.now() - start_time).total_seconds()
            return {
                "success": False,
                "blocked": True,
                "reason": "资源不足，任务被拒绝",
                "resource_detail": resource_allocated,
                "track": "A",
                "version": "v3.2.0",
                "elapsed_seconds": elapsed,
            }

        task_id = self._dispatch_to_track_b(strategy)
        
        # 注册锦督促节点
        self._register_deadlines(task_id, strategy)
        
        # 5. 等待B轨执行结果 (简化版：同步等待)
        result = self._wait_for_result(task_id)
        
        # 6. 对执行结果进行质量监管
        supervised_result = self._supervise_execution(task_id, result)
        
        # 7. 验收结果
        final_result = self._review_result(task_id, supervised_result)
        
        # 8. 存档核心知识
        self._archive_knowledge(query, analysis, strategy, final_result)
        
        # 9. 任务完成后释放资源 (v3.1新增)
        self._release_task_resources(task_id)
        
        # 10. 任务完成后演化记录
        self._record_evolution(analysis, final_result)
        
        elapsed = (datetime.now() - start_time).total_seconds()
        
        return {
            "success": True,
            "query": query,
            "analysis": analysis,
            "strategy": strategy,
            "execution_result": final_result,
            "supervision_reports": [r for r in self.supervision_reports if r.id.split('-')[0] == task_id[:8]],
            "ecosystem_snapshot": ecosystem_context,
            "daemon_alerts": len(self._daemon_alerts),
            "daemon_actions": len(self._daemon_actions),
            "track": "A",
            "version": "v3.2.0",
            "elapsed_seconds": elapsed,
        }
    
    def _analyze_and_decide(self, query: str, context: Optional[Dict]) -> Dict[str, Any]:
        """问题分析与决策"""
        logger.info("[A轨] 开始问题分析...")

        # 1. 使用 ProblemAnalyzer 分析问题（获取问题类型、紧迫度等）
        problem_type = "UNKNOWN"
        urgency = "normal"
        angles = []

        try:
            from ..engines.sub_engines._divine_reason_engine import ProblemAnalyzer
            pa_result = ProblemAnalyzer.analyze(query)
            problem_type = pa_result.get("problem_type", "UNKNOWN")
            urgency = pa_result.get("urgency", "normal")
            angles = pa_result.get("angles", [])
        except Exception as e:
            logger.warning(f"[A轨] ProblemAnalyzer 不可用: {e}")

        # 2. 使用 DivineReason 进行深度推理
        reasoning_summary = ""
        confidence = 0.5
        engines_used = []

        try:
            from ..engines.sub_engines._divine_reason_engine import (
                DivineReasonEngine,
                ReasoningRequest,
            )
            engine = DivineReasonEngine()
            request = ReasoningRequest(
                query=query,
                problem_type=problem_type,
                context=context or {},
            )
            response = engine.reason(request)
            reasoning_summary = response.reasoning_summary
            confidence = response.confidence
            engines_used = response.engines_used
        except Exception as e:
            logger.warning(f"[A轨] DivineReason 不可用: {e}")

        return {
            "problem_type": problem_type,
            "urgency": urgency,
            "angles": angles,
            "reasoning_summary": reasoning_summary,
            "confidence": confidence,
            "engines_used": engines_used,
        }
    
    def _formulate_strategy(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """制定执行策略"""
        logger.info("[A轨] 制定执行策略...")
        
        problem_type = analysis.get("problem_type", "")
        
        # 根据问题类型确定主责部门
        from ..dispatcher.wisdom_dispatch._dispatch_court import get_department_for_problem
        from ..dispatcher.wisdom_dispatch._dispatch_enums import ProblemType
        
        department_name = "工部"  # 默认
        reason = "默认调度"

        try:
            # ProblemAnalyzer 返回字符串类型的 problem_type
            # 尝试按枚举名或值匹配
            matched_pt = None
            for pt in ProblemType:
                if pt.value == problem_type or pt.name == problem_type:
                    matched_pt = pt
                    break

            if matched_pt:
                dept, reason = get_department_for_problem(matched_pt)
                department_name = dept.value
        except Exception as e:
            logger.warning(f"[A轨] 部门路由失败: {e}")

        return {
            "department": department_name,
            "department_reason": reason,
            "execution_mode": "direct",
            "priority": "high" if analysis.get("urgency") == "high" else "normal",
            "context": analysis,
        }
    
    # ══════════════════════════════════════════════════════════════════════════
    # 监管方法
    # ══════════════════════════════════════════════════════════════════════════
    
    def _supervise_analysis(self, analysis: Dict[str, Any]) -> Optional[SupervisionReport]:
        """对分析结果进行质量质疑"""
        if self._supervision_factory is None:
            return None
        
        supervision_claws = _get_supervision_claws()
        quality_claw = self._supervision_factory.get_claw("quality")
        
        if quality_claw:
            context = {
                "task_id": "analysis",
                "result": {
                    "confidence": analysis.get("confidence", 0.5),
                    "problem_type": analysis.get("problem_type", ""),
                }
            }
            
            # 质疑分析质量
            level = supervision_claws['SupervisionLevel'].NORMAL
            if analysis.get("confidence", 0) < 0.7:
                level = supervision_claws['SupervisionLevel'].HARSH
            
            # 同步执行async supervise方法
            try:
                loop = asyncio.new_event_loop()
                record = loop.run_until_complete(quality_claw.supervise(
                    target="DivineReason",
                    context=context,
                    level=level,
                ))
                record_id = record.id if hasattr(record, 'id') else str(id(record))
                loop.close()
            except Exception as e:
                logger.warning(f"[A轨] 监管Claw监督失败: {e}")
                record_id = f"supervision_{id(e)}"
            
            report = SupervisionReport(
                id=record_id,
                timestamp=datetime.now().isoformat(),
                target_claw="DivineReason",
                target_task="analysis",
                supervision_type="quality",
                level=level.value,
                message=f"分析质量质疑: 置信度 {analysis.get('confidence', 0):.2f}",
            )
            self.supervision_reports.append(report)
            
            return report
        
        return None
    
    def _supervise_execution(self, task_id: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """对执行结果进行监管"""
        if self._supervision_factory is None:
            return result
        
        supervision_claws = _get_supervision_claws()
        assigned_claw = self.assignments.get(task_id, TaskAssignment("", "", "", "", "")).assigned_claw
        
        try:
            loop = asyncio.new_event_loop()
            
            # 1. 进度监管
            progress_claw = self._supervision_factory.get_claw("progress")
            if progress_claw:
                context = {
                    "task_id": task_id,
                    "progress": result.get("progress", 100) if result else 0,
                    "expected_progress": 100,
                }
                loop.run_until_complete(progress_claw.supervise(
                    target=assigned_claw,
                    context=context,
                    level=supervision_claws['SupervisionLevel'].NORMAL,
                ))
            
            # 2. 质量监管
            quality_claw = self._supervision_factory.get_claw("quality")
            if quality_claw:
                context = {
                    "task_id": task_id,
                    "result": result or {},
                }
                loop.run_until_complete(quality_claw.supervise(
                    target=assigned_claw,
                    context=context,
                    level=supervision_claws['SupervisionLevel'].NORMAL,
                ))
            
            # 3. 绩效监管
            performance_claw = self._supervision_factory.get_claw("performance")
            if performance_claw:
                context = {
                    "task_id": task_id,
                    "result": result or {},
                    "metrics": {
                        "progress": result.get("progress", 100) if result else 0,
                        "confidence": result.get("confidence", 0.8) if result else 0.8,
                        "issues": [] if (result and result.get("success")) else ["执行失败"],
                    },
                }
                loop.run_until_complete(performance_claw.supervise(
                    target=assigned_claw,
                    context=context,
                    level=supervision_claws['SupervisionLevel'].NORMAL,
                ))
            
            # 4. 贤者协作规则审核（多Claw协作时触发品秩仲裁）
            collab_list = self._extract_collaborators(result)
            if len(collab_list) > 1:
                try:
                    from .sage_collaboration_rules import get_sage_collaboration_rules
                    rules = get_sage_collaboration_rules()
                    review = rules.review_collaboration_result(result, collab_list)
                    if review.get("review_warnings"):
                        logger.info(
                            f"[A轨-协作审核] 任务 {task_id}: "
                            f"{review['review_warnings']}"
                        )
                    # 将审核结果注入result，传递给下游
                    if isinstance(result, dict):
                        result["collaboration_review"] = review
                except Exception as e:
                    logger.debug(f"[A轨] 协作仲裁跳过: {e}")

            loop.close()
        except Exception as e:
            logger.warning(f"[A轨] 执行监管失败: {e}")
        
        return result
    
    def _register_deadlines(self, task_id: str, strategy: Dict[str, Any]) -> None:
        """注册截止节点到锦督促引擎"""
        if self._jindu_engine is None:
            return
        
        from datetime import timedelta
        
        assigned_claw = self.assignments.get(task_id, TaskAssignment("", "", "", "", "")).assigned_claw
        
        self._jindu_engine.register_deadline(
            task_id=task_id,
            target_claw=assigned_claw,
            description=f"执行策略: {strategy.get('department', 'unknown')}",
            deadline=datetime.now() + timedelta(minutes=10),  # 默认10分钟
            urgency_level=3,
        )
    
    # ══════════════════════════════════════════════════════════════════════════
    # NeuralMemory集成
    # ══════════════════════════════════════════════════════════════════════════
    
    def _archive_knowledge(
        self,
        query: str,
        analysis: Dict[str, Any],
        strategy: Dict[str, Any],
        result: Dict[str, Any],
    ) -> None:
        """存档核心知识到NeuralMemory"""
        if self._memory_interface is None:
            logger.info("[A轨] NeuralMemory未连接，跳过存档")
            return
        
        try:
            # 同步调用async方法
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # 存档分析结果
            loop.run_until_complete(self._memory_interface.add_memory(
                content=f"[神政轨分析] Q: {query} | 问题类型: {analysis.get('problem_type')} | 置信度: {analysis.get('confidence', 0):.2f}",
                metadata={
                    "source": "track_a_analysis",
                    "type": "analysis",
                    "query": query,
                    "problem_type": analysis.get("problem_type"),
                    "confidence": analysis.get("confidence", 0),
                },
                operator="神政轨-存档",
            ))
            
            # 存档执行结果
            loop.run_until_complete(self._memory_interface.add_memory(
                content=f"[神政轨执行] 策略: {strategy.get('department')} | 结果: {result.get('accepted', False)} | 质量: {result.get('quality', 'unknown')}",
                metadata={
                    "source": "track_a_execution",
                    "type": "execution",
                    "department": strategy.get("department"),
                    "success": result.get("accepted", False),
                },
                operator="神政轨-存档",
            ))
            
            # 存档监管报告摘要
            recent_reports = [r for r in self.supervision_reports[-5:]]
            if recent_reports:
                report_summary = "; ".join([r.message for r in recent_reports])
                loop.run_until_complete(self._memory_interface.add_memory(
                    content=f"[神政轨监管] {report_summary}",
                    metadata={
                        "source": "track_a_supervision",
                        "type": "supervision",
                        "report_count": len(recent_reports),
                    },
                    operator="神政轨-存档",
                ))
            
            loop.close()
            logger.info("[A轨] 核心知识已存档到NeuralMemory")
            
        except Exception as e:
            logger.error(f"[A轨] 存档失败: {e}")
    
    # ══════════════════════════════════════════════════════════════════════════
    # B轨通信
    # ══════════════════════════════════════════════════════════════════════════
    
    def _dispatch_to_track_b(self, strategy: Dict[str, Any]) -> str:
        """
        派发任务给B轨
        
        v2.5.0: 策略中携带具体Claw名称（如果B轨有任命的话）
        关键设计：A轨可以直接调用B轨的职能部门 (跳过多余环节)
        """
        self.task_counter += 1
        task_id = f"A_TO_B_{self.task_counter}"
        
        department = strategy.get("department", "")
        
        # v2.5.0: 查询B轨该部门的具体Claw任命
        assigned_claw_name = "B轨执行器"
        if self._track_b and hasattr(self._track_b, 'get_primary_claw'):
            primary_claw = self._track_b.get_primary_claw(department)
            if primary_claw:
                claw_name = primary_claw.claw_name if hasattr(primary_claw, 'claw_name') else str(primary_claw)
                assigned_claw_name = claw_name
                strategy["claw_name"] = claw_name
                logger.info(f"[A轨] 派发任务 {task_id} → {department}（主责Claw: {claw_name}）")
            else:
                # 查看所有任命的Claw
                dept_claws = self._track_b.get_department_claws(department)
                if dept_claws:
                    first_claw = dept_claws[0]
                    claw_name = first_claw.claw_name if hasattr(first_claw, 'claw_name') else str(first_claw)
                    assigned_claw_name = claw_name
                    strategy["claw_name"] = claw_name
                    logger.info(f"[A轨] 派发任务 {task_id} → {department}（Claw: {claw_name}）")
                else:
                    logger.info(f"[A轨] 派发任务 {task_id} → {department}（无Claw任命，使用降级推理）")
        else:
            logger.info(f"[A轨] 派发任务 {task_id} 给B轨...")
        
        # 创建任务记录
        assignment = TaskAssignment(
            task_id=task_id,
            task_type=department,
            department=department,
            assigned_claw=assigned_claw_name,
            assigned_time=datetime.now().isoformat(),
            status="pending",
        )
        self.assignments[task_id] = assignment
        
        # 确保策略中有task_description
        if "task_description" not in strategy:
            strategy["task_description"] = strategy.get("context", {}).get("query", "")
        
        # 调用B轨执行
        self._track_b.receive_task(
            task_id=task_id,
            strategy=strategy,
            callback=self._on_task_completed,
        )
        
        return task_id
    
    def _wait_for_result(self, task_id: str, timeout: float = 30.0) -> Dict[str, Any]:
        """等待B轨执行结果 (简化版)"""
        import time
        
        start = time.time()
        while time.time() - start < timeout:
            assignment = self.assignments.get(task_id)
            if assignment and assignment.status in ("completed", "failed"):
                return assignment.result or {}
            time.sleep(0.1)
        
        logger.warning(f"[A轨] 任务 {task_id} 超时")
        # v3.2: 超时后立即释放资源
        self._release_task_resources(task_id)
        return {"error": "timeout"}
    
    def _on_task_completed(self, task_id: str, result: Dict[str, Any]) -> None:
        """B轨任务完成回调"""
        logger.info(f"[A轨] 收到任务 {task_id} 完成通知")
        
        assignment = self.assignments.get(task_id)
        if assignment:
            assignment.status = "completed"
            assignment.result = result
        
        # 标记锦督促节点完成
        if self._jindu_engine:
            self._jindu_engine.mark_completed(task_id)
    
    @staticmethod
    def _extract_collaborators(result: Optional[Dict[str, Any]]) -> List[str]:
        """
        从多种B轨返回格式中提取协作Claw列表。

        兼容格式:
        1. CollaborativeResult: {'collaborators': [...], 'primary_claw': '...'}
        2. TaskTicket: {'collaborators_used': ['...'], 'claw_used': '...'}
        3. B轨ClawResult: {'claw_name': '...'} (单Claw, 返回 [claw_name])
        4. CollaborationProtocol: {'contributions': [{'claw_name': '...'}, ...]}
        """
        if not result or not isinstance(result, dict):
            return []

        # 格式1: 直接collaborators字段
        collabs = result.get("collaborators") or result.get("collaborators_used")
        if isinstance(collabs, list) and len(collabs) > 0:
            primary = result.get("primary_claw") or result.get("claw_used", "")
            full = [primary] + [c for c in collabs if c != primary] if primary else list(collabs)
            return [c for c in full if c]

        # 格式2: contributions字段
        contributions = result.get("contributions")
        if isinstance(contributions, list):
            names = []
            for c in contributions:
                name = c.get("claw_name") or c.get("author") or ""
                if name and name not in names:
                    names.append(name)
            return names

        # 格式3: 单Claw (回退)
        claw = result.get("claw_name") or result.get("claw_used", "")
        return [claw] if claw else []

    def _review_result(self, task_id: str, result: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"[A轨] 验收任务 {task_id} 结果...")
        
        # 基础验收逻辑
        if not result.get("success"):
            return {
                "accepted": False,
                "quality": "poor",
                "feedback": result.get("error", "执行失败"),
                "result": result,
            }

        # ── 贤者协作规则审核（多Claw协作时触发）──
        collaboration_review = None
        collab_list = self._extract_collaborators(result)
        if len(collab_list) > 1:
            try:
                from .sage_collaboration_rules import get_sage_collaboration_rules
                rules = get_sage_collaboration_rules()
                collaboration_review = rules.review_collaboration_result(
                    result, collab_list
                )
            except Exception as e:
                logger.debug(f"[A轨] 协作规则审核跳过: {e}")
                collaboration_review = None

        return {
            "accepted": True,
            "quality": "good",
            "feedback": "执行结果符合要求",
            "result": result,
            "collaboration_review": collaboration_review,
        }
    
    # ══════════════════════════════════════════════════════════════════════════
    # 公共监管接口
    # ══════════════════════════════════════════════════════════════════════════
    
    def supervise_track_b_claw(
        self,
        claw_name: str,
        reason: str,
        level: str = "normal",
    ) -> Optional[SupervisionReport]:
        """
        直接监管B轨Claw
        
        Args:
            claw_name: Claw名称
            reason: 监管原因
            level: 监管等级 (mild/normal/harsh/extreme)
            
        Returns:
            监管报告
        """
        if self._supervision_factory is None:
            self._init_supervision_system()
        
        level_map = {
            "mild": "MILD",
            "normal": "NORMAL",
            "harsh": "HARSH",
            "extreme": "EXTREME",
        }
        
        supervision_claws = _get_supervision_claws()
        sup_level = getattr(supervision_claws['SupervisionLevel'], level_map.get(level, "NORMAL"))
        
        # 获取绩效Claw执行监管
        claw = self._supervision_factory.get_claw("performance")
        if claw:
            record_id = claw.supervise(
                target=claw_name,
                context={"task_id": "direct_supervision"},
                level=sup_level,
            )
            
            report = SupervisionReport(
                id=record_id,
                timestamp=datetime.now().isoformat(),
                target_claw=claw_name,
                target_task="direct_supervision",
                supervision_type="direct",
                level=level,
                message=f"[直接监管] {reason}",
            )
            self.supervision_reports.append(report)
            return report
        
        return None
    
    def punish_track_b_claw(
        self,
        claw_name: str,
        reason: str,
        punishment: str = "warning",
    ) -> Optional[Dict]:
        """
        惩罚B轨Claw
        
        Args:
            claw_name: Claw名称
            reason: 惩罚原因
            punishment: 惩罚类型 (warning/criticism/logging/public_shame/escalation/suspension)
            
        Returns:
            惩罚记录
        """
        if self._whiplash_engine is None:
            self._init_supervision_system()
        
        punishment_map = {
            "warning": "WARNING",
            "criticism": "CRITICISM",
            "logging": "LOGGING",
            "public_shame": "PUBLIC_SHAME",
            "escalation": "ESCALATION",
            "suspension": "SUSPENSION",
        }
        
        from ._supervision_engines import PunishmentType
        p_type = getattr(PunishmentType, punishment_map.get(punishment, "WARNING"))
        
        record = self._whiplash_engine.punish(
            target_claw=claw_name,
            target_task="direct_punishment",
            reason=reason,
            punishment=p_type,
        )
        
        return {
            "id": record.id,
            "target": claw_name,
            "punishment": record.punishment_type.value,
            "reason": reason,
            "executed": record.executed,
        }

    # ══════════════════════════════════════════════════════════════════════════
    # 网络搜索增强（v2.6.0）
    # ══════════════════════════════════════════════════════════════════════════

    def search_execution_cases(
        self,
        task_type: str,
        context: str = "",
        max_results: int = 3,
    ) -> Dict[str, Any]:
        """
        搜索执行案例

        在派发任务前，搜索相关执行案例作为参考

        Args:
            task_type: 任务类型
            context: 上下文
            max_results: 最大结果数

        Returns:
            执行案例列表
        """
        track_a_web = self.track_a_web
        if not track_a_web or not track_a_web.is_enabled():
            return {"success": False, "source": "disabled", "reason": "web_disabled"}

        try:
            result = track_a_web.search_execution_cases(task_type, context, max_results)
            if result.get("success"):
                logger.info(f"[TrackA] Found {len(result.get('results', []))} execution cases for {task_type}")
            return result
        except Exception as e:
            logger.warning(f"[TrackA] Execution case search failed: {e}")
            return {"success": False, "error": str(e)}

    def search_regulation_updates(
        self,
        domain: str,
        max_results: int = 2,
    ) -> Dict[str, Any]:
        """
        搜索监管政策更新

        Args:
            domain: 相关领域
            max_results: 最大结果数

        Returns:
            最新监管政策
        """
        track_a_web = self.track_a_web
        if not track_a_web or not track_a_web.is_enabled():
            return {"success": False, "source": "disabled"}

        try:
            return track_a_web.search_regulation_updates(domain, max_results)
        except Exception as e:
            logger.warning(f"[TrackA] Regulation search failed: {e}")
            return {"success": False, "error": str(e)}

    def search_benchmark_data(
        self,
        metric: str,
        industry: str = "",
        max_results: int = 2,
    ) -> Dict[str, Any]:
        """
        搜索行业基准数据

        用于绩效评估时对比行业标准

        Args:
            metric: 指标名称
            industry: 行业
            max_results: 最大结果数

        Returns:
            基准数据
        """
        track_a_web = self.track_a_web
        if not track_a_web or not track_a_web.is_enabled():
            return {"success": False, "source": "disabled"}

        try:
            return track_a_web.search_benchmark_data(metric, industry, max_results)
        except Exception as e:
            logger.warning(f"[TrackA] Benchmark data search failed: {e}")
            return {"success": False, "error": str(e)}

    # ══════════════════════════════════════════════════════════════════════════
    # 系统级全局监管（v3.0 生态引擎集成）
    # ══════════════════════════════════════════════════════════════════════════

    def _quick_ecosystem_check(self) -> Dict[str, Any]:
        """
        快速生态检查 — 在任务处理前评估系统环境
        
        v3.0 核心方法：每次请求前调用，获取系统健康快照。
        如果生态引擎不可用，返回降级信息。
        
        Returns:
            生态快照 dict，包含 health/environment/resources/changes 等信息
        """
        if self._ecosystem is None:
            return {"available": False, "reason": "ecosystem_not_initialized"}
        
        try:
            monitor_result = self._ecosystem.monitor()
            self._ecosystem_last_monitor = monitor_result
            self._ecosystem_monitor_count += 1
            
            # 提取关键信息作为生态快照
            eco_report = monitor_result.get("ecosystem_report", {})
            resource_report = monitor_result.get("resource_report", {})
            env_changes = monitor_result.get("environment_changes", [])
            
            overall_health = eco_report.get("overall_health", "unknown")
            alerts = eco_report.get("alerts", [])
            
            snapshot = {
                "available": True,
                "overall_health": overall_health,
                "alerts_count": len(alerts),
                "has_critical_alerts": any(
                    a.get("severity") == "high" for a in alerts
                ) if alerts else False,
                "environment_changes": env_changes,
                "resource_suggestions": resource_report.get("suggestions", []),
                "monitor_count": self._ecosystem_monitor_count,
            }
            
            # 如果有危急警报，记录到监管报告
            if snapshot["has_critical_alerts"]:
                for alert in alerts:
                    if alert.get("severity") == "high":
                        report = SupervisionReport(
                            id=f"ECO_{self._ecosystem_monitor_count}_{alert['metric']}",
                            timestamp=datetime.now().isoformat(),
                            target_claw="SYSTEM",
                            target_task="ecosystem_health",
                            supervision_type="ecosystem",
                            level="critical",
                            message=f"[生态警报] {alert['metric']}: {alert.get('value', '?')}, "
                                    f"偏差: {alert.get('deviation', 0):.1f}%",
                        )
                        self.supervision_reports.append(report)
                        logger.warning(
                            f"[A轨] 生态警报: {alert['metric']} 状态={alert['status']}, "
                            f"偏差={alert.get('deviation', 0):.1f}%"
                        )
            
            return snapshot
        except Exception as e:
            logger.error(f"[A轨] 生态监控失败: {e}")
            return {"available": False, "reason": str(e)}

    def _ecosystem_supervise(
        self,
        analysis: Dict[str, Any],
        ecosystem_context: Dict[str, Any],
    ) -> Optional[SupervisionReport]:
        """
        生态监管 — 用生态监管Claw对任务进行生态影响评估
        
        v3.0 新增：生态监管Claw（第5个监管岗位）参与质量质疑。
        从系统资源消耗角度评估任务对生态系统的影响。
        """
        if not ecosystem_context.get("available"):
            return None
        
        if self._supervision_factory is None:
            return None
        
        eco_claw = self._supervision_factory.get_claw("ecosystem")
        if not eco_claw:
            return None
        
        supervision_claws = _get_supervision_claws()
        
        try:
            loop = asyncio.new_event_loop()
            
            # 系统健康度影响监管级别
            health = ecosystem_context.get("overall_health", "good")
            if health in ("poor", "critical"):
                level = supervision_claws['SupervisionLevel'].HARSH
            elif health == "fair":
                level = supervision_claws['SupervisionLevel'].NORMAL
            else:
                level = supervision_claws['SupervisionLevel'].MILD
            
            context = {
                "task_id": "ecosystem_check",
                "result": {
                    "confidence": analysis.get("confidence", 0.5),
                    "ecosystem_health": health,
                    "alerts_count": ecosystem_context.get("alerts_count", 0),
                    "resource_suggestions": ecosystem_context.get("resource_suggestions", []),
                }
            }
            
            record = loop.run_until_complete(eco_claw.supervise(
                target="SYSTEM_ECOSYSTEM",
                context=context,
                level=level,
            ))
            record_id = record.id if hasattr(record, 'id') else str(id(record))
            loop.close()
            
            report = SupervisionReport(
                id=record_id,
                timestamp=datetime.now().isoformat(),
                target_claw="SYSTEM_ECOSYSTEM",
                target_task="ecosystem_supervision",
                supervision_type="ecosystem",
                level=level.value,
                message=f"生态监管: 健康度={health}, "
                        f"警报数={ecosystem_context.get('alerts_count', 0)}",
            )
            self.supervision_reports.append(report)
            
            return report
        except Exception as e:
            logger.warning(f"[A轨] 生态监管Claw监督失败: {e}")
            return None

    def _record_evolution(
        self,
        analysis: Dict[str, Any],
        result: Dict[str, Any],
    ) -> None:
        """
        演化记录 — 将任务执行结果注入演化引擎
        
        v3.0 新增：每次任务完成后，将关键指标记录到 EvolutionEngine，
        支持多代演化追踪和长期趋势分析。
        v3.1 升级：EvolutionEngine 自动执行策略（declining趋势触发）
        """
        if self._ecosystem is None:
            return
        
        try:
            # 构建演化状态
            evolution_state = {
                "task_confidence": analysis.get("confidence", 0.5),
                "result_accepted": result.get("accepted", False),
                "result_quality": 1.0 if result.get("quality") == "good" else 0.5,
            }
            
            # 如果有生态监控数据，也加入演化
            if self._ecosystem_last_monitor:
                eco_report = self._ecosystem_last_monitor.get("ecosystem_report", {})
                metrics = eco_report.get("metrics", {})
                for metric_name, metric_data in metrics.items():
                    if isinstance(metric_data, dict) and "value" in metric_data:
                        evolution_state[f"eco_{metric_name}"] = metric_data["value"]
            
            # v3.1: evolve 现在会自动执行策略
            improvements = self._ecosystem.evolve(evolution_state)
            
            # 记录自动执行的策略到监管报告
            actions = improvements.get("actions_taken", [])
            if actions:
                for action in actions:
                    self._daemon_actions.append({
                        "detail": action.get("detail", ""),
                        "data": action,
                        "timestamp": time.time(),
                    })
                    report = SupervisionReport(
                        id=f"EVOLUTION_{action.get('strategy_id', '')}",
                        timestamp=datetime.now().isoformat(),
                        target_claw="EVOLUTION_ENGINE",
                        target_task="auto_strategy",
                        supervision_type="ecosystem",
                        level="warning",
                        message=f"[演化策略] {action.get('strategy_name', '')}: "
                                f"{action.get('detail', '')}",
                    )
                    self.supervision_reports.append(report)
        except Exception as e:
            logger.debug(f"[A轨] 演化记录失败: {e}")

    # ══════════════════════════════════════════════════════════════════════════
    # 资源管理（v3.1 新增）
    # ══════════════════════════════════════════════════════════════════════════

    def _release_task_resources(self, task_id: str) -> None:
        """
        释放任务占用的全部资源 (v3.1新增)

        任务完成后自动调用，确保资源及时归还。
        """
        if self._ecosystem is None:
            return

        try:
            released = self._ecosystem.resource_optimizer.release_resource(task_id)
            if released > 0:
                logger.info(f"[A轨] 任务 {task_id} 释放资源: {released:.0f}")
        except Exception as e:
            logger.debug(f"[A轨] 资源释放失败: {e}")

    # ══════════════════════════════════════════════════════════════════════════
    # v3.2: 系统压力门控 + 生态驱动决策 + 真实资源分配
    # ══════════════════════════════════════════════════════════════════════════

    def _system_pressure_gate(
        self,
        query: str,
        ecosystem_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        系统压力门控 (v3.2新增)

        当 Daemon 检测到系统压力危急时, 阻止低优先级任务进入。
        高优先级任务 (urgency=high) 始终放行。

        Returns:
            {"blocked": bool, "reason": str, "pressure": dict}
        """
        if self._ecosystem is None or not self._ecosystem.daemon_running:
            return {"blocked": False, "reason": "no_daemon"}

        daemon = self._ecosystem._daemon

        # 判断任务优先级
        task_priority = 5
        if ecosystem_context.get("overall_health") in ("poor", "critical"):
            # 系统不健康时, 只有高紧迫度的任务才高优先级
            task_priority = 8 if "紧急" in query or "重要" in query else 3
        else:
            task_priority = 7 if "紧急" in query or "重要" in query else 5

        gate = daemon.should_block_task(task_priority)
        if gate["should_block"]:
            report = SupervisionReport(
                id=f"GATE_BLOCKED_{int(time.time())}",
                timestamp=datetime.now().isoformat(),
                target_claw="SYSTEM",
                target_task="pressure_gate",
                supervision_type="ecosystem",
                level="warning",
                message=f"[压力门控] 任务被拒绝: {gate['reason']}",
            )
            self.supervision_reports.append(report)
            logger.warning(f"[A轨] 压力门控拒绝任务: {gate['reason']}")

        return gate

    def _ecosystem_driven_adjustment(
        self,
        analysis: Dict[str, Any],
        ecosystem_context: Dict[str, Any],
    ) -> None:
        """
        生态快照驱动决策 (v3.2新增)

        根据系统健康度动态调整任务处理策略:
        - 危急: 提高质量门槛, 缩短超时, 启用轻量模式
        - 一般: 正常处理
        - 良好: 正常处理 + 可接受更多任务
        """
        if not ecosystem_context.get("available"):
            return

        health = ecosystem_context.get("overall_health", "good")
        has_critical = ecosystem_context.get("has_critical_alerts", False)

        if health == "critical":
            # 危急模式
            analysis["quality_threshold"] = 0.85  # 提高质量门槛
            analysis["execution_timeout"] = 15.0  # 缩短超时
            analysis["mode"] = "lightweight"       # 轻量模式
            analysis["skip_ecosystem_supervision"] = True  # 跳过重复生态检查
            logger.info("[A轨] 生态危急模式: 提高质量门槛+缩短超时+轻量模式")
        elif health == "poor" or has_critical:
            # 较差模式
            analysis["quality_threshold"] = 0.75
            analysis["execution_timeout"] = 20.0
            analysis["mode"] = "cautious"
            logger.info("[A轨] 生态较差模式: 审慎处理")
        elif health == "fair":
            # 一般模式
            analysis["quality_threshold"] = 0.65
            analysis["execution_timeout"] = 30.0
            analysis["mode"] = "normal"
        else:
            # 良好/优秀模式
            analysis["quality_threshold"] = 0.50
            analysis["execution_timeout"] = 30.0
            analysis["mode"] = "normal"

        # 资源建议
        suggestions = ecosystem_context.get("resource_suggestions", [])
        if suggestions:
            analysis["resource_warnings"] = suggestions

    def _allocate_task_resources(
        self,
        task_id: str,
        priority: int = 5,
    ) -> Dict[str, Any]:
        """
        为任务分配资源 (v3.2新增)

        在任务派发到B轨之前, 预分配基础资源。
        分配失败时返回建议(降级或拒绝)。

        Returns:
            {"success": bool, "suggestion": str, "detail": dict}
        """
        if self._ecosystem is None:
            return {"success": True, "suggestion": "no_ecosystem", "detail": {}}

        # src/ecology/ 已移除，以下为历史代码（不可达）
        try:
            opt = self._ecosystem.resource_optimizer

            # 先刷新真实系统占用
            opt.refresh_totals()

            # 计算基础资源需求
            resource_requests = []
            for rtype in [ResourceType.CPU, ResourceType.MEMORY]:
                if rtype in opt.resources:
                    alloc = opt.resources[rtype]
                    # 基础需求 = 总量的 2%
                    base_amount = alloc.total * 0.02

                    # 如果系统已经很高负载, 减少分配
                    if alloc.effective_scarcity > 0.8:
                        base_amount *= 0.5  # 减半

                    resource_requests.append({
                        "resource_type": rtype,
                        "amount": base_amount,
                    })

            # 批量分配 (原子操作)
            results = opt.allocate_resources_bulk(task_id, resource_requests, priority)

            all_ok = all(results.values())
            suggestion = "normal" if all_ok else (
                "reject" if not any(results.values()) else "degraded"
            )

            return {
                "success": all_ok,
                "suggestion": suggestion,
                "detail": results,
                "effective_scarcity": {
                    rt.value: alloc.effective_scarcity
                    for rt, alloc in opt.resources.items()
                },
            }
        except Exception as e:
            logger.warning(f"[A轨] 资源分配失败: {e}")
            return {"success": True, "suggestion": "fallback_no_alloc", "detail": {"error": str(e)}}

    # ══════════════════════════════════════════════════════════════════════════
    # 后台监控管理（v3.1 新增）
    # ══════════════════════════════════════════════════════════════════════════

    def start_monitoring(
        self,
        interval: float = 5.0,
        alert_callback: Optional[Callable] = None,
    ) -> Dict[str, Any]:
        """
        启动后台持续监控 (v3.1新增)

        启动 EcosystemDaemon 守护线程, 持续采集系统资源,
        超阈值自动告警 + 趋势分析 + 自动策略执行。

        Args:
            interval: 采样间隔 (秒), 默认5s
            alert_callback: 外部告警回调 (event_dict) -> None

        Returns:
            启动结果
        """
        self._init_ecosystem()

        if self._ecosystem is None:
            return {"success": False, "reason": "ecosystem_not_available"}

        if alert_callback:
            self._on_resource_alert = alert_callback

        started = self._ecosystem.start_daemon(interval=interval)

        if started:
            # 注册回调
            self._setup_daemon_callbacks()
            return {
                "success": True,
                "interval": interval,
                "message": f"后台监控已启动 (间隔={interval}s)",
            }
        else:
            return {"success": False, "reason": "daemon_already_running"}

    def stop_monitoring(self) -> Dict[str, Any]:
        """
        停止后台持续监控 (v3.1新增)

        Returns:
            停止结果 + 运行统计
        """
        if self._ecosystem is None:
            return {"success": False, "reason": "ecosystem_not_available"}

        stopped = self._ecosystem.stop_daemon()

        result = {
            "success": stopped,
            "total_alerts_received": len(self._daemon_alerts),
            "total_actions_executed": len(self._daemon_actions),
            "message": "后台监控已停止" if stopped else "无运行中的监控",
        }

        if stopped:
            self._setup_daemon_callbacks()  # 清理回调

        return result

    def get_monitoring_status(self) -> Dict[str, Any]:
        """
        获取后台监控状态 (v3.1新增)

        Returns:
            Daemon状态 + 当前读数 + 最近告警
        """
        if self._ecosystem is None or not self._ecosystem.daemon_running:
            return {
                "running": False,
                "alerts_received": len(self._daemon_alerts),
                "actions_executed": len(self._daemon_actions),
            }

        dashboard = self._ecosystem._daemon.get_dashboard()
        dashboard["alerts_received"] = len(self._daemon_alerts)
        dashboard["actions_executed"] = len(self._daemon_actions)
        dashboard["recent_alerts_detail"] = self._daemon_alerts[-10:]
        dashboard["recent_actions_detail"] = self._daemon_actions[-10:]

        return dashboard

    def get_monitoring_alerts(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取后台监控产生的告警"""
        return self._daemon_alerts[-limit:]

    def get_monitoring_actions(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取后台监控触发的策略执行"""
        return self._daemon_actions[-limit:]

    def monitor_system(self) -> Dict[str, Any]:
        """
        【系统级监管接口】全面监控生态系统
        
        神政轨的核心升级：从任务级监管扩展到系统级全局监管。
        对外暴露的接口，可被外部系统调用获取完整生态报告。
        
        Returns:
            完整生态系统报告
        """
        self._init_ecosystem()
        
        if self._ecosystem is None:
            return {
                "success": False,
                "reason": "ecosystem_not_available",
                "track": "A",
                "role": "governance",
            }
        
        try:
            full_monitor = self._ecosystem.monitor()
            
            # 补充监管维度的信息
            full_monitor["governance_context"] = {
                "track": "A",
                "role": "system_governance",
                "monitor_count": self._ecosystem_monitor_count,
                "supervision_reports_count": len(self.supervision_reports),
                "active_assignments": len([
                    a for a in self.assignments.values() if a.status == "running"
                ]),
            }
            
            # 补充演化引擎报告
            try:
                full_monitor["evolution_report"] = self._ecosystem.evolution_engine.get_evolution_report()
            except Exception:
                pass
            
            full_monitor["success"] = True
            return full_monitor
        except Exception as e:
            logger.error(f"[A轨] 系统监控失败: {e}")
            return {"success": False, "error": str(e)}

    def check_ecosystem_health(self) -> Dict[str, Any]:
        """
        【系统级监管接口】快速检查生态健康度
        
        轻量级接口，只返回健康状态概览。
        
        Returns:
            健康状态概览 dict
        """
        self._init_ecosystem()
        
        if self._ecosystem is None:
            return {
                "overall": "unknown",
                "available": False,
                "reason": "ecosystem_not_available",
            }
        
        try:
            report = self._ecosystem.ecosystem_manager.generate_report()
            return {
                "overall": report.get("overall_health", "unknown"),
                "balanced": report.get("balance_status", False),
                "metrics_count": len(report.get("metrics", {})),
                "alerts": report.get("alerts", []),
                "available": True,
            }
        except Exception as e:
            return {"overall": "error", "available": False, "error": str(e)}

    def optimize_resources(self, task_id: str, resource_type: str = "cpu", amount: float = 10.0, priority: int = 5) -> Dict[str, Any]:
        """
        【系统级监管接口】资源优化分配
        
        利用 ResourceOptimizer 进行优先级抢占式资源分配。
        神政轨作为监管方，根据生态状态决定资源分配策略。
        
        Args:
            task_id: 任务ID
            resource_type: 资源类型 (cpu/memory/storage/network/token/time)
            amount: 需要量
            priority: 优先级 (1-10, 10最高)
            
        Returns:
            分配结果
        """
        self._init_ecosystem()
        
        if self._ecosystem is None:
            return {"success": False, "reason": "ecosystem_not_available"}
        
        # src/ecology/ 已移除，以下为历史不可达代码
        try:
            rt_map = {
                "cpu": None,
                "memory": None,
                "storage": None,
                "network": None,
                "token": None,
                "time": None,
            }
            rt = None
            
            allocated = self._ecosystem.resource_optimizer.allocate_resource(
                task_id=task_id,
                resource_type=rt,
                amount=amount,
                priority=priority,
            )
            
            return {
                "success": allocated,
                "task_id": task_id,
                "resource_type": resource_type,
                "amount": amount,
                "priority": priority,
            }
        except Exception as e:
            logger.error(f"[A轨] 资源分配失败: {e}")
            return {"success": False, "error": str(e)}

    def release_resources(self, task_id: str, resource_type: str = "cpu") -> Dict[str, Any]:
        """
        【系统级监管接口】释放资源
        
        任务完成后释放占用资源。
        """
        self._init_ecosystem()
        
        if self._ecosystem is None:
            return {"success": False, "reason": "ecosystem_not_available"}
        
        # src/ecology/ 已移除，以下为历史不可达代码
        try:
            rt_map = {
                "cpu": None,
                "memory": None,
                "storage": None,
                "network": None,
                "token": None,
                "time": None,
            }
            rt = None
            
            self._ecosystem.resource_optimizer.release_resource(task_id, rt)
            
            return {"success": True, "task_id": task_id, "resource_type": resource_type}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_resource_utilization(self) -> Dict[str, Any]:
        """
        【系统级监管接口】获取资源利用率报告
        
        Returns:
            各资源类型的利用率、可用量、稀缺度
        """
        self._init_ecosystem()
        
        if self._ecosystem is None:
            return {"success": False, "reason": "ecosystem_not_available"}
        
        try:
            return self._ecosystem.resource_optimizer.get_utilization_report()
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_evolution_report(self) -> Dict[str, Any]:
        """
        【系统级监管接口】获取演化报告
        
        Returns:
            演化趋势、改进建议、历史数据
        """
        self._init_ecosystem()
        
        if self._ecosystem is None:
            return {"success": False, "reason": "ecosystem_not_available"}
        
        try:
            report = self._ecosystem.evolution_engine.get_evolution_report()
            report["success"] = True
            return report
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ══════════════════════════════════════════════════════════════════════════
    # 状态查询
    # ══════════════════════════════════════════════════════════════════════════
    
    def get_status(self) -> Dict[str, Any]:
        """获取A轨状态"""
        status = {
            "track": "A",
            "name": "神政轨",
            "role": "监管",
            "version": "v3.2.0",
            "active_assignments": len([a for a in self.assignments.values() if a.status == "running"]),
            "total_assignments": len(self.assignments),
            "track_b_connected": self._track_b is not None,
            "supervision_reports_count": len(self.supervision_reports),
        }

        # 监管系统状态
        if self._supervision_factory:
            status["supervision"] = self._supervision_factory.get_status()

            # 列出每个Claw的详细信息
            claws_detail = []
            for claw in self._supervision_factory.get_all_claws():
                claws_detail.append({
                    "name": claw.name,
                    "position": claw.position,
                    "title": claw.title,
                    "mode": "wiseone" if claw.has_wiseone_power else "internal",
                    "wiseone": claw.appointment.claw_name if claw.appointment else None,
                    "stats": claw.get_status()["stats"],
                    "thinking_depth": len(claw.thinking_chain),
                })
            status["supervision_claws"] = claws_detail

        if self._jindu_engine:
            status["jindu"] = self._jindu_engine.get_stats()

        if self._whiplash_engine:
            status["whiplash"] = self._whiplash_engine.get_stats()

        if self._memory_interface:
            status["neural_memory"] = "connected"

        # ── v3.0: 生态引擎状态 ──
        status["ecosystem"] = {
            "available": self._ecosystem is not None,
            "monitor_count": self._ecosystem_monitor_count,
            "last_health": self._quick_ecosystem_check().get("overall_health", "unknown")
            if self._ecosystem else "not_initialized",
        }

        # ── v3.1: 后台监控状态 ──
        status["monitoring"] = {
            "daemon_running": self._ecosystem.daemon_running if self._ecosystem else False,
            "alerts_received": len(self._daemon_alerts),
            "actions_executed": len(self._daemon_actions),
            "resource_allocations": (
                len(self._ecosystem.resource_optimizer.allocations)
                if self._ecosystem else 0
            ),
            "reclamation_events": (
                len(self._ecosystem.resource_optimizer.reclamation_events)
                if self._ecosystem else 0
            ),
        }

        return status

    def get_supervision_history(self, limit: int = 20) -> List[Dict]:
        """获取监管历史"""
        reports = self.supervision_reports[-limit:]
        return [
            {
                "id": r.id,
                "timestamp": r.timestamp,
                "target": r.target_claw,
                "task": r.target_task,
                "type": r.supervision_type,
                "level": r.level,
                "message": r.message,
            }
            for r in reports
        ]


# ══════════════════════════════════════════════════════════════════════════════
# 便捷函数
# ══════════════════════════════════════════════════════════════════════════════

def create_divine_governance_track() -> DivineGovernanceTrack:
    """创建神政轨实例"""
    return DivineGovernanceTrack()


__all__ = [
    'DivineGovernanceTrack',
    'TaskAssignment',
    'SupervisionReport',
    'create_divine_governance_track',
    # v3.0 生态引擎懒加载入口
    '_get_ecosystem_intelligence',
]
