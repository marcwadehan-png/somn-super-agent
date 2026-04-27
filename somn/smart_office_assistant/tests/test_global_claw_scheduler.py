# -*- coding: utf-8 -*-
"""
GlobalClawScheduler 测试套件
============================

验证全局Claw调度器的四大核心能力：
1. 初始化与配置
2. 独立工作（单Claw ReAct闭环）
3. 协作工作（多Claw角色分工）
4. 分布式工作（批量并发分发）
5. 全局调动（多种路由策略）
6. 同步包装器
7. 统计与监控
8. SomnCore集成

运行方式:
    python -m pytest tests/test_global_claw_scheduler.py -v
"""

import asyncio
import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, AsyncMock
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

# ── 路径设置 ──
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_src_path = str(_PROJECT_ROOT / "smart_office_assistant" / "src")
_sa_path = str(_PROJECT_ROOT / "smart_office_assistant")
if _src_path not in sys.path:
    sys.path.insert(0, _src_path)
if _sa_path not in sys.path:
    sys.path.insert(0, _sa_path)
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))


# ═══════════════════════════════════════════════════════════════
# 测试1: 数据结构
# ═══════════════════════════════════════════════════════════════

class TestDataStructures:
    """验证数据结构定义正确"""
    
    def test_task_ticket_create(self):
        """TaskTicket快捷创建"""
        from src.intelligence.claws._global_claw_scheduler import TaskTicket
        
        ticket = TaskTicket.create(
            query="什么是仁？",
            target_claw="孔子",
        )
        
        assert ticket.query == "什么是仁？"
        assert ticket.target_claw == "孔子"
        assert ticket.task_id.startswith("task_")
        assert ticket.success is False
        assert ticket.mode.value == "auto"
        assert len(ticket.task_id) == 17  # task_ + 12位hex
    
    def test_task_ticket_with_all_fields(self):
        """TaskTicket完整字段"""
        from src.intelligence.claws._global_claw_scheduler import (
            TaskTicket, DispatchMode, TaskPriority,
        )
        
        ticket = TaskTicket(
            task_id="test_001",
            query="如何治理国家",
            target_claw="管仲",
            mode=DispatchMode.COLLABORATIVE,
            priority=TaskPriority.HIGH,
            collaborators=["孔子", "韩非子"],
            problem_type="LEADERSHIP",
            department="吏部",
        )
        
        assert ticket.mode == DispatchMode.COLLABORATIVE
        assert ticket.priority == TaskPriority.HIGH
        assert len(ticket.collaborators) == 2
        assert ticket.problem_type == "LEADERSHIP"
    
    def test_dispatch_mode_enum(self):
        """DispatchMode枚举"""
        from src.intelligence.claws._global_claw_scheduler import DispatchMode
        
        assert DispatchMode.SINGLE.value == "single"
        assert DispatchMode.COLLABORATIVE.value == "collaborative"
        assert DispatchMode.DISTRIBUTED.value == "distributed"
        assert DispatchMode.AUTO.value == "auto"
    
    def test_task_priority_ordering(self):
        """TaskPriority优先级顺序"""
        from src.intelligence.claws._global_claw_scheduler import TaskPriority
        
        assert TaskPriority.CRITICAL.value < TaskPriority.HIGH.value
        assert TaskPriority.HIGH.value < TaskPriority.NORMAL.value
        assert TaskPriority.NORMAL.value < TaskPriority.LOW.value
        assert TaskPriority.LOW.value < TaskPriority.BACKGROUND.value
    
    def test_claw_work_mode_enum(self):
        """ClawWorkMode枚举"""
        from src.intelligence.claws._global_claw_scheduler import ClawWorkMode
        
        assert ClawWorkMode.INDEPENDENT.value == "independent"
        assert ClawWorkMode.PRIMARY.value == "primary"
        assert ClawWorkMode.CONTRIBUTOR.value == "contributor"
        assert ClawWorkMode.ADVISOR.value == "advisor"
        assert ClawWorkMode.REVIEWER.value == "reviewer"
    
    def test_scheduler_stats_defaults(self):
        """SchedulerStats默认值"""
        from src.intelligence.claws._global_claw_scheduler import SchedulerStats
        
        stats = SchedulerStats(pool_size=10)
        assert stats.total_dispatched == 0
        assert stats.pool_size == 10
        assert stats.avg_response_time == 0.0
    
    def test_work_pool_status_defaults(self):
        """WorkPoolStatus默认值"""
        from src.intelligence.claws._global_claw_scheduler import WorkPoolStatus
        
        status = WorkPoolStatus()
        assert status.total_claws == 0
        assert status.departments == {}
        assert status.top_busy == []


