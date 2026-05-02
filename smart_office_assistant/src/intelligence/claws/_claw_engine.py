# ClawEngine - 独立/协作工作主引擎
# v4.1.0: 每个Claw独立工作+协作工作+完整上下文+环境适配
# 每个Claw拥有独立的记忆存储

from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Dict, Optional, Any, TYPE_CHECKING
from dataclasses import dataclass, field
from datetime import datetime

if TYPE_CHECKING:
    from ._claw_architect import ClawArchitect, ClawMetadata
    from .soul._soul_driver import SoulBehaviorEngine
    from .identity._identity_router import IdentityRouterEngine
    from .memory._learning_engine import LearningEngine

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════
# 协作消息
# ═══════════════════════════════════════════════════════════════════

@dataclass
class CollaboratorMessage:
    """协作消息"""
    sender: str              # 发送者Claw名称
    receiver: str           # 接收者Claw名称
    content: str            # 消息内容
    timestamp: str = ""     # 时间戳
    context: str = ""        # 上下文
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


@dataclass
class CollaborationResult:
    """协作结果"""
    success: bool
    primary_response: str  # 主要响应
    collaborator_responses: Dict[str, str] = field(default_factory=dict)
    shared_context: Dict[str, Any] = field(default_factory=dict)
    total_time: float = 0.0
    error: str = ""


# ═══════════════════════════════════════════════════════════════════
# Claw独立工作器
# ═══════════════════════════════════════════════════════════════════

