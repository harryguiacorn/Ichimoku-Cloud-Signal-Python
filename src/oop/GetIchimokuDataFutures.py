from DataKijunSignal import GetBatchDataKijunSignal


if __name__ == "__main__":
    getBatchDataKijunSignal = GetBatchDataKijunSignal('data/futures/', 'asset_list/Futures.csv')
    getBatchDataKijunSignal.main()
