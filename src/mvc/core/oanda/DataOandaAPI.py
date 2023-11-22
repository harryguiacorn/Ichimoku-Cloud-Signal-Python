import requests
import time
import json
import pandas as pd
from src.mvc import Util


class DataOandaAPI:
    def __init__(self):
        self.data = None

    def get_oanda_data(
        self,
        instrument="EUR_USD",
        count=60,
        granularity="H4",
        pricingComponent="M",
    ) -> json:
        url = "https://api-fxpractice.oanda.com/v3/instruments/USD_JPY/candles?count=10&price=A&from=2016-01-01T00%3A00%3A00.000000000Z&granularity=D"
        url = (
            "https://api-fxpractice.oanda.com/v3/accounts/101-004-21686905-001"
        )
        url = "https://api-fxpractice.oanda.com/v3/accounts/101-004-21686905-001/instruments"
        url = f"https://api-fxpractice.oanda.com/v3/instruments/{instrument}/candles?{count}&price={pricingComponent}&granularity={granularity}"
        headers = {
            "Authorization": "Bearer 3b627083d16f29d1e31994bffbe3f229-5b8b7091a8fe4eeaac8223daebd30a94"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def save_json(self, filePath="data.json", data: json = None):
        # Save data to a JSON file
        with open(filePath, "w") as f:
            json.dump(data, f)

    def poll_api(self):
        while True:
            self.data = self.get_oanda_data()
            self.save_json()
            print(self.data)
            time.sleep(5)  # Poll every 5 seconds

    def json_to_csv(self, data: json, filePath="data.csv") -> pd.DataFrame:
        # Assuming json_string is your JSON data
        # print(data)
        json_data = data.copy()

        # Extracting the 'candles' data
        candles = json_data["candles"]

        # Convert the candle data to a DataFrame
        df = pd.DataFrame(
            [candle["mid"] for candle in candles],
            index=pd.to_datetime(
                [candle["time"] for candle in candles], utc=True
            ),
        )

        # Rename the columns
        df.columns = ["Open", "High", "Low", "Close"]

        # Add a column for 'Datetime' and set the index values
        df.insert(0, "Datetime", df.index)

        # Export the DataFrame to a CSV file
        df.to_csv(filePath, index=False)

        # print("json_to_csv:", df)
        return df


if __name__ == "__main__":
    api = DataOandaAPI()
    # poll_api()
    data = api.get_oanda_data()
    # data = get_oanda_data()
    api.save_json(data=data, filePath="data/oanda/")
    print(data)

    api.json_to_csv(data)
