from genericpath import isdir
import os
import pandas as pd
from typing import Dict
from src.mvc import Util


class Model(object):
    def __init__(
        self,
        __csvPath="data/",
        __assetListPath="",
        __outputPath="",
        __assetClassName="",
        __csvColumnPrefix="",
        __use_datetime_format=False,
    ):
        self.csvPath = __csvPath
        self.assetListPath = __assetListPath
        self.assetClassName = __assetClassName
        self.outputPath = __outputPath
        self.resultList = None
        self.resultDataFrame = None
        self.csvColumnPrefix = __csvColumnPrefix
        self.use_datetime_format = __use_datetime_format

    @property
    def resultList(self):
        return self.__resultList

    @resultList.setter
    def resultList(self, __list):
        self.__resultList = __list

    @property
    def resultDataFrame(self):
        return self.__resultDataFrame

    @resultDataFrame.setter
    def resultDataFrame(self, __df):
        self.__resultDataFrame = __df

    def readLocalCsvData(self, symbols, __csvPath, __suffix):
        __dict_df: Dict[str, pd.DataFrame] = {}

        for __symbol in symbols:
            try:
                __filePath = __csvPath + __symbol + __suffix + ".csv"
                __df = pd.read_csv(__filePath)
            except FileNotFoundError:
                print(f"Error: {__filePath} not found")
                continue
            else:
                __dict_df[__symbol] = __df
        # print(__dict_df)
        return __dict_df

    def readAssetList(self, __csvPath, __colName="symbol"):
        df = pd.read_csv(__csvPath)
        # print(df.to_string())
        # l_symbol = df[__colName].tolist()
        d_symbol = df.to_dict(orient="list")
        # print(d_symbol)
        return d_symbol

    def getLatestResultFromEachDataFrame(self):
        symbols = self.readAssetList(self.assetListPath)
        # print("------------------",symbols)
        dict_df = self.readLocalCsvData(
            symbols["symbol"], self.csvPath, "_tkxCount"
        )
        list_result = []
        for __symbol, __value in dict_df.items():
            try:
                # check if yahoo finance gives empty data
                if __value.empty:
                    print(
                        f"\n------------ {__symbol} TKx value empty --------------",
                        __value.empty,
                    )
                    continue

                # get latest direction sits at the bottom of dataframe
                __colSize = __value["TKx Signal"].size
                print(
                    "[symbol:",
                    __symbol,
                    ", entries:",
                    __colSize,
                    end="]",
                )
                #  check if column for signals is empty
                # when yahoo receives empty data
                if __colSize == 0:
                    continue
                __tkxDirection = __value["TKx Signal"].iloc[-1]
                __tkxConsecutiveCount = __value["TKx Signal Count"].iloc[-1]
                __index = symbols["symbol"].index(__symbol)
                __symbolName = symbols["name"][__index]
                __date = __value["Date"].iloc[-1]

            except KeyError as e:
                print("------ KeyError ------", e.args)
                continue
            else:
                list_temp = []
                list_temp.append(__date)
                list_temp.append(__symbol)
                list_temp.append(__symbolName)
                list_temp.append(__tkxDirection)
                list_temp.append(__tkxConsecutiveCount)
                list_result.append(list_temp)
        self.resultList = list_result
        return list_result

    def getLatestResultFromEachDataFrame_use_datetime_format(self):
        symbols = self.readAssetList(self.assetListPath)
        # print("------------------",symbols)
        dict_df = self.readLocalCsvData(
            symbols["symbol"], self.csvPath, "_tkxCount"
        )
        list_result = []
        for __symbol, __value in dict_df.items():
            try:
                # check if yahoo finance gives empty data
                if __value.empty:
                    print(
                        f"\n------------ {__symbol} TKx value empty --------------",
                        __value.empty,
                    )
                    continue

                # get latest direction sits at the bottom of dataframe
                __tkxDirection = __value["TKx Signal"].iloc[-1]
                __tkxConsecutiveCount = __value["TKx Signal Count"].iloc[-1]
                __index = symbols["symbol"].index(__symbol)
                __symbolName = symbols["name"][__index]
                __date = __value["Datetime"].iloc[-1]

            except KeyError as e:
                print("------ KeyError ------", e.args)
                continue
            else:
                list_temp = []
                list_temp.append(__date)
                list_temp.append(__symbol)
                list_temp.append(__symbolName)
                list_temp.append(__tkxDirection)
                list_temp.append(__tkxConsecutiveCount)
                list_result.append(list_temp)
        self.resultList = list_result
        return list_result

    def getColumns(self):
        if self.use_datetime_format:
            return [
                "Datetime",
                "Symbol",
                "Name",
                f"{self.csvColumnPrefix} TKx Direction",
                f"{self.csvColumnPrefix} TKx Count",
            ]
        else:
            return [
                "Date",
                "Symbol",
                "Name",
                f"{self.csvColumnPrefix} TKx Direction",
                f"{self.csvColumnPrefix} TKx Count",
            ]

    def exportResult(self, list_result):
        df_result = pd.DataFrame(list_result, columns=self.getColumns())
        df_result.sort_values(
            by=[f"{self.csvColumnPrefix} TKx Count"], inplace=True
        )
        Util.create_folder(self.outputPath)
        df_result.to_csv(
            self.outputPath + self.assetClassName.replace(" ", "") + ".csv",
            index=False,
        )
        self.resultDataFrame = df_result
        return df_result

    def exportResultXML(self, list_result):
        df_result = pd.DataFrame(list_result, columns=self.getColumns())
        df_result.sort_values(
            by=[f"{self.csvColumnPrefix} TKx Count"], inplace=True
        )
        Util.create_folder(self.outputPath)
        df_result_xml = df_result.to_xml(
            self.outputPath + self.assetClassName.replace(" ", "") + ".xml",
            index=False,
        )
        return df_result

    def exportResultJSON(self, list_result):
        df_result = pd.DataFrame(list_result, columns=self.getColumns())
        df_result.sort_values(
            by=[f"{self.csvColumnPrefix} TKx Count"], inplace=True
        )
        Util.create_folder(self.outputPath)
        df_result_xml = df_result.to_json(
            self.outputPath + self.assetClassName.replace(" ", "") + ".json",
            index=False,
            orient="table",
        )
        return df_result


