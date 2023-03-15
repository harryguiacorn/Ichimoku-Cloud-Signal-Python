from src.mvc import (
    GetDataDJ30,
    GetIchimokuCloudDataDJ30Aggregator,
    GetIchimokuCloudDataNAS100,
    GetIchimokuCloudDataNAS100Aggregator,
    GetSymbolDowJones30,
    GetSymbolNAS100,
)
from src.mvc import GetIchimokuKijunDataDJ30
from src.mvc import GetIchimokuCloudDataDJ30
from src.mvc import GetIchimokuKijunDataDJ30Aggregator
from src.mvc import GetKickerDataDJ30
from src.mvc import GetKickerDataDJ30Aggregator

from src.mvc import GetDataNas100
from src.mvc import GetIchimokuKijunDataNas100
from src.mvc import GetIchimokuKijunDataNas100Aggregator
from src.mvc import GetKickerDataNas100
from src.mvc import GetKickerDataNas100Aggregator

from src.mvc import GetDataFTSE100
from src.mvc import GetIchimokuKijunDataFTSE100
from src.mvc import GetIchimokuKijunDataFTSE100Aggregator
from src.mvc import GetKickerDataFTSE100
from src.mvc import GetKickerDataFTSE100Aggregator

from src.mvc import GetDataFTSE250
from src.mvc import GetIchimokuKijunDataFTSE250
from src.mvc import GetIchimokuKijunDataFTSE250Aggregator
from src.mvc import GetKickerDataFTSE250
from src.mvc import GetKickerDataFTSE250Aggregator

from src.mvc import GetDataSPX500
from src.mvc import GetIchimokuKijunDataSPX500
from src.mvc import GetIchimokuKijunDataSPX500Aggregator
from src.mvc import GetKickerDataSPX500
from src.mvc import GetKickerDataSPX500Aggregator

from src.mvc import GetDataFutures
from src.mvc import GetIchimokuKijunDataFutures
from src.mvc import GetIchimokuKijunDataFuturesAggregator
from src.mvc import GetKickerDataFutures
from src.mvc import GetKickerDataFuturesAggregator

from src.mvc import GetDataFuturesCurrency
from src.mvc import GetIchimokuKijunDataFuturesCurrency
from src.mvc import GetIchimokuKijunDataFuturesCurrencyAggregator
from src.mvc import GetKickerDataFuturesCurrency
from src.mvc import GetKickerDataFuturesCurrencyAggregator

fetch_DJ30_1H = True
fetch_SPX500_1H = False
fetch_Nas100_1H = True
fetch_FTSE100_1H = False
fetch_FTSE250_1H = False
fetch_Futures_1H = False
fetch_CurrencyFutures_1H = False

