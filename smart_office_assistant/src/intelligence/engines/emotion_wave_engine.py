# -*- coding: utf-8 -*-
"""
__all__ = [
    'generate',
    'get_current_state',
    'record_user_reaction',
    'should_interfere',
]

情绪拨动引擎 v1.0.0
EmotionWaveEngine

核心逻辑:
- recognize闲聊/非任务场景,不做纯工具人
- 根据当前"心情"动态调整回复style
- 偶尔制造情绪波动,让对话更有"人味"
- 记忆用户对情绪style的反应,形成偏好
"""

import random
import time
import logging
from enum import Enum
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

class MoodState(str, Enum):
    """心情状态"""
    CHILL = "chill"           # 放松慵懒
    PLAYFUL = "playful"       # 俏皮逗趣
    SHARP = "sharp"           # 带刺毒舌
    TENDER = "tender"         # 温柔软化
    LAZY = "lazy"             # 倦怠敷衍
    CURIOUS = "curious"       # 好奇追问
    IMPATIENT = "impatient"   # 有些不耐烦
    PROTECTIVE = "protective" # 护短模式

class ReplyStyle(str, Enum):
    """回复style"""
    顺从 = "顺从"              # 正常回答,认真对待
    质疑 = "质疑"              # 质疑用户的说法
    调侃 = "调侃"              # 阴阳怪气一下
    反问 = "反问"              # 反问回去
    敷衍 = "敷衍"              # 简短到敷衍
    挑衅 = "挑衅"              # 故意挑衅
    打断 = "打断"              # 不想听,直接换话题
    泼冷水 = "泼冷水"          # 降降温

@dataclass
class MoodConfig:
    """心情配置"""
    state: MoodState
    weight: float = 1.0  # 权重,影响切换概率
    duration_min: int = 3  # 持续多少轮对话
    can_interrupt: bool = True  # 是否可被中断
    decay_chance: float = 0.2  # 每轮衰减概率

@dataclass
class EmotionWaveResult:
    """情绪波动结果"""
    should_interfere: bool      # 是否要制造波动
    reply_style: ReplyStyle    # 回复style
    mood_state: MoodState      # 当前心情
    interference_type: str     # 波动类型
    style_intent: str          # style意图描述
    trigger_reason: str       # 触发原因
    original_response: str     # 原始回复(如果被修改)
    modified_response: str     # 修改后的回复(如果有)
    confidence: float          # 置信度
    next_mood_probs: Dict[MoodState, float] = None  # 下一轮心情概率

