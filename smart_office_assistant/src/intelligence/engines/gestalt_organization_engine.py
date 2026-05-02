# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze',
    'create_gestalt_engine',
    'explain_organization',
    'find',
    'get_gestalt_insights',
    'get_organization_quality',
    'organize',
    'union',
]

格式塔感知组织系统 v1.0.0
======================

感知组织系统

核心来源:
- Gestalt心理学原则
- 变分理论:感知组织 = 变分问题的最优解
- 神经几何学

格式塔原则:
1. 接近律 (Proximity) - 距离近的元素被分组
2. 相似律 (Similarity) - 相似的元素被分组
3. 连续律 (Continuity) - 光滑轨迹的优先性
4. 闭合律 (Closure) - 倾向补全不完整的图形
5. 共命运律 (Common Fate) - 同步运动的元素分组
6. Prägnanz律 - 倾向最简洁规则的形式

核心思想:整体大于部分之和

@author: Somn AI
@version: 1.0.0
@date: 2026-04-02
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass, field
from enum import Enum
import heapq
from collections import defaultdict

class GestaltPrinciple(Enum):
    """格式塔原则"""
    PROXIMITY = "proximity"           # 接近律
    SIMILARITY = "similarity"         # 相似律
    CONTINUITY = "continuity"        # 连续律
    CLOSURE = "closure"              # 闭合律
    COMMON_FATE = "common_fate"      # 共命运律
    FIGURE_GROUND = "figure_ground"  # 图底关系
    SYMMETRY = "symmetry"            # 对称性
    PRAGNANZ = "pragnanz"            # 好形律

@dataclass
class VisualElement:
    """视觉元素 - 感知组织的基本单位"""
    element_id: str
    position: Tuple[float, float]
    properties: Dict[str, Any]      # 颜色,大小,方向等
    activation: float = 1.0
    group_id: Optional[str] = None

@dataclass
class PerceptualGroup:
    """感知组群 - 格式塔组织的结果"""
    group_id: str
    elements: List[VisualElement]
    principles: List[GestaltPrinciple] = field(default_factory=list)
    coherence: float = 0.0           # 内聚度
    saliency: float = 1.0            # 显著性
    is_figure: bool = True           # 是否是前景

