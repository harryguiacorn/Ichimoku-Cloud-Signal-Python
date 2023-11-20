import pandas as pd
from abc import abstractclassmethod, ABC


class DataOHLC(ABC):
    @abstractclassmethod
    def readLocalCsvData(self, symbols, __csvPath):
        pass


class DataTKxSignal(DataOHLC):
    def __init__(self, __symbol, __csvPath, __isIntraday=False):
        self.symbol = __symbol
        self.csvPath = __csvPath
        self.isIntraday = __isIntraday

    def setupPd_intraday(self, csvSuffix="_tkx.csv", folderPath="data/"):
        # pd.set_option("display.max_rows", None)  # print every row for debug
        # pd.set_option(
        #     "display.max_columns", None
        # )  # print every column for debug

        try:
            __path = self.csvPath + self.symbol + csvSuffix
            __data = pd.read_csv(__path)
            if __data.empty:  # Check if the DataFrame is empty
                print("CSV file is empty", __path)
            else:
                # print(__path)
                # print(__data.Datetime)
                __data.index = __data.Datetime
                __data["Returns"] = self.getReturn(
                    __data["Close"], __data["Close"].shift(1)
                )
                __data["TKx Signal"] = self.getTKxDirection(
                    __data["tenkan_sen"], __data["kijun_sen"]
                )
                __data["TKx Signal Count"] = self.getTKxSignalCount(
                    __data["TKx Signal"]
                )
                self.setColumnsSaveCsv_intraday(__data)
                # print(__data)
        except pd.errors.EmptyDataError:
            print("CSV file is empty", __path)
        except FileNotFoundError:
            print(f"Error: {__path} not found")

    def setupPd(self, csvSuffix="_tkx.csv", folderPath="data/"):
        # pd.set_option("display.max_rows", None)  # print every row for debug
        # pd.set_option(
        #     "display.max_columns", None
        # )  # print every column for debug
        try:
            __path = self.csvPath + self.symbol + csvSuffix
            __data = pd.read_csv(__path)
            if __data.empty:  # Check if the DataFrame is empty
                print("CSV file is empty", __path)
            else:
                # print(__data.Date)
                __data.index = __data.Date
                __data["Returns"] = self.getReturn(
                    __data["Close"], __data["Close"].shift(1)
                )
                __data["TKx Signal"] = self.getTKxDirection(
                    __data["tenkan_sen"], __data["kijun_sen"]
                )
                __data["TKx Signal Count"] = self.getTKxSignalCount(
                    __data["TKx Signal"]
                )
                self.setColumnsSaveCsv(__data)
        except pd.errors.EmptyDataError:
            print("CSV file is empty", __path)
        except FileNotFoundError:
            print(f"Error: {__path} not found")

    def getTKxSignalCount(self, __tkxDirectionList):
        __newList = []
        __tkxDirectionCount = None
        __curKijunDirection = None
        for __i in range(len(__tkxDirectionList)):
            if pd.isna(__tkxDirectionList.iloc[__i]):
                __tkxDirectionCount = __tkxDirectionList.iloc[__i]
            elif __curKijunDirection is None:
                __curKijunDirection = __tkxDirectionList.iloc[__i]
                __tkxDirectionCount = 1
            elif not __tkxDirectionList.iloc[__i] == __curKijunDirection:
                __curKijunDirection = -__curKijunDirection
                __tkxDirectionCount = 1
            else:
                __tkxDirectionCount += 1

            __newList.append(__tkxDirectionCount)
        return __newList

    def getTKxDirection(self, __curKijun, __preKijun):
        __data = []
        __curDirection = None
        for __i in range(len(__preKijun)):
            if pd.isna(__preKijun.iloc[__i]):
                __data.append(__preKijun.iloc[__i])
            elif pd.isna(__curKijun.iloc[__i]):
                __data.append(__curKijun.iloc[__i])
            elif __curKijun.iloc[__i] > __preKijun.iloc[__i]:
                __curDirection = 1
                __data.append(1)
            elif __curKijun.iloc[__i] < __preKijun.iloc[__i]:
                __curDirection = -1
                __data.append(-1)
            else:
                __data.append(__curDirection)
        return __data

    def getReturn(self, __curClose, __preClose):
        return __curClose / __preClose - 1

    def setColumnsSaveCsv(self, __data, csvSuffix="_tkxCount.csv"):
        header = ["Date", "TKx Signal", "TKx Signal Count"]
        __data.to_csv(
            self.csvPath + self.symbol + csvSuffix, columns=header, index=False
        )

    def setColumnsSaveCsv_intraday(self, __data, csvSuffix="_tkxCount.csv"):
        header = ["Datetime", "TKx Signal", "TKx Signal Count"]
        __data.to_csv(
            self.csvPath + self.symbol + csvSuffix, columns=header, index=False
        )

    def readLocalCsvData(self, symbols, __csvPath):
        pass

    def main(self):
        if self.isIntraday is False:
            # print(self.symbol, "N-------------", self.isIntraday)
            self.setupPd(
                "_ichimokuTapy.csv"
            )  # _ichimokuPlotly _ichimokuTapy _ichimokuFinta
        else:
            # print(self.symbol, "Y-------------", self.isIntraday)
            self.setupPd_intraday(
                "_ichimokuTapy.csv"
            )  # _ichimokuPlotly _ichimokuTapy _ichimokuFinta


class Model(object):
    def __init__(
        self,
        __csvPath,
        __assetListPath,
        # __csvColumnPrefix="",
        __isIntraday=False,
    ):
        self.csvPath = __csvPath
        self.assetListPath = __assetListPath
        # self.csvColumnPrefix = __csvColumnPrefix
        self.isIntraday = __isIntraday
        self.symbols = None
        self.dataOHLC = None

    @property
    def isIntraday(self):
        return self.__isIntraday

    @isIntraday.setter
    def isIntraday(self, __isIntraday):
        self.__isIntraday = __isIntraday

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

    def readAssetList(self, __csvPath, __colName="symbol"):
        df = pd.read_csv(__csvPath)
        # print(df.to_string())
        l_symbol = df[__colName].tolist()
        self.symbols = l_symbol
        return l_symbol

    def readLocalCsvData(self, symbols, __csvPath):
        __dict_df = {}
        for __symbol in symbols:
            try:
                __filePath = __csvPath + __symbol + ".csv"
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
            # print(__symbol, self.csvPath)
            dataP = DataTKxSignal(__symbol, self.csvPath, self.isIntraday)
            # print("*************", self.isIntraday)
            dataP.main()
        print("TKx count csv files are created")


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
        print(
            "-------------------- Generating TKx Signals --------------------"
        )
        self.getAssetList()
        self.getBatchLocalData()
        self.getIndividualSymbolData()


class View(object):
    def __init__(self):
        pass


if __name__ == "__main__":
    _model = Model("data/futurescurrency/w/", "asset_list/FuturesCurrency.csv")
    _control = Control(_model, View())
    _control.main()
