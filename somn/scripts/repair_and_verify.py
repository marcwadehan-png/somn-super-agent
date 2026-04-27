import sys
sys.path.insert(0, 'smart_office_assistant/src')

from core.storage import get_library_integration

integration = get_library_integration()

# 修复索引
repaired = integration.repair_library_index()
print(f'Repaired {repaired} entries')

# 验证完整性
integrity = integration.validate_library_integrity()
is_valid = integrity['is_valid']
orphaned = len(integrity['orphaned_files'])
missing = len(integrity['missing_from_index'])
corrupted = len(integrity['corrupted_backups'])

print(f'Is valid: {is_valid}')
print(f'Orphaned files: {orphaned}')
print(f'Missing from index: {missing}')
print(f'Corrupted: {corrupted}')

# 获取藏书阁状态
status = integration.get_library_status()
total = status['total_backups']
size = status['total_size_mb']
tiers = status['tier_distribution']

print(f'')
print(f'Library Status:')
print(f'  Total backups: {total}')
print(f'  Size: {size} MB')
print(f'  Tiers: {tiers}')
