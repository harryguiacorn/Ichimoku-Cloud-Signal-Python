from DataKijunSignal import GetBatchDataKijunSignal


if __name__ == "__main__":
    getBatchDataKijunSignal = GetBatchDataKijunSignal('data/dowjones30/', 'asset_list/DowJones30.csv')
    getBatchDataKijunSignal.main()
