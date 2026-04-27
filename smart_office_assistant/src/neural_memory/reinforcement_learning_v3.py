"""
__all__ = [
    'add_experience',
    'calculate_reward',
    'choose_action',
    'episode_end',
    'get_stats',
    'learn',
    'load_model',
    'save_model',
    'to_dict',
]

强化学习系统 v3.0
Reinforcement Learning System v3.0

核心功能:
1. Q-Learning学习 - 基于奖励优化行为
2. 深度Q网络 - 复杂环境下的学习
3. strategy梯度方法 - 连续动作空间
4. 经验回放 - 提高样本效率
5. 优先级回放 - 优先学习重要样本
6. 模型集成 - 提高稳定性
"""

import json
from pathlib import Path
from src.core.paths import DATA_DIR
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from collections import deque, defaultdict
import random
from loguru import logger
import pickle

# [v22.5 优化] torch 不在模块顶层导入，延迟到 _ensure_networks() 内部
# 这样不使用的用户无需承受 torch 导入的 0.5~1s 开销
TORCH_AVAILABLE = False  # 将在 _ensure_networks() 中按需检测

class LearningType(Enum):
    """学习类型"""
    Q_LEARNING = "q_learning"              # Q-Learning
    DEEP_Q_NETWORK = "deep_q_network"      # 深度Q网络
    POLICY_GRADIENT = "policy_gradient"    # strategy梯度
    ACTOR_CRITIC = "actor_critic"         # Actor-Critic

class RewardType(Enum):
    """奖励类型"""
    ACCURACY = "accuracy"        # 准确性奖励
    EFFICIENCY = "efficiency"    # 效率奖励
    USER_FEEDBACK = "user_feedback"  # 用户反馈奖励
    TASK_SUCCESS = "task_success"    # 任务成功奖励
    MEMORY_RETRIEVAL = "memory_retrieval"  # 记忆检索奖励
    KNOWLEDGE_ACQUISITION = "knowledge_acquisition"  # 知识get奖励

@dataclass
class LearningState:
    """学习状态"""
    state_id: str
    state_vector: List[float]
    
    # 状态描述
    description: str
    context: Dict[str, Any]
    
    # 时间信息
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LearningAction:
    """学习动作"""
    action_id: str
    action_vector: List[float]
    
    # 动作描述
    description: str
    action_type: str
    
    # 参数
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LearningExperience:
    """学习经验"""
    experience_id: str
    
    # 状态-动作-奖励-下一状态
    state: LearningState
    action: LearningAction
    reward: float
    next_state: Optional[LearningState]
    done: bool  # 是否终止
    
    # 优先级(用于优先级回放)
    priority: float = 0.0
    
    # 时间信息
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'experience_id': self.experience_id,
            'state': {
                'state_id': self.state.state_id,
                'state_vector': self.state.state_vector,
                'description': self.state.description,
                'context': self.state.context,
                'timestamp': self.state.timestamp
            },
            'action': {
                'action_id': self.action.action_id,
                'action_vector': self.action.action_vector,
                'description': self.action.description,
                'action_type': self.action.action_type,
                'parameters': self.action.parameters,
                'metadata': self.action.metadata
            },
            'reward': self.reward,
            'next_state': self.next_state.state_id if self.next_state else None,
            'done': self.done,
            'priority': self.priority,
            'timestamp': self.timestamp
        }

