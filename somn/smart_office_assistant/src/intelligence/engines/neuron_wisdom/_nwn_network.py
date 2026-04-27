"""神经元智慧网络 - 核心网络类"""

import math
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

from ._nwn_enums import NeuronState
from ._nwn_dataclasses import WisdomNeuron, Synapse, NetworkPathway
from ._nwn_schools import WISDOM_SCHOOLS

__all__ = [
    'activate_network',
    'get_activated_neurons',
    'get_network_insights',
]

class NeuronWisdomNetwork:
    """
    神经元智慧网络
    
    将43个智慧学派用神经网络的逻辑连接起来
    """
    
    # 默认激活阈值
    DEFAULT_ACTIVATION_THRESHOLD = 0.15
    
    # 激活模式参数
    ACTIVATION_PATTERNS = {
        "sharp": {"steepness": 5.0, "settle_time": 2},
        "gradual": {"steepness": 2.0, "settle_time": 4},
        "resonant": {"steepness": 3.0, "settle_time": 3},
        "slow": {"steepness": 1.0, "settle_time": 6}
    }
    
    def __init__(self, enable_learning: bool = True):
        """初始化神经元网络"""
        self.neurons: Dict[str, WisdomNeuron] = {}
        self.synapses: Dict[Tuple[str, str], Synapse] = {}
        self.pathways: Dict[str, NetworkPathway] = {}
        
        self.enable_learning = enable_learning
        
        # 初始化所有神经元
        self._initialize_neurons()
        
        # 建立突触连接
        self._initialize_synapses()
        
        # 初始化经典网络通路
        self._initialize_pathways()
        
        # 统计信息
        self.total_queries = 0
        self.activation_history: List[Dict] = []
    
    def _initialize_neurons(self):
        """初始化所有智慧神经元"""
        for school_id, school_info in WISDOM_SCHOOLS.items():
            neuron = WisdomNeuron(
                neuron_id=school_id,
                wisdom_school=school_info["name"],
                keywords=school_info["keywords"],
                problem_types=school_info["problems"],
                activation_threshold=self.DEFAULT_ACTIVATION_THRESHOLD
            )
            self.neurons[school_id] = neuron
    
    def _initialize_synapses(self):
        """初始化突触连接"""
        for school_id, school_info in WISDOM_SCHOOLS.items():
            # 促进性连接
            for enhanced_id in school_info.get("mutual_enhance", []):
                if enhanced_id in self.neurons:
                    synapse = Synapse(
                        source=school_id,
                        target=enhanced_id,
                        weight=0.6,
                        plasticity=0.1,
                        last_activation=datetime.now()
                    )
                    self.synapses[(school_id, enhanced_id)] = synapse
            
            # 抑制性连接
            for inhibited_id in school_info.get("mutual_inhibit", []):
                if inhibited_id in self.neurons:
                    synapse = Synapse(
                        source=school_id,
                        target=inhibited_id,
                        weight=-0.3,
                        plasticity=0.05,
                        last_activation=datetime.now()
                    )
                    self.synapses[(school_id, inhibited_id)] = synapse
            
            # 全局弱连接
            for other_id in self.neurons:
                if other_id != school_id:
                    if (school_id, other_id) not in self.synapses:
                        synapse = Synapse(
                            source=school_id,
                            target=other_id,
                            weight=0.1,
                            plasticity=0.01,
                            last_activation=datetime.now()
                        )
                        self.synapses[(school_id, other_id)] = synapse
    
    def _initialize_pathways(self):
        """初始化经典网络通路"""
        self.pathways["strategic"] = NetworkPathway(
            pathway_id="strategic",
            neurons=["SUFU", "MILITARY", "CIVILIZATION", "CIV_WAR_ECONOMY"],
            primary_type="战略决策"
        )
        self.pathways["ethical"] = NetworkPathway(
            pathway_id="ethical",
            neurons=["CONFUCIAN", "YANGMING", "LVSHI", "SUFU"],
            primary_type="伦理治理"
        )
        self.pathways["spiritual"] = NetworkPathway(
            pathway_id="spiritual",
            neurons=["BUDDHIST", "DAOIST", "METAPHYSICS", "YANGMING"],
            primary_type="心灵智慧"
        )
        self.pathways["growth"] = NetworkPathway(
            pathway_id="growth",
            neurons=["GROWTH", "SCI_FI", "BEHAVIOR", "SCIENCE"],
            primary_type="成长进化"
        )
    
    def _sigmoid_activation(self, x: float, steepness: float = 3.0) -> float:
        """Sigmoid激活函数"""
        return 1 / (1 + math.exp(-steepness * (x - 0.5)))
    
    def _calculate_query_similarity(self, query: str, neuron: WisdomNeuron) -> float:
        """计算查询与神经元的相似度"""
        query_lower = query.lower()
        score = 0.0
        
        # 关键词匹配
        for kw in neuron.keywords:
            if kw in query_lower:
                score += 2.0 * len(kw)
            elif any(c in query_lower for c in kw):
                score += 0.5
        
        # 问题类型匹配
        for pt in neuron.problem_types:
            if pt.lower() in query_lower.replace("_", ""):
                score += 1.5
        
        # 归一化
        max_possible = len(neuron.keywords) * 2.0 + len(neuron.problem_types) * 1.5
        similarity = min(score / max(1.0, max_possible * 0.3), 1.0)
        
        return similarity
    
    def activate_network(self, query: str, context: Optional[Dict] = None) -> Dict[str, float]:
        """激活网络"""
        # 第一步:计算初始激活
        initial_activations = {}
        for neuron_id, neuron in self.neurons.items():
            similarity = self._calculate_query_similarity(query, neuron)
            
            school_info = WISDOM_SCHOOLS.get(neuron_id, {})
            pattern = school_info.get("activation_pattern", "gradual")
            params = self.ACTIVATION_PATTERNS.get(pattern, {"steepness": 2.0})
            
            activation = self._sigmoid_activation(similarity, params["steepness"])
            
            neuron.accumulated_activation = activation
            if activation >= neuron.activation_threshold:
                neuron.state = NeuronState.ACTIVE
            else:
                neuron.state = NeuronState.DORMANT
            
            initial_activations[neuron_id] = activation
        
        # 第二步:信号传播
        propagated_activations = self._propagate_signals(initial_activations, max_iterations=3)
        
        # 第三步:整合结果
        final_activations = {}
        for neuron_id in self.neurons:
            base = initial_activations.get(neuron_id, 0.0)
            propagated = propagated_activations.get(neuron_id, 0.0)
            final_activations[neuron_id] = base * 0.6 + propagated * 0.4
        
        # 第四步:抑制-促进机制
        final_activations = self._apply_modulation(final_activations)
        
        return final_activations
    
    def _propagate_signals(self, initial_activations: Dict[str, float], 
                           max_iterations: int = 3) -> Dict[str, float]:
        """信号传播"""
        activations = initial_activations.copy()
        
        for iteration in range(max_iterations):
            new_activations = activations.copy()
            
            for (source, target), synapse in self.synapses.items():
                if source in activations:
                    signal = activations[source] * synapse.weight
                    
                    if target in new_activations:
                        time_decay = math.exp(-0.1 * iteration)
                        contribution = signal * time_decay
                        
                        if synapse.weight > 0:
                            new_activations[target] += contribution
                        else:
                            new_activations[target] = max(0, new_activations[target] + contribution)
            
            activations = new_activations
        
        # 归一化
        max_val = max(activations.values()) if activations else 1.0
        if max_val > 0:
            activations = {k: v / max_val for k, v in activations.items()}
        
        return activations
    
    def _apply_modulation(self, activations: Dict[str, float]) -> Dict[str, float]:
        """应用促进和抑制调制"""
        final = activations.copy()
        
        for neuron_id, neuron in self.neurons.items():
            school_info = WISDOM_SCHOOLS.get(neuron_id, {})
            
            # 促进
            for enhanced_id in school_info.get("mutual_enhance", []):
                if enhanced_id in activations and neuron_id in activations:
                    synergy = (activations.get(neuron_id, 0) * activations.get(enhanced_id, 0)) ** 0.5
                    final[enhanced_id] = min(1.0, final.get(enhanced_id, 0) + synergy * 0.2)
            
            # 抑制
            for inhibited_id in school_info.get("mutual_inhibit", []):
                if inhibited_id in activations:
                    inhibition = activations.get(neuron_id, 0) * 0.15
                    final[inhibited_id] = max(0, final.get(inhibited_id, 0) - inhibition)
        
        # 重新归一化
        max_val = max(final.values()) if final else 1.0
        if max_val > 0:
            final = {k: v / max_val for k, v in final.items()}
        
        return final
    
    def get_activated_neurons(self, activations: Dict[str, float], 
                              threshold: float = 0.3) -> List[Tuple[str, float]]:
        """获取激活的神经元列表"""
        activated = [(nid, act) for nid, act in activations.items() 
                     if act >= threshold]
        activated.sort(key=lambda x: x[1], reverse=True)
        return activated
    
    def get_network_insights(self, activations: Dict[str, float]) -> Dict[str, Any]:
        """获取网络洞察"""
        activated = self.get_activated_neurons(activations)
        
        insights = {
            "total_activated": len(activated),
            "top_neurons": [n[0] for n in activated[:5]],
            "pathway_match": None,
            "coverage": len(activated) / len(self.neurons),
            "network_state": "balanced" if len(activated) > 3 else "focused"
        }
        
        return insights
