"""咨询验证器 - 五维调研完整性检查器"""
import re
from typing import Any, Dict, List

from ._cv_types import (
    ResearchDimension,
    ResearchCheckItem,
)

__all__ = [
    'check',
]

class ResearchCompletenessChecker:
    """
    五维调研完整性检查器

    确保咨询方案在调研阶段覆盖了所有关键信息维度.

    调研五维:
    1. 企业自身 - 财务/产能/组织/渠道/产品/品牌资产
    2. 用户画像 - 现有用户/增量用户/用户分层/购买decision/复购留存
    3. 竞争格局 - 直接竞品/间接竞品/对标案例/竞争壁垒
    4. 市场环境 - 市场规模/细分市场/出海市场/趋势研判
    5. 风险全景 - 合规/宏观/供应链/人才/品牌/财务/竞争/执行
    """

    # 各维度的必须检查项
    DIMENSION_CHECKLIST = {
        ResearchDimension.ENTERPRISE: [
            ("财务基本面", "营收,利润率,纳税额,增速数据"),
            ("产能与供应链", "产能数据,扩产空间,原材料依赖"),
            ("组织能力", "团队规模,核心人才,管理架构"),
            ("渠道现状", "线上线下渠道,门店数据,客单价"),
            ("产品体系", "SKU数量,价格带,爆款数据"),
            ("品牌资产", "品牌历史,文化IP,收藏荣誉"),
        ],
        ResearchDimension.USER: [
            ("现有用户画像", "年龄/收入/地域/购买动机/复购率"),
            ("增量目标用户", "目标扩展客群的需求/偏好/触达渠道"),
            ("用户分层", "收藏级/高端/入门/礼品用户比例与需求差异"),
            ("购买decision因素", "decision因素排序,信息触点,decision周期"),
            ("复购与留存", "复购周期,留存率,流失原因"),
        ],
        ResearchDimension.COMPETITION: [
            ("直接竞品分析", "市场份额,产品体系,渠道布局,定价strategy"),
            ("间接竞品/替代品", "替代品威胁分析"),
            ("对标案例", "同路径品牌的成功经验与失败教训"),
            ("竞争壁垒分析", "各品牌护城河来源"),
        ],
        ResearchDimension.MARKET: [
            ("市场规模", "TAM/SAM/SOM,增速,渗透率"),
            ("细分市场", "各价格带规模,各渠道占比"),
            ("出海市场", "目标市场规模,竞争格局,政策法规"),
            ("消费趋势", "行业趋势,政策趋势,技术趋势"),
        ],
        ResearchDimension.RISK: [
            ("合规风险", "环保,食品安全,跨境合规,知识产权"),
            ("供应链风险", "原材料供应,代工品控,产能约束"),
            ("财务风险", "资金链,投入ROI,融资需求"),
            ("品牌风险", "品牌稀释,舆情危机,质量事故"),
            ("人才风险", "核心人员流失,招聘难度"),
        ],
    }

    def check(self, solution_data: Dict[str, Any]) -> List[ResearchCheckItem]:
        """
        检查调研完整性

        Args:
            solution_data: 方案数据,应包含各维度的调研内容

        Returns:
            检查结果列表
        """
        results = []

        for dimension, checklist in self.DIMENSION_CHECKLIST.items():
            dim_data = solution_data.get(dimension.value, {})
            dim_content = solution_data.get('full_text', '')

            for item_name, item_desc in checklist:
                is_present = self._check_item_present(dim_data, item_name, dim_content)
                quality = self._assess_quality(dim_data, item_name, dim_content, is_present)

                results.append(ResearchCheckItem(
                    dimension=dimension,
                    item_name=item_name,
                    is_present=is_present,
                    quality_score=quality,
                    evidence=self._extract_evidence(dim_content, item_name),
                    suggestion=self._generate_suggestion(dimension, item_name, is_present, quality)
                ))

        return results

    def _check_item_present(self, dim_data: Dict, item_name: str, full_text: str) -> bool:
        """检查某项调研内容是否存在"""
        # 先检查结构化数据
        if item_name in dim_data:
            return True
        # 再检查全文关键词
        keywords = item_name.replace('/', ' ').split()
        for kw in keywords:
            if len(kw) >= 2 and kw in full_text:
                return True
        return False

    def _assess_quality(self, dim_data: Dict, item_name: str,
                        full_text: str, is_present: bool) -> float:
        """评估某项调研内容的质量"""
        if not is_present:
            return 0.0

        score = 0.3  # 基础分:存在即给分

        # 有结构化数据加分
        if item_name in dim_data:
            val = dim_data[item_name]
            if isinstance(val, dict) and len(val) > 2:
                score += 0.4
            elif isinstance(val, list) and len(val) > 1:
                score += 0.3
            elif isinstance(val, str) and len(val) > 50:
                score += 0.2

        # 有量化数据加分
        numbers = re.findall(r'[\d.]+[万亿%]', full_text[max(0, full_text.find(item_name)-200):full_text.find(item_name)+500] if item_name in full_text else '')
        if len(numbers) >= 2:
            score += 0.2

        # 有数据来源加分
        source_keywords = ['据', '数据', '报告', '统计', '来源', '调研', '报告']
        context = full_text[max(0, full_text.find(item_name)-100):full_text.find(item_name)+300] if item_name in full_text else ''
        if any(kw in context for kw in source_keywords):
            score += 0.1

        return min(1.0, score)

    def _extract_evidence(self, full_text: str, item_name: str) -> str:
        """提取某项调研的证据片段"""
        if item_name not in full_text:
            return ""
        idx = full_text.find(item_name)
        start = max(0, idx - 50)
        end = min(len(full_text), idx + 200)
        return full_text[start:end].replace('\n', ' ').strip()

    def _generate_suggestion(self, dimension: ResearchDimension,
                            item_name: str, is_present: bool, quality: float) -> str:
        """generate改进建议"""
        if not is_present:
            return f"[{dimension.value}] 缺失'{item_name}'调研,必须补充.参考调研方向:{self.DIMENSION_CHECKLIST[dimension]}"
        if quality < 0.5:
            return f"[{dimension.value}] '{item_name}'调研质量不足,建议补充量化数据和数据来源."
        return ""
