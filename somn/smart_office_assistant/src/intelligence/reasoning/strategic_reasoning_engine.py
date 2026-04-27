# -*- coding: utf-8 -*-
"""
智慧推理引擎 v1.0.0
Wisdom Reasoning Engine

fusion儒家,道家,佛家,素书,兵法,吕氏春秋,科幻思维,成长思维
八种智慧体系的推理框架

版本: v1.0.0
日期: 2026-04-02
"""

from enum import Enum
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime
import random

class WisdomReasoningMode(Enum):
    """智慧推理模式"""
    # 传统智慧
    CONFUCIAN = "confucian"           # 儒家推理 - 修身齐家
    DAOIST = "daoist"                 # 道家推理 - 道法自然
    BUDDHIST = "buddhist"             # 佛家推理 - 缘起性空
    SUFU = "sufu"                     # 素书推理 - 五德decision
    MILITARY = "military"             # 兵法推理 - 知己知彼
    LVSHI = "lvshi"                   # 吕氏春秋推理 - 贵公去私
    
    # 现代思维
    SCI_FI = "scifi"                  # 科幻推理 - 维度超越
    GROWTH = "growth"                  # 成长推理 - 持续迭代
    
    # fusion模式
    FUSION = "fusion"                 # fusion推理

@dataclass
class ReasoningStep:
    """推理步骤"""
    step_number: int
    mode: WisdomReasoningMode
    premise: str                      # 前提
    inference: str                    # 推理
    conclusion: str                   # 结论
    wisdom_source: str                # 智慧来源
    classical_quote: str              # 经典语录
    confidence: float                 # 置信度
    warnings: List[str] = field(default_factory=list)

@dataclass
class WisdomReasoningResult:
    """推理结果"""
    timestamp: datetime
    problem: str
    primary_mode: WisdomReasoningMode
    reasoning_chain: List[ReasoningStep]
    final_conclusion: str
    alternative_perspectives: List[str]
    classical_wisdom: List[str]
    practical_guidance: List[str]
    confidence: float
    wisdom_alignment: Dict[str, float]

