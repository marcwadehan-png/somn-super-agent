"""
增强分析引擎 - DivineReason V4.0
提供更有意义的 insights 和 recommendations
"""

from typing import Any, Dict, List, Optional
from ._sub_engine_base import (
    SubReasoningEngine,
    EngineCategory,
    ReasoningResult,
    GLOBAL_ENGINE_REGISTRY,
)


class StrategicAnalysisEngine(SubReasoningEngine):
    """战略分析增强引擎 - 针对性分析具体问题"""
    
    def __init__(self):
        super().__init__(
            engine_id="strategic_analysis",
            engine_name="战略分析引擎",
            category=EngineCategory.STRATEGIC,
            sub_type=None,
            description="深入分析战略问题并提供针对性建议",
            capability_score=0.95
        )
    
    def _detect_scenario(self, query: str) -> Dict[str, bool]:
        """检测具体战略场景"""
        return {
            'market_share': any(kw in query for kw in ['市场份额', '占有率']),
            'growth': any(kw in query for kw in ['增长', '突破', '提升', '提高']),
            'competition': any(kw in query for kw in ['竞争', '对手', ' rivalry']),
            'differentiation': any(kw in query for kw in ['差异化', '优势', '独特']),
            'new_product': any(kw in query for kw in ['新产品', '上市', '推出']),
            'planning': any(kw in query for kw in ['规划', '战略', '计划']),
        }
    
    def _calculate_confidence(self, query: str, scenario: Dict) -> float:
        """动态计算置信度"""
        base = 0.70
        # 问题越具体，置信度越高
        if scenario['market_share']:
            base += 0.10
        if '30%' in query or '20%' in query or '50%' in query:
            base += 0.05  # 有具体数字
        if len(query) > 20:
            base += 0.05  # 问题描述详细
        return min(base, 0.95)
    
    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        query = input_data.get('query', '')
        problem_type = input_data.get('problem_type', '')
        
        reasoning_chain = ["【战略分析】"]
        insights = []
        recommendations = []
        
        # 场景检测
        scenario = self._detect_scenario(query)
        confidence = self._calculate_confidence(query, scenario)
        
        # 针对性分析
        if scenario['market_share']:
            # 市场份额下降
            insights.extend([
                "市场份额下降通常反映客户选择了竞争对手",
                "需分析：产品力下降/价格劣势/渠道覆盖不足/品牌力减弱",
                "定量评估：计算份额下降的季度趋势和区域分布",
                "竞品分析：对手是否有重大产品/营销动作",
                "客户流失分析：流失到哪些竞品，原因是什么"
            ])
            recommendations.extend([
                "立即启动竞品对标分析，找出差距",
                "访谈流失客户，了解真实离开原因",
                "评估产品路线图，是否需要重大升级",
                "审查定价策略，考虑价值定价而非成本定价",
                "加强品牌建设，提升心智份额"
            ])
        elif scenario['growth']:
            # 增长突破
            insights.extend([
                "增长突破需要找到杠杆点：产品/渠道/营销/价格",
                "分析增长类型：获取新客/提升客单价/增加复购",
                "市场饱和度分析：红海vs蓝海战略选择",
                "增长质量评估：薅羊毛vs真实价值增长"
            ])
            recommendations.extend([
                "明确增长目标：用户数/GMV/利润，选一个核心指标",
                "找到增长杠杆：一个能撬动全局的关键动作",
                "设计增长实验：小预算测试，快速迭代",
                "建立增长团队：跨部门增长小组，数据驱动"
            ])
        elif scenario['differentiation']:
            # 差异化优势
            insights.extend([
                "差异化=客户选择你不选对手的理由",
                "差异化层次：产品功能/用户体验/品牌形象/服务体验",
                "差异化可持续性：容易被模仿的差异化不是真差异化"
            ])
            recommendations.extend([
                "找到客户最在意的3个价值点",
                "在这3个点上做到行业第一",
                "传播差异化：让市场知道你的独特价值",
                "持续创新：差异化优势需要持续投入维护"
            ])
        elif scenario['new_product']:
            # 新产品上市
            insights.extend([
                "新产品上市成功率<30%，需要系统化方法",
                "上市前验证：MVP测试/种子用户反馈/竞品对标",
                "上市策略：狂轰滥炸vs低调测试vs逐步推广"
            ])
            recommendations.extend([
                "先在小范围试点，验证产品市场匹配度(PMF)",
                "设计上市launch计划：预热/首发/持续运营三阶段",
                "建立快速反馈机制，2周内根据市场反应调整",
                "准备B计划：如果首批反响平淡，如何调整定位"
            ])
        elif scenario['competition']:
            # 竞争分析
            insights.extend([
                "竞争分析核心是找出对手弱点和我方优势",
                "直接竞品vs间接竞品vs潜在替代方案",
                "竞争态势：领先/追平/落后，决定进攻/防守策略"
            ])
            recommendations.extend([
                "画出竞争雷达图：功能/价格/品牌/渠道/服务五维度",
                "找出对手最薄弱的1-2个维度，集中攻击",
                "建立竞争情报系统：定期监测对手动态",
                "考虑非对称竞争：避开对手优势，用我方优势打"
            ])
        else:
            # 通用战略规划
            insights.extend([
                f"战略核心：在哪里竞争、如何竞争、何时竞争",
                "内外部分析：SWOT+PEST，找出战略机会窗口",
                "资源匹配：战略目标需要对应的资源投入"
            ])
            recommendations.extend([
                "明确3-5年愿景，倒推年度战略目标",
                "战略规划需要一线输入，不能只靠高管拍脑袋",
                "建立战略里程碑，每季度review进度并调整"
            ])
        
        reasoning_chain.append(f"场景检测: {scenario}")
        reasoning_chain.append(f"置信度: {confidence:.2f}")
        reasoning_chain.append(f"生成{len(insights)}条洞察，{len(recommendations)}条建议")
        
        return self._create_result(
            success=True,
            result={
                "analysis": "战略分析完成",
                "problem_type": problem_type,
                "scenario": scenario,
                "insights": insights,
                "recommendations": recommendations
            },
            confidence=confidence,
            reasoning_chain=reasoning_chain,
            insights=insights,
            recommendations=recommendations
        )


