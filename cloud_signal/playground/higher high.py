import yfinance as yf
import logging

logger = logging.getLogger(__name__)

# Define the stock symbol and date range
stock_symbol = "WMT"  # Apple Inc.
start_date = "2023-01-01"
end_date = "2023-12-31"

# Fetch Apple stock data
apple_stock = yf.Ticker(stock_symbol)
df = apple_stock.history(period="1d", start=start_date, end=end_date)

# Calculate daily difference of highs
df["High_Difference"] = df["High"] - df["High"].shift(1)

# Create a new column 'higher high' based on the condition
df["higher high"] = (df["High"] > df["High"].shift(1)).astype(int)

# Identify the Kicker Bullish pattern
df["Kicker Bullish"] = 0  # Initialize the column to 0
for i in range(1, len(df) - 1):
    if (
        df["Open"].iloc[i] < df["Open"].iloc[i + 1]
        and df["Close"].iloc[i] < df["Open"].iloc[i]
        and df["Close"].iloc[i] < df["Low"].iloc[i]
        and df["Close"].iloc[i + 1] < df["Open"].iloc[i + 1]
    ):
        df.at[df.index[i + 1], "Kicker Bullish"] = 1

# Create a new CSV file with the results
output_file = "output/apple_stock_daily_high_difference_kicker.csv"
df.to_csv(output_file)

logger.info(f"Data saved to {output_file}")
