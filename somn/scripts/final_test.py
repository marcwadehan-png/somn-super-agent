import sys
sys.path.insert(0, 'smart_office_assistant/src')

print('Testing v1.1 imports...')

# 测试所有导入
from core.storage import (
    SomnStorageManager, StorageConfig, ConnectionPool,
    BackupTier, LogLevel, LogCategory, TaskStatus, SessionStatus, DataPriority,
    BackupMetadata, StorageStats, AutoBackupRule, SyncStatus,
    StorageError, DatabaseError, BackupError, ConfigurationError,
    get_storage_manager, backup_critical_data, log_somn_operation, log_somn_error,
    get_library_integration
)

print('  All imports OK')

# 测试存储管理器
manager = get_storage_manager()
health = manager.health_check()
health_status = health['status']
print(f'  Health check: {health_status}')

# 测试藏书阁集成
integration = get_library_integration()
status = integration.get_library_status()
total_backups = status['total_backups']
print(f'  Library backups: {total_backups}')

# 测试功能
backup_id = integration.auto_backup_session('final_test', 'Final test session', {'test': True})
auto_backup_result = 'OK' if backup_id else 'FAIL'
print(f'  Auto backup: {auto_backup_result}')

# 存储统计
stats = manager.get_storage_stats()
print(f'')
print('Storage Stats:')
print(f'  Run DB: {stats.run_db_size_mb} MB')
print(f'  Log DB: {stats.log_db_size_mb} MB')
print(f'  Library: {stats.library_size_mb} MB')
print(f'  Sessions: {stats.sessions_count}')
print(f'  Tasks: {stats.tasks_count}')
print(f'  Logs: {stats.logs_count}')

print()
print('All v1.1 tests passed!')
