from src.mvc import (
    GetDataDJ30,
    GetIchimokuCloudDataDJ30Aggregator,
    GetIchimokuCloudDataFTSE100,
    GetIchimokuCloudDataFTSE250,
    GetIchimokuCloudDataFTSE250Aggregator,
    GetIchimokuCloudDataFuturesCurrency,
    GetIchimokuCloudDataFuturesCurrencyAggregator,
    GetIchimokuCloudDataNAS100,
    GetIchimokuCloudDataNAS100Aggregator,
    GetIchimokuCloudDataSPX500,
    GetIchimokuCloudDataSPX500Aggregator,
    GetIchimokuTKxDataDJ30,
    GetIchimokuTKxDataDJ30Aggregator,
    GetIchimokuTKxDataFTSE100,
    GetIchimokuTKxDataFTSE100Aggregator,
    GetIchimokuTKxDataNas100,
    GetIchimokuTKxDataNas100Aggregator,
    GetIchimokuTKxDataSPX500,
    GetIchimokuTKxDataSPX500Aggregator,
    GetSymbolDowJones30,
    GetSymbolFTSE100,
    GetSymbolFTSE250,
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
    GetIchimokuKijunDataFutures,
    GetIchimokuKijunDataFuturesAggregator,
    GetKickerDataFutures,
    GetKickerDataFuturesAggregator,
    GetDataFuturesCurrency,
    GetIchimokuKijunDataFuturesCurrency,
    GetIchimokuKijunDataFuturesCurrencyAggregator,
    GetKickerDataFuturesCurrency,
    GetKickerDataFuturesCurrencyAggregator,
)

fetch_symbols_latest = True

fetch_DJ30_1H = False
fetch_SPX500_1H = False
fetch_Nas100_1H = False
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

fetch_DJ30_W = False
fetch_SPX500_W = False
fetch_Nas100_W = False
fetch_FTSE100_W = False
fetch_FTSE250_W = False
fetch_Futures_W = False
fetch_CurrencyFutures_W = False

fetch_DJ30_M = False
fetch_SPX500_M = False
fetch_Nas100_M = False
fetch_FTSE100_M = False
fetch_FTSE250_M = False
fetch_Futures_M = False
fetch_CurrencyFutures_M = False

fetch_Kicker_intraday = False


