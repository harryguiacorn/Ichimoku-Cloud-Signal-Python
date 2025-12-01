import pandas as pd
import requests
import io
import logging
logger = logging.getLogger(__name__)


class Model(object):
    def __init__(self, __url, __fileNameCSV, __readHtmlMatch="") -> None:
        self.url = __url
        self.fileNameCSV = __fileNameCSV
        self.readHtmlMatch = __readHtmlMatch
        self.df_list = None
        self.df = pd.DataFrame

    @property
    def df_list(self):
        return self.__df_list

    @df_list.setter
    def df_list(self, __df_list):
        self.__df_list = __df_list

    def readHtml(self):
        logger.info("Reading symbols from source: ", self.url)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes
            # Corrected line: Wrap the response text in StringIO
            html_string_io = io.StringIO(response.text)
            self.df_list = pd.read_html(
                html_string_io, match=self.readHtmlMatch
            )[0]
            logger.info("Reading symbols from source: ", self.url)
            logger.info(f"Total symbols: {len(self.df_list)}")
            return self.df_list
        except Exception as e:
            logger.info(f"Error reading HTML: {e}")
            raise

    def cleanData(self):
        __df_list = self.df_list
        self.df = __df_list
        # print(self.df)
        self.df.rename(
            columns={"Company": "name", "Ticker": "symbol"}, inplace=True
        )
        self.df["symbol"] = (
            self.df["symbol"].astype(str) + ".L"
        )  # add .L to symbol for Yahoo Finance

    def saveData(self):
        # print(type(self.df))
        __columns = ["symbol", "name"]
        logger.info("Table:\n", self.df[__columns])
        self.df.to_csv(self.fileNameCSV, columns=__columns, index=False)
        return self.df[__columns]


class View(object):
    pass


class Control(object):
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view

    def main(self):
        self.readHtml()
        # print("self.model.df_list:\n", self.model.df_list)
        self.cleanData()
        self.saveData()

    def readHtml(self, __match=""):
        self.model.readHtml()

    def cleanData(self):
        self.model.cleanData()

    def saveData(self):
        self.model.saveData()


def main(__fetch_symbols_latest=True):
    if __fetch_symbols_latest is False:
        return
    _model = Model(
        "https://en.wikipedia.org/wiki/FTSE_100_Index",
        "asset_list/FTSE100.csv",
        "Company",
    )

    _control = Control(_model, View())
    _control.main()


if __name__ == "__main__":
    main()
