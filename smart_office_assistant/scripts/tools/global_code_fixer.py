# -*- coding: utf-8 -*-
"""
全局代码优化工具 - 中文转英文/拼音
Global Code Optimization Tool - Chinese to English/Pinyin

【兼容层】主入口，委托给 global_code_fixer 包处理
"""
import argparse
import sys
from pathlib import Path

# 向后兼容导入
from scripts.tools.global_code_fixer import ChineseCodeFixer


def main():
    parser = argparse.ArgumentParser(description='Global Code Optimization Tool')
    parser.add_argument('--scan', action='store_true', help='Scan files with Chinese content')
    parser.add_argument('--fix', action='store_true', help='Fix Chinese content')
    parser.add_argument('--dry-run', action='store_true', help='Dry run (no actual changes)')
    parser.add_argument('--path', default='.', help='Root path to scan')
    parser.add_argument('--pattern', default='*.py', help='File pattern to match')
    parser.add_argument('--report', help='Save report to file')

    args = parser.parse_args()

    fixer = ChineseCodeFixer(args.path)

    if args.scan:
        print("Scanning files...")
        results = fixer.scan_all(args.pattern)

        print(f"\nFound {len(results)} files with Chinese content:\n")

        sorted_files = sorted(results.items(), key=lambda x: x[1]['count'], reverse=True)
        for path, info in sorted_files[:30]:
            print(f"  {info['count']:4d}  {path}")

        if len(sorted_files) > 30:
            print(f"\n  ... and {len(sorted_files) - 30} more files")

    if args.fix:
        print(f"Fixing files (dry_run={args.dry_run})...")
        fixer.fix_all(args.pattern, dry_run=args.dry_run)

        if args.report:
            report = fixer.generate_report()
            with open(args.report, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\nReport saved to: {args.report}")
        else:
            print(f"\nTotal fixes: {fixer.total_fixes}")


if __name__ == "__main__":
    main()
