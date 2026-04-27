"""global_wisdom_scheduler execution methods v1.0"""
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Any, Optional, Tuple
from ._gws_base import WisdomQuery, SchedulerConfig, SchoolOutput, ScheduledResult

__all__ = [
    'get_statistics',
    'schedule',
]

logger = logging.getLogger(__name__)

def schedule(self, query: WisdomQuery) -> ScheduledResult:
    from ._gws_base import ScheduledResult
    import datetime as dt
    import json
    import time as tme
    start_time = dt.datetime.now()
    abs_start = tme.time()
    step_times = {}
    query_id = query.query_id or _uuid()[:8]
    try:
        # [v22.5 性能监控] 各阶段耗时记录
        t_activate = None
        t_call = None
        t_fuse = None

        # [v22.5 调度优化] 缓存神经网络激活结果
        # 生成缓存键：基于 query_text 和 context（排序后的 JSON）
        context_sorted = sorted(query.context.items()) if query.context else []
        cache_key = (query.query_text, json.dumps(context_sorted))
        cache_hit = False
        t0 = tme.time()
        if cache_key in self._activation_cache:
            activations = self._activation_cache[cache_key]
            cache_hit = True
            self._activation_cache_hits += 1
        else:
            activations = self.network.activate_network(query.query_text, query.context)
            # 更新缓存，控制大小
            if len(self._activation_cache) >= self._max_activation_cache_size:
                # 删除最早的一个条目（简单FIFO）
                try:
                    oldest_key = next(iter(self._activation_cache))
                    del self._activation_cache[oldest_key]
                except StopIteration:
                    pass
            self._activation_cache[cache_key] = activations
            self._activation_cache_misses += 1
        step_times["activate"] = tme.time() - t0

        t0 = tme.time()
        activated = self.network.get_activated_neurons(activations, query.config.activation_threshold)
        activated = self._apply_rules(activated, query)
        step_times["prepare"] = tme.time() - t0

        t0 = tme.time()
        school_outputs = self._call_schools(activated[:query.config.max_activated_schools], query)
        step_times["call_schools"] = tme.time() - t0

        t0 = tme.time()
        fused_wisdom = self._fuse_wisdom(school_outputs, query)
        integrated_insight = self._generate_insight(school_outputs, fused_wisdom)
        step_times["fuse"] = tme.time() - t0

        network_insights = self.network.get_network_insights(activations)
        coverage = len(school_outputs) / max(1, len(self.registry.list_registered()))
        confidence = sum(s.confidence for s in school_outputs) / max(1, len(school_outputs))
        diversity = network_insights.get("diversity", 0)
        synergy = self._calculate_synergy(school_outputs)
        processing_time = (dt.datetime.now() - start_time).total_seconds()
        step_times["total"] = tme.time() - abs_start

        # [v22.5 性能监控] 统计超时/跳过的学派数量
        timeout_count = sum(1 for o in school_outputs if o.processing_time >= getattr(query.config, 'max_wait_time', 12.0))

        result = ScheduledResult(
            query_id=query_id, query_text=query.query_text, success=True,
            activated_schools=school_outputs, fused_wisdom=fused_wisdom,
            integrated_insight=integrated_insight, network_insights=network_insights,
            synergy_score=synergy, coverage=coverage, confidence=confidence,
            diversity=diversity, processing_time=processing_time,
            step_times=step_times,
            cache_stats={
                "activation_cache_hits": self._activation_cache_hits,
                "activation_cache_misses": self._activation_cache_misses,
                "cache_hit": cache_hit,
            },
            timeout_count=timeout_count,
        )
        self._record_query(query, result)
        return result
    except Exception as e:
        logger.error(f"调度失败: {e}")
        return ScheduledResult(
            query_id=query_id, query_text=query.query_text, success=False,
            activated_schools=[], fused_wisdom={},
            integrated_insight="处理失败",
            synergy_score=0, coverage=0, confidence=0, diversity=0,
            processing_time=(dt.datetime.now() - start_time).total_seconds()
        )

def _uuid() -> str:
    import uuid
    return str(uuid.uuid4())

def _apply_rules(self, activated: List[Tuple[str, float]], query: WisdomQuery) -> List[Tuple[str, float]]:
    result = activated.copy()
    for school_id in query.required_schools:
        if not any(s == school_id for s, _ in result):
            result.append((school_id, 1.0))
    result = [(s, a) for s, a in result if s not in query.excluded_schools]
    result.sort(key=lambda x: x[1], reverse=True)
    return result

_executor = None

def _get_executor():
    global _executor
    if _executor is None:
        _executor = ThreadPoolExecutor(max_workers=6, thread_name_prefix="wisdom_")
    return _executor

