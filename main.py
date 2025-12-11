#!/usr/bin/env python3
from scripts._bootstrap import ensure_repo_root, setup_runner_logging

ensure_repo_root()
# configure runner logging before importing the heavy `scripts.main` module
# use a stable filename 'main' so logs go to `output/logs/main.txt`
log_file = setup_runner_logging("main", None)

import logging
from scripts import main as _module

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Shim: launching scripts.main")
    _module.main()