class CauseAnalysisEngine(SubReasoningEngine):
    """因果分析增强引擎 - 精准定位问题根因"""
    
    def __init__(self):
        super().__init__(
            engine_id="cause_analysis",
            engine_name="因果分析引擎",
            category=EngineCategory.COGNITIVE,
            sub_type=None,
            description="精准分析问题的根本原因并提供可执行的改进建议",
            capability_score=0.92
        )
    
    def _detect_cause_scenario(self, query: str) -> Dict[str, bool]:
        """检测具体因果场景"""
        return {
            'complaint': any(kw in query for kw in ['投诉', '抱怨', '不满', '差评']),
            'churn': any(kw in query for kw in ['流失', '离开', '取消', '停用']),
            'delay': any(kw in query for kw in ['延迟', '延期', '推迟', '慢']),
            'sales_drop': any(kw in query for kw in ['下降', '下滑', '跌幅', '减少']) and any(kw in query for kw in ['销售', 'GMV', '营收', '收入']),
            'cost_rise': any(kw in query for kw in ['成本', '费用']) and any(kw in query for kw in ['上升', '增加', '提高']),
            'quality': any(kw in query for kw in ['质量', '缺陷', '故障', 'bug', '错误']),
            'positive': any(kw in query for kw in ['提升', '增长', '增加', '改善', '成功']),
        }
    
    def _calculate_confidence(self, query: str, scenario: Dict, numbers: List[float]) -> float:
        """动态计算置信度"""
        base = 0.75
        # 有具体数字，置信度更高
        if numbers:
            base += 0.10
        # 问题具体，置信度更高
        if scenario['complaint'] or scenario['churn'] or scenario['delay']:
            base += 0.05
        # 问题描述详细
        if len(query) > 30:
            base += 0.05
        return min(base, 0.95)
    
    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        query = input_data.get('query', '')
        observations = input_data.get('observations', [])
        potential_causes = input_data.get('potential_causes', [])
        
        reasoning_chain = ["【因果分析】"]
        insights = []
        recommendations = []
        
        # 场景检测
        scenario = self._detect_cause_scenario(query)
        import re
        numbers = []
        for match in re.findall(r'\d+(?:\.\d+)?%?', query):
            try:
                numbers.append(float(match.replace('%', '')))
            except:
                pass
        
        confidence = self._calculate_confidence(query, scenario, numbers)
        
        # 精准判断问题方向
        is_negative = scenario['complaint'] or scenario['churn'] or scenario['delay'] or scenario['sales_drop'] or scenario['cost_rise'] or scenario['quality']
        is_positive = scenario['positive'] and not is_negative
        
        if is_negative:
            # 负向变化 - 针对性分析
            if scenario['complaint']:
                insights.extend([
                    "投诉增加通常反映：产品缺陷/服务不到位/承诺未兑现",
                    "投诉内容分类可定位最严重问题（物流/质量/态度/流程）",
                    f"30%投诉增加可能触发口碑拐点，需立即响应"
                ])
                recommendations.extend([
                    "立即导出投诉明细，按问题类型分类统计",
                    "联系高频投诉用户，一对一沟通挽回",
                    "检查近期是否有政策/产品/人员变动导致投诉激增",
                    "设置投诉预警阈值：单日投诉>50单立即告警"
                ])
            
            elif scenario['churn']:
                insights.extend([
                    "用户流失通常遵循：不满→减少使用→尝试竞品→离开",
                    "流失前30天通常有行为信号：登录减少/功能使用下降",
                    f"15%流失率已属危险水平，需立即启动挽留"
                ])
                recommendations.extend([
                    "分析流失用户最后30天行为，找出共同触发事件",
                    "对高危流失用户（登录减少50%）主动触达",
                    "设计流失挽留机制：优惠/专属服务/新功能邀请",
                    "计算流失成本：获客成本是挽留成本的5-10倍"
                ])
            
            elif scenario['delay']:
                insights.extend([
                    "项目延迟通常由：需求变更/资源不足/风险未识别/依赖方延迟",
                    "延迟具有累积效应：前期延迟1周≠后期延迟1周",
                    "关键路径上的延迟对整体影响最大"
                ])
                recommendations.extend([
                    "立即重新评估关键路径，找出最大延迟风险点",
                    "启动每日站会，实时跟踪进度偏差",
                    "准备应急预案：加班/加人/缩减范围三选一",
                    "分析延迟根本原因：是估算不准还是执行不力"
                ])
            
            elif scenario['sales_drop']:
                insights.extend([
                    "销售额下降需拆解：流量下降/转化率下降/客单价下降",
                    "外部因素（市场/竞争/政策）vs内部因素（产品/价格/渠道）",
                    "下降是结构性还是季节性，决定应对策略"
                ])
                recommendations.extend([
                    "拆解销售漏斗，定位下降发生在哪个环节",
                    "对比竞争对手同期表现，判断是行业还是公司问题",
                    "启动销售异常分析：区域/产品/客户三段式拆解",
                    "制定销售提升计划：老客召回/新客获取/客单价提升三管齐下"
                ])
            
            else:
                # 通用负向分析
                insights.extend([
                    f"负向变化{numbers[0] if numbers else ''}%通常由多重因素叠加",
                    "直接原因（表面）vs根本原因（深层）需要5Why追问",
                    "相关性≠因果性，需控制变量验证"
                ])
                recommendations.extend([
                    "使用5Why分析法追问5层根本原因",
                    "对比变化前后的关键指标差异",
                    "绘制鱼骨图系统梳理人/机/料/法/环因素"
                ])
        
        elif is_positive:
            # 正向变化
            insights.extend([
                f"正向变化{numbers[0] if numbers else ''}%需评估：是趋势性增长还是偶然波动",
                "增长驱动力：产品优化/营销投放/外部事件/季节性因素",
                "警惕增长陷阱：补贴带来的增长不可持续"
            ])
            recommendations.extend([
                "分析增长的主要驱动因素，评估可持续性",
                "将成功经验抽象为标准流程，复制到其他业务",
                "监控增长拐点：当增速放缓时及时调整策略"
            ])
        
        else:
            # 无法判断方向
            insights.extend([
                "因果分析需要明确的问题定义",
                "区分必要原因（必须有）和充分原因（有了就够）",
                "考虑近因（直接）和远因（根因）的交互"
            ])
            recommendations.extend([
                "明确问题：要分析的是什么的因果关系",
                "收集多方面证据支持因果判断",
                "使用A/B测试验证因果关系"
            ])
        
        reasoning_chain.append(f"场景检测: {scenario}")
        reasoning_chain.append(f"量化数据: {numbers}")
        reasoning_chain.append(f"置信度: {confidence:.2f}")
        
        # 量化分析
        if numbers:
            main_change = numbers[0]
            is_large_change = abs(main_change) >= 10
            insights.append(f"变化幅度: {main_change}%，{'属于显著变化' if is_large_change else '属于小幅波动'}")
            if is_large_change:
                recommendations.append("显著变化需立即启动根因分析")
        
        return self._create_result(
            success=True,
            result={
                "analysis": "因果分析完成",
                "scenario": scenario,
                "causes_identified": insights,
                "query": query,
                "change_percentage": numbers[0] if numbers else None
            },
            confidence=confidence,  # 动态置信度
            reasoning_chain=reasoning_chain,
            insights=insights,
            recommendations=recommendations
        )


