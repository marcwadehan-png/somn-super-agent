"""
__all__ = [
    'activate_for_task',
    'activate_neuron',
    'activate_subnetwork',
    'build_subnetwork',
    'classify',
    'deactivate_neuron',
    'get_activation_stats',
    'get_activation_status',
    'get_active_neurons',
    'get_phase4_dynamic_activation',
    'get_stats',
    'get_status',
    'get_subnetwork',
    'is_active',
    'process_task',
    'release_subnetwork',
    'TaskProfile',
    'SubNetwork',
    'NeuronActivation',
    'TaskClassifier',
    'SubNetworkBuilder',
    'DynamicActivator',
    'Phase4DynamicActivation',
    'TaskType',
    'ActivationStrategy',
]

Phase 4: 动态网络激活 - 子网络构建与任务识别

实现动态神经网络激活机制：
1. 任务类型识别与分类
2. 动态子网络构建
3. 神经元选择性激活
4. 资源优化与负载均衡
"""

import asyncio
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import defaultdict
import re

class TaskType(Enum):
    """任务类型"""
    ANALYSIS = auto()       # 分析型任务
    CREATION = auto()       # 创造型任务
    REASONING = auto()      # 推理型任务
    MEMORY = auto()         # 记忆型任务
    WISDOM = auto()         # 智慧型任务
    EXECUTION = auto()      # 执行型任务
    LEARNING = auto()       # 学习型任务
    COORDINATION = auto()   # 协调型任务
    UNKNOWN = auto()        # 未知类型

class ActivationStrategy(Enum):
    """激活策略"""
    GREEDY = auto()         # 贪婪策略 - 激活所有相关神经元
    SELECTIVE = auto()      # 选择性策略 - 只激活最相关的
    CASCADE = auto()        # 级联策略 - 逐层激活
    ADAPTIVE = auto()       # 自适应策略 - 基于历史动态调整

@dataclass
class TaskProfile:
    """任务画像"""
    task_id: str
    task_type: TaskType
    keywords: List[str]
    complexity: float  # 0.0 - 1.0
    required_modules: List[str]
    estimated_duration_ms: float
    priority: int = 5  # 1-10
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SubNetwork:
    """子网络定义"""
    network_id: str
    task_type: TaskType
    neurons: List[str]  # 神经元ID列表
    connections: List[Tuple[str, str]]  # (source, target) 连接列表
    activation_threshold: float
    created_at: float = field(default_factory=time.time)
    activation_count: int = 0
    avg_processing_time: float = 0.0

@dataclass
class NeuronActivation:
    """神经元激活状态"""
    neuron_id: str
    activation_level: float  # 0.0 - 1.0
    activated_at: float
    task_id: Optional[str] = None
    
    def is_active(self, timeout_ms: float = 5000) -> bool:
        """检查是否仍处于激活状态
        
        Args:
            timeout_ms: 超时时间（毫秒）
            
        Returns:
            bool: 是否仍在激活状态
        """
        elapsed = (time.time() - self.activated_at) * 1000
        return elapsed < timeout_ms