# ═══════════════════════════════════════════════════════════════
# 测试2: GlobalClawScheduler 初始化
# ═══════════════════════════════════════════════════════════════

class TestSchedulerInitialization:
    """验证调度器初始化"""
    
    @pytest.mark.asyncio
    async def test_create_scheduler(self):
        """创建调度器实例"""
        from src.intelligence.claws._global_claw_scheduler import GlobalClawScheduler
        
        scheduler = GlobalClawScheduler(max_concurrent=3)
        assert scheduler._max_concurrent == 3
        assert scheduler._initialized is False
        assert scheduler._stats.pool_size == 3
    
    @pytest.mark.asyncio
    async def test_max_concurrent_limit(self):
        """并发数上限限制"""
        from src.intelligence.claws._global_claw_scheduler import GlobalClawScheduler
        
        scheduler = GlobalClawScheduler(max_concurrent=100)
        assert scheduler._max_concurrent == 20  # MAX_CONCURRENT_LIMIT
    
    def test_ensure_initialized_raises(self):
        """未初始化时调用应抛出异常"""
        from src.intelligence.claws._global_claw_scheduler import GlobalClawScheduler
        
        scheduler = GlobalClawScheduler()
        with pytest.raises(RuntimeError, match="未初始化"):
            scheduler._ensure_initialized()
    
    @pytest.mark.asyncio
    async def test_get_global_singleton(self):
        """全局单例"""
        from src.intelligence.claws._global_claw_scheduler import (
            GlobalClawScheduler, get_global_claw_scheduler,
            _global_scheduler,
        )
        
        # 重置全局实例
        import src.intelligence.claws._global_claw_scheduler as mod
        mod._global_scheduler = None
        
        s1 = get_global_claw_scheduler()
        s2 = get_global_claw_scheduler()
        assert s1 is s2
        
        # 清理
        mod._global_scheduler = _global_scheduler


# ═══════════════════════════════════════════════════════════════
# 测试3: 独立工作（单Claw执行）
# ═══════════════════════════════════════════════════════════════

class TestIndependentWork:
    """验证独立工作模式"""
    
    @pytest.mark.asyncio
    async def test_dispatch_single_direct(self):
        """单Claw直接执行"""
        from src.intelligence.claws._global_claw_scheduler import GlobalClawScheduler
        
        scheduler = GlobalClawScheduler()
        
        # Mock协调器
        mock_coordinator = MagicMock()
        mock_claw = AsyncMock()
        mock_claw.process = AsyncMock(return_value=MagicMock(
            success=True,
            final_answer="仁者爱人",
        ))
        mock_coordinator.get_claw = MagicMock(return_value=mock_claw)
        
        scheduler._coordinator = mock_coordinator
        scheduler._initialized = True
        scheduler._semaphore = asyncio.Semaphore(5)
        
        ticket = await scheduler.dispatch_single("孔子", "什么是仁？")
        
        assert ticket.success is True
        assert ticket.answer == "仁者爱人"
        assert ticket.claw_used == "孔子"
        assert ticket.completed_at is not None
    
    @pytest.mark.asyncio
    async def test_dispatch_single_timeout(self):
        """单Claw执行超时"""
        from src.intelligence.claws._global_claw_scheduler import GlobalClawScheduler
        
        scheduler = GlobalClawScheduler()
        
        mock_coordinator = MagicMock()
        mock_claw = AsyncMock()
        # 用永远不完成的协程模拟超时
        async def never_finish(*args, **kwargs):
            await asyncio.sleep(100)
        mock_claw.process = never_finish
        mock_coordinator.get_claw = MagicMock(return_value=mock_claw)
        
        scheduler._coordinator = mock_coordinator
        scheduler._initialized = True
        scheduler._semaphore = asyncio.Semaphore(5)
        
        ticket = await scheduler.dispatch_single("孔子", "什么是仁？", timeout=0.1)
        
        assert ticket.success is False
        assert "超时" in ticket.error
    
    @pytest.mark.asyncio
    async def test_dispatch_single_claw_not_found(self):
        """单Claw不存在时回退到Bridge"""
        from src.intelligence.claws._global_claw_scheduler import GlobalClawScheduler
        
        scheduler = GlobalClawScheduler()
        
        mock_coordinator = MagicMock()
        mock_coordinator.get_claw = MagicMock(return_value=None)
        
        mock_bridge = AsyncMock()
        mock_bridge.dispatch = AsyncMock(return_value=MagicMock(
            success=True,
            answer="这是Bridge的回答",
            claw_name="孔子",
            confidence=0.8,
            collaborators=["孟子"],
        ))
        
        scheduler._coordinator = mock_coordinator
        scheduler._bridge = mock_bridge
        scheduler._initialized = True
        scheduler._semaphore = asyncio.Semaphore(5)
        
        ticket = await scheduler.dispatch_single("孔子", "什么是仁？")
        
        assert ticket.success is True
        assert ticket.answer == "这是Bridge的回答"
    
    @pytest.mark.asyncio
    async def test_dispatch_single_with_ticket(self):
        """使用已有Ticket进行单Claw调度"""
        from src.intelligence.claws._global_claw_scheduler import (
            GlobalClawScheduler, TaskTicket,
        )
        
        scheduler = GlobalClawScheduler()
        mock_coordinator = MagicMock()
        mock_claw = AsyncMock()
        mock_claw.process = AsyncMock(return_value=MagicMock(
            success=True,
            final_answer="道可道，非常道",
        ))
        mock_coordinator.get_claw = MagicMock(return_value=mock_claw)
        
        scheduler._coordinator = mock_coordinator
        scheduler._initialized = True
        scheduler._semaphore = asyncio.Semaphore(5)
        
        existing_ticket = TaskTicket.create("什么是道？")
        result = await scheduler.dispatch_single("老子", "什么是道？", ticket=existing_ticket)
        
        assert result.task_id == existing_ticket.task_id
        assert result.success is True


