"""
重试工具模块 [v10.1 新增]
提供通用重试机制，支持指数退避、熔断降级、结果缓存。

适用场景：
- LLM API 调用（网络超时、429限流、5xx服务端错误）
- 网络搜索（DNS失败、连接超时、API不可用）
- 学派调度（引擎加载失败、模块导入错误）
- 记忆查询（文件I/O错误、索引损坏）

[v10.1] 作为 P1级性能优化的一部分，补充缺失的重试机制。
"""

from __future__ import annotations

import time
import logging
import threading
from typing import Callable, TypeVar, Optional, Tuple, List, Dict, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps

logger = logging.getLogger(__name__)

T = TypeVar("T")


# ─────────────────────────────────────────────────────────────────────────────
# 可重试异常定义
# ─────────────────────────────────────────────────────────────────────────────

class RetryableError(Exception):
    """可重试的异常基类（网络超时、429限流、5xx错误）"""
    pass


class NonRetryableError(Exception):
    """不可重试的异常（参数错误、认证失败、权限不足）"""
    pass


# ─────────────────────────────────────────────────────────────────────────────
# 重试策略配置
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class RetryConfig:
    """重试策略配置 [v18.0 优化：最大延迟从10s→3s，减少阻塞]"""
    max_attempts: int = 3           # 最大尝试次数（含首次）
    base_delay: float = 0.5        # 基础退避延迟（秒）v18.0: 1.0→0.5
    max_delay: float = 3.0          # 最大退避延迟（秒）v18.0: 10.0→3.0（减少阻塞）
    exponential_base: float = 2.0    # 指数底数
    jitter: bool = True             # 是否添加随机抖动
    retryable_exceptions: Tuple[type, ...] = (RetryableError, ConnectionError, TimeoutError)
    # 非重试的HTTP状态码（认证失败、参数错误等）
    non_retryable_status: Set[int] = field(default_factory=lambda: {400, 401, 403, 404, 422})


# ─────────────────────────────────────────────────────────────────────────────
# 全局熔断器（防止对故障服务持续重试）
# ─────────────────────────────────────────────────────────────────────────────

class CircuitBreaker:
    """
    熔断器：跟踪服务的故障状态，自动开启/关闭熔断。

    状态机：
        CLOSED（正常）→ 故障率超过 threshold → OPEN（熔断）
        OPEN（熔断）→ 冷却时间到期 → HALF_OPEN（半开）
        HALF_OPEN（半开）→ 成功 → CLOSED | 失败 → OPEN
    """

    class State(Enum):
        CLOSED = "closed"
        OPEN = "open"
        HALF_OPEN = "half_open"

    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        half_open_attempts: int = 1,
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_attempts = half_open_attempts

        self._lock = threading.RLock()
        self._state = self.State.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time: Optional[float] = None
        self._opened_at: Optional[float] = None

    @property
    def state(self) -> State:
        with self._lock:
            if self._state == self.State.OPEN:
                # 检查冷却时间是否到期
                if self._opened_at and (time.time() - self._opened_at) >= self.recovery_timeout:
                    self._state = self.State.HALF_OPEN
                    self._success_count = 0
            return self._state

    def is_available(self) -> bool:
        """检查服务是否可用（未熔断）"""
        return self.state != self.State.OPEN

    def record_success(self):
        """记录一次成功调用"""
        with self._lock:
            if self._state == self.State.HALF_OPEN:
                self._success_count += 1
                if self._success_count >= self.half_open_attempts:
                    self._state = self.State.CLOSED
                    self._failure_count = 0
                    logger.info(f"[熔断器] {self.name}: 恢复 CLOSED")
            elif self._state == self.State.CLOSED:
                # 成功后清零失败计数
                self._failure_count = max(0, self._failure_count - 1)

    def record_failure(self):
        """记录一次失败调用"""
        with self._lock:
            if self._state == self.State.HALF_OPEN:
                self._state = self.State.OPEN
                self._opened_at = time.time()
                logger.warning(f"[熔断器] {self.name}: HALF_OPEN→OPEN（半开失败）")
            elif self._state == self.State.CLOSED:
                self._failure_count += 1
                self._last_failure_time = time.time()
                if self._failure_count >= self.failure_threshold:
                    self._state = self.State.OPEN
                    self._opened_at = time.time()
                    logger.warning(
                        f"[熔断器] {self.name}: CLOSED→OPEN（连续{self._failure_count}次失败）"
                    )

    def get_status(self) -> Dict[str, Any]:
        """获取熔断器状态（用于监控）"""
        with self._lock:
            return {
                "name": self.name,
                "state": self.state.value,
                "failure_count": self._failure_count,
                "success_count": self._success_count,
                "opened_at": self._opened_at,
                "recovery_timeout": self.recovery_timeout,
            }


