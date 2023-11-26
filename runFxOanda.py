from src.mvc.controllers import (
    GetDataOanda,
    GetIchimokuCloudDataOanda,
    GetIchimokuCloudDataOandaAggregator,
    GetIchimokuCloudDataOandaMultiTFMerger,
    GetIchimokuTKxDataOanda,
    GetIchimokuTKxDataOandaAggregator,
    GetIchimokuTKxDataOandaMultiTFMerger,
)


fetch_ForexOanda_1H = True

fetch_ForexOanda_4H = True

fetch_ForexOanda_D = True

fetch_ForexOanda_W = True

fetch_ForexOanda_M = False

fetch_Kicker_use_datetime_format = False

run_Multi_TimeFrame_Merger_Oanda = True


def main():
    # Stop script being auto-run by Replit or Gitpod
    # return

    # ---------------- Forex Oanda ----------------

    # 1. Grab latest symbols - NA
    # 2. Download latest OHLC data for each symbol
    _getDataForexOanda = GetDataOanda
    _getDataForexOanda.main(
        fetch_ForexOanda_1H,
        fetch_ForexOanda_4H,
        fetch_ForexOanda_D,
        fetch_ForexOanda_W,
        fetch_ForexOanda_M,
    )

    # 3. Produce Ichimoku Cloud data for each symbol
    _getIchimokuCloudDataOanda = GetIchimokuCloudDataOanda
    _getIchimokuCloudDataOanda.main(
        fetch_ForexOanda_1H,
        fetch_ForexOanda_4H,
        fetch_ForexOanda_D,
        fetch_ForexOanda_W,
        fetch_ForexOanda_M,
    )

    # 3.1 Combine latest cloud signals of all symbols into one spreadsheet
    _getIchimokuCloudDataOandaAggregator = GetIchimokuCloudDataOandaAggregator
    _getIchimokuCloudDataOandaAggregator.main(
        fetch_ForexOanda_1H,
        fetch_ForexOanda_4H,
        fetch_ForexOanda_D,
        fetch_ForexOanda_W,
        fetch_ForexOanda_M,
    )

    # 3.2 Merge Multi Time Frame Cloud signals
    _getIchimokuCloudDataOandaMultiTFMerger = (
        GetIchimokuCloudDataOandaMultiTFMerger
    )
    _getIchimokuCloudDataOandaMultiTFMerger.main()

    # 3.3 Produce Ichimoku TK Cross data
    _getIchimokuTKxDataOanda = GetIchimokuTKxDataOanda
    _getIchimokuTKxDataOanda.main(
        fetch_ForexOanda_1H,
        fetch_ForexOanda_4H,
        fetch_ForexOanda_D,
        fetch_ForexOanda_W,
        fetch_ForexOanda_M,
    )

    # 3.4 Combine latest TK Cross signals from all symbols into one spreadsheet
    _getIchimokuTKxDataOandaAggregator = GetIchimokuTKxDataOandaAggregator
    _getIchimokuTKxDataOandaAggregator.main(
        fetch_ForexOanda_1H,
        fetch_ForexOanda_4H,
        fetch_ForexOanda_D,
        fetch_ForexOanda_W,
        fetch_ForexOanda_M,
    )

    # 3.5 Merge Multi Time Frame TKx signals
    _getIchimokuTKxDataOandaMultiTFMerger = (
        GetIchimokuTKxDataOandaMultiTFMerger
    )
    _getIchimokuTKxDataOandaMultiTFMerger.main(
        run_Multi_TimeFrame_Merger_Oanda
    )

    print(f"Tasks completed.")


if __name__ == "__main__":
    main()
