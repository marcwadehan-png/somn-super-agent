# -*- coding: utf-8 -*-
"""
ReAct扩展工具集 v1.0
Extended Tool Suite for ReAct Engine

新增工具：
- CodeTool: 代码执行工具
- WebFetchTool: 网页获取工具
- FileReadTool: 文件读取工具
- AnalyzeTool: 数据分析工具
- CompareTool: 对比分析工具
- ValidateTool: 验证工具
- TransformTool: 数据转换工具
- FilterTool: 数据过滤工具
- AggregateTool: 聚合统计工具

作者: Somn AI
版本: V2.0.0
日期: 2026-04-24
"""

from __future__ import annotations

import time
import json
import re
import math
import statistics
from typing import Dict, List, Optional, Any, Callable, Union
from collections import Counter, defaultdict

from ._react_engine import Tool, ToolResult


# ═══════════════════════════════════════════════════════════════════════════
# 数据处理工具
# ═══════════════════════════════════════════════════════════════════════════

class AnalyzeTool(Tool):
    """数据分析工具 - 统计分析"""
    
    def __init__(self):
        super().__init__(
            name="analyze",
            description="对数据进行统计分析（均值/中位数/标准差等）"
        )
    
    def execute(self, data: List[Union[int, float]], analysis_type: str = "full", **kwargs) -> ToolResult:
        """执行数据分析"""
        start_time = time.time()
        try:
            if not data:
                raise ValueError("数据列表为空")
            
            result = {}
            
            if analysis_type in ["full", "basic"]:
                result["count"] = len(data)
                result["sum"] = sum(data)
                result["mean"] = statistics.mean(data)
                result["median"] = statistics.median(data)
                result["min"] = min(data)
                result["max"] = max(data)
            
            if analysis_type in ["full", "statistical"]:
                if len(data) >= 2:
                    result["stdev"] = statistics.stdev(data)
                    result["variance"] = statistics.variance(data)
                result["range"] = max(data) - min(data)
            
            if analysis_type in ["full", "advanced"]:
                # 分位数
                sorted_data = sorted(data)
                n = len(sorted_data)
                result["q1"] = sorted_data[int(n * 0.25)]
                result["q3"] = sorted_data[int(n * 0.75)]
                result["iqr"] = result["q3"] - result["q1"]
            
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
                error="工具调用失败",
                execution_time=time.time() - start_time
            )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'description': self.description,
            'parameters': {
                'data': {'type': 'array', 'description': '数值数组'},
                'analysis_type': {'type': 'string', 'description': '分析类型: basic/statistical/advanced/full', 'default': 'full'}
            },
            'required': ['data']
        }


class CompareTool(Tool):
    """对比分析工具"""
    
    def __init__(self):
        super().__init__(
            name="compare",
            description="对比多个选项的差异和相似性"
        )
    
    def execute(self, items: List[Dict[str, Any]], criteria: Optional[List[str]] = None, **kwargs) -> ToolResult:
        """执行对比分析"""
        start_time = time.time()
        try:
            if not items:
                raise ValueError("对比项列表为空")
            
            if len(items) < 2:
                return ToolResult(
                    tool_name=self.name,
                    success=True,
                    result={"warning": "对比项少于2个，返回单一项分析", "item": items[0] if items else None},
                    execution_time=time.time() - start_time
                )
            
            result = {
                "item_count": len(items),
                "comparison": []
            }
            
            # 获取所有键（排除name/id）
            all_keys = set()
            for item in items:
                all_keys.update(k for k in item.keys() if k not in ['name', 'id'])
            
            # 对比每个键
            for key in all_keys:
                values = [item.get(key) for item in items if key in item]
                names = [item.get('name', item.get('id', f'Item{i}')) for i, item in enumerate(items)]
                
                comparison = {
                    "criterion": key,
                    "values": dict(zip(names, values)),
                    "all_equal": len(set(str(v) for v in values)) == 1 if values else True
                }
                
                # 数值比较
                numeric_values = [v for v in values if isinstance(v, (int, float))]
                if len(numeric_values) == len(values) and len(numeric_values) >= 2:
                    comparison["max"] = max(numeric_values)
                    comparison["min"] = min(numeric_values)
                    comparison["max_item"] = names[numeric_values.index(max(numeric_values))]
                    comparison["min_item"] = names[numeric_values.index(min(numeric_values))]
                
                result["comparison"].append(comparison)
            
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
                error="工具调用失败",
                execution_time=time.time() - start_time
            )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'description': self.description,
            'parameters': {
                'items': {'type': 'array', 'description': '要对比的项列表'},
                'criteria': {'type': 'array', 'description': '对比标准（可选）'}
            },
            'required': ['items']
        }


