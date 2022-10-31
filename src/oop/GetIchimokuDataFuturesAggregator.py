
from DataKijunSignalAggregator import DataKijunSignalAggregator


if __name__ == "__main__":
    getDataKijunSignalAggregator = DataKijunSignalAggregator('data/futures/', 'asset_list/Futures.csv', 'Futures')
    getDataKijunSignalAggregator.main()
