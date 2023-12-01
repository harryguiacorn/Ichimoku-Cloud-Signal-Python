from src.mvc.controllers import (
    GetDataDJ30,
    GetIchimokuCloudDataDJ30Aggregator,
    GetIchimokuCloudDataDJ30MultiTFMerger,
    GetIchimokuCloudDataFTSE100,
    GetIchimokuCloudDataFTSE100MultiTFMerger,
    GetIchimokuCloudDataFTSE250,
    GetIchimokuCloudDataFTSE250Aggregator,
    GetIchimokuCloudDataFTSE250MultiTFMerger,
    GetIchimokuCloudDataFutures,
    GetIchimokuCloudDataFuturesAggregator,
    GetIchimokuCloudDataFuturesCurrency,
    GetIchimokuCloudDataFuturesCurrencyAggregator,
    GetIchimokuCloudDataFuturesMultiTFMerger,
    GetIchimokuCloudDataNAS100,
    GetIchimokuCloudDataNAS100Aggregator,
    GetIchimokuCloudDataNAS100MultiTFMerger,
    GetIchimokuCloudDataSPX500,
    GetIchimokuCloudDataSPX500Aggregator,
    GetIchimokuTKxDataDJ30,
    GetIchimokuTKxDataDJ30Aggregator,
    GetIchimokuTKxDataFTSE100,
    GetIchimokuTKxDataFTSE100Aggregator,
    GetIchimokuTKxDataFTSE100MultiTFMerger,
    GetIchimokuTKxDataFTSE250,
    GetIchimokuTKxDataFTSE250Aggregator,
    GetIchimokuTKxDataFTSE250MultiTFMerger,
    GetIchimokuTKxDataFutures,
    GetIchimokuTKxDataFuturesAggregator,
    GetIchimokuTKxDataFuturesCurrency,
    GetIchimokuTKxDataFuturesCurrencyAggregator,
    GetIchimokuTKxDataFuturesCurrencyMultiTFMerger,
    GetIchimokuTKxDataFuturesMultiTFMerger,
    GetIchimokuTKxDataNas100,
    GetIchimokuTKxDataNas100Aggregator,
    GetIchimokuTKxDataSPX500,
    GetIchimokuTKxDataSPX500Aggregator,
    GetSymbolDowJones30,
    GetSymbolFTSE100,
    GetSymbolFTSE250,
    GetSymbolFutures,
    GetSymbolNAS100,
    GetIchimokuCloudDataFTSE100Aggregator,
    GetSymbolSPX500,
    GetIchimokuKijunDataDJ30,
    GetIchimokuCloudDataDJ30,
    GetIchimokuKijunDataDJ30Aggregator,
    GetKickerDataDJ30,
    GetKickerDataDJ30Aggregator,
    GetDataNas100,
    GetIchimokuKijunDataNas100,
    GetIchimokuKijunDataNas100Aggregator,
    GetKickerDataNas100,
    GetKickerDataNas100Aggregator,
    GetDataFTSE100,
    GetIchimokuKijunDataFTSE100,
    GetIchimokuKijunDataFTSE100Aggregator,
    GetKickerDataFTSE100,
    GetKickerDataFTSE100Aggregator,
    GetDataFTSE250,
    GetIchimokuKijunDataFTSE250,
    GetIchimokuKijunDataFTSE250Aggregator,
    GetKickerDataFTSE250,
    GetKickerDataFTSE250Aggregator,
    GetDataSPX500,
    GetIchimokuKijunDataSPX500,
    GetIchimokuKijunDataSPX500Aggregator,
    GetKickerDataSPX500,
    GetKickerDataSPX500Aggregator,
    GetDataFutures,
    GetIchimokuCloudDataSPX500MultiTFMerger,
    GetIchimokuTKxDataDJ30MultiTFMerger,
    GetIchimokuKijunDataFutures,
    GetIchimokuKijunDataFuturesAggregator,
    GetKickerDataFutures,
    GetKickerDataFuturesAggregator,
    GetDataFuturesCurrency,
    GetIchimokuKijunDataFuturesCurrency,
    GetIchimokuKijunDataFuturesCurrencyAggregator,
    GetKickerDataFuturesCurrency,
    GetKickerDataFuturesCurrencyAggregator,
    GetIchimokuCloudDataFuturesCurrencyMultiTFMerger,
    GetIchimokuTKxDataNas100MultiTFMerger,
    GetIchimokuTKxDataSPX500MultiTFMerger,
)


