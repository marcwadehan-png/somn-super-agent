"""
Somn 存储模块 v1.1
===================================
提供统一存储管理功能：
- 运行数据库
- 日志数据库
- 藏书阁备份
- 连接池管理
- 自动维护
"""

from ._somn_storage_manager import (
    # 主类
    SomnStorageManager,
    StorageConfig,
    ConnectionPool,

    # 枚举
    BackupTier,
    LogLevel,
    LogCategory,
    TaskStatus,
    SessionStatus,

    # 数据类
    BackupMetadata,
    StorageStats,

    # 异常
    StorageError,
    DatabaseError,
    BackupError,
    ConfigurationError,

    # 便捷函数
    get_storage_manager,
    backup_critical_data,
    log_somn_operation,
    log_somn_error,

    # 装饰器
    retry_on_failure,
    log_operation,
)

from ._library_integration import (
    # 主类
    LibraryIntegration,

    # 枚举
    DataPriority,

    # 数据类
    AutoBackupRule,
    SyncStatus,

    # 便捷函数
    get_library_integration,

    # 装饰器
    auto_backup_to_library,
)

__all__ = [
    # 主类
    "SomnStorageManager",
    "StorageConfig",
    "ConnectionPool",
    "LibraryIntegration",

    # 枚举
    "BackupTier",
    "LogLevel",
    "LogCategory",
    "TaskStatus",
    "SessionStatus",
    "DataPriority",

    # 数据类
    "BackupMetadata",
    "StorageStats",
    "AutoBackupRule",
    "SyncStatus",

    # 异常
    "StorageError",
    "DatabaseError",
    "BackupError",
    "ConfigurationError",

    # 便捷函数
    "get_storage_manager",
    "backup_critical_data",
    "log_somn_operation",
    "log_somn_error",
    "get_library_integration",

    # 装饰器
    "retry_on_failure",
    "log_operation",
    "auto_backup_to_library",
]

__version__ = "1.1"
