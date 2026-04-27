"""咨询验证器 - 方案质量评分器"""
import re
from typing import Any, Dict, List, Tuple

from ._cv_types import (
    QualityDimension,
    QualityScoreDetail,
)

__all__ = [
    'score',
]

class SolutionQualityScorer:
    """
    方案质量评分器

    基于七大质量维度对咨询方案进行synthesize评分.

    评分维度(各100分):
    1. 用户分析 - 至少覆盖2类用户画像
    2. 竞争分析 - 至少3个直接竞品深度拆解
    3. 数据论证 - 关键主张有可溯源数据
    4. 执行细节 - 每个增长引擎有落地路径
    5. 风险管控 - 至少10项风险recognize
    6. 逻辑自洽 - 无内部矛盾
    7. 财务闭环 - 有资金来源和使用规划
    """

    DIMENSION_SCORING = {
        QualityDimension.USER_ANALYSIS: {
            'minimum': 30,
            'ideal': 80,
            'indicators': {
                30: ['用户画像', '客群', '消费者'],
                50: ['年龄', '收入', '购买动机', '复购'],
                70: ['用户分层', '增量用户', 'decision因素'],
                80: ['用户分层运营', '生命周期', '用户旅程'],
                100: ['留存strategy', '转介绍', '用户增长模型'],
            },
            'critical_items': ['用户画像'],
        },
        QualityDimension.COMPETITION_ANALYSIS: {
            'minimum': 30,
            'ideal': 75,
            'indicators': {
                30: ['竞品', '竞争', '对手'],
                50: ['市场份额', '万仟堂|东道|观复', '差异化'],
                70: ['对标', '品类扩展', '失败教训'],
                80: ['渠道布局', '定价strategy', '核心壁垒'],
                100: ['竞品反制', '先发优势', '护城河建设'],
            },
            'critical_items': ['竞品'],
        },
        QualityDimension.DATA_ARGUMENTATION: {
            'minimum': 40,
            'ideal': 80,
            'indicators': {
                40: [r'\d+.*亿', '市场.*规模', '增速'],
                60: ['来源', '据', '报告', '数据'],
                80: ['交叉验证', '对标数据', '行业基准'],
                100: ['多源验证', '量级检验', '数据时效'],
            },
            'critical_items': [],
        },
        QualityDimension.EXECUTION_DETAIL: {
            'minimum': 30,
            'ideal': 75,
            'indicators': {
                30: ['渠道', '产品', '营销'],
                50: ['团队', '预算', 'KPI', '时间'],
                70: ['落地', '执行', '里程碑'],
                80: ['责任人', '考核', '单店模型', '转化率'],
                100: ['资源分配', '节奏规划', '阶段性目标'],
            },
            'critical_items': ['渠道', '产品'],
        },
        QualityDimension.RISK_MANAGEMENT: {
            'minimum': 25,
            'ideal': 70,
            'indicators': {
                25: ['风险'],
                40: [r'风险.*\d+', '合规', '供应链'],
                60: ['应急预案', '止损'],
                70: ['情景分析', '预警', '触发条件'],
                85: ['止损线', '资源调整方案', '20项风险'],
                100: ['压力测试', '风险矩阵', '风险预案'],
            },
            'critical_items': ['风险'],
        },
        QualityDimension.LOGICAL_CONSISTENCY: {
            'minimum': 40,
            'ideal': 80,
            'indicators': {
                40: ['逻辑', '论证'],
                60: ['矛盾', '一致性'],
                80: ['交叉论证', '三重验证', '压力测试'],
                100: ['附录.*回应', '逐条修正', '反驳分析'],
            },
            'critical_items': [],
        },
        QualityDimension.FINANCIAL_CLOSURE: {
            'minimum': 20,
            'ideal': 70,
            'indicators': {
                20: ['预算', '投入', '资金'],
                40: ['融资', '自有资金', '营销投入'],
                60: ['现金流', '资金来源', '使用规划'],
                70: ['测算', '5年.*资金', '财务模型'],
                85: ['融资节奏', '信贷', 'ROI'],
                100: ['敏感性分析', '资金链风控', '盈亏平衡'],
            },
            'critical_items': [],
        },
    }

    def score(self, solution_data: Dict[str, Any]) -> Tuple[float, List[QualityScoreDetail]]:
        """计算方案质量评分"""
        full_text = solution_data.get('full_text', '')
        dimension_scores = []

        for dimension, config in self.DIMENSION_SCORING.items():
            score = self._calculate_dimension_score(full_text, config)

            gap = ""
            if score < config['minimum']:
                gap = f"未达到最低标准({config['minimum']}分),{dimension.value}严重不足."
            elif score < config['ideal']:
                gap = f"距离理想标准({config['ideal']}分)差{config['ideal'] - score}分."

            dimension_scores.append(QualityScoreDetail(
                dimension=dimension,
                score=score,
                minimum_standard=config['minimum'],
                ideal_standard=config['ideal'],
                gap_analysis=gap
            ))

        # 加权总分
        weights = [0.15, 0.15, 0.10, 0.20, 0.15, 0.15, 0.10]
        total = sum(d.score * w for d, w in zip(dimension_scores, weights))

        return round(total, 1), dimension_scores

    def _calculate_dimension_score(self, full_text: str, config: Dict) -> float:
        """计算单个维度的得分"""
        indicators = config['indicators']
        sorted_thresholds = sorted(indicators.keys())

        # 从高分到低分检测,找到匹配的最高分
        matched_score = 0
        for threshold in reversed(sorted_thresholds):
            pattern_list = indicators[threshold]
            match_count = sum(1 for p in pattern_list if re.search(p, full_text))
            # 至少匹配该等级的50%metrics才得分
            if match_count >= max(1, len(pattern_list) * 0.5):
                matched_score = threshold
                break

        # 检查关键项是否存在
        critical_items = config.get('critical_items', [])
        for item in critical_items:
            if item not in full_text:
                matched_score = min(matched_score, config['minimum'] - 10)

        return max(0, matched_score)
