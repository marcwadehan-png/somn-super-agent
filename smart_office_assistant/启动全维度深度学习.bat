@echo off
chcp 65001 >nul
echo ============================================================
echo Somn项目 - 全维度深度学习系统
echo ============================================================
echo.
echo 本系统将：
echo   1. 扫描E盘所有资料（PMP、保险、简历、Abyss AI）
echo   2. 启动所有19个学习维度
echo   3. 深度学习所有资料
echo   4. 自动识别学习不足
echo   5. 生成优化建议报告
echo.
echo ============================================================
echo.

cd /d "%~dp0"

echo [选项]
echo   1. 启动完整学习流程（E盘 + 网络）
echo   2. 仅E盘深度学习
echo   3. 仅网络学习
echo   4. 分析学习状态
echo   5. 生成学习报告
echo   0. 退出
echo.
set /p choice=请选择操作 (0-5): 

if "%choice%"=="1" (
    echo.
    echo [启动] 完整学习流程...
    python integrated_learning_system.py
) else if "%choice%"=="2" (
    echo.
    echo [启动] E盘深度学习...
    python e_drive_learning_system.py
) else if "%choice%"=="3" (
    echo.
    echo [启动] 网络学习...
    python super_learning_system.py
) else if "%choice%"=="4" (
    echo.
    echo [分析] 学习状态分析...
    python integrated_learning_system.py --analyze-only
) else if "%choice%"=="5" (
    echo.
    echo [生成] 学习报告...
    python e_drive_learning_system.py --report-only
) else if "%choice%"=="0" (
    echo.
    echo [退出] 用户取消
) else (
    echo.
    echo [错误] 无效选择
)

echo.
echo ============================================================
echo 操作完成
echo ============================================================
echo.
pause
