#!/usr/bin/env python3
import os
import sys
from datetime import datetime

def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def analyze_code(project_root):
    """分析代码优化机会"""
    results = {
        'large_files': [],
        'complex_files': [],
        'todo_files': [],
        'total_lines': 0,
        'total_files': 0,
    }
    
    skip_dirs = ['__pycache__', 'node_modules', '.git', 'venv', 'env', '.workbuddy', '.codebuddy']
    
    print("分析代码优化机会...")
    
    for root, dirs, files in os.walk(project_root):
        # 跳过不需要分析的目录
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if not file.endswith('.py'):
                continue
            
            file_path = os.path.join(root, file)
            
            try:
                size = os.path.getsize(file_path)
                results['total_files'] += 1
                
                # 检查文件大小
                if size > 100 * 1024:  # > 100KB
                    results['large_files'].append({
                        'path': file_path,
                        'size': size,
                    })
                
                # 分析文件内容
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.count('\n')
                    results['total_lines'] += lines
                    
                    # 检查文件行数
                    if lines > 500:
                        results['complex_files'].append({
                            'path': file_path,
                            'lines': lines,
                        })
                    
                    # 检查 TODO 注释
                    todo_count = content.count('TODO') + content.count('FIXME')
                    if todo_count > 0:
                        results['todo_files'].append({
                            'path': file_path,
                            'count': todo_count,
                        })
            
            except (OSError, UnicodeDecodeError):
                pass
    
    # 排序
    results['large_files'].sort(key=lambda x: x['size'], reverse=True)
    results['complex_files'].sort(key=lambda x: x['lines'], reverse=True)
    results['todo_files'].sort(key=lambda x: x['count'], reverse=True)
    
    return results

def generate_report(project_root, results):
    """生成优化报告"""
    report_path = os.path.join(project_root, 'file/系统文件/代码优化分析报告.md')
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Somn 代码优化分析报告\n\n")
        f.write(f"生成时间: {datetime.now().isoformat()}\n")
        f.write(f"项目路径: {project_root}\n\n")
        
        f.write("## 执行摘要\n\n")
        f.write(f"- **Python 文件总数**: {results['total_files']} 个\n")
        f.write(f"- **代码总行数**: {results['total_lines']} 行\n")
        f.write(f"- **大文件 (>100KB)**: {len(results['large_files'])} 个\n")
        f.write(f"- **复杂文件 (>500行)**: {len(results['complex_files'])} 个\n")
        f.write(f"- **TODO/FIXME 文件**: {len(results['todo_files'])} 个\n\n")
        
        f.write("## 一、大文件分析 (>100KB)\n\n")
        if results['large_files']:
            f.write(f"共 {len(results['large_files'])} 个文件超过 100KB，可能包含过多功能，建议拆分。\n\n")
            f.write("### 前20个大文件:\n\n")
            for i, info in enumerate(results['large_files'][:20]):
                rel_path = os.path.relpath(info['path'], project_root)
                f.write(f"{i+1}. `{rel_path}` - {format_size(info['size'])}\n")
            if len(results['large_files']) > 20:
                f.write(f"\n... 还有 {len(results['large_files']) - 20} 个未显示\n")
        else:
            f.write("无超过 100KB 的 Python 文件。\n")
        f.write("\n")
        
        f.write("## 二、复杂文件分析 (>500行)\n\n")
        if results['complex_files']:
            f.write(f"共 {len(results['complex_files'])} 个文件超过 500 行，建议拆分成多个小文件以提高可维护性。\n\n")
            f.write("### 前20个复杂文件:\n\n")
            for i, info in enumerate(results['complex_files'][:20]):
                rel_path = os.path.relpath(info['path'], project_root)
                f.write(f"{i+1}. `{rel_path}` - {info['lines']} 行\n")
            if len(results['complex_files']) > 20:
                f.write(f"\n... 还有 {len(results['complex_files']) - 20} 个未显示\n")
        else:
            f.write("无超过 500 行的 Python 文件。\n")
        f.write("\n")
        
        f.write("## 三、TODO/FIXME 注释分析\n\n")
        if results['todo_files']:
            f.write(f"共 {len(results['todo_files'])} 个文件包含 TODO/FIXME 注释，建议逐步处理这些待办事项。\n\n")
            f.write("### 前20个文件:\n\n")
            for i, info in enumerate(results['todo_files'][:20]):
                rel_path = os.path.relpath(info['path'], project_root)
                f.write(f"{i+1}. `{rel_path}` - {info['count']} 个注释\n")
            if len(results['todo_files']) > 20:
                f.write(f"\n... 还有 {len(results['todo_files']) - 20} 个未显示\n")
        else:
            f.write("无 TODO/FIXME 注释。\n")
        f.write("\n")
        
        f.write("## 四、优化建议\n\n")
        f.write("1. **拆分大文件**: 对于 >100KB 或 >500行的文件，考虑拆分成多个小文件\n")
        f.write("2. **处理 TODO/FIXME**: 逐步处理代码中的待办事项，提高代码质量\n")
        f.write("3. **代码重复检查**: 使用工具（如 pylint, flake8）检查代码质量和重复\n")
        f.write("4. **类型注解完善**: 根据项目记忆，类型注解覆盖率20.79%，可继续完善\n")
        f.write("5. **性能优化**: 对于频繁执行的代码，考虑使用性能分析工具（如 cProfile）找出瓶颈\n")
        f.write("6. **内存优化**: 对于大型数据结构，考虑使用生成器或迭代器减少内存占用\n\n")
        
        f.write("## 五、下一步操作建议\n\n")
        f.write("1. 根据本报告，选择优先级高的大文件进行拆分\n")
        f.write("2. 处理 TODO/FIXME 注释，提高代码质量\n")
        f.write("3. 使用代码质量工具进行更全面的分析\n")
        f.write("4. 考虑引入代码审查流程，防止代码复杂度继续增长\n\n")
        
        f.write("---\n\n")
        f.write("*本报告由代码优化分析器自动生成*\n")
    
    print(f"\n报告已保存到: {report_path}")
    return report_path

if __name__ == '__main__':
    project_root = 'd:/AI/somn'
    
    print("=" * 60)
    print("Somn 代码优化分析")
    print("=" * 60)
    
    # 分析代码
    results = analyze_code(project_root)
    
    # 生成报告
    report_path = generate_report(project_root, results)
    
    print("\n" + "=" * 60)
    print("分析完成！")
    print("=" * 60)
    
    # 输出摘要
    print(f"\nPython 文件: {results['total_files']} 个")
    print(f"代码行数: {results['total_lines']} 行")
    print(f"大文件: {len(results['large_files'])} 个")
    print(f"复杂文件: {len(results['complex_files'])} 个")
    print(f"TODO/FIXME: {len(results['todo_files'])} 个")
    print(f"\n详细报告: {report_path}")
