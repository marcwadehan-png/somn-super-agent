# -*- coding: utf-8 -*-
"""
ToT树推理引擎模块
Tree-of-Thoughts Reasoning Engine

提供树状多路径推理能力，支持：
- BFS/DFS/最佳优先搜索
- 多分支并行探索
- 状态评估与剪枝
- 回溯机制

作者: Somn AI
版本: V1.0.0
日期: 2026-04-24
"""

from __future__ import annotations

import uuid
import time
import logging
import heapq
from typing import Dict, List, Optional, Any, Callable, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod
import threading
from collections import defaultdict

logger = logging.getLogger(__name__)


class SearchStrategy(Enum):
    """搜索策略枚举"""
    BFS = "breadth_first"           # 广度优先搜索
    DFS = "depth_first"             # 深度优先搜索
    BEST_FIRST = "best_first"       # 最佳优先搜索
    MONTE_CARLO = "monte_carlo"    # 蒙特卡洛树搜索
    BEAM = "beam"                   # 束搜索


@dataclass
class ThoughtTreeNode:
    """ToT树节点"""
    node_id: str
    state: Any                       # 当前状态
    content: str                     # 推理内容
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    
    # 评估分数
    feasibility_score: float = 0.5   # 可行性评分 0-1
    progress_score: float = 0.5       # 进展性评分 0-1
    diversity_score: float = 0.5       # 多样性评分 0-1
    combined_score: float = 0.5       # 综合评分
    
    # 状态
    depth: int = 0
    status: str = "pending"          # pending/expanded/evaluated/pruned/solved
    expanded: bool = False
    
    # 元数据
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def __lt__(self, other: 'ThoughtTreeNode'):
        """支持优先队列排序"""
        return self.combined_score < other.combined_score
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'content': self.content[:100] + '...' if len(self.content) > 100 else self.content,
            'depth': self.depth,
            'status': self.status,
            'scores': {
                'feasibility': self.feasibility_score,
                'progress': self.progress_score,
                'diversity': self.diversity_score,
                'combined': self.combined_score
            },
            'child_count': len(self.children_ids)
        }


class ThoughtTree:
    """思维树"""
    
    def __init__(self, root: ThoughtTreeNode):
        self.root = root
        self.nodes: Dict[str, ThoughtTreeNode] = {root.node_id: root}
        self.children_map: Dict[str, List[str]] = defaultdict(list)
        self.parent_map: Dict[str, str] = {}
        self._node_count = 1
        
    def add_node(self, node: ThoughtTreeNode) -> bool:
        """添加节点到树"""
        if node.node_id in self.nodes:
            return False
            
        self.nodes[node.node_id] = node
        self.children_map[node.parent_id].append(node.node_id)
        if node.parent_id:
            self.parent_map[node.node_id] = node.parent_id
            # 更新父节点的children_ids
            if node.parent_id in self.nodes:
                self.nodes[node.parent_id].children_ids.append(node.node_id)
        self._node_count += 1
        return True
    
    def get_node(self, node_id: str) -> Optional[ThoughtTreeNode]:
        """获取节点"""
        return self.nodes.get(node_id)
    
    def get_children(self, node_id: str) -> List[ThoughtTreeNode]:
        """获取子节点列表"""
        child_ids = self.children_map.get(node_id, [])
        return [self.nodes[cid] for cid in child_ids if cid in self.nodes]
    
    def get_path(self, node_id: str) -> List[ThoughtTreeNode]:
        """获取从根节点到指定节点的路径"""
        path = []
        current_id = node_id
        
        while current_id and current_id in self.nodes:
            path.append(self.nodes[current_id])
            current_id = self.parent_map.get(current_id)
            
        return list(reversed(path))
    
    def prune_branch(self, node_id: str):
        """剪枝分支"""
        if node_id not in self.nodes:
            return
            
        node = self.nodes[node_id]
        node.status = "pruned"
        
        # 递归剪枝子节点
        for child_id in self.children_map.get(node_id, []):
            self.prune_branch(child_id)
    
    def get_all_nodes(self, status: Optional[str] = None) -> List[ThoughtTreeNode]:
        """获取所有节点"""
        if status:
            return [n for n in self.nodes.values() if n.status == status]
        return list(self.nodes.values())
    
    def get_stats(self) -> Dict[str, Any]:
        """获取树统计信息"""
        return {
            'total_nodes': self._node_count,
            'depth': self.root.depth if self.root else 0,
            'status_counts': {
                status: len([n for n in self.nodes.values() if n.status == status])
                for status in ['pending', 'expanded', 'evaluated', 'pruned', 'solved']
            },
            'average_score': sum(n.combined_score for n in self.nodes.values()) / max(len(self.nodes), 1)
        }


