"""
__all__ = [
    'generate_security_report',
    'get_recent_security_events',
    'get_security_stats',
    'process_request',
    'sanitize_output',
    'sanitize_response',
    'validate',
]

防御深度系统 - Defense Depth System
多层防御实现:
"在宇宙中,只有层层防御才能生存"

核心哲学:
1. 深度防御:多层防护,即使一层被突破,其他层仍能防护
2. 最小权限:默认拒绝,最小权限原则
3. 纵向防御:每层都有独立的防御能力
4. 快速响应:检测到攻击立即响应

参考<三体>中的防御strategy:
- 地球建立三体防御体系(多个层面的防御)
- 面壁者的独立decision能力(分布式防御)
- 黑暗森林威慑(威慑即防御)
"""

import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
from loguru import logger

try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    logger.warning("PyJWT未安装,JWT功能将受限")

class SecurityLevel(Enum):
    """安全级别"""
    LOW = "low"         # 低安全
    MEDIUM = "medium"   # 中安全
    HIGH = "high"       # 高安全
    CRITICAL = "critical" # 严重安全

class ThreatLevel(Enum):
    """威胁级别"""
    SAFE = "safe"           # 安全
    LOW = "low"             # 低威胁
    MEDIUM = "medium"       # 中等威胁
    HIGH = "high"           # 高威胁
    CRITICAL = "critical"   # 严重威胁

@dataclass
class SecurityRequest:
    """安全请求"""
    user_id: Optional[str]
    ip_address: str
    user_agent: str
    path: str
    method: str
    headers: Dict[str, str]
    body: Any
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class SecurityResponse:
    """安全响应"""
    allowed: bool
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    threat_level: ThreatLevel = ThreatLevel.SAFE
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SecurityEvent:
    """安全事件"""
    event_type: str
    severity: ThreatLevel
    description: str
    ip_address: str
    user_id: Optional[str]
    timestamp: datetime = field(default_factory=datetime.now)
    details: Dict[str, Any] = field(default_factory=dict)

class DefenseLayer:
    """
    防御层基类
    每个防御层独立工作,即使其他层失效
    """
    
    def __init__(self, name: str, enabled: bool = True):
        self.name = name
        self.enabled = enabled
        self.stats = {
            'total_requests': 0,
            'blocked_requests': 0,
            'passed_requests': 0
        }
    
    def validate(self, request: SecurityRequest) -> SecurityResponse:
        """
        验证请求
        
        Args:
            request: 安全请求
            
        Returns:
            SecurityResponse: 安全响应
        """
        if not self.enabled:
            self.stats['passed_requests'] += 1
            return SecurityResponse(allowed=True)
        
        self.stats['total_requests'] += 1
        
        # 默认通过
        response = self._validate_internal(request)
        
        if response.allowed:
            self.stats['passed_requests'] += 1
        else:
            self.stats['blocked_requests'] += 1
        
        return response
    
    def _validate_internal(self, request: SecurityRequest) -> SecurityResponse:
        """内部验证方法 - 子类实现"""
        raise NotImplementedError

class InputValidationLayer(DefenseLayer):
    """输入验证层 - 第一层防御"""
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__("InputValidation", config and config.get('enabled', True))
        self.config = config or {}
        
        # 最大长度限制
        self.max_input_length = self.config.get('max_input_length', 10000)
        
        # SQL注入模式
        self.sql_injection_patterns = [
            r"(\bunion\b.*\bselect\b)",
            r"(\bselect\b.*\bfrom\b)",
            r"(\bdrop\b.*\btable\b)",
            r"(\binsert\b.*\binto\b)",
            r"(\bdelete\b.*\bfrom\b)",
            r"(\bupdate\b.*\bset\b)",
        ]
        
        # XSS模式
        self.xss_patterns = [
            r"<script.*>.*</script>",
            r"javascript:",
            r"on\w+\s*=",
        ]
    
    def _validate_internal(self, request: SecurityRequest) -> SecurityResponse:
        """验证输入"""
        body_str = str(request.body)
        
        # 检查长度
        if len(body_str) > self.max_input_length:
            return SecurityResponse(
                allowed=False,
                error_code="INPUT_TOO_LONG",
                error_message=f"输入长度超过限制 ({len(body_str)} > {self.max_input_length})",
                threat_level=ThreatLevel.MEDIUM
            )
        
        # 检查SQL注入
        for pattern in self.sql_injection_patterns:
            if re.search(pattern, body_str, re.IGNORECASE):
                return SecurityResponse(
                    allowed=False,
                    error_code="SQL_INJECTION_DETECTED",
                    error_message="检测到SQL注入尝试",
                    threat_level=ThreatLevel.HIGH
                )
        
        # 检查XSS
        for pattern in self.xss_patterns:
            if re.search(pattern, body_str, re.IGNORECASE):
                return SecurityResponse(
                    allowed=False,
                    error_code="XSS_DETECTED",
                    error_message="检测到XSS攻击尝试",
                    threat_level=ThreatLevel.HIGH
                )
        
        return SecurityResponse(allowed=True)

