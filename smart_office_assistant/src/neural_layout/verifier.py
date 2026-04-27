"""
__all__ = [
    'bfs',
    'detect_cycles',
    'detect_isolation',
    'detect_orphans',
    'dfs',
    'verify_all',
    'verify_connectivity',
    'verify_network',
    'verify_pathways',
    'verify_structure',
]

神经网络验证器

验证神经网络布局的完整性和连通性
"""

from typing import Any, Dict, List, Optional, Set, Tuple
from collections import deque

from .signal import Signal, SignalType
from .synapse_connection import SynapseConnection, ConnectionType
from .neuron_node import NeuronNode, NeuronType, NeuronState
from .neural_network import NeuralNetwork

class NetworkVerifier:
    """
    网络验证器
    
    验证神经网络的：
    1. 结构完整性
    2. 连通性
    3. 通路可达性
    4. 循环检测
    """
    
    def __init__(self, network: NeuralNetwork):
        self.network = network
        self.issues: List[Dict] = []
    
    def verify_all(self) -> Dict:
        """执行所有验证"""
        self.issues = []
        
        results = {
            "structure": self.verify_structure(),
            "connectivity": self.verify_connectivity(),
            "pathways": self.verify_pathways(),
            "cycles": self.detect_cycles(),
            "isolation": self.detect_isolation(),
            "orphans": self.detect_orphans(),
        }
        
        # 计算总体状态
        all_passed = all(r.get("passed", False) for r in results.values())
        
        return {
            "overall_status": "PASSED" if all_passed else "FAILED",
            "total_issues": len(self.issues),
            "issues": self.issues,
            "details": results,
            "summary": self._generate_summary(results)
        }
    
    def verify_structure(self) -> Dict:
        """验证结构完整性"""
        issues = []
        
        # 检查是否有神经元
        if not self.network.neurons:
            issues.append({
                "type": "ERROR",
                "message": "网络中没有神经元"
            })
        
        # 检查是否有连接
        if not self.network.synapses:
            issues.append({
                "type": "WARNING",
                "message": "网络中没有突触连接"
            })
        
        # 检查神经元类型分布
        for neuron_type, neuron_ids in self.network.neurons_by_type.items():
            if neuron_type == NeuronType.INPUT and not neuron_ids:
                issues.append({
                    "type": "WARNING",
                    "message": "缺少输入神经元"
                })
            if neuron_type == NeuronType.OUTPUT and not neuron_ids:
                issues.append({
                    "type": "WARNING",
                    "message": "缺少输出神经元"
                })
        
        self.issues.extend(issues)
        
        return {
            "passed": len([i for i in issues if i["type"] == "ERROR"]) == 0,
            "issue_count": len(issues),
            "issues": issues
        }
    
    def verify_connectivity(self) -> Dict:
        """验证连通性"""
        issues = []
        
        # 检查每个神经元的连接
        for neuron_id, neuron in self.network.neurons.items():
            in_count = len(neuron.incoming_synapses)
            out_count = len(neuron.outgoing_synapses)
            
            # 输入神经元应该有出连接
            if neuron.neuron_type == NeuronType.INPUT and out_count == 0:
                issues.append({
                    "type": "WARNING",
                    "message": f"输入神经元 {neuron_id} 没有出连接"
                })
            
            # 输出神经元应该有入连接
            if neuron.neuron_type == NeuronType.OUTPUT and in_count == 0:
                issues.append({
                    "type": "WARNING",
                    "message": f"输出神经元 {neuron_id} 没有入连接"
                })
            
            # 隐藏神经元应该既有入连接又有出连接
            if neuron.neuron_type == NeuronType.HIDDEN:
                if in_count == 0:
                    issues.append({
                        "type": "WARNING",
                        "message": f"隐藏神经元 {neuron_id} 没有入连接"
                    })
                if out_count == 0:
                    issues.append({
                        "type": "WARNING",
                        "message": f"隐藏神经元 {neuron_id} 没有出连接"
                    })
        
        self.issues.extend(issues)
        
        return {
            "passed": len([i for i in issues if i["type"] == "ERROR"]) == 0,
            "issue_count": len(issues),
            "issues": issues
        }
    
    def verify_pathways(self) -> Dict:
        """验证通路可达性"""
        issues = []
        
        # 获取输入和输出神经元
        input_neurons = self.network.neurons_by_type.get(NeuronType.INPUT, set())
        output_neurons = self.network.neurons_by_type.get(NeuronType.OUTPUT, set())
        
        if not input_neurons or not output_neurons:
            return {
                "passed": False,
                "issue_count": 1,
                "issues": [{"type": "ERROR", "message": "缺少输入或输出神经元"}]
            }
        
        # 检查从输入到输出的可达性
        unreachable_outputs = set()
        for output_id in output_neurons:
            reachable = False
            for input_id in input_neurons:
                path = self.network.find_path(input_id, output_id)
                if path:
                    reachable = True
                    break
            if not reachable:
                unreachable_outputs.add(output_id)
        
        if unreachable_outputs:
            issues.append({
                "type": "WARNING",
                "message": f"以下输出神经元不可达: {unreachable_outputs}"
            })
        
        self.issues.extend(issues)
        
        return {
            "passed": len([i for i in issues if i["type"] == "ERROR"]) == 0,
            "issue_count": len(issues),
            "issues": issues,
            "unreachable_outputs": list(unreachable_outputs)
        }
    
    def detect_cycles(self) -> Dict:
        """检测循环"""
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node_id: str, path: List[str]):
            visited.add(node_id)
            rec_stack.add(node_id)
            path.append(node_id)
            
            neuron = self.network.neurons.get(node_id)
            if neuron:
                for synapse in neuron.outgoing_synapses.values():
                    neighbor = synapse.target_id
                    if neighbor not in visited:
                        dfs(neighbor, path)
                    elif neighbor in rec_stack:
                        # 发现循环
                        cycle_start = path.index(neighbor)
                        cycle = path[cycle_start:] + [neighbor]
                        cycles.append(cycle)
            
            path.pop()
            rec_stack.remove(node_id)
        
        for neuron_id in self.network.neurons:
            if neuron_id not in visited:
                dfs(neuron_id, [])
        
        # 循环不一定是问题，但我们需要知道它们
        issues = []
        if cycles:
            issues.append({
                "type": "INFO",
                "message": f"检测到 {len(cycles)} 个循环"
            })
        
        return {
            "passed": True,  # 循环不一定是错误
            "cycle_count": len(cycles),
            "cycles": cycles,
            "issues": issues
        }
    
    def detect_isolation(self) -> Dict:
        """检测孤立节点组"""
        if not self.network.neurons:
            return {"passed": True, "groups": [], "issues": []}
        
        # 使用并查集或BFS找出连通分量
        visited = set()
        groups = []
        
        def bfs(start_id: str) -> Set[str]:
            group = set()
            queue = deque([start_id])
            
            while queue:
                node_id = queue.popleft()
                if node_id in group:
                    continue
                group.add(node_id)
                
                neuron = self.network.neurons.get(node_id)
                if neuron:
                    for synapse in neuron.outgoing_synapses.values():
                        if synapse.target_id not in group:
                            queue.append(synapse.target_id)
                    for synapse in neuron.incoming_synapses.values():
                        if synapse.source_id not in group:
                            queue.append(synapse.source_id)
            
            return group
        
        for neuron_id in self.network.neurons:
            if neuron_id not in visited:
                group = bfs(neuron_id)
                groups.append(group)
                visited.update(group)
        
        issues = []
        if len(groups) > 1:
            issues.append({
                "type": "WARNING",
                "message": f"网络分为 {len(groups)} 个不连通的组"
            })
        
        return {
            "passed": len(groups) == 1,
            "group_count": len(groups),
            "groups": [list(g) for g in groups],
            "issues": issues
        }
    
    def detect_orphans(self) -> Dict:
        """检测孤立节点（没有任何连接的节点）"""
        orphans = []
        
        for neuron_id, neuron in self.network.neurons.items():
            if not neuron.incoming_synapses and not neuron.outgoing_synapses:
                orphans.append(neuron_id)
        
        issues = []
        if orphans:
            issues.append({
                "type": "WARNING",
                "message": f"检测到 {len(orphans)} 个孤立节点: {orphans}"
            })
        
        return {
            "passed": len(orphans) == 0,
            "orphan_count": len(orphans),
            "orphans": orphans,
            "issues": issues
        }
    
    def _generate_summary(self, results: Dict) -> str:
        """生成验证摘要"""
        total_issues = sum(r.get("issue_count", 0) for r in results.values())
        error_count = sum(
            len([i for i in r.get("issues", []) if i.get("type") == "ERROR"])
            for r in results.values()
        )
        warning_count = sum(
            len([i for i in r.get("issues", []) if i.get("type") == "WARNING"])
            for r in results.values()
        )
        
        if error_count == 0 and warning_count == 0:
            return "✅ 网络验证通过，未发现明显问题"
        elif error_count == 0:
            return f"⚠️ 网络验证通过，但有 {warning_count} 个警告"
        else:
            return f"❌ 网络验证失败，发现 {error_count} 个错误和 {warning_count} 个警告"

def verify_network(network: NeuralNetwork) -> Dict:
    """
    验证网络
    
    Args:
        network: 神经网络
        
    Returns:
        验证结果
    """
    verifier = NetworkVerifier(network)
    return verifier.verify_all()
