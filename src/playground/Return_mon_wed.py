import pandas as pd
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

symbol = "AAPL"  # Replace with your desired stock symbol
# start_date = "2022-01-01"
# end_date = "2022-01-31"

# period : str
#     Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
#     Either Use period parameter or use start and end
stock_data = yf.download(symbol, period="2y")

stock_returns = stock_data["Close"].pct_change()
stock_data["Returns"] = stock_returns

# Select only the Wednesday prices
# wednesday_prices = stock_data["Close"].loc[stock_data.index.weekday == 2]
# wednesday_prices = stock_data.index.weekday

# Calculate the percentage change between the Wednesday prices
# wednesday_returns = wednesday_prices.pct_change()
# print(stock_data.head())

# Select only the Monday and Wednesday prices
# monday_prices = stock_data["Close"].loc[stock_data.index.weekday == 0]
monday_prices = stock_data["Close"].shift(2)
wednesday_prices = stock_data["Close"].loc[stock_data.index.weekday == 2]

# Shift the Monday prices one week back
monday_prices_shifted = monday_prices.shift(5)

# Calculate the percentage change between the Monday and Wednesday prices
wednesday_returns = (wednesday_prices - monday_prices) / monday_prices

stock_data["Week day"] = stock_data.index.weekday
stock_data["MON-WED Returns"] = wednesday_returns
print(monday_prices, wednesday_prices, wednesday_returns)
stock_data.to_csv(
    "data/playground/" + symbol + ".csv",
    columns=["Week day", "Close", "Returns", "MON-WED Returns"],
)


# Plot a bell curve of the returns
sns.displot(stock_returns, kde=True)
# plt.hist(stock_returns)
plt.xlabel("Daily Returns")
plt.title("Histogram of Daily Stock Returns")
plt.show()

# # make this example reproducible
# np.random.seed(0)

# # create data
# x = np.random.normal(size=1000)

# # create normal distribution curve
# sns.displot(x, kde=True)