class TaskClassifier:
    """任务分类器 - 识别任务类型"""
    
    # 关键词映射到任务类型
    KEYWORD_PATTERNS = {
        TaskType.ANALYSIS: [
            r"分析|剖析|解析|研究|调查|评估|诊断|审查|检查|比较|对比|趋势|模式|洞察",
            r"analyze|analysis|research|evaluate|assess|diagnose|compare|trend|pattern"
        ],
        TaskType.CREATION: [
            r"创建|生成|设计|构建|制作|编写|撰写|创作|开发|实现|搭建",
            r"create|generate|design|build|make|write|develop|implement|construct"
        ],
        TaskType.REASONING: [
            r"推理|推导|逻辑|思考|为什么|原因|因果|论证|证明|推断",
            r"reason|infer|logic|think|why|cause|proof|deduce|conclude"
        ],
        TaskType.MEMORY: [
            r"记忆|回忆|记住|存储|检索|查询|历史|过去|之前|曾经",
            r"memory|remember|recall|store|retrieve|history|past|before"
        ],
        TaskType.WISDOM: [
            r"智慧|建议|策略|方案|决策|选择|指导|建议|哲学|道理",
            r"wisdom|advice|strategy|decision|choice|guide|philosophy"
        ],
        TaskType.EXECUTION: [
            r"执行|运行|启动|调用|操作|处理|完成|实施|应用|部署",
            r"execute|run|start|call|operate|process|complete|implement|deploy"
        ],
        TaskType.LEARNING: [
            r"学习|训练|优化|改进|适应|进化|调整|更新|迭代|提升",
            r"learn|train|optimize|improve|adapt|evolve|adjust|update|iterate"
        ],
        TaskType.COORDINATION: [
            r"协调|调度|编排|管理|组织|整合|同步|协作|配合",
            r"coordinate|schedule|orchestrate|manage|organize|integrate|sync"
        ]
    }
    
    # 模块需求映射
    MODULE_REQUIREMENTS = {
        TaskType.ANALYSIS: ["deep_reasoning", "data_analysis", "pattern_recognition"],
        TaskType.CREATION: ["generative_engine", "knowledge_base", "creative_module"],
        TaskType.REASONING: ["logic_engine", "inference_system", "rule_engine"],
        TaskType.MEMORY: ["memory_system", "retrieval_engine", "storage"],
        TaskType.WISDOM: ["wisdom_dispatcher", "school_engines", "philosophy_core"],
        TaskType.EXECUTION: ["execution_engine", "workflow_manager", "action_dispatcher"],
        TaskType.LEARNING: ["learning_engine", "adaptation_system", "feedback_loop"],
        TaskType.COORDINATION: ["orchestrator", "scheduler", "coordination_core"]
    }
    
    def __init__(self):
        self.classification_history: List[Dict] = []
    
    def classify(self, query: str, context: Optional[Dict] = None) -> TaskProfile:
        """分类任务"""
        query_lower = query.lower()
        
        # 计算各类型匹配分数
        scores = {}
        for task_type, patterns in self.KEYWORD_PATTERNS.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, query_lower))
                score += matches
            scores[task_type] = score
        
        # 确定主要类型
        if max(scores.values()) > 0:
            task_type = max(scores, key=scores.get)
        else:
            task_type = TaskType.UNKNOWN
        
        # 提取关键词
        keywords = self._extract_keywords(query)
        
        # 计算复杂度
        complexity = self._calculate_complexity(query, scores)
        
        # 确定所需模块
        required_modules = self.MODULE_REQUIREMENTS.get(task_type, ["core"])
        
        # 估计处理时间
        estimated_duration = self._estimate_duration(query, complexity)
        
        profile = TaskProfile(
            task_id=f"task_{int(time.time() * 1000)}",
            task_type=task_type,
            keywords=keywords,
            complexity=complexity,
            required_modules=required_modules,
            estimated_duration_ms=estimated_duration,
            context=context or {}
        )
        
        self.classification_history.append({
            "query": query[:100],
            "classified_type": task_type.name,
            "confidence": max(scores.values()) / (sum(scores.values()) or 1),
            "timestamp": time.time()
        })
        
        return profile
    
    def _extract_keywords(self, query: str) -> List[str]:
        """提取关键词"""
        # 简单的关键词提取
        words = re.findall(r'\b\w{2,}\b', query.lower())
        # 过滤常见停用词
        stopwords = {"the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        keywords = [w for w in words if w not in stopwords][:10]
        return keywords
    
    def _calculate_complexity(self, query: str, scores: Dict[TaskType, int]) -> float:
        """计算任务复杂度"""
        # 基于查询长度、类型混合度计算
        length_factor = min(len(query) / 500, 1.0)  # 长度因素
        
        # 类型混合度（多种类型关键词出现）
        active_types = sum(1 for s in scores.values() if s > 0)
        type_mix_factor = min(active_types / 3, 1.0)
        
        # 复杂度 = 长度因素 * 0.4 + 类型混合 * 0.6
        complexity = length_factor * 0.4 + type_mix_factor * 0.6
        return min(complexity, 1.0)
    
    def _estimate_duration(self, query: str, complexity: float) -> float:
        """估计处理时间"""
        # 基础时间 + 复杂度加成
        base_time = 100  # 100ms基础
        complexity_bonus = complexity * 900  # 最多900ms加成
        return base_time + complexity_bonus

class SubNetworkBuilder:
    """子网络构建器"""
    
    def __init__(self, network_layout_manager=None):
        self.layout_manager = network_layout_manager
        self.subnetworks: Dict[str, SubNetwork] = {}
        self.neuron_pool: Dict[str, Dict] = {}  # 可用神经元池
        self._build_templates()
    
    def _build_templates(self) -> None:
        """构建子网络模板"""
        self.templates = {
            TaskType.ANALYSIS: {
                "neurons": ["input", "perception", "analysis", "inference", "output"],
                "connections": [("input", "perception"), ("perception", "analysis"), 
                               ("analysis", "inference"), ("inference", "output")],
                "threshold": 0.6
            },
            TaskType.CREATION: {
                "neurons": ["input", "knowledge", "generative", "evaluation", "output"],
                "connections": [("input", "knowledge"), ("knowledge", "generative"),
                               ("generative", "evaluation"), ("evaluation", "output")],
                "threshold": 0.5
            },
            TaskType.REASONING: {
                "neurons": ["input", "logic", "inference", "validation", "output"],
                "connections": [("input", "logic"), ("logic", "inference"),
                               ("inference", "validation"), ("validation", "output")],
                "threshold": 0.7
            },
            TaskType.MEMORY: {
                "neurons": ["input", "encoding", "storage", "retrieval", "output"],
                "connections": [("input", "encoding"), ("encoding", "storage"),
                               ("storage", "retrieval"), ("retrieval", "output")],
                "threshold": 0.4
            },
            TaskType.WISDOM: {
                "neurons": ["input", "context", "wisdom_dispatcher", "fusion", "output"],
                "connections": [("input", "context"), ("context", "wisdom_dispatcher"),
                               ("wisdom_dispatcher", "fusion"), ("fusion", "output")],
                "threshold": 0.5
            },
            TaskType.EXECUTION: {
                "neurons": ["input", "planning", "execution", "monitoring", "output"],
                "connections": [("input", "planning"), ("planning", "execution"),
                               ("execution", "monitoring"), ("monitoring", "output")],
                "threshold": 0.6
            },
            TaskType.LEARNING: {
                "neurons": ["input", "feedback", "adaptation", "update", "output"],
                "connections": [("input", "feedback"), ("feedback", "adaptation"),
                               ("adaptation", "update"), ("update", "output")],
                "threshold": 0.5
            },
            TaskType.COORDINATION: {
                "neurons": ["input", "scheduler", "coordinator", "synchronizer", "output"],
                "connections": [("input", "scheduler"), ("scheduler", "coordinator"),
                               ("coordinator", "synchronizer"), ("synchronizer", "output")],
                "threshold": 0.6
            }
        }
    
    def build_subnetwork(self, task_profile: TaskProfile) -> SubNetwork:
        """为任务构建子网络"""
        template = self.templates.get(task_profile.task_type, self.templates[TaskType.ANALYSIS])
        
        # 根据复杂度调整神经元数量
        neurons = self._select_neurons(template["neurons"], task_profile.complexity)
        
        # 构建连接
        connections = self._build_connections(neurons, template["connections"])
        
        subnetwork = SubNetwork(
            network_id=f"subnet_{task_profile.task_id}",
            task_type=task_profile.task_type,
            neurons=neurons,
            connections=connections,
            activation_threshold=template["threshold"]
        )
        
        self.subnetworks[subnetwork.network_id] = subnetwork
        
        return subnetwork
    
    def _select_neurons(self, base_neurons: List[str], complexity: float) -> List[str]:
        """根据复杂度选择神经元"""
        # 复杂度越高，激活的神经元越多
        num_neurons = max(3, int(len(base_neurons) * (0.5 + complexity * 0.5)))
        return base_neurons[:num_neurons]
    
    def _build_connections(
        self,
        neurons: List[str],
        template_connections: List[Tuple[str, str]]
    ) -> List[Tuple[str, str]]:
        """构建神经元连接"""
        neuron_set = set(neurons)
        connections = []
        
        for source, target in template_connections:
            if source in neuron_set and target in neuron_set:
                connections.append((source, target))
        
        return connections
    
    def get_subnetwork(self, network_id: str) -> Optional[SubNetwork]:
        """获取子网络"""
        return self.subnetworks.get(network_id)
    
    def get_stats(self) -> Dict:
        """获取构建统计"""
        return {
            "total_subnetworks": len(self.subnetworks),
            "by_task_type": {
                task_type.name: sum(1 for s in self.subnetworks.values() if s.task_type == task_type)
                for task_type in TaskType
            }
        }

class DynamicActivator:
    """动态激活器"""
    
    def __init__(self):
        self.activations: Dict[str, NeuronActivation] = {}
        self.activation_history: List[Dict] = []
        self.max_concurrent = 10  # 最大并发激活数
        self.current_active = 0
        self._lock = asyncio.Lock()
    
    async def activate_neuron(
        self,
        neuron_id: str,
        activation_level: float = 1.0,
        task_id: Optional[str] = None
    ) -> bool:  # 返回是否成功激活
        """激活神经元"""
        async with self._lock:
            if self.current_active >= self.max_concurrent:
                return False
            
            activation = NeuronActivation(
                neuron_id=neuron_id,
                activation_level=activation_level,
                activated_at=time.time(),
                task_id=task_id
            )
            
            self.activations[neuron_id] = activation
            self.current_active += 1
            
            self.activation_history.append({
                "neuron_id": neuron_id,
                "activation_level": activation_level,
                "task_id": task_id,
                "timestamp": time.time()
            })
            
            return True
    
    async def deactivate_neuron(self, neuron_id: str) -> None:
        """停用神经元"""
        async with self._lock:
            if neuron_id in self.activations:
                del self.activations[neuron_id]
                self.current_active = max(0, self.current_active - 1)
    
    async def activate_subnetwork(
        self,
        subnetwork: SubNetwork,
        strategy: ActivationStrategy = ActivationStrategy.ADAPTIVE
    ) -> Dict[str, bool]:
        """激活子网络"""
        results = {}
        
        if strategy == ActivationStrategy.GREEDY:
            # 贪婪策略 - 激活所有
            for neuron_id in subnetwork.neurons:
                success = await self.activate_neuron(neuron_id, 1.0, subnetwork.network_id)
                results[neuron_id] = success
        
        elif strategy == ActivationStrategy.SELECTIVE:
            # 选择性策略 - 只激活关键神经元
            key_neurons = subnetwork.neurons[:3]  # 前3个是关键
            for neuron_id in key_neurons:
                success = await self.activate_neuron(neuron_id, 1.0, subnetwork.network_id)
                results[neuron_id] = success
        
        elif strategy == ActivationStrategy.CASCADE:
            # 级联策略 - 逐层激活
            for i, neuron_id in enumerate(subnetwork.neurons):
                level = 1.0 - (i * 0.1)  # 逐层递减
                success = await self.activate_neuron(neuron_id, level, subnetwork.network_id)
                results[neuron_id] = success
                await asyncio.sleep(0.01)  # 级联延迟
        
        else:  # ADAPTIVE
            # 自适应策略
            for neuron_id in subnetwork.neurons:
                # 基于历史调整激活级别
                level = self._calculate_adaptive_level(neuron_id, subnetwork)
                success = await self.activate_neuron(neuron_id, level, subnetwork.network_id)
                results[neuron_id] = success
        
        subnetwork.activation_count += 1
        return results
    
    def _calculate_adaptive_level(self, neuron_id: str, subnetwork: SubNetwork) -> float:
        """计算自适应激活级别"""
        # 基于子网络的历史表现调整
        if subnetwork.activation_count == 0:
            return 1.0
        
        # 处理时间越短，激活级别越高
        if subnetwork.avg_processing_time > 0:
            base_level = min(1.0, 1000 / subnetwork.avg_processing_time)
        else:
            base_level = 1.0
        
        return base_level
    
    def get_active_neurons(self) -> List[str]:
        """获取当前激活的神经元"""
        return [
            nid for nid, act in self.activations.items()
            if act.is_active()
        ]
    
    def get_activation_stats(self) -> Dict[str, Any]:
        """获取激活统计"""
        return {
            "current_active": self.current_active,
            "max_concurrent": self.max_concurrent,
            "total_activations": len(self.activation_history),
            "active_neurons": self.get_active_neurons()
        }

class Phase4DynamicActivation:
    """
    Phase 4: 动态网络激活主类
    
    整合任务分类、子网络构建和动态激活
    """
    
    def __init__(self) -> None:
        self.classifier = TaskClassifier()
        self.builder = SubNetworkBuilder()
        self.activator = DynamicActivator()
        
        self.active_subnetworks: Dict[str, SubNetwork] = {}
        self.processing_tasks: Dict[str, asyncio.Task] = {}
    
    async def process_task(
        self,
        query: str,
        context: Optional[Dict] = None,
        strategy: ActivationStrategy = ActivationStrategy.ADAPTIVE
    ) -> Dict[str, Any]:
        """处理任务"""
        start_time = time.time()
        
        # 1. 任务分类
        task_profile = self.classifier.classify(query, context)
        
        # 2. 构建子网络
        subnetwork = self.builder.build_subnetwork(task_profile)
        self.active_subnetworks[subnetwork.network_id] = subnetwork
        
        # 3. 动态激活
        activation_results = await self.activator.activate_subnetwork(subnetwork, strategy)
        
        # 4. 模拟处理
        await self._simulate_processing(subnetwork)
        
        # 5. 更新统计
        duration = (time.time() - start_time) * 1000
        subnetwork.avg_processing_time = (
            (subnetwork.avg_processing_time * (subnetwork.activation_count - 1) + duration)
            / subnetwork.activation_count
        )
        
        return {
            "task_id": task_profile.task_id,
            "task_type": task_profile.task_type.name,
            "subnetwork_id": subnetwork.network_id,
            "neurons_activated": sum(1 for v in activation_results.values() if v),
            "activation_results": activation_results,
            "processing_time_ms": duration,
            "complexity": task_profile.complexity
        }
    
    async def _simulate_processing(self, subnetwork: SubNetwork) -> None:
        """模拟处理过程"""
        # 模拟子网络处理时间
        processing_time = 0.05 + (len(subnetwork.neurons) * 0.02)
        await asyncio.sleep(processing_time)
    
    async def release_subnetwork(self, network_id: str) -> None:
        """释放子网络"""
        if network_id in self.active_subnetworks:
            subnetwork = self.active_subnetworks[network_id]
            
            # 停用所有神经元
            for neuron_id in subnetwork.neurons:
                await self.activator.deactivate_neuron(neuron_id)
            
            del self.active_subnetworks[network_id]
    
    def get_status(self) -> Dict[str, Any]:
        """获取状态"""
        return {
            "classifier": {
                "total_classifications": len(self.classifier.classification_history)
            },
            "builder": self.builder.get_stats(),
            "activator": self.activator.get_activation_stats(),
            "active_subnetworks": len(self.active_subnetworks)
        }

# 全局实例
_phase4_instance: Optional[Phase4DynamicActivation] = None

def get_phase4_dynamic_activation() -> Phase4DynamicActivation:
    """获取Phase 4动态激活实例"""
    global _phase4_instance
    if _phase4_instance is None:
        _phase4_instance = Phase4DynamicActivation()
    return _phase4_instance

# 便捷函数
async def activate_for_task(query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """为任务激活网络"""
    phase4 = get_phase4_dynamic_activation()
    return await phase4.process_task(query, context)

def get_activation_status() -> Dict[str, Any]:
    """获取激活状态"""
    return get_phase4_dynamic_activation().get_status()
