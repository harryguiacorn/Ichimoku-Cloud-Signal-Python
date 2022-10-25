import datetime
from genericpath import isdir
import os
import pandas as pd
from finta import TA
from pandas_datareader import data as pdr
from tapy import Indicators
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from DataOHLC import DataOHLC


class DataPandas(DataOHLC):

    def __init__(self,
                 __csvPath='data/',
                 __assetListPath='',
                 __getLatestDataFromYahoo=False):
        '''__csvPath points to csv files for asset class
        __assetListPath points to the path for asset list'''
        self.csvPath = __csvPath
        self.assetListPath = __assetListPath
        self.getLatestDataFromYahoo = __getLatestDataFromYahoo

    def readAssetList(self, __csvPath, __colName='symbol'):
        df = pd.read_csv(__csvPath)
        print(df.to_string())
        l_symbol = df[__colName].tolist()
        return l_symbol

    def getLastestData(self,
                       symbols,
                       __lookbackDays=3 * 365,
                       __toDate='today'):

        startDate = (
            datetime.datetime.now() -
            datetime.timedelta(days=__lookbackDays)).strftime("%Y-%m-%d")
        endData = __toDate

        __dict_df = {}
        for __symbol in symbols:
            try:
                data = pdr.get_data_yahoo(__symbol, startDate, endData)

                __dict_df[__symbol] = data

                data.to_csv(self.csvPath + __symbol + '.csv')
            except Exception as e:
                raise Exception("Error getting: " + e.args)
        return __dict_df

    def createIchimokuDataTapy(self,
                               __dict_df):  # create Ichimoku data using tapy
        __dict_df_ichimoku = {}
        for __key, __df in __dict_df.items():
            # initialising indicators
            __i = Indicators(__df)
            __i.ichimoku_kinko_hyo()  #column_name_kijun_sen="K Line"
            __dataCloud = __i.df
            __dict_df_ichimoku[__key] = __dataCloud
            __dataCloud.to_csv(self.csvPath + __key + '_ichimokuTapy.csv')
        return __dict_df_ichimoku

    def main(self):
        # initializing Parameters
        self.__createDataFolder(self.csvPath)

        symbols = self.readAssetList(self.assetListPath)
        if self.getLatestDataFromYahoo:
            print("*************************************************")
            # method 1. grab latest data from yahoo finance
            DictData = self.getLastestData(symbols, 1 * 365, 'today')
        else:
            # method 2. grab data from local raw csv files to prevent IP getting blocked by Yahoo servers
            DictData = self.readLocalCsvData(symbols, self.csvPath)

        # method 1. create Ichimoku data using tapy
        DictDataIchinokuTapy = self.createIchimokuDataTapy(DictData)
        # method 2. alternative method to add ichimoku columns to csv using finta
        # self.createIchimokuDataFinta(DictData)

        # self.displayCharts(DictDataIchinokuTapy)

    # create Ichimoku data using finta, this is the alternative option
    def createIchimokuDataFinta(self, __dict_df):
        for __symbol, __df in __dict_df.items():
            df = pd.read_csv(self.csvPath + __symbol + '.csv')
            TA.ICHIMOKU(df).to_csv(self.csvPath + __symbol +
                                   '_ichimokuFinta.csv')

    def readLocalCsvData(self, symbols, __csvPath):
        __dict_df = {}
        for __symbol in symbols:
            __df = pd.read_csv(__csvPath + __symbol + '.csv')
            __dict_df[__symbol] = __df
        return __dict_df

    def displayCharts(self, __data):
        for __key, __df in __data.items():
            self.displayChart(__key, __df)

    def displayChart(self, __symbol, __df):
        __df['diff'] = __df['Close'] - __df['Open']
        __df.loc[__df['diff'] >= 0, 'color'] = 'green'
        __df.loc[__df['diff'] < 0, 'color'] = 'red'
        # print(__df.head())

        pd.set_option('display.max_rows', None)  # print every row for debug

        fig3 = make_subplots(specs=[[{"secondary_y": True}]])

        # __Tenkan_sen = self.midPoint(__df, 9)
        # __Kijun_sen = self.midPoint(__df, 26)
        fig3.add_trace(
            go.Scatter(x=__df.index,
                       y=__df['tenkan_sen'],
                       marker_color='#e377c2',
                       name='Tenkan'))
        fig3.add_trace(
            go.Scatter(x=__df.index,
                       y=__df['kijun_sen'],
                       marker_color='blue',
                       name='Kijun'))

        fig3.add_trace(
            go.Scatter(x=__df.index,
                       y=__df['senkou_span_a'],
                       line_color='#e377c2',
                       name='senkou_span_a'))

        # print(__df['senkou_span_a'].iloc[__df.index])
        fig3.add_trace(
            go.Scatter(x=__df.index,
                       y=__df['senkou_span_b'],
                       line_color='#fee440',
                       name='senkou_span_b',
                       fill='tonexty'))

        fig3.add_trace(
            go.Scatter(x=__df.index,
                       y=__df['chikou_span'],
                       marker_color='#8c564b',
                       name='chikou_span',
                       mode='markers'))
        fig3.add_trace(go.Bar(x=__df.index,
                              y=__df['Volume'],
                              name='Volume',
                              marker={'color': __df['color']}),
                       secondary_y=True)
        fig3.add_trace(
            go.Candlestick(x=__df.index,
                           open=__df['Open'],
                           high=__df['High'],
                           low=__df['Low'],
                           close=__df['Close'],
                           name='Price'))

        fig3.update_yaxes(range=[0, 700000000], secondary_y=True)
        fig3.update_yaxes(visible=False, secondary_y=True)
        fig3.update_layout(xaxis={'type': 'category'},
                           xaxis_rangeslider_visible=True)  # hide range slider
        fig3.update_layout(title={'text': __symbol, 'x': 0.5})
        fig3.update_xaxes(rangebreaks=[
            dict(bounds=['sat', 'sun']),  # hide weekends
            # dict(bounds=[16, 9.5], pattern='hour'), # for hourly chart, hide non-trading hours (24hr format)
            dict(values=["2021-12-25", "2022-01-01"])  # hide Xmas and New Year
        ])

        fig3.show()

    def __createDataFolder(self, __name="data"):
        # create data folder
        try:
            if isdir(__name) == False:
                os.mkdir(__name)
        except FileExistsError as __errFile:
            print("data folder exists")


if __name__ == "__main__":
    print("----------------------------------------------")
    dataP = DataPandas('data/', 'asset_list/spx.csv')
    dataP.main()
