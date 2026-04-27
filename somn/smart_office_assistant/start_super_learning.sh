#!/bin/bash

echo "========================================"
echo "启动超级学习计划"
echo "========================================"
echo ""
echo "学习间隔: 5分钟"
echo "报告时间: 21:00"
echo ""
echo "按任意键开始..."
read -n 1

python3 super_learning_system.py --interval 5 --report-time 21:00

echo ""
echo "学习计划已完成或已停止"
echo "报告已生成在 data/learning/super_learning/"
