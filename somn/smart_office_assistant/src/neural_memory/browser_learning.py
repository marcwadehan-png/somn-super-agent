"""


__all__ = [
    'run',
    'run_browser_learning',
]

browser_learning.py
===================
真实浏览器网络学习模块 v1.0

通过 Playwright 驱动 Chromium 浏览器,自动访问学术/技术网站,
抓取最新研究发现,为神经记忆系统提供网络知识输入.

v1.0 改进 (2026-04-03):
  - 修复知乎/掘金/InfoQ选择器过期问题
  - 新增多选择器fallback机制
  - 按来源(name)去重,替代按domain去重
  - 新增重试机制(失败重试1次)
  - 新增CSDN/36kr等稳定数据源
  - 增强通用fallback提取
  - 超时配置与注释保持一致(30秒)

v2.1 改进 (2026-04-03):
  - 知乎改为搜索引擎间接检索(site:zhihu.com via 必应/搜狗)
  - 新增 search_engine_source 类型支持

v2.2 改进 (2026-04-04):
  - 修复去重逻辑:glob匹配从 `{source_key}*.yaml` 改为 `{source_key}_{date_str}*.yaml`
  - 确保"今日已抓取"只对当天文件去重,昨天的文件不再阻止新一天抓取
"""
from __future__ import annotations
import logging
import re
import time
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import yaml

# ─────────────────────────────────────────────────────────────────
# 搜索目标配置
# ─────────────────────────────────────────────────────────────────
# 每个源支持多组选择器(fallback_selectors),按顺序尝试
# 第一组命中就用,否则尝试下一组

