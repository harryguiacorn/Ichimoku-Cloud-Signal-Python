import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Download AAPL stock data using yfinance
aapl = yf.download("GBPJPY=X", period="1y", interval="60m")

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
aapl["Returns"] = aapl["Close"].pct_change()

# Calculate the cumulative returns
aapl["Cumulative Returns"] = (1 + aapl["Returns"]).cumprod()

# Calculate the daily returns
aapl["Returns(Cloud)"] = aapl["Close"].pct_change() * aapl["Position"].shift(1)

# Calculate the cumulative returns
aapl["Cumulative Returns(Cloud)"] = (1 + aapl["Returns(Cloud)"]).cumprod()

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

# Save the data to a CSV file
aapl.to_csv("output/Playground_Ichimoku_Cloud_Signal.csv")

# Plot the cumulative returns
fig = plt.figure()
ax1 = fig.add_subplot(321)
ax2 = fig.add_subplot(322)
ax1.plot(aapl["Cumulative Returns"])
ax1.set_title("Amazon")
ax2.plot(aapl["Cumulative Returns(Cloud)"])
ax2.set_title("Apple")
plt.tight_layout()
plt.show()

# aapl["Cumulative Returns"].plot()
# aapl["Cumulative Returns(Cloud)"].plot()
