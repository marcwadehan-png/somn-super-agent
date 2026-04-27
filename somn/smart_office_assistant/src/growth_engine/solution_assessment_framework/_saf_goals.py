"""solution_assessment_framework 目标生成模块 - 各解决方案目标生成方法"""
# 本文件内容由 solution_assessment_framework.py 拆分而来

from typing import Dict, List

from ._saf_base import ClientContext, DynamicOutcomeRange, PainPointType

__all__ = [
    'generate_crm_goals',
    'generate_digital_operation_goals',
    'generate_douyin_goals',
    'generate_generic_goals',
    'generate_membership_goals',
    'generate_private_domain_goals',
    'generate_xiaohongshu_goals',
]

def generate_private_domain_goals(
    context: ClientContext, factors: Dict[str, float],
    health_score: float, potential_score: float, ambition_level: str
) -> List[Dict]:
    """generate私域运营核心目标"""
    goals = []
    execution_factor = factors.get("execution", 0.7)

    if health_score >= 6:
        goals.append({
            "priority": 1,
            "goal": "构建高价值用户私域池",
            "target": f"私域用户规模增长 {int(50 * execution_factor)}-{int(100 * execution_factor)}%",
            "rationale": f"基于品牌经营健康度({health_score:.1f}/10),具备快速扩张私域的基础,重点在于规模化获客与精细化运营"
        })
        goals.append({
            "priority": 2,
            "goal": "提升私域用户LTV",
            "target": f"私域用户年均消费提升 {int(30 * execution_factor)}-{int(60 * execution_factor)}%",
            "rationale": "基于现有用户基础,通过会员体系与精准营销提升单客价值"
        })
    else:
        goals.append({
            "priority": 1,
            "goal": "建立私域用户基本盘",
            "target": f"核心用户沉淀 {int(20 * execution_factor)}-{int(40 * execution_factor)}%",
            "rationale": f"品牌经营需夯实基础({health_score:.1f}/10),优先建立稳定的私域用户池,再求增长"
        })

    if context.avg_order_value and context.avg_order_value > 500:
        goals.append({
            "priority": 3,
            "goal": "高客单用户深度运营",
            "target": f"高价值用户复购率提升至 {int(40 * execution_factor)}-{int(60 * execution_factor)}%",
            "rationale": f"客单价¥{context.avg_order_value:.0f}较高,适合深度服务与长期关系经营"
        })

    return goals

def generate_membership_goals(
    context: ClientContext, factors: Dict[str, float],
    health_score: float, potential_score: float, ambition_level: str
) -> List[Dict]:
    """generate会员体系核心目标"""
    goals = []
    execution_factor = factors.get("execution", 0.7)

    if context.development_stage == "mature":
        goals.append({
            "priority": 1,
            "goal": "会员精细化分层运营",
            "target": f"会员消费占比提升至 {int(60 * execution_factor)}-{int(80 * execution_factor)}%",
            "rationale": "品牌已进入成熟期,会员体系是提升存量价值的核心抓手"
        })
    else:
        goals.append({
            "priority": 1,
            "goal": "快速建立会员基础",
            "target": f"会员注册率 {int(30 * execution_factor)}-{int(50 * execution_factor)}%",
            "rationale": "品牌处于成长期,优先扩大会员覆盖面,建立用户连接"
        })

    if context.industry in ["航空", "酒店", "餐饮"]:
        goals.append({
            "priority": 2,
            "goal": "会员活跃度提升",
            "target": f"年活跃会员比例 {int(50 * execution_factor)}-{int(70 * execution_factor)}%",
            "rationale": f"{context.industry}行业复购周期较长,保持会员活跃是关键"
        })

    return goals

