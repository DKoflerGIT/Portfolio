from fastapi import templating
from numpy import double
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
import yfinance as yf

# local utilities
from classes import stock as Stock
from functions import stockFunctions as sf, models
from functions.database import SessionLocal, engine

app = FastAPI()
templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=engine)

stocks = []
pathFinances = "/finances"

# ./run


# /
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", { "request" : request, "title" : "Home" })


# Overview of stocks in portfolio
# /finances/stocks/portfolio
@app.get(pathFinances + "/stocks/portfolio")
def portfolio(request: Request):
    stocks = sf.refreshStocks()
    data = {}
    for s in stocks:
        data[s.ticker] = {
            'value' :  s.getValue(),
            'valueChange' :  s.calcValueChange(),
            'valueChangePercent' :  s.calcValueChangePercent(),
            'buyPrice' :  s.buyPrice,
            'profitPercent' : s.calcProfitPercent()
            }

    # return data
    return templates.TemplateResponse("portfolio.html", { "request" : request, "title" : "Portfolio" })


# Add a stock to the portfolio
# /finances/stocks/portfolio/add-stock
@app.post(pathFinances + "/stocks/portfolio/add-stock")
def addStock(ticker: str, buyPrice: double, buyAmount: double, buyFees: double):
    return {"error" : "not implemented yet"}


# Get info about a specific stock
# /finances/stocks/[ticker]
@app.get(pathFinances + "/stocks/{ticker}")
def stockInfo(ticker: str):
    s = yf.Ticker(ticker)
    try:
        h = s.history(period="5d")
        lastval = round(h.Close[-1], 2)
        change = str(round(100 / h.Close[-2] * h.Close[-1] - 100, 2)) + '%'
    except:
        return { 'error' : 'Invalid ticker or no information availlable!' }

    return {
        ticker: {
            'value' : lastval,
            'change' : change
        }
    }
    