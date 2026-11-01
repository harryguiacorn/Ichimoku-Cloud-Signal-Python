import pandas as pd
import requests
import json
import time
from cloud_signal.cache import get_cached_json, save_cached_json
import logging

logger = logging.getLogger(__name__)

RAW_CACHE_TTL_SECONDS = 300
RAW_CACHE_VERSION = "kraken-v1"


# Define the Model class
class Model:

    def __init__(
        self,
        base_url: str = "https://api.kraken.com/0/public/OHLC/",
        time_frame: str = "1440",
        instrument: str = "BTC/USD",
        lookbackPeriod: int = 720,
    ):
        # Initialize an empty list to store the data
        self.data = []

        # Define the base url for the Kraken API
        self.base_url = base_url

        # Define the time frame and the instrument for the candles
        self.time_frame = time_frame
        self.instrument = instrument
        self.lookbackPeriod = lookbackPeriod

        # Define the endpoint for the BTC USD hourly candles
        self.endpoint: str = (
            f"?pair={instrument}&interval={time_frame}&since={lookbackPeriod}"
        )

        # # Define the parameters for the request
        # # limit: the number of candles to return, max 10000
        # # end: the end timestamp of the query range
        # # sort: the sorting direction of the results, 1 for ascending, -1 for descending
        # self.params = {"limit": self.lookbackPeriod, "end": None, "sort": -1}

        self.response = None

        # Initialize an empty DataFrame to store the data
        self.df = pd.DataFrame()

    def get_data_list(self) -> list:
        # Return the data list
        # print("------- get_data_list --------", self.data)
        return self.data

    def get_data(self) -> pd.DataFrame:
        # Return the data list
        # print("------- get_data --------", self.data)
        return self.df

    def fetch_data(self):
        identity = json.dumps(
            {
                "base_url": self.base_url,
                "instrument": self.instrument,
                "time_frame": self.time_frame,
                "lookback": self.lookbackPeriod,
            },
            sort_keys=True,
        )
        cached = get_cached_json(
            "kraken_raw",
            identity,
            RAW_CACHE_VERSION,
            RAW_CACHE_TTL_SECONDS,
            allow_stale=True,
        )
        if cached is not None and cached[2]:
            self.data = cached[0]
            return True

        since = self.lookbackPeriod
        merge_cached_rows = False
        if cached is not None and isinstance(cached[0], list) and cached[0]:
            try:
                latest_timestamp = int(float(cached[0][-1][0]))
                interval_seconds = int(self.time_frame) * 60
                max_gap_seconds = interval_seconds * 720
                gap_seconds = int(time.time()) - latest_timestamp
                if gap_seconds <= max_gap_seconds:
                    since = max(0, latest_timestamp - 1)
                    merge_cached_rows = True
                else:
                    since = max(
                        0, int(time.time()) - max_gap_seconds
                    )
            except (IndexError, TypeError, ValueError):
                logger.warning(
                    "Ignoring malformed Kraken cache for %s", self.instrument
                )

        url = (
            self.base_url
            + f"?pair={self.instrument}&interval={self.time_frame}"
            + f"&since={since}"
        )

        logger.info(
            "fetch_data: instrument=%s time_frame=%s lookback=%s url=%s",
            self.instrument,
            self.time_frame,
            self.lookbackPeriod,
            url,
        )
        payload = {}
        headers = {"Accept": "application/json"}

        self.response = requests.request(
            "GET", url, headers=headers, data=payload
        )

        # Check if the response status code is 200 (OK)
        if self.response.status_code == 200:
            # Convert the response JSON to a list of lists
            candles = self.response.json()

            # Extend the data list with the candles
            # self.data.extend(candles)
            refreshed = candles["result"][self.instrument]
            if merge_cached_rows and cached is not None:
                by_timestamp = {
                    row[0]: row
                    for row in cached[0] + refreshed
                    if isinstance(row, list) and row
                }
                refreshed = sorted(
                    by_timestamp.values(), key=lambda row: float(row[0])
                )[-720:]
            self.data = refreshed
            save_cached_json(
                "kraken_raw",
                identity,
                self.data,
                RAW_CACHE_VERSION,
            )

            # # Update the end parameter to the timestamp of the last candle
            # self.params["end"] = candles[-1][0]

            # print(
            #     "self.response.status_code",
            #     self.response.status_code,
            #     "---- fetch data ----",
            #     self.data,
            # )

            # Return True if the data is fetched successfully
            return True
        else:
            # Return False if the data is not fetched successfully
            logger.warning(
                "fetch_data failed with status_code=%s",
                self.response.status_code,
            )
            return False

    def save_json(self, filePath="data.json"):
        # initializing Parameters
        # Util.create_folder(filePath)

        # print(f"---------- filePath: {filePath} ---------")
        # print("---------- get data ", self.get_data())
        # print("---------- df ", self.df)

        # Save data to a JSON file
        with open(filePath, "w") as f:
            json.dump(self.get_data(), f)
        logger.info(f"Saved json to {filePath}")

    def save_csv(self, filePath="data.csv"):
        # print(
        #     "save_csv path:",
        #     filePath,
        #     "\nself.df\n",
        #     self.df,
        # )
        self.df.to_csv(filePath)
        logger.info(f"Saved csv to {filePath}")

    def set_data(self, data):
        # Convert the data list to a pandas DataFrame
        self.df = pd.DataFrame(
            data,
            columns=[
                "Datetime",
                "Open",
                "High",
                "Low",
                "Close",
                "vwap",
                "Volume",
                "count",
            ],
        )
        # print("----- set_data -----:", data, self.df)
        # Kraken data is in an ascending order so no need to flip them
        # self.df = self.df.iloc[::-1]

        # # Convert the timestamp column to datetime format
        # self.df["Datetime"] = pd.to_datetime(self.df["Timestamp"], unit="ms")

        # Convert the 'time' column from UNIX timestamp to readable datetime format
        self.df["Datetime"] = pd.to_datetime(self.df["Datetime"], unit="s")

        # self.df = self.df.drop("Timestamp", axis=1)
        # Set the timestamp column as the index
        self.df = self.df.set_index("Datetime")
        logger.debug("Set dataframe index and shape: %s", self.df.shape)


# Define the View class
class View:
    def __init__(self):
        pass

    def show_data(self, df: pd.DataFrame):
        # Log the DataFrame head
        logger.debug("kraken show_data head:\n%s", df.head(2).to_string())


# Define the Controller class
class Controller:
    def __init__(self, model, view):
        # Initialize the model and the view objects
        self.model = model
        self.view = view

    def run(self):
        # Fetch the data from the model
        result = self.model.fetch_data()
        # Check if the result is True
        if result:
            # Set the data to the view
            self.model.set_data(self.model.get_data_list())
            # print(
            #     "self.model.set_data(self.model.get_data_list())",
            #     self.model.get_data_list(),
            # )
            # Show the data from the view
            self.view.show_data(self.model.df)
        else:
            # Log the error status code
            logger.error(
                "Error fetching data: status_code=%s",
                self.model.response.status_code,
            )

    def save_json(self, filePath="data.json"):
        self.model.save_json(filePath)

    def save_csv(self, filePath="data.csv"):
        self.model.save_csv(filePath)


if __name__ == "__main__":
    # Create an instance of the Model class
    model = Model()
    # Create an instance of the View class
    view = View()
    # Create an instance of the Controller class
    controller = Controller(model, view)
    # Run the controller
    controller.run()
    controller.save_json(filePath="data/kraken/")
    controller.save_csv(filePath="data/kraken/")
