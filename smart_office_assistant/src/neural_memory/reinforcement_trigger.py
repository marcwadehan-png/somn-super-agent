"""
__all__ = [
    'apply_decay',
    'get_action_confidence',
    'get_best_action',
    'get_q_values',
    'get_recent_updates',
    'learning_engine',
    'push_feedback',
    'push_roi_feedback',
    'should_trigger',
    'trigger_update',
]

强化学习触发器
Reinforcement Trigger - 将反馈信号闭环到 learning_engine

填补技术债务:learning_engine.learn_by_reinforcement() 框架就绪但从未被调用.
本模块负责:
1. 监听反馈管道中的 reward 信号
2. 积累足够的样本后触发 Q-learning 更新
3. 将更新结果写入记忆系统
4. 与 ROI 追踪器联动,get action value
"""

import logging
import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import statistics

logger = logging.getLogger(__name__)
class TriggerMode(Enum):
    """触发模式"""
    IMMEDIATE = "immediate"     # 每次反馈立即触发
    BATCH = "batch"             # 积累到阈值后批量触发(默认)
    PERIODIC = "periodic"       # 每日定时触发

@dataclass
class RLUpdate:
    """强化学习更新记录"""
    update_id: str
    timestamp: str
    action: str
    q_value_before: float
    q_value_after: float
    reward: float
    learning_rate: float
    n_samples: int
    source: str  # "feedback" | "roi_tracker" | "validation"

