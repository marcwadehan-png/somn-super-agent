# -*- coding: utf-8 -*-
"""
ClawsCoordinator - 多Claw任务协调器
===================================

Phase 4: Gateway调度器 + 多Claw协作机制。

功能:
- Gateway意图路由：根据用户输入分发到最合适的Claw
- YAML配置批量加载：从configs/目录初始化所有可用Claw
- 多Claw协作：支持主Claw+子Claw的任务委派模式
- 负载均衡：避免单Claw过载
- 全局状态监控

架构:
                    用户输入
                        │
                  ┌─────▼─────┐
                  │  Gateway   │ ← 意图识别 + 触发词匹配
                  │ Dispatcher │
                  └──┬────┬───┘
           ┌──────────┘    └──────────┐
           ▼                          ▼
    ┌─────────────┐          ┌─────────────┐
    │  Claw A     │◄──►│  Claw B     │
    │  (主Agent)  │  协作   │ (子Agent)   │
    └─────────────┘          └─────────────┘

版本: v1.0.0
创建: 2026-04-22
"""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum

from ._claw_architect import (
    ClawArchitect,
    ClawMetadata,
    ClawStatus,
    ReActResult,
    load_claw_config,
    list_all_configs,
    create_claw,
    ClawLoadError,  # [v10.3] 用于懒加载失败检测
)

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# 路由策略
# ═══════════════════════════════════════════════════════════════

class RouteStrategy(Enum):
    """路由策略"""
    TRIGGER_MATCH = "trigger_match"       # 触发词匹配（默认）
    SINGLE_BEST = "single_best"           # 单最佳匹配
    MULTI_COLLABORATIVE = "multi_collaborative"  # 多Claw协作
    ROUND_ROBIN = "round_robin"           # 轮询
    MANUAL = "manual"                     # 手动指定
    SCHOOL_BASED = "school_based"         # 基于学派路由
    FALLBACK = "fallback"                 # 回退策略 [v10.3 新增]


@dataclass
class RouteDecision:
    """路由决策结果"""
    primary: str              # 主Claw名称
    collaborators: List[str]  # 协作Claw列表
    strategy: RouteStrategy
    confidence: float = 0.0
    reason: str = ""


@dataclass
class CoordinatorStats:
    """协调器统计"""
    total_requests: int = 0
    successful_routes: int = 0
    failed_routes: int = 0
    avg_response_time: float = 0.0
    claw_usage_counts: Dict[str, int] = field(default_factory=dict)
    active_claws: int = 0
    total_claws_loaded: int = 0


# ═══════════════════════════════════════════════════════════════
# Gateway 意图路由器
# ═══════════════════════════════════════════════════════════════

