from argparse import ArgumentParser
import pandas as pd

class DataKijunSignalAggregator:

    def __init__(self, __csvPath='data/', __assetListPath='', __symbol= "", __kijunDirection = None, __kijunConsecutiveCount= None):
        self.csvPath = __csvPath
        self.assetListPath = __assetListPath
        self.symbol = __symbol
        self.kijunDirection = __kijunDirection
        self.kijunConsecutiveCount = __kijunConsecutiveCount

    def readLocalCsvData(self, symbols, __csvPath, __suffix):
        __dict_df = {}
        for __symbol in symbols:
            __df = pd.read_csv(__csvPath + __symbol + __suffix+ '.csv')
            __dict_df[__symbol] = __df
        return __dict_df

    def readAssetList(self, __csvPath, __colName='symbol'):
        df = pd.read_csv(__csvPath)
        print(df.to_string())
        l_symbol = df[__colName].tolist()
        return l_symbol

    def main(self):
        print("*************************************************")
        symbols = self.readAssetList(self.assetListPath)
        dict_df = self.readLocalCsvData(symbols, self.csvPath, '_kijunCount')
        list_result = []
        for __symbol, __value in dict_df.items():
            # print(__symbol, self.csvPath)
            __kijunDirection = __value['Kijun Direction'].iloc[-1]
            __kijunConsecutiveCount = __value['Kijun Signal Count'].iloc[-1]
            # print(__symbol, __kijunDirection, __kijunConsecutiveCount)
            dataP = DataKijunSignalAggregator(__symbol, self.csvPath, __symbol, __kijunDirection, __kijunConsecutiveCount)
            
            list_temp = []
            list_temp.append(__symbol)
            list_temp.append(__kijunDirection)
            list_temp.append(__kijunConsecutiveCount)
            list_result.append(list_temp)
            
        df_result = pd.DataFrame(list_result, columns = ['Symbol', 'Direction', 'Count'])
        df_result.sort_values(by=['Count'], inplace=True)

        print(df_result)

            
