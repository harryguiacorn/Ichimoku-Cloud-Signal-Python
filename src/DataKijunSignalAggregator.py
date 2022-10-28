from argparse import ArgumentParser
from genericpath import isdir
import os
import pandas as pd


class DataKijunSignalAggregator:

    def __init__(self,
                 __csvPath='data/',
                 __assetListPath='',
                 __assetClassName=""):
        self.csvPath = __csvPath
        self.assetListPath = __assetListPath
        self.assetClassName = __assetClassName

    def readLocalCsvData(self, symbols, __csvPath, __suffix):
        __dict_df = {}
        for __symbol in symbols:
            # print("#####################",__symbol[1])
            __df = pd.read_csv(__csvPath + __symbol + __suffix + '.csv')
            __dict_df[__symbol] = __df
        return __dict_df

    def readAssetList(self, __csvPath, __colName='symbol'):
        df = pd.read_csv(__csvPath)
        # print(df.to_string())
        # l_symbol = df[__colName].tolist()
        d_symbol = df.to_dict(orient="list")
        # print(d_symbol)
        return d_symbol

    def __createDataFolder(self, __name="data"):
        # create data folder
        try:
            if isdir(__name) == False:
                os.mkdir(__name)
        except FileExistsError as __errFile:
            print("data folder exists")

    def main(self):
        print("*************************************************")
        list_result = self.getLatestResultFromEachDataFrame()
        df_result = self.exportResult(list_result)
        print(df_result)
        print("aggregator csv file is created")
        return df_result

    def getLatestResultFromEachDataFrame(self):
        symbols = self.readAssetList(self.assetListPath)
        # print("------------------",symbols)
        dict_df = self.readLocalCsvData(symbols['symbol'], self.csvPath, '_kijunCount')
        list_result = []
        for __symbol, __value in dict_df.items():
            __kijunDirection = __value['Kijun Direction'].iloc[
                -1]  # get latest direction sits at the bottom of dataframe
            __kijunConsecutiveCount = __value['Kijun Signal Count'].iloc[-1]
            # print(symbols['symbol'].index(__symbol))
            __index = symbols['symbol'].index(__symbol)
            __symbolName = symbols['name'][__index]

            list_temp = []
            list_temp.append(__symbol)
            list_temp.append(__kijunDirection)
            list_temp.append(__kijunConsecutiveCount)
            list_temp.append(__symbolName)
            list_result.append(list_temp)
        return list_result

    def exportResult(self, list_result):
        df_result = pd.DataFrame(list_result,
                                 columns=['Symbol', 'Direction', 'Count', 'Name'])
        df_result.sort_values(by=['Count'], inplace=True)
        self.__createDataFolder(self.csvPath + 'result/')
        df_result.to_csv(self.csvPath + 'result/' +
                         self.assetClassName.replace(" ", "") + '.csv',
                         index=False)
        return df_result
