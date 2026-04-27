"""
__all__ = [
    'calculate_strategic_confidence',
    'detect_strategic',
    'init_strategic_detection_patterns',
    'init_strategic_fallacies',
]

战略咨询谬误库与检测 (v5.1)
"""

from typing import Dict, List
from ._fd_types import FallacyCategory, FallacyDetection
from datetime import datetime
import re

def init_strategic_fallacies() -> Dict[str, Dict]:
    """
    初始化战略咨询专用谬误库

    这些谬误在商业战略咨询场景中高频出现,但传统逻辑学谬误库未覆盖.
    基于咨询项目暴露的30+项不足抽象而来.
    """
    return {
        # --- 认知层谬误 ---
        'goal_driven_planning': {
            'name': '目标驱动型规划',
            'category': FallacyCategory.STRATEGIC,
            'description': '先设定雄心勃勃的增长目标(如"十倍增长"),再从目标反推路径,完全忽略企业的实际约束条件和市场天花板.本质是"颠倒因果"--目标应该是推理的结果,而非推理的前提.',
            'example': '目标从1亿做到10亿,为此我们需要六大增长引擎齐头并进...',
            'correction': '从企业能力边界(产能/人才/资金)和市场天花板出发,反推合理目标范围.目标应是约束分析的输出,而非输入.',
            'severity': 'critical'
        },
        'confirmation_bias_strategy': {
            'name': '战略确认偏差',
            'category': FallacyCategory.STRATEGIC,
            'description': '在战略分析中只搜索和呈现支持增长假设的证据,系统性忽略不利数据,行业增速放缓,竞争格局恶化等反向信号.',
            'example': '市场高速增长(仅引用乐观数据),蓝海机会巨大(忽略红海竞争),对标品牌成功验证了可行性(忽略失败案例)...',
            'correction': '主动搜索并呈现与核心假设相矛盾的证据.每个增长假设都必须有对应的"证伪条件".',
            'severity': 'critical'
        },
        'false_analogy_strategy': {
            'name': '战略错误类比',
            'category': FallacyCategory.STRATEGIC,
            'description': '引用成功企业的案例(如"简一陶瓷从2亿到10亿")作为可行性的证据,但不分析两个企业在行业属性,市场阶段,品牌定位,资源禀赋等关键条件上的差异.',
            'example': '参考行业成功经验,企业也能实现增长...',
            'correction': '对标分析必须包含:①核心差异列表 ②差异对方法论适用性的影响 ③哪些经验可迁移,哪些不可迁移',
            'severity': 'major'
        },
        'brand_growth_contradiction': {
            'name': '品牌心智与增长来源矛盾',
            'category': FallacyCategory.STRATEGIC,
            'description': '品牌核心心智是"高端/稀缺/非遗/收藏",但主要增长来源依赖"规模化/大众化/量产".消费者的认知中品牌代表稀缺,而战略要求品牌走向大众,二者根本不相容.',
            'example': '品牌以传统文化非遗为核心资产(高端/稀缺),同时规划大规模电商下沉(大众/量产)...',
            'correction': '明确品牌战略路径:要么走爱马仕路线(稀缺驱动高溢价),要么走无印良品路线(规模驱动低毛利),不要试图同时做两件事.如果必须双轨,必须用完全隔离的子品牌.',
            'severity': 'critical'
        },
        'narrative_blindness': {
            'name': '叙事蒙蔽',
            'category': FallacyCategory.STRATEGIC,
            'description': '被自己构建的宏大叙事("数字化生态矩阵""全链路闭环""赋能体系")说服,以为提出了方案就等于解决了问题,忽视了每个概念都需要转化为具体的执action作.',
            'example': '构建全链路数字化生态矩阵,打造私域+公域+跨界赋能体系,实现品效合一的闭环增长...',
            'correction': '每个概念必须拆解为:具体做什么→谁来做→需要什么资源→预期什么效果→怎么衡量成功.',
            'severity': 'major'
        },

        # --- 输出层谬误 ---
        'concept_stacking': {
            'name': '概念堆砌',
            'category': FallacyCategory.STRATEGIC,
            'description': '用一连串高大上的概念(生态,矩阵,闭环,赋能,全链路,数字化)替代具体的action方案.读起来很专业,但实际上无法执行.',
            'example': '建设数字化私域生态矩阵,实现全链路用户赋能和品效闭环...',
            'correction': '将每个抽象概念替换为具体action.例如"私域生态矩阵"→"建立企业微信社群,每月4次活动,首年覆盖5000用户".',
            'severity': 'major'
        },
        'number_game': {
            'name': '数字游戏',
            'category': FallacyCategory.STRATEGIC,
            'description': '使用精确数字("3年达到5.2亿营收""转化率提升18.7%")制造专业感,但这些数字没有测算逻辑,没有数据来源,无法追溯推导过程.',
            'example': '预计第三年营收达到5.2亿,第四年突破8.1亿...',
            'correction': '每个关键数字必须附带:①测算公式/模型 ②数据来源 ③关键假设 ④敏感性分析.',
            'severity': 'major'
        },
        'slogan_planning': {
            'name': '口号式规划',
            'category': FallacyCategory.STRATEGIC,
            'description': '有方向性描述("打造XX体系""构建XX矩阵""建设XX平台")但没有具体的执行方案--无团队配置,无预算分配,无KPImetrics,无时间节点.',
            'example': '打造全渠道数字化营销体系,建设品牌私域流量池...',
            'correction': '为每个规划方向补充五要素:负责人,团队配置,预算,KPI,里程碑时间节点.',
            'severity': 'major'
        },
        'hollow_risk_management': {
            'name': '空洞风控',
            'category': FallacyCategory.STRATEGIC,
            'description': 'recognize了风险类别("财务风险""供应链风险""品牌风险"),但应对措施都是原则性口号("加强风控""优化供应链""维护品牌"),没有可落地的应急预案,止损触发条件和资源调整方案.',
            'example': '风险应对:建立完善的风险管理体系,加强财务监控,优化供应链管理...',
            'correction': '为每个风险设计具体的应急预案:预警metrics→触发条件→应对动作→责任人→止损线.',
            'severity': 'major'
        },
        'fake_validation': {
            'name': '走过场验证',
            'category': FallacyCategory.STRATEGIC,
            'description': '声称做了验证("已进行市场调研""经过可行性分析"),但实际上验证过程不深入,不系统,只是走个形式来增加方案的可信度.',
            'example': '经过深入的市场调研和可行性分析,我们认为该方案切实可行...',
            'correction': '验证必须是可追溯的:调研方法→样本量→关键发现→数据来源→验证结论→局限性.',
            'severity': 'moderate'
        },
        'omni_channel_price_conflict': {
            'name': '全渠道价格冲突',
            'category': FallacyCategory.STRATEGIC,
            'description': '规划了线上线下双渠道布局,但没有设计价格管控机制,导致线上低价冲击线下门店的溢价体系,或线下体验客户在线上比价后流失.',
            'example': '大力发展电商直播和线下门店,覆盖全客群...',
            'correction': '设计完整的渠道价格体系:线上线下的价格带区隔,渠道专属产品线,窜货处罚规则,价格一致性监控机制.',
            'severity': 'major'
        },
        'resource_overextension': {
            'name': '资源过度分散',
            'category': FallacyCategory.STRATEGIC,
            'description': '同时推进3个以上的增长方向("六大引擎齐头并进""多线并行"),但未评估企业是否有足够的资金,人才和管理带宽来支撑多线作战.',
            'example': '同步推进数字化营销,私域运营,品牌出海,品类扩展,直播带货,B2B礼品六大增长引擎...',
            'correction': '明确优先级排序:第一阶段集中资源做1-2个核心增长方向,验证成功后再扩展.资源有限时,少做就是多做.',
            'severity': 'critical'
        },
    }

