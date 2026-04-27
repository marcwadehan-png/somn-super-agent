"""
__all__ = [
    'allocate_attention',
    'analyze_concept',
    'compute_entropy',
    'compute_mutual_info',
    'create_neuroscience_system',
    'create_reasoning_engine',
    'encode_knowledge',
    'get_associations',
    'get_attention_weights',
    'get_comprehensive_statistics',
    'get_retrieval_metrics',
    'get_top_attended',
    'index_for_retrieval',
    'learn_association',
    'propagate_activation',
    'reason',
    'retrieve_knowledge',
    'update_attention',
]

计算神经科学unified核心系统 v1.0
Computational Neuroscience Unified Core System v1.0

整合所有计算神经科学模块的unified接口

作者: Somn AI System
日期: 2026-04-02
"""

from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import numpy as np

# 导入各子系统
try:
    from ..neural_memory.neural_encoding_core import (
        NeuralCodingKnowledgeSystem,
        NeuralEncoder,
        TuningCurve,
        TuningCurveType,
        FiringRateModel,
        NeuralActivity
    )
    NEURAL_ENCODING_AVAILABLE = True
except ImportError:
    NEURAL_ENCODING_AVAILABLE = False

try:
    from ..neural_memory.hebbian_learning_engine import (
        HebbianLearningEngine,
        AttractorMemory,
        LearningRule,
        ConceptNode,
        Synapse
    )
    HEBBIAN_LEARNING_AVAILABLE = True
except ImportError:
    HEBBIAN_LEARNING_AVAILABLE = False

try:
    from ..neural_memory.firing_rate_attention import (
        FiringRateAttentionSystem,
        AttentionType,
        WinnerTakeAll,
        AttentionResource
    )
    ATTENTION_AVAILABLE = True
except ImportError:
    ATTENTION_AVAILABLE = False

try:
    from ..neural_memory.information_theory_retrieval import (
        InformationTheoryRetrievalSystem,
        KnowledgeDistribution,
        InformationMetrics,
        EntropyCalculator
    )
    INFO_THEORY_AVAILABLE = True
except ImportError:
    INFO_THEORY_AVAILABLE = False

@dataclass
class NeuroscienceConfig:
    """计算神经科学配置"""
    # 神经编码配置
    embedding_dim: int = 384
    base_firing_rate: float = 10.0
    
    # Hebbian学习配置
    learning_rate: float = 0.01
    default_learning_rule: str = "covariance"
    
    # 注意力配置
    attention_capacity: float = 100.0
    lateral_inhibition: float = 0.1
    
    # 信息论配置
    info_base: float = 2.0  # bits
    
    # 模块开关
    enable_neural_encoding: bool = True
    enable_hebbian_learning: bool = True
    enable_attention: bool = True
    enable_info_theory: bool = True