# ═══════════════════════════════════════════════════════════════
# 测试4: 协作工作（多Claw协作）
# ═══════════════════════════════════════════════════════════════

class TestCollaborativeWork:
    """验证协作工作模式"""
    
    @pytest.mark.asyncio
    async def test_dispatch_collaborative_basic(self):
        """基本协作调度"""
        from src.intelligence.claws._global_claw_scheduler import GlobalClawScheduler
        
        scheduler = GlobalClawScheduler()
        
        mock_protocol = AsyncMock()
        mock_protocol.execute_collaboration = AsyncMock(return_value=MagicMock(
            success=True,
            final_answer="综合分析结果",
            confidence=0.85,
            contributions=[
                MagicMock(claw_name="孔子"),
                MagicMock(claw_name="管仲"),
                MagicMock(claw_name="韩非子"),
            ],
            errors=[],
        ))
        
        scheduler._collaboration_protocol = mock_protocol
        scheduler._initialized = True
        scheduler._semaphore = asyncio.Semaphore(5)
        
        ticket = await scheduler.dispatch_collaborative(
            "如何治理国家",
            ["孔子", "管仲", "韩非子"],
        )
        
        assert ticket.success is True
        assert ticket.answer == "综合分析结果"
        assert ticket.claw_used == "孔子"
        assert len(ticket.collaborators_used) == 3
    
    @pytest.mark.asyncio
    async def test_dispatch_collaborative_with_roles(self):
        """协作调度带角色分配"""
        from src.intelligence.claws._global_claw_scheduler import (
            GlobalClawScheduler, ClawWorkMode,
        )
        
        scheduler = GlobalClawScheduler()
        
        mock_protocol = AsyncMock()
        mock_protocol.execute_collaboration = AsyncMock(return_value=MagicMock(
            success=True,
            final_answer="角色协作结果",
            confidence=0.9,
            contributions=[
                MagicMock(claw_name="孔子"),
                MagicMock(claw_name="孟子"),
            ],
            errors=[],
        ))
        
        scheduler._collaboration_protocol = mock_protocol
        scheduler._initialized = True
        scheduler._semaphore = asyncio.Semaphore(5)
        
        ticket = await scheduler.dispatch_collaborative(
            "什么是仁义",
            ["孔子", "孟子"],
            roles={
                "孔子": ClawWorkMode.PRIMARY,
                "孟子": ClawWorkMode.ADVISOR,
            },
        )
        
        assert ticket.success is True
    
    @pytest.mark.asyncio
    async def test_dispatch_collaborative_no_claws(self):
        """协作模式至少需要1个Claw"""
        from src.intelligence.claws._global_claw_scheduler import GlobalClawScheduler
        
        scheduler = GlobalClawScheduler()
        scheduler._initialized = True
        
        with pytest.raises(ValueError, match="至少需要1个Claw"):
            await scheduler.dispatch_collaborative("测试", [])


