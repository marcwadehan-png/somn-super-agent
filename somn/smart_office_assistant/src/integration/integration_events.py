"""
__all__ = [
    'create_correlation_id',
    'get_event_history',
    'get_handler_stats',
    'handle',
    'publish',
    'publish_sync',
    'subscribe',
    'to_dict',
]

集成事件总线
Integration Event Bus

实现模块间的事件驱动通信机制
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import defaultdict

logger = logging.getLogger(__name__)

class EventType(Enum):
    """事件类型"""
    # 进化引擎事件
    EVOLUTION_STARTED = "evolution_started"
    EVOLUTION_COMPLETED = "evolution_completed"
    EVOLUTION_FAILED = "evolution_failed"
    HEALTH_STATUS_CHANGED = "health_status_changed"
    ANOMALY_DETECTED = "anomaly_detected"
    
    # 知识图谱事件
    KNOWLEDGE_UPDATED = "knowledge_updated"
    ENTITY_ADDED = "entity_added"
    RELATION_INFERRED = "relation_inferred"
    CASE_STUDY_ADDED = "case_study_added"
    INDUSTRY_COMPARED = "industry_compared"
    
    # 增长strategy事件
    STRATEGY_ACTIVATED = "strategy_activated"
    EXPERIMENT_STARTED = "experiment_started"
    EXPERIMENT_COMPLETED = "experiment_completed"
    GROWTH_MILESTONE = "growth_milestone"
    ATTRIBUTION_ANALYZED = "attribution_analyzed"
    
    # 集成事件
    CROSS_MODULE_SYNC = "cross_module_sync"
    WORKFLOW_TRIGGERED = "workflow_triggered"
    ALERT_GENERATED = "alert_generated"

class EventPriority(Enum):
    """事件优先级"""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4

@dataclass
class IntegrationEvent:
    """集成事件"""
    event_id: str
    event_type: EventType
    source_module: str
    payload: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    priority: EventPriority = EventPriority.NORMAL
    correlation_id: Optional[str] = None  # 关联ID,用于追踪事件链
    
    def to_dict(self) -> Dict:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "source_module": self.source_module,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "priority": self.priority.value,
            "correlation_id": self.correlation_id
        }

class EventHandler:
    """事件处理器"""
    def __init__(self, handler_func: Callable, event_types: List[EventType],
                 priority: EventPriority = EventPriority.NORMAL):
        self.handler_func = handler_func
        self.event_types = event_types
        self.priority = priority
        self.call_count = 0
        self.last_called = None
    
    async def handle(self, event: IntegrationEvent) -> Any:
        """处理事件"""
        self.call_count += 1
        self.last_called = datetime.now()
        try:
            result = await self.handler_func(event)
            return result
        except Exception as e:
            logger.error(f"事件处理失败 {event.event_id}: {e}")
            raise

class IntegrationEventBus:
    """集成事件总线"""
    
    def __init__(self):
        self._handlers: Dict[EventType, List[EventHandler]] = defaultdict(list)
        self._event_history: List[IntegrationEvent] = []
        self._max_history = 1000
        self._lock = asyncio.Lock()
        self._event_count = 0
    
    def subscribe(self, event_types: List[EventType], handler_func: Callable,
                  priority: EventPriority = EventPriority.NORMAL) -> str:
        """订阅事件"""
        handler_id = f"handler_{len(self._handlers)}_{id(handler_func)}"
        handler = EventHandler(handler_func, event_types, priority)
        
        for event_type in event_types:
            self._handlers[event_type].append(handler)
            # 按优先级排序
            self._handlers[event_type].sort(key=lambda h: h.priority.value)
        
        logger.info(f"事件处理器订阅成功: {handler_id} -> {[e.value for e in event_types]}")
        return handler_id
    
    async def publish(self, event: IntegrationEvent) -> List[Any]:
        """发布事件"""
        async with self._lock:
            self._event_count += 1
            self._event_history.append(event)
            
            # 限制历史记录大小
            if len(self._event_history) > self._max_history:
                self._event_history = self._event_history[-self._max_history:]
        
        results = []
        handlers = self._handlers.get(event.event_type, [])
        
        for handler in handlers:
            try:
                result = await handler.handle(event)
                results.append(result)
            except Exception as e:
                logger.error(f"事件处理器执行失败: {e}")
        
        logger.debug(f"事件发布完成: {event.event_type.value}, 处理器数量: {len(handlers)}")
        return results
    
    async def publish_sync(self, source_module: str, event_type: EventType,
                          payload: Dict[str, Any], 
                          priority: EventPriority = EventPriority.NORMAL,
                          correlation_id: Optional[str] = None) -> List[Any]:
        """便捷方法:创建并发布事件"""
        event_id = f"evt_{self._event_count}_{datetime.now().timestamp()}"
        event = IntegrationEvent(
            event_id=event_id,
            event_type=event_type,
            source_module=source_module,
            payload=payload,
            priority=priority,
            correlation_id=correlation_id
        )
        return await self.publish(event)
    
    def get_event_history(self, event_type: Optional[EventType] = None,
                         source_module: Optional[str] = None,
                         limit: int = 100) -> List[IntegrationEvent]:
        """get事件历史"""
        filtered = self._event_history
        
        if event_type:
            filtered = [e for e in filtered if e.event_type == event_type]
        if source_module:
            filtered = [e for e in filtered if e.source_module == source_module]
        
        return filtered[-limit:]
    
    def get_handler_stats(self) -> Dict[str, Any]:
        """get处理器统计"""
        stats = {}
        for event_type, handlers in self._handlers.items():
            stats[event_type.value] = {
                "handler_count": len(handlers),
                "handlers": [
                    {
                        "call_count": h.call_count,
                        "last_called": h.last_called.isoformat() if h.last_called else None,
                        "priority": h.priority.name
                    }
                    for h in handlers
                ]
            }
        return stats
    
    def create_correlation_id(self) -> str:
        """创建关联ID"""
        return f"corr_{self._event_count}_{datetime.now().timestamp()}"

# 全局事件总线实例
event_bus = IntegrationEventBus()