fetch_symbols_latest = True

fetch_DJ30_1H = True
fetch_SPX500_1H = True
fetch_Nas100_1H = True
fetch_FTSE100_1H = False
fetch_FTSE250_1H = False
fetch_Futures_1H = False
fetch_CurrencyFutures_1H = False

fetch_DJ30_D = True
fetch_SPX500_D = True
fetch_Nas100_D = True
fetch_FTSE100_D = False
fetch_FTSE250_D = False
fetch_Futures_D = False
fetch_CurrencyFutures_D = False

fetch_DJ30_W = True
fetch_SPX500_W = True
fetch_Nas100_W = True
fetch_FTSE100_W = False
fetch_FTSE250_W = False
fetch_Futures_W = False
fetch_CurrencyFutures_W = False

fetch_DJ30_M = True
fetch_SPX500_M = True
fetch_Nas100_M = True
fetch_FTSE100_M = False
fetch_FTSE250_M = False
fetch_Futures_M = False
fetch_CurrencyFutures_M = False

run_Multi_TimeFrame_Merger_DJ30 = True
run_Multi_TimeFrame_Merger_SPX500 = True
run_Multi_TimeFrame_Merger_Nas100 = True
run_Multi_TimeFrame_Merger_FTSE100 = False
run_Multi_TimeFrame_Merger_FTSE250 = False
run_Multi_TimeFrame_Merger_Futures = False
run_Multi_TimeFrame_Merger_CurrencyFutures = False


# Use "Datetime" for Yahoo intraday data,
# "Date" for D, W, M data.
# Use "Datetime" for all Oanda data.
fetch_Kicker_use_datetime_format = False


