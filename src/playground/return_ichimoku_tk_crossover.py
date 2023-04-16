import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Download AAPL stock data using yfinance
aapl = yf.download("AAPL", period="6mo")

# Calculate the Ichimoku cloud components
high_9 = aapl["High"].rolling(window=9).max()
low_9 = aapl["Low"].rolling(window=9).min()
high_26 = aapl["High"].rolling(window=26).max()
low_26 = aapl["Low"].rolling(window=26).min()
tenkan_sen = (high_9 + low_9) / 2
kijun_sen = (high_26 + low_26) / 2
senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)
senkou_span_b = (
    (
        aapl["High"].rolling(window=52).max()
        + aapl["Low"].rolling(window=52).min()
    )
    / 2
).shift(26)
chikou_span = aapl["Close"].shift(-26)

# Determine the position based on price's relation to the cloud
aapl["Position"] = np.where(
    (aapl["Close"] < senkou_span_a) & (aapl["Close"] > senkou_span_b), 0, 0
)
aapl["Position"] = np.where(
    (aapl["Close"] > senkou_span_a) & (aapl["Close"] < senkou_span_b), 0, 0
)
aapl["Position"] = np.where(
    (aapl["Close"] > senkou_span_a) & (aapl["Close"] > senkou_span_b),
    1,
    aapl["Position"],
)
aapl["Position"] = np.where(
    (aapl["Close"] < senkou_span_a) & (aapl["Close"] < senkou_span_b),
    -1,
    aapl["Position"],
)

# Calculate the daily returns
aapl["Returns"] = aapl["Close"].pct_change() * aapl["Position"].shift(1)

# Create a column to track the position changes
aapl["Position Change"] = aapl["Position"].diff()

# Create a column to track the previous position
aapl["Previous Position"] = aapl["Position"].shift(1)

# Create a column to track the cumulative returns for each individual position
aapl["Cumulative Returns Daily"] = np.nan
aapl["Cumulative Returns"] = np.nan

# Loop through the rows and calculate the cumulative returns
# for each individual position
cumulative_returns = 1
for i, row in aapl.iterrows():
    if row["Position Change"] != 0:
        cumulative_returns = 1
    aapl.at[i, "Cumulative Returns Daily"] = (
        row["Returns"] * cumulative_returns
    )
    cumulative_returns *= 1 + row["Returns"]
# aapl["Cumulative Returns"] += aapl["Cumulative Returns Daily"].shift(1)


# x = (1 + aapl["Returns"]).cumprod() - 1
# aapl["Cumulative Returns %"] = x

# Remove the columns used for the calculation
aapl.drop(
    [
        "Open",
        "High",
        "Low",
        "Adj Close",
        "Volume",
        # "Position Change",
        # "Previous Position",
    ],
    axis=1,
    inplace=True,
)

# Plot the cumulative returns
aapl["Cumulative Returns"].plot()
# plt.show()

# Save the data to a CSV file
aapl.to_csv("output/AAPL_Ichimoku_TK_Crossover.csv")
