import pandas as pd

from src.mvc import Util


class Model(object):
    def __init__(self, __outputPathList="", __outputMergePath="") -> None:
        self.outputPathList = __outputPathList
        self.outputMergePath = __outputMergePath
        pass

    def merge(self) -> pd.DataFrame:
        list_pd = self.outputPathList

        print("Check files for merging: ", list_pd)

        # check to see if files exist before parsing to Pandas
        list_pd_exist = iter([x for x in list_pd if Util.file_exists(x)])

        # print(list_pd_exist)
        combined_csv = pd.DataFrame()

        for x in list_pd_exist:
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

        print("Multi Timeframe Cloud Signals Merged: ", self.outputMergePath)

        print(combined_csv)

        return combined_csv

    def exportResult(self, list_result):
        df_result = pd.DataFrame(list_result, columns=self.getColumns())

        Util.createDataFolder(self.outputPath)
        df_result.to_csv(
            self.outputPath + self.assetClassName.replace(" ", "") + ".csv",
            index=False,
        )
        self.resultDataFrame = df_result
        return df_result

    def saveData(self, __df: pd.DataFrame) -> pd.DataFrame:
        __df.sort_values(by=["Cloud Score Sum"], ascending=False, inplace=True)

        __df.to_csv(f"{self.outputMergePath}", index=False)

        __df.to_html(f"{self.outputMergePath}.html", index=False)

        # print("__df:", __df)

        return __df

    def create_sum_column(self, df: pd.DataFrame):
        # Add the three columns and create a new column 'Sum_Columns'
        print("-------------------- Cloud Score --------------------")
        df["Cloud Score Sum"] = (
            df["1D Cloud Direction"] * df["1D Cloud Count"]
            + df["1W Cloud Direction"] * df["1W Cloud Count"]
            + df["1M Cloud Direction"] * df["1M Cloud Count"]
        )


class Control(object):
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view

    def main(self):
        df = self.merge()
        self.create_sum_column(df)
        self.saveData(df)

    def merge(self):
        return self.model.merge()

    def create_sum_column(self, df):
        self.model.create_sum_column(df)

    def saveData(self, df):
        self.model.saveData(df)


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
