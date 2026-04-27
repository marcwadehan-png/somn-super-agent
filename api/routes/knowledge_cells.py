"""
知识格子API路由
===============
提供知识格子系统的HTTP API接口

端点:
- GET  /api/v1/cells              - 获取所有格子
- GET  /api/v1/cells/{cell_id}     - 获取指定格子
- GET  /api/v1/cells/{cell_id}/related - 获取关联格子
- POST /api/v1/cells/query         - 知识查询
- POST /api/v1/cells/check         - 方法论检查
- GET  /api/v1/cells/graph         - 获取知识图谱
- GET  /api/v1/cells/hot           - 获取最热格子
- GET  /api/v1/cells/search        - 搜索格子
- GET  /api/v1/cells/status        - 系统状态
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# 延迟导入避免循环依赖
_knowledge_system = None
_library_bridge = None

# 尝试导入藏书阁知识桥接器
try:
    from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._library_knowledge_bridge import (
        LibraryKnowledgeBridge,
    )
    HAS_LIBRARY_BRIDGE = True
except ImportError:
    HAS_LIBRARY_BRIDGE = False
    LibraryKnowledgeBridge = None


def get_knowledge_system():
    """获取知识系统单例"""
    global _knowledge_system
    if _knowledge_system is None:
        from knowledge_cells import get_knowledge_system as _get
        _knowledge_system = _get()
    return _knowledge_system


def get_library_bridge():
    """获取藏书阁知识桥接器单例"""
    global _library_bridge
    if _library_bridge is None and HAS_LIBRARY_BRIDGE and LibraryKnowledgeBridge:
        _library_bridge = LibraryKnowledgeBridge()
    return _library_bridge


# ============ 请求/响应模型 ============

class QueryRequest(BaseModel):
    """知识查询请求"""
    question: str = Field(..., description="问题")
    context: Optional[str] = Field(None, description="上下文")


class CheckRequest(BaseModel):
    """方法论检查请求"""
    content: str = Field(..., description="需要检查的内容")
    context: Optional[str] = Field(None, description="上下文")


class QueryResponse(BaseModel):
    """知识查询响应"""
    answer: str
    cells_used: List[str]
    frameworks: List[str]
    analogies: List[str]
    data_points: List[str]
    quality_score: float
    methodology_check: Dict[str, Any]


class CheckResponse(BaseModel):
    """方法论检查响应"""
    overall_score: float
    level: str
    dimensions: Dict[str, Any]
    suggestions: List[str]


class CellInfo(BaseModel):
    """格子信息"""
    cell_id: str
    name: str
    tags: List[str]
    activation_count: int
    last_activation: Optional[str]
    associations: Dict[str, float]


class RelatedCell(BaseModel):
    """关联格子"""
    cell_id: str
    name: str
    weight: float


class GraphNode(BaseModel):
    """图谱节点"""
    id: str
    name: str
    activations: int
    category: str


class GraphLink(BaseModel):
    """图谱边"""
    source: str
    target: str
    weight: float


class KnowledgeGraph(BaseModel):
    """知识图谱"""
    nodes: List[GraphNode]
    links: List[GraphLink]


class StatusResponse(BaseModel):
    """系统状态"""
    total_cells: int
    summary: str
    hot_cells: List[Dict[str, Any]]
    knowledge_graph_nodes: int


# ============ 路由 ============

router = APIRouter(prefix="/api/v1/cells", tags=["知识格子"])


@router.get("", response_model=List[Dict[str, Any]])
async def list_cells():
    """获取所有格子"""
    system = get_knowledge_system()
    return system.list_all_cells()


@router.get("/status", response_model=StatusResponse)
async def get_status():
    """获取系统状态"""
    system = get_knowledge_system()
    return system.get_status()


@router.get("/search", response_model=List[Dict[str, Any]])
async def search_cells(keyword: str):
    """搜索格子"""
    system = get_knowledge_system()
    return system.search_cells(keyword)


@router.get("/hot", response_model=List[Dict[str, Any]])
async def get_hot_cells(top_n: int = 5):
    """获取最热格子"""
    system = get_knowledge_system()
    return system.get_hot_cells(top_n)


@router.get("/graph", response_model=KnowledgeGraph)
async def get_graph():
    """获取知识图谱"""
    system = get_knowledge_system()
    data = system.get_knowledge_graph()
    return KnowledgeGraph(
        nodes=[GraphNode(**n) for n in data['nodes']],
        links=[GraphLink(**l) for l in data['links']]
    )


@router.get("/{cell_id}", response_model=Optional[Dict[str, Any]])
async def get_cell(cell_id: str):
    """获取指定格子"""
    system = get_knowledge_system()
    cell = system.get_cell_content(cell_id.upper())
    if not cell:
        raise HTTPException(status_code=404, detail=f"格子 {cell_id} 不存在")
    return cell


@router.get("/{cell_id}/related", response_model=List[RelatedCell])
async def get_related_cells(cell_id: str, threshold: float = 0.6):
    """获取关联格子"""
    system = get_knowledge_system()
    related = system.get_related_cells(cell_id.upper(), threshold)
    return [RelatedCell(**r) for r in related]


@router.post("/query", response_model=QueryResponse)
async def query_knowledge(request: QueryRequest):
    """知识查询"""
    system = get_knowledge_system()
    result = system.query(request.question, request.context or "")
    return QueryResponse(**result)


@router.post("/check", response_model=CheckResponse)
async def check_methodology(request: CheckRequest):
    """方法论检查"""
    system = get_knowledge_system()
    result = system.check_methodology(request.content, request.context or "")
    return CheckResponse(**result)


# ============ 藏书阁集成路由 ============

class LibraryQueryRequest(BaseModel):
    """藏书阁知识查询请求"""
    question: str = Field(..., description="问题")


class LibraryQueryResponse(BaseModel):
    """藏书阁知识查询响应"""
    question: str
    fused_answer: str
    related_cells: List[Dict[str, Any]]
    methodology_score: float
    suggestions: List[str]
    via_library: bool = True


@router.post("/library/query", response_model=LibraryQueryResponse)
async def library_query(request: LibraryQueryRequest):
    """藏书阁知识查询（通过藏书阁桥接器）"""
    bridge = get_library_bridge()
    if not bridge:
        raise HTTPException(
            status_code=503, 
            detail="藏书阁知识桥接器不可用"
        )
    
    result = bridge.query_knowledge(request.question)
    return LibraryQueryResponse(
        question=result.question,
        fused_answer=result.fused_answer,
        related_cells=result.related_cells,
        methodology_score=result.methodology_score,
        suggestions=result.suggestions,
        via_library=True
    )


@router.get("/library/stats", response_model=Dict[str, Any])
async def library_stats():
    """藏书阁知识桥接器统计"""
    bridge = get_library_bridge()
    if not bridge:
        raise HTTPException(
            status_code=503, 
            detail="藏书阁知识桥接器不可用"
        )
    return bridge.get_stats()


@router.post("/library/sync")
async def sync_to_library():
    """同步知识格子到藏书阁"""
    bridge = get_library_bridge()
    if not bridge:
        raise HTTPException(
            status_code=503, 
            detail="藏书阁知识桥接器不可用"
        )
    
    # 延迟导入藏书阁
    try:
        from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._imperial_library import ImperialLibrary
        library = ImperialLibrary()
        bridge.library = library
        result = bridge.sync_to_library()
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
