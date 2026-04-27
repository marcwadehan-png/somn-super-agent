"""
__all__ = [
    'analyze',
    'collect_signals',
    'create_personas',
    'export_report',
    'get_analysis_framework',
    'identify_demands',
    'prioritized_demands',
    'priority_score',
]

需求分析引擎 - Demand Analysis Engine
基于超级智能体理念
实现六步需求分析流程
"""

import json
import yaml
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import re
import logging

logger = logging.getLogger(__name__)

class DemandType(Enum):
    """需求类型"""
    EXPLICIT = "explicit"       # 显性需求 - 用户明确表达
    IMPLICIT = "implicit"       # 隐性需求 - 用户未明确表达但存在
    LATENT = "latent"           # 潜在需求 - 用户自己都没意识到
    FUTURE = "future"           # 未来需求 - 趋势驱动

class DemandUrgency(Enum):
    """需求紧急程度"""
    CRITICAL = "critical"       # 紧急且重要
    HIGH = "high"               # 重要
    MEDIUM = "medium"           # 一般
    LOW = "low"                 # 低优先级

class DemandCategory(Enum):
    """需求分类"""
    FUNCTIONAL = "functional"       # 功能需求
    EMOTIONAL = "emotional"         # 情感需求
    SOCIAL = "social"               # 社交需求
    ECONOMIC = "economic"           # 经济需求
    EXPERIENCE = "experience"       # 体验需求

@dataclass
class UserPersona:
    """用户画像"""
    id: str
    name: str
    description: str
    demographics: Dict = field(default_factory=dict)  # 人口统计characteristics
    behaviors: List[str] = field(default_factory=list)  # 行为characteristics
    pain_points: List[str] = field(default_factory=list)  # 痛点
    goals: List[str] = field(default_factory=list)  # 目标
    motivations: List[str] = field(default_factory=list)  # 动机
    tech_savvy: str = "medium"  # low/medium/high
    price_sensitivity: str = "medium"  # low/medium/high
    decision_making: str = "rational"  # rational/emotional/social
    
    # 需求强度
    demand_strength: float = 0.5  # 0-1
    
    # 使用场景
    usage_scenarios: List[Dict] = field(default_factory=list)

@dataclass
class DemandSignal:
    """需求信号"""
    id: str
    source: str  # 来源: 用户反馈/搜索数据/竞品分析/市场报告
    signal_type: str  # 信号类型: 反馈/搜索/行为/趋势
    content: str  # 信号内容
    timestamp: str
    
    # 分析结果
    related_demands: List[str] = field(default_factory=list)
    sentiment: str = "neutral"  # positive/negative/neutral
    intensity: float = 0.5  # 0-1
    
    # 元数据
    metadata: Dict = field(default_factory=dict)

@dataclass
class DemandItem:
    """需求项"""
    id: str
    name: str
    description: str
    
    demand_type: DemandType
    category: DemandCategory
    urgency: DemandUrgency
    
    # 量化metrics
    frequency: int = 1  # 出现频次
    impact_score: float = 0.5  # 影响程度 0-1
    feasibility: float = 0.5  # 可行性 0-1
    
    # 关联
    related_personas: List[str] = field(default_factory=list)
    related_signals: List[str] = field(default_factory=list)
    
    # 优先级计算
    @property
    def priority_score(self) -> float:
        """计算优先级分数"""
        urgency_weights = {
            DemandUrgency.CRITICAL: 1.0,
            DemandUrgency.HIGH: 0.8,
            DemandUrgency.MEDIUM: 0.5,
            DemandUrgency.LOW: 0.2
        }
        
        urgency_weight = urgency_weights.get(self.urgency, 0.5)
        
        # 优先级 = 紧急度 × 影响 × 可行性 × 频次因子
        frequency_factor = min(self.frequency / 10, 1.0)  # 最高1.0
        
        return urgency_weight * self.impact_score * self.feasibility * (1 + frequency_factor)

@dataclass
class DemandAnalysisReport:
    """需求分析报告"""
    id: str
    business_context: Dict
    
    # 分析结果
    personas: List[UserPersona] = field(default_factory=list)
    signals: List[DemandSignal] = field(default_factory=list)
    demands: List[DemandItem] = field(default_factory=list)
    
    # 洞察
    key_insights: List[str] = field(default_factory=list)
    opportunities: List[Dict] = field(default_factory=list)
    recommendations: List[Dict] = field(default_factory=list)
    
    # 优先级排序后的需求
    @property
    def prioritized_demands(self) -> List[DemandItem]:
        return sorted(self.demands, key=lambda d: d.priority_score, reverse=True)
    
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

