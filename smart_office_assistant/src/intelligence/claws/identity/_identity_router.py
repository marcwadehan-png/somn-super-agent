# Claw IDENTITY驱动路由引擎
# v3.2.0: Phase 1核心实现
# role→主要路由目标 | skills_tags→触发词匹配 | entity→协作角色

from __future__ import annotations

import logging
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field

# 从父级模块导入ClawIdentity（v3.2修复）
try:
    from .._claw_architect import ClawIdentity
except ImportError:
    @dataclass
    class ClawIdentity:
        name: str = ""
        role_primary: str = ""
        role_secondary: List[str] = field(default_factory=list)
        skills_tags: List[str] = field(default_factory=list)

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════
# 路由目标
# ═══════════════════════════════════════════════════════════════════

@dataclass
class RouteTarget:
    """路由目标"""
    name: str              # 目标Claw名称
    confidence: float     # 置信度 0.0-1.0
    reason: str          # 匹配原因
    role: str           # 角色类型


class IdentityDrivenRouter:
    """
    IDENTITY驱动的路由引擎
    
    role → 主要路由目标
    根据身份角色确定路由目标
    """
    
    # 角色到路由目标的映射
    ROLE_TARGET_MAP = {
        "教育家": ["孔子", "王阳明", "孟子"],
        "思想家": ["老子", "庄子", "荀子"],
        "政治家": ["管仲", "商鞅", "王安石"],
        "军事家": ["孙子", "克劳塞维茨"],
        "经济学家": ["亚当·斯密", "凯恩斯", "马克思"],
        "管理学家": ["德鲁克", "韦伯", "泰勒"],
    }
    
    def __init__(self, identity: ClawIdentity):
        self.identity = identity
    
    def get_route_target(self) -> str:
        """
        获取主要路由目标
        
        Returns:
            str: 路由目标Claw名称
        """
        role = self.identity.role_primary
        
        if role in self.ROLE_TARGET_MAP:
            targets = self.ROLE_TARGET_MAP[role]
            # 返回第一个作为主要目标
            target = targets[0]
            logger.info(f"[IdentityRouter] 角色'{role}' → 路由到'{target}'")
            return target
        
        # 默认返回name
        return self.identity.name or "孔子"
    
    def get_fallback_targets(self) -> List[str]:
        """获取备用路由目标"""
        role = self.identity.role_primary
        
        if role in self.ROLE_TARGET_MAP:
            return self.ROLE_TARGET_MAP[role][1:]
        
        return []


# ═══════════════════════════════════════════════════════════════════
# 触发词匹配
# ═══════════════════════════════════════════════════════════════════

class SkillsTriggerMatcher:
    """
    技能触发词匹配器
    
    skills_tags → 触发词匹配
    根据技能标签确定触发词
    """
    
    # 技能标签到触发词的映射
    SKILL_TRIGGER_MAP = {
        "营销": ["营销", "增长", "推广", "用户", "转化"],
        "增长": ["增长", "扩张", " Scaling", "用户增长"],
        "运营": ["运营", "维护", "管理", "流程"],
        "策略": ["策略", "战略", "规划", "方案"],
        "教育": ["教育", "教学", "培训", "学习"],
        "伦理": ["伦理", "道德", "价值", "善恶"],
        "政治": ["政治", "治理", "治国", "政策"],
        "经济": ["经济", "财富", "生产", "分配"],
    }
    
    def __init__(self, identity: ClawIdentity):
        self.identity = identity
    
    def match(self, query: str) -> float:
        """
        匹配查询与技能标签
        
        Args:
            query: 用户查询
            
        Returns:
            float: 匹配分数 0.0-1.0
        """
        query_lower = query.lower()
        matched_skills = set()
        
        # 检查skills_tags
        for skill_tag in self.identity.skills_tags:
            # 检查预定义映射
            triggers = self.SKILL_TRIGGER_MAP.get(skill_tag, [])
            for trigger in triggers:
                if trigger in query_lower:
                    matched_skills.add(skill_tag)
                    break
        
        # 检查直接匹配
        for skill_tag in self.identity.skills_tags:
            if skill_tag in query_lower:
                matched_skills.add(skill_tag)
        
        if matched_skills:
            score = len(matched_skills) / max(len(self.identity.skills_tags), 1)
            logger.info(f"[SkillsMatcher] 技能匹配: {matched_skills}, 分数: {score:.2f}")
            return min(score, 1.0)
        
        return 0.0
    
    def get_triggered_skills(self, query: str) -> List[str]:
        """
        获取触发匹配的技能标签
        
        Args:
            query: 用户查询
            
        Returns:
            List[str]: 匹配的技能标签
        """
        query_lower = query.lower()
        triggered = []
        
        for skill_tag in self.identity.skills_tags:
            triggers = self.SKILL_TRIGGER_MAP.get(skill_tag, [skill_tag])
            if any(t in query_lower for t in triggers):
                triggered.append(skill_tag)
        
        return triggered