class RateLimitLayer(DefenseLayer):
    """速率限制层 - 第二层防御"""
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__("RateLimit", config and config.get('enabled', True))
        self.config = config or {}
        
        # 速率限制配置
        self.max_requests_per_minute = self.config.get('max_requests_per_minute', 60)
        self.max_requests_per_hour = self.config.get('max_requests_per_hour', 1000)
        
        # 请求计数器
        self.minute_counter = defaultdict(list)
        self.hour_counter = defaultdict(list)
    
    def _validate_internal(self, request: SecurityRequest) -> SecurityResponse:
        """验证速率限制"""
        now = datetime.now()
        key = f"{request.ip_address}:{request.path}"
        
        # 检查每分钟限制
        minute_key = f"{key}:{now.minute}"
        self.minute_counter[minute_key] = [
            t for t in self.minute_counter[minute_key]
            if now - t < timedelta(minutes=1)
        ]
        
        if len(self.minute_counter[minute_key]) >= self.max_requests_per_minute:
            return SecurityResponse(
                allowed=False,
                error_code="RATE_LIMIT_EXCEEDED_MINUTE",
                error_message=f"超过每分钟请求限制 ({self.max_requests_per_minute})",
                threat_level=ThreatLevel.MEDIUM,
                metadata={
                    'limit': self.max_requests_per_minute,
                    'current': len(self.minute_counter[minute_key])
                }
            )
        
        # 检查每小时限制
        hour_key = f"{key}:{now.hour}"
        self.hour_counter[hour_key] = [
            t for t in self.hour_counter[hour_key]
            if now - t < timedelta(hours=1)
        ]
        
        if len(self.hour_counter[hour_key]) >= self.max_requests_per_hour:
            return SecurityResponse(
                allowed=False,
                error_code="RATE_LIMIT_EXCEEDED_HOUR",
                error_message=f"超过每小时请求限制 ({self.max_requests_per_hour})",
                threat_level=ThreatLevel.LOW,
                metadata={
                    'limit': self.max_requests_per_hour,
                    'current': len(self.hour_counter[hour_key])
                }
            )
        
        # 记录请求
        self.minute_counter[minute_key].append(now)
        self.hour_counter[hour_key].append(now)
        
        return SecurityResponse(allowed=True)

class AuthenticationLayer(DefenseLayer):
    """认证层 - 第三层防御"""
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__("Authentication", config and config.get('enabled', True))
        self.config = config or {}
        
        self.secret_key = self.config.get('secret_key', 'your-secret-key-here')
        self.algorithm = self.config.get('algorithm', 'HS256')
    
    def _validate_internal(self, request: SecurityRequest) -> SecurityResponse:
        """验证认证"""
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return SecurityResponse(
                allowed=False,
                error_code="AUTHENTICATION_REQUIRED",
                error_message="需要认证",
                threat_level=ThreatLevel.LOW
            )
        
        # 检查Bearer token
        if not auth_header.startswith('Bearer '):
            return SecurityResponse(
                allowed=False,
                error_code="INVALID_AUTH_FORMAT",
                error_message="无效的认证格式",
                threat_level=ThreatLevel.MEDIUM
            )
        
        token = auth_header[7:]
        
        # 验证token
        if not JWT_AVAILABLE:
            logger.warning("JWT不可用,跳过token验证")
            return SecurityResponse(allowed=True)
        
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            request.user_id = payload.get('user_id')
            return SecurityResponse(allowed=True)
        except jwt.ExpiredSignatureError:
            return SecurityResponse(
                allowed=False,
                error_code="TOKEN_EXPIRED",
                error_message="令牌已过期",
                threat_level=ThreatLevel.LOW
            )
        except jwt.InvalidTokenError as e:
            return SecurityResponse(
                allowed=False,
                error_code="INVALID_TOKEN",
                error_message="无效的令牌",
                threat_level=ThreatLevel.MEDIUM
            )

