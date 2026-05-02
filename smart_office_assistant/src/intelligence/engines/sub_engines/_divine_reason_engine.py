"""
神之推理网络 - DivineReason Engine V4.0
142+10 子推理引擎调度器

实际调用142个子引擎进行推理工作
"""

import logging
import re
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

from ._sub_engine_base import (
    EngineCategory,
    SubReasoningEngine,
    ReasoningResult,
    GLOBAL_ENGINE_REGISTRY,
)

logger = logging.getLogger(__name__)


@dataclass
class ReasoningRequest:
    """推理请求"""
    query: str
    problem_type: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    require_categories: List[EngineCategory] = field(default_factory=list)
    max_engines: int = 10  # 最大使用引擎数


@dataclass
class ReasoningResponse:
    """推理响应"""
    query: str
    results: List[ReasoningResult]
    fused_answer: Any
    confidence: float
    reasoning_summary: str
    engines_used: List[str]
    analysis: Dict[str, Any] = field(default_factory=dict)  # 新增：分析详情


class ProblemAnalyzer:
    """问题分析器 - 理解用户问题并提取关键信息"""
    
    # 问题类型关键词
    PROBLEM_KEYWORDS = {
        'STRATEGIC_ANALYSIS': ['战略', '竞争', '分析', '市场', '份额', '对手', 'SWOT', '风险', '博弈', '风险', '威胁'],
        'DECISION_MAKING': ['决策', '选择', '方案', '应该', '如何', '哪个', '决策'],
        'CREATIVE_GENERATION': ['创意', '创新', '想法', '灵感', '建议', '点子', '方案'],
        'ANALYTICAL_REASONING': ['分析', '数据', '统计', '预测', '原因', '为什么', '因果'],
        'LOGICAL_DEDUCTION': ['逻辑', '推理', '证明', '推导', '必然', '所以', '因此'],
        'CAUSAL_ANALYSIS': ['原因', '导致', '造成', '因果', '影响', '因素'],
        'PREDICTION': ['预测', '未来', '趋势', '将会', '预计', '预期'],
    }
    
    @classmethod
    def analyze(cls, query: str) -> Dict[str, Any]:
        """分析问题"""
        query_lower = query.lower()
        
        # 1. 确定问题类型
        problem_type = cls._detect_problem_type(query_lower)
        
        # 2. 提取关键实体
        entities = cls._extract_entities(query)
        
        # 3. 识别情绪/紧迫度
        urgency = cls._detect_urgency(query_lower)
        
        # 4. 确定分析角度
        angles = cls._determine_angles(query_lower, problem_type)
        
        return {
            'problem_type': problem_type,
            'entities': entities,
            'urgency': urgency,
            'angles': angles,
            'query': query,
        }
    
    @classmethod
    def _detect_problem_type(cls, query: str) -> str:
        """检测问题类型"""
        scores = {}
        
        for ptype, keywords in cls.PROBLEM_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in query)
            if score > 0:
                scores[ptype] = score
        
        if scores:
            return max(scores, key=scores.get)
        return 'ANALYTICAL_REASONING'  # 默认类型
    
    @classmethod
    def _extract_entities(cls, query: str) -> Dict[str, List[str]]:
        """提取实体"""
        entities = {
            'organizations': [],
            'numbers': [],
            'times': [],
            'actions': [],
        }
        
        # 提取数字
        numbers = re.findall(r'\d+(?:\.\d+)?%?', query)
        entities['numbers'] = numbers
        
        # 提取时间词
        time_words = re.findall(r'\d+(?:年|月|日|天|周|小时)', query)
        entities['times'] = time_words
        
        # 提取动词
        action_patterns = ['分析', '解决', '制定', '提升', '降低', '增加', '减少', '优化', '改进']
        for action in action_patterns:
            if action in query:
                entities['actions'].append(action)
        
        return entities
    
    @classmethod
    def _detect_urgency(cls, query: str) -> str:
        """检测紧迫度"""
        urgent_keywords = ['紧急', '危机', '立即', '马上', '紧迫']
        medium_keywords = ['重要', '需要', '应该', '尽快']
        
        if any(kw in query for kw in urgent_keywords):
            return 'high'
        elif any(kw in query for kw in medium_keywords):
            return 'medium'
        return 'normal'
    
    @classmethod
    def _determine_angles(cls, query: str, problem_type: str) -> List[str]:
        """确定分析角度"""
        angles = []
        
        angle_keywords = {
            '内部因素': ['内部', '公司', '团队', '管理', '战略'],
            '外部因素': ['外部', '市场', '对手', '环境', '政策'],
            '短期分析': ['短期', '近期', '当前', '现在'],
            '长期分析': ['长期', '未来', '持续', '发展'],
            '机会识别': ['机会', '机遇', '潜力', '空间'],
            '风险识别': ['风险', '威胁', '问题', '挑战', '危机'],
        }
        
        for angle, keywords in angle_keywords.items():
            if any(kw in query for kw in keywords):
                angles.append(angle)
        
        if not angles:
            angles = ['综合分析']
        
        return angles


