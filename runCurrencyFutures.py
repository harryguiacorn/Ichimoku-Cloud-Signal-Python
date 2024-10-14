from src.mvc.controllers import (
    GetIchimokuCloudDataFuturesCurrency,
    GetIchimokuCloudDataFuturesCurrencyAggregator,
    GetIchimokuTKxDataFuturesCurrency,
    GetIchimokuTKxDataFuturesCurrencyAggregator,
    GetIchimokuTKxDataFuturesCurrencyMultiTFMerger,
    GetDataFuturesCurrency,
    GetIchimokuKijunDataFuturesCurrency,
    GetIchimokuKijunDataFuturesCurrencyAggregator,
    GetKickerDataFuturesCurrency,
    GetKickerDataFuturesCurrencyAggregator,
    GetIchimokuCloudDataFuturesCurrencyMultiTFMerger,
    GetIchimokuSumCloudTKxDataFuturesCurrencyMultiTFMerger,
)
from datetime import datetime
from pytz import timezone

fetch_symbols_latest_CurrencyFutures = False

fetch_CurrencyFutures_1H = True
fetch_CurrencyFutures_D = True
fetch_CurrencyFutures_W = True
fetch_CurrencyFutures_M = True

run_Multi_TimeFrame_Merger_CurrencyFutures = True

fetch_kijun_analysis = False

fetch_kicker = False

# Use "Datetime" for Yahoo intraday data,
# "Date" for D, W, M data.
# Use "Datetime" for all Oanda data.
fetch_Kicker_use_datetime_format = False


