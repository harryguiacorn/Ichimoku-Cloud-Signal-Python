import datetime
import pandas as pd
from finta import TA
from tapy import Indicators
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from src.mvc import Util


class Model(object):
    def __init__(
        self,
        __csvPath="data/",
        __assetListPath="",
        __interval="",
        __lookbackPeriod="",
        __bGetLatestDataFromYahoo=False,
    ):
        """__csvPath points to csv files for asset class
        __assetListPath points to the path for asset list"""
        self.csvPath = __csvPath
        self.assetListPath = __assetListPath
        self.interval = __interval
        self.bGetLatestDataFromYahoo = __bGetLatestDataFromYahoo
        self.symbols = None
        self.dataOHLC = None
        self.interval = __interval
        self.lookbackPeriod = __lookbackPeriod

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
    def dataOHLC(self):
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
    def bGetLatestDataFromYahoo(self):
        return self.__bGetLatestDataFromYahoo

    @bGetLatestDataFromYahoo.setter
    def bGetLatestDataFromYahoo(self, __b):
        self.__bGetLatestDataFromYahoo = __b

    def readAssetList(self, __csvPath, __colName="symbol"):
        df = pd.read_csv(__csvPath)

        # Remove any slashes from the 'symbol' column
        df[__colName] = df[__colName].str.replace("/", "", regex=False)

        print("----------- Reading symbols -----------")
        print("readAssetList path:", __csvPath, end="\n")
        print(df.values.ravel().tolist(), end="\n\n")
        # print(df[__colName])
        l_symbol = df[__colName].tolist()
        self.symbols = l_symbol
        return l_symbol

    def getDataOHLC(self):
        # __dict_lookbackPeriodConvertInt = {'h': 1, 'd': 1, 'w': 7, 'm': 31}
        if self.bGetLatestDataFromYahoo:
            print("----------- Downloading from Yahoo -----------")
            print(self.symbols, self.lookbackPeriod, self.interval)
            # method 1. grab latest data from yahoo finance
            # using Pandas Datareader (now defunct)
            self.dataOHLC = self.getLatestDataFromYahooByYFinance(
                self.symbols, self.lookbackPeriod, self.interval
            )
            return self.dataOHLC
        else:
            # method 2. grab data from local raw csv files to
            # prevent IP getting blocked by Yahoo servers
            self.dataOHLC = self.readLocalCsvData(self.symbols, self.csvPath)
            return self.dataOHLC
        print("csv files are downloaded")

    def getLatestDataFromYahooByYFinance(
        self, symbols, __lookbackPeriods, __interval
    ):
        __dict_df = {}
        for __symbol in symbols:
            try:
                print(
                    "getLatestDataFromYahooByYFinance download",
                    __symbol,
                    __lookbackPeriods,
                    __interval,
                )
                data = yf.download(
                    tickers=__symbol,
                    period=__lookbackPeriods,
                    interval=__interval,
                )

                # clean data
                df_dropped_rows = data.dropna()

                # print("getLatestDataFromYahooByYFinance", df_dropped_rows)

                __dict_df[__symbol] = df_dropped_rows

                __path = self.csvPath + __symbol + ".csv"
                df_dropped_rows.to_csv(__path)
                print(f"{symbols.index(__symbol)} {__symbol} -> {__path}")
            except Exception as e:
                # raise Exception("Error: ", __symbol, " e.args: ",e.args)
                print(f"Error: {__symbol}: {e.args}")
                continue
        return __dict_df

    # Using Pandas Datareader until Yahoo finance blocked it
    def getLatestDataFromYahoo(
        self, symbols, __lookbackDays=3 * 365, __toDate="today"
    ):
        startDate = (
            datetime.datetime.now() - datetime.timedelta(days=__lookbackDays)
        ).strftime("%Y-%m-%d")
        endData = __toDate

        __dict_df = {}
        for __symbol in symbols:
            try:
                data = pdr.get_data_yahoo(
                    __symbol, startDate, endData, interval=self.interval
                )

                __dict_df[__symbol] = data
                __path = self.csvPath + __symbol + ".csv"
                data.to_csv(__path)
                print(f"{symbols.index(__symbol)} {__symbol} -> {__path}")
            except Exception as e:
                # raise Exception("Error: ", __symbol, " e.args: ",e.args)
                print(f"Error: {__symbol}: {e.args}")
                continue
        return __dict_df

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

    def createIchimokuData(self):
        print("\n----------- Creating Ichimoku Data -----------")
        # method 1. create Ichimoku data using tapy
        DictDataIchinokuTapy = self.createIchimokuDataTapy(self.dataOHLC)
        print("Ichimoku columns added to csv\n")
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
        self.model.readAssetList(self.model.assetListPath)

    def showAssetList(self):
        __dict_symbols = self.model.readAssetList(self.model.assetListPath)
        self.view.showAssetList(__dict_symbols)

    def main(self):
        # initializing Parameters
        Util.create_folder(self.model.csvPath)

        # symbols = self.readAssetList(self.assetListPath)
        self.getAssetList()

        self.model.getDataOHLC()

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
        "data/dowjones30/d/", "asset_list/DowJones30.csv", "1w", "max", True
    )
    _model = Model(
        "data/dowjones30/w/", "asset_list/DowJones30.csv", "1wk", "max", True
    )
    _control = Control(_model, View())
    _control.main()
    _control.showAssetList()
