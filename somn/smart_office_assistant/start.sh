#!/bin/bash

# SmartOffice AI 启动脚本

echo "=========================================="
echo "   Somn - 汇千古之智，向未知而生"
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

# 启动应用
echo "[信息] 启动 SmartOffice AI..."
echo ""
$PYTHON main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[错误] 应用启动失败"
    read -p "按回车键退出..."
fi
