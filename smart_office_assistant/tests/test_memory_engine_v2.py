"""神经记忆系统v2单元测试
Neural Memory System V2 Unit Tests
"""

import sys
from pathlib import Path
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import tempfile
import shutil
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

from src.neural_memory.memory_engine_v2 import (

    MemoryEngineV2,
    MemoryType,
    MemoryTier,
    MemoryMetadata,
    MemoryQuery,
    MemoryStatistics,
    StorageStats
)


class TestMemoryType(unittest.TestCase):
    """记忆类型测试"""
    
    def test_all_memory_types(self):
        """测试所有记忆类型"""
        types = [
            MemoryType.SENSORY,
            MemoryType.WORKING,
            MemoryType.LONG_TERM,
            MemoryType.PROCEDURAL,
            MemoryType.SEMANTIC,
            MemoryType.EPISODIC
        ]
        
        self.assertEqual(len(types), 6)
        for t in types:
            self.assertIsInstance(t.value, str)


class TestMemoryTier(unittest.TestCase):
    """记忆分层测试"""
    
    def test_all_tiers(self):
        """测试所有分层"""
        tiers = [MemoryTier.HOT, MemoryTier.WARM, MemoryTier.COLD]
        
        self.assertEqual(len(tiers), 3)
        for tier in tiers:
            self.assertIsInstance(tier.value, str)
    
    def test_tier_priority(self):
        """测试分层优先级"""
        self.assertEqual(MemoryTier.HOT.priority, 1)
        self.assertEqual(MemoryTier.WARM.priority, 2)
        self.assertEqual(MemoryTier.COLD.priority, 3)


class TestMemoryMetadata(unittest.TestCase):
    """记忆元数据测试"""
    
    def test_metadata_creation(self):
        """测试元数据创建"""
        metadata = MemoryMetadata(
            memory_type=MemoryType.WORKING,
            tier=MemoryTier.HOT,
            activation=0.8,
            access_count=10
        )
        
        self.assertEqual(metadata.memory_type, MemoryType.WORKING)
        self.assertEqual(metadata.tier, MemoryTier.HOT)
        self.assertEqual(metadata.activation, 0.8)
        self.assertEqual(metadata.access_count, 10)
    
    def test_metadata_to_dict(self):
        """测试元数据序列化"""
        metadata = MemoryMetadata(
            memory_type=MemoryType.LONG_TERM,
            tier=MemoryTier.WARM
        )
        
        metadata_dict = metadata.to_dict()
        
        self.assertIn('memory_type', metadata_dict)
        self.assertIn('tier', metadata_dict)
        self.assertIn('activation', metadata_dict)
    
    def test_metadata_update_activation(self):
        """测试更新激活度"""
        metadata = MemoryMetadata(
            memory_type=MemoryType.WORKING,
            activation=0.5
        )
        
        metadata.update_activation(delta=0.3)
        self.assertEqual(metadata.activation, 0.8)
        
        metadata.update_activation(delta=-0.5)
        self.assertEqual(metadata.activation, 0.3)  # 最小值限制


class TestMemoryQuery(unittest.TestCase):
    """记忆查询测试"""
    
    def test_query_creation(self):
        """测试查询创建"""
        query = MemoryQuery(
            query_text="测试查询",
            memory_types=[MemoryType.WORKING],
            top_k=5,
            min_activation=0.5
        )
        
        self.assertEqual(query.query_text, "测试查询")
        self.assertEqual(query.top_k, 5)
        self.assertEqual(query.min_activation, 0.5)
    
    def test_query_defaults(self):
        """测试查询默认值"""
        query = MemoryQuery(query_text="测试")
        
        self.assertEqual(query.top_k, 10)
        self.assertEqual(query.min_activation, 0.0)
        self.assertIsNone(query.memory_types)
    
    def test_query_validation(self):
        """测试查询验证"""
        query = MemoryQuery(query_text="")
        
        self.assertFalse(query.is_valid())
        
        query.query_text = "有效查询"
        self.assertTrue(query.is_valid())


