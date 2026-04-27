# -*- coding: utf-8 -*-
"""
智慧风险预警系统 v1.0.0
Wisdom Risk Warning System

fusion素书遵义章46种警示,易经变易风险,兵法风险管理
提供全维度的企业风险预警体系

版本: v1.0.0
日期: 2026-04-02
"""

from enum import Enum
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

class RiskCategory(Enum):
    """风险类别"""
    LEADERSHIP = "领导风险"      # 领导层风险
    STRATEGY = "战略风险"        # 战略decision风险
    TALENT = "人才风险"          # 人才管理风险
    CULTURE = "文化风险"         # 企业文化风险
    COMPLIANCE = "合规风险"      # 合规法律风险
    FINANCE = "财务风险"         # 财务风险
    MARKET = "市场风险"          # 市场竞争风险
    OPERATION = "运营风险"       # 运营管理风险

class RiskLevel(Enum):
    """风险等级"""
    LOW = "低"
    MEDIUM = "中"
    HIGH = "高"
    CRITICAL = "极高"

@dataclass
class RiskWarning:
    """风险警示"""
    code: str                            # 警示编码
    name: str                            # 警示名称
    description: str                     # 风险描述
    category: RiskCategory
    level: RiskLevel
    classical_source: str                # 经典来源
    classical_quote: str                 # 相关语录
    warning_signs: List[str]            # 预警信号
    prevention: List[str]               # 预防措施
    mitigation: List[str]               # 缓解措施

@dataclass
class RiskAssessment:
    """风险评估"""
    timestamp: datetime
    target: str                          # 评估对象
    total_risks: int
    
    critical_risks: List[RiskWarning]    # 极高风险
    high_risks: List[RiskWarning]        # 高风险
    medium_risks: List[RiskWarning]      # 中风险
    low_risks: List[RiskWarning]         # 低风险
    
    # synthesize建议
    top_priority_actions: List[str]
    risk_score: float
    
    # 古典指引
    classical_guidance: str
    sufu_warnings: List[str]
    yijing_guidance: str

