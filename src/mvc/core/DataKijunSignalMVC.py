import pandas as pd
from abc import abstractclassmethod, ABC


class DataOHLC(ABC):
    @abstractclassmethod
    def readLocalCsvData(self, symbols, __csvPath):
        pass


class DataKijunSignal(DataOHLC):
    def __init__(self, __symbol, __csvPath, __use_datetime_format=False):
        self.symbol = __symbol
        self.csvPath = __csvPath
        self.use_datetime_format = __use_datetime_format

    def setupPd_use_datetime_format(
        self, csvSuffix="_kijun.csv", folderPath="data/"
    ):
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
                ).round(4)
                # print(__data["Returns"])
                __data["Kijun Direction"] = self.getKijunDirection(
                    __data["kijun_sen"], __data["kijun_sen"].shift(1)
                )
                __data["Kijun Signal Count"] = self.getKijunSignalCount(
                    __data["Kijun Direction"]
                )

                # drop chikou_span because it creates na values
                # for 26 periods from last date
                __data.drop("chikou_span", axis=1, inplace=True)
                __data = __data.dropna()

                # convert float64 to int64
                __data["Kijun Direction"] = __data["Kijun Direction"].astype(
                    "int64"
                )
                __data["Kijun Signal Count"] = __data[
                    "Kijun Signal Count"
                ].astype("int64")

                self.setColumnsSaveCsv_use_datetime_format(__data)
                # print(__data)
        except pd.errors.EmptyDataError:
            print("CSV file is empty", __path)
        except FileNotFoundError:
            print(f"Error: {__path} not found")

    def setupPd(self, csvSuffix="_kijun.csv", folderPath="data/"):
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
                ).round(4)
                __data["Kijun Direction"] = self.getKijunDirection(
                    __data["kijun_sen"], __data["kijun_sen"].shift(1)
                )
                __data["Kijun Signal Count"] = self.getKijunSignalCount(
                    __data["Kijun Direction"]
                )

                # drop chikou_span because it creates na values
                # for 26 periods from last date
                __data.drop("chikou_span", axis=1, inplace=True)
                __data = __data.dropna()

                # convert float64 to int64
                __data["Kijun Direction"] = __data["Kijun Direction"].astype(
                    "int64"
                )
                __data["Kijun Signal Count"] = __data[
                    "Kijun Signal Count"
                ].astype("int64")

                self.setColumnsSaveCsv(__data)
        except pd.errors.EmptyDataError:
            print("CSV file is empty", __path)
        except FileNotFoundError:
            print(f"Error: {__path} not found")

    def getKijunSignalCount(self, __kijunDirectionList):
        __newList = []
        __kijunDirectionCount = None
        __curKijunDirection = None
        for __i in range(len(__kijunDirectionList)):
            if pd.isna(__kijunDirectionList.iloc[__i]):
                __kijunDirectionCount = __kijunDirectionList.iloc[__i]
            elif __curKijunDirection is None:
                __curKijunDirection = __kijunDirectionList.iloc[__i]
                __kijunDirectionCount = 1
            elif not __kijunDirectionList.iloc[__i] == __curKijunDirection:
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

    def setColumnsSaveCsv(self, __data, csvSuffix="_kijunCount.csv"):
        header = ["Date", "Kijun Direction", "Kijun Signal Count"]
        __data.to_csv(
            self.csvPath + self.symbol + csvSuffix, columns=header, index=False
        )

    def setColumnsSaveCsv_use_datetime_format(
        self, __data, csvSuffix="_kijunCount.csv"
    ):
        header = ["Datetime", "Kijun Direction", "Kijun Signal Count"]
        __data.to_csv(
            self.csvPath + self.symbol + csvSuffix, columns=header, index=False
        )

    def readLocalCsvData(self, symbols, __csvPath):
        pass

    def main(self):
        if self.use_datetime_format is False:
            self.setupPd(
                "_ichimokuTapy.csv"
            )  # _ichimokuPlotly _ichimokuTapy _ichimokuFinta
        else:
            self.setupPd_use_datetime_format(
                "_ichimokuTapy.csv"
            )  # _ichimokuPlotly _ichimokuTapy _ichimokuFinta


class Model(object):
    def __init__(
        self, __csvPath, __assetListPath, __use_datetime_format=False
    ):
        self.csvPath = __csvPath
        self.assetListPath = __assetListPath
        self.use_datetime_format = __use_datetime_format
        self.symbols = None
        self.dataOHLC = None

    @property
    def use_datetime_format(self):
        return self.__use_datetime_format

    @use_datetime_format.setter
    def use_datetime_format(self, __use_datetime_format):
        self.__use_datetime_format = __use_datetime_format

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

        # Remove any slashes from the 'symbol' column
        df[__colName] = df[__colName].str.replace("/", "", regex=False)

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
            dataP = DataKijunSignal(
                __symbol, self.csvPath, self.use_datetime_format
            )
            dataP.main()
        print("Kijun count csv files are created\n")


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
        print("-------- Generating Kijun Signals --------")
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
