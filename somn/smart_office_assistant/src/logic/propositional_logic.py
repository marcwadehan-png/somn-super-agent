"""
__all__ = [
    'addition',
    'apply_associative_1',
    'apply_associative_2',
    'apply_commutative_1',
    'apply_commutative_2',
    'apply_contradiction',
    'apply_contraposition',
    'apply_demorgan_1',
    'apply_demorgan_2',
    'apply_distributive_1',
    'apply_distributive_2',
    'apply_double_negation',
    'apply_excluded_middle',
    'apply_exportation',
    'apply_idempotent_1',
    'apply_idempotent_2',
    'apply_identity_1',
    'apply_identity_2',
    'apply_implication_equiv',
    'check_entailment',
    'check_equivalence',
    'conditional_proof',
    'conjunction',
    'constructive_dilemma',
    'create_atomic_proposition',
    'create_compound_proposition',
    'destructive_dilemma',
    'disjunctive_syllogism',
    'evaluate_truth_value',
    'format_truth_table',
    'generate_truth_table',
    'hypothetical_syllogism',
    'indirect_proof',
    'is_contingent',
    'is_contradiction',
    'is_tautology',
    'modus_ponens',
    'modus_tollens',
    'natural_deduction',
    'resolution',
    'simplification',
]

命题逻辑引擎 (Propositional Logic Engine)
逻辑推理引擎

功能:
1. 复合命题的符号化 (Symbolization)
2. 真值表generate与验证 (Truth Tables)
3. 命题等价性证明 (Equivalence Proofs)
4. 演绎推理规则应用 (Deduction Rules)
5. 形式化证明generate (Formal Proofs)

作者: AI工程师
创建时间: 2026-03-31
版本: 1.0.0
"""

from typing import Dict, List, Set, Tuple, Optional
from enum import Enum
from dataclasses import dataclass
import itertools

class LogicalOperator(Enum):
    """逻辑运算符"""
    NOT = "~"           # 否定
    AND = "∧"           # 合取 (与)
    OR = "∨"           # 析取 (或)
    IMPLIES = "→"       # 蕴涵 (条件)
    IFF = "↔"          # 双向条件 (当且仅当)
    NAND = "↑"         # 舍佛竖线
    NOR = "↓"          # 皮尔斯箭头

class TruthValue(Enum):
    """真值"""
    TRUE = True
    FALSE = False
    UNKNOWN = None

@dataclass
class Proposition:
    """命题"""
    symbol: str               # 命题符号 (P, Q, R等)
    operator: Optional[LogicalOperator] = None
    operands: List['Proposition'] = None
    is_atomic: bool = True
    
    def __post_init__(self):
        if self.operands is None:
            self.operands = []
        if self.operator is not None:
            self.is_atomic = False
    
    def __str__(self) -> str:
        if self.is_atomic:
            return self.symbol
        
        if len(self.operands) == 1:
            # 一元运算符 (NOT)
            return f"{self.operator.value}{self.operands[0]}"
        elif len(self.operands) == 2:
            # 二元运算符
            return f"({self.operands[0]} {self.operator.value} {self.operands[1]})"
        else:
            return str(self.symbol)

