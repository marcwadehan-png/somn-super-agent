"""
推理-网络桥接模块 v1.0
=====================
让 LLM 推理过程中主动触发网络搜索

核心设计：
1. LLM 在推理过程中可以主动调用 `request_web_search(query)` 请求搜索
2. 搜索结果以结构化方式返回给 LLM 作为推理上下文
3. 支持推理级联：一次搜索可触发多次相关搜索

使用方式：
    bridge = ReasoningWebBridge()

    # LLM 推理过程中主动请求搜索
    if bridge.needs_web_search(reasoning_step):
        results = bridge.request_web_search(
            query="茅台最新股价",
            context="用户问茅台今天表现"
        )
        # 将结果注入到下一步推理
        reasoning_step = bridge.inject_results(reasoning_step, results)
"""

from __future__ import annotations

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import threading

logger = logging.getLogger(__name__)


# ==================== 枚举定义 ====================


class SearchIntent(Enum):
    """搜索意图类型"""
    FACT_LOOKUP = "fact_lookup"         # 事实查询
    DATA_VERIFY = "data_verify"         # 数据验证
    KNOWLEDGE_BOTTOM = "knowledge_bottom"  # 知识补全
    NEWS_CHECK = "news_check"           # 新闻核查
    TREND_RESEARCH = "trend_research"  # 趋势调研


# ==================== 数据结构 ====================


@dataclass
class WebSearchRequest:
    """网络搜索请求"""
    query: str
    intent: SearchIntent = SearchIntent.FACT_LOOKUP
    context: str = ""
    priority: int = 0  # 0=低, 1=中, 2=高
    session_id: str = ""
    request_id: str = ""


@dataclass
class WebSearchResult:
    """网络搜索结果（结构化）"""
    query: str
    intent: SearchIntent
    success: bool
    results: List[Dict[str, str]] = field(default_factory=list)
    result_count: int = 0
    search_time_ms: float = 0.0
    source: str = "web"  # web / knowledge_base / none
    error: str = ""


@dataclass
class ReasoningWebContext:
    """推理-网络上下文"""
    session_id: str
    search_history: List[WebSearchRequest] = field(default_factory=list)
    result_history: List[WebSearchResult] = field(default_factory=list)
    injected_contexts: List[str] = field(default_factory=list)
    total_searches: int = 0


# ==================== 搜索意图识别器 ====================


class IntentClassifier:
    """
    从推理步骤中识别搜索意图

    规则：
    - 包含具体数字/日期 → FACT_LOOKUP
    - 包含"最新"/"今天"/"现在" → NEWS_CHECK
    - 包含"验证"/"确认"/"核实" → DATA_VERIFY
    - 包含"不知道"/"不清楚"/"需要查" → KNOWLEDGE_BOTTOM
    - 包含"趋势"/"发展"/"预测" → TREND_RESEARCH
    """

    INTENT_PATTERNS = {
        SearchIntent.FACT_LOOKUP: [
            "多少", "是多少", "最新价格", "当前", "股价", "营收",
            "多少", "数量", "数据", "统计",
        ],
        SearchIntent.DATA_VERIFY: [
            "验证", "确认", "核实", "是否正确", "准确吗",
        ],
        SearchIntent.NEWS_CHECK: [
            "最新", "今日", "今天", "现在", "刚刚", "最新消息",
            "新闻", "动态", "进展",
        ],
        SearchIntent.KNOWLEDGE_BOTTOM: [
            "不知道", "不清楚", "需要查", "查一下", "了解一下",
            "具体", "详情", "详细介绍",
        ],
        SearchIntent.TREND_RESEARCH: [
            "趋势", "发展", "预测", "未来", "预期", "展望",
        ],
    }

    @classmethod
    def classify(cls, text: str) -> List[Tuple[SearchIntent, float]]:
        """
        识别文本中的搜索意图

        Returns:
            [(intent, confidence), ...] 按置信度排序
        """
        if not text:
            return []

        text_lower = text.lower()
        scores = {}

        for intent, patterns in cls.INTENT_PATTERNS.items():
            score = 0.0
            matched_patterns = []
            for pattern in patterns:
                if pattern.lower() in text_lower:
                    score += 1.0
                    matched_patterns.append(pattern)
            if score > 0:
                scores[intent] = (score, matched_patterns)

        # 转换为置信度并排序
        results = []
        for intent, (score, matched) in scores.items():
            # 归一化置信度
            confidence = min(0.95, 0.3 + score * 0.15)
            results.append((intent, confidence, matched))

        # 按置信度排序
        results.sort(key=lambda x: x[1], reverse=True)
        return [(r[0], r[1]) for r in results]