def init_strategic_detection_patterns() -> Dict[str, List[str]]:
    """初始化战略谬误专用检测模式"""
    return {
        'goal_driven_planning': [
            r'\d+亿.*目标',
            r'从.*到.*增长',
            r'十倍|十.*倍',
            r'X倍增长',
        ],
        'confirmation_bias_strategy': [
            r'高速增长|快速增长|爆发式',
            r'蓝海|巨大机会|风口',
            r'市场.*大|潜力.*巨大',
        ],
        'false_analogy_strategy': [
            r'对标|参考.*成功|借鉴',
            r'学习.*经验',
        ],
        'brand_growth_contradiction': [
            r'(非遗|稀缺|收藏|孤品|高端|手工|匠心)',
            r'(规模化|大众|入门|代工|量产|平价)',
        ],
        'narrative_blindness': [
            r'数字化.*生态|全链路.*闭环|赋能.*体系',
            r'品效合一|全域.*fusion',
        ],
        'concept_stacking': [
            r'生态.*矩阵|矩阵.*闭环|闭环.*赋能',
            r'全链路|全渠道|全域',
            r'数字化.*转型.*体系',
        ],
        'number_game': [
            r'\d+.*[-~至]\d+亿',
            r'预计.*年.*\d+亿',
            r'增长率?\d+\.?\d*%',
        ],
        'slogan_planning': [
            r'打造.*体系|构建.*矩阵|建设.*平台',
            r'建立.*机制|完善.*制度',
        ],
        'hollow_risk_management': [
            r'风险.*管控|风险管理|风险应对',
            r'加强.*管理|优化.*体系',
        ],
        'fake_validation': [
            r'经过.*调研|可行性分析',
            r'深入.*研究|全面.*评估',
        ],
        'omni_channel_price_conflict': [
            r'线上.*线下|电商.*门店',
            r'直播.*渠道|全渠道',
        ],
        'resource_overextension': [
            r'同时推进|多线并行|全面铺开|齐头并进',
            r'大.*引擎|大.*方向',
        ],
    }

