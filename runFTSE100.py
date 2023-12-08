from src.mvc.controllers import (
    GetIchimokuCloudDataFTSE100,
    GetIchimokuCloudDataFTSE100MultiTFMerger,
    GetIchimokuTKxDataFTSE100,
    GetIchimokuTKxDataFTSE100Aggregator,
    GetIchimokuTKxDataFTSE100MultiTFMerger,
    GetSymbolFTSE100,
    GetIchimokuCloudDataFTSE100Aggregator,
    GetDataFTSE100,
    GetIchimokuKijunDataFTSE100,
    GetIchimokuKijunDataFTSE100Aggregator,
    GetKickerDataFTSE100,
    GetKickerDataFTSE100Aggregator,
    GetIchimokuSumCloudTKxDataFTSE100MultiTFMerger,
)

fetch_symbols_latest_FTSE100 = True
fetch_FTSE100_1H = True
fetch_FTSE100_D = True
fetch_FTSE100_W = True
fetch_FTSE100_M = True
run_Multi_TimeFrame_Merger_FTSE100 = True

fetch_kijun_analysis = False

# Use "Datetime" for Yahoo intraday data,
# "Date" for D, W, M data.
# Use "Datetime" for all Oanda data.
fetch_Kicker_use_datetime_format = False


def main(
    fetch_symbols_latest_FTSE100,
    fetch_FTSE100_1H,
    fetch_FTSE100_D,
    fetch_FTSE100_W,
    fetch_FTSE100_M,
    fetch_Kicker_use_datetime_format,
    run_Multi_TimeFrame_Merger_FTSE100,
):
    # Stop script being auto-run by Replit or Gitpod
    # return

    # ---------------- FTSE 100 ----------------

    # 1. Grab latest symbols
    _getSymbolFTSE100 = GetSymbolFTSE100
    _getSymbolFTSE100.main(fetch_symbols_latest_FTSE100)

    # 2. Download latest OHLC data for each symbol
    _getDataFTSE100 = GetDataFTSE100
    _getDataFTSE100.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W, fetch_FTSE100_M
    )

    # 3. Produce Ichimoku Cloud data for each symbol
    _getIchimokuCloudDataFTSE100 = GetIchimokuCloudDataFTSE100
    _getIchimokuCloudDataFTSE100.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W, fetch_FTSE100_M
    )

    # 3.1 Combine latest cloud signals of all symbols into one spreadsheet
    _getIchimokuCloudDataFTSE100Aggregator = (
        GetIchimokuCloudDataFTSE100Aggregator
    )
    _getIchimokuCloudDataFTSE100Aggregator.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W, fetch_FTSE100_M
    )

    # 3.2 Merge Multi Time Frame Cloud signals
    _getIchimokuCloudDataFTSE100MultiTFMerger = (
        GetIchimokuCloudDataFTSE100MultiTFMerger
    )
    _getIchimokuCloudDataFTSE100MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_FTSE100
    )

    # 3.3 Produce Ichimoku TK Cross data
    _getIchimokuTKxDataFTSE100 = GetIchimokuTKxDataFTSE100
    _getIchimokuTKxDataFTSE100.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W, fetch_FTSE100_M
    )

    # 3.4 Combine latest TK Cross signals from all symbols into one spreadsheet
    _getIchimokuTKxDataFTSE100Aggregator = GetIchimokuTKxDataFTSE100Aggregator
    _getIchimokuTKxDataFTSE100Aggregator.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W, fetch_FTSE100_M
    )

    # 3.5 Merge Multi Time Frame TKx signals
    _getIchimokuTKxDataFTSE100MultiTFMerger = (
        GetIchimokuTKxDataFTSE100MultiTFMerger
    )
    _getIchimokuTKxDataFTSE100MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_FTSE100
    )

    # 3.6 Merge Multi Time Frame Cloud and TKx Sum signals
    _getIchimokuSumCloudTKxDataFTSE100MultiTFMerger = (
        GetIchimokuSumCloudTKxDataFTSE100MultiTFMerger
    )
    _getIchimokuSumCloudTKxDataFTSE100MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_FTSE100
    )

    # 4. Produce Kijun data
    _getIchimokuKijunDataFTSE100 = GetIchimokuKijunDataFTSE100
    _getIchimokuKijunDataFTSE100.main(
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
    )

    # 4.1 Combine latest Kijun signals from all symbols into one spreadsheet
    _getIchimokuKijunDataFTSE100Aggregator = (
        GetIchimokuKijunDataFTSE100Aggregator
    )
    _getIchimokuKijunDataFTSE100Aggregator.main(
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
    )

    # 5. Produce Kicker data
    _getKickerDataFTSE100 = GetKickerDataFTSE100
    _getKickerDataFTSE100.main(
        fetch_Kicker_use_datetime_format,
        fetch_FTSE100_D,
        fetch_FTSE100_W,
        fetch_FTSE100_M,
    )

    # 5.1 Combine latest Kicker signals from all symbols into one spreadsheet
    _getKickerDataFTSE100Aggregator = GetKickerDataFTSE100Aggregator
    _getKickerDataFTSE100Aggregator.main(
        fetch_Kicker_use_datetime_format,
        fetch_FTSE100_D,
        fetch_FTSE100_W,
        fetch_FTSE100_M,
    )

    print("\nTasks completed.")


if __name__ == "__main__":
    main(
        fetch_symbols_latest_FTSE100,
        fetch_FTSE100_1H,
        fetch_FTSE100_D,
        fetch_FTSE100_W,
        fetch_FTSE100_M,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_FTSE100,
    )