class AuthorizationLayer(DefenseLayer):
    """授权层 - 第四层防御"""
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__("Authorization", config and config.get('enabled', True))
        self.config = config or {}
        
        # 权限mapping
        self.permission_map = self.config.get('permission_map', {})
    
    def _validate_internal(self, request: SecurityRequest) -> SecurityResponse:
        """验证授权"""
        if not request.user_id:
            return SecurityResponse(
                allowed=False,
                error_code="USER_NOT_AUTHENTICATED",
                error_message="用户未认证",
                threat_level=ThreatLevel.LOW
            )
        
        # 检查权限
        user_permissions = self.permission_map.get(request.user_id, [])
        required_permission = self._get_required_permission(request.path, request.method)
        
        if required_permission and required_permission not in user_permissions:
            return SecurityResponse(
                allowed=False,
                error_code="PERMISSION_DENIED",
                error_message=f"缺少权限: {required_permission}",
                threat_level=ThreatLevel.MEDIUM
            )
        
        return SecurityResponse(allowed=True)
    
    def _get_required_permission(self, path: str, method: str) -> Optional[str]:
        """get所需权限"""
        # 简单实现:基于路径和方法
        return f"{method}:{path}"

class DataValidationLayer(DefenseLayer):
    """数据验证层 - 第五层防御"""
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__("DataValidation", config and config.get('enabled', True))
        self.config = config or {}
    
    def _validate_internal(self, request: SecurityRequest) -> SecurityResponse:
        """验证数据"""
        # 检查数据完整性
        if request.body is None and request.method in ['POST', 'PUT']:
            return SecurityResponse(
                allowed=False,
                error_code="MISSING_DATA",
                error_message="缺少请求数据",
                threat_level=ThreatLevel.LOW
            )
        
        # 可以添加更多数据验证逻辑
        
        return SecurityResponse(allowed=True)

class OutputSanitizationLayer(DefenseLayer):
    """输出清理层 - 第六层防御"""
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__("OutputSanitization", config and config.get('enabled', True))
        self.config = config or {}
    
    def _validate_internal(self, request: SecurityRequest) -> SecurityResponse:
        """清理输出"""
        # 这个层在响应时应用,不是在请求时
        # 返回允许,但在处理响应时会清理
        return SecurityResponse(allowed=True)
    
    def sanitize_output(self, output: Any) -> Any:
        """清理输出数据"""
        if isinstance(output, str):
            # 移除危险的HTML标签
            import html
            return html.escape(output)
        elif isinstance(output, dict):
            return {k: self.sanitize_output(v) for k, v in output.items()}
        elif isinstance(output, list):
            return [self.sanitize_output(item) for item in output]
        return output

