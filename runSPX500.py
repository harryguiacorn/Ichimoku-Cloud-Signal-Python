from src.mvc.controllers import (
    GetIchimokuCloudDataSPX500,
    GetIchimokuCloudDataSPX500Aggregator,
    GetIchimokuTKxDataSPX500,
    GetIchimokuTKxDataSPX500Aggregator,
    GetSymbolSPX500,
    GetDataSPX500,
    GetIchimokuKijunDataSPX500,
    GetIchimokuKijunDataSPX500Aggregator,
    GetKickerDataSPX500,
    GetKickerDataSPX500Aggregator,
    GetIchimokuCloudDataSPX500MultiTFMerger,
    GetIchimokuTKxDataSPX500MultiTFMerger,
    GetIchimokuSumCloudTKxDataSPX500MultiTFMerger,
)

fetch_symbols_latest_SPX500 = True

fetch_SPX500_1H = True
fetch_SPX500_D = True
fetch_SPX500_W = True
fetch_SPX500_M = True

run_Multi_TimeFrame_Merger_SPX500 = True

fetch_kijun_analysis = False

# Use "Datetime" for Yahoo intraday data,
# "Date" for D, W, M data.
# Use "Datetime" for all Oanda data.
fetch_Kicker_use_datetime_format = False


def main(
    fetch_SPX500_1H,
    fetch_SPX500_D,
    fetch_SPX500_W,
    fetch_SPX500_M,
    fetch_Kicker_use_datetime_format,
    run_Multi_TimeFrame_Merger_SPX500,
):
    # Stop script being auto-run by Replit or Gitpod
    # return

    # ---------------- S&P 500 ----------------

    # 1. Grab latest symbols
    _getSymbolSPX500 = GetSymbolSPX500
    _getSymbolSPX500.main(fetch_symbols_latest_SPX500)

    # 2. Download latest OHLC data for each symbol
    _getDataSPX500 = GetDataSPX500
    _getDataSPX500.main(
        fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W, fetch_SPX500_M
    )

    # 3. Produce Ichimoku Cloud data for each symbol
    _getIchimokuCloudDataSPX500 = GetIchimokuCloudDataSPX500
    _getIchimokuCloudDataSPX500.main(
        fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W, fetch_SPX500_M
    )

    # 3.1 Combine latest cloud signals of all symbols into one spreadsheet
    _getIchimokuCloudDataSPX500Aggregator = (
        GetIchimokuCloudDataSPX500Aggregator
    )
    _getIchimokuCloudDataSPX500Aggregator.main(
        fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W, fetch_SPX500_M
    )

    # 3.2 Merge Multi Time Frame Cloud signals
    _getIchimokuCloudDataSPX500MultiTFMerger = (
        GetIchimokuCloudDataSPX500MultiTFMerger
    )
    _getIchimokuCloudDataSPX500MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_SPX500
    )

    # 3.3 Produce Ichimoku TK Cross data
    _getIchimokuTKxDataSPX500 = GetIchimokuTKxDataSPX500
    _getIchimokuTKxDataSPX500.main(
        fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W, fetch_SPX500_M
    )

    # 3.4 Combine latest TK Cross signals from all symbols into one spreadsheet
    _getIchimokuTKxDataSPX500Aggregator = GetIchimokuTKxDataSPX500Aggregator
    _getIchimokuTKxDataSPX500Aggregator.main(
        fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W, fetch_SPX500_M
    )

    # 3.5 Merge Multi Time Frame TKx signals
    _getIchimokuTKxDataSPX500MultiTFMerger = (
        GetIchimokuTKxDataSPX500MultiTFMerger
    )
    _getIchimokuTKxDataSPX500MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_SPX500
    )

    # 3.6 Merge Multi Time Frame Cloud and TKx Sum signals
    _getIchimokuSumCloudTKxDataSPX500MultiTFMerger = (
        GetIchimokuSumCloudTKxDataSPX500MultiTFMerger
    )
    _getIchimokuSumCloudTKxDataSPX500MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_SPX500
    )

    # 4. Produce Kijun data
    _getIchimokuKijunDataSPX500 = GetIchimokuKijunDataSPX500
    _getIchimokuKijunDataSPX500.main(
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
    )

    # 4.1 Combine latest Kijun signals from all symbols into one spreadsheet
    _getIchimokuKijunDataSPX500Aggregator = (
        GetIchimokuKijunDataSPX500Aggregator
    )
    _getIchimokuKijunDataSPX500Aggregator.main(
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
    )

    # 5. Produce Kicker data
    _getKickerDataSPX500 = GetKickerDataSPX500
    _getKickerDataSPX500.main(
        fetch_Kicker_use_datetime_format,
        fetch_SPX500_D,
        fetch_SPX500_W,
        fetch_SPX500_M,
    )

    # 5.1 Combine latest Kicker signals from all symbols into one spreadsheet
    _getKickerDataSPX500Aggregator = GetKickerDataSPX500Aggregator
    _getKickerDataSPX500Aggregator.main(
        fetch_Kicker_use_datetime_format,
        fetch_SPX500_D,
        fetch_SPX500_W,
        fetch_SPX500_M,
    )

    print("\nTasks completed.")


if __name__ == "__main__":
    main(
        fetch_SPX500_1H,
        fetch_SPX500_D,
        fetch_SPX500_W,
        fetch_SPX500_M,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_SPX500,
    )
