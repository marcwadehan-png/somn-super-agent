# -*- coding: utf-8 -*-
"""
朝廷岗位体系 - 岗位补充
从 _court_positions.py 提取，V4.2.0
"""
from typing import List
from .court_helpers import _p, _zheng_cong_pair, _specialist_batch


def build_supplement_positions() -> List:
    """补充岗位（各系统空缺岗位）"""
    positions = []

    # 文治系统补充
    positions += _zheng_cong_pair(
        "WZ_S_01", "经筵讲官", "文治系统", pin_level=3,
        system_type_str="wenzhi",
        domain="皇帝经学讲授",
        dispatch_path_prefix="文渊阁大学士→经筵讲官",
        suitable_schools=["儒家"],
        description_prefix="经学讲授",
    )

    # 经济系统补充
    positions += _zheng_cong_pair(
        "JJ_S_01", "漕运总督", "经济系统", pin_level=2,
        system_type_str="economy",
        domain="漕运与粮食运输",
        dispatch_path_prefix="户部尚书→漕运总督",
        suitable_schools=["法家", "经济学家"],
        description_prefix="漕运管理",
    )

    # 军政系统补充
    positions += _zheng_cong_pair(
        "JZ_S_01", "边防都督", "军政系统", pin_level=2,
        system_type_str="military",
        domain="边防与边疆防御",
        dispatch_path_prefix="太尉→边防都督",
        suitable_schools=["兵家"],
        description_prefix="边防管理",
        sage_type_str="practitioner",
    )

    # 创新系统补充
    positions += _zheng_cong_pair(
        "CX_S_01", "天工监", "创新系统", pin_level=2,
        system_type_str="chuangxin",
        domain="天工开物与工艺创新",
        dispatch_path_prefix="墨家钜子→天工监",
        suitable_schools=["墨家", "科学家"],
        description_prefix="工艺创新",
        sage_type_str="practitioner",
    )

    # 标准系统补充
    positions += _zheng_cong_pair(
        "BZ_S_01", "考功郎中", "标准系统", pin_level=3,
        system_type_str="standard",
        domain="官员考核与绩效",
        dispatch_path_prefix="大理寺卿→考功郎中",
        suitable_schools=["法家", "儒家"],
        description_prefix="官员考核",
    )

    return positions
