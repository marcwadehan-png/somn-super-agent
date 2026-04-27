# -*- coding: utf-8 -*-
"""
神之架构智能体 V4.0 - 完整自动化
=================================

整合V2.0路由 + V3.0协作，提供从问题输入到Claw调用的全流程自动化

功能：
1. 问题分析自动识别ProblemType
2. 部门路由自动选择
3. Claw自动选择与调用
4. 多Claw自动协作（按需）
5. 结果自动合成与输出

使用方式：
    from src.intelligence.dispatcher.wisdom_dispatch._dispatch_agents import SomnAgent
    
    agent = SomnAgent()
    result = await agent.process("如何治理一个国家")
    print(result.answer)
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════════════════════

class ProcessStatus(Enum):
    """处理状态"""
    PENDING = "pending"
    ANALYZING = "analyzing"
    ROUTING = "routing"
    EXECUTING = "executing"
    COLLABORATING = "collaborating"
    SYNTHESIZING = "synthesizing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentContext:
    """智能体上下文"""
    query: str
    problem_type: str = ""
    departments: List[str] = field(default_factory=list)
    schools: List[str] = field(default_factory=list)
    primary_claw: str = ""
    collaborator_claws: List[str] = field(default_factory=list)
    routing_reason: str = ""
    confidence: float = 0.0


@dataclass
class AgentResult:
    """智能体处理结果"""
    success: bool
    answer: str
    query: str
    context: AgentContext
    status: ProcessStatus
    steps: List[Dict[str, Any]] = field(default_factory=list)
    elapsed_seconds: float = 0.0
    errors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "answer": self.answer,
            "query": self.query,
            "problem_type": self.context.problem_type,
            "departments": self.context.departments,
            "primary_claw": self.context.primary_claw,
            "collaborators": self.context.collaborator_claws,
            "confidence": self.context.confidence,
            "status": self.status.value,
            "steps": self.steps,
            "elapsed_seconds": self.elapsed_seconds,
            "errors": self.errors,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 问题类型识别
# ═══════════════════════════════════════════════════════════════════════════════

class ProblemTypeClassifier:
    """问题类型分类器"""
    
    # 关键词到ProblemType的映射
    KEYWORD_MAPPING = {
        # 兵部场景
        "竞争": "COMPETITION",
        "危机": "CRISIS",
        "攻击": "ATTACK",
        "防守": "DEFENSE",
        "谈判": "NEGOTIATION",
        "战争": "WAR_ECONOMY_NEXUS",
        
        # 户部场景
        "市场分析": "MARKET_ANALYSIS",
        "营销": "MARKETING",
        "消费者": "CONSUMER_MARKETING",
        "品牌": "BRAND_STRATEGY",
        "增长": "GROWTH_STRATEGY",
        
        # 吏部场景
        "团队": "TEAM_BUILDING",
        "组织": "ORGANIZATION",
        "领导": "LEADERSHIP",
        "人才": "TALENT",
        
        # 礼部场景
        "价值": "VALUES",
        "教育": "EDUCATION",
        "文化": "CULTURE",
        "仁": "VALUES",
        "义": "VALUES",
        
        # 工部场景
        "创新": "INNOVATION",
        "技术": "TECHNICAL",
        "产品": "PRODUCT",
        
        # 刑部场景
        "法律": "LEGAL",
        "合规": "COMPLIANCE",
        "风险": "RISK",
    }
    
    # 部门默认映射
    DEFAULT_DEPARTMENT = {
        "COMPETITION": "兵部",
        "CRISIS": "兵部",
        "ATTACK": "兵部",
        "DEFENSE": "兵部",
        "NEGOTIATION": "兵部",
        "WAR_ECONOMY_NEXUS": "兵部",
        "MARKET_ANALYSIS": "户部",
        "MARKETING": "户部",
        "CONSUMER_MARKETING": "户部",
        "BRAND_STRATEGY": "户部",
        "GROWTH_STRATEGY": "工部",
        "TEAM_BUILDING": "吏部",
        "ORGANIZATION": "吏部",
        "LEADERSHIP": "吏部",
        "TALENT": "吏部",
        "VALUES": "礼部",
        "EDUCATION": "礼部",
        "CULTURE": "礼部",
        "INNOVATION": "工部",
        "TECHNICAL": "工部",
        "PRODUCT": "工部",
        "LEGAL": "刑部",
        "COMPLIANCE": "刑部",
        "RISK": "刑部",
    }
    
    def classify(self, query: str) -> str:
        """
        分类问题类型
        
        Returns:
            ProblemType字符串
        """
        query_lower = query.lower()
        
        # 精确匹配
        for keyword, problem_type in self.KEYWORD_MAPPING.items():
            if keyword in query_lower:
                return problem_type
        
        # 默认分类
        return "GENERAL"
    
    def get_department(self, problem_type: str) -> str:
        """获取问题类型对应的部门"""
        return self.DEFAULT_DEPARTMENT.get(problem_type, "礼部")


# ═══════════════════════════════════════════════════════════════════════════════
# 核心智能体
# ═══════════════════════════════════════════════════════════════════════════════

class SomnAgent:
    """
    神之架构智能体 V4.0
    
    完整自动化：从问题输入到Claw调用全流程
    """
    
    def __init__(self):
        self._classifier = ProblemTypeClassifier()
        self._claw_router = None
        self._collaboration = None
    
    def _ensure_initialized(self):
        """确保依赖模块已初始化"""
        if self._claw_router is None:
            try:
                from ._dispatch_claw import get_claw_router
                self._claw_router = get_claw_router()
            except ImportError as e:
                logger.warning(f"[SomnAgent] 无法导入ClawRouter: {e}")
        
        if self._collaboration is None:
            try:
                from ._dispatch_collaboration import get_collaboration_protocol
                self._collaboration = get_collaboration_protocol()
            except ImportError as e:
                logger.warning(f"[SomnAgent] 无法导入Collaboration: {e}")
    
    async def process(
        self,
        query: str,
        enable_collaboration: bool = True,
        max_collaborators: int = 3,
    ) -> AgentResult:
        """
        处理问题的完整流程
        
        Args:
            query: 用户问题
            enable_collaboration: 是否启用多Claw协作
            max_collaborators: 最大协作Claw数量
            
        Returns:
            AgentResult
        """
        start_time = time.time()
        steps = []
        errors = []
        
        # 初始化
        self._ensure_initialized()
        
        # 1. 问题分析
        steps.append({"step": "analyze", "status": "start", "detail": "分析问题"})
        problem_type = self._classifier.classify(query)
        department = self._classifier.get_department(problem_type)
        steps[-1]["status"] = "done"
        steps[-1]["result"] = {"problem_type": problem_type, "department": department}
        
        # 2. Claw路由
        steps.append({"step": "route", "status": "start", "detail": "路由Claw"})
        
        if self._claw_router:
            route_result = self._claw_router.route_by_department(
                department, query, 
                include_collaborators=enable_collaboration
            )
            primary_claw = route_result.primary_claw
            collaborator_claws = route_result.collaborator_claws[:max_collaborators] if enable_collaboration else []
            confidence = route_result.confidence
            routing_reason = route_result.routing_reason
        else:
            # 降级处理
            primary_claw = "孔子"  # 默认
            collaborator_claws = []
            confidence = 0.5
            routing_reason = "默认路由"
        
        steps[-1]["status"] = "done"
        steps[-1]["result"] = {
            "primary_claw": primary_claw,
            "collaborators": collaborator_claws,
            "confidence": confidence,
        }
        
        # 3. 构建上下文
        context = AgentContext(
            query=query,
            problem_type=problem_type,
            departments=[department],
            primary_claw=primary_claw,
            collaborator_claws=collaborator_claws,
            routing_reason=routing_reason,
            confidence=confidence,
        )
        
        # 4. 执行Claw
        steps.append({"step": "execute", "status": "start", "detail": f"执行Claw: {primary_claw}"})
        
        try:
            from ..claws.claw import ClawSystem
            
            system = ClawSystem(claw_names=[primary_claw] + collaborator_claws)
            await system.start()
            
            response = await system.ask(query, target=primary_claw)
            
            await system.shutdown()
            
            final_answer = response.answer
            steps[-1]["status"] = "done"
            steps[-1]["result"] = {
                "answer_length": len(final_answer),
                "elapsed": response.elapsed,
            }
            
        except Exception as e:
            error_msg = f"Claw执行异常: {e}"
            logger.error(f"[SomnAgent] {error_msg}")
            errors.append(error_msg)
            final_answer = f"处理过程中出现错误："
            steps[-1]["status"] = "error"
            steps[-1]["error"] = "操作失败"
        
        # 5. 协作处理（如果需要）
        if enable_collaboration and collaborator_claws and self._collaboration:
            steps.append({"step": "collaborate", "status": "start", "detail": "多Claw协作"})
            
            try:
                collab_result = await self._collaboration.execute_collaboration(
                    primary_claw=primary_claw,
                    query=query,
                    collaborators=collaborator_claws,
                )
                
                if collab_result.success and collab_result.final_answer:
                    # 合并协作结果
                    final_answer = collab_result.final_answer
                    context.confidence = collab_result.confidence
                
                steps[-1]["status"] = "done"
                steps[-1]["result"] = {
                    "contributors": len(collab_result.contributions),
                    "confidence": collab_result.confidence,
                }
                
            except Exception as e:
                logger.warning(f"[SomnAgent] 协作执行异常: {e}")
                steps[-1]["status"] = "warning"
                steps[-1]["error"] = "操作失败"
        
        elapsed = time.time() - start_time
        
        return AgentResult(
            success=len(errors) == 0,
            answer=final_answer,
            query=query,
            context=context,
            status=ProcessStatus.COMPLETED if len(errors) == 0 else ProcessStatus.FAILED,
            steps=steps,
            elapsed_seconds=elapsed,
            errors=errors,
        )
    
    async def process_batch(
        self,
        queries: List[str],
        enable_collaboration: bool = True,
    ) -> List[AgentResult]:
        """批量处理问题"""
        tasks = [self.process(q, enable_collaboration) for q in queries]
        return await asyncio.gather(*tasks)


# ═══════════════════════════════════════════════════════════════════════════════
# 便捷函数
# ═══════════════════════════════════════════════════════════════════════════════

# 全局智能体实例
_somn_agent: Optional[SomnAgent] = None

def get_somn_agent() -> SomnAgent:
    """获取全局SomnAgent实例"""
    global _somnn_agent
    if _somn_agent is None:
        _somn_agent = SomnAgent()
    return _somn_agent


async def process_query(
    query: str,
    enable_collaboration: bool = True,
) -> AgentResult:
    """
    处理单个问题的便捷函数
    
    Args:
        query: 用户问题
        enable_collaboration: 是否启用多Claw协作
        
    Returns:
        AgentResult
    """
    agent = get_somn_agent()
    return await agent.process(query, enable_collaboration)


async def process_queries(
    queries: List[str],
    enable_collaboration: bool = True,
) -> List[AgentResult]:
    """
    批量处理问题的便捷函数
    """
    agent = get_somn_agent()
    return await agent.process_batch(queries, enable_collaboration)


__all__ = [
    "SomnAgent",
    "AgentContext",
    "AgentResult",
    "ProcessStatus",
    "ProblemTypeClassifier",
    "get_somn_agent",
    "process_query",
    "process_queries",
]