def _call_schools(self, activated: List[Tuple[str, float]], query: WisdomQuery) -> List[SchoolOutput]:
    if not activated:
        return []
    import datetime as dt

    def _invoke_one(school_id, activation_level):
        start_time = dt.datetime.now()
        try:
            engine = self.registry.get_engine(school_id)
            if engine is None:
                output = self._default_school_output(school_id, query.query_text)
            else:
                output = self._call_engine(engine, school_id, query)
            processing_time = (dt.datetime.now() - start_time).total_seconds()
            school_info = self.network.WISDOM_SCHOOLS.get(school_id, {})
            return SchoolOutput(
                school_id=school_id, school_name=school_info.get("name", school_id),
                activation_level=activation_level, output=output,
                confidence=activation_level, processing_time=processing_time,
                insights=self._extract_insights(output), warnings=self._extract_warnings(output)
            )
        except Exception as e:
            logger.warning(f"调用 {school_id} 失败: {e}")
            return SchoolOutput(
                school_id=school_id, school_name=school_id, activation_level=activation_level,
                output={"error": "操作失败"}, confidence=0, processing_time=0,
                warnings=["处理异常"]
            )

    outputs = []
    futures = {}
    executor = _get_executor()
    for school_id, activation_level in activated:
        future = executor.submit(_invoke_one, school_id, activation_level)
        futures[future] = school_id

    # [v22.5 去阻塞优化] 使用配置的超时时间，超时返回部分结果
    import time
    max_wait = getattr(query.config, 'max_wait_time', 12.0)
    deadline = time.time() + max_wait

    for future in as_completed(futures, timeout=max(0.5, max_wait)):
        try:
            remaining = max(0.1, deadline - time.time())
            result = future.result(timeout=remaining)
            if result:
                outputs.append(result)
        except Exception as e:
            school_id = futures[future]
            logger.warning(f"学派 {school_id} 超时或异常: {e}")
            outputs.append(SchoolOutput(
                school_id=school_id, school_name=school_id, activation_level=0,
                output={"error": "操作失败"}, confidence=0, processing_time=max_wait,
                warnings=["超时或异常"]
            ))

    # [v22.5 去阻塞] 超时后，未完成的任务记录为超时
    done_futures = set()
    for future in futures:
        if future.done():
            done_futures.add(future)
    unfinished = set(futures.keys()) - done_futures
    if unfinished:
        for fut in unfinished:
            school_id = futures[fut]
            outputs.append(SchoolOutput(
                school_id=school_id, school_name=school_id, activation_level=0,
                output={"error": "timeout"}, confidence=0,
                processing_time=max_wait,
                warnings=[f"[去阻塞] 学派 {school_id} 在 {max_wait}s 内未完成，已跳过"]
            ))
            logger.warning(f"[去阻塞] 学派 {school_id} 超时（>{max_wait}s），已跳过")

    return outputs

def _call_engine(self, engine: Any, school_id: str, query: WisdomQuery) -> Dict[str, Any]:
    """[修复] 统一引擎接口context处理，确保所有引擎都能接收上下文"""
    context = query.context or {}
    
    if hasattr(engine, 'analyze'):
        # 优先传递context参数
        try:
            raw_output = engine.analyze(query.query_text, context)
        except TypeError:
            # 如果不支持context，降级到仅传递query_text
            raw_output = engine.analyze(query.query_text)
    elif hasattr(engine, 'wisdom_analysis'):
        # wisdom_analysis可能只支持query_text，但尝试传递context
        try:
            raw_output = engine.wisdom_analysis(query.query_text, context)
        except TypeError:
            raw_output = engine.wisdom_analysis(query.query_text)
    elif hasattr(engine, 'get_insight'):
        raw_output = engine.get_insight(query.query_text, context)
    elif hasattr(engine, 'analyze_problem'):
        # analyze_problem不支持context，传递额外信息
        raw_output = engine.analyze_problem(query.query_text, context)
    else:
        raw_output = {"status": "ok", "message": f"{school_id} 引擎已调用", "context_used": bool(context)}
    return self._normalize_engine_output(raw_output, school_id)

