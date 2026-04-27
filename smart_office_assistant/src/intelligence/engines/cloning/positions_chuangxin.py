# -*- coding: utf-8 -*-
"""
朝廷岗位体系 - 创新系统岗位
从 _court_positions.py 提取，V4.2.0
"""
from typing import List
from .court_helpers import _p, _zheng_cong_pair, _specialist_batch


def build_chuangxin_positions() -> List:
    """创新系统岗位（墨家、科学家主导）"""
    positions = []

    # 一品
    positions += _zheng_cong_pair(
        "CX_1_01", "墨家钜子", "创新系统", pin_level=1,
        system_type_str="chuangxin",
        domain="科技创新与工艺最高",
        dispatch_path_prefix="皇帝→墨家钜子",
        suitable_schools=["墨家", "科学家"],
        description_prefix="科技创新最高决策",
        sage_type_str="practitioner",
    )

    # 二品
    positions += _zheng_cong_pair(
        "CX_2_01", "工部侍郎", "创新系统", pin_level=2,
        system_type_str="chuangxin",
        domain="工艺与工程",
        dispatch_path_prefix="墨家钜子→工部侍郎",
        suitable_schools=["墨家", "科学家"],
        description_prefix="工艺工程管理",
    )

    # 三品
    positions += _zheng_cong_pair(
        "CX_3_01", "司天监", "创新系统", pin_level=3,
        system_type_str="chuangxin",
        domain="天文与历法创新",
        dispatch_path_prefix="墨家钜子→司天监",
        suitable_schools=["科学家", "墨家"],
        description_prefix="天文历法创新",
    )

    # 四品
    positions += _zheng_cong_pair(
        "CX_4_01", "医官令", "创新系统", pin_level=4,
        system_type_str="chuangxin",
        domain="医疗与医药创新",
        dispatch_path_prefix="墨家钜子→医官令",
        suitable_schools=["科学家", "医家"],
        description_prefix="医疗医药创新",
    )

    # 专员（七品）
    positions += _specialist_batch("CX_P7", "创新系统", pin_level=7, items=[
        ("工艺专员", "器械制造、工艺改良", ["墨家", "科学家"]),
        ("算学专员", "数学计算、历法推算", ["科学家", "数学家"]),
        ("医药专员", "药材辨识、药方研究", ["科学家", "医家"]),
        ("工程专员", "工程建设、器械设计", ["墨家", "科学家"]),
    ])

    return positions
