from src.mvc import GetDataDJ30
from src.mvc import GetIchimokuDataDJ30
from src.mvc import GetIchimokuCloudDataDJ30
from src.mvc import GetIchimokuDataDJ30Aggregator
from src.mvc import GetKickerDataDJ30
from src.mvc import GetKickerDataDJ30Aggregator

from src.mvc import GetDataNas100
from src.mvc import GetIchimokuDataNas100
from src.mvc import GetIchimokuDataNas100Aggregator
from src.mvc import GetKickerDataNas100
from src.mvc import GetKickerDataNas100Aggregator

from src.mvc import GetDataFTSE100
from src.mvc import GetIchimokuDataFTSE100
from src.mvc import GetIchimokuDataFTSE100Aggregator
from src.mvc import GetKickerDataFTSE100
from src.mvc import GetKickerDataFTSE100Aggregator

from src.mvc import GetDataFTSE250
from src.mvc import GetIchimokuDataFTSE250
from src.mvc import GetIchimokuDataFTSE250Aggregator
from src.mvc import GetKickerDataFTSE250
from src.mvc import GetKickerDataFTSE250Aggregator

from src.mvc import GetDataSPX500
from src.mvc import GetIchimokuDataSPX500
from src.mvc import GetIchimokuDataSPX500Aggregator
from src.mvc import GetKickerDataSPX500
from src.mvc import GetKickerDataSPX500Aggregator

from src.mvc import GetDataFutures
from src.mvc import GetIchimokuDataFutures
from src.mvc import GetIchimokuDataFuturesAggregator
from src.mvc import GetKickerDataFutures
from src.mvc import GetKickerDataFuturesAggregator

from src.mvc import GetDataFuturesCurrency
from src.mvc import GetIchimokuDataFuturesCurrency
from src.mvc import GetIchimokuDataFuturesCurrencyAggregator
from src.mvc import GetKickerDataFuturesCurrency
from src.mvc import GetKickerDataFuturesCurrencyAggregator

fetchDJ30_1H = False
fetchSPX500_1H = False
fetchNas100_1H = False
fetchFTSE100_1H = False
fetchFTSE250_1H = False
fetchFutures_1H = False
fetchCurrencyFutures_1H = False

fetchDJ30_D = True
fetchSPX500_D = False
fetchNas100_D = False
fetchFTSE100_D = False
fetchFTSE250_D = False
fetchFutures_D = False
fetchCurrencyFutures_D = False

fetchDJ30_W = False
fetchSPX500_W = False
fetchNas100_W = False
fetchFTSE100_W = False
fetchFTSE250_W = False
fetchFutures_W = False
fetchCurrencyFutures_W = False

fetchKicker_intraday = False


