# -*- coding: utf-8 -*-
"""
朝廷岗位体系 - 经济系统岗位
从 _court_positions.py 提取，V4.2.0
"""
from typing import List
from .court_helpers import _p, _zheng_cong_pair, _specialist_batch


def build_economy_positions() -> List:
    """经济系统岗位"""
    positions = []

    # 一品
    positions += _zheng_cong_pair(
        "JJ_1_01", "户部尚书", "经济系统", pin_level=1,
        system_type_str="economy",
        domain="国家财政与税收",
        dispatch_path_prefix="皇帝→户部尚书",
        suitable_schools=["儒家", "法家", "经济学家"],
        description_prefix="国家财政管理",
        sage_type_str="theorist",
    )

    # 二品
    positions += _zheng_cong_pair(
        "JJ_2_01", "盐铁史", "经济系统", pin_level=2,
        system_type_str="economy",
        domain="盐铁专营与资源管控",
        dispatch_path_prefix="户部尚书→盐铁史",
        suitable_schools=["法家", "经济学家"],
        description_prefix="盐铁专营管理",
    )

    positions += _zheng_cong_pair(
        "JJ_2_02", "度支郎中", "经济系统", pin_level=2,
        system_type_str="economy",
        domain="财政预算与支出",
        dispatch_path_prefix="户部尚书→度支郎中",
        suitable_schools=["儒家", "经济学家"],
        description_prefix="财政预算管理",
    )

    # 三品
    positions += _zheng_cong_pair(
        "JJ_3_01", "市舶使", "经济系统", pin_level=3,
        system_type_str="economy",
        domain="海外贸易与关税",
        dispatch_path_prefix="户部尚书→市舶使",
        suitable_schools=["法家", "经济学家", "纵横家"],
        description_prefix="海外贸易管理",
    )

    # 四品
    positions += _zheng_cong_pair(
        "JJ_4_01", "均输平准史", "经济系统", pin_level=4,
        system_type_str="economy",
        domain="物价调控与市场管理",
        dispatch_path_prefix="户部尚书→均输平准史",
        suitable_schools=["法家", "经济学家"],
        description_prefix="物价与市场管理",
    )

    # 五品
    positions += _zheng_cong_pair(
        "JJ_5_01", "户籍郎中", "经济系统", pin_level=5,
        system_type_str="economy",
        domain="户籍管理与人口统计",
        dispatch_path_prefix="户部尚书→户籍郎中",
        suitable_schools=["法家", "儒家"],
        description_prefix="户籍管理",
    )

    # 专员（七品）
    positions += _specialist_batch("JJ_P7", "经济系统", pin_level=7, items=[
        ("税赋专员", "税赋征收、账册登记", ["法家", "经济学家"]),
        ("市场专员", "市场监督、交易管理", ["法家"]),
        ("仓储专员", "粮食储备、仓储管理", ["农家"]),
        ("金融专员", "货币流通、物价监测", ["经济学家"]),
    ])

    return positions
