"""
网络搜索集成模块 v1.0
=======================
为 Somn 所有子系统提供统一的网络搜索能力

集成系统：
- NeuralMemory 记忆系统
- RefuteCore 论证系统
- Pan-Wisdom Tree 智慧树
- DivineReason 推理系统
- TianShu 天枢工作流
- 神政轨 (Track A)
- 神行轨 (Track B)

设计原则：
1. 联网检测优先 - 先检测网络状态
2. 离线优雅降级 - 无网络时使用本地知识库
3. 懒加载 - 不影响系统启动速度
4. 统一接口 - 所有子系统使用相同调用方式

Usage:
    from knowledge_cells.web_integration import (
        WebSearchMixin,
        NeuralMemoryWeb,
        RefuteCoreWeb,
        TianShuWeb,
        TrackAWeb,
        TrackBWeb,
    )
"""

from __future__ import annotations

import logging
from typing import Dict, List, Any, Optional, Callable, Tuple
from functools import lru_cache
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# ==================== 懒加载网络搜索引擎 ====================

_web_engine: Optional[Any] = None
_network_checked: bool = False
_network_online: bool = False
_network_check_time: float = 0.0  # 上次检查时间
_NETWORK_CACHE_TTL: float = 300.0  # 网络状态缓存5分钟


def _get_web_engine():
    """获取全局网络搜索引擎实例（懒加载）"""
    global _web_engine
    if _web_engine is None:
        try:
            from .web_search_engine import WebSearchEngine
            _web_engine = WebSearchEngine()
        except ImportError:
            try:
                from knowledge_cells.web_search_engine import WebSearchEngine
                _web_engine = WebSearchEngine()
            except ImportError:
                logger.warning("WebSearchEngine not available, network search disabled")
                return None
    return _web_engine


def is_online() -> bool:
    """检测网络是否可用（带TTL缓存，5分钟刷新）"""
    global _network_checked, _network_online, _network_check_time
    import time

    now = time.time()
    # 超过TTL或从未检查，重新检测
    if not _network_checked or (now - _network_check_time) > _NETWORK_CACHE_TTL:
        try:
            from .web_search_engine import is_online as check_online
            _network_online = check_online()
        except ImportError:
            try:
                from knowledge_cells.web_search_engine import is_online as check_online
                _network_online = check_online()
            except ImportError:
                _network_online = False
        _network_checked = True
        _network_check_time = now

    return _network_online


def search_with_fallback(
    query: str,
    context: str = "",
    max_results: int = 5,
) -> Dict[str, Any]:
    """
    带降级的搜索函数

    Args:
        query: 搜索关键词
        context: 上下文信息
        max_results: 最大结果数

    Returns:
        {
            "success": bool,
            "results": List[SearchResult],
            "online": bool,
            "source": str,  # "web" / "knowledge_base" / "none"
        }
    """
    # 联网检测
    if not is_online():
        return {
            "success": True,
            "results": [],
            "online": False,
            "source": "none",
            "message": "离线模式，无网络搜索结果"
        }

    engine = _get_web_engine()
    if engine is None:
        return {
            "success": False,
            "results": [],
            "online": False,
            "source": "none",
            "message": "搜索引擎未初始化"
        }

    try:
        # 构建增强查询
        enhanced_query = f"{context} {query}".strip() if context else query

        # 执行搜索
        response = engine.search(enhanced_query, max_results=max_results)

        if response.success and response.results:
            return {
                "success": True,
                "results": [
                    {
                        "title": r.title,
                        "url": r.url,
                        "snippet": r.snippet,
                        "source": r.source,
                        "source_type": r.source_type.value if hasattr(r.source_type, 'value') else str(r.source_type),
                    }
                    for r in response.results
                ],
                "online": True,
                "source": "web",
                "search_time_ms": response.search_time_ms,
            }
        else:
            # 网络搜索无结果 → fallback到DomainNexus知识库
            return _fallback_to_knowledge_base(query)
    except Exception as e:
        logger.warning(f"Web search failed: {e}")
        # 搜索异常 → fallback到DomainNexus
        return _fallback_to_knowledge_base(query)


# ==================== 网络搜索触发关键词 ====================

