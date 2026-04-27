"""
ROI计算模块单元测试
覆盖 _roi_calculation.py 中的核心计算逻辑，包括v1.0 bug修复验证。

运行: pytest tests/neural_memory/test_roi_calculation.py -v
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


class MockROICore:
    """Mock ROICore for isolated unit testing."""
    def __init__(self):
        self.params = {
            "quality_weight": 0.3,
            "time_weight": 0.3,
            "task_weight": 0.2,
            "satisfaction_weight": 0.2,
        }


# Import after mock setup
from src.neural_memory._roi_calculation import (
    calculate_efficiency_impl,
    calculate_roi_impl,
)


class TestCalculateROIImpl:
    """calculate_roiImpl 测试"""

    def test_basic_roi(self):
        core = MockROICore()
        roi = calculate_roi_impl(core, output_value=100.0, input_cost=50.0)
        assert isinstance(roi, float)
        assert roi >= 0


class TestCalculateEfficiencyImpl:
    """calculate_efficiencyImpl — 验证v1.0 bug修复"""

    def test_perfect_score(self):
        """完美输入应接近1.0"""
        core = MockROICore()
        score = calculate_efficiency_impl(core, quality=1.0, time_saved=100, actual_minutes=10, adopted=True)
        assert score >= 0.9, f"Perfect input too low: {score}"

    def test_zero_quality(self):
        """质量为0时应显著降低分数"""
        core = MockROICore()
        score = calculate_efficiency_impl(core, quality=0.0, time_saved=100, actual_minutes=10, adopted=True)
        assert score < 0.7, f"Zero quality too high: {score}"

    def test_no_time_saved(self):
        """无时间节省时应低于有时间节省的情况"""
        core = MockROICore()
        score_low = calculate_efficiency_impl(core, quality=1.0, time_saved=0, actual_minutes=10, adopted=True)
        score_high = calculate_efficiency_impl(core, quality=1.0, time_saved=100, actual_minutes=10, adopted=True)
        assert score_high >= score_low

    def test_not_adopted_penalty(self):
        """未被采纳应比已采纳得分低"""
        core = MockROICore()
        score_adopted = calculate_efficiency_impl(core, quality=1.0, time_saved=50, actual_minutes=10, adopted=True)
        score_not = calculate_efficiency_impl(core, quality=1.0, time_saved=50, actual_minutes=10, adopted=False)
        assert score_adopted > score_not

    def test_time_weight_applied_once_v22_fix(self):
        """[v1.0 fix验证] time_weight不应被双重应用
        
        原bug: time_part定义时乘weight，求和时又乘一次 → 实际0.09而非0.3
        """
        core = MockROICore()
        # time_ratio = 1.0 (time_saved == actual_minutes)
        score = calculate_efficiency_impl(core, quality=0.5, time_saved=10, actual_minutes=10, adopted=False)
        
        # 修复后期望: Q*0.3 + min(1,1)*0.3 + 0 + 0.2*0.5 = 0.15+0.3+0+0.1 = 0.55
        # max_score = 1.0 → normalized ≈ 0.55
        assert 0.50 <= score <= 0.60, \
            f"time weight may be double-applied: {score}"

    def test_satisfaction_not_constant_v22_fix(self):
        """[v1.0 fix验证] satisfaction不再固定0.2常量
        
        新代码: satisfaction_part = 0.2 * quality（与质量挂钩）
        """
        core = MockROICore()
        score_good = calculate_efficiency_impl(core, quality=1.0, time_saved=0, actual_minutes=10, adopted=False)
        score_bad = calculate_efficiency_impl(core, quality=0.0, time_saved=0, actual_minutes=10, adopted=False)
        assert score_good != score_bad, "satisfaction appears constant"

    def test_normalized_range_01(self):
        """结果必须归一化到[0, 1]区间"""
        core = MockROICore()
        for q in [0.0, 0.5, 1.0]:
            for ts in [0, 50, 200]:
                for am in [1, 10, 100]:
                    for adopted in [True, False]:
                        score = calculate_efficiency_impl(core, q, ts, am, adopted)
                        assert 0.0 <= score <= 1.0, \
                            f"Out of range: q={q}, ts={ts}, am={am}, adopted={adopted} -> {score}"

    def test_zero_actual_minutes_no_crash(self):
        """actual_minutes=0不应崩溃（除零保护）"""
        core = MockROICore()
        score = calculate_efficiency_impl(core, quality=1.0, time_saved=10, actual_minutes=0, adopted=True)
        assert isinstance(score, float)

    def test_extreme_values_clamp(self):
        """极端输入值不应导致异常"""
        core = MockROICore()
        # 极大时间节省
        s1 = calculate_efficiency_impl(core, quality=0.8, time_saved=999999, actual_minutes=1, adopted=True)
        assert 0 <= s1 <= 1.0
        # 质量超范围
        s2 = calculate_efficiency_impl(core, quality=5.0, time_saved=0, actual_minutes=100, adopted=False)
        assert 0 <= s2 <= 1.0
