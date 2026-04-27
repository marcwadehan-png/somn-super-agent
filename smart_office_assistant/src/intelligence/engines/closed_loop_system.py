# -*- coding: utf-8 -*-
"""
__all__ = [
    'add_feedback',
    'add_node',
    'close_stale_loops',
    'complete_node',
    'create_closed_loop_system',
    'create_loop',
    'ensure_closed_loop',
    'generate_report',
    'get_loop_analytics',
    'get_loop_status',
    'get_open_loops',
    'get_progress',
    'is_closed',
    'to_dict',
]

闭环思维系统 v1.0.0
Closed Loop Thinking System

核心思想:
- 有输入必有输出,有action必有反馈
- 信息形成回路,decision形成闭环
- PDCA循环:计划-执行-检查-改进
- 事事有回应,件件有着落

作者:Somn AI
版本:v1.0.0
日期:2026-04-02
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
import uuid

# FeedbackType 从通用枚举导入（与 _common_enums 保持一致）
try:
    from ._common_enums import FeedbackType
except ImportError:
    # 备用：本地定义（避免循环依赖）
    class FeedbackType(Enum):
        POSITIVE = "positive"
        NEGATIVE = "negative"
        NEUTRAL = "neutral"
        ADAPTIVE = "adaptive"

class LoopStatus(Enum):
    """闭环状态"""
    OPEN = "未开始"  # 任务已创建但未开始
    IN_PROGRESS = "进行中"  # 任务执行中
    PENDING_REVIEW = "待检查"  # 执行完成,等待检查
    PENDING_IMPROVEMENT = "待改进"  # 发现问题,需要改进
    CLOSED = "已完成"  # 闭环完成
    OVERDUE = "已超时"  # 任务超时未完成

class ClosedLoopFeedbackType(Enum):
    """闭环系统反馈类型（区别于其他模块的FeedbackType）"""
    POSITIVE = "正向反馈"  # 认可,鼓励
    NEGATIVE = "负向反馈"  # 批评,指正
    NEUTRAL = "中性反馈"  # 信息性反馈
    CONSTRUCTIVE = "建设性反馈"  # 提供改进建议

@dataclass
class LoopNode:
    """闭环节点"""
    node_id: str
    node_type: str  # "input" | "action" | "output" | "feedback" | "improvement"
    description: str
    responsible: str = ""  # 责任人
    deadline: Optional[datetime] = None
    status: LoopStatus = LoopStatus.OPEN
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "description": self.description,
            "responsible": self.responsible,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }

@dataclass
class ClosedLoop:
    """闭环实例"""
    loop_id: str
    name: str
    description: str
    nodes: List[LoopNode] = field(default_factory=list)
    connections: List[tuple] = field(default_factory=list)  # (from_id, to_id)
    current_node_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    metadata: Dict = field(default_factory=dict)
    
    def is_closed(self) -> bool:
        return all(n.status == LoopStatus.CLOSED for n in self.nodes)
    
    def get_progress(self) -> float:
        if not self.nodes:
            return 0.0
        closed_count = sum(1 for n in self.nodes if n.status == LoopStatus.CLOSED)
        return closed_count / len(self.nodes) * 100
    
    def to_dict(self) -> Dict:
        return {
            "loop_id": self.loop_id,
            "name": self.name,
            "description": self.description,
            "progress": round(self.get_progress(), 1),
            "is_closed": self.is_closed(),
            "current_node": self.current_node_id,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "nodes": [n.to_dict() for n in self.nodes]
        }

@dataclass
class Feedback:
    """反馈记录"""
    feedback_id: str
    source_node_id: str
    target_node_id: str
    feedback_type: FeedbackType
    content: str
    rating: int = 0  # 1-5星评分
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "feedback_id": self.feedback_id,
            "source_node_id": self.source_node_id,
            "target_node_id": self.target_node_id,
            "feedback_type": self.feedback_type.value,
            "content": self.content,
            "rating": self.rating,
            "created_at": self.created_at.isoformat()
        }

class ClosedLoopThinkingSystem:
    """
    闭环思维系统
    
    确保每个任务,每个decision都形成完整闭环.
    
    主要功能:
    1. 创建和管理闭环
    2. 追踪闭环状态
    3. 收集和记录反馈
    4. 持续改进
    5. generate闭环报告
    """
    
    def __init__(self):
        self.loops: Dict[str, ClosedLoop] = {}
        self.feedbacks: List[Feedback] = []
        self.loop_templates: Dict[str, Dict] = self._init_templates()
    
    def _init_templates(self) -> Dict[str, Dict]:
        """init闭环模板"""
        return {
            "pdca": {
                "name": "PDCA循环",
                "description": "计划-执行-检查-改进",
                "nodes": [
                    {"type": "input", "name": "P-计划", "desc": "制定目标和计划"},
                    {"type": "action", "name": "D-执行", "desc": "实施计划"},
                    {"type": "output", "name": "C-检查", "desc": "检查执行结果"},
                    {"type": "improvement", "name": "A-改进", "desc": "总结改进"}
                ]
            },
            "basic": {
                "name": "基本闭环",
                "description": "输入-action-输出-反馈",
                "nodes": [
                    {"type": "input", "name": "输入", "desc": "明确任务输入"},
                    {"type": "action", "name": "action", "desc": "执行任务"},
                    {"type": "output", "name": "输出", "desc": "产出结果"},
                    {"type": "feedback", "name": "反馈", "desc": "收集反馈"}
                ]
            },
            "decision": {
                "name": "decision闭环",
                "description": "问题-方案-decision-执行-复盘",
                "nodes": [
                    {"type": "input", "name": "问题recognize", "desc": "明确要解决的问题"},
                    {"type": "action", "name": "方案设计", "desc": "设计多个解决方案"},
                    {"type": "output", "name": "decision选择", "desc": "选择最佳方案"},
                    {"type": "action", "name": "执行实施", "desc": "执行decision"},
                    {"type": "feedback", "name": "复盘总结", "desc": "复盘decision效果"}
                ]
            },
            "task": {
                "name": "任务闭环",
                "description": "接收-执行-汇报-确认",
                "nodes": [
                    {"type": "input", "name": "任务接收", "desc": "明确任务要求"},
                    {"type": "action", "name": "执行任务", "desc": "执行任务"},
                    {"type": "output", "name": "结果汇报", "desc": "汇报执行结果"},
                    {"type": "feedback", "name": "确认验收", "desc": "获得确认"}
                ]
            }
        }
    
    def create_loop(self, name: str, description: str = "", 
                    template: str = "basic", metadata: Dict = None) -> ClosedLoop:
        """
        创建新的闭环
        
        Args:
            name: 闭环名称
            description: 闭环描述
            template: 闭环模板
            metadata: 附加信息
            
        Returns:
            ClosedLoop: 创建的闭环实例
        """
        loop_id = str(uuid.uuid4())[:8]
        loop = ClosedLoop(
            loop_id=loop_id,
            name=name,
            description=description,
            metadata=metadata or {}
        )
        
        # 根据模板添加节点
        if template in self.loop_templates:
            tmpl = self.loop_templates[template]
            for node_def in tmpl["nodes"]:
                node = LoopNode(
                    node_id=str(uuid.uuid4())[:8],
                    node_type=node_def["type"],
                    description=f"{node_def['name']}: {node_def['desc']}"
                )
                loop.nodes.append(node)
        
        # 设置第一个节点为当前节点
        if loop.nodes:
            loop.current_node_id = loop.nodes[0].node_id
        
        self.loops[loop_id] = loop
        return loop
    
    def add_node(self, loop_id: str, node_type: str, description: str,
                 responsible: str = "", deadline: Optional[datetime] = None) -> Optional[LoopNode]:
        """在闭环中添加节点"""
        if loop_id not in self.loops:
            return None
        
        node = LoopNode(
            node_id=str(uuid.uuid4())[:8],
            node_type=node_type,
            description=description,
            responsible=responsible,
            deadline=deadline
        )
        
        self.loops[loop_id].nodes.append(node)
        return node
    
    def complete_node(self, loop_id: str, node_id: str) -> bool:
        """标记节点完成"""
        if loop_id not in self.loops:
            return False
        
        loop = self.loops[loop_id]
        for node in loop.nodes:
            if node.node_id == node_id:
                node.status = LoopStatus.CLOSED
                node.completed_at = datetime.now()
                
                # 自动移动到下一个节点
                idx = loop.nodes.index(node)
                if idx + 1 < len(loop.nodes):
                    loop.current_node_id = loop.nodes[idx + 1].node_id
                else:
                    loop.current_node_id = None
                    loop.completed_at = datetime.now()
                return True
        return False
    
    def add_feedback(self, loop_id: str, node_id: str, 
                    feedback_type: FeedbackType, content: str,
                    rating: int = 0) -> Optional[Feedback]:
        """添加反馈"""
        if loop_id not in self.loops:
            return None
        
        feedback = Feedback(
            feedback_id=str(uuid.uuid4())[:8],
            source_node_id=node_id,
            target_node_id=loop_id,
            feedback_type=feedback_type,
            content=content,
            rating=rating
        )
        
        self.feedbacks.append(feedback)
        
        # 如果是负向反馈,可能需要添加改进节点
        if feedback_type == ClosedLoopFeedbackType.NEGATIVE:
            self._add_improvement_node(loop_id, content)
        
        return feedback
    
    def _add_improvement_node(self, loop_id: str, issue: str):
        """为问题添加改进节点"""
        self.add_node(
            loop_id=loop_id,
            node_type="improvement",
            description=f"改进:{issue}"
        )
    
    def get_loop_status(self, loop_id: str) -> Optional[Dict]:
        """get闭环状态"""
        if loop_id not in self.loops:
            return None
        
        loop = self.loops[loop_id]
        
        # 检查超时
        now = datetime.now()
        for node in loop.nodes:
            if node.deadline and node.status != LoopStatus.CLOSED:
                if now > node.deadline:
                    node.status = LoopStatus.OVERDUE
        
        return {
            "loop_id": loop.loop_id,
            "name": loop.name,
            "status": "已闭环" if loop.is_closed() else "进行中",
            "progress": round(loop.get_progress(), 1),
            "current_node": loop.current_node_id,
            "overdue_count": sum(1 for n in loop.nodes if n.status == LoopStatus.OVERDUE),
            "node_summary": self._summarize_nodes(loop),
            "created_at": loop.created_at.isoformat(),
            "completed_at": loop.completed_at.isoformat() if loop.completed_at else None
        }
    
    def _summarize_nodes(self, loop: ClosedLoop) -> Dict:
        """总结节点状态"""
        summary = defaultdict(int)
        for node in loop.nodes:
            summary[node.status.value] += 1
        return dict(summary)
    
    def get_open_loops(self) -> List[Dict]:
        """get所有未闭环的任务"""
        open_loops = []
        for loop in self.loops.values():
            if not loop.is_closed():
                status = self.get_loop_status(loop.loop_id)
                if status:
                    open_loops.append(status)
        return sorted(open_loops, key=lambda x: x["progress"])
    
    def get_loop_analytics(self) -> Dict:
        """get闭环分析统计"""
        total_loops = len(self.loops)
        closed_loops = sum(1 for l in self.loops.values() if l.is_closed())
        open_loops = total_loops - closed_loops
        
        # 计算平均完成时间
        completed_with_time = [l for l in self.loops.values() 
                             if l.completed_at and l.created_at]
        
        avg_completion_time = 0
        if completed_with_time:
            total_time = sum((l.completed_at - l.created_at).total_seconds() 
                           for l in completed_with_time)
            avg_completion_time = total_time / len(completed_with_time) / 3600  # 转换为小时
        
        # 反馈统计
        feedback_stats = defaultdict(int)
        for fb in self.feedbacks:
            feedback_stats[fb.feedback_type.value] += 1
        
        avg_rating = 0
        rated_feedbacks = [fb for fb in self.feedbacks if fb.rating > 0]
        if rated_feedbacks:
            avg_rating = sum(fb.rating for fb in rated_feedbacks) / len(rated_feedbacks)
        
        return {
            "total_loops": total_loops,
            "closed_loops": closed_loops,
            "open_loops": open_loops,
            "closure_rate": round(closed_loops / total_loops * 100, 1) if total_loops > 0 else 0,
            "avg_completion_time_hours": round(avg_completion_time, 1),
            "feedback_stats": dict(feedback_stats),
            "avg_rating": round(avg_rating, 2),
            "total_feedbacks": len(self.feedbacks)
        }
    
    def generate_report(self, loop_id: str) -> str:
        """generate闭环报告"""
        if loop_id not in self.loops:
            return "闭环不存在"
        
        loop = self.loops[loop_id]
        status = self.get_loop_status(loop_id)
        
        report = f"""
{'='*50}
闭环报告:{loop.name}
{'='*50}