WEB_SEARCH_TRIGGERS = [
    # 时间敏感
    "最新", "最近", "今日", "今年", "2024", "2025", "2026",
    # 实时信息
    "新闻", "行情", "股价", "汇率", "天气",
    # 趋势分析
    "趋势", "动态", "发展", "变化",
    # 热点事件
    "热点", "热搜", "热门",
    # 数据查询
    "数据", "统计", "报告", "研究",
    # 实时决策
    "现在", "当前", "此时此刻",
    # 学术/验证 (v7.0新增)
    "验证", "核查", "对比", "查询", "搜索",
    "证明", "证据", "来源", "出处", "参考",
    "学术", "论文", "文献", "实验",
    # 商业/行业 (v7.0新增)
    "行业", "市场", "竞品", "对标", "基准",
    "案例", "实践", "方法", "方法论",
]


def should_trigger_web_search(text: str) -> Tuple[bool, str]:
    """
    判断是否应该触发网络搜索

    Returns:
        (should_search, trigger_keyword)
    """
    if not text:
        return False, ""

    text_lower = text.lower()

    for keyword in WEB_SEARCH_TRIGGERS:
        if keyword.lower() in text_lower:
            return True, keyword

    return False, ""


def _fallback_to_knowledge_base(query: str) -> Dict[str, Any]:
    """
    网络搜索无结果时，fallback到DomainNexus知识库

    这是真正的知识库查询，不是空占位。

    Returns:
        {
            "success": bool,
            "results": list,
            "online": bool,
            "source": "knowledge_base",
        }
    """
    try:
        from .domain_nexus import quick_query
        kb_result = quick_query(query)

        results = []
        for cell in kb_result.get("relevant_cells", []):
            results.append({
                "title": f"[知识库] {cell.get('name', '')}",
                "url": "",
                "snippet": cell.get("summary_preview", ""),
                "source": "domain_nexus",
                "source_type": "knowledge_base",
            })

        if results:
            return {
                "success": True,
                "results": results,
                "online": is_online(),
                "source": "knowledge_base",
                "message": f"从知识库找到 {len(results)} 条相关结果"
            }
    except Exception as e:
        logger.debug(f"[WebIntegration] DomainNexus fallback failed: {e}")

    # 知识库也无结果
    return {
        "success": True,
        "results": [],
        "online": is_online(),
        "source": "knowledge_base",
        "message": "网络搜索和知识库均无结果"
    }


# ==================== 通用网络搜索混入类 ====================

class WebSearchMixin:
    """
    网络搜索混入类

    为任何系统提供网络搜索能力

    Usage:
        class MySystem(WebSearchMixin):
            def __init__(self):
                self._init_web_search()

            def process_with_web(self, query: str):
                # 先检查是否需要网络搜索
                if self.should_search(query):
                    results = self.search_web(query)
                    # 融合结果
                    return self.fuse_with_web_results(results, ...)

                # 正常处理
                return self.process_normal(query)
    """

    _web_enabled: bool = True
    _search_triggers: List[str] = None  # 延迟初始化，避免 field() 在非 dataclass 中崩溃

    def _init_web_search(self):
        """初始化网络搜索（子类调用）"""
        self._web_enabled = True
        if self._search_triggers is None:
            self._search_triggers = list(WEB_SEARCH_TRIGGERS)

    def should_search(self, text: str) -> bool:
        """判断是否应该触发网络搜索"""
        if not self._web_enabled:
            return False
        should, _ = should_trigger_web_search(text)
        return should

    def search_web(
        self,
        query: str,
        context: str = "",
        max_results: int = 5,
    ) -> Dict[str, Any]:
        """执行网络搜索"""
        return search_with_fallback(query, context, max_results)

    def fuse_with_web_results(
        self,
        web_results: Dict[str, Any],
        local_result: Any,
        weight: float = 0.3,
    ) -> Any:
        """
        融合网络搜索结果与本地结果

        Args:
            web_results: 网络搜索结果
            local_result: 本地处理结果
            weight: 网络结果权重 (0.0-1.0)

        Returns:
            融合后的结果
        """
        if not web_results.get("success") or not web_results.get("results"):
            return local_result

        # 构建增强结果
        enhanced = {
            "local": local_result,
            "web": web_results["results"],
            "source": web_results.get("source", "unknown"),
            "online": web_results.get("online", False),
        }

        return enhanced


