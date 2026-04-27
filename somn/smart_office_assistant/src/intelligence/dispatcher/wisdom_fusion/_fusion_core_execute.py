"""wisdom_fusion core execute methods v1.0"""
import logging
import time
from collections import defaultdict
from typing import Dict, List, Any, Optional, Set

__all__ = [
    'fuse_wisdom',
    'get_fusion_insights',
]

logger = logging.getLogger(__name__)

def fuse_wisdom(self, task_type: str, problem: str, context: Dict[str, Any]):
    from ._fusion_enums import FusionResult
    from ._fusion_conflict import ConflictResolver
    start_time = time.time()
    task_id = f"fusion_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}"
    logger.info(f"开始智慧fusion任务: {task_id} - {task_type}")
    try:
        selected_modules = self._select_modules_for_task(task_type, context)
        if not selected_modules:
            return FusionResult(
                task_id=task_id, success=False, fused_output="未找到合适的智慧系统",
                contributions=[], fusion_method=self.config.method, warnings=["无可用智慧系统"]
            )
        contributions = []
        for module_name in selected_modules:
            contribution = self._execute_wisdom_module(module_name, task_type, problem, context)
            if contribution:
                contributions.append(contribution)
        if not contributions:
            return FusionResult(
                task_id=task_id, success=False, fused_output="所有智慧系统执行失败",
                contributions=[], fusion_method=self.config.method, warnings=["智慧系统执行失败"]
            )
        for contrib in contributions:
            contrib.weight = self._calculate_initial_weight(contrib.module_name, task_type, context)
        if self.config.enable_conflict_resolution:
            if self.conflict_resolver is None:
                self.conflict_resolver = ConflictResolver()
            domain = context.get("domain", "general")
            contributions, conflict_notes = self.conflict_resolver.resolve_conflicts(contributions, domain, context)
        else:
            conflict_notes = []
        fused_output = self._apply_fusion_method(contributions, task_type, problem, context)
        fusion_confidence = self._calculate_fusion_confidence(contributions)
        consistency = self._calculate_consistency_score(contributions)
        diversity = self._calculate_diversity_score(contributions)
        suggestions = self._generate_suggestions(contributions, context)
        execution_time = time.time() - start_time
        result = FusionResult(
            task_id=task_id, success=True, fused_output=fused_output,
            contributions=contributions, fusion_method=self.config.method,
            confidence=fusion_confidence, consistency_score=consistency,
            diversity_score=diversity, execution_time=execution_time,
            suggestions=suggestions, warnings=conflict_notes
        )
        if self.config.enable_learning:
            self._record_fusion_experience(task_id, task_type, contributions, result, context)
        logger.info(f"智慧fusion完成: {task_id} - 置信度: {fusion_confidence:.2f} - 耗时: {execution_time:.2f}s")
        return result
    except Exception as e:
        logger.error(f"智慧fusion失败: {task_id} - {str(e)}")
        return FusionResult(
            task_id=task_id, success=False, fused_output="fusion异常",
            contributions=[], fusion_method=self.config.method, warnings=["执行异常"]
        )

def _select_modules_for_task(self, task_type: str, context: Dict[str, Any]) -> List[str]:
    suitable_modules = []
    for module_name, module_info in self.wisdom_modules.items():
        capabilities = module_info.get("capabilities", [])
        domains = module_info.get("domains", [])
        if task_type in capabilities:
            context_domain = context.get("domain", "general")
            if context_domain in domains or "general" in domains:
                capability_score = 1.0
                domain_relevance = self._calculate_domain_relevance(module_name, context_domain)
                historical_performance = self._get_module_performance(module_name, task_type)
                total_score = (capability_score * 0.4 + domain_relevance * 0.3 + historical_performance * 0.3)
                suitable_modules.append((module_name, total_score))
    suitable_modules.sort(key=lambda x: x[1], reverse=True)
    return [mod[0] for mod in suitable_modules[:4]]

