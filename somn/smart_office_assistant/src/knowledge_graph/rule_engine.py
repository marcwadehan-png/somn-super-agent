"""
__all__ = [
    'add_rule',
    'evaluate',
    'execute_rules',
    'find_applicable_rules',
    'get_rule_statistics',
    'to_dict',
]

规则引擎 - 管理三层知识架构的规则层
支持演绎,归纳,启发,因果四种规则类型
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import re

class RuleType(Enum):
    """规则类型"""
    DEDUCTIVE = "deductive"       # 演绎规则: 一般 → 特殊
    INDUCTIVE = "inductive"       # 归纳规则: 特殊 → 一般
    HEURISTIC = "heuristic"       # 启发规则: 经验法则
    CAUSAL = "causal"             # 因果规则: 原因 → 结果

class RulePriority(Enum):
    """规则优先级"""
    CRITICAL = 1      # 关键
    HIGH = 2          # 高
    MEDIUM = 3        # 中
    LOW = 4           # 低

@dataclass
class RuleCondition:
    """规则条件"""
    field: str                    # 字段名
    operator: str                 # 操作符: eq, ne, gt, lt, gte, lte, contains, regex
    value: Any                    # 比较值
    
    def evaluate(self, data: Dict) -> bool:
        """评估条件"""
        actual_value = data.get(self.field)
        
        if self.operator == 'eq':
            return actual_value == self.value
        elif self.operator == 'ne':
            return actual_value != self.value
        elif self.operator == 'gt':
            return actual_value is not None and actual_value > self.value
        elif self.operator == 'lt':
            return actual_value is not None and actual_value < self.value
        elif self.operator == 'gte':
            return actual_value is not None and actual_value >= self.value
        elif self.operator == 'lte':
            return actual_value is not None and actual_value <= self.value
        elif self.operator == 'contains':
            return self.value in str(actual_value) if actual_value else False
        elif self.operator == 'regex':
            return bool(re.search(self.value, str(actual_value))) if actual_value else False
        elif self.operator == 'in':
            return actual_value in self.value if isinstance(self.value, list) else False
        elif self.operator == 'exists':
            return self.field in data
        
        return False

@dataclass
class RuleAction:
    """规则动作"""
    action_type: str              # 动作类型: set, add, remove, recommend, alert
    target: str                   # 目标字段或对象
    value: Any = None             # 动作值
    parameters: Dict = field(default_factory=dict)  # 附加参数

@dataclass
class Rule:
    """规则定义"""
    rule_id: str
    name: str
    rule_type: RuleType
    description: str = ""
    conditions: List[RuleCondition] = field(default_factory=list)
    actions: List[RuleAction] = field(default_factory=list)
    priority: RulePriority = RulePriority.MEDIUM
    confidence: float = 1.0       # 规则置信度
    source: str = "manual"        # 来源
    applicable_industries: List[str] = field(default_factory=list)
    applicable_stages: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    execution_count: int = 0
    success_count: int = 0
    
    def to_dict(self) -> Dict:
        return {
            'rule_id': self.rule_id,
            'name': self.name,
            'rule_type': self.rule_type.value,
            'description': self.description,
            'conditions': [{'field': c.field, 'operator': c.operator, 'value': c.value} 
                          for c in self.conditions],
            'actions': [{'action_type': a.action_type, 'target': a.target, 
                        'value': a.value, 'parameters': a.parameters} 
                       for a in self.actions],
            'priority': self.priority.value,
            'confidence': self.confidence,
            'source': self.source,
            'applicable_industries': self.applicable_industries,
            'applicable_stages': self.applicable_stages,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'execution_count': self.execution_count,
            'success_count': self.success_count
        }

@dataclass
class RuleExecutionResult:
    """规则执行结果"""
    rule_id: str
    triggered: bool
    matched_conditions: List[str] = field(default_factory=list)
    actions_taken: List[Dict] = field(default_factory=list)
    output: Dict = field(default_factory=dict)
    confidence: float = 0.0
    execution_time_ms: int = 0

class RuleEngine:
    """规则引擎"""
    
    def __init__(self, graph_engine=None):
        self.graph_engine = graph_engine
        self.rules: Dict[str, Rule] = {}
        self.rule_index_by_type: Dict[RuleType, List[str]] = {t: [] for t in RuleType}
        self.rule_index_by_industry: Dict[str, List[str]] = {}
        
        # init核心规则
        self._init_core_rules()
    
    def _init_core_rules(self):
        """init核心增长规则"""
        core_rules = [
            # 演绎规则
            {
                'rule_id': 'deductive_high_churn_alert',
                'name': '高流失率预警',
                'rule_type': RuleType.DEDUCTIVE,
                'description': '当月流失率超过阈值时触发预警',
                'conditions': [
                    RuleCondition('churn_rate', 'gt', 0.05),
                    RuleCondition('data_freshness_days', 'lte', 7)
                ],
                'actions': [
                    RuleAction('alert', 'growth_team', None, {'level': 'high', 'message': '流失率异常升高'}),
                    RuleAction('recommend', 'intervention', ['用户访谈', '流失分析', '挽回活动'])
                ],
                'priority': RulePriority.CRITICAL,
                'applicable_industries': ['saas', 'subscription'],
                'confidence': 0.95
            },
            {
                'rule_id': 'deductive_low_conversion_alert',
                'name': '低转化率诊断',
                'rule_type': RuleType.DEDUCTIVE,
                'description': '当转化率低于行业基准时触发优化建议',
                'conditions': [
                    RuleCondition('conversion_rate', 'lt', 0.01),
                    RuleCondition('traffic_volume', 'gt', 1000)
                ],
                'actions': [
                    RuleAction('recommend', 'optimization', ['漏斗分析', '落地页优化', 'A/B测试']),
                    RuleAction('set', 'priority', 'high')
                ],
                'priority': RulePriority.HIGH,
                'applicable_industries': ['ecommerce', 'saas'],
                'confidence': 0.90
            },
            
            # 归纳规则
            {
                'rule_id': 'inductive_high_value_user_pattern',
                'name': '高价值用户characteristics归纳',
                'rule_type': RuleType.INDUCTIVE,
                'description': '从多个高价值用户案例中归纳共同characteristics',
                'conditions': [
                    RuleCondition('user_cases_count', 'gte', 10),
                    RuleCondition('avg_ltv', 'gt', 1000)
                ],
                'actions': [
                    RuleAction('extract', 'pattern', 'high_value_user_profile'),
                    RuleAction('recommend', 'targeting', 'lookalike_audience')
                ],
                'priority': RulePriority.HIGH,
                'confidence': 0.80
            },
            {
                'rule_id': 'inductive_viral_content_pattern',
                'name': '病毒内容模式归纳',
                'rule_type': RuleType.INDUCTIVE,
                'description': '从爆款内容中归纳传播规律',
                'conditions': [
                    RuleCondition('viral_content_count', 'gte', 5),
                    RuleCondition('share_rate', 'gt', 0.10)
                ],
                'actions': [
                    RuleAction('extract', 'content_pattern', 'viral_formula'),
                    RuleAction('recommend', 'content_strategy', 'replicate_pattern')
                ],
                'priority': RulePriority.MEDIUM,
                'applicable_industries': ['content', 'social'],
                'confidence': 0.75
            },
            
            # 启发规则
            {
                'rule_id': 'heuristic_seasonal_prep',
                'name': '大促提前准备',
                'rule_type': RuleType.HEURISTIC,
                'description': '根据历史经验,大促前需要提前准备',
                'conditions': [
                    RuleCondition('days_to_promotion', 'lte', 30),
                    RuleCondition('promotion_type', 'in', ['618', '双11', '双12'])
                ],
                'actions': [
                    RuleAction('recommend', 'preparation', ['库存准备', '流量预估', '客服扩容']),
                    RuleAction('set', 'alert_date', 'promotion_start')
                ],
                'priority': RulePriority.HIGH,
                'applicable_industries': ['ecommerce'],
                'confidence': 0.85
            },
            {
                'rule_id': 'heuristic_new_user_onboarding',
                'name': '新用户引导优化',
                'rule_type': RuleType.HEURISTIC,
                'description': '新用户首周体验决定长期留存',
                'conditions': [
                    RuleCondition('user_tenure_days', 'lte', 7),
                    RuleCondition('activation_events', 'lt', 3)
                ],
                'actions': [
                    RuleAction('recommend', 'intervention', ['个性化引导', '功能推荐', '客服触达']),
                    RuleAction('set', 'priority', 'high')
                ],
                'priority': RulePriority.HIGH,
                'confidence': 0.88
            },
            
            # 因果规则
            {
                'rule_id': 'causal_price_promotion_impact',
                'name': '促销价格影响分析',
                'rule_type': RuleType.CAUSAL,
                'description': '降价促销通常会导致销量上升但利润率下降',
                'conditions': [
                    RuleCondition('price_discount', 'gt', 0.20),
                    RuleCondition('promotion_active', 'eq', True)
                ],
                'actions': [
                    RuleAction('predict', 'sales_volume', 'increase_30_50_percent'),
                    RuleAction('predict', 'profit_margin', 'decrease_10_20_percent'),
                    RuleAction('recommend', 'monitor', ['库存周转', '利润贡献'])
                ],
                'priority': RulePriority.MEDIUM,
                'applicable_industries': ['ecommerce', 'retail'],
                'confidence': 0.82
            },
            {
                'rule_id': 'causal_content_frequency_engagement',
                'name': '内容频次与参与度关系',
                'rule_type': RuleType.CAUSAL,
                'description': '发布频次与粉丝互动存在倒U型关系',
                'conditions': [
                    RuleCondition('content_frequency_daily', 'gt', 5),
                    RuleCondition('engagement_rate_trend', 'eq', 'declining')
                ],
                'actions': [
                    RuleAction('recommend', 'frequency_adjustment', 'reduce_to_3_per_day'),
                    RuleAction('recommend', 'focus', 'quality_over_quantity')
                ],
                'priority': RulePriority.MEDIUM,
                'applicable_industries': ['content', 'social'],
                'confidence': 0.78
            }
        ]
        
        for rule_data in core_rules:
            self.add_rule(Rule(**rule_data))
    
    def add_rule(self, rule: Rule) -> Rule:
        """添加规则"""
        self.rules[rule.rule_id] = rule
        
        # 更新索引
        self.rule_index_by_type[rule.rule_type].append(rule.rule_id)
        
        for industry in rule.applicable_industries:
            if industry not in self.rule_index_by_industry:
                self.rule_index_by_industry[industry] = []
            self.rule_index_by_industry[industry].append(rule.rule_id)
        
        return rule
    
    def execute_rules(self, data: Dict, rule_type: RuleType = None,
                     industry: str = None, stage: str = None) -> List[RuleExecutionResult]:
        """执行规则"""
        results = []
        
        # 确定要执行的规则
        candidate_rules = set(self.rules.keys())
        
        if rule_type:
            candidate_rules &= set(self.rule_index_by_type.get(rule_type, []))
        
        if industry:
            industry_rules = set(self.rule_index_by_industry.get(industry, []))
            # 如果没有行业特定规则,使用通用规则
            if industry_rules:
                candidate_rules &= industry_rules
        
        # 按优先级排序
        sorted_rules = sorted(
            [self.rules[r] for r in candidate_rules],
            key=lambda r: r.priority.value
        )
        
        # 执行规则
        for rule in sorted_rules:
            result = self._execute_single_rule(rule, data)
            results.append(result)
            
            # 更新规则统计
            rule.execution_count += 1
            if result.triggered:
                rule.success_count += 1
        
        return results
    
    def _execute_single_rule(self, rule: Rule, data: Dict) -> RuleExecutionResult:
        """执行单条规则"""
        import time
        start_time = time.time()
        
        # 评估所有条件
        matched_conditions = []
        all_conditions_met = True
        
        for condition in rule.conditions:
            if condition.evaluate(data):
                matched_conditions.append(f"{condition.field} {condition.operator} {condition.value}")
            else:
                all_conditions_met = False
                break
        
        # 构建结果
        result = RuleExecutionResult(
            rule_id=rule.rule_id,
            triggered=all_conditions_met,
            matched_conditions=matched_conditions,
            execution_time_ms=int((time.time() - start_time) * 1000),
            confidence=rule.confidence if all_conditions_met else 0.0
        )
        
        # 如果触发,执action作
        if all_conditions_met:
            for action in rule.actions:
                action_result = {
                    'action_type': action.action_type,
                    'target': action.target,
                    'value': action.value,
                    'parameters': action.parameters
                }
                result.actions_taken.append(action_result)
                
                # 更新输出
                if action.action_type == 'set':
                    result.output[action.target] = action.value
                elif action.action_type == 'add':
                    if action.target not in result.output:
                        result.output[action.target] = []
                    result.output[action.target].append(action.value)
                elif action.action_type == 'recommend':
                    if 'recommendations' not in result.output:
                        result.output['recommendations'] = []
                    result.output['recommendations'].append({
                        'category': action.target,
                        'items': action.value if isinstance(action.value, list) else [action.value]
                    })
        
        return result
    
    def get_rule_statistics(self) -> Dict[str, Any]:
        """get规则统计"""
        stats = {
            'total_rules': len(self.rules),
            'by_type': {t.value: len(rules) for t, rules in self.rule_index_by_type.items()},
            'by_priority': {},
            'execution_summary': {
                'total_executions': sum(r.execution_count for r in self.rules.values()),
                'total_triggers': sum(r.success_count for r in self.rules.values()),
            }
        }
        
        # 按优先级统计
        priority_counts = {}
        for rule in self.rules.values():
            p = rule.priority.name
            priority_counts[p] = priority_counts.get(p, 0) + 1
        stats['by_priority'] = priority_counts
        
        # 计算触发率
        total_exec = stats['execution_summary']['total_executions']
        total_trig = stats['execution_summary']['total_triggers']
        stats['execution_summary']['trigger_rate'] = total_trig / total_exec if total_exec > 0 else 0
        
        return stats
    
    def find_applicable_rules(self, context: Dict) -> List[Rule]:
        """根据上下文查找适用规则"""
        applicable = []
        
        industry = context.get('industry')
        stage = context.get('stage')
        
        for rule in self.rules.values():
            # 检查行业匹配
            if rule.applicable_industries and industry:
                if industry not in rule.applicable_industries:
                    continue
            
            # 检查阶段匹配
            if rule.applicable_stages and stage:
                if stage not in rule.applicable_stages:
                    continue
            
            applicable.append(rule)
        
        # 按优先级排序
        return sorted(applicable, key=lambda r: r.priority.value)