def main():
    # Stop script being auto-run by Replit or Gitpod
    # return

    # ---------------- Dow Jones 30 ----------------

    # Grab latest symbols
    _getSymbolDowJones30 = GetSymbolDowJones30
    _getSymbolDowJones30.main(fetch_symbols_latest)

    # Download latest OHLC data
    _getDataDJ30 = GetDataDJ30
    _getDataDJ30.main(fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W, fetch_DJ30_M)

    # Produce Ichimoku Cloud data
    _getIchimokuCloudDataDJ30 = GetIchimokuCloudDataDJ30
    _getIchimokuCloudDataDJ30.main(
        fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W, fetch_DJ30_M
    )

    # Combine latest cloud signals from all symbols into one spreadsheet
    _getIchimokuCloudDataDJ30Aggregator = GetIchimokuCloudDataDJ30Aggregator
    _getIchimokuCloudDataDJ30Aggregator.main(
        fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W, fetch_DJ30_M
    )

    # Produce Ichimoku TK Cross data
    _getIchimokuTKxDataDJ30 = GetIchimokuTKxDataDJ30
    _getIchimokuTKxDataDJ30.main(
        fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W, fetch_DJ30_M
    )

    # Combine latest TK Cross signals from all symbols into one spreadsheet
    _getIchimokuTKxDataDJ30Aggregator = GetIchimokuTKxDataDJ30Aggregator
    _getIchimokuTKxDataDJ30Aggregator.main(
        fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W, fetch_DJ30_M
    )

    # Produce Kijun data
    _getIchimokuKijunDataDJ30 = GetIchimokuKijunDataDJ30
    _getIchimokuKijunDataDJ30.main(
        fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W, fetch_DJ30_M
    )

    # Combine latest Kijun signals from all symbols into one spreadsheet
    _getIchimokuKijunDataDJ30Aggregator = GetIchimokuKijunDataDJ30Aggregator
    _getIchimokuKijunDataDJ30Aggregator.main(
        fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W, fetch_DJ30_M
    )

    # Produce Kicker data
    _getKickerDataDJ30 = GetKickerDataDJ30
    _getKickerDataDJ30.main(
        fetch_Kicker_intraday, fetch_DJ30_D, fetch_DJ30_W, fetch_DJ30_M
    )

    # Combine latest Kicker signals from all symbols into one spreadsheet
    _getKickerDataDJ30Aggregator = GetKickerDataDJ30Aggregator
    _getKickerDataDJ30Aggregator.main(
        fetch_Kicker_intraday, fetch_DJ30_D, fetch_DJ30_W, fetch_DJ30_M
    )

    # ---------------- Nasdaq 100 ----------------
    _getSymbolNAS100 = GetSymbolNAS100
    _getSymbolNAS100.main(fetch_symbols_latest)

    _getDataNas100 = GetDataNas100
    _getDataNas100.main(
        fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W, fetch_Nas100_M
    )

    _getIchimokuCloudDataNas100 = GetIchimokuCloudDataNAS100
    _getIchimokuCloudDataNas100.main(
        fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W, fetch_Nas100_M
    )

    _getIchimokuCloudDataNas100Aggregator = (
        GetIchimokuCloudDataNAS100Aggregator
    )
    _getIchimokuCloudDataNas100Aggregator.main(
        fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W, fetch_Nas100_M
    )

    # Produce Ichimoku TK Cross data
    _getIchimokuTKxDataNas100 = GetIchimokuTKxDataNas100
    _getIchimokuTKxDataNas100.main(
        fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W, fetch_Nas100_M
    )

    # Combine latest TK Cross signals from all symbols into one spreadsheet
    _getIchimokuTKxDataNas100Aggregator = GetIchimokuTKxDataNas100Aggregator
    _getIchimokuTKxDataNas100Aggregator.main(
        fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W, fetch_Nas100_M
    )

    _getIchimokuKijunDataNas100 = GetIchimokuKijunDataNas100
    _getIchimokuKijunDataNas100.main(
        fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W, fetch_Nas100_M
    )

    _getIchimokuKijunDataNas100Aggregator = (
        GetIchimokuKijunDataNas100Aggregator
    )
    _getIchimokuKijunDataNas100Aggregator.main(
        fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W, fetch_Nas100_M
    )

    _getKickerDataNas100 = GetKickerDataNas100
    _getKickerDataNas100.main(
        fetch_Kicker_intraday, fetch_Nas100_D, fetch_Nas100_W, fetch_Nas100_M
    )

    _getKickerDataNas100Aggregator = GetKickerDataNas100Aggregator
    _getKickerDataNas100Aggregator.main(
        fetch_Kicker_intraday, fetch_Nas100_D, fetch_Nas100_W, fetch_Nas100_M
    )

    # ---------------- FTSE 100 ----------------

    _getSymbolFTSE100 = GetSymbolFTSE100
    _getSymbolFTSE100.main(fetch_symbols_latest)

    _getDataFTSE100 = GetDataFTSE100
    _getDataFTSE100.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W, fetch_FTSE100_M
    )

    _getIchimokuCloudDataFTSE100 = GetIchimokuCloudDataFTSE100
    _getIchimokuCloudDataFTSE100.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W, fetch_FTSE100_M
    )

    _getIchimokuCloudDataFTSE100Aggregator = (
        GetIchimokuCloudDataFTSE100Aggregator
    )
    _getIchimokuCloudDataFTSE100Aggregator.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W, fetch_FTSE100_M
    )

    # Produce Ichimoku TK Cross data
    _getIchimokuTKxDataFTSE100 = GetIchimokuTKxDataFTSE100
    _getIchimokuTKxDataFTSE100.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W, fetch_FTSE100_M
    )

    # Combine latest TK Cross signals from all symbols into one spreadsheet
    _getIchimokuTKxDataFTSE100Aggregator = GetIchimokuTKxDataFTSE100Aggregator
    _getIchimokuTKxDataFTSE100Aggregator.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W, fetch_FTSE100_M
    )

    _getIchimokuKijunDataFTSE100 = GetIchimokuKijunDataFTSE100
    _getIchimokuKijunDataFTSE100.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W, fetch_FTSE100_M
    )

    _getIchimokuKijunDataFTSE100Aggregator = (
        GetIchimokuKijunDataFTSE100Aggregator
    )
    _getIchimokuKijunDataFTSE100Aggregator.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W, fetch_FTSE100_M
    )

    _getKickerDataFTSE100 = GetKickerDataFTSE100
    _getKickerDataFTSE100.main(
        fetch_Kicker_intraday,
        fetch_FTSE100_D,
        fetch_FTSE100_W,
        fetch_FTSE100_M,
    )

    _getKickerDataFTSE100Aggregator = GetKickerDataFTSE100Aggregator
    _getKickerDataFTSE100Aggregator.main(
        fetch_Kicker_intraday,
        fetch_FTSE100_D,
        fetch_FTSE100_W,
        fetch_FTSE100_M,
    )

    # ---------------- FTSE 250 ----------------

    _getSymbolFTSE250 = GetSymbolFTSE250
    _getSymbolFTSE250.main(fetch_symbols_latest)

    _getDataFTSE250 = GetDataFTSE250
    _getDataFTSE250.main(
        fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W, fetch_FTSE250_M
    )

    _getIchimokuCloudDataFTSE250 = GetIchimokuCloudDataFTSE250
    _getIchimokuCloudDataFTSE250.main(
        fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W, fetch_FTSE250_M
    )

    _getIchimokuCloudDataFTSE250Aggregator = (
        GetIchimokuCloudDataFTSE250Aggregator
    )
    _getIchimokuCloudDataFTSE250Aggregator.main(
        fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W, fetch_FTSE250_M
    )

    _gtIchimokuKijunDataFTSE250 = GetIchimokuKijunDataFTSE250
    _gtIchimokuKijunDataFTSE250.main(
        fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W, fetch_FTSE250_M
    )

    _getIchimokuKijunDataFTSE250Aggregator = (
        GetIchimokuKijunDataFTSE250Aggregator
    )
    _getIchimokuKijunDataFTSE250Aggregator.main(
        fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W, fetch_FTSE250_M
    )

    _getKickerDataFTSE250 = GetKickerDataFTSE250
    _getKickerDataFTSE250.main(
        fetch_Kicker_intraday,
        fetch_FTSE250_D,
        fetch_FTSE250_W,
        fetch_FTSE250_M,
    )

    _getKickerDataFTSE250Aggregator = GetKickerDataFTSE250Aggregator
    _getKickerDataFTSE250Aggregator.main(
        fetch_Kicker_intraday,
        fetch_FTSE250_D,
        fetch_FTSE250_W,
        fetch_FTSE250_M,
    )

    # ---------------- Futures ----------------

    _getDataFutures = GetDataFutures
    _getDataFutures.main(
        fetch_Futures_1H, fetch_Futures_D, fetch_Futures_W, fetch_Futures_M
    )

    _getIchimokuDataFutures = GetIchimokuKijunDataFutures
    _getIchimokuDataFutures.main(
        fetch_Futures_1H, fetch_Futures_D, fetch_Futures_W, fetch_Futures_M
    )

    _getIchimokuDataFuturesAggregator = GetIchimokuKijunDataFuturesAggregator
    _getIchimokuDataFuturesAggregator.main(
        fetch_Futures_1H, fetch_Futures_D, fetch_Futures_W, fetch_Futures_M
    )

    _getKickerDataFutures = GetKickerDataFutures
    _getKickerDataFutures.main(
        fetch_Kicker_intraday,
        fetch_Futures_D,
        fetch_Futures_W,
        fetch_Futures_M,
    )

    _getKickerDataFuturesAggregator = GetKickerDataFuturesAggregator
    _getKickerDataFuturesAggregator.main(
        fetch_Kicker_intraday,
        fetch_Futures_D,
        fetch_Futures_W,
        fetch_Futures_M,
    )

    # ---------------- Futures Currency ----------------

    _getDataFuturesCurrency = GetDataFuturesCurrency
    _getDataFuturesCurrency.main(
        fetch_CurrencyFutures_1H,
        fetch_CurrencyFutures_D,
        fetch_CurrencyFutures_W,
        fetch_CurrencyFutures_M,
    )

    _getIchimokuCloudDataFuturesCurrency = GetIchimokuCloudDataFuturesCurrency
    _getIchimokuCloudDataFuturesCurrency.main(
        fetch_CurrencyFutures_1H,
        fetch_CurrencyFutures_D,
        fetch_CurrencyFutures_W,
        fetch_CurrencyFutures_M,
    )

    _getIchimokuCloudDataFuturesCurrencyAggregator = (
        GetIchimokuCloudDataFuturesCurrencyAggregator
    )
    _getIchimokuCloudDataFuturesCurrencyAggregator.main(
        fetch_CurrencyFutures_1H,
        fetch_CurrencyFutures_D,
        fetch_CurrencyFutures_W,
        fetch_CurrencyFutures_M,
    )

    _getIchimokuKijunDataFuturesCurrency = GetIchimokuKijunDataFuturesCurrency
    _getIchimokuKijunDataFuturesCurrency.main(
        fetch_CurrencyFutures_1H,
        fetch_CurrencyFutures_D,
        fetch_CurrencyFutures_W,
        fetch_CurrencyFutures_M,
    )

    _getIchimokuKijunDataFuturesCurrencyAggregator = (
        GetIchimokuKijunDataFuturesCurrencyAggregator
    )
    _getIchimokuKijunDataFuturesCurrencyAggregator.main(
        fetch_CurrencyFutures_1H,
        fetch_CurrencyFutures_D,
        fetch_CurrencyFutures_W,
        fetch_CurrencyFutures_M,
    )

    _getKickerDataFuturesCurrency = GetKickerDataFuturesCurrency
    _getKickerDataFuturesCurrency.main(
        fetch_CurrencyFutures_1H,
        fetch_CurrencyFutures_D,
        fetch_CurrencyFutures_W,
        fetch_CurrencyFutures_M,
    )

    _getKickerDataFuturesCurrencyAggregator = (
        GetKickerDataFuturesCurrencyAggregator
    )
    _getKickerDataFuturesCurrencyAggregator.main(
        fetch_CurrencyFutures_1H,
        fetch_CurrencyFutures_D,
        fetch_CurrencyFutures_W,
        fetch_CurrencyFutures_M,
    )

    # ---------------- S&P 500 ----------------

    _getSymbolSPX500 = GetSymbolSPX500
    _getSymbolSPX500.main(fetch_symbols_latest)

    _getDataSPX500 = GetDataSPX500
    _getDataSPX500.main(
        fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W, fetch_SPX500_M
    )

    _getIchimokuCloudDataSPX500 = GetIchimokuCloudDataSPX500
    _getIchimokuCloudDataSPX500.main(
        fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W, fetch_SPX500_M
    )

    _getIchimokuCloudDataSPX500Aggregator = (
        GetIchimokuCloudDataSPX500Aggregator
    )
    _getIchimokuCloudDataSPX500Aggregator.main(
        fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W, fetch_SPX500_M
    )

    # Produce Ichimoku TK Cross data
    _getIchimokuTKxDataSPX500 = GetIchimokuTKxDataSPX500
    _getIchimokuTKxDataSPX500.main(
        fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W, fetch_SPX500_M
    )

    # Combine latest TK Cross signals from all symbols into one spreadsheet
    _getIchimokuTKxDataSPX500Aggregator = GetIchimokuTKxDataSPX500Aggregator
    _getIchimokuTKxDataSPX500Aggregator.main(
        fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W, fetch_SPX500_M
    )

    _getIchimokuKijunDataSPX500 = GetIchimokuKijunDataSPX500
    _getIchimokuKijunDataSPX500.main(
        fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W, fetch_SPX500_M
    )

    _getIchimokuKijunDataSPX500Aggregator = (
        GetIchimokuKijunDataSPX500Aggregator
    )
    _getIchimokuKijunDataSPX500Aggregator.main(
        fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W, fetch_SPX500_M
    )

    _getKickerDataSPX500 = GetKickerDataSPX500
    _getKickerDataSPX500.main(
        fetch_Kicker_intraday, fetch_SPX500_D, fetch_SPX500_W, fetch_SPX500_M
    )

    _getKickerDataSPX500Aggregator = GetKickerDataSPX500Aggregator
    _getKickerDataSPX500Aggregator.main(
        fetch_Kicker_intraday, fetch_SPX500_D, fetch_SPX500_W, fetch_SPX500_M
    )

    print(f"Tasks completed.")


if __name__ == "__main__":
    main()
