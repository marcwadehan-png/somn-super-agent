#!/usr/bin/env python3
"""
项目瘦身分析器 - 扫描项目并识别可安全清理的文件
"""
import os
import sys
from pathlib import Path
from datetime import datetime
import json

# 需要绝对保护的数据目录（根据working_memory）
PROTECTED_DIRS = [
    'data/memory_v2',
    'data/q_values',
    'data/learning',
    'data/solution_learning',
    'data/memory',
    'data/feedback_production',
    'data/feedback_loop',
    'data/reasoning',
    'data/ml',
]

# 可安全清理的目录/文件模式
CACHE_PATTERNS = [
    '__pycache__',
    '*.pyc',
    '*.pyo',
    '*.pyd',
    '.pytest_cache',
    '.coverage',
    'htmlcov',
    '*.egg-info',
    'dist',
    'build',
    'node_modules/.cache',
]

# 临时文件扩展名
TEMP_EXTENSIONS = ['.tmp', '.temp', '.bak', '.backup', '.log', '.swp', '.swo', '~']

def get_dir_size(path):
    """计算目录大小"""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    except (PermissionError, OSError):
        pass
    return total

def format_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def is_protected(path, project_root):
    """检查路径是否在保护列表中"""
    rel_path = os.path.relpath(path, project_root).replace('\\', '/')
    for protected in PROTECTED_DIRS:
        if rel_path.startswith(protected):
            return True
    return False

def analyze_project(project_root):
    """分析项目并生成瘦身报告"""
    results = {
        'timestamp': datetime.now().isoformat(),
        'project_root': project_root,
        'cache_dirs': [],
        'cache_files': [],
        'temp_files': [],
        'large_files': [],
        'empty_dirs': [],
        'duplicate_candidates': [],
        'total_size': 0,
    }
    
    print(f"正在扫描项目: {project_root}")
    print("=" * 60)
    
    # 1. 扫描 __pycache__ 目录
    print("\n[1/6] 扫描 __pycache__ 目录...")
    pycache_count = 0
    pycache_size = 0
    for root, dirs, files in os.walk(project_root):
        # 检查是否在保护目录中
        if is_protected(root, project_root):
            dirs[:] = []  # 不递归进入保护目录
            continue
            
        if '__pycache__' in dirs:
            cache_path = os.path.join(root, '__pycache__')
            size = get_dir_size(cache_path)
            file_count = sum([len(files) for r, d, files in os.walk(cache_path)])
            results['cache_dirs'].append({
                'path': cache_path,
                'size': size,
                'file_count': file_count,
            })
            pycache_count += 1
            pycache_size += size
            dirs.remove('__pycache__')  # 不进一步递归
    
    print(f"  发现 {pycache_count} 个 __pycache__ 目录，总大小: {format_size(pycache_size)}")
    
    # 2. 扫描 .pyc/.pyo/.pyd 文件
    print("\n[2/6] 扫描 .pyc/.pyo/.pyd 文件...")
    pyc_count = 0
    pyc_size = 0
    for root, dirs, files in os.walk(project_root):
        if is_protected(root, project_root):
            dirs[:] = []
            continue
            
        for file in files:
            if file.endswith(('.pyc', '.pyo', '.pyd')):
                file_path = os.path.join(root, file)
                size = os.path.getsize(file_path)
                results['cache_files'].append({
                    'path': file_path,
                    'size': size,
                })
                pyc_count += 1
                pyc_size += size
    
    print(f"  发现 {pyc_count} 个缓存文件，总大小: {format_size(pyc_size)}")
    
    # 3. 扫描临时文件和日志
    print("\n[3/6] 扫描临时文件和日志...")
    temp_count = 0
    temp_size = 0
    for root, dirs, files in os.walk(project_root):
        if is_protected(root, project_root):
            dirs[:] = []
            continue
            
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in TEMP_EXTENSIONS or file.endswith('.log'):
                file_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(file_path)
                    results['temp_files'].append({
                        'path': file_path,
                        'size': size,
                        'type': 'temp' if ext in TEMP_EXTENSIONS else 'log',
                    })
                    temp_count += 1
                    temp_size += size
                except OSError:
                    pass
    
    print(f"  发现 {temp_count} 个临时/日志文件，总大小: {format_size(temp_size)}")
    
    # 4. 扫描大文件 (>10MB)
    print("\n[4/6] 扫描大文件 (>10MB)...")
    large_count = 0
    for root, dirs, files in os.walk(project_root):
        if is_protected(root, project_root):
            dirs[:] = []
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                if size > 10 * 1024 * 1024:  # >10MB
                    results['large_files'].append({
                        'path': file_path,
                        'size': size,
                    })
                    large_count += 1
            except OSError:
                pass
    
    print(f"  发现 {large_count} 个大于10MB的文件")
    
    # 5. 扫描空目录
    print("\n[5/6] 扫描空目录...")
    empty_count = 0
    for root, dirs, files in os.walk(project_root, topdown=False):
        if is_protected(root, project_root):
            continue
            
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                if not os.listdir(dir_path):
                    results['empty_dirs'].append(dir_path)
                    empty_count += 1
            except OSError:
                pass
    
    print(f"  发现 {empty_count} 个空目录")
    
    # 计算可节省的总空间
    total_savings = pycache_size + pyc_size + temp_size
    results['total_potential_savings'] = total_savings
    results['total_potential_savings_formatted'] = format_size(total_savings)
    
    print("\n" + "=" * 60)
    print("扫描完成！")
    print(f"潜在可节省空间: {format_size(total_savings)}")
    print("=" * 60)
    
    return results

