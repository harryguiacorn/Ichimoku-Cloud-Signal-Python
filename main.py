from src.mvc import GetDataDJ30
from src.mvc import GetIchimokuDataDJ30
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

fetchDJ30 = True
fetchSPX500 = True
fetchNas100 = True
fetchFTSE100 = True
fetchFTSE250 = False
fetchFutures = False
fetchCurrencyFutures = False

# ---------------- Dow Jones 30 ----------------
if fetchDJ30:
    _getDataDJ30 = GetDataDJ30
    # _getDataDJ30.main()

    _getIchimokuDataDJ30 = GetIchimokuDataDJ30
    _getIchimokuDataDJ30.main()

    _getIchimokuDataDJ30Aggregator = GetIchimokuDataDJ30Aggregator
    _getIchimokuDataDJ30Aggregator.main()

    _getKickerDataDJ30 = GetKickerDataDJ30
    _getKickerDataDJ30.main()

    _getKickerDataDJ30Aggregator = GetKickerDataDJ30Aggregator
    _getKickerDataDJ30Aggregator.main()

# ---------------- Nasdaq 100 ----------------
if fetchNas100:
    _getDataNas100 = GetDataNas100
    # _getDataNas100.main()

    _getIchimokuDataNas100 = GetIchimokuDataNas100
    _getIchimokuDataNas100.main()

    _getIchimokuDataNas100Aggregator = GetIchimokuDataNas100Aggregator
    _getIchimokuDataNas100Aggregator.main()

    _getKickerDataNas100 = GetKickerDataNas100
    _getKickerDataNas100.main()

    _getKickerDataNas100Aggregator = GetKickerDataNas100Aggregator
    _getKickerDataNas100Aggregator.main()

# ---------------- FTSE 100 ----------------
if fetchFTSE100:
    _getDataFTSE100 = GetDataFTSE100
    # _getDataFTSE100.main()

    _getIchimokuDataFTSE100 = GetIchimokuDataFTSE100
    _getIchimokuDataFTSE100.main()

    _getIchimokuDataFTSE100Aggregator = GetIchimokuDataFTSE100Aggregator
    _getIchimokuDataFTSE100Aggregator.main()

    _getKickerDataFTSE100 = GetKickerDataFTSE100
    _getKickerDataFTSE100.main()

    _getKickerDataFTSE100Aggregator = GetKickerDataFTSE100Aggregator
    _getKickerDataFTSE100Aggregator.main()

# ---------------- FTSE 250 ----------------
if fetchFTSE250:
    _getDataFTSE250 = GetDataFTSE250
    # _getDataFTSE250.main()

    _getIchimokuDataFTSE250 = GetIchimokuDataFTSE250
    _getIchimokuDataFTSE250.main()

    _getIchimokuDataFTSE250Aggregator = GetIchimokuDataFTSE250Aggregator
    _getIchimokuDataFTSE250Aggregator.main()

    _getKickerDataFTSE250 = GetKickerDataFTSE250
    _getKickerDataFTSE250.main()

    _getKickerDataFTSE250Aggregator = GetKickerDataFTSE250Aggregator
    _getKickerDataFTSE250Aggregator.main()

# ---------------- S&P 500 ----------------
if fetchSPX500:
    _getDataSPX500 = GetDataSPX500
    # _getDataSPX500.main()

    _getIchimokuDataSPX500 = GetIchimokuDataSPX500
    _getIchimokuDataSPX500.main()

    _getIchimokuDataSPX500Aggregator = GetIchimokuDataSPX500Aggregator
    _getIchimokuDataSPX500Aggregator.main()

    _getKickerDataSPX500 = GetKickerDataSPX500
    _getKickerDataSPX500.main()

    _getKickerDataSPX500Aggregator = GetKickerDataSPX500Aggregator
    _getKickerDataSPX500Aggregator.main()

# ---------------- Futures ----------------
if fetchFutures:
    _getDataFutures = GetDataFutures
    _getDataFutures.main()

    _getIchimokuDataFutures = GetIchimokuDataFutures
    _getIchimokuDataFutures.main()

    _getIchimokuDataFuturesAggregator = GetIchimokuDataFuturesAggregator
    _getIchimokuDataFuturesAggregator.main()

    _getKickerDataFutures = GetKickerDataFutures
    _getKickerDataFutures.main()

    _getKickerDataFuturesAggregator = GetKickerDataFuturesAggregator
    _getKickerDataFuturesAggregator.main()

# ---------------- Futures Currency ----------------
if fetchCurrencyFutures:
    _getDataFuturesCurrency = GetDataFuturesCurrency
    _getDataFuturesCurrency.main()

    _getIchimokuDataFuturesCurrency = GetIchimokuDataFuturesCurrency
    _getIchimokuDataFuturesCurrency.main()

    _getIchimokuDataFuturesCurrencyAggregator = GetIchimokuDataFuturesCurrencyAggregator
    _getIchimokuDataFuturesCurrencyAggregator.main()

    _getKickerDataFuturesCurrency = GetKickerDataFuturesCurrency
    _getKickerDataFuturesCurrency.main()

    _getKickerDataFuturesCurrencyAggregator = GetKickerDataFuturesCurrencyAggregator
    _getKickerDataFuturesCurrencyAggregator.main()