def _execute_wisdom_module(self, module_name: str, task_type: str, problem: str, context: Dict[str, Any]):
    from ._fusion_enums import WisdomContribution
    module_info = self.wisdom_modules.get(module_name)
    if not module_info or module_info["module"] is None:
        return None
    module = module_info["module"]
    try:
        if module_name == "sufu_wisdom":
            output = module.make_decision(problem, self._select_sufu_principle(problem, context))
        elif module_name == "military_strategy":
            output = module.analyze_situation(problem)
        elif module_name == "dao_wisdom":
            output = module.seek_harmony(problem)
        elif module_name == "ru_wisdom":
            output = module.apply_ethic(problem, context.get("ethical_focus", "general"))
        elif module_name == "hongming_wisdom":
            output = module.analyze_cross_culture(problem, context)
        else:
            if hasattr(module, "process"):
                output = module.process({"problem": problem, "context": context})
            else:
                output = f"{module_name} 分析完成"
        confidence = self._estimate_confidence(module_name, task_type, problem)
        relevance = self._calculate_relevance(module_name, task_type, context)
        return WisdomContribution(module_name=module_name, output=output, confidence=confidence, relevance=relevance, reliability=0.8)
    except Exception as e:
        logger.warning(f"智慧模块执行失败: {module_name} - {str(e)}")
        return None

def _select_sufu_principle(self, problem: str, context: Dict[str, Any]) -> str:
    if "道德" in problem or "伦理" in problem:
        return "德"
    elif "仁爱" in problem or "关怀" in problem:
        return "仁"
    elif "正义" in problem or "公平" in problem:
        return "义"
    elif "礼仪" in problem or "规范" in problem:
        return "礼"
    else:
        return "道"

def _estimate_confidence(self, module_name: str, task_type: str, problem: str) -> float:
    base_confidence = 0.7
    if len(problem) > 100:
        complexity_factor = 0.9
    elif len(problem) < 30:
        complexity_factor = 0.5
    else:
        complexity_factor = 0.7
    module_adjustment = {
        "sufu_wisdom": 1.0, "military_strategy": 0.9,
        "dao_wisdom": 0.8, "ru_wisdom": 0.9, "hongming_wisdom": 0.8
    }.get(module_name, 0.8)
    confidence = base_confidence * complexity_factor * module_adjustment
    return min(0.95, max(0.3, confidence))

def _calculate_relevance(self, module_name: str, task_type: str, context: Dict[str, Any]) -> float:
    base_relevance = 0.7
    domain = context.get("domain", "general")
    domain_mapping = self._calculate_domain_relevance(module_name, domain)
    capabilities = self.wisdom_modules.get(module_name, {}).get("capabilities", [])
    capability_relevance = 1.0 if task_type in capabilities else 0.3
    relevance = (base_relevance * 0.4 + domain_mapping * 0.3 + capability_relevance * 0.3)
    return min(0.95, max(0.3, relevance))

def _calculate_initial_weight(self, module_name: str, task_type: str, context: Dict[str, Any]) -> float:
    default_weights = self.config.default_weights.get(task_type, {})
    base_weight = default_weights.get(module_name, 0.2)
    domain = context.get("domain", "general")
    domain_relevance = self._calculate_domain_relevance(module_name, domain)
    problem_complexity = self._estimate_problem_complexity(context)
    final_weight = (base_weight * 0.5 + domain_relevance * 0.3 + (1.0 - problem_complexity) * 0.2)
    return max(0.05, min(0.4, final_weight))

def _apply_fusion_method(self, contributions: List, task_type: str, problem: str, context: Dict[str, Any]):
    from ._fusion_enums import FusionMethod
    method = self.config.method
    if method == FusionMethod.WEIGHTED_AVERAGE:
        return self._weighted_average_fusion(contributions)
    elif method == FusionMethod.MAJORITY_VOTE:
        return self._majority_vote_fusion(contributions)
    elif method == FusionMethod.META_LEARNING:
        return self._meta_learning_fusion(contributions, task_type, problem, context)
    elif method == FusionMethod.ADAPTIVE:
        return self._adaptive_fusion(contributions, task_type, context)
    else:
        return self._hierarchical_fusion(contributions)

