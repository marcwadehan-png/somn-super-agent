# -*- coding: utf-8 -*-
"""
Long CoT推理引擎模块
Long Chain-of-Thought Reasoning Engine

提供长思维链推理能力，支持：
- 可配置的最大推理长度
- 推理边界检测
- 中间检查点机制
- 顿悟时刻检测
- 自适应思考分配

作者: Somn AI
版本: V1.0.0
日期: 2026-04-24
"""

from __future__ import annotations

import re
import uuid
import time
import logging
from typing import Dict, List, Optional, Any, Callable, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from collections import deque
import threading

logger = logging.getLogger(__name__)


class InsightType(Enum):
    """顿悟类型枚举"""
    INTEGRATION = "integration"           # 信息整合型
    BREAKTHROUGH = "breakthrough"         # 突破型
    CORRECTION = "correction"             # 纠错型
    SYNTHESIS = "synthesis"              # 综合型
    NONE = "none"                         # 无顿悟


@dataclass
class ThoughtCheckpoint:
    """推理检查点"""
    checkpoint_id: str
    depth: int
    content: str
    partial_conclusions: List[str]
    confidence: float
    validity_score: float
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'checkpoint_id': self.checkpoint_id,
            'depth': self.depth,
            'content': self.content[:100] + '...' if len(self.content) > 100 else self.content,
            'partial_conclusions': self.partial_conclusions,
            'confidence': self.confidence,
            'validity_score': self.validity_score,
            'created_at': self.created_at
        }


@dataclass
class InsightMoment:
    """顿悟时刻"""
    moment_id: str
    insight_type: InsightType
    trigger_content: str
    insight_description: str
    impact_assessment: float  # 影响评估 0-1
    related_checkpoints: List[str]
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'moment_id': self.moment_id,
            'insight_type': self.insight_type.value,
            'trigger_content': self.trigger_content,
            'insight_description': self.insight_description,
            'impact_assessment': self.impact_assessment,
            'related_checkpoints': self.related_checkpoints,
            'created_at': self.created_at
        }


@dataclass
class LongCoTConfig:
    """Long CoT配置"""
    max_thinking_length: int = 2048          # 最大推理Token数
    boundary_threshold: float = 0.85         # 边界检测阈值
    checkpoint_interval: int = 128           # 检查点间隔(Token)
    min_checkpoint_interval: int = 64       # 最小检查点间隔
    enable_insight_detection: bool = True    # 启用顿悟检测
    enable_self_correction: bool = True      # 启用自我纠错
    max_corrections: int = 3                 # 最大纠错次数
    adaptive_allocation: bool = True          # 自适应思考分配
    difficulty_based_scaling: bool = True     # 基于难度的缩放
    
    # 顿悟检测配置
    insight_keywords: List[str] = None       # 顿悟关键词
    insight_patterns: List[str] = None       # 顿悟模式
    
    def __post_init__(self):
        if self.insight_keywords is None:
            self.insight_keywords = [
                "突然", "忽然", "关键", "核心", "本质",
                "顿悟", "领悟", "发现", "意识到", "认识到",
                "整合", "统一", "综合", "归纳", "演绎",
                "原来如此", "关键是", "本质是", "根本问题"
            ]
        if self.insight_patterns is None:
            self.insight_patterns = [
                r"(突然|忽然)意识到",
                r"(关键|核心|本质)是",
                r"通过.*(整合|综合|归纳)",
                r"这说明",
                r"因此可以得出",
                r"综合以上.*可以.*",
                r"(原来|原来如此)",
                r"(关键点|重点)是"
            ]