# ==================== NeuralMemory 网络搜索增强 ====================

class NeuralMemoryWeb:
    """
    NeuralMemory 网络搜索增强

    在以下场景触发网络搜索：
    1. 记忆入库时 - 搜索相关背景知识
    2. 记忆检索时 - 搜索最新相关信息
    3. 知识关联时 - 搜索跨域关联知识
    """

    def __init__(self):
        self._enabled = True

    def is_enabled(self) -> bool:
        """检查是否启用"""
        return self._enabled and is_online()

    def search_for_memory(
        self,
        content: str,
        tags: List[str] = None,
        max_results: int = 3,
    ) -> Dict[str, Any]:
        """
        为记忆内容搜索相关背景知识

        Args:
            content: 记忆内容
            tags: 记忆标签
            max_results: 最大结果数

        Returns:
            相关知识列表
        """
        if not self.is_enabled():
            return {"success": False, "source": "disabled"}

        # 构建搜索查询
        query = content[:100]  # 使用内容前100字作为查询
        if tags:
            tag_str = " ".join(tags[:3])  # 最多3个标签
            query = f"{tag_str} {query}"

        return search_with_fallback(query, max_results=max_results)

    def enhance_retrieval(
        self,
        query: str,
        local_results: List[Any],
        max_web_results: int = 2,
    ) -> List[Any]:
        """
        增强记忆检索结果

        当本地结果不足或相关性低时，补充网络搜索结果
        """
        if not self.is_enabled():
            return local_results

        # 检查是否需要网络搜索
        if not self.should_search(query):
            return local_results

        # 如果本地结果少或相关性低，补充网络结果
        if len(local_results) < 2:
            web_results = self.search_for_memory(query, max_results=max_web_results)
            if web_results.get("success") and web_results.get("results"):
                return local_results + web_results["results"][:max_web_results]

        return local_results

    def should_search(self, text: str) -> bool:
        """判断是否应该触发网络搜索"""
        should, keyword = should_trigger_web_search(text)
        if should:
            logger.info(f"NeuralMemory web search triggered by keyword: {keyword}")
        return should


# ==================== RefuteCore 网络搜索增强 ====================

class RefuteCoreWeb:
    """
    RefuteCore 论证系统网络搜索增强

    在以下场景触发网络搜索：
    1. 论证审核时 - 搜索权威来源支持/反驳
    2. 谬误检测时 - 搜索相关事实核查
    3. 证据验证时 - 搜索最新数据和研究
    """

    def __init__(self):
        self._enabled = True

    def is_enabled(self) -> bool:
        """检查是否启用"""
        return self._enabled and is_online()

    def search_supporting_evidence(
        self,
        claim: str,
        max_results: int = 3,
    ) -> Dict[str, Any]:
        """
        搜索支持性证据

        Args:
            claim: 论点/主张
            max_results: 最大结果数

        Returns:
            支持性证据列表
        """
        if not self.is_enabled():
            return {"success": False, "source": "disabled"}

        query = f"支持 {claim}"
        return search_with_fallback(query, max_results=max_results)

    def search_counter_evidence(
        self,
        claim: str,
        max_results: int = 3,
    ) -> Dict[str, Any]:
        """
        搜索反驳性证据

        Args:
            claim: 论点/主张
            max_results: 最大结果数

        Returns:
            反驳性证据列表
        """
        if not self.is_enabled():
            return {"success": False, "source": "disabled"}

        query = f"反驳 {claim}"
        return search_with_fallback(query, max_results=max_results)

    def verify_fact(
        self,
        statement: str,
        max_results: int = 2,
    ) -> Dict[str, Any]:
        """
        事实核查

        Args:
            statement: 待核查陈述
            max_results: 最大结果数

        Returns:
            核查结果
        """
        if not self.is_enabled():
            return {"success": False, "source": "disabled"}

        # 检查是否包含可搜索的关键词
        if not self.should_search(statement):
            return {"success": True, "verifiable": False, "reason": "statement_too_generic"}

        query = f"事实核查 {statement}"
        return search_with_fallback(query, max_results=max_results)

    def should_search(self, text: str) -> bool:
        """判断是否应该触发网络搜索"""
        should, keyword = should_trigger_web_search(text)
        if should:
            logger.info(f"RefuteCore web search triggered by keyword: {keyword}")
        return should


