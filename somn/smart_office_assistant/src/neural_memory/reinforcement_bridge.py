"""
__all__ = [
    'get_adaptive_reward',
    'feedback_to_experience',
    'get_dqn_config',
    'get_reinforcement_bridge',
    'rl_update_to_pattern',
    'sync_to_rl',
]

强化学习桥接器 - Reinforcement Learning Bridge v1.0.0
实现反馈系统与强化学习引擎的深度集成

核心功能:
1. 反馈转换 - 将标准化反馈转换为RL经验
2. 奖励计算 - 自适应多维度奖励函数
3. 模式更新 - 将RL更新转换为知识模式更新
4. DQN配置 - 提供开箱即用的深度Q网络配置
"""

from __future__ import annotations

import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import math

import numpy as np

from src.core.paths import LEARNING_DIR

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════════

class RLStateType(Enum):
    """RL状态类型"""
    STRATEGY_CONTEXT = "strategy_context"
    TASK_CONTEXT = "task_context"
    FEEDBACK_CONTEXT = "feedback_context"
    COMPOSITE = "composite"

@dataclass
class RLExperience:
    """强化学习经验"""
    experience_id: str
    state_type: RLStateType
    state_vector: List[float]
    action: str
    reward: float
    next_state_vector: Optional[List[float]]
    done: bool
    priority: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class PatternUpdate:
    """模式更新"""
    pattern_id: str
    update_type: str  # create / enhance / diminish / delete
    confidence_delta: float
    new_confidence: float
    evidence: List[Dict]
    source: str  # rl / feedback / pattern

@dataclass
class DQNConfig:
    """DQN网络配置"""
    state_dim: int = 128
    action_dim: int = 64
    hidden_layers: List[int] = field(default_factory=lambda: [256, 128, 64])
    learning_rate: float = 0.001
    gamma: float = 0.99
    epsilon_start: float = 1.0
    epsilon_decay: float = 0.995
    epsilon_min: float = 0.01
    target_update_freq: int = 100
    replay_memory_size: int = 10000
    batch_size: int = 32

# ═══════════════════════════════════════════════════════════════════
# 强化学习桥接器
# ═══════════════════════════════════════════════════════════════════

