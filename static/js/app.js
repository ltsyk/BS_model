// Black-Scholes可视化应用主脚本

// 全局变量
let currentData = null;

// DOM元素
const calculateBtn = document.getElementById('calculateBtn');
const tabBtns = document.querySelectorAll('.tab-btn');
const chartTabBtns = document.querySelectorAll('.chart-tab-btn');

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    // 绑定事件
    calculateBtn.addEventListener('click', calculate);

    // 标签切换
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            switchTab(this.dataset.tab);
        });
    });

    chartTabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            switchChartTab(this.dataset.chart);
        });
    });

    // 输入变化时自动计算
    const inputs = document.querySelectorAll('.input-group input, .input-group select');
    inputs.forEach(input => {
        input.addEventListener('change', calculate);
    });

    // 初始计算
    calculate();
});

// 切换结果标签
function switchTab(tab) {
    tabBtns.forEach(btn => btn.classList.remove('active'));
    document.querySelector(`[data-tab="${tab}"]`).classList.add('active');

    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tab}Results`).classList.add('active');
}

// 切换图表标签
function switchChartTab(chart) {
    chartTabBtns.forEach(btn => btn.classList.remove('active'));
    document.querySelector(`[data-chart="${chart}"]`).classList.add('active');

    document.querySelectorAll('.chart-container').forEach(container => {
        container.classList.remove('active');
    });
    document.getElementById(`${chart}Chart`).classList.add('active');

    // 加载对应图表
    if (chart === 'payoff') {
        loadPayoffChart();
    } else {
        loadGreeksSurface(chart);
    }
}

// 获取输入参数
function getParameters() {
    return {
        S: parseFloat(document.getElementById('spotPrice').value),
        K: parseFloat(document.getElementById('strikePrice').value),
        T: parseFloat(document.getElementById('timeToMaturity').value),
        r: parseFloat(document.getElementById('riskFreeRate').value) / 100,
        sigma: parseFloat(document.getElementById('volatility').value) / 100,
        option_type: document.getElementById('optionType').value
    };
}

// 计算期权价格和Greeks
async function calculate() {
    try {
        const params = getParameters();

        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });

        if (!response.ok) {
            throw new Error('计算失败');
        }

        const data = await response.json();
        currentData = data;

        // 更新显示
        updateResults(data);

        // 更新图表
        loadPayoffChart();

    } catch (error) {
        console.error('错误:', error);
        alert('计算出错，请检查输入参数');
    }
}

// 更新结果显示
function updateResults(data) {
    // 看涨期权
    document.getElementById('callPrice').textContent = `$${data.call.price.toFixed(4)}`;
    document.getElementById('callDelta').textContent = data.call.delta.toFixed(4);
    document.getElementById('callGamma').textContent = data.call.gamma.toFixed(4);
    document.getElementById('callTheta').textContent = `$${data.call.theta.toFixed(4)}`;
    document.getElementById('callVega').textContent = `$${data.call.vega.toFixed(4)}`;
    document.getElementById('callRho').textContent = `$${data.call.rho.toFixed(4)}`;
    document.getElementById('callIntrinsic').textContent = `$${data.call.intrinsic_value.toFixed(4)}`;
    document.getElementById('callTime').textContent = `$${data.call.time_value.toFixed(4)}`;

    // 看跌期权
    document.getElementById('putPrice').textContent = `$${data.put.price.toFixed(4)}`;
    document.getElementById('putDelta').textContent = data.put.delta.toFixed(4);
    document.getElementById('putGamma').textContent = data.put.gamma.toFixed(4);
    document.getElementById('putTheta').textContent = `$${data.put.theta.toFixed(4)}`;
    document.getElementById('putVega').textContent = `$${data.put.vega.toFixed(4)}`;
    document.getElementById('putRho').textContent = `$${data.put.rho.toFixed(4)}`;
    document.getElementById('putIntrinsic').textContent = `$${data.put.intrinsic_value.toFixed(4)}`;
    document.getElementById('putTime').textContent = `$${data.put.time_value.toFixed(4)}`;
}

// 加载期权收益图
async function loadPayoffChart() {
    try {
        const params = getParameters();

        const response = await fetch('/api/payoff', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });

        if (!response.ok) {
            throw new Error('加载图表失败');
        }

        const data = await response.json();

        const trace1 = {
            x: data.spot_prices,
            y: data.option_prices,
            type: 'scatter',
            mode: 'lines',
            name: '期权价格',
            line: {
                color: '#667eea',
                width: 3
            }
        };

        const trace2 = {
            x: data.spot_prices,
            y: data.intrinsic_values,
            type: 'scatter',
            mode: 'lines',
            name: '内在价值',
            line: {
                color: '#f56565',
                width: 2,
                dash: 'dash'
            }
        };

        const trace3 = {
            x: data.spot_prices,
            y: data.time_values,
            type: 'scatter',
            mode: 'lines',
            name: '时间价值',
            line: {
                color: '#48bb78',
                width: 2,
                dash: 'dot'
            }
        };

        const layout = {
            title: {
                text: `${params.option_type === 'call' ? '看涨' : '看跌'}期权价格随标的价格变化`,
                font: { size: 18 }
            },
            xaxis: {
                title: '标的资产价格 ($)',
                gridcolor: '#e0e0e0'
            },
            yaxis: {
                title: '期权价格 ($)',
                gridcolor: '#e0e0e0'
            },
            hovermode: 'x unified',
            plot_bgcolor: '#fafafa',
            paper_bgcolor: 'white',
            showlegend: true,
            legend: {
                x: 0.02,
                y: 0.98,
                bgcolor: 'rgba(255,255,255,0.8)'
            }
        };

        Plotly.newPlot('payoffChart', [trace1, trace2, trace3], layout, {responsive: true});

    } catch (error) {
        console.error('错误:', error);
    }
}

// 加载Greeks曲面图
async function loadGreeksSurface(greek) {
    try {
        const params = getParameters();
        params.greek = greek;

        const response = await fetch('/api/greeks_surface', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });

        if (!response.ok) {
            throw new Error('加载图表失败');
        }

        const data = await response.json();

        const trace = {
            x: data.spot_prices,
            y: data.times,
            z: data.values,
            type: 'surface',
            colorscale: 'Viridis',
            contours: {
                z: {
                    show: true,
                    usecolormap: true,
                    highlightcolor: "#42f462",
                    project: { z: true }
                }
            }
        };

        const greekNames = {
            'delta': 'Delta (Δ)',
            'gamma': 'Gamma (Γ)',
            'theta': 'Theta (Θ)',
            'vega': 'Vega (ν)',
            'rho': 'Rho (ρ)'
        };

        const layout = {
            title: {
                text: `${greekNames[greek]}曲面 - ${params.option_type === 'call' ? '看涨期权' : '看跌期权'}`,
                font: { size: 18 }
            },
            scene: {
                xaxis: {
                    title: '标的资产价格 ($)',
                    gridcolor: '#e0e0e0'
                },
                yaxis: {
                    title: '到期时间 (年)',
                    gridcolor: '#e0e0e0'
                },
                zaxis: {
                    title: greekNames[greek],
                    gridcolor: '#e0e0e0'
                },
                camera: {
                    eye: { x: 1.5, y: 1.5, z: 1.3 }
                }
            },
            paper_bgcolor: 'white',
            plot_bgcolor: '#fafafa'
        };

        Plotly.newPlot(`${greek}Chart`, [trace], layout, {responsive: true});

    } catch (error) {
        console.error('错误:', error);
    }
}

// 格式化数字
function formatNumber(num, decimals = 4) {
    return num.toFixed(decimals);
}

// 格式化货币
function formatCurrency(num, decimals = 2) {
    return `$${num.toFixed(decimals)}`;
}

// 格式化百分比
function formatPercent(num, decimals = 2) {
    return `${(num * 100).toFixed(decimals)}%`;
}
