# -*- coding: utf-8 -*-
"""
ReAct推理引擎模块
Reasoning and Acting Engine

实现推理与行动的协同框架(ReAct)，支持：
- TAO闭环机制 (Thought-Act-Observe)
- 外部工具注册和调用
- 上下文管理和轨迹裁剪
- 多轮推理与行动协同

作者: Somn AI
版本: V1.0.0
日期: 2026-04-24
"""

from __future__ import annotations

import uuid
import time
import json
import logging
from typing import Dict, List, Optional, Any, Callable, Set, Type, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod
from collections import deque
import threading
import re

logger = logging.getLogger(__name__)


class ActionType(Enum):
    """行动类型枚举"""
    SEARCH = "search"                 # 搜索
    CALCULATE = "calculate"           # 计算
    LOOKUP = "lookup"                # 查询
    RETRIEVE = "retrieve"            # 检索
    EXECUTE = "execute"              # 执行
    QUERY = "query"                  # 询问
    CUSTOM = "custom"                # 自定义


@dataclass
class ToolResult:
    """工具执行结果"""
    tool_name: str
    success: bool
    result: Any
    error: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'tool_name': self.tool_name,
            'success': self.success,
            'result': str(self.result)[:500] if self.result else None,
            'error': self.error,
            'execution_time': self.execution_time
        }


@dataclass
class TAOStep:
    """TAO闭环单步"""
    step_id: str
    step_type: str                    # "thought", "act", "observe"
    content: str
    action: Optional[Dict[str, Any]] = None
    observation: Optional[ToolResult] = None
    confidence: float = 1.0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'step_id': self.step_id,
            'step_type': self.step_type,
            'content': self.content[:200] + '...' if len(self.content) > 200 else self.content,
            'action': self.action,
            'observation': self.observation.to_dict() if self.observation else None,
            'confidence': self.confidence,
            'created_at': self.created_at
        }


@dataclass
class TAOTrajectory:
    """TAO推理轨迹"""
    trajectory_id: str
    problem: str
    steps: List[TAOStep] = field(default_factory=list)
    status: str = "running"           # running, completed, failed, timeout
    total_thoughts: int = 0
    total_actions: int = 0
    total_observations: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    
    def add_thought(self, content: str, confidence: float = 1.0) -> TAOStep:
        """添加思考步骤"""
        step = TAOStep(
            step_id=str(uuid.uuid4()),
            step_type="thought",
            content=content,
            confidence=confidence
        )
        self.steps.append(step)
        self.total_thoughts += 1
        return step
    
    def add_action(self, content: str, action: Dict[str, Any]) -> TAOStep:
        """添加行动步骤"""
        step = TAOStep(
            step_id=str(uuid.uuid4()),
            step_type="act",
            content=content,
            action=action
        )
        self.steps.append(step)
        self.total_actions += 1
        return step
    
    def add_observation(self, content: str, result: ToolResult) -> TAOStep:
        """添加观察步骤"""
        step = TAOStep(
            step_id=str(uuid.uuid4()),
            step_type="observe",
            content=content,
            observation=result
        )
        self.steps.append(step)
        self.total_observations += 1
        return step
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'trajectory_id': self.trajectory_id,
            'problem': self.problem[:100],
            'steps_count': len(self.steps),
            'status': self.status,
            'total_thoughts': self.total_thoughts,
            'total_actions': self.total_actions,
            'total_observations': self.total_observations,
            'steps': [s.to_dict() for s in self.steps],
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }
    
    def get_recent_steps(self, n: int = 3) -> List[TAOStep]:
        """获取最近n个步骤"""
        return self.steps[-n:] if len(self.steps) >= n else self.steps
    
    def get_summary(self) -> str:
        """获取轨迹摘要"""
        return (
            f"轨迹包含 {len(self.steps)} 个步骤 "
            f"(思考: {self.total_thoughts}, "
            f"行动: {self.total_actions}, "
            f"观察: {self.total_observations})"
        )


