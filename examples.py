"""
Black-Scholes模型使用示例
演示各种期权定价和Greeks计算场景
"""

from black_scholes import BlackScholesModel, calculate_implied_volatility
import numpy as np


def example_basic_pricing():
    """示例1: 基本期权定价"""
    print("\n" + "="*60)
    print("示例1: 基本期权定价")
    print("="*60)

    # 平值期权
    bs_call = BlackScholesModel(S=100, K=100, T=1.0, r=0.05, sigma=0.2, option_type='call')
    bs_put = BlackScholesModel(S=100, K=100, T=1.0, r=0.05, sigma=0.2, option_type='put')

    print(f"\n参数: S=100, K=100, T=1年, r=5%, σ=20%")
    print(f"\n看涨期权价格: ${bs_call.price():.4f}")
    print(f"看跌期权价格: ${bs_put.price():.4f}")

    # 验证看涨看跌平价关系: C - P = S - K*e^(-rT)
    parity_diff = bs_call.price() - bs_put.price()
    expected_diff = 100 - 100 * np.exp(-0.05 * 1.0)
    print(f"\n看涨看跌平价关系验证:")
    print(f"C - P = ${parity_diff:.4f}")
    print(f"S - Ke^(-rT) = ${expected_diff:.4f}")
    print(f"差异: ${abs(parity_diff - expected_diff):.6f}")


def example_itm_otm():
    """示例2: 实值、平值、虚值期权比较"""
    print("\n" + "="*60)
    print("示例2: 实值、平值、虚值期权比较")
    print("="*60)

    K = 100  # 执行价格
    scenarios = [
        ("实值", 110),
        ("平值", 100),
        ("虚值", 90)
    ]

    print("\n看涨期权 (K=100, T=1年, r=5%, σ=20%):")
    print(f"{'类型':<8} {'标的价格':<10} {'期权价格':<12} {'内在价值':<12} {'时间价值':<12} {'Delta':<10}")
    print("-" * 70)

    for name, S in scenarios:
        bs = BlackScholesModel(S=S, K=K, T=1.0, r=0.05, sigma=0.2, option_type='call')
        print(f"{name:<8} ${S:<9} ${bs.price():<11.4f} ${bs.intrinsic_value():<11.4f} "
              f"${bs.time_value():<11.4f} {bs.delta():<10.4f}")


def example_greeks():
    """示例3: Greeks详细分析"""
    print("\n" + "="*60)
    print("示例3: Greeks详细分析")
    print("="*60)

    bs_call = BlackScholesModel(S=100, K=100, T=1.0, r=0.05, sigma=0.2, option_type='call')
    bs_put = BlackScholesModel(S=100, K=100, T=1.0, r=0.05, sigma=0.2, option_type='put')

    print("\n平值期权Greeks (S=100, K=100, T=1年, r=5%, σ=20%):")
    print(f"\n{'Greek':<15} {'看涨期权':<15} {'看跌期权':<15} {'说明'}")
    print("-" * 80)
    print(f"{'Delta':<15} {bs_call.delta():<15.4f} {bs_put.delta():<15.4f} 价格变动$1的影响")
    print(f"{'Gamma':<15} {bs_call.gamma():<15.4f} {bs_put.gamma():<15.4f} Delta的变化率")
    print(f"{'Theta (日)':<15} {bs_call.theta():<15.4f} {bs_put.theta():<15.4f} 每天的时间衰减")
    print(f"{'Vega':<15} {bs_call.vega():<15.4f} {bs_put.vega():<15.4f} 波动率变动1%的影响")
    print(f"{'Rho':<15} {bs_call.rho():<15.4f} {bs_put.rho():<15.4f} 利率变动1%的影响")

    print("\nGreeks解读:")
    print(f"- Call Delta={bs_call.delta():.4f}: 标的价格上涨$1，看涨期权价格上涨约${bs_call.delta():.4f}")
    print(f"- Put Delta={bs_put.delta():.4f}: 标的价格上涨$1，看跌期权价格下跌约${abs(bs_put.delta()):.4f}")
    print(f"- Gamma={bs_call.gamma():.4f}: 标的价格变动$1，Delta变化约{bs_call.gamma():.4f}")
    print(f"- Theta={bs_call.theta():.4f}: 每天损失${abs(bs_call.theta()):.4f}的时间价值")


def example_time_decay():
    """示例4: 时间衰减分析"""
    print("\n" + "="*60)
    print("示例4: 时间衰减分析")
    print("="*60)

    print("\n平值看涨期权时间衰减 (S=100, K=100, r=5%, σ=20%):")
    print(f"{'到期时间':<12} {'期权价格':<12} {'Theta (日)':<12} {'时间价值':<12}")
    print("-" * 50)

    time_periods = [1.0, 0.75, 0.5, 0.25, 0.1, 0.05, 0.01]

    for T in time_periods:
        bs = BlackScholesModel(S=100, K=100, T=T, r=0.05, sigma=0.2, option_type='call')
        print(f"{T:<12.2f} ${bs.price():<11.4f} ${bs.theta():<11.4f} ${bs.time_value():<11.4f}")

    print("\n观察: 时间价值随着到期日临近加速衰减，Theta的绝对值增大")


