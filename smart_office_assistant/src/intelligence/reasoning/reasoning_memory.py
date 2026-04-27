"""
__all__ = [
    'analyze_reasoning_patterns',
    'check_cache',
    'clear_cache',
    'clear_old_traces',
    'export_traces',
    'from_dict',
    'get_failed_reasonings',
    'get_reasoning_pattern',
    'get_statistics',
    'get_successful_reasonings',
    'import_traces',
    'retrieve_reasoning_trace',
    'retrieve_similar_reasoning',
    'save_reasoning_trace',
    'to_dict',
]

推理记忆系统 - 存储和检索推理过程

功能:
- 保存推理轨迹
- 检索相似推理
- 推理结果缓存
- 推理模式学习

作者: Somn AI
版本: v4.0.0
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
import json
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class ReasoningMode(Enum):
    """推理模式"""
    CHAIN_OF_THOUGHT = "chain_of_thought"
    TREE_OF_THOUGHTS = "tree_of_thoughts"
    GRAPH_OF_THOUGHTS = "graph_of_thoughts"
    META_REASONING = "meta_reasoning"

@dataclass
class ReasoningStep:
    """推理步骤"""
    step_number: int
    description: str
    reasoning: str
    conclusion: str
    confidence: float = 0.9
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)

@dataclass
class ReasoningTrace:
    """推理轨迹"""
    trace_id: str
    problem: str
    reasoning_mode: ReasoningMode
    steps: List[ReasoningStep]
    final_answer: str
    confidence: float
    created_at: datetime
    metadata: Optional[Dict] = None
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        data = asdict(self)
        data['reasoning_mode'] = self.reasoning_mode.value
        data['created_at'] = self.created_at.isoformat()
        data['steps'] = [step.to_dict() for step in self.steps]
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ReasoningTrace':
        """从字典创建"""
        data = data.copy()
        data['reasoning_mode'] = ReasoningMode(data['reasoning_mode'])
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['steps'] = [ReasoningStep(**step) for step in data['steps']]
        return cls(**data)

@dataclass
class ReasoningPattern:
    """推理模式"""
    pattern_id: str
    pattern_type: str
    problem_templates: List[str]
    typical_steps: List[Dict]
    success_rate: float
    usage_count: int
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)

class ReasoningMemory:
    """
    推理记忆系统
    
    核心功能:
    1. 保存推理轨迹
    2. 检索相似推理
    3. 推理结果缓存
    4. 推理模式学习
    """
    
    def __init__(self):
        """init推理记忆"""
        # 推理轨迹存储
        self.traces: Dict[str, ReasoningTrace] = {}
        
        # 推理模式库
        self.patterns: Dict[str, ReasoningPattern] = {}
        
        # 问题-结果缓存
        self.cache: Dict[str, ReasoningTrace] = {}
        
        # 统计信息
        self.stats = {
            'total_traces': 0,
            'total_patterns': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'similar_retrievals': 0
        }
        
        logger.info("推理记忆系统init完成")
    
    def save_reasoning_trace(self, trace: ReasoningTrace) -> bool:
        """
        保存推理轨迹
        
        Args:
            trace: 推理轨迹
            
        Returns:
            是否成功
        """
        try:
            self.traces[trace.trace_id] = trace
            self.stats['total_traces'] += 1
            
            # 添加到缓存
            self.cache[trace.problem] = trace
            
            # 提取推理模式
            self._extract_pattern(trace)
            
            logger.info(f"推理轨迹已保存: {trace.trace_id}")
            return True
            
        except Exception as e:
            logger.error(f"保存推理轨迹失败: {e}")
            return False
    
    def retrieve_reasoning_trace(self, trace_id: str) -> Optional[ReasoningTrace]:
        """
        按ID检索推理轨迹
        
        Args:
            trace_id: 轨迹ID
            
        Returns:
            推理轨迹或None
        """
        return self.traces.get(trace_id)
    
    def retrieve_similar_reasoning(self, problem: str, 
                                   top_k: int = 5,
                                   min_similarity: float = 0.5) -> List[ReasoningTrace]:
        """
        检索相似推理
        
        Args:
            problem: 问题
            top_k: 返回前k个
            min_similarity: 最小相似度
            
        Returns:
            相似推理轨迹列表
        """
        self.stats['similar_retrievals'] += 1
        
        similar_traces = []
        
        for trace in self.traces.values():
            similarity = self._calculate_similarity(problem, trace.problem)
            
            if similarity >= min_similarity:
                similar_traces.append((trace, similarity))
        
        # 按相似度排序
        similar_traces.sort(key=lambda x: x[1], reverse=True)
        
        result = [trace for trace, _ in similar_traces[:top_k]]
        
        logger.debug(f"检索相似推理: {len(result)}个结果")
        return result
    
    def _calculate_similarity(self, problem1: str, problem2: str) -> float:
        """
        计算问题相似度
        
        简化实现: 基于关键词重叠
        """
        # 移除标点符号
        import string
        translator = str.maketrans('', '', string.punctuation)
        problem1_clean = problem1.lower().translate(translator)
        problem2_clean = problem2.lower().translate(translator)
        
        words1 = set(problem1_clean.split())
        words2 = set(problem2_clean.split())
        
        if not words1 or not words2:
            return 0.0
        
        # Jaccard相似度
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        similarity = intersection / union if union > 0 else 0.0
        
        return similarity
    
    def check_cache(self, problem: str) -> Optional[ReasoningTrace]:
        """
        检查缓存
        
        Args:
            problem: 问题
            
        Returns:
            缓存的推理轨迹或None
        """
        # 精确匹配
        if problem in self.cache:
            self.stats['cache_hits'] += 1
            return self.cache[problem]
        
        # 模糊匹配
        for cached_problem, trace in self.cache.items():
            similarity = self._calculate_similarity(problem, cached_problem)
            if similarity > 0.8:
                self.stats['cache_hits'] += 1
                return trace
        
        self.stats['cache_misses'] += 1
        return None
    
    def _extract_pattern(self, trace: ReasoningTrace):
        """
        从推理轨迹中提取模式
        
        Args:
            trace: 推理轨迹
        """
        # 简化实现: 基于步骤结构
        pattern_type = trace.reasoning_mode.value
        
        # 提取步骤结构
        typical_steps = [
            {
                'step_type': step.description.split(':')[0] if ':' in step.description else 'analysis',
                'reasoning_type': step.reasoning.split()[0] if step.reasoning else 'deduction'
            }
            for step in trace.steps
        ]
        
        # generate模式ID
        pattern_id = f"{pattern_type}_{'_'.join([s['step_type'] for s in typical_steps[:3]])}"
        
        # 更新模式
        if pattern_id in self.patterns:
            pattern = self.patterns[pattern_id]
            pattern.usage_count += 1
            pattern.success_rate = (
                (pattern.success_rate * (pattern.usage_count - 1) + trace.confidence)
                / pattern.usage_count
            )
        else:
            pattern = ReasoningPattern(
                pattern_id=pattern_id,
                pattern_type=pattern_type,
                problem_templates=[trace.problem],
                typical_steps=typical_steps,
                success_rate=trace.confidence,
                usage_count=1
            )
            self.patterns[pattern_id] = pattern
            self.stats['total_patterns'] += 1
    
    def get_reasoning_pattern(self, problem: str) -> Optional[ReasoningPattern]:
        """
        get适合问题的推理模式
        
        Args:
            problem: 问题
            
        Returns:
            推理模式或None
        """
        best_pattern = None
        best_score = 0.0
        
        for pattern in self.patterns.values():
            # 检查问题模板匹配
            for template in pattern.problem_templates:
                similarity = self._calculate_similarity(problem, template)
                score = similarity * pattern.success_rate
                
                if score > best_score:
                    best_score = score
                    best_pattern = pattern
        
        return best_pattern if best_score > 0.3 else None
    
    def get_successful_reasonings(self, min_confidence: float = 0.8) -> List[ReasoningTrace]:
        """
        get成功推理
        
        Args:
            min_confidence: 最小置信度
            
        Returns:
            成功推理列表
        """
        return [
            trace for trace in self.traces.values()
            if trace.confidence >= min_confidence
        ]
    
    def get_failed_reasonings(self, max_confidence: float = 0.5) -> List[ReasoningTrace]:
        """
        get失败推理
        
        Args:
            max_confidence: 最大置信度
            
        Returns:
            失败推理列表
        """
        return [
            trace for trace in self.traces.values()
            if trace.confidence <= max_confidence
        ]
    
    def analyze_reasoning_patterns(self) -> Dict:
        """
        分析推理模式
        
        Returns:
            分析结果
        """
        if not self.traces:
            return {}
        
        analysis = {
            'total_traces': len(self.traces),
            'average_confidence': sum(t.confidence for t in self.traces.values()) / len(self.traces),
            'average_steps': sum(len(t.steps) for t in self.traces.values()) / len(self.traces),
            'mode_distribution': {},
            'success_rate': 0.0
        }
        
        # 按模式统计
        mode_counts = {}
        success_counts = {}
        
        for trace in self.traces.values():
            mode = trace.reasoning_mode.value
            mode_counts[mode] = mode_counts.get(mode, 0) + 1
            
            if trace.confidence >= 0.8:
                success_counts[mode] = success_counts.get(mode, 0) + 1
        
        for mode, count in mode_counts.items():
            analysis['mode_distribution'][mode] = {
                'count': count,
                'percentage': count / len(self.traces) * 100,
                'success_rate': success_counts.get(mode, 0) / count * 100
            }
        
        # 总成功率
        successful = sum(1 for t in self.traces.values() if t.confidence >= 0.8)
        analysis['success_rate'] = successful / len(self.traces) * 100
        
        return analysis
    
    def export_traces(self, filepath: str, format: str = 'json'):
        """
        导出推理轨迹
        
        Args:
            filepath: 输出文件
            format: 文件格式 ('json')
        """
        if format == 'json':
            data = {
                'traces': [trace.to_dict() for trace in self.traces.values()],
                'patterns': [p.to_dict() for p in self.patterns.values()],
                'statistics': self.stats,
                'exported_at': datetime.now().isoformat()
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"推理轨迹已导出: {filepath}")
        else:
            raise ValueError(f"不支持的格式: {format}")
    
    def import_traces(self, filepath: str):
        """
        导入推理轨迹
        
        Args:
            filepath: 输入文件
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 导入轨迹
        for trace_data in data.get('traces', []):
            trace = ReasoningTrace.from_dict(trace_data)
            self.traces[trace.trace_id] = trace
            self.cache[trace.problem] = trace
        
        # 导入模式
        for pattern_data in data.get('patterns', []):
            pattern = ReasoningPattern(**pattern_data)
            self.patterns[pattern.pattern_id] = pattern
        
        # 更新统计
        imported_stats = data.get('statistics', {})
        self.stats.update(imported_stats)
        self.stats['total_traces'] = len(self.traces)
        self.stats['total_patterns'] = len(self.patterns)
        
        logger.info(f"推理轨迹已导入: {len(self.traces)}条轨迹, {len(self.patterns)}个模式")
    
    def clear_cache(self):
        """清除缓存"""
        self.cache.clear()
        logger.info("推理缓存已清除")
    
    def clear_old_traces(self, days: int = 30):
        """
        清除旧轨迹
        
        Args:
            days: 保留天数
        """
        cutoff = datetime.now() - timedelta(days=days)
        
        to_remove = [
            trace_id for trace_id, trace in self.traces.items()
            if trace.created_at < cutoff
        ]
        
        for trace_id in to_remove:
            del self.traces[trace_id]
            # 同时从缓存中删除
            problem_to_remove = [
                prob for prob, trace in self.cache.items()
                if trace.trace_id == trace_id
            ]
            for prob in problem_to_remove:
                del self.cache[prob]
        
        logger.info(f"清除{len(to_remove)}条旧轨迹")
    
    def get_statistics(self) -> Dict:
        """get统计信息"""
        stats = self.stats.copy()
        
        # 计算缓存命中率
        total_cache_accesses = stats['cache_hits'] + stats['cache_misses']
        if total_cache_accesses > 0:
            stats['cache_hit_rate'] = stats['cache_hits'] / total_cache_accesses * 100
        else:
            stats['cache_hit_rate'] = 0.0
        
        # 计算平均置信度
        if self.traces:
            stats['average_confidence'] = sum(t.confidence for t in self.traces.values()) / len(self.traces)
        else:
            stats['average_confidence'] = 0.0
        
        return stats