基本信息
--------
闭环ID: {loop.loop_id}
描述: {loop.description}
创建时间: {loop.created_at.strftime('%Y-%m-%d %H:%M:%S')}
完成时间: {loop.completed_at.strftime('%Y-%m-%d %H:%M:%S') if loop.completed_at else '进行中'}

执行状态
--------
进度: {status['progress']}%
状态: {status['status']}
超时任务: {status['overdue_count']}个

节点详情
--------
"""
        
        for i, node in enumerate(loop.nodes, 1):
            report += f"\n{i}. {node.description}\n"
            report += f"   责任人: {node.responsible or '未指定'}\n"
            report += f"   状态: {node.status.value}\n"
            if node.deadline:
                report += f"   截止: {node.deadline.strftime('%Y-%m-%d %H:%M')}\n"
            if node.completed_at:
                report += f"   完成: {node.completed_at.strftime('%Y-%m-%d %H:%M')}\n"
        
        # 添加反馈摘要
        loop_feedbacks = [fb for fb in self.feedbacks if fb.target_node_id == loop_id]
        if loop_feedbacks:
            report += f"""
反馈记录
--------
共{len(loop_feedbacks)}条反馈
"""
            for fb in loop_feedbacks[-5:]:
                report += f"- [{fb.feedback_type.value}] {fb.content[:50]}...\n"
        
        report += f"\n{'='*50}\n"
        return report
    
    def close_stale_loops(self, days: int = 7) -> int:
        """关闭超时的闭环"""
        cutoff = datetime.now() - timedelta(days=days)
        count = 0
        
        for loop in self.loops.values():
            if loop.created_at < cutoff and not loop.is_closed():
                # 将所有未完成的节点标记为关闭
                for node in loop.nodes:
                    if node.status != LoopStatus.CLOSED:
                        node.status = LoopStatus.CLOSED
                loop.completed_at = datetime.now()
                count += 1
        
        return count
    
    def ensure_closed_loop(self, task: str, executor: Callable, 
                          on_error: Optional[Callable] = None) -> Any:
        """
        确保任务形成闭环
        
        Args:
            task: 任务描述
            executor: 执行函数
            on_error: 错误处理函数
            
        Returns:
            执行结果
        """
        # 创建闭环
        loop = self.create_loop(
            name=task,
            description=f"执行任务: {task}",
            template="task"
        )
        
        try:
            # 执行
            result = executor()
            
            # 完成节点
            for node in loop.nodes:
                self.complete_node(loop.loop_id, node.node_id)
            
            return result
            
        except Exception as e:
            # 记录错误
            self.add_feedback(
                loop_id=loop.loop_id,
                node_id=loop.nodes[0].node_id,
                feedback_type=ClosedLoopFeedbackType.NEGATIVE,
                content=f"执行出错"
            )
            
            if on_error:
                return on_error(e)
            raise

def create_closed_loop_system() -> ClosedLoopThinkingSystem:
    """工厂函数"""
    return ClosedLoopThinkingSystem()
