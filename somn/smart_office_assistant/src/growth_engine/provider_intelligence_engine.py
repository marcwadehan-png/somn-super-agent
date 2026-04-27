"""
__all__ = [
    'batch_learn_providers',
    'export_knowledge_base',
    'extract_best_practices',
    'generate_solution_enhancement',
    'get_core_differentiators',
    'get_leaderboard',
    'get_top_capabilities',
    'learn_provider',
    'quick_learn',
]

服务商智能学习引擎
Provider Intelligence Engine - 持续学习各赛道头部服务商能力优势

核心能力:
1. 多源数据采集 - 聚合官网,案例,评价等多维度信息
2. 智能分析引擎 - recognize服务商核心优势与差异化能力
3. 择优提炼系统 - 基于逻辑judge选择最优实践
4. 知识库进化 - 持续更新完善解决方案能力

设计原则:
- 智能: 自动recognize高价值信息
- 敏捷: 快速迭代学习
- 持续: 长期跟踪更新
- 择优: 只学习最优实践
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import re

class ProviderCategory(Enum):
    """服务商赛道分类"""
    MEMBERSHIP = "会员体系"
    DIGITAL_OPERATION = "数字化运营"
    DIGITAL_TRANSFORMATION = "数字化转型"
    INTEGRATED_MARKETING = "整合营销"
    XIAOHONGSHU = "小红书运营"
    DOUYIN = "抖音运营"
    AI_GROWTH = "AI增长"
    O2O = "O2O运营"
    NEW_RETAIL = "新零售"
    CROSS_BORDER = "跨境电商"
    LIVE_COMMERCE = "直播电商"
    KOL_MARKETING = "KOL营销"
    BRAND_BUILDING = "品牌建设"
    DATA_DRIVEN = "数据驱动营销"
    SOFTWARE_SOLUTION = "软件系统/解决方案"

class CapabilityType(Enum):
    """能力类型"""
    TECHNOLOGY = "技术能力"
    PRODUCT = "产品能力"
    SERVICE = "服务能力"
    INDUSTRY_EXPERTISE = "行业 expertise"
    DATA_CAPABILITY = "数据能力"
    ECOSYSTEM = "生态能力"
    INNOVATION = "创新能力"
    EXECUTION = "执行能力"

class AdvantageLevel(Enum):
    """优势等级"""
    INDUSTRY_LEADING = "行业领先"      # 行业TOP3
    STRONG = "强势"                   # 明显优势
    COMPETITIVE = "有竞争力"          # 具备竞争力
    AVERAGE = "一般"                  # 平均水平
    WEAK = "较弱"                     # 相对弱势

@dataclass
class ProviderCapability:
    """服务商能力项"""
    capability_type: CapabilityType
    name: str
    description: str
    advantage_level: AdvantageLevel
    evidence: List[str] = field(default_factory=list)  # 支撑证据
    differentiators: List[str] = field(default_factory=list)  # 差异化点
    score: float = 0.0  # 能力评分 0-10
    confidence: float = 0.7  # 置信度

@dataclass
class SolutionAdvantage:
    """解决方案优势"""
    solution_name: str
    core_strengths: List[str]  # 核心优势
    target_scenarios: List[str]  # 适用场景
    unique_value: str  # 独特价值主张
    case_evidence: List[Dict] = field(default_factory=list)  # 案例证据
    advantage_level: AdvantageLevel = AdvantageLevel.COMPETITIVE

@dataclass
class PPTCapability:
    """PPT/提案能力"""
    visual_style: str  # 视觉style
    content_structure: str  # 内容结构特点
    storytelling_ability: str  # 叙事能力
    data_visualization: str  # 数据呈现
    industry_templates: List[str] = field(default_factory=list)  # 行业模板
    score: float = 0.0

@dataclass
class ProviderProfile:
    """服务商档案"""
    name: str
    category: ProviderCategory
    official_website: Optional[str] = None
    founded_year: Optional[int] = None
    company_scale: str = "unknown"  # startup/growth/mature/enterprise
    funding_stage: Optional[str] = None
    
    # 能力评估
    capabilities: Dict[CapabilityType, ProviderCapability] = field(default_factory=dict)
    solutions: Dict[str, SolutionAdvantage] = field(default_factory=dict)
    ppt_capability: Optional[PPTCapability] = None
    
    # 学习元数据
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())
    data_sources: List[str] = field(default_factory=list)
    learning_confidence: float = 0.0
    
    def get_top_capabilities(self, n: int = 3) -> List[ProviderCapability]:
        """getTOP N能力"""
        sorted_caps = sorted(
            self.capabilities.values(),
            key=lambda x: x.score,
            reverse=True
        )
        return sorted_caps[:n]
    
    def get_core_differentiators(self) -> List[str]:
        """get核心差异化优势"""
        differentiators = []
        for cap in self.capabilities.values():
            if cap.advantage_level in [AdvantageLevel.INDUSTRY_LEADING, AdvantageLevel.STRONG]:
                differentiators.extend(cap.differentiators)
        return list(set(differentiators))

@dataclass
class CategoryIntelligence:
    """赛道情报汇总"""
    category: ProviderCategory
    providers: Dict[str, ProviderProfile] = field(default_factory=dict)
    
    # 赛道洞察
    key_trends: List[str] = field(default_factory=list)
    best_practices: List[str] = field(default_factory=list)
    capability_gaps: List[str] = field(default_factory=list)
    
    # 标杆分析
    technology_leader: Optional[str] = None
    service_leader: Optional[str] = None
    innovation_leader: Optional[str] = None
    
    def get_leaderboard(self, by: str = "overall") -> List[Tuple[str, float]]:
        """get服务商排名"""
        scores = []
        for name, profile in self.providers.items():
            if by == "overall":
                score = sum(c.score for c in profile.capabilities.values()) / max(len(profile.capabilities), 1)
            elif by == "technology":
                score = profile.capabilities.get(CapabilityType.TECHNOLOGY, ProviderCapability(
                    CapabilityType.TECHNOLOGY, "", "", AdvantageLevel.AVERAGE
                )).score
            elif by == "service":
                score = profile.capabilities.get(CapabilityType.SERVICE, ProviderCapability(
                    CapabilityType.SERVICE, "", "", AdvantageLevel.AVERAGE
                )).score
            else:
                score = 0
            scores.append((name, score))
        
        return sorted(scores, key=lambda x: x[1], reverse=True)

class ProviderIntelligenceEngine:
    """服务商智能学习引擎"""
    
    def __init__(self):
        self.intelligence_db: Dict[ProviderCategory, CategoryIntelligence] = {}
        self.learning_history: List[Dict] = []
        self._init_categories()
    
    def _init_categories(self):
        """init赛道分类"""
        for category in ProviderCategory:
            self.intelligence_db[category] = CategoryIntelligence(category=category)
    
    def learn_provider(self, category: ProviderCategory, provider_name: str,
                       raw_data: Dict[str, Any]) -> ProviderProfile:
        """
        学习单个服务商
        
        流程:
        1. 数据清洗与结构化
        2. 能力recognize与评分
        3. 优势提炼
        4. 知识库更新
        """
        # 1. 创建或更新档案
        category_intel = self.intelligence_db[category]
        if provider_name in category_intel.providers:
            profile = category_intel.providers[provider_name]
        else:
            profile = ProviderProfile(name=provider_name, category=category)
        
        # 2. 提取基础信息
        profile.official_website = raw_data.get("website")
        profile.company_scale = raw_data.get("scale", "unknown")
        profile.founded_year = raw_data.get("founded_year")
        profile.data_sources.append(raw_data.get("source", "manual"))
        
        # 3. 分析能力
        profile.capabilities = self._analyze_capabilities(raw_data)
        
        # 4. 分析解决方案
        profile.solutions = self._analyze_solutions(raw_data)
        
        # 5. 分析PPT能力
        profile.ppt_capability = self._analyze_ppt_capability(raw_data)
        
        # 6. 计算学习置信度
        profile.learning_confidence = self._calculate_confidence(raw_data)
        profile.last_updated = datetime.now().isoformat()
        
        # 7. 更新知识库
        category_intel.providers[provider_name] = profile
        
        # 8. 记录学习历史
        self.learning_history.append({
            "timestamp": datetime.now().isoformat(),
            "category": category.value,
            "provider": provider_name,
            "confidence": profile.learning_confidence,
            "top_capabilities": [c.name for c in profile.get_top_capabilities(3)]
        })
        
        return profile
    
    def _analyze_capabilities(self, raw_data: Dict) -> Dict[CapabilityType, ProviderCapability]:
        """分析服务商能力"""
        capabilities = {}
        
        # 技术能力分析
        tech_indicators = raw_data.get("technology_indicators", [])
        tech_score = self._score_capability(tech_indicators, "technology")
        capabilities[CapabilityType.TECHNOLOGY] = ProviderCapability(
            capability_type=CapabilityType.TECHNOLOGY,
            name="技术能力",
            description=self._extract_tech_description(tech_indicators),
            advantage_level=self._level_from_score(tech_score),
            evidence=tech_indicators[:5],
            differentiators=self._extract_differentiators(tech_indicators),
            score=tech_score,
            confidence=0.7 if tech_indicators else 0.3
        )
        
        # 产品能力分析
        product_indicators = raw_data.get("product_indicators", [])
        product_score = self._score_capability(product_indicators, "product")
        capabilities[CapabilityType.PRODUCT] = ProviderCapability(
            capability_type=CapabilityType.PRODUCT,
            name="产品能力",
            description=self._extract_product_description(product_indicators),
            advantage_level=self._level_from_score(product_score),
            evidence=product_indicators[:5],
            differentiators=self._extract_differentiators(product_indicators),
            score=product_score,
            confidence=0.7 if product_indicators else 0.3
        )
        
        # 服务能力分析
        service_indicators = raw_data.get("service_indicators", [])
        service_score = self._score_capability(service_indicators, "service")
        capabilities[CapabilityType.SERVICE] = ProviderCapability(
            capability_type=CapabilityType.SERVICE,
            name="服务能力",
            description=self._extract_service_description(service_indicators),
            advantage_level=self._level_from_score(service_score),
            evidence=service_indicators[:5],
            differentiators=self._extract_differentiators(service_indicators),
            score=service_score,
            confidence=0.7 if service_indicators else 0.3
        )
        
        # 行业 expertise 分析
        industry_indicators = raw_data.get("industry_expertise", [])
        industry_score = self._score_capability(industry_indicators, "industry")
        capabilities[CapabilityType.INDUSTRY_EXPERTISE] = ProviderCapability(
            capability_type=CapabilityType.INDUSTRY_EXPERTISE,
            name="行业 expertise",
            description=self._extract_industry_description(industry_indicators),
            advantage_level=self._level_from_score(industry_score),
            evidence=industry_indicators[:5],
            differentiators=self._extract_differentiators(industry_indicators),
            score=industry_score,
            confidence=0.7 if industry_indicators else 0.3
        )
        
        return capabilities
    
    def _analyze_solutions(self, raw_data: Dict) -> Dict[str, SolutionAdvantage]:
        """分析解决方案优势"""
        solutions = {}
        
        solution_data = raw_data.get("solutions", [])
        for sol in solution_data:
            name = sol.get("name", "未知方案")
            advantages = sol.get("advantages", [])
            
            solutions[name] = SolutionAdvantage(
                solution_name=name,
                core_strengths=advantages[:5],
                target_scenarios=sol.get("scenarios", []),
                unique_value=sol.get("unique_value", ""),
                case_evidence=sol.get("cases", []),
                advantage_level=self._level_from_score(len(advantages) * 2)
            )
        
        return solutions
    
    def _analyze_ppt_capability(self, raw_data: Dict) -> Optional[PPTCapability]:
        """分析PPT/提案能力"""
        ppt_data = raw_data.get("ppt_capability", {})
        
        if not ppt_data:
            return None
        
        return PPTCapability(
            visual_style=ppt_data.get("visual_style", "unknown"),
            content_structure=ppt_data.get("content_structure", "standard"),
            storytelling_ability=ppt_data.get("storytelling", "average"),
            data_visualization=ppt_data.get("data_viz", "standard"),
            industry_templates=ppt_data.get("templates", []),
            score=ppt_data.get("score", 5.0)
        )
    
    def _score_capability(self, indicators: List[str], cap_type: str) -> float:
        """
        基于metrics评分能力
        
        评分逻辑:
        - metrics数量: 每1个metrics+1分,最多5分
        - metrics质量: 包含关键词额外加分
        - 独特性: 有差异化描述额外加分
        """
        base_score = min(len(indicators), 5)
        
        # 关键词加分
        quality_keywords = {
            "technology": ["AI", "大数据", "云计算", "自研", "专利", "算法", "智能"],
            "product": ["全链路", "一站式", "模块化", "SaaS", "PaaS", "生态"],
            "service": ["专属", "7x24", "本地化", "行业专家", "全程", "定制"],
            "industry": ["深耕", "标杆", "头部", "垂直", "专注", "领先"]
        }
        
        quality_bonus = 0
        keywords = quality_keywords.get(cap_type, [])
        for indicator in indicators:
            for keyword in keywords:
                if keyword in indicator:
                    quality_bonus += 0.5
                    break
        
        # 差异化加分
        unique_bonus = 0
        for indicator in indicators:
            if any(word in indicator for word in ["首创", "唯一", "独家", "领先", "第一"]):
                unique_bonus += 0.3
        
        total = base_score + min(quality_bonus, 3) + min(unique_bonus, 2)
        return min(10, total)
    
    def _level_from_score(self, score: float) -> AdvantageLevel:
        """分数转等级"""
        if score >= 8:
            return AdvantageLevel.INDUSTRY_LEADING
        elif score >= 6:
            return AdvantageLevel.STRONG
        elif score >= 4:
            return AdvantageLevel.COMPETITIVE
        elif score >= 2:
            return AdvantageLevel.AVERAGE
        else:
            return AdvantageLevel.WEAK
    
    def _extract_tech_description(self, indicators: List[str]) -> str:
        """提取技术能力描述"""
        if not indicators:
            return "技术能力信息不足"
        
        # 提取核心技术关键词
        tech_keywords = ["AI", "大数据", "云计算", "算法", "平台", "系统", "引擎"]
        found_keywords = []
        for indicator in indicators[:3]:
            for kw in tech_keywords:
                if kw in indicator and kw not in found_keywords:
                    found_keywords.append(kw)
        
        if found_keywords:
            return f"具备{', '.join(found_keywords)}等技术能力"
        return "拥有自主研发技术能力"
    
    def _extract_product_description(self, indicators: List[str]) -> str:
        """提取产品能力描述"""
        if not indicators:
            return "产品能力信息不足"
        return "产品线完善,覆盖核心场景"
    
    def _extract_service_description(self, indicators: List[str]) -> str:
        """提取服务能力描述"""
        if not indicators:
            return "服务能力信息不足"
        return "服务体系完善,响应及时"
    
    def _extract_industry_description(self, indicators: List[str]) -> str:
        """提取行业 expertise 描述"""
        if not indicators:
            return "行业经验信息不足"
        return "深耕垂直行业,理解业务场景"
    
    def _extract_differentiators(self, indicators: List[str]) -> List[str]:
        """提取差异化优势"""
        differentiators = []
        unique_keywords = ["首创", "唯一", "独家", "领先", "第一", "最大", "最强"]
        
        for indicator in indicators:
            for keyword in unique_keywords:
                if keyword in indicator:
                    differentiators.append(indicator)
                    break
        
        return differentiators[:3]
    
    def _calculate_confidence(self, raw_data: Dict) -> float:
        """计算学习置信度"""
        factors = []
        
        # 数据源丰富度
        if raw_data.get("website"):
            factors.append(0.2)
        if raw_data.get("cases"):
            factors.append(0.2)
        if raw_data.get("reviews"):
            factors.append(0.15)
        
        # 信息完整度
        info_fields = ["technology_indicators", "product_indicators", "service_indicators"]
        for field in info_fields:
            if raw_data.get(field):
                factors.append(0.15)
        
        return min(0.95, sum(factors))
    
    def extract_best_practices(self, category: ProviderCategory) -> Dict[str, Any]:
        """
        提取赛道最佳实践
        
        择优逻辑:
        1. 找出各领域评分最高的服务商
        2. 提取其核心优势作为最佳实践
        3. 汇总形成赛道能力标准
        """
        category_intel = self.intelligence_db[category]
        
        best_practices = {
            "category": category.value,
            "extracted_at": datetime.now().isoformat(),
            "technology_best": None,
            "product_best": None,
            "service_best": None,
            "overall_best": None,
            "key_insights": []
        }
        
        # 找出各领域最佳
        tech_leader = None
        product_leader = None
        service_leader = None
        overall_leader = None
        
        max_tech_score = 0
        max_product_score = 0
        max_service_score = 0
        max_overall_score = 0
        
        for name, profile in category_intel.providers.items():
            # 技术领先
            tech_score = profile.capabilities.get(CapabilityType.TECHNOLOGY, ProviderCapability(
                CapabilityType.TECHNOLOGY, "", "", AdvantageLevel.AVERAGE
            )).score
            if tech_score > max_tech_score:
                max_tech_score = tech_score
                tech_leader = name
            
            # 产品领先
            product_score = profile.capabilities.get(CapabilityType.PRODUCT, ProviderCapability(
                CapabilityType.PRODUCT, "", "", AdvantageLevel.AVERAGE
            )).score
            if product_score > max_product_score:
                max_product_score = product_score
                product_leader = name
            
            # 服务领先
            service_score = profile.capabilities.get(CapabilityType.SERVICE, ProviderCapability(
                CapabilityType.SERVICE, "", "", AdvantageLevel.AVERAGE
            )).score
            if service_score > max_service_score:
                max_service_score = service_score
                service_leader = name
            
            # synthesize领先
            overall_score = sum(c.score for c in profile.capabilities.values()) / max(len(profile.capabilities), 1)
            if overall_score > max_overall_score:
                max_overall_score = overall_score
                overall_leader = name
        
        best_practices["technology_best"] = {
            "provider": tech_leader,
            "score": max_tech_score,
            "key_strengths": self._get_provider_strengths(category, tech_leader) if tech_leader else []
        }
        best_practices["product_best"] = {
            "provider": product_leader,
            "score": max_product_score,
            "key_strengths": self._get_provider_strengths(category, product_leader) if product_leader else []
        }
        best_practices["service_best"] = {
            "provider": service_leader,
            "score": max_service_score,
            "key_strengths": self._get_provider_strengths(category, service_leader) if service_leader else []
        }
        best_practices["overall_best"] = {
            "provider": overall_leader,
            "score": max_overall_score,
            "key_strengths": self._get_provider_strengths(category, overall_leader) if overall_leader else []
        }
        
        # generate洞察
        best_practices["key_insights"] = self._generate_insights(category, best_practices)
        
        return best_practices
    
    def _get_provider_strengths(self, category: ProviderCategory, provider_name: str) -> List[str]:
        """get服务商核心优势"""
        profile = self.intelligence_db[category].providers.get(provider_name)
        if not profile:
            return []
        
        strengths = []
        for cap in profile.get_top_capabilities(3):
            strengths.append(f"{cap.name}: {cap.description}")
        
        return strengths
    
    def _generate_insights(self, category: ProviderCategory, best_practices: Dict) -> List[str]:
        """generate赛道洞察"""
        insights = []
        
        # 技术洞察
        if best_practices["technology_best"]["provider"]:
            insights.append(
                f"技术领先者: {best_practices['technology_best']['provider']} "
                f"(评分: {best_practices['technology_best']['score']:.1f})"
            )
        
        # synthesize洞察
        if best_practices["overall_best"]["provider"]:
            insights.append(
                f"synthesize领先者: {best_practices['overall_best']['provider']} "
                f"(评分: {best_practices['overall_best']['score']:.1f})"
            )
        
        return insights
    
    def generate_solution_enhancement(self, category: ProviderCategory) -> Dict[str, Any]:
        """
        generate解决方案能力增强建议
        
        基于学习结果,提出自身能力提升方向
        """
        best_practices = self.extract_best_practices(category)
        
        enhancement = {
            "category": category.value,
            "generated_at": datetime.now().isoformat(),
            "recommended_capabilities": [],
            "differentiation_opportunities": [],
            "implementation_priority": []
        }
        
        # 推荐学习的能力
        for cap_type in CapabilityType:
            best_provider = best_practices.get(f"{cap_type.value.lower()}_best", {})
            if best_provider and best_provider.get("score", 0) >= 7:
                enhancement["recommended_capabilities"].append({
                    "capability": cap_type.value,
                    "learn_from": best_provider["provider"],
                    "key_strengths": best_provider["key_strengths"][:2]
                })
        
        return enhancement
    
    def export_knowledge_base(self, output_path: str):
        """导出知识库"""
        export_data = {
            "export_time": datetime.now().isoformat(),
            "categories": {}
        }
        
        for category, intel in self.intelligence_db.items():
            export_data["categories"][category.value] = {
                "provider_count": len(intel.providers),
                "providers": {
                    name: {
                        "top_capabilities": [
                            {"type": c.capability_type.value, "name": c.name, "score": c.score}
                            for c in profile.get_top_capabilities(3)
                        ],
                        "core_differentiators": profile.get_core_differentiators(),
                        "learning_confidence": profile.learning_confidence
                    }
                    for name, profile in intel.providers.items()
                },
                "best_practices": self.extract_best_practices(category)
            }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        return export_data

# ==================== 便捷使用接口 ====================

def quick_learn(category: str, provider_name: str, raw_data: Dict) -> Dict:
    """
    快速学习单个服务商
    
    示例:
        result = quick_learn(
            category="会员体系",
            provider_name="有赞新零售 CRM",
            raw_data={
                "technology_indicators": ["SaaS平台", "AI智能推荐", "大数据分析"],
                "product_indicators": ["全渠道会员管理", "营销自动化", "积分商城"],
                "service_indicators": ["专属客户成功经理", "7x24技术支持"],
                "solutions": [
                    {
                        "name": "新零售会员解决方案",
                        "advantages": ["全渠道打通", "智能分层运营", "自动化营销"],
                        "scenarios": ["连锁零售", "品牌直营"]
                    }
                ]
            }
        )
    """
    engine = ProviderIntelligenceEngine()
    
    # 转换分类
    category_map = {c.value: c for c in ProviderCategory}
    cat_enum = category_map.get(category, ProviderCategory.MEMBERSHIP)
    
    profile = engine.learn_provider(cat_enum, provider_name, raw_data)
    
    return {
        "provider": profile.name,
        "category": profile.category.value,
        "top_capabilities": [
            {"name": c.name, "score": c.score, "level": c.advantage_level.value}
            for c in profile.get_top_capabilities(3)
        ],
        "core_differentiators": profile.get_core_differentiators(),
        "learning_confidence": profile.learning_confidence
    }

def batch_learn_providers(providers_data: List[Dict]) -> Dict:
    """
    批量学习服务商
    
    输入格式:
    [
        {
            "category": "会员体系",
            "name": "有赞新零售 CRM",
            "data": {...}
        },
        ...
    ]
    """
    engine = ProviderIntelligenceEngine()
    results = []
    
    category_map = {c.value: c for c in ProviderCategory}
    
    for item in providers_data:
        cat_enum = category_map.get(item["category"], ProviderCategory.MEMBERSHIP)
        profile = engine.learn_provider(cat_enum, item["name"], item["data"])
        results.append({
            "name": profile.name,
            "category": profile.category.value,
            "top_capability": profile.get_top_capabilities(1)[0].name if profile.capabilities else "未知"
        })
    
    return {
        "learned_count": len(results),
        "providers": results
    }

# ==================== 测试示例 ====================

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
