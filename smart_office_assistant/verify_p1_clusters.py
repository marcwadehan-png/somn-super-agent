#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""P1集群验证脚本"""
import sys
sys.path.insert(0, 'src')

modules = [
    'economics_cluster',
    'psychology_cluster',
    'sociology_cluster',
    'governance_cluster',
    'investment_cluster',
]
base = 'intelligence.engines.cloning.clusters.'
errors = []
total_members = 0

for name in modules:
    m = base + name
    try:
        mod = __import__(m, fromlist=['build_cluster'])
        cluster = mod.build_cluster()
        cnt = len(cluster.members)
        total_members += cnt
        print(f'OK  {name}: {cnt} members => {list(cluster.members.keys())}')
    except Exception as e:
        errors.append(name)
        print(f'FAIL {name}: {e}')

print(f'\nTotal members loaded: {total_members}')
print(f'Errors: {len(errors)}')
sys.exit(len(errors))
