# -*- coding: utf-8 -*-
"""
三核联动整合器 v1.0.0
Three-Core Integration Engine
================================

整合"统一研究体系"(脑) + "神之架构V5"(躯) + "贤者系统"(魂)

核心理念: "研究为源·调度为脉·智慧为魂"

架构文档: file/系统文件/三核联动架构文档_v1.0.md

版本: v1.0.0
日期: 2026-04-23
"""

import logging
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# 第一部分：研究体系枚举与数据结构 (核心脑)
# ═══════════════════════════════════════════════════════════════════════════════

class ResearchLevel(Enum):
    """研究层级 L1-L4"""
    L1_QUANTITATIVE = "L1_定量研究"      # 大规模、可量化、统计推断
    L2_QUALITATIVE = "L2_定性研究"       # 深度、探索性、理解动机
    L3_DIGITAL = "L3_数字化工具"          # 实时、全量、自动化
    L4_NEURO = "L4_神经科学"             # 潜意识、生理指标、直接测量

class ResearchDepth(Enum):
    """研究深度 D0-D5"""
    D0_SCAN = "D0_快速扫描"              # 5-30分钟, 1-3个信息源
    D1_BASIC = "D1_基础研究"             # 1-4小时, 3-8个信息源
    D2_STANDARD = "D2_标准研究"          # 4-16小时, 8-20个信息源
    D3_DEEP = "D3_深入研究"             # 1-3天, 20-50个信息源
    D4_DOCTORAL = "D4_博士研究"          # 3-7天, 50-200个信息源
    D5_ARGUMENT = "D5_论证研究"          # 3-14天, 100-500+个信息源

class ResearchDimension(Enum):
    """研究维度 A-E"""
    A_EMOTION_TRIGGER = "A_情绪触发与波动机制"
    B_EMOTION_TYPE = "B_情绪类型与消费行为关联"
    C_VALUE_PERCEPTION = "C_情绪价值感知维度_心价比"
    D_SENSING_DECISION = "D_感性决策关键维度"
    E_AI_EMOTION = "E_AI时代情绪计算与智能决策"

class ResearchDirection(Enum):
    """研究方向 1-6"""
    DIR1_CONSUMER_EMOTION = "①消费情绪"
    DIR2_SENSING_DECISION = "②感性决策"
    DIR3_RESEARCH_METHOD = "③研究方法"
    DIR4_APPLICATION = "④落地应用"
    DIR5_RISK_CONTROL = "⑤风险管控"
    DIR6_NEUROSCIENCE = "⑥神经科学"

class ComplexityLevel(Enum):
    """复杂度等级"""
    SIMPLE = "SIMPLE"           # 1部门, 1主线
    MODERATE = "MODERATE"       # 3部门, 2主线
    COMPLEX = "COMPLEX"         # 5部门, 4主线
    CRITICAL = "CRITICAL"       # 99部门, 7主线

# ═══════════════════════════════════════════════════════════════════════════════
# 第二部分：神之架构枚举与数据结构 (核心躯)
# ═══════════════════════════════════════════════════════════════════════════════

class MainLine(Enum):
    """7条主线"""
    IMPERIAL = "皇家主线"         # 最高决策, 七人代表大会
    CIVIL_ADMIN = "文治主线"       # 智慧中枢, 内阁/吏部/礼部
    ECONOMIC = "经济主线"         # 数据支撑, 户部/市易司
    MILITARY = "军政主线"         # 执行调度, 兵部/锦衣卫
    STANDARD = "标准主线"         # 执行落地, 刑部/工部/三法司
    INNOVATION = "创新主线"        # 增长引擎, 科学院/经济战略司
    AUDIT = "审核主线"            # 质量保障, 翰林院/藏书阁

class CrossLineSyncType(Enum):
    """跨线协同类型"""
    PARALLEL = "PARALLEL"        # 并行协同
    SEQUENTIAL = "SEQUENTIAL"    # 串联协同
    FEEDBACK = "FEEDBACK"        # 反馈协同
    HYBRID = "HYBRID"            # 混合协同

