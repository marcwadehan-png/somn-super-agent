# -*- coding: utf-8 -*-
"""
ClawReActParallel - Claw ReAct并行分支推理
===========================================

A.4 Claw ReAct并行分支：支持多条推理路径并行探索后合并

功能:
- 多路径并行ReAct推理
- 路径评分与剪枝
- 结果合并与冲突解决
- 置信度聚合

版本: v1.1.0
创建: 2026-04-24
"""

from __future__ import annotations

import logging
import time
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# 枚举定义
# ═══════════════════════════════════════════════════════════════

class PathStatus(Enum):
    """推理路径状态"""
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PRUNED = "pruned"
    MERGED = "merged"


class MergeStrategy(Enum):
    """合并策略"""
    WEIGHTED_AVERAGE = "weighted_average"    # 加权平均
    VOTE = "vote"                            # 投票
    CONFIDENCE_FIRST = "confidence_first"    # 置信度优先
    EXPERT_VOTE = "expert_vote"              # 专家投票


# ═══════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════

@dataclass
class ReasoningStep:
    """推理步骤"""
    step_type: str          # thought/action/observation/answer
    content: str
    confidence: float = 1.0
    timestamp: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReasoningPath:
    """推理路径"""
    path_id: str
    strategy: str           # 策略名称（e.g., "演绎", "归纳", "类比"）
    steps: List[ReasoningStep] = field(default_factory=list)
    final_answer: Any = None
    confidence: float = 0.0
    status: PathStatus = PathStatus.RUNNING
    score: float = 0.0      # 综合评分
    start_time: float = 0.0
    end_time: float = 0.0
    error: str = ""

    def duration(self) -> float:
        """推理耗时"""
        if self.end_time and self.start_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time

    def add_step(self, step: ReasoningStep) -> None:
        """添加推理步骤"""
        self.steps.append(step)

    def complete(self, answer: Any, confidence: float = 1.0) -> None:
        """标记完成"""
        self.final_answer = answer
        self.confidence = confidence
        self.status = PathStatus.COMPLETED
        self.end_time = time.time()

    def fail(self, error: str) -> None:
        """标记失败"""
        self.error = error
        self.status = PathStatus.FAILED
        self.end_time = time.time()


@dataclass
class MergeResult:
    """合并结果"""
    merged_answer: Any
    confidence: float
    paths_used: List[str]           # 参与合并的路径ID
    merge_strategy: MergeStrategy
    path_scores: Dict[str, float]    # 各路径评分
    details: Dict[str, Any] = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════
# ReAct执行器
# ═══════════════════════════════════════════════════════════════

class ReActExecutor:
    """
    单路径ReAct执行器。
    
    实现经典的ReAct (Reasoning + Acting) 循环。
    """

    def __init__(
        self,
        max_iterations: int = 10,
        max_depth: int = 5,
    ):
        self.max_iterations = max_iterations
        self.max_depth = max_depth

    def execute(
        self,
        query: str,
        agent_fn: Callable[[str, List[ReasoningStep]], ReasoningStep],
        context: Dict[str, Any] = None,
    ) -> ReasoningPath:
        """
        执行ReAct推理。
        
        Args:
            query: 查询问题
            agent_fn: Agent函数，输入(当前状态, 历史步骤)，输出新步骤
            context: 额外上下文
            
        Returns:
            ReasoningPath
        """
        path = ReasoningPath(
            path_id=f"react_{int(time.time() * 1000)}",
            strategy="react",
            start_time=time.time(),
        )
        
        history: List[ReasoningStep] = []
        current_state = query
        
        for i in range(self.max_iterations):
            try:
                # 调用Agent
                step = agent_fn(current_state, history)
                path.add_step(step)
                
                # 检查终止条件
                if step.step_type == "answer":
                    path.complete(step.content, step.confidence)
                    return path
                
                # 更新状态
                if step.step_type == "observation":
                    current_state = step.content
                
                # 检查深度限制
                if len(path.steps) >= self.max_depth * 2:
                    path.complete(
                        history[-1].content if history else "推理深度超限",
                        0.5
                    )
                    return path
                    
            except Exception as e:
                path.fail("并行推理失败")
                return path
        
        # 迭代耗尽
        path.complete(
            history[-1].content if history else "推理迭代超限",
            0.3
        )
        return path


# ═══════════════════════════════════════════════════════════════
# 并行分支推理管理器
# ═══════════════════════════════════════════════════════════════

