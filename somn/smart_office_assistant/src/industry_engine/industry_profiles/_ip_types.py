"""
行业画像类型定义
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class IndustryType(Enum):
    """扩展行业类型"""
    # 原有行业
    SAAS_B2B = "saas_b2b"
    SAAS_B2C = "saas_b2c"
    ECOMMERCE = "ecommerce"
    FINTECH = "fintech"
    
    # 新增行业 - Month 1
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    REAL_ESTATE = "real_estate"
    TRAVEL = "travel"
    FOOD_BEVERAGE = "food_beverage"
    
    # 新增行业 - Month 2
    AI_TECH = "ai_tech"
    NEW_ENERGY = "new_energy"
    LUXURY = "luxury"
    SPORTS_FITNESS = "sports_fitness"
    PET = "pet"
    
    # 新增行业 - Month 3 (v2.1)
    CONTENT_GAMING = "content_gaming"  # 内容媒体/游戏
    LOCAL_LIFE = "local_life"           # 本地生活（外卖、到店、餐饮）

class BusinessModel(Enum):
    """商业模式"""
    SUBSCRIPTION = "subscription"
    TRANSACTION = "transaction"
    ADVERTISING = "advertising"
    FREEMIUM = "freemium"
    ENTERPRISE = "enterprise"
    COMMISSION = "commission"
    HYBRID = "hybrid"

@dataclass
class IndustryProfile:
    """行业画像"""
    industry_type: IndustryType
    name: str
    name_en: str
    description: str
    
    # 子类型
    sub_types: List[str] = field(default_factory=list)
    
    # 商业模式
    business_models: List[BusinessModel] = field(default_factory=list)
    
    # 关键characteristics
    key_characteristics: List[str] = field(default_factory=list)
    
    # 增长驱动因素
    growth_drivers: List[str] = field(default_factory=list)
    
    # 关键metrics
    key_metrics: List[str] = field(default_factory=list)
    
    # 行业基准
    benchmarks: Dict[str, str] = field(default_factory=dict)
    
    # 典型挑战
    typical_challenges: List[str] = field(default_factory=list)
    
    # 最佳实践
    best_practices: List[str] = field(default_factory=list)
    
    # 行业标签
    tags: List[str] = field(default_factory=list)
    
    # 特殊属性
    special_attributes: Dict[str, Any] = field(default_factory=dict)
