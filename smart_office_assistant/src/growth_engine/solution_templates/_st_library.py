"""解决方案模板库核心类"""

from typing import Dict, List, Optional

from ._st_enums import SolutionType, SolutionCategory
from ._st_dataclasses import AssessmentParameter, DynamicMetric, SolutionTemplateV2

__all__ = [
    'get_assessment_parameters',
    'get_dynamic_metrics',
    'get_template',
    'list_templates',
]

class SolutionTemplateLibraryV2:
    """解决方案模板库 V2"""
    
    def __init__(self):
        self.templates: Dict[SolutionType, SolutionTemplateV2] = {}
        self._init_templates()
    
    def _init_templates(self):
        """init_all解决方案模板"""
        
        # ========== 私域运营 ==========
        self.templates[SolutionType.PRIVATE_DOMAIN] = SolutionTemplateV2(
            solution_id="private_domain_v2",
            solution_type=SolutionType.PRIVATE_DOMAIN,
            name="私域流量运营体系",
            category=SolutionCategory.RETENTION,
            description="构建品牌自有流量池,通过精细化运营提升用户LTV,降低获客成本",
            applicable_industries=["电商", "零售", "美妆", "母婴", "教育", "健身"],
            applicable_stages=["成长", "成熟"],
            applicable_scales=["中型", "大型"],
            
            # 评估参数定义
            required_parameters=[
                AssessmentParameter(
                    param_name="industry",
                    param_type="str",
                    description="所属行业",
                    required=True,
                    options=["电商", "零售", "美妆", "母婴", "教育", "健身", "餐饮", "其他"]
                ),
                AssessmentParameter(
                    param_name="avg_order_value",
                    param_type="float",
                    description="平均客单价(元)",
                    required=True,
                    valid_range=(10, 10000)
                ),
                AssessmentParameter(
                    param_name="current_cac",
                    param_type="float",
                    description="当前获客成本(元)",
                    required=False,
                    valid_range=(1, 5000)
                ),
                AssessmentParameter(
                    param_name="current_retention_rate",
                    param_type="float",
                    description="当前留存率(%)",
                    required=False,
                    valid_range=(0, 100)
                ),
                AssessmentParameter(
                    param_name="execution_capability",
                    param_type="float",
                    description="执行能力评分(1-10分)",
                    required=True,
                    default_value=5.0,
                    valid_range=(1, 10)
                ),
                AssessmentParameter(
                    param_name="team_size",
                    param_type="int",
                    description="运营团队规模",
                    required=False,
                    valid_range=(1, 1000)
                ),
                AssessmentParameter(
                    param_name="primary_pain_points",
                    param_type="list",
                    description="主要痛点",
                    required=True,
                    options=["获客成本高", "用户留存低", "转化率低", "缺乏运营体系", "数据孤岛"]
                ),
            ],
            
            # 动态metrics定义
            dynamic_metrics=[
                DynamicMetric(
                    metric_id="cac_reduction",
                    metric_name="获客成本降低",
                    unit="%",
                    industry_baselines={
                        "美妆": {"low": 20, "typical": 35, "high": 55},
                        "母婴": {"low": 15, "typical": 30, "high": 45},
                        "电商": {"low": 15, "typical": 30, "high": 50},
                        "零售": {"low": 10, "typical": 25, "high": 40},
                        "教育": {"low": 15, "typical": 30, "high": 50},
                        "健身": {"low": 20, "typical": 35, "high": 50},
                    },
                    factor_weights={
                        "execution_capability": 0.3,
                        "team_size": 0.2,
                        "industry": 0.25,
                        "pain_point_match": 0.25
                    },
                    assessment_notes="基于行业基准,结合执行能力和痛点匹配度动态计算"
                ),
                DynamicMetric(
                    metric_id="ltv_lift",
                    metric_name="用户LTV提升",
                    unit="%",
                    industry_baselines={
                        "美妆": {"low": 30, "typical": 60, "high": 120},
                        "母婴": {"low": 25, "typical": 50, "high": 100},
                        "电商": {"low": 20, "typical": 50, "high": 100},
                        "零售": {"low": 15, "typical": 40, "high": 80},
                        "教育": {"low": 25, "typical": 55, "high": 110},
                        "健身": {"low": 30, "typical": 60, "high": 100},
                    },
                    factor_weights={
                        "execution_capability": 0.35,
                        "avg_order_value": 0.25,
                        "industry": 0.2,
                        "pain_point_match": 0.2
                    },
                    assessment_notes="客单价越高,LTV提升空间通常越大"
                ),
                DynamicMetric(
                    metric_id="conversion_rate",
                    metric_name="私域转化率",
                    unit="%",
                    industry_baselines={
                        "美妆": {"low": 8, "typical": 15, "high": 25},
                        "母婴": {"low": 5, "typical": 12, "high": 20},
                        "电商": {"low": 5, "typical": 10, "high": 18},
                        "零售": {"low": 3, "typical": 8, "high": 15},
                        "教育": {"low": 6, "typical": 12, "high": 20},
                        "健身": {"low": 8, "typical": 15, "high": 22},
                    },
                    factor_weights={
                        "execution_capability": 0.4,
                        "industry": 0.3,
                        "team_size": 0.3
                    },
                    assessment_notes="私域转化率通常高于公域2-3倍"
                ),
                DynamicMetric(
                    metric_id="user_growth",
                    metric_name="私域用户年增长",
                    unit="%",
                    industry_baselines={
                        "default": {"low": 50, "typical": 150, "high": 300},
                    },
                    factor_weights={
                        "execution_capability": 0.4,
                        "budget": 0.3,
                        "market_competition": 0.3
                    },
                    assessment_notes="取决于引流预算和执行效率"
                ),
            ],
            
            core_strategies=[
                {
                    "name": "全域引流",
                    "description": "从公域平台引流至私域",
                    "tactics": ["包裹卡引流", "AI外呼加微", "直播间引导", "内容种草"],
                    "applicable_pains": ["获客成本高"]
                },
                {
                    "name": "分层运营",
                    "description": "基于用户价值分层,差异化运营strategy",
                    "tactics": ["RFM分层", "生命周期分层", "兴趣标签分层"],
                    "applicable_pains": ["用户留存低", "转化率低"]
                },
                {
                    "name": "内容触达",
                    "description": "通过优质内容持续触达用户,建立信任",
                    "tactics": ["朋友圈运营", "社群内容", "1V1服务", "视频号直播"],
                    "applicable_pains": ["用户留存低"]
                },
                {
                    "name": "转化变现",
                    "description": "私域场景下的成交转化",
                    "tactics": ["社群团购", "直播带货", "会员专享", "限时秒杀"],
                    "applicable_pains": ["转化率低"]
                }
            ],
            
            implementation_steps=[
                {"step": 1, "name": "私域基建", "duration": "2-4周", "tasks": ["企微SCRM部署", "标签体系设计", "内容库搭建"]},
                {"step": 2, "name": "引流获客", "duration": "持续", "tasks": ["设计引流钩子", "全渠道布点", "自动化欢迎语"]},
                {"step": 3, "name": "用户分层", "duration": "2周", "tasks": ["RFM模型搭建", "自动化标签", "分层strategy制定"]},
                {"step": 4, "name": "内容运营", "duration": "持续", "tasks": ["内容日历规划", "SOP标准化", "IP人设打造"]},
                {"step": 5, "name": "转化优化", "duration": "持续", "tasks": ["成交话术优化", "活动节奏设计", "复购机制搭建"]}
            ],
            
            required_resources={
                "team": ["私域运营经理", "内容运营", "社群运营", "客服"],
                "budget_range": {"min": 10, "max": 50, "unit": "万/年"},
                "tools": ["企业微信", "SCRM系统", "小程序商城"]
            },
            
            common_pitfalls=[
                "盲目追求用户规模,忽视质量",
                "过度营销导致用户流失",
                "缺乏系统化运营SOP",
                "私域与公域割裂运营"
            ],
            
            recommended_tools=["企业微信", "有赞", "微盟", "圈量", "句子互动"],
            
            case_studies=[
                {
                    "company": "完美日记",
                    "industry": "美妆",
                    "context": {"客单价": 120, "执行能力": "强"},
                    "result": "私域用户超3000万,私域GMV占比超30%",
                    "key_tactics": ["小完子IP", "社群精细化运营", "小程序商城闭环"]
                },
                {
                    "company": "瑞幸咖啡",
                    "industry": "餐饮",
                    "context": {"客单价": 25, "执行能力": "强"},
                    "result": "私域用户超1亿,复购率提升30%",
                    "key_tactics": ["LBS精准推送", "社群秒杀", "企微1V1服务"]
                }
            ]
        )
        
        # ========== 会员体系 ==========
        self.templates[SolutionType.MEMBERSHIP] = SolutionTemplateV2(
            solution_id="membership_v2",
            solution_type=SolutionType.MEMBERSHIP,
            name="会员体系设计与运营",
            category=SolutionCategory.RETENTION,
            description="构建多层级会员体系,通过权益设计提升用户忠诚度和消费频次",
            applicable_industries=["电商", "零售", "餐饮", "美妆", "母婴", "航空", "酒店"],
            applicable_stages=["成长", "成熟"],
            applicable_scales=["中型", "大型"],
            
            required_parameters=[
                AssessmentParameter(
                    param_name="industry",
                    param_type="str",
                    description="所属行业",
                    required=True
                ),
                AssessmentParameter(
                    param_name="avg_order_value",
                    param_type="float",
                    description="平均客单价(元)",
                    required=True
                ),
                AssessmentParameter(
                    param_name="purchase_frequency",
                    param_type="float",
                    description="当前购买频次(次/年)",
                    required=False,
                    valid_range=(0, 365)
                ),
                AssessmentParameter(
                    param_name="current_retention_rate",
                    param_type="float",
                    description="当前留存率(%)",
                    required=False
                ),
                AssessmentParameter(
                    param_name="execution_capability",
                    param_type="float",
                    description="执行能力评分(1-10分)",
                    required=True,
                    default_value=5.0
                ),
                AssessmentParameter(
                    param_name="primary_pain_points",
                    param_type="list",
                    description="主要痛点",
                    required=True,
                    options=["用户留存低", "复购率低", "用户忠诚度低", "缺乏会员体系"]
                ),
            ],
            
            dynamic_metrics=[
                DynamicMetric(
                    metric_id="penetration_rate",
                    metric_name="会员渗透率",
                    unit="%",
                    industry_baselines={
                        "零售": {"low": 20, "typical": 40, "high": 60},
                        "餐饮": {"low": 25, "typical": 50, "high": 70},
                        "航空": {"low": 30, "typical": 55, "high": 75},
                        "酒店": {"low": 25, "typical": 50, "high": 70},
                        "美妆": {"low": 20, "typical": 45, "high": 65},
                    },
                    factor_weights={
                        "execution_capability": 0.4,
                        "industry": 0.3,
                        "purchase_frequency": 0.3
                    },
                    assessment_notes="高频消费行业会员渗透率通常更高"
                ),
                DynamicMetric(
                    metric_id="arpu_lift",
                    metric_name="会员ARPU提升倍数",
                    unit="倍",
                    industry_baselines={
                        "零售": {"low": 1.5, "typical": 3.0, "high": 5.0},
                        "餐饮": {"low": 1.3, "typical": 2.5, "high": 4.0},
                        "航空": {"low": 2.0, "typical": 4.0, "high": 6.0},
                        "酒店": {"low": 1.8, "typical": 3.5, "high": 5.5},
                        "美妆": {"low": 1.6, "typical": 3.2, "high": 5.0},
                    },
                    factor_weights={
                        "execution_capability": 0.35,
                        "avg_order_value": 0.25,
                        "industry": 0.25,
                        "pain_point_match": 0.15
                    },
                    assessment_notes="会员ARPU通常是非会员的2-5倍"
                ),
                DynamicMetric(
                    metric_id="retention_lift",
                    metric_name="会员留存率提升",
                    unit="%",
                    industry_baselines={
                        "default": {"low": 15, "typical": 30, "high": 50},
                    },
                    factor_weights={
                        "execution_capability": 0.4,
                        "current_retention_rate": 0.3,
                        "industry": 0.3
                    },
                    assessment_notes="会员留存率通常比非会员高20-50%"
                ),
            ],
            
            core_strategies=[
                {
                    "name": "等级设计",
                    "description": "设计合理的会员等级和成长路径",
                    "tactics": ["消费积分制", "任务成长制", "付费会员制", "邀请升级制"],
                    "applicable_pains": ["缺乏会员体系"]
                },
                {
                    "name": "权益包装",
                    "description": "设计有吸引力的会员专属权益",
                    "tactics": ["价格权益", "服务权益", "内容权益", "身份权益"],
                    "applicable_pains": ["用户忠诚度低"]
                },
                {
                    "name": "生命周期运营",
                    "description": "针对不同会员生命周期的运营strategy",
                    "tactics": ["新会员激活", "成长会员培育", "高价值会员维护", "流失会员召回"],
                    "applicable_pains": ["用户留存低", "复购率低"]
                }
            ],
            
            implementation_steps=[
                {"step": 1, "name": "会员体系设计", "duration": "2-4周", "tasks": ["等级体系设计", "权益体系设计", "成长规则设计"]},
                {"step": 2, "name": "系统开发", "duration": "4-8周", "tasks": ["会员系统开发", "积分系统开发", "权益核销系统"]},
                {"step": 3, "name": "冷启动", "duration": "2-4周", "tasks": ["老用户等级init", "种子会员招募", "内测优化"]},
                {"step": 4, "name": "全面推广", "duration": "持续", "tasks": ["全渠道推广", "会员日活动", "联合权益拓展"]}
            ],
            
            required_resources={
                "team": ["会员运营经理", "产品经理", "开发工程师", "数据分析师"],
                "budget_range": {"min": 20, "max": 100, "unit": "万"},
                "tools": ["会员系统", "积分系统", "BI工具"]
            },
            
            common_pitfalls=[
                "等级设计过于复杂,用户难以理解",
                "权益缺乏吸引力,会员价值感低",
                "积分体系通胀,贬值严重",
                "会员运营与业务目标脱节"
            ],
            
            recommended_tools=["有赞会员", "微盟会员", "Salesforce", "SAP"],
            
            case_studies=[
                {
                    "company": "奈雪的茶",
                    "industry": "茶饮",
                    "context": {"客单价": 35, "执行能力": "强"},
                    "result": "会员超5000万,会员订单占比超70%",
                    "key_tactics": ["付费会员卡", "积分商城", "生日特权"]
                }
            ]
        )
        
        # 可以继续添加其他解决方案模板...
    
    def get_template(self, solution_type: SolutionType) -> Optional[SolutionTemplateV2]:
        """get解决方案模板"""
        return self.templates.get(solution_type)
    
    def list_templates(self, 
                       category: Optional[SolutionCategory] = None,
                       industry: Optional[str] = None) -> List[SolutionTemplateV2]:
        """列出所有模板,支持筛选"""
        results = list(self.templates.values())
        
        if category:
            results = [t for t in results if t.category == category]
        
        if industry:
            results = [t for t in results if industry in t.applicable_industries or "全品类" in t.applicable_industries]
        
        return results
    
    def get_assessment_parameters(self, solution_type: SolutionType) -> List[AssessmentParameter]:
        """get解决方案的评估参数定义"""
        template = self.get_template(solution_type)
        if not template:
            return []
        return template.required_parameters
    
    def get_dynamic_metrics(self, solution_type: SolutionType) -> List[DynamicMetric]:
        """get解决方案的动态metrics定义"""
        template = self.get_template(solution_type)
        if not template:
            return []
        return template.dynamic_metrics


# 别名：兼容 V1 名称（由 growth_engine 的 __getattr__ 引用）
SolutionTemplateLibrary = SolutionTemplateLibraryV2
