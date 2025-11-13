import pandas as pd
import requests
import io


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
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes

            # Corrected line: Wrap the response text in StringIO
            html_string_io = io.StringIO(response.text)
            tables = pd.read_html(html_string_io, match=self.readHtmlMatch)
            # print(f"Total symbols: {len(tables )}")
            # print("Columns found:", self.df_list.columns.tolist())
            # print(f"Symbols: {tables}")

            # 🔍 Dynamically find the correct table
            selected_table = None
            for i, df in enumerate(tables):
                cols = [str(c).strip() for c in df.columns]
                print(f"Table {i} columns: {cols}")

                symbol_col = next(
                    (c for c in cols if "Symbol" in c or "Ticker" in c), None
                )
                name_col = next(
                    (c for c in cols if "Security" in c or "Company" in c),
                    None,
                )

                if symbol_col and name_col:
                    print(f"✅ Found matching table at index {i}")
                    selected_table = df
                    break

            if selected_table is None:
                raise ValueError(
                    f"❌ Could not find a table with symbol/name columns among {[t.columns.tolist() for t in tables]}"
                )

            self.df_list = selected_table
            return self.df_list
        except Exception as e:
            print(f"Error reading HTML: {e}")
            raise

    def cleanData(self):
        __df_list = self.df_list
        self.df = __df_list

        print("cleanData -> Columns available:", self.df.columns.tolist())
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