def main(
    fetch_symbols_latest_CurrencyFutures=fetch_symbols_latest_CurrencyFutures,
    fetch_CurrencyFutures_1H=fetch_CurrencyFutures_1H,
    fetch_CurrencyFutures_D=fetch_CurrencyFutures_D,
    fetch_CurrencyFutures_W=fetch_CurrencyFutures_W,
    fetch_CurrencyFutures_M=fetch_CurrencyFutures_M,
    fetch_kijun_analysis=fetch_kijun_analysis,
    fetch_Kicker_use_datetime_format=fetch_Kicker_use_datetime_format,
    run_Multi_TimeFrame_Merger_CurrencyFutures=run_Multi_TimeFrame_Merger_CurrencyFutures,
    fetch_kicker=fetch_kicker,
):
    # Stop script being auto-run by Replit or Gitpod
    # return

    london_tz_start = timezone("Europe/London")
    time_start = datetime.now(london_tz_start)
    time_start_formatted = time_start.strftime("%Y-%m-%d %H:%M:%S")
    print(f"CurrencyFutures task begins at: {time_start_formatted} [UK]")

    # ---------------- Futures Currency ----------------

    # 1. Currency Futures list is hard coded to only include the majors.

    # 2. Download latest OHLC data for each symbol
    _getDataFuturesCurrency = GetDataFuturesCurrency
    _getDataFuturesCurrency.main(
        fetch_CurrencyFutures_1H,
        fetch_CurrencyFutures_D,
        fetch_CurrencyFutures_W,
        fetch_CurrencyFutures_M,
    )

    # 3. Produce Ichimoku Cloud data for each symbol
    _getIchimokuCloudDataFuturesCurrency = GetIchimokuCloudDataFuturesCurrency
    _getIchimokuCloudDataFuturesCurrency.main(
        fetch_CurrencyFutures_1H,
        fetch_CurrencyFutures_D,
        fetch_CurrencyFutures_W,
        fetch_CurrencyFutures_M,
    )

    # 3.1 Combine latest cloud signals of all symbols into one spreadsheet
    _getIchimokuCloudDataFuturesCurrencyAggregator = (
        GetIchimokuCloudDataFuturesCurrencyAggregator
    )
    _getIchimokuCloudDataFuturesCurrencyAggregator.main(
        fetch_CurrencyFutures_1H,
        fetch_CurrencyFutures_D,
        fetch_CurrencyFutures_W,
        fetch_CurrencyFutures_M,
    )

    # 3.2 Merge Multi Time Frame Cloud signals
    _getIchimokuCloudDataFuturesCurrencyMultiTFMerger = (
        GetIchimokuCloudDataFuturesCurrencyMultiTFMerger
    )
    _getIchimokuCloudDataFuturesCurrencyMultiTFMerger.main(
        run_Multi_TimeFrame_Merger_CurrencyFutures
    )

    # 3.3 Produce Ichimoku TK Cross data
    _getIchimokuTKxDataFuturesCurrency = GetIchimokuTKxDataFuturesCurrency
    _getIchimokuTKxDataFuturesCurrency.main(
        fetch_CurrencyFutures_1H,
        fetch_CurrencyFutures_D,
        fetch_CurrencyFutures_W,
        fetch_CurrencyFutures_M,
    )

    # 3.4 Combine latest TK Cross signals from all symbols into one spreadsheet
    _getIchimokuTKxDataFuturesCurrencyAggregator = (
        GetIchimokuTKxDataFuturesCurrencyAggregator
    )
    _getIchimokuTKxDataFuturesCurrencyAggregator.main(
        fetch_CurrencyFutures_1H,
        fetch_CurrencyFutures_D,
        fetch_CurrencyFutures_W,
        fetch_CurrencyFutures_M,
    )

    # 3.5 Merge Multi Time Frame TKx signals
    _getIchimokuTKxDataFuturesCurrencyMultiTFMerger = (
        GetIchimokuTKxDataFuturesCurrencyMultiTFMerger
    )
    _getIchimokuTKxDataFuturesCurrencyMultiTFMerger.main(
        run_Multi_TimeFrame_Merger_CurrencyFutures
    )

    # 3.6 Merge Multi Time Frame Cloud and TKx Sum signals
    _getIchimokuSumCloudTKxDataFuturesCurrencyMultiTFMerger = (
        GetIchimokuSumCloudTKxDataFuturesCurrencyMultiTFMerger
    )
    _getIchimokuSumCloudTKxDataFuturesCurrencyMultiTFMerger.main(
        run_Multi_TimeFrame_Merger_CurrencyFutures
    )

    # 4. Produce Kijun data
    _getIchimokuKijunDataFuturesCurrency = GetIchimokuKijunDataFuturesCurrency
    _getIchimokuKijunDataFuturesCurrency.main(
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
    )

    # 4.1 Combine latest Kijun signals from all symbols into one spreadsheet
    _getIchimokuKijunDataFuturesCurrencyAggregator = (
        GetIchimokuKijunDataFuturesCurrencyAggregator
    )
    _getIchimokuKijunDataFuturesCurrencyAggregator.main(
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
    )

    if fetch_kicker:
        # 5. Produce Kicker data
        _getKickerDataFuturesCurrency = GetKickerDataFuturesCurrency
        _getKickerDataFuturesCurrency.main(
            fetch_Kicker_use_datetime_format,
            fetch_CurrencyFutures_D,
            fetch_CurrencyFutures_W,
            fetch_CurrencyFutures_M,
        )

        # 5.1 Combine latest Kicker signals from all symbols into one spreadsheet
        _getKickerDataFuturesCurrencyAggregator = (
            GetKickerDataFuturesCurrencyAggregator
        )
        _getKickerDataFuturesCurrencyAggregator.main(
            fetch_Kicker_use_datetime_format,
            fetch_CurrencyFutures_D,
            fetch_CurrencyFutures_W,
            fetch_CurrencyFutures_M,
        )

    # calculate time elapsed
    london_tz_finish = timezone("Europe/London")
    time_finish = datetime.now(london_tz_finish)
    time_elapsed = time_finish - time_start
    time_finish_formatted = time_finish.strftime("%Y-%m-%d %H:%M:%S")
    print(
        f"\nCurrencyFutures tasks completed at {time_finish_formatted} [UK] (Time elapsed: {time_elapsed})",
    )


if __name__ == "__main__":
    main(
        fetch_symbols_latest_CurrencyFutures,
        fetch_CurrencyFutures_1H,
        fetch_CurrencyFutures_D,
        fetch_CurrencyFutures_W,
        fetch_CurrencyFutures_M,
        fetch_kijun_analysis,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_CurrencyFutures,
        fetch_kicker,
    )