def main():

    # Stop script being auto-run by Replit or Gitpod
    # return

    # ---------------- Dow Jones 30 ----------------

    # _getDataDJ30 = GetDataDJ30
    # _getDataDJ30.main(fetchDJ30_1H, fetchDJ30_D, fetchDJ30_W)

    _getIchimokuCloudDataDJ30 = GetIchimokuCloudDataDJ30
    _getIchimokuCloudDataDJ30.main(fetchDJ30_1H, fetchDJ30_D, fetchDJ30_W)

    # _getIchimokuDataDJ30 = GetIchimokuDataDJ30
    # _getIchimokuDataDJ30.main(fetchDJ30_1H, fetchDJ30_D, fetchDJ30_W)

    # _getIchimokuDataDJ30Aggregator = GetIchimokuDataDJ30Aggregator
    # _getIchimokuDataDJ30Aggregator.main(fetchDJ30_1H, fetchDJ30_D, fetchDJ30_W)

    # _getKickerDataDJ30 = GetKickerDataDJ30
    # _getKickerDataDJ30.main(fetchKicker_intraday, fetchDJ30_D, fetchDJ30_W)

    # _getKickerDataDJ30Aggregator = GetKickerDataDJ30Aggregator
    # _getKickerDataDJ30Aggregator.main(fetchKicker_intraday, fetchDJ30_D, fetchDJ30_W)

    # ---------------- Nasdaq 100 ----------------

    # _getDataNas100 = GetDataNas100
    # _getDataNas100.main(fetchNas100_1H, fetchNas100_D, fetchNas100_W)

    # _getIchimokuDataNas100 = GetIchimokuDataNas100
    # _getIchimokuDataNas100.main(fetchNas100_1H, fetchNas100_D, fetchNas100_W)

    # _getIchimokuDataNas100Aggregator = GetIchimokuDataNas100Aggregator
    # _getIchimokuDataNas100Aggregator.main(fetchNas100_1H, fetchNas100_D, fetchNas100_W)

    # _getKickerDataNas100 = GetKickerDataNas100
    # _getKickerDataNas100.main(fetchKicker_intraday, fetchNas100_D, fetchNas100_W)

    # _getKickerDataNas100Aggregator = GetKickerDataNas100Aggregator
    # _getKickerDataNas100Aggregator.main(fetchKicker_intraday, fetchNas100_D, fetchNas100_W)

    # ---------------- FTSE 100 ----------------

    # _getDataFTSE100 = GetDataFTSE100
    # _getDataFTSE100.main(fetchFTSE100_1H, fetchFTSE100_D, fetchFTSE100_W)

    # _getIchimokuDataFTSE100 = GetIchimokuDataFTSE100
    # _getIchimokuDataFTSE100.main(fetchFTSE100_1H, fetchFTSE100_D, fetchFTSE100_W)

    # _getIchimokuDataFTSE100Aggregator = GetIchimokuDataFTSE100Aggregator
    # _getIchimokuDataFTSE100Aggregator.main(
    #     fetchFTSE100_1H, fetchFTSE100_D, fetchFTSE100_W
    # )

    # _getKickerDataFTSE100 = GetKickerDataFTSE100
    # _getKickerDataFTSE100.main(fetchKicker_intraday, fetchFTSE100_D, fetchFTSE100_W)

    # _getKickerDataFTSE100Aggregator = GetKickerDataFTSE100Aggregator
    # _getKickerDataFTSE100Aggregator.main(
    #     fetchKicker_intraday, fetchFTSE100_D, fetchFTSE100_W
    # )

    # ---------------- FTSE 250 ----------------

    # _getDataFTSE250 = GetDataFTSE250
    # _getDataFTSE250.main(fetchFTSE250_1H, fetchFTSE250_D, fetchFTSE250_W)

    # _getIchimokuDataFTSE250 = GetIchimokuDataFTSE250
    # _getIchimokuDataFTSE250.main(fetchFTSE250_1H, fetchFTSE250_D, fetchFTSE250_W)

    # _getIchimokuDataFTSE250Aggregator = GetIchimokuDataFTSE250Aggregator
    # _getIchimokuDataFTSE250Aggregator.main(
    #     fetchFTSE250_1H, fetchFTSE250_D, fetchFTSE250_W
    # )

    # _getKickerDataFTSE250 = GetKickerDataFTSE250
    # _getKickerDataFTSE250.main(fetchKicker_intraday, fetchFTSE250_D, fetchFTSE250_W)

    # _getKickerDataFTSE250Aggregator = GetKickerDataFTSE250Aggregator
    # _getKickerDataFTSE250Aggregator.main(
    #     fetchKicker_intraday, fetchFTSE250_D, fetchFTSE250_W
    # )

    # ---------------- Futures ----------------

    # _getDataFutures = GetDataFutures
    # _getDataFutures.main(fetchFutures_1H, fetchFutures_D, fetchFutures_W)

    # _getIchimokuDataFutures = GetIchimokuDataFutures
    # _getIchimokuDataFutures.main(fetchFutures_1H, fetchFutures_D, fetchFutures_W)

    # _getIchimokuDataFuturesAggregator = GetIchimokuDataFuturesAggregator
    # _getIchimokuDataFuturesAggregator.main(
    #     fetchFutures_1H, fetchFutures_D, fetchFutures_W
    # )

    # _getKickerDataFutures = GetKickerDataFutures
    # _getKickerDataFutures.main(fetchKicker_intraday, fetchFutures_D, fetchFutures_W)

    # _getKickerDataFuturesAggregator = GetKickerDataFuturesAggregator
    # _getKickerDataFuturesAggregator.main(
    #     fetchKicker_intraday, fetchFutures_D, fetchFutures_W
    # )

    # ---------------- Futures Currency ----------------

    # _getDataFuturesCurrency = GetDataFuturesCurrency
    # _getDataFuturesCurrency.main(
    #     fetchCurrencyFutures_1H, fetchCurrencyFutures_D, fetchCurrencyFutures_W
    # )

    # _getIchimokuDataFuturesCurrency = GetIchimokuDataFuturesCurrency
    # _getIchimokuDataFuturesCurrency.main(
    #     fetchCurrencyFutures_1H, fetchCurrencyFutures_D, fetchCurrencyFutures_W
    # )

    # _getIchimokuDataFuturesCurrencyAggregator = GetIchimokuDataFuturesCurrencyAggregator
    # _getIchimokuDataFuturesCurrencyAggregator.main(
    #     fetchCurrencyFutures_1H, fetchCurrencyFutures_D, fetchCurrencyFutures_W
    # )

    # _getKickerDataFuturesCurrency = GetKickerDataFuturesCurrency
    # _getKickerDataFuturesCurrency.main(
    #     fetchCurrencyFutures_1H, fetchCurrencyFutures_D, fetchCurrencyFutures_W
    # )

    # _getKickerDataFuturesCurrencyAggregator = GetKickerDataFuturesCurrencyAggregator
    # _getKickerDataFuturesCurrencyAggregator.main(
    #     fetchCurrencyFutures_1H, fetchCurrencyFutures_D, fetchCurrencyFutures_W
    # )

    # ---------------- S&P 500 ----------------

    # _getDataSPX500 = GetDataSPX500
    # _getDataSPX500.main(fetchSPX500_1H, fetchSPX500_D, fetchSPX500_W)

    # _getIchimokuDataSPX500 = GetIchimokuDataSPX500
    # _getIchimokuDataSPX500.main(fetchSPX500_1H, fetchSPX500_D, fetchSPX500_W)

    # _getIchimokuDataSPX500Aggregator = GetIchimokuDataSPX500Aggregator
    # _getIchimokuDataSPX500Aggregator.main(fetchSPX500_1H, fetchSPX500_D, fetchSPX500_W)

    # _getKickerDataSPX500 = GetKickerDataSPX500
    # _getKickerDataSPX500.main(fetchKicker_intraday, fetchSPX500_D, fetchSPX500_W)

    # _getKickerDataSPX500Aggregator = GetKickerDataSPX500Aggregator
    # _getKickerDataSPX500Aggregator.main(fetchKicker_intraday, fetchSPX500_D, fetchSPX500_W)


if __name__ == "__main__":
    main()