SEARCH_TARGETS = [
    # ── 知乎(通过搜索引擎间接检索,避免反爬) ──
    {
        "name": "知乎 - AI记忆系统",
        "type": "search_engine",
        "target_site": "zhihu.com",
        "url": "https://www.bing.com/search?q=site%3Azhihu.com+AI+%E8%AE%B0%E5%BF%86%E7%B3%BB%E7%BB%9F&ensearch=0",
        "fallback_url": "https://www.sogou.com/web?query=site%3Azhihu.com+AI+%E8%AE%B0%E5%BF%86%E7%B3%BB%E7%BB%9F",
        "domain": "记忆系统",
        "keywords": ["记忆", "AI", "LLM", "Memory"],
        "fallback_selectors": [
            {"card": ".b_algo", "title": "h2 a", "desc": ".b_caption p"},
            {"card": "li.b_algo", "title": "h2", "desc": "p"},
            {"card": ".vrwrap, .b_algo", "title": "a", "desc": "p, div"},
        ],
        "fallback_selectors_2": [
            {"card": ".vrwrap, .rb", "title": "h3 a", "desc": ".str_info, .ft"},
            {"card": "div.result", "title": "h3 a", "desc": "p"},
            {"card": ".results div", "title": "a", "desc": "p"},
        ],
    },
    {
        "name": "知乎 - 智能办公Agent",
        "type": "search_engine",
        "target_site": "zhihu.com",
        "url": "https://www.bing.com/search?q=site%3Azhihu.com+%E6%99%BA%E8%83%BD%E5%8A%9E%E5%85%AC+Agent&ensearch=0",
        "fallback_url": "https://www.sogou.com/web?query=site%3Azhihu.com+%E6%99%BA%E8%83%BD%E5%8A%9E%E5%85%AC+Agent",
        "domain": "智能办公",
        "keywords": ["智能体", "办公", "自动化", "Agent"],
        "fallback_selectors": [
            {"card": ".b_algo", "title": "h2 a", "desc": ".b_caption p"},
            {"card": "li.b_algo", "title": "h2", "desc": "p"},
            {"card": ".vrwrap, .b_algo", "title": "a", "desc": "p, div"},
        ],
        "fallback_selectors_2": [
            {"card": ".vrwrap, .rb", "title": "h3 a", "desc": ".str_info, .ft"},
            {"card": "div.result", "title": "h3 a", "desc": "p"},
            {"card": ".results div", "title": "a", "desc": "p"},
        ],
    },
    # ── 搜狗微信 ── (已验证有效)
    {
        "name": "搜狗微信 - 神经记忆",
        "url": "https://weixin.sogou.com/weixin?type=2&query=%E7%A5%9E%E7%BB%8F%E8%AE%B0%E5%BF%86+AI&ie=utf8",
        "domain": "记忆系统",
        "keywords": ["记忆", "神经", "AI"],
        "fallback_selectors": [
            {"card": ".news-box .txt-box", "title": "h3 a", "desc": "p"},
            {"card": ".news-list li", "title": "h3 a", "desc": "p"},
        ],
    },
    {
        "name": "搜狗微信 - 大模型应用",
        "url": "https://weixin.sogou.com/weixin?type=2&query=%E5%A4%A7%E6%A8%A1%E5%9E%8B+%E6%99%BA%E8%83%BD%E5%8A%9E%E5%85%AC&ie=utf8",
        "domain": "AI智能体",
        "keywords": ["大模型", "LLM", "智能", "Agent"],
        "fallback_selectors": [
            {"card": ".news-box .txt-box", "title": "h3 a", "desc": "p"},
            {"card": ".news-list li", "title": "h3 a", "desc": "p"},
        ],
    },
    # ── 掘金 ──
    {
        "name": "掘金 - AI Agent",
        "url": "https://juejin.cn/search?query=AI+Agent+%E8%AE%B0%E5%BF%86&type=0",
        "domain": "AI智能体",
        "keywords": ["Agent", "记忆", "RAG", "向量"],
        "fallback_selectors": [
            {"card": ".entry-box", "title": ".title-row a", "desc": ".abstract"},
            {"card": "[class*='entry']", "title": "a[class*='title']", "desc": "[class*='abstract'], [class*='content']"},
            {"card": "div[class*='item']", "title": "a", "desc": "div"},
        ],
    },
    # ── InfoQ ──
    {
        "name": "InfoQ - 智能办公",
        "url": "https://www.infoq.cn/search?q=%E6%99%BA%E8%83%BD%E5%8A%9E%E5%85%AC+AI",
        "domain": "智能办公",
        "keywords": ["办公", "AI", "智能", "效率"],
        "fallback_selectors": [
            {"card": ".article-item", "title": ".article-title", "desc": ".article-abstract"},
            {"card": "[class*='article']", "title": "h2, h3, a[class*='title']", "desc": "p, div"},
            {"card": "div[class*='item']", "title": "a", "desc": "p"},
        ],
    },
    # ── CSDN ── (新增,SSR渲染,DOM稳定)
    {
        "name": "CSDN - AI记忆系统",
        "url": "https://so.csdn.net/so/search?q=AI+%E8%AE%B0%E5%BF%86%E7%B3%BB%E7%BB%9F&t=all",
        "domain": "记忆系统",
        "keywords": ["记忆", "AI", "LLM", "Memory"],
        "fallback_selectors": [
            {"card": ".search-item", "title": ".search-item-title a", "desc": ".search-item-content"},
            {"card": "[class*='search-item']", "title": "a[class*='title'], h3 a", "desc": "[class*='content'], [class*='abstract']"},
            {"card": "div[class*='item']", "title": "a", "desc": "p"},
        ],
    },
    {
        "name": "CSDN - 智能办公Agent",
        "url": "https://so.csdn.net/so/search?q=%E6%99%BA%E8%83%BD%E5%8A%9E%E5%85%AC+Agent&t=all",
        "domain": "AI智能体",
        "keywords": ["智能体", "办公", "自动化", "Agent"],
        "fallback_selectors": [
            {"card": ".search-item", "title": ".search-item-title a", "desc": ".search-item-content"},
            {"card": "[class*='search-item']", "title": "a[class*='title'], h3 a", "desc": "[class*='content'], [class*='abstract']"},
            {"card": "div[class*='item']", "title": "a", "desc": "p"},
        ],
    },
    # ── 36kr ── (新增,科技媒体,SSR稳定)
    {
        "name": "36kr - AI智能体",
        "url": "https://36kr.com/search/articles/AI%20%E6%99%BA%E8%83%BD%E4%BD%93",
        "domain": "AI智能体",
        "keywords": ["AI", "智能体", "大模型", "Agent"],
        "fallback_selectors": [
            {"card": ".article-item-title, .kr-flow-article-item", "title": "a", "desc": "p, .article-item-summary"},
            {"card": "[class*='article-item'], [class*='flow-article']", "title": "a", "desc": "p, span"},
            {"card": "div[class*='item']", "title": "a", "desc": "p"},
        ],
    },
    # ── 搜狗微信 - 多Agent协作 ── (新增v2.2)
    {
        "name": "搜狗微信 - 多Agent协作",
        "url": "https://weixin.sogou.com/weixin?type=2&query=%E5%A4%9AAgent%E5%8D%8F%E4%BD%9C+%E6%99%BA%E8%83%BD%E4%BD%93&ie=utf8",
        "domain": "AI智能体",
        "keywords": ["多Agent", "协作", "智能体", "Multi-Agent"],
        "fallback_selectors": [
            {"card": ".news-box .txt-box", "title": "h3 a", "desc": "p"},
            {"card": ".news-list li", "title": "h3 a", "desc": "p"},
        ],
    },
    # ── 掘金 - RAG向量检索 ── (新增v2.2)
    {
        "name": "掘金 - RAG向量检索",
        "url": "https://juejin.cn/search?query=RAG+%E5%90%91%E9%87%8F%E6%A3%80%E7%B4%A2+%E7%9F%A5%E8%AF%86%E5%BA%93&type=0",
        "domain": "记忆系统",
        "keywords": ["RAG", "向量", "检索", "知识库", "Embedding"],
        "fallback_selectors": [
            {"card": ".entry-box", "title": ".title-row a", "desc": ".abstract"},
            {"card": "[class*='entry']", "title": "a[class*='title']", "desc": "[class*='abstract'], [class*='content']"},
            {"card": "div[class*='item']", "title": "a", "desc": "div"},
        ],
    },
    # ── 搜狗微信 - AI进化与自主学习 ── (新增v2.2)
    {
        "name": "搜狗微信 - AI进化自主学习",
        "url": "https://weixin.sogou.com/weixin?type=2&query=AI%E8%87%AA%E4%B8%BB%E8%BF%9B%E5%8C%96+%E8%87%AA%E5%AD%A6%E4%B9%A0&ie=utf8",
        "domain": "系统进化",
        "keywords": ["AI进化", "自主学习", "持续学习", "Self-Evolving"],
        "fallback_selectors": [
            {"card": ".news-box .txt-box", "title": "h3 a", "desc": "p"},
            {"card": ".news-list li", "title": "h3 a", "desc": "p"},
        ],
    },
    # ── CSDN - 知识图谱 ── (新增v2.2)
    {
        "name": "CSDN - 知识图谱",
        "url": "https://so.csdn.net/so/search?q=AI%E7%9F%A5%E8%AF%86%E5%9B%BE%E8%B0%B1+%E6%99%BA%E8%83%BD%E4%BD%93&t=all",
        "domain": "系统进化",
        "keywords": ["知识图谱", "AI", "智能体", "Knowledge Graph"],
        "fallback_selectors": [
            {"card": ".search-item", "title": ".search-item-title a", "desc": ".search-item-content"},
            {"card": "[class*='search-item']", "title": "a[class*='title'], h3 a", "desc": "[class*='content'], [class*='abstract']"},
            {"card": "div[class*='item']", "title": "a", "desc": "p"},
        ],
    },
]

