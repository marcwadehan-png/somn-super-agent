"""
跨尺度思维引擎 - 常量定义模块
Cross-Scale Thinking Engine - Constants Module
"""

from typing import Dict
from ._cst_types import ScaleLevel, ScaleInfo, EmergenceExample, EmergenceType, PhysicalConstant

# 尺度层级完整定义
SCALE_HIERARCHY: Dict[ScaleLevel, ScaleInfo] = {
    ScaleLevel.QUANTUM_FOAM: ScaleInfo(
        level=ScaleLevel.QUANTUM_FOAM,
        name_zh="量子泡沫",
        size_range=(1.6e-35, 1e-20),
        key_theories=["量子引力", "弦理论", "圈量子引力", "非交换几何"],
        key_entities=["量子泡沫", "弦", "时空本身"],
        energy_scale=1.22e19,  # 普朗克能量
        governing_laws=["未知的量子引力定律"]
    ),
    ScaleLevel.SUBATOMIC: ScaleInfo(
        level=ScaleLevel.SUBATOMIC,
        name_zh="亚原子",
        size_range=(1e-20, 1e-14),
        key_theories=["标准模型", "量子色动力学", "电弱理论", "量子场论"],
        key_entities=["夸克", "轻子", "规范玻色子", "希格斯玻色子"],
        energy_scale=1e9,
        governing_laws=["SU(3)×SU(2)×U(1)规范对称性", "费曼路径积分"]
    ),
    ScaleLevel.ATOMIC: ScaleInfo(
        level=ScaleLevel.ATOMIC,
        name_zh="原子",
        size_range=(1e-14, 1e-9),
        key_theories=["量子力学", "原子物理", "化学元素理论"],
        key_entities=["原子", "离子", "原子轨道", "电子云"],
        energy_scale=13.6,  # 氢原子电离能
        governing_laws=["薛定谔方程", "泡利不相容原理"]
    ),
    ScaleLevel.MOLECULAR: ScaleInfo(
        level=ScaleLevel.MOLECULAR,
        name_zh="分子",
        size_range=(1e-9, 1e-6),
        key_theories=["量子化学", "分子轨道理论", "统计热力学"],
        key_entities=["分子", "蛋白质", "DNA", "RNA", "脂质膜"],
        energy_scale=0.1,
        governing_laws=["Born-Oppenheimer近似", "Hartree-Fock/DFT", "配分函数"]
    ),
    ScaleLevel.CELLULAR: ScaleInfo(
        level=ScaleLevel.CELLULAR,
        name_zh="细胞",
        size_range=(1e-6, 1e-3),
        key_theories=["分子生物学", "系统生物学", "生物化学"],
        key_entities=["细胞", "细胞器", "病毒", "细胞信号网络"],
        energy_scale=1e-3,
        governing_laws=["中心法则", "代谢网络", "信号转导"]
    ),
    ScaleLevel.ORGANISM: ScaleInfo(
        level=ScaleLevel.ORGANISM,
        name_zh="生物体",
        size_range=(1e-3, 1e5),
        key_theories=["演化生物学", "生态学", "神经科学", "心理学"],
        key_entities=["多细胞生物", "大脑", "生态系统"],
        energy_scale=1e-10,
        governing_laws=["自然选择", "遗传学定律", "神经动力学"]
    ),
    ScaleLevel.PLANETARY: ScaleInfo(
        level=ScaleLevel.PLANETARY,
        name_zh="行星",
        size_range=(1e5, 1e12),
        key_theories=["地质学", "大气科学", "海洋学", "地球系统科学"],
        key_entities=["行星", "大气层", "海洋", "板块"],
        energy_scale=1e-30,
        governing_laws=["纳维-斯托克斯方程", "Stokes对流", "放射性衰变"]
    ),
    ScaleLevel.STELLAR: ScaleInfo(
        level=ScaleLevel.STELLAR,
        name_zh="恒星系统",
        size_range=(1e12, 1e16),
        key_theories=["恒星物理", "核天体物理", "行星系统动力学"],
        key_entities=["恒星", "行星系统", "星云", "恒星风"],
        energy_scale=1e-20,
        governing_laws=["恒星核合成", "流体力学+辐射转移"]
    ),
    ScaleLevel.GALACTIC: ScaleInfo(
        level=ScaleLevel.GALACTIC,
        name_zh="星系",
        size_range=(1e16, 1e23),
        key_theories=["星系动力学", "宇宙学", "暗物质理论"],
        key_entities=["星系", "星系团", "暗物质晕", "超大质量黑洞"],
        energy_scale=1e-25,
        governing_laws=["广义相对论", "修正牛顿动力学(MOND?)"]
    ),
    ScaleLevel.COSMOLOGICAL: ScaleInfo(
        level=ScaleLevel.COSMOLOGICAL,
        name_zh="宇宙学",
        size_range=(1e23, 8.8e26),
        key_theories=["ΛCDM宇宙学", "暴胀理论", "量子宇宙学"],
        key_entities=["可观测宇宙", "宇宙微波背景", "大尺度结构", "暗能量"],
        energy_scale=1e-33,
        governing_laws=["Einstein场方程", "Friedmann方程"]
    ),
}

