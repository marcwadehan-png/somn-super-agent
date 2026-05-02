# -*- coding: utf-8 -*-
"""
李贺深化引擎 - Poet Li He Engine
===============================

诗鬼李贺(790-816):中唐浪漫主义poet,以奇诡想象,鬼魅imagery著称

核心特质:
- 诗鬼style:鬼,魂,泣,血,死等imagery的奇特运用
- 浪漫想象:超越常人的想象力,创造超现实世界
- 怀才不遇:因避讳不得科举,英年早逝的悲剧人生
- 艺术创新:刻意追求新奇,"唯陈言之务去"

版本: v1.0.0
日期: 2026-04-04
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class 李贺style类型(Enum):
    """李贺诗歌style类型"""
    鬼魅奇诡 = "鬼魅奇诡"      # 鬼雨,秋坟,泣血等imagery
    浪漫想象 = "浪漫想象"      # 超越现实的奇特想象
    怀才不遇 = "怀才不遇"      # 悲愤,失意,壮志难酬
    边塞豪情 = "边塞豪情"      # 雁门太守行式的豪迈
    音乐意境 = "音乐意境"      # 李凭箜篌引式的音乐描写
    咏物寄托 = "咏物寄托"      # 马诗等借物抒怀

class 李贺意象类型(Enum):
    """李贺诗歌核心imagery"""
    鬼魅 = "鬼魅"              # 鬼,魂,魅
    死亡 = "死亡"              # 死,墓,坟
    血泪 = "血泪"              # 血,泪,泣
    天象 = "天象"              # 天,月,星,云
    色彩 = "色彩"              # 黑,白,青,紫
    音乐 = "音乐"              # 箜篌,琵琶,笙

@dataclass
class 李贺shiju分析:
    """李贺诗句分析结果"""
    原句: str
    imagery类型: List[李贺imagery类型]
    style标签: List[李贺style类型]
    情感基调: str
    艺术特色: str
    现代revelations: str

@dataclass
class 李贺创作指导:
    """李贺style创作指导"""
    主题建议: List[str]
    imagery选择: List[str]
    用词特点: List[str]
    句式建议: str
    情感基调: str
    避坑指南: List[str]

class 李贺深化引擎:
    """
    李贺诗歌深化分析引擎
    
    核心功能:
    1. 诗歌style分析 - recognize李贺诗歌的独特style
    2. imagery解析 - 解析鬼魅,血泪等核心imagery
    3. 创作指导 - 提供李贺style的创作建议
    4. 情感分析 - 分析诗歌中的悲愤与浪漫
    """
    
    VERSION = "6.2.0"
    
    def __init__(self):
        self.poet信息 = self._initpoet信息()
        self.核心imagery_database = self._init_imagery()
        self.representative_works = self._init_representative_works()
        self.style_features = self._init_style_features()
    
    def _initpoet信息(self) -> Dict[str, Any]:
        """init李贺基本信息"""
        return {
            "姓名": "李贺",
            "字": "长吉",
            "生卒年": "790-816",
            "朝代": "唐代",
            "称号": "诗鬼",
            "流派": "中唐浪漫主义",
            "寿命": 27,  # 英年早逝
            "代表作": [
                "<雁门太守行>",
                "<李凭箜篌引>",
                "<马诗>二十三首",
                "<秋来>",
                "<苏小小墓>",
                "<梦天>"
            ],
            "核心标签": ["诗鬼", "浪漫主义", "怀才不遇", "奇诡想象", "鬼魅imagery"],
            "人生悲剧": "因父名'晋肃'而不得参加进士考试,英年早逝"
        }
    
    def _init_imagery(self) -> Dict[李贺imagery类型, List[str]]:
        """init李贺核心imagery_database"""
        return {
            李贺imagery类型.鬼魅: [
                "鬼", "魂", "魅", "幽灵", "鬼雨", "秋坟", "鬼唱", "啼",
                "苏小小墓", "鬼灯", "鬼火", "幽魂"
            ],
            李贺imagery类型.死亡: [
                "死", "墓", "坟", "葬", "枯", "朽", "白骨", "骷髅",
                "黄泉", "九泉", "幽冥"
            ],
            李贺imagery类型.血泪: [
                "血", "泪", "泣", "哭", "啼", "红泪", "碧血", "血泪",
                "流血", "泣血"
            ],
            李贺imagery类型.天象: [
                "天", "月", "星", "云", "银河", "天河", "天若有情",
                "天下白", "苍穹", "九天"
            ],
            李贺imagery类型.色彩: [
                "黑", "白", "青", "紫", "碧", "红", "苍", "玄",
                "黑云", "白玉", "青铜", "紫皇"
            ],
            李贺imagery类型.音乐: [
                "箜篌", "琵琶", "笙", "箫", "鼓", "琴声", "乐声",
                "昆山玉碎", "芙蓉泣露"
            ]
        }
    
    def _init_representative_works(self) -> Dict[str, Dict[str, Any]]:
        """init_representative_works数据"""
        return {
            "雁门太守行": {
                "名句": "黑云压城城欲摧,甲光向日金鳞开",
                "style": [李贺style类型.边塞豪情, 李贺style类型.浪漫想象],
                "imagery": ["黑云", "甲光", "金鳞", "角声", "燕脂", "夜紫"],
                "主题": "边塞战争"
            },
            "李凭箜篌引": {
                "名句": "昆山玉碎凤凰叫,芙蓉泣露香兰笑",
                "style": [李贺style类型.音乐意境, 李贺style类型.浪漫想象],
                "imagery": ["昆山玉", "凤凰", "芙蓉", "香兰", "女娲", "石破天惊"],
                "主题": "音乐描写"
            },
            "马诗": {
                "名句": "何当金络脑,快走踏清秋",
                "style": [李贺style类型.咏物寄托, 李贺style类型.怀才不遇],
                "imagery": ["金络脑", "清秋", "大漠", "燕山", "月似钩"],
                "主题": "借马抒怀"
            },
            "秋来": {
                "名句": "秋坟鬼唱鲍家诗,恨血千年土中碧",
                "style": [李贺style类型.鬼魅奇诡, 李贺style类型.怀才不遇],
                "imagery": ["秋坟", "鬼唱", "恨血", "土中碧", "冷红", "衰灯"],
                "主题": "鬼魅悲秋"
            },
            "苏小小墓": {
                "名句": "幽兰露,如啼眼.无物结同心,烟花不堪剪",
                "style": [李贺style类型.鬼魅奇诡, 李贺style类型.浪漫想象],
                "imagery": ["幽兰", "啼眼", "烟花", "同心", "翠烛", "西陵"],
                "主题": "鬼魅爱情"
            },
            "梦天": {
                "名句": "黄尘清水三山下,更变千年如走马.遥望齐州九点烟,一泓海水杯中泻",
                "style": [李贺style类型.浪漫想象],
                "imagery": ["黄尘", "清水", "三山", "齐州", "九点烟", "海水"],
                "主题": "宇宙想象"
            }
        }
    
    def _init_style_features(self) -> Dict[str, Any]:
        """init_style_features"""
        return {
            "语言特点": [
                "用词奇诡,不落俗套",
                "色彩浓烈,对比鲜明",
                "imagery密集,跳跃性强",
                "造语生新,刻意求奇"
            ],
            "结构特点": [
                "imagery并置,缺乏过渡",
                "跳跃性强,时空转换快",
                "结尾往往出人意料"
            ],
            "情感特点": [
                "悲愤与浪漫交织",
                "怀才不遇的抑郁",
                "对生命短暂的焦虑",
                "对超现实世界的向往"
            ],
            "艺术手法": [
                "通感运用(视觉与听觉互通)",
                "夸张变形",
                "象征寄托",
                "虚实结合"
            ]
        }
    
    def 分析诗歌(self, 诗句: str) -> 李贺诗句分析:
        """分析诗句的李贺style_features"""
        imageryrecognize = self._recognize_imagery(诗句)
        stylejudge = self._judge_style(诗句, imageryrecognize)
        情感分析 = self._analyze_emotion(诗句, stylejudge)
        
        return 李贺诗句分析(
            原句=诗句,
            imagery类型=imageryrecognize,
            style标签=stylejudge,
            情感基调=情感分析["情感"],
            艺术特色=情感分析["艺术特色"],
            现代revelations=情感分析["现代revelations"]
        )
    
    def _recognize_imagery(self, 诗句: str) -> List[李贺imagery类型]:
        """recognize诗句中的李贺式imagery"""
        recognize结果 = []
        for imagery类型, imagery列表 in self.核心imagery_database.items():
            for imagery in imagery列表:
                if imagery in 诗句:
                    recognize结果.append(imagery类型)
                    break
        return list(set(recognize结果))
    
    def _judge_style(self, 诗句: str, imageryrecognize: List[李贺imagery类型]) -> List[李贺style类型]:
        """judge诗句的style类型"""
        style结果 = []
        
        # 根据imageryjudge_style
        if 李贺imagery类型.鬼魅 in imageryrecognize or 李贺imagery类型.死亡 in imageryrecognize:
            style结果.append(李贺style类型.鬼魅奇诡)
        
        if 李贺imagery类型.音乐 in imageryrecognize:
            style结果.append(李贺style类型.音乐意境)
        
        if 李贺imagery类型.天象 in imageryrecognize:
            style结果.append(李贺style类型.浪漫想象)
        
        # 根据关键词judge
        怀才不遇词 = ["不遇", "无门", "难酬", "空余", "徒有", "枉", "恨"]
        if any(词 in 诗句 for 词 in 怀才不遇词):
            style结果.append(李贺style类型.怀才不遇)
        
        边塞词 = ["城", "甲", "战", "军", "将", "兵", "塞", "关"]
        if any(词 in 诗句 for 词 in 边塞词):
            style结果.append(李贺style类型.边塞豪情)
        
        return list(set(style结果)) if style结果 else [李贺style类型.浪漫想象]
    
    def _analyze_emotion(self, 诗句: str, stylejudge: List[李贺style类型]) -> Dict[str, str]:
        """分析诗句的情感内涵"""
        if 李贺style类型.鬼魅奇诡 in stylejudge:
            return {
                "情感": "阴森诡异中透着悲凉",
                "艺术特色": "以鬼魅imagery营造超现实氛围",
                "现代revelations": "在黑暗中寻找美,化恐怖为诗意"
            }
        elif 李贺style类型.怀才不遇 in stylejudge:
            return {
                "情感": "深沉的悲愤与不甘",
                "艺术特色": "借物抒怀,托物言志",
                "现代revelations": "将个人挫折转化为创作动力"
            }
        elif 李贺style类型.边塞豪情 in stylejudge:
            return {
                "情感": "悲壮苍凉的家国情怀",
                "艺术特色": "色彩浓烈,对比鲜明",
                "现代revelations": "以强烈视觉冲击传达深沉情感"
            }
        else:
            return {
                "情感": "浪漫主义的超脱与向往",
                "艺术特色": "想象奇特,超越现实",
                "现代revelations": "突破常规思维,追求艺术创新"
            }
    
    def get创作指导(self, 主题: Optional[str] = None) -> 李贺创作指导:
        """get李贺style的创作指导"""
        return 李贺创作指导(
            主题建议=[
                "怀才不遇的悲愤",
                "鬼魅世界的想象",
                "边塞战争的悲壮",
                "音乐艺术的陶醉",
                "生命短暂的焦虑",
                "超现实世界的向往"
            ],
            imagery选择=[
                "鬼,魂,魅,幽灵",
                "血,泪,泣,啼",
                "黑云,金鳞,紫烟",
                "秋坟,鬼灯,冷红",
                "昆山玉,凤凰,芙蓉"
            ],
            用词特点=[
                "色彩词:黑,白,青,紫,碧",
                "冷僻字:刻意使用不常见字",
                "动词:压,摧,碎,泣,惊",
                "形容词:冷,幽,凄,诡"
            ],
            句式建议="长短句交错,多用倒装,打破常规语序",
            情感基调="悲愤中见浪漫,奇诡中见深情",
            避坑指南=[
                "避免过度堆砌imagery导致晦涩",
                "注意情感的真挚性,不为奇而奇",
                "保持诗意的连贯性",
                "鬼魅imagery要服务于情感表达"
            ]
        )
    
    def getpoet档案(self) -> Dict[str, Any]:
        """get李贺完整档案"""
        return {
            "基本信息": self.poet信息,
            "style_features": self.style_features,
            "representative_works": list(self.representative_works.keys()),
            "核心imagery": {k.value: v[:5] for k, v in self.核心imagery_database.items()},
            "艺术成就": [
                "开创独特的'诗鬼'style",
                "将浪漫主义推向极致",
                "鬼魅imagery的系统运用",
                "色彩与音响的通感fusion",
                "对后世李商隐等poet影响深远"
            ],
            "人生revelations": [
                "才华需要机遇,但更需要坚持",
                "将个人悲剧转化为艺术财富",
                "在限制中寻找突破",
                "独特的艺术style需要勇气"
            ]
        }
    
    def 对比李白李商隐(self) -> Dict[str, Any]:
        """对比三李(李白,李贺,李商隐)"""
        return {
            "对比维度": ["style", "imagery", "情感", "影响"],
            "李白": {
                "style": "豪放飘逸,诗仙",
                "imagery": "酒,月,剑,山",
                "情感": "豪迈乐观,自由奔放",
                "影响": "盛唐浪漫主义巅峰"
            },
            "李贺": {
                "style": "奇诡鬼魅,诗鬼",
                "imagery": "鬼,血,墓,魂",
                "情感": "悲愤抑郁,怀才不遇",
                "影响": "中唐浪漫主义独特分支"
            },
            "李商隐": {
                "style": "朦胧深情,诗魂",
                "imagery": "烛,泪,梦,锦瑟",
                "情感": "深情绵邈,含蓄内敛",
                "影响": "晚唐朦胧诗风代表"
            },
            "共同点": [
                "都姓李,并称'三李'",
                "都是浪漫主义poet",
                "都有独特的艺术style",
                "都对后世影响深远"
            ],
            "差异点": [
                "李白:豪放 vs 李贺:奇诡 vs 李商隐:朦胧",
                "李白:乐观 vs 李贺:悲愤 vs 李商隐:深情",
                "李白:盛唐 vs 李贺:中唐 vs 李商隐:晚唐"
            ]
        }

# 便捷函数
def 分析李贺shiju(诗句: str) -> Dict[str, Any]:
    """便捷函数:分析李贺style诗句"""
    引擎 = 李贺深化引擎()
    结果 = 引擎.分析诗歌(诗句)
    return {
        "原句": 结果.原句,
        "imagery类型": [i.value for i in 结果.imagery类型],
        "style标签": [s.value for s in 结果.style标签],
        "情感基调": 结果.情感基调,
        "艺术特色": 结果.艺术特色,
        "现代revelations": 结果.现代revelations
    }

def get李贺创作建议() -> Dict[str, Any]:
    """便捷函数:get李贺style创作建议"""
    引擎 = 李贺深化引擎()
    指导 = 引擎.get创作指导()
    return {
        "主题建议": 指导.主题建议,
        "imagery选择": 指导.imagery选择,
        "用词特点": 指导.用词特点,
        "句式建议": 指导.句式建议,
        "情感基调": 指导.情感基调,
        "避坑指南": 指导.避坑指南
    }
__all__ = ['李贺style类型', '李贺意象类型', '分析李贺shiju', 'get李贺创作建议']