# ==================== TianShu 天枢工作流网络搜索增强 ====================

class TianShuWeb:
    """
    TianShu 天枢工作流网络搜索增强

    在以下场景触发网络搜索：
    1. L2 NLP分析层 - 搜索词条解释
    2. L3 需求分类层 - 搜索相关领域知识
    3. L5 推理层 - 搜索背景知识和最新研究
    4. L7 输出层 - 搜索相关案例和数据
    """

    def __init__(self):
        self._enabled = True

    def is_enabled(self) -> bool:
        """检查是否启用"""
        return self._enabled and is_online()

    def enhance_nlp_analysis(
        self,
        text: str,
        layer_context: str = "",
    ) -> Dict[str, Any]:
        """
        增强NLP分析

        Args:
            text: 用户输入
            layer_context: 层上下文（如"提取术语"）

        Returns:
            术语解释和相关概念
        """
        if not self.is_enabled():
            return {"success": False, "source": "disabled"}

        # 提取可能的术语
        terms = self._extract_terms(text)
        if not terms:
            return {"success": True, "terms": [], "source": "none"}

        results = []
        for term in terms[:3]:  # 最多3个术语
            search_result = search_with_fallback(
                f"解释 {term}",
                context=layer_context,
                max_results=2
            )
            if search_result.get("success") and search_result.get("results"):
                results.append({
                    "term": term,
                    "explanations": search_result["results"]
                })

        return {
            "success": True,
            "terms": results,
            "source": "web" if results else "none"
        }

    def _extract_terms(self, text: str) -> List[str]:
        """提取可能的术语（简化版）"""
        # 去除常见停用词
        stop_words = {"的", "了", "是", "在", "和", "与", "或", "以及", "对于", "关于"}
        words = text.split()
        terms = [w for w in words if len(w) >= 2 and w not in stop_words]
        return terms[:5]

    def search_contextual_knowledge(
        self,
        query: str,
        layer_name: str,
        max_results: int = 3,
    ) -> Dict[str, Any]:
        """
        搜索上下文相关知识

        Args:
            query: 查询内容
            layer_name: 当前层名称
            max_results: 最大结果数

        Returns:
            相关知识
        """
        if not self.is_enabled():
            return {"success": False, "source": "disabled"}

        context = f"来自{layer_name}层"
        return search_with_fallback(query, context=context, max_results=max_results)

    def enhance_reasoning(
        self,
        problem: str,
        reasoning_type: str = "",
    ) -> Dict[str, Any]:
        """
        增强推理

        Args:
            problem: 问题描述
            reasoning_type: 推理类型（如"因果分析"、"趋势预测"）

        Returns:
            相关研究和案例
        """
        if not self.is_enabled():
            return {"success": False, "source": "disabled"}

        if not self.should_search(problem):
            return {"success": True, "enhanced": False, "reason": "no_trigger"}

        query = f"{reasoning_type} {problem}" if reasoning_type else problem
        return search_with_fallback(query, max_results=5)

    def should_search(self, text: str) -> bool:
        """判断是否应该触发网络搜索"""
        should, keyword = should_trigger_web_search(text)
        if should:
            logger.info(f"TianShu web search triggered by keyword: {keyword}")
        return should


# ==================== 神政轨 (Track A) 网络搜索增强 ====================

