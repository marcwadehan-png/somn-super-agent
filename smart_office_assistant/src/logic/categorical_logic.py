"""
__all__ = [
    'check_contradiction',
    'check_contrariety',
    'check_subalternation',
    'check_subcontrariety',
    'create_proposition',
    'evaluate_opposition',
    'get_opposition_type',
    'get_predicate_distribution',
    'get_square_of_opposition',
    'get_subject_distribution',
    'is_affirmative',
    'is_negative',
    'is_particular',
    'is_universal',
    'prop2_truth_to_str',
    'prop_truth_to_str',
    'to_symbolic',
]

直言命题逻辑引擎
Categorical Logic Engine
"""

from typing import Dict, List, Tuple, Optional
from enum import Enum

class PropositionType(Enum):
    """直言命题类型"""
    A = 'A'  # 全称肯定: All S are P
    E = 'E'  # 全称否定: No S are P
    I = 'I'  # 特称肯定: Some S are P
    O = 'O'  # 特称否定: Some S are not P

class Distribution(Enum):
    """周延性"""
    DISTRIBUTED = '周延'
    UNDISTRIBUTED = '不周延'

class CategoricalProposition:
    """直言命题"""

    def __init__(self, prop_type: PropositionType, subject: str, predicate: str):
        self.prop_type = prop_type
        self.subject = subject  # 主项 S
        self.predicate = predicate  # 谓项 P

    def __str__(self):
        """自然语言表示"""
        representations = {
            PropositionType.A: f"所有{self.subject}都是{self.predicate}",
            PropositionType.E: f"所有{self.subject}都不是{self.predicate}",
            PropositionType.I: f"有些{self.subject}是{self.predicate}",
            PropositionType.O: f"有些{self.subject}不是{self.predicate}"
        }
        return representations[self.prop_type]

    def to_symbolic(self) -> str:
        """符号化表示"""
        subject_var = 'S'
        predicate_var = 'P'
        symbolic_forms = {
            PropositionType.A: f"∀x({subject_var}(x) → {predicate_var}(x))",
            PropositionType.E: f"∀x({subject_var}(x) → ¬{predicate_var}(x))",
            PropositionType.I: f"∃x({subject_var}(x) ∧ {predicate_var}(x))",
            PropositionType.O: f"∃x({subject_var}(x) ∧ ¬{predicate_var}(x))"
        }
        return symbolic_forms[self.prop_type]

    def get_subject_distribution(self) -> Distribution:
        """get主项周延性"""
        # 全称命题(A, E)的主项周延
        # 特称命题(I, O)的主项不周延
        if self.prop_type in [PropositionType.A, PropositionType.E]:
            return Distribution.DISTRIBUTED
        else:
            return Distribution.UNDISTRIBUTED

    def get_predicate_distribution(self) -> Distribution:
        """get谓项周延性"""
        # 否定命题(E, O)的谓项周延
        # 肯定命题(A, I)的谓项不周延
        if self.prop_type in [PropositionType.E, PropositionType.O]:
            return Distribution.DISTRIBUTED
        else:
            return Distribution.UNDISTRIBUTED

    def is_universal(self) -> bool:
        """是否为全称命题"""
        return self.prop_type in [PropositionType.A, PropositionType.E]

    def is_particular(self) -> bool:
        """是否为特称命题"""
        return self.prop_type in [PropositionType.I, PropositionType.O]

    def is_affirmative(self) -> bool:
        """是否为肯定命题"""
        return self.prop_type in [PropositionType.A, PropositionType.I]

    def is_negative(self) -> bool:
        """是否为否定命题"""
        return self.prop_type in [PropositionType.E, PropositionType.O]

