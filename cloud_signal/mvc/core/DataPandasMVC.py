import datetime
import os
import pandas as pd
from finta import TA
from tapy import Indicators
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from cloud_signal.mvc import Util
import logging

logger = logging.getLogger(__name__)


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

        # Remove rows where symbol is missing or empty
        df = df[df[__colName].notna()]
        df[__colName] = (
            df[__colName]
            .astype(str)
            .str.strip()
            .str.replace("/", "", regex=False)
        )
        df = df[df[__colName] != ""]

        logger.info("----------- Reading symbols -----------")
        logger.info(f"readAssetList path: {__csvPath}")
        logger.debug(df.values.ravel().tolist())
        l_symbol = df[__colName].tolist()
        self.symbols = l_symbol
        return l_symbol

    def getDataOHLC(self):
        # __dict_lookbackPeriodConvertInt = {'h': 1, 'd': 1, 'w': 7, 'm': 31}
        if self.bGetLatestDataFromYahoo:
            logger.info("----------- Downloading from Yahoo -----------")
            logger.debug(
                "symbols=%s lookback=%s interval=%s",
                self.symbols,
                self.lookbackPeriod,
                self.interval,
            )
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
        logger.info("csv files are downloaded")

    def getLatestDataFromYahooByYFinance(
        self, symbols, __lookbackPeriods, __interval
    ):
        __dict_df = {}
        batch_size = 20
        overlap_days = {
            "1h": 7,
            "60m": 7,
            "1d": 14,
            "1wk": 60,
            "1mo": 180,
        }.get(__interval, 14)
        caches = {}
        groups = {}
        for symbol_index, symbol in enumerate(symbols):
            try:
                cache_path = os.path.join(self.csvPath, symbol + ".csv")
                cached_data = self._read_market_data_cache(
                    cache_path, symbol
                )
                caches[symbol] = cached_data
                if cached_data is None or cached_data.empty:
                    request = ("period", __lookbackPeriods)
                else:
                    latest_cached_date = cached_data.index.max()
                    start_date = latest_cached_date - datetime.timedelta(
                        days=overlap_days
                    )
                    request = ("start", start_date.strftime("%Y-%m-%d"))
                groups.setdefault(request, []).append((symbol_index, symbol))
            except Exception:
                logger.exception(
                    "Unable to prepare cached data for symbol %s", symbol
                )
                caches[symbol] = None
                request = ("period", __lookbackPeriods)
                groups.setdefault(request, []).append((symbol_index, symbol))

        for request, indexed_symbols in groups.items():
            for offset in range(0, len(indexed_symbols), batch_size):
                batch = indexed_symbols[offset : offset + batch_size]
                tickers = [symbol for _, symbol in batch]
                try:
                    request_kwargs = {
                        request[0]: request[1],
                        "interval": __interval,
                    }
                    downloaded = yf.download(
                        tickers=tickers,
                        auto_adjust=True,
                        progress=False,
                        threads=False,
                        group_by="ticker",
                        **request_kwargs,
                    )
                    batch_data = self._split_yfinance_batch(downloaded, tickers)
                except Exception:
                    logger.exception(
                        "Batch download failed for %s; retrying symbols individually",
                        tickers,
                    )
                    batch_data = {}
                    for symbol in tickers:
                        try:
                            request_kwargs = {
                                request[0]: request[1],
                                "interval": __interval,
                            }
                            single = yf.download(
                                tickers=symbol,
                                auto_adjust=True,
                                progress=False,
                                **request_kwargs,
                            )
                            batch_data[symbol] = (
                                self._split_yfinance_batch(
                                    single, [symbol]
                                )[symbol]
                            )
                        except Exception:
                            logger.exception(
                                "Yahoo download failed for symbol %s", symbol
                            )
                            batch_data[symbol] = None

                for symbol_index, symbol in batch:
                    data = batch_data.get(symbol)
                    cached_data = caches[symbol]
                    __path = os.path.join(self.csvPath, symbol + ".csv")
                    if data is None or data.empty:
                        if cached_data is None or cached_data.empty:
                            logger.warning(
                                "No Yahoo data returned for symbol %s", symbol
                            )
                            continue
                        data = cached_data
                    else:
                        if isinstance(data.index, pd.DatetimeIndex):
                            data.index = pd.to_datetime(
                                data.index, utc=True, errors="coerce"
                            )
                        data = data.dropna()
                        if cached_data is not None and not cached_data.empty:
                            data = pd.concat([cached_data, data])
                            data = data.loc[
                                ~data.index.duplicated(keep="last")
                            ]
                            data = data.sort_index()

                    data = self._trim_to_lookback(data, __lookbackPeriods)
                    __dict_df[symbol] = data
                    data.to_csv(__path)
                    logger.info("%s %s -> %s", symbol_index, symbol, __path)
        return __dict_df

    @staticmethod
    def _split_yfinance_batch(data, symbols):
        if data is None or data.empty:
            return {symbol: pd.DataFrame() for symbol in symbols}
        if not isinstance(data.columns, pd.MultiIndex):
            if len(symbols) != 1:
                raise ValueError(
                    "Yahoo batch response has flat columns for multiple symbols"
                )
            return {symbols[0]: data}

        result = {}
        for symbol in symbols:
            selected = None
            for level in range(data.columns.nlevels):
                if symbol in data.columns.get_level_values(level):
                    selected = data.xs(symbol, axis=1, level=level)
                    break
            if selected is None:
                result[symbol] = pd.DataFrame(index=data.index)
            else:
                result[symbol] = selected
        return result

    @staticmethod
    def _trim_to_lookback(data, lookback):
        if data.empty or not isinstance(data.index, pd.DatetimeIndex):
            return data
        offsets = {
            "1d": pd.DateOffset(days=1),
            "5d": pd.DateOffset(days=5),
            "1mo": pd.DateOffset(months=1),
            "3mo": pd.DateOffset(months=3),
            "6mo": pd.DateOffset(months=6),
            "1y": pd.DateOffset(years=1),
            "2y": pd.DateOffset(years=2),
            "5y": pd.DateOffset(years=5),
            "10y": pd.DateOffset(years=10),
        }
        normalized_lookback = str(lookback).lower()
        index_timezone = getattr(data.index, "tz", None)
        now = pd.Timestamp.now(tz=index_timezone)
        if normalized_lookback == "ytd":
            cutoff = pd.Timestamp(now.year, 1, 1, tz=index_timezone)
        elif normalized_lookback in offsets:
            cutoff = now - offsets[normalized_lookback]
        else:
            return data
        return data.loc[data.index >= cutoff]

    @staticmethod
    def _read_market_data_cache(path, symbol):
        if not os.path.exists(path):
            return None

        cached_data = pd.read_csv(path, index_col=0)
        parsed_index = pd.to_datetime(
            cached_data.index,
            errors="coerce",
            utc=True,
            format="mixed",
        )
        if parsed_index.isna().any():
            cached_data = pd.read_csv(
                path, header=[0, 1], index_col=0
            )
            if isinstance(cached_data.columns, pd.MultiIndex):
                if symbol in cached_data.columns.get_level_values(-1):
                    cached_data = cached_data.xs(
                        symbol, axis=1, level=-1
                    )
                else:
                    cached_data.columns = cached_data.columns.droplevel(-1)
            parsed_index = pd.to_datetime(
                cached_data.index,
                errors="coerce",
                utc=True,
                format="mixed",
            )

        if parsed_index.isna().any():
            raise ValueError(f"Cached market data has invalid dates: {path}")
        cached_data.index = parsed_index
        return cached_data

    # Using Pandas Datareader until Yahoo finance blocked it
    def getLatestDataFromYahoo(
        self, symbols, __lookbackDays=3 * 365, __toDate="today"
    ):
        startDate = (
            datetime.datetime.now() - datetime.timedelta(days=__lookbackDays)
        ).strftime("%Y-%m-%d")
        endData = __toDate

        __dict_df = {}
        for symbol_index, __symbol in enumerate(symbols):
            try:
                data = pdr.get_data_yahoo(
                    __symbol, startDate, endData, interval=self.interval
                )

                __dict_df[__symbol] = data
                __path = self.csvPath + __symbol + ".csv"
                data.to_csv(__path)
                logger.info(
                    "%s %s -> %s", symbol_index, __symbol, __path
                )
            except Exception as e:
                # raise Exception("Error: ", __symbol, " e.args: ",e.args)
                logger.error("Error: %s: %s", __symbol, e.args)
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
                logger.warning("Error: %s not found", __filePath)
                continue
        return __dict_df

    def createIchimokuData(self):
        logger.info("\n----------- Creating Ichimoku Data -----------")
        # method 1. create Ichimoku data using tapy
        DictDataIchinokuTapy = self.createIchimokuDataTapy(self.dataOHLC)
        logger.info("Ichimoku columns added to csv")
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
            __dataCloud = self.createIchimokuDataTapyForSymbol(
                __key, __df
            )
            __dict_df_ichimoku[__key] = __dataCloud
        return __dict_df_ichimoku

    def createIchimokuDataTapyForSymbol(self, symbol, data):
        ichimoku_data = self.calculateIchimokuData(data)
        self.saveIchimokuData(symbol, ichimoku_data)
        return ichimoku_data

    @staticmethod
    def calculateIchimokuData(data):
        indicators = Indicators(data)
        indicators.ichimoku_kinko_hyo()
        return indicators.df

    def saveIchimokuData(self, symbol, ichimoku_data):
        ichimoku_data.to_csv(
            os.path.join(self.csvPath, symbol + "_ichimokuTapy.csv")
        )

    def getSymbolData(self, symbol):
        if self.bGetLatestDataFromYahoo:
            return self.getLatestDataFromYahooByYFinance(
                [symbol], self.lookbackPeriod, self.interval
            ).get(symbol)

        path = os.path.join(self.csvPath, symbol + ".csv")
        try:
            return pd.read_csv(path)
        except FileNotFoundError:
            logger.warning("Error: %s not found", path)
            return None

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
        Util.create_folder(self.model.csvPath)
        return self.model.readAssetList(self.model.assetListPath)

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

    def main_streaming(self):
        Util.create_folder(self.model.csvPath)
        for symbol in self.getAssetList():
            self.process_symbol(symbol)

    def process_symbol(self, symbol):
        data = self.model.getSymbolData(symbol)
        if data is None:
            return None
        ichimoku_data = self.model.calculateIchimokuData(data)
        self.model.saveIchimokuData(symbol, ichimoku_data)
        date_column = ichimoku_data.index.name
        if (
            date_column in {"Date", "Datetime"}
            and date_column not in ichimoku_data
        ):
            ichimoku_data = ichimoku_data.copy()
            ichimoku_data[date_column] = ichimoku_data.index
        return ichimoku_data

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
    logger.info("------ __main__ -----")
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
