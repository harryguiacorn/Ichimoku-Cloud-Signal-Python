import logging
import pandas as pd
import requests


class Model(object):
    def __init__(self, __url, __fileNameCSV, __readHtmlMatch="") -> None:
        self.url = __url
        self.fileNameCSV = __fileNameCSV
        self.readHtmlMatch = __readHtmlMatch
        self.df_list = None
        self.df = pd.DataFrame()
        self.logger = logging.getLogger(__name__)

    @property
    def df_list(self):
        return self.__df_list

    @df_list.setter
    def df_list(self, __df_list):
        self.__df_list = __df_list

    def readHtml(self):
        self.logger.debug("Reading symbols from source: %s", self.url)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes

            # Read HTML tables from response text
            tables = pd.read_html(response.text, match=self.readHtmlMatch)
            # print(f"Total symbols: {len(tables )}")
            # print("Columns found:", self.df_list.columns.tolist())
            # print(f"Symbols: {tables}")

            # 🔍 Dynamically find the correct table
            selected_table = None
            for i, df in enumerate(tables):
                # normalize column names for robust matching
                cols = [str(c).strip() for c in df.columns]
                cols_norm = [c.lower() for c in cols]
                self.logger.debug("Table %d columns: %s", i, cols)

                # look for common header variants
                symbol_idx = next(
                    (
                        idx
                        for idx, c in enumerate(cols_norm)
                        if "symbol" in c or "ticker" in c
                    ),
                    None,
                )
                name_idx = next(
                    (
                        idx
                        for idx, c in enumerate(cols_norm)
                        if "security" in c or "company" in c or "name" in c
                    ),
                    None,
                )

                if symbol_idx is not None and name_idx is not None:
                    self.logger.debug("Found matching table at index %d", i)
                    selected_table = df.copy()
                    # ensure canonical column names
                    selected_table.columns = cols
                    break

            if selected_table is None:
                raise ValueError(
                    "Could not find a table with symbol/name columns among the parsed HTML tables"
                )

            self.df_list = selected_table
            return self.df_list
        except requests.RequestException as e:
            self.logger.error("Network error reading %s: %s", self.url, e)
            raise
        except ValueError:
            # re-raise ValueError from above
            raise
        except Exception as e:
            self.logger.exception("Unexpected error reading HTML: %s", e)
            raise

    def cleanData(self):
        __df_list = self.df_list
        self.df = __df_list
        self.logger.debug(
            "cleanData -> Columns available: %s", self.df.columns.tolist()
        )

        # normalize columns for safe renaming
        cols_map = {}
        cols_lower = {str(c).lower(): c for c in self.df.columns}
        if "security" in cols_lower:
            cols_map[cols_lower["security"]] = "name"
        if "company" in cols_lower:
            cols_map[cols_lower["company"]] = "name"
        if "symbol" in cols_lower:
            cols_map[cols_lower["symbol"]] = "symbol"
        if "ticker" in cols_lower:
            cols_map[cols_lower["ticker"]] = "symbol"

        if not cols_map:
            raise ValueError(
                "Expected symbol/company columns not found in HTML table"
            )

        self.df.rename(columns=cols_map, inplace=True)

        # Ensure symbol column is string and replace dots with dashes
        if "symbol" in self.df.columns:
            self.df["symbol"] = (
                self.df["symbol"]
                .astype(str)
                .str.replace(".", "-", regex=False)
            )
        else:
            raise KeyError("symbol column missing after rename")

    def saveData(self):
        __columns = ["symbol", "name"]
        # print(type(self.df))
        # print(self.df)
        self.logger.info(f"Saving table to {self.fileNameCSV}")
        self.logger.debug(
            "Table:\n%s", self.df[__columns].head(20).to_string()
        )
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
