# region Imports
from fastapi import templating
from numpy import double
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from openpyxl import load_workbook
from sqlalchemy.orm import Session, session
import uvicorn
import yfinance as yf
from classes.stock import Stock

# local utilities
from classes.stockRequest import StockRequest
from database import models, dbFunctions as dbF
from functions import stockFunctions as sF
from database.database import SessionLocal, engine
from database.models import Stock as dbModelStock

# endregion

app = FastAPI()
templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=engine)

# region Home

@app.get("/")
def home(request: Request):
    dataDict = {
        "request" : request,
        "title" : "Home"
    }
    return templates.TemplateResponse("home.html", dataDict)
# endregion

# region Finances

@app.get("/finances")
def home(request: Request):
    dataDict = {
        "request" : request,
        "title" : "Finances"
    }
    return templates.TemplateResponse("finances.html", dataDict)
# endregion

# region Dashboard

@app.get("/finances/dashboard")
def home(request: Request):
    dataDict = {
        "request" : request,
        "title" : "Dashboard"
    }
    return templates.TemplateResponse("dashboard.html", dataDict)
# endregion

# region Portfolio

# Overview /finances/stocks/portfolio
@app.get("/finances/stocks/portfolio")
def portfolio(request: Request):
    stocks = sF.fetchStockDataPortfolio()

    if stocks:
        pStocks = []
        for s in stocks:
            pStocks.append([
                s.ticker,
                s.getValue(),
                s.calcValue1dChange(),
                str(s.calcValueChange1dPercent()) + ' %',
                str(s.buyPrice),
                str(s.calcProfitPercent()) + ' %',
                s.calcProfit(),
                s.calcEquity()
            ])

    dataDict = {
        "request" : request,
        "title" : "Portfolio",
        "stocks" : pStocks if stocks else None
    }
    return templates.TemplateResponse("portfolio.html", dataDict)


# Add a stock /finances/stocks/portfolio/add-stock
@app.post("/finances/stocks/portfolio/add-stock")
async def portfolioAddStock(stockRequest: StockRequest, backgroundTasks: BackgroundTasks):
    backgroundTasks.add_task(sF.saveStockToDB(stockRequest.ticker, stockRequest.buyDate, stockRequest.buyAmount, stockRequest.buyFeeEur))


# Remove a stock /finances/stocks/portfolio/remove-stock
@app.delete("/finances/stocks/portfolio/remove-stock")
async def portfolioDeleteStock(stockRequest: StockRequest, backgroundTasks: BackgroundTasks):
    backgroundTasks.add_task(sF.deleteStockFromDB(stockRequest.ticker))

# endregion

# region Watchlist

# Overview /finances/stocks/watchlist
@app.get("/finances/stocks/watchlist")
def watchlist(request: Request): 
    stocks = sF.fetchStockDataWatchlist() # list of watchlist stock objects

    if stocks:
        wStocks = []
        for s in stocks:
            wStocks.append([s.ticker, s.getValue(), s.calcValue1dChange(), str(s.calcValueChange1dPercent()) + ' %'])

    dataDict = {
        "request" : request,
        "title" : "Watchlist",
        "stocks" : wStocks if stocks else None
    }

    return templates.TemplateResponse("watchlist.html", dataDict)
    # return dataDict


# Add a stock /finances/stocks/watchlist/add-stock
@app.post("/finances/stocks/watchlist/add-stock")
async def watchlistAddStock(stockRequest: StockRequest, backgroundTasks: BackgroundTasks):
    backgroundTasks.add_task(sF.saveStockToDB(stockRequest.ticker))


# Remove a stock /finances/stocks/watchlist/remove-stock
@app.delete("/finances/stocks/watchlist/remove-stock")
async def watchlistRemoveStock(stockRequest: StockRequest, backgroundTasks: BackgroundTasks):
    backgroundTasks.add_task(sF.deleteStockFromDB(stockRequest.ticker))

# endregion

# region StockInfo

# Get info about a specific stock /finances/stocks/[ticker]
@app.get("/finances/stocks/{ticker}")
def stockinfo(request: Request, ticker: str): 
    stock = yf.Ticker(ticker)
    name = stock.info['shortName']

    dataDict = {
        "request" : request,
        "title" : name,
        "ticker" : ticker.upper()
    }
    return templates.TemplateResponse("stock.html", dataDict)


@app.get("/finances/stocks/{ticker}/getData")
def stockinfo(request: Request, ticker: str): 

    stock = yf.Ticker(ticker)
    info = stock.info
    history = stock.history(period='5y').Close
    close = info['regularMarketPreviousClose']
    change = str(round(100 / history[-2] * (history[-1] -  history[-2]), 2)) + ' %'
    open = info['regularMarketOpen']
    low = info['regularMarketDayLow']
    high = info['regularMarketDayHigh']
    sector = info['sector']
    news = stock.news
    exchange = info['exchange']
    currency = info['financialCurrency']

    dataDict = {
        "history" : dict(history),
        "close" : close,
        "open" : open,
        "high" : high,
        "low" : low,
        "change" : change,
        "sector" : sector,
        "news" : news,
        "exchange" : exchange,
        "currency" : currency
    }
    return dataDict


@app.get("/finances/stocks/{ticker}/getDataBalanceSheet")
def stockinfo(request: Request, ticker: str): 

    stock = yf.Ticker(ticker)
    balanceSheet = stock.balance_sheet

    dataDict = {
        "balanceSheet" : dict(balanceSheet)
    }
    return dataDict


@app.get("/finances/stocks/{ticker}/getDataFinancials")
def stockinfo(request: Request, ticker: str): 

    stock = yf.Ticker(ticker)
    financials = stock.financials

    # rename columns to be a nice header
    rename_dict = {}

    for i in range(len(financials.columns)):
        rename_dict[financials.columns[i]] = financials.columns[i].strftime("%b %d, %Y")

    financials.rename(columns=rename_dict, inplace=True)

    # fill Nones with empty strings
    financials.fillna("-", inplace=True)

    # format numbers to be better readable
    for i in range(len(financials.columns)):
        c = financials[financials.columns[i]][2]
        for j in range(len(financials[financials.columns[i]])):
            f = financials[financials.columns[i]][j]

            if type(f) == float:
                if c>1000000000:
                    f /= 1000000000
                    financials[financials.columns[i]][j] = str(f) + " Bn"
                else:
                    f /= 1000000
                    financials[financials.columns[i]][j] = str(f) + " Mn"

    dataDict = {
        "financials" : dict(financials)
    }
    return dataDict


@app.get("/finances/stocks/{ticker}/getDataCashflow")
def stockinfo(request: Request, ticker: str): 

    stock = yf.Ticker(ticker)
    cashflow = stock.cashflow

    dataDict = {
        "cashflow" : dict(cashflow)
    }
    return dataDict

 # endregion

if __name__ == '__main__':
     uvicorn.run(app)