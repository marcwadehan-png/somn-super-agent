"""
Browser Crawler E2E Test
=========================
测试浏览器爬虫功能

运行方式:
    python -m pytest knowledge_cells/test_browser_crawler.py -v

@author: C0dy
@date: 2026-04-29
"""

import sys
import time
import pytest

# 添加项目根目录到路径
sys.path.insert(0, str(__file__).rsplit("knowledge_cells", 1)[0])


class TestBrowserCrawler:
    """浏览器爬虫测试"""

    @pytest.fixture
    def crawler(self):
        """创建爬虫实例"""
        from knowledge_cells.browser_crawler import HiddenBrowserCrawler

        crawler = HiddenBrowserCrawler(headless=True)
        crawler.start()
        yield crawler
        crawler.close()

    def test_import(self):
        """测试导入"""
        from knowledge_cells.browser_crawler import (
            HiddenBrowserCrawler,
            CrawlerManager,
            CrawledResult,
            CrawlResponse,
            CrawlerEngine,
            SearchEngineType,
            get_crawler_manager,
            search_with_browser,
        )
        assert True

    def test_crawler_creation(self):
        """测试爬虫创建"""
        from knowledge_cells.browser_crawler import HiddenBrowserCrawler

        crawler = HiddenBrowserCrawler(headless=True)
        assert crawler is not None
        assert crawler.headless is True

    @pytest.mark.skipif(
        sys.platform != "win32",
        reason="Browser crawler test requires Windows"
    )
    def test_crawler_start_stop(self):
        """测试爬虫启动和关闭"""
        from knowledge_cells.browser_crawler import HiddenBrowserCrawler

        crawler = HiddenBrowserCrawler(headless=True)
        crawler.start()
        assert crawler._browser is not None or crawler._context is not None

        crawler.close()

    @pytest.mark.skipif(
        sys.platform != "win32",
        reason="Browser crawler test requires Windows"
    )
    def test_search_baidu(self, crawler):
        """测试百度搜索"""
        from knowledge_cells.browser_crawler import SearchEngineType

        response = crawler.search(
            "人工智能",
            search_engine=SearchEngineType.BAIDU,
            max_results=5,
            simulate_human=False,
        )

        print(f"\n[Baidu Search] Query: '人工智能'")
        print(f"Success: {response.success}")
        print(f"Results: {len(response.results)}")
        print(f"Time: {response.crawl_time_ms:.0f}ms")

        if response.results:
            for i, r in enumerate(response.results[:3]):
                print(f"  {i+1}. {r.title[:50]}...")
                print(f"     {r.url[:60]}...")

        assert response.query == "人工智能"

    @pytest.mark.skipif(
        sys.platform != "win32",
        reason="Browser crawler test requires Windows"
    )
    def test_search_duckduckgo(self, crawler):
        """测试 DuckDuckGo 搜索"""
        from knowledge_cells.browser_crawler import SearchEngineType

        response = crawler.search(
            "Python programming",
            search_engine=SearchEngineType.DUCKDUCKGO,
            max_results=5,
            simulate_human=False,
        )

        print(f"\n[DuckDuckGo Search] Query: 'Python programming'")
        print(f"Success: {response.success}")
        print(f"Results: {len(response.results)}")
        print(f"Time: {response.crawl_time_ms:.0f}ms")

        if response.results:
            for i, r in enumerate(response.results[:3]):
                print(f"  {i+1}. {r.title[:50]}...")

        assert response.query == "Python programming"

    @pytest.mark.skipif(
        sys.platform != "win32",
        reason="Browser crawler test requires Windows"
    )
    def test_batch_search(self, crawler):
        """测试批量搜索"""
        from knowledge_cells.browser_crawler import SearchEngineType

        queries = ["机器学习", "深度学习", "神经网络"]
        responses = crawler.batch_search(
            queries,
            search_engine=SearchEngineType.DUCKDUCKGO,
            max_results=3,
        )

        print(f"\n[Batch Search] {len(queries)} queries")

        for resp in responses:
            print(f"  - {resp.query}: {len(resp.results)} results")

        assert len(responses) == len(queries)

    def test_stats(self, crawler):
        """测试统计功能"""
        stats = crawler.get_stats()
        print(f"\n[Stats] {stats}")

        assert "total_searches" in stats
        assert "successful_searches" in stats
        assert "success_rate" in stats

    def test_crawl_response_structure(self):
        """测试响应数据结构"""
        from knowledge_cells.browser_crawler import CrawlResponse, CrawledResult

        resp = CrawlResponse(
            query="test",
            success=True,
            results=[
                CrawledResult(
                    title="Test Title",
                    url="https://example.com",
                    snippet="Test snippet",
                    rank=1,
                    search_engine="test",
                )
            ],
            total_found=1,
            crawl_time_ms=100.0,
            search_engine="test_engine",
        )

        assert resp.query == "test"
        assert resp.success is True
        assert len(resp.results) == 1
        assert resp.results[0].title == "Test Title"


