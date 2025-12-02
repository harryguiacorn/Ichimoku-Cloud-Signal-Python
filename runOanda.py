#!/usr/bin/env python3
import logging
from scripts import runOanda as _module

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    filemode="w",
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Shim: launching scripts.runOanda")
    _module.main()
