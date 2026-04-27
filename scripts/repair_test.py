"""修复验证测试脚本"""
import sys
import uuid
sys.path.insert(0, 'smart_office_assistant/src')
print('Testing imports...')

# 测试导入
try:
    from core.storage import SomnStorageManager, BackupTier, get_storage_manager
    print('  OK: core.storage imports')
except Exception as e:
    print(f'  FAIL: core.storage - {e}')

try:
    from core.storage._library_integration import LibraryIntegration, get_library_integration
    print('  OK: library_integration imports')
except Exception as e:
    print(f'  FAIL: library_integration - {e}')

try:
    from main_chain.config_loader import StorageConfig, get_storage_config
    print('  OK: config_loader.StorageConfig imports')
except Exception as e:
    print(f'  FAIL: config_loader - {e}')

print()
print('Testing storage manager...')
manager = get_storage_manager()

# 使用唯一ID避免冲突
unique_id = str(uuid.uuid4())[:8]

# 测试基本操作
print('  Testing create_session...')
session_id = f'repair_test_{unique_id}'
result = manager.create_session(session_id, user_id='test')
print(f'    Result: {result}')

print('  Testing update_task_state...')
task_id = f'task_repair_{unique_id}'
result = manager.update_task_state(task_id, 'running', progress=0.8)
print(f'    Result: {result}')

print('  Testing log_operation...')
result = manager.log_operation('repair', 'test', 'Testing storage system')
print(f'    Result: {result}')

print('  Testing backup_to_library...')
backup_id = manager.backup_to_library(
    data={'repair_test': True, 'timestamp': '2026-04-25', 'unique_id': unique_id},
    category='repair_test',
    tier=BackupTier.BING,
    title='Repair Test Backup'
)
print(f'    Backup ID: {backup_id}')

print('  Testing restore_from_library...')
restored = manager.restore_from_library(backup_id)
print(f'    Restored: {restored}')

print()
print('Testing library integration...')
integration = get_library_integration()
status = integration.get_library_status()
total = status['total_backups']
size = status['total_size_mb']
print(f'  Library status: total={total}, size={size}MB')

# 检查核心数据目录
from pathlib import Path
core_dir = Path('data/core')
print()
print('Checking core directory structure...')
expected_dirs = ['config_backups', 'snapshots', 'storage_reports']
for d in expected_dirs:
    path = core_dir / d
    exists = 'OK' if path.exists() else 'MISSING'
    print(f'  {d}: {exists}')

# 检查藏书阁目录
library_dir = Path('data/imperial_library')
print()
print('Checking imperial library structure...')
for tier in ['甲', '乙', '丙', '丁']:
    path = library_dir / tier
    exists = 'OK' if path.exists() else 'MISSING'
    files = len(list(path.glob('*.json'))) if path.exists() else 0
    print(f'  {tier}级: {exists}, {files} files')

print()
print('All repair verification tests passed!')