class BoundaryDetector:
    """推理边界检测器"""
    
    def __init__(self, threshold: float = 0.85):
        self.threshold = threshold
        self.recent_confidences: deque = deque(maxlen=10)
        self.recent_validities: deque = deque(maxlen=10)
        self.degradation_count: int = 0
        self.last_confidence: float = 1.0
        
    def assess_boundary(
        self,
        current_confidence: float,
        current_validity: float,
        reasoning_length: int,
        max_length: int
    ) -> Dict[str, Any]:
        """
        评估是否接近推理边界
        
        Returns:
            Dict包含:
            - is_boundary: bool 是否达到边界
            - boundary_type: str "confidence"|"validity"|"length"|"none"
            - boundary_score: float 0-1 边界程度
            - warning: str 警告信息
        """
        self.recent_confidences.append(current_confidence)
        self.recent_validities.append(current_validity)
        
        # 长度边界评估
        length_ratio = reasoning_length / max_length
        length_boundary = length_ratio > 0.95
        
        # 置信度边界评估
        confidence_drop = self._calculate_confidence_drop()
        confidence_boundary = confidence_drop > (1 - self.threshold)
        
        # 有效性边界评估
        validity_boundary = current_validity < self.threshold
        
        # 综合边界评估
        boundary_scores = {
            'length': length_ratio,
            'confidence_degradation': confidence_drop,
            'validity': 1 - current_validity
        }
        
        max_boundary_type = max(boundary_scores, key=boundary_scores.get)
        max_boundary_score = boundary_scores[max_boundary_type]
        
        is_boundary = (
            length_boundary or 
            confidence_boundary or 
            validity_boundary or
            max_boundary_score > self.threshold
        )
        
        warning = self._generate_warning(
            is_boundary, 
            max_boundary_type, 
            max_boundary_score
        )
        
        self.last_confidence = current_confidence
        
        return {
            'is_boundary': is_boundary,
            'boundary_type': max_boundary_type if is_boundary else 'none',
            'boundary_score': max_boundary_score,
            'warning': warning,
            'recommendations': self._generate_recommendations(boundary_scores)
        }
    
    def _calculate_confidence_drop(self) -> float:
        """计算置信度下降"""
        if len(self.recent_confidences) < 2:
            return 0.0
        
        drops = []
        for i in range(1, len(self.recent_confidences)):
            drop = self.recent_confidences[i-1] - self.recent_confidences[i]
            if drop > 0:
                drops.append(drop)
        
        return sum(drops) / len(drops) if drops else 0.0
    
    def _generate_warning(
        self, 
        is_boundary: bool, 
        boundary_type: str, 
        boundary_score: float
    ) -> str:
        """生成警告信息"""
        if not is_boundary:
            return ""
        
        warnings = {
            'length': f"推理长度接近上限({boundary_score:.0%})，建议考虑终止或回溯",
            'confidence_degradation': f"置信度持续下降({boundary_score:.0%})，可能存在推理错误",
            'validity': f"推理有效性下降({boundary_score:.0%})，建议重新审视推理路径"
        }
        
        return warnings.get(boundary_type, "检测到推理边界，建议重新评估")
    
    def _generate_recommendations(self, boundary_scores: Dict[str, float]) -> List[str]:
        """生成建议"""
        recommendations = []
        
        if boundary_scores['length'] > 0.7:
            recommendations.append("考虑将复杂问题分解为子问题")
        if boundary_scores['confidence_degradation'] > 0.3:
            recommendations.append("回溯到上一个检查点重新推理")
        if boundary_scores['validity'] > 0.5:
            recommendations.append("验证当前推理步骤的有效性")
            
        return recommendations


