import logging
import sys
from types import ModuleType

from cloud_signal.runners._bootstrap import (
    _log_stage_summary,
    instrument_controller_mains,
    setup_runner_logging,
    timed_stage,
)


def test_controller_main_is_timed_once_and_keeps_return_value(caplog):
    module = ModuleType(
        "cloud_signal.mvc.controllers.GetDataTest"
    )
    module.main = lambda value: value + 1
    logger = logging.getLogger("test.runner.logging")

    with caplog.at_level(logging.INFO, logger=logger.name):
        instrument_controller_mains(logger, [module])
        instrument_controller_mains(logger, [module])
        result = module.main(2)

    assert result == 3
    assert sum(
        "Workflow stage cloud_signal.mvc.controllers.GetDataTest.main"
        in record.getMessage()
        for record in caplog.records
    ) == 1


def test_stage_summary_logs_a_table(caplog):
    logger = logging.getLogger("test.runner.summary")
    with caplog.at_level(logging.INFO):
        with timed_stage(logger, "market data fetch"):
            pass
        with timed_stage(logger, "signal aggregation"):
            pass
        _log_stage_summary()

    summary = next(
        record.getMessage()
        for record in caplog.records
        if "Workflow stage timing summary:" in record.getMessage()
    )
    assert "| Stage" in summary
    assert "| Calls" in summary
    assert "| Total time" in summary
    assert "| market data fetch" in summary
    assert "| signal aggregation" in summary
    total_row = next(
        line for line in summary.splitlines() if "| TOTAL" in line
    )
    assert total_row.rstrip().endswith("s |")


def test_setup_runner_logging_adds_file_when_console_handler_exists(
    tmp_path,
):
    root = logging.getLogger()
    original_handlers = root.handlers[:]
    original_level = root.level
    console_handler = logging.StreamHandler(sys.stderr)
    root.handlers = [console_handler]

    try:
        log_path = setup_runner_logging(
            "test_runner", log_dir=str(tmp_path)
        )
        logging.getLogger("test.runner.file").info("file logging works")
        for handler in root.handlers:
            handler.flush()

        content = (tmp_path / "test_runner.txt").read_text(
            encoding="utf-8"
        )
        assert log_path == str(tmp_path / "test_runner.txt")
        assert "file logging works" in content
    finally:
        for handler in root.handlers:
            if handler not in original_handlers:
                handler.close()
        root.handlers = original_handlers
        root.setLevel(original_level)