class TestMemoryStatistics(unittest.TestCase):
    """记忆统计测试"""
    
    def test_statistics_creation(self):
        """测试统计创建"""
        stats = MemoryStatistics(
            total_memories=1000,
            by_tier={
                MemoryTier.HOT: 100,
                MemoryTier.WARM: 400,
                MemoryTier.COLD: 500
            },
            by_type={
                MemoryType.WORKING: 200,
                MemoryType.LONG_TERM: 800
            }
        )
        
        self.assertEqual(stats.total_memories, 1000)
        self.assertEqual(stats.by_tier[MemoryTier.HOT], 100)
        self.assertEqual(stats.by_type[MemoryType.LONG_TERM], 800)
    
    def test_statistics_update(self):
        """测试统计更新"""
        stats = MemoryStatistics()
        
        stats.update(
            tier=MemoryTier.HOT,
            memory_type=MemoryType.WORKING
        )
        
        self.assertEqual(stats.total_memories, 1)
        self.assertEqual(stats.by_tier[MemoryTier.HOT], 1)
        self.assertEqual(stats.by_type[MemoryType.WORKING], 1)


class TestStorageStats(unittest.TestCase):
    """存储统计测试"""
    
    def test_storage_stats_creation(self):
        """测试存储统计创建"""
        stats = StorageStats(
            total_memories=10000,
            hot_memories=1000,
            warm_memories=4000,
            cold_memories=5000,
            total_size_mb=100.0
        )
        
        self.assertEqual(stats.total_memories, 10000)
        self.assertEqual(stats.hot_memories, 1000)
        self.assertEqual(stats.total_size_mb, 100.0)
    
    def test_storage_efficiency(self):
        """测试存储效率"""
        stats = StorageStats(
            total_memories=10000,
            hot_memories=1000,
            total_size_mb=100.0
        )
        
        self.assertEqual(stats.storage_efficiency, 100)  # 10000/100


class TestMemoryEngineV2Init(unittest.TestCase):
    """记忆引擎v2初始化测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.temp_dir = tempfile.mkdtemp()
        self.config = {
            'hot_memory_limit': 500,
            'warm_memory_limit': 5000,
            'cold_memory_limit': 100000,
            'hnsw_m': 16,
            'hnsw_ef_construction': 100,
            'hnsw_ef_search': 50,
            'storage_path': self.temp_dir
        }
    
    def tearDown(self):
        """清理测试环境"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('src.neural_memory.memory_engine_v2.chromadb')
    def test_engine_initialization(self, mock_chromadb):
        """测试引擎初始化"""
        # Mock ChromaDB
        mock_client = Mock()
        mock_collection = Mock()
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_chromadb.PersistentClient.return_value = mock_client
        
        engine = MemoryEngineV2(self.config)
        
        self.assertIsNotNone(engine)
        self.assertEqual(engine.hot_memory_limit, 500)
        self.assertEqual(engine.warm_memory_limit, 5000)
        self.assertEqual(engine.cold_memory_limit, 100000)
    
    def test_default_config(self):
        """测试默认配置"""
        with patch('src.neural_memory.memory_engine_v2.chromadb'):
            engine = MemoryEngineV2({})
        
        self.assertEqual(engine.hot_memory_limit, 1000)
        self.assertEqual(engine.hnsw_m, 16)
        self.assertEqual(engine.hnsw_ef_search, 50)


