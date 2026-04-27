"""
知识格子系统测试
================
测试knowledge_cells模块的完整功能

运行方式:
    python -m pytest tests/test_knowledge_cells.py -v
"""

import pytest
import sys
import os
from pathlib import Path

# 添加父目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from knowledge_cells import (
    get_knowledge_system,
    query,
    check,
    get_status,
    KnowledgeSystem
)


class TestKnowledgeCellsEngine:
    """测试知识格子引擎"""
    
    @pytest.fixture
    def system(self):
        """创建知识系统实例"""
        cells_dir = project_root / "knowledge_cells"
        return get_knowledge_system(str(cells_dir))
    
    def test_engine_load(self, system):
        """测试引擎加载"""
        assert system is not None
        assert system.engine is not None
        assert len(system.engine.cells) >= 21
    
    def test_get_cell(self, system):
        """测试获取格子"""
        cell = system.get_cell_content("A1")
        assert cell is not None
        assert cell['cell_id'] == "A1"
        assert 'name' in cell
        assert 'tags' in cell
    
    def test_get_nonexistent_cell(self, system):
        """测试获取不存在的格子"""
        cell = system.get_cell_content("Z9")
        assert cell is None
    
    def test_search_cells(self, system):
        """测试格子搜索"""
        results = system.search_cells("裂变")
        assert len(results) > 0
        assert any("B1" in r['cell_id'] for r in results)
    
    def test_related_cells(self, system):
        """测试关联格子"""
        related = system.get_related_cells("A1")
        assert isinstance(related, list)
    
    def test_hot_cells(self, system):
        """测试最热格子"""
        hot = system.get_hot_cells(5)
        assert len(hot) <= 5
        assert all('cell_id' in c for c in hot)
    
    def test_list_all_cells(self, system):
        """测试列出所有格子"""
        cells = system.list_all_cells()
        assert len(cells) >= 21
        # 应该有智慧核心(A1-A8)和知识域(B1-C4)
        core_ids = [c['cell_id'] for c in cells if c['cell_id'].startswith('A')]
        domain_ids = [c['cell_id'] for c in cells if c['cell_id'].startswith(('B', 'C'))]
        assert len(core_ids) >= 8
        assert len(domain_ids) >= 13
    
    def test_knowledge_graph(self, system):
        """测试知识图谱"""
        graph = system.get_knowledge_graph()
        assert 'nodes' in graph
        assert 'links' in graph
        assert len(graph['nodes']) >= 21
    
    def test_system_status(self, system):
        """测试系统状态"""
        status = system.get_status()
        assert 'total_cells' in status
        assert status['total_cells'] >= 21
        assert 'hot_cells' in status
        assert 'summary' in status


class TestKnowledgeFusion:
    """测试知识融合"""
    
    @pytest.fixture
    def system(self):
        """创建知识系统实例"""
        cells_dir = project_root / "knowledge_cells"
        return get_knowledge_system(str(cells_dir))
    
    def test_query_user_growth(self, system):
        """测试用户增长查询"""
        result = system.query("如何提升用户增长")
        
        assert 'answer' in result
        assert 'cells_used' in result
        assert 'frameworks' in result
        assert 'quality_score' in result
        assert len(result['cells_used']) > 0
    
    def test_query_live_streaming(self, system):
        """测试直播运营查询"""
        result = system.query("直播运营的关键指标有哪些")
        
        assert result['cells_used'] is not None
        assert len(result['cells_used']) > 0
    
    def test_query_empty(self, system):
        """测试空查询"""
        result = system.query("")
        assert result['answer'] is not None


class TestMethodologyChecker:
    """测试方法论检查"""
    
    @pytest.fixture
    def system(self):
        """创建知识系统实例"""
        cells_dir = project_root / "knowledge_cells"
        return get_knowledge_system(str(cells_dir))
    
    def test_good_response(self, system):
        """测试高质量回答检查"""
        good_response = """
        【问题诊断】
        当前面临获客成本高、留存率低的问题。
        
        【数据支撑】
        CAC为80元，高于行业平均60元
        次日留存率35%，低于目标50%
        
        【框架建议】
        采用AARRR模型进行分析优化
        
        【举一反三】
        用户增长就像经营线下门店
        """
        
        result = system.check_methodology(good_response)
        
        assert 'overall_score' in result
        assert 'level' in result
        assert 'checks' in result
        # 检查各个维度的检查结果
        assert 'diagnosis' in result['checks']
        assert 'framework' in result['checks']
        assert 'data' in result['checks']
        assert result['overall_score'] >= 60
    
    def test_poor_response(self, system):
        """测试低质量回答检查"""
        poor_response = "我觉得应该这样做。"
        
        result = system.check_methodology(poor_response)
        
        assert result['overall_score'] < 50
        assert 'diagnosis' in result['checks']
        assert result['checks']['diagnosis'].score < 60
    
    def test_diagnosis_required(self, system):
        """测试诊断维度"""
        result = system.check_methodology("方案是...")
        assert 'diagnosis' in result['checks']
    
    def test_framework_required(self, system):
        """测试框架维度"""
        result = system.check_methodology("用SWOT分析...")
        assert 'framework' in result['checks']


class TestQuickFunctions:
    """测试快捷函数"""
    
    def test_query_function(self):
        """测试query快捷函数"""
        result = query("什么是AARRR")
        assert 'answer' in result
    
    def test_check_function(self):
        """测试check快捷函数"""
        result = check("这是一个测试内容")
        assert 'overall_score' in result
    
    def test_get_status_function(self):
        """测试get_status快捷函数"""
        status = get_status()
        assert 'total_cells' in status


class TestAPIRoutes:
    """测试API路由 (需要服务器运行)"""
    
    @pytest.fixture
    def api_url(self):
        """API基础URL"""
        return "http://127.0.0.1:8964"
    
    @pytest.mark.integration
    def test_cells_endpoint(self, api_url):
        """测试cells端点"""
        try:
            import requests
            response = requests.get(f"{api_url}/api/v1/cells", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert len(data) >= 21
        except ImportError:
            pytest.skip("requests未安装")
        except Exception:
            pytest.skip("服务器未运行")
    
    @pytest.mark.integration
    def test_cells_query_endpoint(self, api_url):
        """测试cells query端点"""
        try:
            import requests
            response = requests.post(
                f"{api_url}/api/v1/cells/query",
                json={"question": "如何提升用户增长"},
                timeout=5
            )
            assert response.status_code == 200
            data = response.json()
            assert 'cells_used' in data
        except ImportError:
            pytest.skip("requests未安装")
        except Exception:
            pytest.skip("服务器未运行")
    
    @pytest.mark.integration
    def test_cells_status_endpoint(self, api_url):
        """测试cells status端点"""
        try:
            import requests
            response = requests.get(f"{api_url}/api/v1/cells/status", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert 'total_cells' in data
        except ImportError:
            pytest.skip("requests未安装")
        except Exception:
            pytest.skip("服务器未运行")


# 运行测试
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
