import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# download the stock data
aapl = yf.download("AAPL", start="2010-01-01", end="2023-04-09")
tsla = yf.download("TSLA", start="2010-01-01", end="2023-04-09")

# select the Adjusted Close price column
aapl = aapl["Adj Close"]
tsla = tsla["Adj Close"]

# combine the data into one DataFrame
df = pd.concat([aapl, tsla], axis=1)
df.columns = ["AAPL", "TSLA"]

# calculate the cumulative returns
cum_returns = (1 + df.pct_change()).cumprod()

# plot the cumulative returns of two stocks on one chart
plt.plot(cum_returns["AAPL"], label="AAPL")
plt.plot(cum_returns["TSLA"], label="TSLA")

# set the chart title and axis labels
plt.title("Cumulative Returns of AAPL and TSLA")
plt.xlabel("Date")
plt.ylabel("Cumulative Returns")

# add a legend
plt.legend()

# display the chart
plt.show()
