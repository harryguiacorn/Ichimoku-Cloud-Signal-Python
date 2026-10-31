import logging
import os

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def get_instruments():
    """Fetch FXCM instruments using credentials configured outside the source."""
    load_dotenv()
    token = os.getenv("FXCM_ACCESS_TOKEN")
    if not token:
        raise RuntimeError(
            "FXCM_ACCESS_TOKEN must be set to use the FXCM integration"
        )

    try:
        import fxcmpy
    except ImportError as error:
        raise RuntimeError(
            "FXCM integration requires the optional 'fxcmpy' package"
        ) from error

    connection = fxcmpy.fxcmpy(access_token=token, log_level="error")
    try:
        instruments = connection.get_instruments()
        logger.info("Sample FXCM instruments: %s", instruments[:5])
        return instruments
    finally:
        connection.close()


if __name__ == "__main__":
    get_instruments()
