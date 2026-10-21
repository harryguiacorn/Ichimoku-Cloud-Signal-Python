import logging

from cloud_signal.mvc.controllers.EmailDigestController import (
    create_email_digest_controller,
)

logger = logging.getLogger(__name__)


def main() -> None:
    result = create_email_digest_controller().send_digest()
    logger.info(
        "Cloud digest completed: %s matches, %s Kit broadcasts scheduled, %s already scheduled",
        result["matches"],
        result["scheduled"],
        result["skipped"],
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
