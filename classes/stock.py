import yfinance as yf
from helpers import helpers as hlp

class stock:
    def __init__(self, ticker, buy_price, num_stocks, buy_fees_eur):
        self.ticker = yf.Ticker(ticker)

        try:
            self.i =  self.ticker.info
        except:
            raise ValueError("Invalid ticker!")
            
        self.name = ticker
        self.buy_price = buy_price
        self.num_stocks = num_stocks
        self.buy_fees_eur = buy_fees_eur
        self.buy_fees_usd = round(buy_fees_eur * hlp.eurusd(), 2)

        self.history = None
        self.info = None
        self.actions = None
        self.dividends = None
        self.splits = None
        self.financials = None
        self.balance_sheet = None
        self.cash_flow = None
        self.earnings = None
    
    #get information methods
    def get_history(self, p = "5y", i = "1d"):
        self.history = self.ticker.history(period = p, interval = i)

    def get_info(self):
        self.info = self.ticker.info

    def get_actions(self):
        self.actions = self.ticker.actions

    def get_dividends(self):    
        self.dividends = self.ticker.dividends

    def get_splits(self):    
        self.splits = self.ticker.splits

    def get_financials(self):    
        self.financials = self.ticker.financials
    
    def get_balance_sheet(self):
        self.balance_sheet =  self.ticker.balance_sheet
    
    def get_cash_flow(self):
        self.cash_flow = self.ticker.cashflow
    
    def get_earnings(self):
        self.earnings = self.ticker.earnings

    # calculation methods
    def get_currentValue(self):
        return round(self.history.Close[-1] if self.history.Close[-1] is not None else 0, 2)

    def calc_valueChange(self):
        prev_close = hlp.validate(self.history.Close[-2])
        last_close = hlp.validate(self.history.Close[-1])
        return round(100 / prev_close * (last_close - prev_close), 2)
    
    def calc_profit(self):
        return round(hlp.validate(self.history.Close[-1]) - self.buy_price, 2)

    def calc_profitChange(self):
        return round(100 / self.buy_price * hlp.validate(self.history.Close[-1]) - 100, 2)