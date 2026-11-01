import json
from datetime import datetime, timedelta, timezone

import pandas as pd
import pytest

from cloud_signal.cache import save_cached_json
from cloud_signal.mvc.core.bitfinex.DataBitfinexAPI import (
    RAW_CACHE_VERSION as BITFINEX_CACHE_VERSION,
    Model as BitfinexModel,
)
from cloud_signal.mvc.core.kraken.DataKrakenAPI import (
    RAW_CACHE_VERSION as KRAKEN_CACHE_VERSION,
    Model as KrakenModel,
)
from cloud_signal.mvc.core.oanda.DataOandaAPI import (
    RAW_CACHE_VERSION as OANDA_CACHE_VERSION,
    DataOandaAPI,
)


@pytest.fixture(autouse=True)
def isolate_shared_cache(tmp_path, monkeypatch):
    monkeypatch.setenv(
        "CLOUD_SIGNAL_CACHE_DIR", str(tmp_path / "shared-cache")
    )


class FakeResponse:
    def __init__(self, data, status_code=200):
        self.data = data
        self.status_code = status_code

    def json(self):
        return self.data

    def raise_for_status(self):
        return None


def test_oanda_uses_fresh_cache_without_another_request(monkeypatch):
    monkeypatch.setenv("OANDA_ACCESS_TOKEN", "test-token")
    calls = []

    def fake_get(url, **kwargs):
        calls.append((url, kwargs))
        return FakeResponse({"candles": [{"time": "2026-10-31T00:00:00Z"}]})

    monkeypatch.setattr(
        "cloud_signal.mvc.core.oanda.DataOandaAPI.requests.get", fake_get
    )
    api = DataOandaAPI()

    first = api.get_oanda_data("EUR_USD", 3, "H1")
    second = api.get_oanda_data("EUR_USD", 3, "H1")

    assert first == second
    assert len(calls) == 1


def test_oanda_refreshes_from_cached_latest_candle(monkeypatch):
    monkeypatch.setenv("OANDA_ACCESS_TOKEN", "test-token")
    api = DataOandaAPI()
    latest = datetime.now(timezone.utc) - timedelta(hours=2)
    latest_text = latest.isoformat().replace("+00:00", "Z")
    cached = {
        "candles": [
            {"time": latest_text, "mid": {"c": "1"}},
            {
                "time": (latest + timedelta(hours=1))
                .isoformat()
                .replace("+00:00", "Z"),
                "mid": {"c": "2"},
            },
        ]
    }
    identity = json.dumps(
        {
            "base_url": api._base_url(),
            "instrument": "EUR_USD",
            "count": 3,
            "granularity": "H1",
            "price": "M",
        },
        sort_keys=True,
    )
    save_cached_json(
        "oanda_raw",
        identity,
        cached,
        OANDA_CACHE_VERSION,
        fetched_at=datetime.now(timezone.utc) - timedelta(hours=1),
    )
    calls = []

    def fake_get(url, **kwargs):
        calls.append(kwargs["params"])
        return FakeResponse(
            {
                "candles": [
                    {"time": latest_text, "mid": {"c": "1.5"}},
                    {
                        "time": (latest + timedelta(hours=2))
                        .isoformat()
                        .replace("+00:00", "Z"),
                        "mid": {"c": "3"},
                    },
                ]
            }
        )

    monkeypatch.setattr(
        "cloud_signal.mvc.core.oanda.DataOandaAPI.requests.get", fake_get
    )

    result = api.get_oanda_data("EUR_USD", 3, "H1")

    assert calls[0]["from"] == cached["candles"][-1]["time"]
    assert [candle["mid"]["c"] for candle in result["candles"]] == [
        "1.5",
        "2",
        "3",
    ]


def test_kraken_uses_fresh_cache_without_another_request(monkeypatch):
    calls = []
    data = {"result": {"BTC/USD": [[1, "1", "2", "0", "1", "1", "1", 1]]}}
    monkeypatch.setattr(
        "cloud_signal.mvc.core.kraken.DataKrakenAPI.requests.request",
        lambda *args, **kwargs: calls.append(args) or FakeResponse(data),
    )

    assert KrakenModel().fetch_data()
    assert KrakenModel().fetch_data()

    assert len(calls) == 1


def test_kraken_refreshes_from_cached_latest_timestamp(monkeypatch):
    model = KrakenModel()
    latest = int(datetime.now(timezone.utc).timestamp()) - 60
    identity = json.dumps(
        {
            "base_url": model.base_url,
            "instrument": model.instrument,
            "time_frame": model.time_frame,
            "lookback": model.lookbackPeriod,
        },
        sort_keys=True,
    )
    cached_rows = [[latest, "1", "2", "0", "1", "1", "1", 1]]
    save_cached_json(
        "kraken_raw",
        identity,
        cached_rows,
        KRAKEN_CACHE_VERSION,
        fetched_at=datetime.now(timezone.utc) - timedelta(minutes=10),
    )
    calls = []
    response = {
        "result": {
            "BTC/USD": [
                [latest, "1", "2", "0", "1", "1", "1", 1],
                [latest + 60, "1", "2", "0", "2", "1", "1", 1],
            ]
        }
    }
    monkeypatch.setattr(
        "cloud_signal.mvc.core.kraken.DataKrakenAPI.requests.request",
        lambda method, url, **kwargs: (
            calls.append(url) or FakeResponse(response)
        ),
    )

    assert model.fetch_data()

    assert f"since={latest - 1}" in calls[0]
    assert [row[0] for row in model.data] == [latest, latest + 60]


def test_bitfinex_uses_fresh_cache_without_another_request(monkeypatch):
    calls = []
    monkeypatch.setattr(
        "cloud_signal.mvc.core.bitfinex.DataBitfinexAPI.requests.get",
        lambda *args, **kwargs: calls.append(args)
        or FakeResponse([[1000, "1", "2", "0", "1", "1"]]),
    )

    assert BitfinexModel().fetch_data()
    assert BitfinexModel().fetch_data()

    assert len(calls) == 1


def test_bitfinex_refreshes_from_cached_latest_timestamp(monkeypatch):
    model = BitfinexModel(lookbackPeriod=10)
    identity = json.dumps(
        {
            "base_url": model.base_url,
            "instrument": model.instrument,
            "time_frame": model.time_frame,
            "lookback": model.lookbackPeriod,
        },
        sort_keys=True,
    )
    latest = int(pd.Timestamp.now(tz="UTC").timestamp() * 1000)
    save_cached_json(
        "bitfinex_raw",
        identity,
        [[latest, "1", "2", "0", "1", "1"]],
        BITFINEX_CACHE_VERSION,
        fetched_at=datetime.now(timezone.utc) - timedelta(minutes=10),
    )
    calls = []
    monkeypatch.setattr(
        "cloud_signal.mvc.core.bitfinex.DataBitfinexAPI.requests.get",
        lambda url, params: (
            calls.append(params)
            or FakeResponse([[latest + 3600000, "2", "3", "1", "2", "1"]])
        ),
    )

    assert model.fetch_data()

    assert calls[0]["start"] == latest - 3600000
    assert [row[0] for row in model.data] == [latest + 3600000, latest]