def generate_digital_operation_goals(
    context: ClientContext, factors: Dict[str, float],
    health_score: float, potential_score: float, ambition_level: str
) -> List[Dict]:
    """generate数字化运营核心目标"""
    goals = []
    execution_factor = factors.get("execution", 0.7)

    if context.team_size and context.team_size > 50:
        goals.append({
            "priority": 1,
            "goal": "运营流程标准化与自动化",
            "target": f"核心流程自动化率 {int(60 * execution_factor)}-{int(80 * execution_factor)}%",
            "rationale": f"团队规模{context.team_size}人,通过数字化提升协同效率是首要目标"
        })
    else:
        goals.append({
            "priority": 1,
            "goal": "关键业务数据化",
            "target": f"核心metrics可视化覆盖 {int(80 * execution_factor)}%+",
            "rationale": "中小团队优先解决数据可见性问题,支撑快速decision"
        })

    goals.append({
        "priority": 2,
        "goal": "decision效率提升",
        "target": f"关键decision响应速度提升 {int(3 * execution_factor)}-{int(5 * execution_factor)}倍",
        "rationale": "通过数据驱动替代经验judge,缩短decision链路"
    })

    return goals

def generate_douyin_goals(
    context: ClientContext, factors: Dict[str, float],
    health_score: float, potential_score: float, ambition_level: str
) -> List[Dict]:
    """generate抖音运营核心目标"""
    goals = []
    execution_factor = factors.get("execution", 0.7)

    if health_score >= 7:
        goals.append({
            "priority": 1,
            "goal": "品牌自播矩阵建设",
            "target": f"月GMV {int(500 * execution_factor)}-{int(1000 * execution_factor)}万",
            "rationale": f"品牌基础良好({health_score:.1f}/10),具备自播能力,重点构建稳定销售渠道"
        })
    else:
        goals.append({
            "priority": 1,
            "goal": "达人种草与品牌曝光",
            "target": f"月曝光 {int(1000 * execution_factor)}-{int(3000 * execution_factor)}万次",
            "rationale": "品牌认知度待提升,优先通过达人合作建立声量"
        })

    return goals

def generate_xiaohongshu_goals(
    context: ClientContext, factors: Dict[str, float],
    health_score: float, potential_score: float, ambition_level: str
) -> List[Dict]:
    """generate小红书运营核心目标"""
    goals = []
    execution_factor = factors.get("execution", 0.7)

    if context.industry in ["美妆", "母婴", "食品"]:
        goals.append({
            "priority": 1,
            "goal": "种草内容矩阵建设",
            "target": f"月均优质笔记 {int(100 * execution_factor)}-{int(200 * execution_factor)}篇",
            "rationale": f"{context.industry}品类在小红书有天然内容优势,重点构建种草能力"
        })

    goals.append({
        "priority": 2,
        "goal": "搜索占位与转化",
        "target": f"核心品类搜索排名 TOP{int(10 / execution_factor)}",
        "rationale": "小红书已成为消费decision入口,搜索占位直接影响转化"
    })

    return goals

def generate_crm_goals(
    context: ClientContext, factors: Dict[str, float],
    health_score: float, potential_score: float, ambition_level: str
) -> List[Dict]:
    """generateCRM系统核心目标"""
    goals = []
    execution_factor = factors.get("execution", 0.7)

    goals.append({
        "priority": 1,
        "goal": "销售流程标准化",
        "target": f"销售漏斗可视化率 {int(90 * execution_factor)}%+",
        "rationale": "建立标准化的客户跟进流程,提升销售可预测性"
    })
    goals.append({
        "priority": 2,
        "goal": "客户数据资产化",
        "target": f"客户信息完整度 {int(80 * execution_factor)}%+",
        "rationale": "构建完整的客户画像,支撑精准营销与服务"
    })

    return goals

def generate_generic_goals(
    context: ClientContext, factors: Dict[str, float],
    health_score: float, potential_score: float, ambition_level: str
) -> List[Dict]:
    """generate通用核心目标"""
    goals = []
    execution_factor = factors.get("execution", 0.7)

    goals.append({
        "priority": 1,
        "goal": f"{ambition_level}增长目标",
        "target": f"核心业务metrics提升 {int(20 * execution_factor)}-{int(50 * execution_factor)}%",
        "rationale": f"基于synthesize评估(经营健康度{health_score:.1f}/10, 增长潜力{potential_score:.1f}/10),设定{ambition_level}目标"
    })

    return goals