class ReinforcementBridge:
    """
    强化学习桥接器 v1.0.0
    
    在反馈管道和强化学习引擎之间建立深度集成:
    1. 反馈信号 → RL经验
    2. RL更新 → 模式更新
    3. 自适应奖励计算
    4. 状态表示学习
    """
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else LEARNING_DIR
        self.rl_bridge_path = self.base_path / "rl_bridge"
        self.rl_bridge_path.mkdir(parents=True, exist_ok=True)
        
        # 奖励权重配置
        self.reward_weights = {
            "accuracy": 1.0,
            "efficiency": 0.8,
            "user_feedback": 1.5,
            "task_success": 2.0,
            "memory_retrieval": 1.2,
            "knowledge_gain": 1.0,
            "pattern_quality": 1.3,
            "confidence_stability": 0.5
        }
        
        # 动作空间定义
        self.action_space = {
            "DAILY": 0,
            "THREE_TIER": 1,
            "ENHANCED": 2,
            "SOLUTION": 3,
            "FEEDBACK": 4
        }
        self.action_dim = len(self.action_space)
        
        # 状态编码器配置
        self.state_encoder_config = {
            "strategy_embedding_dim": 32,
            "feedback_embedding_dim": 16,
            "context_embedding_dim": 64,
            "output_dim": 128
        }
        
        # 经验池
        self._experience_pool: List[RLExperience] = []
        self._load_experiences()
        
        logger.info("强化学习桥接器初始化完成")
        logger.info(f"  动作空间: {list(self.action_space.keys())}")
        logger.info(f"  状态维度: {self.state_encoder_config['output_dim']}")
    
    def feedback_to_experience(self,
                              feedback_data: Dict,
                              context: Optional[Dict] = None) -> RLExperience:
        """将标准化反馈转换为RL经验"""
        state_vector = self._encode_state(feedback_data, context, is_next=False)
        action = feedback_data.get("strategy", "DAILY")
        reward = self._compute_reward(feedback_data, context)
        next_state = self._encode_state(feedback_data, context, is_next=True) if context else None
        priority = self._calculate_priority(feedback_data, reward)
        
        exp_id = f"EXP_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        experience = RLExperience(
            experience_id=exp_id,
            state_type=RLStateType.COMPOSITE,
            state_vector=state_vector,
            action=action,
            reward=reward,
            next_state_vector=next_state,
            done=False,
            priority=priority,
            timestamp=datetime.now().isoformat()
        )
        
        self._experience_pool.append(experience)
        self._save_experiences()
        
        logger.debug(f"反馈→经验转换: {action}, reward={reward:.3f}")
        
        return experience
    
    def rl_update_to_pattern(self, 
                            rl_update: Dict,
                            current_patterns: List[Dict]) -> List[PatternUpdate]:
        """将RL更新转换为模式更新"""
        updates = []
        q_values = rl_update.get("action_q_values", {})
        if not q_values:
            return updates
        
        best_action = max(q_values, key=q_values.get)
        value_change = rl_update.get("value_change", 0)
        learning_rate = rl_update.get("learning_rate", 0.1)
        
        for pattern in current_patterns:
            pattern_action = pattern.get("action", "")
            
            if pattern_action == best_action:
                confidence_delta = learning_rate * value_change * 0.1
                new_confidence = min(1.0, pattern.get("confidence", 0.5) + confidence_delta)
                
                updates.append(PatternUpdate(
                    pattern_id=pattern.get("pattern_id", ""),
                    update_type="enhance",
                    confidence_delta=confidence_delta,
                    new_confidence=new_confidence,
                    evidence=[{"source": "rl", "q_value": q_values.get(best_action, 0)}],
                    source="rl"
                ))
            else:
                confidence_delta = -0.01 * abs(value_change)
                old_conf = pattern.get("confidence", 0.5)
                new_conf = max(0.1, old_conf + confidence_delta)
                
                updates.append(PatternUpdate(
                    pattern_id=pattern.get("pattern_id", ""),
                    update_type="diminish",
                    confidence_delta=confidence_delta,
                    new_confidence=new_conf,
                    evidence=[{"source": "rl"}],
                    source="rl"
                ))
        
        return updates
    
    def get_adaptive_reward(self,
                           task_result: Dict,
                           user_feedback: Optional[Dict] = None) -> float:
        """自适应奖励计算"""
        total_reward = 0.0
        
        # 准确性奖励
        accuracy = task_result.get("accuracy", 0.5)
        total_reward += self.reward_weights["accuracy"] * accuracy
        
        # 效率奖励
        efficiency = task_result.get("efficiency", 0.5)
        total_reward += self.reward_weights["efficiency"] * efficiency
        
        # 任务成功奖励
        success = task_result.get("success", False)
        total_reward += self.reward_weights["task_success"] * (1.0 if success else -0.5)
        
        # 知识获取奖励
        knowledge_gain = task_result.get("knowledge_gain", 0.0)
        total_reward += self.reward_weights["knowledge_gain"] * knowledge_gain
        
        # 模式质量奖励
        pattern_quality = task_result.get("pattern_quality", 0.5)
        total_reward += self.reward_weights["pattern_quality"] * pattern_quality
        
        # 用户反馈加成
        if user_feedback:
            fb_type = user_feedback.get("type", "")
            fb_value = user_feedback.get("value", 0)
            
            if fb_type == "rating":
                fb_reward = (fb_value - 3) / 2
                total_reward += self.reward_weights["user_feedback"] * fb_reward
            elif fb_type == "adoption" and fb_value:
                total_reward += self.reward_weights["user_feedback"] * 0.5
        
        return total_reward
    
    def sync_to_rl(self, experiences: List[RLExperience]) -> Dict[str, Any]:
        """同步经验到RL系统"""
        stats = {"synced": 0, "skipped": 0, "total_priority": 0.0}
        
        existing_ids = {e.experience_id for e in self._experience_pool}
        for exp in experiences:
            if exp.experience_id not in existing_ids:
                self._experience_pool.append(exp)
                stats["synced"] += 1
                stats["total_priority"] += exp.priority
            else:
                stats["skipped"] += 1
        
        if stats["synced"] > 0:
            stats["avg_priority"] = stats["total_priority"] / stats["synced"]
        
        self._save_experiences()
        return stats
    
    def get_dqn_config(self) -> DQNConfig:
        """获取DQN网络配置"""
        return DQNConfig(
            state_dim=self.state_encoder_config["output_dim"],
            action_dim=self.action_dim,
            hidden_layers=[256, 128, 64],
            learning_rate=0.001,
            gamma=0.99
        )
    
    def _encode_state(self, feedback_data: Dict, context: Optional[Dict], is_next: bool) -> List[float]:
        """状态编码 - 生成128维状态向量"""
        state = np.zeros(128, dtype=np.float32)
        
        # 策略嵌入 (32维)
        action = feedback_data.get("strategy", "DAILY")
        action_idx = self.action_space.get(action, 0)
        state[0:32] = self._get_embedding(action_idx, 32)
        
        # 反馈嵌入 (16维)
        feedback_type = feedback_data.get("raw_type", "")
        fb_idx = self._hash_to_idx(feedback_type, 16)
        state[32:48] = self._get_embedding(fb_idx, 16)
        
        # 上下文嵌入 (64维)
        if context:
            task_type = context.get("task_type", "")
            task_idx = self._hash_to_idx(task_type, 32)
            state[48:80] = self._get_embedding(task_idx, 32)
            
            result = context.get("task_result", {})
            accuracy = result.get("accuracy", 0.5)
            efficiency = result.get("efficiency", 0.5)
            success = 1.0 if result.get("success") else 0.0
            state[80:83] = [accuracy, efficiency, success]
        
        # 时间特征 (16维)
        if is_next:
            state[112] = 1.0
        else:
            state[112] = 0.5
        
        # 归一化
        norm = np.linalg.norm(state)
        if norm > 0:
            state = state / norm
        
        return state.tolist()
    
    def _get_embedding(self, idx: int, dim: int) -> np.ndarray:
        """生成确定性嵌入"""
        np.random.seed(idx * 1000 + 42)
        return np.random.randn(dim) * 0.1
    
    def _hash_to_idx(self, text: str, size: int) -> int:
        """文本哈希到索引"""
        return abs(hash(text)) % size
    
    def _compute_reward(self, feedback_data: Dict, context: Optional[Dict]) -> float:
        """计算奖励"""
        reward = feedback_data.get("reward_value", 0)
        
        if context:
            result = context.get("task_result", {})
            if result.get("success"):
                reward += 1.0
            else:
                reward -= 0.5
        
        return float(reward)
    
    def _calculate_priority(self, feedback_data: Dict, reward: float) -> float:
        """计算经验优先级"""
        priority = abs(reward) + 0.1
        
        fb_type = feedback_data.get("raw_type", "")
        if fb_type in ("correction", "rejection"):
            priority *= 1.5
        
        return min(priority, 5.0)
    
    def _load_experiences(self):
        """加载经验池"""
        exp_file = self.rl_bridge_path / "experiences.json"
        if exp_file.exists():
            try:
                import json
                with open(exp_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for exp_data in data:
                        exp_data["state_type"] = RLStateType(exp_data.get("state_type", "composite"))
                        self._experience_pool.append(RLExperience(**exp_data))
            except Exception as e:
                logger.warning(f"加载经验池失败: {e}")
    
    def _save_experiences(self):
        """保存经验池"""
        try:
            import json
            exp_file = self.rl_bridge_path / "experiences.json"
            
            if len(self._experience_pool) > 1000:
                self._experience_pool = self._experience_pool[-1000:]
            
            data = [
                {
                    "experience_id": e.experience_id,
                    "state_type": e.state_type.value,
                    "state_vector": e.state_vector,
                    "action": e.action,
                    "reward": e.reward,
                    "next_state_vector": e.next_state_vector,
                    "done": e.done,
                    "priority": e.priority,
                    "timestamp": e.timestamp
                }
                for e in self._experience_pool
            ]
            
            with open(exp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"保存经验池失败: {e}")


# ═══════════════════════════════════════════════════════════════════
# 便捷函数
# ═══════════════════════════════════════════════════════════════════

_bridge_instance = None

def get_reinforcement_bridge() -> ReinforcementBridge:
    """获取桥接器单例"""
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = ReinforcementBridge()
    return _bridge_instance

def feedback_to_experience(feedback_data: Dict, context: Optional[Dict] = None) -> RLExperience:
    """便捷函数：反馈转经验"""
    return get_reinforcement_bridge().feedback_to_experience(feedback_data, context)

def rl_update_to_pattern(rl_update: Dict, patterns: List[Dict]) -> List[PatternUpdate]:
    """便捷函数：RL更新转模式更新"""
    return get_reinforcement_bridge().rl_update_to_pattern(rl_update, patterns)

def get_adaptive_reward(task_result: Dict, user_feedback: Optional[Dict] = None) -> float:
    """便捷函数：计算自适应奖励"""
    return get_reinforcement_bridge().get_adaptive_reward(task_result, user_feedback)

def sync_to_rl(experiences: List[RLExperience]) -> Dict[str, Any]:
    """便捷函数：同步到RL系统"""
    return get_reinforcement_bridge().sync_to_rl(experiences)

def get_dqn_config() -> DQNConfig:
    """便捷函数：获取DQN配置"""
    return get_reinforcement_bridge().get_dqn_config()
