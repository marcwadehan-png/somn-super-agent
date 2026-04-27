@echo off
chcp 65001 >nul
title SmartOffice AI - 安装程序

echo ==========================================
echo    Somn - 汇千古之智，向未知而生
echo    安装程序
echo ==========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请访问 https://python.org 下载安装
    pause
    exit /b 1
)

echo [信息] Python 版本:
python --version
echo.

REM 创建虚拟环境
if not exist "venv" (
    echo [信息] 创建虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo [错误] 创建虚拟环境失败
        pause
        exit /b 1
    )
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 升级 pip
echo [信息] 升级 pip...
python -m pip install --upgrade pip

REM 安装依赖
echo [信息] 安装依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] 安装依赖失败
    pause
    exit /b 1
)

REM 创建必要的目录
echo [信息] 创建数据目录...
mkdir data\memory 2>nul
mkdir data\knowledge 2>nul
mkdir data\learning\memory 2>nul
mkdir data\learning\knowledge_base 2>nul
mkdir data\learning\findings 2>nul
mkdir data\learning\reasoning 2>nul
mkdir data\learning\validation 2>nul
mkdir data\learning\learning 2>nul
mkdir data\learning\evolution 2>nul
mkdir outputs 2>nul
mkdir logs 2>nul
mkdir templates 2>nul

echo.
echo ==========================================
echo    安装完成！
echo ==========================================
echo.
echo 启动方式:
echo   1. 双击 start.bat 启动
echo   2. 运行: python main.py
echo.
echo 打包为可执行文件:
echo   1. 安装 PyInstaller: pip install pyinstaller
echo   2. 运行: pyinstaller SmartOffice.spec
echo.
pause
