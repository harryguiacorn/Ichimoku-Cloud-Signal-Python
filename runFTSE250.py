from src.mvc.controllers import (
    GetIchimokuCloudDataFTSE250,
    GetIchimokuCloudDataFTSE250Aggregator,
    GetIchimokuCloudDataFTSE250MultiTFMerger,
    GetIchimokuTKxDataFTSE250,
    GetIchimokuTKxDataFTSE250Aggregator,
    GetIchimokuTKxDataFTSE250MultiTFMerger,
    GetSymbolFTSE250,
    GetDataFTSE250,
    GetIchimokuKijunDataFTSE250,
    GetIchimokuKijunDataFTSE250Aggregator,
    GetKickerDataFTSE250,
    GetKickerDataFTSE250Aggregator,
    GetIchimokuSumCloudTKxDataFTSE250MultiTFMerger,
)
from datetime import datetime

fetch_symbols_latest_FTSE250 = True

fetch_FTSE250_1H = True

fetch_FTSE250_D = True
fetch_FTSE250_W = True
fetch_FTSE250_M = True
run_Multi_TimeFrame_Merger_FTSE250 = True

fetch_kijun_analysis = False

# Use "Datetime" for Yahoo intraday data,
# "Date" for D, W, M data.
# Use "Datetime" for all Oanda data.
fetch_Kicker_use_datetime_format = False


def main(
    fetch_symbols_latest_FTSE250,
    fetch_FTSE250_1H,
    fetch_FTSE250_D,
    fetch_FTSE250_W,
    fetch_FTSE250_M,
    fetch_Kicker_use_datetime_format,
    run_Multi_TimeFrame_Merger_FTSE250,
):
    # Stop script being auto-run by Replit or Gitpod
    # return

    time_start = datetime.now()
    print("Task begins at:", time_start.strftime("%Y-%m-%d %H:%M:%S"), "\n")

    # ---------------- FTSE 250 ----------------

    # 1. Grab latest symbols
    _getSymbolFTSE250 = GetSymbolFTSE250
    _getSymbolFTSE250.main(fetch_symbols_latest_FTSE250)

    # 2. Download latest OHLC data for each symbol
    _getDataFTSE250 = GetDataFTSE250
    _getDataFTSE250.main(
        fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W, fetch_FTSE250_M
    )

    # 3. Produce Ichimoku Cloud data for each symbol
    _getIchimokuCloudDataFTSE250 = GetIchimokuCloudDataFTSE250
    _getIchimokuCloudDataFTSE250.main(
        fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W, fetch_FTSE250_M
    )

    # 3.1 Combine latest cloud signals of all symbols into one spreadsheet
    _getIchimokuCloudDataFTSE250Aggregator = (
        GetIchimokuCloudDataFTSE250Aggregator
    )
    _getIchimokuCloudDataFTSE250Aggregator.main(
        fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W, fetch_FTSE250_M
    )

    # 3.2 Merge Multi Time Frame Cloud signals
    _getIchimokuCloudDataFTSE250MultiTFMerger = (
        GetIchimokuCloudDataFTSE250MultiTFMerger
    )
    _getIchimokuCloudDataFTSE250MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_FTSE250
    )

    # 3.3 Produce Ichimoku TK Cross data
    _gtIchimokuKijunDataFTSE250 = GetIchimokuTKxDataFTSE250
    _gtIchimokuKijunDataFTSE250.main(
        fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W, fetch_FTSE250_M
    )

    # 3.4 Combine latest TK Cross signals from all symbols into one spreadsheet
    _getIchimokuTKxDataFTSE250Aggregator = GetIchimokuTKxDataFTSE250Aggregator
    _getIchimokuTKxDataFTSE250Aggregator.main(
        fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W, fetch_FTSE250_M
    )

    # 3.5 Merge Multi Time Frame TKx signals
    _getIchimokuTKxDataFTSE250MultiTFMerger = (
        GetIchimokuTKxDataFTSE250MultiTFMerger
    )
    _getIchimokuTKxDataFTSE250MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_FTSE250
    )

    # 3.6 Merge Multi Time Frame Cloud and TKx Sum signals
    _getIchimokuSumCloudTKxDataFTSE250MultiTFMerger = (
        GetIchimokuSumCloudTKxDataFTSE250MultiTFMerger
    )
    _getIchimokuSumCloudTKxDataFTSE250MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_FTSE250
    )

    # 4. Produce Kijun data
    _getIchimokuKijunDataFTSE250 = GetIchimokuKijunDataFTSE250
    _getIchimokuKijunDataFTSE250.main(
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
    )

    # 4.1 Combine latest Kijun signals from all symbols into one spreadsheet
    _getIchimokuKijunDataFTSE250Aggregator = (
        GetIchimokuKijunDataFTSE250Aggregator
    )
    _getIchimokuKijunDataFTSE250Aggregator.main(
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
    )

    # 5. Produce Kicker data
    _getKickerDataFTSE250 = GetKickerDataFTSE250
    _getKickerDataFTSE250.main(
        fetch_Kicker_use_datetime_format,
        fetch_FTSE250_D,
        fetch_FTSE250_W,
        fetch_FTSE250_M,
    )

    # 5.1 Combine latest Kicker signals from all symbols into one spreadsheet
    _getKickerDataFTSE250Aggregator = GetKickerDataFTSE250Aggregator
    _getKickerDataFTSE250Aggregator.main(
        fetch_Kicker_use_datetime_format,
        fetch_FTSE250_D,
        fetch_FTSE250_W,
        fetch_FTSE250_M,
    )
    # calculate time elapsed
    time_finish = datetime.now()
    time_elapsed = time_finish - time_start
    time_finish_formatted = time_finish.strftime("%Y-%m-%d %H:%M:%S")
    print(
        f"\nTasks completed at {time_finish_formatted} (Time elapsed: {time_elapsed})",
    )


if __name__ == "__main__":
    main(
        fetch_symbols_latest_FTSE250,
        fetch_FTSE250_1H,
        fetch_FTSE250_D,
        fetch_FTSE250_W,
        fetch_FTSE250_M,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_FTSE250,
    )
