import pandas as pd
import requests


class SymbolScraper:
    def __init__(self, url="https://finance.yahoo.com/world-indices/"):
        self.url = url


class Model(object):
    def __init__(self, __url, __fileNameCSV) -> None:
        self.url = __url
        self.fileNameCSV = __fileNameCSV
        self.df_list = None
        self.df = pd.DataFrame

    @property
    def df_list(self):
        return self.__df_list

    @df_list.setter
    def df_list(self, __df_list):
        self.__df_list = __df_list

    def readHtml(self):
        self.scrape_symbols_name()

    def scrape_symbols_name(self):
        print("Reading symbols from source: ", self.url)
        response = requests.get(self.url)
        df = pd.read_html(response.content)
        print("Web Content::\n", df)
        df_symbols = df[0][["Symbol"]] # Yahoo Finance removed "Name", OLD CODING: df[0][["Symbol", "Name"]]
        self.df_list = df_symbols
        # print(df_symbols.values.ravel())
        print(f"Total symbols: {len(self.df_list)}")
        return df_symbols

    def cleanData(self):
        __df_list = self.df_list
        self.df = __df_list

        # self.df.rename(
        #     columns={
        #         "Symbol": "symbol",
        #         "Name": "name",
        #     },
        #     inplace=True,
        # )
        
        # Split the "Symbol" column at the first space
        self.df[['symbol', 'name']] = self.df['Symbol'].str.split(n=1, expand=True)

        print("cleanData::\n", self.df)
        
        # self.df["symbol"] = self.df["symbol"].str.replace(
        #     ".", "-", regex=False
        # )

    def saveData(self):
        # print(type(self.df))
        # print(self.df[__columns])
        # df_symbol.to_csv(self.fileNameCSV, index=False)
        __columns = ["symbol", "name"]
        print("Table:\n", self.df[__columns])
        self.df.to_csv(
            self.fileNameCSV,
            columns=__columns,
            index=False,
        )
        return self.df[__columns]


class View(object):
    pass


class Control(object):
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view

    def main(self):
        self.readHtml()
        self.cleanData()
        self.saveData()

    def readHtml(self):
        self.model.readHtml()

    def cleanData(self):
        self.model.cleanData()

    def saveData(self):
        self.model.saveData()


def main(__fetch_symbols_latest=True):
    if __fetch_symbols_latest is False:
        return
    _model = Model(
        "https://finance.yahoo.com/markets/commodities/",
        "asset_list/Futures.csv",
    )

    _control = Control(_model, View())
    _control.main()


if __name__ == "__main__":
    main()