# ═══════════════════════════════════════════════════════════════
# 测试5: 分布式工作（批量并发）
# ═══════════════════════════════════════════════════════════════

class TestDistributedWork:
    """验证分布式工作模式"""
    
    @pytest.mark.asyncio
    async def test_dispatch_distributed_basic(self):
        """基本批量分发"""
        from src.intelligence.claws._global_claw_scheduler import (
            GlobalClawScheduler, TaskTicket, TaskPriority,
        )
        
        scheduler = GlobalClawScheduler()
        scheduler._initialized = True
        scheduler._semaphore = asyncio.Semaphore(5)
        scheduler._collaboration_protocol = None  # 不使用协作
        
        # 使用真实dispatch但mock内部组件
        mock_coordinator = MagicMock()
        mock_claw = AsyncMock()
        mock_claw.process = AsyncMock(return_value=MagicMock(
            success=True,
            final_answer="回答成功",
        ))
        mock_coordinator.get_claw = MagicMock(return_value=mock_claw)
        scheduler._coordinator = mock_coordinator
        
        mock_router = MagicMock()
        mock_router.route_by_query = MagicMock(return_value=MagicMock(
            primary_claw="孔子",
            collaborator_claws=[],  # 无协作者 → 独立工作
            confidence=0.7,
        ))
        scheduler._claw_router = mock_router
        
        tickets = [
            TaskTicket.create(f"问题{i}", priority=TaskPriority.NORMAL)
            for i in range(3)
        ]
        
        # 直接并发调用dispatch（绕过dispatch_distributed的batch逻辑）
        tasks = []
        for t in tickets:
            tasks.append(asyncio.create_task(scheduler.dispatch(t)))
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 3
        assert all(r.success for r in results)
    
    @pytest.mark.asyncio
    async def test_dispatch_distributed_empty(self):
        """空列表返回空结果"""
        from src.intelligence.claws._global_claw_scheduler import GlobalClawScheduler
        
        scheduler = GlobalClawScheduler()
        scheduler._initialized = True
        
        results = await scheduler.dispatch_distributed([])
        assert results == []
    
    @pytest.mark.asyncio
    async def test_dispatch_distributed_with_failures(self):
        """批量分发中部分失败"""
        from src.intelligence.claws._global_claw_scheduler import (
            GlobalClawScheduler, TaskTicket,
        )
        
        scheduler = GlobalClawScheduler()
        scheduler._initialized = True
        scheduler._semaphore = asyncio.Semaphore(5)
        scheduler._collaboration_protocol = None  # 不使用协作
        
        # Mock让第偶数个请求失败
        mock_coordinator = MagicMock()
        call_count = 0
        def get_claw_side_effect(name):
            nonlocal call_count
            call_count += 1
            mock_claw = AsyncMock()
            if call_count % 2 == 0:
                mock_claw.process = AsyncMock(return_value=MagicMock(
                    success=False, final_answer="", reason="模拟失败",
                ))
            else:
                mock_claw.process = AsyncMock(return_value=MagicMock(
                    success=True, final_answer="成功",
                ))
            return mock_claw
        mock_coordinator.get_claw = MagicMock(side_effect=get_claw_side_effect)
        scheduler._coordinator = mock_coordinator
        
        mock_router = MagicMock()
        mock_router.route_by_query = MagicMock(return_value=MagicMock(
            primary_claw="孔子",
            collaborator_claws=[],
            confidence=0.7,
        ))
        scheduler._claw_router = mock_router
        
        tickets = [TaskTicket.create(f"问题{i}") for i in range(4)]
        tasks = [asyncio.create_task(scheduler.dispatch(t)) for t in tickets]
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 4
        assert sum(1 for r in results if r.success) >= 1
    
    @pytest.mark.asyncio
    async def test_dispatch_distributed_priority_ordering(self):
        """按优先级排序分发"""
        from src.intelligence.claws._global_claw_scheduler import (
            GlobalClawScheduler, TaskTicket, TaskPriority,
        )
        
        scheduler = GlobalClawScheduler()
        
        execution_order = []
        async def mock_dispatch(ticket):
            execution_order.append(ticket.priority.value)
            ticket.success = True
            return ticket
        
        scheduler.dispatch = mock_dispatch
        scheduler._initialized = True
        
        import random
        priorities = list(TaskPriority)
        random.shuffle(priorities)
        
        tickets = [TaskTicket.create(f"问题{i}", priority=p) for i, p in enumerate(priorities)]
        await scheduler.dispatch_distributed(tickets)
        
        # 应按优先级排序（CRITICAL=0最先）
        assert execution_order == sorted(execution_order)


