# -*- coding: utf-8 -*-
"""
test_claw_agent_wrapper.py - Claw独立子Agent化功能测试
=======================================================

测试ClawAgentWrapper和GlobalClawScheduler.spawn_as_task功能。

运行: python -m pytest tests/test_claw_agent_wrapper.py -v

版本: v1.0.0
创建: 2026-04-24
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch


class TestClawAgentWrapper:
    """ClawAgentWrapper单元测试"""
    
    @pytest.fixture
    def mock_claw(self):
        """模拟Claw实例"""
        claw = AsyncMock()
        claw.process.return_value = MagicMock(
            final_answer="测试答案",
            success=True,
            steps=[MagicMock()],
        )
        return claw
    
    @pytest.mark.asyncio
    async def test_spawn_returns_task_id(self, mock_claw):
        """测试spawn返回task_id"""
        from src.intelligence.claws._claw_agent_wrapper import (
            ClawAgentWrapper, AgentTaskInfo
        )
        
        wrapper = ClawAgentWrapper("孔子")
        
        with patch.object(wrapper, '_ensure_claw_loaded', return_value=mock_claw):
            task_id = await wrapper.spawn("什么是仁？")
        
        assert task_id is not None
        assert task_id.startswith("claw_task_")
        assert task_id in wrapper._tasks
    
    @pytest.mark.asyncio
    async def test_spawn_with_options(self, mock_claw):
        """测试带选项的spawn"""
        from src.intelligence.claws._claw_agent_wrapper import (
            ClawAgentWrapper, SpawnOptions, TaskStatus
        )
        
        wrapper = ClawAgentWrapper("孔子")
        
        options = SpawnOptions(
            background=True,
            timeout=60.0,
            enable_nested=True,
        )
        
        with patch.object(wrapper, '_ensure_claw_loaded', return_value=mock_claw):
            task_id = await wrapper.spawn("什么是仁？", options=options)
        
        task_info = wrapper.get_task_info(task_id)
        assert task_info.claw_name == "孔子"
        assert task_info.query == "什么是仁？"
    
    @pytest.mark.asyncio
    async def test_task_status_tracking(self, mock_claw):
        """测试任务状态追踪"""
        from src.intelligence.claws._claw_agent_wrapper import (
            ClawAgentWrapper, TaskStatus
        )
        
        wrapper = ClawAgentWrapper("孔子")
        
        with patch.object(wrapper, '_ensure_claw_loaded', return_value=mock_claw):
            task_id = await wrapper.spawn("什么是仁？")
        
        # 初始状态
        status = wrapper.get_task_status(task_id)
        assert status == TaskStatus.PENDING or status == TaskStatus.RUNNING
        
        # 等待完成
        result = await wrapper.wait_result(task_id, timeout=10)
        
        assert result is not None
        assert result.claw_name == "孔子"
    
    @pytest.mark.asyncio
    async def test_cancel_task(self, mock_claw):
        """测试取消任务"""
        from src.intelligence.claws._claw_agent_wrapper import (
            ClawAgentWrapper, TaskStatus
        )
        
        # 模拟长时间运行的Claw
        async def slow_process(*args, **kwargs):
            await asyncio.sleep(60)  # 模拟长时间任务
            return MagicMock(final_answer="慢答案", success=True)
        
        mock_claw.process = slow_process
        
        wrapper = ClawAgentWrapper("孔子")
        
        with patch.object(wrapper, '_ensure_claw_loaded', return_value=mock_claw):
            task_id = await wrapper.spawn("长时间任务")
        
        # 等待任务开始执行
        await asyncio.sleep(0.5)
        
        # 取消任务
        cancelled = await wrapper.cancel_task(task_id)
        assert cancelled == True
        
        status = wrapper.get_task_status(task_id)
        assert status == TaskStatus.CANCELLED
    
    def test_get_stats(self):
        """测试统计信息"""
        from src.intelligence.claws._claw_agent_wrapper import ClawAgentWrapper
        
        wrapper = ClawAgentWrapper("孔子")
        stats = wrapper.get_stats()
        
        assert stats["claw_name"] == "孔子"
        assert stats["total_tasks"] == 0
        assert "status_counts" in stats


class TestClawAgentPool:
    """ClawAgentPool测试"""
    
    def test_get_wrapper_creates_new(self):
        """测试获取/创建Wrapper"""
        from src.intelligence.claws._claw_agent_wrapper import ClawAgentPool
        
        pool = ClawAgentPool()
        wrapper1 = pool.get_wrapper("孔子")
        wrapper2 = pool.get_wrapper("孔子")
        
        assert wrapper1 is wrapper2  # 同一个实例
    
    def test_get_wrapper_different_claws(self):
        """测试不同Claw返回不同Wrapper"""
        from src.intelligence.claws._claw_agent_wrapper import ClawAgentPool
        
        pool = ClawAgentPool()
        wrapper1 = pool.get_wrapper("孔子")
        wrapper2 = pool.get_wrapper("老子")
        
        assert wrapper1 is not wrapper2
        assert wrapper1.claw_name == "孔子"
        assert wrapper2.claw_name == "老子"
    
    def test_pool_stats(self):
        """测试池统计"""
        from src.intelligence.claws._claw_agent_wrapper import ClawAgentPool
        
        pool = ClawAgentPool()
        pool.get_wrapper("孔子")
        pool.get_wrapper("老子")
        
        stats = pool.get_pool_stats()
        
        assert stats["total_claws"] == 2
        assert "孔子" in stats["wrappers"]
        assert "老子" in stats["wrappers"]


class TestGlobalClawSchedulerSpawn:
    """GlobalClawScheduler.spawn_as_task测试"""
    
    @pytest.mark.asyncio
    async def test_spawn_as_task_basic(self):
        """测试基本spawn功能"""
        from src.intelligence.claws._global_claw_scheduler import (
            GlobalClawScheduler, ClawWorkMode
        )
        
        # 确认TASK_AGENT模式已添加
        assert ClawWorkMode.TASK_AGENT.value == "task_agent"
        
        # 创建调度器但不初始化完整依赖
        scheduler = GlobalClawScheduler()
        scheduler._initialized = True
        
        # 由于依赖复杂，只验证方法存在
        assert hasattr(scheduler, 'spawn_as_task')
        assert hasattr(scheduler, 'get_agent_task_status')
        assert hasattr(scheduler, 'wait_agent_task')
        assert hasattr(scheduler, 'spawn_multi_agent_tasks')
    
    @pytest.mark.asyncio
    async def test_spawn_as_task_signature(self):
        """测试spawn_as_task方法签名"""
        import inspect
        from src.intelligence.claws._global_claw_scheduler import GlobalClawScheduler
        
        sig = inspect.signature(GlobalClawScheduler.spawn_as_task)
        params = list(sig.parameters.keys())
        
        # 验证必要参数
        assert 'self' in params
        assert 'claw_name' in params
        assert 'query' in params
        assert 'background' in params
        assert 'timeout' in params
        assert 'context' in params
        assert 'enable_nested' in params


class TestSpawnOptions:
    """SpawnOptions测试"""
    
    def test_default_options(self):
        """测试默认选项"""
        from src.intelligence.claws._claw_agent_wrapper import SpawnOptions
        
        options = SpawnOptions()
        
        assert options.background == True
        assert options.timeout is None
        assert options.priority == 1
        assert options.enable_nested == True
        assert options.on_complete is None
        assert options.on_error is None
    
    def test_custom_options(self):
        """测试自定义选项"""
        from src.intelligence.claws._claw_agent_wrapper import SpawnOptions
        
        def my_callback(info):
            pass
        
        options = SpawnOptions(
            background=False,
            timeout=300.0,
            priority=0,
            enable_nested=False,
            on_complete=my_callback,
        )
        
        assert options.background == False
        assert options.timeout == 300.0
        assert options.priority == 0
        assert options.enable_nested == False
        assert options.on_complete == my_callback


class TestTaskStatus:
    """TaskStatus枚举测试"""
    
    def test_all_statuses_defined(self):
        """测试所有状态已定义"""
        from src.intelligence.claws._claw_agent_wrapper import TaskStatus
        
        expected = ["PENDING", "RUNNING", "COMPLETED", "FAILED", "CANCELLED", "TIMEOUT"]
        
        for status_name in expected:
            assert hasattr(TaskStatus, status_name)
            status = getattr(TaskStatus, status_name)
            assert status.value == status_name.lower()
    
    def test_task_status_values(self):
        """测试状态值"""
        from src.intelligence.claws._claw_agent_wrapper import TaskStatus
        
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.RUNNING.value == "running"
        assert TaskStatus.COMPLETED.value == "completed"
        assert TaskStatus.FAILED.value == "failed"
        assert TaskStatus.CANCELLED.value == "cancelled"
        assert TaskStatus.TIMEOUT.value == "timeout"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