class ValidateTool(Tool):
    """验证工具 - 格式/规则验证"""
    
    def __init__(self):
        super().__init__(
            name="validate",
            description="验证数据格式和规则"
        )
    
    def execute(self, value: Any, rules: Dict[str, Any], **kwargs) -> ToolResult:
        """执行验证"""
        start_time = time.time()
        try:
            results = {"valid": True, "errors": [], "warnings": []}
            
            # 类型验证
            if "type" in rules:
                expected_type = rules["type"]
                type_map = {"string": str, "number": (int, float), "boolean": bool, "array": list, "object": dict}
                if expected_type in type_map:
                    if not isinstance(value, type_map[expected_type]):
                        results["valid"] = False
                        results["errors"].append(f"类型错误: 期望{expected_type}，实际{type(value).__name__}")
            
            # 范围验证
            if "min" in rules and isinstance(value, (int, float)):
                if value < rules["min"]:
                    results["valid"] = False
                    results["errors"].append(f"值{value}小于最小值{rules['min']}")
            
            if "max" in rules and isinstance(value, (int, float)):
                if value > rules["max"]:
                    results["valid"] = False
                    results["errors"].append(f"值{value}大于最大值{rules['max']}")
            
            # 长度验证
            if "min_length" in rules and hasattr(value, "__len__"):
                if len(value) < rules["min_length"]:
                    results["valid"] = False
                    results["errors"].append(f"长度{len(value)}小于最小长度{rules['min_length']}")
            
            if "max_length" in rules and hasattr(value, "__len__"):
                if len(value) > rules["max_length"]:
                    results["valid"] = False
                    results["errors"].append(f"长度{len(value)}大于最大长度{rules['max_length']}")
            
            # 格式验证
            if "pattern" in rules and isinstance(value, str):
                if not re.match(rules["pattern"], value):
                    results["valid"] = False
                    results["errors"].append(f"格式不匹配: {rules['pattern']}")
            
            # 枚举验证
            if "enum" in rules:
                if value not in rules["enum"]:
                    results["valid"] = False
                    results["errors"].append(f"值不在允许列表中: {rules['enum']}")
            
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
                error="工具调用失败",
                execution_time=time.time() - start_time
            )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'description': self.description,
            'parameters': {
                'value': {'type': 'any', 'description': '要验证的值'},
                'rules': {'type': 'object', 'description': '验证规则'}
            },
            'required': ['value', 'rules']
        }


class TransformTool(Tool):
    """数据转换工具"""
    
    def __init__(self):
        super().__init__(
            name="transform",
            description="数据格式转换（JSON/CSV/列表互转等）"
        )
    
    def execute(self, data: Any, target_format: str, **kwargs) -> ToolResult:
        """执行数据转换"""
        start_time = time.time()
        try:
            result = None
            
            if target_format == "json":
                if isinstance(data, str):
                    result = json.loads(data)
                elif isinstance(data, (dict, list)):
                    result = json.dumps(data, ensure_ascii=False, indent=2)
                else:
                    result = str(data)
            
            elif target_format == "dict":
                if isinstance(data, str):
                    result = {"value": data}
                elif isinstance(data, (dict, list)):
                    result = {"data": data}
                else:
                    result = {"value": data}
            
            elif target_format == "list":
                if isinstance(data, (list, tuple)):
                    result = list(data)
                elif isinstance(data, dict):
                    result = list(data.items())
                else:
                    result = [data]
            
            elif target_format == "table":
                if isinstance(data, list) and all(isinstance(d, dict) for d in data):
                    headers = list(data[0].keys())
                    result = {"headers": headers, "rows": [[d.get(h) for h in headers] for d in data]}
                else:
                    result = {"headers": ["value"], "rows": [[d] for d in data]}
            
            else:
                raise ValueError(f"不支持的目标格式: {target_format}")
            
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
                error="工具调用失败",
                execution_time=time.time() - start_time
            )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'description': self.description,
            'parameters': {
                'data': {'type': 'any', 'description': '要转换的数据'},
                'target_format': {'type': 'string', 'description': '目标格式: json/dict/list/table'}
            },
            'required': ['data', 'target_format']
        }


