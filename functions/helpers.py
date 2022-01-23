import yfinance as yf

def validate(v):
    return v if v is not None else 0

def eurToUsd(eur: float):
    u = yf.Ticker("EURUSD=X")
    h = u.history(period="1d", interval="1d").Close[-1]
    return round(float(eur) * float(h), 2)

def usdToEur(usd: float):
    e = yf.Ticker("EUR=X")
    h = e.history(period="1d", interval="1d").Close[-1]
    return round(float(usd) * float(h), 2)