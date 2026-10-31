import pytest

from cloud_signal.runners import main as main_runner


def test_main_runs_only_selected_markets_without_digest(monkeypatch):
    markets = [
        {"name": "Nas100", "enabled": True},
        {"name": "SPX500", "enabled": True},
        {"name": "HSI", "enabled": True},
    ]
    calls = []
    monkeypatch.setattr(main_runner, "get_market_configs", lambda: markets)
    monkeypatch.setattr(main_runner, "run_market", calls.append)
    monkeypatch.setattr(
        main_runner,
        "create_email_digest_controller",
        lambda: pytest.fail("single-market runs should not send a digest"),
    )

    main_runner.main(["spx500", "nas100"])

    assert calls == ["Nas100", "SPX500"]


def test_main_rejects_unknown_market_before_running(monkeypatch):
    calls = []
    monkeypatch.setattr(
        main_runner,
        "get_market_configs",
        lambda: [{"name": "Nas100", "enabled": True}],
    )
    monkeypatch.setattr(main_runner, "run_market", calls.append)

    with pytest.raises(ValueError, match="Unknown market"):
        main_runner.main(["unknown"])

    assert calls == []
