"""知识图谱引擎 - 兼容层（与神经记忆系统双向对齐）"""
import json
from typing import Dict, List, Any, Optional, Set, Tuple
from ._ge_types import NodeType, EdgeType, GraphNode

__all__ = [
    'add_concept_impl',
    'add_relation_impl',
    'add_rule_impl',
    'bootstrap_rule_views',
    'build_compat_concept_dict',
    'build_compat_rule_dict',
    'build_relation_dict',
    'find_rule_node',
    'match_rule',
    'query_concept_impl',
    'query_relation_impl',
    'query_rule_impl',
    'sync_rule_relationships',
    'update_confidence_impl',
    'upsert_rule_node',
    'upsert_rule_store',
]

def _ensure_list(value: Any) -> List[Any]:
    """把任意值标准化为列表."""
    if value is None:
        return []
    if isinstance(value, list):
        return [item for item in value if item not in (None, "")]
    if isinstance(value, (tuple, set)):
        return [item for item in value if item not in (None, "")]
    return [value]

def _normalize_rule_type(rule_type: Any) -> Tuple[str, str]:
    """unified规则类型的中英文字段."""
    mapping = {
        "deductive": ("演绎规则", "deductive"),
        "inductive": ("归纳规则", "inductive"),
        "heuristic": ("启发规则", "heuristic"),
        "causal": ("因果规则", "causal"),
        "演绎规则": ("演绎规则", "deductive"),
        "归纳规则": ("归纳规则", "inductive"),
        "启发规则": ("启发规则", "heuristic"),
        "因果规则": ("因果规则", "causal")
    }
    raw = str(rule_type or "通用规则").strip()
    if raw in mapping:
        return mapping[raw]
    lowered = raw.lower()
    if lowered in mapping:
        return mapping[lowered]
    return raw, lowered if lowered != raw else raw

def _resolve_node_type(node_type_value: Any, default: NodeType = NodeType.CONCEPT) -> NodeType:
    """把字符串节点类型解析为枚举."""
    if isinstance(node_type_value, NodeType):
        return node_type_value
    try:
        return NodeType(str(node_type_value).lower())
    except (ValueError, TypeError):
        return default

def _generate_relation_id(source_id: str, target_id: str, edge_type: str, scope: str = "") -> str:
    """为图谱关系generate稳定ID."""
    import hashlib
    seed = f"{source_id}:{target_id}:{edge_type}:{scope}"
    return f"REL_{hashlib.md5(seed.encode()).hexdigest()[:16]}"

def build_compat_concept_dict(node: GraphNode) -> Dict[str, Any]:
    """把图谱概念节点转换为神经记忆系统兼容结构."""
    properties = dict(node.properties or {})
    concept_dict = {
        "概念ID": properties.get("概念ID", node.node_id),
        "概念名": properties.get("概念名", node.name),
        "概念类型": properties.get("概念类型", properties.get("category", "通用概念")),
        "定义": properties.get("定义", properties.get("definition", "")),
        "来源": properties.get("来源", node.source),
        "置信度": properties.get("置信度", node.confidence),
        "创建时间": properties.get("创建时间", node.created_at),
        "更新时间": node.updated_at,
        "图谱节点ID": node.node_id
    }
    concept_dict.update(properties)
    concept_dict.setdefault("概念ID", node.node_id)
    concept_dict.setdefault("概念名", node.name)
    concept_dict.setdefault("图谱节点ID", node.node_id)
    return concept_dict

