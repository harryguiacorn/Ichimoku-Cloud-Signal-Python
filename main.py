import runDJ30, runNas100, runFTSE100, runFTSE250, runFutures, runCurrencyFutures, runSPX500, runOanda, runBitfinex, runSPDR_ETFs

from datetime import datetime
from pytz import timezone

fetch_symbols_latest_DJ30 = True
fetch_symbols_latest_SPX500 = True
fetch_symbols_latest_Nas100 = True
fetch_symbols_latest_FTSE100 = True
fetch_symbols_latest_FTSE250 = True
fetch_symbols_latest_Futures = True
fetch_symbols_latest_CurrencyFutures = True

fetch_DJ30_1H = True
fetch_SPX500_1H = True
fetch_Nas100_1H = True
fetch_FTSE100_1H = True
fetch_FTSE250_1H = True
fetch_Futures_1H = True
fetch_CurrencyFutures_1H = True
fetch_Oanda_1H = True
fetch_Bitfinex_1H = True
fetch_SPDR_ETFs_1H = True

fetch_Oanda_4H = True
fetch_Bitfinex_4H = True

fetch_DJ30_D = True
fetch_SPX500_D = True
fetch_Nas100_D = True
fetch_FTSE100_D = True
fetch_FTSE250_D = True
fetch_Futures_D = True
fetch_CurrencyFutures_D = True
fetch_Oanda_D = True
fetch_Bitfinex_D = True
fetch_SPDR_ETFs_D = True

fetch_DJ30_W = True
fetch_SPX500_W = True
fetch_Nas100_W = True
fetch_FTSE100_W = True
fetch_FTSE250_W = True
fetch_Futures_W = True
fetch_CurrencyFutures_W = True
fetch_Oanda_W = True
fetch_Bitfinex_W = True
fetch_SPDR_ETFs_W = True

fetch_DJ30_M = True
fetch_SPX500_M = True
fetch_Nas100_M = True
fetch_FTSE100_M = True
fetch_FTSE250_M = True
fetch_Futures_M = True
fetch_CurrencyFutures_M = True
fetch_Oanda_M = True
fetch_Bitfinex_M = True
fetch_SPDR_ETFs_M = True

run_Multi_TimeFrame_Merger_DJ30 = True
run_Multi_TimeFrame_Merger_SPX500 = True
run_Multi_TimeFrame_Merger_Nas100 = True
run_Multi_TimeFrame_Merger_FTSE100 = True
run_Multi_TimeFrame_Merger_FTSE250 = True
run_Multi_TimeFrame_Merger_Futures = True
run_Multi_TimeFrame_Merger_CurrencyFutures = True
run_Multi_TimeFrame_Merger_Oanda = True
run_Multi_TimeFrame_Merger_Bitfinex = True
run_Multi_TimeFrame_Merger_SPDR_ETFs = True

fetch_kijun_analysis = False

fetch_kicker = False

# Use "Datetime" for Yahoo intraday data,
# "Date" for D, W, M data.
# Use "Datetime" for all Oanda data.
fetch_Kicker_use_datetime_format = False


