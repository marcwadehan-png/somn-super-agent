"""
__all__ = [
    'add_concept',
    'add_relation',
    'add_rule',
    'get_knowledge_graph_data',
    'get_statistics',
    'query_concept',
    'query_relation',
    'query_rule',
    'update_confidence',
]

知识库管理引擎
Knowledge Base Engine
"""

import json
import yaml
from pathlib import Path
from src.core.paths import LEARNING_DIR
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import uuid

class KnowledgeEngine:
    """神经记忆系统 - 知识库引擎"""
    
    def __init__(self, base_path: str = None):
        from src.core.paths import NEURAL_KNOWLEDGE_DIR
        self.base_path = Path(base_path) if base_path else NEURAL_KNOWLEDGE_DIR
        self.knowledge_path = self.base_path / "knowledge_base"
        
        # 创建必要的目录
        self.knowledge_path.mkdir(parents=True, exist_ok=True)
        
        # 知识库文件路径
        self.concepts_file = self.knowledge_path / "concepts.yaml"
        self.rules_file = self.knowledge_path / "rules.yaml"
        self.relations_file = self.knowledge_path / "relations.yaml"
        
        # [v22.5 缓存优化] 内存缓存，避免每次查询都重新读取YAML
        self._concepts_cache = None
        self._rules_cache = None
        self._relations_cache = None
        self._concepts_mtime = None
        self._rules_mtime = None
        self._relations_mtime = None
        
        # init知识库
        self._init_knowledge_base()
    
    def _init_knowledge_base(self):
        """init知识库文件"""
        
        # 概念知识库
        if not self.concepts_file.exists():
            initial_concepts = {
                "元数据": {
                    "版本": "1.0",
                    "创建时间": datetime.now().isoformat(),
                    "概念数量": 0
                },
                "概念类型": {
                    "情绪概念": [],
                    "价值概念": [],
                    "strategy概念": [],
                    "方法概念": [],
                    "工具概念": [],
                    "场景概念": []
                }
            }
            with open(self.concepts_file, 'w', encoding='utf-8') as f:
                yaml.dump(initial_concepts, f, allow_unicode=True, default_flow_style=False)
        
        # 规则知识库
        if not self.rules_file.exists():
            initial_rules = {
                "元数据": {
                    "版本": "1.0",
                    "创建时间": datetime.now().isoformat(),
                    "规则数量": 0
                },
                "规则类型": {
                    "演绎规则": [],
                    "归纳规则": [],
                    "启发规则": [],
                    "因果规则": []
                }
            }
            with open(self.rules_file, 'w', encoding='utf-8') as f:
                yaml.dump(initial_rules, f, allow_unicode=True, default_flow_style=False)
        
        # 关系知识库
        if not self.relations_file.exists():
            initial_relations = {
                "元数据": {
                    "版本": "1.0",
                    "创建时间": datetime.now().isoformat(),
                    "关系数量": 0
                },
                "关系类型": {
                    "因果关系": [],
                    "相关关系": [],
                    "层次关系": [],
                    "时序关系": []
                }
            }
            with open(self.relations_file, 'w', encoding='utf-8') as f:
                yaml.dump(initial_relations, f, allow_unicode=True, default_flow_style=False)
    
    # ── [v22.5 缓存优化] 缓存辅助方法 ───────────────────────────────────────────
    
    def _load_concepts_if_needed(self):
        """按需加载概念缓存（如果文件被修改则重新加载）"""
        import os
        need_reload = False
        if self._concepts_cache is None:
            need_reload = True
        elif self.concepts_file.exists():
            current_mtime = os.path.getmtime(self.concepts_file)
            if current_mtime != self._concepts_mtime:
                need_reload = True
        
        if need_reload:
            if self.concepts_file.exists():
                try:
                    with open(self.concepts_file, 'r', encoding='utf-8') as f:
                        self._concepts_cache = yaml.safe_load(f)
                    self._concepts_mtime = os.path.getmtime(self.concepts_file)
                except Exception as e:
                    logger.warning(f"加载概念缓存失败: {e}")
                    self._concepts_cache = None
            else:
                # 文件不存在，使用默认结构
                self._concepts_cache = {
                    "元数据": {"版本": "1.0", "创建时间": datetime.now().isoformat(), "概念数量": 0},
                    "概念类型": {
                        "情绪概念": [], "价值概念": [], "策略概念": [],
                        "方法概念": [], "工具概念": [], "场景概念": []
                    }
                }
                self._concepts_mtime = None
    
    def _load_rules_if_needed(self):
        """按需加载规则缓存"""
        import os
        need_reload = False
        if self._rules_cache is None:
            need_reload = True
        elif self.rules_file.exists():
            current_mtime = os.path.getmtime(self.rules_file)
            if current_mtime != self._rules_mtime:
                need_reload = True
        
        if need_reload:
            if self.rules_file.exists():
                try:
                    with open(self.rules_file, 'r', encoding='utf-8') as f:
                        self._rules_cache = yaml.safe_load(f)
                    self._rules_mtime = os.path.getmtime(self.rules_file)
                except Exception as e:
                    logger.warning(f"加载规则缓存失败: {e}")
                    self._rules_cache = None
            else:
                self._rules_cache = {
                    "元数据": {"版本": "1.0", "创建时间": datetime.now().isoformat(), "规则数量": 0},
                    "规则类型": {"演绎规则": [], "归纳规则": [], "启发规则": [], "因果规则": []}
                }
                self._rules_mtime = None
    
    def _load_relations_if_needed(self):
        """按需加载关系缓存"""
        import os
        need_reload = False
        if self._relations_cache is None:
            need_reload = True
        elif self.relations_file.exists():
            current_mtime = os.path.getmtime(self.relations_file)
            if current_mtime != self._relations_mtime:
                need_reload = True
        
        if need_reload:
            if self.relations_file.exists():
                try:
                    with open(self.relations_file, 'r', encoding='utf-8') as f:
                        self._relations_cache = yaml.safe_load(f)
                    self._relations_mtime = os.path.getmtime(self.relations_file)
                except Exception as e:
                    logger.warning(f"加载关系缓存失败: {e}")
                    self._relations_cache = None
            else:
                self._relations_cache = {
                    "元数据": {"版本": "1.0", "创建时间": datetime.now().isoformat(), "关系数量": 0},
                    "关系类型": {"因果关系": [], "相关关系": [], "层次关系": [], "时序关系": []}
                }
                self._relations_mtime = None
    
    # ── 原有方法 ─────────────────────────────────────────────────────────────────
    
    def add_concept(self, concept_type: str, concept_data: Dict) -> str:
        """
        添加概念到知识库（使用缓存优化）
        
        Args:
            concept_type: 概念类型 (情绪概念/价值概念/strategy概念/方法概念/工具概念/场景概念)
            concept_data: 概念数据
            
        Returns:
            概念ID
        """
        # [v22.5 缓存优化] 使用缓存，避免重复读取文件
        self._load_concepts_if_needed()
        concepts = self._concepts_cache
        
        # generate概念ID
        concept_id = f"CON_{datetime.now().strftime('%Y%m%d')}_{len(concepts['概念类型'].get(concept_type, [])) + 1:03d}"
        
        # 添加概念元数据
        concept_data["概念ID"] = concept_id
        concept_data["创建时间"] = datetime.now().isoformat()
        concept_data["验证状态"] = "待验证"
        concept_data["置信度"] = 0.5
        
        # 添加到对应类型
        if concept_type not in concepts["概念类型"]:
            concepts["概念类型"][concept_type] = []
        
        concepts["概念类型"][concept_type].append(concept_data)
        
        # 更新元数据
        concepts["元数据"]["概念数量"] = sum(len(v) for v in concepts["概念类型"].values())
        concepts["元数据"]["更新时间"] = datetime.now().isoformat()
        
        # 保存文件并更新缓存
        import os
        with open(self.concepts_file, 'w', encoding='utf-8') as f:
            yaml.dump(concepts, f, allow_unicode=True, default_flow_style=False)
        self._concepts_mtime = os.path.getmtime(self.concepts_file)
        
        return concept_id
    
    def add_rule(self, rule_type: str, rule_data: Dict) -> str:
        """
        添加规则到知识库（使用缓存优化）
        
        Args:
            rule_type: 规则类型 (演绎规则/归纳规则/启发规则/因果规则)
            rule_data: 规则数据
            
        Returns:
            规则ID
        """
        # [v22.5 缓存优化] 使用缓存
        self._load_rules_if_needed()
        rules = self._rules_cache
        
        # generate规则ID
        rule_id = f"RULE_{datetime.now().strftime('%Y%m%d')}_{len(rules['规则类型'].get(rule_type, [])) + 1:03d}"
        
        # 添加规则元数据
        rule_data["规则ID"] = rule_id
        rule_data["创建时间"] = datetime.now().isoformat()
        rule_data["验证状态"] = "待验证"
        rule_data["应用次数"] = 0
        rule_data["成功次数"] = 0
        
        # 添加到对应类型
        if rule_type not in rules["规则类型"]:
            rules["规则类型"][rule_type] = []
        
        rules["规则类型"][rule_type].append(rule_data)
        
        # 更新元数据
        rules["元数据"]["规则数量"] = sum(len(v) for v in rules["规则类型"].values())
        rules["元数据"]["更新时间"] = datetime.now().isoformat()
        
        # 保存文件并更新缓存
        import os
        with open(self.rules_file, 'w', encoding='utf-8') as f:
            yaml.dump(rules, f, allow_unicode=True, default_flow_style=False)
        self._rules_mtime = os.path.getmtime(self.rules_file)
        
        return rule_id
    
    def add_relation(self, relation_type: str, relation_data: Dict) -> str:
        """
        添加关系到知识库（使用缓存优化）
        
        Args:
            relation_type: 关系类型 (因果关系/相关关系/层次关系/时序关系)
            relation_data: 关系数据
            
        Returns:
            关系ID
        """
        # [v22.5 缓存优化] 使用缓存
        self._load_relations_if_needed()
        relations = self._relations_cache
        
        # generate关系ID
        relation_id = f"REL_{datetime.now().strftime('%Y%m%d')}_{len(relations['关系类型'].get(relation_type, [])) + 1:03d}"
        
        # 添加关系元数据
        relation_data["关系ID"] = relation_id
        relation_data["创建时间"] = datetime.now().isoformat()
        relation_data["验证状态"] = "待验证"
        
        # 添加到对应类型
        if relation_type not in relations["关系类型"]:
            relations["关系类型"][relation_type] = []
        
        relations["关系类型"][relation_type].append(relation_data)
        
        # 更新元数据
        relations["元数据"]["关系数量"] = sum(len(v) for v in relations["关系类型"].values())
        relations["元数据"]["更新时间"] = datetime.now().isoformat()
        
        # 保存文件并更新缓存
        import os
        with open(self.relations_file, 'w', encoding='utf-8') as f:
            yaml.dump(relations, f, allow_unicode=True, default_flow_style=False)
        self._relations_mtime = os.path.getmtime(self.relations_file)
        
        return relation_id
    
    def query_concept(self, concept_id: str = None, concept_name: str = None, 
                      concept_type: str = None) -> List[Dict]:
        """
        查询概念（使用缓存优化）
        
        Args:
            concept_id: 概念ID
            concept_name: 概念名称(模糊匹配)
            concept_type: 概念类型
            
        Returns:
            匹配的概念列表
        """
        # [v22.5 缓存优化] 使用缓存，避免每次读取文件
        self._load_concepts_if_needed()
        concepts = self._concepts_cache
        
        # 如果文件为空或格式不正确,返回空列表
        if not concepts or "概念类型" not in concepts:
            return []
        
        # 如果文件为空或格式不正确,返回空列表
        if not concepts or "概念类型" not in concepts:
            return []
        
        results = []
        
        # 确定搜索范围
        if concept_type:
            search_types = [concept_type]
        else:
            search_types = list(concepts["概念类型"].keys())
        
        # 搜索
        for ctype in search_types:
            for concept in concepts["概念类型"].get(ctype, []):
                # ID精确匹配
                if concept_id and concept.get("概念ID") == concept_id:
                    return [concept]
                
                # 名称模糊匹配
                if concept_name:
                    if concept_name.lower() in concept.get("概念名", "").lower():
                        results.append(concept)
                        continue
                
                # 如果没有过滤条件,返回所有
                if not concept_id and not concept_name:
                    results.append(concept)
        
        return results
    
    def query_rule(self, rule_id: str = None, rule_type: str = None,
                   applicable_scenario: str = None) -> List[Dict]:
        """
        查询规则（使用缓存优化）
        
        Args:
            rule_id: 规则ID
            rule_type: 规则类型
            applicable_scenario: 适用场景(模糊匹配)
            
        Returns:
            匹配的规则列表
        """
        # [v22.5 缓存优化] 使用缓存
        self._load_rules_if_needed()
        rules = self._rules_cache
        
        # 如果文件为空或格式不正确,返回空列表
        if not rules or "规则类型" not in rules:
            return []
        
        results = []
        
        # 确定搜索范围
        if rule_type:
            search_types = [rule_type]
        else:
            search_types = list(rules["规则类型"].keys())
        
        # 搜索
        for rtype in search_types:
            for rule in rules["规则类型"].get(rtype, []):
                # ID精确匹配
                if rule_id and rule.get("规则ID") == rule_id:
                    return [rule]
                
                # 场景匹配
                if applicable_scenario:
                    scenarios = rule.get("适用范围", [])
                    if isinstance(scenarios, list):
                        if any(applicable_scenario.lower() in str(s).lower() for s in scenarios):
                            results.append(rule)
                            continue
                
                # 如果没有过滤条件,返回所有
                if not rule_id and not applicable_scenario:
                    results.append(rule)
        
        return results
    
    def query_relation(self, relation_id: str = None, concept_id: str = None,
                       relation_type: str = None) -> List[Dict]:
        """
        查询关系（使用缓存优化）
        
        Args:
            relation_id: 关系ID
            concept_id: 相关概念ID(作为源或目标)
            relation_type: 关系类型
            
        Returns:
            匹配的关系列表
        """
        # [v22.5 缓存优化] 使用缓存
        self._load_relations_if_needed()
        relations = self._relations_cache
        
        # 如果文件为空或格式不正确,返回空列表
        if not relations or "关系类型" not in relations:
            return []
        
        results = []
        
        # 确定搜索范围
        if relation_type:
            search_types = [relation_type]
        else:
            search_types = list(relations["关系类型"].keys())
        
        # 搜索
        for rtype in search_types:
            for relation in relations["关系类型"].get(rtype, []):
                # ID精确匹配
                if relation_id and relation.get("关系ID") == relation_id:
                    return [relation]
                
                # 概念相关匹配
                if concept_id:
                    if concept_id in str(relation.get("原因", "")) or \
                       concept_id in str(relation.get("结果", "")) or \
                       concept_id in str(relation.get("概念A", "")) or \
                       concept_id in str(relation.get("概念B", "")) or \
                       concept_id in str(relation.get("父概念", "")) or \
                       concept_id in str(relation.get("子概念", "")):
                        results.append(relation)
                        continue
                
                # 如果没有过滤条件,返回所有
                if not relation_id and not concept_id:
                    results.append(relation)
        
        return results
    
    def update_confidence(self, entity_type: str, entity_id: str, 
                         new_confidence: float, evidence: str):
        """
        更新实体置信度
        
        Args:
            entity_type: 实体类型 (concept/rule/relation)
            entity_id: 实体ID
            new_confidence: 新置信度 (0-1)
            evidence: 证据描述
        """
        file_map = {
            "concept": self.concepts_file,
            "rule": self.rules_file,
            "relation": self.relations_file
        }
        
        type_map = {
            "concept": "概念类型",
            "rule": "规则类型",
            "relation": "关系类型"
        }
        
        file_path = file_map.get(entity_type)
        if not file_path:
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        # 查找并更新
        for type_name, entities in data[type_map[entity_type]].items():
            for entity in entities:
                if entity.get(f"{entity_type.upper()}ID") == entity_id or \
                   entity.get(f"概念ID") == entity_id or \
                   entity.get(f"规则ID") == entity_id or \
                   entity.get(f"关系ID") == entity_id:
                    
                    old_confidence = entity.get("置信度", 0.5)
                    entity["置信度"] = new_confidence
                    
                    # 记录置信度变更历史
                    if "置信度历史" not in entity:
                        entity["置信度历史"] = []
                    
                    entity["置信度历史"].append({
                        "原置信度": old_confidence,
                        "新置信度": new_confidence,
                        "时间": datetime.now().isoformat(),
                        "证据": evidence
                    })
                    
                    # 更新验证状态
                    if new_confidence >= 0.85:
                        entity["验证状态"] = "已验证"
                    elif new_confidence >= 0.70:
                        entity["验证状态"] = "部分验证"
                    elif new_confidence < 0.40:
                        entity["验证状态"] = "待验证"
        
        # 保存
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
    
    def get_knowledge_graph_data(self) -> Dict:
        """
        get知识图谱数据(用于可视化)
        
        Returns:
            图谱数据 {nodes, edges}
        """
        nodes = []
        edges = []
        
        # 读取概念作为节点
        with open(self.concepts_file, 'r', encoding='utf-8') as f:
            concepts = yaml.safe_load(f)
        
        for ctype, concept_list in concepts["概念类型"].items():
            for concept in concept_list:
                nodes.append({
                    "id": concept.get("概念ID", ""),
                    "label": concept.get("概念名", ""),
                    "type": ctype,
                    "confidence": concept.get("置信度", 0.5)
                })
        
        # 读取关系作为边
        with open(self.relations_file, 'r', encoding='utf-8') as f:
            relations = yaml.safe_load(f)
        
        edge_id = 1
        for rtype, relation_list in relations["关系类型"].items():
            for relation in relation_list:
                source = relation.get("原因") or relation.get("概念A") or relation.get("父概念")
                target = relation.get("结果") or relation.get("概念B") or relation.get("子概念")
                
                if source and target:
                    edges.append({
                        "id": f"edge_{edge_id}",
                        "source": source if isinstance(source, str) else str(source),
                        "target": target if isinstance(target, str) else str(target),
                        "type": rtype,
                        "strength": relation.get("关系强度", relation.get("相关系数", 0.5))
                    })
                    edge_id += 1
        
        return {"nodes": nodes, "edges": edges}
    
    def get_statistics(self) -> Dict:
        """get知识库统计信息"""
        stats = {
            "概念统计": {},
            "规则统计": {},
            "关系统计": {},
            "总体统计": {}
        }
        
        # 确保知识库文件存在
        self._init_knowledge_base()
        
        # 概念统计
        with open(self.concepts_file, 'r', encoding='utf-8') as f:
            concepts = yaml.safe_load(f)
        
        # 如果文件格式不正确,返回空统计
        if not concepts or "概念类型" not in concepts:
            return stats
        
        for ctype, concept_list in concepts["概念类型"].items():
            stats["概念统计"][ctype] = len(concept_list)
        
        # 规则统计
        with open(self.rules_file, 'r', encoding='utf-8') as f:
            rules = yaml.safe_load(f)
        
        if not rules or "规则类型" not in rules:
            return stats
        
        for rtype, rule_list in rules["规则类型"].items():
            stats["规则统计"][rtype] = len(rule_list)
        
        # 关系统计
        with open(self.relations_file, 'r', encoding='utf-8') as f:
            relations = yaml.safe_load(f)
        
        if not relations or "关系类型" not in relations:
            return stats
        
        for rtype, relation_list in relations["关系类型"].items():
            stats["关系统计"][rtype] = len(relation_list)
        
        # 总体统计
        stats["总体统计"] = {
            "概念总数": sum(stats["概念统计"].values()),
            "规则总数": sum(stats["规则统计"].values()),
            "关系总数": sum(stats["关系统计"].values()),
            "知识密度": sum(stats["概念统计"].values()) / max(1, sum(stats["关系统计"].values()))
        }
        
        return stats

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