def calculate_strategic_confidence(
    fallacy_id: str,
    fallacy_info: Dict,
    argument: str
) -> float:
    """计算战略谬误的置信度"""
    confidence = 0.0

    # 基于示例文本中的关键词匹配
    example = fallacy_info.get('example', '')
    example_keywords = [kw for kw in example.split() if len(kw) >= 2]
    match_count = sum(1 for kw in example_keywords if kw in argument)
    if example_keywords:
        confidence += (match_count / len(example_keywords)) * 0.3

    # 基于检测模式
    strategic_patterns = init_strategic_detection_patterns()
    if fallacy_id in strategic_patterns:
        patterns = strategic_patterns[fallacy_id]
        pattern_matches = sum(1 for p in patterns if re.search(p, argument))
        if patterns:
            confidence += (pattern_matches / len(patterns)) * 0.5

    # 基于描述中的核心概念
    desc_keywords = ['目标', '增长', '数字化', '生态', '矩阵', '闭环',
                    '赋能', '全链路', '体系', '平台', '私域', '规模',
                    '高端', '大众', '品牌', '对标本', '风险']
    desc_match = sum(1 for kw in desc_keywords if kw in argument)
    confidence += min(0.2, desc_match * 0.02)

    return min(confidence, 1.0)

def detect_strategic(
    strategic_fallacies: Dict[str, Dict],
    argument: str
) -> List[FallacyDetection]:
    """
    检测战略咨询专用谬误
    """
    detections = []

    for fallacy_id, fallacy_info in strategic_fallacies.items():
        confidence = calculate_strategic_confidence(
            fallacy_id, fallacy_info, argument
        )

        if confidence > 0.25:  # 战略谬误用更低的阈值,宁可误报不可漏报
            detection = FallacyDetection(
                fallacy_name=fallacy_info['name'],
                category=fallacy_info['category'],
                description=fallacy_info['description'],
                severity=fallacy_info.get('severity', 'major'),
                confidence=confidence,
                suggestion=fallacy_info['correction'],
                detected_at=datetime.now()
            )
            detections.append(detection)

    detections.sort(key=lambda x: x.confidence, reverse=True)
    return detections
