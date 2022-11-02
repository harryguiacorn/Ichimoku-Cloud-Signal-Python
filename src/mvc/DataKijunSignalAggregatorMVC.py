from genericpath import isdir
import os
import pandas as pd


class Model(object):

    def __init__(self,
                 __csvPath='data/',
                 __assetListPath='',
                 __outputPath="",
                 __assetClassName=""):
        self.csvPath = __csvPath
        self.assetListPath = __assetListPath
        self.assetClassName = __assetClassName
        self.outputPath = __outputPath
        self.resultList = None
        self.resultDataFrame = None

    @property
    def resultList(self):
        return self.__resultList

    @resultList.setter
    def resultList(self, __list):
        self.__resultList = __list

    @property
    def resultDataFrame(self):
        return self.__resultDataFrame

    @resultDataFrame.setter
    def resultDataFrame(self, __df):
        self.__resultDataFrame = __df

    def readLocalCsvData(self, symbols, __csvPath, __suffix):
        __dict_df = {}
        for __symbol in symbols:
            try:
                __filePath = __csvPath + __symbol + __suffix + '.csv'
                __df = pd.read_csv(__filePath)
            except FileNotFoundError:
                print(f"Error: {__filePath} not found")
                continue
            else:
                __dict_df[__symbol] = __df
        # print(__dict_df)
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

    def getLatestResultFromEachDataFrame(self):
        symbols = self.readAssetList(self.assetListPath)
        # print("------------------",symbols)
        dict_df = self.readLocalCsvData(symbols['symbol'], self.csvPath,
                                        '_kijunCount')
        list_result = []
        for __symbol, __value in dict_df.items():
            try:
                # get latest direction sits at the bottom of dataframe
                __kijunDirection = __value['Kijun Direction'].iloc[-1]
                __kijunConsecutiveCount = __value['Kijun Signal Count'].iloc[
                    -1]
                __index = symbols['symbol'].index(__symbol)
                __symbolName = symbols['name'][__index]
                __date = __value['Date'].iloc[-1]

            except KeyError as e:
                print("--------------KeyError------------------", e.args)
                continue
            else:
                list_temp = []
                list_temp.append(__date)
                list_temp.append(__symbol)
                list_temp.append(__symbolName)
                list_temp.append(__kijunDirection)
                list_temp.append(__kijunConsecutiveCount)
                list_result.append(list_temp)
        self.resultList = list_result
        return list_result

    def exportResult(self, list_result):
        df_result = pd.DataFrame(
            list_result,
            columns=['Date', 'Symbol', 'Name', 'Direction', 'Count'])
        df_result.sort_values(by=['Count'], inplace=True)
        self.__createDataFolder(self.outputPath)
        df_result.to_csv(self.outputPath +
                         self.assetClassName.replace(" ", "") + '.csv',
                         index=False)
        self.resultDataFrame = df_result
        return df_result


class Control(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def getData(self):
        return self.model.getLatestResultFromEachDataFrame()

    def exportResult(self, __list_result):
        return self.model.exportResult(__list_result)

    def main(self):
        print("*************************************************")
        list_result = self.getData()
        # print(list_result)
        df_result = self.exportResult(list_result)

        # print(df_result)
        # return df_result

        self.view.showResultKCount(self.model.resultDataFrame)
        print(f"aggregator {self.model.assetClassName}.csv is created")


class View(object):

    @staticmethod
    def showResultKCount(__df):
        print(__df)


if __name__ == "__main__":
    _model = Model('data/futurescurrency/d/', 'asset_list/FuturesCurrency.csv',
                   'Futures-D')
    _control = Control(_model, View())
    _control.main()
