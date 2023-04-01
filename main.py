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

fetch_DJ30_W = False
fetch_SPX500_W = False
fetch_Nas100_W = False
fetch_FTSE100_W = False
fetch_FTSE250_W = False
fetch_Futures_W = False
fetch_CurrencyFutures_W = False

fetch_Kicker_intraday = False


def main():
    # Stop script being auto-run by Replit or Gitpod
    # return

    # ---------------- Dow Jones 30 ----------------

    # Grab latest symbols
    _getSymbolDowJones30 = GetSymbolDowJones30
    _getSymbolDowJones30.main()

    # Download latest OHLC data
    _getDataDJ30 = GetDataDJ30
    _getDataDJ30.main(fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W)

    # Produce Ichimoku Cloud data
    _getIchimokuCloudDataDJ30 = GetIchimokuCloudDataDJ30
    _getIchimokuCloudDataDJ30.main(fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W)

    # Combine latest cloud signals from all symbols into one spreadsheet
    _getIchimokuCloudDataDJ30Aggregator = GetIchimokuCloudDataDJ30Aggregator
    _getIchimokuCloudDataDJ30Aggregator.main(fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W)

    # Produce Kijun data
    _getIchimokuKijunDataDJ30 = GetIchimokuKijunDataDJ30
    _getIchimokuKijunDataDJ30.main(fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W)

    # Combine latest Kijun signals from all symbols into one spreadsheet
    _getIchimokuKijunDataDJ30Aggregator = GetIchimokuKijunDataDJ30Aggregator
    _getIchimokuKijunDataDJ30Aggregator.main(fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W)

    # Produce Kicker data
    _getKickerDataDJ30 = GetKickerDataDJ30
    _getKickerDataDJ30.main(fetch_Kicker_intraday, fetch_DJ30_D, fetch_DJ30_W)

    # Combine latest Kicker signals from all symbols into one spreadsheet
    _getKickerDataDJ30Aggregator = GetKickerDataDJ30Aggregator
    _getKickerDataDJ30Aggregator.main(fetch_Kicker_intraday, fetch_DJ30_D, fetch_DJ30_W)

    # ---------------- Nasdaq 100 ----------------
    _getSymbolNAS100 = GetSymbolNAS100
    _getSymbolNAS100.main()

    _getDataNas100 = GetDataNas100
    _getDataNas100.main(fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W)

    _getIchimokuCloudDataNas100 = GetIchimokuCloudDataNAS100
    _getIchimokuCloudDataNas100.main(fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W)

    _getIchimokuCloudDataNas100Aggregator = GetIchimokuCloudDataNAS100Aggregator
    _getIchimokuCloudDataNas100Aggregator.main(
        fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W
    )

    _getIchimokuKijunDataNas100 = GetIchimokuKijunDataNas100
    _getIchimokuKijunDataNas100.main(fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W)

    _getIchimokuKijunDataNas100Aggregator = GetIchimokuKijunDataNas100Aggregator
    _getIchimokuKijunDataNas100Aggregator.main(
        fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W
    )

    _getKickerDataNas100 = GetKickerDataNas100
    _getKickerDataNas100.main(fetch_Kicker_intraday, fetch_Nas100_D, fetch_Nas100_W)

    _getKickerDataNas100Aggregator = GetKickerDataNas100Aggregator
    _getKickerDataNas100Aggregator.main(
        fetch_Kicker_intraday, fetch_Nas100_D, fetch_Nas100_W
    )

    # ---------------- FTSE 100 ----------------

    _getSymbolFTSE100 = GetSymbolFTSE100
    _getSymbolFTSE100.main()

    _getDataFTSE100 = GetDataFTSE100
    _getDataFTSE100.main(fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W)

    _getIchimokuCloudDataFTSE100 = GetIchimokuCloudDataFTSE100
    _getIchimokuCloudDataFTSE100.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W
    )

    _getIchimokuCloudDataFTSE100Aggregator = GetIchimokuCloudDataFTSE100Aggregator
    _getIchimokuCloudDataFTSE100Aggregator.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W
    )

    _getIchimokuKijunDataFTSE100 = GetIchimokuKijunDataFTSE100
    _getIchimokuKijunDataFTSE100.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W
    )

    _getIchimokuKijunDataFTSE100Aggregator = GetIchimokuKijunDataFTSE100Aggregator
    _getIchimokuKijunDataFTSE100Aggregator.main(
        fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W
    )

    _getKickerDataFTSE100 = GetKickerDataFTSE100
    _getKickerDataFTSE100.main(fetch_Kicker_intraday, fetch_FTSE100_D, fetch_FTSE100_W)

    _getKickerDataFTSE100Aggregator = GetKickerDataFTSE100Aggregator
    _getKickerDataFTSE100Aggregator.main(
        fetch_Kicker_intraday, fetch_FTSE100_D, fetch_FTSE100_W
    )

    # ---------------- FTSE 250 ----------------

    _getSymbolFTSE250 = GetSymbolFTSE250
    _getSymbolFTSE250.main()

    _getDataFTSE250 = GetDataFTSE250
    _getDataFTSE250.main(fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W)

    _getIchimokuCloudDataFTSE250 = GetIchimokuCloudDataFTSE250
    _getIchimokuCloudDataFTSE250.main(
        fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W
    )

    _getIchimokuCloudDataFTSE250Aggregator = GetIchimokuCloudDataFTSE250Aggregator
    _getIchimokuCloudDataFTSE250Aggregator.main(
        fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W
    )

    _gtIchimokuKijunDataFTSE250 = GetIchimokuKijunDataFTSE250
    _gtIchimokuKijunDataFTSE250.main(fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W)

    _getIchimokuKijunDataFTSE250Aggregator = GetIchimokuKijunDataFTSE250Aggregator
    _getIchimokuKijunDataFTSE250Aggregator.main(
        fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W
    )

    _getKickerDataFTSE250 = GetKickerDataFTSE250
    _getKickerDataFTSE250.main(fetch_Kicker_intraday, fetch_FTSE250_D, fetch_FTSE250_W)

    _getKickerDataFTSE250Aggregator = GetKickerDataFTSE250Aggregator
    _getKickerDataFTSE250Aggregator.main(
        fetch_Kicker_intraday, fetch_FTSE250_D, fetch_FTSE250_W
    )

    # ---------------- Futures ----------------

    _getDataFutures = GetDataFutures
    _getDataFutures.main(fetch_Futures_1H, fetch_Futures_D, fetch_Futures_W)

    _getIchimokuDataFutures = GetIchimokuKijunDataFutures
    _getIchimokuDataFutures.main(fetch_Futures_1H, fetch_Futures_D, fetch_Futures_W)

    _getIchimokuDataFuturesAggregator = GetIchimokuKijunDataFuturesAggregator
    _getIchimokuDataFuturesAggregator.main(
        fetch_Futures_1H, fetch_Futures_D, fetch_Futures_W
    )

    _getKickerDataFutures = GetKickerDataFutures
    _getKickerDataFutures.main(fetch_Kicker_intraday, fetch_Futures_D, fetch_Futures_W)

    _getKickerDataFuturesAggregator = GetKickerDataFuturesAggregator
    _getKickerDataFuturesAggregator.main(
        fetch_Kicker_intraday, fetch_Futures_D, fetch_Futures_W
    )

    # ---------------- Futures Currency ----------------

    _getDataFuturesCurrency = GetDataFuturesCurrency
    _getDataFuturesCurrency.main(
        fetch_CurrencyFutures_1H, fetch_CurrencyFutures_D, fetch_CurrencyFutures_W
    )

    _getIchimokuCloudDataFuturesCurrency = GetIchimokuCloudDataFuturesCurrency
    _getIchimokuCloudDataFuturesCurrency.main(
        fetch_CurrencyFutures_1H, fetch_CurrencyFutures_D, fetch_CurrencyFutures_W
    )

    _getIchimokuCloudDataFuturesCurrencyAggregator = (
        GetIchimokuCloudDataFuturesCurrencyAggregator
    )
    _getIchimokuCloudDataFuturesCurrencyAggregator.main(
        fetch_CurrencyFutures_1H, fetch_CurrencyFutures_D, fetch_CurrencyFutures_W
    )

    _getIchimokuKijunDataFuturesCurrency = GetIchimokuKijunDataFuturesCurrency
    _getIchimokuKijunDataFuturesCurrency.main(
        fetch_CurrencyFutures_1H, fetch_CurrencyFutures_D, fetch_CurrencyFutures_W
    )

    _getIchimokuKijunDataFuturesCurrencyAggregator = (
        GetIchimokuKijunDataFuturesCurrencyAggregator
    )
    _getIchimokuKijunDataFuturesCurrencyAggregator.main(
        fetch_CurrencyFutures_1H, fetch_CurrencyFutures_D, fetch_CurrencyFutures_W
    )

    _getKickerDataFuturesCurrency = GetKickerDataFuturesCurrency
    _getKickerDataFuturesCurrency.main(
        fetch_CurrencyFutures_1H, fetch_CurrencyFutures_D, fetch_CurrencyFutures_W
    )

    _getKickerDataFuturesCurrencyAggregator = GetKickerDataFuturesCurrencyAggregator
    _getKickerDataFuturesCurrencyAggregator.main(
        fetch_CurrencyFutures_1H, fetch_CurrencyFutures_D, fetch_CurrencyFutures_W
    )

    # ---------------- S&P 500 ----------------

    _getSymbolSPX500 = GetSymbolSPX500
    _getSymbolSPX500.main()

    _getDataSPX500 = GetDataSPX500
    _getDataSPX500.main(fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W)

    _getIchimokuCloudDataSPX500 = GetIchimokuCloudDataSPX500
    _getIchimokuCloudDataSPX500.main(fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W)

    _getIchimokuCloudDataSPX500Aggregator = GetIchimokuCloudDataSPX500Aggregator
    _getIchimokuCloudDataSPX500Aggregator.main(
        fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W
    )

    _getIchimokuKijunDataSPX500 = GetIchimokuKijunDataSPX500
    _getIchimokuKijunDataSPX500.main(fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W)

    _getIchimokuKijunDataSPX500Aggregator = GetIchimokuKijunDataSPX500Aggregator
    _getIchimokuKijunDataSPX500Aggregator.main(
        fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W
    )

    _getKickerDataSPX500 = GetKickerDataSPX500
    _getKickerDataSPX500.main(fetch_Kicker_intraday, fetch_SPX500_D, fetch_SPX500_W)

    _getKickerDataSPX500Aggregator = GetKickerDataSPX500Aggregator
    _getKickerDataSPX500Aggregator.main(
        fetch_Kicker_intraday, fetch_SPX500_D, fetch_SPX500_W
    )
    pass


if __name__ == "__main__":
    main()
