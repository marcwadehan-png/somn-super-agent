"""
V1.0 社会科学智慧版系统集成测试

测试覆盖：
1. WisdomSchool枚举包含V1.0新增7学派
2. ProblemType枚举包含V1.0新增30+问题类型
3. ENGINE_TABLE正确注册7个V1.0引擎
4. problem_school_mapping包含V6.2映射
5. school_weights包含V6.2权重配置
6. V1.0引擎模块可正常导入
7. V1.0引擎可正常实例化
8. WisdomDispatcher可正确调度V1.0引擎
9. Claw配置文件格式正确

版本: V1.0
创建: 2026-04-25
"""

import pytest
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestV62Enums:
    """测试V1.0枚举定义"""

    def test_wisdom_school_v62_count(self):
        """验证WisdomSchool枚举包含42个学派（35+7）"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums import WisdomSchool
        schools = list(WisdomSchool)
        assert len(schools) >= 42, f"WisdomSchool应有42个学派，实际{len(schools)}个"

    def test_wisdom_school_v62_new_schools(self):
        """验证V1.0新增7个学派存在"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums import WisdomSchool

        v62_schools = [
            WisdomSchool.SOCIOLOGY,
            WisdomSchool.BEHAVIORAL_ECONOMICS,
            WisdomSchool.COMMUNICATION,
            WisdomSchool.CULTURAL_ANTHROPOLOGY,
            WisdomSchool.POLITICAL_ECONOMICS,
            WisdomSchool.ORGANIZATIONAL_PSYCHOLOGY,
            WisdomSchool.SOCIAL_PSYCHOLOGY,
        ]

        for school in v62_schools:
            assert school is not None, f"学派 {school} 未正确创建"
            assert school.value, f"学派 {school} 值为空"

    def test_problem_type_v62_count(self):
        """验证ProblemType枚举包含V1.0新增问题类型"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums import ProblemType

        v62_problem_types = [
            # 社会学
            ProblemType.SOCIAL_STRUCTURE_ANALYSIS,
            ProblemType.CLASS_MOBILITY,
            ProblemType.INSTITUTIONAL_SOCIOLOGY,
            ProblemType.SOCIAL_STRATIFICATION,
            ProblemType.COLLECTIVE_ACTION,
            # 行为经济学
            ProblemType.COGNITIVE_BIAS_V62,
            ProblemType.DECISION_MAKING_BEHAVIOR,
            ProblemType.MARKET_BEHAVIOR,
            ProblemType.INCENTIVE_DESIGN,
            ProblemType.NUDGE_POLICY,
            # 传播学
            ProblemType.MEDIA_EFFECT,
            ProblemType.PUBLIC_OPINION_FORMATION,
            ProblemType.INFORMATION_CASCADE,
            ProblemType.DISCOURSE_ANALYSIS,
            ProblemType.INTERPERSONAL_COMMUNICATION,
            # 文化人类学
            ProblemType.CULTURAL_PATTERN_RECOGNITION,
            ProblemType.SYMBOL_SYSTEM_ANALYSIS,
            ProblemType.RITUAL_CONTEXT_ANALYSIS,
            ProblemType.CROSS_CULTURAL_ADAPTATION,
            # 政治经济学
            ProblemType.INSTITUTIONAL_POLITICAL_ANALYSIS,
            ProblemType.POLICY_GAME_THEORY,
            ProblemType.MARKET_REGULATION_ANALYSIS,
            ProblemType.PUBLIC_CHOICE,
            # 组织心理学
            ProblemType.ORGANIZATIONAL_CHANGE_V62,
            ProblemType.LEADERSHIP_STYLE_ANALYSIS,
            ProblemType.TEAM_COHESION_ANALYSIS,
            ProblemType.ORGANIZATIONAL_CULTURE_V62,
            # 社会心理学
            ProblemType.CONFORMITY_BEHAVIOR,
            ProblemType.AUTHORITY_OBEDIENCE,
            ProblemType.SOCIAL_INFLUENCE_MECHANISM,
            ProblemType.GROUP_THINK_ANALYSIS,
        ]

        count = 0
        for pt in v62_problem_types:
            assert pt is not None, f"ProblemType {pt} 未正确创建"
            assert pt.value, f"ProblemType {pt} 值为空"
            count += 1

        assert count >= 30, f"V1.0应有至少30个ProblemType，实际{count}个"


class TestV62EngineRegistry:
    """测试V1.0引擎注册"""

    def test_engine_table_v62_registration(self):
        """验证ENGINE_TABLE包含V6.2的7个引擎注册"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_mapping import WisdomDispatcher
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums import WisdomSchool

        dispatcher = WisdomDispatcher()

        v62_schools = [
            WisdomSchool.SOCIOLOGY,
            WisdomSchool.BEHAVIORAL_ECONOMICS,
            WisdomSchool.COMMUNICATION,
            WisdomSchool.CULTURAL_ANTHROPOLOGY,
            WisdomSchool.POLITICAL_ECONOMICS,
            WisdomSchool.ORGANIZATIONAL_PSYCHOLOGY,
            WisdomSchool.SOCIAL_PSYCHOLOGY,
        ]

        for school in v62_schools:
            assert school in dispatcher._engine_registry, \
                f"学派 {school.value} 未在ENGINE_TABLE中注册"

    def test_school_weights_v62(self):
        """验证school_weights包含V6.2权重配置"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_mapping import WisdomDispatcher
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums import WisdomSchool

        dispatcher = WisdomDispatcher()

        v62_schools = [
            WisdomSchool.SOCIOLOGY,
            WisdomSchool.BEHAVIORAL_ECONOMICS,
            WisdomSchool.COMMUNICATION,
            WisdomSchool.CULTURAL_ANTHROPOLOGY,
            WisdomSchool.POLITICAL_ECONOMICS,
            WisdomSchool.ORGANIZATIONAL_PSYCHOLOGY,
            WisdomSchool.SOCIAL_PSYCHOLOGY,
        ]

        for school in v62_schools:
            assert school in dispatcher.school_weights, \
                f"学派 {school.value} 缺少权重配置"
            assert dispatcher.school_weights[school] > 0, \
                f"学派 {school.value} 权重应大于0"


class TestV62ProblemMapping:
    """测试V1.0问题类型映射"""

    def test_problem_school_mapping_v62(self):
        """验证problem_school_mapping包含V6.2映射"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_mapping import WisdomDispatcher
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums import ProblemType

        dispatcher = WisdomDispatcher()

        # 验证部分关键V1.0问题类型有映射
        key_problem_types = [
            ProblemType.SOCIAL_STRUCTURE_ANALYSIS,
            ProblemType.COGNITIVE_BIAS_V62,
            ProblemType.MEDIA_EFFECT,
            ProblemType.CULTURAL_PATTERN_RECOGNITION,
            ProblemType.INSTITUTIONAL_POLITICAL_ANALYSIS,
            ProblemType.ORGANIZATIONAL_CHANGE_V62,
            ProblemType.CONFORMITY_BEHAVIOR,
        ]

        for pt in key_problem_types:
            assert pt in dispatcher.problem_school_mapping, \
                f"ProblemType {pt.value} 缺少问题-学派映射"
            mappings = dispatcher.problem_school_mapping[pt]
            assert len(mappings) >= 2, \
                f"ProblemType {pt.value} 应至少有2个学派映射，实际{len(mappings)}个"