class Tool(ABC):
    """工具基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """执行工具"""
        pass
    
    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """获取工具schema"""
        pass
    
    def validate_params(self, params: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """验证参数"""
        schema = self.get_schema()
        required = schema.get('required', [])
        
        for req_param in required:
            if req_param not in params:
                return False, f"缺少必需参数: {req_param}"
        
        return True, None


class SearchTool(Tool):
    """搜索工具"""
    
    def __init__(self, search_func: Callable[[str, int], List[Dict]]):
        super().__init__(
            name="search",
            description="搜索互联网获取信息"
        )
        self.search_func = search_func
    
    def execute(self, query: str, max_results: int = 5, **kwargs) -> ToolResult:
        """执行搜索"""
        start_time = time.time()
        try:
            results = self.search_func(query, max_results)
            return ToolResult(
                tool_name=self.name,
                success=True,
                result=results,
                execution_time=time.time() - start_time
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                success=False,
                result=None,
                error="执行失败",
                execution_time=time.time() - start_time
            )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'description': self.description,
            'parameters': {
                'query': {'type': 'string', 'description': '搜索查询'},
                'max_results': {'type': 'integer', 'description': '最大结果数', 'default': 5}
            },
            'required': ['query']
        }


class CalculatorTool(Tool):
    """计算工具"""
    
    def __init__(self):
        super().__init__(
            name="calculate",
            description="执行数学计算"
        )
    
    def execute(self, expression: str, **kwargs) -> ToolResult:
        """执行计算"""
        start_time = time.time()
        try:
            # 安全计算（仅支持基本运算）
            safe_chars = set('0123456789+-*/()., ')
            if not all(c in safe_chars for c in expression):
                raise ValueError("表达式包含非法字符")
            
            result = eval(expression, {"__builtins__": {}}, {})

            return ToolResult(
                tool_name=self.name,
                success=True,
                result=result,
                execution_time=time.time() - start_time
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                success=False,
                result=None,
                error="执行失败",
                execution_time=time.time() - start_time
            )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'description': self.description,
            'parameters': {
                'expression': {'type': 'string', 'description': '数学表达式'}
            },
            'required': ['expression']
        }


class LookupTool(Tool):
    """查询工具（知识库/数据库）"""
    
    def __init__(self, lookup_func: Callable[[str], Optional[Dict]]):
        super().__init__(
            name="lookup",
            description="从知识库查询信息"
        )
        self.lookup_func = lookup_func
    
    def execute(self, entity: str, **kwargs) -> ToolResult:
        """执行查询"""
        start_time = time.time()
        try:
            result = self.lookup_func(entity)
            return ToolResult(
                tool_name=self.name,
                success=True,
                result=result,
                execution_time=time.time() - start_time
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                success=False,
                result=None,
                error="执行失败",
                execution_time=time.time() - start_time
            )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'description': self.description,
            'parameters': {
                'entity': {'type': 'string', 'description': '要查询的实体名称'}
            },
            'required': ['entity']
        }


class RetrieveTool(Tool):
    """检索工具（文档/文件）"""
    
    def __init__(self, retrieve_func: Callable[[str], Optional[str]]):
        super().__init__(
            name="retrieve",
            description="从文档或文件中检索内容"
        )
        self.retrieve_func = retrieve_func
    
    def execute(self, query: str, source: Optional[str] = None, **kwargs) -> ToolResult:
        """执行检索"""
        start_time = time.time()
        try:
            result = self.retrieve_func(query, source)
            return ToolResult(
                tool_name=self.name,
                success=True,
                result=result,
                execution_time=time.time() - start_time
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                success=False,
                result=None,
                error="执行失败",
                execution_time=time.time() - start_time
            )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'description': self.description,
            'parameters': {
                'query': {'type': 'string', 'description': '检索查询'},
                'source': {'type': 'string', 'description': '来源（可选）'}
            },
            'required': ['query']
        }


class ToolRegistry:
    """工具注册表"""
    
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
        self._lock = threading.Lock()
    
    def register(self, tool: Tool) -> bool:
        """注册工具"""
        with self._lock:
            if tool.name in self._tools:
                logger.warning(f"工具 {tool.name} 已存在，将被覆盖")
            self._tools[tool.name] = tool
            logger.info(f"工具已注册: {tool.name}")
            return True
    
    def unregister(self, name: str) -> bool:
        """注销工具"""
        with self._lock:
            if name in self._tools:
                del self._tools[name]
                logger.info(f"工具已注销: {name}")
                return True
            return False
    
    def get(self, name: str) -> Optional[Tool]:
        """获取工具"""
        return self._tools.get(name)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """列出所有工具"""
        return [
            {
                'name': tool.name,
                'description': tool.description,
                'schema': tool.get_schema()
            }
            for tool in self._tools.values()
        ]
    
    def has_tool(self, name: str) -> bool:
        """检查工具是否存在"""
        return name in self._tools


class ToolExecutor:
    """工具执行器"""
    
    def __init__(self, registry: ToolRegistry):
        self.registry = registry
        self.execution_history: deque = deque(maxlen=100)
        self._execution_count: Dict[str, int] = {}
    
    def execute(
        self, 
        tool_name: str, 
        params: Dict[str, Any],
        max_retries: int = 2
    ) -> ToolResult:
        """执行工具"""
        tool = self.registry.get(tool_name)
        
        if not tool:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                result=None,
                error=f"工具不存在: {tool_name}"
            )
        
        # 参数验证
        valid, error = tool.validate_params(params)
        if not valid:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                result=None,
                error=error
            )
        
        # 重试机制
        last_error = None
        for attempt in range(max_retries):
            try:
                result = tool.execute(**params)
                
                # 记录执行历史
                self._record_execution(tool_name, result)
                
                return result
            except Exception as e:
                last_error = "推理引擎失败"
                logger.warning(f"工具执行失败 (尝试 {attempt + 1}/{max_retries}): {e}")
        
        return ToolResult(
            tool_name=tool_name,
            success=False,
            result=None,
            error=last_error or "执行失败"
        )
    
    def _record_execution(self, tool_name: str, result: ToolResult):
        """记录执行历史"""
        self.execution_history.append({
            'tool_name': tool_name,
            'success': result.success,
            'execution_time': result.execution_time,
            'timestamp': datetime.now().isoformat()
        })
        
        self._execution_count[tool_name] = self._execution_count.get(tool_name, 0) + 1
    
    def get_stats(self) -> Dict[str, Any]:
        """获取执行统计"""
        return {
            'total_executions': len(self.execution_history),
            'execution_counts': self._execution_count,
            'success_rate': self._calculate_success_rate()
        }
    
    def _calculate_success_rate(self) -> float:
        """计算成功率"""
        if not self.execution_history:
            return 0.0
        
        successes = sum(1 for e in self.execution_history if e['success'])
        return successes / len(self.execution_history)


class ThoughtGenerator:
    """思考生成器"""
    
    def __init__(self, llm_callable: Callable[[str], str]):
        self.llm_callable = llm_callable
        self.prompt_template = self._default_template()
    
    def _default_template(self) -> str:
        return """你是一个推理引擎，负责分析问题并决定下一步行动。