class StateEvaluator(ABC):
    """状态评估器基类"""
    
    @abstractmethod
    def evaluate(self, node: ThoughtTreeNode, problem: str, goal: Optional[str] = None) -> Dict[str, float]:
        """
        评估节点状态
        
        Returns:
            Dict包含:
            - feasibility: float 可行性评分
            - progress: float 进展性评分
            - diversity: float 多样性评分
        """
        pass
    
    @abstractmethod
    def is_goal_state(self, node: ThoughtTreeNode) -> bool:
        """判断是否为目标状态"""
        pass


class DefaultStateEvaluator(StateEvaluator):
    """默认状态评估器"""
    
    def __init__(self, goal_keywords: Optional[List[str]] = None):
        self.goal_keywords = goal_keywords or ["答案", "结论", "结果", "因此", "所以"]
    
    def evaluate(self, node: ThoughtTreeNode, problem: str, goal: Optional[str] = None) -> Dict[str, float]:
        """评估节点"""
        content = node.content.lower()
        problem_lower = problem.lower()
        
        # 可行性评估
        feasibility = 0.5
        # 排除明显不可行的标记
        invalid_markers = ["矛盾", "错误", "不行", "无法", "失败"]
        if any(marker in content for marker in invalid_markers):
            feasibility -= 0.2
        # 合理的推理步骤增加可行性
        valid_markers = ["因为", "所以", "因此", "分析", "推理"]
        if any(marker in content for marker in valid_markers):
            feasibility += 0.2
            
        # 进展性评估
        progress = 0.5
        # 更长的推理内容通常意味着更深入的进展
        if len(content) > 200:
            progress += 0.2
        # 包含结论性语言表示有进展
        conclusion_markers = ["因此", "所以", "得出", "结论"]
        if any(marker in content for marker in conclusion_markers):
            progress += 0.15
            
        # 多样性评估（相对于兄弟节点）
        diversity = 0.5
        # 这里可以添加更复杂的多样性评估逻辑
        
        return {
            'feasibility': max(0.0, min(1.0, feasibility)),
            'progress': max(0.0, min(1.0, progress)),
            'diversity': max(0.0, min(1.0, diversity))
        }
    
    def is_goal_state(self, node: ThoughtTreeNode) -> bool:
        """判断是否为目标状态"""
        content = node.content
        return any(keyword in content for keyword in self.goal_keywords)


class ThoughtGenerator(ABC):
    """思维生成器基类"""
    
    @abstractmethod
    def generate(
        self, 
        node: ThoughtTreeNode, 
        problem: str, 
        k: int = 3
    ) -> List[ThoughtTreeNode]:
        """
        生成下一步思维节点
        
        Args:
            node: 当前节点
            problem: 问题描述
            k: 生成数量
            
        Returns:
            List[ThoughtTreeNode]: 生成的新节点列表
        """
        pass


