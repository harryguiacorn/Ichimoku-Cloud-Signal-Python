import datetime
from genericpath import isdir
import os
import pandas as pd
from finta import TA
from tapy import Indicators
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf

from src.mvc.DataOandaAPI import DataOandaAPI


class Resampler:
    def __init__(self, ticker_symbol, data):
        self.ticker_symbol = ticker_symbol
        self.ticker = yf.Ticker(ticker_symbol)
        self.data = data
        self.resampled_data = None

    def fetch_data(self, interval="1h", period="1mo"):
        self.data = self.ticker.history(interval=interval, period=period)
        self.data.sort_index(inplace=True)
        self.data.to_csv(f"{self.ticker_symbol}-{interval}.csv")


class Model(object):
    def __init__(
        self,
        __csvPath="data/",
        __assetListPath="",
        __interval="",
        __lookbackPeriod="",
        __bGetLatestDataFromOanda=False,
        __pricingComponent="M",
    ):
        """__csvPath points to csv files for asset class
        __assetListPath points to the path for asset list"""
        self.csvPath = __csvPath
        self.assetListPath = __assetListPath
        self.interval = __interval
        self.bGetLatestDataFromOanda = __bGetLatestDataFromOanda
        self.symbols = None
        self.dataOHLC = pd.DataFrame
        self.lookbackPeriod = __lookbackPeriod
        self.pricingComponent = __pricingComponent

    @property
    def lookbackPeriod(self):
        return self.__lookbackPeriod

    @lookbackPeriod.setter
    def lookbackPeriod(self, __lookbackPeriod):
        self.__lookbackPeriod = __lookbackPeriod

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, __interval):
        self.__interval = __interval

    @property
    def dataOHLC(self) -> pd.DataFrame:
        return self.__dataOHLC

    @dataOHLC.setter
    def dataOHLC(self, __dictData):
        self.__dataOHLC = __dictData

    @property
    def csvPath(self):
        return self.__csvPath

    @csvPath.setter
    def csvPath(self, __path):
        self.__csvPath = __path

    @property
    def assetListPath(self):
        return self.__assetListPath

    @assetListPath.setter
    def assetListPath(self, __path):
        self.__assetListPath = __path

    @property
    def bGetLatestDataFromOanda(self):
        return self.__bGetLatestDataFromOanda

    @bGetLatestDataFromOanda.setter
    def bGetLatestDataFromOanda(self, __b):
        self.__bGetLatestDataFromOanda = __b

    def readAssetList(self, __csvPath, __colName="symbol"):
        df = pd.read_csv(__csvPath)
        print(f"----------- Reading symbols for {self.interval} -----------")
        print(df.to_string(), sep=",")
        # print(df[__colName])
        l_symbol = df[__colName].tolist()
        self.symbols = l_symbol
        return l_symbol

    def getDataOHLC(self):
        # __dict_lookbackPeriodConvertInt = {'h': 1, 'd': 1, 'w': 7, 'm': 31}
        if self.bGetLatestDataFromOanda:
            print("----------- Downloading from Oanda API -----------")
            # print(
            #     "getDataOHLC: ",
            #     self.symbols,
            #     self.interval,
            #     self.lookbackPeriod,
            # )
            # method 1. grab latest data from Oanda API

            self.dataOHLC = self.getLatestDataFromOandaAPI(
                self.symbols, self.lookbackPeriod, self.interval
            )
            return self.dataOHLC
        else:
            # method 2. grab data from local raw csv files to
            # prevent IP getting blocked by Yahoo servers
            self.dataOHLC = self.readLocalCsvData(self.symbols, self.csvPath)
            return self.dataOHLC

    def getLatestDataFromOandaAPI(
        self, symbols, __lookbackPeriods, __interval
    ) -> pd.DataFrame:
        __dict_df = {}
        for __symbol in symbols:
            try:
                api = DataOandaAPI()
                data = api.get_oanda_data(
                    __symbol, __lookbackPeriods, __interval
                )

                __dict_df[__symbol] = data
                __path = self.csvPath + __symbol + ".json"
                api.save_json(__path, data)
                __path = self.csvPath + __symbol + ".csv"
                api.json_to_csv(data, __path)
                # print(f"{symbols.index(__symbol)} {__symbol} -> {__path}")
            except Exception as e:
                # raise Exception("Error: ", __symbol, " e.args: ",e.args)
                print(f"Error getLatestDataFromOandaAPI: {__symbol}: {e.args}")
                continue
        return __dict_df

    def readLocalCsvData(self, symbols, __csvPath) -> pd.DataFrame:
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

    def createIchimokuData(self):
        print(
            "----------- Creating Ichimoku Data -----------"
        )
        # method 1. create Ichimoku data using tapy
        DictDataIchinokuTapy = self.createIchimokuDataTapy(self.dataOHLC)
        print("Ichimoku columns added to csv")
        # method 2. alternative method to
        # add ichimoku columns to csv using finta
        # self.createIchimokuDataFinta(DictData)
        # self.displayCharts(DictDataIchinokuTapy)
        return DictDataIchinokuTapy

    def createIchimokuDataTapy(
        self, __dict_df
    ):  # create Ichimoku data using tapy
        __dict_df_ichimoku = {}
        for __key, __df in __dict_df.items():
            # initialising indicators
            __i = Indicators(__df)
            __i.ichimoku_kinko_hyo()  # column_name_kijun_sen="K Line"
            __dataCloud = __i.df
            __dict_df_ichimoku[__key] = __dataCloud
            __dataCloud.to_csv(self.csvPath + __key + "_ichimokuTapy.csv")
        return __dict_df_ichimoku

    # create Ichimoku data using finta, this is the alternative option
    def createIchimokuDataFinta(self, __dict_df):
        for __symbol, __df in __dict_df.items():
            df = pd.read_csv(self.csvPath + __symbol + ".csv")
            TA.ICHIMOKU(df).to_csv(
                self.csvPath + __symbol + "_ichimokuFinta.csv"
            )


