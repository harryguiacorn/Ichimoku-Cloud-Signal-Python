import logging
from abc import ABC, abstractmethod

import pandas as pd

logger = logging.getLogger(__name__)


class DataOHLC(ABC):
    @abstractmethod
    def readLocalCsvData(self, symbols, csvPath):
        pass


class DataChikouSignal(DataOHLC):
    def __init__(self, symbol, csvPath, use_datetime_format=False):
        self.symbol = symbol
        self.csvPath = csvPath
        self.use_datetime_format = use_datetime_format

    def check_yfinance_format(self, path, first_column):
        data = pd.read_csv(path, header=[0])
        if data.columns[0] == first_column:
            return data

        data = pd.read_csv(path, header=[0, 1])
        data.columns = data.columns.droplevel(1)
        first_cell_third_row = pd.read_csv(path, skiprows=2).columns[0]
        data.columns.values[0] = first_cell_third_row
        return data.drop(data.index[0])

    def setup(self, first_column, date_column, output_suffix):
        path = self.csvPath + self.symbol + "_ichimokuTapy.csv"
        try:
            data = self.check_yfinance_format(path, first_column)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            logger.warning("Error: %s not found or empty", path)
            return

        if date_column not in data.columns:
            return

        data.index = data[date_column]
        data["Chikou Signal"] = self.getChikouSignal(
            data["Close"], data["High"], data["Low"]
        )
        data["Chikou Signal Count"], data["Chikou State"] = (
            self.getChikouState(data["Chikou Signal"])
        )
        data["Chikou Signal"] = data["Chikou Signal"].astype("int64")
        data["Chikou Signal Count"] = data["Chikou Signal Count"].astype(
            "int64"
        )
        header = [
            date_column,
            "Chikou Signal",
            "Chikou Signal Count",
            "Chikou State",
        ]
        data.to_csv(
            self.csvPath + self.symbol + output_suffix,
            columns=header,
            index=False,
        )

    def getChikouSignal(self, close, high, low, kijun_period=26):
        signal = []
        for index in range(len(close)):
            historical_index = index - kijun_period
            if historical_index < 0:
                signal.append(0)
            elif close.iloc[index] > high.iloc[historical_index]:
                signal.append(1)
            elif close.iloc[index] < low.iloc[historical_index]:
                signal.append(-1)
            else:
                signal.append(0)
        return signal

    def getChikouState(self, signals):
        counts = []
        states = []
        previous_direction = 0
        periods = 0
        for signal in signals:
            if pd.isna(signal):
                signal = 0

            if signal in (1, -1) and signal != previous_direction:
                previous_direction = int(signal)
                periods = 1
            elif previous_direction != 0:
                periods += 1
            else:
                periods = 0

            counts.append(periods * previous_direction)
            states.append(self.getChikouStateLabel(previous_direction))
        return counts, states

    def getChikouStateLabel(self, direction):
        return {
            1: "above chikou",
            -1: "below chikou",
        }.get(direction, "neutral chikou")

    def readLocalCsvData(self, symbols, csvPath):
        pass

    def main(self):
        if self.use_datetime_format:
            self.setup("Datetime", "Datetime", "_chikouCount.csv")
        else:
            self.setup("Date", "Date", "_chikouCount.csv")


class Model(object):
    def __init__(self, csvPath, assetListPath, use_datetime_format=False):
        self.csvPath = csvPath
        self.assetListPath = assetListPath
        self.use_datetime_format = use_datetime_format

    def readAssetList(self):
        data = pd.read_csv(self.assetListPath)
        data = data.dropna(subset=["symbol"])
        symbols = data["symbol"].astype(str).str.replace("/", "", regex=False)
        return symbols.str.strip()[
            ~symbols.str.lower().str.startswith("nan")
        ].tolist()


class Control(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def main(self):
        for symbol in self.model.readAssetList():
            DataChikouSignal(
                symbol, self.model.csvPath, self.model.use_datetime_format
            ).main()


class View(object):
    pass