class LLMBasedThoughtGenerator(ThoughtGenerator):
    """基于LLM的思维生成器"""
    
    def __init__(
        self, 
        llm_callable: Callable[[str], str],
        prompt_template: Optional[str] = None
    ):
        self.llm_callable = llm_callable
        self.prompt_template = prompt_template or self._default_template()
    
    def _default_template(self) -> str:
        return """问题：{problem}

当前推理状态：
{current_state}

请生成{k}个不同的下一步推理方向。每个方向应该：
1. 从当前状态自然延续
2. 提供不同的分析角度
3. 保持逻辑连贯性

请用以下格式回答：
[方向1] 具体推理内容...
[方向2] 具体推理内容...
[方向3] 具体推理内容...
"""
    
    def generate(
        self, 
        node: ThoughtTreeNode, 
        problem: str, 
        k: int = 3
    ) -> List[ThoughtTreeNode]:
        """生成下一步思维"""
        prompt = self.prompt_template.format(
            problem=problem,
            current_state=node.content,
            k=k
        )
        
        try:
            response = self.llm_callable(prompt)
        except Exception as e:
            logger.error(f"LLM调用失败: {e}")
            return []
        
        # 解析生成的方向
        nodes = []
        lines = response.split('\n')
        current_content = ""
        direction_count = 0
        
        for line in lines:
            line = line.strip()
            if line.startswith('[方向') or line.startswith('[Direction'):
                if current_content and direction_count < k:
                    # 创建新节点
                    new_node = ThoughtTreeNode(
                        node_id=str(uuid.uuid4()),
                        state={"step": node.depth + 1},
                        content=current_content.strip(),
                        parent_id=node.node_id,
                        depth=node.depth + 1
                    )
                    nodes.append(new_node)
                    direction_count += 1
                current_content = line
            else:
                current_content += "\n" + line
        
        # 添加最后一个方向
        if current_content and direction_count < k:
            new_node = ThoughtTreeNode(
                node_id=str(uuid.uuid4()),
                state={"step": node.depth + 1},
                content=current_content.strip(),
                parent_id=node.node_id,
                depth=node.depth + 1
            )
            nodes.append(new_node)
        
        return nodes[:k]


@dataclass
class ToTConfig:
    """ToT配置"""
    max_depth: int = 5                    # 最大树深度
    branching_factor: int = 3             # 分支因子
    pruning_threshold: float = 0.3        # 剪枝阈值
    beam_width: int = 3                  # 束搜索宽度
    max_nodes: int = 100                 # 最大节点数
    enable_backtracking: bool = True      # 启用回溯
    strategy: SearchStrategy = SearchStrategy.BEST_FIRST
    
    # 评分权重
    feasibility_weight: float = 0.3
    progress_weight: float = 0.5
    diversity_weight: float = 0.2
    
    # BFS特定配置
    bfs_breadth_limit: int = 10
    
    # DFS特定配置
    dfs_max_unexplored: int = 5


