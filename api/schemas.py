"""
Somn API Server - 数据模型定义 (Pydantic v2)
定义所有API请求和响应的数据结构
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ═══════════════════════════════════════════════════════════════
# 通用模型
# ═══════════════════════════════════════════════════════════════

class APIResponse(BaseModel):
    """通用API响应基类"""
    success: bool = True
    message: str = ""
    timestamp: datetime = Field(default_factory=datetime.now)
    data: Optional[Any] = None


class PaginatedResponse(APIResponse):
    """分页响应"""
    total: int = 0
    page: int = 1
    page_size: int = 20


class ErrorResponse(BaseModel):
    """错误响应"""
    success: bool = False
    error: str
    error_code: str = "UNKNOWN_ERROR"
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


# ═══════════════════════════════════════════════════════════════
# 健康检查 & 系统状态
# ═══════════════════════════════════════════════════════════════

class HealthCheckResponse(APIResponse):
    """健康检查响应"""
    status: str = "healthy"  # healthy / degraded / unhealthy
    version: str = ""
    uptime_seconds: float = 0
    components: Dict[str, str] = {}


class SystemStatusResponse(APIResponse):
    """系统状态响应"""
    version: str = ""
    environment: str = "standalone"
    loaded_modules: List[str] = []
    wisdom_schools_count: int = 0
    engine_count: int = 0
    memory_usage_mb: float = 0


class ConfigResponse(APIResponse):
    """前端可见配置响应"""
    config: Dict[str, Any] = {}


# ═══════════════════════════════════════════════════════════════
# 对话
# ═══════════════════════════════════════════════════════════════

class ChatRequest(BaseModel):
    """对话请求"""
    message: str
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    industry: Optional[str] = None
    stream: bool = False


class ChatResponse(APIResponse):
    """对话响应"""
    session_id: str = ""
    reply: str = ""
    wisdom_insights: List[str] = []
    confidence: float = 0.0
    processing_time_ms: float = 0.0
    metadata: Dict[str, Any] = {}


class StreamChunk(BaseModel):
    """流式响应块"""
    chunk_type: str  # "text" | "thinking" | "done" | "error"
    content: str = ""
    session_id: str = ""


# ═══════════════════════════════════════════════════════════════
# 知识库
# ═══════════════════════════════════════════════════════════════

class KnowledgeSearchRequest(BaseModel):
    """知识搜索请求"""
    query: str
    top_k: int = 10
    category: Optional[str] = None


class KnowledgeEntry(BaseModel):
    """知识条目"""
    id: str
    title: str
    content: str
    category: Optional[str] = None
    source: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class KnowledgeListResponse(PaginatedResponse):
    """知识列表响应"""
    items: List[Dict[str, Any]] = []


class KnowledgeSearchResponse(APIResponse):
    """知识搜索响应"""
    results: List[Dict[str, Any]] = []
    total: int = 0


class KnowledgeAddRequest(BaseModel):
    """添加知识请求"""
    title: str
    content: str
    category: Optional[str] = None
    source: Optional[str] = None


# ═══════════════════════════════════════════════════════════════
# 文档生成
# ═══════════════════════════════════════════════════════════════

class DocumentGenerateRequest(BaseModel):
    """文档生成请求"""
    doc_type: str  # "report" | "proposal" | "analysis" | "plan"
    title: str
    template: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    format: str = "docx"  # "docx" | "pdf" | "xlsx" | "pptx"


class DocumentGenerateResponse(APIResponse):
    """文档生成响应"""
    document_id: str = ""
    download_url: str = ""
    file_size: int = 0


# ═══════════════════════════════════════════════════════════════
# 分析 & 策略
# ═══════════════════════════════════════════════════════════════

class AnalysisRequest(BaseModel):
    """分析请求"""
    analysis_type: str  # "strategy" | "market" | "growth" | "risk"
    description: str
    industry: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    depth: str = "standard"  # "quick" | "standard" | "deep"


class AnalysisResponse(APIResponse):
    """分析响应"""
    analysis_id: str = ""
    result: Dict[str, Any] = {}
    recommendations: List[str] = []
    confidence: float = 0.0
    processing_time_ms: float = 0.0


# ═══════════════════════════════════════════════════════════════
# 记忆 & 学习
# ═══════════════════════════════════════════════════════════════

class MemoryListResponse(PaginatedResponse):
    """记忆列表响应"""
    items: List[Dict[str, Any]] = []


class LearningStatusResponse(APIResponse):
    """学习状态响应"""
    is_learning: bool = False
    last_learning_time: Optional[str] = None
    total_learned_items: int = 0
    learning_queue_size: int = 0


class WisdomQueryRequest(BaseModel):
    """智慧引擎查询请求"""
    query: str
    schools: Optional[List[str]] = None  # 指定学派，空则全部
    depth: str = "standard"  # "quick" | "standard" | "deep"


class WisdomQueryResponse(APIResponse):
    """智慧引擎查询响应"""
    insights: List[Dict[str, Any]] = []
    contributing_schools: List[str] = []
    processing_time_ms: float = 0.0


class WisdomSchoolInfo(BaseModel):
    """智慧学派信息"""
    name: str
    name_en: str
    description: str
    founder: Optional[str] = None
    wisdom_count: int = 0


# ═══════════════════════════════════════════════════════════════
# 系统管理 (Admin)
# ═══════════════════════════════════════════════════════════════

class PreloadModulesRequest(BaseModel):
    """预加载模块请求"""
    names: List[str]


class MemoryDecayRequest(BaseModel):
    """记忆衰减请求"""
    force: bool = False


class MemoryReinforceRequest(BaseModel):
    """记忆强化请求"""
    knowledge_id: str
    boost: float = 0.1


class ClawDispatchRequest(BaseModel):
    """Claw调度请求"""
    query: str
    claw_name: Optional[str] = None
    department: Optional[str] = None
    school: Optional[str] = None
    collaborators: Optional[List[str]] = None


class AdminDashboardResponse(APIResponse):
    """管理仪表盘响应"""
    timestamp: str = ""
    load_manager: Optional[Dict[str, Any]] = None
    llm: Optional[Dict[str, Any]] = None
    chain: Optional[Dict[str, Any]] = None
    evolution: Optional[Dict[str, Any]] = None
    memory: Optional[Dict[str, Any]] = None
    claw: Optional[Dict[str, Any]] = None
    system: Optional[Dict[str, Any]] = None
