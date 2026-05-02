"""
Pan-Wisdom Tree 神行轨适配器
让Pan-Wisdom Tree的枝丫能够调用神行轨完成工作

功能：
1. 提供统一的神行轨调用接口
2. 管理神行轨执行器的生命周期
3. 处理执行结果和错误

使用方法：
    from knowledge_cells.dispatchers import TrackBExecutor
    
    # 获取执行器
    executor = TrackBExecutor.get_instance()
    
    # 调用神行轨执行任务
    result = executor.execute(
        branch_id="SD-F1",
        department="兵部",
        task="分析竞争对手策略",
        context={"user_query": "..."}
    )
"""

import logging
import threading
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TrackBConfig:
    """神行轨配置"""
    # 神行轨部门映射
    DEPARTMENT_MAP = {
        # SD-F1 学派融合
        "兵部": "兵部",
        "吏部": "吏部", 
        "户部": "户部",
        "礼部": "礼部",
        "刑部": "刑部",
        "工部": "工部",
        "外交部": "外交部",
        "教育部": "教育部",
        "科技部": "科技部",
        "文化部": "文化部",
        "卫生部": "卫生部",
    }
    
    # 枝丫到部门的默认映射
    BRANCH_DEPARTMENT_DEFAULT = {
        "SD-F1": "礼部",      # 学派融合 → 礼部(文化智慧)
        "SD-D1": "吏部",      # 轻量推理 → 吏部(人才考核)
        "SD-D2": "吏部",      # 标准推理 → 吏部
        "SD-D3": "吏部",      # 极致推理 → 吏部
        "SD-C1": "兵部",      # 阴阳决策 → 兵部(战略)
        "SD-C2": "兵部",      # 神之架构 → 兵部
        "SD-E1": "工部",      # 执行调度 → 工部
        "SD-L1": "户部",      # 学习追踪 → 户部(资源)
        "SD-R2": "刑部",      # 谬误检测 → 刑部(律法)
    }
    
    # 执行超时时间(秒)
    EXECUTION_TIMEOUT = 30
    
    # 重试次数
    MAX_RETRIES = 2

    # LLM 回复最小有效长度（低于此值视为无实质内容）
    LLM_MIN_MEANINGFUL_LENGTH = 10