class InsightDetector:
    """顿悟时刻检测器"""
    
    def __init__(self, config: LongCoTConfig):
        self.config = config
        self.insight_patterns = [
            re.compile(p) for p in config.insight_patterns
        ]
        self.previous_insights: List[str] = []
        
    def detect_insight(
        self,
        new_content: str,
        previous_content: str,
        checkpoints: List[ThoughtCheckpoint]
    ) -> Optional[InsightMoment]:
        """
        检测顿悟时刻
        
        Returns:
            InsightMoment如果检测到顿悟，否则None
        """
        if not self.config.enable_insight_detection:
            return None
        
        insight_type = self._classify_insight(new_content, previous_content)
        
        if insight_type == InsightType.NONE:
            return None
        
        # 计算影响评估
        impact = self._assess_impact(
            new_content, 
            previous_content, 
            insight_type,
            checkpoints
        )
        
        # 创建顿悟时刻
        moment = InsightMoment(
            moment_id=str(uuid.uuid4()),
            insight_type=insight_type,
            trigger_content=self._extract_trigger(new_content),
            insight_description=self._describe_insight(new_content, insight_type),
            impact_assessment=impact,
            related_checkpoints=[cp.checkpoint_id for cp in checkpoints[-3:]]
        )
        
        self.previous_insights.append(new_content)
        
        return moment
    
    def _classify_insight(
        self, 
        new_content: str, 
        previous_content: str
    ) -> InsightType:
        """分类顿悟类型"""
        # 检查关键词
        for keyword in self.config.insight_keywords:
            if keyword in new_content:
                return self._infer_insight_type(new_content)
        
        # 检查模式匹配
        for pattern in self.insight_patterns:
            if pattern.search(new_content):
                return self._infer_insight_type(new_content)
        
        # 检测信息整合型
        if self._is_integration(new_content, previous_content):
            return InsightType.INTEGRATION
        
        # 检测纠错型
        if self._is_correction(new_content, previous_content):
            return InsightType.CORRECTION
        
        return InsightType.NONE
    
    def _infer_insight_type(self, content: str) -> InsightType:
        """推断顿悟类型"""
        integration_keywords = ["整合", "综合", "归纳", "统一", "联系起来"]
        correction_keywords = ["纠正", "修正", "重新审视", "不对", "错误"]
        breakthrough_keywords = ["突破", "关键", "核心", "本质", "顿悟"]
        synthesis_keywords = ["因此", "所以", "得出", "综合以上"]
        
        if any(kw in content for kw in integration_keywords):
            return InsightType.INTEGRATION
        if any(kw in content for kw in correction_keywords):
            return InsightType.CORRECTION
        if any(kw in content for kw in breakthrough_keywords):
            return InsightType.BREAKTHROUGH
        if any(kw in content for kw in synthesis_keywords):
            return InsightType.SYNTHESIS
            
        return InsightType.INTEGRATION
    
    def _is_integration(self, new: str, previous: str) -> bool:
        """检测是否信息整合"""
        integration_markers = [
            "综合", "整合", "结合", "联系起来",
            "考虑到", "综合考虑", "综合分析"
        ]
        
        if any(marker in new for marker in integration_markers):
            # 检查是否确实整合了前面内容
            if len(new) > len(previous) * 0.5:
                return True
                
        return False
    
    def _is_correction(self, new: str, previous: str) -> bool:
        """检测是否纠错型"""
        correction_markers = [
            "不对", "错误", "重新", "纠正", 
            "实际上", "事实上", "但实际上"
        ]
        
        return any(marker in new for marker in correction_markers)
    
    def _extract_trigger(self, content: str) -> str:
        """提取触发顿悟的内容"""
        for pattern in self.insight_patterns:
            match = pattern.search(content)
            if match:
                # 返回匹配上下文
                start = max(0, match.start() - 20)
                end = min(len(content), match.end() + 50)
                return content[start:end]
        
        # 返回最后100字符
        return content[-100:] if len(content) > 100 else content
    
    def _describe_insight(self, content: str, insight_type: InsightType) -> str:
        """描述顿悟内容"""
        type_descriptions = {
            InsightType.INTEGRATION: "信息整合顿悟",
            InsightType.CORRECTION: "纠错型顿悟",
            InsightType.BREAKTHROUGH: "突破型顿悟",
            InsightType.SYNTHESIS: "综合型顿悟"
        }
        
        return type_descriptions.get(insight_type, "未知顿悟")
    
    def _assess_impact(
        self,
        new: str,
        previous: str,
        insight_type: InsightType,
        checkpoints: List[ThoughtCheckpoint]
    ) -> float:
        """评估顿悟影响"""
        base_impact = 0.5
        
        # 根据类型调整
        if insight_type == InsightType.BREAKTHROUGH:
            base_impact += 0.2
        elif insight_type == InsightType.CORRECTION:
            base_impact += 0.15
        
        # 根据内容长度调整
        if len(new) > len(previous) * 0.3:
            base_impact += 0.1
            
        # 根据相关检查点调整
        if len(checkpoints) > 5:
            base_impact += 0.1
            
        return min(base_impact, 1.0)