# ─────────────────────────────────────────────────────────────────────────────
# 全局熔断器注册表（按服务名隔离熔断状态）
# ─────────────────────────────────────────────────────────────────────────────

_CIRCUIT_BREAKERS: Dict[str, CircuitBreaker] = {}
_CB_LOCK = threading.RLock()


def get_circuit_breaker(
    name: str,
    failure_threshold: int = 5,
    recovery_timeout: float = 30.0,
) -> CircuitBreaker:
    """获取或创建命名熔断器"""
    with _CB_LOCK:
        if name not in _CIRCUIT_BREAKERS:
            _CIRCUIT_BREAKERS[name] = CircuitBreaker(
                name=name,
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
            )
        return _CIRCUIT_BREAKERS[name]


# ─────────────────────────────────────────────────────────────────────────────
# 核心重试函数
# ─────────────────────────────────────────────────────────────────────────────

def retry_with_backoff(
    config: RetryConfig = None,
    circuit_breaker: Optional[CircuitBreaker] = None,
    name: str = "unnamed",
    on_retry: Optional[Callable[[Exception, int], None]] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    重试装饰器：使用指数退避+熔断器装饰任意函数。

    用法示例：
        @retry_with_backoff(name="openai-api", config=RetryConfig(max_attempts=3))
        def call_llm_api(messages):
            return llm.chat(messages)

    Args:
        config: 重试策略，默认 RetryConfig()
        circuit_breaker: 熔断器，不传则不启用熔断
        name: 标识名称（用于日志和熔断器隔离）
        on_retry: 每次重试前的回调，参数为 (异常, 当前重试次数)

    Returns:
        装饰后的函数
    """

    if config is None:
        config = RetryConfig()

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            cb = circuit_breaker
            if cb is None:
                cb = get_circuit_breaker(name)

            last_exception: Optional[Exception] = None

            for attempt in range(1, config.max_attempts + 1):
                # 熔断检查
                if not cb.is_available():
                    logger.warning(
                        f"[重试-{name}] 熔断器 OPEN，跳过调用（等待冷却）"
                    )
                    # 抛出特殊异常，让调用方知道服务不可用
                    raise NonRetryableError(
                        f"服务 {name} 熔断中，请稍后重试"
                    )

                try:
                    result = func(*args, **kwargs)
                    cb.record_success()
                    return result

                except NonRetryableError:
                    # 不可重试的错误直接抛出
                    raise

                except config.retryable_exceptions as e:
                    last_exception = e
                    cb.record_failure()

                    if attempt >= config.max_attempts:
                        logger.error(
                            f"[重试-{name}] 达到最大重试次数({config.max_attempts})，"
                            f"最后一次错误: {e}"
                        )
                        raise

                    # 计算退避延迟
                    delay = min(
                        config.base_delay * (config.exponential_base ** (attempt - 1)),
                        config.max_delay,
                    )
                    if config.jitter:
                        import random
                        delay = delay * (0.5 + random.random())  # [0.5x, 1.5x]

                    logger.warning(
                        f"[重试-{name}] 第{attempt}次尝试失败: {type(e).__name__}: {e}，"
                        f"{delay:.2f}s后重试..."
                    )

                    if on_retry:
                        on_retry(e, attempt)

                    time.sleep(delay)

                except Exception as e:
                    # 未知异常：不重试，直接抛出
                    logger.error(f"[重试-{name}] 未知异常（不重试）: {type(e).__name__}: {e}")
                    raise

            # 理论上不会到这里
            if last_exception:
                raise last_exception
            raise RuntimeError(f"[重试-{name}] 重试耗尽但无异常记录")

        return wrapper
    return decorator


# ─────────────────────────────────────────────────────────────────────────────
# HTTP状态码友好的重试封装
# ─────────────────────────────────────────────────────────────────────────────

def is_retryable_http_status(status_code: int) -> bool:
    """
    判断HTTP状态码是否值得重试。

    值得重试：408（请求超时）、429（限流）、5xx（服务端错误）、网络错误
    不值得重试：400/401/403/404/422（客户端错误，不会因重试而改变）
    """
    return status_code in {408, 429, 500, 502, 503, 504}


def http_retry_with_status(
    max_attempts: int = 3,
    base_delay: float = 0.5,      # v18.0: 1.0→0.5
    max_delay: float = 3.0,        # v18.0: 10.0→3.0
    retry_on_status: Tuple[int, ...] = (408, 429, 500, 502, 503, 504),
    no_retry_status: Tuple[int, ...] = (400, 401, 403, 404, 422),
    circuit_breaker: Optional[CircuitBreaker] = None,
    name: str = "http",
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    专门针对HTTP请求的重试装饰器，自动识别状态码决定是否重试。

    示例：
        @http_retry_with_status(name="deepseek", max_attempts=3)
        def call_deepseek(payload):
            resp = requests.post(url, json=payload, timeout=30)
            resp.raise_for_status()
            return resp.json()
    """
    config = RetryConfig(
        max_attempts=max_attempts,
        base_delay=base_delay,
        max_delay=max_delay,
        retryable_exceptions=(RetryableError, ConnectionError, TimeoutError),
    )

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            cb = circuit_breaker or get_circuit_breaker(name)
            last_err: Optional[Exception] = None

            for attempt in range(1, max_attempts + 1):
                if not cb.is_available():
                    raise NonRetryableError(f"服务 {name} 熔断中")

                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    last_err = e
                    cb.record_failure()

                    # 提取 HTTP 状态码
                    status_code = _extract_http_status(e)

                    # 不可重试的状态码
                    if status_code and status_code in no_retry_status:
                        logger.warning(
                            f"[HTTP重试-{name}] 状态码 {status_code} 不值得重试，直接抛出"
                        )
                        raise

                    # 可重试但已达最大次数
                    if attempt >= max_attempts:
                        logger.error(
                            f"[HTTP重试-{name}] 达到最大重试次数({max_attempts}): {e}"
                        )
                        raise

                    # 计算延迟
                    delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                    import random
                    delay = delay * (0.5 + random.random())

                    should_retry = (
                        status_code is None  # 网络错误
                        or (status_code and status_code in retry_on_status)
                    )

                    if should_retry:
                        logger.warning(
                            f"[HTTP重试-{name}] 第{attempt}次失败 "
                            f"(status={status_code}): {e}，{delay:.2f}s后重试..."
                        )
                        time.sleep(delay)
                    else:
                        raise

            if last_err:
                raise last_err
            raise RuntimeError(f"[HTTP重试-{name}] 重试耗尽")

        return wrapper
    return decorator


def _extract_http_status(e: Exception) -> Optional[int]:
    """从异常中提取HTTP状态码"""
    # 常见 HTTPError 包装
    for attr in ("code", "status_code", "status"):
        val = getattr(e, attr, None)
        if isinstance(val, int):
            return val
    return None


# ─────────────────────────────────────────────────────────────────────────────
# 简化版：直接使用的重试函数（不需要装饰器）
# ─────────────────────────────────────────────────────────────────────────────

def execute_with_retry(
    func: Callable[..., T],
    *args,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 10.0,
    retryable_exceptions: Tuple[type, ...] = (RetryableError, ConnectionError, TimeoutError),
    on_retry: Optional[Callable[[Exception, int], None]] = None,
    **kwargs,
) -> T:
    """
    直接调用的重试函数（装饰器的函数版）。

    用法：
        result = execute_with_retry(
            llm.chat,
            prompt="hello",
            max_attempts=3,
            base_delay=1.0,
        )
    """
    import random as _random

    last_exception: Optional[Exception] = None

    for attempt in range(1, max_attempts + 1):
        try:
            return func(*args, **kwargs)

        except NonRetryableError:
            raise

        except retryable_exceptions as e:
            last_exception = e

            if attempt >= max_attempts:
                logger.error(
                    f"[重试] 达到最大重试次数({max_attempts})，最后一次: {e}"
                )
                raise

            delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
            delay = delay * (0.5 + _random.random())

            logger.warning(
                f"[重试] 第{attempt}次失败: {type(e).__name__}: {e}，"
                f"{delay:.2f}s后重试..."
            )

            if on_retry:
                on_retry(e, attempt)

            time.sleep(delay)

        except Exception:
            raise

    if last_exception:
        raise last_exception
    raise RuntimeError("execute_with_retry: 耗尽但无异常")
