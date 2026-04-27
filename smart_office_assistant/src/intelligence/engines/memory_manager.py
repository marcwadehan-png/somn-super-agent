"""
__all__ = [
    'access_memory',
    'apply_forgetting_curve',
    'consolidate_memories',
    'export_memory_state',
    'get_low_activation_memories',
    'get_memory_tier_distribution',
    'get_statistics',
    'optimize_memory_layout',
    'MemoryManager',
]

智能记忆管理器 - 神经记忆系统的智能管理核心

功能:
- 记忆强化 - 基于访问频率和重要性
- 记忆遗忘 - 艾宾浩斯遗忘曲线
- 记忆巩固 - 短期转长期记忆
- 智能调度 - 优化记忆访问

[v20.0 升级] 使用统一 MemoryTier 枚举

作者: Somn AI
版本: v4.1.0 (2026-04-23)
"""

import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)

# 使用统一的 MemoryTier (v20.0)
try:
    from src.neural_memory.memory_types import UnifiedMemoryTier, MemoryTier
except ImportError:
    # 兼容：若统一类型不可用，使用本地定义
    class UnifiedMemoryTier(Enum):
        HOT = "hot"
        WARM = "warm"
        COLD = "cold"
        EPISODIC = "episodic"
    
    class MemoryTier(Enum):
        HOT = "hot"
        WARM = "warm"
        COLD = "cold"

# 使用兼容别名
MemoryTier = UnifiedMemoryTier

