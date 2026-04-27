"""
__all__ = [
    'add_edge',
    'add_node',
    'add_rule',
    'apply_rules',
    'causal_reasoning',
    'get_statistics',
    'multi_hop_reasoning',
    'narrative_reasoning',
    'path_finding',
    'pattern_matching',
]

图推理引擎v2 - 增强的知识推理能力

功能:
- 多跳推理
- 路径发现
- 图模式匹配
- 因果推理
- 叙事推理 [v1.0.0 文学智能增强]

作者: Somn AI
版本: v1.0.0
"""

from typing import Dict, List, Tuple, Optional, Set, Any
from collections import deque, defaultdict
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class ReasoningType(Enum):
    """推理类型"""
    DEDUCTIVE = "deductive"  # 演绎推理
    INDUCTIVE = "inductive"  # 归纳推理
    ABDUCTIVE = "abductive"  # 溯因推理
    CAUSAL = "causal"  # 因果推理
    NARRATIVE = "narrative"  # 叙事推理 [v1.0.0 文学智能增强]

class PathScore:
    """路径评分"""
    
    def __init__(self, path: List[str], score: float, 
                 path_type: str = "default", metadata: Optional[Dict] = None):
        """
        init路径评分
        
        Args:
            path: 路径节点列表
            score: 路径分数
            path_type: 路径类型
            metadata: 额外元数据
        """
        self.path = path
        self.score = score
        self.path_type = path_type
        self.metadata = metadata or {}
    
    def __lt__(self, other):
        return self.score > other.score  # 降序
    
    def __repr__(self):
        return f"PathScore(score={self.score:.3f}, type={self.path_type}, nodes={len(self.path)})"