class TreeSearchCoordinator:
    """树搜索协调器"""
    
    def __init__(
        self, 
        config: ToTConfig,
        thought_generator: ThoughtGenerator,
        state_evaluator: StateEvaluator
    ):
        self.config = config
        self.thought_generator = thought_generator
        self.state_evaluator = state_evaluator
        
        # 搜索队列
        self.pending_queue: List[ThoughtTreeNode] = []
        self.evaluated_nodes: Set[str] = set()
        
        # 历史记录
        self.search_history: List[Dict[str, Any]] = []
    
    def initialize(self, root_content: str, problem: str) -> ThoughtTree:
        """初始化搜索"""
        root = ThoughtTreeNode(
            node_id=str(uuid.uuid4()),
            state={"step": 0},
            content=root_content,
            depth=0
        )
        
        tree = ThoughtTree(root)
        self.pending_queue = [root]
        self.evaluated_nodes.clear()
        self.search_history.clear()
        
        # 评估根节点
        self._evaluate_node(root, problem)
        
        return tree
    
    def step(self, tree: ThoughtTree, problem: str) -> Tuple[ThoughtTree, bool]:
        """
        执行一步搜索
        
        Returns:
            Tuple[ThoughtTree, bool]: (更新后的树, 是否完成)
        """
        if not self.pending_queue:
            return tree, True
        
        # 根据策略选择下一个节点
        node = self._select_next_node()
        
        if node is None:
            return tree, True
        
        # 检查是否达到目标
        if self.state_evaluator.is_goal_state(node):
            node.status = "solved"
            return tree, True
        
        # 检查深度限制
        if node.depth >= self.config.max_depth:
            node.status = "expanded"
            return tree, True
        
        # 检查节点数限制
        if len(tree.nodes) >= self.config.max_nodes:
            return tree, True
        
        # 生成子节点
        children = self.thought_generator.generate(
            node, 
            problem, 
            self.config.branching_factor
        )
        
        # 添加并评估子节点
        for child in children:
            # 更新父节点
            child.parent_id = node.node_id
            child.depth = node.depth + 1
            
            # 添加到树
            tree.add_node(child)
            
            # 评估子节点
            self._evaluate_node(child, problem)
            
            # 检查是否应该加入队列
            if child.combined_score >= self.config.pruning_threshold:
                self._add_to_queue(child)
        
        node.expanded = True
        node.status = "expanded"
        
        # 剪枝低分分支
        self._prune_low_score_nodes(tree)
        
        return tree, False
    
    def _select_next_node(self) -> Optional[ThoughtTreeNode]:
        """根据策略选择下一个节点"""
        strategy = self.config.strategy
        
        if strategy == SearchStrategy.BFS:
            # 广度优先：选择深度最小且未展开的节点
            candidates = [
                n for n in self.pending_queue 
                if not n.expanded and n.depth < self.config.bfs_breadth_limit
            ]
            if not candidates:
                return None
            return min(candidates, key=lambda n: n.depth)
        
        elif strategy == SearchStrategy.DFS:
            # 深度优先：选择深度最大且未展开的节点
            candidates = [
                n for n in self.pending_queue 
                if not n.expanded
            ]
            if not candidates:
                return None
            return max(candidates, key=lambda n: n.depth)
        
        elif strategy == SearchStrategy.BEST_FIRST:
            # 最佳优先：选择综合评分最高的节点
            candidates = [
                n for n in self.pending_queue 
                if not n.expanded and n.node_id not in self.evaluated_nodes
            ]
            if not candidates:
                return None
            # 使用最大堆
            return max(candidates, key=lambda n: n.combined_score)
        
        elif strategy == SearchStrategy.BEAM:
            # 束搜索：保持beam_width个最优节点
            candidates = sorted(
                [n for n in self.pending_queue if not n.expanded],
                key=lambda n: n.combined_score,
                reverse=True
            )
            return candidates[0] if candidates else None
        
        else:
            # 默认最佳优先
            return self._select_next_node() if self.config.strategy == SearchStrategy.BEST_FIRST else None
    
    def _evaluate_node(self, node: ThoughtTreeNode, problem: str):
        """评估节点"""
        scores = self.state_evaluator.evaluate(node, problem)
        
        node.feasibility_score = scores['feasibility']
        node.progress_score = scores['progress']
        node.diversity_score = scores['diversity']
        
        # 计算综合评分
        node.combined_score = (
            self.config.feasibility_weight * scores['feasibility'] +
            self.config.progress_weight * scores['progress'] +
            self.config.diversity_weight * scores['diversity']
        )
        
        node.status = "evaluated"
        self.evaluated_nodes.add(node.node_id)
    
    def _add_to_queue(self, node: ThoughtTreeNode):
        """添加到队列"""
        # 使用最大堆性质
        heapq.heappush(self.pending_queue, node)
        # 保持队列排序
        self.pending_queue.sort(key=lambda n: n.combined_score, reverse=True)
    
    def _prune_low_score_nodes(self, tree: ThoughtTree):
        """剪枝低分节点"""
        for node in tree.nodes.values():
            if node.status not in ['pruned', 'solved'] and node.combined_score < self.config.pruning_threshold:
                tree.prune_branch(node.node_id)


