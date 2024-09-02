from src.mvc.controllers import (
    GetDataKraken,
    GetIchimokuCloudDataKraken,
    GetIchimokuCloudDataKrakenAggregator,
    GetIchimokuCloudDataKrakenMultiTFMerger,
    GetIchimokuTKxDataKraken,
    GetIchimokuTKxDataKrakenAggregator,
    GetIchimokuTKxDataKrakenMultiTFMerger,
    GetIchimokuSumCloudTKxDataKrakenMultiTFMerger,
)
from datetime import datetime
from pytz import timezone

fetch_Kraken_1H = True
fetch_Kraken_4H = True
fetch_Kraken_D = True
fetch_Kraken_W = True
fetch_Kraken_M = True

run_Multi_TimeFrame_Merger_Kraken = True

fetch_Kicker_use_datetime_format = False
fetch_kicker = False


def main(
    fetch_Kraken_1H=fetch_Kraken_1H,
    fetch_Kraken_4H=fetch_Kraken_4H,
    fetch_Kraken_D=fetch_Kraken_D,
    fetch_Kraken_W=fetch_Kraken_W,
    fetch_Kraken_M=fetch_Kraken_M,
    fetch_Kicker_use_datetime_format=fetch_Kicker_use_datetime_format,
    run_Multi_TimeFrame_Merger_Kraken=run_Multi_TimeFrame_Merger_Kraken,
    fetch_kicker=fetch_kicker,
):
    # Stop script being auto-run by Replit or Gitpod
    # return

    london_tz_start = timezone("Europe/London")
    time_start = datetime.now(london_tz_start)
    time_start_formatted = time_start.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Task begins at: {time_start_formatted} [UK]")

    # ----------------  Kraken ----------------

    # 1. Grab latest symbols - NA
    # 2. Download latest OHLC data for each symbol
    _getDataKraken = GetDataKraken
    _getDataKraken.main(
        fetch_Kraken_1H,
        fetch_Kraken_4H,
        fetch_Kraken_D,
        fetch_Kraken_W,
        fetch_Kraken_M,
    )

    # 3. Produce Ichimoku Cloud data for each symbol
    _getIchimokuCloudDataKraken = GetIchimokuCloudDataKraken
    _getIchimokuCloudDataKraken.main(
        fetch_Kraken_1H,
        fetch_Kraken_4H,
        fetch_Kraken_D,
        fetch_Kraken_W,
        fetch_Kraken_M,
    )

    # 3.1 Combine latest cloud signals of all symbols into one spreadsheet
    _getIchimokuCloudDataKrakenAggregator = (
        GetIchimokuCloudDataKrakenAggregator
    )
    _getIchimokuCloudDataKrakenAggregator.main(
        fetch_Kraken_1H,
        fetch_Kraken_4H,
        fetch_Kraken_D,
        fetch_Kraken_W,
        fetch_Kraken_M,
    )

    # 3.2 Merge Multi Time Frame Cloud signals
    _getIchimokuCloudDataKrakenMultiTFMerger = (
        GetIchimokuCloudDataKrakenMultiTFMerger
    )
    _getIchimokuCloudDataKrakenMultiTFMerger.main()

    # 3.3 Produce Ichimoku TK Cross data
    _getIchimokuTKxDataKraken = GetIchimokuTKxDataKraken
    _getIchimokuTKxDataKraken.main(
        fetch_Kraken_1H,
        fetch_Kraken_4H,
        fetch_Kraken_D,
        fetch_Kraken_W,
        fetch_Kraken_M,
    )

    # 3.4 Combine latest TK Cross signals from all symbols into one spreadsheet
    _getIchimokuTKxDataKrakenAggregator = GetIchimokuTKxDataKrakenAggregator
    _getIchimokuTKxDataKrakenAggregator.main(
        fetch_Kraken_1H,
        fetch_Kraken_4H,
        fetch_Kraken_D,
        fetch_Kraken_W,
        fetch_Kraken_M,
    )

    # 3.5 Merge Multi Time Frame TKx signals
    _getIchimokuTKxDataKrakenMultiTFMerger = (
        GetIchimokuTKxDataKrakenMultiTFMerger
    )
    _getIchimokuTKxDataKrakenMultiTFMerger.main(
        run_Multi_TimeFrame_Merger_Kraken
    )

    # 3.6 Merge Multi Time Frame Cloud and TKx Sum signals
    _getIchimokuSumCloudTKxDataKrakenMultiTFMerger = (
        GetIchimokuSumCloudTKxDataKrakenMultiTFMerger
    )
    _getIchimokuSumCloudTKxDataKrakenMultiTFMerger.main(
        run_Multi_TimeFrame_Merger_Kraken
    )

    # calculate time elapsed
    london_tz_finish = timezone("Europe/London")
    time_finish = datetime.now(london_tz_finish)
    time_elapsed = time_finish - time_start
    time_finish_formatted = time_finish.strftime("%Y-%m-%d %H:%M:%S")
    print(
        f"\nTasks completed at {time_finish_formatted} [UK] (Time elapsed: {time_elapsed})",
    )


if __name__ == "__main__":
    main(
        fetch_Kraken_1H,
        fetch_Kraken_4H,
        fetch_Kraken_D,
        fetch_Kraken_W,
        fetch_Kraken_M,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_Kraken,
        fetch_kicker,
    )
