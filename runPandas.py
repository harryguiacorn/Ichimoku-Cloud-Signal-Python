# import modules
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
from tapy import Indicators
from TAcharts.indicators.ichimoku import Ichimoku
from TAcharts.utils.ohlcv import OHLCV

# initializing Parameters
start = "2022-01-01"
end = "today"
symbols = ["AAPL"]
  
# Getting the data
data = pdr.get_data_yahoo(symbols, start, end)
data.to_csv('AAPL.csv')

# initialising indicators
""" __i = Indicators(data)
__i.ichimoku_kinko_hyo(column_name_kijun_sen="K Line")
data = __i.df
data.to_csv('AAPL Cloud.csv') """

# Display
""" plt.figure(figsize = (20,10))
plt.title('Opening Prices from {} to {}'.format(start, end))
plt.plot(data['Close'])
plt.show() """

# Plot Cloud Chart
# __plot = Ichimoku(data)
# __plot.build(26, 52, 52, 26)

# __plot.plot()