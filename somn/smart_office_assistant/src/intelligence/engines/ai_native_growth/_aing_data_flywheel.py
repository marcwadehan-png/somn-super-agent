# -*- coding: utf-8 -*-
"""AI数据飞轮 - AIDataFlywheel类

__all__ = [
    'get_state',
    'project_growth',
    'simulate_step',
]

用户越多 → 数据越多 → AI越智能 → 体验越好 → 用户越多
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class AIDataFlywheel:
    """
    AI数据飞轮
    
    用户越多 → 数据越多 → AI越智能 → 体验越好 → 用户越多
    """
    
    def __init__(self):
        self.users = 0
        self.data_points = 0
        self.model_accuracy = 0.7  # 初始准确率
        self.user_satisfaction = 3.5  # 初始满意度
        self.flywheel_speed = 1.0  # 飞轮转速
        
        # 飞轮参数
        self.data_per_user = 100  # 每个用户产生的数据点
        self.accuracy_improvement_rate = 0.001  # 每1000数据点提升准确率
        self.satisfaction_impact = 0.5  # 准确率对满意度的影响
        self.viral_coefficient = 0.1  # 病毒系数
        
    def simulate_step(self, days: int = 1):
        """模拟飞轮运转"""
        for _ in range(days):
            # 1. 用户产生数据
            new_data = self.users * self.data_per_user
            self.data_points += new_data
            
            # 2. 数据提升AI准确率
            accuracy_gain = (new_data / 1000) * self.accuracy_improvement_rate
            self.model_accuracy = min(0.99, self.model_accuracy + accuracy_gain)
            
            # 3. AI准确率提升用户满意度
            satisfaction_gain = accuracy_gain * self.satisfaction_impact * 10
            self.user_satisfaction = min(5.0, self.user_satisfaction + satisfaction_gain)
            
            # 4. 满意度带来新用户 (病毒传播)
            new_users = int(self.users * self.viral_coefficient * (self.user_satisfaction / 5.0))
            self.users += new_users
            
            # 5. 飞轮加速
            self.flywheel_speed = 1.0 + (self.model_accuracy - 0.7) * 2
    
    def get_state(self) -> Dict:
        """get飞轮状态"""
        return {
            "users": self.users,
            "data_points": self.data_points,
            "model_accuracy": f"{self.model_accuracy:.2%}",
            "user_satisfaction": f"{self.user_satisfaction:.2f}/5.0",
            "flywheel_speed": f"{self.flywheel_speed:.2f}x",
            "viral_coefficient": self.viral_coefficient
        }
    
    def project_growth(self, days: int) -> List[Dict]:
        """预测增长轨迹"""
        projections = []
        
        # 保存当前状态
        original_state = {
            "users": self.users,
            "data_points": self.data_points,
            "model_accuracy": self.model_accuracy,
            "user_satisfaction": self.user_satisfaction
        }
        
        for day in range(days):
            self.simulate_step(1)
            projections.append({
                "day": day + 1,
                "users": self.users,
                "model_accuracy": self.model_accuracy,
                "satisfaction": self.user_satisfaction
            })
        
        # 恢复状态
        self.users = original_state["users"]
        self.data_points = original_state["data_points"]
        self.model_accuracy = original_state["model_accuracy"]
        self.user_satisfaction = original_state["user_satisfaction"]
        
        return projections