class TestMemoryEngineV2Basic(unittest.TestCase):
    """记忆引擎v2基础功能测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.temp_dir = tempfile.mkdtemp()
        self.config = {
            'storage_path': self.temp_dir,
            'hot_memory_limit': 100,
            'hnsw_m': 8,
            'hnsw_ef_construction': 50,
            'hnsw_ef_search': 25
        }
        
        # Mock ChromaDB
        self.patcher = patch('src.neural_memory.memory_engine_v2.chromadb')
        mock_chromadb = self.patcher.start()
        
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.count.return_value = 0
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_chromadb.PersistentClient.return_value = mock_client
        
        self.engine = MemoryEngineV2(self.config)
        self.engine.initialize()
    
    def tearDown(self):
        """清理测试环境"""
        self.patcher.stop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_encode_memory(self):
        """测试记忆编码"""
        content = "这是一段测试内容"
        memory_type = MemoryType.WORKING
        
        memory_id = self.engine.encode_memory(
            content=content,
            memory_type=memory_type
        )
        
        self.assertIsNotNone(memory_id)
        self.assertIsInstance(memory_id, str)
    
    def test_retrieve_memory(self):
        """测试记忆检索"""
        # 先编码记忆
        content = "测试记忆内容"
        memory_id = self.engine.encode_memory(
            content=content,
            memory_type=MemoryType.WORKING
        )
        
        # 检索记忆
        query = MemoryQuery(query_text="测试")
        results = self.engine.retrieve(query)
        
        self.assertIsNotNone(results)
        self.assertGreater(len(results), 0)
    
    def test_retrieve_with_filters(self):
        """测试带过滤的记忆检索"""
        content = "测试记忆"
        memory_id = self.engine.encode_memory(
            content=content,
            memory_type=MemoryType.LONG_TERM
        )
        
        query = MemoryQuery(
            query_text="测试",
            memory_types=[MemoryType.LONG_TERM]
        )
        results = self.engine.retrieve(query)
        
        # 应该只返回长期记忆
        for result in results:
            self.assertEqual(result['metadata']['memory_type'], 'long_term')


class TestMemoryEngineV2TierManagement(unittest.TestCase):
    """记忆引擎v2分层管理测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.temp_dir = tempfile.mkdtemp()
        self.config = {
            'storage_path': self.temp_dir,
            'hot_memory_limit': 50,
            'warm_memory_limit': 500,
            'cold_memory_limit': 5000
        }
        
        # Mock ChromaDB
        self.patcher = patch('src.neural_memory.memory_engine_v2.chromadb')
        mock_chromadb = self.patcher.start()
        
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.count.return_value = 0
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_chromadb.PersistentClient.return_value = mock_client
        
        self.engine = MemoryEngineV2(self.config)
        self.engine.initialize()
    
    def tearDown(self):
        """清理测试环境"""
        self.patcher.stop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_promote_memory_hot_to_warm(self):
        """测试记忆升级：热→温"""
        # 编码多个记忆，超过热记忆限制
        for i in range(60):
            self.engine.encode_memory(
                content=f"记忆内容{i}",
                memory_type=MemoryType.WORKING
            )
        
        # 触发分层管理
        self.engine.manage_memory_tiers()
        
        # 验证热记忆不超过限制
        hot_count = len(self.engine.hot_memory)
        self.assertLessEqual(hot_count, 50)
    
    def test_demote_memory_warm_to_cold(self):
        """测试记忆降级：温→冷"""
        # 编码大量记忆
        for i in range(600):
            self.engine.encode_memory(
                content=f"记忆内容{i}",
                memory_type=MemoryType.LONG_TERM
            )
        
        # 触发分层管理
        self.engine.manage_memory_tiers()
        
        # 验证温记忆不超过限制
        warm_count = len(self.engine.warm_memory)
        self.assertLessEqual(warm_count, 500)
    
    def test_memory_activation_update(self):
        """测试记忆激活度更新"""
        content = "测试记忆"
        memory_id = self.engine.encode_memory(
            content=content,
            memory_type=MemoryType.WORKING
        )
        
        # 检索记忆（应该更新激活度）
        query = MemoryQuery(query_text="测试")
        self.engine.retrieve(query)
        
        # 验证激活度已更新
        if memory_id in self.engine.memory_metadata:
            self.assertGreater(
                self.engine.memory_metadata[memory_id].activation,
                0
            )


