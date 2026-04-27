"""
__all__ = [
    'analyze_content',
    'assign_variant',
    'create_ab_test_manager',
    'create_content_optimizer',
    'create_experiment',
    'create_strategy_optimizer',
    'get_results',
    'optimize',
    'optimize_strategy',
    'record_event',
]

优化器模块 - 从abyss AI迁移
功能:内容优化,strategy优化,A/B测试管理
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import random

@dataclass
class OptimizationResult:
    """优化结果"""
    original_score: float
    optimized_score: float
    improvements: List[Dict[str, Any]]
    suggestions: List[str]
    confidence: float

@dataclass
class Variant:
    """A/B测试变体"""
    id: str
    name: str
    config: Dict[str, Any]
    metrics: Dict[str, float] = field(default_factory=dict)
    sample_size: int = 0

class ContentOptimizer:
    """内容优化器"""
    
    def __init__(self):
        self.optimization_rules = self._load_rules()
        self.scoring_weights = {
            'readability': 0.2,
            'engagement': 0.3,
            'seo': 0.2,
            'structure': 0.15,
            'uniqueness': 0.15
        }
    
    def _load_rules(self) -> List[Dict]:
        """加载优化规则"""
        return [
            {
                'name': '标题优化',
                'check': lambda c: len(c.get('title', '')) < 10 or len(c.get('title', '')) > 60,
                'suggest': '标题长度应在10-60字符之间,包含核心关键词'
            },
            {
                'name': '段落长度',
                'check': lambda c: any(len(p) > 300 for p in c.get('paragraphs', [])),
                'suggest': '段落应控制在300字符以内,提升可读性'
            },
            {
                'name': '视觉元素',
                'check': lambda c: not c.get('has_images') and not c.get('has_videos'),
                'suggest': '添加图片或视频可提升3倍参与度'
            },
            {
                'name': '数据支持',
                'check': lambda c: not c.get('has_data'),
                'suggest': '加入统计数据增强说服力'
            },
            {
                'name': 'action号召',
                'check': lambda c: not c.get('has_cta'),
                'suggest': '添加明确的action号召(CTA)'
            }
        ]
    
    def analyze_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """分析内容质量"""
        scores = {}
        
        # 可读性评分
        scores['readability'] = self._score_readability(content)
        
        # 参与度评分
        scores['engagement'] = self._score_engagement(content)
        
        # SEO评分
        scores['seo'] = self._score_seo(content)
        
        # 结构评分
        scores['structure'] = self._score_structure(content)
        
        # 独特性评分
        scores['uniqueness'] = self._score_uniqueness(content)
        
        # 加权总分
        total_score = sum(
            scores[k] * self.scoring_weights[k] 
            for k in scores
        )
        
        return {
            'total_score': round(total_score, 2),
            'breakdown': scores,
            'grade': self._score_to_grade(total_score),
            'issues': self._identify_issues(content),
            'strengths': self._identify_strengths(content, scores)
        }
    
    def _score_readability(self, content: Dict) -> float:
        """评分可读性"""
        score = 0.5
        text = content.get('text', '')
        
        if not text:
            return score
        
        # 句子长度
        sentences = text.split('.')
        avg_sentence_len = np.mean([len(s) for s in sentences if s])
        if 20 <= avg_sentence_len <= 50:
            score += 0.2
        
        # 段落结构
        paragraphs = content.get('paragraphs', [])
        if paragraphs and all(len(p) <= 300 for p in paragraphs):
            score += 0.15
        
        # 小标题使用
        if content.get('has_subheadings'):
            score += 0.15
        
        return min(1.0, score)
    
    def _score_engagement(self, content: Dict) -> float:
        """评分参与度"""
        score = 0.3
        
        if content.get('has_images'):
            score += 0.2
        if content.get('has_videos'):
            score += 0.25
        if content.get('interactive'):
            score += 0.15
        if content.get('has_cta'):
            score += 0.1
        
        return min(1.0, score)
    
    def _score_seo(self, content: Dict) -> float:
        """评分SEO"""
        score = 0.4
        
        title = content.get('title', '')
        keywords = content.get('keywords', [])
        
        # 标题长度
        if 10 <= len(title) <= 60:
            score += 0.2
        
        # 关键词密度
        if keywords:
            score += min(0.3, len(keywords) * 0.05)
        
        # Meta描述
        if content.get('meta_description'):
            score += 0.1
        
        return min(1.0, score)
    
    def _score_structure(self, content: Dict) -> float:
        """评分结构"""
        score = 0.5
        
        if content.get('has_introduction'):
            score += 0.15
        if content.get('has_conclusion'):
            score += 0.15
        if content.get('has_subheadings'):
            score += 0.1
        if content.get('bullet_points'):
            score += 0.1
        
        return min(1.0, score)
    
    def _score_uniqueness(self, content: Dict) -> float:
        """评分独特性"""
        score = 0.6
        
        if content.get('original_research'):
            score += 0.2
        if content.get('unique_perspective'):
            score += 0.1
        if content.get('case_studies'):
            score += 0.1
        
        return min(1.0, score)
    
    def _score_to_grade(self, score: float) -> str:
        """分数转等级"""
        if score >= 0.9:
            return 'A+'
        elif score >= 0.8:
            return 'A'
        elif score >= 0.7:
            return 'B'
        elif score >= 0.6:
            return 'C'
        else:
            return 'D'
    
    def _identify_issues(self, content: Dict) -> List[Dict]:
        """recognize问题"""
        issues = []
        
        for rule in self.optimization_rules:
            if rule['check'](content):
                issues.append({
                    'type': rule['name'],
                    'description': rule['suggest'],
                    'severity': 'high' if rule['name'] in ['标题优化', '视觉元素'] else 'medium'
                })
        
        return issues
    
    def _identify_strengths(self, content: Dict, scores: Dict) -> List[str]:
        """recognize优势"""
        strengths = []
        
        for category, score in scores.items():
            if score >= 0.8:
                strengths.append(f'{category}: 优秀')
            elif score >= 0.7:
                strengths.append(f'{category}: 良好')
        
        return strengths
    
    def optimize(self, content: Dict[str, Any]) -> OptimizationResult:
        """优化内容"""
        # 分析原始内容
        original_analysis = self.analyze_content(content)
        original_score = original_analysis['total_score']
        
        # generate优化建议
        improvements = []
        suggestions = []
        
        for issue in original_analysis['issues']:
            improvements.append({
                'area': issue['type'],
                'action': issue['description'],
                'expected_impact': 'high' if issue['severity'] == 'high' else 'medium'
            })
            suggestions.append(issue['description'])
        
        # 计算优化后的预期分数
        potential_gain = len(improvements) * 0.05
        optimized_score = min(1.0, original_score + potential_gain)
        
        return OptimizationResult(
            original_score=original_score,
            optimized_score=optimized_score,
            improvements=improvements,
            suggestions=suggestions,
            confidence=0.7 + min(0.2, len(improvements) * 0.02)
        )

class ABTestManager:
    """A/B测试管理器"""
    
    def __init__(self):
        self.experiments: Dict[str, Dict] = {}
        self.variants: Dict[str, List[Variant]] = {}
    
    def create_experiment(
        self, 
        name: str, 
        hypothesis: str,
        metric: str,
        variants_config: List[Dict]
    ) -> str:
        """创建实验"""
        exp_id = f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.experiments[exp_id] = {
            'id': exp_id,
            'name': name,
            'hypothesis': hypothesis,
            'primary_metric': metric,
            'status': 'running',
            'created_at': datetime.now().isoformat(),
            'total_samples': 0
        }
        
        # 创建变体
        self.variants[exp_id] = []
        for i, config in enumerate(variants_config):
            variant = Variant(
                id=f"{exp_id}_v{i}",
                name=config.get('name', f'Variant {i}'),
                config=config.get('config', {})
            )
            self.variants[exp_id].append(variant)
        
        return exp_id
    
    def assign_variant(self, exp_id: str, user_id: str) -> str:
        """为用户分配变体"""
        if exp_id not in self.variants:
            return None
        
        # 基于用户ID哈希分配,确保一致性
        hash_val = hash(f"{exp_id}_{user_id}")
        variants = self.variants[exp_id]
        variant_index = hash_val % len(variants)
        
        return variants[variant_index].id
    
    def record_event(
        self, 
        exp_id: str, 
        variant_id: str, 
        event_type: str,
        value: float = 1.0
    ):
        """记录事件"""
        if exp_id not in self.variants:
            return
        
        for variant in self.variants[exp_id]:
            if variant.id == variant_id:
                variant.sample_size += 1
                variant.metrics[event_type] = variant.metrics.get(event_type, 0) + value
                break
        
        self.experiments[exp_id]['total_samples'] += 1
    
    def get_results(self, exp_id: str) -> Dict[str, Any]:
        """get实验结果"""
        if exp_id not in self.experiments:
            return {'error': 'Experiment not found'}
        
        exp = self.experiments[exp_id]
        variants = self.variants.get(exp_id, [])
        
        if not variants:
            return {'error': 'No variants found'}
        
        # 计算各变体表现
        variant_results = []
        for v in variants:
            metrics = v.metrics.copy()
            metrics['sample_size'] = v.sample_size
            
            # 计算转化率等
            if 'impressions' in metrics and 'clicks' in metrics:
                metrics['ctr'] = metrics['clicks'] / metrics['impressions']
            
            variant_results.append({
                'id': v.id,
                'name': v.name,
                'metrics': metrics
            })
        
        # 找出最佳变体
        primary_metric = exp['primary_metric']
        best_variant = max(
            variant_results,
            key=lambda x: x['metrics'].get(primary_metric, 0)
        )
        
        return {
            'experiment': exp,
            'variants': variant_results,
            'winner': best_variant,
            'confidence': self._calculate_confidence(variants, primary_metric),
            'recommendation': self._generate_recommendation(variants, best_variant, primary_metric)
        }
    
    def _calculate_confidence(
        self, 
        variants: List[Variant], 
        metric: str
    ) -> float:
        """计算统计置信度"""
        # 简化的置信度计算
        if len(variants) < 2:
            return 0.0
        
        values = [v.metrics.get(metric, 0) for v in variants]
        samples = [v.sample_size for v in variants]
        
        if sum(samples) < 100:
            return 0.5
        
        # 基于样本量和差异计算
        max_val = max(values)
        min_val = min(values)
        
        if max_val == 0:
            return 0.0
        
        relative_diff = (max_val - min_val) / max_val
        
        return min(0.95, 0.5 + relative_diff * 0.3 + min(sum(samples) / 10000, 0.15))
    
    def _generate_recommendation(
        self,
        variants: List[Variant],
        winner: Dict,
        metric: str
    ) -> str:
        """generate建议"""
        confidence = self._calculate_confidence(variants, metric)
        
        if confidence >= 0.9:
            return f"强烈建议采用 '{winner['name']}' 变体"
        elif confidence >= 0.7:
            return f"建议采用 '{winner['name']}' 变体,但建议继续收集数据"
        elif confidence >= 0.5:
            return "数据尚不充分,建议继续实验"
        else:
            return "当前数据无法得出明确结论,建议扩大样本量"

class StrategyOptimizer:
    """strategy优化器"""
    
    def __init__(self):
        self.strategies = []
        self.performance_history = []
    
    def optimize_strategy(
        self, 
        current_strategy: Dict[str, Any],
        goals: Dict[str, float],
        constraints: Dict[str, Any]
    ) -> Dict[str, Any]:
        """优化strategy"""
        optimized = current_strategy.copy()
        adjustments = []
        
        # 基于目标调整strategy
        for goal, target in goals.items():
            current = current_strategy.get('metrics', {}).get(goal, 0)
            gap = target - current
            
            if gap > 0.1:  # 需要提升
                adjustment = self._suggest_adjustment(goal, gap, constraints)
                adjustments.append(adjustment)
                
                # 应用调整
                if 'actions' not in optimized:
                    optimized['actions'] = []
                optimized['actions'].extend(adjustment['actions'])
        
        return {
            'original_strategy': current_strategy,
            'optimized_strategy': optimized,
            'adjustments': adjustments,
            'expected_improvement': self._estimate_improvement(adjustments),
            'implementation_priority': self._prioritize_adjustments(adjustments)
        }
    
    def _suggest_adjustment(
        self, 
        goal: str, 
        gap: float,
        constraints: Dict
    ) -> Dict:
        """建议调整"""
        adjustments_map = {
            'engagement': {
                'actions': ['增加互动元素', '优化内容标题', '添加视觉内容'],
                'resources': 'medium',
                'timeline': '1-2周'
            },
            'conversion': {
                'actions': ['优化CTA按钮', '简化转化流程', '添加社会证明'],
                'resources': 'low',
                'timeline': '1周'
            },
            'reach': {
                'actions': ['扩大分发渠道', '优化SEO', '增加推广预算'],
                'resources': 'high',
                'timeline': '2-4周'
            }
        }
        
        return {
            'goal': goal,
            'gap': gap,
            **adjustments_map.get(goal, {
                'actions': ['分析现状', '制定改进计划'],
                'resources': 'medium',
                'timeline': '2周'
            })
        }
    
    def _estimate_improvement(self, adjustments: List[Dict]) -> float:
        """估计改进幅度"""
        if not adjustments:
            return 0.0
        
        # 简化估计
        total_gap = sum(adj['gap'] for adj in adjustments)
        return min(total_gap * 0.7, 0.5)  # 假设能实现70%的gap
    
    def _prioritize_adjustments(self, adjustments: List[Dict]) -> List[Dict]:
        """优先级排序"""
        # 按gap大小和资源需求排序
        resource_priority = {'low': 3, 'medium': 2, 'high': 1}
        
        return sorted(
            adjustments,
            key=lambda x: (x['gap'] * resource_priority.get(x.get('resources', 'medium'), 2)),
            reverse=True
        )

# 便捷函数
def create_content_optimizer() -> ContentOptimizer:
    """创建内容优化器"""
    return ContentOptimizer()

def create_ab_test_manager() -> ABTestManager:
    """创建A/B测试管理器"""
    return ABTestManager()

def create_strategy_optimizer() -> StrategyOptimizer:
    """创建strategy优化器"""
    return StrategyOptimizer()