class MemoryManager:
    """
    智能记忆管理器
    
    核心功能:
    1. 记忆强化 - 提升重要记忆的激活度
    2. 记忆遗忘 - 艾宾浩斯遗忘曲线
    3. 记忆巩固 - 层级迁移和持久化
    4. 智能调度 - 优化记忆访问效率
    """
    
    def __init__(self):
        """init记忆管理器"""
        # 记忆存储
        self.hot_memories: Dict[str, Dict] = {}  # 热记忆池
        self.warm_memories: Dict[str, Dict] = {} # 温记忆池
        self.cold_memories: Dict[str, Dict] = {} # 冷记忆池
        
        # 配置参数
        self.config = {
            # 访问频率阈值
            'hot_threshold': 10,      # 访问次数 > 10 → 热
            'warm_threshold': 5,      # 访问次数 > 5 → 温
            
            # 记忆衰减参数
            'decay_rate': 0.1,        # 遗忘速度
            'forgetting_days': [1, 6, 30],  # 艾宾浩斯曲线关键点
            
            # 记忆巩固阈值
            'consolidation_threshold': 0.8,  # 激活度 > 0.8 → 巩固
            
            # 容量限制
            'hot_capacity': 1000,       # 热记忆容量
            'warm_capacity': 10000,    # 温记忆容量
            'cold_capacity': 1000000, # 冷记忆容量
        }
        
        # 统计信息
        self.stats = {
            'total_memories': 0,
            'hot_count': 0,
            'warm_count': 0,
            'cold_count': 0,
            'consolidations': 0,
            'promotions': 0,
            'demotions': 0,
            'forgets': 0
        }
        
        logger.info("记忆管理器init完成")
    
    def access_memory(self, memory_id: str) -> Optional[Dict]:
        """
        访问记忆 - 触发强化和调度
        
        Args:
            memory_id: 记忆ID
            
        Returns:
            记忆数据或None
        """
        # 查找记忆
        memory = self._find_memory(memory_id)
        
        if memory:
            # 更新访问统计
            memory['access_count'] += 1
            memory['last_accessed'] = datetime.now()
            
            # 计算激活度
            activation = self._calculate_activation(memory)
            memory['activation'] = activation
            
            # 强化记忆
            self._strengthen_memory(memory)
            
            # 检查是否需要层级迁移
            self._check_tier_migration(memory)
            
            return memory
        
        return None
    
    def _find_memory(self, memory_id: str) -> Optional[Dict]:
        """在所有层级中查找记忆"""
        # 先查热记忆
        if memory_id in self.hot_memories:
            return self.hot_memories[memory_id]
        
        # 再查温记忆
        if memory_id in self.warm_memories:
            # 访问时可能需要提升到热层
            return self.warm_memories[memory_id]
        
        # 最后查冷记忆
        if memory_id in self.cold_memories:
            return self.cold_memories[memory_id]
        
        return None
    
    def _calculate_activation(self, memory: Dict) -> float:
        """
        计算记忆激活度
        
        公式:
        activation = base_importance * (1 + log(access_count + 1)) * time_factor
        
        Args:
            memory: 记忆数据
            
        Returns:
            激活度 (0-1)
        """
        # 基础重要性
        base_importance = memory.get('importance', 0.5)
        
        # 访问频率增强
        access_count = memory.get('access_count', 0)
        frequency_boost = np.log(access_count + 1)
        
        # 时间衰减
        created = memory.get('created_at', datetime.now())
        days_since_creation = (datetime.now() - created).days
        time_factor = np.exp(-self.config['decay_rate'] * days_since_creation / 10)
        
        # 计算激活度
        activation = base_importance * (1 + frequency_boost) * time_factor
        
        # 归一化到0-1
        activation = max(0.0, min(1.0, activation))
        
        return activation
    
    def _strengthen_memory(self, memory: Dict):
        """
        记忆强化 - 提升重要性
        
        Args:
            memory: 记忆数据
        """
        # 基于访问频率强化
        if memory['access_count'] % 10 == 0:
            boost = 0.05
            memory['importance'] = min(1.0, memory['importance'] + boost)
            logger.debug(f"记忆 {memory['id']} 强化: +{boost:.2f}")
    
    def _check_tier_migration(self, memory: Dict):
        """
        检查并执行层级迁移
        
        Args:
            memory: 记忆数据
        """
        current_tier = memory.get('tier', MemoryTier.COLD)
        activation = memory['activation']
        access_count = memory['access_count']
        
        # 提升层级
        if (current_tier == MemoryTier.COLD and 
            (activation > self.config['consolidation_threshold'] or 
             access_count > self.config['warm_threshold'])):
            self._promote_memory(memory, MemoryTier.WARM)
        
        elif (current_tier == MemoryTier.WARM and 
              access_count > self.config['hot_threshold']):
            self._promote_memory(memory, MemoryTier.HOT)
        
        # 降级层级
        elif (current_tier == MemoryTier.HOT and 
              activation < self.config['consolidation_threshold']):
            self._demote_memory(memory, MemoryTier.WARM)
        
        elif (current_tier == MemoryTier.WARM and 
              activation < 0.3):
            self._demote_memory(memory, MemoryTier.COLD)
    
    def _promote_memory(self, memory: Dict, target_tier: MemoryTier):
        """提升记忆层级"""
        old_tier = memory['tier']
        memory['tier'] = target_tier
        
        # 执行迁移
        memory_id = memory['id']
        if old_tier == MemoryTier.COLD:
            del self.cold_memories[memory_id]
            self.warm_memories[memory_id] = memory
        elif old_tier == MemoryTier.WARM:
            del self.warm_memories[memory_id]
            self.hot_memories[memory_id] = memory
        
        self.stats['promotions'] += 1
        logger.info(f"记忆提升: {memory_id} {old_tier.value} → {target_tier.value}")
    
    def _demote_memory(self, memory: Dict, target_tier: MemoryTier):
        """降级记忆层级"""
        old_tier = memory['tier']
        memory['tier'] = target_tier
        
        # 执行迁移
        memory_id = memory['id']
        if old_tier == MemoryTier.HOT:
            del self.hot_memories[memory_id]
            self.warm_memories[memory_id] = memory
        elif old_tier == MemoryTier.WARM:
            del self.warm_memories[memory_id]
            self.cold_memories[memory_id] = memory
        
        self.stats['demotions'] += 1
        logger.debug(f"记忆降级: {memory_id} {old_tier.value} → {target_tier.value}")
    
    def apply_forgetting_curve(self):
        """
        应用艾宾浩斯遗忘曲线
        
        遗忘曲线:
        - 1天后: 保留34%
        - 6天后: 保留25%
        - 30天后: 保留21%
        """
        logger.info("应用遗忘曲线...")
        
        for tier_name, memories in [
            ('hot', self.hot_memories),
            ('warm', self.warm_memories),
            ('cold', self.cold_memories)
        ]:
            to_forget = []
            
            for memory_id, memory in memories.items():
                days_since_access = (datetime.now() - memory['last_accessed']).days
                
                # 计算遗忘率
                if days_since_access >= 30:
                    retention_rate = 0.21
                elif days_since_access >= 6:
                    retention_rate = 0.25
                elif days_since_access >= 1:
                    retention_rate = 0.34
                else:
                    continue  # 不遗忘
                
                # 降低激活度
                memory['activation'] *= retention_rate
                
                # 检查是否应该遗忘
                if (memory['activation'] < 0.1 and 
                    memory['importance'] < 0.3):
                    to_forget.append(memory_id)
            
            # 执行遗忘
            for memory_id in to_forget:
                del memories[memory_id]
                self.stats['forgets'] += 1
                logger.debug(f"遗忘记忆: {memory_id} from {tier_name}")
    
    def consolidate_memories(self):
        """
        记忆巩固 - 将高激活度记忆持久化
        """
        logger.info("执行记忆巩固...")
        
        # 巩固热记忆
        hot_to_consolidate = []
        for memory_id, memory in self.hot_memories.items():
            if memory['activation'] > self.config['consolidation_threshold']:
                hot_to_consolidate.append(memory)
        
        # 巩固温记忆
        warm_to_consolidate = []
        for memory_id, memory in self.warm_memories.items():
            if memory['activation'] > self.config['consolidation_threshold']:
                warm_to_consolidate.append(memory)
        
        # 标记为已巩固
        for memory in hot_to_consolidate + warm_to_consolidate:
            memory['consolidated'] = True
            memory['consolidated_at'] = datetime.now()
            self.stats['consolidations'] += 1
        
        logger.info(f"巩固记忆: {len(hot_to_consolidate) + len(warm_to_consolidate)} 条")
    
    def optimize_memory_layout(self):
        """
        优化记忆布局 - 确保容量限制
        """
        logger.info("优化记忆布局...")
        
        # 检查热记忆容量
        while len(self.hot_memories) > self.config['hot_capacity']:
            # 找到最低激活度的热记忆
            lowest_memory = min(
                self.hot_memories.values(),
                key=lambda m: m['activation']
            )
            self._demote_memory(lowest_memory, MemoryTier.WARM)
        
        # 检查温记忆容量
        while len(self.warm_memories) > self.config['warm_capacity']:
            # 找到最低激活度的温记忆
            lowest_memory = min(
                self.warm_memories.values(),
                key=lambda m: m['activation']
            )
            self._demote_memory(lowest_memory, MemoryTier.COLD)
        
        # 检查冷记忆容量
        while len(self.cold_memories) > self.config['cold_capacity']:
            # 找到最低激活度的冷记忆
            lowest_memory = min(
                self.cold_memories.values(),
                key=lambda m: m['activation']
            )
            # 删除冷记忆
            del self.cold_memories[lowest_memory['id']]
            self.stats['forgets'] += 1
    
    def get_statistics(self) -> Dict:
        """get统计信息"""
        self.stats['total_memories'] = (
            len(self.hot_memories) +
            len(self.warm_memories) +
            len(self.cold_memories)
        )
        self.stats['hot_count'] = len(self.hot_memories)
        self.stats['warm_count'] = len(self.warm_memories)
        self.stats['cold_count'] = len(self.cold_memories)
        
        return self.stats
    
    def get_memory_tier_distribution(self) -> Dict[str, int]:
        """get记忆层级分布"""
        return {
            'hot': len(self.hot_memories),
            'warm': len(self.warm_memories),
            'cold': len(self.cold_memories)
        }
    
    def get_low_activation_memories(self, tier: MemoryTier, threshold: float = 0.3) -> List[Dict]:
        """get低激活度记忆"""
        if tier == MemoryTier.HOT:
            memories = self.hot_memories
        elif tier == MemoryTier.WARM:
            memories = self.warm_memories
        else:
            memories = self.cold_memories
        
        return [
            memory for memory in memories.values()
            if memory['activation'] < threshold
        ]
    
    def export_memory_state(self, filepath: str):
        """导出记忆状态"""
        state = {
            'hot_memories': {
                mid: {
                    k: str(v) if isinstance(v, datetime) else v
                    for k, v in m.items()
                }
                for mid, m in self.hot_memories.items()
            },
            'warm_memories': {
                mid: {
                    k: str(v) if isinstance(v, datetime) else v
                    for k, v in m.items()
                }
                for mid, m in self.warm_memories.items()
            },
            'cold_memories': {
                mid: {
                    k: str(v) if isinstance(v, datetime) else v
                    for k, v in m.items()
                }
                for mid, m in self.cold_memories.items()
            },
            'stats': self.stats,
            'config': self.config,
            'exported_at': str(datetime.now())
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        
        logger.info(f"记忆状态已导出: {filepath}")