class DecisionAnalysisEngine(SubReasoningEngine):
    """决策分析增强引擎 - 针对性决策支持"""
    
    def __init__(self):
        super().__init__(
            engine_id="decision_analysis",
            engine_name="决策分析引擎",
            category=EngineCategory.DECISION,
            sub_type=None,
            description="针对性决策分析，提供可执行建议",
            capability_score=0.93
        )
    
    def _detect_decision_scenario(self, query: str) -> Dict[str, bool]:
        """检测具体决策场景"""
        return {
            'supplier': any(kw in query for kw in ['供应商', '供应', '采购']),
            'investment': any(kw in query for kw in ['投资', '预算', '回报', '回收']),
            'make_or_buy': any(kw in query for kw in ['自研', '外包', '外采', '采购']),
            'market_entry': any(kw in query for kw in ['进入', '市场', '城市', '区域']),
            'acquisition': any(kw in query for kw in ['收购', '并购', '竞争对手']),
            'product': any(kw in query for kw in ['产品', '功能', '特性']),
        }
    
    def _calculate_confidence(self, alternatives: List, criteria: List) -> float:
        """动态计算置信度"""
        base = 0.75
        if len(alternatives) >= 2:
            base += 0.10
        if len(criteria) >= 3:
            base += 0.05
        if len(alternatives) >= 3 and len(criteria) >= 3:
            base += 0.05  # 充分信息
        return min(base, 0.95)
    
    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        query = input_data.get('query', '')
        alternatives = input_data.get('alternatives', [])
        criteria = input_data.get('criteria', [])
        
        reasoning_chain = ["【决策分析】"]
        insights = []
        recommendations = []
        
        # 场景检测
        scenario = self._detect_decision_scenario(query)
        confidence = self._calculate_confidence(alternatives, criteria)
        
        # 分析决策类型
        if len(alternatives) > 1:
            # 识别决策场景类型
            if scenario['supplier']:
                # 供应商选择场景
                insights.extend([
                    "供应商选择核心：TCO（总拥有成本）而非只看采购价",
                    "评估维度：价格/质量/交期/服务/财务稳定性",
                    "风险：单一供应商风险 vs 多供应商管理成本"
                ])
                
                # 针对性建议
                for i, alt in enumerate(alternatives, 1):
                    alt_str = str(alt)
                    if 'A' in alt_str or '低' in alt_str:
                        insights.append(f"方案{i}（低价）：适合非核心物料/短期合作")
                        recommendations.append(f"方案{i}：小批量试单，验收合格后再扩大")
                    elif 'B' in alt_str or '高' in alt_str:
                        insights.append(f"方案{i}（高价）：适合核心物料/长期合作")
                        recommendations.append(f"方案{i}：要求提供成本结构分析，评估降价空间")
                
                recommendations.extend([
                    "建立供应商评分卡：价格30%、质量30%、交期20%、服务20%",
                    "要求两家提供样品或小规模试单，对比实际表现",
                    "评估供应商产能：能否应对你的需求波动"
                ])
                
            elif scenario['make_or_buy']:
                # 自研vs外包决策
                insights.extend([
                    "自研vs外包核心权衡：控制权/成本/速度/核心竞争力",
                    "自研适合：核心差异点/长期成本优势/技术积累",
                    "外包适合：非核心功能/快速上线/避免招聘难题"
                ])
                recommendations.extend([
                    "评估该功能是否是核心竞争力：是→自研，否→考虑外包",
                    "计算3年TCO：自研（人力成本+维护）vs外包（服务费）",
                    "考虑混合模式：核心自研+边缘外包",
                    "外包需评估：代码所有权/技术债务/替换成本"
                ])
                
            elif scenario['investment']:
                # 投资决策
                insights.extend([
                    "投资决策核心指标：NPV/IRR/回收期/风险调整后回报",
                    "500万预算属于中型投资，需严格评估",
                    "关注机会成本：这笔钱的其他用途回报是多少"
                ])
                recommendations.extend([
                    "计算DCF现金流折现，评估NPV是否>0",
                    "做情景分析：乐观/基准/悲观三种假设下的回报",
                    "评估如果项目失败，最大损失是多少，能否承受",
                    "考虑分阶段投资：先投20%验证，再决定是否继续"
                ])
                
            elif scenario['market_entry']:
                # 市场进入决策
                insights.extend([
                    "市场进入需评估：市场规模/竞争格局/进入壁垒/盈利能力",
                    "一线城市：红海但基础设施好；二线城市：蓝海但需教育",
                    "进入策略：自建/收购/合资/加盟，各有优劣"
                ])
                recommendations.extend([
                    "先做3个月小范围测试，验证市场需求",
                    "评估竞争对手反应：如果它们降价或跟进怎么办",
                    "计算单城市盈利模型，再决定扩张速度",
                    "考虑先进入二线城市树立标杆，再攻一线城市"
                ])
                
            elif scenario['acquisition']:
                # 收购决策
                insights.extend([
                    "收购核心：1+1>2的协同效应是否真实存在",
                    "估值陷阱：避免为市场份额付过高溢价",
                    "整合风险：文化冲突/人才流失往往被低估"
                ])
                recommendations.extend([
                    "先做深度尽调：财务/法律/业务/技术/人事五维度",
                    "明确收购目的：消灭对手/获取技术/扩大规模，不同目的评估重点不同",
                    "设计对赌协议：如果承诺业绩未达成，降低收购价",
                    "制定整合Plan B：如果核心团队离职，如何维持业务"
                ])
                
            else:
                # 通用决策
                insights.extend([
                    f"决策核心：明确{len(alternatives)}个方案的评估标准",
                    "量化+定性结合：有些因素（如品牌）难以量化但很重要",
                    "考虑决策可逆性：可逆决策可快速试错，不可逆决策需谨慎"
                ])
                recommendations.extend([
                    "建立多准则决策矩阵，给每个标准分配权重",
                    "请3个相关专家独立打分，减少个人偏见",
                    "做敏感性分析：如果关键假设变化，结论是否改变"
                ])
        
        else:
            # 无明确备选方案
            insights.extend([
                "决策首先需要明确备选方案",
                "好的决策=好的备选方案+好的选择方法",
                "拓展备选方案：通常第一个想法不是最好的"
            ])
            recommendations.extend([
                "头脑风暴：至少想出5个备选方案再筛选",
                "借鉴行业案例：类似决策别人是怎么做的",
                "考虑'不行动'也是一个备选方案"
            ])
        
        reasoning_chain.append(f"场景检测: {scenario}")
        reasoning_chain.append(f"备选方案数: {len(alternatives)}")
        reasoning_chain.append(f"置信度: {confidence:.2f}")
        
        return self._create_result(
            success=True,
            result={
                "analysis": "决策分析完成",
                "scenario": scenario,
                "alternatives_count": len(alternatives),
                "criteria": criteria,
                "recommendations": recommendations
            },
            confidence=confidence,  # 动态置信度
            reasoning_chain=reasoning_chain,
            insights=insights,
            recommendations=recommendations
        )


