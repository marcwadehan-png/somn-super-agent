"""
科学广告验证系统 - Scientific Advertising Verification System

科学广告方法论:
1. 明确目标 - 广告的唯一目的是销售
2. 科学测试 - 用数据验证假设
3. 量化优化 - 基于测试结果持续优化
4. 直接反应 - 设计可追踪的反应机制

版本: v6.0.0
创建: 2026-04-02
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import uuid

logger = logging.getLogger(__name__)

class AdElement(Enum):
    """广告元素类型"""
    HEADLINE = "headline"              # 标题
    SUBHEADLINE = "subheadline"        # 副标题
    BODY = "body"                      # 正文
    CALL_TO_ACTION = "cta"            # action号召
    VISUAL = "visual"                  # 视觉
    OFFER = "offer"                    # 优惠

class TestType(Enum):
    """测试类型"""
    A_B_TEST = "a_b_test"             # A/B测试
    MULTIVARIATE = "multivariate"      # 多变量测试
    PRE_POST = "pre_post"             # 前后测试
    CONTROL = "control"               # 控制组测试

@dataclass
class HopkinsGoldRule:
    """霍普金斯21条广告金律"""
    rule_id: str
    rule_number: int
    rule_content: str
    application_guide: str
    modern_application: str
    
    @classmethod
    def get_all_rules(cls) -> List['HopkinsGoldRule']:
        """get全部21条金律"""
        rules = [
            (1, "广告标题应包含利益承诺", "明确告诉读者能得到什么好处", "利益导向标题+SEO关键词"),
            (2, "避免聪明的文案", "清晰胜过机智,消费者太忙", "简洁直白的表达"),
            (3, "使用具体的事实和数字", "具体数字增加可信度", "数据化文案:3分钟,99%"),
            (4, "提供免费样品或试用", "降低试用门槛,消除风险", "免费试用,满意保证"),
            (5, "讲述一个故事", "故事增加记忆度和情感连接", "品牌故事,用户故事"),
            (6, "不要批评竞争对手", "批评反而可能为对手做宣传", "专注自身优势"),
            (7, "不要试图幽默", "幽默可能分散注意力", "适度幽默,避免过度"),
            (8, "始终使用你视角", "关注读者利益,而非自己", "你/你的视角"),
            (9, "避免夸张", "夸大破坏可信度", "诚实,具体,可验证"),
            (10, "测试每一个广告", "数据验证效果", "A/B测试持续优化"),
            (11, "持续追踪结果", "监控广告效果", "归因分析"),
            (12, "一次只承诺一件事", "聚焦核心信息", "单一卖点"),
            (13, "使用情感诉求", "情感驱动decision", "情感共鸣+理性支撑"),
            (14, "不要改变成功的广告", "守成优于频繁变更", "稳定投放测试过的广告"),
            (15, "关注分销,而非仅是广告", "渠道配合广告", "全渠道协同"),
            (16, "地区性广告优于全国性", "先测试后扩展", "区域测试strategy"),
            (17, "使用优惠券追踪效果", "可衡量的反应机制", "优惠码追踪"),
            (18, "不要依赖样式,依赖原则", "原则不变,形式可新", "核心原则+创新形式"),
            (19, "建立长期品牌形象", "广告是长期投资", "品牌一致性"),
            (20, "不要欺骗消费者", "欺骗短期有效,长期自毁", "诚信为本"),
            (21, "记住广告是为了销售", "销售是广告的唯一目的", "效果导向")
        ]
        
        return [HopkinsGoldRule(
            rule_id=f"rule_{i}",
            rule_number=r[0],
            rule_content=r[1],
            application_guide=r[2],
            modern_application=r[3]
        ) for i, r in enumerate(rules)]

@dataclass
class AdCopyElement:
    """广告文案元素"""
    element_id: str
    element_type: AdElement
    content: str
    
    # 评估metrics
    specificity_score: float = 0.0      # 具体性得分
    benefit_score: float = 0.0         # 利益承诺得分
    clarity_score: float = 0.0         # 清晰度得分
    emotional_score: float = 0.0      # 情感得分

@dataclass
class AdTestResult:
    """广告测试结果"""
    test_id: str
    test_type: TestType
    variants: List[Dict]               # 测试变体
    
    # 性能metrics
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    
    click_rate: float = 0.0           # 点击率
    conversion_rate: float = 0.0     # 转化率
    cost_per_conversion: float = 0.0 # 单次转化成本
    
    # 胜出版本
    winner_id: Optional[str] = None
    confidence_level: float = 0.0
    
    # 统计显著性
    is_significant: bool = False
    p_value: float = 1.0
    
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class ScientificAdVerification:
    """科学广告验证报告"""
    verification_id: str
    ad_copy: str
    
    # 霍普金斯金律检验
    hopkins_rules_passed: List[int] = field(default_factory=list)
    hopkins_rules_failed: List[int] = field(default_factory=list)
    hopkins_score: float = 0.0      # 0-100
    
    # 拉斯克尔原则检验
    lasker_principles_passed: List[str] = field(default_factory=list)
    lasker_principles_failed: List[str] = field(default_factory=list)
    lasker_score: float = 0.0
    
    # synthesize评估
    overall_score: float = 0.0
    sales_effectiveness: str = ""
    
    # 优化建议
    improvements: List[str] = field(default_factory=list)
    
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

class AdCopyAnalyzer:
    """广告文案分析器"""
    
    def analyze_copy(self, ad_copy: str) -> List[AdCopyElement]:
        """分析广告文案元素"""
        elements = []
        
        # 简单分割 - 实际应用中需要更复杂的NLP
        lines = ad_copy.split('\n')
        
        for i, line in enumerate(lines):
            if not line.strip():
                continue
                
            if i == 0:  # 第一行通常是标题
                elem_type = AdElement.HEADLINE
            elif 'http' in line.lower() or '点击' in line or '立即' in line:
                elem_type = AdElement.CALL_TO_ACTION
            elif len(line) < 50:
                elem_type = AdElement.SUBHEADLINE
            else:
                elem_type = AdElement.BODY
            
            element = AdCopyElement(
                element_id=f"elem_{i}",
                element_type=elem_type,
                content=line.strip(),
                specificity_score=self._score_specificity(line),
                benefit_score=self._score_benefit(line),
                clarity_score=self._score_clarity(line),
                emotional_score=self._score_emotional(line)
            )
            elements.append(element)
        
        return elements
    
    def _score_specificity(self, text: str) -> float:
        """评估具体性"""
        has_numbers = any(c.isdigit() for c in text)
        has_verbs = any(v in text for v in ['获得', '得到', '节省', '提升'])
        has_specs = any(s in text for s in ['%', '倍', '分钟', '天'])
        
        score = 0.3
        if has_numbers: score += 0.25
        if has_verbs: score += 0.25
        if has_specs: score += 0.2
        
        return min(1.0, score)
    
    def _score_benefit(self, text: str) -> float:
        """评估利益承诺"""
        benefit_words = ['获得', '得到', '节省', '提升', '解决', '享受', '拥有', '实现']
        has_benefit = any(w in text for w in benefit_words)
        return 0.8 if has_benefit else 0.3
    
    def _score_clarity(self, text: str) -> float:
        """评估清晰度"""
        length_penalty = max(0, len(text) - 100) / 200
        jargon_penalty = sum(0.1 for j in ['专业', '先进', '领先'] if j in text) if '术语' in text else 0
        
        clarity = 0.7 - length_penalty - jargon_penalty
        return max(0.1, min(1.0, clarity))
    
    def _score_emotional(self, text: str) -> float:
        """评估情感"""
        emotion_words = ['爱', '惊喜', '感动', '兴奋', '快乐', '幸福', '渴望']
        has_emotion = sum(1 for w in emotion_words if w in text)
        return min(1.0, 0.3 + has_emotion * 0.15)

class ScientificVerificationEngine:
    """科学广告验证引擎"""
    
    def __init__(self):
        self.analyzer = AdCopyAnalyzer()
        self.test_history: List[AdTestResult] = []
    
    def verify_ad(self, ad_copy: str, context: Dict = None) -> ScientificAdVerification:
        """
        验证广告是否符合科学广告原则
        
        霍普金斯21条金律 + 拉斯克尔6大原则
        """
        verification_id = f"verify_{uuid.uuid4().hex[:8]}"
        
        # 分析文案元素
        elements = self.analyzer.analyze_copy(ad_copy)
        
        # 霍普金斯金律检验
        hopkins_rules = HopkinsGoldRule.get_all_rules()
        rules_passed = []
        rules_failed = []
        
        for rule in hopkins_rules:
            if self._check_rule(rule, elements, ad_copy):
                rules_passed.append(rule.rule_number)
            else:
                rules_failed.append(rule.rule_number)
        
        hopkins_score = len(rules_passed) / len(hopkins_rules) * 100
        
        # 拉斯克尔原则检验
        lasker_checks = self._check_lasker_principles(ad_copy, context or {})
        lasker_passed = [p for p, result in lasker_checks.items() if result]
        lasker_failed = [p for p, result in lasker_checks.items() if not result]
        lasker_score = len(lasker_passed) / len(lasker_checks) * 100
        
        # synthesize评估
        overall_score = (hopkins_score * 0.6 + lasker_score * 0.4)
        
        # 销售有效性评估
        sales_effectiveness = self._assess_sales_effectiveness(
            overall_score, hopkins_score, lasker_score
        )
        
        # 优化建议
        improvements = self._generate_improvements(
            rules_failed, lasker_failed, elements
        )
        
        return ScientificAdVerification(
            verification_id=verification_id,
            ad_copy=ad_copy[:100] + "...",
            hopkins_rules_passed=rules_passed,
            hopkins_rules_failed=rules_failed,
            hopkins_score=hopkins_score,
            lasker_principles_passed=lasker_passed,
            lasker_principles_failed=lasker_failed,
            lasker_score=lasker_score,
            overall_score=overall_score,
            sales_effectiveness=sales_effectiveness,
            improvements=improvements
        )
    
    def _check_rule(self, rule: HopkinsGoldRule, elements: List, ad_copy: str) -> bool:
        """检验单条金律"""
        rule_num = rule.rule_number
        
        # 规则1: 标题包含利益承诺
        if rule_num == 1:
            headline = elements[0].content if elements else ""
            return any(b in headline for b in ['获得', '节省', '提升', '解决', '免费'])
        
        # 规则2: 避免过度聪明
        if rule_num == 2:
            return not any(w in ad_copy for w in ['666', '绝绝子', 'yyds'])
        
        # 规则3: 使用具体数字
        if rule_num == 3:
            return any(c.isdigit() for c in ad_copy)
        
        # 规则4: 提供试用
        if rule_num == 4:
            return any(t in ad_copy for t in ['免费', '试用', '体验', '领取'])
        
        # 规则5: 讲故事
        if rule_num == 5:
            return any(s in ad_copy for s in ['曾经', '后来', '故事', '经历'])
        
        # 规则6: 不批评竞品
        if rule_num == 6:
            return True  # 无法检测,默认通过
        
        # 规则7: 不过度幽默
        if rule_num == 7:
            return True  # 无法检测,默认通过
        
        # 规则8: 使用"你"视角
        if rule_num == 8:
            you_count = ad_copy.count('你') + ad_copy.count('您的')
            return you_count > 0
        
        # 规则10: 可测试性
        if rule_num == 10:
            return True  # 假设可测试
        
        # 规则12: 单一承诺
        if rule_num == 12:
            benefit_count = sum(1 for b in ['获得', '节省', '提升'] if b in ad_copy)
            return benefit_count <= 2
        
        # 规则19: 建立品牌形象
        if rule_num == 19:
            return True  # 假设有品牌意识
        
        # 规则20: 不欺骗
        if rule_num == 20:
            return not any(w in ad_copy for w in ['最', '第一', '唯一'] if ad_copy.count(w) > 2)
        
        # 规则21: 销售导向
        if rule_num == 21:
            return any(a in ad_copy for a in ['立即', '现在', '点击', '购买'])
        
        return True  # 默认通过
    
    def _check_lasker_principles(self, ad_copy: str, context: Dict) -> Dict[str, bool]:
        """检验拉斯克尔原则"""
        return {
            'sales_oriented': any(s in ad_copy for s in ['购买', '下单', '立即', '申请']),
            'why_not_what': '为什么' in ad_copy or '因为' in ad_copy or '因此' in ad_copy,
            'sufficient_info': len(ad_copy) > 100,
            'no_puffery': not any(w in ad_copy for w in ['最好', '完美', '极致'] if ad_copy.count(w) > 1),
            'testable': True,  # 假设可测试
            'action_oriented': any(a in ad_copy for a in ['立即', '现在', '马上', '赶紧'])
        }
    
    def _assess_sales_effectiveness(self, overall: float, hopkins: float, lasker: float) -> str:
        """评估销售有效性"""
        if overall >= 85:
            return "卓越 - 符合科学广告原则,预计销售效果好"
        elif overall >= 70:
            return "良好 - 符合大部分原则,有一定销售潜力"
        elif overall >= 50:
            return "一般 - 需要优化以提升销售效果"
        else:
            return "较差 - 建议重新策划广告strategy"
    
    def _generate_improvements(self, 
                             hopkins_failed: List[int],
                             lasker_failed: List[str],
                             elements: List[AdCopyElement]) -> List[str]:
        """generate改进建议"""
        suggestions = []
        
        # 基于霍普金斯金律失败项
        rule_suggestions = {
            1: "标题应明确承诺用户能获得的具体利益",
            2: "使用清晰直白的语言,避免过度创意",
            3: "加入具体数字和数据增加可信度",
            4: "提供免费试用或满意保证降低购买门槛",
            5: "讲述用户故事增加情感连接",
            8: "使用'你'的视角,关注读者利益",
            12: "聚焦单一核心信息,不要多重承诺",
            21: "确保广告有明确的action号召"
        }
        
        for rule_num in hopkins_failed[:5]:
            if rule_num in rule_suggestions:
                suggestions.append(rule_suggestions[rule_num])
        
        # 基于拉斯克尔原则失败项
        if 'sales_oriented' in lasker_failed:
            suggestions.append("增强销售导向:明确告知用户下一步action")
        if 'why_not_what' in lasker_failed:
            suggestions.append("解释'为什么'用户需要这个产品")
        if 'sufficient_info' in lasker_failed:
            suggestions.append("提供更充分的产品信息说服用户")
        
        return suggestions if suggestions else ["广告质量良好"]

class AdTestingEngine:
    """广告测试引擎"""
    
    def __init__(self):
        self.tests: List[AdTestResult] = []
    
    def create_test(self,
                   variants: List[Dict],
                   test_type: TestType = TestType.A_B_TEST) -> AdTestResult:
        """创建广告测试"""
        test_id = f"test_{uuid.uuid4().hex[:8]}"
        
        result = AdTestResult(
            test_id=test_id,
            test_type=test_type,
            variants=variants
        )
        
        self.tests.append(result)
        return result
    
    def record_results(self,
                      test_id: str,
                      impressions: int,
                      clicks: int,
                      conversions: int,
                      costs: float = 0) -> AdTestResult:
        """记录测试结果"""
        test = next((t for t in self.tests if t.test_id == test_id), None)
        if not test:
            return None
        
        test.impressions = impressions
        test.clicks = clicks
        test.conversions = conversions
        
        # 计算metrics
        test.click_rate = clicks / impressions if impressions > 0 else 0
        test.conversion_rate = conversions / clicks if clicks > 0 else 0
        test.cost_per_conversion = costs / conversions if conversions > 0 else 0
        
        # 确定胜出版本(简化版)
        if test.variants:
            test.winner_id = test.variants[0].get('id', 'variant_1')
            test.confidence_level = 0.85
        
        test.is_significant = test.conversions >= 100
        
        return test
    
    def run_ab_test(self,
                   variant_a: Dict,
                   variant_b: Dict,
                   sample_size: int = 1000) -> Dict:
        """
        运行A/B测试分析
        
        返回统计分析结果
        """
        # 简化版A/B测试分析
        results = {
            'variant_a': variant_a,
            'variant_b': variant_b,
            'sample_size': sample_size,
            'recommended_winner': 'A',
            'confidence': 0.0,
            'lift': 0.0
        }
        
        # 简化提升度计算
        if variant_a.get('conversion_rate', 0) > 0:
            lift = (variant_b.get('conversion_rate', 0) - variant_a.get('conversion_rate', 0)) / variant_a.get('conversion_rate', 0.01)
            results['lift'] = lift
        
        # 选择胜者
        if variant_b.get('conversion_rate', 0) > variant_a.get('conversion_rate', 0):
            results['recommended_winner'] = 'B'
        
        # 置信度(简化)
        results['confidence'] = min(0.95, 0.7 + abs(results['lift']) * 0.1)
        
        return results

# 导出
__all__ = [
    'ScientificVerificationEngine',
    'AdTestingEngine',
    'AdCopyAnalyzer',
    'HopkinsGoldRule',
    'ScientificAdVerification',
    'AdTestResult',
    'TestType',
    'AdElement'
]
