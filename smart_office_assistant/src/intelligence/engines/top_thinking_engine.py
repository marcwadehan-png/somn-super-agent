"""
__all__ = [
    'create_thinking_toolkit',
    'get_method_comparison',
    'get_toolkit',
    'integrate_with_somn',
    'recommend_methods',
    'solve_with_method',
    'synthesize',
    'synthesize_methods',
]

顶级思维法集成模块 - Top Thinking Methods Integration Module
v7.0.0 版本

整合全球顶级思维方法论,构建synthesize思维工具箱:

[东方智慧思维]
1. 王阳明xinxue - 心即理,知行合一,致良知
2. 素书智慧 - 五德decision,人才recognize,修身二十法
3. 道家辩证 - 阴阳平衡,柔弱胜刚,无为而治

[西方经典思维]
4. 麦肯锡方法 - MECE,金字塔原理,假设驱动
5. 第一性原理 - 拆解到不可约分的基本事实
6. 批判性思维 - 质疑假设,评估证据,逻辑推理

[创意与decision思维]
7. 逆向思维 - 反过来想,往往更容易找到答案
8. 博弈思维 - strategy互动中的最优decision
9. 系统思维 - 整体观,动态观,演化观

[现代应用思维]
10. 设计思维 - 共情,定义,创意,原型,测试
11. 精益思维 - 最小可行产品,快速迭代
12. 成长思维 - 能力可发展,失败是学习

版本历史:
- v7.0.0 (2026-04-02): 初始版本,集成12种顶级思维方法
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

class ThinkingMethod(Enum):
    """顶级思维方法"""
    # 东方智慧
    YANGMING_XIN = "阳明xinxue"
    SUFU_WISDOM = "素书智慧"
    DAOIST_DIALECTICS = "道家辩证"
    
    # 西方经典
    MCKINSEY = "麦肯锡方法"
    FIRST_PRINCIPLES = "第一性原理"
    CRITICAL = "批判性思维"
    
    # 创意decision
    REVERSE = "逆向思维"
    GAME_THEORY = "博弈思维"
    SYSTEMIC = "系统思维"
    
    # 现代应用
    DESIGN = "设计思维"
    LEAN = "精益思维"
    GROWTH_MINDSET = "成长思维"

class ProblemType(Enum):
    """问题类型"""
    ANALYSIS = "分析型"      # 需要深入理解
    CREATIVE = "创意型"     # 需要创新突破
    DECISION = "decision型"     # 需要选择judge
    STRATEGY = "战略型"     # 需要长期规划
    COMPLEX = "复杂型"      # 多种因素交织

@dataclass
class MethodApplication:
    """方法应用指南"""
    method: ThinkingMethod
    applicability: float  # 适用度 0-1
    when_to_use: str
    key_steps: List[str]
    core_questions: List[str]
    pitfalls: List[str]
    example: str

@dataclass
class ThinkingToolkit:
    """思维工具箱"""
    problem: str
    problem_type: ProblemType
    recommended_methods: List[MethodApplication]
    integrated_approach: str
    action_plan: List[str]
    expected_outcome: str

@dataclass
class CrossMethodSynthesis:
    """跨方法synthesize"""
    problem: str
    methods_used: List[ThinkingMethod]
    synthesis_insight: str
    complementary_points: List[str]
    conflict_points: List[str]
    integrated_solution: str

class TopThinkingMethodsEngine:
    """
    顶级思维法集成模块
    
    功能:
    1. 方法推荐 - 根据问题类型推荐最佳思维方法
    2. 方法fusion - 整合多种思维方法
    3. 实战应用 - 具体问题的思维指导
    4. 陷阱预警 - 常见思维误区提醒
    
    应用场景:
    - 复杂问题分析
    - 战略decision制定
    - 创意方案generate
    - 批判性评估
    """
    
    # 思维方法详细定义
    METHOD_DEFINITIONS = {
        ThinkingMethod.YANGMING_XIN: {
            "origin": "中国明代王阳明",
            "core": "心即理,知行合一,致良知",
            "essence": "相信内在judge,在事上磨练",
            "steps": [
                "静心:让心静下来",
                "观照:观察内心的声音",
                "良知judge:让良知做决定",
                "action:立即action",
                "反思:复盘结果"
            ],
            "best_for": ["道德困境", "内心纠结", "价值观问题"],
            "pitfalls": ["过度内省", "忽视外部信息"]
        },
        ThinkingMethod.SUFU_WISDOM: {
            "origin": "中国古典<素书>",
            "core": "道,德,仁,,礼五位一体",
            "essence": "人才recognize与五德decision",
            "steps": [
                "明道:理解事物本质",
                "修德:培养品德修养",
                "守仁:保持仁爱之心",
                "行义:做正确的事",
                "循礼:遵守规范秩序"
            ],
            "best_for": ["人才评估", "领导力发展", "组织建设"],
            "pitfalls": ["过于理想化", "忽视变通"]
        },
        ThinkingMethod.DAOIST_DIALECTICS: {
            "origin": "中国道家<道德经>",
            "core": "阴阳平衡,柔弱胜刚",
            "essence": "对立unified,转化循环",
            "steps": [
                "辨阴阳:recognize对立因素",
                "观转化:看转化方向",
                "求平衡:找动态平衡点",
                "顺势为:顺应规律action"
            ],
            "best_for": ["矛盾分析", "风险评估", "战略调整"],
            "pitfalls": ["消极无为", "过于玄虚"]
        },
        ThinkingMethod.MCKINSEY: {
            "origin": "麦肯锡咨询公司",
            "core": "MECE,金字塔原理",
            "essence": "结构化分解,逻辑化表达",
            "steps": [
                "界定问题:明确真正的问题",
                "分解问题:MECE分类",
                "假设驱动:提出假设",
                "验证假设:收集证据",
                "形成结论:逻辑推导"
            ],
            "best_for": ["商业分析", "问题诊断", "方案呈现"],
            "pitfalls": ["过度分解", "忽视细节"]
        },
        ThinkingMethod.FIRST_PRINCIPLES: {
            "origin": "亚里士多德,后由马斯克推广",
            "core": "拆解到不可约分的基本事实",
            "essence": "从零开始思考,不接受假设",
            "steps": [
                "拆解:分解到最基本元素",
                "质疑:挑战每一个假设",
                "重建:从事实重建解决方案"
            ],
            "best_for": ["创新突破", "颠覆性思考", "根本性变革"],
            "pitfalls": ["效率较低", "可能过度复杂"]
        },
        ThinkingMethod.CRITICAL: {
            "origin": "西方哲学传统",
            "core": "质疑假设,评估证据,逻辑推理",
            "essence": "不轻信,系统性检验",
            "steps": [
                "质疑前提:这是真的吗?",
                "检查证据:证据充分吗?",
                "检验逻辑:推理通顺吗?",
                "考虑替代:还有其他解释吗?"
            ],
            "best_for": ["评估judge", "防止被误导", "深度理解"],
            "pitfalls": ["过度质疑", "难以action"]
        },
        ThinkingMethod.REVERSE: {
            "origin": "雅各布悖论",
            "core": "反过来想,往往更容易找到答案",
            "essence": "逆向思考,绕过思维定势",
            "steps": [
                "正向列出问题",
                "反转问题",
                "探索反面的原因",
                "找到新路径"
            ],
            "best_for": ["突破困境", "发现盲点", "创新方案"],
            "pitfalls": ["反向不一定正确", "可能过于极端"]
        },
        ThinkingMethod.GAME_THEORY: {
            "origin": "冯·诺依曼,纳什",
            "core": "strategy互动中的最优decision",
            "essence": "考虑对手反应,找到均衡",
            "steps": [
                "recognize参与人",
                "分析利益",
                "预测反应",
                "寻找均衡"
            ],
            "best_for": ["竞争strategy", "谈判博弈", "多方协调"],
            "pitfalls": ["假设理性", "信息不完全"]
        },
        ThinkingMethod.SYSTEMIC: {
            "origin": "系统论,控制论",
            "core": "整体观,动态观,演化观",
            "essence": "看整体,不只看部分",
            "steps": [
                "recognize要素",
                "理清关系",
                "理解反馈",
                "预测行为"
            ],
            "best_for": ["复杂系统", "组织问题", "政策设计"],
            "pitfalls": ["过于复杂", "难以操作"]
        },
        ThinkingMethod.DESIGN: {
            "origin": "斯坦福设计学院",
            "core": "共情,定义,创意,原型,测试",
            "essence": "以用户为中心的创新方法",
            "steps": [
                "共情:深入理解用户",
                "定义:明确问题",
                "创意:产生想法",
                "原型:快速制作",
                "测试:验证迭代"
            ],
            "best_for": ["产品设计", "服务创新", "用户体验"],
            "pitfalls": ["用户可能说谎", "迭代可能失控"]
        },
        ThinkingMethod.LEAN: {
            "origin": "精益制造/创业",
            "core": "MVP,快速迭代,数据驱动",
            "essence": "最小成本验证,最大学习",
            "steps": [
                "提出假设",
                "构建MVP",
                "测量数据",
                "学习迭代"
            ],
            "best_for": ["创业验证", "产品迭代", "流程优化"],
            "pitfalls": ["过早迭代", "数据偏见"]
        },
        ThinkingMethod.GROWTH_MINDSET: {
            "origin": "卡罗尔·德韦克",
            "core": "能力可发展,失败是学习机会",
            "essence": "成长导向,积极面对挑战",
            "steps": [
                "接受挑战",
                "面对挫折",
                "寻找strategy",
                "持续努力"
            ],
            "best_for": ["个人发展", "团队建设", "学习改进"],
            "pitfalls": ["忽视外部限制", "过度强调努力"]
        }
    }
    
    # 问题类型与推荐方法mapping
    PROBLEM_METHOD_MAP = {
        ProblemType.ANALYSIS: [ThinkingMethod.MCKINSEY, ThinkingMethod.CRITICAL, 
                               ThinkingMethod.FIRST_PRINCIPLES],
        ProblemType.CREATIVE: [ThinkingMethod.DESIGN, ThinkingMethod.REVERSE,
                              ThinkingMethod.GAME_THEORY],
        ProblemType.DECISION: [ThinkingMethod.CRITICAL, ThinkingMethod.YANGMING_XIN,
                              ThinkingMethod.SUFU_WISDOM],
        ProblemType.STRATEGY: [ThinkingMethod.SYSTEMIC, ThinkingMethod.DAOIST_DIALECTICS,
                              ThinkingMethod.GAME_THEORY],
        ProblemType.COMPLEX: [ThinkingMethod.SYSTEMIC, ThinkingMethod.FIRST_PRINCIPLES,
                             ThinkingMethod.DESIGN]
    }
    
    def __init__(self):
        """init顶级思维法引擎"""
        self.name = "顶级思维法集成模块"
        self.version="6.2.0"
        logger.info(f"{self.name} {self.version} init完成")
    
    def recommend_methods(self,
                         problem: str,
                         problem_type: ProblemType) -> List[MethodApplication]:
        """
        推荐适合的思维方法
        
        Args:
            problem: 问题描述
            problem_type: 问题类型
        
        Returns:
            推荐的思维方法列表
        """
        recommended_types = self.PROBLEM_METHOD_MAP.get(problem_type, 
                                                         [ThinkingMethod.CRITICAL])
        
        applications = []
        for method_type in recommended_types:
            definition = self.METHOD_DEFINITIONS[method_type]
            
            # 计算适用度
            applicability = 0.8
            for keyword in definition.get("best_for", []):
                if keyword in problem:
                    applicability = 1.0
                    break
            
            app = MethodApplication(
                method=method_type,
                applicability=applicability,
                when_to_use=definition["core"],
                key_steps=definition["steps"],
                core_questions=self._get_core_questions(method_type),
                pitfalls=definition["pitfalls"],
                example=definition["origin"]
            )
            applications.append(app)
        
        return applications
    
    def _get_core_questions(self, method: ThinkingMethod) -> List[str]:
        """get核心问题"""
        questions = {
            ThinkingMethod.YANGMING_XIN: [
                "我的良知如何judge?",
                "如果这是圣人,会怎么做?",
                "十年后回看,这个选择对吗?"
            ],
            ThinkingMethod.SUFU_WISDOM: [
                "是否符合道义?",
                "是否合乎仁德?",
                "是否遵循法度?"
            ],
            ThinkingMethod.DAOIST_DIALECTICS: [
                "阴阳两面是什么?",
                "对立如何转化?",
                "平衡点在哪里?"
            ],
            ThinkingMethod.MCKINSEY: [
                "真正的问题是什么?",
                "如何MECE分解?",
                "核心假设是什么?"
            ],
            ThinkingMethod.FIRST_PRINCIPLES: [
                "最基本的事实是什么?",
                "什么假设可以被质疑?",
                "如何从零重建?"
            ],
            ThinkingMethod.CRITICAL: [
                "前提是什么?可靠吗?",
                "证据充分吗?",
                "逻辑通顺吗?"
            ],
            ThinkingMethod.REVERSE: [
                "反过来是什么?",
                "最坏的情况是什么?",
                "如果相反呢?"
            ],
            ThinkingMethod.GAME_THEORY: [
                "其他参与人会怎么做?",
                "各方利益是什么?",
                "均衡点在哪里?"
            ],
            ThinkingMethod.SYSTEMIC: [
                "整体是什么样的?",
                "要素之间有什么关系?",
                "反馈回路是什么?"
            ],
            ThinkingMethod.DESIGN: [
                "用户真正需要什么?",
                "如何快速验证?",
                "从失败中学到什么?"
            ],
            ThinkingMethod.LEAN: [
                "最小可行产品是什么?",
                "需要验证什么假设?",
                "如何快速迭代?"
            ],
            ThinkingMethod.GROWTH_MINDSET: [
                "这次失败教我什么?",
                "如何把挑战当机会?",
                "需要发展什么能力?"
            ]
        }
        return questions.get(method, [])
    
    def solve_with_method(self,
                         problem: str,
                         method: ThinkingMethod) -> Dict[str, Any]:
        """
        使用特定方法解决问题
        
        Args:
            problem: 问题描述
            method: 思维方法
        
        Returns:
            思维过程与结果
        """
        definition = self.METHOD_DEFINITIONS[method]
        
        result = {
            "method": method.value,
            "origin": definition["origin"],
            "core_principle": definition["core"],
            "steps": [],
            "analysis": [],
            "conclusion": "",
            "pitfalls_to_avoid": definition["pitfalls"]
        }
        
        # generate步骤分析
        for i, step in enumerate(definition["steps"]):
            result["steps"].append({
                "step": i + 1,
                "name": step,
                "guidance": f"应用'{step}'于当前问题",
                "reflection": ""
            })
        
        return result
    
    def synthesize_methods(self,
                          problem: str,
                          methods: List[ThinkingMethod]) -> CrossMethodSynthesis:
        """
        synthesize多种思维方法
        
        Args:
            problem: 问题描述
            methods: 要synthesize的方法列表
        
        Returns:
            跨方法synthesize分析
        """
        # 提取各方法的核心
        cores = [self.METHOD_DEFINITIONS[m]["core"] for m in methods]
        
        synthesis = CrossMethodSynthesis(
            problem=problem,
            methods_used=methods,
            synthesis_insight="",
            complementary_points=[],
            conflict_points=[],
            integrated_solution=""
        )
        
        # recognize互补点
        complementary = {
            (ThinkingMethod.CRITICAL, ThinkingMethod.GAME_THEORY):
                "批判性评估+博弈strategy=更稳健decision",
            (ThinkingMethod.FIRST_PRINCIPLES, ThinkingMethod.DESIGN):
                "根本思考+用户中心=创新且可行方案",
            (ThinkingMethod.DAOIST_DIALECTICS, ThinkingMethod.SYSTEMIC):
                "阴阳辩证+系统思维=动态平衡的全局观",
            (ThinkingMethod.YANGMING_XIN, ThinkingMethod.GROWTH_MINDSET):
                "良知judge+成长心态=内在指引+持续进步"
        }
        
        synthesis.complementary_points = [
            f"{methods[0].value} + {methods[1].value}: 互补增强"
            for methods in complementary.keys()
            if methods[0] in methods and methods[1] in methods
        ]
        
        # generate整合方案
        synthesis.integrated_solution = f"""
        [多方法整合方案]
        
        第一层:阳明xinxuejudge方向
        - 静心观照:这是真正重要的问题吗?
        - 良知检验:什么是最正确的选择?
        
        第二层:批判性思维拆解
        - 质疑假设:哪些前提可能是错的?
        - 评估证据:支持/反对的证据是什么?
        
        第三层:系统思维全局把握
        - 整体关系:这个问题与什么相关?
        - 动态演化:系统将如何发展?
        
        第四层:设计思维找方案
        - 用户视角:用户真正需要什么?
        - 快速验证:如何最小成本测试?
        
        整合结论:先用心judge方向,再用理性分析,最后用创意突破.
        """
        
        return synthesis
    
    def create_thinking_toolkit(self,
                                problem: str,
                                problem_type: ProblemType) -> ThinkingToolkit:
        """
        创建思维工具箱
        
        Args:
            problem: 问题描述
            problem_type: 问题类型
        
        Returns:
            synthesize思维工具箱
        """
        recommended = self.recommend_methods(problem, problem_type)
        
        toolkit = ThinkingToolkit(
            problem=problem,
            problem_type=problem_type,
            recommended_methods=recommended,
            integrated_approach="",
            action_plan=[],
            expected_outcome=""
        )
        
        # generate整合方法
        toolkit.integrated_approach = f"""
        [问题类型]:{problem_type.value}
        [推荐方法]:{' / '.join([m.method.value for m in recommended])}
        
        [整合应用]:
        1. 首先用{recommended[0].method.value}定义和分解问题
        2. 然后用{recommended[1].method.value if len(recommended) > 1 else recommended[0].method.value}进行深度分析
        3. 最后用{recommended[-1].method.value}形成action方案
        """
        
        # generateaction计划
        toolkit.action_plan = [
            f"步骤1:使用{recommended[0].method.value}分析问题",
            f"步骤2:提出{recommended[0].method.value}的核心问题",
            f"步骤3:使用{recommended[1].method.value if len(recommended) > 1 else recommended[0].method.value}验证假设",
            "步骤4:整合各方见解,形成synthesize方案",
            "步骤5:制定具体action计划"
        ]
        
        toolkit.expected_outcome = "通过多方法整合,形成全面,深入,可行的解决方案"
        
        return toolkit
    
    def get_method_comparison(self) -> Dict[str, Any]:
        """
        get方法对比
        
        Returns:
            各方法的对比分析
        """
        comparison = {
            "标题": "顶级思维方法对比",
            "维度": ["方法", "起源", "核心", "优势", "局限", "适用场景"],
            "rows": []
        }
        
        for method in ThinkingMethod:
            defn = self.METHOD_DEFINITIONS[method]
            comparison["rows"].append({
                "method": method.value,
                "origin": defn["origin"],
                "core": defn["core"],
                "advantage": defn["steps"][0] if defn["steps"] else "",
                "limitation": defn["pitfalls"][0] if defn["pitfalls"] else "",
                "scenarios": ",".join(defn["best_for"][:2])
            })
        
        return comparison
    
    def integrate_with_somn(self,
                           user_query: str,
                           context: Dict[str, Any]) -> Dict[str, Any]:
        """
        与Somn系统fusion
        
        Args:
            user_query: 用户查询
            context: 上下文
        
        Returns:
            思维方法分析结果
        """
        # 分析问题类型
        query_lower = user_query.lower()
        
        if any(word in query_lower for word in ["分析", "研究", "理解"]):
            problem_type = ProblemType.ANALYSIS
        elif any(word in query_lower for word in ["创意", "创新", "突破"]):
            problem_type = ProblemType.CREATIVE
        elif any(word in query_lower for word in ["decision", "选择", "决定"]):
            problem_type = ProblemType.DECISION
        elif any(word in query_lower for word in ["战略", "规划", "长期"]):
            problem_type = ProblemType.STRATEGY
        else:
            problem_type = ProblemType.COMPLEX
        
        # 创建工具箱
        toolkit = self.create_thinking_toolkit(user_query, problem_type)
        
        result = {
            "engine": "顶级思维法集成模块",
            "problem_type": problem_type.value,
            "recommended_methods": [m.method.value for m in toolkit.recommended_methods],
            "primary_method": toolkit.recommended_methods[0].method.value if toolkit.recommended_methods else "",
            "integrated_approach": toolkit.integrated_approach,
            "action_plan": toolkit.action_plan,
            "method_comparison": self.get_method_comparison()["rows"][:3],
            "quick_tips": [
                "遇到复杂问题,先用批判性思维质疑假设",
                "需要创新时,尝试逆向思维",
                "战略decision时,结合系统思维和博弈思维",
                "最后用阳明xinxue做良知检验"
            ]
        }
        
        return result

# 向后兼容别名 - 多个模块引用 TopThinkingEngine
TopThinkingEngine = TopThinkingMethodsEngine

# 便捷函数
def get_toolkit(problem: str, ptype: str = "COMPLEX") -> ThinkingToolkit:
    """快速get思维工具箱"""
    engine = TopThinkingMethodsEngine()
    problem_type = ProblemType[ptype.upper()]
    return engine.create_thinking_toolkit(problem, problem_type)

def synthesize(problem: str, method_names: List[str]) -> CrossMethodSynthesis:
    """快速synthesize多种方法"""
    engine = TopThinkingMethodsEngine()
    methods = [ThinkingMethod[m.upper()] for m in method_names]
    return engine.synthesize_methods(problem, methods)

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