class ClawIndependentWorker:
    """
    Claw独立工作器
    
    每个Claw独立处理请求，拥有自己的：
    - 完整上下文（ClawContext）
    - 环境变量适配（ClawEnvironment）
    - 记忆系统
    - SOUL行为引擎
    - IDENTITY路由引擎
    - ReAct闭环
    """
    
    def __init__(
        self,
        name: str,
        metadata: "ClawMetadata",
        architect: Optional["ClawArchitect"] = None,
        project_root: Optional[Path] = None
    ):
        self.name = name
        self.metadata = metadata
        self.architect = architect
        
        # 存储目录（独立）
        self.root = project_root or Path(__file__).resolve().parents[4]
        self.memory_dir = self.root / "data" / "claws" / name / "memory"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # ── 完整上下文 v4.1.0 ──
        from .context._claw_context import ClawContextContainer
        from .context._claw_environment import ClawEnvironment
        
        self.context = ClawContextContainer(name)
        self.environment = ClawEnvironment(name)
        
        # Lazy load engines
        self._soul_engine: Optional["SoulBehaviorEngine"] = None
        self._identity_engine: Optional["IdentityRouterEngine"] = None
        self._learning_engine: Optional["LearningEngine"] = None
        
        logger.info(f"[ClawIndependent] {name} 独立工作器初始化")
    
    @property
    def soul_engine(self) -> "SoulBehaviorEngine":
        """懒加载SOUL引擎"""
        if self._soul_engine is None:
            from .soul._soul_driver import SoulBehaviorEngine
            self._soul_engine = SoulBehaviorEngine(self.metadata.soul)
        return self._soul_engine
    
    @property
    def identity_engine(self) -> "IdentityRouterEngine":
        """懒加载IDENTITY引擎"""
        if self._identity_engine is None:
            from .identity._identity_router import IdentityRouterEngine
            self._identity_engine = IdentityRouterEngine(self.metadata.identity)
        return self._identity_engine
    
    @property
    def learning_engine(self) -> "LearningEngine":
        """懒加载学习引擎"""
        if self._learning_engine is None:
            from .memory._learning_engine import LearningEngine
            self._learning_engine = LearningEngine(self.memory_dir)
        return self._learning_engine
    
    async def process(
        self,
        query: str,
        context: Optional[str] = None,
        session_id: Optional[str] = None,
        user_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        独立处理查询（v4.1.0 完整上下文）
        
        Args:
            query: 用户查询
            context: 上下文描述
            session_id: 会话ID
            user_info: 用户信息
            
        Returns:
            Dict: 处理结果
        """
        start_time = datetime.now()
        
        try:
            # ── 更新上下文 v4.1.0 ──
            
            # 1. 设置会话上下文
            if session_id:
                self.context.set_session(session_id, current_topic=query[:50])
            
            # 2. 添加用户消息
            self.context.add_user_message(query)
            
            # 3. 更新用户信息
            if user_info:
                self.context.set_user(
                    user_id=user_info.get("id", ""),
                    user_name=user_info.get("name", ""),
                    level=user_info.get("level", "normal")
                )
            
            # 4. 获取完整上下文
            full_context = self.context.get_full_context()
            
            # 5. SOUL驱动行为（传入上下文）
            soul_result = self.soul_engine.process(
                query=query,
                options=[],
                context=context or self.context.system.get_greeting()
            )
            
            # 6. ReAct闭环处理（如有architect）
            react_result = None
            if self.architect:
                # ClawArchitect的process方法返回ReActResult
                react_result = await self.architect.process(query, {"independent_mode": True})
            
            # 7. 学习记录
            learning_result = self.learning_engine.learn(
                query,
                context=context
            )
            
            # 8. 添加助手消息
            response_text = react_result.final_answer if react_result else soul_result.get("response_style", "")
            self.context.add_assistant_message(response_text)
            
            # 9. 更新Claw状态
            self.context.update_claw_state(
                status="active",
                memory_snapshot=learning_result
            )
            
            elapsed = (datetime.now() - start_time).total_seconds()
            
            return {
                "success": True,
                "query": query,
                "response": response_text,
                "soul_result": soul_result,
                "learning_result": learning_result,
                "context": full_context,  # v4.1.0 新增
                "environment": self.environment.to_dict(),  # v4.1.0 新增
                "elapsed_seconds": elapsed,
                "mode": "independent"
            }
            
        except Exception as e:
            logger.error(f"[ClawIndependent] {self.name} 处理失败: {e}")
            return {
                "success": False,
                "error": "操作失败",
                "mode": "independent"
            }


# ═══════════════════════════════════════════════════════════════════
# Claw协作协调器
# ═══════════════════════════════════════════════════════════════════

class ClawCollaborationCoordinator:
    """
    Claw协作协调器
    
    管理多个Claw的协作：
    - 确定主导Claw
    - 分配协作者
    - 协调消息传递
    - 整合响应
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        self.root = project_root or Path(__file__).resolve().parents[4]
        self._workers: Dict[str, ClawIndependentWorker] = {}
        self._message_log: List[CollaboratorMessage] = []
        
        logger.info("[ClawCoordinator] 协作协调器初始化")
    
    def register_worker(self, name: str, worker: ClawIndependentWorker) -> None:
        """注册Claw工作器"""
        self._workers[name] = worker
        logger.info(f"[ClawCoordinator] 注册工作器: {name}")
    
    def get_worker(self, name: str) -> Optional[ClawIndependentWorker]:
        """获取工作器"""
        return self._workers.get(name)
    
    def list_workers(self) -> List[str]:
        """列出所有工作器"""
        return list(self._workers.keys())
    
    async def collaborate(
        self,
        query: str,
        primary: str,
        collaborators: List[str],
        context: Optional[str] = None
    ) -> CollaborationResult:
        """
        协作处理查询
        
        Args:
            query: 用户查询
            primary: 主导Claw名称
            collaborators: 协作者列表
            context: 上下文
            
        Returns:
            CollaborationResult: 协作结果
        """
        start_time = datetime.now()
        
        # 验证Claw存在
        primary_worker = self._workers.get(primary)
        if not primary_worker:
            return CollaborationResult(
                success=False,
                primary_response="",
                error=f"主导Claw '{primary}' 不存在"
            )
        
        try:
            # 1. 主导Claw处理
            primary_result = await primary_worker.process(query, context)
            
            # 2. 协作者处理（支持所有协作者，并发执行）
            collab_responses = {}
            
            async def process_collab(collab_name: str) -> tuple:
                """并发处理单个协作者"""
                collab_worker = self._workers.get(collab_name)
                if not collab_worker:
                    return collab_name, ""
                
                # 发送协作消息
                msg = CollaboratorMessage(
                    sender=primary,
                    receiver=collab_name,
                    content=f"需要协助: {query}",
                    context=context or ""
                )
                self._message_log.append(msg)
                
                # 协作者处理
                collab_result = await collab_worker.process(
                    f"补充视角: {query}",
                    context=f"来自{primary}的协作请求"
                )
                return collab_name, collab_result.get("response", "")
            
            # 并发执行所有协作者
            if collaborators:
                collab_tasks = [process_collab(c) for c in collaborators]
                collab_results = await asyncio.gather(*collab_tasks, return_exceptions=True)
                
                for collab_name, response in collab_results:
                    if isinstance(response, Exception):
                        logger.warning(f"[ClawCoordinator] 协作者{collab_name}处理失败: {response}")
                        collab_responses[collab_name] = f"[错误: {str(response)}]"
                    else:
                        collab_responses[collab_name] = response
            
            # 3. 整合响应
            elapsed = (datetime.now() - start_time).total_seconds()
            
            return CollaborationResult(
                success=True,
                primary_response=primary_result.get("response", ""),
                collaborator_responses=collab_responses,
                total_time=elapsed
            )
            
        except Exception as e:
            logger.error(f"[ClawCoordinator] 协作失败: {e}")
            return CollaborationResult(
                success=False,
                primary_response="",
                error="执行失败",
                total_time=(datetime.now() - start_time).total_seconds()
            )
    
    def get_message_history(
        self,
        claw_name: Optional[str] = None
    ) -> List[CollaboratorMessage]:
        """获取消息历史"""
        if claw_name:
            return [
                m for m in self._message_log
                if m.sender == claw_name or m.receiver == claw_name
            ]
        return self._message_log


# ═══════════════════════════════════════════════════════════════════
# ClawEngine主类
# ═══════════════════════════════════════════════════════════════════

class ClawEngine:
    """
    ClawEngine主类
    
    统一入口，支持：
    - 独立工作模式
    - 协作工作模式
    - 每个Claw独立记忆存储
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        self.root = project_root or Path(__file__).resolve().parents[4]
        self.coordinator = ClawCollaborationCoordinator(self.root)
        
        # 加载所有Claw
        self._load_all_claws()
        
        logger.info(f"[ClawEngine] 初始化完成，{len(self.coordinator.list_workers())}个Claw就绪")
    
    def _load_all_claws(self) -> None:
        """加载所有Claw为独立工作器"""
        from ._claw_architect import create_claw, list_all_configs
        
        # 列出所有配置
        configs_dir = self.root / "smart_office_assistant" / "src" / "intelligence" / "claws" / "configs"
        all_names = list_all_configs(configs_dir)
        
        # 加载所有Claw配置（无数量限制）
        for name in all_names:
            try:
                architect = create_claw(name, configs_dir)
                if architect:
                    worker = ClawIndependentWorker(
                        name=name,
                        metadata=architect.metadata,
                        architect=architect,
                        project_root=self.root
                    )
                    self.coordinator.register_worker(name, worker)
            except Exception as e:
                logger.warning(f"[ClawEngine] 加载{name}失败: {e}")
    
    async def ask(
        self,
        query: str,
        claw_name: Optional[str] = None,
        collaborators: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        提问
        
        Args:
            query: 问题
            claw_name: 指定Claw（可选，自动路由）
            collaborators: 协作者列表（可选）
            
        Returns:
            Dict: 处理结果
        """
        # 确定Claw
        if not claw_name:
            # 自动路由到孔子（默认）
            claw_name = "孔子"
        
        # 判断工作模式
        if collaborators:
            # 协作模式
            result = await self.coordinator.collaborate(
                query=query,
                primary=claw_name,
                collaborators=collaborators
            )
            return {
                "success": result.success,
                "response": result.primary_response,
                "collaborators": result.collaborator_responses,
                "mode": "collaborative",
                "elapsed": result.total_time
            }
        else:
            # 独立模式
            worker = self.coordinator.get_worker(claw_name)
            if not worker:
                return {"success": False, "error": f"Claw '{claw_name}' 不存在"}
            
            result = await worker.process(query)
            return {
                "success": result["success"],
                "response": result.get("response", ""),
                "soul_result": result.get("soul_result"),
                "learning_result": result.get("learning_result"),
                "mode": "independent",
                "elapsed": result.get("elapsed_seconds", 0)
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """获取系统统计"""
        workers = self.coordinator.list_workers()
        
        stats = {
            "total_claws": len(workers),
            "workers": {}
        }
        
        for name in workers:
            worker = self.coordinator.get_worker(name)
            if worker:
                stats["workers"][name] = {
                    "memory_dir": str(worker.memory_dir),
                    "has_soul": bool(worker.metadata.soul.beliefs),
                    "has_identity": bool(worker.metadata.identity.name)
                }
        
        return stats
    
    def list_all_claws(self) -> List[str]:
        """列出所有可用的Claw名称"""
        return list(self.coordinator.list_workers())
    
    async def ask_with_all(
        self,
        query: str,
        exclude: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        与所有Claw协作
        
        Args:
            query: 问题
            exclude: 排除的Claw列表
            
        Returns:
            Dict: 所有Claw的响应
        """
        all_claws = self.list_all_claws()
        exclude = exclude or []
        collaborators = [c for c in all_claws if c not in exclude]
        
        # 使用第一个Claw作为主导
        primary = collaborators[0] if collaborators else "孔子"
        other_collabs = collaborators[1:] if len(collaborators) > 1 else []
        
        result = await self.ask(query, claw_name=primary, collaborators=other_collabs)
        result["all_participants"] = collaborators
        return result


# ═══════════════════════════════════════════════════════════
# 导出
# ═══════════════════════════════════════════════════════════

__all__ = [
    "CollaboratorMessage",
    "CollaborationResult",
    "ClawIndependentWorker",
    "ClawCollaborationCoordinator",
    "ClawEngine",
]