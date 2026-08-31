from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "markets.toml"

RUNTIME_DEFAULTS: Dict[str, Dict[str, Any]] = {
    "DJ30": {
        "fetch_symbols_latest_DJ30": True,
        "fetch_DJ30_1H": True,
        "fetch_DJ30_D": True,
        "fetch_DJ30_W": True,
        "fetch_DJ30_M": True,
        "fetch_kijun_analysis": False,
        "fetch_Kicker_use_datetime_format": False,
        "run_Multi_TimeFrame_Merger_DJ30": True,
        "fetch_kicker": False,
    },
    "FTSE100": {
        "fetch_symbols_latest_FTSE100": True,
        "fetch_FTSE100_1H": True,
        "fetch_FTSE100_D": True,
        "fetch_FTSE100_W": True,
        "fetch_FTSE100_M": True,
        "fetch_kijun_analysis": False,
        "fetch_Kicker_use_datetime_format": False,
        "run_Multi_TimeFrame_Merger_FTSE100": True,
        "fetch_kicker": False,
    },
    "FTSE250": {
        "fetch_symbols_latest_FTSE250": True,
        "fetch_FTSE250_1H": True,
        "fetch_FTSE250_D": True,
        "fetch_FTSE250_W": True,
        "fetch_FTSE250_M": True,
        "fetch_kijun_analysis": False,
        "fetch_Kicker_use_datetime_format": False,
        "run_Multi_TimeFrame_Merger_FTSE250": True,
        "fetch_kicker": False,
    },
    "Futures": {
        "fetch_symbols_latest_Futures": True,
        "fetch_Futures_1H": True,
        "fetch_Futures_D": True,
        "fetch_Futures_W": True,
        "fetch_Futures_M": True,
        "fetch_kijun_analysis": False,
        "fetch_Kicker_use_datetime_format": False,
        "run_Multi_TimeFrame_Merger_Futures": True,
        "fetch_kicker": False,
    },
    "CurrencyFutures": {
        "fetch_symbols_latest_CurrencyFutures": False,
        "fetch_CurrencyFutures_1H": True,
        "fetch_CurrencyFutures_D": True,
        "fetch_CurrencyFutures_W": True,
        "fetch_CurrencyFutures_M": True,
        "fetch_kijun_analysis": False,
        "fetch_Kicker_use_datetime_format": False,
        "run_Multi_TimeFrame_Merger_CurrencyFutures": True,
        "fetch_kicker": False,
    },
    "HSI": {
        "fetch_symbols_latest_HSI": True,
        "fetch_HSI_1H": True,
        "fetch_HSI_D": True,
        "fetch_HSI_W": True,
        "fetch_HSI_M": True,
        "fetch_kijun_analysis": False,
        "fetch_Kicker_use_datetime_format": False,
        "run_Multi_TimeFrame_Merger_HSI": True,
        "fetch_kicker": False,
    },
    "Nas100": {
        "fetch_symbols_latest_Nas100": True,
        "fetch_Nas100_1H": True,
        "fetch_Nas100_D": True,
        "fetch_Nas100_W": True,
        "fetch_Nas100_M": True,
        "fetch_kijun_analysis": False,
        "fetch_Kicker_use_datetime_format": False,
        "run_Multi_TimeFrame_Merger_Nas100": True,
        "fetch_kicker": False,
    },
    "Oanda": {
        "fetch_Oanda_1H": True,
        "fetch_Oanda_4H": True,
        "fetch_Oanda_D": True,
        "fetch_Oanda_W": True,
        "fetch_Oanda_M": True,
        "fetch_kijun_analysis": False,
        "fetch_Kicker_use_datetime_format": False,
        "run_Multi_TimeFrame_Merger_Oanda": True,
        "fetch_kicker": False,
    },
    "SPX500": {
        "fetch_symbols_latest_SPX500": True,
        "fetch_SPX500_1H": True,
        "fetch_SPX500_D": True,
        "fetch_SPX500_W": True,
        "fetch_SPX500_M": True,
        "fetch_kijun_analysis": False,
        "fetch_Kicker_use_datetime_format": False,
        "run_Multi_TimeFrame_Merger_SPX500": True,
        "fetch_kicker": False,
    },
    "SPDR_ETFs": {
        "fetch_symbols_latest_SPDR_ETFs": True,
        "fetch_SPDR_ETFs_1H": True,
        "fetch_SPDR_ETFs_D": True,
        "fetch_SPDR_ETFs_W": True,
        "fetch_SPDR_ETFs_M": True,
        "fetch_kijun_analysis": False,
        "fetch_Kicker_use_datetime_format": False,
        "run_Multi_TimeFrame_Merger_SPDR_ETFs": True,
        "fetch_kicker": False,
    },
    "Kraken": {
        "fetch_Kraken_1H": True,
        "fetch_Kraken_4H": True,
        "fetch_Kraken_D": True,
        "fetch_Kraken_W": True,
        "fetch_Kraken_M": True,
        "fetch_Kicker_use_datetime_format": False,
        "run_Multi_TimeFrame_Merger_Kraken": True,
        "fetch_kicker": False,
    },
    "Bitfinex": {
        "fetch_Bitfinex_1H": True,
        "fetch_Bitfinex_4H": True,
        "fetch_Bitfinex_D": True,
        "fetch_Bitfinex_W": True,
        "fetch_Bitfinex_M": True,
        "fetch_Kicker_use_datetime_format": False,
        "run_Multi_TimeFrame_Merger_Bitfinex": True,
        "fetch_kicker": False,
    },
    "Russell1000": {
        "fetch_symbols_latest_Russell1000": True,
        "fetch_Russell1000_1H": True,
        "fetch_Russell1000_D": True,
        "fetch_Russell1000_W": True,
        "fetch_Russell1000_M": True,
        "fetch_kijun_analysis": False,
        "fetch_Kicker_use_datetime_format": False,
        "run_Multi_TimeFrame_Merger_Russell1000": True,
        "fetch_kicker": False,
    },
}