# ═══════════════════════════════════════════════════════════════
# 测试6: 全局调动（路由策略）
# ═══════════════════════════════════════════════════════════════

class TestGlobalRouting:
    """验证全局调动路由策略"""
    
    @pytest.mark.asyncio
    async def test_dispatch_to_department(self):
        """按部门调度"""
        from src.intelligence.claws._global_claw_scheduler import (
            GlobalClawScheduler, TaskTicket,
        )
        
        scheduler = GlobalClawScheduler()
        
        # Mock ClawRouter
        mock_router = MagicMock()
        mock_router.route_by_department = MagicMock(return_value=MagicMock(
            primary_claw="孔子",
            collaborator_claws=["孟子", "荀子"],
            department="礼部",
            confidence=0.8,
            routing_reason="部门匹配",
        ))
        
        scheduler._claw_router = mock_router
        scheduler._initialized = True
        
        # Mock dispatch to avoid full execution
        async def mock_dispatch(ticket):
            ticket.success = True
            ticket.answer = "部门调度结果"
            return ticket
        scheduler.dispatch = mock_dispatch
        
        ticket = await scheduler.dispatch_to_department("礼部", "什么是仁？")
        
        assert ticket.department == "礼部"
        assert ticket.target_claw == "孔子"
        assert "孟子" in ticket.collaborators
        mock_router.route_by_department.assert_called_once_with("礼部", "什么是仁？")
    
    @pytest.mark.asyncio
    async def test_dispatch_to_problem_type(self):
        """按ProblemType调度"""
        from src.intelligence.claws._global_claw_scheduler import GlobalClawScheduler
        
        scheduler = GlobalClawScheduler()
        
        mock_router = MagicMock()
        mock_router.route_by_problem_type = MagicMock(return_value=MagicMock(
            primary_claw="孙子",
            collaborator_claws=["韩信"],
            department="兵部",
            confidence=0.85,
            routing_reason="PT映射",
        ))
        
        scheduler._claw_router = mock_router
        scheduler._initialized = True
        
        async def mock_dispatch(ticket):
            ticket.success = True
            return ticket
        scheduler.dispatch = mock_dispatch
        
        ticket = await scheduler.dispatch_to_problem_type("COMPETITION", "如何应对竞争")
        
        assert ticket.problem_type == "COMPETITION"
        assert ticket.target_claw == "孙子"
        assert ticket.department == "兵部"
    
    @pytest.mark.asyncio
    async def test_dispatch_to_school(self):
        """按学派调度"""
        from src.intelligence.claws._global_claw_scheduler import GlobalClawScheduler
        
        scheduler = GlobalClawScheduler()
        
        mock_coordinator = MagicMock()
        mock_coordinator.find_by_school = MagicMock(return_value=["老子", "庄子", "列子"])
        
        scheduler._coordinator = mock_coordinator
        scheduler._initialized = True
        
        async def mock_dispatch(ticket):
            ticket.success = True
            return ticket
        scheduler.dispatch = mock_dispatch
        
        ticket = await scheduler.dispatch_to_school("道家", "什么是无为")
        
        assert ticket.target_claw == "老子"
        assert "庄子" in ticket.collaborators
    
    @pytest.mark.asyncio
    async def test_dispatch_to_claw(self):
        """直接调度到指定Claw"""
        from src.intelligence.claws._global_claw_scheduler import GlobalClawScheduler
        
        scheduler = GlobalClawScheduler()
        
        mock_coordinator = MagicMock()
        mock_claw = AsyncMock()
        mock_claw.process = AsyncMock(return_value=MagicMock(
            success=True,
            final_answer="法者，治国之重器",
        ))
        mock_coordinator.get_claw = MagicMock(return_value=mock_claw)
        
        scheduler._coordinator = mock_coordinator
        scheduler._initialized = True
        scheduler._semaphore = asyncio.Semaphore(5)
        
        ticket = await scheduler.dispatch_to_claw("韩非子", "什么是法？")
        
        assert ticket.success is True
        assert ticket.claw_used == "韩非子"
    
    @pytest.mark.asyncio
    async def test_auto_dispatch_with_problem_type(self):
        """自动路由优先使用ProblemType"""
        from src.intelligence.claws._global_claw_scheduler import (
            GlobalClawScheduler, TaskTicket,
        )
        
        scheduler = GlobalClawScheduler()
        scheduler._initialized = True
        scheduler._semaphore = asyncio.Semaphore(5)
        scheduler._collaboration_protocol = None  # 不使用协作
        
        mock_router = MagicMock()
        mock_router.route_by_problem_type = MagicMock(return_value=MagicMock(
            primary_claw="商鞅",
            collaborator_claws=["韩非子"],
            department="刑部",
            confidence=0.9,
            routing_reason="PT路由",
        ))
        
        scheduler._claw_router = mock_router
        
        mock_coordinator = MagicMock()
        mock_claw = AsyncMock()
        mock_claw.process = AsyncMock(return_value=MagicMock(
            success=True,
            final_answer="变法图强",
        ))
        mock_coordinator.get_claw = MagicMock(return_value=mock_claw)
        scheduler._coordinator = mock_coordinator
        
        ticket = TaskTicket.create("如何变法", problem_type="LEGAL")
        result = await scheduler.dispatch(ticket)
        
        assert result.claw_used == "商鞅"
        mock_router.route_by_problem_type.assert_called_once()


