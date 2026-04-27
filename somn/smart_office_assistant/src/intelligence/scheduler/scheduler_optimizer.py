# -*- coding: utf-8 -*-
"""
__all__ = [
    'adjust_weight',
    'check_optimization_status',
    'check_quality_targets',
    'enhance_engine_domains',
    'expand_keywords',
    'generate_optimization_report',
    'get_average_performance',
    'get_coverage_trend',
    'get_engine_weights',
    'get_enhanced_weight',
    'get_optimization_report',
    'get_optimizer',
    'record_metrics',
    'record_performance',
    'record_scheduler_metrics',
    'to_dict',
]

调度器优化器 v1.0
Scheduler Optimizer
===================

三级神经网络调度器优化模块:
- 覆盖率提升: 88% → 95%
- 关键词语义扩展
- 引擎域标签增强
- 自适应权重调整
- 质量监控体系

版本: v1.0
日期: 2026-04-03
"""

from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
import logging
import json
from collections import defaultdict

logger = logging.getLogger(__name__)

# ============================================================
# 优化strategy1: 关键词语义扩展
# ============================================================

DOMAIN_KEYWORD_EXPANSION: Dict[str, List[str]] = {
    # === 用户增长相关 ===
    "用户流失": ["churn", "attrition", "retention_crisis", "user_loss", "stickiness"],
    "获客成本": ["cac", "acquisition_cost", "customer_acquisition", "cpa", "user_acquisition"],
    "转化率": ["conversion", "conversion_rate", "funnel_optimization", "funnel", "landing_page"],
    "复购": ["repurchase", "repeat_purchase", "retention", "loyalty", "ltv", "clv"],
    "留存": ["retention", "stickiness", "engagement", "dau", "mau", "cohort"],
    "私域": ["private_domain", "private_traffic", "community", "crm", "membership", "wecom"],
    "增长": ["growth", "scaling", "expansion", "user_acquisition", "growth_hacking", "growth_loop"],
    "裂变": ["viral", "referral", "growth_loop", "network_effect", "word_of_mouth"],
    
    # === 产品运营相关 ===
    "产品": ["product", "product_management", "feature", "roadmap", "mvp", "pmf"],
    "运营": ["operations", "user_operations", "content", "activity", "community_ops"],
    "数据": ["data", "analytics", "metrics", "kpi", "dashboard", "ab_test"],
    "优化": ["optimization", "improvement", "iteration", "fine_tuning", "tuning"],
    
    # === 商业模式相关 ===
    "变现": ["monetization", "revenue", "pricing", "business_model", "unit_economics"],
    "盈利": ["profitability", "revenue", "margin", "unit_economics", "roi"],
    "商业模式": ["business_model", "revenue_model", "monetization", "unit_economics"],
    "订阅": ["subscription", "saas", "recurring_revenue", "mrr", "arr"],
    "平台": ["platform", "marketplace", "network_effect", "two_sided_market"],
    
    # === 市场竞争相关 ===
    "护城河": ["moat", "competitive_advantage", "barrier", "defensibility", "sustainable"],
    "壁垒": ["barrier", "moat", "defensibility", "entry_barrier", "switching_cost"],
    "差异化": ["differentiation", "positioning", "unique_value", "usp", "competitive_advantage"],
    "市场份额": ["market_share", "penetration", "market_position", "competitive_landscape"],
    
    # === 组织团队相关 ===
    "执行力": ["execution", "implementation", "delivery", "operational_excellence", "speed"],
    "协同": ["collaboration", "coordination", "alignment", "cross_functional", "teamwork"],
    "文化": ["culture", "values", "mission", "vision", "organizational_culture"],
    "招聘": ["hiring", "recruiting", "talent_acquisition", "onboarding", "retention"],
    
    # === 技术工程相关 ===
    "技术债": ["tech_debt", "technical_debt", "refactoring", "legacy", "modernization"],
    "架构": ["architecture", "system_design", "scalability", "reliability", "performance"],
    "敏捷": ["agile", "scrum", "kanban", "sprint", "iteration", "continuous_delivery"],
    "中台": ["platform", "shared_service", "reusable", "infrastructure", "enablement"],
}

