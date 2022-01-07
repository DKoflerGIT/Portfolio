import yfinance as yf
from helpers import helpers as hlp

class stock:
    def __init__(self, ticker, data, buy_price, num_stocks, buy_fees_eur):           
        self.ticker = ticker
        self.data = data
        self.buy_price = buy_price
        self.num_stocks = num_stocks
        self.buy_fees_eur = buy_fees_eur
        self.buy_fees_usd = round(buy_fees_eur * hlp.eurusd(), 2)

    # calculation methods
    def get_value(self):
        return round(self.data['Close'][-1], 2)

    def calc_valueChange(self):
        return round(self.data['Close'][-1] - self.data['Close'][-2], 2)

    def calc_valueChangePercent(self):
        return round(100 / self.data['Close'][-2] * (self.data['Close'][-1] - self.data['Close'][-2]), 2)
    
    def calc_profit(self):
        return round(self.data['Close'][-1] - self.buy_price, 2)

    def calc_profitPercent(self):
        return round(100 / self.buy_price * self.data['Close'][-1] - 100, 2)