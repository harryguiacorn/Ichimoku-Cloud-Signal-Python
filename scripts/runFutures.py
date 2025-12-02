from src.mvc.controllers import (
    GetIchimokuCloudDataFutures,
    GetIchimokuCloudDataFuturesAggregator,
    GetIchimokuCloudDataFuturesMultiTFMerger,
    GetIchimokuTKxDataFutures,
    GetIchimokuTKxDataFuturesAggregator,
    GetIchimokuTKxDataFuturesMultiTFMerger,
    GetSymbolFutures,
    GetDataFutures,
    GetIchimokuKijunDataFutures,
    GetIchimokuKijunDataFuturesAggregator,
    GetKickerDataFutures,
    GetKickerDataFuturesAggregator,
    GetIchimokuSumCloudTKxDataFuturesMultiTFMerger,
)
from scripts._bootstrap import ensure_repo_root, setup_runner_logging

ensure_repo_root()
RUNNER_CLASS = ""
log_file = setup_runner_logging(__name__, RUNNER_CLASS)
import logging

logger = logging.getLogger(__name__)

from datetime import datetime
from pytz import timezone

fetch_symbols_latest_Futures = True
fetch_Futures_1H = True
fetch_Futures_D = True
fetch_Futures_W = True
fetch_Futures_M = True
run_Multi_TimeFrame_Merger_Futures = True

fetch_kijun_analysis = False

fetch_kicker = False

# Use "Datetime" for Yahoo intraday data,
# "Date" for D, W, M data.
# Use "Datetime" for all Oanda data.
fetch_Kicker_use_datetime_format = False


def main(
    fetch_symbols_latest_Futures=fetch_symbols_latest_Futures,
    fetch_Futures_1H=fetch_Futures_1H,
    fetch_Futures_D=fetch_Futures_D,
    fetch_Futures_W=fetch_Futures_W,
    fetch_Futures_M=fetch_Futures_M,
    fetch_kijun_analysis=fetch_kijun_analysis,
    fetch_Kicker_use_datetime_format=fetch_Kicker_use_datetime_format,
    run_Multi_TimeFrame_Merger_Futures=run_Multi_TimeFrame_Merger_Futures,
    fetch_kicker=fetch_kicker,
):
    # Stop script being auto-run by Replit or Gitpod
    # return

    london_tz_start = timezone("Europe/London")
    time_start = datetime.now(london_tz_start)
    time_start_formatted = time_start.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Futures task begins at: {time_start_formatted} [UK]")

    # ---------------- Futures ----------------

    # 1. Grab latest symbols
    _getSymbolFutures = GetSymbolFutures
    _getSymbolFutures.main(fetch_symbols_latest_Futures)

    # 2. Download latest OHLC data for each symbol
    _getDataFutures = GetDataFutures
    _getDataFutures.main(
        fetch_Futures_1H, fetch_Futures_D, fetch_Futures_W, fetch_Futures_M
    )

    # 3. Produce Ichimoku Cloud data for each symbol
    _getIchimokuCloudDataFutures = GetIchimokuCloudDataFutures
    _getIchimokuCloudDataFutures.main(
        fetch_Futures_1H, fetch_Futures_D, fetch_Futures_W, fetch_Futures_M
    )

    # 3.1 Combine latest cloud signals of all symbols into one spreadsheet
    _getIchimokuDataFuturesAggregator = GetIchimokuCloudDataFuturesAggregator
    _getIchimokuDataFuturesAggregator.main(
        fetch_Futures_1H, fetch_Futures_D, fetch_Futures_W, fetch_Futures_M
    )

    # 3.2 Merge Multi Time Frame Cloud signals
    _getIchimokuCloudDataFuturesMultiTFMerger = (
        GetIchimokuCloudDataFuturesMultiTFMerger
    )
    _getIchimokuCloudDataFuturesMultiTFMerger.main(
        run_Multi_TimeFrame_Merger_Futures
    )

    # 3.3 Produce Ichimoku TK Cross data
    _getIchimokuTKxDataFutures = GetIchimokuTKxDataFutures
    _getIchimokuTKxDataFutures.main(
        fetch_Futures_1H, fetch_Futures_D, fetch_Futures_W, fetch_Futures_M
    )

    # 3.4 Combine latest TK Cross signals from all symbols into one spreadsheet
    _getIchimokuTKxDataFuturesAggregator = GetIchimokuTKxDataFuturesAggregator
    _getIchimokuTKxDataFuturesAggregator.main(
        fetch_Futures_1H, fetch_Futures_D, fetch_Futures_W, fetch_Futures_M
    )

    # 3.5 Merge Multi Time Frame TKx signals
    _getIchimokuTKxDataFuturesMultiTFMerger = (
        GetIchimokuTKxDataFuturesMultiTFMerger
    )
    _getIchimokuTKxDataFuturesMultiTFMerger.main(
        run_Multi_TimeFrame_Merger_Futures
    )

    # 3.6 Merge Multi Time Frame Cloud and TKx Sum signals
    _getIchimokuSumCloudTKxDataFuturesMultiTFMerger = (
        GetIchimokuSumCloudTKxDataFuturesMultiTFMerger
    )
    _getIchimokuSumCloudTKxDataFuturesMultiTFMerger.main(
        run_Multi_TimeFrame_Merger_Futures
    )

    # 4. Produce Kijun data
    _getIchimokuKijunDataFutures = GetIchimokuKijunDataFutures
    _getIchimokuKijunDataFutures.main(
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
    )

    # 4.1 Combine latest Kijun signals from all symbols into one spreadsheet
    _getIchimokuKijunDataFuturesAggregator = (
        GetIchimokuKijunDataFuturesAggregator
    )
    _getIchimokuKijunDataFuturesAggregator.main(
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
    )
    if fetch_kicker:
        # 5. Produce Kicker data
        _getKickerDataFutures = GetKickerDataFutures
        _getKickerDataFutures.main(
            fetch_Kicker_use_datetime_format,
            fetch_Futures_D,
            fetch_Futures_W,
            fetch_Futures_M,
        )

        # 5.1 Combine latest Kicker signals from all symbols into one spreadsheet
        _getKickerDataFuturesAggregator = GetKickerDataFuturesAggregator
        _getKickerDataFuturesAggregator.main(
            fetch_Kicker_use_datetime_format,
            fetch_Futures_D,
            fetch_Futures_W,
            fetch_Futures_M,
        )

    # calculate time elapsed
    london_tz_finish = timezone("Europe/London")
    time_finish = datetime.now(london_tz_finish)
    time_elapsed = time_finish - time_start
    time_finish_formatted = time_finish.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(
        "Futures tasks completed at %s [UK] (Time elapsed: %s)",
        time_finish_formatted,
        time_elapsed,
    )


if __name__ == "__main__":
    main(
        fetch_symbols_latest_Futures,
        fetch_Futures_1H,
        fetch_Futures_D,
        fetch_Futures_W,
        fetch_Futures_M,
        fetch_kijun_analysis,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_Futures,
        fetch_kicker,
    )