class SelfCorrector:
    """自我纠错器"""
    
    def __init__(self, max_corrections: int = 3):
        self.max_corrections = max_corrections
        self.corrections: List[Dict[str, Any]] = []
        self.correction_history: deque = deque(maxlen=50)
        
    def should_correct(
        self,
        current_reasoning: str,
        checkpoints: List[ThoughtCheckpoint],
        boundary_assessment: Dict[str, Any]
    ) -> bool:
        """判断是否应该纠错"""
        # 检查纠错次数
        if len(self.corrections) >= self.max_corrections:
            return False
        
        # 检查边界评估
        if boundary_assessment.get('is_boundary'):
            if boundary_assessment.get('boundary_type') in ['confidence_degradation', 'validity']:
                return True
        
        # 检查检查点有效性
        if len(checkpoints) >= 2:
            recent_validity = checkpoints[-1].validity_score
            if recent_validity < 0.6:
                return True
        
        # 检测推理矛盾
        if self._detect_contradiction(checkpoints):
            return True
            
        return False
    
    def perform_correction(
        self,
        reasoning_so_far: str,
        checkpoints: List[ThoughtCheckpoint],
        error_type: str
    ) -> Dict[str, Any]:
        """执行纠错"""
        correction_id = str(uuid.uuid4())
        
        # 确定回溯点
        rollback_point = self._determine_rollback_point(checkpoints)
        
        # 生成纠正内容
        correction_text = self._generate_correction(
            reasoning_so_far,
            checkpoints,
            rollback_point,
            error_type
        )
        
        correction = {
            'correction_id': correction_id,
            'timestamp': datetime.now().isoformat(),
            'rollback_point': rollback_point.to_dict() if rollback_point else None,
            'error_type': error_type,
            'correction_text': correction_text
        }
        
        self.corrections.append(correction)
        self.correction_history.append(correction)
        
        return correction
    
    def _determine_rollback_point(
        self, 
        checkpoints: List[ThoughtCheckpoint]
    ) -> Optional[ThoughtCheckpoint]:
        """确定回溯点"""
        if not checkpoints:
            return None
        
        # 找到有效性最高的检查点
        best_checkpoint = max(checkpoints, key=lambda cp: cp.validity_score)
        
        # 如果当前检查点有效性太低，回溯
        if checkpoints[-1].validity_score < 0.5:
            return best_checkpoint
        
        # 否则回溯到倒数第二个检查点
        if len(checkpoints) >= 2:
            return checkpoints[-2]
            
        return checkpoints[0]
    
    def _generate_correction(
        self,
        reasoning: str,
        checkpoints: List[ThoughtCheckpoint],
        rollback_point: Optional[ThoughtCheckpoint],
        error_type: str
    ) -> str:
        """生成纠正内容"""
        correction_intro = {
            'confidence_degradation': "让我重新审视这个问题，之前的推理可能在某一步出现了偏差。",
            'validity': "经过检查，我发现之前的推理可能存在问题，需要重新思考。",
            'contradiction': "我注意到前面的推理存在矛盾，让我重新推导。"
        }
        
        intro = correction_intro.get(error_type, "让我重新思考这个问题。")
        
        # 添加检查点回顾
        checkpoint_review = ""
        if rollback_point:
            checkpoint_review = f"\n从关键检查点\"{rollback_point.content[:50]}...\"重新开始。"
        
        return f"{intro}{checkpoint_review}"
    
    def _detect_contradiction(self, checkpoints: List[ThoughtCheckpoint]) -> bool:
        """检测推理矛盾"""
        if len(checkpoints) < 3:
            return False
        
        # 检查连续检查点是否有冲突的结论
        for i in range(len(checkpoints) - 1):
            current = checkpoints[i]
            next_cp = checkpoints[i + 1]
            
            # 如果后一个检查点有效性显著下降
            if next_cp.validity_score < current.validity_score - 0.3:
                return True
                
        return False


class AdaptiveThinkingAllocator:
    """自适应思考分配器"""
    
    def __init__(self, config: LongCoTConfig):
        self.config = config
        self.problem_difficulty_cache: Dict[str, float] = {}
        self.thinking_efficiency_history: List[Dict[str, Any]] = []
        
    def estimate_difficulty(self, problem: str) -> float:
        """
        评估问题难度
        
        Returns:
            float: 0-1, 0表示简单, 1表示极难
        """
        # 检查缓存
        problem_hash = str(hash(problem))
        if problem_hash in self.problem_difficulty_cache:
            return self.problem_difficulty_cache[problem_hash]
        
        difficulty = 0.3  # 默认中等难度
        
        # 复杂度指标
        complex_indicators = [
            "复杂", "困难", "挑战", "多因素", "多层次",
            "系统", "综合", "战略", "长期", "全局"
        ]
        simple_indicators = [
            "简单", "直接", "基础", "单", "一步", "快速"
        ]
        
        problem_lower = problem.lower()
        
        # 计算复杂度得分
        complex_count = sum(1 for ind in complex_indicators if ind in problem_lower)
        simple_count = sum(1 for ind in simple_indicators if ind in problem_lower)
        
        difficulty = 0.3 + (complex_count * 0.1) - (simple_count * 0.1)
        difficulty = max(0.1, min(0.95, difficulty))
        
        # 问题长度调整
        if len(problem) > 200:
            difficulty += 0.1
        if len(problem) > 500:
            difficulty += 0.1
            
        self.problem_difficulty_cache[problem_hash] = difficulty
        
        return difficulty
    
    def allocate_thinking_budget(
        self,
        problem: str,
        base_budget: int
    ) -> Dict[str, Any]:
        """
        分配思考预算
        
        Returns:
            Dict包含:
            - budget: int 分配的Token预算
            - difficulty: float 评估的难度
            - reasoning: str 分配理由
        """
        if not self.config.adaptive_allocation:
            return {
                'budget': base_budget,
                'difficulty': 0.5,
                'reasoning': "自适应分配已禁用，使用基础预算"
            }
        
        difficulty = self.estimate_difficulty(problem)
        
        # 根据难度调整预算
        if difficulty < 0.3:
            # 简单问题，减少预算
            budget = int(base_budget * 0.6)
            reasoning = f"问题较简单({difficulty:.1%})，使用较少思考预算"
        elif difficulty < 0.5:
            # 中等问题，标准预算
            budget = base_budget
            reasoning = f"问题中等难度({difficulty:.1%})，使用标准思考预算"
        elif difficulty < 0.7:
            # 较难问题，增加预算
            budget = int(base_budget * 1.5)
            reasoning = f"问题较难({difficulty:.1%})，增加思考预算以确保充分推理"
        else:
            # 极难问题，最大预算
            budget = self.config.max_thinking_length
            reasoning = f"问题极难({difficulty:.1%})，使用最大思考预算"
        
        # 确保不超过配置的最大长度
        budget = min(budget, self.config.max_thinking_length)
        
        return {
            'budget': budget,
            'difficulty': difficulty,
            'reasoning': reasoning
        }
    
    def record_thinking_efficiency(
        self,
        problem: str,
        budget_used: int,
        success: bool,
        quality_score: float
    ):
        """记录思考效率用于后续优化"""
        self.thinking_efficiency_history.append({
            'problem': problem[:50],
            'budget_used': budget_used,
            'success': success,
            'quality_score': quality_score,
            'timestamp': datetime.now().isoformat()
        })
        
        # 保持历史记录在合理范围
        if len(self.thinking_efficiency_history) > 1000:
            self.thinking_efficiency_history = self.thinking_efficiency_history[-500:]


