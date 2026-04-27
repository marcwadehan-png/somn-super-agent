"""
__all__ = [
    'analyze_competition',
    'audit_positioning',
    'create_positioning_statement',
    'design_differentiation',
    'determine_positioning_type',
    'develop_repositioning_strategy',
]

心理学先驱深化引擎 - 特劳特定位decision引擎
Pioneer Positioning - Ries & Trout Positioning Engine
=====================================================
版本: v1.0.0
创建时间: 2026-04-03

特劳特核心思想:
1. 定位理论 - 在心智中占据位置
2. 竞争导向 - 关注竞争对手而非用户
3. 差异化 - 成为第一或唯一
4. 重新定位 - 对手强势下的strategy
5. 简单原则 - 单一概念,反复传播
6. 聚焦 - 少即是多

核心功能:
1. 竞争分析
2. 定位strategy制定
3. 差异化设计
4. 重新定位strategy
5. 品牌定位卡
"""

from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime
from enum import Enum

class 定位类型(Enum):
    """定位类型"""
    领导者定位 = "领导者定位"     # 占据第一的位置
    跟随者定位 = "跟随者定位"     # 寻找空位
    重新定位 = "重新定位"         # 对手强势下的strategy
    专业化定位 = "专业化定位"     # 专注细分领域

class 竞争策略(Enum):
    """竞争策略"""
    正面进攻 = "正面进攻"        # 以强对强
    侧翼进攻 = "侧翼进攻"        # 寻找弱点
    包围进攻 = "包围进攻"        # 多点突破
    游击战 = "游击战"           # 小规模灵活

