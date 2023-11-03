import yfinance as yf

stock = yf.Ticker("MSFT")
get = stock.info
print(get)