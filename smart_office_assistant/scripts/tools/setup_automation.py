#!/usr/bin/env python3
"""
设置超级学习计划的自动化任务
"""

import sys
import os

# 设置自动化任务
def setup_super_learning_automation():
    print("="*80)
    print("🤖 设置超级学习计划自动化")
    print("="*80)
    
    print("\n⚠️  注意: 自动化任务将在后台运行，每5分钟执行一次深度学习")
    print("📅 每日21:00自动生成学习报告")
    print("\n请选择:")
    print("1. 立即启动学习计划（前台运行）")
    print("2. 设置为系统计划任务（后台运行）")
    print("3. 测试单次学习")
    print("0. 退出")
    
    choice = input("\n请输入选项: ").strip()
    
    if choice == "1":
        print("\n🚀 启动超级学习计划...")
        os.system("python super_learning_system.py --interval 5 --report-time 21:00")
    
    elif choice == "2":
        print("\n⚙️  设置自动化任务...")
        print("\n对于Windows用户:")
        print("  1. 打开'任务计划程序'")
        print("  2. 创建基本任务")
        print("  3. 设置触发器: 当计算机启动时")
        print("  4. 设置操作: 启动程序")
        print(f"  5. 程序/脚本: {PYTHON_EXECUTABLE}")
        print(f"  6. 参数: {SUPER_LEARNING_SCRIPT} --interval 5 --report-time 21:00")
        print(f"  7. 起始于: {PROJECT_ROOT}")

        
        print("\n对于Linux/Mac用户:")
        print("  1. 编辑crontab: crontab -e")
        print("  2. 添加: @reboot cd /path/to/smart_office_assistant && python3 super_learning_system.py --interval 5 --report-time 21:00")
        print("  3. 保存退出")
        
        input("\n按回车键继续...")
    
    elif choice == "3":
        print("\n🧪 执行单次学习测试...")
        os.system("python super_learning_system.py --single")
    
    elif choice == "0":
        print("\n👋 退出")
        return
    
    else:
        print("\n❌ 无效选项")


if __name__ == "__main__":
    setup_super_learning_automation()
