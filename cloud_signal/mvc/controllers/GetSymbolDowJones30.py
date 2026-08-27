import pandas as pd
import requests
import io
import logging

logger = logging.getLogger(__name__)


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
        logger.info(f"Reading symbols from source: {self.url}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes
            tables = pd.read_html(io.StringIO(response.text))
            selected_table = None
            for table in tables:
                columns = [str(column).strip() for column in table.columns]
                normalized_columns = [column.lower() for column in columns]
                symbol_column = next(
                    (
                        column
                        for column, normalized in zip(
                            columns, normalized_columns
                        )
                        if "symbol" in normalized or "ticker" in normalized
                    ),
                    None,
                )
                name_column = next(
                    (
                        column
                        for column, normalized in zip(
                            columns, normalized_columns
                        )
                        if "company" in normalized
                        or "security" in normalized
                        or normalized == "name"
                    ),
                    None,
                )
                if symbol_column is not None and name_column is not None:
                    selected_table = table.copy()
                    selected_table.rename(
                        columns={symbol_column: "symbol", name_column: "name"},
                        inplace=True,
                    )
                    break

            if selected_table is None:
                raise ValueError(
                    "Could not find a Dow Jones table with symbol and company columns"
                )

            self.df_list = selected_table
            logger.info(f"Reading symbols from source: {self.url}")
            logger.info(f"Total symbols: {len(self.df_list)}")
            return self.df_list
        except Exception as e:
            logger.info(f"Error reading HTML: {e}")
            raise

    def cleanData(self):
        __df_list = self.df_list
        self.df = __df_list
        self.df["symbol"] = (
            self.df["symbol"].astype(str).str.replace(".", "-", regex=False)
        )

    def saveData(self):
        __columns = ["symbol", "name"]
        # print(type(self.df))
        # print(self.df)
        # print("Table:\n", self.df[__columns].values.ravel())
        logger.info(f"Table:\n{self.df[__columns]}")
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
        "https://en.wikipedia.org/wiki/List_of_Dow_Jones_Industrial_Average_companies",
        "asset_list/DowJones30.csv",
    )

    _control = Control(_model, View())
    _control.main()


if __name__ == "__main__":
    main()
