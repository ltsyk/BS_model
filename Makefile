.PHONY: help install dev run examples test clean format lint

help:
	@echo "Black-Scholes 可视化平台 - 开发命令"
	@echo ""
	@echo "可用命令:"
	@echo "  make install    - 安装项目依赖"
	@echo "  make dev        - 安装开发依赖"
	@echo "  make run        - 启动Web服务器"
	@echo "  make examples   - 运行示例代码"
	@echo "  make test       - 运行测试"
	@echo "  make format     - 格式化代码"
	@echo "  make lint       - 代码检查"
	@echo "  make clean      - 清理缓存文件"
	@echo ""

install:
	@echo "安装项目依赖..."
	uv pip install -r requirements.txt

dev:
	@echo "安装开发依赖..."
	uv pip install -e ".[dev]"

run:
	@echo "启动服务器..."
	@. .venv/bin/activate && python app.py

examples:
	@echo "运行示例代码..."
	@. .venv/bin/activate && python examples.py

test:
	@echo "运行测试..."
	@. .venv/bin/activate && pytest

format:
	@echo "格式化代码..."
	@. .venv/bin/activate && black .

lint:
	@echo "代码检查..."
	@. .venv/bin/activate && flake8 .

clean:
	@echo "清理缓存文件..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	@echo "清理完成!"