# ═══════════════════════════════════════════════════════════════
# 测试7: 统计与监控
# ═══════════════════════════════════════════════════════════════

class TestMonitoring:
    """验证统计与监控功能"""
    
    def test_get_stats(self):
        """获取统计信息"""
        from src.intelligence.claws._global_claw_scheduler import (
            GlobalClawScheduler, SchedulerStats,
        )
        
        scheduler = GlobalClawScheduler()
        scheduler._stats = SchedulerStats(
            total_dispatched=10,
            total_completed=8,
            total_failed=2,
        )
        scheduler._active_tickets = {"t1": MagicMock(), "t2": MagicMock()}
        
        stats = scheduler.get_stats()
        
        assert stats.total_dispatched == 10
        assert stats.total_completed == 8
        assert stats.active_tasks == 2
    
    def test_get_work_pool_status(self):
        """获取工作池状态"""
        from src.intelligence.claws._global_claw_scheduler import GlobalClawScheduler
        
        scheduler = GlobalClawScheduler()
        
        mock_router = MagicMock()
        mock_router._claws = {"孔子": MagicMock(), "老子": MagicMock()}
        mock_router._department_claws = {"礼部": ["孔子"], "道家": ["老子"]}
        mock_router._school_claws = {"儒家": ["孔子"], "道家": ["老子"]}
        
        scheduler._claw_router = mock_router
        
        status = scheduler.get_work_pool_status()
        
        assert status.total_claws == 2
        assert status.departments == {"礼部": 1, "道家": 1}
    
    def test_list_available_claws(self):
        """列出可用Claw"""
        from src.intelligence.claws._global_claw_scheduler import GlobalClawScheduler
        
        scheduler = GlobalClawScheduler()
        
        mock_router = MagicMock()
        mock_claw = MagicMock()
        mock_claw.name = "孔子"
        mock_claw.department = "礼部"
        mock_claw.school = "儒家"
        mock_claw.position_name = "太子太傅"
        mock_claw.priority_score = 200.0
        mock_router._claws = {"孔子": mock_claw}
        mock_router._department_claws = {"礼部": ["孔子"]}
        mock_router._school_claws = {"儒家": ["孔子"]}
        
        scheduler._coordinator = None
        scheduler._claw_router = mock_router
        
        claws = scheduler.list_available_claws()
        
        assert len(claws) == 1
        assert claws[0]["name"] == "孔子"
        assert claws[0]["department"] == "礼部"
    
    def test_get_active_tickets(self):
        """获取活跃任务"""
        from src.intelligence.claws._global_claw_scheduler import (
            GlobalClawScheduler, TaskTicket, DispatchMode,
        )
        
        scheduler = GlobalClawScheduler()
        
        ticket = TaskTicket.create("测试任务", mode=DispatchMode.SINGLE)
        ticket.started_at = "2026-04-23T18:00:00"
        scheduler._active_tickets = {ticket.task_id: ticket}
        
        active = scheduler.get_active_tickets()
        
        assert len(active) == 1
        assert active[0]["task_id"] == ticket.task_id
    
    def test_get_recent_results(self):
        """获取最近结果"""
        from src.intelligence.claws._global_claw_scheduler import (
            GlobalClawScheduler, TaskTicket,
        )
        
        scheduler = GlobalClawScheduler()
        
        for i in range(5):
            t = TaskTicket.create(f"任务{i}")
            t.success = i % 2 == 0
            t.claw_used = "孔子"
            t.elapsed_seconds = float(i + 1)
            scheduler._completed_tickets.append(t)
        
        recent = scheduler.get_recent_results(limit=3)
        
        assert len(recent) == 3
        # 最新的在前（倒序）
        assert recent[0]["query"] == "任务4"
    
    def test_find_collaborators(self):
        """发现协作Claw"""
        from src.intelligence.claws._global_claw_scheduler import GlobalClawScheduler
        
        scheduler = GlobalClawScheduler()
        
        mock_protocol = MagicMock()
        mock_protocol.discover_collaborators = MagicMock(return_value=[
            ("孟子", "contributor"),
            ("荀子", "advisor"),
        ])
        
        # 需要mock CollaborationRole
        from src.intelligence.dispatcher.wisdom_dispatch._dispatch_collaboration import (
            CollaborationRole,
        )
        mock_protocol.discover_collaborators = MagicMock(return_value=[
            ("孟子", CollaborationRole.CONTRIBUTOR),
            ("荀子", CollaborationRole.ADVISOR),
        ])
        
        scheduler._collaboration_protocol = mock_protocol
        
        collaborators = scheduler.find_collaborators("孔子", "什么是仁？")
        
        assert len(collaborators) == 2
        assert collaborators[0][0] == "孟子"


