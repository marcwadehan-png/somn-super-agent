"""
__all__ = [
    'analyze_argument_quality',
    'calculate_quality_score',
    'detect_argument_fallacy',
    'get_overall_assessment',
    'suggest_improvements',
]

核心检测与质量评估
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)
from ._fd_types import FallacyDetection
from datetime import datetime

def detect_argument_fallacy(
    informal_detect_fn,
    strategic_detect_fn,
    argument: Dict
) -> List[Dict]:
    """
    unified的论证谬误检测接口
    
    Args:
        informal_detect_fn: 非形式谬误检测函数
        strategic_detect_fn: 战略谬误检测函数
        argument: 论证字典,包含type, premises, conclusion等字段
        
    Returns:
        检测到的谬误列表(字典格式)
    """
    detections = []
    
    arg_type = argument.get('type', 'general')
    
    # 构建完整论证文本
    if arg_type == 'deduction':
        premises = argument.get('premises', [])
        conclusion = argument.get('conclusion', '')
        full_text = ' '.join(premises) + ' ' + conclusion
    elif arg_type == 'induction':
        observations = argument.get('observations', [])
        conclusion = argument.get('conclusion', '')
        full_text = ' '.join(observations) + ' ' + conclusion
    else:
        full_text = str(argument)
    
    # 检测非形式谬误
    try:
        informal_detections = informal_detect_fn(full_text)
        for detection in informal_detections:
            detections.append({
                'name': detection.fallacy_name,
                'category': detection.category.value,
                'description': detection.description,
                'severity': detection.severity,
                'confidence': detection.confidence,
                'suggestion': detection.suggestion
            })
    except Exception as e:
        logger.debug(f"通用谬误检测跳过: {e}")
    
    # 检测战略咨询专用谬误
    try:
        strategic_detections = strategic_detect_fn(full_text)
        for detection in strategic_detections:
            detections.append({
                'name': detection.fallacy_name,
                'category': detection.category.value,
                'description': detection.description,
                'severity': detection.severity,
                'confidence': detection.confidence,
                'suggestion': detection.suggestion
            })
    except Exception as e:
        logger.debug(f"谬误检测失败: {e}")
    
    # 按置信度排序
    detections.sort(key=lambda x: x.get('confidence', 0), reverse=True)
    return detections

def calculate_quality_score(fallacies: List[FallacyDetection]) -> float:
    """计算论证质量得分"""
    score = 1.0
    
    for fallacy in fallacies:
        if fallacy.severity == 'critical':
            score -= 0.3 * fallacy.confidence
        elif fallacy.severity == 'major':
            score -= 0.2 * fallacy.confidence
        else:
            score -= 0.1 * fallacy.confidence
    
    return max(0.0, min(1.0, score))

def get_overall_assessment(score: float) -> str:
    """获取整体评估"""
    if score >= 0.9:
        return "优秀 - 论证逻辑严密,几乎没有谬误"
    elif score >= 0.7:
        return "良好 - 论证基本合理,存在少量可改进之处"
    elif score >= 0.5:
        return "中等 - 论证存在明显问题,需要进一步完善"
    elif score >= 0.3:
        return "较差 - 论证有较多逻辑谬误,可信度较低"
    else:
        return "很差 - 论证存在严重逻辑问题,不可信"

def analyze_argument_quality(
    informal_detect_fn,
    argument: str
) -> Dict:
    """
    分析论证质量
    """
    # 检测非形式谬误
    informal_fallacies = informal_detect_fn(argument)
    
    # 计算质量得分
    quality_score = calculate_quality_score(informal_fallacies)
    
    # 生成评估报告
    report = {
        'quality_score': quality_score,
        'fallacy_count': len(informal_fallacies),
        'critical_fallacies': [f for f in informal_fallacies if f.severity == 'critical'],
        'major_fallacies': [f for f in informal_fallacies if f.severity == 'major'],
        'minor_fallacies': [f for f in informal_fallacies if f.severity == 'minor'],
        'overall_assessment': get_overall_assessment(quality_score),
        'improvement_suggestions': [f.suggestion for f in informal_fallacies]
    }
    
    return report

def suggest_improvements(
    informal_detect_fn,
    argument: str
) -> List[str]:
    """
    建议论证改进
    """
    detections = informal_detect_fn(argument)
    suggestions = []
    
    if not detections:
        suggestions.append("论证逻辑清晰,可以考虑:")
        suggestions.append("  - 增加更多具体证据")
        suggestions.append("  - 引用权威来源")
        suggestions.append("  - 预判并回应可能的反驳")
    else:
        suggestions.append("发现以下改进方向:")
        
        # 按类别分组
        by_category = {}
        for detection in detections:
            category = detection.category.value
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(detection)
        
        for category, fallacies in by_category.items():
            suggestions.append(f"\n{category}:")
            for fallacy in fallacies:
                suggestions.append(f"  - {fallacy.suggestion}")
    
    return suggestions
