from oop.DataPandas import DataPandas


if __name__ == "__main__":
    dataP = DataPandas('data/futurescurrency/', 'asset_list/FuturesCurrency.csv', True)
    dataP.main()