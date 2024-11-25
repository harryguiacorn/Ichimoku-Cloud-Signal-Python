from src.mvc.controllers import (
    GetDataRussell1000,
    GetIchimokuCloudDataRussell1000,
    GetIchimokuCloudDataRussell1000Aggregator,
    GetIchimokuCloudDataRussell1000MultiTFMerger,
    # GetIchimokuTKxDataRussell1000,
    # GetIchimokuTKxDataRussell1000Aggregator,
    # GetSymbolRussell1000,
    # GetIchimokuKijunDataRussell1000,
    # GetIchimokuKijunDataRussell1000Aggregator,
    # GetKickerDataRussell1000,
    # GetKickerDataRussell1000Aggregator,
    # GetIchimokuTKxDataRussell1000MultiTFMerger,
    # GetIchimokuSumCloudTKxDataRussell1000MultiTFMerger,
)
from datetime import datetime
from pytz import timezone

fetch_symbols_latest_Russell1000 = True

fetch_Russell1000_1H = True
fetch_Russell1000_D = True
fetch_Russell1000_W = True
fetch_Russell1000_M = True

run_Multi_TimeFrame_Merger_Russell1000 = True

fetch_kijun_analysis = False

# Use "Datetime" for Yahoo intraday data,
# "Date" for D, W, M data.
# Use "Datetime" for all Oanda data.
fetch_Kicker_use_datetime_format = False

fetch_kicker = False


def __init__(self):
    pass


def main(
    fetch_symbols_latest_Russell1000=fetch_symbols_latest_Russell1000,
    fetch_Russell1000_1H=fetch_Russell1000_1H,
    fetch_Russell1000_D=fetch_Russell1000_D,
    fetch_Russell1000_W=fetch_Russell1000_W,
    fetch_Russell1000_M=fetch_Russell1000_M,
    fetch_kijun_analysis=fetch_kijun_analysis,
    fetch_Kicker_use_datetime_format=fetch_Kicker_use_datetime_format,
    run_Multi_TimeFrame_Merger_Russell1000=run_Multi_TimeFrame_Merger_Russell1000,
    fetch_kicker=fetch_kicker,
):
    # ---------------- Russell 1000 ----------------

    london_tz_start = timezone("Europe/London")
    time_start = datetime.now(london_tz_start)
    time_start_formatted = time_start.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Dow Jones 30 task begins at: {time_start_formatted} [UK]")

    # # 1. Grab latest symbols
    # _getSymbolRussell1000 = GetSymbolRussell1000
    # _getSymbolRussell1000.main(fetch_symbols_latest_Russell1000)

    # 2. Download latest OHLC data for each symbol
    _getDataRussell1000 = GetDataRussell1000
    _getDataRussell1000.main(fetch_Russell1000_1H, fetch_Russell1000_D, fetch_Russell1000_W, fetch_Russell1000_M)

    # 3. Produce Ichimoku Cloud data for each symbol
    _getIchimokuCloudDataRussell1000 = GetIchimokuCloudDataRussell1000
    _getIchimokuCloudDataRussell1000.main(
        fetch_Russell1000_1H, fetch_Russell1000_D, fetch_Russell1000_W, fetch_Russell1000_M
    )

    
    # 3.1 Combine latest cloud signals of all symbols into one spreadsheet
    _getIchimokuCloudDataRussell1000Aggregator = GetIchimokuCloudDataRussell1000Aggregator
    _getIchimokuCloudDataRussell1000Aggregator.main(
        fetch_Russell1000_1H, fetch_Russell1000_D, fetch_Russell1000_W, fetch_Russell1000_M
    )

    # 3.2 Merge Multi Time Frame Cloud signals
    _getIchimokuCloudDataRussell1000MultiTFMerger = (
        GetIchimokuCloudDataRussell1000MultiTFMerger
    )
    _getIchimokuCloudDataRussell1000MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_Russell1000
    )

    return
    # 3.3 Produce Ichimoku TK Cross data
    _getIchimokuTKxDataRussell1000 = GetIchimokuTKxDataRussell1000
    _getIchimokuTKxDataRussell1000.main(
        fetch_Russell1000_1H, fetch_Russell1000_D, fetch_Russell1000_W, fetch_Russell1000_M
    )

    # 3.4 Combine latest TK Cross signals from all symbols into one spreadsheet
    _getIchimokuTKxDataRussell1000Aggregator = GetIchimokuTKxDataRussell1000Aggregator
    _getIchimokuTKxDataRussell1000Aggregator.main(
        fetch_Russell1000_1H, fetch_Russell1000_D, fetch_Russell1000_W, fetch_Russell1000_M
    )

    # 3.5 Merge Multi Time Frame TKx signals
    _getIchimokuTKxDataRussell1000MultiTFMerger = GetIchimokuTKxDataRussell1000MultiTFMerger
    _getIchimokuTKxDataRussell1000MultiTFMerger.main(run_Multi_TimeFrame_Merger_Russell1000)

    # 3.6 Merge Multi Time Frame Cloud and TKx Sum signals
    _getIchimokuSumCloudTKxDataRussell1000MultiTFMerger = (
        GetIchimokuSumCloudTKxDataRussell1000MultiTFMerger
    )
    _getIchimokuSumCloudTKxDataRussell1000MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_Russell1000
    )

    # 4. Produce Kijun data
    _getIchimokuKijunDataRussell1000 = GetIchimokuKijunDataRussell1000
    _getIchimokuKijunDataRussell1000.main(
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
    )

    # 4.1 Combine latest Kijun signals from all symbols into one spreadsheet
    _getIchimokuKijunDataRussell1000Aggregator = GetIchimokuKijunDataRussell1000Aggregator
    _getIchimokuKijunDataRussell1000Aggregator.main(
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
    )

    if fetch_kicker:
        # 5. Produce Kicker data
        _getKickerDataRussell1000 = GetKickerDataRussell1000
        _getKickerDataRussell1000.main(
            fetch_Kicker_use_datetime_format,
            fetch_Russell1000_D,
            fetch_Russell1000_W,
            fetch_Russell1000_M,
        )

        # 5.1 Combine latest Kicker signals from all symbols into one spreadsheet
        _getKickerDataRussell1000Aggregator = GetKickerDataRussell1000Aggregator
        _getKickerDataRussell1000Aggregator.main(
            fetch_Kicker_use_datetime_format,
            fetch_Russell1000_D,
            fetch_Russell1000_W,
            fetch_Russell1000_M,
        )

    # calculate time elapsed
    london_tz_finish = timezone("Europe/London")
    time_finish = datetime.now(london_tz_finish)
    time_elapsed = time_finish - time_start
    time_finish_formatted = time_finish.strftime("%Y-%m-%d %H:%M:%S")
    print(
        f"\nDow Jones 30 tasks completed at {time_finish_formatted} [UK] (Time elapsed: {time_elapsed})",
    )


if __name__ == "__main__":
    main(
        fetch_symbols_latest_Russell1000,
        fetch_Russell1000_1H,
        fetch_Russell1000_D,
        fetch_Russell1000_W,
        fetch_Russell1000_M,
        fetch_kijun_analysis,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_Russell1000,
        fetch_kicker,
    )