class ProximityAnalyzer:
    """接近律分析器"""
    
    def __init__(self, threshold: float = 0.1):
        self.threshold = threshold
    
    def analyze(self, elements: List[VisualElement]) -> Dict[str, Set[str]]:
        """分析接近律
        
        返回距离近的元素对
        """
        adjacency = defaultdict(set)
        
        for i, elem1 in enumerate(elements):
            for elem2 in elements[i+1:]:
                dist = self._distance(elem1.position, elem2.position)
                if dist < self.threshold:
                    adjacency[elem1.element_id].add(elem2.element_id)
                    adjacency[elem2.element_id].add(elem1.element_id)
        
        return adjacency
    
    def _distance(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """计算距离"""
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

class SimilarityAnalyzer:
    """相似律分析器"""
    
    def analyze(
        self,
        elements: List[VisualElement],
        properties: List[str] = None
    ) -> Dict[str, Set[str]]:
        """分析相似律
        
        根据指定属性的相似度分组
        """
        if properties is None:
            properties = ["color", "size", "orientation"]
        
        similarity_groups = defaultdict(set)
        
        for i, elem1 in enumerate(elements):
            for elem2 in elements[i+1:]:
                similarity = self._compute_similarity(elem1, elem2, properties)
                if similarity > 0.7:  # 相似度阈值
                    similarity_groups[elem1.element_id].add(elem2.element_id)
                    similarity_groups[elem2.element_id].add(elem1.element_id)
        
        return similarity_groups
    
    def _compute_similarity(
        self,
        elem1: VisualElement,
        elem2: VisualElement,
        properties: List[str]
    ) -> float:
        """计算相似度"""
        similarities = []
        
        for prop in properties:
            val1 = elem1.properties.get(prop)
            val2 = elem2.properties.get(prop)
            
            if val1 is None or val2 is None:
                continue
            
            # 数值属性
            if isinstance(val1, (int, float)):
                max_val = max(abs(val1), abs(val2))
                if max_val > 0:
                    sim = 1.0 - abs(val1 - val2) / max_val
                    similarities.append(max(0, sim))
            # 类别属性
            else:
                sim = 1.0 if val1 == val2 else 0.0
                similarities.append(sim)
        
        return np.mean(similarities) if similarities else 0.0

class ContinuityAnalyzer:
    """连续律分析器"""
    
    def __init__(self, curvature_threshold: float = 0.5):
        self.curvature_threshold = curvature_threshold
    
    def analyze(self, elements: List[VisualElement]) -> List[List[str]]:
        """分析连续律
        
        返回连续轨迹
        """
        # 按位置排序
        sorted_elems = sorted(elements, key=lambda e: (e.position[0], e.position[1]))
        
        # recognize连续轨迹
        paths = []
        used = set()
        
        for start in sorted_elems:
            if start.element_id in used:
                continue
            
            path = self._build_path(start, sorted_elems, used)
            if len(path) > 1:
                paths.append(path)
        
        return paths
    
    def _build_path(
        self,
        start: VisualElement,
        elements: List[VisualElement],
        used: Set[str]
    ) -> List[str]:
        """
        [v10.0 P0-4修复] 构建连续路径 — 添加绝对超时保护。

        原有 max_iterations 保护，但补充绝对时间超时（0.5s），
        防止曲率约束严格时路径构建耗时过长。
        """
        import time as _time
        path = [start.element_id]
        used.add(start.element_id)

        current = start
        # ★ [v10.0 P0-4] 双保护：迭代上限 + 绝对时间超时
        _max_path_iterations = len(elements) + 5
        _iter = 0
        _abs_deadline = _time.monotonic() + 0.5   # 绝对超时0.5s

        while True:
            # ★ [v10.0 P0-4] 双重退出条件
            if _iter > _max_path_iterations:
                logger.warning(
                    f"[GestaltEngine] 路径构建达到迭代上限({_max_path_iterations})，"
                    f"已构建{len(path)}个元素"
                )
                break

            if _time.monotonic() > _abs_deadline:
                logger.warning(
                    f"[GestaltEngine] 路径构建达到绝对超时(0.5s)，"
                    f"已构建{len(path)}个元素，提前终止"
                )
                break

            _iter += 1
            
            # 找最近的未使用元素
            best_next = None
            best_dist = float('inf')
            
            for elem in elements:
                if elem.element_id in used:
                    continue
                
                dist = np.sqrt(
                    (elem.position[0] - current.position[0])**2 +
                    (elem.position[1] - current.position[1])**2
                )
                
                # 检查曲率(不应太急转)
                if len(path) >= 2:
                    prev = [e for e in elements if e.element_id == path[-2]][0]
                    curvature = self._compute_curvature(prev.position, current.position, elem.position)
                    
                    if curvature > self.curvature_threshold:
                        continue
                
                if dist < best_dist:
                    best_dist = dist
                    best_next = elem
            
            if best_next is None or best_dist > 0.2:
                break
            
            path.append(best_next.element_id)
            used.add(best_next.element_id)
            current = best_next
        
        return path
    
    def _compute_curvature(
        self,
        p1: Tuple[float, float],
        p2: Tuple[float, float],
        p3: Tuple[float, float]
    ) -> float:
        """计算曲率"""
        v1 = np.array([p2[0] - p1[0], p2[1] - p1[1]])
        v2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])
        
        len1 = np.linalg.norm(v1)
        len2 = np.linalg.norm(v2)
        
        if len1 < 1e-6 or len2 < 1e-6:
            return 0
        
        v1_norm = v1 / len1
        v2_norm = v2 / len2
        
        dot_product = np.dot(v1_norm, v2_norm)
        angle = np.arccos(np.clip(dot_product, -1, 1))
        
        return angle