class PropositionalLogicEngine:
    """
    命题逻辑引擎
    
    实现功能:
    1. 复合命题的符号化
    2. 真值表generate
    3. 逻辑等价性验证
    4. 演绎推理规则
    5. 自然演绎证明
    """
    
    def __init__(self):
        self.equivalence_rules = {
            # 双重否定律
            'Double Negation': lambda p: self.apply_double_negation(p),
            
            # 德摩根定律
            'De Morgan 1': lambda p: self.apply_demorgan_1(p),
            'De Morgan 2': lambda p: self.apply_demorgan_2(p),
            
            # 分配律
            'Distributive 1': lambda p: self.apply_distributive_1(p),
            'Distributive 2': lambda p: self.apply_distributive_2(p),
            
            # 结合律
            'Associative 1': lambda p: self.apply_associative_1(p),
            'Associative 2': lambda p: self.apply_associative_2(p),
            
            # 交换律
            'Commutative 1': lambda p: self.apply_commutative_1(p),
            'Commutative 2': lambda p: self.apply_commutative_2(p),
            
            # 同一律
            'Identity 1': lambda p: self.apply_identity_1(p),
            'Identity 2': lambda p: self.apply_identity_2(p),
            
            # 幂等律
            'Idempotent 1': lambda p: self.apply_idempotent_1(p),
            'Idempotent 2': lambda p: self.apply_idempotent_2(p),
            
            # 矛盾律
            'Contradiction': lambda p: self.apply_contradiction(p),
            
            # 排中律
            'Excluded Middle': lambda p: self.apply_excluded_middle(p),
            
            # 蕴涵等价
            'Implication Equivalence': lambda p: self.apply_implication_equiv(p),
            
            # 条件交换
            'Contraposition': lambda p: self.apply_contraposition(p),
            
            # 输出律
            'Exportation': lambda p: self.apply_exportation(p),
        }
        
        self.inference_rules = {
            # 演绎规则
            'Modus Ponens': self.modus_ponens,
            'Modus Tollens': self.modus_tollens,
            'Hypothetical Syllogism': self.hypothetical_syllogism,
            'Disjunctive Syllogism': self.disjunctive_syllogism,
            'Constructive Dilemma': self.constructive_dilemma,
            'Destructive Dilemma': self.destructive_dilemma,
            
            # 归纳规则
            'Simplification': self.simplification,
            'Conjunction': self.conjunction,
            'Addition': self.addition,
            'Resolution': self.resolution,
            
            # 条件证明
            'Conditional Proof': self.conditional_proof,
            'Indirect Proof': self.indirect_proof,
        }
    
    def create_atomic_proposition(self, symbol: str) -> Proposition:
        """创建原子命题"""
        return Proposition(symbol=symbol, is_atomic=True)
    
    def create_compound_proposition(self, 
                                    operator: LogicalOperator,
                                    operands: List[Proposition]) -> Proposition:
        """创建复合命题"""
        return Proposition(
            symbol="", 
            operator=operator, 
            operands=operands,
            is_atomic=False
        )
    
    def evaluate_truth_value(self, 
                            proposition: Proposition,
                            assignments: Dict[str, bool]) -> Optional[bool]:
        """
        计算命题的真值
        
        Args:
            proposition: 待计算的命题
            assignments: 原子命题的真值分配
            
        Returns:
            命题的真值 (True/False/None)
        """
        if proposition.is_atomic:
            return assignments.get(proposition.symbol, None)
        
        operator = proposition.operator
        if operator == LogicalOperator.NOT:
            return not self.evaluate_truth_value(proposition.operands[0], assignments)
        
        elif operator == LogicalOperator.AND:
            left_val = self.evaluate_truth_value(proposition.operands[0], assignments)
            right_val = self.evaluate_truth_value(proposition.operands[1], assignments)
            if left_val is None or right_val is None:
                return None
            return left_val and right_val
        
        elif operator == LogicalOperator.OR:
            left_val = self.evaluate_truth_value(proposition.operands[0], assignments)
            right_val = self.evaluate_truth_value(proposition.operands[1], assignments)
            if left_val is None or right_val is None:
                return None
            return left_val or right_val
        
        elif operator == LogicalOperator.IMPLIES:
            left_val = self.evaluate_truth_value(proposition.operands[0], assignments)
            right_val = self.evaluate_truth_value(proposition.operands[1], assignments)
            if left_val is None or right_val is None:
                return None
            return (not left_val) or right_val
        
        elif operator == LogicalOperator.IFF:
            left_val = self.evaluate_truth_value(proposition.operands[0], assignments)
            right_val = self.evaluate_truth_value(proposition.operands[1], assignments)
            if left_val is None or right_val is None:
                return None
            return left_val == right_val
        
        return None
    
    def generate_truth_table(self, proposition: Proposition) -> List[Dict[str, bool]]:
        """
        generate真值表
        
        Args:
            proposition: 待分析的命题
            
        Returns:
            真值表,每行是一个真值分配
        """
        # 收集所有原子命题
        atomic_props = self._extract_atomic_propositions(proposition)
        atomic_props = sorted(atomic_props)
        
        # generate所有可能的真值组合
        num_vars = len(atomic_props)
        combinations = list(itertools.product([False, True], repeat=num_vars))
        
        truth_table = []
        for combo in combinations:
            assignment = dict(zip(atomic_props, combo))
            truth_value = self.evaluate_truth_value(proposition, assignment)
            
            row = assignment.copy()
            row['result'] = truth_value
            truth_table.append(row)
        
        return truth_table
    
    def _extract_atomic_propositions(self, proposition: Proposition) -> Set[str]:
        """提取所有原子命题符号"""
        if proposition.is_atomic:
            return {proposition.symbol}
        
        atomic_set = set()
        for operand in proposition.operands:
            atomic_set.update(self._extract_atomic_propositions(operand))
        
        return atomic_set
    
    def is_tautology(self, proposition: Proposition) -> bool:
        """judge是否为重言式 (永真式)"""
        truth_table = self.generate_truth_table(proposition)
        return all(row['result'] for row in truth_table)
    
    def is_contradiction(self, proposition: Proposition) -> bool:
        """judge是否为矛盾式 (永假式)"""
        truth_table = self.generate_truth_table(proposition)
        return all(not row['result'] for row in truth_table)
    
    def is_contingent(self, proposition: Proposition) -> bool:
        """judge是否为偶然式 (既非永真也非永假)"""
        return not self.is_tautology(proposition) and not self.is_contradiction(proposition)
    
    def check_equivalence(self, 
                         prop1: Proposition,
                         prop2: Proposition) -> bool:
        """
        检查两个命题是否逻辑等价
        
        使用双条件命题 (P ↔ Q) 是否为重言式来judge
        """
        biconditional = self.create_compound_proposition(
            LogicalOperator.IFF,
            [prop1, prop2]
        )
        return self.is_tautology(biconditional)
    
    def check_entailment(self,
                        premises: List[Proposition],
                        conclusion: Proposition) -> bool:
        """
        检查结论是否可以从前提中逻辑推出
        
        方法: 检查 (前提1 ∧ 前提2 ∧ ... ∧ 前提n) → 结论 是否为重言式
        """
        if not premises:
            return False
        
        # 合取所有前提
        combined_premise = premises[0]
        for premise in premises[1:]:
            combined_premise = self.create_compound_proposition(
                LogicalOperator.AND,
                [combined_premise, premise]
            )
        
        # 检查蕴涵关系
        implication = self.create_compound_proposition(
            LogicalOperator.IMPLIES,
            [combined_premise, conclusion]
        )
        
        return self.is_tautology(implication)
    
    def modus_ponens(self, 
                    premise1: Proposition,
                    premise2: Proposition) -> Optional[Proposition]:
        """
        肯定前件律 (Modus Ponens)
        
        形式: P → Q, P ⊢ Q
        """
        # 检查 premise1 是否为蕴涵命题
        if (premise1.operator == LogicalOperator.IMPLIES and
            len(premise1.operands) == 2):
            
            P = premise1.operands[0]
            Q = premise1.operands[1]
            
            # 检查 premise2 是否与 P 等价
            if self.check_equivalence(premise2, P):
                return Q
        
        return None
    
    def modus_tollens(self,
                     premise1: Proposition,
                     premise2: Proposition) -> Optional[Proposition]:
        """
        否定后件律 (Modus Tollens)
        
        形式: P → Q, ~Q ⊢ ~P
        """
        if (premise1.operator == LogicalOperator.IMPLIES and
            len(premise1.operands) == 2):
            
            P = premise1.operands[0]
            Q = premise1.operands[1]
            
            # 检查 premise2 是否与 ~Q 等价
            not_Q = self.create_compound_proposition(
                LogicalOperator.NOT,
                [Q]
            )
            
            if self.check_equivalence(premise2, not_Q):
                return self.create_compound_proposition(
                    LogicalOperator.NOT,
                    [P]
                )
        
        return None
    
    def hypothetical_syllogism(self,
                             premise1: Proposition,
                             premise2: Proposition) -> Optional[Proposition]:
        """
        假言三段论 (Hypothetical Syllogism)
        
        形式: P → Q, Q → R ⊢ P → R
        """
        if (premise1.operator == LogicalOperator.IMPLIES and
            premise2.operator == LogicalOperator.IMPLIES):
            
            P = premise1.operands[0]
            Q1 = premise1.operands[1]
            Q2 = premise2.operands[0]
            R = premise2.operands[1]
            
            # 检查中间项是否相同
            if self.check_equivalence(Q1, Q2):
                return self.create_compound_proposition(
                    LogicalOperator.IMPLIES,
                    [P, R]
                )
        
        return None
    
    def disjunctive_syllogism(self,
                            premise1: Proposition,
                            premise2: Proposition) -> Optional[Proposition]:
        """
        析取三段论 (Disjunctive Syllogism)
        
        形式: P ∨ Q, ~P ⊢ Q
        """
        if (premise1.operator == LogicalOperator.OR and
            len(premise1.operands) == 2):
            
            P = premise1.operands[0]
            Q = premise1.operands[1]
            
            # 检查 premise2 是否为 ~P
            not_P = self.create_compound_proposition(
                LogicalOperator.NOT,
                [P]
            )
            
            if self.check_equivalence(premise2, not_P):
                return Q
        
        return None
    
    def constructive_dilemma(self,
                            premise1: Proposition,
                            premise2: Proposition) -> Optional[Proposition]:
        """
        构造性二难推理 (Constructive Dilemma)
        
        形式: (P → Q) ∧ (R → S), P ∨ R ⊢ Q ∨ S
        """
        # 检查 premise1 是否为合取
        if premise1.operator == LogicalOperator.AND and len(premise1.operands) == 2:
            implies1 = premise1.operands[0]
            implies2 = premise1.operands[1]
            
            if (implies1.operator == LogicalOperator.IMPLIES and
                implies2.operator == LogicalOperator.IMPLIES and
                len(implies1.operands) == 2 and
                len(implies2.operands) == 2):
                
                P = implies1.operands[0]
                Q = implies1.operands[1]
                R = implies2.operands[0]
                S = implies2.operands[1]
                
                # 检查 premise2 是否为 P ∨ R
                if (premise2.operator == LogicalOperator.OR and
                    len(premise2.operands) == 2):
                    
                    P2 = premise2.operands[0]
                    R2 = premise2.operands[1]
                    
                    if self.check_equivalence(P, P2) and self.check_equivalence(R, R2):
                        return self.create_compound_proposition(
                            LogicalOperator.OR,
                            [Q, S]
                        )
        
        return None
    
    def destructive_dilemma(self,
                           premise1: Proposition,
                           premise2: Proposition) -> Optional[Proposition]:
        """
        破坏性二难推理 (Destructive Dilemma)
        
        形式: (P → Q) ∧ (R → S), ~Q ∨ ~S ⊢ ~P ∨ ~R
        """
        if premise1.operator == LogicalOperator.AND and len(premise1.operands) == 2:
            implies1 = premise1.operands[0]
            implies2 = premise1.operands[1]
            
            if (implies1.operator == LogicalOperator.IMPLIES and
                implies2.operator == LogicalOperator.IMPLIES and
                len(implies1.operands) == 2 and
                len(implies2.operands) == 2):
                
                P = implies1.operands[0]
                Q = implies1.operands[1]
                R = implies2.operands[0]
                S = implies2.operands[1]
                
                # 检查 premise2 是否为 ~Q ∨ ~S
                if premise2.operator == LogicalOperator.OR and len(premise2.operands) == 2:
                    not_Q = self.create_compound_proposition(
                        LogicalOperator.NOT,
                        [Q]
                    )
                    not_S = self.create_compound_proposition(
                        LogicalOperator.NOT,
                        [S]
                    )
                    
                    Q2 = premise2.operands[0]
                    S2 = premise2.operands[1]
                    
                    if self.check_equivalence(Q2, not_Q) and self.check_equivalence(S2, not_S):
                        return self.create_compound_proposition(
                            LogicalOperator.OR,
                            [self.create_compound_proposition(LogicalOperator.NOT, [P]),
                             self.create_compound_proposition(LogicalOperator.NOT, [R])]
                        )
        
        return None
    
    def simplification(self, proposition: Proposition) -> Optional[Proposition]:
        """
        简化律 (Simplification)
        
        形式: P ∧ Q ⊢ P
        """
        if proposition.operator == LogicalOperator.AND and len(proposition.operands) == 2:
            return proposition.operands[0]
        return None
    
    def conjunction(self,
                   prop1: Proposition,
                   prop2: Proposition) -> Proposition:
        """
        合取律 (Conjunction)
        
        形式: P, Q ⊢ P ∧ Q
        """
        return self.create_compound_proposition(
            LogicalOperator.AND,
            [prop1, prop2]
        )
    
    def addition(self,
                proposition: Proposition,
                additional_symbol: str = "Q") -> Proposition:
        """
        添加律 (Addition)
        
        形式: P ⊢ P ∨ Q
        """
        Q = self.create_atomic_proposition(additional_symbol)
        return self.create_compound_proposition(
            LogicalOperator.OR,
            [proposition, Q]
        )
    
    def resolution(self,
                  premise1: Proposition,
                  premise2: Proposition) -> Optional[Proposition]:
        """
        消解律 (Resolution)
        
        形式: P ∨ Q, ~P ∨ R ⊢ Q ∨ R
        """
        if (premise1.operator == LogicalOperator.OR and
            premise2.operator == LogicalOperator.OR):
            
            P1 = premise1.operands[0]
            Q1 = premise1.operands[1]
            P2 = premise2.operands[0]
            R = premise2.operands[1]
            
            # 检查 P2 是否为 ~P1
            not_P1 = self.create_compound_proposition(
                LogicalOperator.NOT,
                [P1]
            )
            
            if self.check_equivalence(P2, not_P1):
                return self.create_compound_proposition(
                    LogicalOperator.OR,
                    [Q1, R]
                )
        
        return None
    
    # 逻辑等价规则实现
    def apply_double_negation(self, proposition: Proposition) -> Optional[Proposition]:
        """双重否定律: ~~P ≡ P"""
        if proposition.operator == LogicalOperator.NOT:
            operand = proposition.operands[0]
            if operand.operator == LogicalOperator.NOT:
                return operand.operands[0]
        return None
    
    def apply_demorgan_1(self, proposition: Proposition) -> Optional[Proposition]:
        """德摩根定律1: ~(P ∧ Q) ≡ ~P ∨ ~Q"""
        if (proposition.operator == LogicalOperator.NOT and
            len(proposition.operands) == 1):
            
            inner = proposition.operands[0]
            if inner.operator == LogicalOperator.AND and len(inner.operands) == 2:
                not_P = self.create_compound_proposition(LogicalOperator.NOT, [inner.operands[0]])
                not_Q = self.create_compound_proposition(LogicalOperator.NOT, [inner.operands[1]])
                return self.create_compound_proposition(LogicalOperator.OR, [not_P, not_Q])
        return None
    
    def apply_demorgan_2(self, proposition: Proposition) -> Optional[Proposition]:
        """德摩根定律2: ~(P ∨ Q) ≡ ~P ∧ ~Q"""
        if (proposition.operator == LogicalOperator.NOT and
            len(proposition.operands) == 1):
            
            inner = proposition.operands[0]
            if inner.operator == LogicalOperator.OR and len(inner.operands) == 2:
                not_P = self.create_compound_proposition(LogicalOperator.NOT, [inner.operands[0]])
                not_Q = self.create_compound_proposition(LogicalOperator.NOT, [inner.operands[1]])
                return self.create_compound_proposition(LogicalOperator.AND, [not_P, not_Q])
        return None
    
    # ... 其他等价规则的简化实现
    def apply_distributive_1(self, proposition: Proposition) -> Optional[Proposition]:
        """分配律1: P ∧ (Q ∨ R) ≡ (P ∧ Q) ∨ (P ∧ R)"""
        if (proposition.operator == LogicalOperator.AND and
            len(proposition.operands) == 2):
            P = proposition.operands[0]
            QR = proposition.operands[1]
            if QR.operator == LogicalOperator.OR and len(QR.operands) == 2:
                Q = QR.operands[0]
                R = QR.operands[1]
                PQ = self.create_compound_proposition(LogicalOperator.AND, [P, Q])
                PR = self.create_compound_proposition(LogicalOperator.AND, [P, R])
                return self.create_compound_proposition(LogicalOperator.OR, [PQ, PR])
        return None
    
    def apply_distributive_2(self, proposition: Proposition) -> Optional[Proposition]:
        """分配律2: P ∨ (Q ∧ R) ≡ (P ∨ Q) ∧ (P ∨ R)"""
        if (proposition.operator == LogicalOperator.OR and
            len(proposition.operands) == 2):
            P = proposition.operands[0]
            QR = proposition.operands[1]
            if QR.operator == LogicalOperator.AND and len(QR.operands) == 2:
                Q = QR.operands[0]
                R = QR.operands[1]
                PQ = self.create_compound_proposition(LogicalOperator.OR, [P, Q])
                PR = self.create_compound_proposition(LogicalOperator.OR, [P, R])
                return self.create_compound_proposition(LogicalOperator.AND, [PQ, PR])
        return None
    
    def apply_associative_1(self, proposition: Proposition) -> Optional[Proposition]:
        """结合律1: (P ∧ Q) ∧ R ≡ P ∧ (Q ∧ R)"""
        if (proposition.operator == LogicalOperator.AND and
            len(proposition.operands) == 2):
            PQ = proposition.operands[0]
            R = proposition.operands[1]
            if PQ.operator == LogicalOperator.AND and len(PQ.operands) == 2:
                P = PQ.operands[0]
                Q = PQ.operands[1]
                QR = self.create_compound_proposition(LogicalOperator.AND, [Q, R])
                return self.create_compound_proposition(LogicalOperator.AND, [P, QR])
        return None
    
    def apply_associative_2(self, proposition: Proposition) -> Optional[Proposition]:
        """结合律2: (P ∨ Q) ∨ R ≡ P ∨ (Q ∨ R)"""
        if (proposition.operator == LogicalOperator.OR and
            len(proposition.operands) == 2):
            PQ = proposition.operands[0]
            R = proposition.operands[1]
            if PQ.operator == LogicalOperator.OR and len(PQ.operands) == 2:
                P = PQ.operands[0]
                Q = PQ.operands[1]
                QR = self.create_compound_proposition(LogicalOperator.OR, [Q, R])
                return self.create_compound_proposition(LogicalOperator.OR, [P, QR])
        return None
    
    def apply_commutative_1(self, proposition: Proposition) -> Optional[Proposition]:
        """交换律1: P ∧ Q ≡ Q ∧ P"""
        if (proposition.operator == LogicalOperator.AND and
            len(proposition.operands) == 2):
            return self.create_compound_proposition(
                LogicalOperator.AND,
                [proposition.operands[1], proposition.operands[0]]
            )
        return None
    
    def apply_commutative_2(self, proposition: Proposition) -> Optional[Proposition]:
        """交换律2: P ∨ Q ≡ Q ∨ P"""
        if (proposition.operator == LogicalOperator.OR and
            len(proposition.operands) == 2):
            return self.create_compound_proposition(
                LogicalOperator.OR,
                [proposition.operands[1], proposition.operands[0]]
            )
        return None
    
    def apply_identity_1(self, proposition: Proposition) -> Optional[Proposition]:
        """同一律1: P ∧ T ≡ P"""
        if (proposition.operator == LogicalOperator.AND and
            len(proposition.operands) == 2):
            # 这里简化处理,实际应该检查操作数是否为重言式
            return proposition.operands[0] if self.is_tautology(proposition.operands[1]) else None
        return None
    
    def apply_identity_2(self, proposition: Proposition) -> Optional[Proposition]:
        """同一律2: P ∨ F ≡ P"""
        if (proposition.operator == LogicalOperator.OR and
            len(proposition.operands) == 2):
            # 这里简化处理,实际应该检查操作数是否为矛盾式
            return proposition.operands[0] if self.is_contradiction(proposition.operands[1]) else None
        return None
    
    def apply_idempotent_1(self, proposition: Proposition) -> Optional[Proposition]:
        """幂等律1: P ∧ P ≡ P"""
        if (proposition.operator == LogicalOperator.AND and
            len(proposition.operands) == 2 and
            self.check_equivalence(proposition.operands[0], proposition.operands[1])):
            return proposition.operands[0]
        return None
    
    def apply_idempotent_2(self, proposition: Proposition) -> Optional[Proposition]:
        """幂等律2: P ∨ P ≡ P"""
        if (proposition.operator == LogicalOperator.OR and
            len(proposition.operands) == 2 and
            self.check_equivalence(proposition.operands[0], proposition.operands[1])):
            return proposition.operands[0]
        return None
    
    def apply_contradiction(self, proposition: Proposition) -> Optional[Proposition]:
        """矛盾律: P ∧ ~P ≡ F"""
        if (proposition.operator == LogicalOperator.AND and
            len(proposition.operands) == 2):
            P = proposition.operands[0]
            not_P = self.create_compound_proposition(LogicalOperator.NOT, [P])
            if self.check_equivalence(proposition.operands[1], not_P):
                # 返回矛盾式
                return self.create_compound_proposition(
                    LogicalOperator.AND,
                    [P, not_P]
                )
        return None
    
    def apply_excluded_middle(self, proposition: Proposition) -> Optional[Proposition]:
        """排中律: P ∨ ~P ≡ T"""
        P = proposition.operands[0] if proposition.operator == LogicalOperator.NOT else proposition
        not_P = self.create_compound_proposition(LogicalOperator.NOT, [P])
        return self.create_compound_proposition(LogicalOperator.OR, [P, not_P])
    
    def apply_implication_equiv(self, proposition: Proposition) -> Optional[Proposition]:
        """蕴涵等价: P → Q ≡ ~P ∨ Q"""
        if proposition.operator == LogicalOperator.IMPLIES and len(proposition.operands) == 2:
            P = proposition.operands[0]
            Q = proposition.operands[1]
            not_P = self.create_compound_proposition(LogicalOperator.NOT, [P])
            return self.create_compound_proposition(LogicalOperator.OR, [not_P, Q])
        return None
    
    def apply_contraposition(self, proposition: Proposition) -> Optional[Proposition]:
        """条件交换: P → Q ≡ ~Q → ~P"""
        if proposition.operator == LogicalOperator.IMPLIES and len(proposition.operands) == 2:
            P = proposition.operands[0]
            Q = proposition.operands[1]
            not_Q = self.create_compound_proposition(LogicalOperator.NOT, [Q])
            not_P = self.create_compound_proposition(LogicalOperator.NOT, [P])
            return self.create_compound_proposition(LogicalOperator.IMPLIES, [not_Q, not_P])
        return None
    
    def apply_exportation(self, proposition: Proposition) -> Optional[Proposition]:
        """输出律: (P ∧ Q) → R ≡ P → (Q → R)"""
        if (proposition.operator == LogicalOperator.IMPLIES and
            len(proposition.operands) == 2):
            left = proposition.operands[0]
            right = proposition.operands[1]
            
            if (left.operator == LogicalOperator.AND and
                len(left.operands) == 2):
                P = left.operands[0]
                Q = left.operands[1]
                Q_implies_R = self.create_compound_proposition(
                    LogicalOperator.IMPLIES,
                    [Q, right]
                )
                return self.create_compound_proposition(
                    LogicalOperator.IMPLIES,
                    [P, Q_implies_R]
                )
        return None
    
    def conditional_proof(self,
                         assumption: Proposition,
                         conclusion: Proposition) -> Optional[Proposition]:
        """
        条件证明 (Conditional Proof)
        
        形式: 如果在假设P下能推出Q,则P → Q有效
        """
        return self.create_compound_proposition(
            LogicalOperator.IMPLIES,
            [assumption, conclusion]
        )
    
    def indirect_proof(self,
                      assumption: Proposition) -> Optional[Proposition]:
        """
        间接证明 / 归谬法 (Indirect Proof / Reductio ad Absurdum)
        
        形式: 如果从假设P推出矛盾,则~P有效
        """
        not_P = self.create_compound_proposition(
            LogicalOperator.NOT,
            [assumption]
        )
        return not_P
    
    def natural_deduction(self,
                          premises: List[Proposition],
                          conclusion: Proposition) -> Tuple[bool, List[str]]:
        """
        自然演绎证明
        
        Args:
            premises: 前提列表
            conclusion: 要证明的结论
            
        Returns:
            (是否成功, 证明步骤列表)
        """
        # 简化实现: 使用真值表检查
        steps = []
        
        # 步骤1: 验证结论是否可从前提推出
        is_valid = self.check_entailment(premises, conclusion)
        
        if is_valid:
            steps.append("证明开始")
            steps.append(f"前提: {[str(p) for p in premises]}")
            steps.append(f"待证结论: {conclusion}")
            
            # 尝试应用推理规则
            if len(premises) == 2:
                result = self.modus_ponens(premises[0], premises[1])
                if result and self.check_equivalence(result, conclusion):
                    steps.append("应用肯定前件律 (Modus Ponens)")
                    steps.append("证明成功 ✓")
                else:
                    result = self.modus_tollens(premises[0], premises[1])
                    if result and self.check_equivalence(result, conclusion):
                        steps.append("应用否定后件律 (Modus Tollens)")
                        steps.append("证明成功 ✓")
                    else:
                        steps.append("通过真值表验证有效性")
                        steps.append("证明成功 ✓")
            else:
                steps.append("通过真值表验证有效性")
                steps.append("证明成功 ✓")
        else:
            steps.append("证明失败: 结论不能从前提推出")
        
        return is_valid, steps
    
    def format_truth_table(self, proposition: Proposition) -> str:
        """格式化输出真值表"""
        truth_table = self.generate_truth_table(proposition)
        atomic_props = self._extract_atomic_propositions(proposition)
        atomic_props = sorted(atomic_props)
        
        output = []
        # 表头
        header = " | ".join(atomic_props) + " | " + str(proposition)
        output.append(header)
        output.append("-" * len(header))
        
        # 每一行
        for row in truth_table:
            values = []
            for prop in atomic_props:
                values.append("T" if row[prop] else "F")
            values.append("T" if row['result'] else "F")
            output.append(" | ".join(values))
        
        return "\n".join(output)

# 使用示例
# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