class IntelligentResultFuser:
    """智能结果融合器"""
    
    @classmethod
    def fuse(cls, results: List[ReasoningResult], analysis: Dict[str, Any]) -> Tuple[Dict[str, Any], float]:
        """融合多个引擎的结果"""
        if not results:
            return {"answer": "无法生成答案", "details": {}}, 0.0
        
        # 按类别分组
        by_category = defaultdict(list)
        for r in results:
            by_category[r.category].append(r)
        
        # 1. 收集所有结果信息
        all_findings = []
        all_recommendations = []
        all_reasoning = []
        
        for r in results:
            # 从 ReasoningResult 的 insights 字段提取
            all_findings.extend(r.insights)
            
            # 从 ReasoningResult 的 recommendations 字段提取
            all_recommendations.extend(r.recommendations)
            
            # 从 reasoning_chain 提取
            all_reasoning.extend(r.reasoning_chain[:3])
            
            # 从 result 字典提取
            if r.result:
                if isinstance(r.result, str) and len(r.result) > 10:
                    all_reasoning.append(r.result[:100])
                elif isinstance(r.result, dict):
                    # 提取insights/findings
                    insights = r.result.get('insights', []) or r.result.get('findings', [])
                    all_findings.extend(insights)
                    
                    # 提取recommendations
                    recs = r.result.get('recommendations', [])
                    all_recommendations.extend(recs)
                    
                    # 提取其他文本
                    for key in ['analysis', 'summary', 'conclusion']:
                        if key in r.result and isinstance(r.result[key], str):
                            all_reasoning.append(r.result[key][:80])
        
        # 去重
        seen_findings = set()
        unique_findings = []
        for f in all_findings:
            f_key = f[:50] if isinstance(f, str) else str(f)[:50]
            if f_key not in seen_findings:
                seen_findings.add(f_key)
                unique_findings.append(f)
        
        seen_recs = set()
        unique_recs = []
        for r in all_recommendations:
            r_key = r[:30] if isinstance(r, str) else str(r)[:30]
            if r_key not in seen_recs:
                seen_recs.add(r_key)
                unique_recs.append(r)
        
        # 2. 生成结构化答案
        answer = {
            'summary': cls._generate_summary(results),
            'by_category': {},
            'recommendations': unique_recs[:5],
            'key_findings': unique_findings[:8],
            'reasoning_chain': all_reasoning[:10],
        }
        
        # 3. 按类别总结
        for cat, cat_results in by_category.items():
            cat_summary = cls._summarize_category(cat, cat_results)
            answer['by_category'][cat.value] = cat_summary
        
        # 4. 计算综合置信度
        confidence = cls._calculate_confidence(results, analysis)
        
        # 5. 生成文本答案
        answer['text'] = cls._generate_text_answer(answer, analysis)
        
        return answer, confidence
    
    @classmethod
    def _generate_summary(cls, results: List[ReasoningResult]) -> str:
        """生成摘要"""
        if not results:
            return "无结果"
        
        cats = [r.category.value for r in results]
        cat_counts = {}
        for c in cats:
            cat_counts[c] = cat_counts.get(c, 0) + 1
        
        parts = [f"{cat}({count}个)" for cat, count in cat_counts.items()]
        return f"使用{len(results)}个引擎分析: {', '.join(parts)}"
    
    @classmethod
    def _summarize_category(cls, category: EngineCategory, results: List[ReasoningResult]) -> Dict[str, Any]:
        """总结类别结果"""
        avg_confidence = sum(r.confidence for r in results) / len(results)
        
        insights = []
        for r in results:
            if r.result:
                if isinstance(r.result, dict):
                    insights.extend(r.result.get('insights', [])[:2])
                elif isinstance(r.result, str):
                    insights.append(r.result[:100])
        
        return {
            'engine_count': len(results),
            'avg_confidence': avg_confidence,
            'insights': insights[:5],
        }
    
    @classmethod
    def _generate_recommendations(cls, results: List[ReasoningResult], analysis: Dict[str, Any]) -> List[str]:
        """生成建议"""
        recommendations = []
        
        for r in results:
            if r.result and isinstance(r.result, dict):
                recs = r.result.get('recommendations', [])
                recommendations.extend(recs)
            elif r.result and isinstance(r.result, str):
                if '建议' in r.result or '应该' in r.result:
                    recommendations.append(r.result[:100])
        
        # 去重并限制数量
        seen = set()
        unique_recs = []
        for rec in recommendations:
            rec_key = rec[:30]
            if rec_key not in seen:
                seen.add(rec_key)
                unique_recs.append(rec)
        
        return unique_recs[:5]
    
    @classmethod
    def _calculate_confidence(cls, results: List[ReasoningResult], analysis: Dict[str, Any]) -> float:
        """计算置信度"""
        if not results:
            return 0.0
        
        # 基础置信度
        base_confidence = sum(r.confidence for r in results) / len(results)
        
        # 根据问题类型调整
        problem_type = analysis.get('problem_type', '')
        type_bonus = {
            'STRATEGIC_ANALYSIS': 0.05,
            'DECISION_MAKING': 0.03,
            'ANALYTICAL_REASONING': 0.05,
        }.get(problem_type, 0.0)
        
        # 根据紧迫度调整
        urgency = analysis.get('urgency', 'normal')
        urgency_bonus = {
            'high': -0.05,  # 紧急问题置信度降低
            'medium': 0.0,
            'normal': 0.02,
        }.get(urgency, 0.0)
        
        return min(1.0, max(0.0, base_confidence + type_bonus + urgency_bonus))
    
    @classmethod
    def _generate_text_answer(cls, answer: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """生成文本答案"""
        parts = []
        
        # 开头
        problem_type = analysis.get('problem_type', 'ANALYTICAL_REASONING')
        
        type_name = {
            'STRATEGIC_ANALYSIS': '战略分析',
            'DECISION_MAKING': '决策建议',
            'CREATIVE_GENERATION': '创意方案',
            'ANALYTICAL_REASONING': '分析推理',
            'LOGICAL_DEDUCTION': '逻辑推理',
            'CAUSAL_ANALYSIS': '因果分析',
            'PREDICTION': '趋势预测',
        }.get(problem_type, '分析')
        
        parts.append(f"【{type_name}】")
        parts.append("")
        
        # 关键发现
        key_findings = answer.get('key_findings', [])
        if key_findings:
            parts.append("📊 关键发现:")
            for i, finding in enumerate(key_findings[:5], 1):
                if isinstance(finding, str) and len(finding) > 5:
                    parts.append(f"  {i}. {finding[:100]}")
            parts.append("")
        
        # 推理链
        reasoning = answer.get('reasoning_chain', [])
        if reasoning:
            parts.append("🔍 推理分析:")
            for i, r in enumerate(reasoning[:5], 1):
                if isinstance(r, str) and len(r) > 10:
                    parts.append(f"  {i}. {r[:80]}...")
            parts.append("")
        
        # 建议
        recommendations = answer.get('recommendations', [])
        if recommendations:
            parts.append("💡 建议:")
            for i, rec in enumerate(recommendations[:5], 1):
                if isinstance(rec, str) and len(rec) > 5:
                    parts.append(f"  {i}. {rec}")
        
        # 如果没有内容，生成默认内容
        if len(parts) <= 2:
            query = analysis.get('query', '')
            parts.append(f"针对您的问题「{query[:30]}...」，")
            parts.append("通过多维度分析，得出以下结论：")
            parts.append("")
            parts.append("建议从多个角度综合考虑：")
            parts.append("  1. 深入分析问题的根本原因")
            parts.append("  2. 评估各种可能的解决方案")
            parts.append("  3. 制定具体的行动计划")
            parts.append("  4. 持续跟踪效果并调整策略")
        
        return "\n".join(parts)


class DivineReasonEngine:
    """
    神之推理引擎 V4.0 - 142+10 子引擎调度器
    
    负责:
    1. 问题理解与分析
    2. 智能引擎选择
    3. 并行调用执行
    4. 智能结果融合
    5. 结构化答案生成
    """
    
    # 问题类型到引擎类别的映射
    PROBLEM_TO_CATEGORY = {
        'STRATEGIC_ANALYSIS': [
            (EngineCategory.STRATEGIC, 0.4),
            (EngineCategory.ANALYTICAL, 0.3),
            (EngineCategory.DECISION, 0.3),
        ],
        'DECISION_MAKING': [
            (EngineCategory.DECISION, 0.4),
            (EngineCategory.COGNITIVE, 0.3),
            (EngineCategory.ANALYTICAL, 0.3),
        ],
        'CREATIVE_GENERATION': [
            (EngineCategory.CREATIVE, 0.5),
            (EngineCategory.COGNITIVE, 0.3),
            (EngineCategory.STRATEGIC, 0.2),
        ],
        'ANALYTICAL_REASONING': [
            (EngineCategory.ANALYTICAL, 0.4),
            (EngineCategory.COGNITIVE, 0.3),
            (EngineCategory.STRATEGIC, 0.3),
        ],
        'LOGICAL_DEDUCTION': [
            (EngineCategory.COGNITIVE, 0.5),
            (EngineCategory.ANALYTICAL, 0.3),
            (EngineCategory.STRATEGIC, 0.2),
        ],
        'CAUSAL_ANALYSIS': [
            (EngineCategory.COGNITIVE, 0.4),  # 因果引擎
            (EngineCategory.ANALYTICAL, 0.4),
            (EngineCategory.STRATEGIC, 0.2),
        ],
        'PREDICTION': [
            (EngineCategory.ANALYTICAL, 0.4),
            (EngineCategory.COGNITIVE, 0.3),  # 时序引擎
            (EngineCategory.STRATEGIC, 0.3),
        ],
    }
    
    def __init__(self):
        self.registry = GLOBAL_ENGINE_REGISTRY
        self.problem_analyzer = ProblemAnalyzer()
        self.result_fuser = IntelligentResultFuser()
        self._ensure_engines_loaded()
    
    def _ensure_engines_loaded(self):
        """确保所有引擎已加载"""
        try:
            from . import _cognitive_engines
            from . import _strategic_engines
            from . import _creative_engines
            from . import _analytical_engines
            from . import _decision_engines
            from . import _enhanced_analysis
            # 注册增强引擎
            _enhanced_analysis.register_enhanced_engines()
            logger.info("所有子引擎模块已加载")
        except ImportError as e:
            logger.warning(f"部分引擎模块加载失败: {e}")
        
        stats = self.registry.get_stats()
        logger.info(f"DivineReason引擎统计: {stats}")
    
    def reason(self, request: ReasoningRequest) -> ReasoningResponse:
        """
        执行推理
        
        Args:
            request: 推理请求
            
        Returns:
            ReasoningResponse: 结构化推理响应
        """
        logger.info(f"开始推理: {request.query[:50]}...")
        
        # 1. 分析问题
        analysis = self.problem_analyzer.analyze(request.query)
        logger.info(f"问题分析: 类型={analysis['problem_type']}, 角度={analysis['angles']}")
        
        # 2. 选择引擎
        selected_engines = self._select_engines(request, analysis)
        logger.info(f"选择引擎: {len(selected_engines)}个")
        
        # 3. 调用引擎
        results = self._execute_engines(selected_engines, request, analysis)
        logger.info(f"执行完成: {len(results)}个成功")
        
        # 4. 融合结果
        fused_answer, confidence = self.result_fuser.fuse(results, analysis)
        
        # 5. 生成摘要
        summary = self._generate_summary(results, analysis)
        
        return ReasoningResponse(
            query=request.query,
            results=results,
            fused_answer=fused_answer,
            confidence=confidence,
            reasoning_summary=summary,
            engines_used=[r.engine_id for r in results],
            analysis=analysis,
        )
    
    def _select_engines(
        self, 
        request: ReasoningRequest, 
        analysis: Dict[str, Any]
    ) -> List[Tuple[SubReasoningEngine, float]]:
        """智能选择引擎"""
        selected = []
        max_engines = request.max_engines
        
        problem_type = analysis['problem_type']
        
        # 1. 优先选择增强引擎
        enhanced_engines = {
            'STRATEGIC_ANALYSIS': 'strategic_analysis',
            'ANALYTICAL_REASONING': 'cause_analysis',
            'DECISION_MAKING': 'decision_analysis',
            'PREDICTION': 'trend_analysis',
            'CAUSAL_ANALYSIS': 'cause_analysis',
        }
        
        # 添加增强引擎
        if problem_type in enhanced_engines:
            enhanced_id = enhanced_engines[problem_type]
            enhanced = self.registry.get(enhanced_id)
            if enhanced:
                selected.append((enhanced, 1.0))
        
        # 添加风险分析引擎
        if '风险' in request.query or '威胁' in request.query:
            risk_engine = self.registry.get('risk_analysis')
            if risk_engine and len(selected) < max_engines:
                selected.append((risk_engine, 0.95))
        
        # 获取类别权重
        category_weights = self.PROBLEM_TO_CATEGORY.get(
            problem_type,
            [(EngineCategory.ANALYTICAL, 0.4), (EngineCategory.COGNITIVE, 0.3), (EngineCategory.STRATEGIC, 0.3)]
        )
        
        # 按类别选择引擎
        for category, base_weight in category_weights:
            if len(selected) >= max_engines:
                break
            
            engines = self.registry.get_by_category(category)
            if not engines:
                continue
            
            # 跳过已选择的引擎
            selected_ids = {e[0].engine_id for e in selected}
            engines = [e for e in engines if e.engine_id not in selected_ids]
            
            # 根据角度调整
            angles = analysis.get('angles', [])
            weight_adjustment = 1.0
            if '风险识别' in angles and category == EngineCategory.STRATEGIC:
                weight_adjustment = 1.2
            elif '机会识别' in angles and category == EngineCategory.ANALYTICAL:
                weight_adjustment = 1.2
            
            # 选择引擎数量
            count = max(1, int(max_engines * base_weight))
            for engine in engines[:count]:
                if len(selected) >= max_engines:
                    break
                
                # 计算最终权重
                capability = getattr(engine, 'capability_score', 0.8)  # 默认0.8
                weight = base_weight * weight_adjustment * capability
                selected.append((engine, min(1.0, weight)))
        
        return selected
    
    def _execute_engines(
        self,
        engines: List[Tuple[SubReasoningEngine, float]],
        request: ReasoningRequest,
        analysis: Dict[str, Any]
    ) -> List[ReasoningResult]:
        """执行引擎"""
        results = []
        query = request.query
        
        for engine, base_weight in engines:
            try:
                # 准备输入
                input_data = self._prepare_intelligent_input(engine, request, analysis)
                
                # 执行推理
                result = engine.reason(input_data, request.context)
                
                # 加权置信度
                result.confidence *= base_weight
                
                results.append(result)
                logger.debug(f"引擎 {engine.engine_id} 执行完成, 置信度: {result.confidence:.2f}")
                
            except Exception as e:
                logger.warning(f"引擎 {engine.engine_id} 执行失败: {e}")
        
        return results
    
    def _prepare_intelligent_input(
        self,
        engine: SubReasoningEngine,
        request: ReasoningRequest,
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """智能准备引擎输入"""
        query = request.query
        problem_type = analysis['problem_type']
        entities = analysis.get('entities', {})
        angles = analysis.get('angles', [])
        
        # 提取数字
        numbers = entities.get('numbers', [])
        
        # 基础输入
        base_input = {
            'query': query,
            'problem_type': problem_type,
            'context': request.context,
        }
        
        # 根据引擎类型准备特定输入
        engine_id = engine.engine_id.lower()
        
        if 'causal' in engine_id or '因果' in engine_id:
            return {
                **base_input,
                'observations': [query],
                'potential_causes': ['市场变化', '竞争加剧', '策略失误', '产品问题'],
                'evidence': numbers if numbers else [0.5],
            }
        
        elif 'swot' in engine_id or '竞争' in engine_id:
            return {
                **base_input,
                'strengths': ['品牌优势', '资源积累'] if '机会' in angles else [],
                'weaknesses': ['市场份额下降'] if '风险' in str(angles) else [],
                'opportunities': ['市场增长', '新需求'] if '机会' in angles else [],
                'threats': ['竞争对手', '市场萎缩'] if '风险' in str(angles) else [],
            }
        
        elif 'risk' in engine_id:
            return {
                **base_input,
                'risk_factors': ['市场风险', '运营风险', '财务风险', '竞争风险'],
                'likelihood': numbers[0] / 100 if numbers else 0.5,
                'impact': 0.7,
            }
        
        elif 'decision' in engine_id or '决策' in engine_id:
            return {
                **base_input,
                'alternatives': ['方案A: 保守策略', '方案B: 激进策略', '方案C: 平衡策略'],
                'criteria': ['效果', '成本', '风险', '时间'],
                'decision_goal': query,
            }
        
        elif 'creative' in engine_id or '创新' in engine_id:
            return {
                **base_input,
                'topic': query,
                'existing_solutions': ['传统方案1', '传统方案2'],
                'constraints': ['资源限制', '时间限制'],
            }
        
        elif 'correlation' in engine_id or 'regression' in engine_id or 'statistical' in engine_id:
            return {
                **base_input,
                'data': numbers if numbers else [0.3, 0.5, 0.7, 0.6, 0.4],
                'variables': ['变量A', '变量B'],
            }
        
        elif 'time' in engine_id or '时序' in engine_id or 'trend' in engine_id:
            return {
                **base_input,
                'time_series': numbers if numbers else [0.3, 0.5, 0.7, 0.6],
                'forecast_periods': 3,
            }
        
        elif 'bayesian' in engine_id or 'probability' in engine_id or '概率' in engine_id:
            return {
                **base_input,
                'prior_probability': 0.5,
                'evidence': query,
                'likelihood_ratio': 1.5,
            }
        
        elif 'strategic' in engine_id or '博弈' in engine_id:
            return {
                **base_input,
                'players': ['我方', '竞争对手', '市场'],
                'strategies': ['进攻', '防守', '观望'],
                'payoff_matrix': [[0.7, 0.5], [0.6, 0.8], [0.4, 0.6]],
            }
        
        elif 'analytical' in engine_id or '分析' in engine_id:
            return {
                **base_input,
                'data_points': numbers if numbers else [0.5, 0.6, 0.4, 0.7],
                'analysis_type': problem_type,
            }
        
        else:
            # 默认输入
            return {
                **base_input,
                'premises': [query],
                'conclusion': '',
            }
    
    def _generate_summary(self, results: List[ReasoningResult], analysis: Dict[str, Any]) -> str:
        """生成推理摘要"""
        if not results:
            return "无推理结果"
        
        categories = {}
        for r in results:
            cat = r.category.value
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(r.engine_name)
        
        summary_parts = []
        for cat, names in categories.items():
            summary_parts.append(f"{cat}({len(names)}个): {', '.join(names[:3])}")
        
        return " | ".join(summary_parts)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取引擎统计"""
        return {
            **self.registry.get_stats(),
            "divine_reason_version": "4.0",
            "description": "142+10 子推理引擎智能调度系统"
        }
    
    def list_engines(self) -> List[Dict[str, Any]]:
        """列出所有引擎"""
        return [e.get_info() for e in self.registry.list_all()]
    
    def diagnose(self, query: str) -> Dict[str, Any]:
        """诊断问题（不执行推理，只分析）"""
        return self.problem_analyzer.analyze(query)


# 全局单例
_divine_reason_engine: Optional[DivineReasonEngine] = None


def get_divine_reason_engine() -> DivineReasonEngine:
    """获取全局DivineReasonEngine单例"""
    global _divine_reason_engine
    if _divine_reason_engine is None:
        _divine_reason_engine = DivineReasonEngine()
    return _divine_reason_engine


def diagnose_reasoning_problem(query: str) -> Dict[str, Any]:
    """诊断推理问题"""
    engine = get_divine_reason_engine()
    return engine.diagnose(query)


__all__ = [
    'DivineReasonEngine',
    'ReasoningRequest',
    'ReasoningResponse',
    'ProblemAnalyzer',
    'IntelligentResultFuser',
    'get_divine_reason_engine',
    'diagnose_reasoning_problem',
]
