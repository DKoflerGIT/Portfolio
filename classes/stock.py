from typing import Optional
#from pydantic import BaseModel
from functions import helpers as hlp

class Stock():
    def __init__(self, ticker, data, buyPrice, buyAmount, buyFeeEur):           
        self.ticker = ticker
        self.data = data
        self.buyPrice = buyPrice
        self.buyAmount = buyAmount
        self.buyFeeEur = buyFeeEur
        self.buyFeeUsd = hlp.eurToUsd(buyFeeEur)

    # calculation methods
    def getValue(self):
        return round(self.data['Close'][-1], 2)

    def calcValueChange(self):
        return round(self.data['Close'][-1] - self.data['Close'][-2], 2)

    def calcValueChangePercent(self):
        return round(100 / self.data['Close'][-2] * (self.data['Close'][-1] - self.data['Close'][-2]), 2)
    
    def calcProfit(self):
        return round(self.data['Close'][-1] - self.buyPrice, 2)

    def calcProfitPercent(self):
        return round(100 / self.buyPrice * self.data['Close'][-1] - 100, 2)