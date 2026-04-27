"""
__all__ = [
    'analyze_logical_structure',
    'detect_fallacies_in_argument',
    'export_logic_memory',
    'extract_logical_patterns',
    'get_logic_statistics',
    'import_logic_memory',
    'learn_from_valid_logic',
    'make_logical_inference',
    'validate_categorical_proposition',
    'validate_propositional_inference',
    'validate_reasoning_chain',
    'validate_syllogism',
]

逻辑学集成模块 (Logic Integration Module)
将柯匹<逻辑学导论>的逻辑引擎集成到神经记忆系统

功能:
1. 整合直言命题逻辑,三段论验证,命题逻辑和谬误检测
2. 增强神经记忆系统的逻辑推理能力
3. 提供逻辑验证接口给推理引擎
4. 记录逻辑学习成果

作者: AI工程师
创建时间: 2026-03-31
版本: 1.0.0
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
import json

from .categorical_logic import CategoricalLogicEngine
from .syllogism_validator import SyllogismValidator
from .propositional_logic import PropositionalLogicEngine, Proposition, LogicalOperator
from .fallacy_detector import FallacyDetector, FallacyDetection

@dataclass
class LogicValidationResult:
    """逻辑验证结果"""
    is_valid: bool
    validation_type: str              # 验证类型
    confidence: float                 # 置信度
    errors: List[str]                 # 错误列表
    suggestions: List[str]            # 改进建议
    raw_result: Dict[str, Any] = field(default_factory=dict)
    validated_at: datetime = field(default_factory=datetime.now)

@dataclass
class LogicalInference:
    """逻辑推理结果"""
    conclusion: str
    premises: List[str]
    inference_type: str               # 推理类型
    confidence: float
    fallacy_warnings: List[FallacyDetection] = field(default_factory=list)
    proof_steps: List[str] = field(default_factory=list)
    inferred_at: datetime = field(default_factory=datetime.now)

class LogicIntegration:
    """
    逻辑学集成模块
    
    整合所有逻辑学引擎,为神经记忆系统提供unified的逻辑验证和推理接口
    """
    
    def __init__(self):
        """init逻辑学集成模块"""
        # init各个逻辑引擎
        self.categorical_engine = CategoricalLogicEngine()
        self.syllogism_validator = SyllogismValidator()
        self.propositional_engine = PropositionalLogicEngine()
        self.fallacy_detector = FallacyDetector()
        
        # 逻辑学习记录
        self.logic_memory = {
            'valid_inferences': [],
            'detected_fallacies': [],
            'valid_syllogisms': [],
            'learned_patterns': []
        }
    
    def validate_categorical_proposition(self,
                                        proposition_text: str) -> LogicValidationResult:
        """
        验证直言命题
        
        Args:
            proposition_text: 命题文本
            
        Returns:
            验证结果
        """
        result = LogicValidationResult(
            is_valid=False,
            validation_type='categorical_proposition',
            confidence=0.0,
            errors=[],
            suggestions=[]
        )
        
        # 解析命题
        try:
            prop = self.categorical_engine.parse_proposition(proposition_text)
            
            if prop:
                result.is_valid = True
                result.confidence = 0.9
                result.raw_result = {
                    'type': prop.type.value,
                    'subject': prop.subject,
                    'predicate': prop.predicate,
                    'quantity': prop.quantity.value,
                    'distribution': {
                        'subject_distributed': prop.subject_distributed,
                        'predicate_distributed': prop.predicate_distributed
                    }
                }
            else:
                result.errors.append("无法解析直言命题")
                result.suggestions.append("确保命题格式正确: 所有/没有/有些 A 是/不是 B")
        
        except Exception as e:
            result.errors.append("解析错误")
        
        return result
    
    def validate_syllogism(self,
                          major_premise: str,
                          minor_premise: str,
                          conclusion: str) -> LogicValidationResult:
        """
        验证三段论
        
        Args:
            major_premise: 大前提
            minor_premise: 小前提
            conclusion: 结论
            
        Returns:
            验证结果
        """
        result = LogicValidationResult(
            is_valid=False,
            validation_type='syllogism',
            confidence=0.0,
            errors=[],
            suggestions=[]
        )
        
        try:
            # 先使用直言命题引擎解析命题
            major_prop = self.categorical_engine.parse_proposition(major_premise)
            minor_prop = self.categorical_engine.parse_proposition(minor_premise)
            conc_prop = self.categorical_engine.parse_proposition(conclusion)
            
            # 如果解析失败,返回错误
            if not major_prop or not minor_prop or not conc_prop:
                result.errors.append("无法解析一个或多个直言命题")
                result.suggestions.append("确保命题格式正确: 所有/没有/有些 A 是/不是 B")
                return result
            
            # 使用三段论验证器
            validation_result = self.syllogism_validator.validate(
                major_prop,
                minor_prop,
                conc_prop
            )

            result.is_valid = validation_result['is_valid']
            result.confidence = validation_result['confidence']
            result.errors = validation_result['errors']
            result.suggestions = validation_result['suggestions']
            result.raw_result = validation_result

        except Exception as e:
            result.errors.append("三段论验证错误")
            return result
        
        # 记录有效三段论
        if result.is_valid:
            self.logic_memory['valid_syllogisms'].append({
                'major': major_premise,
                'minor': minor_premise,
                'conclusion': conclusion,
                'timestamp': datetime.now().isoformat()
            })
        
        return result
    
    def validate_propositional_inference(self,
                                        premises: List[str],
                                        conclusion: str) -> LogicValidationResult:
        """
        验证命题逻辑推理
        
        Args:
            premises: 前提列表
            conclusion: 结论
            
        Returns:
            验证结果
        """
        result = LogicValidationResult(
            is_valid=False,
            validation_type='propositional_inference',
            confidence=0.0,
            errors=[],
            suggestions=[]
        )
        
        try:
            # 简化的命题解析 (实际实现需要更复杂的NLP)
            # 这里创建简单的原子命题
            prop_premises = []
            for i, premise in enumerate(premises):
                prop = Proposition(symbol=f"P{i}")
                prop_premises.append(prop)
            
            prop_conclusion = Proposition(symbol="C")
            
            # 检查蕴涵关系
            is_entailed = self.propositional_engine.check_entailment(
                prop_premises,
                prop_conclusion
            )
            
            result.is_valid = is_entailed
            result.confidence = 0.7 if is_entailed else 0.3
            result.raw_result = {
                'premises_count': len(premises),
                'premise_types': [type(p).__name__ for p in prop_premises],
                'conclusion_type': type(prop_conclusion).__name__
            }
            
            if not is_entailed:
                result.errors.append("结论不能从前提中逻辑推出")
                result.suggestions.append("检查推理规则应用是否正确")
                result.suggestions.append("确保前提足够支持结论")
        
        except Exception as e:
            result.errors.append("推理验证错误")
        
        return result
    
    def detect_fallacies_in_argument(self,
                                    argument: str) -> List[FallacyDetection]:
        """
        检测论证中的谬误
        
        Args:
            argument: 论证文本
            
        Returns:
            检测到的谬误列表
        """
        detections = self.fallacy_detector.detect_informal_fallacies(argument)
        
        # 记录检测到的谬误
        for detection in detections:
            self.logic_memory['detected_fallacies'].append({
                'fallacy_name': detection.fallacy_name,
                'category': detection.category.value,
                'confidence': detection.confidence,
                'argument_preview': argument[:100],
                'timestamp': datetime.now().isoformat()
            })
        
        return detections
    
    def analyze_logical_structure(self,
                                 argument: str) -> Dict[str, Any]:
        """
        分析论证的逻辑结构
        
        Args:
            argument: 论证文本
            
        Returns:
            逻辑结构分析
        """
        analysis = {
            'argument': argument,
            'fallacy_analysis': {},
            'argument_quality': {},
            'suggestions': []
        }
        
        # 检测谬误
        fallacies = self.detect_fallacies_in_argument(argument)
        
        if fallacies:
            analysis['fallacy_analysis'] = {
                'count': len(fallacies),
                'critical': [f.fallacy_name for f in fallacies if f.severity == 'critical'],
                'major': [f.fallacy_name for f in fallacies if f.severity == 'major'],
                'minor': [f.fallacy_name for f in fallacies if f.severity == 'minor'],
                'details': [
                    {
                        'name': f.fallacy_name,
                        'category': f.category.value,
                        'confidence': f.confidence
                    } for f in fallacies
                ]
            }
        
        # 分析论证质量
        quality_report = self.fallacy_detector.analyze_argument_quality(argument)
        analysis['argument_quality'] = quality_report
        
        # generate建议
        suggestions = self.fallacy_detector.suggest_improvements(argument)
        analysis['suggestions'] = suggestions
        
        return analysis
    
    def make_logical_inference(self,
                             premises: List[str],
                             inference_type: str = 'deductive') -> LogicalInference:
        """
        进行逻辑推理
        
        Args:
            premises: 前提列表
            inference_type: 推理类型 (deductive/inductive)
            
        Returns:
            推理结果
        """
        inference = LogicalInference(
            conclusion="",
            premises=premises,
            inference_type=inference_type,
            confidence=0.0
        )
        
        if len(premises) == 2:
            # 尝试三段论推理
            syllogism_result = self.syllogism_validator.validate(
                premises[0],
                premises[1],
                ""  # 暂时不指定结论
            )
            
            if syllogism_result['is_valid'] and 'conclusion' in syllogism_result:
                inference.conclusion = syllogism_result['conclusion']
                inference.confidence = syllogism_result['confidence']
                inference.proof_steps = syllogism_result.get('proof_steps', [])
        
        # 检测推理中的谬误
        argument = ' '.join(premises)
        if inference.conclusion:
            argument += f" 因此 {inference.conclusion}"
        
        fallacies = self.detect_fallacies_in_argument(argument)
        inference.fallacy_warnings = fallacies
        
        # 如果检测到严重谬误,降低置信度
        critical_fallacies = [f for f in fallacies if f.severity == 'critical']
        if critical_fallacies:
            inference.confidence *= 0.5
        
        # 记录有效推理
        if inference.confidence > 0.7:
            self.logic_memory['valid_inferences'].append({
                'premises': premises,
                'conclusion': inference.conclusion,
                'confidence': inference.confidence,
                'timestamp': datetime.now().isoformat()
            })
        
        return inference
    
    def validate_reasoning_chain(self,
                                reasoning_steps: List[Dict[str, str]]) -> LogicValidationResult:
        """
        验证推理链
        
        Args:
            reasoning_steps: 推理步骤列表,每步包含 premise 和 conclusion
            
        Returns:
            验证结果
        """
        result = LogicValidationResult(
            is_valid=True,
            validation_type='reasoning_chain',
            confidence=1.0,
            errors=[],
            suggestions=[]
        )
        
        all_errors = []
        all_suggestions = []
        min_confidence = 1.0
        
        for i, step in enumerate(reasoning_steps):
            premise = step.get('premise', '')
            conclusion = step.get('conclusion', '')
            
            # 验证每一步推理
            if '是' in premise and '是' in conclusion:
                # 可能是三段论
                if i + 1 < len(reasoning_steps):
                    next_premise = reasoning_steps[i + 1].get('premise', '')
                    validation = self.validate_syllogism(
                        premise,
                        next_premise,
                        conclusion
                    )
                else:
                    validation = LogicValidationResult(
                        is_valid=True,
                        validation_type='single_step',
                        confidence=0.6,
                        errors=[],
                        suggestions=[]
                    )
            else:
                # 一般推理验证
                validation = self.validate_propositional_inference(
                    [premise],
                    conclusion
                )
            
            if not validation.is_valid:
                result.is_valid = False
                all_errors.extend([f"步骤{i+1}: {err}" for err in validation.errors])
            
            all_suggestions.extend(validation.suggestions)
            min_confidence = min(min_confidence, validation.confidence)
        
        result.errors = all_errors
        result.suggestions = all_suggestions
        result.confidence = min_confidence
        
        return result
    
    def extract_logical_patterns(self,
                                text: str) -> List[Dict[str, Any]]:
        """
        从文本中提取逻辑模式
        
        Args:
            text: 文本内容
            
        Returns:
            提取的逻辑模式列表
        """
        patterns = []
        
        # 检测三段论模式
        # "所有A是B,所有C是A,所以所有C是B"
        if '所有' in text and '所以' in text:
            syllogism_pattern = self._extract_syllogism_pattern(text)
            if syllogism_pattern:
                patterns.append(syllogism_pattern)
        
        # 检测条件推理模式
        # "如果A,那么B. A,所以B"
        if '如果' in text or '那么' in text:
            conditional_pattern = self._extract_conditional_pattern(text)
            if conditional_pattern:
                patterns.append(conditional_pattern)
        
        # 检测因果模式
        # "因为A,所以B"
        if '因为' in text and '所以' in text:
            causal_pattern = self._extract_causal_pattern(text)
            if causal_pattern:
                patterns.append(causal_pattern)
        
        return patterns
    
    def _extract_syllogism_pattern(self, text: str) -> Optional[Dict[str, Any]]:
        """提取三段论模式"""
        # 简化实现
        sentences = text.split('.')
        if len(sentences) >= 3:
            major = sentences[0].strip()
            minor = sentences[1].strip()
            conclusion = sentences[2].strip()
            
            if '所有' in major and '所有' in minor and '所以' in conclusion:
                return {
                    'type': 'syllogism',
                    'major_premise': major,
                    'minor_premise': minor,
                    'conclusion': conclusion,
                    'confidence': 0.7
                }
        
        return None
    
    def _extract_conditional_pattern(self, text: str) -> Optional[Dict[str, Any]]:
        """提取条件推理模式"""
        # 简化实现
        if '如果' in text and '那么' in text:
            return {
                'type': 'conditional',
                'antecedent': '',
                'consequent': '',
                'confidence': 0.6
            }
        return None
    
    def _extract_causal_pattern(self, text: str) -> Optional[Dict[str, Any]]:
        """提取因果模式"""
        # 简化实现
        if '因为' in text and '所以' in text:
            return {
                'type': 'causal',
                'cause': '',
                'effect': '',
                'confidence': 0.6
            }
        return None
    
    def learn_from_valid_logic(self,
                              valid_inference: LogicalInference) -> None:
        """
        从有效的逻辑推理中学习
        
        Args:
            valid_inference: 有效的推理结果
        """
        if valid_inference.confidence > 0.8:
            pattern = {
                'inference_type': valid_inference.inference_type,
                'premises': valid_inference.premises,
                'conclusion': valid_inference.conclusion,
                'confidence': valid_inference.confidence,
                'learned_at': datetime.now().isoformat()
            }
            self.logic_memory['learned_patterns'].append(pattern)
    
    def get_logic_statistics(self) -> Dict[str, Any]:
        """get逻辑学习统计"""
        return {
            'valid_inferences_count': len(self.logic_memory['valid_inferences']),
            'detected_fallacies_count': len(self.logic_memory['detected_fallacies']),
            'valid_syllogisms_count': len(self.logic_memory['valid_syllogisms']),
            'learned_patterns_count': len(self.logic_memory['learned_patterns']),
            'total_validations': len(self.logic_memory['valid_inferences']) + 
                                len(self.logic_memory['valid_syllogisms']),
            'fallacy_categories': self._get_fallacy_category_distribution()
        }
    
    def _get_fallacy_category_distribution(self) -> Dict[str, int]:
        """get谬误类别分布"""
        distribution = {}
        
        for fallacy in self.logic_memory['detected_fallacies']:
            category = fallacy.get('category', 'unknown')
            distribution[category] = distribution.get(category, 0) + 1
        
        return distribution
    
    def export_logic_memory(self, filepath: str) -> None:
        """导出逻辑学习记忆"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.logic_memory, f, ensure_ascii=False, indent=2)
    
    def import_logic_memory(self, filepath: str) -> None:
        """导入逻辑学习记忆"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.logic_memory = json.load(f)

# 使用示例
# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
