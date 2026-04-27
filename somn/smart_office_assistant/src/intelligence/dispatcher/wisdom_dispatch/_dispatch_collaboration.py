# -*- coding: utf-8 -*-
"""
跨部门多Claw协作协议 V1.0
==========================

功能：
1. 跨部门Claw发现与协作
2. 协作请求/响应协议
3. 结果聚合机制
4. 协作历史记忆

使用方式：
    from src.intelligence.dispatcher.wisdom_dispatch._dispatch_collaboration import (
        CollaborationProtocol, collaborate_claws
    )
    
    result = await collaborate_claws(
        primary="孔子",
        query="如何治理一个国家",
        collaborators=["孟子", "荀子", "管仲"]
    )
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════════════════════

class CollaborationRole(Enum):
    """协作角色"""
    PRIMARY = "primary"       # 主Claw，负责统筹和最终输出
    CONTRIBUTOR = "contributor"  # 贡献者，提供独立视角
    ADVISOR = "advisor"       # 顾问，提供补充建议
    REVIEWER = "reviewer"     # 审核者，审查结果


class CollaborationPhase(Enum):
    """协作阶段"""
    INITIATION = "initiation"     # 发起阶段
    ANALYSIS = "analysis"         # 分析阶段
    CONTRIBUTION = "contribution" # 贡献阶段
    SYNTHESIS = "synthesis"       # 合成阶段
    REVIEW = "review"             # 审核阶段
    COMPLETION = "completion"     # 完成阶段


@dataclass
class CollaborationRequest:
    """协作请求"""
    request_id: str
    primary_claw: str
    query: str
    collaborators: List[str]
    roles: Dict[str, CollaborationRole]
    context: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ContributionResult:
    """贡献结果"""
    claw_name: str
    role: CollaborationRole
    content: str
    insights: List[str] = field(default_factory=list)
    confidence: float = 0.0
    elapsed_seconds: float = 0.0


@dataclass
class CollaborationResult:
    """协作结果"""
    request_id: str
    success: bool
    primary_claw: str
    final_answer: str
    contributions: List[ContributionResult]
    synthesis_notes: str = ""
    confidence: float = 0.0
    elapsed_seconds: float = 0.0
    errors: List[str] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════════════
# 协作协议核心
# ═══════════════════════════════════════════════════════════════════════════════

class CollaborationProtocol:
    """
    跨部门Claw协作协议 V1.0
    
    提供标准化的多Claw协作流程
    """
    
    def __init__(self, claw_router=None):
        """
        Args:
            claw_router: ClawRouter实例，用于发现协作Claw
        """
        self._claw_router = claw_router
        self._history: List[CollaborationResult] = []
        self._max_history = 100
    
    def discover_collaborators(
        self,
        primary_claw: str,
        query: str,
        department: str = None,
        max_count: int = 3,
    ) -> List[Tuple[str, CollaborationRole]]:
        """
        发现可用的协作Claw
        
        Args:
            primary_claw: 主Claw名称
            query: 问题内容
            department: 优先部门
            max_count: 最大协作Claw数量
            
        Returns:
            [(claw_name, role), ...]
        """
        collaborators = []
        
        # 导入ClawRouter
        if self._claw_router is None:
            try:
                from ._dispatch_claw import get_claw_router
                self._claw_router = get_claw_router()
            except ImportError:
                logger.warning("[Collaboration] 无法导入ClawRouter")
                return []
        
        # 获取主Claw信息
        claw_info = self._claw_router._claws.get(primary_claw)
        if not claw_info:
            return []
        
        # 1. 同一学派的Claw
        school = claw_info.school
        school_claws = self._claw_router._school_claws.get(school, [])
        for c in school_claws:
            if c != primary_claw and len(collaborators) < max_count:
                collaborators.append((c, CollaborationRole.CONTRIBUTOR))
        
        # 2. 同一部门的其他Claw（不同学派）
        dept = claw_info.department
        dept_claws = self._department_claws.get(dept, [])
        for c in dept_claws:
            if c != primary_claw and c not in [x[0] for x in collaborators] and len(collaborators) < max_count:
                collaborators.append((c, CollaborationRole.ADVISOR))
        
        # 3. 跨部门Claw（如果指定了部门）
        if department and department != dept:
            other_dept_claws = self._department_claws.get(department, [])
            for c in other_dept_claws:
                if c != primary_claw and c not in [x[0] for x in collaborators] and len(collaborators) < max_count:
                    collaborators.append((c, CollaborationRole.REVIEWER))
        
        return collaborators[:max_count]
    
    @property
    def _department_claws(self) -> Dict[str, List[str]]:
        """获取部门Claw索引"""
        if self._claw_router:
            return self._claw_router._department_claws
        return {}
    
    async def execute_collaboration(
        self,
        primary_claw: str,
        query: str,
        collaborators: List[str],
        roles: Dict[str, CollaborationRole] = None,
    ) -> CollaborationResult:
        """
        执行多Claw协作
        
        Args:
            primary_claw: 主Claw
            query: 问题
            collaborators: 协作Claw列表
            roles: 角色映射
            
        Returns:
            CollaborationResult
        """
        import time
        start_time = time.time()
        
        # 生成请求ID
        request_id = f"collab_{int(start_time * 1000)}"
        
        # 默认角色
        if roles is None:
            roles = {primary_claw: CollaborationRole.PRIMARY}
            for i, c in enumerate(collaborators):
                if i == 0:
                    roles[c] = CollaborationRole.CONTRIBUTOR
                elif i == 1:
                    roles[c] = CollaborationRole.ADVISOR
                else:
                    roles[c] = CollaborationRole.REVIEWER
        
        # 创建请求
        request = CollaborationRequest(
            request_id=request_id,
            primary_claw=primary_claw,
            query=query,
            collaborators=collaborators,
            roles=roles,
        )
        
        contributions = []
        errors = []
        
        # 1. 主Claw先处理
        logger.info(f"[Collaboration] 主Claw {primary_claw} 开始处理...")
        primary_result = await self._execute_single_claw(primary_claw, query)
        if primary_result:
            contributions.append(primary_result)
        else:
            errors.append(f"主Claw {primary_claw} 执行失败")
        
        # 2. 并行执行协作Claw
        if collaborators:
            tasks = [
                self._execute_single_claw(c, query, context=primary_result.content if primary_result else "")
                for c in collaborators
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for c, result in zip(collaborators, results):
                if isinstance(result, Exception):
                    errors.append(f"协作Claw {c} 执行异常: {result}")
                elif result:
                    contributions.append(result)
                else:
                    errors.append(f"协作Claw {c} 执行失败")
        
        # 3. 合成结果
        synthesis = self._synthesize_results(
            query, contributions, roles
        )
        
        elapsed = time.time() - start_time
        
        # 4. 构建最终结果
        result = CollaborationResult(
            request_id=request_id,
            success=len(errors) == 0,
            primary_claw=primary_claw,
            final_answer=synthesis["answer"],
            contributions=contributions,
            synthesis_notes=synthesis["notes"],
            confidence=synthesis["confidence"],
            elapsed_seconds=elapsed,
            errors=errors,
        )
        
        # 记录历史
        self._history.append(result)
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history:]
        
        logger.info(f"[Collaboration] 协作完成: {request_id}, 耗时 {elapsed:.2f}s")
        return result
    
    async def _execute_single_claw(
        self,
        claw_name: str,
        query: str,
        context: str = "",
    ) -> Optional[ContributionResult]:
        """执行单个Claw"""
        import time
        start = time.time()
        
        try:
            # 动态导入Claw系统
            from ..claws.claw import ClawSystem
            
            # 创建临时Claw系统
            system = ClawSystem(claw_names=[claw_name])
            await system.start()
            
            # 添加上下文
            full_query = query
            if context:
                full_query = f"{query}\n\n参考信息：{context}"
            
            # 执行
            response = await system.ask(full_query, target=claw_name)
            
            await system.shutdown()
            
            elapsed = time.time() - start
            
            return ContributionResult(
                claw_name=claw_name,
                role=CollaborationRole.CONTRIBUTOR,
                content=response.answer,
                confidence=response.confidence,
                elapsed_seconds=elapsed,
            )
            
        except Exception as e:
            logger.error(f"[Collaboration] Claw {claw_name} 执行异常: {e}")
            return None
    
    def _synthesize_results(
        self,
        query: str,
        contributions: List[ContributionResult],
        roles: Dict[str, CollaborationRole],
    ) -> Dict[str, Any]:
        """合成多Claw结果"""
        
        if not contributions:
            return {"answer": "无法处理该问题", "notes": "无有效贡献", "confidence": 0.0}
        
        # 按角色排序
        primary = None
        others = []
        for c in contributions:
            if roles.get(c.claw_name) == CollaborationRole.PRIMARY:
                primary = c
            else:
                others.append(c)
        
        # 主Claw的结果作为基础
        if primary:
            base_answer = primary.content
        else:
            base_answer = contributions[0].content
        
        # 整合其他Claw的见解
        insights = []
        for c in others:
            if c.content and c.content != base_answer:
                # 提取关键见解
                lines = c.content.split('\n')
                key_lines = [l for l in lines if l.strip() and len(l) < 100][:2]
                insights.extend(key_lines)
        
        # 构建综合答案
        synthesis_notes = ""
        if insights:
            synthesis_notes = "【其他视角】\n" + "\n".join(insights[:5])
        
        final_answer = base_answer
        if synthesis_notes:
            final_answer = f"{base_answer}\n\n{synthesis_notes}"
        
        # 计算置信度
        confidences = [c.confidence for c in contributions if c.confidence > 0]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.5
        
        return {
            "answer": final_answer,
            "notes": synthesis_notes,
            "confidence": min(avg_confidence + 0.1, 1.0),  # 协作增加置信度
        }
    
    def get_history(self, limit: int = 10) -> List[CollaborationResult]:
        """获取协作历史"""
        return self._history[-limit:]


# ═══════════════════════════════════════════════════════════════════════════════
# 便捷函数
# ═══════════════════════════════════════════════════════════════════════════════

# 全局协作协议实例
_collaboration_protocol: Optional[CollaborationProtocol] = None

def get_collaboration_protocol() -> CollaborationProtocol:
    """获取全局协作协议实例"""
    global _collaboration_protocol
    if _collaboration_protocol is None:
        _collaboration_protocol = CollaborationProtocol()
    return _collaboration_protocol


async def collaborate_claws(
    primary: str,
    query: str,
    collaborators: List[str] = None,
    auto_discover: bool = True,
) -> CollaborationResult:
    """
    执行多Claw协作的便捷函数
    
    Args:
        primary: 主Claw名称
        query: 问题
        collaborators: 协作Claw列表（可选）
        auto_discover: 是否自动发现协作Claw
        
    Returns:
        CollaborationResult
    """
    protocol = get_collaboration_protocol()
    
    # 自动发现协作Claw
    if auto_discover and not collaborators:
        discovered = protocol.discover_collaborators(primary, query)
        collaborators = [c[0] for c in discovered]
    
    return await protocol.execute_collaboration(
        primary_claw=primary,
        query=query,
        collaborators=collaborators or [],
    )


__all__ = [
    "CollaborationProtocol",
    "CollaborationRole",
    "CollaborationPhase",
    "CollaborationRequest",
    "CollaborationResult",
    "ContributionResult",
    "get_collaboration_protocol",
    "collaborate_claws",
]