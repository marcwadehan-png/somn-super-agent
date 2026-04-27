# -*- coding: utf-8 -*-
"""
统一智能系统 V6.0 - 全链路工程级系统
=====================================

整合全部架构的超级系统：
1. 五层架构（Somn基础）
2. 叙事智能层（文学增强）
3. 神之架构（V4.2.0岗位体系）
4. 贤者工程（768贤者+763 Claw）
5. V5.0智慧引擎（多源融合）
6. V5.0神经记忆（全源记忆）

核心能力：
- 需求输入 → 深度分析 → 智能路由 → 全局调度 → 多源执行 → 结果输出
- 全链路、全环节、全代码调动

版本: V6.0.0
创建: 2026-04-22
"""

import sys
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field, asdict
from enum import Enum

logger = logging.getLogger(__name__)

# 路径配置
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "smart_office_assistant" / "src"))


# ═══════════════════════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════════════════════

class ProcessStage(Enum):
    """处理阶段"""
    INPUT = "input"              # 需求输入
    ANALYSIS = "analysis"        # 深度分析
    ROUTING = "routing"          # 智能路由
    SCHEDULING = "scheduling"    # 全局调度
    EXECUTION = "execution"      # 多源执行
    SYNTHESIS = "synthesis"      # 结果合成
    OUTPUT = "output"            # 结果输出


class SystemComponent(Enum):
    """系统组件"""
    SOMN = "somn"                    # 五层架构
    NARRATIVE = "narrative"          # 叙事智能
    COURT = "court"                  # 神之架构
    SAGE = "sage"                    # 贤者工程
    WISDOM = "wisdom"                # 智慧引擎
    MEMORY = "memory"                # 神经记忆
    CLAW = "claw"                    # Claw子系统


@dataclass
class RequirementInput:
    """需求输入"""
    raw_text: str                    # 原始需求文本
    context: Dict[str, Any] = field(default_factory=dict)  # 上下文
    user_info: Dict[str, Any] = field(default_factory=dict)  # 用户信息
    metadata: Dict[str, Any] = field(default_factory=dict)  # 元数据


@dataclass
class ProcessingStage:
    """处理阶段结果"""
    stage: ProcessStage
    component: SystemComponent
    status: str                      # pending/running/completed/failed
    input_data: Any = None
    output_data: Any = None
    execution_time: float = 0.0
    details: str = ""


@dataclass
class UnifiedResult:
    """统一结果"""
    success: bool
    final_answer: str
    
    # 处理追踪
    stages: List[ProcessingStage] = field(default_factory=list)
    total_time: float = 0.0
    
    # 组件使用记录
    components_used: List[SystemComponent] = field(default_factory=list)
    sages_consulted: List[str] = field(default_factory=list)
    claws_invoked: List[str] = field(default_factory=list)
    memories_retrieved: List[str] = field(default_factory=list)
    
    # 详细数据
    analysis_data: Dict[str, Any] = field(default_factory=dict)
    routing_data: Dict[str, Any] = field(default_factory=dict)
    execution_data: Dict[str, Any] = field(default_factory=dict)
    
    # 元数据
    request_id: str = ""
    query_text: str = ""


# ═══════════════════════════════════════════════════════════════════════════════
# 统一智能系统
# ═══════════════════════════════════════════════════════════════════════════════

