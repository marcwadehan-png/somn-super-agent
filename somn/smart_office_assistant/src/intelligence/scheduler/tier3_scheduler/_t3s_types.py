# -*- coding: utf-8 -*-
"""
Tier3 调度器 - 类型定义模块
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum

class EngineTier(Enum):
    """引擎层级"""
    P1 = "P1"  # 核心策略层
    P2 = "P2"  # 交叉验证层
    P3 = "P3"  # 可行性论证层

@dataclass
class Tier3Query:
    """Tier3 查询"""
    query_id: str
    query_text: str
    context: Dict[str, Any] = field(default_factory=dict)
    p1_count: int = 3
    p2_count: int = 2
    p3_count: int = 2
    random_seed: int = 42
    excluded_engines: List[str] = field(default_factory=list)
    required_engines: List[str] = field(default_factory=list)

@dataclass
class TierSelection:
    """层级选择结果"""
    tier: EngineTier
    engine_id: str
    match_score: float
    domains: List[str]
    reason: str = ""

@dataclass
class EngineOutput:
    """引擎输出"""
    engine_id: str
    tier: str
    match_score: float
    execution_time: float
    raw_output: Dict[str, Any]
    perspective_content: str = ""
    strategy_content: str = ""
    论证_content: str = ""
    success: bool = True
    warnings: List[str] = field(default_factory=list)

@dataclass
class Tier3Result:
    """Tier3 调度结果"""
    query_id: str
    query_text: str
    success: bool
    fused_strategy: Dict[str, Any]
    feasibility_report: Dict[str, Any]
    perspective_synthesis: Dict[str, Any]
    final_strategy: str
    decision_confidence: float
    risk_warnings: List[str] = field(default_factory=list)
    key_insights: List[str] = field(default_factory=list)
    tier_balance: float = 0.0
    coverage: float = 0.0
    synergy_score: float = 0.0
    processing_time: float = 0.0
    workflow_reference_id: str = ""
    strategy_combo: List[str] = field(default_factory=list)
    roi_trace: Dict[str, Any] = field(default_factory=dict)