def build_compat_rule_dict(
    core,
    rule_data: Dict[str, Any],
    graph_node_id: str = None
) -> Dict[str, Any]:
    """把 RuleEngine / 兼容存储unified转换为神经记忆系统兼容结构."""
    from datetime import datetime
    rule_data = dict(rule_data or {})
    rule_type_zh, rule_type_en = _normalize_rule_type(
        rule_data.get("规则类型") or rule_data.get("rule_type")
    )

    raw_conditions = rule_data.get(
        "conditions",
        rule_data.get("condition", rule_data.get("条件", rule_data.get("前提", [])))
    )
    explicit_metrics = [str(item) for item in _ensure_list(
        rule_data.get("关注metrics", rule_data.get("applicable_metrics", rule_data.get("metrics", rule_data.get("metric", []))))
    )]
    conditions = []
    for item in _ensure_list(raw_conditions):
        if isinstance(item, dict):
            conditions.append(dict(item))
        else:
            conditions.append({
                "field": str(item),
                "operator": "text",
                "value": None
            })
    existing_condition_fields = {
        str((item or {}).get("field", "")).strip()
        for item in conditions
        if isinstance(item, dict) and str((item or {}).get("field", "")).strip()
    }
    for metric_name in explicit_metrics:
        if metric_name and metric_name not in existing_condition_fields:
            conditions.append({
                "field": metric_name,
                "operator": "metric",
                "value": None
            })

    raw_actions = rule_data.get(
        "actions",
        rule_data.get("action", rule_data.get("动作", rule_data.get("consequences", rule_data.get("后果", []))))
    )
    actions = []
    for item in _ensure_list(raw_actions):
        if isinstance(item, dict):
            actions.append(dict(item))
        else:
            actions.append({
                "action_type": "recommend",
                "target": str(item),
                "value": None,
                "parameters": {}
            })

    applicable_industries = [str(item) for item in _ensure_list(
        rule_data.get("适用行业", rule_data.get("applicable_industries", rule_data.get("industries", rule_data.get("industry", []))))
    )]
    applicable_stages = [str(item) for item in _ensure_list(
        rule_data.get("适用阶段", rule_data.get("applicable_stages", rule_data.get("stages", rule_data.get("stage", []))))
    )]
    applicable_scenarios = [str(item) for item in _ensure_list(
        rule_data.get(
            "适用范围",
            rule_data.get("applicable_scenarios", rule_data.get("applicable_scenario", rule_data.get("scenarios", rule_data.get("scenario", []))))
        )
    )]
    for item in applicable_industries + applicable_stages + explicit_metrics:
        if item not in applicable_scenarios:
            applicable_scenarios.append(item)

    existing_ids = {
        item.get("规则ID")
        for item in core.compat_rule_store
        if isinstance(item, dict) and item.get("规则ID")
    }
    rule_id = str(
        rule_data.get("规则ID")
        or rule_data.get("rule_id")
        or f"RULE_KG_{datetime.now().strftime('%Y%m%d')}_{len(existing_ids) + 1:03d}"
    )
    while rule_id in existing_ids and rule_data.get("规则ID") is None and rule_data.get("rule_id") is None:
        rule_id = f"RULE_KG_{datetime.now().strftime('%Y%m%d')}_{len(existing_ids) + 1:03d}"
        existing_ids.add(rule_id)

    name = str(
        rule_data.get("名称")
        or rule_data.get("name")
        or f"{rule_type_zh}_{len(existing_ids) + 1}"
    )
    description = str(rule_data.get("描述", rule_data.get("description", "")))
    conclusion = rule_data.get("结论", rule_data.get("conclusion", ""))
    priority = rule_data.get("优先级", rule_data.get("priority", 3))
    source = str(rule_data.get("来源", rule_data.get("source", "knowledge_graph")))

    try:
        confidence = float(rule_data.get("置信度", rule_data.get("confidence", 0.5)))
    except (TypeError, ValueError):
        confidence = 0.5

    normalized = dict(rule_data)
    normalized.update({
        "规则ID": rule_id,
        "规则类型": rule_type_zh,
        "规则类型英文": rule_type_en,
        "名称": name,
        "描述": description,
        "前提": rule_data.get("前提", conditions),
        "条件": conditions,
        "conditions": conditions,
        "动作": actions,
        "actions": actions,
        "结论": conclusion,
        "优先级": priority,
        "priority": priority,
        "置信度": confidence,
        "confidence": confidence,
        "来源": source,
        "source": source,
        "适用行业": applicable_industries,
        "applicable_industries": applicable_industries,
        "适用阶段": applicable_stages,
        "applicable_stages": applicable_stages,
        "关注metrics": explicit_metrics,
        "applicable_metrics": explicit_metrics,
        "适用范围": applicable_scenarios,
        "applicable_scenarios": applicable_scenarios,
        "验证状态": rule_data.get("验证状态", "待验证"),
        "创建时间": rule_data.get("创建时间", rule_data.get("created_at", datetime.now().isoformat())),
        "更新时间": rule_data.get("更新时间", rule_data.get("updated_at", datetime.now().isoformat())),
        "应用次数": int(rule_data.get("应用次数", rule_data.get("execution_count", 0) or 0)),
        "成功次数": int(rule_data.get("成功次数", rule_data.get("success_count", 0) or 0))
    })
    if graph_node_id:
        normalized["图谱节点ID"] = graph_node_id
    return normalized

