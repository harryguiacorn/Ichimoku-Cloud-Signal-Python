import pandas as pd
from src.mvc import Util
from src.mvc.html_creator import TableGenerator
import logging

logger = logging.getLogger(__name__)


class Model(object):

    def __init__(
        self,
        __symbolPathList: str = "",
        __dataFilePathList: str = "",
        __outputMergePath: str = "",
        __html_title: str = "Cloud Scan",
    ) -> None:
        self.symbolPathList = __symbolPathList
        self.dataFilePathList = __dataFilePathList
        self.outputMergePath = __outputMergePath
        self.html_title = __html_title

    def merge(self) -> pd.DataFrame:
        logger.info(
            f"\n------------- Merging {self.html_title} Symbols with {self.dataFilePathList} Multi Timeframe Cloud and TKx Sum -------------"
        )

        logger.info(
            f"Check symbol file for merging: {self.symbolPathList} exist:{Util.file_exists(self.symbolPathList)}"
        )
        logger.info(
            f"Check data file for merging: {self.dataFilePathList} exist: {Util.file_exists(self.dataFilePathList)}"
        )

        # Load the two CSV files into dataframes
        df_symbols = pd.read_csv(
            self.symbolPathList,
            usecols=["symbol"],
        )  # CSV with stock symbols and names

        logger.info(f"{self.html_title} Symbols:\n {df_symbols}")

        # return

        df_data = pd.read_csv(
            self.dataFilePathList
        )  # CSV with additional data

        logger.info(f"Data:\n{df_data}")

        # # Assuming the stock symbol is in a column named 'symbol' in both dataframes
        # # Perform a merge to match rows based on the 'symbol' column
        # df_merged = pd.merge(df_symbols, df_data, on="Symbol")

        # Ensure column names match in both dataframes for merging
        # Convert both to lowercase (or uppercase) to standardize
        df_symbols.rename(columns={"symbol": "Symbol"}, inplace=True)
        df_data.rename(columns={"symbol": "Symbol"}, inplace=True)

        # Merge the dataframes on the 'Symbol' column
        df_merged = pd.merge(df_symbols, df_data, on="Symbol", how="inner")

        logger.info(f"Multi Timeframe Cloud and TKx Signals Merged\n\n")

        logger.info(f"{self.symbolPathList}\n{df_merged}")

        return df_merged

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
        # if self.list_score_names[0] in __df:
        #     __df.sort_values(
        #         by=[self.list_score_names[0]],
        #         ascending=False,
        #         inplace=True,
        #     )
        # # print("------ Cleaning columns ------")

        (
            filepath_without_filename,
            filename_with_extension,
        ) = Util.split_filepath(self.outputMergePath)
        logger.info(f"File path without filename:{filepath_without_filename}")
        logger.info(f"File name with extension:{filename_with_extension}")

        Util.create_folder(filepath_without_filename)

        if save_to_csv:
            __df.to_csv(
                f"{self.outputMergePath}",
                # columns=__filter_list_column,
                index=False,
            )
        if save_to_html:
            __df.to_html(f"{self.outputMergePath}.html", index=False)

        logger.info(
            f"Saved data to: {self.outputMergePath} {self.outputMergePath}.html\n"
        )
        logger.info(
            f"----------- {self.html_title} Cloud and TKx Sum Score Multi Timeframe Final View -----------\n {__df}"
        )
        return __df


class Control(object):
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view

    def main(self):
        df = self.merge()
        # self.create_sum_column(df)

        self.saveData(df)
        self.generate_html()

    def merge(self):
        return self.model.merge()

    def create_sum_column(self, df):
        return self.model.create_sum_column(df)

    def saveData(self, df):
        self.model.saveData(df)

    def generate_html(self):
        self.view.generate_html(
            self.model.outputMergePath, self.model.html_title
        )


class View(object):
    def __init__(self) -> None:
        pass

    def generate_html(self, csv_file_path: str, html_title: str):
        table_generator = TableGenerator(csv_file_path)
        html_table = table_generator.generate_html_table(html_title)
        logger.info(f"generate_html{csv_file_path}")
        table_generator.save_html_table(html_table, csv_file_path + ".html")
        # table_generator.display_html_table_jupyter(csv_file_path + ".html")


if __name__ == "__main__":
    _model = Model(
        "output/sum/Oanda-sum-cloud-tkx-merged.csv",
        "output/sum/Oanda-sum-cloud-tkx-merged.csv",
        "output/sum/Oanda-sum-cloud-tkx-merged.csv",
        "TEST",
    )
    _control = Control(_model, View())
    _control.main()
