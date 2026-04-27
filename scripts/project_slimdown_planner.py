#!/usr/bin/env python3
"""
项目瘦身方案生成器 - 生成详细的可执行瘦身方案
"""
import os
import json
from pathlib import Path
from datetime import datetime

def format_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

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

def analyze_large_dirs(project_root):
    """分析大目录"""
    large_dirs = []
    
    # 检查常见的可能的大目录
    candidates = [
        'node_modules',
        'models',
        'data',
        '.git',
        'venv',
        'env',
        '.workbuddy',
        '.codebuddy',
    ]
    
    for candidate in candidates:
        path = os.path.join(project_root, candidate)
        if os.path.exists(path) and os.path.isdir(path):
            size = get_dir_size(path)
            file_count = sum([len(files) for r, d, files in os.walk(path)])
            large_dirs.append({
                'path': path,
                'relative_path': candidate,
                'size': size,
                'file_count': file_count,
            })
    
    return large_dirs

def check_gitignore(project_root):
    """检查 .gitignore 是否完善"""
    gitignore_path = os.path.join(project_root, '.gitignore')
    
    recommended_ignores = [
        '__pycache__/',
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '.pytest_cache/',
        'node_modules/',
        'dist/',
        'build/',
        '*.egg-info/',
        '.coverage',
        'htmlcov/',
        '*.log',
        '*.tmp',
        '*.temp',
    ]
    
    missing = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for ignore in recommended_ignores:
                if ignore not in content:
                    missing.append(ignore)
    else:
        missing = recommended_ignores
    
    return missing