def build_relation_dict(core, source_id: str, target_id: str, edge_data: Dict[str, Any]) -> Dict[str, Any]:
    """把图谱边转换为关系兼容结构."""
    source_node = core.node_index.get(source_id)
    target_node = core.node_index.get(target_id)
    properties = dict(edge_data.get("properties") or {})
    edge_type = str(edge_data.get("edge_type", EdgeType.RELATED_TO.value))
    relation_type = str(properties.get("关系类型", properties.get("relation_type", edge_type)))
    relation_id = str(
        properties.get("关系ID")
        or properties.get("relation_id")
        or _generate_relation_id(source_id, target_id, edge_type, str(properties.get("scope", "")))
    )

    relation_dict = {
        "关系ID": relation_id,
        "关系类型": relation_type,
        "关系类型英文": edge_type,
        "源节点ID": source_id,
        "目标节点ID": target_id,
        "源节点名": source_node.name if source_node else source_id,
        "目标节点名": target_node.name if target_node else target_id,
        "源节点类型": source_node.node_type.value if source_node else "",
        "目标节点类型": target_node.node_type.value if target_node else "",
        "置信度": float(edge_data.get("confidence", properties.get("置信度", 1.0))),
        "创建时间": edge_data.get("created_at", properties.get("创建时间", ""))
    }
    relation_dict.update(properties)
    relation_dict.setdefault("关系ID", relation_id)
    return relation_dict

def find_rule_node(core, rule_id: str = None, rule_name: str = None) -> Optional[GraphNode]:
    """按规则ID或名称查找规则节点."""
    for node_id in core.type_index.get(NodeType.RULE, set()):
        node = core.node_index.get(node_id)
        if not node:
            continue
        if rule_id and (node.properties.get("规则ID") == rule_id or node.node_id == rule_id):
            return node
        if rule_name and node.name == rule_name:
            return node
    return None

def upsert_rule_store(core, rule_entry: Dict[str, Any]):
    """把规则写入兼容规则存储."""
    replaced = False
    for index, item in enumerate(core.compat_rule_store):
        if item.get("规则ID") == rule_entry.get("规则ID"):
            core.compat_rule_store[index] = dict(rule_entry)
            replaced = True
            break
    if not replaced:
        core.compat_rule_store.append(dict(rule_entry))

def upsert_rule_node(core, rule_entry: Dict[str, Any]) -> GraphNode:
    """把规则写入图谱规则节点."""
    from datetime import datetime
    confidence = float(rule_entry.get("置信度", rule_entry.get("confidence", 0.5)))
    existing_node = find_rule_node(core, rule_id=rule_entry.get("规则ID"), rule_name=rule_entry.get("名称"))
    if existing_node:
        existing_node.name = str(rule_entry.get("名称", existing_node.name))
        existing_node.properties.update(dict(rule_entry))
        existing_node.source = str(rule_entry.get("来源", existing_node.source))
        existing_node.confidence = confidence
        existing_node.updated_at = datetime.now().isoformat()
        core.graph.add_node(existing_node.node_id, **existing_node.to_dict())
        return existing_node

    return core.add_node(
        name=str(rule_entry.get("名称", rule_entry.get("规则ID", "rule"))),
        node_type=NodeType.RULE,
        properties=dict(rule_entry),
        source=str(rule_entry.get("来源", "rule_engine")),
        confidence=confidence
    )

