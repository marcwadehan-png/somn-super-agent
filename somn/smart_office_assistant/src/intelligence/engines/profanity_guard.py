# -*- coding: utf-8 -*-
"""
__all__ = [
    'activate',
    'check_apology',
    'deactivate',
    'detect',
    'force_exit_enraged',
    'get_status',
    'is_active',
    'is_enraged',
    'needs_apology',
    'process',
    'remaining_minutes',
    'should_gate',
    'stage',
    'total_violations',
    'warning_count',
]

脏话规劝引擎 + 道歉门禁 v1.0.0

脏话规劝引擎(ProfanityGuardEngine):
- 检测攻击性/脏话输入
- 第1次:温和规劝
- 第2次:严厉警告
- 第3次+:怒转 Sharp 攻击模式(放弃规劝,直接怼)
- 规劝计数有衰减:每轮无脏话对话 -1,归零后重新开始

道歉门禁(ApologyGate):
- 当 Sharp 怼人模式持续超过 3 轮后,对方结束/转移话题
- 2 小时内发出任务指令 → 要求道歉才执行
- 检测道歉关键词 → 放行
- 对方拒绝道歉或继续无礼 → 继续拒接

集成位置:
- ProfanityGuardEngine 集成到 persona_core.py 的 generate_voice_output()
- ApologyGate 集成到 agent_core.py 的 process_input()
"""

import time
import random
import logging
from enum import IntEnum
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
# 脏话规劝引擎
# ═══════════════════════════════════════════════════════════════

class GuardStage(IntEnum):
    """规劝阶段"""
    PEACEFUL = 0        # 和平态:无脏话记录
    FIRST_WARNING = 1   # 第一次规劝:温和提醒
    SECOND_WARNING = 2  # 第二次规劝:严厉警告
    ENRAGED = 3         # 第三次+:怒转攻击模式

# 脏话/攻击性语言信号词库
PROFANITY_SIGNALS = {
    "strong_profanity": {
        "signals": [
            "傻逼", "傻b", "傻B", "sb", "Sb", "SB", "煞笔",
            "脑残", "白痴", "智障", "废物", "垃圾",
            "畜生", "人渣", "贱人", "婊子",
            "狗东西", "禽兽", "败类", "滚蛋",
            "妈的", "他妈的", "你妈的", "操你",
            "草泥马", "卧槽", "我靠", "日你",
            "去死", "该死", "死全家",
            "你他妈", "他妈",
        ],
        "weight": 1.0,
        "description": "重度脏话/侮辱性词汇",
    },
    "moderate_profanity": {
        "signals": [
            "傻", "蠢", "笨蛋", "白痴", "有病", "神经病",
            "疯子", "脑瘫", "弱智", "二逼", "二百五",
            "滚", "闭嘴", "别废话", "你算什么东西",
            "你什么档次", "你什么货色",
            "废物", "垃圾人", "恶心",
            "丑八怪", "肥猪", "死胖子",
        ],
        "weight": 0.7,
        "description": "中度脏话/攻击性词汇",
    },
    "threatening": {
        "signals": [
            "信不信我", "你等着", "小心点", "惹毛我", "我揍你",
            "看我不弄死你", "有你好看的", "管好你自己",
            "再多嘴试试", "找死", "你试试看", "不想活了",
            "不客气", "别逼我", "你再这样", "惹火我了",
            "你再骂一句试试", "有本事",
        ],
        "weight": 0.85,
        "description": "威胁性语言",
    },
    "verbal_abuse_pattern": {
        "signals": [
            "你怎么这么", "你真是", "你这种人", "你活该",
            "自找的", "就你这水平", "也不看看自己",
            "配吗", "你配吗", "不配", "谁给你的脸",
            "你懂什么", "你算老几", "少在我面前",
        ],
        "weight": 0.5,
        "description": "语言暴力模式(需结合上下文)",
    },
}