class DecisionSystem(Enum):
    """决策制"""
    DICTATORSHIP = "独裁制"       # 1人决策
    COLLEGIAL = "共议制"         # 3人共议
    DUAL = "双人制"             # 2人决策
    INDEPENDENT_AUDIT = "独立审核"  # 翰林院独立
    COUNCIL = "代表大会制"        # 7人投票4票通过

# ═══════════════════════════════════════════════════════════════════════════════
# 第三部分：贤者系统枚举与数据结构 (核心魂)
# ═══════════════════════════════════════════════════════════════════════════════

class SagePhase(Enum):
    """贤者工程五层链路"""
    PHASE0_DOC = "Phase0_深度学习文档"     # D4-D5级
    PHASE1_DISTILL = "Phase1_蒸馏文档"      # D3级
    PHASE2_CODE = "Phase2_智慧编码"        # D2级
    PHASE3_CLONE = "Phase3_克隆实现"       # D1-D2级
    PHASE4_CLAW = "Phase4_Claw子系统"     # D0-D1级

# ═══════════════════════════════════════════════════════════════════════════════
# 第四部分：三核联动数据结构
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ResearchPlan:
    """研究计划 (核心脑输出)"""
    level: ResearchLevel
    depth: ResearchDepth
    dimensions: List[ResearchDimension]
    directions: List[ResearchDirection]
    cross_points: List[Tuple[ResearchDimension, ResearchDirection]]  # 交叉研究点
    ice_score: float = 0.0
    priority: str = "P2"
    estimated_hours: float = 0.0

@dataclass
class DispatchAllocation:
    """调度分配 (核心躯输出)"""
    main_line: MainLine
    secondary_lines: List[MainLine]
    cross_sync_type: CrossLineSyncType
    departments: List[str]
    positions: List[Dict[str, Any]]
    decision_system: DecisionSystem
    complexity: ComplexityLevel

@dataclass
class WisdomInjection:
    """智慧注入 (核心魂输出)"""
    schools: List[str]  # WisdomSchool列表
    claws: List[Dict[str, Any]]  # Claw配置列表
    phase_chain: SagePhase
    sage_representatives: List[str]  # 代表贤者

@dataclass
class ThreeCoreResult:
    """三核联动结果"""
    timestamp: datetime
    research_plan: ResearchPlan
    dispatch_allocation: DispatchAllocation
    wisdom_injection: WisdomInjection
    fusion_decision: Dict[str, Any]
    feedback_loop: Dict[str, Any]

# ═══════════════════════════════════════════════════════════════════════════════
# 第五部分：映射矩阵
# ═══════════════════════════════════════════════════════════════════════════════

# 研究层级 × 主线选择矩阵
RESEARCH_LEVEL_MAINLINE_MATRIX: Dict[ResearchLevel, Tuple[List[MainLine], ComplexityLevel]] = {
    ResearchLevel.L1_QUANTITATIVE: ([MainLine.ECONOMIC, MainLine.MILITARY], ComplexityLevel.SIMPLE),
    ResearchLevel.L2_QUALITATIVE: ([MainLine.CIVIL_ADMIN, MainLine.INNOVATION], ComplexityLevel.MODERATE),
    ResearchLevel.L3_DIGITAL: ([MainLine.ECONOMIC, MainLine.STANDARD], ComplexityLevel.SIMPLE),
    ResearchLevel.L4_NEURO: ([MainLine.INNOVATION, MainLine.IMPERIAL], ComplexityLevel.COMPLEX),
}