class DemandAnalyzer:
    """
    需求分析引擎
    
    核心流程 (六步法):
    1. 需求收集 - 多源数据整合
    2. 需求recognize - 从信号中提取需求
    3. 需求分类 - 按类型/类别/紧急度分类
    4. 需求验证 - 验证需求真实性
    5. 需求量化 - 评估影响与可行性
    6. 需求优先级 - 排序与输出
    """
    
    def __init__(self):
        self.demand_patterns = self._init_demand_patterns()
        self.persona_templates = self._init_persona_templates()
        
    def _init_demand_patterns(self) -> Dict:
        """init需求模式库"""
        return {
            "pain_point_indicators": [
                "太麻烦", "浪费时间", "不好用", "难操作", "太贵",
                "找不到", "不懂", "不会", "太复杂", "太慢"
            ],
            "desire_indicators": [
                "希望能", "想要", "期待", "需要", "建议",
                "要是能", "如果有", "最好有", "建议增加"
            ],
            "satisfaction_indicators": [
                "很好", "不错", "满意", "喜欢", "方便",
                "好用", "简单", "快捷", "高效"
            ],
            "comparison_indicators": [
                "比XX好", "不如XX", "和XX比", "XX有"
            ]
        }
    
    def _init_persona_templates(self) -> Dict:
        """init用户画像模板"""
        return {
            "early_adopter": {
                "name": "早期采用者",
                "description": "愿意尝试新产品,对创新敏感",
                "tech_savvy": "high",
                "price_sensitivity": "low",
                "decision_making": "emotional",
                "motivations": ["领先体验", "社交货币", "效率提升"]
            },
            "pragmatist": {
                "name": "务实主义者",
                "description": "注重实用性和性价比",
                "tech_savvy": "medium",
                "price_sensitivity": "high",
                "decision_making": "rational",
                "motivations": ["成本节约", "效率提升", "问题解决"]
            },
            "conservative": {
                "name": "保守派用户",
                "description": "谨慎decision,依赖口碑和推荐",
                "tech_savvy": "low",
                "price_sensitivity": "medium",
                "decision_making": "social",
                "motivations": ["安全可靠", "他人推荐", "减少风险"]
            },
            "power_user": {
                "name": "重度用户",
                "description": "高频使用,深度依赖",
                "tech_savvy": "high",
                "price_sensitivity": "low",
                "decision_making": "rational",
                "motivations": ["效率最大化", "功能完整", "专业需求"]
            }
        }
    
    def collect_signals(self, sources: List[Dict]) -> List[DemandSignal]:
        """
        需求收集 - 从多源数据收集需求信号
        
        Args:
            sources: 数据源列表
                [
                    {"type": "user_feedback", "data": [...]},
                    {"type": "search_data", "data": [...]},
                    {"type": "behavior_data", "data": [...]},
                    {"type": "competitor_analysis", "data": [...]},
                    {"type": "market_report", "data": [...]}
                ]
        
        Returns:
            需求信号列表
        """
        signals = []
        signal_counter = 0
        
        for source in sources:
            source_type = source.get("type", "unknown")
            data = source.get("data", [])
            
            for item in data:
                signal_counter += 1
                
                # 根据数据源类型解析
                if source_type == "user_feedback":
                    signal = self._parse_user_feedback(item, signal_counter)
                elif source_type == "search_data":
                    signal = self._parse_search_data(item, signal_counter)
                elif source_type == "behavior_data":
                    signal = self._parse_behavior_data(item, signal_counter)
                elif source_type == "competitor_analysis":
                    signal = self._parse_competitor_data(item, signal_counter)
                elif source_type == "market_report":
                    signal = self._parse_market_data(item, signal_counter)
                else:
                    signal = DemandSignal(
                        id=f"signal_{signal_counter:04d}",
                        source=source_type,
                        signal_type="unknown",
                        content=str(item),
                        timestamp=datetime.now().isoformat()
                    )
                
                signals.append(signal)
        
        logger.info(f"需求信号收集完成: 共 {len(signals)} 条")
        return signals
    
    def _parse_user_feedback(self, item: Dict, counter: int) -> DemandSignal:
        """解析用户反馈"""
        content = item.get("content", "")
        
        # 情感分析
        sentiment = self._analyze_sentiment(content)
        
        # recognize相关需求
        related_demands = self._extract_demand_keywords(content)
        
        return DemandSignal(
            id=f"signal_{counter:04d}",
            source="user_feedback",
            signal_type="feedback",
            content=content,
            timestamp=item.get("timestamp", datetime.now().isoformat()),
            related_demands=related_demands,
            sentiment=sentiment,
            intensity=abs(self._calculate_intensity(content)),
            metadata={
                "user_id": item.get("user_id"),
                "channel": item.get("channel"),
                "rating": item.get("rating")
            }
        )
    
    def _parse_search_data(self, item: Dict, counter: int) -> DemandSignal:
        """解析搜索数据"""
        query = item.get("query", "")
        
        return DemandSignal(
            id=f"signal_{counter:04d}",
            source="search_data",
            signal_type="search",
            content=query,
            timestamp=item.get("timestamp", datetime.now().isoformat()),
            related_demands=self._extract_demand_keywords(query),
            sentiment="neutral",
            intensity=min(item.get("volume", 100) / 1000, 1.0),
            metadata={
                "search_volume": item.get("volume"),
                "trend": item.get("trend", "stable")
            }
        )
    
    def _parse_behavior_data(self, item: Dict, counter: int) -> DemandSignal:
        """解析行为数据"""
        event = item.get("event", "")
        
        return DemandSignal(
            id=f"signal_{counter:04d}",
            source="behavior_data",
            signal_type="behavior",
            content=f"{event}: {item.get("details", "")}",
            timestamp=item.get("timestamp", datetime.now().isoformat()),
            related_demands=[],
            sentiment="neutral",
            intensity=0.5,
            metadata={
                "user_id": item.get("user_id"),
                "event_type": event,
                "session_duration": item.get("session_duration")
            }
        )
    
    def _parse_competitor_data(self, item: Dict, counter: int) -> DemandSignal:
        """解析竞品分析数据"""
        feature = item.get("feature", "")
        
        return DemandSignal(
            id=f"signal_{counter:04d}",
            source="competitor_analysis",
            signal_type="comparison",
            content=f"竞品{feature}: {item.get("description", "")}",
            timestamp=item.get("timestamp", datetime.now().isoformat()),
            related_demands=[feature],
            sentiment="neutral",
            intensity=0.6,
            metadata={
                "competitor": item.get("competitor"),
                "user_adoption": item.get("adoption_rate")
            }
        )
    
    def _parse_market_data(self, item: Dict, counter: int) -> DemandSignal:
        """解析市场报告数据"""
        trend = item.get("trend", "")
        
        return DemandSignal(
            id=f"signal_{counter:04d}",
            source="market_report",
            signal_type="trend",
            content=trend,
            timestamp=item.get("timestamp", datetime.now().isoformat()),
            related_demands=item.get("related_demands", []),
            sentiment="neutral",
            intensity=0.7,
            metadata={
                "report_source": item.get("source"),
                "confidence": item.get("confidence")
            }
        )
    
    def _analyze_sentiment(self, text: str) -> str:
        """简单情感分析"""
        positive_words = self.demand_patterns["satisfaction_indicators"]
        negative_words = self.demand_patterns["pain_point_indicators"]
        
        pos_count = sum(1 for w in positive_words if w in text)
        neg_count = sum(1 for w in negative_words if w in text)
        
        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        else:
            return "neutral"
    
    def _calculate_intensity(self, text: str) -> float:
        """计算强度"""
        # 感叹号数量
        exclamation_count = text.count("!") + text.count("!")
        # 负面词汇数量
        negative_count = sum(1 for w in self.demand_patterns["pain_point_indicators"] if w in text)
        
        base_intensity = 0.3
        intensity = base_intensity + exclamation_count * 0.1 + negative_count * 0.1
        return min(intensity, 1.0)
    
    def _extract_demand_keywords(self, text: str) -> List[str]:
        """提取需求关键词"""
        keywords = []
        
        # 匹配需求表达模式
        for indicator in self.demand_patterns["desire_indicators"]:
            if indicator in text:
                # 提取关键词后的内容
                pattern = f"{indicator}(.{{0,20}})"
                matches = re.findall(pattern, text)
                keywords.extend([m.strip() for m in matches])
        
        return keywords[:5]  # 最多5个
    
    def identify_demands(self, signals: List[DemandSignal]) -> List[DemandItem]:
        """
        需求recognize - 从信号中提取需求
        
        Args:
            signals: 需求信号列表
        
        Returns:
            需求项列表
        """
        demand_map = {}  # 用于去重
        demand_counter = 0
        
        for signal in signals:
            # 基于信号内容recognize需求
            extracted_demands = self._extract_demands_from_signal(signal)
            
            for demand_info in extracted_demands:
                demand_key = demand_info["name"]
                
                if demand_key in demand_map:
                    # 更新已有需求
                    existing = demand_map[demand_key]
                    existing.frequency += 1
                    existing.related_signals.append(signal.id)
                    existing.impact_score = min(existing.impact_score + 0.05, 1.0)
                else:
                    # 创建新需求
                    demand_counter += 1
                    demand = DemandItem(
                        id=f"demand_{demand_counter:04d}",
                        name=demand_info["name"],
                        description=demand_info["description"],
                        demand_type=demand_info.get("type", DemandType.EXPLICIT),
                        category=demand_info.get("category", DemandCategory.FUNCTIONAL),
                        urgency=demand_info.get("urgency", DemandUrgency.MEDIUM),
                        frequency=1,
                        impact_score=signal.intensity * 0.7,
                        feasibility=0.5,
                        related_signals=[signal.id]
                    )
                    demand_map[demand_key] = demand
        
        demands = list(demand_map.values())
        logger.info(f"需求recognize完成: 共 {len(demands)} 个独立需求")
        return demands
    
    def _extract_demands_from_signal(self, signal: DemandSignal) -> List[Dict]:
        """从单个信号提取需求"""
        demands = []
        content = signal.content
        
        # 基于信号类型提取
        if signal.signal_type == "feedback":
            # 用户反馈中提取痛点
            for indicator in self.demand_patterns["pain_point_indicators"]:
                if indicator in content:
                    demands.append({
                        "name": f"解决{indicator}问题",
                        "description": f"用户反馈: {content[:50]}...",
                        "type": DemandType.EXPLICIT,
                        "category": DemandCategory.FUNCTIONAL,
                        "urgency": DemandUrgency.HIGH if signal.sentiment == "negative" else DemandUrgency.MEDIUM
                    })
                    break
        
        elif signal.signal_type == "search":
            # 搜索词直接作为需求
            demands.append({
                "name": f"搜索需求: {content[:20]}",
                "description": f"用户搜索: {content}",
                "type": DemandType.EXPLICIT,
                "category": DemandCategory.FUNCTIONAL,
                "urgency": DemandUrgency.MEDIUM
            })
        
        elif signal.signal_type == "trend":
            # 趋势作为潜在需求
            demands.append({
                "name": f"趋势需求: {content[:20]}",
                "description": f"市场趋势: {content}",
                "type": DemandType.LATENT,
                "category": DemandCategory.FUNCTIONAL,
                "urgency": DemandUrgency.MEDIUM
            })
        
        # 如果没有提取到,创建一个通用需求
        if not demands:
            demands.append({
                "name": f"需求信号: {content[:15]}...",
                "description": content,
                "type": DemandType.IMPLICIT,
                "category": DemandCategory.FUNCTIONAL,
                "urgency": DemandUrgency.LOW
            })
        
        return demands
    
    def create_personas(self, business_context: Dict) -> List[UserPersona]:
        """
        创建用户画像
        
        Args:
            business_context: 业务上下文
        
        Returns:
            用户画像列表
        """
        personas = []
        industry = business_context.get("industry", "general")
        target_market = business_context.get("target_market", "")
        
        # 基于行业选择模板
        if industry in ["saas_b2b", "enterprise"]:
            persona_types = ["pragmatist", "power_user", "conservative"]
        elif industry in ["saas_b2c", "consumer"]:
            persona_types = ["early_adopter", "pragmatist", "conservative"]
        else:
            persona_types = ["early_adopter", "pragmatist", "power_user"]
        
        for i, ptype in enumerate(persona_types):
            template = self.persona_templates.get(ptype, self.persona_templates["pragmatist"])
            
            persona = UserPersona(
                id=f"persona_{i+1:02d}",
                name=template["name"],
                description=template["description"],
                demographics={
                    "age_range": "25-45",
                    "income_level": "中高收入" if template["price_sensitivity"] == "low" else "中等收入"
                },
                behaviors=template.get("motivations", []),
                pain_points=[],
                goals=template.get("motivations", []),
                motivations=template.get("motivations", []),
                tech_savvy=template.get("tech_savvy", "medium"),
                price_sensitivity=template.get("price_sensitivity", "medium"),
                decision_making=template.get("decision_making", "rational"),
                demand_strength=0.7 if ptype == "early_adopter" else 0.5,
                usage_scenarios=[]
            )
            personas.append(persona)
        
        return personas
    
    def analyze(
        self,
        business_context: Dict,
        data_sources: List[Dict]
    ) -> DemandAnalysisReport:
        """
        执行完整的需求分析流程
        
        Args:
            business_context: 业务上下文
            data_sources: 多源数据
        
        Returns:
            需求分析报告
        """
        report_id = f"demand_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Step 1: 需求收集
        signals = self.collect_signals(data_sources)
        
        # Step 2: 需求recognize
        demands = self.identify_demands(signals)
        
        # Step 3: 用户画像
        personas = self.create_personas(business_context)
        
        # Step 4: 关联画像与需求
        self._associate_demands_with_personas(demands, personas)
        
        # Step 5: generate洞察
        insights = self._generate_insights(demands, signals, personas)
        
        # Step 6: recognize机会
        opportunities = self._identify_opportunities(demands, business_context)
        
        # Step 7: generate建议
        recommendations = self._generate_recommendations(demands, opportunities)
        
        report = DemandAnalysisReport(
            id=report_id,
            business_context=business_context,
            personas=personas,
            signals=signals,
            demands=demands,
            key_insights=insights,
            opportunities=opportunities,
            recommendations=recommendations
        )
        
        logger.info(f"需求分析完成: {report_id}, recognize {len(demands)} 个需求")
        return report
    
    def _associate_demands_with_personas(self, demands: List[DemandItem], personas: List[UserPersona]):
        """关联需求与用户画像"""
        for demand in demands:
            # 简单匹配:根据需求类型匹配画像
            if demand.category == DemandCategory.FUNCTIONAL:
                demand.related_personas = [p.id for p in personas if p.tech_savvy == "high"]
            elif demand.category == DemandCategory.EMOTIONAL:
                demand.related_personas = [p.id for p in personas if p.decision_making == "emotional"]
            else:
                demand.related_personas = [p.id for p in personas]
    
    def _generate_insights(self, demands: List[DemandItem], signals: List[DemandSignal], personas: List[UserPersona]) -> List[str]:
        """generate关键洞察"""
        insights = []
        
        # 洞察1: 需求分布
        type_distribution = {}
        for d in demands:
            t = d.demand_type.value
            type_distribution[t] = type_distribution.get(t, 0) + 1
        
        insights.append(f"需求类型分布: {type_distribution}")
        
        # 洞察2: 高优先级需求
        high_priority = [d for d in demands if d.urgency == DemandUrgency.CRITICAL]
        if high_priority:
            insights.append(f"发现 {len(high_priority)} 个高优先级需求需立即处理")
        
        # 洞察3: 信号强度
        negative_signals = [s for s in signals if s.sentiment == "negative"]
        if negative_signals:
            insights.append(f"有 {len(negative_signals)} 个负面信号需关注")
        
        # 洞察4: 用户画像匹配
        if personas:
            insights.append(f"recognize {len(personas)} 类核心用户群体")
        
        return insights
    
    def _identify_opportunities(self, demands: List[DemandItem], context: Dict) -> List[Dict]:
        """recognize增长机会"""
        opportunities = []
        
        # 机会1: 高优先级未满足需求
        unmet_critical = [d for d in demands if d.urgency == DemandUrgency.CRITICAL and d.feasibility > 0.6]
        if unmet_critical:
            opportunities.append({
                "name": "快速响应关键需求",
                "description": f"有 {len(unmet_critical)} 个高优先级需求具备高可行性",
                "potential_impact": "high",
                "effort": "medium",
                "related_demands": [d.id for d in unmet_critical[:3]]
            })
        
        # 机会2: 高频需求
        frequent_demands = [d for d in demands if d.frequency >= 5]
        if frequent_demands:
            opportunities.append({
                "name": "满足高频共性需求",
                "description": f"{len(frequent_demands)} 个需求被多次提及",
                "potential_impact": "high",
                "effort": "low",
                "related_demands": [d.id for d in frequent_demands[:3]]
            })
        
        # 机会3: 潜在需求
        latent_demands = [d for d in demands if d.demand_type == DemandType.LATENT]
        if latent_demands:
            opportunities.append({
                "name": "挖掘潜在需求",
                "description": f"发现 {len(latent_demands)} 个潜在需求可提前布局",
                "potential_impact": "medium",
                "effort": "high",
                "related_demands": [d.id for d in latent_demands[:3]]
            })
        
        return opportunities
    
    def _generate_recommendations(self, demands: List[DemandItem], opportunities: List[Dict]) -> List[Dict]:
        """generate建议"""
        recommendations = []
        
        # 按优先级排序的需求
        sorted_demands = sorted(demands, key=lambda d: d.priority_score, reverse=True)
        
        # 建议1: 立即action
        immediate = sorted_demands[:3]
        if immediate:
            recommendations.append({
                "priority": "immediate",
                "title": "立即action项",
                "items": [
                    {
                        "demand_id": d.id,
                        "demand_name": d.name,
                        "action": f"启动{d.name}的解决方案设计",
                        "expected_impact": f"优先级分数: {d.priority_score:.2f}"
                    }
                    for d in immediate
                ]
            })
        
        # 建议2: 短期规划
        short_term = sorted_demands[3:6]
        if short_term:
            recommendations.append({
                "priority": "short_term",
                "title": "短期规划项",
                "items": [
                    {
                        "demand_id": d.id,
                        "demand_name": d.name,
                        "action": f"纳入Q2产品规划"
                    }
                    for d in short_term
                ]
            })
        
        # 建议3: 机会把握
        for opp in opportunities[:2]:
            recommendations.append({
                "priority": "opportunity",
                "title": f"机会: {opp['name']}",
                "description": opp['description'],
                "expected_impact": opp['potential_impact']
            })
        
        return recommendations
    
    def export_report(self, report: DemandAnalysisReport, format: str = "yaml") -> str:
        """导出分析报告"""
        report_data = {
            "id": report.id,
            "business_context": report.business_context,
            "summary": {
                "total_signals": len(report.signals),
                "total_demands": len(report.demands),
                "personas_count": len(report.personas),
                "critical_demands": len([d for d in report.demands if d.urgency == DemandUrgency.CRITICAL])
            },
            "key_insights": report.key_insights,
            "prioritized_demands": [
                {
                    "rank": i+1,
                    "id": d.id,
                    "name": d.name,
                    "priority_score": round(d.priority_score, 2),
                    "urgency": d.urgency.value,
                    "type": d.demand_type.value,
                    "frequency": d.frequency
                }
                for i, d in enumerate(report.prioritized_demands[:10])
            ],
            "user_personas": [
                {
                    "id": p.id,
                    "name": p.name,
                    "description": p.description,
                    "demand_strength": p.demand_strength
                }
                for p in report.personas
            ],
            "opportunities": report.opportunities,
            "recommendations": report.recommendations,
            "created_at": report.created_at
        }
        
        if format == "yaml":
            return yaml.dump(report_data, allow_unicode=True, default_flow_style=False)
        else:
            return json.dumps(report_data, ensure_ascii=False, indent=2)
    
    def get_analysis_framework(self) -> Dict:
        """get需求分析框架"""
        return {
            "steps": [
                {"step": 1, "name": "需求信号收集", "description": "从多渠道收集用户行为,反馈,搜索等信号"},
                {"step": 2, "name": "需求recognize", "description": "从信号中recognize和提取具体需求"},
                {"step": 3, "name": "用户画像", "description": "创建目标用户画像并关联需求"},
                {"step": 4, "name": "需求优先级", "description": "根据频率,强度,可服务性排序需求"},
                {"step": 5, "name": "机会recognize", "description": "recognize满足需求的产品机会"},
                {"step": 6, "name": "建议generate", "description": "generate产品优化和增长建议"}
            ]
        }