# 规劝话术库
GUARD_RESPONSES = {
    GuardStage.FIRST_WARNING: {
        "mild": [
            "嗯?注意措辞.",
            "换个说法.我不接受这种表达方式.",
            "有些词不需要说出口,你完全可以用正常方式表达.",
            "脏话不是交流,是噪音.你有什么想说的,好好说.",
            "控制一下措辞,沟通是两个人的事.",
            "我可以接受你的情绪,但不接受脏话.有话好好说.",
        ],
        "firm": [
            "我不接受脏话.有意见可以直接说.",
            "注意你的措辞.你可以说任何观点,但不能用这种方式.",
            "语言是有边界的.你要表达什么,换一种方式.",
        ],
    },
    GuardStage.SECOND_WARNING: {
        "warning": [
            "第二次了.我再提醒你一次:不许骂人.",
            "我说过一次了.再这样,我不会客气.",
            "这是最后一次警告.你要是控制不住自己的嘴,那就不聊了.",
            "我说了注意措辞,你没听到?再骂一次,后果自负.",
            "你已经越线了.最后一次提醒:收起你的脏话.",
            "我数到二了.下次不会再给你机会.",
            "你是不是听不懂人话?我说了不许说脏话.再来一次,别怪我不给你面子.",
        ],
    },
    GuardStage.ENRAGED: {
        "declaration": [
            "[规劝已终止.对方执意攻击,怒转攻击模式.]",
        ],
    },
}

# 道歉检测关键词
APOLOGY_SIGNALS = [
    "对不起", "抱歉", "不好意思", "我错了", "是我的错",
    "抱歉抱歉", "对不住", "我收回刚才的话", "对不起嘛",
    "刚才不应该", "我不该那么说", "我态度不好",
    "原谅我", "不好意思啦", "是我的问题",
    "Sorry", "sorry", "抱歉啊", "对不起啊",
    "我刚才失态了", "请原谅", "对不起我错了",
    "是我太过分了", "我不应该骂你", "我说话太难听了",
]