def sync_rule_relationships(core, rule_node: GraphNode, rule_entry: Dict[str, Any]):
    """把规则的行业/阶段/metrics/动作目标写回到图谱关系."""
    from ._ge_graph import _generate_id
    if rule_node.node_id in core.graph:
        stale_edges = []
        for target_id, edge_data in list(core.graph[rule_node.node_id].items()):
            scope = str((edge_data.get("properties") or {}).get("scope", ""))
            if scope in {"industry", "stage", "condition", "action"}:
                stale_edges.append((rule_node.node_id, target_id))
        for source_id, target_id in stale_edges:
            if core.graph.has_edge(source_id, target_id):
                core.graph.remove_edge(source_id, target_id)

    rule_name = str(rule_entry.get("名称", rule_node.name))
    rule_id = str(rule_entry.get("规则ID", rule_node.node_id))
    rule_confidence = float(rule_entry.get("置信度", rule_entry.get("confidence", 0.5)))

    for industry in [str(item) for item in _ensure_list(rule_entry.get("适用行业", []))]:
        core.add_node(
            name=industry,
            node_type=NodeType.INDUSTRY,
            properties={"行业名": industry, "来源": "rule_engine"},
            source="rule_engine",
            confidence=rule_confidence
        )
        target_id = _generate_id(industry, NodeType.INDUSTRY)
        core.add_edge(
            source_name=rule_name,
            source_type=NodeType.RULE,
            target_name=industry,
            target_type=NodeType.INDUSTRY,
            edge_type=EdgeType.APPLIES_TO,
            properties={
                "关系ID": _generate_relation_id(rule_node.node_id, target_id, EdgeType.APPLIES_TO.value, "industry"),
                "关系类型": "规则适用行业",
                "scope": "industry",
                "规则ID": rule_id,
                "目标行业": industry
            },
            confidence=rule_confidence
        )

    for stage in [str(item) for item in _ensure_list(rule_entry.get("适用阶段", []))]:
        core.add_node(
            name=stage,
            node_type=NodeType.CONCEPT,
            properties={"概念名": stage, "概念类型": "业务阶段", "来源": "rule_engine"},
            source="rule_engine",
            confidence=rule_confidence
        )
        target_id = _generate_id(stage, NodeType.CONCEPT)
        core.add_edge(
            source_name=rule_name,
            source_type=NodeType.RULE,
            target_name=stage,
            target_type=NodeType.CONCEPT,
            edge_type=EdgeType.APPLIES_TO,
            properties={
                "关系ID": _generate_relation_id(rule_node.node_id, target_id, EdgeType.APPLIES_TO.value, "stage"),
                "关系类型": "规则适用阶段",
                "scope": "stage",
                "规则ID": rule_id,
                "目标阶段": stage
            },
            confidence=rule_confidence
        )

    for condition in _ensure_list(rule_entry.get("conditions", [])):
        field_name = str((condition or {}).get("field", "")).strip() if isinstance(condition, dict) else ""
        if not field_name:
            continue
        core.add_node(
            name=field_name,
            node_type=NodeType.METRIC,
            properties={"metrics名": field_name, "来源": "rule_engine"},
            source="rule_engine",
            confidence=rule_confidence
        )
        target_id = _generate_id(field_name, NodeType.METRIC)
        core.add_edge(
            source_name=rule_name,
            source_type=NodeType.RULE,
            target_name=field_name,
            target_type=NodeType.METRIC,
            edge_type=EdgeType.DEPENDS_ON,
            properties={
                "关系ID": _generate_relation_id(rule_node.node_id, target_id, EdgeType.DEPENDS_ON.value, "condition"),
                "关系类型": "规则依赖metrics",
                "scope": "condition",
                "规则ID": rule_id,
                "字段": field_name,
                "操作符": condition.get("operator"),
                "阈值": condition.get("value")
            },
            confidence=rule_confidence
        )

    for action in _ensure_list(rule_entry.get("actions", [])):
        target_name = str((action or {}).get("target", "")).strip() if isinstance(action, dict) else ""
        if not target_name:
            continue
        core.add_node(
            name=target_name,
            node_type=NodeType.ENTITY,
            properties={"实体名": target_name, "实体类型": "规则动作目标", "来源": "rule_engine"},
            source="rule_engine",
            confidence=rule_confidence
        )
        target_id = _generate_id(target_name, NodeType.ENTITY)
        core.add_edge(
            source_name=rule_name,
            source_type=NodeType.RULE,
            target_name=target_name,
            target_type=NodeType.ENTITY,
            edge_type=EdgeType.RELATED_TO,
            properties={
                "关系ID": _generate_relation_id(rule_node.node_id, target_id, EdgeType.RELATED_TO.value, "action"),
                "关系类型": "规则动作目标",
                "scope": "action",
                "规则ID": rule_id,
                "动作类型": action.get("action_type"),
                "动作值": action.get("value"),
                "动作参数": action.get("parameters", {})
            },
            confidence=rule_confidence
        )

