import pandas as pd
import requests
import logging
logger = logging.getLogger(__name__)


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
        logger.info("Reading symbols from source: ", self.url)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        response = requests.get(self.url, headers=headers)

        logger.info("response.status_code:", response.status_code)

        df_temp = pd.read_html(response.content)
        logger.info("Web Content::\n", df_temp)

        # df_symbols = df[0][["Symbol"]] # If Yahoo Finance removed "Name", Otherwise use OLD CODING: df[0][["Symbol", "Name"]]
        df_symbols = df_temp[0][["Symbol", "Name"]]

        self.df_list = df_symbols
        # print(df_symbols.values.ravel())
        logger.info(f"Total symbols: {len(self.df_list)}")
        return df_symbols

    def cleanData(self):
        # print("before leanData::\n", self.df_list)

        __df_list = self.df_list.dropna()

        # __df_list = self.df_lgetLatestDataFromYahooByYFinanceist
        self.df = __df_list

        self.df.rename(
            columns={
                "Symbol": "symbol",
                "Name": "name",
            },
            inplace=True,
        )
        # # If Yahoo Finance removes "Name", Split the "Symbol" column at the first space
        # self.df[['symbol', 'name']] = self.df['Symbol'].str.split(n=1, expand=True)

        logger.info("cleanData::\n", self.df)

        # self.df["symbol"] = self.df["symbol"].str.replace(
        #     ".", "-", regex=False
        # )

    def saveData(self):
        # print(type(self.df))
        # print(self.df[__columns])
        # df_symbol.to_csv(self.fileNameCSV, index=False)
        __columns = ["symbol", "name"]
        logger.info("Table:\n", self.df[__columns])
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
