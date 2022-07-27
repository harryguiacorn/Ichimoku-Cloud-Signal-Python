# import modules
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
from tapy import Indicators

from finta import TA

# initializing Parameters
start = "2022-01-01"
end = "today"
symbols = ["AAPL"]  # , "TSLA", "GOOGL"
list_data = []

f = open('pandas.txt', 'w')

# Getting the data
for __symbol in symbols:
    try:
        data = pdr.get_data_yahoo(__symbol, start, end)

        f.write(__symbol+'\n')
        f.write(data.corr().to_string())
        f.write('\n')

        list_data.append(data)

        data.to_csv('data/' + __symbol + '.csv')
    except Exception as e:
        print("Error: ")
        raise Exception("Error getting: ")
f.close()

# initialising indicators
__i = Indicators(data)
__i.ichimoku_kinko_hyo(column_name_kijun_sen="K Line")
__dataCloud = __i.df
__dataCloud.to_csv('data/AAPL_cloud.csv')

# Display
""" plt.figure(figsize = (20,10))
plt.title('Closing Prices from {} to {}'.format(start, end))
plt.plot(data['Close'])
plt.show() """

""" df = pd.read_csv('data/AAPL.csv')
print(df.head())
print(TA.ICHIMOKU(df))
TA.ICHIMOKU(df).to_csv('data/' + __symbol + '-cloud.csv') """