def main():
    # Stop script being auto-run by Replit or Gitpod
    # return

    # ---------------- Dow Jones 30 ----------------

    # 1. Grab latest symbols
    _getSymbolDowJones30 = GetSymbolDowJones30
    _getSymbolDowJones30.main(fetch_symbols_latest)

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

    # 4. Produce Kijun data
    _getIchimokuKijunDataDJ30 = GetIchimokuKijunDataDJ30
    _getIchimokuKijunDataDJ30.main(
        fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W, fetch_DJ30_M
    )

    # 4.1 Combine latest Kijun signals from all symbols into one spreadsheet
    _getIchimokuKijunDataDJ30Aggregator = GetIchimokuKijunDataDJ30Aggregator
    _getIchimokuKijunDataDJ30Aggregator.main(
        fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W, fetch_DJ30_M
    )

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

    # ---------------- Nasdaq 100 ----------------

    # 1. Grab latest symbols
    _getSymbolNAS100 = GetSymbolNAS100
    _getSymbolNAS100.main(fetch_symbols_latest)

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

    # 4. Produce Kijun data
    _getIchimokuKijunDataDJ30 = GetIchimokuKijunDataDJ30
    _getIchimokuKijunDataDJ30.main(
        fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W, fetch_DJ30_M
    )

    # 4. Produce Kijun data
    _getIchimokuKijunDataNas100 = GetIchimokuKijunDataNas100
    _getIchimokuKijunDataNas100.main(
        fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W, fetch_Nas100_M
    )

    # 4.1 Combine latest Kijun signals from all symbols into one spreadsheet
    _getIchimokuKijunDataNas100Aggregator = (
        GetIchimokuKijunDataNas100Aggregator
    )
    _getIchimokuKijunDataNas100Aggregator.main(
        fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W, fetch_Nas100_M
    )

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

    # ---------------- FTSE 100 ----------------

    # 1. Grab latest symbols
    _getSymbolFTSE100 = GetSymbolFTSE100
    _getSymbolFTSE100.main(fetch_symbols_latest)

    # 2. Download latest OHLC data for each symbol
    _getDataFTSE100 = GetDataFTSE100
    _getDataFTSE100.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W, fetch_FTSE100_M
    )

    # 3. Produce Ichimoku Cloud data for each symbol
    _getIchimokuCloudDataFTSE100 = GetIchimokuCloudDataFTSE100
    _getIchimokuCloudDataFTSE100.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W, fetch_FTSE100_M
    )

    # 3.1 Combine latest cloud signals of all symbols into one spreadsheet
    _getIchimokuCloudDataFTSE100Aggregator = (
        GetIchimokuCloudDataFTSE100Aggregator
    )
    _getIchimokuCloudDataFTSE100Aggregator.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W, fetch_FTSE100_M
    )

    # 3.2 Merge Multi Time Frame Cloud signals
    _getIchimokuCloudDataFTSE100MultiTFMerger = (
        GetIchimokuCloudDataFTSE100MultiTFMerger
    )
    _getIchimokuCloudDataFTSE100MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_FTSE100
    )

    # 3.3 Produce Ichimoku TK Cross data
    _getIchimokuTKxDataFTSE100 = GetIchimokuTKxDataFTSE100
    _getIchimokuTKxDataFTSE100.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W, fetch_FTSE100_M
    )

    # 3.4 Combine latest TK Cross signals from all symbols into one spreadsheet
    _getIchimokuTKxDataFTSE100Aggregator = GetIchimokuTKxDataFTSE100Aggregator
    _getIchimokuTKxDataFTSE100Aggregator.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W, fetch_FTSE100_M
    )

    # 3.5 Merge Multi Time Frame TKx signals
    _getIchimokuTKxDataFTSE100MultiTFMerger = (
        GetIchimokuTKxDataFTSE100MultiTFMerger
    )
    _getIchimokuTKxDataFTSE100MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_FTSE100
    )

    # 4. Produce Kijun data
    _getIchimokuKijunDataFTSE100 = GetIchimokuKijunDataFTSE100
    _getIchimokuKijunDataFTSE100.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W, fetch_FTSE100_M
    )

    # 4.1 Combine latest Kijun signals from all symbols into one spreadsheet
    _getIchimokuKijunDataFTSE100Aggregator = (
        GetIchimokuKijunDataFTSE100Aggregator
    )
    _getIchimokuKijunDataFTSE100Aggregator.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W, fetch_FTSE100_M
    )

    # 5. Produce Kicker data
    _getKickerDataFTSE100 = GetKickerDataFTSE100
    _getKickerDataFTSE100.main(
        fetch_Kicker_use_datetime_format,
        fetch_FTSE100_D,
        fetch_FTSE100_W,
        fetch_FTSE100_M,
    )

    # 5.1 Combine latest Kicker signals from all symbols into one spreadsheet
    _getKickerDataFTSE100Aggregator = GetKickerDataFTSE100Aggregator
    _getKickerDataFTSE100Aggregator.main(
        fetch_Kicker_use_datetime_format,
        fetch_FTSE100_D,
        fetch_FTSE100_W,
        fetch_FTSE100_M,
    )

    # ---------------- FTSE 250 ----------------

    # 1. Grab latest symbols
    _getSymbolFTSE250 = GetSymbolFTSE250
    _getSymbolFTSE250.main(fetch_symbols_latest)

    # 2. Download latest OHLC data for each symbol
    _getDataFTSE250 = GetDataFTSE250
    _getDataFTSE250.main(
        fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W, fetch_FTSE250_M
    )

    # 3. Produce Ichimoku Cloud data for each symbol
    _getIchimokuCloudDataFTSE250 = GetIchimokuCloudDataFTSE250
    _getIchimokuCloudDataFTSE250.main(
        fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W, fetch_FTSE250_M
    )

    # 3.1 Combine latest cloud signals of all symbols into one spreadsheet
    _getIchimokuCloudDataFTSE250Aggregator = (
        GetIchimokuCloudDataFTSE250Aggregator
    )
    _getIchimokuCloudDataFTSE250Aggregator.main(
        fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W, fetch_FTSE250_M
    )

    # 3.2 Merge Multi Time Frame Cloud signals
    _getIchimokuCloudDataFTSE250MultiTFMerger = (
        GetIchimokuCloudDataFTSE250MultiTFMerger
    )
    _getIchimokuCloudDataFTSE250MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_FTSE250
    )

    # 3.3 Produce Ichimoku TK Cross data
    _gtIchimokuKijunDataFTSE250 = GetIchimokuTKxDataFTSE250
    _gtIchimokuKijunDataFTSE250.main(
        fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W, fetch_FTSE250_M
    )

    # 3.4 Combine latest TK Cross signals from all symbols into one spreadsheet
    _getIchimokuTKxDataFTSE250Aggregator = GetIchimokuTKxDataFTSE250Aggregator
    _getIchimokuTKxDataFTSE250Aggregator.main(
        fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W, fetch_FTSE250_M
    )

    # 3.5 Merge Multi Time Frame TKx signals
    _getIchimokuTKxDataFTSE250MultiTFMerger = (
        GetIchimokuTKxDataFTSE250MultiTFMerger
    )
    _getIchimokuTKxDataFTSE250MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_FTSE250
    )

    # 4. Produce Kijun data
    _getIchimokuKijunDataFTSE250 = GetIchimokuKijunDataFTSE250
    _getIchimokuKijunDataFTSE250.main(
        fetch_Kicker_use_datetime_format,
        fetch_FTSE250_D,
        fetch_FTSE250_W,
        fetch_FTSE250_M,
    )

    # 4.1 Combine latest Kijun signals from all symbols into one spreadsheet
    _getIchimokuKijunDataFTSE250Aggregator = (
        GetIchimokuKijunDataFTSE250Aggregator
    )
    _getIchimokuKijunDataFTSE250Aggregator.main(
        fetch_Kicker_use_datetime_format,
        fetch_FTSE250_D,
        fetch_FTSE250_W,
        fetch_FTSE250_M,
    )

    # 5. Produce Kicker data
    _getKickerDataFTSE250 = GetKickerDataFTSE250
    _getKickerDataFTSE250.main(
        fetch_Kicker_use_datetime_format,
        fetch_FTSE250_D,
        fetch_FTSE250_W,
        fetch_FTSE250_M,
    )

    # 5.1 Combine latest Kicker signals from all symbols into one spreadsheet
    _getKickerDataFTSE250Aggregator = GetKickerDataFTSE250Aggregator
    _getKickerDataFTSE250Aggregator.main(
        fetch_Kicker_use_datetime_format,
        fetch_FTSE250_D,
        fetch_FTSE250_W,
        fetch_FTSE250_M,
    )
    # ---------------- Futures ----------------

    # 1. Grab latest symbols
    _getSymbolFutures = GetSymbolFutures
    _getSymbolFutures.main(fetch_symbols_latest)

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

    # 4. Produce Kijun data
    _getIchimokuKijunDataFutures = GetIchimokuKijunDataFutures
    _getIchimokuKijunDataFutures.main(
        fetch_Futures_1H, fetch_Futures_D, fetch_Futures_W, fetch_Futures_M
    )

    # 4.1 Combine latest Kijun signals from all symbols into one spreadsheet
    _getIchimokuKijunDataFuturesAggregator = (
        GetIchimokuKijunDataFuturesAggregator
    )
    _getIchimokuKijunDataFuturesAggregator.main(
        fetch_Futures_1H, fetch_Futures_D, fetch_Futures_W, fetch_Futures_M
    )

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

    # 4. Produce Kijun data
    _getIchimokuKijunDataFuturesCurrency = GetIchimokuKijunDataFuturesCurrency
    _getIchimokuKijunDataFuturesCurrency.main(
        fetch_CurrencyFutures_1H,
        fetch_CurrencyFutures_D,
        fetch_CurrencyFutures_W,
        fetch_CurrencyFutures_M,
    )

    # 4.1 Combine latest Kijun signals from all symbols into one spreadsheet
    _getIchimokuKijunDataFuturesCurrencyAggregator = (
        GetIchimokuKijunDataFuturesCurrencyAggregator
    )
    _getIchimokuKijunDataFuturesCurrencyAggregator.main(
        fetch_CurrencyFutures_1H,
        fetch_CurrencyFutures_D,
        fetch_CurrencyFutures_W,
        fetch_CurrencyFutures_M,
    )

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

    # ---------------- S&P 500 ----------------

    # 1. Grab latest symbols
    _getSymbolSPX500 = GetSymbolSPX500
    _getSymbolSPX500.main(fetch_symbols_latest)

    # 2. Download latest OHLC data for each symbol
    _getDataSPX500 = GetDataSPX500
    _getDataSPX500.main(
        fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W, fetch_SPX500_M
    )

    # 3. Produce Ichimoku Cloud data for each symbol
    _getIchimokuCloudDataSPX500 = GetIchimokuCloudDataSPX500
    _getIchimokuCloudDataSPX500.main(
        fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W, fetch_SPX500_M
    )

    # 3.1 Combine latest cloud signals of all symbols into one spreadsheet
    _getIchimokuCloudDataSPX500Aggregator = (
        GetIchimokuCloudDataSPX500Aggregator
    )
    _getIchimokuCloudDataSPX500Aggregator.main(
        fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W, fetch_SPX500_M
    )

    # 3.2 Merge Multi Time Frame Cloud signals
    _getIchimokuCloudDataSPX500MultiTFMerger = (
        GetIchimokuCloudDataSPX500MultiTFMerger
    )
    _getIchimokuCloudDataSPX500MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_SPX500
    )

    # 3.3 Produce Ichimoku TK Cross data
    _getIchimokuTKxDataSPX500 = GetIchimokuTKxDataSPX500
    _getIchimokuTKxDataSPX500.main(
        fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W, fetch_SPX500_M
    )

    # 3.4 Combine latest TK Cross signals from all symbols into one spreadsheet
    _getIchimokuTKxDataSPX500Aggregator = GetIchimokuTKxDataSPX500Aggregator
    _getIchimokuTKxDataSPX500Aggregator.main(
        fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W, fetch_SPX500_M
    )

    # 3.5 Merge Multi Time Frame TKx signals
    _getIchimokuTKxDataSPX500MultiTFMerger = (
        GetIchimokuTKxDataSPX500MultiTFMerger
    )
    _getIchimokuTKxDataSPX500MultiTFMerger.main(
        run_Multi_TimeFrame_Merger_SPX500
    )

    # 4. Produce Kijun data
    _getIchimokuKijunDataSPX500 = GetIchimokuKijunDataSPX500
    _getIchimokuKijunDataSPX500.main(
        fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W, fetch_SPX500_M
    )

    # 4.1 Combine latest Kijun signals from all symbols into one spreadsheet
    _getIchimokuKijunDataSPX500Aggregator = (
        GetIchimokuKijunDataSPX500Aggregator
    )
    _getIchimokuKijunDataSPX500Aggregator.main(
        fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W, fetch_SPX500_M
    )

    # 5. Produce Kicker data
    _getKickerDataSPX500 = GetKickerDataSPX500
    _getKickerDataSPX500.main(
        fetch_Kicker_use_datetime_format,
        fetch_SPX500_D,
        fetch_SPX500_W,
        fetch_SPX500_M,
    )

    # 5.1 Combine latest Kicker signals from all symbols into one spreadsheet
    _getKickerDataSPX500Aggregator = GetKickerDataSPX500Aggregator
    _getKickerDataSPX500Aggregator.main(
        fetch_Kicker_use_datetime_format,
        fetch_SPX500_D,
        fetch_SPX500_W,
        fetch_SPX500_M,
    )

    print("\nTasks completed.")


if __name__ == "__main__":
    main()
