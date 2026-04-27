#!/usr/bin/env python3
"""
重构计划生成器 - 为复杂文件制定详细的重构计划
"""
import os
import sys
from datetime import datetime

def analyze_complexity(file_path):
    """分析文件复杂度"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.count('\n') + 1
            # 计算函数数量（简单估算）
            func_count = content.count('def ') + content.count('class ')
            # 计算导入数量
            import_count = content.count('import ') + content.count('from ')
            # 估算复杂度
            complexity = lines * 0.3 + func_count * 2 + import_count * 0.5
            
            return {
                'lines': lines,
                'func_count': func_count,
                'import_count': import_count,
                'complexity_score': complexity,
            }
    except:
        return None

def categorize_file(file_path, lines):
    """将文件分类，以便制定重构策略"""
    filename = os.path.basename(file_path)
    
    # 根据文件名和路径分类
    if 'test_' in filename:
        return 'test'  # 测试文件
    elif 'engine' in filename.lower():
        return 'engine'  # 引擎类文件
    elif 'manager' in filename.lower():
        return 'manager'  # 管理类文件
    elif 'core' in filename.lower():
        return 'core'  # 核心文件
    elif 'dispatcher' in filename.lower() or 'dispatch' in filename.lower():
        return 'dispatcher'  # 调度类文件
    elif 'scheduler' in filename.lower():
        return 'scheduler'  # 调度器文件
    elif 'coordinator' in filename.lower():
        return 'coordinator'  # 协调器文件
    elif lines > 1500:
        return 'very_complex'  # 非常复杂
    elif lines > 1000:
        return 'complex'  # 复杂
    else:
        return 'moderate'  # 中等复杂度

def generate_refactor_suggestions(file_path, analysis):
    """生成重构建议"""
    suggestions = []
    lines = analysis['lines']
    func_count = analysis['func_count']
    import_count = analysis['import_count']
    
    # 基于行数的建议
    if lines > 2000:
        suggestions.append(f"文件非常大（{lines} 行），建议拆分为 3-5 个模块")
        suggestions.append("可以按功能域拆分：将相关的函数和类放到单独的文件中")
    elif lines > 1500:
        suggestions.append(f"文件很大（{lines} 行），建议拆分为 2-3 个模块")
    elif lines > 1000:
        suggestions.append(f"文件较大（{lines} 行），建议拆分为 2 个模块")
    
    # 基于函数数量的建议
    if func_count > 30:
        suggestions.append(f"包含大量函数/类（约{func_count} 个），建议按功能分组")
    
    # 基于导入数量的建议
    if import_count > 30:
        suggestions.append(f"导入语句较多（约{import_count} 个），建议检查是否有未使用的导入")
        suggestions.append("考虑使用延迟导入（在函数内部导入）减少启动时间")
    
    # 通用建议
    suggestions.append("添加/完善文档字符串（docstring）")
    suggestions.append("添加类型注解（项目当前覆盖率20.79%）")
    suggestions.append("考虑函数/类的单一职责原则（SRP）")
    
    return suggestions

def generate_refactor_plan(project_root):
    """生成详细的重构计划"""
    print("生成重构计划...")
    
    # 读取之前的分析结果
    analysis_path = os.path.join(project_root, 'project_slimdown_analysis.json')
    complex_files = []
    
    # 重新扫描复杂文件
    print("扫描复杂文件...")
    for root, dirs, files in os.walk(project_root):
        # 跳过不需要分析的目录
        skip_dirs = ['__pycache__', 'node_modules', '.git', 'venv', 'env', '.workbuddy', '.codebuddy', 'models']
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if not file.endswith('.py'):
                continue
            
            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.read().count('\n') + 1
                    
                    if lines > 500:
                        analysis = analyze_complexity(file_path)
                        if analysis:
                            category = categorize_file(file_path, lines)
                            suggestions = generate_refactor_suggestions(file_path, analysis)
                            
                            complex_files.append({
                                'path': file_path,
                                'relative_path': os.path.relpath(file_path, project_root),
                                'lines': lines,
                                'category': category,
                                'analysis': analysis,
                                'suggestions': suggestions,
                            })
            except:
                pass
    
    # 按行数排序
    complex_files.sort(key=lambda x: x['lines'], reverse=True)
    
    print(f"共发现 {len(complex_files)} 个复杂文件")
    
    # 生成重构计划
    plan = {
        'timestamp': datetime.now().isoformat(),
        'project_root': project_root,
        'total_complex_files': len(complex_files),
        'refactor_plan': [],
    }
    
    # 优先级1: 最复杂的文件（>1500行）
    priority1 = [f for f in complex_files if f['lines'] > 1500]
    # 优先级2: 中等复杂文件（1000-1500行）
    priority2 = [f for f in complex_files if 1000 < f['lines'] <= 1500]
    # 优先级3: 较复杂文件（500-1000行）
    priority3 = [f for f in complex_files if 500 < f['lines'] <= 1000]
    
    plan['refactor_plan'] = [
        {
            'priority': 1,
            'description': '最复杂的文件（>1500行），建议立即重构',
            'count': len(priority1),
            'files': priority1[:20],  # 只取前20个
        },
        {
            'priority': 2,
            'description': '中等复杂文件（1000-1500行），建议逐步重构',
            'count': len(priority2),
            'files': priority2[:20],
        },
        {
            'priority': 3,
            'description': '较复杂文件（500-1000行），建议考虑重构',
            'count': len(priority3),
            'files': priority3[:20],
        },
    ]
    
    return plan

def save_refactor_plan(plan, output_path):
    """保存重构计划到文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Somn 项目重构计划\n\n")
        f.write(f"生成时间: {plan['timestamp']}\n")
        f.write(f"项目路径: {plan['project_root']}\n\n")
        
        f.write("## 执行摘要\n\n")
        f.write(f"- **复杂文件总数**: {plan['total_complex_files']} 个\n")
        f.write(f"- **优先级1（>1500行）**: {plan['refactor_plan'][0]['count']} 个\n")
        f.write(f"- **优先级2（1000-1500行）**: {plan['refactor_plan'][1]['count']} 个\n")
        f.write(f"- **优先级3（500-1000行）**: {plan['refactor_plan'][2]['count']} 个\n\n")
        
        f.write("## 重构策略\n\n")
        f.write("### 1. 拆分策略\n\n")
        f.write("对于大型文件，建议按以下方式拆分：\n\n")
        f.write("1. **按功能域拆分**: 将相关的函数和类放到单独的文件中\n")
        f.write("2. **按层级拆分**: 将不同抽象层级的功能分开（如：API层、业务逻辑层、数据访问层）\n")
        f.write("3. **按变化频率拆分**: 将经常变化的部分和不常变化的部分分开\n\n")
        
        f.write("### 2. 重构步骤\n\n")
        f.write("1. **第一步**: 为待重构文件编写测试（确保重构后功能不变）\n")
        f.write("2. **第二步**: 识别可以提取的函数/类\n")
        f.write("3. **第三步**: 创建新模块，将代码移过去\n")
        f.write("4. **第四步**: 更新导入语句\n")
        f.write("5. **第五步**: 运行测试，确保功能不变\n")
        f.write("6. **第六步**: 提交代码，做小幅、频繁的提交\n\n")
        
        f.write("### 3. 注意事项\n\n")
        f.write("1. **保持功能不变**: 重构的目的是改善代码结构，不改变外部行为\n")
        f.write("2. **逐步重构**: 不要一次性重构太多文件，降低风险\n")
        f.write("3. **编写测试**: 重构前确保有足够的测试覆盖\n")
        f.write("4. **代码审查**: 重构后的代码需要仔细审查\n\n")
        
        # 详细重构计划
        for plan_item in plan['refactor_plan']:
            priority = plan_item['priority']
            f.write(f"## 优先级 {priority}: {plan_item['description']}\n\n")
            f.write(f"共 {plan_item['count']} 个文件\n\n")
            
            if plan_item['files']:
                f.write("### 文件列表（前20个）:\n\n")
                
                for i, file_info in enumerate(plan_item['files']):
                    rel_path = file_info['relative_path']
                    lines = file_info['lines']
                    category = file_info['category']
                    analysis = file_info['analysis']
                    suggestions = file_info['suggestions']
                    
                    f.write(f"{i+1}. `{rel_path}` - {lines} 行（分类: {category}）\n\n")
                    f.write(f"   - 函数/类数量: 约{analysis['func_count']} 个\n")
                    f.write(f"   - 导入数量: 约{analysis['import_count']} 个\n")
                    f.write(f"   - 复杂度评分: {analysis['complexity_score']:.1f}\n\n")
                    
                    f.write("   - **重构建议**:\n")
                    for j, suggestion in enumerate(suggestions[:5]):  # 只显示前5条建议
                        f.write(f"     {j+1}. {suggestion}\n")
                    
                    f.write("\n")
            
            f.write("\n")
        
        f.write("## 重构时间表建议\n\n")
        f.write("### 第1周: 优先级1的文件（>1500行）\n\n")
        f.write("选择2-3个最重要的文件开始重构，建立重构模式\n\n")
        
        f.write("### 第2-4周: 继续优先级1的文件\n\n")
        f.write("完成所有优先级1的文件重构\n\n")
        
        f.write("### 第5-8周: 优先级2的文件（1000-1500行）\n\n")
        f.write("逐步重构优先级2的文件\n\n")
        
        f.write("### 第9-12周: 优先级3的文件（500-1000行）\n\n")
        f.write("考虑重构优先级3的文件，或评估是否值得重构\n\n")
        
        f.write("## 工具推荐\n\n")
        f.write("1. **代码质量工具**: pylint, flake8, mypy\n")
        f.write("2. **重构工具**: rope (Python重构库)\n")
        f.write("3. **测试工具**: pytest, coverage\n")
        f.write("4. **性能分析**: cProfile, line_profiler\n\n")
        
        f.write("---\n\n")
        f.write("*本报告由重构计划生成器自动生成*\n")
    
    print(f"重构计划已保存到: {output_path}")

if __name__ == '__main__':
    project_root = 'd:/AI/somn'
    output_path = os.path.join(project_root, 'file/系统文件/项目重构计划.md')
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print("=" * 60)
    print("Somn 项目重构计划生成器")
    print("=" * 60)
    
    # 生成重构计划
    plan = generate_refactor_plan(project_root)
    
    # 保存重构计划
    save_refactor_plan(plan, output_path)
    
    print("\n" + "=" * 60)
    print("重构计划生成完成！")
    print("=" * 60)
    
    # 输出摘要
    print(f"\n复杂文件总数: {plan['total_complex_files']} 个")
    print(f"优先级1（>1500行）: {plan['refactor_plan'][0]['count']} 个")
    print(f"优先级2（1000-1500行）: {plan['refactor_plan'][1]['count']} 个")
    print(f"优先级3（500-1000行）: {plan['refactor_plan'][2]['count']} 个")
    print(f"\n详细计划: {output_path}")
