from src.mvc.controllers import (
    GetDataSPDR_ETFS,
    GetIchimokuCloudDataSPDR_ETFSAggregator,
    GetIchimokuCloudDataSPDR_ETFSMultiTFMerger,
    GetIchimokuTKxDataSPDR_ETFS,
    GetIchimokuTKxDataSPDR_ETFSAggregator,
    # GetIchimokuKijunDataSPDR_ETFS,
    # GetIchimokuKijunDataSPDR_ETFSAggregator,
    GetIchimokuSumCloudTKxDataMatchSPY_SPDR_ETFSMultiTFMerger,
    GetIchimokuCloudDataSPDR_ETFS,
    GetKickerDataSPDR_ETFS,
    GetKickerDataSPDR_ETFSAggregator,
    GetIchimokuTKxDataSPDR_ETFSMultiTFMerger,
    GetIchimokuSumCloudTKxDataSPDR_ETFSMultiTFMerger,
)
from datetime import datetime
from pytz import timezone

fetch_symbols_latest_SPDR_ETFS = True

fetch_SPDR_ETFS_1H = True
fetch_SPDR_ETFS_D = True
fetch_SPDR_ETFS_W = True
fetch_SPDR_ETFS_M = True

run_Multi_TimeFrame_Merger_SPDR_ETFS = True
run_Multi_TimeFrame_Merger_Individual_SPDR_ETFS = True

fetch_kijun_analysis = False

# Use "Datetime" for Yahoo intraday data,
# "Date" for D, W, M data.
# Use "Datetime" for all Oanda data.
fetch_Kicker_use_datetime_format = False

fetch_kicker = False


def __init__(self):
    pass


