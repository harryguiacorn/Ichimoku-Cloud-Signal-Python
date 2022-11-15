# import modules
from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt
  
# initialize parameters
start_date = datetime(2020, 1, 1)
end_date = datetime(2021, 1, 1)
  
# get the data
data = yf.download('SPY', start = start_date,
                   end = end_date)
print(data)
# display
plt.figure(figsize = (20,10))
plt.title('Opening Prices from {} to {}'.format(start_date,
                                                end_date))
plt.plot(data['Open'])
plt.show()