class GraphReasoningEngineV2:
    """
    图推理引擎v2
    
    核心功能:
    1. 多跳推理 - 跨越多个关系进行推理
    2. 路径发现 - 找到推理路径
    3. 图模式匹配 - recognize子图模式
    4. 因果推理 - 推断因果关系
    """
    
    def __init__(self):
        """init推理引擎"""
        # 图结构
        self.graph: Dict[str, List[str]] = defaultdict(list)
        self.node_attributes: Dict[str, Dict] = {}
        self.edge_attributes: Dict[Tuple[str, str], Dict] = {}
        
        # 推理统计
        self.stats = {
            'total_reasonings': 0,
            'successful_reasonings': 0,
            'average_path_length': 0,
            'reasoning_types': defaultdict(int)
        }
        
        # 推理规则库
        self.rules: List[Dict] = []
        
        logger.info("图推理引擎v2init完成")
    
    def add_node(self, node_id: str, attributes: Optional[Dict] = None):
        """添加节点"""
        if node_id not in self.graph:
            self.graph[node_id] = []
        self.node_attributes[node_id] = attributes or {}
    
    def add_edge(self, source: str, target: str, 
                 relation: str = "related", weight: float = 1.0,
                 attributes: Optional[Dict] = None):
        """添加边"""
        if source not in self.graph:
            self.add_node(source)
        if target not in self.graph:
            self.add_node(target)
        
        self.graph[source].append(target)
        
        edge_key = (source, target)
        self.edge_attributes[edge_key] = {
            'relation': relation,
            'weight': weight,
            'attributes': attributes or {}
        }
    
    def add_rule(self, rule: Dict):
        """
        添加推理规则
        
        Args:
            rule: 规则字典
                {
                    'name': '规则名称',
                    'pattern': ['A', 'B', 'C'],  # 模式
                    'conclusion': 'D',  # 结论
                    'confidence': 0.9  # 置信度
                }
        """
        self.rules.append(rule)
        logger.debug(f"添加推理规则: {rule['name']}")
    
    def multi_hop_reasoning(self, start_node: str, max_hops: int = 5,
                            top_k: int = 10) -> List[PathScore]:
        """
        多跳推理 - 从起始节点探索
        
        Args:
            start_node: 起始节点
            max_hops: 最大跳数
            top_k: 返回前k条路径
            
        Returns:
            路径评分列表
        """
        self.stats['total_reasonings'] += 1
        
        if start_node not in self.graph:
            logger.warning(f"节点不存在: {start_node}")
            return []
        
        # BFS探索所有路径
        all_paths = []
        visited = set()
        queue = deque([(start_node, [start_node], 1.0)])
        
        while queue:
            current, path, path_score = queue.popleft()
            
            if len(path) > max_hops:
                continue
            
            # 记录路径
            if len(path) > 1:
                all_paths.append(PathScore(
                    path=path,
                    score=path_score,
                    path_type="multi_hop"
                ))
            
            # 探索邻居
            for neighbor in self.graph[current]:
                if neighbor not in path:  # 避免环
                    # 计算边权重
                    edge_weight = self._get_edge_weight(current, neighbor)
                    new_score = path_score * edge_weight
                    
                    queue.append((neighbor, path + [neighbor], new_score))
        
        # 排序并返回top_k
        all_paths.sort()
        result = all_paths[:top_k]
        
        if result:
            self.stats['successful_reasonings'] += 1
            avg_length = sum(len(p.path) for p in result) / len(result)
            self.stats['average_path_length'] = avg_length
            self.stats['reasoning_types']['multi_hop'] += 1
        
        logger.info(f"多跳推理完成: 从{start_node}找到{len(result)}条路径")
        return result
    
    def path_finding(self, start: str, end: str, 
                     k: int = 10, max_length: int = 10) -> List[PathScore]:
        """
        路径发现 - 找到多条推理路径
        
        Args:
            start: 起始节点
            end: 目标节点
            k: 返回前k条路径
            max_length: 最大路径长度
            
        Returns:
            路径评分列表
        """
        self.stats['total_reasonings'] += 1
        
        if start not in self.graph or end not in self.graph:
            logger.warning(f"节点不存在: {start} -> {end}")
            return []
        
        # 使用DFS找到所有路径
        all_paths = []
        self._find_all_paths(start, end, [], all_paths, max_length)
        
        # 计算路径分数
        scored_paths = []
        for path in all_paths:
            score = self._calculate_path_score(path)
            scored_paths.append(PathScore(
                path=path,
                score=score,
                path_type="path_finding"
            ))
        
        # 排序并返回top_k
        scored_paths.sort()
        result = scored_paths[:k]
        
        if result:
            self.stats['successful_reasonings'] += 1
            self.stats['reasoning_types']['path_finding'] += 1
        
        logger.info(f"路径发现完成: {start} -> {end}, 找到{len(result)}条路径")
        return result
    
    def _find_all_paths(self, current: str, target: str, path: List[str], 
                       all_paths: List[List[str]], max_length: int):
        """递归查找所有路径"""
        path = path + [current]
        
        if current == target:
            all_paths.append(path)
            return
        
        if len(path) >= max_length:
            return
        
        for neighbor in self.graph[current]:
            if neighbor not in path:
                self._find_all_paths(neighbor, target, path, all_paths, max_length)
    
    def _calculate_path_score(self, path: List[str]) -> float:
        """
        计算路径分数
        
        考虑因素:
        1. 边权重
        2. 路径长度 (越短越好)
        3. 节点属性
        """
        if len(path) < 2:
            return 0.0
        
        # 边权重乘积
        edge_weight = 1.0
        for i in range(len(path) - 1):
            edge_weight *= self._get_edge_weight(path[i], path[i+1])
        
        # 路径长度惩罚
        length_penalty = 1.0 / len(path)
        
        # 节点属性奖励
        node_bonus = self._calculate_node_bonus(path)
        
        # synthesize分数
        score = edge_weight * length_penalty * (1 + node_bonus)
        
        return score
    
    def _get_edge_weight(self, source: str, target: str) -> float:
        """get边权重"""
        edge_key = (source, target)
        if edge_key in self.edge_attributes:
            return self.edge_attributes[edge_key].get('weight', 1.0)
        return 1.0
    
    def _calculate_node_bonus(self, path: List[str]) -> float:
        """计算节点属性奖励"""
        bonus = 0.0
        
        for node in path:
            if node in self.node_attributes:
                attrs = self.node_attributes[node]
                if attrs.get('importance', 0) > 0.8:
                    bonus += 0.1
                if attrs.get('confidence', 0) > 0.9:
                    bonus += 0.1
        
        return bonus
    
    def pattern_matching(self, pattern: List[Tuple[str, str, str]]) -> List[List[str]]:
        """
        图模式匹配
        
        Args:
            pattern: 模式列表 [(节点, 关系, 节点), ...]
            
        Returns:
            匹配的实例列表
        """
        self.stats['total_reasonings'] += 1
        
        if not pattern:
            return []
        
        # 简化实现:匹配第一个三元组,然后扩展
        source_pattern = pattern[0]
        matches = []
        
        # 找到所有起始节点
        for node in self.graph.keys():
            if self._match_node_pattern(node, source_pattern[0]):
                # 扩展匹配
                match = self._extend_match([node], pattern, 1)
                if match:
                    matches.append(match)
        
        if matches:
            self.stats['successful_reasonings'] += 1
            self.stats['reasoning_types']['pattern_matching'] += 1
        
        logger.info(f"模式匹配完成: 找到{len(matches)}个匹配")
        return matches
    
    def _match_node_pattern(self, node: str, pattern: str) -> bool:
        """检查节点是否匹配模式"""
        if pattern == "*":
            return True  # 通配符
        
        if node in self.node_attributes:
            node_type = self.node_attributes[node].get('type', 'default')
            return node_type == pattern
        
        return False
    
    def _extend_match(self, current_match: List[str], 
                     pattern: List[Tuple[str, str, str]], 
                     pattern_idx: int) -> Optional[List[str]]:
        """递归扩展匹配"""
        if pattern_idx >= len(pattern):
            return current_match
        
        current_node = current_match[-1]
        target_pattern = pattern[pattern_idx]
        
        # 找到匹配的邻居
        for neighbor in self.graph[current_node]:
            if neighbor not in current_match:
                if self._match_node_pattern(neighbor, target_pattern[2]):
                    # 检查关系
                    if self._match_relation(current_node, neighbor, target_pattern[1]):
                        # 递归
                        result = self._extend_match(
                            current_match + [neighbor],
                            pattern,
                            pattern_idx + 1
                        )
                        if result:
                            return result
        
        return None
    
    def _match_relation(self, source: str, target: str, relation: str) -> bool:
        """检查关系是否匹配"""
        edge_key = (source, target)
        if edge_key in self.edge_attributes:
            edge_relation = self.edge_attributes[edge_key].get('relation', 'default')
            return edge_relation == relation or relation == "*"
        return False
    
    def causal_reasoning(self, effect: str, max_depth: int = 3) -> List[PathScore]:
        """
        因果推理 - 寻找导致effect的原因
        
        Args:
            effect: 效果节点
            max_depth: 最大深度
            
        Returns:
            因果路径列表
        """
        self.stats['total_reasonings'] += 1
        self.stats['reasoning_types']['causal'] += 1
        
        if effect not in self.graph:
            logger.warning(f"节点不存在: {effect}")
            return []
        
        # 逆向搜索
        causal_paths = []
        self._find_causes(effect, [], causal_paths, max_depth)
        
        # 计算分数
        scored_paths = []
        for path in causal_paths:
            score = self._calculate_causal_score(path)
            scored_paths.append(PathScore(
                path=path,
                score=score,
                path_type="causal"
            ))
        
        scored_paths.sort()
        result = scored_paths[:10]
        
        if result:
            self.stats['successful_reasonings'] += 1
        
        logger.info(f"因果推理完成: {effect}, 找到{len(result)}条因果路径")
        return result
    
    def _find_causes(self, current: str, path: List[str], 
                    all_paths: List[List[str]], max_depth: int):
        """递归查找原因"""
        if len(path) >= max_depth:
            return
        
        # 找到所有指向current的边
        for node in self.graph.keys():
            if current in self.graph[node] and node not in path:
                new_path = [node] + path + [current]
                all_paths.append(new_path)
                self._find_causes(node, new_path, all_paths, max_depth)
    
    def _calculate_causal_score(self, path: List[str]) -> float:
        """计算因果路径分数"""
        # 因果链越长,置信度越低
        length_penalty = 1.0 / len(path)
        
        # 边权重乘积
        edge_weight = 1.0
        for i in range(len(path) - 1):
            edge_key = (path[i], path[i+1])
            if edge_key in self.edge_attributes:
                edge_weight *= self.edge_attributes[edge_key].get('weight', 1.0)
        
        return edge_weight * length_penalty
    
    def apply_rules(self, node: str) -> List[Dict]:
        """
        应用推理规则
        
        Args:
            node: 起始节点
            
        Returns:
            推导出的结论列表
        """
        conclusions = []
        
        for rule in self.rules:
            pattern = rule['pattern']
            
            # 检查是否匹配规则
            if node in pattern:
                # 查找完整模式
                match = self.pattern_matching([
                    (pattern[i], "*", pattern[i+1])
                    for i in range(len(pattern) - 1)
                ])
                
                if match:
                    conclusions.append({
                        'rule_name': rule['name'],
                        'conclusion': rule['conclusion'],
                        'confidence': rule['confidence'],
                        'match': match[0]
                    })
        
        return conclusions
    
    def narrative_reasoning(self, central_node: str, 
                           narrative_type: str = "multi_voice") -> Dict:
        """
        叙事推理 - 基于知识图谱的叙事分析 [v1.0.0 文学智能增强]
        
        从知识图谱中提取叙事结构,支持两种叙事模式:
        
        1. multi_voice (多声部叙事 - 莫言style):
           从中心节点出发,探索不同关系路径,构建多维叙事网络
           每条路径代表一个"声部"(视角),多个声部交织成完整叙事
           
        2. temporal (时间轴叙事 - 路遥style):
           沿知识图谱追踪因果关系链,构建从困境到突破的时间线
           recognize关键转折点和演变规律
        
        Args:
            central_node: 中心叙事节点
            narrative_type: 叙事类型 (multi_voice / temporal)
            
        Returns:
            叙事分析结果
        """
        self.stats['total_reasonings'] += 1
        self.stats['reasoning_types']['narrative'] += 1
        
        if central_node not in self.graph:
            logger.warning(f"叙事推理: 节点不存在: {central_node}")
            return {"error": f"节点不存在: {central_node}"}
        
        if narrative_type == "multi_voice":
            result = self._multi_voice_narrative(central_node)
        elif narrative_type == "temporal":
            result = self._temporal_narrative(central_node)
        else:
            result = self._multi_voice_narrative(central_node)
        
        if result and "error" not in result:
            self.stats['successful_reasonings'] += 1
        
        logger.info(f"叙事推理完成: {central_node} [{narrative_type}]")
        return result
    
    def _multi_voice_narrative(self, central_node: str) -> Dict:
        """
        多声部叙事推理 - 莫言style
        
        从中心节点探索所有直接关系,每条关系代表一个"声部",
        构建多视角的叙事网络
        """
        # get中心节点的所有邻居
        neighbors = self.graph.get(central_node, [])
        
        if not neighbors:
            return {
                "narrative_type": "multi_voice",
                "central_node": central_node,
                "voices": [],
                "narrative_coherence": 0.0,
                "summary": f"节点 {central_node} 没有关联节点,无法构建多声部叙事"
            }
        
        # 为每个邻居构建一个"声部"
        voices = []
        for neighbor in neighbors:
            edge_key = (central_node, neighbor)
            edge_info = self.edge_attributes.get(edge_key, {})
            relation = edge_info.get('relation', 'related')
            weight = edge_info.get('weight', 1.0)
            
            # 进一步探索该声部的深度
            sub_neighbors = self.graph.get(neighbor, [])
            voice_depth = {
                "voice_id": f"voice_{neighbor}",
                "perspective": neighbor,
                "relation_to_center": relation,
                "weight": weight,
                "sub_nodes": sub_neighbors[:5],  # 限制深度
                "narrative_role": self._assign_narrative_role(relation)
            }
            voices.append(voice_depth)
        
        # 计算叙事连贯性 (声部之间的关系密度)
        coherence = self._calculate_narrative_coherence(voices)
        
        # 构建叙事弧线
        narrative_arc = self._construct_narrative_arc(central_node, voices)
        
        return {
            "narrative_type": "multi_voice",
            "central_node": central_node,
            "voice_count": len(voices),
            "voices": voices,
            "narrative_coherence": round(coherence, 3),
            "narrative_arc": narrative_arc,
            "summary": (
                f"以\"{central_node}\"为中心构建了 {len(voices)} 个声部的叙事网络, "
                f"叙事连贯性: {coherence:.2f}"
            )
        }
    
    def _temporal_narrative(self, central_node: str) -> Dict:
        """
        时间轴叙事推理 - 路遥style
        
        沿因果链追踪,构建困境→积累→转折→突破的叙事时间线
        """
        # 向后追踪(原因/历史)
        causal_paths = []
        for node in self.graph.keys():
            if central_node in self.graph[node]:
                edge_key = (node, central_node)
                edge_info = self.edge_attributes.get(edge_key, {})
                causal_paths.append({
                    "node": node,
                    "relation": edge_info.get('relation', 'causes'),
                    "weight": edge_info.get('weight', 1.0)
                })
        
        # 向前追踪(结果/未来)
        effect_paths = []
        for neighbor in self.graph.get(central_node, []):
            edge_key = (central_node, neighbor)
            edge_info = self.edge_attributes.get(edge_key, {})
            effect_paths.append({
                "node": neighbor,
                "relation": edge_info.get('relation', 'leads_to'),
                "weight": edge_info.get('weight', 1.0)
            })
        
        # 构建时间轴
        timeline = {
            "past": {
                "phase": "困境与积累",
                "nodes": [p["node"] for p in causal_paths[:5]],
                "connections": causal_paths[:5]
            },
            "present": {
                "phase": "当前状态",
                "node": central_node,
                "attributes": self.node_attributes.get(central_node, {})
            },
            "future": {
                "phase": "转折与突破",
                "nodes": [p["node"] for p in effect_paths[:5]],
                "connections": effect_paths[:5]
            }
        }
        
        # recognize关键转折点
        turning_points = []
        for effect in effect_paths:
            if effect["weight"] >= 0.9:  # 高权重的结果节点为潜在转折点
                turning_points.append(effect["node"])
        
        # 评估叙事动力 (困境的严重程度 vs 突破的可能性)
        narrative_momentum = (
            len(causal_paths) * 0.3 +  # 历史深度
            len(effect_paths) * 0.4 +  # 未来可能性
            len(turning_points) * 0.3   # 转折点数量
        )
        narrative_momentum = min(1.0, narrative_momentum / 5)
        
        return {
            "narrative_type": "temporal",
            "central_node": central_node,
            "timeline": timeline,
            "turning_points": turning_points,
            "narrative_momentum": round(narrative_momentum, 3),
            "summary": (
                f"\"{central_node}\"的时间轴叙事: "
                f"过去({len(causal_paths)}个因果) → 现在(核心节点) → "
                f"未来({len(effect_paths)}个推演), "
                f"叙事动力: {narrative_momentum:.2f}"
            )
        }
    
    def _assign_narrative_role(self, relation: str) -> str:
        """为关系分配叙事角色"""
        role_map = {
            "causes": "推动者",
            "leads_to": "引导者",
            "related": "关联者",
            "depends_on": "依赖者",
            "conflicts_with": "对抗者",
            "supports": "支持者",
            "opposes": "反对者",
            "part_of": "组成部分",
            "similar_to": "类比者"
        }
        return role_map.get(relation, "参与角色")
    
    def _calculate_narrative_coherence(self, voices: List[Dict]) -> float:
        """计算叙事连贯性 - 声部之间的关系密度"""
        if len(voices) < 2:
            return 1.0
        
        # 检查声部之间是否存在交叉引用
        cross_references = 0
        total_possible = 0
        
        voice_nodes = [v["perspective"] for v in voices]
        
        for i, vn1 in enumerate(voice_nodes):
            for j, vn2 in enumerate(voice_nodes):
                if i != j:
                    total_possible += 1
                    # 检查vn1和vn2之间是否有连接
                    if vn2 in self.graph.get(vn1, []):
                        cross_references += 1
        
        return cross_references / total_possible if total_possible > 0 else 0.0
    
    def _construct_narrative_arc(self, central_node: str, voices: List[Dict]) -> str:
        """构建叙事弧线描述"""
        voice_names = [v["perspective"] for v in voices[:3]]  # 取前3个声部
        roles = [v["narrative_role"] for v in voices[:3]]
        
        if len(voice_names) >= 3:
            arc = (
                f"\"{central_node}\"的叙事网络中, "
                f"\"{voice_names[0]}\"作为{roles[0]}, "
                f"\"{voice_names[1]}\"作为{roles[1]}, "
                f"与\"{voice_names[2]}\"({roles[2]}) "
                f"交织成多声部叙事"
            )
        elif len(voice_names) == 2:
            arc = (
                f"\"{central_node}\"的叙事由 "
                f"\"{voice_names[0]}\"({roles[0]}) "
                f"和\"{voice_names[1]}\"({roles[1]}) 双声部交织"
            )
        else:
            arc = f"\"{central_node}\"的单声部叙事"
        
        return arc
    
    def get_statistics(self) -> Dict:
        """get统计信息"""
        return {
            **self.stats,
            'num_nodes': len(self.graph),
            'num_edges': sum(len(neighbors) for neighbors in self.graph.values()),
            'num_rules': len(self.rules),
            'success_rate': (
                self.stats['successful_reasonings'] / self.stats['total_reasonings']
                if self.stats['total_reasonings'] > 0 else 0
            )
        }
