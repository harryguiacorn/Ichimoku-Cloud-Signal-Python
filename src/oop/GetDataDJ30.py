from oop.DataPandas import DataPandas

if __name__ == "__main__":
    dataP = DataPandas('data/dowjones30/', 'asset_list/DowJones30.csv', True)
    dataP.main()