class 特劳特定位引擎:
    """
    特劳特定位decision引擎
    
    核心功能:
    1. 竞争分析 - 分析竞争格局
    2. 定位strategy制定 - 确定定位方向
    3. 差异化设计 - 构建差异化
    4. 重新定位strategy - 对手强势下的strategy
    5. 品牌定位卡 - 输出定位方案
    """
    
    def __init__(self):
        self.name = "特劳特定位引擎"
        self.version = "8.2.0"
        
        # 定位类型定义
        self.定位类型定义 = {
            定位类型.领导者定位: {
                "适用条件": "市场无明确领导者",
                "strategy": "第一个进入心智,建立第一认知",
                "执行": "不断重复,强调领先"
            },
            定位类型.跟随者定位: {
                "适用条件": "市场领导者已建立",
                "strategy": "寻找空位,差异化切入",
                "执行": "聚焦细分,建立独特价值"
            },
            定位类型.重新定位: {
                "适用条件": "竞争对手定位强势",
                "strategy": "改变认知,重新排序",
                "执行": "发现对手弱点,重新定位"
            },
            定位类型.专业化定位: {
                "适用条件": "资源有限",
                "strategy": "专注细分领域第一",
                "执行": "深耕细作,建立专家地位"
            }
        }
        
        # 定位维度
        self.定位维度 = [
            "产品属性定位",
            "价格定位",
            "使用者定位",
            "使用场景定位",
            "竞争对比定位",
            "情感定位",
            "文化定位"
        ]
        
        # 常见定位陷阱
        self.定位陷阱 = [
            "产品陷阱 - 沉迷于产品功能",
            "营销近视 - 只看技术不看市场",
            "自我定位 - 基于内部视角而非外部认知",
            "过度定位 - 目标市场太小",
            "模糊定位 - 没有清晰的差异化",
            "多定位 - 试图满足所有人"
        ]
    
    def analyze_competition(self, brand_data: Dict, competitors: List[Dict]) -> Dict:
        """
        竞争分析
        
        Args:
            brand_data: 品牌数据
            competitors: 竞争对手数据
            
        Returns:
            竞争分析结果
        """
        品牌定位 = brand_data.get("positioning", "")
        品牌优势 = set(brand_data.get("strengths", []))
        
        # 分析竞争格局
        竞争格局 = self._analyze_market_structure(brand_data, competitors)
        
        # recognize机会
        机会点 = self._identify_opportunities(竞争格局, 品牌优势)
        
        # recognize威胁
        威胁点 = self._identify_threats(竞争格局, 品牌优势)
        
        # 竞争定位矩阵
        定位矩阵 = self._build_positioning_matrix(brand_data, competitors)
        
        return {
            "竞争格局": 竞争格局,
            "机会点": 机会点,
            "威胁点": 威胁点,
            "定位矩阵": 定位矩阵,
            "竞争建议": self._generate_competition_advice(竞争格局, 机会点, 威胁点)
        }
    
    def _analyze_market_structure(self, brand: Dict, competitors: List) -> Dict:
        """分析市场结构"""
        total = len(competitors) + 1
        
        # 市场份额
        market_share = []
        for c in competitors:
            market_share.append({
                "品牌": c.get("name", "未知"),
                "份额": c.get("market_share", 0),
                "优势": c.get("positioning", "")
            })
        
        # 领导者recognize
        领导者 = max(market_share, key=lambda x: x["份额"]) if market_share else None
        
        # 市场集中度
        top3_share = sum(sorted([c.get("market_share", 0) for c in competitors], reverse=True)[:3])
        
        return {
            "品牌数": total,
            "市场领导者": 领导者,
            "Top3份额": top3_share,
            "市场类型": "高度集中" if top3_share > 70 else "适度竞争" if top3_share > 40 else "碎片化",
            "各品牌定位": market_share
        }
    
    def _identify_opportunities(self, 格局: Dict, 优势: Set) -> List[Dict]:
        """recognize机会"""
        opportunities = []
        
        # 市场类型机会
        if 格局["市场类型"] == "碎片化":
            opportunities.append({
                "类型": "整合机会",
                "描述": "市场碎片化,存在整合机会",
                "strategy": "通过并购或合作建立规模"
            })
        elif 格局["市场类型"] == "高度集中":
            opportunities.append({
                "类型": "细分机会",
                "描述": "领导者存在未覆盖的细分需求",
                "strategy": "聚焦细分领域,建立专家地位"
            })
        
        # 定位空白
        已占定位 = set(c.get("优势", "") for c in 格局.get("各品牌定位", []))
        可选定位 = [dim for dim in self.定位维度 if dim not in 已占定位]
        
        if 可选定位:
            opportunities.append({
                "类型": "定位空白",
                "描述": f"可用定位维度:{', '.join(可选定位[:3])}",
                "strategy": "占据未被占据的定位"
            })
        
        return opportunities
    
    def _identify_threats(self, 格局: Dict, 优势: Set) -> List[Dict]:
        """recognize威胁"""
        threats = []
        
        # 领导者威胁
        if 格局["市场领导者"]:
            threats.append({
                "类型": "领导者压力",
                "描述": f"领导者{格局['市场领导者']['品牌']}占据强势地位",
                "应对": "寻找差异化空位或重新定位"
            })
        
        # 市场集中度威胁
        if 格局["市场类型"] == "高度集中":
            threats.append({
                "类型": "进入壁垒",
                "描述": "市场高度集中,新进入者面临挑战",
                "应对": "采用侧翼战或游击战"
            })
        
        return threats
    
    def _build_positioning_matrix(self, brand: Dict, competitors: List) -> Dict:
        """构建定位矩阵"""
        # 简化:基于两个核心维度
        return {
            "维度1": "价格(低-高)",
            "维度2": "品质(基础-高端)",
            "品牌位置": {
                "自有品牌": brand.get("positioning", "待确定"),
                "主要竞品": [c.get("name", "") for c in competitors[:3]]
            }
        }
    
    def _generate_competition_advice(self, 格局: Dict, 机会: List, 威胁: List) -> str:
        """generate竞争建议"""
        advice = []
        
        if 机会:
            advice.append(f"抓住机会:{机会[0]['类型']} - {机会[0]['描述']}")
        
        if 威胁:
            advice.append(f"应对威胁:{威胁[0]['类型']} - {威胁[0]['应对']}")
        
        return "; ".join(advice) if advice else "保持现有strategy,稳步发展"
    
    def determine_positioning_type(self, market_data: Dict, brand_data: Dict) -> Dict:
        """
        确定定位类型
        
        Args:
            market_data: 市场数据
            brand_data: 品牌数据
            
        Returns:
            定位类型建议
        """
        市场份额 = brand_data.get("market_share", 0)
        资源状况 = brand_data.get("resources", "中")
        竞争优势 = brand_data.get("competitive_advantage", "")
        
        # decision逻辑
        if 市场份额 >= 30:
            推荐类型 = 定位类型.领导者定位
            理由 = "市场份额领先,应巩固领导者地位"
        elif 资源状况 == "有限":
            推荐类型 = 定位类型.专业化定位
            理由 = "资源有限,应聚焦细分领域"
        elif 竞争优势:
            推荐类型 = 定位类型.跟随者定位
            理由 = f"具有{竞争优势}优势,可差异化切入"
        else:
            推荐类型 = 定位类型.重新定位
            理由 = "需要重新定位以建立差异化"
        
        # generate备选
        alternatives = [t for t in 定位类型 if t != 推荐类型]
        
        return {
            "推荐定位类型": 推荐类型.value,
            "推荐理由": 理由,
            "类型定义": self.定位类型定义.get(推荐类型, {}),
            "备选方案": [a.value for a in alternatives[:2]],
            "执行要点": self._get_positioning_execution_points(推荐类型)
        }
    
    def _get_positioning_execution_points(self, ptype: 定位类型) -> List[str]:
        """get定位执行要点"""
        执行表 = {
            定位类型.领导者定位: [
                "尽早占领心智第一位置",
                "不断重复,强化领先认知",
                "用action维护领先地位"
            ],
            定位类型.跟随者定位: [
                "深入研究领导者,寻找空位",
                "聚焦细分,建立独特价值",
                "快速action,抢占先机"
            ],
            定位类型.重新定位: [
                "发现竞争对手的弱点",
                "建立与竞品的对比",
                "用新认知替代旧认知"
            ],
            定位类型.专业化定位: [
                "选择一个足够小的领域",
                "成为该领域的绝对专家",
                "逐步扩展相关领域"
            ]
        }
        return 执行表.get(ptype, ["确定定位,执行到位"])
    
    def design_differentiation(self, brand_data: Dict, market_data: Dict) -> Dict:
        """
        差异化设计
        
        Args:
            brand_data: 品牌数据
            market_data: 市场数据
            
        Returns:
            差异化方案
        """
        产品 = brand_data.get("product", "")
        目标受众 = brand_data.get("target", "")
        竞争优势 = brand_data.get("competitive_advantage", "")
        
        # recognize差异化维度
        差异化维度 = self._identify_differentiation_dimensions(产品, 目标受众)
        
        # generate差异化概念
        差异化概念 = self._generate_differentiation_concepts(差异化维度, 竞争优势)
        
        # 评估差异化
        评估结果 = self._evaluate_differentiation(差异化概念, market_data)
        
        # 选择最佳差异化
        最佳 = max(评估结果, key=lambda x: x["总分"]) if 评估结果 else {}
        
        return {
            "差异化维度": 差异化维度,
            "可选概念": 差异化概念,
            "概念评估": 评估结果,
            "推荐差异化": 最佳,
            "传播要点": self._get_differentiation_messaging(最佳)
        }
    
    def _identify_differentiation_dimensions(self, product: str, target: str) -> List[Dict]:
        """recognize差异化维度"""
        维度 = []
        
        # 产品属性
        维度.append({
            "维度": "产品属性",
            "示例": ["独特功能", "更好性能", "更高品质"],
            "适用": "产品有明显优势时"
        })
        
        # 价格
        维度.append({
            "维度": "价格",
            "示例": ["最便宜", "性价比最高", "最贵"],
            "适用": "价格是重要decision因素时"
        })
        
        # 使用场景
        维度.append({
            "维度": "使用场景",
            "示例": ["送礼首选", "自用首选", "商务专用"],
            "适用": "场景是decision关键时"
        })
        
        # 使用者
        维度.append({
            "维度": "使用者",
            "示例": ["年轻人的选择", "专业人士", "妈妈最爱"],
            "适用": "用户群体清晰时"
        })
        
        # 领导者
        维度.append({
            "维度": "竞争对比",
            "示例": ["比X品牌更好", "非X品牌的选择", "X品牌替代品"],
            "适用": "竞品强势时"
        })
        
        return 维度
    
    def _generate_differentiation_concepts(self, dimensions: List, advantage: str) -> List[Dict]:
        """generate差异化概念"""
        concepts = []
        
        for dim in dimensions[:3]:  # 取前3个维度
            for example in dim["示例"][:2]:  # 每个维度取2个示例
                concepts.append({
                    "概念": f"{dim['维度']}:{example}",
                    "维度": dim["维度"],
                    "可执行性": "高" if advantage else "中"
                })
        
        return concepts
    
    def _evaluate_differentiation(self, concepts: List, market: Dict) -> List[Dict]:
        """评估差异化"""
        evaluated = []
        
        for concept in concepts:
            score = 0
            reasons = []
            
            # 可实现性
            if "高" in concept.get("可执行性", ""):
                score += 25
                reasons.append("可执行性强")
            
            # 独特性
            if "独特" in concept.get("概念", "") or "专业" in concept.get("概念", ""):
                score += 30
                reasons.append("独特性强")
            
            # 重要性
            if "品质" in concept.get("概念", "") or "功能" in concept.get("概念", ""):
                score += 25
                reasons.append("对用户重要")
            
            # 可传播性
            if len(concept.get("概念", "")) < 10:
                score += 20
                reasons.append("简洁易记")
            
            evaluated.append({
                "概念": concept["概念"],
                "维度": concept["维度"],
                "总分": score,
                "得分理由": reasons
            })
        
        return sorted(evaluated, key=lambda x: x["总分"], reverse=True)
    
    def _get_differentiation_messaging(self, best: Dict) -> Dict:
        """get差异化传播要点"""
        return {
            "核心信息": best.get("概念", ""),
            "支撑点": ["支撑点1", "支撑点2", "支撑点3"],
            "传播建议": "简洁,重复,聚焦"
        }
    
    def develop_repositioning_strategy(self, brand_data: Dict, competitors: List[Dict]) -> Dict:
        """
        重新定位strategy
        
        Args:
            brand_data: 品牌数据
            competitors: 竞争对手数据
            
        Returns:
            重新定位方案
        """
        当前定位 = brand_data.get("current_positioning", "")
        竞品定位 = [c.get("positioning", "") for c in competitors]
        
        # 分析竞品弱点
        竞品弱点 = self._analyze_competitor_weaknesses(competitors)
        
        # 制定重新定位strategy
        新定位 = self._develop_new_positioning(brand_data, 竞品弱点)
        
        # 过渡方案
        过渡 = self._develop_transition_plan(当前定位, 新定位)
        
        return {
            "当前定位": 当前定位,
            "竞品弱点": 竞品弱点,
            "建议新定位": 新定位,
            "过渡方案": 过渡,
            "风险提示": self._identify_repositioning_risks(当前定位, 新定位),
            "成功要素": ["领导层支持", "资源投入", "执行一致性"]
        }
    
    def _analyze_competitor_weaknesses(self, competitors: List) -> List[Dict]:
        """分析竞争对手弱点"""
        weaknesses = []
        
        for c in competitors[:3]:
            # 简化分析
            weaknesses.append({
                "品牌": c.get("name", "未知"),
                "弱点": c.get("weakness", "存在改进空间"),
                "机会": f"提供更好的替代方案"
            })
        
        return weaknesses
    
    def _develop_new_positioning(self, brand: Dict, weaknesses: List) -> Dict:
        """制定新定位"""
        brand_name = brand.get("name", "")
        
        if weaknesses:
            # 基于竞品弱点定位
            return {
                "定位": f"更{weaknesses[0]['弱点']}的选择",
                "对比": f"相比{weaknesses[0]['品牌']}更胜一筹",
                "差异化": weaknesses[0]["机会"]
            }
        else:
            # 基于自身优势定位
            return {
                "定位": f"{brand.get('core_advantage', '独特价值')}专家",
                "对比": "行业领先",
                "差异化": "专业,深耕"
            }
    
    def _develop_transition_plan(self, current: str, new: Dict) -> List[str]:
        """制定过渡方案"""
        return [
            f"第一阶段:认知铺垫(2-3月)- 引入新概念",
            f"第二阶段:重新定位(3-6月)- 强化新认知",
            f"第三阶段:巩固(6月+)- 持续传播新定位"
        ]
    
    def _identify_repositioning_risks(self, current: str, new: Dict) -> List[str]:
        """recognize重新定位风险"""
        return [
            "原有认知可能难以改变",
            "过渡期可能造成市场混乱",
            "需要持续投入资源"
        ]
    
    def create_positioning_statement(self, brand_data: Dict) -> Dict:
        """
        创建品牌定位陈述
        
        Args:
            brand_data: 品牌数据
            
        Returns:
            定位陈述
        """
        品牌 = brand_data.get("name", "")
        产品类别 = brand_data.get("category", "")
        目标市场 = brand_data.get("target", "")
        核心价值 = brand_data.get("core_value", "")
        差异化 = brand_data.get("differentiation", "")
        
        # 完整定位陈述
        完整陈述 = f"{品牌}是{产品类别},致力于为{目标市场}提供{核心价值}," \
                   f"其独特之处在于{differentiation}."
        
        # 简洁定位陈述
        简洁陈述 = f"{品牌} = {差异化}的{产品类别}"
        
        # 品牌承诺
        品牌承诺 = f"选择{品牌},{目标市场}将获得{核心价值}"
        
        # 品牌主张
        品牌主张 = f"为什么选择{品牌}?因为{差异化}"
        
        return {
            "品牌": 品牌,
            "完整定位陈述": 完整陈述,
            "简洁定位陈述": 简洁陈述,
            "品牌承诺": 品牌承诺,
            "品牌主张": 品牌主张,
            "使用场景": self._suggest_positioning_usage(完整陈述, 简洁陈述)
        }
    
    def _suggest_positioning_usage(self, full: str, short: str) -> Dict:
        """建议定位使用场景"""
        return {
            "完整陈述": "品牌官网,关于我们",
            "简洁陈述": "广告语,slogan",
            "品牌承诺": "客服话术,服务承诺",
            "品牌主张": "对比广告,案例展示"
        }
    
    def audit_positioning(self, brand_data: Dict, customer_perception: Dict) -> Dict:
        """
        定位审计
        
        Args:
            brand_data: 品牌数据
            customer_perception: 客户认知数据
            
        Returns:
            定位审计结果
        """
        品牌定位 = brand_data.get("positioning", "")
        客户认知 = customer_perception.get("perception", "")
        
        # 对比分析
        一致性 = self._check_consistency(品牌定位, 客户认知)
        
        # recognize问题
        问题 = self._identify_positioning_problems(一致性, customer_perception)
        
        # 优化建议
        建议 = self._generate_optimization_suggestions(问题)
        
        return {
            "当前定位": 品牌定位,
            "客户认知": 客户认知,
            "一致性分析": 一致性,
            "存在问题": 问题,
            "优化建议": 建议
        }
    
    def _check_consistency(self, positioning: str, perception: str) -> str:
        """检查一致性"""
        # 简化检查
        关键词重叠 = sum(1 for w in positioning.split() if w in perception)
        
        if 关键词重叠 >= 3:
            return "高度一致"
        elif 关键词重叠 >= 1:
            return "部分一致"
        else:
            return "不一致,需要调整"
    
    def _identify_positioning_problems(self, consistency: str, perception: Dict) -> List[str]:
        """recognize定位问题"""
        problems = []
        
        if consistency == "不一致":
            problems.append("品牌定位与客户认知存在差距")
        
        if perception.get("confusion"):
            problems.append("客户对品牌认知模糊")
        
        if perception.get("irrelevant"):
            problems.append("品牌定位与客户需求不相关")
        
        return problems if problems else ["未发现明显问题"]
    
    def _generate_optimization_suggestions(self, problems: List) -> List[str]:
        """generate优化建议"""
        suggestions = []
        
        for problem in problems:
            if "差距" in problem:
                suggestions.append("加强传播,强化核心信息")
            elif "模糊" in problem:
                suggestions.append("简化定位,聚焦单一信息")
            elif "不相关" in problem:
                suggestions.append("调整定位,更贴近客户需求")
        
        return suggestions if suggestions else ["保持现有strategy"]

# 全局实例
positioning_engine = 特劳特定位引擎()
