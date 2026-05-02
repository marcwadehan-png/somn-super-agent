"""
API 中间件 - 超时保护和请求频率限制
"""
import time
import asyncio
import logging
from typing import Dict, Tuple, Optional, Callable
from collections import defaultdict
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)


# ============================================================================
# 全局超时中间件
# ============================================================================

class GlobalTimeoutMiddleware(BaseHTTPMiddleware):
    """
    全局超时中间件 - 为所有请求添加超时保护
    
    默认超时时间：
    - GET 请求：30秒
    - POST 请求：60秒
    - 上传请求：300秒
    """
    
    def __init__(
        self,
        app: ASGIApp,
        default_timeout: float = 60.0,
        get_timeout: float = 30.0,
        post_timeout: float = 60.0,
        upload_timeout: float = 300.0,
    ):
        super().__init__(app)
        self.default_timeout = default_timeout
        self.get_timeout = get_timeout
        self.post_timeout = post_timeout
        self.upload_timeout = upload_timeout
        
        # 特殊路径的超时设置
        self.path_timeouts: Dict[str, float] = {
            "/api/v1/chat": 120.0,           # 聊天接口
            "/api/v1/chat/stream": 300.0,    # 流式聊天
            "/api/v1/admin/claw/dispatch": 180.0,  # Claw调度
            "/api/v1/analysis/strategy": 120.0,     # 策略分析
            "/api/v1/analysis/market": 120.0,       # 市场分析
            "/api/v1/documents/generate": 180.0,    # 文档生成
        }
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """处理请求，添加超时保护"""
        # 确定超时时间
        timeout = self._get_timeout(request)
        
        # 记录开始时间
        start_time = time.time()
        logger.info(f"[超时保护] {request.method} {request.url.path} (超时: {timeout}s)")
        
        try:
            # 使用 asyncio.wait_for 添加超时
            response = await asyncio.wait_for(
                call_next(request),
                timeout=timeout,
            )
            
            # 记录耗时
            elapsed = time.time() - start_time
            logger.info(f"[超时保护] {request.method} {request.url.path} 完成（耗时: {elapsed:.2f}s）")
            
            return response
        
        except asyncio.TimeoutError:
            # 超时处理
            elapsed = time.time() - start_time
            logger.error(f"[超时保护] {request.method} {request.url.path} 超时（耗时: {elapsed:.2f}s > {timeout}s）")
            
            return JSONResponse(
                status_code=408,
                content={
                    "success": False,
                    "error": f"请求超时（{timeout}秒），请稍后重试或联系管理员",
                    "path": request.url.path,
                    "method": request.method,
                    "timeout": timeout,
                    "elapsed": round(elapsed, 2),
                }
            )
        
        except Exception as e:
            # 其他异常
            elapsed = time.time() - start_time
            logger.error(f"[超时保护] {request.method} {request.url.path} 异常（耗时: {elapsed:.2f}s）: {e}")
            raise
    
    def _get_timeout(self, request: Request) -> float:
        """根据请求类型和路径确定超时时间"""
        # 检查特殊路径
        path = request.url.path
        if path in self.path_timeouts:
            return self.path_timeouts[path]
        
        # 根据请求方法确定超时
        if request.method == "GET":
            return self.get_timeout
        elif request.method == "POST":
            # 检查是否是上传请求
            content_type = request.headers.get("content-type", "")
            if "multipart/form-data" in content_type or "application/octet-stream" in content_type:
                return self.upload_timeout
            return self.post_timeout
        else:
            return self.default_timeout


