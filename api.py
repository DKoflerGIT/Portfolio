# region Imports
from fastapi import templating
from numpy import double
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, session
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
 # endregion