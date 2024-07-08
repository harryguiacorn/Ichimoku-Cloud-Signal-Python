# import modules
from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt
  
import yfinance as yf
import pandas as pd

symbol = 'AAPL'
interval = '1h'

start_date = '2023-01-01'
end_date = '2023-02-01'

data = yf.download(symbol, start=start_date, interval=interval)

# Save data to a CSV file
data.to_csv(symbol + " - " + interval + " - "+ start_date  + " - " + end_date +  ".csv")


print(data)
# display
plt.figure(figsize = (20,10))
plt.title('Opening Prices from {} to {}'.format(start_date,
                                                end_date))
plt.plot(data['Open'])
# plt.show()