当前问题：{problem}

推理历史：
{history}

观察结果：
{observations}

请进行思考并决定下一步行动。

要求：
1. 分析当前状态和问题
2. 考虑已有的推理和观察结果
3. 决定是否需要采取行动（使用工具）还是继续推理
4. 如果需要行动，明确指定工具名称和参数

请用以下格式回答：
[思考] 你的分析推理过程...
[行动] (如果需要行动)
工具: <工具名称>
参数: <参数JSON>
(如果不需要行动)
[结论] 你的最终结论或答案...
"""
    
    def generate(
        self, 
        problem: str, 
        trajectory: TAOTrajectory,
        available_tools: List[str]
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """
        生成思考和行动
        
        Returns:
            Tuple[str, Optional[Dict[str, Any]]]: (思考内容, 行动参数如果需要)
        """
        # 构建历史上下文
        history = self._build_history_context(trajectory)
        observations = self._build_observations_context(trajectory)
        
        prompt = self.prompt_template.format(
            problem=problem,
            history=history,
            observations=observations
        )
        
        # 添加可用工具信息
        tools_info = "\n可用工具:\n" + "\n".join([f"- {t}" for t in available_tools])
        prompt += f"\n{tools_info}\n\n请注意：如果需要使用工具，请严格按照上述格式返回。"
        
        try:
            response = self.llm_callable(prompt)
        except Exception as e:
            logger.error(f"思考生成失败: {e}")
            return f"分析问题：{problem}", None
        
        # 解析响应
        return self._parse_response(response)
    
    def _build_history_context(self, trajectory: TAOTrajectory) -> str:
        """构建历史上下文"""
        if not trajectory.steps:
            return "暂无推理历史"
        
        lines = []
        for step in trajectory.steps[-5:]:  # 最近5步
            if step.step_type == "thought":
                lines.append(f"[思考] {step.content[:100]}")
            elif step.step_type == "act":
                lines.append(f"[行动] {step.content[:100]}")
        
        return "\n".join(lines) if lines else "暂无详细历史"
    
    def _build_observations_context(self, trajectory: TAOTrajectory) -> str:
        """构建观察上下文"""
        observations = [
            s for s in trajectory.steps 
            if s.step_type == "observe"
        ]
        
        if not observations:
            return "暂无观察结果"
        
        lines = []
        for obs in observations[-3:]:  # 最近3个观察
            if obs.observation:
                result_str = str(obs.observation.result)[:200]
                lines.append(f"- {obs.observation.tool_name}: {result_str}")
        
        return "\n".join(lines) if lines else "暂无观察结果"
    
    def _parse_response(self, response: str) -> Tuple[str, Optional[Dict[str, Any]]]:
        """解析LLM响应"""
        thought = None
        action = None
        
        # 提取思考
        thought_match = re.search(r'\[思考\]\s*(.+?)(?=\[行动\]|\[结论\]|$)', response, re.DOTALL)
        if thought_match:
            thought = thought_match.group(1).strip()
        
        # 提取行动
        action_match = re.search(r'\[行动\]\s*工具:\s*(\w+)\s*参数:\s*(\{.+?\})', response, re.DOTALL)
        if action_match:
            tool_name = action_match.group(1)
            params_str = action_match.group(2)
            try:
                params = json.loads(params_str)
                action = {'tool': tool_name, 'params': params}
            except json.JSONDecodeError:
                logger.warning(f"参数解析失败: {params_str}")
        
        # 提取结论
        if not thought:
            conclusion_match = re.search(r'\[结论\]\s*(.+)$', response, re.DOTALL)
            if conclusion_match:
                thought = conclusion_match.group(1).strip()
        
        return thought or "分析中...", action


class ContextManager:
    """上下文管理器"""
    
    def __init__(
        self, 
        max_context_length: int = 8000,
        preserve_recent: int = 3,
        summary_enabled: bool = True
    ):
        self.max_context_length = max_context_length
        self.preserve_recent = preserve_recent
        self.summary_enabled = summary_enabled
        
        self._summary_history: List[str] = []
    
    def manage(
        self, 
        trajectory: TAOTrajectory,
        llm_callable: Optional[Callable] = None
    ) -> str:
        """
        管理上下文，必要时进行裁剪和摘要
        
        Returns:
            str: 管理后的上下文字符串
        """
        total_length = self._estimate_total_length(trajectory)
        
        if total_length <= self.max_context_length:
            return self._build_full_context(trajectory)
        
        # 需要裁剪
        if self.summary_enabled and llm_callable:
            return self._build_summarized_context(trajectory, llm_callable)
        else:
            return self._build_pruned_context(trajectory)
    
    def _estimate_total_length(self, trajectory: TAOTrajectory) -> int:
        """估算总长度"""
        return sum(len(s.content) for s in trajectory.steps)
    
    def _build_full_context(self, trajectory: TAOTrajectory) -> str:
        """构建完整上下文"""
        lines = [f"问题：{trajectory.problem}"]
        
        for step in trajectory.steps:
            if step.step_type == "thought":
                lines.append(f"\n[思考] {step.content}")
            elif step.step_type == "act":
                action_str = json.dumps(step.action, ensure_ascii=False) if step.action else ""
                lines.append(f"\n[行动] {step.content} {action_str}")
            elif step.step_type == "observe":
                obs = step.observation
                lines.append(f"\n[观察] {obs.tool_name}: {obs.result}")
        
        return "\n".join(lines)
    
    def _build_pruned_context(self, trajectory: TAOTrajectory) -> str:
        """构建裁剪后的上下文"""
        # 保留最近的步骤
        recent_steps = trajectory.steps[-self.preserve_recent:]
        
        # 构建摘要
        lines = [f"问题：{trajectory.problem}"]
        
        if self._summary_history:
            lines.append("\n[历史摘要]")
            lines.extend(self._summary_history[-2:])  # 最多2条历史摘要
        
        lines.append("\n[最近步骤]")
        for step in recent_steps:
            lines.append(f"- [{step.step_type}] {step.content[:100]}")
        
        return "\n".join(lines)
    
    def _build_summarized_context(
        self, 
        trajectory: TAOTrajectory,
        llm_callable: Callable
    ) -> str:
        """构建摘要上下文"""
        # 保留最近的步骤
        recent_steps = trajectory.steps[-self.preserve_recent:]
        
        # 生成摘要
        if len(trajectory.steps) > self.preserve_recent + 5:
            older_steps = trajectory.steps[:-self.preserve_recent]
            summary = self._generate_summary(older_steps, llm_callable)
            self._summary_history.append(summary)
        
        # 构建最终上下文
        lines = [f"问题：{trajectory.problem}"]
        
        if self._summary_history:
            lines.append("\n[推理摘要]")
            lines.extend(self._summary_history[-2:])
        
        lines.append("\n[最近步骤]")
        for step in recent_steps:
            lines.append(f"- [{step.step_type}] {step.content[:100]}")
        
        return "\n".join(lines)
    
    def _generate_summary(
        self, 
        steps: List[TAOStep],
        llm_callable: Callable
    ) -> str:
        """生成步骤摘要"""
        if not steps:
            return ""
        
        prompt = f"""请简要总结以下推理步骤的核心要点（不超过100字）：

