"""工具注册中心核心类"""

import json
import re
import time
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

from src.core.paths import TOOLS_DIR
from ._tr_enums import ToolCategory, ToolStatus
from ._tr_dataclasses import Tool, ToolParameter

__all__ = [
    'attach_llm_service',
    'describe_tools',
    'execute_tool',
    'get_tool',
    'list_tools',
    'register_tool',
]

class ToolRegistry:
    """工具注册中心"""

    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else TOOLS_DIR
        self.base_path.mkdir(parents=True, exist_ok=True)

        self.tools: Dict[str, Tool] = {}
        self.category_index: Dict[ToolCategory, List[str]] = {c: [] for c in ToolCategory}
        self.llm_service = None

        self._report_engine = None
        self._data_collector = None
        self._chart_generator = None

        self._init_core_tools()

    def attach_llm_service(self, llm_service: Any):
        """挂载 LLM 服务,供 llm_chat / llm_analyze 等工具调用."""
        self.llm_service = llm_service

    def _init_core_tools(self):
        """init核心工具"""
        core_tools = [
            Tool(
                tool_id="llm_chat",
                name="LLM对话",
                category=ToolCategory.LLM,
                description="与本地大语言模型进行对话",
                parameters=[
                    ToolParameter("prompt", "str", "输入提示", required=True),
                    ToolParameter("model", "str", "模型名称", required=False, default="local-default"),
                    ToolParameter("temperature", "float", "温度参数", required=False, default=0.3),
                    ToolParameter("max_tokens", "int", "最大token数", required=False, default=2000),
                    ToolParameter("system_prompt", "str", "系统提示词", required=False, default="")
                ],
                return_type="dict",
                config={"max_retries": 1}
            ),
            Tool(
                tool_id="llm_analyze",
                name="LLM分析",
                category=ToolCategory.LLM,
                description="使用本地 LLM 进行文本分析",
                parameters=[
                    ToolParameter("text", "str", "待分析文本", required=True),
                    ToolParameter(
                        "task",
                        "str",
                        "分析任务",
                        required=True,
                        enum_values=["sentiment", "summary", "keywords", "classification", "growth_insight"]
                    ),
                    ToolParameter("context", "str", "上下文信息", required=False, default=""),
                    ToolParameter("model", "str", "模型名称", required=False, default="local-default")
                ],
                return_type="dict",
                config={"max_retries": 1}
            ),
            Tool(
                tool_id="data_stats",
                name="数据统计",
                category=ToolCategory.DATA_ANALYSIS,
                description="计算数据集的基本统计信息",
                parameters=[
                    ToolParameter("data", "list", "数据集", required=True),
                    ToolParameter("metrics", "list", "统计metrics", required=False, default=["mean", "median", "std", "min", "max", "count"])
                ],
                return_type="dict"
            ),
            Tool(
                tool_id="data_correlation",
                name="相关性分析",
                category=ToolCategory.DATA_ANALYSIS,
                description="分析变量间的相关性",
                parameters=[
                    ToolParameter("x", "list", "变量X", required=True),
                    ToolParameter("y", "list", "变量Y", required=True),
                    ToolParameter("method", "str", "计算方法", required=False, default="pearson", enum_values=["pearson", "spearman", "kendall"])
                ],
                return_type="dict"
            ),
            Tool(
                tool_id="trend_forecast",
                name="趋势预测",
                category=ToolCategory.DATA_ANALYSIS,
                description="基于历史数据进行趋势预测",
                parameters=[
                    ToolParameter("historical_data", "list", "历史数据", required=True),
                    ToolParameter("forecast_periods", "int", "预测期数", required=True),
                    ToolParameter("method", "str", "预测方法", required=False, default="linear", enum_values=["linear", "moving_average", "exponential"])
                ],
                return_type="dict"
            ),
            Tool(
                tool_id="calc_roi",
                name="计算ROI",
                category=ToolCategory.CALCULATION,
                description="计算投资回报率",
                parameters=[
                    ToolParameter("investment", "float", "投资额", required=True),
                    ToolParameter("return_value", "float", "回报额", required=True),
                    ToolParameter("period_months", "int", "周期(月)", required=False, default=12)
                ],
                return_type="dict"
            ),
            Tool(
                tool_id="calc_cac_ltv",
                name="计算CAC和LTV",
                category=ToolCategory.CALCULATION,
                description="计算获客成本和用户终身价值",
                parameters=[
                    ToolParameter("marketing_spend", "float", "营销支出", required=True),
                    ToolParameter("new_customers", "int", "新增客户数", required=True),
                    ToolParameter("avg_revenue_per_customer", "float", "客均收入", required=True),
                    ToolParameter("gross_margin", "float", "毛利率", required=False, default=0.7),
                    ToolParameter("churn_rate", "float", "月流失率", required=True)
                ],
                return_type="dict"
            ),
        ]

        for tool in core_tools:
            self.register_tool(tool)

    def register_tool(self, tool: Tool) -> Tool:
        """注册工具"""
        self.tools[tool.tool_id] = tool
        if tool.tool_id not in self.category_index[tool.category]:
            self.category_index[tool.category].append(tool.tool_id)
        return tool

    def get_tool(self, tool_id: str) -> Optional[Tool]:
        """get工具"""
        return self.tools.get(tool_id)

    def list_tools(self, category: ToolCategory = None, status: ToolStatus = None) -> List[Tool]:
        """列出工具"""
        tool_ids = self.category_index.get(category, []) if category else list(self.tools.keys())
        results: List[Tool] = []
        for tool_id in tool_ids:
            tool = self.tools.get(tool_id)
            if not tool:
                continue
            if status and tool.status != status:
                continue
            results.append(tool)
        return results

    def describe_tools(self) -> List[Dict[str, Any]]:
        """输出适合给规划器使用的工具描述."""
        return [
            {
                "tool_id": tool.tool_id,
                "name": tool.name,
                "category": tool.category.value,
                "description": tool.description,
                "return_type": tool.return_type,
                "parameters": [
                    {
                        "name": param.name,
                        "type": param.param_type,
                        "required": param.required,
                        "description": param.description,
                        "enum": param.enum_values,
                        "default": param.default
                    }
                    for param in tool.parameters
                ]
            }
            for tool in self.list_tools(status=ToolStatus.ACTIVE)
        ]

    def execute_tool(self, tool_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """执行工具"""
        tool = self.tools.get(tool_id)
        if not tool:
            return {"success": False, "error": f"工具不存在: {tool_id}"}

        if tool.status != ToolStatus.ACTIVE:
            return {"success": False, "error": f"工具不可用: {tool.status.value}"}

        normalized = self._normalize_parameters(tool, parameters)
        if not normalized["valid"]:
            return {"success": False, "error": normalized["error"]}

        safe_parameters = normalized["parameters"]
        max_attempts = max(1, int(tool.config.get("max_retries", 0)) + 1)

        for attempt in range(1, max_attempts + 1):
            try:
                if tool.handler:
                    result = tool.handler(**safe_parameters)
                else:
                    result = self._default_handler(tool, safe_parameters)

                tool.call_count += 1
                return {
                    "success": True,
                    "tool_id": tool_id,
                    "result": result,
                    "attempts": attempt,
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as exc:
                if attempt < max_attempts and self._is_retryable_error(exc):
                    threading.Event().wait(0.2 * attempt)
                    continue
                return {
                    "success": False,
                    "error": self._format_exception(exc),
                    "tool_id": tool_id,
                    "attempts": attempt,
                    "timestamp": datetime.now().isoformat()
                }

        return {
            "success": False,
            "error": f"工具执行失败且未捕获明确异常: {tool_id}",
            "tool_id": tool_id,
            "timestamp": datetime.now().isoformat()
        }

    def _normalize_parameters(self, tool: Tool, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """补全默认值,执行参数类型归一化并校验."""
        errors: List[str] = []
        normalized: Dict[str, Any] = {}
        parameter_map = {param.name: param for param in tool.parameters}

        for param in tool.parameters:
            provided = param.name in parameters and self._has_value(parameters.get(param.name))
            if provided:
                raw_value = parameters.get(param.name)
            elif param.required and param.default is None:
                errors.append(f"缺少必需参数: {param.name}")
                continue
            else:
                raw_value = param.default

            try:
                coerced = self._coerce_parameter_value(param, raw_value)
            except ValueError as exc:
                errors.append(str(exc))
                continue

            if param.enum_values:
                coerced = self._normalize_enum_value(param, coerced, errors)
                if errors:
                    continue

            normalized[param.name] = coerced

        for key, value in parameters.items():
            if key not in parameter_map:
                normalized[key] = value

        return {
            "valid": len(errors) == 0,
            "error": "; ".join(errors) if errors else None,
            "parameters": normalized
        }

    def _normalize_enum_value(self, param: ToolParameter, value: Any, errors: List[str]) -> Any:
        """规范化枚举值,支持大小写无关匹配."""
        if value in param.enum_values:
            return value

        if isinstance(value, str):
            lowered = value.lower()
            for enum_value in param.enum_values:
                if isinstance(enum_value, str) and enum_value.lower() == lowered:
                    return enum_value

        errors.append(f"参数 {param.name} 值错误,可选: {param.enum_values}")
        return value

    def _coerce_parameter_value(self, param: ToolParameter, value: Any) -> Any:
        """把 LLM 或外部输入归一化为工具可执行参数."""
        if not self._has_value(value):
            return param.default

        param_type = param.param_type

        if param_type == "any":
            if isinstance(value, str):
                parsed = self._try_parse_json(value)
                return parsed if parsed is not None else value
            return value

        if param_type == "str":
            if isinstance(value, str):
                return value
            if isinstance(value, (dict, list)):
                return json.dumps(value, ensure_ascii=False)
            return str(value)

        if param_type == "int":
            if isinstance(value, bool):
                raise ValueError(f"参数 {param.name} 类型错误,期望 int")
            return int(value)

        if param_type == "float":
            if isinstance(value, bool):
                raise ValueError(f"参数 {param.name} 类型错误,期望 float")
            return float(value)

        if param_type == "bool":
            if isinstance(value, bool):
                return value
            if isinstance(value, (int, float)):
                return bool(value)
            if isinstance(value, str):
                lowered = value.strip().lower()
                if lowered in {"true", "1", "yes", "y", "on"}:
                    return True
                if lowered in {"false", "0", "no", "n", "off"}:
                    return False
            raise ValueError(f"参数 {param.name} 类型错误,期望 bool")

        if param_type == "list":
            if isinstance(value, list):
                return value
            if isinstance(value, tuple):
                return list(value)
            if isinstance(value, str):
                parsed = self._try_parse_json(value)
                if isinstance(parsed, list):
                    return parsed
                split_values = [item.strip() for item in re.split(r"[\n,,]", value) if item.strip()]
                return split_values
            raise ValueError(f"参数 {param.name} 类型错误,期望 list")

        if param_type == "dict":
            if isinstance(value, dict):
                return value
            if isinstance(value, str):
                parsed = self._try_parse_json(value)
                if isinstance(parsed, dict):
                    return parsed
            raise ValueError(f"参数 {param.name} 类型错误,期望 dict")

        raise ValueError(f"不支持的参数类型: {param_type}")

    def _try_parse_json(self, raw_text: str) -> Any:
        """尝试解析 JSON 文本."""
        text = raw_text.strip()
        if not text:
            return None
        if not ((text.startswith("{") and text.endswith("}")) or (text.startswith("[") and text.endswith("]"))):
            return None
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None

    def _has_value(self, value: Any) -> bool:
        """judge参数是否真正提供."""
        if value is None:
            return False
        if isinstance(value, str):
            return value.strip() != ""
        return True

    def _default_handler(self, tool: Tool, parameters: Dict[str, Any]) -> Any:
        """默认工具处理器"""
        handlers = {
            "llm_chat": self._handle_llm_chat,
            "llm_analyze": self._handle_llm_analyze,
            "calc_roi": self._handle_calc_roi,
            "calc_cac_ltv": self._handle_calc_cac_ltv,
            "data_stats": self._handle_data_stats,
            "data_correlation": self._handle_data_correlation,
            "trend_forecast": self._handle_trend_forecast,
        }

        handler = handlers.get(tool.tool_id)
        if handler:
            return handler(parameters)

        return {"message": f"工具 {tool.tool_id} 执行成功", "parameters": parameters}

    def _handle_llm_chat(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理 llm_chat."""
        if self.llm_service is None:
            raise RuntimeError("LLM 服务尚未挂载到工具注册中心")

        response = self.llm_service.chat(
            prompt=params["prompt"],
            model=params.get("model") or self.llm_service.get_default_model(),
            system_prompt=params.get("system_prompt") or None,
            temperature=params.get("temperature", 0.3),
            max_tokens=params.get("max_tokens", 2000)
        )
        return {
            "content": response.content,
            "model": response.model,
            "provider": response.provider,
            "usage": response.usage,
            "finish_reason": response.finish_reason,
            "latency_ms": response.latency_ms
        }

    def _handle_llm_analyze(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理 llm_analyze."""
        if self.llm_service is None:
            raise RuntimeError("LLM 服务尚未挂载到工具注册中心")

        return self.llm_service.analyze(
            text=params["text"],
            task=params["task"],
            context=params.get("context", ""),
            model=params.get("model") or self.llm_service.get_default_model()
        )

    def _handle_calc_roi(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理 ROI 计算"""
        investment = float(params["investment"])
        return_value = float(params["return_value"])
        period = int(params.get("period_months", 12))

        roi = (return_value - investment) / investment if investment > 0 else 0.0
        annualized_roi = (1 + roi) ** (12 / period) - 1 if period > 0 else roi
        payback = round(investment / (return_value / period), 2) if return_value > 0 and period > 0 else None

        return {
            "roi": round(roi, 4),
            "roi_percentage": round(roi * 100, 2),
            "annualized_roi": round(annualized_roi, 4),
            "payback_period_months": payback
        }

    def _handle_calc_cac_ltv(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理 CAC 和 LTV 计算"""
        marketing_spend = float(params["marketing_spend"])
        new_customers = int(params["new_customers"])
        avg_revenue = float(params["avg_revenue_per_customer"])
        gross_margin = float(params.get("gross_margin", 0.7))
        churn_rate = float(params["churn_rate"])

        cac = marketing_spend / new_customers if new_customers > 0 else 0.0
        ltv = (avg_revenue * gross_margin) / churn_rate if churn_rate > 0 else 0.0

        return {
            "cac": round(cac, 2),
            "ltv": round(ltv, 2),
            "ltv_cac_ratio": round(ltv / cac, 2) if cac > 0 else 0.0,
            "months_to_break_even": round(cac / (avg_revenue * gross_margin), 2) if avg_revenue > 0 else 0.0
        }

    def _handle_data_stats(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理数据统计"""
        import numpy as np

        data = params["data"]
        metrics = params.get("metrics", ["mean", "median", "std", "min", "max", "count"])
        if not data:
            raise ValueError("data_stats 需要非空数据集")

        arr = np.array(data, dtype=float)
        result: Dict[str, Any] = {}

        if "mean" in metrics:
            result["mean"] = float(np.mean(arr))
        if "median" in metrics:
            result["median"] = float(np.median(arr))
        if "std" in metrics:
            result["std"] = float(np.std(arr))
        if "min" in metrics:
            result["min"] = float(np.min(arr))
        if "max" in metrics:
            result["max"] = float(np.max(arr))
        if "count" in metrics:
            result["count"] = int(len(arr))

        return result

    def _handle_data_correlation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理相关性分析."""
        import pandas as pd

        x = pd.Series(params["x"], dtype="float64")
        y = pd.Series(params["y"], dtype="float64")
        method = params.get("method", "pearson")

        if len(x) != len(y):
            raise ValueError("x 和 y 的长度必须一致")
        if len(x) < 2:
            raise ValueError("相关性分析至少需要 2 个样本")

        correlation = x.corr(y, method=method)
        if pd.isna(correlation):
            raise ValueError("相关性计算失败,可能是输入常量序列或数据异常")

        abs_corr = abs(float(correlation))
        if abs_corr >= 0.8:
            strength = "强相关"
        elif abs_corr >= 0.5:
            strength = "中等相关"
        elif abs_corr >= 0.3:
            strength = "弱相关"
        else:
            strength = "极弱相关"

        direction = "正相关" if correlation > 0 else "负相关" if correlation < 0 else "无明显相关"
        return {
            "method": method,
            "sample_size": int(len(x)),
            "correlation": round(float(correlation), 6),
            "strength": strength,
            "direction": direction
        }

    def _handle_trend_forecast(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理趋势预测."""
        import numpy as np

        historical = [float(value) for value in params["historical_data"]]
        forecast_periods = int(params["forecast_periods"])
        method = params.get("method", "linear")

        if len(historical) < 2:
            raise ValueError("趋势预测至少需要 2 个历史点")
        if forecast_periods <= 0:
            raise ValueError("forecast_periods 必须大于 0")

        forecast: List[float]
        if method == "linear":
            x = np.arange(len(historical), dtype=float)
            slope, intercept = np.polyfit(x, np.array(historical, dtype=float), 1)
            future_x = np.arange(len(historical), len(historical) + forecast_periods, dtype=float)
            forecast = [round(float(intercept + slope * value), 4) for value in future_x]
            trend_score = float(slope)
        elif method == "moving_average":
            window = min(3, len(historical))
            moving_avg = float(sum(historical[-window:]) / window)
            forecast = [round(moving_avg, 4) for _ in range(forecast_periods)]
            trend_score = moving_avg - float(historical[-1])
        else:
            alpha = 0.4
            level = historical[0]
            for value in historical[1:]:
                level = alpha * value + (1 - alpha) * level
            forecast = [round(float(level), 4) for _ in range(forecast_periods)]
            trend_score = float(level - historical[-1])

        if forecast[-1] > historical[-1]:
            trend_direction = "上升"
        elif forecast[-1] < historical[-1]:
            trend_direction = "下降"
        else:
            trend_direction = "平稳"

        return {
            "method": method,
            "historical_points": len(historical),
            "forecast_periods": forecast_periods,
            "forecast": forecast,
            "trend_direction": trend_direction,
            "trend_score": round(float(trend_score), 6)
        }

    def _format_exception(self, exc: Exception) -> str:
        """标准化错误文本."""
        return f"{type(exc).__name__}: {exc}"

    def _is_retryable_error(self, exc: Exception) -> bool:
        """judge是否值得自动重试."""
        if isinstance(exc, (TimeoutError, ConnectionError, OSError)):
            return True
        message = str(exc).lower()
        retry_keywords = ["timeout", "temporar", "busy", "connection", "reset", "try again"]
        return any(keyword in message for keyword in retry_keywords)
