# -*- coding: utf-8 -*-
"""
神经网络布局管理器
统一管理神经网络布局的创建、调度和优化

V2.0: 完善布局管理接口，支持多布局管理
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)

# 从network_layout_manager导入实际类（使用相对导入，保持包内一致性）
from .network_layout_manager import (
    NetworkLayoutManager,
    FunctionNeuron,
    ConnectionWeight,
    PhaseSystemStatus,
)

__all__ = [
    "NeuralLayoutManager",
    "LayoutConfig",
    "LayoutInfo",
    "get_layout_manager",
    "NetworkLayoutManager",
    "FunctionNeuron",
    "ConnectionWeight",
    "PhaseSystemStatus",
]


@dataclass
class LayoutConfig:
    """布局配置"""
    layout_id: str = ""
    name: str = ""
    description: str = ""
    neurons: List[str] = field(default_factory=list)
    synapses: List[Tuple[str, str, float]] = field(default_factory=list)
    optimization_level: int = 3


@dataclass
class LayoutInfo:
    """布局信息"""
    layout_id: str
    name: str
    description: str
    created_at: str
    neuron_count: int = 0
    synapse_count: int = 0
    is_active: bool = False


class NeuralLayoutManager(NetworkLayoutManager):
    """
    神经网络布局管理器 (继承NetworkLayoutManager)
    提供统一的多布局管理接口
    """
    
    _instance = None
    
    def __new__(cls) -> 'NeuralLayoutManager':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._singleton_inited = False
        return cls._instance
    
    def __init__(self) -> None:
        if self._singleton_inited:
            return
        super().__init__()
        self._singleton_inited = True
        
        # 多布局管理
        self._layouts: Dict[str, LayoutInfo] = {}
        self._active_layout_id: Optional[str] = None
        
        # 默认全局布局
        self._register_default_layout()
        
        logger.info("NeuralLayoutManager V2.0 initialized")
    
    def _register_default_layout(self) -> None:
        """注册默认全局布局"""
        layout_id = "somn_global_layout"
        info = LayoutInfo(
            layout_id=layout_id,
            name="Somn 全局神经网络布局",
            description="Somn 系统默认全局布局，包含主链路/智慧学派/记忆/自主系统",
            created_at=datetime.now().isoformat(),
            is_active=True,
        )
        self._layouts[layout_id] = info
        self._active_layout_id = layout_id
    
    def create_layout(self, config: LayoutConfig) -> Dict:
        """创建新布局
        
        Args:
            config: 布局配置
            
        Returns:
            创建结果
        """
        if not config.layout_id:
            config.layout_id = f"layout_{uuid.uuid4().hex[:8]}"
        
        info = LayoutInfo(
            layout_id=config.layout_id,
            name=config.name or f"布局 {config.layout_id}",
            description=config.description or "",
            created_at=datetime.now().isoformat(),
            neuron_count=len(config.neurons),
            synapse_count=len(config.synapses),
        )
        self._layouts[config.layout_id] = info
        logger.info(f"布局已创建: {config.layout_id} ({config.name})")
        
        return {
            "layout_id": config.layout_id,
            "name": config.name,
            "status": "created",
            "neurons": len(config.neurons),
            "synapses": len(config.synapses),
        }
    
    def get_layout(self, layout_id: str) -> Optional[Dict]:
        """获取指定布局信息
        
        Args:
            layout_id: 布局ID
            
        Returns:
            布局信息，不存在则返回None
        """
        info = self._layouts.get(layout_id)
        if not info:
            return None
        
        result = {
            "layout_id": info.layout_id,
            "name": info.name,
            "description": info.description,
            "created_at": info.created_at,
            "neuron_count": info.neuron_count,
            "synapse_count": info.synapse_count,
            "is_active": info.is_active,
        }
        
        # 如果是活跃布局，附加完整状态
        if info.is_active and self.initialized:
            result["network_status"] = self.get_layout_status()
            result["phase_status"] = self.get_phase_status()
        
        return result
    
    def switch_layout(self, layout_id: str) -> bool:
        """切换活跃布局
        
        Args:
            layout_id: 目标布局ID
            
        Returns:
            是否切换成功
        """
        if layout_id not in self._layouts:
            logger.warning(f"布局不存在: {layout_id}")
            return False
        
        # 取消当前活跃布局
        if self._active_layout_id and self._active_layout_id in self._layouts:
            self._layouts[self._active_layout_id].is_active = False
        
        # 设置新活跃布局
        self._layouts[layout_id].is_active = True
        self._active_layout_id = layout_id
        logger.info(f"已切换到布局: {layout_id}")
        return True
    
    def optimize_layout(self, layout_id: str = None) -> Dict:
        """优化指定布局的集群连接
        
        Args:
            layout_id: 布局ID（默认优化活跃布局）
            
        Returns:
            优化结果
        """
        target_id = layout_id or self._active_layout_id
        if not target_id or target_id not in self._layouts:
            return {"error": f"布局不存在: {target_id}"}
        
        results = self.optimize_clusters()
        return {
            "layout_id": target_id,
            "optimized": len(results),
            "results": results,
        }
    
    def list_layouts(self) -> List[Dict]:
        """列出所有布局
        
        Returns:
            布局列表
        """
        return [
            {
                "layout_id": info.layout_id,
                "name": info.name,
                "neuron_count": info.neuron_count,
                "synapse_count": info.synapse_count,
                "is_active": info.is_active,
                "created_at": info.created_at,
            }
            for info in self._layouts.values()
        ]
    
    def delete_layout(self, layout_id: str) -> bool:
        """删除指定布局（不能删除活跃布局）
        
        Args:
            layout_id: 布局ID
            
        Returns:
            是否删除成功
        """
        if layout_id not in self._layouts:
            return False
        if layout_id == self._active_layout_id:
            logger.warning("不能删除活跃布局")
            return False
        if layout_id == "somn_global_layout":
            logger.warning("不能删除默认全局布局")
            return False
        
        del self._layouts[layout_id]
        logger.info(f"布局已删除: {layout_id}")
        return True
    
    def get_active_layout_id(self) -> Optional[str]:
        """获取当前活跃布局ID"""
        return self._active_layout_id
    
    def get_manager_summary(self) -> Dict:
        """获取管理器摘要信息"""
        return {
            "version": "2.0",
            "initialized": self.initialized,
            "active_layout": self._active_layout_id,
            "total_layouts": len(self._layouts),
            "network": {
                "main_chain_nodes": len(self.main_chain_mapping),
                "wisdom_nodes": len(self.wisdom_mapping),
                "memory_nodes": len(self.memory_mapping),
                "autonomy_nodes": len(self.autonomy_mapping),
            } if self.initialized else None,
            "phase_system": self.get_phase_status() if self.initialized else None,
            "execution_history": len(self._execution_history),
        }


def get_layout_manager() -> NeuralLayoutManager:
    """获取布局管理器单例"""
    return NeuralLayoutManager()
