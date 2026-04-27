"""
__all__ = [
    'add_historical_data',
    'create_adaptive_learner',
    'create_predictor',
    'get_insights',
    'get_learning_status',
    'learn_from_feedback',
    'predict_performance',
    'predict_trend',
]

预测引擎模块 - 从abyss AI迁移
功能:内容效果预测,趋势预测,自适应学习
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

@dataclass
class PredictionResult:
    """预测结果"""
    value: float
    confidence: float
    trend: str  # 'up', 'down', 'stable'
    factors: List[str]
    recommendations: List[str]

class PredictorEngine:
    """预测引擎 - 基于历史数据预测未来趋势"""
    
    def __init__(self):
        self.models = {}
        self.historical_data = []
        self.weights = {
            'recency': 0.3,
            'frequency': 0.2,
            'engagement': 0.3,
            'quality': 0.2
        }
    
    def add_historical_data(self, data_point: Dict[str, Any]):
        """添加历史数据点"""
        data_point['timestamp'] = datetime.now().isoformat()
        self.historical_data.append(data_point)
        # 保持最近1000条数据
        if len(self.historical_data) > 1000:
            self.historical_data = self.historical_data[-1000:]
    
    def predict_performance(self, content_features: Dict[str, Any]) -> PredictionResult:
        """预测内容表现"""
        if not self.historical_data:
            return PredictionResult(
                value=0.5,
                confidence=0.3,
                trend='unknown',
                factors=['insufficient_data'],
                recommendations=['collect_more_data']
            )
        
        # 计算相似历史内容的表现
        similar_performances = self._find_similar_performances(content_features)
        
        if not similar_performances:
            return PredictionResult(
                value=0.5,
                confidence=0.4,
                trend='stable',
                factors=['no_similar_content'],
                recommendations=['create_baseline_content']
            )
        
        # 加权平均预测
        predicted_value = np.mean(similar_performances)
        confidence = min(0.9, 0.5 + len(similar_performances) * 0.05)
        
        # judge趋势
        recent_avg = np.mean(similar_performances[-10:]) if len(similar_performances) >= 10 else predicted_value
        older_avg = np.mean(similar_performances[:10]) if len(similar_performances) >= 20 else predicted_value
        
        if recent_avg > older_avg * 1.1:
            trend = 'up'
        elif recent_avg < older_avg * 0.9:
            trend = 'down'
        else:
            trend = 'stable'
        
        # recognize影响因素
        factors = self._identify_factors(content_features)
        
        # generate建议
        recommendations = self._generate_recommendations(
            predicted_value, trend, factors, content_features
        )
        
        return PredictionResult(
            value=predicted_value,
            confidence=confidence,
            trend=trend,
            factors=factors,
            recommendations=recommendations
        )
    
    def _find_similar_performances(self, features: Dict[str, Any]) -> List[float]:
        """查找相似历史内容的表现"""
        performances = []
        
        for data in self.historical_data:
            similarity = self._calculate_similarity(features, data)
            if similarity > 0.6:  # 相似度阈值
                if 'performance' in data:
                    performances.append(data['performance'])
        
        return performances
    
    def _calculate_similarity(self, features1: Dict, features2: Dict) -> float:
        """计算两个characteristics向量的相似度"""
        # 基于关键词,类型,长度等计算相似度
        score = 0.0
        total_weight = 0.0
        
        # 类型匹配
        if features1.get('type') == features2.get('type'):
            score += 0.3
        total_weight += 0.3
        
        # 关键词重叠
        keywords1 = set(features1.get('keywords', []))
        keywords2 = set(features2.get('keywords', []))
        if keywords1 and keywords2:
            overlap = len(keywords1 & keywords2) / len(keywords1 | keywords2)
            score += overlap * 0.4
        total_weight += 0.4
        
        # 长度相似度
        len1 = features1.get('length', 0)
        len2 = features2.get('length', 0)
        if len1 > 0 and len2 > 0:
            len_sim = 1 - abs(len1 - len2) / max(len1, len2)
            score += len_sim * 0.3
        total_weight += 0.3
        
        return score / total_weight if total_weight > 0 else 0.0
    
    def _identify_factors(self, features: Dict[str, Any]) -> List[str]:
        """recognize影响表现的因素"""
        factors = []
        
        if features.get('has_images'):
            factors.append('visual_content')
        if features.get('has_data'):
            factors.append('data_driven')
        if features.get('length', 0) > 1000:
            factors.append('long_form')
        if features.get('interactive'):
            factors.append('interactive_elements')
        if features.get('personalized'):
            factors.append('personalization')
        
        return factors if factors else ['standard_content']
    
    def _generate_recommendations(
        self, 
        predicted_value: float, 
        trend: str, 
        factors: List[str],
        features: Dict[str, Any]
    ) -> List[str]:
        """generate优化建议"""
        recommendations = []
        
        if predicted_value < 0.5:
            recommendations.append('improve_content_quality')
            if 'visual_content' not in factors:
                recommendations.append('add_visual_elements')
            if 'data_driven' not in factors:
                recommendations.append('include_data_support')
        
        if trend == 'down':
            recommendations.append('refresh_content_strategy')
            recommendations.append('analyze_audience_feedback')
        
        if features.get('length', 0) < 500:
            recommendations.append('expand_content_depth')
        
        if 'personalization' not in factors:
            recommendations.append('add_personalized_elements')
        
        return recommendations if recommendations else ['maintain_current_approach']
    
    def predict_trend(self, metric: str, days: int = 30) -> Dict[str, Any]:
        """预测metrics趋势"""
        # 提取指定metrics的历史数据
        metric_history = [
            d.get(metric, 0) for d in self.historical_data 
            if metric in d
        ]
        
        if len(metric_history) < 7:
            return {
                'predicted_values': [np.mean(metric_history)] * days if metric_history else [0] * days,
                'confidence_interval': [(0, 0)] * days,
                'trend_direction': 'unknown',
                'growth_rate': 0.0
            }
        
        # 简单线性回归预测
        x = np.arange(len(metric_history))
        y = np.array(metric_history)
        
        # 计算趋势
        slope = np.polyfit(x, y, 1)[0]
        
        # 预测未来值
        last_value = metric_history[-1]
        predicted_values = []
        confidence_intervals = []
        
        for i in range(1, days + 1):
            pred = last_value + slope * i
            predicted_values.append(max(0, pred))
            
            # 置信区间随时间扩大
            std = np.std(metric_history) if len(metric_history) > 1 else pred * 0.1
            margin = std * (1 + i * 0.05)
            confidence_intervals.append((max(0, pred - margin), pred + margin))
        
        return {
            'predicted_values': predicted_values,
            'confidence_interval': confidence_intervals,
            'trend_direction': 'up' if slope > 0 else 'down' if slope < 0 else 'stable',
            'growth_rate': slope / last_value if last_value > 0 else 0.0
        }
    
    def get_insights(self) -> Dict[str, Any]:
        """get数据洞察"""
        if not self.historical_data:
            return {'status': 'no_data', 'insights': []}
        
        insights = []
        
        # 最佳表现内容characteristics
        best_performances = sorted(
            self.historical_data,
            key=lambda x: x.get('performance', 0),
            reverse=True
        )[:10]
        
        if best_performances:
            common_factors = self._extract_common_factors(best_performances)
            insights.append({
                'type': 'success_pattern',
                'description': '高表现内容的共同characteristics',
                'factors': common_factors
            })
        
        # 趋势分析
        if len(self.historical_data) >= 30:
            recent = self.historical_data[-30:]
            older = self.historical_data[-60:-30] if len(self.historical_data) >= 60 else self.historical_data[:30]
            
            recent_avg = np.mean([d.get('performance', 0) for d in recent])
            older_avg = np.mean([d.get('performance', 0) for d in older])
            
            if recent_avg > older_avg * 1.1:
                insights.append({
                    'type': 'positive_trend',
                    'description': '近期表现呈上升趋势',
                    'change': f'+{((recent_avg/older_avg-1)*100):.1f}%'
                })
            elif recent_avg < older_avg * 0.9:
                insights.append({
                    'type': 'negative_trend',
                    'description': '近期表现呈下降趋势',
                    'change': f'{((recent_avg/older_avg-1)*100):.1f}%'
                })
        
        return {
            'status': 'success',
            'total_records': len(self.historical_data),
            'insights': insights
        }
    
    def _extract_common_factors(self, data_list: List[Dict]) -> List[str]:
        """提取共同characteristics"""
        factor_counts = {}
        
        for data in data_list:
            factors = self._identify_factors(data)
            for factor in factors:
                factor_counts[factor] = factor_counts.get(factor, 0) + 1
        
        # 返回出现频率高的characteristics
        threshold = len(data_list) * 0.5
        return [f for f, c in factor_counts.items() if c >= threshold]

class AdaptiveLearner:
    """自适应学习器 - 根据反馈持续优化"""
    
    def __init__(self):
        self.learning_rate = 0.1
        self.weights = {
            'accuracy': 1.0,
            'speed': 1.0,
            'user_satisfaction': 1.0
        }
        self.feedback_history = []
    
    def learn_from_feedback(self, prediction: PredictionResult, actual: float, context: Dict):
        """从反馈中学习"""
        error = abs(prediction.value - actual)
        
        feedback = {
            'timestamp': datetime.now().isoformat(),
            'predicted': prediction.value,
            'actual': actual,
            'error': error,
            'context': context
        }
        
        self.feedback_history.append(feedback)
        
        # 调整权重
        if error > 0.2:
            # 预测偏差大,降低当前模型权重
            self._adjust_weights(context, decrease=True)
        elif error < 0.1:
            # 预测准确,增强相关characteristics权重
            self._adjust_weights(context, decrease=False)
    
    def _adjust_weights(self, context: Dict, decrease: bool):
        """调整权重"""
        factor = 0.9 if decrease else 1.1
        
        for key in context.get('important_factors', []):
            if key in self.weights:
                self.weights[key] *= factor
                # 保持权重在合理范围内
                self.weights[key] = max(0.1, min(5.0, self.weights[key]))
    
    def get_learning_status(self) -> Dict[str, Any]:
        """get学习状态"""
        if not self.feedback_history:
            return {'status': 'no_feedback', 'accuracy': 0.0}
        
        recent_errors = [f['error'] for f in self.feedback_history[-50:]]
        avg_error = np.mean(recent_errors)
        
        return {
            'status': 'learning',
            'total_feedback': len(self.feedback_history),
            'recent_accuracy': 1 - avg_error,
            'current_weights': self.weights,
            'trend': 'improving' if len(recent_errors) > 10 and 
                     np.mean(recent_errors[-10:]) < np.mean(recent_errors[:10])
                     else 'stable'
        }

# 便捷函数
def create_predictor() -> PredictorEngine:
    """创建预测引擎实例"""
    return PredictorEngine()

def create_adaptive_learner() -> AdaptiveLearner:
    """创建自适应学习器实例"""
    return AdaptiveLearner()

# 向后兼容别名 (v1.1 2026-04-06)
ContentPredictor = PredictorEngine
