"""
学习监控和报告生成脚本
监控学习进度，完成后自动生成详细报告
"""

import time
import json
import subprocess
from pathlib import Path
from datetime import datetime

def check_learning_progress():
    """检查学习进度"""
    progress_file = Path("data/learning/finest_grain/progress.json")
    
    if not progress_file.exists():
        return None
    
    with open(progress_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    learned_count = len(data.get("learned_files", []))
    total_files = 8596
    
    return {
        'learned': learned_count,
        'total': total_files,
        'progress': learned_count / total_files * 100,
        'remaining': total_files - learned_count
    }

def is_learning_complete():
    """检查学习是否完成"""
    progress = check_learning_progress()
    if not progress:
        return False
    
    return progress['remaining'] == 0

def monitor_learning():
    """监控学习进度"""
    print("=" * 80)
    print("开始监控学习进度...")
    print("=" * 80)
    
    last_progress = 0
    start_time = datetime.now()
    
    while True:
        progress = check_learning_progress()
        
        if not progress:
            print("⚠️  无法读取进度文件")
            time.sleep(60)
            continue
        
        # 显示进度
        elapsed = (datetime.now() - start_time).total_seconds()
        speed = (progress['learned'] - last_progress) / (elapsed / 3600) if elapsed > 0 and last_progress > 0 else 0
        
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 学习进度: {progress['learned']:,}/{progress['total']:,} ({progress['progress']:.1f}%)")
        print(f"    剩余: {progress['remaining']:,} 个文件")
        if speed > 0:
            eta = progress['remaining'] / speed
            print(f"    速度: {speed:.0f} 文件/小时")
            print(f"    预计剩余时间: {eta/3600:.1f} 小时")
        
        # 检查是否完成
        if progress['remaining'] == 0:
            print("\n" + "=" * 80)
            print("🎉 学习完成！")
            print("=" * 80)
            return True
        
        # 更新上次进度
        last_progress = progress['learned']
        
        # 等待5分钟
        print("    等待5分钟后再次检查...")
        time.sleep(300)

def generate_report():
    """生成学习报告"""
    print("\n开始生成学习报告...")
    
    try:
        result = subprocess.run(
            ["python", "generate_learning_report.py"],
            capture_output=True,
            text=True,
            timeout=3600  # 1小时超时
        )
        
        print(result.stdout)
        if result.stderr:
            print("警告:", result.stderr)
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ 报告生成超时")
        return False
    except Exception as e:
        print(f"❌ 报告生成失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 80)
    print("学习监控和报告生成系统")
    print("=" * 80)
    print()
    
    # 检查学习是否已完成
    if is_learning_complete():
        print("✅ 学习已经完成！")
        print()
        generate_report()
    else:
        # 监控学习进度
        if monitor_learning():
            # 学习完成，生成报告
            generate_report()
    
    print("\n" + "=" * 80)
    print("所有任务完成！")
    print("=" * 80)

if __name__ == "__main__":
    main()
