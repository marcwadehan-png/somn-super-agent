"""
超级学习引擎 - 整合所有学习能力的unified入口
Super Learning Engine - Unified Entry for All Learning Capabilities

功能:
1. 整合分散的学习引擎
2. 智能学习任务路由
3. 学习效果评估
4. 学习strategy优化
5. 叙事学习能力 [v4.1.0 文学智能增强]

版本: v1.0 -> v2.0 (模块化拆分)
日期: 2026-04-08
"""

__all__ = [
    'close',
    'get_all_engine_info',
    'get_engine_by_capability',
    'get_engine_info',
    'get_learning_history',
    'get_stats',
    'get_stats_by_capability',
    'learn',
    'learn_parallel',
    'main',
    'optimize_learning_strategy',
    'parallel_learn',
    'register_engine',
    'route_request_to_engine',
]

import sys
import threading
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from loguru import logger

# 路径引导
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.paths import LEARNING_DIR

# 子模块导入
from ._sle_types import (
    LearningCapability, LearningRequest, LearningResult,
    LearningStats, EngineLoadInfo
)
from ._sle_engines import init_engines, create_capability_engine_map
from ._sle_routing import (
    execute_with_timeout, execute_learning,
    learn_with_unified, learn_with_neural, learn_with_smart,
    learn_with_core, learn_with_meta, learn_with_narrative
)

