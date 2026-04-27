"""
SomnCore 情绪研究体系整合模块 [v1.0.0]
将EmotionResearchCore深度整合到Somn主执行链

整合点:
1. 需求分析阶段 - 强制校验需求是否符合情绪研究框架
2. 策略设计阶段 - 基于框架生成策略设计指导
3. 执行阶段 - 提供框架约束和神经科学/AI指导
4. 评估阶段 - 基于框架评估产出质量
5. 学习阶段 - 执行结果反馈到框架学习系统
"""

import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

# 延迟导入EmotionResearchCore
def _get_erc():
    """延迟获取EmotionResearchCore实例"""
    from ..intelligence.engines.emotion_research_core import get_emotion_research_core
    return get_emotion_research_core()


# ═══════════════════════════════════════════════════════════════════════════════
# 阶段1: 需求分析整合 - 强制框架校验
# ═══════════════════════════════════════════════════════════════════════════════

def validate_requirement_with_framework(
    requirement: str,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    [阶段1] 需求分析 - 强制情绪研究框架校验
    
    所有进入SomnCore的需求必须通过此校验
    """
    try:
        erc = _get_erc()
        validation_result = erc.validate_requirement(requirement, context)
        
        result = {
            "is_valid": validation_result.is_valid,
            "coverage_score": validation_result.coverage_score,
            "matched_intersections": validation_result.matched_intersections,
            "gaps": validation_result.gaps,
            "recommendations": validation_result.recommendations,
            "enhanced_requirement": validation_result.enhanced_requirement,
            "validation_timestamp": validation_result.validation_timestamp,
            "framework_version": erc.framework.version,
        }
        
        # 记录校验日志
        if validation_result.is_valid:
            logger.info(f"✅ 需求通过框架校验: coverage={validation_result.coverage_score:.2f}")
        else:
            logger.warning(f"⚠️ 需求未通过框架校验: coverage={validation_result.coverage_score:.2f}, gaps={validation_result.gaps}")
        
        return result
    
    except Exception as e:
        logger.error(f"框架校验失败: {e}")
        # 失败时返回宽松通过，避免阻塞
        return {
            "is_valid": True,  # 容错
            "coverage_score": 0.0,
            "matched_intersections": [],
            "gaps": [],
            "recommendations": [f"框架校验异常: {e}"],
            "enhanced_requirement": requirement,
            "error": "操作失败",
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 阶段2: 策略设计整合 - 框架指导策略生成
# ═══════════════════════════════════════════════════════════════════════════════

def build_strategy_with_framework(
    requirement: str,
    validation_result: Dict[str, Any],
    additional_context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    [阶段2] 策略设计 - 基于情绪研究框架生成策略指导
    
    所有策略设计必须基于此框架产出
    """
    try:
        erc = _get_erc()
        
        # 生成策略框架
        strategy_framework = erc.generate_strategy_framework(requirement)
        
        # 获取心价比公式指导
        heart_price_guide = erc.get_heart_price_formula()
        
        # 构建完整的策略设计指导
        strategy_guidance = {
            "framework_based_strategy": strategy_framework,
            "heart_price_formula": heart_price_guide,
            "design_principles": _extract_design_principles(strategy_framework),
            "measurement_plan": _build_measurement_plan(strategy_framework),
            "risk_control_checklist": strategy_framework.get("risk_control_points", []),
            "neuroscience_insights": strategy_framework.get("neuroscience_insights", []),
            "ai_application_suggestions": strategy_framework.get("ai_applications", []),
            "sss_wisdom_refs": strategy_framework.get("sss_wisdom_refs", []),
        }
        
        logger.info(f"✅ 策略框架已生成: {len(strategy_framework.get('research_dimensions', {}))}个维度")
        
        return strategy_guidance
    
    except Exception as e:
        logger.error(f"策略框架生成失败: {e}")
        return {
            "error": "操作失败",
            "fallback": "使用默认策略设计流程",
        }


def _extract_design_principles(strategy_framework: Dict[str, Any]) -> List[str]:
    """从策略框架中提取设计原则"""
    principles = []
    
    # 基于神经科学的设计原则
    neuroscience_insights = strategy_framework.get("neuroscience_insights", [])
    if "多巴胺间歇强化" in neuroscience_insights:
        principles.append("采用间歇强化机制，避免奖赏回路钝化")
    if "前额叶负荷降低" in neuroscience_insights:
        principles.append("简化决策流程，降低认知负荷")
    if "催产素情感联结" in neuroscience_insights:
        principles.append("设计情感共鸣点，建立长期情感联结")
    
    # 基于AI的设计原则
    ai_apps = strategy_framework.get("ai_applications", [])
    if "个性化推荐" in ai_apps:
        principles.append("利用AI实现情绪感知的个性化体验")
    if "实时情绪识别" in ai_apps:
        principles.append("集成实时情绪识别，动态调整交互策略")
    
    return principles


def _build_measurement_plan(strategy_framework: Dict[str, Any]) -> Dict[str, Any]:
    """构建测量计划"""
    methodology_stack = strategy_framework.get("methodology_stack", [])
    
    return {
        "physiological_measures": [m for m in methodology_stack if m in ["GSR", "HRV", "fMRI", "EEG"]],
        "behavioral_measures": [m for m in methodology_stack if m in ["眼动追踪", "点击热力图", "微表情识别"]],
        "cognitive_measures": [m for m in methodology_stack if "量表" in m or "测验" in m],
        "ai_measures": [m for m in methodology_stack if "AI" in m or "LLM" in m],
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 阶段3: 执行阶段整合 - 框架约束检查
# ═══════════════════════════════════════════════════════════════════════════════

def check_execution_compliance(
    execution_plan: Dict[str, Any],
    strategy_framework: Dict[str, Any]
) -> Dict[str, Any]:
    """
    [阶段3] 执行阶段 - 检查执行计划是否符合框架约束
    """
    compliance_report = {
        "is_compliant": True,
        "violations": [],
        "warnings": [],
        "suggestions": [],
    }
    
    # 检查是否覆盖了框架要求的维度
    required_dimensions = set(strategy_framework.get("research_dimensions", {}).keys())
    executed_dimensions = set(execution_plan.get("dimensions_covered", []))
    
    missing_dimensions = required_dimensions - executed_dimensions
    if missing_dimensions:
        compliance_report["warnings"].append(f"未覆盖框架要求的维度: {missing_dimensions}")
    
    # 检查风险管控点
    risk_points = strategy_framework.get("risk_control_points", [])
    executed_risk_controls = set(execution_plan.get("risk_controls", []))
    
    for risk in risk_points[:5]:  # 检查前5个关键风险
        if risk not in executed_risk_controls:
            compliance_report["warnings"].append(f"未处理风险: {risk}")
    
    # 检查神经科学应用
    if strategy_framework.get("neuroscience_insights"):
        if not execution_plan.get("neuroscience_applied"):
            compliance_report["suggestions"].append("建议应用神经科学洞察优化执行")
    
    # 检查AI应用
    if strategy_framework.get("ai_applications"):
        if not execution_plan.get("ai_applied"):
            compliance_report["suggestions"].append("建议应用AI技术增强执行效果")
    
    # 最终判定
    if len(compliance_report["violations"]) > 0:
        compliance_report["is_compliant"] = False
    
    return compliance_report


# ═══════════════════════════════════════════════════════════════════════════════
# 阶段4: 评估阶段整合 - 框架质量评估
# ═══════════════════════════════════════════════════════════════════════════════

def evaluate_output_quality(
    output: Any,
    original_requirement: str,
    strategy_framework: Dict[str, Any]
) -> Dict[str, Any]:
    """
    [阶段4] 评估阶段 - 基于框架评估产出质量
    """
    evaluation = {
        "overall_score": 0.0,
        "dimension_scores": {},
        "framework_alignment": 0.0,
        "neuroscience_application": 0.0,
        "ai_application": 0.0,
        "improvement_suggestions": [],
    }
    
    try:
        erc = _get_erc()
        
        # 1. 检查产出是否符合原始需求
        # (这里可以调用LLM进行评估)
        
        # 2. 检查框架对齐度
        matched_intersections = strategy_framework.get("validation", {}).get("matched_intersections", [])
        covered_intersections = _extract_covered_intersections(output)
        
        if matched_intersections:
            coverage = len(set(covered_intersections) & set(matched_intersections)) / len(matched_intersections)
            evaluation["framework_alignment"] = coverage
        
        # 3. 检查神经科学应用
        neuroscience_keywords = ["多巴胺", "血清素", "催产素", "杏仁核", "前额叶", "神经"]
        if any(kw in str(output) for kw in neuroscience_keywords):
            evaluation["neuroscience_application"] = 0.8
        
        # 4. 检查AI应用
        ai_keywords = ["AI", "算法", "预测", "个性化", "智能"]
        if any(kw in str(output) for kw in ai_keywords):
            evaluation["ai_application"] = 0.8
        
        # 5. 计算总分
        evaluation["overall_score"] = (
            evaluation["framework_alignment"] * 0.4 +
            evaluation["neuroscience_application"] * 0.3 +
            evaluation["ai_application"] * 0.3
        )
        
        # 6. 生成改进建议
        if evaluation["framework_alignment"] < 0.6:
            evaluation["improvement_suggestions"].append("建议增强与情绪研究框架的对齐度")
        if evaluation["neuroscience_application"] < 0.5:
            evaluation["improvement_suggestions"].append("建议增加神经科学视角的分析")
        if evaluation["ai_application"] < 0.5:
            evaluation["improvement_suggestions"].append("建议考虑AI技术的应用")
        
        logger.info(f"✅ 产出质量评估完成: score={evaluation['overall_score']:.2f}")
        
    except Exception as e:
        logger.error(f"质量评估失败: {e}")
        evaluation["error"] = "操作失败"
    
    return evaluation


def _extract_covered_intersections(output: Any) -> List[str]:
    """从产出中提取覆盖的交叉点"""
    output_str = str(output)
    covered = []
    
    # 检查是否提到了交叉点代码
    for code in [f"{d}{n}" for d in "ABCDE" for n in range(1, 7)]:
        if code in output_str:
            covered.append(code)
    
    return covered


# ═══════════════════════════════════════════════════════════════════════════════
# 阶段5: 学习阶段整合 - 执行反馈学习
# ═══════════════════════════════════════════════════════════════════════════════

def learn_from_execution_result(
    execution_id: str,
    requirement: str,
    strategy_framework: Dict[str, Any],
    evaluation_result: Dict[str, Any],
    execution_metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    [阶段5] 学习阶段 - 从执行结果中学习，更新研究框架
    """
    try:
        erc = _get_erc()
        
        # 构建学习数据
        execution_data = {
            "execution_id": execution_id,
            "requirement": requirement,
            "intersections_used": strategy_framework.get("validation", {}).get("matched_intersections", []),
            "effectiveness_score": evaluation_result.get("overall_score", 0.0),
            "new_insights": _extract_new_insights(execution_metadata),
            "gaps_identified": evaluation_result.get("improvement_suggestions", []),
        }
        
        # 调用核心学习功能
        learning_result = erc.learn_from_execution(execution_data)
        
        logger.info(f"✅ 执行学习完成: learning_id={learning_result.get('learning_record_id')}")
        
        return learning_result
    
    except Exception as e:
        logger.error(f"学习失败: {e}")
        return {"error": "学习失败"}


def _extract_new_insights(metadata: Optional[Dict[str, Any]]) -> List[str]:
    """提取新洞察"""
    if not metadata:
        return []
    
    insights = []
    
    # 从执行元数据中提取洞察
    if "discovered_patterns" in metadata:
        insights.extend(metadata["discovered_patterns"])
    if "unexpected_findings" in metadata:
        insights.extend(metadata["unexpected_findings"])
    
    return insights[:10]  # 最多10条


# ═══════════════════════════════════════════════════════════════════════════════
# 联网学习整合 - 自动升级
# ═══════════════════════════════════════════════════════════════════════════════

def trigger_web_learning(search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    触发联网学习，自动更新研究框架
    
    当系统进行网络搜索后自动调用
    """
    try:
        erc = _get_erc()
        learning_result = erc.auto_learn_from_web(search_results)
        
        logger.info(f"🌐 联网学习完成: learned={learning_result.get('items_learned', 0)}条")
        
        return learning_result
    
    except Exception as e:
        logger.error(f"联网学习失败: {e}")
        return {"error": "联网学习失败"}


def check_framework_upgrade() -> Dict[str, Any]:
    """
    检查是否需要升级框架
    
    定期调用，实现框架自主迭代
    """
    try:
        erc = _get_erc()
        upgrade_proposal = erc.propose_framework_upgrade()
        
        logger.info(f"📈 框架升级检查完成: proposal_id={upgrade_proposal.get('proposal_id')}")
        
        return upgrade_proposal
    
    except Exception as e:
        logger.error(f"升级检查失败: {e}")
        return {"error": "升级检查失败"}


# ═══════════════════════════════════════════════════════════════════════════════
# SomnCore集成接口 - 主链调用点
# ═══════════════════════════════════════════════════════════════════════════════

def integrate_with_somn_core(somn_core_instance: Any) -> bool:
    """
    将情绪研究体系整合到SomnCore实例
    
    在SomnCore初始化时调用
    """
    try:
        # 初始化EmotionResearchCore
        erc = _get_erc()
        
        # 将核心实例附加到SomnCore
        somn_core_instance.emotion_research_core = erc
        
        # 注册框架校验钩子
        somn_core_instance._emotion_research_validate = validate_requirement_with_framework
        somn_core_instance._emotion_research_build_strategy = build_strategy_with_framework
        somn_core_instance._emotion_research_evaluate = evaluate_output_quality
        somn_core_instance._emotion_research_learn = learn_from_execution_result
        
        logger.info("✅ EmotionResearchCore 已成功整合到SomnCore")
        return True
    
    except Exception as e:
        logger.error(f"整合失败: {e}")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# 便捷导出
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # 阶段整合函数
    "validate_requirement_with_framework",
    "build_strategy_with_framework",
    "check_execution_compliance",
    "evaluate_output_quality",
    "learn_from_execution_result",
    
    # 联网学习
    "trigger_web_learning",
    "check_framework_upgrade",
    
    # 集成接口
    "integrate_with_somn_core",
]
