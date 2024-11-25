import pandas as pd


class Model(object):
    def __init__(
        self,
        __url,
        __fileNameCSV,
        __readHtmlMatch="",
    ) -> None:
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
        self.df_list = pd.read_html(
            self.url,
            match=self.readHtmlMatch,
        )[0]

        print("Reading symbols from source: ", self.url)
        # return type is list[DataFrame]
        print(f"Total symbols: {len(self.df_list)}")
        return self.df_list

    def cleanData(self):
        __df_list = self.df_list
        self.df = __df_list
        self.df.rename(
            columns={
                "Company": "name",
                "Symbol": "symbol",
            },
            inplace=True,
        )
        self.df["symbol"] = self.df["symbol"].str.replace(
            ".", "-", regex=False
        )

    def saveData(self):
        __columns = ["symbol", "name"]
        # print(type(self.df))
        # print(self.df)
        # print("Table:\n", self.df[__columns].values.ravel())
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
        "https://en.wikipedia.org/wiki/Russell_1000_Index#Components",
        "asset_list/Russell1000.csv",
        "Components",
    )

    _control = Control(_model, View())
    _control.main()


if __name__ == "__main__":
    main()
