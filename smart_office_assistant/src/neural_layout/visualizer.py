"""
__all__ = [
    'export_to_json',
    'generate_activation_heatmap_html',
    'generate_html_visualization',
    'generate_mermaid_graph',
    'generate_realtime_topology_html',
    'generate_signal_flow_report',
    'generate_topology_report',
    'visualize_network',
]

神经网络可视化器

可视化神经网络布局和信号流动，支持：
- Mermaid 拓扑图
- HTML 静态可视化
- 实时拓扑 SVG 交互图（节点激活热力）
- 激活热力图（信号强度矩阵）
"""

from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
import json

from .signal import Signal, SignalType
from .synapse_connection import SynapseConnection, ConnectionType
from .neuron_node import NeuronNode, NeuronType, NeuronState
from .neural_network import NeuralNetwork

class NetworkVisualizer:
    """
    网络可视化器
    
    生成神经网络的可视化表示
    """
    
    def __init__(self, network: NeuralNetwork):
        self.network = network
    
    def generate_mermaid_graph(self) -> str:
        """生成Mermaid图表"""
        lines = ["graph TD"]
        
        # 定义节点样式
        type_styles = {
            NeuronType.INPUT: "((%s))",
            NeuronType.OUTPUT: "([%s])",
            NeuronType.WISDOM: "{%s}",
            NeuronType.MEMORY: "[%s]",
            NeuronType.HIDDEN: "(%s)",
            NeuronType.CONTROL: "[[%s]]",
            NeuronType.FEEDBACK: ">%s]",
        }
        
        # 添加节点定义
        for neuron_id, neuron in self.network.neurons.items():
            style = type_styles.get(neuron.neuron_type, "(%s)")
            node_def = f"    {neuron_id}{style % neuron.name}"
            lines.append(node_def)
        
        # 添加连接
        for synapse in self.network.synapses.values():
            source = synapse.source_id
            target = synapse.target_id
            weight = synapse.weight
            
            if synapse.connection_type == ConnectionType.INHIBITORY:
                arrow = "-.->"
            elif synapse.connection_type == ConnectionType.RECURRENT:
                arrow = "==>"
            else:
                arrow = "-->"
            
            line = f"    {source} {arrow}|{weight:.2f}| {target}"
            lines.append(line)
        
        # 添加样式类
        lines.append("")
        lines.append("    classDef input fill:#e1f5fe")
        lines.append("    classDef output fill:#f3e5f5")
        lines.append("    classDef wisdom fill:#fff3e0")
        lines.append("    classDef memory fill:#e8f5e9")
        lines.append("    classDef hidden fill:#f5f5f5")
        
        # 应用样式
        for neuron_id, neuron in self.network.neurons.items():
            if neuron.neuron_type == NeuronType.INPUT:
                lines.append(f"    class {neuron_id} input")
            elif neuron.neuron_type == NeuronType.OUTPUT:
                lines.append(f"    class {neuron_id} output")
            elif neuron.neuron_type == NeuronType.WISDOM:
                lines.append(f"    class {neuron_id} wisdom")
            elif neuron.neuron_type == NeuronType.MEMORY:
                lines.append(f"    class {neuron_id} memory")
            elif neuron.neuron_type == NeuronType.HIDDEN:
                lines.append(f"    class {neuron_id} hidden")
        
        return "\n".join(lines)
    
    def generate_topology_report(self) -> Dict:
        """生成拓扑报告"""
        topology = self.network.get_network_topology()
        
        # 计算网络指标
        neuron_count = len(self.network.neurons)
        synapse_count = len(self.network.synapses)
        
        # 计算密度
        max_possible = neuron_count * (neuron_count - 1) if neuron_count > 1 else 1
        density = synapse_count / max_possible if max_possible > 0 else 0
        
        # 计算平均度数
        total_degree = sum(
            len(n.incoming_synapses) + len(n.outgoing_synapses)
            for n in self.network.neurons.values()
        )
        avg_degree = total_degree / neuron_count if neuron_count > 0 else 0
        
        # 找出中心节点
        centrality = {}
        for neuron_id in self.network.neurons:
            in_degree = len(self.network.neurons[neuron_id].incoming_synapses)
            out_degree = len(self.network.neurons[neuron_id].outgoing_synapses)
            centrality[neuron_id] = in_degree + out_degree
        
        top_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "topology": topology,
            "metrics": {
                "neuron_count": neuron_count,
                "synapse_count": synapse_count,
                "network_density": round(density, 4),
                "average_degree": round(avg_degree, 2),
                "top_central_nodes": [
                    {"node_id": nid, "degree": deg, "name": self.network.neurons[nid].name}
                    for nid, deg in top_nodes
                ]
            },
            "layer_structure": self.network.get_layered_structure(),
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_signal_flow_report(self, pathway_log: List[Dict]) -> Dict:
        """生成信号流动报告"""
        if not pathway_log:
            return {"error": "No pathway data"}
        
        # 分析信号流动
        depth_analysis = {}
        for entry in pathway_log:
            depth = entry.get("depth", 0)
            if depth not in depth_analysis:
                depth_analysis[depth] = []
            depth_analysis[depth].append(entry)
        
        # 统计活跃节点
        active_nodes = set()
        for entry in pathway_log:
            active_nodes.add(entry.get("source", ""))
            active_nodes.update(entry.get("targets", []))
        
        return {
            "total_steps": len(pathway_log),
            "max_depth": max(depth_analysis.keys()) if depth_analysis else 0,
            "active_nodes": list(active_nodes),
            "active_node_count": len(active_nodes),
            "depth_distribution": {
                depth: len(entries) for depth, entries in depth_analysis.items()
            },
            "pathway_details": pathway_log
        }
    
    def export_to_json(self, filepath: str):
        """导出网络数据到JSON"""
        data = {
            "network_id": self.network.network_id,
            "created_at": self.network.created_at.isoformat(),
            "neurons": [
                neuron.to_dict() for neuron in self.network.neurons.values()
            ],
            "synapses": [
                synapse.to_dict() for synapse in self.network.synapses.values()
            ],
            "topology": self.network.get_network_topology(),
            "stats": self.network.network_stats
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def generate_realtime_topology_html(self, phase_status: Optional[Dict] = None) -> str:
        """生成实时交互拓扑图（SVG + 激活热力着色）

        Args:
            phase_status: Phase 系统状态字典（可选，用于叠加显示）

        Returns:
            完整 HTML 字符串，包含 SVG 拓扑和交互脚本
        """
        topology = self.network.get_network_topology()
        neurons = self.network.neurons
        synapses = self.network.synapses

        # 神经元类型 -> 颜色映射
        type_color_map = {
            NeuronType.INPUT: "#4FC3F7",
            NeuronType.OUTPUT: "#CE93D8",
            NeuronType.WISDOM: "#FFB74D",
            NeuronType.MEMORY: "#81C784",
            NeuronType.HIDDEN: "#B0BEC5",
            NeuronType.CONTROL: "#E57373",
            NeuronType.FEEDBACK: "#FFF176",
        }

        # 激活级别映射（根据神经元状态）
        def _activation_level(neuron: NeuronNode) -> float:
            """0.0 (idle) -> 1.0 (highly active)"""
            if neuron.state == NeuronState.EXCITED:
                return 1.0
            elif neuron.state == NeuronState.ACTIVE:
                return 0.9
            elif neuron.state == NeuronState.PLASTIC:
                return 0.7
            elif neuron.state == NeuronState.INHIBITED:
                return 0.2
            elif neuron.state == NeuronState.REFRACTORY:
                return 0.1
            return 0.4

        # 环形布局坐标
        import math
        cx, cy = 500, 400
        radius = 280
        n_count = len(neurons)
        positions: Dict[str, Tuple[float, float]] = {}
        for i, nid in enumerate(neurons):
            angle = 2 * math.pi * i / max(n_count, 1) - math.pi / 2
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            positions[nid] = (x, y)

        # 构建 SVG
        svg_parts = []
        # 连接线
        for sid, syn in synapses.items():
            src_pos = positions.get(syn.source_id)
            tgt_pos = positions.get(syn.target_id)
            if not src_pos or not tgt_pos:
                continue
            weight = syn.weight
            stroke_width = max(1, weight * 4)
            opacity = 0.3 + weight * 0.5
            dash = "stroke-dasharray='6 3'" if syn.connection_type == ConnectionType.INHIBITORY else ""
            color = "#e74c3c" if syn.connection_type == ConnectionType.INHIBITORY else "#3498db"
            if syn.connection_type == ConnectionType.RECURRENT:
                color = "#f39c12"
            svg_parts.append(
                f'<line x1="{src_pos[0]:.1f}" y1="{src_pos[1]:.1f}" '
                f'x2="{tgt_pos[0]:.1f}" y2="{tgt_pos[1]:.1f}" '
                f'stroke="{color}" stroke-width="{stroke_width:.1f}" '
                f'opacity="{opacity:.2f}" {dash}/>'
            )

        # 节点
        node_labels = []
        for nid, neuron in neurons.items():
            pos = positions.get(nid, (cx, cy))
            base_color = type_color_map.get(neuron.neuron_type, "#B0BEC5")
            activation = _activation_level(neuron)
            r = 16 + activation * 14  # 16~30
            # 光晕效果
            glow_opacity = activation * 0.4
            svg_parts.append(
                f'<circle cx="{pos[0]:.1f}" cy="{pos[1]:.1f}" r="{r + 8}" '
                f'fill="{base_color}" opacity="{glow_opacity:.2f}"/>'
            )
            svg_parts.append(
                f'<circle cx="{pos[0]:.1f}" cy="{pos[1]:.1f}" r="{r:.1f}" '
                f'fill="{base_color}" stroke="#fff" stroke-width="2" opacity="0.9">'
                f'<title>{neuron.name} ({neuron.neuron_type.value})\n'
                f'State: {neuron.state.value}\n'
                f'Activation: {activation:.0%}</title></circle>'
            )
            # 标签
            svg_parts.append(
                f'<text x="{pos[0]:.1f}" y="{pos[1] + r + 14:.1f}" '
                f'text-anchor="middle" fill="#555" font-size="10">{neuron.name}</text>'
            )

        svg_body = "\n        ".join(svg_parts)

        # Phase 状态面板
        phase_panel_html = ""
        if phase_status:
            items = []
            for key, val in phase_status.items():
                if isinstance(val, dict):
                    status = val.get("status", val.get("running", ""))
                    items.append(f"<b>{key}</b>: {status}")
                else:
                    items.append(f"<b>{key}</b>: {val}")
            phase_panel_html = f"""
        <div class="phase-panel">
            <h3>Phase 系统状态</h3>
            {"<br>".join(items)}
        </div>"""

        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Somn 实时拓扑 — {datetime.now().strftime('%Y-%m-%d %H:%M')}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; background: #1a1a2e; color: #eee; }}
        .header {{ text-align: center; padding: 16px; background: #16213e; border-bottom: 2px solid #0f3460; }}
        .header h1 {{ margin: 0; font-size: 20px; }}
        .header .timestamp {{ color: #888; font-size: 12px; }}
        .container {{ display: flex; flex-wrap: wrap; }}
        .svg-wrap {{ flex: 1; min-width: 600px; display: flex; justify-content: center; align-items: center; padding: 20px; }}
        .svg-wrap svg {{ background: #0f3460; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }}
        .side-panel {{ width: 280px; padding: 16px; }}
        .legend {{ background: #16213e; border-radius: 8px; padding: 12px; margin-bottom: 12px; }}
        .legend h3 {{ margin: 0 0 8px; font-size: 13px; }}
        .legend-item {{ display: flex; align-items: center; margin: 4px 0; font-size: 12px; }}
        .legend-dot {{ width: 12px; height: 12px; border-radius: 50%; margin-right: 8px; }}
        .phase-panel {{ background: #16213e; border-radius: 8px; padding: 12px; font-size: 12px; line-height: 1.8; }}
        .phase-panel h3 {{ margin: 0 0 8px; font-size: 13px; }}
        .stats-bar {{ display: flex; gap: 12px; padding: 12px 20px; background: #16213e; border-top: 1px solid #0f3460; }}
        .stat {{ text-align: center; }}
        .stat-val {{ font-size: 22px; font-weight: bold; color: #4FC3F7; }}
        .stat-lbl {{ font-size: 11px; color: #888; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 Somn 神经网络实时拓扑</h1>
        <div class="timestamp">更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
    </div>
    <div class="container">
        <div class="svg-wrap">
            <svg width="1000" height="800" viewBox="0 0 1000 800">
                {svg_body}
            </svg>
        </div>
        <div class="side-panel">
            <div class="legend">
                <h3>节点类型图例</h3>
                <div class="legend-item"><div class="legend-dot" style="background:#4FC3F7"></div>输入层 Input</div>
                <div class="legend-item"><div class="legend-dot" style="background:#FFB74D"></div>智慧层 Wisdom</div>
                <div class="legend-item"><div class="legend-dot" style="background:#81C784"></div>记忆层 Memory</div>
                <div class="legend-item"><div class="legend-dot" style="background:#E57373"></div>控制层 Control</div>
                <div class="legend-item"><div class="legend-dot" style="background:#B0BEC5"></div>隐藏层 Hidden</div>
                <div class="legend-item"><div class="legend-dot" style="background:#CE93D8"></div>输出层 Output</div>
                <hr style="border-color:#333;margin:8px 0">
                <div class="legend-item"><div style="width:20px;height:3px;background:#3498db;margin-right:8px"></div>兴奋连接</div>
                <div class="legend-item"><div style="width:20px;height:3px;background:#e74c3c;margin-right:8px"></div>抑制连接</div>
                <div class="legend-item"><div style="width:20px;height:3px;background:#f39c12;margin-right:8px"></div>循环连接</div>
            </div>
            {phase_panel_html}
        </div>
    </div>
    <div class="stats-bar">
        <div class="stat"><div class="stat-val">{topology['neuron_count']}</div><div class="stat-lbl">神经元</div></div>
        <div class="stat"><div class="stat-val">{topology['synapse_count']}</div><div class="stat-lbl">突触</div></div>
        <div class="stat"><div class="stat-val">{len(topology.get('neurons_by_type', {}))}</div><div class="stat-lbl">类型</div></div>
    </div>
</body>
</html>"""
        return html

    def generate_activation_heatmap_html(self) -> str:
        """生成激活热力图 — 信号强度矩阵

        展示神经元之间的信号强度矩阵，用颜色深浅表示连接权重。

        Returns:
            完整 HTML 字符串
        """
        neurons = self.network.neurons
        synapses = self.network.synapses
        neuron_ids = list(neurons.keys())

        # 构建权重矩阵
        matrix: Dict[str, Dict[str, float]] = {}
        for nid in neuron_ids:
            matrix[nid] = {}
        for syn in synapses.values():
            if syn.source_id in matrix and syn.target_id in matrix[syn.source_id]:
                # 取最大权重
                matrix[syn.source_id][syn.target_id] = max(
                    matrix[syn.source_id].get(syn.target_id, 0), syn.weight
                )
            else:
                matrix[syn.source_id][syn.target_id] = syn.weight

        n = len(neuron_ids)
        # 限制展示数量（太多会导致矩阵过大）
        display_ids = neuron_ids[:40]
        dn = len(display_ids)

        # 生成矩阵单元格
        cells_html = []
        for i, src in enumerate(display_ids):
            for j, tgt in enumerate(display_ids):
                w = matrix.get(src, {}).get(tgt, 0.0)
                if w > 0:
                    # 绿(低) -> 黄(中) -> 红(高)
                    if w < 0.7:
                        r_c = int(255 * (w / 0.7))
                        g_c = 200
                        color = f"rgb({r_c},{g_c},80)"
                    else:
                        r_c = 255
                        g_c = int(200 * (1 - (w - 0.7) / 0.3))
                        color = f"rgb({r_c},{max(g_c,0)},60)"
                    title = f"{neurons[src].name} → {neurons[tgt].name}: {w:.2f}"
                    cells_html.append(
                        f'<td style="background:{color};min-width:14px;max-width:14px;height:14px;" '
                        f'title="{title}"></td>'
                    )
                else:
                    cells_html.append('<td style="background:#1a1a2e;min-width:14px;max-width:14px;height:14px;"></td>')

        # 行头和列头
        th_cells = "".join(
            f'<th style="font-size:9px;padding:2px;writing-mode:vertical-lr;transform:rotate(180deg);'
            f'max-width:14px;height:60px;overflow:hidden;">{neurons[nid].name[:6]}</th>'
            for nid in display_ids
        )
        rows_html = []
        for i, src in enumerate(display_ids):
            row_cells = "".join(cells_html[i * dn:(i + 1) * dn])
            rows_html.append(
                f'<tr><th style="font-size:9px;padding:2px;white-space:nowrap;">'
                f'{neurons[src].name[:10]}</th>{row_cells}</tr>'
            )

        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Somn 激活热力图 — {datetime.now().strftime('%Y-%m-%d %H:%M')}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; background: #1a1a2e; color: #eee; }}
        .header {{ text-align: center; padding: 16px; background: #16213e; border-bottom: 2px solid #0f3460; }}
        .header h1 {{ margin: 0; font-size: 20px; }}
        .chart-area {{ display: flex; justify-content: center; padding: 30px; overflow: auto; }}
        table {{ border-collapse: collapse; }}
        td, th {{ border: 1px solid #0f3460; }}
        .color-bar {{ display: flex; align-items: center; justify-content: center; gap: 8px; padding: 12px; font-size: 12px; }}
        .gradient {{ width: 200px; height: 14px; border-radius: 4px; background: linear-gradient(to right, #1a1a2e, #c0c850, #ff3c3c); }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔥 激活热力图 — 信号强度矩阵</h1>
        <div>神经元 × 神经元 连接权重分布 ({dn}×{dn})</div>
    </div>
    <div class="color-bar">
        <span>0.0 无连接</span>
        <div class="gradient"></div>
        <span>1.0 强连接</span>
    </div>
    <div class="chart-area">
        <table>
            <tr><th></th>{th_cells}</tr>
            {"".join(rows_html)}
        </table>
    </div>
</body>
</html>"""
        return html

    def generate_html_visualization(self) -> str:
        """生成HTML可视化"""
        topology = self.network.get_network_topology()
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Somn Neural Network Layout</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
        h1 {{ color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
        .stat-card {{ background: #f9f9f9; padding: 15px; border-radius: 6px; border-left: 4px solid #4CAF50; }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: #4CAF50; }}
        .stat-label {{ color: #666; font-size: 14px; }}
        .neuron-list {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 10px; }}
        .neuron-card {{ background: #fff; border: 1px solid #ddd; padding: 10px; border-radius: 4px; }}
        .neuron-type {{ font-size: 12px; color: #999; text-transform: uppercase; }}
        .neuron-name {{ font-weight: bold; color: #333; }}
        .connection-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        .connection-table th, .connection-table td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
        .connection-table th {{ background: #f5f5f5; font-weight: bold; }}
        .mermaid {{ background: #f9f9f9; padding: 20px; border-radius: 6px; overflow-x: auto; }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
</head>
<body>
    <div class="container">
        <h1>🧠 Somn 神经网络布局可视化</h1>
        
        <h2>网络统计</h2>
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{topology['neuron_count']}</div>
                <div class="stat-label">神经元总数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{topology['synapse_count']}</div>
                <div class="stat-label">突触连接数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(topology['neurons_by_type'])}</div>
                <div class="stat-label">神经元类型</div>
            </div>
        </div>
        
        <h2>神经元类型分布</h2>
        <div class="stats">
"""
        
        for neuron_type, count in topology['neurons_by_type'].items():
            html += f"""
            <div class="stat-card">
                <div class="stat-value">{count}</div>
                <div class="stat-label">{neuron_type}</div>
            </div>
"""
        
        html += """
        </div>
        
        <h2>网络拓扑图</h2>
        <div class="mermaid">
"""
        html += self.generate_mermaid_graph()
        html += """
        </div>
    </div>
    <script>
        mermaid.initialize({ startOnLoad: true });
    </script>
</body>
</html>
"""
        return html

def visualize_network(network: NeuralNetwork, output_path: Optional[str] = None) -> str:
    """
    可视化网络
    
    Args:
        network: 神经网络
        output_path: 输出文件路径
        
    Returns:
        HTML字符串
    """
    visualizer = NetworkVisualizer(network)
    html = visualizer.generate_html_visualization()
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
    
    return html
