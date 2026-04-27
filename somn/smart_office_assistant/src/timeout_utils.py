"""
超时工具模块 - 为耗时操作添加超时保护

支持Windows和Unix系统
"""

import threading
import time
import logging
from typing import Callable, Any, Optional

logger = logging.getLogger(__name__)


class TimeoutException(Exception):
    """超时异常"""
    pass


def run_with_timeout(func: Callable, args: tuple = (), kwargs: dict = None,
                    timeout: float = 30.0, DESCRIPTION: str = "操作") -> Any:
    """
    在线程中运行函数，支持超时
    
    Args:
        func: 要执行的函数
        args: 位置参数
        kwargs: 关键字参数
        timeout: 超时时间（秒）
        description: 操作描述（用于日志）
    
    Returns:
        函数的返回值
    
    Raises:
        TimeoutException: 超时异常
        Exception: 函数执行的其他异常
    """
    if kwargs is None:
        kwargs = {}
    
    result = [None]
    exception = [None]
    finished = [False]
    
    def target():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            exception[0] = e
        finally:
            finished[0] = True
    
    thread = threading.Thread(target=target)
    thread.daemon = True
    
    start_time = time.time()
    logger.info(f"[超时保护] 开始执行: {DESCRIPTION} (超时: {timeout}s)")
    
    thread.start()
    thread.join(timeout)
    
    if thread.is_alive():
        elapsed = time.time() - start_time
        logger.error(f"[超时保护] {DESCRIPTION} 执行超时（{elapsed:.1f}s > {timeout}s）")
        raise TimeoutException(f"{DESCRIPTION} 执行超时（{timeout}秒）")
    
    elapsed = time.time() - start_time
    
    if exception[0]:
        logger.error(f"[超时保护] {DESCRIPTION} 执行失败（{elapsed:.1f}s）: {exception[0]}")
        raise exception[0]
    
    logger.info(f"[超时保护] {DESCRIPTION} 执行完成（{elapsed:.1f}s）")
    return result[0]


def with_timeout(timeout: float = 30.0, description: str = "操作"):
    """
    超时装饰器 - 为函数添加超时保护
    
    Args:
        timeout: 超时时间（秒）
        description: 操作描述
    
    Usage:
        @with_timeout(timeout=60.0, description="神经网络初始化")
        def initialize_neural_network():
            pass
    """
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            return run_with_timeout(func, args, kwargs, timeout, description)
        return wrapper
    return decorator


# ============================================================================
# 使用示例
# ============================================================================

if __name__ == "__main__":
    import time
    
    # 示例1: 使用 run_with_timeout
    def slow_function():
        time.sleep(5)
        return "完成"
    
    try:
        result = run_with_timeout(slow_function, timeout=3.0, description="慢速函数")
    except TimeoutException as e:
        print(f"超时: {e}")
    
    # 示例2: 使用装饰器
    @with_timeout(timeout=3.0, description="装饰器示例")
    def another_slow_function():
        time.sleep(5)
        return "完成"
    
    try:
        result = another_slow_function()
    except TimeoutException as e:
        print(f"超时: {e}")
    
    print("示例执行完成")
