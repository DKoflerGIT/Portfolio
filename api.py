import yfinance as yf
from matplotlib import pyplot as plt
import pandas as pd
from fastapi import FastAPI
from datetime import date, timedelta

from classes import stock as Stock

app = FastAPI()
stocks = []
path_investing = "/investing"

# uvicorn api:app --reload

def refreshStocks():
    stocks.clear()
    stocks_bought_raw = pd.read_excel('data\stocks_bought.xlsx')
    stocks_bought = list(stocks_bought_raw.ticker)
    data = yf.download(stocks_bought, start=date.today() - timedelta(days=5*365), end=date.today(), group_by="ticker", threads=True)
    
    for i, s in enumerate(stocks_bought):
        stocks.append(Stock.stock(s, data[s], stocks_bought_raw.buy_price[i], stocks_bought_raw.num_stocks[i], stocks_bought_raw.buy_fees_eur[i]))

# /
@app.get("/")
def root():
    return "root"

# /investing
@app.get(path_investing)
def overview():
    refreshStocks()
    overview = {}
    for s in stocks:
        overview[s.ticker] = {
            'value' :  s.get_value(),
            'valueChange' :  s.calc_valueChange(),
            'valueChangePercent' :  s.calc_valueChangePercent(),
            'buyPrice' :  s.buy_price,
            #'buyAmount' : s.num_stocks,
            #'buyFeesEur' : s.buy_fees_eur,
            #'buyFeesUsd' : s.buy_fees_usd,
            #'profit' : s.calc_profit(),
            'profitPercent' : s.calc_profitPercent()
            }

    return overview

@app.get(path_investing + "/stock/{ticker}")
def stockOverview(ticker: str):
    s = yf.Ticker(ticker)
    try:
        lastval = round(s.history(period="1d").Close[-1], 2)
    except:
        lastval = 'Invalid ticker or no information availlable!'

    return lastval
    