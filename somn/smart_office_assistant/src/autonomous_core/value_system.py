"""
__all__ = [
    'evaluate_options',
    'get_values',
    'make_decision',
    'to_dict',
    'update_value_weight',
]

价值驱动decision系统 - Value System
实现智能体的价值judge和decision能力
"""

import json
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from loguru import logger

class ValueType(Enum):
    CORE = "core"
    STRATEGIC = "strategic"
    OPERATIONAL = "operational"

class DecisionType(Enum):
    GOAL_SELECTION = "goal_selection"
    ACTION_SELECTION = "action_selection"
    RESOURCE_ALLOCATION = "resource_allocation"

@dataclass
class Value:
    name: str
    description: str
    weight: float = 1.0
    value_type: ValueType = ValueType.CORE
    
    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'weight': self.weight,
            'value_type': self.value_type.value
        }

@dataclass
class Decision:
    decision_id: str
    decision_type: DecisionType
    selected_option: str
    reasoning: str
    confidence: float
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self):
        return {
            'decision_id': self.decision_id,
            'decision_type': self.decision_type.value,
            'selected_option': self.selected_option,
            'reasoning': self.reasoning,
            'confidence': self.confidence,
            'created_at': self.created_at
        }

class ValueSystem:
    """价值系统 - 基于价值的decision"""
    
    # 默认价值观
    DEFAULT_VALUES = [
        Value("用户价值", "最大化对用户的帮助和价值", 0.95, ValueType.CORE),
        Value("准确性", "提供准确可靠的信息和建议", 0.90, ValueType.CORE),
        Value("效率", "高效完成任务", 0.75, ValueType.STRATEGIC),
        Value("可解释性", "decision过程透明可解释", 0.70, ValueType.STRATEGIC),
        Value("安全性", "确保操作安全", 0.85, ValueType.CORE),
        Value("持续学习", "从经验中持续改进", 0.65, ValueType.OPERATIONAL),
        Value("自主性", "在适当范围内自主decision", 0.60, ValueType.OPERATIONAL),
    ]
    
    def __init__(self, storage_path: str = "data/values"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._values: List[Value] = self.DEFAULT_VALUES.copy()
        self._decisions: List[Decision] = []
        self._load_data()
        logger.info(f"价值系统init完成,{len(self._values)} 个价值观")
    
    def _load_data(self):
        """加载价值观（空文件/损坏时优雅降级）"""
        values_file = self.storage_path / "values.json"
        if values_file.exists():
            try:
                with open(values_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                if not content:
                    logger.info("values.json 为空，初始化为空价值观列表")
                    self._values = []
                    return
                data = json.loads(content)
                self._values = [
                    Value(v['name'], v['description'], v['weight'], ValueType(v['value_type']))
                    for v in data.get('values', [])
                ]
            except json.JSONDecodeError as e:
                logger.warning(f"values.json 格式损坏 ({e})，初始化为空价值观列表")
                self._values = []
            except Exception as e:
                logger.warning(f"加载价值观失败 ({e})，初始化为空价值观列表")
                self._values = []
    
    def _save_data(self):
        try:
            values_file = self.storage_path / "values.json"
            with open(values_file, 'w', encoding='utf-8') as f:
                json.dump({'values': [v.to_dict() for v in self._values]}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存价值观失败: {e}")
    
    def evaluate_options(
        self,
        options: List[Dict[str, Any]],
        criteria: Optional[List[str]] = None
    ) -> List[Tuple[Dict, float, str]]:
        """
        评估选项
        返回: [(选项, 得分, 理由), ...]
        """
        results = []
        for option in options:
            score, reasoning = self._evaluate_single(option, criteria)
            results.append((option, score, reasoning))
        return sorted(results, key=lambda x: x[1], reverse=True)
    
    def _evaluate_single(self, option: Dict, criteria: Optional[List[str]]) -> Tuple[float, str]:
        score = 0.0
        reasons = []
        
        for value in self._values:
            if criteria and value.name not in criteria:
                continue
            
            # 根据选项属性评估
            value_score = self._assess_value_alignment(option, value)
            weighted_score = value_score * value.weight
            score += weighted_score
            
            if value_score > 0.7:
                reasons.append(f"符合{value.name}")
            elif value_score < 0.3:
                reasons.append(f"可能违背{value.name}")
        
        return score, "; ".join(reasons) if reasons else "常规选项"
    
    def _assess_value_alignment(self, option: Dict, value: Value) -> float:
        """评估选项与价值的对齐程度"""
        option_str = json.dumps(option, ensure_ascii=False).lower()
        value_name = value.name.lower()
        
        # 简单启发式评估
        if value_name in option_str:
            return 0.9
        
        # 根据选项属性judge
        if value.name == "用户价值" and any(k in option for k in ['user', 'help', 'benefit']):
            return 0.8
        if value.name == "准确性" and any(k in option for k in ['verify', 'check', 'accurate']):
            return 0.8
        if value.name == "效率" and any(k in option for k in ['fast', 'quick', 'efficient']):
            return 0.8
        if value.name == "安全性" and any(k in option for k in ['safe', 'secure', 'backup']):
            return 0.8
        
        return 0.5  # 默认中等
    
    def make_decision(
        self,
        decision_type: DecisionType,
        options: List[Dict[str, Any]],
        context: Optional[Dict] = None
    ) -> Decision:
        """做出decision"""
        evaluated = self.evaluate_options(options)
        
        if not evaluated:
            return Decision(
                decision_id=str(datetime.now().timestamp()),
                decision_type=decision_type,
                selected_option="none",
                reasoning="无可用选项",
                confidence=0.0
            )
        
        best_option, score, reasoning = evaluated[0]
        confidence = min(1.0, score / len(self._values))
        
        decision = Decision(
            decision_id=str(datetime.now().timestamp()),
            decision_type=decision_type,
            selected_option=best_option.get('name', str(best_option)),
            reasoning=f"基于价值评估: {reasoning} (得分: {score:.2f})",
            confidence=confidence
        )
        
        self._decisions.append(decision)
        logger.info(f"decision: {decision.selected_option} (置信度: {confidence:.2f})")
        
        return decision
    
    def get_values(self) -> List[Value]:
        return self._values
    
    def update_value_weight(self, name: str, weight: float):
        for v in self._values:
            if v.name == name:
                v.weight = max(0.0, min(1.0, weight))
                self._save_data()
                return True
        return False
