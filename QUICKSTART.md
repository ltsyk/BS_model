# 快速开始指南

本指南将帮助你快速启动Black-Scholes期权定价可视化平台。

## 前置要求

### 安装 uv

uv 是一个极快的Python包管理器和项目管理工具。

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**通过 pip:**
```bash
pip install uv
```

**验证安装:**
```bash
uv --version
```

## 快速启动

### 方法1: 使用启动脚本（推荐）

**Linux/macOS:**
```bash
chmod +x run.sh
./run.sh
```

**Windows:**
```cmd
run.bat
```

启动脚本会自动：
1. 检查uv是否安装
2. 创建虚拟环境（如果不存在）
3. 安装所有依赖
4. 启动Web服务器

### 方法2: 使用 Makefile（Linux/macOS）

```bash
# 安装依赖
make install

# 启动服务器
make run
```

### 方法3: 手动步骤

```bash
# 1. 创建虚拟环境
uv venv

# 2. 激活虚拟环境
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# 3. 安装依赖
uv pip install -e .

# 4. 启动服务器
python app.py
```

## 访问应用

服务器启动后，在浏览器中访问：

**http://localhost:5000**

## 运行示例

查看完整的使用示例：

```bash
# 使用 Makefile
make examples

# 或激活虚拟环境后运行
source .venv/bin/activate  # Linux/macOS
# 或 .venv\Scripts\activate  # Windows
python examples.py
```

## 命令行选项

启动服务器时可以自定义参数：

```bash
# 自定义端口
python app.py --port 8080

# 自定义主机
python app.py --host 127.0.0.1

# 启用调试模式
python app.py --debug

# 组合使用
python app.py --host 127.0.0.1 --port 8080 --debug
```

## 作为Python模块使用

```python
from black_scholes import BlackScholesModel

# 创建期权模型
option = BlackScholesModel(
    S=100,      # 标的价格
    K=100,      # 执行价格
    T=1.0,      # 到期时间（年）
    r=0.05,     # 无风险利率
    sigma=0.2,  # 波动率
    option_type='call'
)

# 计算价格
print(f"期权价格: ${option.price():.4f}")

# 计算Greeks
print(f"Delta: {option.delta():.4f}")
print(f"Gamma: {option.gamma():.4f}")
print(f"Theta: {option.theta():.4f}")
print(f"Vega: {option.vega():.4f}")
print(f"Rho: {option.rho():.4f}")
```

## 开发模式

安装开发依赖（包括测试工具、代码格式化等）：

```bash
# 使用 Makefile
make dev

# 或手动安装
uv pip install -e ".[dev]"
```

### 常用开发命令

```bash
# 代码格式化
make format

# 代码检查
make lint

# 运行测试
make test

# 清理缓存
make clean
```

## 项目结构

```
BS_model/
├── app.py                 # Flask Web应用
├── black_scholes.py       # 核心算法
├── examples.py            # 使用示例
├── pyproject.toml         # 项目配置（uv）
├── requirements.txt       # 依赖列表（备用）
├── run.sh                 # Unix启动脚本
├── run.bat                # Windows启动脚本
├── Makefile              # 开发命令
├── templates/            # HTML模板
│   └── index.html
└── static/               # 静态资源
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## 常见问题

### Q: 端口5000已被占用？
A: 使用 `--port` 参数指定其他端口：
```bash
python app.py --port 8080
```

### Q: 如何更新依赖？
A: 运行：
```bash
uv pip install -e . --upgrade
```

### Q: 虚拟环境损坏了怎么办？
A: 删除并重新创建：
```bash
rm -rf .venv
uv venv
uv pip install -e .
```

### Q: 在Windows上运行脚本权限错误？
A: 以管理员身份运行PowerShell，或直接使用：
```cmd
python app.py
```

## 性能优化

uv 相比传统的 pip 有显著的性能优势：

- **更快的依赖解析**: uv 使用 Rust 编写，速度比 pip 快10-100倍
- **并行下载**: 同时下载多个包
- **智能缓存**: 避免重复下载
- **更好的依赖解析**: 更可靠的依赖冲突解决

## 下一步

- 阅读 [README.md](README.md) 了解详细功能
- 运行 `examples.py` 学习各种使用场景
- 修改参数，观察期权价格和Greeks的变化
- 探索可视化图表，理解期权定价原理

## 获取帮助

如有问题，请：
1. 查看 [README.md](README.md) 完整文档
2. 运行示例代码学习用法
3. 提交 GitHub Issue

祝学习愉快！
