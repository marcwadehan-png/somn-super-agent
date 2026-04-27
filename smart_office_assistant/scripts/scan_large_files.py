#!/usr/bin/env python3
"""
扫描项目中超过指定行数的 Python 文件
用法: python scripts/scan_large_files.py [max_lines] [project_root]
"""

import sys
import os
from pathlib import Path
from datetime import datetime


def count_lines(file_path: Path) -> int:
    """计算文件行数"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return len(f.readlines())
    except Exception as e:
        print(f"  警告: 无法读取 {file_path}: {e}")
        return 0


def scan_large_files(project_root: Path, max_lines: int = 500) -> list:
    """
    扫描项目中超过 max_lines 行的 Python 文件
    
    Returns:
        列表，元素为 (文件路径, 行数) 的元组，按行数降序排列
    """
    large_files = []
    src_dir = project_root / "src"
    
    if not src_dir.exists():
        print(f"错误: 未找到 src 目录: {src_dir}")
        return large_files
    
    print(f"扫描目录: {src_dir}")
    print(f"行数限制: {max_lines}")
    print("-" * 60)
    
    for py_file in src_dir.rglob("*.py"):
        # 跳过 __pycache__ 和 .pyc 文件
        if "__pycache__" in str(py_file) or py_file.suffix == ".pyc":
            continue
        
        line_count = count_lines(py_file)
        if line_count > max_lines:
            large_files.append((py_file, line_count))
    
    # 按行数降序排列
    large_files.sort(key=lambda x: x[1], reverse=True)
    return large_files


def print_report(large_files: list, project_root: Path, max_lines: int):
    """打印扫描报告"""
    print(f"\n{'='*60}")
    print(f"大文件扫描报告")
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"项目路径: {project_root}")
    print(f"行数限制: {max_lines}")
    print(f"{'='*60}\n")
    
    if not large_files:
        print("✅ 未发现超过行数限制的文件")
        return
    
    # 按严重程度分组
    critical = []  # > 1500 行
    high = []      # 1000-1500 行
    medium = []    # 800-1000 行
    low = []       # 500-800 行
    
    for file_path, line_count in large_files:
        rel_path = file_path.relative_to(project_root)
        if line_count > 1500:
            critical.append((rel_path, line_count))
        elif line_count > 1000:
            high.append((rel_path, line_count))
        elif line_count > 800:
            medium.append((rel_path, line_count))
        else:
            low.append((rel_path, line_count))
    
    total_violations = len(large_files)
    total_lines = sum(lc for _, lc in large_files)
    
    print(f"发现 {total_violations} 个违规文件，共 {total_lines} 行\n")
    
    # 打印各组
    if critical:
        print(f"🔴 严重 (>1500行): {len(critical)} 个文件")
        print("-" * 60)
        for rel_path, line_count in critical:
            print(f"  {line_count:5d} 行  {rel_path}")
        print()
    
    if high:
        print(f"🟠 高危 (1000-1500行): {len(high)} 个文件")
        print("-" * 60)
        for rel_path, line_count in high:
            print(f"  {line_count:5d} 行  {rel_path}")
        print()
    
    if medium:
        print(f"🟡 中危 (800-1000行): {len(medium)} 个文件")
        print("-" * 60)
        for rel_path, line_count in medium:
            print(f"  {line_count:5d} 行  {rel_path}")
        print()
    
    if low:
        print(f"🟢 低危 (500-800行): {len(low)} 个文件")
        print("-" * 60)
        for rel_path, line_count in low:
            print(f"  {line_count:5d} 行  {rel_path}")
        print()
    
    # 统计信息
    print(f"{'='*60}")
    print("统计摘要")
    print(f"{'='*60}")
    print(f"总违规文件数: {total_violations}")
    print(f"平均行数: {total_lines // total_violations if total_violations else 0}")
    print(f"最大行数: {large_files[0][1] if large_files else 0}")
    print(f"最小行数: {large_files[-1][1] if large_files else 0}")


def export_to_markdown(large_files: list, project_root: Path, max_lines: int, output_path: Path):
    """导出报告为 Markdown 文件"""
    lines = [
        "# 大文件扫描报告\n",
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n",
        f"**项目路径**: {project_root}  \n",
        f"**行数限制**: {max_lines}  \n\n",
        "---\n\n",
    ]
    
    if not large_files:
        lines.append("✅ 未发现超过行数限制的文件\n")
    else:
        lines.append(f"发现 {len(large_files)} 个违规文件\n\n")
        lines.append("| 行数 | 文件路径 | 严重程度 |\n")
        lines.append("|------|---------|---------|\n")
        
        for file_path, line_count in large_files:
            rel_path = file_path.relative_to(project_root)
            if line_count > 1500:
                severity = "🔴 严重"
            elif line_count > 1000:
                severity = "🟠 高危"
            elif line_count > 800:
                severity = "🟡 中危"
            else:
                severity = "🟢 低危"
            lines.append(f"| {line_count} | `{rel_path}` | {severity} |\n")
    
    output_path.write_text(''.join(lines), encoding='utf-8')
    print(f"\n报告已导出: {output_path}")


def main():
    # 解析参数
    max_lines = 500
    project_root = None
    
    if len(sys.argv) > 1:
        try:
            max_lines = int(sys.argv[1])
        except ValueError:
            pass
    
    if len(sys.argv) > 2:
        project_root = Path(sys.argv[2])
    else:
        # 自动定位项目根目录
        script_dir = Path(__file__).parent.resolve()
        project_root = script_dir.parent
    
    project_root = project_root.resolve()
    
    # 执行扫描
    large_files = scan_large_files(project_root, max_lines)
    
    # 打印报告
    print_report(large_files, project_root, max_lines)
    
    # 导出 Markdown 报告
    if large_files:
        output_path = project_root / "docs" / "reports" / f"large_files_report_{datetime.now().strftime('%Y%m%d')}.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        export_to_markdown(large_files, project_root, max_lines, output_path)
    
    # 返回退出码
    return 1 if large_files else 0


if __name__ == "__main__":
    sys.exit(main())
