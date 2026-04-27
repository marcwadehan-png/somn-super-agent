"""
数字大脑集成API [v1.0.0]
提供SomnCore与数字大脑的深度集成接口

集成方式:
- SomnCore属性: digital_brain, digital_brain_config, is_digital_brain_ready
- SomnCore方法: think_with_brain(), evolve_brain(), purify_brain(), get_brain_health()

Author: Somn Digital Brain Team
"""

import asyncio
import logging
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# 数字大脑配置
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class DigitalBrainSomnConfig:
    """数字大脑与Somn集成配置"""
    # 自动集成开关
    auto_integrate: bool = True              # 自动集成到SomnCore
    enable_through_somn: bool = True         # 启用穿越Somn的思维
    enable_somn_through_brain: bool = True   # 启用Somn穿越数字大脑
    
    # 思维模式
    default_think_mode: str = "integrated"   # integrated/solo/bypass
    somn_weight: float = 0.6                 # Somn思维权重
    brain_weight: float = 0.4                # 数字大脑思维权重
    
    # 性能配置
    async_mode: bool = True                  # 异步模式
    parallel_think: bool = True             # 并行思考
    timeout_seconds: float = 30.0           # 超时时间
    
    # 进化配置
    auto_evolve_interval: int = 3600        # 自动进化间隔(秒)
    evolve_on_idle: bool = True             # 空闲时进化
    min_thoughts_before_evolve: int = 10   # 进化前最小思考次数
    
    # 记忆同步配置
    sync_to_imperial_library: bool = True   # 同步到藏书阁
    sync_interval: int = 300                # 同步间隔(秒)
    memory_encryption: bool = False         # 记忆加密
    
    # 调试配置
    verbose_logging: bool = False            # 详细日志
    log_thought_process: bool = False       # 记录思考过程


# ═══════════════════════════════════════════════════════════════════════════════
# 穿越结果数据结构
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ThroughResult:
    """穿越结果"""
    success: bool
    somn_result: Optional[Any] = None
    brain_result: Optional[Dict[str, Any]] = None
    fusion_result: Optional[str] = None
    thinking_trace: list = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# 数字大脑集成器
# ═══════════════════════════════════════════════════════════════════════════════

