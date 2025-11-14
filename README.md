# Black-Scholes期权定价模型可视化学习平台

一个交互式的Black-Scholes期权定价模型可视化学习工具，帮助理解期权定价理论和Greeks敏感性指标。

## 项目简介

本项目实现了完整的Black-Scholes期权定价模型，包括：

- **期权定价计算**：精确计算欧式看涨和看跌期权的理论价格
- **Greeks风险指标**：计算Delta、Gamma、Theta、Vega、Rho等敏感性指标
- **交互式可视化**：实时图表展示期权价格和Greeks随参数变化的关系
- **教育性内容**：详细的模型说明和公式解释

## 功能特性

### 1. 期权定价
- 支持看涨期权（Call）和看跌期权（Put）
- 基于Black-Scholes-Merton公式的精确计算
- 显示内在价值和时间价值分解

### 2. Greeks计算
- **Delta (Δ)**: 标的资产价格敏感度
- **Gamma (Γ)**: Delta变化率
- **Theta (Θ)**: 时间衰减（日度）
- **Vega (ν)**: 波动率敏感度
- **Rho (ρ)**: 利率敏感度

### 3. 可视化图表
- **期权收益图**: 展示期权价格随标的资产价格变化
- **Greeks曲面图**: 3D可视化Greeks随价格和时间的变化
- 使用Plotly.js实现交互式图表

### 4. 隐含波动率计算
- 使用牛顿迭代法从市场价格反推波动率
- 支持自定义精度和迭代次数

## 技术栈

### 后端
- **Python 3.8+**
- **NumPy**: 数值计算
- **SciPy**: 统计函数（正态分布）
- **Flask**: Web框架
- **Flask-CORS**: 跨域支持

### 前端
- **HTML5/CSS3**: 响应式界面
- **JavaScript (ES6+)**: 交互逻辑
- **Plotly.js**: 数据可视化

## 安装与运行

