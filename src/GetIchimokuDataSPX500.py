from DataKijunSignal import GetBatchDataKijunSignal


if __name__ == "__main__":
    getBatchDataKijunSignal = GetBatchDataKijunSignal('data/spx500/', 'asset_list/SPX500.csv')
    getBatchDataKijunSignal.main()
