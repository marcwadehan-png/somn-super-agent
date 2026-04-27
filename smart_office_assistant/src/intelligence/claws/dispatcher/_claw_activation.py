# Claw激活与调度系统
# v4.2.0: 关联度计算 + 激活调度

from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import heapq

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════
# 调度优先级
# ═══════════════════════════════════════════════════════════════════

class ActivationPriority(Enum):
    """激活优先级"""
    CRITICAL = 1   # 关键
    HIGH = 2        # 高
    NORMAL = 3      # 正常
    LOW = 4          # 低
    IDLE = 5         # 空闲


# ═══════════════════════════════════════════════════════════════════
# Claw调度状态
# ═══════════════════════════════════════════════════════════════════

@dataclass
class ClawActivationState:
    """Claw激活状态"""
    claw_name: str
    last_activation: str = ""           # ISO时间戳
    activation_count: int = 0
    activation_score: float = 0.0       # 激活分数
    priority: ActivationPriority = ActivationPriority.NORMAL
    is_active: bool = False
    context_match: float = 0.0          # 上下文匹配度
    
    def update_activation(self) -> None:
        """更新激活"""
        self.activation_count += 1
        self.last_activation = datetime.now().isoformat()
        self.is_active = True
    
    def calculate_score(self, current_time: datetime) -> float:
        """计算激活分数"""
        # 基础分数
        score = self.activation_score
        
        # 时间衰减（越久未激活分数越高）
        if self.last_activation:
            try:
                last = datetime.fromisoformat(self.last_activation)
                hours_since = (current_time - last).total_seconds() / 3600
                score += min(hours_since * 0.1, 1.0)  # 最多加1分
            except Exception as e:
                logger.debug(f"score += min(hours_since * 0.1, 1.0)  # 最多加1分失败: {e}")
        
        # 上下文匹配加成
        score += self.context_match * 0.5
        
        self.activation_score = min(score, 10.0)  # 最高10分
        return score


# ═══════════════════════════════════════════════════════════════════
# 关联度计算引擎
# ═══════════════════════════════════════════════════════════════════

class CorrelationComputer:
    """
    关联度计算引擎
    
    基于多维度计算Claw/格子间的关联度
    """
    
    # 关联维度权重
    WEIGHTS = {
        "tag": 0.3,        # 标签相似度
        "content": 0.25,    # 内容相似度
        "role": 0.2,       # 角色关联
        "skill": 0.15,     # 技能关联
        "history": 0.1     # 历史协作
    }
    
    def __init__(self):
        self._correlation_cache: Dict[Tuple[str, str], float] = {}
    
    def calculate_claw_correlation(
        self,
        claw1_tags: List[str],
        claw2_tags: List[str],
        claw1_skills: List[str] = None,
        claw2_skills: List[str] = None,
        role_relation: str = "none"  # none/complementary/competitive/similar
    ) -> float:
        """
        计算两个Claw的关联度
        
        Args:
            claw1_tags: Claw1标签
            claw2_tags: Claw2标签
            claw1_skills: Claw1技能
            claw2_skills: Claw2技能
            role_relation: 角色关系
            
        Returns:
            float: 关联度 0.0-1.0
        """
        # 1. 标签关联度 (Jaccard)
        tags_corr = self._jaccard_similarity(
            set(claw1_tags), 
            set(claw2_tags)
        )
        
        # 2. 技能关联度
        skills_corr = 0.0
        if claw1_skills and claw2_skills:
            skills_corr = self._jaccard_similarity(
                set(claw1_skills),
                set(claw2_skills)
            )
        
        # 3. 角色关系
        role_corr = self._role_similarity(role_relation)
        
        # 综合计算
        correlation = (
            tags_corr * self.WEIGHTS["tag"] +
            skills_corr * self.WEIGHTS["skill"] +
            role_corr * self.WEIGHTS["role"]
        )
        
        return min(correlation, 1.0)
    
    def _jaccard_similarity(self, set1: set, set2: set) -> float:
        """Jaccard相似度"""
        if not set1 or not set2:
            return 0.0
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0.0
    
    def _role_similarity(self, relation: str) -> float:
        """角色关系相似度"""
        mapping = {
            "similar": 0.9,
            "complementary": 0.7,
            "competitive": 0.3,
            "none": 0.1
        }
        return mapping.get(relation, 0.1)
    
    def find_collaborators(
        self,
        current_claw: str,
        available_claws: Dict[str, Dict],
        max_count: int = 2
    ) -> List[Tuple[str, float]]:
        """
        查找最佳协作者
        
        Args:
            current_claw: 当前Claw
            available_claws: 可用Claw字典
            max_count: 最大协作者数量
            
        Returns:
            List[Tuple[str, float]]: (Claw名称, 关联度)
        """
        current = available_claws.get(current_claw, {})
        current_tags = current.get("tags", [])
        current_skills = current.get("skills", [])
        
        candidates = []
        for name, claw in available_claws.items():
            if name == current_claw:
                continue
            
            corr = self.calculate_claw_correlation(
                current_tags,
                claw.get("tags", []),
                current_skills,
                claw.get("skills", [])
            )
            candidates.append((name, corr))
        
        # 按关联度排序，取前max_count个
        return heapq.nlargest(max_count, candidates, key=lambda x: x[1])
    
    def build_correlation_matrix(
        self,
        claws: Dict[str, Dict]
    ) -> Dict[Tuple[str, str], float]:
        """
        构建关联矩阵
        
        Args:
            claws: Claw字典
            
        Returns:
            Dict: (claw1, claw2) -> 关联度
        """
        matrix = {}
        names = list(claws.keys())
        
        for i, name1 in enumerate(names):
            for name2 in names[i+1:]:
                corr = self.calculate_claw_correlation(
                    claws[name1].get("tags", []),
                    claws[name2].get("tags", []),
                    claws[name1].get("skills", []),
                    claws[name2].get("skills", [])
                )
                matrix[(name1, name2)] = corr
                matrix[(name2, name1)] = corr
        
        return matrix