class WisdomRiskWarningSystem:
    """
    智慧风险预警系统
    
    fusion:
    1. 素书遵义章46种警示
    2. 易经变易风险预测
    3. 道德经风险哲学
    4. 孙子兵法先为不可胜
    5. 吕氏春秋阴阳平衡
    """
    
    def __init__(self):
        self.warning_database = self._build_warning_database()
        self.classical_wisdom = self._build_classical_wisdom()
    
    def _build_warning_database(self) -> List[RiskWarning]:
        """构建风险数据库"""
        return [
            # 领导风险
            RiskWarning(
                code="L001",
                name="独断专行",
                description="领导者过于独断,不听谏言",
                category=RiskCategory.LEADERSHIP,
                level=RiskLevel.HIGH,
                classical_source="素书·遵义章",
                classical_quote="自见者不明,自是者不彰",
                warning_signs=["排斥不同意见", "不开会议", "重大decision无人参与"],
                prevention=["建立decision会议制度", "鼓励多元声音"],
                mitigation=["引入外部顾问", "建立反馈机制"]
            ),
            RiskWarning(
                code="L002",
                name="道德失范",
                description="领导层道德品质问题",
                category=RiskCategory.LEADERSHIP,
                level=RiskLevel.CRITICAL,
                classical_source="素书·遵义章",
                classical_quote="德薄而位尊,智小而谋大,力小而任重,鲜不及矣",
                warning_signs=["违规行为", "道德绑架", "虚假承诺"],
                prevention=["道德考察", "价值观培训"],
                mitigation=["管理层换血", "重建企业文化"]
            ),
            RiskWarning(
                code="L003",
                name="亢龙有悔",
                description="成功后过度自满",
                category=RiskCategory.LEADERSHIP,
                level=RiskLevel.HIGH,
                classical_source="易经·乾卦",
                classical_quote="亢龙有悔",
                warning_signs=["成功后急速扩张", "无视风险", "过度冒险"],
                prevention=["保持危机意识", "定期风险评估"],
                mitigation=["回归核心业务", "控制扩张节奏"]
            ),
            
            # 战略风险
            RiskWarning(
                code="S001",
                name="方向迷失",
                description="战略方向不清晰",
                category=RiskCategory.STRATEGY,
                level=RiskLevel.HIGH,
                classical_source="道德经",
                classical_quote="知常容,不知常,妄作凶",
                warning_signs=["战略频繁变动", "团队困惑", "执行混乱"],
                prevention=["制定3-5年战略规划", "确立核心使命"],
                mitigation=["战略复盘", "重新梳理方向"]
            ),
            RiskWarning(
                code="S002",
                name="急于求成",
                description="过于追求速度,忽视质量",
                category=RiskCategory.STRATEGY,
                level=RiskLevel.MEDIUM,
                classical_source="论语",
                classical_quote="无欲速,无见小利.欲速则不达,见小利则大事不成",
                warning_signs=["质量问题频发", "客户投诉增加", "团队疲惫"],
                prevention=["制定可持续增长目标", "建立质量保障体系"],
                mitigation=["放慢节奏", "补齐短板"]
            ),
            RiskWarning(
                code="S003",
                name="盲目扩张",
                description="无节制地扩大规模",
                category=RiskCategory.STRATEGY,
                level=RiskLevel.HIGH,
                classical_source="素书·安礼章",
                classical_quote="吉莫吉于知足",
                warning_signs=["资金紧张", "管理失控", "主业衰退"],
                prevention=["控制扩张节奏", "聚焦核心业务"],
                mitigation=["收缩业务线", "优化资源配置"]
            ),
            
            # 人才风险
            RiskWarning(
                code="T001",
                name="德才失衡",
                description="重才轻德,用人不当",
                category=RiskCategory.TALENT,
                level=RiskLevel.HIGH,
                classical_source="论语",
                classical_quote="举直错诸枉,能使枉者直",
                warning_signs=["内部腐败", "道德滑坡", "团队涣散"],
                prevention=["建立德才评估体系", "定期品德考察"],
                mitigation=["人才汰换", "重建团队文化"]
            ),
            RiskWarning(
                code="T002",
                name="人才流失",
                description="核心人才大规模离职",
                category=RiskCategory.TALENT,
                level=RiskLevel.HIGH,
                classical_source="孟子",
                classical_quote="得其民斯得天下,失其民斯失天下",
                warning_signs=["月度离职率>5%", "核心岗位空缺", "士气低落"],
                prevention=["完善激励机制", "打造成长文化"],
                mitigation=["紧急挽留计划", "加速人才补充"]
            ),
            RiskWarning(
                code="T003",
                name="近墨者黑",
                description="小人聚集,影响组织文化",
                category=RiskCategory.TALENT,
                level=RiskLevel.HIGH,
                classical_source="素书·遵义章",
                classical_quote="近君子远小人",
                warning_signs=["负面八卦盛行", "互相拆台", "信任度下降"],
                prevention=["文化建设", "行为准则制定"],
                mitigation=["清除负能量", "重建团队氛围"]
            ),
            
            # 文化风险
            RiskWarning(
                code="C001",
                name="礼崩乐坏",
                description="组织秩序和规范失效",
                category=RiskCategory.CULTURE,
                level=RiskLevel.HIGH,
                classical_source="论语·子路",
                classical_quote="上好礼,则民易使也",
                warning_signs=["制度形同虚设", "规则无人遵守", "管理失序"],
                prevention=["强化制度执行力", "领导以身作则"],
                mitigation=["重建制度体系", "树立规范典型"]
            ),
            RiskWarning(
                code="C002",
                name="信义缺失",
                description="企业诚信形象受损",
                category=RiskCategory.CULTURE,
                level=RiskLevel.CRITICAL,
                classical_source="论语",
                classical_quote="人而无信,不知其可也",
                warning_signs=["客户投诉信任问题", "媒体负面报道", "合作方流失"],
                prevention=["诚信文化建设", "信息透明化"],
                mitigation=["危机公关", "信誉修复计划"]
            ),
            
            # 合规风险
            RiskWarning(
                code="R001",
                name="违法违规",
                description="经营行为违反法律法规",
                category=RiskCategory.COMPLIANCE,
                level=RiskLevel.CRITICAL,
                classical_source="尚书",
                classical_quote="罪疑惟轻,功疑惟重",
                warning_signs=["收到监管警告", "媒体曝光违规行为", "诉讼风险"],
                prevention=["建立合规体系", "定期法律审查"],
                mitigation=["立即整改", "积极配合调查"]
            ),
            
            # 财务风险
            RiskWarning(
                code="F001",
                name="现金流危机",
                description="资金链断裂风险",
                category=RiskCategory.FINANCE,
                level=RiskLevel.CRITICAL,
                classical_source="素书·遵义章",
                classical_quote="危于利也",
                warning_signs=["账期延长", "拒付债务", "银行征信恶化"],
                prevention=["维持3-6月现金储备", "多元融资渠道"],
                mitigation=["紧急融资", "削减非必要支出"]
            ),
            RiskWarning(
                code="F002",
                name="过度负债",
                description="杠杆率过高",
                category=RiskCategory.FINANCE,
                level=RiskLevel.HIGH,
                classical_source="道德经",
                classical_quote="飘风不终朝,骤雨不终日",
                warning_signs=["资产负债率>70%", "利息支出过大", "偿债压力"],
                prevention=["控制负债率", "优化债务结构"],
                mitigation=["降杠杆计划", "引入股权融资"]
            ),
            
            # 市场风险
            RiskWarning(
                code="M001",
                name="市场洞察盲区",
                description="对市场变化失去敏感性",
                category=RiskCategory.MARKET,
                level=RiskLevel.HIGH,
                classical_source="孙子兵法",
                classical_quote="知己知彼,百战不殆",
                warning_signs=["竞品快速增长", "客户需求变化", "市场份额下降"],
                prevention=["建立市场监测体系", "定期竞品分析"],
                mitigation=["产品快速迭代", "市场重新定位"]
            ),
            RiskWarning(
                code="M002",
                name="黑暗森林效应",
                description="行业竞争白热化",
                category=RiskCategory.MARKET,
                level=RiskLevel.HIGH,
                classical_source="刘慈欣<三体>",
                classical_quote="黑暗森林法则",
                warning_signs=["价格战激烈", "利润大幅下降", "行业洗牌"],
                prevention=["差异化竞争", "构建护城河"],
                mitigation=["价值重塑", "合作抱团取暖"]
            ),
            
            # 运营风险
            RiskWarning(
                code="O001",
                name="物极必反",
                description="快速增长后的系统性崩溃",
                category=RiskCategory.OPERATION,
                level=RiskLevel.HIGH,
                classical_source="易经",
                classical_quote="物极必反",
                warning_signs=["增长达到顶点", "系统压力极大", "团队疲惫"],
                prevention=["可持续发展模式", "压力测试"],
                mitigation=["系统优化", "战略休整"]
            ),
            RiskWarning(
                code="O002",
                name="执行力衰减",
                description="团队执行力下降",
                category=RiskCategory.OPERATION,
                level=RiskLevel.MEDIUM,
                classical_source="大学",
                classical_quote="格物致知,诚意正心",
                warning_signs=["目标完成率下降", "任务延期", "推诿扯皮"],
                prevention=["建立大秦指标/KPI体系", "流程优化"],
                mitigation=["激励重建", "执行力培训"]
            ),
        ]
    
    def _build_classical_wisdom(self) -> Dict[str, str]:
        """构建经典智慧"""
        return {
            "整体保护": "先为不可胜,以待敌之可胜.--孙子兵法",
            "风险意识": "居安思危,思则有备,有备无患.--左传",
            "持续警觉": "生于忧患,死于安乐.--孟子",
            "预防为主": "圣人不治已病,治未病;不治已乱,治未乱.--黄帝内经",
            "根本防范": "道可道,非常道.--道德经",
            "synthesize把控": "凡事豫则立,不豫则废.--礼记"
        }
    
    def assess_risks(
        self, 
        situation: str,
        context: Optional[Dict[str, Any]] = None
    ) -> RiskAssessment:
        """
        评估风险
        
        Args:
            situation: 当前情况描述
            context: 上下文信息
            
        Returns:
            RiskAssessment: 风险评估结果
        """
        situation_lower = situation.lower()
        matched_risks = []
        
        # 根据情况关键词匹配风险
        for warning in self.warning_database:
            match_score = 0
            
            # 检查警示信号
            for sign in warning.warning_signs:
                if any(keyword in situation_lower for keyword in sign.split()):
                    match_score += 1
            
            # 检查关键词
            if warning.category.value in situation or warning.name in situation:
                match_score += 3
            
            if match_score > 0:
                matched_risks.append((warning, match_score))
        
        # 如果没有匹配,返回通用警示
        if not matched_risks:
            matched_risks = [(warning, 1) for warning in self.warning_database[:5]]
        
        # 按匹配度和等级排序
        matched_risks.sort(key=lambda x: (x[1], list(RiskLevel).index(x[0].level)), reverse=True)
        
        all_matched = [r[0] for r in matched_risks]
        
        critical = [r for r in all_matched if r.level == RiskLevel.CRITICAL]
        high = [r for r in all_matched if r.level == RiskLevel.HIGH]
        medium = [r for r in all_matched if r.level == RiskLevel.MEDIUM]
        low = [r for r in all_matched if r.level == RiskLevel.LOW]
        
        # 计算风险分数
        risk_score = (
            len(critical) * 0.4 + 
            len(high) * 0.25 + 
            len(medium) * 0.15 + 
            len(low) * 0.05
        ) / max(len(all_matched), 1)
        
        # generate优先action
        top_actions = []
        for risk in (critical + high)[:3]:
            top_actions.extend(risk.prevention[:2])
        
        # 易经指引
        if risk_score > 0.7:
            yijing_guidance = "坤卦警示:'臣弑其君,子弑其父,非一朝一夕之故,其所由来者渐矣.'须立即整改!"
        elif risk_score > 0.5:
            yijing_guidance = "乾卦提示:'终日乾乾,夕惕若厉,无咎.'保持警觉,积极应对."
        else:
            yijing_guidance = "坤卦安慰:'积善之家,必有余庆.'继续保持,防微杜渐."
        
        return RiskAssessment(
            timestamp=datetime.now(),
            target=situation[:50] + "..." if len(situation) > 50 else situation,
            total_risks=len(matched_risks),
            critical_risks=critical,
            high_risks=high,
            medium_risks=medium,
            low_risks=low,
            top_priority_actions=list(set(top_actions))[:5],
            risk_score=risk_score,
            classical_guidance=self.classical_wisdom.get("整体保护", ""),
            sufu_warnings=[w.classical_quote for w in critical + high[:3]],
            yijing_guidance=yijing_guidance
        )
    
    def get_warning_by_code(self, code: str) -> Optional[RiskWarning]:
        """根据编号get警示"""
        for warning in self.warning_database:
            if warning.code == code:
                return warning
        return None
    
    def get_warnings_by_category(self, category: RiskCategory) -> List[RiskWarning]:
        """根据类别get警示"""
        return [w for w in self.warning_database if w.category == category]
    
    def get_all_warnings(self) -> Dict[str, List[RiskWarning]]:
        """get全部警示"""
        result = {}
        for warning in self.warning_database:
            cat = warning.category.value
            if cat not in result:
                result[cat] = []
            result[cat].append(warning)
        return result
    
    def get_statistics(self) -> Dict[str, Any]:
        """get统计信息"""
        by_category = {}
        by_level = {}
        
        for w in self.warning_database:
            cat = w.category.value
            level = w.level.value
            
            by_category[cat] = by_category.get(cat, 0) + 1
            by_level[level] = by_level.get(level, 0) + 1
        
        return {
            "total_warnings": len(self.warning_database),
            "by_category": by_category,
            "by_level": by_level,
            "classical_sources": [
                "素书·遵义章",
                "易经",
                "论语",
                "孙子兵法",
                "道德经",
                "刘慈欣<三体>"
            ]
        }

