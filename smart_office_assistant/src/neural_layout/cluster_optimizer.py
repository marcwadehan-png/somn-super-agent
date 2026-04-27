# -*- coding: utf-8 -*-
"""
神经网络集群优化器 V2.0
用于优化神经网络节点集群的布局和连接

优化策略:
1. 连接密度优化: 分析集群内/外连接密度，识别弱连接
2. 冗余连接修剪: 移除低权重的冗余突触
3. 缺失连接补全: 在高亲和节点间建议新连接
4. 集群间桥接优化: 增强关键跨集群桥梁连接
"""

from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
import logging
import random

logger = logging.getLogger(__name__)

__all__ = [
    "ClusterOptimizer",
    "ClusterConfig",
    "OptimizationResult",
    "get_cluster_optimizer"
]


@dataclass
class ClusterConfig:
    """集群配置"""
    cluster_id: str
    nodes: List[str]
    optimization_level: int = 3
    target_density: float = 0.7


@dataclass
class OptimizationResult:
    """优化结果"""
    cluster_id: str
    original_cost: float
    optimized_cost: float
    improvement: float
    connections_added: List[Tuple[str, str]] = field(default_factory=list)
    connections_removed: List[Tuple[str, str]] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)


class ClusterOptimizer:
    """神经网络集群优化器 V2.0 — 基于真实网络拓扑的优化"""

    def __init__(self) -> None:
        self._clusters: Dict[str, Dict] = {}
        self._optimization_history: List[OptimizationResult] = []
        self._network_ref = None  # 延迟绑定 NeuralNetwork

    def bind_network(self, network) -> None:
        """绑定 NeuralNetwork 实例，启用拓扑感知优化"""
        self._network_ref = network
        logger.info("[ClusterOptimizer] 已绑定 NeuralNetwork")

    def register_cluster(self, config: ClusterConfig) -> bool:
        """注册集群"""
        self._clusters[config.cluster_id] = {
            "config": config,
            "nodes": set(config.nodes),
            "connections": [],
        }
        logger.info(f"[ClusterOptimizer] 注册集群: {config.cluster_id} ({len(config.nodes)} 节点)")
        return True

    def _get_synapse_weight(self, source: str, target: str) -> float:
        """获取两节点间突触权重"""
        if self._network_ref is None:
            return 0.5  # 无网络引用时使用默认值

        try:
            synapse = self._network_ref.get_synapse(source, target)
            if synapse:
                return getattr(synapse, "weight", 0.5)
        except Exception as e:
            logger.debug(f"[ClusterOptimizer] 获取突触权重失败 ({source}→{target}): {e}")
        return 0.0

    def _get_node_degree(self, node_id: str) -> int:
        """获取节点连接度"""
        if self._network_ref is None:
            return 5  # 默认值

        try:
            neuron = self._network_ref.get_neuron(node_id)
            if neuron:
                return len(getattr(neuron, "connections", []) or [])
        except Exception as e:
            logger.debug(f"[ClusterOptimizer] 获取节点连接度失败 ({node_id}): {e}")
        return 0

    def _analyze_cluster_topology(self, cluster_id: str) -> Dict[str, Any]:
        """分析集群拓扑特征"""
        cluster = self._clusters[cluster_id]
        nodes = cluster["nodes"]
        n = len(nodes)

        if n == 0:
            return {"node_count": 0, "internal_edges": 0, "density": 0.0}

        # 统计集群内部连接数
        internal_edges = 0
        internal_weight_sum = 0.0
        low_weight_edges = []  # 权重 < 0.2 的弱连接

        # 统计与外部的连接数
        external_edges = 0
        external_weight_sum = 0.0

        if self._network_ref:
            try:
                # 遍历所有突触
                for syn in self._network_ref.synapses:
                    src = getattr(syn, "source_id", None)
                    tgt = getattr(syn, "target_id", None)
                    if not src or not tgt:
                        continue
                    w = getattr(syn, "weight", 0.5)

                    src_in = src in nodes
                    tgt_in = tgt in nodes

                    if src_in and tgt_in:
                        internal_edges += 1
                        internal_weight_sum += w
                        if w < 0.2:
                            low_weight_edges.append((src, tgt, w))
                    elif src_in or tgt_in:
                        external_edges += 1
                        external_weight_sum += w
            except Exception as e:
                logger.warning(f"[ClusterOptimizer] 拓扑分析失败: {e}")

        # 理论最大内部边数 = n*(n-1)/2 (有向图则为 n*(n-1))
        max_edges = n * (n - 1) if n > 1 else 1
        density = internal_edges / max_edges if max_edges > 0 else 0.0

        return {
            "node_count": n,
            "internal_edges": internal_edges,
            "external_edges": external_edges,
            "density": density,
            "avg_internal_weight": internal_weight_sum / internal_edges if internal_edges > 0 else 0.0,
            "avg_external_weight": external_weight_sum / external_edges if external_edges > 0 else 0.0,
            "low_weight_edges": low_weight_edges,
        }

    def optimize(self, cluster_id: str) -> Optional[OptimizationResult]:
        """优化指定集群 — 基于真实拓扑分析"""
        if cluster_id not in self._clusters:
            logger.warning(f"[ClusterOptimizer] 集群不存在: {cluster_id}")
            return None

        cluster = self._clusters[cluster_id]
        config = cluster["config"]
        nodes = cluster["nodes"]
        n = len(nodes)

        if n < 2:
            return OptimizationResult(
                cluster_id=cluster_id,
                original_cost=0.0, optimized_cost=0.0, improvement=0.0,
            )

        # ── 拓扑分析 ──
        topo = self._analyze_cluster_topology(cluster_id)

        # 原始代价: 节点数 + 弱连接惩罚 + 密度偏离惩罚
        density_penalty = abs(topo["density"] - config.target_density) * 50
        weak_penalty = len(topo["low_weight_edges"]) * 5
        original_cost = n * 2.0 + density_penalty + weak_penalty

        # ── 优化策略 ──
        connections_removed = []
        connections_added = []
        optimization_details = {}

        # 策略 1: 修剪弱连接 (权重 < 0.2)
        pruned = 0
        for src, tgt, w in topo["low_weight_edges"][:max(1, n // 3)]:
            connections_removed.append((src, tgt))
            pruned += 1
        optimization_details["pruned_weak_connections"] = pruned

        # 策略 2: 密度优化 — 若密度低于目标，建议补全连接
        suggested = 0
        if topo["density"] < config.target_density:
            deficit = config.target_density - topo["density"]
            # 计算需要补全的连接数
            max_edges = n * (n - 1) if n > 1 else 1
            needed = int(deficit * max_edges * 0.3)  # 补 30% 缺口
            node_list = list(nodes)

            # 基于节点连接度偏好选择高亲和节点对
            degree_map = {nid: self._get_node_degree(nid) for nid in node_list}
            candidates = sorted(node_list, key=lambda x: degree_map.get(x, 0), reverse=True)

            for i in range(min(needed, len(candidates) - 1)):
                src = candidates[i]
                # 找一个尚未直连的伙伴
                for j in range(i + 1, len(candidates)):
                    tgt = candidates[j]
                    w = self._get_synapse_weight(src, tgt)
                    if w == 0.0:  # 尚未连接
                        connections_added.append((src, tgt))
                        suggested += 1
                        break
        optimization_details["suggested_connections"] = suggested

        # 策略 3: 集群间桥接优化
        bridge_boost = 0
        if topo["external_edges"] > 0 and topo["avg_external_weight"] < 0.3:
            bridge_boost = int(topo["external_edges"] * 0.1)
        optimization_details["bridge_boost"] = bridge_boost

        # ── 计算优化后代价 ──
        new_density = topo["density"]
        if connections_added:
            max_edges = n * (n - 1) if n > 1 else 1
            new_density = (topo["internal_edges"] + len(connections_added)) / max_edges

        new_density_penalty = abs(new_density - config.target_density) * 50
        new_weak_penalty = max(0, len(topo["low_weight_edges"]) - pruned) * 5
        optimized_cost = n * 2.0 + new_density_penalty + new_weak_penalty - bridge_boost * 2
        optimized_cost = max(0.1, optimized_cost)

        improvement = (original_cost - optimized_cost) / original_cost if original_cost > 0 else 0.0

        result = OptimizationResult(
            cluster_id=cluster_id,
            original_cost=round(original_cost, 2),
            optimized_cost=round(optimized_cost, 2),
            improvement=round(improvement, 4),
            connections_added=connections_added,
            connections_removed=connections_removed,
            details={
                "topology": {
                    "density": round(topo["density"], 3),
                    "internal_edges": topo["internal_edges"],
                    "external_edges": topo["external_edges"],
                    "avg_internal_weight": round(topo.get("avg_internal_weight", 0), 3),
                },
                "strategies": optimization_details,
            },
        )

        self._optimization_history.append(result)
        logger.info(
            f"[ClusterOptimizer] 优化 {cluster_id}: "
            f"密度 {topo['density']:.2f}→{new_density:.2f}, "
            f"修剪 {pruned}, 补全 {suggested}, "
            f"改进 {improvement:.1%}"
        )

        return result

    def optimize_all(self) -> List[OptimizationResult]:
        """优化所有集群"""
        results = []
        for cluster_id in self._clusters:
            result = self.optimize(cluster_id)
            if result:
                results.append(result)
        return results

    def get_cluster(self, cluster_id: str) -> Optional[Dict]:
        """获取集群信息"""
        cluster = self._clusters.get(cluster_id)
        if cluster and self._network_ref:
            topo = self._analyze_cluster_topology(cluster_id)
            return {
                "id": cluster_id,
                "nodes": list(cluster["nodes"]),
                "topology": topo,
            }
        return self._clusters.get(cluster_id)

    def list_clusters(self) -> List[str]:
        """列出所有集群"""
        return list(self._clusters.keys())

    def get_optimization_summary(self) -> Dict[str, Any]:
        """获取优化历史摘要"""
        if not self._optimization_history:
            return {"total_optimizations": 0, "avg_improvement": 0.0}

        improvements = [r.improvement for r in self._optimization_history]
        return {
            "total_optimizations": len(self._optimization_history),
            "avg_improvement": round(sum(improvements) / len(improvements), 4),
            "best_improvement": round(max(improvements), 4),
            "latest": {
                "cluster_id": self._optimization_history[-1].cluster_id,
                "improvement": self._optimization_history[-1].improvement,
            },
        }


def get_cluster_optimizer() -> ClusterOptimizer:
    """获取集群优化器实例"""
    return ClusterOptimizer()
