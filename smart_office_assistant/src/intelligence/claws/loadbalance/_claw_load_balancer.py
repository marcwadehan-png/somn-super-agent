# -*- coding: utf-8 -*-
"""
ClawLoadBalancer - Claw动态负载均衡器
======================================

A.2 Claw动态负载均衡：基于Claw历史响应时间调整路由权重

功能:
- 响应时间加权轮询
- 活跃请求计数
- 自适应权重调整
- 熔断保护

版本: v1.1.0
创建: 2026-04-24
"""

from __future__ import annotations

import time
import logging
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from collections import deque
from threading import Lock
from enum import Enum

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# 负载状态枚举
# ═══════════════════════════════════════════════════════════════

class LoadState(Enum):
    """负载状态"""
    HEALTHY = "healthy"      # 健康
    WARMING = "warming"       # 预热中（样本不足）
    HEAVY = "heavy"           # 负载较高
    OVERLOADED = "overloaded" # 过载（熔断）


# ═══════════════════════════════════════════════════════════════
# Claw负载指标
# ═══════════════════════════════════════════════════════════════

@dataclass
class ClawLoadMetrics:
    """Claw负载指标"""
    claw_name: str
    response_times: deque = field(default_factory=lambda: deque(maxlen=50))
    error_count: int = 0
    total_requests: int = 0
    successful_requests: int = 0
    active_requests: int = 0
    
    # 权重相关
    weight: float = 1.0
    avg_response_time: float = 0.0
    min_response_time: float = float('inf')
    max_response_time: float = 0.0
    p95_response_time: float = 0.0
    
    # 状态
    state: LoadState = LoadState.WARMING
    last_request_time: float = 0.0
    
    def _compute_stats(self) -> None:
        """计算统计指标"""
        if not self.response_times:
            self.avg_response_time = 0.0
            return
        
        times = list(self.response_times)
        self.avg_response_time = sum(times) / len(times)
        self.min_response_time = min(times)
        self.max_response_time = max(times)
        
        # P95
        sorted_times = sorted(times)
        idx = int(len(sorted_times) * 0.95)
        self.p95_response_time = sorted_times[min(idx, len(sorted_times) - 1)]

    def record_request_start(self) -> None:
        """记录请求开始"""
        self.active_requests += 1
        self.total_requests += 1
        self.last_request_time = time.time()

    def record_request_end(self, duration: float, success: bool = True) -> None:
        """记录请求结束"""
        self.active_requests = max(0, self.active_requests - 1)
        
        if success:
            self.successful_requests += 1
            self.response_times.append(duration)
        else:
            self.error_count += 1
        
        # 更新状态
        self._compute_stats()
        self._update_state()

    def _update_state(self) -> None:
        """更新负载状态"""
        # 样本不足
        if len(self.response_times) < 5:
            self.state = LoadState.WARMING
            return
        
        # 错误率过高
        if self.total_requests > 10:
            error_rate = self.error_count / self.total_requests
            if error_rate > 0.3:
                self.state = LoadState.OVERLOADED
                return
        
        # P95响应时间判断
        if self.p95_response_time > 30.0:  # >30秒
            self.state = LoadState.OVERLOADED
        elif self.p95_response_time > 10.0:  # >10秒
            self.state = LoadState.HEAVY
        else:
            self.state = LoadState.HEALTHY

    def get_weight(self) -> float:
        """获取当前权重"""
        if self.state == LoadState.OVERLOADED:
            return 0.0  # 熔断
        if self.state == LoadState.HEAVY:
            return 0.5
        if self.state == LoadState.WARMING:
            return 0.8
        
        # 健康状态：基于响应时间的自适应权重
        if self.avg_response_time > 0:
            # 响应越快，权重越高（最高2.0，最低0.5）
            baseline = 5.0  # 5秒为基准
            weight = baseline / max(self.avg_response_time, 0.5)
            return max(0.5, min(2.0, weight))
        
        return 1.0


# ═══════════════════════════════════════════════════════════════
# 动态负载均衡器
# ═══════════════════════════════════════════════════════════════

@dataclass
class LoadBalanceResult:
    """负载均衡结果"""
    selected_claw: str
    weight: float
    state: LoadState
    reason: str


