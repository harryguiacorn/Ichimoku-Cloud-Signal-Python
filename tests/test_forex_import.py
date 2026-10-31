import sys
from types import SimpleNamespace

import pytest

from cloud_signal.mvc.controllers.GetDataForex import get_instruments


def test_fxcm_credentials_are_required_only_when_integration_is_used(
    monkeypatch,
):
    monkeypatch.delenv("FXCM_ACCESS_TOKEN", raising=False)

    with pytest.raises(RuntimeError, match="FXCM_ACCESS_TOKEN"):
        get_instruments()


def test_fxcm_connection_is_closed_after_fetch(monkeypatch):
    state = {"closed": False}
    monkeypatch.setenv("FXCM_ACCESS_TOKEN", "test-token")

    class FakeConnection:
        def get_instruments(self):
            return ["EUR/USD", "USD/JPY"]

        def close(self):
            state["closed"] = True

    fake_fxcmpy = SimpleNamespace(
        fxcmpy=lambda **kwargs: (
            state.update(connection_kwargs=kwargs) or FakeConnection()
        )
    )
    monkeypatch.setitem(sys.modules, "fxcmpy", fake_fxcmpy)

    assert get_instruments() == ["EUR/USD", "USD/JPY"]
    assert state["closed"]
    assert state["connection_kwargs"] == {
        "access_token": "test-token",
        "log_level": "error",
    }
