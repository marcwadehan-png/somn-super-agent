"""
知识格子推理增强器
==================
将知识格子系统与Somn核心推理引擎集成

功能：
- 推理前自动激活相关格子
- 推理后方法论检查
- 知识图谱与推理链融合
- 举一反三自动注入

集成点：
- reasoning/reasoning_memory.py
- neural_memory/knowledge_engine.py
- intelligence/reasoning/*.py
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from functools import wraps

# 延迟导入避免循环依赖
_knowledge_system = None
_method_checker = None


def get_knowledge_system():
    """获取知识系统单例"""
    global _knowledge_system
    if _knowledge_system is None:
        try:
            from knowledge_cells import get_knowledge_system as _get
            _knowledge_system = _get()
        except ImportError:
            return None
    return _knowledge_system


def get_method_checker():
    """获取方法论检查器"""
    global _method_checker
    if _method_checker is None:
        try:
            from knowledge_cells.method_checker import get_method_checker as _get
            _method_checker = _get()
        except ImportError:
            return None
    return _method_checker


class ReasoningEnhancer:
    """
    推理增强器
    在推理过程中注入知识格子能力
    """
    
    def __init__(self):
        self.system = get_knowledge_system()
        self.checker = get_method_checker()
        self._enabled = self.system is not None
    
    @property
    def enabled(self) -> bool:
        """是否启用"""
        return self._enabled
    
    def pre_reasoning_hook(self, question: str, context: str = "") -> Dict[str, Any]:
        """
        推理前钩子 - 准备相关知识
        
        Args:
            question: 问题
            context: 上下文
            
        Returns:
            包含准备好的知识的字典
        """
        if not self.enabled:
            return {"enabled": False}
        
        result = {
            "enabled": True,
            "question": question,
        }
        
        # 查询相关格子
        try:
            query_result = self.system.query(question, context)
            result["cells_to_use"] = query_result["cells_used"]
            result["frameworks"] = query_result["frameworks"]
            result["analogies"] = query_result["analogies"]
            result["knowledge_hint"] = query_result["answer"]
            
            # 激活使用的格子
            for cell_id in query_result["cells_used"]:
                self.system.engine.activate_cell(cell_id)
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def post_reasoning_hook(self, reasoning_result: str, context: str = "") -> Dict[str, Any]:
        """
        推理后钩子 - 方法论检查
        
        Args:
            reasoning_result: 推理结果
            context: 上下文
            
        Returns:
            检查结果字典
        """
        if not self.enabled or not self.checker:
            return {"enabled": False}
        
        result = {
            "enabled": True,
        }
        
        try:
            check_result = self.checker.full_check(reasoning_result, context)
            result["methodology"] = check_result
            
            # 如果评分低于阈值，添加改进建议
            if check_result["overall_score"] < 70:
                result["improvement_needed"] = True
                result["suggestions"] = check_result["suggestions"]
            else:
                result["improvement_needed"] = False
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def enhance_reasoning(self, question: str, reasoning_func: Callable, 
                         context: str = "") -> Dict[str, Any]:
        """
        增强推理 - 前后钩子合一
        
        Args:
            question: 问题
            reasoning_func: 推理函数 (接收 question, context)
            context: 上下文
            
        Returns:
            增强后的结果
        """
        result = {
            "question": question,
        }
        
        # 推理前准备
        pre = self.pre_reasoning_hook(question, context)
        result["preparation"] = pre
        
        # 执行推理
        try:
            reasoning_output = reasoning_func(question, context)
            result["reasoning"] = reasoning_output
        except Exception as e:
            result["reasoning_error"] = str(e)
            return result
        
        # 推理后检查
        if isinstance(reasoning_output, str):
            post = self.post_reasoning_hook(reasoning_output, context)
            result["methodology_check"] = post
            
            # 如果需要改进，添加知识格子建议
            if post.get("improvement_needed"):
                result["knowledge_suggestions"] = self._get_knowledge_suggestions(
                    question, post["suggestions"]
                )
        
        return result
    
    def _get_knowledge_suggestions(self, question: str, 
                                  suggestions: List[str]) -> Dict[str, Any]:
        """获取知识建议"""
        if not self.enabled:
            return {"enabled": False}
        
        suggestions_result = {
            "question": question,
            "related_cells": [],
            "frameworks": [],
        }
        
        try:
            # 搜索相关格子
            cells = self.system.search_cells(question)
            suggestions_result["related_cells"] = [
                {"cell_id": c["cell_id"], "name": c["name"]}
                for c in cells[:5]
            ]
            
            # 推荐框架
            hot_cells = self.system.get_hot_cells(5)
            suggestions_result["frameworks"] = [
                {"cell_id": c["cell_id"], "name": c["name"]}
                for c in hot_cells
            ]
        except Exception:
            pass
        
        return suggestions_result
    
    def inject_analogies(self, content: str, max_count: int = 2) -> str:
        """
        自动注入举一反三
        
        Args:
            content: 原内容
            max_count: 最大注入数量
            
        Returns:
            注入后的内容
        """
        if not self.enabled:
            return content
        
        # 查找可能相关的格子
        try:
            cells = self.system.search_cells(content[:100])
            analogies = []
            
            for cell in cells[:max_count]:
                analogy = self.system.engine.get_analogy(cell["cell_id"])
                if analogy:
                    analogies.append(f"【举一反三】{analogy}")
            
            if analogies:
                content += "\n\n" + "\n".join(analogies)
        except Exception:
            pass
        
        return content
    
    def get_reasoning_context(self, question: str) -> Dict[str, Any]:
        """
        获取推理上下文 - 用于增强提示词
        
        Args:
            question: 问题
            
        Returns:
            上下文字典
        """
        if not self.enabled:
            return {"enabled": False}
        
        context = {
            "enabled": True,
            "system_prompt_addition": "",
        }
        
        try:
            # 获取相关格子
            cells = self.system.search_cells(question)
            
            if cells:
                cell_names = [c["name"] for c in cells[:3]]
                context["relevant_knowledge"] = cell_names
                
                # 构建提示词补充
                prompt_parts = [
                    "【相关知识域】",
                    f"建议参考以下知识格子: {', '.join(cell_names)}",
                ]
                
                # 获取推荐框架
                for cell in cells[:2]:
                    analogy = self.system.engine.get_analogy(cell["cell_id"])
                    if analogy:
                        prompt_parts.append(f"举一反三: {analogy}")
                        break
                
                context["system_prompt_addition"] = "\n".join(prompt_parts)
        except Exception:
            pass
        
        return context


# 全局实例
_enhancer: Optional[ReasoningEnhancer] = None


def get_reasoning_enhancer() -> ReasoningEnhancer:
    """获取推理增强器单例"""
    global _enhancer
    if _enhancer is None:
        _enhancer = ReasoningEnhancer()
    return _enhancer


def enhance_reasoning_hook(reasoning_func: Callable) -> Callable:
    """
    装饰器 - 自动增强推理函数
    
    用法:
        @enhance_reasoning_hook
        def my_reasoning(question, context):
            return do_reasoning(question, context)
    """
    @wraps(reasoning_func)
    def wrapper(question: str, context: str = "", **kwargs):
        enhancer = get_reasoning_enhancer()
        
        if enhancer.enabled:
            # 推理前
            pre = enhancer.pre_reasoning_hook(question, context)
            
            # 执行推理
            result = reasoning_func(question, context, **kwargs)
            
            # 推理后
            post = enhancer.post_reasoning_hook(str(result), context)
            
            return {
                "result": result,
                "preparation": pre,
                "methodology": post,
            }
        else:
            return reasoning_func(question, context, **kwargs)
    
    return wrapper


class WisdomSchedulerIntegration:
    """
    智慧调度器集成
    将知识格子与智慧学派调度集成
    """
    
    # 格子与学派的映射
    CELL_TO_SCHOOLS = {
        "A1": ["logic", "analytic"],
        "A2": ["philosophy", "holistic"],
        "A3": ["academic"],
        "A4": ["practical", "strategic"],
        "A5": ["systems"],
        "A6": ["practical"],
        "A7": ["intuitive"],
        "A8": ["evolutionary"],
        "B1": ["practical", "strategic"],
        "B2": ["practical"],
        "B3": ["practical", "relational"],
        "C2": ["analytic", "data-driven"],
    }
    
    @classmethod
    def get_schools_for_cells(cls, cells: List[str]) -> List[str]:
        """根据格子获取应激活的学派"""
        schools = set()
        for cell in cells:
            if cell in cls.CELL_TO_SCHOOLS:
                schools.update(cls.CELL_TO_SCHOOLS[cell])
        return list(schools)
    
    @classmethod
    def enhance_wisdom_dispatch(cls, question: str, 
                               dispatch_func: Callable) -> Dict[str, Any]:
        """
        增强智慧调度
        
        Args:
            question: 问题
            dispatch_func: 原调度函数
            
        Returns:
            增强后的调度结果
        """
        enhancer = get_reasoning_enhancer()
        
        result = {
            "question": question,
        }
        
        if enhancer.enabled:
            # 获取相关格子
            pre = enhancer.pre_reasoning_hook(question)
            result["relevant_cells"] = pre.get("cells_to_use", [])
            
            # 获取应激活的学派
            if result["relevant_cells"]:
                result["recommended_schools"] = cls.get_schools_for_cells(
                    result["relevant_cells"]
                )
        else:
            result["relevant_cells"] = []
            result["recommended_schools"] = []
        
        # 执行原调度
        try:
            dispatch_result = dispatch_func(question)
            result["dispatch"] = dispatch_result
        except Exception as e:
            result["dispatch_error"] = str(e)
        
        return result


def create_reasoning_context(question: str, context: str = "") -> str:
    """
    快捷函数 - 创建增强的推理上下文
    
    Args:
        question: 问题
        context: 上下文
        
    Returns:
        增强后的提示词
    """
    enhancer = get_reasoning_enhancer()
    
    if not enhancer.enabled:
        return ""
    
    ctx = enhancer.get_reasoning_context(question)
    return ctx.get("system_prompt_addition", "")


# 导出
__all__ = [
    "ReasoningEnhancer",
    "get_reasoning_enhancer",
    "enhance_reasoning_hook",
    "WisdomSchedulerIntegration",
    "create_reasoning_context",
]