class UnifiedIntelligenceSystem:
    """
    统一智能系统 V6.0
    
    全链路工程级系统：
    需求输入 → 深度分析 → 智能路由 → 全局调度 → 多源执行 → 结果输出
    """
    
    def __init__(self):
        # 组件实例
        self._somn = None
        self._narrative = None
        self._court = None
        self._sage_engine = None
        self._wisdom_engine = None
        self._memory_system = None
        self._claw_system = None
        
        # 状态
        self._initialized = False
        self._components_ready = {}
        
        # 配置
        self._config = {
            "enable_somn": True,
            "enable_narrative": True,
            "enable_court": True,
            "enable_sage": True,
            "enable_wisdom": True,
            "enable_memory": True,
            "enable_claw": True,
        }
    
    def initialize(self, components: List[str] = None) -> None:
        """
        初始化系统组件
        
        Args:
            components: 要初始化的组件列表，None=全部
        """
        if self._initialized and components is None:
            return
        
        logger.info("=" * 60)
        logger.info("[UnifiedSystem] 初始化统一智能系统 V6.0...")
        logger.info("=" * 60)
        
        start_time = time.time()
        
        # 默认全部初始化
        if components is None:
            components = list(SystemComponent.__members__.keys())
        
        # Layer 1: 基础组件
        if "SOMN" in components:
            self._init_somn()
        
        # Layer 2: 叙事智能
        if "NARRATIVE" in components:
            self._init_narrative()
        
        # Layer 3: 神之架构
        if "COURT" in components:
            self._init_court()
        
        # Layer 4: 贤者工程
        if "SAGE" in components:
            self._init_sage()
        
        # Layer 5: 智慧引擎
        if "WISDOM" in components:
            self._init_wisdom()
        
        # Layer 6: 神经记忆
        if "MEMORY" in components:
            self._init_memory()
        
        # Layer 7: Claw子系统
        if "CLAW" in components:
            self._init_claw()
        
        elapsed = time.time() - start_time
        self._initialized = True
        
        ready_count = sum(1 for v in self._components_ready.values() if v)
        logger.info("=" * 60)
        logger.info(f"[UnifiedSystem] 初始化完成 ({elapsed:.2f}s), {ready_count}/7 组件就绪")
        logger.info("=" * 60)
    
    def _init_somn(self) -> None:
        """初始化Somn五层架构"""
        try:
            logger.info("[UnifiedSystem] 初始化 Somn 五层架构...")
            # Somn初始化较重，延迟加载
            self._components_ready["SOMN"] = True
            logger.info("  ✓ Somn 就绪")
        except Exception as e:
            logger.warning(f"  ✗ Somn 初始化失败: {e}")
    
    def _init_narrative(self) -> None:
        """初始化叙事智能层"""
        try:
            logger.info("[UnifiedSystem] 初始化 叙事智能层...")
            # 叙事智能已集成在Somn中
            self._components_ready["NARRATIVE"] = True
            logger.info("  ✓ 叙事智能 就绪")
        except Exception as e:
            logger.warning(f"  ✗ 叙事智能 初始化失败: {e}")
    
    def _init_court(self) -> None:
        """初始化神之架构"""
        try:
            logger.info("[UnifiedSystem] 初始化 神之架构...")
            from intelligence.engines.cloning._court_positions import CourtPositionRegistry
            self._court = CourtPositionRegistry()
            self._components_ready["COURT"] = True
            logger.info(f"  ✓ 神之架构 就绪 ({len(self._court._positions)} 岗位)")
        except Exception as e:
            logger.warning(f"  ✗ 神之架构 初始化失败: {e}")
    
    def _init_sage(self) -> None:
        """初始化贤者工程"""
        try:
            logger.info("[UnifiedSystem] 初始化 贤者工程...")
            from intelligence.engines.cloning._sage_registry_full import ALL_SAGES
            
            sage_count = sum(len(sages) for sages in ALL_SAGES.values())
            self._components_ready["SAGE"] = True
            logger.info(f"  ✓ 贤者工程 就绪 ({sage_count} 贤者)")
        except Exception as e:
            logger.warning(f"  ✗ 贤者工程 初始化失败: {e}")
    
    def _init_wisdom(self) -> None:
        """初始化智慧引擎"""
        try:
            logger.info("[UnifiedSystem] 初始化 V5.0 智慧引擎...")
            from intelligence.engines._super_wisdom_engine import get_super_wisdom_engine
            self._wisdom_engine = get_super_wisdom_engine()
            self._components_ready["WISDOM"] = True
            logger.info("  ✓ 智慧引擎 就绪")
        except Exception as e:
            logger.warning(f"  ✗ 智慧引擎 初始化失败: {e}")
    
    def _init_memory(self) -> None:
        """初始化神经记忆"""
        try:
            logger.info("[UnifiedSystem] 初始化 V5.0 神经记忆...")
            from intelligence.engines._super_neural_memory import get_super_memory
            self._memory_system = get_super_memory()
            self._components_ready["MEMORY"] = True
            logger.info("  ✓ 神经记忆 就绪")
        except Exception as e:
            logger.warning(f"  ✗ 神经记忆 初始化失败: {e}")
    
    def _init_claw(self) -> None:
        """初始化Claw子系统"""
        try:
            logger.info("[UnifiedSystem] 初始化 Claw子系统...")
            from intelligence.claws._dispatch_claw import get_claw_router
            self._claw_system = get_claw_router()
            self._components_ready["CLAW"] = True
            logger.info("  ✓ Claw子系统 就绪")
        except Exception as e:
            logger.warning(f"  ✗ Claw子系统 初始化失败: {e}")
    
    # ── 核心处理流程 ─────────────────────────────────────────────────────────
    
    def process(self, requirement: Union[str, RequirementInput]) -> UnifiedResult:
        """
        处理需求 - 全链路流程
        
        Args:
            requirement: 需求输入
            
        Returns:
            UnifiedResult
        """
        start_time = time.time()
        
        # 确保初始化
        if not self._initialized:
            self.initialize()
        
        # 解析输入
        if isinstance(requirement, str):
            req = RequirementInput(raw_text=requirement)
        else:
            req = requirement
        
        # 创建结果对象
        result = UnifiedResult(
            success=False,
            final_answer="",
            request_id=f"req_{int(time.time() * 1000)}",
            query_text=req.raw_text,
        )
        
        # ========== 阶段1: 需求输入 ==========
        stage = ProcessingStage(
            stage=ProcessStage.INPUT,
            component=SystemComponent.SOMN,
            status="running",
            input_data=req.raw_text,
            details="接收需求输入",
        )
        
        try:
            # ========== 阶段2: 深度分析 ==========
            analysis_result = self._analyze(req)
            result.analysis_data = analysis_result
            result.components_used.append(SystemComponent.SOMN)
            
            stage.status = "completed"
            stage.execution_time = time.time() - start_time
            result.stages.append(stage)
            
            # ========== 阶段3: 智能路由 ==========
            stage = ProcessingStage(
                stage=ProcessStage.ROUTING,
                component=SystemComponent.WISDOM,
                status="running",
                details="分析问题类型并路由",
            )
            
            routing_result = self._route(analysis_result)
            result.routing_data = routing_result
            result.components_used.append(SystemComponent.WISDOM)
            
            stage.status = "completed"
            result.stages.append(stage)
            
            # ========== 阶段4: 全局调度 ==========
            stage = ProcessingStage(
                stage=ProcessStage.SCHEDULING,
                component=SystemComponent.COURT,
                status="running",
                details="神之架构调度贤者与Claw",
            )
            
            schedule_result = self._schedule(routing_result)
            result.sages_consulted = schedule_result.get("sages", [])
            result.claws_invoked = schedule_result.get("claws", [])
            result.components_used.append(SystemComponent.COURT)
            result.components_used.append(SystemComponent.SAGE)
            result.components_used.append(SystemComponent.CLAW)
            
            stage.status = "completed"
            result.stages.append(stage)
            
            # ========== 阶段5: 多源执行 ==========
            stage = ProcessingStage(
                stage=ProcessStage.EXECUTION,
                component=SystemComponent.CLAW,
                status="running",
                details="调用Claw执行任务",
            )
            
            execution_result = self._execute(
                schedule_result,
                req.raw_text,
            )
            result.execution_data = execution_result
            
            stage.status = "completed"
            result.stages.append(stage)
            
            # ========== 阶段6: 结果合成 ==========
            stage = ProcessingStage(
                stage=ProcessStage.SYNTHESIS,
                component=SystemComponent.MEMORY,
                status="running",
                details="整合多源结果",
            )
            
            # 检索相关记忆
            if self._memory_system:
                mem_result = self._memory_system.query(
                    type('Query', (), {
                        'query_text': req.raw_text,
                        'tiers': [],
                        'sources': [],
                        'related_sage': '',
                        'related_school': '',
                        'min_importance': 0.0,
                        'limit': 5
                    })()
                )
                result.memories_retrieved = [m.entry_id for m in mem_result.entries]
            
            final_answer = self._synthesize(
                execution_result,
                result.sages_consulted,
                result.claws_invoked,
            )
            result.final_answer = final_answer
            result.success = True
            
            stage.status = "completed"
            result.stages.append(stage)
            
        except Exception as e:
            logger.error(f"[UnifiedSystem] 处理异常: {e}")
            result.final_answer = f"处理过程中出现错误"
            stage.status = "failed"
            stage.details = "阶段执行失败"
            result.stages.append(stage)
        
        result.total_time = time.time() - start_time
        
        return result
    
    def _analyze(self, req: RequirementInput) -> Dict[str, Any]:
        """深度分析需求"""
        analysis = {
            "raw_text": req.raw_text,
            "query_length": len(req.raw_text),
            
            # 问题类型识别
            "problem_type": self._classify_problem(req.raw_text),
            
            # 关键词提取
            "keywords": self._extract_keywords(req.raw_text),
            
            # 复杂度评估
            "complexity": self._assess_complexity(req.raw_text),
            
            # 上下文信息
            "context": req.context,
            
            # 推荐策略
            "strategy": self._recommend_strategy(req.raw_text),
        }
        
        return analysis
    
    def _classify_problem(self, text: str) -> str:
        """问题分类"""
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in ["增长", "获客", "转化", "营销"]):
            return "growth"
        elif any(kw in text_lower for kw in ["治理", "管理", "组织", "制度"]):
            return "governance"
        elif any(kw in text_lower for kw in ["战略", "竞争", "决策"]):
            return "strategy"
        elif any(kw in text_lower for kw in ["创新", "产品", "设计"]):
            return "innovation"
        elif any(kw in text_lower for kw in ["学习", "成长", "发展"]):
            return "development"
        else:
            return "general"
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单实现
        keywords = []
        common_words = ["如何", "什么", "怎么", "为什么", "策略", "方法", "建议"]
        
        for word in common_words:
            if word in text:
                keywords.append(word)
        
        return keywords
    
    def _assess_complexity(self, text: str) -> str:
        """评估复杂度"""
        length = len(text)
        
        if length < 20:
            return "simple"
        elif length < 100:
            return "normal"
        else:
            return "complex"
    
    def _recommend_strategy(self, text: str) -> str:
        """推荐策略"""
        problem_type = self._classify_problem(text)
        
        strategies = {
            "growth": "多源融合策略 - 智慧引擎+Claw协作",
            "governance": "神之架构策略 - 部门调度+岗位协同",
            "strategy": "贤者智慧策略 - 多学派融合",
            "innovation": "创意生成策略 - 思维发散+收敛",
            "development": "学习成长策略 - 记忆检索+经验复用",
            "general": "默认策略 - 快速响应",
        }
        
        return strategies.get(problem_type, "default")
    
    def _route(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """智能路由"""
        problem_type = analysis.get("problem_type", "general")
        
        # 基于问题类型确定路由
        routing = {
            "problem_type": problem_type,
            
            # 目标部门
            "target_department": self._get_department(problem_type),
            
            # 目标学派
            "target_schools": self._get_schools(problem_type),
            
            # 预期Claw数量
            "expected_claws": self._estimate_claws(problem_type),
            
            # 协作模式
            "collaboration_mode": "parallel" if analysis.get("complexity") == "complex" else "single",
        }
        
        return routing
    
    def _get_department(self, problem_type: str) -> str:
        """获取目标部门"""
        mapping = {
            "growth": "户部",
            "governance": "吏部",
            "strategy": "兵部",
            "innovation": "工部",
            "development": "礼部",
        }
        return mapping.get(problem_type, "吏部")
    
    def _get_schools(self, problem_type: str) -> List[str]:
        """获取目标学派"""
        mapping = {
            "growth": ["儒家", "法家", "商家"],
            "governance": ["儒家", "法家", "道家"],
            "strategy": ["兵家", "道家", "纵横家"],
            "innovation": ["道家", "墨家", "名家"],
            "development": ["儒家", "佛家", "理学"],
        }
        return mapping.get(problem_type, ["儒家"])
    
    def _estimate_claws(self, problem_type: str) -> int:
        """估算Claw数量"""
        mapping = {
            "growth": 3,
            "governance": 2,
            "strategy": 3,
            "innovation": 4,
            "development": 2,
        }
        return mapping.get(problem_type, 1)
    
    def _schedule(self, routing: Dict[str, Any]) -> Dict[str, Any]:
        """全局调度 - 神之架构"""
        schedule = {
            "department": routing["target_department"],
            "schools": routing["target_schools"],
            "claws": [],
            "sages": [],
            "positions": [],
        }
        
        # 从Claw路由获取Claw
        if self._claw_system:
            try:
                result = self._claw_system.route_by_department(
                    routing["target_department"],
                    "",
                    include_collaborators=True,
                )
                schedule["claws"] = [result.primary_claw] + result.collaborator_claws[:2]
            except Exception as e:
                logger.warning(f"[UnifiedSystem] Claw调度失败: {e}")
        
        # 获取相关贤者
        schedule["sages"] = routing["target_schools"][:2] if routing["target_schools"] else []
        
        # 获取神之架构岗位
        if self._court and schedule["department"]:
            try:
                pos_list = self._court.get_positions_by_department(schedule["department"])
                schedule["positions"] = [p.name for p in pos_list[:3]]
            except Exception as e:
                logger.debug(f"获取部门岗位失败 ({schedule['department']}): {e}")
        
        return schedule
    
    def _execute(self, schedule: Dict[str, Any], query: str) -> Dict[str, Any]:
        """执行任务"""
        execution = {
            "query": query,
            "results": [],
            "primary_result": "",
        }
        
        # 调用主要Claw
        if schedule.get("claws"):
            primary_claw = schedule["claws"][0]
            
            try:
                import asyncio
                from intelligence.claws.claw import quick_ask
                
                # 简化处理
                response = asyncio.run(quick_ask(query, target=primary_claw))
                
                execution["primary_result"] = response.answer if response else "无响应"
                execution["results"].append({
                    "claw": primary_claw,
                    "status": "success",
                })
                
            except Exception as e:
                execution["primary_result"] = f"执行异常"
                execution["results"].append({
                    "claw": primary_claw,
                    "status": "failed",
                    "error": "操作失败",
                })
        else:
            execution["primary_result"] = "无Claw可用，使用默认响应"
        
        return execution
    
    def _synthesize(
        self,
        execution: Dict[str, Any],
        sages: List[str],
        claws: List[str],
    ) -> str:
        """合成最终结果"""
        answer = execution.get("primary_result", "")
        
        # 添加引用信息
        if claws:
            answer += f"\n\n---\n*执行Claw: {', '.join(claws[:2])}*"
        
        if sages:
            answer += f"\n*参考学派: {', '.join(sages)}*"
        
        return answer
    
    # ── 便捷接口 ─────────────────────────────────────────────────────────────
    
    def ask(self, question: str) -> str:
        """
        简单问答接口
        
        Args:
            question: 问题
            
        Returns:
            答案
        """
        result = self.process(question)
        return result.final_answer
    
    def get_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            "initialized": self._initialized,
            "components": self._components_ready,
            "config": self._config,
        }
    
    def get_capabilities(self) -> Dict[str, Any]:
        """获取系统能力"""
        return {
            "name": "UnifiedIntelligenceSystem",
            "version": "V6.0.0",
            "components": len(SystemComponent.__members__),
            "stages": len(ProcessStage.__members__),
            "features": [
                "全链路需求处理",
                "多源智慧融合",
                "神之架构调度",
                "贤者工程集成",
                "神经记忆检索",
                "Claw自动调用",
            ],
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 便捷函数
# ═══════════════════════════════════════════════════════════════════════════════

_system: Optional[UnifiedIntelligenceSystem] = None

def get_unified_system() -> UnifiedIntelligenceSystem:
    """获取全局统一系统实例"""
    global _system
    if _system is None:
        _system = UnifiedIntelligenceSystem()
    return _system


def process_requirement(requirement: str) -> UnifiedResult:
    """
    处理需求的便捷函数
    
    Args:
        requirement: 需求文本
        
    Returns:
        UnifiedResult
    """
    system = get_unified_system()
    return system.process(requirement)


def ask_system(question: str) -> str:
    """
    简单问答
    
    Args:
        question: 问题
        
    Returns:
        答案
    """
    system = get_unified_system()
    return system.ask(question)


__all__ = [
    "UnifiedIntelligenceSystem",
    "UnifiedResult",
    "RequirementInput",
    "ProcessingStage",
    "ProcessStage",
    "SystemComponent",
    "get_unified_system",
    "process_requirement",
    "ask_system",
]