#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
全局代码优化工具 v2.0
Global Code Optimization Tool v2.0

功能：
1. 合并重复模块
2. 重命名冲突文件
3. 替换中文标点符号
4. 生成优化报告

使用方法：
python global_optimizer.py --merge     # 合并重复模块
python global_optimizer.py --rename    # 重命名冲突文件
python global_optimizer.py --punct     # 替换中文标点
python global_optimizer.py --all       # 执行全部优化
"""

import os
import re
import json
import shutil
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import argparse

# ============================================================
# 1. 中文标点符号映射
# ============================================================
CHINESE_PUNCT_TO_ASCII = {
    '「': '"', '」': '"',
    '『': "'", '』': "'",
    '【': '[', '】': ']',
    '（': '(', '）': ')',
    '《': '<', '》': '>',
    '〈': '<', '〉': '>',
    '！': '!', '？': '?',
    '。': '.', '，': ',',
    '；': ';', '：': ':',
    '、': ',',
    '～': '~',
    '……': '...', '…': '...',
    '—': '-', '–': '-',
    '｜': '|',
}

# ============================================================
# 2. 文件合并映射表
# ============================================================
MERGE_MAPPINGS = {
    # Memory模块 - 合并到主版本
    'neural_memory/memory_engine_v2.py': 'neural_memory/memory_engine.py',
    'neural_memory/optimized_memory_engine.py': 'neural_memory/memory_engine.py',
    'neural_memory/memory_enhanced_v3.py': 'neural_memory/memory_engine.py',
    'neural_memory/memory_granularity_v3.py': 'neural_memory/memory_engine.py',
    'neural_memory/memory_richness_v3.py': 'neural_memory/memory_engine.py',
    'neural_memory/memory_encoding_system_v31.py': 'neural_memory/memory_encoding_system_v3.py',

    # Reasoning模块 - 合并到主版本
    'neural_memory/enhanced_reasoning_engine.py': 'neural_memory/reasoning_engine.py',
    'intelligence/enhanced_reasoning_engine.py': 'neural_memory/reasoning_engine.py',

    # Wisdom协调器 - 合并
    'intelligence/supreme_wisdom_coordinator.py': 'intelligence/super_wisdom_coordinator.py',
}

# ============================================================
# 3. 文件重命名映射表
# ============================================================
RENAME_MAPPINGS = {
    # Wisdom重命名（功能区分）
    'intelligence/wisdom_risk_warning.py': 'intelligence/risk_warning_wisdom.py',
    'intelligence/wisdom_talent_assessor.py': 'intelligence/talent_assessment_wisdom.py',
    'intelligence/wisdom_reasoning_engine.py': 'intelligence/strategic_reasoning_engine.py',

    # 知识图谱推理引擎重命名
    'knowledge_graph/reasoning_engine_v2.py': 'knowledge_graph/knowledge_reasoning_engine.py',

    # Growth引擎版本统一
    'growth_engine/engine_v2.py': 'growth_engine/growth_engine.py',
    'growth_engine/solution_templates_v2.py': 'growth_engine/solution_templates.py',
    'growth_engine/solution_learning_v2.py': 'growth_engine/solution_learning.py',

    # 行业引擎版本统一
    'industry_engine/industry_profiles_v2.py': 'industry_engine/industry_profiles.py',
}

# ============================================================
# 4. 待删除文件列表（废弃/备份文件）
# ============================================================
DELETE_FILES = [
    # 备份文件
    'intelligence/persona_core_v101_backup.py',
    'intelligence/_build_tender_engine.py',
    'intelligence/_build_v112_heal.py',
    'intelligence/_build_v112_heal_v2.py',
    'intelligence/_build_neural_core.py',
    'intelligence/_fix_neural_build.py',
    'intelligence/_verify_v102.py',
    'intelligence/_verify_v110.py',
    'intelligence/_verify_v111.py',
    'intelligence/_verify_v111_exact.py',
    'intelligence/_verify_v111_same_topic.py',
    'intelligence/_verify_v112_full.py',
    'intelligence/_verify_v112_nvc.py',
    'intelligence/_verify_v1121.py',
    'intelligence/_verify_brief.py',
    'intelligence/_verify_neural.py',
    'intelligence/_verify_emoji.py',
    'intelligence/_verify_sticker.py',
    'intelligence/_check_nvc.py',
    'intelligence/_fix_heal_json.py',
    'intelligence/_fix_json_clean.py',
    'intelligence/_rebuild_v102.py',
    'intelligence/_inject_neural_core.py',
    'intelligence/_inject_tender_engine.py',
    'intelligence/test_wisdom_system.py',
]


@dataclass
class OptimizationResult:
    """优化结果"""
    operation: str
    source: str
    target: str
    status: str  # success, skipped, error
    message: str
    timestamp: str


class GlobalOptimizer:
    """全局代码优化器"""

    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.results: List[OptimizationResult] = []
        self.stats = {
            'merged': 0,
            'renamed': 0,
            'deleted': 0,
            'punct_fixed': 0,
            'errors': 0,
        }

    def _now(self) -> str:
        return datetime.now().isoformat()

    def _log(self, op: str, src: str, tgt: str, status: str, msg: str):
        self.results.append(OptimizationResult(
            operation=op,
            source=src,
            target=tgt,
            status=status,
            message=msg,
            timestamp=self._now()
        ))

    # --------------------------------------------------------
    # 1. 合并模块
    # --------------------------------------------------------
    def merge_modules(self, dry_run: bool = True):
        """合并重复模块"""
        print("\n=== 合并重复模块 ===")

        for src_rel, tgt_rel in MERGE_MAPPINGS.items():
            src = self.root_path / src_rel
            tgt = self.root_path / tgt_rel

            if not src.exists():
                self._log('MERGE', src_rel, tgt_rel, 'skipped', '源文件不存在')
                print(f"  [SKIP] {src_rel} (不存在)")
                continue

            if dry_run:
                self._log('MERGE', src_rel, tgt_rel, 'success', '预览模式')
                print(f"  [PREVIEW] {src_rel} -> {tgt_rel}")
            else:
                try:
                    # 备份源文件（如果目标存在）
                    if tgt.exists():
                        backup = tgt.with_suffix('.bak')
                        shutil.copy2(tgt, backup)

                    # 移动源文件到目标位置
                    shutil.move(str(src), str(tgt))
                    self._log('MERGE', src_rel, tgt_rel, 'success', '合并完成')
                    print(f"  [OK] {src_rel} -> {tgt_rel}")
                    self.stats['merged'] += 1
                except Exception as e:
                    self._log('MERGE', src_rel, tgt_rel, 'error', str(e))
                    print(f"  [ERROR] {src_rel} -> {tgt_rel}: {e}")
                    self.stats['errors'] += 1

    # --------------------------------------------------------
    # 2. 重命名文件
    # --------------------------------------------------------
    def rename_files(self, dry_run: bool = True):
        """重命名冲突文件"""
        print("\n=== 重命名冲突文件 ===")

        for old_rel, new_rel in RENAME_MAPPINGS.items():
            old_path = self.root_path / old_rel
            new_path = self.root_path / new_rel

            if not old_path.exists():
                self._log('RENAME', old_rel, new_rel, 'skipped', '文件不存在')
                print(f"  [SKIP] {old_rel} (不存在)")
                continue

            if new_path.exists():
                self._log('RENAME', old_rel, new_rel, 'skipped', '目标已存在')
                print(f"  [SKIP] {old_rel} -> {new_rel} (目标已存在)")
                continue

            if dry_run:
                self._log('RENAME', old_rel, new_rel, 'success', '预览模式')
                print(f"  [PREVIEW] {old_rel} -> {new_rel}")
            else:
                try:
                    shutil.move(str(old_path), str(new_path))
                    self._log('RENAME', old_rel, new_rel, 'success', '重命名完成')
                    print(f"  [OK] {old_rel} -> {new_rel}")
                    self.stats['renamed'] += 1
                except Exception as e:
                    self._log('RENAME', old_rel, new_rel, 'error', str(e))
                    print(f"  [ERROR] {old_rel} -> {new_rel}: {e}")
                    self.stats['errors'] += 1

    # --------------------------------------------------------
    # 3. 删除废弃文件
    # --------------------------------------------------------
    def delete_obsolete(self, dry_run: bool = True):
        """删除废弃文件"""
        print("\n=== 删除废弃文件 ===")

        for rel_path in DELETE_FILES:
            path = self.root_path / rel_path

            if not path.exists():
                self._log('DELETE', rel_path, '-', 'skipped', '文件不存在')
                continue

            if dry_run:
                self._log('DELETE', rel_path, '-', 'success', '预览模式')
                print(f"  [PREVIEW] 删除: {rel_path}")
            else:
                try:
                    # 备份到 .trash 目录
                    trash = self.root_path / '.trash'
                    trash.mkdir(exist_ok=True)
                    dest = trash / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{path.name}"
                    shutil.move(str(path), str(dest))
                    self._log('DELETE', rel_path, str(dest), 'success', '已移动到.trash')
                    print(f"  [OK] {rel_path} -> .trash/")
                    self.stats['deleted'] += 1
                except Exception as e:
                    self._log('DELETE', rel_path, '-', 'error', str(e))
                    print(f"  [ERROR] {rel_path}: {e}")
                    self.stats['errors'] += 1

    # --------------------------------------------------------
    # 4. 替换中文标点符号
    # --------------------------------------------------------
    def fix_punctuation(self, pattern: str = "*.py", dry_run: bool = True):
        """替换中文标点符号"""
        print(f"\n=== 替换中文标点符号 (pattern={pattern}) ===")

        fixed_files = 0
        total_replacements = 0

        for path in self.root_path.rglob(pattern):
            if '__pycache__' in str(path) or 'node_modules' in str(path):
                continue

            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()

                original = content
                replacement_count = 0

                # 替换中文标点
                for cn, en in CHINESE_PUNCT_TO_ASCII.items():
                    count = content.count(cn)
                    if count > 0:
                        content = content.replace(cn, en)
                        replacement_count += count

                if replacement_count > 0:
                    if not dry_run:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content)

                    print(f"  {'[PREVIEW]' if dry_run else '[OK]'} {path}: {replacement_count} replacements")
                    fixed_files += 1
                    total_replacements += replacement_count

            except Exception as e:
                print(f"  [ERROR] {path}: {e}")
                self.stats['errors'] += 1

        self.stats['punct_fixed'] = total_replacements
        print(f"\n  Total: {fixed_files} files, {total_replacements} replacements")

    # --------------------------------------------------------
    # 5. 生成报告
    # --------------------------------------------------------
    def generate_report(self) -> str:
        """生成优化报告"""
        report = []
        report.append("# Somn Global Code Optimization Report")
        report.append("")
        report.append(f"**Timestamp**: {self._now()}")
        report.append("")
        report.append("## Stats")
        report.append("")
        report.append(f"| Item | Count |")
        report.append(f"|------|-------|")
        report.append(f"| Merged | {self.stats['merged']} |")
        report.append(f"| Renamed | {self.stats['renamed']} |")
        report.append(f"| Deleted | {self.stats['deleted']} |")
        report.append(f"| Punct Fixed | {self.stats['punct_fixed']} |")
        report.append(f"| Errors | {self.stats['errors']} |")
        report.append("")

        # Detailed results
        if self.results:
            report.append("## Detailed Operations")
            report.append("")
            report.append("| Op | Source | Target | Status | Message |")
            report.append("|----|--------|--------|--------|---------|")
            for r in self.results:
                status_icon = {"success": "OK", "skipped": "SKIP", "error": "ERR"}.get(r.status, "?")
                report.append(f"| {r.operation} | `{r.source}` | `{r.target}` | {status_icon} | {r.message} |")

        report.append("")
        report.append(f"*Report generated: {datetime.now().isoformat()}*")

        return "\n".join(report)

    def save_report(self, filename: str = "optimization_report.md"):
        """Save report"""
        report = self.generate_report()
        with open(self.root_path / filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\nReport saved: {filename}")


def main():
    parser = argparse.ArgumentParser(description='Somn Global Code Optimizer')
    parser.add_argument('--merge', action='store_true', help='Merge duplicate modules')
    parser.add_argument('--rename', action='store_true', help='Rename conflicting files')
    parser.add_argument('--delete', action='store_true', help='Delete obsolete files')
    parser.add_argument('--punct', action='store_true', help='Replace Chinese punctuation')
    parser.add_argument('--all', action='store_true', help='Run all optimizations')
    parser.add_argument('--dry-run', action='store_true', help='Preview mode (no actual changes)')
    parser.add_argument('--path', default='.', help='Project root directory')
    parser.add_argument('--report', help='Report output file')

    args = parser.parse_args()

    optimizer = GlobalOptimizer(args.path)

    # Default to dry-run if no specific operation
    if not any([args.merge, args.rename, args.delete, args.punct, args.all]):
        args.dry_run = True
        print("[PREVIEW MODE] No changes will be made.")
        print("   Use --merge/--rename/--delete/--punct/--all to execute.")
        print()

    if args.merge or args.all:
        optimizer.merge_modules(dry_run=args.dry_run)

    if args.rename or args.all:
        optimizer.rename_files(dry_run=args.dry_run)

    if args.delete or args.all:
        optimizer.delete_obsolete(dry_run=args.dry_run)

    if args.punct or args.all:
        optimizer.fix_punctuation(dry_run=args.dry_run)

    # Generate and save report
    report = optimizer.generate_report()
    if args.report:
        optimizer.save_report(args.report)
    else:
        print("\n" + report)


if __name__ == "__main__":
    main()