# ==================== 推理-网络桥接器 ====================


class ReasoningWebBridge:
    """
    推理-网络桥接器

    核心功能：
    1. 判断推理步骤是否需要网络搜索
    2. 执行网络搜索并结构化返回
    3. 将搜索结果注入推理上下文

    使用方式：
        bridge = ReasoningWebBridge()

        # 判断是否需要搜索
        if bridge.needs_web_search(reasoning_step):
            # 执行搜索
            result = bridge.request_web_search(
                query="茅台股价",
                context="用户询问"
            )
            # 注入结果
            enhanced_step = bridge.inject_results(reasoning_step, result)
    """

    def __init__(self, session_id: str = ""):
        self.session_id = session_id or self._generate_session_id()
        self._context = ReasoningWebContext(session_id=self.session_id)
        self._lock = threading.Lock()

        # 搜索结果缓存（避免重复搜索）
        self._search_cache: Dict[str, WebSearchResult] = {}
        self._cache_max_size = 100

    @staticmethod
    def _generate_session_id() -> str:
        """生成会话ID"""
        import time
        return f"rw_{int(time.time() * 1000):016x}"

    def needs_web_search(self, reasoning_text: str) -> bool:
        """
        判断推理步骤是否需要网络搜索

        触发条件：
        1. 显式意图：包含"查一下"/"需要知道"等
        2. 时间敏感：包含"最新"/"今日"/"当前"
        3. 数据验证：包含"验证"/"确认"/"是否正确"
        4. 知识缺失：包含"不知道"/"不清楚"

        Args:
            reasoning_text: 当前推理步骤文本

        Returns:
            True = 需要搜索
        """
        if not reasoning_text:
            return False

        # 规则1: 显式搜索意图
        explicit_patterns = [
            "查一下", "查查", "搜索", "搜一下", "需要查",
            "网上", "搜索一下", "查证", "核实一下",
        ]
        for pattern in explicit_patterns:
            if pattern in reasoning_text:
                return True

        # 规则2: 意图分类器
        intents = IntentClassifier.classify(reasoning_text)
        if intents and intents[0][1] >= 0.5:  # 置信度 >= 0.5
            return True

        # 规则3: 知识空白检测
        knowledge_gaps = ["不知道", "不清楚", "不了解", "不确定", "可能需要"]
        for gap in knowledge_gaps:
            if gap in reasoning_text:
                return True

        return False

    def request_web_search(
        self,
        query: str,
        context: str = "",
        intent: SearchIntent = SearchIntent.FACT_LOOKUP,
        priority: int = 0,
    ) -> WebSearchResult:
        """
        主动请求网络搜索

        Args:
            query: 搜索关键词
            context: 上下文信息
            intent: 搜索意图
            priority: 优先级 (0=低, 1=中, 2=高)

        Returns:
            WebSearchResult 结构化搜索结果
        """
        import time
        start_time = time.perf_counter()

        # 检查缓存
        cache_key = query.strip().lower()
        if cache_key in self._search_cache:
            cached = self._search_cache[cache_key]
            logger.debug(f"Cache hit for query: {query}")
            return cached

        # 构建请求
        request = WebSearchRequest(
            query=query,
            intent=intent,
            context=context,
            priority=priority,
            session_id=self.session_id,
            request_id=f"req_{int(time.time() * 1000):016x}",
        )

        with self._lock:
            self._context.search_history.append(request)
            self._context.total_searches += 1

        # 执行搜索
        result = self._execute_search(request, start_time)

        # 缓存结果
        with self._lock:
            if len(self._search_cache) >= self._cache_max_size:
                # FIFO 淘汰
                oldest_key = next(iter(self._search_cache))
                del self._search_cache[oldest_key]
            self._search_cache[cache_key] = result
            self._context.result_history.append(result)

        return result

    def _execute_search(
        self,
        request: WebSearchRequest,
        start_time: float,
    ) -> WebSearchResult:
        """执行搜索"""
        try:
            from knowledge_cells.web_integration import search_with_fallback, is_online

            if not is_online():
                return WebSearchResult(
                    query=request.query,
                    intent=request.intent,
                    success=False,
                    error="离线模式",
                    source="none",
                    search_time_ms=(time.perf_counter() - start_time) * 1000,
                )

            # 执行搜索
            response = search_with_fallback(
                query=request.query,
                context=request.context,
                max_results=5,
            )

            search_time_ms = (time.perf_counter() - start_time) * 1000

            if response.get("success") and response.get("results"):
                results_list = []
                for r in response["results"]:
                    results_list.append({
                        "title": r.get("title", ""),
                        "url": r.get("url", ""),
                        "snippet": r.get("snippet", ""),
                        "source": r.get("source", ""),
                    })

                return WebSearchResult(
                    query=request.query,
                    intent=request.intent,
                    success=True,
                    results=results_list,
                    result_count=len(results_list),
                    search_time_ms=search_time_ms,
                    source=response.get("source", "web"),
                )
            else:
                return WebSearchResult(
                    query=request.query,
                    intent=request.intent,
                    success=False,
                    error=response.get("message", "无搜索结果"),
                    source=response.get("source", "none"),
                    search_time_ms=search_time_ms,
                )

        except ImportError as e:
            logger.warning(f"web_integration not available: {e}")
            return WebSearchResult(
                query=request.query,
                intent=request.intent,
                success=False,
                error=f"模块导入失败: {e}",
                source="none",
                search_time_ms=(time.perf_counter() - start_time) * 1000,
            )
        except Exception as e:
            logger.error(f"Web search failed: {e}")
            return WebSearchResult(
                query=request.query,
                intent=request.intent,
                success=False,
                error=str(e),
                source="none",
                search_time_ms=(time.perf_counter() - start_time) * 1000,
            )

    def inject_results(
        self,
        reasoning_step: str,
        search_result: WebSearchResult,
    ) -> str:
        """
        将搜索结果注入推理步骤

        Args:
            reasoning_step: 当前推理步骤
            search_result: 搜索结果

        Returns:
            增强后的推理步骤
        """
        if not search_result.success or not search_result.results:
            return reasoning_step

        # 构建注入内容
        injected_lines = [f"\n【网络搜索结果 - {search_result.query}】"]

        for i, r in enumerate(search_result.results[:3], 1):  # 最多3条
            title = r.get("title", "无标题")
            snippet = r.get("snippet", "")
            source = r.get("source", "")

            injected_lines.append(f"  {i}. {title}")
            if snippet:
                injected_lines.append(f"     {snippet[:100]}...")
            if source:
                injected_lines.append(f"     来源: {source}")

        injected_lines.append("【搜索结果结束】\n")

        injected_context = "\n".join(injected_lines)
        enhanced_step = reasoning_step + "\n" + injected_context

        with self._lock:
            self._context.injected_contexts.append(injected_context)

        return enhanced_step

    def get_context_summary(self) -> Dict[str, Any]:
        """获取桥接上下文摘要"""
        with self._lock:
            return {
                "session_id": self.session_id,
                "total_searches": self._context.total_searches,
                "cache_size": len(self._search_cache),
                "search_history_count": len(self._context.search_history),
                "injected_count": len(self._context.injected_contexts),
            }

    def clear_cache(self):
        """清空搜索缓存"""
        with self._lock:
            self._search_cache.clear()


