"""
__all__ = [
    'adapt_strategy',
    'add_metric',
    'allocate_resource',
    'available',
    'check_balance',
    'detect_changes',
    'deviation',
    'evolve',
    'generate_alerts',
    'generate_report',
    'get_evolution_report',
    'get_health_status',
    'get_optimization_suggestions',
    'get_overall_health',
    'get_utilization_report',
    'health_status',
    'initialize',
    'monitor',
    'observe_environment',
    'predict_trend',
    'record_environment',
    'register_resource',
    'release_resource',
    'scarcity',
    'suggest_improvements',
    'update_metric',
    'utilization',
]

生态智能系统 - 基于沙丘生态学思维

核心哲学思想:
- 生态平衡 - 系统各部分相互依赖
- 资源稀缺 - 香料隐喻的关键资源
- 环境适应 - 弗里曼人的生存智慧
- 长期演化 - 缓慢但深刻的改变
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import time
from collections import defaultdict
import statistics

class HealthStatus(Enum):
    """健康状态"""
    EXCELLENT = "excellent"      # 优秀
    GOOD = "good"               # 良好
    FAIR = "fair"               # 一般
    POOR = "poor"               # 较差
    CRITICAL = "critical"       # 危急

class ResourceType(Enum):
    """资源类型"""
    CPU = "cpu"                 # CPU资源
    MEMORY = "memory"           # 内存资源
    STORAGE = "storage"         # 存储资源
    NETWORK = "network"         # 网络资源
    TOKEN = "token"             # Token资源
    TIME = "time"               # 时间资源

@dataclass
class EcosystemMetric:
    """生态metrics"""
    name: str                   # metrics名称
    value: float                # 当前值
    target: float               # 目标值
    min_acceptable: float       # 最小可接受值
    max_acceptable: float       # 最大可接受值
    unit: str                   # 单位
    timestamp: float = field(default_factory=time.time)
    
    @property
    def health_status(self) -> HealthStatus:
        """健康状态"""
        if self.target * 0.9 <= self.value <= self.target * 1.1:
            return HealthStatus.EXCELLENT
        elif self.min_acceptable <= self.value <= self.max_acceptable:
            return HealthStatus.GOOD
        elif self.value < self.min_acceptable * 0.8 or self.value > self.max_acceptable * 1.2:
            return HealthStatus.FAIR
        elif self.value < self.min_acceptable * 0.5 or self.value > self.max_acceptable * 1.5:
            return HealthStatus.POOR
        else:
            return HealthStatus.CRITICAL
    
    @property
    def deviation(self) -> float:
        """偏差百分比"""
        return abs(self.value - self.target) / self.target * 100

@dataclass
class ResourceAllocation:
    """资源分配"""
    resource_type: ResourceType
    allocated: float            # 已分配
    total: float                # 总量
    unit: str = ""
    
    @property
    def utilization(self) -> float:
        """利用率"""
        return self.allocated / self.total * 100
    
    @property
    def available(self) -> float:
        """可用量"""
        return self.total - self.allocated
    
    @property
    def scarcity(self) -> float:
        """稀缺程度 (0-1, 越高越稀缺)"""
        return self.allocated / self.total

class EcosystemManager:
    """
    生态系统管理器
    
    核心功能:
    - 监控系统各模块的健康度
    - 维持生态平衡
    - 检测和修复异常
    - generate生态报告
    """
    
    def __init__(self):
        self.metrics: Dict[str, EcosystemMetric] = {}
        self.alerts: List[Dict[str, Any]] = []
        self.history: Dict[str, List[float]] = defaultdict(list)
        
    def add_metric(self, metric: EcosystemMetric) -> None:
        """添加metrics"""
        self.metrics[metric.name] = metric
        
    def update_metric(self, name: str, value: float) -> None:
        """更新metrics"""
        if name in self.metrics:
            self.metrics[name].value = value
            self.metrics[name].timestamp = time.time()
            self.history[name].append(value)
            # 只保留最近100个历史值
            if len(self.history[name]) > 100:
                self.history[name] = self.history[name][-100:]
    
    def get_health_status(self) -> Dict[str, HealthStatus]:
        """get所有metrics的健康状态"""
        return {name: metric.health_status for name, metric in self.metrics.items()}
    
    def get_overall_health(self) -> HealthStatus:
        """get整体健康状态"""
        statuses = self.get_health_status().values()
        
        if all(s == HealthStatus.EXCELLENT for s in statuses):
            return HealthStatus.EXCELLENT
        elif all(s in [HealthStatus.EXCELLENT, HealthStatus.GOOD] for s in statuses):
            return HealthStatus.GOOD
        elif HealthStatus.CRITICAL in statuses:
            return HealthStatus.CRITICAL
        elif HealthStatus.POOR in statuses:
            return HealthStatus.POOR
        else:
            return HealthStatus.FAIR
    
    def check_balance(self) -> bool:
        """检查生态平衡"""
        overall_health = self.get_overall_health()
        return overall_health in [HealthStatus.EXCELLENT, HealthStatus.GOOD]
    
    def generate_alerts(self) -> List[Dict[str, Any]]:
        """generate警报"""
        alerts = []
        
        for name, metric in self.metrics.items():
            status = metric.health_status
            if status in [HealthStatus.POOR, HealthStatus.CRITICAL]:
                alert = {
                    "metric": name,
                    "status": status.value,
                    "value": metric.value,
                    "target": metric.target,
                    "deviation": metric.deviation,
                    "timestamp": metric.timestamp,
                    "severity": "high" if status == HealthStatus.CRITICAL else "medium"
                }
                alerts.append(alert)
        
        self.alerts = alerts
        return alerts
    
    def generate_report(self) -> Dict[str, Any]:
        """generate生态报告"""
        return {
            "overall_health": self.get_overall_health().value,
            "balance_status": self.check_balance(),
            "metrics": {
                name: {
                    "value": metric.value,
                    "target": metric.target,
                    "health": metric.health_status.value,
                    "deviation": metric.deviation
                }
                for name, metric in self.metrics.items()
            },
            "alerts": self.generate_alerts(),
            "timestamp": time.time()
        }

class ResourceOptimizer:
    """
    资源优化器
    
    核心功能:
    - 基于稀缺性的智能分配
    - 优先级调度
    - 资源回收
    - 效率优化
    """
    
    def __init__(self):
        self.resources: Dict[ResourceType, ResourceAllocation] = {}
        self.allocations: Dict[str, Dict[ResourceType, float]] = defaultdict(dict)
        self.priorities: Dict[str, int] = {}  # task_id -> priority (1-10, 10最高)
        
    def register_resource(self, resource_type: ResourceType, total: float, unit: str = "") -> None:
        """注册资源"""
        self.resources[resource_type] = ResourceAllocation(
            resource_type=resource_type,
            allocated=0.0,
            total=total,
            unit=unit
        )
    
    def allocate_resource(self, task_id: str, resource_type: ResourceType, 
                         amount: float, priority: int = 5) -> bool:
        """分配资源"""
        if resource_type not in self.resources:
            return False
        
        resource = self.resources[resource_type]
        
        # 检查是否可用
        if resource.available < amount:
            # 尝试回收低优先级任务的资源
            self._reclaim_resources(resource_type, amount, priority)
            
        if resource.available >= amount:
            resource.allocated += amount
            self.allocations[task_id][resource_type] = amount
            self.priorities[task_id] = priority
            return True
        
        return False
    
    def _reclaim_resources(self, resource_type: ResourceType, 
                          required: float, priority: int) -> None:
        """回收低优先级任务的资源"""
        resource = self.resources[resource_type]
        
        # 按优先级排序任务
        sorted_tasks = sorted(
            self.allocations.items(),
            key=lambda x: self.priorities.get(x[0], 0)
        )
        
        reclaimed = 0.0
        for task_id, allocations in sorted_tasks:
            if reclaimed >= required:
                break
            
            task_priority = self.priorities.get(task_id, 0)
            if task_priority < priority and resource_type in allocations:
                amount = allocations[resource_type]
                resource.allocated -= amount
                reclaimed += amount
                del self.allocations[task_id][resource_type]
    
    def release_resource(self, task_id: str, resource_type: ResourceType) -> None:
        """释放资源"""
        if task_id in self.allocations and resource_type in self.allocations[task_id]:
            amount = self.allocations[task_id][resource_type]
            if resource_type in self.resources:
                self.resources[resource_type].allocated -= amount
            del self.allocations[task_id][resource_type]
    
    def get_optimization_suggestions(self) -> List[str]:
        """get优化建议"""
        suggestions = []
        
        for resource_type, resource in self.resources.items():
            utilization = resource.utilization
            scarcity = resource.scarcity
            
            if utilization > 90:
                suggestions.append(
                    f"{resource_type.value} 利用率过高 ({utilization:.1f}%), "
                    f"建议增加资源或优化使用"
                )
            elif utilization < 30:
                suggestions.append(
                    f"{resource_type.value} 利用率过低 ({utilization:.1f}%), "
                    f"资源可能浪费"
                )
            
            if scarcity > 0.8:
                suggestions.append(
                    f"{resource_type.value} 稀缺度高 ({scarcity:.2f}), "
                    f"建议优先处理关键任务"
                )
        
        return suggestions
    
    def get_utilization_report(self) -> Dict[str, Any]:
        """get利用率报告"""
        return {
            "resources": {
                rtype.value: {
                    "utilization": resource.utilization,
                    "available": resource.available,
                    "total": resource.total,
                    "scarcity": resource.scarcity
                }
                for rtype, resource in self.resources.items()
            },
            "suggestions": self.get_optimization_suggestions(),
            "timestamp": time.time()
        }

class EnvironmentalAdapter:
    """
    环境适配器
    
    核心功能:
    - 监控环境变化
    - 自动调整系统参数
    - 预测环境趋势
    - 适应strategy选择
    """
    
    def __init__(self):
        self.environment_state: Dict[str, Any] = {}
        self.history: Dict[str, List[Any]] = defaultdict(list)
        self.strategies: Dict[str, Callable] = {}
        
    def observe_environment(self) -> Dict[str, Any]:
        """观察环境状态"""
        # 这里应该get实际的系统环境状态
        # 示例: CPU,内存,网络等
        import psutil
        
        return {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "network_sent": psutil.net_io_counters().bytes_sent,
            "network_recv": psutil.net_io_counters().bytes_recv,
            "timestamp": time.time()
        }
    
    def record_environment(self, state: Dict[str, Any]) -> None:
        """记录环境状态"""
        self.environment_state = state
        
        for key, value in state.items():
            if key != "timestamp":
                self.history[key].append(value)
                if len(self.history[key]) > 100:
                    self.history[key] = self.history[key][-100:]
    
    def detect_changes(self, threshold: float = 10.0) -> List[str]:
        """检测环境变化"""
        changes = []
        
        if not self.environment_state:
            return changes
        
        for key, history in self.history.items():
            if len(history) >= 2:
                current = history[-1]
                previous = history[-2]
                change_pct = abs(current - previous) / previous * 100 if previous != 0 else 0
                
                if change_pct > threshold:
                    changes.append(
                        f"{key} 变化 {change_pct:.1f}% "
                        f"({previous:.2f} -> {current:.2f})"
                    )
        
        return changes
    
    def predict_trend(self, key: str, window: int = 10) -> Optional[str]:
        """预测趋势"""
        if key not in self.history or len(self.history[key]) < window:
            return None
        
        values = self.history[key][-window:]
        
        # 计算趋势
        if len(values) >= 2:
            trend = (values[-1] - values[0]) / len(values)
            
            if trend > 0:
                return f"{key} 呈上升趋势 (增长率: {trend:.2f}/单位时间)"
            elif trend < 0:
                return f"{key} 呈下降趋势 (下降率: {abs(trend):.2f}/单位时间)"
            else:
                return f"{key} 保持稳定"
        
        return None
    
    def adapt_strategy(self, key: str, value: float) -> Optional[Any]:
        """选择适应strategy"""
        # 这里应该根据环境状态选择合适的strategy
        # 示例: 如果CPU使用率高, 降低某些任务的优先级
        pass

class EvolutionEngine:
    """
    演化引擎
    
    核心功能:
    - 持续优化系统架构
    - 模式学习和适应
    - 长期趋势分析
    - 演化方向指引
    """
    
    def __init__(self):
        self.generations: List[Dict[str, Any]] = []
        self.current_generation = 0
        self.evolution_metrics: Dict[str, List[float]] = defaultdict(list)
        
    def evolve(self, current_state: Dict[str, Any]) -> Dict[str, Any]:
        """演化到下一代"""
        self.current_generation += 1
        
        generation = {
            "generation": self.current_generation,
            "state": current_state,
            "timestamp": time.time()
        }
        
        self.generations.append(generation)
        
        # 记录演化metrics
        for key, value in current_state.items():
            if isinstance(value, (int, float)):
                self.evolution_metrics[key].append(value)
        
        # 只保留最近100代
        if len(self.generations) > 100:
            self.generations = self.generations[-100:]
        
        return self.suggest_improvements()
    
    def suggest_improvements(self) -> Dict[str, Any]:
        """建议改进"""
        improvements = {}
        
        # 分析演化趋势
        for key, values in self.evolution_metrics.items():
            if len(values) >= 10:
                # 计算改进趋势
                recent = values[-5:]
                earlier = values[-10:-5]
                
                if statistics.mean(recent) > statistics.mean(earlier):
                    improvements[key] = {
                        "trend": "improving",
                        "rate": (statistics.mean(recent) - statistics.mean(earlier)) / statistics.mean(earlier) * 100
                    }
                else:
                    improvements[key] = {
                        "trend": "declining",
                        "rate": (statistics.mean(earlier) - statistics.mean(recent)) / statistics.mean(earlier) * 100
                    }
        
        return improvements
    
    def get_evolution_report(self) -> Dict[str, Any]:
        """get演化报告"""
        return {
            "current_generation": self.current_generation,
            "total_generations": len(self.generations),
            "improvements": self.suggest_improvements(),
            "evolution_history": {
                key: {
                    "latest": values[-1] if values else None,
                    "trend": values[-1] - values[0] if len(values) > 1 else 0
                }
                for key, values in self.evolution_metrics.items()
            },
            "timestamp": time.time()
        }

# 集成接口
class EcosystemIntelligence:
    """
    生态智能系统集成接口
    """
    
    def __init__(self):
        self.ecosystem_manager = EcosystemManager()
        self.resource_optimizer = ResourceOptimizer()
        self.environment_adapter = EnvironmentalAdapter()
        self.evolution_engine = EvolutionEngine()
    
    def initialize(self) -> None:
        """init生态智能系统"""
        # 注册默认metrics
        self.ecosystem_manager.add_metric(EcosystemMetric(
            name="cpu_usage",
            value=50.0,
            target=50.0,
            min_acceptable=30.0,
            max_acceptable=70.0,
            unit="%"
        ))
        
        self.ecosystem_manager.add_metric(EcosystemMetric(
            name="memory_usage",
            value=60.0,
            target=60.0,
            min_acceptable=40.0,
            max_acceptable=80.0,
            unit="%"
        ))
        
        # 注册默认资源
        self.resource_optimizer.register_resource(ResourceType.CPU, 100.0, "%")
        self.resource_optimizer.register_resource(ResourceType.MEMORY, 100.0, "%")
        self.resource_optimizer.register_resource(ResourceType.STORAGE, 1000.0, "GB")
        self.resource_optimizer.register_resource(ResourceType.TOKEN, 1000000, "tokens")
        
    def monitor(self) -> Dict[str, Any]:
        """监控系统状态"""
        # 观察环境
        env_state = self.environment_adapter.observe_environment()
        self.environment_adapter.record_environment(env_state)
        
        # 更新metrics
        self.ecosystem_manager.update_metric("cpu_usage", env_state["cpu_percent"])
        self.ecosystem_manager.update_metric("memory_usage", env_state["memory_percent"])
        
        # generate报告
        return {
            "ecosystem_report": self.ecosystem_manager.generate_report(),
            "resource_report": self.resource_optimizer.get_utilization_report(),
            "environment_changes": self.environment_adapter.detect_changes(),
            "timestamp": time.time()
        }
    
    def evolve(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """演化系统"""
        return self.evolution_engine.evolve(state)