### 环境要求
- Python 3.8 或更高版本
- [uv](https://github.com/astral-sh/uv) - 现代化Python包管理器（推荐）

### 安装 uv

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**或使用 pip:**
```bash
pip install uv
```

### 快速启动

#### 方法1: 使用启动脚本（最简单）

**Linux/macOS:**
```bash
chmod +x run.sh
./run.sh
```

**Windows:**
```cmd
run.bat
```

启动脚本会自动创建虚拟环境、安装依赖并启动服务器。

#### 方法2: 使用 Makefile（Linux/macOS）

```bash
make install  # 安装依赖
make run      # 启动服务器
```

#### 方法3: 手动安装

```bash
# 1. 克隆项目
git clone <repository-url>
cd BS_model

# 2. 创建虚拟环境
uv venv

# 3. 激活虚拟环境
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# 4. 安装依赖
uv pip install -e .

# 5. 运行应用
python app.py
```

#### 传统方式（使用 pip）

```bash
pip install -r requirements.txt
python app.py
```

### 访问应用
启动后，打开浏览器访问: **http://localhost:5000**

### 命令行选项

```bash
python app.py --help              # 查看帮助
python app.py --port 8080         # 指定端口
python app.py --host 127.0.0.1    # 指定主机
python app.py --debug             # 调试模式
```

### 运行示例

```bash
make examples      # 使用 Makefile
# 或
uv run python examples.py
```

## 使用指南

### 基本使用

1. **输入参数**
   - 标的资产价格 (S): 当前股票价格
   - 执行价格 (K): 期权行权价格
   - 到期时间 (T): 距离到期的时间（年）
   - 无风险利率 (r): 年化无风险利率（%）
   - 波动率 (σ): 年化波动率（%）
   - 期权类型: 看涨或看跌

2. **查看结果**
   - 点击"计算"按钮或修改参数自动计算
   - 在"看涨期权"和"看跌期权"标签间切换查看结果
   - 查看期权价格和所有Greeks指标

3. **分析图表**
   - 期权收益图：了解期权价格随标的价格的变化
   - Greeks曲面图：观察Greeks在不同价格和时间下的表现

### 示例场景

#### 场景1：平值期权定价
```
标的价格: $100
执行价格: $100
到期时间: 1年
无风险利率: 5%
波动率: 20%
```

#### 场景2：实值看涨期权
```
标的价格: $110
执行价格: $100
到期时间: 0.5年
无风险利率: 5%
波动率: 25%
```

#### 场景3：虚值看跌期权
```
标的价格: $105
执行价格: $100
到期时间: 0.25年
无风险利率: 5%
波动率: 30%
```

## Black-Scholes模型详解

### 基本公式

**看涨期权定价公式:**
```
C = S₀N(d₁) - Ke⁻ʳᵀN(d₂)
```

**看跌期权定价公式:**
```
P = Ke⁻ʳᵀN(-d₂) - S₀N(-d₁)
```

**其中:**
```
d₁ = [ln(S/K) + (r + σ²/2)T] / (σ√T)
d₂ = d₁ - σ√T
```

### 参数说明

- **S**: 标的资产当前价格
- **K**: 期权执行价格（行权价）
- **T**: 到期时间（年）
- **r**: 无风险利率（连续复利）
- **σ**: 波动率（标准差）
- **N(x)**: 标准正态分布的累积分布函数

### Greeks公式

**Delta:**
```
Call Delta = N(d₁)
Put Delta = N(d₁) - 1
```

**Gamma:**
```
Γ = N'(d₁) / (S σ √T)
```

**Theta:**
```
Call Θ = -[S N'(d₁) σ / (2√T)] - rKe⁻ʳᵀN(d₂)
Put Θ = -[S N'(d₁) σ / (2√T)] + rKe⁻ʳᵀN(-d₂)
```

**Vega:**
```
ν = S N'(d₁) √T
```

**Rho:**
```
Call ρ = KTe⁻ʳᵀN(d₂)
Put ρ = -KTe⁻ʳᵀN(-d₂)
```

### 模型假设

1. **欧式期权**: 只能在到期日行权
2. **无摩擦市场**: 无交易成本、税收
3. **连续交易**: 市场随时可交易
4. **恒定参数**: 波动率和利率不变
5. **对数正态分布**: 标的资产价格服从几何布朗运动
6. **无股息**: 标的资产在期权有效期内不支付股息
7. **无套利**: 市场不存在套利机会

## API接口文档

### POST /api/calculate
计算期权价格和Greeks

**请求体:**
```json
{
  "S": 100,
  "K": 100,
  "T": 1.0,
  "r": 0.05,
  "sigma": 0.2,
  "option_type": "call"
}
```

**响应:**
```json
{
  "call": {
    "price": 10.4506,
    "delta": 0.6368,
    "gamma": 0.0188,
    "theta": -0.0123,
    "vega": 0.3752,
    "rho": 0.5318,
    "intrinsic_value": 0,
    "time_value": 10.4506
  },
  "put": { ... }
}
```

### POST /api/payoff
生成期权收益图数据

**请求体:**
```json
{
  "K": 100,
  "T": 1.0,
  "r": 0.05,
  "sigma": 0.2,
  "option_type": "call"
}
```

**响应:**
```json
{
  "spot_prices": [50, 51, ..., 150],
  "option_prices": [0.0001, 0.0002, ..., 50.45],
  "intrinsic_values": [0, 0, ..., 50],
  "time_values": [0.0001, 0.0002, ..., 0.45]
}
```

### POST /api/greeks_surface
生成Greeks曲面数据

**请求体:**
```json
{
  "K": 100,
  "r": 0.05,
  "sigma": 0.2,
  "option_type": "call",
  "greek": "delta"
}
```

### POST /api/implied_volatility
计算隐含波动率

**请求体:**
```json
{
  "market_price": 10.45,
  "S": 100,
  "K": 100,
  "T": 1.0,
  "r": 0.05,
  "option_type": "call"
}
```

## 为什么使用 uv？

本项目使用 [uv](https://github.com/astral-sh/uv) 作为包管理器，相比传统的 pip 有显著优势：

- **极速安装**: 使用 Rust 编写，依赖安装速度比 pip 快 10-100 倍
- **智能依赖解析**: 更可靠的依赖冲突解决
- **磁盘空间优化**: 全局缓存机制，避免重复下载
- **现代化设计**: 支持 pyproject.toml，遵循 Python 最新标准
- **一致性**: 确保团队成员使用相同的依赖版本

## 项目结构

```
BS_model/
├── app.py                  # Flask应用主文件
├── black_scholes.py        # Black-Scholes模型核心算法
├── examples.py             # 完整使用示例
├── pyproject.toml          # 项目配置（uv/pip）
├── requirements.txt        # Python依赖（备用）
├── run.sh                  # Unix/Linux/macOS 启动脚本
├── run.bat                 # Windows 启动脚本
├── Makefile                # 开发命令（Linux/macOS）
├── QUICKSTART.md           # 快速开始指南
├── README.md               # 项目文档
├── .gitignore              # Git忽略文件
├── templates/              # HTML模板
│   └── index.html          # 主页面
└── static/                 # 静态资源
    ├── css/
    │   └── style.css       # 样式文件
    └── js/
        └── app.js          # JavaScript逻辑
```

## 使用Python模块

除了Web界面，你也可以直接使用Python模块：

```python
from black_scholes import BlackScholesModel

# 创建模型实例
bs = BlackScholesModel(
    S=100,      # 标的价格
    K=100,      # 执行价格
    T=1.0,      # 到期时间
    r=0.05,     # 无风险利率
    sigma=0.2,  # 波动率
    option_type='call'
)

# 计算期权价格
price = bs.price()
print(f"期权价格: ${price:.4f}")

# 计算Greeks
print(f"Delta: {bs.delta():.4f}")
print(f"Gamma: {bs.gamma():.4f}")
print(f"Theta: {bs.theta():.4f}")
print(f"Vega: {bs.vega():.4f}")
print(f"Rho: {bs.rho():.4f}")

# 获取所有Greeks
greeks = bs.all_greeks()
print(greeks)
```

## 学习资源

### 推荐阅读
1. **Options, Futures, and Other Derivatives** - John C. Hull
2. **The Concepts and Practice of Mathematical Finance** - Mark Joshi
3. **Paul Wilmott on Quantitative Finance** - Paul Wilmott

### 在线资源
- [Investopedia - Black-Scholes Model](https://www.investopedia.com/terms/b/blackscholes.asp)
- [QuantLib - Quantitative Finance Library](https://www.quantlib.org/)
- [Options Greeks Explained](https://www.optionsplaybook.com/options-introduction/option-greeks/)

## 局限性与注意事项

### 模型局限性
1. **现实市场偏差**: 实际市场不满足所有假设
2. **波动率微笑**: 实际隐含波动率呈微笑曲线
3. **跳跃风险**: 模型未考虑价格跳跃
4. **股息影响**: 基础版本不考虑股息

### 使用建议
- 本工具主要用于教育和学习目的
- 实际交易应考虑更多市场因素
- 建议结合其他风险管理工具使用
- 参数选择应基于市场数据

## 贡献指南

欢迎提交Issue和Pull Request来改进项目！

### 开发建议
- 遵循PEP 8代码规范
- 添加适当的注释和文档
- 编写单元测试
- 更新README文档

## 许可证

MIT License

## 联系方式

如有问题或建议，请通过GitHub Issues联系。

## 更新日志

### v1.1.0 (2025-11-14)
- 🚀 迁移到 uv 包管理器，提升安装速度
- 📦 添加 pyproject.toml 标准化配置
- 🛠️ 新增启动脚本 (run.sh, run.bat)
- 📝 添加快速开始指南 (QUICKSTART.md)
- 🔧 添加 Makefile 便捷开发命令
- ⚡ 优化依赖管理和项目结构

### v1.0.0 (2025-11-13)
- 初始版本发布
- 实现完整的Black-Scholes模型
- 添加交互式Web界面
- 支持所有Greeks计算
- 提供多种可视化图表

---

**注意**: 本项目仅供教育和学习使用，不构成任何投资建议。期权交易存在重大风险，请谨慎决策。
