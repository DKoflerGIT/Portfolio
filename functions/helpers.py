import yfinance as yf

def validate(v):
    return v if v is not None else 0

def eurToUsd(eur):
    u = yf.Ticker("EURUSD=X")
    h = u.history(period="1d", interval="1d").Close[-1]
    return round(eur * h, 2)

def usdToEur(usd):
    e = yf.Ticker("EUR=X")
    h = e.history(period="1d", interval="1d").Close[-1]
    return round(usd * h, 2)