class WisdomReasoningEngine:
    """
    智慧推理引擎
    
    提供八种智慧推理模式:
    1. 儒家推理 - 修身齐家治国平天下
    2. 道家推理 - 道法自然无为而治
    3. 佛家推理 - 缘起性空戒定慧
    4. 素书推理 - 道德仁义礼五德
    5. 兵法推理 - 知己知彼奇正相生
    6. 吕氏春秋推理 - 贵公去私阴阳平衡
    7. 科幻推理 - 黑暗森林降维打击
    8. 成长推理 - 成长型思维闭环迭代
    """
    
    def __init__(self):
        self.classical_quotes = self._load_classical_quotes()
        self.reasoning_templates = self._load_reasoning_templates()
    
    def _load_classical_quotes(self) -> Dict[str, List[str]]:
        """加载经典语录"""
        return {
            WisdomReasoningMode.CONFUCIAN: [
                "大学之道,在明明德,在亲民,在止于至善",
                "修身齐家治国平天下",
                "己所不欲,勿施于人",
                "君子喻于义,小人喻于利",
                "学而时习之,不亦说乎",
                "三人行必有我师",
                "知之为知之,不知为不知",
                "君子求诸己,小人求诸人",
                "仁者爱人",
                "礼之用,和为贵"
            ],
            WisdomReasoningMode.DAOIST: [
                "道可道,非常道",
                "上善若水",
                "无为而无不为",
                "柔弱胜刚强",
                "知足者富",
                "为而不争",
                "致虚极,守静笃",
                "飘风不终朝,骤雨不终日",
                "物壮则老",
                "知人者智,自知者明"
            ],
            WisdomReasoningMode.BUDDHIST: [
                "缘起性空",
                "诸行无常",
                "诸法无我",
                "涅槃寂静",
                "戒定慧三学",
                "八正道",
                "六度万行",
                "色即是空,空即是色",
                "放下屠刀,立地成佛",
                "苦海无边,回头是岸"
            ],
            WisdomReasoningMode.SUFU: [
                "道者,人之所蹈",
                "德者,人之所失",
                "仁者,人之所亲",
                "义者,人之所宜",
                "礼者,人之所履",
                "俊者,人之所羡",
                "豪者,人之所畏",
                "贤者,人之所称",
                "吉莫吉于知足",
                "危于利也,害于义也"
            ],
            WisdomReasoningMode.MILITARY: [
                "知己知彼,百战不殆",
                "不战而屈人之兵",
                "上兵伐谋",
                "兵者,诡道也",
                "致人而不致于人",
                "善战者,致人而不致于人",
                "兵贵胜,不贵久",
                "先为不可胜",
                "乱生于治,怯生于勇",
                "奇正相生"
            ],
            WisdomReasoningMode.LVSHI: [
                "贵公去私",
                "公则天下平",
                "阴阳调和",
                "因时制宜",
                "天下为公",
                "春生夏长秋收冬藏",
                "物极必反",
                "顺势而为",
                "审时度势",
                "和而不同"
            ],
            WisdomReasoningMode.SCI_FI: [
                "黑暗森林法则",
                "降维打击",
                "文明的第一需求是生存",
                "弱小和无知不是生存的障碍",
                "傲慢才是",
                "给岁月以文明",
                "失去人性,失去很多",
                "失去兽性,失去一切",
                "宇宙很大,生活更大",
                "沉默是金"
            ],
            WisdomReasoningMode.GROWTH: [
                "能力可以培养",
                "失败是成长的机会",
                "挑战是学习的契机",
                "努力是通往成功的道路",
                "批评是改进的信息",
                "他人的成功是灵感",
                "大脑可塑性",
                "从错误中学习",
                "坚持不懈",
                "拥抱未知"
            ]
        }
    
    def _load_reasoning_templates(self) -> Dict[WisdomReasoningMode, Dict]:
        """加载推理模板"""
        return {
            WisdomReasoningMode.CONFUCIAN: {
                "step1": "[修身]分析问题本质,反求诸己",
                "step2": "[齐家]考虑相关利益方",
                "step3": "[明德]明确核心价值观",
                "step4": "[亲民]考虑对他人影响",
                "step5": "[至善]追求最佳解决方案"
            },
            WisdomReasoningMode.DAOIST: {
                "step1": "[观道]洞察事物发展规律",
                "step2": "[自然]顺应自然之势",
                "step3": "[无为]有所为有所不为",
                "step4": "[柔弱]以柔克刚",
                "step5": "[复归]回归本质"
            },
            WisdomReasoningMode.BUDDHIST: {
                "step1": "[观苦]认识问题之苦",
                "step2": "[寻因]追溯问题根源",
                "step3": "[悟空]看透本质空性",
                "step4": "[修定]保持内心平静",
                "step5": "[生慧]获得智慧解脱"
            },
            WisdomReasoningMode.SUFU: {
                "step1": "[明道]明确方向规律",
                "step2": "[积德]积累品德资本",
                "step3": "[守仁]保持仁爱之心",
                "step4": "[循义]做适宜之事",
                "step5": "[循礼]遵守规范程序"
            },
            WisdomReasoningMode.MILITARY: {
                "step1": "[知彼]分析对手和环境",
                "step2": "[知己]评估自身实力",
                "step3": "[伐谋]制定战略计划",
                "step4": "[奇正]配置正奇兵力",
                "step5": "[速胜]追求高效胜利"
            },
            WisdomReasoningMode.LVSHI: {
                "step1": "[贵公]坚持公正原则",
                "step2": "[去私]去除私心杂念",
                "step3": "[审时]把握时机节点",
                "step4": "[度势]评估形势走向",
                "step5": "[阴阳]平衡刚柔两面"
            },
            WisdomReasoningMode.SCI_FI: {
                "step1": "[降维]简化问题维度",
                "step2": "[森林]保持警惕生存",
                "step3": "[尺度]放大思考格局",
                "step4": "[沉默]保持低调隐藏",
                "step5": "[威慑]维持战略平衡"
            },
            WisdomReasoningMode.GROWTH: {
                "step1": "[接纳]接受当前状态",
                "step2": "[学习]从中get经验",
                "step3": "[迭代]持续改进优化",
                "step4": "[坚持]保持长期投入",
                "step5": "[超越]突破能力边界"
            }
        }
    
    def reason(
        self,
        problem: str,
        mode: Optional[WisdomReasoningMode] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> WisdomReasoningResult:
        """
        执行智慧推理
        
        Args:
            problem: 待解决的问题
            mode: 推理模式(默认为fusion模式)
            context: 上下文信息
            
        Returns:
            WisdomReasoningResult: 推理结果
        """
        if mode is None:
            mode = WisdomReasoningMode.FUSION
        
        if mode == WisdomReasoningMode.FUSION:
            return self._fusion_reasoning(problem, context)
        else:
            return self._single_mode_reasoning(problem, mode, context)
    
    def _single_mode_reasoning(
        self,
        problem: str,
        mode: WisdomReasoningMode,
        context: Optional[Dict[str, Any]]
    ) -> WisdomReasoningResult:
        """单模式推理"""
        template = self.reasoning_templates.get(mode, {})
        quotes = self.classical_quotes.get(mode, [])
        
        chain = []
        conclusions = []
        
        for i, (step_key, step_desc) in enumerate(template.items(), 1):
            # generate推理步骤
            step = ReasoningStep(
                step_number=i,
                mode=mode,
                premise=f"基于{step_desc.split('[')[1].split(']')[0]}原则",
                inference=f"运用{mode.value}智慧进行分析",
                conclusion=f"{step_desc.split('[')[1].split(']')[1]}",
                wisdom_source=self._get_source_name(mode),
                classical_quote=quotes[i-1] if i <= len(quotes) else "",
                confidence=0.7 + i * 0.05,
                warnings=self._get_warnings(mode)
            )
            chain.append(step)
            conclusions.append(step.conclusion)
        
        return WisdomReasoningResult(
            timestamp=datetime.now(),
            problem=problem,
            primary_mode=mode,
            reasoning_chain=chain,
            final_conclusion=conclusions[-1] if conclusions else "synthesize分析",
            alternative_perspectives=self._get_alternatives(mode),
            classical_wisdom=quotes[:5],
            practical_guidance=self._generate_guidance(mode, problem),
            confidence=0.85,
            wisdom_alignment={mode.value: 0.95}
        )
    
    def _fusion_reasoning(
        self,
        problem: str,
        context: Optional[Dict[str, Any]]
    ) -> WisdomReasoningResult:
        """fusion模式推理"""
        # 选择最适合的模式组合
        modes = self._select_modes(problem)
        
        chains = []
        all_conclusions = []
        all_wisdom = []
        
        for mode in modes:
            result = self._single_mode_reasoning(problem, mode, context)
            chains.extend(result.reasoning_chain)
            all_conclusions.append(result.final_conclusion)
            all_wisdom.extend(result.classical_wisdom)
        
        # 按步骤排序
        chains.sort(key=lambda x: x.step_number)
        
        # synthesize结论
        fusion_conclusion = self._synthesize_conclusions(all_conclusions)
        
        # 计算智慧对齐度
        alignment = {m.value: 0.8 + i * 0.05 for i, m in enumerate(modes)}
        
        return WisdomReasoningResult(
            timestamp=datetime.now(),
            problem=problem,
            primary_mode=WisdomReasoningMode.FUSION,
            reasoning_chain=chains,
            final_conclusion=fusion_conclusion,
            alternative_perspectives=all_conclusions,
            classical_wisdom=all_wisdom[:10],
            practical_guidance=self._generate_fusion_guidance(modes, problem),
            confidence=0.90,
            wisdom_alignment=alignment
        )
    
    def _select_modes(self, problem: str) -> List[WisdomReasoningMode]:
        """选择推理模式"""
        problem_lower = problem.lower()
        modes = []
        
        # 根据问题关键词选择模式
        if any(k in problem_lower for k in ["道德", "伦理", "仁义", "修身"]):
            modes.append(WisdomReasoningMode.CONFUCIAN)
        if any(k in problem_lower for k in ["战略", "转型", "自然", "无为"]):
            modes.append(WisdomReasoningMode.DAOIST)
        if any(k in problem_lower for k in ["心态", "情绪", "解脱", "放下"]):
            modes.append(WisdomReasoningMode.BUDDHIST)
        if any(k in problem_lower for k in ["领导", "decision", "风险", "人才"]):
            modes.append(WisdomReasoningMode.SUFU)
        if any(k in problem_lower for k in ["竞争", "攻防", "谈判", "博弈"]):
            modes.append(WisdomReasoningMode.MILITARY)
        if any(k in problem_lower for k in ["公正", "公私", "时令", "平衡"]):
            modes.append(WisdomReasoningMode.LVSHI)
        if any(k in problem_lower for k in ["维度", "降维", "宇宙", "文明"]):
            modes.append(WisdomReasoningMode.SCI_FI)
        if any(k in problem_lower for k in ["成长", "突破", "迭代", "挑战"]):
            modes.append(WisdomReasoningMode.GROWTH)
        
        # 默认至少两个模式
        if len(modes) < 2:
            modes = [WisdomReasoningMode.CONFUCIAN, WisdomReasoningMode.SUFU]
        
        return modes[:4]  # 最多4个模式
    
    def _get_source_name(self, mode: WisdomReasoningMode) -> str:
        """get智慧来源"""
        sources = {
            WisdomReasoningMode.CONFUCIAN: "儒家经典<论语><孟子><大学>",
            WisdomReasoningMode.DAOIST: "道家经典<道德经><庄子>",
            WisdomReasoningMode.BUDDHIST: "佛家经典<金刚经><心经>",
            WisdomReasoningMode.SUFU: "素书<原始章><正道章>",
            WisdomReasoningMode.MILITARY: "兵法<孙子兵法><三十六计>",
            WisdomReasoningMode.LVSHI: "<吕氏春秋>",
            WisdomReasoningMode.SCI_FI: "刘慈欣<三体>",
            WisdomReasoningMode.GROWTH: "卡罗尔·德韦克<终身成长>"
        }
        return sources.get(mode, "synthesize智慧")
    
    def _get_warnings(self, mode: WisdomReasoningMode) -> List[str]:
        """get警示"""
        warnings = {
            WisdomReasoningMode.CONFUCIAN: ["勿过于迂腐", "权变与原则并重"],
            WisdomReasoningMode.DAOIST: ["勿消极逃避", "无为非不为"],
            WisdomReasoningMode.BUDDHIST: ["勿陷入虚无", "空非无"],
            WisdomReasoningMode.SUFU: ["勿过于理想", "因时制宜"],
            WisdomReasoningMode.MILITARY: ["慎用对抗", "不战而屈人"],
            WisdomReasoningMode.LVSHI: ["公正非冷漠", "刚柔并济"],
            WisdomReasoningMode.SCI_FI: ["保持人性", "威慑有度"],
            WisdomReasoningMode.GROWTH: ["接受局限", "过程重于结果"]
        }
        return warnings.get(mode, [])
    
    def _get_alternatives(self, mode: WisdomReasoningMode) -> List[str]:
        """get替代视角"""
        alternatives = {
            WisdomReasoningMode.CONFUCIAN: [
                "从道家视角:顺应自然",
                "从兵法视角:审时度势"
            ],
            WisdomReasoningMode.DAOIST: [
                "从儒家视角:积极入世",
                "从佛家视角:看空一切"
            ],
            WisdomReasoningMode.MILITARY: [
                "从成长视角:以和为贵",
                "从佛家视角:放下执念"
            ],
            WisdomReasoningMode.GROWTH: [
                "从道家视角:顺其自然",
                "从佛家视角:接受现实"
            ]
        }
        return alternatives.get(mode, [])
    
    def _synthesize_conclusions(self, conclusions: List[str]) -> str:
        """synthesize结论"""
        if len(conclusions) == 1:
            return conclusions[0]
        
        return f"synthesize分析表明:{';'.join(conclusions[:3])}"
    
    def _generate_guidance(self, mode: WisdomReasoningMode, problem: str) -> List[str]:
        """generate指导"""
        guidance_map = {
            WisdomReasoningMode.CONFUCIAN: [
                "以仁爱之心对待他人",
                "坚守道义底线",
                "注重修身养德"
            ],
            WisdomReasoningMode.DAOIST: [
                "顺应事物发展规律",
                "保持内心平静",
                "有所为有所不为"
            ],
            WisdomReasoningMode.MILITARY: [
                "知己知彼,全面分析",
                "制定多个预案",
                "把握时机,快速action"
            ],
            WisdomReasoningMode.GROWTH: [
                "将挑战视为成长机会",
                "从失败中学习",
                "保持开放心态"
            ]
        }
        return guidance_map.get(mode, ["synthesize考虑,审慎decision"])
    
    def _generate_fusion_guidance(
        self, modes: List[WisdomReasoningMode], problem: str
    ) -> List[str]:
        """generatefusion指导"""
        guidance = []
        
        for mode in modes[:2]:
            specific = self._generate_guidance(mode, problem)
            guidance.extend(specific)
        
        return list(set(guidance))[:5]
    
    def get_system_status(self) -> Dict[str, Any]:
        """get系统状态"""
        return {
            "available_modes": [m.value for m in WisdomReasoningMode],
            "mode_count": len(WisdomReasoningMode),
            "classical_sources": {
                "confucian": "论语,孟子,大学",
                "daoist": "道德经,庄子",
                "buddhist": "金刚经,心经",
                "sufu": "素书",
                "military": "孙子兵法",
                "lvshi": "吕氏春秋",
                "scifi": "三体",
                "growth": "终身成长"
            },
            "version": "v1.0.0"
        }

def quick_reason(problem: str) -> str:
    """
    快速推理接口
    
    用法:
    >>> quick_reason("如何提升团队凝聚力")
    """
    engine = WisdomReasoningEngine()
    result = engine.reason(problem)
    
    output = f"""
{'='*60}
🧠 智慧推理分析
{'='*60}

📋 问题: {result.problem}
🎯 主模式: {result.primary_mode.value}

{'-'*60}
📝 推理过程:
"""
    
    for step in result.reasoning_chain[:5]:
        output += f"""
第{step.step_number}步 [{step.wisdom_source.split('<')[0]}]
  前提: {step.premise}
  推理: {step.inference}
  结论: {step.conclusion}
  经典: {step.classical_quote}
"""
    
    output += f"""
{'-'*60}
🎯 最终结论: {result.final_conclusion}

{'-'*60}
💡 实践指导:
{chr(10).join(f"  {i+1}. {g}" for i, g in enumerate(result.practical_guidance))}

{'-'*60}
📚 相关经典:
{chr(10).join(f"  • {q}" for q in result.classical_wisdom[:5])}

{'-'*60}
⚠️ 注意事项:
  • 勿偏执一端
  • 因时制宜
  • 权变与原则并重

{'='*60}
"""
    
    return output

# 向后兼容别名 (v1.1 2026-04-06)
# StrategicReasoningEngine 是 WisdomReasoningEngine 的别名
StrategicReasoningEngine = WisdomReasoningEngine

# 导出
__all__ = [
    'WisdomReasoningEngine',
    'StrategicReasoningEngine',  # 向后兼容别名
    'WisdomReasoningMode',
    'ReasoningStep',
    'WisdomReasoningResult',
    'quick_reason'
]