def _normalize_market(raw_market: Dict[str, Any]) -> Dict[str, Any]:
    market = dict(raw_market)
    runtime = dict(market.get("runtime", {}))
    market["runtime"] = runtime
    return market


def _build_default_market(name: str, module: str, asset_list: str, data_dir: str, output_dir: str, timeframes: List[str], *, fetch_symbols: bool) -> Dict[str, Any]:
    runtime = dict(RUNTIME_DEFAULTS.get(name, {}))
    return {
        "name": name,
        "module": module,
        "asset_list": asset_list,
        "data_dir": data_dir,
        "output_dir": output_dir,
        "timeframes": timeframes,
        "fetch_symbols": fetch_symbols,
        "merge_multitimeframe": True,
        "fetch_kijun": False,
        "fetch_kicker": False,
        "symbol_key": None,
        "enabled": True,
        "runtime": runtime,
    }


DEFAULT_MARKETS: List[Dict[str, Any]] = [
    _build_default_market("DJ30", "runDJ30", "asset_list/DowJones30.csv", "data/dowjones30", "output/dowjones30", ["1h", "d", "w", "m"], fetch_symbols=True),
    _build_default_market("FTSE100", "runFTSE100", "asset_list/FTSE100.csv", "data/ftse100", "output/ftse100", ["1h", "d", "w", "m"], fetch_symbols=True),
    _build_default_market("FTSE250", "runFTSE250", "asset_list/FTSE250.csv", "data/ftse250", "output/ftse250", ["1h", "d", "w", "m"], fetch_symbols=True),
    _build_default_market("Futures", "runFutures", "asset_list/Futures.csv", "data/futures", "output/futures", ["1h", "d", "w", "m"], fetch_symbols=True),
    _build_default_market("CurrencyFutures", "runCurrencyFutures", "asset_list/FuturesCurrency.csv", "data/futurescurrency", "output/futurescurrency", ["1h", "d", "w", "m"], fetch_symbols=False),
    _build_default_market("HSI", "runHSI", "asset_list/HSI.csv", "data/hsi", "output/hsi", ["1h", "d", "w", "m"], fetch_symbols=True),
    _build_default_market("Nas100", "runNas100", "asset_list/Nasdaq100.csv", "data/nasdaq100", "output/nasdaq100", ["1h", "d", "w", "m"], fetch_symbols=True),
    _build_default_market("Oanda", "runOanda", "asset_list/Oanda.csv", "data/oanda", "output/oanda", ["1h", "4h", "d", "w", "m"], fetch_symbols=False),
    _build_default_market("SPX500", "runSPX500", "asset_list/SPX500.csv", "data/spx500", "output/spx500", ["1h", "d", "w", "m"], fetch_symbols=True),
    _build_default_market("SPDR_ETFs", "runSPDR_ETFs", "asset_list/SPDR_ETFs.csv", "data/spdr_etfs", "output/spdr_etfs", ["1h", "d", "w", "m"], fetch_symbols=False),
    _build_default_market("Kraken", "runKraken", "asset_list/Kraken.csv", "data/kraken", "output/kraken", ["1h", "4h", "d", "w", "m"], fetch_symbols=False),
    _build_default_market("Bitfinex", "runBitfinex", "asset_list/Bitfinex.csv", "data/bitfinex", "output/bitfinex", ["1h", "4h", "d", "w", "m"], fetch_symbols=False),
    _build_default_market("Russell1000", "runRussell1000", "asset_list/Russell1000.csv", "data/russell1000", "output/russell1000", ["1h", "d", "w", "m"], fetch_symbols=True),
]


def _load_toml_market_config(config_path: Path | str | None = None) -> List[Dict[str, Any]]:
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    if not path.exists():
        return [_normalize_market(market) for market in DEFAULT_MARKETS]

    with path.open("rb") as fh:
        payload = tomllib.load(fh)
    markets = payload.get("market", [])
    if not markets:
        return [_normalize_market(market) for market in DEFAULT_MARKETS]
    return [_normalize_market(market) for market in markets]


MARKETS: List[Dict[str, Any]] = _load_toml_market_config(os.getenv("CLOUD_SIGNAL_MARKETS_CONFIG"))


def list_market_names() -> List[str]:
    return [market["name"] for market in MARKETS]


def get_market_config(name: str) -> Dict[str, Any]:
    for market in MARKETS:
        if market["name"].lower() == name.lower():
            runtime = dict(market.get("runtime", {}))
            market_copy = dict(market)
            market_copy["runtime"] = runtime
            return market_copy
    raise KeyError(f"Unknown market: {name}")


def get_market_configs(names: List[str] | None = None) -> List[Dict[str, Any]]:
    if names is None:
        return [dict(market) for market in MARKETS]
    return [get_market_config(name) for name in names]
