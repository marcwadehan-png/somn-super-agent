"""
神之架构 - 动态部门能力矩阵 V1.0.0
_dynamic_department_matrix.py

核心理念：部门处理问题类别，而非单个问题
- 问题按大类（ProblemCategory）归类
- 每个部门声明自己能处理的问题类别
- 动态构建路由，实现真正的网状串联

版本: 5.1.0
日期: 2026-04-22
"""

from enum import Enum
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass


class ProblemCategory(Enum):
    """问题大类 - 部门处理的是类别而非单个问题"""
    # 战略决策类
    STRATEGY = "战略决策"           # 战略规划、转型、变革
    CRISIS = "危机处理"             # 危机应对、风险管控
    COMPETITION = "竞争博弈"         # 竞争策略、谈判博弈
    
    # 数据分析类
    ANALYSIS = "分析诊断"           # 市场分析、数据洞察、趋势预测
    MARKETING = "营销传播"          # 品牌营销、消费者洞察
    
    # 智慧方案类
    WISDOM = "智慧方案"             # 方案设计、创新思考
    NARRATIVE = "叙事构建"          # 故事创作、人物塑造
    
    # 执行落地类
    EXECUTION = "执行落地"           # 闭环执行、增长驱动
    TECHNICAL = "技术工程"           # 科学验证、系统分析
    
    # 审核监督类
    REVIEW = "审核监督"             # 风险评估、合规审查
    ETHICS = "伦理道德"              # 伦理考量、心态调适


# ═══════════════════════════════════════════════════════════════
# 问题类别与具体问题的映射（可配置）
# ═══════════════════════════════════════════════════════════════