# 研究深度 × SagePhase链路映射
DEPTH_PHASE_MATRIX: Dict[ResearchDepth, SagePhase] = {
    ResearchDepth.D0_SCAN: SagePhase.PHASE4_CLAW,
    ResearchDepth.D1_BASIC: SagePhase.PHASE4_CLAW,
    ResearchDepth.D2_STANDARD: SagePhase.PHASE3_CLONE,
    ResearchDepth.D3_DEEP: SagePhase.PHASE2_CODE,
    ResearchDepth.D4_DOCTORAL: SagePhase.PHASE1_DISTILL,
    ResearchDepth.D5_ARGUMENT: SagePhase.PHASE0_DOC,
}

# 维度 × WisdomSchool映射
DIMENSION_SCHOOL_MATRIX: Dict[ResearchDimension, List[str]] = {
    ResearchDimension.A_EMOTION_TRIGGER: ["DAO_WISDOM", "BUDDHIST", "MILITARY"],
    ResearchDimension.B_EMOTION_TYPE: ["CONFUCIAN", "BEHAVIOR", "SOCIAL_SCIENCE"],
    ResearchDimension.C_VALUE_PERCEPTION: ["CONFUCIAN", "ECONOMIC", "MILITARY"],
    ResearchDimension.D_SENSING_DECISION: ["GROWTH", "DEWEY", "TOP_METHODS"],
    ResearchDimension.E_AI_EMOTION: ["SCIENCE", "NATURAL_SCIENCE", "WCC"],
}

# 七贤 × 主线映射
SAGE_MAINLINE_MATRIX: Dict[str, Tuple[MainLine, float]] = {
    "孔子": (MainLine.IMPERIAL, 1.0),
    "管仲": (MainLine.ECONOMIC, 0.9),
    "韦伯": (MainLine.CIVIL_ADMIN, 0.85),
    "德鲁克": (MainLine.STANDARD, 0.85),
    "孟子": (MainLine.IMPERIAL, 0.95),
    "张衡": (MainLine.INNOVATION, 0.8),
    "范蠡": (MainLine.MILITARY, 0.75),
}

# 主线 × 复杂度 × 决策制映射
MAINLINE_COMPLEXITY_MATRIX: Dict[Tuple[MainLine, ComplexityLevel], DecisionSystem] = {
    (MainLine.IMPERIAL, ComplexityLevel.CRITICAL): DecisionSystem.COUNCIL,
    (MainLine.IMPERIAL, ComplexityLevel.COMPLEX): DecisionSystem.COUNCIL,
    (MainLine.ECONOMIC, ComplexityLevel.MODERATE): DecisionSystem.COLLEGIAL,
    (MainLine.CIVIL_ADMIN, ComplexityLevel.MODERATE): DecisionSystem.COLLEGIAL,
    (MainLine.INNOVATION, ComplexityLevel.MODERATE): DecisionSystem.DUAL,
    (MainLine.STANDARD, ComplexityLevel.SIMPLE): DecisionSystem.DUAL,
    (MainLine.MILITARY, ComplexityLevel.SIMPLE): DecisionSystem.DICTATORSHIP,
}

# 跨线协同类型映射
CROSS_SYNC_MATRIX: Dict[Tuple[int, ComplexityLevel], CrossLineSyncType] = {
    (1, ComplexityLevel.SIMPLE): CrossLineSyncType.PARALLEL,
    (2, ComplexityLevel.MODERATE): CrossLineSyncType.SEQUENTIAL,
    (3, ComplexityLevel.COMPLEX): CrossLineSyncType.HYBRID,
    (7, ComplexityLevel.CRITICAL): CrossLineSyncType.HYBRID,
}

# ═══════════════════════════════════════════════════════════════════════════════
# 第六部分：三核联动整合器
# ═══════════════════════════════════════════════════════════════════════════════