def _normalize_engine_output(self, output: Any, school_id: str) -> Dict[str, Any]:
    from dataclasses import is_dataclass, asdict
    if output is None:
        return {"status": "empty", "school": school_id, "message": f"{school_id} 未返回内容", "insights": [], "action_items": [], "risk_warnings": []}
    if isinstance(output, dict):
        normalized = dict(output)
    elif is_dataclass(output):
        normalized = asdict(output)
    elif hasattr(output, "__dict__"):
        normalized = dict(vars(output))
    else:
        normalized = {"status": "normalized", "school": school_id, "message": str(output), "insights": [str(output)], "action_items": [], "risk_warnings": []}
    normalized.setdefault("status", "ok")
    normalized.setdefault("school", school_id)
    primary_insight = normalized.get("primary_insight")
    if primary_insight and "insights" not in normalized:
        normalized["insights"] = [primary_insight]
    elif primary_insight and isinstance(normalized.get("insights"), list) and primary_insight not in normalized["insights"]:
        normalized["insights"].insert(0, primary_insight)
    for list_key in ("insights", "action_items", "risk_warnings", "warnings"):
        value = normalized.get(list_key)
        if value is None:
            normalized[list_key] = []
        elif isinstance(value, str):
            normalized[list_key] = [value]
    return normalized

def _default_school_output(self, school_id: str, query: str) -> Dict[str, Any]:
    school_info = self.network.WISDOM_SCHOOLS.get(school_id, {})
    return {"school": school_info.get("name", school_id), "tag": school_info.get("tag", ""), "keywords": school_info.get("keywords", []), "message": f"基于{school_info.get('name', school_id)}智慧的分析", "status": "default"}

def _extract_insights(self, output: Dict[str, Any]) -> List[str]:
    insights = []
    if isinstance(output, dict):
        if "insights" in output:
            insights.extend(output["insights"] if isinstance(output["insights"], list) else [output["insights"]])
        if "advice" in output:
            insights.append(output["advice"])
        if "recommendation" in output:
            insights.append(output["recommendation"])
        if "guidance" in output:
            insights.append(output["guidance"])
    return insights[:5]

def _extract_warnings(self, output: Dict[str, Any]) -> List[str]:
    warnings = []
    if isinstance(output, dict):
        if "warnings" in output:
            warnings.extend(output["warnings"] if isinstance(output["warnings"], list) else [output["warnings"]])
        if "risk_warnings" in output:
            warnings.extend(output["risk_warnings"])
    return warnings[:3]

def _fuse_wisdom(self, outputs: List[SchoolOutput], query: WisdomQuery) -> Dict[str, Any]:
    import datetime as dt
    fused = {"schools_contributed": [o.school_id for o in outputs], "total_schools": len(outputs), "fusion_timestamp": dt.datetime.now().isoformat()}
    all_advice, all_warnings, all_insights = [], [], []
    for output in outputs:
        if "advice" in output.output:
            advice = output.output["advice"]
            all_advice.extend(advice if isinstance(advice, list) else [advice])
        all_warnings.extend(output.warnings)
        all_insights.extend(output.insights)
    fused["advice"] = list(dict.fromkeys(all_advice))[:10]
    fused["warnings"] = list(dict.fromkeys(all_warnings))[:5]
    fused["insights"] = list(dict.fromkeys(all_insights))[:15]
    return fused

def _generate_insight(self, outputs: List[SchoolOutput], fused: Dict[str, Any]) -> str:
    if not outputs:
        return "暂无足够智慧支持"
    school_names = [o.school_name for o in outputs[:3]]
    insight_parts = [f"本次分析汇聚了 {len(outputs)} 个智慧学派的力量:{', '.join(school_names)}", ""]
    if fused.get("insights"):
        insight_parts.append("核心洞察:")
        for i, insight in enumerate(fused["insights"][:3], 1):
            insight_parts.append(f"  {i}. {insight}")
    if fused.get("warnings"):
        insight_parts.append("")
        insight_parts.append("需要关注:")
        for warning in fused["warnings"][:2]:
            insight_parts.append(f"  - {warning}")
    insight_parts.append("")
    insight_parts.append(f"置信度:{sum(o.confidence for o in outputs) / len(outputs):.1%}")
    return "\n".join(insight_parts)

def _calculate_synergy(self, outputs: List[SchoolOutput]) -> float:
    if len(outputs) < 2:
        return 0.5
    return min(1.0, sum(o.activation_level * o.confidence for o in outputs) / len(outputs) * 1.5)

def _record_query(self, query: WisdomQuery, result: ScheduledResult):
    self.total_queries += 1
    record = {"query_id": result.query_id, "query_text": query.query_text[:100], "schools_activated": len(result.activated_schools), "success": result.success, "timestamp": result.timestamp.isoformat()}
    self.query_history.append(record)
    if len(self.query_history) > 100:
        self.query_history = self.query_history[-100:]

def get_statistics(self) -> Dict[str, Any]:
    return {"total_queries": self.total_queries, "registered_engines": len(self.registry.list_registered()), "recent_queries": len(self.query_history), "network_neurons": len(self.network.neurons)}
