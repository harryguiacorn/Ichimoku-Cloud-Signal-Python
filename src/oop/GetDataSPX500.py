from oop.DataPandas import DataPandas

if __name__ == "__main__":
    dataP = DataPandas('data/spx500/', 'asset_list/SPX500.csv', True)
    dataP.main()
    