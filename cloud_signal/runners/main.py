from cloud_signal.runners._bootstrap import (
    ensure_repo_root,
    setup_runner_logging,
)
from cloud_signal.runners.market_registry import get_market_configs
from cloud_signal.runners.run_market import run_market
from cloud_signal.mvc.controllers.EmailDigestController import (
    create_email_digest_controller,
)

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
    controller = create_email_digest_controller()
    result = controller.send_digest()
    logger.info(
        "Email digest completed: %s matches, %s Kit broadcasts scheduled, %s already scheduled",
        result["matches"],
        result["scheduled"],
        result["skipped"],
    )


if __name__ == "__main__":
    main()
