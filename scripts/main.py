from scripts._bootstrap import ensure_repo_root, setup_runner_logging

ensure_repo_root()
RUNNER_CLASS = None
log_file = setup_runner_logging(__name__, RUNNER_CLASS)
import logging
from datetime import datetime
from pytz import timezone

from scripts import (
    runDJ30,
    runNas100,
    runFTSE100,
    runFTSE250,
    runFutures,
    runCurrencyFutures,
    runSPX500,
    runOanda,
    runBitfinex,
    runSPDR_ETFs,
    runKraken,
    runHSI,
)

logger = logging.getLogger(__name__)

fetch_symbols_latest_DJ30 = True
fetch_symbols_latest_SPX500 = True
fetch_symbols_latest_Nas100 = True
fetch_symbols_latest_FTSE100 = True
fetch_symbols_latest_FTSE250 = True
fetch_symbols_latest_Futures = True
fetch_symbols_latest_CurrencyFutures = True
fetch_symbols_latest_HSI = True

fetch_DJ30_1H = True
fetch_SPX500_1H = True
fetch_Nas100_1H = True
fetch_FTSE100_1H = True
fetch_FTSE250_1H = True
fetch_Futures_1H = True
fetch_CurrencyFutures_1H = True
fetch_Oanda_1H = True
fetch_Bitfinex_1H = True
fetch_Kraken_1H = True
fetch_SPDR_ETFs_1H = True
fetch_HSI_1H = True

fetch_Oanda_4H = True
fetch_Bitfinex_4H = True
fetch_Kraken_4H = True

fetch_DJ30_D = True
fetch_SPX500_D = True
fetch_Nas100_D = True
fetch_FTSE100_D = True
fetch_FTSE250_D = True
fetch_Futures_D = True
fetch_CurrencyFutures_D = True
fetch_Oanda_D = True
fetch_Bitfinex_D = True
fetch_Kraken_D = True
fetch_SPDR_ETFs_D = True
fetch_HSI_D = True

fetch_DJ30_W = True
fetch_SPX500_W = True
fetch_Nas100_W = True
fetch_FTSE100_W = True
fetch_FTSE250_W = True
fetch_Futures_W = True
fetch_CurrencyFutures_W = True
fetch_Oanda_W = True
fetch_Bitfinex_W = True
fetch_Kraken_W = True
fetch_SPDR_ETFs_W = True
fetch_HSI_W = True

fetch_DJ30_M = True
fetch_SPX500_M = True
fetch_Nas100_M = True
fetch_FTSE100_M = True
fetch_FTSE250_M = True
fetch_Futures_M = True
fetch_CurrencyFutures_M = True
fetch_Oanda_M = True
fetch_Bitfinex_M = True
fetch_Kraken_M = True
fetch_SPDR_ETFs_M = True
fetch_HSI_M = True

run_Multi_TimeFrame_Merger_DJ30 = True
run_Multi_TimeFrame_Merger_SPX500 = True
run_Multi_TimeFrame_Merger_Nas100 = True
run_Multi_TimeFrame_Merger_FTSE100 = True
run_Multi_TimeFrame_Merger_FTSE250 = True
run_Multi_TimeFrame_Merger_Futures = True
run_Multi_TimeFrame_Merger_CurrencyFutures = True
run_Multi_TimeFrame_Merger_Oanda = True
run_Multi_TimeFrame_Merger_Bitfinex = True
run_Multi_TimeFrame_Merger_Kraken = True
