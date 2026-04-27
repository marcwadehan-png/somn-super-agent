"""
知识格子系统统一接口
====================
提供对知识格子系统的统一访问

使用示例：
    from knowledge_cells import get_knowledge_system
    
    system = get_knowledge_system()
    
    # 知识检索
    result = system.query("如何提升用户增长")
    
    # 方法论检查
    check = system.check_methodology("分析报告...")
    
    # 获取系统状态
    status = system.get_status()
"""

from typing import Dict, List, Optional, Any
import os

# 延迟加载避免循环导入
_system = None


class KnowledgeSystem:
    """知识格子系统统一接口"""
    
    def __init__(self, cells_dir: Optional[str] = None):
        self.cells_dir = cells_dir or os.path.dirname(__file__)
        self._engine = None
        self._fusion = None
        self._checker = None
    
    @property
    def engine(self):
        """知识格子引擎"""
        if self._engine is None:
            from .cell_engine import get_knowledge_engine
            self._engine = get_knowledge_engine(self.cells_dir)
        return self._engine
    
    @property
    def fusion(self):
        """融合引擎"""
        if self._fusion is None:
            from .fusion_engine import get_fusion_engine
            self._fusion = get_fusion_engine(self.engine)
        return self._fusion
    
    @property
    def checker(self):
        """方法论检查器"""
        if self._checker is None:
            from .method_checker import get_method_checker
            self._checker = get_method_checker()
        return self._checker
    
    def query(self, question: str, context: str = "") -> Dict[str, Any]:
        """
        查询知识
        
        Args:
            question: 问题
            context: 上下文
            
        Returns:
            包含回答、相关格子、框架推荐的字典
        """
        # 使用融合引擎
        result = self.fusion.fuse(question, context)
        
        # 激活使用的格子
        for cell_id in result.cells_used:
            self.engine.activate_cell(cell_id)
        
        return {
            "answer": result.answer,
            "cells_used": result.cells_used,
            "frameworks": result.frameworks,
            "analogies": result.analogies,
            "data_points": result.data_points,
            "quality_score": result.quality_score,
            "methodology_check": self.check_methodology(result.answer, context)
        }
    
    def check_methodology(self, response: str, context: str = "") -> Dict[str, Any]:
        """
        方法论检查
        
        Args:
            response: 需要检查的回答
            context: 上下文
            
        Returns:
            检查结果字典
        """
        return self.checker.full_check(response, context)
    
    def get_related_cells(self, cell_id: str, threshold: float = 0.6) -> List[Dict]:
        """
        获取关联格子
        
        Args:
            cell_id: 格子ID
            threshold: 关联阈值
            
        Returns:
            关联格子列表
        """
        cell = self.engine.get_cell(cell_id)
        if not cell:
            return []
        
        related = self.engine.find_related(cell_id, threshold)
        return [
            {"cell_id": c.cell_id, "name": c.name, "weight": w}
            for c, w in related
        ]
    
    def get_cell_content(self, cell_id: str) -> Optional[Dict[str, Any]]:
        """
        获取格子完整内容
        
        Args:
            cell_id: 格子ID
            
        Returns:
            格子内容字典
        """
        cell = self.engine.get_cell(cell_id)
        if not cell:
            return None
        
        return {
            "cell_id": cell.cell_id,
            "name": cell.name,
            "tags": list(cell.tags),
            "associations": cell.associations,
            "activation_count": cell.activation_count,
            "last_activation": cell.last_activation,
            "content": cell.content
        }
    
    def search_cells(self, keyword: str) -> List[Dict]:
        """
        搜索格子
        
        Args:
            keyword: 关键词
            
        Returns:
            匹配的格子列表
        """
        results = self.engine.search_by_content(keyword)
        return [
            {"cell_id": c.cell_id, "name": c.name}
            for c in results
        ]
    
    def get_hot_cells(self, top_n: int = 5) -> List[Dict]:
        """
        获取最热格子
        
        Args:
            top_n: 返回数量
            
        Returns:
            最热格子列表
        """
        cells = self.engine.get_hot_cells(top_n)
        return [
            {"cell_id": c.cell_id, "name": c.name, "activations": c.activation_count}
            for c in cells
        ]
    
    def get_knowledge_graph(self) -> Dict:
        """
        获取知识图谱
        
        Returns:
            知识图谱数据
        """
        return self.engine.get_knowledge_graph()
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取系统状态
        
        Returns:
            系统状态字典
        """
        return {
            "total_cells": len(self.engine.cells),
            "summary": self.engine.summarize(),
            "hot_cells": self.get_hot_cells(5),
            "knowledge_graph_nodes": len(self.engine.cells),
        }
    
    def list_all_cells(self) -> List[Dict]:
        """
        列出所有格子
        
        Returns:
            所有格子列表
        """
        return [
            {"cell_id": cid, "name": c.name, "activations": c.activation_count}
            for cid, c in self.engine.cells.items()
        ]


def get_knowledge_system(cells_dir: Optional[str] = None) -> KnowledgeSystem:
    """
    获取知识系统单例
    
    Args:
        cells_dir: 格子目录路径
        
    Returns:
        KnowledgeSystem实例
    """
    global _system
    if _system is None:
        _system = KnowledgeSystem(cells_dir)
    return _system


# 便捷函数
def query(question: str, context: str = "") -> Dict[str, Any]:
    """快速查询"""
    return get_knowledge_system().query(question, context)


def check(response: str, context: str = "") -> Dict[str, Any]:
    """快速方法论检查"""
    return get_knowledge_system().check_methodology(response, context)


def get_status() -> Dict[str, Any]:
    """快速获取状态"""
    return get_knowledge_system().get_status()


__all__ = [
    # 核心系统
    "KnowledgeSystem",
    "get_knowledge_system",
    "query",
    "check",
    "get_status",
    
    # 推理增强
    "ReasoningEnhancer",
    "get_reasoning_enhancer",
    "enhance_reasoning_hook",
    "WisdomSchedulerIntegration",
    "create_reasoning_context",
    
    # 神经集成
    "NeuralKnowledgeBridge",
    "get_neural_knowledge_bridge",
    "initialize_default_mappings",
    "ActivationType",
]
