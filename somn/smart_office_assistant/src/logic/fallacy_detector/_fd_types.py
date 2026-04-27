"""
谬误检测器类型定义
"""

from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class FallacyCategory(Enum):
    """谬误类别"""
    FORMAL = "形式谬误"
    INFORMAL = "非形式谬误"
    AMBIGUITY = "歧义谬误"
    RELEVANCE = "相关性谬误"
    PRESUMPTION = "预设谬误"
    CAUSATION = "因果谬误"
    STRATEGIC = "战略咨询谬误"  # v5.1 增长咨询专用

@dataclass
class FallacyDetection:
    """谬误检测结果"""
    fallacy_name: str                    # 谬误名称
    category: FallacyCategory            # 类别
    description: str                    # 描述
    severity: str                        # 严重程度 (critical/major/minor)
    confidence: float                   # 置信度 (0.0-1.0)
    suggestion: str                     # 改进建议
    detected_at: datetime                # 检测时间
