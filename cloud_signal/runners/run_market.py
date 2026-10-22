from __future__ import annotations

import argparse
import importlib
import logging
from time import perf_counter

from cloud_signal.runners.market_registry import get_market_config

logger = logging.getLogger(__name__)


def run_market(name: str):
    started_at = perf_counter()
    config = get_market_config(name)
    module_name = f"cloud_signal.runners.{config['module']}"
    try:
        module = importlib.import_module(module_name)
        if not hasattr(module, "main"):
            raise AttributeError(
                f"Runner module {module_name} has no main() entry point"
            )
        runtime = config.get("runtime", {})
        if not runtime:
            return module.main()
        return module.main(**runtime)
    finally:
        logger.info(
            "Market runner %s finished in %.2f seconds",
            name,
            perf_counter() - started_at,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run a configured market workflow."
    )
    parser.add_argument(
        "--market", required=True, help="Market name, e.g. FTSE250"
    )
    args = parser.parse_args()
    run_market(args.market)