PROBLEM_CATEGORY_MAP: Dict[str, ProblemCategory] = {
    # 战略决策类
    "STRATEGY": ProblemCategory.STRATEGY,
    "CHANGE": ProblemCategory.STRATEGY,
    "GOVERNANCE": ProblemCategory.STRATEGY,
    "LEADERSHIP": ProblemCategory.STRATEGY,
    
    # 危机处理类
    "CRISIS": ProblemCategory.COMPETITION,
    "RISK": ProblemCategory.REVIEW,
    "DEFENSE": ProblemCategory.COMPETITION,
    "ATTACK": ProblemCategory.COMPETITION,
    
    # 竞争博弈类
    "COMPETITION": ProblemCategory.COMPETITION,
    "NEGOTIATION": ProblemCategory.COMPETITION,
    "WAR_ECONOMY_NEXUS": ProblemCategory.COMPETITION,
    
    # 数据分析类
    "MARKET_ANALYSIS": ProblemCategory.ANALYSIS,
    "SOCIAL_DEVELOPMENT": ProblemCategory.ANALYSIS,
    "PSYCHOLOGICAL_INSIGHT": ProblemCategory.ANALYSIS,
    "HISTORICAL_ANALYSIS": ProblemCategory.ANALYSIS,
    "THOUGHT_EVOLUTION": ProblemCategory.ANALYSIS,
    "ECONOMIC_EVOLUTION": ProblemCategory.ANALYSIS,
    "TECH_HISTORY": ProblemCategory.ANALYSIS,
    "CROSS_DIMENSION": ProblemCategory.ANALYSIS,
    
    # 营销传播类
    "MARKETING": ProblemCategory.MARKETING,
    "CONSUMER_MARKETING": ProblemCategory.MARKETING,
    "BRAND_STRATEGY": ProblemCategory.MARKETING,
    "SOCIAL_STABILITY": ProblemCategory.MARKETING,
    
    # 智慧方案类
    "TALENT": ProblemCategory.WISDOM,
    "PERSONNEL": ProblemCategory.WISDOM,
    "CULTURE": ProblemCategory.WISDOM,
    "GROWTH_MINDSET": ProblemCategory.WISDOM,
    "LONGTERM": ProblemCategory.WISDOM,
    "REVERSE": ProblemCategory.WISDOM,
    "CLOSED_LOOP": ProblemCategory.WISDOM,
    
    # 叙事构建类
    "NARRATIVE": ProblemCategory.NARRATIVE,
    "CHARACTER": ProblemCategory.NARRATIVE,
    "RESILIENCE": ProblemCategory.NARRATIVE,
    "CREATION_MYTH": ProblemCategory.NARRATIVE,
    "APOCALYPSE": ProblemCategory.NARRATIVE,
    "CYCLICAL": ProblemCategory.NARRATIVE,
    
    # 执行落地类
    "EXECUTION": ProblemCategory.EXECUTION,
    "GROWTH": ProblemCategory.EXECUTION,
    "HABIT": ProblemCategory.EXECUTION,
    "NUDGE": ProblemCategory.EXECUTION,
    "WILLPOWER": ProblemCategory.EXECUTION,
    
    # 技术工程类
    "SCIENTIFIC_METHOD": ProblemCategory.TECHNICAL,
    "SYSTEM_THINKING": ProblemCategory.TECHNICAL,
    "EVIDENCE": ProblemCategory.TECHNICAL,
    "PHYSICS_ANALYSIS": ProblemCategory.TECHNICAL,
    "LIFE_SCIENCE": ProblemCategory.TECHNICAL,
    "EARTH_SYSTEM": ProblemCategory.TECHNICAL,
    "COSMOS_EXPLORATION": ProblemCategory.TECHNICAL,
    "SCALE_CROSSING": ProblemCategory.TECHNICAL,
    "DIMENSION": ProblemCategory.TECHNICAL,
    "SURVIVAL": ProblemCategory.TECHNICAL,
    "SCALE": ProblemCategory.TECHNICAL,
    
    # 审核监督类
    "REVIEW": ProblemCategory.REVIEW,
    "BALANCE": ProblemCategory.REVIEW,
    "ENVIRONMENT": ProblemCategory.REVIEW,
    "TIMING": ProblemCategory.REVIEW,
    "PATTERN": ProblemCategory.REVIEW,
    "STATE_CAPACITY": ProblemCategory.REVIEW,
    "INSTITUTIONAL_SEDIMENTATION": ProblemCategory.REVIEW,
    
    # 伦理道德类
    "ETHICAL": ProblemCategory.ETHICS,
    "MINDSET": ProblemCategory.ETHICS,
    "HARMONY": ProblemCategory.ETHICS,
    "INTEREST": ProblemCategory.ETHICS,
    "PUBLIC_INTEREST": ProblemCategory.ETHICS,
    "SEASONAL": ProblemCategory.ETHICS,
    "YINYANG": ProblemCategory.ETHICS,
    "CROSS_CULTURE": ProblemCategory.ETHICS,
    "RITUAL": ProblemCategory.ETHICS,
    "CULTURAL_CHANGE": ProblemCategory.ETHICS,

    # ── V1.0.1 精细优化: 学派子领域细分ProblemType ──
    "CONFUCIAN_SUB_SCHOOL": ProblemCategory.WISDOM,
    "DAOIST_SUB_SCHOOL": ProblemCategory.WISDOM,
    "BUDDHIST_SUB_SCHOOL": ProblemCategory.ETHICS,
    "MILITARY_SUB_SCHOOL": ProblemCategory.COMPETITION,
    "TALENT_PIPELINE": ProblemCategory.WISDOM,
    "ORGANIZATIONAL_CULTURE": ProblemCategory.WISDOM,
    "BRAND_CULTURE": ProblemCategory.MARKETING,
    "PHILOSOPHY_OF_MIND": ProblemCategory.ETHICS,
    "DECISION_FRAMEWORK": ProblemCategory.TECHNICAL,
    "RESOURCE_ECOLOGY": ProblemCategory.ANALYSIS,
    "INNOVATION_ECOLOGY": ProblemCategory.EXECUTION,
}


# ═══════════════════════════════════════════════════════════════
# 部门能力声明 - 每个部门声明自己能处理的问题类别及学派
# ═══════════════════════════════════════════════════════════════

@dataclass
class DepartmentCapability:
    """部门能力声明"""
    department: str              # 部门ID
    department_name: str         # 部门名称
    categories: Set[ProblemCategory]  # 能处理的问题类别
    primary_schools: Dict[ProblemCategory, List[Tuple[str, float]]]  # 各类别的首选学派
    secondary_schools: Dict[ProblemCategory, List[Tuple[str, float]]]  # 各类别的辅助学派
    description: str = ""


