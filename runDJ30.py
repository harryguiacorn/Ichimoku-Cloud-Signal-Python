from src.mvc.controllers import (
    GetDataDJ30,
    GetIchimokuCloudDataDJ30Aggregator,
    GetIchimokuCloudDataDJ30MultiTFMerger,
    GetIchimokuTKxDataDJ30,
    GetIchimokuTKxDataDJ30Aggregator,
    GetSymbolDowJones30,
    GetIchimokuKijunDataDJ30,
    GetIchimokuCloudDataDJ30,
    GetIchimokuKijunDataDJ30Aggregator,
    GetKickerDataDJ30,
    GetKickerDataDJ30Aggregator,
    GetIchimokuTKxDataDJ30MultiTFMerger,
    GetIchimokuSumCloudTKxDataDJ30MultiTFMerger,
)
from datetime import datetime
from pytz import timezone

fetch_symbols_latest_DJ30 = True

fetch_DJ30_1H = True
fetch_DJ30_D = True
fetch_DJ30_W = True
fetch_DJ30_M = True

run_Multi_TimeFrame_Merger_DJ30 = True

fetch_kijun_analysis = False

# Use "Datetime" for Yahoo intraday data,
# "Date" for D, W, M data.
# Use "Datetime" for all Oanda data.
fetch_Kicker_use_datetime_format = False

fetch_kicker = False


def __init__(self):
    pass


def main(
    fetch_symbols_latest_DJ30=fetch_symbols_latest_DJ30,
    fetch_DJ30_1H=fetch_DJ30_1H,
    fetch_DJ30_D=fetch_DJ30_D,
    fetch_DJ30_W=fetch_DJ30_W,
    fetch_DJ30_M=fetch_DJ30_M,
    fetch_kijun_analysis=fetch_kijun_analysis,
    fetch_Kicker_use_datetime_format=fetch_Kicker_use_datetime_format,
    run_Multi_TimeFrame_Merger_DJ30=run_Multi_TimeFrame_Merger_DJ30,
    fetch_kicker=fetch_kicker,
):
    # ---------------- Dow Jones 30 ----------------

    london_tz_start = timezone("Europe/London")
    time_start = datetime.now(london_tz_start)
    time_start_formatted = time_start.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Dow Jones 30 task begins at: {time_start_formatted} [UK]")

    # 1. Grab latest symbols
    _getSymbolDowJones30 = GetSymbolDowJones30
    _getSymbolDowJones30.main(fetch_symbols_latest_DJ30)

    # 2. Download latest OHLC data for each symbol
    _getDataDJ30 = GetDataDJ30
    _getDataDJ30.main(fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W, fetch_DJ30_M)

    # 3. Produce Ichimoku Cloud data for each symbol
    _getIchimokuCloudDataDJ30 = GetIchimokuCloudDataDJ30
    _getIchimokuCloudDataDJ30.main(
        fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W, fetch_DJ30_M
    )

    # 3.1 Combine latest cloud signals of all symbols into one spreadsheet
    _getIchimokuCloudDataDJ30Aggregator = GetIchimokuCloudDataDJ30Aggregator
    _getIchimokuCloudDataDJ30Aggregator.main(
        fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W, fetch_DJ30_M
    )

    # 3.2 Merge Multi Time Frame Cloud signals
    _getIchimokuCloudDataDJ30MultiTFMerger = (
        GetIchimokuCloudDataDJ30MultiTFMerger
    )
    _getIchimokuCloudDataDJ30MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_DJ30
    )

    # 3.3 Produce Ichimoku TK Cross data
    _getIchimokuTKxDataDJ30 = GetIchimokuTKxDataDJ30
    _getIchimokuTKxDataDJ30.main(
        fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W, fetch_DJ30_M
    )

    # 3.4 Combine latest TK Cross signals from all symbols into one spreadsheet
    _getIchimokuTKxDataDJ30Aggregator = GetIchimokuTKxDataDJ30Aggregator
    _getIchimokuTKxDataDJ30Aggregator.main(
        fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W, fetch_DJ30_M
    )

    # 3.5 Merge Multi Time Frame TKx signals
    _getIchimokuTKxDataDJ30MultiTFMerger = GetIchimokuTKxDataDJ30MultiTFMerger
    _getIchimokuTKxDataDJ30MultiTFMerger.main(run_Multi_TimeFrame_Merger_DJ30)

    # 3.6 Merge Multi Time Frame Cloud and TKx Sum signals
    _getIchimokuSumCloudTKxDataDJ30MultiTFMerger = (
        GetIchimokuSumCloudTKxDataDJ30MultiTFMerger
    )
    _getIchimokuSumCloudTKxDataDJ30MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_DJ30
    )

    # 4. Produce Kijun data
    _getIchimokuKijunDataDJ30 = GetIchimokuKijunDataDJ30
    _getIchimokuKijunDataDJ30.main(
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
    )

    # 4.1 Combine latest Kijun signals from all symbols into one spreadsheet
    _getIchimokuKijunDataDJ30Aggregator = GetIchimokuKijunDataDJ30Aggregator
    _getIchimokuKijunDataDJ30Aggregator.main(
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
    )

    if fetch_kicker:
        # 5. Produce Kicker data
        _getKickerDataDJ30 = GetKickerDataDJ30
        _getKickerDataDJ30.main(
            fetch_Kicker_use_datetime_format,
            fetch_DJ30_D,
            fetch_DJ30_W,
            fetch_DJ30_M,
        )

        # 5.1 Combine latest Kicker signals from all symbols into one spreadsheet
        _getKickerDataDJ30Aggregator = GetKickerDataDJ30Aggregator
        _getKickerDataDJ30Aggregator.main(
            fetch_Kicker_use_datetime_format,
            fetch_DJ30_D,
            fetch_DJ30_W,
            fetch_DJ30_M,
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
        fetch_symbols_latest_DJ30,
        fetch_DJ30_1H,
        fetch_DJ30_D,
        fetch_DJ30_W,
        fetch_DJ30_M,
        fetch_kijun_analysis,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_DJ30,
        fetch_kicker,
    )
