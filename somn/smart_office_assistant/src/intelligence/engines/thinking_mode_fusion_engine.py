# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze_problem',
    'compare_modes',
    'create_fusion_engine',
    'fuse_decision',
    'get_thinking_toolkit',
    'think_in_mode',
]

思维模式fusion引擎 v1.0.0
Thinking Mode Fusion Engine

基于<底层逻辑><格局><闭环思维><逆转思维><逆思维心理学>等核心思想构建

核心思想:
- 不同问题需要不同的思维模式
- 掌握多种思维才能灵活应对
- fusion创新往往来自跨界思维
- 思维决定action,action塑造思维

作者:Somn AI
版本:v1.0.0
日期:2026-04-02
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from collections import defaultdict
import uuid

class ThinkingMode(Enum):
    """思维模式"""
    SYSTEMATIC = "系统思维"  # 整体性,关联性
    DESIGN = "设计思维"  # 以人为本,创新解决方案
    CRITICAL = "批判性思维"  # 质疑,分析,评估
    CREATIVE = "创造性思维"  # 发散,联想,突破
    LOGICAL = "逻辑思维"  # 推理,演绎,归纳
    LATERAL = "横向思维"  # 跨界,类比,跳跃
    PROBABILISTIC = "概率思维"  # 不确定性,风险评估
    FIRST_PRINCIPLES = "第一性原理"  # 从本质出发
    INVERSION = "逆向思维"  # 反过来想
    DESIGNED = "设计思维"  # 以用户为中心
    SCENARIO = "情景思维"  # 设想多种可能
    WIN_WIN = "双赢思维"  # 合作共赢

@dataclass
class ThinkingAnalysis:
    """思维分析"""
    mode: ThinkingMode
    relevance: float  # 相关度 0-1
    key_questions: List[str]
    approach_description: str
    strengths: List[str]
    limitations: List[str]

@dataclass
class ProblemProfile:
    """问题画像"""
    problem: str
    problem_type: str  # 问题类型
    complexity: str  # 简单/复杂/混乱
    time_horizon: str  # 短期/中期/长期
    stakeholder_count: str  # 单方/多方
    recommended_modes: List[ThinkingMode]
    analysis_results: List[ThinkingAnalysis]