class CheckpointManager:
    """检查点管理器"""
    
    def __init__(self, config: LongCoTConfig):
        self.config = config
        self.checkpoints: List[ThoughtCheckpoint] = []
        self.current_depth: int = 0
        self._token_counter: int = 0
        
    def should_create_checkpoint(
        self,
        current_length: int,
        current_confidence: float,
        current_validity: float
    ) -> bool:
        """判断是否应该创建检查点"""
        # 到达固定间隔
        if current_length - self._token_counter >= self.config.checkpoint_interval:
            return True
        
        # 置信度或有效性显著变化
        if self.checkpoints:
            last_cp = self.checkpoints[-1]
            if abs(current_confidence - last_cp.confidence) > 0.2:
                return True
            if abs(current_validity - last_cp.validity_score) > 0.2:
                return True
        
        # 达到最小间隔且有显著内容变化
        if current_length - self._token_counter >= self.config.min_checkpoint_interval:
            if current_confidence > 0.9 or current_confidence < 0.5:
                return True
                
        return False
    
    def create_checkpoint(
        self,
        content: str,
        partial_conclusions: List[str],
        confidence: float,
        validity: float
    ) -> ThoughtCheckpoint:
        """创建检查点"""
        checkpoint = ThoughtCheckpoint(
            checkpoint_id=str(uuid.uuid4()),
            depth=self.current_depth,
            content=content,
            partial_conclusions=partial_conclusions,
            confidence=confidence,
            validity_score=validity
        )
        
        self.checkpoints.append(checkpoint)
        self._token_counter = len(content) // 4  # 粗略估计Token数
        self.current_depth += 1
        
        return checkpoint
    
    def get_best_checkpoint(self) -> Optional[ThoughtCheckpoint]:
        """获取最佳检查点"""
        if not self.checkpoints:
            return None
            
        return max(self.checkpoints, key=lambda cp: cp.validity_score * cp.confidence)
    
    def rollback_to(self, checkpoint: ThoughtCheckpoint) -> str:
        """回滚到指定检查点"""
        # 找到检查点索引
        idx = next(
            (i for i, cp in enumerate(self.checkpoints) if cp.checkpoint_id == checkpoint.checkpoint_id),
            -1
        )
        
        if idx >= 0:
            self.checkpoints = self.checkpoints[:idx + 1]
            self.current_depth = checkpoint.depth + 1
            
        return checkpoint.content
    
    def clear(self):
        """清空检查点"""
        self.checkpoints = []
        self.current_depth = 0
        self._token_counter = 0