# ============================================================
# 优化strategy2: 引擎域标签增强
# ============================================================

ENGINE_DOMAIN_ENHANCEMENT: Dict[str, Dict[str, Any]] = {
    "SOCIAL_SCIENCE": {
        "add_domains": [
            "user_behavior", "consumer_insight", "market_research",
            "growth_hacking", "product_led_growth", "community_led_growth"
        ],
        "weight_adjustment": 0.95,  # 提升至1.0
    },
    "POSITIONING": {
        "add_domains": [
            "brand_strategy", "market_entry", "differentiation",
            "competitive_positioning", "category_creation"
        ],
        "weight_adjustment": 0.95,  # 提升至0.95
    },
    "MARKETING": {
        "add_domains": [
            "growth_marketing", "performance_marketing", "content_marketing",
            "viral_marketing", "influencer_marketing"
        ],
        "weight_adjustment": 0.95,
    },
    "STRATEGY": {
        "add_domains": [
            "business_model", "platform_strategy", "ecosystem_strategy",
            "international_expansion", "diversification"
        ],
        "weight_adjustment": 1.0,
    },
    "GROWTH": {
        "add_domains": [
            "growth_loop", "growth_hacking", "product_led_growth",
            "viral_growth", "network_effect"
        ],
        "weight_adjustment": 0.9,
    },
    "BEHAVIOR": {
        "add_domains": [
            "user_engagement", "habit_formation", "behavioral_design",
            "gamification", "nudge_theory"
        ],
        "weight_adjustment": 0.9,
    },
}

# ============================================================
# 优化strategy3: 质量metrics监控体系
# ============================================================

@dataclass
class QualityMetrics:
    """质量metrics数据类"""
    coverage_rate: float = 0.0  # 覆盖率
    response_time_ms: float = 0.0  # 响应时间(毫秒)
    domain_diversity: int = 0  # 域多样性
    tier_balance: Dict[str, int] = field(default_factory=dict)  # 层级平衡
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "coverage_rate": self.coverage_rate,
            "response_time_ms": self.response_time_ms,
            "domain_diversity": self.domain_diversity,
            "tier_balance": self.tier_balance,
            "timestamp": self.timestamp,
        }

QUALITY_TARGETS = {
    "coverage_rate": {
        "target": 0.95,  # 95%
        "current": 0.88,  # 当前88%
        "measurement": "问题域匹配引擎数/总引擎数",
        "priority": "高"
    },
    "response_time": {
        "target": 3000,  # 3秒
        "current": None,
        "measurement": "端到端调度耗时(ms)",
        "priority": "中"
    },
    "domain_diversity": {
        "target": 8,  # 至少8个不同域
        "current": None,
        "measurement": "单次调度覆盖的域种类数",
        "priority": "中"
    },
    "tier_balance": {
        "target": {"P1": 6, "P3": 4, "P2": 4},
        "current": None,
        "measurement": "每层实际激活引擎数",
        "priority": "高"
    }
}

# ============================================================
# 优化strategy4: 自适应权重调整
# ============================================================

@dataclass
class AdaptiveWeightConfig:
    """自适应权重配置"""
    feedback_driven: bool = True  # 基于用户反馈调整
    performance_based: bool = True  # 基于历史表现调整
    context_aware: bool = True  # 基于上下文动态调整
    learning_rate: float = 0.1  # 学习率
    min_weight: float = 0.5  # 最小权重
    max_weight: float = 1.0  # 最大权重

