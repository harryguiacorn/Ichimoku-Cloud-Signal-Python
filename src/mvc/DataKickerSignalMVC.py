import pandas as pd
from abc import abstractclassmethod, ABC


class DataOHLC(ABC):
    @abstractclassmethod
    def readLocalCsvData(self, symbols, __csvPath):
        pass


class DataKickerSignal(DataOHLC):
    def __init__(self, __symbol, __csvPath):
        self.symbol = __symbol
        self.csvPath = __csvPath

    def setupPd(self, csvSuffix=".csv", minBodyPerc1=0, minBodyPerc2=0):
        """
        param minBodyPerc1: Minimum body to candle range percentage
        for left candle formation, default is 0
        param minBodyPerc2: Minimum body to candle range percentage
        for right candle formation, default is 0
        """
        pd.set_option("display.max_rows", None)  # print every row for debug
        pd.set_option(
            "display.max_columns", None
        )  # print every column for debug
        try:
            __path = self.csvPath + self.symbol + csvSuffix
            __data = pd.read_csv(__path)
            __data.index = __data.Date
            # __data['Returns'] = self.getReturn(__data['Close'],
            #                                    __data['Close'].shift(1))
            __data["Kicker"] = self.getKickerSignal(
                __data, minBodyPerc1, minBodyPerc2
            )
            self.cleanupDF(__data)

            # print(__data)
            self.setColumnsSaveCsv(__data)
        except FileNotFoundError:
            print(f"Error: {__path} not found")

    def cleanupDF(
        self, __data
    ):  # keep date which kicker signal is either -1 or 1
        __data.drop(__data[(__data["Kicker"] == 0)].index, inplace=True)

    def getKickerSignal(self, __data, minBodyPerc1=0, minBodyPerc2=0):
        __lKicker = []
        for i in range(len(__data)):
            __signal = 0
            if i > 0:
                __preClose = __data["Close"][i - 1]
                __preOpen = __data["Open"][i - 1]
                __preHigh = __data["High"][i - 1]
                __preLow = __data["Low"][i - 1]
                __curClose = __data["Close"][i]
                __curOpen = __data["Open"][i]
                __curHigh = __data["High"][i]
                __curLow = __data["Low"][i]
                __preBodyPerc = abs(
                    (__preClose - __preOpen) / (__preHigh - __preLow)
                )
                __curBodyPerc = abs(
                    (__curClose - __curOpen) / (__curHigh - __curLow)
                )
                # print(__preBodyPerc, __curBodyPerc)
                if (
                    __preClose < __preOpen
                    and __curClose > __curOpen
                    and __preOpen < __curOpen
                    and __preBodyPerc > minBodyPerc1
                    and __curBodyPerc > minBodyPerc2
                ):
                    __signal = 1
                elif (
                    __preClose > __preOpen
                    and __curClose < __curOpen
                    and __preOpen > __curOpen
                    and __preBodyPerc > minBodyPerc1
                    and __curBodyPerc > minBodyPerc2
                ):
                    __signal = -1
            __lKicker.append(__signal)
        # print(__lKicker)
        return __lKicker

    def getReturn(self, __curClose, __nxtClose):
        # print(__curClose, __nxtClose)
        return __curClose / __nxtClose - 1

    def setColumnsSaveCsv(self, __data, csvSuffix="_kicker.csv"):
        header = ["Date", "Kicker"]
        __data.to_csv(
            self.csvPath + self.symbol + csvSuffix, columns=header, index=False
        )

    def readLocalCsvData(self, symbols, __csvPath):
        pass

    def main(self):
        self.setupPd(".csv", 0, 0)


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
            dataP = DataKickerSignal(__symbol, self.csvPath)
            dataP.main()


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
        print("********* Creating Kicker Signals *********")
        self.getAssetList()
        self.getBatchLocalData()
        self.getIndividualSymbolData()
        print(f"Populated kicker csv {self.model.csvPath}")


class View(object):
    def __init__(self):
        pass


if __name__ == "__main__":
    _model = Model("data/dowjones30/d/", "asset_list/DowJones30.csv")
    _control = Control(_model, View())
    _control.main()