class TrackBExecutor:
    """
    神行轨执行器
    
    Pan-Wisdom Tree的枝丫通过此类调用神行轨。
    提供两种调用模式：
    1. 直接执行：executor.execute(branch_id, task, department)
    2. 快捷执行：executor.execute_quick(branch_id, task)
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __init__(self):
        self._caller: Optional[Callable] = None
        self._connected = False
        self._config = TrackBConfig()
        self._execution_history: List[Dict] = []
        logger.info("[TrackB-Adapter] 神行轨执行器初始化")
    
    @classmethod
    def get_instance(cls) -> "TrackBExecutor":
        """获取单例实例（线程安全）"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    @classmethod
    def reset_instance(cls):
        """重置单例（用于断开后重新创建）"""
        if cls._instance is not None:
            cls._instance.disconnect()
            cls._instance = None
    
    def connect(self, bridge_caller: Callable) -> bool:
        """
        连接神行轨调用器
        
        Args:
            bridge_caller: 从TrackBridge.create_wisdom_tree_caller()获取的调用函数
            
        Returns:
            连接是否成功
        """
        # 如果已有连接，先断开旧的
        if self._connected and self._caller is not None:
            self.disconnect()
        self._caller = bridge_caller
        self._connected = True
        logger.info("[TrackB-Adapter] 已连接到神行轨")
        return True
    
    def reconnect(self, bridge_caller: Callable) -> bool:
        """
        重新连接神行轨调用器（等效于 disconnect + connect）
        
        用途：当连接丢失或调用器更新时，可直接调用此方法重连。
        """
        self.reset_instance()
        instance = self.get_instance()
        return instance.connect(bridge_caller)
    
    def disconnect(self):
        """断开连接"""
        self._caller = None
        self._connected = False
        logger.info("[TrackB-Adapter] 已断开神行轨连接")
    
    def is_connected(self) -> bool:
        """检查是否已连接"""
        return self._connected and self._caller is not None
    
    def execute(
        self,
        branch_id: str,
        department: str,
        task: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        执行神行轨任务
        
        Args:
            branch_id: 枝丫标识 (如 "SD-F1", "SD-D2")
            department: 目标部门 (如 "兵部", "礼部")
            task: 任务描述
            context: 额外上下文
            
        Returns:
            执行结果
        """
        logger.info(f"[TrackB-Adapter] 枝丫 {branch_id} → 部门 {department}: {task[:50]}...")
        
        # 记录执行
        execution_record = {
            "branch_id": branch_id,
            "department": department,
            "task": task,
            "status": "pending"
        }
        
        # 检查连接
        if not self.is_connected():
            # 尝试使用向后兼容方式
            return self._execute_fallback(branch_id, department, task, context)
        
        try:
            # 构建合并后的调用上下文（确保 context 不被忽略）
            call_context = dict(context or {})
            call_context.setdefault("_branch_id", branch_id)
            call_context.setdefault("_department", department)
            call_context.setdefault("_caller_type", "pan_wisdom_tree")
            
            # 调用神行轨
            result = self._caller(
                department=department,
                task_description=task,
                context=call_context
            )
            
            # 智能判断执行成功：检查返回结构中的 success 字段
            if isinstance(result, dict):
                exec_success = result.get("success", True)
            else:
                exec_success = True  # 非字典结果视为成功
            
            execution_record["status"] = "success" if exec_success else "failed"
            execution_record["result"] = result
            self._execution_history.append(execution_record)
            
            return {
                "success": exec_success,
                "source": "track_b",
                "caller": "pan_wisdom_tree",
                "branch_id": branch_id,
                "department": department,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"[TrackB-Adapter] 执行失败: {e}")
            execution_record["status"] = "failed"
            execution_record["error"] = str(e)
            self._execution_history.append(execution_record)
            
            return {
                "success": False,
                "source": "track_b",
                "error": str(e),
                "fallback": "local"
            }
    
    def execute_quick(
        self,
        branch_id: str,
        task: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        快捷执行 - 自动选择部门
        
        Args:
            branch_id: 枝丫标识
            task: 任务描述
            context: 额外上下文
            
        Returns:
            执行结果
        """
        department = self._config.BRANCH_DEPARTMENT_DEFAULT.get(branch_id, "礼部")
        return self.execute(branch_id, department, task, context)
    
    def execute_chain(
        self,
        branch_id: str,
        tasks: List[Dict[str, str]],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        链式执行 - 多个任务顺序执行
        
        Args:
            branch_id: 枝丫标识
            tasks: 任务列表 [{"department": "兵部", "task": "任务1"}, ...]
            context: 额外上下文
            
        Returns:
            链式执行结果
        """
        results = []
        
        for i, item in enumerate(tasks):
            department = item.get("department", self._config.BRANCH_DEPARTMENT_DEFAULT.get(branch_id, "礼部"))
            task = item.get("task", "")
            
            logger.info(f"[TrackB-Adapter] 链式执行 [{i+1}/{len(tasks)}]: {department}")
            
            # 将上一步结果作为上下文传递给下一步
            chain_context = dict(context or {})
            if results:
                chain_context["_prev_step_result"] = results[-1].get("result", {})
            
            result = self.execute(branch_id, department, task, chain_context)
            results.append({
                "step": i + 1,
                "department": department,
                "result": result
            })
            
            # 如果失败，停止链式执行（基于顶层的 success 字段）
            if not result.get("success", False):
                logger.warning(f"[TrackB-Adapter] 链式执行在步骤 {i+1} 失败")
                break
        
        # 成功判断：所有已完成的步骤都必须 success=True
        all_success = all(r.get("success", False) for r in results)
        
        return {
            "success": all_success,
            "chain": results,
            "total_steps": len(results),
            "completed_steps": len([r for r in results if r.get("success", False)]),
            "failed_at": results[-1]["step"] if results and not results[-1].get("success", False) else None,
        }
    
    def _execute_fallback(
        self,
        branch_id: str,
        department: str,
        task: str,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        回退执行 - 神行轨未连接时使用 LLM 增强回退 + 本地模拟

        Args:
            branch_id: 枝丫标识
            department: 部门
            task: 任务
            context: 上下文

        Returns:
            模拟执行结果
        """
        logger.debug(f"[TrackB-Adapter] 神行轨未连接，使用本地模拟执行")

        # 构建包含完整上下文的任务描述
        context_info = ""
        if context:
            context_keys = [k for k in context if not k.startswith("_")]
            if context_keys:
                context_info = f"（上下文：{', '.join(f'{k}={context[k]}' for k in context_keys[:5])}）"

        # 尝试 LLM 增强回退
        try:
            from .llm_rule_layer import call_module_llm
            prompt = f"从{department}视角分析：{task[:200]}{context_info}"
            llm_result = call_module_llm("TrackB", prompt)
            # 降低有效长度阈值：只要内容有实质意义（非空/非纯空格）就使用
            if llm_result and len(llm_result.strip()) >= self._config.LLM_MIN_MEANINGFUL_LENGTH:
                return {
                    "success": True,
                    "is_fallback": True,
                    "source": "llm_fallback",
                    "branch_id": branch_id,
                    "department": department,
                    "result": {
                        "success": True,
                        "is_fallback": True,
                        "department": department,
                        "task": task,
                        "output": llm_result,
                        "mode": "llm_enhanced_fallback",
                        "context_used": bool(context),
                    }
                }
        except Exception as e:
            logger.debug(f"[TrackB-Adapter] LLM fallback失败: {e}")

        # 根据部门返回模拟结果
        mock_results = {
            "兵部": "【兵部策略分析】基于战略视角的综合分析已完成",
            "吏部": "【吏部人才评估】从人才管理角度的分析已完成",
            "户部": "【户部资源规划】资源分配方案已制定",
            "礼部": "【礼部文化融合】跨学派智慧融合已完成",
            "刑部": "【刑部风险审查】合规性和风险评估已完成",
            "工部": "【工部执行计划】实施方案已制定",
            "外交部": "【外交部协调】外部资源协调方案已生成",
            "教育部": "【教育部培训】能力提升计划已制定",
            "科技部": "【科技部创新】技术创新方案已分析",
            "文化部": "【文化部洞察】文化影响分析已完成",
            "卫生部": "【卫生部健康】健康风险管理方案已制定",
        }

        return {
            "success": False,
            "is_mock": True,
            "source": "local_mock",
            "caller": "pan_wisdom_tree",
            "branch_id": branch_id,
            "department": department,
            "result": {
                "success": False,
                "is_mock": True,
                "department": department,
                "task": task,
                "output": mock_results.get(department, f"【{department}】分析已完成"),
                "mode": "local_fallback",
                "context_used": bool(context),
                "warning": "神行轨未连接，返回本地模拟结果，不具备真实分析能力"
            }
        }
    
    def get_execution_history(self, limit: int = 10) -> List[Dict]:
        """获取执行历史"""
        return self._execution_history[-limit:]
    
    def clear_history(self):
        """清空执行历史"""
        self._execution_history.clear()
        logger.info("[TrackB-Adapter] 执行历史已清空")


# 全局执行器实例（懒加载 — 首次调用时才实例化）
_executor: Optional[TrackBExecutor] = None


def get_track_b_executor() -> TrackBExecutor:
    """获取全局神行轨执行器（懒加载，首次调用时实例化）"""
    global _executor
    if _executor is None:
        _executor = TrackBExecutor.get_instance()
    return _executor


def execute_with_track_b(
    branch_id: str,
    task: str,
    department: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    便捷函数：使用神行轨执行任务
    
    Args:
        branch_id: 枝丫标识 (如 "SD-F1")
        task: 任务描述
        department: 部门 (可选，默认使用BRANCH_DEPARTMENT_DEFAULT映射)
        context: 额外上下文
        
    Returns:
        执行结果
    """
    executor = get_track_b_executor()
    
    if department:
        return executor.execute(branch_id, department, task, context)
    else:
        return executor.execute_quick(branch_id, task, context)


# ═══════════════════════════════════════════════════════════════════
# 枝丫快捷调用函数
# ═══════════════════════════════════════════════════════════════════

def wisdom_tree_call(branch_id: str, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """
    通用枝丫调用函数
    
    使用方式:
        result = wisdom_tree_call("SD-F1", "融合东西方智慧分析这个问题")
    """
    return execute_with_track_b(branch_id, task, context=context)


def sd_f1_call(task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """SD-F1 学派融合调用"""
    return execute_with_track_b("SD-F1", task, "礼部", context)


def sd_d_call(task: str, depth: str = "standard", context: Optional[Dict] = None) -> Dict[str, Any]:
    """SD-D系列推理调用"""
    branch_id = f"SD-D{'1' if depth == 'light' else '2' if depth == 'standard' else '3'}"
    return execute_with_track_b(branch_id, task, "吏部", context)


def sd_c1_call(task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """SD-C1 太极阴阳决策调用"""
    return execute_with_track_b("SD-C1", task, "兵部", context)


def sd_c2_call(task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """SD-C2 神之架构决策调用"""
    return execute_with_track_b("SD-C2", task, "兵部", context)


def sd_e1_call(task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """SD-E1 五步主链执行调用"""
    return execute_with_track_b("SD-E1", task, "工部", context)


def sd_l1_call(task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """SD-L1 学习追踪调用"""
    return execute_with_track_b("SD-L1", task, "户部", context)


def sd_r2_call(task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """SD-R2 谬误检测调用"""
    return execute_with_track_b("SD-R2", task, "刑部", context)