# ═══════════════════════════════════════════════════════════════════
# 协作角色分配
# ═══════════════════════════════════════════════════════════════════

class CollaborationRoleAssigner:
    """
    协作角色分配器
    
    entity → 协作角色
    确定在多Claw协作中的角色
    """
    
    def __init__(self, identity: ClawIdentity):
        self.identity = identity
    
    def get_collaboration_role(
        self,
        collaborators: List[str]
    ) -> str:
        """
        获取协作角色
        
        Args:
            collaborators: 协作者列表
            
        Returns:
            str: 角色（leader/analyst/supporter/reviewer）
        """
        # 根据secondary roles确定
        secondary = self.identity.role_secondary
        
        if "教育家" in secondary:
            return "mentor"
        if "思想家" in secondary:
            return "analyst"
        if "政治家" in secondary:
            return "leader"
        
        # 默认analyst
        return "analyst"
    
    def should_lead(self, collaborators: List[str]) -> bool:
        """是否应该主导协作"""
        # 根据primary role判断
        if self.identity.role_primary in ["政治家", "军事���", "管理学家"]:
            return True
        
        return False
    
    def should_support(self, collaborators: List[str]) -> bool:
        """是否应该支持协作"""
        return True


# ═══════════════════════════════════════════════════════════════════
# IDENTITY驱动路由主引擎
# ═══════════════════════════════════════════════════════════════════

class IdentityRouterEngine:
    """
    IDENTITY驱动路由主引擎
    
    整合所有IDENTITY驱动的路由模块
    """
    
    def __init__(self, identity: ClawIdentity):
        self.identity = identity
        
        # 初始化各子引擎
        self.router = IdentityDrivenRouter(identity)
        self.matcher = SkillsTriggerMatcher(identity)
        self.collaboration = CollaborationRoleAssigner(identity)
    
    def route(
        self,
        query: str,
        available_claws: Optional[List[str]] = None
    ) -> RouteTarget:
        """
        执行IDENTITY驱动的路由
        
        Args:
            query: 用户查询
            available_claws: 可用的Claw列表
            
        Returns:
            RouteTarget: 路由结果
        """
        # 1. 主要路由目标
        primary_target = self.router.get_route_target()
        
        # 2. 技能匹配
        skill_score = self.matcher.match(query)
        
        # 3. 计算置信度
        confidence = 0.5
        if skill_score > 0:
            confidence = skill_score * 0.4 + 0.5
        
        # 4. 协作角色
        collab_role = self.collaboration.get_collaboration_role([])
        
        return RouteTarget(
            name=primary_target,
            confidence=confidence,
            reason=f"role:{self.identity.role_primary}",
            role=collab_role
        )
    
    def find_similar_claws(
        self,
        query: str,
        available_claws: List[str]
    ) -> List[Tuple[str, float]]:
        """
        查找相似的Claw
        
        Args:
            query: 用户查询
            available_claws: 可用的Claw列表
            
        Returns:
            List[Tuple[str, float]]: (Claw名称, 相似度分数)
        """
        triggered = self.matcher.get_triggered_skills(query)
        if not triggered:
            return []
        
        # 简单相似度计算
        similar = []
        for claw in available_claws:
            score = 0.3  # 基础分
            if any(t in claw for t in triggered):
                score += 0.5
            similar.append((claw, score))
        
        return sorted(similar, key=lambda x: x[1], reverse=True)[:3]


# ═══════════════════════════════════════════════════════════════════
# 导出
# ═══════════════════════════════════════════════════════════════

__all__ = [
    "RouteTarget",
    "IdentityDrivenRouter",
    "SkillsTriggerMatcher",
    "CollaborationRoleAssigner",
    "IdentityRouterEngine",
]