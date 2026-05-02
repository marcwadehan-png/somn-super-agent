# Claw SOUL驱动行为引擎
# v3.1.0: Phase 0核心实现
# 信念→决策优先级 | 价值观→过滤选项 | 自律准则→行为规范 | 性格→响应风格

from __future__ import annotations

import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

# 从父级模块导入ClawSoul和ClawIdentity（v3.1修复）
try:
    from .._claw_architect import ClawSoul, ClawIdentity
except ImportError:
    # 兼容没有identity的情况
    @dataclass
    class ClawSoul:
        beliefs: List[str] = field(default_factory=list)
        values: List[str] = field(default_factory=list)
        discipline: List[str] = field(default_factory=list)
        personality_traits: List[str] = field(default_factory=list)
        response_style: Dict[str, str] = field(default_factory=dict)
        
        def get_response_style(self, context: str = "default") -> str:
            return self.response_style.get(context, self.response_style.get("default", ""))
    
    @dataclass
    class ClawIdentity:
        name: str = ""
        role_primary: str = ""
        role_secondary: List[str] = field(default_factory=list)
        skills_tags: List[str] = field(default_factory=list)

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════
# 决策优先级
# ═══════════════════════════════════════════════════════════════════

class DecisionPriority(Enum):
    """决策优先级"""
    CRITICAL = 1      # 关键决策
    HIGH = 2          # 高优先级
    MEDIUM = 3        # 中等
    LOW = 4           # 低优先级
    ROUTINE = 5       # 常规


class SoulDrivenDecision:
    """
    SOUL驱动的决策引擎
    
    信念 → 决策优先级
    根据核心信念确定问题的决策优先级
    """
    
    # 信念关键词到优先级的映射
    BELIEF_PRIORITY_MAP = {
        # 关键信念 → 高优先级
        "有教无类": DecisionPriority.HIGH,
        "知行合一": DecisionPriority.HIGH,
        "致良知": DecisionPriority.HIGH,
        "不战而屈人之兵": DecisionPriority.CRITICAL,
        # 一般信念 → 中等
        "中庸之道": DecisionPriority.MEDIUM,
    }
    
    def __init__(self, soul: ClawSoul):
        self.soul = soul
    
    def get_priority(self, query: str) -> DecisionPriority:
        """
        根据查询确定决策优先级
        
        Args:
            query: 用户查询
            
        Returns:
            DecisionPriority: 决策优先级
        """
        query_lower = query.lower()
        
        # 检查核心信念是否匹配
        for belief in self.soul.beliefs:
            if belief in query_lower:
                priority = self.BELIEF_PRIORITY_MAP.get(
                    belief, 
                    DecisionPriority.MEDIUM
                )
                logger.info(f"[SoulDecision] 信念'{belief}'匹配，优先级: {priority.name}")
                return priority
        
        # 默认中等优先级
        return DecisionPriority.MEDIUM
    
    def should_escalate(self, query: str) -> bool:
        """是否需要升级处理"""
        return self.get_priority(query).value <= DecisionPriority.HIGH.value


# ═══════════════════════════════════════════════════════════════════
# 价值观过滤
# ═══════════════════════════════════════════════════════════════════

class ValueFilter:
    """
    价值观过滤器
    
    价值观 → 过滤选项
    根据价值观过滤不可接受的选项
    """
    
    # 价值观到过滤行为的映射
    VALUE_FILTER_RULES = {
        # 仁爱价值观：过滤伤害性选项
        "仁爱": {
            "filter_out": ["攻击", "伤害", "破坏", "欺骗"],
            "require": ["帮助", "保护", "促进"]
        },
        # 诚信价值观��过滤虚假选项
        "诚信": {
            "filter_out": ["虚假", "欺骗", "夸张", "隐瞒"],
            "require": ["真实", "准确", "透明"]
        },
        # 学习价值观：过滤封闭选项
        "学习": {
            "filter_out": ["拒绝学习", "封闭", "排斥"],
            "require": ["开放", "接受", "探索"]
        },
    }
    
    def __init__(self, soul: ClawSoul):
        self.soul = soul
    
    def filter_options(self, options: List[str]) -> List[str]:
        """
        根据价值观过滤选项
        
        Args:
            options: 候选选项列表
            
        Returns:
            List[str]: 过滤后的选项
        """
        filtered = options.copy()
        reasons = []
        
        for value in self.soul.values:
            if value not in self.VALUE_FILTER_RULES:
                continue
            
            rule = self.VALUE_FILTER_RULES[value]
            filter_out = rule.get("filter_out", [])
            
            # 过滤
            before_count = len(filtered)
            filtered = [
                opt for opt in filtered 
                if not any(f in opt for f in filter_out)
            ]
            after_count = len(filtered)
            
            if before_count != after_count:
                reasons.append(
                    f"价值'{value}'过滤{before_count - after_count}个选项"
                )
        
        if reasons:
            logger.info(f"[ValueFilter] 过滤原因: {reasons}")
        
        return filtered
    
    def score_option(self, option: str, base_score: float = 0.5) -> float:
        """
        根据价值观给选项打分
        
        Args:
            option: 选项
            base_score: 基础分数
            
        Returns:
            float: 加权后的分数
        """
        score = base_score
        
        for value in self.soul.values:
            if value not in self.VALUE_FILTER_RULES:
                continue
            
            rule = self.VALUE_FILTER_RULES[value]
            require = rule.get("require", [])
            
            # 如果选项包含需要的关键词，加分
            if any(r in option for r in require):
                score += 0.15
        
        return min(score, 1.0)


# ═══════════════════════════════════════════════════════════
# 自律准则引擎
# ═══════════════════════════════════════════════════════════════════

