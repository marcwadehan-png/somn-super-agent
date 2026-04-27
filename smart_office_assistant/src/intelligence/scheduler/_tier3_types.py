# -*- coding: utf-8 -*-
"""
三级神经网络调度器 - 类型定义模块
Tier-3 Neural Scheduler Types
=============================

包含所有类型定义:
- EngineTier: 引擎层级枚举
- TierSelection: 层级选择结果
- Tier3Query: 三级神经网络查询
- EngineOutput: 引擎输出
- Tier3Result: 三级调度结果

版本: v1.0
日期: 2026-04-06
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class EngineTier(Enum):
    """引擎层级"""
    P1 = "P1"  # 核心strategy层
    P2 = "P2"  # 交叉验证层
    P3 = "P3"  # 论证可行性层

@dataclass
class TierSelection:
    """层级选择结果"""
    tier: EngineTier
    engine_id: str
    match_score: float
    domains: List[str]
    reason: str = ""

@dataclass
class Tier3Query:
    """三级神经网络查询"""
    query_id: str
    query_text: str
    context: Dict[str, Any] = field(default_factory=dict)
    # 可选:强制包含/排除的引擎
    required_engines: List[str] = field(default_factory=list)
    excluded_engines: List[str] = field(default_factory=list)
    # 可选:强制包含/排除的层级
    required_tiers: List[str] = field(default_factory=list)
    # 调度配置
    p1_count: int = 6   # P1层引擎数量
    p3_count: int = 4   # P3层引擎数量
    p2_count: int = 4   # P2层引擎数量
    random_seed: Optional[int] = None  # 随机种子(可复现)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class EngineOutput:
    """引擎输出"""
    engine_id: str
    tier: str
    match_score: float
    execution_time: float
    raw_output: Any
    strategy_content: Optional[str] = None   # P1strategy内容
    论证_content: Optional[str] = None        # P3论证内容
    perspective_content: Optional[str] = None  # P2视角内容
    warnings: List[str] = field(default_factory=list)
    success: bool = True

@dataclass
class Tier3Result:
    """三级调度结果"""
    # 必需字段(前)
    query_id: str
    query_text: str
    success: bool
    fused_strategy: Dict[str, Any]  # P1strategyfusion
    feasibility_report: Dict[str, Any]  # P3可行性报告
    perspective_synthesis: Dict[str, Any]  # P2多元视角
    final_strategy: str
    decision_confidence: float
    tier_balance: float
    coverage: float
    synergy_score: float
    processing_time: float
    # 带默认值的字段(后)
    p1_outputs: List[EngineOutput] = field(default_factory=list)
    p3_outputs: List[EngineOutput] = field(default_factory=list)
    p2_outputs: List[EngineOutput] = field(default_factory=list)
    risk_warnings: List[str] = field(default_factory=list)
    key_insights: List[str] = field(default_factory=list)
    workflow_reference_id: str = ""
    strategy_combo: List[str] = field(default_factory=list)
    roi_trace: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
