
from DataKijunSignalAggregator import DataKijunSignalAggregator


if __name__ == "__main__":
    getDataKijunSignalAggregator = DataKijunSignalAggregator('data/spx500/', 'asset_list/SPX500.csv', 'SPX 500')
    getDataKijunSignalAggregator.main()