class ClawLoadBalancer:
    """
    Claw动态负载均衡器。
    
    基于历史响应时间、自适应权重、活跃请求数进行智能路由。
    
    算法:
    1. 排除过载/熔断的Claw
    2. 计算权重（响应时间 + 活跃度）
    3. 加权随机选择
    
    用法:
        balancer = ClawLoadBalancer()
        balancer.register_claw("孔子")
        balancer.register_claw("孟子")
        
        result = balancer.select()
        balancer.record_start("孔子")
        # ... 执行任务 ...
        balancer.record_end("孔子", 2.5, success=True)
    """

    def __init__(self):
        self._metrics: Dict[str, ClawLoadMetrics] = {}
        self._lock = Lock()
        
        # 配置
        self._max_active_per_claw: int = 3
        self._circuit_breaker_threshold: int = 5
        self._recovery_timeout: float = 60.0  # 秒

    def register_claw(self, claw_name: str) -> None:
        """注册Claw"""
        with self._lock:
            if claw_name not in self._metrics:
                self._metrics[claw_name] = ClawLoadMetrics(claw_name=claw_name)
                logger.debug(f"[LoadBalancer] Registered: {claw_name}")

    def unregister_claw(self, claw_name: str) -> None:
        """注销Claw"""
        with self._lock:
            if claw_name in self._metrics:
                del self._metrics[claw_name]
                logger.debug(f"[LoadBalancer] Unregistered: {claw_name}")

    def select(
        self,
        candidates: List[str] = None,
        exclude_states: List[LoadState] = None,
    ) -> Optional[LoadBalanceResult]:
        """
        选择最佳Claw。
        
        Args:
            candidates: 候选Claw列表（None表示全部）
            exclude_states: 排除的状态
            
        Returns:
            LoadBalanceResult或None
        """
        if exclude_states is None:
            exclude_states = [LoadState.OVERLOADED]

        with self._lock:
            # 获取候选Claw
            if candidates:
                available = {
                    name: self._metrics[name]
                    for name in candidates
                    if name in self._metrics
                }
            else:
                available = self._metrics.copy()
            
            # 过滤状态
            if exclude_states:
                available = {
                    name: m for name, m in available.items()
                    if m.state not in exclude_states
                }
            
            # 过滤活跃度过高
            available = {
                name: m for name, m in available.items()
                if m.active_requests < self._max_active_per_claw
            }
            
            if not available:
                logger.warning("[LoadBalancer] No available claws")
                return None
            
            # 计算权重
            weights = []
            for name, metrics in available.items():
                w = metrics.get_weight()
                # 活跃请求惩罚
                if metrics.active_requests > 0:
                    w *= (1.0 - metrics.active_requests * 0.2)
                weights.append((name, max(0.1, w)))
            
            # 加权随机选择
            selected = self._weighted_random(weights)
            metrics = available[selected]
            
            return LoadBalanceResult(
                selected_claw=selected,
                weight=metrics.weight,
                state=metrics.state,
                reason=f"weight={metrics.weight:.2f}, active={metrics.active_requests}, state={metrics.state.value}",
            )

    def _weighted_random(self, weights: List[Tuple[str, float]]) -> str:
        """加权随机选择"""
        import random
        total = sum(w for _, w in weights)
        r = random.uniform(0, total)
        
        cumulative = 0
        for name, w in weights:
            cumulative += w
            if r <= cumulative:
                return name
        
        return weights[-1][0]

    def record_start(self, claw_name: str) -> bool:
        """记录请求开始"""
        with self._lock:
            if claw_name not in self._metrics:
                self.register_claw(claw_name)
            
            metrics = self._metrics[claw_name]
            metrics.record_request_start()
            return True

    def record_end(
        self,
        claw_name: str,
        duration: float,
        success: bool = True,
    ) -> None:
        """记录请求结束"""
        with self._lock:
            if claw_name not in self._metrics:
                logger.warning(f"[LoadBalancer] Unknown claw: {claw_name}")
                return
            
            self._metrics[claw_name].record_request_end(duration, success)

    def get_claw_status(self, claw_name: str) -> Optional[Dict]:
        """获取Claw状态"""
        with self._lock:
            if claw_name not in self._metrics:
                return None
            
            m = self._metrics[claw_name]
            return {
                "name": m.claw_name,
                "state": m.state.value,
                "weight": m.get_weight(),
                "active_requests": m.active_requests,
                "avg_response_time": m.avg_response_time,
                "p95_response_time": m.p95_response_time,
                "total_requests": m.total_requests,
                "success_rate": (
                    m.successful_requests / m.total_requests
                    if m.total_requests > 0 else 0.0
                ),
            }

    def get_all_status(self) -> Dict[str, Dict]:
        """获取所有Claw状态"""
        with self._lock:
            return {
                name: {
                    "state": m.state.value,
                    "weight": m.get_weight(),
                    "active": m.active_requests,
                    "avg_time": m.avg_response_time,
                }
                for name, m in self._metrics.items()
            }

    def reset_circuit(self, claw_name: str) -> bool:
        """重置熔断器"""
        with self._lock:
            if claw_name not in self._metrics:
                return False
            
            self._metrics[claw_name].state = LoadState.WARMING
            self._metrics[claw_name].error_count = 0
            return True

    def get_stats(self) -> Dict:
        """获取统计信息"""
        with self._lock:
            states = {s: 0 for s in LoadState}
            for m in self._metrics.values():
                states[m.state] += 1
            
            return {
                "total_claws": len(self._metrics),
                "states": {s.value: c for s, c in states.items()},
                "total_requests": sum(m.total_requests for m in self._metrics.values()),
            }
