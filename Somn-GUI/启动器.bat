@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ================================
echo    Somn V1.0 快捷启动器
echo ================================
echo.
echo  [1] 全功能套件
echo  [2] 全局控制中心
echo  [3] 传统GUI
echo  [4] 仅后端服务
echo  [0] 退出
echo.

set /p choice=请选择: 

if "%choice%"=="1" start python start_full_suite.py
if "%choice%"=="2" start python start_control_center.py
if "%choice%"=="3" start start_somn.bat
if "%choice%"=="4" start cmd /k "python ..\somn\start_server.py --port 8964"