class GatewayRouter:
    """
    Gateway路由器。

    根据用户输入，智能选择最合适的Claw处理请求。

    匹配策略（按优先级）:
    1. 精确触发词匹配（triggers字段）
    2. 学派关键词推断
    3. 时代关键词推断
    4. 名称直接提及
    5. 默认Claw
    """

    def __init__(self, coordinator: "ClawsCoordinator"):
        self.coordinator = coordinator
        self._fallback_claw: Optional[str] = None

    def set_fallback(self, claw_name: str) -> None:
        """设置默认兜底Claw"""
        self._fallback_claw = claw_name

    def route(self, query: str, strategy: RouteStrategy = RouteStrategy.TRIGGER_MATCH) -> RouteDecision:
        """
        执行路由决策。

        Args:
            query: 用户输入文本
            strategy: 路由策略

        Returns:
            RouteDecision包含主Claw和协作者列表
        """
        claws = self.coordinator.claws
        if not claws:
            return RouteDecision(
                primary=self._fallback_claw or "",
                collaborators=[],
                strategy=strategy,
                confidence=0.0,
                reason="No claws available"
            )

        if strategy == RouteStrategy.MANUAL:
            return self._route_manual(query)

        # 策略1: 触发词匹配（主要策略）
        matches = self._match_triggers(query)

        if matches:
            primary = matches[0][0]
            collabs = [m[0] for m in matches[1:3]]  # 最多2个协作者
            return RouteDecision(
                primary=primary,
                collaborators=collabs,
                strategy=RouteStrategy.TRIGGER_MATCH,
                confidence=matches[0][1],
                reason=f"Trigger match: {primary} ({matches[0][1]:.2f})"
            )

        # 策略2: 名称直接匹配
        name_match = self._match_name(query)
        if name_match:
            return RouteDecision(
                primary=name_match,
                collaborators=[],
                strategy=RouteStrategy.SINGLE_BEST,
                confidence=0.95,
                reason=f"Direct name match: {name_match}"
            )

        # 策略3: 学派关键词匹配
        school_match = self._match_school(query)
        if school_match:
            return RouteDecision(
                primary=school_match,
                collaborators=[],
                strategy=RouteStrategy.SCHOOL_BASED,
                confidence=0.7,
                reason=f"School-based match: {school_match}"
            )

        # 兜底
        fallback = self._fallback_claw or (list(claws.keys())[0] if claws else "")
        return RouteDecision(
            primary=fallback,
            collaborators=[],
            strategy=RouteStrategy.TRIGGER_MATCH,
            confidence=0.2,
            reason="Fallback - no specific match"
        )

    def _match_triggers(self, query: str) -> List[Tuple[str, float]]:
        """
        触发词匹配。

        Returns:
            [(claw_name, score)] 按分数降序排列
        """
        query_lower = query.lower()
        scored = []

        for name, claw in self.coordinator.claws.items():
            triggers = claw.metadata.triggers
            if not triggers:
                continue

            best_score = 0.0
            for trigger in triggers:
                trigger_lower = trigger.lower()
                if trigger_lower in query_lower:
                    # ★ v1.1 修复: 分数 = 触发词长度 / 查询长度（长触发词在短查询中匹配得分更高）
                    score = len(trigger_lower) / max(len(query_lower), 1)
                    # 额外加权：更长的匹配通常更有意义
                    score *= (1.0 + len(trigger_lower) * 0.05)
                    best_score = max(best_score, score)

            if best_score > 0:
                scored.append((name, best_score))

        scored.sort(key=lambda x: -x[1])
        return scored

    def _match_name(self, query: str) -> Optional[str]:
        """检查是否直接提到了某个贤者的名字"""
        query_lower = query.lower()
        for name in self.coordinator.claws:
            if name.lower() in query_lower:
                return name
        return None

    def _match_school(self, query: str) -> Optional[str]:
        """基于学派关键词匹配最佳Claw"""
        # 学派 → 关键词映射
        SCHOOL_KEYWORDS = {
            "儒家": ["仁", "礼", "德", "君子", "孔子", "孟子", "儒家", "论语", "仁义"],
            "道家": ["道", "无为", "自然", "逍遥", "老子", "庄子", "道家", "道德经"],
            "法家": ["法", "术", "势", "法治", "韩非", "商鞅", "法家"],
            "兵家": ["兵", "战", "谋略", "孙子", "孙武", "兵法", "战争"],
            "墨家": ["兼爱", "非攻", "墨子", "墨家", "尚贤"],
            "佛学": ["佛", "禅", "菩提", "涅槃", "白玉蟾", "佛教", "禅宗"],
            "阴阳": ["阴阳", "五行", "八卦", "易经"],
        }

        query_lower = query.lower()
        best_match = None
        best_count = 0

        # 找到该学派下认知维度最高的Claw
        for school, keywords in SCHOOL_KEYWORDS.items():
            count = sum(1 for kw in keywords if kw in query_lower)
            if count > best_count:
                best_count = count
                # 在该学派中找最好的Claw
                school_claws = [
                    (n, c) for n, c in self.coordinator.claws.items()
                    if c.metadata.school == school or c.metadata.wisdom_school == school
                ]
                if school_claws:
                    # 取cog_depth最高的
                    school_claws.sort(key=lambda x: x[1].metadata.cognitive_dimensions.cog_depth, reverse=True)
                    best_match = school_claws[0][0]

        return best_match

    def _route_manual(self, query: str) -> RouteDecision:
        """手动路由：从query中解析目标claw名称"""
        target = query.strip()
        if target in self.coordinator.claws:
            return RouteDecision(
                primary=target,
                collaborators=[],
                strategy=RouteStrategy.MANUAL,
                confidence=1.0,
                reason=f"Manual route to: {target}"
            )
        return RouteDecision(
            primary=target,
            collaborators=[],
            strategy=RouteStrategy.MANUAL,
            confidence=0.0,
            reason=f"Target '{target}' not found in loaded claws"
        )


