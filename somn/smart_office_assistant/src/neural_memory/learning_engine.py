"""
__all__ = [
    'apply_memory_decay',
    'learn_by_reinforcement',
    'learn_by_transfer',
    'learn_from_association',
    'learn_from_error',
    'learn_from_instance',
    'learn_from_validation',
    'save_learning_event',
]

自主学习引擎
Learning Engine
"""

import json
import yaml
from pathlib import Path
from src.core.paths import LEARNING_DIR
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import math

class LearningType(Enum):
    """学习类型"""
    INSTANCE = "实例学习"      # 从具体案例中提取模式
    VALIDATION = "验证学习"    # 通过验证结果修正置信度
    ERROR = "错误学习"        # 从失败中recognize错误假设
    ASSOCIATION = "关联学习"  # 发现新的概念关联
    TRANSFER = "迁移学习"     # 将知识应用到新场景
    REINFORCEMENT = "强化学习" # 基于反馈调整行为

@dataclass
class LearningEvent:
    """学习事件"""
    event_id: str
    event_type: LearningType
    trigger: str              # 触发源
    input_data: Dict          # 输入数据
    learning_result: Dict     # 学习结果
    knowledge_updates: List   # 知识更新列表
    confidence_change: float  # 置信度变化
    created_at: str

class LearningEngine:
    """神经记忆系统 - 自主学习引擎"""
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else LEARNING_DIR
        self.learning_path = self.base_path / "learning"
        self.patterns_path = self.learning_path / "patterns"
        
        # 创建必要的目录
        self.learning_path.mkdir(parents=True, exist_ok=True)
        self.patterns_path.mkdir(parents=True, exist_ok=True)
        
        # 学习参数
        self.params = {
            "min_sample_size": 5,        # 最小样本量
            "confidence_threshold": 0.7,  # 置信度阈值
            "decay_rate": 0.01,          # 记忆衰减率
            "reinforcement_rate": 0.1,   # 强化学习率
            "pattern_threshold": 0.6     # 模式recognize阈值
        }
        
        # 贝叶斯更新参数
        self.bayesian_params = {
            "prior_weight": 0.3,
            "evidence_weight": 0.7
        }
    
    def learn_from_instance(self, instances: List[Dict], 
                           pattern_type: str) -> Tuple[Dict, LearningEvent]:
        """
        实例学习:从具体案例中提取模式
        
        Args:
            instances: 实例列表 [{characteristics, 结果, 置信度}]
            pattern_type: 模式类型
            
        Returns:
            (提取的模式, 学习事件)
        """
        if len(instances) < self.params["min_sample_size"]:
            return None, None
        
        # 提取共同characteristics
        common_features = self._extract_common_features(instances)
        
        # 计算模式强度
        pattern_strength = self._calculate_pattern_strength(instances, common_features)
        
        # 如果模式强度足够高,则确认为有效模式
        if pattern_strength >= self.params["pattern_threshold"]:
            pattern = {
                "模式ID": f"PAT_{datetime.now().strftime('%Y%m%d')}_{len(instances)}",
                "模式类型": pattern_type,
                "共同characteristics": common_features,
                "支持实例数": len(instances),
                "模式强度": pattern_strength,
                "创建时间": datetime.now().isoformat(),
                "验证状态": "待验证"
            }
            
            # 保存模式
            pattern_file = self.patterns_path / f"{pattern['模式ID']}.yaml"
            with open(pattern_file, 'w', encoding='utf-8') as f:
                yaml.dump(pattern, f, allow_unicode=True, default_flow_style=False)
            
            # 创建学习事件
            event = LearningEvent(
                event_id=f"LE_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                event_type=LearningType.INSTANCE,
                trigger=f"从{len(instances)}个实例中提取模式",
                input_data={"实例数": len(instances), "模式类型": pattern_type},
                learning_result=pattern,
                knowledge_updates=[{
                    "更新类型": "新增模式",
                    "模式ID": pattern["模式ID"],
                    "置信度": pattern_strength
                }],
                confidence_change=pattern_strength,
                created_at=datetime.now().isoformat()
            )
            
            return pattern, event
        
        return None, None
    
    def learn_from_validation(self, hypothesis_id: str, 
                              validation_result: Dict) -> LearningEvent:
        """
        验证学习:通过验证结果修正置信度
        
        使用贝叶斯更新:
        P(H|E) = P(E|H) × P(H) / P(E)
        
        Args:
            hypothesis_id: 假设ID
            validation_result: 验证结果 {是否通过, 样本量, 效应量, p值, ...}
            
        Returns:
            学习事件
        """
        # 原始置信度(从假设中get,这里简化处理)
        prior_confidence = validation_result.get("original_confidence", 0.5)
        
        # 验证是否通过
        passed = validation_result.get("passed", False)
        sample_size = validation_result.get("sample_size", 0)
        effect_size = validation_result.get("effect_size", 0)
        p_value = validation_result.get("p_value", 1.0)
        
        # 计算证据强度
        # 样本量越大,证据越强
        sample_factor = min(1.0, sample_size / 100)
        
        # 效应量越大,证据越强
        effect_factor = min(1.0, abs(effect_size))
        
        # p值越小,证据越强
        significance_factor = max(0, 1 - p_value)
        
        # synthesize证据强度
        evidence_strength = (sample_factor + effect_factor + significance_factor) / 3
        
        # 贝叶斯更新
        if passed:
            # 验证通过,增强置信度
            likelihood = 0.8 + evidence_strength * 0.15  # 0.80 - 0.95
        else:
            # 验证失败,降低置信度
            likelihood = 0.2 - evidence_strength * 0.15  # 0.05 - 0.20
        
        # 简化的贝叶斯更新
        posterior_confidence = (likelihood * prior_confidence) / (
            likelihood * prior_confidence + (1 - likelihood) * (1 - prior_confidence)
        )
        
        # 置信度变化
        confidence_change = posterior_confidence - prior_confidence
        
        # 创建学习事件
        event = LearningEvent(
            event_id=f"LE_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            event_type=LearningType.VALIDATION,
            trigger=f"假设{hypothesis_id}的验证结果",
            input_data={
                "假设ID": hypothesis_id,
                "验证结果": "通过" if passed else "失败",
                "样本量": sample_size,
                "效应量": effect_size,
                "p值": p_value
            },
            learning_result={
                "先验置信度": prior_confidence,
                "后验置信度": posterior_confidence,
                "置信度变化": confidence_change
            },
            knowledge_updates=[{
                "更新类型": "置信度更新",
                "假设ID": hypothesis_id,
                "原置信度": prior_confidence,
                "新置信度": posterior_confidence
            }],
            confidence_change=confidence_change,
            created_at=datetime.now().isoformat()
        )
        
        return event
    
    def learn_from_error(self, error_case: Dict) -> LearningEvent:
        """
        错误学习:从失败中recognize错误假设
        
        Args:
            error_case: 错误案例 {假设, 实际结果, 错误原因, ...}
            
        Returns:
            学习事件
        """
        hypothesis = error_case.get("hypothesis", "")
        actual_result = error_case.get("actual_result", "")
        error_reason = error_case.get("error_reason", "")
        
        # 分析错误类型
        error_type = self._classify_error_type(error_case)
        
        # 提取错误模式
        error_pattern = {
            "错误类型": error_type,
            "错误假设": hypothesis,
            "实际情况": actual_result,
            "错误原因": error_reason,
            "改进建议": self._generate_improvement(error_case, error_type)
        }
        
        # 更新相关知识(标记为需要修正)
        knowledge_updates = [{
            "更新类型": "错误标记",
            "假设": hypothesis,
            "错误类型": error_type,
            "置信度调整": -0.3  # 大幅降低置信度
        }]
        
        # 创建学习事件
        event = LearningEvent(
            event_id=f"LE_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            event_type=LearningType.ERROR,
            trigger="假设验证失败",
            input_data=error_case,
            learning_result=error_pattern,
            knowledge_updates=knowledge_updates,
            confidence_change=-0.3,
            created_at=datetime.now().isoformat()
        )
        
        return event
    
    def learn_from_association(self, concept_a: str, concept_b: str,
                               association_evidence: List[Dict]) -> LearningEvent:
        """
        关联学习:发现新的概念关联
        
        Args:
            concept_a: 概念A
            concept_b: 概念B
            association_evidence: 关联证据列表
            
        Returns:
            学习事件
        """
        # 计算关联强度
        # 基于共现频率,因果证据,统计相关性等
        
        evidence_count = len(association_evidence)
        
        # 共现频率
        co_occurrence = sum(1 for e in association_evidence if e.get("co_occurred", False))
        co_occurrence_rate = co_occurrence / evidence_count if evidence_count > 0 else 0
        
        # 统计相关性(如果有)
        correlations = [e.get("correlation", 0) for e in association_evidence if "correlation" in e]
        avg_correlation = sum(correlations) / len(correlations) if correlations else 0
        
        # 关联类型judge
        if avg_correlation > 0.5:
            association_type = "正相关"
        elif avg_correlation < -0.5:
            association_type = "负相关"
        elif co_occurrence_rate > 0.7:
            association_type = "共现"
        else:
            association_type = "弱关联"
        
        # 关联强度
        association_strength = (co_occurrence_rate + abs(avg_correlation)) / 2
        
        # 如果关联强度足够,创建新关联
        knowledge_updates = []
        if association_strength >= self.params["pattern_threshold"]:
            knowledge_updates.append({
                "更新类型": "新增关联",
                "概念A": concept_a,
                "概念B": concept_b,
                "关联类型": association_type,
                "关联强度": association_strength,
                "证据数": evidence_count
            })
        
        # 创建学习事件
        event = LearningEvent(
            event_id=f"LE_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            event_type=LearningType.ASSOCIATION,
            trigger=f"发现{concept_a}与{concept_b}的潜在关联",
            input_data={
                "概念A": concept_a,
                "概念B": concept_b,
                "证据数": evidence_count
            },
            learning_result={
                "关联类型": association_type,
                "关联强度": association_strength,
                "共现率": co_occurrence_rate,
                "平均相关性": avg_correlation
            },
            knowledge_updates=knowledge_updates,
            confidence_change=association_strength,
            created_at=datetime.now().isoformat()
        )
        
        return event
    
    def learn_by_transfer(self, source_knowledge: Dict, 
                         target_scenario: Dict) -> LearningEvent:
        """
        迁移学习:将知识应用到新场景
        
        Args:
            source_knowledge: 源知识 {概念, 规则, 置信度, 适用场景}
            target_scenario: 目标场景 {场景名, characteristics, 差异点}
            
        Returns:
            学习事件
        """
        # 评估迁移可行性
        source_confidence = source_knowledge.get("confidence", 0.5)
        source_scenarios = source_knowledge.get("applicable_scenarios", [])
        
        # 场景相似度评估
        similarity = self._assess_scenario_similarity(source_scenarios, target_scenario)
        
        # 迁移置信度 = 源置信度 × 场景相似度 × 迁移衰减
        transfer_decay = 0.85  # 迁移带来的置信度衰减
        transfer_confidence = source_confidence * similarity * transfer_decay
        
        # 需要验证的假设
        transfer_hypothesis = {
            "源知识": source_knowledge.get("concept", ""),
            "目标场景": target_scenario.get("场景名", ""),
            "迁移假设": f"{source_knowledge.get('concept', '')}在{target_scenario.get('场景名', '')}中可能适用",
            "迁移置信度": transfer_confidence,
            "需要验证": transfer_confidence < self.params["confidence_threshold"],
            "验证建议": self._generate_validation_plan(target_scenario, source_knowledge)
        }
        
        # 创建学习事件
        event = LearningEvent(
            event_id=f"LE_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            event_type=LearningType.TRANSFER,
            trigger=f"知识迁移:从{source_knowledge.get('concept', '')}到{target_scenario.get('场景名', '')}",
            input_data={
                "源知识": source_knowledge,
                "目标场景": target_scenario
            },
            learning_result=transfer_hypothesis,
            knowledge_updates=[{
                "更新类型": "知识迁移",
                "迁移假设": transfer_hypothesis["迁移假设"],
                "置信度": transfer_confidence
            }],
            confidence_change=transfer_confidence - source_confidence,
            created_at=datetime.now().isoformat()
        )
        
        return event
    
    def learn_by_reinforcement(self, action: str, outcome: Dict,
                               previous_state: Dict) -> LearningEvent:
        """
        强化学习:基于反馈调整行为
        
        Args:
            action: 执行的action
            outcome: 结果 {成功, 奖励, 惩罚, ...}
            previous_state: 之前的状态
            
        Returns:
            学习事件
        """
        # 提取反馈
        success = outcome.get("success", False)
        reward = outcome.get("reward", 0)
        penalty = outcome.get("penalty", 0)
        
        # 计算净反馈
        net_feedback = reward - penalty
        
        # 更新动作价值
        learning_rate = self.params["reinforcement_rate"]
        
        # 简化的Q-learning更新
        # Q(s,a) = Q(s,a) + α × (r + γ × max(Q(s',a')) - Q(s,a))
        old_value = previous_state.get("action_value", 0.5)
        new_value = old_value + learning_rate * (net_feedback - old_value)
        
        # 确保值在合理范围内
        new_value = max(0, min(1, new_value))
        
        # 价值变化
        value_change = new_value - old_value
        
        # 创建学习事件
        event = LearningEvent(
            event_id=f"LE_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            event_type=LearningType.REINFORCEMENT,
            trigger=f"action反馈:{action}",
            input_data={
                "action": action,
                "结果": outcome,
                "原状态": previous_state
            },
            learning_result={
                "原动作价值": old_value,
                "新动作价值": new_value,
                "价值变化": value_change,
                "净反馈": net_feedback
            },
            knowledge_updates=[{
                "更新类型": "价值更新",
                "action": action,
                "原价值": old_value,
                "新价值": new_value
            }],
            confidence_change=value_change,
            created_at=datetime.now().isoformat()
        )
        
        return event
    
    def apply_memory_decay(self, memories: List[Dict]) -> List[Dict]:
        """
        应用记忆衰减:模拟遗忘过程
        
        Args:
            memories: 记忆列表
            
        Returns:
            更新后的记忆列表
        """
        decay_rate = self.params["decay_rate"]
        now = datetime.now()
        
        for memory in memories:
            created_at = datetime.fromisoformat(memory.get("创建时间", now.isoformat()))
            days_passed = (now - created_at).days
            
            # 越久未访问,衰减越多
            decay_factor = math.exp(-decay_rate * days_passed)
            
            # 更新置信度
            old_confidence = memory.get("置信度", 0.5)
            memory["置信度"] = old_confidence * decay_factor
            
            # 如果置信度太低,标记为弱记忆
            if memory["置信度"] < 0.2:
                memory["状态"] = "弱记忆"
        
        return memories
    
    def _extract_common_features(self, instances: List[Dict]) -> Dict:
        """提取共同characteristics"""
        common = {}
        
        # 简化的characteristics提取:找到所有实例共有的属性
        if not instances:
            return common
        
        # get第一个实例的所有属性
        first_instance = instances[0]
        
        for key in first_instance:
            # 检查该属性在所有实例中是否相同
            values = [inst.get(key) for inst in instances]
            
            # 如果是列表,计算交集
            if isinstance(first_instance.get(key), list):
                common[key] = list(set.intersection(*[set(v) if isinstance(v, list) else set() for v in values]))
            # 如果是字符串,检查是否相同
            elif all(v == values[0] for v in values):
                common[key] = values[0]
        
        return common
    
    def _calculate_pattern_strength(self, instances: List[Dict], 
                                    common_features: Dict) -> float:
        """计算模式强度"""
        # 样本量因子
        sample_factor = min(1.0, len(instances) / 10)
        
        # 共同characteristics比例
        feature_ratio = len(common_features) / max(1, len(instances[0])) if instances else 0
        
        # 平均置信度
        avg_confidence = sum(inst.get("置信度", 0.5) for inst in instances) / len(instances)
        
        # synthesize强度
        strength = (sample_factor + feature_ratio + avg_confidence) / 3
        
        return strength
    
    def _classify_error_type(self, error_case: Dict) -> str:
        """分类错误类型"""
        reason = error_case.get("error_reason", "").lower()
        
        if "样本" in reason or "数据" in reason:
            return "样本偏差"
        elif "混淆" in reason or "变量" in reason:
            return "混淆变量"
        elif "因果" in reason:
            return "因果误判"
        elif "假设" in reason:
            return "假设错误"
        elif "边界" in reason or "范围" in reason:
            return "边界外推"
        else:
            return "其他错误"
    
    def _generate_improvement(self, error_case: Dict, error_type: str) -> str:
        """generate改进建议"""
        improvements = {
            "样本偏差": "增加样本量和样本多样性,避免选择性偏差",
            "混淆变量": "recognize并控制潜在的混淆变量",
            "因果误判": "进行更严格的因果检验,避免相关即因果的错误",
            "假设错误": "重新审视假设的合理性,考虑替代解释",
            "边界外推": "明确规则的适用边界,避免过度外推",
            "其他错误": "深入分析错误原因,完善研究设计"
        }
        return improvements.get(error_type, "需要进行更深入的分析")
    
    def _assess_scenario_similarity(self, source_scenarios: List, 
                                    target_scenario: Dict) -> float:
        """评估场景相似度"""
        if not source_scenarios:
            return 0.5
        
        # 简化处理:检查目标场景的characteristics是否在源场景中出现
        target_features = target_scenario.get("characteristics", [])
        
        similarity_scores = []
        for source in source_scenarios:
            source_features = source.get("characteristics", []) if isinstance(source, dict) else []
            common_features = set(target_features) & set(source_features)
            
            if target_features and source_features:
                similarity = len(common_features) / len(set(target_features) | set(source_features))
            else:
                similarity = 0.3  # 默认相似度
            
            similarity_scores.append(similarity)
        
        return max(similarity_scores) if similarity_scores else 0.5
    
    def _generate_validation_plan(self, target_scenario: Dict, 
                                  source_knowledge: Dict) -> Dict:
        """generate验证计划"""
        return {
            "验证方法": "A/B测试",
            "样本量建议": "至少500",
            "主要metrics": ["转化率", "用户满意度"],
            "控制变量": target_scenario.get("差异点", []),
            "验证周期": "2-4周"
        }
    
    def save_learning_event(self, event: LearningEvent) -> str:
        """保存学习事件"""
        event_file = self.learning_path / f"{event.event_id}.yaml"
        
        event_data = {
            "事件ID": event.event_id,
            "学习类型": event.event_type.value,
            "触发源": event.trigger,
            "输入数据": event.input_data,
            "学习结果": event.learning_result,
            "知识更新": event.knowledge_updates,
            "置信度变化": event.confidence_change,
            "创建时间": event.created_at
        }
        
        with open(event_file, 'w', encoding='utf-8') as f:
            yaml.dump(event_data, f, allow_unicode=True, default_flow_style=False)
        
        return event.event_id

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
