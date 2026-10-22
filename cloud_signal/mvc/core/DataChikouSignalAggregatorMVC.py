import os

import pandas as pd
from cloud_signal.mvc.html_creator import TableGenerator
from cloud_signal.mvc.core._csv_utils import latest_csv_path


class Model(object):
    def __init__(
        self, csvPath, assetListPath, outputPath, assetClassName, prefix
    ):
        self.csvPath = csvPath
        self.assetListPath = assetListPath
        self.outputPath = outputPath
        self.assetClassName = assetClassName
        self.prefix = prefix

    def main(self):
        assets = pd.read_csv(self.assetListPath).dropna(subset=["symbol"])
        assets["symbol"] = (
            assets["symbol"]
            .astype(str)
            .str.replace("/", "", regex=False)
            .str.strip()
        )
        rows = []
        date_column = "Date"
        for _, asset in assets.iterrows():
            symbol = asset["symbol"]
            path = os.path.join(self.csvPath, f"{symbol}_chikouCount.csv")
            path = latest_csv_path(path)
            if not os.path.exists(path):
                continue
            data = pd.read_csv(path)
            if data.empty:
                continue
            latest = data.iloc[-1]
            date_column = "Datetime" if "Datetime" in data.columns else "Date"
            rows.append(
                [
                    latest[date_column],
                    symbol,
                    asset["name"],
                    latest.get("Close", pd.NA),
                    latest["Chikou Signal"],
                    latest["Chikou Signal Count"],
                    latest["Chikou State"],
                ]
            )

        columns = [
            "Date",
            "Symbol",
            "Name",
            "Close",
            f"{self.prefix} Chikou Direction",
            f"{self.prefix} Chikou Count",
            f"{self.prefix} Chikou State",
        ]
        if date_column == "Datetime":
            columns[0] = "Datetime"
        result = pd.DataFrame(rows, columns=columns)
        if not result.empty:
            result.sort_values(by=f"{self.prefix} Chikou Count", inplace=True)
        os.makedirs(self.outputPath, exist_ok=True)
        csv_path = os.path.join(
            self.outputPath, self.assetClassName.replace(" ", "") + ".csv"
        )
        result.to_csv(csv_path, index=False)
        return csv_path


class Control(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def main(self):
        csv_path = self.model.main()
        market_name = self.model.assetClassName.rsplit("-chikou-", 1)[0]
        market_name = {
            "SPX500": "S&P 500",
            "Nasdaq100": "Nasdaq 100",
            "DowJones30": "Dow Jones 30",
            "Russell1000": "Russell 1000",
            "Kraken": "Kraken Cryptocurrency",
            "FTSE100": "FTSE 100",
            "FTSE250": "FTSE 250",
            "FuturesCurrency": "Futures Currency",
            "HSI": "Hang Seng Index",
        }.get(market_name, market_name)
        html = TableGenerator(csv_path).generate_html_table(
            f"{market_name} Chikou Scan"
        )
        TableGenerator(csv_path).save_html_table(html, csv_path + ".html")


class View(object):
    pass
