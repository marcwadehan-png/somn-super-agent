#!/usr/bin/env python3
"""
神经网络可视化组件 - ASCII艺术版
"""

import math
import random
from typing import List, Tuple, Dict


class NeuralVisualizer:
    """神经网络可视化器"""

    def __init__(self, width: int = 60, height: int = 20):
        self.width = width
        self.height = height
        self.grid = [[" " for _ in range(width)] for _ in range(height)]

    def clear(self):
        self.grid = [[" " for _ in range(self.width)] for _ in range(self.height)]

    def _set(self, x: int, y: int, char: str):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = char

    def _line(self, x1: int, y1: int, x2: int, y2: int, char: str = "●"):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            self._set(x1, y1, char)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def draw_cluster(self, cx: int, cy: int, radius: int, name: str, color: str = "●"):
        for angle in range(0, 360, 45):
            x = int(cx + radius * math.cos(math.radians(angle)))
            y = int(cy + radius * math.sin(math.radians(angle)))
            self._set(x, y, color)
        self._set(cx, cy, "◆")
        for i, c in enumerate(name):
            self._set(cx - len(name)//2 + i, cy + radius + 1, c)

    def draw_synapse(self, x1: int, y1: int, x2: int, y2: int, weight: float = 1.0):
        char = "─"
        self._line(x1, y1, x2, y2, char)

    def render(self) -> str:
        return "\n".join("".join(row) for row in self.grid)


def create_network_diagram(neurons: int = 57, synapses: int = 74, clusters: int = 4, phase: int = 3) -> str:
    """创建神经网络图"""
    viz = NeuralVisualizer(70, 22)

    # 标题
    title = "SOMN NEURAL NETWORK"
    for i, c in enumerate(title):
        viz._set(35 - len(title)//2 + i, 1, c)

    # Phase进度条
    phase_str = f"Phase {phase}/5: "
    for i in range(1, 6):
        phase_str += "█" if i <= phase else "░"
    for i, c in enumerate(phase_str):
        viz._set(35 - len(phase_str)//2 + i, 3, c)

    # 绘制集群
    positions = [(15, 11), (55, 11), (15, 17), (55, 17)]
    names = ["INPUT", "PROCESS", "OUTPUT", "MEMORY"]
    colors = ["●", "○", "◎", "◉"]
    for i in range(min(clusters, 4)):
        viz.draw_cluster(positions[i][0], positions[i][1], 3, names[i], colors[i])

    # 绘制连接
    for _ in range(5):
        p1 = random.choice(positions[:clusters])
        p2 = random.choice(positions[:clusters])
        if p1 != p2:
            viz.draw_synapse(p1[0], p1[1], p2[0], p2[1])

    # 统计
    stats = f"N:{neurons} S:{synapses} C:{clusters}"
    for i, c in enumerate(stats):
        viz._set(35 - len(stats)//2 + i, 21, c)

    return viz.render()


if __name__ == "__main__":
    print(create_network_diagram(57, 74, 4, 3))
