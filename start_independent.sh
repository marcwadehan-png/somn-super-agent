#!/bin/bash
# ============================================================
# Somn AI 独立运行启动脚本 v2.0
# 无需WorkBuddy，可直接在任意Linux/macOS设备运行
# ============================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "============================================================"
echo "  Somn AI 独立运行版 v2.0"
echo "  不依赖WorkBuddy，复制即可运行"
echo "============================================================"
echo ""

# 检测Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}[错误] 未检测到Python，请先安装Python 3.11+${NC}"
    echo "下载地址: https://www.python.org/downloads/"
    exit 1
fi

# 显示Python版本
echo -e "[信息] 检测到Python:"
$PYTHON_CMD --version
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检测虚拟环境
if [ -f "smart_office_assistant/.venv/bin/activate" ]; then
    echo "[信息] 检测到虚拟环境，正在激活..."
    source smart_office_assistant/.venv/bin/activate
    PYTHON_CMD="python"
fi

# 检查依赖
echo "[信息] 检查核心依赖..."
$PYTHON_CMD -c "import sys; sys.path.insert(0, '.'); from src.core.paths import ensure_directories; ensure_directories(); print('[OK] 路径系统正常')" 2>/dev/null || {
    echo -e "${YELLOW}[警告] 核心模块导入失败，尝试安装依赖...${NC}"
    $PYTHON_CMD -m pip install -q -r smart_office_assistant/requirements.txt || {
        echo -e "${YELLOW}[警告] 自动安装失败，请手动执行:${NC}"
        echo "  pip install -r smart_office_assistant/requirements.txt"
    }
}

echo ""
echo "============================================================"
echo "  选择运行模式:"
echo "============================================================"
echo "  1. GUI模式 (图形界面)"
echo "  2. CLI交互模式 (命令行)"
echo "  3. 健康检查"
echo "  4. 系统状态"
echo "  5. 列出解决方案"
echo "  6. 单次查询 (需要输入)"
echo "  0. 退出"
echo "============================================================"
echo ""

read -p "请输入选项 [1-6, 0退出]: " MODE_CHOICE

case $MODE_CHOICE in
    1) 
        echo "[信息] 启动GUI模式..."
        cd "$SCRIPT_DIR"
        $PYTHON_CMD smart_office_assistant/run.py --gui
        ;;
    2) 
        echo "[信息] 启动CLI交互模式..."
        echo "输入 quit/exit 退出"
        cd "$SCRIPT_DIR"
        $PYTHON_CMD smart_office_assistant/run.py --cli
        ;;
    3) 
        echo "[信息] 执行健康检查..."
        cd "$SCRIPT_DIR"
        $PYTHON_CMD smart_office_assistant/run.py --health
        ;;
    4) 
        echo "[信息] 显示系统状态..."
        cd "$SCRIPT_DIR"
        $PYTHON_CMD smart_office_assistant/run.py --status
        ;;
    5) 
        echo "[信息] 列出解决方案..."
        cd "$SCRIPT_DIR"
        $PYTHON_CMD smart_office_assistant/run.py --solutions
        ;;
    6) 
        echo ""
        read -p "请输入查询内容: " USER_QUERY
        cd "$SCRIPT_DIR"
        $PYTHON_CMD smart_office_assistant/run.py --cli -q "$USER_QUERY"
        ;;
    0) 
        exit 0
        ;;
    *) 
        echo "[错误] 无效选项"
        exit 1
        ;;
esac
