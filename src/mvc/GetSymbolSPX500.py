import pandas as pd


class Model(object):
    def __init__(self, __url, __fileNameCSV, __readHtmlMatch="") -> None:
        self.url = __url
        self.fileNameCSV = __fileNameCSV
        self.readHtmlMatch = __readHtmlMatch
        self.df_list = None
        self.df = None

    @property
    def df_list(self):
        return self.__df_list

    @df_list.setter
    def df_list(self, __df_list):
        self.__df_list = __df_list

    def readHtml(self):
        self.df_list = pd.read_html(self.url, match=self.readHtmlMatch)[0]

        # return type is list[DataFrame]
        print(f"Total tables: {len(self.df_list)}")
        return self.df_list

    def cleanData(self):
        __df_list = self.df_list
        self.df = __df_list
        # print(self.df)
        self.df.rename(
            columns={"Security": "name", "Symbol": "symbol"}, inplace=True
        )
        self.df["symbol"] = self.df["symbol"].str.replace(
            ".", "-", regex=False
        )
        # print(*self.df["symbol"], sep=",")

    def saveData(self):
        __columns = ["symbol", "name"]
        # print(type(self.df))
        # print(self.df)
        # print(self.df[__columns])
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
        # print(self.model.df_list)
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
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks",
        "asset_list/SPX500.csv",
    )

    _control = Control(_model, View())
    _control.main()


if __name__ == "__main__":
    main()
