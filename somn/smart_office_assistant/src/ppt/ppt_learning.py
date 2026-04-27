"""
__all__ = [
    'comprehensive_learning',
    'extract_color_knowledge',
    'extract_knowledge_from_html',
    'extract_layout_knowledge',
    'extract_typography_knowledge',
    'generate_learning_report',
    'main',
    'save_knowledge_to_yaml',
    'search_web',
]

PPT学习引擎 - 全网搜索,知识提取,案例分析与模式recognize
"""

import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import yaml
import json
from datetime import datetime
import re
from bs4 import BeautifulSoup
import logging
from src.core.paths import LEARNING_DIR, PROJECT_ROOT

logger = logging.getLogger(__name__)

class LearningCategory(Enum):
    """学习类别"""
    LAYOUT = "layout"           # 排版
    COLOR = "color"             # 配色
    TYPOGRAPHY = "typography"   # 字体
    TEMPLATES = "templates"     # 模板
    TRENDS = "trends"           # 趋势

@dataclass
class SearchResult:
    """搜索结果"""
    url: str
    title: str
    snippet: str
    category: LearningCategory
    source: str
    relevance_score: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class PPTKnowledge:
    """PPT知识"""
    type: str  # rule / pattern / concept / case
    category: str  # layout / color / typography
    content: Dict[str, Any]
    confidence: float
    evidence: List[str]
    tags: List[str]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