class LongCoTReasoningEngine:
    """
    Long CoT推理引擎
    
    提供长思维链推理能力，支持推理边界检测、中间检查点、
    顿悟时刻检测和自我纠错机制。
    """
    
    VERSION = "6.2.0"
    
    def __init__(
        self,
        llm_callable: Optional[Callable] = None,
        config: Optional[LongCoTConfig] = None
    ):
        """
        初始化Long CoT推理引擎
        
        Args:
            llm_callable: LLM调用函数，签名应为 fn(prompt: str) -> str
            config: Long CoT配置
        """
        self.config = config or LongCoTConfig()
        self.llm_callable = llm_callable
        
        # 初始化各组件
        self.boundary_detector = BoundaryDetector(
            threshold=self.config.boundary_threshold
        )
        self.insight_detector = InsightDetector(self.config)
        self.self_corrector = SelfCorrector(
            max_corrections=self.config.max_corrections
        )
        self.thinking_allocator = AdaptiveThinkingAllocator(self.config)
        self.checkpoint_manager = CheckpointManager(self.config)
        
        # 推理状态
        self._is_reasoning: bool = False
        self._reasoning_lock = threading.Lock()
        
        # 统计信息
        self.stats = {
            'total_reasoning_count': 0,
            'boundary_detections': 0,
            'insights_detected': 0,
            'self_corrections': 0,
            'average_thinking_length': 0
        }
        
        logger.info(f"LongCoTReasoningEngine v{self.VERSION} 初始化完成")
        logger.info(f"  - 最大推理长度: {self.config.max_thinking_length}")
        logger.info(f"  - 边界检测阈值: {self.config.boundary_threshold}")
        logger.info(f"  - 检查点间隔: {self.config.checkpoint_interval}")
        logger.info(f"  - 顿悟检测: {'启用' if self.config.enable_insight_detection else '禁用'}")
        logger.info(f"  - 自我纠错: {'启用' if self.config.enable_self_correction else '禁用'}")
    
    def reason(
        self,
        problem: str,
        context: Optional[Dict[str, Any]] = None,
        llm_callable: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        执行Long CoT推理
        
        Args:
            problem: 问题描述
            context: 额外的上下文信息
            llm_callable: LLM调用函数（会覆盖初始化时设置的）
            
        Returns:
            Dict包含推理结果:
            - reasoning_trace: List[str] 推理过程
            - final_answer: str 最终答案
            - checkpoints: List[Dict] 检查点列表
            - insights: List[Dict] 顿悟时刻列表
            - corrections: List[Dict] 纠错记录
            - boundary_info: Dict 边界评估信息
            - metadata: Dict 元数据
        """
        with self._reasoning_lock:
            self._is_reasoning = True
            
        try:
            # 重置状态
            self.checkpoint_manager.clear()
            self.self_corrector.corrections = []
            
            insights: List[InsightMoment] = []
            corrections: List[Dict[str, Any]] = []
            
            # 分配思考预算
            budget_info = self.thinking_allocator.allocate_thinking_budget(
                problem,
                self.config.max_thinking_length
            )
            
            logger.debug(f"问题难度评估: {budget_info['difficulty']:.1%}")
            logger.debug(f"分配的思考预算: {budget_info['budget']} tokens")
            
            # 获取LLM调用函数
            llm = llm_callable or self.llm_callable
            if not llm:
                raise ValueError("需要提供LLM调用函数")
            
            # 构建初始提示
            system_prompt = self._build_system_prompt()
            user_prompt = self._build_user_prompt(problem, context, budget_info['budget'])
            
            # 初始化推理
            reasoning_so_far = ""
            reasoning_trace = []
            partial_conclusions: List[str] = []
            
            # 推理循环
            max_iterations = 20
            current_confidence = 1.0
            current_validity = 1.0
            
            for iteration in range(max_iterations):
                # 检查是否达到预算上限
                if len(reasoning_so_far) > budget_info['budget'] * 4:
                    logger.debug(f"达到思考预算上限，停止推理")
                    break
                
                # 生成下一步推理
                full_prompt = f"{system_prompt}\n\n{user_prompt}\n\n[推理过程]\n{reasoning_so_far}"
                
                try:
                    next_step = llm(full_prompt)
                except Exception as e:
                    logger.error(f"LLM调用失败: {e}")
                    break
                
                reasoning_so_far += f"\n{next_step}"
                reasoning_trace.append(next_step)
                
                # 更新置信度和有效性（简化评估）
                current_confidence = self._assess_confidence(reasoning_so_far, reasoning_trace)
                current_validity = self._assess_validity(reasoning_so_far, partial_conclusions)
                
                # 检查点管理
                if self.checkpoint_manager.should_create_checkpoint(
                    len(reasoning_so_far),
                    current_confidence,
                    current_validity
                ):
                    # 提取部分结论
                    new_conclusions = self._extract_conclusions(reasoning_so_far)
                    partial_conclusions.extend([c for c in new_conclusions if c not in partial_conclusions])
                    
                    checkpoint = self.checkpoint_manager.create_checkpoint(
                        content=reasoning_so_far,
                        partial_conclusions=partial_conclusions,
                        confidence=current_confidence,
                        validity=current_validity
                    )
                    logger.debug(f"创建检查点 #{len(self.checkpoint_manager.checkpoints)}")
                
                # 顿悟检测
                if len(reasoning_trace) >= 2:
                    insight = self.insight_detector.detect_insight(
                        next_step,
                        reasoning_trace[-2] if len(reasoning_trace) >= 2 else "",
                        self.checkpoint_manager.checkpoints
                    )
                    if insight:
                        insights.append(insight)
                        self.stats['insights_detected'] += 1
                        logger.debug(f"检测到顿悟时刻: {insight.insight_type.value}")
                
                # 边界评估
                boundary_info = self.boundary_detector.assess_boundary(
                    current_confidence,
                    current_validity,
                    len(reasoning_so_far) // 4,
                    budget_info['budget']
                )
                
                if boundary_info['is_boundary']:
                    self.stats['boundary_detections'] += 1
                    logger.debug(f"边界检测: {boundary_info['boundary_type']}")
                    
                    # 自我纠错
                    if self.config.enable_self_correction:
                        if self.self_corrector.should_correct(
                            reasoning_so_far,
                            self.checkpoint_manager.checkpoints,
                            boundary_info
                        ):
                            correction = self.self_corrector.perform_correction(
                                reasoning_so_far,
                                self.checkpoint_manager.checkpoints,
                                boundary_info['boundary_type']
                            )
                            corrections.append(correction)
                            self.stats['self_corrections'] += 1
                            
                            # 回滚到最佳检查点
                            rollback_cp = self.self_corrector._determine_rollback_point(
                                self.checkpoint_manager.checkpoints
                            )
                            if rollback_cp:
                                reasoning_so_far = self.checkpoint_manager.rollback_to(rollback_cp)
                                reasoning_so_far += f"\n\n{correction['correction_text']}"
                            
                            logger.debug(f"执行自我纠错 #{len(corrections)}")
                
                # 检查是否完成
                if self._is_complete(reasoning_so_far, partial_conclusions):
                    logger.debug("推理完成")
                    break
            
            # 生成最终答案
            final_answer = self._generate_answer(reasoning_so_far, problem)
            
            # 更新统计
            self.stats['total_reasoning_count'] += 1
            self._update_average_thinking_length(len(reasoning_so_far) // 4)
            
            return {
                'reasoning_trace': reasoning_trace,
                'final_answer': final_answer,
                'checkpoints': [cp.to_dict() for cp in self.checkpoint_manager.checkpoints],
                'insights': [i.to_dict() for i in insights],
                'corrections': corrections,
                'boundary_info': boundary_info,
                'budget_info': budget_info,
                'metadata': {
                    'engine_version': self.VERSION,
                    'problem': problem[:100],
                    'thinking_length': len(reasoning_so_far) // 4,
                    'iterations': iteration + 1,
                    'final_confidence': current_confidence,
                    'final_validity': current_validity
                }
            }
            
        finally:
            with self._reasoning_lock:
                self._is_reasoning = False
    
    def _build_system_prompt(self) -> str:
        """构建系统提示"""
        return f"""你是一个深度推理AI助手。请进行详细的长链推理，逐步分析问题并给出答案。

要求：
1. 展示完整的推理过程，每一步都要有清晰的逻辑
2. 在关键节点提取部分结论
3. 注意检测推理中的矛盾和错误
4. 当发现更优解时，可以进行自我纠错
5. 最终给出明确、可靠的答案

推理格式示例：
[步骤1] 分析问题...
[步骤2] 提取关键信息...
[关键检查] 总结当前进展... 
[步骤3] 深入分析...
...
[最终答案] 综上所述，答案是..."""
    
    def _build_user_prompt(
        self, 
        problem: str, 
        context: Optional[Dict[str, Any]],
        budget: int
    ) -> str:
        """构建用户提示"""
        prompt = f"""问题：{problem}

请进行深度推理，本次推理最多使用约 {budget} tokens。

"""
        if context:
            prompt += f"附加上下文：\n"
            for key, value in context.items():
                prompt += f"- {key}: {value}\n"
        
        return prompt
    
    def _assess_confidence(self, reasoning: str, trace: List[str]) -> float:
        """评估推理置信度"""
        confidence = 0.8
        
        # 基于推理长度调整
        if len(reasoning) > 500:
            confidence += 0.1
            
        # 基于结论数量调整
        conclusions = self._extract_conclusions(reasoning)
        if len(conclusions) >= 3:
            confidence += 0.1
            
        # 检测否定词（可能表示不确定）
        uncertainty_markers = ["可能", "也许", "不确定", "不太确定", "需要进一步"]
        if any(marker in reasoning for marker in uncertainty_markers):
            confidence -= 0.15
            
        # 检测确定表达
        certainty_markers = ["确定", "明确", "一定", "必然", "毫无疑问"]
        if any(marker in reasoning for marker in certainty_markers):
            confidence += 0.05
            
        return max(0.1, min(1.0, confidence))
    
    def _assess_validity(self, reasoning: str, conclusions: List[str]) -> float:
        """评估推理有效性"""
        validity = 0.8
        
        # 检查结论一致性
        if conclusions:
            # 简化检查：结论越多，有效性越稳定
            if len(conclusions) > 2:
                validity += 0.1
                
        # 检测逻辑矛盾
        contradictions = ["但是", "然而", "不过", "但实际上"]
        if sum(reasoning.count(c) for c in contradictions) > 3:
            validity -= 0.2
            
        # 检测回退
        if "重新" in reasoning or "纠正" in reasoning:
            validity -= 0.1
            
        return max(0.1, min(1.0, validity))
    
    def _extract_conclusions(self, reasoning: str) -> List[str]:
        """提取结论"""
        conclusions = []
        
        # 结论标记词
        markers = [
            "因此", "所以", "得出", "结论是", 
            "总结", "可以得出", "关键是", "本质是"
        ]
        
        for marker in markers:
            if marker in reasoning:
                idx = reasoning.index(marker)
                # 提取标记后的内容
                snippet = reasoning[idx:idx+100]
                if snippet:
                    conclusions.append(snippet.strip())
        
        return conclusions[:5]  # 限制结论数量
    
    def _is_complete(self, reasoning: str, conclusions: List[str]) -> bool:
        """判断推理是否完成"""
        # 检查是否有最终答案标记
        completion_markers = [
            "最终答案", "综上所述", "因此可以确定",
            "答案是", "结论是", "我的回答是"
        ]
        
        for marker in completion_markers:
            if marker in reasoning:
                return True
                
        # 检查结论是否充分
        if len(conclusions) >= 3 and len(reasoning) > 1000:
            return True
            
        return False
    
    def _generate_answer(self, reasoning: str, problem: str) -> str:
        """生成最终答案"""
        # 尝试提取最终答案部分
        completion_markers = [
            "最终答案", "因此", "所以", "结论是", "答案是"
        ]
        
        for marker in completion_markers:
            if marker in reasoning:
                idx = reasoning.index(marker)
                answer = reasoning[idx:]
                
                # 截取到合理长度
                if len(answer) > 500:
                    # 找到下一个段落或句号
                    for sep in ["\n\n", "\n", "。"]:
                        sep_idx = answer.find(sep, 100)
                        if sep_idx > 0:
                            return answer[:sep_idx].strip()
                    return answer[:500].strip()
                    
                return answer.strip()
        
        # 如果没有明确的答案标记，返回最后一段
        paragraphs = reasoning.split("\n\n")
        if paragraphs:
            return paragraphs[-1].strip()
            
        return reasoning.strip()[-500:] if len(reasoning) > 500 else reasoning.strip()
    
    def _update_average_thinking_length(self, length: int):
        """更新平均思考长度"""
        total = self.stats['total_reasoning_count']
        current_avg = self.stats['average_thinking_length']
        
        self.stats['average_thinking_length'] = (
            (current_avg * (total - 1) + length) / total
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            **self.stats,
            'is_reasoning': self._is_reasoning,
            'checkpoint_count': len(self.checkpoint_manager.checkpoints),
            'correction_count': len(self.self_corrector.corrections)
        }
    
    def reset_stats(self):
        """重置统计信息"""
        self.stats = {
            'total_reasoning_count': 0,
            'boundary_detections': 0,
            'insights_detected': 0,
            'self_corrections': 0,
            'average_thinking_length': 0
        }


# 全局单例
_engine_instance: Optional[LongCoTReasoningEngine] = None
_instance_lock = threading.Lock()


def get_long_cot_engine(
    llm_callable: Optional[Callable] = None,
    config: Optional[LongCoTConfig] = None
) -> LongCoTReasoningEngine:
    """获取LongCoT引擎单例"""
    global _engine_instance
    
    with _instance_lock:
        if _engine_instance is None:
            _engine_instance = LongCoTReasoningEngine(llm_callable, config)
        return _engine_instance


def create_long_cot_engine(
    llm_callable: Optional[Callable] = None,
    config: Optional[LongCoTConfig] = None
) -> LongCoTReasoningEngine:
    """创建新的LongCoT引擎实例"""
    return LongCoTReasoningEngine(llm_callable, config)


# 便捷函数
def reason_with_long_cot(
    problem: str,
    llm_callable: Callable,
    context: Optional[Dict[str, Any]] = None,
    config: Optional[LongCoTConfig] = None
) -> Dict[str, Any]:
    """
    使用Long CoT进行推理的便捷函数
    
    Example:
        result = reason_with_long_cot(
            problem="为什么天空是蓝色的？",
            llm_callable=lambda p: openai.Completion.create(prompt=p)
        )
    """
    engine = create_long_cot_engine(llm_callable, config)
    return engine.reason(problem, context)


__all__ = [
    'LongCoTReasoningEngine',
    'LongCoTConfig',
    'BoundaryDetector',
    'InsightDetector',
    'SelfCorrector',
    'AdaptiveThinkingAllocator',
    'CheckpointManager',
    'ThoughtCheckpoint',
    'InsightMoment',
    'InsightType',
    'get_long_cot_engine',
    'create_long_cot_engine',
    'reason_with_long_cot',
]
