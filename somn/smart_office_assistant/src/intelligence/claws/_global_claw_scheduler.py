# -*- coding: utf-8 -*-
"""
GlobalClawScheduler - 全局Claw调度器
=====================================

V1.0.0: Claw任职体系的代码级全局调度实现。

统一调度763个贤者Claw的四大能力：
1. 全局调动 — 从SomnCore统一调度任意Claw，支持ProblemType/Department/School/Name四种路由
2. 分布式工作 — 任务队列 + 工作池，批量并发分发，支持优先级和超时
3. 独立工作 — 单Claw自主执行，ReAct闭环，完整生命周期管理
4. 协作工作 — 多Claw协作协议，角色分工（PRIMARY/CONTRIBUTOR/ADVISOR/REVIEWER），结果聚合

架构位置:
  SomnCore.global_claw_scheduler → GlobalClawScheduler
      │
      ├── ClawRouter          (route_by_department/problem_type/query/name)
      ├── ClawsCoordinator    (process / process_batch)
      ├── ClawSystemBridge    (dispatch / dispatch_batch)
      ├── CollaborationProtocol (execute_collaboration / discover_collaborators)
      └── CourtPositionRegistry (岗位信息 / 部门映射)

数据流:
  用户请求/系统调度 → GlobalClawScheduler
      │
      ├── 单Claw独立工作: dispatch_single(name, query) → ClawArchitect.process()
      ├── 多Claw协作工作: dispatch_collaborative(query, names) → CollaborationProtocol
      ├── 批量分布式工作: dispatch_distributed(tasks[]) → asyncio.gather + semaphore
      └── 全局调度: dispatch(request) → 自动路由 → 最优执行策略

版本: v1.0.0
创建: 2026-04-23
"""

from __future__ import annotations

import asyncio
import logging
import time
import uuid
from typing import Dict, List, Optional, Any, Callable, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════

class DispatchMode(Enum):
    """调度模式"""
    SINGLE = "single"                   # 单Claw独立工作
    COLLABORATIVE = "collaborative"     # 多Claw协作工作
    DISTRIBUTED = "distributed"         # 批量分布式工作
    AUTO = "auto"                       # 自动选择最优模式


class TaskPriority(Enum):
    """任务优先级"""
    CRITICAL = 0    # 紧急（立即执行）
    HIGH = 1        # 高
    NORMAL = 2      # 普通
    LOW = 3         # 低
    BACKGROUND = 4  # 后台


class ClawWorkMode(Enum):
    """Claw工作模式"""
    INDEPENDENT = "independent"       # 独立工作（ReAct闭环）
    PRIMARY = "primary"               # 主Claw（协作统筹）
    CONTRIBUTOR = "contributor"       # 贡献者
    ADVISOR = "advisor"               # 顾问
    REVIEWER = "reviewer"             # 审核者
    TASK_AGENT = "task_agent"        # 独立子Agent（异步/隔离会话/嵌套调度）


@dataclass
class TaskTicket:
    """
    任务票据 — 全局调度的核心数据结构。
    
    每个被调度到Claw的任务都有一个TaskTicket，
    记录完整的生命周期：创建→分配→执行→完成/失败。
    """
    task_id: str
    query: str
    target_claw: Optional[str] = None
    mode: DispatchMode = DispatchMode.AUTO
    priority: TaskPriority = TaskPriority.NORMAL
    collaborators: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    
    # ProblemType / Department / WisdomSchool 路由信息
    problem_type: Optional[str] = None
    department: Optional[str] = None
    wisdom_school: Optional[str] = None
    
    # 执行控制
    timeout_seconds: float = 120.0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    
    # 结果
    success: bool = False
    answer: str = ""
    error: str = ""
    elapsed_seconds: float = 0.0
    confidence: float = 0.0
    claw_used: str = ""
    collaborators_used: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @staticmethod
    def create(
        query: str,
        target_claw: Optional[str] = None,
        **kwargs,
    ) -> "TaskTicket":
        """快捷创建任务票据"""
        return TaskTicket(
            task_id=f"task_{uuid.uuid4().hex[:12]}",
            query=query,
            target_claw=target_claw,
            **kwargs,
        )


@dataclass
class SchedulerStats:
    """调度器统计信息"""
    total_dispatched: int = 0
    total_completed: int = 0
    total_failed: int = 0
    total_collaborative: int = 0
    total_distributed: int = 0
    total_single: int = 0
    avg_response_time: float = 0.0
    claw_usage_counts: Dict[str, int] = field(default_factory=dict)
    department_usage_counts: Dict[str, int] = field(default_factory=dict)
    active_tasks: int = 0
    pending_tasks: int = 0
    pool_size: int = 0


@dataclass
class WorkPoolStatus:
    """工作池状态"""
    total_claws: int = 0
    loaded_claws: int = 0
    active_claws: int = 0
    departments: Dict[str, int] = field(default_factory=dict)
    schools: Dict[str, int] = field(default_factory=dict)
    top_busy: List[Tuple[str, int]] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════
# GlobalClawScheduler 核心调度器
# ═══════════════════════════════════════════════════════════════