class PPTLearningEngine:
    """PPT学习引擎"""

    def __init__(self, knowledge_base_path: str):
        self.knowledge_base_path = knowledge_base_path
        self.search_queries = self._load_search_queries()
        self.knowledge_base = self._load_knowledge_base()

    def _load_search_queries(self) -> Dict[str, List[str]]:
        """加载搜索查询"""
        queries = {
            "layout": [
                "PPT排版技巧 2025 2026",
                "幻灯片布局设计原则",
                "slide layout best practices",
                "presentation design trends",
                "PPT设计布局教程",
                "幻灯片版式设计案例"
            ],
            "color": [
                "PPT配色方案 2025 2026",
                "幻灯片色彩搭配",
                "color scheme presentation",
                "presentation color trends",
                "PPT配色技巧",
                "幻灯片配色指南"
            ],
            "typography": [
                "PPT字体搭配",
                "幻灯片字体设计",
                "presentation typography",
                "font pairing PPT",
                "PPT字体选择",
                "幻灯片字体排版"
            ],
            "templates": [
                "PPT模板设计 2025 2026",
                "幻灯片模板案例分析",
                "presentation templates",
                "slide design examples",
                "PPT优秀模板",
                "专业PPT模板设计"
            ],
            "trends": [
                "PPT设计趋势 2025 2026",
                "幻灯片设计流行趋势",
                "presentation design trends",
                "slide design trends",
                "PPT设计style",
                "幻灯片设计潮流"
            ]
        }
        return queries

    def _load_knowledge_base(self) -> Dict[str, Any]:
        """加载现有知识库"""
        try:
            # 尝试加载各知识库文件
            layouts_path = f"{self.knowledge_base_path}/layouts.yaml"
            colors_path = f"{self.knowledge_base_path}/color_schemes.yaml"
            fonts_path = f"{self.knowledge_base_path}/fonts.yaml"

            knowledge_base = {}

            if os.path.exists(layouts_path):
                with open(layouts_path, 'r', encoding='utf-8') as f:
                    knowledge_base['layouts'] = yaml.safe_load(f)
            if os.path.exists(colors_path):
                with open(colors_path, 'r', encoding='utf-8') as f:
                    knowledge_base['colors'] = yaml.safe_load(f)
            if os.path.exists(fonts_path):
                with open(fonts_path, 'r', encoding='utf-8') as f:
                    knowledge_base['fonts'] = yaml.safe_load(f)

            return knowledge_base
        except Exception as e:
            logger.warning(f"加载知识库失败: {e}")
            return {}

    async def search_web(self, query: str, category: LearningCategory) -> List[SearchResult]:
        """
        搜索网络内容 [v1.0 已实现]
        使用WebSearchEngine进行搜索
        """
        try:
            # 延迟导入避免循环依赖
            from src.data_layer.web_search import WebSearchEngine, SearchSource

            results = []
            logger.info(f"搜索查询: {query} (类别: {category.value})")

            # 创建搜索引擎
            search_engine = WebSearchEngine(cache_dir=None)

            # 根据类别设置搜索来源
            source_map = {
                LearningCategory.LAYOUT: [SearchSource.GENERAL, SearchSource.INDUSTRY],
                LearningCategory.COLOR: [SearchSource.GENERAL, SearchSource.INDUSTRY],
                LearningCategory.TYPOGRAPHY: [SearchSource.GENERAL],
                LearningCategory.TEMPLATES: [SearchSource.GENERAL, SearchSource.INDUSTRY],
                LearningCategory.TRENDS: [SearchSource.NEWS, SearchSource.INDUSTRY],
            }
            sources = source_map.get(category, [SearchSource.GENERAL])

            # 执行搜索
            try:
                search_results = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: search_engine.search_sync(
                        keywords=query.split(),
                        sources=sources,
                        max_results=5,
                        language="zh" if any(ord(c) > 127 for c in query) else "en"
                    )
                )

                # 转换结果格式
                for sr in search_results[:5]:
                    result = SearchResult(
                        url=sr.get('url', ''),
                        title=sr.get('title', ''),
                        snippet=sr.get('snippet', ''),
                        category=category,
                        source=sr.get('source', 'web'),
                        relevance_score=sr.get('relevance_score', 0.5)
                    )
                    results.append(result)

            except Exception as search_error:
                logger.warning(f"WebSearchEngine调用失败，使用备用搜索: {search_error}")
                # 备用：返回预定义的模板知识源
                results = self._get_fallback_sources(category, query)

            return results
        except Exception as e:
            logger.error(f"搜索失败: {e}")
            return []

    def _get_fallback_sources(self, category: LearningCategory, query: str) -> List[SearchResult]:
        """获取备用数据源（当WebSearch不可用时）"""
        fallback_urls = {
            LearningCategory.LAYOUT: [
                ("https://www.zhihu.com/topic/PPT排版", "PPT排版技巧", "知乎PPT排版话题"),
                ("https://www.canva.com/learn/presentation-design/", "Presentation Design Principles", "Canva官方设计指南"),
            ],
            LearningCategory.COLOR: [
                ("https://color.adobe.com/zh/create/color-wheel", "Adobe Color Wheel", "Adobe官方配色工具"),
                ("https://coolors.co/palettes/trending", "Trending Color Palettes", "Coolors趋势配色"),
            ],
            LearningCategory.TYPOGRAPHY: [
                ("https://fonts.google.com/", "Google Fonts", "Google字体库"),
                ("https://www.dafont.com/", "Dafont Fonts", "免费字体下载"),
            ],
            LearningCategory.TEMPLATES: [
                ("https://www.presentationload.com/", "Presentation Templates", "专业PPT模板"),
            ],
            LearningCategory.TRENDS: [
                ("https://www.slidescarnival.com/", "Slide Templates & Trends", "SlideCarnival模板趋势"),
            ],
        }

        results = []
        for url, title, snippet in fallback_urls.get(category, []):
            if query.lower() in title.lower() or query.lower() in snippet.lower():
                results.append(SearchResult(
                    url=url,
                    title=title,
                    snippet=snippet,
                    category=category,
                    source="fallback",
                    relevance_score=0.6
                ))

        return results

    async def extract_layout_knowledge(self, content: str, url: str) -> List[PPTKnowledge]:
        """
        提取排版知识
        """
        knowledge_list = []

        # 提取排版规则
        layout_patterns = [
            r"([^\s]+(?:排版|布局|版式))[::]\s*([^\n]+)",
            r"([^\s]+(?:对齐|间距|留白))[::]\s*([^\n]+)",
            r"([^\s]+(?:层级|视觉))[::]\s*([^\n]+)"
        ]

        for pattern in layout_patterns:
            matches = re.findall(pattern, content)
            for rule_name, rule_content in matches:
                knowledge = PPTKnowledge(
                    type="rule",
                    category="layout",
                    content={
                        "name": rule_name.strip(),
                        "description": rule_content.strip(),
                        "source": url
                    },
                    confidence=0.7,
                    evidence=[url],
                    tags=["layout", "rule", rule_name]
                )
                knowledge_list.append(knowledge)

        return knowledge_list

    async def extract_color_knowledge(self, content: str, url: str) -> List[PPTKnowledge]:
        """
        提取配色知识
        """
        knowledge_list = []

        # 提取颜色代码(HEX格式)
        hex_pattern = r'#[0-9A-Fa-f]{6}'
        colors = re.findall(hex_pattern, content)

        if len(colors) >= 2:
            knowledge = PPTKnowledge(
                type="pattern",
                category="color",
                content={
                    "colors": colors[:6],  # 最多取6个颜色
                    "description": f"发现{len(colors)}个颜色",
                    "source": url
                },
                confidence=0.8,
                evidence=[url],
                tags=["color", "scheme"]
            )
            knowledge_list.append(knowledge)

        # 提取配色原则
        color_principles = [
            r"(?:60-30-10|603010|60%30%10%)",
            r"(?:互补色|类比色|单色|近似色)",
            r"(?:对比度|可读性|无障碍)"
        ]

        for principle in color_principles:
            if re.search(principle, content, re.IGNORECASE):
                knowledge = PPTKnowledge(
                    type="concept",
                    category="color",
                    content={
                        "name": principle,
                        "description": "配色原则",
                        "source": url
                    },
                    confidence=0.75,
                    evidence=[url],
                    tags=["color", "principle", principle]
                )
                knowledge_list.append(knowledge)

        return knowledge_list

    async def extract_typography_knowledge(self, content: str, url: str) -> List[PPTKnowledge]:
        """
        提取字体知识
        """
        knowledge_list = []

        # 提取字体名称(常见中英文字体)
        font_patterns = [
            r"(?:思源黑体|苹方|微软雅黑|Arial|Helvetica|Roboto|Inter)",
            r"(?:Times New Roman|Georgia|Fira Code|Source Code Pro)"
        ]

        found_fonts = []
        for pattern in font_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            found_fonts.extend(matches)

        if len(found_fonts) >= 2:
            knowledge = PPTKnowledge(
                type="pattern",
                category="typography",
                content={
                    "fonts": list(set(found_fonts)),  # 去重
                    "description": f"发现{len(set(found_fonts))}种字体",
                    "source": url
                },
                confidence=0.7,
                evidence=[url],
                tags=["typography", "font"]
            )
            knowledge_list.append(knowledge)

        return knowledge_list

    async def extract_knowledge_from_html(self, html_content: str, url: str,
                                        category: LearningCategory) -> List[PPTKnowledge]:
        """
        从HTML内容中提取知识 [v1.0 已实现]

        Args:
            html_content: HTML内容
            url: 来源URL
            category: 学习类别

        Returns:
            提取的知识列表
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text()

        knowledge_list = []

        # 根据类别提取不同知识
        if category == LearningCategory.LAYOUT:
            knowledge_list.extend(await self.extract_layout_knowledge(text_content, url))
            # 提取布局案例
            case_data = self._extract_layout_cases(soup, url)
            if case_data:
                knowledge_list.append(case_data)
        elif category == LearningCategory.COLOR:
            knowledge_list.extend(await self.extract_color_knowledge(text_content, url))
            # 提取配色案例
            case_data = self._extract_color_cases(soup, url)
            if case_data:
                knowledge_list.append(case_data)
        elif category == LearningCategory.TYPOGRAPHY:
            knowledge_list.extend(await self.extract_typography_knowledge(text_content, url))
        elif category == LearningCategory.TEMPLATES:
            knowledge_list.extend(await self.extract_template_knowledge(soup, url))
        elif category == LearningCategory.TRENDS:
            knowledge_list.extend(await self.extract_trend_knowledge(text_content, url))

        # 提取通用元数据
        meta_knowledge = self._extract_meta_knowledge(soup, url, category)
        if meta_knowledge:
            knowledge_list.append(meta_knowledge)

        logger.info(f"从 {url} 提取了 {len(knowledge_list)} 条知识")
        return knowledge_list

    def _extract_layout_cases(self, soup: BeautifulSoup, url: str) -> Optional[PPTKnowledge]:
        """提取布局案例"""
        title = soup.find('title')
        h1_tags = soup.find_all('h1')
        h2_tags = soup.find_all('h2')

        if title or h1_tags:
            return PPTKnowledge(
                type="case",
                category="layout",
                content={
                    "title": (title.get_text() if title else h1_tags[0].get_text()) if h1_tags else "未命名",
                    "sections": [h2.get_text() for h2 in h2_tags[:5]],
                    "source": url
                },
                confidence=0.6,
                evidence=[url],
                tags=["layout", "case"]
            )
        return None

    def _extract_color_cases(self, soup: BeautifulSoup, url: str) -> Optional[PPTKnowledge]:
        """提取配色案例"""
        style_tags = soup.find_all('style')
        style_content = '\n'.join([s.get_text() for s in style_tags])

        # 提取HEX颜色
        colors = re.findall(r'#[0-9A-Fa-f]{6}', style_content)
        if len(colors) >= 2:
            return PPTKnowledge(
                type="pattern",
                category="color",
                content={
                    "colors": list(set(colors))[:8],
                    "count": len(set(colors)),
                    "source": url
                },
                confidence=0.7,
                evidence=[url],
                tags=["color", "case"]
            )
        return None

    async def extract_template_knowledge(self, soup: BeautifulSoup, url: str) -> List[PPTKnowledge]:
        """提取模板知识"""
        knowledge_list = []

        # 提取链接的模板资源
        template_links = soup.find_all('a', href=re.compile(r'template|slide|ppt|presentation'))
        if template_links:
            templates = []
            for link in template_links[:10]:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                if href:
                    templates.append({"name": text or "未命名", "url": href})

            if templates:
                knowledge_list.append(PPTKnowledge(
                    type="case",
                    category="templates",
                    content={
                        "templates": templates,
                        "count": len(templates),
                        "source": url
                    },
                    confidence=0.65,
                    evidence=[url],
                    tags=["templates", "resources"]
                ))

        return knowledge_list

    async def extract_trend_knowledge(self, content: str, url: str) -> List[PPTKnowledge]:
        """提取趋势知识"""
        knowledge_list = []

        # 提取年份标识的趋势
        year_pattern = r'(20\d{2})\s*(?:年|年度)?\s*((?:趋势|流行|热门|新兴|设计))'
        matches = re.findall(year_pattern, content)

        trends = {}
        for year, trend in matches:
            if year not in trends:
                trends[year] = []
            trends[year].append(trend)

        if trends:
            knowledge_list.append(PPTKnowledge(
                type="concept",
                category="trends",
                content={
                    "trends_by_year": trends,
                    "description": "设计趋势年份分布",
                    "source": url
                },
                confidence=0.7,
                evidence=[url],
                tags=["trends", "temporal"]
            ))

        return knowledge_list

    def _extract_meta_knowledge(self, soup: BeautifulSoup, url: str, category: LearningCategory) -> Optional[PPTKnowledge]:
        """提取元数据知识"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})

        if meta_desc or meta_keywords:
            return PPTKnowledge(
                type="concept",
                category=category.value,
                content={
                    "description": meta_desc.get('content', '') if meta_desc else '',
                    "keywords": meta_keywords.get('content', '') if meta_keywords else '',
                    "source": url
                },
                confidence=0.5,
                evidence=[url],
                tags=["meta", "keywords"]
            )
        return None

    async def comprehensive_learning(self, categories: Optional[List[LearningCategory]] = None) -> Dict[str, Any]:
        """
        synthesize学习:搜索所有类别并提取知识
        """
        if categories is None:
            categories = list(LearningCategory)

        learning_results = {
            "timestamp": datetime.now().isoformat(),
            "categories": {},
            "total_searches": 0,
            "total_knowledge": 0
        }

        for category in categories:
            logger.info(f"开始学习类别: {category.value}")

            queries = self.search_queries.get(category.value, [])
            category_results = {
                "searches": len(queries),
                "knowledge_count": 0,
                "knowledge": []
            }

            for query in queries:
                # 搜索
                search_results = await self.search_web(query, category)
                learning_results["total_searches"] += 1

                # 提取知识 [v1.0 已实现网页抓取]
                for result in search_results:
                    try:
                        # 获取网页内容
                        html_content = await self._fetch_url_content(result.url)
                        if html_content:
                            # 提取知识
                            knowledge_list = await self.extract_knowledge_from_html(
                                html_content, result.url, category
                            )
                        else:
                            knowledge_list = []

                        category_results["knowledge"].extend(knowledge_list)
                        category_results["knowledge_count"] += len(knowledge_list)
                    except Exception as e:
                        logger.warning(f"从 {result.url} 提取知识失败: {e}")

    async def _fetch_url_content(self, url: str, timeout: int = 15) -> str:
        """
        获取URL内容 [v1.0 已实现]

        Args:
            url: 目标URL
            timeout: 超时时间(秒)

        Returns:
            HTML内容字符串，失败返回空字符串
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            }

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
                async with session.get(url, headers=headers, allow_redirects=True) as response:
                    if response.status == 200:
                        content_type = response.headers.get('Content-Type', '')
                        # 优先获取HTML内容
                        if 'text/html' in content_type or 'application/xhtml' in content_type:
                            html = await response.text()
                            return html
                        else:
                            # 非HTML内容也尝试获取
                            return await response.text()
                    else:
                        logger.warning(f"HTTP {response.status}: {url}")
                        return ''
        except asyncio.TimeoutError:
            logger.warning(f"获取超时: {url}")
            return ''
        except Exception as e:
            logger.warning(f"获取失败 {url}: {e}")
            return ''

            learning_results["categories"][category.value] = category_results
            learning_results["total_knowledge"] += category_results["knowledge_count"]

        return learning_results

    def save_knowledge_to_yaml(self, knowledge_list: List[PPTKnowledge], output_path: str):
        """
        保存知识到YAML文件
        """
        # 按类别分组
        knowledge_by_category = {}
        for knowledge in knowledge_list:
            if knowledge.category not in knowledge_by_category:
                knowledge_by_category[knowledge.category] = []
            knowledge_by_category[knowledge.category].append({
                "type": knowledge.type,
                "content": knowledge.content,
                "confidence": knowledge.confidence,
                "evidence": knowledge.evidence,
                "tags": knowledge.tags,
                "timestamp": knowledge.timestamp
            })

        # 保存
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(knowledge_by_category, f, allow_unicode=True, default_flow_style=False)

        logger.info(f"知识已保存到: {output_path}")

    def generate_learning_report(self, learning_results: Dict[str, Any]) -> str:
        """
        generate学习报告
        """
        report_lines = [
            "# PPT设计学习报告",
            f"",
            f"**generate时间**: {learning_results['timestamp']}",
            f"",
            f"## 概览",
            f"- 搜索类别数: {len(learning_results['categories'])}",
            f"- 总搜索次数: {learning_results['total_searches']}",
            f"- 提取知识数: {learning_results['total_knowledge']}",
            f"",
            f"## 分类详情"
        ]

        for category, details in learning_results['categories'].items():
            report_lines.extend([
                f"",
                f"### {category.upper()}",
                f"- 搜索次数: {details['searches']}",
                f"- 知识数量: {details['knowledge_count']}",
                f""
            ])

            # 显示部分知识示例
            if details['knowledge']:
                sample = details['knowledge'][:3]
                for i, knowledge in enumerate(sample, 1):
                    report_lines.append(f"{i}. {knowledge.type}: {knowledge.content.get('name', 'N/A')}")

        return "\n".join(report_lines)

async def main():
    """主函数"""
    # init学习引擎
    engine = PPTLearningEngine(
        knowledge_base_path=str(LEARNING_DIR / "knowledge_base/ppt")
    )

    # 执行synthesize学习
    logger.info("开始PPT设计学习...")
    results = await engine.comprehensive_learning()

    # generate报告
    report = engine.generate_learning_report(results)
    print(report)

    # 保存报告
    report_path=str(PROJECT_ROOT / "reports/ppt_learning_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    logger.info(f"学习完成!报告已保存到: {report_path}")

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
