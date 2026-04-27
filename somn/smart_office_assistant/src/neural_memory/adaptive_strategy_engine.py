"""
__all__ = [
    'get_adaptive_recommendation',
    'get_strategy_performance',
    'get_strategy_weights',
    'recommend_strategies',
    'select_strategies',
]

自适应策略引擎 - Adaptive Strategy Engine v1.0.0
根据数据特征、任务类型、历史表现自动选择最优策略组合

核心能力:
1. 场景评估 - 分析数据特征判断学习场景
2. 策略推荐 - 基于ROI历史选择最优策略
3. 权重计算 - 根据上下文调整策略权重
4. 自适应选择 - 动态组合多种策略
"""

from __future__ import annotations

import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

import logging

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════════

class LearningScene(Enum):
    """学习场景类型"""
    COLD_START = "cold_start"           # 冷启动 - 数据稀少
    DATA_RICH = "data_rich"            # 数据丰富
    FEEDBACK_HEAVY = "feedback_heavy"  # 反馈密集
    TIME_SENSITIVE = "time_sensitive"  # 时效敏感
    QUALITY_FOCUS = "quality_focus"     # 质量优先
    EFFICIENCY_FOCUS = "efficiency_focus"  # 效率优先
    EXPLORATION = "exploration"        # 探索模式
    EXPLOITATION = "exploitation"      # 利用模式

@dataclass
class SceneAnalysis:
    """场景分析结果"""
    scene_type: LearningScene
    confidence: float  # 场景识别置信度 0-1
    features: Dict[str, float]  # 场景特征得分
    recommendations: List[str]  # 针对此场景的建议
    strategy_weights: Dict[str, float]  # 策略权重建议

@dataclass
class StrategyPerformance:
    """策略历史表现"""
    strategy_type: str
    total_executions: int = 0
    successful_executions: int = 0
    avg_outcome: float = 0.0
    avg_duration: float = 0.0
    avg_feedback: float = 0.0
    last_execution: Optional[str] = None
    
    # 时序表现
    recent_success_rate: float = 0.0  # 最近10次的成功率
    trend: str = "stable"  # improving / declining / stable
    
    @property
    def success_rate(self) -> float:
        if self.total_executions == 0:
            return 0.0
        return self.successful_executions / self.total_executions
    
    @property
    def roi_score(self) -> float:
        """综合ROI评分"""
        return (
            self.success_rate * 0.4 +
            (self.avg_feedback + 1) / 2 * 0.3 +
            self.avg_outcome * 0.3
        )

@dataclass
class StrategyRecommendation:
    """策略推荐结果"""
    primary_strategy: str
    secondary_strategies: List[str]
    weights: Dict[str, float]
    reasoning: List[str]
    confidence: float
    scene_analysis: SceneAnalysis

# ═══════════════════════════════════════════════════════════════════
# 自适应策略引擎
# ═══════════════════════════════════════════════════════════════════