# 部门能力矩阵 - 按问题类别配置，而非按单个问题
DEPARTMENT_CAPABILITIES: Dict[str, DepartmentCapability] = {
    # ═══════════════════════════════════════════════════════════════
    # 吏部 - 能力层：智慧调度、选拔考核
    # ═══════════════════════════════════════════════════════════════
    "吏部": DepartmentCapability(
        department="LIBU",
        department_name="吏部",
        categories={
            ProblemCategory.STRATEGY,
            ProblemCategory.WISDOM,
            ProblemCategory.ETHICS,
        },
        primary_schools={
            ProblemCategory.STRATEGY: [
                ("儒家", 0.85),
                ("素书", 0.60),
                ("道家", 0.40),
            ],
            ProblemCategory.WISDOM: [
                ("素书", 0.90),
                ("儒家", 0.50),
                ("佛家", 0.30),
            ],
            ProblemCategory.ETHICS: [
                ("儒家", 0.90),
                ("素书", 0.50),
                ("佛家", 0.30),
            ],
        },
        secondary_schools={
            ProblemCategory.STRATEGY: [("法家", 0.3), ("兵家", 0.2)],
            ProblemCategory.WISDOM: [("道家", 0.3), ("阴阳家", 0.2)],
            ProblemCategory.ETHICS: [("道家", 0.3), ("法家", 0.2)],
        },
        description="智慧调度、学派注册、权重配置、融合决策",
    ),
    
    # ═══════════════════════════════════════════════════════════════
    # 礼部 - 记忆层：知识管理、学习系统
    # ═══════════════════════════════════════════════════════════════
    "礼部": DepartmentCapability(
        department="LIBU_LI",
        department_name="礼部",
        categories={
            ProblemCategory.NARRATIVE,
            ProblemCategory.WISDOM,
            ProblemCategory.ETHICS,
        },
        primary_schools={
            ProblemCategory.NARRATIVE: [
                ("文学叙事", 0.90),
                ("儒家", 0.40),
                ("道家", 0.30),
            ],
            ProblemCategory.WISDOM: [
                ("佛家", 0.85),
                ("儒家", 0.50),
                ("道家", 0.50),
            ],
            ProblemCategory.ETHICS: [
                ("佛家", 0.90),
                ("儒家", 0.60),
                ("道家", 0.30),
            ],
        },
        secondary_schools={
            ProblemCategory.NARRATIVE: [("神话智慧", 0.3), ("人类学", 0.2)],
            ProblemCategory.WISDOM: [("成长思维", 0.3), ("王阳明心学", 0.2)],
            ProblemCategory.ETHICS: [("人类学", 0.3), ("行为塑造", 0.2)],
        },
        description="记忆系统、学习系统、文学科举",
    ),
    
    # ═══════════════════════════════════════════════════════════════
    # 户部 - 数据层：经济分析、市场研究
    # ═══════════════════════════════════════════════════════════════
    "户部": DepartmentCapability(
        department="HUBU",
        department_name="户部",
        categories={
            ProblemCategory.ANALYSIS,
            ProblemCategory.MARKETING,
            ProblemCategory.COMPETITION,
        },
        primary_schools={
            ProblemCategory.ANALYSIS: [
                ("社会科学", 0.90),
                ("自然科学", 0.40),
                ("兵家", 0.30),
            ],
            ProblemCategory.MARKETING: [
                ("中国社会消费文化", 0.95),
                ("行为塑造", 0.85),
                ("社会科学", 0.80),
                ("文学叙事", 0.60),
                ("道家", 0.40),
            ],
            ProblemCategory.COMPETITION: [
                ("素书", 0.90),
                ("儒家", 0.50),
                ("道家", 0.40),
            ],
        },
        secondary_schools={
            ProblemCategory.ANALYSIS: [("经济学", 0.4), ("人类学", 0.3)],
            ProblemCategory.MARKETING: [("成长思维", 0.3), ("杜威反省思维", 0.2)],
            ProblemCategory.COMPETITION: [("法家", 0.3), ("兵家", 0.2)],
        },
        description="数据采集、知识图谱、行业知识、市场监控",
    ),
    
    # ═══════════════════════════════════════════════════════════════
    # 兵部 - 调度层：战略调度、神经网络
    # ═══════════════════════════════════════════════════════════════
    "兵部": DepartmentCapability(
        department="BINGBU",
        department_name="兵部",
        categories={
            ProblemCategory.COMPETITION,
            ProblemCategory.STRATEGY,
            ProblemCategory.CRISIS,
        },
        primary_schools={
            ProblemCategory.COMPETITION: [
                ("兵家", 0.90),
                ("道家", 0.50),
                ("素书", 0.40),
            ],
            ProblemCategory.STRATEGY: [
                ("道家", 0.85),
                ("儒家", 0.50),
                ("兵家", 0.40),
            ],
            ProblemCategory.CRISIS: [
                ("道家", 0.90),
                ("兵家", 0.50),
                ("佛家", 0.40),
            ],
        },
        secondary_schools={
            ProblemCategory.COMPETITION: [("法家", 0.3), ("纵横家", 0.2)],
            ProblemCategory.STRATEGY: [("素书", 0.3), ("术数时空", 0.2)],
            ProblemCategory.CRISIS: [("素书", 0.3), ("兵家", 0.2)],
        },
        description="主线调度、神经网络布局、信号传递",
    ),
    
    # ═══════════════════════════════════════════════════════════════
    # 刑部 - 监察层：风控安全、内容审核
    # ═══════════════════════════════════════════════════════════════
    "刑部": DepartmentCapability(
        department="XINGBU",
        department_name="刑部",
        categories={
            ProblemCategory.REVIEW,
            ProblemCategory.ETHICS,
            ProblemCategory.TECHNICAL,
        },
        primary_schools={
            ProblemCategory.REVIEW: [
                ("素书", 0.90),
                ("兵家", 0.50),
                ("道家", 0.40),
            ],
            ProblemCategory.ETHICS: [
                ("儒家", 0.90),
                ("素书", 0.50),
                ("佛家", 0.30),
            ],
            ProblemCategory.TECHNICAL: [
                ("科学思维", 0.90),
                ("儒家", 0.40),
                ("道家", 0.30),
            ],
        },
        secondary_schools={
            ProblemCategory.REVIEW: [("法家", 0.3), ("阴阳家", 0.2)],
            ProblemCategory.ETHICS: [("法家", 0.3), ("人类学", 0.2)],
            ProblemCategory.TECHNICAL: [("自然科学", 0.4), ("顶级思维法", 0.3)],
        },
        description="风控、安全合规、内容审核、情绪分析",
    ),
    
    # ═══════════════════════════════════════════════════════════════
    # 工部 - 执行层：核心执行、增长引擎
    # ═══════════════════════════════════════════════════════════════
    "工部": DepartmentCapability(
        department="GONGBU",
        department_name="工部",
        categories={
            ProblemCategory.EXECUTION,
            ProblemCategory.TECHNICAL,
            ProblemCategory.WISDOM,
        },
        primary_schools={
            ProblemCategory.EXECUTION: [
                ("成长思维", 0.90),
                ("素书", 0.50),
                ("儒家", 0.30),
            ],
            ProblemCategory.TECHNICAL: [
                ("科学思维", 0.90),
                ("兵家", 0.40),
                ("儒家", 0.30),
            ],
            ProblemCategory.WISDOM: [
                ("道家", 0.90),
                ("术数时空", 0.60),
                ("儒家", 0.40),
            ],
        },
        secondary_schools={
            ProblemCategory.EXECUTION: [("法家", 0.3), ("行为塑造", 0.2)],
            ProblemCategory.TECHNICAL: [("自然科学", 0.4), ("科幻思维", 0.3)],
            ProblemCategory.WISDOM: [("顶级思维法", 0.3), ("王阳明心学", 0.2)],
        },
        description="核心执行、增长引擎、工具链、方案评估",
    ),
    
    # ═══════════════════════════════════════════════════════════════
    # 厂卫 - 监控层：系统监控、效能评估
    # ═══════════════════════════════════════════════════════════════
    "厂卫": DepartmentCapability(
        department="CHANGWEI",
        department_name="厂卫",
        categories={
            ProblemCategory.REVIEW,
            ProblemCategory.CRISIS,
        },
        primary_schools={
            ProblemCategory.REVIEW: [
                ("道家", 0.95),
                ("术数时空", 0.70),
                ("儒家", 0.40),
            ],
            ProblemCategory.CRISIS: [
                ("术数时空", 0.95),
                ("道家", 0.55),
                ("儒家", 0.25),
            ],
        },
        secondary_schools={
            ProblemCategory.REVIEW: [("科学思维", 0.5), ("法家", 0.3)],
            ProblemCategory.CRISIS: [("兵家", 0.3), ("素书", 0.2)],
        },
        description="系统监控、性能优化、异常检测、安全审计",
    ),
    
    # ═══════════════════════════════════════════════════════════════
    # 五军都督府 - 神经网络层：网络布局、信号传递
    # ═══════════════════════════════════════════════════════════════
    "五军都督府": DepartmentCapability(
        department="WUJUN",
        department_name="五军都督府",
        categories={
            ProblemCategory.ANALYSIS,
            ProblemCategory.WISDOM,
        },
        primary_schools={
            ProblemCategory.ANALYSIS: [
                ("WCC智慧演化", 0.90),
                ("自然科学", 0.60),
                ("科幻思维", 0.40),
            ],
            ProblemCategory.WISDOM: [
                ("历史思想三维度", 0.95),
                ("WCC智慧演化", 0.70),
                ("科学思维", 0.60),
            ],
        },
        secondary_schools={
            ProblemCategory.ANALYSIS: [("文明演化", 0.5), ("文明经战", 0.3)],
            ProblemCategory.WISDOM: [("文明演化", 0.4), ("自然科学", 0.3)],
        },
        description="神经网络布局、信号传递、跨模块洞察",
    ),
    
    # ═══════════════════════════════════════════════════════════════
    # 翰林院 - 审核层：决策审核、逻辑论证
    # ═══════════════════════════════════════════════════════════════
    "翰林院": DepartmentCapability(
        department="HANLIN",
        department_name="翰林院",
        categories={
            ProblemCategory.REVIEW,
            ProblemCategory.ETHICS,
            ProblemCategory.TECHNICAL,
        },
        primary_schools={
            ProblemCategory.REVIEW: [
                ("法家", 0.95),
                ("素书", 0.60),
                ("儒家", 0.40),
            ],
            ProblemCategory.ETHICS: [
                ("儒家", 0.90),
                ("法家", 0.50),
                ("墨家", 0.40),
            ],
            ProblemCategory.TECHNICAL: [
                ("科学思维", 0.90),
                ("法家", 0.50),
                ("名家", 0.40),
            ],
        },
        secondary_schools={
            ProblemCategory.REVIEW: [("兵家", 0.3), ("纵横家", 0.2)],
            ProblemCategory.ETHICS: [("阴阳家", 0.3), ("佛家", 0.2)],
            ProblemCategory.TECHNICAL: [("行为塑造", 0.3), ("成长思维", 0.2)],
        },
        description="逻辑论证、多视角反驳、综合评审",
    ),
    
    # ═══════════════════════════════════════════════════════════════
    # 皇家藏书阁 - 独立记忆层
    # ═══════════════════════════════════════════════════════════════
    "皇家藏书阁": DepartmentCapability(
        department="CANGSHUGE",
        department_name="皇家藏书阁",
        categories=set(ProblemCategory),  # 接收所有类别
        primary_schools={
            ProblemCategory.STRATEGY: [("儒家", 0.8), ("道家", 0.7)],
            ProblemCategory.ANALYSIS: [("史学", 0.9), ("文明演化", 0.7)],
            ProblemCategory.WISDOM: [("儒道佛融合", 0.8), ("王阳明心学", 0.7)],
            ProblemCategory.NARRATIVE: [("文学叙事", 0.9), ("史学", 0.8)],
            ProblemCategory.EXECUTION: [("法家", 0.7), ("兵家", 0.6)],
            ProblemCategory.REVIEW: [("史学", 0.8), ("儒家", 0.7)],
            ProblemCategory.ETHICS: [("儒家", 0.9), ("佛家", 0.7)],
            ProblemCategory.TECHNICAL: [("自然科学", 0.8), ("科学思维", 0.7)],
            ProblemCategory.MARKETING: [("社会科学", 0.8), ("中国社会消费文化", 0.7)],
            ProblemCategory.COMPETITION: [("兵家", 0.8), ("法家", 0.6)],
            ProblemCategory.CRISIS: [("道家", 0.8), ("兵家", 0.6)],
        },
        secondary_schools={},
        description="独立记忆体系、记录一切有价值之记忆",
    ),
}