class CategoricalLogicEngine:
    """直言命题逻辑引擎"""

    def __init__(self):
        self.opposition_relations = {
            '矛盾': [(PropositionType.A, PropositionType.O), (PropositionType.E, PropositionType.I)],
            '反对': [(PropositionType.A, PropositionType.E)],
            '下反对': [(PropositionType.I, PropositionType.O)],
            '差等': [(PropositionType.A, PropositionType.I), (PropositionType.E, PropositionType.O)]
        }

    def create_proposition(self, prop_type: str, subject: str, predicate: str) -> CategoricalProposition:
        """
        创建直言命题

        Args:
            prop_type: 命题类型 ('A', 'E', 'I', 'O')
            subject: 主项
            predicate: 谓项

        Returns:
            直言命题对象
        """
        try:
            prop_type_enum = PropositionType(prop_type.upper())
            return CategoricalProposition(prop_type_enum, subject, predicate)
        except ValueError:
            raise ValueError(f"无效的命题类型: {prop_type}. 必须是 'A', 'E', 'I', 或 'O'")

    def check_contradiction(self, prop1: CategoricalProposition,
                           prop2: CategoricalProposition) -> bool:
        """
        检查矛盾关系 (Contradiction)
        - A ↔ O (全称肯定 ↔ 特称否定)
        - E ↔ I (全称否定 ↔ 特称肯定)
        - 两者不能同真,不能同假

        Args:
            prop1: 命题1
            prop2: 命题2

        Returns:
            是否为矛盾关系
        """
        contradictions = self.opposition_relations['矛盾']
        for (t1, t2) in contradictions:
            if (prop1.prop_type == t1 and prop2.prop_type == t2) or \
               (prop1.prop_type == t2 and prop2.prop_type == t1):
                # 还需要检查主谓项是否相同
                if prop1.subject == prop2.subject and prop1.predicate == prop2.predicate:
                    return True
        return False

    def check_contrariety(self, prop1: CategoricalProposition,
                        prop2: CategoricalProposition) -> bool:
        """
        检查反对关系 (Contrariety)
        - A ↔ E (全称肯定 ↔ 全称否定)
        - 两者不能同真,但可以同假

        Args:
            prop1: 命题1
            prop2: 命题2

        Returns:
            是否为反对关系
        """
        contraries = self.opposition_relations['反对']
        for (t1, t2) in contraries:
            if (prop1.prop_type == t1 and prop2.prop_type == t2) or \
               (prop1.prop_type == t2 and prop2.prop_type == t1):
                if prop1.subject == prop2.subject and prop1.predicate == prop2.predicate:
                    return True
        return False

    def check_subcontrariety(self, prop1: CategoricalProposition,
                           prop2: CategoricalProposition) -> bool:
        """
        检查下反对关系 (Subcontrariety)
        - I ↔ O (特称肯定 ↔ 特称否定)
        - 两者不能同假,但可以同真

        Args:
            prop1: 命题1
            prop2: 命题2

        Returns:
            是否为下反对关系
        """
        subcontraries = self.opposition_relations['下反对']
        for (t1, t2) in subcontraries:
            if (prop1.prop_type == t1 and prop2.prop_type == t2) or \
               (prop1.prop_type == t2 and prop2.prop_type == t1):
                if prop1.subject == prop2.subject and prop1.predicate == prop2.predicate:
                    return True
        return False

    def check_subalternation(self, prop1: CategoricalProposition,
                           prop2: CategoricalProposition) -> Optional[str]:
        """
        检查差等关系 (Subalternation)
        - A → I (全称肯定 → 特称肯定)
        - E → O (全称否定 → 特称否定)
        - 上真下必真,下假上必假

        Args:
            prop1: 命题1
            prop2: 命题2

        Returns:
            差等关系方向 ('prop1_implies_prop2', 'prop2_implies_prop1', None)
        """
        subalternations = self.opposition_relations['差等']

        if prop1.subject == prop2.subject and prop1.predicate == prop2.predicate:
            for (universal, particular) in subalternations:
                if prop1.prop_type == universal and prop2.prop_type == particular:
                    return 'prop1_implies_prop2'  # 全称蕴涵特称
                elif prop1.prop_type == particular and prop2.prop_type == universal:
                    return 'prop2_implies_prop1'  # 特称蕴涵全称(逆否)

        return None

    def get_opposition_type(self, prop1: CategoricalProposition,
                          prop2: CategoricalProposition) -> Optional[str]:
        """
        get两个命题的对当关系类型

        Args:
            prop1: 命题1
            prop2: 命题2

        Returns:
            对当关系类型 ('矛盾', '反对', '下反对', '差等', None)
        """
        if prop1.subject != prop2.subject or prop1.predicate != prop2.predicate:
            return None

        if self.check_contradiction(prop1, prop2):
            return '矛盾'
        elif self.check_contrariety(prop1, prop2):
            return '反对'
        elif self.check_subcontrariety(prop1, prop2):
            return '下反对'
        elif self.check_subalternation(prop1, prop2):
            return '差等'
        else:
            return None

    def evaluate_opposition(self, prop1: CategoricalProposition,
                          prop2: CategoricalProposition,
                          prop1_truth: Optional[bool] = None,
                          prop2_truth: Optional[bool] = None) -> Dict:
        """
        评估对当关系的真值关系

        Args:
            prop1: 命题1
            prop2: 命题2
            prop1_truth: 命题1的真值
            prop2_truth: 命题2的真值

        Returns:
            评估结果
        """
        relation_type = self.get_opposition_type(prop1, prop2)

        result = {
            '关系类型': relation_type,
            '命题1': str(prop1),
            '命题2': str(prop2),
            '真值关系': {},
            '结论': ''
        }

        if relation_type == '矛盾':
            result['真值关系'] = {
                '说明': '两者不能同真,不能同假',
                '关系': '一真一假'
            }
            if prop1_truth is not None:
                result['结论'] = f'因为{prop1_truth_to_str(prop1_truth)},所以{prop2_truth_to_str(not prop1_truth)}'
            elif prop2_truth is not None:
                result['结论'] = f'因为{prop2_truth_to_str(prop2_truth)},所以{prop1_truth_to_str(not prop2_truth)}'

        elif relation_type == '反对':
            result['真值关系'] = {
                '说明': '两者不能同真,但可以同假',
                '关系': '至少一假'
            }
            if prop1_truth is True:
                result['结论'] = f'因为命题1为真,所以命题2必为假'
            elif prop2_truth is True:
                result['结论'] = f'因为命题2为真,所以命题1必为假'
            elif prop1_truth is False and prop2_truth is False:
                result['结论'] = f'两者都可以为假 (一致)'

        elif relation_type == '下反对':
            result['真值关系'] = {
                '说明': '两者不能同假,但可以同真',
                '关系': '至少一真'
            }
            if prop1_truth is False:
                result['结论'] = f'因为命题1为假,所以命题2必为真'
            elif prop2_truth is False:
                result['结论'] = f'因为命题2为假,所以命题1必为真'
            elif prop1_truth is True and prop2_truth is True:
                result['结论'] = f'两者都可以为真 (一致)'

        elif relation_type == '差等':
            direction = self.check_subalternation(prop1, prop2)
            result['真值关系'] = {
                '说明': '上真下必真,下假上必假',
                '关系': direction
            }
            if direction == 'prop1_implies_prop2':
                if prop1_truth is True:
                    result['结论'] = f'因为全称命题为真,所以特称命题必为真'
                elif prop2_truth is False:
                    result['结论'] = f'因为特称命题为假,所以全称命题必为假'
            elif direction == 'prop2_implies_prop1':
                if prop2_truth is True:
                    result['结论'] = f'因为全称命题为真,所以特称命题必为真'
                elif prop1_truth is False:
                    result['结论'] = f'因为特称命题为假,所以全称命题必为假'

        return result

    def get_square_of_opposition(self, subject: str, predicate: str) -> Dict:
        """
        get对当方阵 (Square of Opposition)

        Args:
            subject: 主项
            predicate: 谓项

        Returns:
            对当方阵
        """
        A = self.create_proposition('A', subject, predicate)
        E = self.create_proposition('E', subject, predicate)
        I = self.create_proposition('I', subject, predicate)
        O = self.create_proposition('O', subject, predicate)

        return {
            '主项': subject,
            '谓项': predicate,
            '全称肯定(A)': str(A),
            '全称否定(E)': str(E),
            '特称肯定(I)': str(I),
            '特称否定(O)': str(O),
            '关系': {
                'A-O': '矛盾关系',
                'E-I': '矛盾关系',
                'A-E': '反对关系',
                'I-O': '下反对关系',
                'A-I': '差等关系 (A→I)',
                'E-O': '差等关系 (E→O)'
            }
        }

