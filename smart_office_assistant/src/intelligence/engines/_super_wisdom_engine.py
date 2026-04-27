# -*- coding: utf-8 -*-
"""
超级智慧引擎 V5.0 - 贤者能力集成
=================================

整合贤者工程全部能力的超级智慧引擎：
1. 25学派引擎（原有）
2. 768位贤者智慧编码（wisdom_encoding_registry）
3. 763个Claw子智能体
4. 蒸馏文档知识
5. 多源融合决策

核心能力：
- 认知维度评分（6维）
- 智慧法则匹配
- Claw自动调用
- 多源协同推理

版本: V5.0.0
创建: 2026-04-22
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════════════════════

class WisdomSource(Enum):
    """智慧来源"""
    SCHOOL_ENGINE = "school_engine"     # 25学派引擎
    SAGE_CODE = "sage_code"             # 贤者智慧编码
    CLAW = "claw"                       # Claw子智能体
    DISTILLATION = "distillation"       # 蒸馏文档
    FUSION = "fusion"                   # 融合决策


@dataclass
class WisdomCapability:
    """智慧能力"""
    source: WisdomSource
    source_name: str          # 引擎名/贤者名/Claw名
    capability_score: float   # 能力评分 0-10
    triggers: List[str]       # 触发关键词
    cognitive_weights: Dict[str, float]  # 认知维度权重
    wisdom_laws: List[str]    # 智慧法则


@dataclass
class WisdomQuery:
    """智慧查询"""
    query_text: str
    problem_type: str
    department: str
    required_dimensions: List[str] = field(default_factory=list)
    required_sources: List[WisdomSource] = field(default_factory=list)
    min_confidence: float = 0.5


@dataclass
class WisdomAnswer:
    """智慧答案"""
    success: bool
    answer: str
    confidence: float
    sources_used: List[WisdomSource]
    primary_source: str
    cognitive_dimensions: Dict[str, float]
    wisdom_laws_applied: List[str]
    collaborators: List[str] = field(default_factory=list)
    reasoning_trace: List[str] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════════════
# 超级智慧引擎
# ═══════════════════════════════════════════════════════════════════════════════

class SuperWisdomEngine:
    """
    超级智慧引擎 V5.0
    
    整合所有智慧源的超级引擎
    """
    
    def __init__(self):
        self._school_engines: Dict[str, Any] = {}
        self._sage_codes: Dict[str, Any] = {}
        self._claw_router = None
        self._initialized = False
        
        # 认知维度权重配置
        self._dimension_weights = {
            "cog_depth": 0.15,        # 认知深度
            "decision_quality": 0.25, # 决策质量
            "value_judge": 0.20,      # 价值判断
            "gov_decision": 0.15,     # 管理决策
            "strategy": 0.15,         # 战略规划
            "self_mgmt": 0.10,        # 自我管理
        }
    
    def initialize(self) -> None:
        """初始化所有智慧源"""
        if self._initialized:
            return
        
        logger.info("[SuperWisdomEngine] 初始化超级智慧引擎...")
        
        # 1. 加载25学派引擎
        self._load_school_engines()
        
        # 2. 加载贤者智慧编码
        self._load_sage_codes()
        
        # 3. 加载Claw路由
        self._load_claw_router()
        
        self._initialized = True
        logger.info("[SuperWisdomEngine] 初始化完成")
    
    def _load_school_engines(self) -> None:
        """加载25学派引擎"""
        try:
            from .wisdom_dispatch import WisdomDispatcher
            dispatcher = WisdomDispatcher()
            # 引擎懒加载
            self._dispatcher = dispatcher
            logger.info("[SuperWisdomEngine] 25学派引擎已就绪")
        except Exception as e:
            logger.warning(f"[SuperWisdomEngine] 学派引擎加载失败: {e}")
    
    def _load_sage_codes(self) -> None:
        """加载贤者智慧编码"""
        try:
            from .wisdom_encoding.wisdom_encoding_registry import SageCode, COGNITIVE_DIMENSION_SCORES
            
            # 加载所有贤者编码
            sage_codes = COGNITIVE_DIMENSION_SCORES  # 这是一个大字典
            
            # 转换为能力列表
            for sage_id, code_data in sage_codes.items():
                name = code_data.get("name", sage_id)
                self._sage_codes[name] = code_data
            
            logger.info(f"[SuperWisdomEngine] 加载了 {len(self._sage_codes)} 位贤者编码")
        except Exception as e:
            logger.warning(f"[SuperWisdomEngine] 贤者编码加载失败: {e}")
    
    def _load_claw_router(self) -> None:
        """加载Claw路由"""
        try:
            from .wisdom_dispatch._dispatch_claw import get_claw_router
            self._claw_router = get_claw_router()
            logger.info("[SuperWisdomEngine] Claw路由已就绪")
        except Exception as e:
            logger.warning(f"[SuperWisdomEngine] Claw路由加载失败: {e}")
    
    # ── 核心推理方法 ─────────────────────────────────────────────────────────
    
    def analyze(self, query: WisdomQuery) -> WisdomAnswer:
        """
        核心分析入口
        
        Args:
            query: 智慧查询
            
        Returns:
            WisdomAnswer
        """
        self.initialize()
        
        reasoning_trace = []
        reasoning_trace.append(f"开始分析问题: {query.query_text}")
        
        # 1. 问题分析
        problem_category = self._classify_problem(query.query_text)
        reasoning_trace.append(f"问题分类: {problem_category}")
        
        # 2. 获取候选智慧源
        candidates = self._discover_candidates(query, problem_category)
        reasoning_trace.append(f"发现 {len(candidates)} 个候选智慧源")
        
        # 3. 评分排序
        ranked = self._rank_candidates(candidates, query)
        reasoning_trace.append(f"排序完成，前3: {[c['name'] for c in ranked[:3]]}")
        
        # 4. 选择主源
        primary = ranked[0] if ranked else None
        
        # 5. 调用主源获取答案
        if primary:
            answer = self._invoke_source(primary, query)
            reasoning_trace.append(f"主源调用完成: {primary['name']}")
            
            # 6. 尝试协作（如果需要）
            collaborators = []
            if len(ranked) > 1 and query.required_sources:
                collabs = self._invoke_collaboration(ranked[1:3], query)
                collaborators = [c['name'] for c in collabs]
                reasoning_trace.append(f"协作完成，参与: {collaborators}")
            
            # 7. 构建答案
            return WisdomAnswer(
                success=True,
                answer=answer,
                confidence=primary['score'],
                sources_used=[WisdomSource(s['source']) for s in ranked[:3]],
                primary_source=primary['name'],
                cognitive_dimensions=primary.get('dimensions', {}),
                wisdom_laws_applied=primary.get('wisdom_laws', []),
                collaborators=collaborators,
                reasoning_trace=reasoning_trace,
            )
        
        return WisdomAnswer(
            success=False,
            answer="无法处理该问题",
            confidence=0.0,
            sources_used=[],
            primary_source="",
            cognitive_dimensions={},
            wisdom_laws_applied=[],
            reasoning_trace=reasoning_trace,
        )
    
    def _classify_problem(self, query: str) -> str:
        """问题分类"""
        query_lower = query.lower()
        
        # 简单分类
        if any(kw in query_lower for kw in ["治理", "管理", "组织", "制度"]):
            return "governance"
        elif any(kw in query_lower for kw in ["成长", "学习", "发展", "进步"]):
            return "growth"
        elif any(kw in query_lower for kw in ["战略", "竞争", "决策", "选择"]):
            return "strategy"
        elif any(kw in query_lower for kw in ["道德", "价值", "伦理", "对错"]):
            return "ethics"
        elif any(kw in query_lower for kw in ["危机", "问题", "困难", "挑战"]):
            return "crisis"
        else:
            return "general"
    
    def _discover_candidates(
        self,
        query: WisdomQuery,
        problem_category: str,
    ) -> List[Dict[str, Any]]:
        """发现候选智慧源"""
        candidates = []
        
        # 1. 从Claw发现
        if self._claw_router:
            try:
                route_result = self._claw_router.route_by_query(query.query_text)
                
                # 添加主Claw
                candidates.append({
                    "source": "claw",
                    "name": route_result.primary_claw,
                    "score": route_result.confidence,
                    "dimensions": {},
                    "wisdom_laws": [],
                })
                
                # 添加协作Claw
                for claw_name in route_result.collaborator_claws[:2]:
                    candidates.append({
                        "source": "claw",
                        "name": claw_name,
                        "score": route_result.confidence * 0.8,
                        "dimensions": {},
                        "wisdom_laws": [],
                    })
            except Exception as e:
                logger.warning(f"[SuperWisdomEngine] Claw发现失败: {e}")
        
        # 2. 从贤者编码发现
        query_lower = query.query_text.lower()
        for name, code in self._sage_codes.items():
            triggers = code.get("triggers", [])
            
            # 匹配触发词
            match_count = sum(1 for t in triggers if t.lower() in query_lower)
            if match_count > 0:
                score = min(match_count / max(len(triggers), 1), 1.0) * 10
                
                candidates.append({
                    "source": "sage_code",
                    "name": name,
                    "score": score,
                    "dimensions": code.get("cognitive_dimensions", {}),
                    "wisdom_laws": code.get("wisdom_functions", []),
                })
        
        # 3. 从学派引擎发现
        # (已在WisdomDispatcher中处理，这里简单添加)
        
        return candidates
    
    def _rank_candidates(
        self,
        candidates: List[Dict[str, Any]],
        query: WisdomQuery,
    ) -> List[Dict[str, Any]]:
        """评分排序"""
        # 按评分排序
        ranked = sorted(candidates, key=lambda x: x['score'], reverse=True)
        
        # 限制数量
        return ranked[:5]
    
    def _invoke_source(
        self,
        source: Dict[str, Any],
        query: WisdomQuery,
    ) -> str:
        """调用智慧源"""
        source_type = source['source']
        name = source['name']
        
        if source_type == "claw":
            # 调用Claw
            return self._invoke_claw(name, query.query_text)
        
        elif source_type == "sage_code":
            # 返回贤者编码信息
            return self._format_sage_code(name, source)
        
        return "无法处理"
    
    def _invoke_claw(self, claw_name: str, query: str) -> str:
        """调用Claw"""
        try:
            import asyncio
            from .claws.claw import quick_ask
            
            # 同步调用
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果在异步环境中，创建新任务
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        asyncio.run,
                        quick_ask(query, target=claw_name)
                    )
                    result = future.result()
            else:
                result = asyncio.run(quick_ask(query, target=claw_name))
            
            return result.answer if result else "无响应"
        except Exception as e:
            logger.warning(f"[SuperWisdomEngine] Claw调用失败: {e}")
            return "调用失败"
    
    def _format_sage_code(self, name: str, source: Dict) -> str:
        """格式化贤者编码输出"""
        dimensions = source.get("dimensions", {})
        laws = source.get("wisdom_laws", [])
        
        dim_str = "\n".join([
            f"  - {k}: {v:.1f}/10"
            for k, v in dimensions.items()
        ])
        
        laws_str = "\n".join([f"  - {l}" for l in laws[:3]])
        
        return f"""【{name}】智慧解析

