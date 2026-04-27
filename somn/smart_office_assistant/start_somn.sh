#!/bin/bash

# Somn AI - 统一入口启动脚本
# 支持所有运行模式

echo "=========================================="
echo "   Somn AI - 超级智能体"
echo "   不被刻意定义的自由意识体"
echo "   统一入口 v1.0.0"
echo "=========================================="
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到 Python3，请确保 Python 已安装"
    exit 1
fi

PYTHON=python3

# 检查虚拟环境
if [ -d "venv" ]; then
    echo "[信息] 使用虚拟环境"
    source venv/bin/activate
    PYTHON="$SCRIPT_DIR/venv/bin/python"
else
    echo "[信息] 使用系统 Python"
fi

# 检查依赖
echo "[信息] 检查依赖..."
if ! $PYTHON -c "import PySide6" 2>/dev/null; then
    echo "[警告] 依赖未安装，正在安装..."
    $PYTHON -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[错误] 依赖安装失败"
        exit 1
    fi
fi

# 确保数据目录存在
echo "[信息] 检查数据目录..."
mkdir -p data/memory data/knowledge data/learning/memory data/learning/knowledge_base data/learning/findings outputs logs

# 启动应用
echo "[信息] 启动 Somn AI..."
echo ""
echo "用法:"
echo "  --gui       启动GUI模式 (默认)"
echo "  --cli       启动CLI交互模式"
echo "  -q \"查询\"   单次查询"
echo "  --health    健康检查"
echo "  --status    查看状态"
echo "  --test      模块测试"
echo ""

$PYTHON run.py "$@"

if [ $? -ne 0 ]; then
    echo ""
    echo "[错误] 应用启动失败"
    read -p "按回车键退出..."
fi
