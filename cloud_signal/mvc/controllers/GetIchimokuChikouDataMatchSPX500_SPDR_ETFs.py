import os

import pandas as pd

from cloud_signal.mvc.html_creator import TableGenerator


ETF_SECTORS = [
    ("XLC", "Communication Services"),
    ("XLY", "Consumer Discretionary"),
    ("XLP", "Consumer Staples"),
    ("XLE", "Energy"),
    ("XLF", "Financials"),
    ("XLV", "Health Care"),
    ("XLI", "Industrials"),
    ("XLB", "Materials"),
    ("XLRE", "Real Estate"),
    ("XLK", "Technology"),
    ("XLU", "Utilities"),
]


def main(run_scan=True):
    if not run_scan:
        return

    source_path = "output/chikou/SPX500-chikou-merged.csv"
    for ticker, sector_name in ETF_SECTORS:
        holdings_path = f"asset_list/SPDR_ETF/index-holdings-{ticker.lower()}.csv"
        if not os.path.exists(holdings_path) or not os.path.exists(source_path):
            continue

        holdings = pd.read_csv(holdings_path, skiprows=1, usecols=["Symbol"])
        scan = pd.read_csv(source_path)
        result = scan[scan["Symbol"].isin(holdings["Symbol"])]
        output_path = f"output/chikou/SPDR_ETF-{ticker}-chikou-merged.csv"
        result.to_csv(output_path, index=False)

        hidden_columns = [
            column for column in result.columns if "Chikou Direction" in column
        ]
        html = TableGenerator(output_path).generate_html_table(
            f"{ticker} - {sector_name} Chikou Scan",
            hidden_columns=hidden_columns,
        )
        TableGenerator(output_path).save_html_table(html, output_path + ".html")
