"""
__all__ = [
    'get_benchmarks',
    'get_industry',
    'get_playbooks',
    'list_industries',
    'match_industry',
    'to_dict',
    'BusinessModel',
    'IndustryProfile',
    'GrowthPlaybook',
    'IndustryKnowledgeBase',
]

行业知识库 - 管理行业特定的增长知识和最佳实践

[v22.1 统一入口] IndustryType从industry_engine统一导入，避免重复定义
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

# [v22.1 统一入口] 从industry_engine统一导入，避免17处重复定义
# 相对导入层级：knowledge_graph(0) → src(..) → industry_engine(..)
# 正确用法：..industry_engine（向上2级），而非 ...industry_engine（向上3级，越界）
try:
    from ..industry_engine import IndustryType
except ImportError:
    from enum import Enum as EnumBase
    IndustryType = EnumBase('IndustryType', {'ECOMMERCE': 'ecommerce'})  # 兜底

class BusinessModel(Enum):
    """商业模式"""
    B2C = "b2c"                       # 企业对消费者
    B2B = "b2b"                       # 企业对企业
    B2B2C = "b2b2c"                   # 平台模式
    C2C = "c2c"                       # 消费者对消费者
    SUBSCRIPTION = "subscription"     # 订阅制
    MARKETPLACE = "marketplace"       # 交易平台

@dataclass
class IndustryProfile:
    """行业画像"""
    industry_type: IndustryType
    name: str
    business_models: List[BusinessModel] = field(default_factory=list)
    key_metrics: List[str] = field(default_factory=list)
    growth_strategies: List[str] = field(default_factory=list)
    typical_channels: List[str] = field(default_factory=list)
    user_behavior_patterns: Dict[str, Any] = field(default_factory=dict)
    competitive_landscape: List[str] = field(default_factory=list)
    regulatory_factors: List[str] = field(default_factory=list)
    seasonality: Dict[str, Any] = field(default_factory=dict)
    case_studies: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            'industry_type': self.industry_type.value,
            'name': self.name,
            'business_models': [bm.value for bm in self.business_models],
            'key_metrics': self.key_metrics,
            'growth_strategies': self.growth_strategies,
            'typical_channels': self.typical_channels,
            'user_behavior_patterns': self.user_behavior_patterns,
            'competitive_landscape': self.competitive_landscape,
            'regulatory_factors': self.regulatory_factors,
            'seasonality': self.seasonality,
            'case_studies': self.case_studies,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

@dataclass
class GrowthPlaybook:
    """增长strategy手册"""
    playbook_id: str
    name: str
    industry: IndustryType
    stage: str  # 阶段: 初创/成长/成熟
    objectives: List[str] = field(default_factory=list)
    strategies: List[Dict] = field(default_factory=list)
    tactics: List[Dict] = field(default_factory=list)
    expected_outcomes: Dict[str, Any] = field(default_factory=dict)
    success_cases: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

class IndustryKnowledgeBase:
    """行业知识库"""
    
    def __init__(self, graph_engine=None):
        self.graph_engine = graph_engine
        self.industries: Dict[IndustryType, IndustryProfile] = {}
        self.playbooks: Dict[str, GrowthPlaybook] = {}
        
        # init行业数据
        self._init_industries()
        self._init_playbooks()
    
    def _init_industries(self):
        """init行业数据"""
        industries_data = [
            {
                'industry_type': IndustryType.ECOMMERCE,
                'name': '电商零售',
                'business_models': [BusinessModel.B2C, BusinessModel.B2B2C, BusinessModel.MARKETPLACE],
                'key_metrics': ['GMV', '转化率', '客单价', '复购率', '获客成本', '库存周转'],
                'growth_strategies': [
                    '品类扩张', '私域流量运营', '直播带货', '会员体系',
                    '供应链优化', '跨境电商', '下沉市场'
                ],
                'typical_channels': [
                    '搜索引擎', '社交媒体', 'KOL合作', '信息流广告',
                    '私域社群', '线下门店', '异业合作'
                ],
                'user_behavior_patterns': {
                    'decision_cycle': '短(冲动消费)',
                    'price_sensitivity': '高',
                    'loyalty': '低(易比价)',
                    'seasonality': '强(大促节点)'
                },
                'seasonality': {
                    'peak_periods': ['618', '双11', '双12', '年货节'],
                    'low_periods': ['春节后', '7-8月'],
                    'preparation_lead_time': '1-2个月'
                }
            },
            {
                'industry_type': IndustryType.SAAS_B2B,
                'name': 'SaaS软件',
                'business_models': [BusinessModel.B2B, BusinessModel.SUBSCRIPTION],
                'key_metrics': ['MRR', 'ARR', 'CAC', 'LTV', 'Churn Rate', 'NRR', 'NPS'],
                'growth_strategies': [
                    '产品主导增长(PLG)', '销售主导增长(SLG)',
                    '客户成功驱动', '生态合作伙伴',
                    '垂直行业深耕', '国际化扩张'
                ],
                'typical_channels': [
                    '内容营销', 'SEO/SEM', '销售团队', '合作伙伴',
                    '产品内推荐', '行业会议', '客户推荐'
                ],
                'user_behavior_patterns': {
                    'decision_cycle': '长(多轮评估)',
                    'price_sensitivity': '中(看ROI)',
                    'loyalty': '高(迁移成本高)',
                    'seasonality': '弱(Q4预算冲刺)'
                }
            },
            {
                'industry_type': IndustryType.CONTENT_GAMING,
                'name': '内容媒体',
                'business_models': [BusinessModel.B2C, BusinessModel.B2B2C, BusinessModel.SUBSCRIPTION],
                'key_metrics': ['DAU/MAU', '停留时长', '完播率', '互动率', '广告收入', '付费转化率'],
                'growth_strategies': [
                    '算法推荐优化', '创作者生态', '内容品类扩张',
                    '社交化互动', 'IP孵化', '多平台分发'
                ],
                'typical_channels': [
                    '应用商店', '社交分享', '搜索引擎', '预装合作',
                    '跨平台引流', 'KOL合作'
                ],
                'user_behavior_patterns': {
                    'decision_cycle': '极短(即时消费)',
                    'price_sensitivity': '低(免费为主)',
                    'loyalty': '中(看内容质量)',
                    'seasonality': '弱(热点驱动)'
                }
            },
            {
                'industry_type': IndustryType.LOCAL_LIFE,
                'name': '本地生活',
                'business_models': [BusinessModel.B2C, BusinessModel.B2B2C, BusinessModel.MARKETPLACE],
                'key_metrics': ['订单量', 'GTV', '商户数', '骑手效率', '配送时效', '用户频次'],
                'growth_strategies': [
                    '地推扩张', '补贴大战', '会员体系',
                    '场景渗透(外卖/到店/酒旅)', '下沉市场', '即时零售'
                ],
                'typical_channels': [
                    '地推团队', '广告投放', '商户推荐', '用户裂变',
                    '异业合作', 'LBS推送'
                ],
                'user_behavior_patterns': {
                    'decision_cycle': '极短(即时需求)',
                    'price_sensitivity': '极高',
                    'loyalty': '低(补贴敏感)',
                    'seasonality': '中(用餐高峰)'
                },
                'seasonality': {
                    'peak_periods': ['午餐高峰', '晚餐高峰', '周末'],
                    'low_periods': ['凌晨', '工作日下午'],
                    'daily_pattern': '三餐高峰明显'
                }
            },
            {
                'industry_type': IndustryType.FINTECH,
                'name': '金融科技',
                'business_models': [BusinessModel.B2C, BusinessModel.B2B],
                'key_metrics': ['AUM', '交易笔数', '坏账率', '获客成本', '用户留存', 'ARPU'],
                'growth_strategies': [
                    '场景金融', '风控模型优化', '产品矩阵',
                    '合规先行', '科技输出', '生态合作'
                ],
                'typical_channels': [
                    '应用商店', '场景嵌入', '品牌广告', '内容营销',
                    '线下网点', '合作伙伴导流'
                ],
                'user_behavior_patterns': {
                    'decision_cycle': '长(信任建立)',
                    'price_sensitivity': '中(看收益/费率)',
                    'loyalty': '高(资金沉淀)',
                    'seasonality': '弱(理财周期)'
                },
                'regulatory_factors': [
                    '牌照要求', '资金存管', '信息披露',
                    '反洗钱', '数据安全', '利率上限'
                ]
            }
        ]
        
        for data in industries_data:
            profile = IndustryProfile(**data)
            self.industries[profile.industry_type] = profile
            
            # 同步到图谱
            if self.graph_engine:
                from .graph_engine import NodeType
                self.graph_engine.add_node(
                    name=profile.name,
                    node_type=NodeType.INDUSTRY,
                    properties=profile.to_dict()
                )
    
    def _init_playbooks(self):
        """init增长strategy手册"""
        playbooks_data = [
            {
                'playbook_id': 'ecommerce_early',
                'name': '电商初创期增长手册',
                'industry': IndustryType.ECOMMERCE,
                'stage': '初创',
                'objectives': ['验证PMF', 'get首批用户', '建立供应链'],
                'strategies': [
                    {'name': '单品爆款strategy', 'priority': '高', 'timeline': '1-3个月'},
                    {'name': '私域冷启动', 'priority': '高', 'timeline': '1-2个月'},
                    {'name': 'KOC种草', 'priority': '中', 'timeline': '持续'}
                ],
                'tactics': [
                    {'name': '小红书种草', 'channel': '社交媒体', 'budget': '低'},
                    {'name': '微信群运营', 'channel': '私域', 'budget': '低'},
                    {'name': '抖音直播', 'channel': '直播', 'budget': '中'}
                ],
                'expected_outcomes': {
                    'users': '1000-10000',
                    'gmv': '10万-100万/月',
                    'timeline': '3-6个月'
                }
            },
            {
                'playbook_id': 'saas_plg',
                'name': 'SaaS产品主导增长(PLG)手册',
                'industry': IndustryType.SAAS_B2B,
                'stage': '成长',
                'objectives': ['降低CAC', '提高产品采用率', '建立病毒传播'],
                'strategies': [
                    {'name': '免费增值模式', 'priority': '高', 'timeline': '持续'},
                    {'name': '产品内病毒机制', 'priority': '高', 'timeline': '1-2个月'},
                    {'name': '自助服务优化', 'priority': '中', 'timeline': '持续'}
                ],
                'tactics': [
                    {'name': '免费版功能设计', 'channel': '产品内', 'budget': '开发成本'},
                    {'name': '模板市场', 'channel': '产品内', 'budget': '中'},
                    {'name': '邀请奖励', 'channel': '产品内', 'budget': '低'}
                ],
                'expected_outcomes': {
                    'viral_coefficient': '>0.5',
                    'free_to_paid': '10-20%',
                    'nrr': '>100%'
                }
            },
            {
                'playbook_id': 'content_algorithm',
                'name': '内容平台算法驱动增长手册',
                'industry': IndustryType.CONTENT_GAMING,
                'stage': '成长',
                'objectives': ['提升留存', '增加时长', '扩大DAU'],
                'strategies': [
                    {'name': '推荐算法优化', 'priority': '高', 'timeline': '持续'},
                    {'name': '创作者激励', 'priority': '高', 'timeline': '持续'},
                    {'name': '社交裂变', 'priority': '中', 'timeline': '1-3个月'}
                ],
                'tactics': [
                    {'name': '冷启动流量池', 'channel': '算法', 'budget': '低'},
                    {'name': '创作者分成', 'channel': '生态', 'budget': '高'},
                    {'name': '分享得金币', 'channel': '社交', 'budget': '中'}
                ],
                'expected_outcomes': {
                    'dau_mau': '>30%',
                    'avg_session': '>15分钟',
                    'retention_d7': '>20%'
                }
            }
        ]
        
        for data in playbooks_data:
            playbook = GrowthPlaybook(**data)
            self.playbooks[playbook.playbook_id] = playbook
    
    def get_industry(self, industry_type: IndustryType) -> Optional[IndustryProfile]:
        """get行业画像"""
        return self.industries.get(industry_type)
    
    def list_industries(self) -> List[IndustryType]:
        """列出所有行业"""
        return list(self.industries.keys())
    
    def get_playbooks(self, industry: IndustryType = None, stage: str = None) -> List[GrowthPlaybook]:
        """getstrategy手册"""
        results = []
        for playbook in self.playbooks.values():
            if industry and playbook.industry != industry:
                continue
            if stage and playbook.stage != stage:
                continue
            results.append(playbook)
        return results
    
    def match_industry(self, description: str) -> List[IndustryType]:
        """根据描述匹配行业"""
        keywords_map = {
            IndustryType.ECOMMERCE: ['电商', '零售', '购物', '商品', '卖家', '买家'],
            IndustryType.SAAS_B2B: ['软件', 'SaaS', '企业服务', '订阅', '工具'],
            IndustryType.CONTENT_GAMING: ['内容', '媒体', '视频', '直播', '资讯', '社区'],
            IndustryType.LOCAL_LIFE: ['本地', '外卖', '到店', '餐饮', '生活服务'],
            IndustryType.FINTECH: ['金融', '支付', '理财', '贷款', '保险', '银行']
        }
        
        scores = {}
        for industry, keywords in keywords_map.items():
            score = sum(1 for kw in keywords if kw in description)
            if score > 0:
                scores[industry] = score
        
        # 按匹配度排序
        return sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    
    def get_benchmarks(self, industry_type: IndustryType) -> Dict[str, Any]:
        """get行业基准数据"""
        benchmarks = {
            IndustryType.ECOMMERCE: {
                'conversion_rate': {'median': 0.02, 'top': 0.05},
                'cart_abandonment': {'median': 0.70, 'target': 0.60},
                'customer_acquisition_cost': {'median': 50, 'target': 30},
                'repeat_purchase_rate': {'median': 0.25, 'top': 0.40}
            },
            IndustryType.SAAS_B2B: {
                'monthly_churn': {'median': 0.05, 'target': 0.03},
                'annual_churn': {'median': 0.20, 'target': 0.10},
                'ltv_cac_ratio': {'median': 3, 'target': 5},
                'nrr': {'median': 1.0, 'top': 1.2}
            },
            IndustryType.CONTENT_GAMING: {
                'dau_mau': {'median': 0.20, 'top': 0.35},
                'avg_session_minutes': {'median': 8, 'top': 20},
                'content_completion_rate': {'median': 0.30, 'top': 0.60}
            }
        }
        
        return benchmarks.get(industry_type, {})
