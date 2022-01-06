import yfinance as yf

def validate(v):
    return v if v is not None else 0

def eurusd():
    eur = yf.Ticker("EURUSD=X")
    return eur.history(period="1d", interval="1d").Close[-1]

def usdeur():
    usd = yf.Ticker("EUR=X")
    return usd.history(period="1d", interval="1d").Close[-1]