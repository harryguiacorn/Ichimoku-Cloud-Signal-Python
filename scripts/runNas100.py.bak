from src.mvc.controllers import (
    GetIchimokuCloudDataNAS100,
    GetIchimokuCloudDataNAS100Aggregator,
    GetIchimokuCloudDataNAS100MultiTFMerger,
    GetIchimokuTKxDataNas100,
    GetIchimokuTKxDataNas100Aggregator,
    GetSymbolNAS100,
    GetDataNas100,
    GetIchimokuKijunDataNas100,
    GetIchimokuKijunDataNas100Aggregator,
    GetKickerDataNas100,
    GetKickerDataNas100Aggregator,
    GetIchimokuTKxDataNas100MultiTFMerger,
    GetIchimokuSumCloudTKxDataNas100MultiTFMerger,
)
from scripts._bootstrap import ensure_repo_root, setup_runner_logging

ensure_repo_root()
RUNNER_CLASS = ""
log_file = setup_runner_logging(__name__, RUNNER_CLASS)
import logging

logger = logging.getLogger(__name__)

from datetime import datetime
from pytz import timezone

fetch_symbols_latest_Nas100 = True

fetch_Nas100_1H = True
fetch_Nas100_D = True
fetch_Nas100_W = True
fetch_Nas100_M = True

run_Multi_TimeFrame_Merger_Nas100 = True

fetch_kijun_analysis = False

fetch_kicker = False

# Use "Datetime" for Yahoo intraday data,
# "Date" for D, W, M data.
# Use "Datetime" for all Oanda data.
fetch_Kicker_use_datetime_format = False


def main(
    fetch_symbols_latest_Nas100=fetch_symbols_latest_Nas100,
    fetch_Nas100_1H=fetch_Nas100_1H,
    fetch_Nas100_D=fetch_Nas100_D,
    fetch_Nas100_W=fetch_Nas100_W,
    fetch_Nas100_M=fetch_Nas100_M,
    fetch_kijun_analysis=fetch_kijun_analysis,
    fetch_Kicker_use_datetime_format=fetch_Kicker_use_datetime_format,
    run_Multi_TimeFrame_Merger_Nas100=run_Multi_TimeFrame_Merger_Nas100,
    fetch_kicker=fetch_kicker,
):
    # Stop script being auto-run by Replit or Gitpod
    # return

    london_tz_start = timezone("Europe/London")
    time_start = datetime.now(london_tz_start)
    time_start_formatted = time_start.strftime("%Y-%m-%d %H:%M:%S")
    logger.info("Nasdaq 100 task begins at: %s [UK]", time_start_formatted)

    # ---------------- Nasdaq 100 ----------------

    # 1. Grab latest symbols
    _getSymbolNAS100 = GetSymbolNAS100
    _getSymbolNAS100.main(fetch_symbols_latest_Nas100)

    # 2. Download latest OHLC data for each symbol
    _getDataNas100 = GetDataNas100
    _getDataNas100.main(
        fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W, fetch_Nas100_M
    )

    # 3. Produce Ichimoku Cloud data for each symbol
    _getIchimokuCloudDataNas100 = GetIchimokuCloudDataNAS100
    _getIchimokuCloudDataNas100.main(
        fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W, fetch_Nas100_M
    )

    # 3.1 Combine latest cloud signals of all symbols into one spreadsheet
    _getIchimokuCloudDataNas100Aggregator = (
        GetIchimokuCloudDataNAS100Aggregator
    )
    _getIchimokuCloudDataNas100Aggregator.main(
        fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W, fetch_Nas100_M
    )

    # 3.2 Merge Multi Time Frame Cloud signals
    _getIchimokuCloudDataNAS100MultiTFMerger = (
        GetIchimokuCloudDataNAS100MultiTFMerger
    )
    _getIchimokuCloudDataNAS100MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_Nas100
    )

    # 3.3 Produce Ichimoku TK Cross data
    _getIchimokuTKxDataNas100 = GetIchimokuTKxDataNas100
    _getIchimokuTKxDataNas100.main(
        fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W, fetch_Nas100_M
    )

    # 3.4 Combine latest TK Cross signals from all symbols into one spreadsheet
    _getIchimokuTKxDataNas100Aggregator = GetIchimokuTKxDataNas100Aggregator
    _getIchimokuTKxDataNas100Aggregator.main(
        fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W, fetch_Nas100_M
    )

    # 3.5 Merge Multi Time Frame TKx signals
    _getIchimokuTKxDataNas100MultiTFMerger = (
        GetIchimokuTKxDataNas100MultiTFMerger
    )
    _getIchimokuTKxDataNas100MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_Nas100
    )

    # 3.6 Merge Multi Time Frame Cloud and TKx Sum signals
    _getIchimokuSumCloudTKxDataNas100MultiTFMerger = (
        GetIchimokuSumCloudTKxDataNas100MultiTFMerger
    )
    _getIchimokuSumCloudTKxDataNas100MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_Nas100
    )

    # 4. Produce Kijun data
    _getIchimokuKijunDataNas100 = GetIchimokuKijunDataNas100
    _getIchimokuKijunDataNas100.main(
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
    )

    # 4.1 Combine latest Kijun signals from all symbols into one spreadsheet
    _getIchimokuKijunDataNas100Aggregator = (
        GetIchimokuKijunDataNas100Aggregator
    )
    _getIchimokuKijunDataNas100Aggregator.main(
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
        fetch_kijun_analysis,
    )
    if fetch_kicker:
        # 5. Produce Kicker data
        _getKickerDataNas100 = GetKickerDataNas100
        _getKickerDataNas100.main(
            fetch_Kicker_use_datetime_format,
            fetch_Nas100_D,
            fetch_Nas100_W,
            fetch_Nas100_M,
        )

        # 5.1 Combine latest Kicker signals from all symbols into one spreadsheet
        _getKickerDataNas100Aggregator = GetKickerDataNas100Aggregator
        _getKickerDataNas100Aggregator.main(
            fetch_Kicker_use_datetime_format,
            fetch_Nas100_D,
            fetch_Nas100_W,
            fetch_Nas100_M,
        )

    # calculate time elapsed
    london_tz_finish = timezone("Europe/London")
    time_finish = datetime.now(london_tz_finish)
    time_elapsed = time_finish - time_start
    time_finish_formatted = time_finish.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(
        "Nasdaq 100 tasks completed at %s [UK] (Time elapsed: %s)",
        time_finish_formatted,
        time_elapsed,
    )


if __name__ == "__main__":
    main(
        fetch_symbols_latest_Nas100,
        fetch_Nas100_1H,
        fetch_Nas100_D,
        fetch_Nas100_W,
        fetch_Nas100_M,
        fetch_kijun_analysis,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_Nas100,
        fetch_kicker,
    )
