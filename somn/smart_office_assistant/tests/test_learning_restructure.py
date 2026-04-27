"""
__all__ = [
    'test_create_knowledge_item',
    'test_create_principle',
    'test_create_scheduler',
    'test_evaluate_knowledge',
    'test_import',
    'test_import_from_core_init',
    'test_import_from_engine',
    'test_import_from_learning_root_compat',
    'test_import_from_neural_init',
    'test_instantiate',
    'test_instantiate_engine',
    'test_submit_task',
    'test_super_learning_engine',
]

src/learning 模块单元测试
验证重构后所有子模块导入正常、核心类可实例化、对外 API 不变
"""

import sys
import os
import unittest

# 确保 project root 在 sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
SRC_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

class TestEngineSmartLearning(unittest.TestCase):
    """smart_learning_engine 测试"""

    def test_import_from_engine(self):
        from src.learning.engine.smart_learning_engine import SmartLearningEngine, KnowledgeItem, create_knowledge_item
        self.assertIsNotNone(SmartLearningEngine)
        self.assertIsNotNone(KnowledgeItem)
        self.assertIsNotNone(create_knowledge_item)

    def test_import_from_learning_root_compat(self):
        from src.learning import SmartLearningEngine, KnowledgeItem, create_knowledge_item
        self.assertIsNotNone(SmartLearningEngine)

    def test_instantiate_engine(self):
        from src.learning.engine.smart_learning_engine import SmartLearningEngine, create_knowledge_item
        engine = SmartLearningEngine()
        self.assertIsNotNone(engine)
        self.assertIsInstance(engine.knowledge_base, dict)
        self.assertIsInstance(engine.decision_history, list)

    def test_create_knowledge_item(self):
        from src.learning.engine.smart_learning_engine import create_knowledge_item, KnowledgeQuality, RelevanceLevel
        item = create_knowledge_item("test_source", {"key": "val"}, quality=4, relevance=4, confidence=0.8)
        self.assertEqual(item.source, "test_source")
        self.assertEqual(item.quality, KnowledgeQuality.HIGH)
        self.assertEqual(item.relevance, RelevanceLevel.HIGH)
        self.assertAlmostEqual(item.confidence, 0.8)

    def test_evaluate_knowledge(self):
        from src.learning.engine.smart_learning_engine import SmartLearningEngine, create_knowledge_item
        engine = SmartLearningEngine()
        item = create_knowledge_item("test", "content", quality=5, relevance=5, confidence=0.9)
        result = engine.evaluate_knowledge(item)
        self.assertIn("recommendation", result)
        self.assertIn("priority", result)
        self.assertGreater(result["priority"], 0)

class TestEngineLocalDataLearner(unittest.TestCase):
    """local_data_learner 测试"""

    def test_import(self):
        from src.learning.engine.local_data_learner import LocalDataLearner, FileType, FileCategory
        self.assertIsNotNone(LocalDataLearner)
        self.assertIsNotNone(FileType)
        self.assertIsNotNone(FileCategory)

    def test_instantiate(self):
        from src.learning.engine.local_data_learner import LocalDataLearner
        learner = LocalDataLearner(target_drive="C:")
        self.assertIsNotNone(learner)
        self.assertEqual(learner.target_drive, "C:")

class TestEnginePPTStyleLearner(unittest.TestCase):
    """ppt_style_learner 测试"""

    def test_import_from_engine(self):
        from src.learning.engine.ppt_style_learner import PPTStyleLearner, DesignPrinciple, create_principle
        self.assertIsNotNone(PPTStyleLearner)

    def test_import_from_learning_root_compat(self):
        from src.learning import PPTStyleLearner, DesignPrinciple, create_principle
        self.assertIsNotNone(PPTStyleLearner)

    def test_create_principle(self):
        from src.learning.engine.ppt_style_learner import create_principle
        p = create_principle("Test Principle", "A test", "unit_test", "visual", 4)
        self.assertEqual(p.name, "Test Principle")
        self.assertEqual(p.quality, 4)

