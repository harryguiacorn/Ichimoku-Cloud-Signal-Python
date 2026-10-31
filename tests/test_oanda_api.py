import pytest
import requests

from cloud_signal.mvc.core.oanda.DataOandaAPI import (
    DEFAULT_API_URL,
    REQUEST_TIMEOUT_SECONDS,
    DataOandaAPI,
)


class FakeResponse:
    def __init__(self, data=None, error=None):
        self.data = data
        self.error = error

    def raise_for_status(self):
        if self.error:
            raise self.error

    def json(self):
        return self.data


def test_oanda_candles_request_uses_named_parameters_and_credentials(
    monkeypatch,
):
    calls = []
    monkeypatch.setenv("OANDA_ACCESS_TOKEN", "test-token")
    monkeypatch.delenv("OANDA_API_URL", raising=False)

    def fake_get(url, **kwargs):
        calls.append((url, kwargs))
        return FakeResponse({"candles": []})

    monkeypatch.setattr(
        "cloud_signal.mvc.core.oanda.DataOandaAPI.requests.get", fake_get
    )

    result = DataOandaAPI().get_oanda_data(
        "EUR_USD", count=300, granularity="H1", pricingComponent="M"
    )

    assert result == {"candles": []}
    assert calls == [
        (
            f"{DEFAULT_API_URL}/instruments/EUR_USD/candles",
            {
                "headers": {"Authorization": "Bearer test-token"},
                "params": {
                    "count": 300,
                    "price": "M",
                    "granularity": "H1",
                },
                "timeout": REQUEST_TIMEOUT_SECONDS,
            },
        )
    ]


def test_oanda_account_instruments_uses_configured_account_id(monkeypatch):
    calls = []
    monkeypatch.setenv("OANDA_ACCESS_TOKEN", "test-token")
    monkeypatch.setenv("OANDA_ACCOUNT_ID", "test-account")

    def fake_get(url, **kwargs):
        calls.append((url, kwargs))
        return FakeResponse({"instruments": []})

    monkeypatch.setattr(
        "cloud_signal.mvc.core.oanda.DataOandaAPI.requests.get", fake_get
    )

    assert DataOandaAPI().get_instruments() == {"instruments": []}
    assert calls[0][0] == (
        f"{DEFAULT_API_URL}/accounts/test-account/instruments"
    )
    assert calls[0][1]["headers"] == {
        "Authorization": "Bearer test-token"
    }


def test_oanda_requires_credentials(monkeypatch):
    monkeypatch.delenv("OANDA_ACCESS_TOKEN", raising=False)

    with pytest.raises(RuntimeError, match="OANDA_ACCESS_TOKEN"):
        DataOandaAPI().get_oanda_data()


def test_oanda_http_errors_are_not_silently_discarded(monkeypatch):
    monkeypatch.setenv("OANDA_ACCESS_TOKEN", "test-token")
    monkeypatch.setattr(
        "cloud_signal.mvc.core.oanda.DataOandaAPI.requests.get",
        lambda *args, **kwargs: FakeResponse(
            error=requests.HTTPError("OANDA request failed")
        ),
    )

    with pytest.raises(requests.HTTPError, match="OANDA request failed"):
        DataOandaAPI().get_oanda_data()