class TreeOfThoughtsEngine:
    """
    ToT树推理引擎
    
    提供树状多路径推理能力，支持多种搜索策略。
    """
    
    VERSION = "6.2.0"
    
    def __init__(
        self,
        llm_callable: Optional[Callable] = None,
        config: Optional[ToTConfig] = None,
        thought_generator: Optional[ThoughtGenerator] = None,
        state_evaluator: Optional[StateEvaluator] = None
    ):
        """
        初始化ToT引擎
        
        Args:
            llm_callable: LLM调用函数
            config: ToT配置
            thought_generator: 思维生成器
            state_evaluator: 状态评估器
        """
        self.config = config or ToTConfig()
        self.llm_callable = llm_callable
        
        # 初始化组件
        if thought_generator:
            self.thought_generator = thought_generator
        elif llm_callable:
            self.thought_generator = LLMBasedThoughtGenerator(llm_callable)
        else:
            self.thought_generator = None
        
        self.state_evaluator = state_evaluator or DefaultStateEvaluator()
        self.coordinator = TreeSearchCoordinator(
            self.config,
            self.thought_generator or LLMBasedThoughtGenerator(lambda x: ""),
            self.state_evaluator
        )
        
        # 搜索状态
        self._is_searching = False
        self._search_lock = threading.Lock()
        
        # 统计信息
        self.stats = {
            'total_searches': 0,
            'solutions_found': 0,
            'average_depth': 0,
            'average_nodes': 0
        }
        
        logger.info(f"TreeOfThoughtsEngine v{self.VERSION} 初始化完成")
        logger.info(f"  - 搜索策略: {self.config.strategy.value}")
        logger.info(f"  - 最大深度: {self.config.max_depth}")
        logger.info(f"  - 分支因子: {self.config.branching_factor}")
        logger.info(f"  - 剪枝阈值: {self.config.pruning_threshold}")
    
    def solve(
        self,
        problem: str,
        initial_hint: Optional[str] = None,
        max_iterations: int = 50,
        goal: Optional[str] = None,
        llm_callable: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        使用ToT解决问題
        
        Args:
            problem: 问题描述
            initial_hint: 初始提示
            max_iterations: 最大迭代次数
            goal: 目标描述
            llm_callable: LLM调用函数
            
        Returns:
            Dict包含:
            - solution: str 最终解决方案
            - tree: ThoughtTree 完整思维树
            - path: List[Dict] 解决方案路径
            - metadata: Dict 元数据
        """
        with self._search_lock:
            self._is_searching = True
        
        try:
            # 获取LLM调用函数
            llm = llm_callable or self.llm_callable
            
            # 更新思维生成器
            if llm and not isinstance(self.thought_generator, LLMBasedThoughtGenerator):
                self.thought_generator = LLMBasedThoughtGenerator(llm)
                self.coordinator.thought_generator = self.thought_generator
            
            # 更新状态评估器
            if goal:
                self.state_evaluator = DefaultStateEvaluator(
                    goal_keywords=[goal]
                )
            
            # 初始化
            initial_content = initial_hint or f"问题：{problem}\n\n请开始分析..."
            tree = self.coordinator.initialize(initial_content, problem)
            
            # 搜索循环
            solution = None
            solution_path = None
            
            for iteration in range(max_iterations):
                # 执行一步搜索
                tree, is_complete = self.coordinator.step(tree, problem)
                
                # 检查是否完成
                if is_complete:
                    # 查找解决方案
                    solved_nodes = tree.get_all_nodes(status='solved')
                    if solved_nodes:
                        solution_node = solved_nodes[0]
                        solution = solution_node.content
                        solution_path = [n.to_dict() for n in tree.get_path(solution_node.node_id)]
                    break
                
                # 检查是否找到解决方案
                solved_nodes = tree.get_all_nodes(status='solved')
                if solved_nodes:
                    solution_node = solved_nodes[0]
                    solution = solution_node.content
                    solution_path = [n.to_dict() for n in tree.get_path(solution_node.node_id)]
                    break
            
            # 如果没有找到解决方案，选择评分最高的叶节点
            if not solution:
                leaf_nodes = [
                    n for n in tree.get_all_nodes(status='expanded')
                    if not tree.get_children(n.node_id)
                ]
                if leaf_nodes:
                    best_leaf = max(leaf_nodes, key=lambda n: n.combined_score)
                    solution = best_leaf.content
                    solution_path = [n.to_dict() for n in tree.get_path(best_leaf.node_id)]
            
            # 更新统计
            self.stats['total_searches'] += 1
            if solution:
                self.stats['solutions_found'] += 1
            
            tree_stats = tree.get_stats()
            self.stats['average_depth'] = (
                (self.stats['average_depth'] * (self.stats['total_searches'] - 1) + tree_stats['depth'])
                / self.stats['total_searches']
            )
            self.stats['average_nodes'] = (
                (self.stats['average_nodes'] * (self.stats['total_searches'] - 1) + tree_stats['total_nodes'])
                / self.stats['total_searches']
            )
            
            return {
                'solution': solution or "未找到解决方案",
                'tree': tree,
                'tree_stats': tree_stats,
                'path': solution_path or [],
                'metadata': {
                    'engine_version': self.VERSION,
                    'problem': problem[:100],
                    'iterations': iteration + 1,
                    'strategy': self.config.strategy.value,
                    'tree_stats': tree_stats
                }
            }
            
        finally:
            with self._search_lock:
                self._is_searching = False
    
    def search(
        self,
        problem: str,
        initial_hint: Optional[str] = None,
        max_iterations: int = 50,
        llm_callable: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        执行ToT搜索
        
        这是solve方法的别名，专注于搜索过程
        """
        return self.solve(problem, initial_hint, max_iterations, llm_callable=llm_callable)
    
    def set_strategy(self, strategy: SearchStrategy):
        """设置搜索策略"""
        self.config.strategy = strategy
        self.coordinator.config.strategy = strategy
        logger.info(f"搜索策略已更新: {strategy.value}")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            **self.stats,
            'is_searching': self._is_searching
        }
    
    def reset_stats(self):
        """重置统计"""
        self.stats = {
            'total_searches': 0,
            'solutions_found': 0,
            'average_depth': 0,
            'average_nodes': 0
        }