def quick_risk_check(situation: str) -> str:
    """
    快速风险检查
    
    用法:
    >>> quick_risk_check("公司快速扩张,现金流紧张")
    """
    system = WisdomRiskWarningSystem()
    result = system.assess_risks(situation)
    
    output = f"""
{'='*60}
⚠️ 智慧风险预警报告
{'='*60}

📋 评估情况: {result.target}
🎯 风险总数: {result.total_risks}
📊 风险分数: {result.risk_score:.1%}
"""
    
    if result.critical_risks:
        output += f"\n❗ 极高风险 ({len(result.critical_risks)}项):\n"
        for r in result.critical_risks:
            output += f"  [{r.code}] {r.name}: {r.description}\n"
            output += f"  经典: '{r.classical_quote}'\n"
    
    if result.high_risks:
        output += f"\n🔴 高风险 ({len(result.high_risks)}项):\n"
        for r in result.high_risks[:3]:
            output += f"  [{r.code}] {r.name}: {r.description}\n"
    
    output += f"""
{'-'*60}
🚨 优先action:
{chr(10).join(f"  {i+1}. {a}" for i, a in enumerate(result.top_priority_actions))}

{'-'*60}
📜 古典警示:
{chr(10).join(f"  '{w}'" for w in result.sufu_warnings)}

{'-'*60}
☯️ 易经指引:
  {result.yijing_guidance}

{'='*60}
"""
    
    return output

# 导出
__all__ = [
    'WisdomRiskWarningSystem',
    'RiskCategory',
    'RiskLevel',
    'RiskWarning',
    'RiskAssessment',
    'quick_risk_check'
]