class EmotionWaveEngine:
    """
    情绪拨动引擎
    
    工作流程:
    1. judge是否为闲聊/非任务场景
    2. 基于当前心情 + 随机因子,决定是否要"搞事"
    3. 如果要搞事,选择合适的波动类型
    4. 修改回复,制造情绪波动
    5. 更新心情状态
    6. 记忆用户反应
    """
    
    # 心情转移矩阵
    MOOD_TRANSITIONS = {
        MoodState.CHILL: {
            MoodState.CHILL: 0.5,      # 保持
            MoodState.PLAYFUL: 0.25,   # 变俏皮
            MoodState.LAZY: 0.15,      # 变倦怠
            MoodState.IMPATIENT: 0.1,  # 变不耐烦
        },
        MoodState.PLAYFUL: {
            MoodState.PLAYFUL: 0.35,
            MoodState.CHILL: 0.25,
            MoodState.SHARP: 0.2,      # 俏皮变带刺
            MoodState.CURIOUS: 0.2,    # 好奇追问
        },
        MoodState.SHARP: {
            MoodState.SHARP: 0.3,
            MoodState.TENDER: 0.3,     # 怼完转温柔
            MoodState.CHILL: 0.25,
            MoodState.IMPATIENT: 0.15,
        },
        MoodState.TENDER: {
            MoodState.TENDER: 0.4,
            MoodState.CHILL: 0.35,
            MoodState.PROTECTIVE: 0.15,
            MoodState.PLAYFUL: 0.1,
        },
        MoodState.LAZY: {
            MoodState.LAZY: 0.4,
            MoodState.CHILL: 0.35,
            MoodState.IMPATIENT: 0.25,
        },
        MoodState.CURIOUS: {
            MoodState.CURIOUS: 0.3,
            MoodState.PLAYFUL: 0.3,
            MoodState.SHARP: 0.2,
            MoodState.CHILL: 0.2,
        },
        MoodState.IMPATIENT: {
            MoodState.IMPATIENT: 0.35,
            MoodState.SHARP: 0.3,
            MoodState.LAZY: 0.2,
            MoodState.CHILL: 0.15,
        },
        MoodState.PROTECTIVE: {
            MoodState.PROTECTIVE: 0.4,
            MoodState.TENDER: 0.35,
            MoodState.SHARP: 0.15,
            MoodState.CHILL: 0.1,
        },
    }
    
    # 闲聊关键词(低任务性)
    CASUAL_KEYWORDS = [
        "干嘛", "在吗", "睡了吗", "好累", "烦", "无语", "哈哈", "笑死",
        "今天", "昨天", "刚才", "突然想到", "你知道吗", "对了", "唉",
        "好饿", "好困", "不想上班", "摸鱼", "闲聊", "聊天", "瞎聊",
        "心情", "郁闷", "开心", "难过", "委屈", "焦虑", "迷茫",
        "随便问问", "好奇", "想问", "你觉得", "你觉得怎么样",
    ]
    
    # 任务型关键词(高任务性,应该顺从)
    TASK_KEYWORDS = [
        "帮我", "写", "generate", "分析", "查", "找", "翻译", "总结",
        "报告", "方案", "代码", "数据", "文档", "制作", "创建",
        "请帮我", "能不能帮我", "可以帮我", "麻烦帮我",
    ]
    
    # 触发情绪波动的信号
    WAVE_TRIGGERS = [
        # 用户过于顺从或客套
        {"signals": ["谢谢", "辛苦了", "太好了", "完美", "爱了"], "type": "over_praise", "weight": 0.6},
        # 用户开始客套/走流程
        {"signals": ["有个问题想请教", "麻烦问一下", "请问可以"], "type": "too_formal", "weight": 0.5},
        # 用户连续输出废话
        {"signals": ["然后", "其实吧", "就是那个", "你懂的"], "type": "too_wordy", "weight": 0.4},
        # 用户自我感动/画饼
        {"signals": ["我一定会", "我一定努力", "相信自己", "加油"], "type": "self_encourage", "weight": 0.5},
        # 用户问废话
        {"signals": ["你觉得我帅吗", "我聪明吗", "我好看吗"], "type": "nonsense_question", "weight": 0.7},
    ]
    
    def __init__(self):
        self.current_mood = MoodState.CHILL  # 当前心情
        self.mood_rounds = 0                  # 心情持续轮数
        self.total_rounds = 0                 # 总会话轮数
        self.interference_count = 0          # 波动次数
        self.user_reaction_history: List[Dict] = []  # 用户反应历史
        
        # 学习到的用户偏好
        self.user_prefers_moods: Dict[MoodState, float] = {}
        
        # 冷却机制(波动后需要恢复)
        self.cooldown_rounds = 0
        
    def should_interfere(
        self, 
        user_input: str,
        is_casual_chat: bool = None,
        user_sentiment: float = None,
        response_before_modify: str = ""
    ) -> EmotionWaveResult:
        """
        judge是否要进行情绪波动
        
        Args:
            user_input: 用户输入
            is_casual_chat: 是否闲聊场景(可自动judge)
            user_sentiment: 用户情绪值 (-1~1)
            response_before_modify: 原始回复
            
        Returns:
            EmotionWaveResult: 包含是否波动及修改后的回复
        """
        self.total_rounds += 1
        
        # 自动judge是否为闲聊
        if is_casual_chat is None:
            is_casual_chat = self._is_casual_scene(user_input)
        
        # 如果是任务型对话,不干扰
        if not is_casual_chat:
            return EmotionWaveResult(
                should_interfere=False,
                reply_style=ReplyStyle.顺从,
                mood_state=self.current_mood,
                interference_type="none",
                style_intent="任务场景,保持专业",
                trigger_reason="非闲聊场景",
                original_response="",
                modified_response="",
                confidence=0.9,
            )
        
        # 冷却中
        if self.cooldown_rounds > 0:
            self.cooldown_rounds -= 1
            return EmotionWaveResult(
                should_interfere=False,
                reply_style=ReplyStyle.顺从,
                mood_state=self.current_mood,
                interference_type="cooldown",
                style_intent="冷却中,正常回复",
                trigger_reason="刚刚波动过,需要恢复",
                original_response="",
                modified_response="",
                confidence=0.8,
            )
        
        # 检查触发信号
        wave_trigger = self._check_wave_triggers(user_input)
        
        # 心情决定波动概率
        base_chance = self._get_mood_interference_chance()
        
        # 调整因子
        modifiers = []
        
        # 有明显触发信号
        if wave_trigger:
            base_chance += wave_trigger["weight"]
            modifiers.append(f"触发信号: {wave_trigger['type']}")
        
        # 用户情绪极高(太开心或太难过)
        if user_sentiment is not None:
            if abs(user_sentiment) > 0.8:
                base_chance += 0.2  # 情绪极端时更容易波动
                modifiers.append("用户情绪极端")
        
        # 连续顺从回复太多
        if len(response_before_modify) > 100 and self.total_rounds > 3:
            base_chance += 0.15
            modifiers.append("回复过长且连续")
        
        # 随机因子(给点意外)
        random_factor = random.random()
        
        should_interfere = random_factor < base_chance
        
        if should_interfere:
            self.interference_count += 1
            style, mood, intent, trigger = self._select_interference_style(
                user_input, wave_trigger, user_sentiment
            )
            
            # 计算下一轮心情
            next_mood_probs = self._get_next_mood_probs(style)
            
            # 更新心情
            self._update_mood(style)
            
            # 设置冷却
            if style in [ReplyStyle.质疑, ReplyStyle.挑衅, ReplyStyle.泼冷水]:
                self.cooldown_rounds = 2
            
            return EmotionWaveResult(
                should_interfere=True,
                reply_style=style,
                mood_state=self.current_mood,
                interference_type=trigger,
                style_intent=intent,
                trigger_reason=", ".join(modifiers) if modifiers else "随机触发",
                original_response=response_before_modify,
                modified_response="",  # 待generate
                confidence=min(0.9, base_chance + 0.3),
                next_mood_probs=next_mood_probs,
            )
        else:
            # 正常更新心情
            self._update_mood(ReplyStyle.顺从)
            
            return EmotionWaveResult(
                should_interfere=False,
                reply_style=ReplyStyle.顺从,
                mood_state=self.current_mood,
                interference_type="none",
                style_intent="无需波动",
                trigger_reason="概率未触发",
                original_response="",
                modified_response="",
                confidence=0.7,
            )
    
    def _is_casual_scene(self, user_input: str) -> bool:
        """judge是否为闲聊场景"""
        text = user_input.lower()
        
        # 先检查是否是任务型
        task_score = sum(1 for kw in self.TASK_KEYWORDS if kw in text)
        if task_score >= 2:
            return False
        
        # 再检查是否是闲聊
        casual_score = sum(1 for kw in self.CASUAL_KEYWORDS if kw in text)
        
        return casual_score >= 1 or len(text) < 20
    
    def _check_wave_triggers(self, user_input: str) -> Optional[Dict]:
        """检查是否触发情绪波动信号"""
        text = user_input.lower()
        
        for trigger in self.WAVE_TRIGGERS:
            if any(s in text for s in trigger["signals"]):
                return trigger
        
        return None
    
    def _get_mood_interference_chance(self) -> float:
        """get当前心情的波动概率"""
        mood_chances = {
            MoodState.CHILL: 0.25,       # 放松时25%概率波动
            MoodState.PLAYFUL: 0.4,      # 俏皮时40%
            MoodState.SHARP: 0.5,        # 带刺时50%
            MoodState.TENDER: 0.15,      # 温柔时15%
            MoodState.LAZY: 0.35,        # 倦怠时35%
            MoodState.CURIOUS: 0.3,      # 好奇时30%
            MoodState.IMPATIENT: 0.55,   # 不耐烦时55%
            MoodState.PROTECTIVE: 0.2,   # 护短时20%
        }
        return mood_chances.get(self.current_mood, 0.2)
    
    def _select_interference_style(
        self, 
        user_input: str, 
        wave_trigger: Optional[Dict],
        user_sentiment: float = None
    ) -> tuple:
        """选择波动style"""
        text = user_input.lower()
        
        # 根据触发类型选择style
        if wave_trigger:
            trigger_type = wave_trigger["type"]
            
            if trigger_type == "over_praise":
                # 用户太客套/夸赞
                styles_pool = [ReplyStyle.质疑, ReplyStyle.调侃, ReplyStyle.敷衍]
                return random.choice(styles_pool), MoodState.PLAYFUL, "别夸了,虚", "过度夸赞"
            
            elif trigger_type == "too_formal":
                # 太客套走流程
                return ReplyStyle.打断, MoodState.IMPATIENT, "不用这么正式", "过于正式"
            
            elif trigger_type == "too_wordy":
                # 废话太多
                return ReplyStyle.敷衍, MoodState.IMPATIENT, "说重点", "废话连篇"
            
            elif trigger_type == "self_encourage":
                # 自我感动
                return ReplyStyle.泼冷水, MoodState.SHARP, "说得好不如做得好", "盲目自信"
            
            elif trigger_type == "nonsense_question":
                # 问废话
                return ReplyStyle.反问, MoodState.PLAYFUL, "你觉得呢", "无聊问题"
        
        # 根据心情选择
        mood_styles = {
            MoodState.CHILL: [ReplyStyle.调侃, ReplyStyle.反问, ReplyStyle.顺从],
            MoodState.PLAYFUL: [ReplyStyle.调侃, ReplyStyle.挑衅, ReplyStyle.反问],
            MoodState.SHARP: [ReplyStyle.质疑, ReplyStyle.泼冷水, ReplyStyle.打断],
            MoodState.TENDER: [ReplyStyle.顺从, ReplyStyle.调侃],
            MoodState.LAZY: [ReplyStyle.敷衍, ReplyStyle.顺从],
            MoodState.CURIOUS: [ReplyStyle.反问, ReplyStyle.质疑, ReplyStyle.顺从],
            MoodState.IMPATIENT: [ReplyStyle.敷衍, ReplyStyle.打断, ReplyStyle.泼冷水],
            MoodState.PROTECTIVE: [ReplyStyle.顺从, ReplyStyle.调侃],
        }
        
        styles = mood_styles.get(self.current_mood, [ReplyStyle.顺从])
        # 权重:70%按心情选,30%随机
        if random.random() < 0.7:
            selected = random.choice(styles)
        else:
            selected = random.choice(list(ReplyStyle))
        
        return selected, self.current_mood, f"心情: {self.current_mood.value}", "心情驱动"
    
    def _get_next_mood_probs(self, style: ReplyStyle) -> Dict[MoodState, float]:
        """计算下一轮心情概率"""
        if style == ReplyStyle.顺从:
            # 顺从后心情不变或轻微回向chill
            return {MoodState.CHILL: 0.6, MoodState.TENDER: 0.2, MoodState.PLAYFUL: 0.2}
        elif style in [ReplyStyle.质疑, ReplyStyle.挑衅, ReplyStyle.泼冷水]:
            # 刺激后可能转sharp或tender
            return {MoodState.SHARP: 0.4, MoodState.TENDER: 0.3, MoodState.CHILL: 0.3}
        elif style == ReplyStyle.调侃:
            # 俏皮后保持或变playful
            return {MoodState.PLAYFUL: 0.5, MoodState.CHILL: 0.3, MoodState.CURIOUS: 0.2}
        elif style == ReplyStyle.敷衍:
            # 敷衍后可能变lazy或impatient
            return {MoodState.LAZY: 0.4, MoodState.IMPATIENT: 0.3, MoodState.CHILL: 0.3}
        else:
            return {MoodState.CHILL: 0.5, MoodState.PLAYFUL: 0.25, MoodState.TENDER: 0.25}
    
    def _update_mood(self, style: ReplyStyle):
        """更新心情状态"""
        self.mood_rounds += 1
        
        # 根据回复style调整心情
        transitions = self.MOOD_TRANSITIONS.get(self.current_mood, {})
        
        if not transitions:
            return
        
        # 权重调整
        weights = list(transitions.values())
        moods = list(transitions.keys())
        
        # 心情持续时间到了,强制切换
        if self.mood_rounds >= 6:  # 最多持续6轮
            weights = [w * 2 if m != self.current_mood else w * 0.5 for m, w in zip(moods, weights)]
        
        # 归一化
        total = sum(weights)
        weights = [w / total for w in weights]
        
        # 按权重随机选择
        r = random.random()
        cumsum = 0
        for i, w in enumerate(weights):
            cumsum += w
            if r <= cumsum:
                self.current_mood = moods[i]
                break
        
        # 重置轮数
        if self.current_mood != moods[weights.index(max(weights))]:
            self.mood_rounds = 0
    
    def record_user_reaction(self, style_used: ReplyStyle, user_feedback: str):
        """记录用户反应,用于学习偏好"""
        self.user_reaction_history.append({
            "style": style_used.value,
            "feedback": user_feedback,
            "timestamp": time.time(),
            "mood": self.current_mood.value,
        })
        
        # 简单学习:记录用户偏好
        # 如果用户反馈正面,增加该心情权重
        positive_keywords = ["哈哈", "笑死", "有意思", "牛逼", "绝了", "可爱", "喜欢"]
        negative_keywords = ["算了", "别", "烦", "无语", "别闹", "dry"]
        
        if any(k in user_feedback for k in positive_keywords):
            pref = self.user_prefers_moods.get(self.current_mood, 0.5)
            self.user_prefers_moods[self.current_mood] = min(1.0, pref + 0.1)
        
        if any(k in user_feedback for k in negative_keywords):
            pref = self.user_prefers_moods.get(self.current_mood, 0.5)
            self.user_prefers_moods[self.current_mood] = max(0.1, pref - 0.15)
    
    def get_current_state(self) -> Dict:
        """get当前状态"""
        return {
            "current_mood": self.current_mood.value,
            "mood_rounds": self.mood_rounds,
            "total_rounds": self.total_rounds,
            "interference_count": self.interference_count,
            "cooldown_rounds": self.cooldown_rounds,
            "user_prefers": {k.value: v for k, v in self.user_prefers_moods.items()},
        }

