"""
__all__ = [
    'assess',
    'assess_solution',
    'compare',
    'compare_solutions',
    'get_benchmark_stats',
    'get_solution_list',
    'learn_from_case',
    'list_solutions',
]

增长解决方案引擎 V2 - unified入口

核心特性:
1. 动态效果评估 - 基于客户实际情况计算预期效果
2. 深度需求分析 - 拆解痛点,客单,历史经营
3. 行业基准数据 - 细分行业的合理效果区间
4. 执行能力校准 - 专业团队最多达到理想状态的70%
5. 评估准确性验证 - 80%-120%阈值检测
6. 持续学习优化 - 从服务商案例中提取行业基准

使用示例:
    from src.growth_engine import SolutionEngineV2
    
    engine = SolutionEngineV2()
    
    # 评估解决方案
    result = engine.assess_solution(
        solution_type="private_domain",
        client_info={
            "industry": "美妆",
            "avg_order_value": 350,
            "execution_capability": 6.0,
            "pain_points": ["获客成本高", "用户留存低"]
        }
    )
"""

from typing import Dict, List, Any, Optional
import logging
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)

# 导入模板模块（V2已合并到 solution_templates/ 子包）
from .solution_templates import (
    SolutionType,
    SolutionCategory,
    SolutionTemplateV2,
    SolutionTemplateLibraryV2,
    DynamicOutcomeCalculator,
    AssessmentParameter,
    DynamicMetric,
    quick_calculate
)

from .solution_assessment_framework import (
    SolutionAssessmentEngine,
    ClientContext,
    AssessmentResult,
    DynamicOutcomeRange,
    IndustryBenchmarkDB,
    assess_solution_for_client,
    quick_assessment
)

from .solution_learning import (
    BenchmarkLearningEngine,
    BenchmarkDataPoint,
    IndustryBenchmarkUpdate,
    LearningSourceType,
    integrate_with_template_library
)

@dataclass
class AssessmentReport:
    """评估报告"""
    # 基础信息
    solution_type: str
    solution_name: str
    client_industry: str
    
    # 需求分析
    client_context: Dict
    primary_pain_points: List[str]
    
    # 定制化目标
    customized_goals: List[Dict]
    
    # 预期效果(动态计算)
    expected_outcomes: List[Dict]
    
    # 关键metrics
    key_metrics: List[Dict]
    
    # 执行建议
    implementation_suggestions: List[str]
    
    # 风险评估
    risk_factors: List[str]
    success_probability: float
    
    # 评估质量
    assessment_quality: Dict
    validation_result: Dict
    
    # 建议的替代方案
    alternative_solutions: List[Dict] = field(default_factory=list)
    
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())

