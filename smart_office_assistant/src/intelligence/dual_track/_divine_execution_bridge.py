"""
DivineReason 神行轨桥接器 - DivineExecutionBridge V1.0

核心功能:
1. 将 DivineReason 的推荐节点映射到神行轨的部门执行器
2. 提供推荐节点的可执行化
3. 追踪推荐执行结果

使用方式:
    bridge = DivineExecutionBridge()
    
    # DivineReason 推理后，获取推荐
    recommendations = response.fused_answer.get('recommendations', [])
    
    # 将推荐转化为可执行节点
    executable_nodes = bridge.prepare_executable_recommendations(recommendations, query)
    
    # 执行推荐
    results = bridge.execute_recommendations(executable_nodes)
"""

import logging
import uuid
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class RecommendationPriority(Enum):
    """推荐优先级"""
    HIGH = "high"      # 立即执行
    MEDIUM = "medium"  # 常规执行
    LOW = "low"        # 可选执行


@dataclass
class ExecutableRecommendation:
    """
    可执行的推荐节点
    
    代表 DivineReason 推理图中的一个推荐节点，
    可以被映射到神行轨的某个部门执行器。
    """
    node_id: str                    # 节点唯一标识
    content: str                     # 推荐内容
    target_department: str           # 目标部门
    priority: RecommendationPriority # 优先级
    context: Dict[str, Any]          # 执行上下文
    estimated_impact: float = 0.5   # 预估影响 (0-1)
    prerequisites: List[str] = field(default_factory=list)  # 前置依赖
    
    # 执行结果（执行后填充）
    executed: bool = False
    execution_result: Optional[Dict[str, Any]] = None
    execution_time: Optional[str] = None
    success: bool = False


@dataclass  
class ExecutionReport:
    """执行报告"""
    total_recommendations: int
    executed_count: int
    success_count: int
    failed_count: int
    results: List[Dict[str, Any]]
    summary: str


class DepartmentMapper:
    """
    推荐内容到部门的智能映射器
    
    根据推荐内容的语义，自动识别应该由哪个部门执行。
    """
    
    # 部门关键词映射
    DEPARTMENT_PATTERNS = {
        "兵部": {
            "keywords": ["竞争", "对手", "博弈", "战略", "军事", "危机", "谈判", "冲突", 
                        "威胁", "市场份额", "对手策略", "攻防", "突围", "抢占"],
            "weight": 0.8
        },
        "户部": {
            "keywords": ["营销", "市场", "销售", "客户", "收入", "利润", "成本", "预算",
                        "增长", "流量", "转化", "定价", "推广", "品牌"],
            "weight": 0.8
        },
        "工部": {
            "keywords": ["技术", "产品", "开发", "系统", "架构", "代码", "性能", "优化",
                        "创新", "研发", "功能", "接口", "bug", "质量"],
            "weight": 0.8
        },
        "吏部": {
            "keywords": ["团队", "人才", "招聘", "管理", "领导", "组织", "绩效", "培训",
                        "人员", "HR", "人员配置", "激励", "考核"],
            "weight": 0.8
        },
        "礼部": {
            "keywords": ["文化", "品牌", "形象", "公关", "沟通", "培训", "价值观", 
                        "客户关系", "服务", "满意度", "口碑"],
            "weight": 0.8
        },
        "刑部": {
            "keywords": ["风险", "合规", "法律", "审计", "安全", "漏洞", "隐私", 
                        "政策", "监管", "条例", "规则"],
            "weight": 0.8
        },
        "厂卫": {
            "keywords": ["监控", "日志", "告警", "性能", "可用性", "稳定性", "运维",
                        "SRE", "异常", "故障", "巡检"],
            "weight": 0.8
        },
        "三法司": {
            "keywords": ["评估", "验证", "效果", "ROI", "反馈", "复盘", "总结",
                        "改进", "迭代", "优化效果"],
            "weight": 0.8
        },
        "翰林院": {
            "keywords": ["分析", "论证", "审核", "决策", "逻辑", "方案", "策略",
                        "计划", "研究", "评估"],
            "weight": 0.8
        },
        "五军都督府": {
            "keywords": ["网络", "连接", "通信", "协作", "协调", "集成", "接口",
                        "对接", "联调", "整合"],
            "weight": 0.8
        },
    }
    
    @classmethod
    def map_to_department(cls, recommendation: str, context: str = "") -> Tuple[str, float]:
        """
        将推荐内容映射到部门
        
        Args:
            recommendation: 推荐内容
            context: 上下文信息
            
        Returns:
            (部门名称, 置信度)
        """
        combined_text = f"{recommendation} {context}".lower()
        
        scores = {}
        for dept, pattern in cls.DEPARTMENT_PATTERNS.items():
            score = 0
            for kw in pattern["keywords"]:
                if kw.lower() in combined_text:
                    score += pattern["weight"]
            if score > 0:
                scores[dept] = score
        
        if not scores:
            return "默认", 0.5
        
        best_dept = max(scores, key=scores.get)
        max_score = scores[best_dept]
        confidence = min(1.0, max_score / 2.0)  # 归一化
        
        return best_dept, confidence
    
    @classmethod
    def detect_priority(cls, recommendation: str) -> RecommendationPriority:
        """
        检测推荐优先级
        
        基于关键词判断紧急程度
        """
        urgent_keywords = ["紧急", "立即", "马上", "必须", "危机", "问题"]
        medium_keywords = ["应该", "建议", "考虑", "推荐"]
        
        rec_lower = recommendation.lower()
        
        if any(kw in rec_lower for kw in urgent_keywords):
            return RecommendationPriority.HIGH
        elif any(kw in rec_lower for kw in medium_keywords):
            return RecommendationPriority.MEDIUM
        return RecommendationPriority.LOW


