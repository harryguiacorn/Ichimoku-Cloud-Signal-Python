import pandas as pd
from src.mvc import Util


class Model(object):
    def __init__(
        self,
        __outputPathList: str = "",
        __outputMergePath: str = "",
        __list_direction_count_names: list = [],
        __list_score_names: list = [],
    ) -> None:
        self.outputPathList = __outputPathList
        self.outputMergePath = __outputMergePath
        self.list_direction_count_names = __list_direction_count_names
        self.list_score_names = __list_score_names

    def merge(self) -> pd.DataFrame:
        print("------------- Merging Multi Timeframe TKx -------------")

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
            if "Date" in df_csv1.columns:
                df_csv1 = df_csv1.drop(columns=["Date"])
            elif "Datetime" in df_csv1.columns:
                df_csv1 = df_csv1.drop(columns=["Datetime"])

            if combined_csv.empty:
                combined_csv = df_csv1
            else:
                # Combine the two dataframes
                combined_csv = pd.merge(
                    combined_csv, df_csv1, on=["Symbol", "Name"]
                )

        print(
            "Multi Timeframe TKx Signals Merged: ",
            self.outputMergePath,
            end="\n\n",
        )

        # print(combined_csv)

        return combined_csv

    def exportResult(self, list_result):
        df_result = pd.DataFrame(list_result, columns=self.getColumns())

        Util.create_folder(self.outputPath)
        df_result.to_csv(
            self.outputPath + self.assetClassName.replace(" ", "") + ".csv",
            index=False,
        )
        self.resultDataFrame = df_result
        return df_result

    def saveData(
        self,
        __df: pd.DataFrame,
        save_to_csv: bool = True,
        save_to_html: bool = False,
    ) -> pd.DataFrame:
        if "TKx Score Sum" in __df:
            __df.sort_values(
                by=["TKx Score Sum"], ascending=False, inplace=True
            )
        print("------ Cleaning columns ------")
        # filter through columns in df and output Score columns
        __filter_list_column = [
            x for x in __df.columns if x in self.list_score_names
        ]

        # add Symbol and Name columns in the front of the list
        __filter_list_column.insert(0, "Symbol")
        __filter_list_column.insert(1, "Name")
        print("Available columns: ", __filter_list_column)

        # Filter columns based on the list of column names
        # print(__df)
        __df = __df[__filter_list_column]

        if save_to_csv:
            __df.to_csv(
                f"{self.outputMergePath}",
                columns=__filter_list_column,
                index=False,
            )

        if save_to_html:
            __df.to_html(f"{self.outputMergePath}.html", index=False)

        print(
            f"Saved data to: {self.outputMergePath} {self.outputMergePath}.html\n"
        )
        print(
            "----------- TKx Score Multi Timeframe Final View -----------\n",
            __df,
        )
        return __df

    def create_score_column(
        self, df: pd.DataFrame, list_for_merge: list, name_sum="Sum"
    ):
        # check if a list of columns for TKx direction or Count exists in df.
        if set(list_for_merge).issubset(df.columns):
            df[name_sum] = df[list_for_merge[0]] * df[list_for_merge[1]]
            print(
                "All specified columns exist.",
                # df[name_sum],
                # df[list_for_merge[0]],
                # df[list_for_merge[1]],
                # sep=", ",
                # end="\n",
            )
        else:
            print("At least one column is missing.", end="\n\n")
            # df[name_sum] = 0
        return df

    def create_score_columns(self, df: pd.DataFrame):
        for i, __list in enumerate(self.list_direction_count_names):
            df = self.create_score_column(df, __list, self.list_score_names[i])
        print(
            "-------------------- TKx Score Multi Timeframe Raw --------------------\n",
            df,
            end="\n\n",
        )

    def create_sum_column(self, df: pd.DataFrame):
        print(
            "create_sum_column self.list_score_names: ",
            self.list_score_names,
            "\ncreate_sum_column df.columns",
            df.columns,
        )
        __sum = 0
        for __name in self.list_score_names:
            if __name in df.columns:
                __sum += df[__name]
                # print(__name, __sum)
        df["TKx Score Sum"] = __sum
        return df


class Control(object):
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view

    def main(self):
        df = self.merge()
        self.create_score_columns(df)
        self.create_sum_column(df)

        self.saveData(df)

    def merge(self):
        return self.model.merge()

    def create_score_columns(self, df):
        self.model.create_score_columns(df)

    def create_sum_column(self, df):
        return self.model.create_sum_column(df)

    def saveData(self, df):
        self.model.saveData(df)


class View(object):
    def __init__(self) -> None:
        pass

    pass


if __name__ == "__main__":
    __model = Model(
        [
            "output/DowJones30-tkx-D.csv",
            "output/DowJones30-tkx-W.csv",
            "output/DowJones30-tkx-M.csv",
        ],
        "output/DowJones30-tkx-Multi-Timeframe.csv",
    )

    __control = Control(__model, View())
    __control.main()
