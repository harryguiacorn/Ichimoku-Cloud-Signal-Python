import json
import logging
import os
import time
from datetime import datetime, timezone
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

from cloud_signal.cache import get_cached_json, save_cached_json

logger = logging.getLogger(__name__)

DEFAULT_API_URL = "https://api-fxpractice.oanda.com/v3"
REQUEST_TIMEOUT_SECONDS = 30
RAW_CACHE_TTL_SECONDS = 900
RAW_CACHE_VERSION = "oanda-v1"


class DataOandaAPI:
    def __init__(self):
        self.data = None

    @staticmethod
    def _credentials() -> tuple[str, str | None]:
        load_dotenv()
        token = os.getenv("OANDA_ACCESS_TOKEN")
        if not token:
            raise RuntimeError(
                "OANDA_ACCESS_TOKEN must be set to use the OANDA API"
            )
        return token, os.getenv("OANDA_ACCOUNT_ID")

    @staticmethod
    def _base_url() -> str:
        load_dotenv()
        return os.getenv("OANDA_API_URL", DEFAULT_API_URL).rstrip("/")

    def _get_json(
        self, url: str, params: dict[str, Any] | None = None
    ) -> Any:
        token, _ = self._credentials()
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {token}"},
            params=params,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json()

    def get_oanda_data(
        self,
        instrument="EUR_USD",
        count=60,
        granularity="H4",
        pricingComponent="M",
    ) -> Any:
        count = int(count)
        identity = json.dumps(
            {
                "base_url": self._base_url(),
                "instrument": instrument,
                "count": count,
                "granularity": granularity,
                "price": pricingComponent,
            },
            sort_keys=True,
        )
        cached = get_cached_json(
            "oanda_raw",
            identity,
            RAW_CACHE_VERSION,
            RAW_CACHE_TTL_SECONDS,
            allow_stale=True,
        )
        if cached is not None and cached[2]:
            return cached[0]

        url = f"{self._base_url()}/instruments/{instrument}/candles"
        params: dict[str, Any] = {
            "count": count,
            "price": pricingComponent,
            "granularity": granularity,
        }
        stale = cached[0] if cached is not None else None
        if isinstance(stale, dict):
            candles = stale.get("candles")
            if isinstance(candles, list) and candles:
                latest_time = candles[-1].get("time")
                if isinstance(latest_time, str):
                    try:
                        latest_datetime = datetime.fromisoformat(
                            latest_time.replace("Z", "+00:00")
                        )
                        max_gap = (
                            self._granularity_seconds(granularity) * count
                        )
                        gap = (
                            datetime.now(timezone.utc) - latest_datetime
                        ).total_seconds()
                    except (TypeError, ValueError):
                        logger.warning(
                            "Ignoring invalid OANDA candle timestamp %s",
                            latest_time,
                        )
                    else:
                        if gap <= max_gap:
                            params["from"] = latest_time

        data = self._get_json(
            url,
            params=params,
        )
        if stale is not None:
            data = self._merge_candles(stale, data, count)
        save_cached_json(
            "oanda_raw", identity, data, RAW_CACHE_VERSION
        )
        return data

    @staticmethod
    def _granularity_seconds(granularity: str) -> int:
        units = {
            "S": 1,
            "M": 30 * 24 * 60 * 60,
            "H": 60 * 60,
            "D": 24 * 60 * 60,
            "W": 7 * 24 * 60 * 60,
        }
        unit = granularity[0]
        multiplier = int(granularity[1:] or "1")
        return multiplier * units.get(unit, 24 * 60 * 60)

    @staticmethod
    def _merge_candles(
        cached: Any, refreshed: Any, count: int
    ) -> Any:
        if not isinstance(cached, dict) or not isinstance(refreshed, dict):
            return refreshed
        old_candles = cached.get("candles")
        new_candles = refreshed.get("candles")
        if not isinstance(old_candles, list) or not isinstance(
            new_candles, list
        ):
            return refreshed
        by_time = {
            candle["time"]: candle
            for candle in old_candles + new_candles
            if isinstance(candle, dict) and isinstance(candle.get("time"), str)
        }
        merged = sorted(by_time.values(), key=lambda candle: candle["time"])
        if isinstance(count, int) and count > 0:
            merged = merged[-count:]
        result = dict(refreshed)
        result["candles"] = merged
        return result

    def get_instruments(self, account_id: str | None = None) -> Any:
        _, configured_account_id = self._credentials()
        account_id = account_id or configured_account_id
        if not account_id:
            raise RuntimeError(
                "OANDA_ACCOUNT_ID must be set to fetch account instruments"
            )
        url = f"{self._base_url()}/accounts/{account_id}/instruments"
        return self._get_json(url)

    def save_json(self, filePath="data.json", data: Any = None):
        with open(filePath, "w") as f:
            json.dump(data, f)

    def poll_api(self):
        while True:
            self.data = self.get_oanda_data()
            self.save_json()
            logger.debug("Polled data: %s", self.data)
            time.sleep(5)

    def json_to_csv(
        self, data: dict[str, Any], filePath="data.csv"
    ) -> pd.DataFrame:
        candles = data["candles"]
        df = pd.DataFrame([candle["mid"] for candle in candles])
        df["Datetime"] = pd.to_datetime(
            [candle["time"] for candle in candles], utc=True
        )
        df.columns = ["Open", "High", "Low", "Close", "Datetime"]
        df = df[["Datetime", "Open", "High", "Low", "Close"]]
        df.to_csv(filePath, index=False)
        return df


if __name__ == "__main__":
    api = DataOandaAPI()
    data = api.get_oanda_data()
    instruments = api.get_instruments()
    api.save_json("data/oanda/instruments.json", instruments)
    logger.info("Instruments: %s", instruments)
