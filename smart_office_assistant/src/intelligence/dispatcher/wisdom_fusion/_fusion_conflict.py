"""wisdom_fusion conflict resolver v1.0"""
import logging
from typing import Dict, List, Any, Tuple, Set

__all__ = [
    'resolve_conflicts',
]

logger = logging.getLogger(__name__)

def _find_common_keywords(contributions: List) -> Set[str]:
    keyword_sets = []
    for contrib in contributions:
        text = str(contrib.output).lower()
        words = []
        chars = []
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                chars.append(char)
                if len(chars) >= 2:
                    words.append(''.join(chars[-2:]))
                if len(chars) >= 3:
                    words.append(''.join(chars[-3:]))
        keyword_sets.append(set(words))
    if not keyword_sets:
        return set()
    common = set.intersection(*keyword_sets)
    common_words = {"的", "了", "在", "和", "与", "是", "有", "可以", "需要"}
    common = {kw for kw in common if kw not in common_words and len(kw) >= 2}
    return common

def resolve_conflicts(self, contributions: List, task_domain: str, context: Dict[str, Any]) -> Tuple[List, List]:
    resolved_contributions = contributions.copy()
    resolved_conflicts = []
    conflicts = _detect_conflicts(contributions)
    if not conflicts:
        return resolved_contributions, resolved_conflicts
    logger.info(f"检测到 {len(conflicts)} 个冲突,正在解决...")
    if task_domain in ["strategic", "tactical"]:
        strategy = "hierarchical_priority"
    elif task_domain in ["ethical", "cultural"]:
        strategy = "consensus_building"
    else:
        strategy = "weighted_consensus"
    resolution_method = self.conflict_resolution_strategies.get(strategy)
    if resolution_method:
        resolved_contributions, resolution_notes = resolution_method(contributions, task_domain, context)
        resolved_conflicts.extend(resolution_notes)
    return resolved_contributions, resolved_conflicts

def _detect_conflicts(contributions: List) -> List[Tuple[str, str]]:
    conflicts = []
    for i, contrib_i in enumerate(contributions):
        for j, contrib_j in enumerate(contributions):
            if i >= j:
                continue
            if contrib_i.confidence > 0.7 and contrib_j.confidence > 0.7:
                i_text = str(contrib_i.output).lower()
                j_text = str(contrib_j.output).lower()
                conflict_keywords = {
                    ("扩张", "收缩"), ("激进", "保守"),
                    ("立即", "等待"), ("投资", "缩减"),
                    ("进攻", "防守"), ("创新", "传统")
                }
                for (kw1, kw2) in conflict_keywords:
                    if (kw1 in i_text and kw2 in j_text) or (kw2 in i_text and kw1 in j_text):
                        conflicts.append((contrib_i.module_name, contrib_j.module_name))
                        break
    return conflicts

def _consensus_building(contributions: List, task_domain: str, context: Dict[str, Any]) -> Tuple[List, List]:
    adjusted = contributions.copy()
    notes = []
    common_keywords = _find_common_keywords(contributions)
    if common_keywords:
        for contrib in adjusted:
            contrib_text = str(contrib.output).lower()
            keyword_match = sum(1 for kw in common_keywords if kw in contrib_text)
            match_ratio = keyword_match / len(common_keywords) if common_keywords else 0
            contrib.weight *= (1.0 + match_ratio * 0.3)
            notes.append(f"提升 {contrib.module_name} 权重(共识匹配度: {match_ratio:.2f})")
    total_weight = sum(contrib.weight for contrib in adjusted)
    if total_weight > 0:
        for contrib in adjusted:
            contrib.weight /= total_weight
    return adjusted, notes

def _hierarchical_priority(contributions: List, task_domain: str, context: Dict[str, Any]) -> Tuple[List, List]:
    adjusted = contributions.copy()
    notes = []
    domain_priority = self.domain_priority_map.get(task_domain, [])
    if domain_priority:
        for idx, module_name in enumerate(domain_priority):
            for contrib in adjusted:
                if contrib.module_name == module_name:
                    priority_factor = 1.0 / (idx + 1)
                    contrib.weight *= (1.0 + priority_factor * 0.5)
                    notes.append(f"基于优先级调整 {module_name} 权重(等级: {idx+1})")
    total_weight = sum(contrib.weight for contrib in adjusted)
    if total_weight > 0:
        for contrib in adjusted:
            contrib.weight /= total_weight
    return adjusted, notes

