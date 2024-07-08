import pandas as pd
import yfinance as yf
import numpy as np

# Download AAPL stock data using yfinance
aapl = yf.download("AAPL")

# Calculate the 8-day and 21-day moving averages
aapl["MA8"] = aapl["Close"].rolling(window=8).mean()
aapl["MA21"] = aapl["Close"].rolling(window=21).mean()

# Create a new column to hold the position (1 for long, -1 for short)
aapl["Position"] = 0
aapl["Position"][8:] = np.where(aapl["MA8"][8:] > aapl["MA21"][8:], 1, -1)

# Calculate the daily returns
aapl["Returns"] = aapl["Close"].pct_change() * aapl["Position"].shift(1)

# Calculate the cumulative returns
aapl["Cumulative Returns"] = (1 + aapl["Returns"]).cumprod()

# Save the data to a CSV file
aapl.to_csv("output/AAPL_Moving_Average_Crossover.csv")
