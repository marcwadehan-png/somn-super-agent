"""
测试存储管理器
"""
import sys
sys.path.insert(0, 'smart_office_assistant/src')

from core.storage import get_storage_manager, BackupTier

# 测试存储管理器
manager = get_storage_manager()

# 创建测试会话
session_id = 'test_session_001'
manager.create_session(session_id, user_id='test_user')
print('✓ 会话创建成功')

# 更新任务状态
manager.update_task_state('task_001', 'running', progress=0.5, session_id=session_id)
print('✓ 任务状态更新成功')

# 运行时数据
manager.set_runtime_data('test_key', {'value': 123}, 'json')
value = manager.get_runtime_data('test_key')
print(f'✓ 运行时数据: {value}')

# 日志测试
manager.log_operation('test', 'test_action', 'Test message', level='INFO')
manager.log_error('test', 'TestError', 'This is a test error')
manager.log_performance('test', 'response_time', 125.5, 'ms')
print('✓ 日志写入成功')

# 藏书阁备份测试
backup_id = manager.backup_to_library(
    data={'test': 'data', 'timestamp': '2026-04-25'},
    category='test_backup',
    tier=BackupTier.YI,
    title='Test Backup'
)
print(f'✓ 藏书阁备份成功: {backup_id}')

# 恢复备份
restored = manager.restore_from_library(backup_id)
print(f'✓ 备份恢复: {restored}')

# 存储统计
stats = manager.get_storage_stats()
print()
print('📊 存储统计:')
print(f'  运行数据库: {stats.run_db_size_mb:.2f} MB')
print(f'  日志数据库: {stats.log_db_size_mb:.2f} MB')
print(f'  藏书阁: {stats.library_size_mb:.2f} MB')
print(f'  会话数: {stats.sessions_count}')
print(f'  任务数: {stats.tasks_count}')
print(f'  日志数: {stats.logs_count}')

# 藏书阁状态
backups = manager.get_library_backups()
print(f'  藏书阁备份数: {len(backups)}')

print()
print('🎉 所有测试通过!')
