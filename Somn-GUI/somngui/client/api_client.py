"""
Somn GUI - API客户端
封装所有后端API调用，对GUI层提供简洁的Python接口
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class SomnAPIClient:
    """Somn后端API客户端"""

    def __init__(self, connection):
        """
        Args:
            connection: BackendConnection 实例
        """
        self._conn = connection

    # ── 系统 ──

    async def health_check(self) -> dict:
        """健康检查"""
        return await self._conn.get("/health")

    async def get_status(self) -> dict:
        """获取系统状态"""
        return await self._conn.get("/status")

    async def get_config(self) -> dict:
        """获取安全配置"""
        return await self._conn.get("/config")

    # ── 对话 ──

    async def chat(self, message: str, session_id: str = None,
                   context: dict = None, industry: str = None) -> dict:
        """发送对话消息"""
        body = {"message": message}
        if session_id:
            body["session_id"] = session_id
        if context:
            body["context"] = context
        if industry:
            body["industry"] = industry
        return await self._conn.post("/chat", json_data=body)

    async def chat_stream(self, message: str, session_id: str = None):
        """SSE流式对话 (复用连接管理器的客户端)"""
        import json
        url = f"/chat/stream"
        params = {"message": message}
        if session_id:
            params["session_id"] = session_id
        async with self._conn.client.stream("GET", url, params=params) as resp:
            async for line in resp.aiter_lines():
                if line.startswith("data: "):
                    yield json.loads(line[6:])

    # ── 知识库 ──

    async def list_knowledge(self, page: int = 1, page_size: int = 20,
                             category: str = None) -> dict:
        """获取知识库列表"""
        params = {"page": page, "page_size": page_size}
        if category:
            params["category"] = category
        return await self._conn.get("/knowledge", params=params)

    async def search_knowledge(self, query: str, top_k: int = 10) -> dict:
        """搜索知识库"""
        return await self._conn.post("/knowledge/search", json_data={
            "query": query, "top_k": top_k,
        })

    async def add_knowledge(self, title: str, content: str,
                            category: str = None, source: str = None) -> dict:
        """添加知识"""
        body = {"title": title, "content": content}
        if category:
            body["category"] = category
        if source:
            body["source"] = source
        return await self._conn.post("/knowledge/add", json_data=body)

    # ── 分析 ──

    async def strategy_analysis(self, description: str, industry: str = None,
                                depth: str = "standard", context: dict = None) -> dict:
        """策略分析"""
        body = {"description": description, "depth": depth}
        if industry:
            body["industry"] = industry
        if context:
            body["context"] = context
        return await self._conn.post("/analysis/strategy", json_data=body)

    async def market_analysis(self, description: str, context: dict = None) -> dict:
        """市场分析"""
        body = {"description": description}
        if context:
            body["context"] = context
        return await self._conn.post("/analysis/market", json_data=body)

    # ── 文档 ──

    async def generate_document(self, doc_type: str, title: str,
                                 format: str = "docx", context: dict = None) -> dict:
        """生成文档"""
        body = {"doc_type": doc_type, "title": title, "format": format}
        if context:
            body["context"] = context
        return await self._conn.post("/documents/generate", json_data=body)

    # ── 智慧引擎 ──

    async def list_wisdom_schools(self) -> dict:
        """获取智慧学派列表"""
        return await self._conn.get("/wisdom/schools")

    async def wisdom_query(self, query: str, schools: List[str] = None,
                           depth: str = "standard") -> dict:
        """智慧引擎查询"""
        body = {"query": query, "depth": depth}
        if schools:
            body["schools"] = schools
        return await self._conn.post("/wisdom/query", json_data=body)

    # ── 记忆 ──

    async def list_memories(self, page: int = 1, page_size: int = 20) -> dict:
        """获取记忆列表"""
        return await self._conn.get("/memory", params={
            "page": page, "page_size": page_size,
        })

    # ── 学习 ──

    async def get_learning_status(self) -> dict:
        """获取学习状态"""
        return await self._conn.get("/learning/status")

    async def trigger_learning(self) -> dict:
        """手动触发学习"""
        return await self._conn.post("/learning/trigger")

    # ═══════════════════════════════════════════════════════════
    # 系统管理 (Admin)
    # ═══════════════════════════════════════════════════════════

    # -- 仪表盘 --

    async def admin_dashboard(self) -> dict:
        """全局管理仪表盘"""
        return await self._conn.get("/admin/dashboard")

    # -- 引擎加载管理 --

    async def admin_load_stats(self) -> dict:
        """获取加载管理器统计"""
        return await self._conn.get("/admin/load-manager/stats")

    async def admin_load_status(self) -> dict:
        """获取所有模块加载状态"""
        return await self._conn.get("/admin/load-manager/status")

    async def admin_preload_modules(self, names: List[str]) -> dict:
        """预加载指定模块"""
        return await self._conn.post("/admin/load-manager/preload", json_data={"names": names})

    # -- LLM管理 --

    async def admin_llm_status(self) -> dict:
        """获取LLM管理器状态"""
        return await self._conn.get("/admin/llm/status")

    async def admin_llm_start(self) -> dict:
        """启动LLM引擎"""
        return await self._conn.post("/admin/llm/start")

    async def admin_llm_stop(self) -> dict:
        """停止LLM引擎"""
        return await self._conn.post("/admin/llm/stop")

    async def admin_llm_sessions(self) -> dict:
        """获取LLM会话列表"""
        return await self._conn.get("/admin/llm/sessions")

    async def admin_llm_clear_session(self, session_id: str) -> dict:
        """清除指定LLM会话"""
        return await self._conn.delete(f"/admin/llm/sessions/{session_id}")

    # -- 主链路监控 --

    async def admin_chain_full_status(self) -> dict:
        """获取主链路完整状态"""
        return await self._conn.get("/admin/chain/full-status")

    async def admin_chain_health(self) -> dict:
        """获取链路健康状态"""
        return await self._conn.get("/admin/chain/health")

    async def admin_chain_nodes(self) -> dict:
        """获取节点状态"""
        return await self._conn.get("/admin/chain/nodes")

    async def admin_chain_modes(self) -> dict:
        """获取模式分布"""
        return await self._conn.get("/admin/chain/modes")

    async def admin_chain_report(self) -> dict:
        """生成监控报告"""
        return await self._conn.get("/admin/chain/report")

    # -- 自主进化 --

    async def admin_evolution_report(self) -> dict:
        """获取进化报告"""
        return await self._conn.get("/admin/evolution/report")

    async def admin_evolution_diagnose(self) -> dict:
        """运行诊断周期"""
        return await self._conn.post("/admin/evolution/diagnose")

    async def admin_evolution_plans(self) -> dict:
        """获取活跃进化计划"""
        return await self._conn.get("/admin/evolution/plans")

    async def admin_evolution_visualizations(self) -> dict:
        """获取进化可视化数据"""
        return await self._conn.get("/admin/evolution/visualizations")

    # -- 记忆生命周期 --

    async def admin_memory_health(self) -> dict:
        """获取知识库健康报告"""
        return await self._conn.get("/admin/memory/health")

    async def admin_memory_registry(self, category: str = None, status: str = None,
                                      min_confidence: float = 0.0,
                                      page: int = 1, page_size: int = 20) -> dict:
        """获取知识注册表"""
        params = {"page": page, "page_size": page_size, "min_confidence": min_confidence}
        if category:
            params["category"] = category
        if status:
            params["status"] = status
        return await self._conn.get("/admin/memory/registry", params=params)

    async def admin_memory_review_tasks(self, max_tasks: int = 10,
                                          category: str = None) -> dict:
        """获取复习任务"""
        params = {"max_tasks": max_tasks}
        if category:
            params["category"] = category
        return await self._conn.get("/admin/memory/review-tasks", params=params)

    async def admin_memory_decay(self, force: bool = False) -> dict:
        """手动触发记忆衰减"""
        return await self._conn.post("/admin/memory/decay", json_data={"force": force})

    async def admin_memory_reinforce(self, knowledge_id: str,
                                       boost: float = 0.1) -> dict:
        """强化指定知识"""
        return await self._conn.post("/admin/memory/reinforce", json_data={
            "knowledge_id": knowledge_id, "boost": boost,
        })

    # -- Claw调度 --

    async def admin_claw_stats(self) -> dict:
        """获取Claw调度器统计"""
        return await self._conn.get("/admin/claw/stats")

    async def admin_claw_work_pool(self) -> dict:
        """获取工作池状态"""
        return await self._conn.get("/admin/claw/work-pool")

    async def admin_claw_list(self, department: str = None,
                                school: str = None, limit: int = 50) -> dict:
        """列出可用Claw"""
        params = {"limit": limit}
        if department:
            params["department"] = department
        if school:
            params["school"] = school
        return await self._conn.get("/admin/claw/list", params=params)

    async def admin_claw_recent(self, limit: int = 20) -> dict:
        """获取最近执行结果"""
        return await self._conn.get("/admin/claw/recent", params={"limit": limit})

    async def admin_claw_active_tasks(self) -> dict:
        """获取活跃任务"""
        return await self._conn.get("/admin/claw/active-tasks")

    async def admin_claw_dispatch(self, query: str, claw_name: str = None,
                                    department: str = None, school: str = None,
                                    collaborators: List[str] = None) -> dict:
        """调度Claw执行任务"""
        body = {"query": query}
        if claw_name:
            body["claw_name"] = claw_name
        if department:
            body["department"] = department
        if school:
            body["school"] = school
        if collaborators:
            body["collaborators"] = collaborators
        return await self._conn.post("/admin/claw/dispatch", json_data=body)

    # -- 系统监控 --

    async def admin_system_components(self) -> dict:
        """获取所有组件状态"""
        return await self._conn.get("/admin/system/components")

    async def admin_system_component_health(self, component_name: str) -> dict:
        """获取指定组件健康状态"""
        return await self._conn.get(f"/admin/system/component/{component_name}")

    # -- 神经网络布局管理 --

    async def admin_neural_status(self) -> dict:
        """获取神经网络布局状态"""
        return await self._conn.get("/admin/neural/status")

    async def admin_neural_topology(self) -> dict:
        """获取网络拓扑"""
        return await self._conn.get("/admin/neural/topology")

    async def admin_neural_phase_status(self) -> dict:
        """获取 Phase 1-5 系统状态"""
        return await self._conn.get("/admin/neural/phase-status")

    async def admin_neural_activate(self, input_data: dict = None) -> dict:
        """手动激活主链路"""
        return await self._conn.post("/admin/neural/activate", json_data=input_data)

    async def admin_neural_optimize_clusters(self) -> dict:
        """优化所有集群连接"""
        return await self._conn.post("/admin/neural/optimize-clusters")

    async def admin_neural_execution_history(self, limit: int = 20) -> dict:
        """获取执行历史"""
        return await self._conn.get("/admin/neural/execution-history", params={"limit": limit})

    async def admin_neural_bridge_status(self) -> dict:
        """获取全局神经桥梁状态"""
        return await self._conn.get("/admin/neural/bridge-status")

    async def admin_neural_layouts(self) -> dict:
        """列出所有布局"""
        return await self._conn.get("/admin/neural/layouts")

    async def admin_neural_create_layout(self, name: str, description: str = "") -> dict:
        """创建新布局"""
        return await self._conn.post("/admin/neural/layouts", json_data={
            "name": name, "description": description,
        })

    async def admin_neural_switch_layout(self, layout_id: str) -> dict:
        """切换活跃布局"""
        return await self._conn.put(f"/admin/neural/layouts/{layout_id}/switch")

    async def admin_neural_delete_layout(self, layout_id: str) -> dict:
        """删除指定布局"""
        return await self._conn.delete(f"/admin/neural/layouts/{layout_id}")

    async def admin_neural_visualize(self, vtype: str = "topology") -> dict:
        """生成网络可视化 (topology=拓扑, heatmap=热力图)"""
        return await self._conn.get("/admin/neural/visualize", params={"vtype": vtype})

    # -- 告警管理 --

    async def admin_alerts_history(self, limit: int = 50,
                                  level: str = None) -> dict:
        """获取告警历史"""
        params = {"limit": limit}
        if level:
            params["level"] = level
        return await self._conn.get("/admin/alerts/history", params=params)

    async def admin_alerts_stats(self) -> dict:
        """获取告警统计"""
        return await self._conn.get("/admin/alerts/stats")

    async def admin_alerts_clear(self, level: str = None) -> dict:
        """清除告警历史"""
        params = {}
        if level:
            params["level"] = level
        return await self._conn.delete("/admin/alerts/clear", params=params)

    async def admin_alerts_trigger(self, level: str = "WARNING",
                                   source: str = "manual",
                                   message: str = "手动触发测试告警",
                                   details: dict = None) -> dict:
        """手动触发告警（测试用）"""
        body = {"level": level, "source": source, "message": message}
        if details:
            body["details"] = details
        return await self._conn.post("/admin/alerts/trigger", json_data=body)