# ═══════════════════════════════════════════════════════════════
# 动态路由引擎
# ═══════════════════════════════════════════════════════════════

class DynamicDepartmentMatrix:
    """
    动态部门能力矩阵引擎
    根据问题类别动态确定最优部门组合
    """
    
    def __init__(self):
        self._capabilities = DEPARTMENT_CAPABILITIES
        self._category_dept_cache: Dict[ProblemCategory, List[Tuple[str, float]]] = {}
        self._build_category_index()
    
    def _build_category_index(self):
        """构建类别→部门索引"""
        for dept_id, cap in self._capabilities.items():
            for cat in cap.categories:
                if cat not in self._category_dept_cache:
                    self._category_dept_cache[cat] = []
                # 简单权重：主部门1.0，辅助部门0.5
                self._category_dept_cache[cat].append((dept_id, 1.0))
    
    def get_problem_category(self, problem_type: str) -> ProblemCategory:
        """获取问题类型对应的类别"""
        return PROBLEM_CATEGORY_MAP.get(problem_type, ProblemCategory.WISDOM)
    
    def get_departments_for_problem(
        self, 
        problem_type: str,
        include_secondary: bool = True
    ) -> List[Tuple[str, List[Tuple[str, float]], str]]:
        """
        根据问题类型获取最佳部门组合
        
        Returns:
            [(部门ID, [(学派, 权重)], 部门描述), ...]
        """
        category = self.get_problem_category(problem_type)
        
        results = []
        for dept_id, cap in self._capabilities.items():
            if category in cap.categories:
                # 合并主学派和辅助学派
                schools = cap.primary_schools.get(category, [])
                
                if include_secondary:
                    secondary = cap.secondary_schools.get(category, [])
                    # 辅助学派权重减半
                    secondary = [(s, w * 0.5) for s, w in secondary]
                    schools = schools + secondary
                
                if schools:
                    results.append((dept_id, schools, cap.description))
        
        # 按主学派权重排序
        results.sort(key=lambda x: sum(w for _, w in x[1]), reverse=True)
        
        return results
    
    def get_school_department_matrix(
        self, 
        category: ProblemCategory
    ) -> Dict[str, List[Tuple[str, float]]]:
        """获取某类别下所有部门的学派配置"""
        matrix = {}
        for dept_id, cap in self._capabilities.items():
            if category in cap.categories:
                schools = cap.primary_schools.get(category, [])
                if schools:
                    matrix[dept_id] = schools
        return matrix
    
    def get_all_categories(self) -> List[str]:
        """获取所有问题类别"""
        return [c.value for c in ProblemCategory]
    
    def get_department_categories(self, department: str) -> List[str]:
        """获取某部门能处理的所有类别"""
        cap = self._capabilities.get(department)
        if cap:
            return [c.value for c in cap.categories]
        return []
    
    def get_capability_summary(self) -> Dict:
        """获取能力矩阵摘要"""
        summary = {}
        for dept_id, cap in self._capabilities.items():
            summary[dept_id] = {
                "name": cap.department_name,
                "categories": [c.value for c in cap.categories],
                "category_count": len(cap.categories),
                "description": cap.description,
            }
        return summary


# 全局实例
_matrix_engine = None

def get_dynamic_matrix() -> DynamicDepartmentMatrix:
    """获取动态矩阵引擎实例"""
    global _matrix_engine
    if _matrix_engine is None:
        _matrix_engine = DynamicDepartmentMatrix()
    return _matrix_engine


# ═══════════════════════════════════════════════════════════════
# 兼容层：与现有V4接口兼容
# ═══════════════════════════════════════════════════════════════

def resolve_department_by_category(
    problem_type: str,
    include_secondary: bool = True
) -> List[Tuple[str, List[Tuple[str, float]], str]]:
    """
    V1.0新增：按问题类别解析部门
    替代原有的按ProblemType逐个配置的方式
    """
    engine = get_dynamic_matrix()
    return engine.get_departments_for_problem(problem_type, include_secondary)


def get_category_for_problem(problem_type: str) -> str:
    """获取问题类型对应的问题类别"""
    engine = get_dynamic_matrix()
    category = engine.get_problem_category(problem_type)
    return category.value