"""
__all__ = [
    'get_all_valid_syllogisms',
    'get_figure',
    'get_mood',
    'get_valid_syllogisms_by_figure',
    'validate',
    'validate_by_mood_and_figure',
]

三段论验证器
Syllogism Validator
实现三段论有效性验证 (5+3规则)
"""

from typing import Dict, List, Tuple, Optional
from enum import Enum

from .categorical_logic import CategoricalLogicEngine, CategoricalProposition, PropositionType

class Figure(Enum):
    """三段论格 (基于中项在前提中的位置)

    格的定义:
    - 第1格: MP / SM → SP (中项在大前提主项,小前提谓项)
    - 第2格: PM / SM → SP (中项在两个前提谓项)
    - 第3格: MP / MS → SP (中项在两个前提主项)
    - 第4格: PM / MS → SP (中项在大前提谓项,小前提主项)
    """
    FIGURE_1 = '第1格'
    FIGURE_2 = '第2格'
    FIGURE_3 = '第3格'
    FIGURE_4 = '第4格'

class Syllogism:
    """三段论"""

    def __init__(self, major_premise: CategoricalProposition,
                 minor_premise: CategoricalProposition,
                 conclusion: CategoricalProposition):
        self.major_premise = major_premise
        self.minor_premise = minor_premise
        self.conclusion = conclusion

        # recognize三个项
        self.major_term = conclusion.predicate  # 大项 P
        self.minor_term = conclusion.subject  # 小项 S
        self.middle_term = self._identify_middle_term()  # 中项 M

    def _identify_middle_term(self) -> str:
        """recognize中项 (中项是前提中出现但结论中不出现的项)"""
        major_terms = {self.major_premise.subject, self.major_premise.predicate}
        minor_terms = {self.minor_premise.subject, self.minor_premise.predicate}
        conclusion_terms = {self.conclusion.subject, self.conclusion.predicate}

        # 中项 = 前提中的项 - 结论中的项
        middle_terms = (major_terms | minor_terms) - conclusion_terms

        if len(middle_terms) != 1:
            raise ValueError(f"无法recognize中项.期望1个,找到{len(middle_terms)}个: {middle_terms}")

        return middle_terms.pop()

    def get_mood(self) -> str:
        """get三段论式 (Mood: 大前提-小前提-结论的命题类型序列)"""
        mood = (self.major_premise.prop_type.value +
                self.minor_premise.prop_type.value +
                self.conclusion.prop_type.value)
        return mood

    def get_figure(self) -> Figure:
        """get三段论格 (Figure: 基于中项在前提中的位置)"""
        # 大前提中中项的位置
        if self.major_premise.subject == self.middle_term:
            major_position = 'subject'
        elif self.major_premise.predicate == self.middle_term:
            major_position = 'predicate'
        else:
            raise ValueError("中项不在大前提中")

        # 小前提中中项的位置
        if self.minor_premise.subject == self.middle_term:
            minor_position = 'subject'
        elif self.minor_premise.predicate == self.middle_term:
            minor_position = 'predicate'
        else:
            raise ValueError("中项不在小前提中")

        # 确定格
        if major_position == 'subject' and minor_position == 'predicate':
            return Figure.FIGURE_1
        elif major_position == 'predicate' and minor_position == 'predicate':
            return Figure.FIGURE_2
        elif major_position == 'subject' and minor_position == 'subject':
            return Figure.FIGURE_3
        elif major_position == 'predicate' and minor_position == 'subject':
            return Figure.FIGURE_4
        else:
            raise ValueError(f"无法确定格: major={major_position}, minor={minor_position}")

    def __str__(self):
        """自然语言表示"""
        return (f"大前提: {self.major_premise}\n"
                f"小前提: {self.minor_premise}\n"
                f"结论: {self.conclusion}")

