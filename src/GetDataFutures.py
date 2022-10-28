from DataPandas import DataPandas

if __name__ == "__main__":
    dataP = DataPandas('data/futures/', 'asset_list/Futures.csv', True)
    dataP.main()
    