# 全局单例
_engine_instance: Optional[TreeOfThoughtsEngine] = None
_instance_lock = threading.Lock()


def get_tot_engine(
    llm_callable: Optional[Callable] = None,
    config: Optional[ToTConfig] = None
) -> TreeOfThoughtsEngine:
    """获取ToT引擎单例"""
    global _engine_instance
    
    with _instance_lock:
        if _engine_instance is None:
            _engine_instance = TreeOfThoughtsEngine(llm_callable, config)
        return _engine_instance


def create_tot_engine(
    llm_callable: Optional[Callable] = None,
    config: Optional[ToTConfig] = None,
    thought_generator: Optional[ThoughtGenerator] = None,
    state_evaluator: Optional[StateEvaluator] = None
) -> TreeOfThoughtsEngine:
    """创建新的ToT引擎实例"""
    return TreeOfThoughtsEngine(
        llm_callable, config, thought_generator, state_evaluator
    )


# 便捷函数
def solve_with_tot(
    problem: str,
    llm_callable: Callable,
    strategy: SearchStrategy = SearchStrategy.BEST_FIRST,
    max_depth: int = 5,
    branching_factor: int = 3,
    initial_hint: Optional[str] = None
) -> Dict[str, Any]:
    """
    使用ToT解决问題的便捷函数
    
    Example:
        result = solve_with_tot(
            problem="如何提高用户留存率？",
            llm_callable=lambda p: openai.Completion.create(prompt=p),
            strategy=SearchStrategy.BEST_FIRST,
            max_depth=5
        )
    """
    config = ToTConfig(
        strategy=strategy,
        max_depth=max_depth,
        branching_factor=branching_factor
    )
    
    engine = create_tot_engine(llm_callable, config)
    return engine.solve(problem, initial_hint)


__all__ = [
    'TreeOfThoughtsEngine',
    'TreeSearchCoordinator',
    'ThoughtTree',
    'ThoughtTreeNode',
    'ThoughtGenerator',
    'LLMBasedThoughtGenerator',
    'StateEvaluator',
    'DefaultStateEvaluator',
    'ToTConfig',
    'SearchStrategy',
    'get_tot_engine',
    'create_tot_engine',
    'solve_with_tot',
]