class DigitalBrainSomnIntegrator:
    """
    数字大脑与SomnCore集成器 [v1.0.0]
    
    提供两种集成模式:
    1. 数字大脑穿越Somn: 先Somn处理，数字大脑增强
    2. Somn穿越数字大脑: 先数字大脑处理，Somn增强
    
    属性(通过SomnCore访问):
    - digital_brain: 数字大脑核心实例
    - digital_brain_config: 集成配置
    - is_digital_brain_ready: 数字大脑就绪状态
    
    方法:
    - think_with_brain(query, context): 数字大脑增强的思考
    - evolve_brain(target): 触发数字大脑进化
    - purify_brain(mode): 触发数字大脑净化
    - get_brain_health(): 获取数字大脑健康状态
    - get_through_somn(query, context): 穿越Somn的思考
    - get_through_brain(query, context): 穿越数字大脑的思考
    """
    
    def __init__(
        self,
        somn_core: Any,
        config: Optional[DigitalBrainSomnConfig] = None
    ):
        """
        初始化数字大脑集成器
        
        Args:
            somn_core: SomnCore实例
            config: 集成配置
        """
        self._somn = somn_core
        self._config = config or DigitalBrainSomnConfig()
        self._digital_brain = None
        self._is_ready = False
        self._init_lock = asyncio.Lock()
        
        # 统计
        self._stats = {
            'total_thinks': 0,
            'successful_thinks': 0,
            'failed_thinks': 0,
            'total_evolutions': 0,
            'total_purifications': 0,
        }
        
        logger.info(f"[数字大脑集成器] 初始化完成，配置: {self._config}")
    
    @property
    def digital_brain(self):
        """获取数字大脑核心"""
        return self._digital_brain
    
    @property
    def digital_brain_config(self) -> DigitalBrainSomnConfig:
        """获取集成配置"""
        return self._config
    
    @property
    def is_digital_brain_ready(self) -> bool:
        """获取就绪状态"""
        return self._is_ready and self._digital_brain is not None
    
    @property
    def stats(self) -> Dict[str, int]:
        """获取统计信息"""
        return self._stats.copy()
    
    async def initialize(self) -> bool:
        """
        异步初始化数字大脑
        
        Returns:
            是否初始化成功
        """
        async with self._init_lock:
            if self._is_ready:
                return True
            
            try:
                logger.info("[数字大脑集成器] 开始初始化数字大脑...")
                
                # 导入数字大脑核心
                from ..digital_brain.digital_brain_core import (
                    DigitalBrainCore,
                    BrainConfig,
                    LoadMode
                )
                
                # 导入集成桥接
                from ..digital_brain.digital_brain_integration import (
                    create_digital_brain_integration
                )
                
                # 构建BrainConfig
                brain_config = BrainConfig(
                    enable_neural_memory=self._config.auto_integrate,
                    enable_wisdom_dispatch=self._config.auto_integrate,
                    enable_autonomous_evolution=self._config.auto_integrate,
                    enable_local_llm=self._config.enable_through_somn,
                    enable_imperial_library=self._config.sync_to_imperial_library,
                    async_mode=self._config.async_mode,
                    auto_evolve=self._config.evolve_on_idle,
                    evolve_interval=self._config.auto_evolve_interval,
                    sync_interval=self._config.sync_interval,
                )
                
                # 创建数字大脑核心
                self._digital_brain = DigitalBrainCore(brain_config)
                
                # 异步初始化
                await self._digital_brain.initialize()
                
                # 创建集成桥接
                self._integration = create_digital_brain_integration(
                    somn_core=self._somn,
                    digital_brain=self._digital_brain,
                    config=self._config
                )
                
                self._is_ready = True
                logger.info("[数字大脑集成器] 初始化成功!")
                return True
                
            except Exception as e:
                logger.error(f"[数字大脑集成器] 初始化失败: {e}")
                self._is_ready = False
                return False
    
    async def think_with_brain(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        mode: str = "integrated"
    ) -> ThroughResult:
        """
        数字大脑增强的思考
        
        Args:
            query: 查询字符串
            context: 上下文
            mode: 思考模式 (integrated/solo/bypass)
        
        Returns:
            ThroughResult: 穿越结果
        """
        start_time = time.time()
        self._stats['total_thinks'] += 1
        
        try:
            if not self.is_digital_brain_ready:
                return ThroughResult(
                    success=False,
                    error="数字大脑未就绪"
                )
            
            # 根据模式选择处理方式
            if mode == "solo":
                # 仅数字大脑
                brain_result = await self._digital_brain.think(query, context)
                return ThroughResult(
                    success=True,
                    brain_result=brain_result,
                    metrics={'mode': 'solo', 'duration': time.time() - start_time}
                )
            
            elif mode == "bypass":
                # 绕过数字大脑，直接Somn处理
                somn_result = await self._somn_run(query, context)
                return ThroughResult(
                    success=True,
                    somn_result=somn_result,
                    metrics={'mode': 'bypass', 'duration': time.time() - start_time}
                )
            
            else:
                # integrated: Somn + 数字大脑融合
                return await self._think_integrated(query, context, start_time)
                
        except Exception as e:
            self._stats['failed_thinks'] += 1
            logger.error(f"[数字大脑集成器] think_with_brain失败: {e}")
            return ThroughResult(
                success=False,
                error="数字大脑链路异常"
            )
    
    async def _think_integrated(
        self,
        query: str,
        context: Optional[Dict[str, Any]],
        start_time: float
    ) -> ThroughResult:
        """融合思考: Somn + 数字大脑"""
        
        if self._config.parallel_think and self._config.async_mode:
            # 并行处理
            somn_task = self._somn_run_async(query, context)
            brain_task = self._digital_brain.think(query, context)
            
            somn_result, brain_result = await asyncio.gather(
                somn_task, brain_task, return_exceptions=True
            )
            
            if isinstance(somn_result, Exception):
                somn_result = None
            if isinstance(brain_result, Exception):
                brain_result = None
        else:
            # 串行处理
            somn_result = await self._somn_run_async(query, context)
            brain_result = await self._digital_brain.think(query, context)
        
        # 融合结果
        fusion = self._fuse_results(somn_result, brain_result)
        
        duration = time.time() - start_time
        self._stats['successful_thinks'] += 1
        
        return ThroughResult(
            success=True,
            somn_result=somn_result,
            brain_result=brain_result,
            fusion_result=fusion,
            thinking_trace=[
                f"Somn处理完成: {bool(somn_result)}",
                f"数字大脑处理完成: {bool(brain_result)}",
                f"结果融合完成"
            ],
            metrics={
                'mode': 'integrated',
                'duration': duration,
                'somn_weight': self._config.somn_weight,
                'brain_weight': self._config.brain_weight,
            }
        )
    
    async def evolve_brain(
        self,
        target: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        触发数字大脑进化
        
        Args:
            target: 进化目标 (None=自动判断)
        
        Returns:
            进化结果
        """
        self._stats['total_evolutions'] += 1
        
        if not self.is_digital_brain_ready:
            return {'success': False, 'error': '数字大脑未就绪'}
        
        try:
            result = await self._digital_brain.evolve(target)
            return {
                'success': True,
                'evolution': result,
                'stats': self._stats
            }
        except Exception as e:
            logger.error(f"[数字大脑集成器] evolve_brain失败: {e}")
            return {'success': False, 'error': '数字大脑进化失败'}
    
    async def purify_brain(
        self,
        mode: str = "auto"
    ) -> Dict[str, Any]:
        """
        触发数字大脑净化
        
        Args:
            mode: 净化模式 (auto/light/deep)
        
        Returns:
            净化结果
        """
        self._stats['total_purifications'] += 1
        
        if not self.is_digital_brain_ready:
            return {'success': False, 'error': '数字大脑未就绪'}
        
        try:
            result = await self._digital_brain.purify(mode)
            return {
                'success': True,
                'purification': result,
                'stats': self._stats
            }
        except Exception as e:
            logger.error(f"[数字大脑集成器] purify_brain失败: {e}")
            return {'success': False, 'error': '数字大脑净化失败'}
    
    def get_brain_health(self) -> Dict[str, Any]:
        """
        获取数字大脑健康状态
        
        Returns:
            健康状态
        """
        if not self.is_digital_brain_ready:
            return {
                'ready': False,
                'error': '数字大脑未就绪'
            }
        
        try:
            health = self._digital_brain.get_health()
            return {
                'ready': True,
                'health': health,
                'stats': self._stats
            }
        except Exception as e:
            logger.error(f"[数字大脑集成器] get_brain_health失败: {e}")
            return {'ready': False, 'error': '获取数字大脑健康状态失败'}
    
    async def get_through_somn(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> ThroughResult:
        """
        穿越Somn思考: Somn先处理，数字大脑后增强
        
        Args:
            query: 查询
            context: 上下文
        
        Returns:
            穿越结果
        """
        start_time = time.time()
        
        try:
            # Step 1: Somn处理
            somn_result = await self._somn_run_async(query, context)
            
            # Step 2: 数字大脑增强
            enhanced_context = {
                **(context or {}),
                'somn_result': somn_result,
                'enhancement_mode': 'through_somn'
            }
            brain_result = await self._digital_brain.think(
                f"增强以下Somn结果: {query}",
                enhanced_context
            )
            
            return ThroughResult(
                success=True,
                somn_result=somn_result,
                brain_result=brain_result,
                fusion_result=brain_result.get('enhanced_thought') if brain_result else None,
                thinking_trace=[
                    "Step 1: SomnCore处理完成",
                    "Step 2: 数字大脑增强完成",
                    "Step 3: 结果融合完成"
                ],
                metrics={
                    'mode': 'through_somn',
                    'duration': time.time() - start_time
                }
            )
        except Exception as e:
            logger.error(f"[数字大脑集成器] get_through_somn失败: {e}")
            return ThroughResult(success=False, error="Somn链路穿越失败")
    
    async def get_through_brain(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> ThroughResult:
        """
        穿越数字大脑思考: 数字大脑先处理，Somn后增强
        
        Args:
            query: 查询
            context: 上下文
        
        Returns:
            穿越结果
        """
        start_time = time.time()
        
        try:
            # Step 1: 数字大脑处理
            brain_result = await self._digital_brain.think(query, context)
            
            # Step 2: Somn增强
            enhanced_context = {
                **(context or {}),
                'brain_result': brain_result,
                'enhancement_mode': 'through_brain'
            }
            somn_result = await self._somn_run_async(
                f"增强以下数字大脑结果: {query}",
                enhanced_context
            )
            
            return ThroughResult(
                success=True,
                somn_result=somn_result,
                brain_result=brain_result,
                fusion_result=somn_result,
                thinking_trace=[
                    "Step 1: 数字大脑处理完成",
                    "Step 2: SomnCore增强完成",
                    "Step 3: 结果融合完成"
                ],
                metrics={
                    'mode': 'through_brain',
                    'duration': time.time() - start_time
                }
            )
        except Exception as e:
            logger.error(f"[数字大脑集成器] get_through_brain失败: {e}")
            return ThroughResult(success=False, error="数字大脑链路穿越失败")
    
    def _fuse_results(self, somn_result: Any, brain_result: Dict) -> str:
        """融合Somn和数字大脑的结果"""
        if not brain_result:
            return str(somn_result) if somn_result else ""
        
        thought = brain_result.get('thought', '')
        confidence = brain_result.get('confidence', 0.5)
        
        if somn_result:
            # 根据权重融合
            fused = f"[Somn权重{self._config.somn_weight:.0%}] {str(somn_result)[:200]}..."
            fused += f"\n[数字大脑权重{self._config.brain_weight:.0%}] {thought[:200]}..."
            fused += f"\n综合置信度: {confidence * self._config.brain_weight + 0.5 * self._config.somn_weight:.2f}"
            return fused
        
        return thought
    
    async def _somn_run(self, query: str, context: Optional[Dict]) -> Any:
        """同步运行Somn"""
        return await self._somn_run_async(query, context)
    
    async def _somn_run_async(self, query: str, context: Optional[Dict]) -> Any:
        """异步运行Somn"""
        try:
            # 尝试调用SomnCore的方法
            if hasattr(self._somn, 'run'):
                return await self._somn.run(query, context or {})
            elif hasattr(self._somn, 'analyze'):
                return await self._somn.analyze(query, context or {})
            elif hasattr(self._somn, '_module_run_analyze_requirement'):
                return await self._somn._module_run_analyze_requirement(query, context or {})
            else:
                logger.warning("[数字大脑集成器] SomnCore无可用的处理方法")
                return None
        except Exception as e:
            logger.error(f"[数字大脑集成器] Somn运行失败: {e}")
            return None
    
    async def shutdown(self):
        """关闭数字大脑"""
        if self._digital_brain:
            await self._digital_brain.shutdown()
        self._is_ready = False
        logger.info("[数字大脑集成器] 关闭完成")


# ═══════════════════════════════════════════════════════════════════════════════
# 工厂函数
# ═══════════════════════════════════════════════════════════════════════════════

def create_digital_brain_somn_integrator(
    somn_core: Any,
    config: Optional[DigitalBrainSomnConfig] = None
) -> DigitalBrainSomnIntegrator:
    """
    创建数字大脑Somn集成器
    
    Args:
        somn_core: SomnCore实例
        config: 集成配置
    
    Returns:
        DigitalBrainSomnIntegrator实例
    """
    return DigitalBrainSomnIntegrator(somn_core, config)
