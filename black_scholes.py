"""
Black-Scholes期权定价模型
用于计算欧式期权的理论价格和Greeks
"""

import numpy as np
from scipy.stats import norm
import math


class BlackScholesModel:
    """Black-Scholes期权定价模型"""

    def __init__(self, S, K, T, r, sigma, option_type='call'):
        """
        初始化Black-Scholes模型参数

        参数:
            S (float): 标的资产当前价格
            K (float): 期权执行价格
            T (float): 到期时间（年）
            r (float): 无风险利率（年化）
            sigma (float): 波动率（年化）
            option_type (str): 期权类型 'call' 或 'put'
        """
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.option_type = option_type.lower()

    def _d1(self):
        """计算d1参数"""
        return (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))

    def _d2(self):
        """计算d2参数"""
        return self._d1() - self.sigma * np.sqrt(self.T)

    def price(self):
        """
        计算期权价格

        返回:
            float: 期权理论价格
        """
        if self.T <= 0:
            # 到期时的内在价值
            if self.option_type == 'call':
                return max(self.S - self.K, 0)
            else:
                return max(self.K - self.S, 0)

        d1 = self._d1()
        d2 = self._d2()

        if self.option_type == 'call':
            price = self.S * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        else:  # put
            price = self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1)

        return price

    def delta(self):
        """
        计算Delta: 期权价格对标的资产价格的一阶导数
        表示标的资产价格变动1单位时，期权价格的变动

        返回:
            float: Delta值
        """
        if self.T <= 0:
            if self.option_type == 'call':
                return 1.0 if self.S > self.K else 0.0
            else:
                return -1.0 if self.S < self.K else 0.0

        d1 = self._d1()

        if self.option_type == 'call':
            return norm.cdf(d1)
        else:  # put
            return norm.cdf(d1) - 1

    def gamma(self):
        """
        计算Gamma: Delta对标的资产价格的一阶导数
        表示Delta的变化率

        返回:
            float: Gamma值
        """
        if self.T <= 0:
            return 0.0

        d1 = self._d1()
        return norm.pdf(d1) / (self.S * self.sigma * np.sqrt(self.T))

    def theta(self):
        """
        计算Theta: 期权价格对时间的导数
        表示时间流逝1天时，期权价格的变动（通常为负值）

        返回:
            float: Theta值（日度）
        """
        if self.T <= 0:
            return 0.0

        d1 = self._d1()
        d2 = self._d2()

        if self.option_type == 'call':
            theta = (-self.S * norm.pdf(d1) * self.sigma / (2 * np.sqrt(self.T))
                    - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2))
        else:  # put
            theta = (-self.S * norm.pdf(d1) * self.sigma / (2 * np.sqrt(self.T))
                    + self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2))

        # 转换为日度Theta（除以365）
        return theta / 365

    def vega(self):
        """
        计算Vega: 期权价格对波动率的导数
        表示波动率变动1%时，期权价格的变动

        返回:
            float: Vega值
        """
        if self.T <= 0:
            return 0.0

        d1 = self._d1()
        return self.S * norm.pdf(d1) * np.sqrt(self.T) / 100

    def rho(self):
        """
        计算Rho: 期权价格对无风险利率的导数
        表示利率变动1%时，期权价格的变动

        返回:
            float: Rho值
        """
        if self.T <= 0:
            return 0.0

        d2 = self._d2()

        if self.option_type == 'call':
            return self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(d2) / 100
        else:  # put
            return -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-d2) / 100

    def all_greeks(self):
        """
        计算所有Greeks

        返回:
            dict: 包含所有Greeks的字典
        """
        return {
            'price': self.price(),
            'delta': self.delta(),
            'gamma': self.gamma(),
            'theta': self.theta(),
            'vega': self.vega(),
            'rho': self.rho()
        }

    def intrinsic_value(self):
        """
        计算期权内在价值

        返回:
            float: 内在价值
        """
        if self.option_type == 'call':
            return max(self.S - self.K, 0)
        else:
            return max(self.K - self.S, 0)

    def time_value(self):
        """
        计算期权时间价值

        返回:
            float: 时间价值
        """
        return self.price() - self.intrinsic_value()


def calculate_implied_volatility(market_price, S, K, T, r, option_type='call',
                                 max_iterations=100, precision=1e-5):
    """
    使用牛顿迭代法计算隐含波动率

    参数:
        market_price (float): 市场期权价格
        S (float): 标的资产价格
        K (float): 执行价格
        T (float): 到期时间
        r (float): 无风险利率
        option_type (str): 期权类型
        max_iterations (int): 最大迭代次数
        precision (float): 精度要求

    返回:
        float: 隐含波动率，如果无法收敛则返回None
    """
    # 初始猜测值
    sigma = 0.5

    for i in range(max_iterations):
        bs = BlackScholesModel(S, K, T, r, sigma, option_type)
        price = bs.price()
        vega = bs.vega() * 100  # 转换回百分比形式

        diff = market_price - price

        if abs(diff) < precision:
            return sigma

        if vega == 0:
            return None

        sigma = sigma + diff / vega

        # 确保波动率在合理范围内
        if sigma <= 0 or sigma > 5:
            return None

    return None


if __name__ == "__main__":
    # 示例使用
    print("Black-Scholes期权定价模型示例")
    print("=" * 50)

    # 参数设置
    S = 100  # 标的资产价格
    K = 100  # 执行价格
    T = 1.0  # 1年到期
    r = 0.05  # 5%无风险利率
    sigma = 0.2  # 20%波动率

    # 计算看涨期权
    call = BlackScholesModel(S, K, T, r, sigma, 'call')
    print(f"\n看涨期权 (Call Option):")
    print(f"标的价格: ${S}")
    print(f"执行价格: ${K}")
    print(f"到期时间: {T}年")
    print(f"无风险利率: {r*100}%")
    print(f"波动率: {sigma*100}%")
    print(f"\n期权价格: ${call.price():.4f}")
    print(f"Delta: {call.delta():.4f}")
    print(f"Gamma: {call.gamma():.4f}")
    print(f"Theta: ${call.theta():.4f}/日")
    print(f"Vega: ${call.vega():.4f}")
    print(f"Rho: ${call.rho():.4f}")

    # 计算看跌期权
    put = BlackScholesModel(S, K, T, r, sigma, 'put')
    print(f"\n看跌期权 (Put Option):")
    print(f"期权价格: ${put.price():.4f}")
    print(f"Delta: {put.delta():.4f}")
    print(f"Gamma: {put.gamma():.4f}")
    print(f"Theta: ${put.theta():.4f}/日")
    print(f"Vega: ${put.vega():.4f}")
    print(f"Rho: ${put.rho():.4f}")
