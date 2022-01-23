from functions import helpers as hlp
from datetime import date, datetime
import yfinance as yf

class Stock():
    def __init__(self, ticker, data = None, buyDate = None, buyAmount = 0, buyFeeEur = 0):           
        self.ticker = ticker
        self.data = data

        if buyAmount == 0 or buyFeeEur == 0:
            self.buyDate = None
            self.buyPrice = 0
            self.buyAmount = 0
            self.buyFeeEur = 0
            self.buyFeeUsd = 0
        else:
            self.buyDate = buyDate
            self.buyPrice = round(data['Close'][str(buyDate)], 2)
            self.buyAmount = buyAmount
            self.buyFeeEur = buyFeeEur
            self.buyFeeUsd = hlp.eurToUsd(buyFeeEur)

    # calculation methods
    def getValue(self):
        return round(self.data.Close[-1], 2)

    def calcValue1dChange(self):
        return round(self.data.Close[-1] - self.data.Close[-2], 2)

    def calcValueChange1dPercent(self):
        return round(100 / self.data.Close[-2] * (self.data.Close[-1] - self.data.Close[-2]), 2)
    
    def calcProfit(self):
        if self.buyDate == None:
            return 0
        return round(self.data['Close'][-1] - self.data[''], 2)

    def calcProfitPercent(self):
        if self.buyPrice == 0:
            return 0
        return round(100 / self.buyPrice * self.data.Close[-1] - 100, 2)
    
    def calcProfit(self):
        if self.buyPrice == 0:
            return 0
        return round(self.data.Close[-1] * self.buyAmount - self.buyPrice * self.buyAmount, 2)