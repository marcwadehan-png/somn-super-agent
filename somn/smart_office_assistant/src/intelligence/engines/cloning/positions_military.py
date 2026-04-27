# -*- coding: utf-8 -*-
"""
朝廷岗位体系 - 军政系统岗位
从 _court_positions.py 提取，V1.0.0
"""
from typing import List
from .court_helpers import _p, _zheng_cong_pair, _specialist_batch


def build_military_positions() -> List:
    """军政系统岗位"""
    positions = []

    # 一品
    positions += _zheng_cong_pair(
        "JZ_1_01", "太尉", "军政系统", pin_level=1,
        system_type_str="military",
        domain="全国军政最高决策",
        dispatch_path_prefix="皇帝→太尉",
        suitable_schools=["兵家", "法家"],
        description_prefix="军政最高决策",
        sage_type_str="practitioner",
    )

    # 二品
    positions += _zheng_cong_pair(
        "JZ_2_01", "大将军", "军政系统", pin_level=2,
        system_type_str="military",
        domain="战时最高指挥",
        dispatch_path_prefix="太尉→大将军",
        suitable_schools=["兵家"],
        description_prefix="战时指挥",
        sage_type_str="practitioner",
    )

    positions += _zheng_cong_pair(
        "JZ_2_02", "五军都督", "军政系统", pin_level=2,
        system_type_str="military",
        domain="五军训练与调度",
        dispatch_path_prefix="太尉→五军都督",
        suitable_schools=["兵家", "法家"],
        description_prefix="五军管理",
    )

    # 三品
    positions += _zheng_cong_pair(
        "JZ_3_01", "武库史", "军政系统", pin_level=3,
        system_type_str="military",
        domain="兵器管理与研发",
        dispatch_path_prefix="大将军→武库史",
        suitable_schools=["兵家", "科学家"],
        description_prefix="兵器管理",
    )

    # 四品
    positions += _zheng_cong_pair(
        "JZ_4_01", "卫尉", "军政系统", pin_level=4,
        system_type_str="military",
        domain="宫廷与都城防卫",
        dispatch_path_prefix="太尉→卫尉",
        suitable_schools=["兵家", "法家"],
        description_prefix="宫廷防卫",
    )

    # 五品
    positions += _zheng_cong_pair(
        "JZ_5_01", "车骑将军", "军政系统", pin_level=5,
        system_type_str="military",
        domain="骑兵指挥与边防",
        dispatch_path_prefix="大将军→车骑将军",
        suitable_schools=["兵家"],
        description_prefix="骑兵指挥",
    )

    # 专员（七品）
    positions += _specialist_batch("JZ_P7", "军政系统", pin_level=7, items=[
        ("军士教官", "兵法教学、阵法训练", ["兵家"]),
        ("军需专员", "粮草调度、军备管理", ["法家", "经济学家"]),
        ("侦察专员", "敌情侦察、情报收集", ["兵家", "纵横家"]),
        ("军法专员", "军纪执行、军法审判", ["法家"]),
    ])

    return positions