class ReinforcementTrigger:
    """
    强化学习触发器

    核心逻辑:Simple Q-learning
    Q(a) = Q(a) + alpha * (r - Q(a))
    其中 alpha = 强化学习率,r = 奖励信号

    使用方式:
    1. init → ReinforcementTrigger()
    2. 积累反馈 → push_feedback()
    3. 检查触发条件 → should_trigger()
    4. 执行 Q-learning 更新 → trigger_update()
    """

    def __init__(self, base_path: str = None):
        from src.core.paths import LEARNING_DIR
        self.base_path = Path(base_path) if base_path else LEARNING_DIR / "rl_trigger"
        self.base_path.mkdir(parents=True, exist_ok=True)

        self.updates_path = self.base_path / "updates"
        self.q_values_path = self.base_path / "q_values"
        self.updates_path.mkdir(exist_ok=True)
        self.q_values_path.mkdir(exist_ok=True)

        self.params = {
            "learning_rate": 0.1,
            "discount_factor": 0.9,
            "batch_threshold": 5,
            "decay_rate": 0.01,
            "min_q_value": 0.0,
            "max_q_value": 1.0,
            "trigger_mode": TriggerMode.BATCH,
            "periodic_hours": 24,
        }

        self._reward_buffer: Dict[str, List[float]] = {}
        self._q_table: Dict[str, float] = {}
        self._load_q_table()

        self._learning_engine = None
        self._recent_updates: List[RLUpdate] = []

    @property
    def learning_engine(self):
        if self._learning_engine is None:
            from .learning_engine import LearningEngine
            self._learning_engine = LearningEngine(str(self.base_path.parent.parent))
        return self._learning_engine

    def push_feedback(self, action: str, reward: float) -> None:
        """推送奖励信号到缓冲区"""
        if action not in self._reward_buffer:
            self._reward_buffer[action] = []
        reward = max(-1.0, min(1.0, reward))
        self._reward_buffer[action].append(reward)

    def push_roi_feedback(self, action: str, roi_record: Dict) -> None:
        """从 ROI 追踪器推送反馈(效率分作为奖励)"""
        quality = roi_record.get("quality_score", 0.5)
        adopted = roi_record.get("adopted", 0)
        fb_score = roi_record.get("feedback_score", 0.5)
        combined_reward = quality * 0.4 + adopted * 0.4 + (fb_score - 0.5) * 0.2
        self.push_feedback(action, combined_reward)

    def should_trigger(self) -> bool:
        """检查是否满足触发条件"""
        mode = self.params["trigger_mode"]
        if mode == TriggerMode.IMMEDIATE:
            return any(len(v) >= 1 for v in self._reward_buffer.values())
        elif mode == TriggerMode.BATCH:
            return any(len(v) >= self.params["batch_threshold"]
                      for v in self._reward_buffer.values())
        elif mode == TriggerMode.PERIODIC:
            last_update = self._get_last_update_time()
            if last_update is None:
                return True
            elapsed = datetime.now() - last_update
            return elapsed >= timedelta(hours=self.params["periodic_hours"])
        return False

    def trigger_update(self, force: bool = False) -> List[RLUpdate]:
        """执行 Q-learning 更新"""
        if not force and not self.should_trigger():
            return []

        updates = []
        alpha = self.params["learning_rate"]

        for action, rewards in list(self._reward_buffer.items()):
            if not rewards:
                continue

            avg_reward = statistics.mean(rewards)
            old_q = self._q_table.get(action, 0.5)
            new_q = old_q + alpha * (avg_reward - old_q)
            new_q = max(self.params["min_q_value"], min(self.params["max_q_value"], new_q))
            self._q_table[action] = new_q

            try:
                event = self.learning_engine.learn_by_reinforcement(
                    action=action,
                    outcome={
                        "success": avg_reward > 0,
                        "reward": avg_reward,
                        "penalty": abs(min(0, avg_reward)),
                        "n_samples": len(rewards),
                    },
                    previous_state={"action_value": old_q}
                )
                if event:
                    self.learning_engine.save_learning_event(event)
            except Exception as e:
                logger.debug(f"强化触发器更新失败: {e}")

            update = RLUpdate(
                update_id=f"RL_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                timestamp=datetime.now().isoformat(),
                action=action,
                q_value_before=old_q,
                q_value_after=new_q,
                reward=avg_reward,
                learning_rate=alpha,
                n_samples=len(rewards),
                source="reinforcement_trigger",
            )
            updates.append(update)
            self._recent_updates.append(update)
            self._save_update(update)
            self._reward_buffer[action] = []

        if updates:
            self._save_q_table()
        return updates

    def get_q_values(self) -> Dict[str, float]:
        """get当前所有strategy的 Q 值"""
        return dict(self._q_table)

    def get_best_action(self) -> Tuple[Optional[str], float]:
        """get最优动作(Q值最高的strategy)"""
        if not self._q_table:
            return None, 0.5
        min_samples = 3
        candidates = {
            a: q for a, q in self._q_table.items()
            if self._get_action_sample_count(a) >= min_samples
        }
        if not candidates:
            best = max(self._q_table.items(), key=lambda x: self._get_action_sample_count(x[0]))
            return best
        return max(candidates.items(), key=lambda x: x[1])

    def get_action_confidence(self, action: str) -> float:
        """get某strategyQ值的置信度"""
        count = self._get_action_sample_count(action)
        return min(1.0, count / 20.0)

    def apply_decay(self) -> int:
        """对所有Q值应用自然衰减"""
        decayed = 0
        for action, q in list(self._q_table.items()):
            last_update = self._get_action_last_update(action)
            if last_update:
                days_idle = (datetime.now() - last_update).days
                if days_idle > 7:
                    factor = min(1.0, days_idle / 7 * self.params["decay_rate"])
                    new_q = q + factor * (0.5 - q)
                    self._q_table[action] = new_q
                    decayed += 1
        if decayed > 0:
            self._save_q_table()
        return decayed

    def get_recent_updates(self, limit: int = 20) -> List[Dict]:
        """get最近的更新记录"""
        return [asdict(u) for u in self._recent_updates[-limit:]]

    def _get_action_sample_count(self, action: str) -> int:
        return sum(1 for f in self._recent_updates if f.action == action)

    def _get_action_last_update(self, action: str) -> Optional[datetime]:
        updates = [u for u in self._recent_updates if u.action == action]
        if not updates:
            return None
        return datetime.fromisoformat(max(u.timestamp for u in updates))

    def _get_last_update_time(self) -> Optional[datetime]:
        if not self._recent_updates:
            return None
        return datetime.fromisoformat(max(u.timestamp for u in self._recent_updates))

    def _save_update(self, update: RLUpdate):
        path = self.updates_path / f"{update.update_id}.yaml"
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(asdict(update), f, allow_unicode=True, default_flow_style=False)

    def _save_q_table(self):
        path = self.q_values_path / "q_table.yaml"
        with open(path, "w", encoding="utf-8") as f:
            data = {k: float(v) for k, v in self._q_table.items()}
            yaml.dump(data, f, default_flow_style=False)

    def _load_q_table(self):
        path = self.q_values_path / "q_table.yaml"
        if path.exists():
            try:
                with open(path, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                self._q_table = {k: float(v) for k, v in (data or {}).items()}
            except Exception:
                self._q_table = {}
        for p in sorted(self.updates_path.glob("*.yaml"))[-200:]:
            try:
                with open(p, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                self._recent_updates.append(RLUpdate(**data))
            except Exception:
                continue