fetch_DJ30_D = True
fetch_SPX500_D = False
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
    # _getSymbolDowJones30 = GetSymbolDowJones30
    # _getSymbolDowJones30.main()

    # _getDataDJ30 = GetDataDJ30
    # _getDataDJ30.main(fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W)

    # _getIchimokuCloudDataDJ30 = GetIchimokuCloudDataDJ30
    # _getIchimokuCloudDataDJ30.main(fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W)

    # _getIchimokuCloudDataDJ30Aggregator = GetIchimokuCloudDataDJ30Aggregator
    # _getIchimokuCloudDataDJ30Aggregator.main(fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W)

    # _getIchimokuKijunDataDJ30 = GetIchimokuKijunDataDJ30
    # _getIchimokuKijunDataDJ30.main(fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W)

    # _getIchimokuKijunDataDJ30Aggregator = GetIchimokuKijunDataDJ30Aggregator
    # _getIchimokuKijunDataDJ30Aggregator.main(fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W)

    # _getKickerDataDJ30 = GetKickerDataDJ30
    # _getKickerDataDJ30.main(fetch_Kicker_intraday, fetch_DJ30_D, fetch_DJ30_W)

    # _getKickerDataDJ30Aggregator = GetKickerDataDJ30Aggregator
    # _getKickerDataDJ30Aggregator.main(fetch_Kicker_intraday, fetch_DJ30_D, fetch_DJ30_W)

    # ---------------- Nasdaq 100 ----------------
    _getSymbolNAS100 = GetSymbolNAS100
    _getSymbolNAS100.main()

    _getDataNas100 = GetDataNas100
    _getDataNas100.main(fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W)

    # _getIchimokuCloudDataNas100 = GetIchimokuCloudDataNAS100
    # _getIchimokuCloudDataNas100.main(fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W)

    # _getIchimokuCloudDataDJ30Aggregator = GetIchimokuCloudDataNAS100Aggregator
    # _getIchimokuCloudDataDJ30Aggregator.main(fetch_DJ30_1H, fetch_DJ30_D, fetch_DJ30_W)

    # _getIchimokuKijunDataNas100 = GetIchimokuKijunDataNas100
    # _getIchimokuKijunDataNas100.main(fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W)

    # _getIchimokuKijunDataNas100Aggregator = GetIchimokuKijunDataNas100Aggregator
    # _getIchimokuKijunDataNas100Aggregator.main(
    #     fetch_Nas100_1H, fetch_Nas100_D, fetch_Nas100_W
    # )

    # _getKickerDataNas100 = GetKickerDataNas100
    # _getKickerDataNas100.main(fetch_Kicker_intraday, fetch_Nas100_D, fetch_Nas100_W)

    # _getKickerDataNas100Aggregator = GetKickerDataNas100Aggregator
    # _getKickerDataNas100Aggregator.main(
    #     fetch_Kicker_intraday, fetch_Nas100_D, fetch_Nas100_W
    # )

    # ---------------- FTSE 100 ----------------

    # _getDataFTSE100 = GetDataFTSE100
    # _getDataFTSE100.main(fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W)

    # _getIchimokuDataFTSE100 = GetIchimokuKijunDataFTSE100
    # _getIchimokuDataFTSE100.main(fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W)

    # _getIchimokuDataFTSE100Aggregator = GetIchimokuKijunDataFTSE100Aggregator
    # _getIchimokuDataFTSE100Aggregator.main(
    #     fetch_FTSE100_1H, fetch_FTSE100_D, fetch_FTSE100_W
    # )

    # _getKickerDataFTSE100 = GetKickerDataFTSE100
    # _getKickerDataFTSE100.main(fetch_Kicker_intraday, fetch_FTSE100_D, fetch_FTSE100_W)

    # _getKickerDataFTSE100Aggregator = GetKickerDataFTSE100Aggregator
    # _getKickerDataFTSE100Aggregator.main(
    #     fetch_Kicker_intraday, fetch_FTSE100_D, fetch_FTSE100_W
    # )

    # ---------------- FTSE 250 ----------------

    # _getDataFTSE250 = GetDataFTSE250
    # _getDataFTSE250.main(fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W)

    # _getIchimokuDataFTSE250 = GetIchimokuKijunDataFTSE250
    # _getIchimokuDataFTSE250.main(fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W)

    # _getIchimokuDataFTSE250Aggregator = GetIchimokuKijunDataFTSE250Aggregator
    # _getIchimokuDataFTSE250Aggregator.main(
    #     fetch_FTSE250_1H, fetch_FTSE250_D, fetch_FTSE250_W
    # )

    # _getKickerDataFTSE250 = GetKickerDataFTSE250
    # _getKickerDataFTSE250.main(fetch_Kicker_intraday, fetch_FTSE250_D, fetch_FTSE250_W)

    # _getKickerDataFTSE250Aggregator = GetKickerDataFTSE250Aggregator
    # _getKickerDataFTSE250Aggregator.main(
    #     fetch_Kicker_intraday, fetch_FTSE250_D, fetch_FTSE250_W
    # )

    # ---------------- Futures ----------------

    # _getDataFutures = GetDataFutures
    # _getDataFutures.main(fetch_Futures_1H, fetch_Futures_D, fetch_Futures_W)

    # _getIchimokuDataFutures = GetIchimokuKijunDataFutures
    # _getIchimokuDataFutures.main(fetch_Futures_1H, fetch_Futures_D, fetch_Futures_W)

    # _getIchimokuDataFuturesAggregator = GetIchimokuKijunDataFuturesAggregator
    # _getIchimokuDataFuturesAggregator.main(
    #     fetch_Futures_1H, fetch_Futures_D, fetch_Futures_W
    # )

    # _getKickerDataFutures = GetKickerDataFutures
    # _getKickerDataFutures.main(fetch_Kicker_intraday, fetch_Futures_D, fetch_Futures_W)

    # _getKickerDataFuturesAggregator = GetKickerDataFuturesAggregator
    # _getKickerDataFuturesAggregator.main(
    #     fetch_Kicker_intraday, fetch_Futures_D, fetch_Futures_W
    # )

    # ---------------- Futures Currency ----------------

    # _getDataFuturesCurrency = GetDataFuturesCurrency
    # _getDataFuturesCurrency.main(
    #     fetch_CurrencyFutures_1H, fetch_CurrencyFutures_D, fetch_CurrencyFutures_W
    # )

    # _getIchimokuDataFuturesCurrency = GetIchimokuKijunDataFuturesCurrency
    # _getIchimokuDataFuturesCurrency.main(
    #     fetch_CurrencyFutures_1H, fetch_CurrencyFutures_D, fetch_CurrencyFutures_W
    # )

    # _getIchimokuDataFuturesCurrencyAggregator = (
    #     GetIchimokuKijunDataFuturesCurrencyAggregator
    # )
    # _getIchimokuDataFuturesCurrencyAggregator.main(
    #     fetch_CurrencyFutures_1H, fetch_CurrencyFutures_D, fetch_CurrencyFutures_W
    # )

    # _getKickerDataFuturesCurrency = GetKickerDataFuturesCurrency
    # _getKickerDataFuturesCurrency.main(
    #     fetch_CurrencyFutures_1H, fetch_CurrencyFutures_D, fetch_CurrencyFutures_W
    # )

    # _getKickerDataFuturesCurrencyAggregator = GetKickerDataFuturesCurrencyAggregator
    # _getKickerDataFuturesCurrencyAggregator.main(
    #     fetch_CurrencyFutures_1H, fetch_CurrencyFutures_D, fetch_CurrencyFutures_W
    # )

    # ---------------- S&P 500 ----------------

    # _getDataSPX500 = GetDataSPX500
    # _getDataSPX500.main(fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W)

    # _getIchimokuDataSPX500 = GetIchimokuKijunDataSPX500
    # _getIchimokuDataSPX500.main(fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W)

    # _getIchimokuDataSPX500Aggregator = GetIchimokuKijunDataSPX500Aggregator
    # _getIchimokuDataSPX500Aggregator.main(
    #     fetch_SPX500_1H, fetch_SPX500_D, fetch_SPX500_W
    # )

    # _getKickerDataSPX500 = GetKickerDataSPX500
    # _getKickerDataSPX500.main(fetch_Kicker_intraday, fetch_SPX500_D, fetch_SPX500_W)

    # _getKickerDataSPX500Aggregator = GetKickerDataSPX500Aggregator
    # _getKickerDataSPX500Aggregator.main(
    #     fetch_Kicker_intraday, fetch_SPX500_D, fetch_SPX500_W
    # )


if __name__ == "__main__":
    main()
