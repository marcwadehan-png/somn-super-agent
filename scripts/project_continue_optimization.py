#!/usr/bin/env python3
"""
项目继续优化脚本 - 清理临时文件并分析代码优化机会
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime

def format_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def clean_temp_files(project_root):
    """清理临时文件和日志文件"""
    temp_extensions = ['.tmp', '.temp', '.bak', '.backup', '.swp', '.swo', '~']
    
    temp_files = []
    log_files = []
    
    # 保护的目录
    protected_dirs = [
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
    
    print("扫描临时文件和日志文件...")
    
    for root, dirs, files in os.walk(project_root):
        # 检查是否在保护目录中
        rel_root = os.path.relpath(root, project_root).replace('\\', '/')
        skip = False
        for protected in protected_dirs:
            if rel_root.startswith(protected):
                dirs[:] = []  # 不递归进入保护目录
                skip = True
                break
        if skip:
            continue
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            file_path = os.path.join(root, file)
            
            if ext in temp_extensions:
                try:
                    size = os.path.getsize(file_path)
                    temp_files.append({'path': file_path, 'size': size})
                except OSError:
                    pass
            elif file.endswith('.log'):
                try:
                    size = os.path.getsize(file_path)
                    log_files.append({'path': file_path, 'size': size})
                except OSError:
                    pass
    
    print(f"发现临时文件: {len(temp_files)} 个")
    print(f"发现日志文件: {len(log_files)} 个")
    
    # 计算总大小
    total_temp_size = sum(f['size'] for f in temp_files)
    total_log_size = sum(f['size'] for f in log_files)
    
    print(f"临时文件总大小: {format_size(total_temp_size)}")
    print(f"日志文件总大小: {format_size(total_log_size)}")
    
    # 删除临时文件
    deleted_temp = 0
    
    print("\n删除临时文件...")
    for file_info in temp_files:
        try:
            os.remove(file_info['path'])
            deleted_temp += 1
            print(f"  已删除: {os.path.relpath(file_info['path'], project_root)}")
        except OSError as e:
            print(f"  删除失败: {file_info['path']} - {e}")
    
    return {
        'deleted_temp': deleted_temp,
        'deleted_log': 0,  # 需要确认
        'temp_files': temp_files,
        'log_files': log_files,
        'total_temp_size': total_temp_size,
        'total_log_size': total_log_size,
    }

def analyze_code_optimization_opportunities(project_root):
    """分析代码优化机会"""
    opportunities = {
        'large_files': [],
        'complex_files': [],
        'todo_comments': [],
    }
    
    print("\n分析代码优化机会...")
    
    for root, dirs, files in os.walk(project_root):
        # 跳过不需要分析的目录
        if any(x in root for x in ['__pycache__', 'node_modules', '.git', 'venv', 'env']):
            dirs[:] = []
            continue
        
        for file in files:
            if not file.endswith('.py'):
                continue
            
            file_path = os.path.join(root, file)
            
            try:
                # 检查文件大小
                size = os.path.getsize(file_path)
                if size > 100 * 1024:  # > 100KB
                    opportunities['large_files'].append({
                        'path': file_path,
                        'size': size,
                    })
                
                # 分析文件内容
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.count('\n')
                    
                    # 检查文件行数
                    if lines > 500:
                        opportunities['complex_files'].append({
                            'path': file_path,
                            'lines': lines,
                        })
                    
                    # 检查 TODO 注释
                    if 'TODO' in content or 'FIXME' in content:
                        opportunities['todo_comments'].append({
                            'path': file_path,
                            'count': content.count('TODO') + content.count('FIXME'),
                        })
            
            except (OSError, UnicodeDecodeError):
                pass
    
    # 排序
    opportunities['large_files'].sort(key=lambda x: x['size'], reverse=True)
    opportunities['complex_files'].sort(key=lambda x: x['lines'], reverse=True)
    opportunities['todo_comments'].sort(key=lambda x: x['count'], reverse=True)
    
    print(f"发现大文件(>100KB): {len(opportunities['large_files'])} 个")
    print(f"发现复杂文件(>500行): {len(opportunities['complex_files'])} 个")
    print(f"发现 TODO/FIXME 注释: {len(opportunities['todo_comments'])} 个")
    
    return opportunities

def generate_optimization_report(project_root, clean_results, opportunities):
    """生成优化报告"""
    report_path = os.path.join(project_root, 'file/系统文件/项目继续优化报告.md')
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Somn 项目继续优化报告\n\n")
        f.write(f"生成时间: {datetime.now().isoformat()}\n")
        f.write(f"项目路径: {project_root}\n\n")
        
        f.write("## 执行摘要\n\n")
        f.write(f"- **已删除临时文件**: {clean_results['deleted_temp']} 个\n")
        f.write(f"- **释放空间**: {format_size(clean_results['total_temp_size'])}\n")
        f.write(f"- **待处理日志文件**: {len(clean_results['log_files'])} 个 ({format_size(clean_results['total_log_size'])})\n")
        f.write(f"- **大文件(>100KB)**: {len(opportunities['large_files'])} 个\n")
        f.write(f"- **复杂文件(>500行)**: {len(opportunities['complex_files'])} 个\n")
        f.write(f"- **TODO/FIXME 注释**: {len(opportunities['todo_comments'])} 个\n\n")
        
        f.write("## 一、已完成的清理操作\n\n")
        f.write(f"### 1. 临时文件清理\n\n")
        f.write(f"已删除 {clean_results['deleted_temp']} 个临时文件，释放空间: {format_size(clean_results['total_temp_size'])}\n\n")
        
        if clean_results['temp_files']:
            f.write("### 已删除的临时文件（前20个）:\n\n")
            for i, file_info in enumerate(clean_results['temp_files'][:20]):
                rel_path = os.path.relpath(file_info['path'], project_root)
                f.write(f"{i+1}. `{rel_path}` - {format_size(file_info['size'])}\n")
            if len(clean_results['temp_files']) > 20:
                f.write(f"\n... 还有 {len(clean_results['temp_files']) - 20} 个未显示\n")
        f.write("\n")
        
        f.write("## 二、待处理的文件\n\n")
        f.write("### 1. 日志文件\n\n")
        f.write(f"共 {len(clean_results['log_files'])} 个日志文件，总大小: {format_size(clean_results['total_log_size'])}\n\n")
        
        if clean_results['log_files']:
            f.write("### 日志文件列表（前20个）:\n\n")
            for i, file_info in enumerate(clean_results['log_files'][:20]):
                rel_path = os.path.relpath(file_info['path'], project_root)
                f.write(f"{i+1}. `{rel_path}` - {format_size(file_info['size'])}\n")
            if len(clean_results['log_files']) > 20:
                f.write(f"\n... 还有 {len(clean_results['log_files']) - 20} 个未显示\n")
        f.write("\n")
        
        f.write("**建议**: 日志文件可能包含有用的调试信息，建议先审查再决定是否删除。\n\n")
        
        f.write("## 三、代码优化机会\n\n")
        f.write("### 1. 大文件 (>100KB)\n\n")
        f.write(f"共 {len(opportunities['large_files'])} 个文件\n\n")
        
        if opportunities['large_files']:
            f.write("### 前20个大文件:\n\n")
            for i, file_info in enumerate(opportunities['large_files'][:20]):
                rel_path = os.path.relpath(file_info['path'], project_root)
                f.write(f"{i+1}. `{rel_path}` - {format_size(file_info['size'])}\n")
        f.write("\n")
        
        f.write("### 2. 复杂文件 (>500行)\n\n")
        f.write(f"共 {len(opportunities['complex_files'])} 个文件\n\n")
        
        if opportunities['complex_files']:
            f.write("### 前20个复杂文件:\n\n")
            for i, file_info in enumerate(opportunities['complex_files'][:20]):
                rel_path = os.path.relpath(file_info['path'], project_root)
                f.write(f"{i+1}. `{rel_path}` - {file_info['lines']} 行\n")
        f.write("\n")
        
        f.write("### 3. TODO/FIXME 注释\n\n")
        f.write(f"共 {len(opportunities['todo_comments'])} 个文件包含 TODO/FIXME 注释\n\n")
        
        if opportunities['todo_comments']:
            f.write("### 前20个文件:\n\n")
            for i, file_info in enumerate(opportunities['todo_comments'][:20]):
                rel_path = os.path.relpath(file_info['path'], project_root)
                f.write(f"{i+1}. `{rel_path}` - {file_info['count']} 个注释\n")
        f.write("\n")
        
        f.write("## 四、优化建议\n\n")
        f.write("1. **审查日志文件**: 确认是否有用的日志，无用的可以删除\n")
        f.write("2. **拆分大文件**: 对于 >100KB 或 >500行的文件，考虑拆分成多个小文件\n")
        f.write("3. **处理 TODO/FIXME**: 逐步处理代码中的待办事项\n")
        f.write("4. **代码重复检查**: 使用工具（如 pylint, flake8）检查代码质量和重复\n")
        f.write("5. **类型注解完善**: 根据项目记忆，类型注解覆盖率20.79%，可继续完善\n\n")
        
        f.write("---\n\n")
        f.write("*本报告由项目继续优化脚本自动生成*\n")
    
    print(f"\n报告已保存到: {report_path}")
    return report_path

if __name__ == '__main__':
    project_root = 'd:/AI/somn'
    
    print("=" * 60)
    print("Somn 项目继续优化")
    print("=" * 60)
    
    # 1. 清理临时文件
    print("\n[1/3] 清理临时文件...")
    clean_results = clean_temp_files(project_root)
    
    # 2. 分析代码优化机会
    print("\n[2/3] 分析代码优化机会...")
    opportunities = analyze_code_optimization_opportunities(project_root)
    
    # 3. 生成报告
    print("\n[3/3] 生成优化报告...")
    report_path = generate_optimization_report(project_root, clean_results, opportunities)
    
    print("\n" + "=" * 60)
    print("优化完成！")
    print("=" * 60)
    
    # 输出摘要
    print(f"\n已删除临时文件: {clean_results['deleted_temp']} 个")
    print(f"释放空间: {format_size(clean_results['total_temp_size'])}")
    print(f"大文件: {len(opportunities['large_files'])} 个")
    print(f"复杂文件: {len(opportunities['complex_files'])} 个")
    print(f"TODO/FIXME: {len(opportunities['todo_comments'])} 个")
    print(f"\n详细报告: {report_path}")