def _weighted_consensus(contributions: List, task_domain: str, context: Dict[str, Any]) -> Tuple[List, List]:
    adjusted = contributions.copy()
    notes = []
    for contrib in adjusted:
        effective = contrib.confidence * contrib.reliability * contrib.relevance
        contrib.weight = effective
    total = sum(contrib.weight for contrib in adjusted)
    if total > 0:
        for contrib in adjusted:
            contrib.weight /= total
            notes.append(f"{contrib.module_name} 权重: {contrib.weight:.3f}")
    return adjusted, notes

def _contextual_adjustment(contributions: List, task_domain: str, context: Dict[str, Any]) -> Tuple[List, List]:
    adjusted = contributions.copy()
    notes = []
    urgency = context.get("urgency", "normal")
    if urgency == "high":
        fast_modules = ["military_strategy", "sufu_wisdom", "yangming_xinxue"]
        for contrib in adjusted:
            if contrib.module_name in fast_modules:
                contrib.weight *= 1.5
                notes.append(f"紧迫任务,提升 {contrib.module_name} 权重")
    elif urgency == "low":
        deep_modules = ["science_thinking", "dewey_thinking", "anthropology_wisdom"]
        for contrib in adjusted:
            if contrib.module_name in deep_modules:
                contrib.weight *= 1.3
                notes.append(f"宽松任务,提升 {contrib.module_name} 权重")
    user_role = context.get("user_role", "general")
    if user_role == "leader":
        leader_modules = ["sufu_wisdom", "ru_wisdom", "hongming_wisdom", "civilization_wisdom", "dao_wisdom"]
        for contrib in adjusted:
            if contrib.module_name in leader_modules:
                contrib.weight *= 1.4
                notes.append(f"领导者角色,提升 {contrib.module_name} 权重")
    elif user_role == "practitioner":
        practice_modules = ["military_strategy", "behavior_shaping", "growth_engine"]
        for contrib in adjusted:
            if contrib.module_name in practice_modules:
                contrib.weight *= 1.3
                notes.append(f"执行者角色,提升 {contrib.module_name} 权重")
    domain_boost = {
        "business": ["growth_engine", "social_science", "sufu_wisdom"],
        "strategy": ["military_strategy", "sufu_wisdom", "civilization_war_economy"],
        "culture": ["ru_wisdom", "hongming_wisdom", "literary_narrative"],
        "personal": ["yangming_xinxue", "dao_wisdom", "behavior_shaping"],
        "analysis": ["science_thinking", "dewey_thinking", "top_thinking"],
    }
    domain_modules = domain_boost.get(task_domain, [])
    for contrib in adjusted:
        if contrib.module_name in domain_modules:
            contrib.weight *= 1.25
            notes.append(f"领域匹配,提升 {contrib.module_name} 权重(领域: {task_domain})")
    total = sum(contrib.weight for contrib in adjusted)
    if total > 0:
        for contrib in adjusted:
            contrib.weight /= total
    return adjusted, notes

class ConflictResolver:
    def __init__(self):
        self.conflict_resolution_strategies = {
            "consensus_building": _consensus_building,
            "hierarchical_priority": _hierarchical_priority,
            "weighted_consensus": _weighted_consensus,
            "contextual_adjustment": _contextual_adjustment
        }
        self.domain_priority_map = {
            "strategic": ["sufu_wisdom", "military_strategy", "dao_wisdom"],
            "tactical": ["military_strategy", "sufu_wisdom", "dao_wisdom"],
            "ethical": ["ru_wisdom", "sufu_wisdom", "hongming_wisdom"],
            "cultural": ["hongming_wisdom", "ru_wisdom", "sufu_wisdom"],
            "natural": ["dao_wisdom", "sufu_wisdom", "ru_wisdom"]
        }

    def resolve_conflicts(self, contributions: List, task_domain: str, context: Dict[str, Any]) -> Tuple[List, List]:
        return resolve_conflicts(self, contributions, task_domain, context)
