"""
__all__ = [
    'are_all_modules_ready',
    'get_all_states',
    'get_dependencies',
    'get_dependents',
    'get_initialization_order',
    'get_module',
    'get_module_state',
    'get_system_health',
    'initialize_all',
    'is_healthy',
    'on_state_change',
    'register_module',
    'shutdown_all',
    'to_dict',
    'update_health_score',
    'update_metadata',
    'visit',
]

模块协调器
Module Coordinator

管理模块间的依赖关系,生命周期和状态同步
"""

import asyncio
import logging
from datetime import datetime
from typing import Callable, Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum, auto

logger = logging.getLogger(__name__)

class ModuleStatus(Enum):
    """模块状态"""
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"
    SHUTDOWN = "shutdown"

class ModuleType(Enum):
    """模块类型"""
    EVOLUTION_ENGINE = "evolution_engine"
    KNOWLEDGE_GRAPH = "knowledge_graph"
    GROWTH_STRATEGIES = "growth_strategies"

@dataclass
class ModuleState:
    """模块状态"""
    module_type: ModuleType
    module_name: str
    status: ModuleStatus
    version: str
    capabilities: List[str]
    health_score: float = 100.0
    last_heartbeat: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_healthy(self) -> bool:
        return self.health_score >= 80 and self.status in [ModuleStatus.READY, ModuleStatus.RUNNING]
    
    def to_dict(self) -> Dict:
        return {
            "module_type": self.module_type.value,
            "module_name": self.module_name,
            "status": self.status.value,
            "version": self.version,
            "capabilities": self.capabilities,
            "health_score": self.health_score,
            "last_heartbeat": self.last_heartbeat.isoformat(),
            "metadata": self.metadata
        }

@dataclass
class DependencyGraph:
    """依赖图"""
    dependencies: Dict[ModuleType, Set[ModuleType]] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.dependencies:
            # 定义默认依赖关系
            self.dependencies = {
                ModuleType.EVOLUTION_ENGINE: set(),  # 进化引擎不依赖其他模块
                ModuleType.KNOWLEDGE_GRAPH: {ModuleType.EVOLUTION_ENGINE},  # 知识图谱依赖进化引擎
                ModuleType.GROWTH_STRATEGIES: {ModuleType.KNOWLEDGE_GRAPH, ModuleType.EVOLUTION_ENGINE}  # 增长strategy依赖其他两个
            }
    
    def get_dependencies(self, module: ModuleType) -> Set[ModuleType]:
        """get模块的依赖"""
        return self.dependencies.get(module, set())
    
    def get_dependents(self, module: ModuleType) -> Set[ModuleType]:
        """get依赖于该模块的其他模块"""
        dependents = set()
        for m, deps in self.dependencies.items():
            if module in deps:
                dependents.add(m)
        return dependents
    
    def get_initialization_order(self) -> List[ModuleType]:
        """getinit顺序(拓扑排序)"""
        visited = set()
        order = []
        
        def visit(m: ModuleType):
            if m in visited:
                return
            visited.add(m)
            for dep in self.get_dependencies(m):
                visit(dep)
            order.append(m)
        
        for module in ModuleType:
            visit(module)
        
        return order