class TrackAWeb:
    """
    神政轨网络搜索增强

    在以下场景触发网络搜索：
    1. 任务派发时 - 搜索相关执行案例
    2. 监管决策时 - 搜索最新监管政策
    3. 绩效评估时 - 搜索行业基准数据
    """

    def __init__(self):
        self._enabled = True

    def is_enabled(self) -> bool:
        """检查是否启用"""
        return self._enabled and is_online()

    def search_execution_cases(
        self,
        task_type: str,
        context: str = "",
        max_results: int = 3,
    ) -> Dict[str, Any]:
        """
        搜索执行案例

        Args:
            task_type: 任务类型
            context: 任务上下文
            max_results: 最大结果数

        Returns:
            相关执行案例
        """
        if not self.is_enabled():
            return {"success": False, "source": "disabled"}

        query = f"{task_type} 执行案例"
        return search_with_fallback(query, context=context, max_results=max_results)

    def search_regulation_updates(
        self,
        domain: str,
        max_results: int = 2,
    ) -> Dict[str, Any]:
        """
        搜索监管政策更新

        Args:
            domain: 相关领域
            max_results: 最大结果数

        Returns:
            最新监管政策
        """
        if not self.is_enabled():
            return {"success": False, "source": "disabled"}

        query = f"{domain} 监管政策 最新"
        return search_with_fallback(query, max_results=max_results)

    def search_benchmark_data(
        self,
        metric: str,
        industry: str = "",
        max_results: int = 2,
    ) -> Dict[str, Any]:
        """
        搜索行业基准数据

        Args:
            metric: 指标名称
            industry: 行业
            max_results: 最大结果数

        Returns:
            基准数据
        """
        if not self.is_enabled():
            return {"success": False, "source": "disabled"}

        query = f"{industry} {metric} 基准" if industry else f"{metric} 基准"
        return search_with_fallback(query, max_results=max_results)

    def should_search(self, text: str) -> bool:
        """判断是否应该触发网络搜索"""
        should, keyword = should_trigger_web_search(text)
        if should:
            logger.info(f"TrackA web search triggered by keyword: {keyword}")
        return should


# ==================== 神行轨 (Track B) 网络搜索增强 ====================

class TrackBWeb:
    """
    神行轨网络搜索增强

    在以下场景触发网络搜索：
    1. Claw执行时 - 搜索专业知识
    2. 跨部门协作时 - 搜索相关领域知识
    3. 工具调用时 - 搜索最新工具和方法
    """

    def __init__(self):
        self._enabled = True

    def is_enabled(self) -> bool:
        """检查是否启用"""
        return self._enabled and is_online()

    def search_expertise(
        self,
        expertise_area: str,
        problem: str,
        max_results: int = 3,
    ) -> Dict[str, Any]:
        """
        搜索专业知识

        Args:
            expertise_area: 专业领域
            problem: 具体问题
            max_results: 最大结果数

        Returns:
            相关专业知识
        """
        if not self.is_enabled():
            return {"success": False, "source": "disabled"}

        query = f"{expertise_area} {problem}"
        return search_with_fallback(query, max_results=max_results)

    def search_tools_and_methods(
        self,
        task: str,
        max_results: int = 3,
    ) -> Dict[str, Any]:
        """
        搜索工具和方法

        Args:
            task: 任务描述
            max_results: 最大结果数

        Returns:
            相关工具和方法
        """
        if not self.is_enabled():
            return {"success": False, "source": "disabled"}

        query = f"{task} 工具 方法"
        return search_with_fallback(query, max_results=max_results)

    def search_best_practices(
        self,
        practice: str,
        domain: str = "",
        max_results: int = 2,
    ) -> Dict[str, Any]:
        """
        搜索最佳实践

        Args:
            practice: 实践名称
            domain: 领域
            max_results: 最大结果数

        Returns:
            最佳实践
        """
        if not self.is_enabled():
            return {"success": False, "source": "disabled"}

        query = f"{domain} {practice} 最佳实践" if domain else f"{practice} 最佳实践"
        return search_with_fallback(query, max_results=max_results)

    def should_search(self, text: str) -> bool:
        """判断是否应该触发网络搜索"""
        should, keyword = should_trigger_web_search(text)
        if should:
            logger.info(f"TrackB web search triggered by keyword: {keyword}")
        return should


# ==================== 统一导出 ====================

# ── get_network_status 桥接（定义在 web_search_engine.py）─────────────────
def get_network_status() -> Dict[str, Any]:
    """
    获取网络状态详情（桥接自 web_search_engine.py）
    """
    try:
        from .web_search_engine import get_network_status as _gs
        return _gs()
    except ImportError:
        return {"online": False, "latency_ms": -1, "error": "web_search_engine unavailable"}


__all__ = [
    # 核心函数
    "is_online",
    "get_network_status",
    "search_with_fallback",
    "should_trigger_web_search",

    # 混入类
    "WebSearchMixin",

    # 各系统增强类
    "NeuralMemoryWeb",
    "RefuteCoreWeb",
    "TianShuWeb",
    "TrackAWeb",
    "TrackBWeb",

    # 常量
    "WEB_SEARCH_TRIGGERS",
]