class GlobalClawScheduler:
    """
    全局Claw调度器 V1.0.0
    
    统一调度763个贤者Claw，提供：
    1. 全局调动 — 四种路由策略（ProblemType/Department/School/Name）
    2. 分布式工作 — 任务队列+工作池+并发控制
    3. 独立工作 — 单Claw ReAct闭环执行
    4. 协作工作 — 多Claw角色分工+结果聚合
    
    用法:
        >>> scheduler = GlobalClawScheduler()
        >>> await scheduler.initialize()
        
        # 全局调度（自动路由）
        >>> ticket = await scheduler.dispatch(TaskTicket.create("什么是仁？"))
        
        # 独立工作
        >>> ticket = await scheduler.dispatch_single("孔子", "什么是仁？")
        
        # 协作工作
        >>> ticket = await scheduler.dispatch_collaborative(
        ...     "如何治理国家", ["孔子", "管仲", "韩非子"]
        ... )
        
        # 分布式工作
        >>> tickets = await scheduler.dispatch_distributed([
        ...     TaskTicket.create("什么是仁？"),
        ...     TaskTicket.create("什么是道？"),
        ...     TaskTicket.create("什么是法？"),
        ... ])
    """
    
    # ── 超时与并发配置（与TimeoutGuard分级对齐 v1.0）──
    # TimeoutGuard分级: L1=30s, L2=60s, L3=120s, L4=180s
    # GCS场景映射: 单Claw→L3(120), 协作→L4(180), 批量总控→L4(180), 分布单项→L2.5(90)
    SINGLE_TIMEOUT = 120.0          # 单Claw执行超时 → L3-SLOW
    COLLABORATIVE_TIMEOUT = 180.0   # 协作执行超时 → L4-CRITICAL（原300s下调）
    DISTRIBUTED_BATCH_TIMEOUT = 180.0  # 批量分发总超时 → L4-CRITICAL（原600s大幅下调）
    DEFAULT_MAX_CONCURRENT = 5      # 默认最大并发数
    MAX_CONCURRENT_LIMIT = 20       # 最大并发上限
    CLAW_PER_ITEM_TIMEOUT = 90.0    # 分布式单项超时 → L2-L3之间
    
    def __init__(self, max_concurrent: Optional[int] = None):
        """
        Args:
            max_concurrent: 最大并发Claw数（None=使用默认值5）
        """
        self._max_concurrent = min(
            max_concurrent or self.DEFAULT_MAX_CONCURRENT,
            self.MAX_CONCURRENT_LIMIT,
        )
        
        # 子系统引用（延迟初始化）
        self._claw_router = None
        self._coordinator = None
        self._bridge = None
        self._collaboration_protocol = None
        self._position_registry = None
        
        # 状态
        self._initialized = False
        self._semaphore: Optional[asyncio.Semaphore] = None
        self._stats = SchedulerStats(pool_size=self._max_concurrent)
        
        # 任务追踪
        self._active_tickets: Dict[str, TaskTicket] = {}
        self._completed_tickets: List[TaskTicket] = []
        self._max_history = 1000
        
        # 回调钩子
        self._on_task_start: List[Callable] = []
        self._on_task_complete: List[Callable] = []
        self._on_task_fail: List[Callable] = []
        
        # 线程池（用于同步环境下的异步调用）
        self._thread_pool: Optional[ThreadPoolExecutor] = None
    
    # ═════════════════════════════════════════════════════════
    # 初始化
    # ═════════════════════════════════════════════════════════
    
    async def initialize(self) -> Dict[str, Any]:
        """
        初始化全局调度器。
        
        加载所有子系统：
        - ClawRouter（776个YAML配置索引）
        - ClawsCoordinator（Claw实例管理）
        - CollaborationProtocol（协作协议）
        - CourtPositionRegistry（岗位信息）
        
        Returns:
            初始化结果统计
        """
        if self._initialized:
            return {"status": "already_initialized"}
        
        start_time = time.monotonic()
        logger.info("[GlobalClawScheduler] 初始化全局Claw调度器...")
        
        results = {}
        
        # 1. 初始化 ClawRouter（轻量，仅建索引）
        try:
            from src.intelligence.dispatcher.wisdom_dispatch._dispatch_claw import (
                ClawRouter, get_claw_router,
            )
            self._claw_router = get_claw_router()
            self._claw_router.initialize()
            results["claw_router"] = {
                "total_claws": len(self._claw_router._claws),
                "departments": len(self._claw_router._department_claws),
                "schools": len(self._claw_router._school_claws),
            }
            logger.info(f"[GlobalClawScheduler] ClawRouter就绪: "
                        f"{results['claw_router']['total_claws']}个Claw")
        except Exception as e:
            logger.warning(f"[GlobalClawScheduler] ClawRouter初始化失败: {e}")
            results["claw_router"] = {"error": "调度失败"}
        
        # 2. 初始化 ClawsCoordinator（懒加载元数据模式）
        try:
            from src.intelligence.claws._claws_coordinator import ClawsCoordinator
            self._coordinator = ClawsCoordinator(
                max_concurrent=self._max_concurrent,
            )
            init_result = await self._coordinator.initialize(
                lazy_load=True,  # 懒加载：仅加载元数据，不创建实例
            )
            results["coordinator"] = init_result
            logger.info(f"[GlobalClawScheduler] ClawsCoordinator就绪: "
                        f"{init_result['loaded']}个Claw(懒加载)")
        except Exception as e:
            logger.warning(f"[GlobalClawScheduler] ClawsCoordinator初始化失败: {e}")
            results["coordinator"] = {"error": "调度失败"}
        
        # 3. 初始化 CollaborationProtocol
        try:
            from src.intelligence.dispatcher.wisdom_dispatch._dispatch_collaboration import (
                CollaborationProtocol,
            )
            self._collaboration_protocol = CollaborationProtocol(
                claw_router=self._claw_router,
            )
            results["collaboration"] = "ready"
            logger.info("[GlobalClawScheduler] CollaborationProtocol就绪")
        except Exception as e:
            logger.warning(f"[GlobalClawScheduler] CollaborationProtocol初始化失败: {e}")
            results["collaboration"] = {"error": "调度失败"}
        
        # 4. 初始化 CourtPositionRegistry（岗位信息）
        try:
            from src.intelligence.engines.cloning._court_positions import (
                CourtPositionRegistry,
            )
            self._position_registry = CourtPositionRegistry()
            results["positions"] = {
                "total_positions": len(self._position_registry._positions) if hasattr(self._position_registry, '_positions') else 0,
            }
            logger.info("[GlobalClawScheduler] CourtPositionRegistry就绪")
        except Exception as e:
            logger.warning(f"[GlobalClawScheduler] CourtPositionRegistry初始化失败: {e}")
            results["positions"] = {"error": "调度失败"}
        
        # 5. 创建信号量和线程池
        self._semaphore = asyncio.Semaphore(self._max_concurrent)
        self._thread_pool = ThreadPoolExecutor(
            max_workers=self._max_concurrent,
            thread_name_prefix="claw_dispatch",
        )
        
        self._initialized = True
        elapsed = time.monotonic() - start_time
        
        logger.info(f"[GlobalClawScheduler] 初始化完成，耗时 {elapsed:.2f}s")
        return {
            "status": "initialized",
            "elapsed_seconds": round(elapsed, 3),
            "max_concurrent": self._max_concurrent,
            **results,
        }
    
    def _ensure_initialized(self):
        """确保已初始化（同步检查）"""
        if not self._initialized:
            raise RuntimeError(
                "GlobalClawScheduler 未初始化。请先调用 await initialize()"
            )
    
    # ═════════════════════════════════════════════════════════
    # 核心调度入口
    # ═════════════════════════════════════════════════════════
    
    async def dispatch(self, ticket: TaskTicket) -> TaskTicket:
        """
        全局调度入口 — 自动选择最优执行模式。
        
        路由逻辑（优先级递减）:
        1. 如果指定了 target_claw → 独立工作
        2. 如果指定了 collaborators → 协作工作
        3. 如果指定了 problem_type/department → 路由后独立工作
        4. 默认 → 智能路由（ClawRouter自动匹配）
        
        Args:
            ticket: 任务票据
            
        Returns:
            已完成的任务票据（含结果）
        """
        self._ensure_initialized()
        self._stats.total_dispatched += 1
        self._stats.active_tasks += 1
        
        ticket.started_at = datetime.now().isoformat()
        self._active_tickets[ticket.task_id] = ticket
        
        # 触发前置回调
        for cb in self._on_task_start:
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb(ticket)
                else:
                    cb(ticket)
            except Exception:
                logger.debug("[GlobalClawScheduler] on_task_start回调失败")
        
        try:
            # ── 模式选择 ──
            if ticket.mode == DispatchMode.COLLABORATIVE or ticket.collaborators:
                result_ticket = await self.dispatch_collaborative_from_ticket(ticket)
            elif ticket.mode == DispatchMode.DISTRIBUTED:
                # 分布式模式不应通过dispatch入口调用
                raise ValueError("分布式模式请使用 dispatch_distributed() 方法")
            elif ticket.target_claw:
                result_ticket = await self.dispatch_single(ticket.target_claw, ticket.query, ticket)
            else:
                # 自动路由
                result_ticket = await self._auto_dispatch(ticket)
            
            # 更新统计
            self._stats.total_completed += 1
            self._stats.avg_response_time = (
                (self._stats.avg_response_time * (self._stats.total_completed - 1) + result_ticket.elapsed_seconds)
                / self._stats.total_completed
            )
            if result_ticket.claw_used:
                self._stats.claw_usage_counts[result_ticket.claw_used] = \
                    self._stats.claw_usage_counts.get(result_ticket.claw_used, 0) + 1
            
            # 记录历史
            self._completed_tickets.append(result_ticket)
            if len(self._completed_tickets) > self._max_history:
                self._completed_tickets = self._completed_tickets[-self._max_history:]
            
            return result_ticket
            
        except Exception as e:
            self._stats.total_failed += 1
            ticket.success = False
            ticket.error = "任务执行失败"
            ticket.completed_at = datetime.now().isoformat()
            
            # 触发失败回调
            for cb in self._on_task_fail:
                try:
                    if asyncio.iscoroutinefunction(cb):
                        await cb(ticket, e)
                    else:
                        cb(ticket, e)
                except Exception:
                    logger.debug("[GlobalClawScheduler] on_task_fail回调失败")
            
            return ticket
            
        finally:
            self._stats.active_tasks -= 1
            self._active_tickets.pop(ticket.task_id, None)
            
            # 触发完成回调
            for cb in self._on_task_complete:
                try:
                    if asyncio.iscoroutinefunction(cb):
                        await cb(ticket)
                    else:
                        cb(ticket)
                except Exception:
                    logger.debug("[GlobalClawScheduler] on_task_complete回调失败")
    
    async def _auto_dispatch(self, ticket: TaskTicket) -> TaskTicket:
        """
        自动路由：根据ProblemType/Department/Query自动选择最优Claw。
        
        路由策略:
        1. ProblemType → Department映射 → 部门内最优Claw
        2. Department → 部门内最优Claw
        3. Query → ClawRouter智能匹配
        """
        target = None
        
        # 策略1: ProblemType路由
        if ticket.problem_type and self._claw_router:
            route_result = self._claw_router.route_by_problem_type(
                ticket.problem_type, ticket.query,
            )
            target = route_result.primary_claw
            if route_result.collaborator_claws:
                ticket.collaborators = route_result.collaborator_claws[:3]
            
            # 记录部门统计
            dept = route_result.department
            self._stats.department_usage_counts[dept] = \
                self._stats.department_usage_counts.get(dept, 0) + 1
        
        # 策略2: Department路由
        elif ticket.department and self._claw_router:
            route_result = self._claw_router.route_by_department(
                ticket.department, ticket.query,
            )
            target = route_result.primary_claw
            self._stats.department_usage_counts[ticket.department] = \
                self._stats.department_usage_counts.get(ticket.department, 0) + 1
        
        # 策略3: WisdomSchool路由
        elif ticket.wisdom_school and self._coordinator:
            candidates = self._coordinator.find_by_school(ticket.wisdom_school)
            if candidates:
                target = candidates[0]
        
        # 策略4: Query智能匹配
        elif self._claw_router:
            route_result = self._claw_router.route_by_query(ticket.query)
            target = route_result.primary_claw
            if route_result.collaborator_claws:
                ticket.collaborators = route_result.collaborator_claws[:3]
        
        if not target:
            # 最终兜底：使用协调器的Gateway路由
            if self._coordinator:
                decision = self._coordinator.gateway.route(ticket.query)
                target = decision.primary
            else:
                target = "孔子"  # 终极兜底
        
        # 如果有协作者且协作子系统可用，升级为协作模式
        if (ticket.collaborators and len(ticket.collaborators) >= 1
                and self._collaboration_protocol):
            return await self.dispatch_collaborative_from_ticket(ticket)
        
        return await self.dispatch_single(target, ticket.query, ticket)
    
    # ═════════════════════════════════════════════════════════
    # 能力1: 独立工作（单Claw自主执行）
    # ═════════════════════════════════════════════════════════
    
    async def dispatch_single(
        self,
        claw_name: str,
        query: str,
        ticket: Optional[TaskTicket] = None,
        context: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> TaskTicket:
        """
        独立工作模式 — 指定单个Claw执行任务。
        
        完整的ReAct闭环执行：
        1. 确保目标Claw已加载（懒加载）
        2. 执行ReAct推理循环
        3. 返回完整结果
        
        Args:
            claw_name: 目标Claw名称（如"孔子"）
            query: 任务/问题
            ticket: 可选的任务票据（如果提供则更新而非创建）
            context: 额外上下文
            timeout: 超时（秒）
            
        Returns:
            已完成的任务票据
        """
        self._ensure_initialized()
        self._stats.total_single += 1
        
        if ticket is None:
            ticket = TaskTicket.create(
                query=query,
                target_claw=claw_name,
                mode=DispatchMode.SINGLE,
            )
        else:
            ticket.target_claw = claw_name
            ticket.mode = DispatchMode.SINGLE
        
        ticket.started_at = datetime.now().isoformat()
        
        actual_timeout = timeout or self.SINGLE_TIMEOUT
        
        try:
            # 确保目标Claw已加载
            claw = self._coordinator.get_claw(claw_name) if self._coordinator else None
            
            if claw is None:
                # 通过ClawSystemBridge分发
                if self._bridge:
                    from src.intelligence.claws._claw_bridge import DispatchRequest
                    dispatch_req = DispatchRequest(
                        query=query,
                        context=context,
                        metadata=ticket.metadata,
                    )
                    response = await asyncio.wait_for(
                        self._bridge.dispatch(dispatch_req),
                        timeout=actual_timeout,
                    )
                    ticket.success = response.success
                    ticket.answer = response.answer
                    ticket.claw_used = response.claw_name or claw_name
                    ticket.confidence = response.confidence
                    ticket.collaborators_used = response.collaborators
                    if not response.success:
                        ticket.error = response.error
                else:
                    raise ValueError(f"Claw '{claw_name}' 不可用且无ClawBridge")
            else:
                # 直接通过ClawArchitect执行
                result = await asyncio.wait_for(
                    claw.process(query, context),
                    timeout=actual_timeout,
                )
                ticket.success = result.success
                ticket.answer = result.final_answer
                ticket.claw_used = claw_name
                ticket.confidence = 1.0
                if not result.success:
                    ticket.error = result.reason
        
        except asyncio.TimeoutError:
            ticket.success = False
            ticket.error = f"独立工作超时({actual_timeout}s): {claw_name}"
            logger.warning(f"[GlobalClawScheduler] {ticket.error}")
        
        except Exception as e:
            ticket.success = False
            ticket.error = "独立工作异常"
            logger.warning(f"[GlobalClawScheduler] 独立工作异常({claw_name}): {e}")
        
        ticket.completed_at = datetime.now().isoformat()
        if ticket.started_at:
            try:
                started = datetime.fromisoformat(ticket.started_at)
                ticket.elapsed_seconds = (datetime.now() - started).total_seconds()
            except (ValueError, TypeError):
                pass
        
        return ticket
    
    # ═════════════════════════════════════════════════════════
    # 能力2: 协作工作（多Claw协作）
    # ═════════════════════════════════════════════════════════
    
    async def dispatch_collaborative(
        self,
        query: str,
        claw_names: List[str],
        roles: Optional[Dict[str, ClawWorkMode]] = None,
        context: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> TaskTicket:
        """
        协作工作模式 — 多Claw分工协作完成任务。
        
        工作流程:
        1. 主Claw(PRIMARY)执行核心分析
        2. 贡献者(CONTRIBUTOR)提供独立视角
        3. 顾问(ADVISOR)补充建议
        4. 审核者(REVIEWER)审查结果
        5. 结果聚合为统一输出
        
        Args:
            query: 任务/问题
            claw_names: 参与协作的Claw名称列表（第一个为主Claw）
            roles: 角色映射 {claw_name: ClawWorkMode}
            context: 额外上下文
            timeout: 超时（秒）
            
        Returns:
            已完成的任务票据
        """
        self._ensure_initialized()
        self._stats.total_collaborative += 1
        
        if not claw_names:
            raise ValueError("协作模式至少需要1个Claw")
        
        primary = claw_names[0]
        collaborators = claw_names[1:]
        
        ticket = TaskTicket.create(
            query=query,
            target_claw=primary,
            mode=DispatchMode.COLLABORATIVE,
            collaborators=collaborators,
        )
        
        # 转换角色格式
        role_map = None
        if roles:
            role_map = {}
            role_enum_map = {
                ClawWorkMode.PRIMARY: "PRIMARY",
                ClawWorkMode.CONTRIBUTOR: "CONTRIBUTOR",
                ClawWorkMode.ADVISOR: "ADVISOR",
                ClawWorkMode.REVIEWER: "REVIEWER",
            }
            for name, mode in roles.items():
                role_map[name] = role_enum_map.get(mode, "CONTRIBUTOR")
        
        return await self.dispatch_collaborative_from_ticket(
            ticket, roles=role_map, timeout=timeout,
        )
    
    async def dispatch_collaborative_from_ticket(
        self,
        ticket: TaskTicket,
        roles: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> TaskTicket:
        """
        从TaskTicket执行协作工作（内部方法）。
        
        Args:
            ticket: 任务票据（必须包含target_claw和collaborators）
            roles: 角色映射 {claw_name: "PRIMARY"/"CONTRIBUTOR"/"ADVISOR"/"REVIEWER"}
            timeout: 超时
            
        Returns:
            已完成的任务票据
        """
        self._ensure_initialized()
        self._stats.total_collaborative += 1
        
        primary = ticket.target_claw
        collaborators = ticket.collaborators
        actual_timeout = timeout or self.COLLABORATIVE_TIMEOUT
        
        ticket.started_at = datetime.now().isoformat()
        
        try:
            if self._collaboration_protocol and primary:
                # 使用CollaborationProtocol执行协作
                from src.intelligence.dispatcher.wisdom_dispatch._dispatch_collaboration import (
                    CollaborationRole,
                )
                
                # 转换角色
                collab_roles = None
                if roles:
                    collab_roles = {}
                    role_map = {
                        "PRIMARY": CollaborationRole.PRIMARY,
                        "CONTRIBUTOR": CollaborationRole.CONTRIBUTOR,
                        "ADVISOR": CollaborationRole.ADVISOR,
                        "REVIEWER": CollaborationRole.REVIEWER,
                    }
                    for name, role_str in roles.items():
                        collab_roles[name] = role_map.get(
                            role_str.upper(), CollaborationRole.CONTRIBUTOR
                        )
                
                result = await asyncio.wait_for(
                    self._collaboration_protocol.execute_collaboration(
                        primary_claw=primary,
                        query=ticket.query,
                        collaborators=collaborators,
                        roles=collab_roles,
                    ),
                    timeout=actual_timeout,
                )
                
                ticket.success = result.success
                ticket.answer = result.final_answer
                ticket.claw_used = primary
                ticket.collaborators_used = [
                    c.claw_name for c in result.contributions
                ]
                ticket.confidence = result.confidence
                if not result.success and result.errors:
                    ticket.error = "; ".join(result.errors[:3])
            
            elif self._coordinator and primary:
                # 回退到ClawsCoordinator的协作模式
                result = await asyncio.wait_for(
                    self._coordinator.process(
                        ticket.query,
                        target_claw=primary,
                        include_collaborators=True,
                        context=ticket.context,
                    ),
                    timeout=actual_timeout,
                )
                
                ticket.success = result.success
                if result.react_result:
                    ticket.answer = result.react_result.final_answer
                ticket.claw_used = result.routed_to
                ticket.collaborators_used = result.collaborators_used
                ticket.confidence = result.route_confidence
                if not result.success:
                    ticket.error = result.error
            
            else:
                raise RuntimeError("无可用的协作子系统")
        
        except asyncio.TimeoutError:
            ticket.success = False
            ticket.error = f"协作工作超时({actual_timeout}s)"
            logger.warning(f"[GlobalClawScheduler] {ticket.error}")
        
        except Exception as e:
            ticket.success = False
            ticket.error = "协作工作异常"
            logger.warning(f"[GlobalClawScheduler] 协作工作异常: {e}")
        
        ticket.completed_at = datetime.now().isoformat()
        if ticket.started_at:
            try:
                started = datetime.fromisoformat(ticket.started_at)
                ticket.elapsed_seconds = (datetime.now() - started).total_seconds()
            except (ValueError, TypeError):
                pass
        
        return ticket
    
    # ═════════════════════════════════════════════════════════
    # 能力3: 分布式工作（批量并发分发）
    # ═════════════════════════════════════════════════════════
    
    async def dispatch_distributed(
        self,
        tickets: List[TaskTicket],
        max_concurrent: Optional[int] = None,
        timeout_per_item: Optional[float] = None,
    ) -> List[TaskTicket]:
        """
        分布式工作模式 — 批量并发分发任务到工作池。
        
        特性:
        - 优先级调度（CRITICAL > HIGH > NORMAL > LOW > BACKGROUND）
        - 信号量控制并发数（防止过载）
        - 独立超时保护（单项超时不影响其他任务）
        - 整体批次超时保护
        
        Args:
            tickets: 任务票据列表
            max_concurrent: 最大并发数（None=使用默认值）
            timeout_per_item: 每个任务的独立超时（秒）
            
        Returns:
            已完成的任务票据列表（顺序与输入一致）
        """
        self._ensure_initialized()
        self._stats.total_distributed += len(tickets)
        
        if not tickets:
            return []
        
        actual_max_concurrent = min(
            max_concurrent or self._max_concurrent,
            self.MAX_CONCURRENT_LIMIT,
        )
        actual_timeout_per_item = timeout_per_item or self.CLAW_PER_ITEM_TIMEOUT
        
        sem = asyncio.Semaphore(actual_max_concurrent)
        
        # 按优先级排序（高优先级先执行）
        sorted_tickets = sorted(tickets, key=lambda t: t.priority.value)
        
        async def _process_one(ticket: TaskTicket) -> TaskTicket:
            """处理单个任务"""
            async with sem:
                try:
                    return await asyncio.wait_for(
                        self.dispatch(ticket),
                        timeout=actual_timeout_per_item,
                    )
                except asyncio.TimeoutError:
                    ticket.success = False
                    ticket.error = f"分布式单项超时({actual_timeout_per_item}s)"
                    ticket.completed_at = datetime.now().isoformat()
                    return ticket
                except Exception as e:
                    ticket.success = False
                    ticket.error = "分布式单项异常"
                    ticket.completed_at = datetime.now().isoformat()
                    return ticket
        
        # 并发执行所有任务（建立task→ticket_id映射）
        task_ticket_map: Dict[asyncio.Task, str] = {}
        ticket_id_map: Dict[str, TaskTicket] = {t.task_id: t for t in sorted_tickets}
        tasks = []
        for t in sorted_tickets:
            task = asyncio.create_task(_process_one(t))
            task_ticket_map[task] = t.task_id
            tasks.append(task)

        try:
            done, pending = await asyncio.wait(
                tasks,
                timeout=self.DISTRIBUTED_BATCH_TIMEOUT,
            )
            # 取消未完成的任务
            for p in pending:
                p.cancel()
            if pending:
                await asyncio.gather(*pending, return_exceptions=True)

            # 收集结果（保持原始顺序）
            result_map = {}
            for t in done:
                try:
                    tid = task_ticket_map[t]
                    result_map[tid] = t.result()
                except (asyncio.CancelledError, Exception):
                    pass

            # 按原始顺序返回
            ordered_results = []
            for ticket in tickets:
                if ticket.task_id in result_map:
                    ordered_results.append(result_map[ticket.task_id])
                else:
                    # 未完成的任务
                    ticket.success = False
                    ticket.error = f"批次超时({self.DISTRIBUTED_BATCH_TIMEOUT}s)"
                    ticket.completed_at = datetime.now().isoformat()
                    ordered_results.append(ticket)

            return ordered_results
            
        except Exception as e:
            logger.error(f"[GlobalClawScheduler] 分布式批次异常: {e}")
            # 返回错误结果
            for t in tickets:
                if not t.completed_at:
                    t.success = False
                    t.error = "分布式批次异常"
                    t.completed_at = datetime.now().isoformat()
            return tickets
    
    # ═════════════════════════════════════════════════════════
    # 能力4: 全局调动（统一调度接口）
    # ═════════════════════════════════════════════════════════
    
    async def dispatch_to_department(
        self,
        department: str,
        query: str,
        mode: DispatchMode = DispatchMode.AUTO,
        context: Optional[Dict[str, Any]] = None,
    ) -> TaskTicket:
        """
        按部门调度 — 将任务分发到指定部门的Claw。
        
        Args:
            department: 部门名称（如"礼部"、"兵部"、"户部"）
            query: 任务内容
            mode: 调度模式
            context: 额外上下文
        """
        self._ensure_initialized()
        
        ticket = TaskTicket.create(
            query=query,
            department=department,
            mode=mode,
        )
        
        if self._claw_router:
            route_result = self._claw_router.route_by_department(department, query)
            ticket.target_claw = route_result.primary_claw
            ticket.collaborators = route_result.collaborator_claws[:3]
            ticket.confidence = route_result.confidence
            ticket.metadata["routing_reason"] = route_result.routing_reason
        
        return await self.dispatch(ticket)
    
    async def dispatch_to_problem_type(
        self,
        problem_type: str,
        query: str,
        mode: DispatchMode = DispatchMode.AUTO,
        context: Optional[Dict[str, Any]] = None,
    ) -> TaskTicket:
        """
        按ProblemType调度 — 将任务分发到对应问题类型的Claw。
        
        Args:
            problem_type: 问题类型（如"MARKET_ANALYSIS"、"INNOVATION"）
            query: 任务内容
            mode: 调度模式
            context: 额外上下文
        """
        self._ensure_initialized()
        
        ticket = TaskTicket.create(
            query=query,
            problem_type=problem_type,
            mode=mode,
        )
        
        if self._claw_router:
            route_result = self._claw_router.route_by_problem_type(problem_type, query)
            ticket.target_claw = route_result.primary_claw
            ticket.collaborators = route_result.collaborator_claws[:3]
            ticket.department = route_result.department
            ticket.confidence = route_result.confidence
            ticket.metadata["routing_reason"] = route_result.routing_reason
        
        return await self.dispatch(ticket)
    
    async def dispatch_to_school(
        self,
        wisdom_school: str,
        query: str,
        mode: DispatchMode = DispatchMode.AUTO,
        context: Optional[Dict[str, Any]] = None,
    ) -> TaskTicket:
        """
        按学派调度 — 将任务分发到指定学派的Claw。
        
        Args:
            wisdom_school: 学派名称（如"儒家"、"道家"、"法家"）
            query: 任务内容
            mode: 调度模式
            context: 额外上下文
        """
        self._ensure_initialized()
        
        ticket = TaskTicket.create(
            query=query,
            wisdom_school=wisdom_school,
            mode=mode,
        )
        
        if self._coordinator:
            candidates = self._coordinator.find_by_school(wisdom_school)
            if candidates:
                ticket.target_claw = candidates[0]
                # 同学派取前2个作为协作者
                if len(candidates) > 1:
                    ticket.collaborators = candidates[1:3]
        
        return await self.dispatch(ticket)
    
    async def dispatch_to_claw(
        self,
        claw_name: str,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> TaskTicket:
        """
        直接调度到指定Claw — 独立工作模式的快捷入口。
        
        Args:
            claw_name: 目标Claw名称
            query: 任务内容
            context: 额外上下文
            timeout: 超时（秒）
        """
        return await self.dispatch_single(claw_name, query, context=context, timeout=timeout)
    
    # ═════════════════════════════════════════════════════════
    # 查询与监控
    # ═════════════════════════════════════════════════════════
    
    def get_stats(self) -> SchedulerStats:
        """获取调度器统计信息"""
        self._stats.active_tasks = len(self._active_tickets)
        self._stats.pending_tasks = max(0, self._stats.active_tasks)
        return self._stats
    
    def get_work_pool_status(self) -> WorkPoolStatus:
        """获取工作池状态"""
        status = WorkPoolStatus()
        
        if self._claw_router:
            status.total_claws = len(self._claw_router._claws)
            status.departments = dict(self._claw_router._department_claws) if self._claw_router._department_claws else {}
            # 将列表转换为计数
            status.departments = {
                dept: len(claws) for dept, claws in status.departments.items()
            }
            status.schools = dict(self._claw_router._school_claws) if self._claw_router._school_claws else {}
            status.schools = {
                school: len(claws) for school, claws in status.schools.items()
            }
        
        if self._coordinator:
            status.loaded_claws = len(self._coordinator.claws)
            status.active_claws = status.loaded_claws
        
        # Top使用频率
        top_usage = sorted(
            self._stats.claw_usage_counts.items(),
            key=lambda x: -x[1],
        )[:10]
        status.top_busy = top_usage
        
        return status
    
    def list_available_claws(
        self,
        department: Optional[str] = None,
        school: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        列出可用的Claw。
        
        Args:
            department: 按部门过滤
            school: 按学派过滤
            limit: 最大返回数量
        """
        if self._coordinator:
            return self._coordinator.list_claws(
                filter_school=school,
            )[:limit]
        elif self._claw_router:
            claws = list(self._claw_router._claws.values())
            if department:
                claws = [c for c in claws if c.department == department]
            if school:
                claws = [c for c in claws if c.school == school]
            return [
                {
                    "name": c.name,
                    "department": c.department,
                    "school": c.school,
                    "position": c.position_name,
                    "priority": c.priority_score,
                }
                for c in sorted(claws, key=lambda x: -x.priority_score)[:limit]
            ]
        return []
    
    def find_collaborators(
        self,
        primary_claw: str,
        query: str,
        max_count: int = 3,
    ) -> List[Tuple[str, ClawWorkMode]]:
        """
        发现可用的协作Claw。
        
        Args:
            primary_claw: 主Claw名称
            query: 问题内容
            max_count: 最大协作数量
            
        Returns:
            [(claw_name, role), ...]
        """
        if not self._collaboration_protocol:
            return []
        
        collaborators = self._collaboration_protocol.discover_collaborators(
            primary_claw=primary_claw,
            query=query,
            max_count=max_count,
        )
        
        # 转换为ClawWorkMode
        mode_map = {
            "primary": ClawWorkMode.PRIMARY,
            "contributor": ClawWorkMode.CONTRIBUTOR,
            "advisor": ClawWorkMode.ADVISOR,
            "reviewer": ClawWorkMode.REVIEWER,
        }
        
        from src.intelligence.dispatcher.wisdom_dispatch._dispatch_collaboration import (
            CollaborationRole,
        )
        
        return [
            (name, mode_map.get(
                role.value if isinstance(role, CollaborationRole) else str(role),
                ClawWorkMode.CONTRIBUTOR,
            ))
            for name, role in collaborators
        ]
    
    def get_active_tickets(self) -> List[Dict[str, Any]]:
        """获取当前活跃任务的快照"""
        return [
            {
                "task_id": t.task_id,
                "query": t.query[:50],
                "target_claw": t.target_claw,
                "mode": t.mode.value,
                "priority": t.priority.value,
                "started_at": t.started_at,
            }
            for t in self._active_tickets.values()
        ]
    
    def get_recent_results(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取最近的执行结果"""
        recent = self._completed_tickets[-limit:]
        return [
            {
                "task_id": t.task_id,
                "query": t.query[:50],
                "claw_used": t.claw_used,
                "success": t.success,
                "elapsed": round(t.elapsed_seconds, 2),
                "confidence": round(t.confidence, 2),
            }
            for t in reversed(recent)
        ]
    
    # ═════════════════════════════════════════════════════════
    # 同步包装器（供非async环境使用）
    # ═════════════════════════════════════════════════════════
    
    def dispatch_sync(self, ticket: TaskTicket) -> TaskTicket:
        """
        同步版本的dispatch（在非async环境使用）。
        
        使用ThreadPoolExecutor将异步调用包装为同步。
        """
        if self._thread_pool is None:
            self._thread_pool = ThreadPoolExecutor(max_workers=1)
        
        future = self._thread_pool.submit(
            asyncio.run, self.dispatch(ticket),
        )
        return future.result(timeout=self.COLLABORATIVE_TIMEOUT + 10)
    
    def dispatch_single_sync(
        self, claw_name: str, query: str, **kwargs,
    ) -> TaskTicket:
        """同步版本的单Claw调度"""
        if self._thread_pool is None:
            self._thread_pool = ThreadPoolExecutor(max_workers=1)
        
        future = self._thread_pool.submit(
            asyncio.run,
            self.dispatch_single(claw_name, query, **kwargs),
        )
        return future.result(timeout=self.SINGLE_TIMEOUT + 10)
    
    def dispatch_to_department_sync(
        self, department: str, query: str, **kwargs,
    ) -> TaskTicket:
        """同步版本的部门调度"""
        if self._thread_pool is None:
            self._thread_pool = ThreadPoolExecutor(max_workers=1)
        
        future = self._thread_pool.submit(
            asyncio.run,
            self.dispatch_to_department(department, query, **kwargs),
        )
        return future.result(timeout=self.COLLABORATIVE_TIMEOUT + 10)
    
    # ═════════════════════════════════════════════════════════
    # 生命周期管理
    # ═════════════════════════════════════════════════════════
    
    async def shutdown(self) -> Dict[str, Any]:
        """
        关闭调度器，释放资源。
        
        Returns:
            关闭统计
        """
        stats = self.get_stats()
        
        # 关闭线程池
        if self._thread_pool:
            self._thread_pool.shutdown(wait=False)
            self._thread_pool = None
        
        self._initialized = False
        
        logger.info(
            f"[GlobalClawScheduler] 已关闭: "
            f"{stats.total_dispatched}次调度, "
            f"{stats.total_completed}次完成, "
            f"{stats.total_failed}次失败"
        )
        
        return {
            "status": "shutdown",
            "total_dispatched": stats.total_dispatched,
            "total_completed": stats.total_completed,
            "total_failed": stats.total_failed,
            "avg_response_time": round(stats.avg_response_time, 3),
        }
    
    # ═════════════════════════════════════════════════════════
    # 回调注册
    # ═════════════════════════════════════════════════════════
    
    def on_task_start(self, callback: Callable) -> None:
        """注册任务开始回调"""
        self._on_task_start.append(callback)
    
    def on_task_complete(self, callback: Callable) -> None:
        """注册任务完成回调"""
        self._on_task_complete.append(callback)
    
    def on_task_fail(self, callback: Callable) -> None:
        """注册任务失败回调"""
        self._on_task_fail.append(callback)
    
    # ═════════════════════════════════════════════════════════
    # 能力5: 独立子Agent模式（异步启动/会话隔离/嵌套调度）
    # ═════════════════════════════════════════════════════════
    
    async def spawn_as_task(
        self,
        claw_name: str,
        query: str,
        background: bool = True,
        timeout: Optional[float] = None,
        context: Optional[Dict[str, Any]] = None,
        enable_nested: bool = True,
        on_complete: Optional[Callable] = None,
        on_error: Optional[Callable] = None,
    ) -> str:
        """
        将Claw作为独立子Agent启动（非阻塞异步执行）。
        
        核心能力:
        - 异步启动：立即返回task_id，不阻塞
        - 会话隔离：每个子Agent独立ClawContext
        - 嵌套调度：子Agent可继续调度其他Claw
        - 状态追踪：完整Task生命周期管理
        
        Args:
            claw_name: 目标Claw名称
            query: 任务内容
            background: 是否后台执行（True=异步立即返回）
            timeout: 超时秒数（None=继承默认值120s）
            context: 额外上下文
            enable_nested: 是否允许嵌套调度
            on_complete: 完成回调函数
            on_error: 错误回调函数
            
        Returns:
            task_id: 任务标识符
            
        用法:
            # 异步后台执行
            >>> task_id = await scheduler.spawn_as_task("孔子", "什么是仁？")
            >>> # 立即返回，可继续其他工作
            >>> status = scheduler.get_agent_task_status(task_id)
            
            # 同步等待结果
            >>> task_id = await scheduler.spawn_as_task("孔子", "什么是仁？", background=False)
            >>> result = await scheduler.wait_agent_task(task_id)
            
            # 带回调
            >>> def on_done(info):
            ...     print(f"Task完成: {info.result}")
            >>> task_id = await scheduler.spawn_as_task("孔子", "什么是仁？", on_complete=on_done)
        """
        self._ensure_initialized()
        
        # 延迟导入避免循环依赖
        from ._claw_agent_wrapper import (
            ClawAgentWrapper,
            SpawnOptions,
            get_global_agent_pool,
        )
        
        # 获取或创建Wrapper
        pool = get_global_agent_pool()
        wrapper = pool.get_wrapper(claw_name)
        
        # 构建选项
        options = SpawnOptions(
            background=background,
            timeout=timeout or self.SINGLE_TIMEOUT,
            enable_nested=enable_nested,
            on_complete=on_complete,
            on_error=on_error,
        )
        
        # Spawn
        task_id = await wrapper.spawn(query, options, context)

        # 如果非后台模式，等待完成
        if not background:
            await wrapper.wait_result(task_id, timeout)

        logger.info(
            f"[GlobalClawScheduler] 子Agent启动: {task_id} -> {claw_name} "
            f"(background={background})"
        )

        return task_id

    def get_agent_task_status(self, task_id: str) -> Optional[str]:
        """获取子Agent任务状态"""
        from ._claw_agent_wrapper import get_global_agent_pool

        pool = get_global_agent_pool()
        info = pool.get_task_info(task_id)

        if info:
            return info.status.value if hasattr(info.status, 'value') else str(info.status)
        return None

    def list_agent_tasks(
        self,
        status_filter: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """列出子Agent任务"""
        from ._claw_agent_wrapper import get_global_agent_pool

        pool = get_global_agent_pool()
        result = []

        for name, wrapper in pool._wrappers.items():
            for task_id, info in wrapper._tasks.items():
                if status_filter is None or info.status.value == status_filter:
                    result.append({
                        "task_id": task_id,
                        "claw_name": name,
                        "status": info.status.value,
                        "elapsed": info.elapsed_seconds,
                    })

        return result
    
    async def wait_agent_task(
        self,
        task_id: str,
        timeout: Optional[float] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        等待子Agent任务完成并返回结果。
        
        Args:
            task_id: 任务ID
            timeout: 等待超时
            
        Returns:
            任务结果字典，包含result/status/error/elapsed等信息
        """
        from ._claw_agent_wrapper import get_global_agent_pool
        
        pool = get_global_agent_pool()
        
        # 找到对应的wrapper
        claw_name = None
        for name, wrapper in pool._wrappers.items():
            if task_id in wrapper._tasks:
                claw_name = name
                break
        
        if not claw_name:
            return None
        
        wrapper = pool._wrappers[claw_name]
        info = await wrapper.wait_result(task_id, timeout)

        if info is None:
            return None

        return {
            "task_id": info.task_id,
            "claw_name": info.claw_name,
            "query": info.query,
            "status": info.status.value,
            "result": info.result,
            "error": info.error,
            "success": info.success,
            "confidence": info.confidence,
            "elapsed_seconds": info.elapsed_seconds,
            "steps_count": info.steps_count,
        }
    
    async def spawn_multi_agent_tasks(
        self,
        tasks: List[Dict[str, str]],  # [{"claw_name": "...", "query": "..."}, ...]
        background: bool = True,
        timeout: Optional[float] = None,
    ) -> List[str]:
        """
        批量启动多个子Agent任务。
        
        Args:
            tasks: 任务列表
            background: 是否后台执行
            timeout: 超时
            
        Returns:
            task_id列表
        """
        self._ensure_initialized()
        
        from ._claw_agent_wrapper import SpawnOptions, get_global_agent_pool
        
        pool = get_global_agent_pool()
        options = SpawnOptions(
            background=background,
            timeout=timeout or self.SINGLE_TIMEOUT,
        )
        
        return await pool.spawn_batch(
            tasks,
            options=options,
        )

    async def wait_multi_results(
        self,
        task_ids: List[str],
        timeout: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        批量等待多个任务完成。

        Args:
            task_ids: 任务ID列表
            timeout: 总体超时

        Returns:
            结果字典列表
        """
        pool = get_global_agent_pool()
        results = []

        for tid in task_ids:
            result = await self.wait_agent_task(tid, timeout)
            if result:
                results.append(result)

        return results

    async def shutdown(self) -> None:
        """
        清理所有子Agent资源。

        取消所有运行中的任务，清理全局池。
        """
        pool = get_global_agent_pool()

        # 取消所有运行中的任务
        for name, wrapper in pool._wrappers.items():
            for task_id in wrapper.list_active_tasks():
                await wrapper.cancel_task(task_id)

        # 清空全局池
        pool._wrappers.clear()
        pool._global_tasks.clear()

        logger.info("[GlobalClawScheduler] 子Agent资源已清理")


# ═══════════════════════════════════════════════════════════════
# 全局单例
# ═══════════════════════════════════════════════════════════════

_global_scheduler: Optional[GlobalClawScheduler] = None


def get_global_claw_scheduler() -> GlobalClawScheduler:
    """获取全局Claw调度器单例"""
    global _global_scheduler
    if _global_scheduler is None:
        _global_scheduler = GlobalClawScheduler()
    return _global_scheduler


async def ensure_global_scheduler() -> GlobalClawScheduler:
    """确保全局调度器已初始化（异步版本）"""
    scheduler = get_global_claw_scheduler()
    if not scheduler._initialized:
        await scheduler.initialize()
    return scheduler


def quick_dispatch(
    query: str,
    claw_name: Optional[str] = None,
    department: Optional[str] = None,
    problem_type: Optional[str] = None,
    wisdom_school: Optional[str] = None,
    collaborators: Optional[List[str]] = None,
) -> TaskTicket:
    """
    快捷调度函数（同步，用于简单场景）。
    
    Args:
        query: 任务内容
        claw_name: 指定Claw
        department: 指定部门
        problem_type: 指定问题类型
        wisdom_school: 指定学派
        collaborators: 协作Claw列表
    
    Returns:
        任务票据
    """
    scheduler = get_global_claw_scheduler()
    return scheduler.dispatch_sync(
        TaskTicket.create(
            query=query,
            target_claw=claw_name,
            department=department,
            problem_type=problem_type,
            wisdom_school=wisdom_school,
            collaborators=collaborators or [],
        )
    )


__all__ = [
    # 核心类
    "GlobalClawScheduler",
    "TaskTicket",
    "SchedulerStats",
    "WorkPoolStatus",
    # 枚举
    "DispatchMode",
    "TaskPriority",
    "ClawWorkMode",
    # 便捷函数
    "get_global_claw_scheduler",
    "ensure_global_scheduler",
    "quick_dispatch",
]
