@echo off
chcp 65001 >nul
title Somn - 汇千古之智，向未知而生

echo ==========================================
echo    Somn - 汇千古之智，向未知而生
echo ==========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请确保 Python 已安装并添加到 PATH
    pause
    exit /b 1
)

REM 检查虚拟环境
if exist "venv\Scripts\python.exe" (
    echo [信息] 使用虚拟环境
    set PYTHON=venv\Scripts\python.exe
) else (
    echo [信息] 使用系统 Python
    set PYTHON=python
)

REM 检查依赖
echo [信息] 检查依赖...
%PYTHON% -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo [警告] 依赖未安装，正在安装...
    %PYTHON% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
)

REM 确保数据目录存在
echo [信息] 检查数据目录...
if not exist "data\memory" mkdir data\memory
if not exist "data\knowledge" mkdir data\knowledge
if not exist "data\learning\memory" mkdir data\learning\memory
if not exist "data\learning\knowledge_base" mkdir data\learning\knowledge_base
if not exist "data\learning\findings" mkdir data\learning\findings
if not exist "outputs" mkdir outputs
if not exist "logs" mkdir logs

REM 启动应用
echo [信息] 启动 Somn...
echo.
%PYTHON% main.py

if errorlevel 1 (
    echo.
    echo [错误] 应用启动失败
    pause
)
