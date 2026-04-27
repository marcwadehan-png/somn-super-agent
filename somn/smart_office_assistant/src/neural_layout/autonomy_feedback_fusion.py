"""
__all__ = [
    'export_fusion_data',
    'get_autonomy_feedback_fusion_engine',
    'get_fusion_history',
    'get_fusion_statistics',
    'initialize',
    'register_decision_callback',
    'register_feedback_callback',
]

自主层 ↔ 反馈层深度整合模块

实现自主智能体与反馈闭环的深度融合
"""

from typing import Dict, List, Any, Optional, Callable, Set
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import json
from pathlib import Path

class FusionEventType(Enum):
    """融合事件类型"""
    AUTONOMY_DECISION = "autonomy_decision"  # 自主决策
    FEEDBACK_RECEIVED = "feedback_received"  # 反馈接收
    INSIGHT_GENERATED = "insight_generated"  # 洞察生成
    ACTION_VALIDATED = "action_validated"    # 行动验证

@dataclass
class AutonomyFeedbackFusion:
    """自主-反馈融合记录"""
    fusion_id: str
    autonomy_action: Dict[str, Any]
    feedback_data: Dict[str, Any]
    insight: str
    confidence: float
    validated: bool = False
    created_at: datetime = field(default_factory=datetime.now)