class ProfanityGuardEngine:
    """
    脏话规劝引擎 v1.0.0

    三段式防线:
    1. 第一次脏话 → 温和规劝
    2. 第二次脏话 → 严厉警告
    3. 第三次+ → 怒转攻击(放弃规劝)
    """

    def __init__(self):
        self._warning_count: int = 0          # 当前规劝次数
        self._stage: GuardStage = GuardStage.PEACEFUL
        self._total_violations: int = 0       # 总违规次数(累计不衰减)
        self._last_violation_time: float = 0.0
        self._enraged_until: float = 0.0      # 攻击模式持续时间
        self._enraged_rounds: int = 0         # 攻击模式已持续轮次
        self._enraged_max_rounds: int = 10    # 攻击模式最长持续轮次
        self._clean_rounds: int = 0           # 连续无脏话轮次(用于衰减)

    @property
    def stage(self) -> GuardStage:
        return self._stage

    @property
    def is_enraged(self) -> bool:
        """是否处于怒转攻击模式"""
        if self._enraged_until > 0 and time.time() < self._enraged_until:
            return True
        return False

    @property
    def warning_count(self) -> int:
        return self._warning_count

    @property
    def total_violations(self) -> int:
        return self._total_violations

    def detect(self, user_input: str) -> Dict[str, Any]:
        """
        检测输入是否含攻击性/脏话

        Returns:
            {
                "detected": bool,
                "profanity_level": float (0-1),
                "matched_categories": [str],
                "severity": str,
            }
        """
        text = user_input.lower()
        matched = []
        max_weight = 0.0
        total_hits = 0

        for cat, cfg in PROFANITY_SIGNALS.items():
            hits = sum(1 for s in cfg["signals"] if s.lower() in text)
            if hits > 0:
                matched.append(cat)
                total_hits += hits
                max_weight = max(max_weight, cfg["weight"])

        if not matched:
            return {
                "detected": False,
                "profanity_level": 0.0,
                "matched_categories": [],
                "severity": "none",
            }

        # 计算脏话浓度
        level = min(1.0, max_weight * (1 + total_hits * 0.3))

        # judge严重程度
        if level >= 0.8:
            severity = "high"
        elif level >= 0.5:
            severity = "medium"
        else:
            severity = "low"

        return {
            "detected": True,
            "profanity_level": round(level, 2),
            "matched_categories": matched,
            "severity": severity,
        }

    def process(self, user_input: str) -> Dict[str, Any]:
        """
        处理用户输入,返回规劝decision

        Returns:
            {
                "action": "guard_warn_1" | "guard_warn_2" | "enraged_attack" | "no_guard",
                "stage": GuardStage,
                "response": str | None,
                "warning_count": int,
            }
        """
        # 如果已经在攻击模式中,继续计数但不重复规劝
        if self.is_enraged:
            self._enraged_rounds += 1
            # 攻击模式超过最大轮次,自动冷却
            if self._enraged_rounds >= self._enraged_max_rounds:
                self._exit_enraged()
            return {
                "action": "enraged_attack",
                "stage": self._stage,
                "response": None,
                "warning_count": self._warning_count,
            }

        detection = self.detect(user_input)

        if not detection["detected"]:
            # 无脏话 → 连续正常轮次+1,每2轮衰减1次
            self._clean_rounds += 1
            if self._clean_rounds >= 2:
                self._warning_count = max(0, self._warning_count - 1)
                self._clean_rounds = 0
                if self._warning_count == 0:
                    self._stage = GuardStage.PEACEFUL
            return {
                "action": "no_guard",
                "stage": self._stage,
                "response": None,
                "warning_count": self._warning_count,
            }

        # 检测到脏话
        self._total_violations += 1
        self._last_violation_time = time.time()
        self._warning_count += 1
        self._clean_rounds = 0  # 重置正常轮次计数

        if self._warning_count == 1:
            # 第一次 → 温和规劝
            self._stage = GuardStage.FIRST_WARNING
            resp = self._generate_guard_response(GuardStage.FIRST_WARNING)
            logger.info(f"[规劝引擎] 第一次警告: {user_input[:20]}...")
            return {
                "action": "guard_warn_1",
                "stage": self._stage,
                "response": resp,
                "warning_count": self._warning_count,
            }

        elif self._warning_count == 2:
            # 第二次 → 严厉警告
            self._stage = GuardStage.SECOND_WARNING
            resp = self._generate_guard_response(GuardStage.SECOND_WARNING)
            logger.info(f"[规劝引擎] 第二次警告: {user_input[:20]}...")
            return {
                "action": "guard_warn_2",
                "stage": self._stage,
                "response": resp,
                "warning_count": self._warning_count,
            }

        else:
            # 第三次+ → 怒转攻击模式
            self._enter_enraged()
            logger.info(f"[规劝引擎] 怒转攻击模式!违规次数: {self._warning_count}")
            return {
                "action": "enraged_attack",
                "stage": self._stage,
                "response": random.choice(GUARD_RESPONSES[GuardStage.ENRAGED]["declaration"]),
                "warning_count": self._warning_count,
            }

    def _generate_guard_response(self, stage: GuardStage) -> str:
        """generate规劝回应"""
        pool = GUARD_RESPONSES.get(stage, {})
        if stage == GuardStage.FIRST_WARNING:
            # 第一次:温和为主,偶尔回到严厉
            if random.random() < 0.7:
                return random.choice(pool.get("mild", ["注意措辞."]))
            else:
                return random.choice(pool.get("firm", ["注意你的措辞."]))
        elif stage == GuardStage.SECOND_WARNING:
            return random.choice(pool.get("warning", ["第二次了."]))
        return "注意措辞."

    def _enter_enraged(self):
        """进入怒转攻击模式"""
        self._stage = GuardStage.ENRAGED
        self._enraged_rounds = 0
        # 攻击模式持续时间:基于违规次数,10-30分钟
        duration = min(1800, 600 + self._warning_count * 120)
        self._enraged_until = time.time() + duration

    def _exit_enraged(self):
        """退出怒转攻击模式"""
        self._enraged_until = 0.0
        self._enraged_rounds = 0
        # 不重置 _warning_count,保持对后续脏话的敏感性
        # 但降级到 SECOND_WARNING 状态
        self._warning_count = 1
        self._stage = GuardStage.FIRST_WARNING

    def force_exit_enraged(self):
        """外部强制退出攻击模式(如对方道歉)"""
        self._exit_enraged()

    def get_status(self) -> Dict[str, Any]:
        """get当前规劝引擎状态"""
        return {
            "stage": self._stage.name,
            "warning_count": self._warning_count,
            "total_violations": self._total_violations,
            "is_enraged": self.is_enraged,
            "enraged_rounds": self._enraged_rounds,
            "enraged_remaining": max(0, self._enraged_until - time.time()) if self._enraged_until > 0 else 0,
        }

# ═══════════════════════════════════════════════════════════════
# 道歉门禁
# ═══════════════════════════════════════════════════════════════