def match_rule(core, rule_entry: Dict[str, Any], rule_id: str = None,
               rule_type: str = None, applicable_scenario: str = None) -> bool:
    """规则兼容过滤."""
    if rule_id and rule_entry.get("规则ID") != rule_id and rule_entry.get("图谱节点ID") != rule_id:
        return False

    if rule_type:
        target_zh, target_en = _normalize_rule_type(rule_type)
        matched_type = {
            str(rule_entry.get("规则类型", "")),
            str(rule_entry.get("规则类型英文", "")),
            str(rule_entry.get("rule_type", ""))
        }
        if target_zh not in matched_type and target_en not in matched_type and str(rule_type) not in matched_type:
            return False

    if applicable_scenario:
        scenario = applicable_scenario.lower()
        search_parts = []
        for key in ("适用范围", "适用行业", "适用阶段"):
            search_parts.extend([str(item) for item in _ensure_list(rule_entry.get(key))])
        search_parts.extend([
            str(rule_entry.get("名称", "")),
            str(rule_entry.get("描述", "")),
            str(rule_entry.get("结论", ""))
        ])
        if scenario not in " ".join(search_parts).lower():
            return False

    return True

# =============================================================================
# 以下为需要 core 引用的方法（延迟导入避免循环依赖）
# =============================================================================

