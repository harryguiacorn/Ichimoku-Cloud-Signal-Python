from cloud_signal.runners._bootstrap import ensure_repo_root, setup_runner_logging
from cloud_signal import config

ensure_repo_root()
RUNNER_CLASS = None
log_file = setup_runner_logging(__name__, RUNNER_CLASS)
import logging
from datetime import datetime
from pytz import timezone

from cloud_signal.runners import (
    runCurrencyFutures,
    runDJ30,
    runFTSE100,
    runFTSE250,
    runFutures,
    runHSI,
    runKraken,
    runNas100,
    runOanda,
    runSPDR_ETFs,
    runSPX500,
)

logger = logging.getLogger(__name__)

def main():
    # Run the main class and save output
    # python main.py > output_main.txt

    # Stop script being auto-run by Replit or Gitpod
    # return

    # Time counter
    london_tz_start = timezone("Europe/London")
    time_start = datetime.now(london_tz_start)
    time_start_formatted = time_start.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Main Task begins at: {time_start_formatted} [UK]")

    # ---------------- Oanda ----------------

    _runOanda = runOanda
    _runOanda.main(
        config.fetch_Oanda_1H,
        config.fetch_Oanda_4H,
        config.fetch_Oanda_D,
        config.fetch_Oanda_W,
        config.fetch_Oanda_M,
        config.fetch_kijun_analysis,
        config.fetch_Kicker_use_datetime_format,
        config.run_Multi_TimeFrame_Merger_Oanda,
        config.fetch_kicker,
    )
    logger.info("\nTasks completed.")

    # ---------------- Dow Jones 30 ----------------

    _runDJ30 = runDJ30
    _runDJ30.main(
        config.fetch_symbols_latest_DJ30,
        config.fetch_DJ30_1H,
        config.fetch_DJ30_D,
        config.fetch_DJ30_W,
        config.fetch_DJ30_M,
        config.fetch_kijun_analysis,
        config.fetch_Kicker_use_datetime_format,
        config.run_Multi_TimeFrame_Merger_DJ30,
        config.fetch_kicker,
    )

    # ---------------- Nasdaq 100 ----------------

    _runNas100 = runNas100
    _runNas100.main(
        config.fetch_symbols_latest_Nas100,
        config.fetch_Nas100_1H,
        config.fetch_Nas100_D,
        config.fetch_Nas100_W,
        config.fetch_Nas100_M,
        config.fetch_kijun_analysis,
        config.fetch_Kicker_use_datetime_format,
        config.run_Multi_TimeFrame_Merger_Nas100,
        config.fetch_kicker,
    )

    # ---------------- S&P 500 ----------------

    _runSPX500 = runSPX500
    _runSPX500.main(
        config.fetch_SPX500_1H,
        config.fetch_SPX500_D,
        config.fetch_SPX500_W,
        config.fetch_SPX500_M,
        config.fetch_kijun_analysis,
        config.fetch_Kicker_use_datetime_format,
        config.run_Multi_TimeFrame_Merger_SPX500,
        config.fetch_kicker,
    )

    # ---------------- SPDR ETFs ----------------

    _runSPDR_ETFs = runSPDR_ETFs
    _runSPDR_ETFs.main(
        False,
        config.fetch_SPDR_ETFs_1H,
        config.fetch_SPDR_ETFs_D,
        config.fetch_SPDR_ETFs_W,
        config.fetch_SPDR_ETFs_M,
        config.fetch_kijun_analysis,
        config.fetch_Kicker_use_datetime_format,
        config.run_Multi_TimeFrame_Merger_SPDR_ETFs,
        config.fetch_kicker,
    )

    # ---------------- Kraken ----------------

    _runKraken = runKraken
    _runKraken.main(
        config.fetch_Kraken_1H,
        config.fetch_Kraken_4H,
        config.fetch_Kraken_D,
        config.fetch_Kraken_W,
        config.fetch_Kraken_M,
        config.fetch_Kicker_use_datetime_format,
        config.run_Multi_TimeFrame_Merger_Kraken,
        config.fetch_kicker,
    )

    # ---------------- FTSE 100 ----------------

    _runFTSE100 = runFTSE100
    _runFTSE100.main(
        config.fetch_symbols_latest_FTSE100,
        config.fetch_FTSE100_1H,
        config.fetch_FTSE100_D,
        config.fetch_FTSE100_W,
        config.fetch_FTSE100_M,
        config.fetch_kijun_analysis,
        config.fetch_Kicker_use_datetime_format,
        config.run_Multi_TimeFrame_Merger_FTSE100,
        config.fetch_kicker,
    )

    # ---------------- FTSE 250 ----------------

    _runFTSE250 = runFTSE250
    _runFTSE250.main(
        config.fetch_symbols_latest_FTSE250,
        config.fetch_FTSE250_1H,
        config.fetch_FTSE250_D,
        config.fetch_FTSE250_W,
        config.fetch_FTSE250_M,
        config.fetch_kijun_analysis,
        config.fetch_Kicker_use_datetime_format,
        config.run_Multi_TimeFrame_Merger_FTSE250,
        config.fetch_kicker,
    )

    # ---------------- Futures ----------------

    _runFutures = runFutures
    _runFutures.main(
        config.fetch_symbols_latest_Futures,
        config.fetch_Futures_1H,
        config.fetch_Futures_D,
        config.fetch_Futures_W,
        config.fetch_Futures_M,
        config.fetch_kijun_analysis,
        config.fetch_Kicker_use_datetime_format,
        config.run_Multi_TimeFrame_Merger_Futures,
        config.fetch_kicker,
    )

    # ---------------- Hang Seng Index ----------------
    _runHSI = runHSI
    _runHSI.main(
        config.fetch_symbols_latest_HSI,
        config.fetch_HSI_1H,
        config.fetch_HSI_D,
        config.fetch_HSI_W,
        config.fetch_HSI_M,
        config.fetch_kijun_analysis,
        config.fetch_Kicker_use_datetime_format,
        config.run_Multi_TimeFrame_Merger_HSI,
        config.fetch_kicker,
    )

    # ---------------- Futures Currency ----------------

    _runCurrencyFutures = runCurrencyFutures
    _runCurrencyFutures.main(
        config.fetch_symbols_latest_CurrencyFutures,
        config.fetch_CurrencyFutures_1H,
        config.fetch_CurrencyFutures_D,
        config.fetch_CurrencyFutures_W,
        config.fetch_CurrencyFutures_M,
        config.fetch_kijun_analysis,
        config.fetch_Kicker_use_datetime_format,
        config.run_Multi_TimeFrame_Merger_CurrencyFutures,
        config.fetch_kicker,
    )

    # ---------------- Bitfinex ----------------

    """ _runBitfinex = runBitfinex
    _runBitfinex.main(
        config.fetch_Bitfinex_1H,
        config.fetch_Bitfinex_4H,
        config.fetch_Bitfinex_D,
        config.fetch_Bitfinex_W,
        config.fetch_Bitfinex_M,
        config.fetch_Kicker_use_datetime_format,
        config.run_Multi_TimeFrame_Merger_Bitfinex,
        config.fetch_kicker,
    ) """

    # calculate time elapsed
    london_tz_finish = timezone("Europe/London")
    time_finish = datetime.now(london_tz_finish)
    time_elapsed = time_finish - time_start
    time_finish_formatted = time_finish.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(
        f"\nMain Tasks completed at {time_finish_formatted} [UK] (Time elapsed: {time_elapsed})",
    )


if __name__ == "__main__":
    main()