def main(
    fetch_symbols_latest_SPDR_ETFS=fetch_symbols_latest_SPDR_ETFS,
    fetch_SPDR_ETFS_1H=fetch_SPDR_ETFS_1H,
    fetch_SPDR_ETFS_D=fetch_SPDR_ETFS_D,
    fetch_SPDR_ETFS_W=fetch_SPDR_ETFS_W,
    fetch_SPDR_ETFS_M=fetch_SPDR_ETFS_M,
    fetch_kijun_analysis=fetch_kijun_analysis,
    fetch_Kicker_use_datetime_format=fetch_Kicker_use_datetime_format,
    run_Multi_TimeFrame_Merger_SPDR_ETFS=run_Multi_TimeFrame_Merger_SPDR_ETFS,
    fetch_kicker=fetch_kicker,
):
    # ---------------- Dow Jones 30 ----------------

    london_tz_start = timezone("Europe/London")
    time_start = datetime.now(london_tz_start)
    time_start_formatted = time_start.strftime("%Y-%m-%d %H:%M:%S")
    print(f"SPDR ETFs task begins at: {time_start_formatted} [UK]")

    # # 1. Grab latest symbols

    # 2. Download latest OHLC data for each symbol
    _getDataSPDR_ETFS = GetDataSPDR_ETFS
    _getDataSPDR_ETFS.main(
        fetch_SPDR_ETFS_1H,
        fetch_SPDR_ETFS_D,
        fetch_SPDR_ETFS_W,
        fetch_SPDR_ETFS_M,
    )

    # 3. Produce Ichimoku Cloud data for each symbol
    _getIchimokuCloudDataSPDR_ETFS = GetIchimokuCloudDataSPDR_ETFS
    _getIchimokuCloudDataSPDR_ETFS.main(
        fetch_SPDR_ETFS_1H,
        fetch_SPDR_ETFS_D,
        fetch_SPDR_ETFS_W,
        fetch_SPDR_ETFS_M,
    )

    # 3.1 Combine latest cloud signals of all symbols into one spreadsheet
    _getIchimokuCloudDataSPDR_ETFSAggregator = (
        GetIchimokuCloudDataSPDR_ETFSAggregator
    )
    _getIchimokuCloudDataSPDR_ETFSAggregator.main(
        fetch_SPDR_ETFS_1H,
        fetch_SPDR_ETFS_D,
        fetch_SPDR_ETFS_W,
        fetch_SPDR_ETFS_M,
    )

    # 3.2 Merge Multi Time Frame Cloud signals
    _getIchimokuCloudDataSPDR_ETFSMultiTFMerger = (
        GetIchimokuCloudDataSPDR_ETFSMultiTFMerger
    )
    _getIchimokuCloudDataSPDR_ETFSMultiTFMerger.main(
        run_Multi_TimeFrame_Merger_SPDR_ETFS
    )

    # 3.3 Produce Ichimoku TK Cross data
    _getIchimokuTKxDataSPDR_ETFS = GetIchimokuTKxDataSPDR_ETFS
    _getIchimokuTKxDataSPDR_ETFS.main(
        fetch_SPDR_ETFS_1H,
        fetch_SPDR_ETFS_D,
        fetch_SPDR_ETFS_W,
        fetch_SPDR_ETFS_M,
    )

    # 3.4 Combine latest TK Cross signals from all symbols into one spreadsheet
    _getIchimokuTKxDataSPDR_ETFSAggregator = (
        GetIchimokuTKxDataSPDR_ETFSAggregator
    )
    _getIchimokuTKxDataSPDR_ETFSAggregator.main(
        fetch_SPDR_ETFS_1H,
        fetch_SPDR_ETFS_D,
        fetch_SPDR_ETFS_W,
        fetch_SPDR_ETFS_M,
    )

    # 3.5 Merge Multi Time Frame TKx signals
    _getIchimokuTKxDataSPDR_ETFSMultiTFMerger = (
        GetIchimokuTKxDataSPDR_ETFSMultiTFMerger
    )
    _getIchimokuTKxDataSPDR_ETFSMultiTFMerger.main(
        run_Multi_TimeFrame_Merger_SPDR_ETFS
    )

    # 3.6 Merge Multi Time Frame Cloud and TKx Sum signals
    _getIchimokuSumCloudTKxDataSPDR_ETFSMultiTFMerger = (
        GetIchimokuSumCloudTKxDataSPDR_ETFSMultiTFMerger
    )
    _getIchimokuSumCloudTKxDataSPDR_ETFSMultiTFMerger.main(
        run_Multi_TimeFrame_Merger_SPDR_ETFS
    )

    # 4. Produce Kijun data
    # _getIchimokuKijunDataSPDR_ETFS = GetIchimokuKijunDataSPDR_ETFS
    # _getIchimokuKijunDataSPDR_ETFS.main(
    #     fetch_kijun_analysis,
    #     fetch_kijun_analysis,
    #     fetch_kijun_analysis,
    #     fetch_kijun_analysis,
    # )

    # 4.1 Combine latest Kijun signals from all symbols into one spreadsheet
    # _getIchimokuKijunDataSPDR_ETFSAggregator = GetIchimokuKijunDataSPDR_ETFSAggregator
    # _getIchimokuKijunDataSPDR_ETFSAggregator.main(
    #     fetch_kijun_analysis,
    #     fetch_kijun_analysis,
    #     fetch_kijun_analysis,
    #     fetch_kijun_analysis,
    # )

    # 6.1 Create individual ETF constituents scan
    _getIchimokuSumCloudTKxDataMatchSPY_SPDR_ETFSMultiTFMerger = (
        GetIchimokuSumCloudTKxDataMatchSPY_SPDR_ETFSMultiTFMerger
    )
    _getIchimokuSumCloudTKxDataMatchSPY_SPDR_ETFSMultiTFMerger.main(
        run_Multi_TimeFrame_Merger_Individual_SPDR_ETFS
    )

    if fetch_kicker:
        # 5. Produce Kicker data
        _getKickerDataSPDR_ETFS = GetKickerDataSPDR_ETFS
        _getKickerDataSPDR_ETFS.main(
            fetch_Kicker_use_datetime_format,
            fetch_SPDR_ETFS_D,
            fetch_SPDR_ETFS_W,
            fetch_SPDR_ETFS_M,
        )

        # 5.1 Combine latest Kicker signals from all symbols into one spreadsheet
        _getKickerDataSPDR_ETFSAggregator = GetKickerDataSPDR_ETFSAggregator
        _getKickerDataSPDR_ETFSAggregator.main(
            fetch_Kicker_use_datetime_format,
            fetch_SPDR_ETFS_D,
            fetch_SPDR_ETFS_W,
            fetch_SPDR_ETFS_M,
        )

    # calculate time elapsed
    london_tz_finish = timezone("Europe/London")
    time_finish = datetime.now(london_tz_finish)
    time_elapsed = time_finish - time_start
    time_finish_formatted = time_finish.strftime("%Y-%m-%d %H:%M:%S")
    print(
        f"\nSPDR ETFs tasks completed at {time_finish_formatted} [UK] (Time elapsed: {time_elapsed})",
    )


if __name__ == "__main__":
    main(
        fetch_symbols_latest_SPDR_ETFS,
        fetch_SPDR_ETFS_1H,
        fetch_SPDR_ETFS_D,
        fetch_SPDR_ETFS_W,
        fetch_SPDR_ETFS_M,
        fetch_kijun_analysis,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_SPDR_ETFS,
        fetch_kicker,
    )
