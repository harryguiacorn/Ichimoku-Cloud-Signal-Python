#!/usr/bin/env python3
import logging
from cloud_signal.runners import runDJ30_source_russell as _module

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    filemode="w",
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Shim: launching scripts.runDJ30_source_russell")
    _module.main()
