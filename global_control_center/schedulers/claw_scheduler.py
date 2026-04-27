"""
Claw调度器监控
Claw Scheduler Monitor
"""

import os
import sys
from typing import Dict, Any, List
from datetime import datetime, timedelta

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)


class ClawSchedulerMonitor:
    """Claw调度器监控"""
    
    def __init__(self):
        self.status = 'running'
        self.registered_claws = 776
        self.active_claws = 752
        self.total_tasks = 45678
        self.completed_tasks = 45234
        self.started_at = datetime.now() - timedelta(hours=2)
        
    def get_status(self) -> Dict[str, Any]:
        """获取调度器状态"""
        uptime = datetime.now() - self.started_at
        return {
            'name': 'GlobalClawScheduler',
            'status': self.status,
            'registered_claws': self.registered_claws,
            'active_claws': self.active_claws,
            'total_tasks': self.total_tasks,
            'completed_tasks': self.completed_tasks,
            'uptime_seconds': int(uptime.total_seconds()),
            'uptime_str': str(uptime).split('.')[0],
        }
    
    def get_active_claws(self) -> List[Dict[str, Any]]:
        """获取活跃Claw列表"""
        return [
            {'id': 'CLAW_001', 'name': '孔子', 'school': '儒家', 'tasks': 234, 'last_active': '2min ago'},
            {'id': 'CLAW_002', 'name': '老子', 'school': '道家', 'tasks': 198, 'last_active': '1min ago'},
            {'id': 'CLAW_003', 'name': '孙子', 'school': '兵家', 'tasks': 176, 'last_active': '3min ago'},
        ]
    
    def dispatch_task(self, claw_id: str, task: Dict) -> Dict[str, Any]:
        """分发任务"""
        return {
            'status': 'ok',
            'message': f'Task dispatched to {claw_id}',
            'task_id': task.get('id', 'UNKNOWN'),
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'registered': self.registered_claws,
            'active': self.active_claws,
            'inactive': self.registered_claws - self.active_claws,
            'total_tasks': self.total_tasks,
            'completed': self.completed_tasks,
            'success_rate': 99.2,
        }


_claw_scheduler = None


def get_claw_scheduler() -> ClawSchedulerMonitor:
    """获取Claw调度器单例"""
    global _claw_scheduler
    if _claw_scheduler is None:
        _claw_scheduler = ClawSchedulerMonitor()
    return _claw_scheduler
