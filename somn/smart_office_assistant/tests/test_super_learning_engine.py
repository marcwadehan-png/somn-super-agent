"""超级学习引擎单元测试
Super Learning Engine Unit Tests
"""

import sys
from pathlib import Path
import unittest
from unittest.mock import Mock, patch
import tempfile
import shutil
import time

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

from src.intelligence.super_learning_engine import (
    SuperLearningEngine,
    LearningCapability,
    LearningRequest,
    LearningResult,
    LearningStats,
    EngineLoadInfo,
)


class SuperLearningEngineTestCase(unittest.TestCase):
    """带依赖补丁的基础测试类。"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.patchers = [
            patch("src.intelligence.super_learning_engine.UnifiedLearningSystem"),
            patch("src.intelligence.super_learning_engine.NeuralLearningEngine"),
            patch("src.intelligence.super_learning_engine.SmartLearningEngine"),
            patch("src.intelligence.super_learning_engine.CoreLearningEngine"),
        ]
        self.mocks = [patcher.start() for patcher in self.patchers]

    def tearDown(self):
        for patcher in reversed(self.patchers):
            patcher.stop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def build_engine(self, **overrides) -> SuperLearningEngine:
        config = {
            "storage_path": self.temp_dir,
            "max_workers": 2,
            "enable_parallel": True,
            "enable_learning_stats": True,
        }
        config.update(overrides)
        return SuperLearningEngine(config)


class TestLearningModels(unittest.TestCase):
    """数据模型测试。"""

    def test_all_capabilities_defined(self):
        capabilities = list(LearningCapability)
        self.assertEqual(len(capabilities), 12)
        self.assertIn(LearningCapability.META_LEARNING, capabilities)
        self.assertIn(LearningCapability.NARRATIVE_LEARNING, capabilities)

    def test_learning_request_defaults_and_auto_id(self):
        request = LearningRequest(
            capability=LearningCapability.NEURAL_LEARNING,
            input_data=None,
        )

        self.assertTrue(request.request_id.startswith("learning_"))
        self.assertEqual(request.priority, 5)
        self.assertIsNone(request.timeout)
        self.assertEqual(request.input_data, {})

    def test_learning_result_failure_defaults(self):
        result = LearningResult(
            capability=LearningCapability.ERROR_LEARNING,
            success=False,
            error="学习失败",
        )

        self.assertFalse(result.success)
        self.assertEqual(result.error, "学习失败")
        self.assertEqual(result.data, {})
        self.assertEqual(result.confidence, 0.0)

    def test_learning_stats_update(self):
        stats = LearningStats()
        stats.update(True, 0.5)
        stats.update(False, 0.3)
        stats.update_by_capability(LearningCapability.INSTANCE_LEARNING, True, 0.5)

        self.assertEqual(stats.total_requests, 2)
        self.assertEqual(stats.successful_requests, 1)
        self.assertAlmostEqual(stats.total_execution_time, 0.8)
        self.assertAlmostEqual(stats.success_rate, 0.5)
        self.assertIn(LearningCapability.INSTANCE_LEARNING.value, stats.capability_breakdown)

    def test_engine_load_info_properties(self):
        load = EngineLoadInfo(name="neural", active_tasks=5, queue_size=10, avg_response_time=0.2)

        self.assertEqual(load.name, "neural")
        self.assertEqual(load.load_score, 0.5)
        self.assertFalse(load.is_overloaded)


class TestSuperLearningEngineInit(SuperLearningEngineTestCase):
    """初始化与映射测试。"""

    def test_engine_initialization(self):
        engine = self.build_engine(max_workers=3)
        self.addCleanup(engine.close)

        self.assertEqual(engine.max_workers, 3)
        self.assertTrue(engine.enable_parallel)
        self.assertTrue(engine.enable_learning_stats)
        self.assertIn(LearningCapability.INSTANCE_LEARNING, engine.capability_engine_map)
        self.assertEqual(
            engine.capability_to_engine_mapping[LearningCapability.INSTANCE_LEARNING.value],
            "neural",
        )

    def test_compat_config_keys(self):
        engine = self.build_engine(base_path=self.temp_dir, max_workers=4)
        self.addCleanup(engine.close)

        self.assertEqual(str(engine.base_path), self.temp_dir)
        self.assertEqual(engine.max_workers, 4)


class TestSuperLearningEngineRouting(SuperLearningEngineTestCase):
    """路由与注册测试。"""

    def setUp(self):
        super().setUp()
        self.engine = self.build_engine()

    def tearDown(self):
        self.engine.close()
        super().tearDown()

    def test_register_engine(self):
        mock_engine = Mock(name="custom_engine")
        self.engine.register_engine("custom", mock_engine)

        self.assertIs(self.engine.engines["custom"], mock_engine)

    def test_get_engine_by_capability(self):
        neural = Mock()
        self.engine.engines["neural"] = neural

        result = self.engine.get_engine_by_capability(LearningCapability.INSTANCE_LEARNING)
        self.assertIs(result, neural)

    def test_route_request_to_engine(self):
        smart = Mock()
        self.engine.engines.pop("neural", None)
        self.engine.engines["smart"] = smart
        request = LearningRequest(
            request_id="route_001",
            capability=LearningCapability.INSTANCE_LEARNING,
            input_data={"demo": True},
        )

        result = self.engine.route_request_to_engine(request)
        self.assertIs(result, smart)


class TestSuperLearningEngineLearning(SuperLearningEngineTestCase):
    """学习执行测试。"""

    def setUp(self):
        super().setUp()
        self.engine = self.build_engine()

    def tearDown(self):
        self.engine.close()
        super().tearDown()

    def test_learn_single_request(self):
        mock_engine = Mock()
        mock_engine.learn.return_value = {"result": "success"}
        self.engine.engines["neural"] = mock_engine

        request = LearningRequest(
            request_id="learn_001",
            capability=LearningCapability.INSTANCE_LEARNING,
            input_data={"item": "example"},
        )
        result = self.engine.learn(request)

        self.assertTrue(result.success)
        self.assertEqual(result.engine_used, "neural")
        # learning_type 存储的是 NeuralLearningType 枚举的中文 .value（例如 "实例学习"）
        self.assertIn("learning_type", result.data)
        self.assertIsInstance(result.data["learning_type"], str)
        self.assertGreater(len(result.data["learning_type"]), 0)
        self.assertGreaterEqual(result.execution_time, 0.0)

    def test_learn_with_timeout(self):
        def slow_learn(*args, **kwargs):
            time.sleep(0.1)
            return {"result": "slow_success"}

        mock_engine = Mock()
        mock_engine.learn.side_effect = slow_learn
        self.engine.engines["neural"] = mock_engine

        request = LearningRequest(
            request_id="timeout_001",
            capability=LearningCapability.NEURAL_LEARNING,
            input_data={"item": "example"},
            timeout=0.01,
        )
        result = self.engine.learn(request)

        self.assertFalse(result.success)
        self.assertIn("超时", result.error)

    def test_meta_learning(self):
        history_result = LearningResult(
            request_id="history_001",
            capability=LearningCapability.INSTANCE_LEARNING,
            success=True,
            data={"ok": True},
            engine_used="neural",
            execution_time=0.2,
        )
        self.engine.learning_history.append(history_result)
        self.engine._update_stats(history_result)

        request = LearningRequest(
            request_id="meta_001",
            capability=LearningCapability.META_LEARNING,
            input_data={"target_capability": LearningCapability.INSTANCE_LEARNING.value},
        )
        result = self.engine.learn(request)

        self.assertTrue(result.success)
        self.assertEqual(result.engine_used, "super")
        self.assertIn("recommendations", result.data)
        self.assertGreaterEqual(len(result.data["recommendations"]), 1)

    def test_narrative_learning(self):
        request = LearningRequest(
            request_id="narrative_001",
            capability=LearningCapability.NARRATIVE_LEARNING,
            input_data={
                "content": "后来他在困境中坚持，终于迎来突破。",
                "source": "unit_test",
                "narrative_type": "brand_story",
            },
        )
        result = self.engine.learn(request)

        self.assertTrue(result.success)
        self.assertEqual(result.engine_used, "narrative")
        self.assertIn("narrative_insights", result.data)
        self.assertIn("knowledge_extracted", result.data)

    def test_parallel_learn(self):
        mock_engine = Mock()
        mock_engine.learn.return_value = {"result": "success"}
        self.engine.engines["neural"] = mock_engine

        requests = [
            LearningRequest(
                request_id=f"parallel_{i}",
                capability=LearningCapability.INSTANCE_LEARNING,
                input_data={"item": i},
            )
            for i in range(3)
        ]
        results = self.engine.learn_parallel(requests)

        self.assertEqual(len(results), 3)
        self.assertTrue(all(result.success for result in results))


class TestSuperLearningEngineObservability(SuperLearningEngineTestCase):
    """统计与引擎信息测试。"""

    def setUp(self):
        super().setUp()
        self.engine = self.build_engine()

    def tearDown(self):
        self.engine.close()
        super().tearDown()

    def test_get_stats_and_stats_by_capability(self):
        mock_engine = Mock()
        mock_engine.learn.return_value = {"result": "success"}
        self.engine.engines["neural"] = mock_engine

        request = LearningRequest(
            request_id="stats_001",
            capability=LearningCapability.INSTANCE_LEARNING,
            input_data={"item": "example"},
        )
        self.engine.learn(request)

        stats = self.engine.get_stats()
        capability_stats = self.engine.get_stats_by_capability(LearningCapability.INSTANCE_LEARNING)

        self.assertEqual(stats["total_requests"], 1)
        self.assertEqual(stats["successful_requests"], 1)
        self.assertEqual(capability_stats.total_requests, 1)
        self.assertEqual(capability_stats.successful_requests, 1)

    def test_get_engine_info_and_all_engine_info(self):
        info = self.engine.get_engine_info("neural")
        all_info = self.engine.get_all_engine_info()

        self.assertIsNotNone(info)
        self.assertEqual(info.name, "neural")
        self.assertIn("neural", all_info)


if __name__ == "__main__":
    unittest.main(verbosity=2)