def _weighted_average_fusion(self, contributions: List) -> Dict[str, Any]:
    total_effective_weight = sum(contrib.effective_weight() for contrib in contributions)
    if total_effective_weight == 0:
        return {"error": "无有效贡献"}
    result = {
        "wisdom_sources": [contrib.module_name for contrib in contributions],
        "contributions": [],
        "primary_recommendation": "",
        "confidence_breakdown": {}
    }
    for contrib in contributions:
        effective_weight = contrib.effective_weight() / total_effective_weight
        result["contributions"].append({
            "module": contrib.module_name, "output": contrib.output,
            "effective_weight": effective_weight, "confidence": contrib.confidence, "relevance": contrib.relevance
        })
        result["confidence_breakdown"][contrib.module_name] = {
            "weight": effective_weight, "confidence": contrib.confidence, "reliability": contrib.reliability
        }
    if result["contributions"]:
        top_contrib = max(result["contributions"], key=lambda x: x["effective_weight"])
        result["primary_recommendation"] = top_contrib["output"]
    return result

def _majority_vote_fusion(self, contributions: List) -> Dict[str, Any]:
    suggestion_counts = defaultdict(int)
    for contrib in contributions:
        output_str = str(contrib.output)
        key = output_str[:20] if len(output_str) > 20 else output_str
        suggestion_counts[key] += 1
    if not suggestion_counts:
        return {"error": "无有效建议"}
    top_suggestion = max(suggestion_counts.items(), key=lambda x: x[1])
    return {
        "top_suggestion": top_suggestion[0], "support_count": top_suggestion[1],
        "total_contributions": len(contributions),
        "consensus_ratio": top_suggestion[1] / len(contributions),
        "all_suggestions": list(suggestion_counts.keys())
    }

def _meta_learning_fusion(self, contributions: List, task_type: str, problem: str, context: Dict[str, Any]) -> Dict[str, Any]:
    scores = {}
    for contrib in contributions:
        score = (contrib.confidence * 0.4 + contrib.relevance * 0.3 + contrib.reliability * 0.3)
        scores[contrib.module_name] = score
    top_module = max(scores.items(), key=lambda x: x[1])
    other_contribs = [c for c in contributions if c.module_name != top_module[0]]
    return {
        "primary_module": top_module[0], "primary_score": top_module[1],
        "primary_output": next(c.output for c in contributions if c.module_name == top_module[0]),
        "secondary_modules": [c.module_name for c in other_contribs],
        "fusion_strategy": "meta_learning_weighted_selection", "confidence": top_module[1]
    }