class ThreeCoreIntegration:
    """
    三核联动整合器
    
    整合统一研究体系(脑) + 神之架构V5(躯) + 贤者系统(魂)
    
    使用方法:
        integration = ThreeCoreIntegration()
        
        # 方式1: 完整三核联动
        result = integration.three_core_dispatch(user_input, context)
        
        # 方式2: 分步执行
        research_plan = integration.parse_research_depth(query)
        dispatch = integration.allocate_positions(research_plan)
        wisdom = integration.inject_wisdom(dispatch)
        fusion = integration.fuse_results(research_plan, dispatch, wisdom)
    """
    
    def __init__(self):
        self._initialized = False
        logger.info("ThreeCoreIntegration initialized (lazy)")
    
    def _ensure_init(self):
        """延迟初始化"""
        if not self._initialized:
            self._load_mapping_matrices()
            self._initialized = True
    
    def _load_mapping_matrices(self):
        """加载映射矩阵"""
        # 懒加载: 仅在实际需要时加载WisdomSchool等枚举
        try:
            # 使用绝对导入
            from src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums import WisdomSchool
            from src.intelligence.dispatcher.wisdom_dispatch._dispatch_court import Department
            self._WisdomSchool = WisdomSchool
            self._Department = Department
            logger.info("Mapping matrices loaded successfully")
        except ImportError as e:
            logger.warning(f"Could not load dispatch enums: {e}")
            # 使用内置枚举作为fallback
            self._WisdomSchool = None
            self._Department = None
    
    # ═══════════════════════════════════════════════════════════════════════
    # 核心脑接口: 研究体系
    # ═══════════════════════════════════════════════════════════════════════
    
    def parse_research_depth(self, query: str, context: Optional[Dict] = None) -> ResearchPlan:
        """
        解析研究层级与深度
        
        Args:
            query: 用户查询
            context: 可选上下文信息
            
        Returns:
            ResearchPlan: 研究计划
        """
        self._ensure_init()
        
        # 关键词识别 → 研究层级
        level = self._infer_research_level(query)
        
        # 复杂度分析 → 研究深度
        depth = self._infer_research_depth(query, level)
        
        # 研究维度识别
        dimensions = self._extract_dimensions(query)
        
        # 研究方向识别
        directions = self._extract_directions(query)
        
        # 生成交叉研究点
        cross_points = self._generate_cross_points(dimensions, directions)
        
        # 计算ICE评分
        ice_score = self._calculate_ice_score(cross_points)
        
        # 确定优先级
        priority = self._determine_priority(ice_score)
        
        # 估算耗时
        estimated_hours = self._estimate_hours(depth)
        
        return ResearchPlan(
            level=level,
            depth=depth,
            dimensions=dimensions,
            directions=directions,
            cross_points=cross_points,
            ice_score=ice_score,
            priority=priority,
            estimated_hours=estimated_hours,
        )
    
    def _infer_research_level(self, query: str) -> ResearchLevel:
        """根据查询推断研究层级"""
        query_lower = query.lower()
        
        if any(k in query_lower for k in ['多少', '比例', '趋势', '统计', '数据', '量化']):
            return ResearchLevel.L1_QUANTITATIVE
        elif any(k in query_lower for k in ['为什么', '怎么想', '感受', '动机', '理解']):
            return ResearchLevel.L2_QUALITATIVE
        elif any(k in query_lower for k in ['实时', '预测', '监控', '自动化']):
            return ResearchLevel.L3_DIGITAL
        elif any(k in query_lower for k in ['本能', '潜意识', '生理', '神经']):
            return ResearchLevel.L4_NEURO
        
        return ResearchLevel.L2_QUALITATIVE  # 默认定性研究
    
    def _infer_research_depth(self, query: str, level: ResearchLevel) -> ResearchDepth:
        """根据查询和层级推断研究深度"""
        query_lower = query.lower()
        
        if any(k in query_lower for k in ['快速', '简单', '概要', '大概']):
            return ResearchDepth.D0_SCAN
        elif any(k in query_lower for k in ['深入', '详细', '全面', '系统']):
            return ResearchDepth.D3_DEEP
        elif any(k in query_lower for k in ['博士', '学术', '论证', '论文']):
            return ResearchDepth.D4_DOCTORAL
        
        # 根据层级默认
        depth_defaults = {
            ResearchLevel.L1_QUANTITATIVE: ResearchDepth.D1_BASIC,
            ResearchLevel.L2_QUALITATIVE: ResearchDepth.D2_STANDARD,
            ResearchLevel.L3_DIGITAL: ResearchDepth.D1_BASIC,
            ResearchLevel.L4_NEURO: ResearchDepth.D4_DOCTORAL,
        }
        return depth_defaults.get(level, ResearchDepth.D2_STANDARD)
    
    def _extract_dimensions(self, query: str) -> List[ResearchDimension]:
        """提取研究维度"""
        query_lower = query.lower()
        dimensions = []
        
        if any(k in query_lower for k in ['情绪', '情感', '触发', '波动']):
            dimensions.append(ResearchDimension.A_EMOTION_TRIGGER)
        if any(k in query_lower for k in ['行为', '消费', '类型', '关联']):
            dimensions.append(ResearchDimension.B_EMOTION_TYPE)
        if any(k in query_lower for k in ['价值', '价格', '性价比', '心价']):
            dimensions.append(ResearchDimension.C_VALUE_PERCEPTION)
        if any(k in query_lower for k in ['决策', '判断', '选择', '感性']):
            dimensions.append(ResearchDimension.D_SENSING_DECISION)
        if any(k in query_lower for k in ['ai', '人工智能', '智能', '算法']):
            dimensions.append(ResearchDimension.E_AI_EMOTION)
        
        return dimensions if dimensions else [ResearchDimension.D_SENSING_DECISION]
    
    def _extract_directions(self, query: str) -> List[ResearchDirection]:
        """提取研究方向"""
        query_lower = query.lower()
        directions = []
        
        if any(k in query_lower for k in ['营销', '品牌', '消费者', '市场']):
            directions.append(ResearchDirection.DIR1_CONSUMER_EMOTION)
        if any(k in query_lower for k in ['决策', '判断', '选择']):
            directions.append(ResearchDirection.DIR2_SENSING_DECISION)
        if any(k in query_lower for k in ['方法', '研究', '分析']):
            directions.append(ResearchDirection.DIR3_RESEARCH_METHOD)
        if any(k in query_lower for k in ['落地', '应用', '执行', '实施']):
            directions.append(ResearchDirection.DIR4_APPLICATION)
        if any(k in query_lower for k in ['风险', '管控', '安全', '合规']):
            directions.append(ResearchDirection.DIR5_RISK_CONTROL)
        if any(k in query_lower for k in ['神经', '科学', '实验', '生理']):
            directions.append(ResearchDirection.DIR6_NEUROSCIENCE)
        
        return directions if directions else [ResearchDirection.DIR2_SENSING_DECISION]
    
    def _generate_cross_points(
        self, 
        dimensions: List[ResearchDimension], 
        directions: List[ResearchDirection]
    ) -> List[Tuple[ResearchDimension, ResearchDirection]]:
        """生成交叉研究点"""
        cross_points = []
        for dim in dimensions:
            for dir in directions:
                cross_points.append((dim, dir))
        return cross_points
    
    def _calculate_ice_score(self, cross_points: List[Tuple]) -> float:
        """计算ICE评分 (Impact40% + Confidence30% + Ease30%)"""
        # 简化实现: 基于交叉点数量和质量
        base_score = min(len(cross_points) * 0.5, 5.0)  # 最多5分
        confidence = 7.0  # 默认置信度
        ease = 6.0  # 默认难易度
        
        ice_score = 0.4 * base_score + 0.3 * confidence + 0.3 * ease
        return round(ice_score, 1)
    
    def _determine_priority(self, ice_score: float) -> str:
        """根据ICE评分确定优先级"""
        if ice_score >= 8.0:
            return "P0"
        elif ice_score >= 6.0:
            return "P1"
        elif ice_score >= 4.0:
            return "P2"
        elif ice_score >= 2.0:
            return "P3"
        else:
            return "P4"
    
    def _estimate_hours(self, depth: ResearchDepth) -> float:
        """估算研究耗时"""
        hour_map = {
            ResearchDepth.D0_SCAN: 0.5,
            ResearchDepth.D1_BASIC: 2.0,
            ResearchDepth.D2_STANDARD: 8.0,
            ResearchDepth.D3_DEEP: 24.0,
            ResearchDepth.D4_DOCTORAL: 72.0,
            ResearchDepth.D5_ARGUMENT: 120.0,
        }
        return hour_map.get(depth, 8.0)
    
    # ═══════════════════════════════════════════════════════════════════════
    # 核心躯接口: 神之架构调度
    # ═══════════════════════════════════════════════════════════════════════
    
    def select_main_lines(self, complexity: ComplexityLevel, context: Optional[Dict] = None) -> Tuple[List[MainLine], CrossLineSyncType]:
        """
        根据复杂度选择主线
        
        Returns:
            (主线条列表, 跨线协同类型)
        """
        complexity_value = {
            ComplexityLevel.SIMPLE: 1,
            ComplexityLevel.MODERATE: 2,
            ComplexityLevel.COMPLEX: 3,
            ComplexityLevel.CRITICAL: 7,
        }.get(complexity, 1)
        
        sync_type = CROSS_SYNC_MATRIX.get((complexity_value, complexity), CrossLineSyncType.PARALLEL)
        
        # 选择主线
        if complexity == ComplexityLevel.SIMPLE:
            main_lines = [MainLine.ECONOMIC]
        elif complexity == ComplexityLevel.MODERATE:
            main_lines = [MainLine.ECONOMIC, MainLine.CIVIL_ADMIN]
        elif complexity == ComplexityLevel.COMPLEX:
            main_lines = [MainLine.IMPERIAL, MainLine.CIVIL_ADMIN, MainLine.ECONOMIC, MainLine.INNOVATION]
        else:  # CRITICAL
            main_lines = list(MainLine)
        
        return main_lines, sync_type
    
    def allocate_positions(
        self, 
        research_plan: ResearchPlan,
        main_lines: List[MainLine]
    ) -> DispatchAllocation:
        """
        策略→岗位分配
        
        Args:
            research_plan: 研究计划 (核心脑输出)
            main_lines: 选定的主线
            
        Returns:
            DispatchAllocation: 调度分配
        """
        # 确定复杂度
        complexity = self._level_to_complexity(research_plan.level)
        
        # 主导主线
        primary_line = main_lines[0] if main_lines else MainLine.ECONOMIC
        
        # 协同主线
        secondary_lines = main_lines[1:] if len(main_lines) > 1 else []
        
        # 确定跨线协同类型
        _, sync_type = self.select_main_lines(complexity)
        
        # 部门分配
        departments = self._lines_to_departments(main_lines)
        
        # 岗位分配
        positions = self._allocate_positions_for_departments(departments, complexity)
        
        # 决策制
        decision_system = self._get_decision_system(primary_line, complexity)
        
        return DispatchAllocation(
            main_line=primary_line,
            secondary_lines=secondary_lines,
            cross_sync_type=sync_type,
            departments=departments,
            positions=positions,
            decision_system=decision_system,
            complexity=complexity,
        )
    
    def _level_to_complexity(self, level: ResearchLevel) -> ComplexityLevel:
        """研究层级 → 复杂度"""
        mapping = {
            ResearchLevel.L1_QUANTITATIVE: ComplexityLevel.SIMPLE,
            ResearchLevel.L2_QUALITATIVE: ComplexityLevel.MODERATE,
            ResearchLevel.L3_DIGITAL: ComplexityLevel.SIMPLE,
            ResearchLevel.L4_NEURO: ComplexityLevel.COMPLEX,
        }
        return mapping.get(level, ComplexityLevel.MODERATE)
    
    def _lines_to_departments(self, lines: List[MainLine]) -> List[str]:
        """主线 → 部门"""
        line_dept_map = {
            MainLine.IMPERIAL: ["皇家系统", "七人代表大会"],
            MainLine.CIVIL_ADMIN: ["内阁", "吏部", "礼部"],
            MainLine.ECONOMIC: ["户部", "市易司", "盐铁司"],
            MainLine.MILITARY: ["兵部", "锦衣卫", "五军都督府"],
            MainLine.STANDARD: ["刑部", "工部", "三法司"],
            MainLine.INNOVATION: ["皇家科学院", "经济战略司"],
            MainLine.AUDIT: ["翰林院", "皇家藏书阁"],
        }
        departments = []
        for line in lines:
            departments.extend(line_dept_map.get(line, []))
        return departments
    
    def _allocate_positions_for_departments(
        self, 
        departments: List[str], 
        complexity: ComplexityLevel
    ) -> List[Dict[str, Any]]:
        """为部门分配岗位"""
        positions = []
        for dept in departments[:5]:  # 最多5个部门
            positions.append({
                "department": dept,
                "level": "executive",
                "authority": 0.8,
            })
        return positions
    
    def _get_decision_system(self, line: MainLine, complexity: ComplexityLevel) -> DecisionSystem:
        """获取决策制"""
        return MAINLINE_COMPLEXITY_MATRIX.get((line, complexity), DecisionSystem.COLLEGIAL)
    
    # ═══════════════════════════════════════════════════════════════════════
    # 核心魂接口: 贤者系统
    # ═══════════════════════════════════════════════════════════════════════
    
    def match_wisdom_schools(self, dimensions: List[ResearchDimension]) -> List[str]:
        """
        研究维度 → 学派匹配
        
        Returns:
            WisdomSchool列表
        """
        schools = []
        for dim in dimensions:
            schools.extend(DIMENSION_SCHOOL_MATRIX.get(dim, []))
        return list(set(schools))  # 去重
    
    def invoke_phase_chain(self, depth: ResearchDepth) -> SagePhase:
        """
        获取对应深度的五层链路阶段
        
        Returns:
            SagePhase: 链路阶段
        """
        return DEPTH_PHASE_MATRIX.get(depth, SagePhase.PHASE3_CLONE)
    
    def inject_wisdom(
        self, 
        dispatch: DispatchAllocation,
        research_plan: ResearchPlan
    ) -> WisdomInjection:
        """
        智慧注入
        
        Args:
            dispatch: 调度分配 (核心躯输出)
            research_plan: 研究计划 (核心脑输出)
            
        Returns:
            WisdomInjection: 智慧注入
        """
        # 学派匹配
        schools = self.match_wisdom_schools(research_plan.dimensions)
        
        # Claw配置
        claws = self._generate_claw_configs(dispatch, schools)
        
        # 五层链路
        phase_chain = self.invoke_phase_chain(research_plan.depth)
        
        # 代表贤者
        sage_representatives = self._select_sage_representatives(dispatch.main_line)
        
        return WisdomInjection(
            schools=schools,
            claws=claws,
            phase_chain=phase_chain,
            sage_representatives=sage_representatives,
        )
    
    def _generate_claw_configs(
        self, 
        dispatch: DispatchAllocation,
        schools: List[str]
    ) -> List[Dict[str, Any]]:
        """生成Claw配置"""
        claws = []
        for school in schools[:5]:  # 最多5个学派
            claws.append({
                "school": school,
                "activation": "auto",
                "priority": "P1",
            })
        return claws
    
    def _select_sage_representatives(self, main_line: MainLine) -> List[str]:
        """选择代表贤者"""
        line_sages = {
            MainLine.IMPERIAL: ["孔子", "孟子"],
            MainLine.CIVIL_ADMIN: ["郑玄", "刘向"],
            MainLine.ECONOMIC: ["管仲", "桑弘羊"],
            MainLine.MILITARY: ["孙武", "孙膑"],
            MainLine.STANDARD: ["商鞅", "韩非"],
            MainLine.INNOVATION: ["张衡", "沈括"],
            MainLine.AUDIT: ["墨子", "荀子"],
        }
        return line_sages.get(main_line, ["孔子"])
    
    # ═══════════════════════════════════════════════════════════════════════
    # 三核融合接口
    # ═══════════════════════════════════════════════════════════════════════
    
    def three_core_dispatch(
        self, 
        user_input: str, 
        context: Optional[Dict] = None
    ) -> ThreeCoreResult:
        """
        三核联动调度主方法
        
        完整流程: 研究体系(脑) → 神之架构(躯) → 贤者系统(魂) → 融合执行
        
        Args:
            user_input: 用户输入
            context: 可选上下文
            
        Returns:
            ThreeCoreResult: 三核联动结果
        """
        self._ensure_init()
        context = context or {}
        
        # 第一步: 核心脑·研究体系解析
        research_plan = self.parse_research_depth(user_input, context)
        
        # 第二步: 核心躯·神之架构调度
        complexity = self._level_to_complexity(research_plan.level)
        main_lines, sync_type = self.select_main_lines(complexity, context)
        dispatch = self.allocate_positions(research_plan, main_lines)
        
        # 第三步: 核心魂·贤者系统注入
        wisdom = self.inject_wisdom(dispatch, research_plan)
        
        # 第四步: 融合执行
        fusion_decision = self.fuse_results(research_plan, dispatch, wisdom)
        
        # 第五步: 反馈闭环
        feedback_loop = self._build_feedback_loop(fusion_decision)
        
        return ThreeCoreResult(
            timestamp=datetime.now(),
            research_plan=research_plan,
            dispatch_allocation=dispatch,
            wisdom_injection=wisdom,
            fusion_decision=fusion_decision,
            feedback_loop=feedback_loop,
        )
    
    def fuse_results(
        self,
        research_plan: ResearchPlan,
        dispatch: DispatchAllocation,
        wisdom: WisdomInjection
    ) -> Dict[str, Any]:
        """
        融合三核输出
        
        Returns:
            融合决策结果
        """
        return {
            "summary": {
                "research_level": research_plan.level.value,
                "research_depth": research_plan.depth.value,
                "main_line": dispatch.main_line.value,
                "primary_school": wisdom.schools[0] if wisdom.schools else "UNKNOWN",
                "ice_score": research_plan.ice_score,
                "priority": research_plan.priority,
            },
            "research_plan": {
                "dimensions": [d.value for d in research_plan.dimensions],
                "directions": [d.value for d in research_plan.directions],
                "cross_points_count": len(research_plan.cross_points),
                "estimated_hours": research_plan.estimated_hours,
            },
            "dispatch": {
                "main_line": dispatch.main_line.value,
                "secondary_lines": [l.value for l in dispatch.secondary_lines],
                "cross_sync": dispatch.cross_sync_type.value,
                "departments": dispatch.departments,
                "decision_system": dispatch.decision_system.value,
                "complexity": dispatch.complexity.value,
            },
            "wisdom": {
                "schools": wisdom.schools,
                "phase": wisdom.phase_chain.value,
                "sages": wisdom.sage_representatives,
                "claw_count": len(wisdom.claws),
            },
        }
    
    def _build_feedback_loop(self, fusion_result: Dict) -> Dict[str, Any]:
        """构建反馈闭环"""
        return {
            "track_metrics": ["ROI", "转化率", "满意度"],
            "audit_system": "翰林院",
            "council_approval": "七人代表大会",
            "optimization_signal": "基于执行结果动态调整",
        }

# ═══════════════════════════════════════════════════════════════════════════════
# 第七部分：全局单例
# ═══════════════════════════════════════════════════════════════════════════════

_three_core_integration: Optional[ThreeCoreIntegration] = None

def get_three_core_integration() -> ThreeCoreIntegration:
    """获取三核联动整合器全局单例"""
    global _three_core_integration
    if _three_core_integration is None:
        _three_core_integration = ThreeCoreIntegration()
    return _three_core_integration
