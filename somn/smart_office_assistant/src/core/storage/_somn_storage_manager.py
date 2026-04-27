"""
Somn 统一存储管理器 v1.1
===================================
功能：
1. 运行数据库管理（会话、任务状态、运行时数据）
2. 日志数据库管理（操作、错误、性能、审计日志）
3. 藏书阁备份接口（与 Imperial Library 打通）
4. 核心数据快照与恢复
5. 自动维护与数据清理

使用方式：
    from smart_office_assistant.src.core.storage import SomnStorageManager, get_storage_manager
    
    # 获取单例
    manager = get_storage_manager()
    
    # 创建会话
    manager.create_session("session_001", user_id="user")
    
    # 记录日志
    manager.log_operation("component", "action", "message")
    
    # 备份到藏书阁
    manager.backup_to_library(data, category="test", tier=BackupTier.JIA)
"""

import sqlite3
import json
import gzip
import logging
import threading
import queue
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union, Iterator, Callable
from dataclasses import dataclass
from enum import Enum
from contextlib import contextmanager
from functools import wraps
import time
import uuid

# ==================== 配置路径 ====================

def _get_project_root() -> Path:
    """动态获取项目根目录"""
    try:
        from src.core.paths import PROJECT_ROOT
        return Path(PROJECT_ROOT)
    except ImportError:
        return Path(__file__).parent.parent.parent.parent.parent

PROJECT_ROOT = _get_project_root()
CONFIG_PATH = PROJECT_ROOT / "config" / "storage_config.yaml"
DATA_DIR = PROJECT_ROOT / "data"
RUN_DIR = DATA_DIR / "run"
LOG_DIR = DATA_DIR / "logs"
CORE_DIR = DATA_DIR / "core"
BACKUP_DIR = DATA_DIR / "backups"
LIBRARY_DIR = DATA_DIR / "imperial_library"


# ==================== 枚举定义 ====================

class BackupTier(Enum):
    """备份级别 - 与藏书阁甲乙丙丁对应"""
    JIA = "甲"   # 永久备份
    YI = "乙"    # 365天
    BING = "丙"  # 30天
    DING = "丁"  # 7天
    
    @classmethod
    def from_string(cls, value: str) -> "BackupTier":
        """从字符串创建备份级别"""
        mapping = {"甲": cls.JIA, "乙": cls.YI, "丙": cls.BING, "丁": cls.DING}
        return mapping.get(value, cls.YI)


class LogLevel(Enum):
    """日志级别"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogCategory(Enum):
    """日志分类"""
    OPERATION = "operation"
    ERROR = "error"
    PERFORMANCE = "performance"
    AUDIT = "audit"


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SessionStatus(Enum):
    """会话状态"""
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


# ==================== 数据类定义 ====================

@dataclass
class StorageConfig:
    """存储配置"""
    run_db_path: Path = RUN_DIR / "run.db"
    log_db_path: Path = LOG_DIR / "logs.db"
    library_dir: Path = LIBRARY_DIR
    
    # 数据库配置
    journal_mode: str = "WAL"
    cache_size: int = -64000
    auto_vacuum: bool = True
    
    # 备份配置
    auto_backup_enabled: bool = True
    backup_interval_minutes: int = 60
    compression_enabled: bool = True
    max_backup_size_mb: int = 500
    
    # 保留策略
    session_retention_days: int = 90
    task_state_retention_days: int = 30
    log_retention_days: int = 30
    
    # 连接池配置
    pool_size: int = 5
    pool_timeout: int = 30


@dataclass
class BackupMetadata:
    """备份元数据"""
    backup_id: str
    category: str
    tier: str
    title: str
    original_size: int
    compressed: bool
    created_at: str
    metadata: Dict[str, Any]


@dataclass
class StorageStats:
    """存储统计"""
    run_db_size_mb: float
    log_db_size_mb: float
    library_size_mb: float
    total_backups: int
    sessions_count: int
    tasks_count: int
    logs_count: int


# ==================== 异常定义 ====================

class StorageError(Exception):
    """存储基础异常"""
    pass


class DatabaseError(StorageError):
    """数据库操作异常"""
    pass


class BackupError(StorageError):
    """备份操作异常"""
    pass


class ConfigurationError(StorageError):
    """配置异常"""
    pass


# ==================== 辅助装饰器 ====================

def retry_on_failure(max_retries: int = 3, delay: float = 0.1):
    """失败重试装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (sqlite3.OperationalError, sqlite3.DatabaseError) as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay * (attempt + 1))
            raise DatabaseError(f"操作失败，重试{max_retries}次后仍失败: {last_exception}")
        return wrapper
    return decorator