class ComputationalNeuroscienceCore:
    """
    计算神经科学unified核心
    
    整合<Theoretical Neuroscience>三大主题:
    1. 神经编码与解码 (Part I)
    2. 神经元与环路 (Part II)  
    3. 适应与学习 (Part III)
    
    提供unified的接口访问所有子系统
    """
    
    def __init__(self, config: Optional[NeuroscienceConfig] = None):
        self.config = config or NeuroscienceConfig()
        self.created_at = datetime.now()
        
        # init各子系统
        self._init_subsystems()
        
        # 统计
        self.total_operations = 0
        self.operation_history: List[Dict] = []
    
    def _init_subsystems(self):
        """init子系统"""
        # 神经编码系统
        if NEURAL_ENCODING_AVAILABLE and self.config.enable_neural_encoding:
            self.neural_coding = NeuralCodingKnowledgeSystem(
                embedding_dim=self.config.embedding_dim
            )
        
        # Hebbian学习系统
        if HEBBIAN_LEARNING_AVAILABLE and self.config.enable_hebbian_learning:
            from ..neural_memory.hebbian_learning_engine import LearningRule
            rule = LearningRule.COVARIANCE
            self.hebbian_engine = HebbianLearningEngine(
                learning_rate=self.config.learning_rate,
                default_rule=rule
            )
            self.attractor_memory = AttractorMemory(
                dimension=self.config.embedding_dim
            )
        
        # 注意力系统
        if ATTENTION_AVAILABLE and self.config.enable_attention:
            self.attention_system = FiringRateAttentionSystem(
                total_capacity=self.config.attention_capacity
            )
        
        # 信息论检索系统
        if INFO_THEORY_AVAILABLE and self.config.enable_info_theory:
            self.info_retrieval = InformationTheoryRetrievalSystem()
    
    # ==================== 知识编码接口 ====================
    
    def encode_knowledge(self, knowledge: Dict[str, Any],
                       stimuli: Optional[np.ndarray] = None) -> str:
        """
        编码知识为神经活动模式
        
        整合神经编码与Hebbian学习
        """
        self.total_operations += 1
        
        if NEURAL_ENCODING_AVAILABLE and hasattr(self, 'neural_coding'):
            # 神经编码
            activity_id = self.neural_coding.encode(knowledge, stimuli)
            
            # 同步到Hebbian系统
            if HEBBIAN_LEARNING_AVAILABLE and hasattr(self, 'hebbian_engine'):
                kid = knowledge.get('id', activity_id)
                if kid not in self.hebbian_engine.concepts:
                    self.hebbian_engine.add_concept(
                        kid, 
                        knowledge.get('content', kid)[:50]
                    )
            
            self._record_operation('encode_knowledge', {'knowledge_id': kid})
            return activity_id
        
        return knowledge.get('id', 'unknown')
    
    def retrieve_knowledge(self, query: Any, top_k: int = 10) -> List[Dict]:
        """
        检索知识
        
        使用信息论+神经编码+注意力synthesize排序
        """
        results = []
        
        if INFO_THEORY_AVAILABLE and hasattr(self, 'info_retrieval'):
            # 信息论检索
            results = self.info_retrieval.retrieve(
                str(query),
                {k: 0.5 for k in getattr(self.info_retrieval, 'knowledge', {}).keys()},
                top_k
            )
        
        if ATTENTION_AVAILABLE and hasattr(self, 'attention_system'):
            # 注意力加权
            weights = self.attention_system.get_attention_weights()
            for r in results:
                kid = r.get('knowledge_id')
                if kid in weights:
                    r['attention_weight'] = weights[kid]
                    r['score'] = r.get('score', 0.5) * (1 + weights[kid])
        
        # 按synthesize分数排序
        results.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        self._record_operation('retrieve_knowledge', 
                             {'query': str(query), 'top_k': top_k})
        return results[:top_k]
    
    # ==================== Hebbian学习接口 ====================
    
    def learn_association(self, concept_a: str, concept_b: str,
                        strength: float = 0.1,
                        rule: str = "covariance") -> Dict:
        """
        学习概念关联
        
        使用Hebbian学习规则
        """
        if not HEBBIAN_LEARNING_AVAILABLE or not hasattr(self, 'hebbian_engine'):
            return {}
        
        # 添加概念
        for kid in [concept_a, concept_b]:
            if kid not in self.hebbian_engine.concepts:
                self.hebbian_engine.add_concept(kid, kid)
        
        # 执行学习
        from ..neural_memory.hebbian_learning_engine import LearningRule
        rule_enum = getattr(LearningRule, rule.upper(), LearningRule.COVARIANCE)
        
        result = self.hebbian_engine.learn(
            concept_a, concept_b,
            pre_activity=0.8,
            post_activity=0.8,
            learning_rule=rule_enum
        )
        
        self._record_operation('learn_association', 
                             {'a': concept_a, 'b': concept_b, 'rule': rule})
        
        return {
            'source': result.source_id,
            'target': result.target_id,
            'delta_weight': result.delta_weight,
            'new_weight': result.new_weight
        }
    
    def get_associations(self, concept: str, top_k: int = 10) -> List[Dict]:
        """get概念关联"""
        if not HEBBIAN_LEARNING_AVAILABLE or not hasattr(self, 'hebbian_engine'):
            return []
        
        associations = self.hebbian_engine.get_associated_concepts(
            concept, top_k=top_k
        )
        
        return [{'concept': kid, 'weight': w} for kid, w in associations]
    
    def propagate_activation(self, source_concept: str, 
                           steps: int = 3) -> Dict[str, float]:
        """传播激活"""
        if not HEBBIAN_LEARNING_AVAILABLE or not hasattr(self, 'hebbian_engine'):
            return {}
        
        return self.hebbian_engine.propagate(source_concept, steps)
    
    # ==================== 注意力接口 ====================
    
    def allocate_attention(self, item_id: str, amount: float) -> bool:
        """分配注意力"""
        if not ATTENTION_AVAILABLE or not hasattr(self, 'attention_system'):
            return False
        
        # 添加项目
        if item_id not in self.attention_system.items:
            self.attention_system.add_item(item_id, item_id)
        
        return self.attention_system.allocate_attention(item_id, amount)
    
    def update_attention(self, inputs: Dict[str, float], dt: float = 1.0):
        """更新注意力"""
        if not ATTENTION_AVAILABLE or not hasattr(self, 'attention_system'):
            return
        
        self.attention_system.update(inputs, dt)
    
    def get_attention_weights(self) -> Dict[str, float]:
        """get注意力权重"""
        if not ATTENTION_AVAILABLE or not hasattr(self, 'attention_system'):
            return {}
        
        return self.attention_system.get_attention_weights()
    
    def get_top_attended(self, k: int = 5) -> List[tuple]:
        """get最被注意的项目"""
        if not ATTENTION_AVAILABLE or not hasattr(self, 'attention_system'):
            return []
        
        return self.attention_system.get_top_attended(k)
    
    # ==================== 信息论接口 ====================
    
    def index_for_retrieval(self, knowledge_id: str, content: str):
        """索引知识用于检索"""
        if not INFO_THEORY_AVAILABLE or not hasattr(self, 'info_retrieval'):
            return
        
        self.info_retrieval.index_knowledge(knowledge_id, content)
    
    def compute_entropy(self, probabilities: List[float]) -> float:
        """计算熵"""
        calc = EntropyCalculator()
        return calc.entropy(np.array(probabilities))
    
    def compute_mutual_info(self, p_x: List[float], 
                          p_y: List[float]) -> float:
        """计算互信息"""
        calc = EntropyCalculator()
        return calc.mutual_information(np.array(p_x), np.array(p_y), 
                                       np.outer(p_x, p_y).flatten())
    
    def get_retrieval_metrics(self) -> InformationMetrics:
        """get检索metrics"""
        if not INFO_THEORY_AVAILABLE or not hasattr(self, 'info_retrieval'):
            return InformationMetrics()
        
        return self.info_retrieval.get_statistics()
    
    # ==================== synthesize分析接口 ====================
    
    def analyze_concept(self, concept_id: str) -> Dict[str, Any]:
        """
        synthesize分析概念
        
        返回:
        - 神经编码状态
        - Hebbian关联
        - 注意力权重
        - 统计信息
        """
        analysis = {
            'concept_id': concept_id,
            'timestamp': datetime.now().isoformat()
        }
        
        # Hebbian分析
        if HEBBIAN_LEARNING_AVAILABLE and hasattr(self, 'hebbian_engine'):
            node = self.hebbian_engine.get_concept(concept_id)
            if node:
                analysis['hebbian'] = {
                    'activity': node.activity,
                    'base_activity': node.base_activity,
                    'associations': self.get_associations(concept_id, 5)
                }
        
        # 注意力分析
        if ATTENTION_AVAILABLE and hasattr(self, 'attention_system'):
            if concept_id in self.attention_system.items:
                item = self.attention_system.items[concept_id]
                analysis['attention'] = {
                    'current_rate': item.current_rate,
                    'normalized_rate': item.get_normalized_rate()
                }
        
        return analysis
    
    def get_comprehensive_statistics(self) -> Dict[str, Any]:
        """getsynthesize统计"""
        stats = {
            'timestamp': datetime.now().isoformat(),
            'total_operations': self.total_operations
        }
        
        if NEURAL_ENCODING_AVAILABLE and hasattr(self, 'neural_coding'):
            stats['neural_coding'] = self.neural_coding.get_statistics()
        
        if HEBBIAN_LEARNING_AVAILABLE and hasattr(self, 'hebbian_engine'):
            stats['hebbian_learning'] = self.hebbian_engine.get_network_statistics()
        
        if ATTENTION_AVAILABLE and hasattr(self, 'attention_system'):
            stats['attention'] = self.attention_system.get_statistics()
        
        if INFO_THEORY_AVAILABLE and hasattr(self, 'info_retrieval'):
            stats['info_theory'] = self.info_retrieval.get_statistics()
        
        return stats
    
    def _record_operation(self, op_type: str, params: Dict):
        """记录操作"""
        self.operation_history.append({
            'type': op_type,
            'params': params,
            'timestamp': datetime.now().isoformat()
        })
        
        # 限制历史长度
        if len(self.operation_history) > 1000:
            self.operation_history = self.operation_history[-1000:]