class SolutionEngineV2:
    """
    解决方案引擎 V2 - unified入口
    
    整合所有V2功能,提供一站式解决方案评估服务
    """
    
    def __init__(self):
        # init各组件
        self.template_library = SolutionTemplateLibraryV2()
        self.assessment_engine = SolutionAssessmentEngine()
        self.outcome_calculator = DynamicOutcomeCalculator(self.template_library)
        self.learning_engine = BenchmarkLearningEngine()
        
        # 集成学习引擎与模板库
        integrate_with_template_library(self.template_library)
    
    def assess_solution(self, 
                       solution_type: str,
                       client_info: Dict[str, Any]) -> AssessmentReport:
        """
        评估解决方案
        
        Args:
            solution_type: 解决方案类型 (如: private_domain, membership, douyin)
            client_info: 客户信息
                - industry: 行业
                - avg_order_value: 客单价
                - execution_capability: 执行能力评分(1-10)
                - pain_points: 痛点列表
                - ...其他参数
                
        Returns:
            评估报告
        """
        # 1. 验证解决方案类型
        try:
            solution_enum = SolutionType(solution_type)
        except ValueError:
            return self._create_error_report(f"未知的解决方案类型: {solution_type}")
        
        template = self.template_library.get_template(solution_enum)
        if not template:
            return self._create_error_report(f"解决方案模板不存在: {solution_type}")
        
        # 2. 深度需求分析
        client_context = self.assessment_engine.analyze_client_needs(client_info)
        
        # 3. 计算动态预期效果
        outcome_result = self.outcome_calculator.calculate_outcomes(
            solution_enum, client_info
        )
        
        # 4. generate定制化目标
        adjustment_factors = self.assessment_engine.calculate_adjustment_factors(
            client_context, solution_type
        )
        customized_goals = self.assessment_engine._generate_customized_goals(
            solution_type, client_context, adjustment_factors
        )
        
        # 5. 构建评估报告
        report = AssessmentReport(
            solution_type=solution_type,
            solution_name=template.name,
            client_industry=client_info.get("industry", "未知"),
            client_context=self._context_to_dict(client_context),
            primary_pain_points=[p.value for p in client_context.primary_pain_points],
            customized_goals=customized_goals,
            expected_outcomes=outcome_result.get("outcomes", []),
            key_metrics=self._extract_key_metrics(outcome_result),
            implementation_suggestions=self._generate_implementation_suggestions(
                template, client_context
            ),
            risk_factors=self._assess_risks(client_context, outcome_result),
            success_probability=self._calculate_success_probability(
                client_context, adjustment_factors
            ),
            assessment_quality={
                "completeness": self._assess_completeness(client_info, template),
                "confidence": self._calculate_overall_confidence(outcome_result),
            },
            validation_result=outcome_result.get("validation", {})
        )
        
        # 6. 推荐替代方案
        report.alternative_solutions = self._recommend_alternatives(
            solution_type, client_info
        )
        
        return report
    
    def compare_solutions(self,
                         solution_types: List[str],
                         client_info: Dict) -> Dict:
        """
        对比多个解决方案
        
        Args:
            solution_types: 解决方案类型列表
            client_info: 客户信息
            
        Returns:
            对比结果
        """
        comparisons = []
        
        for solution_type in solution_types:
            report = self.assess_solution(solution_type, client_info)
            comparisons.append({
                "solution_type": solution_type,
                "solution_name": report.solution_name,
                "success_probability": report.success_probability,
                "expected_outcomes": report.expected_outcomes,
                "risk_factors": report.risk_factors,
                "assessment_quality": report.assessment_quality
            })
        
        # 排序:按成功概率
        comparisons.sort(key=lambda x: x["success_probability"], reverse=True)
        
        return {
            "client_industry": client_info.get("industry"),
            "comparisons": comparisons,
            "recommendation": self._generate_comparison_recommendation(comparisons)
        }
    
    def get_solution_list(self, 
                         industry: Optional[str] = None,
                         category: Optional[str] = None) -> List[Dict]:
        """
        get解决方案列表
        
        Args:
            industry: 行业筛选
            category: 分类筛选
            
        Returns:
            解决方案列表
        """
        category_enum = None
        if category:
            try:
                category_enum = SolutionCategory(category)
            except ValueError:
                logger.warning(f"[GrowthEngine] 未知的解决方案类别: {category}，使用全类别搜索")
        
        templates = self.template_library.list_templates(category_enum, industry)
        
        return [
            {
                "solution_type": t.solution_type.value,
                "name": t.name,
                "category": t.category.value,
                "description": t.description,
                "applicable_industries": t.applicable_industries,
                "required_parameters": [
                    {"name": p.param_name, "description": p.description, "required": p.required}
                    for p in t.required_parameters
                ]
            }
            for t in templates
        ]
    
    def learn_from_case(self,
                       provider_name: str,
                       case_data: Dict) -> Dict:
        """
        从案例学习 [修复：添加重复检测机制]
        
        Args:
            provider_name: 服务商名称
            case_data: 案例数据
                - content: 案例内容
                - industry: 行业
                - solution_type: 解决方案类型
                - case_id: 案例唯一标识 (可选，用于重复检测)
                
        Returns:
            学习结果
        """
        # [修复] 重复检测：检查是否已学习过相同案例
        solution_type = case_data.get("solution_type", "unknown")
        industry = case_data.get("industry", "未知")
        case_id = case_data.get("case_id", "")
        
        # 如果没有提供case_id，基于内容生成哈希
        if not case_id:
            import hashlib
            content = case_data.get("content", "")
            provider = provider_name
            # 基于内容+服务商+行业生成唯一标识
            case_hash = hashlib.md5(f"{content}{provider}{industry}".encode()).hexdigest()[:16]
            case_id = f"{solution_type}_{industry}_{case_hash}"
        
        # 检查是否已学习过
        try:
            existing_learned = self._get_learned_case_ids()
            if case_id in existing_learned:
                return {
                    "status": "duplicate",
                    "case_id": case_id,
                    "data_points_extracted": 0,
                    "message": f"案例 {case_id} 已学习过，跳过重复学习"
                }
        except Exception as e:
            logger.warning(f"[GrowthEngine] 检查重复案例失败: {e}，继续学习")
        
        data_points = self.learning_engine.extract_outcomes_from_case(
            case_content=case_data.get("content", ""),
            provider_name=provider_name,
            industry=industry,
            solution_type=solution_type
        )
        
        if data_points:
            update = self.learning_engine.propose_benchmark_update(
                solution_type=solution_type,
                industry=industry,
                new_data_points=data_points
            )
            
            # [修复] 记录已学习的案例ID
            try:
                self._record_learned_case(case_id)
            except Exception as e:
                logger.warning(f"[GrowthEngine] 记录案例ID失败(不影响结果): {e}")
            
            return {
                "status": "success",
                "case_id": case_id,
                "data_points_extracted": len(data_points),
                "benchmark_update_proposed": update is not None,
                "update_id": update.update_id if update else None
            }
        
        return {
            "status": "no_data",
            "case_id": case_id,
            "data_points_extracted": 0
        }
    
    def _get_learned_case_ids(self) -> set:
        """[新增] 获取已学习案例ID集合"""
        import json
        learned_file = self.data_path / "learned_cases.json" if hasattr(self, 'data_path') else None
        if learned_file and learned_file.exists():
            try:
                with open(learned_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return set(data.get("learned_ids", []))
            except Exception as e:
                logger.warning(f"[GrowthEngine] 读取已学习案例失败: {e}")
        return set()
    
    def _record_learned_case(self, case_id: str):
        """[新增] 记录已学习的案例"""
        import json
        learned_file = self.data_path / "learned_cases.json" if hasattr(self, 'data_path') else None
        if learned_file:
            learned_file.parent.mkdir(parents=True, exist_ok=True)
            try:
                if learned_file.exists():
                    with open(learned_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                else:
                    data = {"learned_ids": []}
                
                if case_id not in data.get("learned_ids", []):
                    data["learned_ids"].append(case_id)
                
                with open(learned_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            except Exception as e:
                logger.warning(f"[GrowthEngine] 记录案例ID失败: {e}")
    
    def get_benchmark_stats(self) -> Dict:
        """get基准数据统计"""
        return self.learning_engine.get_benchmark_statistics()
    
    # ==================== 内部方法 ====================
    
    def _create_error_report(self, error_message: str) -> AssessmentReport:
        """创建错误报告"""
        return AssessmentReport(
            solution_type="error",
            solution_name="评估失败",
            client_industry="未知",
            client_context={},
            primary_pain_points=[],
            customized_goals=[],
            expected_outcomes=[],
            key_metrics=[],
            implementation_suggestions=[],
            risk_factors=[error_message],
            success_probability=0.0,
            assessment_quality={"error": error_message},
            validation_result={"status": "error"}
        )
    
    def _context_to_dict(self, context: ClientContext) -> Dict:
        """转换上下文为字典"""
        return {
            "industry": context.industry,
            "scale": context.company_scale,
            "stage": context.development_stage,
            "avg_order_value": context.avg_order_value,
            "execution_capability": context.execution_capability_score,
            "primary_pain_points": [p.value for p in context.primary_pain_points]
        }
    
    def _extract_key_metrics(self, outcome_result: Dict) -> List[Dict]:
        """提取关键metrics"""
        metrics = []
        for outcome in outcome_result.get("outcomes", []):
            metrics.append({
                "name": outcome.get("metric_name"),
                "unit": outcome.get("unit"),
                "expected_range": outcome.get("calculated_range"),
                "industry_baseline": outcome.get("industry_baseline")
            })
        return metrics
    
    def _generate_implementation_suggestions(self,
                                            template: SolutionTemplateV2,
                                            context: ClientContext) -> List[str]:
        """generate实施建议"""
        suggestions = []
        
        # 基于痛点匹配strategy
        for strategy in template.core_strategies:
            applicable_pains = strategy.get("applicable_pains", [])
            matched = any(
                p.value in [f"{ap}_low" for ap in applicable_pains] or
                any(ap in p.value for ap in applicable_pains)
                for p in context.primary_pain_points
            )
            if matched:
                suggestions.append(f"优先实施'{strategy['name']}'strategy:{strategy['description']}")
        
        # 基于执行能力的建议
        if context.execution_capability_score < 5:
            suggestions.append("执行能力较弱,建议先从简单的自动化工具入手,逐步建立运营能力")
        elif context.execution_capability_score > 7:
            suggestions.append("执行能力较强,可以考虑更复杂的strategy和更高的目标")
        
        # 基于团队规模的建议
        if context.team_size and context.team_size < 5:
            suggestions.append("团队规模较小,建议借助外部服务商或自动化工具弥补人力不足")
        
        return suggestions
    
    def _assess_risks(self, context: ClientContext, outcome_result: Dict) -> List[str]:
        """评估风险因素"""
        risks = []
        
        if context.execution_capability_score < 4:
            risks.append("执行能力不足,可能导致预期效果难以达成")
        
        if not context.primary_pain_points:
            risks.append("痛点不明确,解决方案可能无法精准匹配需求")
        
        validation = outcome_result.get("validation", {})
        if validation.get("status") == "over_estimated":
            risks.append("评估结果可能过于乐观,建议降低预期或增加资源投入")
        
        return risks
    
    def _calculate_success_probability(self,
                                      context: ClientContext,
                                      factors: Dict) -> float:
        """计算成功概率"""
        base = 0.6
        execution_factor = factors.get("execution", 0.7) / 0.7
        pain_match = factors.get("pain_point", 1.0)
        
        probability = base * execution_factor * pain_match
        return min(0.95, max(0.3, probability))
    
    def _assess_completeness(self, client_info: Dict, template: SolutionTemplateV2) -> float:
        """评估信息完整度"""
        required_params = [p for p in template.required_parameters if p.required]
        if not required_params:
            return 1.0
        
        provided = sum(1 for p in required_params if p.param_name in client_info)
        return provided / len(required_params)
    
    def _calculate_overall_confidence(self, outcome_result: Dict) -> float:
        """计算整体置信度"""
        outcomes = outcome_result.get("outcomes", [])
        if not outcomes:
            return 0.5
        
        total_confidence = sum(
            o.get("adjustment_factor", 0.7) * o.get("execution_factor", 0.7)
            for o in outcomes
        )
        return round(total_confidence / len(outcomes), 2)
    
    def _recommend_alternatives(self, 
                               current_solution: str,
                               client_info: Dict) -> List[Dict]:
        """推荐替代方案"""
        alternatives = []
        
        # get所有适用的解决方案
        industry = client_info.get("industry")
        all_solutions = self.get_solution_list(industry=industry)
        
        # 排除当前方案,取前2个
        for sol in all_solutions:
            if sol["solution_type"] != current_solution:
                alt_report = self.assess_solution(sol["solution_type"], client_info)
                alternatives.append({
                    "solution_type": sol["solution_type"],
                    "name": sol["name"],
                    "success_probability": alt_report.success_probability,
                    "why_consider": f"成功概率{alt_report.success_probability*100:.0f}%,可能更适合您的实际情况"
                })
                
                if len(alternatives) >= 2:
                    break
        
        return alternatives
    
    def _generate_comparison_recommendation(self, comparisons: List[Dict]) -> str:
        """generate对比建议"""
        if not comparisons:
            return "无可用对比数据"
        
        best = comparisons[0]
        return (
            f"建议优先选择'{best['solution_name']}',"
            f"预计成功概率为{best['success_probability']*100:.0f}%."
            f"该方案最符合您的行业特点和资源条件."
        )

# ==================== 便捷函数 ====================

def assess(solution_type: str, client_info: Dict) -> AssessmentReport:
    """
    快速评估函数
    
    示例:
        from src.growth_engine import assess
        
        report = assess("private_domain", {
            "industry": "美妆",
            "avg_order_value": 350,
            "execution_capability": 6.0,
            "pain_points": ["获客成本高", "用户留存低"]
        })
        
        logger.info(f"成功概率: {report.success_probability*100:.0f}%")
        for outcome in report.expected_outcomes:
            logger.info(f"{outcome['metric_name']}: {outcome['calculated_range']}")
    """
    engine = SolutionEngineV2()
    return engine.assess_solution(solution_type, client_info)

def compare(solution_types: List[str], client_info: Dict) -> Dict:
    """快速对比函数"""
    engine = SolutionEngineV2()
    return engine.compare_solutions(solution_types, client_info)

def list_solutions(industry: Optional[str] = None) -> List[Dict]:
    """快速列出解决方案"""
    engine = SolutionEngineV2()
    return engine.get_solution_list(industry=industry)

# ==================== 测试示例 ====================

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
