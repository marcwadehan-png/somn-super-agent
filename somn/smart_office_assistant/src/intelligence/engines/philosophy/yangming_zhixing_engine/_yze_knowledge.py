# -*- coding: utf-8 -*-
"""王阳明知行合一引擎 - 知识库模块"""
from typing import Dict, List

class ZhixingKnowledgeBase:
    """知行知识库"""

    # 知行语录库
    ZHIXING_QUOTES = {
        "知行本质": [
            "知之真切笃实处即是行,行之明觉精察处即是知.",
            "知是行的开始,行是知的功夫.",
            "知而不行,只是未知.",
            "未有知而不行者,知而不行,只是未知."
        ],
        "真知验证": [
            "真知必能行,真行才是知.",
            "知而不行,犹未知也.",
            "知到极处,行到极处,方是真知."
        ],
        "action启动": [
            "人须在事上磨,方立得住.",
            "知是行的主意,行是知的功夫.",
            "只想不做,不是真知."
        ],
        "迭代深化": [
            "在事上磨练,在行中证知.",
            "知一行十,方见真章.",
            "知行相长,如车两轮."
        ]
    }

    # 知的层次定义
    KNOWING_LEVELS = {
        "UNKNOWN": {
            "description": "完全不了解",
            "action_test": "是否听说过?",
            "score_range": (0, 10)
        },
        "HEARSAY": {
            "description": "听过但不了解,不能复述",
            "action_test": "能用自己的话解释吗?",
            "score_range": (10, 30)
        },
        "UNDERSTANDING": {
            "description": "理论上理解,但缺乏实践验证",
            "action_test": "能在实际中应用吗?",
            "score_range": (30, 55)
        },
        "PRACTICED": {
            "description": "有实践经验,有切身体会",
            "action_test": "能从经验中总结规律吗?",
            "score_range": (55, 75)
        },
        "INTEGRATED": {
            "description": "知与行开始unified,能灵活应用",
            "action_test": "能教授他人吗?",
            "score_range": (75, 90)
        },
        "NATURAL": {
            "description": "无需思考自然做到,身心合一",
            "action_test": "已经成为本能了吗?",
            "score_range": (90, 100)
        }
    }

    # action阶段定义
    ACTION_STAGES = {
        "NOT_STARTED": {
            "description": "完全没开始action",
            "indicators": ["还没做", "一直拖着", "没开始"],
            "score_range": (0, 15)
        },
        "DELAYED": {
            "description": "知道要做但一直拖延",
            "indicators": ["等会", "以后", "再说"],
            "score_range": (15, 35)
        },
        "STARTED": {
            "description": "已经开始action",
            "indicators": ["开始做了", "已经启动"],
            "score_range": (35, 60)
        },
        "PERSISTING": {
            "description": "持续执行中",
            "indicators": ["坚持", "持续", "一直在做"],
            "score_range": (60, 80)
        },
        "HABITUAL": {
            "description": "已经成为习惯",
            "indicators": ["习惯了", "每天", "自然"],
            "score_range": (80, 95)
        },
        "MASTERED": {
            "description": "精通,身心合一",
            "indicators": ["不刻意", "无条件", "身心合一"],
            "score_range": (95, 100)
        }
    }

    # 障碍解决方案
    BARRIER_SOLUTIONS = {
        "COGNITIVE": {
            "problem": "知之不深,停留在表面理解",
            "solution": [
                "1. 多角度理解:从不同角度学习同一知识",
                "2. 联系实际:将知识与自身经验联系起来",
                "3. 案例分析:研究他人如何实践",
                "4. 教授他人:用自己的话解释给别人听"
            ],
            "mini_action": "找一个具体的例子来说明这个道理"
        },
        "MOTIVATION": {
            "problem": "知与行之间缺乏动力连接",
            "solution": [
                "1. 找到意义:理解为什么要做这件事",
                "2. 愿景激励:想象完成后带来的好处",
                "3. 降低门槛:从小目标开始,减少心理阻力",
                "4. 即时奖励:给action设立即时反馈"
            ],
            "mini_action": "想象完成后的三个好处"
        },
        "CAPABILITY": {
            "problem": "知道该做什么但不知道怎么做到",
            "solution": [
                "1. 分解任务:大目标分解为小步骤",
                "2. 寻找榜样:学习有经验的人如何做",
                "3. 寻求帮助:不要闭门造车",
                "4. 边做边学:在实践中学习"
            ],
            "mini_action": "把任务分解为三个步骤"
        },
        "ENVIRONMENT": {
            "problem": "外部条件不成熟",
            "solution": [
                "1. 创造条件:主动营造有利环境",
                "2. 简化条件:寻找不需要完美条件的方法",
                "3. 利用现有:充分利用现有资源",
                "4. 等待时机:在等待中做好准备"
            ],
            "mini_action": "找一个不需要外部条件的切入点"
        },
        "DESIRE": {
            "problem": "私欲遮蔽良知",
            "solution": [
                "1. 静心反思:找出是什么欲望在阻碍",
                "2. 致良知:问自己什么是真正应该做的",
                "3. 去私欲:放下小我,追求更高目标",
                "4. 事上练:在大是大非上检验良知"
            ],
            "mini_action": "问自己:三年后回看,这件事重要吗?"
        }
    }