def example_volatility_impact():
    """示例5: 波动率对期权价格的影响"""
    print("\n" + "="*60)
    print("示例5: 波动率对期权价格的影响")
    print("="*60)

    print("\n平值期权在不同波动率下的价格 (S=100, K=100, T=1年, r=5%):")
    print(f"{'波动率':<12} {'看涨价格':<12} {'看跌价格':<12} {'Vega':<12}")
    print("-" * 50)

    volatilities = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]

    for sigma in volatilities:
        bs_call = BlackScholesModel(S=100, K=100, T=1.0, r=0.05, sigma=sigma, option_type='call')
        bs_put = BlackScholesModel(S=100, K=100, T=1.0, r=0.05, sigma=sigma, option_type='put')
        print(f"{sigma*100:<11.0f}% ${bs_call.price():<11.4f} ${bs_put.price():<11.4f} ${bs_call.vega():<11.4f}")

    print("\n观察: 波动率越高，期权价值越大（买方有利）")


def example_moneyness():
    """示例6: 不同价值状态的Delta分布"""
    print("\n" + "="*60)
    print("示例6: 不同价值状态的Delta分布")
    print("="*60)

    K = 100
    spot_prices = np.linspace(70, 130, 13)

    print("\n看涨期权Delta分布 (K=100, T=0.5年, r=5%, σ=20%):")
    print(f"{'标的价格':<12} {'期权类型':<12} {'期权价格':<12} {'Delta':<12} {'实值程度':<12}")
    print("-" * 70)

    for S in spot_prices:
        bs_call = BlackScholesModel(S=S, K=K, T=0.5, r=0.05, sigma=0.2, option_type='call')
        moneyness = (S - K) / K * 100

        if S < K - 5:
            status = "深度虚值"
        elif S < K:
            status = "虚值"
        elif S == K:
            status = "平值"
        elif S < K + 5:
            status = "实值"
        else:
            status = "深度实值"

        print(f"${S:<11.0f} {status:<12} ${bs_call.price():<11.4f} {bs_call.delta():<12.4f} {moneyness:>5.1f}%")

    print("\n观察: 深度虚值期权Delta接近0，深度实值期权Delta接近1")


def example_implied_volatility():
    """示例7: 隐含波动率计算"""
    print("\n" + "="*60)
    print("示例7: 隐含波动率计算")
    print("="*60)

    # 已知参数
    S, K, T, r = 100, 100, 1.0, 0.05
    true_sigma = 0.25

    # 计算理论价格
    bs = BlackScholesModel(S, K, T, r, true_sigma, 'call')
    market_price = bs.price()

    print(f"\n市场数据:")
    print(f"标的价格: ${S}")
    print(f"执行价格: ${K}")
    print(f"到期时间: {T}年")
    print(f"无风险利率: {r*100}%")
    print(f"期权市场价格: ${market_price:.4f}")

    # 计算隐含波动率
    iv = calculate_implied_volatility(market_price, S, K, T, r, 'call')

    print(f"\n计算结果:")
    print(f"隐含波动率: {iv*100:.2f}%")
    print(f"真实波动率: {true_sigma*100:.2f}%")
    print(f"差异: {abs(iv - true_sigma)*100:.6f}%")

    # 验证
    bs_check = BlackScholesModel(S, K, T, r, iv, 'call')
    print(f"\n验证:")
    print(f"使用隐含波动率计算的价格: ${bs_check.price():.4f}")
    print(f"市场价格: ${market_price:.4f}")


def example_hedging_strategy():
    """示例8: Delta对冲策略"""
    print("\n" + "="*60)
    print("示例8: Delta对冲策略")
    print("="*60)

    # 卖出看涨期权
    bs = BlackScholesModel(S=100, K=100, T=0.5, r=0.05, sigma=0.2, option_type='call')

    print(f"\n初始持仓:")
    print(f"卖出1份看涨期权")
    print(f"期权价格: ${bs.price():.4f}")
    print(f"期权Delta: {bs.delta():.4f}")
    print(f"期权Gamma: {bs.gamma():.4f}")

    # Delta对冲
    hedge_shares = bs.delta()
    print(f"\nDelta对冲策略:")
    print(f"买入{hedge_shares:.4f}股标的资产进行对冲")
    print(f"投资组合Delta: {-bs.delta() + hedge_shares:.6f} (接近0)")

    # 价格变动后
    print(f"\n假设标的价格上涨到$105:")
    bs_new = BlackScholesModel(S=105, K=100, T=0.5, r=0.05, sigma=0.2, option_type='call')

    option_loss = -(bs_new.price() - bs.price())
    stock_gain = hedge_shares * (105 - 100)
    net_pnl = option_loss + stock_gain

    print(f"期权亏损: ${option_loss:.4f}")
    print(f"股票盈利: ${stock_gain:.4f}")
    print(f"净损益: ${net_pnl:.4f}")
    print(f"\n由于Gamma效应，完美对冲需要动态调整持仓")


def run_all_examples():
    """运行所有示例"""
    print("\n" + "="*60)
    print("Black-Scholes期权定价模型 - 完整示例")
    print("="*60)

    example_basic_pricing()
    example_itm_otm()
    example_greeks()
    example_time_decay()
    example_volatility_impact()
    example_moneyness()
    example_implied_volatility()
    example_hedging_strategy()

    print("\n" + "="*60)
    print("所有示例运行完成！")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_all_examples()
