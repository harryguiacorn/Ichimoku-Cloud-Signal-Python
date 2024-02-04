from src.mvc.controllers import (
    GetDataBitfinex,
    GetIchimokuCloudDataBitfinex,
    GetIchimokuCloudDataBitfinexAggregator,
    GetIchimokuCloudDataBitfinexMultiTFMerger,
    GetIchimokuTKxDataBitfinex,
    GetIchimokuTKxDataBitfinexAggregator,
    GetIchimokuTKxDataBitfinexMultiTFMerger,
    GetIchimokuSumCloudTKxDataBitfinexMultiTFMerger,
)
from datetime import datetime

fetch_Bitfinex_1H = True
fetch_Bitfinex_4H = True
fetch_Bitfinex_D = True
fetch_Bitfinex_W = True
fetch_Bitfinex_M = True

run_Multi_TimeFrame_Merger_Bitfinex = True

fetch_Kicker_use_datetime_format = False
fetch_kicker = False


def main(
    fetch_Bitfinex_1H,
    fetch_Bitfinex_4H,
    fetch_Bitfinex_D,
    fetch_Bitfinex_W,
    fetch_Bitfinex_M,
    fetch_Kicker_use_datetime_format,
    run_Multi_TimeFrame_Merger_Bitfinex,
    fetch_kicker,
):
    # Stop script being auto-run by Replit or Gitpod
    # return

    time_start = datetime.now()
    print("Task begins at:", time_start.strftime("%Y-%m-%d %H:%M:%S"), "\n")

    # ----------------  Bitfinex ----------------

    # 1. Grab latest symbols - NA
    # 2. Download latest OHLC data for each symbol
    _getDataBitfinex = GetDataBitfinex
    _getDataBitfinex.main(
        fetch_Bitfinex_1H,
        fetch_Bitfinex_4H,
        fetch_Bitfinex_D,
        fetch_Bitfinex_W,
        fetch_Bitfinex_M,
    )

    # 3. Produce Ichimoku Cloud data for each symbol
    _getIchimokuCloudDataBitfinex = GetIchimokuCloudDataBitfinex
    _getIchimokuCloudDataBitfinex.main(
        fetch_Bitfinex_1H,
        fetch_Bitfinex_4H,
        fetch_Bitfinex_D,
        fetch_Bitfinex_W,
        fetch_Bitfinex_M,
    )

    # 3.1 Combine latest cloud signals of all symbols into one spreadsheet
    _getIchimokuCloudDataBitfinexAggregator = (
        GetIchimokuCloudDataBitfinexAggregator
    )
    _getIchimokuCloudDataBitfinexAggregator.main(
        fetch_Bitfinex_1H,
        fetch_Bitfinex_4H,
        fetch_Bitfinex_D,
        fetch_Bitfinex_W,
        fetch_Bitfinex_M,
    )

    # 3.2 Merge Multi Time Frame Cloud signals
    _getIchimokuCloudDataBitfinexMultiTFMerger = (
        GetIchimokuCloudDataBitfinexMultiTFMerger
    )
    _getIchimokuCloudDataBitfinexMultiTFMerger.main()

    # 3.3 Produce Ichimoku TK Cross data
    _getIchimokuTKxDataBitfinex = GetIchimokuTKxDataBitfinex
    _getIchimokuTKxDataBitfinex.main(
        fetch_Bitfinex_1H,
        fetch_Bitfinex_4H,
        fetch_Bitfinex_D,
        fetch_Bitfinex_W,
        fetch_Bitfinex_M,
    )

    # 3.4 Combine latest TK Cross signals from all symbols into one spreadsheet
    _getIchimokuTKxDataBitfinexAggregator = (
        GetIchimokuTKxDataBitfinexAggregator
    )
    _getIchimokuTKxDataBitfinexAggregator.main(
        fetch_Bitfinex_1H,
        fetch_Bitfinex_4H,
        fetch_Bitfinex_D,
        fetch_Bitfinex_W,
        fetch_Bitfinex_M,
    )

    # 3.5 Merge Multi Time Frame TKx signals
    _getIchimokuTKxDataBitfinexMultiTFMerger = (
        GetIchimokuTKxDataBitfinexMultiTFMerger
    )
    _getIchimokuTKxDataBitfinexMultiTFMerger.main(
        run_Multi_TimeFrame_Merger_Bitfinex
    )

    # 3.6 Merge Multi Time Frame Cloud and TKx Sum signals
    _getIchimokuSumCloudTKxDataBitfinexMultiTFMerger = (
        GetIchimokuSumCloudTKxDataBitfinexMultiTFMerger
    )
    _getIchimokuSumCloudTKxDataBitfinexMultiTFMerger.main(
        run_Multi_TimeFrame_Merger_Bitfinex
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
        fetch_Bitfinex_1H,
        fetch_Bitfinex_4H,
        fetch_Bitfinex_D,
        fetch_Bitfinex_W,
        fetch_Bitfinex_M,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_Bitfinex,
        fetch_kicker,
    )