class ModuleCoordinator:
    """模块协调器"""
    
    def __init__(self):
        self._modules: Dict[ModuleType, Any] = {}
        self._states: Dict[ModuleType, ModuleState] = {}
        self._dependency_graph = DependencyGraph()
        self._lock = asyncio.Lock()
        self._state_change_callbacks: List[Callable] = []
    
    def register_module(self, module_type: ModuleType, module_instance: Any,
                       module_name: str, version: str, capabilities: List[str]):
        """注册模块"""
        self._modules[module_type] = module_instance
        self._states[module_type] = ModuleState(
            module_type=module_type,
            module_name=module_name,
            status=ModuleStatus.INITIALIZING,
            version=version,
            capabilities=capabilities
        )
        logger.info(f"模块注册成功: {module_type.value} ({module_name} v{version})")
    
    async def initialize_all(self) -> Dict[ModuleType, bool]:
        """按依赖顺序init_all模块"""
        order = self._dependency_graph.get_initialization_order()
        results = {}
        
        for module_type in order:
            if module_type in self._modules:
                try:
                    await self._initialize_module(module_type)
                    results[module_type] = True
                except Exception as e:
                    logger.error(f"模块init失败 {module_type.value}: {e}")
                    results[module_type] = False
                    await self._set_module_status(module_type, ModuleStatus.ERROR)
        
        return results
    
    async def _initialize_module(self, module_type: ModuleType):
        """init单个模块"""
        async with self._lock:
            module = self._modules.get(module_type)
            if not module:
                raise ValueError(f"模块未注册: {module_type.value}")
            
            # 检查依赖是否已就绪
            for dep in self._dependency_graph.get_dependencies(module_type):
                if dep in self._states:
                    if not self._states[dep].is_healthy():
                        raise RuntimeError(f"依赖模块未就绪: {dep.value}")
            
            # 调用模块的init方法(如果存在)
            if hasattr(module, 'initialize'):
                if asyncio.iscoroutinefunction(module.initialize):
                    await module.initialize()
                else:
                    module.initialize()
            
            await self._set_module_status(module_type, ModuleStatus.READY)
            logger.info(f"模块init完成: {module_type.value}")
    
    async def _set_module_status(self, module_type: ModuleType, status: ModuleStatus):
        """设置模块状态"""
        if module_type in self._states:
            old_status = self._states[module_type].status
            self._states[module_type].status = status
            self._states[module_type].last_heartbeat = datetime.now()
            
            # 触发状态变更回调
            for callback in self._state_change_callbacks:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(module_type, old_status, status)
                    else:
                        callback(module_type, old_status, status)
                except Exception as e:
                    logger.error(f"状态变更回调失败: {e}")
    
    def on_state_change(self, callback: Callable):
        """注册状态变更回调"""
        self._state_change_callbacks.append(callback)
    
    def get_module(self, module_type: ModuleType) -> Optional[Any]:
        """get模块实例"""
        return self._modules.get(module_type)
    
    def get_module_state(self, module_type: ModuleType) -> Optional[ModuleState]:
        """get模块状态"""
        return self._states.get(module_type)
    
    def get_all_states(self) -> Dict[ModuleType, ModuleState]:
        """get所有模块状态"""
        return self._states.copy()
    
    def are_all_modules_ready(self) -> bool:
        """检查所有模块是否就绪"""
        return all(
            state.is_healthy()
            for state in self._states.values()
        )
    
    async def update_health_score(self, module_type: ModuleType, score: float):
        """更新模块健康分数"""
        async with self._lock:
            if module_type in self._states:
                self._states[module_type].health_score = max(0, min(100, score))
                self._states[module_type].last_heartbeat = datetime.now()
    
    async def update_metadata(self, module_type: ModuleType, metadata: Dict[str, Any]):
        """更新模块元数据"""
        async with self._lock:
            if module_type in self._states:
                self._states[module_type].metadata.update(metadata)
    
    def get_system_health(self) -> Dict[str, Any]:
        """get系统整体健康状态"""
        if not self._states:
            return {"overall_score": 0, "status": "no_modules"}
        
        scores = [s.health_score for s in self._states.values()]
        overall_score = sum(scores) / len(scores)
        
        healthy_count = sum(1 for s in self._states.values() if s.is_healthy())
        
        return {
            "overall_score": overall_score,
            "module_count": len(self._states),
            "healthy_count": healthy_count,
            "unhealthy_count": len(self._states) - healthy_count,
            "status": "healthy" if healthy_count == len(self._states) else "degraded",
            "modules": {m.value: s.to_dict() for m, s in self._states.items()}
        }
    
    async def shutdown_all(self):
        """关闭所有模块"""
        for module_type in reversed(self._dependency_graph.get_initialization_order()):
            if module_type in self._modules:
                try:
                    module = self._modules[module_type]
                    if hasattr(module, 'shutdown'):
                        if asyncio.iscoroutinefunction(module.shutdown):
                            await module.shutdown()
                        else:
                            module.shutdown()
                    
                    await self._set_module_status(module_type, ModuleStatus.SHUTDOWN)
                    logger.info(f"模块已关闭: {module_type.value}")
                except Exception as e:
                    logger.error(f"模块关闭失败 {module_type.value}: {e}")

# 全局协调器实例
coordinator = ModuleCoordinator()
