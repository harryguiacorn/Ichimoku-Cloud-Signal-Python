from cloud_signal.runners._bootstrap import ensure_repo_root, setup_runner_logging
from cloud_signal.runners.market_registry import get_market_configs
from cloud_signal.runners.run_market import run_market

ensure_repo_root()
RUNNER_CLASS = None
log_file = setup_runner_logging(__name__, RUNNER_CLASS)
import logging

logger = logging.getLogger(__name__)


def main():
    """Run all enabled market runners from the registry."""
    for market in get_market_configs():
        if not market.get("enabled", True):
            continue
        logger.info("Starting runner for %s", market["name"])
        run_market(market["name"])

    logger.info("All configured market runners completed.")


if __name__ == "__main__":
    main()
