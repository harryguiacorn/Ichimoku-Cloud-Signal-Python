import pandas as pd
import yfinance as yf

symbol = "AAPL"  # Replace with your desired stock symbol
# start_date = "2022-01-01"
# end_date = "2022-01-31"

stock_data = yf.download(symbol, period="1mo")

stock_returns = stock_data["Close"].pct_change()

# Select only the Wednesday prices
# wednesday_prices = stock_data["Close"].loc[stock_data.index.weekday == 2]
wednesday_prices = stock_data.index.weekday


# Calculate the percentage change between the Wednesday prices
# wednesday_returns = wednesday_prices.pct_change()

stock_data["Returns"] = stock_returns
stock_data["MON-WED Returns"] = wednesday_prices

# print(stock_data.head())
stock_data.to_csv("data/playground/" + symbol + ".csv")