def generate_report(results, output_path):
    """生成详细的瘦身报告"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Somn 项目瘦身分析报告\n\n")
        f.write(f"生成时间: {results['timestamp']}\n")
        f.write(f"项目路径: {results['project_root']}\n\n")
        
        f.write("## 执行摘要\n\n")
        f.write(f"- **潜在可节省空间**: {results['total_potential_savings_formatted']}\n")
        f.write(f"- **__pycache__ 目录**: {len(results['cache_dirs'])} 个\n")
        f.write(f"- **缓存文件 (.pyc/.pyo/.pyd)**: {len(results['cache_files'])} 个\n")
        f.write(f"- **临时/日志文件**: {len(results['temp_files'])} 个\n")
        f.write(f"- **空目录**: {len(results['empty_dirs'])} 个\n")
        f.write(f"- **大文件 (>10MB)**: {len(results['large_files'])} 个\n\n")
        
        f.write("## 1. __pycache__ 目录\n\n")
        if results['cache_dirs']:
            total_size = sum(d['size'] for d in results['cache_dirs'])
            f.write(f"共 {len(results['cache_dirs'])} 个目录，总大小: {format_size(total_size)}\n\n")
            f.write("这些目录可以在Python运行时自动重新生成，可安全删除。\n\n")
            f.write("### 前10个最大的 __pycache__ 目录:\n\n")
            sorted_dirs = sorted(results['cache_dirs'], key=lambda x: x['size'], reverse=True)[:10]
            for d in sorted_dirs:
                rel_path = os.path.relpath(d['path'], results['project_root'])
                f.write(f"- `{rel_path}` - {format_size(d['size'])} ({d['file_count']} 文件)\n")
        else:
            f.write("未发现 __pycache__ 目录。\n")
        f.write("\n")
        
        f.write("## 2. 缓存文件 (.pyc/.pyo/.pyd)\n\n")
        if results['cache_files']:
            total_size = sum(f['size'] for f in results['cache_files'])
            f.write(f"共 {len(results['cache_files'])} 个文件，总大小: {format_size(total_size)}\n\n")
            f.write("这些文件是Python字节码缓存，可安全删除。\n\n")
        else:
            f.write("未发现缓存文件。\n")
        f.write("\n")
        
        f.write("## 3. 临时文件和日志\n\n")
        if results['temp_files']:
            total_size = sum(f['size'] for f in results['temp_files'])
            f.write(f"共 {len(results['temp_files'])} 个文件，总大小: {format_size(total_size)}\n\n")
            f.write("### 按类型分类:\n")
            temp_files = [f for f in results['temp_files'] if f['type'] == 'temp']
            log_files = [f for f in results['temp_files'] if f['type'] == 'log']
            f.write(f"- 临时文件: {len(temp_files)} 个\n")
            f.write(f"- 日志文件: {len(log_files)} 个\n\n")
        else:
            f.write("未发现临时文件或日志文件。\n")
        f.write("\n")
        
        f.write("## 4. 大文件 (>10MB)\n\n")
        if results['large_files']:
            f.write(f"共 {len(results['large_files'])} 个文件\n\n")
            f.write("### 前20个大文件:\n\n")
            sorted_files = sorted(results['large_files'], key=lambda x: x['size'], reverse=True)[:20]
            for file_info in sorted_files:
                rel_path = os.path.relpath(file_info['path'], results['project_root'])
                f.write(f"- `{rel_path}` - {format_size(file_info['size'])}\n")
            f.write("\n**注意**: 大文件需要人工审查，确认是否可以安全删除。\n")
        else:
            f.write("未发现大于10MB的文件。\n")
        f.write("\n")
        
        f.write("## 5. 空目录\n\n")
        if results['empty_dirs']:
            f.write(f"共 {len(results['empty_dirs'])} 个空目录\n\n")
            f.write("### 前20个空目录:\n\n")
            for dir_path in results['empty_dirs'][:20]:
                rel_path = os.path.relpath(dir_path, results['project_root'])
                f.write(f"- `{rel_path}`\n")
            if len(results['empty_dirs']) > 20:
                f.write(f"\n... 还有 {len(results['empty_dirs']) - 20} 个空目录未显示\n")
        else:
            f.write("未发现空目录。\n")
        f.write("\n")
        
        f.write("## 6. 建议的瘦身操作\n\n")
        f.write("### 安全操作（可立即执行）\n\n")
        f.write("1. **删除所有 __pycache__ 目录** - 可节省最大空间，且不会影响功能\n")
        f.write("2. **删除所有 .pyc/.pyo/.pyd 文件** - Python会在运行时重新生成\n")
        f.write("3. **删除临时文件和日志** - 需要确认是否有用的日志\n")
        f.write("4. **删除空目录** - 安全，但需确认是否为必须的目录结构\n\n")
        
        f.write("### 需要人工审查的操作\n\n")
        f.write("1. **大文件审查** - 需要逐个检查是否可以删除或压缩\n")
        f.write("2. **node_modules 目录** - 可通过 `npm install` 重新生成\n")
        f.write("3. **构建产物 (dist/, build/)** - 可重新构建\n\n")
        
        f.write("### 绝对不能删除的目录\n\n")
        for protected in PROTECTED_DIRS:
            f.write(f"- `d:/AI/somn/{protected}`\n")
        f.write("\n")
        
        f.write("## 7. 执行命令示例\n\n")
        f.write("```bash\n")
        f.write("# 删除所有 __pycache__ 目录 (Windows PowerShell)\n")
        f.write("Get-ChildItem -Path 'd:\\AI\\somn' -Include '__pycache__' -Recurse -Directory | Remove-Item -Recurse -Force\n\n")
        f.write("# 删除所有 .pyc 文件 (Windows PowerShell)\n")
        f.write("Get-ChildItem -Path 'd:\\AI\\somn' -Include '*.pyc' -Recurse -File | Remove-Item -Force\n\n")
        f.write("# 删除所有 .pyo 文件 (Windows PowerShell)\n")
        f.write("Get-ChildItem -Path 'd:\\AI\\somn' -Include '*.pyo' -Recurse -File | Remove-Item -Force\n")
        f.write("```\n\n")
        
        f.write("\n---\n\n")
        f.write("*本报告由项目瘦身分析器自动生成*\n")
    
    print(f"\n报告已保存到: {output_path}")

if __name__ == '__main__':
    project_root = 'd:/AI/somn'
    output_path = os.path.join(project_root, 'file/系统文件/项目瘦身分析报告.md')
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 分析项目
    results = analyze_project(project_root)
    
    # 保存结果到JSON（用于后续处理）
    json_path = os.path.join(project_root, 'project_slimdown_analysis.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"分析数据已保存到: {json_path}")
    
    # 生成报告
    generate_report(results, output_path)
    
    print("\n完成！")
