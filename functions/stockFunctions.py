# region imports
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, session
from sqlalchemy.sql import select, or_, and_
import yfinance as yf, pandas as pd, os
from datetime import date, timedelta
import requests

# local utilities
from classes import stock as stk
from classes.stockRequest import StockRequest
from database import models, dbFunctions as dbF
from functions import stockFunctions as sF
from database.database import SessionLocal, engine
from database.models import Stock as dbModelStock
# endregion


def fetchStockDataPortfolio():
    # fetch tickers from database
    db = SessionLocal()
    dbStocks = db.query(dbModelStock).filter(and_(dbModelStock.buyDate != None, dbModelStock.buyAmount != None, dbModelStock.buyFeeEur != None)).order_by(dbModelStock.ticker.asc()).all()
    if not dbStocks: return None
    tickers = []
    stocks = []
    for d in dbStocks:
        tickers.append(d.ticker)
        stocks.append([d.ticker, d.buyDate, d.buyAmount, d.buyFeeEur])

    # fetch data from yahoo finance
    data = yf.download(tickers, period='5y', group_by="ticker")
    
    # create stock objects
    portfolioStocks = []
    if len(tickers) == 1:
        portfolioStocks.append(stk.Stock(tickers[0], data, stocks[0][1], stocks[0][2], stocks[0][3]))
    else:
        for i, s in enumerate(tickers):
            portfolioStocks.append(stk.Stock(stocks[i][0], data[s], stocks[i][1], float(stocks[i][2]), float(stocks[i][3])))

    return portfolioStocks


def fetchStockDataWatchlist():
    # fetch tickers from database
    db = SessionLocal()
    dbStocks = db.query(dbModelStock).filter(or_(dbModelStock.buyAmount == None, dbModelStock.buyFeeEur == None)).all()
    if not dbStocks: return None
    tickers = []
    for d in dbStocks:
        tickers.append(d.ticker)

    # fetch data from yahoo finance
    data = yf.download(tickers, period='5y', group_by="ticker")
    
    # create stock objects
    watchlistStocks = []
    if len(tickers) == 1:
        watchlistStocks.append(stk.Stock(tickers[0], data))
    else:
        for s in tickers:
            watchlistStocks.append(stk.Stock(s, data[s]))
    return watchlistStocks


def saveStockToDB(ticker, buyDate=None, buyAmount=0, buyFeeEur=0):
    db = SessionLocal()
    dbStock = dbModelStock()
    dbStock.ticker = ticker.upper()
    if buyDate != None and buyAmount > 0 and buyFeeEur > 0:
        dbStock.buyDate = buyDate
        dbStock.buyAmount = buyAmount
        dbStock.buyFeeEur = buyFeeEur
    try:
        db.add(dbStock)
        db.commit()
    except:
        return False
    return True


def deleteStockFromDB(ticker):
    db = SessionLocal()
    try:
        db.query(dbModelStock).filter(dbModelStock.ticker==ticker).delete()
        db.commit()
    except:
        return False
    return True


def fetchStockDataWeb(ticker: str):
    yfStock = yf.Ticker(ticker)
    try:
        data = yfStock.history(period="5y")
    except:
        return False
    stock = stk.Stock(ticker, data)
    return stock


def refreshStock(stock: stk.Stock):
    yfStock = yf.Ticker(stock.name)
    stock.data = yfStock.history(period='5y')
    stock.value = yfStock.info["previousClose"]
    stock.pe = yfStock.info["forwardPE"]
    stock.dividendYield = yfStock.info["dividendYield"] * 100

    return stock