class View(object):
    @staticmethod
    def showAssetList(__dict_symbols):
        # print("---------------VIEW-showAssetList---------------------")
        # print(__dict_symbols)
        pass


class Control(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def getAssetList(self):
        print("readAssetList path:", self.model.assetListPath)
        self.model.readAssetList(self.model.assetListPath)

    def showAssetList(self):
        __dict_symbols = self.model.readAssetList(self.model.assetListPath)
        self.view.showAssetList(__dict_symbols)

    def main(self, resample=False):
        # initializing Parameters
        self.createDataFolder(self.model.csvPath)

        # symbols = self.readAssetList(self.assetListPath)
        self.getAssetList()
        self.model.getDataOHLC()
        return

        __df_ichimoku = self.model.createIchimokuData()

        # self.displayCharts(__df_ichimoku)

    def displayCharts(self, __data):
        for __key, __df in __data.items():
            self.displayChart(__key, __df)

    def displayChart(self, __symbol, __df):
        __df["diff"] = __df["Close"] - __df["Open"]
        __df.loc[__df["diff"] >= 0, "color"] = "green"
        __df.loc[__df["diff"] < 0, "color"] = "red"
        # print(__df.head())

        # pd.set_option("display.max_rows", None)  # print every row for debug

        fig3 = make_subplots(specs=[[{"secondary_y": True}]])

        # __Tenkan_sen = self.midPoint(__df, 9)
        # __Kijun_sen = self.midPoint(__df, 26)
        fig3.add_trace(
            go.Scatter(
                x=__df.index,
                y=__df["tenkan_sen"],
                marker_color="#e377c2",
                name="Tenkan",
            )
        )
        fig3.add_trace(
            go.Scatter(
                x=__df.index,
                y=__df["kijun_sen"],
                marker_color="blue",
                name="Kijun",
            )
        )

        fig3.add_trace(
            go.Scatter(
                x=__df.index,
                y=__df["senkou_span_a"],
                line_color="#e377c2",
                name="senkou_span_a",
            )
        )

        # print(__df['senkou_span_a'].iloc[__df.index])
        fig3.add_trace(
            go.Scatter(
                x=__df.index,
                y=__df["senkou_span_b"],
                line_color="#fee440",
                name="senkou_span_b",
                fill="tonexty",
            )
        )

        fig3.add_trace(
            go.Scatter(
                x=__df.index,
                y=__df["chikou_span"],
                marker_color="#8c564b",
                name="chikou_span",
                mode="markers",
            )
        )
        fig3.add_trace(
            go.Bar(
                x=__df.index,
                y=__df["Volume"],
                name="Volume",
                marker={"color": __df["color"]},
            ),
            secondary_y=True,
        )
        fig3.add_trace(
            go.Candlestick(
                x=__df.index,
                open=__df["Open"],
                high=__df["High"],
                low=__df["Low"],
                close=__df["Close"],
                name="Price",
            )
        )

        fig3.update_yaxes(range=[0, 700000000], secondary_y=True)
        fig3.update_yaxes(visible=False, secondary_y=True)
        fig3.update_layout(
            xaxis={"type": "category"}, xaxis_rangeslider_visible=True
        )  # hide range slider
        fig3.update_layout(title={"text": __symbol, "x": 0.5})
        fig3.update_xaxes(
            rangebreaks=[
                dict(bounds=["sat", "sun"]),  # hide weekends
                # for hourly chart, hide non-trading hours (24hr format)
                # dict(bounds=[16, 9.5], pattern='hour'),
                dict(
                    values=["2021-12-25", "2022-01-01"]
                ),  # hide Xmas and New Year
            ]
        )

        # Save the chart as an HTML file
        # fig3.write_html(f"data/charts/{__symbol}_ichimoku_cloud_chart.html")
        # fig3.show()

    def createDataFolder(self, __name="data"):
        # create data folder
        try:
            if isdir(__name) is False:
                os.makedirs(__name)
        except FileExistsError as __errFile:
            print("data folder exists", __errFile)


if __name__ == "__main__":
    print("------ __main__ -----")
    # _model = Model(
    #     "data/futurescurrency/d/",
    #     "asset_list/FuturesCurrency.csv",
    #     "d",
    #     365,
    #     True,
    # )
    # _control = Control(_model, View())
    # _control.main()

    _model = Model(
        "data/dowjones30/d/", "asset_list/DowJones30.csv", "1w", "3mo", True
    )
    _model = Model(
        "data/dowjones30/w/", "asset_list/DowJones30.csv", "1wk", "5y", True
    )
    _control = Control(_model, View())
    _control.main()
    _control.showAssetList()