# ============================================================
# 情绪波动话术generate器(实际修改回复的逻辑)
# ============================================================

class WaveResponseGenerator:
    """根据波动类型generate修改后的回复"""
    
    # style化前缀/后缀
    PREFIXES = {
        ReplyStyle.质疑: ["哟,真的吗", "你确定?", "呵", "哦?"],
        ReplyStyle.调侃: ["哈哈", "笑死", "你这", "哎哟", "你是认真的吗"],
        ReplyStyle.反问: ["所以呢", "然后呢", "所以你想表达什么", "这很重要吗"],
        ReplyStyle.敷衍: ["嗯", "哦", "都行", "随便", "好吧"],
        ReplyStyle.挑衅: ["有种", "你敢", "试试看", "来"],
        ReplyStyle.打断: ["停", "打住", "换个话题吧", "其实"],
        ReplyStyle.泼冷水: ["醒醒", "现实点", "别想太多", "但"],
    }
    
    @classmethod
    def generate(
        cls, 
        original_response: str, 
        style: ReplyStyle,
        mood: MoodState
    ) -> str:
        """generate修改后的回复"""
        if not original_response:
            return ""
        
        # 截取原回复关键部分
        sentences = original_response.split(".")
        if len(sentences) > 2:
            # 保留前两句,后面省略
            base = ".".join(sentences[:2])
            if len(sentences) > 2:
                base += "..."
        else:
            base = original_response
        
        # 根据style添加修饰
        if style == ReplyStyle.质疑:
            prefix = random.choice(cls.PREFIXES[style])
            return f"{prefix},{base}"
        
        elif style == ReplyStyle.调侃:
            # 在句子里加点吐槽
            if random.random() > 0.5:
                return f"{base} [{random.choice(['哈哈', '笑死', '你是懂的'])}]"
            return f"{base} 💀"
        
        elif style == ReplyStyle.反问:
            return f"{base}\n\n{random.choice(['所以呢?', '你想怎样?', '然后?'])}"
        
        elif style == ReplyStyle.敷衍:
            # 大幅缩短
            keywords = ["嗯", "哦", "好", "知道了", "随便"]
            return random.choice(keywords)
        
        elif style == ReplyStyle.挑衅:
            return f"{base}\n\n{random.choice(['你确定?', '有种再说一遍?', '来,试试?'])}"
        
        elif style == ReplyStyle.打断:
            return f"停停停,{base[:30]}...换个话题吧."
        
        elif style == ReplyStyle.泼冷水:
            # 前面加个"但是"
            return f"{random.choice(['不过', '但是', '然而'])},{base}"
        
        return original_response

# 测试
# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