# ═══════════════════════════════════════════════════════════════
# 测试8: 生命周期与回调
# ═══════════════════════════════════════════════════════════════

class TestLifecycle:
    """验证生命周期管理"""
    
    @pytest.mark.asyncio
    async def test_shutdown(self):
        """关闭调度器"""
        from src.intelligence.claws._global_claw_scheduler import GlobalClawScheduler
        
        scheduler = GlobalClawScheduler()
        scheduler._initialized = True
        scheduler._stats.total_dispatched = 10
        scheduler._stats.total_completed = 8
        scheduler._stats.total_failed = 2
        scheduler._stats.avg_response_time = 1.5
        scheduler._thread_pool = MagicMock()
        
        result = await scheduler.shutdown()
        
        assert result["status"] == "shutdown"
        assert result["total_dispatched"] == 10
        assert scheduler._initialized is False
    
    def test_callback_registration(self):
        """回调注册"""
        from src.intelligence.claws._global_claw_scheduler import GlobalClawScheduler
        
        scheduler = GlobalClawScheduler()
        
        cb1 = MagicMock()
        cb2 = MagicMock()
        
        scheduler.on_task_start(cb1)
        scheduler.on_task_complete(cb2)
        scheduler.on_task_fail(MagicMock())
        
        assert len(scheduler._on_task_start) == 1
        assert len(scheduler._on_task_complete) == 1
        assert len(scheduler._on_task_fail) == 1


# ═══════════════════════════════════════════════════════════════
# 测试9: 全局dispatch入口
# ═══════════════════════════════════════════════════════════════