# ============================================================================
# 请求频率限制中间件
# ============================================================================

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    请求频率限制中间件 - 防止API被滥用导致系统卡死
    
    默认限制：
    - 全局：100请求/分钟
    - 单IP：30请求/分钟
    - 单用户：60请求/分钟
    """
    
    def __init__(
        self,
        app: ASGIApp,
        global_limit: int = 500,      # 放宽到500请求/分钟
        ip_limit: int = 100,       # 放宽到100请求/分钟
        user_limit: int = 200,     # 放宽到200请求/分钟
        window_seconds: int = 60,
    ):
        super().__init__(app)
        self.global_limit = global_limit
        self.ip_limit = ip_limit
        self.user_limit = user_limit
        self.window_seconds = window_seconds
        
        # 请求计数（使用字典存储：（计数器，时间戳））
        self.global_requests: Tuple[int, float] = (0, time.time())
        self.ip_requests: Dict[str, Tuple[int, float]] = defaultdict(lambda: (0, time.time()))
        self.user_requests: Dict[str, Tuple[int, float]] = defaultdict(lambda: (0, time.time()))
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """处理请求，检查频率限制"""
        # 获取客户端IP
        client_ip = self._get_client_ip(request)
        
        # 获取用户ID（如果有）
        user_id = self._get_user_id(request)
        
        # 检查频率限制
        limit_exceeded, limit_info = self._check_rate_limit(client_ip, user_id)
        
        if limit_exceeded:
            logger.warning(f"[频率限制] 请求被拒绝: IP={client_ip}, User={user_id}, {limit_info}")
            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "error": "请求过于频繁，请稍后重试",
                    "limit_info": limit_info,
                }
            )
        
        # 记录请求
        self._record_request(client_ip, user_id)
        
        # 继续处理请求
        return await call_next(request)
    
    def _get_client_ip(self, request: Request) -> str:
        """获取客户端IP"""
        # 检查代理头
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # 返回直接连接的IP
        return request.client.host if request.client else "unknown"
    
    def _get_user_id(self, request: Request) -> Optional[str]:
        """获取用户ID（从请求头或参数中）"""
        # 这里可以根据实际需求修改
        # 例如：从JWT token中解析用户ID
        user_id = request.headers.get("X-User-ID")
        return user_id
    
    def _check_rate_limit(self, ip: str, user_id: Optional[str]) -> Tuple[bool, Dict]:
        """检查是否超过频率限制"""
        now = time.time()
        
        # 检查全局限制
        global_count, global_start = self.global_requests
        if now - global_start > self.window_seconds:
            # 时间窗口已过期，重置计数
            self.global_requests = (0, now)
        elif global_count >= self.global_limit:
            return True, {
                "type": "global",
                "limit": self.global_limit,
                "window_seconds": self.window_seconds,
                "current": global_count,
            }
        
        # 检查IP限制
        ip_count, ip_start = self.ip_requests[ip]
        if now - ip_start > self.window_seconds:
            # 时间窗口已过期，重置计数
            self.ip_requests[ip] = (0, now)
        elif ip_count >= self.ip_limit:
            return True, {
                "type": "ip",
                "ip": ip,
                "limit": self.ip_limit,
                "window_seconds": self.window_seconds,
                "current": ip_count,
            }
        
        # 检查用户限制
        if user_id:
            user_count, user_start = self.user_requests[user_id]
            if now - user_start > self.window_seconds:
                # 时间窗口已过期，重置计数
                self.user_requests[user_id] = (0, now)
            elif user_count >= self.user_limit:
                return True, {
                    "type": "user",
                    "user_id": user_id,
                    "limit": self.user_limit,
                    "window_seconds": self.window_seconds,
                    "current": user_count,
                }
        
        return False, {}
    
    def _record_request(self, ip: str, user_id: Optional[str]):
        """记录请求"""
        now = time.time()
        
        # 更新全局计数
        global_count, global_start = self.global_requests
        if now - global_start > self.window_seconds:
            self.global_requests = (1, now)
        else:
            self.global_requests = (global_count + 1, global_start)
        
        # 更新IP计数
        ip_count, ip_start = self.ip_requests[ip]
        if now - ip_start > self.window_seconds:
            self.ip_requests[ip] = (1, now)
        else:
            self.ip_requests[ip] = (ip_count + 1, ip_start)
        
        # 更新用户计数
        if user_id:
            user_count, user_start = self.user_requests[user_id]
            if now - user_start > self.window_seconds:
                self.user_requests[user_id] = (1, now)
            else:
                self.user_requests[user_id] = (user_count + 1, user_start)
        
        # 清理过期记录（简单实现：每次记录时清理）
        self._clean_old_records(now)
    
    def _clean_old_records(self, now: float):
        """清理过期的请求记录"""
        # 清理全局记录
        global_count, global_start = self.global_requests
        if now - global_start > self.window_seconds:
            self.global_requests = (0, now)
        
        # 清理IP记录
        to_delete = []
        for ip, (count, start) in self.ip_requests.items():
            if now - start > self.window_seconds:
                to_delete.append(ip)
        for ip in to_delete:
            del self.ip_requests[ip]
        
        # 清理用户记录
        to_delete = []
        for user_id, (count, start) in self.user_requests.items():
            if now - start > self.window_seconds:
                to_delete.append(user_id)
        for user_id in to_delete:
            del self.user_requests[user_id]


# ============================================================================
# 内存泄漏检测中间件
# ============================================================================

class MemoryLeakDetectionMiddleware(BaseHTTPMiddleware):
    """
    内存泄漏检测中间件 - 检测可能的内存泄漏
    
    定期检查内存使用情况，如果内存使用持续增长，记录警告日志
    """
    
    def __init__(
        self,
        app: ASGIApp,
        check_interval: int = 100,  # 每100个请求检查一次
        growth_threshold: float = 10.0,  # 内存增长超过10MB视为异常
    ):
        super().__init__(app)
        self.check_interval = check_interval
        self.growth_threshold = growth_threshold
        self.request_count = 0
        self.last_memory_mb = 0.0
        self.max_memory_mb = 0.0
        
        # 尝试导入psutil
        try:
            import psutil
            self.process = psutil.Process()
            self.has_psutil = True
        except ImportError:
            self.process = None
            self.has_psutil = False
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """处理请求，定期检查内存使用"""
        # 增加请求计数
        self.request_count += 1
        
        # 定期检查和记录内存使用
        if self.has_psutil and self.request_count % self.check_interval == 0:
            self._check_memory()
        
        # 继续处理请求
        return await call_next(request)
    
    def _check_memory(self):
        """检查内存使用情况"""
        try:
            memory_info = self.process.memory_info()
            current_mb = memory_info.rss / 1024 / 1024
            
            # 更新最大内存使用
            if current_mb > self.max_memory_mb:
                self.max_memory_mb = current_mb
            
            # 检查内存增长
            if self.last_memory_mb > 0:
                growth = current_mb - self.last_memory_mb
                if growth > self.growth_threshold:
                    logger.warning(
                        f"[内存泄漏检测] 内存异常增长: +{growth:.2f}MB "
                        f"(当前: {current_mb:.2f}MB, 最大: {self.max_memory_mb:.2f}MB)"
                    )
            
            # 更新上次内存使用
            self.last_memory_mb = current_mb
            
            logger.info(
                f"[内存泄漏检测] 内存使用: {current_mb:.2f}MB "
                f"(最大: {self.max_memory_mb:.2f}MB, 请求数: {self.request_count})"
            )
        
        except Exception as e:
            logger.error(f"[内存泄漏检测] 检查失败: {e}")


# ============================================================================
# 中间件配置函数
# ============================================================================

def setup_cors_middleware(app, cors_origins: list = None):
    """
    配置CORS中间件
    
    Args:
        app: FastAPI应用实例
        cors_origins: 允许的源列表，默认允许所有
    """
    from fastapi.middleware.cors import CORSMiddleware
    
    if cors_origins is None:
        cors_origins = ["*"]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("[中间件] CORS中间件已添加")


async def request_timing_middleware(request: Request, call_next):
    """
    请求计时中间件 - 记录每个请求的处理时间
    
    Args:
        request: FastAPI请求对象
        call_next: 下一个处理函数
    """
    import time
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time * 1000, 2))
    
    return response


def setup_middlewares(app):
    """
    配置所有中间件
    
    在创建FastAPI应用后调用此函数
    """
    # 添加全局超时中间件
    app.add_middleware(GlobalTimeoutMiddleware)
    logger.info("[中间件] 全局超时中间件已添加")
    
    # 添加请求频率限制中间件
    app.add_middleware(RateLimitMiddleware)
    logger.info("[中间件] 请求频率限制中间件已添加")
    
    # 添加内存泄漏检测中间件
    app.add_middleware(MemoryLeakDetectionMiddleware)
    logger.info("[中间件] 内存泄漏检测中间件已添加")