class TrendAnalysisEngine(SubReasoningEngine):
    """趋势分析增强引擎 - 针对性趋势预测"""
    
    def __init__(self):
        super().__init__(
            engine_id="trend_analysis",
            engine_name="趋势分析引擎",
            category=EngineCategory.ANALYTICAL,
            sub_type=None,
            description="分析趋势和预测未来发展",
            capability_score=0.90
        )
    
    def _detect_trend_scenario(self, query: str) -> Dict[str, bool]:
        """检测趋势分析场景"""
        return {
            'industry': any(kw in query for kw in ['行业', '市场趋势', '产业']),
            'user_behavior': any(kw in query for kw in ['用户', '行为', '习惯', '偏好']),
            'tech': any(kw in query for kw in ['技术', 'AI', '数字化', '科技']),
            'predict': '预测' in query or '未来' in query,
            'growth': any(kw in query for kw in ['增长', '趋势', '变化']),
        }
    
    def _calculate_confidence(self, time_series: List, scenario: Dict) -> float:
        """动态计算置信度"""
        base = 0.65  # 无数据时基础置信度
        if len(time_series) >= 5:
            base += 0.15
        elif len(time_series) >= 3:
            base += 0.10
        if scenario['industry'] or scenario['tech']:
            base += 0.05  # 专业领域置信度稍低
        return min(base, 0.90)
    
    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        query = input_data.get('query', '')
        time_series = input_data.get('time_series', [])
        
        reasoning_chain = ["【趋势分析】"]
        insights = []
        recommendations = []
        
        # 场景检测
        scenario = self._detect_trend_scenario(query)
        confidence = self._calculate_confidence(time_series, scenario)
        
        # 分析趋势方向
        if len(time_series) >= 2:
            first = time_series[0]
            last = time_series[-1]
            change = (last - first) / max(0.001, first) if first != 0 else 0
            
            if change > 0.1:
                insights.append(f"数据显示上升趋势，变化幅度{change*100:.1f}%")
                recommendations.append("抓住增长机遇，加速扩张")
                recommendations.append("警惕增长放缓的拐点")
            elif change < -0.1:
                insights.append(f"数据显示下降趋势，变化幅度{change*100:.1f}%")
                recommendations.append("分析下降原因，制定扭转策略")
                recommendations.append("控制成本，保持现金流")
            else:
                insights.append("数据显示相对平稳")
                recommendations.append("寻找突破机会")
        else:
            # 无数据时的场景化分析
            if scenario['industry']:
                insights.extend([
                    "行业趋势分析需要多维度数据：政策/技术/人口/竞争格局",
                    "判断趋势所处阶段：导入期/成长期/成熟期/衰退期",
                    "关注趋势的加速度：增速放缓可能预示拐点"
                ])
                recommendations.extend([
                    "收集行业报告：艾瑞/36kr/行业白皮书",
                    "访谈行业专家：一手信息更可靠",
                    "监测先行指标：政策变化/技术突破往往领先市场"
                ])
            elif scenario['user_behavior']:
                insights.extend([
                    "用户行为趋势反映真实需求变化",
                    "代际差异明显：Z世代 vs Y世代 vs X世代偏好不同",
                    "行为数据比态度数据更可靠（用户说什么vs做什么）"
                ])
                recommendations.extend([
                    "分析自有用户数据：DAU/MAU/留存/转化趋势",
                    "做用户调研问卷：了解态度变化",
                    "关注新渠道/新玩法：往往预示用户行为变迁"
                ])
            elif scenario['tech']:
                insights.extend([
                    "技术趋势分析关注：新技术采用曲线（Gartner Hype Cycle）",
                    "技术成熟度=商业化可行性（实验室≠商业化）",
                    "AI对行业的渗透速度超预期，需提前布局"
                ])
                recommendations.extend([
                    "跟踪技术源头：斯坦福AI报告/MIT技术评论",
                    "关注大厂技术动态：往往代表行业方向",
                    "小步快跑验证：技术选型用MVP测试"
                ])
            elif scenario['predict']:
                insights.extend([
                    "趋势预测需要考虑：历史模式/当前状态/外部因素",
                    "短期预测（1年内）准确度 > 长期预测（3-5年）",
                    "黑天鹅事件可能完全改变趋势"
                ])
                recommendations.extend([
                    "建立预测模型：定性（专家）+定量（数据）结合",
                    "设置置信区间：给出乐观/基准/悲观三种情景",
                    "定期review和更新预测，趋势会随时间变化"
                ])
            else:
                insights.extend([
                    "趋势分析需要明确：是分析什么对象/什么时间范围的趋势",
                    "建议补充数据：历史数据越多，趋势判断越准确"
                ])
                recommendations.extend([
                    "明确分析对象：用户/销售/产品/行业",
                    "确定时间范围：短期（季度）/中期（年）/长期（3年+）"
                ])
        
        # 补充趋势分析通用方法
        if scenario['predict'] or scenario['growth']:
            insights.extend([
                "趋势预测需要考虑：历史模式/当前状态/外部因素",
                "短期预测准确度高于长期预测",
                "外部冲击可能改变原有趋势"
            ])
            recommendations.extend([
                "结合定性分析补充定量预测",
                "建立预测模型的置信区间",
                "定期更新预测，及时调整策略"
            ])
        
        reasoning_chain.append(f"场景检测: {scenario}")
        reasoning_chain.append(f"数据点: {len(time_series)}")
        reasoning_chain.append(f"置信度: {confidence:.2f}")
        
        return self._create_result(
            success=True,
            result={
                "analysis": "趋势分析完成",
                "scenario": scenario,
                "time_series_length": len(time_series),
                "insights": insights
            },
            confidence=confidence,  # 动态置信度
            reasoning_chain=reasoning_chain,
            insights=insights,
            recommendations=recommendations
        )