def main():
    # Stop script being auto-run by Replit or Gitpod
    # return

    # Time counter
    london_tz_start = timezone("Europe/London")
    time_start = datetime.now(london_tz_start)
    time_start_formatted = time_start.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Main Task begins at: {time_start_formatted} [UK]")

    # ---------------- Oanda ----------------

    _runOanda = runOanda
    _runOanda.main(
        fetch_Oanda_1H,
        fetch_Oanda_4H,
        fetch_Oanda_D,
        fetch_Oanda_W,
        fetch_Oanda_M,
        fetch_kijun_analysis,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_Oanda,
        fetch_kicker,
    )
    print("\nTasks completed.")

    # ---------------- Dow Jones 30 ----------------

    _runDJ30 = runDJ30
    _runDJ30.main(
        fetch_symbols_latest_DJ30,
        fetch_DJ30_1H,
        fetch_DJ30_D,
        fetch_DJ30_W,
        fetch_DJ30_M,
        fetch_kijun_analysis,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_DJ30,
        fetch_kicker,
    )

    # ---------------- Nasdaq 100 ----------------

    _runNas100 = runNas100
    _runNas100.main(
        fetch_symbols_latest_Nas100,
        fetch_Nas100_1H,
        fetch_Nas100_D,
        fetch_Nas100_W,
        fetch_Nas100_M,
        fetch_kijun_analysis,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_Nas100,
        fetch_kicker,
    )

    # ---------------- S&P 500 ----------------

    _runSPX500 = runSPX500
    _runSPX500.main(
        fetch_SPX500_1H,
        fetch_SPX500_D,
        fetch_SPX500_W,
        fetch_SPX500_M,
        fetch_kijun_analysis,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_SPX500,
        fetch_kicker,
    )

    # ---------------- FTSE 100 ----------------

    _runFTSE100 = runFTSE100
    _runFTSE100.main(
        fetch_symbols_latest_FTSE100,
        fetch_FTSE100_1H,
        fetch_FTSE100_D,
        fetch_FTSE100_W,
        fetch_FTSE100_M,
        fetch_kijun_analysis,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_FTSE100,
        fetch_kicker,
    )

    # ---------------- FTSE 250 ----------------

    _runFTSE250 = runFTSE250
    _runFTSE250.main(
        fetch_symbols_latest_FTSE250,
        fetch_FTSE250_1H,
        fetch_FTSE250_D,
        fetch_FTSE250_W,
        fetch_FTSE250_M,
        fetch_kijun_analysis,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_FTSE250,
        fetch_kicker,
    )

    # ---------------- Futures ----------------

    _runFutures = runFutures
    _runFutures.main(
        fetch_symbols_latest_Futures,
        fetch_Futures_1H,
        fetch_Futures_D,
        fetch_Futures_W,
        fetch_Futures_M,
        fetch_kijun_analysis,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_Futures,
        fetch_kicker,
    )

    # ---------------- Futures Currency ----------------

    _runCurrencyFutures = runCurrencyFutures
    _runCurrencyFutures.main(
        fetch_symbols_latest_CurrencyFutures,
        fetch_CurrencyFutures_1H,
        fetch_CurrencyFutures_D,
        fetch_CurrencyFutures_W,
        fetch_CurrencyFutures_M,
        fetch_kijun_analysis,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_CurrencyFutures,
        fetch_kicker,
    )

    # ---------------- Bitfinex ----------------

    """ _runBitfinex = runBitfinex
    _runBitfinex.main(
        fetch_Bitfinex_1H,
        fetch_Bitfinex_4H,
        fetch_Bitfinex_D,
        fetch_Bitfinex_W,
        fetch_Bitfinex_M,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_Bitfinex,
        fetch_kicker,
    ) """

    # ---------------- SPDR ETFs ----------------

    _runSPDR_ETFs = runSPDR_ETFs
    _runSPDR_ETFs.main(
        False,
        fetch_SPDR_ETFs_1H,
        fetch_SPDR_ETFs_D,
        fetch_SPDR_ETFs_W,
        fetch_SPDR_ETFs_M,
        fetch_kijun_analysis,
        fetch_Kicker_use_datetime_format,
        run_Multi_TimeFrame_Merger_SPDR_ETFs,
        fetch_kicker,
    )

    # calculate time elapsed
    london_tz_finish = timezone("Europe/London")
    time_finish = datetime.now(london_tz_finish)
    time_elapsed = time_finish - time_start
    time_finish_formatted = time_finish.strftime("%Y-%m-%d %H:%M:%S")
    print(
        f"\nMain Tasks completed at {time_finish_formatted} [UK] (Time elapsed: {time_elapsed})",
    )


if __name__ == "__main__":
    main()
