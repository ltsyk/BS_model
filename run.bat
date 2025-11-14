@echo off
REM Black-Scholes可视化平台启动脚本 (Windows)

echo ==================================
echo Black-Scholes 可视化平台启动脚本
echo ==================================

REM 检查uv是否安装
where uv >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 错误: uv未安装
    echo 请访问 https://github.com/astral-sh/uv 安装uv
    echo 或运行: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    exit /b 1
)

echo √ uv已安装

REM 检查是否存在虚拟环境
if not exist ".venv" (
    echo 创建虚拟环境...
    uv venv
)

echo √ 虚拟环境已准备

REM 安装依赖
echo 安装/更新依赖...
uv pip install -e .

echo √ 依赖已安装
echo.
echo 启动服务器...
echo.

REM 运行应用
uv run python app.py %*
