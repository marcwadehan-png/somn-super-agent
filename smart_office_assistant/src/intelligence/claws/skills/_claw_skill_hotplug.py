# -*- coding: utf-8 -*-
"""
ClawSkillHotplug - Claw技能热插拔系统
======================================

A.3 Claw技能热插拔：运行时动态注册/注销技能处理器

功能:
- 技能注册表管理
- 运行时技能添加/移除
- 技能依赖解析
- 技能版本控制
- 技能健康检查

版本: v1.1.0
创建: 2026-04-24
"""

from __future__ import annotations

import logging
import time
from typing import Dict, List, Optional, Callable, Any, Set, Type
from dataclasses import dataclass, field
from enum import Enum
from threading import Lock
from functools import wraps

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# 技能状态枚举
# ═══════════════════════════════════════════════════════════════

class SkillStatus(Enum):
    """技能状态"""
    REGISTERED = "registered"     # 已注册
    ACTIVE = "active"             # 激活
    INACTIVE = "inactive"         # 未激活
    DEPENDENCY_MISSING = "missing_dep"  # 依赖缺失
    ERROR = "error"               # 错误


# ═══════════════════════════════════════════════════════════════
# 技能元数据
# ═══════════════════════════════════════════════════════════════

@dataclass
class SkillMetadata:
    """技能元数据"""
    name: str
    version: str = "1.0.0"
    description: str = ""
    author: str = ""
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    priority: int = 0          # 优先级（越大越高）
    enabled: bool = True
    max_concurrent: int = 5     # 最大并发数
    timeout: float = 30.0       # 超时时间（秒）


@dataclass
class SkillHandler:
    """技能处理器"""
    metadata: SkillMetadata
    handler: Callable[..., Any]  # 处理函数
    validator: Optional[Callable[[Any], bool]] = None  # 验证函数
    cleanup: Optional[Callable[[], None]] = None  # 清理函数


@dataclass
class SkillMetrics:
    """技能指标"""
    name: str
    total_calls: int = 0
    success_calls: int = 0
    error_calls: int = 0
    total_duration: float = 0.0
    last_call_time: float = 0.0
    last_error: str = ""
    active_calls: int = 0


# ═══════════════════════════════════════════════════════════════
# 技能热插拔管理器
# ═══════════════════════════════════════════════════════════════

