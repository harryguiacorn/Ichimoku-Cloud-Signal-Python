import pandas as pd
import requests
import json
from src.mvc import Util


# Define the Model class
class Model:
    def __init__(
        self,
        base_url: str = "https://api-pub.bitfinex.com/v2/",
        time_frame: str = "1h",
        instrument: str = "tBTCUSD",
    ):
        # Initialize an empty list to store the data
        self.data = []

        # Define the base url for the Bitfinex API
        self.base_url = base_url

        # Define the time frame and the instrument for the candles
        self.time_frame = time_frame
        self.instrument = instrument

        # Define the endpoint for the BTC USD hourly candles
        self.endpoint: str = f"candles/trade:{time_frame}:{instrument}/hist"

        # Define the parameters for the request
        # limit: the number of candles to return, max 10000
        # end: the end timestamp of the query range
        # sort: the sorting direction of the results, 1 for ascending, -1 for descending
        self.params = {"limit": 10000, "end": None, "sort": -1}

        self.response = None

        # Initialize an empty DataFrame to store the data
        self.df = pd.DataFrame()

    def get_data(self):
        # Return the data list
        return self.data

    def fetch_data(self):
        # Make a GET request to the API with the parameters
        self.response = requests.get(
            self.base_url + self.endpoint, params=self.params
        )
        # Check if the response status code is 200 (OK)
        if self.response.status_code == 200:
            # Convert the response JSON to a list of lists
            candles = self.response.json()
            # Extend the data list with the candles
            self.data.extend(candles)
            # Update the end parameter to the timestamp of the last candle
            self.params["end"] = candles[-1][0]
            # Return True if the data is fetched successfully
            return True
        else:
            # Return False if the data is not fetched successfully
            return False

    def save_json(self, filePath="data.json"):
        # initializing Parameters
        # Util.create_folder(filePath)

        print("----------filePath---------", filePath)
        print("---------- get data ", self.get_data())
        print("---------- df ", self.df)

        # Save data to a JSON file
        with open(filePath, "w") as f:
            json.dump(self.get_data(), f)

    def save_csv(self, filePath="data.csv"):
        self.df.to_csv(filePath)

    def set_data(self, data):
        # Convert the data list to a pandas DataFrame
        self.df = pd.DataFrame(
            data,
            columns=["Timestamp", "Open", "Close", "High", "Low", "Volume"],
        )
        # Convert the timestamp column to datetime format
        self.df["Datetime"] = pd.to_datetime(self.df["Timestamp"], unit="ms")
        self.df = self.df.drop("Timestamp", axis=1)
        # Set the timestamp column as the index
        self.df = self.df.set_index("Datetime")


# Define the View class
class View:
    def __init__(self):
        pass

    def show_data(self, df):
        # Print the DataFrame
        print("--------- show_data ---------", df)


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
            self.model.set_data(self.model.get_data())
            # Show the data from the view
            self.view.show_data(self.model.df)
        else:
            # Print the error message and break the loop
            print(f"Error: {self.model.response.status_code}")

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
    controller.save_json(filePath="data/bitfinex/")
    controller.save_csv(filePath="data/bitfinex/")