# ==================== 全局桥接管理器 ====================


_bridge_store: Dict[str, ReasoningWebBridge] = {}
_bridge_lock = threading.Lock()


def get_reasoning_bridge(session_id: str = "") -> ReasoningWebBridge:
    """
    获取或创建推理-网络桥接实例

    Args:
        session_id: 会话ID（空则自动生成）

    Returns:
        ReasoningWebBridge 实例
    """
    with _bridge_lock:
        if not session_id:
            session_id = ReasoningWebBridge._generate_session_id()

        if session_id not in _bridge_store:
            _bridge_store[session_id] = ReasoningWebBridge(session_id=session_id)

        return _bridge_store[session_id]


# ==================== 集成函数 ====================


def auto_search_in_reasoning(
    reasoning_steps: List[str],
    session_id: str = "",
) -> Tuple[List[str], List[WebSearchResult]]:
    """
    自动在推理过程中插入网络搜索

    Args:
        reasoning_steps: 推理步骤列表
        session_id: 会话ID

    Returns:
        (增强后的推理步骤列表, 搜索结果列表)
    """
    bridge = get_reasoning_bridge(session_id)
    enhanced_steps = []
    search_results = []

    for step in reasoning_steps:
        if bridge.needs_web_search(step):
            # 识别意图
            intents = IntentClassifier.classify(step)
            intent = intents[0][0] if intents else SearchIntent.FACT_LOOKUP

            # 提取搜索关键词
            keywords = _extract_keywords_from_step(step)
            if keywords:
                result = bridge.request_web_search(
                    query=keywords,
                    context=step[:100],
                    intent=intent,
                )
                if result.success:
                    step = bridge.inject_results(step, result)
                    search_results.append(result)

        enhanced_steps.append(step)

    return enhanced_steps, search_results


