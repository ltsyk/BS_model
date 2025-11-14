"""
Flask Web应用 - Black-Scholes可视化服务
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import numpy as np
from black_scholes import BlackScholesModel, calculate_implied_volatility

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/calculate', methods=['POST'])
def calculate():
    """
    计算期权价格和Greeks
    """
    try:
        data = request.json
        S = float(data.get('S', 100))
        K = float(data.get('K', 100))
        T = float(data.get('T', 1.0))
        r = float(data.get('r', 0.05))
        sigma = float(data.get('sigma', 0.2))
        option_type = data.get('option_type', 'call')

        # 验证输入
        if S <= 0 or K <= 0 or T < 0 or sigma <= 0:
            return jsonify({'error': '参数必须为正数'}), 400

        # 计算看涨期权
        call = BlackScholesModel(S, K, T, r, sigma, 'call')
        call_greeks = call.all_greeks()

        # 计算看跌期权
        put = BlackScholesModel(S, K, T, r, sigma, 'put')
        put_greeks = put.all_greeks()

        result = {
            'call': {
                'price': call_greeks['price'],
                'delta': call_greeks['delta'],
                'gamma': call_greeks['gamma'],
                'theta': call_greeks['theta'],
                'vega': call_greeks['vega'],
                'rho': call_greeks['rho'],
                'intrinsic_value': call.intrinsic_value(),
                'time_value': call.time_value()
            },
            'put': {
                'price': put_greeks['price'],
                'delta': put_greeks['delta'],
                'gamma': put_greeks['gamma'],
                'theta': put_greeks['theta'],
                'vega': put_greeks['vega'],
                'rho': put_greeks['rho'],
                'intrinsic_value': put.intrinsic_value(),
                'time_value': put.time_value()
            }
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/payoff', methods=['POST'])
def payoff():
    """
    计算期权收益图数据
    """
    try:
        data = request.json
        K = float(data.get('K', 100))
        T = float(data.get('T', 1.0))
        r = float(data.get('r', 0.05))
        sigma = float(data.get('sigma', 0.2))
        option_type = data.get('option_type', 'call')

        # 生成价格范围
        S_range = np.linspace(K * 0.5, K * 1.5, 100)

        prices = []
        intrinsic_values = []
        time_values = []

        for S in S_range:
            bs = BlackScholesModel(S, K, T, r, sigma, option_type)
            prices.append(bs.price())
            intrinsic_values.append(bs.intrinsic_value())
            time_values.append(bs.time_value())

        result = {
            'spot_prices': S_range.tolist(),
            'option_prices': prices,
            'intrinsic_values': intrinsic_values,
            'time_values': time_values
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/greeks_surface', methods=['POST'])
def greeks_surface():
    """
    计算Greeks随价格和时间变化的数据
    """
    try:
        data = request.json
        K = float(data.get('K', 100))
        r = float(data.get('r', 0.05))
        sigma = float(data.get('sigma', 0.2))
        option_type = data.get('option_type', 'call')
        greek = data.get('greek', 'delta')

        # 生成价格和时间范围
        S_range = np.linspace(K * 0.7, K * 1.3, 30)
        T_range = np.linspace(0.1, 2.0, 30)

        values = []

        for T in T_range:
            row = []
            for S in S_range:
                bs = BlackScholesModel(S, K, T, r, sigma, option_type)
                if greek == 'delta':
                    row.append(bs.delta())
                elif greek == 'gamma':
                    row.append(bs.gamma())
                elif greek == 'theta':
                    row.append(bs.theta())
                elif greek == 'vega':
                    row.append(bs.vega())
                elif greek == 'rho':
                    row.append(bs.rho())
                else:
                    row.append(bs.price())
            values.append(row)

        result = {
            'spot_prices': S_range.tolist(),
            'times': T_range.tolist(),
            'values': values
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/implied_volatility', methods=['POST'])
def implied_vol():
    """
    计算隐含波动率
    """
    try:
        data = request.json
        market_price = float(data.get('market_price'))
        S = float(data.get('S', 100))
        K = float(data.get('K', 100))
        T = float(data.get('T', 1.0))
        r = float(data.get('r', 0.05))
        option_type = data.get('option_type', 'call')

        iv = calculate_implied_volatility(market_price, S, K, T, r, option_type)

        if iv is None:
            return jsonify({'error': '无法计算隐含波动率'}), 400

        result = {
            'implied_volatility': iv,
            'implied_volatility_percent': iv * 100
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def main():
    """启动Flask应用服务器"""
    import argparse

    parser = argparse.ArgumentParser(description='Black-Scholes期权定价可视化服务器')
    parser.add_argument('--host', default='0.0.0.0', help='服务器主机地址 (默认: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, help='服务器端口 (默认: 5000)')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')

    args = parser.parse_args()

    print(f"\n{'='*60}")
    print("Black-Scholes期权定价模型可视化平台")
    print(f"{'='*60}")
    print(f"服务器运行在: http://{args.host}:{args.port}")
    print(f"调试模式: {'开启' if args.debug else '关闭'}")
    print(f"{'='*60}\n")

    app.run(debug=args.debug, host=args.host, port=args.port)


if __name__ == '__main__':
    main()