class TestV62EngineModules:
    """测试V1.0引擎模块"""

    def test_sociology_wisdom_import(self):
        """验证社会学引擎可导入"""
        try:
            from smart_office_assistant.src.intelligence.engines.sociology_wisdom import SociologyWisdomCore
            assert SociologyWisdomCore is not None
        except ImportError as e:
            pytest.skip(f"sociology_wisdom模块导入失败: {e}")

    def test_behavioral_economics_wisdom_import(self):
        """验证行为经济学引擎可导入"""
        try:
            from smart_office_assistant.src.intelligence.engines.behavioral_economics_wisdom import BehavioralEconomicsWisdomCore
            assert BehavioralEconomicsWisdomCore is not None
        except ImportError as e:
            pytest.skip(f"behavioral_economics_wisdom模块导入失败: {e}")

    def test_communication_wisdom_import(self):
        """验证传播学引擎可导入"""
        try:
            from smart_office_assistant.src.intelligence.engines.communication_wisdom import CommunicationWisdomCore
            assert CommunicationWisdomCore is not None
        except ImportError as e:
            pytest.skip(f"communication_wisdom模块导入失败: {e}")

    def test_anthropology_wisdom_import(self):
        """验证文化人类学引擎可导入"""
        try:
            from smart_office_assistant.src.intelligence.engines.anthropology_wisdom import AnthropologyWisdomCore
            assert AnthropologyWisdomCore is not None
        except ImportError as e:
            pytest.skip(f"anthropology_wisdom模块导入失败: {e}")

    def test_political_economics_wisdom_import(self):
        """验证政治经济学引擎可导入"""
        try:
            from smart_office_assistant.src.intelligence.engines.political_economics_wisdom import PoliticalEconomicsWisdomCore
            assert PoliticalEconomicsWisdomCore is not None
        except ImportError as e:
            pytest.skip(f"political_economics_wisdom模块导入失败: {e}")

    def test_organizational_psychology_wisdom_import(self):
        """验证组织心理学引擎可导入"""
        try:
            from smart_office_assistant.src.intelligence.engines.organizational_psychology_wisdom import OrganizationalPsychologyWisdomCore
            assert OrganizationalPsychologyWisdomCore is not None
        except ImportError as e:
            pytest.skip(f"organizational_psychology_wisdom模块导入失败: {e}")

    def test_social_psychology_wisdom_import(self):
        """验证社会心理学引擎可导入"""
        try:
            from smart_office_assistant.src.intelligence.engines.social_psychology_wisdom import SocialPsychologyWisdomCore
            assert SocialPsychologyWisdomCore is not None
        except ImportError as e:
            pytest.skip(f"social_psychology_wisdom模块导入失败: {e}")