def prop_truth_to_str(truth: bool) -> str:
    """真值转字符串"""
    return '真' if truth else '假'

def prop2_truth_to_str(truth: bool) -> str:
    """真值转字符串 (别名)"""
    return prop_truth_to_str(truth)

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")

    # 创建命题
    A_prop = engine.create_proposition('A', '人', '会死的')
    E_prop = engine.create_proposition('E', '人', '会死的')
    I_prop = engine.create_proposition('I', '人', '会死的')
    O_prop = engine.create_proposition('O', '人', '会死的')

    print("=== 直言命题 ===")
    print(f"A命题: {A_prop}")
    print(f"  符号化: {A_prop.to_symbolic()}")
    print(f"  主项周延性: {A_prop.get_subject_distribution().value}")
    print(f"  谓项周延性: {A_prop.get_predicate_distribution().value}")

    print(f"\nO命题: {O_prop}")
    print(f"  符号化: {O_prop.to_symbolic()}")
    print(f"  主项周延性: {O_prop.get_subject_distribution().value}")
    print(f"  谓项周延性: {O_prop.get_predicate_distribution().value}")

    # 检查对当关系
    print("\n=== 对当关系 ===")
    print(f"A与O: {engine.get_opposition_type(A_prop, O_prop)}")
    print(f"E与I: {engine.get_opposition_type(E_prop, I_prop)}")
    print(f"A与E: {engine.get_opposition_type(A_prop, E_prop)}")
    print(f"I与O: {engine.get_opposition_type(I_prop, O_prop)}")

    # 评估对当关系
    print("\n=== 评估对当关系 ===")
    result = engine.evaluate_opposition(A_prop, O_prop, prop1_truth=True)
    print(f"A为真时的评估:")
    print(f"  {result}")

    # 对当方阵
    print("\n=== 对当方阵 ===")
    square = engine.get_square_of_opposition('人', '会死的')
    for key, value in square.items():
        if key != '关系':
            print(f"  {key}: {value}")
    print("  关系:")
    for rel, desc in square['关系'].items():
        print(f"    {rel}: {desc}")
