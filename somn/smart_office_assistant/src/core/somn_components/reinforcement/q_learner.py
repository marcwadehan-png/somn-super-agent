# -*- coding: utf-8 -*-
"""
__all__ = [
    'apply_feedback',
    'clamp_score',
    'encode_state',
    'get_action_value_report',
    'get_q_value',
    'resolve_from_execution',
    'resolve_from_strategy_combo',
    'select_best_action',
    'update_q_value',
]

Q学习器 - QLearner
负责强化学习的核心逻辑：Q值更新、动作映射、状态编码等
"""
import logging
import hashlib
import json
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)
class ActionResolver:
    """
    动作解析器 - 把执行记录映射为可复用的强化学习动作标识

    职责：
    1. 任务状态 -> 动作标识
    2. 策略组合 -> 动作标识
    3. 结果 -> 奖励信号
    """

    def __init__(self):
        self._action_cache: Dict[str, str] = {}

    def resolve_from_execution(self, execution_record: Dict[str, Any]) -> str:
        """
        从执行记录中提取动作标识

        Returns:
            动作标识字符串
        """
        strategy = execution_record.get('strategy', 'default')
        workflow = execution_record.get('workflow', 'direct')
        intent = execution_record.get('intent_type', 'general')

        return self._make_action_key(strategy=strategy, workflow=workflow, intent=intent)

    def resolve_from_strategy_combo(self, strategies: List[str]) -> str:
        """
        从策略组合中提取动作标识

        Returns:
            动作标识字符串
        """
        combo_key = '+'.join(sorted(strategies))
        return self._make_action_key(combo=combo_key)

    def _make_action_key(self, strategy: str = None, workflow: str = None,
                         intent: str = None, combo: str = None) -> str:
        """生成动作标识"""
        if combo:
            cache_key = f"combo:{combo}"
        else:
            parts = [p for p in [strategy, workflow, intent] if p]
            cache_key = ':'.join(parts)

        if cache_key in self._action_cache:
            return self._action_cache[cache_key]

        action_id = hashlib.md5(cache_key.encode()).hexdigest()[:12]
        self._action_cache[cache_key] = action_id
        return action_id

    def clamp_score(self, score: float) -> float:
        """
        把分值限制在 0~1,避免异常评估污染反馈
        """
        return max(0.0, min(1.0, score))

class QLearner:
    """
    Q学习器 - 实现核心的Q值更新逻辑

    职责：
    1. 状态-动作Q值表管理
    2. Q值更新 (Bellman方程)
    3. 学习率/折扣因子管理
    """

    LEARNING_RATE = 0.1
    DISCOUNT_FACTOR = 0.9
    MIN_Q = 0.0
    MAX_Q = 1.0

    def __init__(self, data_dir: str = None):
        """
        初始化Q学习器

        Args:
            data_dir: Q值数据存储目录
        """
        if data_dir is None:
            data_dir = 'data/ml'

        self._data_dir = Path(data_dir)
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._q_table_file = self._data_dir / 'q_values.json'

        self._q_table: Dict[str, float] = {}
        self._lock = threading.RLock()
        self._action_resolver = ActionResolver()

        self._load_q_table()

    def _load_q_table(self) -> None:
        """从磁盘加载Q值表"""
        if self._q_table_file.exists():
            try:
                with open(self._q_table_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._q_table = data.get('q_values', {})
            except Exception:
                self._q_table = {}
        else:
            self._q_table = {}

    def _save_q_table(self) -> None:
        """保存Q值表到磁盘"""
        try:
            data = {
                'q_values': self._q_table,
                'updated_at': time.time(),
            }
            with open(self._q_table_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.debug(f"Q学习器加载失败: {e}")

    def encode_state(self, context: Dict[str, Any]) -> str:
        """
        编码状态为字符串key

        Args:
            context: 上下文字典

        Returns:
            状态key
        """
        industry = context.get('industry', 'general')
        intent_type = context.get('intent_type', 'general')
        user_id = context.get('user_id', 'default')

        state_key = f"{user_id}:{industry}:{intent_type}"
        return hashlib.md5(state_key.encode()).hexdigest()[:16]

    def get_q_value(self, state: str, action: str) -> float:
        """
        获取Q值，默认返回0.5（中性值）
        """
        key = f"{state}:{action}"
        return self._q_table.get(key, 0.5)

    def update_q_value(self, state: str, action: str, reward: float,
                      next_state: str = None, learning_rate: float = None) -> float:
        """
        Q值更新 (Bellman方程)

        Q(s,a) = Q(s,a) + α * (r + γ * max(Q(s',a')) - Q(s,a))

        Args:
            state: 当前状态
            action: 动作标识
            reward: 即时奖励
            next_state: 下一状态（可选）
            learning_rate: 学习率（可选）

        Returns:
            更新后的Q值
        """
        lr = learning_rate or self.LEARNING_RATE
        key = f"{state}:{action}"

        current_q = self.get_q_value(state, action)

        # 如果有下一状态，计算最大Q值
        if next_state:
            max_next_q = max(
                self.get_q_value(next_state, a)
                for a in self._get_available_actions(next_state)
            )
        else:
            max_next_q = 0.0

        # Bellman方程
        new_q = current_q + lr * (reward + self.DISCOUNT_FACTOR * max_next_q - current_q)

        # 限制在有效范围内
        new_q = max(self.MIN_Q, min(self.MAX_Q, new_q))

        with self._lock:
            self._q_table[key] = new_q

        return new_q

    def _get_available_actions(self, state: str) -> List[str]:
        """获取某状态下的可用动作列表"""
        # 返回已知动作或默认动作
        actions = set()
        for key in self._q_table:
            if key.startswith(f"{state}:"):
                action = key.split(':')[1]
                actions.add(action)
        if not actions:
            actions.add('default')
        return list(actions)

    def select_best_action(self, state: str, available_actions: List[str] = None) -> str:
        """
        选择最优动作（ε-greedy简化版：直接选最高Q值）

        Args:
            state: 当前状态
            available_actions: 可用动作列表

        Returns:
            最优动作标识
        """
        if not available_actions:
            available_actions = ['default']

        best_action = available_actions[0]
        best_q = -float('inf')

        for action in available_actions:
            q = self.get_q_value(state, action)
            if q > best_q:
                best_q = q
                best_action = action

        return best_action

    def apply_feedback(self, execution_record: Dict[str, Any],
                       feedback_score: float) -> None:
        """
        应用反馈更新Q值

        Args:
            execution_record: 执行记录
            feedback_score: 反馈评分(0~1)
        """
        state = self.encode_state(execution_record)
        action = self._action_resolver.resolve_from_execution(execution_record)

        # 评分转奖励
        reward = self._action_resolver.clamp_score(feedback_score)

        self.update_q_value(state, action, reward)
        self._save_q_table()

    def get_action_value_report(self) -> Dict[str, Any]:
        """
        获取动作价值报告（调试用）
        """
        with self._lock:
            return {
                'total_q_entries': len(self._q_table),
                'sample_q_values': dict(list(self._q_table.items())[:10]),
            }
