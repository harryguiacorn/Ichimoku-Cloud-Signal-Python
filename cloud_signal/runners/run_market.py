from __future__ import annotations

import argparse
import importlib

from cloud_signal.runners.market_registry import get_market_config


def run_market(name: str):
    config = get_market_config(name)
    module_name = f"cloud_signal.runners.{config['module']}"
    module = importlib.import_module(module_name)
    if not hasattr(module, "main"):
        raise AttributeError(f"Runner module {module_name} has no main() entry point")
    runtime = config.get("runtime", {})
    if not runtime:
        return module.main()
    return module.main(**runtime)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a configured market workflow.")
    parser.add_argument("--market", required=True, help="Market name, e.g. FTSE250")
    args = parser.parse_args()
    run_market(args.market)
