#!/usr/bin/env python3
"""
Somn API 客户端 - 全局控制中心专用
"""

import requests
import json
from typing import Optional, Dict, Any, List
from datetime import datetime


class SomnAPIClient:
    """Somn API 客户端"""

    def __init__(self, base_url: str = "http://127.0.0.1:8964", timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict]:
        """发送请求"""
        url = f"{self.base_url}{endpoint}"
        try:
            resp = self.session.request(method, url, timeout=self.timeout, **kwargs)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.ConnectionError:
            return {"error": "无法连接到后端服务"}
        except requests.exceptions.Timeout:
            return {"error": "请求超时"}
        except Exception as e:
            print(f"[API客户端] 请求异常: {e}")
            return {"error": "请求失败"}

    def get(self, endpoint: str, **kwargs) -> Optional[Dict]:
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Optional[Dict]:
        return self._request("POST", endpoint, **kwargs)

    # ========== 基础端点 ==========

    def health_check(self) -> Dict:
        """健康检查"""
        return self.get("/api/v1/health")

    def get_system_info(self) -> Dict:
        """系统信息"""
        return self.get("/api/v1/info")

    # ========== 管理端点 ==========

    def get_loaded_modules(self) -> Dict:
        """已加载模块"""
        return self.get("/api/v1/admin/load-manager/loaded-modules")

    def get_llm_status(self) -> Dict:
        """LLM状态"""
        return self.get("/api/v1/admin/llm/status")

    def get_chain_status(self) -> Dict:
        """主链路状态"""
        return self.get("/api/v1/admin/chain/status")

    def get_evolution_status(self) -> Dict:
        """进化状态"""
        return self.get("/api/v1/admin/evolution/status")

    def get_memory_status(self) -> Dict:
        """记忆状态"""
        return self.get("/api/v1/admin/memory/status")

    def get_claw_status(self) -> Dict:
        """Claw系统状态"""
        return self.get("/api/v1/admin/claw/status")

    def get_system_components(self) -> Dict:
        """系统组件"""
        return self.get("/api/v1/admin/system/components")

    # ========== 神经网络端点 ==========

    def get_neural_status(self) -> Dict:
        """神经网络状态"""
        return self.get("/api/v1/neural/status")

    def get_neural_topology(self) -> Dict:
        """神经网络拓扑"""
        return self.get("/api/v1/neural/topology")

    def get_phase_status(self, phase: int = None) -> Dict:
        """Phase状态"""
        if phase:
            return self.get(f"/api/v1/neural/phase-status/{phase}")
        return self.get("/api/v1/neural/phase-status")

    def get_execution_history(self, limit: int = 10) -> Dict:
        """执行历史"""
        return self.get(f"/api/v1/neural/execution-history?limit={limit}")

    def get_bridge_status(self) -> Dict:
        """桥接状态"""
        return self.get("/api/v1/neural/bridge-status")

    def get_all_layouts(self) -> Dict:
        """所有布局"""
        return self.get("/api/v1/neural/layouts")

    # ========== 综合信息 ==========

    def get_full_status(self) -> Dict:
        """获取完整状态"""
        return {
            "timestamp": datetime.now().isoformat(),
            "health": self.health_check(),
            "system": self.get_system_info(),
            "modules": self.get_loaded_modules(),
            "llm": self.get_llm_status(),
            "chain": self.get_chain_status(),
            "evolution": self.get_evolution_status(),
            "memory": self.get_memory_status(),
            "claw": self.get_claw_status(),
            "neural": self.get_neural_status(),
        }

    def get_dashboard_data(self) -> Dict:
        """获取仪表板数据"""
        try:
            health = self.health_check()
            neural = self.get_neural_status()
            claw = self.get_claw_status()
            modules = self.get_loaded_modules()

            return {
                "status": "online",
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "modules": {
                    "total": modules.get("total_count", 32),
                    "loaded": modules.get("loaded_count", 0),
                },
                "engines": {
                    "total": 45,
                    "active": claw.get("active_count", 0),
                },
                "claws": {
                    "total": claw.get("total_count", 776),
                    "active": claw.get("active_count", 0),
                    "schools": claw.get("school_count", 35),
                },
                "neural": {
                    "neurons": neural.get("neuron_count", 57),
                    "synapses": neural.get("synapse_count", 74),
                    "clusters": neural.get("cluster_count", 4),
                    "phase": neural.get("current_phase", 0),
                },
            }
        except Exception as e:
            print(f"[API客户端] 获取仪表板数据异常: {e}")
            return {"status": "error", "error": "获取仪表板数据失败"}


# 全局实例
_api_client: Optional[SomnAPIClient] = None


def get_api_client(base_url: str = "http://127.0.0.1:8964") -> SomnAPIClient:
    """获取API客户端实例"""
    global _api_client
    if _api_client is None:
        _api_client = SomnAPIClient(base_url)
    return _api_client
