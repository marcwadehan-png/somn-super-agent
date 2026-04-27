# -*- coding: utf-8 -*-
"""智能体网络效应 - AgentNetworkEffects类

__all__ = [
    'add_agent',
    'get_network_stats',
    'simulate_collaboration',
]

智能体越多 → 协作越强 → 价值越大 → 吸引更多智能体
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class AgentNetworkEffects:
    """
    智能体网络效应
    
    智能体越多 → 协作越强 → 价值越大 → 吸引更多智能体
    """
    
    def __init__(self):
        self.agents = 0
        self.connections = 0
        self.network_value = 0  # 网络价值 (梅特卡夫定律)
        self.collaboration_efficiency = 0.5
        
    def add_agent(self, agent_type: str, capabilities: List[str]):
        """添加智能体"""
        self.agents += 1
        
        # 新智能体与现有智能体建立连接
        new_connections = self.agents - 1
        self.connections += new_connections
        
        # 计算网络价值 (n^2 增长)
        self.network_value = self.agents ** 2
        
        # 协作效率提升
        self.collaboration_efficiency = min(0.95, 0.5 + self.agents * 0.01)
        
        logger.info(f"🤖 添加智能体: {agent_type}, 当前总数: {self.agents}")
    
    def get_network_stats(self) -> Dict:
        """get网络统计"""
        return {
            "total_agents": self.agents,
            "total_connections": self.connections,
            "network_value": self.network_value,
            "collaboration_efficiency": f"{self.collaboration_efficiency:.2%}",
            "value_per_agent": self.network_value / self.agents if self.agents > 0 else 0
        }
    
    def simulate_collaboration(self, task_complexity: float) -> Dict:
        """模拟智能体协作"""
        # 协作效果 = 智能体数量 × 协作效率 / 任务复杂度
        effectiveness = (self.agents * self.collaboration_efficiency) / max(1, task_complexity)
        
        # 完成时间 = 任务复杂度 / 协作效果
        completion_time = task_complexity / max(0.1, effectiveness)
        
        return {
            "effectiveness": effectiveness,
            "completion_time": completion_time,
            "success_rate": min(0.99, self.collaboration_efficiency * 0.95),
            "agents_involved": min(self.agents, int(task_complexity * 2))
        }