class DivineExecutionBridge:
    """
    DivineReason 神行轨桥接器 V1.0
    
    核心职责:
    1. 接收 DivineReason 的推理结果（包含 recommendations）
    2. 将推荐转化为可执行的推荐节点
    3. 映射到神行轨的对应部门
    4. 调用神行轨执行并收集结果
    5. 生成执行报告
    
    设计原则:
    - DivineReason 是"思考者"，神行轨是"执行者"
    - 推理完成后，推荐节点可以"行动起来"
    - 保持两轨职责清晰：想清楚 vs 干漂亮
    """
    
    def __init__(self):
        self._track_b = None
        self._mapper = DepartmentMapper()
        self._executed_nodes: List[ExecutableRecommendation] = []
        self._execution_history: List[ExecutionReport] = []
        
        logger.info("[DR-Bridge] DivineExecutionBridge V1.0 初始化完成")
    
    def _get_track_b(self):
        """懒加载神行轨"""
        if self._track_b is None:
            try:
                from .track_b import DivineExecutionTrack
                self._track_b = DivineExecutionTrack()
                logger.info("[DR-Bridge] 神行轨连接成功")
            except ImportError as e:
                logger.warning(f"[DR-Bridge] 神行轨导入失败: {e}")
                return None
        return self._track_b
    
    def prepare_executable_recommendations(
        self,
        recommendations: List[str],
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> List[ExecutableRecommendation]:
        """
        将 DivineReason 的推荐列表转化为可执行节点
        
        Args:
            recommendations: DivineReason 生成的推荐列表
            query: 原始问题（用于上下文理解）
            context: 额外上下文
            
        Returns:
            可执行的推荐节点列表
        """
        nodes = []
        context_text = context.get("query", "") if context else query
        
        for i, rec in enumerate(recommendations):
            if not rec or len(rec) < 5:
                continue
            
            # 映射到部门
            dept, confidence = self._mapper.map_to_department(rec, query)
            
            # 检测优先级
            priority = self._mapper.detect_priority(rec)
            
            # 创建节点
            node = ExecutableRecommendation(
                node_id=f"dr_node_{uuid.uuid4().hex[:8]}",
                content=rec,
                target_department=dept,
                priority=priority,
                context={
                    "original_query": query,
                    "department_confidence": confidence,
                    "index": i,
                    **(context or {})
                },
                estimated_impact=confidence
            )
            nodes.append(node)
            
            logger.debug(f"[DR-Bridge] 推荐→{dept}: {rec[:30]}...")
        
        return nodes
    
    def execute_recommendations(
        self,
        nodes: List[ExecutableRecommendation],
        max_concurrent: int = 5
    ) -> ExecutionReport:
        """
        执行推荐节点
        
        Args:
            nodes: 可执行推荐节点列表
            max_concurrent: 最大并发执行数（预留）
            
        Returns:
            执行报告
        """
        track_b = self._get_track_b()
        if not track_b:
            return self._create_error_report(nodes, "神行轨不可用")
        
        results = []
        success_count = 0
        failed_count = 0
        
        for node in nodes:
            try:
                # 调用神行轨执行
                result = track_b.execute_sync(
                    department=node.target_department,
                    task_description=node.content,
                    context={
                        **node.context,
                        "dr_node_id": node.node_id,
                        "execution_mode": "divine_reason_recommendation"
                    },
                    caller="divine_reason"
                )
                
                # 更新节点状态
                from datetime import datetime
                node.executed = True
                node.execution_result = result
                node.execution_time = datetime.now().isoformat()
                node.success = result.get("success", False)
                
                if node.success:
                    success_count += 1
                else:
                    failed_count += 1
                
                results.append({
                    "node_id": node.node_id,
                    "department": node.target_department,
                    "content": node.content[:50],
                    "success": node.success,
                    "result": result
                })
                
                logger.info(f"[DR-Bridge] 执行 {node.node_id} → {node.target_department}: {'成功' if node.success else '失败'}")
                
            except Exception as e:
                logger.error(f"[DR-Bridge] 执行节点失败 {node.node_id}: {e}")
                node.executed = True
                node.execution_result = {"error": str(e)}
                node.success = False
                failed_count += 1
                
                results.append({
                    "node_id": node.node_id,
                    "department": node.target_department,
                    "content": node.content[:50],
                    "success": False,
                    "error": str(e)
                })
        
        # 保存执行历史
        self._executed_nodes.extend(nodes)
        
        # 生成报告
        report = ExecutionReport(
            total_recommendations=len(nodes),
            executed_count=len([n for n in nodes if n.executed]),
            success_count=success_count,
            failed_count=failed_count,
            results=results,
            summary=self._generate_summary(nodes, success_count, failed_count)
        )
        
        self._execution_history.append(report)
        
        return report
    
    def reason_and_execute(
        self,
        query: str,
        problem_type: str = "",
        max_engines: int = 8,
        execute_recommendations: bool = True,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        完整推理+执行流程
        
        这是 DivineReason + 神行轨的联合入口：
        1. DivineReason 推理分析
        2. 生成推荐
        3. 将推荐转化为可执行节点
        4. 调用神行轨执行
        5. 返回完整结果
        
        Args:
            query: 问题
            problem_type: 问题类型（可选，自动检测）
            max_engines: 最大引擎数
            execute_recommendations: 是否执行推荐
            context: 额外上下文
            
        Returns:
            完整结果（推理结果 + 执行报告）
        """
        from ..engines.sub_engines._divine_reason_engine import (
            DivineReasonEngine,
            ReasoningRequest
        )
        
        logger.info(f"[DR-Bridge] 开始推理+执行: {query[:50]}...")
        
        # 1. DivineReason 推理
        engine = DivineReasonEngine()
        request = ReasoningRequest(
            query=query,
            problem_type=problem_type,
            context=context or {},
            max_engines=max_engines
        )
        reasoning_response = engine.reason(request)
        
        result = {
            "reasoning": {
                "query": query,
                "problem_type": reasoning_response.analysis.get("problem_type", ""),
                "fused_answer": reasoning_response.fused_answer,
                "confidence": reasoning_response.confidence,
                "engines_used": reasoning_response.engines_used,
                "reasoning_summary": reasoning_response.reasoning_summary,
            },
            "recommendations": [],
            "execution_report": None
        }
        
        # 2. 如果需要执行推荐
        if execute_recommendations:
            recommendations = reasoning_response.fused_answer.get("recommendations", [])
            
            if recommendations:
                # 准备可执行节点
                nodes = self.prepare_executable_recommendations(
                    recommendations, 
                    query, 
                    context
                )
                
                # 执行
                report = self.execute_recommendations(nodes)
                
                result["recommendations"] = [
                    {
                        "node_id": n.node_id,
                        "content": n.content,
                        "department": n.target_department,
                        "priority": n.priority.value,
                        "executed": n.executed,
                        "success": n.success
                    }
                    for n in nodes
                ]
                result["execution_report"] = {
                    "total": report.total_recommendations,
                    "executed": report.executed_count,
                    "success": report.success_count,
                    "failed": report.failed_count,
                    "summary": report.summary
                }
        
        return result
    
    def _create_error_report(
        self, 
        nodes: List[ExecutableRecommendation], 
        error: str
    ) -> ExecutionReport:
        """创建错误报告"""
        return ExecutionReport(
            total_recommendations=len(nodes),
            executed_count=0,
            success_count=0,
            failed_count=len(nodes),
            results=[{"error": error} for _ in nodes],
            summary=f"执行失败: {error}"
        )
    
    def _generate_summary(
        self, 
        nodes: List[ExecutableRecommendation],
        success: int,
        failed: int
    ) -> str:
        """生成执行摘要"""
        if not nodes:
            return "无推荐节点"
        
        depts = {}
        for n in nodes:
            d = n.target_department
            if d not in depts:
                depts[d] = {"success": 0, "failed": 0}
            if n.success:
                depts[d]["success"] += 1
            else:
                depts[d]["failed"] += 1
        
        parts = [f"执行{len(nodes)}个推荐"]
        for dept, stats in depts.items():
            parts.append(f"{dept}(成{stats['success']}/败{stats['failed']})")
        
        return " | ".join(parts)
    
    def get_execution_history(self) -> List[ExecutionReport]:
        """获取执行历史"""
        return self._execution_history
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_nodes_executed": len(self._executed_nodes),
            "total_sessions": len(self._execution_history),
            "success_rate": (
                sum(1 for n in self._executed_nodes if n.success) / len(self._executed_nodes)
                if self._executed_nodes else 0
            )
        }


# 全局单例
_divine_execution_bridge: Optional[DivineExecutionBridge] = None


def get_divine_execution_bridge() -> DivineExecutionBridge:
    """获取全局桥接器单例"""
    global _divine_execution_bridge
    if _divine_execution_bridge is None:
        _divine_execution_bridge = DivineExecutionBridge()
    return _divine_execution_bridge


def reason_and_execute(
    query: str,
    problem_type: str = "",
    max_engines: int = 8,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    快捷函数：推理+执行一步到位
    
    示例:
        result = reason_and_execute("公司市场份额下降20%，请分析并采取行动")
        
        # 推理结果
        print(result["reasoning"]["fused_answer"]["text"])
        
        # 执行报告
        print(result["execution_report"]["summary"])
    """
    bridge = get_divine_execution_bridge()
    return bridge.reason_and_execute(
        query=query,
        problem_type=problem_type,
        max_engines=max_engines,
        execute_recommendations=True,
        context=context
    )


__all__ = [
    'DivineExecutionBridge',
    'ExecutableRecommendation',
    'ExecutionReport',
    'DepartmentMapper',
    'RecommendationPriority',
    'get_divine_execution_bridge',
    'reason_and_execute',
]