def generate_slimdown_plan(project_root):
    """生成瘦身方案"""
    print("正在生成瘦身方案...")
    print("=" * 60)
    
    # 读取之前的分析结果
    analysis_path = os.path.join(project_root, 'project_slimdown_analysis.json')
    if os.path.exists(analysis_path):
        with open(analysis_path, 'r', encoding='utf-8') as f:
            analysis = json.load(f)
    else:
        print("错误: 找不到分析结果文件，请先运行分析器")
        return None
    
    # 分析大目录
    print("\n分析大目录...")
    large_dirs = analyze_large_dirs(project_root)
    
    # 检查 .gitignore
    print("检查 .gitignore...")
    missing_ignores = check_gitignore(project_root)
    
    # 生成方案
    plan = {
        'timestamp': datetime.now().isoformat(),
        'project_root': project_root,
        'immediate_actions': [],  # 可立即执行的安全操作
        'review_needed': [],       # 需要审查的操作
        'long_term_suggestions': [],  # 长期优化建议
        'analysis': analysis,
        'large_dirs': large_dirs,
        'missing_gitignore': missing_ignores,
    }
    
    # 1. 立即可以执行的安全操作
    cache_size = sum(d['size'] for d in analysis['cache_dirs'])
    pyc_size = sum(f['size'] for f in analysis['cache_files'])
    
    if analysis['cache_dirs'] or analysis['cache_files']:
        plan['immediate_actions'].append({
            'action': '删除所有 __pycache__ 目录和 .pyc/.pyo/.pyd 文件',
            'description': '这些文件是Python字节码缓存，可以在运行时自动重新生成',
            'potential_savings': cache_size + pyc_size,
            'commands': [
                "powershell -Command \"Get-ChildItem -Path 'd:\\AI\\somn' -Include '__pycache__' -Recurse -Directory | Remove-Item -Recurse -Force\"",
                "powershell -Command \"Get-ChildItem -Path 'd:\\AI\\somn' -Include '*.pyc','*.pyo','*.pyd' -Recurse -File | Remove-Item -Force\"",
            ],
            'Risk_level': '低风险',
        })
    
    if analysis['empty_dirs']:
        plan['immediate_actions'].append({
            'action': f"删除 {len(analysis['empty_dirs'])} 个空目录",
            'description': '空目录不影响功能，可安全删除',
            'potential_savings': 0,  # 空目录几乎不占空间
            'commands': [
                "powershell -Command \"Get-ChildItem -Path 'd:\\AI\\somn' -Recurse -Directory | Where-Object { $_.GetFiles().Count -eq 0 -and $_.GetDirectories().Count -eq 0 } | Remove-Item -Force\"",
            ],
            'Risk_level': '低风险',
        })
    
    # 2. 需要审查的操作
    if analysis['temp_files']:
        temp_size = sum(f['size'] for f in analysis['temp_files'])
        plan['review_needed'].append({
            'action': f"审查并删除临时/日志文件 ({len(analysis['temp_files'])} 个文件)",
            'description': '需要确认这些文件是否还用途',
            'potential_savings': temp_size,
            'Risk_level': '中等风险',
        })
    
    # 检查大目录
    for dir_info in large_dirs:
        if dir_info['relative_path'] == 'node_modules':
            plan['review_needed'].append({
                'action': f"审查 node_modules 目录 ({format_size(dir_info['size'])})",
                'description': '可以通过 npm install 重新生成，但删除后需要重新下载',
                'potential_savings': dir_info['size'],
                'commands': ['npm install'],
                'Risk_level': '低风险（可重新生成）',
            })
        elif dir_info['relative_path'] == 'models':
            plan['review_needed'].append({
                'action': f"审查 models 目录 ({format_size(dir_info['size'])})",
                'description': '模型文件较大，可以考虑使用Git LFS或放到单独的位置',
                'potential_savings': dir_info['size'],
                'Risk_level': '高风险（重新下载耗时）',
            })
        elif dir_info['relative_path'] == 'data':
            plan['review_needed'].append({
                'action': f"审查 data 目录 ({format_size(dir_info['size'])})",
                'description': '数据目录包含重要数据，需要仔细审查。根据项目规则，部分目录（如 data/memory_v2/, data/learning/ 等）绝对不能删除',
                'potential_savings': dir_info['size'],
                'Risk_level': '高风险（包含重要数据）',
            })
    
    # 3. 长期优化建议
    if missing_ignores:
        plan['long_term_suggestions'].append({
            'suggestion': '完善 .gitignore 文件',
            'description': f'建议添加 {len(missing_ignores)} 个忽略规则，防止缓存和临时文件被提交到版本控制',
            'details': missing_ignores,
        })
    
    plan['long_term_suggestions'].append({
        'suggestion': '使用 Git LFS 管理大文件',
        'description': '对于 models/ 目录中的模型文件，建议使用 Git LFS 来管理，减少仓库大小',
    })
    
    plan['long_term_suggestions'].append({
        'suggestion': '定期清理缓存和临时文件',
        'description': '建议将缓存清理命令添加到定期任务中，保持项目整洁',
    })
    
    # 计算总潜在节省空间
    total_immediate = sum(action['potential_savings'] for action in plan['immediate_actions'])
    total_review = sum(item['potential_savings'] for item in plan['review_needed'])
    plan['total_potential_savings'] = total_immediate + total_review
    plan['total_potential_savings_formatted'] = format_size(plan['total_potential_savings'])
    plan['immediate_savings_formatted'] = format_size(total_immediate)
    
    print(f"\n完成！潜在可节省空间: {plan['total_potential_savings_formatted']}")
    print(f"可立即安全清理: {plan['immediate_savings_formatted']}")
    print("=" * 60)
    
    return plan

