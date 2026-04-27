"""便捷接口模块"""

from typing import Dict, Any

from ._st_enums import SolutionType
from ._st_library import SolutionTemplateLibraryV2
from ._st_calculator import DynamicOutcomeCalculator

# 全局模板库实例
__all__ = [
    'quick_calculate',
]

solution_library_v2 = SolutionTemplateLibraryV2()
outcome_calculator = DynamicOutcomeCalculator(solution_library_v2)

def quick_calculate(solution_type: str, client_params: Dict) -> Dict:
    """
    快速计算预期效果
    
    示例:
        result = quick_calculate("private_domain", {
            "industry": "美妆",
            "avg_order_value": 350,
            "execution_capability": 6.0,
            "pain_points": ["获客成本高", "用户留存低"]
        })
    """
    try:
        solution_enum = SolutionType(solution_type)
    except ValueError:
        return {"error": f"未知的解决方案类型: {solution_type}"}
    
    return outcome_calculator.calculate_outcomes(solution_enum, client_params)
