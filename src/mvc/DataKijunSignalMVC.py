from logging import exception
import pandas as pd
from abc import abstractclassmethod, ABC


class DataOHLC(ABC):

    @abstractclassmethod
    def readLocalCsvData(self, symbols, __csvPath):
        pass


class DataKijunSignal(DataOHLC):

    def __init__(self, __symbol, __csvPath):
        self.symbol = __symbol
        self.csvPath = __csvPath

    def setupPd(self, csvSuffix='_cloud.csv', folderPath='data/'):
        pd.set_option('display.max_rows', None)  # print every row for debug
        pd.set_option('display.max_columns',
                      None)  # print every column for debug
        try:
            __path = self.csvPath + self.symbol + csvSuffix
            __data = pd.read_csv(__path)
            __data.index = __data.Date
            __data['Returns'] = self.getReturn(__data['Close'],
                                            __data['Close'].shift(1))
            __data['Kijun Direction'] = self.getKijunDirection(
                __data['kijun_sen'], __data['kijun_sen'].shift(1))
            __data['Kijun Signal Count'] = self.getKijunSignalCount(
                __data['Kijun Direction'])
            self.setColumnsSaveCsv(__data)
        except FileNotFoundError:
            print(f'Error: {__path} not found')
            
    def getKijunSignalCount(self, __kijunDirectionList):
        __newList = []
        __kijunDirectionCount = None
        __curKijunDirection = None
        for __i in range(len(__kijunDirectionList)):
            if pd.isna(__kijunDirectionList[__i]):
                __kijunDirectionCount = __kijunDirectionList[__i]
            elif __curKijunDirection == None:
                __curKijunDirection = __kijunDirectionList[__i]
                __kijunDirectionCount = 1
            elif not __kijunDirectionList[__i] == __curKijunDirection:
                __curKijunDirection = -__curKijunDirection
                __kijunDirectionCount = 1
            else:
                __kijunDirectionCount += 1

            __newList.append(__kijunDirectionCount)
        return __newList

    def getKijunDirection(self, __curKijun, __preKijun):
        __data = []
        __curDirection = None
        for __i in range(len(__preKijun)):
            if pd.isna(__preKijun[__i]):
                __data.append(__preKijun[__i])
            elif pd.isna(__curKijun[__i]):
                __data.append(__curKijun[__i])
            elif __curKijun[__i] > __preKijun[__i]:
                __curDirection = 1
                __data.append(1)
            elif __curKijun[__i] < __preKijun[__i]:
                __curDirection = -1
                __data.append(-1)
            else:
                __data.append(__curDirection)
        return __data

    def getReturn(self, __curClose, __preClose):
        return __curClose / __preClose - 1

    def setColumnsSaveCsv(self, __data, csvSuffix='_kijunCount.csv'):
        header = ["Date", "Kijun Direction", "Kijun Signal Count"]
        __data.to_csv(self.csvPath + self.symbol + csvSuffix,
                      columns=header,
                      index=False)

    def readLocalCsvData(self, symbols, __csvPath):
        pass

    def main(self):
        self.setupPd('_ichimokuTapy.csv'
                     )  # _ichimokuPlotly _ichimokuTapy _ichimokuFinta


class Model(object):

    def __init__(self, __csvPath, __assetListPath):
        self.csvPath = __csvPath
        self.assetListPath = __assetListPath
        self.symbols = None
        self.dataOHLC = None

    @property
    def symbol(self):
        return self.__symbol

    @symbol.setter
    def symbol(self, __symbol):
        self.__symbol = __symbol

    @property
    def csvPath(self):
        return self.__csvPath

    @csvPath.setter
    def csvPath(self, __csvPath):
        self.__csvPath = __csvPath

    @property
    def assetListPath(self):
        return self.__assetListPath

    @assetListPath.setter
    def assetListPath(self, __assetListPath):
        self.__assetListPath = __assetListPath

    def readAssetList(self, __csvPath, __colName='symbol'):
        df = pd.read_csv(__csvPath)
        # print(df.to_string())
        l_symbol = df[__colName].tolist()
        self.symbols = l_symbol
        return l_symbol

    def readLocalCsvData(self, symbols, __csvPath):
        __dict_df = {}
        for __symbol in symbols:
            try:
                __filePath = __csvPath + __symbol + '.csv'
                __df = pd.read_csv(__filePath)
                __dict_df[__symbol] = __df
            except FileNotFoundError:
                print(f"Error: {__filePath} not found")
                continue
        return __dict_df

    def getBatchLocalData(self):
        self.dataOHLC = self.readLocalCsvData(self.symbols, self.csvPath)

    def getIndividualSymbolData(self):
        for __symbol, __value in self.dataOHLC.items():
            print(__symbol, self.csvPath)
            dataP = DataKijunSignal(__symbol, self.csvPath)
            dataP.main()
        print("Kijun count csv files are created")


class Control(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def getAssetList(self):
        self.model.readAssetList(self.model.assetListPath)

    def showAssetList(self):
        __dict_symbols = self.model.readAssetList(self.model.assetListPath)
        self.view.showAssetList(__dict_symbols)

    def getDataOHLC(self):
        self.model.getDataOHLC()

    def getBatchLocalData(self):
        self.model.getBatchLocalData()

    def getIndividualSymbolData(self):
        self.model.getIndividualSymbolData()

    def main(self):
        print("---------------------------------")
        self.getAssetList()
        self.getBatchLocalData()
        self.getIndividualSymbolData()


class View(object):

    def __init__(self):
        pass


if __name__ == "__main__":
    _model = Model('data/futurescurrency/w/', 'asset_list/FuturesCurrency.csv')
    _control = Control(_model, View())
    _control.main()