"""
        for step in steps[:10]:  # 最多10步
            prompt += f"- {step.step_type}: {step.content[:100]}\n"
        
        try:
            summary = llm_callable(prompt)
            return summary.strip()[:200]
        except Exception as e:
            logger.warning(f"摘要生成失败: {e}")
            return f"已完成 {len(steps)} 步推理"


@dataclass
class ReActConfig:
    """ReAct配置"""
    max_iterations: int = 10              # 最大迭代次数
    max_context_length: int = 8000        # 最大上下文长度
    preserve_recent: int = 3              # 保留的最近步骤数
    enable_context_summary: bool = True     # 启用上下文摘要
    termination_keywords: List[str] = None # 终止关键词
    
    # 熔断配置
    max_consecutive_failures: int = 3     # 最大连续失败次数
    failure_threshold: float = 0.5        # 成功率低于此值时熔断
    
    def __post_init__(self):
        if self.termination_keywords is None:
            self.termination_keywords = [
                "最终答案", "综上所述", "结论是", "答案是",
                "问题已解决", "完成", "完毕"
            ]


class ReActEngine:
    """
    ReAct推理引擎
    
    实现推理与行动的协同框架，支持TAO闭环机制。
    """
    
    VERSION = "6.2.0"
    
    def __init__(
        self,
        llm_callable: Optional[Callable[[str], str]] = None,
        config: Optional[ReActConfig] = None,
        tools: Optional[List[Tool]] = None
    ):
        """
        初始化ReAct引擎
        
        Args:
            llm_callable: LLM调用函数（可选，未提供时使用模拟函数）
            config: ReAct配置
            tools: 初始工具列表
        """
        self.config = config or ReActConfig()
        
        # 如果未提供LLM调用函数，使用默认模拟函数
        if llm_callable is None:
            def _mock_llm(prompt: str) -> str:
                return f"[模拟推理] 基于问题分析: {prompt[:50]}..."
            llm_callable = _mock_llm
        
        self.llm_callable = llm_callable
        
        # 初始化组件
        self.registry = ToolRegistry()
        self.executor = ToolExecutor(self.registry)
        self.thought_generator = ThoughtGenerator(llm_callable)
        self.context_manager = ContextManager(
            max_context_length=self.config.max_context_length,
            preserve_recent=self.config.preserve_recent,
            summary_enabled=self.config.enable_context_summary
        )
        
        # 注册初始工具
        if tools:
            for tool in tools:
                self.registry.register(tool)
        
        # 推理状态
        self._is_running = False
        self._run_lock = threading.Lock()
        
        # 统计
        self.stats = {
            'total_runs': 0,
            'successful_runs': 0,
            'average_iterations': 0,
            'total_actions': 0,
            'tool_usage': {}
        }
        
        logger.info(f"ReActEngine v{self.VERSION} 初始化完成")
        logger.info(f"  - 最大迭代: {self.config.max_iterations}")
        logger.info(f"  - 注册工具数: {len(self.registry.list_tools())}")
    
    def register_tool(self, tool: Tool) -> bool:
        """注册工具"""
        return self.registry.register(tool)
    
    def register_tools(self, tools: List[Tool]) -> int:
        """批量注册工具"""
        count = 0
        for tool in tools:
            if self.registry.register(tool):
                count += 1
        return count
    
    def reason(
        self,
        problem: str,
        context: Optional[Dict[str, Any]] = None,
        llm_callable: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        执行ReAct推理
        
        Args:
            problem: 问题描述
            context: 额外上下文
            llm_callable: LLM调用函数
            
        Returns:
            Dict包含:
            - trajectory: TAOTrajectory 完整轨迹
            - final_answer: str 最终答案
            - success: bool 是否成功
            - metadata: Dict 元数据
        """
        with self._run_lock:
            self._is_running = True
        
        try:
            llm = llm_callable or self.llm_callable
            
            # 创建轨迹
            trajectory = TAOTrajectory(
                trajectory_id=str(uuid.uuid4()),
                problem=problem
            )
            
            # 获取可用工具
            available_tools = [t['name'] for t in self.registry.list_tools()]
            
            # 熔断状态
            consecutive_failures = 0
            
            # 推理循环
            final_answer = None
            start_time = time.time()
            
            for iteration in range(self.config.max_iterations):
                # 生成思考和行动
                thought, action = self.thought_generator.generate(
                    problem,
                    trajectory,
                    available_tools
                )
                
                # 添加思考步骤
                trajectory.add_thought(thought)
                
                # 检查终止条件
                if self._check_termination(thought):
                    trajectory.status = "completed"
                    trajectory.completed_at = datetime.now().isoformat()
                    final_answer = thought
                    break
                
                # 执行行动
                if action:
                    action_result = self._execute_action(action)
                    
                    if action_result.success:
                        consecutive_failures = 0
                        trajectory.add_observation(
                            f"工具 {action['tool']} 执行成功",
                            action_result
                        )
                        self._update_tool_stats(action['tool'], True)
                    else:
                        consecutive_failures += 1
                        trajectory.add_observation(
                            f"工具 {action['tool']} 执行失败: {action_result.error}",
                            action_result
                        )
                        self._update_tool_stats(action['tool'], False)
                        
                        # 检查熔断
                        if consecutive_failures >= self.config.max_consecutive_failures:
                            trajectory.status = "failed"
                            trajectory.completed_at = datetime.now().isoformat()
                            final_answer = "连续执行失败，推理终止"
                            break
                else:
                    # 无行动，检查是否有结论
                    if self._has_conclusion(thought):
                        final_answer = self._extract_answer(thought)
                        trajectory.status = "completed"
                        trajectory.completed_at = datetime.now().isoformat()
                        break
                
                # 管理上下文
                trajectory_str = self.context_manager.manage(
                    trajectory,
                    llm if self.config.enable_context_summary else None
                )
            
            else:
                # 达到最大迭代
                trajectory.status = "timeout"
                trajectory.completed_at = datetime.now().isoformat()
                if not final_answer:
                    final_answer = "达到最大迭代次数，未得出明确结论"
            
            # 更新统计
            self._update_stats(trajectory, time.time() - start_time)
            
            return {
                'trajectory': trajectory,
                'final_answer': final_answer or "无结论",
                'success': trajectory.status == "completed",
                'metadata': {
                    'engine_version': self.VERSION,
                    'problem': problem[:100],
                    'iterations': len(trajectory.steps),
                    'status': trajectory.status,
                    'total_actions': trajectory.total_actions,
                    'execution_time': time.time() - start_time
                }
            }
            
        finally:
            with self._run_lock:
                self._is_running = False
    
    def _execute_action(self, action: Dict[str, Any]) -> ToolResult:
        """执行行动"""
        tool_name = action.get('tool')
        params = action.get('params', {})
        
        if not self.registry.has_tool(tool_name):
            return ToolResult(
                tool_name=tool_name,
                success=False,
                result=None,
                error=f"工具不存在: {tool_name}"
            )
        
        return self.executor.execute(tool_name, params)
    
    def _check_termination(self, thought: str) -> bool:
        """检查终止条件"""
        for keyword in self.config.termination_keywords:
            if keyword in thought:
                return True
        return False
    
    def _has_conclusion(self, content: str) -> bool:
        """检查是否有结论"""
        conclusion_markers = [
            "因此", "所以", "结论是", "答案是", "最终",
            "综上所述", "问题已解决"
        ]
        return any(marker in content for marker in conclusion_markers)
    
    def _extract_answer(self, content: str) -> str:
        """提取答案"""
        # 尝试提取答案部分
        for marker in ["因此", "结论是", "答案是"]:
            if marker in content:
                idx = content.index(marker)
                return content[idx:].strip()[:500]
        
        return content.strip()[-500:] if len(content) > 500 else content.strip()
    
    def _update_tool_stats(self, tool_name: str, success: bool):
        """更新工具统计"""
        if tool_name not in self.stats['tool_usage']:
            self.stats['tool_usage'][tool_name] = {'success': 0, 'failure': 0}
        
        if success:
            self.stats['tool_usage'][tool_name]['success'] += 1
        else:
            self.stats['tool_usage'][tool_name]['failure'] += 1
    
    def _update_stats(self, trajectory: TAOTrajectory, execution_time: float):
        """更新统计"""
        self.stats['total_runs'] += 1
        
        if trajectory.status == "completed":
            self.stats['successful_runs'] += 1
        
        # 计算平均迭代
        n = self.stats['total_runs']
        current_avg = self.stats['average_iterations']
        iterations = len(trajectory.steps)
        self.stats['average_iterations'] = (
            (current_avg * (n - 1) + iterations) / n
        )
        
        self.stats['total_actions'] += trajectory.total_actions
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            **self.stats,
            'is_running': self._is_running,
            'available_tools': [t['name'] for t in self.registry.list_tools()],
            'executor_stats': self.executor.get_stats()
        }
    
    def reset_stats(self):
        """重置统计"""
        self.stats = {
            'total_runs': 0,
            'successful_runs': 0,
            'average_iterations': 0,
            'total_actions': 0,
            'tool_usage': {}
        }


