#!/usr/bin/env python3
import logging
from scripts import runSPX500 as _module

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Shim: launching scripts.runSPX500")
    _module.main()