# 重试配置
MAX_RETRIES = 1                # 每个源最多重试1次
PAGE_TIMEOUT_MS = 30000        # 页面加载超时 30秒(与注释一致)
DYNAMIC_WAIT_MS = 3000         # 动态内容等待 3秒(JS渲染)
INTER_SOURCE_DELAY = (1.0, 2.5)  # 源间礼貌延迟范围(秒)

logger = logging.getLogger(__name__)
class BrowserNetworkLearner:
    """
    使用 Playwright 驱动浏览器执行网络学习.

    设计原则:
    - 优先使用 Chromium(最稳定,头部headless兼容性最好)
    - 多选择器fallback:每个源配置多组选择器,依次尝试
    - 按来源去重:每天每个name只抓一次(非domain去重)
    - 超时保护:单站点最多30秒
    - 重试机制:失败自动重试1次
    - 降级:抓取失败时跳过,不中断整体流程
    """

    def __init__(self, findings_dir: Path, browser_type: str = "chromium"):
        """
        Args:
            findings_dir: 发现数据保存目录
            browser_type: 'chromium' | 'firefox' | 'webkit' | 'auto'(随机)
                          默认 chromium,比 auto 更稳定可预测
        """
        self.findings_dir = Path(findings_dir)
        self.findings_dir.mkdir(parents=True, exist_ok=True)
        self.browser_type = browser_type
        self.date_str = datetime.now().strftime('%Y%m%d')

    def _pick_browser(self) -> str:
        if self.browser_type != "auto":
            return self.browser_type
        return random.choices(
            ["chromium", "firefox", "webkit"],
            weights=[0.6, 0.3, 0.1]
        )[0]

    def run(self) -> List[Dict]:
        """执行浏览器网络学习,返回新发现列表"""
        chosen_browser = self._pick_browser()
        logger.info(f"  🌐 启动浏览器学习 (engine={chosen_browser})")

        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            logger.error("  ❌ playwright 未安装,跳过浏览器学习")
            return []

        findings = []
        with sync_playwright() as p:
            browser_engine = {
                "chromium": p.chromium,
                "firefox": p.firefox,
                "webkit": p.webkit,
            }.get(chosen_browser, p.chromium)

            try:
                browser = browser_engine.launch(
                    headless=True,
                    args=["--no-sandbox", "--disable-dev-shm-usage"]
                    if chosen_browser == "chromium" else [],
                )
            except Exception as e:
                logger.error(f"  ⚠️ 浏览器启动失败 ({chosen_browser}): {e}")
                if chosen_browser != "chromium":
                    try:
                        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
                        logger.info("  ↩️  已降级到 chromium")
                    except Exception as e2:
                        logger.error(f"  ❌ chromium 也失败: {e2}")
                        return []
                else:
                    return []

            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/131.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1280, "height": 800},
                locale="zh-CN",
            )

            success_count = 0
            skip_count = 0
            fail_count = 0

            for target in SEARCH_TARGETS:
                # 幂等检查:按name+日期去重(同一天内不重复抓取,但跨天强制重新抓取)
                source_key = self._source_to_file_key(target['name'])
                existing = list(self.findings_dir.glob(f"NET_BROWSER_{source_key}_{self.date_str}*.yaml"))
                if existing:
                    logger.warning(f"    ⏭️  {target['name']} 今日已抓取,跳过")
                    try:
                        with open(existing[0], 'r', encoding='utf-8') as f:
                            data = yaml.safe_load(f)
                            if data:
                                data["source"] = "network"
                                findings.append(data)
                    except (yaml.YAMLError, IOError):
                        pass
                    skip_count += 1
                    time.sleep(random.uniform(*INTER_SOURCE_DELAY))
                    continue

                result = self._scrape_target(context, target)
                if result:
                    findings.append(result)
                    success_count += 1
                else:
                    fail_count += 1
                time.sleep(random.uniform(*INTER_SOURCE_DELAY))

            context.close()
            browser.close()

            logger.error(f"  📈 本次抓取: 成功{success_count} | 跳过{skip_count} | 失败{fail_count}")

        # 写入 findings 目录
        saved = self._save_findings(findings)
        logger.info(f"  ✅ 浏览器学习完成:{len(saved)} 条新发现已保存")
        return saved

    def _source_to_file_key(self, name: str) -> str:
        """将数据源名称转为文件key(用于去重和文件命名)"""
        # e.g. "知乎 - AI记忆系统" -> "zhihu_AIjiyixitong"
        safe = re.sub(r"[^\w\u4e00-\u9fff]", "_", name).strip("_")
        safe = re.sub(r"_+", "_", safe)
        return safe

    def _scrape_target(self, context, target: Dict) -> Optional[Dict]:
        """爬取单个目标站点,支持多选择器fallback和重试"""
        for attempt in range(1, MAX_RETRIES + 2):  # 1次原始 + MAX_RETRIES次重试
            result = self._try_scrape(context, target, attempt)
            if result is not None:
                return result
            if attempt < MAX_RETRIES + 1:
                wait = random.uniform(2.0, 4.0)
                logger.error(f"    🔄 {target['name']} 第{attempt}次失败,{wait:.1f}秒后重试...")
                time.sleep(wait)
        return None

    def _try_scrape(self, context, target: Dict, attempt: int) -> Optional[Dict]:
        """单次尝试爬取,返回None表示失败.

        对于 type='search_engine' 的源,先尝试主搜索引擎(必应),
        失败则尝试备用搜索引擎(搜狗).两组URL使用各自的选择器.
        """
        # ── 搜索引擎间接检索模式 ──
        if target.get("type") == "search_engine":
            return self._try_search_engine_scrape(context, target, attempt)

        # ── 直接爬取模式(原有逻辑) ──
        return self._try_direct_scrape(context, target, attempt)

    def _try_search_engine_scrape(self, context, target: Dict, attempt: int) -> Optional[Dict]:
        """通过搜索引擎间接检索目标站点内容(如 site:zhihu.com via 必应)"""
        page = context.new_page()
        try:
            if attempt == 1:
                logger.info(f"    🔍 检索: {target['name']} (via 搜索引擎)")

            # 尝试主搜索引擎(必应)
            result = self._try_search_engine_page(
                page, target,
                target["url"],
                target.get("fallback_selectors", []),
            )
            if result is not None:
                page.close()
                return result

            # 主引擎失败 → 尝试备用搜索引擎(搜狗)
            fallback_url = target.get("fallback_url", "")
            if fallback_url:
                logger.info(f"    ↩️  {target['name']} 必应无结果,尝试搜狗...")
                result = self._try_search_engine_page(
                    page, target,
                    fallback_url,
                    target.get("fallback_selectors_2", []),
                )
                if result is not None:
                    page.close()
                    return result

            page.close()
            return None

        except Exception as e:
            err_msg = "学习失败"
            if "timeout" in err_msg.lower() or "Timeout" in err_msg:
                logger.warning(f"    ⚠️  {target['name']} 超时")
            else:
                logger.error(f"    ❌ {target['name']} 检索失败: {err_msg[:80]}")
            try:
                page.close()
            except Exception as e:
                logger.debug(f"关闭页面失败: {e}")
            return None

    def _extract_search_snippet(self, page, target: Dict, url: str, selectors: List[Dict]) -> Optional[Dict]:
        """在搜索引擎结果页中提取目标站点的搜索摘要"""
        page.goto(url, timeout=PAGE_TIMEOUT_MS, wait_until="domcontentloaded")
        page.wait_for_timeout(DYNAMIC_WAIT_MS)

        # 提取标题和描述
        titles, descs = self._try_fallback_selectors(page, selectors)
        if not titles:
            titles, descs = self._generic_fallback(page, target.get("keywords", []))

        if not titles:
            return None

        # 过滤:只保留指向目标站点的结果(URL含target_site)
        target_site = target.get("target_site", "")
        if target_site:
            filtered_titles = []
            filtered_descs = []
            try:
                # 从搜索结果卡片中的链接提取href
                cards = page.query_selector_all(selectors[0]["card"]) if selectors else []
                for idx, card in enumerate(cards[:10]):
                    link = card.query_selector("a")
                    if link:
                        href = link.get_attribute("href") or ""
                        if target_site in href:
                            if idx < len(titles):
                                filtered_titles.append(titles[idx])
                                if idx < len(descs):
                                    filtered_descs.append(descs[idx])
            except Exception:
                filtered_titles = titles
                filtered_descs = descs

            # 如果过滤后为空,退回使用全部结果(搜索引擎可能不暴露完整URL)
            if not filtered_titles:
                filtered_titles = titles
                filtered_descs = descs
            else:
                titles = filtered_titles
                descs = filtered_descs

        if not titles:
            return None

        # 构建发现条目(标注实际来源站点)
        search_engine = "必应" if "bing.com" in url else "搜狗"
        insight_parts = [t for t in titles[:3]]
        core_insight = "; ".join(insight_parts[:3])
        if descs:
            core_insight += f". 摘要: {descs[0][:150]}"

        finding = {
            "发现标题": f"{target['domain']}领域最新研究({self.date_str},来源:{target['name']})",
            "核心洞察": core_insight[:400],
            "应用领域": target["domain"],
            "应用场景": list({kw for kw in target["keywords"] if kw in core_insight}
                           or target["keywords"][:2]),
            "关键词": [kw for kw in target["keywords"] if kw in core_insight]
                     or target["keywords"],
            "置信度评估": {"置信度评分": 65},  # 间接检索略低
            "研究来源": f"browser_{target['name'].replace(' ', '_')}",
            "抓取URL": url,
            "检索引擎": search_engine,
            "原始标题列表": titles[:5],
        }
        return finding

    def _try_direct_scrape(self, context, target: Dict, attempt: int) -> Optional[Dict]:
        """直接爬取目标站点(原有逻辑)"""
        """单次尝试爬取,返回None表示失败"""
        page = context.new_page()
        try:
            if attempt == 1:
                logger.info(f"    🔍 访问: {target['name']}")
            else:
                logger.info(f"    🔄 重试({attempt}): {target['name']}")

            page.goto(target["url"], timeout=PAGE_TIMEOUT_MS, wait_until="domcontentloaded")
            page.wait_for_timeout(DYNAMIC_WAIT_MS)

            titles = []
            descs = []

            # 1. 多选择器fallback
            selectors = target.get("fallback_selectors", [])
            if selectors:
                titles, descs = self._try_fallback_selectors(page, selectors)
            else:
                # 兼容旧配置格式
                titles, descs = self._try_legacy_selector(
                    page,
                    target.get("selector", ""),
                    target.get("title_sel", "h2"),
                    target.get("desc_sel", "p"),
                )

            # 2. 如果所有选择器都未命中,增强通用fallback
            if not titles:
                titles, descs = self._generic_fallback(page, target.get("keywords", []))

            if not titles:
                logger.warning(f"    ⚠️  {target['name']} 未提取到内容")
                page.close()
                return None

            # 构建发现条目
            insight_parts = [t for t in titles[:3]]
            core_insight = "; ".join(insight_parts[:3])
            if descs:
                core_insight += f". 摘要: {descs[0][:150]}"

            finding = {
                "发现标题": f"{target['domain']}领域最新研究({self.date_str},来源:{target['name']})",
                "核心洞察": core_insight[:400],
                "应用领域": target["domain"],
                "应用场景": list({kw for kw in target["keywords"] if kw in core_insight}
                               or target["keywords"][:2]),
                "关键词": [kw for kw in target["keywords"] if kw in core_insight]
                         or target["keywords"],
                "置信度评估": {"置信度评分": 68},
                "研究来源": f"browser_{target['name'].replace(' ', '_')}",
                "抓取URL": target["url"],
                "原始标题列表": titles[:5],
            }

            page.close()
            return finding

        except Exception as e:
            err_msg = "网络学习失败"
            # 缩减常见超时错误信息
            if "timeout" in err_msg.lower() or "Timeout" in err_msg:
                logger.warning(f"    ⚠️  {target['name']} 超时")
            else:
                logger.error(f"    ❌ {target['name']} 抓取失败: {err_msg[:80]}")
            try:
                page.close()
            except Exception as e:
                logger.debug(f"关闭页面失败: {e}")
            return None

    def _try_fallback_selectors(self, page, selectors: List[Dict]) -> tuple:
        """按顺序尝试多组选择器,第一组命中就返回"""
        for sel_group in selectors:
            card_sel = sel_group.get("card", "")
            title_sel = sel_group.get("title", "h2")
            desc_sel = sel_group.get("desc", "p")

            try:
                cards = page.query_selector_all(card_sel)
                if not cards:
                    continue

                titles = []
                descs = []
                for card in cards[:8]:
                    # title选择器可能是逗号分隔的多个选择器
                    for ts in title_sel.split(","):
                        ts = ts.strip()
                        t_el = card.query_selector(ts)
                        if t_el:
                            title = t_el.inner_text().strip()
                            if title and len(title) > 5:
                                titles.append(title)
                            break

                    for ds in desc_sel.split(","):
                        ds = ds.strip()
                        d_el = card.query_selector(ds)
                        if d_el:
                            desc = d_el.inner_text().strip()
                            if desc and len(desc) > 10:
                                descs.append(desc[:200])
                            break

                if titles:
                    return titles, descs
            except Exception:
                continue

        return [], []

    def _try_legacy_selector(self, page, selector: str, title_sel: str, desc_sel: str) -> tuple:
        """兼容旧格式单组选择器"""
        if not selector:
            return [], []
        try:
            elements = page.query_selector_all(selector)
            titles = []
            descs = []
            for el in elements[:8]:
                t_el = el.query_selector(title_sel)
                d_el = el.query_selector(desc_sel)
                if t_el:
                    title = t_el.inner_text().strip()
                    if title and len(title) > 5:
                        titles.append(title)
                if d_el:
                    desc = d_el.inner_text().strip()
                    if desc and len(desc) > 10:
                        descs.append(desc[:200])
            return titles, descs
        except Exception:
            return [], []

    def _generic_fallback(self, page, keywords: List[str]) -> tuple:
        """增强的通用fallback提取"""
        titles = []
        descs = []

        try:
            # strategy1: 匹配关键词的 h1-h4
            for tag in ["h1", "h2", "h3", "h4"]:
                elements = page.query_selector_all(tag)
                for el in elements[:5]:
                    text = el.inner_text().strip()
                    if text and 5 < len(text) < 200:
                        if keywords and any(kw.lower() in text.lower() for kw in keywords):
                            titles.append(text)
                        elif not keywords and len(text) > 10:
                            # 无关键词时放宽条件
                            titles.append(text)

            # strategy2: 列表链接(很多搜索结果用 li > a 结构)
            if not titles:
                list_items = page.query_selector_all("li a, .list-item a, .result-item a")
                for link in list_items[:8]:
                    text = link.inner_text().strip()
                    href = link.get_attribute("href") or ""
                    if text and 8 < len(text) < 200:
                        if not keywords or any(kw.lower() in text.lower() for kw in keywords):
                            titles.append(text)
                            break  # 每个list取一条避免过多

            # strategy3: 任何包含关键词的链接文本
            if not titles and keywords:
                all_links = page.query_selector_all("a")
                for link in all_links[:20]:
                    text = link.inner_text().strip()
                    if text and 10 < len(text) < 150:
                        if any(kw.lower() in text.lower() for kw in keywords):
                            titles.append(text)
                            if len(titles) >= 3:
                                break

            # 提取描述:取第一个有意义的段落
            if titles:
                for p_tag in page.query_selector_all("p, .desc, .summary, .abstract")[:5]:
                    text = p_tag.inner_text().strip()
                    if text and len(text) > 15:
                        descs.append(text[:200])
                        break

        except Exception as e:
            logger.debug(f"提取内容失败: {e}")

        return titles, descs

    def _save_findings(self, findings: List[Dict]) -> List[Dict]:
        """保存新发现到 findings 目录,按来源name去重"""
        saved = []
        saved_sources = set()  # 记录已保存的来源name,避免重复

        for i, finding in enumerate(findings, 1):
            if not finding:
                continue

            source_name = finding.get("研究来源", f"source_{i}")
            if source_name in saved_sources:
                continue

            source_key = self._source_to_file_key(
                source_name.replace("browser_", "").replace("_", " - ", 1)
            )
            file_key = f"{source_key}_{self.date_str}"

            # 幂等检查
            existing = list(self.findings_dir.glob(f"NET_BROWSER_{file_key}*.yaml"))
            if existing:
                saved_sources.add(source_name)
                continue

            file_name = f"NET_BROWSER_{file_key}_{i:03d}.yaml"
            file_path = self.findings_dir / file_name

            finding["发现ID"] = f"NET_BROWSER_{file_key}_{i:03d}"
            finding["source"] = "network"
            finding["创建时间"] = datetime.now().isoformat()

            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(finding, f, allow_unicode=True, default_flow_style=False)

            saved.append(finding)
            saved_sources.add(source_name)

        return saved

def run_browser_learning(
    findings_dir: str | Path,
    browser_type: str = "chromium",
) -> List[Dict]:
    """
    顶层入口:执行一次完整的浏览器网络学习.

    Args:
        findings_dir: 发现数据保存路径
        browser_type: 'chromium' | 'firefox' | 'webkit' | 'auto'

    Returns:
        新发现列表(已写入磁盘)
    """
    learner = BrowserNetworkLearner(findings_dir=findings_dir, browser_type=browser_type)
    return learner.run()

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