class TestCoreCoordinator(unittest.TestCase):
    """coordinator 测试"""

    def test_import(self):
        from src.learning.core.coordinator import LearningCoordinator, LearningTask, LearningPriority, TaskStatus
        self.assertIsNotNone(LearningCoordinator)
        self.assertIsNotNone(LearningTask)
        self.assertIsNotNone(LearningPriority)
        self.assertIsNotNone(TaskStatus)

    def test_instantiate(self):
        from src.learning.core.coordinator import LearningCoordinator
        coord = LearningCoordinator(max_workers=2)
        self.assertIsNotNone(coord)
        self.assertEqual(coord.max_workers, 2)

    def test_submit_task(self):
        from src.learning.core.coordinator import LearningCoordinator, LearningTask, LearningPriority
        coord = LearningCoordinator(max_workers=1)
        task = LearningTask(task_id="test_001", engine_type="test", priority=LearningPriority.P1_HIGH)
        task_id = coord.submit_task(task)
        self.assertEqual(task_id, "test_001")
        self.assertEqual(len(coord.task_queue), 1)

    def test_import_from_core_init(self):
        from src.learning.core import LearningCoordinator, SmartScheduler
        self.assertIsNotNone(LearningCoordinator)
        self.assertIsNotNone(SmartScheduler)

class TestCoreSmartScheduler(unittest.TestCase):
    """smart_scheduler 测试"""

    def test_import(self):
        from src.learning.core.smart_scheduler import SmartScheduler, SchedulingStrategy, create_scheduler
        self.assertIsNotNone(SmartScheduler)
        self.assertIsNotNone(SchedulingStrategy)
        self.assertIsNotNone(create_scheduler)

    def test_create_scheduler(self):
        from src.learning.core.smart_scheduler import create_scheduler
        scheduler = create_scheduler("adaptive")
        self.assertIsNotNone(scheduler)
        self.assertEqual(scheduler.strategy.value, "adaptive")

class TestUnifiedLearningSystem(unittest.TestCase):
    """unified_learning_system 测试"""

    def test_import(self):
        from src.learning.unified_learning_system import UnifiedLearningSystem, UnifiedLearningConfig
        self.assertIsNotNone(UnifiedLearningSystem)
        self.assertIsNotNone(UnifiedLearningConfig)

    def test_instantiate(self):
        from src.learning.unified_learning_system import UnifiedLearningSystem, UnifiedLearningConfig
        config = UnifiedLearningConfig(target_drive="C:", max_concurrent_tasks=2)
        system = UnifiedLearningSystem(config)
        self.assertIsNotNone(system)

class TestNeuralAdaptive(unittest.TestCase):
    """adaptive_learning_coordinator 测试"""

    def test_import(self):
        from src.learning.neural.adaptive_learning_coordinator import AdaptiveLearningCoordinator
        self.assertIsNotNone(AdaptiveLearningCoordinator)

    def test_import_from_neural_init(self):
        from src.learning.neural import AdaptiveLearningCoordinator, LearningStage
        self.assertIsNotNone(AdaptiveLearningCoordinator)
        self.assertIsNotNone(LearningStage)

    def test_instantiate(self):
        from src.learning.neural.adaptive_learning_coordinator import AdaptiveLearningCoordinator
        coord = AdaptiveLearningCoordinator()
        self.assertIsNotNone(coord)

class TestExternalCallers(unittest.TestCase):
    """验证外部调用者的 import 路径仍有效"""

    def test_super_learning_engine(self):
        from src.intelligence.super_learning_engine import SuperLearningEngine, UnifiedLearningSystem, SmartLearningEngine
        self.assertIsNotNone(SuperLearningEngine)
        self.assertIsNotNone(UnifiedLearningSystem)
        self.assertIsNotNone(SmartLearningEngine)

if __name__ == "__main__":
    raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
