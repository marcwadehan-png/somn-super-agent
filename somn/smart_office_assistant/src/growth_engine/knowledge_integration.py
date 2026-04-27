"""
__all__ = [
    'export_enhanced_knowledge_base',
    'generate_full_integration_report',
    'generate_solution_differentiation',
    'integrate_category_knowledge',
    'quick_integrate',
]

知识库整合模块
Knowledge Integration - 将服务商学习成果整合到解决方案能力

功能:
1. 能力mapping - 将服务商能力mapping到自身解决方案
2. 最佳实践注入 - 将学习到的最佳实践融入方案设计
3. 差异化定位 - 基于竞品分析确定自身差异化优势
4. 持续进化 - 定期更新知识库
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json

from .provider_intelligence_engine import (
    ProviderIntelligenceEngine, ProviderCategory, CapabilityType, AdvantageLevel
)
from .continuous_learning_plan import ContinuousLearningPlan, LearningStatus

@dataclass
class CapabilityMapping:
    """能力mapping"""
    source_provider: str                    # 来源服务商
    source_capability: str                  # 来源能力
    target_solution: str                    # 目标解决方案
    integration_approach: str               # 整合方式
    priority: int = 1                       # 优先级
    learned_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class SolutionEnhancement:
    """解决方案增强"""
    solution_type: str
    enhancement_areas: List[Dict]           # 增强领域
    best_practices_adopted: List[str]       # 采纳的最佳实践
    differentiation_strategy: str           # 差异化strategy
    confidence_score: float = 0.0

class KnowledgeIntegrator:
    """知识整合器"""
    
    def __init__(self):
        self.intelligence_engine = ProviderIntelligenceEngine()
        self.learning_plan = ContinuousLearningPlan()
        self.capability_mappings: List[CapabilityMapping] = []
        self.enhancement_history: List[Dict] = []
    
    def integrate_category_knowledge(self, category: ProviderCategory) -> Dict[str, Any]:
        """
        整合单个赛道的学习成果
        
        流程:
        1. 提取赛道最佳实践
        2. recognize可学习的能力
        3. generate解决方案增强建议
        4. 更新能力mapping
        """
        # 1. 提取最佳实践
        best_practices = self.intelligence_engine.extract_best_practices(category)
        
        # 2. generate增强建议
        enhancement = self.intelligence_engine.generate_solution_enhancement(category)
        
        # 3. 创建能力mapping
        mappings = self._create_capability_mappings(category, best_practices)
        self.capability_mappings.extend(mappings)
        
        # 4. 整合结果
        integration_result = {
            "category": category.value,
            "integrated_at": datetime.now().isoformat(),
            "best_practices": best_practices,
            "enhancement_recommendations": enhancement,
            "capability_mappings": [
                {
                    "source": m.source_provider,
                    "capability": m.source_capability,
                    "target": m.target_solution
                }
                for m in mappings
            ],
            "key_takeaways": self._extract_key_takeaways(best_practices)
        }
        
        # 5. 记录历史
        self.enhancement_history.append(integration_result)
        
        return integration_result
    
    def _create_capability_mappings(self, category: ProviderCategory, 
                                    best_practices: Dict) -> List[CapabilityMapping]:
        """创建能力mapping"""
        mappings = []
        
        # mapping技术能力
        tech_best = best_practices.get("technology_best", {})
        if tech_best and tech_best.get("score", 0) >= 7:
            mappings.append(CapabilityMapping(
                source_provider=tech_best["provider"],
                source_capability="技术能力",
                target_solution=self._map_category_to_solution(category),
                integration_approach="参考技术架构设计",
                priority=1
            ))
        
        # mapping产品能力
        product_best = best_practices.get("product_best", {})
        if product_best and product_best.get("score", 0) >= 7:
            mappings.append(CapabilityMapping(
                source_provider=product_best["provider"],
                source_capability="产品能力",
                target_solution=self._map_category_to_solution(category),
                integration_approach="借鉴产品功能设计",
                priority=2
            ))
        
        # mapping服务能力
        service_best = best_practices.get("service_best", {})
        if service_best and service_best.get("score", 0) >= 7:
            mappings.append(CapabilityMapping(
                source_provider=service_best["provider"],
                source_capability="服务能力",
                target_solution=self._map_category_to_solution(category),
                integration_approach="学习服务模式",
                priority=3
            ))
        
        return mappings
    
    def _map_category_to_solution(self, category: ProviderCategory) -> str:
        """将赛道mapping到解决方案类型"""
        mapping = {
            ProviderCategory.MEMBERSHIP: "private_domain",
            ProviderCategory.DIGITAL_OPERATION: "digital_operation",
            ProviderCategory.DIGITAL_TRANSFORMATION: "digital_transformation",
            ProviderCategory.INTEGRATED_MARKETING: "integrated_marketing",
            ProviderCategory.XIAOHONGSHU: "xiaohongshu",
            ProviderCategory.DOUYIN: "douyin",
            ProviderCategory.AI_GROWTH: "ai_growth",
            ProviderCategory.O2O: "o2o_operation",
            ProviderCategory.NEW_RETAIL: "new_retail",
            ProviderCategory.CROSS_BORDER: "cross_border",
            ProviderCategory.LIVE_COMMERCE: "live_commerce",
            ProviderCategory.KOL_MARKETING: "kol_marketing",
            ProviderCategory.BRAND_BUILDING: "brand_building",
            ProviderCategory.DATA_DRIVEN: "data_driven",
            ProviderCategory.SOFTWARE_SOLUTION: "crm"
        }
        return mapping.get(category, "generic")
    
    def _extract_key_takeaways(self, best_practices: Dict) -> List[str]:
        """提取关键要点"""
        takeaways = []
        
        # 技术要点
        tech = best_practices.get("technology_best", {})
        if tech and tech.get("provider"):
            takeaways.append(
                f"技术标杆: {tech['provider']} - "
                f"重点学习其技术架构和创新能力"
            )
        
        # synthesize要点
        overall = best_practices.get("overall_best", {})
        if overall and overall.get("provider"):
            takeaways.append(
                f"synthesize标杆: {overall['provider']} - "
                f"学习其整体解决方案设计思路"
            )
        
        return takeaways
    
    def generate_solution_differentiation(self, solution_type: str,
                                          category: ProviderCategory) -> Dict[str, Any]:
        """
        generate解决方案差异化strategy
        
        基于竞品分析,确定自身独特定位
        """
        # get该赛道的所有服务商
        category_intel = self.intelligence_engine.intelligence_db.get(category)
        if not category_intel:
            return {"error": "赛道数据不存在"}
        
        # 分析竞品的共同特点(红海)
        common_capabilities = self._analyze_common_capabilities(category_intel)
        
        # 分析竞品的薄弱环节(机会)
        weak_areas = self._identify_weak_areas(category_intel)
        
        # generate差异化strategy
        differentiation = {
            "solution_type": solution_type,
            "category": category.value,
            "generated_at": datetime.now().isoformat(),
            "market_analysis": {
                "total_competitors": len(category_intel.providers),
                "common_capabilities": common_capabilities[:5],
                "saturated_areas": self._identify_saturated_areas(category_intel),
            },
            "opportunity_areas": weak_areas[:5],
            "differentiation_strategy": self._craft_differentiation_strategy(
                solution_type, common_capabilities, weak_areas
            ),
            "positioning_recommendation": self._generate_positioning(
                category_intel, weak_areas
            )
        }
        
        return differentiation
    
    def _analyze_common_capabilities(self, category_intel) -> List[str]:
        """分析竞品的共同能力(红海区域)"""
        capability_count = {}
        
        for profile in category_intel.providers.values():
            for cap in profile.capabilities.values():
                if cap.score >= 6:  # 只统计强势能力
                    cap_name = cap.name
                    capability_count[cap_name] = capability_count.get(cap_name, 0) + 1
        
        # 按出现频率排序
        sorted_caps = sorted(capability_count.items(), key=lambda x: x[1], reverse=True)
        return [cap for cap, count in sorted_caps if count >= 3]
    
    def _identify_weak_areas(self, category_intel) -> List[str]:
        """recognize竞品的薄弱环节(机会)"""
        weak_areas = []
        
        # 统计各能力类型的平均得分
        type_scores = {}
        type_counts = {}
        
        for profile in category_intel.providers.values():
            for cap_type, cap in profile.capabilities.items():
                type_name = cap_type.value
                if type_name not in type_scores:
                    type_scores[type_name] = 0
                    type_counts[type_name] = 0
                type_scores[type_name] += cap.score
                type_counts[type_name] += 1
        
        # 找出平均分较低的能力类型
        for type_name, total_score in type_scores.items():
            avg_score = total_score / max(type_counts[type_name], 1)
            if avg_score < 5:
                weak_areas.append(f"{type_name}(平均分{avg_score:.1f})")
        
        return weak_areas
    
    def _identify_saturated_areas(self, category_intel) -> List[str]:
        """recognize过度竞争的区域"""
        saturated = []
        
        # 统计高评分能力的集中度
        high_score_providers = {}
        
        for profile in category_intel.providers.values():
            for cap in profile.capabilities.values():
                if cap.score >= 7:
                    cap_name = cap.name
                    if cap_name not in high_score_providers:
                        high_score_providers[cap_name] = []
                    high_score_providers[cap_name].append(profile.name)
        
        # 找出超过5家都擅长的能力
        for cap_name, providers in high_score_providers.items():
            if len(providers) >= 5:
                saturated.append(f"{cap_name}({len(providers)}家擅长)")
        
        return saturated
    
    def _craft_differentiation_strategy(self, solution_type: str,
                                        common_capabilities: List[str],
                                        weak_areas: List[str]) -> str:
        """制定差异化strategy"""
        if weak_areas:
            return (
                f"避开红海竞争({', '.join(common_capabilities[:2])}),"
                f"重点突破薄弱环节: {', '.join(weak_areas[:2])}"
            )
        else:
            return (
                f"在主流能力({', '.join(common_capabilities[:2])})基础上,"
                f"强化服务体验和行业深度"
            )
    
    def _generate_positioning(self, category_intel, weak_areas: List[str]) -> str:
        """generate定位建议"""
        if not weak_areas:
            return "synthesize型解决方案提供商"
        
        # 找出最大的薄弱环节
        main_weakness = weak_areas[0].split("(")[0]
        
        return f"专注{main_weakness}的差异化解决方案提供商"
    
    def export_enhanced_knowledge_base(self, output_path: str):
        """导出增强后的知识库"""
        export_data = {
            "export_time": datetime.now().isoformat(),
            "integration_summary": {
                "total_mappings": len(self.capability_mappings),
                "total_enhancements": len(self.enhancement_history),
                "categories_covered": list(set(
                    e["category"] for e in self.enhancement_history
                ))
            },
            "capability_mappings": [
                {
                    "source_provider": m.source_provider,
                    "source_capability": m.source_capability,
                    "target_solution": m.target_solution,
                    "integration_approach": m.integration_approach,
                    "priority": m.priority
                }
                for m in self.capability_mappings
            ],
            "enhancement_history": self.enhancement_history
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        return export_data

# ==================== 便捷使用接口 ====================

def quick_integrate(category: str) -> Dict[str, Any]:
    """
    快速整合单个赛道的知识
    
    示例:
        result = quick_integrate("会员体系")
    """
    integrator = KnowledgeIntegrator()
    
    # 转换分类
    category_map = {c.value: c for c in ProviderCategory}
    cat_enum = category_map.get(category, ProviderCategory.MEMBERSHIP)
    
    # 整合知识
    integration = integrator.integrate_category_knowledge(cat_enum)
    
    # generate差异化strategy
    solution_type = integrator._map_category_to_solution(cat_enum)
    differentiation = integrator.generate_solution_differentiation(solution_type, cat_enum)
    
    return {
        "category": integration["category"],
        "key_takeaways": integration["key_takeaways"],
        "capability_mappings_count": len(integration["capability_mappings"]),
        "differentiation_strategy": differentiation["differentiation_strategy"],
        "positioning": differentiation["positioning_recommendation"]
    }

def generate_full_integration_report() -> Dict[str, Any]:
    """generate完整的知识整合报告"""
    integrator = KnowledgeIntegrator()
    
    report = {
        "generated_at": datetime.now().isoformat(),
        "categories_integrated": [],
        "total_mappings": 0,
        "key_insights": []
    }
    
    for category in ProviderCategory:
        integration = integrator.integrate_category_knowledge(category)
        report["categories_integrated"].append(category.value)
        report["total_mappings"] += len(integration["capability_mappings"])
        report["key_insights"].extend(integration["key_takeaways"])
    
    return report

# ==================== 测试示例 ====================

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
