"""
__all__ = [
    'add_link',
    'add_module',
    'analyze_axis',
    'broadcast',
    'execute_main_chain_cross',
    'get_all_axes_status',
    'get_all_links',
    'get_all_nodes',
    'get_all_paths',
    'get_cross_network',
    'get_cross_weaver',
    'get_downstream',
    'get_evolution_log',
    'get_link',
    'get_signals',
    'get_upstream',
    'propagate',
    'register_module',
    'send_signal',
    'to_dict',
    'update_link_strength',
    'weave',
]

主线交叉织网器 v1.0
Main Chain Cross Weaver

功能：
1. 网状交叉影响 - 实现多模块之间的相互反馈
2. 元推理增强 - 将多个模块的输出交叉融合
3. 反馈闭环 - 将输出反馈到其他模块形成闭环
4. 进化驱动 - 基于反馈驱动系统进化

运行模式：
- 交叉运转（Cross）：网状交叉影响多模块
- 支持正向反馈和负向反馈
- 支持跨层反馈和跨域反馈

适用场景：
- 元推理、反思优化、策略迭代等需要多模块相互反馈的任务
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional, Set, Callable, Tuple
from collections import defaultdict
import threading
import time
import uuid

from src.intelligence.engines._common_enums import FeedbackType

logger = logging.getLogger(__name__)

class CrossAxis(Enum):
    """交叉轴"""
    WISDOM_REASONING = "wisdom_reasoning"     # 智慧-推理轴
    MEMORY_LEARNING = "memory_learning"        # 记忆-学习轴
    SCHEDULING_VALUE = "scheduling_value"      # 调度-价值轴
    AUTONOMOUS_REFLECTION = "autonomous_reflection"  # 自主-反思轴
    NEURAL_META = "neural_meta"              # 神经-元认知轴

@dataclass
class CrossLink:
    """交叉链接"""
    link_id: str
    source_module: str
    target_module: str
    feedback_type: FeedbackType
    weight: float = 1.0                        # 权重
    strength: float = 0.5                     # 强度（0-1）
    last_triggered: Optional[str] = None
    trigger_count: int = 0

    def to_dict(self) -> Dict:
        return {
            "link_id": self.link_id,
            "source": self.source_module,
            "target": self.target_module,
            "type": self.feedback_type.value,
            "weight": self.weight,
            "strength": self.strength,
            "triggered": self.trigger_count
        }

@dataclass
class CrossSignal:
    """交叉信号"""
    signal_id: str
    source_module: str
    target_module: str
    content: Any
    feedback_type: FeedbackType
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "signal_id": self.signal_id,
            "source": self.source_module,
            "target": self.target_module,
            "content": str(self.content)[:100],
            "type": self.feedback_type.value,
            "timestamp": self.timestamp
        }

@dataclass
class CrossResult:
    """交叉结果"""
    result_id: str
    initial_output: Any
    final_output: Any
    signals: List[CrossSignal]
    iterations: int
    convergence: bool
    insights: List[str]
    evolved_modules: List[str]
    total_time: float

class CrossGraph:
    """
    交叉影响图

    表示模块之间的网状交叉关系
    """

    def __init__(self):
        self._nodes: Set[str] = set()
        self._links: Dict[str, CrossLink] = {}
        self._adjacency: Dict[str, List[str]] = defaultdict(list)
        self._reverse_adjacency: Dict[str, List[str]] = defaultdict(list)
        self._lock = threading.RLock()

    def add_module(self, module: str):
        """添加模块节点"""
        with self._lock:
            self._nodes.add(module)

    def add_link(self, source: str, target: str,
                 feedback_type: FeedbackType = FeedbackType.NEUTRAL,
                 weight: float = 1.0) -> str:
        """添加交叉链接"""
        with self._lock:
            self.add_module(source)
            self.add_module(target)

            link_id = f"{source}->{target}"
            link = CrossLink(
                link_id=link_id,
                source_module=source,
                target_module=target,
                feedback_type=feedback_type,
                weight=weight
            )

            self._links[link_id] = link
            self._adjacency[source].append(target)
            self._reverse_adjacency[target].append(source)

            return link_id

    def get_downstream(self, module: str) -> List[str]:
        """获取下游模块"""
        with self._lock:
            return list(self._adjacency.get(module, []))

    def get_upstream(self, module: str) -> List[str]:
        """获取上游模块"""
        with self._lock:
            return list(self._reverse_adjacency.get(module, []))

    def get_all_paths(self, source: str, target: str) -> List[List[str]]:
        """获取所有路径（简单BFS实现）"""
        with self._lock:
            paths = []
            queue = [(source, [source])]

            while queue:
                current, path = queue.pop(0)
                if current == target:
                    paths.append(path)
                    continue

                for next_node in self._adjacency.get(current, []):
                    if next_node not in path:
                        queue.append((next_node, path + [next_node]))

            return paths

    def update_link_strength(self, link_id: str, delta: float):
        """更新链接强度"""
        with self._lock:
            if link_id in self._links:
                link = self._links[link_id]
                link.strength = max(0.0, min(1.0, link.strength + delta))
                link.trigger_count += 1
                link.last_triggered = datetime.now().isoformat()

    def get_link(self, source: str, target: str) -> Optional[CrossLink]:
        """获取链接"""
        return self._links.get(f"{source}->{target}")

    def get_all_links(self) -> List[CrossLink]:
        """获取所有链接"""
        with self._lock:
            return list(self._links.values())

    def get_all_nodes(self) -> List[str]:
        """获取所有节点"""
        with self._lock:
            return list(self._nodes)

class CrossWeaver:
    """
    主线交叉织网器

    功能：
    1. 构建模块间网状交叉关系
    2. 实现跨模块信号传递
    3. 基于反馈驱动系统进化
    4. 提供元推理能力

    主线定位：
    - 串联运转：WisdomDispatcher -> GlobalScheduler -> ThinkingEngine
    - 并形运转：ParallelRouter 多路并发
    - 交叉运转：CrossWeaver 网状交叉影响
    """

    def __init__(self):
        self.cross_graph = CrossGraph()
        self._modules: Dict[str, Any] = {}
        self._handlers: Dict[str, Callable] = {}
        self._signal_history: List[CrossSignal] = []
        self._evolution_log: List[Dict] = []
        self._lock = threading.RLock()

        # 初始化主线交叉网络
        self._init_main_chain_network()

        logger.info("CrossWeaver 初始化完成")

    def _init_main_chain_network(self):
        """初始化主线交叉网络"""
        # 定义主线节点
        main_nodes = [
            "wisdom_dispatcher",
            "deep_reasoning",
            "narrative_engine",
            "neural_scheduler",
            "learning_coordinator",
            "autonomous_agent",
            "neural_memory",
            "semantic_memory",
            "reinforcement_trigger",
            "roi_tracker",
            "reflection_engine",
            "goal_system"
        ]

        # 添加所有节点
        for node in main_nodes:
            self.cross_graph.add_module(node)

        # 定义交叉链接（反馈关系）
        cross_links = [
            # WisdomDispatcher -> 各模块（智慧输出）
            ("wisdom_dispatcher", "deep_reasoning", FeedbackType.POSITIVE, 0.8),
            ("wisdom_dispatcher", "narrative_engine", FeedbackType.POSITIVE, 0.7),
            ("wisdom_dispatcher", "learning_coordinator", FeedbackType.POSITIVE, 0.9),

            # DeepReasoning -> 各模块（推理反馈）
            ("deep_reasoning", "wisdom_dispatcher", FeedbackType.ADAPTIVE, 0.6),
            ("deep_reasoning", "autonomous_agent", FeedbackType.POSITIVE, 0.7),
            ("deep_reasoning", "reflection_engine", FeedbackType.POSITIVE, 0.8),

            # NeuralScheduler -> 各模块（调度反馈）
            ("neural_scheduler", "learning_coordinator", FeedbackType.ADAPTIVE, 0.5),
            ("neural_scheduler", "autonomous_agent", FeedbackType.ADAPTIVE, 0.6),

            # LearningCoordinator -> 各模块（学习反馈）
            ("learning_coordinator", "semantic_memory", FeedbackType.POSITIVE, 0.9),
            ("learning_coordinator", "neural_memory", FeedbackType.POSITIVE, 0.8),
            ("learning_coordinator", "wisdom_dispatcher", FeedbackType.ADAPTIVE, 0.5),

            # AutonomousAgent -> 各模块（自主反馈）
            ("autonomous_agent", "reflection_engine", FeedbackType.POSITIVE, 0.7),
            ("autonomous_agent", "goal_system", FeedbackType.POSITIVE, 0.8),
            ("autonomous_agent", "roi_tracker", FeedbackType.ADAPTIVE, 0.6),

            # Memory -> 各模块（记忆反馈）
            ("neural_memory", "wisdom_dispatcher", FeedbackType.ADAPTIVE, 0.7),
            ("semantic_memory", "deep_reasoning", FeedbackType.POSITIVE, 0.8),

            # Reinforcement -> 各模块（强化反馈）
            ("reinforcement_trigger", "learning_coordinator", FeedbackType.POSITIVE, 0.9),
            ("reinforcement_trigger", "autonomous_agent", FeedbackType.ADAPTIVE, 0.7),

            # ROITracker -> 各模块（价值反馈）
            ("roi_tracker", "autonomous_agent", FeedbackType.ADAPTIVE, 0.8),
            ("roi_tracker", "reflection_engine", FeedbackType.POSITIVE, 0.6),

            # ReflectionEngine -> 各模块（反思反馈）
            ("reflection_engine", "autonomous_agent", FeedbackType.POSITIVE, 0.8),
            ("reflection_engine", "goal_system", FeedbackType.ADAPTIVE, 0.7),
            ("reflection_engine", "wisdom_dispatcher", FeedbackType.ADAPTIVE, 0.5),

            # GoalSystem -> 各模块（目标反馈）
            ("goal_system", "autonomous_agent", FeedbackType.POSITIVE, 0.9),
            ("goal_system", "learning_coordinator", FeedbackType.ADAPTIVE, 0.6),
        ]

        # 添加所有链接
        for source, target, fb_type, weight in cross_links:
            self.cross_graph.add_link(source, target, fb_type, weight)

    def register_module(self, module_key: str, handler: Callable):
        """注册模块处理器"""
        with self._lock:
            self._modules[module_key] = handler
            self._handlers[module_key] = handler
            self.cross_graph.add_module(module_key)
            logger.debug(f"模块已注册: {module_key}")

    def weave(self, initial_output: Any,
              context: Dict[str, Any],
              max_iterations: int = 3) -> CrossResult:
        """
        交叉织网主方法

        将初始输出通过网状交叉影响得到进化后的输出

        Args:
            initial_output: 初始输出
            context: 上下文
            max_iterations: 最大迭代次数

        Returns:
            CrossResult: 交叉结果
        """
        start_time = time.time()
        result_id = f"cross_{uuid.uuid4().hex[:8]}"

        current_output = initial_output
        signals = []
        iterations = 0
        evolved_modules = set()

        logger.info(f"交叉织网开始: {result_id}, 最大迭代: {max_iterations}")

        for iteration in range(max_iterations):
            iterations += 1
            logger.debug(f"交叉织网迭代 {iteration + 1}/{max_iterations}")

            # 执行单次交叉
            iter_output, iter_signals, iter_evolved = self._single_cross_iteration(
                current_output, context, iteration
            )

            # 收集信号
            signals.extend(iter_signals)
            evolved_modules.update(iter_evolved)

            # 检查收敛
            if self._check_convergence(current_output, iter_output):
                logger.info(f"交叉织网收敛于迭代 {iteration + 1}")
                current_output = iter_output
                break

            current_output = iter_output

        total_time = time.time() - start_time

        # 记录进化
        self._log_evolution(result_id, initial_output, current_output, iterations, evolved_modules)

        result = CrossResult(
            result_id=result_id,
            initial_output=initial_output,
            final_output=current_output,
            signals=signals,
            iterations=iterations,
            convergence=iterations < max_iterations,
            insights=self._extract_cross_insights(signals, evolved_modules),
            evolved_modules=list(evolved_modules),
            total_time=total_time
        )

        logger.info(f"交叉织网完成: {result_id}, 迭代 {iterations}, 耗时 {total_time:.2f}s")

        return result

    def _single_cross_iteration(self, output: Any,
                                 context: Dict,
                                 iteration: int) -> Tuple[Any, List[CrossSignal], Set[str]]:
        """
        单次交叉迭代

        遍历所有交叉链接，将输出反馈到目标模块
        """
        signals = []
        evolved_modules = set()

        # 获取所有链接
        links = self.cross_graph.get_all_links()

        # 按反馈类型分组处理
        positive_signals = [l for l in links if l.feedback_type == FeedbackType.POSITIVE]
        adaptive_signals = [l for l in links if l.feedback_type == FeedbackType.ADAPTIVE]

        # 处理正向反馈（增强）
        for link in positive_signals:
            signal = self._process_link(link, output, context, iteration)
            if signal:
                signals.append(signal)
                evolved_modules.add(link.target_module)
                # 更新链接强度
                self.cross_graph.update_link_strength(link.link_id, 0.05)

        # 处理自适应反馈（调节）
        for link in adaptive_signals:
            signal = self._process_link(link, output, context, iteration)
            if signal:
                signals.append(signal)
                evolved_modules.add(link.target_module)
                # 更新链接强度
                self.cross_graph.update_link_strength(link.link_id, 0.03)

        # 处理所有信号
        processed_output = self._apply_signals(output, signals)

        return processed_output, signals, evolved_modules

    def _process_link(self, link: CrossLink, output: Any,
                     context: Dict, iteration: int) -> Optional[CrossSignal]:
        """处理单个交叉链接"""
        # 生成信号内容
        signal_content = {
            "iteration": iteration,
            "weight": link.weight,
            "strength": link.strength,
            "source_output": str(output)[:50] if output else None,
            "context_hints": context.get("hints", [])
        }

        signal = CrossSignal(
            signal_id=f"sig_{uuid.uuid4().hex[:8]}",
            source_module=link.source_module,
            target_module=link.target_module,
            content=signal_content,
            feedback_type=link.feedback_type,
            metadata={"link_id": link.link_id, "iteration": iteration}
        )

        # 记录信号历史
        with self._lock:
            self._signal_history.append(signal)

        return signal

    def _apply_signals(self, output: Any,
                      signals: List[CrossSignal]) -> Any:
        """应用信号到输出"""
        if not signals:
            return output

        # 按目标模块分组
        target_signals = defaultdict(list)
        for signal in signals:
            target_signals[signal.target_module].append(signal)

        # 融合信号到输出
        if isinstance(output, dict):
            fused_output = output.copy()
            for target, sigs in target_signals.items():
                fused_output[f"cross_{target}"] = [
                    {"type": s.feedback_type.value, "content": s.content}
                    for s in sigs
                ]
            return fused_output
        else:
            # 非字典输出，包装为信号容器
            return {
                "original": output,
                "cross_signals": [s.to_dict() for s in signals]
            }

    def _check_convergence(self, old_output: Any, new_output: Any) -> bool:
        """检查是否收敛"""
        if not isinstance(old_output, dict) or not isinstance(new_output, dict):
            return False

        # 简单收敛检查：关键字段不再变化
        old_keys = set(k for k in old_output.keys() if k.startswith("cross_"))
        new_keys = set(k for k in new_output.keys() if k.startswith("cross_"))

        return old_keys == new_keys

    def _extract_cross_insights(self, signals: List[CrossSignal],
                                evolved_modules: Set[str]) -> List[str]:
        """提取交叉洞察"""
        insights = []

        # 统计反馈分布
        feedback_dist = defaultdict(int)
        for signal in signals:
            feedback_dist[signal.feedback_type.value] += 1

        insights.append(f"交叉反馈完成: {len(signals)} 个信号")
        insights.append(f"涉及 {len(evolved_modules)} 个模块进化")

        if feedback_dist.get("positive"):
            insights.append(f"正向反馈: {feedback_dist['positive']} 次")
        if feedback_dist.get("adaptive"):
            insights.append(f"自适应反馈: {feedback_dist['adaptive']} 次")

        return insights

    def _log_evolution(self, result_id: str, initial: Any, final: Any,
                      iterations: int, evolved: Set[str]):
        """记录进化日志"""
        with self._lock:
            self._evolution_log.append({
                "result_id": result_id,
                "initial_type": type(initial).__name__,
                "final_type": type(final).__name__,
                "iterations": iterations,
                "evolved_modules": list(evolved),
                "timestamp": datetime.now().isoformat()
            })

    # ── 信号发送接口 ─────────────────────────────────────────

    def send_signal(self, source: str, target: str,
                   content: Any,
                   feedback_type: FeedbackType = FeedbackType.NEUTRAL) -> str:
        """
        发送交叉信号

        Args:
            source: 源模块
            target: 目标模块
            content: 信号内容
            feedback_type: 反馈类型

        Returns:
            str: 信号ID
        """
        signal_id = f"sig_{uuid.uuid4().hex[:8]}"

        signal = CrossSignal(
            signal_id=signal_id,
            source_module=source,
            target_module=target,
            content=content,
            feedback_type=feedback_type
        )

        with self._lock:
            self._signal_history.append(signal)

        # 如果链接不存在，动态创建
        link = self.cross_graph.get_link(source, target)
        if not link:
            self.cross_graph.add_link(source, target, feedback_type)
        else:
            self.cross_graph.update_link_strength(link.link_id, 0.1)

        logger.debug(f"信号发送: {source} -> {target}, 类型: {feedback_type.value}")

        return signal_id

    def broadcast(self, source: str, content: Any,
                 feedback_type: FeedbackType = FeedbackType.NEUTRAL) -> List[str]:
        """
        广播信号到所有下游模块

        Args:
            source: 源模块
            content: 信号内容
            feedback_type: 反馈类型

        Returns:
            List[str]: 信号ID列表
        """
        downstream = self.cross_graph.get_downstream(source)
        signal_ids = []

        for target in downstream:
            sig_id = self.send_signal(source, target, content, feedback_type)
            signal_ids.append(sig_id)

        logger.info(f"广播完成: {source} -> {len(signal_ids)} 个模块")

        return signal_ids

    def propagate(self, source: str, content: Any,
                 feedback_type: FeedbackType = FeedbackType.NEUTRAL,
                 max_hops: int = 3) -> List[str]:
        """
        传播信号（多跳）

        Args:
            source: 源模块
            content: 信号内容
            feedback_type: 反馈类型
            max_hops: 最大跳数

        Returns:
            List[str]: 信号ID列表
        """
        signal_ids = []
        visited = {source}

        current_layer = [source]

        for hop in range(max_hops):
            next_layer = []

            for current in current_layer:
                downstream = self.cross_graph.get_downstream(current)
                for target in downstream:
                    if target not in visited:
                        sig_id = self.send_signal(current, target, content, feedback_type)
                        signal_ids.append(sig_id)
                        next_layer.append(target)
                        visited.add(target)

            current_layer = next_layer

            if not current_layer:
                break

        logger.info(f"信号传播完成: {source} -> {len(signal_ids)} 个信号 ({hop + 1} 跳)")

        return signal_ids

    # ── 便捷方法 ─────────────────────────────────────────────

    def execute_main_chain_cross(self, initial_output: Any,
                                 context: Dict[str, Any]) -> CrossResult:
        """
        执行主线交叉运转

        将主线输出通过交叉网络进行网状影响

        Args:
            initial_output: 初始输出
            context: 上下文

        Returns:
            CrossResult: 交叉结果
        """
        # 首先执行交叉网络传播
        wisdom_output = {
            "source": "wisdom_dispatcher",
            "output": initial_output,
            "hints": context.get("hints", [])
        }

        self.propagate("wisdom_dispatcher", wisdom_output,
                      FeedbackType.POSITIVE, max_hops=2)

        # 然后执行交叉织网
        return self.weave(initial_output, context, max_iterations=3)

    def get_cross_network(self) -> Dict[str, Any]:
        """获取交叉网络状态"""
        links = self.cross_graph.get_all_links()

        return {
            "total_links": len(links),
            "modules": self.cross_graph.get_all_nodes(),
            "links": [link.to_dict() for link in links],
            "signal_history_count": len(self._signal_history),
            "evolution_log_count": len(self._evolution_log)
        }

    def get_signals(self, limit: int = 50) -> List[Dict]:
        """获取最近信号"""
        with self._lock:
            recent = self._signal_history[-limit:]
            return [s.to_dict() for s in recent]

    def get_evolution_log(self, limit: int = 20) -> List[Dict]:
        """获取进化日志"""
        with self._lock:
            return self._evolution_log[-limit:]

    # ── 交叉轴分析 ──────────────────────────────────────────

    def analyze_axis(self, axis: CrossAxis) -> Dict[str, Any]:
        """分析指定交叉轴"""
        axis_modules = {
            CrossAxis.WISDOM_REASONING: ["wisdom_dispatcher", "deep_reasoning"],
            CrossAxis.MEMORY_LEARNING: ["semantic_memory", "learning_coordinator", "neural_memory"],
            CrossAxis.SCHEDULING_VALUE: ["neural_scheduler", "roi_tracker"],
            CrossAxis.AUTONOMOUS_REFLECTION: ["autonomous_agent", "reflection_engine", "goal_system"],
            CrossAxis.NEURAL_META: ["neural_memory", "reinforcement_trigger", "wisdom_dispatcher"]
        }

        modules = axis_modules.get(axis, [])

        # 获取该轴上所有链接
        links = []
        for module in modules:
            downstream = self.cross_graph.get_downstream(module)
            for target in downstream:
                if target in modules:
                    link = self.cross_graph.get_link(module, target)
                    if link:
                        links.append(link.to_dict())

        return {
            "axis": axis.value,
            "modules": modules,
            "links": links,
            "link_count": len(links)
        }

    def get_all_axes_status(self) -> Dict[str, Dict]:
        """获取所有交叉轴状态"""
        return {
            axis.value: self.analyze_axis(axis)
            for axis in CrossAxis
        }

# ── 全局实例 ─────────────────────────────────────────────────

_cross_weaver: Optional[CrossWeaver] = None
_weaver_lock = threading.Lock()

def get_cross_weaver() -> CrossWeaver:
    """获取全局交叉织网器实例"""
    global _cross_weaver
    if _cross_weaver is None:
        with _weaver_lock:
            if _cross_weaver is None:
                _cross_weaver = CrossWeaver()
    return _cross_weaver

# ── 使用示例 ─────────────────────────────────────────────────

