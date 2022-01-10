from functions import helpers as hlp
import yfinance as yf

class Stock():
    def __init__(self, ticker, data = None, buyPrice = 0, buyAmount = 0, buyFeeEur = 0):           
        self.ticker = ticker
        
        self.buyPrice = 0 if buyPrice == 0 or buyAmount == 0 or buyFeeEur == 0 else buyPrice
        self.buyAmount = 0 if buyPrice == 0 or buyAmount == 0 or buyFeeEur == 0 else buyAmount
        self.buyFeeEur = 0 if buyPrice == 0 or buyAmount == 0 or buyFeeEur == 0 else buyFeeEur
        self.buyFeeUsd = hlp.eurToUsd(buyFeeEur)

        self.data = data

        # yfStock = yf.Ticker("ticker")
        # self.name = yfStock.info["shortName"]

        # if data == None:
        #     self.data = yfStock.history(period="5y")
        # else:
        #     self.data = data

        # self.value = yfStock.info["previousClose"]
        # self.pe = yfStock.info["forwardPE"]
        # self.dividendYield = yfStock.info["dividendYield"] * 100

    # calculation methods
    def getValue(self):
        # yfStock = yf.Ticker(self.ticker)
        # d = yfStock.history(period='1d')
        # return round(d.Close[-1], 2)
        return round(self.data.Close[-1], 2)

    def calcValue1dChange(self):
        # yfStock = yf.Ticker(self.ticker)
        # d = yfStock.history(period='5d')
        # return round(d.Close[-1] - d.Close[-2], 2)
        return round(self.data.Close[-1] - self.data.Close[-2], 2)

    def calcValueChange1dPercent(self):
        # yfStock = yf.Ticker(self.ticker)
        # d = yfStock.history(period='5d')
        # return round(100 / d.Close[-2] * (d.Close[-1] - d.Close[-2]), 2)
        return round(100 / self.data.Close[-2] * (self.data.Close[-1] - self.data.Close[-2]), 2)
    
    def calcProfit(self):
        if self.buyPrice == 0:
            return 0
        return round(self.data['Close'][-1] - self.buyPrice, 2)

    def calcProfitPercent(self):
        if self.buyPrice == 0:
            return 0
        # yfStock = yf.Ticker(self.ticker)
        # d = yfStock.history(period='1d')
        # return round(100 / self.buyPrice * d.Close[-1] - 100, 2)
        return round(100 / self.buyPrice * self.data.Close[-1] - 100, 2)