def save_plan(plan, output_path):
    """保存瘦身方案到文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Somn 项目瘦身方案\n\n")
        f.write(f"生成时间: {plan['timestamp']}\n")
        f.write(f"项目路径: {plan['project_root']}\n\n")
        
        f.write("## 执行摘要\n\n")
        f.write(f"- **潜在可节省总空间**: {plan['total_potential_savings_formatted']}\n")
        f.write(f"- **可立即安全清理**: {plan['immediate_savings_formatted']}\n")
        f.write(f"- **立即执行操作**: {len(plan['immediate_actions'])} 项\n")
        f.write(f"- **需要审查操作**: {len(plan['review_needed'])} 项\n")
        f.write(f"- **长期优化建议**: {len(plan['long_term_suggestions'])} 项\n\n")
        
        f.write("## 一、可立即执行的安全操作（低风险）\n\n")
        if plan['immediate_actions']:
            for i, action in enumerate(plan['immediate_actions'], 1):
                f.write(f"### {i}. {action['action']}\n\n")
                f.write(f"**风险等级**: {action['Risk_level']}\n\n")
                f.write(f"**说明**: {action['description']}\n\n")
                if action['potential_savings'] > 0:
                    f.write(f"**可节省空间**: {format_size(action['potential_savings'])}\n\n")
                if 'commands' in action:
                    f.write("**执行命令**:\n\n")
                    for cmd in action['commands']:
                        f.write(f"```bash\n{cmd}\n```\n\n")
                f.write("---\n\n")
        else:
            f.write("无立即可执行的安全操作。\n\n")
        
        f.write("## 二、需要审查的操作（中等/高风险）\n\n")
        if plan['review_needed']:
            for i, item in enumerate(plan['review_needed'], 1):
                f.write(f"### {i}. {item['action']}\n\n")
                f.write(f"**风险等级**: {item['Risk_level']}\n\n")
                f.write(f"**说明**: {item['description']}\n\n")
                if item['potential_savings'] > 0:
                    f.write(f"**可节省空间**: {format_size(item['potential_savings'])}\n\n")
                if 'commands' in item:
                    f.write("**相关命令**:\n\n")
                    for cmd in item['commands']:
                        f.write(f"```bash\n{cmd}\n```\n\n")
                f.write("---\n\n")
        else:
            f.write("无需审查的操作。\n\n")
        
        f.write("## 三、长期优化建议\n\n")
        if plan['long_term_suggestions']:
            for i, suggestion in enumerate(plan['long_term_suggestions'], 1):
                f.write(f"### {i}. {suggestion['suggestion']}\n\n")
                f.write(f"{suggestion['description']}\n\n")
                if 'details' in suggestion:
                    f.write("**建议添加的忽略规则**:\n\n")
                    for detail in suggestion['details']:
                        f.write(f"- `{detail}`\n")
                    f.write("\n")
                f.write("---\n\n")
        else:
            f.write("无长期优化建议。\n\n")
        
        f.write("## 四、大目录分析\n\n")
        if plan['large_dirs']:
            f.write(f"共发现 {len(plan['large_dirs'])} 个可能的大目录:\n\n")
            for dir_info in plan['large_dirs']:
                f.write(f"- **{dir_info['relative_path']}** - {format_size(dir_info['size'])} ({dir_info['file_count']} 文件)\n")
        else:
            f.write("未发现特殊的大目录。\n")
        f.write("\n")
        
        f.write("## 五、.gitignore 建议\n\n")
        if plan['missing_gitignore']:
            f.write(f"建议将以下 {len(plan['missing_gitignore'])} 个规则添加到 `.gitignore`:\n\n")
            for ignore in plan['missing_gitignore']:
                f.write(f"- `{ignore}`\n")
        else:
            f.write("`.gitignore` 已完善。\n")
        f.write("\n")
        
        f.write("## 六、执行步骤建议\n\n")
        f.write("1. **第一步**: 执行「可立即执行的安全操作」，这些操作风险低，可显著减少项目大小\n")
        f.write("2. **第二步**: 审查「需要审查的操作」，根据实际情况决定是否执行\n")
        f.write("3. **第三步**: 实施「长期优化建议」，完善项目配置\n")
        f.write("4. **第四步**: 定期执行缓存清理，保持项目整洁\n\n")
        
        f.write("---\n\n")
        f.write("*本方案由项目瘦身方案生成器自动生成*\n")
    
    print(f"方案已保存到: {output_path}")

if __name__ == '__main__':
    project_root = 'd:/AI/somn'
    output_path = os.path.join(project_root, 'file/系统文件/项目瘦身方案.md')
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 生成瘦身方案
    plan = generate_slimdown_plan(project_root)
    
    if plan:
        # 保存方案到JSON
        json_path = os.path.join(project_root, 'project_slimdown_plan.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        print(f"方案数据已保存到: {json_path}")
        
        # 保存方案到Markdown
        save_plan(plan, output_path)
        
        print("\n完成！请查看方案文档以了解详细的瘦身步骤。")