def _load_compat_rules_impl(core):
    """加载兼容神经记忆系统的规则存储."""
    if not core.compat_rules_path.exists():
        _save_compat_rules_impl(core)
        return

    try:
        with open(core.compat_rules_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            core.compat_rule_store = data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        core.compat_rule_store = []
        _save_compat_rules_impl(core)

def _save_compat_rules_impl(core):
    """保存兼容神经记忆系统的规则存储."""
    with open(core.compat_rules_path, "w", encoding="utf-8") as file:
        json.dump(core.compat_rule_store, file, ensure_ascii=False, indent=2)

def bootstrap_rule_views(core):
    """启动时把规则兼容存储与规则节点双向对齐."""
    rule_node_ids = core.type_index.get(NodeType.RULE, set())
    if not core.compat_rule_store and not rule_node_ids:
        return

    normalized_store = []
    for rule in list(core.compat_rule_store):
        if not isinstance(rule, dict):
            continue
        normalized = build_compat_rule_dict(core, rule)
        rule_node = upsert_rule_node(core, normalized)
        normalized["图谱节点ID"] = rule_node.node_id
        sync_rule_relationships(core, rule_node, normalized)
        normalized_store.append(normalized)
    core.compat_rule_store = normalized_store

    for node_id in list(rule_node_ids):
        node = core.node_index.get(node_id)
        if not node:
            continue
        normalized = build_compat_rule_dict(core, node.properties, graph_node_id=node.node_id)
        upsert_rule_store(core, normalized)

    core._save_graph()
    _save_compat_rules_impl(core)

def add_concept_impl(core, concept_type: str, concept_data: Dict[str, Any]) -> str:
    """兼容神经记忆系统的概念写入接口."""
    from datetime import datetime
    concept_data = dict(concept_data or {})
    concept_name = str(
        concept_data.get("概念名")
        or concept_data.get("name")
        or concept_data.get("title")
        or f"{concept_type}_{len(core.type_index.get(NodeType.CONCEPT, set())) + 1}"
    )
    concept_id = _generate_relation_id(concept_name, concept_type, "concept", "")

    confidence_value = concept_data.get("置信度", concept_data.get("confidence", 0.5))
    try:
        confidence = float(confidence_value)
    except (TypeError, ValueError):
        confidence = 0.5

    concept_data.setdefault("概念ID", concept_id)
    concept_data.setdefault("概念名", concept_name)
    concept_data.setdefault("概念类型", concept_type)
    concept_data.setdefault("定义", concept_data.get("definition", ""))
    concept_data.setdefault("来源", concept_data.get("source", "knowledge_graph"))
    concept_data.setdefault("置信度", confidence)
    concept_data.setdefault("创建时间", datetime.now().isoformat())
    concept_data.setdefault("验证状态", "待验证")

    from ._ge_graph import add_node_impl, _generate_id
    add_node_impl(
        core,
        name=concept_name,
        node_type=NodeType.CONCEPT,
        properties=concept_data,
        source=str(concept_data.get("来源", "knowledge_graph")),
        confidence=confidence
    )
    core._save_graph()
    return concept_id

def query_concept_impl(core, concept_id: str = None, concept_name: str = None,
                       concept_type: str = None) -> List[Dict[str, Any]]:
    """兼容神经记忆系统的概念查询接口."""
    results = []
    for node_id in core.type_index.get(NodeType.CONCEPT, set()):
        node = core.node_index.get(node_id)
        if not node:
            continue

        concept = build_compat_concept_dict(node)
        if concept_id and concept.get("概念ID") != concept_id and node.node_id != concept_id:
            continue
        if concept_name and concept_name.lower() not in str(concept.get("概念名", node.name)).lower():
            continue
        if concept_type and concept.get("概念类型") != concept_type:
            continue
        results.append(concept)

    return results

def add_rule_impl(core, rule_type: str, rule_data: Dict[str, Any]) -> str:
    """兼容神经记忆系统的规则写入接口,并同步成规则节点与关系."""
    rule_entry = build_compat_rule_dict(core, {**dict(rule_data or {}), "规则类型": rule_type})
    rule_node = upsert_rule_node(core, rule_entry)
    rule_entry["图谱节点ID"] = rule_node.node_id
    upsert_rule_store(core, rule_entry)
    sync_rule_relationships(core, rule_node, rule_entry)
    core._save_graph()
    _save_compat_rules_impl(core)
    return rule_entry["规则ID"]

def add_relation_impl(core, relation_type: str, relation_data: Dict[str, Any]) -> str:
    """兼容神经记忆系统的关系写入接口."""
    from datetime import datetime
    from ._ge_graph import add_node_impl, add_edge_impl, _generate_id

    relation_entry = dict(relation_data or {})
    source_name = relation_entry.get("source") or relation_entry.get("原因") or relation_entry.get("概念A") or relation_entry.get("父概念")
    target_name = relation_entry.get("target") or relation_entry.get("结果") or relation_entry.get("概念B") or relation_entry.get("子概念")
    if not source_name or not target_name:
        return ""

    relation_mapping = {
        "因果关系": EdgeType.CAUSES,
        "causal": EdgeType.CAUSES,
        "相关关系": EdgeType.RELATED_TO,
        "related": EdgeType.RELATED_TO,
        "层次关系": EdgeType.BELONGS_TO,
        "hierarchy": EdgeType.BELONGS_TO,
        "时序关系": EdgeType.DEPENDS_ON,
        "temporal": EdgeType.DEPENDS_ON
    }
    relation_type_text = str(relation_type or relation_entry.get("关系类型") or relation_entry.get("relation_type") or "相关关系")
    edge_type = relation_mapping.get(relation_type_text, relation_mapping.get(relation_type_text.lower(), EdgeType.RELATED_TO))

    source_type = _resolve_node_type(relation_entry.get("source_type"), NodeType.CONCEPT)
    target_type = _resolve_node_type(relation_entry.get("target_type"), NodeType.CONCEPT)
    source_name = str(source_name)
    target_name = str(target_name)
    source_id = _generate_id(source_name, source_type)
    target_id = _generate_id(target_name, target_type)

    try:
        confidence = float(relation_entry.get("置信度", relation_entry.get("confidence", 0.5)))
    except (TypeError, ValueError):
        confidence = 0.5

    relation_id = str(
        relation_entry.get("关系ID")
        or relation_entry.get("relation_id")
        or _generate_relation_id(source_id, target_id, edge_type.value, relation_type_text)
    )

    source_properties = relation_entry.get("source_properties") or {"概念名": source_name, "概念类型": "通用概念", "来源": "knowledge_graph"}
    target_properties = relation_entry.get("target_properties") or {"概念名": target_name, "概念类型": "通用概念", "来源": "knowledge_graph"}
    add_node_impl(core, source_name, source_type, properties=source_properties, source="knowledge_graph", confidence=confidence)
    add_node_impl(core, target_name, target_type, properties=target_properties, source="knowledge_graph", confidence=confidence)

    properties = dict(relation_entry)
    properties.update({
        "关系ID": relation_id,
        "关系类型": relation_type_text,
        "relation_type": edge_type.value,
        "创建时间": relation_entry.get("创建时间", datetime.now().isoformat()),
        "置信度": confidence
    })

    add_edge_impl(
        core,
        source_name=source_name,
        source_type=source_type,
        target_name=target_name,
        target_type=target_type,
        edge_type=edge_type,
        properties=properties,
        confidence=confidence
    )
    core._save_graph()
    return relation_id

def query_rule_impl(core, rule_id: str = None, rule_type: str = None,
                    applicable_scenario: str = None) -> List[Dict[str, Any]]:
    """兼容神经记忆系统的规则查询接口."""
    results: Dict[str, Dict[str, Any]] = {}

    for node_id in core.type_index.get(NodeType.RULE, set()):
        node = core.node_index.get(node_id)
        if not node:
            continue
        rule_entry = build_compat_rule_dict(core, node.properties, graph_node_id=node.node_id)
        if match_rule(core, rule_entry, rule_id=rule_id, rule_type=rule_type, applicable_scenario=applicable_scenario):
            results[rule_entry["规则ID"]] = rule_entry

    for rule in core.compat_rule_store:
        if not isinstance(rule, dict):
            continue
        rule_entry = build_compat_rule_dict(core, rule, graph_node_id=rule.get("图谱节点ID"))
        if match_rule(core, rule_entry, rule_id=rule_id, rule_type=rule_type, applicable_scenario=applicable_scenario):
            results.setdefault(rule_entry["规则ID"], rule_entry)

    return list(results.values())

def query_relation_impl(core, relation_id: str = None, concept_id: str = None,
                        relation_type: str = None) -> List[Dict[str, Any]]:
    """兼容神经记忆系统的关系查询接口."""
    results = []
    concept_token = str(concept_id).lower() if concept_id else ""
    relation_token = str(relation_type).lower() if relation_type else ""

    for source_id, target_id, edge_data in core.graph.edges(data=True):
        relation = build_relation_dict(core, source_id, target_id, edge_data)
        if relation_id and relation.get("关系ID") != relation_id:
            continue

        if relation_token:
            relation_values = {
                str(relation.get("关系类型", "")).lower(),
                str(relation.get("关系类型英文", "")).lower(),
                str(relation.get("relation_type", "")).lower()
            }
            if relation_token not in relation_values:
                continue

        if concept_token:
            searchable = [
                relation.get("源节点ID", ""),
                relation.get("目标节点ID", ""),
                relation.get("源节点名", ""),
                relation.get("目标节点名", ""),
                relation.get("概念A", ""),
                relation.get("概念B", ""),
                relation.get("原因", ""),
                relation.get("结果", ""),
                relation.get("父概念", ""),
                relation.get("子概念", ""),
                relation.get("规则ID", "")
            ]
            if not any(concept_token in str(item).lower() for item in searchable if item not in (None, "")):
                continue

        results.append(relation)

    return results

def update_confidence_impl(core, entity_type: str, entity_id: str,
                          new_confidence: float, evidence: str = ""):
    """兼容神经记忆系统的置信度更新接口."""
    from datetime import datetime

    if entity_type == "concept":
        target_node = core.node_index.get(entity_id)
        if not target_node:
            return
        history = list(target_node.properties.get("置信度历史", []))
        history.append({
            "原置信度": target_node.properties.get("置信度", target_node.confidence),
            "新置信度": new_confidence,
            "时间": datetime.now().isoformat(),
            "证据": evidence
        })
        target_node.properties["置信度"] = new_confidence
        target_node.properties["置信度历史"] = history
        target_node.properties["验证状态"] = "已验证" if new_confidence >= 0.85 else "部分验证" if new_confidence >= 0.70 else "待验证"
        target_node.confidence = new_confidence
        target_node.updated_at = datetime.now().isoformat()
        core.graph.add_node(target_node.node_id, **target_node.to_dict())
        core._save_graph()
        return

    if entity_type == "rule":
        matched_rules = query_rule_impl(core, rule_id=entity_id)
        if not matched_rules:
            return
        updated_rule = dict(matched_rules[0])
        history = list(updated_rule.get("置信度历史", []))
        history.append({
            "原置信度": updated_rule.get("置信度", 0.5),
            "新置信度": new_confidence,
            "时间": datetime.now().isoformat(),
            "证据": evidence
        })
        updated_rule["置信度"] = new_confidence
        updated_rule["confidence"] = new_confidence
        updated_rule["置信度历史"] = history
        updated_rule["验证状态"] = "已验证" if new_confidence >= 0.85 else "部分验证" if new_confidence >= 0.70 else "待验证"
        updated_rule["更新时间"] = datetime.now().isoformat()

        rule_node = find_rule_node(core, rule_id=entity_id)
        if rule_node:
            rule_node.properties.update(updated_rule)
            rule_node.confidence = new_confidence
            rule_node.updated_at = updated_rule["更新时间"]
            core.graph.add_node(rule_node.node_id, **rule_node.to_dict())

        upsert_rule_store(core, updated_rule)
        core._save_graph()
        _save_compat_rules_impl(core)
        return

    if entity_type == "relation":
        for source_id, target_id, edge_data in core.graph.edges(data=True):
            relation = build_relation_dict(core, source_id, target_id, edge_data)
            if relation.get("关系ID") != entity_id:
                continue
            properties = dict(edge_data.get("properties") or {})
            history = list(properties.get("置信度历史", []))
            history.append({
                "原置信度": edge_data.get("confidence", properties.get("置信度", 0.5)),
                "新置信度": new_confidence,
                "时间": datetime.now().isoformat(),
                "证据": evidence
            })
            properties["置信度"] = new_confidence
            properties["置信度历史"] = history
            properties["验证状态"] = "已验证" if new_confidence >= 0.85 else "部分验证" if new_confidence >= 0.70 else "待验证"
            edge_data["properties"] = properties
            edge_data["confidence"] = new_confidence
            core.graph[source_id][target_id].update(edge_data)
            core._save_graph()
            return