class DefenseDepthSystem:
    """
    防御深度系统
    
    基于<三体>黑暗森林法则:
    - 多层防御,即使一层被突破,其他层仍能防护
    - 每层独立,没有单点故障
    - 纵向防御,全面覆盖
    
    功能:
    1. 输入验证 - 第一层
    2. 速率限制 - 第二层
    3. 认证 - 第三层
    4. 授权 - 第四层
    5. 数据验证 - 第五层
    6. 输出清理 - 第六层
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        
        # init防御层
        self.layers = self._init_layers()
        
        # 安全事件记录
        self.security_events: List[SecurityEvent] = []
        
        logger.info(f"防御深度系统init完成 - {len(self.layers)}层防御")
    
    def _init_layers(self) -> List[DefenseLayer]:
        """init防御层"""
        layers = []
        
        # 输入验证层
        layers.append(InputValidationLayer(self.config.get('input_validation')))
        
        # 速率限制层
        layers.append(RateLimitLayer(self.config.get('rate_limit')))
        
        # 认证层
        layers.append(AuthenticationLayer(self.config.get('authentication')))
        
        # 授权层
        layers.append(AuthorizationLayer(self.config.get('authorization')))
        
        # 数据验证层
        layers.append(DataValidationLayer(self.config.get('data_validation')))
        
        # 输出清理层
        layers.append(OutputSanitizationLayer(self.config.get('output_sanitization')))
        
        return layers
    
    def process_request(self, request: SecurityRequest) -> SecurityResponse:
        """
        处理请求 - 多层防御
        
        基于<三体>:层层防御,全面防护
        
        Args:
            request: 安全请求
            
        Returns:
            SecurityResponse: 安全响应
        """
        start_time = time.time()
        
        # 逐层验证
        for layer in self.layers:
            response = layer.validate(request)
            
            if not response.allowed:
                # 记录安全事件
                event = SecurityEvent(
                    event_type=f"{layer.name}_BLOCKED",
                    severity=response.threat_level,
                    description=response.error_message or "请求被拦截",
                    ip_address=request.ip_address,
                    user_id=request.user_id,
                    details={
                        'layer': layer.name,
                        'error_code': response.error_code,
                        'path': request.path,
                        'method': request.method
                    }
                )
                self.security_events.append(event)
                
                logger.warning(f"请求被{layer.name}拦截: {response.error_message}")
                
                return response
        
        # 所有层都通过
        processing_time = time.time() - start_time
        logger.info(f"请求通过所有防御层 - 处理时间: {processing_time:.3f}s")
        
        return SecurityResponse(
            allowed=True,
            metadata={
                'processing_time': processing_time,
                'layers_validated': len(self.layers)
            }
        )
    
    def sanitize_response(self, response_data: Any) -> Any:
        """
        清理响应数据
        
        Args:
            response_data: 响应数据
            
        Returns:
            清理后的数据
        """
        output_layer = self.layers[-1]
        if isinstance(output_layer, OutputSanitizationLayer):
            return output_layer.sanitize_output(response_data)
        return response_data
    
    def get_security_stats(self) -> Dict[str, Any]:
        """
        get安全统计信息
        
        Returns:
            统计信息
        """
        total_requests = sum(layer.stats['total_requests'] for layer in self.layers)
        blocked_requests = sum(layer.stats['blocked_requests'] for layer in self.layers)
        passed_requests = sum(layer.stats['passed_requests'] for layer in self.layers)
        
        layer_stats = {
            layer.name: layer.stats.copy()
            for layer in self.layers
        }
        
        # 威胁级别统计
        threat_level_count = defaultdict(int)
        for event in self.security_events:
            threat_level_count[event.severity.value] += 1
        
        return {
            'total_requests': total_requests,
            'blocked_requests': blocked_requests,
            'passed_requests': passed_requests,
            'block_rate': blocked_requests / total_requests if total_requests > 0 else 0,
            'layer_stats': layer_stats,
            'security_events_count': len(self.security_events),
            'threat_level_distribution': dict(threat_level_count)
        }
    
    def get_recent_security_events(self, hours: int = 24) -> List[SecurityEvent]:
        """
        get最近的安全事件
        
        Args:
            hours: 小时数
            
        Returns:
            安全事件列表
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [
            event for event in self.security_events
            if event.timestamp > cutoff_time
        ]
    
    def generate_security_report(self) -> str:
        """
        generate安全报告
        
        Returns:
            安全报告
        """
        stats = self.get_security_stats()
        recent_events = self.get_recent_security_events()
        
        report = f"""
# 安全报告

generate时间: {datetime.now().isoformat()}

## 统计信息
- 总请求数: {stats['total_requests']}
- 拦截请求: {stats['blocked_requests']}
- 通过请求: {stats['passed_requests']}
- 拦截率: {stats['block_rate']:.2%}

## 各层统计
"""
        for layer_name, layer_stats in stats['layer_stats'].items():
            report += f"""
### {layer_name}
- 总请求: {layer_stats['total_requests']}
- 拦截: {layer_stats['blocked_requests']}
- 通过: {layer_stats['passed_requests']}
"""

        if recent_events:
            report += f"""

## 最近的安全事件 (最近24小时)
- 事件总数: {len(recent_events)}

### 威胁级别分布
"""
            threat_dist = stats['threat_level_distribution']
            for level, count in threat_dist.items():
                report += f"- {level}: {count}\n"
        
        return report

# 测试代码
# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")

# 添加re导入
import re