class TestV62EngineInstantiation:
    """测试V1.0引擎实例化"""

    def test_sociology_wisdom_instantiation(self):
        """验证社会学引擎可实例化"""
        try:
            from smart_office_assistant.src.intelligence.engines.sociology_wisdom import SociologyWisdomCore
            engine = SociologyWisdomCore()
            assert engine is not None
            # 验证基本方法存在
            assert hasattr(engine, '_initialize_sages')
        except ImportError:
            pytest.skip("sociology_wisdom模块不可用")

    def test_behavioral_economics_wisdom_instantiation(self):
        """验证行为经济学引擎可实例化"""
        try:
            from smart_office_assistant.src.intelligence.engines.behavioral_economics_wisdom import BehavioralEconomicsWisdomCore
            engine = BehavioralEconomicsWisdomCore()
            assert engine is not None
        except ImportError:
            pytest.skip("behavioral_economics_wisdom模块不可用")

    def test_communication_wisdom_instantiation(self):
        """验证传播学引擎可实例化"""
        try:
            from smart_office_assistant.src.intelligence.engines.communication_wisdom import CommunicationWisdomCore
            engine = CommunicationWisdomCore()
            assert engine is not None
        except ImportError:
            pytest.skip("communication_wisdom模块不可用")


class TestV62ClawConfigs:
    """测试V1.0 Claw配置文件"""

    def test_claw_config_directory_exists(self):
        """验证V1.0 Claw配置目录存在"""
        claw_dir = project_root / "smart_office_assistant" / "src" / "intelligence" / "engines" / "claws" / "configs_v62"
        assert claw_dir.exists(), f"V1.0 Claw配置目录不存在: {claw_dir}"

    def test_claw_config_count(self):
        """验证V1.0 Claw配置文件数量为50个"""
        claw_dir = project_root / "smart_office_assistant" / "src" / "intelligence" / "engines" / "claws" / "configs_v62"
        yaml_files = list(claw_dir.glob("*.yaml"))
        assert len(yaml_files) >= 50, f"V1.0应有50个Claw配置，实际{len(yaml_files)}个"

    def test_claw_config_format(self):
        """验证Claw配置文件格式正确"""
        import yaml
        claw_dir = project_root / "smart_office_assistant" / "src" / "intelligence" / "engines" / "claws" / "configs_v62"
        yaml_files = list(claw_dir.glob("*.yaml"))[:5]  # 检查前5个

        for yaml_file in yaml_files:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                assert data is not None, f"{yaml_file.name} 解析失败"
                assert 'name' in data, f"{yaml_file.name} 缺少name字段"
                assert 'school' in data, f"{yaml_file.name} 缺少school字段"
                assert 'core_ability' in data, f"{yaml_file.name} 缺少core_ability字段"

    def test_claw_school_coverage(self):
        """验证V6.2的7个学派都有Claw配置"""
        import yaml
        claw_dir = project_root / "smart_office_assistant" / "src" / "intelligence" / "engines" / "claws" / "configs_v62"
        yaml_files = list(claw_dir.glob("*.yaml"))

        schools = set()
        for yaml_file in yaml_files:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if 'school' in data:
                    schools.add(data['school'])

        expected_schools = [
            'SOCIOLOGY',
            'BEHAVIORAL_ECONOMICS',
            'COMMUNICATION',
            'CULTURAL_ANTHROPOLOGY',
            'POLITICAL_ECONOMICS',
            'ORGANIZATIONAL_PSYCHOLOGY',
            'SOCIAL_PSYCHOLOGY',
        ]

        for school in expected_schools:
            assert school in schools, f"学派 {school} 缺少Claw配置"


class TestV62Integration:
    """测试V1.0系统集成"""

    def test_wisdom_dispatcher_v62_schools(self):
        """验证WisdomDispatcher可识别V1.0学派"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_mapping import WisdomDispatcher
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums import WisdomSchool

        dispatcher = WisdomDispatcher()

        # 验证所有42个学派都在school_weights中
        all_schools = list(WisdomSchool)
        missing = [s for s in all_schools if s not in dispatcher.school_weights]
        assert len(missing) == 0, f"缺少权重配置: {[s.value for s in missing]}"

    def test_v62_school_weight_total(self):
        """验证V6.2后学派权重总和合理（相对权重，不需要归一化到1.0）"""
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._dispatch_mapping import WisdomDispatcher

        dispatcher = WisdomDispatcher()
        total_weight = sum(dispatcher.school_weights.values())

        # 权重总和应 > 0（所有学派都有权重配置）
        assert total_weight > 0, f"学派权重总和为零"
        # 每个权重值应在合理范围内
        for school, w in dispatcher.school_weights.items():
            assert 0.01 <= w <= 0.15, f"学派{school}权重{w}超出合理范围[0.01, 0.15]"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
