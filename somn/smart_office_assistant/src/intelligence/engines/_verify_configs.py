"""验证提取的task配置JSON完整性"""
import json
from pathlib import Path

config_path = Path(__file__).parent / "data" / "task_executor_configs.json"
with open(str(config_path), encoding='utf-8') as f:
    d = json.load(f)

print(f'Version: {d["version"]}')
print(f'Total: {d["total_tasks"]} tasks')
all_ok = True
for tid, cfg in d['tasks'].items():
    od = cfg.get('output_data', {})
    kf = cfg.get('key_findings', [])
    has_required = bool(cfg.get("task_id") and cfg.get("task_name") and cfg.get("phase") is not None)
    print(f'  {tid}: output_data keys={len(od)}, findings={len(kf)}, required_ok={has_required}')
    if not has_required:
        all_ok = False

# 验证P2T1的matrix数据（最复杂的执行器）
p2t1 = d['tasks'].get('P2-T1', {})
matrix = p2t1.get('output_data', {}).get('matrix', {})
if matrix:
    emotions = list(matrix.keys())
    behaviors = list(matrix[emotions[0]].keys()) if emotions else []
    print(f'\nP2-T1 Matrix: {len(emotions)} emotions x {len(behaviors)} behaviors')

if all_ok:
    print('\nALL 16 TASKS OK ✅')
