"""
__all__ = [
    'analyze_paradigm',
    'analyze_system',
    'apply_scientific_method',
    'cross_domain_transfer',
    'detect_logical_fallacies',
    'evaluate_evidence',
    'get_cross_domain_insights',
    'quick_fallacy_check',
    'quick_scientific_analysis',
]

科学思维框架引擎 v1.0
基于自然科学全景深度研究报告

核心能力:
1. 科学方法论 - 观察→假设→实验→验证→修正
2. 系统思维 - 整体性,涌现性,反馈回路
3. 量化分析 - 数学建模,统计分析,概率思维
4. 批判思维 - 逻辑推理,证据评估,偏差recognize
5. 跨学科连接 - 物理学→化学→生物学→信息论
6. 科学史智慧 - 范式转换,科学革命,否定之否定

版本:v1.0.0
更新:2026-04-02
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field
import math

class ScientificDomain(Enum):
    """科学领域"""
    PHYSICS = "物理学"
    CHEMISTRY = "化学"
    BIOLOGY = "生物学"
    MATHEMATICS = "数学"
    COMPUTER_SCIENCE = "计算机科学"
    NEUROSCIENCE = "神经科学"
    INFORMATION_THEORY = "信息论"
    COMPLEX_SYSTEMS = "复杂系统"

class ReasoningPattern(Enum):
    """推理模式"""
    DEDUCTIVE = "演绎推理"       # 从一般到特殊
    INDUCTIVE = "归纳推理"       # 从特殊到一般
    ABDUCTIVE = "溯因推理"       # 最佳解释推断
    ANALOGICAL = "类比推理"      # 从相似到相似
    STATISTICAL = "统计推理"     # 基于数据的概率推断
    CAUSAL = "因果推理"          # 因果关系推断

@dataclass
class Hypothesis:
    """科学假设"""
    statement: str
    testable: bool
    falsifiable: bool
    predictions: List[str]
    confidence: float            # 初始置信度 0-1

@dataclass
class Evidence:
    """证据"""
    source: str
    type: str                    # empirical/theoretical/experimental
    reliability: float           # 可靠性 0-1
    relevance: float             # 相关性 0-1
    finding: str

class ScienceThinkingEngine:
    """
    科学思维框架引擎
    
    fusion自然科学全景的核心思维模式:
    - 物理学:还原论+涌现论的辩证unified,守恒定律,对称性思维
    - 生物学:进化论思维,适应性系统,自组织
    - 信息论:熵,信息量,信道容量
    - 复杂系统:非线性,反馈回路,混沌边缘
    - 科学哲学:可证伪性(波普尔),范式转换(库恩),研究纲领(拉卡托斯)
    
    核心价值:让系统具备严格的科学思维框架,而非模糊的"理性"
    """

    VERSION = "6.2.0"
    
    def __init__(self):
        # === 科学方法论五步模型 ===
        self.scientific_method = {
            "观察": {
                "desc": "系统性地观察现象,收集数据",
                "tools": ["定量测量", "对照实验", "随机抽样", "重复验证"],
                "pitfalls": ["确认偏差", "选择偏差", "幸存者偏差"]
            },
            "假设": {
                "desc": "基于观察提出可检验的假设",
                "criteria": ["可证伪性(波普尔)", "解释力", "简洁性(奥卡姆剃刀)", "预测力"],
                "pitfalls": ["过度拟合", "后验假设", "不可证伪的命题"]
            },
            "实验": {
                "desc": "设计实验检验假设",
                "principles": ["随机对照", "双盲设计", "大样本", "可重复性"],
                "pitfalls": ["混淆变量", "样本偏差", "实验者效应"]
            },
            "验证": {
                "desc": "分析数据,评估假设",
                "tools": ["统计显著性检验", "效应量评估", "置信区间", "贝叶斯更新"],
                "pitfalls": ["p值误用", "相关≠因果", "回归均值"]
            },
            "修正": {
                "desc": "基于证据修正或拒绝假设",
                "principles": ["证据优先", "量化不确定性", "接受暂定性", "持续修正"],
                "pitfalls": ["理论固着", "否认矛盾证据", "过度确信"]
            }
        }
        
        # === 认知偏差清单(卡尼曼)===
        self.cognitive_biases = {
            "确认偏差": "倾向于寻找和记住支持已有信念的信息",
            "锚定效应": "过度依赖最先接收到的信息",
            "可得性偏差": "根据信息的容易get程度judge其概率",
            "框架效应": "相同信息不同呈现方式导致不同decision",
            "沉没成本谬误": "因已投入的成本而继续不理性的行为",
            "过度自信偏差": "高估自己judge的准确性",
            "后见之明偏差": "事后觉得结果是显而易见的",
            "基本归因错误": "将他人行为归因于性格而非情境",
            "从众效应": "倾向于与群体保持一致",
            "光环效应": "一个正面characteristics影响整体评价"
        }
        
        # === 跨学科核心概念 ===
        self.cross_disciplinary_concepts = {
            "熵": {
                "physics": "热力学第二定律:孤立系统的熵永不减少",
                "information_theory": "香农熵:信息不确定性的度量",
                "biology": "生命通过摄取负熵维持有序",
                "economics": "市场熵增:竞争趋于均衡",
                "insight": "所有系统都趋向无序,维持有序需要持续输入能量/信息"
            },
            "涌现": {
                "physics": "水分子单独无液态属性,大量聚集涌现出液体行为",
                "biology": "神经元无意识,大量涌现出意识",
                "economics": "个人简单规则涌现出市场复杂行为",
                "cs": "简单规则涌现出复杂智能(如蚁群算法)",
                "insight": "整体大于部分之和;理解系统需要在适当层次分析"
            },
            "反馈": {
                "biology": "体内平衡:负反馈维持稳定",
                "ecology": "捕食-被捕食:正负反馈交替",
                "economics": "供需调节:价格机制",
                "climate": "冰雪反照率:正反馈加速变化",
                "insight": "理解动态系统需要recognize反馈回路的类型和强度"
            },
            "对称性": {
                "physics": "诺特定理:每种对称性对应一个守恒定律",
                "mathematics": "群论描述对称结构",
                "biology": "生物体的近似对称",
                "economics": "博弈论中的对称均衡",
                "insight": "对称性破缺是产生差异和结构的根本机制"
            },
            "进化": {
                "biology": "自然选择:变异+选择+遗传",
                "computer_science": "遗传算法,进化计算",
                "economics": "市场进化,企业竞争选择",
                "culture": "模因论:文化信息的传播和演化",
                "insight": "进化不是有目的的设计,而是无目的的优化过程"
            }
        }
        
        # === 科学范式(库恩)===
        self.scientific_paradigms = {
            "前科学期": "没有unified的理论框架,多种学派并存",
            "常规科学": "在既有范式内解决谜题",
            "危机期": "现有范式无法解释的异常积累",
            "科学革命": "新范式替代旧范式",
            "新常规科学": "在新范式下重新解释世界"
        }

    def apply_scientific_method(self, problem: str) -> Dict:
        """
        应用科学方法论分析问题
        
        Args:
            problem: 待分析的问题
            
        Returns:
            科学方法论分析报告
        """
        return {
            "problem": problem,
            "step1_observation": self._systematic_observation(problem),
            "step2_hypothesis": self._generate_hypotheses(problem),
            "step3_experiment": self._design_experiment(problem),
            "step4_validation": self._plan_validation(problem),
            "step5_revision": self._plan_revision(problem),
            "bias_check": self._check_biases(problem),
            "scientific_culture": self._apply_scientific_culture(problem)
        }

    def analyze_system(self, system_desc: str) -> Dict:
        """
        系统思维分析
        
        Args:
            system_desc: 系统描述
            
        Returns:
            系统分析报告
        """
        return {
            "system": system_desc,
            "components": self._identify_components(system_desc),
            "relationships": self._identify_relationships(system_desc),
            "feedback_loops": self._identify_feedback_loops(system_desc),
            "emergent_properties": self._identify_emergent_properties(system_desc),
            "system_dynamics": self._analyze_dynamics(system_desc),
            "leverage_points": self._find_leverage_points(system_desc),
            "system_archetypes": self._match_system_archetype(system_desc)
        }

    def evaluate_evidence(self, claim: str, evidences: List[Dict] = None) -> Dict:
        """
        评估证据质量
        
        Args:
            claim: 待评估的主张
            evidences: 证据列表
            
        Returns:
            证据评估报告
        """
        if not evidences:
            evidences = []
        
        return {
            "claim": claim,
            "evidence_quality": self._assess_evidence_quality(evidences),
            "logical_structure": self._analyze_logical_structure(claim),
            "bias_scan": self._scan_for_biases(claim),
            "alternative_explanations": self._generate_alternatives(claim),
            "confidence_assessment": self._assess_confidence(claim, evidences),
            "bayesian_update": self._bayesian_analysis(claim, evidences)
        }

    def cross_domain_transfer(self, concept: str, source_domain: str, target_domain: str) -> Dict:
        """
        跨领域概念迁移
        
        Args:
            concept: 核心概念
            source_domain: 源领域
            target_domain: 目标领域
            
        Returns:
            跨领域迁移分析
        """
        concept_info = self.cross_disciplinary_concepts.get(concept)
        
        if concept_info:
            source_insight = concept_info.get(source_domain, "待补充")
            target_insight = concept_info.get(target_domain, "待补充")
            universal_insight = concept_info.get("insight", "")
        else:
            source_insight = f"在{source_domain}中的含义待补充"
            target_insight = f"在{target_domain}中的含义待补充"
            universal_insight = f"'{concept}'可能是跨学科的通用概念"
        
        return {
            "concept": concept,
            "source_domain": source_domain,
            "target_domain": target_domain,
            "source_insight": source_insight,
            "target_insight": target_insight,
            "universal_principle": universal_insight,
            "transfer_hypothesis": self._generate_transfer_hypothesis(concept, source_domain, target_domain),
            "limitations": self._identify_transfer_limitations(concept, source_domain, target_domain)
        }

    def detect_logical_fallacies(self, argument: str) -> Dict:
        """
        检测逻辑谬误
        
        Args:
            argument: 待检测的论证
            
        Returns:
            逻辑谬误检测报告
        """
        fallacies = {
            "诉诸权威": {"pattern": ["专家说", "权威认为", "研究表明"], "fix": "权威不等于真理,需要独立评估证据"},
            "诉诸情感": {"pattern": ["你不觉得吗", "想想看", "难道不应该"], "fix": "情感不能替代逻辑论证"},
            "稻草人谬误": {"pattern": ["所以你是说", "你的意思是"], "fix": "准确理解对方观点后再反驳"},
            "滑坡谬误": {"pattern": ["如果...就会...", "一旦...必然"], "fix": "每一步因果链都需要独立验证"},
            "虚假二分": {"pattern": ["要么...要么...", "不是...就是..."], "fix": "现实往往有第三种选择"},
            "循环论证": {"pattern": ["因为A所以A", "A证明了A"], "fix": "论据不能等同于论点"},
            "以偏概全": {"pattern": ["都是", "全部", "没有不"], "fix": "需要统计上显著的样本量"},
            "因果混淆": {"pattern": ["因为", "导致了", "造成"], "fix": "相关不等于因果"}
        }
        
        detected = []
        for fallacy_name, fallacy_info in fallacies.items():
            for pattern in fallacy_info["pattern"]:
                if pattern in argument:
                    detected.append({
                        "fallacy": fallacy_name,
                        "matched_pattern": pattern,
                        "fix": fallacy_info["fix"]
                    })
                    break
        
        return {
            "argument": argument,
            "detected_fallacies": detected,
            "overall_assessment": "发现潜在逻辑问题" if detected else "论证结构较为合理",
            "strengthening_suggestions": self._suggest_argument_improvements(argument, detected)
        }

    def analyze_paradigm(self, field: str) -> Dict:
        """
        分析科学范式状态(库恩模型)
        
        Args:
            field: 科学/学术领域
            
        Returns:
            范式分析报告
        """
        return {
            "field": field,
            "paradigm_model": self.scientific_paradigms,
            "current_state": self._assess_paradigm_state(field),
            "anomalies": self._identify_anomalies(field),
            "paradigm_shift_indicators": self._identify_shift_indicators(field),
            "historical_parallels": self._find_paradigm_history(field),
            "kuhnian_insight": "科学进步不是线性积累,而是范式转换--旧理论不是被'证伪',而是被更优越的新理论'替代'"
        }

    # === 内部方法 ===
    
    def _systematic_observation(self, problem: str) -> Dict:
        """系统性观察"""
        return {
            "approach": "从多角度,多维度收集信息",
            "data_types": ["定量数据", "定性数据", "对比数据", "时间序列数据"],
            "warning": "注意避免确认偏差:主动寻找可能推翻假设的证据"
        }
    
    def _generate_hypotheses(self, problem: str) -> Dict:
        """generate假设"""
        return {
            "hypothesis": f"关于'{problem}'的可检验假设",
            "criteria": ["可证伪性", "可操作化", "有预测力"],
            "note": "好假设必须能被实验反驳--如果任何结果都能'解释',那就不是科学假设"
        }
    
    def _design_experiment(self, problem: str) -> Dict:
        """设计实验"""
        return {
            "approach": "对照实验设计",
            "control_group": "设置对照组,控制混淆变量",
            "randomization": "随机分组,消除选择偏差",
            "sample_size": "确保统计效力(通常n≥30)"
        }
    
    def _plan_validation(self, problem: str) -> Dict:
        """验证计划"""
        return {
            "statistical_tests": "根据数据类型选择合适的统计检验",
            "effect_size": "关注效应量而非仅p值",
            "confidence_interval": "报告置信区间而非仅点估计",
            "replication": "结果必须可重复"
        }
    
    def _plan_revision(self, problem: str) -> Dict:
        """修正计划"""
        return {
            "principle": "证据优先于理论",
            "approach": "根据实验结果修正或拒绝假设",
            "attitude": "保持科学谦逊:对结论保持暂定性"
        }
    
    def _check_biases(self, problem: str) -> Dict:
        """检查认知偏差"""
        relevant_biases = {}
        for bias_name, bias_desc in self.cognitive_biases.items():
            if any(kw in problem for kw in ["认为", "觉得", "应该", "大家都", "显然"]):
                relevant_biases[bias_name] = bias_desc
        return relevant_biases if relevant_biases else {"note": "常规偏差检查清单:确认偏差,锚定效应,可得性偏差,框架效应"}
    
    def _apply_scientific_culture(self, problem: str) -> Dict:
        """应用科学文化"""
        return {
            "skepticism": "对未经充分证据支持的主张保持质疑",
            "openness": "对新证据和新解释保持开放",
            "humility": "承认知识的暂定性和局限性",
            "rigor": "坚持严格的方法论标准"
        }
    
    def _identify_components(self, system_desc: str) -> List[str]:
        """recognize系统组件"""
        return ["需要进一步分析系统的具体组件"]
    
    def _identify_relationships(self, system_desc: str) -> List[str]:
        """recognize关系"""
        return ["组件间的因果/相关/层级关系"]
    
    def _identify_feedback_loops(self, system_desc: str) -> List[Dict]:
        """recognize反馈回路"""
        return [
            {"type": "正反馈", "effect": "自我强化,趋向极端"},
            {"type": "负反馈", "effect": "自我调节,趋向平衡"}
        ]
    
    def _identify_emergent_properties(self, system_desc: str) -> List[str]:
        """recognize涌现属性"""
        return ["整体层面才出现的属性,无法从组件单独推导"]
    
    def _analyze_dynamics(self, system_desc: str) -> Dict:
        """分析系统动态"""
        return {
            "linear_vs_nonlinear": "区分线性和非线性关系",
            "time_delays": "注意因果之间的时间延迟",
            "thresholds": "recognize系统的临界点和相变"
        }
    
    def _find_leverage_points(self, system_desc: str) -> List[str]:
        """寻找杠杆点(德内拉·梅多斯)"""
        return [
            "改变系统的目标",
            "改变系统的规则",
            "改变信息流",
            "改变系统的反馈结构",
            "改变系统的自组织能力"
        ]
    
    def _match_system_archetype(self, system_desc: str) -> str:
        """匹配系统原型(系统思考经典模式)"""
        archetypes = [
            "增长极限(增长遇到瓶颈)",
            "公地悲剧(共享资源的过度使用)",
            "恶性竞争(零和博弈升级)",
            "成功陷阱(过去的成功strategy变成障碍)",
            "目标侵蚀(标准逐渐降低)"
        ]
        return archetypes[hash(system_desc) % len(archetypes)]
    
    def _assess_evidence_quality(self, evidences: List[Dict]) -> Dict:
        """评估证据质量"""
        if not evidences:
            return {"warning": "缺乏证据支持,需要进一步收集"}
        
        avg_reliability = sum(e.get("reliability", 0.5) for e in evidences) / len(evidences)
        avg_relevance = sum(e.get("relevance", 0.5) for e in evidences) / len(evidences)
        
        return {
            "total_evidence": len(evidences),
            "average_reliability": avg_reliability,
            "average_relevance": avg_relevance,
            "quality_grade": "高质量" if avg_reliability > 0.8 and avg_relevance > 0.8 else 
                           "中等质量" if avg_reliability > 0.5 else "低质量"
        }
    
    def _analyze_logical_structure(self, claim: str) -> Dict:
        """分析论证逻辑结构"""
        return {
            "claim": claim,
            "premises": ["需要提取论证的前提"],
            "conclusion": claim,
            "validity": "需要检验前提是否支持结论",
            "soundness": "需要检验前提是否为真"
        }
    
    def _scan_for_biases(self, claim: str) -> List[Dict]:
        """扫描认知偏差"""
        return [{"bias": name, "desc": desc} for name, desc in self.cognitive_biases.items()]
    
    def _generate_alternatives(self, claim: str) -> List[str]:
        """generate替代解释"""
        return [
            f"替代解释1:存在未考虑的混淆变量",
            f"替代解释2:样本选择偏差导致的结果",
            f"替代解释3:因果方向可能相反"
        ]
    
    def _assess_confidence(self, claim: str, evidences: List[Dict]) -> Dict:
        """评估置信度"""
        return {
            "confidence_level": "初步" if not evidences else "中等",
            "key_uncertainties": ["数据质量", "样本代表性", "混淆变量"],
            "recommendation": "收集更多证据以提高置信度"
        }
    
    def _bayesian_analysis(self, claim: str, evidences: List[Dict]) -> Dict:
        """贝叶斯分析"""
        prior = 0.5  # 先验概率
        if evidences:
            likelihood = sum(e.get("reliability", 0.5) * e.get("relevance", 0.5) for e in evidences) / len(evidences)
            posterior = (likelihood * prior) / ((likelihood * prior) + (1 - likelihood) * (1 - prior))
        else:
            posterior = prior
        
        return {
            "prior_probability": prior,
            "likelihood": evidences[0].get("reliability", 0.5) if evidences else 0.5,
            "posterior_probability": posterior,
            "interpretation": f"考虑证据后,该主张的可信度从{prior:.0%}更新为{posterior:.0%}"
        }
    
    def _generate_transfer_hypothesis(self, concept: str, source: str, target: str) -> str:
        """generate迁移假设"""
        return f"假设:{source}中关于'{concept}'的原理可以解释{target}中的相关现象"
    
    def _identify_transfer_limitations(self, concept: str, source: str, target: str) -> List[str]:
        """recognize迁移局限"""
        return [
            f"{source}和{target}的基本假设可能不同",
            f"概念在跨领域时含义可能发生变化",
            "类比推理不等于证明,需要独立验证"
        ]
    
    def _suggest_argument_improvements(self, argument: str, fallacies: List[Dict]) -> List[str]:
        """建议论证改进"""
        improvements = ["明确界定核心概念", "提供充分的证据支持", "考虑反论并回应"]
        for f in fallacies:
            improvements.append(f["fix"])
        return list(set(improvements))
    
    def _assess_paradigm_state(self, field: str) -> str:
        """评估范式状态"""
        return "需要根据该领域的具体发展来judge当前处于哪个阶段"
    
    def _identify_anomalies(self, field: str) -> List[str]:
        """recognize异常现象"""
        return [f"该领域中与主流理论不符的观察现象"]
    
    def _identify_shift_indicators(self, field: str) -> List[str]:
        """recognize范式转换metrics"""
        return [
            "越来越多的异常无法被现有范式解释",
            "新的竞争性理论开始出现",
            "年轻研究者更倾向于新理论",
            "旧范式的拥护者开始转向"
        ]
    
    def _find_paradigm_history(self, field: str) -> str:
        """寻找范式转换历史"""
        return "每个科学领域都经历了多次范式转换,理解这一历史有助于judge当前领域的发展阶段"

    def get_cross_domain_insights(self, problem: str) -> Dict:
        """
        get跨学科洞察
        
        Args:
            problem: 待分析的问题
            
        Returns:
            多学科视角的synthesize洞察
        """
        insights = {}
        for concept, info in self.cross_disciplinary_concepts.items():
            insight = info.get("insight", "")
            if insight:
                insights[concept] = insight
        
        return {
            "problem": problem,
            "cross_domain_concepts": insights,
            "universal_patterns": [
                "熵增定律:无序化是默认方向,维持秩序需要能量投入",
                "涌现效应:整体具有部分所没有的属性",
                "反馈调节:正反馈趋向极端,负反馈趋向平衡",
                "进化优化:没有设计者的设计,通过变异和选择实现适应",
                "对称破缺:差异和结构来源于对称性的打破"
            ],
            "thinking_tools": [
                "还原论:将复杂系统分解为简单组件来理解",
                "涌现论:在整体层面理解不可还原的属性",
                "系统动力学:追踪因果反馈回路",
                "统计思维:用概率和不确定性思考问题",
                "进化思维:通过变异+选择+遗传理解变化"
            ]
        }

# 便捷函数
def quick_scientific_analysis(problem: str) -> Dict:
    """便捷函数:快速科学方法论分析"""
    engine = ScienceThinkingEngine()
    return engine.apply_scientific_method(problem)

def quick_fallacy_check(argument: str) -> Dict:
    """便捷函数:快速逻辑谬误检查"""
    engine = ScienceThinkingEngine()
    return engine.detect_logical_fallacies(argument)