class ClosureAnalyzer:
    """闭合律分析器
    
    检测并补全不完整的形状
    """
    
    def analyze(self, elements: List[VisualElement]) -> List[PerceptualGroup]:
        """分析闭合律
        
        返回缺失闭合的组
        """
        groups = []
        
        # 检测闭合度
        for subset in self._generate_subsets(elements):
            closedness = self._compute_closedness(subset)
            
            if 0.3 < closedness < 0.95:  # 不完全闭合
                group = PerceptualGroup(
                    group_id=f"closure_{len(groups)}",
                    elements=subset,
                    principles=[GestaltPrinciple.CLOSURE],
                    coherence=closedness
                )
                groups.append(group)
        
        return groups
    
    def _generate_subsets(self, elements: List[VisualElement]):
        """generate候选子集"""
        # 简化:只返回相邻元素组
        for i in range(len(elements)):
            for j in range(i + 3, min(i + 10, len(elements) + 1)):
                yield elements[i:j]
    
    def _compute_closedness(self, elements: List[VisualElement]) -> float:
        """计算闭合度"""
        if len(elements) < 3:
            return 0
        
        # 计算形心到各点的距离
        centroid = self._compute_centroid(elements)
        distances = [
            np.sqrt((e.position[0] - centroid[0])**2 + (e.position[1] - centroid[1])**2)
            for e in elements
        ]
        
        mean_dist = np.mean(distances)
        variance = np.var(distances)
        
        # 闭合度 = 距离方差小的程度
        closedness = 1.0 / (1.0 + variance / (mean_dist**2 + 1e-6))
        return closedness
    
    def _compute_centroid(self, elements: List[VisualElement]) -> Tuple[float, float]:
        """计算形心"""
        x = np.mean([e.position[0] for e in elements])
        y = np.mean([e.position[1] for e in elements])
        return (x, y)

class CommonFateAnalyzer:
    """共命运律分析器"""
    
    def analyze(
        self,
        elements: List[VisualElement],
        motion: Dict[str, Tuple[float, float]]
    ) -> Dict[str, Set[str]]:
        """分析共命运律
        
        基于运动相似度分组
        """
        motion_groups = defaultdict(set)
        
        for i, elem1 in enumerate(elements):
            for elem2 in elements[i+1:]:
                m1 = motion.get(elem1.element_id, (0, 0))
                m2 = motion.get(elem2.element_id, (0, 0))
                
                # 计算运动相似度
                motion_sim = self._compute_motion_similarity(m1, m2)
                
                if motion_sim > 0.7:
                    motion_groups[elem1.element_id].add(elem2.element_id)
                    motion_groups[elem2.element_id].add(elem1.element_id)
        
        return motion_groups
    
    def _compute_motion_similarity(
        self,
        m1: Tuple[float, float],
        m2: Tuple[float, float]
    ) -> float:
        """计算运动相似度"""
        v1 = np.array(m1)
        v2 = np.array(m2)
        
        len1 = np.linalg.norm(v1)
        len2 = np.linalg.norm(v2)
        
        if len1 < 1e-6 or len2 < 1e-6:
            return 0
        
        cos_sim = np.dot(v1, v2) / (len1 * len2)
        return max(0, cos_sim)