class Control(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def getData(self):
        print(
            "self.model.use_datetime_format::", self.model.use_datetime_format
        )
        if self.model.use_datetime_format is False:
            return self.model.getLatestResultFromEachDataFrame()
        else:
            return (
                self.model.getLatestResultFromEachDataFrame_use_datetime_format()
            )

    def exportResult(self, __list_result):
        return self.model.exportResult(__list_result)

    def exportResultXML(self, __list_result):
        return self.model.exportResultXML(__list_result)

    def exportResultJSON(self, __list_result):
        return self.model.exportResultJSON(__list_result)

    def main(self):
        print(
            f"----------- Creating TKx Signal Aggregator {self.model.csvPath} -----------"
        )
        list_result = self.getData()
        # print(list_result)
        df_result = self.exportResult(list_result)

        # self.exportResultXML(list_result)
        # self.exportResultJSON(list_result)

        # print(df_result)
        # return df_result

        self.view.showResultKCount(self.model.resultDataFrame)
        print(
            f"Aggregator {self.model.assetClassName}.csv and .xml are created\n"
        )


class View(object):
    @staticmethod
    def showResultKCount(__df):
        # print("showResultKCount", __df)
        pass


if __name__ == "__main__":
    _model = Model(
        "data/futurescurrency/d/",
        "asset_list/FuturesCurrency.csv",
        "Futures-D",
    )
    _control = Control(_model, View())
    _control.main()