class TestDispatchEntry:
    """验证dispatch主入口"""
    
    @pytest.mark.asyncio
    async def test_dispatch_auto_mode(self):
        """AUTO模式自动选择独立/协作"""
        from src.intelligence.claws._global_claw_scheduler import (
            GlobalClawScheduler, TaskTicket,
        )
        
        scheduler = GlobalClawScheduler()
        scheduler._initialized = True
        scheduler._semaphore = asyncio.Semaphore(5)
        
        # 无target_claw → 走auto路由
        mock_router = MagicMock()
        mock_router.route_by_query = MagicMock(return_value=MagicMock(
            primary_claw="孔子",
            collaborator_claws=[],
            confidence=0.7,
        ))
        scheduler._claw_router = mock_router
        
        mock_coordinator = MagicMock()
        mock_claw = AsyncMock()
        mock_claw.process = AsyncMock(return_value=MagicMock(
            success=True,
            final_answer="自动路由成功",
        ))
        mock_coordinator.get_claw = MagicMock(return_value=mock_claw)
        scheduler._coordinator = mock_coordinator
        
        ticket = TaskTicket.create("什么是仁义礼智信？")
        result = await scheduler.dispatch(ticket)
        
        assert result.success is True
        assert result.claw_used == "孔子"
    
    @pytest.mark.asyncio
    async def test_dispatch_collaborative_mode(self):
        """COLLABORATIVE模式走协作路径"""
        from src.intelligence.claws._global_claw_scheduler import (
            GlobalClawScheduler, TaskTicket, DispatchMode,
        )
        
        scheduler = GlobalClawScheduler()
        scheduler._initialized = True
        scheduler._semaphore = asyncio.Semaphore(5)
        scheduler._stats.total_collaborative = 0  # 确保初始为0
        
        mock_protocol = AsyncMock()
        mock_protocol.execute_collaboration = AsyncMock(return_value=MagicMock(
            success=True,
            final_answer="协作结果",
            confidence=0.88,
            contributions=[MagicMock(claw_name="孔子")],
            errors=[],
        ))
        scheduler._collaboration_protocol = mock_protocol
        
        ticket = TaskTicket.create(
            "如何治理国家",
            target_claw="孔子",
            mode=DispatchMode.COLLABORATIVE,
            collaborators=["管仲", "韩非子"],
        )
        result = await scheduler.dispatch(ticket)
        
        assert result.success is True
        assert result.answer == "协作结果"
        # dispatch_collaborative_from_ticket内部递增total_collaborative
        # 但dispatch入口的dispatch_collaborative_from_ticket是在try块内的
        assert scheduler._stats.total_collaborative >= 1


# ═══════════════════════════════════════════════════════════════
# 测试10: 模块导入完整性
# ═══════════════════════════════════════════════════════════════

class TestModuleImports:
    """验证模块导入完整"""
    
    def test_import_from_module(self):
        """直接从模块导入"""
        from src.intelligence.claws._global_claw_scheduler import (
            GlobalClawScheduler,
            TaskTicket,
            SchedulerStats,
            WorkPoolStatus,
            DispatchMode,
            TaskPriority,
            ClawWorkMode,
            get_global_claw_scheduler,
            ensure_global_scheduler,
            quick_dispatch,
        )
        assert callable(GlobalClawScheduler)
        assert callable(TaskTicket.create)
        assert callable(get_global_claw_scheduler)
    
    def test_import_from_package(self):
        """从claws包导入"""
        from src.intelligence.claws import (
            GlobalClawScheduler,
            TaskTicket,
            DispatchMode,
            ClawWorkMode,
            get_global_claw_scheduler,
            quick_dispatch,
        )
        assert GlobalClawScheduler is not None
        assert TaskTicket is not None


# ═══════════════════════════════════════════════════════════════
# 测试11: quick_dispatch同步函数
# ═══════════════════════════════════════════════════════════════

class TestQuickDispatch:
    """验证快捷同步调度"""
    
    def test_quick_dispatch_claw_name(self):
        """指定Claw的快捷调度"""
        from src.intelligence.claws._global_claw_scheduler import (
            GlobalClawScheduler, TaskTicket,
        )
        import src.intelligence.claws._global_claw_scheduler as mod
        
        scheduler = GlobalClawScheduler()
        scheduler._initialized = True
        
        # Mock dispatch_sync
        def mock_sync(ticket):
            ticket.success = True
            ticket.answer = "同步结果"
            ticket.claw_used = ticket.target_claw or "孔子"
            return ticket
        scheduler.dispatch_sync = mock_sync
        
        # 重置单例
        original = mod._global_scheduler
        mod._global_scheduler = scheduler
        
        try:
            result = mod.quick_dispatch("什么是仁？", claw_name="孔子")
            assert result.success is True
            assert result.claw_used == "孔子"
        finally:
            mod._global_scheduler = original


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