# 全局单例
_engine_instance: Optional[ReActEngine] = None
_instance_lock = threading.Lock()


def get_react_engine(
    llm_callable: Callable[[str], str],
    config: Optional[ReActConfig] = None,
    tools: Optional[List[Tool]] = None
) -> ReActEngine:
    """获取ReAct引擎单例"""
    global _engine_instance
    
    with _instance_lock:
        if _engine_instance is None:
            _engine_instance = ReActEngine(llm_callable, config, tools)
        return _engine_instance


def create_react_engine(
    llm_callable: Callable[[str], str],
    config: Optional[ReActConfig] = None,
    tools: Optional[List[Tool]] = None
) -> ReActEngine:
    """创建新的ReAct引擎实例"""
    return ReActEngine(llm_callable, config, tools)


# 便捷函数
def reason_with_react(
    problem: str,
    llm_callable: Callable[[str], str],
    tools: Optional[List[Tool]] = None,
    max_iterations: int = 10
) -> Dict[str, Any]:
    """
    使用ReAct进行推理的便捷函数
    
    Example:
        result = reason_with_react(
            problem="北京今天的天气如何？适合户外活动吗？",
            llm_callable=lambda p: openai.ChatCompletion.create(messages=[{"role": "user", "content": p}]),
            tools=[SearchTool(search_func=my_search)],
            max_iterations=10
        )
    """
    config = ReActConfig(max_iterations=max_iterations)
    engine = create_react_engine(llm_callable, config, tools)
    return engine.reason(problem)


__all__ = [
    'ReActEngine',
    'Tool',
    'ToolRegistry',
    'ToolExecutor',
    'ThoughtGenerator',
    'ContextManager',
    'SearchTool',
    'CalculatorTool',
    'LookupTool',
    'RetrieveTool',
    'ToolResult',
    'TAOStep',
    'TAOTrajectory',
    'ReActConfig',
    'ActionType',
    'get_react_engine',
    'create_react_engine',
    'reason_with_react',
]
