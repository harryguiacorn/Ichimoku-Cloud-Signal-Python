import pandas as pd
import Util


class Model(object):
    def __init__(self, __outputPathList="", __outputMergePath="") -> None:
        self.outputPathList = __outputPathList
        self.outputMergePath = __outputMergePath
        pass

    def merge(self):
        list_pd = self.outputPathList

        list_pd_read = iter([x for x in list_pd if Util.file_exists(x)])

        # print(list_pd_read)
        combined_csv = pd.DataFrame()

        for x in list_pd_read:
            # print("path", x)
            df_csv1 = pd.read_csv(x)
            # Drop the "Date" column
            df_csv1 = df_csv1.drop(columns=["Date"])
            if combined_csv.empty:
                combined_csv = df_csv1
            else:
                # Combine the two dataframes
                combined_csv = pd.merge(
                    combined_csv, df_csv1, on=["Symbol", "Name"]
                )
        if Util.file_exists(self.outputMergePath):
            combined_csv.to_csv(f"{self.outputMergePath}")
        # print(combined_csv)


class Control(object):
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view

    def main(self):
        self.merge()

    def merge(self):
        self.model.merge()


class View(object):
    def __init__(self) -> None:
        pass

    pass


if __name__ == "__main__":
    __model = Model(
        [
            "output/DowJones30-cloud-D.csv",
            "output/DowJones30-cloud-W.csv",
            "output/DowJones30-cloud-M.csv",
        ],
        "output/DowJones30-cloud-Multi-Timeframe.csv",
    )

    __control = Control(__model, View())
    __control.main()
