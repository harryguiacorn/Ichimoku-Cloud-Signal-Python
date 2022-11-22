import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tapy import Indicators
from pandas_datareader import data as pdr
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
from DataOHLC import DataOHLC

class DataPlotly(DataOHLC): # deprecated, use DataPandas
    csvPath='data/'
    def __init__(self, stockSymbol):
        self.stockSymbol = stockSymbol
        # self.lookbackPeriod = lookbackPeriod
        # self.ticker = yfinance.Ticker(stockSymbol)
        # self.history = self.ticker.history(lookbackPeriod)

    def setFromToToday(self, countbackDays):
        delta = pd.Timedelta(days=countbackDays)
        today = datetime.now()
        self.history = pdr.get_data_yahoo(
            self.stockSymbol, today - delta, today)

    def saveData(self):
        self.history.to_csv(DataPlotly.csvPath + self.stockSymbol + '.csv')

    def midPoint(self, __data, __lookbackPeriod=26):
        __max = __data['Close'].rolling(window=__lookbackPeriod).max()
        __min = __data['Close'].rolling(window=__lookbackPeriod).min()
        return (__max + __min)/2

    def runIndicator(self):
        # initialising indicators
        __data = pd.read_csv(DataPlotly.csvPath + self.stockSymbol + '.csv')
        # __data.index = __data.Date
        # __data = self.history
        __i = Indicators(__data)
        __i.ichimoku_kinko_hyo()
        __dataCloud = __i.df
        self.history = __dataCloud
        # print(self.history.tail())
        __dataCloud.to_csv(DataPlotly.csvPath + self.stockSymbol + '_ichimokuPlotly.csv')

    # custom function to set fill color
    def fillcol(self, lineA, lineB):
        # if not (pd.isna(lineA) & pd.isna(lineB)):
        try:
            if lineA >= lineB:
                return 'rgba(0,250,0,0.4)'
            else:
                return 'rgba(250,0,0,0.4)'
        except:
            print("fillcol Line Errors")
        finally:
            return "blue"

    def show(self):
        self.history['diff'] = self.history['Close'] - self.history['Open']
        self.history.loc[self.history['diff'] >= 0, 'color'] = 'green'
        self.history.loc[self.history['diff'] < 0, 'color'] = 'red'
        # print(self.history.head())

        pd.set_option('display.max_rows', None)  # print every row for debug

        fig3 = make_subplots(specs=[[{"secondary_y": True}]])

        # __Tenkan_sen = self.midPoint(self.history, 9)
        # __Kijun_sen = self.midPoint(self.history, 26)
        fig3.add_trace(go.Scatter(x=self.history.index, y=self.history['tenkan_sen'],
                                  marker_color='#e377c2', name='Tenkan'))
        fig3.add_trace(go.Scatter(x=self.history.index, y=self.history['kijun_sen'],
                                  marker_color='blue', name='Kijun'))

        fig3.add_trace(go.Scatter(x=self.history.index, y=self.history['senkou_span_a'],
                                  line_color='#e377c2',
                                  name='senkou_span_a'))

        # print(self.history['senkou_span_a'].iloc[self.history.index])
        fig3.add_trace(go.Scatter(x=self.history.index,
                       y=self.history['senkou_span_b'], line_color='#fee440', name='senkou_span_b', fill='tonexty'))

        fig3.add_trace(go.Scatter(x=self.history.index, y=self.history['chikou_span'],
                                  marker_color='#8c564b', name='chikou_span', mode='markers'))
        fig3.add_trace(go.Bar(x=self.history.index, y=self.history['Volume'], name='Volume', marker={
            'color': self.history['color']}), secondary_y=True)
        fig3.add_trace(go.Candlestick(x=self.history.index,
                                      open=self.history['Open'],
                                      high=self.history['High'],
                                      low=self.history['Low'],
                                      close=self.history['Close'],
                                      name='Price'))

        fig3.update_yaxes(range=[0, 700000000], secondary_y=True)
        fig3.update_yaxes(visible=False, secondary_y=True)
        fig3.update_layout(xaxis={'type': 'category'},
                           xaxis_rangeslider_visible=True)  # hide range slider
        fig3.update_layout(title={'text': self.stockSymbol, 'x': 0.5})
        fig3.update_xaxes(rangebreaks=[
            dict(bounds=['sat', 'sun']),  # hide weekends
            # dict(bounds=[16, 9.5], pattern='hour'), # for hourly chart, hide non-trading hours (24hr format)
            dict(values=["2021-12-25", "2022-01-01"])  # hide Xmas and New Year
        ])

        fig3.show()
    
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

def main():
    stock1 = DataPlotly('AAPL')
    stock1.setFromToToday(240)
    stock1.saveData()
    stock1.runIndicator()
    # stock1.show()

    stock1 = DataPlotly('MSFT')
    stock1.setFromToToday(240)
    stock1.saveData()
    stock1.runIndicator()
    stock1.show()

if __name__ == "__main__":
    main()