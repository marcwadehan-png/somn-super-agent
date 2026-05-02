"""
__all__ = [
    'export_result',
    'get_capabilities',
    'health_check',
]

Somn 工具方法 - 从 somn.py 拆分
包含 export_result, get_capabilities, health_check, main
"""

import json
import yaml
from datetime import datetime

def export_result(self, result, format: str = "yaml") -> str:
    """导出分析结果"""
    data = {
        "request_id": result.request_id,
        "request_type": result.request_type,
        "status": result.status,
        "execution_time": f"{result.execution_time:.2f}s",
        "created_at": result.created_at,
        "data": result.data,
        "next_steps": result.next_steps
    }

    if format == "yaml":
        return yaml.dump(data, allow_unicode=True, default_flow_style=False)
    else:
        return json.dumps(data, ensure_ascii=False, indent=2)

def get_capabilities(self) -> dict:
    """get能力清单"""
    return {
        "name": "Somn - 超级智能体",
        "version": "1.0.0",
        "layers": {
            "layer1_foundation": {
                "description": "基础层 - 工具链与模型服务",
                "components": ["ToolRegistry", "LLMService"]
            },
            "layer2_data": {
                "description": "数据层 - 知识图谱与数据收集",
                "components": ["KnowledgeGraphEngine", "WebSearchEngine", "NeuralMemorySystem"]
            },
            "layer3_intelligence": {
                "description": "智能层 - ML与自主学习",
                "components": ["MLEngine", "LearningEngine", "ReasoningEngine"]
            },
            "layer4_capability": {
                "description": "能力层 - 增长核心能力",
                "components": ["DemandAnalyzer", "UserJourneyMapper", "FunnelOptimizer"]
            },
            "layer5_application": {
                "description": "应用层 - 行业解决方案",
                "components": ["GrowthStrategyEngine", "IndustryAdapter"]
            }
        },
        "analysis_types": [
            {
                "type": "growth_plan",
                "name": "增长计划generate",
                "description": "基于业务诊断generate完整增长strategy和路线图"
            },
            {
                "type": "demand_analysis",
                "name": "需求分析",
                "description": "六步需求分析流程,recognize用户真实需求"
            },
            {
                "type": "funnel_analysis",
                "name": "漏斗分析",
                "description": "量化转化漏斗,recognize瓶颈和优化机会"
            },
            {
                "type": "journey_mapping",
                "name": "用户旅程mapping",
                "description": "绘制用户旅程,发现摩擦点和惊喜时刻"
            },
            {
                "type": "business_diagnosis",
                "name": "业务诊断",
                "description": "全面诊断业务健康状况,recognize增长机会"
            }
        ],
        "supported_industries": [
            "saas_b2b", "saas_b2c", "ecommerce", "fintech",
            "healthcare", "education", "marketplace", "content_media"
        ],
        "supported_solutions": [
            "private_domain", "membership", "digital_operation",
            "digital_transformation", "integrated_marketing",
            "xiaohongshu", "douyin", "ai_growth", "o2o",
            "new_retail", "cross_border", "live_commerce",
            "kol_marketing", "brand_building", "data_driven"
        ]
    }

def health_check(self) -> dict:
    """系统健康检查"""
    checks = {
        "knowledge_graph": self.kg_engine is not None,
        "concept_manager": self.concept_manager is not None,
        "industry_knowledge": self.industry_knowledge is not None,
        "web_search": self.web_search is not None,
        "data_collector": self.data_collector is not None,
        "memory_system": self.memory_system is not None,
        "user_classifier": self.user_classifier is not None,
        "time_series_forecaster": self.time_series_forecaster is not None,
        "demand_analyzer": self.demand_analyzer is not None,
        "journey_mapper": self.journey_mapper is not None,
        "funnel_optimizer": self.funnel_optimizer is not None,
        "growth_engine": self.growth_engine is not None,
        "industry_adapter": self.industry_adapter is not None,
        "solution_library": self.solution_library is not None,
        "reasoning_engine": getattr(self, 'reasoning_engine', None) is not None,
        "solution_engine_v2": getattr(self, 'solution_engine_v2', None) is not None,
    }

    all_healthy = all(checks.values())

    return {
        "status": "healthy" if all_healthy else "degraded",
        "timestamp": datetime.now().isoformat(),
        "checks": checks,
        "healthy_components": sum(checks.values()),
        "total_components": len(checks),
        "solution_count": len(self.solution_library.templates) if self.solution_library else 0
    }
