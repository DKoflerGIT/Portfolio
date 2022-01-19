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

# region Portfolio

# Overview /finances/stocks/portfolio
@app.get("/finances/stocks/portfolio")
def portfolio(request: Request):
    stocks = sF.fetchStockDataPortfolio()

    if stocks:
        pStocks = []
        for s in stocks:
            pStocks.append([s.ticker, s.getValue(), s.calcValue1dChange(), str(s.calcValueChange1dPercent()) + ' %', str(s.calcProfitPercent()) + ' %'])

    dataDict = {
        "request" : request,
        "title" : "Portfolio",
        "stocks" : pStocks if stocks else None
    }
    return templates.TemplateResponse("portfolio.html", dataDict)


# Add a stock /finances/stocks/portfolio/add-stock
@app.post("/finances/stocks/portfolio/add-stock")
async def portfolioAddStock(stockRequest: StockRequest, backgroundTasks: BackgroundTasks):
    backgroundTasks.add_task(sF.saveStockToDB(stockRequest.ticker, stockRequest.buyPrice, stockRequest.buyAmount, stockRequest.buyFeeEur))


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
    history = stock.history(period='5y').Close
    close = stock.info['regularMarketPreviousClose']
    change = str(round(100 / history[-2] * (history[-1] -  history[-2]), 2)) + ' %'
    open = stock.info['regularMarketOpen']
    low = stock.info['regularMarketDayLow']
    high = stock.info['regularMarketDayHigh']
    sector = stock.info['sector']

    dataDict = {
        "history" : dict(history),
        "close" : close,
        "open" : open,
        "high" : high,
        "low" : low,
        "change" : change,
        "sector" : sector
    }
    return dataDict

 # endregion


if __name__ == '__main__':
     uvicorn.run(app)