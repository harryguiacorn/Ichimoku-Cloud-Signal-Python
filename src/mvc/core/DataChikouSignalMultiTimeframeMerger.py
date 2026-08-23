import os

import pandas as pd
from src.mvc.html_creator import TableGenerator


class Model(object):
    def __init__(
        self, input_paths, output_path, direction_count_names, score_names
    ):
        self.input_paths = input_paths
        self.output_path = output_path
        self.direction_count_names = direction_count_names
        self.score_names = score_names

    def main(self):
        merged = None
        for path in self.input_paths:
            if not os.path.exists(path):
                continue
            data = pd.read_csv(path)
            date_columns = [
                column for column in ("Date", "Datetime") if column in data
            ]
            if date_columns:
                data = data.drop(columns=date_columns)
            merged = (
                data
                if merged is None
                else pd.merge(merged, data, on=["Symbol", "Name"])
            )

        if merged is None:
            merged = pd.DataFrame()
        count_columns = [
            count
            for _direction, count in self.direction_count_names
            if count in merged
        ]
        if count_columns:
            merged["Chikou Score Sum"] = (
                merged[count_columns]
                .apply(pd.to_numeric, errors="coerce")
                .fillna(0)
                .sum(axis=1)
            )
        else:
            merged["Chikou Score Sum"] = 0
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        merged.to_csv(self.output_path, index=False)
        html = TableGenerator(self.output_path).generate_html_table(
            "Dow Jones 30 Chikou Multi Timeframe Scan"
        )
        TableGenerator(self.output_path).save_html_table(
            html, self.output_path + ".html"
        )


class Control(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def main(self):
        self.model.main()


class View(object):
    pass
