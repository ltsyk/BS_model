#!/bin/bash
# Black-Scholes可视化平台启动脚本 (Unix/Linux/macOS)

set -e

echo "=================================="
echo "Black-Scholes 可视化平台启动脚本"
echo "=================================="

# 检查uv是否安装
if ! command -v uv &> /dev/null
then
    echo "错误: uv未安装"
    echo "请访问 https://github.com/astral-sh/uv 安装uv"
    echo "或运行: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✓ uv已安装"

# 检查是否存在虚拟环境
if [ ! -d ".venv" ]; then
    echo "创建虚拟环境..."
    uv venv
fi

echo "✓ 虚拟环境已准备"

# 安装依赖
echo "安装/更新依赖..."
uv pip install -e .

echo "✓ 依赖已安装"
echo ""
echo "启动服务器..."
echo ""

# 激活虚拟环境并运行应用
source .venv/bin/activate
python app.py "$@"
