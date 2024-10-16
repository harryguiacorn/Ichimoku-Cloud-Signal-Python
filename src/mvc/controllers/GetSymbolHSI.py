import pandas as pd


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
        print("Reading symbols from source: ", self.url)
        # print("self.readHtmlMatch", self.readHtmlMatch)
        self.df_list = pd.read_html(self.url, match=self.readHtmlMatch)[0]
        # self.df_list = pd.read_html(self.url)[4]

        # return type is list[DataFrame]
        print(f"Total symbols: {len(self.df_list)}")
        return self.df_list

    def cleanData(self):
        __df_list = self.df_list
        self.df = __df_list
        # print(self.df)
        self.df.rename(
            columns={"Name": "name", "Ticker": "symbol"}, inplace=True
        )

        # Extract only the digits from the ticker
        self.df["symbol"] = self.df["symbol"].str.extract(r"(\d+)")

        # Ensure tickers are 4 digits by padding with leading zeros
        self.df["symbol"] = self.df["symbol"].str.zfill(4)

        # add .HK to symbol for Yahoo Finance
        self.df["symbol"] = self.df["symbol"].astype(str) + ".HK"

    def saveData(self):
        # print(type(self.df))
        __columns = ["symbol", "name"]
        print("Table:\n", self.df[__columns])
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
        "https://en.wikipedia.org/wiki/Hang_Seng_Index",
        "asset_list/HSI.csv",
        "Ticker",
    )

    _control = Control(_model, View())
    _control.main()


if __name__ == "__main__":
    main()