class ReActParallelManager:
    """
    ReAct并行分支推理管理器。
    
    支持多条推理路径并行探索，结果合并。
    
    用法:
        manager = ReActParallelManager(max_workers=4)
        
        # 定义不同的推理策略
        strategies = [
            {"name": "演绎", "fn": deductive_agent},
            {"name": "归纳", "fn": inductive_agent},
            {"name": "类比", "fn": analogical_agent},
        ]
        
        # 并行执行
        result = manager.execute_parallel(
            query="如何解决XXX问题",
            strategies=strategies,
            merge_strategy=MergeStrategy.WEIGHTED_AVERAGE,
        )
        
        logger.info(f"合并结果: {result.merged_answer}")
        logger.info(f"置信度: {result.confidence}")
    """

    def __init__(
        self,
        max_workers: int = 4,
        timeout_per_path: float = 30.0,
        prune_threshold: float = 0.2,
    ):
        self.max_workers = max_workers
        self.timeout_per_path = timeout_per_path
        self.prune_threshold = prune_threshold
        
        self._paths: Dict[str, ReasoningPath] = {}
        self._lock = Lock()

    def execute_parallel(
        self,
        query: str,
        strategies: List[Dict[str, Any]],
        merge_strategy: MergeStrategy = MergeStrategy.WEIGHTED_AVERAGE,
        context: Dict[str, Any] = None,
        early_stop: Optional[Callable[[List[ReasoningPath]], bool]] = None,
    ) -> MergeResult:
        """
        并行执行多条推理路径。
        
        Args:
            query: 查询问题
            strategies: 策略列表 [{"name": str, "fn": Callable}]
            merge_strategy: 合并策略
            context: 上下文
            early_stop: 提前停止回调
            
        Returns:
            MergeResult
        """
        self._paths.clear()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            future_to_strategy = {}
            
            for strategy in strategies:
                name = strategy.get("name", f"strategy_{len(future_to_strategy)}")
                agent_fn = strategy.get("fn")
                
                if not agent_fn:
                    continue
                
                # 创建路径
                path = ReasoningPath(
                    path_id=f"path_{name}_{int(time.time() * 1000)}",
                    strategy=name,
                    start_time=time.time(),
                )
                self._paths[path.path_id] = path
                
                # 提交任务
                future = executor.submit(
                    self._execute_single_path,
                    path,
                    query,
                    agent_fn,
                    context,
                )
                future_to_strategy[future] = (path.path_id, name)
            
            # 收集结果
            completed_paths: List[ReasoningPath] = []
            
            for future in as_completed(future_to_strategy, timeout=self.timeout_per_path * len(strategies)):
                path_id, name = future_to_strategy[future]
                
                try:
                    path = future.result()
                    self._paths[path_id] = path
                    completed_paths.append(path)
                    
                    # 提前停止检查
                    if early_stop and early_stop(completed_paths):
                        # 取消剩余任务
                        for f in future_to_strategy:
                            f.cancel()
                        break
                        
                except Exception as e:
                    logger.error(f"[ReActParallel] Path {path_id} failed: {e}")
                    self._paths[path_id].fail("推理路径失败")
                    completed_paths.append(self._paths[path_id])
        
        # 剪枝低分路径
        self._prune_paths()
        
        # 合并结果
        return self._merge_paths(completed_paths, merge_strategy)

    def _execute_single_path(
        self,
        path: ReasoningPath,
        query: str,
        agent_fn: Callable,
        context: Dict[str, Any],
    ) -> ReasoningPath:
        """执行单条路径"""
        executor = ReActExecutor()
        
        try:
            return executor.execute(query, agent_fn, context)
        except Exception as e:
            path.fail("并行推理失败")
            return path

    def _prune_paths(self) -> None:
        """剪枝低分路径"""
        if not self._paths:
            return
        
        # 按分数排序
        sorted_paths = sorted(
            self._paths.values(),
            key=lambda p: p.score,
            reverse=True
        )
        
        # 保留前50%或最高的几条
        max_keep = max(3, len(sorted_paths) // 2)
        
        for i, path in enumerate(sorted_paths):
            if i >= max_keep:
                path.status = PathStatus.PRUNED

    def _merge_paths(
        self,
        paths: List[ReasoningPath],
        strategy: MergeStrategy,
    ) -> MergeResult:
        """合并多条路径的结果"""
        # 只合并已完成且未被剪枝的路径
        valid_paths = [
            p for p in paths
            if p.status == PathStatus.COMPLETED
        ]
        
        if not valid_paths:
            # 找得分最高的
            valid_paths = [max(paths, key=lambda p: p.score)] if paths else []
        
        if not valid_paths:
            return MergeResult(
                merged_answer=None,
                confidence=0.0,
                paths_used=[],
                merge_strategy=strategy,
                path_scores={},
            )
        
        # 计算路径权重
        total_score = sum(p.score for p in valid_paths)
        weights = {
            p.path_id: p.score / total_score if total_score > 0 else 1.0 / len(valid_paths)
            for p in valid_paths
        }
        
        merged_answer = None
        confidence = 0.0
        
        if strategy == MergeStrategy.WEIGHTED_AVERAGE:
            # 加权平均（适用于数值结果）
            answers = [p.final_answer for p in valid_paths if p.final_answer is not None]
            if answers and all(isinstance(a, (int, float)) for a in answers):
                merged_answer = sum(
                    float(a) * weights[p.path_id]
                    for a, p in zip(answers, valid_paths)
                )
                confidence = sum(p.confidence * weights[p.path_id] for p in valid_paths)
            else:
                # 非数值：取最高置信度
                best = max(valid_paths, key=lambda p: p.confidence)
                merged_answer = best.final_answer
                confidence = best.confidence * 0.8  # 降权
                
        elif strategy == MergeStrategy.VOTE:
            # 投票（适用于分类/选项）
            from collections import Counter
            answers = [str(p.final_answer) for p in valid_paths]
            counter = Counter(answers)
            merged_answer, vote_count = counter.most_common(1)[0]
            confidence = vote_count / len(valid_paths)
            
        elif strategy == MergeStrategy.CONFIDENCE_FIRST:
            # 置信度优先
            best = max(valid_paths, key=lambda p: p.confidence)
            merged_answer = best.final_answer
            confidence = best.confidence
            
        elif strategy == MergeStrategy.EXPERT_VOTE:
            # 专家投票（需要策略有专家权重）
            expert_weights = {p.strategy: p.confidence for p in valid_paths}
            total_exp_weight = sum(expert_weights.values())
            
            answer_weights: Dict[str, float] = {}
            for p in valid_paths:
                ans = str(p.final_answer)
                w = weights[p.path_id] * expert_weights.get(p.strategy, 1.0)
                answer_weights[ans] = answer_weights.get(ans, 0.0) + w
            
            merged_answer = max(answer_weights, key=answer_weights.get)
            confidence = answer_weights.get(merged_answer, 0) / total_exp_weight
        
        return MergeResult(
            merged_answer=merged_answer,
            confidence=confidence,
            paths_used=[p.path_id for p in valid_paths],
            merge_strategy=strategy,
            path_scores={p.path_id: p.score for p in valid_paths},
            details={
                "total_paths": len(paths),
                "valid_paths": len(valid_paths),
                "pruned_paths": sum(1 for p in paths if p.status == PathStatus.PRUNED),
            },
        )

    # ═══════════════════════════════════════════════════════════════
    # 辅助方法
    # ═══════════════════════════════════════════════════════════════

    def get_path(self, path_id: str) -> Optional[ReasoningPath]:
        """获取路径"""
        return self._paths.get(path_id)

    def get_all_paths(self) -> List[ReasoningPath]:
        """获取所有路径"""
        return list(self._paths.values())

    def get_best_path(self) -> Optional[ReasoningPath]:
        """获取最佳路径"""
        if not self._paths:
            return None
        return max(
            self._paths.values(),
            key=lambda p: p.score if p.status == PathStatus.COMPLETED else -1
        )

    def score_path(
        self,
        path: ReasoningPath,
        criteria: Dict[str, float] = None,
    ) -> float:
        """
        评分路径。
        
        评分维度:
        - 置信度 (conf)
        - 深度 (depth)
        - 效率 (efficiency)
        - 多样性 (diversity)
        """
        if criteria is None:
            criteria = {
                "conf": 0.4,
                "depth": 0.2,
                "efficiency": 0.2,
                "diversity": 0.2,
            }
        
        score = 0.0
        
        # 置信度
        score += criteria["conf"] * path.confidence
        
        # 深度
        depth_ratio = len(path.steps) / (self.max_workers * 2)
        score += criteria["depth"] * min(1.0, depth_ratio)
        
        # 效率（用时越短越好）
        duration = path.duration()
        if duration > 0:
            efficiency = max(0, 1 - duration / self.timeout_per_path)
            score += criteria["efficiency"] * efficiency
        
        # 多样性（不同策略越多越好）
        strategies = set(s.strategy for s in self._paths.values())
        diversity = 1.0 / len(strategies) if strategies else 0
        score += criteria["diversity"] * diversity
        
        path.score = score
        return score

    def get_stats(self) -> Dict:
        """获取统计信息"""
        paths = list(self._paths.values())
        return {
            "total_paths": len(paths),
            "completed": sum(1 for p in paths if p.status == PathStatus.COMPLETED),
            "failed": sum(1 for p in paths if p.status == PathStatus.FAILED),
            "pruned": sum(1 for p in paths if p.status == PathStatus.PRUNED),
            "avg_score": sum(p.score for p in paths) / len(paths) if paths else 0,
            "best_score": max((p.score for p in paths), default=0),
        }
