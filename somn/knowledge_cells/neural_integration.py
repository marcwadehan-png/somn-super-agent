"""
知识格子神经网络集成
====================
将知识格子系统与Somn神经网络布局系统集成

功能：
- 知识激活与神经激活联动
- 格子知识注入神经网络
- 知识驱动的拓扑优化

集成点：
- neural_layout/*.py
- neural_memory/*.py
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class ActivationType(Enum):
    """激活类型"""
    READ = "read"
    WRITE = "write"
    FUSE = "fuse"
    QUERY = "query"


@dataclass
class CellActivation:
    """格子激活记录"""
    cell_id: str
    activation_type: ActivationType
    strength: float  # 0-1
    neurons: List[str]  # 关联的神经元ID
    timestamp: float


@dataclass
class NeuralKnowledgeState:
    """神经知识状态"""
    active_cells: List[str]
    active_neurons: List[str]
    fusion_strength: float
    knowledge_flow: Dict[str, float]  # cell_id -> flow_strength


class NeuralKnowledgeBridge:
    """
    神经知识桥接器
    连接知识格子与神经网络
    """
    
    def __init__(self):
        self._activation_history: List[CellActivation] = []
        self._cell_to_neurons: Dict[str, List[str]] = {}
        self._neuron_to_cells: Dict[str, List[str]] = {}
        self._knowledge_system = None
    
    @property
    def knowledge_system(self):
        """延迟加载知识系统"""
        if self._knowledge_system is None:
            try:
                from knowledge_cells import get_knowledge_system
                self._knowledge_system = get_knowledge_system()
            except ImportError:
                return None
        return self._knowledge_system
    
    def register_mapping(self, cell_id: str, neuron_ids: List[str]):
        """
        注册格子与神经元的映射
        
        Args:
            cell_id: 格子ID
            neuron_ids: 神经元ID列表
        """
        self._cell_to_neurons[cell_id] = neuron_ids
        for nid in neuron_ids:
            if nid not in self._neuron_to_cells:
                self._neuron_to_cells[nid] = []
            self._neuron_to_cells[nid].append(cell_id)
    
    def activate_cells(self, cell_ids: List[str], 
                       activation_type: ActivationType = ActivationType.QUERY,
                       strength: float = 0.8) -> NeuralKnowledgeState:
        """
        激活格子，同时关联激活神经元
        
        Args:
            cell_ids: 要激活的格子ID
            activation_type: 激活类型
            strength: 激活强度
            
        Returns:
            神经知识状态
        """
        if not cell_ids:
            return NeuralKnowledgeState(
                active_cells=[],
                active_neurons=[],
                fusion_strength=0.0,
                knowledge_flow={}
            )
        
        active_neurons = []
        knowledge_flow = {}
        
        # 激活每个格子
        for cell_id in cell_ids:
            # 激活格子
            if self.knowledge_system:
                self.knowledge_system.engine.activate_cell(cell_id)
            
            # 获取关联神经元
            neurons = self._cell_to_neurons.get(cell_id, [])
            active_neurons.extend(neurons)
            
            knowledge_flow[cell_id] = strength
        
        # 计算融合强度
        fusion_strength = min(len(cell_ids) * 0.2, 1.0)
        
        # 记录历史
        for cell_id in cell_ids:
            self._activation_history.append(CellActivation(
                cell_id=cell_id,
                activation_type=activation_type,
                strength=strength,
                neurons=self._cell_to_neurons.get(cell_id, []),
                timestamp=0  # 简化，实际应使用time.time()
            ))
        
        return NeuralKnowledgeState(
            active_cells=cell_ids,
            active_neurons=list(set(active_neurons)),
            fusion_strength=fusion_strength,
            knowledge_flow=knowledge_flow
        )
    
    def get_knowledge_for_neuron(self, neuron_id: str) -> Dict[str, Any]:
        """
        获取神经元对应的知识
        
        Args:
            neuron_id: 神经元ID
            
        Returns:
            知识字典
        """
        if not self.knowledge_system:
            return {"enabled": False}
        
        cell_ids = self._neuron_to_cells.get(neuron_id, [])
        
        if not cell_ids:
            return {
                "enabled": True,
                "neuron_id": neuron_id,
                "cells": [],
                "knowledge": []
            }
        
        knowledge = []
        for cell_id in cell_ids:
            cell = self.knowledge_system.get_cell_content(cell_id)
            if cell:
                knowledge.append({
                    "cell_id": cell["cell_id"],
                    "name": cell["name"],
                    "content": cell.get("content", {}),
                    "activation_count": cell.get("activation_count", 0)
                })
        
        return {
            "enabled": True,
            "neuron_id": neuron_id,
            "cells": cell_ids,
            "knowledge": knowledge
        }
    
    def optimize_topology(self, active_cells: List[str]) -> Dict[str, Any]:
        """
        基于活跃格子优化拓扑
        
        Args:
            active_cells: 活跃格子列表
            
        Returns:
            优化建议
        """
        if not self.knowledge_system:
            return {"enabled": False}
        
        # 获取知识图谱
        graph = self.knowledge_system.get_knowledge_graph()
        
        # 找出活跃格子相关的边
        active_set = set(active_cells)
        relevant_edges = [
            edge for edge in graph.get("links", [])
            if edge["source"] in active_set or edge["target"] in active_set
        ]
        
        # 计算推荐的新连接
        new_connections = []
        for edge in relevant_edges:
            if edge["weight"] > 0.7:
                new_connections.append({
                    "from": edge["source"],
                    "to": edge["target"],
                    "strength": edge["weight"],
                    "reason": "high_knowledge_correlation"
                })
        
        return {
            "enabled": True,
            "active_cells": active_cells,
            "recommended_connections": new_connections,
            "graph_stats": {
                "nodes": len(graph.get("nodes", [])),
                "edges": len(graph.get("links", [])),
                "relevant_edges": len(relevant_edges)
            }
        }
    
    def fuse_knowledge(self, cell_ids: List[str]) -> Dict[str, Any]:
        """
        融合多个格子的知识
        
        Args:
            cell_ids: 格子ID列表
            
        Returns:
            融合结果
        """
        if not self.knowledge_system:
            return {"enabled": False}
        
        fusion_engine = self.knowledge_system.fusion
        
        # 获取每个格子的内容
        contents = []
        for cell_id in cell_ids:
            cell = self.knowledge_system.get_cell_content(cell_id)
            if cell:
                content = f"【{cell['name']}】"
                if "content" in cell:
                    if "what" in cell["content"]:
                        content += cell["content"]["what"]
                    if "points" in cell["content"]:
                        content += "\n" + cell["content"]["points"]
                contents.append(content)
        
        # 获取举一反三
        analogies = []
        for cell_id in cell_ids:
            analogy = self.knowledge_system.engine.get_analogy(cell_id)
            if analogy:
                analogies.append(analogy)
        
        # 获取推荐框架
        frameworks = []
        for cell_id in cell_ids:
            if cell_id.startswith("B"):
                if cell_id in ["B1", "B2", "B3"]:
                    frameworks.append("AARRR")
                elif cell_id in ["B6", "C4"]:
                    frameworks.append("4P")
                elif cell_id in ["C2", "B9"]:
                    frameworks.append("漏斗分析")
        
        return {
            "enabled": True,
            "fused_content": "\n\n".join(contents),
            "analogies": analogies,
            "frameworks": list(set(frameworks)),
            "cell_count": len(cell_ids)
        }
    
    def get_activation_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        获取激活历史
        
        Args:
            limit: 返回数量限制
            
        Returns:
            激活历史列表
        """
        history = self._activation_history[-limit:]
        return [
            {
                "cell_id": h.cell_id,
                "type": h.activation_type.value,
                "strength": h.strength,
                "neurons": h.neurons
            }
            for h in history
        ]


