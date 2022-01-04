def main():
    import yfinance as yf
    import matplotlib.pyplot as plt
    import pandas as pd

    from classes import stock as stock

    stocks_bought = pd.read_excel('data\stocks_bought.xlsx')

    stocks = []
    for i, t in enumerate(list(stocks_bought.ticker)):
        t = stocks_bought.ticker[i]
        bp = stocks_bought.buy_price[i]
        ns = stocks_bought.num_stocks[i]
        bf = stocks_bought.buy_fees_eur[i]

        s = stock.stock(t, bp, ns, bf)
        stocks.append(s)

if __name__ == '__main__':
    main()