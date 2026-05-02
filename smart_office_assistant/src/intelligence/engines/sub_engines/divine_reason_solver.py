"""
DivineReason V4.0 快捷求解器
一键调用神之推理网络解决实际问题
"""
import sys
sys.path.insert(0, 'd:/AI/somn/smart_office_assistant/src')

from intelligence.engines.sub_engines import (
    get_divine_reason_engine,
    ReasoningRequest,
)


def solve(query: str, max_engines: int = 8) -> dict:
    """
    DivineReason 快捷求解函数
    
    Args:
        query: 问题描述
        max_engines: 最大使用引擎数
        
    Returns:
        dict: {
            'success': bool,
            'query': str,
            'engines_used': int,
            'confidence': float,
            'answer': str,
            'key_findings': List[str],
            'recommendations': List[str]
        }
    """
    engine = get_divine_reason_engine()
    
    request = ReasoningRequest(
        query=query,
        max_engines=max_engines
    )
    
    response = engine.reason(request)
    
    return {
        'success': True,
        'query': query,
        'engines_used': len(response.results),
        'confidence': response.confidence,
        'answer': response.fused_answer.get('text', ''),
        'key_findings': response.fused_answer.get('key_findings', [])[:5],
        'recommendations': response.fused_answer.get('recommendations', [])[:5],
        'engines': response.engines_used,
        'analysis': response.analysis,
    }


def solve_strategic(query: str) -> dict:
    """战略分析快捷求解"""
    engine = get_divine_reason_engine()
    request = ReasoningRequest(
        query=query,
        problem_type="STRATEGIC_ANALYSIS",
        max_engines=8
    )
    response = engine.reason(request)
    return {
        'query': query,
        'engines_used': len(response.results),
        'confidence': response.confidence,
        'answer': response.fused_answer.get('text', ''),
        'findings': response.fused_answer.get('key_findings', []),
        'recommendations': response.fused_answer.get('recommendations', []),
    }


def solve_causal(query: str) -> dict:
    """因果分析快捷求解"""
    engine = get_divine_reason_engine()
    request = ReasoningRequest(
        query=query,
        problem_type="CAUSAL_ANALYSIS",
        max_engines=8
    )
    response = engine.reason(request)
    return {
        'query': query,
        'engines_used': len(response.results),
        'confidence': response.confidence,
        'answer': response.fused_answer.get('text', ''),
        'findings': response.fused_answer.get('key_findings', []),
        'recommendations': response.fused_answer.get('recommendations', []),
    }


def solve_decision(query: str) -> dict:
    """决策分析快捷求解"""
    engine = get_divine_reason_engine()
    request = ReasoningRequest(
        query=query,
        problem_type="DECISION_MAKING",
        max_engines=8
    )
    response = engine.reason(request)
    return {
        'query': query,
        'engines_used': len(response.results),
        'confidence': response.confidence,
        'answer': response.fused_answer.get('text', ''),
        'findings': response.fused_answer.get('key_findings', []),
        'recommendations': response.fused_answer.get('recommendations', []),
    }


def solve_trend(query: str) -> dict:
    """趋势预测快捷求解"""
    engine = get_divine_reason_engine()
    request = ReasoningRequest(
        query=query,
        problem_type="PREDICTION",
        max_engines=8
    )
    response = engine.reason(request)
    return {
        'query': query,
        'engines_used': len(response.results),
        'confidence': response.confidence,
        'answer': response.fused_answer.get('text', ''),
        'findings': response.fused_answer.get('key_findings', []),
        'recommendations': response.fused_answer.get('recommendations', []),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 示例调用
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("DivineReason V4.0 快捷求解演示")
    print("=" * 70)
    
    # 示例1: 战略分析
    print("\n【示例1】战略分析: 公司市场份额下降20%")
    result1 = solve_strategic("公司市场份额下降20%，请分析原因并制定反击策略")
    print(f"置信度: {result1['confidence']:.1%}")
    print(f"洞察: {result1['findings'][:3]}")
    
    # 示例2: 因果分析
    print("\n【示例2】因果分析: 用户投诉增加")
    result2 = solve_causal("为什么这个月的用户投诉增加了30%？")
    print(f"置信度: {result2['confidence']:.1%}")
    print(f"洞察: {result2['findings'][:3]}")
    
    # 示例3: 决策分析
    print("\n【示例3】决策分析: 供应商选择")
    result3 = solve_decision("有三个供应商，价格/质量/交期分别是高/中/低、中/中/中、低/高/短，应该选择哪个？")
    print(f"置信度: {result3['confidence']:.1%}")
    print(f"建议: {result3['recommendations'][:3]}")
    
    # 示例4: 一键求解
    print("\n【示例4】一键求解: 通用问题")
    result4 = solve("如何提高团队的工作效率？")
    print(f"置信度: {result4['confidence']:.1%}")
    print(f"引擎数: {result4['engines_used']}")
    
    print("\n" + "=" * 70)
    print("DivineReason 快捷求解演示完成!")
    print("=" * 70)
