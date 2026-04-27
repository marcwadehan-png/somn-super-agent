# -*- coding: utf-8 -*-
"""
多Claw协作调度器 - 让一群AI打工人都能干活
版本: v1.0.0
"""

import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import uuid

# 任务优先级
class Priority:
    HIGH = 3
    MEDIUM = 2
    LOW = 1

@dataclass
class SubTask:
    """子任务"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    claw_id: str = ""  # 分配给哪个Claw
    content: str = ""
    priority: int = Priority.MEDIUM
    status: str = "pending"  # pending/running/done/failed
    result: Any = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

@dataclass  
class TaskQueue:
    """任务队列"""
    name: str
    tasks: List[SubTask] = field(default_factory=list)
    claw_assignments: Dict[str, str] = field(default_factory=dict)  # claw_id -> task_id
    
    def add(self, task: SubTask):
        self.tasks.append(task)
        self.tasks.sort(key=lambda t: -t.priority)
    
    def get_next(self, claw_id: str) -> Optional[SubTask]:
        for t in self.tasks:
            if t.status == "pending" and (not t.claw_id or t.claw_id == claw_id):
                return t
        return None
    
    def mark_done(self, task_id: str, result: Any):
        for t in self.tasks:
            if t.id == task_id:
                t.status = "done"
                t.result = result
                t.completed_at = datetime.now()

class ClawCoordinator:
    """多Claw协作调度器"""
    
    def __init__(self):
        self.claws: Dict[str, Any] = {}  # claw_id -> claw实例
        self.queues: Dict[str, TaskQueue] = {}  # queue_name -> 队列
    
    def register_claw(self, claw_id: str, claw):
        """注册Claw实例"""
        self.claws[claw_id] = claw
    
    def create_queue(self, name: str) -> TaskQueue:
        """创建队列"""
        q = TaskQueue(name=name)
        self.queues[name] = q
        return q
    
    async def dispatch(self, queue_name: str) -> Dict[str, Any]:
        """分发任务给Claws"""
        q = self.queues.get(queue_name)
        if not q:
            return {"error": f"队列{queue_name}不存在"}
        
        # 并行执行所有pending任务
        results = []
        for claw_id, claw in self.claws.items():
            task = q.get_next(claw_id)
            if task:
                task.claw_id = claw_id
                task.status = "running"
                
                # 执行
                try:
                    result = await claw.run(task.content)
                    q.mark_done(task.id, result)
                    results.append({"claw": claw_id, "task": task.id, "status": "done"})
                except Exception as e:
                    task.status = "failed"
                    results.append({"claw": claw_id, "task": task.id, "status": "failed", "error": "操作失败"})
        
        return {"dispatched": len(results), "results": results}
    
    async def wait_all(self, queue_name: str, timeout: int = 60) -> List[Dict]:
        """等待所有任务完成"""
        q = self.queues.get(queue_name)
        if not q:
            return []
        
        # 简单轮询等待
        import time
        start = time.time()
        while time.time() - start < timeout:
            pending = [t for t in q.tasks if t.status == "pending"]
            if not pending:
                break
            await asyncio.sleep(0.5)
        
        return [{"id": t.id, "status": t.status, "result": t.result} for t in q.tasks]

# 全局调度器
_coordinator = None

def get_coordinator() -> ClawCoordinator:
    global _coordinator
    if _coordinator is None:
        _coordinator = ClawCoordinator()
    return _coordinator

__all__ = ["SubTask", "TaskQueue", "ClawCoordinator", "get_coordinator", "Priority"]