class GestaltOrganizationEngine:
    """格式塔感知组织引擎
    
    整合所有格式塔原则,generate感知组织
    
    核心思想:多种原则共同作用,产生整体的感知组织
    """
    
    def __init__(self):
        """init引擎"""
        self.name = "GestaltOrganizationEngine"
        self.version="6.2.0"
        
        # 各分析器
        self.proximity_analyzer = ProximityAnalyzer()
        self.similarity_analyzer = SimilarityAnalyzer()
        self.continuity_analyzer = ContinuityAnalyzer()
        self.closure_analyzer = ClosureAnalyzer()
        self.common_fate_analyzer = CommonFateAnalyzer()
        
        # 权重配置
        self.principle_weights = {
            GestaltPrinciple.PROXIMITY: 0.2,
            GestaltPrinciple.SIMILARITY: 0.2,
            GestaltPrinciple.CONTINUITY: 0.2,
            GestaltPrinciple.CLOSURE: 0.15,
            GestaltPrinciple.COMMON_FATE: 0.15,
            GestaltPrinciple.PRAGNANZ: 0.1
        }
        
        # 组织历史
        self.organization_history: List[List[PerceptualGroup]] = []
    
    # [v10.0 P0-4] organize 整体超时上限
    ORGANIZE_TIMEOUT_SECONDS = 2.0

    def organize(
        self,
        elements: List[VisualElement],
        motion: Optional[Dict[str, Tuple[float, float]]] = None,
        active_principles: Optional[List[GestaltPrinciple]] = None
    ) -> List[PerceptualGroup]:
        """
        [v10.0 P0-4修复] 感知组织 — 添加整体超时保护。

        根据格式塔原则将元素分组。

        Args:
            elements: 视觉元素列表
            motion: 运动字典(可选)
            active_principles: 活跃原则列表

        Returns:
            感知组群列表（超时则返回已完成的分组）
        """
        import time as _time
        _org_start = _time.monotonic()

        if active_principles is None:
            active_principles = list(GestaltPrinciple)

        # [v10.0 P0-4] 每原则执行前检查整体超时
        groupings = {}

        _principles = [
            (GestaltPrinciple.PROXIMITY, 'proximity', lambda: self.proximity_analyzer.analyze(elements)),
            (GestaltPrinciple.SIMILARITY, 'similarity', lambda: self.similarity_analyzer.analyze(elements)),
            (GestaltPrinciple.CONTINUITY, 'continuity', lambda: self.continuity_analyzer.analyze(elements)),
            (GestaltPrinciple.CLOSURE, 'closure', lambda: self.closure_analyzer.analyze(elements)),
        ]

        for principle, key, analyzer_fn in _principles:
            if principle in active_principles:
                if _time.monotonic() - _org_start > self.ORGANIZE_TIMEOUT_SECONDS:
                    logger.warning(
                        f"[GestaltEngine] organize() 达到整体超时({self.ORGANIZE_TIMEOUT_SECONDS}s)，"
                        f"跳过原则 {key} 及后续"
                    )
                    break
                try:
                    groupings[key] = analyzer_fn()
                except Exception as e:
                    logger.warning(f"[GestaltEngine] {key} 分析失败: {e}")
                    groupings[key] = []

        if motion and GestaltPrinciple.COMMON_FATE in active_principles:
            if _time.monotonic() - _org_start <= self.ORGANIZE_TIMEOUT_SECONDS:
                try:
                    groupings['common_fate'] = self.common_fate_analyzer.analyze(elements, motion)
                except Exception as e:
                    logger.warning(f"[GestaltEngine] common_fate 分析失败: {e}")

        # synthesize所有原则
        try:
            final_groups = self._synthesize_groupings(elements, groupings)
        except Exception as e:
            logger.warning(f"[GestaltEngine] _synthesize_groupings 失败: {e}")
            final_groups = []

        # 计算内聚度和显著性（最后阶段也检查超时）
        for group in final_groups:
            if _time.monotonic() - _org_start > self.ORGANIZE_TIMEOUT_SECONDS:
                break
            try:
                group.coherence = self._compute_group_coherence(group, elements)
                group.saliency = self._compute_saliency(group, elements)
            except Exception:
                group.coherence = 0.0
                group.saliency = 0.0

        # 排序(显著性高的在前)
        final_groups.sort(key=lambda g: g.saliency, reverse=True)

        self.organization_history.append(final_groups)
        return final_groups
    
    def _synthesize_groupings(
        self,
        elements: List[VisualElement],
        groupings: Dict[str, Any]
    ) -> List[PerceptualGroup]:
        """synthesize多个分组结果"""
        # 使用联合-查找算法合并分组
        parent = {elem.element_id: elem.element_id for elem in elements}
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
        
        # 应用所有分组
        for group_type, grouping in groupings.items():
            if isinstance(grouping, dict):  # 邻接表
                for elem_id, adjacent in grouping.items():
                    for adj_id in adjacent:
                        union(elem_id, adj_id)
            elif isinstance(grouping, list):  # 路径列表
                for path in grouping:
                    for i in range(len(path) - 1):
                        union(path[i], path[i+1])
        
        # 构建最终的组
        groups_map = defaultdict(list)
        for elem in elements:
            root = find(elem.element_id)
            groups_map[root].append(elem)
        
        # 创建感知组
        final_groups = []
        for i, (root, elems) in enumerate(groups_map.items()):
            group = PerceptualGroup(
                group_id=f"group_{i}",
                elements=elems,
                principles=self._identify_active_principles(elems, groupings)
            )
            final_groups.append(group)
        
        return final_groups
    
    def _identify_active_principles(
        self,
        elements: List[VisualElement],
        groupings: Dict[str, Any]
    ) -> List[GestaltPrinciple]:
        """recognize活跃的格式塔原则"""
        principles = []
        elem_ids = {e.element_id for e in elements}
        
        # 检查每个原则是否适用
        if 'proximity' in groupings:
            for id1, adjacent in groupings['proximity'].items():
                if id1 in elem_ids and any(adj_id in elem_ids for adj_id in adjacent):
                    principles.append(GestaltPrinciple.PROXIMITY)
                    break
        
        if 'similarity' in groupings:
            for id1, adjacent in groupings['similarity'].items():
                if id1 in elem_ids:
                    principles.append(GestaltPrinciple.SIMILARITY)
                    break
        
        if 'continuity' in groupings:
            for path in groupings['continuity']:
                if any(elem_id in elem_ids for elem_id in path):
                    principles.append(GestaltPrinciple.CONTINUITY)
                    break
        
        return principles
    
    def _compute_group_coherence(
        self,
        group: PerceptualGroup,
        all_elements: List[VisualElement]
    ) -> float:
        """计算组的内聚度"""
        if len(group.elements) <= 1:
            return 1.0
        
        # 平均成对距离
        distances = []
        for i, elem1 in enumerate(group.elements):
            for elem2 in group.elements[i+1:]:
                dist = np.sqrt(
                    (elem1.position[0] - elem2.position[0])**2 +
                    (elem1.position[1] - elem2.position[1])**2
                )
                distances.append(dist)
        
        mean_dist = np.mean(distances) if distances else 0
        
        # 与组外元素的距离
        external_distances = []
        for elem_in in group.elements:
            for elem_out in all_elements:
                if elem_out not in group.elements:
                    dist = np.sqrt(
                        (elem_in.position[0] - elem_out.position[0])**2 +
                        (elem_in.position[1] - elem_out.position[1])**2
                    )
                    external_distances.append(dist)
        
        mean_external = np.mean(external_distances) if external_distances else mean_dist
        
        # 内聚度 = 1 - (组内距离 / 组外距离)
        coherence = 1.0 - min(1.0, mean_dist / (mean_external + 1e-6))
        return max(0, coherence)
    
    def _compute_saliency(
        self,
        group: PerceptualGroup,
        all_elements: List[VisualElement]
    ) -> float:
        """计算显著性"""
        # 基于原则数量和元素数量
        num_principles = len(group.principles)
        num_elements = len(group.elements)
        total_elements = len(all_elements)
        
        principle_saliency = num_principles / len(GestaltPrinciple)
        size_saliency = num_elements / total_elements
        coherence_saliency = group.coherence
        
        # 加权组合
        saliency = 0.3 * principle_saliency + 0.3 * size_saliency + 0.4 * coherence_saliency
        return saliency
    
    def get_organization_quality(self) -> float:
        """评估组织质量
        
        基于最后一次组织
        """
        if not self.organization_history:
            return 0.0
        
        last_org = self.organization_history[-1]
        
        if not last_org:
            return 0.0
        
        avg_coherence = np.mean([g.coherence for g in last_org])
        avg_saliency = np.mean([g.saliency for g in last_org])
        
        quality = 0.6 * avg_coherence + 0.4 * avg_saliency
        return quality
    
    def explain_organization(self, groups: List[PerceptualGroup]) -> str:
        """解释感知组织"""
        explanation = "感知组织说明:\n"
        
        for i, group in enumerate(groups):
            explanation += f"\n组 {i+1}:\n"
            explanation += f"  元素数: {len(group.elements)}\n"
            explanation += f"  活跃原则: {', '.join(p.value for p in group.principles)}\n"
            explanation += f"  内聚度: {group.coherence:.2f}\n"
            explanation += f"  显著性: {group.saliency:.2f}\n"
        
        overall_quality = self.get_organization_quality()
        explanation += f"\n总体组织质量: {overall_quality:.2f}"
        
        return explanation

# ==================== 工厂函数 ====================

def create_gestalt_engine() -> GestaltOrganizationEngine:
    """创建格式塔组织引擎"""
    return GestaltOrganizationEngine()

def get_gestalt_insights() -> List[str]:
    """get格式塔的关键洞见"""
    return [
        "整体大于部分之和 - 感知是形成完整的 Gestalt",
        "接近律 - 距离近的元素被分为一组",
        "相似律 - 相似的元素被分为一组",
        "连续律 - 光滑连续的轨迹被优先感知",
        "闭合律 - 视觉倾向补全不完整的形状",
        "共命运律 - 同步运动的元素被分组",
        "Prägnanz律 - 倾向最简洁规则的表示",
        "多种原则共同作用产生最终的感知组织"
    ]

# ==================== 测试代码 ====================

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