# 核心涌现现象
EMERGENCE_EXAMPLES = [
    EmergenceExample(
        name="原子→化学键→分子",
        from_level=ScaleLevel.ATOMIC,
        to_level=ScaleLevel.MOLECULAR,
        type=EmergenceType.WEAK_EMERGENCE,
        description="原子间的电磁相互作用产生化学键,原子单独不存在'化学性'",
        key_mechanism="量子力学多体效应 + Born-Oppenheimer近似"
    ),
    EmergenceExample(
        name="分子→自复制→生命",
        from_level=ScaleLevel.MOLECULAR,
        to_level=ScaleLevel.CELLULAR,
        type=EmergenceType.STRONG_EMERGENCE,
        description="特定分子组合产生自复制和代谢--生命涌现",
        key_mechanism="自催化化学网络 + 原始细胞形成"
    ),
    EmergenceExample(
        name="细胞→多细胞组织→器官",
        from_level=ScaleLevel.CELLULAR,
        to_level=ScaleLevel.ORGANISM,
        type=EmergenceType.WEAK_EMERGENCE,
        description="细胞分化产生组织和器官功能",
        key_mechanism="基因调控网络 + 细胞信号转导 + 形态发生素梯度"
    ),
    EmergenceExample(
        name="神经元→意识",
        from_level=ScaleLevel.CELLULAR,
        to_level=ScaleLevel.ORGANISM,
        type=EmergenceType.STRONG_EMERGENCE,
        description="约860亿神经元的电化学活动涌现出主观体验",
        key_mechanism="未知--意识的困难问题(Hard Problem)"
    ),
    EmergenceExample(
        name="个体→文化→文明",
        from_level=ScaleLevel.ORGANISM,
        to_level=ScaleLevel.PLANETARY,
        type=EmergenceType.WEAK_EMERGENCE,
        description="人类个体通过语言和制度涌现出文明",
        key_mechanism="文化演化 + 累积性技术创新 + 制度演化"
    ),
    EmergenceExample(
        name="星系→大尺度结构→宇宙网",
        from_level=ScaleLevel.GALACTIC,
        to_level=ScaleLevel.COSMOLOGICAL,
        type=EmergenceType.WEAK_EMERGENCE,
        description="暗物质+暗能量驱动的引力不稳定性产生宇宙丝状结构",
        key_mechanism="金斯不稳定性 + 暗物质N体模拟"
    ),
]

# 关键物理常数及其人择意义
FINE_TUNED_CONSTANTS = {
    "fine_structure": PhysicalConstant(
        name="精细结构常数",
        symbol="α",
        value=1/137.036,
        unit="无量纲",
        fine_tuning_sensitivity="α变化>10%将阻止碳基生命(恒星核合成路径改变)",
        anthropic_relevance="决定原子大小,化学键强度,核反应速率"
    ),
    "strong_coupling": PhysicalConstant(
        name="强耦合常数",
        symbol="α_s",
        value=1.2,
        unit="无量纲(μ=91GeV)",
        fine_tuning_sensitivity="α_s变化>5%将使氘不稳定或碳无法合成",
        anthropic_relevance="决定原子核稳定性,元素丰度"
    ),
    "cosmological_constant": PhysicalConstant(
        name="宇宙学常数",
        symbol="Λ",
        value=1.1e-52,
        unit="m^-2",
        fine_tuning_sensitivity="理论预测~10^120倍于观测值,精度~10^-122",
        anthropic_relevance="Λ过大→宇宙膨胀过快→结构无法形成"
    ),
    "gravity_ratio": PhysicalConstant(
        name="引力与电磁力之比",
        symbol="F_g/F_em",
        value=2.3e-39,
        unit="无量纲(质子间)",
        fine_tuning_sensitivity="引力若强10^36倍→恒星寿命从数十亿年降至数年",
        anthropic_relevance="决定恒星寿命→决定复杂生命是否有时间演化"
    ),
    "higgs_vacuum": PhysicalConstant(
        name="希格斯真空期望值",
        symbol="v",
        value=246.22,
        unit="GeV",
        fine_tuning_sensitivity="v变化数倍将改变所有基本粒子质量",
        anthropic_relevance="决定电子质量→决定原子大小和化学"
    ),
    "neutron_proton_mass_diff": PhysicalConstant(
        name="中子-质子质量差",
        symbol="Δm_n-p",
        value=1.293,
        unit="MeV/c²",
        fine_tuning_sensitivity="Δm_n-p若为负→中子比质子稳定→无氢→无水→无生命",
        anthropic_relevance="决定氢元素丰度→决定水和有机化学的可能性"
    ),
    "carbon_resonance": PhysicalConstant(
        name="碳-12 Hoyle共振态",
        symbol="E_Hoyle",
        value=7.65,
        unit="MeV",
        fine_tuning_sensitivity="Hoyle态能量偏移100keV将使三重α过程效率暴跌",
        anthropic_relevance="碳基生命的元素基础"
    ),
}

__all__ = [
    'SCALE_HIERARCHY',
    'EMERGENCE_EXAMPLES',
    'FINE_TUNED_CONSTANTS',
]