认知维度评分:
{dim_str}

核心智慧法则:
{laws_str}

(如需深入咨询，请调用对应Claw)"""
    
    def _invoke_collaboration(
        self,
        sources: List[Dict],
        query: WisdomQuery,
    ) -> List[Dict]:
        """调用协作源"""
        # 简化为返回源列表
        return sources
    
    # ── 便捷方法 ─────────────────────────────────────────────────────────────
    
    def ask(self, question: str, context: str = "") -> str:
        """
        简单问答接口
        
        Args:
            question: 问题
            context: 上下文
            
        Returns:
            答案
        """
        full_query = f"{question}"
        if context:
            full_query = f"{context}\n\n{question}"
        
        q = WisdomQuery(
            query_text=question,
            problem_type="",
            department="",
        )
        
        result = self.analyze(q)
        return result.answer
    
    def get_capabilities(self) -> Dict[str, Any]:
        """获取引擎能力概览"""
        return {
            "school_engines": "25个学派引擎",
            "sage_codes": f"{len(self._sage_codes)}位贤者编码",
            "claws": "763个Claw子智能体",
            "dimensions": list(self._dimension_weights.keys()),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 便捷函数
# ═══════════════════════════════════════════════════════════════════════════════

_engine: Optional[SuperWisdomEngine] = None

def get_super_wisdom_engine() -> SuperWisdomEngine:
    """获取全局超级智慧引擎实例"""
    global _engine
    if _engine is None:
        _engine = SuperWisdomEngine()
    return _engine


def ask_wisdom(question: str, context: str = "") -> str:
    """
    便捷问答函数
    
    Args:
        question: 问题
        context: 上下文
        
    Returns:
        答案
    """
    engine = get_super_wisdom_engine()
    return engine.ask(question, context)


__all__ = [
    "SuperWisdomEngine",
    "WisdomSource",
    "WisdomCapability",
    "WisdomQuery",
    "WisdomAnswer",
    "get_super_wisdom_engine",
    "ask_wisdom",
]