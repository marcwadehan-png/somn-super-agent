# -*- coding: utf-8 -*-
"""
__all__ = [
    'assess_minimalism_level',
    'create_focus_plan',
    'create_minimalist_system',
    'declutter_area',
    'essentialism_checklist',
    'get_focus_analytics',
    'get_minimalism_quotes',
    'identify_distractions',
    'record_focus_session',
    'to_dict',
]

极简专注系统 v1.0.0
Minimalist Focus System

基于<极简主义><大脑整理术>核心思想构建

核心思想:
- 极简不是苦行,而是找到真正重要的
- 专注是有限资源的最佳配置
- 少即是多,简化才能深化
- 断舍离是通往自由的路径

作者:Somn AI
版本:v1.0.0
日期:2026-04-02
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from collections import defaultdict
import re

class MinimalismLevel(Enum):
    """极简程度"""
    ACCUMULATOR = "囤积型"  # 什么都舍不得扔
    SELECTIVE = "选择型"  # 有选择地保留
    ESSENTIALIST = "本质型"  # 只保留真正重要的
    MONK = "修行型"  # 极度精简

class DeclutterArea(Enum):
    """整理领域"""
    PHYSICAL = "物理空间"  # 物品,环境
    DIGITAL = "数字空间"  # 文件,邮件,应用
    MENTAL = "精神空间"  # 思想,信念
    SCHEDULE = "时间安排"  # 日程,承诺
    RELATIONSHIPS = "人际关系"  # 社交圈

class FocusBarrier(Enum):
    """专注障碍"""
    EXTERNAL = "外部干扰"  # 通知,他人打断
    INTERNAL = "内部干扰"  # 思绪,情绪
    ENVIRONMENTAL = "环境干扰"  # 杂乱,噪音
    HABITUAL = "习惯性"  # 拖延,多任务

@dataclass
class DeclutterResult:
    """整理结果"""
    area: DeclutterArea
    items_removed: List[str]
    items_retained: List[str]
    space_freed: str  # 释放的空间
    emotional_relief: float  # 心理释放感 (0-100)
    
    def to_dict(self) -> Dict:
        return {
            "area": self.area.value,
            "items_removed_count": len(self.items_removed),
            "items_retained_count": len(self.items_retained),
            "space_freed": self.space_freed,
            "emotional_relief": round(self.emotional_relief, 1)
        }

@dataclass
class FocusSession:
    """专注时段"""
    duration_minutes: int
    distractions: int
    interruptions: int
    completion_rate: float  # 完成度 0-1
    quality_score: float  # 专注质量 0-100

class MinimalistFocusSystem:
    """
    极简专注系统
    
    基于<极简主义>和<大脑整理术>构建,帮助用户:
    1. 简化物理和数字空间
    2. 减少精神负担
    3. 提升专注力
    4. 找到真正重要的事
    
    主要功能:
    1. 极简程度评估
    2. 整理指导
    3. 专注力训练
    4. 时间极简化
    """
    
    # 极简主义关键词
    MINIMALISM_KEYWORDS = {
        "必要": 2, "需要": 1, "重要": 2, "经常用": 1,
        "有用": 1, "美": 1, "情感价值": 2, "纪念": 1,
        "可能有用": -1, "以后": -1, "舍不得": -1, "万一": -1,
        "太多": -2, "杂乱": -2, "闲置": -1
    }
    
    # 专注障碍关键词
    DISTRACTION_KEYWORDS = {
        FocusBarrier.EXTERNAL: ["通知", "消息", "邮件", "电话", "同事"],
        FocusBarrier.INTERNAL: ["想", "担心", "焦虑", "杂念", "走神"],
        FocusBarrier.ENVIRONMENTAL: ["乱", "吵", "光线", "温度", "不舒服"],
        FocusBarrier.HABITUAL: ["拖延", "等会", "刷", "逛", "多任务"]
    }
    
    # 极简原则
    MINIMALISM_PRINCIPLES = {
        "physical": [
            "如果一年没用过,扔掉或送人",
            "每买一件新的,扔掉或送出一件旧的",
            "保持表面无杂物",
            "物归原位"
        ],
        "digital": [
            "每天清空一次收件箱",
            "文件夹不超过三层",
            "删除不用的应用",
            "定期清理照片和文件"
        ],
        "mental": [
            "只保留能激发热情的想法",
            "质疑每个信念:这真的是事实吗?",
            "放下对过去的执念",
            "不要为小事消耗精力"
        ],
        "schedule": [
            "每天留出空白时间",
            "说不需要每周说不",
            "一个时间段只做一件事",
            "设定截止日期"
        ],
        "relationships": [
            "远离消耗你的人",
            "深度交流胜于泛泛之交",
            "删除社交媒体假朋友",
            "珍惜真正的支持者"
        ]
    }
    
    def __init__(self):
        self.focus_sessions: List[FocusSession] = []
        self.declutter_history: List[DeclutterResult] = []
        self.focus_streak: int = 0
    
    def assess_minimalism_level(self, text: str = "") -> Dict:
        """
        评估极简程度
        
        Args:
            text: 关于生活习惯的描述
            
        Returns:
            Dict: 极简程度评估
        """
        if not text:
            return {
                "level": MinimalismLevel.SELECTIVE.value,
                "score": 50,
                "advice": "建议开始有意识地简化生活"
            }
        
        text_lower = text.lower()
        score = 50
        
        for keyword, weight in self.MINIMALISM_KEYWORDS.items():
            if keyword in text_lower:
                score += weight * 10
        
        score = max(0, min(100, score))
        
        # 确定极简程度
        if score < 30:
            level = MinimalismLevel.ACCUMULATOR
        elif score < 60:
            level = MinimalismLevel.SELECTIVE
        elif score < 85:
            level = MinimalismLevel.ESSENTIALIST
        else:
            level = MinimalismLevel.MONK
        
        return {
            "level": level.value,
            "score": round(score, 1),
            "characteristics": self._get_level_characteristics(level),
            "advice": self._get_level_advice(level)
        }
    
    def _get_level_characteristics(self, level: MinimalismLevel) -> List[str]:
        """get程度characteristics"""
        chars = {
            MinimalismLevel.ACCUMULATOR: [
                "家里物品很多,难以找到东西",
                "数字空间杂乱,文件堆积",
                "日程过满,没有空闲时间",
                "人际关系广泛但深度不够"
            ],
            MinimalismLevel.SELECTIVE: [
                "会定期整理,但整理不够彻底",
                "有整理的意愿但action力不足",
                "开始思考什么是真正重要的"
            ],
            MinimalismLevel.ESSENTIALIST: [
                "生活空间简洁有序",
                "时间安排合理有度",
                "人际关系精简但深厚",
                "专注力强,能做深度工作"
            ],
            MinimalismLevel.MONK: [
                "拥有极少物品",
                "极简到影响生活质量",
                "可能过于追求极简而忽略实用"
            ]
        }
        return chars.get(level, [])
    
    def _get_level_advice(self, level: MinimalismLevel) -> str:
        """get程度建议"""
        advices = {
            MinimalismLevel.ACCUMULATOR: "从一个小角落开始,不要试图一次性整理所有",
            MinimalismLevel.SELECTIVE: "设定每月整理目标,有计划地精简",
            MinimalismLevel.ESSENTIALIST: "保持现状,警惕新物品的入侵",
            MinimalismLevel.MONK: "确保基本需求满足,极简是为了自由而非束缚"
        }
        return advices.get(level, "继续探索适合自己的极简程度")
    
    def declutter_area(self, area: DeclutterArea, items: List[str]) -> DeclutterResult:
        """
        整理指定领域
        
        Args:
            area: 整理领域
            items: 待整理的物品/项目列表
            
        Returns:
            DeclutterResult: 整理结果
        """
        kept = []
        removed = []
        
        for item in items:
            if self._should_keep(item, area):
                kept.append(item)
            else:
                removed.append(item)
        
        result = DeclutterResult(
            area=area,
            items_removed=removed,
            items_retained=kept,
            space_freed=self._estimate_space_freed(area, len(removed)),
            emotional_relief=min(100, len(removed) * 5 + 30)
        )
        
        self.declutter_history.append(result)
        return result
    
    def _should_keep(self, item: str, area: DeclutterArea) -> bool:
        """judge是否保留"""
        item_lower = item.lower()
        
        # 保留标准
        keep_criteria = ["必要", "经常", "重要", "喜欢", "需要"]
        remove_criteria = ["一年没", "不记得", "坏了", "重复", "闲置"]
        
        keep_score = sum(10 for c in keep_criteria if c in item_lower)
        remove_score = sum(15 for c in remove_criteria if c in item_lower)
        
        # 领域特定规则
        if area == DeclutterArea.PHYSICAL:
            if "礼物" in item_lower or "纪念" in item_lower:
                keep_score += 5
        
        if area == DeclutterArea.DIGITAL:
            if "未读" in item_lower:
                remove_score += 20
        
        return keep_score >= remove_score
    
    def _estimate_space_freed(self, area: DeclutterArea, count: int) -> str:
        """估算释放空间"""
        estimates = {
            DeclutterArea.PHYSICAL: f"约{count * 0.5:.1f}平方米空间",
            DeclutterArea.DIGITAL: f"约{count * 100:.0f}MB存储",
            DeclutterArea.MENTAL: f"减少约{count * 5:.0f}%精神负担",
            DeclutterArea.SCHEDULE: f"每周约{count * 0.5:.1f}小时空闲",
            DeclutterArea.RELATIONSHIPS: f"约{count * 2:.0f}个消耗性关系"
        }
        return estimates.get(area, f"约{count}项")
    
    def identify_distractions(self, work_description: str) -> Dict:
        """
        recognize专注障碍
        
        Args:
            work_description: 工作/学习环境描述
            
        Returns:
            Dict: 专注障碍分析
        """
        barriers = defaultdict(list)
        text_lower = work_description.lower()
        
        for barrier_type, keywords in self.DISTRACTION_KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    barriers[barrier_type].append(kw)
        
        return {
            "barriers_found": {k.value: v for k, v in barriers.items()},
            "dominant_barrier": self._get_dominant_barrier(barriers),
            "solutions": self._get_barrier_solutions(barriers)
        }
    
    def _get_dominant_barrier(self, barriers: defaultdict) -> str:
        """get主要障碍"""
        if not barriers:
            return "未发现明显障碍"
        
        max_barrier = max(barriers.items(), key=lambda x: len(x[1]))
        return max_barrier[0].value
    
    def _get_barrier_solutions(self, barriers: defaultdict) -> Dict[str, List[str]]:
        """get障碍解决方案"""
        solutions = {
            FocusBarrier.EXTERNAL: [
                "关闭非必要通知",
                "设置'勿扰模式'",
                "告知他人不要打扰",
                "使用番茄工作法"
            ],
            FocusBarrier.INTERNAL: [
                "做5分钟冥想",
                "把杂念写下来",
                "进行深呼吸",
                "接受杂念,不对抗"
            ],
            FocusBarrier.ENVIRONMENTAL: [
                "整理工作区域",
                "使用耳塞或白噪音",
                "调整光线和温度",
                "只保留工作必需品"
            ],
            FocusBarrier.HABITUAL: [
                "设定明确的目标和截止时间",
                "先做最难的事",
                "避免多任务",
                "使用专注App"
            ]
        }
        
        return {k.value: solutions.get(k, []) for k in barriers.keys()}
    
    def create_focus_plan(self, goal: str, available_minutes: int) -> Dict:
        """
        创建专注计划
        
        Args:
            goal: 目标任务
            available_minutes: 可用时间
            
        Returns:
            Dict: 专注计划
        """
        # 分割成番茄时段
        pomodoro_length = 25
        break_length = 5
        long_break_length = 15
        
        pomodoros = available_minutes // pomodoro_length
        total_breaks = (pomodoros - 1) // 4 * (long_break_length - break_length)
        
        effective_time = available_minutes - total_breaks
        
        return {
            "goal": goal,
            "available_minutes": available_minutes,
            "effective_minutes": effective_time,
            "structure": {
                "pomodoros": pomodoros,
                "short_breaks": pomodoros - 1 if pomodoros > 1 else 0,
                "long_breaks": (pomodoros - 1) // 4,
                "pomodoro_length_minutes": pomodoro_length,
                "break_length_minutes": break_length
            },
            "tips": [
                "开始前清空所有干扰",
                "每个番茄只做一件事",
                "休息时远离工作区",
                "记录每个番茄的完成情况"
            ]
        }
    
    def record_focus_session(self, session: FocusSession):
        """记录专注时段"""
        self.focus_sessions.append(session)
        
        # 更新连续专注天数
        if session.completion_rate >= 0.8:
            self.focus_streak += 1
        else:
            self.focus_streak = 0
    
    def get_focus_analytics(self) -> Dict:
        """get专注力分析"""
        if not self.focus_sessions:
            return {"message": "暂无专注数据"}
        
        total_sessions = len(self.focus_sessions)
        avg_quality = sum(s.quality_score for s in self.focus_sessions) / total_sessions
        avg_completion = sum(s.completion_rate for s in self.focus_sessions) / total_sessions
        avg_distractions = sum(s.distractions for s in self.focus_sessions) / total_sessions
        
        # 趋势分析
        recent = self.focus_sessions[-5:]
        recent_quality = sum(s.quality_score for s in recent) / len(recent) if recent else 0
        
        return {
            "total_sessions": total_sessions,
            "focus_streak_days": self.focus_streak,
            "avg_quality_score": round(avg_quality, 1),
            "avg_completion_rate": round(avg_completion * 100, 1),
            "avg_distractions_per_session": round(avg_distractions, 1),
            "recent_trend": "提升" if recent_quality > avg_quality else "稳定",
            "recommendation": self._get_focus_recommendation(avg_quality, avg_completion)
        }
    
    def _get_focus_recommendation(self, quality: float, completion: float) -> str:
        """get专注建议"""
        if quality < 60:
            return "专注力有待提升,建议减少干扰源,缩短单次专注时长"
        elif quality < 80:
            return "专注力良好,可以尝试深度工作模式(90分钟无中断)"
        else:
            return "专注力优秀,保持现状并继续挑战更难的任务"
    
    def essentialism_checklist(self, decision: str) -> Dict:
        """
        本质主义decision检查
        
        Args:
            decision: 需要做的决定
            
        Returns:
            Dict: decision分析
        """
        return {
            "question": decision,
            "criteria": [
                "这个问题/任务/物品是否让我兴奋?",
                "如果只能做一件事,我会选择它吗?",
                "它是否符合我的长期目标?",
                "做/拥有它是否让我更自由?"
            ],
            "yes_score": 0,
            "no_score": 0,
            "advice": "如果不能对以上所有问题回答'是',可能值得重新考虑"
        }
    
    def get_minimalism_quotes(self) -> List[str]:
        """get极简主义语录"""
        return [
            "极简主义不是关于拥有最少的东西,而是关于拥有最适合的东西.",
            "你拥有物品,物品也拥有你.",
            "清理杂乱是清理心灵的隐喻.",
            "少即是多,但少必须是有意识的少.",
            "不是要放弃生活,而是放弃生活的噪音.",
            "自由来自能够说不.",
            "简单是复杂的最终形式.",
            "专注的艺术在于知道什么可以忽略."
        ]

def create_minimalist_system() -> MinimalistFocusSystem:
    """工厂函数"""
    return MinimalistFocusSystem()