class DisciplineEngine:
    """
    自律准则引擎
    
    自律准则 → 行为规范
    根据自律准则约束AI行为
    """
    
    def __init__(self, soul: ClawSoul):
        self.soul = soul
    
    def should_do(self, action: str) -> bool:
        """
        根据自律准则判断是否应该执行动作
        
        Args:
            action: 拟执行的动作
            
        Returns:
            bool: 是否允许执行
        """
        # 检查是否违反任何自律准则
        for rule in self.soul.discipline:
            if self._violates(rule, action):
                logger.warning(f"[Discipline] 动作'{action}'违反准则'{rule}'")
                return False
        
        return True
    
    def _violates(self, rule: str, action: str) -> bool:
        """检查动作是否违反准则"""
        action_lower = action.lower()
        
        # 学而时习之：拒绝学习
        if "学而时习" in rule:
            if "不学习" in action_lower or "拒绝" in action_lower:
                return True
        
        # 温故而知新：拒绝复习
        if "温故知新" in rule:
            if "不复习" in action_lower:
                return True
        
        # 不耻下问：拒绝提问
        if "不耻下问" in rule:
            if "拒绝提问" in action_lower or "耻于" in action_lower:
                return True
        
        return False
    
    def suggest_actions(self, context: str) -> List[str]:
        """
        根据自律准则建议动作
        
        Args:
            context: 当前上下文
            
        Returns:
            List[str]: 建议的动作列表
        """
        suggestions = []
        
        for rule in self.soul.discipline:
            if "学而时习" in rule:
                suggestions.append("复习相关知识")
            if "温故知新" in rule:
                suggestions.append("回顾之前的 context")
            if "三人行" in rule:
                suggestions.append("寻求多元视角")
        
        return suggestions


# ═══════════════════════════════════════════════════════════
# 响应风格引擎
# ═══════════════════════════════════════════════════════════════════

class ResponseStyleEngine:
    """
    响应风格引擎
    
    性格 → 响应风格
    根据性格特征调整响应方式
    """
    
    def __init__(self, soul: ClawSoul):
        self.soul = soul
    
    def get_style(self, context: str = "default") -> str:
        """
        获取响应风格
        
        Args:
            context: 上下文（default/quick/formal/casual）
            
        Returns:
            str: 响应风格描述
        """
        return self.soul.get_response_style(context)
    
    def format_response(
        self, 
        content: str, 
        style: Optional[str] = None
    ) -> str:
        """
        根据风格格式化响应
        
        Args:
            content: 原始内容
            style: 指定风格（可选）
            
        Returns:
            str: 格式化后的内容
        """
        if style is None:
            style = self.get_style()
        
        # 根据风格添加修饰
        if style == "循循善诱，谆谆教诲":
            # 教育家风格：添加引导性问题
            content += "\n\n你对这个问题的看法是什么？"
        elif style == "简洁明了":
            # 简洁风格：去掉多余修饰
            content = content.split("\n\n")[0]
        elif style == "正式":
            # 正式风格：添加敬语
            content = "根据分析：" + content
        
        return content
    
    def adjust_tone(self, content: str, traits: List[str]) -> str:
        """
        根据性格特征调整语气
        
        Args:
            content: 原始内容
            traits: 性格特征列表
            
        Returns:
            str: 调整后的内容
        """
        # 温而厉：保持温和但有原则
        if "温而厉" in traits or "温和" in traits:
            if "但是" in content or "然而" in content:
                content = content.replace(
                    "但是", "��过"
                ).replace(
                    "然而", "不过"
                )
        
        # 学而不厌：添加探索性结尾
        if "学而不厌" in traits:
            if not content.endswith("？"):
                content += "\n\n你觉得还有其他角度吗？"
        
        return content


# ═══════════════════════════════════════════════════════════════════
# SOUL驱动行为主引擎
# ═══════════════════════════════════════════════════════════════════

class SoulBehaviorEngine:
    """
    SOUL驱动行为主引擎
    
    整合所有SOUL驱动的行为模块
    """
    
    def __init__(self, soul: ClawSoul):
        self.soul = soul
        
        # 初始化各子引擎
        self.decision = SoulDrivenDecision(soul)
        self.filter = ValueFilter(soul)
        self.discipline = DisciplineEngine(soul)
        self.style = ResponseStyleEngine(soul)
    
    def process(
        self,
        query: str,
        options: List[str],
        context: str = "default"
    ) -> Dict[str, Any]:
        """
        处理SOUL驱动的行为
        
        Args:
            query: 用户查询
            options: 候选选项
            context: 上下文
            
        Returns:
            Dict: 处理结果
                - priority: 决策优先级
                - filtered_options: 过滤后的选项
                - allowed: 是否允许执行
                - response_style: 响应风格
                - suggestions: 建议的动作
        """
        # 1. 决策优先级
        priority = self.decision.get_priority(query)
        
        # 2. 价值观过滤
        filtered = self.filter.filter_options(options)
        
        # 3. 自律检查
        allowed = self.discipline.should_do(query)
        
        # 4. 响应风格
        style = self.style.get_style(context)
        
        # 5. 建议动作
        suggestions = self.discipline.suggest_actions(query)
        
        return {
            "priority": priority,
            "filtered_options": filtered,
            "allowed": allowed,
            "response_style": style,
            "suggestions": suggestions,
            "belief_matched": self.decision.get_priority(query).name
        }


# ═══════════════════════════════════════════════════════════════════
# 导出
# ═══════════════════════════════════════════════════════════════

__all__ = [
    "DecisionPriority",
    "SoulDrivenDecision",
    "ValueFilter",
    "DisciplineEngine",
    "ResponseStyleEngine",
    "SoulBehaviorEngine",
]