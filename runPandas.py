# import modules
from genericpath import isdir
import os
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
from tapy import Indicators
from finta import TA


def main():
    # initializing Parameters
    start = "2022-01-01"
    end = "today"
    symbols = ["AAPL", "TSLA", "GOOGL"]  #
    list_data = []

    __create_folder()

    with open('pandas.txt', 'w') as f:
        # Getting the data
        __dict_df = {}
        for __symbol in symbols:
            try:
                data = pdr.get_data_yahoo(__symbol, start, end)

                __dict_df[__symbol] = data

                f.write(__symbol + '\n')
                f.write(data.corr().to_string())
                f.write('\n')

                list_data.append(data)

                data.to_csv('data/' + __symbol + '.csv')
            except Exception as e:
                print("Error: ")
                raise Exception("Error getting: ")

    for __key, __df in __dict_df.items():
        # initialising indicators
        __i = Indicators(__df)
        # __i.ichimoku_kinko_hyo(column_name_kijun_sen="K Line")
        __dataCloud = __i.df
        __dataCloud.to_csv('data/' + __key + '_cloud.csv')

    # Display
    """ plt.figure(figsize = (20,10))
    plt.title('Closing Prices from {} to {}'.format(start, end))
    plt.plot(data['Close'])
    plt.show() """
    """ df = pd.read_csv('data/AAPL.csv')
    print(df.head())
    print(TA.ICHIMOKU(df))
    TA.ICHIMOKU(df).to_csv('data/' + __symbol + '-cloud.csv') """


def __create_folder(__name="data"):
    # create data folder
    try:
        if isdir(__name) == False:
            os.mkdir(__name)
    except FileExistsError as __errFile:
        print("data folder exists")


if __name__ == "__main__":
    main()