# ==================== 深度推理引擎集成 ====================

class NeuroscienceReasoningEngine:
    """
    计算神经科学推理引擎
    
    将计算神经科学原理融入深度推理:
    1. Hebbian关联推理 - 概念关联传播
    2. 注意力选择推理 - 资源聚焦
    3. 发放率激活推理 - 强度驱动
    4. 信息论优化推理 - 效率最大化
    """
    
    def __init__(self, core: Optional[ComputationalNeuroscienceCore] = None):
        self.core = core or ComputationalNeuroscienceCore()
    
    def reason(self, problem: str, 
              context: Optional[Dict] = None,
              mode: str = "integrated") -> Dict[str, Any]:
        """
        推理
        
        Args:
            problem: 问题描述
            context: 上下文
            mode: 推理模式 ('hebbian', 'attention', 'info_theory', 'integrated')
        """
        if mode == "hebbian":
            return self._hebbian_reason(problem, context)
        elif mode == "attention":
            return self._attention_reason(problem, context)
        elif mode == "info_theory":
            return self._info_theory_reason(problem, context)
        else:
            return self._integrated_reason(problem, context)
    
    def _hebbian_reason(self, problem: str, 
                       context: Optional[Dict]) -> Dict[str, Any]:
        """基于Hebbian学习的推理"""
        # 提取关键概念
        concepts = context.get('concepts', []) if context else []
        
        # 学习关联
        for i in range(len(concepts) - 1):
            self.core.learn_association(
                concepts[i], 
                concepts[i + 1],
                strength=0.1
            )
        
        # 传播激活
        if concepts:
            activations = self.core.propagate_activation(concepts[0])
            
            return {
                'mode': 'hebbian',
                'concepts': concepts,
                'activations': activations,
                'reasoning_type': 'associative_propagation'
            }
        
        return {'mode': 'hebbian', 'reasoning_type': 'associative_propagation'}
    
    def _attention_reason(self, problem: str,
                         context: Optional[Dict]) -> Dict[str, Any]:
        """基于注意力的推理"""
        # 分配注意力
        concepts = context.get('concepts', []) if context else []
        
        for i, concept in enumerate(concepts):
            # 优先级分配注意力
            priority = 1.0 - (i / max(1, len(concepts)))
            self.core.allocate_attention(concept, priority * 50)
        
        # 更新注意力
        inputs = {c: 0.8 for c in concepts}
        self.core.update_attention(inputs)
        
        # get加权结果
        weights = self.core.get_attention_weights()
        top = self.core.get_top_attended(3)
        
        return {
            'mode': 'attention',
            'weights': weights,
            'top_attended': top,
            'reasoning_type': 'selective_focus'
        }
    
    def _info_theory_reason(self, problem: str,
                           context: Optional[Dict]) -> Dict[str, Any]:
        """基于信息论的推理"""
        # 索引概念
        concepts = context.get('concepts', []) if context else []
        
        for concept in concepts:
            self.core.index_for_retrieval(concept, problem)
        
        # 检索
        results = self.core.retrieve_knowledge(problem, top_k=5)
        
        # 计算熵
        probs = [0.3, 0.25, 0.2, 0.15, 0.1][:len(concepts)]
        entropy = self.core.compute_entropy(probs)
        
        return {
            'mode': 'info_theory',
            'retrieval_results': results,
            'entropy': entropy,
            'reasoning_type': 'information_optimized'
        }
    
    def _integrated_reason(self, problem: str,
                          context: Optional[Dict]) -> Dict[str, Any]:
        """synthesize推理"""
        concepts = context.get('concepts', []) if context else []
        
        # Step 1: Hebbian关联学习
        hebbian_result = self._hebbian_reason(problem, context)
        
        # Step 2: 注意力选择
        attention_result = self._attention_reason(problem, context)
        
        # Step 3: 信息论优化
        info_result = self._info_theory_reason(problem, context)
        
        # synthesize分析
        top_attended = attention_result.get('top_attended', [])
        
        return {
            'mode': 'integrated',
            'problem': problem,
            'concepts': concepts,
            'hebbian': {
                'activations': hebbian_result.get('activations', {}),
                'associations': hebbian_result.get('associations', [])
            },
            'attention': {
                'top_attended': top_attended,
                'weights': attention_result.get('weights', {})
            },
            'information': {
                'entropy': info_result.get('entropy', 0),
                'relevant_concepts': [r['knowledge_id'] for r in info_result.get('retrieval_results', [])]
            },
            'reasoning_type': 'neuroscience_integrated',
            'reasoning_depth': 'multi_layer'
        }

# ==================== 便捷函数 ====================

def create_neuroscience_system(
    embedding_dim: int = 384,
    learning_rate: float = 0.01,
    attention_capacity: float = 100.0
) -> ComputationalNeuroscienceCore:
    """创建计算神经科学系统"""
    config = NeuroscienceConfig(
        embedding_dim=embedding_dim,
        learning_rate=learning_rate,
        attention_capacity=attention_capacity
    )
    return ComputationalNeuroscienceCore(config)

def create_reasoning_engine(
    core: Optional[ComputationalNeuroscienceCore] = None
) -> NeuroscienceReasoningEngine:
    """创建神经科学推理引擎"""
    return NeuroscienceReasoningEngine(core)

# ==================== 示例使用 ====================

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