class AutonomyFeedbackFusionEngine:
    """
    自主-反馈融合引擎
    
    深度整合自主层与反馈层：
    1. 自主决策自动触发反馈采集
    2. 反馈结果实时影响自主策略
    3. 生成可学习的融合洞察
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = Path(storage_path) if storage_path else Path("data/autonomy_feedback_fusion")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self._fusion_records: List[AutonomyFeedbackFusion] = []
        self._decision_callbacks: List[Callable] = []
        self._feedback_callbacks: List[Callable] = []
        self._autonomy_agent = None
        self._feedback_integrator = None
        
        self._initialized = False
    
    def initialize(self) -> bool:
        """初始化融合引擎"""
        if self._initialized:
            return True
        
        try:
            # 延迟导入避免循环依赖
            from src.autonomous_core.autonomous_agent import AutonomousAgent
            from src.core.feedback_loop_integration import FeedbackLoopIntegrator
            
            self._autonomy_agent = AutonomousAgent()
            self._feedback_integrator = FeedbackLoopIntegrator(str(self.storage_path.parent))
            
            # 注册回调
            self._register_fusion_callbacks()
            
            self._initialized = True
            return True
        except ImportError as e:
            print(f"融合引擎初始化失败: {e}")
            return False
    
    def _register_fusion_callbacks(self):
        """注册融合回调"""
        # 自主决策回调 → 触发反馈采集
        if self._autonomy_agent:
            self._autonomy_agent.scheduler.register_callback(
                "post_decision_feedback",
                self._on_autonomy_decision
            )
    
    async def _on_autonomy_decision(self, decision_data: Dict):
        """自主决策回调 - 触发反馈采集"""
        # 1. 记录决策
        decision_id = f"dec_{datetime.now().strftime('%Y%m%d%H%M%S')}_{id(decision_data) % 10000}"
        
        # 2. 自动触发反馈采集
        feedback_context = {
            "decision_id": decision_id,
            "decision_data": decision_data,
            "collection_timing": "post_decision",
            "expected_signals": ["execution_result", "adoption", "outcome"]
        }
        
        if self._feedback_integrator:
            self._feedback_integrator.setup_collection_point(
                f"autonomy_decision_{decision_id}",
                feedback_context
            )
        
        # 3. 等待反馈并融合
        asyncio.create_task(
            self._wait_and_fuse_feedback(decision_id, decision_data)
        )
    
    async def _wait_and_fuse_feedback(self, decision_id: str, decision_data: Dict):
        """等待反馈并进行融合"""
        # 模拟等待反馈（实际实现中应该监听反馈事件）
        await asyncio.sleep(5)  # 等待5秒收集反馈
        
        # 获取反馈数据
        feedback_data = await self._collect_feedback_for_decision(decision_id)
        
        # 融合决策与反馈
        fusion = self._fuse_decision_feedback(decision_data, feedback_data)
        
        # 存储融合记录
        self._fusion_records.append(fusion)
        
        # 通知回调
        for callback in self._feedback_callbacks:
            try:
                callback(fusion)
            except Exception as e:
                logger.debug(f"[AutonomyFeedback] 回调执行失败: {e}")
    
    async def _collect_feedback_for_decision(self, decision_id: str) -> Dict:
        """收集决策相关的反馈"""
        if not self._feedback_integrator:
            return {}
        
        # 从反馈集成器获取数据
        try:
            feedback = self._feedback_integrator.get_feedback_for_context(
                f"autonomy_decision_{decision_id}"
            )
            return feedback or {}
        except Exception as e:
            logger.debug(f"[AutonomyFeedback] 反馈集成器数据获取失败: {e}")
    
    def _fuse_decision_feedback(self, decision: Dict, feedback: Dict) -> AutonomyFeedbackFusion:
        """融合决策与反馈数据"""
        # 生成洞察
        insight = self._generate_fusion_insight(decision, feedback)
        
        # 计算置信度
        confidence = self._calculate_fusion_confidence(decision, feedback)
        
        fusion = AutonomyFeedbackFusion(
            fusion_id=f"fusion_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self._fusion_records)}",
            autonomy_action=decision,
            feedback_data=feedback,
            insight=insight,
            confidence=confidence,
            validated=feedback.get("validated", False)
        )
        
        return fusion
    
    def _generate_fusion_insight(self, decision: Dict, feedback: Dict) -> str:
        """生成融合洞察"""
        insights = []
        
        # 分析决策效果
        outcome = feedback.get("outcome", "unknown")
        if outcome == "success":
            insights.append("自主决策取得预期效果")
        elif outcome == "partial":
            insights.append("自主决策部分有效，需要调整")
        elif outcome == "failure":
            insights.append("自主决策未达预期，建议重新评估策略")
        
        # 分析反馈信号
        signals = feedback.get("signals", [])
        if "high_adoption" in signals:
            insights.append("用户采纳度高，策略方向正确")
        if "low_engagement" in signals:
            insights.append("参与度低，需要优化交互方式")
        
        return "; ".join(insights) if insights else "融合洞察待生成"
    
    def _calculate_fusion_confidence(self, decision: Dict, feedback: Dict) -> float:
        """计算融合置信度"""
        base_confidence = 0.5
        
        # 根据反馈质量调整
        if feedback.get("outcome") == "success":
            base_confidence += 0.3
        elif feedback.get("outcome") == "partial":
            base_confidence += 0.1
        
        # 根据信号数量调整
        signal_count = len(feedback.get("signals", []))
        base_confidence += min(signal_count * 0.05, 0.15)
        
        return min(base_confidence, 1.0)
    
    def register_decision_callback(self, callback: Callable):
        """注册决策回调"""
        self._decision_callbacks.append(callback)
    
    def register_feedback_callback(self, callback: Callable):
        """注册反馈回调"""
        self._feedback_callbacks.append(callback)
    
    def get_fusion_history(self, limit: int = 10) -> List[Dict]:
        """获取融合历史"""
        return [
            {
                "fusion_id": f.fusion_id,
                "insight": f.insight,
                "confidence": f.confidence,
                "validated": f.validated,
                "created_at": f.created_at.isoformat()
            }
            for f in sorted(self._fusion_records, key=lambda x: x.created_at, reverse=True)[:limit]
        ]
    
    def get_fusion_statistics(self) -> Dict:
        """获取融合统计"""
        if not self._fusion_records:
            return {"total": 0, "validated_rate": 0.0, "avg_confidence": 0.0}
        
        total = len(self._fusion_records)
        validated = sum(1 for f in self._fusion_records if f.validated)
        avg_confidence = sum(f.confidence for f in self._fusion_records) / total
        
        return {
            "total": total,
            "validated_rate": validated / total,
            "avg_confidence": avg_confidence,
            "high_confidence_count": sum(1 for f in self._fusion_records if f.confidence > 0.8)
        }
    
    def export_fusion_data(self) -> Dict:
        """导出融合数据用于学习"""
        return {
            "records": [
                {
                    "fusion_id": f.fusion_id,
                    "autonomy_action": f.autonomy_action,
                    "feedback_data": f.feedback_data,
                    "insight": f.insight,
                    "confidence": f.confidence,
                    "validated": f.validated,
                    "created_at": f.created_at.isoformat()
                }
                for f in self._fusion_records
            ],
            "statistics": self.get_fusion_statistics(),
            "export_time": datetime.now().isoformat()
        }

# 全局融合引擎实例
_fusion_engine: Optional[AutonomyFeedbackFusionEngine] = None

def get_autonomy_feedback_fusion_engine() -> AutonomyFeedbackFusionEngine:
    """获取自主-反馈融合引擎"""
    global _fusion_engine
    if _fusion_engine is None:
        _fusion_engine = AutonomyFeedbackFusionEngine()
    return _fusion_engine