class RiskAnalysisEngine(SubReasoningEngine):
    """风险分析增强引擎 - 针对性风险识别与应对"""
    
    def __init__(self):
        super().__init__(
            engine_id="risk_analysis",
            engine_name="风险分析引擎",
            category=EngineCategory.STRATEGIC,
            sub_type=None,
            description="精准识别风险并提供应对策略",
            capability_score=0.91
        )
    
    def _detect_risk_scenario(self, query: str) -> Dict[str, bool]:
        """检测风险分析场景"""
        return {
            'project': any(kw in query for kw in ['项目', '计划', '里程碑']),
            'market': any(kw in query for kw in ['市场', '竞争', '份额']),
            'compliance': any(kw in query for kw in ['合规', '法律', '监管', '政策']),
            'technology': any(kw in query for kw in ['技术', '系统', '故障', 'bug']),
            'financial': any(kw in query for kw in ['财务', '资金', '现金流', '成本']),
            'operational': any(kw in query for kw in ['运营', '供应链', '渠道']),
        }
    
    def _calculate_confidence(self, risk_factors: List, scenario: Dict) -> float:
        """动态计算置信度"""
        base = 0.70
        if len(risk_factors) >= 3:
            base += 0.10
        if scenario['project'] or scenario['compliance']:
            base += 0.05
        return min(base, 0.92)
    
    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        query = input_data.get('query', '')
        risk_factors = input_data.get('risk_factors', [])
        likelihood = input_data.get('likelihood', 0.5)
        impact = input_data.get('impact', 0.5)
        
        reasoning_chain = ["【风险分析】"]
        insights = []
        recommendations = []
        
        # 场景检测
        scenario = self._detect_risk_scenario(query)
        confidence = self._calculate_confidence(risk_factors, scenario)
        
        # 计算风险评分
        risk_score = likelihood * impact
        risk_level = "高" if risk_score > 0.5 else "中" if risk_score > 0.25 else "低"
        
        insights.extend([
            f"风险评分: {risk_score:.2f} ({risk_level}风险)",
            f"发生可能性: {likelihood*100:.0f}%, 影响程度: {impact*100:.0f}%",
            "风险识别需要全面扫描内部和外部环境",
            "风险之间可能存在关联和叠加效应"
        ])
        
        # 场景化风险分析
        if scenario['project']:
            insights.extend([
                "项目风险核心：范围蔓延/资源不足/技术难题/需求变更",
                "识别关键路径风险：任何关键路径上的延迟都会影响整体",
                "风险往往发生在跨团队协作边界"
            ])
            recommendations.extend([
                "建立项目风险登记册，识别>20个潜在风险",
                "每周进行风险review，及时发现新风险",
                "为高风险项准备Plan B（应急预案）",
                "关键里程碑前设置缓冲时间"
            ])
            
        elif scenario['market']:
            insights.extend([
                "市场风险核心：需求变化/竞争加剧/政策调整",
                "警惕竞争对手的非理性行为（价格战/恶意竞争）",
                "市场风险往往来得快且难以预测"
            ])
            recommendations.extend([
                "建立竞争情报系统，实时监测对手动态",
                "保持产品差异化，避免陷入同质化竞争",
                "多元化收入来源，降低单一市场依赖",
                "储备足够的现金流，应对市场波动"
            ])
            
        elif scenario['compliance']:
            insights.extend([
                "合规风险核心：政策变化/监管收紧/历史违规",
                "合规风险往往具有滞后性（今天的问题来自过去的决策）",
                "跨境业务需同时满足多个司法管辖区的合规要求"
            ])
            recommendations.extend([
                "聘请专业律师/合规顾问，建立合规审查流程",
                "定期进行合规自查，发现问题及时整改",
                "关注监管动态：政策征求意见稿往往是监管方向的信号",
                "建立合规培训机制，全员合规意识"
            ])
            
        elif scenario['technology']:
            insights.extend([
                "技术风险核心：系统故障/数据泄露/技术债务",
                "技术风险往往在业务高峰期爆发",
                "历史数据显示：重大故障90%由变更引起"
            ])
            recommendations.extend([
                "建立完善的监控告警体系（APM/日志/链路追踪）",
                "核心系统做多活/容灾设计，避免单点故障",
                "建立变更管理流程：变更前评估风险，变更后验证",
                "定期进行故障演练，验证应急预案有效性"
            ])
            
        elif scenario['financial']:
            insights.extend([
                "财务风险核心：现金流断裂/坏账/汇率波动",
                "创业公司死亡的第一原因通常是现金流问题",
                "财务风险具有隐蔽性：报表健康≠现金流健康"
            ])
            recommendations.extend([
                "建立现金流预测模型，提前6个月预测资金需求",
                "控制应收账款周期，加速资金回笼",
                "保持12个月以上的现金储备（经济不好时更多）",
                "多元化融资渠道，避免单一依赖"
            ])
            
        elif scenario['operational']:
            insights.extend([
                "运营风险核心：供应链中断/质量事故/人员流失",
                "供应链风险往往在危机时暴露（疫情/战争）",
                "核心员工流失是运营中断的重要原因"
            ])
            recommendations.extend([
                "建立供应商风险评估机制，不依赖单一供应商",
                "关键岗位建立备份机制，避免人员单点",
                "建立质量管理体系，预防质量事故",
                "定期进行业务连续性演练"
            ])
            
        else:
            # 通用风险分析
            insights.extend([
                "风险管理核心：识别→评估→应对→监控",
                "风险按概率×影响计算，分为可接受/需缓解/需规避三类",
                "最好的风险应对是预防，而非事后补救"
            ])
            recommendations.extend([
                "建立风险管理框架：定期风险识别和评估",
                "为高风险项准备应急预案",
                "培养全员风险意识，让风险可见",
                "定期review风险管理效果，持续改进"
            ])
        
        # 风险等级应对
        if risk_level == "高":
            recommendations.extend([
                "高风险需要立即关注，制定缓解计划",
                "考虑风险规避或转移策略（如保险/对冲）",
                "建立风险预警机制，设定触发阈值"
            ])
        elif risk_level == "中":
            recommendations.extend([
                "中等风险需要持续监控，定期评估",
                "准备风险应对预案，明确责任人"
            ])
        else:
            recommendations.extend([
                "低风险可接受监控，保持关注",
                "将精力集中在中高风险项"
            ])
        
        reasoning_chain.append(f"场景检测: {scenario}")
        reasoning_chain.append(f"风险评分: {risk_score:.2f} ({risk_level})")
        reasoning_chain.append(f"置信度: {confidence:.2f}")
        
        return self._create_result(
            success=True,
            result={
                "analysis": "风险分析完成",
                "scenario": scenario,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "likelihood": likelihood,
                "impact": impact
            },
            confidence=confidence,  # 动态置信度
            reasoning_chain=reasoning_chain,
            insights=insights,
            recommendations=recommendations
        )


# 注册增强引擎
def register_enhanced_engines():
    """注册增强引擎"""
    engines = [
        StrategicAnalysisEngine(),
        CauseAnalysisEngine(),
        DecisionAnalysisEngine(),
        TrendAnalysisEngine(),
        RiskAnalysisEngine(),
    ]
    
    for engine in engines:
        GLOBAL_ENGINE_REGISTRY.register(engine)
    
    return engines
