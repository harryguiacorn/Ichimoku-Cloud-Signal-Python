from __future__ import annotations

import argparse
import importlib
import logging
from collections.abc import Iterable
from time import perf_counter
from typing import Any

from cloud_signal.cache import log_cache_metrics
from cloud_signal.runners.market_registry import get_market_config

logger = logging.getLogger(__name__)

TIMEFRAME_SUFFIXES = {
    "1h": "1H",
    "4h": "4H",
    "d": "D",
    "w": "W",
    "m": "M",
}


def _normalize_timeframes(
    config: dict[str, Any], timeframes: Iterable[str]
) -> set[str]:
    if isinstance(timeframes, str):
        timeframes = [timeframes]
    available = {item.lower() for item in config.get("timeframes", [])}
    requested = {item.lower() for item in timeframes}
    unknown = requested - available
    if unknown:
        raise ValueError(
            f"Unsupported timeframe(s) for {config['name']}: "
            f"{', '.join(sorted(unknown))}"
        )
    if not requested:
        raise ValueError("At least one timeframe must be selected")
    return requested


def _runtime_for_timeframes(
    config: dict[str, Any], timeframes: Iterable[str]
) -> tuple[dict[str, Any], set[str]]:
    runtime = dict(config.get("runtime", {}))
    available = {item.lower() for item in config.get("timeframes", [])}
    requested = _normalize_timeframes(config, timeframes)
    if requested != available:
        for timeframe in available:
            suffix = TIMEFRAME_SUFFIXES.get(timeframe)
            if suffix is None:
                raise ValueError(
                    f"No runner flag mapping exists for timeframe "
                    f"{timeframe!r}"
                )
            flag = f"fetch_{config['name']}_{suffix}"
            if flag not in runtime:
                raise ValueError(
                    f"Runner configuration for {config['name']} is missing "
                    f"the {flag!r} flag"
                )
            runtime[flag] = timeframe in requested

        merger_flag = (
            f"run_Multi_TimeFrame_Merger_{config['name']}"
        )
        if merger_flag not in runtime:
            raise ValueError(
                f"Runner configuration for {config['name']} is missing "
                f"the {merger_flag!r} flag required for partial runs"
            )
        runtime[merger_flag] = False
    return runtime, requested


def run_market(name: str, timeframes: Iterable[str] | None = None):
    started_at = perf_counter()
    config = get_market_config(name)
    module_name = f"cloud_signal.runners.{config['module']}"
    try:
        runtime = config.get("runtime", {})
        selected_timeframes = None
        if timeframes is not None:
            if config["name"].lower() == "majoretfs":
                selected_timeframes = _normalize_timeframes(
                    config, timeframes
                )
            else:
                runtime, selected_timeframes = _runtime_for_timeframes(
                    config, timeframes
                )

        module = importlib.import_module(module_name)
        if not hasattr(module, "main"):
            raise AttributeError(
                f"Runner module {module_name} has no main() entry point"
            )
        if config["name"].lower() == "majoretfs" and selected_timeframes:
            runtime["timeframes"] = selected_timeframes
        if not runtime:
            return module.main()
        return module.main(**runtime)
    finally:
        elapsed = perf_counter() - started_at
        logger.info(
            "Market runner %s finished in %.2f seconds",
            name,
            elapsed,
        )
        log_cache_metrics()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run a configured market workflow."
    )
    parser.add_argument(
        "--market", required=True, help="Market name, e.g. FTSE250"
    )
    parser.add_argument(
        "--timeframes",
        nargs="+",
        help="Optional timeframe subset, e.g. 1h d. "
        "Partial runs skip multi-timeframe merged outputs.",
    )
    args = parser.parse_args()
    run_market(args.market, args.timeframes)
