import yfinance as yf
from matplotlib import pyplot as plt
import pandas as pd
from fastapi import FastAPI

from classes import stock as stock

app = FastAPI()
path = "/finances/investing"

# uvicorn main:app --reload

@app.get(path)
def test():
    return "successful"

@app.get(path + "/overview")
def overview():
    stocks_bought = pd.read_excel('data\stocks_bought.xlsx')

    stocks = []
    for i, t in enumerate(list(stocks_bought.ticker)):
        t = stocks_bought.ticker[i]
        bp = stocks_bought.buy_price[i]
        ns = stocks_bought.num_stocks[i]
        bf = stocks_bought.buy_fees_eur[i]

        s = stock.stock(t, bp, ns, bf)
        stocks.append(s)

        p = []
        for s in stocks:
            s.get_history("5d", "1d")
            p.append(s.calc_profitChange())
        
    return "    ".join(s.name + " " + str(p[i]) + " %" for i, s in enumerate(stocks))

@app.get(path + "/stock/{ticker}")
def stockOverview(ticker: str):
    s = stock.stock(ticker, 0, 0, 0)
    try:
        s.get_history()
        lastval = s.get_currentValue()
    except:
        lastval = 'Invalid ticker or no information availlable!'

    return lastval
    