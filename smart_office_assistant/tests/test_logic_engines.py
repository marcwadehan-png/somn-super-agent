"""
逻辑学引擎测试套件
测试基于柯匹《逻辑学导论》实现的所有逻辑引擎

作者: AI工程师
创建时间: 2026-03-31
版本: 1.0.0
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

from logic.categorical_logic import CategoricalLogicEngine

from logic.syllogism_validator import SyllogismValidator
from logic.propositional_logic import (
    PropositionalLogicEngine,
    Proposition,
    LogicalOperator
)
from logic.fallacy_detector import FallacyDetector
from neural_memory.logic_integration import LogicIntegration


class TestCategoricalLogicEngine(unittest.TestCase):
    """测试直言命题逻辑引擎"""
    
    def setUp(self):
        self.engine = CategoricalLogicEngine()
    
    def test_parse_a_proposition(self):
        """测试A命题解析"""
        prop = self.engine.parse_proposition("所有人类都是理性的")
        self.assertIsNotNone(prop)
        self.assertEqual(prop.type.value, "A")
        self.assertEqual(prop.subject, "人类")
        self.assertEqual(prop.predicate, "理性的")
    
    def test_parse_e_proposition(self):
        """测试E命题解析"""
        prop = self.engine.parse_proposition("没有独角兽是哺乳动物")
        self.assertIsNotNone(prop)
        self.assertEqual(prop.type.value, "E")
    
    def test_parse_i_proposition(self):
        """测试I命题解析"""
        prop = self.engine.parse_proposition("有些学生是勤奋的")
        self.assertIsNotNone(prop)
        self.assertEqual(prop.type.value, "I")
    
    def test_parse_o_proposition(self):
        """测试O命题解析"""
        prop = self.engine.parse_proposition("有些学生不是勤奋的")
        self.assertIsNotNone(prop)
        self.assertEqual(prop.type.value, "O")
    
    def test_check_contradictory(self):
        """测试矛盾关系"""
        prop1 = self.engine.parse_proposition("所有S都是P")
        prop2 = self.engine.parse_proposition("有些S不是P")
        relation = self.engine.check_relationship(prop1, prop2)
        self.assertEqual(relation, "contradictory")
    
    def test_check_subcontrary(self):
        """测试下反对关系"""
        prop1 = self.engine.parse_proposition("有些S是P")
        prop2 = self.engine.parse_proposition("有些S不是P")
        relation = self.engine.check_relationship(prop1, prop2)
        self.assertEqual(relation, "subcontrary")
    
    def test_check_distribution_a(self):
        """测试A命题的周延性"""
        prop = self.engine.parse_proposition("所有S都是P")
        self.assertTrue(prop.subject_distributed)
        self.assertFalse(prop.predicate_distributed)
    
    def test_check_distribution_e(self):
        """测试E命题的周延性"""
        prop = self.engine.parse_proposition("没有S是P")
        self.assertTrue(prop.subject_distributed)
        self.assertTrue(prop.predicate_distributed)


class TestSyllogismValidator(unittest.TestCase):
    """测试三段论验证器"""
    
    def setUp(self):
        self.validator = SyllogismValidator()
    
    def test_valid_barbara(self):
        """测试有效的Barbara式 (AAA-1)"""
        result = self.validator.validate(
            "所有M都是P",
            "所有S都是M",
            "所有S都是P"
        )
        self.assertTrue(result['is_valid'])
        self.assertEqual(result['figure'], 1)
        self.assertEqual(result['mood'], 'AAA')
    
    def test_valid_celarent(self):
        """测试有效的Celarent式 (EAE-1)"""
        result = self.validator.validate(
            "没有M是P",
            "所有S都是M",
            "没有S是P"
        )
        self.assertTrue(result['is_valid'])
        self.assertEqual(result['mood'], 'EAE')
    
    def test_valid_darii(self):
        """测试有效的Darii式 (AII-1)"""
        result = self.validator.validate(
            "所有M都是P",
            "有些S是M",
            "有些S是P"
        )
        self.assertTrue(result['is_valid'])
        self.assertEqual(result['mood'], 'AII')
    
    def test_valid_ferio(self):
        """测试有效的Ferio式 (EIO-1)"""
        result = self.validator.validate(
            "没有M是P",
            "有些S是M",
            "有些S不是P"
        )
        self.assertTrue(result['is_valid'])
        self.assertEqual(result['mood'], 'EIO')
    
    def test_invalid_undistributed_middle(self):
        """测试中项不周延谬误"""
        result = self.validator.validate(
            "所有P都是M",
            "所有S都是M",
            "所有S都是P"
        )
        self.assertFalse(result['is_valid'])
        self.assertIn("undistributed", str(result['errors']).lower())
    
    def test_invalid_two_negative_premises(self):
        """测试双否定前提谬误"""
        result = self.validator.validate(
            "没有P是M",
            "没有S是M",
            "没有S是P"
        )
        self.assertFalse(result['is_valid'])
        self.assertTrue(any("negative" in err.lower() for err in result['errors']))
    
    def test_invalid_affirmative_from_negative(self):
        """测试否定前提肯定结论谬误"""
        result = self.validator.validate(
            "没有P是M",
            "所有S都是P",
            "所有S都是M"
        )
        self.assertFalse(result['is_valid'])
        self.assertTrue(any("affirmative" in err.lower() for err in result['errors']))


class TestPropositionalLogicEngine(unittest.TestCase):
    """测试命题逻辑引擎"""
    
    def setUp(self):
        self.engine = PropositionalLogicEngine()
    
    def test_create_atomic_proposition(self):
        """测试创建原子命题"""
        P = self.engine.create_atomic_proposition("P")
        self.assertTrue(P.is_atomic)
        self.assertEqual(P.symbol, "P")
    
    def test_evaluate_conjunction(self):
        """测试合取运算"""
        P = self.engine.create_atomic_proposition("P")
        Q = self.engine.create_atomic_proposition("Q")
        and_prop = self.engine.create_compound_proposition(LogicalOperator.AND, [P, Q])
        
        # T ∧ T = T
        result = self.engine.evaluate_truth_value(and_prop, {"P": True, "Q": True})
        self.assertTrue(result)
        
        # T ∧ F = F
        result = self.engine.evaluate_truth_value(and_prop, {"P": True, "Q": False})
        self.assertFalse(result)
    
    def test_evaluate_disjunction(self):
        """测试析取运算"""
        P = self.engine.create_atomic_proposition("P")
        Q = self.engine.create_atomic_proposition("Q")
        or_prop = self.engine.create_compound_proposition(LogicalOperator.OR, [P, Q])
        
        # T ∨ F = T
        result = self.engine.evaluate_truth_value(or_prop, {"P": True, "Q": False})
        self.assertTrue(result)
        
        # F ∨ F = F
        result = self.engine.evaluate_truth_value(or_prop, {"P": False, "Q": False})
        self.assertFalse(result)
    
    def test_evaluate_implication(self):
        """测试蕴涵运算"""
        P = self.engine.create_atomic_proposition("P")
        Q = self.engine.create_atomic_proposition("Q")
        impl_prop = self.engine.create_compound_proposition(LogicalOperator.IMPLIES, [P, Q])
        
        # T → T = T
        result = self.engine.evaluate_truth_value(impl_prop, {"P": True, "Q": True})
        self.assertTrue(result)
        
        # T → F = F
        result = self.engine.evaluate_truth_value(impl_prop, {"P": True, "Q": False})
        self.assertFalse(result)
        
        # F → T = T
        result = self.engine.evaluate_truth_value(impl_prop, {"P": False, "Q": True})
        self.assertTrue(result)
        
        # F → F = T
        result = self.engine.evaluate_truth_value(impl_prop, {"P": False, "Q": False})
        self.assertTrue(result)
    
    def test_is_tautology(self):
        """测试重言式检测"""
        P = self.engine.create_atomic_proposition("P")
        
        # P ∨ ~P 是重言式
        not_P = self.engine.create_compound_proposition(LogicalOperator.NOT, [P])
        tautology = self.engine.create_compound_proposition(LogicalOperator.OR, [P, not_P])
        self.assertTrue(self.engine.is_tautology(tautology))
        
        # P ∧ ~P 是矛盾式
        contradiction = self.engine.create_compound_proposition(LogicalOperator.AND, [P, not_P])
        self.assertTrue(self.engine.is_contradiction(contradiction))
    
    def test_modus_ponens(self):
        """测试肯定前件律"""
        P = self.engine.create_atomic_proposition("P")
        Q = self.engine.create_atomic_proposition("Q")
        implies = self.engine.create_compound_proposition(LogicalOperator.IMPLIES, [P, Q])
        
        result = self.engine.modus_ponens(implies, P)
        self.assertEqual(result, Q)
    
    def test_modus_tollens(self):
        """测试否定后件律"""
        P = self.engine.create_atomic_proposition("P")
        Q = self.engine.create_atomic_proposition("Q")
        implies = self.engine.create_compound_proposition(LogicalOperator.IMPLIES, [P, Q])
        
        not_Q = self.engine.create_compound_proposition(LogicalOperator.NOT, [Q])
        result = self.engine.modus_tollens(implies, not_Q)
        
        expected = self.engine.create_compound_proposition(LogicalOperator.NOT, [P])
        self.assertEqual(str(result), str(expected))
    
    def test_check_equivalence(self):
        """测试等价性检查"""
        P = self.engine.create_atomic_proposition("P")
        Q = self.engine.create_atomic_proposition("Q")
        
        # P → Q 等价于 ~P ∨ Q
        implies = self.engine.create_compound_proposition(LogicalOperator.IMPLIES, [P, Q])
        not_P = self.engine.create_compound_proposition(LogicalOperator.NOT, [P])
        or_prop = self.engine.create_compound_proposition(LogicalOperator.OR, [not_P, Q])
        
        self.assertTrue(self.engine.check_equivalence(implies, or_prop))


class TestFallacyDetector(unittest.TestCase):
    """测试谬误检测器"""
    
    def setUp(self):
        self.detector = FallacyDetector()
    
    def test_detect_false_dilemma(self):
        """测试检测虚假二分法"""
        argument = "你要么支持我们,要么就是敌人"
        fallacies = self.detector.detect_informal_fallacies(argument)
        
        self.assertTrue(len(fallacies) > 0)
        self.assertTrue(any(f.fallacy_name == '虚假二分法' for f in fallacies))
    
    def test_detect_appeal_to_popularity(self):
        """测试检测诉诸大众"""
        argument = "大家都相信这个观点,所以它一定是正确的"
        fallacies = self.detector.detect_informal_fallacies(argument)
        
        self.assertTrue(len(fallacies) > 0)
        self.assertTrue(any('诉诸' in f.fallacy_name for f in fallacies))
    
    def test_detect_hasty_generalization(self):
        """测试检测草率概括"""
        argument = "我遇到的两个法国人都很粗鲁,所以法国人都很粗鲁"
        fallacies = self.detector.detect_informal_fallacies(argument)
        
        self.assertTrue(len(fallacies) > 0)
        self.assertTrue(any(f.fallacy_name == '草率概括' for f in fallacies))
    
    def test_analyze_argument_quality(self):
        """测试论证质量分析"""
        argument = "大家都说这个方法有效,专家也支持。如果你不认同,那你肯定是外行。只有两种选择:要么接受我的方法,要么失败。"
        
        report = self.detector.analyze_argument_quality(argument)
        
        self.assertIn('quality_score', report)
        self.assertIn('overall_assessment', report)
        self.assertLess(report['quality_score'], 1.0)  # 应该检测到问题


class TestLogicIntegration(unittest.TestCase):
    """测试逻辑学集成模块"""
    
    def setUp(self):
        self.integration = LogicIntegration()
    
    def test_validate_syllogism_integration(self):
        """测试三段论验证集成"""
        result = self.integration.validate_syllogism(
            "所有M都是P",
            "所有S都是M",
            "所有S都是P"
        )
        
        self.assertTrue(result.is_valid)
        self.assertGreater(result.confidence, 0.8)
    
    def test_detect_fallacies_integration(self):
        """测试谬误检测集成"""
        argument = "大家都认为这是对的,所以它就是对的。"
        fallacies = self.integration.detect_fallacies_in_argument(argument)
        
        self.assertTrue(len(fallacies) > 0)
    
    def test_analyze_logical_structure(self):
        """测试逻辑结构分析"""
        argument = "专家说这个产品很好,所以我们应该购买它"
        analysis = self.integration.analyze_logical_structure(argument)
        
        self.assertIn('fallacy_analysis', analysis)
        self.assertIn('argument_quality', analysis)
        self.assertIn('suggestions', analysis)
    
    def test_validate_reasoning_chain(self):
        """测试推理链验证"""
        reasoning_steps = [
            {'premise': '所有动物都需要食物', 'conclusion': '哺乳动物是动物'},
            {'premise': '哺乳动物是动物', 'conclusion': '哺乳动物需要食物'}
        ]
        
        result = self.integration.validate_reasoning_chain(reasoning_steps)
        
        self.assertIn('is_valid', result)
        self.assertIn('confidence', result)
    
    def test_extract_logical_patterns(self):
        """测试逻辑模式提取"""
        text = "所有A都是B。所有C都是A。所以所有C都是B。"
        patterns = self.integration.extract_logical_patterns(text)
        
        self.assertTrue(len(patterns) > 0)
        self.assertTrue(any(p['type'] == 'syllogism' for p in patterns))
    
    def test_logic_statistics(self):
        """测试逻辑学习统计"""
        # 先进行一些操作
        self.integration.validate_syllogism(
            "所有M都是P",
            "所有S都是M",
            "所有S都是P"
        )
        
        stats = self.integration.get_logic_statistics()
        
        self.assertIn('valid_syllogisms_count', stats)
        self.assertIn('detected_fallacies_count', stats)
        self.assertIn('learned_patterns_count', stats)


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试
    suite.addTests(loader.loadTestsFromTestCase(TestCategoricalLogicEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestSyllogismValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestPropositionalLogicEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestFallacyDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestLogicIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回结果
    return result


if __name__ == "__main__":
    print("=" * 70)
    print("逻辑学引擎测试套件")
    print("基于柯匹《逻辑学导论》")
    print("=" * 70)
    print()
    
    result = run_tests()
    
    print()
    print("=" * 70)
    print(f"测试完成: 运行 {result.testsRun} 个测试")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print("=" * 70)
    
    # 退出码
    sys.exit(0 if result.wasSuccessful() else 1)
