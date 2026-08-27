"""Packaged market-data runner modules.

Run with `python -m cloud_signal.runners.main` or call specific modules like
`python -m cloud_signal.runners.runBitfinex`.
"""

__all__ = [
    "runBitfinex",
    "runSPX500",
    "runSPDR_ETFs",
    "runRussell1000",
    "runOanda",
    "runNas100",
    "runKraken",
    "runHSI",
    "runFutures",
    "runFTSE250",
    "runFTSE100",
    "runDJ30",
    "runDJ30_source_russell",
    "runCurrencyFutures",
]