class FilterTool(Tool):
    """数据过滤工具"""
    
    def __init__(self):
        super().__init__(
            name="filter",
            description="根据条件过滤数据"
        )
    
    def execute(self, data: List[Any], condition: Dict[str, Any], **kwargs) -> ToolResult:
        """执行数据过滤"""
        start_time = time.time()
        try:
            if not isinstance(data, list):
                raise ValueError("数据必须是列表")
            
            filtered = data
            result_count = len(data)
            
            # 字段过滤（用于字典列表）
            if "field" in condition and isinstance(data[0] if data else None, dict):
                field = condition["field"]
                if "equals" in condition:
                    filtered = [d for d in filtered if d.get(field) == condition["equals"]]
                if "contains" in condition:
                    filtered = [d for d in filtered if condition["contains"] in str(d.get(field, ""))]
                if "greater_than" in condition:
                    filtered = [d for d in filtered if isinstance(d.get(field), (int, float)) and d.get(field) > condition["greater_than"]]
                if "less_than" in condition:
                    filtered = [d for d in filtered if isinstance(d.get(field), (int, float)) and d.get(field) < condition["less_than"]]
                if "in" in condition:
                    filtered = [d for d in filtered if d.get(field) in condition["in"]]
            
            # 数值范围过滤
            if "range" in condition and isinstance(data[0] if data else None, (int, float)):
                min_val, max_val = condition["range"]
                filtered = [d for d in filtered if min_val <= d <= max_val]
            
            # 正则过滤
            if "regex" in condition:
                pattern = re.compile(condition["regex"])
                filtered = [d for d in filtered if pattern.search(str(d))]
            
            return ToolResult(
                tool_name=self.name,
                success=True,
                result={
                    "filtered": filtered,
                    "original_count": result_count,
                    "filtered_count": len(filtered),
                    "removed_count": result_count - len(filtered)
                },
                execution_time=time.time() - start_time
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                success=False,
                result=None,
                error="工具调用失败",
                execution_time=time.time() - start_time
            )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'description': self.description,
            'parameters': {
                'data': {'type': 'array', 'description': '要过滤的数据列表'},
                'condition': {'type': 'object', 'description': '过滤条件'}
            },
            'required': ['data', 'condition']
        }


