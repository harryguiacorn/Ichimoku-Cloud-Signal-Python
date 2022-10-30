
from DataKijunSignalAggregator import DataKijunSignalAggregator


if __name__ == "__main__":
    getDataKijunSignalAggregator = DataKijunSignalAggregator('data/futurescurrency-d/', 'asset_list/FuturesCurrency.csv', 'Futures')
    getDataKijunSignalAggregator.main()