class ThinkingModeFusionEngine:
    """
    思维模式fusion引擎
    
    基于<底层逻辑><格局><闭环思维><逆转思维><逆思维心理学>等构建,
    提供多种思维模式的unified调用接口.
    
    主要功能:
    1. 问题类型recognize
    2. 思维模式推荐
    3. 多模式分析
    4. fusiondecision
    """
    
    # 思维模式详细定义
    THINKING_MODE_DEFINITIONS = {
        ThinkingMode.SYSTEMATIC: {
            "核心": "整体大于部分之和",
            "关键词": ["系统", "要素", "关系", "反馈", "涌现"],
            "问题类型": ["复杂系统", "组织问题", "流程优化"],
            "步骤": [
                "recognize系统要素",
                "分析要素间关系",
                "recognize反馈回路",
                "寻找杠杆点"
            ],
            "优势": ["全面性", "前瞻性", "避免局部优化"],
            "局限": ["可能过于复杂", "难以精确"]
        },
        ThinkingMode.DESIGN: {
            "核心": "以人为中心的创新",
            "关键词": ["用户", "同理心", "原型", "测试", "迭代"],
            "问题类型": ["产品设计", "服务优化", "体验提升"],
            "步骤": [
                "同理心理解用户",
                "定义问题",
                "构思解决方案",
                "制作原型",
                "测试迭代"
            ],
            "优势": ["用户导向", "创新性", "实践性"],
            "局限": ["可能忽视技术约束", "迭代成本"]
        },
        ThinkingMode.CRITICAL: {
            "核心": "质疑一切,有理有据",
            "关键词": ["质疑", "证据", "推理", "假设", "偏见"],
            "问题类型": ["评估judge", "decision审查", "信息judge"],
            "步骤": [
                "明确论点和假设",
                "评估证据质量",
                "检查逻辑谬误",
                "考虑替代解释"
            ],
            "优势": ["避免错误", "深度分析", "独立judge"],
            "局限": ["可能过于消极", "action迟缓"]
        },
        ThinkingMode.CREATIVE: {
            "核心": "突破常规,创造可能",
            "关键词": ["创意", "发散", "联想", "组合", "打破"],
            "问题类型": ["寻找创意", "解决问题", "产品创新"],
            "步骤": [
                "打破思维定式",
                "发散思维产生想法",
                "联想和类比",
                "组合和重组",
                "筛选优化"
            ],
            "优势": ["创新性", "突破性", "可能性"],
            "局限": ["可能不切实际", "难以量化"]
        },
        ThinkingMode.LOGICAL: {
            "核心": "推理的确定性",
            "关键词": ["逻辑", "推理", "因果", "演绎", "归纳"],
            "问题类型": ["分析推理", "证明验证", "因果分析"],
            "步骤": [
                "明确前提",
                "应用推理规则",
                "得出结论",
                "验证逻辑链"
            ],
            "优势": ["严谨性", "确定性", "可验证"],
            "局限": ["依赖前提准确性", "处理不确定性困难"]
        },
        ThinkingMode.LATERAL: {
            "核心": "跨界跳跃,意外发现",
            "关键词": ["跨界", "类比", "跳跃", "意外", "侧面"],
            "问题类型": ["创新问题", "难题突破", "寻找灵感"],
            "步骤": [
                "从问题侧面试探",
                "寻找类似问题",
                "跨界借鉴",
                "产生意外解决方案"
            ],
            "优势": ["创新性", "突破性", "启发性"],
            "局限": ["不确定性高", "难以系统化"]
        },
        ThinkingMode.PROBABILISTIC: {
            "核心": "不确定性下的decision",
            "关键词": ["概率", "风险", "期望值", "不确定性", "贝叶斯"],
            "问题类型": ["风险评估", "投资decision", "预测分析"],
            "步骤": [
                "recognize不确定因素",
                "估计概率分布",
                "计算期望值",
                "敏感性分析"
            ],
            "优势": ["量化风险", "科学decision", "可更新"],
            "局限": ["依赖概率估计", "计算复杂"]
        },
        ThinkingMode.FIRST_PRINCIPLES: {
            "核心": "从本质出发",
            "关键词": ["本质", "基本", "假设", "重新构建", "第一性"],
            "问题类型": ["战略decision", "创新突破", "根本问题"],
            "步骤": [
                "分解问题到基本元素",
                "质疑每个假设",
                "从本质重建",
                "验证新方案"
            ],
            "优势": ["根本性", "创新性", "避免惯性"],
            "局限": ["耗时", "需要深度思考能力"]
        },
        ThinkingMode.INVERSION: {
            "核心": "反过来想",
            "关键词": ["逆向", "反过来", "避免失败", "倒推"],
            "问题类型": ["风险规避", "目标设定", "问题解决"],
            "步骤": [
                "明确目标",
                "倒推需要的条件",
                "recognize可能的障碍",
                "制定规避strategy"
            ],
            "优势": ["避免错误", "全面性", "action导向"],
            "局限": ["可能过于保守", "需要想象力"]
        },
        ThinkingMode.WIN_WIN: {
            "核心": "创造增量价值",
            "关键词": ["双赢", "合作", "增量", "价值创造", "互利"],
            "问题类型": ["谈判协商", "合作decision", "利益分配"],
            "步骤": [
                "理解各方利益",
                "扩大共同利益池",
                "创造增量价值",
                "公平分配"
            ],
            "优势": ["合作性", "持久性", "价值创造"],
            "局限": ["耗时", "需要信任基础"]
        }
    }
    
    # 问题类型mapping
    PROBLEM_TYPE_MAPPINGS = {
        "战略": [ThinkingMode.FIRST_PRINCIPLES, ThinkingMode.SYSTEMATIC, ThinkingMode.INVERSION],
        "创新": [ThinkingMode.CREATIVE, ThinkingMode.DESIGN, ThinkingMode.LATERAL],
        "decision": [ThinkingMode.CRITICAL, ThinkingMode.PROBABILISTIC, ThinkingMode.LOGICAL],
        "风险": [ThinkingMode.INVERSION, ThinkingMode.PROBABILISTIC, ThinkingMode.CRITICAL],
        "关系": [ThinkingMode.WIN_WIN, ThinkingMode.SYSTEMATIC, ThinkingMode.LATERAL],
        "执行": [ThinkingMode.LOGICAL, ThinkingMode.SYSTEMATIC, ThinkingMode.DESIGN],
        "学习": [ThinkingMode.FIRST_PRINCIPLES, ThinkingMode.CRITICAL, ThinkingMode.SYSTEMATIC],
        "沟通": [ThinkingMode.WIN_WIN, ThinkingMode.CRITICAL, ThinkingMode.SYSTEMATIC]
    }
    
    def __init__(self):
        self.analysis_cache: Dict[str, ProblemProfile] = {}
        self.mode_usage_stats: Dict[str, int] = defaultdict(int)
    
    def analyze_problem(self, problem: str) -> ProblemProfile:
        """
        分析问题并推荐思维模式
        
        Args:
            problem: 问题描述
            
        Returns:
            ProblemProfile: 问题画像
        """
        # recognize问题类型
        problem_type = self._classify_problem(problem)
        
        # judge复杂度
        complexity = self._assess_complexity(problem)
        
        # judge时间跨度
        time_horizon = self._assess_time_horizon(problem)
        
        # judge利益相关方
        stakeholder_count = self._assess_stakeholders(problem)
        
        # 推荐思维模式
        recommended_modes = self._recommend_modes(problem_type, complexity, stakeholder_count)
        
        # generate分析
        analysis_results = []
        for mode in recommended_modes[:3]:
            analysis = self._analyze_with_mode(problem, mode)
            analysis_results.append(analysis)
        
        profile = ProblemProfile(
            problem=problem,
            problem_type=problem_type,
            complexity=complexity,
            time_horizon=time_horizon,
            stakeholder_count=stakeholder_count,
            recommended_modes=recommended_modes,
            analysis_results=analysis_results
        )
        
        self.analysis_cache[problem] = profile
        return profile
    
    def _classify_problem(self, problem: str) -> str:
        """分类问题"""
        text_lower = problem.lower()
        
        for ptype, modes in self.PROBLEM_TYPE_MAPPINGS.items():
            if ptype in text_lower:
                return ptype
        
        # 默认分类
        if any(kw in text_lower for kw in ["如何", "怎么", "方法"]):
            return "执行"
        elif any(kw in text_lower for kw in ["为什么", "原因", "分析"]):
            return "decision"
        elif any(kw in text_lower for kw in ["是否", "应该", "judge"]):
            return "decision"
        else:
            return "创新"
    
    def _assess_complexity(self, problem: str) -> str:
        """评估复杂度"""
        # 简单metrics
        simple_indicators = ["一个", "简单", "直接", "单一"]
        # 复杂metrics
        complex_indicators = ["多个", "复杂", "涉及", "系统", "很多因素"]
        # 混乱metrics
        chaotic_indicators = ["混乱", "无序", "不确定", "模糊", "变化"]
        
        text_lower = problem.lower()
        
        if any(ind in text_lower for ind in chaotic_indicators):
            return "混乱"
        elif any(ind in text_lower for ind in complex_indicators):
            return "复杂"
        else:
            return "简单"
    
    def _assess_time_horizon(self, problem: str) -> str:
        """评估时间跨度"""
        text_lower = problem.lower()
        
        if any(kw in text_lower for kw in ["短期", "近期", "马上", "立刻"]):
            return "短期"
        elif any(kw in text_lower for kw in ["长期", "未来", "持续", "根本"]):
            return "长期"
        else:
            return "中期"
    
    def _assess_stakeholders(self, problem: str) -> str:
        """评估利益相关方"""
        text_lower = problem.lower()
        
        multi_indicators = ["他们", "大家", "所有", "合作", "谈判", "各方"]
        if any(ind in text_lower for ind in multi_indicators):
            return "多方"
        else:
            return "单方"
    
    def _recommend_modes(self, problem_type: str, complexity: str,
                        stakeholders: str) -> List[ThinkingMode]:
        """推荐思维模式"""
        base_modes = self.PROBLEM_TYPE_MAPPINGS.get(problem_type, [])
        
        # 根据复杂度调整
        if complexity == "混乱":
            base_modes.extend([ThinkingMode.PROBABILISTIC, ThinkingMode.INVERSION])
        elif complexity == "简单":
            base_modes.extend([ThinkingMode.LOGICAL, ThinkingMode.CRITICAL])
        
        # 根据利益相关方调整
        if stakeholders == "多方":
            base_modes.append(ThinkingMode.WIN_WIN)
        
        # 去重并返回前4个
        seen = set()
        unique_modes = []
        for mode in base_modes:
            if mode not in seen:
                seen.add(mode)
                unique_modes.append(mode)
        
        return unique_modes[:4]
    
    def _analyze_with_mode(self, problem: str, mode: ThinkingMode) -> ThinkingAnalysis:
        """用指定模式分析"""
        definition = self.THINKING_MODE_DEFINITIONS.get(mode, {})
        
        # generate关键问题
        key_questions = self._generate_mode_questions(problem, mode)
        
        # 计算相关度
        relevance = self._calculate_relevance(problem, mode)
        
        return ThinkingAnalysis(
            mode=mode,
            relevance=relevance,
            key_questions=key_questions,
            approach_description=definition.get("核心", ""),
            strengths=definition.get("优势", []),
            limitations=definition.get("局限", [])
        )
    
    def _generate_mode_questions(self, problem: str, mode: ThinkingMode) -> List[str]:
        """generate关键问题"""
        questions = {
            ThinkingMode.SYSTEMATIC: [
                "这个系统有哪些组成部分?",
                "各部分之间如何相互影响?",
                "什么是主要的反馈回路?",
                "哪里是系统的杠杆点?"
            ],
            ThinkingMode.DESIGN: [
                "用户真正需要什么?",
                "当前的痛点是什么?",
                "如何快速验证解决方案?",
                "如何迭代改进?"
            ],
            ThinkingMode.CRITICAL: [
                "这个结论的假设是什么?",
                "有什么证据支持?",
                "有什么可能的偏见?",
                "有什么替代解释?"
            ],
            ThinkingMode.CREATIVE: [
                "如果没有任何限制,我会怎么做?",
                "其他领域是如何解决类似问题的?",
                "最疯狂的想法是什么?",
                "如何组合这些想法?"
            ],
            ThinkingMode.LOGICAL: [
                "前提是什么?",
                "推理链条是否有效?",
                "结论是否必然得出?",
                "有什么逻辑漏洞?"
            ],
            ThinkingMode.PROBABILISTIC: [
                "有哪些不确定因素?",
                "每个结果的概率是多少?",
                "期望值如何?",
                "敏感性如何?"
            ],
            ThinkingMode.FIRST_PRINCIPLES: [
                "这件事的本质是什么?",
                "哪些假设可能是错的?",
                "如果从零开始,我会怎么做?",
                "什么是最基本的要素?"
            ],
            ThinkingMode.INVERSION: [
                "如何确保失败?",
                "最大的风险是什么?",
                "如何避免这些问题?",
                "反过来想会得到什么?"
            ],
            ThinkingMode.WIN_WIN: [
                "各方的核心利益是什么?",
                "如何扩大共同利益?",
                "如何创造增量价值?",
                "如何公平分配?"
            ]
        }
        
        return questions.get(mode, ["从该模式角度思考这个问题"])
    
    def _calculate_relevance(self, problem: str, mode: ThinkingMode) -> float:
        """计算相关度"""
        definition = self.THINKING_MODE_DEFINITIONS.get(mode, {})
        keywords = definition.get("关键词", [])
        
        text_lower = problem.lower()
        matches = sum(1 for kw in keywords if kw in text_lower)
        
        return min(1.0, 0.5 + matches * 0.1)
    
    def fuse_decision(self, profile: ProblemProfile) -> Dict:
        """
        fusion多模式分析,做出decision
        
        Args:
            profile: 问题画像
            
        Returns:
            Dict: fusiondecision结果
        """
        # 收集各模式的洞见
        insights_by_mode = {}
        for analysis in profile.analysis_results:
            insights_by_mode[analysis.mode.value] = {
                "key_questions": analysis.key_questions[:2],
                "approach": analysis.approach_description
            }
        
        # synthesize建议
        comprehensive_advice = self._synthesize_advice(profile)
        
        return {
            "problem": profile.problem,
            "recommended_modes": [m.value for m in profile.recommended_modes],
            "insights": insights_by_mode,
            "comprehensive_advice": comprehensive_advice,
            "action_plan": self._generate_action_plan(profile),
            "key_insight": self._get_key_insight(profile)
        }
    
    def _synthesize_advice(self, profile: ProblemProfile) -> List[str]:
        """synthesize建议"""
        advices = []
        
        # 基于问题类型
        if profile.problem_type == "战略":
            advices.append("从第一性原理出发,回归本质思考")
            advices.append("建立系统视角,考虑长期影响")
        
        elif profile.problem_type == "创新":
            advices.append("打破思维定式,尝试跨界借鉴")
            advices.append("快速原型和测试,小步迭代")
        
        elif profile.problem_type == "decision":
            advices.append("批判性审视假设和证据")
            advices.append("用概率思维评估风险")
        
        elif profile.problem_type == "风险":
            advices.append("逆向思考,预判可能的失败")
            advices.append("建立风险缓冲和应急预案")
        
        elif profile.problem_type == "执行":
            advices.append("逻辑分解任务,建立执行闭环")
            advices.append("持续反馈,及时调整")
        
        # 基于复杂度
        if profile.complexity == "混乱":
            advices.append("先稳定局面,再逐步优化")
            advices.append("接受不确定性,灵活应对")
        elif profile.complexity == "简单":
            advices.append("直接action,避免过度分析")
        
        return advices
    
    def _generate_action_plan(self, profile: ProblemProfile) -> List[str]:
        """generateaction计划"""
        plan = []
        
        # 第一步:理解
        plan.append(f"1. 理解问题:{profile.problem_type}问题,{profile.complexity}复杂度")
        
        # 第二步:分析
        plan.append(f"2. 分析角度:优先使用{profile.recommended_modes[0].value}")
        if len(profile.recommended_modes) > 1:
            plan.append(f"   辅助视角:{profile.recommended_modes[1].value}")
        
        # 第三步:decision
        plan.append("3. decision框架:synthesize各模式洞见,选择最优方案")
        
        # 第四步:执行
        plan.append("4. 执行监控:建立反馈闭环,及时调整")
        
        return plan
    
    def _get_key_insight(self, profile: ProblemProfile) -> str:
        """get关键洞见"""
        if profile.problem_type == "战略":
            return "战略问题需要长期视野和系统思考,不能只看眼前"
        elif profile.problem_type == "创新":
            return "创新往往来自跨界组合,不要自我设限"
        elif profile.problem_type == "decision":
            return "好decision建立在对假设的质疑和对不确定性的量化上"
        elif profile.problem_type == "风险":
            return "最好的风险管理是预判风险并做好准备"
        else:
            return "用多种思维模式审视问题,可以获得更全面的理解"
    
    def think_in_mode(self, problem: str, mode: ThinkingMode) -> Dict:
        """
        使用指定思维模式思考
        
        Args:
            problem: 问题
            mode: 思维模式
            
        Returns:
            Dict: 思考结果
        """
        definition = self.THINKING_MODE_DEFINITIONS.get(mode, {})
        
        return {
            "mode": mode.value,
            "core_principle": definition.get("核心", ""),
            "key_questions": self._generate_mode_questions(problem, mode),
            "steps": definition.get("步骤", []),
            "strengths": definition.get("优势", []),
            "thinking_result": self._apply_mode_thinking(problem, mode)
        }
    
    def _apply_mode_thinking(self, problem: str, mode: ThinkingMode) -> str:
        """应用思维模式"""
        # 这里应该根据不同模式generate具体的思考结果
        # 简化实现
        return f"使用{mode.value}思考:{problem}"
    
    def get_thinking_toolkit(self) -> Dict:
        """get思维工具箱"""
        toolkit = {}
        
        for mode, definition in self.THINKING_MODE_DEFINITIONS.items():
            toolkit[mode.value] = {
                "definition": definition.get("核心", ""),
                "keywords": definition.get("关键词", []),
                "steps": definition.get("步骤", []),
                "when_to_use": definition.get("问题类型", [])
            }
        
        return toolkit
    
    def compare_modes(self, modes: List[ThinkingMode]) -> Dict:
        """
        比较多种思维模式
        
        Args:
            modes: 要比较的模式列表
            
        Returns:
            Dict: 比较结果
        """
        comparison = {
            "modes": [m.value for m in modes],
            "differences": [],
            "synergies": []
        }
        
        # 找出差异
        for i, mode1 in enumerate(modes):
            for mode2 in modes[i+1:]:
                comparison["differences"].append({
                    "between": f"{mode1.value} vs {mode2.value}",
                    "difference": f"{mode1.value}侧重{self.THINKING_MODE_DEFINITIONS[mode1]['核心']},"
                                  f"{mode2.value}侧重{self.THINKING_MODE_DEFINITIONS[mode2]['核心']}"
                })
        
        # 找出协同
        if len(modes) >= 2:
            comparison["synergies"].append(
                f"{modes[0].value}提供方向,{modes[1].value}提供方法,结合使用效果更佳"
            )
        
        return comparison

def create_fusion_engine() -> ThinkingModeFusionEngine:
    """工厂函数"""
    return ThinkingModeFusionEngine()