def _extract_keywords_from_step(step: str) -> str:
    """从推理步骤中提取搜索关键词"""
    # 去除常见停用词
    stop_words = {
        "的", "了", "是", "在", "和", "与", "或", "以及", "对于", "关于",
        "我", "你", "他", "她", "它", "我们", "你们", "他们",
        "这个", "那个", "一个", "这种", "某种",
        "可能", "应该", "需要", "可以", "能够",
        "不知道", "不清楚", "需要查", "查一下",
    }

    import re
    words = re.findall(r'[\w\u4e00-\u9fff]{2,}', step)
    keywords = [w for w in words if w not in stop_words and len(w) >= 2]

    # 返回前5个关键词组合
    return " ".join(keywords[:5])


# ==================== 快捷函数 ====================


def needs_search(reasoning_text: str) -> bool:
    """快捷函数：判断是否需要搜索"""
    return get_reasoning_bridge().needs_web_search(reasoning_text)


def search_for_reasoning(
    query: str,
    context: str = "",
) -> WebSearchResult:
    """快捷函数：执行搜索并返回结构化结果"""
    return get_reasoning_bridge().request_web_search(query, context)


def enhance_with_web(
    reasoning_step: str,
    session_id: str = "",
) -> str:
    """
    快捷函数：自动判断并注入搜索结果

    Returns:
        增强后的推理步骤
    """
    bridge = get_reasoning_bridge(session_id)
    if bridge.needs_web_search(reasoning_step):
        intents = IntentClassifier.classify(reasoning_step)
        intent = intents[0][0] if intents else SearchIntent.FACT_LOOKUP
        keywords = _extract_keywords_from_step(reasoning_step)
        if keywords:
            result = bridge.request_web_search(keywords, reasoning_step[:100], intent)
            return bridge.inject_results(reasoning_step, result)
    return reasoning_step


# ==================== 测试用例 ====================


def _test_reasoning_web_bridge():
    """内部测试"""
    bridge = ReasoningWebBridge(session_id="test_session")

    test_steps = [
        "用户询问茅台今天的股价表现",
        "我需要查一下最新数据来验证这个观点",
        "根据公开信息，茅台2024年营收达到1500亿元",
        "关于AI发展趋势，需要了解一下最新研究",
        "我认为这个方案是可行的",
    ]

    print("=== 推理步骤搜索需求检测 ===")
    for step in test_steps:
        needs = bridge.needs_web_search(step)
        intents = IntentClassifier.classify(step)
        keywords = _extract_keywords_from_step(step)
        print(f"\n原文: {step[:40]}...")
        print(f"  需要搜索: {needs}")
        if intents:
            print(f"  意图: {intents[0][0].value} ({intents[0][1]:.2f})")
        print(f"  关键词: {keywords}")

    print("\n=== 执行搜索测试 ===")
    result = bridge.request_web_search(
        query="茅台股价",
        context="用户询问",
        intent=SearchIntent.FACT_LOOKUP,
    )
    print(f"搜索成功: {result.success}")
    print(f"结果数: {result.result_count}")
    print(f"来源: {result.source}")

    if result.success:
        print(f"第一条: {result.results[0].get('title', '')[:50]}")


if __name__ == "__main__":
    _test_reasoning_web_bridge()