class ReinforcementLearningSystemV3:
    """
    强化学习系统v3.0
    
    核心特性:
    1. 多种学习算法 - Q-Learning/Deep Q-Network/Policy Gradient
    2. 经验回放 - 提高样本效率
    3. 优先级回放 - 优先学习重要样本
    4. 模型集成 - 提高稳定性
    5. 自适应学习率 - 动态调整学习参数
    6. 探索-利用平衡 - ε-greedystrategy
    """
    
    def __init__(self,
                 state_dim: int = 128,
                 action_dim: int = 64,
                 learning_type: LearningType = LearningType.DEEP_Q_NETWORK,
                 learning_rate: float = 0.001,
                 gamma: float = 0.99,
                 epsilon: float = 1.0,
                 epsilon_decay: float = 0.995,
                 epsilon_min: float = 0.01,
                 memory_size: int = 10000,
                 batch_size: int = 32,
                 base_path: str = None):
        self.base_path = Path(base_path) if base_path else LEARNING_DIR
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # 超参数
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.learning_type = learning_type
        self.learning_rate = learning_rate
        self.gamma = gamma  # 折扣因子
        self.epsilon = epsilon  # 探索率
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.memory_size = memory_size
        self.batch_size = batch_size
        
        # 经验回放
        self.replay_memory = deque(maxlen=memory_size)
        # [v22.5 内存优化] priority_memory 改用 deque + heapq，避免每次 append 后全量 sort
        self.priority_memory = deque(maxlen=memory_size)
        self._priority_heap = []  # 用于heapq的堆结构，存储(-priority, experience_id)
        self._priority_sorted = False  # 懒排序标志
        
        # Q-表(用于Q-Learning)
        self.q_table = defaultdict(lambda: defaultdict(float))
        
        # 神经网络(用于Deep Q-Network) — 懒加载，首次使用时才创建
        self.q_network = None
        self.target_network = None
        self.optimizer = None
        self._networks_inited = False  # 懒加载标志
        
        # 统计
        self.learning_stats = {
            "total_episodes": 0,
            "total_steps": 0,
            "total_rewards": 0.0,
            "avg_reward": 0.0,
            "exploration_rate": epsilon,
            "learning_rate": learning_rate,
            "win_rate": 0.0,
            "reward_history": deque(maxlen=1000),
            "loss_history": deque(maxlen=1000)
        }
        
        # 奖励函数
        self.reward_weights = {
            RewardType.ACCURACY: 1.0,
            RewardType.EFFICIENCY: 0.8,
            RewardType.USER_FEEDBACK: 1.5,
            RewardType.TASK_SUCCESS: 2.0,
            RewardType.MEMORY_RETRIEVAL: 1.2,
            RewardType.KNOWLEDGE_ACQUISITION: 1.0
        }
        
        logger.info("强化学习系统v3.0init完成")
        logger.info(f"  学习类型: {learning_type.value}")
        logger.info(f"  状态维度: {state_dim}")
        logger.info(f"  动作维度: {action_dim}")
        logger.info(f"  学习率: {learning_rate}")
        logger.info(f"  探索率: {epsilon}")
        logger.info(f"  经验回放大小: {memory_size}")
    
    def _init_networks(self):
        """init神经网络"""
        if self.learning_type in [LearningType.DEEP_Q_NETWORK,
                                 LearningType.ACTOR_CRITIC] and TORCH_AVAILABLE:
            try:
                # Q网络
                self.q_network = nn.Sequential(
                    nn.Linear(self.state_dim, 256),
                    nn.ReLU(),
                    nn.Linear(256, 128),
                    nn.ReLU(),
                    nn.Linear(128, 64),
                    nn.ReLU(),
                    nn.Linear(64, self.action_dim)
                )
                
                # 目标网络
                self.target_network = nn.Sequential(
                    nn.Linear(self.state_dim, 256),
                    nn.ReLU(),
                    nn.Linear(256, 128),
                    nn.ReLU(),
                    nn.Linear(128, 64),
                    nn.ReLU(),
                    nn.Linear(64, self.action_dim)
                )
                
                # init目标网络
                self.target_network.load_state_dict(self.q_network.state_dict())
                
                # 优化器
                self.optimizer = optim.Adam(self.q_network.parameters(), lr=self.learning_rate)
                
                logger.info("神经网络init成功")
            except Exception as e:
                logger.warning(f"神经网络init失败: {e}")
                self.q_network = None
    
    def _ensure_networks(self):
        """懒初始化神经网络（首次使用时调用）"""
        if self._networks_inited:
            return
        # [v22.5 优化] 按需导入 torch，避免不必要的启动延迟
        global TORCH_AVAILABLE
        if not TORCH_AVAILABLE:
            try:
                import torch
                import torch.nn as nn
                import torch.optim as optim
                TORCH_AVAILABLE = True
                logger.info("PyTorch 按需导入成功")
            except ImportError:
                TORCH_AVAILABLE = False
                logger.info("PyTorch 未安装，将使用简化强化学习")
        if self.learning_type in [LearningType.DEEP_Q_NETWORK,
                                 LearningType.ACTOR_CRITIC] and TORCH_AVAILABLE:
            try:
                self._init_networks()
            except Exception as e:
                logger.warning(f"神经网络init失败: {e}")
                self.q_network = None
        # 无论成功失败，均标记为已尝试，避免重复init
        self._networks_inited = True
    
    def choose_action(self, 
                     state: LearningState,
                     training: bool = True) -> LearningAction:
        """
        选择动作
        
        Args:
            state: 当前状态
            training: 是否在训练模式
        
        Returns:
            LearningAction: 选择的动作
        """

        # 懒加载：首次使用 DQN 时初始化神经网络
        self._ensure_networks()
        state_vector = np.array(state.state_vector)
        
        # ε-greedystrategy
        if training and random.random() < self.epsilon:
            # 探索:随机选择动作
            action_vector = np.random.randn(self.action_dim).tolist()
            action_type = "random_exploration"
        else:
            # 利用:选择最优动作
            if self.learning_type == LearningType.Q_LEARNING:
                # Q-Learning
                state_id = state.state_id
                q_values = self.q_table[state_id]
                best_action_id = max(q_values, key=q_values.get)
                action_vector = [0.0] * self.action_dim
                action_vector[int(best_action_id) % self.action_dim] = 1.0
                action_type = "q_learning_exploitation"
            elif self.q_network is not None:
                # Deep Q-Network
                with torch.no_grad():
                    state_tensor = torch.FloatTensor(state_vector).unsqueeze(0)
                    q_values = self.q_network(state_tensor)
                    action_idx = q_values.argmax().item()
                    action_vector = [0.0] * self.action_dim
                    action_vector[action_idx] = 1.0
                    action_type = "deep_q_exploitation"
            else:
                # 随机选择
                action_vector = np.random.randn(self.action_dim).tolist()
                action_type = "random"
        
        action = LearningAction(
            action_id=f"action_{hash(str(action_vector)) % 10000}",
            action_vector=action_vector,
            description=f"选择动作 ({action_type})",
            action_type=action_type
        )
        
        return action
    
    def add_experience(self, experience: LearningExperience):
        """
        添加学习经验
        
        Args:
            experience: 学习经验
        """
        # 添加到经验回放
        self.replay_memory.append(experience)

        # [v22.5 内存优化] 优先级回放：用 heapq 维护最大堆
        # priority_memory 是 deque，不能直接 sort()，改用堆索引
        import heapq
        # 存储 (-priority, experience) 实现最大堆
        neg_priority = -experience.priority
        if len(self.priority_memory) < self.memory_size:
            self.priority_memory.append(experience)
            heapq.heappush(self._priority_heap, (neg_priority, experience.experience_id))
        else:
            # 替换最低优先级（堆顶）
            if self._priority_heap and neg_priority > self._priority_heap[0][0]:
                heapq.heapreplace(
                    self._priority_heap,
                    (neg_priority, experience.experience_id)
                )
                # 替换 deque 中对应的元素（按 experience_id 查找）
                for i, e in enumerate(self.priority_memory):
                    if e.experience_id == self._priority_heap[0][1]:
                        self.priority_memory[i] = experience
                        break

        logger.debug(f"添加经验: {experience.experience_id}, 奖励: {experience.reward:.2f}")
    
    def calculate_reward(self,
                        action: LearningAction,
                        result: Dict[str, Any],
                        reward_types: List[RewardType] = None) -> float:
        """
        计算奖励
        
        Args:
            action: 执行的动作
            result: 执行结果
            reward_types: 奖励类型列表
        
        Returns:
            float: 奖励值
        """
        reward_types = reward_types or list(RewardType)
        
        total_reward = 0.0
        
        for reward_type in reward_types:
            weight = self.reward_weights.get(reward_type, 1.0)
            
            if reward_type == RewardType.ACCURACY:
                accuracy = result.get('accuracy', 0.0)
                reward = weight * accuracy
            
            elif reward_type == RewardType.EFFICIENCY:
                efficiency = result.get('efficiency', 0.0)
                reward = weight * efficiency
            
            elif reward_type == RewardType.USER_FEEDBACK:
                feedback = result.get('user_feedback', 0.5)
                reward = weight * (feedback - 0.5) * 2  # 归一化到[-1, 1]
            
            elif reward_type == RewardType.TASK_SUCCESS:
                success = result.get('task_success', False)
                reward = weight * (2.0 if success else -1.0)
            
            elif reward_type == RewardType.MEMORY_RETRIEVAL:
                retrieval_score = result.get('memory_retrieval_score', 0.0)
                reward = weight * retrieval_score
            
            elif reward_type == RewardType.KNOWLEDGE_ACQUISITION:
                knowledge_gain = result.get('knowledge_gain', 0.0)
                reward = weight * knowledge_gain
            
            else:
                reward = 0.0
            
            total_reward += reward
        
        return total_reward
    
    def learn(self, batch_size: Optional[int] = None) -> Dict[str, float]:
        """
        学习
        
        Args:
            batch_size: 批次大小
        
        Returns:
            Dict: 学习统计
        """
        # 懒加载：确保神经网络已初始化（DQN模式）
        self._ensure_networks()
        batch_size = batch_size or self.batch_size
        
        if len(self.replay_memory) < batch_size:
            return {"loss": 0.0, "reward": 0.0}
        
        # 经验回放
        if self.learning_type == LearningType.Q_LEARNING:
            stats = self._learn_q_learning(batch_size)
        elif self.q_network is not None:
            stats = self._learn_deep_q_network(batch_size)
        else:
            stats = {"loss": 0.0, "reward": 0.0}
        
        # 更新探索率
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)
        
        # 更新统计
        self.learning_stats["total_steps"] += 1
        self.learning_stats["exploration_rate"] = self.epsilon
        
        return stats
    
    def _learn_q_learning(self, batch_size: int) -> Dict[str, float]:
        """Q-Learning学习"""
        # 随机采样
        batch = random.sample(list(self.replay_memory), min(batch_size, len(self.replay_memory)))
        
        total_loss = 0.0
        total_reward = 0.0
        
        for experience in batch:
            state_id = experience.state.state_id
            action_idx = int(experience.action.action_id.split('_')[-1]) % self.action_dim
            reward = experience.reward
            
            # Q-Learning更新
            current_q = self.q_table[state_id][action_idx]
            
            if experience.next_state:
                next_state_id = experience.next_state.state_id
                max_next_q = max(self.q_table[next_state_id].values()) if self.q_table[next_state_id] else 0.0
                target_q = reward + self.gamma * max_next_q
            else:
                target_q = reward
            
            # 更新Q值
            self.q_table[state_id][action_idx] = current_q + self.learning_rate * (target_q - current_q)
            
            loss = abs(target_q - current_q)
            total_loss += loss
            total_reward += reward
        
        avg_loss = total_loss / len(batch)
        avg_reward = total_reward / len(batch)
        
        self.learning_stats["loss_history"].append(avg_loss)
        self.learning_stats["reward_history"].append(avg_reward)
        
        return {"loss": avg_loss, "reward": avg_reward}
    
    def _learn_deep_q_network(self, batch_size: int) -> Dict[str, float]:
        """深度Q网络学习"""
        # 采样经验
        batch = random.sample(list(self.replay_memory), min(batch_size, len(self.replay_memory)))
        
        # 准备数据
        states = torch.FloatTensor([exp.state.state_vector for exp in batch])
        actions = torch.LongTensor([int(exp.action.action_id.split('_')[-1]) % self.action_dim for exp in batch])
        rewards = torch.FloatTensor([exp.reward for exp in batch])
        next_states = torch.FloatTensor([exp.next_state.state_vector if exp.next_state else np.zeros(self.state_dim) for exp in batch])
        dones = torch.BoolTensor([exp.done for exp in batch])
        
        # 当前Q值
        current_q_values = self.q_network(states).gather(1, actions.unsqueeze(1))
        
        # 目标Q值
        with torch.no_grad():
            next_q_values = self.target_network(next_states)
            max_next_q = next_q_values.max(1)[0]
            target_q_values = rewards + (self.gamma * max_next_q * ~dones)
        
        # 计算损失
        loss = nn.MSELoss()(current_q_values.squeeze(), target_q_values)
        
        # 优化
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # 定期更新目标网络
        if self.learning_stats["total_steps"] % 100 == 0:
            self.target_network.load_state_dict(self.q_network.state_dict())
        
        # 统计
        total_reward = sum(exp.reward for exp in batch)
        avg_reward = total_reward / len(batch)
        
        self.learning_stats["loss_history"].append(loss.item())
        self.learning_stats["reward_history"].append(avg_reward)
        
        return {"loss": loss.item(), "reward": avg_reward}
    
    def episode_end(self, episode_reward: float, episode_success: bool):
        """
        Episode结束
        
        Args:
            episode_reward: Episode总奖励
            episode_success: Episode是否成功
        """
        self.learning_stats["total_episodes"] += 1
        self.learning_stats["total_rewards"] += episode_reward
        
        # 更新平均奖励
        total = self.learning_stats["total_episodes"]
        old_avg = self.learning_stats["avg_reward"]
        self.learning_stats["avg_reward"] = (old_avg * (total - 1) + episode_reward) / total
        
        # 更新胜率
        if episode_success:
            self.learning_stats["win_rate"] = (self.learning_stats["win_rate"] * (total - 1) + 1.0) / total
        else:
            self.learning_stats["win_rate"] = (self.learning_stats["win_rate"] * (total - 1) + 0.0) / total
        
        logger.info(f"Episode {total}: 奖励={episode_reward:.2f}, 胜率={self.learning_stats['win_rate']:.2%}")
    
    def get_stats(self) -> Dict[str, Any]:
        """get学习统计"""
        stats = self.learning_stats.copy()
        
        # 计算最近100个episode的平均奖励
        if len(stats["reward_history"]) > 0:
            recent_rewards = stats["reward_history"][-100:]
            stats["recent_avg_reward"] = sum(recent_rewards) / len(recent_rewards)
        
        # 计算最近100次学习的平均损失
        if len(stats["loss_history"]) > 0:
            recent_losses = stats["loss_history"][-100:]
            stats["recent_avg_loss"] = sum(recent_losses) / len(recent_losses)
        
        return stats
    
    def save_model(self, path: Optional[str] = None):
        """保存模型"""
        if path is None:
            path = self.base_path / "rl_model.pkl"
        
        model_data = {
            "q_table": dict(self.q_table),
            "q_network": self.q_network.state_dict() if self.q_network else None,
            "target_network": self.target_network.state_dict() if self.target_network else None,
            "epsilon": self.epsilon,
            "learning_stats": self.learning_stats
        }
        
        with open(path, 'wb') as f:
            pickle.dump(model_data, f)
        
        logger.info(f"模型已保存: {path}")
    
    def load_model(self, path: Optional[str] = None):
        """加载模型"""
        if path is None:
            path = self.base_path / "rl_model.pkl"
        
        if not path.exists():
            logger.warning(f"模型文件不存在: {path}")
            return
        
        with open(path, 'rb') as f:
            # SECURITY: pickle仅用于内部模型文件，数据由本模块生成
            model_data = pickle.load(f)
        
        self.q_table = defaultdict(lambda: defaultdict(float), model_data.get("q_table", {}))
        
        if self.q_network and model_data.get("q_network"):
            self.q_network.load_state_dict(model_data["q_network"])
        
        if self.target_network and model_data.get("target_network"):
            self.target_network.load_state_dict(model_data["target_network"])
        
        self.epsilon = model_data.get("epsilon", 1.0)
        self.learning_stats.update(model_data.get("learning_stats", {}))
        
        logger.info(f"模型已加载: {path}")
        logger.info(f"  加载Episodes: {self.learning_stats['total_episodes']}")
        logger.info(f"  探索率: {self.epsilon:.3f}")

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