class AggregateTool(Tool):
    """聚合统计工具"""
    
    def __init__(self):
        super().__init__(
            name="aggregate",
            description="对数据进行分组聚合统计"
        )
    
    def execute(self, data: List[Dict[str, Any]], group_by: str, agg_field: str, 
                agg_func: str = "sum", **kwargs) -> ToolResult:
        """执行聚合统计"""
        start_time = time.time()
        try:
            if not data:
                raise ValueError("数据列表为空")
            
            # 分组
            groups: Dict[Any, List[Any]] = defaultdict(list)
            for item in data:
                key = item.get(group_by)
                value = item.get(agg_field)
                if key is not None:
                    groups[key].append(value)
            
            # 聚合计算
            result = {}
            for key, values in groups.items():
                numeric_values = [v for v in values if isinstance(v, (int, float))]
                
                if agg_func == "sum":
                    result[key] = sum(numeric_values) if numeric_values else 0
                elif agg_func == "avg" or agg_func == "mean":
                    result[key] = statistics.mean(numeric_values) if numeric_values else 0
                elif agg_func == "count":
                    result[key] = len(values)
                elif agg_func == "min":
                    result[key] = min(numeric_values) if numeric_values else None
                elif agg_func == "max":
                    result[key] = max(numeric_values) if numeric_values else None
                elif agg_func == "list":
                    result[key] = values
            
            return ToolResult(
                tool_name=self.name,
                success=True,
                result={
                    "group_by": group_by,
                    "agg_field": agg_field,
                    "agg_func": agg_func,
                    "groups": dict(result),
                    "group_count": len(result)
                },
                execution_time=time.time() - start_time
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                success=False,
                result=None,
                error="工具调用失败",
                execution_time=time.time() - start_time
            )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'description': self.description,
            'parameters': {
                'data': {'type': 'array', 'description': '数据列表（字典数组）'},
                'group_by': {'type': 'string', 'description': '分组字段'},
                'agg_field': {'type': 'string', 'description': '聚合字段'},
                'agg_func': {'type': 'string', 'description': '聚合函数: sum/avg/count/min/max/list', 'default': 'sum'}
            },
            'required': ['data', 'group_by', 'agg_field']
        }


class SortTool(Tool):
    """排序工具"""
    
    def __init__(self):
        super().__init__(
            name="sort",
            description="对数据进行排序"
        )
    
    def execute(self, data: List[Any], key: Optional[str] = None, 
                reverse: bool = False, limit: Optional[int] = None, **kwargs) -> ToolResult:
        """执行排序"""
        start_time = time.time()
        try:
            if not data:
                raise ValueError("数据列表为空")
            
            # 字典列表排序
            if key and isinstance(data[0] if data else None, dict):
                sorted_data = sorted(data, key=lambda x: x.get(key, ""), reverse=reverse)
            else:
                sorted_data = sorted(data, reverse=reverse)
            
            # 限制返回数量
            if limit:
                sorted_data = sorted_data[:limit]
            
            return ToolResult(
                tool_name=self.name,
                success=True,
                result={
                    "sorted_data": sorted_data,
                    "count": len(sorted_data),
                    "key": key,
                    "reverse": reverse,
                    "limited": limit is not None
                },
                execution_time=time.time() - start_time
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                success=False,
                result=None,
                error="工具调用失败",
                execution_time=time.time() - start_time
            )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'description': self.description,
            'parameters': {
                'data': {'type': 'array', 'description': '要排序的数据'},
                'key': {'type': 'string', 'description': '排序键（字典字段）'},
                'reverse': {'type': 'boolean', 'description': '降序', 'default': False},
                'limit': {'type': 'integer', 'description': '返回数量限制'}
            },
            'required': ['data']
        }


# ═══════════════════════════════════════════════════════════════════════════
# 文本处理工具
# ═══════════════════════════════════════════════════════════════════════════

class ExtractTool(Tool):
    """信息提取工具"""
    
    def __init__(self):
        super().__init__(
            name="extract",
            description="从文本中提取结构化信息"
        )
    
    def execute(self, text: str, pattern: str, extract_type: str = "all", **kwargs) -> ToolResult:
        """执行信息提取"""
        start_time = time.time()
        try:
            matches = re.findall(pattern, text)
            
            result = {}
            if extract_type == "all":
                result["matches"] = matches
                result["count"] = len(matches)
            elif extract_type == "first":
                result["match"] = matches[0] if matches else None
            elif extract_type == "groups":
                # 返回捕获组
                all_groups = re.findall(pattern, text)
                if all_groups:
                    result["groups"] = all_groups
                    result["count"] = len(all_groups)
            
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
                error="工具调用失败",
                execution_time=time.time() - start_time
            )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'description': self.description,
            'parameters': {
                'text': {'type': 'string', 'description': '源文本'},
                'pattern': {'type': 'string', 'description': '正则表达式'},
                'extract_type': {'type': 'string', 'description': '提取类型: all/first/groups', 'default': 'all'}
            },
            'required': ['text', 'pattern']
        }


