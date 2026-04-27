"""神经元智慧网络 - 枚举定义"""

from enum import Enum

class NeuronState(Enum):
    """神经元状态"""
    DORMANT = "休眠"      # 未激活
    PRIMED = "预备"       # 轻度激活
    ACTIVE = "活跃"       # 正常激活
    HYPERACTIVE = "亢奋"  # 高度激活
    INTEGRATING = "整合中" # 信号整合