def _adaptive_fusion(self, contributions: List, task_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
    complexity = self._estimate_problem_complexity(context)
    domain = context.get("domain", "general")
    if complexity > 0.7 or domain in ["strategic", "complex"]:
        return self._meta_learning_fusion(contributions, task_type, "", context)
    elif len(contributions) > 3:
        return self._weighted_average_fusion(contributions)
    else:
        return self._hierarchical_fusion(contributions)

def _hierarchical_fusion(self, contributions: List) -> Dict[str, Any]:
    sorted_contribs = sorted(contributions, key=lambda x: x.effective_weight(), reverse=True)
    hierarchy = {
        "primary": {
            "module": sorted_contribs[0].module_name if sorted_contribs else None,
            "output": sorted_contribs[0].output if sorted_contribs else None,
            "weight": sorted_contribs[0].effective_weight() if sorted_contribs else 0
        },
        "secondary": [
            {"module": contrib.module_name, "output": contrib.output, "weight": contrib.effective_weight()}
            for contrib in sorted_contribs[1:3]
        ],
        "tertiary": [
            {"module": contrib.module_name, "weight": contrib.effective_weight()}
            for contrib in sorted_contribs[3:]
        ]
    }
    return {
        "fusion_method": "hierarchical_priority", "hierarchy": hierarchy,
        "total_contributions": len(contributions),
        "primary_recommendation": sorted_contribs[0].output if sorted_contribs else None
    }

def _calculate_fusion_confidence(self, contributions: List) -> float:
    if not contributions:
        return 0.0
    total_weight = sum(contrib.effective_weight() for contrib in contributions)
    if total_weight == 0:
        return 0.0
    weighted_confidence = sum(contrib.confidence * contrib.effective_weight() for contrib in contributions)
    return weighted_confidence / total_weight

def _calculate_consistency_score(self, contributions: List) -> float:
    if len(contributions) < 2:
        return 1.0
    common_keywords = self._find_common_keywords_in_contributions(contributions)
    keyword_count = len(common_keywords)
    max_keywords = 5
    consistency = min(1.0, keyword_count / max_keywords)
    return consistency

def _find_common_keywords_in_contributions(self, contributions: List) -> Set[str]:
    all_keywords = []
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
        common_words = ["的", "了", "在", "和", "与", "是", "有", "可以", "需要"]
        filtered_words = [w for w in words if w not in common_words and len(w) >= 2]
        all_keywords.append(set(filtered_words))
    if not all_keywords:
        return set()
    return set.intersection(*all_keywords)

def _calculate_diversity_score(self, contributions: List) -> float:
    if not contributions:
        return 0.0
    outputs = [str(contrib.output) for contrib in contributions]
    unique_outputs = len(set(outputs))
    total_outputs = len(outputs)
    return unique_outputs / total_outputs

def _generate_suggestions(self, contributions: List, context: Dict[str, Any]) -> List[str]:
    suggestions = []
    for contrib in contributions:
        if contrib.confidence > 0.8 and contrib.relevance > 0.7:
            suggestion = f"基于{contrib.module_name}的分析,建议关注其核心观点"
            suggestions.append(suggestion)
    if len(contributions) >= 3:
        suggestions.append("多个智慧系统达成共识,建议采纳共同建议")
    if len(contributions) > 0:
        avg_confidence = sum(c.confidence for c in contributions) / len(contributions)
        if avg_confidence < 0.6:
            suggestions.append("整体置信度偏低,建议谨慎采纳")
    return suggestions

def _record_fusion_experience(self, task_id: str, task_type: str, contributions: List, result, context: Dict[str, Any]):
    experience = {
        "task_id": task_id, "task_type": task_type,
        "context_summary": {
            "domain": context.get("domain", "general"),
            "complexity": self._estimate_problem_complexity(context),
            "industry": context.get("industry", "general")
        },
        "contributions_summary": [
            {"module": c.module_name, "confidence": c.confidence, "relevance": c.relevance, "effective_weight": c.effective_weight()}
            for c in contributions
        ],
        "result_summary": {
            "success": result.success, "final_confidence": result.confidence,
            "consistency": result.consistency_score, "diversity": result.diversity_score
        },
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }
    self.fusion_history.append(experience)
    if len(self.fusion_history) > 1000:
        self.fusion_history = self.fusion_history[-500:]
    for contrib in contributions:
        if contrib.module_name in self.wisdom_modules:
            module_info = self.wisdom_modules[contrib.module_name]
            performance_factor = (contrib.confidence * 0.5 + contrib.relevance * 0.5)
            module_info["weight_adjustment"] = 0.9 * module_info.get("weight_adjustment", 1.0) + 0.1 * performance_factor

def get_fusion_insights(self, task_type: Optional[str] = None) -> Dict[str, Any]:
    insights = {
        "total_fusion_tasks": len(self.fusion_history),
        "success_rate": 0.0, "average_confidence": 0.0,
        "module_performance": {}, "fusion_patterns": {}
    }
    if not self.fusion_history:
        return insights
    successful_tasks = sum(1 for exp in self.fusion_history if exp.get("result_summary", {}).get("success", False))
    insights["success_rate"] = successful_tasks / len(self.fusion_history)
    confidences = [exp.get("result_summary", {}).get("final_confidence", 0.0) for exp in self.fusion_history]
    insights["average_confidence"] = sum(confidences) / len(confidences) if confidences else 0.0
    module_stats = defaultdict(lambda: {"count": 0, "total_confidence": 0.0})
    for exp in self.fusion_history:
        for contrib in exp.get("contributions_summary", []):
            module_name = contrib.get("module", "")
            confidence = contrib.get("confidence", 0.0)
            module_stats[module_name]["count"] += 1
            module_stats[module_name]["total_confidence"] += confidence
    for module_name, stats in module_stats.items():
        avg_confidence = stats["total_confidence"] / stats["count"] if stats["count"] > 0 else 0.0
        insights["module_performance"][module_name] = {"usage_count": stats["count"], "average_confidence": round(avg_confidence, 3)}
    if task_type:
        relevant_history = [exp for exp in self.fusion_history if exp.get("task_type") == task_type]
        insights["fusion_patterns"][task_type] = {
            "count": len(relevant_history),
            "average_confidence": round(
                sum(exp.get("result_summary", {}).get("final_confidence", 0.0) for exp in relevant_history) / len(relevant_history), 3
            ) if relevant_history else 0.0,
        }
    return insights
