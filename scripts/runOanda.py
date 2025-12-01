from src.mvc.controllers import (
    GetDataOanda,
    GetIchimokuCloudDataOanda,
    GetIchimokuCloudDataOandaAggregator,
    GetIchimokuCloudDataOandaMultiTFMerger,
    GetIchimokuTKxDataOanda,
    GetIchimokuTKxDataOandaAggregator,
    GetIchimokuTKxDataOandaMultiTFMerger,
    GetIchimokuSumCloudTKxDataOandaMultiTFMerger,
)
from scripts._bootstrap import ensure_repo_root, setup_runner_logging

ensure_repo_root()
RUNNER_CLASS = ""
log_file = setup_runner_logging(__name__, RUNNER_CLASS)
import logging

logger = logging.getLogger(__name__)

from datetime import datetime
from pytz import timezone

fetch_Oanda_1H = True
fetch_Oanda_4H = True
fetch_Oanda_D = True
fetch_Oanda_W = True
fetch_Oanda_M = True

run_Multi_TimeFrame_Merger_Oanda = True

fetch_Kicker_use_datetime_format = False

fetch_kijun_analysis = False

fetch_kicker = False


def main(
    fetch_Oanda_1H=fetch_Oanda_1H,
    fetch_Oanda_4H=fetch_Oanda_4H,
    fetch_Oanda_D=fetch_Oanda_D,
    fetch_Oanda_W=fetch_Oanda_W,
    fetch_Oanda_M=fetch_Oanda_M,
    fetch_kijun_analysis=fetch_kijun_analysis,
    fetch_Kicker_use_datetime_format=fetch_Kicker_use_datetime_format,
    run_Multi_TimeFrame_Merger_Oanda=run_Multi_TimeFrame_Merger_Oanda,
    fetch_kicker=fetch_kicker,
):
    # Stop script being auto-run by Replit or Gitpod
    # return

    london_tz_start = timezone("Europe/London")
    time_start = datetime.now(london_tz_start)
    time_start_formatted = time_start.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Oanda task begins at: {time_start_formatted} [UK]")

    # ----------------  Oanda ----------------

    # 1. Grab latest symbols - NA
    # 2. Download latest OHLC data for each symbol
    _getDataOanda = GetDataOanda
    _getDataOanda.main(
        fetch_Oanda_1H,
        fetch_Oanda_4H,
        fetch_Oanda_D,
        fetch_Oanda_W,
        fetch_Oanda_M,
    )

    # 3. Produce Ichimoku Cloud data for each symbol
    _getIchimokuCloudDataOanda = GetIchimokuCloudDataOanda
    _getIchimokuCloudDataOanda.main(
        fetch_Oanda_1H,
        fetch_Oanda_4H,
        fetch_Oanda_D,
        fetch_Oanda_W,
        fetch_Oanda_M,
    )

    # 3.1 Combine latest cloud signals of all symbols into one spreadsheet
    _getIchimokuCloudDataOandaAggregator = GetIchimokuCloudDataOandaAggregator
    _getIchimokuCloudDataOandaAggregator.main(
        fetch_Oanda_1H,
        fetch_Oanda_4H,
        fetch_Oanda_D,
        fetch_Oanda_W,
        fetch_Oanda_M,
    )
    # 3.2 Merge Multi Time Frame Cloud signals
    _getIchimokuCloudDataOandaMultiTFMerger = (
        GetIchimokuCloudDataOandaMultiTFMerger
    )
    _getIchimokuCloudDataOandaMultiTFMerger.main()

    # 3.3 Produce Ichimoku TK Cross data
    _getIchimokuTKxDataOanda = GetIchimokuTKxDataOanda
    _getIchimokuTKxDataOanda.main(
        fetch_Oanda_1H,
        fetch_Oanda_4H,
        fetch_Oanda_D,
        fetch_Oanda_W,
        fetch_Oanda_M,
    )

    # 3.4 Combine latest TK Cross signals from all symbols into one spreadsheet
    _getIchimokuTKxDataOandaAggregator = GetIchimokuTKxDataOandaAggregator
    _getIchimokuTKxDataOandaAggregator.main(
        fetch_Oanda_1H,
        fetch_Oanda_4H,
        fetch_Oanda_D,
        fetch_Oanda_W,
        fetch_Oanda_M,
    )

    # 3.5 Merge Multi Time Frame TKx signals
    _getIchimokuTKxDataOandaMultiTFMerger = (
        GetIchimokuTKxDataOandaMultiTFMerger
    )
    _getIchimokuTKxDataOandaMultiTFMerger.main(
        run_Multi_TimeFrame_Merger_Oanda
    )

    # 3.6 Merge Multi Time Frame Cloud and TKx Sum signals
    _getIchimokuSumCloudTKxDataOandaMultiTFMerger = (
        GetIchimokuSumCloudTKxDataOandaMultiTFMerger
    )
    _getIchimokuSumCloudTKxDataOandaMultiTFMerger.main(
        run_Multi_TimeFrame_Merger_Oanda
    )

    # calculate time elapsed
    london_tz_finish = timezone("Europe/London")
    time_finish = datetime.now(london_tz_finish)
    time_elapsed = time_finish - time_start
    time_finish_formatted = time_finish.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(
        "Oanda tasks completed at %s [UK] (Time elapsed: %s)",
        time_finish_formatted,
        time_elapsed,
    )


if __name__ == "__main__":
    main(
        fetch_Oanda_1H,
        fetch_Oanda_4H,
        fetch_Oanda_D,
        fetch_Oanda_W,
        fetch_Oanda_M,
        fetch_kijun_analysis,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_Oanda,
        fetch_kicker,
    )
