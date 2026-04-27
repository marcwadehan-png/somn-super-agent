"""咨询验证器 - 反模式检测器"""
import re
from typing import Any, Dict, List

from ._cv_types import (
    AntiPatternType,
    SeverityLevel,
    AntiPatternDetection,
)

__all__ = [
    'detect',
]

class AntiPatternDetector:
    """
    反模式检测器

    检测咨询方案中的认知偏差和输出缺陷.

    认知反模式:
    - C-01 目标驱动型规划: 先定目标,再反推路径,忽略约束
    - C-02 确认偏差: 只找支持自己假设的证据
    - C-03 锚定效应: 被第一个想法锚定,不探索替代方案
    - C-04 可得性偏差: 只考虑容易想到的信息
    - C-05 错误类比: 不考虑条件差异,盲目套用成功案例
    - C-06 叙事蒙蔽: 被自己的宏大叙事说服

    输出反模式:
    - O-01 概念堆砌: 用高大上的概念替代具体方案
    - O-02 数字游戏: 用精确数字制造专业感,实际无支撑
    - O-03 口号式规划: 有方向无路径
    - O-04 空洞风控: 风险recognize了但应对是空话
    - O-05 走过场验证: 声称做了验证但实际未深入
    """

    # 反模式检测规则
    DETECTION_RULES = {
        AntiPatternType.GOAL_DRIVEN: {
            'severity': SeverityLevel.CRITICAL,
            'indicators': [
                (r'\d+亿.*目标', '设定了具体营收目标'),
                (r'(从.*到.*)', '使用了"从X到Y"的增长叙事'),
            ],
            'counter_indicators': [
                (r'约束.*反推', '有约束反推分析'),
                (r'天花板|能力边界', '有天花板/能力边界分析'),
                (r'合理目标', '使用了"合理目标"表述'),
            ],
            'description': '先设定增长目标,再反推路径,未从约束条件出发推导合理目标范围.',
            'fix': '从企业能力边界和市场天花板出发,反推合理目标范围,而非自上而下拍目标.'
        },
        AntiPatternType.CONFIRMATION_BIAS: {
            'severity': SeverityLevel.CRITICAL,
            'indicators': [
                (r'增长.*快|高速增长|爆发', '使用了乐观的增长描述'),
                (r'蓝海|巨大机会|风口', '使用了机会导向的乐观描述'),
            ],
            'counter_indicators': [
                (r'风险|挑战|约束|瓶颈|不足', '提到了风险或挑战'),
                (r'增速.*低|增速.*下降|放缓', '提到了增速放缓'),
            ],
            'description': '只呈现支持增长假设的证据,忽略了不利数据和风险因素.',
            'fix': '主动搜索并呈现与核心假设相矛盾的数据和证据.'
        },
        AntiPatternType.FALSE_ANALOGY: {
            'severity': SeverityLevel.MAJOR,
            'indicators': [
                (r'对标|参考|学习.*成功|借鉴', '引用了对标案例'),
            ],
            'counter_indicators': [
                (r'差异|不同|条件|适配', '分析了对标差异'),
                (r'底层逻辑.*不同|不可复制', '意识到方法论不适用'),
            ],
            'description': '引用对标案例但未分析条件差异,盲目套用成功方法论.',
            'fix': '分析对标案例与当前企业的核心差异,评估方法论的适配性.'
        },
        AntiPatternType.CONCEPT_STACKING: {
            'severity': SeverityLevel.MAJOR,
            'indicators': [
                (r'生态|矩阵|闭环|赋能|全链路|数字化', '使用了抽象概念词汇'),
            ],
            'counter_indicators': [
                (r'具体.*方案|落地.*路径|执行.*细则', '有具体落地方案'),
            ],
            'description': '使用高大上的概念替代具体可落地的方案.',
            'fix': '将每个抽象概念转化为具体的执action作,时间节点和负责团队.'
        },
        AntiPatternType.NUMBER_GAME: {
            'severity': SeverityLevel.MODERATE,
            'indicators': [
                (r'\d+.*[-~至]\d+亿', '使用了营收区间数字'),
            ],
            'counter_indicators': [
                (r'测算|推导|反推|模型', '有测算逻辑说明'),
                (r'来源|据.*报告', '有数据来源标注'),
            ],
            'description': '使用精确数字但未提供测算逻辑和数据来源.',
            'fix': '为每个关键数字提供完整的测算逻辑和数据来源.'
        },
        AntiPatternType.SLOGAN_PLANNING: {
            'severity': SeverityLevel.MAJOR,
            'indicators': [
                (r'打造.*体系|构建.*矩阵|建设.*平台', '提出了体系建设方向'),
            ],
            'counter_indicators': [
                (r'KPI|考核|metrics|里程碑|时间表', '有具体执行metrics'),
                (r'团队.*人|预算.*万|周期.*月', '有资源和时间规划'),
            ],
            'description': '有方向性规划但无具体执行细节(团队/预算/KPI/时间表).',
            'fix': '为每个规划方向补充:团队配置,预算分配,KPImetrics,时间节点.'
        },
        AntiPatternType.HOLLOW_RISK: {
            'severity': SeverityLevel.MAJOR,
            'indicators': [
                (r'风险.*管控|风险管理|风险应对', '提到了风险管控'),
            ],
            'counter_indicators': [
                (r'应急预案|止损|预警.*红线', '有应急预案'),
                (r'触发条件|资源调整', '有风险应对细则'),
            ],
            'description': 'recognize了风险但应对措施是原则性口号,无可落地的执行细则.',
            'fix': '为每个风险设计具体的应急预案,止损触发条件和资源调整方案.'
        },
        AntiPatternType.AVAILABILITY_BIAS: {
            'severity': SeverityLevel.MODERATE,
            'indicators': [
                (r'传统.*转型|门店.*电商|线下.*线上', '提到了常规转型路径'),
            ],
            'counter_indicators': [
                (r'创新.*路径|差异化|蓝海', '探索了差异化路径'),
                (r'替代方案|备选', '考虑了多种方案'),
            ],
            'description': '只考虑容易想到的常规转型路径,未探索替代方案.',
            'fix': '至少提出2-3个不同方向的替代增长路径,并分析各路径的优劣.'
        },
        AntiPatternType.ANCHORING: {
            'severity': SeverityLevel.MODERATE,
            'indicators': [
                (r'第一.*方案|最终.*方案|唯一.*方案', '只提了一个方案'),
            ],
            'counter_indicators': [
                (r'方案A|方案B|多方案|备选', '提出了多个方案'),
                (r'权衡|取舍|优劣', '分析了方案权衡'),
            ],
            'description': '被第一个想到的方案锚定,未探索替代方案.',
            'fix': '提出至少两个不同方向的备选方案,并分析各自的优劣和适用条件.'
        },
        AntiPatternType.NARRATIVE_BLINDNESS: {
            'severity': SeverityLevel.MAJOR,
            'indicators': [
                (r'伟大|愿景|使命|颠覆|改变', '使用了宏大叙事词汇'),
            ],
            'counter_indicators': [
                (r'挑战|风险|约束|瓶颈', '提到了执行挑战'),
                (r'分阶段|小步快跑|快速迭代', '有务实执行思路'),
            ],
            'description': '被自己的宏大叙事说服,忽略了执行层面的挑战和约束.',
            'fix': '为宏大愿景设计具体的分阶段执行路径,并识别每个阶段的关键挑战.'
        },
        AntiPatternType.FAKE_VALIDATION: {
            'severity': SeverityLevel.MAJOR,
            'indicators': [
                (r'验证.*通过|可行性.*确认|逻辑.*自洽', '声称做了验证'),
            ],
            'counter_indicators': [
                (r'用户调研|市场测试|试点', '有实际验证行动'),
                (r'数据.*支撑|事实.*依据', '有数据支撑'),
            ],
            'description': '声称做了验证但未提供具体的验证过程和数据支撑.',
            'fix': '补充验证过程:用户调研样本量,试点数据,关键假设的数据支撑.'
        },
    }

    def detect(self, solution_data: Dict[str, Any]) -> List[AntiPatternDetection]:
        """执行反模式检测"""
        full_text = solution_data.get('full_text', '')
        detections = []

        for pattern_type, rule in self.DETECTION_RULES.items():
            # 检查正面metrics
            positive_matches = []
            for regex, desc in rule['indicators']:
                if re.search(regex, full_text):
                    positive_matches.append(desc)

            if not positive_matches:
                continue

            # 检查反面metrics(缓解措施)
            negative_matches = []
            for regex, desc in rule.get('counter_indicators', []):
                if re.search(regex, full_text):
                    negative_matches.append(desc)

            # 如果有缓解措施,降低严重程度
            if negative_matches:
                severity = SeverityLevel.MINOR
                detection_desc = f"检测到{rule['description']}的苗头,但已有部分缓解措施({', '.join(negative_matches[:2])}),建议进一步完善."
            else:
                severity = rule['severity']
                detection_desc = rule['description']

            detections.append(AntiPatternDetection(
                pattern_type=pattern_type,
                severity=severity,
                description=detection_desc,
                evidence='; '.join(positive_matches[:3]),
                fix_suggestion=rule['fix']
            ))

        return detections