# ═══════════════════════════════════════════════════════════════
# ClawsCoordinator 主类
# ═══════════════════════════════════════════════════════════════

@dataclass
class ProcessResult:
    """处理结果（包装ReActResult，增加路由信息）"""
    query: str
    routed_to: str
    collaborators_used: List[str]
    success: bool
    react_result: Optional[ReActResult] = None
    error: str = ""
    elapsed_seconds: float = 0.0
    route_confidence: float = 0.0


class ClawsCoordinator:
    """
    多Claw任务协调器。

    用法:
        >>> coord = ClawsCoordinator()
        >>> await coord.initialize()  # 加载所有YAML配置
        >>> result = await coord.process("什么是仁？")
        >>> print(result.react_result.final_answer)

        # 或只加载指定的Claw
        >>> coord = ClawsCoordinator()
        >>> await coord.initialize(["孔子", "王阳明"])
    """

    def __init__(
        self,
        configs_dir: Optional[Any] = None,
        auto_load: bool = False,
        max_concurrent: int = 5,
    ):
        """
        Args:
            configs_dir: 配置目录路径
            auto_load: 是否在初始化时自动加载所有配置
            max_concurrent: 最大并发Claw数
        """
        self.configs_dir = configs_dir
        self.max_concurrent = max_concurrent

        # Claw注册表: {name: ClawArchitect}
        self.claws: Dict[str, ClawArchitect] = {}

        # 元数据索引（轻量，不加载完整Claw）
        self._metadata_index: Dict[str, ClawMetadata] = {}

        # 子模块
        self.gateway = GatewayRouter(self)

        # 统计
        self.stats = CoordinatorStats()

        # 信号量（限制并发）
        self._semaphore: Optional[asyncio.Semaphore] = None

        # 回调
        self._on_process_start: List[Callable] = []
        self._on_process_complete: List[Callable] = []

    async def initialize(
        self,
        names: Optional[List[str]] = None,
        lazy_load: bool = False,
    ) -> Dict[str, Any]:
        """
        初始化协调器，加载Claw配置。

        Args:
            names: 要加载的Claw名称列表。None=加载全部
            lazy_load: 是否懒加载（仅加载元数据，不创建Claw实例）

        Returns:
            初始化统计信息
        """
        start_time = time.monotonic()

        if names is None:
            names = list_all_configs(self.configs_dir)

        logger.info(f"[ClawsCoordinator] Initializing with {len(names)} claws...")

        loaded = 0
        failed = 0

        for name in names:
            try:
                meta = load_claw_config(name, self.configs_dir)
                if meta is None:
                    failed += 1
                    continue

                self._metadata_index[name] = meta

                if not lazy_load:
                    claw = create_claw(name, self.configs_dir)
                    if claw is not None:
                        self.claws[name] = claw
                        loaded += 1
                    else:
                        failed += 1
                else:
                    loaded += 1

            except Exception as e:
                logger.warning(f"[ClawsCoordinator] Failed to load {name}: {e}")
                failed += 1

        elapsed = time.monotonic() - start_time
        self.stats.total_claws_loaded = len(self.claws)
        self.stats.active_claws = len(self.claws)

        # 设置信号量
        self._semaphore = asyncio.Semaphore(self.max_concurrent)

        # 如果有孔子，设为默认兜底
        if "孔子" in self.claws:
            self.gateway.set_fallback("孔子")

        result = {
            "loaded": loaded,
            "failed": failed,
            "total": len(names),
            "lazy_mode": lazy_load,
            "elapsed_seconds": round(elapsed, 3),
            "active_claws": list(self.claws.keys())[:20],  # 显示前20个
            "total_active": len(self.claws),
        }

        logger.info(f"[ClawsCoordinator] Init complete: {loaded} loaded, {failed} failed in {elapsed:.2f}s")
        return result

    async def process(
        self,
        query: str,
        target_claw: Optional[str] = None,
        strategy: RouteStrategy = RouteStrategy.TRIGGER_MATCH,
        include_collaborators: bool = True,
        context: Optional[Dict[str, Any]] = None,
    ) -> ProcessResult:
        """
        处理用户请求的主入口。

        完整流程:
        1. Gateway路由 → 决定主Claw和协作者
        2. 主Claw执行推理
        3. （可选）协作Claw补充分析
        4. 汇总结果

        Args:
            query: 用户输入
            target_claw: 手动指定目标Claw（跳过Gateway）
            strategy: 路由策略
            include_collaborators: 是否启用多Claw协作
            context: 额外上下文

        Returns:
            ProcessResult
        """
        start_time = time.monotonic()
        self.stats.total_requests += 1

        # 触发回调
        for cb in self._on_process_start:
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb(self, query)
                else:
                    cb(self, query)
            except Exception:
                logger.debug("[ClawsCoordinator] 回调执行失败")

        try:
            # ── 路由阶段 ──
            if target_claw and target_claw in self.claws:
                decision = RouteDecision(
                    primary=target_claw,
                    collaborators=[],
                    strategy=RouteStrategy.MANUAL,
                    confidence=1.0,
                    reason=f"Manual target: {target_claw}",
                )
            else:
                decision = self.gateway.route(query, strategy)

            # 检查主Claw是否存在
            if decision.primary not in self.claws:
                # [v10.3] 尝试懒加载
                # ★ v1.2 修复: 扩大异常捕获范围，防止非 ClawLoadError 异常绕过 fallback
                try:
                    claw = create_claw(decision.primary, self.configs_dir)
                    if claw is None:
                        raise ClawLoadError(f"create_claw返回None: {decision.primary}")
                    self.claws[decision.primary] = claw
                except Exception as e:
                    logger.warning(f"[ClawsCoordinator] 懒加载 {decision.primary} 失败: {e}")
                    # [v10.3] 回退到fallback_claw
                    fallback = self.gateway._fallback_claw
                    if fallback and fallback != decision.primary:
                        logger.info(f"[ClawsCoordinator] 尝试回退到fallback: {fallback}")
                        if fallback in self.claws:
                            decision = RouteDecision(
                                primary=fallback,
                                collaborators=decision.collaborators,
                                strategy=RouteStrategy.FALLBACK,
                                confidence=decision.confidence * 0.5,
                                reason="Fallback失败",
                            )
                        else:
                            try:
                                fallback_claw = create_claw(fallback, self.configs_dir)
                                if fallback_claw:
                                    self.claws[fallback] = fallback_claw
                                    decision = RouteDecision(
                                        primary=fallback,
                                        collaborators=decision.collaborators,
                                        strategy=RouteStrategy.FALLBACK,
                                        confidence=decision.confidence * 0.5,
                                        reason=f"Lazy-loaded fallback from {decision.primary}",
                                    )
                                    logger.info(f"[ClawsCoordinator] 回退claw加载成功: {fallback}")
                                else:
                                    raise ClawLoadError(f"Fallback {fallback} 加载失败")
                            except Exception as fb_e:
                                logger.error(f"[ClawsCoordinator] 回退claw {fallback} 也失败: {fb_e}")
                                self.stats.failed_routes += 1
                                return ProcessResult(
                                    query=query,
                                    routed_to=decision.primary,
                                    collaborators_used=[],
                                    success=False,
                                    error="主Claw不可用且回退失败",
                                    elapsed_seconds=time.monotonic() - start_time,
                                    route_confidence=0.0,
                                )
                    else:
                        self.stats.failed_routes += 1
                        return ProcessResult(
                            query=query,
                            routed_to=decision.primary,
                            collaborators_used=[],
                            success=False,
                            error=f"Claw '{decision.primary}' not available (无fallback)",
                            elapsed_seconds=time.monotonic() - start_time,
                            route_confidence=0.0,
                        )

            primary_claw = self.claws[decision.primary]

            # ── 注册跨Claw协作伙伴 ──
            for collab_name in (decision.collaborators if include_collaborators else []):
                collab_claw = self.claws.get(collab_name)
                if collab_claw and collab_claw != primary_claw:
                    primary_claw.react_loop.register_collaborator(collab_name, collab_claw)

            # ── 主Claw执行 ──
            react_result = await primary_claw.process(query, context)

            # ── [v10.0 修复] 协作阶段（可选）— 带独立超时保护
            collaborators_used = []
            COLLAB_TIMEOUT = 30.0  # 协作者超时30秒（不影响主Claw结果）

            if include_collaborators and decision.collaborators:
                for collab_name in decision.collaborators:  # 支持所有协作者
                    collab_claw = self.claws.get(collab_name)
                    if collab_claw and collab_claw.status != ClawStatus.ERROR:
                        try:
                            # 协作者以"补充视角"模式运行
                            collab_context = dict(context or {})
                            collab_context["_collaboration_role"] = "supplementary"
                            collab_context["_primary_answer"] = react_result.final_answer

                            # ★ 协作者独立超时保护
                            collab_result = await asyncio.wait_for(
                                collab_claw.process(
                                    f"请从{collab_claw.metadata.school}学派视角补充分析：{query}",
                                    collab_context,
                                ),
                                timeout=COLLAB_TIMEOUT
                            )
                            collaborators_used.append(collab_name)
                            # 将协作结果追加到主结果
                            if collab_result.success and collab_result.final_answer:
                                react_result.final_answer += (
                                    f"\n\n--- 【{collab_name}的{collab_claw.metadata.school}学派补充】 ---\n"
                                    f"{collab_result.final_answer[:500]}"
                                )
                        except asyncio.TimeoutError:
                            logger.warning(f"[ClawsCoordinator] Collaborator {collab_name} 超时({COLLAB_TIMEOUT}s)")
                        except Exception as e:
                            logger.warning(f"[ClawsCoordinator] Collaborator {collab_name} error: {e}")

            # ── 汇总结果 ──
            elapsed = time.monotonic() - start_time
            self.stats.successful_routes += 1
            self.stats.avg_response_time = (
                (self.stats.avg_response_time * (self.stats.successful_routes - 1) + elapsed)
                / self.stats.successful_routes
            )
            self.stats.claw_usage_counts[decision.primary] = \
                self.stats.claw_usage_counts.get(decision.primary, 0) + 1

            result = ProcessResult(
                query=query,
                routed_to=decision.primary,
                collaborators_used=collaborators_used,
                success=react_result.success,
                react_result=react_result,
                error=react_result.reason if not react_result.success else "",
                elapsed_seconds=elapsed,
                route_confidence=decision.confidence,
            )

        except Exception as e:
            elapsed = time.monotonic() - start_time
            self.stats.failed_routes += 1
            result = ProcessResult(
                query=query,
                routed_to=target_claw or "unknown",
                collaborators_used=[],
                success=False,
                error="执行失败",
                elapsed_seconds=elapsed,
            )

        # 触发完成回调
        for cb in self._on_process_complete:
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb(self, result)
                else:
                    cb(self, result)
            except Exception:
                logger.debug("[ClawsCoordinator] 完成回调执行失败")

        return result

    # ★ v10.0 修复: 批量处理超时保护
    BATCH_TIMEOUT_SECONDS = 300  # 单批次最大超时5分钟

    async def process_batch(
        self,
        queries: List[str],
        target_claw: Optional[str] = None,
        max_concurrent: Optional[int] = None,
        timeout_per_item: float = 60.0,  # 每个查询的超时
    ) -> List[ProcessResult]:
        """
        [v10.0 修复] 批量处理多个查询（并发执行，带超时保护）。

        Args:
            queries: 查询列表
            target_claw: 目标Claw（可选）
            max_concurrent: 并发上限
            timeout_per_item: 每个查询的超时时间（秒），默认60s

        Returns:
            结果列表（超时项返回错误结果）
        """
        sem = asyncio.Semaphore(max_concurrent or self.max_concurrent)

        async def _process_one(q: str) -> ProcessResult:
            async with sem:
                try:
                    # ★ 每个查询独立超时保护
                    return await asyncio.wait_for(
                        self.process(q, target_claw=target_claw),
                        timeout=timeout_per_item
                    )
                except asyncio.TimeoutError:
                    logger.warning(f"[process_batch] 单项超时({timeout_per_item}s): {q[:50]}")
                    return ProcessResult(
                        query=q,
                        routed_to=target_claw or "unknown",
                        collaborators_used=[],
                        success=False,
                        error=f"单项处理超时({timeout_per_item}s)",
                        elapsed_seconds=timeout_per_item,
                        route_confidence=0.0,
                    )

        tasks = [_process_one(q) for q in queries]

        # ★ v1.2 修复: 将协程对象包装为 Task，再传给 asyncio.wait
        # Python 3.11+ 不允许直接向 wait() 传递协程对象
        task_list = [asyncio.create_task(t) for t in tasks]

        # ★ v1.1 修复: 整体批次超时保护（使用 wait 保留已完成结果）
        try:
            done, pending = await asyncio.wait(
                task_list, timeout=self.BATCH_TIMEOUT_SECONDS
            )
            # ★ v1.2 修复: cancel 后必须 await，避免 "Task was destroyed but it is pending" 警告
            for p in pending:
                p.cancel()
            if pending:
                await asyncio.gather(*pending, return_exceptions=True)
            # 收集已完成的结果
            processed = []
            for t in done:
                try:
                    r = t.result()
                    if isinstance(r, ProcessResult):
                        processed.append(r)
                    elif isinstance(r, Exception):
                        processed.append(ProcessResult(
                            query="(unknown)",
                            routed_to=target_claw or "unknown",
                            collaborators_used=[],
                            success=False,
                            error=str(r)[:200],
                            elapsed_seconds=0.0,
                            route_confidence=0.0,
                        ))
                except asyncio.CancelledError:
                    # ★ v1.2 修复: 捕获取消异常，防止批处理崩溃
                    pass
                except Exception as e:
                    processed.append(ProcessResult(
                        query="(unknown)",
                        routed_to=target_claw or "unknown",
                        collaborators_used=[],
                        success=False,
                        error="执行失败"[:200],
                        elapsed_seconds=0.0,
                        route_confidence=0.0,
                    ))
            # 补充未完成项为超时错误
            if pending:
                for i, t in enumerate(task_list):
                    if t in pending:
                        processed.append(ProcessResult(
                            query=queries[i],
                            routed_to=target_claw or "unknown",
                            collaborators_used=[],
                            success=False,
                            error=f"批次超时({self.BATCH_TIMEOUT_SECONDS}s)",
                            elapsed_seconds=self.BATCH_TIMEOUT_SECONDS,
                            route_confidence=0.0,
                        ))
            return processed
        except Exception as e:
            logger.error(f"[process_batch] 批次异常: {e}")
            return []

    # ── 查询方法 ──

    def list_claws(self, filter_school: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        列出所有已加载的Claw信息。

        Args:
            filter_school: 按学派过滤

        Returns:
            信息字典列表
        """
        result = []
        for name, claw in self.claws.items():
            if filter_school and claw.metadata.school != filter_school:
                continue
            result.append({
                "name": name,
                "sage_id": claw.metadata.sage_id,
                "school": claw.metadata.school,
                "era": claw.metadata.era,
                "status": claw.status.value,
                "triggers_count": len(claw.metadata.triggers),
                "wisdom_laws_count": len(claw.metadata.wisdom_laws),
                "cog_depth": claw.metadata.cognitive_dimensions.cog_depth,
            })
        return result

    def find_by_trigger(self, text: str) -> List[str]:
        """查找所有触发词匹配给定文本的Claw"""
        matched = []
        for name, claw in self.claws.items():
            if claw.matches_trigger(text):
                matched.append(name)
        return matched

    def find_by_school(self, school: str) -> List[str]:
        """查找指定学派的所有Claw"""
        return [
            name for name, claw in self.claws.items()
            if claw.metadata.school == school or claw.metadata.wisdom_school == school
        ]

    def get_claw(self, name: str) -> Optional[ClawArchitect]:
        """
        获取指定Claw实例（如未加载则懒加载）[v10.3 回退机制]。

        [v10.3] 懒加载失败回退：
        - 如果指定Claw加载失败，尝试fallback_claw
        - 回退失败后返回None而非抛出异常
        """
        if name in self.claws:
            return self.claws[name]

        # 懒加载
        try:
            claw = create_claw(name, self.configs_dir)
            if claw:
                self.claws[name] = claw
                # ★ v1.2 修复: 懒加载的Claw元数据同步到索引
                self._metadata_index[name] = claw.metadata
                return claw
        except Exception as e:
            logger.warning(f"[ClawsCoordinator] 懒加载 {name} 失败: {e}")

        # [v10.3] 回退到fallback_claw
        fallback = self.gateway._fallback_claw
        if fallback and fallback != name:
            if fallback in self.claws:
                logger.info(f"[ClawsCoordinator] 回退到fallback_claw: {fallback}")
                return self.claws[fallback]
            else:
                # 尝试懒加载fallback
                try:
                    fallback_claw = create_claw(fallback, self.configs_dir)
                    if fallback_claw:
                        self.claws[fallback] = fallback_claw
                        logger.info(f"[ClawsCoordinator] 回退加载fallback_claw: {fallback}")
                        return fallback_claw
                except Exception as e:
                    logger.warning(f"[ClawsCoordinator] 回退claw {fallback} 也加载失败: {e}")

        return None

    def get_metadata_index(self) -> Dict[str, ClawMetadata]:
        """获取元数据索引（含未加载为Claw实例的条目）"""
        return dict(self._metadata_index)

    # ── 回调注册 ──

    def on_process_start(self, fn: Callable) -> "ClawsCoordinator":
        self._on_process_start.append(fn)
        return self

    def on_process_complete(self, fn: Callable) -> "ClawsCoordinator":
        self._on_process_complete.append(fn)
        return self

    # ── 统计与诊断 ──

    def get_stats(self) -> Dict[str, Any]:
        """获取完整统计信息"""
        base = {
            **self.stats.__dict__,
            "loaded_claws": len(self.claws),
            "indexed_metadata": len(self._metadata_index),
            "max_concurrent": self.max_concurrent,
            "fallback_claw": self.gateway._fallback_claw,
        }
        # 序列化usage_counts
        if isinstance(base.get("claw_usage_counts"), dict):
            base["claw_usage_counts"] = dict(base["claw_usage_counts"])
        return base

    def get_health_report(self) -> Dict[str, Any]:
        """
        健康报告：检查所有Claw的状态。
        """
        healthy = []
        degraded = []
        errors = []

        for name, claw in self.claws.items():
            # ★ v1.2 修复: 防御性检查 memory 可能为 None 或未初始化
            if claw.memory is None:
                status = {
                    "name": name,
                    "status": claw.status.value,
                    "episodes": 0,
                    "memory_type": "uninitialized",
                }
            else:
                try:
                    mem_stats = claw.memory.get_stats()
                    status = {
                        "name": name,
                        "status": claw.status.value,
                        "episodes": mem_stats.get("episode_count", 0),
                        "memory_type": mem_stats.get("memory_type", "unknown"),
                    }
                except Exception:
                    status = {
                        "name": name,
                        "status": claw.status.value,
                        "episodes": 0,
                        "memory_type": "error",
                    }
            if claw.status == ClawStatus.ERROR:
                errors.append(status)
            elif claw.status == ClawStatus.IDLE:
                healthy.append(status)
            else:
                degraded.append(status)

        return {
            "total": len(self.claws),
            "healthy": len(healthy),
            "degraded": len(degraded),
            "errors": len(errors),
            "healthy_claws": healthy[:10],
            "error_claws": errors,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }


__all__ = [
    # 类型
    "RouteStrategy", "RouteDecision", "CoordinatorStats", "ProcessResult",
    # 核心
    "ClawsCoordinator", "GatewayRouter",
]