# 全局实例
_bridge: Optional[NeuralKnowledgeBridge] = None


def get_neural_knowledge_bridge() -> NeuralKnowledgeBridge:
    """获取神经知识桥接器单例"""
    global _bridge
    if _bridge is None:
        _bridge = NeuralKnowledgeBridge()
    return _bridge


# 预设的格子-神经元映射
DEFAULT_CELL_NEURON_MAPPINGS = {
    # 智慧核心 -> 主链神经元
    "A1": ["logic_chain_1", "logic_chain_2"],
    "A2": ["wisdom_core_1", "wisdom_core_2"],
    "A3": ["verification_1", "verification_2"],
    "A4": ["decision_1", "decision_2"],
    "A5": ["architecture_1", "architecture_2"],
    "A6": ["execution_1", "execution_2"],
    "A7": ["perception_1", "perception_2"],
    "A8": ["evolution_1", "evolution_2"],
    # 知识域 -> 对应领域神经元
    "B1": ["growth_neuron_1", "growth_neuron_2"],
    "B2": ["live_stream_1", "live_stream_2"],
    "B3": ["private_domain_1", "private_domain_2"],
    "C2": ["data_neuron_1", "data_neuron_2"],
    "C4": ["ad_neuron_1", "ad_neuron_2"],
}


def initialize_default_mappings():
    """初始化默认映射"""
    bridge = get_neural_knowledge_bridge()
    for cell_id, neuron_ids in DEFAULT_CELL_NEURON_MAPPINGS.items():
        bridge.register_mapping(cell_id, neuron_ids)


# 导出
__all__ = [
    "ActivationType",
    "CellActivation",
    "NeuralKnowledgeState",
    "NeuralKnowledgeBridge",
    "get_neural_knowledge_bridge",
    "initialize_default_mappings",
    "DEFAULT_CELL_NEURON_MAPPINGS",
]
