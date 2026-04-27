"""
__all__ = [
    'get_learnable_feedbacks',
    'quick_feedback',
    'receive_feedback',
    'receive_implicit_signal',
    'roi_tracker',
    'route_to_reinforcement',
    'sync_to_roi_tracker',
]

用户反馈管道
Feedback Pipeline - 建立用户反馈到学习引擎的闭环通道

填补技术债务:此前 engagement 模块(value_reinforcement / natural_engagement)
和 learning_engine 彼此断连.本模块负责:
1. 收集并标准化各类反馈信号(显式/隐式)
2. 将反馈路由到 ROI 追踪系统和强化学习引擎
3. 支持每日学习系统的反馈整合阶段
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
class MemoryFeedbackType(Enum):
    """记忆管道反馈类型（区别于其他模块的FeedbackType）"""
    RATING = "rating"             # 评分(1-5星)
    ADOPTION = "adoption"         # 采纳(采纳/拒绝/修改)
    CORRECTION = "correction"     # corrective(修正内容)
    REJECTION = "rejection"       # 拒绝(直接否定)
    THUMBS = "thumbs"             # 点赞/点踩
    COMMENT = "comment"            # 文字评论
    SILENCE = "silence"           # 沉默(无反馈 → 隐式负面)
    ITERATION = "iteration"       # 迭代次数(修改越多 → 质量越低)
    TIME_SPENT = "time_spent"     # 耗时(超预估 → 效率问题)

class FeedbackSignal(Enum):
    """反馈信号强度"""
    STRONG_POSITIVE = 3  # 明确采纳/高评分
    WEAK_POSITIVE = 2    # 轻微认可
    NEUTRAL = 1          # 无反馈/模糊
    WEAK_NEGATIVE = -2   # 轻微不满
    STRONG_NEGATIVE = -3 # 明确拒绝/强烈不满

@dataclass
class NormalizedFeedback:
    """标准化反馈"""
    feedback_id: str
    task_id: str
    task_type: str
    strategy: str

    signal: FeedbackSignal
    reward_value: float  # 归一化奖励值 -1.0 ~ 1.0

    # 明细
    raw_type: str
    raw_value: Any
    timestamp: str

    # 上下文
    session_id: str = ""
    user_id: str = "default"

class FeedbackPipeline:
    """
    用户反馈管道

    负责接收来自 GUI / CLI / API 各渠道的反馈,
    标准化后分发到 ROI 追踪器和强化学习引擎.

    使用方式:
    1. 接收原始反馈 → receive_feedback()
    2. 批量同步到学习系统 → sync_to_roi_tracker()
    3. get可学习反馈 → get_learnable_feedbacks()
    """

    def __init__(self, base_path: str = None):
        from src.core.paths import LEARNING_DIR
        self.base_path = Path(base_path) if base_path else LEARNING_DIR / "feedback_pipeline"
        self.base_path.mkdir(parents=True, exist_ok=True)

        self.queue_path = self.base_path / "queue"
        self.archive_path = self.base_path / "archive"
        self.queue_path.mkdir(exist_ok=True)
        self.archive_path.mkdir(exist_ok=True)

        # ROI追踪器(延迟导入避免循环)
        self._roi_tracker = None

        # 反馈队列
        self._pending: List[NormalizedFeedback] = []
        self._load_queue()

    @property
    def roi_tracker(self):
        if self._roi_tracker is None:
            from .roi_tracker import ROITracker
            self._roi_tracker = ROITracker(str(self.base_path.parent))
        return self._roi_tracker

    def receive_feedback(self, raw_feedback: Dict[str, Any]) -> Optional[str]:
        """
        接收原始反馈并标准化

        Args:
            raw_feedback: 原始反馈 {
                task_id: str,
                task_type: str,
                strategy: str,
                type: str,          # FeedbackType 枚举值
                value: Any,          # 具体值
                session_id: str,
                user_id: str,
                timestamp: str,
            }

        Returns:
            标准化后的 feedback_id
        """
        required = ["task_id", "task_type", "type", "value"]
        if not all(k in raw_feedback for k in required):
            return None

        fb_id = f"FB_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

        # 标准化
        normalized = self._normalize(raw_feedback, fb_id)
        if normalized is None:
            return None

        self._pending.append(normalized)
        self._save_to_queue(normalized)
        return fb_id

    def receive_implicit_signal(self, task_id: str, task_type: str,
                                strategy: str, signal: Dict) -> Optional[str]:
        """
        接收隐式行为信号

        Args:
            signal: {
                type: "silence" | "iteration" | "time_spent",
                value: float,
                threshold: float,  # judge阈值
            }
        """
        signal_type = signal.get("type", "silence")

        if signal_type == "silence":
            value = float(signal.get("value", 0))
            threshold = float(signal.get("threshold", 300))
            if value >= threshold:
                raw = {
                    "task_id": task_id,
                    "task_type": task_type,
                    "strategy": strategy,
                    "type": "silence",
                    "value": 0.0,
                    "session_id": "system",
                }
            else:
                return None

        elif signal_type == "iteration":
            iterations = int(signal.get("value", 0))
            if iterations <= 0:
                return None
            raw = {
                "task_id": task_id,
                "task_type": task_type,
                "strategy": strategy,
                "type": "correction",
                "value": -min(1.0, iterations / 5.0),
                "session_id": "system",
            }

        elif signal_type == "time_spent":
            actual = float(signal.get("value", 0))
            estimated = float(signal.get("threshold", actual))
            if estimated <= 0:
                return None
            ratio = actual / estimated
            if ratio < 0.5:
                raw = {
                    "task_id": task_id,
                    "task_type": task_type,
                    "strategy": strategy,
                    "type": "time_spent",
                    "value": 0.5,
                    "session_id": "system",
                }
            elif ratio > 2.0:
                raw = {
                    "task_id": task_id,
                    "task_type": task_type,
                    "strategy": strategy,
                    "type": "time_spent",
                    "value": -min(1.0, (ratio - 2.0) * 0.5),
                    "session_id": "system",
                }
            else:
                return None
        else:
            return None

        raw["timestamp"] = datetime.now().isoformat()
        return self.receive_feedback(raw)

    def sync_to_roi_tracker(self) -> Dict[str, int]:
        """
        将队列中的反馈同步到 ROI 追踪器

        Returns:
            同步统计 {synced, skipped, errors}
        """
        stats = {"synced": 0, "skipped": 0, "errors": 0}
        synced_ids = []

        for fb in self._pending[:]:
            try:
                self.roi_tracker.record_user_feedback(
                    task_id=fb.task_id,
                    feedback={
                        "type": fb.raw_type,
                        "value": fb.raw_value,
                        "source": "feedback_pipeline",
                        "task_type": fb.task_type,
                    }
                )
                synced_ids.append(fb.feedback_id)
                stats["synced"] += 1
            except Exception:
                stats["errors"] += 1

        for fb_id in synced_ids:
            for fb in list(self._pending):
                if fb.feedback_id == fb_id:
                    self._archive(fb)
                    self._pending.remove(fb)
                    break

        self._save_queue()
        return stats

    def get_learnable_feedbacks(self, since: datetime = None,
                                 task_type: str = None,
                                 limit: int = 50) -> List[Dict]:
        """
        get可被学习引擎消费的标准化反馈
        """
        feedbacks = self._pending + self._load_recent_archived(since)

        if task_type:
            feedbacks = [f for f in feedbacks if f.task_type == task_type]
        if since:
            feedbacks = [
                f for f in feedbacks
                if datetime.fromisoformat(f.timestamp) >= since
            ]

        feedbacks.sort(key=lambda x: x.timestamp, reverse=True)

        return [
            {
                "feedback_id": f.feedback_id,
                "task_type": f.task_type,
                "strategy": f.strategy,
                "signal": f.signal.name,
                "reward_value": f.reward_value,
                "raw_type": f.raw_type,
                "raw_value": f.raw_value,
                "timestamp": f.timestamp,
            }
            for f in feedbacks[:limit]
        ]

    def route_to_reinforcement(self,
                               recent_feedbacks: List[NormalizedFeedback] = None
                               ) -> List[Dict]:
        """
        将反馈路由到强化学习引擎(generate learn_by_reinforcement 所需格式)
        """
        if recent_feedbacks is None:
            recent_feedbacks = self._pending[-20:] if self._pending else []

        if not recent_feedbacks:
            return []

        strategy_actions: Dict[str, List[NormalizedFeedback]] = {}
        for fb in recent_feedbacks:
            if fb.strategy not in strategy_actions:
                strategy_actions[fb.strategy] = []
            strategy_actions[fb.strategy].append(fb)

        rl_inputs = []
        for strategy, fbs in strategy_actions.items():
            avg_reward = statistics.mean(f.reward_value for f in fbs)
            outcome = {
                "success": avg_reward > 0,
                "reward": avg_reward,
                "penalty": abs(min(0, avg_reward)),
                "feedback_count": len(fbs),
            }
            previous_q = self.roi_tracker.get_strategy_roi(strategy).get("q_value", 0.5)
            rl_inputs.append({
                "action": strategy,
                "outcome": outcome,
                "previous_state": {"action_value": previous_q},
                "feedbacks": [asdict(f) for f in fbs],
            })

        return rl_inputs

    def _normalize(self, raw: Dict, fb_id: str) -> Optional[NormalizedFeedback]:
        fb_type = raw.get("type", "")
        value = raw.get("value")
        signal, reward = self._compute_signal(fb_type, value)

        try:
            return NormalizedFeedback(
                feedback_id=fb_id,
                task_id=raw.get("task_id", ""),
                task_type=raw.get("task_type", "unknown"),
                strategy=raw.get("strategy", ""),
                signal=signal,
                reward_value=reward,
                raw_type=fb_type,
                raw_value=value,
                timestamp=raw.get("timestamp", datetime.now().isoformat()),
                session_id=raw.get("session_id", ""),
                user_id=raw.get("user_id", "default"),
            )
        except Exception:
            return None

    def _compute_signal(self, fb_type: str, value: Any) -> Tuple[FeedbackSignal, float]:
        try:
            if fb_type == "rating":
                score = float(value) if value is not None else 3
                if score >= 4:
                    return FeedbackSignal.STRONG_POSITIVE, (score - 3) / 2
                elif score >= 3:
                    return FeedbackSignal.WEAK_POSITIVE, (score - 3) / 4
                elif score >= 2:
                    return FeedbackSignal.WEAK_NEGATIVE, (score - 3) / 3
                else:
                    return FeedbackSignal.STRONG_NEGATIVE, -1.0

            elif fb_type in ("adopt", "adoption", "采纳"):
                if value in (True, "true", 1, "1", "采纳", "yes"):
                    return FeedbackSignal.STRONG_POSITIVE, 1.0
                elif value in ("modified", "修改", 2):
                    return FeedbackSignal.NEUTRAL, 0.0
                else:
                    return FeedbackSignal.STRONG_NEGATIVE, -1.0

            elif fb_type in ("correction", "reject", "rejection", "corrective", "拒绝"):
                neg = float(value) if value is not None else -1.0
                if neg < -0.5:
                    return FeedbackSignal.STRONG_NEGATIVE, neg
                return FeedbackSignal.WEAK_NEGATIVE, neg

            elif fb_type in ("thumbs", "点赞"):
                if value in (True, 1, "1"):
                    return FeedbackSignal.STRONG_POSITIVE, 1.0
                return FeedbackSignal.STRONG_NEGATIVE, -1.0

            elif fb_type in ("silence",):
                return FeedbackSignal.WEAK_NEGATIVE, -0.2

            elif fb_type in ("time_spent",):
                return FeedbackSignal.NEUTRAL, float(value)

            return FeedbackSignal.NEUTRAL, 0.0

        except (TypeError, ValueError):
            return FeedbackSignal.NEUTRAL, 0.0

    def _signal_to_value(self, signal: FeedbackSignal) -> float:
        mapping = {
            FeedbackSignal.STRONG_POSITIVE: 1.0,
            FeedbackSignal.WEAK_POSITIVE: 0.5,
            FeedbackSignal.NEUTRAL: 0.0,
            FeedbackSignal.WEAK_NEGATIVE: -0.5,
            FeedbackSignal.STRONG_NEGATIVE: -1.0,
        }
        return mapping.get(signal, 0.0)

    def _save_to_queue(self, fb: NormalizedFeedback):
        path = self.queue_path / f"{fb.feedback_id}.yaml"
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(asdict(fb), f, allow_unicode=True, default_flow_style=False)

    def _load_queue(self):
        for path in sorted(self.queue_path.glob("*.yaml")):
            try:
                with open(path, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                self._pending.append(NormalizedFeedback(**data))
            except Exception:
                continue

    def _save_queue(self):
        for path in self.queue_path.glob("*.yaml"):
            try:
                path.unlink()
            except Exception as e:
                logger.debug(f"反馈管道加载失败: {e}")
        for fb in self._pending:
            self._save_to_queue(fb)

    def _archive(self, fb: NormalizedFeedback):
        path = self.archive_path / f"{fb.feedback_id}.yaml"
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(asdict(fb), f, allow_unicode=True, default_flow_style=False)

    def _load_recent_archived(self, since: datetime = None) -> List[NormalizedFeedback]:
        results = []
        for path in sorted(self.archive_path.glob("*.yaml"), reverse=True)[:100]:
            try:
                with open(path, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                fb = NormalizedFeedback(**data)
                if since is None or datetime.fromisoformat(fb.timestamp) >= since:
                    results.append(fb)
            except Exception:
                continue
        return results

def quick_feedback(task_id: str, task_type: str, strategy: str,
                   feedback_type: str, value: Any) -> str:
    """
    快速记录反馈(单行调用)

    示例:
    quick_feedback("T001", "分析", "小红书运营", "rating", 5)
    quick_feedback("T001", "分析", "小红书运营", "adoption", True)
    """
    pipeline = FeedbackPipeline()
    return pipeline.receive_feedback({
        "task_id": task_id,
        "task_type": task_type,
        "strategy": strategy,
        "type": feedback_type,
        "value": value,
        "timestamp": datetime.now().isoformat(),
    })
