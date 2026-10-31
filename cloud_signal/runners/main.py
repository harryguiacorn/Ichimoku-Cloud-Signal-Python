import argparse
import logging
from collections.abc import Iterable

from cloud_signal.mvc.controllers.EmailDigestController import (
    create_email_digest_controller,
)
from cloud_signal.runners._bootstrap import (
    ensure_repo_root,
    setup_runner_logging,
)
from cloud_signal.runners.market_registry import get_market_configs
from cloud_signal.runners.run_market import run_market

ensure_repo_root()
RUNNER_CLASS = None
log_file = setup_runner_logging(__name__, RUNNER_CLASS)

logger = logging.getLogger(__name__)


def main(
    markets: Iterable[str] | None = None,
    send_digest: bool | None = None,
) -> None:
    """Run enabled market runners, optionally limited to selected names."""
    configured_markets = get_market_configs()
    if markets is not None:
        requested = {name.casefold() for name in markets}
        known = {
            market["name"].casefold(): market["name"]
            for market in configured_markets
        }
        unknown = requested - known.keys()
        if unknown:
            raise ValueError(
                f"Unknown market(s): {', '.join(sorted(unknown))}"
            )
        configured_markets = [
            market
            for market in configured_markets
            if market["name"].casefold() in requested
        ]

    for market in configured_markets:
        if not market.get("enabled", True):
            continue
        logger.info("Starting runner for %s", market["name"])
        run_market(market["name"])

    logger.info("Selected market runners completed.")
    if send_digest is None:
        send_digest = markets is None
    if not send_digest:
        return
    controller = create_email_digest_controller()
    result = controller.send_digest()
    logger.info(
        "Email digest completed: %s matches, %s Kit broadcasts scheduled, %s already scheduled",
        result["matches"],
        result["scheduled"],
        result["skipped"],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run enabled market scans from the registry."
    )
    parser.add_argument(
        "--markets",
        nargs="+",
        help="Optional market names; by default, run all enabled markets.",
    )
    parser.add_argument(
        "--send-digest",
        action="store_true",
        default=None,
        help="Send the email digest after the selected scans.",
    )
    args = parser.parse_args()
    main(args.markets, send_digest=args.send_digest)