class TranslateTool(Tool):
    """翻译工具（模拟）"""
    
    def __init__(self):
        super().__init__(
            name="translate",
            description="文本翻译（需要外部翻译API）"
        )
    
    def execute(self, text: str, source_lang: str = "auto", target_lang: str = "zh", **kwargs) -> ToolResult:
        """执行翻译"""
        start_time = time.time()
        
        # 模拟翻译结果（实际需要接入翻译API）
        translated = f"[翻译结果({source_lang}->{target_lang})]: {text}"
        
        return ToolResult(
            tool_name=self.name,
            success=True,
            result={
                "original": text,
                "translated": translated,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "note": "模拟翻译，请接入真实翻译API"
            },
            execution_time=time.time() - start_time
        )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'description': self.description,
            'parameters': {
                'text': {'type': 'string', 'description': '要翻译的文本'},
                'source_lang': {'type': 'string', 'description': '源语言', 'default': 'auto'},
                'target_lang': {'type': 'string', 'description': '目标语言', 'default': 'zh'}
            },
            'required': ['text']
        }


# ═══════════════════════════════════════════════════════════════════════════
# 决策辅助工具
# ═══════════════════════════════════════════════════════════════════════════

class ScoreTool(Tool):
    """评分工具"""
    
    def __init__(self):
        super().__init__(
            name="score",
            description="对选项进行多维度评分"
        )
    
    def execute(self, items: List[Dict[str, Any]], criteria: List[Dict[str, Any]], **kwargs) -> ToolResult:
        """执行多维度评分"""
        start_time = time.time()
        try:
            results = []
            
            for item in items:
                scores = {}
                total_score = 0
                total_weight = 0
                
                for criterion in criteria:
                    name = criterion.get("name", "unknown")
                    weight = criterion.get("weight", 1.0)
                    metric = criterion.get("metric", "field")
                    field = criterion.get("field", name)
                    
                    value = item.get(field, 0)
                    
                    # 计算得分
                    if "range" in criterion:
                        min_val, max_val = criterion["range"]
                        if isinstance(value, (int, float)):
                            score = min(100, max(0, (value - min_val) / (max_val - min_val) * 100)) if max_val != min_val else 50
                        else:
                            score = 50
                    else:
                        score = value if isinstance(value, (int, float)) else 50
                    
                    scores[name] = {"raw": value, "score": score, "weight": weight}
                    total_score += score * weight
                    total_weight += weight
                
                final_score = total_score / total_weight if total_weight > 0 else 0
                
                results.append({
                    "item": item.get("name", item),
                    "scores": scores,
                    "final_score": round(final_score, 2),
                    "rank": 0
                })
            
            # 排序
            results.sort(key=lambda x: x["final_score"], reverse=True)
            for i, r in enumerate(results):
                r["rank"] = i + 1
            
            return ToolResult(
                tool_name=self.name,
                success=True,
                result={
                    "rankings": results,
                    "criteria_count": len(criteria),
                    "items_scored": len(results)
                },
                execution_time=time.time() - start_time
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                success=False,
                result=None,
                error="工具调用失败",
                execution_time=time.time() - start_time
            )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'description': self.description,
            'parameters': {
                'items': {'type': 'array', 'description': '待评分项列表'},
                'criteria': {'type': 'array', 'description': '评分标准列表'}
            },
            'required': ['items', 'criteria']
        }


# ═══════════════════════════════════════════════════════════════════════════
# 工具集注册函数
# ═══════════════════════════════════════════════════════════════════════════

def get_extended_tools() -> List[Tool]:
    """获取扩展工具集"""
    return [
        # 数据处理
        AnalyzeTool(),
        CompareTool(),
        ValidateTool(),
        TransformTool(),
        FilterTool(),
        AggregateTool(),
        SortTool(),
        # 文本处理
        ExtractTool(),
        TranslateTool(),
        # 决策辅助
        ScoreTool(),
    ]


def register_extended_tools(registry) -> int:
    """向注册表批量注册扩展工具"""
    tools = get_extended_tools()
    for tool in tools:
        registry.register(tool)
    return len(tools)