# ═══════════════════════════════════════════════════════════════════
# 激活与调度引擎
# ═══════════════════════════════════════════════════════════════════

class ActivationScheduler:
    """
    激活与调度引擎
    
    功能：
    - 根据关联度激活Claw
    - 调度优先级管理
    - 协作推荐
    """
    
    MAX_ACTIVE_CLAWS = 3      # 最大活跃Claw数量
    ACTIVATION_COOLDOWN = 300   # 激活冷却时间(秒)
    PRIORITY_THRESHOLDS = {
        ActivationPriority.CRITICAL: 8.0,
        ActivationPriority.HIGH: 6.0,
        ActivationPriority.NORMAL: 4.0,
        ActivationPriority.LOW: 2.0,
    }
    
    def __init__(self):
        self._states: Dict[str, ClawActivationState] = {}
        self._correlation = CorrelationComputer()
        self._activation_history: List[Dict[str, Any]] = []
    
    def register_claw(self, name: str) -> None:
        """注册Claw"""
        if name not in self._states:
            self._states[name] = ClawActivationState(claw_name=name)
            logger.info(f"[Scheduler] 注册Claw: {name}")
    
    def register_claws(self, names: List[str]) -> None:
        """批量注册Claw"""
        for name in names:
            self.register_claw(name)
    
    def activate(
        self,
        claw_name: str,
        context_match: float = 0.5,
        forced: bool = False
    ) -> bool:
        """
        激活Claw
        
        Args:
            claw_name: Claw名称
            context_match: 上下文匹配度
            forced: 强制激活
            
        Returns:
            bool: 是否激活成功
        """
        # 检查是否已注册
        if claw_name not in self._states:
            self.register_claw(claw_name)
        
        state = self._states[claw_name]
        now = datetime.now()
        
        # 检查冷却时间
        if not forced and state.last_activation:
            try:
                last = datetime.fromisoformat(state.last_activation)
                if (now - last).total_seconds() < self.ACTIVATION_COOLDOWN:
                    logger.info(f"[Scheduler] {claw_name} 冷却中")
                    return False
            except Exception as e:
                logger.debug(f"return False失败: {e}")
        
        # 检查活跃数量限制
        active_count = sum(1 for s in self._states.values() if s.is_active)
        if not forced and active_count >= self.MAX_ACTIVE_CLAWS:
            # 尝试替换最低优先级
            self._evict_lowest_priority()
        
        # 更新状态
        state.context_match = context_match
        state.calculate_score(now)
        state.update_activation()
        
        # 记录历史
        self._activation_history.append({
            "claw": claw_name,
            "timestamp": now.isoformat(),
            "context_match": context_match,
            "score": state.activation_score
        })
        
        logger.info(f"[Scheduler] 激活Claw: {claw_name} (score={state.activation_score:.2f})")
        return True
    
    def _evict_lowest_priority(self) -> None:
        """驱逐最低优先级Claw"""
        active = [s for s in self._states.values() if s.is_active]
        if not active:
            return
        
        # 找到最低分
        lowest = min(active, key=lambda s: s.activation_score)
        lowest.is_active = False
        logger.info(f"[Scheduler] 驱逐Claw: {lowest.claw_name}")
    
    def get_active_claws(self) -> List[str]:
        """获取活跃Claw列表"""
        return [s.claw_name for s in self._states.values() if s.is_active]
    
    def recommend_collaborators(
        self,
        current_claw: str,
        available_claws: Dict[str, Dict]
    ) -> List[Tuple[str, float]]:
        """
        推荐协作者
        
        Args:
            current_claw: 当前Claw
            available_claws: 可用Claw
            
        Returns:
            List[Tuple[str, float]]: (Claw名称, 推荐分数)
        """
        # 获取关联度最高的
        return self._correlation.find_collaborators(
            current_claw,
            available_claws,
            max_count=2
        )
    
    def get_activation_stats(self) -> Dict[str, Any]:
        """获取激活统计"""
        return {
            "total_claws": len(self._states),
            "active_claws": len(self.get_active_claws()),
            "activation_history_count": len(self._activation_history),
            "states": {
                name: {
                    "count": s.activation_count,
                    "score": s.activation_score,
                    "is_active": s.is_active,
                    "last_activation": s.last_activation
                }
                for name, s in self._states.items()
            }
        }
    
    def auto_schedule(
        self,
        query: str,
        claw_configs: Dict[str, Dict]
    ) -> List[str]:
        """
        自动调度
        
        Args:
            query: 用户查询
            claw_configs: Claw配置字典
            
        Returns:
            List[str]: 调度的Claw列表
        """
        scheduled = []
        
        # 根据查询匹配置信度最高的Claw
        query_lower = query.lower()
        
        # 计算每个Claw的匹配度
        scores = []
        for name, config in claw_configs.items():
            # 注册
            self.register_claw(name)
            
            # 计算匹配度
            match = 0.0
            triggers = config.get("triggers", [])
            for trigger in triggers:
                if trigger.lower() in query_lower:
                    match += 0.3
            
            # 激活
            if self.activate(name, context_match=match):
                scheduled.append(name)
            
            if len(scheduled) >= self.MAX_ACTIVE_CLAWS:
                break
        
        return scheduled


# ═══════════════════════════════════════════════════════════════════
# 导出
# ═══════════════════════════════════════════════════════════════════

__all__ = [
    "ActivationPriority",
    "ClawActivationState",
    "CorrelationComputer",
    "ActivationScheduler",
]