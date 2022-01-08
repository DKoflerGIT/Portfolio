from classes import stock as stk
from datetime import date, timedelta
import yfinance as yf, pandas as pd, os

def refreshStocks():
    stocks = []
    # p = os.path.join(os.getcwd(), '..', 'datasets\stocks_bought.xlsx' )
    p = 'datasets\stocks_bought.xlsx'
    stocksBoughtRaw = pd.read_excel(p)
    stocksBought = list(stocksBoughtRaw.ticker)
    data = yf.download(stocksBought, start=date.today() - timedelta(days = 5 * 365), end=date.today(), group_by="ticker")
    
    for i, s in enumerate(stocksBought):
        stocks.append(stk.Stock(s, data[s], stocksBoughtRaw.buy_price[i], stocksBoughtRaw.num_stocks[i], stocksBoughtRaw.buy_fees_eur[i]))
    
    return stocks