class AdaptiveStrategyEngine:
    """
    自适应策略引擎 v1.0.0
    
    根据场景特征和历史表现，自动选择最优策略组合
    
    核心流程:
    1. analyze_scene() - 分析当前学习场景
    2. get_strategy_performance() - 获取策略历史表现
    3. recommend_strategies() - 生成策略推荐
    4. select_strategies() - 选择最终执行策略
    """
    
    def __init__(self, base_path: str = None):
        from src.core.paths import LEARNING_DIR
        self.base_path = Path(base_path) if base_path else LEARNING_DIR
        self.cache_path = self.base_path / "adaptive_cache"
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # 策略性能记录
        self.performance_path = self.cache_path / "strategy_performance.json"
        self._performance_cache: Dict[str, StrategyPerformance] = {}
        self._load_performance()
        
        # 场景特征阈值
        self.scene_thresholds = {
            "cold_start": {"min_data": 3, "min_quality": 0.0},
            "data_rich": {"min_data": 20, "min_quality": 0.5},
            "feedback_heavy": {"min_feedback": 10, "feedback_ratio": 0.3},
            "time_sensitive": {"max_age_days": 1},
            "quality_focus": {"min_quality": 0.7},
            "efficiency_focus": {"max_duration": 30.0},
        }
        
        # 策略-场景映射
        self.strategy_scene_map = {
            LearningScene.COLD_START: {
                "primary": "DAILY",
                "secondary": ["THREE_TIER"],
                "reason": "冷启动场景需要稳健的每日学习策略，逐步积累"
            },
            LearningScene.DATA_RICH: {
                "primary": "ENHANCED",
                "secondary": ["DAILY", "FEEDBACK"],
                "reason": "数据丰富时启用增强学习，最大化知识提取"
            },
            LearningScene.FEEDBACK_HEAVY: {
                "primary": "FEEDBACK",
                "secondary": ["ENHANCED", "DAILY"],
                "reason": "反馈密集时启用反馈闭环，精准调整"
            },
            LearningScene.TIME_SENSITIVE: {
                "primary": "DAILY",
                "secondary": ["SOLUTION"],
                "reason": "时效敏感场景优先快速学习，避免深度挖掘"
            },
            LearningScene.QUALITY_FOCUS: {
                "primary": "ENHANCED",
                "secondary": ["THREE_TIER", "FEEDBACK"],
                "reason": "质量优先场景启用多层验证，确保知识可靠性"
            },
            LearningScene.EFFICIENCY_FOCUS: {
                "primary": "SOLUTION",
                "secondary": ["DAILY"],
                "reason": "效率优先场景直接复用成熟方案"
            },
            LearningScene.EXPLORATION: {
                "primary": "THREE_TIER",
                "secondary": ["DAILY", "ENHANCED"],
                "reason": "探索模式需要多角度交叉验证"
            },
            LearningScene.EXPLOITATION: {
                "primary": "FEEDBACK",
                "secondary": ["SOLUTION"],
                "reason": "利用模式基于反馈精调现有知识"
            },
        }
        
        logger.info("自适应策略引擎初始化完成")
    
    # ─────────────────────────────────────────────────────────────────
    # 核心API
    # ─────────────────────────────────────────────────────────────────
    
    def analyze_scene(self, 
                      data_scan_result, 
                      feedback_stats: Optional[Dict] = None,
                      task_context: Optional[Dict] = None) -> SceneAnalysis:
        """
        分析当前学习场景
        
        Args:
            data_scan_result: 数据扫描结果
            feedback_stats: 反馈统计 {count, recent_avg, ratio}
            task_context: 任务上下文 {time_pressure, quality_requirement, ...}
        
        Returns:
            SceneAnalysis: 场景分析结果
        """
        features = {}
        scene_votes = defaultdict(float)
        
        # 1. 数据量评估
        total_data = data_scan_result.total if hasattr(data_scan_result, 'total') else 0
        local_data = data_scan_result.local_count if hasattr(data_scan_result, 'local_count') else 0
        
        features["data_volume"] = min(1.0, total_data / 50)
        features["local_ratio"] = local_data / max(total_data, 1)
        
        if total_data < 5:
            scene_votes[LearningScene.COLD_START] += 0.8
        elif total_data >= 20:
            scene_votes[LearningScene.DATA_RICH] += 0.7
        
        # 2. 数据时效性评估
        if hasattr(data_scan_result, 'findings'):
            recency_days = self._estimate_data_recency(data_scan_result)
            features["data_recency"] = max(0, 1 - recency_days / 7)
            if recency_days <= 1:
                scene_votes[LearningScene.TIME_SENSITIVE] += 0.6
        
        # 3. 反馈强度评估
        if feedback_stats:
            fb_count = feedback_stats.get("count", 0)
            fb_ratio = feedback_stats.get("ratio", 0)
            features["feedback_density"] = min(1.0, fb_count / 20)
            
            if fb_count >= 10 and fb_ratio >= 0.3:
                scene_votes[LearningScene.FEEDBACK_HEAVY] += 0.8
        
        # 4. 任务上下文评估
        if task_context:
            time_pressure = task_context.get("time_pressure", 0.5)
            quality_req = task_context.get("quality_requirement", 0.5)
            
            features["time_pressure"] = time_pressure
            features["quality_requirement"] = quality_req
            
            if time_pressure > 0.7:
                scene_votes[LearningScene.EFFICIENCY_FOCUS] += time_pressure
            if quality_req > 0.7:
                scene_votes[LearningScene.QUALITY_FOCUS] += quality_req
        
        # 5. 探索-利用平衡
        exploration_score = self._calculate_exploration_score()
        features["exploration_tendency"] = exploration_score
        
        if exploration_score > 0.6:
            scene_votes[LearningScene.EXPLORATION] += exploration_score
        elif exploration_score < 0.3:
            scene_votes[LearningScene.EXPLOITATION] += (1 - exploration_score)
        
        # 6. 确定主场景
        if not scene_votes:
            scene_votes[LearningScene.DATA_RICH] = 0.5
        
        primary_scene = max(scene_votes, key=scene_votes.get)
        confidence = scene_votes[primary_scene] / sum(scene_votes.values()) if scene_votes else 0.5
        
        # 7. 生成建议
        recommendations = self._generate_scene_recommendations(primary_scene, features)
        
        # 8. 计算策略权重
        weights = self._calculate_strategy_weights(primary_scene, features)
        
        return SceneAnalysis(
            scene_type=primary_scene,
            confidence=confidence,
            features=features,
            recommendations=recommendations,
            strategy_weights=weights
        )
    
    def get_strategy_performance(self, strategy_type: str) -> StrategyPerformance:
        """
        获取策略历史表现
        
        Args:
            strategy_type: 策略类型
        
        Returns:
            StrategyPerformance: 策略表现
        """
        return self._performance_cache.get(strategy_type, StrategyPerformance(
            strategy_type=strategy_type
        ))
    
    def get_strategy_weights(self, scene: SceneAnalysis) -> Dict[str, float]:
        """
        根据场景获取策略权重
        
        Args:
            scene: 场景分析结果
        
        Returns:
            Dict[str, float]: 策略权重映射
        """
        return scene.strategy_weights
    
    def recommend_strategies(self, 
                            scene: SceneAnalysis,
                            max_strategies: int = 3) -> StrategyRecommendation:
        """
        推荐策略组合
        
        Args:
            scene: 场景分析结果
            max_strategies: 最大策略数量
        
        Returns:
            StrategyRecommendation: 策略推荐
        """
        reasoning = []
        
        # 1. 获取场景推荐
        scene_rec = self.strategy_scene_map.get(scene.scene_type, {})
        primary = scene_rec.get("primary", "DAILY")
        secondary = scene_rec.get("secondary", [])
        reasoning.append(scene_rec.get("reason", "基于场景特征选择"))
        
        # 2. 融合ROI表现
        all_strategies = [primary] + secondary
        roi_scores = {}
        for stype in all_strategies:
            perf = self.get_strategy_performance(stype)
            roi_scores[stype] = perf.roi_score
            if perf.total_executions > 0:
                reasoning.append(f"{stype}: ROI={perf.roi_score:.2f}, 成功率={perf.success_rate:.1%}")
        
        # 3. 计算综合权重
        base_weights = {s: 1.0 for s in all_strategies}
        for stype, score in roi_scores.items():
            base_weights[stype] = 1.0 + score * 0.5  # ROI加成
        
        # 场景特征调整
        if scene.scene_type == LearningScene.FEEDBACK_HEAVY:
            base_weights["FEEDBACK"] = base_weights.get("FEEDBACK", 1.0) * 1.5
        elif scene.scene_type == LearningScene.QUALITY_FOCUS:
            base_weights["ENHANCED"] = base_weights.get("ENHANCED", 1.0) * 1.3
        
        # 4. 归一化权重
        total_weight = sum(base_weights.values())
        weights = {s: w / total_weight for s, w in base_weights.items()}
        
        # 5. 排序并截取
        sorted_strategies = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        primary = sorted_strategies[0][0]
        secondary = [s for s, _ in sorted_strategies[1:max_strategies]]
        
        # 6. 过滤低权重策略
        weights = {s: w for s, w in weights.items() if w >= 0.1}
        
        return StrategyRecommendation(
            primary_strategy=primary,
            secondary_strategies=secondary,
            weights=weights,
            reasoning=reasoning,
            confidence=scene.confidence,
            scene_analysis=scene
        )
    
    def select_strategies(self,
                         data_scan_result,
                         feedback_stats: Optional[Dict] = None,
                         task_context: Optional[Dict] = None,
                         strategy_types: Optional[List[str]] = None) -> Tuple[List[str], Dict]:
        """
        选择最终执行的策略组合（主要入口）
        
        Args:
            data_scan_result: 数据扫描结果
            feedback_stats: 反馈统计
            task_context: 任务上下文
            strategy_types: 可选的策略类型限制
        
        Returns:
            (策略列表, 完整推荐结果)
        """
        # 1. 场景分析
        scene = self.analyze_scene(data_scan_result, feedback_stats, task_context)
        
        # 2. 如果指定了策略类型，优先使用
        if strategy_types:
            return strategy_types, {"source": "explicit", "scene": scene}
        
        # 3. 获取推荐
        recommendation = self.recommend_strategies(scene)
        
        # 4. 返回策略列表
        strategies = [recommendation.primary_strategy] + recommendation.secondary_strategies
        
        logger.info(f"自适应策略选择: {scene.scene_type.value} → {strategies}")
        
        return strategies, {
            "source": "adaptive",
            "recommendation": recommendation,
            "scene": scene
        }
    
    # ─────────────────────────────────────────────────────────────────
    # 性能记录更新
    # ─────────────────────────────────────────────────────────────────
    
    def record_execution(self, 
                        strategy_type: str, 
                        success: bool,
                        outcome: float,
                        duration: float,
                        feedback: Optional[float] = None):
        """
        记录策略执行结果
        
        Args:
            strategy_type: 策略类型
            success: 是否成功
            outcome: 结果评分
            duration: 执行耗时
            feedback: 用户反馈
        """
        if strategy_type not in self._performance_cache:
            self._performance_cache[strategy_type] = StrategyPerformance(
                strategy_type=strategy_type
            )
        
        perf = self._performance_cache[strategy_type]
        perf.total_executions += 1
        if success:
            perf.successful_executions += 1
        
        # 更新滑动平均
        n = perf.total_executions
        perf.avg_outcome = (perf.avg_outcome * (n - 1) + outcome) / n
        perf.avg_duration = (perf.avg_duration * (n - 1) + duration) / n
        if feedback is not None:
            perf.avg_feedback = (perf.avg_feedback * (n - 1) + feedback) / n
        
        # 更新最近表现
        perf.recent_success_rate = self._calculate_recent_success_rate(strategy_type)
        perf.trend = self._calculate_trend(strategy_type)
        perf.last_execution = datetime.now().isoformat()
        
        # 持久化
        self._save_performance()
    
    def get_adaptive_recommendation(self, 
                                   context: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取自适应推荐（综合入口）
        
        Args:
            context: {
                data_scan: DataScanResult,
                feedback: Dict,
                task: Dict,
                roi_history: Dict
            }
        
        Returns:
            完整推荐报告
        """
        data_scan = context.get("data_scan")
        feedback = context.get("feedback")
        task = context.get("task")
        
        if data_scan is None:
            return {"error": "缺少数据扫描结果"}
        
        # 执行完整流程
        strategies, meta = self.select_strategies(
            data_scan, feedback, task
        )
        
        # 添加性能详情
        perf_details = {}
        for s in strategies:
            perf = self.get_strategy_performance(s)
            perf_details[s] = {
                "success_rate": perf.success_rate,
                "roi_score": perf.roi_score,
                "trend": perf.trend,
                "executions": perf.total_executions
            }
        
        return {
            "selected_strategies": strategies,
            "weights": meta.get("recommendation").weights if "recommendation" in meta else {},
            "scene": meta.get("scene").scene_type.value if "scene" in meta else None,
            "confidence": meta.get("recommendation").confidence if "recommendation" in meta else 0,
            "performance": perf_details,
            "reasoning": meta.get("recommendation").reasoning if "recommendation" in meta else []
        }
    
    # ─────────────────────────────────────────────────────────────────
    # 内部方法
    # ─────────────────────────────────────────────────────────────────
    
    def _load_performance(self):
        """加载性能缓存"""
        if self.performance_path.exists():
            try:
                with open(self.performance_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for stype, perf_data in data.items():
                        self._performance_cache[stype] = StrategyPerformance(**perf_data)
                logger.debug(f"加载策略性能记录: {len(self._performance_cache)} 条")
            except Exception as e:
                logger.warning(f"加载性能缓存失败: {e}")
    
    def _save_performance(self):
        """保存性能缓存"""
        try:
            data = {
                stype: {
                    "strategy_type": perf.strategy_type,
                    "total_executions": perf.total_executions,
                    "successful_executions": perf.successful_executions,
                    "avg_outcome": perf.avg_outcome,
                    "avg_duration": perf.avg_duration,
                    "avg_feedback": perf.avg_feedback,
                    "last_execution": perf.last_execution,
                    "recent_success_rate": perf.recent_success_rate,
                    "trend": perf.trend
                }
                for stype, perf in self._performance_cache.items()
            }
            with open(self.performance_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"保存性能缓存失败: {e}")
    
    def _estimate_data_recency(self, data_scan_result) -> float:
        """估算数据时效性（天）"""
        if hasattr(data_scan_result, 'findings') and data_scan_result.findings:
            try:
                # 尝试从第一条finding获取时间
                first = data_scan_result.findings[0]
                if 'timestamp' in first:
                    ts = datetime.fromisoformat(first['timestamp'])
                    return (datetime.now() - ts).total_seconds() / 86400
            except Exception as e:
                logger.debug(f"return (datetime.now() - ts).total_seconds() / 86400失败: {e}")
        return 7.0  # 默认7天前
    
    def _calculate_exploration_score(self) -> float:
        """计算探索倾向得分"""
        if not self._performance_cache:
            return 0.5  # 默认中等探索
        
        total_new = 0
        total_old = 0
        for perf in self._performance_cache.values():
            if perf.trend == "declining":
                total_new += 1
            elif perf.trend == "improving":
                total_old += 1
        
        if total_new + total_old == 0:
            return 0.5
        
        return total_new / (total_new + total_old)
    
    def _calculate_recent_success_rate(self, strategy_type: str) -> float:
        """计算最近成功率"""
        # 简化实现：使用总成功率
        perf = self._performance_cache.get(strategy_type)
        return perf.success_rate if perf else 0.0
    
    def _calculate_trend(self, strategy_type: str) -> str:
        """计算趋势"""
        perf = self._performance_cache.get(strategy_type)
        if not perf or perf.total_executions < 5:
            return "stable"
        
        # 简化实现
        if perf.recent_success_rate > perf.success_rate * 1.1:
            return "improving"
        elif perf.recent_success_rate < perf.success_rate * 0.9:
            return "declining"
        return "stable"
    
    def _generate_scene_recommendations(self, 
                                       scene: LearningScene,
                                       features: Dict) -> List[str]:
        """生成场景建议"""
        recs = []
        
        if scene == LearningScene.COLD_START:
            recs.append("建议: 降低学习阈值，耐心积累")
            recs.append("提示: 冷启动阶段适合快速试错")
        elif scene == LearningScene.DATA_RICH:
            recs.append("建议: 启用深度学习，提取高阶模式")
            recs.append("提示: 充足数据可支撑复杂关联学习")
        elif scene == LearningScene.FEEDBACK_HEAVY:
            recs.append("建议: 启用反馈闭环，快速调整")
            recs.append("提示: 高反馈场景适合精细化调优")
        elif scene == LearningScene.TIME_SENSITIVE:
            recs.append("建议: 优先效率，选择成熟方案")
            recs.append("提示: 时效敏感场景避免深度探索")
        
        return recs
    
    def _calculate_strategy_weights(self,
                                   scene: LearningScene,
                                   features: Dict) -> Dict[str, float]:
        """计算策略权重"""
        weights = {
            "DAILY": 0.3,
            "THREE_TIER": 0.2,
            "ENHANCED": 0.2,
            "SOLUTION": 0.15,
            "FEEDBACK": 0.15
        }
        
        # 根据场景调整
        if scene == LearningScene.COLD_START:
            weights["DAILY"] = 0.5
            weights["THREE_TIER"] = 0.3
        elif scene == LearningScene.DATA_RICH:
            weights["ENHANCED"] = 0.4
            weights["DAILY"] = 0.2
        elif scene == LearningScene.FEEDBACK_HEAVY:
            weights["FEEDBACK"] = 0.5
            weights["ENHANCED"] = 0.3
        
        return weights


# ═══════════════════════════════════════════════════════════════════
# 便捷函数
# ═══════════════════════════════════════════════════════════════════

_engine_instance = None

def get_adaptive_engine() -> AdaptiveStrategyEngine:
    """获取引擎单例"""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = AdaptiveStrategyEngine()
    return _engine_instance

def recommend_strategies(*args, **kwargs) -> StrategyRecommendation:
    """便捷函数：推荐策略"""
    return get_adaptive_engine().recommend_strategies(*args, **kwargs)

def select_strategies(*args, **kwargs) -> Tuple[List[str], Dict]:
    """便捷函数：选择策略"""
    return get_adaptive_engine().select_strategies(*args, **kwargs)

def get_strategy_performance(strategy_type: str) -> StrategyPerformance:
    """便捷函数：获取策略表现"""
    return get_adaptive_engine().get_strategy_performance(strategy_type)

def get_strategy_weights(scene: SceneAnalysis) -> Dict[str, float]:
    """便捷函数：获取策略权重"""
    return get_adaptive_engine().get_strategy_weights(scene)

def get_adaptive_recommendation(context: Dict[str, Any]) -> Dict[str, Any]:
    """便捷函数：综合推荐"""
    return get_adaptive_engine().get_adaptive_recommendation(context)