class AdaptiveWeightManager:
    """自适应权重管理器"""
    
    def __init__(self, config: Optional[AdaptiveWeightConfig] = None):
        self.config = config or AdaptiveWeightConfig()
        self.engine_performance: Dict[str, List[float]] = defaultdict(list)
        self.engine_weights: Dict[str, float] = {}
        
    def record_performance(self, engine_id: str, score: float):
        """记录引擎表现"""
        self.engine_performance[engine_id].append(score)
        # 只保留最近100条记录
        if len(self.engine_performance[engine_id]) > 100:
            self.engine_performance[engine_id] = self.engine_performance[engine_id][-100:]
    
    def get_average_performance(self, engine_id: str) -> float:
        """get引擎平均表现"""
        scores = self.engine_performance.get(engine_id, [])
        if not scores:
            return 0.5
        return sum(scores) / len(scores)
    
    def adjust_weight(self, engine_id: str, base_weight: float) -> float:
        """调整引擎权重"""
        if not self.config.performance_based:
            return base_weight
        
        avg_perf = self.get_average_performance(engine_id)
        # 表现好的引擎权重提升,表现差的降低
        adjustment = (avg_perf - 0.5) * self.config.learning_rate
        new_weight = base_weight + adjustment
        
        # 限制在合理范围内
        new_weight = max(self.config.min_weight, min(self.config.max_weight, new_weight))
        self.engine_weights[engine_id] = new_weight
        
        return new_weight
    
    def get_engine_weights(self) -> Dict[str, float]:
        """get所有引擎权重"""
        return self.engine_weights.copy()

# ============================================================
# 优化器主类
# ============================================================

