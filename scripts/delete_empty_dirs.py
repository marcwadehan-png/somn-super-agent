#!/usr/bin/env python3
"""
安全删除空目录脚本
"""
import os
import sys

def delete_empty_dirs(root_path, protected_paths=None):
    """递归删除空目录，保护指定路径"""
    if protected_paths is None:
        protected_paths = []
    
    # 将保护路径转换为绝对路径
    protected_abs = [os.path.abspath(p) for p in protected_paths]
    
    deleted = []
    failed = []
    
    # 自底向上遍历目录
    for root, dirs, files in os.walk(root_path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.abspath(os.path.join(root, dir_name))
            
            # 检查是否在保护列表中
            if dir_path in protected_abs:
                continue
            
            try:
                # 检查目录是否为空
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    deleted.append(dir_path)
                    print(f"已删除: {dir_path}")
            except OSError as e:
                failed.append((dir_path, str(e)))
    
    return deleted, failed

if __name__ == '__main__':
    project_root = 'd:/AI/somn'
    
    # 保护的重要目录（包含重要数据的目录不应删除，即使为空）
    protected = [
        'd:/AI/somn/data/memory_v2',
        'd:/AI/somn/data/q_values',
        'd:/AI/somn/data/learning',
        'd:/AI/somn/data/solution_learning',
        'd:/AI/somn/data/memory',
        'd:/AI/somn/data/feedback_production',
        'd:/AI/somn/data/feedback_loop',
        'd:/AI/somn/data/reasoning',
        'd:/AI/somn/data/ml',
    ]
    
    print(f"开始扫描空目录: {project_root}")
    print("=" * 60)
    
    deleted, failed = delete_empty_dirs(project_root, protected)
    
    print("=" * 60)
    print(f"完成！共删除 {len(deleted)} 个空目录")
    if failed:
        print(f"失败 {len(failed)} 个")
        for path, error in failed[:10]:
            print(f"  - {path}: {error}")
    print("=" * 60)
