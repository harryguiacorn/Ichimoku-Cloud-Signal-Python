import pandas as pd
from src.mvc import Util
import logging

logger = logging.getLogger(__name__)


class Model(object):

    def __init__(
        self,
        __outputPathList: list = [],
        __outputMergePath: str = "",
        __list_direction_count_names: list = [],
        __list_score_names: list = [],
    ) -> None:
        self.outputPathList = __outputPathList
        self.outputMergePath = __outputMergePath
        self.list_direction_count_names = __list_direction_count_names
        self.list_score_names = __list_score_names

    def merge(self) -> pd.DataFrame:
        logger.info(
            "------------- Merging Multi Timeframe Cloud -------------"
        )

        list_pd = self.outputPathList

        logger.info("Check files for merging: ", list_pd)

        # check to see if files exist before parsing to Pandas
        list_pd_exist = iter([x for x in list_pd if Util.file_exists(x)])

        # print(list_pd_exist)
        combined_csv = pd.DataFrame()

        for x in list_pd_exist:
            logger.info("merge path::", x)

            df_csv_each = pd.read_csv(x)

            # if a particular csv is missing, move onto reading the next one.
            if df_csv_each.empty:
                continue

            # Drop the "Date" column
            if "Date" in df_csv_each.columns:
                df_csv_each = df_csv_each.drop(columns=["Date"])
            elif "Datetime" in df_csv_each.columns:
                df_csv_each = df_csv_each.drop(columns=["Datetime"])

            if combined_csv.empty:
                # parse the first df, usually the smallest time frame, e.g. 1h
                combined_csv = df_csv_each
            else:
                # Since "Close" values are different across different time frame.
                # The value from the lowest time frame is kept.
                # In this case, 1h "Close" is kept.
                # Drop the 'Close' column from all other time frames apart from 1h.
                df_csv_each = df_csv_each.drop(columns=["Close"])

                # Combine the two dataframes
                combined_csv = pd.merge(
                    combined_csv,
                    df_csv_each,
                    on=["Symbol", "Name"],  # , "Close"
                )
            logger.info("merge::df_csv1::\n", df_csv_each)
            logger.info("merge::combined_csv::\n", combined_csv, "\n")

        logger.info(
            "Multi Timeframe Cloud Signals Merged: ",
            self.outputMergePath,
            "\n\n",
        )
        logger.info("combined_csv size::", combined_csv.shape)
        logger.info("combined_csv::\n", combined_csv)

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
        if "Cloud Score Sum" in __df:
            __df.sort_values(
                by=["Cloud Score Sum"], ascending=False, inplace=True
            )
        logger.info("------ Cleaning columns ------")
        # filter through columns in df and output Score columns
        __filter_list_column = [
            x for x in __df.columns if x in self.list_score_names
        ]

        # add Symbol and Name columns in the front of the list
        __filter_list_column.insert(0, "Symbol")
        __filter_list_column.insert(1, "Name")
        __filter_list_column.insert(2, "Close")
        logger.info("Available columns: ", __filter_list_column)

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

        logger.info(
            f"Saved data to: {self.outputMergePath} {self.outputMergePath}.html\n"
        )
        logger.info(
            "----------- Cloud Score Multi Timeframe Final View -----------\n",
            __df,
        )
        return __df

    def create_score_column(
        self, df: pd.DataFrame, list_for_merge: list, name_sum="Sum"
    ):
        # check if a list of columns for Cloud direction or Count exists in df.
        if set(list_for_merge).issubset(df.columns):
            df[name_sum] = df[list_for_merge[0]] * df[list_for_merge[1]]
            logger.info(
                "Columns exist:",
                list_for_merge,
                # df[name_sum],
                # df[list_for_merge[0]],
                # df[list_for_merge[1]],
                # sep=", ",
                "\n",
            )
        else:
            logger.info("Columns missing:", list_for_merge, "\n")
            # df[name_sum] = 0
        return df

    def create_score_columns(self, df: pd.DataFrame):
        for i, __list in enumerate(self.list_direction_count_names):
            df = self.create_score_column(df, __list, self.list_score_names[i])
        logger.info(
            "\n-------------------- Cloud Score Multi Timeframe Raw --------------------\n",
            df,
            "\n\n",
        )

    def create_sum_column(self, df: pd.DataFrame):
        logger.info(
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
        df["Cloud Score Sum"] = __sum
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
            "output/DowJones30-cloud-D.csv",
            "output/DowJones30-cloud-W.csv",
            "output/DowJones30-cloud-M.csv",
        ],
        "output/DowJones30-cloud-Multi-Timeframe.csv",
    )

    __control = Control(__model, View())
    __control.main()