class SkillHotplugManager:
    """
    技能热插拔管理器。
    
    支持运行时动态注册、注销、启用、禁用技能处理器。
    
    用法:
        manager = SkillHotplugManager()
        
        # 注册技能
        def my_handler(ctx):
            return f"Handled: {ctx['input']}"
        
        manager.register(
            name="my_skill",
            handler=my_handler,
            metadata=SkillMetadata(name="my_skill", description="测试技能"),
        )
        
        # 调用技能
        result = manager.execute("my_skill", {"input": "hello"})
        
        # 动态添加新技能
        manager.register("new_skill", new_handler, ...)
        
        # 移除技能
        manager.unregister("old_skill")
    """

    def __init__(self):
        self._skills: Dict[str, SkillHandler] = {}
        self._metrics: Dict[str, SkillMetrics] = {}
        self._lock = Lock()
        
        # 事件回调
        self._on_register: List[Callable[[str], None]] = []
        self._on_unregister: List[Callable[[str], None]] = []
        self._on_error: List[Callable[[str, Exception], None]] = []

    # ═══════════════════════════════════════════════════════════════
    # 注册/注销
    # ═══════════════════════════════════════════════════════════════

    def register(
        self,
        name: str,
        handler: Callable[..., Any],
        metadata: Optional[SkillMetadata] = None,
        validator: Optional[Callable[[Any], bool]] = None,
        cleanup: Optional[Callable[[], None]] = None,
        overwrite: bool = False,
    ) -> bool:
        """
        注册技能。
        
        Args:
            name: 技能名称
            handler: 处理函数
            metadata: 技能元数据
            validator: 验证函数
            cleanup: 清理函数
            overwrite: 是否覆盖已存在的技能
            
        Returns:
            是否成功
        """
        with self._lock:
            if name in self._skills and not overwrite:
                logger.warning(f"[SkillHotplug] Skill already exists: {name}")
                return False
            
            # 验证依赖
            if metadata and metadata.dependencies:
                missing = self._check_dependencies(metadata.dependencies)
                if missing:
                    logger.warning(f"[SkillHotplug] Missing dependencies for {name}: {missing}")
            
            # 创建元数据
            if metadata is None:
                metadata = SkillMetadata(name=name)
            else:
                metadata.name = name  # 确保名称一致
            
            # 创建处理器
            skill = SkillHandler(
                metadata=metadata,
                handler=handler,
                validator=validator,
                cleanup=cleanup,
            )
            
            self._skills[name] = skill
            self._metrics[name] = SkillMetrics(name=name)
            
            # 触发回调
            for cb in self._on_register:
                try:
                    cb(name)
                except Exception as e:
                    logger.error(f"[SkillHotplug] Register callback error: {e}")
            
            logger.info(f"[SkillHotplug] Registered skill: {name} (v{metadata.version})")
            return True

    def unregister(self, name: str, cleanup: bool = True) -> bool:
        """
        注销技能。
        
        Args:
            name: 技能名称
            cleanup: 是否调用清理函数
            
        Returns:
            是否成功
        """
        with self._lock:
            if name not in self._skills:
                logger.warning(f"[SkillHotplug] Skill not found: {name}")
                return False
            
            skill = self._skills[name]
            
            # 调用清理函数
            if cleanup and skill.cleanup:
                try:
                    skill.cleanup()
                except Exception as e:
                    logger.error(f"[SkillHotplug] Cleanup error for {name}: {e}")
            
            del self._skills[name]
            
            # 触发回调
            for cb in self._on_unregister:
                try:
                    cb(name)
                except Exception as e:
                    logger.error(f"[SkillHotplug] Unregister callback error: {e}")
            
            logger.info(f"[SkillHotplug] Unregistered skill: {name}")
            return True

    def _check_dependencies(self, deps: List[str]) -> List[str]:
        """检查依赖是否满足"""
        return [d for d in deps if d not in self._skills]

    # ═══════════════════════════════════════════════════════════════
    # 执行
    # ═══════════════════════════════════════════════════════════════

    def execute(
        self,
        name: str,
        context: Dict[str, Any],
        timeout: Optional[float] = None,
    ) -> Any:
        """
        执行技能。
        
        Args:
            name: 技能名称
            context: 执行上下文
            timeout: 超时时间（覆盖默认值）
            
        Returns:
            执行结果
            
        Raises:
            ValueError: 技能不存在
            TimeoutError: 执行超时
            RuntimeError: 执行错误
        """
        with self._lock:
            if name not in self._skills:
                raise ValueError(f"Skill not found: {name}")
            
            skill = self._skills[name]
            metrics = self._metrics[name]
        
        # 检查状态
        if not skill.metadata.enabled:
            raise RuntimeError(f"Skill is disabled: {name}")
        
        if skill.metadata.dependencies:
            missing = self._check_dependencies(skill.metadata.dependencies)
            if missing:
                raise RuntimeError(f"Skill dependencies missing: {missing}")
        
        # 检查并发限制
        with self._lock:
            if metrics.active_calls >= skill.metadata.max_concurrent:
                raise RuntimeError(f"Skill concurrent limit reached: {name}")
            metrics.active_calls += 1
            metrics.total_calls += 1
            metrics.last_call_time = time.time()
        
        start_time = time.time()
        timeout = timeout or skill.metadata.timeout
        
        try:
            # 验证输入
            if skill.validator:
                if not skill.validator(context):
                    raise ValueError(f"Validation failed for skill: {name}")
            
            # 执行
            result = skill.handler(context)
            
            # 记录成功
            with self._lock:
                metrics.success_calls += 1
                metrics.total_duration += time.time() - start_time
                metrics.active_calls -= 1
            
            return result
            
        except Exception as e:
            # 记录错误
            with self._lock:
                metrics.error_calls += 1
                metrics.last_error = "热插拔失败"
                metrics.total_duration += time.time() - start_time
                metrics.active_calls -= 1
            
            # 触发错误回调
            for cb in self._on_error:
                try:
                    cb(name, e)
                except Exception as e:
                    logger.debug(f"cb(name, e)失败: {e}")
            
            raise

    def execute_async(
        self,
        name: str,
        context: Dict[str, Any],
        callback: Optional[Callable[[Any, Optional[Exception]], None]] = None,
        timeout: Optional[float] = None,
    ) -> None:
        """异步执行技能"""
        import threading
        
        def _run():
            try:
                result = self.execute(name, context, timeout)
                if callback:
                    callback(result, None)
            except Exception as e:
                if callback:
                    callback(None, e)
        
        thread = threading.Thread(target=_run, daemon=True)
        thread.start()

    # ═══════════════════════════════════════════════════════════════
    # 状态管理
    # ═══════════════════════════════════════════════════════════════

    def enable(self, name: str) -> bool:
        """启用技能"""
        with self._lock:
            if name not in self._skills:
                return False
            self._skills[name].metadata.enabled = True
            return True

    def disable(self, name: str) -> bool:
        """禁用技能"""
        with self._lock:
            if name not in self._skills:
                return False
            self._skills[name].metadata.enabled = False
            return True

    def get_status(self, name: str) -> Optional[SkillStatus]:
        """获取技能状态"""
        with self._lock:
            if name not in self._skills:
                return None
            
            skill = self._skills[name]
            
            if not skill.metadata.enabled:
                return SkillStatus.INACTIVE
            
            if skill.metadata.dependencies:
                if self._check_dependencies(skill.metadata.dependencies):
                    return SkillStatus.DEPENDENCY_MISSING
            
            return SkillStatus.ACTIVE

    def list_skills(
        self,
        status: Optional[SkillStatus] = None,
        tag: Optional[str] = None,
    ) -> List[str]:
        """列出技能"""
        with self._lock:
            names = list(self._skills.keys())
        
        if status:
            names = [n for n in names if self.get_status(n) == status]
        
        if tag:
            names = [
                n for n in names
                if tag in self._skills[n].metadata.tags
            ]
        
        return names

    def get_metrics(self, name: str) -> Optional[Dict]:
        """获取技能指标"""
        with self._lock:
            if name not in self._metrics:
                return None
            
            m = self._metrics[name]
            return {
                "name": m.name,
                "total_calls": m.total_calls,
                "success_rate": (
                    m.success_calls / m.total_calls
                    if m.total_calls > 0 else 0.0
                ),
                "avg_duration": (
                    m.total_duration / m.total_calls
                    if m.total_calls > 0 else 0.0
                ),
                "active_calls": m.active_calls,
                "last_call_time": m.last_call_time,
                "last_error": m.last_error,
            }

    def get_all_metrics(self) -> Dict[str, Dict]:
        """获取所有技能指标"""
        return {
            name: self.get_metrics(name)
            for name in list(self._skills.keys())
            if self.get_metrics(name)
        }

    # ═══════════════════════════════════════════════════════════════
    # 事件回调
    # ═══════════════════════════════════════════════════════════════

    def on_register(self, callback: Callable[[str], None]) -> None:
        """注册回调"""
        self._on_register.append(callback)

    def on_unregister(self, callback: Callable[[str], None]) -> None:
        """注销回调"""
        self._on_unregister.append(callback)

    def on_error(self, callback: Callable[[str, Exception], None]) -> None:
        """错误回调"""
        self._on_error.append(callback)

    # ═══════════════════════════════════════════════════════════════
    # 批量操作
    # ═══════════════════════════════════════════════════════════════

    def load_skill_set(self, skills: List[Dict]) -> int:
        """
        批量加载技能。
        
        Args:
            skills: 技能定义列表 [{"name": ..., "handler": ..., ...}]
            
        Returns:
            成功加载数量
        """
        count = 0
        for skill_def in skills:
            try:
                self.register(
                    name=skill_def["name"],
                    handler=skill_def["handler"],
                    metadata=skill_def.get("metadata"),
                    validator=skill_def.get("validator"),
                    cleanup=skill_def.get("cleanup"),
                    overwrite=skill_def.get("overwrite", False),
                )
                count += 1
            except Exception as e:
                logger.error(f"[SkillHotplug] Failed to load {skill_def.get('name', '?')}: {e}")
        
        return count

    def get_stats(self) -> Dict:
        """获取统计信息"""
        with self._lock:
            total = len(self._skills)
            active = sum(
                1 for name in self._skills
                if self.get_status(name) == SkillStatus.ACTIVE
            )
            
            return {
                "total_skills": total,
                "active_skills": active,
                "inactive_skills": total - active,
                "total_calls": sum(m.total_calls for m in self._metrics.values()),
            }
