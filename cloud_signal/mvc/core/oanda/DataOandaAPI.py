import json
import logging
import os
import time
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

DEFAULT_API_URL = "https://api-fxpractice.oanda.com/v3"
REQUEST_TIMEOUT_SECONDS = 30


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
        url = f"{self._base_url()}/instruments/{instrument}/candles"
        return self._get_json(
            url,
            params={
                "count": count,
                "price": pricingComponent,
                "granularity": granularity,
            },
        )

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
