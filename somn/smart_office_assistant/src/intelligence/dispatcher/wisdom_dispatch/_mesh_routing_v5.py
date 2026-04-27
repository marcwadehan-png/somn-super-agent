"""
神之架构 V1.0.0 - 网状串联调度层
_optimization_v5.py

核心升级理念："主线网状串联，动态协同调度"
- 打破部门壁垒，实现跨部门网状协同
- 7条主线横向贯通，形成真正的智能调度网络
- 动态路由算法，根据问题特征自动构建最优调度路径

版本: 5.0.0
日期: 2026-04-22
基于: V1.0.0
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import time


class MainLine(Enum):
    """神之架构7条主线（V5新增网状串联层）"""
    ROYAL = "皇家主线"           # 决策中枢：太师+太傅+太保
    WENZHI = "文治主线"          # 智慧中枢：内阁+吏部+礼部
    ECONOMY = "经济主线"         # 数据中枢：户部+市易司+盐铁司
    MILITARY = "军政主线"        # 调度中枢：兵部+五军都督府+锦衣卫
    STANDARD = "标准主线"        # 执行中枢：刑部+工部+三法司
    INNOVATION = "创新主线"      # 增长中枢：皇家科学院+经济战略司+文化输出局
    REVIEW = "审核主线"          # 质量中枢：翰林院+藏书阁


class CrossLineType(Enum):
    """跨线协同类型"""
    PARALLEL = "并行协同"        # 多线同时处理不同子任务
    SEQUENTIAL = "串联协同"       # 上一线输出作为下一线输入
    FEEDBACK = "反馈协同"         # 结果反馈影响调度策略
    HYBRID = "混合协同"          # 并行+串联组合


@dataclass
class CrossLineEdge:
    """跨线协同边（两个主线之间的协同关系）"""
    source: MainLine
    target: MainLine
    sync_type: CrossLineType
    trigger: str              # 什么情况下触发此协同
    weight: float = 0.5       # 协同强度系数


@dataclass
class RoutingNode:
    """动态路由节点"""
    line: MainLine
    department: str
    position_id: str
    sage: str
    schools: List[Tuple[str, float]]  # (学派, 权重)
    authority: float = 1.0
    is_primary: bool = True


@dataclass
class DynamicRoutingPath:
    """动态构建的调度路径"""
    problem_type: str
    path_id: str
    nodes: List[RoutingNode]
    cross_lines: List[Tuple[MainLine, MainLine, CrossLineType]]
    total_weight: float
    estimated_complexity: float


# ═══════════════════════════════════════════════════════════════
# V5 核心：主线网状串联矩阵
# ═══════════════════════════════════════════════════════════════

# 7条主线之间的协同关系矩阵
MAIN_LINE_MATRIX: Dict[MainLine, Dict[MainLine, CrossLineEdge]] = {
    # 皇家主线：协调所有其他主线
    MainLine.ROYAL: {
        MainLine.WENZHI: CrossLineEdge(
            MainLine.ROYAL, MainLine.WENZHI, 
            CrossLineType.SEQUENTIAL,
            "战略决策→智慧调度",
            0.95
        ),
        MainLine.ECONOMY: CrossLineEdge(
            MainLine.ROYAL, MainLine.ECONOMY,
            CrossLineType.SEQUENTIAL,
            "资源调配→经济执行",
            0.90
        ),
        MainLine.MILITARY: CrossLineEdge(
            MainLine.ROYAL, MainLine.MILITARY,
            CrossLineType.SEQUENTIAL,
            "危机响应→军事调度",
            0.95
        ),
        MainLine.STANDARD: CrossLineEdge(
            MainLine.ROYAL, MainLine.STANDARD,
            CrossLineType.SEQUENTIAL,
            "决策→执行",
            0.85
        ),
        MainLine.INNOVATION: CrossLineEdge(
            MainLine.ROYAL, MainLine.INNOVATION,
            CrossLineType.PARALLEL,
            "战略方向←创新建议",
            0.80
        ),
        MainLine.REVIEW: CrossLineEdge(
            MainLine.ROYAL, MainLine.REVIEW,
            CrossLineType.SEQUENTIAL,
            "决策→审核",
            0.90
        ),
    },
    
    # 文治主线：智慧核心，连接所有
    MainLine.WENZHI: {
        MainLine.ECONOMY: CrossLineEdge(
            MainLine.WENZHI, MainLine.ECONOMY,
            CrossLineType.PARALLEL,
            "市场分析←消费者洞察",
            0.85
        ),
        MainLine.MILITARY: CrossLineEdge(
            MainLine.WENZHI, MainLine.MILITARY,
            CrossLineType.PARALLEL,
            "战略规划←军事情报",
            0.80
        ),
        MainLine.STANDARD: CrossLineEdge(
            MainLine.WENZHI, MainLine.STANDARD,
            CrossLineType.SEQUENTIAL,
            "智慧方案→执行标准",
            0.90
        ),
        MainLine.INNOVATION: CrossLineEdge(
            MainLine.WENZHI, MainLine.INNOVATION,
            CrossLineType.SEQUENTIAL,
            "知识创新→研究执行",
            0.85
        ),
    },
    
    # 经济主线：数据支撑
    MainLine.ECONOMY: {
        MainLine.MILITARY: CrossLineEdge(
            MainLine.ECONOMY, MainLine.MILITARY,
            CrossLineType.PARALLEL,
            "战争经济学←资源调度",
            0.75
        ),
        MainLine.STANDARD: CrossLineEdge(
            MainLine.ECONOMY, MainLine.STANDARD,
            CrossLineType.PARALLEL,
            "市场监控←风险评估",
            0.80
        ),
        MainLine.INNOVATION: CrossLineEdge(
            MainLine.ECONOMY, MainLine.INNOVATION,
            CrossLineType.SEQUENTIAL,
            "市场趋势→创新方向",
            0.85
        ),
    },
    
    # 军政主线：执行核心
    MainLine.MILITARY: {
        MainLine.STANDARD: CrossLineEdge(
            MainLine.MILITARY, MainLine.STANDARD,
            CrossLineType.SEQUENTIAL,
            "行动执行→合规标准",
            0.90
        ),
        MainLine.REVIEW: CrossLineEdge(
            MainLine.MILITARY, MainLine.REVIEW,
            CrossLineType.FEEDBACK,
            "执行结果→审核反馈",
            0.70
        ),
    },
    
    # 标准主线：执行落地
    MainLine.STANDARD: {
        MainLine.INNOVATION: CrossLineEdge(
            MainLine.STANDARD, MainLine.INNOVATION,
            CrossLineType.PARALLEL,
            "执行反馈←创新迭代",
            0.75
        ),
        MainLine.REVIEW: CrossLineEdge(
            MainLine.STANDARD, MainLine.REVIEW,
            CrossLineType.SEQUENTIAL,
            "执行结果→质量审核",
            0.95
        ),
    },
    
    # 创新主线：增长引擎
    MainLine.INNOVATION: {
        MainLine.ECONOMY: CrossLineEdge(
            MainLine.INNOVATION, MainLine.ECONOMY,
            CrossLineType.FEEDBACK,
            "创新成果→市场价值",
            0.80
        ),
    },
    
    # 审核主线：独立质量保障
    MainLine.REVIEW: {
        MainLine.ROYAL: CrossLineEdge(
            MainLine.REVIEW, MainLine.ROYAL,
            CrossLineType.FEEDBACK,
            "审核意见→决策调整",
            0.85
        ),
    },
}


# 问题复杂度等级（V5新增）
class ProblemComplexity(Enum):
    SIMPLE = "简单问题"      # 单部门可解
    MODERATE = "中等问题"    # 2-3部门协同
    COMPLEX = "复杂问题"     # 4-5部门协同
    CRITICAL = "关键问题"    # 全线联动


# 复杂度评估规则
COMPLEXITY_RULES = {
    ProblemComplexity.SIMPLE: {
        "indicators": ["单一领域", "明确目标", "标准解法"],
        "max_departments": 1,
        "max_lines": 1,
    },
    ProblemComplexity.MODERATE: {
        "indicators": ["多领域交叉", "需多视角", "创新方案"],
        "max_departments": 3,
        "max_lines": 2,
    },
    ProblemComplexity.COMPLEX: {
        "indicators": ["跨系统问题", "利益冲突", "战略影响"],
        "max_departments": 5,
        "max_lines": 4,
    },
    ProblemComplexity.CRITICAL: {
        "indicators": ["全局影响", "生死攸关", "变革需求"],
        "max_departments": 99,
        "max_lines": 7,
    },
}


# ═══════════════════════════════════════════════════════════════
# V5 核心算法：动态网状路由
# ═══════════════════════════════════════════════════════════════

class MeshRoutingEngine:
    """
    V5核心：网状串联调度引擎
    替代原有的静态 DEPARTMENT_SCHOOL_MATRIX
    """
    
    def __init__(self):
        self._routing_history: List[Dict] = []
        self._weight_learner = {}  # 从历史中学习的权重调整
    
    def evaluate_complexity(
        self, 
        problem_type: str, 
        context: Dict = None
    ) -> ProblemComplexity:
        """
        评估问题复杂度，确定需要调动的部门/主线数量
        """
        # 简化版：基于问题类型的预设复杂度
        complex_types = {
            "战略", "变革", "危机", "竞争", "营销", "创新", "治理",
            "文化", "制度", "范式", "文明", "演化"
        }
        
        # 检查关键词
        score = 0
        pt_lower = problem_type.lower()
        for keyword in complex_types:
            if keyword in pt_lower:
                score += 1
        
        if score >= 3:
            return ProblemComplexity.CRITICAL
        elif score >= 2:
            return ProblemComplexity.COMPLEX
        elif score >= 1:
            return ProblemComplexity.MODERATE
        else:
            return ProblemComplexity.SIMPLE
    
    def build_routing_path(
        self,
        problem_type: str,
        primary_department: str,
        context: Dict = None
    ) -> DynamicRoutingPath:
        """
        核心方法：根据问题动态构建调度路径
        替代原有静态矩阵，实现真正的网状串联
        """
        complexity = self.evaluate_complexity(problem_type, context)
        
        # 1. 确定主调度主线
        main_line = self._department_to_main_line(primary_department)
        
        # 2. 构建跨线协同路径
        nodes = []
        cross_lines = []
        
        if complexity == ProblemComplexity.SIMPLE:
            # 简单问题：单线处理
            nodes = self._build_single_line_nodes(main_line, primary_department)
            
        elif complexity == ProblemComplexity.MODERATE:
            # 中等问题：2线协同
            secondary_line = self._select_secondary_line(main_line, problem_type)
            nodes = self._build_parallel_nodes(main_line, secondary_line, primary_department)
            cross_lines.append((main_line, secondary_line, CrossLineType.PARALLEL))
            
        elif complexity == ProblemComplexity.COMPLEX:
            # 复杂问题：多线串联+并行
            related_lines = self._find_related_lines(main_line, problem_type)
            nodes = self._build_multi_line_nodes(related_lines, primary_department)
            for i in range(len(related_lines) - 1):
                cross_lines.append((
                    related_lines[i], 
                    related_lines[i+1], 
                    CrossLineType.SEQUENTIAL
                ))
                
        elif complexity == ProblemComplexity.CRITICAL:
            # 关键问题：全线联动
            all_lines = list(MainLine)
            nodes = self._build_full_network_nodes(all_lines, primary_department)
            for src in all_lines:
                for tgt in all_lines:
                    if src != tgt and tgt in MAIN_LINE_MATRIX.get(src, {}):
                        edge = MAIN_LINE_MATRIX[src][tgt]
                        cross_lines.append((src, tgt, edge.协同类型))
        
        # 3. 计算路径权重
        total_weight = sum(n.authority for n in nodes)
        
        return DynamicRoutingPath(
            problem_type=problem_type,
            path_id=f"path_{int(time.time()*1000)}",
            nodes=nodes,
            cross_lines=cross_lines,
            total_weight=total_weight,
            estimated_complexity=len(nodes) / 10.0
        )
    
    def _department_to_main_line(self, department: str) -> MainLine:
        """部门→主线映射"""
        mapping = {
            "吏部": MainLine.WENZHI,
            "礼部": MainLine.WENZHI,
            "户部": MainLine.ECONOMY,
            "兵部": MainLine.MILITARY,
            "刑部": MainLine.STANDARD,
            "工部": MainLine.STANDARD,
            "厂卫": MainLine.MILITARY,
            "三法司": MainLine.STANDARD,
            "翰林院": MainLine.REVIEW,
            "皇家藏书阁": MainLine.REVIEW,
            "内阁": MainLine.WENZHI,
            "七人决策代表大会": MainLine.ROYAL,
        }
        return mapping.get(department, MainLine.WENZHI)
    
    def _select_secondary_line(
        self, 
        primary: MainLine, 
        problem_type: str
    ) -> MainLine:
        """选择次要协同主线"""
        # 简单规则：基于问题类型选择
        if "经济" in problem_type or "市场" in problem_type or "消费" in problem_type:
            return MainLine.ECONOMY
        elif "执行" in problem_type or "增长" in problem_type:
            return MainLine.STANDARD
        elif "创新" in problem_type or "研究" in problem_type:
            return MainLine.INNOVATION
        elif "审核" in problem_type or "风险" in problem_type:
            return MainLine.REVIEW
        else:
            # 默认选文治作为智慧支撑
            return MainLine.WENZHI
    
    def _find_related_lines(
        self, 
        primary: MainLine, 
        problem_type: str
    ) -> List[MainLine]:
        """查找相关主线（用于复杂问题）"""
        related = [primary]
        
        # 从矩阵中查找所有可达的主线
        if primary in MAIN_LINE_MATRIX:
            for target, edge in MAIN_LINE_MATRIX[primary].items():
                if edge.权重 >= 0.75:  # 高权重协同
                    related.append(target)
        
        # 限制最多4条主线
        return related[:4]
    
    def _build_single_line_nodes(
        self, 
        main_line: MainLine, 
        department: str
    ) -> List[RoutingNode]:
        """构建单线节点"""
        # 从原有岗位体系获取
        return self._get_line_nodes(main_line, department)
    
    def _build_parallel_nodes(
        self,
        primary: MainLine,
        secondary: MainLine,
        primary_dept: str
    ) -> List[RoutingNode]:
        """构建并行节点（2线）"""
        nodes = []
        nodes.extend(self._get_line_nodes(primary, primary_dept))
        
        # 查找secondary对应的部门
        secondary_dept = self._main_line_to_department(secondary)
        nodes.extend(self._get_line_nodes(secondary, secondary_dept))
        
        return nodes
    
    def _build_multi_line_nodes(
        self,
        lines: List[MainLine],
        primary_dept: str
    ) -> List[RoutingNode]:
        """构建多线节点"""
        nodes = []
        primary = lines[0]
        
        # 主线用指定的部门
        nodes.extend(self._get_line_nodes(primary, primary_dept))
        
        # 其他线用默认部门
        for line in lines[1:]:
            dept = self._main_line_to_department(line)
            nodes.extend(self._get_line_nodes(line, dept))
        
        return nodes
    
    def _build_full_network_nodes(
        self,
        lines: List[MainLine],
        primary_dept: str
    ) -> List[RoutingNode]:
        """构建全网络节点（关键问题）"""
        nodes = []
        primary = lines[0]
        
        nodes.extend(self._get_line_nodes(primary, primary_dept))
        
        for line in lines[1:]:
            dept = self._main_line_to_department(line)
            nodes.extend(self._get_line_nodes(line, dept))
        
        return nodes
    
    def _main_line_to_department(self, line: MainLine) -> str:
        """主线→默认部门"""
        mapping = {
            MainLine.ROYAL: "七人决策代表大会",
            MainLine.WENZHI: "吏部",
            MainLine.ECONOMY: "户部",
            MainLine.MILITARY: "兵部",
            MainLine.STANDARD: "工部",
            MainLine.INNOVATION: "皇家科学院",
            MainLine.REVIEW: "翰林院",
        }
        return mapping.get(line, "吏部")
    
    def _get_line_nodes(self, line: MainLine, department: str) -> List[RoutingNode]:
        """获取某主线的节点（从岗位体系获取）"""
        # 简化版：返回关键节点
        # 实际实现中应从 _court_positions 获取
        nodes_map = {
            MainLine.ROYAL: [
                ("太师·王爵", "儒家", 1.0),
                ("太傅·公爵", "道家", 0.95),
            ],
            MainLine.WENZHI: [
                ("吏部尚书·伯爵", "素书", 0.9),
                ("礼部尚书·伯爵", "儒家", 0.85),
            ],
            MainLine.ECONOMY: [
                ("户部尚书·伯爵", "素书", 0.95),
                ("货币金融·伯爵", "社会科学", 0.90),
            ],
            MainLine.MILITARY: [
                ("兵部尚书·公爵", "道家", 0.95),
                ("兵部郎中·伯爵", "兵法", 0.90),
            ],
            MainLine.STANDARD: [
                ("工部侍郎·伯爵", "管理学", 0.90),
                ("增长引擎·伯爵", "法家", 0.85),
            ],
            MainLine.INNOVATION: [
                ("皇家科学院·伯爵", "科学", 0.90),
                ("经济战略司·伯爵", "经济学", 0.85),
            ],
            MainLine.REVIEW: [
                ("翰林院掌院", "法家", 0.95),
                ("藏书阁大学士", "史学", 0.90),
            ],
        }
        
        result = []
        for name, school, auth in nodes_map.get(line, []):
            result.append(RoutingNode(
                line=line,
                department=department,
                position_id=f"auto_{line.value}_{name}",
                sage=name.split("·")[0] if "·" in name else name,
                schools=[(school, auth)],
                authority=auth,
                is_primary=True
            ))
        
        return result
    
    def record_routing(self, path: DynamicRoutingPath, success: bool):
        """记录路由历史，用于学习优化"""
        self._routing_history.append({
            "path": path,
            "success": success,
            "timestamp": time.time()
        })
        
        # 简化版：只保留最近100条
        if len(self._routing_history) > 100:
            self._routing_history = self._routing_history[-100:]


# ═══════════════════════════════════════════════════════════════
# V5 兼容层：与V4原有接口兼容
# ═══════════════════════════════════════════════════════════════

# 全局实例
_mesh_engine = None

def get_mesh_routing_engine() -> MeshRoutingEngine:
    """获取网状路由引擎实例"""
    global _mesh_engine
    if _mesh_engine is None:
        _mesh_engine = MeshRoutingEngine()
    return _mesh_engine


def mesh_resolve_departments(
    problem_type: str,
    primary_department: str,
    context: Dict = None
) -> DynamicRoutingPath:
    """
    V5新增：网状动态部门解析
    替代原有的 resolve_departments
    """
    engine = get_mesh_routing_engine()
    return engine.build_routing_path(problem_type, primary_department, context)


def get_cross_line_matrix() -> Dict:
    """获取跨线协同矩阵（可视化用）"""
    matrix = {}
    for src, targets in MAIN_LINE_MATRIX.items():
        matrix[src.value] = {
            tgt.value: {
                "type": edge.协同类型.value,
                "weight": edge.权重,
                "condition": edge.触发条件,
            }
            for tgt, edge in targets.items()
        }
    return matrix


def get_main_line_stats() -> Dict:
    """获取主线统计信息"""
    return {
        "total_lines": len(MainLine),
        "lines": [line.value for line in MainLine],
        "cross_edges": sum(len(v) for v in MAIN_LINE_MATRIX.values()),
    }