class TestMemoryEngineV2Forgetting(unittest.TestCase):
    """记忆引擎v2遗忘机制测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.temp_dir = tempfile.mkdtemp()
        self.config = {
            'storage_path': self.temp_dir,
            'enable_forgetting': True
        }
        
        # Mock ChromaDB
        self.patcher = patch('src.neural_memory.memory_engine_v2.chromadb')
        mock_chromadb = self.patcher.start()
        
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.count.return_value = 0
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_chromadb.PersistentClient.return_value = mock_client
        
        self.engine = MemoryEngineV2(self.config)
        self.engine.initialize()
    
    def tearDown(self):
        """清理测试环境"""
        self.patcher.stop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_apply_forgetting_curve(self):
        """测试应用遗忘曲线"""
        content = "测试记忆"
        memory_id = self.engine.encode_memory(
            content=content,
            memory_type=MemoryType.WORKING
        )
        
        # 设置初始激活度
        if memory_id in self.engine.memory_metadata:
            self.engine.memory_metadata[memory_id].activation = 1.0
        
        # 模拟时间流逝
        time.sleep(0.1)
        
        # 应用遗忘曲线
        self.engine.apply_forgetting_curve()
        
        # 验证激活度下降
        if memory_id in self.engine.memory_metadata:
            activation = self.engine.memory_metadata[memory_id].activation
            self.assertLess(activation, 1.0)
    
    def test_prune_low_activation_memories(self):
        """测试修剪低激活度记忆"""
        # 编码记忆
        for i in range(10):
            memory_id = self.engine.encode_memory(
                content=f"记忆内容{i}",
                memory_type=MemoryType.WORKING
            )
            
            # 设置低激活度
            if memory_id in self.engine.memory_metadata:
                self.engine.memory_metadata[memory_id].activation = 0.1
        
        # 修剪低激活度记忆
        pruned_count = self.engine.prune_low_activation_memories(threshold=0.2)
        
        self.assertGreater(pruned_count, 0)


class TestMemoryEngineV2Statistics(unittest.TestCase):
    """记忆引擎v2统计测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.temp_dir = tempfile.mkdtemp()
        self.config = {
            'storage_path': self.temp_dir
        }
        
        # Mock ChromaDB
        self.patcher = patch('src.neural_memory.memory_engine_v2.chromadb')
        mock_chromadb = self.patcher.start()
        
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.count.return_value = 0
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_chromadb.PersistentClient.return_value = mock_client
        
        self.engine = MemoryEngineV2(self.config)
        self.engine.initialize()
    
    def tearDown(self):
        """清理测试环境"""
        self.patcher.stop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_get_statistics(self):
        """测试获取统计"""
        # 编码一些记忆
        for i in range(10):
            self.engine.encode_memory(
                content=f"记忆内容{i}",
                memory_type=MemoryType.WORKING
            )
        
        stats = self.engine.get_statistics()
        
        self.assertIsNotNone(stats)
        self.assertEqual(stats.total_memories, 10)
        self.assertIn(MemoryType.WORKING, stats.by_type)
    
    def test_get_storage_stats(self):
        """测试获取存储统计"""
        storage_stats = self.engine.get_storage_stats()
        
        self.assertIsNotNone(storage_stats)
        self.assertGreaterEqual(storage_stats.total_memories, 0)
    
    def test_export_statistics(self):
        """测试导出统计"""
        stats = self.engine.get_statistics()
        
        report_path = self.engine.export_statistics()
        
        self.assertTrue(Path(report_path).exists())
        
        # 清理
        Path(report_path).unlink()


class TestMemoryEngineV2Performance(unittest.TestCase):
    """记忆引擎v2性能测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.temp_dir = tempfile.mkdtemp()
        self.config = {
            'storage_path': self.temp_dir,
            'hnsw_m': 8,
            'hnsw_ef_search': 20
        }
        
        # Mock ChromaDB
        self.patcher = patch('src.neural_memory.memory_engine_v2.chromadb')
        mock_chromadb = self.patcher.start()
        
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.count.return_value = 0
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_chromadb.PersistentClient.return_value = mock_client
        
        self.engine = MemoryEngineV2(self.config)
        self.engine.initialize()
    
    def tearDown(self):
        """清理测试环境"""
        self.patcher.stop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_retrieval_performance(self):
        """测试检索性能"""
        # 编码记忆
        for i in range(100):
            self.engine.encode_memory(
                content=f"记忆内容{i}",
                memory_type=MemoryType.WORKING
            )
        
        # 测试检索速度
        start_time = time.time()
        
        query = MemoryQuery(query_text="测试")
        results = self.engine.retrieve(query)
        
        elapsed_time = time.time() - start_time
        
        # 验证检索在合理时间内完成
        self.assertLess(elapsed_time, 1.0)
        self.assertGreater(len(results), 0)
    
    def test_batch_encode_performance(self):
        """测试批量编码性能"""
        # 批量编码
        start_time = time.time()
        
        for i in range(100):
            self.engine.encode_memory(
                content=f"记忆内容{i}",
                memory_type=MemoryType.WORKING
            )
        
        elapsed_time = time.time() - start_time
        
        # 验证批量编码在合理时间内完成
        self.assertLess(elapsed_time, 10.0)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryType))
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryTier))
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryMetadata))
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryQuery))
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryStatistics))
    suite.addTests(loader.loadTestsFromTestCase(TestStorageStats))
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryEngineV2Init))
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryEngineV2Basic))
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryEngineV2TierManagement))
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryEngineV2Forgetting))
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryEngineV2Statistics))
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryEngineV2Performance))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    import time
    start_time = time.time()
    
    success = run_tests()
    
    elapsed_time = time.time() - start_time
    
    print(f"\n{'='*60}")
    print(f"测试完成! 总耗时: {elapsed_time:.2f}秒")
    print(f"结果: {'✅ 全部通过' if success else '❌ 存在失败'}")
    print(f"{'='*60}\n")
    
    sys.exit(0 if success else 1)
