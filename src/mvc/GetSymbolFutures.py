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
        self.df = None

    @property
    def df_list(self):
        return self.__df_list

    @df_list.setter
    def df_list(self, __df_list):
        self.__df_list = __df_list

    def scrape_symbols_name(self):
        response = requests.get(self.url)
        df = pd.read_html(response.content)
        df_symbols = df[0][["Symbol", "Name"]]
        print(df_symbols)
        return df_symbols

    def saveData(self):
        df_symbol = self.scrape_symbols_name()
        df_symbol.to_csv(self.fileNameCSV)


class View(object):
    pass


class Control(object):
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view

    def main(self):
        # self.scrape_symbols_name()
        self.saveData()

    def saveData(self):
        self.model.saveData()


def main(__fetch_symbols_latest=True):
    if __fetch_symbols_latest is False:
        return
    _model = Model(
        "https://finance.yahoo.com/commodities/",
        "asset_list/Futures.csv",
    )

    _control = Control(_model, View())
    _control.main()


if __name__ == "__main__":
    main()
