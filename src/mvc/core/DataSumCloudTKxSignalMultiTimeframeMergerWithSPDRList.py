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
            f"\n------------- Merging %s Symbols with %s Multi Timeframe Cloud and TKx Sum ------------- {self.html_title} {self.dataFilePathList}"
        )

        logger.debug(
            f"Check symbol file for merging: %s exist: %s {self.symbolPathList} {Util.file_exists(self.symbolPathList)}"
        )
        logger.debug(
            f"Check data file for merging: %s exist: %s {self.dataFilePathList} {Util.file_exists(self.dataFilePathList)}"
        )

        # Load the two CSV files into dataframes
        df_symbols = pd.read_csv(
            # self.symbolPathList
            self.symbolPathList,
            skiprows=1,
            usecols=["Symbol"],
        )  # CSV with stock symbols and names

        logger.debug("%s Symbols:\n %s", self.html_title, df_symbols)

        # return

        df_data = pd.read_csv(
            self.dataFilePathList
        )  # CSV with additional data

        # logger.debug("Data:\n%s", df_data)

        # Assuming the stock symbol is in a column named 'symbol' in both dataframes
        # Perform a merge to match rows based on the 'symbol' column
        df_merged = pd.merge(df_symbols, df_data, on="Symbol")

        logger.info("Multi Timeframe Cloud and TKx Signals Merged")

        logger.debug("%s\n%s", self.symbolPathList, df_merged)

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
        logger.debug(
            "File path without filename: %s", filepath_without_filename
        )
        logger.debug("File name with extension: %s", filename_with_extension)

        Util.create_folder(filepath_without_filename)

        if save_to_csv:
            __df.to_csv(
                f"{self.outputMergePath}",
                # columns=__filter_list_column,
                index=False,
            )
        if save_to_html:
            __df.to_html(f"{self.outputMergePath}.html", index=False)

        logger.info(f"Saved data to: {self.outputMergePath}.html")
        logger.info(
            f"----------- %s Cloud and TKx Sum Score Multi Timeframe Final View -----------\n%s {self.html_title} {__df}"
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
        logger.info(f"generate_html {csv_file_path}")
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
