
from DataKijunSignalAggregator import DataKijunSignalAggregator


if __name__ == "__main__":
    getDataKijunSignalAggregator = DataKijunSignalAggregator('data/dowjones30/', 'asset_list/DowJones30.csv', 'Dow Jones 30')
    getDataKijunSignalAggregator.main()