class TestAutoStarter:
    """自启动管理器测试"""

    def test_import(self):
        """测试导入"""
        from knowledge_cells.auto_starter import (
            AutoStarter,
            CrawlerService,
            enable_auto_start,
            disable_auto_start,
            get_auto_start_status,
        )
        assert True

    def test_starter_creation(self):
        """测试启动器创建"""
        from knowledge_cells.auto_starter import AutoStarter

        starter = AutoStarter("TestApp")
        assert starter.app_name == "TestApp"

    def test_status_check(self):
        """测试状态检查"""
        from knowledge_cells.auto_starter import AutoStarter

        starter = AutoStarter("TestApp")
        status = starter.get_status()

        print(f"\n[AutoStart Status] {status}")

        assert "startup_folder" in status
        assert "registry_run" in status
        assert "registry_run_once" in status
        assert "scheduled_task" in status

    @pytest.mark.skipif(
        sys.platform != "win32",
        reason="AutoStarter test requires Windows"
    )
    def test_enable_disable_registry(self):
        """测试注册表自启动开关"""
        from knowledge_cells.auto_starter import AutoStarter, REGISTRY_RUN

        starter = AutoStarter("TestSomnCrawler")
        script_path = __file__.rsplit("knowledge_cells", 1)[0] + "knowledge_cells\\browser_crawler.py"

        # 启用
        result = starter.enable_startup(
            script_path=script_path,
            method=REGISTRY_RUN,
            hidden=True,
        )
        print(f"\n[Enable] {result}")

        # 检查状态
        is_enabled = starter.is_enabled(REGISTRY_RUN)
        print(f"[Is Enabled] {is_enabled}")
        assert is_enabled is True

        # 禁用
        result = starter.disable_startup(REGISTRY_RUN)
        print(f"[Disable] {result}")

        # 再次检查状态
        is_enabled = starter.is_enabled(REGISTRY_RUN)
        assert is_enabled is False


class TestWebSearchEngineIntegration:
    """WebSearchEngine 集成测试"""

    def test_import_browser_functions(self):
        """测试导入浏览器搜索函数"""
        from knowledge_cells.web_search_engine import (
            search_with_browser,
            get_crawler_manager,
            search_enhanced,
        )
        assert callable(search_with_browser)
        assert callable(get_crawler_manager)
        assert callable(search_enhanced)

    @pytest.mark.skipif(
        sys.platform != "win32",
        reason="Browser search test requires Windows"
    )
    def test_search_with_browser_function(self):
        """测试浏览器搜索函数"""
        from knowledge_cells.web_search_engine import search_with_browser

        try:
            response = search_with_browser(
                "Hello World",
                search_engine="duckduckgo",
                max_results=3,
                headless=True,
            )

            print(f"\n[Browser Search] Query: 'Hello World'")
            print(f"Success: {response.success}")
            print(f"Results: {len(response.results)}")

            if response.results:
                for i, r in enumerate(response.results[:3]):
                    print(f"  {i+1}. {r.title[:40]}...")

        except ImportError as e:
            pytest.skip(f"Playwright not installed: {e}")
        except Exception as e:
            pytest.skip(f"Browser test skipped: {e}")

    def test_search_enhanced_fallback(self):
        """测试增强搜索降级"""
        from knowledge_cells.web_search_engine import search_enhanced

        response = search_enhanced(
            "test query",
            max_results=5,
            use_browser=False,
            fallback_to_knowledge_base=True,
        )

        print(f"\n[Enhanced Search] Success: {response.success}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
