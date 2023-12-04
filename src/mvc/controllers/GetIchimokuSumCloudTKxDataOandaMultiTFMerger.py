from src.mvc.core.DataSumCloudTKxSignalMultiTimeframeMerger import (
    Control,
    Model,
    View,
)


def main(run_merger=True):
    if run_merger:
        _model = Model(
            [
                "output/cloud/Oanda-cloud-merged.csv",
                "output/tkx/Oanda-tkx-merged.csv",
            ],
            "output/sum/Oanda-sum-cloud-tkx-merged.csv",
            [
                "Cloud Score Sum",
                "TKx Score Sum",
            ],
            [
                "Total Score Sum",
            ],
            "Oanda instruments Cloud and TKx score page",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
