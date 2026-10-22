import numpy as np
import pandas as pd
from abc import abstractclassmethod, ABC
import logging

from cloud_signal.mvc.core._csv_utils import write_latest_row

logger = logging.getLogger(__name__)


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
        # pd.set_option("display.max_rows", None)  # print every row for debug
        # pd.set_option(
        #     "display.max_columns", None
        # )  # print every column for debug
        try:
            __path = self.csvPath + self.symbol + csvSuffix
            __data = pd.read_csv(__path)
            if __data.empty:  # Check if the DataFrame is empty
                logger.info(f"CSV file is empty{__path}")
            else:
                # Robustly determine the date column. Some CSVs may use 'Date', 'date',
                # or have the date saved as the first/unnamed column. Ensure a
                # `Date` column exists and parse it to datetime before setting index.
                date_col = None
                cols_lower = [c.lower() for c in __data.columns]
                if "date" in __data.columns:
                    date_col = "date"
                elif "Date" in __data.columns:
                    date_col = "Date"
                elif "date" in cols_lower:
                    # pick the column whose lower-case name matches 'date'
                    for c in __data.columns:
                        if c.lower() == "date":
                            date_col = c
                            break
                else:
                    # fallback: use first column (often it's the date or an unnamed index)
                    date_col = __data.columns[0]

                # Normalize into a 'Date' column so downstream code can rely on it
                if date_col != "Date":
                    __data["Date"] = __data[date_col]

                # Try parsing dates; if parsing fails, leave values as-is but avoid AttributeError
                try:
                    __data["Date"] = pd.to_datetime(
                        __data["Date"], errors="coerce", format="mixed"
                    )
                except Exception:
                    logger.debug(
                        f"Failed to parse dates for {__path} in column {date_col}"
                    )

                if __data["Date"].isnull().all():
                    # If no valid dates were parsed, keep original values as strings to avoid attribute errors
                    __data["Date"] = __data["Date"].astype(str)

                __data.index = __data["Date"]

                # Ensure numeric columns are numeric types so arithmetic works
                for _col in ("Open", "High", "Low", "Close"):
                    if _col in __data.columns:
                        __data[_col] = pd.to_numeric(__data[_col], errors="coerce")
                # __data['Returns'] = self.getReturn(__data['Close'],
                #                                    __data['Close'].shift(1))
                __data["Kicker"] = self.getKickerSignal(
                    __data, minBodyPerc1, minBodyPerc2
                )
                self.cleanupDF(__data)

                # print(__data)
                self.setColumnsSaveCsv(__data)
        except pd.errors.EmptyDataError:
            logger.info(f"CSV file is empty{__path}")
        except FileNotFoundError:
            logger.info(f"Error: {__path} not found")

    def cleanupDF(
        self, __data
    ):  # keep date which kicker signal is either -1 or 1
        __data.drop(__data[(__data["Kicker"] == 0)].index, inplace=True)

    def getKickerSignal(self, __data, minBodyPerc1=0, minBodyPerc2=0):
        close = __data["Close"].to_numpy()
        open_ = __data["Open"].to_numpy()
        high = __data["High"].to_numpy()
        low = __data["Low"].to_numpy()

        previous_range = high[:-1] - low[:-1]
        current_range = high[1:] - low[1:]
        previous_body = np.divide(
            np.abs(close[:-1] - open_[:-1]),
            previous_range,
            out=np.zeros_like(previous_range, dtype=float),
            where=previous_range != 0,
        )
        current_body = np.divide(
            np.abs(close[1:] - open_[1:]),
            current_range,
            out=np.zeros_like(current_range, dtype=float),
            where=current_range != 0,
        )

        bullish = (
            (close[:-1] < open_[:-1])
            & (close[1:] > open_[1:])
            & (open_[:-1] < open_[1:])
            & (previous_body > minBodyPerc1)
            & (current_body > minBodyPerc2)
        )
        bearish = (
            (close[:-1] > open_[:-1])
            & (close[1:] < open_[1:])
            & (open_[:-1] > open_[1:])
            & (previous_body > minBodyPerc1)
            & (current_body > minBodyPerc2)
        )
        signals = np.zeros(len(close), dtype="int64")
        signals[1:] = np.where(bullish, 1, np.where(bearish, -1, 0))
        return signals.tolist()

    def getReturn(self, __curClose, __nxtClose):
        # print(__curClose, __nxtClose)
        return __curClose / __nxtClose - 1

    def setColumnsSaveCsv(self, __data, csvSuffix="_kicker.csv"):
        header = ["Date", "Kicker"]
        __data.to_csv(
            self.csvPath + self.symbol + csvSuffix, columns=header, index=False
        )
        write_latest_row(
            __data[header], self.csvPath + self.symbol + csvSuffix
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
                logger.info(f"Error: {__filePath} not found")
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
        logger.info("----------- Creating Kicker Signals -----------")
        self.getAssetList()
        self.getBatchLocalData()
        self.getIndividualSymbolData()
        logger.info(f"Populated kicker csv {self.model.csvPath}", "\n\n")


class View(object):
    def __init__(self):
        pass


if __name__ == "__main__":
    _model = Model("data/dowjones30/d/", "asset_list/DowJones30.csv")
    _control = Control(_model, View())
    _control.main()
