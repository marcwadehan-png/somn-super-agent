"""
吕氏春秋智慧fusion引擎
=================

fusion<吕氏春秋>杂家智慧的decision系统

版本: v1.0.0
作者: Somn AI
日期: 2026-04-02

<吕氏春秋>核心思想:
- 以道家为基调:黄老道家思想
- 兼容并包:兼儒墨合名法
- 贵公去私:天下为公
- 察今知古:因时变法
- 兼听则明:听取谏言
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime

class WisdomSchool(Enum):
    """学派分类"""
    DAO = "道家"
    RU = "儒家"
    FA = "法家"
    MO = "墨家"
    BING = "兵家"
    YINYANG = "阴阳家"
    ZAJIA = "杂家"  # fusion

class Season(Enum):
    """四季"""
    SPRING = "春"
    SUMMER = "夏"
    AUTUMN = "秋"
    WINTER = "冬"

class Month(Enum):
    """十二月"""
    MENG_CHUN = "孟春"
    ZHONG_CHUN = "仲春"
    JI_CHUN = "季春"
    MENG_XIA = "孟夏"
    ZHONG_XIA = "仲夏"
    JI_XIA = "季夏"
    MENG_QIU = "孟秋"
    ZHONG_QIU = "仲秋"
    JI_QIU = "季秋"
    MENG_DONG = "孟冬"
    ZHONG_DONG = "仲冬"
    JI_DONG = "季冬"

@dataclass
class WisdomPrinciple:
    """智慧原则"""
    name: str
    school: WisdomSchool
    core_text: str
    explanation: str
    modern_interpretation: str
    application_scenarios: List[str]
    examples: List[str]

@dataclass
class TimeContext:
    """时势语境"""
    season: Optional[Season] = None
    month: Optional[Month] = None
    era_trend: str = ""  # 时代趋势
    social_mood: str = ""  # 社会氛围
    political_climate: str = ""  # 政治气候

@dataclass
class DecisionContext:
    """decision语境"""
    situation: str  # 情境类型
    stakeholders: List[str] = field(default_factory=list)  # 利益相关者
    time_context: TimeContext = field(default_factory=TimeContext)
    resources: Dict[str, Any] = field(default_factory=dict)  # 资源
    constraints: List[str] = field(default_factory=list)  # 约束

class LvShiWisdomCore:
    """吕氏春秋智慧核心"""
    
    def __init__(self):
        self.principles = self._init_principles()
        self.month_wisdom = self._init_month_wisdom()
    
    def _init_principles(self) -> Dict[str, WisdomPrinciple]:
        """init核心智慧原则"""
        return {
            # ========== 黄老道家思想 ==========
            "道法自然": WisdomPrinciple(
                name="道法自然",
                school=WisdomSchool.DAO,
                core_text="民无道知天,民以四时寒暑日月星辰之行知天.",
                explanation="百姓通过四时寒暑日月的运行来理解天道.",
                modern_interpretation="遵循自然规律,顺应时代潮流,不违背客观规律行事.",
                application_scenarios=[
                    "制定长期战略时考虑客观条件",
                    "顺应行业发展趋势",
                    "遵循事物发展的客观规律"
                ],
                examples=[
                    "企业战略顺应市场规律",
                    "个人发展顺应时代趋势",
                    "政策制定顺应民意"
                ]
            ),
            
            "无为而治": WisdomPrinciple(
                name="无为而治",
                school=WisdomSchool.DAO,
                core_text="无为者,君道也.",
                explanation="君主应当清静守法,不妄为,不扰民.",
                modern_interpretation="高层领导把握大势,不过度干预,让下属发挥主动性.",
                application_scenarios=[
                    "企业管理中的授权",
                    "政府治理中的简政放权",
                    "领导艺术中的放手"
                ],
                examples=[
                    "刘邦的无为而治",
                    "现代企业的扁平化管理",
                    "政府的负面清单制度"
                ]
            ),
            
            "因时变法": WisdomPrinciple(
                name="因时变法",
                school=WisdomSchool.DAO,
                core_text="故择先王之成法,而法其所以为法.先王之所以为法者,人也.",
                explanation="不应死守先王成法,而应学习其制定法度的原则,因时制宜.",
                modern_interpretation="不拘泥于过去的做法,根据当前实际情况灵活调整strategy.",
                application_scenarios=[
                    "商业模式创新",
                    "管理方式改革",
                    "政策调整优化"
                ],
                examples=[
                    "商鞅变法因时制宜",
                    "企业转型升级",
                    "改革开放与时俱进"
                ]
            ),
            
            # ========== 儒家思想 ==========
            "仁政": WisdomPrinciple(
                name="仁政",
                school=WisdomSchool.RU,
                core_text="仁者,爱人.",
                explanation="以仁爱之心待人,以仁政治理国家.",
                modern_interpretation="以用户为中心,关注利益相关者的福祉.",
                application_scenarios=[
                    "客户服务理念",
                    "社会责任履行",
                    "人文关怀"
                ],
                examples=[
                    "以用户为中心的经营理念",
                    "企业的社会责任",
                    "公共政策的民生导向"
                ]
            ),
            
            "孝道": WisdomPrinciple(
                name="孝道",
                school=WisdomSchool.RU,
                core_text="孝悌也者,其为仁之本与.",
                explanation="孝顺父母,敬爱兄长,是仁爱的根本.",
                modern_interpretation="感恩回报,尊重传统,传承文化.",
                application_scenarios=[
                    "企业文化中的感恩",
                    "团队建设中的尊重",
                    "品牌文化中的传承"
                ],
                examples=[
                    "企业的家文化",
                    "感恩回馈社会",
                    "文化传承"
                ]
            ),
            
            "中庸之道": WisdomPrinciple(
                name="中庸之道",
                school=WisdomSchool.RU,
                core_text="极高明而道中庸.",
                explanation="追求高明的境界而以中庸之道行之.",
                modern_interpretation="不走极端,寻求平衡与和谐.",
                application_scenarios=[
                    "平衡短期与长期利益",
                    "协调各方利益诉求",
                    "把握做事分寸"
                ],
                examples=[
                    "企业的稳健经营",
                    "政策的平衡取舍",
                    "人生的智慧抉择"
                ]
            ),
            
            # ========== 法家思想 ==========
            "法治": WisdomPrinciple(
                name="法治",
                school=WisdomSchool.FA,
                core_text="法不远义,近民情也.",
                explanation="法律不应远离道义,要接近民情.",
                modern_interpretation="制度建设要合理,既要有原则性,也要有灵活性.",
                application_scenarios=[
                    "企业制度建设",
                    "流程规范制定",
                    "奖惩机制设计"
                ],
                examples=[
                    "现代企业管理制度",
                    "绩效考核体系",
                    "合规管理体系"
                ]
            ),
            
            "赏罚分明": WisdomPrinciple(
                name="赏罚分明",
                school=WisdomSchool.FA,
                core_text="赏罚信,政事胜.",
                explanation="赏罚守信用,政事就能成功.",
                modern_interpretation="激励机制要公平公正,说到做到.",
                application_scenarios=[
                    "绩效激励",
                    "晋升机制",
                    "责任追究"
                ],
                examples=[
                    "大秦指标考核制度",
                    "股权激励计划",
                    "问责制度"
                ]
            ),
            
            # ========== 墨家思想 ==========
            "兼爱": WisdomPrinciple(
                name="兼爱",
                school=WisdomSchool.MO,
                core_text="视人之国,若视其国;视人之家,若视其家.",
                explanation="看待别人的国家像自己的国家,看待别人的家像自己的家.",
                modern_interpretation="换位思考,利益共享,合作共赢.",
                application_scenarios=[
                    "战略合作伙伴关系",
                    "利益相关者管理",
                    "社会责任履行"
                ],
                examples=[
                    "供应链共赢模式",
                    "生态圈建设",
                    "社会企业"
                ]
            ),
            
            "节用": WisdomPrinciple(
                name="节用",
                school=WisdomSchool.MO,
                core_text="节用之本,在于反本.",
                explanation="节约的根本在于回到根本.",
                modern_interpretation="资源要用在刀刃上,追求实效.",
                application_scenarios=[
                    "成本控制",
                    "资源优化配置",
                    "精益管理"
                ],
                examples=[
                    "精益生产",
                    "降本增效",
                    "节能减排"
                ]
            ),
            
            # ========== 吕氏春秋特有 ==========
            "贵公去私": WisdomPrinciple(
                name="贵公去私",
                school=WisdomSchool.ZAJIA,
                core_text="天无私覆也,地无私载也,日月无私烛也,四时无私行也.",
                explanation="天地日月四时都是公正无私的,治理者应效法这种公正.",
                modern_interpretation="做事公正,不谋私利,追求公共利益最大化.",
                application_scenarios=[
                    "公共decision",
                    "资源分配",
                    "利益协调"
                ],
                examples=[
                    "政府采购的公正透明",
                    "公共资源的公平分配",
                    "利益冲突的公正处理"
                ]
            ),
            
            "兼听则明": WisdomPrinciple(
                name="兼听则明",
                school=WisdomSchool.ZAJIA,
                core_text="贤主所贵莫如士.所以贵士,为其直言也.言直则枉者见矣.",
                explanation="贤明的君主最看重士人,因为士人能直言.直言才能发现错误.",
                modern_interpretation="广开言路,听取不同意见,避免偏听偏信.",
                application_scenarios=[
                    "decision前的调研",
                    "团队讨论",
                    "风险评估"
                ],
                examples=[
                    "民主decision机制",
                    "专家咨询制度",
                    "意见反馈渠道"
                ]
            ),
            
            "慎大览微": WisdomPrinciple(
                name="慎大览微",
                school=WisdomSchool.ZAJIA,
                core_text="有道之士,贵以近知远,以今知古,以益所见,知所不见.",
                explanation="有道之人,贵在能从近处知道远处,从现在知道过去.",
                modern_interpretation="见微知著,通过细节推断全局.",
                application_scenarios=[
                    "市场趋势judge",
                    "风险预警",
                    "趋势分析"
                ],
                examples=[
                    "从用户反馈看产品方向",
                    "从数据看市场变化",
                    "从细节发现本质"
                ]
            ),
            
            "圆道": WisdomPrinciple(
                name="圆道",
                school=WisdomSchool.ZAJIA,
                core_text="日夜一周,圆道也.精行四时,一上一下.",
                explanation="日月的运行是周而复始的,这就是圆道.",
                modern_interpretation="事物发展是循环往复的,要把握周期规律.",
                application_scenarios=[
                    "经济周期把握",
                    "行业发展周期",
                    "个人成长周期"
                ],
                examples=[
                    "宏观经济周期投资",
                    "行业发展周期战略",
                    "个人职业周期规划"
                ]
            ),
            
            "察今": WisdomPrinciple(
                name="察今",
                school=WisdomSchool.ZAJIA,
                core_text="故察己则可以知人,察今则可以知古.古今一也,人与我同耳.",
                explanation="了解自己就能了解别人,了解现在就能知道过去.",
                modern_interpretation="以史为鉴,但要根据现实灵活应用.",
                application_scenarios=[
                    "历史经验借鉴",
                    "标杆学习",
                    "模式创新"
                ],
                examples=[
                    "从历史看未来",
                    "借鉴成功案例",
                    "在继承中创新"
                ]
            ),
            
            "求人之志": WisdomPrinciple(
                name="求人之志",
                school=WisdomSchool.ZAJIA,
                core_text="任力者故劳,任人者故逸.",
                explanation="依靠自己力量的人劳累,依靠别人的人安逸.",
                modern_interpretation="善于借助外力,整合资源.",
                application_scenarios=[
                    "资源整合",
                    "合作共赢",
                    "杠杆效应"
                ],
                examples=[
                    "平台模式",
                    "生态合作",
                    "借力发展"
                ]
            ),
        }
    
    def _init_month_wisdom(self) -> Dict[Month, Dict]:
        """init十二月智慧"""
        return {
            Month.MENG_CHUN: {
                "theme": "生发",
                "advice": "顺应春生之气,开始新的计划",
                "action": "播种,规划,创新"
            },
            Month.ZHONG_CHUN: {
                "theme": "生长",
                "advice": "万物生长,适合推动发展",
                "action": "执行,推进,扩张"
            },
            Month.JI_CHUN: {
                "theme": "成就",
                "advice": "春季将尽,总结阶段成果",
                "action": "评估,调整,巩固"
            },
            Month.MENG_XIA: {
                "theme": "成长",
                "advice": "夏季开始,全力发展",
                "action": "冲刺,突破,占领"
            },
            Month.ZHONG_XIA: {
                "theme": "繁盛",
                "advice": "事物达到鼎盛",
                "action": "巩固,维护,深化"
            },
            Month.JI_XIA: {
                "theme": "转化",
                "advice": "夏季将尽,准备转变",
                "action": "转型,准备,储备"
            },
            Month.MENG_QIU: {
                "theme": "收敛",
                "advice": "秋季开始,收敛锋芒",
                "action": "优化,整理,储备"
            },
            Month.ZHONG_QIU: {
                "theme": "收获",
                "advice": "收获季节,收取成果",
                "action": "收获,总结,传承"
            },
            Month.JI_QIU: {
                "theme": "储藏",
                "advice": "秋季将尽,准备过冬",
                "action": "储藏,休养,培训"
            },
            Month.MENG_DONG: {
                "theme": "藏养",
                "advice": "冬季开始,休养生息",
                "action": "学习,思考,规划"
            },
            Month.ZHONG_DONG: {
                "theme": "蛰伏",
                "advice": "事物潜藏,等待时机",
                "action": "蛰伏,等待,观察"
            },
            Month.JI_DONG: {
                "theme": "孕育",
                "advice": "冬季将尽,孕育新生",
                "action": "准备,孕育,期待"
            },
        }
    
    def get_wisdom(self, principle_name: str) -> Optional[WisdomPrinciple]:
        """get智慧原则"""
        return self.principles.get(principle_name)
    
    def get_month_wisdom(self, month: Month) -> Dict:
        """get月度智慧"""
        return self.month_wisdom.get(month, {})
    
    def get_school_wisdom(self, school: WisdomSchool) -> List[WisdomPrinciple]:
        """get学派智慧"""
        return [p for p in self.principles.values() if p.school == school]

class TimeSituationAnalyzer:
    """时势分析器 - 吕氏春秋智慧"""
    
    def __init__(self):
        self.core = LvShiWisdomCore()
    
    def analyze(self, context: DecisionContext) -> Dict:
        """分析时势"""
        result = {
            "situation_type": self._classify_situation(context),
            "recommendations": [],
            "warnings": [],
            "opportunities": [],
            "wisdom_applications": []
        }
        
        # 分析情境
        situation = result["situation_type"]
        
        # 根据情境给出建议
        if situation == "创始期":
            result["recommendations"].append("效法孟春'生发'之道,开始新计划")
            result["wisdom_applications"].append("因时变法")
        elif situation == "发展期":
            result["recommendations"].append("顺应夏季'成长'之势,全力发展")
            result["wisdom_applications"].append("道法自然")
        elif situation == "成熟期":
            result["recommendations"].append("借鉴秋季'收敛'之理,优化整理")
            result["wisdom_applications"].append("中庸之道")
        elif situation == "转型期":
            result["recommendations"].append("学习冬季'藏养'之道,蛰伏待机")
            result["wisdom_applications"].append("无为而治")
        
        # 添加警示
        if context.time_context.era_trend:
            result["warnings"].append(f"注意时代趋势:{context.time_context.era_trend}")
        
        # 发现机会
        result["opportunities"].extend(self._discover_opportunities(context))
        
        return result
    
    def _classify_situation(self, context: DecisionContext) -> str:
        """分类情境"""
        situation = context.situation
        
        if any(k in situation for k in ["创始", "新建", "起步", "孟春"]):
            return "创始期"
        elif any(k in situation for k in ["发展", "扩张", "增长", "夏季"]):
            return "发展期"
        elif any(k in situation for k in ["成熟", "稳定", "收获", "秋季"]):
            return "成熟期"
        elif any(k in situation for k in ["转型", "衰退", "变革", "冬季"]):
            return "转型期"
        else:
            return "常态期"
    
    def _discover_opportunities(self, context: DecisionContext) -> List[str]:
        """发现机会"""
        opportunities = []
        
        # 从资源中发现
        for resource, value in context.resources.items():
            try:
                if isinstance(value, (int, float)) and value > 0.8:
                    opportunities.append(f"资源{resource}充足,可重点发展")
            except (TypeError, ValueError):
                pass
        
        # 从时间语境中发现
        if context.time_context.season:
            opportunities.append(
                f"当前{context.time_context.season.value}季"
            )
        
        return opportunities

class InclusiveWisdomEngine:
    """兼容并包智慧引擎"""
    
    def __init__(self):
        self.core = LvShiWisdomCore()
    
    def integrate(self, 
                 perspectives: List[Tuple[str, WisdomSchool]], 
                 context: DecisionContext) -> Dict:
        """整合多方视角"""
        insights = {}
        
        for name, school in perspectives:
            school_wisdom = self.core.get_school_wisdom(school)
            insights[name] = [w.explanation for w in school_wisdom]
        
        # 分析各学派观点的异同
        analysis = self._analyze_perspectives(insights, context)
        
        return {
            "perspectives": insights,
            "analysis": analysis,
            "synthesis": self._synthesize(analysis, context),
            "recommendation": self._make_recommendation(analysis)
        }
    
    def _analyze_perspectives(self, insights: Dict, context: DecisionContext) -> Dict:
        """分析各方观点"""
        return {
            "common_points": self._find_common_points(insights),
            "differences": self._find_differences(insights),
            "context_fit": self._evaluate_context_fit(insights, context)
        }
    
    def _find_common_points(self, insights: Dict) -> List[str]:
        """寻找共同点"""
        if insights:
            first = list(insights.values())[0]
            return first[:2] if len(first) >= 2 else first
        return []
    
    def _find_differences(self, insights: Dict) -> List[str]:
        """寻找差异点"""
        return ["不同学派切入点不同,可相互补充"]
    
    def _evaluate_context_fit(self, insights: Dict, context: DecisionContext) -> Dict:
        """评估语境契合度"""
        return {
            "overall_fit": 0.8,
            "notes": "需根据具体情境选择合适学派"
        }
    
    def _synthesize(self, analysis: Dict, context: DecisionContext) -> str:
        """synthesize各方观点"""
        synthesis = "synthesize分析:\n"
        
        if analysis["common_points"]:
            synthesis += f"1. 各方共识:{','.join(analysis['common_points'][:2])}\n"
        
        if analysis["differences"]:
            synthesis += f"2. 分歧点:{analysis['differences'][0]}\n"
        
        synthesis += f"3. 情境契合度:{analysis['context_fit']['overall_fit']:.0%}\n"
        
        return synthesis
    
    def _make_recommendation(self, analysis: Dict) -> str:
        """给出建议"""
        fit = analysis["context_fit"]["overall_fit"]
        
        if fit > 0.8:
            return "建议采纳当前方案,同时兼顾各方观点"
        elif fit > 0.5:
            return "建议在采纳主流观点的同时,注意补充其他视角"
        else:
            return "建议重新审视问题,多方论证后再decision"

class PublicFirstDecision:
    """贵公去私decision系统"""
    
    def __init__(self):
        self.core = LvShiWisdomCore()
    
    def evaluate(self, options: List[Dict]) -> Dict:
        """评估选项的公私属性"""
        evaluations = []
        
        for option in options:
            evaluation = self._evaluate_single(option)
            evaluations.append(evaluation)
        
        # 按公利排序
        evaluations.sort(key=lambda x: x["public_score"] - x["private_cost"], reverse=True)
        
        return {
            "rankings": evaluations,
            "best_option": evaluations[0]["name"] if evaluations else None,
            "recommendation": self._make_recommendation(evaluations)
        }
    
    def _evaluate_single(self, option: Dict) -> Dict:
        """评估单个选项"""
        public_score = option.get("public_value", 0.5)
        private_cost = option.get("private_cost", 0.5)
        
        return {
            "name": option.get("name", "未命名"),
            "public_score": public_score,
            "private_cost": private_cost,
            "net_score": public_score - private_cost,
            "assessment": self._assess(option)
        }
    
    def _assess(self, option: Dict) -> str:
        """给出评估"""
        public = option.get("public_value", 0.5)
        private = option.get("private_cost", 0.5)
        
        if public > 0.7 and private < 0.3:
            return "公利优先,私利兼顾的上选"
        elif public > 0.5:
            return "公利大于私利的可行方案"
        else:
            return "私利过重,需要重新审视"
    
    def _make_recommendation(self, evaluations: List[Dict]) -> str:
        """给出建议"""
        if not evaluations:
            return "无选项可评估"
        
        best = evaluations[0]
        
        if best["net_score"] > 0.3:
            return f"建议选择方案'{best['name']}',符合贵公去私原则"
        elif best["net_score"] > 0:
            return f"方案'{best['name']}'勉强可行,但需改进"
        else:
            return "所有方案私利过重,建议重新设计"

class YinYangBalanceDecision:
    """阴阳平衡decision系统"""
    
    def __init__(self):
        self.yin_aspects = ["柔", "静", "阴", "内", "隐", "守"]
        self.yang_aspects = ["刚", "动", "阳", "外", "显", "攻"]
    
    def balance(self, context: DecisionContext) -> Dict:
        """阴阳平衡"""
        # 分析当前状态
        current_state = self._analyze_state(context)
        
        # 计算阴阳得分
        yin_score = current_state.get("yin", 0.5)
        yang_score = current_state.get("yang", 0.5)
        
        # judge需要偏向
        if abs(yin_score - yang_score) < 0.2:
            recommendation = "阴阳平衡,宜保持现状,稳健发展"
            adjustment = "维持"
        elif yin_score > yang_score:
            recommendation = "阴盛阳衰,宜适当增加阳刚之气"
            adjustment = "加阳"
        else:
            recommendation = "阳盛阴衰,宜适当增加阴柔之道"
            adjustment = "加阴"
        
        return {
            "yin_score": yin_score,
            "yang_score": yang_score,
            "balance_status": "平衡" if abs(yin_score - yang_score) < 0.2 else "失衡",
            "recommendation": recommendation,
            "adjustment": adjustment,
            "specific_advice": self._get_specific_advice(adjustment, context)
        }
    
    def _analyze_state(self, context: DecisionContext) -> Dict:
        """分析状态"""
        situation = context.situation
        
        yin = 0.5
        yang = 0.5
        
        if any(k in situation for k in ["守", "稳", "保守", "冬"]):
            yin += 0.2
        elif any(k in situation for k in ["攻", "进", "激进", "夏"]):
            yang += 0.2
        
        return {
            "yin": min(1.0, yin),
            "yang": min(1.0, yang)
        }
    
    def _get_specific_advice(self, adjustment: str, context: DecisionContext) -> str:
        """给出具体建议"""
        if adjustment == "加阳":
            return "宜主动出击,增加action力度,加快节奏"
        elif adjustment == "加阴":
            return "宜静观其变,减少action,积蓄力量"
        else:
            return "宜保持当前节奏,稳扎稳打"

class LvShiWisdomEngine:
    """吕氏春秋智慧引擎主类"""
    
    def __init__(self):
        self.core = LvShiWisdomCore()
        self.time_analyzer = TimeSituationAnalyzer()
        self.inclusive_engine = InclusiveWisdomEngine()
        self.public_engine = PublicFirstDecision()
        self.yin_yang_engine = YinYangBalanceDecision()
    
    def get_wisdom(self, principle_name: str) -> Optional[Dict]:
        """get智慧"""
        wisdom = self.core.get_wisdom(principle_name)
        if wisdom:
            return {
                "name": wisdom.name,
                "school": wisdom.school.value,
                "core_text": wisdom.core_text,
                "explanation": wisdom.explanation,
                "modern_interpretation": wisdom.modern_interpretation,
                "applications": wisdom.application_scenarios
            }
        return None
    
    def analyze_time_situation(self, context: DecisionContext) -> Dict:
        """分析时势"""
        return self.time_analyzer.analyze(context)
    
    def integrate_perspectives(self, 
                              perspectives: List[Tuple[str, WisdomSchool]], 
                              context: DecisionContext) -> Dict:
        """整合多方视角"""
        return self.inclusive_engine.integrate(perspectives, context)
    
    def public_first_decision(self, options: List[Dict]) -> Dict:
        """贵公去私decision"""
        return self.public_engine.evaluate(options)
    
    def yin_yang_balance(self, context: DecisionContext) -> Dict:
        """阴阳平衡"""
        return self.yin_yang_engine.balance(context)
    
    def get_month_guidance(self, month: Optional[Month] = None) -> Dict:
        """get月度指导"""
        if month is None:
            now = datetime.now()
            month_map = {
                1: Month.MENG_DONG, 2: Month.ZHONG_DONG, 3: Month.JI_DONG,
                4: Month.MENG_CHUN, 5: Month.ZHONG_CHUN, 6: Month.JI_CHUN,
                7: Month.MENG_XIA, 8: Month.ZHONG_XIA, 9: Month.JI_XIA,
                10: Month.MENG_QIU, 11: Month.ZHONG_QIU, 12: Month.JI_QIU
            }
            month = month_map.get(now.month, Month.MENG_CHUN)
        
        wisdom = self.core.get_month_wisdom(month)
        
        return {
            "month": month.value,
            "theme": wisdom.get("theme", ""),
            "advice": wisdom.get("advice", ""),
            "action": wisdom.get("action", ""),
            "related_principles": self._get_related_principles(month)
        }
    
    def _get_related_principles(self, month: Month) -> List[str]:
        """get相关原则"""
        if month in [Month.MENG_CHUN, Month.ZHONG_CHUN, Month.JI_CHUN]:
            return ["因时变法", "道法自然"]
        elif month in [Month.MENG_XIA, Month.ZHONG_XIA, Month.JI_XIA]:
            return ["积极进取", "顺势而为"]
        elif month in [Month.MENG_QIU, Month.ZHONG_QIU, Month.JI_QIU]:
            return ["中庸之道", "兼听则明"]
        else:
            return ["无为而治", "慎大览微"]
    
    def get_all_principles(self, school: Optional[WisdomSchool] = None) -> List[Dict]:
        """get所有原则"""
        if school:
            principles = self.core.get_school_wisdom(school)
        else:
            principles = list(self.core.principles.values())
        
        return [
            {
                "name": p.name,
                "school": p.school.value,
                "core_text": p.core_text,
                "explanation": p.explanation,
                "modern_interpretation": p.modern_interpretation,
                "applications": p.application_scenarios,
                "examples": p.examples
            }
            for p in principles
        ]

# 导出
__all__ = [
    'WisdomSchool',
    'Season',
    'Month',
    'WisdomPrinciple',
    'TimeContext',
    'DecisionContext',
    'LvShiWisdomCore',
    'TimeSituationAnalyzer',
    'InclusiveWisdomEngine',
    'PublicFirstDecision',
    'YinYangBalanceDecision',
    'LvShiWisdomEngine'
]

# 向后兼容别名
LvshiWisdomEngine = LvShiWisdomEngine
LvshiWisdomCore = LvShiWisdomCore
LvshiPrinciple = WisdomPrinciple
TwelveMonthsWisdom = Month  # 存根,wisdom_fusion_core.py 导入了但未使用