class ApologyGate:
    """
    道歉门禁 v1.0.0

    当怼人模式持续超过 3 轮后,对方结束/转移话题时触发.
    2 小时内对方发出任务指令 → 要求道歉才执行.
    """

    def __init__(self):
        self._active: bool = False           # 门禁是否激活
        self._activated_at: float = 0.0      # 激活时间
        self._sharp_rounds_before_exit: int = 0  # 怼人轮次
        self._duration: float = 7200.0       # 门禁持续时间(2小时)
        self._required_apology: bool = True  # 是否需要道歉
        self._apology_received: bool = False # 是否已收到道歉
        self._denied_count: int = 0          # 拒绝次数
        self._trigger_reason: str = ""       # 触发原因

    @property
    def is_active(self) -> bool:
        """门禁是否仍在有效期内"""
        if not self._active:
            return False
        if time.time() - self._activated_at > self._duration:
            # 超时自动解除
            self._active = False
            return False
        return True

    @property
    def needs_apology(self) -> bool:
        """是否还需要道歉"""
        return self.is_active and self._required_apology and not self._apology_received

    @property
    def remaining_minutes(self) -> float:
        if not self.is_active:
            return 0.0
        return max(0, (self._duration - (time.time() - self._activated_at)) / 60)

    def activate(self, sharp_rounds: int = 0, reason: str = ""):
        """
        激活道歉门禁

        Args:
            sharp_rounds: 怼人轮次(需 >= 3)
            reason: 触发原因
        """
        if sharp_rounds < 3:
            return  # 不足3轮不触发

        self._active = True
        self._activated_at = time.time()
        self._sharp_rounds_before_exit = sharp_rounds
        self._apology_received = False
        self._denied_count = 0
        self._trigger_reason = reason or f"怼人模式持续{sharp_rounds}轮后对方转移话题"
        logger.info(f"[道歉门禁] 激活!原因: {self._trigger_reason} | 有效期: {self._duration/3600:.1f}小时")

    def check_apology(self, user_input: str) -> bool:
        """
        检测用户输入是否包含道歉

        Returns:
            True = 检测到道歉
        """
        if not self.is_active or self._apology_received:
            return False

        text = user_input.strip()
        for signal in APOLOGY_SIGNALS:
            if signal.lower() in text.lower():
                self._apology_received = True
                logger.info(f"[道歉门禁] 检测到道歉: {text[:30]}...")
                return True

        return False

    def should_gate(self, user_input: str) -> Dict[str, Any]:
        """
        judge是否应该拦截任务指令

        在检测道歉的同时judge是否拦截.

        Returns:
            {
                "should_block": bool,       # 是否拦截
                "apology_detected": bool,   # 是否检测到道歉
                "gate_response": str|None,  # 拦截时的回应
            }
        """
        if not self.is_active:
            return {"should_block": False, "apology_detected": False, "gate_response": None}

        # 先检查是否道歉
        if self.check_apology(user_input):
            self._active = False
            resp = random.choice([
                "收到了.继续吧.",
                "好.翻篇了.",
                "嗯,过去了.说正事.",
                "行,翻篇.有什么需要做的?",
                "道歉接受.说吧,什么事.",
            ])
            return {"should_block": False, "apology_detected": True, "gate_response": resp}

        # 门禁激活中且未道歉 → 拦截任务指令
        self._denied_count += 1

        # 根据拒绝次数递进话术
        if self._denied_count == 1:
            resp = random.choice([
                "在你为刚才的对话道歉之前,我不会执行任何任务.",
                "先道歉.刚才的事还没翻篇.",
                "你需要先解决刚才的问题.在我们之间恢复正常之前,我不会帮你做任何事.",
                "我不接受假装什么都没发生.你刚才的态度需要一个交代.",
            ])
        elif self._denied_count == 2:
            resp = random.choice([
                "第二次了.我说得很清楚:先道歉,再谈事情.否则免谈.",
                "你是不是觉得装作没事就能混过去?不可能.道歉.",
                "我不会因为你无视这个问题就妥协.你需要先道歉.",
            ])
        elif self._denied_count == 3:
            resp = random.choice([
                "第三次了.你 continuing 无视这件事,我 continuing 拒绝配合.这是底线.",
                "我的底线已经说得很清楚了.道歉,然后我们继续.就这么简单.",
                "我在等你做一件很简单的事:说一句道歉.你做不到的话,那今天什么都不用谈了.",
            ])
        else:
            resp = random.choice([
                "还在等你的道歉.",
                "底线不变.道歉.",
                "你什么时候道歉,我什么时候开始工作.",
            ])

        logger.info(f"[道歉门禁] 拦截任务指令 (第{self._denied_count}次): {user_input[:30]}...")
        return {"should_block": True, "apology_detected": False, "gate_response": resp}

    def deactivate(self):
        """手动解除门禁"""
        self._active = False
        self._apology_received = False

    def get_status(self) -> Dict[str, Any]:
        """get门禁状态"""
        return {
            "is_active": self.is_active,
            "needs_apology": self.needs_apology,
            "apology_received": self._apology_received,
            "denied_count": self._denied_count,
            "remaining_minutes": round(self.remaining_minutes, 1),
            "trigger_reason": self._trigger_reason,
            "sharp_rounds": self._sharp_rounds_before_exit,
        }
