# -*- coding: utf-8 -*-
"""
朝廷岗位体系 - 专员领班岗位
从 _court_positions.py 提取，V4.2.0
"""
from typing import List
from .court_helpers import _p, _specialist_batch


def build_specialist_leaders() -> List:
    """专员领班岗位（各系统专员总管）"""
    positions = []

    # 文治系统专员领班（正值从四品）
    positions += _specialist_batch("WZ_SL", "专员领班", pin_level=4, items=[
        ("文治专员领班（正）", "文治系统专员管理与协调", ["儒家", "文学家"]),
        ("文治专员领班（从）", "文治系统专员管理与协调", ["儒家", "文学家"]),
    ])
    positions[-2].is_zheng = True
    positions[-1].is_zheng = False

    # 经济系统专员领班
    positions += _specialist_batch("JJ_SL", "专员领班", pin_level=4, items=[
        ("经济专员领班（正）", "经济系统专员管理与协调", ["法家", "经济学家"]),
        ("经济专员领班（从）", "经济系统专员管理与协调", ["法家", "经济学家"]),
    ])
    positions[-2].is_zheng = True
    positions[-1].is_zheng = False

    # 军政系统专员领班
    positions += _specialist_batch("JZ_SL", "专员领班", pin_level=4, items=[
        ("军政专员领班（正）", "军政系统专员管理与协调", ["兵家"]),
        ("军政专员领班（从）", "军政系统专员管理与协调", ["兵家"]),
    ])
    positions[-2].is_zheng = True
    positions[-1].is_zheng = False

    # 标准系统专员领班
    positions += _specialist_batch("BZ_SL", "专员领班", pin_level=4, items=[
        ("标准专员领班（正）", "标准系统专员管理与协调", ["法家"]),
        ("标准专员领班（从）", "标准系统专员管理与协调", ["法家"]),
    ])
    positions[-2].is_zheng = True
    positions[-1].is_zheng = False

    return positions