class SuperLearningEngine:

    """
    超级学习引擎 - 整合所有学习能力的unified入口
    
    核心特性:
    1. 多引擎整合 - unified所有学习引擎
    2. 智能路由 - 根据任务特性选择最适合的引擎
    3. 并行学习 - 多引擎协同学习
    4. 效果评估 - 学习效果实时评估
    5. strategy优化 - 持续优化学习strategy
    6. 叙事学习 - 基于文学叙事方法论的深度学习 [v4.1.0]
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化超级学习引擎
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.base_path = Path(
            self.config.get("base_path")
            or self.config.get("storage_path")
            or str(LEARNING_DIR)
        )
        self.max_workers = self.config.get(
            "max_workers",
            self.config.get("max_concurrent_tasks", 4)
        )
        self.enable_parallel = self.config.get("enable_parallel", True)
        self.enable_learning_stats = self.config.get("enable_learning_stats", True)
        self.enable_performance_monitoring = self.config.get(
            "enable_performance_monitoring", False
        )
        self.request_timeout = self.config.get("request_timeout", 300.0)
        
        # 初始化所有学习引擎
        self.engines = {}
        self._init_engines()
        
        # 学习能力映射
        self.capability_engine_map = create_capability_engine_map()
        
        # 学习历史
        self.learning_history: List[LearningResult] = []
        self.history_lock = threading.Lock()
        
        # 学习统计
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_execution_time": 0.0,
            "engine_usage": {}
        }
        
        # 线程池
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)

        logger.info("超级学习引擎初始化完成")
        logger.info(f"  整合引擎: {len(self.engines)}")
        logger.info(f"  支持能力: {len(LearningCapability)}")
    
    def _init_engines(self):
        """初始化所有学习引擎"""
        self.engines = init_engines(self.config)
    
    def learn(self, request: LearningRequest) -> LearningResult:
        """
        unified学习入口 - 智能路由到最适合的引擎
        
        Args:
            request: 学习请求
        
        Returns:
            学习结果
        """
        start_time = time.time()
        
        logger.info(f"开始学习: {request.capability.value} [ID: {request.request_id}]")
        
        # 获取适合的引擎列表
        engines_to_use = self.capability_engine_map.get(request.capability.value, ["unified"])
        
        # 过滤掉未初始化的引擎;super/narrative 由超级引擎内部直接处理
        available_engines = [
            e for e in engines_to_use
            if e in self.engines or e in {"super", "narrative"}
        ]
        
        if not available_engines:
            result = LearningResult(
                request_id=request.request_id,
                capability=request.capability,
                success=False,
                data={},
                engine_used="none",
                error=f"没有可用的学习引擎支持 {request.capability.value}"
            )
            return self._finalize_learning_result(result, start_time)
        
        # 选择最佳引擎(优先选择第一个可用的)
        primary_engine = available_engines[0]
        effective_timeout = request.timeout if request.timeout is not None else self.request_timeout
        
        try:
            result = execute_with_timeout(self, request, primary_engine, effective_timeout)
        except TimeoutError as e:
            logger.error(f"学习超时: {request.capability.value} - {e}")
            result = LearningResult(
                request_id=request.request_id,
                capability=request.capability,
                success=False,
                data={},
                engine_used=primary_engine,
                error="执行失败"
            )
        except Exception as e:
            logger.error(f"学习失败: {request.capability.value} - {e}")
            result = LearningResult(
                request_id=request.request_id,
                capability=request.capability,
                success=False,
                data={},
                engine_used=primary_engine,
                error="执行失败"
            )
        
        return self._finalize_learning_result(result, start_time)
    
    def _finalize_learning_result(self, result: LearningResult, start_time: float) -> LearningResult:
        """统一补全学习结果,历史与统计."""
        execution_time = time.time() - start_time
        result.execution_time = execution_time
        
        with self.history_lock:
            self.learning_history.append(result)
        
        self._update_stats(result)
        
        if result.success:
            logger.info(f"学习完成: {result.capability.value} [耗时: {execution_time:.2f}s]")
        else:
            logger.warning(
                f"学习结束但未成功: {result.capability.value} [耗时: {execution_time:.2f}s] - {result.error}"
            )
        
        return result
    
    def _update_stats(self, result: LearningResult):
        """更新学习统计"""
        self.stats["total_requests"] += 1
        
        if result.success:
            self.stats["successful_requests"] += 1
        else:
            self.stats["failed_requests"] += 1
        
        self.stats["total_execution_time"] += result.execution_time
        
        engine = result.engine_used
        if engine not in self.stats["engine_usage"]:
            self.stats["engine_usage"][engine] = 0
        self.stats["engine_usage"][engine] += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """获取学习统计"""
        stats = self.stats.copy()
        
        if stats["total_requests"] > 0:
            stats["avg_execution_time"] = stats["total_execution_time"] / stats["total_requests"]
            stats["success_rate"] = stats["successful_requests"] / stats["total_requests"]
        else:
            stats["avg_execution_time"] = 0.0
            stats["success_rate"] = 0.0
        
        return stats
    
    def get_learning_history(self, limit: int = 10) -> List[LearningResult]:
        """获取学习历史"""
        with self.history_lock:
            return self.learning_history[-limit:]
    
    def register_engine(self, name: str, engine: Any) -> None:
        """注册自定义学习引擎."""
        self.engines[name] = engine
    
    def get_engine_by_capability(self, capability: LearningCapability) -> Optional[Any]:
        """按能力返回首选可用引擎实例."""
        for engine_name in self.capability_engine_map.get(capability.value, []):
            if engine_name in self.engines:
                return self.engines[engine_name]
        return None
    
    def route_request_to_engine(self, request: LearningRequest) -> Optional[Any]:
        """兼容旧接口:根据请求路由到具体引擎实例."""
        return self.get_engine_by_capability(request.capability)
    
    def get_stats_by_capability(self, capability: LearningCapability) -> LearningStats:
        """按学习能力聚合历史统计."""
        stats = LearningStats()
        with self.history_lock:
            for item in self.learning_history:
                if item.capability != capability:
                    continue
                stats.update(item.success, item.execution_time)
                stats.update_by_capability(item.capability, item.success, item.execution_time)
        return stats
    
    def get_engine_info(self, engine_name: str) -> Optional[EngineLoadInfo]:
        """获取单个引擎的基础负载信息."""
        if engine_name not in self.engines:
            return None
        queue_size = 0
        if hasattr(self.executor, "_work_queue"):
            try:
                queue_size = self.executor._work_queue.qsize()
            except Exception:
                queue_size = 0
        return EngineLoadInfo(
            name=engine_name,
            active_tasks=0,
            queue_size=queue_size,
            avg_response_time=self.get_stats().get("avg_execution_time", 0.0),
            available=True
        )
    
    def get_all_engine_info(self) -> Dict[str, EngineLoadInfo]:
        """获取全部引擎信息."""
        return {
            name: info
            for name in self.engines
            if (info := self.get_engine_info(name)) is not None
        }
    
    def learn_parallel(self, requests: List[LearningRequest]) -> List[LearningResult]:
        """兼容旧接口:parallel_learn 的别名."""
        return self.parallel_learn(requests)
    
    def parallel_learn(self, requests: List[LearningRequest]) -> List[LearningResult]:
        """
        并行学习 - 多个学习任务并行执行
        
        Args:
            requests: 学习请求列表
        
        Returns:
            学习结果列表
        """
        logger.info(f"开始并行学习: {len(requests)} 个任务")
        
        futures = {}
        for request in requests:
            future = self.executor.submit(self.learn, request)
            futures[future] = request
        
        results = []
        for future in as_completed(futures):
            request = futures[future]
            try:
                result = future.result(timeout=request.timeout)
                results.append(result)
            except Exception as e:
                logger.error(f"并行学习失败 [{request.request_id}]: {e}")
                results.append(LearningResult(
                    request_id=request.request_id,
                    capability=request.capability,
                    success=False,
                    data={},
                    error="执行失败",
                    execution_time=request.timeout
                ))
        
        logger.info(f"并行学习完成: {len(results)} 个结果")
        return results
    
    def optimize_learning_strategy(self) -> Dict[str, Any]:
        """
        优化学习strategy - 基于历史数据
        
        Returns:
            优化建议
        """
        stats = self.get_stats()
        
        # 分析引擎使用情况
        engine_usage = stats["engine_usage"]
        most_used = max(engine_usage.items(), key=lambda x: x[1]) if engine_usage else ("none", 0)
        
        # 分析成功率
        success_rate = stats["success_rate"]
        
        recommendations = []
        
        if success_rate < 0.8:
            recommendations.append("成功率较低,建议检查学习任务配置")
        
        if stats["avg_execution_time"] > 60.0:
            recommendations.append("平均执行时间较长,建议优化学习算法或增加并行度")
        
        if most_used[1] > stats["total_requests"] * 0.7:
            recommendations.append(f"过度依赖 {most_used[0]} 引擎,建议尝试其他学习方式")
        
        return {
            "stats": stats,
            "most_used_engine": most_used[0],
            "recommendations": recommendations,
            "optimized": len(recommendations) == 0
        }
    
    def close(self):
        """关闭超级学习引擎"""
        logger.info("关闭超级学习引擎...")
        
        # 关闭线程池
        self.executor.shutdown(wait=True)
        
        # 清理各引擎资源
        for engine_name, engine in self.engines.items():
            try:
                if hasattr(engine, 'close'):
                    engine.close()
                logger.info(f"  ✓ {engine_name} 引擎已关闭")
            except Exception as e:
                logger.warning(f"  ✗ {engine_name} 引擎关闭失败: {e}")
        
        logger.info("超级学习引擎已关闭")
    
    def __del__(self):
        """析构时自动关闭"""
        self.close()

def main():
    """主函数 - 演示超级学习引擎"""
    logger.info("=" * 60)
    logger.info("超级学习引擎演示")
    logger.info("=" * 60)
    
    # 初始化超级学习引擎
    super_engine = SuperLearningEngine()
    
    logger.info(f"✓ 引擎已初始化")
    logger.info(f"  整合引擎: {len(super_engine.engines)}")
    logger.info(f"  支持能力: {len(LearningCapability)}")
    
    # 示例1: 单次学习
    logger.info("=" * 60)
    logger.info("示例1: 单次学习")
    logger.info("=" * 60)
    
    request1 = LearningRequest(
        capability=LearningCapability.LOCAL_DATA_LEARNING,
        input_data={"source": str(LEARNING_DIR)},
        context={"priority": "high"}
    )
    
    result1 = super_engine.learn(request1)
    logger.info(f"学习结果: {result1.success}")
    logger.info(f"  引擎: {result1.engine_used}")
    logger.info(f"  置信度: {result1.confidence:.2f}")
    logger.info(f"  耗时: {result1.execution_time:.2f}s")

# 向后兼容导入
LearningEngine = SuperLearningEngine