class SchedulerOptimizer:
    """调度器优化器"""
    
    def __init__(self):
        self.expansion_keywords = DOMAIN_KEYWORD_EXPANSION
        self.engine_enhancement = ENGINE_DOMAIN_ENHANCEMENT
        self.quality_targets = QUALITY_TARGETS
        self.weight_manager = AdaptiveWeightManager()
        self.metrics_history: List[QualityMetrics] = []
        
    def expand_keywords(self, keywords: List[str]) -> List[str]:
        """
        扩展关键词
        
        Args:
            keywords: 原始关键词列表
            
        Returns:
            扩展后的关键词列表
        """
        expanded = set(keywords)
        
        for keyword in keywords:
            if keyword in self.expansion_keywords:
                expanded.update(self.expansion_keywords[keyword])
        
        return list(expanded)
    
    def enhance_engine_domains(self, engine_id: str, base_domains: List[str]) -> List[str]:
        """
        增强引擎域标签
        
        Args:
            engine_id: 引擎ID
            base_domains: 基础域列表
            
        Returns:
            增强后的域列表
        """
        enhanced = list(base_domains)
        
        if engine_id in self.engine_enhancement:
            enhancement = self.engine_enhancement[engine_id]
            if "add_domains" in enhancement:
                enhanced.extend(enhancement["add_domains"])
        
        return list(set(enhanced))  # 去重
    
    def get_enhanced_weight(self, engine_id: str, base_weight: float) -> float:
        """
        get增强后的权重
        
        Args:
            engine_id: 引擎ID
            base_weight: 基础权重
            
        Returns:
            增强后的权重
        """
        if engine_id in self.engine_enhancement:
            enhancement = self.engine_enhancement[engine_id]
            if "weight_adjustment" in enhancement:
                return enhancement["weight_adjustment"]
        
        # 应用自适应权重调整
        return self.weight_manager.adjust_weight(engine_id, base_weight)
    
    def record_metrics(self, metrics: QualityMetrics):
        """记录质量metrics"""
        self.metrics_history.append(metrics)
        
        # 只保留最近1000条记录
        if len(self.metrics_history) > 1000:
            self.metrics_history = self.metrics_history[-1000:]
    
    def get_coverage_trend(self) -> List[float]:
        """get覆盖率趋势"""
        return [m.coverage_rate for m in self.metrics_history]
    
    def check_quality_targets(self) -> Dict[str, Any]:
        """检查质量目标达成情况"""
        if not self.metrics_history:
            return {"status": "no_data", "details": {}}
        
        latest = self.metrics_history[-1]
        results = {}
        
        # 检查覆盖率
        coverage_target = self.quality_targets["coverage_rate"]["target"]
        coverage_status = "achieved" if latest.coverage_rate >= coverage_target else "pending"
        results["coverage_rate"] = {
            "current": latest.coverage_rate,
            "target": coverage_target,
            "status": coverage_status
        }
        
        # 检查响应时间
        time_target = self.quality_targets["response_time"]["target"]
        time_status = "achieved" if latest.response_time_ms <= time_target else "pending"
        results["response_time"] = {
            "current": latest.response_time_ms,
            "target": time_target,
            "status": time_status
        }
        
        # 检查域多样性
        diversity_target = self.quality_targets["domain_diversity"]["target"]
        diversity_status = "achieved" if latest.domain_diversity >= diversity_target else "pending"
        results["domain_diversity"] = {
            "current": latest.domain_diversity,
            "target": diversity_target,
            "status": diversity_status
        }
        
        overall_status = "achieved" if all(
            r["status"] == "achieved" for r in results.values()
        ) else "pending"
        
        return {
            "status": overall_status,
            "details": results
        }
    
    def generate_optimization_report(self) -> Dict[str, Any]:
        """generate优化报告"""
        coverage_trend = self.get_coverage_trend()
        quality_check = self.check_quality_targets()
        
        return {
            "report_type": "scheduler_optimization",
            "timestamp": datetime.now().isoformat(),
            "coverage": {
                "current": coverage_trend[-1] if coverage_trend else 0,
                "trend": coverage_trend[-10:] if len(coverage_trend) >= 10 else coverage_trend,
                "target": self.quality_targets["coverage_rate"]["target"],
                "improvement_needed": self.quality_targets["coverage_rate"]["target"] - (coverage_trend[-1] if coverage_trend else 0)
            },
            "quality_status": quality_check,
            "engine_weights": self.weight_manager.get_engine_weights(),
            "recommendations": self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> List[str]:
        """generate优化建议"""
        recommendations = []
        quality_check = self.check_quality_targets()
        
        if quality_check["status"] != "achieved":
            for metric, details in quality_check["details"].items():
                if details["status"] == "pending":
                    if metric == "coverage_rate":
                        recommendations.append(
                            f"覆盖率未达标: 当前{details['current']:.1%}, "
                            f"目标{details['target']:.1%}. 建议: 扩展关键词mapping,增加引擎域标签"
                        )
                    elif metric == "response_time":
                        recommendations.append(
                            f"响应时间超标: 当前{details['current']:.0f}ms, "
                            f"目标{details['target']:.0f}ms. 建议: 优化引擎加载,启用缓存"
                        )
                    elif metric == "domain_diversity":
                        recommendations.append(
                            f"域多样性不足: 当前{details['current']}, "
                            f"目标{details['target']}. 建议: 增加跨域引擎匹配"
                        )
        else:
            recommendations.append("所有质量目标已达成,建议持续监控并收集用户反馈")
        
        return recommendations

# ============================================================
# 便捷函数
# ============================================================

_optimizer_instance: Optional[SchedulerOptimizer] = None

def get_optimizer() -> SchedulerOptimizer:
    """get优化器实例(单例模式)"""
    global _optimizer_instance
    if _optimizer_instance is None:
        _optimizer_instance = SchedulerOptimizer()
    return _optimizer_instance

def expand_keywords(keywords: List[str]) -> List[str]:
    """便捷函数:扩展关键词"""
    return get_optimizer().expand_keywords(keywords)

def record_scheduler_metrics(
    coverage_rate: float,
    response_time_ms: float,
    domain_diversity: int,
    tier_balance: Dict[str, int]
):
    """便捷函数:记录调度器metrics"""
    metrics = QualityMetrics(
        coverage_rate=coverage_rate,
        response_time_ms=response_time_ms,
        domain_diversity=domain_diversity,
        tier_balance=tier_balance
    )
    get_optimizer().record_metrics(metrics)

def check_optimization_status() -> Dict[str, Any]:
    """便捷函数:检查优化状态"""
    return get_optimizer().check_quality_targets()

def get_optimization_report() -> Dict[str, Any]:
    """便捷函数:get优化报告"""
    return get_optimizer().generate_optimization_report()

# ============================================================
# 测试
# ============================================================

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
