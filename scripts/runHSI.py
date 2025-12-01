from src.mvc.controllers import (
    GetIchimokuCloudDataHSI,
    GetIchimokuCloudDataHSIMultiTFMerger,
    GetIchimokuTKxDataHSI,
    GetIchimokuTKxDataHSIAggregator,
    GetIchimokuTKxDataHSIMultiTFMerger,
    GetSymbolHSI,
    GetIchimokuCloudDataHSIAggregator,
    GetDataHSI,
    # GetIchimokuKijunDataHSI,
    # GetIchimokuKijunDataHSIAggregator,
    # GetKickerDataHSI,
    # GetKickerDataHSIAggregator,
    GetIchimokuSumCloudTKxDataHSIMultiTFMerger,
)
from scripts._bootstrap import ensure_repo_root, setup_runner_logging

ensure_repo_root()
RUNNER_CLASS = ""
log_file = setup_runner_logging(__name__, RUNNER_CLASS)
import logging

logger = logging.getLogger(__name__)

from datetime import datetime
from pytz import timezone

fetch_symbols_latest_HSI = True
fetch_HSI_1H = True
fetch_HSI_D = True
fetch_HSI_W = True
fetch_HSI_M = True
run_Multi_TimeFrame_Merger_HSI = True

fetch_kijun_analysis = False

# Use "Datetime" for Yahoo intraday data,
# "Date" for D, W, M data.
# Use "Datetime" for all Oanda data.
fetch_Kicker_use_datetime_format = False

fetch_kicker = False


def main(
    fetch_symbols_latest_HSI=fetch_symbols_latest_HSI,
    fetch_HSI_1H=fetch_HSI_1H,
    fetch_HSI_D=fetch_HSI_D,
    fetch_HSI_W=fetch_HSI_W,
    fetch_HSI_M=fetch_HSI_M,
    fetch_kijun_analysis=fetch_kijun_analysis,
    fetch_Kicker_use_datetime_format=fetch_Kicker_use_datetime_format,
    run_Multi_TimeFrame_Merger_HSI=run_Multi_TimeFrame_Merger_HSI,
    fetch_kicker=fetch_kicker,
):
    # Stop script being auto-run by Replit or Gitpod
    # return

    london_tz_start = timezone("Europe/London")
    time_start = datetime.now(london_tz_start)
    time_start_formatted = time_start.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(
        "Hang Seng Index task begins at: %s [UK]", time_start_formatted
    )

    # ---------------- Hang Seng Index ----------------

    # 1. Grab latest symbols
    _getSymbolHSI = GetSymbolHSI
    _getSymbolHSI.main(fetch_symbols_latest_HSI)

    # 2. Download latest OHLC data for each symbol
    _getDataHSI = GetDataHSI
    _getDataHSI.main(fetch_HSI_1H, fetch_HSI_D, fetch_HSI_W, fetch_HSI_M)

    # 3. Produce Ichimoku Cloud data for each symbol
    _getIchimokuCloudDataHSI = GetIchimokuCloudDataHSI
    _getIchimokuCloudDataHSI.main(
        fetch_HSI_1H, fetch_HSI_D, fetch_HSI_W, fetch_HSI_M
    )

    # 3.1 Combine latest cloud signals of all symbols into one spreadsheet
    _getIchimokuCloudDataHSIAggregator = GetIchimokuCloudDataHSIAggregator
    _getIchimokuCloudDataHSIAggregator.main(
        fetch_HSI_1H, fetch_HSI_D, fetch_HSI_W, fetch_HSI_M
    )

    # 3.2 Merge Multi Time Frame Cloud signals
    _getIchimokuCloudDataHSIMultiTFMerger = (
        GetIchimokuCloudDataHSIMultiTFMerger
    )
    _getIchimokuCloudDataHSIMultiTFMerger.main(run_Multi_TimeFrame_Merger_HSI)

    # 3.3 Produce Ichimoku TK Cross data
    _getIchimokuTKxDataHSI = GetIchimokuTKxDataHSI
    _getIchimokuTKxDataHSI.main(
        fetch_HSI_1H, fetch_HSI_D, fetch_HSI_W, fetch_HSI_M
    )

    # 3.4 Combine latest TK Cross signals from all symbols into one spreadsheet
    _getIchimokuTKxDataHSIAggregator = GetIchimokuTKxDataHSIAggregator
    _getIchimokuTKxDataHSIAggregator.main(
        fetch_HSI_1H, fetch_HSI_D, fetch_HSI_W, fetch_HSI_M
    )

    # 3.5 Merge Multi Time Frame TKx signals
    _getIchimokuTKxDataHSIMultiTFMerger = GetIchimokuTKxDataHSIMultiTFMerger
    _getIchimokuTKxDataHSIMultiTFMerger.main(run_Multi_TimeFrame_Merger_HSI)

    # 3.6 Merge Multi Time Frame Cloud and TKx Sum signals
    _getIchimokuSumCloudTKxDataHSIMultiTFMerger = (
        GetIchimokuSumCloudTKxDataHSIMultiTFMerger
    )
    _getIchimokuSumCloudTKxDataHSIMultiTFMerger.main(
        run_Multi_TimeFrame_Merger_HSI
    )

    # # 4. Produce Kijun data
    # _getIchimokuKijunDataHSI = GetIchimokuKijunDataHSI
    # _getIchimokuKijunDataHSI.main(
    #     fetch_kijun_analysis,
    #     fetch_kijun_analysis,
    #     fetch_kijun_analysis,
    #     fetch_kijun_analysis,
    # )

    # # 4.1 Combine latest Kijun signals from all symbols into one spreadsheet
    # _getIchimokuKijunDataHSIAggregator = GetIchimokuKijunDataHSIAggregator
    # _getIchimokuKijunDataHSIAggregator.main(
    #     fetch_kijun_analysis,
    #     fetch_kijun_analysis,
    #     fetch_kijun_analysis,
    #     fetch_kijun_analysis,
    # )

    # if fetch_kicker:
    #     # 5. Produce Kicker data
    #     _getKickerDataHSI = GetKickerDataHSI
    #     _getKickerDataHSI.main(
    #         fetch_Kicker_use_datetime_format,
    #         fetch_HSI_D,
    #         fetch_HSI_W,
    #         fetch_HSI_M,
    #     )

    #     # 5.1 Combine latest Kicker signals from all symbols into one spreadsheet
    #     _getKickerDataHSIAggregator = GetKickerDataHSIAggregator
    #     _getKickerDataHSIAggregator.main(
    #         fetch_Kicker_use_datetime_format,
    #         fetch_HSI_D,
    #         fetch_HSI_W,
    #         fetch_HSI_M,
    #     )

    # calculate time elapsed
    london_tz_finish = timezone("Europe/London")
    time_finish = datetime.now(london_tz_finish)
    time_elapsed = time_finish - time_start
    time_finish_formatted = time_finish.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(
        "Hang Seng Index tasks completed at %s [UK] (Time elapsed: %s)",
        time_finish_formatted,
        time_elapsed,
    )


if __name__ == "__main__":
    main(
        fetch_symbols_latest_HSI,
        fetch_HSI_1H,
        fetch_HSI_D,
        fetch_HSI_W,
        fetch_HSI_M,
        fetch_kijun_analysis,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_HSI,
        fetch_kicker,
    )