class SyllogismValidator:
    """三段论验证器 - 实现有效性检查"""

    def __init__(self):
        self.logic_engine = CategoricalLogicEngine()

        # 有效三段论库 (共244个有效式)
        # 格式: {格: {式: True}}
        self.valid_syllogisms = {
            Figure.FIGURE_1: {
                'AAA', 'EAE', 'AII', 'EIO',  # 基本有效式
                'AAI', 'EAO'  # 弱式
            },
            Figure.FIGURE_2: {
                'EAE', 'AEE', 'EIO', 'AOO',
                'EAO', 'AEO'
            },
            Figure.FIGURE_3: {
                'IAI', 'AII', 'OAO', 'EIO',
                'AAI', 'EAO'
            },
            Figure.FIGURE_4: {
                'AEE', 'IAI', 'EIO',
                'AEO', 'EAO'
            }
        }

        # 三段论5规则 (规则集1: 基于周延性)
        self.distribution_rules = {
            '中项规则': '中项至少周延一次',
            '大项规则': '结论中周延的项,前提中必须周延',
            '小项规则': '结论中周延的项,前提中必须周延'
        }

        # 三段论3规则 (规则集2: 基于命题类型)
        self.quality_rules = {
            '否定规则': '两个否定前提推不出有效结论',
            '特称规则': '两个特称前提推不出有效结论',
            '结论规则': '如果前提中有否定,结论必须否定;如果结论否定,前提中必须有一个否定'
        }

    def validate(self, major_premise: CategoricalProposition,
                 minor_premise: CategoricalProposition,
                 conclusion: CategoricalProposition) -> Dict:
        """
        验证三段论有效性

        Args:
            major_premise: 大前提
            minor_premise: 小前提
            conclusion: 结论

        Returns:
            验证结果
        """
        syllogism = Syllogism(major_premise, minor_premise, conclusion)

        # get格和式
        mood = syllogism.get_mood()
        figure = syllogism.get_figure()

        # 方法1: 检查是否在有效三段论库中
        is_valid_by_library = self._check_valid_by_library(mood, figure)

        # 方法2: 检查周延性规则
        distribution_violations = self._check_distribution_rules(syllogism)

        # 方法3: 检查质和量规则
        quality_violations = self._check_quality_rules(syllogism)

        # synthesizejudge
        all_violations = distribution_violations + quality_violations
        is_valid = len(all_violations) == 0

        # 构建结果
        result = {
            '是否有效': is_valid,
            '三段论': str(syllogism),
            '格': figure.value,
            '式': mood,
            '中项': syllogism.middle_term,
            '大项': syllogism.major_term,
            '小项': syllogism.minor_term,
            '周延性检查': {
                '违规': distribution_violations,
                '通过': len(distribution_violations) == 0
            },
            '质和量检查': {
                '违规': quality_violations,
                '通过': len(quality_violations) == 0
            },
            '有效库检查': {
                '在有效库中': is_valid_by_library,
                '一致性': is_valid == is_valid_by_library
            },
            '说明': self._generate_explanation(syllogism, all_violations)
        }

        return result

    def _check_valid_by_library(self, mood: str, figure: Figure) -> bool:
        """通过有效三段论库检查"""
        valid_moods = self.valid_syllogisms.get(figure, set())
        return mood in valid_moods

    def _check_distribution_rules(self, syllogism: Syllogism) -> List[str]:
        """检查周延性规则 (5规则中的3条)"""
        violations = []

        major = syllogism.major_premise
        minor = syllogism.minor_premise
        conclusion = syllogism.conclusion
        middle_term = syllogism.middle_term
        major_term = syllogism.major_term
        minor_term = syllogism.minor_term

        # 规则1: 中项规则 - 中项至少周延一次
        middle_distributed = False
        if major.subject == middle_term and major.get_subject_distribution().value == '周延':
            middle_distributed = True
        elif major.predicate == middle_term and major.get_predicate_distribution().value == '周延':
            middle_distributed = True
        elif minor.subject == middle_term and minor.get_subject_distribution().value == '周延':
            middle_distributed = True
        elif minor.predicate == middle_term and minor.get_predicate_distribution().value == '周延':
            middle_distributed = True

        if not middle_distributed:
            violations.append(f"违反中项规则: 中项'{middle_term}'至少应周延一次")

        # 规则2: 大项规则 - 结论中周延的大项,前提中必须周延
        major_term_in_conclusion_distributed = (conclusion.get_predicate_distribution().value == '周延')

        if major_term_in_conclusion_distributed:
            major_term_in_premises_distributed = False
            if major.subject == major_term and major.get_subject_distribution().value == '周延':
                major_term_in_premises_distributed = True
            elif major.predicate == major_term and major.get_predicate_distribution().value == '周延':
                major_term_in_premises_distributed = True

            if not major_term_in_premises_distributed:
                violations.append(f"违反大项规则: 大项'{major_term}'在结论中周延,但在前提中不周延")

        # 规则3: 小项规则 - 结论中周延的小项,前提中必须周延
        minor_term_in_conclusion_distributed = (conclusion.get_subject_distribution().value == '周延')

        if minor_term_in_conclusion_distributed:
            minor_term_in_premises_distributed = False
            if minor.subject == minor_term and minor.get_subject_distribution().value == '周延':
                minor_term_in_premises_distributed = True
            elif minor.predicate == minor_term and minor.get_predicate_distribution().value == '周延':
                minor_term_in_premises_distributed = True

            if not minor_term_in_premises_distributed:
                violations.append(f"违反小项规则: 小项'{minor_term}'在结论中周延,但在前提中不周延")

        return violations

    def _check_quality_rules(self, syllogism: Syllogism) -> List[str]:
        """检查质和量规则 (5规则中的另外2条)"""
        violations = []

        major = syllogism.major_premise
        minor = syllogism.minor_premise
        conclusion = syllogism.conclusion

        # 规则4: 否定规则 - 两个否定前提推不出有效结论
        if major.is_negative() and minor.is_negative():
            violations.append("违反否定规则: 两个否定前提推不出有效结论")

        # 规则5: 特称规则 - 两个特称前提推不出有效结论
        if major.is_particular() and minor.is_particular():
            violations.append("违反特称规则: 两个特称前提推不出有效结论")

        # 额外规则: 结论规则
        # 如果前提中有否定,结论必须否定
        if (major.is_negative() or minor.is_negative()) and conclusion.is_affirmative():
            violations.append("违反结论规则: 前提中有否定,但结论是肯定的")

        # 如果结论否定,前提中必须有一个否定
        if conclusion.is_negative() and (major.is_affirmative() and minor.is_affirmative()):
            violations.append("违反结论规则: 结论是否定的,但前提中没有否定")

        return violations

    def _generate_explanation(self, syllogism: Syllogism, violations: List[str]) -> str:
        """generate验证说明"""
        if not violations:
            mood = syllogism.get_mood()
            figure = syllogism.get_figure()
            return f"该三段论是有效的.符合{figure.value}的{mood}式,且通过了所有规则检查."
        else:
            explanation = "该三段论是无效的.原因:\n"
            for i, violation in enumerate(violations, 1):
                explanation += f"{i}. {violation}\n"
            return explanation.strip()

    def get_all_valid_syllogisms(self) -> Dict[Figure, List[str]]:
        """get所有有效三段论"""
        return {
            figure: list(moods)
            for figure, moods in self.valid_syllogisms.items()
        }

    def get_valid_syllogisms_by_figure(self, figure: Figure) -> List[str]:
        """get指定格的所有有效三段论"""
        return list(self.valid_syllogisms.get(figure, set()))

    def validate_by_mood_and_figure(self, mood: str, figure: Figure) -> bool:
        """通过格和式验证 (快捷方法)"""
        return mood in self.valid_syllogisms.get(figure, set())

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")

    print("=== 三段论验证测试 ===\n")

    # 测试1: 有效的三段论 (Barbara, 第1格, AAA式)
    print("测试1: Barbara (第1格, AAA)")
    major = logic_engine.create_proposition('A', '人', '会死的')
    minor = logic_engine.create_proposition('A', '苏格拉底', '人')
    conclusion = logic_engine.create_proposition('A', '苏格拉底', '会死的')
    result1 = validator.validate(major, minor, conclusion)
    print(f"  三段论:\n{result1['三段论'].replace(chr(10), chr(10) + '    ')}")
    print(f"  结果: {'有效' if result1['是否有效'] else '无效'}")
    print(f"  格式: {result1['格']} {result1['式']}")
    print(f"  说明: {result1['说明']}\n")

    # 测试2: 无效的三段论 (违反中项规则)
    print("测试2: 无效三段论 (违反中项规则)")
    major = logic_engine.create_proposition('A', '狗', '动物')
    minor = logic_engine.create_proposition('A', '猫', '动物')
    conclusion = logic_engine.create_proposition('A', '狗', '猫')
    result2 = validator.validate(major, minor, conclusion)
    print(f"  三段论:\n{result2['三段论'].replace(chr(10), chr(10) + '    ')}")
    print(f"  结果: {'有效' if result2['是否有效'] else '无效'}")
    print(f"  格式: {result2['格']} {result2['式']}")
    if result2['周延性检查']['违规']:
        print(f"  周延性违规: {result2['周延性检查']['违规'][0]}")
    print(f"  说明: {result2['说明']}\n")

    # 测试3: 有效的三段论 (Celarent, 第1格, EAE式)
    print("测试3: Celarent (第1格, EAE)")
    major = logic_engine.create_proposition('E', '哺乳动物', '鱼')
    minor = logic_engine.create_proposition('A', '鲸鱼', '哺乳动物')
    conclusion = logic_engine.create_proposition('E', '鲸鱼', '鱼')
    result3 = validator.validate(major, minor, conclusion)
    print(f"  三段论:\n{result3['三段论'].replace(chr(10), chr(10) + '    ')}")
    print(f"  结果: {'有效' if result3['是否有效'] else '无效'}")
    print(f"  格式: {result3['格']} {result3['式']}")
    print(f"  说明: {result3['说明']}\n")

    # 显示所有有效三段论
    print("=== 所有有效三段论 ===")
    all_valid = validator.get_all_valid_syllogisms()
    for figure, moods in all_valid.items():
        print(f"{figure.value}: {', '.join(moods)}")
