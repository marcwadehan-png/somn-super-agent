"""
谬误检测器 (Fallacy Detector)
谬误检测器

功能:
1. recognize形式谬误 (Formal Fallacies)
2. recognize非形式谬误 (Informal Fallacies)
3. 推理有效性检查
4. 证据链验证
5. 批判性思维辅助

版本: 1.0.0 -> 2.0.0 (模块化拆分)

作者: AI工程师
创建时间: 2026-03-31
更新时间: 2026-04-08
"""

__all__ = [
    'analyze_argument_quality',
    'detect_argument_fallacy',
    'detect_formal_fallacies',
    'detect_informal_fallacies',
    'detect_strategic_fallacies',
    'generate_fallacy_report',
    'suggest_improvements',
]

from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import re

# 子模块导入
from ._fd_types import FallacyCategory, FallacyDetection
from ._fd_formal import (
    init_formal_fallacies,
    detect_formal,
    check_affirming_consequent,
    check_denying_antecedent,
    has_undistributed_middle,
    extract_terms,
    check_syllogism_fallacies,
    check_propositional_fallacies,
)
from ._fd_informal import (
    init_informal_fallacies,
    init_detection_patterns,
    calculate_fallacy_confidence,
    detect_informal,
)
from ._fd_strategic import (
    init_strategic_fallacies,
    init_strategic_detection_patterns,
    calculate_strategic_confidence,
    detect_strategic,
)
from ._fd_core import (
    detect_argument_fallacy as _detect_argument_fallacy,
    analyze_argument_quality as _analyze_argument_quality,
    suggest_improvements as _suggest_improvements,
    calculate_quality_score,
    get_overall_assessment,
)

class FallacyDetector:
    """
    谬误检测器
    
    实现功能:
    1. 形式谬误检测 (三段论谬误,命题逻辑谬误)
    2. 非形式谬误检测 (歧义,相关性,预设,因果)
    3. 战略咨询谬误检测 (v5.1)
    4. 推理有效性分析
    5. 论证质量评估
    """
    
    def __init__(self):
        # 初始化谬误库
        self.formal_fallacies = init_formal_fallacies()
        self.informal_fallacies = init_informal_fallacies()
        self.strategic_fallacies = init_strategic_fallacies()
        
        # 初始化检测模式
        self.patterns = init_detection_patterns()
        self.strategic_patterns = init_strategic_detection_patterns()
    
    def detect_formal_fallacies(self,
                                premises: List[str],
                                conclusion: str) -> List[FallacyDetection]:
        """检测形式谬误"""
        return detect_formal(self.formal_fallacies, premises, conclusion)
    
    def detect_informal_fallacies(self,
                                 argument: str) -> List[FallacyDetection]:
        """检测非形式谬误(含战略咨询专用谬误)"""
        detections = detect_informal(
            self.informal_fallacies, self.patterns, argument
        )
        
        # v5.1: 同时检测战略咨询专用谬误
        strategic_detections = self.detect_strategic_fallacies(argument)
        detections.extend(strategic_detections)
        
        # 按置信度排序
        detections.sort(key=lambda x: x.confidence, reverse=True)
        return detections
    
    def detect_strategic_fallacies(self, argument: str) -> List[FallacyDetection]:
        """检测战略咨询专用谬误"""
        return detect_strategic(self.strategic_fallacies, argument)
    
    def detect_argument_fallacy(self, argument: Dict) -> List[Dict]:
        """unified的论证谬误检测接口"""
        return _detect_argument_fallacy(
            self.detect_informal_fallacies,
            self.detect_strategic_fallacies,
            argument
        )
    
    def analyze_argument_quality(self, argument: str) -> Dict:
        """分析论证质量"""
        return _analyze_argument_quality(
            self.detect_informal_fallacies, argument
        )
    
    def suggest_improvements(self, argument: str) -> List[str]:
        """建议论证改进"""
        return _suggest_improvements(
            self.detect_informal_fallacies, argument
        )
    
    def generate_fallacy_report(self,
                                detections: List[FallacyDetection],
                                argument: str = "") -> str:
        """生成谬误检测报告"""
        if not detections:
            return "✓ 未检测到明显的逻辑谬误"
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("逻辑谬误检测报告")
        report_lines.append("=" * 60)
        report_lines.append("")
        
        if argument:
            report_lines.append("原始论证:")
            report_lines.append(f"  {argument}")
            report_lines.append("")
        
        report_lines.append(f"检测到 {len(detections)} 个可能的谬误:")
        report_lines.append("")
        
        for i, detection in enumerate(detections, 1):
            report_lines.append(f"{i}. {detection.fallacy_name}")
            report_lines.append(f"   类别: {detection.category.value}")
            report_lines.append(f"   描述: {detection.description}")
            report_lines.append(f"   严重程度: {detection.severity}")
            report_lines.append(f"   置信度: {detection.confidence:.2%}")
            report_lines.append(f"   建议: {detection.suggestion}")
            report_lines.append("")
        
        return "\n".join(report_lines)

# 向后兼容的属性代理 (deprecated, 使用子模块方法)
class _FormalFallback:
    """形式谬误的向后兼容代理"""
    @staticmethod
    def _check_affirming_consequent(text):
        return check_affirming_consequent(text)
    
    @staticmethod
    def _check_denying_antecedent(text):
        return check_denying_antecedent(text)
    
    @staticmethod
    def _has_undistributed_middle(premises):
        return has_undistributed_middle(premises)
    
    @staticmethod
    def _extract_terms(statements):
        return extract_terms(statements)

# 使用示例
# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