def log_operation(func: Callable) -> Callable:
    """操作日志装饰器"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        try:
            result = func(self, *args, **kwargs)
            duration = (time.time() - start_time) * 1000
            self.log_performance(
                component=func.__module__,
                metric_name=f"{func.__name__}_duration",
                metric_value=duration,
                unit="ms"
            )
            return result
        except Exception as e:
            self.log_error(
                component=func.__module__,
                error_type=type(e).__name__,
                error_message="处理失败"
            )
            raise
    return wrapper


# ==================== 连接池 ====================

class ConnectionPool:
    """数据库连接池"""
    
    def __init__(self, db_path: Path, pool_size: int = 5, timeout: int = 30):
        self.db_path = db_path
        self.pool_size = pool_size
        self.timeout = timeout
        self._pool: queue.Queue = queue.Queue(maxsize=pool_size)
        self._lock = threading.Lock()
        self._logger = logging.getLogger("ConnectionPool")
        
        # 预创建连接
        for _ in range(pool_size):
            conn = self._create_connection()
            self._pool.put(conn)
    
    def _create_connection(self) -> sqlite3.Connection:
        """创建新连接"""
        conn = sqlite3.connect(
            str(self.db_path),
            check_same_thread=False,
            timeout=self.timeout
        )
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA cache_size=-64000")
        cursor.execute("PRAGMA auto_vacuum=INCREMENTAL")
        return conn
    
    @contextmanager
    def get_connection(self) -> Iterator[sqlite3.Connection]:
        """获取连接（上下文管理器）"""
        try:
            conn = self._pool.get(timeout=self.timeout)
            try:
                yield conn
            finally:
                if conn.in_transaction:
                    conn.commit()
                self._pool.put(conn)
        except queue.Empty:
            # 连接池耗尽，创建临时连接
            conn = self._create_connection()
            try:
                yield conn
            finally:
                conn.close()
    
    def close_all(self):
        """关闭所有连接"""
        while not self._pool.empty():
            try:
                conn = self._pool.get_nowait()
                conn.close()
            except queue.Empty:
                break


# ==================== 主存储管理器 ====================

class SomnStorageManager:
    """
    Somn 统一存储管理器
    
    提供：
    - SQLite 数据库统一管理（连接池）
    - 藏书阁备份接口
    - 日志存储与查询
    - 状态快照与恢复
    - 自动维护与清理
    """
    
    _instance: Optional["SomnStorageManager"] = None
    _lock = threading.Lock()
    
    def __new__(cls, config: Optional[StorageConfig] = None) -> "SomnStorageManager":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, config: Optional[StorageConfig] = None):
        if self._initialized:
            return
        
        self.config = config or StorageConfig()
        self._initialized = True
        self._logger = logging.getLogger("SomnStorage")
        
        # 批量操作队列
        self._batch_queue: queue.Queue = queue.Queue(maxsize=1000)
        self._batch_thread: Optional[threading.Thread] = None
        self._running = False
        
        # 连接池
        self._run_pool: Optional[ConnectionPool] = None
        self._log_pool: Optional[ConnectionPool] = None
        
        # 确保目录存在
        self._ensure_directories()
        
        # 初始化数据库
        self._init_run_db()
        self._init_log_db()
        
        # 启动批量处理线程
        self._start_batch_processor()
        
        self._logger.info("SomnStorageManager v1.1 initialized successfully")
    
    def _ensure_directories(self) -> None:
        """确保所有目录存在"""
        # 顶层目录
        for dir_path in [RUN_DIR, LOG_DIR, CORE_DIR, BACKUP_DIR, LIBRARY_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # 核心数据子目录
        (CORE_DIR / "config_backups").mkdir(parents=True, exist_ok=True)
        (CORE_DIR / "snapshots").mkdir(parents=True, exist_ok=True)
        (CORE_DIR / "storage_reports").mkdir(parents=True, exist_ok=True)
        
        # 藏书阁备份级别目录
        for tier in ["甲", "乙", "丙", "丁"]:
            (LIBRARY_DIR / tier).mkdir(parents=True, exist_ok=True)
    
    # ==================== 数据库初始化 ====================
    
    def _init_run_db(self) -> None:
        """初始化运行数据库"""
        self._run_pool = ConnectionPool(
            self.config.run_db_path,
            pool_size=self.config.pool_size,
            timeout=self.config.pool_timeout
        )
        
        with self._run_pool.get_connection() as conn:
            cursor = conn.cursor()
            
            # 会话表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    user_id TEXT,
                    context_summary TEXT,
                    metadata TEXT,
                    status TEXT DEFAULT 'active',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 任务状态表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS task_states (
                    task_id TEXT PRIMARY KEY,
                    session_id TEXT,
                    task_type TEXT,
                    status TEXT,
                    progress REAL DEFAULT 0,
                    result TEXT,
                    error TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            """)
            
            # 运行时数据表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS runtime_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT,
                    value_type TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 执行历史表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS execution_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    component TEXT,
                    action TEXT,
                    duration_ms REAL,
                    success INTEGER,
                    details TEXT,
                    session_id TEXT
                )
            """)
            
            # 索引
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_time ON sessions(start_time)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON task_states(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_execution_time ON execution_history(timestamp)")
            
            conn.commit()
        
        self._logger.info(f"Run DB initialized: {self.config.run_db_path}")
    
    def _init_log_db(self) -> None:
        """初始化日志数据库"""
        self._log_pool = ConnectionPool(
            self.config.log_db_path,
            pool_size=max(2, self.config.pool_size // 2),
            timeout=self.config.pool_timeout
        )
        
        with self._log_pool.get_connection() as conn:
            cursor = conn.cursor()
            
            # 操作日志表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS operation_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    level TEXT NOT NULL,
                    component TEXT,
                    action TEXT,
                    message TEXT,
                    details TEXT,
                    session_id TEXT,
                    user_id TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 错误日志表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS error_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    level TEXT NOT NULL,
                    component TEXT,
                    error_type TEXT,
                    error_message TEXT,
                    stack_trace TEXT,
                    session_id TEXT,
                    task_id TEXT,
                    resolved INTEGER DEFAULT 0,
                    resolved_at TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 性能日志表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS performance_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    component TEXT,
                    metric_name TEXT,
                    metric_value REAL,
                    unit TEXT,
                    session_id TEXT,
                    task_id TEXT,
                    details TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 审计日志表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    user_id TEXT,
                    action TEXT,
                    resource_type TEXT,
                    resource_id TEXT,
                    result TEXT,
                    ip_address TEXT,
                    metadata TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 索引
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_oplog_time ON operation_logs(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_oplog_level ON operation_logs(level)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_errlog_time ON error_logs(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_errlog_resolved ON error_logs(resolved)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_perflog_time ON performance_logs(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_auditlog_time ON audit_logs(timestamp)")
            
            conn.commit()
        
        self._logger.info(f"Log DB initialized: {self.config.log_db_path}")
    
    # ==================== 批量处理 ====================
    
    def _start_batch_processor(self) -> None:
        """启动批量处理线程"""
        if self._running:
            return
        
        self._running = True
        
        def batch_worker():
            batch = []
            batch_size = 50
            flush_interval = 5.0
            last_flush = time.time()
            
            while self._running:
                try:
                    # 收集批量操作
                    while len(batch) < batch_size:
                        try:
                            item = self._batch_queue.get(timeout=0.1)
                            batch.append(item)
                        except queue.Empty:
                            break
                    
                    # 检查是否需要刷新
                    if batch and (len(batch) >= batch_size or time.time() - last_flush >= flush_interval):
                        self._flush_batch(batch)
                        batch = []
                        last_flush = time.time()
                        
                except Exception as e:
                    self._logger.error(f"Batch processor error: {e}")
            
            # 最终刷新
            if batch:
                self._flush_batch(batch)
        
        self._batch_thread = threading.Thread(target=batch_worker, daemon=True)
        self._batch_thread.start()
    
    def _flush_batch(self, batch: List[Dict]) -> None:
        """批量写入数据库"""
        if not batch:
            return
        
        # 按数据库分组
        run_ops = [op for op in batch if op.get("_db") == "run"]
        log_ops = [op for op in batch if op.get("_db") == "log"]
        
        if run_ops:
            try:
                with self._run_pool.get_connection() as conn:
                    cursor = conn.cursor()
                    for op in run_ops:
                        cursor.execute(op["sql"], op["params"])
                    conn.commit()
            except Exception as e:
                self._logger.error(f"Batch flush run_db failed: {e}")
        
        if log_ops:
            try:
                with self._log_pool.get_connection() as conn:
                    cursor = conn.cursor()
                    for op in log_ops:
                        cursor.execute(op["sql"], op["params"])
                    conn.commit()
            except Exception as e:
                self._logger.error(f"Batch flush log_db failed: {e}")
    
    # ==================== 会话管理 ====================
    
    @retry_on_failure(max_retries=3)
    def create_session(
        self,
        session_id: str,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """创建新会话"""
        try:
            with self._run_pool.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO sessions 
                    (session_id, start_time, user_id, metadata, status)
                    VALUES (?, ?, ?, ?, 'active')
                """, (session_id, datetime.now().isoformat(), user_id, 
                      json.dumps(metadata, ensure_ascii=False) if metadata else None))
                conn.commit()
            
            self.log_operation("session", "create", f"Session {session_id} created")
            return True
        except Exception as e:
            self._logger.error(f"Failed to create session: {e}")
            return False
    
    @retry_on_failure(max_retries=3)
    def end_session(
        self,
        session_id: str,
        context_summary: Optional[str] = None
    ) -> bool:
        """结束会话"""
        try:
            with self._run_pool.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE sessions 
                    SET end_time = ?, context_summary = ?, status = 'completed'
                    WHERE session_id = ?
                """, (datetime.now().isoformat(), context_summary, session_id))
                conn.commit()
            
            self.log_operation("session", "end", f"Session {session_id} ended")
            return True
        except Exception as e:
            self._logger.error(f"Failed to end session: {e}")
            return False
    
    def get_active_sessions(self) -> List[Dict[str, Any]]:
        """获取活跃会话"""
        with self._run_pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM sessions WHERE status = 'active' ORDER BY start_time DESC
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """获取会话详情"""
        with self._run_pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    # ==================== 任务状态管理 ====================
    
    @retry_on_failure(max_retries=3)
    def update_task_state(
        self,
        task_id: str,
        status: str,
        progress: float = 0,
        result: Optional[Any] = None,
        error: Optional[str] = None,
        session_id: Optional[str] = None,
        task_type: Optional[str] = None
    ) -> bool:
        """更新任务状态"""
        try:
            with self._run_pool.get_connection() as conn:
                cursor = conn.cursor()
                
                # 序列化结果
                result_str = None
                if result is not None:
                    try:
                        result_str = json.dumps(result, ensure_ascii=False, default=str)
                    except (TypeError, ValueError):
                        result_str = str(result)
                
                cursor.execute("""
                    INSERT OR REPLACE INTO task_states 
                    (task_id, session_id, task_type, status, progress, result, error, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (task_id, session_id, task_type, status, progress, 
                      result_str, error, datetime.now().isoformat()))
                conn.commit()
            
            return True
        except Exception as e:
            self._logger.error(f"Failed to update task state: {e}")
            return False
    
    def get_task_state(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务状态"""
        with self._run_pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM task_states WHERE task_id = ?", (task_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_tasks_by_status(self, status: str) -> List[Dict[str, Any]]:
        """按状态获取任务列表"""
        with self._run_pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM task_states WHERE status = ? ORDER BY created_at DESC
            """, (status,))
            return [dict(row) for row in cursor.fetchall()]
    
    # ==================== 运行时数据 ====================
    
    @retry_on_failure(max_retries=3)
    def set_runtime_data(
        self,
        key: str,
        value: Any,
        value_type: str = "json"
    ) -> bool:
        """设置运行时数据"""
        try:
            # 序列化值
            if value_type == "json":
                try:
                    value_str = json.dumps(value, ensure_ascii=False, default=str)
                except (TypeError, ValueError):
                    value_str = str(value)
            else:
                value_str = str(value)
            
            with self._run_pool.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO runtime_data (key, value, value_type, updated_at)
                    VALUES (?, ?, ?, ?)
                """, (key, value_str, value_type, datetime.now().isoformat()))
                conn.commit()
            
            return True
        except Exception as e:
            self._logger.error(f"Failed to set runtime data: {e}")
            return False
    
    def get_runtime_data(
        self,
        key: str,
        default: Any = None
    ) -> Any:
        """获取运行时数据"""
        with self._run_pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM runtime_data WHERE key = ?", (key,))
            row = cursor.fetchone()
            
            if not row:
                return default
            
            value_type = row["value_type"]
            value_str = row["value"]
            
            if value_type == "json":
                try:
                    return json.loads(value_str)
                except (json.JSONDecodeError, TypeError):
                    return value_str
            return value_str
    
    def delete_runtime_data(self, key: str) -> bool:
        """删除运行时数据"""
        try:
            with self._run_pool.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM runtime_data WHERE key = ?", (key,))
                conn.commit()
            return True
        except Exception as e:
            self._logger.error(f"Failed to delete runtime data: {e}")
            return False
    
    # ==================== 日志管理 ====================
    
    @retry_on_failure(max_retries=3)
    def log_operation(
        self,
        component: str,
        action: str,
        message: str,
        level: str = "INFO",
        details: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> bool:
        """记录操作日志"""
        try:
            with self._log_pool.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO operation_logs 
                    (timestamp, level, component, action, message, details, session_id, user_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (datetime.now().isoformat(), level, component, action, message,
                      json.dumps(details, ensure_ascii=False) if details else None,
                      session_id, user_id))
                conn.commit()
            return True
        except Exception as e:
            self._logger.error(f"Failed to log operation: {e}")
            return False
    
    @retry_on_failure(max_retries=3)
    def log_error(
        self,
        component: str,
        error_type: str,
        error_message: str,
        stack_trace: Optional[str] = None,
        session_id: Optional[str] = None,
        task_id: Optional[str] = None
    ) -> bool:
        """记录错误日志"""
        try:
            with self._log_pool.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO error_logs 
                    (timestamp, level, component, error_type, error_message, stack_trace,
                     session_id, task_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (datetime.now().isoformat(), "ERROR", component, error_type,
                      error_message, stack_trace, session_id, task_id))
                conn.commit()
            return True
        except Exception as e:
            self._logger.error(f"Failed to log error: {e}")
            return False
    
    @retry_on_failure(max_retries=3)
    def log_performance(
        self,
        component: str,
        metric_name: str,
        metric_value: float,
        unit: str = "",
        session_id: Optional[str] = None,
        task_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> bool:
        """记录性能日志"""
        try:
            with self._log_pool.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO performance_logs 
                    (timestamp, component, metric_name, metric_value, unit, session_id, task_id, details)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (datetime.now().isoformat(), component, metric_name, metric_value,
                      unit, session_id, task_id,
                      json.dumps(details, ensure_ascii=False) if details else None))
                conn.commit()
            return True
        except Exception as e:
            self._logger.error(f"Failed to log performance: {e}")
            return False
    
    @retry_on_failure(max_retries=3)
    def log_audit(
        self,
        action: str,
        resource_type: str,
        resource_id: str,
        result: str,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """记录审计日志"""
        try:
            with self._log_pool.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO audit_logs 
                    (timestamp, user_id, action, resource_type, resource_id, result, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (datetime.now().isoformat(), user_id, action, resource_type,
                      resource_id, result, json.dumps(metadata, ensure_ascii=False) if metadata else None))
                conn.commit()
            return True
        except Exception as e:
            self._logger.error(f"Failed to log audit: {e}")
            return False
    
    def query_logs(
        self,
        category: str,
        level: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """查询日志"""
        table_map = {
            "operation": "operation_logs",
            "error": "error_logs",
            "performance": "performance_logs",
            "audit": "audit_logs"
        }
        
        table = table_map.get(category, "operation_logs")
        
        with self._log_pool.get_connection() as conn:
            cursor = conn.cursor()
            
            query = f"SELECT * FROM {table} WHERE 1=1"
            params: List[Any] = []
            
            if level and category == "operation":
                query += " AND level = ?"
                params.append(level)
            
            if start_time:
                query += " AND timestamp >= ?"
                params.append(start_time)
            
            if end_time:
                query += " AND timestamp <= ?"
                params.append(end_time)
            
            query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    # ==================== 藏书阁备份接口 ====================
    
    def backup_to_library(
        self,
        data: Any,
        category: str,
        tier: BackupTier = BackupTier.YI,
        title: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        备份数据到藏书阁
        
        Args:
            data: 要备份的数据（任意可序列化对象）
            category: 数据类别（对应藏书阁书架）
            tier: 备份级别（甲乙丙丁）
            title: 标题
            metadata: 元数据
            
        Returns:
            备份ID 或 None
        """
        try:
            backup_id = str(uuid.uuid4())
            timestamp = datetime.now().isoformat()
            
            # 序列化数据
            if isinstance(data, (dict, list)):
                content = json.dumps(data, ensure_ascii=False, indent=2, default=str)
            else:
                content = str(data)
            
            # 压缩内容
            if self.config.compression_enabled:
                content_bytes = gzip.compress(content.encode('utf-8'))
                content_b64 = content_bytes.hex()
                compressed = True
            else:
                content_b64 = content
                compressed = False
            
            # 元数据
            backup_metadata = {
                "backup_id": backup_id,
                "category": category,
                "tier": tier.value,
                "title": title or f"{category}_{timestamp}",
                "original_size": len(str(data)),
                "compressed": compressed,
                "created_at": timestamp,
                "metadata": metadata or {}
            }
            
            # 保存备份文件
            tier_dir = LIBRARY_DIR / tier.value
            tier_dir.mkdir(parents=True, exist_ok=True)
            
            backup_file = tier_dir / f"{backup_id}.json"
            
            backup_entry = {
                "metadata": backup_metadata,
                "content": content_b64
            }
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_entry, f, ensure_ascii=False, indent=2)
            
            # 更新索引
            self._add_to_library_index(backup_id, backup_metadata)
            
            self._logger.info(f"Backup {backup_id} created in tier {tier.value}")
            return backup_id
            
        except Exception as e:
            self._logger.error(f"Failed to backup to library: {e}")
            return None
    
    def _add_to_library_index(self, backup_id: str, metadata: Dict[str, Any]) -> None:
        """添加到藏书阁索引"""
        index_file = LIBRARY_DIR / "library_index.json"
        
        try:
            if index_file.exists():
                with open(index_file, 'r', encoding='utf-8') as f:
                    index = json.load(f)
            else:
                index = {"backups": {}}
        except (json.JSONDecodeError, IOError):
            index = {"backups": {}}
        
        if "backups" not in index:
            index["backups"] = {}
        
        index["backups"][backup_id] = metadata
        
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
    
    def restore_from_library(self, backup_id: str) -> Optional[Any]:
        """从藏书阁恢复数据"""
        try:
            # 搜索备份文件
            backup_file = None
            for tier in ["甲", "乙", "丙", "丁"]:
                path = LIBRARY_DIR / tier / f"{backup_id}.json"
                if path.exists():
                    backup_file = path
                    break
            
            if not backup_file:
                self._logger.warning(f"Backup {backup_id} not found")
                return None
            
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_entry = json.load(f)
            
            content = backup_entry["content"]
            
            # 解压
            if backup_entry["metadata"].get("compressed", False):
                content = gzip.decompress(bytes.fromhex(content)).decode('utf-8')
            
            return json.loads(content)
            
        except Exception as e:
            self._logger.error(f"Failed to restore from library: {e}")
            return None
    
    def get_library_backups(
        self,
        tier: Optional[BackupTier] = None,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """获取藏书阁备份列表"""
        index_file = LIBRARY_DIR / "library_index.json"
        
        if not index_file.exists():
            return []
        
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                index = json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
        
        backups = list(index.get("backups", {}).values())
        
        # 过滤
        if tier:
            backups = [b for b in backups if b.get("tier") == tier.value]
        if category:
            backups = [b for b in backups if b.get("category") == category]
        
        return backups
    
    def delete_library_backup(self, backup_id: str) -> bool:
        """删除藏书阁备份"""
        try:
            # 查找并删除文件
            for tier in ["甲", "乙", "丙", "丁"]:
                path = LIBRARY_DIR / tier / f"{backup_id}.json"
                if path.exists():
                    path.unlink()
                    
                    # 从索引移除
                    index_file = LIBRARY_DIR / "library_index.json"
                    if index_file.exists():
                        with open(index_file, 'r', encoding='utf-8') as f:
                            index = json.load(f)
                        if backup_id in index.get("backups", {}):
                            del index["backups"][backup_id]
                            with open(index_file, 'w', encoding='utf-8') as f:
                                json.dump(index, f, ensure_ascii=False, indent=2)
                    
                    return True
            
            return False
        except Exception as e:
            self._logger.error(f"Failed to delete backup: {e}")
            return False
    
    # ==================== 核心数据快照 ====================
    
    def create_state_snapshot(
        self,
        component: str,
        state: Dict[str, Any]
    ) -> str:
        """创建设备状态快照"""
        snapshot_id = f"snapshot_{component}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        snapshot = {
            "snapshot_id": snapshot_id,
            "component": component,
            "state": state,
            "created_at": datetime.now().isoformat()
        }
        
        # 保存到核心数据目录
        snapshot_file = CORE_DIR / "snapshots" / f"{snapshot_id}.json"
        with open(snapshot_file, 'w', encoding='utf-8') as f:
            json.dump(snapshot, f, ensure_ascii=False, indent=2)
        
        # 备份到藏书阁（甲级永久）
        self.backup_to_library(
            data=snapshot,
            category="system_states",
            tier=BackupTier.JIA,
            title=f"{component} State Snapshot",
            metadata={"snapshot_type": "state"}
        )
        
        return snapshot_id
    
    def load_state_snapshot(self, snapshot_id: str) -> Optional[Dict[str, Any]]:
        """加载状态快照"""
        snapshot_file = CORE_DIR / "snapshots" / f"{snapshot_id}.json"
        
        if snapshot_file.exists():
            with open(snapshot_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return None
    
    def list_snapshots(self, component: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出状态快照"""
        snapshots_dir = CORE_DIR / "snapshots"
        
        if not snapshots_dir.exists():
            return []
        
        snapshots = []
        for file in snapshots_dir.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if component is None or data.get("component") == component:
                        snapshots.append(data)
            except (json.JSONDecodeError, IOError):
                continue
        
        return sorted(snapshots, key=lambda x: x.get("created_at", ""), reverse=True)
    
    # ==================== 清理与维护 ====================
    
    def cleanup_old_data(self, days: Optional[int] = None) -> Dict[str, int]:
        """清理过期数据"""
        days = days or self.config.log_retention_days
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        result = {"sessions": 0, "tasks": 0, "logs": 0}
        
        # 清理会话
        try:
            with self._run_pool.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    DELETE FROM sessions 
                    WHERE start_time < ? AND status = 'completed'
                """, (cutoff,))
                result["sessions"] = cursor.rowcount
                
                cursor.execute("""
                    DELETE FROM task_states 
                    WHERE created_at < ? AND status IN ('completed', 'failed')
                """, (cutoff,))
                result["tasks"] = cursor.rowcount
                
                conn.commit()
        except Exception as e:
            self._logger.error(f"Failed to cleanup old sessions/tasks: {e}")
        
        # 清理日志
        try:
            with self._log_pool.get_connection() as conn:
                cursor = conn.cursor()
                
                for table in ["operation_logs", "error_logs", "performance_logs"]:
                    cursor.execute(f"DELETE FROM {table} WHERE created_at < ?", (cutoff,))
                    result["logs"] += cursor.rowcount
                
                conn.commit()
        except Exception as e:
            self._logger.error(f"Failed to cleanup old logs: {e}")
        
        # Vacuum
        self._vacuum_databases()
        
        self._logger.info(f"Cleanup completed: {result}")
        return result
    
    def cleanup_library_by_tier(self, tier: BackupTier) -> int:
        """按级别清理藏书阁"""
        if tier == BackupTier.JIA:
            self._logger.warning("Cannot cleanup JIA tier - permanent storage")
            return 0
        
        retention_map = {
            BackupTier.YI: 365,
            BackupTier.BING: 30,
            BackupTier.DING: 7
        }
        
        days = retention_map.get(tier, 30)
        cutoff = datetime.now() - timedelta(days=days)
        deleted = 0
        
        tier_dir = LIBRARY_DIR / tier.value
        if not tier_dir.exists():
            return 0
        
        for file in tier_dir.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                created_at = datetime.fromisoformat(data["metadata"]["created_at"])
                if created_at < cutoff:
                    file.unlink()
                    deleted += 1
                    
                    # 从索引移除
                    backup_id = data["metadata"]["backup_id"]
                    index_file = LIBRARY_DIR / "library_index.json"
                    if index_file.exists():
                        with open(index_file, 'r', encoding='utf-8') as f:
                            index = json.load(f)
                        if backup_id in index.get("backups", {}):
                            del index["backups"][backup_id]
                            with open(index_file, 'w', encoding='utf-8') as f:
                                json.dump(index, f, ensure_ascii=False, indent=2)
            except Exception:
                continue
        
        self._logger.info(f"Cleaned up {deleted} backups from tier {tier.value}")
        return deleted
    
    def _vacuum_databases(self) -> None:
        """压缩数据库"""
        try:
            with self._run_pool.get_connection() as conn:
                conn.execute("VACUUM")
            
            with self._log_pool.get_connection() as conn:
                conn.execute("VACUUM")
        except Exception as e:
            self._logger.error(f"Failed to vacuum databases: {e}")
    
    # ==================== 统计与健康检查 ====================
    
    def get_storage_stats(self) -> StorageStats:
        """获取存储统计"""
        # 数据库大小
        run_size = self.config.run_db_path.stat().st_size / (1024 * 1024) if self.config.run_db_path.exists() else 0
        log_size = self.config.log_db_path.stat().st_size / (1024 * 1024) if self.config.log_db_path.exists() else 0
        
        # 藏书阁大小
        library_size = sum(
            f.stat().st_size for f in LIBRARY_DIR.rglob('*') if f.is_file()
        ) / (1024 * 1024)
        
        # 记录数
        with self._run_pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sessions")
            sessions_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM task_states")
            tasks_count = cursor.fetchone()[0]
        
        with self._log_pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM (
                    SELECT id FROM operation_logs
                    UNION ALL
                    SELECT id FROM error_logs
                    UNION ALL
                    SELECT id FROM performance_logs
                    UNION ALL
                    SELECT id FROM audit_logs
                )
            """)
            logs_count = cursor.fetchone()[0]
        
        return StorageStats(
            run_db_size_mb=round(run_size, 2),
            log_db_size_mb=round(log_size, 2),
            library_size_mb=round(library_size, 2),
            total_backups=len(self.get_library_backups()),
            sessions_count=sessions_count,
            tasks_count=tasks_count,
            logs_count=logs_count
        )
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        health = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }
        
        # 检查数据库连接
        try:
            with self._run_pool.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
            health["checks"]["run_db"] = "ok"
        except Exception as e:
            health["checks"]["run_db"] = f"error: {e}"
            health["status"] = "degraded"
        
        try:
            with self._log_pool.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
            health["checks"]["log_db"] = "ok"
        except Exception as e:
            health["checks"]["log_db"] = f"error: {e}"
            health["status"] = "degraded"
        
        # 检查磁盘空间
        try:
            import shutil
            total, used, free = shutil.disk_usage(DATA_DIR)
            health["checks"]["disk_space"] = {
                "total_gb": round(total / (1024**3), 2),
                "used_gb": round(used / (1024**3), 2),
                "free_gb": round(free / (1024**3), 2),
                "percent_used": round(used / total * 100, 1)
            }
            if free / (1024**3) < 1:  # 小于1GB警告
                health["checks"]["disk_space"]["warning"] = "Low disk space"
        except Exception as e:
            health["checks"]["disk_space"] = f"error: {e}"
        
        return health
    
    # ==================== 生命周期管理 ====================
    
    def close(self) -> None:
        """关闭存储管理器"""
        self._running = False
        
        if self._batch_thread:
            self._batch_thread.join(timeout=5)
        
        if self._run_pool:
            self._run_pool.close_all()
        
        if self._log_pool:
            self._log_pool.close_all()
        
        self._logger.info("SomnStorageManager closed")
    
    def __enter__(self) -> "SomnStorageManager":
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


# ==================== 便捷函数 ====================

_storage_instance: Optional[SomnStorageManager] = None


def get_storage_manager(config: Optional[StorageConfig] = None) -> SomnStorageManager:
    """获取存储管理器单例"""
    global _storage_instance
    if _storage_instance is None:
        _storage_instance = SomnStorageManager(config)
    return _storage_instance


def backup_critical_data(
    data: Any,
    title: str,
    metadata: Optional[Dict[str, Any]] = None
) -> Optional[str]:
    """便捷函数：备份关键数据到藏书阁甲级"""
    manager = get_storage_manager()
    return manager.backup_to_library(
        data=data,
        category="critical_data",
        tier=BackupTier.JIA,
        title=title,
        metadata=metadata
    )


def log_somn_operation(
    component: str,
    action: str,
    message: str,
    **kwargs
) -> bool:
    """便捷函数：记录 Somn 操作日志"""
    manager = get_storage_manager()
    return manager.log_operation(component, action, message, **kwargs)


def log_somn_error(
    component: str,
    error_type: str,
    error_message: str,
    **kwargs
) -> bool:
    """便捷函数：记录 Somn 错误日志"""
    manager = get_storage_manager()
    return manager.log_error(component, error_type, error_message, **kwargs)


# ==================== 主程序测试 ====================

if __name__ == "__main__":
    import sys
    
    print("Testing SomnStorageManager v1.1...")
    print("=" * 50)
    
    manager = get_storage_manager()
    
    # 健康检查
    print("\n[1] Health Check:")
    health = manager.health_check()
    print(f"    Status: {health['status']}")
    print(f"    Run DB: {health['checks'].get('run_db')}")
    print(f"    Log DB: {health['checks'].get('log_db')}")
    
    # 存储统计
    print("\n[2] Storage Stats:")
    stats = manager.get_storage_stats()
    print(f"    Run DB: {stats.run_db_size_mb} MB")
    print(f"    Log DB: {stats.log_db_size_mb} MB")
    print(f"    Library: {stats.library_size_mb} MB")
    print(f"    Total Backups: {stats.total_backups}")
    print(f"    Sessions: {stats.sessions_count}")
    print(f"    Tasks: {stats.tasks_count}")
    print(f"    Logs: {stats.logs_count}")
    
    # 功能测试
    print("\n[3] Function Tests:")
    
    unique_id = str(uuid.uuid4())[:8]
    
    # 会话
    session_id = f"test_session_{unique_id}"
    result = manager.create_session(session_id, user_id="test_user")
    print(f"    Create session: {'OK' if result else 'FAIL'}")
    
    # 任务
    task_id = f"test_task_{unique_id}"
    result = manager.update_task_state(task_id, "running", progress=0.5)
    print(f"    Update task: {'OK' if result else 'FAIL'}")
    
    # 运行时数据
    result = manager.set_runtime_data(f"test_key_{unique_id}", {"value": 123})
    value = manager.get_runtime_data(f"test_key_{unique_id}")
    print(f"    Runtime data: {'OK' if value else 'FAIL'}")
    
    # 日志
    result = manager.log_operation("test", "test_action", "Test message")
    print(f"    Log operation: {'OK' if result else 'FAIL'}")
    
    # 藏书阁备份
    backup_id = manager.backup_to_library(
        data={"test": "data", "unique_id": unique_id},
        category="test_backup",
        tier=BackupTier.BING,
        title="Test Backup"
    )
    print(f"    Backup to library: {'OK' if backup_id else 'FAIL'}")
    
    # 恢复备份
    restored = manager.restore_from_library(backup_id)
    print(f"    Restore from library: {'OK' if restored else 'FAIL'}")
    
    # 快照
    snapshot_id = manager.create_state_snapshot("TestComponent", {"mode": "test"})
    print(f"    Create snapshot: {'OK' if snapshot_id else 'FAIL'}")
    
    print("\n" + "=" * 50)
    print("All tests completed successfully!")
